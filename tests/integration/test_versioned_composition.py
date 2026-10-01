"""Tests d'intégration de la composition versionnée (tâches 6.6, design D7).

Exercés via l'API publique ``compose`` avec des doubles d'attestations
synthétiques test-only : versions propres par dimension (aucun proxy de la
version du composant), isolation non bloquante des optionnels, sélection
configurée, choix invalides fermés, préversions et builds au pipeline,
contraintes malformées dans les six groupes, arête unique par fournisseur.
"""

import unittest

from pixs.kernel.composition import compose
from tests.conformity_fixtures import synthetic_attestations


def _toml(
    component_id,
    *,
    component_type="MODULE",
    version="1.0.0",
    dep_components=(),
    dep_capabilities=(),
    dep_contracts=(),
    opt_components=(),
    opt_capabilities=(),
    opt_contracts=(),
    provides=(),
    implements=(),
):
    """Construit un TOML synthétique de composant au schéma 1."""
    lines = [
        "schema_version = \"1\"",
        f"id = \"{component_id}\"",
        f"type = \"{component_type}\"",
        f"version = \"{version}\"",
        "",
    ]
    if dep_components or dep_capabilities or dep_contracts:
        lines.append("[dependencies]")
        if dep_components:
            lines.append(f"components = [{_liste(dep_components)}]")
        if dep_capabilities:
            lines.append(f"capabilities = [{_liste(dep_capabilities)}]")
        if dep_contracts:
            lines.append(f"contracts = [{_liste(dep_contracts)}]")
        lines.append("")
    if opt_components or opt_capabilities or opt_contracts:
        lines.append("[optional_dependencies]")
        if opt_components:
            lines.append(f"components = [{_liste(opt_components)}]")
        if opt_capabilities:
            lines.append(f"capabilities = [{_liste(opt_capabilities)}]")
        if opt_contracts:
            lines.append(f"contracts = [{_liste(opt_contracts)}]")
        lines.append("")
    if provides:
        lines.append("[provides]")
        for cap_id, cap_version, contracts in provides:
            lines.append("[[provides.capabilities]]")
            lines.append(f"id = \"{cap_id}\"")
            lines.append(f"version = \"{cap_version}\"")
            lines.append(f"contracts = [{_liste(contracts)}]")
            lines.append("criticality = \"REQUIRED\"")
            lines.append("fallback = \"none\"")
        lines.append("")
    if implements:
        lines.append("[implements]")
        for contract_id, contract_version in implements:
            lines.append("[[implements.contracts]]")
            lines.append(f"id = \"{contract_id}\"")
            lines.append(f"version = \"{contract_version}\"")
        lines.append("")
    return "\n".join(lines)


def _liste(items):
    return ", ".join(f"\"{item}\"" for item in items)


PROVIDER_TOML = _toml(
    "t.prov",
    component_type="PROVIDER",
    version="9.0.0",
    provides=(("cap", "1.5.0", ()),),
    implements=(("ctr", "2.0.0"),),
)


def _consommateur(**deps):
    return _toml("t.cons", **deps)


class TestVersionsPropresObligatoires(unittest.TestCase):
    def test_satisfaites_active_sans_proxy(self) -> None:
        texts = [
            _consommateur(
                dep_components=("t.prov ==9.0.0",),
                dep_capabilities=("cap ==1.5.0",),
                dep_contracts=("ctr ==2.0.0",),
            ),
            PROVIDER_TOML,
        ]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertIn(("t.cons", "t.prov"), result.edges)
        self.assertLess(result.order.index("t.prov"), result.order.index("t.cons"))

    def test_capacite_insatisfaite_nomme_tout(self) -> None:
        texts = [
            _consommateur(dep_capabilities=("cap ==9.9.9",)),
            PROVIDER_TOML,
        ]
        result = compose(texts)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertTrue(
            any(
                "'t.cons'" in d
                and "'cap'" in d
                and "'cap ==9.9.9'" in d
                and "'1.5.0'" in d
                for d in result.diagnostics
            ),
            f"refus incomplet : {result.diagnostics}",
        )

    def test_contrat_insatisfait_nomme_tout(self) -> None:
        texts = [
            _consommateur(dep_contracts=("ctr >=3.0.0",)),
            PROVIDER_TOML,
        ]
        result = compose(texts)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertTrue(
            any(
                "'t.cons'" in d
                and "'ctr'" in d
                and "'ctr >=3.0.0'" in d
                and "'2.0.0'" in d
                for d in result.diagnostics
            ),
            f"refus incomplet : {result.diagnostics}",
        )

    def test_composant_insatisfait_nomme_tout(self) -> None:
        texts = [
            _consommateur(dep_components=("t.prov <9.0.0",)),
            PROVIDER_TOML,
        ]
        result = compose(texts)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertTrue(
            any(
                "'t.cons'" in d
                and "'t.prov'" in d
                and "'t.prov <9.0.0'" in d
                and "'9.0.0'" in d
                for d in result.diagnostics
            ),
            f"refus incomplet : {result.diagnostics}",
        )


