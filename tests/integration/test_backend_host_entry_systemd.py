"""Recette fonctionnelle C01 réelle dans UNE unité transitoire.

--system-bench utilise un contrôleur de recette sous sudo pour le bail natif
et cette seule unité système 0593a443 (RuntimeMaxSec45). Le consumer reste
UID1000. Seules les fixtures publiques du banc sont chiffrées.

--plan ne crée rien et ne démarre rien. --execute exige un accord explicite
sur l'infrastructure, représenté par --authorized-user-unit ou
--authorized-system-unit selon le manager. Cet accord est
contrôlé par l'orchestrateur avant le mandat ; le drapeau ne le remplace pas.
Fixtures PUBLIQUES, chiffrement null : aucune confidentialité cryptographique,
connexion PostgreSQL, santé Auth ou qualification P0 n'est démontrée ici.
Aucun opaque C01 forgé. Aucun service existant, OpenCode ou CAB modifié.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import time
import traceback

ROOT = Path("/home/devops/datas/pixs")
BASE = ROOT / "output/cismp/cismp4-pixs-04b6968c4b2249d8/entry-systemd"
SYSTEM_BASE = BASE.with_name("entry-systemd-system-journal")
BENCH_UID = 1000
SELF = ROOT / "tests/integration/test_backend_host_entry_systemd.py"
PYTHON = ROOT / ".venv/bin/python3"
UNIT_RE = re.compile(r"pixs-c07-c4-entry-([0-9a-f]{8})\.service")
PUBLIC = {"key": "synth-c07-key-public", "pwd": "synth-c07-password-public"}
PROPERTIES = ("RuntimeMaxSec=45s", "TimeoutStopSec=2s", "TimeoutStopFailureMode=kill",
              "RuntimeRandomizedExtraSec=0", "Restart=no", "KillMode=control-group", "SendSIGKILL=yes")
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]


class BenchError(ValueError):
    pass


def checked(args):
    match = UNIT_RE.fullmatch(args.unit)
    if match is None:
        raise BenchError("UNIT_INVALID")
    nonce = match.group(1)
    if args.system_bench and (nonce != "0593a443" or os.getuid() != os.geteuid() or os.getuid() not in (0, BENCH_UID)):
        raise BenchError("SYSTEM_BENCH_SCOPE_INVALID")
    case = (SYSTEM_BASE if args.system_bench else BASE) / nonce
    if args.case != str(case):
        raise BenchError("CASE_INVALID")
    current = Path("/")
    for part in case.parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise BenchError("CASE_ANCESTOR_INVALID")
    return nonce, case


def environment():
    runtime = "/run/user/" + str(os.getuid())
    return {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1", "XDG_RUNTIME_DIR": runtime,
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=" + runtime + "/bus"}


def command(argv, timeout=10, data=None):
    if type(argv) is not list or not argv or any(type(arg) is not str or "\x00" in arg for arg in argv):
        raise BenchError("COMMAND_INVALID")
    if not argv[0].startswith("/"):
        raise BenchError("COMMAND_NOT_ABSOLUTE")
    return subprocess.run(argv, input=data, capture_output=True, timeout=timeout,
                          env=environment(), check=False)


def error_data(error):
    return {"type": type(error).__name__, "frames": [
        {"file": Path(frame.filename).name, "line": frame.lineno, "func": frame.name}
        for frame in traceback.extract_tb(error.__traceback__)[-12:]]}


def owned_directory(path):
    metadata = path.lstat()
    if (not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != BENCH_UID
            or stat.S_IMODE(metadata.st_mode) != 0o700):
        raise BenchError("DIRECTORY_OWNERSHIP_INVALID")


def publish(path, data):
    owned_directory(path.parent)
    if path.exists() or path.is_symlink() or len(data) > 65536:
        raise BenchError("PUBLICATION_INVALID")
    temporary = path.with_name(path.name + ".tmp-" + str(os.getpid()))
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        if os.geteuid() == 0:
            os.fchown(fd, BENCH_UID, -1)
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written < 1:
                raise BenchError("WRITE_INCOMPLETE")
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temporary, path)
    parent_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def publish_json(path, payload):
    publish(path, (json.dumps(payload, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n").encode("utf-8"))


def read_json(path):
    owned_directory(path.parent)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        metadata = os.fstat(fd)
        if (not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != BENCH_UID
                or stat.S_IMODE(metadata.st_mode) != 0o600 or metadata.st_size > 65536):
            raise BenchError("FILE_OWNERSHIP_INVALID")
        raw = b""
        while len(raw) <= 65536:
            chunk = os.read(fd, min(8192, 65537 - len(raw)))
            if not chunk:
                break
            raw += chunk
        if len(raw) > 65536:
            raise BenchError("FILE_TOO_LARGE")
    finally:
        os.close(fd)
    payload = json.loads(raw.decode("utf-8"))
    if type(payload) is not dict:
        raise BenchError("JSON_OBJECT_REQUIRED")
    return payload


def wait_json(path, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            return read_json(path)
        except FileNotFoundError:
            time.sleep(0.1)
    raise BenchError("HANDSHAKE_TIMEOUT")


def properties(unit, system_bench=False):
    result = command(["/usr/bin/systemctl", "--system" if system_bench else "--user", "show", "--no-pager",
        "--property=LoadState,Transient,Description,MainPID,ActiveState", "--", unit])
    if len(result.stdout) > 16384:
        raise BenchError("UNIT_METADATA_TOO_LARGE")
    rows = {}
    for line in result.stdout.decode("utf-8").splitlines():
        key, separator, value = line.partition("=")
        if not separator or key not in ("LoadState", "Transient", "Description", "MainPID", "ActiveState") or key in rows:
            raise BenchError("UNIT_METADATA_INVALID")
        rows[key] = value
    if not rows or "LoadState" not in rows:
        raise BenchError("UNIT_METADATA_UNAVAILABLE")
    return rows


def start_command(unit, case, description, system_bench=False):
    prefix = []
    identity = ["--property=User=1000", "--property=NoNewPrivileges=yes", "--property=UMask=0077"] if system_bench else []
    consumer = ["--system-bench"] if system_bench else []
    return prefix + ["/usr/bin/systemd-run", "--system" if system_bench else "--user", "--no-ask-password", "--unit=" + unit,
        "--description=" + description, "--service-type=exec", "--working-directory=" + str(ROOT),
        *["--property=" + item for item in PROPERTIES], *identity,
        "--property=LoadCredentialEncrypted=key:" + str(case / "key.cred"),
        "--property=LoadCredentialEncrypted=pwd:" + str(case / "pwd.cred"),
        "--", str(PYTHON), "-B", str(SELF), "--consumer", "--unit", unit, "--case", str(case), *consumer]


def plan(args):
    nonce, case = checked(args)
    tools = {name: Path("/usr/bin", name).is_file() and os.access(Path("/usr/bin", name), os.X_OK) for name in
             ("systemctl", "systemd-run", "systemd-creds", "busctl")}
    manager = command(["/usr/bin/systemctl", "--system" if args.system_bench else "--user", "show", "--property=Version", "--value"])
    manager_available = manager.returncode == 0
    unit_available = properties(args.unit, args.system_bench).get("LoadState") == "not-found" if manager_available else False
    print(json.dumps({"mode": "plan", "effect": "none", "unit": args.unit, "case": str(case),
        "uid": os.getuid(), "manager": "system" if args.system_bench else "user", "manager_available": manager_available,
        "controller_uid": 0 if args.system_bench else BENCH_UID, "consumer_uid": BENCH_UID,
        "tools": tools, "case_absent": not case.exists(), "unit_available": unit_available,
        "command": start_command(args.unit, case, "Pixs C07 entry " + nonce, args.system_bench),
        "public_fixtures": True, "encryption": "null-functional-only", "root": os.geteuid() == 0,
        "real_postgresql": False, "p0_qualified": False, "execute_authorized": False}, ensure_ascii=False), flush=True)
    return 0 if manager_available and unit_available and all(tools.values()) and not case.exists() and os.getuid() == os.geteuid() and os.getuid() > 0 else 2


def execute(args):
    from pixs.backend.systemd_secret_provider import native as native
    authorized = args.authorized_system_unit if args.system_bench else args.authorized_user_unit
    valid_identity = (os.getuid() == os.geteuid() == 0) if args.system_bench else (os.getuid() == os.geteuid() == BENCH_UID)
    if not authorized or not valid_identity:
        raise BenchError("UNIT_APPROVAL_OR_IDENTITY_INVALID")
    nonce, case = checked(args)
    manager = command(["/usr/bin/systemctl", "--system" if args.system_bench else "--user", "show", "--property=Version", "--value"])
    if manager.returncode != 0 or case.exists():
        raise BenchError("PRECONDITION_FAILED")
    before = properties(args.unit, args.system_bench)
    if before.get("LoadState") != "not-found":
        raise BenchError("UNIT_ALREADY_EXISTS")
    base = case.parent
    if base.exists():
        owned_directory(base)
    else:
        base.mkdir(mode=0o700)
        if os.geteuid() == 0:
            os.chown(base, BENCH_UID, -1)
        os.chmod(base, 0o700)
    case.mkdir(mode=0o700)
    if os.geteuid() == 0:
        os.chown(case, BENCH_UID, -1)
    os.chmod(case, 0o700)
    (case / "journal").mkdir(mode=0o700)
    if os.geteuid() == 0:
        os.chown(case / "journal", BENCH_UID, -1)
    os.chmod(case / "journal", 0o700)
    manager_name = "system" if args.system_bench else "user"
    description = "Pixs C07 entry " + nonce
    attempted, owned, cleanup = False, False, False
    lease, snapshot, result, failure = None, None, None, None
    lease_held = False
    checks = {}
    def interrupt(signum, frame):
        raise InterruptedError("INTERRUPTED")
    old_term = signal.signal(signal.SIGTERM, interrupt)
    try:
        for name, value in PUBLIC.items():
            blob = json.dumps({"schema_version": 1, "credential_version": "v1", "value": value}).encode("utf-8")
            if args.system_bench:
                encrypted = command(["/usr/bin/systemd-creds", "encrypt",
                    "--with-key=null", "--name=" + name, "-", "-"], data=blob)
                if encrypted.returncode == 0:
                    publish(case / (name + ".cred"), encrypted.stdout)
            else:
                encrypted = command(["/usr/bin/systemd-creds", "encrypt", "--with-key=null",
                    "--name=" + name, "-", str(case / (name + ".cred"))], data=blob)
            if encrypted.returncode != 0:
                raise BenchError("PUBLIC_CREDENTIAL_FIXTURE_FAILED")
            os.chmod(case / (name + ".cred"), 0o600)
        attempted = True
        started = command(start_command(args.unit, case, description, args.system_bench))
        current = properties(args.unit, args.system_bench)
        owned = current.get("Description") == description and current.get("Transient") == "yes"
        if not owned or started.returncode != 0:
            raise BenchError("OWNED_START_NOT_PROVED")
        lease = native.unit_lease(manager=manager_name, unit=args.unit, timeout_s=10, uid=BENCH_UID)
        lease.__enter__()
        lease_held = True
        snapshot = native.snapshot_service(manager=manager_name, unit=args.unit, timeout_s=10, uid=BENCH_UID)
        ready = wait_json(case / "ready.json", 15)
        if (ready.get("unit") != args.unit or ready.get("nonce") != nonce
                or ready.get("uid") != BENCH_UID or ready.get("pid") != snapshot.main_pid
                or ready.get("invocation") != snapshot.invocation_hex
                or ready.get("control_group") != snapshot.control_group or ready.get("native_self") is not True):
            raise BenchError("NATIVE_HANDSHAKE_MISMATCH")
        mapping = {name: str(case / (name + ".cred")) for name in PUBLIC}
        native.check_loaded_gate(snapshot, max_ttl_s=300, max_revocation_delay_s=60,
            budget_stop_s=2, policy_mapping=mapping, remaining_validity_s=150)
        checks["loaded_gate"] = True
        checks["native_self"] = True
        publish_json(case / "go.json", {"unit": args.unit, "nonce": nonce, "go": True})
        result = wait_json(case / "result.json", 20)
        if (result.get("unit") != args.unit or result.get("nonce") != nonce
                or result.get("ok") is not True or type(result.get("checks")) is not dict
                or not result["checks"] or not all(type(value) is bool and value for value in result["checks"].values())):
            raise BenchError("CONSUMER_RECIPE_FAILED")
        checks.update(result["checks"])
    except BaseException as error:
        failure = error_data(error)
    finally:
        if attempted:
            try:
                current = properties(args.unit, args.system_bench)
                owned = current.get("Description") == description and current.get("Transient") == "yes"
                if not owned:
                    raise BenchError("CLEANUP_OWNERSHIP_UNPROVED")
                live = native.snapshot_service(manager=manager_name, unit=args.unit, timeout_s=10, uid=BENCH_UID)
                if snapshot is None:
                    snapshot = live
                elif live.invocation_hex not in (snapshot.invocation_hex, "0" * 32):
                    raise BenchError("CLEANUP_INVOCATION_CHANGED")
                native.systemctl_stop(manager=manager_name, unit=args.unit, timeout_s=10, uid=BENCH_UID)
                stopped = native.attest_stopped(manager=manager_name, unit=args.unit,
                    old_control_group=snapshot.control_group, old_invocation_hex=snapshot.invocation_hex,
                    timeout_s=10, uid=BENCH_UID)
                cleanup = stopped.main_pid == 0 and stopped.unit == args.unit
                checks["unit_quiescent"] = cleanup
            except BaseException as error:
                checks["unit_quiescent"] = False
                if failure is None:
                    failure = error_data(error)
        else:
            cleanup = True
        if lease_held:
            try:
                lease.__exit__(None, None, None)
            except BaseException as error:
                if failure is None:
                    failure = error_data(error)
        signal.signal(signal.SIGTERM, old_term)
    receipt = {"mode": "execute", "unit": args.unit, "uid": os.getuid(), "manager": manager_name,
        "invocation": snapshot.invocation_hex if snapshot is not None else None,
        "checks": checks, "cleanup": cleanup, "artifacts_preserved": True,
        "case": str(case), "public_fixtures": True, "encryption": "null-functional-only",
        "real_postgresql": False, "p0_qualified": False, "error": failure,
        "versions": result.get("versions") if type(result) is dict else None}
    publish_json(case / "parent-result.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    return 0 if failure is None and cleanup and checks and all(checks.values()) else 1


def consumer(args):
    import asyncio
    import platform
    from pixs.backend.bootstrap_audit import generate_uuidv7, init_journal, read_open_records
    from pixs.backend.bootstrap_policy import C01Policy, CredentialBinding, PolicySource, render_c01_policy, load_c01_policy
    from pixs.backend.host_entry import build_installer_host
    from pixs.backend.host_plan import prepare_host_plan
    from pixs.backend.http_route_guard import RouteDeclaration
    from pixs.backend.liveness_view import liveness_view
    from pixs.backend.settings import build_settings_template
    from pixs.backend.startup_mode import StartupMode
    from pixs.backend.systemd_secret_provider import native
    from pixs.kernel.config.resolution import SecretReference
    from tests.unit.test_backend_host_plan import texts, SyntheticProofPort
    from tests.unit.test_backend_host_runtime import ready_adapters
    nonce, case = checked(args)
    owned_directory(case)
    uid = os.getuid()
    if uid != BENCH_UID or os.geteuid() != BENCH_UID:
        raise BenchError("CONSUMER_UID_INVALID")
    manager_name = "system" if args.system_bench else "user"
    proof = native.prove_self(manager=manager_name, expect_uid=uid, expect_unit=args.unit)
    snapshot = native.snapshot_service(manager=manager_name, unit=args.unit, timeout_s=10, uid=uid)
    if snapshot.main_pid != os.getpid():
        raise BenchError("CONSUMER_MAIN_PID_MISMATCH")
    publish_json(case / "ready.json", {"unit": args.unit, "nonce": nonce, "uid": uid,
        "pid": snapshot.main_pid, "invocation": snapshot.invocation_hex,
        "control_group": snapshot.control_group,
        "native_self": proof.uid == uid and proof.unit == args.unit and proof.manager == manager_name})
    checks, failure = {}, None
    try:
        go = wait_json(case / "go.json", 20)
        if go != {"unit": args.unit, "nonce": nonce, "go": True}:
            raise BenchError("GO_MISMATCH")
        now = datetime.now(timezone.utc)
        begin, end = (now - timedelta(seconds=1)).isoformat(), (now + timedelta(seconds=180)).isoformat()
        references = tuple(SecretReference("pixs.backend", entry, "systemd:c07:" + name)
            for name, entry in (("key", "django_secret_key"), ("pwd", "db_password")))
        bindings = tuple(CredentialBinding(reference, name, "v1", begin, end, str(case / (name + ".cred")))
                         for reference, name in zip(references, ("key", "pwd")))
        credential_dir = os.environ.get("CREDENTIALS_DIRECTORY")
        if type(credential_dir) is not str or not credential_dir:
            raise BenchError("CREDENTIAL_DIRECTORY_MISSING")
        policy = C01Policy(policy_id="c07-entry-" + nonce, policy_version="1", uid=uid,
            unit=args.unit, manager=manager_name, role="web", purpose="c07-entry-native",
            credential_dir=credential_dir, bindings=bindings, valid_from=begin, valid_until=end,
            max_event_bytes=8192, max_journal_bytes=1048576, max_credential_bytes=4096,
            max_ttl_s=300, max_revocation_delay_s=60, max_stop_budget_s=2, max_restart_budget_s=15,
            journal_dir=str(case / "journal"), journal_uid=uid, journal_id=generate_uuidv7(),
            retention_days=1, scope_literal="PLATFORM", controller_uid=uid,
            controller_unit="pixs-c07-c4-controller-" + nonce + ".service", holds=(),
            allowed_actions=("resolve",), revoked_versions=())
        init_journal(journal_dir=policy.journal_dir, journal_uid=uid, journal_id=policy.journal_id,
            retention_days=policy.retention_days, holds=policy.holds)
        initial_records = read_open_records(journal_dir=policy.journal_dir, journal_uid=uid,
            journal_id=policy.journal_id, max_journal_bytes=policy.max_journal_bytes, max_event_bytes=policy.max_event_bytes)
        checks["journal_initialized"] = initial_records == ()
        publish(case / "policy.toml", render_c01_policy(policy).encode("utf-8"))
        policy_source = PolicySource(str(case / "policy.toml"), uid, policy.policy_id, 16384)
        checks["policy_loaded"] = load_c01_policy(policy_source) == policy
        source_texts = texts()
        required = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt")
        prepared = prepare_host_plan(manifest_texts=source_texts, official_ids=required,
            required_ids=required, attestation_port=SyntheticProofPort(source_texts))
        template = build_settings_template(profile="web",
            database={"name": "c07_fixture", "user": "c07_fixture", "host": "127.0.0.1", "port": 1},
            allowed_hosts=["testserver"], secret_key_ref=references[0], database_password_ref=references[1])
        private_calls = []
        def private_handler(request):
            private_calls.append(True)
            raise BenchError("PRIVATE_HANDLER_REACHED")
        host = build_installer_host(template,
            policy_source,
            StartupMode.INSTALLER, "c07-entry-native", prepared,
            lambda selected: ready_adapters(selected, hooks=False),
            RouteDeclaration("health/live", "c07-live", liveness_view, True),
            (RouteDeclaration("private/", "c07-private", private_handler, False),))
        checks["real_c01_entry_constructed"] = host.phase == "NEW"
        async def exercise():
            from asgiref.testing import ApplicationCommunicator
            async def request(path, method="GET", headers=((b"host", b"testserver"),)):
                scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
                    "method": method, "scheme": "http", "server": ("testserver", 80),
                    "client": ("127.0.0.1", 1234), "path": path, "raw_path": path.encode("ascii"),
                    "query_string": b"", "headers": list(headers)}
                connection = ApplicationCommunicator(host, scope)
                await connection.send_input({"type": "http.request", "body": b"", "more_body": False})
                start = await connection.receive_output(5)
                body = await connection.receive_output(5)
                await connection.wait(5)
                return start["status"], body.get("body", b"")
            life = ApplicationCommunicator(host, {"type": "lifespan", "asgi": {"version": "3.0"}})
            await life.send_input({"type": "lifespan.startup"})
            started = await life.receive_output(10)
            if started.get("type") != "lifespan.startup.complete":
                await life.wait(5)
                raise BenchError("LIFESPAN_START_FAILED")
            try:
                checks["runtime_context_active"] = host.context.plan is prepared
                checks["liveness_get"] = await request("/health/live") == (200, b"")
                checks["liveness_head"] = await request("/health/live", "HEAD") == (200, b"")
                checks["liveness_post"] = await request("/health/live", "POST") == (405, b"")
                checks["private_closed"] = (await request("/private/"))[0] == 403 and not private_calls
                checks["unknown_closed"] = (await request("/unknown/"))[0] == 404
                checks["host_closed"] = (await request("/health/live", headers=((b"host", b"evil.example"),)))[0] == 400
                checks["origin_closed"] = (await request("/health/live", headers=((b"host", b"testserver"),
                    (b"origin", b"https://evil.example"))))[0] == 403
            finally:
                await life.send_input({"type": "lifespan.shutdown"})
                stopped = await life.receive_output(10)
                await life.wait(5)
                checks["lifespan_stopped"] = stopped.get("type") == "lifespan.shutdown.complete" and host.phase == "STOPPED"
        asyncio.run(exercise())
        records = read_open_records(journal_dir=policy.journal_dir, journal_uid=uid,
            journal_id=policy.journal_id, max_journal_bytes=policy.max_journal_bytes, max_event_bytes=policy.max_event_bytes)
        actions = [record.event.action for record in records]
        checks["c01_audit_confirmed"] = len(actions) == 4 and actions.count("secret.resolve") == 2 and actions.count("secret.resolve.consume") == 2
        from django.db import connections
        checks["no_database_connection"] = all(connection.connection is None for connection in connections.all())
    except BaseException as error:
        failure = error_data(error)
    import django
    payload = {"unit": args.unit, "nonce": nonce, "ok": failure is None and bool(checks) and all(checks.values()),
        "checks": checks, "error": failure,
        "versions": {"python": platform.python_version(), "django": django.get_version()}}
    publish_json(case / "result.json", payload)
    # Le parent atteste ensuite l'arrêt de ce seul processus devenu inactif.
    time.sleep(25)
    return 0 if payload["ok"] else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--case", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--consumer", action="store_true")
    parser.add_argument("--authorized-user-unit", action="store_true")
    parser.add_argument("--system-bench", action="store_true")
    parser.add_argument("--authorized-system-unit", action="store_true")
    args = parser.parse_args()
    if args.consumer:
        return consumer(args)
    if args.execute:
        return execute(args)
    return plan(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"ok": False, "error": error_data(error), "cleanup": False}, ensure_ascii=False), flush=True)
        raise SystemExit(1)
