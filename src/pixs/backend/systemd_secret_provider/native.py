"""Acces natif systemd, sans mutation pendant ce job.

Preuve propre via libsystemd, busctl borne type, snapshot ferme,
gate de vie chargee, helpers systemctl natifs pour lifecycle futur.
Stdlib seule, import pur, Python>=3.12.
"""
from __future__ import annotations
import ctypes
import json
import os
import re
import stat
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass
__all__ = ["ServiceSnapshot", "StoppedProof", "attest_stopped", "check_loaded_gate", "get_unit_path", "prove_self", "snapshot_service", "systemctl_start", "systemctl_stop", "unit_lease"]
_BUSCTL = "/usr/bin/busctl"
_SYSTEMCTL = "/usr/bin/systemctl"
_MAX_BUSCTL_BYTES = 65536
_UNIT_RE = re.compile(r"[A-Za-z0-9_@.:-]+\.service")
def _refus() -> ValueError:
    return ValueError("systemd natif refuse")
@contextmanager
def _closing_fd(fd: int):
    try:
        yield fd
    finally:
        os.close(fd)
def _exige_timeout(v: object) -> int:
    if type(v) is not int or isinstance(v, bool) or v < 1:
        raise _refus() from None
    return v
def _exige_manager(v: object) -> str:
    if type(v) is not str:
        raise _refus() from None
    if v not in ("system", "user"):
        raise _refus() from None
    return v
def _exige_unit(v: object) -> str:
    if type(v) is not str or not v:
        raise _refus() from None
    if "/" in v or v.startswith(("-", ".")) or not v.endswith(".service"):
        raise _refus() from None
    if _UNIT_RE.fullmatch(v) is None:
        raise _refus() from None
    if "*" in v or "?" in v or "[" in v:
        raise _refus() from None
    return v
@dataclass(frozen=True)
class SelfProof:
    uid: int
    unit: str
    manager: str
def prove_self(*, manager: str, expect_uid: int, expect_unit: str) -> SelfProof:
    _exige_manager(manager)
    _exige_unit(expect_unit)
    if type(expect_uid) is not int or isinstance(expect_uid, bool) or expect_uid < 0:
        raise _refus() from None
    uid = os.getuid()
    euid = os.geteuid()
    if uid != expect_uid or euid != expect_uid:
        raise _refus() from None
    try:
        lib = ctypes.CDLL("libsystemd.so.0")
    except OSError:
        raise _refus() from None
    out = ctypes.c_char_p(None)
    try:
        fn = getattr(lib, "sd_pid_get_user_unit" if manager == "user" else "sd_pid_get_unit", None)
        if fn is None:
            raise _refus() from None
        fn.restype = ctypes.c_int
        fn.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
        rc = fn(0, ctypes.byref(out))
    except OSError:
        raise _refus() from None
    if rc < 0 or not out:
        raise _refus() from None
    try:
        actual = ctypes.string_at(out).decode("utf-8")
    except UnicodeError:
        raise _refus() from None
    finally:
        try:
            libc = ctypes.CDLL(None)
            libc.free.restype = None
            libc.free.argtypes = [ctypes.c_void_p]
            libc.free(out)
        except OSError:
            raise _refus() from None
    if actual != expect_unit:
        raise _refus() from None
    return SelfProof(uid=uid, unit=actual, manager=manager)
def _user_runtime_dir(uid: int) -> str:
    if type(uid) is not int or isinstance(uid, bool) or uid < 0:
        raise _refus() from None
    return "/run/user/" + str(uid)
