"""Recette C08 TEST_ONLY : deux processus et trois refus SQL transactionnels.

Chaque cas prepare un schema jetable reel via le harnais existant. Ces cas
ne qualifient ni perte de reponse au commit, ni PA/PZT/PKI ou plateformes.
Aucun scenario ne s'execute a l'import.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "integration"))
WORKER = ROOT / "tests" / "integration" / "c08_modes_process_worker.py"
CASES = ("DIFFERENT", "SAME", "FAIL_C08", "FAIL_C10", "FAIL_C05")
PROOF_KEYS = {"real_pg", "namespace", "migration", "core_migration",
              "backend_migration", "cleanup", "conns_closed"}
RESULT_KEYS = {"status", "error_code", "result", "target_constraint_detected", "ready", "cleanup"}
PROCESS_BUDGET = 150
CASE_TIMEOUT = 480
MAX_DOCUMENT = 65536


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("DOCUMENT_INVALID")
        result[key] = value
    return result


def _constant(_value):
    raise ValueError("DOCUMENT_INVALID")


def _document(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_DOCUMENT:
        raise ValueError("DOCUMENT_INVALID")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    if type(value) is not dict:
        raise ValueError("DOCUMENT_INVALID")
    return value


def _close_fd(descriptor, owned):
    os.close(descriptor)
    owned.remove(descriptor)


def _feed(process, data, deadline):
    if process.stdin is None:
        raise RuntimeError("CHILD_INPUT_UNPROVED")
    descriptor = process.stdin.fileno()
    os.set_blocking(descriptor, False)
    view = memoryview(data)
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(descriptor, selectors.EVENT_WRITE)
            while view:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    raise RuntimeError("CHILD_INPUT_UNPROVED")
                written = os.write(descriptor, view[:4096])
                if written < 1:
                    raise RuntimeError("CHILD_INPUT_UNPROVED")
                view = view[written:]
    finally:
        process.stdin.close()
        process.stdin = None


def _ready(bundles, recipe, owned, deadline):
    frames = {}
    with selectors.DefaultSelector() as selector:
        for index, item in enumerate(bundles):
            selector.register(item["ready_fd"], selectors.EVENT_READ, index)
            frames[index] = b""
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("CHILD_READY_UNPROVED")
            events = selector.select(remaining)
            if not events:
                raise RuntimeError("CHILD_READY_UNPROVED")
            for key, _ in events:
                fragment = os.read(key.fd, 257)
                if not fragment:
                    raise RuntimeError("CHILD_READY_UNPROVED")
                frames[key.data] += fragment
                if len(frames[key.data]) > 256:
                    raise RuntimeError("CHILD_READY_UNPROVED")
                if b"\n" not in frames[key.data]:
                    continue
                match = re.fullmatch(rb"READY ([1-9][0-9]*) ([1-9][0-9]*) ([1-9][0-9]*)\n",
                                     frames[key.data])
                if match is None:
                    raise RuntimeError("CHILD_READY_UNPROVED")
                pid, schema_oid, db_oid = map(int, match.groups())
                if schema_oid != recipe["schema_oid"] or db_oid != recipe["db_oid"]:
                    raise RuntimeError("CHILD_READY_UNPROVED")
                bundles[key.data]["ready"] = {"pid": pid, "schema_oid": schema_oid, "db_oid": db_oid}
                selector.unregister(key.fd)
                _close_fd(key.fd, owned)
    if len({item["ready"]["pid"] for item in bundles}) != len(bundles):
        raise RuntimeError("CHILD_READY_UNPROVED")
    for item in bundles:
        if os.write(item["go_fd"], b"G") != 1:
            raise RuntimeError("CHILD_GO_UNPROVED")
        _close_fd(item["go_fd"], owned)


@contextmanager
def _workers(recipe, tasks, *, rendezvous):
    processes, bundles, owned = [], [], set()
    deadline = time.monotonic() + PROCESS_BUDGET
    try:
        for task in tasks:
            data = json.dumps({"recipe": recipe, "task": task}, sort_keys=True,
                              separators=(",", ":"), allow_nan=False).encode("utf-8")
            if len(data) > MAX_DOCUMENT:
                raise RuntimeError("CHILD_INPUT_UNPROVED")
            args = [sys.executable, "-B", str(WORKER), "--worker"]
            pass_fds = ()
            item = {}
            if rendezvous:
                ready_read, ready_write = os.pipe()
                owned.update((ready_read, ready_write))
                go_read, go_write = os.pipe()
                owned.update((go_read, go_write))
                pass_fds = (ready_write, go_read)
                args.extend(("--ready-fd", str(ready_write), "--go-fd", str(go_read)))
                item.update(ready_fd=ready_read, go_fd=go_write)
            process = subprocess.Popen(args, cwd=str(ROOT), stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                       close_fds=True, pass_fds=pass_fds)
            processes.append(process)
            item["process"] = process
            bundles.append(item)
            if rendezvous:
                _close_fd(ready_write, owned)
                _close_fd(go_read, owned)
            _feed(process, data, min(deadline, time.monotonic() + 30))
        if rendezvous:
            _ready(bundles, recipe, owned, min(deadline, time.monotonic() + 45))
        results = []
        for item in bundles:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("CHILD_RESULT_UNPROVED")
            output, _ = item["process"].communicate(timeout=remaining)
            if item["process"].returncode != 0:
                raise RuntimeError("CHILD_RESULT_UNPROVED")
            document = _document(output)
            if (set(document) != RESULT_KEYS or document["cleanup"] is not True
                    or document["status"] not in ("SUCCESS", "REJECTED")
                    or type(document["target_constraint_detected"]) is not bool):
                raise RuntimeError("CHILD_RESULT_UNPROVED")
            ready = document["ready"]
            if (type(ready) is not dict or set(ready) != {"pid", "schema_oid", "db_oid"}
                    or type(ready["pid"]) is not int or ready["pid"] < 1
                    or ready["schema_oid"] != recipe["schema_oid"]
                    or ready["db_oid"] != recipe["db_oid"]
                    or (rendezvous and ready != item["ready"])):
                raise RuntimeError("CHILD_RESULT_UNPROVED")
            result = document["result"]
            if document["status"] == "SUCCESS":
                if (type(result) is not dict
                        or set(result) != {"operation_id", "result_ref", "version", "correlation_id"}
                        or type(result["version"]) is not int or result["version"] < 1
                        or document["error_code"] != "NONE"):
                    raise RuntimeError("CHILD_RESULT_UNPROVED")
            elif result is not None:
                raise RuntimeError("CHILD_RESULT_UNPROVED")
            results.append(document)
        yield results
    finally:
        failures = []
        for process in processes:
            try:
                if process.poll() is None:
                    process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                for stream in (process.stdin, process.stdout, process.stderr):
                    if stream is not None and not stream.closed:
                        stream.close()
            except (OSError, subprocess.SubprocessError):
                failures.append("CHILD_CLEANUP_UNPROVED")
        for descriptor in tuple(owned):
            try:
                _close_fd(descriptor, owned)
            except OSError:
                failures.append("FD_CLEANUP_UNPROVED")
        if failures or owned or any(process.poll() is None for process in processes):
            raise RuntimeError("CHILD_CLEANUP_UNPROVED")


def _task(kind, key, operation, correlation, fault="NONE"):
    return {"role": "root", "kind": kind, "expected": 1, "key": key,
            "operation_id": operation, "correlation_id": correlation, "fault": fault}


def _case(case):
    from c08_modes_fixture import make_modes_fixture, ROOT_INST
    from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as Snapshot
    from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord as Receipt
    from pixs.backend.c10_receipt_record import C10ReceiptRecord
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from django.db import connections

    with make_modes_fixture(str(ROOT)) as fixture:
        recipe = fixture["worker_recipe"]()
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid()")
            parent_pid = cursor.fetchone()[0]
        with connections["peer"].cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid()")
            peer_pid = cursor.fetchone()[0]
        assert type(parent_pid) is int and type(peer_pid) is int and parent_pid != peer_pid
        initial = list(Snapshot.objects.using("peer").filter(installation_id=ROOT_INST).values())
        assert len(initial) == 1 and initial[0]["version"] == 1
        assert Receipt.objects.using("peer").filter(installation_id=ROOT_INST).count() == 0
        markers = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
                   for path in recipe["marker_paths"].values()}
        if case == "DIFFERENT":
            tasks = [_task("FINALIZE_CONFIGURATION", "diff1", "op-diff1", "corr-diff1"),
                     _task("ENTER_MAINTENANCE", "diff2", "op-diff2", "corr-diff2")]
        elif case == "SAME":
            tasks = [_task("FINALIZE_CONFIGURATION", "same", "op-same1", "corr-same1"),
                     _task("FINALIZE_CONFIGURATION", "same", "op-same2", "corr-same2")]
        elif case in ("FAIL_C08", "FAIL_C10", "FAIL_C05"):
            tasks = [_task("FINALIZE_CONFIGURATION", "fault", "op-" + case, "corr-" + case, case)]
        else:
            raise RuntimeError("CASE_INVALID")
        with _workers(recipe, tasks, rendezvous=case in ("DIFFERENT", "SAME")) as results:
            assert len(results) == len(tasks)
            assert all(value["ready"]["pid"] not in (parent_pid, peer_pid) for value in results)
            assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
                       for path, digest in markers.items())
            if case in ("DIFFERENT", "SAME"):
                assert all(value["target_constraint_detected"] is False for value in results)
                receipts = list(Receipt.objects.using("peer").filter(installation_id=ROOT_INST))
                snapshots = list(Snapshot.objects.using("peer").filter(installation_id=ROOT_INST).order_by("version"))
                assert len(receipts) == 1 and len(snapshots) == 2
                receipt, latest = receipts[0], snapshots[1]
                assert receipt.status == "SUCCEEDED" and receipt.result_kind == "NEW_SNAPSHOT"
                assert latest.version == receipt.result_version == 2
                assert latest.operation_receipt_id == receipt.record_id
                assert latest.pid == receipt.pid and latest.xid == receipt.xid
                assert latest.predecessor_id == initial[0]["record_id"]
                if case == "DIFFERENT":
                    assert sorted(value["status"] for value in results) == ["REJECTED", "SUCCESS"]
                    winner = next(i for i, value in enumerate(results) if value["status"] == "SUCCESS")
                    loser = 1 - winner
                    assert results[loser]["error_code"] == "IDEMPOTENCE_CONFLIT"
                    expected = (("CONFIGURED", "NORMAL") if winner == 0 else ("PENDING", "MAINTENANCE"))
                else:
                    assert all(value["status"] == "SUCCESS" for value in results)
                    assert results[0]["result"] == results[1]["result"]
                    winner = next(i for i, task in enumerate(tasks)
                                  if task["operation_id"] == results[0]["result"]["operation_id"])
                    expected = ("CONFIGURED", "NORMAL")
                assert (latest.configuration_state, latest.operating_mode) == expected
                assert receipt.operation_id == tasks[winner]["operation_id"]
                assert receipt.pid == results[winner]["ready"]["pid"]
                assert receipt.result_correlation_id == tasks[winner]["correlation_id"]
                assert receipt.result_ref == "pixs.backend.modes:" + ROOT_INST
                for index, (task, value) in enumerate(zip(tasks, results)):
                    audits = list(CoreAuditEvent.objects.using("peer").filter(operation_id=task["operation_id"]))
                    assert len(audits) == 1 and type(audits[0].pdp_payload) is dict
                    effect = "DENY" if value["status"] == "REJECTED" else "ALLOW"
                    assert audits[0].pdp_payload["effect"] == effect
                    assert audits[0].pdp_payload["correlation_id"] == task["correlation_id"]
                    stamps = list(C10ReceiptRecord.objects.using("peer").filter(
                        operation_id=task["operation_id"], receipt_kind="ATTEST"))
                    assert len(stamps) == (0 if value["status"] == "REJECTED" else 1)
                    if stamps:
                        assert stamps[0].core_profile_ref == "c08mode"
                        assert stamps[0].pid == value["ready"]["pid"]
                        assert stamps[0].correlation_id == task["correlation_id"]
                    if value["status"] == "SUCCESS":
                        assert value["result"] == {
                            "operation_id": receipt.operation_id, "result_ref": receipt.result_ref,
                            "version": receipt.result_version, "correlation_id": receipt.result_correlation_id}
            else:
                value = results[0]
                assert value["status"] == "REJECTED" and value["target_constraint_detected"] is True
                code = {"FAIL_C08": "IDEMPOTENCE_PREUVE_INVALIDE", "FAIL_C10": "CORE_PORT_ERROR",
                        "FAIL_C05": "AUDIT_REFUS_INDISPONIBLE"}[case]
                assert value["error_code"] == code
                assert list(Snapshot.objects.using("peer").filter(installation_id=ROOT_INST).values()) == initial
                assert Receipt.objects.using("peer").filter(installation_id=ROOT_INST).count() == 0
                assert C10ReceiptRecord.objects.using("peer").filter(operation_id=tasks[0]["operation_id"]).count() == 0
                audits = list(CoreAuditEvent.objects.using("peer").filter(operation_id=tasks[0]["operation_id"]))
                if case == "FAIL_C05":
                    assert audits == []
                else:
                    assert len(audits) == 1 and type(audits[0].pdp_payload) is dict
                    assert audits[0].pdp_payload["effect"] == "DENY"
                    assert audits[0].pdp_payload["correlation_id"] == tasks[0]["correlation_id"]
    return True


def _run_case(case):
    import core_pg_test_support as support
    from c08_modes_pg_harness import run_in_modes_schema

    with support.mask_output():
        try:
            result = run_in_modes_schema(str(ROOT), lambda: {case: _case(case)}, (case,))
            proof = {key: result[key] for key in PROOF_KEYS}
            document = {"case": case, "code": result["code"], "cases": result["cases"], "proof": proof,
                        "versions": {"pg": result["pg_version_num"], "django": result["django_version"]},
                        "failure_type": result["failure_type"]}
            success = (document["code"] == "NONE" and document["cases"] == {case: True}
                       and all(value is True for value in proof.values()))
        except Exception as error:
            document = {"case": case, "code": "CHILD_FAILED", "failure_type": type(error).__name__}
            success = False
    print(json.dumps(document, sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0 if success else 1


def _driver():
    import core_pg_test_support as support

    aggregate = {"code": "PASS", "cases": {}, "versions": {}}
    with support.mask_output():
        for case in CASES:
            good = False
            try:
                process = subprocess.run([sys.executable, "-B", str(Path(__file__)), "--case", case],
                                         cwd=str(ROOT), capture_output=True, timeout=CASE_TIMEOUT)
                document = _document(process.stdout)
                good = (process.returncode == 0 and set(document) ==
                        {"case", "code", "cases", "proof", "versions", "failure_type"}
                        and document["case"] == case and document["code"] == "NONE"
                        and type(document["cases"]) is dict and document["cases"] == {case: True}
                        and type(document["proof"]) is dict and set(document["proof"]) == PROOF_KEYS
                        and all(value is True for value in document["proof"].values())
                        and type(document["versions"]) is dict
                        and set(document["versions"]) == {"pg", "django"}
                        and all(type(value) is str and value for value in document["versions"].values()))
                if good:
                    aggregate["versions"][case] = document["versions"]
            except (OSError, subprocess.SubprocessError, ValueError):
                good = False
            aggregate["cases"][case] = bool(good)
            if not good:
                aggregate["code"] = "TEST_FAILED"
    print(json.dumps(aggregate, sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0 if aggregate["code"] == "PASS" else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES)
    arguments = parser.parse_args()
    raise SystemExit(_driver() if arguments.case is None else _run_case(arguments.case))
