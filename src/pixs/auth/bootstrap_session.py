"""Session privée R01 Auth : intentions, préparation et challenge, sans autorité.

Une réservation n'est ni une ressource existante ni une autorisation.
Le publisher vérifie les sources réelles avant ses écritures ; cette session
ne prouve aucun commit et ne publie ni confiance ni autorisation SQL.
"""
from __future__ import annotations

import datetime as dt
import hmac
import os
import secrets
import threading
from dataclasses import dataclass
from urllib.parse import quote
import hashlib

from pixs.auth.bootstrap_backend import (
    AuthBootstrapBackend, AuthBootstrapBackendError, PreparedBootstrapCredential)
from pixs.auth.configuration import InitialLocalAuthSelection
from pixs.auth.identifiers import AuthIdentifierError, new_uuid7, parse_identity_reference
from pixs.auth.passwords import AuthPasswordError, hash_password
from pixs.auth.r01 import AuthBootstrapError, canonical_bootstrap_bytes
from pixs.core.bootstrap_operator import (
    BOOTSTRAP_ACTION, BOOTSTRAP_EFFECTS, BOOTSTRAP_WINDOW_SECONDS,
    BootstrapOperatorFacts, BootstrapOperatorError)
from pixs.core.dto import BootstrapActInput, CoreInputInvalid
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.manifest.semver import parse_version

_NO_DRAFT = object()

__all__ = ["AuthBootstrapSessionError", "BootstrapDraft", "BootstrapSigningChallenge",
           "PlannedBootstrapResource", "AuthBootstrapSession"]


class AuthBootstrapSessionError(CorePortError):
    def __init__(self):
        ValueError.__init__(self, "Préparation privée R01 non vérifiable.")
        self.code = "AUTH_BOOTSTRAP_SESSION_INVALID"
        self.element = "auth_bootstrap_session"
        self.step = "prepare_bootstrap"


def _text(value):
    if type(value) is not str or not 0 < len(value) <= 1024 or not value.isprintable():
        raise AuthBootstrapSessionError()


def _hash(value):
    if (type(value) is not str or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value)):
        raise AuthBootstrapSessionError()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapDraft:
    pk: object
    authorization_ref: str
    operator_proof_ref: str
    operation_id: str
    installation_ref: str
    target_identity_ref: str
    closed_effects: tuple[str, ...]
    key_id: str
    trust_policy_version: str


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapSigningChallenge:
    facts: BootstrapOperatorFacts
    nonce: bytes
    canonical_message: bytes
    challenge_sha256: str


@dataclass(frozen=True, slots=True, repr=False)
class PlannedBootstrapResource:
    pk: object
    resource_ref: str
    owner_component: str
    operation_id: str
    installation_ref: str
    target_identity_ref: str
    kind: str


@dataclass(frozen=True, slots=True, repr=False)
class _PublicationMaterial:
    draft: BootstrapDraft
    act: BootstrapActInput
    challenge: BootstrapSigningChallenge
    credential_intent_ref: str | None
    prepared: PreparedBootstrapCredential | None


