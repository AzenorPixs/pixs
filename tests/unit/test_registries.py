"""Tests unitaires des registres génériques du noyau (tâche 4.1, schéma 1).

Critères normés vérifiés : refus d'enregistrement d'une contribution non
déclarée (modèle non validé, propriétaire absent de la composition,
déclaration non tracée dans le manifest) et idempotence d'un double
enregistrement (specs kernel, services, dependencies, extension-contracts) ;
refus en diagnostic typé sans effet sur l'état (tâche 3.4) ; déterminisme de
la construction indépendamment de l'ordre d'entrée ; fermeture des registres
d'événements et de configuration tant que le schéma v1 ne porte aucune source
déclarative.

Au schéma 1, les capacités fournies et contrats implémentés sont des
descripteurs versionnés (``ProvidedCapability``/``ImplementedContract``) aux
versions propres distinctes de la version du composant ; les dépendances de
contrats obligatoires et optionnelles sont dérivées et tracées comme les
autres groupes, et une même cible avec une contrainte complète falsifiée est
refusée sans effet sur le registre.

Fixtures synthétiques stdlib ``unittest``, sans secret ni donnée de
production. Chaque test construit ses propres registres pour exclure tout
partage d'état mutable.
"""

import dataclasses
import unittest

from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest.models import (
    ComponentManifest,
    ImplementedContract,
    ProvidedCapability,
)
from pixs.kernel.registry import (
    REGISTRY_CATEGORIES,
    DependencyEntry,
    ExtensionEntry,
    LifecycleEntry,
    ModuleEntry,
    Registry,
    ServiceEntry,
    build_registries,
)


def _capability(
    capability_id: str,
    version: str = "2.0.0",
    contracts: tuple[str, ...] = (),
    criticality: str = "REQUIRED",
    fallback: str = "none",
) -> ProvidedCapability:
    return ProvidedCapability(
        id=capability_id,
        version=version,
        contracts=contracts,
        criticality=criticality,
        fallback=fallback,
    )


def _contract(contract_id: str, version: str = "3.0.0") -> ImplementedContract:
    return ImplementedContract(id=contract_id, version=version)


def _manifest(
    component_id: str,
    *,
    component_type: str = "MODULE",
    version: str = "1.0.0",
    components: tuple[str, ...] = (),
    capabilities: tuple[str, ...] = (),
    contracts: tuple[str, ...] = (),
    optional_components: tuple[str, ...] = (),
    optional_capabilities: tuple[str, ...] = (),
    optional_contracts: tuple[str, ...] = (),
    provides: tuple[ProvidedCapability, ...] = (),
    implements: tuple[ImplementedContract, ...] = (),
) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type=component_type,
        version=version,
        dependency_components=components,
        dependency_capabilities=capabilities,
        dependency_contracts=contracts,
        optional_dependency_components=optional_components,
        optional_dependency_capabilities=optional_capabilities,
        optional_dependency_contracts=optional_contracts,
        provided_capabilities=provides,
        implemented_contracts=implements,
    )


APP = _manifest(
    "t.app",
    components=("t.lib >=1.0.0",),
    capabilities=("audit",),
    contracts=("t.svc.contract ==1.0.0",),
    optional_components=("t.opt >=0.1.0",),
    optional_capabilities=("notify",),
    optional_contracts=("t.opt.contract",),
    provides=(_capability("app.feature", contracts=("t.app.contract",)),),
    implements=(_contract("t.app.contract", version="1.5.0"),),
)
LIB = _manifest(
    "t.lib",
    provides=(
        _capability("audit", version="1.1.0", contracts=("t.lib.contract",)),
        _capability("metrics", version="1.1.0"),
    ),
    implements=(_contract("t.lib.contract", version="1.1.0"),),
)
EXT = _manifest(
    "t.ext", component_type="EXTENSION", implements=(_contract("audit"),)
)
MANIFESTS = (APP, LIB, EXT)


@dataclasses.dataclass
class ContributionNonFigeée:
    """Modèle non figé : jamais une contribution admissible."""

    owner_id: str
    entry_id: str


class _BaseRegistres(unittest.TestCase):
    def setUp(self) -> None:
        self.registries = build_registries(MANIFESTS)

    def assert_refus(
        self,
        refusals: tuple[Diagnostic, ...],
        element: str,
        constraint_part: str,
    ) -> Diagnostic:
        """Exactement un refus typé nommant élément et contrainte."""
        self.assertEqual(len(refusals), 1, f"refus unique attendu : {refusals}")
        diagnostic = refusals[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, element)
        self.assertIn(constraint_part, diagnostic.constraint)
        self.assertTrue(diagnostic.message)
        return diagnostic


