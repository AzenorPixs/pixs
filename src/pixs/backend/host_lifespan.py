"""Ressources Auth de l’hôte, avec affinité de thread et fermeture bornée.

Le bundle réel est construit et le profil approuvé relu dans le thread Django.
Les métadonnées de migrations et de tables sont vérifiées sans les modifier.
Ce contexte ne certifie ni disponibilité applicative ni conformité globale.
"""
from __future__ import annotations

import asyncio
from contextlib import AsyncExitStack, ExitStack, asynccontextmanager
from dataclasses import dataclass
import threading

__all__ = ["AuthHostConfig", "HostLifespanError", "host_auth_lifespan"]


class HostLifespanError(ValueError):
    def __init__(self):
        super().__init__("Ressource hôte Auth indisponible.")


@dataclass(frozen=True, slots=True, repr=False)
class AuthHostConfig:
    alias: str
    peer_alias: str
    profile_id: str
    clock: object
    installation_ref: str
    base_epoch: str
    catalog: object
    limits: object
    policy_source: object
    classification_source: object


def _validate(config, context):
    from pixs.core.scope.context import ScopeContext, validate_structure

    if type(config) is not AuthHostConfig or type(context) is not ScopeContext:
        raise HostLifespanError()
    for value in (
        config.alias, config.peer_alias, config.profile_id,
        config.installation_ref, config.base_epoch,
    ):
        if type(value) is not str or not value:
            raise HostLifespanError()
    if config.alias == config.peer_alias:
        raise HostLifespanError()
    validate_structure(context)


class _HostAuthState:
    def __init__(self):
        self._stack = ExitStack()
        self._thread_id = None
        self._release_attempted = False

    def acquire(self, config, context):
        from django.db import connections, transaction
        from pixs.backend.host_composition import build_auth_server_bundle
        from pixs.core.services_authorization_guard import transaction_identity

        if self._thread_id is not None or self._release_attempted:
            raise HostLifespanError()
        self._thread_id = threading.get_ident()
        # Le contrat propriétaire valide les paramètres avant les ouvertures.
        aliases = (config.alias, config.peer_alias)
        wrappers = tuple(connections[alias] for alias in aliases)
        for conn in wrappers:
            if conn.vendor != "postgresql" or conn.in_atomic_block:
                raise HostLifespanError()
        for conn in wrappers:
            # Garder la propriété avant tout constructeur pouvant évoluer.
            if conn.connection is None:
                self._stack.callback(conn.close)
        bundle = build_auth_server_bundle(
            alias=config.alias, peer_alias=config.peer_alias,
            profile_id=config.profile_id, clock=config.clock,
            installation_ref=config.installation_ref, base_epoch=config.base_epoch,
            catalog=config.catalog, limits=config.limits,
            policy_source=config.policy_source,
            classification_source=config.classification_source,
        )
        for conn in wrappers:
            conn.ensure_connection()
            if not conn.get_autocommit() or not conn.is_usable():
                raise HostLifespanError()
        identities = []
        for alias in aliases:
            with transaction.atomic(using=alias):
                identities.append(transaction_identity(alias))
        if identities[0][2:] != identities[1][2:] or identities[0][0] == identities[1][0]:
            raise HostLifespanError()
        self._check_schema(wrappers[0])
        bundle.trust_source.current_profile(context)
        return bundle

    @staticmethod
    def _check_schema(conn):
        from django.apps import apps
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(conn)
        targets = []
        managed_tables = set()
        for label in ("pixs_core", "pixs_auth"):
            app = apps.get_app_config(label)
            leaves = executor.loader.graph.leaf_nodes(label)
            if not leaves:
                raise HostLifespanError()
            targets.extend(leaves)
            for model in app.get_models(include_auto_created=True):
                if model._meta.managed and not model._meta.proxy:
                    managed_tables.add(model._meta.db_table)
        if executor.migration_plan(targets) or not managed_tables:
            raise HostLifespanError()
        with conn.cursor() as cursor:
            actual_tables = set(conn.introspection.table_names(cursor))
        if not managed_tables.issubset(actual_tables):
            raise HostLifespanError()

    def release(self):
        if self._thread_id is None:
            return  # Annulation avant toute acquisition.
        if threading.get_ident() != self._thread_id:
            raise HostLifespanError()
        if self._release_attempted:
            return
        try:
            # ExitStack tente tous les callbacks, même si une fermeture échoue.
            self._stack.close()
        finally:
            self._release_attempted = True


@asynccontextmanager
async def host_auth_lifespan(config: AuthHostConfig, *, context: object):
    """Produit le bundle après observations, puis ferme ses ressources propres."""
    _validate(config, context)
    from asgiref.sync import ThreadSensitiveContext, sync_to_async

    state = _HostAuthState()  # Reste accessible si await acquire est annulé.
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(ThreadSensitiveContext())

        async def cleanup():
            task = asyncio.create_task(sync_to_async(state.release, thread_sensitive=True)())
            interrupted = None
            while not task.done():
                try:
                    await asyncio.shield(task)
                except asyncio.CancelledError as error:
                    interrupted = error
            try:
                task.result()
            except BaseException as error:
                if interrupted is not None:
                    raise interrupted from error
                raise
            if interrupted is not None:
                raise interrupted

        # La fermeture est enregistrée avant le premier await d’acquisition.
        stack.push_async_callback(cleanup)
        bundle = await sync_to_async(state.acquire, thread_sensitive=True)(config, context)
        yield bundle
