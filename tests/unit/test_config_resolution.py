"""Tests unitaires de la résolution de configuration (tâche 4.2, acte 2).

Contrôles : priorité déclarée schéma→défaut→statique→runtime→référence de
secret avec valeur gagnante reproductible, refus fermé de type, de clé
requise, de valeurs admises et de clés sans déclaration, opacité des
références de secrets (aucune valeur résolue par le noyau), et absence de
toute valeur de test dans les diagnostics (face publique, tâches 2.3 et 6.3).
"""

import unittest

import pixs.kernel.config as config
from pixs.kernel.config import models as config_models
from pixs.kernel.config import resolution as config_resolution
from pixs.kernel.config.models import ConfigDeclaration, validate_config_declarations
from pixs.kernel.config.resolution import (
    ConfigurationResolution,
    ResolvedValue,
    SecretReference,
    qualified_key,
    resolve_configuration,
)
from pixs.kernel.diagnostics import Diagnostic

OWNER = "pixs.app"


def declaration(entry_id: str, value_type: str = "STRING", **kwargs) -> ConfigDeclaration:
    """Fabrique une ConfigDeclaration portée par le composant de référence."""
    return ConfigDeclaration(
        owner_id=OWNER, entry_id=entry_id, value_type=value_type, **kwargs
    )


def key(entry_id: str) -> str:
    """Retourne la clé qualifiée d'une déclaration du composant de référence."""
    return f"{OWNER}.{entry_id}"


class TestPriorite(unittest.TestCase):
    def test_valeur_gagnante_reproductible_travers_toutes_les_couches(
        self,
    ) -> None:
        expected = ResolvedValue(OWNER, "mode", "runtime", "runtime")
        resultats = [
            resolve_configuration(
                [declaration("mode")],
                schema_values={key("mode"): "schema"},
                static={key("mode"): "statique"},
                runtime={key("mode"): "runtime"},
            )
            for _ in range(2)
        ]
        for resultat in resultats:
            self.assertEqual(resultat.diagnostics, ())
            self.assertTrue(resultat.complete)
            self.assertEqual(resultat.resolved, (expected,))
        self.assertEqual(resultats[0], resultats[1])

    def test_statique_l_emporte_sur_schema_et_defaut(self) -> None:
        resultat = resolve_configuration(
            [declaration("port", "INTEGER", default=100)],
            schema_values={key("port"): 9000},
            static={key("port"): 8000},
        )
        self.assertEqual(
            resultat.resolved, (ResolvedValue(OWNER, "port", "static", 8000),)
        )

    def test_schema_puis_defaut_quand_rien_ne_surcharge(self) -> None:
        resultat = resolve_configuration(
            [declaration("port", "INTEGER", default=100)],
            schema_values={key("port"): 9000},
        )
        self.assertEqual(
            resultat.resolved, (ResolvedValue(OWNER, "port", "schema", 9000),)
        )
        resultat = resolve_configuration(
            [declaration("port", "INTEGER", default=100)]
        )
        self.assertEqual(
            resultat.resolved, (ResolvedValue(OWNER, "port", "default", 100),)
        )

    def test_vue_triée_indépendante_de_l_ordre_d_enveloppe(self) -> None:
        resultat = resolve_configuration(
            [declaration("b"), declaration("a")],
            static={key("b"): "y", key("a"): "x"},
        )
        self.assertEqual(
            [(item.entry_id, item.value) for item in resultat.resolved],
            [("a", "x"), ("b", "y")],
        )


