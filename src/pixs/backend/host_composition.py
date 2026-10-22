"""Raccord serveur Auth/Core/audit pour l’hôte C07.

Les producteurs publics sont assemblés après configuration Django explicite.
Chaque invocation possède son store et ses faits, sans cache partagé de preuve.
Construire ces objets ne sélectionne aucun profil et ne prouve aucune
disponibilité, autorité courante, migration ou activation applicative.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.core.audit_contracts import AuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.query_source import CoreFactSource
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider

__all__ = ["AuthServerBundle", "build_auth_server_bundle"]

@dataclass(frozen=True, slots=True, repr=False)
class AuthServerBundle:
    alias: str
    peer_alias: str
    profile_id: str
    clock: object
    trust_source: object
    assurance_source: object
    facts_reader: CoreFactSource
    audit: PostgresAuditParticipant
    classification_source: object
    decider_factory: Callable[..., RuntimeAuthorizationDecider]
    service: PostgresLocalAuthService

def build_auth_server_bundle(
    *,
    alias: str,
    peer_alias: str,
    profile_id: str,
    clock: object,
    installation_ref: str,
    base_epoch: str,
    catalog: Catalog,
    limits: Limits,
    policy_source: AuditPolicySource,
    classification_source: object,
) -> AuthServerBundle:
    """Assemble les producteurs sans provisionnement ni verdict de disponibilité."""
    if any(type(v) is not str or not v for v in (alias, peer_alias, profile_id, installation_ref, base_epoch)) or peer_alias == alias:
        raise ValueError("Raccord serveur invalide.")
    for obj, meth in ((policy_source, "resolve"), (classification_source, "resolve"), (clock, "now")):
        if not callable(getattr(obj, meth, None)):
            raise ValueError("Raccord serveur invalide.")
    from django.apps import apps
    from django.conf import settings

    if (
        not settings.configured or not apps.ready
        or not apps.is_installed("pixs.auth")
        or not apps.is_installed("django.contrib.postgres")
    ):
        raise ValueError("Raccord serveur invalide.")

    from pixs.auth.configuration import create_local_auth_sources
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.ports import Request
    from pixs.core.query_source import CoreFactSource
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.core.services_runtime_facts import RuntimeResourceOwner, RuntimeTrustedFactsProvider
    from pixs.core.services_runtime_store import CoreAuthorizationStore

    def _new_store() -> CoreAuthorizationStore:
        return CoreAuthorizationStore(
            alias=alias, installation_ref=installation_ref, base_epoch=base_epoch,
            catalog=catalog, limits=limits,
        )

    # Valider par le contrat propriétaire, sans retenir son cache transactionnel.
    _new_store()

    trust_source, assurance_source = create_local_auth_sources(alias=alias, profile_id=profile_id, clock=clock)
    facts_reader = CoreFactSource()
    audit = PostgresAuditParticipant(policy_source, clock, peer_alias)
    def _decider_factory(*, request: Request, operation_id: str, authentication_source: object) -> RuntimeAuthorizationDecider:
        if type(request) is not Request or type(operation_id) is not str or not operation_id:
            raise ValueError("Raccord serveur invalide.")
        if not callable(getattr(authentication_source, "revalidate", None)) or not callable(getattr(authentication_source, "ownership", None)):
            raise ValueError("Raccord serveur invalide.")
        store = _new_store()
        provider = RuntimeTrustedFactsProvider(
            store=store, authentication_source=authentication_source,
            request=request, operation_id=operation_id,
            additional_owners=(RuntimeResourceOwner("pixs.auth.", authentication_source.ownership),),
        )
        return RuntimeAuthorizationDecider(store=store, facts_provider=provider, clock=clock, request=request, operation_id=operation_id)
    service = PostgresLocalAuthService(
        alias=alias, peer_alias=peer_alias, profile_id=profile_id,
        trust_source=trust_source, assurance_source=assurance_source,
        facts_reader=facts_reader, clock=clock, audit=audit,
        classification_source=classification_source, decider_factory=_decider_factory,
    )
    return AuthServerBundle(
        alias=alias, peer_alias=peer_alias, profile_id=profile_id, clock=clock,
        trust_source=trust_source, assurance_source=assurance_source,
        facts_reader=facts_reader, audit=audit,
        classification_source=classification_source,
        decider_factory=_decider_factory, service=service,
    )