class AuthBootstrapSession:
    def __init__(self, *, alias: str, clock, max_password_bytes: int):
        _text(alias)
        if (not callable(getattr(clock, "now", None))
                or type(max_password_bytes) is not int or max_password_bytes < 1):
            raise AuthBootstrapSessionError()
        self._alias, self._clock, self._max_password = alias, clock, max_password_bytes
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._mutex = threading.RLock()
        self._closed = False
        self._draft = self._prepared = self._intent = self._act = self._challenge = None
        self._claim = None
        self._publication_state = "NONE"

    def _ownership(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise AuthBootstrapSessionError()

    def _guard(self, draft=_NO_DRAFT):
        self._ownership()
        if self._closed or (draft is not _NO_DRAFT and
                            (type(draft) is not BootstrapDraft or draft is not self._draft)):
            raise AuthBootstrapSessionError()

    @property
    def using(self):
        self._guard()
        return self._alias

    @property
    def clock(self):
        self._guard()
        return self._clock

    def _now(self):
        value = self._clock.now()
        if type(value) is not dt.datetime or value.tzinfo is not dt.timezone.utc:
            raise AuthBootstrapSessionError()
        return value

    def close(self):
        with self._mutex:
            self._ownership()
            self._closed = True
            self._prepared = self._intent = self._claim = None
            self._publication_state = "CLOSED"
        # Libérer les références ne garantit pas l'effacement des str Python.

    def reserve(self, *, operation_id: str, installation_ref: str,
                target_identity_ref: str, closed_effects: tuple[str, ...],
                key_id: str, trust_policy_version: str) -> BootstrapDraft:
        with self._mutex:
            self._guard()
            if self._draft is not None:
                raise AuthBootstrapSessionError()
            for value in (operation_id, installation_ref, key_id, trust_policy_version):
                _text(value)
            try:
                parse_identity_reference(target_identity_ref)
                parse_version(trust_policy_version)
            except (AuthIdentifierError, ValueError):
                raise AuthBootstrapSessionError() from None
            if (type(closed_effects) is not tuple or not closed_effects
                    or any(type(e) is not str or e not in BOOTSTRAP_EFFECTS for e in closed_effects)
                    or len(set(closed_effects)) != len(closed_effects)):
                raise AuthBootstrapSessionError()
            if closed_effects != ("REUSE_EXISTING",):
                if ("REUSE_EXISTING" in closed_effects
                        or any(e not in closed_effects for e in BOOTSTRAP_EFFECTS[:3])):
                    raise AuthBootstrapSessionError()
            try:
                identifier = new_uuid7()
            except AuthIdentifierError:
                raise AuthBootstrapSessionError() from None
            self._draft = BootstrapDraft(
                identifier, "pixs.auth.bootstrap:" + str(identifier),
                "pixs.auth.bootstrap-proof:" + str(identifier),
                operation_id, installation_ref, target_identity_ref, closed_effects,
                key_id, trust_policy_version)
            return self._draft

    def prepare_initial(self, draft: BootstrapDraft, *, password1: str, password2: str,
                        selection: InitialLocalAuthSelection, external_subject: str) -> str:
        with self._mutex:
            self._guard(draft)
            if (self._draft is None or self._prepared is not None or self._challenge is not None
                    or draft.closed_effects == ("REUSE_EXISTING",)
                    or type(selection) is not InitialLocalAuthSelection):
                raise AuthBootstrapSessionError()
            _text(external_subject)
            if (type(password1) is not str or type(password2) is not str
                    or not password1 or len(password1) > self._max_password
                    or len(password2) > self._max_password):
                raise AuthBootstrapSessionError()
            try:
                first, second = password1.encode("utf-8"), password2.encode("utf-8")
            except UnicodeEncodeError:
                raise AuthBootstrapSessionError() from None
            if (len(first) > self._max_password or len(second) > self._max_password
                    or not hmac.compare_digest(first, second)):
                raise AuthBootstrapSessionError()
            try:
                selection.__post_init__()
            except ValueError:
                raise AuthBootstrapSessionError() from None
            if not selection.valid_from <= self._now() < selection.valid_until:
                raise AuthBootstrapSessionError()
            try:
                prepared = PreparedBootstrapCredential(
                    selection.profile.provider_id, selection.profile.issuer, external_subject,
                    hash_password(password1), selection)
                reference = "pixs.auth.credential-intent:" + str(new_uuid7())
            except (AuthPasswordError, AuthBootstrapBackendError, AuthIdentifierError):
                raise AuthBootstrapSessionError() from None
            self._prepared, self._intent = prepared, reference
            return reference

    def bind_plan(self, draft: BootstrapDraft, *, act: BootstrapActInput,
                  plan_sha256: str, credential_intent_ref: str | None) -> BootstrapSigningChallenge:
        with self._mutex:
            self._guard(draft)
            if self._draft is None or type(act) is not BootstrapActInput:
                raise AuthBootstrapSessionError()
            try:
                act.__post_init__()
            except CoreInputInvalid:
                raise AuthBootstrapSessionError() from None
            _hash(plan_sha256)
            if (act.context != ScopeContext(ScopeType.PLATFORM)
                    or (act.operation_id, act.installation_ref, act.target_identity_ref,
                        act.closed_effects, act.authorization_ref, act.operator_proof_ref) !=
                       (draft.operation_id, draft.installation_ref, draft.target_identity_ref,
                        draft.closed_effects, draft.authorization_ref, draft.operator_proof_ref)):
                raise AuthBootstrapSessionError()
            reuse = draft.closed_effects == ("REUSE_EXISTING",)
            if reuse:
                if credential_intent_ref is not None or self._prepared is not None:
                    raise AuthBootstrapSessionError()
            elif (self._prepared is None or type(credential_intent_ref) is not str
                  or credential_intent_ref != self._intent):
                raise AuthBootstrapSessionError()
            now = self._now()
            if not reuse and not (self._prepared.initial_selection.valid_from <= now <
                                  self._prepared.initial_selection.valid_until):
                raise AuthBootstrapSessionError()
            if self._challenge is not None:
                if (self._act != act or self._challenge.facts.plan_sha256 != plan_sha256
                        or not self._challenge.facts.valid_from <= now <
                               self._challenge.facts.expires_at):
                    raise AuthBootstrapSessionError()
                return self._challenge
            try:
                facts = BootstrapOperatorFacts(
                    act.operator_subject_ref, "pixs.core.bootstrap:" + quote(act.installation_ref, safe=""),
                    BOOTSTRAP_ACTION, act.context, act.installation_ref, act.plan_version,
                    (BOOTSTRAP_ACTION,), act.closed_effects, act.operator_proof_ref,
                    act.authorization_ref, act.operation_id, act.target_identity_ref,
                    act.target_tenant_ref, plan_sha256, now,
                    now + dt.timedelta(seconds=BOOTSTRAP_WINDOW_SECONDS),
                    draft.key_id, draft.trust_policy_version, None)
                nonce = secrets.token_bytes(32)
                message = canonical_bootstrap_bytes(facts, nonce)
            except (BootstrapOperatorError, AuthBootstrapError, UnicodeError):
                raise AuthBootstrapSessionError() from None
            challenge = BootstrapSigningChallenge(
                facts, nonce, message, hashlib.sha256(message).hexdigest())
            self._act, self._challenge = act, challenge
            return challenge

    def describe(self, draft: BootstrapDraft) -> PlannedBootstrapResource:
        with self._mutex:
            self._guard(draft)
            if self._draft is None:
                raise AuthBootstrapSessionError()
            return PlannedBootstrapResource(
                draft.pk, "pixs.auth.bootstrap:" + str(draft.pk), "pixs.auth",
                draft.operation_id, draft.installation_ref, draft.target_identity_ref,
                "CREATION_INTENT")

    def _begin_publication(self, draft: BootstrapDraft):
        with self._mutex:
            self._guard(draft)
            if (self._challenge is None or self._act is None
                    or self._publication_state != "NONE"
                    or not self._challenge.facts.valid_from <= self._now() <
                           self._challenge.facts.expires_at):
                raise AuthBootstrapSessionError()
            if self._prepared is not None:
                selection = self._prepared.initial_selection
                if selection is None or not selection.valid_from <= self._now() < selection.valid_until:
                    raise AuthBootstrapSessionError()
            self._claim = object()
            self._publication_state = "PUBLISHING"
            material = _PublicationMaterial(
                draft, self._act, self._challenge, self._intent, self._prepared)
            return self._claim, material

    def _publication_finished(self, draft: BootstrapDraft, claim):
        """État privé, non preuve : seul le publisher appelle après commit connu.

        Le backend vérifiera encore la vraie ligne Auth et les sources courantes.
        Aucun booléen ni reçu client n'est accepté pour annoncer un commit.
        """
        with self._mutex:
            self._guard(draft)
            if self._publication_state != "PUBLISHING" or claim is not self._claim:
                raise AuthBootstrapSessionError()
            self._publication_state = "PUBLISHED"
            self._claim = None

    def _publication_unknown(self, draft: BootstrapDraft, claim):
        with self._mutex:
            self._guard(draft)
            if self._publication_state != "PUBLISHING" or claim is not self._claim:
                raise AuthBootstrapSessionError()
            self._publication_state = "UNKNOWN"
            self._claim = self._prepared = None

    def create_backend(self, *, proofs, trust, facts_reader, classification_source):
        with self._mutex:
            self._guard()
            if self._publication_state != "PUBLISHED" or self._challenge is None:
                raise AuthBootstrapSessionError()
            if self._draft.closed_effects != ("REUSE_EXISTING",) and self._prepared is None:
                raise AuthBootstrapSessionError()
            return AuthBootstrapBackend(
                alias=self._alias, proofs=proofs, trust=trust, facts_reader=facts_reader,
                classification_source=classification_source, clock=self._clock,
                prepared=self._prepared)