def _check_user_bus_dir(uid: int) -> str:
    base = _user_runtime_dir(uid)
    try:
        dfd = os.open(base, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError:
        raise _refus() from None
    try:
        st = os.fstat(dfd)
        if not stat.S_ISDIR(st.st_mode) or st.st_uid != uid or (st.st_mode & 0o777) != 0o700:
            raise _refus() from None
    finally:
        os.close(dfd)
    sock = base + "/bus"
    try:
        sst = os.lstat(sock)
    except OSError:
        raise _refus() from None
    if stat.S_ISLNK(sst.st_mode):
        raise _refus() from None
    if not stat.S_ISSOCK(sst.st_mode):
        raise _refus() from None
    if sst.st_uid != uid:
        raise _refus() from None
    return base
def _no_dup_object(pairs: list) -> dict:
    out: dict = {}
    seen: set = set()
    for k, v in pairs:
        if k in seen:
            raise _refus() from None
        seen.add(k)
        out[k] = v
    return out
def _check_scalar(typ: str, data: object) -> None:
    if typ == "s" or typ == "o":
        if type(data) is not str:
            raise _refus() from None
    elif typ == "t":
        if type(data) is not int or isinstance(data, bool) or data < 0 or data > (1 << 64) - 1:
            raise _refus() from None
    elif typ == "u":
        if type(data) is not int or isinstance(data, bool) or data < 0 or data > (1 << 32) - 1:
            raise _refus() from None
    elif typ == "b":
        if type(data) is not bool:
            raise _refus() from None
    else:
        raise _refus() from None
def _run_busctl(*, manager: str, args: list, timeout_s: int, uid: int) -> list:
    _exige_manager(manager)
    _exige_timeout(timeout_s)
    if type(args) is not list or not args or not all(type(a) is str and a for a in args):
        raise _refus() from None
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    if manager == "user":
        base = _check_user_bus_dir(uid)
        env["XDG_RUNTIME_DIR"] = base
    cmd = [_BUSCTL]
    cmd.append("--user" if manager == "user" else "--system")
    cmd.extend(["--json=short", "--no-pager", "--allow-interactive-authorization=no", "--auto-start=no"])
    cmd.extend(args)
    if len(cmd) > 24:
        raise _refus() from None
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s, env=env)
    except OSError:
        raise _refus() from None
    except subprocess.SubprocessError:
        raise _refus() from None
    if proc.returncode != 0 or not proc.stdout or len(proc.stdout) > _MAX_BUSCTL_BYTES:
        raise _refus() from None
    objs: list = []
    for raw in proc.stdout.splitlines():
        if not raw.strip():
            raise _refus() from None
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise _refus() from None
        try:
            obj = json.loads(text, object_pairs_hook=_no_dup_object)
        except ValueError:
            raise _refus() from None
        if type(obj) is not dict or set(obj.keys()) != {"type", "data"}:
            raise _refus() from None
        objs.append(obj)
    if not objs:
        raise _refus() from None
    return objs
def get_unit_path(*, manager: str, unit: str, timeout_s: int, uid: int) -> str:
    _exige_manager(manager)
    _exige_unit(unit)
    objs = _run_busctl(manager=manager, args=["call", "org.freedesktop.systemd1", "/org/freedesktop/systemd1", "org.freedesktop.systemd1.Manager", "GetUnit", "s", unit], timeout_s=timeout_s, uid=uid)
    if len(objs) != 1 or objs[0]["type"] != "o":
        raise _refus() from None
    values = objs[0]["data"]
    if type(values) is not list or len(values) != 1 or type(values[0]) is not str:
        raise _refus() from None
    path = values[0]
    if not path.startswith("/org/freedesktop/systemd1/unit/") or re.fullmatch(r"/[A-Za-z0-9_/]+", path) is None:
        raise _refus() from None
    return path
_ALLOWED_GET = {"ActiveState": "s", "SubState": "s", "ControlGroup": "s", "InvocationID": "ay", "ActiveEnterTimestampMonotonic": "t", "MainPID": "u", "Type": "s", "RuntimeMaxUSec": "t", "RuntimeRandomizedExtraUSec": "t", "TimeoutStopUSec": "t", "TimeoutStopFailureMode": "s", "KillMode": "s", "SendSIGKILL": "b", "Restart": "s", "LoadCredentialEncrypted": "a(ss)", "LoadCredential": "a(ss)", "SetCredential": "a(say)", "SetCredentialEncrypted": "a(say)", "ImportCredential": "as", "ImportCredentialEx": "a(ss)", "ExecStop": "a(sasbttttuii)", "ExecStopPost": "a(sasbttttuii)"}
def _get_props(*, manager: str, object_path: str, interface: str, names: tuple, timeout_s: int, uid: int) -> dict:
    if not object_path.startswith("/org/freedesktop/systemd1/"):
        raise _refus() from None
    if interface not in ("org.freedesktop.systemd1.Unit", "org.freedesktop.systemd1.Service"):
        raise _refus() from None
    if type(names) is not tuple or not names:
        raise _refus() from None
    for n in names:
        if n not in _ALLOWED_GET:
            raise _refus() from None
    args = ["get-property", "org.freedesktop.systemd1", object_path, interface] + list(names)
    objs = _run_busctl(manager=manager, args=args, timeout_s=timeout_s, uid=uid)
    if len(objs) != len(names):
        raise _refus() from None
    out: dict = {}
    for name, obj in zip(names, objs):
        exp = _ALLOWED_GET[name]
        if obj["type"] != exp:
            raise _refus() from None
        d = obj["data"]
        if exp in ("s", "o"):
            _check_scalar(exp, d)
        elif exp in ("t", "u"):
            _check_scalar(exp, d)
        elif exp == "b":
            _check_scalar(exp, d)
        elif exp == "ay":
            if type(d) is not list or len(d) != 16:
                raise _refus() from None
            for b in d:
                if type(b) is not int or isinstance(b, bool) or b < 0 or b > 255:
                    raise _refus() from None
        elif exp == "a(ss)":
            if type(d) is not list:
                raise _refus() from None
            for item in d:
                if type(item) is not list or len(item) != 2 or not all(type(x) is str for x in item):
                    raise _refus() from None
        elif exp in ("a(say)", "as", "a(sasbttttuii)"):
            if type(d) is not list:
                raise _refus() from None
        else:
            raise _refus() from None
        out[name] = d
    return out
