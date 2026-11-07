"""Unités exclusion/preuve, écrites seulement, sans effet."""

from __future__ import annotations

import datetime
import unittest

from pixs.pzt_ca.ca_exclusion import (
    CaExclusion,
    CaExclusionError,
    exclusion_from_json,
    exclusion_from_mapping,
)
from pixs.pzt_ca.ca_proof import (
    CaProofError,
    check_directive_proof_match,
    proof_from_json,
    proof_from_mapping,
)

_VALID_OBSERVED = "2026-10-23T09:00:00Z"
_VALID_NOW = datetime.datetime(2026, 10, 23, 9, 5, 0, tzinfo=datetime.timezone.utc)


class EvilEq:
    def __eq__(self, other: object) -> bool:
        raise AssertionError("EvilEq appele")


def _base_exclusion() -> dict:
    return {
        "object_type": "z12.ca_exclusion/v1",
        "schema_version": "1.0.0",
        "exclusion_id": "exc-1",
        "target_issuer_id": "iss-1",
        "target_generation_id": "gen-1",
        "target_key_ref": "key-1",
        "request_id": "req-1",
        "context_ref": "ctx-1",
        "operation_version": "opv-1",
        "epoch_current": 7,
        "target_set": ["proc-a", "sess-b"],
        "operation": "stop_perimeter",
        "reason_code": "incident_rotation",
        "mandate_ref": "mand-1",
    }


def _base_proof() -> dict:
    return {
        "object_type": "z12.ca_proof/v1",
        "schema_version": "1.0.0",
        "proof_id": "proof-1",
        "exclusion_id": "exc-1",
        "request_id": "req-1",
        "controller_id": "ctrl-1",
        "target_issuer_id": "iss-1",
        "target_key_ref": "key-1",
        "target_generation_id": "gen-1",
        "target_set": ["sess-b", "proc-a"],
        "operation": "stop_perimeter",
        "operation_version": "opv-1",
        "context_ref": "ctx-1",
        "mandate_ref": "mand-1",
        "applied_state": "stopped",
        "prohibition_maintained": "maintained",
        "observed_at": _VALID_OBSERVED,
        "epoch_current": 7,
        "proof_content_ref": "content-1",
        "proof_signature_ref": "sig-1",
    }


class ExclusionStructureTest(unittest.TestCase):
    def test_valide_sans_option(self) -> None:
        dec = exclusion_from_mapping(_base_exclusion())
        self.assertEqual(dec.operation, "stop_perimeter")
        self.assertIs(type(dec.target_set), tuple)
        self.assertEqual(set(dec.target_set), {"proc-a", "sess-b"})

    def test_liste_originale_non_conservee(self) -> None:
        base = _base_exclusion()
        lst = ["proc-a", "sess-b"]
        base["target_set"] = lst
        dec = exclusion_from_mapping(base)
        lst.append("proc-c")
        self.assertEqual(set(dec.target_set), {"proc-a", "sess-b"})

    def test_type_direct_refuse(self) -> None:
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping("faux")  # type: ignore[arg-type]

    def test_etranger_refuse(self) -> None:
        bad = _base_exclusion()
        bad["object_type"] = "z12.ca_proof/v1"
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_null_refuse(self) -> None:
        bad = _base_exclusion()
        bad["mandate_ref"] = None
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_doublon_cibles_refuse(self) -> None:
        bad = _base_exclusion()
        bad["target_set"] = ["proc-a", "proc-a"]
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_cibles_vides_refusees(self) -> None:
        bad = _base_exclusion()
        bad["target_set"] = []
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_operation_autre_refusee(self) -> None:
        bad = _base_exclusion()
        bad["operation"] = "inhibit_generation"
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_six_motifs_admis(self) -> None:
        for motif in (
            "incident_rotation",
            "planned_rotation",
            "loss_recovery",
            "succession",
            "compromise_suspected",
            "compromise_known",
        ):
            with self.subTest(motif=motif):
                base = _base_exclusion()
                base["reason_code"] = motif
                dec = exclusion_from_mapping(base)
                self.assertEqual(dec.reason_code, motif)

    def test_motif_inconnu_refuse(self) -> None:
        bad = _base_exclusion()
        bad["reason_code"] = "autre"
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_epoch_bool_refuse(self) -> None:
        bad = _base_exclusion()
        bad["epoch_current"] = True
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_epoch_negative_refusee(self) -> None:
        bad = _base_exclusion()
        bad["epoch_current"] = -1
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)

    def test_evil_eq_et_doublon_json(self) -> None:
        bad = _base_exclusion()
        bad["exclusion_id"] = EvilEq()  # type: ignore[dict-value]
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)
        with self.assertRaises(CaExclusionError):
            exclusion_from_json('{"a": 1, "a": 2}')

    def test_option_absente_admise_null_interdit(self) -> None:
        dec = exclusion_from_mapping(_base_exclusion())
        self.assertIsNone(dec.a12_context_ref)
        bad = _base_exclusion()
        bad["a12_context_ref"] = None
        with self.assertRaises(CaExclusionError):
            exclusion_from_mapping(bad)


