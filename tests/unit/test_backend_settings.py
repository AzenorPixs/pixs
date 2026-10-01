"""Tests unitaires fondation backend préparatoire, synthétiques uniquement."""

import unittest

import pixs.backend as facade
from pixs.backend import checks as checks_module
from pixs.backend import settings as settings_module
from pixs.backend.checks import check_template, inspect_roles
from pixs.backend.settings import (
    POSTGRES_ENGINE,
    PROFILES,
    SettingsTemplate,
    build_settings_template,
)
from pixs.kernel.config.resolution import SecretReference


def _ref_cle():
    return SecretReference(
        owner_id="pixs.backend",
        entry_id="django_secret_key",
        source="vault://test/django-key",
    )


def _ref_mot_de_passe():
    return SecretReference(
        owner_id="pixs.backend",
        entry_id="db_password",
        source="vault://test/db-password",
    )


def _base():
    return {"name": "db-synthetique", "user": "u-synthetique",
            "host": "h-synthetique", "port": 5432}


def _hotes():
    return ["localhost"]


def _gabarit(profile="web"):
    return build_settings_template(
        profile=profile,
        database=dict(_base()),
        allowed_hosts=list(_hotes()),
        secret_key_ref=_ref_cle(),
        database_password_ref=_ref_mot_de_passe(),
    )


class TestProfils(unittest.TestCase):
    def test_trois_roles_explicites_tous_indisponibles(self):
        for profil in ("web", "worker", "scheduler"):
            with self.subTest(profil=profil):
                gabarit = _gabarit(profil)
                self.assertEqual(gabarit.profile, profil)
                roles = inspect_roles(gabarit)
                self.assertEqual(set(roles), {"web", "worker", "scheduler"})
                for nom, etat in roles.items():
                    self.assertEqual(etat["available"], False)
                    self.assertEqual(etat["selected"], nom == profil)

    def test_aucun_role_par_defaut(self):
        for mauvais in (None, "local", "unknown", "", "WEB", 123, b"web"):
            with self.subTest():
                with self.assertRaises(ValueError) as ctx:
                    build_settings_template(
                        profile=mauvais,
                        database=dict(_base()),
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )
                self.assertNotIn("local", str(ctx.exception).lower()
                                 if isinstance(mauvais, str) else "")


class TestMoteurEtCles(unittest.TestCase):
    def test_moteur_pg_constant(self):
        gabarit = _gabarit()
        self.assertEqual(gabarit.engine, POSTGRES_ENGINE)
        self.assertEqual(POSTGRES_ENGINE, "django.db.backends.postgresql")

    def test_database_refuse_cles_inattendues(self):
        extras = [
            {"name": "a", "user": "b", "host": "c", "port": 1, "ENGINE": "x"},
            {"name": "a", "user": "b", "host": "c", "port": 1, "engine": "x"},
            {"name": "a", "user": "b", "host": "c", "port": 1, "password": "x"},
            {"name": "a", "user": "b", "host": "c", "port": 1, "PASSWORD": "x"},
            {"name": "a", "user": "b", "host": "c"},
            {"name": "a", "user": "b"},
            {"name": "a"},
            {},
            {"user": "b", "host": "c", "port": 1},
        ]
        for base in extras:
            with self.subTest():
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=dict(base),
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )

    def test_database_non_mapping_refuse(self):
        for mauvais in (None, "x", [("name", "a")], 123):
            with self.subTest():
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=mauvais,
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )


class TestChampsNonSecrets(unittest.TestCase):
    def test_nom_user_host_types_blanks(self):
        for champ in ("name", "user", "host"):
            for mauvais in (None, 123, "", "   ", b"x"):
                with self.subTest():
                    base = dict(_base())
                    base[champ] = mauvais
                    with self.assertRaises(ValueError) as ctx:
                        build_settings_template(
                            profile="web", database=base,
                            allowed_hosts=list(_hotes()),
                            secret_key_ref=_ref_cle(),
                            database_password_ref=_ref_mot_de_passe(),
                        )
                    if isinstance(mauvais, str) and mauvais.strip():
                        self.assertNotIn(mauvais, str(ctx.exception))

    def test_port_invalides(self):
        for mauvais in (True, False, "5432", None, 0, -1, 65536, 99999, 3.5):
            with self.subTest():
                base = dict(_base())
                base["port"] = mauvais
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=base,
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )


