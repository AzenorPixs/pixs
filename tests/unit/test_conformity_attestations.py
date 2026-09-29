"""Tests des preuves de conformité externes (tâche 6.7, design D8).

Doubles de preuves explicitement nommés, fixtures synthétiques, valeurs
sentinelles jamais attendues dans les diagnostics (``proof_ref``, suites et
valeurs invalides ne doivent jamais fuiter). Couvre la couverture PASS
complète aux versions distinctes avec build exact, les absences par portée,
les mismatch de fournisseur et de versions, les attestations malformées
sans crash, les doublons ambigus, le non-masquage par une PASS valide, les
preuves supplémentaires de cibles déclarées non résolues, le refus des
cibles résolues non déclarées même accompagnées d'une preuve, la
déduplication des liaisons exigées, le déterminisme et la pureté.
"""

import unittest
from dataclasses import replace

from pixs.kernel.conformity import ConformityAttestation, check_conformity
from pixs.kernel.diagnostics import RESOLVE, Diagnostic
from pixs.kernel.manifest.models import (
    ComponentManifest,
    ImplementedContract,
    ProvidedCapability,
)

SENTINELLE_PREUVE = "SENTINELLE-PREUVE-001"
SENTINELLE_SUITE = "SENTINELLE-SUITE-001"
SENTINELLE_INVALIDE = "SENTINELLE-INVALIDE-999"
VERSION_FALSIFIEE = "9.9.9"


def _manifest(
    component_id: str,
    version: str,
    provides=(),
    implements=(),
) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version=version,
        provided_capabilities=provides,
        implemented_contracts=implements,
    )


SVC = _manifest(
    "t.svc",
    "1.0.0",
    provides=(
        ProvidedCapability(
            id="search",
            version="2.0.0+build.7",
            contracts=(),
            criticality="REQUIRED",
            fallback="none",
        ),
    ),
    implements=(ImplementedContract(id="t.svc.contract", version="3.1.0"),),
)
APP = _manifest(
    "t.app",
    "0.5.0",
    provides=(
        ProvidedCapability(
            id="render",
            version="1.0.0",
            contracts=(),
            criticality="OPTIONAL",
            fallback="t.repli.local",
        ),
    ),
)
MANIFESTS = (SVC, APP)

RESOLVED = (
    ("t.svc", "CAPABILITY", "search", "2.0.0+build.7"),
    ("t.svc", "CONTRACT", "t.svc.contract", "3.1.0"),
)


def _preuve(
    component_id: str,
    component_version: str,
    scope: str,
    target_id: str,
    target_version: str,
    verdict: str = "PASS",
    suite_id: str = "t.suite",
    suite_version: str = "4.0.0",
    proof_ref: str = "t.preuve.001",
) -> ConformityAttestation:
    """Double de preuve explicitement nommé pour les fixtures."""
    return ConformityAttestation(
        component_id=component_id,
        component_version=component_version,
        scope=scope,
        target_id=target_id,
        target_version=target_version,
        suite_id=suite_id,
        suite_version=suite_version,
        verdict=verdict,
        proof_ref=proof_ref,
    )


def _couverture_complete() -> list:
    return [
        _preuve("t.svc", "1.0.0", "COMPONENT", "t.svc", "1.0.0"),
        _preuve("t.app", "0.5.0", "COMPONENT", "t.app", "0.5.0"),
        _preuve("t.svc", "1.0.0", "CAPABILITY", "search", "2.0.0+build.7"),
        _preuve("t.svc", "1.0.0", "CONTRACT", "t.svc.contract", "3.1.0"),
    ]