class TestOptionnelsIsoles(unittest.TestCase):
    def test_absents_et_incompatibles_actives_avec_warnings(self) -> None:
        texts = [
            _consommateur(
                opt_components=("t.absent",),
                opt_capabilities=("cap ==9.9.9",),
                opt_contracts=("ctr >=3.0.0",),
            ),
            PROVIDER_TOML,
        ]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertEqual(len(result.warnings), 3)
        for warning in result.warnings:
            self.assertIn("comportement dégradé", str(warning))
        self.assertEqual(result.edges, ())

    def test_compatible_cree_arete_sans_warning(self) -> None:
        texts = [
            _consommateur(opt_capabilities=("cap >=1.0.0",)),
            PROVIDER_TOML,
        ]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertEqual(result.warnings, ())
        self.assertIn(("t.cons", "t.prov"), result.edges)

    def test_optionnels_par_famille_absence_incompatible_succes(self) -> None:
        cas = (
            (
                "components",
                {"opt_components": ("t.absent",)},
                {"opt_components": ("t.prov <9.0.0",)},
                {"opt_components": ("t.prov",)},
                "t.prov",
            ),
            (
                "capabilities",
                {"opt_capabilities": ("fantome",)},
                {"opt_capabilities": ("cap ==9.9.9",)},
                {"opt_capabilities": ("cap >=1.0.0",)},
                "cap",
            ),
            (
                "contracts",
                {"opt_contracts": ("fantome",)},
                {"opt_contracts": ("ctr >=3.0.0",)},
                {"opt_contracts": ("ctr ==2.0.0",)},
                "ctr",
            ),
        )
        for famille, absent, incompatible, succes, cible in cas:
            with self.subTest(famille=famille, cas="absent"):
                texts = [_consommateur(**absent), PROVIDER_TOML]
                result = compose(
                    texts, attestations=synthetic_attestations(texts)
                )
                self.assertTrue(result.activated)
                self.assertEqual(result.diagnostics, ())
                self.assertEqual(len(result.warnings), 1)
                self.assertIn("comportement dégradé", str(result.warnings[0]))
                self.assertNotIn(("t.cons", "t.prov"), result.edges)
            with self.subTest(famille=famille, cas="incompatible"):
                texts = [_consommateur(**incompatible), PROVIDER_TOML]
                result = compose(
                    texts, attestations=synthetic_attestations(texts)
                )
                self.assertTrue(result.activated)
                self.assertEqual(result.diagnostics, ())
                self.assertEqual(len(result.warnings), 1)
                self.assertIn("comportement dégradé", str(result.warnings[0]))
                self.assertNotIn(("t.cons", "t.prov"), result.edges)
            with self.subTest(famille=famille, cas="succes"):
                texts = [_consommateur(**succes), PROVIDER_TOML]
                result = compose(
                    texts, attestations=synthetic_attestations(texts)
                )
                self.assertTrue(result.activated)
                self.assertEqual(result.diagnostics, ())
                self.assertEqual(result.warnings, ())
                self.assertIn(("t.cons", "t.prov"), result.edges)


