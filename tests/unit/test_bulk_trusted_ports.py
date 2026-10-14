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


class _Publisher:
    def publish_declared_event(self, *args, **kwargs):
        raise AssertionError("publisher must not be executed")


class _Download:
    def authorize_then_issue_temporary_reference(self, *args, **kwargs):
        raise AssertionError("le téléchargement ne doit pas être exécuté")


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
            "validate_publisher_contract", "validate_download_contract",
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


    def test_publisher_contract_accepts_python_methods_without_invocation(self):
        self.assertEqual(ports.validate_publisher_contract(_Publisher()), [])
        calls = []
        class Attached:
            pass
        def publish_declared_event(*args, **kwargs):
            calls.append("executed")
            raise AssertionError("publisher must not be executed")
        attached = Attached()
        attached.publish_declared_event = publish_declared_event
        self.assertEqual(ports.validate_publisher_contract(attached), [])
        attached.publish_declared_event = publish_declared_event.__get__(attached, Attached)
        self.assertEqual(ports.validate_publisher_contract(attached), [])
        self.assertEqual(calls, [])

    def test_publisher_contract_refuses_foreign_methods_without_echo(self):
        class ForeignCallable:
            def __call__(self, *args, **kwargs):
                raise AssertionError("foreign callable executed")
            def __str__(self):
                raise AssertionError("foreign value formatted")
            def __repr__(self):
                raise AssertionError("foreign value represented")
        class ForeignPublisher:
            publish_declared_event = ForeignCallable()
        class BuiltinPublisher:
            publish_declared_event = len
        class TextPublisher:
            publish_declared_event = "LEAK-MARKER"
        for component in (None, object(), _Audit(), _Publisher,
                          ForeignPublisher(), BuiltinPublisher(), TextPublisher()):
            diagnostics = ports.validate_publisher_contract(component)
            self.assertIs(type(diagnostics), list)
            self.assertEqual(len(diagnostics), 1)
            for diagnostic in diagnostics:
                self.assertIs(type(diagnostic), Diagnostic)
                self.assertEqual(diagnostic.step, VALIDATE)
                self.assertTrue(diagnostic.element.startswith("bulk_publisher_port."))
                self.assertNotIn("LEAK-MARKER", str(diagnostic))

    def test_publisher_contract_never_executes_dynamic_lookup_or_descriptor(self):
        calls = []
        class PropertyPublisher:
            @property
            def publish_declared_event(self):
                calls.append("property")
                raise AssertionError("dynamic property")
        class DynamicPublisher:
            def __getattr__(self, name):
                calls.append("getattr")
                raise AssertionError("dynamic getattr")
        class Descriptor:
            def __get__(self, instance, owner):
                calls.append("descriptor")
                raise AssertionError("dynamic descriptor")
        class DescriptorPublisher:
            publish_declared_event = Descriptor()
        for component in (PropertyPublisher(), DynamicPublisher(), DescriptorPublisher()):
            self.assertTrue(ports.validate_publisher_contract(component))
        self.assertEqual(calls, [])

    def test_publisher_contract_preserves_existing_decorator_capture_policy(self):
        class StaticPublisher:
            @staticmethod
            def publish_declared_event(*args, **kwargs):
                raise AssertionError("static publisher executed")
        class ClassPublisher:
            @classmethod
            def publish_declared_event(cls, *args, **kwargs):
                raise AssertionError("class publisher executed")
        for component in (StaticPublisher(), ClassPublisher()):
            self.assertTrue(ports.validate_publisher_contract(component))

    def test_download_contract_accepts_python_methods_without_invocation(self):
        self.assertEqual(ports.validate_download_contract(_Download()), [])
        calls = []
        class Attached:
            pass
        def authorize_then_issue_temporary_reference(*args, **kwargs):
            calls.append("executed")
            raise AssertionError("le téléchargement ne doit pas être exécuté")
        attached = Attached()
        attached.authorize_then_issue_temporary_reference = authorize_then_issue_temporary_reference
        self.assertEqual(ports.validate_download_contract(attached), [])
        attached.authorize_then_issue_temporary_reference = authorize_then_issue_temporary_reference.__get__(attached, Attached)
        self.assertEqual(ports.validate_download_contract(attached), [])
        self.assertEqual(calls, [])

    def test_download_contract_refuses_foreign_methods_without_echo(self):
        class ForeignCallable:
            def __call__(self, *args, **kwargs):
                raise AssertionError("appel étranger exécuté")
            def __str__(self):
                raise AssertionError("valeur étrangère formatée")
            def __repr__(self):
                raise AssertionError("valeur étrangère représentée")
        class ForeignDownload:
            authorize_then_issue_temporary_reference = ForeignCallable()
        class BuiltinDownload:
            authorize_then_issue_temporary_reference = len
        class TextDownload:
            authorize_then_issue_temporary_reference = "LEAK-MARKER"
        for component in (None, object(), _Audit(), _Download,
                          ForeignDownload(), BuiltinDownload(), TextDownload()):
            diagnostics = ports.validate_download_contract(component)
            self.assertIs(type(diagnostics), list)
            self.assertEqual(len(diagnostics), 1)
            for diagnostic in diagnostics:
                self.assertIs(type(diagnostic), Diagnostic)
                self.assertEqual(diagnostic.step, VALIDATE)
                self.assertTrue(diagnostic.element.startswith("bulk_download_port."))
                self.assertNotIn("LEAK-MARKER", str(diagnostic))

    def test_download_contract_never_executes_dynamic_lookup_or_descriptor(self):
        calls = []
        class PropertyDownload:
            @property
            def authorize_then_issue_temporary_reference(self):
                calls.append("property")
                raise AssertionError("propriété dynamique exécutée")
        class DynamicDownload:
            def __getattr__(self, name):
                calls.append("getattr")
                raise AssertionError("accès dynamique exécuté")
        class Descriptor:
            def __get__(self, instance, owner):
                calls.append("descriptor")
                raise AssertionError("descripteur dynamique exécuté")
        class DescriptorDownload:
            authorize_then_issue_temporary_reference = Descriptor()
        for component in (PropertyDownload(), DynamicDownload(), DescriptorDownload()):
            self.assertTrue(ports.validate_download_contract(component))
        self.assertEqual(calls, [])

    def test_download_contract_preserves_existing_decorator_capture_policy(self):
        class StaticDownload:
            @staticmethod
            def authorize_then_issue_temporary_reference(*args, **kwargs):
                raise AssertionError("méthode statique de téléchargement exécutée")
        class ClassDownload:
            @classmethod
            def authorize_then_issue_temporary_reference(cls, *args, **kwargs):
                raise AssertionError("méthode de classe de téléchargement exécutée")
        for component in (StaticDownload(), ClassDownload()):
            self.assertTrue(ports.validate_download_contract(component))


