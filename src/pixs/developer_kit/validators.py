"""Façade locale de validation des manifests (parcours Developer Kit P0).

Point d'entrée public unifié pour valider un ``component.toml`` en local :
``validate_manifest_text`` (pur, sans accès FS) et ``validate_manifest_file``
(fichier exact seulement sur demande explicite de l'appelant). Le résultat
est un ``ValidationReport`` immuable portant soit le ``ComponentManifest``
validé, soit des diagnostics sanitisés ``champ : règle`` ne reproduisant
jamais une valeur, une clé brute, un chemin privé ou une version fournie.

Ports publiés uniquement : ``pixs.kernel.manifest``
(``parse_manifest_text``, ``load_manifest_file``, ``ComponentManifest``,
``ManifestValidationError``) et ``pixs.kernel.diagnostics``
(``Diagnostic``, ``VALIDATE``). La validation sémantique est déléguée au
noyau seul, sans duplication. Aucun parcours de répertoire, aucune
résolution, aucun import, aucune activation, aucun provisionnement, aucune
publication, aucune dépendance nouvelle, aucun secret, aucun réseau.

Limites : validateurs locaux de manifests uniquement ; ni Kit complet, ni
preuve de conformité production. P0 global, runtime et audit durable
restent non prouvés.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest import (
    ComponentManifest,
    ManifestValidationError,
    load_manifest_file,
    parse_manifest_text,
)

__all__ = [
    "ValidationReport",
    "validate_manifest_file",
    "validate_manifest_text",
]

#: Chemins connus générés par le parseur, à chiffres ASCII uniquement et
#: sans plafond arbitraire : racines et sections simples admises, sections
#: de dépendances avec indice optionnel, capacités/contrats avec indice et
#: champ final fermé. Tout élément inconnu (clé hostile, suffixe inventé,
#: chemin privé) est replié vers ``manifest`` sans recopier aucun segment.
_ELEMENT_RE = re.compile(
    r"(?:manifest|schema_version|id|name|type|version|dependencies"
    r"|optional_dependencies|provides|implements"
    r"|dependencies\.(?:components|capabilities|contracts)"
    r"|optional_dependencies\.(?:components|capabilities|contracts)"
    r"|dependencies\.(?:components|capabilities|contracts)\[[0-9]+\]"
    r"|optional_dependencies\.(?:components|capabilities|contracts)\[[0-9]+\]"
    r"|provides\.capabilities|provides\.capabilities\[[0-9]+\]"
    r"|provides\.capabilities\[[0-9]+\]\.(?:id|version|contracts"
    r"|criticality|fallback)"
    r"|implements\.contracts|implements\.contracts\[[0-9]+\]"
    r"|implements\.contracts\[[0-9]+\]\.(?:id|version))"
)

#: Règles fermées, sans valeur. Toute règle inconnue est repliée vers
#: ``entrée invalide``.
_RULES = frozenset(
    {
        "champ obligatoire manquant",
        "champ non déclaré interdit",
        "une chaîne est attendue",
        "une chaîne non vide est attendue",
        "une table est attendue",
        "une table inline est attendue",
        "une liste est attendue",
        "identifiant invalide",
        "entrée de dépendance invalide",
        "SemVer 2.0.0 complète attendue",
        "REQUIRED ou OPTIONAL attendu",
        "valeur explicite 'none' attendue",
        "identifiant déjà déclaré",
        "contrat référencé hors implements du même composant",
        "valeur hors des six types attendue",
        "expression exécutable refusée (aucune logique n'est admissible "
        "dans un manifest)",
        "secret embarqué refusé (seule une référence résolue hors noyau "
        "est admise)",
        "version de schéma non supportée",
        "TOML invalide : décodage impossible",
        "fichier de manifest illisible",
        "document texte invalide",
        "le manifest doit être une table clé/valeur",
        "entrée invalide",
    }
)

_FALLBACK_ELEMENT = "manifest"
_FALLBACK_RULE = "entrée invalide"
_SCHEMA_RULE_PREFIX = "version de schéma non supportée"


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Résultat immuable d'une validation locale de manifest."""

    ok: bool
    manifest: ComponentManifest | None
    diagnostics: tuple[Diagnostic, ...]

    def __post_init__(self) -> None:
        if type(self.ok) is not bool:
            raise ValueError("ValidationReport.ok doit être un bool.")
        if self.manifest is not None and not isinstance(
            self.manifest, ComponentManifest
        ):
            raise ValueError(
                "ValidationReport.manifest doit être un "
                "ComponentManifest ou None."
            )
        if type(self.diagnostics) is not tuple:
            raise ValueError(
                "ValidationReport.diagnostics doit être un tuple "
                "de Diagnostic."
            )
        for item in self.diagnostics:
            if type(item) is not Diagnostic:
                raise ValueError(
                    "ValidationReport.diagnostics doit être un tuple "
                    "de Diagnostic."
                )
        if self.ok:
            if self.manifest is None or self.diagnostics != ():
                raise ValueError(
                    "Un rapport en succès porte le manifest validé "
                    "et aucun diagnostic."
                )
        elif self.manifest is not None or len(self.diagnostics) == 0:
            raise ValueError(
                "Un rapport en échec porte des diagnostics et "
                "aucun manifest."
            )


