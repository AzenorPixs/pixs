"""Unités pures des identités CA, métadonnées opaques synthétiques."""

from __future__ import annotations

import dataclasses
import datetime
import traceback
import unittest
import unittest.mock

from pixs.pzt_ca.ca_identity import (
    CaIdentityError,
    IntermediateGeneration,
    IntermediateIssuer,
    RootAuthority,
    generation_from_mapping,
    is_generation_transition_structurally_valid,
    is_root_transition_structurally_valid,
    issuer_from_mapping,
    loads_strict_mapping,
    root_from_mapping,
)

UTC = datetime.timezone.utc


def _root_kwargs(**changes: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object_type": "z12.root_authority/v1",
        "schema_version": "1.0.0",
        "domain": "synthetic:domain",
        "root_ref": "synthetic:root",
        "root_key_ref": "synthetic:root-key",
        "root_cert_ref": "synthetic:root-cert",
        "root_generation_id": "synthetic:root-generation",
        "key_created_at": datetime.datetime(2026, 10, 23, tzinfo=UTC),
        "root_key_material_ref": "synthetic:root-material",
        "status": "prepared",
    }
    base.update(changes)
    return base


def _issuer_kwargs(**changes: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object_type": "z12.intermediate_issuer/v1",
        "schema_version": "1.0.0",
        "domain": "synthetic:domain",
        "logical_authority": "synthetic:authority",
        "emission_scope": "synthetic:scope",
        "issuer_id": "synthetic:issuer",
        "issuer_role": "principal",
        "key_ref": "synthetic:key",
        "generation_id": "synthetic:generation",
    }
    base.update(changes)
    return base


def _generation_kwargs(**changes: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object_type": "z12.ca_generation/v1",
        "schema_version": "1.0.0",
        "generation_id": "synthetic:generation",
        "issuer_id": "synthetic:issuer",
        "key_ref": "synthetic:key",
        "key_created_at": datetime.datetime(2026, 10, 23, tzinfo=UTC),
        "key_material_ref": "synthetic:material",
        "status": "prepared",
        "created_epoch": 0,
    }
    base.update(changes)
    return base


class EvilEqual:
    def __eq__(self, other: object) -> bool:
        raise AssertionError("comparaison interdite")


class PositiveMappingTests(unittest.TestCase):
    def test_root_json_et_mapping(self) -> None:
        mapping = loads_strict_mapping(
            '{"object_type": "z12.root_authority/v1", "schema_version": "1.0.0",'
            ' "domain": "synthetic:domain", "root_ref": "synthetic:root",'
            ' "root_key_ref": "synthetic:key", "root_cert_ref": "synthetic:cert",'
            ' "root_generation_id": "synthetic:generation",'
            ' "key_created_at": "2026-10-23T00:00:00Z",'
            ' "root_key_material_ref": "synthetic:material",'
            ' "status": "prepared"}'
        )
        objet = root_from_mapping(mapping)
        self.assertEqual(objet.status, "prepared")

    def test_issuer_json_minuscules_et_offset(self) -> None:
        mapping = {
            "object_type": "z12.intermediate_issuer/v1",
            "schema_version": "1.0.0",
            "domain": "synthetic:domain",
            "logical_authority": "synthetic:authority",
            "emission_scope": "synthetic:scope",
            "issuer_id": "synthetic:issuer",
            "issuer_role": "standby",
            "key_ref": "synthetic:key",
            "generation_id": "synthetic:generation",
        }
        self.assertEqual(issuer_from_mapping(mapping).issuer_role, "standby")

    def test_generation_sans_predecesseur_puis_avec(self) -> None:
        sans = generation_from_mapping({
            "object_type": "z12.ca_generation/v1",
            "schema_version": "1.0.0",
            "generation_id": "synthetic:generation",
            "issuer_id": "synthetic:issuer",
            "key_ref": "synthetic:key",
            "key_created_at": "2026-10-23T00:00:00+00:00",
            "key_material_ref": "synthetic:material",
            "status": "reserved",
            "created_epoch": 3,
        })
        self.assertIsNone(sans.predecessor_generation_id)
        avec = generation_from_mapping({
            "object_type": "z12.ca_generation/v1",
            "schema_version": "1.0.0",
            "generation_id": "synthetic:generation",
            "issuer_id": "synthetic:issuer",
            "key_ref": "synthetic:key",
            "key_created_at": "2026-10-23t00:00:00z",
            "key_material_ref": "synthetic:material",
            "status": "active",
            "created_epoch": 4,
            "predecessor_generation_id": "synthetic:precedent",
        })
        self.assertEqual(avec.predecessor_generation_id, "synthetic:precedent")