class _GovernanceResolve3:
    def __init__(self, response=None, fail=False):
        self.calls = []
        self.response = response
        self.fail = fail

    def resolve(self, context, contract, references):
        self.calls.append((context, contract, references))
        if self.fail:
            raise _ProviderFailure()
        return self.response


def _valid_profile():
    return ports.DataGovernanceProfile(
        profile_version="1.0.0",
        data_asset_id="asset-test",
        owner_component="owner-test",
        source_of_truth="truth-test",
        data_classes=frozenset({"classe-test"}),
        confidentiality=ports.ConfidentialityLevel.INTERNAL,
        personal_data=ports.PersonalDataLevel.NONE,
        purpose_refs=frozenset({"finalite-test"}),
        retention_policy="retention-test",
        deletion_policy="deletion-test",
        residency_constraints=frozenset({"residence-test"}),
        authorized_consumers=frozenset({"conso-test"}),
        processor_refs=frozenset({"proc-test"}),
        export_policy="export-test",
        lineage="lignee-test",
    )


def _valid_limits():
    from unit.test_bulk_execution_values import _valid_policy

    return _valid_policy()


def _resolved_response(policy_ref="policy-test", policy_ver="1.0.0", obligations=("obligation-test",)):
    context = _context()
    limits = _valid_limits()
    return {
        "resolution_version": "1.0.0",
        "decision": "RESOLVED",
        "resolved_context": dict(context),
        "policy": {
            "policy_reference": policy_ref,
            "policy_version": policy_ver,
            "limits": limits,
        },
        "profile": _valid_profile(),
        "obligations": tuple(obligations) if obligations is not None else None,
    }


def _compose_gov(governance):
    kwargs = _kwargs()
    kwargs["governance_adapter"] = governance
    return ports.compose_bulk_trusted_ports(**kwargs), kwargs


