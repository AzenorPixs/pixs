"""Métadonnées R01 lues chez Auth, sans sujet applicatif ni pouvoir d'écriture.

Les sources de preuve et de politique sont fournies par la composition protégée.
Ce lecteur ne publie pas l'autorisation et ne fournit pas ces sources de confiance.
"""
from __future__ import annotations

import os
import threading
import uuid
from dataclasses import dataclass

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.db import connections, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist

from pixs.auth.bootstrap_backend import (
    AuthBootstrapBackendError, BootstrapProofSource, BootstrapTrustPolicySource, _facts)
from pixs.auth.contracts import AuthDataClassification, AuthServiceError
from pixs.auth.identifiers import AuthIdentifierError, require_uuid7
from pixs.auth.r01 import (
    AuthBootstrapError, BootstrapTrustPolicy, SignedBootstrapProof, verify_signed_bootstrap)
from pixs.auth.runtime_verifier import AuthVerificationError, _native
from pixs.core.authz.ports import Clock
from pixs.core.dto import BootstrapActInput, CoreInputInvalid
from pixs.core.bootstrap_operator import BootstrapOperatorError
from pixs.core.ports import CorePortError
from pixs.core.scope.context import (ScopeContext, ScopeType, validate_structure,
                                     ScopeStructureError)
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

__all__ = ["AuthBootstrapMetadataError", "BootstrapAuthorizationMetadata",
           "BootstrapAuthorizationMetadataReader"]


class AuthBootstrapMetadataError(CorePortError):
    def __init__(self):
        ValueError.__init__(self, "Métadonnées R01 Auth non vérifiables.")
        self.code = "AUTH_BOOTSTRAP_METADATA_INVALID"
        self.element = "auth_bootstrap_metadata"
        self.step = "read_bootstrap_metadata"


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapAuthorizationMetadata:
    resource_ref: str
    context: ScopeContext
    owner_component: str
    classification: AuthDataClassification

    def __post_init__(self):
        if (type(self.resource_ref) is not str
                or not self.resource_ref.startswith("pixs.auth.bootstrap:")
                or type(self.context) is not ScopeContext
                or self.context != ScopeContext(ScopeType.PLATFORM)
                or type(self.owner_component) is not str
                or self.owner_component != "pixs.auth"
                or type(self.classification) is not AuthDataClassification):
            raise AuthBootstrapMetadataError()
        try:
            validate_structure(self.context)
        except ScopeStructureError:
            raise AuthBootstrapMetadataError() from None
        raw = self.resource_ref[len("pixs.auth.bootstrap:"):]
        if len(raw) != 36:
            raise AuthBootstrapMetadataError()
        try:
            identifier = uuid.UUID(raw)
            require_uuid7(identifier)
        except (ValueError, AuthIdentifierError):
            raise AuthBootstrapMetadataError() from None
        if str(identifier) != raw:
            raise AuthBootstrapMetadataError()
        try:
            self.classification.values()
        except AuthServiceError:
            raise AuthBootstrapMetadataError() from None


class BootstrapAuthorizationMetadataReader:
    def __init__(self, *, alias: str, act: BootstrapActInput,
                 proofs: BootstrapProofSource, trust: BootstrapTrustPolicySource,
                 clock: Clock) -> None:
        if (type(alias) is not str or not alias or len(alias) > 1024
                or type(act) is not BootstrapActInput):
            raise AuthBootstrapMetadataError()
        try:
            act.__post_init__()
        except CoreInputInvalid:
            raise AuthBootstrapMetadataError() from None
        if act.context != ScopeContext(ScopeType.PLATFORM):
            raise AuthBootstrapMetadataError()
        for port, name in ((proofs, "resolve"), (trust, "resolve"), (clock, "now")):
            if not callable(getattr(port, name, None)):
                raise AuthBootstrapMetadataError()
        self._alias, self._act = alias, act
        self._proofs, self._trust, self._clock = proofs, trust, clock
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._frame = None
        self._closed = False

    @property
    def binding(self) -> tuple[str, BootstrapActInput]:
        """Liaison publique immutable utilisée par la composition serveur."""
        return self._alias, self._act

    def close(self) -> None:
        self._closed = True
        self._frame = None

    def _transaction(self):
        if (self._closed or os.getpid() != self._pid
                or threading.get_ident() != self._thread):
            raise AuthBootstrapMetadataError()
        try:
            connection = connections[self._alias]
            if (connection.vendor != "postgresql" or not connection.in_atomic_block
                    or connection.connection is None
                    or connection.needs_rollback or connection.closed_in_transaction
                    or connection.connection.autocommit is not False):
                raise AuthBootstrapMetadataError()
            physical, native = _native(self._alias)
        except (ConnectionDoesNotExist, DatabaseError, InterfaceError, AuthVerificationError):
            raise AuthBootstrapMetadataError() from None
        if self._frame is None:
            self._frame = (physical, native)
        elif self._frame[0] is not physical or self._frame[1] != native:
            raise AuthBootstrapMetadataError()
        # Ce lecteur ne prépare aucune écriture : les savepoints imbriqués du
        # participant Auth restent permis dans cette même transaction native.
        return physical, native

    def read(self, *, context: ScopeContext, alias: str,
             operation_id: str) -> BootstrapAuthorizationMetadata:
        if (type(context) is not ScopeContext or context != self._act.context
                or type(alias) is not str or alias != self._alias
                or type(operation_id) is not str or operation_id != self._act.operation_id):
            raise AuthBootstrapMetadataError()
        try:
            validate_structure(context)
        except ScopeStructureError:
            raise AuthBootstrapMetadataError() from None
        self._transaction()
        from pixs.auth.models import AuthBootstrapAuthorization

        try:
            row = AuthBootstrapAuthorization.objects.using(alias).select_for_update().get(
                operator_proof_ref=self._act.operator_proof_ref,
                operation_ref=operation_id, persistence_state="ACTIVE")
            row.full_clean(validate_unique=False, validate_constraints=False)
            proof = self._proofs.resolve(row.operator_proof_ref)
            policy = self._trust.resolve(row.trust_policy_version)
            if type(proof) is not SignedBootstrapProof or type(policy) is not BootstrapTrustPolicy:
                raise AuthBootstrapMetadataError()
            facts = verify_signed_bootstrap(
                proof, _facts(row), row.challenge_sha256, policy, self._clock.now())
            for name in ("operator_subject_ref", "operator_proof_ref", "authorization_ref",
                         "installation_ref", "plan_version", "operation_id",
                         "target_identity_ref", "target_tenant_ref", "closed_effects", "context"):
                if getattr(facts, name) != getattr(self._act, name):
                    raise AuthBootstrapMetadataError()
            require_uuid7(row.pk)
            try:
                confidentiality = ConfidentialityLevel(row.confidentiality)
                personal = PersonalDataLevel(row.personal)
            except ValueError:
                raise AuthBootstrapMetadataError() from None
            classification = AuthDataClassification(row.governance_ref, confidentiality, personal)
            result = BootstrapAuthorizationMetadata(
                "pixs.auth.bootstrap:" + str(row.pk),
                ScopeContext(ScopeType.PLATFORM), "pixs.auth", classification)
            result.__post_init__()
        except (ObjectDoesNotExist, MultipleObjectsReturned, ValidationError,
                DatabaseError, InterfaceError, AuthBootstrapError, AuthIdentifierError,
                AuthServiceError, AuthBootstrapBackendError, BootstrapOperatorError):
            raise AuthBootstrapMetadataError() from None
        self._transaction()
        return result
