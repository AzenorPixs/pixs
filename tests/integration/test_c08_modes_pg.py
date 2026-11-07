"""Suite PG modes C08 : matrix12 + replay + divergences + ordinaire, processus frais."""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "integration"))
CASE_TIMEOUT = 180
MATRIX = (
    (("PENDING", "FIRST_CONFIGURATION"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "NORMAL"), "NEW_SNAPSHOT"),
    (("PENDING", "FIRST_CONFIGURATION"), "ENTER_MAINTENANCE", ("PENDING", "MAINTENANCE"), "NEW_SNAPSHOT"),
    (("PENDING", "FIRST_CONFIGURATION"), "EXIT_MAINTENANCE", ("PENDING", "FIRST_CONFIGURATION"), "NO_CHANGE"),
    (("PENDING", "MAINTENANCE"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "MAINTENANCE"), "NEW_SNAPSHOT"),
    (("PENDING", "MAINTENANCE"), "ENTER_MAINTENANCE", ("PENDING", "MAINTENANCE"), "NO_CHANGE"),
    (("PENDING", "MAINTENANCE"), "EXIT_MAINTENANCE", ("PENDING", "FIRST_CONFIGURATION"), "NEW_SNAPSHOT"),
    (("CONFIGURED", "NORMAL"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "NORMAL"), "NO_CHANGE"),
    (("CONFIGURED", "NORMAL"), "ENTER_MAINTENANCE", ("CONFIGURED", "MAINTENANCE"), "NEW_SNAPSHOT"),
    (("CONFIGURED", "NORMAL"), "EXIT_MAINTENANCE", ("CONFIGURED", "NORMAL"), "NO_CHANGE"),
    (("CONFIGURED", "MAINTENANCE"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "MAINTENANCE"), "NO_CHANGE"),
    (("CONFIGURED", "MAINTENANCE"), "ENTER_MAINTENANCE", ("CONFIGURED", "MAINTENANCE"), "NO_CHANGE"),
    (("CONFIGURED", "MAINTENANCE"), "EXIT_MAINTENANCE", ("CONFIGURED", "NORMAL"), "NEW_SNAPSHOT"),
)
CASES = tuple(["M%02d" % i for i in range(12)] + ["REPLAY", "DIVERGE_KEY", "DIVERGE_STALE", "ORDINARY"])

