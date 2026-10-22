"""Participant R01 Auth réel ; aucun commit autonome, registre global ni session.

C08 injecte ses ports protégés et partage une seule instance par invocation.
La forme des paramètres ne vaut jamais approbation du plan d'installation.
"""
from __future__ import annotations

import datetime
import hashlib
import hmac
import json
import threading
from dataclasses import dataclass, replace
from urllib.parse import quote
from typing import Protocol
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections, transaction
from pixs.auth.identifiers import parse_identity_reference
from pixs.auth.passwords import envelope_to_ldap
from pixs.auth.r01 import AuthBootstrapError, SignedBootstrapProof, BootstrapTrustPolicy, verify_signed_bootstrap
from pixs.auth.runtime_verifier import _native
from pixs.auth.configuration import (InitialLocalAuthSelection, selection_digest, credential_components_digest, bind_prepared_digest, _stage_initial_configuration, _verify_initial_configuration)
from pixs.core.bootstrap_operator import BootstrapOperatorFacts, BOOTSTRAP_ACTION
from pixs.core.dto import CorePageItem
from pixs.core.ports import CorePortError, StagedRef, TransactionProof, CoreFactReader
from pixs.core.authz.ports import Clock
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel


class AuthBootstrapBackendError(CorePortError):
    def __init__(self):
        ValueError.__init__(self, "Stage R01 Auth non vérifiable.")
        self.code = "AUTH_BOOTSTRAP_BACKEND_INVALID"
        self.element = "auth_bootstrap_backend"
        self.step = "stage_bootstrap"


def _text(value):
    if type(value) is not str or not value or len(value) > 1024:
        raise AuthBootstrapBackendError()


@dataclass(frozen=True, slots=True, repr=False)
class PreparedBootstrapCredential:
    provider_id: str
    issuer: str
    external_subject: str
    password_hash: str
    initial_selection: InitialLocalAuthSelection | None = None
    def __post_init__(self):
        for name in ("provider_id", "issuer", "external_subject"):
            _text(getattr(self, name))
        envelope_to_ldap(self.password_hash)
        if self.initial_selection is not None:
            if type(self.initial_selection) is not InitialLocalAuthSelection:
                raise AuthBootstrapBackendError()
            self.initial_selection.__post_init__()
            if (self.initial_selection.profile.provider_id, self.initial_selection.profile.issuer) != (self.provider_id, self.issuer):
                raise AuthBootstrapBackendError()


def prepared_credential_digest(prepared: PreparedBootstrapCredential) -> str:
    if type(prepared) is not PreparedBootstrapCredential:
        raise AuthBootstrapBackendError()
    prepared.__post_init__()
    component = credential_components_digest(prepared.provider_id, prepared.issuer, prepared.external_subject, prepared.password_hash)
    selected = selection_digest(prepared.initial_selection) if prepared.initial_selection is not None else None
    return bind_prepared_digest(component, selected)


# Nom historique conservé comme alias du contrat Auth partagé.
from pixs.auth.contracts import AuthDataClassification as BootstrapAuthClassification


class BootstrapProofSource(Protocol):
    def resolve(self, proof_ref: str) -> SignedBootstrapProof: ...


class BootstrapTrustPolicySource(Protocol):
    def resolve(self, version: str) -> BootstrapTrustPolicy: ...


class BootstrapClassificationSource(Protocol):
    def resolve(self, *, context: ScopeContext, alias: str, operation_id: str) -> BootstrapAuthClassification: ...


@dataclass(frozen=True, slots=True, repr=False)
class _Stage:
    physical: object
    native: tuple
    savepoints: tuple
    token: str
    operation: str
    authorization_id: object
    authorization_version: int
    signature_sha: str
    prepared_sha: str
    gate_id: object
    binding_id: object
    credential_id: object
    core_version: int
    classification: BootstrapAuthClassification
    configuration: tuple | None = None


def _facts(row):
    return BootstrapOperatorFacts(row.operator_subject_ref,
        "pixs.core.bootstrap:"+quote(row.installation_ref, safe=""), BOOTSTRAP_ACTION,
        ScopeContext(ScopeType.PLATFORM), row.installation_ref, row.plan_version,
        tuple(row.authorized_actions), tuple(row.closed_effects), row.operator_proof_ref,
        row.authorization_ref, row.operation_ref, row.target_identity_ref,
        row.target_tenant_ref, row.plan_sha256, row.valid_from, row.expires_at,
        row.key_id, row.trust_policy_version, row.consumed_operation_ref)


