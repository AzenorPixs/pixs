"""Tests unitaires de la projection publique d'erreur d'infrastructure."""

import unittest
import uuid

from pixs.backend.api import (
    API_ERROR_CONTRACT_VERSION,
    ApiContractPlan,
    ApiErrorProjectionError,
    api_major_prefix,
    build_infrastructure_error,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor

_VALID_UUID = uuid.UUID(int=(4 << 76) | (2 << 62) | 42)
_DIAGNOSTIC = "Identifiant de corrélation invalide."


def _forged_missing_int():
    return object.__new__(uuid.UUID)


def _forged_int(value):
    forged = object.__new__(uuid.UUID)
    object.__setattr__(forged, "int", value)
    return forged


class _IntSub(int):
    def __lt__(self, other):
        raise AssertionError("comparaison hostile interdite")

    def __le__(self, other):
        raise AssertionError("comparaison hostile interdite")

    def __ge__(self, other):
        raise AssertionError("comparaison hostile interdite")

    def __bool__(self):
        raise AssertionError("conversion hostile interdite")


class _SubUUID(uuid.UUID):
    def __getattribute__(self, name):
        raise AssertionError("getter hostile interdit")

    def __str__(self):
        raise AssertionError("str hostile interdit")

    def __repr__(self):
        raise AssertionError("repr hostile interdit")


class HostileOpaque:
    """Opaque dont toute inspection lève immédiatement."""

    def __getattribute__(self, name):
        raise AssertionError("getter opaque interdit")

    def __str__(self):
        raise AssertionError("inspection interdite")

    def __repr__(self):
        raise AssertionError("inspection interdite")

    def __bool__(self):
        raise AssertionError("inspection interdite")

    def __iter__(self):
        raise AssertionError("inspection interdite")


class ValidEnvelope(unittest.TestCase):
    def test_enveloppe_exacte_et_version_publique(self):
        envelope = build_infrastructure_error(
            _VALID_UUID, internal_error=RuntimeError("synthetic-boom")
        )
        self.assertEqual(
            set(envelope),
            {"error_code", "message", "details", "field_errors", "correlation_id"},
        )
        self.assertEqual(envelope["error_code"], "INTERNAL_ERROR")
        self.assertEqual(envelope["message"], "Erreur interne du service.")
        self.assertEqual(envelope["details"], {})
        self.assertEqual(envelope["field_errors"], [])
        self.assertEqual(envelope["correlation_id"], str(_VALID_UUID))
        self.assertEqual(API_ERROR_CONTRACT_VERSION, "1.0.0")

    def test_toutes_versions_variants_nil_max_acceptees(self):
        for version in range(16):
            for variant in range(4):
                candidate = uuid.UUID(int=(version << 76) | (variant << 62) | 7)
                envelope = build_infrastructure_error(candidate, internal_error=None)
                self.assertEqual(envelope["correlation_id"], str(candidate))
        for bound in (uuid.UUID(int=0), uuid.UUID(int=2**128 - 1)):
            envelope = build_infrastructure_error(bound, internal_error=None)
            self.assertEqual(envelope["correlation_id"], str(bound))

    def test_opaque_hostile_indifferent(self):
        opaques = (
            None,
            RuntimeError("synthetic-boom"),
            {"cle": "valeur"},
            "texte brut",
            HostileOpaque(),
        )
        first = None
        for opaque in opaques:
            envelope = build_infrastructure_error(_VALID_UUID, internal_error=opaque)
            self.assertEqual(envelope["correlation_id"], str(_VALID_UUID))
            if first is None:
                first = envelope
            else:
                self.assertEqual(envelope, first)


class Rejets(unittest.TestCase):
    def test_types_non_uuid_rejetes(self):
        for bad in (str(_VALID_UUID), None, 42, True, b"x", ["x"], _VALID_UUID.int, HostileOpaque()):
            with self.assertRaises(ApiErrorProjectionError):
                build_infrastructure_error(bad, internal_error=None)

    def test_sous_classe_uuid_rejetee(self):
        hostile = object.__new__(_SubUUID)
        object.__setattr__(hostile, "int", _VALID_UUID.int)
        with self.assertRaises(ApiErrorProjectionError):
            build_infrastructure_error(hostile, internal_error=None)

    def test_uuid_incomplet_rejete(self):
        with self.assertRaises(ApiErrorProjectionError):
            build_infrastructure_error(_forged_missing_int(), internal_error=None)

    def test_entiers_hostiles_rejetes(self):
        for bad_int in (True, "42", None, _IntSub(42), -1, 2**128):
            with self.assertRaises(ApiErrorProjectionError):
                build_infrastructure_error(_forged_int(bad_int), internal_error=None)


class DiagnosticsEtFraicheur(unittest.TestCase):
    def test_diagnostic_constant_sans_echo_cause_supprimee(self):
        with self.assertRaises(ApiErrorProjectionError) as ctx:
            build_infrastructure_error(
                "SENTINEL-BRUT-INTERDITE", internal_error=RuntimeError("boom")
            )
        exc = ctx.exception
        self.assertIsInstance(exc, ValueError)
        self.assertEqual(str(exc), _DIAGNOSTIC)
        self.assertIsNone(exc.__cause__)
        self.assertTrue(exc.__suppress_context__)
        self.assertNotIn("SENTINEL-BRUT", str(exc))

    def test_uuid_incomplet_diagnostic_sans_contexte(self):
        with self.assertRaises(ApiErrorProjectionError) as ctx:
            build_infrastructure_error(_forged_missing_int(), internal_error=None)
        self.assertEqual(str(ctx.exception), _DIAGNOSTIC)
        self.assertIsNone(ctx.exception.__cause__)
        self.assertTrue(ctx.exception.__suppress_context__)

    def test_conteneurs_frais_sans_contamination(self):
        first = build_infrastructure_error(_VALID_UUID, internal_error=None)
        second = build_infrastructure_error(_VALID_UUID, internal_error=None)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertIsNot(first["details"], second["details"])
        self.assertIsNot(first["field_errors"], second["field_errors"])
        first["details"]["cle"] = "valeur"
        first["field_errors"].append("erreur")
        third = build_infrastructure_error(_VALID_UUID, internal_error=None)
        self.assertEqual(third["details"], {})
        self.assertEqual(third["field_errors"], [])

    def test_signature_interne_opaque_obligatoire(self):
        with self.assertRaises(TypeError):
            build_infrastructure_error(_VALID_UUID)
        with self.assertRaises(TypeError):
            build_infrastructure_error(_VALID_UUID, RuntimeError("synthetic-boom"))


class FacadePreexistante(unittest.TestCase):
    def test_plans_api_toujours_accessibles(self):
        plan = ApiContractPlan(
            contract=ContractDescriptor(
                contract_id="pixs.contract.billing",
                category=ContractCategory.API,
                version="1.2.3",
                owner_component="pixs.backend",
                guarantees_doc="Garanties documentees.",
            ),
            openapi_document_ref="pixs.api.billing.v1",
        )
        self.assertEqual(api_major_prefix(plan), "/api/v1")


if __name__ == "__main__":
    unittest.main()
