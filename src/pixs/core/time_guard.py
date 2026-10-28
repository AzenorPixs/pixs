"""Garde locale privee de delegation temps (T1).

Composant strictement prive, non branche. La dependance est fixee
a la construction par la future composition serveuse ; la
construction seule n'atteste jamais ni authentification ni
composition. L'unique methode d'usage recoit seulement une reference
publique, revalide son contenu meme forge, appelle la methode
courante du producteur a chaque usage exactement une fois sans
conserver de methode liee, exige un retour None ou laisse remonter
les erreurs fermees inchangees. Aucun registre partage, choix par
appelant, preuve par conteneur, horodatage local, diagnostic reutilise,
import natif dedie, ni activation. L'horodatage existant est inchange.
La verification de forme de l'appelable ne vaut pas confiance ;
l'absence de vraie composition est inscrite en limites.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pixs.kernel.contracts.models import ContractDescriptorError
from pixs.kernel.contracts.time import TimePublicRef

if TYPE_CHECKING:
    from pixs.kernel.contracts.time import TimeProducer

__all__: list[str] = []

_MSG_PRODUCTEUR = "producteur : objet avec methode time_require_use appelable attendu"
_MSG_REF = "use_ref : reference publique exacte valide attendue"
_MSG_RETOUR = "retour producteur : None attendu, aucune autre valeur"


class _TimeUseGuard:
    """Delegation locale vers le producteur courant, sans autorite propre."""

    def __init__(self, producer: TimeProducer) -> None:
        try:
            candidate = getattr(producer, "time_require_use")
        except AttributeError:
            raise ContractDescriptorError(_MSG_PRODUCTEUR) from None
        if not callable(candidate):
            raise ContractDescriptorError(_MSG_PRODUCTEUR)
        self._producer = producer

    def require_use(self, use_ref: TimePublicRef) -> None:
        if type(use_ref) is not TimePublicRef:
            raise ContractDescriptorError(_MSG_REF)
        try:
            raw = object.__getattribute__(use_ref, "value")
        except AttributeError:
            raise ContractDescriptorError(_MSG_REF) from None
        TimePublicRef(raw)
        try:
            method = getattr(self._producer, "time_require_use")
        except AttributeError:
            raise ContractDescriptorError(_MSG_PRODUCTEUR) from None
        if not callable(method):
            raise ContractDescriptorError(_MSG_PRODUCTEUR)
        result = method(use_ref)
        if result is not None:
            raise ContractDescriptorError(_MSG_RETOUR)
        return None