def _run_one(case):
    import core_pg_test_support as support
    from c08_modes_pg_harness import run_in_modes_schema
    doc = None
    code = 1
    with support.mask_output():
        try:
            from c08_modes_fixture import make_modes_fixture, ROOT_INST, ORD_INST
            from pixs.backend.installation.mode_values import ModeOperationKind as K
            from pixs.core.dto import CoreMutationResult
            from pixs.core.services_common import CoreServiceError
            KIND = {"FINALIZE_CONFIGURATION": K.FINALIZE_CONFIGURATION, "ENTER_MAINTENANCE": K.ENTER_MAINTENANCE, "EXIT_MAINTENANCE": K.EXIT_MAINTENANCE}
            def cb():
                from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as S
                from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord as R
                from pixs.core.persistence.models_audit import CoreAuditEvent
                from pixs.backend.c10_receipt_record import C10ReceiptRecord
                out = {}
                def counts(inst):
                    return (S.objects.using("peer").filter(installation_id=inst).count(), R.objects.using("peer").filter(installation_id=inst).count())
                def cur_row(inst):
                    row = S.objects.using("peer").filter(installation_id=inst).order_by("-version").first()
                    assert row is not None
                    return row
                def check_ok(inst, fx, op, kind_s, exp_ver, key, corr, exp_state, exp_mode, exp_kind):
                    res = fx["invoke"]("root" if inst == ROOT_INST else "ordinary", KIND[kind_s], exp_ver, key, op, corr)
                    assert type(res) is CoreMutationResult
                    assert res.operation_id == op and res.correlation_id == corr and res.version == (exp_ver + (1 if exp_kind == "NEW_SNAPSHOT" else 0))
                    exp_res = "pixs.backend.modes:" + inst
                    assert res.result_ref == exp_res
                    rc = fx["read_receipt_peer"](op)
                    assert rc.status == "SUCCEEDED" and rc.result_kind == exp_kind
                    sn = fx["read_snapshot_peer"](rc.result_snapshot_id)
                    assert (sn.configuration_state, sn.operating_mode) == (exp_state, exp_mode)
                    assert sn.version == rc.result_version == res.version
                    assert rc.result_correlation_id == rc.correlation_id == corr
                    assert str(rc.result_ref) == exp_res and str(rc.record_id) != str(sn.record_id)
                    assert sn.origin in ("R01_INITIAL", "MODE_TRANSITION")
                    assert type(sn.pid) is int and sn.pid > 0 and sn.xid.isdigit() and sn.database_oid > 0 and sn.schema_oid > 0
                    assert sn.metadata_owner_component == "pixs.backend"
                    stamps = C10ReceiptRecord.objects.using("peer").filter(
                        operation_id=op, receipt_kind="ATTEST")
                    assert stamps.count() == 1
                    stamp = stamps.first()
                    assert stamp.core_profile_ref == "c08mode"
                    assert stamp.core_data_asset_id == "asset:c08-mode-test"
                    assert rc.metadata_profile_ref == "c08mode"
                    assert rc.governance_status == "GOVERNED"
                    assert rc.metadata_owner_component == "pixs.backend"
                    assert rc.catalog_sha256 == stamp.raw_sha256
                    if exp_kind == "NEW_SNAPSHOT":
                        assert sn.operation_receipt_id == rc.record_id
                        assert sn.creator_operation_id == op
                        assert sn.version == exp_ver + 1
                        assert (sn.pid, sn.xid, sn.database_oid, sn.schema_oid) == (
                            rc.pid, rc.xid, rc.database_oid, rc.schema_oid)
                        pred = fx["read_snapshot_peer"](sn.predecessor_id)
                        assert pred.version == exp_ver and pred.installation_id == inst
                    else:
                        assert sn.operation_receipt_id != rc.record_id
                    assert CoreAuditEvent.objects.using("peer").filter(operation_id=op).count() == 1
                    return rc, sn
                if case.startswith("M"):
                    idx = int(case[1:])
                    initial, kind_s, target, exp_kind = MATRIX[idx]
                    def body():
                        with make_modes_fixture(str(ROOT)) as fx:
                            inst = ROOT_INST
                            if initial == ("PENDING", "MAINTENANCE"):
                                fx["invoke"]("root", K.ENTER_MAINTENANCE, 1, "k-pre-%s" % case, "op-pre-%s" % case, "corr-pre-%s" % case)
                            elif initial == ("CONFIGURED", "NORMAL"):
                                fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 1, "k-pre-%s" % case, "op-pre-%s" % case, "corr-pre-%s" % case)
                            elif initial == ("CONFIGURED", "MAINTENANCE"):
                                fx["invoke"]("root", K.ENTER_MAINTENANCE, 1, "k-pre1-%s" % case, "op-pre1-%s" % case, "corr-pre1-%s" % case)
                                fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 2, "k-pre2-%s" % case, "op-pre2-%s" % case, "corr-pre2-%s" % case)
                            cur = cur_row(inst)
                            assert (cur.configuration_state, cur.operating_mode) == initial
                            n0, r0 = counts(inst)
                            op, corr, key = "op-%s" % case, "corr-%s" % case, "k-%s" % case
                            check_ok(inst, fx, op, kind_s, cur.version, key, corr, target[0], target[1], exp_kind)
                            n1, r1 = counts(inst)
                            assert r1 == r0 + 1 and n1 == n0 + (1 if exp_kind == "NEW_SNAPSHOT" else 0)
                            rd = fx["readers"][inst].read_current()
                            assert rd.configuration_state.value == target[0] and rd.operating_mode.value == target[1]
                            return True
                    out[case] = bool(body())
                elif case == "REPLAY":
                    def body():
                        with make_modes_fixture(str(ROOT)) as fx:
                            inst = ROOT_INST
                            r1 = fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 1, "k-replay", "op-replay-1", "corr-replay-1")
                            assert type(r1) is CoreMutationResult and r1.version == 2
                            fx["invoke"]("root", K.ENTER_MAINTENANCE, 2, "k-replay-2", "op-replay-2", "corr-replay-2")
                            fx["invoke"]("root", K.EXIT_MAINTENANCE, 3, "k-replay-3", "op-replay-3", "corr-replay-3")
                            assert cur_row(inst).version == 4
                            n0, r0 = counts(inst)
                            r2 = fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 1, "k-replay", "op-replay-new", "corr-replay-new")
                            assert type(r2) is CoreMutationResult
                            assert r2.operation_id == r1.operation_id == "op-replay-1"
                            assert r2.correlation_id == r1.correlation_id == "corr-replay-1"
                            assert r2.version == 2 == r1.version and r2.result_ref == r1.result_ref
                            assert counts(inst) == (n0, r0)
                            assert cur_row(inst).version == 4
                            assert fx["readers"][inst].read_current().version == 4
                            assert CoreAuditEvent.objects.using("peer").filter(
                                operation_id="op-replay-new").count() == 1
                            assert C10ReceiptRecord.objects.using("peer").filter(
                                operation_id="op-replay-new", receipt_kind="ATTEST").count() == 1
                            assert fx["read_receipt_peer"]("op-replay-1").status == "SUCCEEDED"
                            return True
                    out[case] = bool(body())
                elif case == "DIVERGE_KEY":
                    def body():
                        with make_modes_fixture(str(ROOT)) as fx:
                            inst = ROOT_INST
                            fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 1, "k-div-key", "op-div-key-1", "corr-div-key-1")
                            n0, r0 = counts(inst)
                            try:
                                fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 2, "k-div-key", "op-div-key-2", "corr-div-key-2")
                            except CoreServiceError as e:
                                assert e.code == "IDEMPOTENCE_CONFLIT"
                                assert counts(inst) == (n0, r0)
                                return True
                            return False
                    out[case] = bool(body())
                elif case == "DIVERGE_STALE":
                    def body():
                        with make_modes_fixture(str(ROOT)) as fx:
                            inst = ROOT_INST
                            fx["invoke"]("root", K.FINALIZE_CONFIGURATION, 1, "k-stale-1", "op-stale-1", "corr-stale-1")
                            n0, r0 = counts(inst)
                            try:
                                fx["invoke"]("root", K.ENTER_MAINTENANCE, 1, "k-stale-2", "op-stale-2", "corr-stale-2")
                            except CoreServiceError as e:
                                assert e.code == "IDEMPOTENCE_CONFLIT"
                                assert counts(inst) == (n0, r0)
                                return True
                            return False
                    out[case] = bool(body())
                elif case == "ORDINARY":
                    def body():
                        with make_modes_fixture(str(ROOT)) as fx:
                            inst = ORD_INST
                            fx["invoke"]("ordinary", K.ENTER_MAINTENANCE, 1, "k-ord-1", "op-ord-1", "corr-ord-1")
                            fx["invoke"]("ordinary", K.EXIT_MAINTENANCE, 2, "k-ord-2", "op-ord-2", "corr-ord-2")
                            cur = cur_row(inst)
                            assert (cur.configuration_state, cur.operating_mode) == ("PENDING", "FIRST_CONFIGURATION")
                            n0, r0 = counts(inst)
                            try:
                                fx["invoke"]("ordinary", K.FINALIZE_CONFIGURATION, cur.version, "k-ord-3", "op-ord-3", "corr-ord-3")
                            except CoreServiceError as e:
                                assert e.code == "IDEMPOTENCE_PREUVE_INVALIDE"
                                cur2 = cur_row(inst)
                                assert (cur2.configuration_state, cur2.operating_mode) == ("PENDING", "FIRST_CONFIGURATION")
                                assert counts(inst) == (n0, r0)
                                return True
                            return False
                    out[case] = bool(body())
                else:
                    out[case] = False
                return out
            res = run_in_modes_schema(str(ROOT), cb, (case,))
            doc = {"case": case, "code": res["code"], "cases": res["cases"],
                   "proof": {k: res[k] for k in (
                       "real_pg", "namespace", "migration", "core_migration",
                       "backend_migration", "cleanup", "conns_closed")},
                   "versions": {"pg": res["pg_version_num"], "django": res["django_version"]},
                   "failure_type": res["failure_type"], "failure_frames": res["failure_frames"]}
        except Exception as e:
            doc = {"case": case, "code": "CHILD_FAILED", "failure_type": type(e).__name__}
            code = 1
        else:
            code = 0 if (doc["code"] == "NONE" and doc["cases"].get(case) is True
                         and all(v is True for v in doc["proof"].values())) else 1
    print(json.dumps(doc, sort_keys=True, separators=(",", ":")))
    return code

