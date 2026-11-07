"""Unites 2.3 valeurs/schema/politique : ferme, deterministe, sans persistance."""
from __future__ import annotations

import dataclasses
import datetime
import json
import unittest

from pixs.backend.c09_authorization_adapter import C09Identity
from pixs.backend.c09_contracts import C09EventBindingV1, C09PolicyV1, C09RoleDeclarationV1
from pixs.backend.c09_event_values import (
    C09DeliveryPolicyV1,
    C09EventEnvelopeV1,
    C09EventSchemaBindingV1,
    c09_canonical_payload_bytes,
    c09_delivery_fingerprint,
    c09_envelope_canonical_bytes,
    c09_envelope_content_sha256,
    c09_envelope_wire_bytes,
    c09_payload_content_sha256,
    export_c09_event_schema,
    validate_c09_delivery_catalog,
    validate_c09_delivery_policy,
    validate_c09_event_envelope,
    validate_c09_event_schema_binding,
)
from pixs.backend.c09_registry import C09RegistryV1
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.event_contract import DomainEventContract, IntegrationEventContract


def _base_policy(**over):
    base = dict(policy_reference="pol-c09-unit", policy_version="1.0.0", lease_seconds=30,
                renewal_seconds=5, max_attempts=3, retry_delays_seconds=(5, 10),
                polling_interval_ms=50, polling_max_batch=2, max_concurrency=2,
                max_units_per_poll=2, drain_seconds=5, attempt_timeout_seconds=10,
                job_timeout_seconds=60, process_count=1, cpu_millicores=100,
                max_connections=5, memory_mb=128,
                effective_from=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc))
    base.update(over)
    return C09PolicyV1(**base)


def _delivery(**over):
    base = dict(base_policy=_base_policy(), delivery_policy_reference="del-c09-unit",
                delivery_policy_version="1.0.0", max_event_bytes=8192, max_payload_refs=8,
                max_pending_events=100, max_pending_deliveries=60)
    base.update(over)
    return C09DeliveryPolicyV1(**base)


def _contract(kind="DOMAIN"):
    if kind == "DOMAIN":
        return DomainEventContract("evt-c09", "1.0.0", "producer-c09", "schema-c09", "order-c09")
    return IntegrationEventContract("evt-c09", "1.0.0", "producer-c09", "schema-c09", "order-c09")


def _registry(kind="DOMAIN", with_consumer=True):
    from pixs.backend.c09_contracts import C09ConsumerDeclarationV1
    binding = C09EventBindingV1("owner-c09", "entry-c09", _contract(kind), "perim-c09", None)
    role = C09RoleDeclarationV1("worker", "h-c09", "1.0.0", "comp-c09")
    consumers = ()
    if with_consumer:
        consumers = (C09ConsumerDeclarationV1("cons-c09", "entry-c09", "2.0.0", "comp-c09", "1.0.0"),)
    return C09RegistryV1((role,), (binding,), consumers)


def _binding(**over):
    base = dict(entry_reference="entry-c09", owner_reference="owner-c09",
                tenant_context_reference=None, perimeter_reference="perim-c09",
                kind="DOMAIN", event_type="evt-c09", event_version="1.0.0",
                producer_reference="producer-c09", schema_reference="schema-c09",
                order_scope_reference="order-c09")
    base.update(over)
    return C09EventSchemaBindingV1(**base)


def _identity():
    return C09Identity("actor-c09", "perim-c09", "req-c09", "1.0.0", "res-c09",
                       "act-c09", ScopeContext(ScopeType.PLATFORM, None, None), "corr-c09")


def _envelope(**over):
    refs = ("ref-a", "ref-b")
    base = dict(event_id="evt-id-1", kind="DOMAIN", identity=_identity(),
                entry_reference="entry-c09", event_type="evt-c09", event_version="1.0.0",
                producer_reference="producer-c09", schema_reference="schema-c09",
                order_scope_reference="order-c09", causation_id=None,
                occurred_at=datetime.datetime(2026, 5, 1, tzinfo=datetime.timezone.utc),
                sequence_index=1, payload_refs=refs,
                request_content_sha256="0" * 64, content_sha256="0" * 64)
    base.update(over)
    env = C09EventEnvelopeV1(**base)
    fixed = c09_envelope_content_sha256(env)
    if env.content_sha256 != fixed:
        env = dataclasses.replace(env, content_sha256=fixed)
    return env