class TestRefusFermé(unittest.TestCase):
    def _message_unique(self, resultat: ConfigurationResolution) -> str:
        self.assertEqual(len(resultat.diagnostics), 1)
        diagnostic = resultat.diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, "resolve")
        return str(diagnostic)

    def test_valeur_non_conforme_au_type_refusée(self) -> None:
        resultat = resolve_configuration(
            [declaration("port", "INTEGER")],
            runtime={key("port"): "pas-un-entier"},
        )
        self.assertEqual(resultat.resolved, ())
        self.assertIn("type déclaré", self._message_unique(resultat))

    def test_booléen_refusé_pour_un_type_integer(self) -> None:
        resultat = resolve_configuration(
            [declaration("port", "INTEGER")], runtime={key("port"): True}
        )
        self.assertEqual(resultat.resolved, ())
        self.assertIn("type déclaré", self._message_unique(resultat))

    def test_clé_requise_sans_valeur_refusée(self) -> None:
        resultat = resolve_configuration(
            [declaration("nom", required=True)], static={}
        )
        self.assertEqual(resultat.resolved, ())
        self.assertIn("sans valeur", self._message_unique(resultat))

    def test_valeur_hors_admises_refusée(self) -> None:
        resultat = resolve_configuration(
            [declaration("mode", allowed=("normal",))],
            runtime={key("mode"): "sombre"},
        )
        self.assertEqual(resultat.resolved, ())
        self.assertIn("valeurs admises", self._message_unique(resultat))

    def test_clé_sans_déclaration_refusée_par_clé_supplémentaire(self) -> None:
        resultat = resolve_configuration(
            [declaration("a")], static={key("a"): "x", "inconnue": "y"}
        )
        self.assertEqual(
            [(item.entry_id, item.value) for item in resultat.resolved],
            [("a", "x")],
        )
        self.assertEqual(len(resultat.diagnostics), 1)
        self.assertIn("aucune déclaration", str(resultat.diagnostics[0]))

    def test_clés_supplémentaires_refusées_sans_déclaration(self) -> None:
        resultat = resolve_configuration([], static={"x": "y"})
        self.assertEqual(resultat.resolved, ())
        self.assertEqual(len(resultat.diagnostics), 1)
        self.assertIn("aucune déclaration", str(resultat.diagnostics[0]))

    def test_déclarations_invalides_refusent_la_résolution_en_bloc(self) -> None:
        resultat = resolve_configuration([{"entry_id": "brut"}])
        self.assertEqual(resultat.resolved, ())
        self.assertEqual(len(resultat.diagnostics), 1)
        self.assertEqual(resultat.diagnostics[0].step, "validate")

    def test_arguments_non_mapping_refusés(self) -> None:
        with self.assertRaises(ValueError):
            resolve_configuration([declaration("mode")], static=["pas-un-mapping"])


class TestSecretsOpares(unittest.TestCase):
    def test_seule_une_référence_est_portée_jamais_une_valeur(self) -> None:
        resultat = resolve_configuration(
            [declaration("secret", is_secret=True, required=True)],
            secret_references={key("secret"): "vault://chemin"},
        )
        self.assertEqual(resultat.diagnostics, ())
        self.assertTrue(resultat.complete)
        (item,) = resultat.resolved
        self.assertIsInstance(item.value, SecretReference)

    def test_référence_requise_résolue_en_jeton_opaque(self) -> None:
        resultat = resolve_configuration(
            [declaration("secret", is_secret=True, required=True)],
            secret_references={key("secret"): "vault://chemin"},
        )
        (item,) = resultat.resolved
        self.assertEqual(item.source, "secret_reference")
        self.assertEqual(item.value.owner_id, OWNER)
        self.assertEqual(item.value.entry_id, "secret")
        self.assertEqual(item.value.source, "vault://chemin")

    def test_référence_invalide_refusée(self) -> None:
        resultat = resolve_configuration(
            [declaration("secret", is_secret=True)],
            secret_references={key("secret"): ""},
        )
        self.assertEqual(resultat.resolved, ())
        self.assertIn("référence invalide", str(resultat.diagnostics[0]))

    def test_clé_secrète_requise_sans_référence_refusée(self) -> None:
        resultat = resolve_configuration(
            [declaration("secret", is_secret=True, required=True)]
        )
        self.assertEqual(resultat.resolved, ())
        self.assertIn("sans référence", str(resultat.diagnostics[0]))

    def test_littéraux_sur_clé_secrète_refusés_en_agrégation(self) -> None:
        resultat = resolve_configuration(
            [declaration("secret", is_secret=True)],
            schema_values={key("secret"): "litteral"},
            static={key("secret"): "litteral"},
            runtime={key("secret"): "litteral"},
        )
        self.assertEqual(resultat.resolved, ())
        self.assertEqual(len(resultat.diagnostics), 3)
        for diagnostic in resultat.diagnostics:
            self.assertIn("source non admise", str(diagnostic))