class TestModeleValideFerme(unittest.TestCase):
    def test_categories_closes_sur_sept_registres(self) -> None:
        self.assertEqual(
            REGISTRY_CATEGORIES,
            frozenset(
                {
                    "configuration",
                    "dependencies",
                    "events",
                    "extensions",
                    "lifecycle",
                    "modules",
                    "services",
                }
            ),
        )

    def test_categorie_inconnue_refusee(self) -> None:
        with self.assertRaisesRegex(ValueError, "catégorie de registre inconnue"):
            Registry("metier", ["t.app"])

    def test_objets_non_modeles_refuses(self) -> None:
        registry = Registry("modules", ["t.app"])
        for contribution in ("chaîne", {"owner_id": "t.app", "entry_id": "x"}, 42):
            refusals = registry.register(contribution)
            self.assertEqual(len(refusals), 1, f"refus attendu : {contribution!r}")
            self.assertIn(
                "modèle validé",
                refusals[0].constraint,
            )
        self.assertEqual(registry.entries, ())

    def test_classe_et_non_figee_refusees(self) -> None:
        registry = Registry("modules", ["t.app"])
        refusals = registry.register(ModuleEntry)
        self.assertEqual(len(refusals), 1)
        self.assertIn("modèle validé", refusals[0].constraint)
        refusals = registry.register(ContributionNonFigeée("t.app", "x"))
        self.assertEqual(len(refusals), 1)
        self.assertIn("ContributionNonFigeée", refusals[0].message)
        self.assertEqual(registry.entries, ())

    def test_champs_identifiants_vides_refuses(self) -> None:
        registry = Registry("modules", ["t.app"])
        refusals = registry.register(
            ModuleEntry("t.app", "", "MODULE", "1.0.0")
        )
        self.assertEqual(len(refusals), 1)
        self.assertIn("owner_id et entry_id non vides", refusals[0].constraint)
        self.assertEqual(registry.entries, ())