class Hostile:
    def __eq__(self, other):
        raise AssertionError("eq appele")
    def __hash__(self):
        raise AssertionError("hash appele")
    def __iter__(self):
        raise AssertionError("iter appele")
    def __str__(self):
        raise AssertionError("str appele")


class SubStr(str):
    def __eq__(self, other):
        raise AssertionError("eq sous-classe appele")
    def __hash__(self):
        raise AssertionError("hash sous-classe appele")
    def __iter__(self):
        raise AssertionError("iter sous-classe appele")
    def __str__(self):
        raise AssertionError("str sous-classe appele")


class SubDateTime(datetime.datetime):
    pass


class DeliveryTests(unittest.TestCase):
    def test_accept(self):
        self.assertEqual(validate_c09_delivery_policy(_delivery()), [])

    def test_sans_defaut(self):
        with self.assertRaises(TypeError):
            C09DeliveryPolicyV1(_base_policy())

    def test_budgets_independants(self):
        self.assertEqual(validate_c09_delivery_policy(_delivery(max_pending_deliveries=100, max_pending_events=10)), [])

    def test_bool_etranger_bornes(self):
        self.assertTrue(validate_c09_delivery_policy(_delivery(max_event_bytes=True)))
        self.assertTrue(validate_c09_delivery_policy(_delivery(max_event_bytes=0)))
        self.assertTrue(validate_c09_delivery_policy(_delivery(max_event_bytes=2**31)))
        self.assertEqual(validate_c09_delivery_policy(_delivery(max_event_bytes=2**31 - 1)), [])

    def test_base_utf8_nul_surrogate(self):
        for bad in ("a\x00b", "a\ud800", SubStr("ref"), Hostile()):
            with self.subTest(type=type(bad).__name__):
                self.assertTrue(validate_c09_delivery_policy(_delivery(delivery_policy_reference=bad)))
                self.assertTrue(validate_c09_delivery_policy(_delivery(base_policy=_base_policy(policy_reference=bad))))
        self.assertEqual(validate_c09_delivery_policy(_delivery(delivery_policy_reference=" espace é ")), [])

    def test_fingerprint_couvre_chaque_champ(self):
        first = c09_delivery_fingerprint(_delivery())
        base_cases = {
            "policy_reference": "pol-other", "policy_version": "1.0.1",
            "lease_seconds": 31, "renewal_seconds": 6, "retry_delays_seconds": (6, 10),
            "polling_interval_ms": 51, "polling_max_batch": 1, "max_concurrency": 3,
            "max_units_per_poll": 3, "drain_seconds": 6, "attempt_timeout_seconds": 11,
            "job_timeout_seconds": 61, "process_count": 2, "cpu_millicores": 101,
            "max_connections": 6, "memory_mb": 129,
            "effective_from": datetime.datetime(2026, 2, 1, tzinfo=datetime.timezone.utc),
        }
        for name, value in base_cases.items():
            with self.subTest(base_field=name):
                changed = dataclasses.replace(_base_policy(), **{name: value})
                self.assertNotEqual(first, c09_delivery_fingerprint(_delivery(base_policy=changed)))
        # max_attempts et nombre de délais changent ensemble pour rester valides.
        changed = _base_policy(max_attempts=4, retry_delays_seconds=(5, 10, 15))
        self.assertNotEqual(first, c09_delivery_fingerprint(_delivery(base_policy=changed)))
        for name, value in {
            "delivery_policy_reference": "other", "delivery_policy_version": "1.0.1",
            "max_event_bytes": 8193, "max_payload_refs": 9,
            "max_pending_events": 101, "max_pending_deliveries": 61,
        }.items():
            with self.subTest(delivery_field=name):
                self.assertNotEqual(first, c09_delivery_fingerprint(_delivery(**{name: value})))


