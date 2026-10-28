"""Contrat générique pur du temps (T1-A).

Déclaration pure sans autorité sur le temps, le métier ni la
cryptographie ; sans logique métier, sans entrée-sortie, sans
fournisseur ni horloge. Les projections restent des données non
autoritaires : elles ne prouvent aucune admission réelle.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from .models import (
    ContractCategory,
    ContractDescriptor,
    ContractDescriptorError,
)

__all__ = [
    "REFUSAL_REASONS",
    "TIME_CONTRACT_ID",
    "TIME_CONTRACT_VERSION",
    "TIME_DESCRIPTOR",
    "TimeDiagnostic",
    "TimeDoubtError",
    "TimeOutcome",
    "TimeProducer",
    "TimePublicRef",
    "TimeRefusedError",
    "UtcInstant",
    "validate_utc",
]

TIME_CONTRACT_ID = "pixs.time.evidence"
TIME_CONTRACT_VERSION = "2.0.0"

TIME_DESCRIPTOR = ContractDescriptor(
    contract_id=TIME_CONTRACT_ID,
    category=ContractCategory.API,
    version=TIME_CONTRACT_VERSION,
    owner_component="pixs.kernel",
    guarantees_doc=(
        "Déclaration pure du contrat générique de temps, sans autorité "
        "sur le temps, le métier ni la cryptographie ; sans logique "
        "métier, sans entrée-sortie, sans fournisseur ni horloge."
    ),
)

_MSG_REF = "public_ref : texte UTF-8 de 1 à 256 octets sans NUL attendu"
_MSG_OUTCOME = "outcome : membre TimeOutcome attendu"
_MSG_DIAG = "diagnostic : quatre champs exacts attendus"
_MSG_REASON = "reason : motif fermé attendu"
_MSG_STATE = "state_ref : référence publique valide attendue"
_MSG_UTC = "utc : secondes int64 pleine plage et nanos normalisés attendus"

REFUSAL_REASONS = (
    "INVALID_INPUT",
    "FOREIGN_BINDING",
    "NATIVE_PROVENANCE_UNVERIFIED",
    "POLICY_NOT_CURRENT",
    "OPERATOR_NOT_AUTHORIZED",
    "CHALLENGE_NOT_CURRENT",
    "TIME_UNVERIFIABLE",
    "STATE_NOT_CURRENT",
    "ANCHOR_UNVERIFIABLE",
    "MATERIAL_NOT_ADMISSIBLE",
    "CAPABILITY_RETIRED",
    "DEPENDENCY_UNAVAILABLE",
)


def _check_ref_value(value: object) -> bytes:
    """Valide une valeur candidate, sans rien emprunter à l'appelant."""
    if type(value) is not str:
        raise ContractDescriptorError(_MSG_REF)
    if len(value) < 1 or len(value) > 256:
        raise ContractDescriptorError(_MSG_REF)
    try:
        raw = value.encode("utf-8")
    except UnicodeEncodeError:
        raise ContractDescriptorError(_MSG_REF) from None
    if len(raw) < 1 or len(raw) > 256:
        raise ContractDescriptorError(_MSG_REF)
    for char in value:
        code = ord(char)
        if code == 0 or 0xD800 <= code <= 0xDFFF:
            raise ContractDescriptorError(_MSG_REF)
    return raw


@dataclass(frozen=True)
class TimePublicRef:
    """Référence publique non autoritaire, liée à l'opération courante."""

    value: str

    def __post_init__(self) -> None:
        candidate = object.__getattribute__(self, "value")
        _check_ref_value(candidate)


class TimeOutcome(Enum):
    """Trois issues fermées du diagnostic de temps."""

    OBSERVED = "OBSERVED"
    REFUSED = "REFUSED"
    IN_DOUBT = "IN_DOUBT"


@dataclass(frozen=True)
class TimeDiagnostic:
    """Diagnostic exact à quatre champs, sans aucun champ UTC."""

    outcome: TimeOutcome
    producer_ref: TimePublicRef
    clock_domain_ref: TimePublicRef
    detail_ref: TimePublicRef

    def __post_init__(self) -> None:
        try:
            outcome = object.__getattribute__(self, "outcome")
            refs = (
                object.__getattribute__(self, "producer_ref"),
                object.__getattribute__(self, "clock_domain_ref"),
                object.__getattribute__(self, "detail_ref"),
            )
        except AttributeError:
            raise ContractDescriptorError(_MSG_DIAG) from None
        if not any(outcome is member for member in TimeOutcome):
            raise ContractDescriptorError(_MSG_OUTCOME)
        for ref in refs:
            if type(ref) is not TimePublicRef:
                raise ContractDescriptorError(_MSG_DIAG)
            try:
                candidate = object.__getattribute__(ref, "value")
            except AttributeError:
                raise ContractDescriptorError(_MSG_DIAG) from None
            _check_ref_value(candidate)


class TimeRefusedError(ValueError):
    """Échec fermé d'admission, motif exact sans détail d'entrée."""

    def __init__(self, reason: object) -> None:
        if type(reason) is not str:
            raise ContractDescriptorError(_MSG_REASON)
        if reason not in REFUSAL_REASONS:
            raise ContractDescriptorError(_MSG_REASON)
        self.reason = reason
        super().__init__("admission refusée : motif fermé")


class TimeDoubtError(ValueError):
    """Doute fermé, sans motif de refus, état non autoritaire."""

    def __init__(self, state_ref: object) -> None:
        if type(state_ref) is not TimePublicRef:
            raise ContractDescriptorError(_MSG_STATE)
        try:
            candidate = object.__getattribute__(state_ref, "value")
        except AttributeError:
            raise ContractDescriptorError(_MSG_STATE) from None
        _check_ref_value(candidate)
        self.state_ref = state_ref
        super().__init__("admission en doute : état non autoritaire")


def validate_utc(seconds: object, nanos: object) -> None:
    """Valide des secondes int64 pleine plage et des nanos normalisés."""
    if type(seconds) is not int:
        raise ContractDescriptorError(_MSG_UTC)
    if seconds < -(2 ** 63) or seconds > 2 ** 63 - 1:
        raise ContractDescriptorError(_MSG_UTC)
    if type(nanos) is not int:
        raise ContractDescriptorError(_MSG_UTC)
    if nanos < 0 or nanos > 999999999:
        raise ContractDescriptorError(_MSG_UTC)


@dataclass(frozen=True)
class UtcInstant:
    """Paire UTC générique, sans calendrier dans le noyau."""

    seconds: int
    nanos: int

    def __post_init__(self) -> None:
        validate_utc(
            object.__getattribute__(self, "seconds"),
            object.__getattribute__(self, "nanos"),
        )


class TimeProducer(Protocol):
    """Producteur attendu : quatre déclarations, aucune admission offerte."""

    @abstractmethod
    def time_diagnostic(self, use_ref: TimePublicRef) -> TimeDiagnostic:
        """Observe sans admettre."""
        ...

    @abstractmethod
    def time_require_use(self, use_ref: TimePublicRef) -> None:
        """Exige l'usage courant ou lève une erreur fermée."""
        ...

    @abstractmethod
    def time_ceremony_diagnostic(
        self, ceremony_ref: TimePublicRef
    ) -> TimeDiagnostic:
        """Observe la cérémonie sans admettre."""
        ...

    @abstractmethod
    def time_ceremony_require_use(
        self, ceremony_ref: TimePublicRef
    ) -> None:
        """Exige la cérémonie courante ou lève une erreur fermée."""
        ...