class RefusChampsTests(unittest.TestCase):
    def test_manquants_surplus_version_discriminateur_roles_etats(self) -> None:
        valide = _issuer_kwargs()
        for cle in ("domain", "issuer_role"):
            limitee = dict(valide)
            del limitee[cle]
            with self.assertRaises(CaIdentityError):
                issuer_from_mapping(limitee)
        surplus = dict(valide)
        surplus["champ_inconnu"] = "x"
        with self.assertRaises(CaIdentityError):
            issuer_from_mapping(surplus)
        with self.assertRaises(CaIdentityError):
            issuer_from_mapping(_issuer_kwargs(schema_version="2.0.0"))
        with self.assertRaises(CaIdentityError):
            issuer_from_mapping(_issuer_kwargs(object_type="z12.autre/v1"))
        with self.assertRaises(CaIdentityError):
            issuer_from_mapping(_issuer_kwargs(issuer_role="racine"))
        with self.assertRaises(CaIdentityError):
            RootAuthority(**_root_kwargs(status="reserved"))
        with self.assertRaises(CaIdentityError):
            IntermediateGeneration(**_generation_kwargs(status="archived"))

    def test_epoch_negatif_bool_float_chaine(self) -> None:
        for valeur in (-1, True, 1.0, "0"):
            with self.assertRaises(CaIdentityError):
                IntermediateGeneration(**_generation_kwargs(created_epoch=valeur))

    def test_predecesseur_null_invalide(self) -> None:
        with self.assertRaises(CaIdentityError):
            generation_from_mapping({
                "object_type": "z12.ca_generation/v1",
                "schema_version": "1.0.0",
                "generation_id": "synthetic:generation",
                "issuer_id": "synthetic:issuer",
                "key_ref": "synthetic:key",
                "key_created_at": "2026-10-23T00:00:00Z",
                "key_material_ref": "synthetic:material",
                "status": "prepared",
                "created_epoch": 0,
                "predecessor_generation_id": None,
            })


class RefusHorodatagesTests(unittest.TestCase):
    def test_valides_z_et_offset(self) -> None:
        root_from_mapping({
            "object_type": "z12.root_authority/v1",
            "schema_version": "1.0.0",
            "domain": "synthetic:domain",
            "root_ref": "synthetic:root",
            "root_key_ref": "synthetic:key",
            "root_cert_ref": "synthetic:cert",
            "root_generation_id": "synthetic:generation",
            "key_created_at": "2026-10-23T00:00:00Z",
            "root_key_material_ref": "synthetic:material",
            "status": "prepared",
        })
        root_from_mapping({
            "object_type": "z12.root_authority/v1",
            "schema_version": "1.0.0",
            "domain": "synthetic:domain",
            "root_ref": "synthetic:root",
            "root_key_ref": "synthetic:key",
            "root_cert_ref": "synthetic:cert",
            "root_generation_id": "synthetic:generation",
            "key_created_at": "2026-10-23t00:00:00z",
            "root_key_material_ref": "synthetic:material",
            "status": "prepared",
        })
        root_from_mapping({
            "object_type": "z12.root_authority/v1",
            "schema_version": "1.0.0",
            "domain": "synthetic:domain",
            "root_ref": "synthetic:root",
            "root_key_ref": "synthetic:key",
            "root_cert_ref": "synthetic:cert",
            "root_generation_id": "synthetic:generation",
            "key_created_at": "2026-10-23T00:00:00+00:00",
            "root_key_material_ref": "synthetic:material",
            "status": "prepared",
        })

    def test_invalides(self) -> None:
        def fabrique(horodatage: str) -> dict[str, object]:
            return {
                "object_type": "z12.root_authority/v1",
                "schema_version": "1.0.0",
                "domain": "synthetic:domain",
                "root_ref": "synthetic:root",
                "root_key_ref": "synthetic:key",
                "root_cert_ref": "synthetic:cert",
                "root_generation_id": "synthetic:generation",
                "key_created_at": horodatage,
                "root_key_material_ref": "synthetic:material",
                "status": "prepared",
            }
        for horodatage in (
            "2026-10-23 00:00:00Z",
            "20261023T000000Z",
            "2026-W43-4T00:00:00Z",
            "2026-10-23TX00:00:00Z",
            "2026-10-23T00:00:00",
            "2026-10-23T00:00:00+01:00",
            "2026-10-23T00:00:00-00:00",
            "2026-10-23T00:00:00.1234567Z",
            "2026-10-23T00:00:00.123456789Z",
            "2026-10-23T24:00:00Z",
            "2026-02-30T00:00:00Z",
            "2026-10-23T00:00:00Z\n",
            "٢٠٢٦-١٠-٢٣T00:00:00Z",
        ):
            with self.assertRaises(CaIdentityError, msg=horodatage):
                root_from_mapping(fabrique(horodatage))


