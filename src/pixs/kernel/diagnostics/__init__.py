"""Diagnostics de composition typés (tâche 3.4).

Un ``Diagnostic`` est une chaîne immuable rendue au format historique
``« element : message »`` — les tests et producteurs existants (2.x–3.3)
continuent de la comparer et de la filtrer comme un ``str`` — qui porte en
outre les attributs structurants ``step``, ``element`` et ``constraint``
exigés par la spec kernel (« erreur explicite et diagnostiquable ») et le
design D2 (diagnostics nommant l'élément et la contrainte en cause).

La fabrication depuis les messages hérités ``« chemin : message »`` passe par
``from_legacy`` ; les producteurs de la phase de résolution construisent des
``Diagnostic`` natifs avec l'étape ``resolve``. Aucun texte de diagnostic ne
reproduit de valeur sensible : les producteurs nomment l'élément fautif et la
règle violée, jamais le contenu (tâches 2.3 et 6.3).
"""

from __future__ import annotations

__all__ = [
    "DIAGNOSTIC_STEPS",
    "RESOLVE",
    "VALIDATE",
    "Diagnostic",
]

#: Étapes du pipeline ``discover → validate → resolve → activate`` susceptibles
#: d'émettre des diagnostics en P0. ``activate`` n'a aucun producteur à ce jour.
VALIDATE = "validate"
RESOLVE = "resolve"

DIAGNOSTIC_STEPS = frozenset({VALIDATE, RESOLVE})


class Diagnostic(str):
    """Diagnostic typé : texte ``« element : message »``, étape, élément, contrainte.

    Hérite de ``str`` sans état modifiable : les attributs sont figés à la
    construction (``__slots__`` privés, écriture unique via ``object.__new__``)
    et l'égalité ainsi que le rendu texte restent ceux de la chaîne sous-jacente.
    """

    __slots__ = ("_step", "_element", "_constraint", "_message")

    def __new__(
        cls,
        *,
        step: str,
        element: str,
        constraint: str,
        message: str,
    ) -> "Diagnostic":
        if step not in DIAGNOSTIC_STEPS:
            raise ValueError(
                f"étape de diagnostic inconnue ({step!r}) : "
                f"étapes attendues {sorted(DIAGNOSTIC_STEPS)}"
            )
        if not element or not constraint or not message:
            raise ValueError(
                "un Diagnostic exige step, element, constraint et message non vides"
            )
        instance = super().__new__(cls, f"{element} : {message}")
        object.__setattr__(instance, "_step", step)
        object.__setattr__(instance, "_element", element)
        object.__setattr__(instance, "_constraint", constraint)
        object.__setattr__(instance, "_message", message)
        return instance

    @classmethod
    def from_legacy(cls, step: str, text: str) -> "Diagnostic":
        """Emballe un diagnostic hérité ``« chemin : message »``.

        L'élément est le premier segment avant ``" : "`` ; à défaut de
        séparateur, l'élément générique ``manifest`` est retenu. La contrainte
        est le message de règle violée porté par le texte d'origine ; la valeur
        concernée n'y figure jamais (produits par les garde-fous 2.3).
        """
        element, separator, remainder = str.partition(text, " : ")
        if not separator or not element:
            return cls(
                step=step,
                element="manifest",
                constraint=text,
                message=text,
            )
        return cls(
            step=step,
            element=element,
            constraint=remainder,
            message=remainder,
        )

    @property
    def step(self) -> str:
        """Étape du pipeline émettrice du diagnostic."""
        return self._step

    @property
    def element(self) -> str:
        """Élément en cause (champ du manifest, chemin de dépendance, identifiant)."""
        return self._element

    @property
    def constraint(self) -> str:
        """Contrainte ou règle violée, nommée sans valeur sensible."""
        return self._constraint

    @property
    def message(self) -> str:
        """Message rendu après l'élément, inchangé par rapport à l'origine."""
        return self._message
