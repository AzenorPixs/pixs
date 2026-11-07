"""Observation de transport privee 1.0.0, forme seule, sans fournisseur ni qualification."""
from __future__ import annotations
from dataclasses import dataclass

TRANSPORT_OBSERVATION_VERSION = "1.0.0"

OUTCOMES = ("RECEIPT", "REFUSED_NO_SUBMISSION", "UNKNOWN")

REASONS = ("COMMIT_UNRESOLVED", "BINDING_STALE", "GENERATION_STALE", "CLAIM_STALE", "PROVIDER_UNAVAILABLE", "AUTHORITY_REFUSED", "TIME_IN_DOUBT", "SUBMISSION_UNKNOWN", "RECEIPT_UNVERIFIABLE", "RESULT_DIVERGENT", "IDEMPOTENCE_CONFLICT", "PROFILE_UNAVAILABLE")

_FIELDS = ("attempt_ref", "outcome", "receipt_ref", "native_operation_ref", "detail_ref")

class TransportObservationError(ValueError):
    pass

def _fail():
    raise TransportObservationError("TransportObservation invalide.") from None

def _opaque(value, *, allow_none):
    if value is None:
        if allow_none:
            return
        _fail()
    if type(value) is not str or value == "" or "\x00" in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail()

def require_outcome(value):
    if type(value) is not str or value not in OUTCOMES:
        _fail()
    return value

def require_reason(value):
    if type(value) is not str or value not in REASONS:
        _fail()
    return value

@dataclass(frozen=True, slots=True)
class TransportObservation:
    attempt_ref: str
    outcome: str
    receipt_ref: str | None
    native_operation_ref: str | None
    detail_ref: str | None

    def __post_init__(self):
        if type(self.outcome) is not str or self.outcome not in OUTCOMES:
            _fail()
        _opaque(self.attempt_ref, allow_none=False)
        for name in ("native_operation_ref", "detail_ref"):
            _opaque(getattr(self, name), allow_none=True)
        if self.outcome == "RECEIPT":
            _opaque(self.receipt_ref, allow_none=False)
        else:
            _opaque(self.receipt_ref, allow_none=True)
        # Limite : hors RECEIPT, aucune nullabilite supplementaire imposee ici.
        # verified/proprietaire etabli/preuve de non-soumission/recu authentique,
        # ainsi que toute inference depuis date/phase/timeout/chaine, relevent
        # du vrai fournisseur PZT et ne sont pas deduits de la forme.
        # UNKNOWN peut porter une reference non verifiee sans promotion en RECEIPT.

def transport_observation_from_mapping(data):
    if type(data) is not dict:
        _fail()
    for k in data.keys():
        if type(k) is not str:
            _fail()
    if set(data.keys()) != set(_FIELDS):
        _fail()
    return TransportObservation(attempt_ref=data["attempt_ref"], outcome=data["outcome"], receipt_ref=data["receipt_ref"], native_operation_ref=data["native_operation_ref"], detail_ref=data["detail_ref"])
