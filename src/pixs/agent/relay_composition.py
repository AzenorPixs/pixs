"""Enregistrement prive de composition 1.0.0, forme seule, sans fournisseur ni qualification."""
from __future__ import annotations
from dataclasses import dataclass

RELAY_COMPOSITION_VERSION = "1.0.0"

_FIELDS = ("slot", "interface_version", "provider_component", "implementation_ref", "implementation_version", "composition_ref", "qualification_ref")


class RelayCompositionError(ValueError):
    pass


def _fail():
    raise RelayCompositionError("RelayComposition invalide.") from None


def _opaque(value):
    if value is None:
        _fail()
    if type(value) is not str or value == "" or "\x00" in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail()


@dataclass(frozen=True, slots=True)
class RelayComposition:
    slot: str
    interface_version: str
    provider_component: str
    implementation_ref: str
    implementation_version: str
    composition_ref: str
    qualification_ref: str

    def __post_init__(self):
        if type(self.interface_version) is not str or self.interface_version != RELAY_COMPOSITION_VERSION:
            _fail()
        _opaque(self.slot)
        _opaque(self.provider_component)
        _opaque(self.implementation_ref)
        _opaque(self.implementation_version)
        _opaque(self.composition_ref)
        _opaque(self.qualification_ref)
        # Limite : la presence de qualification_ref ne prouve jamais validite,
        # autorisation, resolution, fraicheur ou etat courant. Aucun booleen
        # qualified, chargement, provider, registre runtime, horloge, appel
        # Kernel/Core/Auth n est deduit de la forme. Aucune liste fermee de
        # slot/provider_component ni format de implementation_version impose
        # ici. Aucun tri, normalisation ou conversion des references opaques.


def relay_composition_from_mapping(data):
    if type(data) is not dict:
        _fail()
    for k in data.keys():
        if type(k) is not str:
            _fail()
    if set(data.keys()) != set(_FIELDS):
        _fail()
    return RelayComposition(slot=data["slot"], interface_version=data["interface_version"], provider_component=data["provider_component"], implementation_ref=data["implementation_ref"], implementation_version=data["implementation_version"], composition_ref=data["composition_ref"], qualification_ref=data["qualification_ref"])
