"""Exercice d'intégration des contrats 2.1a avec ScopeContext public et contexte synthétique déclaré."""
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "AGENT_MANAGEMENT_SAFE_INTEGRATION_OK\n"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(
    r'''
    import datetime
    import sys

    sys.path.insert(0, sys.argv[1])

    FORBIDDEN = ("django", "psycopg", "psycopg2", "psycopg_pool", "psycopg_binary")

    class Finder:
        def find_spec(self, fullname, path=None, target=None):
            for prefix in FORBIDDEN:
                if fullname == prefix or fullname.startswith(prefix + "."):
                    raise AssertionError("forbidden base import")
            return None

    sys.meta_path.insert(0, Finder())
    real_datetime = datetime.datetime

    class Guarded(real_datetime):
        @classmethod
        def now(cls, tz=None):
            raise AssertionError("forbidden clock")
        @classmethod
        def today(cls):
            raise AssertionError("forbidden clock")
        @classmethod
        def utcnow(cls):
            raise AssertionError("forbidden clock")

    datetime.datetime = Guarded
    from pixs.agent.contracts import (
        AgentManagementInstruction,
        AgentManagementResult,
        AgentManagementState,
        AgentParam,
        AgentParamSpec,
        AgentValidationContext,
        AllowedCatalogEntry,
        validate_agent_instruction,
        validate_agent_result,
        validate_agent_state,
    )
    from pixs.core.scope import ScopeContext, ScopeType

    scope = ScopeContext(ScopeType.TENANT, "tenant-synth-1", "scope-synth-1")
    catalog = (AllowedCatalogEntry(operation="synth.sys.nop", version="1.0.0", params=(AgentParamSpec(name="message", kind="str", max_len=32, int_min=None, int_max=None, required=True),)),)
    ctx = AgentValidationContext(expected_actor="actor-synth-1", expected_scope=scope, expected_target="pa-synth-1", expected_generation=7, expected_operation="synth.sys.nop", expected_version="1.0.0", expected_operation_id="op-synth-1", expected_idempotency_key="key-synth-1", expected_correlation_ids=("corr-1",), now_iso="2030-01-01T00:00:00Z", mandate_proof="mandate-synth-1", expected_origin_proof="origin-synth-1", expected_confirmation_proof="confirm-synth-1", max_id_len=64, max_doc_len=1024, max_ids=8, max_params=8, max_observation_age_seconds=3600)
    inst = AgentManagementInstruction(schema_version="1.0.0", operation_id="op-synth-1", catalog_operation="synth.sys.nop", catalog_version="1.0.0", initial_actor="actor-synth-1", scope_context=scope, pa_target="pa-synth-1", expected_generation=7, mandate_ref="mandate-synth-1", expires_at="2030-01-01T01:00:00Z", correlation_ids=("corr-1",), causation_ids=(), idempotency_key="key-synth-1", params=(AgentParam(name="message", kind="str", str_value="bonjour", int_value=None, bool_value=None),))
    assert validate_agent_instruction(inst, catalog, ctx) == []
    expired = AgentManagementInstruction(schema_version="1.0.0", operation_id="op-synth-1", catalog_operation="synth.sys.nop", catalog_version="1.0.0", initial_actor="actor-synth-1", scope_context=scope, pa_target="pa-synth-1", expected_generation=7, mandate_ref="mandate-synth-1", expires_at="2029-12-31T23:59:59Z", correlation_ids=("corr-1",), causation_ids=(), idempotency_key="key-synth-1", params=(AgentParam(name="message", kind="str", str_value="bonjour", int_value=None, bool_value=None),))
    assert any("expires_at" in d.element for d in validate_agent_instruction(expired, catalog, ctx))
    cross = AgentManagementInstruction(schema_version="1.0.0", operation_id="op-autre", catalog_operation="synth.sys.nop", catalog_version="1.0.0", initial_actor="actor-synth-1", scope_context=scope, pa_target="pa-synth-1", expected_generation=7, mandate_ref="mandate-synth-1", expires_at="2030-01-01T01:00:00Z", correlation_ids=("corr-1",), causation_ids=(), idempotency_key="key-synth-1", params=(AgentParam(name="message", kind="str", str_value="bonjour", int_value=None, bool_value=None),))
    assert any("binding.operation_id" in d.element for d in validate_agent_instruction(cross, catalog, ctx))
    st = AgentManagementState(scope_context=scope, operation_id="op-synth-1", pa_target="pa-synth-1", generation=7, desired_doc="souhait", observed_doc="appliqué", observed_at="2029-12-31T23:55:00Z", last_known_doc="connu", last_known_at="2029-12-31T23:56:00Z", confirmation_proof="confirm-synth-1")
    assert validate_agent_state(st, ctx) == []
    stale = AgentManagementState(scope_context=scope, operation_id="op-synth-1", pa_target="pa-synth-1", generation=7, desired_doc="souhait", observed_doc="appliqué", observed_at="2029-12-30T00:00:00Z", last_known_doc="connu", last_known_at="2029-12-30T01:00:00Z", confirmation_proof="confirm-synth-1")
    assert any("confirmation" in d.element for d in validate_agent_state(stale, ctx))
    res = AgentManagementResult(scope_context=scope, operation_id="op-synth-1", pa_target="pa-synth-1", generation=7, outcome="confirmed", correlation_ids=("corr-1",), occurred_at="2029-12-31T23:00:00Z", origin_proof="origin-synth-1")
    assert validate_agent_result(res, ctx) == []
    bad_proof = AgentManagementResult(scope_context=scope, operation_id="op-synth-1", pa_target="pa-synth-1", generation=7, outcome="confirmed", correlation_ids=("corr-1",), occurred_at="2029-12-31T23:00:00Z", origin_proof="quelconque")
    assert any("origin" in d.element for d in validate_agent_result(bad_proof, ctx))
    assert "<redacted>" in repr(inst) and "actor-synth-1" not in repr(inst)
    sys.stdout.write("AGENT_MANAGEMENT_SAFE_INTEGRATION_OK\n")
    '''
)


class Boundary(unittest.TestCase):
    def test_exercice_contrats_synthétiques_sans_effet(self):
        proc = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            capture_output=True,
            text=True,
            env=_ENV,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