class TestFacePublique(unittest.TestCase):
    def test_aucune_valeur_de_test_ne_figure_dans_les_diagnostics(self) -> None:
        decls = [
            declaration("token", "STRING", is_secret=True, required=True),
            declaration("port", "INTEGER"),
            declaration("mode", allowed=("normal",)),
            declaration("absente", required=True),
        ]
        resultats = [
            resolve_configuration(
                decls,
                static={key("port"): "neuf-mille"},
                runtime={key("mode"): "sombre"},
                secret_references={key("token"): "vault://sensible"},
            ),
            resolve_configuration(
                decls,
                schema_values={key("token"): "litteral-sensible"},
                static={key("mode"): "also-sensible", key("port"): 9000},
            ),
        ]
        for resultat in resultats:
            for value in (
                "neuf-mille",
                "sombre",
                "litteral-sensible",
                "also-sensible",
                "vault://sensible",
            ):
                for diagnostic in resultat.diagnostics:
                    self.assertNotIn(value, str(diagnostic))

    def test_qualified_key_et_valideur_de_référence(self) -> None:
        self.assertEqual(qualified_key(OWNER, "mode"), "pixs.app.mode")
        self.assertEqual(validate_config_declarations([declaration("mode")]), ())


class TestFacadePublique(unittest.TestCase):
    """Contrôle de la face publique bornée du sous-paquet config (tâche 4.2).

    Exercice exclusif de la façade ``pixs.kernel.config`` : ``__all__``
    exactement l'API déclarée, ``import *`` limité à cet ensemble, absence de
    fuite des sous-modules et implémentations privées, identité des réexports
    et résolution complète via la seule façade.
    """

    API_PUBLIQUE = (
        "CONFIG_SOURCES",
        "CONFIG_VALUE_TYPES",
        "ConfigDeclaration",
        "ConfigurationResolution",
        "ResolvedValue",
        "SecretReference",
        "qualified_key",
        "resolve_configuration",
        "validate_config_declarations",
    )

    def test_all_est_exactement_l_api_déclarée(self) -> None:
        self.assertEqual(tuple(config.__all__), self.API_PUBLIQUE)

    def test_import_star_ne_expose_que_l_api_déclarée(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pixs.kernel.config import *", namespace)
        exposes = {nom for nom in namespace if not nom.startswith("__")}
        self.assertEqual(exposes, set(self.API_PUBLIQUE))

    def test_import_star_ne_fuit_aucun_module_ni_membre_privé(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pixs.kernel.config import *", namespace)
        for fuite in (
            "models",
            "resolution",
            "_matches_type",
            "_check_mapping",
            "_SOURCE_LAYERS",
        ):
            self.assertNotIn(fuite, namespace)

    def test_réexports_identiques_aux_sous_modules(self) -> None:
        self.assertIs(config.ConfigDeclaration, config_models.ConfigDeclaration)
        self.assertIs(
            config.validate_config_declarations,
            config_models.validate_config_declarations,
        )
        self.assertIs(config.CONFIG_VALUE_TYPES, config_models.CONFIG_VALUE_TYPES)
        self.assertIs(config.CONFIG_SOURCES, config_resolution.CONFIG_SOURCES)
        self.assertIs(
            config.ConfigurationResolution,
            config_resolution.ConfigurationResolution,
        )
        self.assertIs(config.ResolvedValue, config_resolution.ResolvedValue)
        self.assertIs(config.SecretReference, config_resolution.SecretReference)
        self.assertIs(config.qualified_key, config_resolution.qualified_key)
        self.assertIs(
            config.resolve_configuration, config_resolution.resolve_configuration
        )

    def test_résolution_effectuée_depuis_la_seule_façade(self) -> None:
        déclaration_façade = config.ConfigDeclaration(
            owner_id=OWNER, entry_id="mode", value_type="STRING"
        )
        resultat = config.resolve_configuration(
            [déclaration_façade], static={key("mode"): "gagnée"}
        )
        self.assertIsInstance(resultat, config.ConfigurationResolution)
        self.assertEqual(
            resultat.resolved,
            (config.ResolvedValue(OWNER, "mode", "static", "gagnée"),),
        )


if __name__ == "__main__":
    unittest.main()
