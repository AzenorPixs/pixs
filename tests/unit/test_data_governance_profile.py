"""Adhesion de DataGovernanceProfile et de son validateur au contrat design."""

import dataclasses
import enum
import unittest

import pixs.kernel.data_governance_profile as profile_module
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.data_governance_profile import (
    DataGovernanceProfile,
    validate_data_governance_profile,
)

_ELEMENT_PREFIX = "data_governance_profile."

_OPAQUE_FIELDS = (
    "data_asset_id",
    "owner_component",
    "source_of_truth",
    "retention_policy",
    "deletion_policy",
    "export_policy",
    "lineage",
)

_COLLECTION_FIELDS = (
    "data_classes",
    "purpose_refs",
    "residency_constraints",
    "authorized_consumers",
    "processor_refs",
)

_ALL_FIELDS = (
    "profile_version",
    "data_asset_id",
    "owner_component",
    "source_of_truth",
    "data_classes",
    "confidentiality",
    "personal_data",
    "purpose_refs",
    "retention_policy",
    "deletion_policy",
    "residency_constraints",
    "authorized_consumers",
    "processor_refs",
    "export_policy",
    "lineage",
)


def _valid_profile(**overrides: object) -> DataGovernanceProfile:
    fields: dict[str, object] = {
        "profile_version": "1.0.0",
        "data_asset_id": "asset-1",
        "owner_component": "owner-1",
        "source_of_truth": "source-1",
        "data_classes": frozenset({"class-a"}),
        "confidentiality": ConfidentialityLevel.INTERNAL,
        "personal_data": PersonalDataLevel.NONE,
        "purpose_refs": frozenset({"purpose-a"}),
        "retention_policy": "retention-1",
        "deletion_policy": "deletion-1",
        "residency_constraints": frozenset({"constraint-a"}),
        "authorized_consumers": frozenset({"consumer-a"}),
        "processor_refs": frozenset({"processor-a"}),
        "export_policy": "export-1",
        "lineage": "lineage-1",
    }
    fields.update(overrides)
    return DataGovernanceProfile(**fields)


def _elements(diagnostics: list[Diagnostic]) -> list[str]:
    return [diagnostic.element for diagnostic in diagnostics]


class _StrSub(str):
    pass


class _FrozensetSub(frozenset):
    pass


class _OtherConfidentiality(enum.Enum):
    INTERNAL = "INTERNAL"


class _OtherPersonalData(enum.Enum):
    NONE = "NONE"


class _Hostile:
    def __init__(self) -> None:
        self.eq_calls = 0
        self.hash_calls = 0
        self.str_calls = 0
        self.repr_calls = 0
        self.bool_calls = 0

    def __bool__(self) -> bool:
        self.bool_calls += 1
        return True

    def __eq__(self, other: object) -> bool:
        self.eq_calls += 1
        return NotImplemented

    def __hash__(self) -> int:
        self.hash_calls += 1
        return 5

    def __str__(self) -> str:
        self.str_calls += 1
        return "HOSTILE_STR_MARKER"

    def __repr__(self) -> str:
        self.repr_calls += 1
        return "HOSTILE_REPR_MARKER"


class _ReadProbe:
    def __init__(self) -> None:
        self.getattr_calls = 0

    def __getattr__(self, name: str) -> object:
        self.getattr_calls += 1
        raise AttributeError(name)


class _Twin:
    def __init__(self) -> None:
        profile = _valid_profile()
        for field in _ALL_FIELDS:
            object.__setattr__(self, field, getattr(profile, field))


class TestValidShape(unittest.TestCase):
    def test_valid_profile_yields_no_diagnostics(self) -> None:
        self.assertEqual(validate_data_governance_profile(_valid_profile()), [])

    def test_all_members_accepted_for_canonical_dimensions(self) -> None:
        for member in ConfidentialityLevel:
            with self.subTest(confidentiality=member.name):
                self.assertEqual(
                    validate_data_governance_profile(
                        _valid_profile(confidentiality=member)
                    ),
                    [],
                )
        for member in PersonalDataLevel:
            with self.subTest(personal_data=member.name):
                self.assertEqual(
                    validate_data_governance_profile(
                        _valid_profile(personal_data=member)
                    ),
                    [],
                )

    def test_empty_collections_accepted_without_invented_obligation(self) -> None:
        overrides = {field: frozenset() for field in _COLLECTION_FIELDS}
        self.assertEqual(
            validate_data_governance_profile(_valid_profile(**overrides)), []
        )