@dataclass(frozen=True)
class ServiceSnapshot:
    unit: str
    object_path: str
    active_state: str
    sub_state: str
    control_group: str
    invocation_hex: str
    active_enter_monotonic: int
    main_pid: int
    svc_type: str
    runtime_max_usec: int
    runtime_randomized_extra_usec: int
    timeout_stop_usec: int
    timeout_stop_failure_mode: str
    kill_mode: str
    send_sigkill: bool
    restart: str
    load_credential_encrypted: tuple
    fallback_counts: tuple
    exec_stop_count: int
    exec_stop_post_count: int
def _ay_to_hex(v: object) -> str:
    if type(v) is not list or len(v) != 16:
        raise _refus() from None
    for b in v:
        if type(b) is not int or isinstance(b, bool) or b < 0 or b > 255:
            raise _refus() from None
    return "".join("%02x" % b for b in v)
def _remaining_or_refuse(deadline_ns: int) -> int:
    try:
        now = time.monotonic_ns()
    except OSError:
        raise _refus() from None
    if deadline_ns <= now:
        raise _refus() from None
    return (deadline_ns - now) // 1_000_000_000 + 1
def snapshot_service(*, manager: str, unit: str, timeout_s: int, uid: int) -> ServiceSnapshot:
    _exige_manager(manager)
    _exige_unit(unit)
    _exige_timeout(timeout_s)
    try:
        deadline = time.monotonic_ns() + timeout_s * 1_000_000_000
    except OSError:
        raise _refus() from None
    path = get_unit_path(manager=manager, unit=unit, timeout_s=_remaining_or_refuse(deadline), uid=uid)
    u1 = _get_props(manager=manager, object_path=path, interface="org.freedesktop.systemd1.Unit", names=("ActiveState", "SubState", "InvocationID", "ActiveEnterTimestampMonotonic"), timeout_s=_remaining_or_refuse(deadline), uid=uid)
    s1 = _get_props(manager=manager, object_path=path, interface="org.freedesktop.systemd1.Service", names=("ControlGroup", "MainPID", "Type", "RuntimeMaxUSec", "RuntimeRandomizedExtraUSec", "TimeoutStopUSec", "TimeoutStopFailureMode", "KillMode", "SendSIGKILL", "Restart", "LoadCredentialEncrypted"), timeout_s=_remaining_or_refuse(deadline), uid=uid)
    fb = _get_props(manager=manager, object_path=path, interface="org.freedesktop.systemd1.Service", names=("LoadCredential", "SetCredential", "SetCredentialEncrypted", "ImportCredential", "ImportCredentialEx"), timeout_s=_remaining_or_refuse(deadline), uid=uid)
    for k in ("LoadCredential", "SetCredential", "SetCredentialEncrypted", "ImportCredential", "ImportCredentialEx"):
        if type(fb[k]) is not list or len(fb[k]) != 0:
            raise _refus() from None
    cnt = _get_props(manager=manager, object_path=path, interface="org.freedesktop.systemd1.Service", names=("ExecStop", "ExecStopPost"), timeout_s=_remaining_or_refuse(deadline), uid=uid)
    u2 = _get_props(manager=manager, object_path=path, interface="org.freedesktop.systemd1.Unit", names=("InvocationID",), timeout_s=_remaining_or_refuse(deadline), uid=uid)
    _remaining_or_refuse(deadline)
    if u1["InvocationID"] != u2["InvocationID"]:
        raise _refus() from None
    creds = s1["LoadCredentialEncrypted"]
    pairs: list = []
    for item in creds:
        pairs.append((item[0], item[1]))
    if len(pairs) != 2:
        raise _refus() from None
    if pairs[0][0] == pairs[1][0]:
        raise _refus() from None
    return ServiceSnapshot(unit=unit, object_path=path, active_state=u1["ActiveState"], sub_state=u1["SubState"], control_group=s1["ControlGroup"], invocation_hex=_ay_to_hex(u1["InvocationID"]), active_enter_monotonic=u1["ActiveEnterTimestampMonotonic"], main_pid=s1["MainPID"], svc_type=s1["Type"], runtime_max_usec=s1["RuntimeMaxUSec"], runtime_randomized_extra_usec=s1["RuntimeRandomizedExtraUSec"], timeout_stop_usec=s1["TimeoutStopUSec"], timeout_stop_failure_mode=s1["TimeoutStopFailureMode"], kill_mode=s1["KillMode"], send_sigkill=s1["SendSIGKILL"], restart=s1["Restart"], load_credential_encrypted=tuple(pairs), fallback_counts=(0, 0, 0, 0, 0), exec_stop_count=len(cnt["ExecStop"]), exec_stop_post_count=len(cnt["ExecStopPost"]))