def _driver():
    import subprocess
    import core_pg_test_support as support
    agg = {"code": "PASS", "cases": {}, "versions": {}}
    with support.mask_output():
        for case in CASES:
            try:
                p = subprocess.run([sys.executable, "-B", str(Path(__file__)), "--case", case], cwd=str(ROOT), timeout=CASE_TIMEOUT, capture_output=True, text=True)
            except (OSError, subprocess.SubprocessError):
                agg["cases"][case] = False
                agg["code"] = "TEST_FAILED"
                continue
            line = (p.stdout.strip().splitlines() or [""]) [-1]
            try:
                doc = json.loads(line)
            except json.JSONDecodeError:
                agg["cases"][case] = False
                agg["code"] = "TEST_FAILED"
                continue
            ok = (type(doc) is dict and p.returncode == 0
                  and doc.get("case") == case and doc.get("code") == "NONE"
                  and type(doc.get("cases")) is dict
                  and set(doc["cases"]) == {case} and doc["cases"][case] is True
                  and type(doc.get("proof")) is dict
                  and set(doc["proof"]) == {"real_pg", "namespace", "migration", "core_migration",
                                             "backend_migration", "cleanup", "conns_closed"}
                  and all(v is True for v in doc["proof"].values()))
            if type(doc) is dict and type(doc.get("versions")) is dict:
                agg["versions"][case] = doc["versions"]
            agg["cases"][case] = bool(ok)
            if not ok:
                agg["code"] = "TEST_FAILED"
    print(json.dumps({"code": agg["code"], "cases": agg["cases"], "versions": agg["versions"]}, sort_keys=True, separators=(",", ":")))
    return 0 if agg["code"] == "PASS" else 1

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default=None)
    ns = ap.parse_args()
    if ns.case is None:
        raise SystemExit(_driver())
    if ns.case not in CASES:
        print(json.dumps({"case": ns.case, "code": "UNKNOWN_CASE"}))
        raise SystemExit(2)
    raise SystemExit(_run_one(ns.case))