class JsonStrictTests(unittest.TestCase):
    def test_doublons_nan_infinity_non_objet(self) -> None:
        with self.assertRaises(CaIdentityError):
            loads_strict_mapping('{"a": "x", "a": "y"}')
        with self.assertRaises(CaIdentityError):
            loads_strict_mapping('{"a": {"b": "x", "b": "y"}}')
        for texte in ("NaN", "Infinity", "-Infinity", '["liste"]', '"chaine"'):
            with self.assertRaises(CaIdentityError):
                loads_strict_mapping(texte)


class EgaliteTrompeuseTests(unittest.TestCase):
    def test_faux_objet_eq_ni_appele_ni_accepte(self) -> None:
        with self.assertRaises(CaIdentityError):
            RootAuthority(**_root_kwargs(object_type=EvilEqual()))  # type: ignore[arg-type]
        with self.assertRaises(CaIdentityError):
            issuer_from_mapping({"a": EvilEqual()})  # type: ignore[dict-item]


class ImmuabiliteTests(unittest.TestCase):
    def test_fige_sans_repr_ni_fuite(self) -> None:
        sentinel = "SENTINELLE_NE_PAS_JOURNALISER"
        instance = IntermediateGeneration(**_generation_kwargs(generation_id=sentinel))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            instance.status = "active"  # type: ignore[misc]
        self.assertNotIn(sentinel, repr(instance))
        with self.assertRaises(CaIdentityError) as captured:
            IntermediateIssuer(**_issuer_kwargs(domain=[sentinel]))
        self.assertNotIn(sentinel, str(captured.exception))
        self.assertNotIn(sentinel, repr(captured.exception.args))
        self.assertEqual(captured.exception.element, "intermediate_issuer.domain")


class MatricesAttenduesTests(unittest.TestCase):
    def test_matrice_racine_3x3_du_contrat(self) -> None:
        attendus = {
            ("prepared", "prepared"): False,
            ("prepared", "active"): True,
            ("prepared", "retired"): True,
            ("active", "prepared"): False,
            ("active", "active"): False,
            ("active", "retired"): True,
            ("retired", "prepared"): False,
            ("retired", "active"): False,
            ("retired", "retired"): False,
        }
        for (avant, apres), attendu in attendus.items():
            self.assertEqual(
                is_root_transition_structurally_valid(avant, apres), attendu,
                f"{avant}->{apres}",
            )

    def test_matrice_generation_4x4_du_contrat(self) -> None:
        attendus = {
            ("prepared", "prepared"): False,
            ("prepared", "reserved"): True,
            ("prepared", "active"): False,
            ("prepared", "retired"): True,
            ("reserved", "prepared"): False,
            ("reserved", "reserved"): False,
            ("reserved", "active"): True,
            ("reserved", "retired"): True,
            ("active", "prepared"): False,
            ("active", "reserved"): False,
            ("active", "active"): False,
            ("active", "retired"): True,
            ("retired", "prepared"): False,
            ("retired", "reserved"): False,
            ("retired", "active"): False,
            ("retired", "retired"): False,
        }
        for (avant, apres), attendu in attendus.items():
            self.assertEqual(
                is_generation_transition_structurally_valid(avant, apres), attendu,
                f"{avant}->{apres}",
            )


class EntreesLimitesTests(unittest.TestCase):
    def test_reference_non_utf8_refusee(self) -> None:
        with self.assertRaises(CaIdentityError):
            IntermediateIssuer(**_issuer_kwargs(domain="\ud800"))

    def test_erreur_parseur_assainie_sans_fuite(self) -> None:
        with unittest.mock.patch(
            "pixs.pzt_ca.ca_identity.json.loads",
            side_effect=RecursionError("SENTINELLE_PARSEUR"),
        ) as mocked_loads:
            with self.assertRaises(CaIdentityError) as captured:
                loads_strict_mapping('{"synthetic": "opaque"}')
        mocked_loads.assert_called_once()
        self.assertEqual(captured.exception.code, "ENVELOPPE_JSON_INVALIDE")
        self.assertEqual(captured.exception.element, "mapping")
        self.assertNotIn("SENTINELLE_PARSEUR", str(captured.exception))
        self.assertNotIn("SENTINELLE_PARSEUR", repr(captured.exception.args))
        self.assertTrue(captured.exception.__suppress_context__)
        rendered = "".join(traceback.format_exception(captured.exception))
        self.assertNotIn("SENTINELLE_PARSEUR", rendered)

    def test_cle_etrangere_refusee_sans_comparaison(self) -> None:
        class ForeignKey:
            def __hash__(self) -> int:
                return hash("domain")

            def __eq__(self, other: object) -> bool:
                raise AssertionError("comparaison de clé interdite")

        with self.assertRaises(CaIdentityError):
            root_from_mapping({ForeignKey(): "synthetic:domain"})

    def test_fraction_exacte_sans_perte(self) -> None:
        mapping = _root_kwargs(key_created_at="2026-10-23T00:00:00.123456000Z")
        self.assertEqual(root_from_mapping(mapping).key_created_at.microsecond, 123456)


if __name__ == "__main__":
    unittest.main()