def check_loaded_gate(snap: ServiceSnapshot, *, max_ttl_s: int, max_revocation_delay_s: int, budget_stop_s: int, policy_mapping: dict, remaining_validity_s: int) -> None:
    if type(snap) is not ServiceSnapshot:
        raise _refus() from None
    for v in (max_ttl_s, max_revocation_delay_s, budget_stop_s, remaining_validity_s):
        if type(v) is not int or isinstance(v, bool) or v < 1:
            raise _refus() from None
    if type(snap.main_pid) is not int or isinstance(snap.main_pid, bool) or snap.main_pid <= 0:
        raise _refus() from None
    if type(snap.send_sigkill) is not bool:
        raise _refus() from None
    for f in (snap.runtime_max_usec, snap.timeout_stop_usec, snap.active_enter_monotonic):
        if type(f) is not int or isinstance(f, bool) or f <= 0:
            raise _refus() from None
    if type(snap.invocation_hex) is not str or len(snap.invocation_hex) != 32 or set(snap.invocation_hex) == {"0"}:
        raise _refus() from None
    if snap.active_state != "active" or snap.sub_state != "running":
        raise _refus() from None
    if snap.svc_type != "exec":
        raise _refus() from None
    inf = (1 << 64) - 1
    if snap.runtime_max_usec == inf or snap.active_enter_monotonic == inf:
        raise _refus() from None
    cap = min(max_ttl_s, max_revocation_delay_s) - budget_stop_s
    if cap < 1 or snap.runtime_max_usec > cap * 1_000_000:
        raise _refus() from None
    if snap.runtime_randomized_extra_usec != 0 or type(snap.runtime_randomized_extra_usec) is not int:
        raise _refus() from None
    if snap.kill_mode != "control-group" or snap.send_sigkill is not True:
        raise _refus() from None
    if snap.timeout_stop_failure_mode != "kill":
        raise _refus() from None
    if snap.timeout_stop_usec > budget_stop_s * 1_000_000:
        raise _refus() from None
    if snap.restart != "no":
        raise _refus() from None
    _exige_unit(snap.unit)
    _check_cgroup_arg(snap.control_group)
    if re.fullmatch(r"[0-9a-f]{32}", snap.invocation_hex) is None:
        raise _refus() from None
    if type(snap.fallback_counts) is not tuple or len(snap.fallback_counts) != 5 or any(type(v) is not int for v in snap.fallback_counts):
        raise _refus() from None
    if any(type(v) is not int or v != 0 for v in (snap.exec_stop_count, snap.exec_stop_post_count)):
        raise _refus() from None
    if type(snap.load_credential_encrypted) is not tuple or len(snap.load_credential_encrypted) != 2:
        raise _refus() from None
    if any(type(pair) is not tuple or len(pair) != 2 or any(type(v) is not str or not v for v in pair) for pair in snap.load_credential_encrypted):
        raise _refus() from None
    if type(policy_mapping) is not dict or len(policy_mapping) != 2 or any(type(k) is not str or type(v) is not str for k, v in policy_mapping.items()):
        raise _refus() from None
    if snap.fallback_counts != (0, 0, 0, 0, 0):
        raise _refus() from None
    if dict(snap.load_credential_encrypted) != dict(policy_mapping) or len(snap.load_credential_encrypted) != 2:
        raise _refus() from None
    try:
        now_mono_us = time.monotonic_ns() // 1000
    except OSError:
        raise _refus() from None
    if snap.active_enter_monotonic > now_mono_us:
        raise _refus() from None
    end_us = snap.active_enter_monotonic + snap.runtime_max_usec + snap.timeout_stop_usec
    if end_us <= now_mono_us:
        raise _refus() from None
    if end_us - now_mono_us > remaining_validity_s * 1_000_000:
        raise _refus() from None
