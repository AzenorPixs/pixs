"""Recu prive de resolution 1.0.0, forme seule, sans fournisseur ni qualification."""
from __future__ import annotations
from dataclasses import dataclass

RESOLUTION_RECEIPT_VERSION = "1.0.0"

_FIELDS = ("binding_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "postcondition_refs", "time_evidence_ref")

_OPAQUES = ("binding_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref")


class ResolutionReceiptError(ValueError):
    pass


def _fail():
    raise ResolutionReceiptError("ResolutionReceipt invalide.") from None


def _opaque(value):
    if value is None:
        _fail()
    if type(value) is not str or value == "" or "\x00" in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail()


def _postconditions(value):
    if type(value) is not tuple:
        _fail()
    for item in value:
        _opaque(item)


@dataclass(frozen=True, slots=True)
class ResolutionReceipt:
    binding_ref: str
    native_operation_ref: str
    native_result_ref: str
    native_snapshot_ref: str
    native_revision_ref: str
    response_digest: str
    origin_proof_ref: str
    postcondition_refs: tuple
    time_evidence_ref: str

    def __post_init__(self):
        for name in _OPAQUES:
            _opaque(getattr(self, name))
        _postconditions(self.postcondition_refs)
        # Limite : la presence des neuf references ne certifie ni snapshot
        # courant, ni origine, ni postconditions, ni droit, ni ordre causal.
        # Aucune phase, date, compteur ou egalite lexicale n etablit une
        # causalite. Aucun champ version/proof_valid/qualified/autorisation,
        # chargement, provider, registre runtime, horloge, appel Kernel/Core/Auth
        # n est deduit de la forme. postcondition_refs garde ordre et doublons
        # proprietaires sans tri, normalisation, conversion ni borne inventee.
        # response_digest reste TEXT opaque sans format HEX64 impose ici.


def resolution_receipt_from_mapping(data):
    if type(data) is not dict:
        _fail()
    for k in data.keys():
        if type(k) is not str:
            _fail()
    if set(data.keys()) != set(_FIELDS):
        _fail()
    return ResolutionReceipt(binding_ref=data["binding_ref"], native_operation_ref=data["native_operation_ref"], native_result_ref=data["native_result_ref"], native_snapshot_ref=data["native_snapshot_ref"], native_revision_ref=data["native_revision_ref"], response_digest=data["response_digest"], origin_proof_ref=data["origin_proof_ref"], postcondition_refs=data["postcondition_refs"], time_evidence_ref=data["time_evidence_ref"])
