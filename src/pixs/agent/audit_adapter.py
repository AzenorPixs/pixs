"""Raccord prive Agent vers C05 public : staging verifie, sans confirmation de commit."""
from __future__ import annotations
import datetime
from django.core.exceptions import ValidationError
from django.db import DatabaseError, InterfaceError
from pixs.core.audit_contracts import AuditError
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.authz.decision import Decision
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.authz.ports import PortError
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.audit_event import AuditEvent, validate_audit_event

__all__ = ["AgentAuditError", "AgentAuditAdapter"]


class AgentAuditError(ValueError):
    def __init__(self, code="AGENT_AUDIT_IMPOSSIBLE"):
        super().__init__("Raccord audit Agent impossible.")
        self.code = code
        self.element = "agent_audit"
        self.step = "agent_stage_audit"


def _fail(code):
    raise AgentAuditError(code) from None


def _text(v):
    if type(v) is not str or v == "" or chr(0) in v:
        return False
    try:
        v.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _check_link(alias, operation_id, transaction_token, context):
    if not _text(alias) or not _text(operation_id) or not _text(transaction_token):
        _fail("LIAISON_INVALIDE")
    if type(context) is not ScopeContext:
        _fail("CONTEXTE_INVALIDE")
    try:
        validate_structure(context)
    except ScopeStructureError:
        _fail("CONTEXTE_INVALIDE")


def _owner_now(owner):
    try:
        now = owner.now()
    except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError) as e:
        raise AgentAuditError("HORLOGE_ILLISIBLE") from None
    if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
        _fail("HORLOGE_NON_UTC")
    return now


def _build_verified_ref(owner, *, alias, operation_id, transaction_token, context):
    try:
        ref = StagedRef(operation_id, alias, transaction_token, context, "audit")
    except CorePortError:
        _fail("REFERENCE_INVALIDE")
    now = _owner_now(owner)
    try:
        proof = TransactionProof(operation_id, alias, transaction_token, context, (ref,), now)
    except CorePortError:
        _fail("PREUVE_INVALIDE")
    try:
        outcome = owner.verify_staged(proof)
    except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError):
        _fail("PREUVE_NON_VERIFIEE")
    if outcome is not None:
        _fail("PREUVE_NON_VERIFIEE")
    return ref


class AgentAuditAdapter:
    @property
    def peer_alias(self):
        return self._owner.peer_alias
    def __init__(self, owner):
        if type(owner) is not PostgresAuditParticipant:
            _fail("PROPRIETAIRE_INVALIDE")
        try:
            owner.__post_init__()
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError):
            _fail("PROPRIETAIRE_INVALIDE")
        self._owner = owner
    def stage_generic(self, event, *, alias, operation_id, transaction_token, context):
        _check_link(alias, operation_id, transaction_token, context)
        if type(event) is not AuditEvent:
            _fail("EVENEMENT_INVALIDE")
        if validate_audit_event(event):
            _fail("EVENEMENT_INVALIDE")
        if object.__getattribute__(event, "tenant_reference") != object.__getattribute__(context, "tenant_id"):
            _fail("LIAISON_TENANT_DIVERGENTE")
        try:
            self._owner.stage_generic(event, alias=alias, operation_id=operation_id, transaction_token=transaction_token, context=context)
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError):
            _fail("STAGING_IMPOSSIBLE")
        return _build_verified_ref(self._owner, alias=alias, operation_id=operation_id, transaction_token=transaction_token, context=context)
    def stage_decision(self, event, *, alias, operation_id, transaction_token, context, decision):
        _check_link(alias, operation_id, transaction_token, context)
        if type(event) is not PdpAuditEvent:
            _fail("EVENEMENT_INVALIDE")
        try:
            event.__post_init__()
        except PortError:
            _fail("EVENEMENT_INVALIDE")
        if decision is not None and type(decision) is not Decision:
            _fail("DECISION_INVALIDE")
        try:
            ref = self._owner.stage(event, alias=alias, operation_id=operation_id, transaction_token=transaction_token, context=context, decision=decision)
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError):
            _fail("STAGING_IMPOSSIBLE")
        if type(ref) is not StagedRef:
            _fail("REFERENCE_INVALIDE")
        if object.__getattribute__(ref, "operation_id") != operation_id or object.__getattribute__(ref, "alias") != alias or object.__getattribute__(ref, "transaction_token") != transaction_token or object.__getattribute__(ref, "context") != context:
            _fail("REFERENCE_DIVERGENTE")
        now = _owner_now(self._owner)
        try:
            proof = TransactionProof(operation_id, alias, transaction_token, context, (ref,), now)
        except CorePortError:
            _fail("PREUVE_INVALIDE")
        try:
            outcome = self._owner.verify_staged(proof)
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError):
            _fail("PREUVE_NON_VERIFIEE")
        if outcome is not None:
            _fail("PREUVE_NON_VERIFIEE")
        return ref
    def verify_staged(self, proof):
        if type(proof) is not TransactionProof:
            _fail("PREUVE_INVALIDE")
        try:
            outcome = self._owner.verify_staged(proof)
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ValidationError):
            _fail("PREUVE_NON_VERIFIEE")
        if outcome is not None:
            _fail("PREUVE_NON_VERIFIEE")
        return None
