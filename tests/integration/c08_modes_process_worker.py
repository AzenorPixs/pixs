"""Travailleur de recette C08 : schema parent, IPC bornee et effets PG reels.

Source TEST_ONLY, sans qualification par sa seule presence. Le parent possede
le schema et verifie les effets par une connexion independante.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import selectors
import stat
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "integration"))
MAX_INPUT = 65536
GO_TIMEOUT = 30
TASK_FIELDS = {"role", "kind", "expected", "key", "operation_id", "correlation_id", "fault"}
FAULT_TABLES = {
    "FAIL_C08": "backend_c08modeoperationreceiptrecord",
    "FAIL_C10": "backend_c10receiptrecord",
    "FAIL_C05": "pixs_core_audit",
}
OUTPUT_FIELDS = {"status", "error_code", "result", "target_constraint_detected", "ready", "cleanup"}


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("INPUT_INVALID")
        result[key] = value
    return result


def _constant(_value):
    raise ValueError("INPUT_INVALID")


def _request(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_INPUT:
        raise ValueError("INPUT_INVALID")
    request = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    if type(request) is not dict or set(request) != {"recipe", "task"}:
        raise ValueError("INPUT_INVALID")
    if type(request["recipe"]) is not dict:
        raise ValueError("INPUT_INVALID")
    task = request["task"]
    if type(task) is not dict or set(task) != TASK_FIELDS:
        raise ValueError("INPUT_INVALID")
    for key in ("role", "kind", "key", "operation_id", "correlation_id", "fault"):
        value = task[key]
        if type(value) is not str or not 0 < len(value) <= 256 or not value.isprintable():
            raise ValueError("INPUT_INVALID")
    if task["role"] not in ("root", "ordinary"):
        raise ValueError("INPUT_INVALID")
    if task["kind"] not in ("FINALIZE_CONFIGURATION", "ENTER_MAINTENANCE"):
        raise ValueError("INPUT_INVALID")
    if task["fault"] not in ("NONE", *FAULT_TABLES):
        raise ValueError("INPUT_INVALID")
    if type(task["expected"]) is not int or not 1 <= task["expected"] <= 2**63 - 1:
        raise ValueError("INPUT_INVALID")
    return request["recipe"], task


def _check_fds(ready, go, owned):
    if (ready is None) != (go is None):
        raise ValueError("INPUT_INVALID")
    if ready is None:
        return
    if ready == go:
        raise ValueError("INPUT_INVALID")
    for descriptor, access in ((ready, os.O_WRONLY), (go, os.O_RDONLY)):
        if type(descriptor) is not int or not 3 <= descriptor <= 2**31 - 1:
            raise ValueError("INPUT_INVALID")
        if not stat.S_ISFIFO(os.fstat(descriptor).st_mode):
            raise ValueError("INPUT_INVALID")
        if fcntl.fcntl(descriptor, fcntl.F_GETFL) & os.O_ACCMODE != access:
            raise ValueError("INPUT_INVALID")
        owned.add(descriptor)


def _rendezvous(ready_fd, go_fd, ready):
    if ready_fd is None:
        return
    message = ("READY %d %d %d\n" % (ready["pid"], ready["schema_oid"], ready["db_oid"])).encode("ascii")
    if os.write(ready_fd, message) != len(message):
        raise RuntimeError("IPC_FAILED")
    deadline = time.monotonic() + GO_TIMEOUT
    with selectors.DefaultSelector() as selector:
        selector.register(go_fd, selectors.EVENT_READ)
        if not selector.select(max(0, deadline - time.monotonic())):
            raise RuntimeError("IPC_FAILED")
        if os.read(go_fd, 1) != b"G":
            raise RuntimeError("IPC_FAILED")


def _constraint_seen(error, name):
    from psycopg.errors import CheckViolation

    pending = [error]
    visited = set()
    while pending:
        current = pending.pop()
        if id(current) in visited:
            continue
        visited.add(id(current))
        if isinstance(current, CheckViolation) and current.diag.constraint_name == name:
            return True
        if isinstance(current, BaseExceptionGroup):
            pending.extend(current.exceptions)
        for other in (current.__cause__, current.__context__):
            if isinstance(other, BaseException):
                pending.append(other)
    return False


def _invoke(fixture, task, namespace):
    from pixs.backend.installation.mode_values import ModeOperationKind
    from pixs.core.dto import CoreMutationResult
    from pixs.core.ports import CorePortError
    from pixs.core.services_common import CoreServiceError
    from django.db import connections
    from psycopg import sql

    kind = {
        "FINALIZE_CONFIGURATION": ModeOperationKind.FINALIZE_CONFIGURATION,
        "ENTER_MAINTENANCE": ModeOperationKind.ENTER_MAINTENANCE,
    }[task["kind"]]
    constraint = None
    if task["fault"] != "NONE":
        constraint = "c08_recipe_" + task["fault"].lower()
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT current_schema()")
            schema = cursor.fetchone()[0]
            import re
            if (type(schema) is not str or schema != namespace
                    or re.fullmatch(r"c08_[0-9a-f]{16}", schema) is None):
                raise RuntimeError("NAMESPACE_UNPROVED")
            cursor.execute(sql.SQL("ALTER TABLE {}.{} ADD CONSTRAINT {} CHECK (FALSE) NOT VALID").format(
                sql.Identifier(schema), sql.Identifier(FAULT_TABLES[task["fault"]]),
                sql.Identifier(constraint)))
    try:
        result = fixture["invoke"](task["role"], kind, task["expected"], task["key"],
                                   task["operation_id"], task["correlation_id"])
    except (CoreServiceError, CorePortError) as error:
        if task["fault"] == "NONE":
            if type(error) is not CoreServiceError or error.code != "IDEMPOTENCE_CONFLIT":
                raise
            return "REJECTED", "IDEMPOTENCE_CONFLIT", None, False
        if constraint is None or not _constraint_seen(error, constraint):
            raise RuntimeError("FAULT_UNPROVED") from None
        if task["fault"] == "FAIL_C05":
            if type(error) is not CoreServiceError or error.code != "AUDIT_REFUS_INDISPONIBLE":
                raise RuntimeError("FAULT_UNPROVED") from None
            return "REJECTED", error.code, None, True
        if task["fault"] == "FAIL_C08":
            if type(error) is not CoreServiceError or error.code != "IDEMPOTENCE_PREUVE_INVALIDE":
                raise RuntimeError("FAULT_UNPROVED") from None
            return "REJECTED", error.code, None, True
        if type(error) is not CorePortError:
            raise RuntimeError("FAULT_UNPROVED") from None
        return "REJECTED", "CORE_PORT_ERROR", None, True
    if task["fault"] != "NONE" or type(result) is not CoreMutationResult:
        raise RuntimeError("RESULT_UNPROVED")
    if type(result.version) is not int or result.version < 1:
        raise RuntimeError("RESULT_UNPROVED")
    public = {key: getattr(result, key) for key in
              ("operation_id", "result_ref", "version", "correlation_id")}
    return "SUCCESS", "NONE", public, False


def main(argv=None):
    import core_pg_test_support as support

    document = {"status": "FAILED", "error_code": "WORKER_FAILED", "result": None,
                "target_constraint_detected": False, "ready": None, "cleanup": False}
    owned = set()
    helper_closed = False
    with support.mask_output():
        try:
            parser = argparse.ArgumentParser(add_help=False, exit_on_error=False)
            parser.add_argument("--worker", action="store_true")
            parser.add_argument("--ready-fd", type=int)
            parser.add_argument("--go-fd", type=int)
            args, unknown = parser.parse_known_args(argv)
            if unknown or not args.worker:
                raise ValueError("INPUT_INVALID")
            _check_fds(args.ready_fd, args.go_fd, owned)
            recipe, task = _request(sys.stdin.buffer.read(MAX_INPUT + 1))
            from c08_modes_worker import open_existing

            with open_existing(recipe) as fixture:
                from django.db import connections

                with connections["default"].cursor() as cursor:
                    cursor.execute("SELECT pg_backend_pid(),"
                                   "(SELECT oid FROM pg_namespace WHERE nspname=current_schema()),"
                                   "(SELECT oid FROM pg_database WHERE datname=current_database())")
                    pid, schema_oid, db_oid = cursor.fetchone()
                if (type(pid) is not int or pid < 1 or schema_oid != recipe["schema_oid"]
                        or db_oid != recipe["db_oid"]):
                    raise RuntimeError("NAMESPACE_UNPROVED")
                ready = {"pid": pid, "schema_oid": schema_oid, "db_oid": db_oid}
                _rendezvous(args.ready_fd, args.go_fd, ready)
                status, error_code, result, proved = _invoke(fixture, task, recipe["namespace"])
                document.update(status=status, error_code=error_code, result=result,
                                target_constraint_detected=proved, ready=ready)
            helper_closed = True
        except Exception:
            # Frontiere de processus : tout echec reste un echec, aucun diagnostic PG transmis.
            document.update(status="FAILED", error_code="WORKER_FAILED", result=None,
                            target_constraint_detected=False)
        finally:
            fds_closed = True
            for descriptor in owned:
                try:
                    os.close(descriptor)
                except OSError:
                    fds_closed = False
            document["cleanup"] = helper_closed and fds_closed
            if not document["cleanup"]:
                document.update(status="FAILED", error_code="WORKER_FAILED", result=None,
                                target_constraint_detected=False)
    assert set(document) == OUTPUT_FIELDS
    print(json.dumps(document, sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0 if document["status"] in ("SUCCESS", "REJECTED") and document["cleanup"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