class TestFournisseurConfigure(unittest.TestCase):
    def _deux_fournisseurs(self):
        cons = _consommateur(dep_capabilities=("audit >=1.0.0 <2.0.0",))
        p1 = _toml(
            "t.p1",
            component_type="PROVIDER",
            provides=(("audit", "1.0.0", ()),),
        )
        p2 = _toml(
            "t.p2",
            component_type="PROVIDER",
            provides=(("audit", "2.0.0", ()),),
        )
        return [cons, p1, p2]

    def test_configure_incompatible_refuse_malgre_autre_compatible(self) -> None:
        texts = self._deux_fournisseurs()
        result = compose(texts, configured_providers={"audit": "t.p2"})
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertTrue(
            any("incompatible" in d and "'audit'" in d for d in result.diagnostics),
            f"refus incomplet : {result.diagnostics}",
        )

    def test_configure_compatible_choisi(self) -> None:
        texts = self._deux_fournisseurs()
        result = compose(
            texts,
            configured_providers={"audit": "t.p1"},
            attestations=synthetic_attestations(texts),
        )
        self.assertTrue(result.activated)
        self.assertIn(("t.cons", "t.p1"), result.edges)
        self.assertNotIn(("t.cons", "t.p2"), result.edges)

    def test_unique_compatible_filtre_les_autres(self) -> None:
        cons = _consommateur(dep_capabilities=("audit >=1.0.0 <2.0.0",))
        p1 = _toml(
            "t.p1", component_type="PROVIDER", provides=(("audit", "1.5.0", ()),)
        )
        p2 = _toml(
            "t.p2", component_type="PROVIDER", provides=(("audit", "9.9.9", ()),)
        )
        texts = [cons, p1, p2]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertTrue(result.activated)
        self.assertIn(("t.cons", "t.p1"), result.edges)

    def test_deux_compatibles_ambigue(self) -> None:
        cons = _consommateur(dep_capabilities=("audit",))
        p1 = _toml(
            "t.p1", component_type="PROVIDER", provides=(("audit", "1.0.0", ()),)
        )
        p2 = _toml(
            "t.p2", component_type="PROVIDER", provides=(("audit", "2.0.0", ()),)
        )
        result = compose([cons, p1, p2])
        self.assertFalse(result.activated)
        self.assertTrue(
            any("ambiguïté" in d for d in result.diagnostics),
            f"ambiguïté non signalée : {result.diagnostics}",
        )

    def test_memes_resultats_manifests_inverses(self) -> None:
        texts = self._deux_fournisseurs()
        first = compose(
            texts,
            configured_providers={"audit": "t.p1"},
            attestations=synthetic_attestations(texts),
        )
        reversed_texts = list(reversed(texts))
        second = compose(
            reversed_texts,
            configured_providers={"audit": "t.p1"},
            attestations=synthetic_attestations(reversed_texts),
        )
        self.assertEqual(first, second)
        self.assertTrue(first.activated)


class TestChoixInvalidesFermes(unittest.TestCase):
    def _textes_audit(self, **deps):
        return [
            _consommateur(**deps),
            _toml(
                "t.p1",
                component_type="PROVIDER",
                provides=(("audit", "1.0.0", ()),),
            ),
        ]

    def test_configures_invalides_sans_echo(self) -> None:
        for portee, deps in (
            ("required", {"dep_capabilities": ("audit",)}),
            ("optional", {"opt_capabilities": ("audit",)}),
        ):
            for valeur in (None, ["t.p1"], {"id": "t.p1"}, "SYNTHETIC-CONFIGURE-001"):
                with self.subTest(
                    portee=portee, valeur=type(valeur).__name__
                ):
                    texts = self._textes_audit(**deps)
                    result = compose(
                        texts, configured_providers={"audit": valeur}
                    )
                    self.assertEqual(result.stage, "resolve")
                    self.assertFalse(result.activated)
                    self.assertEqual(result.warnings, ())
                    texte = " ; ".join(str(d) for d in result.diagnostics)
                    self.assertIn("hors candidats", texte)
                    self.assertNotIn("SYNTHETIC-CONFIGURE-001", texte)

    def test_optionnel_configure_incompatible_fatal(self) -> None:
        cons = _consommateur(opt_capabilities=("audit >=1.0.0 <2.0.0",))
        p1 = _toml(
            "t.p1", component_type="PROVIDER", provides=(("audit", "1.0.0", ()),)
        )
        p2 = _toml(
            "t.p2", component_type="PROVIDER", provides=(("audit", "2.0.0", ()),)
        )
        result = compose(
            [cons, p1, p2], configured_providers={"audit": "t.p2"}
        )
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertEqual(result.warnings, ())
        self.assertTrue(
            any("incompatible" in d for d in result.diagnostics),
            f"configuré optionnel incompatible non fatal : {result.diagnostics}",
        )

    def test_ambiguite_optionnelle_fatale(self) -> None:
        cons = _consommateur(opt_capabilities=("audit",))
        p1 = _toml(
            "t.p1", component_type="PROVIDER", provides=(("audit", "1.0.0", ()),)
        )
        p2 = _toml(
            "t.p2", component_type="PROVIDER", provides=(("audit", "2.0.0", ()),)
        )
        result = compose([cons, p1, p2])
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertEqual(result.warnings, ())
        self.assertTrue(
            any("ambiguïté" in d for d in result.diagnostics),
            f"ambiguïté optionnelle non fatale : {result.diagnostics}",
        )