class TestAllowedHosts(unittest.TestCase):
    def test_formes_invalides(self):
        invalides = [
            "localhost",
            b"localhost",
            bytearray(b"localhost"),
            [],
            (),
            [""],
            ["   "],
            ["*"],
            ["a*b"],
            [".example"],
            [" localhost"],
            ["localhost "],
            [" .example"],
            ["localhost", ""],
            "x",
        ]
        for mauvais in invalides:
            with self.subTest():
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=dict(_base()),
                        allowed_hosts=mauvais,
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )

    def test_non_sequence_refusee(self):
        for mauvais in (None, 123, {"a"}, {"h": "localhost"}):
            with self.subTest():
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=dict(_base()),
                        allowed_hosts=mauvais,
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )


class TestReferences(unittest.TestCase):
    def test_refs_distinctes_requises(self):
        with self.assertRaises(ValueError):
            build_settings_template(
                profile="web", database=dict(_base()),
                allowed_hosts=list(_hotes()),
                secret_key_ref=_ref_cle(),
                database_password_ref=_ref_cle(),
            )

    def test_mauvais_types_refuses(self):
        for mauvais in (None, "vault://x", 123, {"source": "x"}):
            with self.subTest():
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=dict(_base()),
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=mauvais,
                        database_password_ref=_ref_mot_de_passe(),
                    )
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=dict(_base()),
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=_ref_cle(),
                        database_password_ref=mauvais,
                    )

    def test_champs_blanks_refuses(self):
        for kwargs in (
            {"owner_id": "   ", "entry_id": "e", "source": "s"},
            {"owner_id": "o", "entry_id": "  ", "source": "s"},
            {"owner_id": "o", "entry_id": "e", "source": "   "},
            {"owner_id": "", "entry_id": "e", "source": "s"},
        ):
            with self.subTest():
                ref = SecretReference(**kwargs)
                with self.assertRaises(ValueError):
                    build_settings_template(
                        profile="web", database=dict(_base()),
                        allowed_hosts=list(_hotes()),
                        secret_key_ref=ref,
                        database_password_ref=_ref_mot_de_passe(),
                    )

    def test_pas_de_resolution(self):
        gabarit = _gabarit()
        self.assertIsInstance(gabarit.secret_key_ref, SecretReference)
        self.assertIsInstance(gabarit.database_password_ref, SecretReference)
        self.assertNotEqual(
            gabarit.secret_key_ref, gabarit.database_password_ref
        )


