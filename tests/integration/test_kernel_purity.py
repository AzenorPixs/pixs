"""Garde de pureté du noyau : aucun concept métier ni identifiant requis codé en
dur (tâche 4.3, design D4).

Méthode B (arbitrage CGPT) : analyse de l'AST des sources du paquet
``pixs.kernel``, limitée aux constantes littérales de chaînes ``ast.Constant``
EN DEHORS des docstrings. La prose des commentaires et des docstrings est
volontairement ignorée : seuls les littéraux réellement « codés en dur » dans
la logique sont contrôlés. Le noyau ne doit contenir aucun concept métier listé
par la spec ``kernel`` (« Noyau sans logique métier ») et ne doit coder en dur
aucun identifiant de module requis : la règle est portée en données
``required_ids`` par la composition (tâche 4.3).

Les fichiers sont découverts via ``pixs.kernel.__file__`` (aucun chemin absolu
codé en dur, portabilité AGENTS.md §15). Le garde échoue bruyamment s'il
n'inspecte aucune source (il ne peut pas être muet par construction).
"""

from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

import pixs.kernel as kernel_package

# Concepts métier explicitement interdits dans le noyau par la spec kernel.
# Recherche insensible à la casse, bornée par des frontières de mot et
# tolérant le pluriel simple, pour éviter toute correspondance partielle.
FORBIDDEN_BUSINESS_TERMS: tuple[str, ...] = (
    "utilisateur",
    "groupe",
    "acl",
    "organisation",
    "annuaire",
    "oidc",
    "saml",
    "document",
    "flux",
)

# Identifiant que la composition déclare comme requis EN DONNÉES (4.3, D4) :
# jamais codé en dur dans la logique du noyau.
FORBIDDEN_REQUIRED_ID = "pixs.core"

_FORBIDDEN_PATTERNS: dict[str, re.Pattern[str]] = {
    term: re.compile(rf"\b{re.escape(term)}s?\b", re.IGNORECASE)
    for term in FORBIDDEN_BUSINESS_TERMS
}


def _kernel_sources() -> list[Path]:
    """Retourne les sources ``.py`` du paquet noyau, ordonnées et stables."""
    package_dir = Path(kernel_package.__file__).resolve().parent
    return sorted(package_dir.rglob("*.py"))


def _docstring_constant_ids(tree: ast.AST) -> set[int]:
    """Identifiants ``id()`` des constantes de chaîne servant de docstrings."""
    doc_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(
            node,
            (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            body = getattr(node, "body", ())
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                doc_ids.add(id(body[0].value))
    return doc_ids


def _hardcoded_string_literals(path: Path) -> list[str]:
    """Chaînes littérales « codées en dur » d'un module, hors docstrings.

    Les fragments constants des f-string sont couverts (ce sont des
    ``ast.Constant``) ; les valeurs interpolées à l'exécution ne sont pas des
    littéraux source et ne sont donc pas tenues pour « codées en dur ».
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    doc_ids = _docstring_constant_ids(tree)
    literals: list[str] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and id(node) not in doc_ids
        ):
            literals.append(node.value)
    return literals


class TestPureteNoyau(unittest.TestCase):
    def setUp(self) -> None:
        self.sources = _kernel_sources()

    def test_garde_inspecte_reellement_le_noyau(self) -> None:
        self.assertTrue(
            self.sources,
            "aucune source du noyau découverte : le garde serait muet",
        )
        inspectees = sum(
            len(_hardcoded_string_literals(path)) for path in self.sources
        )
        self.assertGreater(
            inspectees,
            0,
            "aucun littéral de chaîne inspecté : le garde serait muet",
        )

    def test_aucun_concept_metier_code_en_dur_dans_le_noyau(self) -> None:
        offenders: list[str] = []
        for path in self.sources:
            for literal in _hardcoded_string_literals(path):
                for term, pattern in _FORBIDDEN_PATTERNS.items():
                    if pattern.search(literal):
                        offenders.append(
                            f"{path.name} : concept métier {term!r} codé en dur"
                        )
        self.assertEqual(
            offenders, [], f"pureté du noyau violée : {offenders}"
        )

    def test_identifiant_requis_non_code_en_dur_dans_le_noyau(self) -> None:
        offenders: list[str] = []
        for path in self.sources:
            for literal in _hardcoded_string_literals(path):
                if FORBIDDEN_REQUIRED_ID in literal:
                    offenders.append(
                        f"{path.name} : identifiant requis "
                        f"{FORBIDDEN_REQUIRED_ID!r} codé en dur"
                    )
        self.assertEqual(
            offenders,
            [],
            f"la règle des composants requis doit rester en données : "
            f"{offenders}",
        )


if __name__ == "__main__":
    unittest.main()