class BindingTests(unittest.TestCase):
    def test_accept_lie_registre(self):
        self.assertEqual(validate_c09_event_schema_binding(_binding(), _registry()), [])

    def test_tous_champs_compares(self):
        values = {
            "entry_reference": "autre", "owner_reference": "autre",
            "tenant_context_reference": "autre", "perimeter_reference": "autre",
            "kind": "INTEGRATION", "event_type": "autre", "event_version": "1.0.1",
            "producer_reference": "autre", "schema_reference": "autre",
            "order_scope_reference": "autre",
        }
        for name, value in values.items():
            with self.subTest(field=name):
                self.assertTrue(validate_c09_event_schema_binding(_binding(**{name: value}), _registry()))
        self.assertEqual(validate_c09_event_schema_binding(
            _binding(kind="INTEGRATION"), _registry(kind="INTEGRATION")), [])

    def test_consumer_absent_divergent(self):
        self.assertTrue(validate_c09_delivery_catalog(_registry(with_consumer=False), (_binding(),), _delivery()))
        bad_reg = _registry()
        from pixs.backend.c09_contracts import C09ConsumerDeclarationV1
        bad_consumer = C09ConsumerDeclarationV1("", "entry-c09", "2.0.0", "comp-c09", "1.0.0")
        bad = C09RegistryV1(bad_reg.roles, bad_reg.bindings, (bad_consumer,))
        self.assertTrue(validate_c09_delivery_catalog(bad, (_binding(),), _delivery()))

    def test_refs_opaques_espaces_preservees(self):
        binding = _binding(entry_reference="entrée avec espaces", producer_reference="prod é")
        reg_binding = dataclasses.replace(_binding(), entry_reference="entrée avec espaces", producer_reference="prod é")
        from pixs.backend.c09_contracts import C09EventBindingV1, C09RoleDeclarationV1
        from pixs.backend.c09_registry import C09RegistryV1 as Reg
        contract = DomainEventContract("evt-c09", "1.0.0", "prod é", "schema-c09", "order-c09")
        rb = C09EventBindingV1("owner-c09", "entrée avec espaces", contract, "perim-c09", None)
        role = C09RoleDeclarationV1("worker", "h-c09", "1.0.0", "comp-c09")
        from pixs.backend.c09_contracts import C09ConsumerDeclarationV1
        cons = (C09ConsumerDeclarationV1("cons-c09", "entrée avec espaces", "2.0.0", "comp-c09", "1.0.0"),)
        reg = Reg((role,), (rb,), cons)
        self.assertEqual(validate_c09_event_schema_binding(binding, reg), [])

    def test_hostile_non_appele(self):
        for field in dataclasses.fields(C09EventSchemaBindingV1):
            for bad in (Hostile(), SubStr("valeur")):
                with self.subTest(field=field.name, type=type(bad).__name__):
                    self.assertTrue(validate_c09_event_schema_binding(
                        dataclasses.replace(_binding(), **{field.name: bad}), _registry()))

    def test_catalogue_et_version_consommateur(self):
        reg = _registry()
        self.assertEqual(validate_c09_delivery_catalog(reg, (_binding(),), _delivery()), [])
        # Version du consommateur 2.0.0, contrat événement 1.0.0 : distinction conservée.
        bad = dataclasses.replace(reg.consumers[0], event_contract_version="2.1.0")
        self.assertTrue(validate_c09_delivery_catalog(
            dataclasses.replace(reg, consumers=(bad,)), (_binding(),), _delivery()))
        self.assertTrue(validate_c09_delivery_catalog(reg, (_binding(), _binding()), _delivery()))
        with self.assertRaises(ValueError):
            export_c09_event_schema(_binding(schema_reference="inconnu"), _delivery(), reg)