class TestConstructeurDirect(unittest.TestCase):
    def test_direct_valide_et_ready_engine_non_parametrables(self):
        gabarit = SettingsTemplate(
            profile="worker",
            name="n", user="u", host="h", port=5433,
            allowed_hosts=("localhost",),
            secret_key_ref=_ref_cle(),
            database_password_ref=_ref_mot_de_passe(),
        )
        self.assertEqual(gabarit.ready, False)
        self.assertEqual(gabarit.engine, POSTGRES_ENGINE)
        with self.assertRaises(TypeError):
            SettingsTemplate(
                profile="worker", name="n", user="u", host="h", port=5433,
                allowed_hosts=("localhost",),
                secret_key_ref=_ref_cle(),
                database_password_ref=_ref_mot_de_passe(),
                ready=True,
            )
        with self.assertRaises(TypeError):
            SettingsTemplate(
                profile="worker", name="n", user="u", host="h", port=5433,
                allowed_hosts=("localhost",),
                secret_key_ref=_ref_cle(),
                database_password_ref=_ref_mot_de_passe(),
                engine="sqlite",
            )

    def test_direct_invalide_tables(self):
        base = {
            "profile": "web", "name": "n", "user": "u", "host": "h",
            "port": 5432, "allowed_hosts": ("localhost",),
        }
        cas = [
            ("profile", "local"),
            ("profile", "unknown"),
            ("port", True),
            ("port", 0),
            ("name", "   "),
            ("allowed_hosts", ("*",)),
            ("allowed_hosts", (".example",)),
        ]
        for champ, mauvais in cas:
            with self.subTest(champ=champ):
                kwargs = dict(base)
                kwargs[champ] = mauvais
                with self.assertRaises(ValueError):
                    SettingsTemplate(
                        profile=kwargs["profile"], name=kwargs["name"],
                        user=kwargs["user"], host=kwargs["host"],
                        port=kwargs["port"],
                        allowed_hosts=kwargs["allowed_hosts"],
                        secret_key_ref=_ref_cle(),
                        database_password_ref=_ref_mot_de_passe(),
                    )
        with self.subTest(champ="secret_key_ref"):
            with self.assertRaises(ValueError):
                SettingsTemplate(
                    profile="web", name="n", user="u", host="h", port=1,
                    allowed_hosts=("localhost",),
                    secret_key_ref="vault://sentinelle-xyz",
                    database_password_ref=_ref_mot_de_passe(),
                )
        with self.subTest(champ="refs-identiques"):
            ref = _ref_cle()
            with self.assertRaises(ValueError):
                SettingsTemplate(
                    profile="web", name="n", user="u", host="h", port=1,
                    allowed_hosts=("localhost",),
                    secret_key_ref=ref,
                    database_password_ref=ref,
                )

    def test_profile_absent_type_error(self):
        with self.assertRaises(TypeError):
            build_settings_template(
                database=dict(_base()),
                allowed_hosts=list(_hotes()),
                secret_key_ref=_ref_cle(),
                database_password_ref=_ref_mot_de_passe(),
            )


class TestImmuabilite(unittest.TestCase):
    def test_frozen(self):
        from dataclasses import FrozenInstanceError

        gabarit = _gabarit()
        with self.assertRaises(FrozenInstanceError):
            gabarit.profile = "worker"  # type: ignore[misc]

    def test_entrees_mutables_independantes(self):
        base = dict(_base())
        hotes = ["localhost"]
        gabarit = build_settings_template(
            profile="web", database=base, allowed_hosts=hotes,
            secret_key_ref=_ref_cle(),
            database_password_ref=_ref_mot_de_passe(),
        )
        base["name"] = "modifie"
        hotes.append("autre")
        self.assertNotEqual(gabarit.name, "modifie")
        self.assertEqual(gabarit.allowed_hosts, ("localhost",))

    def test_copie_fraiche_non_secret(self):
        gabarit = _gabarit()
        premier = gabarit.non_secret_settings
        self.assertNotIn("SECRET_KEY", premier)
        self.assertNotIn("PASSWORD", str(premier))
        self.assertEqual(premier["ENGINE"], POSTGRES_ENGINE)
        self.assertEqual(premier["DEBUG"], False)
        self.assertEqual(premier["USE_TZ"], True)
        self.assertEqual(premier["TIME_ZONE"], "UTC")
        self.assertEqual(premier["INSTALLED_APPS"], ())
        premier["ALLOWED_HOSTS"] = ("modifie",)
        premier["DATABASES"]["default"]["NAME"] = "modifie"
        second = gabarit.non_secret_settings
        self.assertEqual(second["ALLOWED_HOSTS"], ("localhost",))
        self.assertNotEqual(second["DATABASES"]["default"]["NAME"], "modifie")