class TestRefusContributionNonDeclaree(_BaseRegistres):
    def test_proprietaire_absent_de_la_composition(self) -> None:
        before = self.registries.modules.entries
        refusal = self.assert_refus(
            self.registries.modules.register(
                ModuleEntry("t.fantome", "t.fantome", "MODULE", "1.0.0")
            ),
            "registres.modules",
            "composant déclarant présent dans la composition validée",
        )
        self.assertIn("'t.fantome'", str(refusal))
        self.assertEqual(self.registries.modules.entries, before)

    def test_service_non_declare_par_proprietaire(self) -> None:
        before = self.registries.services.entries
        self.assert_refus(
            self.registries.services.register(
                ServiceEntry("t.lib", "contrat-fantasme", "implements")
            ),
            "registres.services",
            "service déclaré par son propriétaire",
        )
        self.assertEqual(self.registries.services.entries, before)

    def test_service_source_inconnue_refusee(self) -> None:
        self.assert_refus(
            self.registries.services.register(
                ServiceEntry("t.lib", "audit", "improvisee")
            ),
            "registres.services",
            "service déclaré par son propriétaire",
        )

    def test_type_d_entree_croise_refuse(self) -> None:
        refusal = self.assert_refus(
            self.registries.services.register(LifecycleEntry("t.lib", "t.lib")),
            "registres.services",
            "contribution de type ServiceEntry",
        )
        self.assertIn("reçu LifecycleEntry", str(refusal))

    def test_module_incoherent_avec_son_manifest_refuse(self) -> None:
        self.assert_refus(
            self.registries.modules.register(
                ModuleEntry("t.app", "t.app", "MODULE", "9.9.9")
            ),
            "registres.modules",
            "module enregistré exactement comme déclaré",
        )

    def test_extension_non_extension_refusee(self) -> None:
        self.assert_refus(
            self.registries.extensions.register(
                ExtensionEntry("t.app", "t.app", "1.0.0")
            ),
            "registres.extensions",
            "extension auto-déclarée par un composant de type EXTENSION",
        )

    def test_extension_version_divergente_refusee(self) -> None:
        self.assert_refus(
            self.registries.extensions.register(
                ExtensionEntry("t.ext", "t.ext", "9.9.9")
            ),
            "registres.extensions",
            "extension auto-déclarée par un composant de type EXTENSION",
        )

    def test_entree_cycle_de_vie_non_auto_declaree_refusee(self) -> None:
        self.assert_refus(
            self.registries.lifecycle.register(
                LifecycleEntry("t.app", "t.lib")
            ),
            "registres.lifecycle",
            "auto-déclarée par son composant",
        )

    def test_dependance_non_declaree_refusee(self) -> None:
        self.assert_refus(
            self.registries.dependencies.register(
                DependencyEntry("t.app", "t.inconnue", "components", True, "t.inconnue")
            ),
            "registres.dependencies",
            "dépendance tracée dans le manifest du composant consommateur",
        )

    def test_dependance_optionnelle_presentee_comme_obligatoire_refusee(
        self,
    ) -> None:
        self.assert_refus(
            self.registries.dependencies.register(
                DependencyEntry("t.app", "t.opt", "components", True, "t.opt >=0.1.0")
            ),
            "registres.dependencies",
            "dépendance tracée dans le manifest du composant consommateur",
        )

    def test_dependance_obligatoire_presentee_comme_optionnelle_refusee(
        self,
    ) -> None:
        before = self.registries.dependencies.entries
        self.assert_refus(
            self.registries.dependencies.register(
                DependencyEntry(
                    "t.app", "t.lib", "components", False, "t.lib >=1.0.0"
                )
            ),
            "registres.dependencies",
            "dépendance tracée dans le manifest du composant consommateur",
        )
        self.assertEqual(self.registries.dependencies.entries, before)

    def test_dependance_meme_cible_contrainte_falsifiee_refusee(self) -> None:
        before = self.registries.dependencies.entries
        self.assert_refus(
            self.registries.dependencies.register(
                DependencyEntry(
                    "t.app", "t.lib", "components", True, "t.lib >=9.9.9"
                )
            ),
            "registres.dependencies",
            "dépendance tracée dans le manifest du composant consommateur",
        )
        self.assertEqual(self.registries.dependencies.entries, before)

    def test_dependance_contrat_falsifie_refusee_registre_inchange(self) -> None:
        before = self.registries.dependencies.entries
        self.assert_refus(
            self.registries.dependencies.register(
                DependencyEntry(
                    "t.app",
                    "t.svc.contract",
                    "contracts",
                    True,
                    "t.svc.contract ==9.9.9",
                )
            ),
            "registres.dependencies",
            "dépendance tracée dans le manifest du composant consommateur",
        )
        self.assertEqual(self.registries.dependencies.entries, before)

    def test_dependance_contrat_exacte_tracee(self) -> None:
        refusals = self.registries.dependencies.register(
            DependencyEntry(
                "t.app",
                "t.svc.contract",
                "contracts",
                True,
                "t.svc.contract ==1.0.0",
            )
        )
        self.assertEqual(refusals, ())
        refusals = self.registries.dependencies.register(
            DependencyEntry(
                "t.app", "t.opt.contract", "contracts", False, "t.opt.contract"
            )
        )
        self.assertEqual(refusals, ())


class TestIdempotenceEtCollision(_BaseRegistres):
    def test_double_enregistrement_identique_idempotent(self) -> None:
        before = self.registries.services.entries
        refusals = self.registries.services.register(
            ServiceEntry("t.lib", "audit", "provides")
        )
        self.assertEqual(refusals, ())
        self.assertEqual(self.registries.services.entries, before)
        self.assertEqual(
            sum(
                1
                for entry in self.registries.services.entries
                if (entry.owner_id, entry.entry_id) == ("t.lib", "audit")
            ),
            1,
        )

    def test_collision_divergente_refusee_sans_effet(self) -> None:
        registry = Registry("services", ["t.lib"])
        self.assertEqual(
            registry.register(ServiceEntry("t.lib", "audit", "provides")), ()
        )
        before = registry.entries
        refusal = self.assert_refus(
            registry.register(ServiceEntry("t.lib", "audit", "implements")),
            "registres.services",
            "contenu identique pour une même clé de contribution",
        )
        self.assertIn("'t.lib'", str(refusal))
        self.assertEqual(registry.entries, before)

    def test_rejeu_complet_des_derivations_sans_changement(self) -> None:
        for entry in self.registries.modules.entries:
            self.assertEqual(self.registries.modules.register(entry), ())
        for entry in self.registries.dependencies.entries:
            self.assertEqual(self.registries.dependencies.register(entry), ())
        for entry in self.registries.lifecycle.entries:
            self.assertEqual(self.registries.lifecycle.register(entry), ())
        for entry in self.registries.extensions.entries:
            self.assertEqual(self.registries.extensions.register(entry), ())