def _sanitize_one(raw: object) -> Diagnostic:
    """Convertit un diagnostic brut en ``Diagnostic`` sanitisé fermé."""
    if type(raw) is not str or not raw:
        return Diagnostic(
            step=VALIDATE,
            element=_FALLBACK_ELEMENT,
            constraint=_FALLBACK_RULE,
            message=_FALLBACK_RULE,
        )
    if any(mark in raw for mark in ("\n", "\r", "\t", "\x00")):
        return Diagnostic(
            step=VALIDATE,
            element=_FALLBACK_ELEMENT,
            constraint=_FALLBACK_RULE,
            message=_FALLBACK_RULE,
        )
    whole = raw.strip()
    if whole in _RULES:
        # Brut intégral égal à une constante fermée (tel message noyau
        # contenant lui-même « : ») : conservé tel quel, sans découpe ni
        # écho de contenu variable.
        return Diagnostic(
            step=VALIDATE,
            element=_FALLBACK_ELEMENT,
            constraint=whole,
            message=whole,
        )
    element, separator, rule = raw.partition(" : ")
    if not separator:
        element = _FALLBACK_ELEMENT
        rule = raw.strip()
    else:
        element = element.strip()
        rule = rule.strip()
    if rule.startswith(_SCHEMA_RULE_PREFIX):
        # La valeur fournie (reproduite par le parser entre parenthèses)
        # n'est jamais recopiée : seule la règle est conservée.
        rule = _SCHEMA_RULE_PREFIX
    if _ELEMENT_RE.fullmatch(element) is None:
        # Clé inconnue, hostile ou privée : repli sans écho d'aucun segment.
        element = _FALLBACK_ELEMENT
    if rule not in _RULES:
        rule = _FALLBACK_RULE
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=rule,
        message=rule,
    )


def _refuse(diagnostics: tuple) -> ValidationReport:
    if len(diagnostics) == 0:
        diagnostics = (
            Diagnostic(
                step=VALIDATE,
                element=_FALLBACK_ELEMENT,
                constraint=_FALLBACK_RULE,
                message=_FALLBACK_RULE,
            ),
        )
    return ValidationReport(ok=False, manifest=None, diagnostics=diagnostics)


def validate_manifest_text(text: str) -> ValidationReport:
    """Valide un manifest TOML fourni en texte, sans accès FS."""
    if type(text) is not str:
        raise TypeError(
            "validate_manifest_text attend une chaîne TOML (str)."
        )
    try:
        manifest = parse_manifest_text(text)
    except ManifestValidationError as error:
        return _refuse(
            tuple(_sanitize_one(item) for item in error.diagnostics)
        )
    return ValidationReport(ok=True, manifest=manifest, diagnostics=())


def validate_manifest_file(path: Union[str, Path]) -> ValidationReport:
    """Valide exactement le fichier désigné, sans parcours ni import."""
    if not isinstance(path, (str, Path)):
        raise TypeError(
            "validate_manifest_file attend un chemin str ou Path "
            "explicitement fourni par l'appelant."
        )
    try:
        manifest = load_manifest_file(path)
    except ManifestValidationError as error:
        return _refuse(
            tuple(_sanitize_one(item) for item in error.diagnostics)
        )
    except (OSError, UnicodeError, ValueError):
        # Refus d'entrée (illisible, indécodable, chemin NUL ou invalide) :
        # diagnostic fermé sans chemin, sans détail et sans traceback.
        return _refuse(
            (
                Diagnostic(
                    step=VALIDATE,
                    element=_FALLBACK_ELEMENT,
                    constraint="fichier de manifest illisible",
                    message="fichier de manifest illisible",
                ),
            )
        )
    return ValidationReport(ok=True, manifest=manifest, diagnostics=())
