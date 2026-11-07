"""Unités résultat, représentation seule, sans effet."""

from __future__ import annotations

import datetime
import unittest

from pixs.pzt_ca.ca_result import (
    CaResult,
    CaResultError,
    result_from_json,
    result_from_mapping,
)

_VALID_AT = "2026-10-23T09:00:00Z"
_SENTINEL = "SENTINELLE-SANS-FUITE-zzz-123"


class EvilEq:
    def __eq__(self, other: object) -> bool:
        raise AssertionError("EvilEq appele")


def _base_current_valid() -> dict:
    return {
        "object_type": "z12.ca_result/v1",
        "schema_version": "1.0.0",
        "result_id": "res-1",
        "operation_id": "op-1",
        "operation_version": "opv-1",
        "request_id": "req-1",
        "context_ref": "ctx-1",
        "result_kind": "current_operation",
        "recorded_at": _VALID_AT,
        "input_fingerprint": "fp-1",
        "validation_outcome": "valid",
        "engagement_outcome": "engaged",
        "engagement_ref": "eng-1",
        "effect_outcome": "applied",
        "effect_evidence_ref": "eff-1",
        "error_code": "ok",
    }


class ResultStructureTest(unittest.TestCase):
    def test_valide_courant_applique(self) -> None:
        dec = result_from_mapping(_base_current_valid())
        self.assertEqual(dec.effect_outcome, "applied")
        self.assertEqual(dec.error_code, "ok")

    def test_type_direct_refuse(self) -> None:
        with self.assertRaises(CaResultError):
            result_from_mapping("faux")  # type: ignore[arg-type]

    def test_etranger_refuse(self) -> None:
        bad = _base_current_valid()
        bad["object_type"] = "z12.ca_proof/v1"
        with self.assertRaises(CaResultError):
            result_from_mapping(bad)

    def test_null_refuse(self) -> None:
        bad = _base_current_valid()
        bad["engagement_ref"] = None
        with self.assertRaises(CaResultError):
            result_from_mapping(bad)

    def test_doublon_json_refuse(self) -> None:
        with self.assertRaises(CaResultError):
            result_from_json('{"a": 1, "a": 2}')

    def test_champ_inconnu_refuse(self) -> None:
        bad = _base_current_valid()
        bad["champ_extra"] = "x"
        with self.assertRaises(CaResultError):
            result_from_mapping(bad)

    def test_version_autre_refusee(self) -> None:
        bad = _base_current_valid()
        bad["schema_version"] = "2.0.0"
        with self.assertRaises(CaResultError):
            result_from_mapping(bad)

    def test_evil_eq_et_bool_refuse(self) -> None:
        bad = _base_current_valid()
        bad["result_id"] = EvilEq()  # type: ignore[dict-value]
        with self.assertRaises(CaResultError):
            result_from_mapping(bad)
        bad2 = _base_current_valid()
        bad2["input_fingerprint"] = 123  # type: ignore[dict-value]
        with self.assertRaises(CaResultError):
            result_from_mapping(bad2)

    def test_diagnostics_sans_entree(self) -> None:
        bad = _base_current_valid()
        bad["result_id"] = _SENTINEL
        bad["validation_outcome"] = "nope"
        try:
            result_from_mapping(bad)
        except CaResultError as exc:
            self.assertNotIn(_SENTINEL, str(exc))
        else:
            self.fail("refus attendu")

    def test_direct_utc_naif_refuse(self) -> None:
        base = _base_current_valid()
        dec = result_from_mapping(base)
        naive = datetime.datetime(2026, 10, 23, 9, 0, 0)
        with self.assertRaises(CaResultError):
            CaResult(
                object_type=dec.object_type,
                schema_version=dec.schema_version,
                result_id=dec.result_id,
                operation_id=dec.operation_id,
                operation_version=dec.operation_version,
                request_id=dec.request_id,
                context_ref=dec.context_ref,
                result_kind=dec.result_kind,
                recorded_at=naive,  # type: ignore[arg-type]
                input_fingerprint=dec.input_fingerprint,
                validation_outcome=dec.validation_outcome,
                engagement_outcome=dec.engagement_outcome,
                effect_outcome=dec.effect_outcome,
                engagement_ref=dec.engagement_ref,
                effect_evidence_ref=dec.effect_evidence_ref,
                error_code=dec.error_code,
            )