class EnvelopeTests(unittest.TestCase):
    def test_accept(self):
        self.assertEqual(validate_c09_event_envelope(_envelope(), _binding(), _delivery()), [])

    def test_tzinfo_hostile_et_sousclasses(self):
        class BadTz(datetime.tzinfo):
            def utcoffset(self, other):
                raise AssertionError("tz appele")
        class BadDateTime(datetime.datetime):
            @property
            def tzinfo(self):
                raise AssertionError("tzinfo appele")
        valid = _envelope()
        for value in (
            datetime.datetime(2026, 5, 1),
            datetime.datetime(2026, 5, 1, tzinfo=BadTz()),
            BadDateTime(2026, 5, 1, tzinfo=datetime.timezone.utc),
        ):
            self.assertTrue(validate_c09_event_envelope(
                dataclasses.replace(valid, occurred_at=value), _binding(), _delivery()))
        self.assertTrue(validate_c09_event_envelope(
            dataclasses.replace(valid, event_id=SubStr("evt-id-1")), _binding(), _delivery()))

    def test_contexte_etranger_nested_corrompu(self):
        bad_ctx = object.__new__(ScopeContext)
        object.__setattr__(bad_ctx, "scope_type", "PLATEFORME")
        object.__setattr__(bad_ctx, "tenant_id", None)
        object.__setattr__(bad_ctx, "scope_id", None)
        bad_ident = dataclasses.replace(_identity(), context=bad_ctx)
        bad = dataclasses.replace(_envelope(), identity=bad_ident)
        self.assertTrue(validate_c09_event_envelope(bad, _binding(), _delivery()))

    def test_payload_vide_doublon_type(self):
        with self.assertRaises(ValueError):
            c09_canonical_payload_bytes(())
        with self.assertRaises(ValueError):
            c09_canonical_payload_bytes(("a", "a"))
        with self.assertRaises(ValueError):
            c09_canonical_payload_bytes(("a", 1))

    def test_ordre_preserve_empreintes_distinctes(self):
        self.assertEqual(c09_canonical_payload_bytes(("a", "b")), b'{"payload_refs":["a","b"]}')
        self.assertNotEqual(c09_payload_content_sha256(("a", "b")), c09_payload_content_sha256(("b", "a")))

    def test_mutation_champ_change_hash(self):
        valid = _envelope()
        first = c09_envelope_content_sha256(valid)
        cases = {
            "event_id": "evt-id-2", "kind": "INTEGRATION", "entry_reference": "entry-other",
            "event_type": "evt-other", "event_version": "1.0.1",
            "producer_reference": "producer-other", "schema_reference": "schema-other",
            "order_scope_reference": "order-other", "causation_id": "cause-1",
            "occurred_at": valid.occurred_at + datetime.timedelta(microseconds=1),
            "sequence_index": 2, "payload_refs": ("ref-b", "ref-a"),
            "request_content_sha256": "1" * 64,
        }
        for name, value in cases.items():
            with self.subTest(envelope_field=name):
                self.assertNotEqual(first, c09_envelope_content_sha256(
                    dataclasses.replace(valid, **{name: value})))
        identities = {
            "actor_reference": "actor-other", "perimeter_reference": "perim-other",
            "request_reference": "req-other", "request_version": "1.0.1",
            "resource_id": "res-other", "action_id": "act-other",
            "context": ScopeContext(ScopeType.TENANT, "tenant-a"),
            "correlation_id": "corr-other",
        }
        for name, value in identities.items():
            with self.subTest(identity_field=name):
                changed = dataclasses.replace(valid.identity, **{name: value})
                self.assertNotEqual(first, c09_envelope_content_sha256(
                    dataclasses.replace(valid, identity=changed)))
        # Le seul champ exclu est celui qui porte l'empreinte elle-même.
        self.assertEqual(first, c09_envelope_content_sha256(
            dataclasses.replace(valid, content_sha256="f" * 64)))

    def test_hash_falsifie_refuse(self):
        valid = _envelope()
        bad = dataclasses.replace(valid, content_sha256="0" * 64)
        self.assertTrue(validate_c09_event_envelope(bad, _binding(), _delivery()))

    def test_perimetre_schema_divergents(self):
        self.assertTrue(validate_c09_event_envelope(_envelope(), _binding(perimeter_reference="autre"), _delivery()))
        self.assertTrue(validate_c09_event_envelope(_envelope(), _binding(schema_reference="autre"), _delivery()))

    def test_maxbytes_metadata_et_maxrefs(self):
        valid = _envelope()
        wire = c09_envelope_wire_bytes(valid)
        self.assertEqual(validate_c09_event_envelope(
            valid, _binding(), _delivery(max_event_bytes=len(wire))), [])
        self.assertTrue(validate_c09_event_envelope(
            valid, _binding(), _delivery(max_event_bytes=len(wire) - 1)))
        self.assertTrue(validate_c09_event_envelope(
            valid, _binding(), _delivery(max_payload_refs=1)))
        # Métadonnées volumineuses avec le même petit payload.
        identity = dataclasses.replace(valid.identity, actor_reference="a" * 4096)
        large = _envelope(identity=identity)
        self.assertTrue(validate_c09_event_envelope(
            large, _binding(), _delivery(max_event_bytes=2048)))

    def test_i64_et_bool(self):
        self.assertEqual(validate_c09_event_envelope(
            _envelope(sequence_index=2**63 - 1), _binding(), _delivery()), [])
        valid = _envelope()
        for bad in (2**63, 0, -1, True, Hostile()):
            self.assertTrue(validate_c09_event_envelope(
                dataclasses.replace(valid, sequence_index=bad), _binding(), _delivery()))

    def test_export_closed_deterministe(self):
        first = export_c09_event_schema(_binding(), _delivery(), _registry())
        second = export_c09_event_schema(_binding(), _delivery(), _registry())
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertNotIn("$id", first)
        self.assertEqual(first["schema_reference"], "schema-c09")
        self.assertTrue(first["payload"]["additionalProperties"] is False)
        self.assertEqual(first["payload"]["properties"]["payload_refs"]["maxItems"], 8)

    def test_immutable(self):
        valid = _envelope()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            valid.event_id = "autre"

    def test_hostiles_avant_hash_egalite_serialisation(self):
        valid = _envelope()
        for field in dataclasses.fields(C09EventEnvelopeV1):
            with self.subTest(field=field.name):
                self.assertTrue(validate_c09_event_envelope(
                    dataclasses.replace(valid, **{field.name: Hostile()}), _binding(), _delivery()))
        for refs in (("a", Hostile()), (SubStr("a"),), ("a\x00b",), ("a\ud800",), [], ()):
            with self.assertRaises(ValueError):
                c09_canonical_payload_bytes(refs)
            self.assertTrue(validate_c09_event_envelope(
                dataclasses.replace(valid, payload_refs=refs), _binding(), _delivery()))
        self.assertTrue(validate_c09_event_envelope(
            valid, _binding(event_type=Hostile()), _delivery()))
        self.assertTrue(validate_c09_event_envelope(valid, _binding(), Hostile()))

    def test_enveloppe_identite_context_utf8(self):
        valid = _envelope()
        for bad in ("a\x00b", "a\ud800", SubStr("actor"), Hostile()):
            identity = dataclasses.replace(valid.identity, actor_reference=bad)
            self.assertTrue(validate_c09_event_envelope(
                dataclasses.replace(valid, identity=identity), _binding(), _delivery()))
        for scope_type, tenant, scope in (
            (Hostile(), None, None),
            (ScopeType.TENANT, Hostile(), None),
            (ScopeType.TENANT, "a\x00b", None),
            (ScopeType.TENANT, "a\ud800", None),
        ):
            context = object.__new__(ScopeContext)
            object.__setattr__(context, "scope_type", scope_type)
            object.__setattr__(context, "tenant_id", tenant)
            object.__setattr__(context, "scope_id", scope)
            identity = dataclasses.replace(valid.identity, context=context)
            self.assertTrue(validate_c09_event_envelope(
                dataclasses.replace(valid, identity=identity), _binding(), _delivery()))

    def test_schema_export_copies_et_pas_de_mutation(self):
        one = export_c09_event_schema(_binding(), _delivery(), _registry())
        two = export_c09_event_schema(_binding(), _delivery(), _registry())
        self.assertEqual(json.dumps(one, sort_keys=True), json.dumps(two, sort_keys=True))
        one["payload"]["properties"]["payload_refs"]["maxItems"] = 999
        self.assertEqual(two["payload"]["properties"]["payload_refs"]["maxItems"], 8)
        self.assertNotIn("$id", two["payload"])

    def test_wire_et_diagnostics_statiques(self):
        valid = _envelope()
        document = json.loads(c09_envelope_wire_bytes(valid))
        self.assertEqual(document["payload"], {"payload_refs": ["ref-a", "ref-b"]})
        self.assertEqual(document["content_sha256"], valid.content_sha256)
        self.assertNotIn("content_sha256", json.loads(c09_envelope_canonical_bytes(valid)))
        marker = "contenu-prive-ne-pas-echo"
        errors = validate_c09_event_envelope(
            dataclasses.replace(valid, event_type=marker), _binding(), _delivery())
        self.assertTrue(errors)
        self.assertNotIn(marker, repr(errors))
        keys = [(d.element, d.constraint, d.message) for d in errors]
        self.assertEqual(keys, sorted(set(keys)))



