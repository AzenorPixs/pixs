import unittest
from dataclasses import FrozenInstanceError
from pixs.agent import relay_observation as ro


class RelayObservationFormTest(unittest.TestCase):
    def _base(self, **over):
        kw = dict(attempt_ref="att-1", outcome="UNKNOWN", receipt_ref=None, native_operation_ref=None, detail_ref=None)
        kw.update(over)
        return kw

    def test_three_outcomes_and_five_fields(self):
        for outcome in ("RECEIPT", "REFUSED_NO_SUBMISSION", "UNKNOWN"):
            kw = self._base(outcome=outcome, receipt_ref="rec-1" if outcome == "RECEIPT" else None)
            obj = ro.TransportObservation(**kw)
            self.assertEqual(obj.outcome, outcome)
        self.assertEqual(set(ro._FIELDS), {"attempt_ref", "outcome", "receipt_ref", "native_operation_ref", "detail_ref"})

    def test_attempt_ref_mandatory(self):
        for bad in (None, "", "a\x00b", 0, True, b"att", ["att"], {"x": 1}):
            with self.assertRaises(ro.TransportObservationError):
                ro.TransportObservation(**self._base(attempt_ref=bad))

    def test_receipt_required_for_receipt(self):
        for bad in (None, "", "x\x00y"):
            with self.assertRaises(ro.TransportObservationError):
                ro.TransportObservation(**self._base(outcome="RECEIPT", receipt_ref=bad))
        obj = ro.TransportObservation(**self._base(outcome="RECEIPT", receipt_ref="rec-opaque-1"))
        self.assertEqual(obj.receipt_ref, "rec-opaque-1")

    def test_other_nullabilities_unrestricted(self):
        for outcome in ("UNKNOWN", "REFUSED_NO_SUBMISSION"):
            o1 = ro.TransportObservation(**self._base(outcome=outcome, receipt_ref=None, native_operation_ref=None, detail_ref=None))
            self.assertIsNone(o1.receipt_ref)
            o2 = ro.TransportObservation(**self._base(outcome=outcome, receipt_ref="ref-unverified-1", native_operation_ref="nop-1", detail_ref="det-1"))
            self.assertEqual(o2.receipt_ref, "ref-unverified-1")

    def test_unknown_unverified_no_promotion(self):
        obj = ro.TransportObservation(**self._base(outcome="UNKNOWN", receipt_ref="unverified-rec-1", native_operation_ref="nop-1"))
        self.assertEqual(obj.outcome, "UNKNOWN")
        self.assertEqual(obj.receipt_ref, "unverified-rec-1")

    def test_strict_types_no_conversion(self):
        for field in ("attempt_ref", "receipt_ref", "native_operation_ref", "detail_ref"):
            for bad in (0, True, False, b"x", ["x"], 1.5):
                with self.assertRaises(ro.TransportObservationError):
                    ro.TransportObservation(**self._base(**{field: bad, "receipt_ref": "r-1" if field != "receipt_ref" else bad, "outcome": "UNKNOWN"}))

    def test_nul_and_empty_opaque(self):
        with self.assertRaises(ro.TransportObservationError):
            ro.TransportObservation(**self._base(native_operation_ref="a\x00b"))
        with self.assertRaises(ro.TransportObservationError):
            ro.TransportObservation(**self._base(detail_ref=""))
        with self.assertRaises(ro.TransportObservationError):
            ro.TransportObservation(**self._base(outcome=""))

    def test_surrogate_and_str_subclass_refused(self):
        with self.assertRaises(ro.TransportObservationError):
            ro.TransportObservation(**self._base(native_operation_ref="ok-\ud800-ok"))
        class S(str):
            pass
        with self.assertRaises(ro.TransportObservationError):
            ro.TransportObservation(**self._base(native_operation_ref=S("nop-1")))
        with self.assertRaises(ro.TransportObservationError):
            ro.TransportObservation(**self._base(outcome=S("UNKNOWN")))

    def test_unicode_spaces_preserved(self):
        nfc = "caf\u00e9"
        nfd = "cafe\u0301"
        spaced = "  ref avec espaces  "
        self.assertNotEqual(nfc, nfd)
        o1 = ro.TransportObservation(**self._base(native_operation_ref=nfc, detail_ref=spaced))
        o2 = ro.TransportObservation(**self._base(native_operation_ref=nfd, detail_ref=spaced))
        self.assertEqual(o1.native_operation_ref, nfc)
        self.assertEqual(o2.native_operation_ref, nfd)
        self.assertEqual(o1.detail_ref, spaced)
        self.assertNotEqual(o1.native_operation_ref, o2.native_operation_ref)

    def test_mapping_closed(self):
        good = self._base(outcome="UNKNOWN")
        obj = ro.transport_observation_from_mapping(dict(good))
        self.assertEqual(obj.attempt_ref, "att-1")
        missing = dict(good)
        del missing["detail_ref"]
        with self.assertRaises(ro.TransportObservationError):
            ro.transport_observation_from_mapping(missing)
        extra = dict(good)
        extra["proof"] = "x"
        with self.assertRaises(ro.TransportObservationError):
            ro.transport_observation_from_mapping(extra)
        with self.assertRaises(ro.TransportObservationError):
            ro.transport_observation_from_mapping([("attempt_ref", "a")])
        with self.assertRaises(ro.TransportObservationError):
            ro.transport_observation_from_mapping(None)

    def test_mapping_key_type_strict(self):
        class S(str):
            pass
        good = self._base(outcome="UNKNOWN")
        bad = {S(k): v for k, v in good.items()}
        self.assertEqual(set(bad.keys()), set(good.keys()))
        with self.assertRaises(ro.TransportObservationError):
            ro.transport_observation_from_mapping(bad)

    def test_mapping_source_independent(self):
        src = self._base(outcome="UNKNOWN", native_operation_ref="nop-1")
        obj = ro.transport_observation_from_mapping(src)
        src["native_operation_ref"] = "mutated"
        src["extra"] = "x"
        self.assertEqual(obj.native_operation_ref, "nop-1")
        self.assertFalse(hasattr(obj, "extra"))

    def test_immutable_and_slots(self):
        obj = ro.TransportObservation(**self._base(outcome="UNKNOWN"))
        with self.assertRaises(FrozenInstanceError):
            obj.outcome = "RECEIPT"
        self.assertFalse(hasattr(obj, "__dict__"))
        import dataclasses as _dc
        names = {f.name for f in _dc.fields(obj)}
        self.assertEqual(names, set(ro._FIELDS))

    def test_no_proof_version_field(self):
        import dataclasses as _dc
        names = {f.name for f in _dc.fields(ro.TransportObservation)}
        self.assertEqual(names, {"attempt_ref", "outcome", "receipt_ref", "native_operation_ref", "detail_ref"})
        self.assertEqual(ro.TRANSPORT_OBSERVATION_VERSION, "1.0.0")
        self.assertFalse(hasattr(ro.TransportObservation("a-1", "UNKNOWN", None, None, None), "version"))

    def test_twelve_private_reasons_closed(self):
        expected = ("COMMIT_UNRESOLVED", "BINDING_STALE", "GENERATION_STALE", "CLAIM_STALE", "PROVIDER_UNAVAILABLE", "AUTHORITY_REFUSED", "TIME_IN_DOUBT", "SUBMISSION_UNKNOWN", "RECEIPT_UNVERIFIABLE", "RESULT_DIVERGENT", "IDEMPOTENCE_CONFLICT", "PROFILE_UNAVAILABLE")
        self.assertEqual(set(ro.REASONS), set(expected))
        self.assertEqual(len(ro.REASONS), 12)
        for value in expected:
            ro.require_reason(value)
        for bad in ("RECEIPT", "ack", "", None, 0, True, "WIRE_OK"):
            with self.assertRaises(ro.TransportObservationError):
                ro.require_reason(bad)
        for value in ("RECEIPT", "REFUSED_NO_SUBMISSION", "UNKNOWN"):
            ro.require_outcome(value)
        for bad in ("ack", "", None, 0, True, "COMMIT_UNRESOLVED"):
            with self.assertRaises(ro.TransportObservationError):
                ro.require_outcome(bad)

    def test_unexpected_errors_propagate(self):
        from unittest import mock as _mock
        good = self._base(outcome="UNKNOWN")
        with _mock.patch.object(ro, "TransportObservation", side_effect=RuntimeError("boom-ctor")):
            with self.assertRaises(RuntimeError):
                ro.transport_observation_from_mapping(dict(good))


if __name__ == "__main__":
    unittest.main()
