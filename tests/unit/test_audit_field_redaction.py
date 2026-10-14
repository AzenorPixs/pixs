"""Adhésion de AuditFieldRedaction et de son validateur au contrat canonique."""

import dataclasses
from enum import Enum
import unittest

import pixs.kernel.audit_field_redaction as redaction_module
from pixs.kernel.audit_field_redaction import (
    AuditFieldRedaction,
    RedactionMode,
    validate_audit_field_redaction,
)
from pixs.kernel.diagnostics import VALIDATE

_ELEMENT_PREFIX = "audit_field_redaction."

_ALL_FIELDS = (
    "field_reference",
    "mode",
    "replacement_reference",
)

_MESSAGE_CANDIDATE = "profil d'occultation de champ exact attendu"
_MESSAGE_FIELD = "référence de champ opaque str exacte non vide attendue"
_MESSAGE_MODE = "membre exact de l'Enum fermé RedactionMode attendu"
_MESSAGE_REDACTED = "None explicite attendue en mode REDACTED"
_MESSAGE_PSEUDONYMIZED = (
    "référence pseudonyme opaque str exacte non vide attendue"
    " en mode PSEUDONYMIZED_REFERENCE"
)


def _full_redaction(**overrides: object) -> AuditFieldRedaction:
    fields: dict[str, object] = {
        "field_reference": "champ-1",
        "mode": RedactionMode.REDACTED,
        "replacement_reference": None,
    }
    fields.update(overrides)
    return AuditFieldRedaction(**fields)


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


class _ForeignMode(Enum):
    REDACTED = "REDACTED"


class TestModuleSurface(unittest.TestCase):
    def test_public_surface_follows_the_contract(self) -> None:
        self.assertEqual(
            redaction_module.__all__,
            [
                "RedactionMode",
                "AuditFieldRedaction",
                "validate_audit_field_redaction",
            ],
        )
        self.assertIs(redaction_module.RedactionMode, RedactionMode)
        self.assertIs(redaction_module.AuditFieldRedaction, AuditFieldRedaction)
        self.assertIs(
            redaction_module.validate_audit_field_redaction,
            validate_audit_field_redaction,
        )

    def test_fields_order_explicit_and_frozen(self) -> None:
        fields = dataclasses.fields(AuditFieldRedaction)
        self.assertEqual(tuple(field.name for field in fields), _ALL_FIELDS)
        self.assertTrue(
            all(
                field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING
                for field in fields
            )
        )
        redaction = _full_redaction()
        for field in _ALL_FIELDS:
            with self.subTest(field=field):
                with self.assertRaises(dataclasses.FrozenInstanceError):
                    setattr(redaction, field, "updated")

    def test_three_fields_must_be_explicit(self) -> None:
        with self.assertRaises(TypeError):
            AuditFieldRedaction()
        with self.assertRaises(TypeError):
            AuditFieldRedaction("champ-1", RedactionMode.REDACTED)
        with self.assertRaises(TypeError):
            AuditFieldRedaction("champ-1", RedactionMode.REDACTED, None, "extra")


class TestRedactionModeEnum(unittest.TestCase):
    def test_enum_is_closed_to_the_two_exact_members(self) -> None:
        self.assertEqual(
            [member.name for member in RedactionMode],
            ["REDACTED", "PSEUDONYMIZED_REFERENCE"],
        )
        self.assertEqual(
            [member.value for member in RedactionMode],
            ["REDACTED", "PSEUDONYMIZED_REFERENCE"],
        )
        self.assertEqual(RedactionMode.REDACTED.name, "REDACTED")
        self.assertEqual(
            RedactionMode.PSEUDONYMIZED_REFERENCE.name,
            "PSEUDONYMIZED_REFERENCE",
        )

    def test_non_members_refused_by_identity(self) -> None:
        for value in (None, True, False, 0, "REDACTED", _IntSub(1), _StrSub("REDACTED"), _ForeignMode.REDACTED):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_field_redaction(
                    _full_redaction(mode=value)
                )
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "mode"])
                self.assertEqual(diagnostics[0].message, _MESSAGE_MODE)

    def test_forged_member_refused(self) -> None:
        forged = object.__new__(RedactionMode)
        diagnostics = validate_audit_field_redaction(
            _full_redaction(mode=forged)
        )
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "mode"])
        self.assertEqual(diagnostics[0].message, _MESSAGE_MODE)

    def test_closed_enum_cannot_be_subclassed(self) -> None:
        with self.assertRaises(TypeError):
            class _ModeSub(RedactionMode):
                pass


