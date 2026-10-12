"""Ports Bulk synthétiques : composition serveur, refus fermés et snapshots."""

import builtins
import unittest
from dataclasses import FrozenInstanceError
from unittest import mock

import pixs.backend.bulk_trusted_ports as ports
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_runtime_contracts import (
    _CODES, _FIELDS, _Hostile, _ForeignDict, _ForeignTuple,
    _ForeignStr, _mapping, _authority, _context,
)


_RESPONSE_UNSET = object()


class _Authority:
    """Provider synthétique ; ne réalise aucune autorisation de production."""

    def __init__(self, response=_RESPONSE_UNSET, fail=False):
        self.calls = []
        self.response = _authority() if response is _RESPONSE_UNSET else response
        self.fail = fail

    def check(self, context, action, operation, resource):
        self.calls.append((context, action, operation, resource))
        if self.fail:
            raise _ProviderFailure()
        return self.response


class _ProviderFailure(Exception):
    def __str__(self):
        raise AssertionError("provider exception must not be formatted")

    def __repr__(self):
        raise AssertionError("provider exception must not be represented")


class _Resolver:
    """Mapping synthétique indépendant du dictionnaire déclaré par le caller."""

    def __init__(self):
        self.calls = []
        self.fail = False
        self.response = None

    def resolve(self, reference, version, owner):
        self.calls.append((reference, version, owner))
        if self.fail:
            raise _ProviderFailure()
        if self.response is not None:
            return self.response
        value = _mapping()
        value.update(mapping_reference=reference, mapping_version=version, owner_reference=owner)
        return value


class _Governance:
    def resolve(self, *args, **kwargs):
        raise AssertionError("governance must not be executed during composition")


class _Owner:
    def validate(self, *args, **kwargs):
        raise AssertionError("owner validation must not be executed during composition")

    def execute(self, *args, **kwargs):
        raise AssertionError("owner mutation must not be executed")

    def canonical_bytes(self, *args, **kwargs):
        raise AssertionError("owner serializer must not be executed during composition")


class _Projection:
    def filter_authorized(self, *args, **kwargs):
        raise AssertionError("projection must not be executed")

    def acquire_consistency(self, *args, **kwargs):
        raise AssertionError("consistency must not be acquired")

    def iterate_projection(self, *args, **kwargs):
        raise AssertionError("projection must not be read")


class _Audit:
    def append_minimized(self, *args, **kwargs):
        raise AssertionError("no fictitious audit append")


def _kwargs(authority=None, resolver=None):
    return {
        "authority_adapter": _Authority() if authority is None else authority,
        "mapping_resolver": _Resolver() if resolver is None else resolver,
        "mapping_descriptors": (_mapping(),),
        "owner_declarations": (("owner-test", "1.0.0", _CODES, _FIELDS),),
        "governance_adapter": None, "owner_command_adapter": None,
        "owner_projection_adapter": None, "audit_adapter": None,
    }


def _compose(authority=None, resolver=None):
    kwargs = _kwargs(authority, resolver)
    return ports.compose_bulk_trusted_ports(**kwargs), kwargs