class TestConformiteExterne(unittest.TestCase):
    def test_couverture_pass_complete_versions_distinctes(self) -> None:
        self.assertEqual(check_conformity(MANIFESTS, RESOLVED, _couverture_complete()), ())

    def test_absence_composant_refusee(self) -> None:
        preuves = [p for p in _couverture_complete() if p.target_id != "t.app"]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 1)
        self._assert_resolve(diagnostics)
        self.assertIn("manquante", diagnostics[0].message)
        self.assertIn("'t.app'", diagnostics[0].message)

    def test_absence_capacite_resolue_refusee(self) -> None:
        preuves = [
            p
            for p in _couverture_complete()
            if not (p.scope == "CAPABILITY" and p.target_id == "search")
        ]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 1)
        self._assert_resolve(diagnostics)
        self.assertIn("manquante", diagnostics[0].message)
        self.assertIn("'search'", diagnostics[0].message)

    def test_absence_contrat_resolu_refuse(self) -> None:
        preuves = [
            p
            for p in _couverture_complete()
            if not (p.scope == "CONTRACT" and p.target_id == "t.svc.contract")
        ]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 1)
        self._assert_resolve(diagnostics)
        self.assertIn("manquante", diagnostics[0].message)

    def test_fournisseur_mismatch_manquant_et_non_declare(self) -> None:
        preuves = _couverture_complete()
        preuves[2] = _preuve(
            "t.app", "0.5.0", "CAPABILITY", "search", "2.0.0+build.7"
        )
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 2)
        manquantes = [d for d in diagnostics if "manquante" in d.message]
        self.assertEqual(len(manquantes), 1)
        self.assertIn("'t.svc'", manquantes[0].message)
        self.assertIn("'search'", manquantes[0].message)
        non_declarees = [d for d in diagnostics if "non déclarée" in d.message]
        self.assertEqual(len(non_declarees), 1)
        self.assertIn("attestation[2]", non_declarees[0].message)
        self._assert_aucune_fuite(diagnostics)

    def test_version_cible_falsifiee_semver_sans_echo(self) -> None:
        preuves = _couverture_complete()
        preuves[2] = _preuve(
            "t.svc",
            "1.0.0",
            "CAPABILITY",
            "search",
            VERSION_FALSIFIEE,
            proof_ref=SENTINELLE_PREUVE,
            suite_id=SENTINELLE_SUITE,
        )
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 2)
        self.assertTrue(
            any("contradictoire" in d.message for d in diagnostics),
            f"mismatch non signalé : {diagnostics}",
        )
        self.assertTrue(
            any("non déclarée" in d.message for d in diagnostics),
            f"cible non déclarée non signalée : {diagnostics}",
        )
        self._assert_aucune_fuite(diagnostics)
        texte = " ; ".join(str(d) for d in diagnostics)
        self.assertNotIn(VERSION_FALSIFIEE, texte)

    def test_version_reellement_malformee_champ_nomme(self) -> None:
        preuves = _couverture_complete()
        preuves[2] = _preuve(
            "t.svc",
            "1.0.0",
            "CAPABILITY",
            "search",
            SENTINELLE_INVALIDE,
            proof_ref=SENTINELLE_PREUVE,
            suite_id=SENTINELLE_SUITE,
        )
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        malformees = [d for d in diagnostics if "target_version" in d.message]
        self.assertEqual(len(malformees), 1)
        self.assertIn("attestation[2]", malformees[0].message)
        self._assert_aucune_fuite(diagnostics)

    def test_build_inexact_mismatch(self) -> None:
        preuves = _couverture_complete()
        preuves[2] = _preuve("t.svc", "1.0.0", "CAPABILITY", "search", "2.0.0")
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertTrue(
            any("contradictoire" in d.message for d in diagnostics),
            f"build inexact non signalé : {diagnostics}",
        )

    def test_version_fournisseur_mismatch(self) -> None:
        preuves = _couverture_complete()
        preuves[0] = _preuve("t.svc", "1.0.1", "COMPONENT", "t.svc", "1.0.1")
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertTrue(
            any("non déclarée" in d.message for d in diagnostics),
            f"version fournisseur non signalée : {diagnostics}",
        )

    def test_build_component_version_mismatch(self) -> None:
        preuves = _couverture_complete()
        preuves[0] = _preuve(
            "t.svc", "1.0.0+build.9", "COMPONENT", "t.svc", "1.0.0+build.9"
        )
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 2)
        self.assertTrue(
            any("contradictoire" in d.message for d in diagnostics),
            f"mismatch build composant non signalé : {diagnostics}",
        )
        self.assertTrue(
            any("non déclarée" in d.message for d in diagnostics),
            f"cible non déclarée non signalée : {diagnostics}",
        )

    def test_cible_component_incoherente(self) -> None:
        preuves = _couverture_complete()
        preuves[0] = _preuve("t.svc", "1.0.0", "COMPONENT", "t.app", "0.5.0")
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 2)
        manquantes = [d for d in diagnostics if "manquante" in d.message]
        self.assertEqual(len(manquantes), 1)
        self.assertIn("'t.svc'", manquantes[0].message)
        non_declarees = [d for d in diagnostics if "non déclarée" in d.message]
        self.assertEqual(len(non_declarees), 1)
        self.assertIn("attestation[0]", non_declarees[0].message)

    def test_mauvais_scope_verdict_chaines_vides(self) -> None:
        base = _couverture_complete()
        cas = [
            _preuve("t.svc", "1.0.0", "SERVICE", "search", "2.0.0+build.7"),
            _preuve(
                "t.svc", "1.0.0", "CAPABILITY", "search", "2.0.0+build.7",
                verdict="FAIL",
            ),
            _preuve("t.svc", "1.0.0", "CAPABILITY", "", "2.0.0+build.7"),
            _preuve("t.svc", "", "COMPONENT", "t.svc", "1.0.0"),
        ]
        for position, mauvaise in enumerate(cas):
            with self.subTest(position=position):
                preuves = base + [mauvaise]
                diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
                self.assertTrue(diagnostics, "aucun refus émis")
                self._assert_aucune_fuite(diagnostics)

    def test_mauvais_types_dans_champs_attestation(self) -> None:
        champs = (
            "component_id",
            "component_version",
            "scope",
            "target_id",
            "target_version",
            "suite_id",
            "suite_version",
            "verdict",
            "proof_ref",
        )
        valeurs = (None, [], {})
        for champ in champs:
            for valeur in valeurs:
                with self.subTest(champ=champ, valeur=type(valeur).__name__):
                    base = _couverture_complete()
                    preuves = base + [replace(base[0], **{champ: valeur})]
                    diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
                    self.assertEqual(len(diagnostics), 1)
                    self.assertIn("attestation[4]", diagnostics[0].message)
                    self.assertIn(champ, diagnostics[0].message)
                    self._assert_aucune_fuite(diagnostics)

    def test_types_invalides_sans_crash(self) -> None:
        base = _couverture_complete()
        for invalide in (None, 42, ["t.svc"], {"scope": "COMPONENT"}, object()):
            with self.subTest(invalide=type(invalide).__name__):
                preuves = base + [invalide]
                diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
                self.assertEqual(len(diagnostics), 1)
                self.assertIn("ConformityAttestation attendu", diagnostics[0].message)

    def test_doublon_liaison_ambigu_refuse(self) -> None:
        preuves = _couverture_complete() + [_preuve(
            "t.svc", "1.0.0", "CONTRACT", "t.svc.contract", "3.1.0",
            suite_id="t.autre-suite", proof_ref="t.preuve.002",
        )]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertTrue(
            any("en double" in d.message for d in diagnostics),
            f"doublon non signalé : {diagnostics}",
        )

    def test_pass_ne_masque_pas_fail(self) -> None:
        preuves = _couverture_complete() + [_preuve(
            "t.svc", "1.0.0", "CONTRACT", "t.svc.contract", "3.1.0",
            verdict="FAIL",
        )]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertTrue(
            any("échec" in d.message for d in diagnostics),
            f"FAIL masqué : {diagnostics}",
        )

    def test_pass_ne_masque_pas_mismatch_valide(self) -> None:
        preuves = _couverture_complete() + [_preuve(
            "t.svc",
            "1.0.0",
            "CAPABILITY",
            "search",
            VERSION_FALSIFIEE,
            proof_ref=SENTINELLE_PREUVE,
            suite_id=SENTINELLE_SUITE,
        )]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 2)
        self.assertTrue(
            any("contradictoire" in d.message for d in diagnostics),
            f"mismatch masqué : {diagnostics}",
        )
        self.assertTrue(
            any("non déclarée" in d.message for d in diagnostics),
            f"cible non déclarée non signalée : {diagnostics}",
        )
        self._assert_aucune_fuite(diagnostics)
        texte = " ; ".join(str(d) for d in diagnostics)
        self.assertNotIn(VERSION_FALSIFIEE, texte)

    def test_pass_ne_masque_pas_malformee(self) -> None:
        preuves = _couverture_complete() + [_preuve(
            "t.svc", "1.0.0", "CAPABILITY", "search", "2.0.0+build.7",
            proof_ref="",
        )]
        diagnostics = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("proof_ref", diagnostics[0].message)

    def test_preuve_supplementaire_declaree_non_resolue_acceptee(self) -> None:
        preuves = _couverture_complete() + [_preuve(
            "t.app", "0.5.0", "CAPABILITY", "render", "1.0.0"
        )]
        self.assertEqual(check_conformity(MANIFESTS, RESOLVED, preuves), ())

    def test_cible_resolue_inconnue_refusee_sans_echo(self) -> None:
        resolved = RESOLVED + (
            ("t.svc", "CAPABILITY", SENTINELLE_INVALIDE, "1.0.0"),
        )
        preuves = _couverture_complete() + [_preuve(
            "t.svc",
            "1.0.0",
            "CAPABILITY",
            SENTINELLE_INVALIDE,
            "1.0.0",
            proof_ref=SENTINELLE_PREUVE,
            suite_id=SENTINELLE_SUITE,
        )]
        diagnostics = check_conformity(MANIFESTS, resolved, preuves)
        self.assertTrue(
            any("cible résolue[2]" in d.message for d in diagnostics),
            f"cible inconnue non signalée : {diagnostics}",
        )
        self._assert_aucune_fuite(diagnostics)

    def test_cible_resolue_version_falsifiee_refusee(self) -> None:
        resolved = (
            ("t.svc", "CAPABILITY", "search", VERSION_FALSIFIEE),
            RESOLVED[1],
        )
        preuves = _couverture_complete()
        preuves[2] = _preuve(
            "t.svc",
            "1.0.0",
            "CAPABILITY",
            "search",
            VERSION_FALSIFIEE,
            proof_ref=SENTINELLE_PREUVE,
            suite_id=SENTINELLE_SUITE,
        )
        diagnostics = check_conformity(MANIFESTS, resolved, preuves)
        self.assertEqual(len(diagnostics), 2)
        self.assertTrue(
            any("cible résolue[0]" in d.message for d in diagnostics),
            f"version falsifiée non signalée : {diagnostics}",
        )
        self.assertTrue(
            any("non déclarée" in d.message for d in diagnostics),
            f"preuve non déclarée non signalée : {diagnostics}",
        )
        self._assert_aucune_fuite(diagnostics)
        texte = " ; ".join(str(d) for d in diagnostics)
        self.assertNotIn(VERSION_FALSIFIEE, texte)

    def test_liaisons_requises_doublonnees_sans_double_preuve(self) -> None:
        resolved = RESOLVED + RESOLVED
        self.assertEqual(
            check_conformity(MANIFESTS, resolved, _couverture_complete()), ()
        )

    def test_determinisme_entrees_inversees(self) -> None:
        preuves = _couverture_complete()
        direct = check_conformity(MANIFESTS, RESOLVED, preuves)
        inverse = check_conformity(
            tuple(reversed(MANIFESTS)),
            tuple(reversed(RESOLVED)),
            list(reversed(preuves)),
        )
        self.assertEqual(direct, ())
        self.assertEqual(inverse, direct)

    def test_absence_effet_de_bord(self) -> None:
        preuves = _couverture_complete()
        avant = (tuple(MANIFESTS), tuple(RESOLVED), list(preuves))
        resultat = check_conformity(MANIFESTS, RESOLVED, preuves)
        self.assertEqual(tuple(MANIFESTS), avant[0])
        self.assertEqual(tuple(RESOLVED), avant[1])
        self.assertEqual(list(preuves), avant[2])
        self.assertIsInstance(resultat, tuple)

    def _assert_resolve(self, diagnostics: tuple) -> None:
        for diagnostic in diagnostics:
            self.assertIsInstance(diagnostic, Diagnostic)
            self.assertEqual(diagnostic.step, RESOLVE)

    def _assert_aucune_fuite(self, diagnostics: tuple) -> None:
        self._assert_resolve(diagnostics)
        texte = " ; ".join(str(diagnostic) for diagnostic in diagnostics)
        for sentinelle in (SENTINELLE_PREUVE, SENTINELLE_SUITE, SENTINELLE_INVALIDE):
            self.assertNotIn(
                sentinelle, texte, f"fuite de {sentinelle} : {texte}"
            )


if __name__ == "__main__":
    unittest.main()