class TestDiagnosticsSansValeurs(unittest.TestCase):
    def test_sentinelles_absentes_valide_et_refus(self):
        sentinelles = (
            "n-sentinelle-xyz", "u-sentinelle-xyz", "h-sentinelle-xyz",
            "hote-sentinelle-xyz", "vault://sentinelle-cle-xyz",
            "vault://sentinelle-mdp-xyz", "pw-sentinelle-xyz",
            "inconnu-sentinelle-xyz",
        )
        ref_cle = SecretReference(
            owner_id="pixs.backend", entry_id="cle-sentinelle-xyz",
            source="vault://sentinelle-cle-xyz",
        )
        ref_mdp = SecretReference(
            owner_id="pixs.backend", entry_id="mdp-sentinelle-xyz",
            source="vault://sentinelle-mdp-xyz",
        )
        gabarit = build_settings_template(
            profile="web",
            database={"name": "n-sentinelle-xyz",
                      "user": "u-sentinelle-xyz",
                      "host": "h-sentinelle-xyz", "port": 5432},
            allowed_hosts=["hote-sentinelle-xyz"],
            secret_key_ref=ref_cle,
            database_password_ref=ref_mdp,
        )
        for resultat in (check_template(gabarit), inspect_roles(gabarit)):
            texte = str(resultat)
            for sentinelle in sentinelles:
                self.assertNotIn(sentinelle, texte)
        with self.assertRaises(ValueError) as ctx1:
            build_settings_template(
                profile="inconnu-sentinelle-xyz",
                database={"name": "n-sentinelle-xyz",
                          "user": "u-sentinelle-xyz",
                          "host": "h-sentinelle-xyz", "port": 5432},
                allowed_hosts=["hote-sentinelle-xyz"],
                secret_key_ref=ref_cle,
                database_password_ref=ref_mdp,
            )
        self.assertNotIn("sentinelle", str(ctx1.exception))
        with self.assertRaises(ValueError) as ctx2:
            build_settings_template(
                profile="web",
                database={"name": "n-sentinelle-xyz",
                          "user": "u-sentinelle-xyz",
                          "host": "h-sentinelle-xyz", "port": 5432,
                          "password": "pw-sentinelle-xyz"},
                allowed_hosts=["hote-sentinelle-xyz"],
                secret_key_ref=ref_cle,
                database_password_ref=ref_mdp,
            )
        self.assertNotIn("sentinelle", str(ctx2.exception))


class TestChecksRefus(unittest.TestCase):
    def test_types_invalides_generiques(self):
        for mauvais in (None, "x", 123, object()):
            with self.subTest():
                with self.assertRaises(ValueError) as ctx1:
                    check_template(mauvais)
                self.assertEqual(str(ctx1.exception), "gabarit invalide")
                with self.assertRaises(ValueError) as ctx2:
                    inspect_roles(mauvais)
                self.assertEqual(str(ctx2.exception), "gabarit invalide")

    def test_check_sans_valeurs(self):
        resultat = check_template(_gabarit("scheduler"))
        self.assertEqual(resultat["template_valid"], True)
        self.assertEqual(resultat["ready"], False)
        self.assertEqual(resultat["engine"], POSTGRES_ENGINE)
        self.assertEqual(resultat["selected_profile"], "scheduler")
        self.assertEqual(resultat["secrets_resolved"], False)
        self.assertEqual(resultat["persistence_available"], False)
        self.assertEqual(resultat["services_available"], False)
        self.assertTrue(isinstance(resultat["limitations"], tuple))
        self.assertNotIn("u-synthetique", str(resultat))

    def test_mutation_resultat_isolee(self):
        gabarit = _gabarit()
        premier = check_template(gabarit)
        premier["limitations"] = ()
        premier["selected_profile"] = "modifie"
        second = check_template(gabarit)
        self.assertNotEqual(second["selected_profile"], "modifie")
        self.assertNotEqual(second["limitations"], ())
        roles_premier = inspect_roles(gabarit)
        roles_premier["web"] = {"selected": False, "available": True}
        roles_second = inspect_roles(gabarit)
        self.assertEqual(
            roles_second["web"], {"selected": True, "available": False}
        )


class TestFacade(unittest.TestCase):
    def test_all_exact_sans_conversion(self):
        self.assertEqual(tuple(facade.__all__), (
            "SettingsTemplate", "build_settings_template",
            "check_template", "inspect_roles",
        ))
        self.assertIs(facade.SettingsTemplate, settings_module.SettingsTemplate)
        self.assertIs(facade.build_settings_template,
                      settings_module.build_settings_template)
        self.assertIs(facade.check_template, checks_module.check_template)
        self.assertIs(facade.inspect_roles, checks_module.inspect_roles)
        self.assertFalse(hasattr(facade, "to_django_dict_for_test_only"))
        self.assertEqual(tuple(PROFILES), ("web", "worker", "scheduler"))


if __name__ == "__main__":
    unittest.main()
