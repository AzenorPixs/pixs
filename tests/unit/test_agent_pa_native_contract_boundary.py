"""Frontieres structurelles Agent/PA01 : aucune conversion ou autorite.

Fixtures synthetiques, sans Subject reel, provider, signature verifiee,
TPM/NV, SQL, TLS ou extension native. Ce module n'est pas un adaptateur.
Les valeurs de bornes et dates ci-dessous ne sont pas des defauts produit.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import json
import subprocess
import sys
import unittest

from pixs.agent.contracts import (
    AgentManagementInstruction, AgentManagementResult, AgentParam,
    AgentParamSpec, AgentValidationContext, AllowedCatalogEntry,
    validate_agent_instruction, validate_agent_result,
)
from pixs.core.scope import ScopeContext, ScopeType
from pixs.pa_native.postgresql_contracts import (
    AnchorSnapshot, AnchorSnapshotLimits, ContractError, NativeRequest,
    NativeResult, PayloadLimits, TechnicalPlan, decode_anchor_snapshot,
    decode_request, decode_result, encode_anchor_snapshot, encode_request,
    encode_result, plan_sha256,
)

OPERATIONS = (
    "inspect_postgresql", "prepare_postgresql", "get_postgresql_result",
)
PHASES = ("RECEIVED", "RUNNING", "SUCCEEDED", "FAILED", "IN_DOUBT", "BLOCKED")


class AgentNativeContractBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.scope = ScopeContext(ScopeType.PLATFORM)
        self.limits = PayloadLimits(8192, 64, 8)
        self.anchor_limits = AnchorSnapshotLimits(self.limits, 16, 32)
        self.plan = TechnicalPlan(
            "1.0.0", "prepare_postgresql", "1.0.0", "op", "idem", "corr",
            "plan", "revision", "inst", "pa", "projection", "confirmation",
            "policy", "preconditions", "service", "role", "database",
        )

    def request(self, operation="inspect_postgresql", target="pa"):
        parameters = {
            "inspect_postgresql": (),
            "prepare_postgresql": (
                ("plan_digest", plan_sha256(self.plan, self.limits)),
                ("plan_ref", "plan"), ("plan_version", "revision"),
            ),
            "get_postgresql_result": (("operation_ref", "subject"),),
        }
        return NativeRequest(
            "1.0.0", operation, "1.0.0", "op", "idem", "corr",
            "inst", target, "mandate", parameters[operation],
        )

    def context(self, operation="inspect_postgresql", target="pa"):
        # Acteur/scope/generation fournis par la fixture, jamais derives du DTO PA.
        return AgentValidationContext(
            "actor", self.scope, target, 7, operation, "1.0.0", "op",
            "idem", ("corr",), "2030-01-01T00:00:01Z", "mandate",
            "origin", None, 64, 2048, 8, 8, 3600,
        )

    def catalog(self):
        shapes = {
            "inspect_postgresql": (),
            "prepare_postgresql": ("plan_digest", "plan_ref", "plan_version"),
            "get_postgresql_result": ("operation_ref",),
        }
        return tuple(
            AllowedCatalogEntry(
                operation, "1.0.0",
                tuple(AgentParamSpec(name, "str", 64, None, None, True)
                      for name in shapes[operation]),
            )
            for operation in OPERATIONS
        )

    def instruction(self, request):
        # Rapprochement de donnees de test seulement : ni mapping adopte,
        # ni preuve de mandat ou binding d'autorite provenant de ce JSON.
        return AgentManagementInstruction(
            "1.0.0", request.operation_id, request.catalog_operation,
            request.catalog_version, "actor", self.scope, request.target_ref,
            7, request.mandate_ref, "2030-01-01T01:00:00Z", ("corr",), (),
            request.idempotency_key,
            tuple(AgentParam(name, "str", value, None, None)
                  for name, value in request.params),
        )

    def native_result(self, phase="SUCCEEDED", target="pa"):
        durable = phase in ("RUNNING", "SUCCEEDED", "FAILED", "IN_DOUBT")
        diagnostic = "FIXTURE_STATUS" if phase in (
            "FAILED", "IN_DOUBT", "BLOCKED",
        ) else None
        return NativeResult(
            "1.0.0", "inspect_postgresql", "1.0.0", "op", "corr",
            "inst", target, None, phase, "result" if durable else None,
            ("observation",) if phase == "SUCCEEDED" else (),
            None, None, None, diagnostic,
        )

    def agent_result(self):
        return AgentManagementResult(
            "op", "pa", 7, self.scope, "ack", ("corr",),
            "2030-01-01T00:00:00Z", "origin",
        )

    def anchor(self):
        # L'objet encode seulement des metadonnees publiques synthetiques.
        return AnchorSnapshot(
            "pixs.agent.postgresql.anchor_snapshot/v1", "1.0.0", "snap",
            "inst", "pa", "registry", "reg-gen", 0, 8, "a" * 64,
            "index", "000b" + "b" * 64, "c" * 64, "owner", "policy",
            "version", "2030-01-01T00:00:00.123456Z",
        )

    def test_three_catalog_shapes_under_explicit_synthetic_context(self):
        for operation in OPERATIONS:
            with self.subTest(operation=operation):
                request = self.request(operation)
                self.assertEqual(
                    decode_request(encode_request(request, self.limits),
                                   self.limits), request,
                )
                self.assertEqual(validate_agent_instruction(
                    self.instruction(request), self.catalog(),
                    self.context(operation),
                ), [])

    def test_client_authority_fields_rejected_by_native_decoder(self):
        body = json.loads(encode_request(self.request(), self.limits))
        for field in (
            "actor", "verified", "tenant_id", "scope_id",
            "expected_generation", "sql", "shell",
        ):
            with self.subTest(field=field):
                extra = dict(body, **{field: "client-claim"})
                with self.assertRaises(ContractError):
                    decode_request(json.dumps(extra), self.limits)

    def test_extra_parameters_rejected_at_both_boundaries(self):
        request = self.request()
        with self.assertRaises(ContractError):
            replace(request, params=(("generation", "7"),))
        bad = replace(
            self.instruction(request),
            params=(AgentParam("generation", "str", "7", None, None),),
        )
        self.assertTrue(validate_agent_instruction(
            bad, self.catalog(), self.context(),
        ))

    def test_unknown_versions_refused_by_both_contracts(self):
        request = self.request()
        for version in ("2.0.0", "1.0", 1):
            with self.subTest(version=version):
                with self.assertRaises(ContractError):
                    replace(request, catalog_version=version)
                bad = replace(self.instruction(request), catalog_version=version)
                self.assertTrue(validate_agent_instruction(
                    bad, self.catalog(), self.context(),
                ))

    def test_utf8_byte_bound_is_not_agent_character_bound(self):
        target = "é" * 24
        request = self.request(target=target)
        self.assertEqual(validate_agent_instruction(
            self.instruction(request), self.catalog(),
            self.context(target=target),
        ), [])
        # 24 caracteres passent le profil Agent de fixture ; 48 octets
        # depassent le profil natif explicite de 32 octets, sans troncature.
        with self.assertRaises(ContractError):
            encode_request(request, PayloadLimits(8192, 32, 8))

    def test_boolean_is_not_a_string_parameter_in_either_contract(self):
        request = self.request("get_postgresql_result")
        with self.assertRaises(ContractError):
            replace(request, params=(("operation_ref", True),))
        bad = replace(self.instruction(request), params=(
            AgentParam("operation_ref", "str", True, None, None),
        ))
        self.assertTrue(validate_agent_instruction(
            bad, self.catalog(), self.context("get_postgresql_result"),
        ))

    def test_native_request_is_not_an_agent_instruction(self):
        self.assertTrue(validate_agent_instruction(
            self.request(), self.catalog(), self.context(),
        ))

    def test_agent_instruction_is_not_a_native_request(self):
        with self.assertRaises(ContractError):
            encode_request(self.instruction(self.request()), self.limits)

    def test_native_result_is_not_an_agent_result(self):
        native = decode_result(
            encode_result(self.native_result(), self.limits), self.limits,
        )
        self.assertTrue(validate_agent_result(native, self.context()))

    def test_agent_result_is_not_a_native_result(self):
        with self.assertRaises(ContractError):
            encode_result(self.agent_result(), self.limits)

    def test_six_native_phases_are_not_agent_outcome_values(self):
        for phase in PHASES:
            with self.subTest(phase=phase):
                native = self.native_result(phase)
                self.assertEqual(
                    decode_result(encode_result(native, self.limits),
                                  self.limits), native,
                )
                self.assertTrue(validate_agent_result(
                    replace(self.agent_result(), outcome=phase), self.context(),
                ))

    def test_native_success_does_not_supply_agent_confirmation_proof(self):
        native = self.native_result("SUCCEEDED")
        self.assertEqual(
            decode_result(encode_result(native, self.limits), self.limits),
            native,
        )
        self.assertTrue(validate_agent_result(
            replace(self.agent_result(), outcome="confirmed", origin_proof=None),
            self.context(),
        ))

    def test_different_anchor_counters_cannot_replace_agent_generation(self):
        anchor = self.anchor()
        for number in (anchor.epoch, anchor.sequence):
            with self.subTest(number=number):
                self.assertTrue(validate_agent_result(
                    replace(self.agent_result(), generation=number),
                    self.context(),
                ))

    def test_boolean_is_neither_anchor_counter_nor_agent_generation(self):
        with self.assertRaises(ContractError):
            replace(self.anchor(), epoch=True)
        self.assertTrue(validate_agent_result(
            replace(self.agent_result(), generation=True), self.context(),
        ))

    def test_native_microseconds_preserved_and_refused_by_agent_format(self):
        anchor = self.anchor()
        restored = decode_anchor_snapshot(
            encode_anchor_snapshot(anchor, self.anchor_limits),
            self.anchor_limits,
        )
        self.assertEqual(restored.observed_at, anchor.observed_at)
        self.assertTrue(validate_agent_result(
            replace(self.agent_result(), occurred_at=restored.observed_at),
            self.context(),
        ))

    def test_seconds_only_fixture_is_not_a_native_anchor_timestamp(self):
        with self.assertRaises(ContractError):
            replace(self.anchor(), observed_at="2030-01-01T00:00:00Z")
        # Une autre fixture Agent au format canonique, pas une projection.
        self.assertEqual(validate_agent_result(
            self.agent_result(), self.context(),
        ), [])

    def test_pure_contract_imports_do_not_load_runtime_providers(self):
        # Processus distinct : la decouverte combinee peut deja avoir charge
        # Django pour les autres tests Agent ; cela ne contamine pas ce cas.
        source_root = str(Path(__file__).resolve().parents[2] / "src")
        code = """import sys
from pixs.agent.contracts import AgentManagementInstruction
from pixs.pa_native.postgresql_contracts import NativeRequest, AnchorSnapshot
for prefix in ("django", "psycopg", "pixs.pa_native.tls_context",
               "pixs.pa_native.nv_anchor", "pixs.pa_native.nv_journal"):
    assert not any(name == prefix or name.startswith(prefix + ".")
                   for name in sys.modules), prefix
print("PURE_CONTRACT_IMPORTS_OK")
"""
        result = subprocess.run(
            [sys.executable, "-B", "-c", code],
            env={"PYTHONPATH": source_root, "PYTHONDONTWRITEBYTECODE": "1",
                 "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
            capture_output=True, text=True, timeout=10, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "PURE_CONTRACT_IMPORTS_OK\n")


if __name__ == "__main__":
    unittest.main()
