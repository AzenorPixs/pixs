"""Adhésion de TombstoneProfile et de son validateur au contrat canonique."""

import dataclasses
import unittest

import pixs.kernel.data_tombstone_profile as profile_module
from pixs.kernel.data_tombstone_profile import (
    TombstoneProfile,
    validate_data_tombstone_profile,
)
from pixs.kernel.diagnostics import VALIDATE

_ELEMENT_PREFIX = "data_tombstone_profile."

_ALL_FIELDS = (
    "resource_reference",
    "deletion_version",
    "deleted_at",
    "tenant_id",
    "scope_id",
    "retention_reference",
    "synchronization_reference",
    "deduplication_reference",
)

_OPTIONAL_FIELDS = (
    "tenant_id",
    "scope_id",
    "retention_reference",
    "synchronization_reference",
    "deduplication_reference",
)

_MESSAGE_PROFILE = "profil tombstone-v1 exact attendu"
_MESSAGE_RESOURCE = "référence opaque exacte non vide attendue"
_MESSAGE_VERSION = "entier exact supérieur ou égal à zéro attendu"
_MESSAGE_INSTANT = (
    "instant calendaire UTC exact au format YYYY-MM-DDTHH:MM:SS"
    " avec fraction optionnelle et suffixe Z ou +00:00 attendu"
)
_MESSAGE_OPTIONAL = "None exact ou référence opaque str exacte non vide attendue"
_MESSAGE_SCOPE_CONTEXT = "scope sans tenant explicite refusé"

_VALID_INSTANTS = (
    "2024-01-01T00:00:00Z",
    "2024-02-29T23:59:59Z",
    "2024-02-29T23:59:59+00:00",
    "2024-12-31T12:34:56.1Z",
    "2024-12-31T12:34:56.123456Z",
    "2024-12-31T12:34:56.123456+00:00",
    "2000-02-29T00:00:00Z",
    "0001-01-01T00:00:00Z",
    "9999-12-31T23:59:59.999999Z",
)

_INVALID_INSTANTS = (
    "0000-01-01T00:00:00Z",
    "0000-02-29T00:00:00Z",
    "2024-01-01T00:00:00,123Z",
    "2024-01-01T00:00:00X123Z",
    "2024-01-01T00:00:00.Z",
    "2024-01-01T00:00:00-00:00",
    "",
    "2024-01-01T00:00:00",
    "2024-01-01T00:00:00.1234567Z",
    "2024-01-01T00:00:00.12345678Z",
    "2024-01-01 00:00:00Z",
    "2024-01-01T00:00:00-01:00",
    "2024-01-01T00:00:00+01:00",
    "2024-01-01T00:00:00.123+0000",
    "2024-01-01T00:00:00Z ",
    "2024-01-01T00:00:00Z\n",
    "2024-01-01T00:00:60Z",
    "2024-01-01T00:60:00Z",
    "2024-01-01T24:00:00Z",
    "2024-01-32T00:00:00Z",
    "2024-13-01T00:00:00Z",
    "2023-02-29T00:00:00Z",
    "1900-02-29T00:00:00Z",
    "2100-02-29T00:00:00Z",
    "2024-01-01T00:00:00,Z",
    "2024-01-01T00:00:00,Z+00:00",
    "2024-01-01T00:00:00.5",
    "٢٠٢٤-٠١-٠١T٠٠:٠٠:٠٠Z",
    "2024-01-01T00:00:00．123Z",
)


def _full_profile(**overrides: object) -> TombstoneProfile:
    fields: dict[str, object] = {
        "resource_reference": "res-1",
        "deletion_version": 0,
        "deleted_at": "2024-01-01T00:00:00Z",
        "tenant_id": "tenant-1",
        "scope_id": "scope-1",
        "retention_reference": "retention-1",
        "synchronization_reference": "sync-1",
        "deduplication_reference": "dedup-1",
    }
    fields.update(overrides)
    return TombstoneProfile(**fields)


def _elements(diagnostics: list) -> list[str]:
    return [diagnostic.element for diagnostic in diagnostics]


def _make_hostile() -> tuple[object, dict[str, int]]:
    counters = {"bool": 0, "eq": 0, "len": 0, "str": 0, "repr": 0, "getattr": 0}

    class _Hostile:
        def __getattribute__(self, name: str) -> object:
            counters["getattr"] += 1
            return object.__getattribute__(self, name)

        def __bool__(self) -> bool:
            counters["bool"] += 1
            return True

        def __eq__(self, other: object) -> object:
            counters["eq"] += 1
            return NotImplemented

        def __len__(self) -> int:
            counters["len"] += 1
            return 0

        def __str__(self) -> str:
            counters["str"] += 1
            return "HOSTILE_STR_MARKER"

        def __repr__(self) -> str:
            counters["repr"] += 1
            return "HOSTILE_REPR_MARKER"

    return _Hostile(), counters


