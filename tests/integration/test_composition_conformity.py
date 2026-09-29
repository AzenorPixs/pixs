"""Tests d'intégration de la conformité de composition (tâche 6.7, design D8).

Exercés via l'API publique ``compose`` et ``ConformityAttestation``, avec des
doubles explicitement marqués de ``tests.conformity_fixtures`` : couverture
PASS complète, absences par portée, mauvais fournisseur isolé, mismatchs
isolés à versions valides, FAIL/malformée/doublon non masqués, identifiant
seul exigeant quand même des preuves, non-fuite des références, portée P0
exacte. Les preuves sont désignées par liaison exacte
(component_id, scope, target_id), jamais par indice positionnel. Aucune vraie
suite de conformité exécutée, aucune fabrique en production.
"""

import unittest
from dataclasses import replace

from pixs.kernel.composition import compose
from tests.conformity_fixtures import synthetic_attestations

PROVIDER_TOML = """
schema_version = "1"
id = "t.prov"
type = "PROVIDER"
version = "1.0.0+build-a"

[provides]
[[provides.capabilities]]
id = "svc"
version = "1.2.0+cap-a"
contracts = []
criticality = "REQUIRED"
fallback = "none"

[implements]
[[implements.contracts]]
id = "t.svc.contract"
version = "2.0.0+contract-a"
"""

CONSUMER_TOML = """
schema_version = "1"
id = "t.cons"
type = "MODULE"
version = "0.1.0"

[dependencies]
capabilities = ["svc >=1.0.0 <2.0.0"]
contracts = ["t.svc.contract >=2.0.0 <3.0.0"]
"""

BARE_CONSUMER_TOML = """
schema_version = "1"
id = "t.cons"
type = "MODULE"
version = "0.1.0"

[dependencies]
capabilities = ["svc"]
contracts = ["t.svc.contract"]
"""

OTHER_TOML = """
schema_version = "1"
id = "t.other"
type = "MODULE"
version = "0.2.0"

[provides]
[[provides.capabilities]]
id = "svc"
version = "1.2.0+cap-a"
contracts = []
criticality = "REQUIRED"
fallback = "none"
"""

TEXTS = [CONSUMER_TOML, PROVIDER_TOML]

SENTINELLE_PREUVE = "SYNTHETIC-PROOF-007"
SENTINELLE_SUITE = "SYNTHETIC-SUITE-007"


def _selection(preuves, component_id, scope, target_id):
    """Désigne une preuve par liaison exacte (échec si absente ou ambiguë)."""
    trouvees = [
        p
        for p in preuves
        if (p.component_id, p.scope, p.target_id)
        == (component_id, scope, target_id)
    ]
    assert len(trouvees) == 1, (
        f"liaison non unique : {(component_id, scope, target_id)}"
    )
    return trouvees[0]


def _remplace(preuves, component_id, scope, target_id, **champs):
    """Copie la liste en modifiant la preuve désignée par liaison exacte."""
    cible = _selection(preuves, component_id, scope, target_id)
    return [replace(p, **champs) if p is cible else p for p in preuves]


def _preuves_completes():
    return list(synthetic_attestations(TEXTS))


class TestCouvertureCompleteActive(unittest.TestCase):
    def test_pass_complet_graph_ordre_correct(self) -> None:
        result = compose(TEXTS, attestations=synthetic_attestations(TEXTS))
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertIn(("t.cons", "t.prov"), result.edges)
        self.assertLess(
            result.order.index("t.prov"), result.order.index("t.cons")
        )

    def test_identique_deux_ordres_manifests_et_attestations(self) -> None:
        preuves = synthetic_attestations(TEXTS)
        first = compose(TEXTS, attestations=preuves)
        reversed_texts = list(reversed(TEXTS))
        second = compose(
            reversed_texts,
            attestations=tuple(reversed(preuves)),
        )
        self.assertEqual(first, second)
        self.assertTrue(first.activated)