class TestDeterminismeEtConstruction(_BaseRegistres):
    def test_build_independant_de_l_ordre_d_entree(self) -> None:
        forward = build_registries(list(MANIFESTS))
        backward = build_registries(list(reversed(MANIFESTS)))
        for name in (
            "modules",
            "dependencies",
            "lifecycle",
            "services",
            "events",
            "configuration",
            "extensions",
        ):
            self.assertEqual(
                getattr(forward, name).entries,
                getattr(backward, name).entries,
                f"ordre non déterministe pour le registre {name}",
            )

    def test_entries_triees_par_cle_canonique(self) -> None:
        keys = [
            (entry.owner_id, entry.entry_id)
            for entry in self.registries.dependencies.entries
        ]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(
            keys,
            [
                ("t.app", "audit"),
                ("t.app", "notify"),
                ("t.app", "t.lib"),
                ("t.app", "t.opt"),
                ("t.app", "t.opt.contract"),
                ("t.app", "t.svc.contract"),
            ],
        )

    def test_build_refuse_un_objet_non_manifest(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "n'accepte que des ComponentManifest validés"
        ):
            build_registries([{"id": "t.a"}])

    def test_build_refuse_un_conflit_de_declaration(self) -> None:
        conflit = _manifest(
            "t.dup",
            provides=(_capability("x"),),
            implements=(_contract("x"),),
        )
        with self.assertRaisesRegex(ValueError, "conflit de déclaration"):
            build_registries([conflit])
        with self.assertRaisesRegex(ValueError, "conflit de déclaration"):
            build_registries(
                [
                    _manifest(
                        "t.a", version="1.0.0", provides=(_capability("s"),)
                    ),
                    _manifest(
                        "t.a", version="2.0.0", provides=(_capability("s"),)
                    ),
                ]
            )

    def test_registres_fermes_refusent_toute_contribution(self) -> None:
        for registry in (self.registries.events, self.registries.configuration):
            refusals = registry.register(ServiceEntry("t.lib", "audit", "provides"))
            self.assert_refus(
                refusals,
                f"registres.{registry.category}",
                "source déclarative validée",
            )
            self.assertEqual(registry.entries, ())


class TestDerivationDepuisManifestes(_BaseRegistres):
    def test_modules_derivés_exactement(self) -> None:
        self.assertEqual(
            self.registries.modules.entries,
            (
                ModuleEntry("t.app", "t.app", "MODULE", "1.0.0"),
                ModuleEntry("t.ext", "t.ext", "EXTENSION", "1.0.0"),
                ModuleEntry("t.lib", "t.lib", "MODULE", "1.0.0"),
            ),
        )

    def test_dependances_obligatoires_et_optionnelles_distinctes(self) -> None:
        self.assertEqual(
            self.registries.dependencies.entries,
            (
                DependencyEntry("t.app", "audit", "capabilities", True, "audit"),
                DependencyEntry("t.app", "notify", "capabilities", False, "notify"),
                DependencyEntry(
                    "t.app", "t.lib", "components", True, "t.lib >=1.0.0"
                ),
                DependencyEntry(
                    "t.app", "t.opt", "components", False, "t.opt >=0.1.0"
                ),
                DependencyEntry(
                    "t.app",
                    "t.opt.contract",
                    "contracts",
                    False,
                    "t.opt.contract",
                ),
                DependencyEntry(
                    "t.app",
                    "t.svc.contract",
                    "contracts",
                    True,
                    "t.svc.contract ==1.0.0",
                ),
            ),
        )

    def test_services_declares_par_source(self) -> None:
        self.assertEqual(
            self.registries.services.entries,
            (
                ServiceEntry("t.app", "app.feature", "provides"),
                ServiceEntry("t.app", "t.app.contract", "implements"),
                ServiceEntry("t.ext", "audit", "implements"),
                ServiceEntry("t.lib", "audit", "provides"),
                ServiceEntry("t.lib", "metrics", "provides"),
                ServiceEntry("t.lib", "t.lib.contract", "implements"),
            ),
        )

    def test_lifecycle_et_extensions_auto_declares(self) -> None:
        self.assertEqual(
            self.registries.lifecycle.entries,
            (
                LifecycleEntry("t.app", "t.app"),
                LifecycleEntry("t.ext", "t.ext"),
                LifecycleEntry("t.lib", "t.lib"),
            ),
        )
        self.assertEqual(
            self.registries.extensions.entries,
            (ExtensionEntry("t.ext", "t.ext", "1.0.0"),),
        )


if __name__ == "__main__":
    unittest.main()