class _StrSub(str):
    pass


class _IntSub(int):
    pass


class TestModuleSurface(unittest.TestCase):
    def test_fields_order_frozen_and_public_surface_follow_the_contract(self) -> None:
        fields = dataclasses.fields(TombstoneProfile)
        self.assertEqual(tuple(field.name for field in fields), _ALL_FIELDS)
        profile = _full_profile()
        for field in _ALL_FIELDS:
            with self.subTest(field=field):
                with self.assertRaises(dataclasses.FrozenInstanceError):
                    setattr(profile, field, "updated")
        self.assertTrue(
            all(
                field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING
                for field in fields
            )
        )
        self.assertEqual(
            profile_module.__all__,
            ["TombstoneProfile", "validate_data_tombstone_profile"],
        )
        self.assertIs(profile_module.TombstoneProfile, TombstoneProfile)
        self.assertIs(
            profile_module.validate_data_tombstone_profile,
            validate_data_tombstone_profile,
        )


class TestValidShapes(unittest.TestCase):
    def test_full_valid_profile_yields_no_diagnostics(self) -> None:
        self.assertEqual(validate_data_tombstone_profile(_full_profile()), [])

    def test_all_optional_fields_none_yields_no_diagnostics(self) -> None:
        profile = _full_profile(
            tenant_id=None,
            scope_id=None,
            retention_reference=None,
            synchronization_reference=None,
            deduplication_reference=None,
        )
        self.assertEqual(validate_data_tombstone_profile(profile), [])

    def test_each_optional_field_accepts_none_or_exact_str(self) -> None:
        for field in _OPTIONAL_FIELDS:
            for value in (None, "valeur-synthetique"):
                with self.subTest(field=field, value=value):
                    overrides = {field: value}
                    if field == "tenant_id" and value is None:
                        overrides["scope_id"] = None
                    profile = _full_profile(**overrides)
                    self.assertEqual(validate_data_tombstone_profile(profile), [])

    def test_valid_instants_yield_no_diagnostics(self) -> None:
        for value in _VALID_INSTANTS:
            with self.subTest(value=value):
                self.assertEqual(
                    validate_data_tombstone_profile(_full_profile(deleted_at=value)),
                    [],
                )

    def test_opaque_references_preserved_without_normalization(self) -> None:
        profile = _full_profile(
            resource_reference="  /res :opaque#  ",
            tenant_id=" ",
            scope_id="scope: ",
            retention_reference="r",
            synchronization_reference="s",
            deduplication_reference="d",
        )
        self.assertEqual(validate_data_tombstone_profile(profile), [])
        self.assertEqual(profile.resource_reference, "  /res :opaque#  ")
        self.assertEqual(profile.tenant_id, " ")
        self.assertEqual(profile.scope_id, "scope: ")


class TestDeletionVersion(unittest.TestCase):
    def test_exact_nonnegative_ints_accepted(self) -> None:
        for value in (0, 1, 2**64):
            with self.subTest(value=value):
                self.assertEqual(
                    validate_data_tombstone_profile(
                        _full_profile(deletion_version=value)
                    ),
                    [],
                )

    def test_bad_version_values_refused(self) -> None:
        for value in (-1, True, False, 1.0, "1", None, _IntSub(1), _StrSub("1")):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_data_tombstone_profile(
                    _full_profile(deletion_version=value)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "deletion_version"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_VERSION)


class TestInvalidRefs(unittest.TestCase):
    def test_bad_resource_reference_refused(self) -> None:
        for value in (None, "", True, 1, _StrSub("res-1")):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_data_tombstone_profile(
                    _full_profile(resource_reference=value)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "resource_reference"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_RESOURCE)

    def test_bad_optional_values_refused_as_field_never_as_scope(self) -> None:
        for field in _OPTIONAL_FIELDS:
            for value in ("", True, 1, _StrSub("opt-1")):
                with self.subTest(field=field, value=type(value).__name__):
                    diagnostics = validate_data_tombstone_profile(
                        _full_profile(**{field: value})
                    )
                    expected = [_ELEMENT_PREFIX + field]
                    self.assertEqual(_elements(diagnostics), sorted(expected))
                    for diagnostic in diagnostics:
                        if diagnostic.element.endswith("scope_context"):
                            self.assertEqual(diagnostic.message, _MESSAGE_SCOPE_CONTEXT)
                        else:
                            self.assertEqual(diagnostic.message, _MESSAGE_OPTIONAL)


