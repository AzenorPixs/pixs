"""Tests du descripteur declaratif, sans verification operationnelle."""

from dataclasses import FrozenInstanceError, replace
import unittest

from pixs.backend.runtime_profiles import RuntimeProfile, validate_runtime_profile


FIELDS = (
    "guaranteed_capabilities", "required_dependencies", "limitations", "disabled_capabilities",
)


class Hostile:
    def __bool__(self):
        raise AssertionError("protocole appele")

    def __hash__(self):
        raise AssertionError("protocole appele")

    def __eq__(self, other):
        raise AssertionError("protocole appele")

    def __repr__(self):
        raise AssertionError("protocole appele")


class HostileStr(str):
    def __hash__(self):
        raise AssertionError("protocole appele")

    def __eq__(self, other):
        raise AssertionError("protocole appele")

    def __repr__(self):
        raise AssertionError("protocole appele")


class TupleSubtype(tuple):
    def __iter__(self):
        raise AssertionError("protocole appele")


class ProfileSubtype(RuntimeProfile):
    def __getattribute__(self, name):
        raise AssertionError("protocole appele")


class RuntimeProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = RuntimeProfile("local", (), ("django", "postgresql"), ("non operationnel",), ("web",))

    def assert_invalid(self, value):
        with self.assertRaises(ValueError) as caught:
            validate_runtime_profile(value)
        self.assertEqual(str(caught.exception), "profil runtime invalide")

    def test_empty_collections_are_explicit(self):
        self.assertIs(validate_runtime_profile(RuntimeProfile("local", (), (), (), ())), True)

    def test_profile_names_are_not_mandatory_defaults(self):
        for name in ("development-local", "mono-tenant", "multi-tenant", "high-availability", "opaque-custom"):
            with self.subTest(name=name):
                self.assertIs(validate_runtime_profile(replace(self.profile, name=name)), True)

    def test_immutable_fields(self):
        with self.assertRaises(FrozenInstanceError):
            self.profile.name = "changed"
        self.assertIs(type(self.profile.required_dependencies), tuple)

    def test_exact_profile_type_before_protocols(self):
        for value in (None, False, (), {}, Hostile(), ProfileSubtype("x", (), (), (), ())):
            self.assert_invalid(value)

    def test_exact_nonempty_name_before_protocols(self):
        for value in (None, False, 0, "", (), Hostile(), HostileStr("x")):
            self.assert_invalid(replace(self.profile, name=value))

    def test_exact_tuple_collections_before_iteration(self):
        for field in FIELDS:
            for value in (None, [], "x", False, Hostile(), TupleSubtype(("x",))):
                self.assert_invalid(replace(self.profile, **{field: value}))

    def test_exact_nonempty_entries_before_hashing(self):
        for field in FIELDS:
            for value in (None, False, 0, "", Hostile(), HostileStr("x")):
                self.assert_invalid(replace(self.profile, **{field: (value,)}))

    def test_duplicates_rejected_in_each_collection(self):
        for field in FIELDS:
            self.assert_invalid(replace(self.profile, **{field: ("x", "x")}))

    def test_guaranteed_and_disabled_cannot_overlap(self):
        self.assert_invalid(replace(self.profile, guaranteed_capabilities=("web",)))

    def test_opaque_names_and_values_are_preserved(self):
        value = RuntimeProfile(" local ", ("Web",), ("dependency ",), (" ",), ("web",))
        self.assertIs(validate_runtime_profile(value), True)
        self.assertEqual(value.name, " local ")
        self.assertEqual(value.limitations, (" ",))

    def test_different_dimensions_do_not_imply_availability(self):
        value = RuntimeProfile("custom", ("postgresql",), ("postgresql",), (), ())
        self.assertIs(validate_runtime_profile(value), True)
        self.assertFalse(hasattr(value, "ready"))

    def test_diagnostic_never_contains_raw_input(self):
        self.assert_invalid(replace(self.profile, required_dependencies=("private-input", "private-input")))

    def test_validation_preserves_order_and_contents(self):
        value = RuntimeProfile("ordered", ("z", "a"), ("y", "b"), ("second", "first"), ("off",))
        before = value
        self.assertIs(validate_runtime_profile(value), True)
        self.assertEqual(value, before)
        self.assertEqual(value.guaranteed_capabilities, ("z", "a"))