class TestOpaqueReferences(unittest.TestCase):
    def test_field_reference_atypical_values_preserved(self) -> None:
        for value in (" ", "champ:opaque#1", "référence éé", "𝕌nicode-42"):
            with self.subTest(value=repr(value)):
                redaction = _full_redaction(field_reference=value)
                self.assertEqual(validate_audit_field_redaction(redaction), [])
                self.assertIs(redaction.field_reference, value)

    def test_invalid_field_reference_values_refused(self) -> None:
        for value in (None, "", True, 1, _StrSub("champ-1")):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_field_redaction(
                    _full_redaction(field_reference=value)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "field_reference"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_FIELD)

    def test_replacement_reference_atypical_values_preserved(self) -> None:
        for value in (" ", "ref:opaque#1", "référence", "𝕌nicode-42"):
            with self.subTest(value=repr(value)):
                redaction = _full_redaction(
                    mode=RedactionMode.PSEUDONYMIZED_REFERENCE,
                    replacement_reference=value,
                )
                self.assertEqual(validate_audit_field_redaction(redaction), [])
                self.assertIs(redaction.replacement_reference, value)

    def test_invalid_pseudonymized_references_refused(self) -> None:
        for value in ("", None, True, 1, _StrSub("ref-1")):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_field_redaction(
                    _full_redaction(
                        mode=RedactionMode.PSEUDONYMIZED_REFERENCE,
                        replacement_reference=value,
                    )
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "replacement_reference"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_PSEUDONYMIZED)


class TestCoherence(unittest.TestCase):
    def test_two_valid_configurations_yield_no_diagnostics(self) -> None:
        cases = (
            _full_redaction(
                mode=RedactionMode.REDACTED, replacement_reference=None
            ),
            _full_redaction(
                mode=RedactionMode.PSEUDONYMIZED_REFERENCE,
                replacement_reference="ref-1",
            ),
        )
        for index, redaction in enumerate(cases):
            with self.subTest(case=index):
                self.assertEqual(validate_audit_field_redaction(redaction), [])

    def test_redacted_with_reference_refused(self) -> None:
        for value in ("ref-1", "", 1, True, _StrSub("ref-1")):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_field_redaction(
                    _full_redaction(
                        mode=RedactionMode.REDACTED, replacement_reference=value
                    )
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "replacement_reference"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_REDACTED)

    def test_invalid_mode_never_cascades_on_replacement_reference(self) -> None:
        for value in ("REF-1", 1, True):
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_field_redaction(
                    _full_redaction(mode="inconnu", replacement_reference=value)
                )
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "mode"])
                self.assertEqual(diagnostics[0].message, _MESSAGE_MODE)


class TestCandidateType(unittest.TestCase):
    def test_foreign_candidates_refused(self) -> None:
        for candidate in (None, "redaction", {}, [], object()):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_audit_field_redaction(candidate)
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "candidate"])
                self.assertEqual(diagnostics[0].message, _MESSAGE_CANDIDATE)

    def test_subclass_candidate_refused(self) -> None:
        class _Sub(AuditFieldRedaction):
            pass

        base = _full_redaction()
        sub = _Sub(**{field: getattr(base, field) for field in _ALL_FIELDS})
        diagnostics = validate_audit_field_redaction(sub)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "candidate"])
        self.assertEqual(diagnostics[0].message, _MESSAGE_CANDIDATE)

    def test_foreign_hostile_candidate_never_accessed(self) -> None:
        hostile, counters = _make_hostile()
        diagnostics = validate_audit_field_redaction(hostile)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "candidate"])
        self.assertEqual(
            counters,
            {"bool": 0, "eq": 0, "len": 0, "str": 0, "repr": 0, "getattr": 0},
        )


