"""Unités structurelles demande et décision, sans effet ni réseau."""
from __future__ import annotations

import datetime
import unittest

from pixs.pzt_ca.ca_decision import (
    CaDecision,
    CaDecisionError,
    decision_from_json,
    decision_from_mapping,
)
from pixs.pzt_ca.ca_request import (
    CaRequest,
    CaRequestError,
    request_from_json,
    request_from_mapping,
)

_VALID_AT = "2026-10-23T09:00:00Z"
_SENTINEL = "SENTINELLE-SANS-FUITE-zzz-123"


class EvilEq:
    """Objet dont l'égalité ne doit jamais être appelée."""

    def __eq__(self, other: object) -> bool:
        raise AssertionError("EvilEq.__eq__ appelé")


def _base_request(kind: str) -> dict:
    base = {
        "object_type": "z12.ca_request/v1",
        "schema_version": "1.0.0",
        "request_id": "req-1",
        "request_kind": kind,
        "domain": "dom-1",
        "policy_version": "pol-1",
        "epoch": 3,
        "requested_at": _VALID_AT,
        "command_metadata_ref": "cmd-1",
        "context_ref": "ctx-1",
    }
    if kind == "terminal_issuance":
        base.update({
            "subject_ref": "sub-1",
            "subject_public_key_ref": "spk-1",
            "possession_proof_ref": "pop-1",
            "terminal_contracts_ref": "tc-1",
        })
    elif kind == "intermediate_certification":
        base.update({
            "target_issuer_id": "iss-1",
            "target_generation_ref": "gen-1",
            "offline_procedure_ref": "off-1",
        })
    else:
        base.update({
            "offline_procedure_ref": "off-1",
            "root_plan_ref": "plan-1",
        })
    return base


class RequestStructureTest(unittest.TestCase):
    def test_terminal_valide(self) -> None:
        req = request_from_mapping(_base_request("terminal_issuance"))
        self.assertEqual(req.request_kind, "terminal_issuance")

    def test_epoch_moins_un_refuse(self) -> None:
        bad = _base_request("terminal_issuance")
        bad["epoch"] = -1
        with self.assertRaises(CaRequestError):
            request_from_mapping(bad)

    def test_epoch_booleen_refuse(self) -> None:
        bad = _base_request("terminal_issuance")
        bad["epoch"] = True
        with self.assertRaises(CaRequestError):
            request_from_mapping(bad)

    def test_objet_etranger_refuse(self) -> None:
        bad = _base_request("terminal_issuance")
        bad["object_type"] = "z12.autre/v1"
        with self.assertRaises(CaRequestError):
            request_from_mapping(bad)

    def test_evil_eq_non_appele(self) -> None:
        bad = _base_request("terminal_issuance")
        bad["object_type"] = EvilEq()  # type: ignore[dict-value]
        with self.assertRaises(CaRequestError):
            request_from_mapping(bad)

    def test_construction_directe_date_naive_refusee(self) -> None:
        good = _base_request("terminal_issuance")
        naive = datetime.datetime(2026, 10, 23, 9, 0, 0)
        with self.assertRaises(CaRequestError):
            CaRequest(
                object_type=good["object_type"],
                schema_version=good["schema_version"],
                request_id=good["request_id"],
                request_kind=good["request_kind"],
                domain=good["domain"],
                policy_version=good["policy_version"],
                epoch=good["epoch"],
                requested_at=naive,
                command_metadata_ref=good["command_metadata_ref"],
                context_ref=good["context_ref"],
                subject_ref="sub-1",
                subject_public_key_ref="spk-1",
                possession_proof_ref="pop-1",
                terminal_contracts_ref="tc-1",
            )

    def test_construction_directe_non_utc_refusee(self) -> None:
        tz = datetime.timezone(datetime.timedelta(hours=1))
        bad_time = datetime.datetime(2026, 10, 23, 9, 0, 0, tzinfo=tz)
        good = _base_request("terminal_issuance")
        with self.assertRaises(CaRequestError):
            CaRequest(
                object_type=good["object_type"],
                schema_version=good["schema_version"],
                request_id=good["request_id"],
                request_kind=good["request_kind"],
                domain=good["domain"],
                policy_version=good["policy_version"],
                epoch=good["epoch"],
                requested_at=bad_time,
                command_metadata_ref=good["command_metadata_ref"],
                context_ref=good["context_ref"],
                subject_ref="sub-1",
                subject_public_key_ref="spk-1",
                possession_proof_ref="pop-1",
                terminal_contracts_ref="tc-1",
            )

    def test_construction_directe_sous_classe_datetime_refusee(self) -> None:
        class SubDate(datetime.datetime):
            pass

        sub = SubDate(
            2026, 10, 23, 9, 0, 0, tzinfo=datetime.timezone.utc
        )
        good = _base_request("terminal_issuance")
        with self.assertRaises(CaRequestError):
            CaRequest(
                object_type=good["object_type"],
                schema_version=good["schema_version"],
                request_id=good["request_id"],
                request_kind=good["request_kind"],
                domain=good["domain"],
                policy_version=good["policy_version"],
                epoch=good["epoch"],
                requested_at=sub,
                command_metadata_ref=good["command_metadata_ref"],
                context_ref=good["context_ref"],
                subject_ref="sub-1",
                subject_public_key_ref="spk-1",
                possession_proof_ref="pop-1",
                terminal_contracts_ref="tc-1",
            )

    def test_branches_et_interdits(self) -> None:
        for kind, missing, extra in [
            ("terminal_issuance", "possession_proof_ref", "target_issuer_id"),
            ("intermediate_certification", "offline_procedure_ref", "subject_ref"),
            ("root_succession", "root_plan_ref", "subject_ref"),
        ]:
            bad = _base_request(kind)
            del bad[missing]
            with self.assertRaises(CaRequestError):
                request_from_mapping(bad)
            bad2 = _base_request(kind)
            bad2[extra] = "x"
            with self.assertRaises(CaRequestError):
                request_from_mapping(bad2)

    def test_null_optional_refuse(self) -> None:
        bad = _base_request("root_succession")
        bad["supersedes_request_id"] = None
        with self.assertRaises(CaRequestError):
            request_from_mapping(bad)

    def test_doublon_json_refuse(self) -> None:
        with self.assertRaises(CaRequestError):
            request_from_json('{"a": 1, "a": 2}')

    def test_diagnostic_sans_sentinelle(self) -> None:
        bad = _base_request("terminal_issuance")
        bad["request_id"] = _SENTINEL
        bad["epoch"] = -1
        try:
            request_from_mapping(bad)
        except CaRequestError as exc:
            self.assertNotIn(_SENTINEL, str(exc))
            self.assertEqual(exc.code, "EPOQUE_INVALIDE")
        else:
            self.fail("refus attendu")