class TestCandidateType(unittest.TestCase):
    def test_foreign_candidates_refused_as_single_diagnostic(self) -> None:
        class _Sub(DataGovernanceProfile):
            pass

        base = _valid_profile()
        sub = _Sub(**{field: getattr(base, field) for field in _ALL_FIELDS})
        for candidate in (None, "profile", {}, sub, _Twin()):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_data_governance_profile(candidate)
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "profile"])

    def test_candidate_without_public_shape_never_reads_attributes(self) -> None:
        probe = _ReadProbe()
        diagnostics = validate_data_governance_profile(probe)
        self.assertEqual(probe.getattr_calls, 0)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "profile"])


class TestProfileVersion(unittest.TestCase):
    def test_valid_semver_accepted(self) -> None:
        for version in ("1.0.0", "0.1.2", "2.3.4", "1.0.0-alpha+build"):
            with self.subTest(version=version):
                self.assertEqual(
                    validate_data_governance_profile(
                        _valid_profile(profile_version=version)
                    ),
                    [],
                )

    def test_invalid_versions_refused(self) -> None:
        for version in (None, True, 1, _StrSub("1.0.0"), "", "1.0", "v1.0.0", "01.0.0"):
            with self.subTest(version=repr(version)):
                diagnostics = validate_data_governance_profile(
                    _valid_profile(profile_version=version)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "profile_version"]
                )


class TestOpaqueReferences(unittest.TestCase):
    def test_invalid_references_refused_per_field(self) -> None:
        for field in _OPAQUE_FIELDS:
            for value in (None, True, 1, _StrSub("opaque-1"), ""):
                with self.subTest(field=field, value=repr(value)):
                    diagnostics = validate_data_governance_profile(
                        _valid_profile(**{field: value})
                    )
                    self.assertEqual(
                        _elements(diagnostics), [_ELEMENT_PREFIX + field]
                    )

    def test_opaque_references_are_preserved_without_normalization(self) -> None:
        raw = "  /référence :opaque#  "
        collection = frozenset({raw})
        overrides = {field: raw for field in _OPAQUE_FIELDS}
        overrides.update({field: collection for field in _COLLECTION_FIELDS})
        profile = _valid_profile(**overrides)
        self.assertEqual(validate_data_governance_profile(profile), [])
        for field, value in overrides.items():
            self.assertEqual(getattr(profile, field), value)
        spaces = {field: " " for field in _OPAQUE_FIELDS}
        spaces.update({field: frozenset({" "}) for field in _COLLECTION_FIELDS})
        self.assertEqual(validate_data_governance_profile(_valid_profile(**spaces)), [])


class TestCollections(unittest.TestCase):
    def test_inexact_containers_refused(self) -> None:
        for field in _COLLECTION_FIELDS:
            for container in (
                {"ref-a"},
                ["ref-a"],
                ("ref-a",),
                _FrozensetSub({"ref-a"}),
                "ref-a",
                None,
                True,
                1,
            ):
                with self.subTest(field=field, container=type(container).__name__):
                    diagnostics = validate_data_governance_profile(
                        _valid_profile(**{field: container})
                    )
                    self.assertEqual(
                        _elements(diagnostics), [_ELEMENT_PREFIX + field]
                    )

    def test_invalid_elements_refused(self) -> None:
        for field in _COLLECTION_FIELDS:
            for elements in (
                frozenset({None}),
                frozenset({True}),
                frozenset({1}),
                frozenset({_StrSub("ref-a")}),
                frozenset({""}),
            ):
                with self.subTest(field=field, element=type(next(iter(elements))).__name__):
                    diagnostics = validate_data_governance_profile(
                        _valid_profile(**{field: elements})
                    )
                    self.assertEqual(
                        _elements(diagnostics), [_ELEMENT_PREFIX + field]
                    )

    def test_hostile_values_and_elements_never_invoked_by_validator(self) -> None:
        for field in _ALL_FIELDS:
            with self.subTest(field=field):
                hostile = _Hostile()
                value = frozenset({hostile}) if field in _COLLECTION_FIELDS else hostile
                hostile.eq_calls = hostile.hash_calls = hostile.str_calls = 0
                hostile.repr_calls = hostile.bool_calls = 0
                diagnostics = validate_data_governance_profile(
                    _valid_profile(**{field: value})
                )
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + field])
                self.assertEqual(
                    (hostile.eq_calls, hostile.hash_calls, hostile.str_calls,
                     hostile.repr_calls, hostile.bool_calls),
                    (0, 0, 0, 0, 0),
                )