class TestAbsencesRefusees(unittest.TestCase):
    def test_aucune_attestation_refuse(self) -> None:
        result = compose(TEXTS, attestations=())
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertTrue(result.diagnostics)

    def test_manquer_component_capacite_contrat(self) -> None:
        for portee, cible in (
            ("COMPONENT", "t.prov"),
            ("CAPABILITY", "svc"),
            ("CONTRACT", "t.svc.contract"),
        ):
            with self.subTest(portee=portee):
                preuves = [
                    p
                    for p in _preuves_completes()
                    if not (p.scope == portee and p.target_id == cible)
                ]
                result = compose(TEXTS, attestations=preuves)
                self.assertFalse(result.activated)
                self.assertEqual(result.order, ())
                self.assertEqual(result.edges, ())
                self.assertEqual(len(result.diagnostics), 1)
                self.assertIn("manquante", result.diagnostics[0].message)


class TestMauvaisFournisseurIsole(unittest.TestCase):
    def test_cap_autre_fournisseur_declare_refusee(self) -> None:
        texts = [CONSUMER_TOML, PROVIDER_TOML, OTHER_TOML]
        toutes = synthetic_attestations(texts)
        cap_other = _selection(toutes, "t.other", "CAPABILITY", "svc")
        preuves = [
            p for p in toutes if p.scope != "CAPABILITY"
        ] + [cap_other]
        result = compose(
            texts,
            configured_providers={"svc": "t.prov"},
            attestations=preuves,
        )
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertEqual(len(result.diagnostics), 1)
        self.assertIn("manquante", result.diagnostics[0].message)
        self.assertIn("'svc'", result.diagnostics[0].message)
        self.assertIn("'t.prov'", result.diagnostics[0].message)


class TestMismatchsIsoles(unittest.TestCase):
    def _refus_double(self, preuves):
        result = compose(TEXTS, attestations=preuves)
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertEqual(len(result.diagnostics), 2)
        return result

    def test_mismatch_version_composant(self) -> None:
        preuves = _remplace(
            _preuves_completes(),
            "t.cons",
            "COMPONENT",
            "t.cons",
            component_version="9.9.9",
        )
        result = self._refus_double(preuves)
        self.assertTrue(
            any("contradictoire" in d.message for d in result.diagnostics)
        )

    def test_mismatch_version_capacite(self) -> None:
        preuves = _remplace(
            _preuves_completes(),
            "t.prov",
            "CAPABILITY",
            "svc",
            target_version="1.2.0",
        )
        result = self._refus_double(preuves)
        self.assertTrue(
            any("contradictoire" in d.message for d in result.diagnostics)
        )

    def test_mismatch_version_contrat(self) -> None:
        preuves = _remplace(
            _preuves_completes(),
            "t.prov",
            "CONTRACT",
            "t.svc.contract",
            target_version="2.0.0",
        )
        result = self._refus_double(preuves)
        self.assertTrue(
            any("contradictoire" in d.message for d in result.diagnostics)
        )

    def test_mismatch_build_seul(self) -> None:
        cas = (
            ("t.prov", "COMPONENT", "t.prov", {"component_version": "1.0.0+build-b"}),
            ("t.prov", "CAPABILITY", "svc", {"target_version": "1.2.0+cap-b"}),
            (
                "t.prov",
                "CONTRACT",
                "t.svc.contract",
                {"target_version": "2.0.0+contract-b"},
            ),
        )
        for component_id, scope, target_id, champs in cas:
            with self.subTest(scope=scope):
                preuves = _remplace(
                    _preuves_completes(),
                    component_id,
                    scope,
                    target_id,
                    **champs,
                )
                result = self._refus_double(preuves)
                self.assertTrue(
                    any(
                        "contradictoire" in d.message
                        for d in result.diagnostics
                    ),
                    f"mismatch build non signalé : {result.diagnostics}",
                )