class DecisionStructureTest(unittest.TestCase):
    def _admitted(self) -> dict:
        return {
            "object_type": "z12.ca_decision/v1",
            "schema_version": "1.0.0",
            "decision_id": "dec-1",
            "request_id": "req-1",
            "context_ref": "ctx-1",
            "verdict": "admitted",
            "decision_epoch": 3,
            "mandate_ref": "man-1",
            "authorized_issuer": "iss-1",
            "authorized_key_ref": "key-1",
            "authorized_generation": "gen-1",
        }

    def _refused(self) -> dict:
        return {
            "object_type": "z12.ca_decision/v1",
            "schema_version": "1.0.0",
            "decision_id": "dec-2",
            "request_id": "req-1",
            "context_ref": "ctx-1",
            "verdict": "refused",
            "decision_epoch": 3,
            "refusal_code": "mandate_missing",
        }

    def test_evil_eq_non_appele(self) -> None:
        bad = self._admitted()
        bad["object_type"] = EvilEq()  # type: ignore[dict-value]
        with self.assertRaises(CaDecisionError):
            decision_from_mapping(bad)

    def test_detail_vide_admis(self) -> None:
        good = self._admitted()
        good["refusal_detail_public"] = ""
        dec = decision_from_mapping(good)
        self.assertEqual(dec.refusal_detail_public, "")

    def test_detail_utf8_lf_admis_et_refuse(self) -> None:
        good = self._admitted()
        good["refusal_detail_public"] = "détail public ✓\nligne2"
        self.assertIn(
            "détail", decision_from_mapping(good).refusal_detail_public or ""
        )
        bad = self._refused()
        bad["refusal_detail_public"] = "détail public ✓\nligne2"
        self.assertIn(
            "détail", decision_from_mapping(bad).refusal_detail_public or ""
        )

    def test_detail_crlf_refuse(self) -> None:
        bad = self._refused()
        bad["refusal_detail_public"] = "a\r\nb"
        with self.assertRaises(CaDecisionError):
            decision_from_mapping(bad)

    def test_construction_directe_detail_vide(self) -> None:
        good = self._admitted()
        dec = CaDecision(
            object_type=good["object_type"],
            schema_version=good["schema_version"],
            decision_id=good["decision_id"],
            request_id=good["request_id"],
            context_ref=good["context_ref"],
            verdict=good["verdict"],
            decision_epoch=good["decision_epoch"],
            mandate_ref=good["mandate_ref"],
            authorized_issuer=good["authorized_issuer"],
            authorized_key_ref=good["authorized_key_ref"],
            authorized_generation=good["authorized_generation"],
            refusal_detail_public="",
        )
        self.assertEqual(dec.refusal_detail_public, "")

    def test_epoch_et_branches(self) -> None:
        for bad_epoch in (-1, True):
            bad = self._admitted()
            bad["decision_epoch"] = bad_epoch
            with self.assertRaises(CaDecisionError):
                decision_from_mapping(bad)
        bad = self._admitted()
        del bad["mandate_ref"]
        with self.assertRaises(CaDecisionError):
            decision_from_mapping(bad)
        bad = self._admitted()
        bad["refusal_code"] = "mandate_missing"
        with self.assertRaises(CaDecisionError):
            decision_from_mapping(bad)
        bad = self._refused()
        del bad["refusal_code"]
        with self.assertRaises(CaDecisionError):
            decision_from_mapping(bad)
        bad = self._refused()
        bad["authorized_issuer"] = "iss-1"
        with self.assertRaises(CaDecisionError):
            decision_from_mapping(bad)

    def test_doublon_et_sentinelle(self) -> None:
        with self.assertRaises(CaDecisionError):
            decision_from_json('{"a": 1, "a": 2}')
        bad = self._refused()
        bad["decision_id"] = _SENTINEL
        bad["decision_epoch"] = -1
        try:
            decision_from_mapping(bad)
        except CaDecisionError as exc:
            self.assertNotIn(_SENTINEL, str(exc))
            self.assertEqual(exc.code, "EPOQUE_INVALIDE")
        else:
            self.fail("refus attendu")


if __name__ == "__main__":
    unittest.main()