class ProofStructureTest(unittest.TestCase):
    def test_valide_ordre_cibles_indifferent(self) -> None:
        dec = proof_from_mapping(_base_proof())
        self.assertEqual(set(dec.target_set), {"proc-a", "sess-b"})

    def test_not_maintained_representable(self) -> None:
        base = _base_proof()
        base["prohibition_maintained"] = "not_maintained"
        dec = proof_from_mapping(base)
        self.assertEqual(dec.prohibition_maintained, "not_maintained")

    def test_type_direct_refuse(self) -> None:
        with self.assertRaises(CaProofError):
            proof_from_mapping([])  # type: ignore[arg-type]

    def test_null_refuse(self) -> None:
        bad = _base_proof()
        bad["proof_signature_ref"] = None
        with self.assertRaises(CaProofError):
            proof_from_mapping(bad)

    def test_doublon_refuse(self) -> None:
        bad = _base_proof()
        bad["target_set"] = ["proc-a", "proc-a"]
        with self.assertRaises(CaProofError):
            proof_from_mapping(bad)

    def test_observed_naif_refuse(self) -> None:
        bad = _base_proof()
        bad["observed_at"] = "2026-10-23T09:00:00"
        with self.assertRaises(CaProofError):
            proof_from_mapping(bad)

    def test_epoch_str_refusee(self) -> None:
        bad = _base_proof()
        bad["epoch_current"] = "7"
        with self.assertRaises(CaProofError):
            proof_from_mapping(bad)

    def test_operation_etrangere_refusee(self) -> None:
        bad = _base_proof()
        bad["operation"] = "inhibit_generation"
        with self.assertRaises(CaProofError):
            proof_from_mapping(bad)