class TestEchecMalformeeDoublon(unittest.TestCase):
    def test_fail_remplace_et_ajoute_refuses(self) -> None:
        for mode in ("remplace", "ajoute"):
            with self.subTest(mode=mode):
                base = _preuves_completes()
                contrat = _selection(
                    base, "t.prov", "CONTRACT", "t.svc.contract"
                )
                echec = replace(contrat, verdict="FAIL")
                preuves = (
                    [echec if p is contrat else p for p in base]
                    if mode == "remplace"
                    else base + [echec]
                )
                result = compose(TEXTS, attestations=preuves)
                self.assertFalse(result.activated)
                self.assertEqual(result.order, ())
                self.assertEqual(result.edges, ())
                self.assertTrue(
                    any("échec" in d.message for d in result.diagnostics),
                    f"FAIL masqué ({mode}) : {result.diagnostics}",
                )

    def test_preuve_malformee_champ_vide(self) -> None:
        preuves = _remplace(
            _preuves_completes(),
            "t.prov",
            "CAPABILITY",
            "svc",
            proof_ref="",
        )
        result = compose(TEXTS, attestations=preuves)
        self.assertFalse(result.activated)
        self.assertTrue(
            any("proof_ref" in d.message for d in result.diagnostics),
            f"malformée non signalée : {result.diagnostics}",
        )

    def test_doublon_meme_liaison_ambigu(self) -> None:
        base = _preuves_completes()
        cap = _selection(base, "t.prov", "CAPABILITY", "svc")
        preuves = base + [
            replace(
                cap,
                suite_id="synthetic.autre",
                proof_ref="synthetic:autre",
            )
        ]
        result = compose(TEXTS, attestations=preuves)
        self.assertFalse(result.activated)
        self.assertTrue(
            any("en double" in d.message for d in result.diagnostics),
            f"doublon non signalé : {result.diagnostics}",
        )


class TestIdentifiantSeulExigePreuves(unittest.TestCase):
    def test_nu_sans_preuve_refuse(self) -> None:
        texts = [BARE_CONSUMER_TOML, PROVIDER_TOML]
        result = compose(texts, attestations=())
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        manquantes = [d for d in result.diagnostics if "manquante" in d.message]
        self.assertEqual(len(manquantes), 4)

    def test_nu_avec_preuves_active(self) -> None:
        texts = [BARE_CONSUMER_TOML, PROVIDER_TOML]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())

    def test_ancienne_preuve_non_reutilisable(self) -> None:
        preuves = _remplace(
            _preuves_completes(),
            "t.prov",
            "CAPABILITY",
            "svc",
            target_version="1.0.0",
        )
        result = compose(TEXTS, attestations=preuves)
        self.assertFalse(result.activated)
        self.assertEqual(len(result.diagnostics), 2)


class TestNonFuiteReferences(unittest.TestCase):
    def test_suite_et_preuve_invalides_jamais_exposees(self) -> None:
        preuves = _remplace(
            _preuves_completes(),
            "t.prov",
            "CAPABILITY",
            "svc",
            target_version="1.2.0",
            suite_id=SENTINELLE_SUITE,
            proof_ref=SENTINELLE_PREUVE,
        )
        result = compose(TEXTS, attestations=preuves)
        self.assertFalse(result.activated)
        texte = "\n".join(
            [str(d) for d in result.diagnostics]
            + [str(w) for w in result.warnings]
            + [repr(result)]
        )
        self.assertNotIn(SENTINELLE_PREUVE, texte)
        self.assertNotIn(SENTINELLE_SUITE, texte)


class TestPorteeP0Exposee(unittest.TestCase):
    def test_scopes_dimensions_et_drapeau(self) -> None:
        result = compose(TEXTS, attestations=synthetic_attestations(TEXTS))
        self.assertTrue(result.activated)
        self.assertEqual(
            result.evaluation_scope,
            ("components", "capabilities", "contracts", "conformity"),
        )
        self.assertEqual(
            result.unevaluated_dimensions,
            ("schemas", "migrations", "events", "providers", "clients"),
        )
        self.assertFalse(result.globally_compatible)


if __name__ == "__main__":
    unittest.main()
