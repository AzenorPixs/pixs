import unittest
from dataclasses import FrozenInstanceError
from pixs.agent import resolution_receipt as rr


class ResolutionReceiptFormTest(unittest.TestCase):
    def _base(self, **over):
        kw = dict(binding_ref="bind-1", native_operation_ref="nop-1", native_result_ref="nres-1", native_snapshot_ref="nsnap-1", native_revision_ref="nrev-1", response_digest="digest-opaque-1", origin_proof_ref="proof-1", postcondition_refs=("pc-1", "pc-2"), time_evidence_ref="time-1")
        kw.update(over)
        return kw

    def test_nine_fields_closed(self):
        obj = rr.ResolutionReceipt(**self._base())
        self.assertEqual(obj.binding_ref, "bind-1")
        self.assertEqual(set(rr._FIELDS), {"binding_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "postcondition_refs", "time_evidence_ref"})
        self.assertEqual(len(rr._FIELDS), 9)
        import dataclasses as _dc
        names = {f.name for f in _dc.fields(rr.ResolutionReceipt)}
        self.assertEqual(names, set(rr._FIELDS))
        self.assertEqual(rr.RESOLUTION_RECEIPT_VERSION, "1.0.0")

    def test_opaque_mandatory(self):
        for field in ("binding_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref"):
            for bad in (None, "", "a\x00b"):
                with self.assertRaises(rr.ResolutionReceiptError):
                    rr.ResolutionReceipt(**self._base(**{field: bad}))

    def test_response_digest_opaque_no_hex_imposed(self):
        obj = rr.ResolutionReceipt(**self._base(response_digest="not-hex-at-all :: avec espaces"))
        self.assertEqual(obj.response_digest, "not-hex-at-all :: avec espaces")
        obj2 = rr.ResolutionReceipt(**self._base(response_digest="0" * 64))
        self.assertEqual(obj2.response_digest, "0" * 64)

    def test_strict_types_no_conversion(self):
        for field in ("binding_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref"):
            for bad in (0, True, False, b"x", ["x"], 1.5, {"x": 1}):
                with self.assertRaises(rr.ResolutionReceiptError):
                    rr.ResolutionReceipt(**self._base(**{field: bad}))
        for bad in (None, "x", b"x", ["pc-1"], {"x": 1}, "pc-1", ("pc-1", None), ("pc-1", ""), ("pc-1", "a\x00b"), ("pc-1", 0), ("pc-1", True)):
            with self.assertRaises(rr.ResolutionReceiptError):
                rr.ResolutionReceipt(**self._base(postcondition_refs=bad))

    def test_surrogate_and_str_subclass_refused(self):
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.ResolutionReceipt(**self._base(binding_ref="ok-\ud800-ok"))
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.ResolutionReceipt(**self._base(postcondition_refs=("ok", "bad-\ud800")))
        class S(str):
            pass
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.ResolutionReceipt(**self._base(native_result_ref=S("nres-1")))
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.ResolutionReceipt(**self._base(postcondition_refs=(S("pc-1"),)))

    def test_unicode_spaces_preserved_no_normalize(self):
        nfc = "caf\u00e9"
        nfd = "cafe\u0301"
        spaced = "  ref avec espaces  "
        self.assertNotEqual(nfc, nfd)
        o1 = rr.ResolutionReceipt(**self._base(native_snapshot_ref=nfc, origin_proof_ref=spaced))
        o2 = rr.ResolutionReceipt(**self._base(native_snapshot_ref=nfd, origin_proof_ref=spaced))
        self.assertEqual(o1.native_snapshot_ref, nfc)
        self.assertEqual(o2.native_snapshot_ref, nfd)
        self.assertNotEqual(o1.native_snapshot_ref, o2.native_snapshot_ref)
        self.assertEqual(o1.origin_proof_ref, spaced)

    def test_postconditions_order_duplicates_empty(self):
        ordered = ("b", "a", "b", "A")
        obj = rr.ResolutionReceipt(**self._base(postcondition_refs=ordered))
        self.assertEqual(obj.postcondition_refs, ordered)
        self.assertEqual(list(obj.postcondition_refs), ["b", "a", "b", "A"])
        empty = rr.ResolutionReceipt(**self._base(postcondition_refs=()))
        self.assertEqual(empty.postcondition_refs, ())
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.ResolutionReceipt(**self._base(postcondition_refs=["pc-1"]))

    def test_mapping_closed(self):
        good = self._base()
        obj = rr.resolution_receipt_from_mapping(dict(good))
        self.assertEqual(obj.binding_ref, "bind-1")
        self.assertEqual(obj.postcondition_refs, ("pc-1", "pc-2"))
        missing = dict(good)
        del missing["time_evidence_ref"]
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.resolution_receipt_from_mapping(missing)
        extra = dict(good)
        extra["qualified"] = True
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.resolution_receipt_from_mapping(extra)
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.resolution_receipt_from_mapping([("binding_ref", "x")])
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.resolution_receipt_from_mapping(None)

    def test_mapping_key_type_strict(self):
        class S(str):
            pass
        good = self._base()
        bad = {S(k): v for k, v in good.items()}
        self.assertEqual(set(bad.keys()), set(good.keys()))
        with self.assertRaises(rr.ResolutionReceiptError):
            rr.resolution_receipt_from_mapping(bad)

    def test_mapping_source_independent(self):
        src = self._base()
        obj = rr.resolution_receipt_from_mapping(src)
        src["binding_ref"] = "mutated"
        src["extra"] = "x"
        self.assertEqual(obj.binding_ref, "bind-1")
        self.assertFalse(hasattr(obj, "extra"))

    def test_immutable_and_slots(self):
        obj = rr.ResolutionReceipt(**self._base())
        with self.assertRaises(FrozenInstanceError):
            obj.binding_ref = "other"
        with self.assertRaises(FrozenInstanceError):
            obj.postcondition_refs = ()
        self.assertFalse(hasattr(obj, "__dict__"))
        with self.assertRaises(FrozenInstanceError):
            obj.postcondition_refs += ("pc-3",)

    def test_no_validity_property_fabricated(self):
        import dataclasses as _dc
        names = {f.name for f in _dc.fields(rr.ResolutionReceipt)}
        self.assertEqual(names, set(rr._FIELDS))
        obj = rr.ResolutionReceipt(**self._base())
        for name in ("qualified", "is_qualified", "valid", "is_valid", "proof_valid", "authorized", "version", "provider", "resolve", "load", "phase", "causal_order"):
            self.assertFalse(hasattr(obj, name))
        for name in ("qualified", "is_qualified", "resolve_result", "verify_origin", "verify_confirmation", "now", "registry", "load_provider"):
            self.assertFalse(hasattr(rr, name))
        a = rr.ResolutionReceipt(**self._base(binding_ref="b-1", postcondition_refs=()))
        b = rr.ResolutionReceipt(**self._base(binding_ref="b-2", postcondition_refs=("pc-1",)))
        self.assertNotEqual(a.binding_ref, b.binding_ref)

    def test_unexpected_errors_propagate(self):
        from unittest import mock as _mock
        good = self._base()
        with _mock.patch.object(rr, "ResolutionReceipt", side_effect=RuntimeError("boom-ctor")):
            with self.assertRaises(RuntimeError):
                rr.resolution_receipt_from_mapping(dict(good))


if __name__ == "__main__":
    unittest.main()