class ResultConditionsTest(unittest.TestCase):
    def test_engagement_requis_si_engaged(self) -> None:
        bad = _base_current_valid()
        del bad["engagement_ref"]
        with self.assertRaises(CaResultError) as releve:
            result_from_mapping(bad)
        self.assertEqual(releve.exception.code, "ENGAGEMENT_REQUIS")

    def test_preuve_effet_requise_si_applied(self) -> None:
        bad = _base_current_valid()
        del bad["effect_evidence_ref"]
        with self.assertRaises(CaResultError) as releve:
            result_from_mapping(bad)
        self.assertEqual(releve.exception.code, "PREUVE_EFFET_REQUISE")

    def test_refs_tolerées_hors_etats_exiges(self) -> None:
        base = _base_current_valid()
        base["engagement_outcome"] = "not_engaged"
        base["engagement_ref"] = "eng-tolerée"
        base["validation_outcome"] = "uncertain"
        base["effect_outcome"] = "failed"
        base["effect_evidence_ref"] = "eff-tolerée"
        base["result_kind"] = "historical_operation"
        dec = result_from_mapping(base)
        self.assertEqual(dec.engagement_ref, "eng-tolerée")

    def test_courant_invalid_exige_not_engaged_not_started(self) -> None:
        for engagement, effet, ok in (
            ("not_engaged", "not_started", True),
            ("engaged", "not_started", False),
            ("not_engaged", "failed", False),
            ("unknown", "not_started", False),
        ):
            with self.subTest(engagement=engagement, effet=effet):
                base = _base_current_valid()
                base["validation_outcome"] = "invalid"
                base["engagement_outcome"] = engagement
                if engagement != "engaged":
                    base.pop("engagement_ref", None)
                else:
                    base["engagement_ref"] = "eng-1"
                base["effect_outcome"] = effet
                if effet != "applied":
                    base.pop("effect_evidence_ref", None)
                else:
                    base["effect_evidence_ref"] = "eff-1"
                if ok:
                    dec = result_from_mapping(base)
                    self.assertEqual(dec.validation_outcome, "invalid")
                else:
                    with self.assertRaises(CaResultError):
                        result_from_mapping(base)

    def test_historique_conserve_invalide_engage_applique(self) -> None:
        base = _base_current_valid()
        base["result_kind"] = "historical_operation"
        base["validation_outcome"] = "invalid"
        dec = result_from_mapping(base)
        self.assertEqual(dec.engagement_outcome, "engaged")
        self.assertEqual(dec.effect_outcome, "applied")

    def test_unknown_courant_representation_sans_nouvel_effet(self) -> None:
        for effet in ("not_started", "uncertain", "applied", "failed"):
            with self.subTest(effet=effet):
                base = _base_current_valid()
                base["engagement_outcome"] = "unknown"
                base.pop("engagement_ref", None)
                base["effect_outcome"] = effet
                if effet == "applied":
                    base["effect_evidence_ref"] = "eff-1"
                else:
                    base.pop("effect_evidence_ref", None)
                dec = result_from_mapping(base)
                self.assertEqual(dec.engagement_outcome, "unknown")
                self.assertEqual(dec.effect_outcome, effet)

    def test_unknown_historique_peut_representer_applique_ancien(self) -> None:
        base = _base_current_valid()
        base["result_kind"] = "historical_operation"
        base["engagement_outcome"] = "unknown"
        base.pop("engagement_ref", None)
        dec = result_from_mapping(base)
        self.assertEqual(dec.effect_outcome, "applied")

    def test_error_ok_ne_prouve_rien(self) -> None:
        base = _base_current_valid()
        base["effect_outcome"] = "uncertain"
        base.pop("effect_evidence_ref", None)
        base["error_code"] = "ok"
        dec = result_from_mapping(base)
        self.assertEqual(dec.error_code, "ok")
        self.assertEqual(dec.effect_outcome, "uncertain")

    def test_sans_registre_global_ni_bool(self) -> None:
        import pixs.pzt_ca.ca_result as module

        self.assertFalse(hasattr(module, "is_verified"))
        self.assertFalse(hasattr(module, "_GLOBAL"))
        self.assertFalse(hasattr(module, "_REGISTRY"))


if __name__ == "__main__":
    unittest.main()