def _systemctl_state(*, manager: str, unit: str, timeout_s: int, uid: int) -> dict:
    _exige_manager(manager)
    _exige_unit(unit)
    _exige_timeout(timeout_s)
    cmd = [_SYSTEMCTL, "--no-ask-password"]
    if manager == "user":
        base = _check_user_bus_dir(uid)
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "XDG_RUNTIME_DIR": base}
        cmd.append("--user")
    else:
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    cmd.extend(["show", "--no-pager", "--property=ActiveState,MainPID,ControlGroup", "--", unit])
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s, env=env)
    except OSError:
        raise _refus() from None
    except subprocess.SubprocessError:
        raise _refus() from None
    if proc.returncode != 0 or len(proc.stdout) > 65536:
        raise _refus() from None
    try:
        text = proc.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise _refus() from None
    out: dict = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k] = v
    if set(out.keys()) != {"ActiveState", "MainPID", "ControlGroup"}:
        raise _refus() from None
    return out
@dataclass(frozen=True)
class StoppedProof:
    unit: str
    active_state: str
    main_pid: int
def _check_cgroup_arg(cg: str) -> str:
    if type(cg) is not str or not cg or cg == "/" or "\x00" in cg:
        raise _refus() from None
    if not cg.startswith("/") or "//" in cg:
        raise _refus() from None
    for seg in cg.split("/"):
        if seg in (".", ".."):
            raise _refus() from None
    return cg