class BulkTrustedPortsTests(unittest.TestCase):
    def assert_refused_result(self, result):
        snapshot, diagnostics = result
        self.assertIsNone(snapshot)
        self.assertIs(type(diagnostics), list)
        self.assertTrue(diagnostics)
        for diagnostic in diagnostics:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertNotIn("LEAK-MARKER", str(diagnostic))

    def test_exports_and_no_provider_mutation_during_composition(self):
        self.assertEqual(set(ports.__all__), {
            "declare_bulk_mapping_descriptor", "compose_bulk_trusted_ports",
            "validate_governance_contract", "validate_owner_command_contract",
            "validate_owner_projection_contract", "validate_audit_contract",
        })
        authority, resolver = _Authority(), _Resolver()
        bundle, _ = _compose(authority, resolver)
        self.assertIsNotNone(bundle)
        self.assertEqual(authority.calls, [])
        self.assertEqual(resolver.calls, [])

    def test_authority_uses_actual_server_context_and_four_arguments(self):
        authority = _Authority()
        resolver = _Resolver()
        bundle, _ = _compose(authority, resolver)
        server_context = object()
        snapshot, diagnostics = bundle.check_authority(
            server_context=server_context, action="ADMIT",
            operation_reference="operation-test", resource_reference="resource-test",
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(snapshot.as_values(), _authority())
        self.assertEqual(authority.calls, [
            (server_context, "ADMIT", "operation-test", "resource-test"),
        ])
        self.assertEqual(resolver.calls, [])

    def test_each_canonical_authority_action_and_nullable_resource(self):
        for action in ("ADMIT", "EXECUTE", "CANCEL", "READ_RESULT"):
            bundle, kwargs = _compose()
            snapshot, diagnostics = bundle.check_authority(
                server_context=object(), action=action,
                operation_reference="operation-test", resource_reference=None,
            )
            self.assertEqual(diagnostics, [])
            self.assertEqual(snapshot.as_values()["decision"], "ALLOW")
            self.assertEqual(len(kwargs["authority_adapter"].calls), 1)

    def test_deny_and_unavailable_never_expose_context_or_fallback(self):
        for decision in ("DENY", "UNAVAILABLE"):
            authority = _Authority({"decision": decision, "resolved_context": None})
            resolver = _Resolver()
            bundle, _ = _compose(authority, resolver)
            self.assert_refused_result(bundle.check_authority(
                server_context=object(), action="EXECUTE",
                operation_reference="operation-test", resource_reference=None,
            ))
            self.assertEqual(len(authority.calls), 1)
            self.assertEqual(resolver.calls, [])

    def test_malformed_authority_response_never_allows(self):
        for response in (
            None, {}, _Hostile(), _ForeignDict(_authority()),
            {"decision": "ALLOW", "resolved_context": None},
            {"decision": "ALLOW", "resolved_context": {**_context(), "tenant_id": None}},
            {"decision": "DENY", "resolved_context": _context()},
            {"decision": "UNKNOWN", "resolved_context": None},
        ):
            authority = _Authority(response)
            resolver = _Resolver()
            bundle, _ = _compose(authority, resolver)
            self.assert_refused_result(bundle.check_authority(
                server_context=object(), action="ADMIT",
                operation_reference="operation-test", resource_reference=None,
            ))
            self.assertEqual(resolver.calls, [])

    def test_provider_exception_unavailable_without_formatting(self):
        authority, resolver = _Authority(fail=True), _Resolver()
        bundle, _ = _compose(authority, resolver)
        self.assert_refused_result(bundle.check_authority(
            server_context=object(), action="EXECUTE",
            operation_reference="operation-test", resource_reference=None,
        ))
        self.assertEqual(resolver.calls, [])

    def test_foreign_authority_arguments_refused_before_provider(self):
        for updates in (
            {"action": _Hostile()}, {"action": _ForeignStr("ADMIT")},
            {"action": "UNKNOWN"}, {"operation_reference": _Hostile()},
            {"operation_reference": ""}, {"resource_reference": _Hostile()},
            {"resource_reference": "LEAK-MARKER\x00"},
        ):
            authority = _Authority()
            bundle, _ = _compose(authority)
            kwargs = {
                "server_context": object(), "action": "ADMIT",
                "operation_reference": "operation-test", "resource_reference": None,
            }
            kwargs.update(updates)
            self.assert_refused_result(bundle.check_authority(**kwargs))
            self.assertEqual(authority.calls, [])

    def test_mapping_resolver_called_with_canonical_three_arguments(self):
        resolver = _Resolver()
        bundle, _ = _compose(resolver=resolver)
        mapping = _mapping()
        snapshot, diagnostics = bundle.resolve_mapping(
            mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(snapshot.as_values(), mapping)
        self.assertEqual(resolver.calls, [
            (mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"]),
        ])

    def test_mapping_reference_arguments_guarded_before_provider(self):
        for args in (
            (_Hostile(), "1.0.0", "owner-test"),
            ("mapping-test", _Hostile(), "owner-test"),
            ("mapping-test", "1.0.0", _Hostile()),
            ("mapping-test", "not-semver", "owner-test"),
        ):
            resolver = _Resolver()
            bundle, _ = _compose(resolver=resolver)
            self.assert_refused_result(bundle.resolve_mapping(*args))
            self.assertEqual(resolver.calls, [])

    def test_unknown_mapping_never_imports_or_calls_resolver(self):
        resolver = _Resolver()
        bundle, _ = _compose(resolver=resolver)
        with mock.patch.object(builtins, "__import__", side_effect=AssertionError("dynamic import")):
            result = bundle.resolve_mapping("LEAK-MARKER.module", "1.0.0", "LEAK-MARKER.owner")
        self.assert_refused_result(result)
        self.assertEqual(resolver.calls, [])

    def test_mapping_provider_failure_never_returns_cached_value(self):
        resolver = _Resolver()
        bundle, _ = _compose(resolver=resolver)
        mapping = _mapping()
        good, diagnostics = bundle.resolve_mapping(
            mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
        )
        self.assertEqual(diagnostics, [])
        resolver.fail = True
        self.assert_refused_result(bundle.resolve_mapping(
            mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
        ))
        self.assertEqual(good.as_values(), mapping)
        self.assertEqual(len(resolver.calls), 2)

    def test_mapping_changed_or_foreign_provider_response_refused(self):
        for response in (
            _Hostile(), _ForeignDict(_mapping()),
            {**_mapping(), "mapping_reference": "LEAK-MARKER.changed"},
            {**_mapping(), "required_source_fields": ()},
            {**_mapping(), "field_bindings": (("source_name", "count"), ("source_count", "name"))},
        ):
            resolver = _Resolver()
            resolver.response = response
            bundle, _ = _compose(resolver=resolver)
            mapping = _mapping()
            self.assert_refused_result(bundle.resolve_mapping(
                mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
            ))
            self.assertEqual(len(resolver.calls), 1)

    def test_declared_snapshot_owned_immutable_and_no_caller_alias(self):
        declared = _mapping()
        resolver = _Resolver()
        kwargs = _kwargs(resolver=resolver)
        kwargs["mapping_descriptors"] = (declared,)
        bundle = ports.compose_bulk_trusted_ports(**kwargs)
        declared["mapping_reference"] = "caller-changed"
        original = _mapping()
        snapshot, diagnostics = bundle.resolve_mapping(
            original["mapping_reference"], original["mapping_version"], original["owner_reference"],
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(snapshot.as_values(), original)
        with self.assertRaises((FrozenInstanceError, AttributeError)):
            snapshot.mapping_reference = "changed"
        rendered = snapshot.as_values()
        rendered["owner_reference"] = "changed"
        self.assertEqual(snapshot.as_values(), original)

    def test_mapping_namespace_is_per_canonical_identity(self):
        first = _mapping()
        second = {**_mapping(), "owner_reference": "owner-other"}
        kwargs = _kwargs()
        kwargs["mapping_descriptors"] = (first, second)
        kwargs["owner_declarations"] = (
            ("owner-test", "1.0.0", _CODES, _FIELDS),
            ("owner-other", "2.0.0", _CODES, _FIELDS),
        )
        bundle = ports.compose_bulk_trusted_ports(**kwargs)
        for mapping in (first, second):
            snapshot, diagnostics = bundle.resolve_mapping(
                mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
            )
            self.assertEqual(diagnostics, [])
            self.assertEqual(snapshot.as_values(), mapping)

    def test_owner_schema_fields_required_before_composition(self):
        kwargs = _kwargs()
        kwargs["owner_declarations"] = (("owner-test", "1.0.0", _CODES, ("name",)),)
        with self.assertRaises(ValueError):
            ports.compose_bulk_trusted_ports(**kwargs)
        self.assertEqual(kwargs["authority_adapter"].calls, [])
        self.assertEqual(kwargs["mapping_resolver"].calls, [])

    def test_foreign_declarations_and_divergent_duplicate_refused(self):
        for mappings, owners in (
            (_ForeignTuple((_mapping(),)), _kwargs()["owner_declarations"]),
            ((_ForeignDict(_mapping()),), _kwargs()["owner_declarations"]),
            ((_mapping(),), (_Hostile(),)),
            ((_mapping(),), (("owner-test", _Hostile(), _CODES, _FIELDS),)),
            ((_mapping(),), (
                ("owner-test", "1.0.0", _CODES, _FIELDS),
                ("owner-test", "2.0.0", _CODES, _FIELDS),
            )),
        ):
            kwargs = _kwargs()
            kwargs.update(mapping_descriptors=mappings, owner_declarations=owners)
            with self.assertRaises(ValueError):
                ports.compose_bulk_trusted_ports(**kwargs)
            self.assertEqual(kwargs["authority_adapter"].calls, [])
            self.assertEqual(kwargs["mapping_resolver"].calls, [])

    def test_required_components_missing_refused_without_fallback(self):
        for field in ("authority_adapter", "mapping_resolver"):
            kwargs = _kwargs()
            kwargs[field] = None
            with self.assertRaises(ValueError):
                ports.compose_bulk_trusted_ports(**kwargs)

    def test_component_properties_and_getattr_never_executed(self):
        calls = []
        class PropertyAuthority:
            @property
            def check(self):
                calls.append("property")
                raise AssertionError("dynamic property")
        class DynamicAuthority:
            def __getattr__(self, name):
                calls.append("getattr")
                raise AssertionError("dynamic getattr")
        for authority in (PropertyAuthority(), DynamicAuthority()):
            kwargs = _kwargs()
            kwargs["authority_adapter"] = authority
            with self.assertRaises(ValueError):
                ports.compose_bulk_trusted_ports(**kwargs)
        self.assertEqual(calls, [])

    def test_optional_ports_structural_only_and_never_executed(self):
        kwargs = _kwargs()
        kwargs.update(
            governance_adapter=_Governance(), owner_command_adapter=_Owner(),
            owner_projection_adapter=_Projection(), audit_adapter=_Audit(),
        )
        bundle = ports.compose_bulk_trusted_ports(**kwargs)
        self.assertIsNotNone(bundle)
        for function, component in (
            (ports.validate_governance_contract, kwargs["governance_adapter"]),
            (ports.validate_owner_command_contract, kwargs["owner_command_adapter"]),
            (ports.validate_owner_projection_contract, kwargs["owner_projection_adapter"]),
            (ports.validate_audit_contract, kwargs["audit_adapter"]),
        ):
            self.assertEqual(function(component), [])
            self.assertTrue(function(None))

    def test_mapping_declaration_is_value_only_not_global_registration(self):
        original = _mapping()
        snapshot = ports.declare_bulk_mapping_descriptor(original)
        self.assertEqual(snapshot.as_values(), original)
        original["owner_reference"] = "caller-changed"
        self.assertEqual(snapshot.as_values(), _mapping())
        with self.assertRaises(ValueError):
            ports.declare_bulk_mapping_descriptor(_Hostile())


    def test_empty_instance_cannot_reuse_another_instance_declarations(self):
        original = _mapping()
        ports.declare_bulk_mapping_descriptor(original)
        first, _ = _compose()
        snapshot, diagnostics = first.resolve_mapping(
            original["mapping_reference"], original["mapping_version"], original["owner_reference"],
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(snapshot.as_values(), original)
        kwargs = _kwargs()
        kwargs.update(mapping_descriptors=(), owner_declarations=())
        empty = ports.compose_bulk_trusted_ports(**kwargs)
        self.assert_refused_result(empty.resolve_mapping(
            original["mapping_reference"], original["mapping_version"], original["owner_reference"],
        ))
        self.assertEqual(kwargs["mapping_resolver"].calls, [])


    def test_all_metadata_types_checked_before_any_semver_parsing(self):
        import pixs.backend.bulk_runtime_contracts as contracts
        for bad_mapping, owners in (
            ({**_mapping(), "owner_reference": _Hostile()}, _kwargs()["owner_declarations"]),
            (_mapping(), (("owner-test", _Hostile(), _CODES, _FIELDS),)),
            (_mapping(), (("owner-test", "1.0.0", (_Hostile(),), _FIELDS),)),
        ):
            kwargs = _kwargs()
            kwargs.update(mapping_descriptors=(_mapping(), bad_mapping), owner_declarations=owners)
            with mock.patch.object(contracts, "parse_version", side_effect=AssertionError("parse before metadata types")):
                with self.assertRaises(ValueError):
                    ports.compose_bulk_trusted_ports(**kwargs)

    def test_bound_method_capture_never_uses_dynamic_getattribute_at_call(self):
        getters = []
        class StaticAuthority(_Authority):
            def __getattribute__(self, name):
                if name == "check":
                    getters.append(name)
                    raise AssertionError("dynamic getter executed")
                return object.__getattribute__(self, name)
        authority = StaticAuthority()
        bundle, _ = _compose(authority=authority)
        snapshot, diagnostics = bundle.check_authority(
            server_context=object(), action="ADMIT",
            operation_reference="operation-test", resource_reference=None,
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(snapshot.as_values(), _authority())
        self.assertEqual(getters, [])
        self.assertEqual(len(authority.calls), 1)


if __name__ == "__main__":
    unittest.main()