class TestCanonicalDimensions(unittest.TestCase):
    def test_values_and_proxies_refused_by_identity(self) -> None:
        for field, bad_values in (
            (
                "confidentiality",
                (
                    "INTERNAL",
                    None,
                    _OtherConfidentiality.INTERNAL,
                ),
            ),
            (
                "personal_data",
                ("NONE", None, _OtherPersonalData.NONE),
            ),
        ):
            for value in bad_values:
                with self.subTest(field=field, value=repr(value)):
                    diagnostics = validate_data_governance_profile(
                        _valid_profile(**{field: value})
                    )
                    self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + field])




class TestDiagnosticShape(unittest.TestCase):
    def test_all_fields_invalid_yield_sorted_unique_stable_diagnostics(self) -> None:
        broken = _valid_profile(
            profile_version="MARKER-VERSION",
            data_asset_id=_StrSub("MARKER-OPAQUE"),
            owner_component="",
            source_of_truth=None,
            data_classes={"MARKER-SET"},
            confidentiality="MARKER-CONF",
            personal_data=_OtherPersonalData.NONE,
            purpose_refs=["MARKER-LIST"],
            retention_policy=True,
            deletion_policy=1,
            residency_constraints=_FrozensetSub({"MARKER-SUB"}),
            authorized_consumers=None,
            processor_refs=(),
            export_policy=_StrSub("MARKER-EXPORT"),
            lineage="",
        )
        first = validate_data_governance_profile(broken)
        second = validate_data_governance_profile(broken)
        self.assertEqual(len(first), len(_ALL_FIELDS))
        self.assertTrue(all(d.step == VALIDATE and d.message == d.constraint for d in first))
        alternate = validate_data_governance_profile(
            _valid_profile(**{field: None for field in _ALL_FIELDS})
        )
        self.assertEqual(first, alternate)
        self.assertNotIn("MARKER", str(first))
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(
            [(d.element, d.constraint, d.message) for d in second], keys
        )
        elements = _elements(first)
        self.assertEqual(elements, sorted(elements))
        self.assertEqual(
            set(elements), {_ELEMENT_PREFIX + field for field in _ALL_FIELDS}
        )

    def test_diagnostics_do_not_echo_values(self) -> None:
        diagnostics = validate_data_governance_profile(
            _valid_profile(profile_version="MARKER-VERSION")
        )
        rendered = " | ".join(str(d) for d in diagnostics)
        for marker in ("MARKER-VERSION", "MARKER", "HOSTILE"):
            self.assertNotIn(marker, rendered)


class TestModuleSurface(unittest.TestCase):
    def test_model_fields_and_public_surface_follow_the_contract(self) -> None:
        fields = dataclasses.fields(DataGovernanceProfile)
        self.assertEqual(tuple(field.name for field in fields), _ALL_FIELDS)
        self.assertTrue(all(field.default is dataclasses.MISSING and
                            field.default_factory is dataclasses.MISSING for field in fields))
        self.assertEqual(
            profile_module.__all__,
            ["DataGovernanceProfile", "validate_data_governance_profile"],
        )
        self.assertIs(profile_module.DataGovernanceProfile, DataGovernanceProfile)
        self.assertIs(
            profile_module.validate_data_governance_profile,
            validate_data_governance_profile,
        )

    def test_profile_is_frozen(self) -> None:
        profile = _valid_profile()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            setattr(profile, "profile_version", "2.0.0")
        self.assertEqual(profile.profile_version, "1.0.0")


if __name__ == "__main__":
    unittest.main()