class WireParserTests(unittest.TestCase):
    def setUp(self):
        from pixs.backend.c09_event_values import c09_envelope_from_document, c09_envelope_from_wire_bytes
        self.decode_document = c09_envelope_from_document
        self.decode_wire = c09_envelope_from_wire_bytes

    def test_roundtrip_domain_and_integration(self):
        for kind in ("DOMAIN", "INTEGRATION"):
            event = _envelope(kind=kind)
            wire = c09_envelope_wire_bytes(event)
            self.assertEqual(self.decode_wire(wire, _binding(kind=kind), _delivery(), _registry(kind=kind)), event)
            self.assertEqual(self.decode_document(json.loads(wire), _binding(kind=kind), _delivery(), _registry(kind=kind)), event)

    def test_closed_every_header_and_nested_mapping(self):
        document = json.loads(c09_envelope_wire_bytes(_envelope()))
        for name in document:
            altered = dict(document)
            del altered[name]
            with self.subTest(header=name), self.assertRaises(ValueError):
                self.decode_document(altered, _binding(), _delivery(), _registry())
        for name in ("context", "payload"):
            altered = dict(document)
            altered[name] = dict(document[name], foreign="x")
            with self.subTest(nested=name), self.assertRaises(ValueError):
                self.decode_document(altered, _binding(), _delivery(), _registry())
        altered = dict(document, foreign="x")
        with self.assertRaises(ValueError):
            self.decode_document(altered, _binding(), _delivery(), _registry())

    def test_duplicate_keys_and_invalid_utf8_refused(self):
        wire = c09_envelope_wire_bytes(_envelope())
        candidates = (
            b'{"event_id":"duplicate",' + wire[1:],
            wire.replace(b'"payload_refs":[', b'"payload_refs":[],"payload_refs":['),
            b"\xff", b"", b'{"context":',
        )
        for candidate in candidates:
            with self.subTest(size=len(candidate)), self.assertRaises(ValueError):
                self.decode_wire(candidate, _binding(), _delivery(), _registry())

    def test_byte_limits_and_exact_bytes(self):
        event = _envelope()
        wire = c09_envelope_wire_bytes(event)
        policy = _delivery(max_event_bytes=len(wire))
        self.assertEqual(self.decode_wire(wire, _binding(), policy, _registry()), event)
        with self.assertRaises(ValueError):
            self.decode_wire(wire, _binding(), dataclasses.replace(policy, max_event_bytes=len(wire)-1), _registry())
        for candidate in (bytearray(wire), memoryview(wire), wire.decode(), Hostile()):
            with self.assertRaises(ValueError):
                self.decode_wire(candidate, _binding(), policy, _registry())

    def test_hostile_types_and_values_never_compared(self):
        document = json.loads(c09_envelope_wire_bytes(_envelope()))
        for header in document:
            for value in (Hostile(), SubStr("foreign")):
                altered = dict(document)
                altered[header] = value
                with self.subTest(header=header, type=type(value).__name__), self.assertRaises(ValueError):
                    self.decode_document(altered, _binding(), _delivery(), _registry())
        for name, value in (("sequence_index", True), ("sequence_index", 2**63),
                            ("content_sha256", "0"*64), ("occurred_at", "2026-05-01T00:00:00Z")):
            altered = dict(document)
            altered[name] = value
            with self.subTest(header=name), self.assertRaises(ValueError):
                self.decode_document(altered, _binding(), _delivery(), _registry())

    def test_payload_order_unicode_and_scope_preserved(self):
        event = _envelope(payload_refs=("Référence:B", "référence:A"),
                          identity=dataclasses.replace(_identity(), actor_reference="Acteur:Équipe"))
        decoded = self.decode_wire(c09_envelope_wire_bytes(event), _binding(), _delivery(), _registry())
        self.assertEqual(decoded.payload_refs, ("Référence:B", "référence:A"))
        self.assertEqual(decoded.identity.actor_reference, "Acteur:Équipe")
        document = json.loads(c09_envelope_wire_bytes(event))
        document["context"] = {"scope_type": "TENANT", "tenant_id": None, "scope_id": None}
        with self.assertRaises(ValueError):
            self.decode_document(document, _binding(), _delivery(), _registry())

    def test_malformed_or_deep_json_refused_without_echo(self):
        candidates = (b"[" * 2000 + b"0" + b"]" * 2000,
                      b'{"sequence_index":NaN}', b'{"sequence_index":Infinity}')
        for candidate in candidates:
            with self.assertRaises(ValueError) as caught:
                self.decode_wire(candidate, _binding(), _delivery(), _registry())
            self.assertNotIn("sequence_index", str(caught.exception))

if __name__ == "__main__":
    unittest.main()
