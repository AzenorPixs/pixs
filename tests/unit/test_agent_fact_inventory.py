# path: tests/unit/test_agent_fact_inventory.py
"""Unite U1 : codec agent-fact-inventory.v1 D-S1 3.6, pur sans DB."""
from __future__ import annotations
import hashlib
import json
import unittest
import uuid
from pixs.agent import fact_inventory as inv

UUID_A = uuid.UUID("0193b7b0-0000-7000-8000-000000000001")
UUID_B = uuid.UUID("0193b7b0-0000-7000-8000-000000000002")
UUID_C = uuid.UUID("0193b7b0-0000-7000-8000-000000000003")
GOLDEN_TEXT = r'["0193b7b0-0000-7000-8000-000000000001","0193b7b0-0000-7000-8000-000000000002",null,"TENANT","café","café","cible a b",7,"OBSERVED","ack","2026-10-26T12:00:01Z",null,null,"doc ligne1\nligne2 😀","src-1",null,null]'

class FactInventoryTest(unittest.TestCase):
    def test_golden_positions(self):
        parsed = json.loads(GOLDEN_TEXT)
        self.assertEqual(parsed[0], str(UUID_A))
        self.assertEqual(parsed[1], str(UUID_B))
        self.assertIsNone(parsed[2])
        self.assertEqual(parsed[3], "TENANT")
        self.assertEqual(parsed[7], 7)
        self.assertEqual(parsed[8], "OBSERVED")
        self.assertIn("😀", GOLDEN_TEXT)
        out = inv.require_fact_inventory_canonical(GOLDEN_TEXT)
        self.assertEqual(out, GOLDEN_TEXT)

    def test_canonical_roundtrip_literal(self):
        text = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="TENANT", tenant_id="café", scope_id="café", target_id="cible a b", generation=7, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof=None, observed_document="doc ligne1\nligne2 😀", source_ref="src-1", proof_ref=None, postcondition_ref=None)
        self.assertEqual(text, GOLDEN_TEXT)
        self.assertEqual(inv.require_fact_inventory_canonical(text), text)

    def test_third_uuid_nonnull_and_generations(self):
        for gen in (0, 9223372036854775807):
            text = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=UUID_C, scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="t", generation=gen, kind="CONFIRMED", outcome="confirmed", occurred_at="2026-10-26T12:00:01.000001Z", observed_at="2026-10-26T12:00:01.000001Z", origin_proof="p", observed_document="d", source_ref="s", proof_ref="pr", postcondition_ref="pc")
            self.assertEqual(inv.require_fact_inventory_canonical(text), text)
            parsed = json.loads(text)
            self.assertEqual(parsed[2], str(UUID_C))
            self.assertEqual(parsed[7], gen)

    def test_uuid_str_rejected_at_encode(self):
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.canonical_fact_inventory(id=str(UUID_A), operation_id=UUID_B, observed_fact_id=None, scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="t", generation=0, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof=None, observed_document=None, source_ref="s", proof_ref=None, postcondition_ref=None)

    def test_noncanonical_uuid_forms_refused_at_decode(self):
        upper = GOLDEN_TEXT.replace("0193b7b0-0000-7000-8000-000000000001", "0193B7B0-0000-7000-8000-000000000001")
        braced = GOLDEN_TEXT.replace("0193b7b0-0000-7000-8000-000000000001", "{0193b7b0-0000-7000-8000-000000000001}")
        compact = GOLDEN_TEXT.replace("0193b7b0-0000-7000-8000-000000000001", "0193b7b0000070008000000000000001")
        for bad in (upper, braced, compact):
            with self.assertRaises(inv.AgentFactInventoryError):
                inv.require_fact_inventory_canonical(bad)

    def test_unicode_nfc_nfd_spaces_lf_preserved(self):
        nfc = "café"
        nfd = "café"
        self.assertNotEqual(nfc, nfd)
        t1 = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="TENANT", tenant_id=nfc, scope_id="a b", target_id="t", generation=0, kind="OBSERVED", outcome="failed", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof="p", observed_document="x", source_ref="s", proof_ref=None, postcondition_ref=None)
        t2 = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="TENANT", tenant_id=nfd, scope_id="a b", target_id="t", generation=0, kind="OBSERVED", outcome="failed", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof="p", observed_document="x", source_ref="s", proof_ref=None, postcondition_ref=None)
        self.assertNotEqual(t1, t2)
        lf = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="t", generation=0, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof=None, observed_document="l1\nl2", source_ref="s", proof_ref=None, postcondition_ref=None)
        self.assertIn("\\n", lf)
        self.assertEqual(inv.require_fact_inventory_canonical(lf), lf)

    def test_dates_untouched_second_and_micro(self):
        for stamp in ("2026-10-26T12:00:01Z", "2026-10-26T12:00:01.000001Z"):
            text = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="t", generation=0, kind="OBSERVED", outcome="ack", occurred_at=stamp, observed_at=None, origin_proof=None, observed_document=None, source_ref="s", proof_ref=None, postcondition_ref=None)
            self.assertIn(stamp, text)
            self.assertEqual(inv.require_fact_inventory_canonical(text), text)

    def test_nullable_shape_and_duplicates_between_columns(self):
        text = inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="TENANT", tenant_id="same", scope_id="same", target_id="same", generation=0, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at="2026-10-26T12:00:01Z", origin_proof="same", observed_document="same", source_ref="same", proof_ref="same", postcondition_ref="same")
        self.assertEqual(inv.require_fact_inventory_canonical(text), text)
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.canonical_fact_inventory(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="PLATFORM", tenant_id="x", scope_id=None, target_id="t", generation=0, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof=None, observed_document=None, source_ref="s", proof_ref=None, postcondition_ref=None)

    def test_bounds_and_types_refused(self):
        base = dict(id=UUID_A, operation_id=UUID_B, observed_fact_id=None, scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="t", generation=0, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof=None, observed_document=None, source_ref="s", proof_ref=None, postcondition_ref=None)
        for bad in (True, "0", 1.0, -1, 9223372036854775808):
            kw = dict(base)
            kw["generation"] = bad
            with self.assertRaises(inv.AgentFactInventoryError):
                inv.canonical_fact_inventory(**kw)
        for key in ("target_id", "occurred_at", "source_ref"):
            kw = dict(base)
            kw[key] = ""
            with self.assertRaises(inv.AgentFactInventoryError):
                inv.canonical_fact_inventory(**kw)
            kw[key] = "a\x00b"
            with self.assertRaises(inv.AgentFactInventoryError):
                inv.canonical_fact_inventory(**kw)
        kw = dict(base)
        kw["target_id"] = "a\ud800b"
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.canonical_fact_inventory(**kw)
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.require_fact_inventory_canonical('["0193b7b0-0000-7000-8000-000000000001","0193b7b0-0000-7000-8000-000000000002",null,"PLATFORM",null,null,"t",1.0,"OBSERVED","ack","2026-10-26T12:00:01Z",null,null,null,"s",null,null]')
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.require_fact_inventory_canonical('{"id":"x"}')
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.require_fact_inventory_canonical(json.dumps([None] * 16))
        with self.assertRaises(inv.AgentFactInventoryError):
            inv.require_fact_inventory_canonical(GOLDEN_TEXT + "\n")

    def test_errors_stable_without_values_and_digest_raw(self):
        try:
            inv.canonical_fact_inventory(id="secret", operation_id=UUID_B, observed_fact_id=None, scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="t", generation=0, kind="OBSERVED", outcome="ack", occurred_at="2026-10-26T12:00:01Z", observed_at=None, origin_proof=None, observed_document=None, source_ref="s", proof_ref=None, postcondition_ref=None)
            self.fail("attendu refus")
        except inv.AgentFactInventoryError as error:
            self.assertEqual(str(error), "AgentFactInventoryError(<redacted>)")
            self.assertNotIn("secret", str(error))
            self.assertEqual(error.code, "AGENT_FACT_INVENTORY_INVALID")
        digest = inv.fact_inventory_sha256(GOLDEN_TEXT)
        self.assertEqual(digest, hashlib.sha256(GOLDEN_TEXT.encode("utf-8")).hexdigest())
        self.assertEqual(len(digest), 64)

if __name__ == "__main__":
    unittest.main()
