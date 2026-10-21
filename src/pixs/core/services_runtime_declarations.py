"""Validation C04 des déclarations, liée à la transaction propriétaire.

Les reçus privés attestent une validation et la présence des lignes C02 dans
cette transaction. Ils ne constituent jamais une preuve de commit.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass

from django.db import connections

from pixs.core.authz.policy import Policy, PolicyError
from pixs.core.authz.ports import Request
from pixs.core.authz.snapshot import build_snapshot, SnapshotError
from pixs.core.persistence.models_authz import (
    CorePermission, CorePolicy, decode_policy, encode_policy,
)
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, validate_structure
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_runtime_store import CoreAuthorizationStore


@dataclass(frozen=True, slots=True, repr=False)
class _Receipt:
    ref: StagedRef
    physical: object
    pin: tuple
    savepoints: tuple
    kind: str
    data: tuple


class RuntimeDeclarationValidator:
    """Validation seule ; C02 reste propriétaire de l'écriture et du commit."""

    def __init__(self, *, store: CoreAuthorizationStore, request: Request,
                 operation_id: str, owners: tuple[str, ...]) -> None:
        if type(store) is not CoreAuthorizationStore or type(request) is not Request:
            raise CorePortError()
        request.__post_init__()
        validate_structure(request.context)
        self._store, self._request, self._op = store, request, operation_id
        self._literal(operation_id)
        if type(owners) is not tuple or not owners or len(owners) > store.limits.max_selector_values:
            raise CorePortError()
        for owner in owners:
            self._literal(owner)
        if len(set(owners)) != len(owners):
            raise CorePortError()
        self._owners = owners
        self._receipts = {}
        self._mutex = threading.RLock()
        self._transaction = None

    def _literal(self, value):
        if (type(value) is not str or not value
                or len(value) > self._store.limits.max_id_length
                or any(ch in value for ch in "*?[]") or value.startswith("resourceType:")):
            raise CorePortError()

    def _context(self, alias, operation_id, token, context):
        if type(alias) is not str or alias != self._store.alias or operation_id != self._op:
            raise CorePortError()
        self._literal(operation_id)
        self._literal(token)
        if type(context) is not ScopeContext or context != self._request.context:
            raise CorePortError()
        validate_structure(context)
        pin = transaction_identity(alias)
        connection = connections[alias]
        return connection.connection, pin, tuple(connection.savepoint_ids)

    def _prune(self, physical, pin, savepoints):
        key = (physical, pin, savepoints)
        if self._transaction != key:
            self._receipts.clear()
            self._transaction = key

    def _stage(self, alias, operation_id, token, context, kind, data):
        physical, pin, savepoints = self._context(alias, operation_id, token, context)
        with self._mutex:
            self._prune(physical, pin, savepoints)
            if len(self._receipts) >= self._store.limits.max_selector_values:
                raise CorePortError()
            ref = StagedRef(operation_id, alias, token, context, "declaration")
            self._receipts[id(ref)] = _Receipt(ref, physical, pin, savepoints, kind, data)
            return ref

    def validate_permission(self, *, permission_id, owner, resource_ref, action_ref,
                            alias, operation_id, transaction_token, context) -> StagedRef:
        self._context(alias, operation_id, transaction_token, context)
        try:
            self._store.pinned_snapshot(context=context, actor_ref=self._request.subject_id)
        except (PolicyError, SnapshotError) as error:
            raise CorePortError() from error
        for value in (permission_id, owner, resource_ref, action_ref):
            self._literal(value)
        if (owner not in self._owners or resource_ref not in self._store.catalog.resource_ids
                or action_ref not in self._store.catalog.action_ids):
            raise CorePortError()
        if CorePermission.objects.using(alias).filter(permission_id=permission_id).exists():
            raise CorePortError()
        return self._stage(alias, operation_id, transaction_token, context,
                           "permission", (permission_id, owner, resource_ref, action_ref))

    def validate_policy(self, *, policy, alias, operation_id, transaction_token, context) -> StagedRef:
        self._context(alias, operation_id, transaction_token, context)
        if type(policy) is not Policy or policy.owner not in self._owners:
            raise CorePortError()
        try:
            policy.__post_init__()
            for value in (policy.policy_id, policy.policy_version, policy.owner):
                self._literal(value)
            for selector in (policy.subject, policy.resource, policy.action):
                for value in selector.values:
                    self._literal(value)
            snapshot, *_ = self._store.pinned_snapshot(context=context, actor_ref=self._request.subject_id)
            # Le validateur pur contrôle aussi les conditions, assurances, bornes et coûts.
            build_snapshot(snapshot.epoch, (policy,), self._store.catalog, self._store.limits)
        except (PolicyError, SnapshotError) as error:
            raise CorePortError() from error
        # Une version opaque ne permet pas de choisir implicitement la dernière.
        if CorePolicy.objects.using(alias).filter(
                policy_id=policy.policy_id, persistence_state="ACTIVE").exists():
            raise CorePortError()
        if CorePolicy.objects.using(alias).filter(
                policy_id=policy.policy_id, policy_version=policy.policy_version).exists():
            raise CorePortError()
        if CorePolicy.objects.using(alias).filter(persistence_state="ACTIVE").count() >= self._store.limits.max_policies:
            raise CorePortError()
        encoded = encode_policy(policy)
        return self._stage(alias, operation_id, transaction_token, context,
                           "policy", (policy.policy_id, policy.policy_version, encoded))

    def verify_staged(self, proof: TransactionProof) -> None:
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        physical, pin, savepoints = self._context(
            proof.alias, proof.operation_id, proof.transaction_token, proof.context)
        with self._mutex:
            self._prune(physical, pin, savepoints)
            refs = tuple(ref for ref in proof.staged if ref.staged_kind == "declaration")
            if not refs:
                raise CorePortError()
            for ref in refs:
                receipt = self._receipts.get(id(ref))
                if (receipt is None or receipt.ref is not ref or receipt.physical is not physical
                        or receipt.pin != pin or receipt.savepoints != savepoints):
                    raise CorePortError()
                if receipt.kind == "permission":
                    pid, owner, resource, action = receipt.data
                    row = CorePermission.objects.using(proof.alias).select_for_update().filter(
                        permission_id=pid, persistence_state="ACTIVE").first()
                    if row is None or (row.owner, row.resource_ref, row.action_ref) != (owner, resource, action):
                        raise CorePortError()
                elif receipt.kind == "policy":
                    pid, version, encoded = receipt.data
                    row = CorePolicy.objects.using(proof.alias).select_for_update().filter(
                        policy_id=pid, policy_version=version, persistence_state="ACTIVE").first()
                    if row is None:
                        raise CorePortError()
                    try:
                        actual = decode_policy(row.definition)
                        canonical = encode_policy(actual)
                    except PolicyError as error:
                        raise CorePortError() from error
                    if ((row.policy_id, row.policy_version, row.owner, row.effect)
                            != (actual.policy_id, actual.policy_version, actual.owner, actual.effect.value)
                            or canonical != encoded or row.definition != encoded):
                        raise CorePortError()
                else:
                    raise CorePortError()
        return None
