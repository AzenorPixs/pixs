import unittest
from dataclasses import FrozenInstanceError
from pixs.agent import relay_composition as rc


class RelayCompositionFormTest(unittest.TestCase):
    def _base(self, **over):
        kw = dict(slot="AgentRelayStore", interface_version="1.0.0", provider_component="pixs-agent", implementation_ref="impl-1", implementation_version="v-1", composition_ref="comp-1", qualification_ref="qual-1")
        kw.update(over)
        return kw

    def test_seven_fields_closed(self):
        obj = rc.RelayComposition(**self._base())
        self.assertEqual(obj.slot, "AgentRelayStore")
        self.assertEqual(set(rc._FIELDS), {"slot", "interface_version", "provider_component", "implementation_ref", "implementation_version", "composition_ref", "qualification_ref"})
        self.assertEqual(len(rc._FIELDS), 7)
        import dataclasses as _dc
        names = {f.name for f in _dc.fields(rc.RelayComposition)}
        self.assertEqual(names, set(rc._FIELDS))

    def test_interface_version_exact(self):
        obj = rc.RelayComposition(**self._base())
        self.assertEqual(obj.interface_version, "1.0.0")
        self.assertEqual(rc.RELAY_COMPOSITION_VERSION, "1.0.0")
        for bad in (None, "", "1.0", "v1.0.0", "1.0.0 ", " 1.0.0", 0, True, b"1.0.0"):
            with self.assertRaises(rc.RelayCompositionError):
                rc.RelayComposition(**self._base(interface_version=bad))

    def test_opaque_mandatory_all_fields(self):
        for field in ("slot", "provider_component", "implementation_ref", "implementation_version", "composition_ref", "qualification_ref"):
            for bad in (None, "", "a\x00b"):
                with self.assertRaises(rc.RelayCompositionError):
                    rc.RelayComposition(**self._base(**{field: bad}))

    def test_strict_types_no_conversion(self):
        for field in rc._FIELDS:
            for bad in (0, True, False, b"x", ["x"], 1.5, {"x": 1}):
                with self.assertRaises(rc.RelayCompositionError):
                    rc.RelayComposition(**self._base(**{field: bad}))

    def test_surrogate_and_str_subclass_refused(self):
        with self.assertRaises(rc.RelayCompositionError):
            rc.RelayComposition(**self._base(slot="ok-\ud800-ok"))
        with self.assertRaises(rc.RelayCompositionError):
            rc.RelayComposition(**self._base(composition_ref="ok-\ud800-ok"))
        class S(str):
            pass
        with self.assertRaises(rc.RelayCompositionError):
            rc.RelayComposition(**self._base(slot=S("AgentRelayStore")))
        with self.assertRaises(rc.RelayCompositionError):
            rc.RelayComposition(**self._base(interface_version=S("1.0.0")))
        with self.assertRaises(rc.RelayCompositionError):
            rc.RelayComposition(**self._base(qualification_ref=S("qual-1")))

    def test_unicode_spaces_preserved_no_normalize(self):
        nfc = "caf\u00e9"
        nfd = "cafe\u0301"
        spaced = "  ref avec espaces  "
        self.assertNotEqual(nfc, nfd)
        o1 = rc.RelayComposition(**self._base(slot=nfc, composition_ref=spaced))
        o2 = rc.RelayComposition(**self._base(slot=nfd, composition_ref=spaced))
        self.assertEqual(o1.slot, nfc)
        self.assertEqual(o2.slot, nfd)
        self.assertNotEqual(o1.slot, o2.slot)
        self.assertEqual(o1.composition_ref, spaced)
        ordered = "b,a,A"
        o3 = rc.RelayComposition(**self._base(implementation_ref=ordered))
        self.assertEqual(o3.implementation_ref, ordered)

    def test_mapping_closed(self):
        good = self._base()
        obj = rc.relay_composition_from_mapping(dict(good))
        self.assertEqual(obj.composition_ref, "comp-1")
        missing = dict(good)
        del missing["qualification_ref"]
        with self.assertRaises(rc.RelayCompositionError):
            rc.relay_composition_from_mapping(missing)
        extra = dict(good)
        extra["qualified"] = True
        with self.assertRaises(rc.RelayCompositionError):
            rc.relay_composition_from_mapping(extra)
        with self.assertRaises(rc.RelayCompositionError):
            rc.relay_composition_from_mapping([("slot", "x")])
        with self.assertRaises(rc.RelayCompositionError):
            rc.relay_composition_from_mapping(None)

    def test_mapping_key_type_strict(self):
        class S(str):
            pass
        good = self._base()
        bad = {S(k): v for k, v in good.items()}
        self.assertEqual(set(bad.keys()), set(good.keys()))
        with self.assertRaises(rc.RelayCompositionError):
            rc.relay_composition_from_mapping(bad)

    def test_mapping_source_independent(self):
        src = self._base()
        obj = rc.relay_composition_from_mapping(src)
        src["composition_ref"] = "mutated"
        src["extra"] = "x"
        self.assertEqual(obj.composition_ref, "comp-1")
        self.assertFalse(hasattr(obj, "extra"))

    def test_immutable_and_slots(self):
        obj = rc.RelayComposition(**self._base())
        with self.assertRaises(FrozenInstanceError):
            obj.slot = "other"
        with self.assertRaises(FrozenInstanceError):
            obj.qualification_ref = "other"
        self.assertFalse(hasattr(obj, "__dict__"))

    def test_no_qualified_property_fabricated(self):
        import dataclasses as _dc
        names = {f.name for f in _dc.fields(rc.RelayComposition)}
        self.assertEqual(names, set(rc._FIELDS))
        obj = rc.RelayComposition(**self._base())
        for name in ("qualified", "is_qualified", "valid", "is_valid", "authorized", "version", "provider", "resolve", "load"):
            self.assertFalse(hasattr(obj, name))
        for name in ("qualified", "is_qualified", "load_provider", "resolve", "now", "registry"):
            self.assertFalse(hasattr(rc, name))
        a = rc.RelayComposition(**self._base(composition_ref="c-1", qualification_ref="q-same"))
        b = rc.RelayComposition(**self._base(composition_ref="c-2", qualification_ref="q-same"))
        self.assertEqual(a.qualification_ref, b.qualification_ref)
        self.assertNotEqual(a.composition_ref, b.composition_ref)

    def test_unexpected_errors_propagate(self):
        from unittest import mock as _mock
        good = self._base()
        with _mock.patch.object(rc, "RelayComposition", side_effect=RuntimeError("boom-ctor")):
            with self.assertRaises(RuntimeError):
                rc.relay_composition_from_mapping(dict(good))


if __name__ == "__main__":
    unittest.main()