class TestDeletedAt(unittest.TestCase):
    def test_non_str_instants_refused(self) -> None:
        for value in (None, 0, True, _StrSub("2024-01-01T00:00:00Z")):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_data_tombstone_profile(
                    _full_profile(deleted_at=value)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "deleted_at"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_INSTANT)

    def test_invalid_instant_forms_refused(self) -> None:
        for value in _INVALID_INSTANTS:
            with self.subTest(instant=repr(value)):
                diagnostics = validate_data_tombstone_profile(
                    _full_profile(deleted_at=value)
                )
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "deleted_at"])
                self.assertEqual(diagnostics[0].message, _MESSAGE_INSTANT)


class TestScopeContext(unittest.TestCase):
    def test_scope_without_explicit_tenant_refused(self) -> None:
        diagnostics = validate_data_tombstone_profile(
            _full_profile(tenant_id=None)
        )
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "scope_context"])
        self.assertEqual(diagnostics[0].message, _MESSAGE_SCOPE_CONTEXT)

    def test_scope_rule_is_independent_of_other_validations(self) -> None:
        cases = (
            {"tenant_id": None, "scope_id": _StrSub("scope-1")},
            {"tenant_id": None, "scope_id": 7},
            {"tenant_id": None, "scope_id": True},
            {"tenant_id": None, "deleted_at": "2024-01-01T00:00:00"},
        )
        for overrides in cases:
            with self.subTest(**overrides):
                diagnostics = _elements(
                    validate_data_tombstone_profile(_full_profile(**overrides))
                )
                self.assertIn(_ELEMENT_PREFIX + "scope_context", diagnostics)

    def test_tenant_without_scope_accepted(self) -> None:
        profile = _full_profile(scope_id=None)
        self.assertEqual(validate_data_tombstone_profile(profile), [])


class TestCandidateType(unittest.TestCase):
    def test_foreign_candidates_refused(self) -> None:
        for candidate in (None, "profile", {}, [], object()):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_data_tombstone_profile(candidate)
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "profile"])
                self.assertEqual(diagnostics[0].message, _MESSAGE_PROFILE)

    def test_subclass_candidate_refused(self) -> None:
        class _Sub(TombstoneProfile):
            pass

        base = _full_profile()
        sub = _Sub(**{field: getattr(base, field) for field in _ALL_FIELDS})
        diagnostics = validate_data_tombstone_profile(sub)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "profile"])
        self.assertEqual(diagnostics[0].message, _MESSAGE_PROFILE)

    def test_foreign_hostile_candidate_never_accessed(self) -> None:
        hostile, counters = _make_hostile()
        diagnostics = validate_data_tombstone_profile(hostile)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "profile"])
        self.assertEqual(
            counters,
            {"bool": 0, "eq": 0, "len": 0, "str": 0, "repr": 0, "getattr": 0},
        )


class TestHostileValuesNeverInvoked(unittest.TestCase):
    def test_hostile_in_any_field_never_invoked_by_validator(self) -> None:
        for field in _ALL_FIELDS:
            with self.subTest(field=field):
                hostile, counters = _make_hostile()
                diagnostics = validate_data_tombstone_profile(
                    _full_profile(**{field: hostile})
                )
                self.assertIn(_ELEMENT_PREFIX + field, _elements(diagnostics))
                self.assertEqual(
                    counters,
                    {
                        "bool": 0,
                        "eq": 0,
                        "len": 0,
                        "str": 0,
                        "repr": 0,
                        "getattr": 0,
                    },
                )


class TestDiagnosticShape(unittest.TestCase):
    def _broken(self) -> TombstoneProfile:
        return _full_profile(
            resource_reference="",
            deletion_version=True,
            deleted_at="ECHO-MARKER",
            tenant_id="",
            scope_id=1,
            retention_reference=_StrSub("ECHO-MARKER-2"),
            synchronization_reference=True,
            deduplication_reference=2,
        )

    def test_all_fields_invalid_yield_sorted_unique_stable_diagnostics(self) -> None:
        first = validate_data_tombstone_profile(self._broken())
        second = validate_data_tombstone_profile(self._broken())
        expected_elements = sorted(
            _ELEMENT_PREFIX + field for field in _ALL_FIELDS
        )
        self.assertEqual(_elements(first), expected_elements)
        self.assertTrue(
            all(d.step == VALIDATE and d.message == d.constraint for d in first)
        )
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual([(d.element, d.constraint, d.message) for d in second], keys)

    def test_diagnostics_do_not_echo_values(self) -> None:
        rendered = " | ".join(
            str(d) for d in validate_data_tombstone_profile(self._broken())
        )
        for marker in ("ECHO-MARKER", "HOSTILE", "True"):
            self.assertNotIn(marker, rendered)
        for diagnostic in validate_data_tombstone_profile(self._broken()):
            self.assertTrue(diagnostic.element.startswith(_ELEMENT_PREFIX))


if __name__ == "__main__":
    unittest.main()
