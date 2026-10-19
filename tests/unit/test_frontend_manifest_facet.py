"""Tests unitaires FrontendManifestFacet v1 : profils publics seuls, sans I/O."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch


def _valid_contribution(
    *,
    type_text: str = "ROUTE",
    id_text: str = "acme.crm.contacts",
    entry_text: str = "frontend/routes/contacts",
    version_text: str = "1.0.0",
    requires=None,
    scope_text: str = "TENANT_SCOPED",
) -> dict:
    if requires is None:
        requires = []
    return {
        "type": type_text,
        "id": id_text,
        "entry": entry_text,
        "version": version_text,
        "requires": list(requires),
        "scope": scope_text,
    }


def _base_manifest(
    *,
    comp_type: str = "MODULE",
    with_frontend: bool = True,
    contributions=None,
) -> dict:
    data: dict = {
        "schema_version": "1",
        "id": "demo",
        "type": comp_type,
        "version": "1.0.0",
    }
    if with_frontend:
        data["frontend"] = {
            "schema_version": "1",
            "contributions": [] if contributions is None else list(contributions),
        }
    return data


def _parse(data):
    from pixs.kernel.manifest import parse_manifest

    return parse_manifest(data)


def _parse_text(text: str):
    from pixs.kernel.manifest import parse_manifest_text

    return parse_manifest_text(text)


def _factory(value):
    from pixs.kernel.frontend_contribution_declarations import (
        validate_frontend_contribution_declaration_v1,
    )

    return validate_frontend_contribution_declaration_v1(value)


class FixturesProvenValidTest(unittest.TestCase):
    def test_factory_accepts_canonical_contribution(self) -> None:
        contrib = _valid_contribution()
        snapshot = _factory(contrib)
        self.assertEqual(snapshot.type, "ROUTE")
        self.assertEqual(snapshot.id, "acme.crm.contacts")
        self.assertEqual(snapshot.entry, "frontend/routes/contacts")
        self.assertEqual(snapshot.version, "1.0.0")
        self.assertEqual(snapshot.requires, ())
        self.assertEqual(snapshot.scope, "TENANT_SCOPED")

    def test_manifest_fixtures_accepted_empty_and_ordered(self) -> None:
        first = _valid_contribution(id_text="acme.crm.first")
        second = _valid_contribution(
            type_text="PAGE",
            id_text="acme.crm.second",
            entry_text="frontend/pages/second",
            version_text="1.2.3-beta+build.1",
            requires=["acme.shared >=1.0.0 <2.0.0"],
            scope_text="AUTHENTICATED",
        )
        manifest = _base_manifest(contributions=[first, second])
        # Prouve la base avant tout rejet : factory directe sur chaque entrée.
        for item in manifest["frontend"]["contributions"]:
            _factory(item)
        parsed = _parse(manifest)
        self.assertIsNotNone(parsed.frontend)
        assert parsed.frontend is not None
        self.assertEqual(parsed.frontend.schema_version, "1")
        self.assertEqual(len(parsed.frontend.contributions), 2)


class ContainerTest(unittest.TestCase):
    def test_empty_facet_recognized_without_activation(self) -> None:
        parsed = _parse(_base_manifest(contributions=[]))
        assert parsed.frontend is not None
        self.assertEqual(parsed.frontend.schema_version, "1")
        self.assertEqual(parsed.frontend.contributions, ())
        self.assertEqual(parsed.schema_version, "1")
        self.assertEqual(parsed.type, "MODULE")

    def test_text_api_empty_facet(self) -> None:
        text = (
            'schema_version = "1"\n'
            'id = "demo"\n'
            'type = "MODULE"\n'
            'version = "1.0.0"\n'
            '[frontend]\n'
            'schema_version = "1"\n'
            'contributions = []\n'
        )
        parsed = _parse_text(text)
        assert parsed.frontend is not None
        self.assertEqual(parsed.frontend.contributions, ())

    def test_missing_key_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        data = _base_manifest()
        del data["frontend"]["contributions"]
        with self.assertRaises(ManifestValidationError) as ctx:
            _parse(data)
        self.assertTrue(any("frontend" in d for d in ctx.exception.diagnostics))

    def test_extra_key_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        data = _base_manifest()
        data["frontend"]["extra"] = "1"
        with self.assertRaises(ManifestValidationError):
            _parse(data)

    def test_facet_version_other_than_string_1_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for bad in ["2", "", "1.0", 1, None, True]:
            with self.subTest(bad=bad):
                data = _base_manifest()
                data["frontend"]["schema_version"] = bad
                with self.assertRaises(ManifestValidationError):
                    _parse(data)

    def test_contributions_not_list_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for bad in [{}, "x", None, {"a": 1}]:
            with self.subTest(bad=bad):
                data = _base_manifest()
                data["frontend"]["contributions"] = bad
                with self.assertRaises(ManifestValidationError):
                    _parse(data)

    def test_contributions_tuple_strict_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        data = _base_manifest()
        data["frontend"]["contributions"] = ()
        with self.assertRaises(ManifestValidationError):
            _parse(data)


class AttachmentTest(unittest.TestCase):
    def test_historical_manifests_without_facet_unchanged_all_six_types(self) -> None:
        for comp_type in (
            "KERNEL",
            "MODULE",
            "SUBMODULE",
            "PROVIDER",
            "EXTENSION",
            "THEME",
        ):
            with self.subTest(comp_type=comp_type):
                data = _base_manifest(comp_type=comp_type, with_frontend=False)
                parsed = _parse(data)
                self.assertIsNone(parsed.frontend)
                self.assertEqual(parsed.type, comp_type)

    def test_absent_is_none_and_valid(self) -> None:
        parsed = _parse(_base_manifest(with_frontend=False))
        self.assertIsNone(parsed.frontend)

    def test_present_none_distinct_from_absent(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        data = _base_manifest(with_frontend=False)
        data["frontend"] = None
        with self.assertRaises(ManifestValidationError) as ctx:
            _parse(data)
        self.assertTrue(
            any(d.startswith("frontend :") for d in ctx.exception.diagnostics)
        )

    def test_module_and_submodule_empty_or_ordered(self) -> None:
        for comp_type in ("MODULE", "SUBMODULE"):
            with self.subTest(comp_type=comp_type):
                empty = _parse(
                    _base_manifest(comp_type=comp_type, contributions=[])
                )
                assert empty.frontend is not None
                self.assertEqual(empty.frontend.contributions, ())
                ordered = _parse(
                    _base_manifest(
                        comp_type=comp_type,
                        contributions=[
                            _valid_contribution(id_text="acme.crm.a"),
                            _valid_contribution(id_text="acme.crm.b"),
                        ],
                    )
                )
                assert ordered.frontend is not None
                self.assertEqual(
                    [c.id for c in ordered.frontend.contributions],
                    ["acme.crm.a", "acme.crm.b"],
                )

    def test_other_types_with_facet_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for comp_type in ("KERNEL", "PROVIDER", "EXTENSION", "THEME"):
            with self.subTest(comp_type=comp_type):
                with self.assertRaises(ManifestValidationError):
                    _parse(_base_manifest(comp_type=comp_type, contributions=[]))

    def test_component_schema_and_type_exact_profile(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        data = _base_manifest()
        data["schema_version"] = "2"
        with self.assertRaises(ManifestValidationError):
            _parse(data)
        data2 = _base_manifest()
        data2["type"] = "module"
        with self.assertRaises(ManifestValidationError):
            _parse(data2)

    def test_non_mapping_top_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for bad in [None, [], "x", 42]:
            with self.subTest(bad=bad):
                with self.assertRaises(ManifestValidationError):
                    _parse(bad)


class ContributionFieldsTest(unittest.TestCase):
    def test_each_missing_field_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for field in ("type", "id", "entry", "version", "requires", "scope"):
            with self.subTest(field=field):
                contrib = _valid_contribution()
                del contrib[field]
                with self.assertRaises(ManifestValidationError):
                    _parse(_base_manifest(contributions=[contrib]))

    def test_extra_field_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        contrib = _valid_contribution()
        contrib["extra"] = "x"
        with self.assertRaises(ManifestValidationError):
            _parse(_base_manifest(contributions=[contrib]))

    def test_all_scopes_accepted_unknown_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for scope in (
            "PUBLIC",
            "AUTHENTICATED",
            "TENANT_SCOPED",
            "PLATFORM_SCOPED",
        ):
            with self.subTest(scope=scope):
                parsed = _parse(
                    _base_manifest(
                        contributions=[_valid_contribution(scope_text=scope)]
                    )
                )
                assert parsed.frontend is not None
                self.assertEqual(parsed.frontend.contributions[0].scope, scope)
        with self.assertRaises(ManifestValidationError):
            _parse(
                _base_manifest(
                    contributions=[_valid_contribution(scope_text="UNKNOWN")]
                )
            )

    def test_type_id_entry_version_requires_strict(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        cases = [
            dict(type_text="UNKNOWN"),
            dict(id_text="single"),
            dict(id_text="acme.crm.bad id"),
            dict(entry_text="/absolute/path"),
            dict(entry_text="frontend//double"),
            dict(entry_text=""),
            dict(version_text="^1.0.0"),
            dict(version_text="1.0"),
            dict(version_text=""),
            dict(requires=["acme.shared ^1.0.0"]),
            dict(requires=["acme.shared *"]),
            dict(requires=["a || b"]),
            dict(requires=[""]),
            dict(requires="acme.shared >=1.0.0"),
            dict(requires=[42]),
        ]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ManifestValidationError):
                    _parse(
                        _base_manifest(
                            contributions=[_valid_contribution(**kwargs)]
                        )
                    )


class PreservationTest(unittest.TestCase):
    def test_texts_order_multiplicity_preserved(self) -> None:
        first = _valid_contribution(
            id_text="ACME.crm-2.contacts_1",
            version_text="1.2.3-beta+build.1",
            requires=["acme.shared >=1.0.0 <2.0.0", "acme.shared >=1.0.0 <2.0.0"],
        )
        second = _valid_contribution(id_text="acme.crm.second")
        parsed = _parse(_base_manifest(contributions=[first, second]))
        assert parsed.frontend is not None
        items = list(parsed.frontend.contributions)
        self.assertEqual(items[0].id, "ACME.crm-2.contacts_1")
        self.assertEqual(items[0].version, "1.2.3-beta+build.1")
        self.assertEqual(
            items[0].requires,
            ("acme.shared >=1.0.0 <2.0.0", "acme.shared >=1.0.0 <2.0.0"),
        )
        self.assertEqual([c.id for c in items], ["ACME.crm-2.contacts_1", "acme.crm.second"])
        self.assertIs(type(items[0].requires), tuple)

    def test_source_mutation_does_not_alter_snapshot(self) -> None:
        contrib = _valid_contribution(requires=["acme.shared >=1.0.0"])
        manifest = _base_manifest(contributions=[contrib])
        parsed = _parse(manifest)
        assert parsed.frontend is not None
        contrib["id"] = "acme.crm.mutated"
        manifest["frontend"]["contributions"].append(_valid_contribution())
        manifest["frontend"]["contributions"][0]["requires"].append("acme.x >=9.0.0")
        snapshot = parsed.frontend.contributions[0]
        self.assertEqual(snapshot.id, "acme.crm.contacts")
        self.assertEqual(snapshot.requires, ("acme.shared >=1.0.0",))

    def test_frozen_and_tuple_snapshots(self) -> None:
        parsed = _parse(
            _base_manifest(contributions=[_valid_contribution()])
        )
        assert parsed.frontend is not None
        self.assertIs(type(parsed.frontend.contributions), tuple)
        with self.assertRaises(FrozenInstanceError):
            parsed.frontend.schema_version = "2"
        with self.assertRaises(FrozenInstanceError):
            parsed.frontend = None
        with self.assertRaises(FrozenInstanceError):
            parsed.frontend.contributions[0].id = "x"

    def test_no_activation_or_copy(self) -> None:
        contrib = _valid_contribution()
        expected = _factory(dict(contrib))
        parsed = _parse(_base_manifest(contributions=[contrib]))
        assert parsed.frontend is not None
        actual = parsed.frontend.contributions[0]
        self.assertEqual(actual, expected)
        self.assertIs(type(actual.requires), tuple)


class StrictBuiltinsTest(unittest.TestCase):
    def test_frontend_wrong_builtin_types_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        for bad in [None, [], "frontend", 42, True]:
            with self.subTest(bad=bad):
                data = _base_manifest(with_frontend=False)
                data["frontend"] = bad
                with self.assertRaises(ManifestValidationError):
                    _parse(data)

    def test_builtin_string_1_exact_and_subclass_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        class EvilStr(str):
            pass

        data = _base_manifest()
        data["frontend"]["schema_version"] = EvilStr("1")
        with self.assertRaises(ManifestValidationError):
            _parse(data)
        data2 = _base_manifest()
        data2["schema_version"] = EvilStr("1")
        data2["frontend"] = {
            "schema_version": "1",
            "contributions": [],
        }
        with self.assertRaises(ManifestValidationError):
            _parse(data2)

    def test_unknown_keys_and_list_subclass_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        class EvilList(list):
            pass

        data = _base_manifest()
        data["frontend"]["unknown"] = []
        with self.assertRaises(ManifestValidationError):
            _parse(data)
        data2 = _base_manifest()
        data2["frontend"]["contributions"] = EvilList([])
        with self.assertRaises(ManifestValidationError):
            _parse(data2)

    def test_component_type_subclass_refused(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        class EvilStr(str):
            pass

        data = _base_manifest(contributions=[])
        data["type"] = EvilStr("MODULE")
        with self.assertRaises(ManifestValidationError):
            _parse(data)


class HostileHooksTest(unittest.TestCase):
    SENTINEL = "SENTINEL_XYZ_789"

    def test_dict_subclass_hook_not_called_and_no_echo(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        sentinel = self.SENTINEL
        calls: list[str] = []

        class EvilDict(dict):
            def __getitem__(self, key):
                calls.append(str(key))
                return sentinel

            def __contains__(self, key):
                return dict.__contains__(self, key)

        evil = EvilDict(
            {
                "type": "ROUTE",
                "id": "acme.crm.contacts",
                "entry": "frontend/routes/contacts",
                "version": "1.0.0",
                "requires": [],
                "scope": "TENANT_SCOPED",
                self.SENTINEL: sentinel,
            }
        )
        data = _base_manifest(contributions=[evil])
        with self.assertRaises(ManifestValidationError) as ctx:
            _parse(data)
        joined = ";".join(ctx.exception.diagnostics)
        self.assertEqual(calls, [])
        self.assertNotIn(sentinel, joined)
        self.assertNotIn(self.SENTINEL, joined)

    def test_list_and_str_subclasses_rejected_without_echo(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        class EvilList(list):
            pass

        class EvilStr(str):
            pass

        sentinel = self.SENTINEL
        contrib = _valid_contribution()
        contrib["requires"] = EvilList([sentinel])
        with self.assertRaises(ManifestValidationError) as ctx:
            _parse(_base_manifest(contributions=[contrib]))
        self.assertNotIn(sentinel, ";".join(ctx.exception.diagnostics))
        contrib2 = _valid_contribution()
        contrib2["type"] = EvilStr("ROUTE")
        with self.assertRaises(ManifestValidationError) as ctx2:
            _parse(_base_manifest(contributions=[contrib2]))
        self.assertNotIn(sentinel, ";".join(ctx2.exception.diagnostics))

    def test_mapping_arbitrary_rejected(self) -> None:
        from collections.abc import Mapping

        from pixs.kernel.manifest import ManifestValidationError

        class EvilMapping(Mapping):
            def __getitem__(self, key):
                return self.SENTINEL

            def __iter__(self):
                return iter(
                    ["type", "id", "entry", "version", "requires", "scope"]
                )

            def __len__(self):
                return 6

        evil: object = EvilMapping()
        with self.assertRaises(ManifestValidationError):
            _parse(_base_manifest(contributions=[evil]))


class CommonGuardsTest(unittest.TestCase):
    def test_eval_entry_lexically_valid_but_manifest_refused_without_raw(self) -> None:
        from pixs.kernel.manifest import ManifestValidationError

        entry = "frontend/eval(1)"
        # Base prouvée valide côté factory : le garde commun reste manifest.
        _factory(_valid_contribution(entry_text=entry))
        contrib = _valid_contribution(entry_text=entry)
        with self.assertRaises(ManifestValidationError) as ctx:
            _parse(_base_manifest(contributions=[contrib]))
        joined = ";".join(ctx.exception.diagnostics)
        self.assertIn("frontend", joined)
        self.assertNotIn("eval(1)", joined)
        self.assertNotIn(entry, joined)


class UnexpectedFactoryErrorTest(unittest.TestCase):
    def test_runtime_error_propagates(self) -> None:
        data = _base_manifest(contributions=[_valid_contribution()])
        with patch(
            "pixs.kernel.frontend_contribution_declarations"
            ".validate_frontend_contribution_declaration_v1",
            side_effect=RuntimeError("boom"),
        ):
            with self.assertRaises(RuntimeError):
                _parse(data)


class AdditionalBoundaryTest(unittest.TestCase):
    def test_legacy_outer_mapping_remains_supported(self):
        from types import MappingProxyType
        for owner in ("KERNEL", "MODULE", "SUBMODULE", "PROVIDER", "EXTENSION", "THEME"):
            with self.subTest(owner=owner):
                self.assertIsNone(_parse(MappingProxyType(_base_manifest(comp_type=owner, with_frontend=False))).frontend)

    def test_duplicate_contributions_preserved_with_texts(self):
        item = _valid_contribution(requires=["audit >=1.0.0", "audit >=1.0.0"])
        actual = _parse(_base_manifest(contributions=[item, item])).frontend
        self.assertEqual(len(actual.contributions), 2)
        self.assertEqual(actual.contributions[0], actual.contributions[1])
        self.assertEqual(actual.contributions[0].requires, ("audit >=1.0.0", "audit >=1.0.0"))

    def test_unknown_builtin_key_never_echoed(self):
        from pixs.kernel.manifest import ManifestValidationError
        for at_facet in (True, False):
            base = _base_manifest(contributions=[_valid_contribution()])
            _parse(base)
            target = base["frontend"] if at_facet else base["frontend"]["contributions"][0]
            target["SENTINEL_UNKNOWN_KEY_789"] = "SENTINEL_VALUE_789"
            with self.assertRaises(ManifestValidationError) as ctx:
                _parse(base)
            self.assertNotIn("SENTINEL", str(ctx.exception))

    def test_hostile_frontend_containers_rejected_before_hooks(self):
        from collections.abc import Mapping
        from pixs.kernel.manifest import ManifestValidationError
        calls = []
        def hook(*args, **kwargs):
            calls.append("hook")
            raise AssertionError("raw frontend hook executed")
        class DictHook(dict):
            __iter__ = __getitem__ = items = keys = values = __contains__ = hook
        class ListHook(list):
            __iter__ = __getitem__ = __len__ = hook
        class MappingHook(Mapping):
            __iter__ = __getitem__ = __len__ = hook
        class StringHook(str):
            __eq__ = __str__ = __repr__ = hook
        bad_facets = [
            DictHook(schema_version="1", contributions=[]),
            MappingHook(),
            {"schema_version": StringHook("1"), "contributions": []},
            {"schema_version": "1", "contributions": ListHook()},
        ]
        for bad in bad_facets:
            base = _base_manifest()
            base["frontend"] = bad
            with self.assertRaises(ManifestValidationError):
                _parse(base)
            self.assertEqual(calls, [])

    def test_raw_requires_non_list_refused(self):
        from pixs.kernel.manifest import ManifestValidationError
        for bad in ((), "audit >=1.0.0", None, {}, 1):
            item = _valid_contribution()
            _factory(item)
            item["requires"] = bad
            with self.assertRaises(ManifestValidationError):
                _parse(_base_manifest(contributions=[item]))

    def test_text_api_ordered_contributions(self):
        text = 'schema_version="1"\nid="demo"\ntype="SUBMODULE"\nversion="1.0.0"\n[frontend]\nschema_version="1"\n'
        item = '\n[[frontend.contributions]]\ntype="ROUTE"\nid="ACME.contacts"\nentry="frontend/contacts"\nversion="1.2.3-beta+build.1"\nrequires=["audit >=1.0.0", "audit >=1.0.0"]\nscope="TENANT_SCOPED"\n'
        actual = _parse_text(text + item + item).frontend
        self.assertEqual(len(actual.contributions), 2)
        self.assertEqual(actual.contributions[0], actual.contributions[1])
        self.assertEqual(actual.contributions[0].id, "ACME.contacts")
        self.assertEqual(actual.contributions[0].version, "1.2.3-beta+build.1")
        self.assertEqual(actual.contributions[0].requires, ("audit >=1.0.0", "audit >=1.0.0"))


if __name__ == "__main__":
    unittest.main()