class AuthBootstrapBackend:
    """Implémente les deux ports Core, reçu privé limité à cette invocation."""
    def __init__(self, *, alias: str, proofs: BootstrapProofSource, trust: BootstrapTrustPolicySource, facts_reader: CoreFactReader, classification_source: BootstrapClassificationSource, clock: Clock, prepared: PreparedBootstrapCredential | None):
        _text(alias)
        for port, method in ((proofs, "resolve"), (trust, "resolve"), (facts_reader, "read_facts"), (classification_source, "resolve"), (clock, "now")):
            if not callable(getattr(port, method, None)):
                raise AuthBootstrapBackendError()
        if prepared is not None:
            prepared_credential_digest(prepared)
        self._alias, self._proofs, self._trust, self._facts_reader = alias, proofs, trust, facts_reader
        self._classification, self._clock, self._prepared = classification_source, clock, prepared
        self._verified_ref, self._stage = None, None
        self._mutex = threading.RLock()
        self._closed = False

    def close(self) -> None:
        with self._mutex:
            self._closed, self._stage, self._verified_ref, self._prepared = True, None, None, None

    def _row(self, proof_ref):
        from pixs.auth.models import AuthBootstrapAuthorization
        if self._closed:
            raise AuthBootstrapBackendError()
        query = AuthBootstrapAuthorization.objects.using(self._alias)
        if connections[self._alias].in_atomic_block:
            query = query.select_for_update()
        try:
            row = query.get(operator_proof_ref=proof_ref, persistence_state="ACTIVE")
            row.full_clean(validate_unique=False, validate_constraints=False)
        except (ObjectDoesNotExist, ValidationError):
            raise AuthBootstrapBackendError() from None
        return row

    def _current(self, row):
        proof = self._proofs.resolve(row.operator_proof_ref)
        policy = self._trust.resolve(row.trust_policy_version)
        if type(proof) is not SignedBootstrapProof or type(policy) is not BootstrapTrustPolicy:
            raise AuthBootstrapBackendError()
        try:
            facts = verify_signed_bootstrap(proof, _facts(row), row.challenge_sha256, policy, self._clock.now())
        except AuthBootstrapError as error:
            raise AuthBootstrapBackendError() from error
        return facts, hashlib.sha256(proof.signature).hexdigest()

    def _target(self, facts):
        rows = self._facts_reader.read_facts("IDENTITY", (facts.target_identity_ref,), facts.context, self._alias, 1)
        if type(rows) is not tuple or len(rows) != 1 or type(rows[0]) is not CorePageItem:
            raise AuthBootstrapBackendError()
        row = rows[0]
        row.__post_init__()
        if (row.kind, row.ref, row.context, row.persistence_state) != ("IDENTITY", facts.target_identity_ref, facts.context, "ACTIVE") or dict(row.data).get("state") != "ACTIVE":
            raise AuthBootstrapBackendError()
        if dict(row.data).get("identity_id") != str(parse_identity_reference(facts.target_identity_ref)):
            raise AuthBootstrapBackendError()
        return row

    def _check_stage(self, row, signature_sha, *, _expected_stack=None):
        from pixs.auth import models as m
        stage = self._stage
        if stage is None or self._closed:
            raise AuthBootstrapBackendError()
        physical, native = _native(self._alias)
        if (physical is not stage.physical or native != stage.native
                or tuple(connections[self._alias].savepoint_ids) != (stage.savepoints if _expected_stack is None else _expected_stack)
                or row.pk != stage.authorization_id or row.version != stage.authorization_version
                or row.operation_ref != stage.operation or row.consumed_operation_ref != stage.operation
                or (row.consumed_backend_pid, row.consumed_xid, row.consumed_db_oid, row.consumed_schema_oid) != stage.native
                or row.proof_signature_sha256 != stage.signature_sha or signature_sha != stage.signature_sha
                or row.credential_prepared_digest != stage.prepared_sha):
            raise AuthBootstrapBackendError()
        facts = _facts(row)
        current = self._target(facts)
        classification = self._classification.resolve(context=facts.context, alias=self._alias, operation_id=facts.operation_id)
        if type(classification) is not BootstrapAuthClassification or classification != stage.classification:
            raise AuthBootstrapBackendError()
        gate = m.AuthAccountGate.objects.using(self._alias).get(pk=stage.gate_id)
        binding = m.AuthBinding.objects.using(self._alias).get(pk=stage.binding_id)
        credential = m.AuthPasswordCredential.objects.using(self._alias).get(pk=stage.credential_id)
        if (self._prepared is None or not hmac.compare_digest(prepared_credential_digest(self._prepared), stage.prepared_sha)
                or gate.pk != parse_identity_reference(facts.target_identity_ref) or gate.core_identity_version != current.version
                or current.version != stage.core_version or gate.session_generation != 1 or gate.credential_generation != 1
                or binding.identity_id != gate.pk or credential.binding_id != binding.pk
                or (binding.provider_id, binding.issuer, binding.external_subject) != (self._prepared.provider_id, self._prepared.issuer, self._prepared.external_subject)
                or not hmac.compare_digest(credential.password_hash, self._prepared.password_hash)
                or not binding.enabled or not credential.enabled
                or any(item.version != 1 or item.persistence_state != "ACTIVE" or item.retention_state != "RETAINED" for item in (gate, binding, credential))
                or any(any(getattr(item, key) != value for key, value in classification.values().items()) for item in (gate, binding, credential))):
            raise AuthBootstrapBackendError()
        if self._prepared.initial_selection is not None:
            if stage.configuration is None:
                raise AuthBootstrapBackendError()
            _verify_initial_configuration(ids=stage.configuration, selection=self._prepared.initial_selection, component_sha=credential_components_digest(self._prepared.provider_id, self._prepared.issuer, self._prepared.external_subject, self._prepared.password_hash), authorization=row, gate=gate, credential=credential, token=stage.token, native=stage.native, metadata=classification.values(), alias=self._alias)
        elif stage.configuration is not None:
            raise AuthBootstrapBackendError()
        return None

    def verify(self, *, operator_subject_ref: str, operator_proof_ref: str, plan_version: str, installation_ref: str, context: ScopeContext) -> BootstrapOperatorFacts:
        with self._mutex:
            for value in (operator_subject_ref, operator_proof_ref, plan_version, installation_ref):
                _text(value)
            if type(context) is not ScopeContext or context != ScopeContext(ScopeType.PLATFORM):
                raise AuthBootstrapBackendError()
            row = self._row(operator_proof_ref)
            if (row.operator_subject_ref, row.plan_version, row.installation_ref) != (operator_subject_ref, plan_version, installation_ref):
                raise AuthBootstrapBackendError()
            facts, signature_sha = self._current(row)
            self._verified_ref = operator_proof_ref
            if self._stage is not None and connections[self._alias].in_atomic_block:
                physical, native = _native(self._alias)
                if physical is self._stage.physical and native == self._stage.native:
                    self._check_stage(row, signature_sha)
                    return replace(facts, consumed_operation_id=None)
            return facts

    def stamp(self, *, alias: str, operation_id: str, transaction_token: str, target_identity_ref: str, context: ScopeContext) -> StagedRef:
        from pixs.auth import models as m
        with self._mutex:
            for value in (alias, operation_id, transaction_token, target_identity_ref):
                _text(value)
            if alias != self._alias or self._verified_ref is None or self._prepared is None:
                raise AuthBootstrapBackendError()
            physical, native = _native(alias)
            owner_savepoints = tuple(connections[alias].savepoint_ids)
            row = self._row(self._verified_ref)
            facts, signature_sha = self._current(row)
            if (facts.operation_id, facts.target_identity_ref, facts.context) != (operation_id, target_identity_ref, context):
                raise AuthBootstrapBackendError()
            if self._stage is not None:
                self._check_stage(row, signature_sha)
                if self._stage.token != transaction_token:
                    raise AuthBootstrapBackendError()
                return StagedRef(operation_id, alias, transaction_token, context, "credential")
            if row.consumed_operation_ref is not None or not hmac.compare_digest(row.credential_prepared_digest, prepared_credential_digest(self._prepared)):
                raise AuthBootstrapBackendError()
            target = self._target(facts)
            classification = self._classification.resolve(context=context, alias=alias, operation_id=operation_id)
            if type(classification) is not BootstrapAuthClassification:
                raise AuthBootstrapBackendError()
            metadata = classification.values()
            identity_id = parse_identity_reference(target_identity_ref)
            now = self._clock.now()
            if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc or not facts.valid_from <= now < facts.expires_at:
                raise AuthBootstrapBackendError()
            # Un échec après la première insertion ne peut laisser un stage partiel.
            configuration_ids = None
            with transaction.atomic(using=alias):
                if m.AuthAccountGate.objects.using(alias).filter(pk=identity_id).exists():
                    raise AuthBootstrapBackendError()
                gate = m.AuthAccountGate.objects.using(alias).create(identity_id=identity_id, core_identity_version=target.version, **metadata)
                binding = m.AuthBinding.objects.using(alias).create(identity=gate, provider_id=self._prepared.provider_id, issuer=self._prepared.issuer, external_subject=self._prepared.external_subject, enabled=True, **metadata)
                credential = m.AuthPasswordCredential.objects.using(alias).create(binding=binding, password_hash=self._prepared.password_hash, enabled=True, **metadata)
                row.verified_at, row.proof_signature_sha256 = now, signature_sha
                row.consumed_at, row.consumed_operation_ref = now, operation_id
                row.consumed_backend_pid, row.consumed_xid, row.consumed_db_oid, row.consumed_schema_oid = native
                row.version += 1
                row.updated_at = now
                row.full_clean(validate_unique=False, validate_constraints=False)
                row.save(using=alias, update_fields=["verified_at", "proof_signature_sha256", "consumed_at", "consumed_operation_ref", "consumed_backend_pid", "consumed_xid", "consumed_db_oid", "consumed_schema_oid", "version", "updated_at"])
                if self._prepared.initial_selection is not None:
                    configuration_ids = _stage_initial_configuration(selection=self._prepared.initial_selection, component_sha=credential_components_digest(self._prepared.provider_id, self._prepared.issuer, self._prepared.external_subject, self._prepared.password_hash), authorization=row, gate=gate, credential=credential, token=transaction_token, native=native, metadata=metadata, alias=alias, now=now)
                self._stage = _Stage(physical, native, owner_savepoints, transaction_token, operation_id, row.pk, row.version, signature_sha, row.credential_prepared_digest, gate.pk, binding.pk, credential.pk, target.version, classification, configuration_ids)
                try:
                    self._check_stage(row, signature_sha, _expected_stack=tuple(connections[alias].savepoint_ids))
                except BaseException:
                    # Nettoyage du reçu seulement ; le savepoint annule les écritures.
                    self._stage = None
                    raise
            return StagedRef(operation_id, alias, transaction_token, context, "credential")

    def verify_staged(self, proof: TransactionProof) -> None:
        with self._mutex:
            if type(proof) is not TransactionProof or self._stage is None:
                raise AuthBootstrapBackendError()
            proof.__post_init__()
            expected = StagedRef(self._stage.operation, self._alias, self._stage.token, ScopeContext(ScopeType.PLATFORM), "credential")
            if (proof.operation_id, proof.alias, proof.transaction_token, proof.context) != (expected.operation_id, expected.alias, expected.transaction_token, expected.context) or tuple(ref for ref in proof.staged if ref.staged_kind == "credential") != (expected,):
                raise AuthBootstrapBackendError()
            row = self._row(self._verified_ref)
            _, signature_sha = self._current(row)
            now = self._clock.now()
            if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc or not row.consumed_at <= proof.prepared_at <= now:
                raise AuthBootstrapBackendError()
            self._check_stage(row, signature_sha)
            return None


__all__ = ["AuthBootstrapBackendError", "PreparedBootstrapCredential", "prepared_credential_digest", "BootstrapAuthClassification", "AuthBootstrapBackend", "BootstrapProofSource", "BootstrapTrustPolicySource", "BootstrapClassificationSource"]