class GovernanceResolutionTests(unittest.TestCase):
    def _authority_snapshot(self):
        from pixs.backend.bulk_runtime_contracts import _build_authority_assessment_snapshot

        return _build_authority_assessment_snapshot(_authority())

    def test_resolved_valid_single_call_no_alias(self):
        gov = _GovernanceResolve3(response=None)
        composed, _ = _compose_gov(gov)
        snapshot = self._authority_snapshot()
        contract = _mapping()
        references = ("policy-test", "1.0.0")
        gov.response = _resolved_response()
        result, diags = composed.resolve_governance(
            server_context=object(),
            authority_snapshot=snapshot,
            governance_contract=dict(contract),
            governance_references=tuple(references),
        )
        self.assertEqual(diags, [])
        self.assertIsNotNone(result)
        self.assertEqual(len(gov.calls), 1)
        ctx, cont, refs = gov.calls[0]
        self.assertEqual(len(gov.calls[0]), 3)
        self.assertEqual(refs, references)
        before = result.as_values()
        gov.response["resolved_context"]["subject_id"] = "mute"
        gov.response["policy"]["limits"]["max_rows"] = 1
        gov.response["obligations"] = ("mute",)
        object.__setattr__(gov.response["profile"], "data_asset_id", "mute")
        after = result.as_values()
        self.assertEqual(before, after)
        self.assertEqual(after["resolved_context"]["subject_id"], "actor-test")
        self.assertEqual(after["obligations"], ("obligation-test",))

    def test_empty_tuple_accepted_none_refused(self):
        gov = _GovernanceResolve3()
        composed, _ = _compose_gov(gov)
        snapshot = self._authority_snapshot()
        gov.response = _resolved_response(obligations=())
        result, diags = composed.resolve_governance(
            server_context=object(),
            authority_snapshot=snapshot,
            governance_contract=_mapping(),
            governance_references=("policy-test", "1.0.0"),
        )
        self.assertEqual(diags, [])
        self.assertIsNotNone(result)
        self.assertEqual(result.obligations, ())
        gov2 = _GovernanceResolve3(response=_resolved_response(obligations=None))
        composed2, _ = _compose_gov(gov2)
        result2, diags2 = composed2.resolve_governance(
            server_context=object(),
            authority_snapshot=snapshot,
            governance_contract=_mapping(),
            governance_references=("policy-test", "1.0.0"),
        )
        self.assertIsNone(result2)
        self.assertTrue(diags2)

    def test_deny_unavailable_closed_exception_never_formatted(self):
        for decision in ("DENY", "UNAVAILABLE"):
            gov = _GovernanceResolve3(
                response={
                    "resolution_version": "1.0.0",
                    "decision": decision,
                    "resolved_context": None,
                    "policy": None,
                    "profile": None,
                    "obligations": None,
                }
            )
            composed, _ = _compose_gov(gov)
            result, diags = composed.resolve_governance(
                server_context=object(),
                authority_snapshot=self._authority_snapshot(),
                governance_contract=_mapping(),
                governance_references=("policy-test", "1.0.0"),
            )
            self.assertIsNone(result)
            self.assertTrue(diags)
            self.assertEqual(len(gov.calls), 1)
        gov_fail = _GovernanceResolve3(fail=True)
        composed_fail, _ = _compose_gov(gov_fail)
        result_fail, diags_fail = composed_fail.resolve_governance(
            server_context=object(),
            authority_snapshot=self._authority_snapshot(),
            governance_contract=_mapping(),
            governance_references=("policy-test", "1.0.0"),
        )
        self.assertIsNone(result_fail)
        self.assertTrue(diags_fail)

    def test_divergent_context_each_field(self):
        base = _context()
        for field in ("subject_id", "tenant_id", "perimeter_reference", "context_reference"):
            divergent = dict(base)
            divergent[field] = "autre-test"
            gov = _GovernanceResolve3(
                response=_resolved_response(),
            )
            gov.response["resolved_context"] = divergent
            composed, _ = _compose_gov(gov)
            result, diags = composed.resolve_governance(
                server_context=object(),
                authority_snapshot=self._authority_snapshot(),
                governance_contract=_mapping(),
                governance_references=("policy-test", "1.0.0"),
            )
            self.assertIsNone(result)
            self.assertTrue(diags)

    def test_limits_closed_types(self):
        valid = _resolved_response()
        cases = []
        bad_unknown = _resolved_response()
        bad_unknown["policy"] = dict(bad_unknown["policy"])
        bad_unknown["policy"]["limits"] = dict(bad_unknown["policy"]["limits"])
        bad_unknown["policy"]["limits"]["cle-inconnue"] = 1
        cases.append(bad_unknown)
        bad_missing = _resolved_response()
        bad_missing["policy"] = dict(bad_missing["policy"])
        limited = dict(bad_missing["policy"]["limits"])
        limited.pop("max_rows")
        bad_missing["policy"]["limits"] = limited
        cases.append(bad_missing)
        bad_bool = _resolved_response()
        bad_bool["policy"] = dict(bad_bool["policy"])
        bad_bool["policy"]["limits"] = dict(bad_bool["policy"]["limits"])
        bad_bool["policy"]["limits"]["max_rows"] = True
        cases.append(bad_bool)
        bad_tuple_lists = _resolved_response()
        bad_tuple_lists["policy"] = dict(bad_tuple_lists["policy"])
        bad_tuple_lists["policy"]["limits"] = dict(bad_tuple_lists["policy"]["limits"])
        bad_tuple_lists["policy"]["limits"]["retry_delays_seconds"] = (1, 2)
        cases.append(bad_tuple_lists)
        bad_list_on_int = _resolved_response()
        bad_list_on_int["policy"] = dict(bad_list_on_int["policy"])
        bad_list_on_int["policy"]["limits"] = dict(bad_list_on_int["policy"]["limits"])
        bad_list_on_int["policy"]["limits"]["max_rows"] = [1]
        cases.append(bad_list_on_int)
        bad_int_on_list = _resolved_response()
        bad_int_on_list["policy"] = dict(bad_int_on_list["policy"])
        bad_int_on_list["policy"]["limits"] = dict(bad_int_on_list["policy"]["limits"])
        bad_int_on_list["policy"]["limits"]["retry_delays_seconds"] = 1
        cases.append(bad_int_on_list)
        for hostile in cases:
            gov = _GovernanceResolve3(response=hostile)
            composed, _ = _compose_gov(gov)
            result, diags = composed.resolve_governance(
                server_context=object(),
                authority_snapshot=self._authority_snapshot(),
                governance_contract=_mapping(),
                governance_references=("policy-test", "1.0.0"),
            )
            self.assertIsNone(result)
            self.assertTrue(diags)

    def test_hostile_response_no_parse_before_type_reject(self):
        import pixs.backend.bulk_trusted_ports as trusted

        def build_cases():
            valid = _resolved_response()
            cases = []
            foreign_profile = dict(valid)
            foreign_profile["profile"] = _Hostile()
            cases.append(foreign_profile)
            hostile_obligations = dict(valid)
            hostile_obligations["obligations"] = (_Hostile(),)
            cases.append(hostile_obligations)
            hostile_str_field = dict(valid)
            bad_profile = _valid_profile()
            object.__setattr__(bad_profile, "data_asset_id", _Hostile())
            hostile_str_field["profile"] = bad_profile
            cases.append(hostile_str_field)
            hostile_collection = dict(valid)
            good_profile = _valid_profile()
            object.__setattr__(
                good_profile, "data_classes", frozenset({"classe-test", _ForeignStr("hostile-test")})
            )
            hostile_collection["profile"] = good_profile
            cases.append(hostile_collection)
            unknown_key = dict(valid)
            unknown_policy = dict(unknown_key["policy"])
            unknown_limits = dict(unknown_policy["limits"])
            unknown_limits["cle-inconnue"] = 1
            unknown_policy["limits"] = unknown_limits
            unknown_key["policy"] = unknown_policy
            cases.append(unknown_key)
            missing_key = dict(valid)
            missing_policy = dict(missing_key["policy"])
            missing_limits = dict(missing_policy["limits"])
            missing_limits.pop("max_rows")
            missing_policy["limits"] = missing_limits
            missing_key["policy"] = missing_policy
            cases.append(missing_key)
            bool_on_int = dict(valid)
            bool_policy = dict(bool_on_int["policy"])
            bool_limits = dict(bool_policy["limits"])
            bool_limits["max_rows"] = True
            bool_policy["limits"] = bool_limits
            bool_on_int["policy"] = bool_policy
            cases.append(bool_on_int)
            tuple_for_list = dict(valid)
            tuple_policy = dict(tuple_for_list["policy"])
            tuple_limits = dict(tuple_policy["limits"])
            tuple_limits["retry_delays_seconds"] = (1, 2)
            tuple_policy["limits"] = tuple_limits
            tuple_for_list["policy"] = tuple_policy
            cases.append(tuple_for_list)
            return cases

        for hostile_response in build_cases():
            gov = _GovernanceResolve3()
            composed, _ = _compose_gov(gov)
            snapshot = self._authority_snapshot()
            p_policy = mock.patch.object(
                trusted, "validate_bulk_policy_values", side_effect=AssertionError("validation sémantique prématurée")
            )
            p_profile = mock.patch.object(
                trusted, "validate_data_governance_profile", side_effect=AssertionError("validation sémantique prématurée")
            )
            p_context = mock.patch.object(
                trusted, "validate_server_context_refs_values", side_effect=AssertionError("validation sémantique prématurée")
            )
            p_semver = mock.patch.object(
                trusted, "_is_complete_semver", side_effect=AssertionError("analyse prématurée")
            )
            started = []
            started_mocks = []

            def arming_resolve(context, contract, references, _patchers=(p_policy, p_profile, p_context, p_semver), _started=started, _gov=gov, _resp=hostile_response):
                for patcher in _patchers:
                    started_mocks.append(patcher.start())
                    _started.append(patcher)
                _gov.calls.append((context, contract, references))
                return _resp

            gov.resolve = arming_resolve
            try:
                result, diags = composed.resolve_governance(
                    server_context=object(),
                    authority_snapshot=snapshot,
                    governance_contract=_mapping(),
                    governance_references=("policy-test", "1.0.0"),
                )
            finally:
                for patcher in reversed(started):
                    patcher.stop()
            self.assertIsNone(result)
            self.assertTrue(diags)
            self.assertEqual(len(gov.calls), 1)
            self.assertEqual(len(started_mocks), 4)
            for spy in started_mocks:
                spy.assert_not_called()

    def test_delay_lists_captured_without_alias(self):
        gov = _GovernanceResolve3()
        composed, _ = _compose_gov(gov)
        snapshot = self._authority_snapshot()
        gov.response = _resolved_response()
        result, diags = composed.resolve_governance(
            server_context=object(),
            authority_snapshot=snapshot,
            governance_contract=_mapping(),
            governance_references=("policy-test", "1.0.0"),
        )
        self.assertEqual(diags, [])
        self.assertIsNotNone(result)
        before = result.as_values()
        gov.response["policy"]["limits"]["retry_delays_seconds"].append(999)
        gov.response["policy"]["limits"]["publish_retry_delays_seconds"].append(999)
        after = result.as_values()
        self.assertEqual(before, after)
        self.assertEqual(len(gov.calls), 1)

    def test_authority_hostile_no_port_call(self):
        from pixs.backend.bulk_runtime_contracts import (
            _AuthorityAssessmentSnapshot,
            _ServerContextRefsSnapshot,
        )

        gov = _GovernanceResolve3(response=_resolved_response())
        composed, _ = _compose_gov(gov)
        hostile_snapshot = _AuthorityAssessmentSnapshot(decision=_Hostile(), resolved_context=None)
        result, diags = composed.resolve_governance(
            server_context=object(),
            authority_snapshot=hostile_snapshot,
            governance_contract=_mapping(),
            governance_references=("policy-test", "1.0.0"),
        )
        self.assertIsNone(result)
        self.assertTrue(diags)
        self.assertEqual(gov.calls, [])
        hostile_context = _ServerContextRefsSnapshot(
            subject_id=_Hostile(),
            tenant_id="tenant-test",
            perimeter_reference="perimeter-test",
            context_reference="context-test",
        )
        hostile_snapshot2 = _AuthorityAssessmentSnapshot(decision="ALLOW", resolved_context=hostile_context)
        result2, diags2 = composed.resolve_governance(
            server_context=object(),
            authority_snapshot=hostile_snapshot2,
            governance_contract=_mapping(),
            governance_references=("policy-test", "1.0.0"),
        )
        self.assertIsNone(result2)
        self.assertTrue(diags2)
        self.assertEqual(gov.calls, [])

    def test_foreign_contract_references_no_port(self):
        gov = _GovernanceResolve3(response=_resolved_response())
        composed, _ = _compose_gov(gov)
        snapshot = self._authority_snapshot()
        for contract, references in [
            (_ForeignDict({"a": "b"}), ("policy-test", "1.0.0")),
            ({"inconnue": "x"}, ("policy-test", "1.0.0")),
            (_mapping(), ("policy-test",)),
            (_mapping(), _ForeignTuple(("policy-test", "1.0.0"))),
        ]:
            result, diags = composed.resolve_governance(
                server_context=object(),
                authority_snapshot=snapshot,
                governance_contract=contract,
                governance_references=references,
            )
            self.assertIsNone(result)
            self.assertTrue(diags)
        self.assertEqual(gov.calls, [])


if __name__ == "__main__":
    unittest.main()