class TestHostileValuesNeverInvoked(unittest.TestCase):
    def test_hostile_in_any_field_never_invoked_by_validator(self) -> None:
        for mode, reference in (
            (RedactionMode.REDACTED, None),
            (RedactionMode.PSEUDONYMIZED_REFERENCE, "ref-synthetic"),
        ):
            for field in _ALL_FIELDS:
                with self.subTest(field=field, mode=mode.name):
                    hostile, counters = _make_hostile()
                    overrides = {
                        "mode": mode,
                        "replacement_reference": reference,
                        field: hostile,
                    }
                    diagnostics = validate_audit_field_redaction(
                        _full_redaction(**overrides)
                    )
                    self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + field])
                    self.assertTrue(all(value == 0 for value in counters.values()))

    def test_hostile_str_subclasses_never_invoked(self) -> None:
        counters = {"bool": 0, "len": 0, "str": 0, "repr": 0}

        class HostileStr(str):
            def __bool__(self):
                counters["bool"] += 1
                return True

            def __len__(self):
                counters["len"] += 1
                return 1

            def __str__(self):
                counters["str"] += 1
                return "HOSTILE_STR"

            def __repr__(self):
                counters["repr"] += 1
                return "HOSTILE_REPR"

        for field in ("field_reference", "replacement_reference"):
            with self.subTest(field=field):
                diagnostics = validate_audit_field_redaction(
                    _full_redaction(
                        **{
                            "mode": RedactionMode.PSEUDONYMIZED_REFERENCE,
                            "replacement_reference": "ref-synthetic",
                            field: HostileStr("synthetic"),
                        }
                    )
                )
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + field])
                self.assertEqual(counters, {"bool": 0, "len": 0, "str": 0, "repr": 0})


class TestDiagnosticShape(unittest.TestCase):
    def _broken(self) -> AuditFieldRedaction:
        return _full_redaction(
            field_reference="",
            mode=True,
            replacement_reference="ECHO-MARKER",
        )

    def test_sorted_unique_stable_and_static(self) -> None:
        first = validate_audit_field_redaction(self._broken())
        second = validate_audit_field_redaction(self._broken())
        self.assertEqual(
            _elements(first),
            [_ELEMENT_PREFIX + "field_reference", _ELEMENT_PREFIX + "mode"],
        )
        self.assertTrue(
            all(d.step == VALIDATE and d.message == d.constraint for d in first)
        )
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual([(d.element, d.constraint, d.message) for d in second], keys)

    def test_invalid_reference_diagnostics_static_across_values(self) -> None:
        first = validate_audit_field_redaction(
            _full_redaction(replacement_reference="SYNTH_ECHO_FIRST")
        )
        second = validate_audit_field_redaction(
            _full_redaction(replacement_reference="SYNTH_ECHO_SECOND")
        )
        self.assertEqual(first, second)
        self.assertEqual(_elements(first), [_ELEMENT_PREFIX + "replacement_reference"])
        rendered = " | ".join(str(d) for d in first)
        self.assertNotIn("SYNTH_ECHO_FIRST", rendered)
        self.assertNotIn("SYNTH_ECHO_SECOND", rendered)

    def test_diagnostics_do_not_echo_values(self) -> None:
        rendered = " | ".join(
            str(d) for d in validate_audit_field_redaction(self._broken())
        )
        for marker in ("ECHO-MARKER", "HOSTILE", "True"):
            self.assertNotIn(marker, rendered)


if __name__ == "__main__":
    unittest.main()