def attest_stopped(*, manager: str, unit: str, old_control_group: str, old_invocation_hex: str, timeout_s: int, uid: int) -> StoppedProof:
    _exige_manager(manager)
    _exige_unit(unit)
    cg = _check_cgroup_arg(old_control_group)
    if type(old_invocation_hex) is not str or len(old_invocation_hex) != 32:
        raise _refus() from None
    props = _systemctl_state(manager=manager, unit=unit, timeout_s=timeout_s, uid=uid)
    if props.get("ActiveState") not in ("inactive", "failed") or props.get("MainPID", "1") != "0":
        raise _refus() from None
    path = get_unit_path(manager=manager, unit=unit, timeout_s=timeout_s, uid=uid)
    cur = _get_props(manager=manager, object_path=path, interface="org.freedesktop.systemd1.Unit", names=("InvocationID",), timeout_s=timeout_s, uid=uid)
    if _ay_to_hex(cur["InvocationID"]) not in (old_invocation_hex, "0" * 32):
        raise _refus() from None
    events = "/sys/fs/cgroup" + cg + "/cgroup.events"
    try:
        fd = os.open(events, os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        try:
            os.stat("/sys/fs/cgroup" + cg, follow_symlinks=False)
        except FileNotFoundError:
            return StoppedProof(unit=unit, active_state=props["ActiveState"], main_pid=0)
        except OSError:
            raise _refus() from None
        raise _refus() from None
    except OSError:
        raise _refus() from None
    with _closing_fd(fd):
        try:
            body = os.read(fd, 4096).decode("utf-8")
        except UnicodeDecodeError:
            raise _refus() from None
        except OSError:
            raise _refus() from None
    for line in body.splitlines():
        if line.startswith("populated ") and line.split()[1] == "0":
            return StoppedProof(unit=unit, active_state=props["ActiveState"], main_pid=0)
    raise _refus() from None
@contextmanager
def unit_lease(*, manager: str, unit: str, timeout_s: int, uid: int):
    """Conserve la définition transitoire ; ne prouve aucune autorisation ni aucun effet."""
    _exige_manager(manager)
    _exige_unit(unit)
    _exige_timeout(timeout_s)
    if type(uid) is not int or uid < 0 or timeout_s * 1000000 >= (1 << 64):
        raise _refus() from None
    if manager == "user":
        if os.getuid() != uid or os.geteuid() != uid:
            raise _refus() from None
        address = ("unix:path=" + _check_user_bus_dir(uid) + "/bus").encode("utf-8")
    else:
        address = b"unix:path=/run/dbus/system_bus_socket"
    try:
        library = ctypes.CDLL("libsystemd.so.0")
        declarations = {
            "sd_bus_new": (ctypes.c_int, [ctypes.POINTER(ctypes.c_void_p)]),
            "sd_bus_set_address": (ctypes.c_int, [ctypes.c_void_p, ctypes.c_char_p]),
            "sd_bus_set_bus_client": (ctypes.c_int, [ctypes.c_void_p, ctypes.c_int]),
            "sd_bus_set_method_call_timeout": (ctypes.c_int, [ctypes.c_void_p, ctypes.c_uint64]),
            "sd_bus_start": (ctypes.c_int, [ctypes.c_void_p]),
            "sd_bus_call_method": (ctypes.c_int, [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]),
            "sd_bus_message_unref": (ctypes.c_void_p, [ctypes.c_void_p]),
            "sd_bus_close": (None, [ctypes.c_void_p]),
            "sd_bus_unref": (ctypes.c_void_p, [ctypes.c_void_p]),
        }
        for name, (result_type, argument_types) in declarations.items():
            function = getattr(library, name)
            function.restype = result_type
            function.argtypes = argument_types
    except (OSError, AttributeError):
        raise _refus() from None
    bus = ctypes.c_void_p()
    reply = ctypes.c_void_p()
    try:
        if library.sd_bus_new(ctypes.byref(bus)) < 0 or not bus:
            raise _refus() from None
        if library.sd_bus_set_address(bus, address) < 0 or library.sd_bus_set_bus_client(bus, 1) < 0:
            raise _refus() from None
        if library.sd_bus_set_method_call_timeout(bus, timeout_s * 1000000) < 0 or library.sd_bus_start(bus) < 0:
            raise _refus() from None
        result = library.sd_bus_call_method(bus, b"org.freedesktop.systemd1", b"/org/freedesktop/systemd1", b"org.freedesktop.systemd1.Manager", b"RefUnit", None, ctypes.byref(reply), b"s", ctypes.c_char_p(unit.encode("utf-8")))
        if result < 0:
            raise _refus() from None
        yield
    finally:
        if reply:
            library.sd_bus_message_unref(reply)
        if bus:
            library.sd_bus_close(bus)
            library.sd_bus_unref(bus)

def systemctl_stop(*, manager: str, unit: str, timeout_s: int, uid: int) -> None:
    _exige_manager(manager)
    _exige_unit(unit)
    _exige_timeout(timeout_s)
    cmd = [_SYSTEMCTL, "--no-ask-password"]
    if manager == "user":
        base = _check_user_bus_dir(uid)
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "XDG_RUNTIME_DIR": base}
        cmd.append("--user")
    else:
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    cmd.extend(["stop", "--", unit])
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s, env=env)
    except OSError:
        raise _refus() from None
    except subprocess.SubprocessError:
        raise _refus() from None
    if proc.returncode != 0:
        raise _refus() from None
def systemctl_start(*, manager: str, unit: str, timeout_s: int, uid: int) -> None:
    _exige_manager(manager)
    _exige_unit(unit)
    _exige_timeout(timeout_s)
    cmd = [_SYSTEMCTL, "--no-ask-password"]
    if manager == "user":
        base = _check_user_bus_dir(uid)
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "XDG_RUNTIME_DIR": base}
        cmd.append("--user")
    else:
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    cmd.extend(["start", "--", unit])
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s, env=env)
    except OSError:
        raise _refus() from None
    except subprocess.SubprocessError:
        raise _refus() from None
    if proc.returncode != 0:
        raise _refus() from None