class TestPreversionsBuildPipeline(unittest.TestCase):
    def test_frontiere_preversion_satisfaite(self) -> None:
        provider = _toml(
            "t.prov",
            component_type="PROVIDER",
            provides=(("cap", "1.0.0-rc.1", ()),),
        )
        texts = [
            _consommateur(dep_capabilities=("cap >=1.0.0-rc.1 <1.0.0",)),
            provider,
        ]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertIn(("t.cons", "t.prov"), result.edges)

    def test_preversion_refusee_pour_stable(self) -> None:
        provider = _toml(
            "t.prov",
            component_type="PROVIDER",
            provides=(("cap", "1.0.0-rc.1", ()),),
        )
        texts = [
            _consommateur(dep_capabilities=("cap >=1.0.0",)),
            provider,
        ]
        result = compose(texts)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertTrue(
            any(
                "'cap'" in d and "'1.0.0-rc.1'" in d
                for d in result.diagnostics
            ),
            f"préversion non refusée : {result.diagnostics}",
        )

    def test_egalite_build_differents_passe(self) -> None:
        provider = _toml(
            "t.prov",
            component_type="PROVIDER",
            implements=(("ctr", "1.0.0+abc"),),
        )
        texts = [
            _consommateur(dep_contracts=("ctr ==1.0.0+xyz",)),
            provider,
        ]
        result = compose(texts, attestations=synthetic_attestations(texts))
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertIn(("t.cons", "t.prov"), result.edges)


class TestContraintesMalformeesSixGroupes(unittest.TestCase):
    def test_malformees_refusees_en_validate(self) -> None:
        toml = (
            "schema_version = \"1\"\n"
            "id = \"t.cons\"\n"
            "type = \"MODULE\"\n"
            "version = \"1.0.0\"\n"
            "[dependencies]\n"
            "components = [\"t.prov ^1.0.0\"]\n"
            "capabilities = [\"cap ~1.0.0\"]\n"
            "contracts = [\"ctr >=1.*\"]\n"
            "[optional_dependencies]\n"
            "components = [\"t.prov ^1.0.0\"]\n"
            "capabilities = [\"cap ~1.0.0\"]\n"
            "contracts = [\"ctr >=1.*\"]\n"
        )
        result = compose([toml])
        self.assertEqual(result.stage, "validate")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(len(result.diagnostics), 6)
        groupes = (
            "dependencies.components",
            "dependencies.capabilities",
            "dependencies.contracts",
            "optional_dependencies.components",
            "optional_dependencies.capabilities",
            "optional_dependencies.contracts",
        )
        for groupe in groupes:
            with self.subTest(groupe=groupe):
                self.assertTrue(
                    any(
                        f"{groupe}[0]" in str(d) and "manifestes[0]" in str(d)
                        for d in result.diagnostics
                    ),
                    f"diagnostic {groupe}[0] + manifestes[0] absent : "
                    f"{result.diagnostics}",
                )


class TestAreteUniqueFournisseur(unittest.TestCase):
    def test_meme_provider_une_seule_arete_ordre_canonique(self) -> None:
        texts = [
            _consommateur(
                dep_components=("t.prov",),
                dep_capabilities=("cap",),
                dep_contracts=("ctr",),
            ),
            PROVIDER_TOML,
        ]
        first = compose(texts, attestations=synthetic_attestations(texts))
        reversed_texts = list(reversed(texts))
        second = compose(
            reversed_texts, attestations=synthetic_attestations(reversed_texts)
        )
        self.assertEqual(first, second)
        self.assertTrue(first.activated)
        self.assertEqual(first.edges, (("t.cons", "t.prov"),))
        self.assertEqual(first.order, ("t.prov", "t.cons"))


if __name__ == "__main__":
    unittest.main()