class MatchPureTest(unittest.TestCase):
    def _paire_valide(self) -> tuple[CaExclusion, object]:
        directive = exclusion_from_mapping(_base_exclusion())
        preuve = proof_from_mapping(_base_proof())
        return directive, preuve

    def test_match_valide_sans_ordre(self) -> None:
        directive, preuve = self._paire_valide()
        self.assertIsNone(
            check_directive_proof_match(directive, preuve, _VALID_NOW, 600)
        )

    def test_types_exacts_avant_comparaison(self) -> None:
        directive, preuve = self._paire_valide()
        with self.assertRaises(CaProofError):
            check_directive_proof_match({"faux": 1}, preuve, _VALID_NOW, 600)
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, {"faux": 1}, _VALID_NOW, 600)
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, preuve, "2026-10-23T09:05:00Z", 600)
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, preuve, _VALID_NOW, True)
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, preuve, _VALID_NOW, -1)

    def test_chaque_champ_cible_et_liens(self) -> None:
        champs = (
            "exclusion_id",
            "request_id",
            "target_issuer_id",
            "target_key_ref",
            "target_generation_id",
            "operation_version",
            "context_ref",
            "mandate_ref",
            "epoch_current",
        )
        for champ in champs:
            with self.subTest(champ=champ):
                directive, preuve = self._paire_valide()
                import dataclasses

                if champ == "epoch_current":
                    preuve2 = dataclasses.replace(preuve, epoch_current=8)
                else:
                    preuve2 = dataclasses.replace(preuve, **{champ: "autre"})
                with self.assertRaises(CaProofError):
                    check_directive_proof_match(directive, preuve2, _VALID_NOW, 600)

    def test_cibles_partielles_refusees(self) -> None:
        import dataclasses

        directive, preuve = self._paire_valide()
        partielle = dataclasses.replace(preuve, target_set=("proc-a",))
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, partielle, _VALID_NOW, 600)
        supplement = dataclasses.replace(preuve, target_set=("proc-a", "sess-b", "extra"))
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, supplement, _VALID_NOW, 600)

    def test_maintained_obligatoire(self) -> None:
        import dataclasses

        directive, preuve = self._paire_valide()
        degradee = dataclasses.replace(preuve, prohibition_maintained="not_maintained")
        with self.assertRaises(CaProofError) as releve:
            check_directive_proof_match(directive, degradee, _VALID_NOW, 600)
        self.assertEqual(releve.exception.code, "MAINTIEN_REQUIS")

    def test_fraicheur_exacte_admise_au_dela_refusee(self) -> None:
        directive, preuve = self._paire_valide()
        limite = _VALID_NOW - datetime.datetime(
            2026, 10, 23, 9, 0, 0, tzinfo=datetime.timezone.utc
        )
        exacte = int(limite.total_seconds())
        self.assertIsNone(
            check_directive_proof_match(directive, preuve, _VALID_NOW, exacte)
        )
        with self.assertRaises(CaProofError) as releve:
            check_directive_proof_match(directive, preuve, _VALID_NOW, exacte - 1)
        self.assertEqual(releve.exception.code, "PREUVE_PERIMEE")

    def test_observation_future_refusee(self) -> None:
        import dataclasses

        directive, preuve = self._paire_valide()
        future = dataclasses.replace(
            preuve,
            observed_at=datetime.datetime(
                2026, 10, 23, 9, 6, 0, tzinfo=datetime.timezone.utc
            ),
        )
        with self.assertRaises(CaProofError):
            check_directive_proof_match(directive, future, _VALID_NOW, 600)

    def test_sans_horloge_implicite_ni_bool(self) -> None:
        import pixs.pzt_ca.ca_proof as module

        self.assertFalse(hasattr(module, "is_verified"))
        self.assertFalse(hasattr(module, "is_authenticated"))
        self.assertFalse(hasattr(module, "authenticate_proof"))


class FreshnessMicrosecondEdgeTest(unittest.TestCase):
    def test_limite_plus_une_microseconde_refusee(self) -> None:
        import datetime
        directive = exclusion_from_mapping(_base_exclusion())
        preuve = proof_from_mapping(_base_proof())
        limite = _VALID_NOW - datetime.datetime(2026, 10, 23, 9, 0, 0, tzinfo=datetime.timezone.utc)
        exacte = limite.days * 86400 + limite.seconds
        self.assertIsNone(check_directive_proof_match(directive, preuve, _VALID_NOW, exacte))
        observed_plus = preuve.observed_at - datetime.timedelta(microseconds=1)
        import dataclasses
        decalee = dataclasses.replace(preuve, observed_at=observed_plus)
        with self.assertRaises(CaProofError) as releve:
            check_directive_proof_match(directive, decalee, _VALID_NOW, exacte)
        self.assertEqual(releve.exception.code, "PREUVE_PERIMEE")

    def test_tres_grande_borne_sans_float(self) -> None:
        directive = exclusion_from_mapping(_base_exclusion())
        preuve = proof_from_mapping(_base_proof())
        self.assertIsNone(check_directive_proof_match(directive, preuve, _VALID_NOW, 10 ** 1000))

    def test_borne_zero_exacte_puis_plus_une_microseconde(self) -> None:
        import dataclasses
        import datetime
        directive = exclusion_from_mapping(_base_exclusion())
        preuve = proof_from_mapping(_base_proof())
        instant = preuve.observed_at
        self.assertIsNone(check_directive_proof_match(directive, preuve, instant, 0))
        apres = instant + datetime.timedelta(microseconds=1)
        with self.assertRaises(CaProofError) as releve:
            check_directive_proof_match(directive, preuve, apres, 0)
        self.assertEqual(releve.exception.code, "PREUVE_PERIMEE")


if __name__ == "__main__":
    unittest.main()
