"""Sonde SSH LXC minimale, stdlib seule, sans effet import."""
import ipaddress
import json
import os
import re
import select
import signal
import stat
import subprocess
import sys
import time
PROJECT_ENV = "/home/devops/datas/pixs/project.env"
SSH_BIN = "/usr/bin/ssh"
SSHPASS_BIN = "/usr/bin/sshpass"
REMOTE_CMD = ("/usr/bin/id", "-u")
MAX_READ = 262144
MAX_OUT = 4096
MAX_NAMES = 3
MAX_PW = 512
CONNECT_TIMEOUT_S = 20
WAIT_TIMEOUT_S = 5
ALLOWED = ("SSH_CISMP_IP", "SSH_CISMP_USER", "SSH_CISMP_PASSWORD")
KEY_RE = re.compile("^[A-Za-z_][A-Za-z0-9_]*$")
USER_RE = re.compile("^[A-Za-z_][A-Za-z0-9_-]*$")
UNQUOTED_RE = re.compile("^[A-Za-z0-9_@.+/:=-]+$")
UID_RE = re.compile("[0-9]{1,10}\n")
TYPE_RE = re.compile("^[A-Za-z_][A-Za-z0-9_]*$")
ENV_FIXED = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
def _is_reg_exe(path):
    if not isinstance(path, str) or path == "":
        return False
    try:
        st = os.stat(path)
    except OSError:
        return False
    if not stat.S_ISREG(st.st_mode):
        return False
    try:
        ok = os.access(path, os.X_OK)
    except OSError:
        return False
    return bool(ok)
def _close_fd(fd):
    if fd is None or not isinstance(fd, int):
        return -1
    if fd < 0 or fd in (0, 1, 2):
        return -1
    try:
        os.close(fd)
    except OSError:
        pass
    return -1
def _close_proc_pipes(proc):
    if proc is None:
        return
    for attr in ("stdout", "stderr"):
        try:
            fh = getattr(proc, attr, None)
        except AttributeError:
            continue
        if fh is None:
            continue
        try:
            fh.close()
        except (OSError, ValueError, AttributeError):
            pass
def _decode_token(token):
    if not isinstance(token, str) or token == "":
        return None, "EMPTY"
    if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
        inner = token[1:-1]
        if "\n" in inner or "\r" in inner:
            return None, "AMBIGUOUS"
        out = []
        i = 0
        while i < len(inner):
            c = inner[i]
            if c == "\\":
                if i + 1 >= len(inner):
                    return None, "AMBIGUOUS"
                n = inner[i + 1]
                if n != '"' and n != "\\":
                    return None, "AMBIGUOUS"
                out.append(n)
                i += 2
            elif c == '"':
                return None, "AMBIGUOUS"
            else:
                out.append(c)
                i += 1
        return "".join(out), "OK"
    if len(token) >= 2 and token[0] == "'" and token[-1] == "'":
        inner = token[1:-1]
        if "\n" in inner or "\r" in inner or "'" in inner:
            return None, "AMBIGUOUS"
        return inner, "OK"
    if UNQUOTED_RE.fullmatch(token) is None:
        return None, "AMBIGUOUS"
    return token, "OK"
def parse_env_bytes(data):
    if not isinstance(data, (bytes, bytearray)):
        return None, "TYPE"
    raw = bytes(data)
    if len(raw) > MAX_READ:
        return None, "LIMIT"
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        return None, "DECODE"
    found = {}
    for line in text.splitlines():
        s = line.strip()
        if s == "":
            continue
        if s.startswith("#"):
            continue
        if s.startswith("export "):
            s = s[7:].lstrip()
            if s == "" or s.startswith("#"):
                continue
        if "=" not in s:
            continue
        left, right = s.split("=", 1)
        name = left.strip()
        if name == "":
            continue
        if KEY_RE.fullmatch(name) is None:
            continue
        up = name.upper()
        if "LXC" not in up and "SSH" not in up:
            continue
        if name not in ALLOWED:
            continue
        token = right.strip()
        value, code = _decode_token(token)
        if code == "EMPTY":
            return None, "EMPTY"
        if code != "OK":
            return None, "AMBIGUOUS"
        if name in found:
            return None, "DUPLICATE"
        found[name] = value
    for k in ALLOWED:
        if k not in found:
            return None, "MISSING"
        if found[k] == "":
            return None, "EMPTY"
    return found, "OK"
def validate_host(host):
    if not isinstance(host, str) or host == "":
        return False
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return False
    return True
def validate_user(user):
    if not isinstance(user, str) or user == "" or len(user) > 32:
        return False
    if user.startswith("-"):
        return False
    return USER_RE.fullmatch(user) is not None
def validate_password_bytes(pw):
    if not isinstance(pw, (bytes, bytearray)):
        return False
    b = bytes(pw)
    if b == b"" or len(b) > MAX_PW:
        return False
    if b"\n" in b or b"\r" in b or b"\x00" in b:
        return False
    return True
def _kill_group(pid):
    if type(pid) is not int or pid <= 0:
        return False
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        return True
    except (OSError, ValueError, AttributeError, TypeError, OverflowError):
        return False
    return True
def _terminate_and_reap(proc):
    try:
        pid = proc.pid
    except AttributeError:
        return False
    if not _kill_group(pid):
        return False
    try:
        proc.wait(timeout=WAIT_TIMEOUT_S)
    except (subprocess.TimeoutExpired, OSError, ValueError, subprocess.SubprocessError, AttributeError):
        return False
    return True
def _collect_bounded(proc, timeout_s):
    out = b""
    err = b""
    out_eof = False
    err_eof = False
    try:
        deadline = time.monotonic() + float(timeout_s)
    except (ValueError, TypeError, OverflowError):
        return None, None, "LOCAL"
    outs = proc.stdout
    errs = proc.stderr
    if outs is None or errs is None:
        return None, None, "LOCAL"
    while True:
        if out_eof and err_eof:
            break
        try:
            remaining = deadline - time.monotonic()
        except (OSError, ValueError):
            return None, None, "LOCAL"
        if remaining <= 0:
            return None, None, "TIMEOUT"
        rlist = []
        if not out_eof:
            rlist.append(outs)
        if not err_eof:
            rlist.append(errs)
        try:
            ready, _, _ = select.select(rlist, [], [], remaining)
        except (OSError, ValueError):
            return None, None, "LOCAL"
        if not ready:
            return None, None, "TIMEOUT"
        for fh in ready:
            want = 1024
            try:
                if fh is outs:
                    want = min(1024, MAX_OUT + 1 - len(out))
                else:
                    want = min(1024, MAX_OUT + 1 - len(err))
            except (TypeError, OverflowError):
                return None, None, "LOCAL"
            if want <= 0:
                return None, None, "OUT_LIMIT"
            try:
                chunk = os.read(fh.fileno(), want)
            except (OSError, ValueError):
                return None, None, "LOCAL"
            if chunk == b"":
                if fh is outs:
                    out_eof = True
                else:
                    err_eof = True
                continue
            if fh is outs:
                out += chunk
                if len(out) > MAX_OUT:
                    return None, None, "OUT_LIMIT"
            else:
                err += chunk
                if len(err) > MAX_OUT:
                    return None, None, "OUT_LIMIT"
    return out, err, "OK"
def _classify(code, err):
    low = bytes(err)[:512].lower()
    if b"host key verification failed" in low or b"no matching host key" in low:
        return "UNKNOWN_HOST_KEY"
    if b"permission denied" in low or b"authentication failed" in low:
        return "AUTH_FAILED"
    if b"timed out" in low or b"connection refused" in low or b"no route" in low or b"could not resolve" in low:
        return "NETWORK"
    if code is None:
        return "TIMEOUT"
    return "REMOTE"
def _wait_code(proc):
    try:
        rc = proc.wait(timeout=WAIT_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None, "WAIT_TIMEOUT"
    except (OSError, ValueError, subprocess.SubprocessError, AttributeError):
        return None, "WAIT_ERROR"
    return rc, "OK"
def run_probe(host, user, password, timeout_s=CONNECT_TIMEOUT_S):
    rfd = -1
    wfd = -1
    proc = None
    try:
        if not isinstance(host, str) or not isinstance(user, str):
            return {"status": "LOCAL_REFUSED", "exit": None, "uid": None}
        if not validate_host(host):
            return {"status": "LOCAL_REFUSED", "exit": None, "uid": None}
        if not validate_user(user):
            return {"status": "LOCAL_REFUSED", "exit": None, "uid": None}
        if not validate_password_bytes(password):
            return {"status": "LOCAL_REFUSED", "exit": None, "uid": None}
        if not _is_reg_exe(SSH_BIN):
            return {"status": "HELPER_MISSING", "exit": None, "uid": None}
        if not _is_reg_exe(SSHPASS_BIN):
            return {"status": "LOCAL_CLIENT_AUTH_HELPER_UNAVAILABLE", "exit": None, "uid": None}
        pw = bytes(password)
        try:
            rfd, wfd = os.pipe()
        except OSError:
            return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
        if rfd in (0, 1, 2) or wfd in (0, 1, 2):
            return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
        msg = pw + b"\n"
        view = memoryview(msg)
        total = 0
        while total < len(msg):
            try:
                n = os.write(wfd, view[total:])
            except OSError:
                return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
            if n is None or n <= 0:
                return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
            total += int(n)
        wfd = _close_fd(wfd)
        if rfd < 0:
            return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
        args = [SSHPASS_BIN, "-d", str(rfd), SSH_BIN, "-p", "22", "-o", "StrictHostKeyChecking=yes", "-o", "PreferredAuthentications=password", "-o", "PubkeyAuthentication=no", "-o", "NumberOfPasswordPrompts=1", "-o", "ConnectTimeout=10", "-o", "ForwardAgent=no", "-o", "ClearAllForwardings=yes", "-o", "ControlMaster=no", "-o", "ControlPath=none", "-o", "UpdateHostKeys=no", "-l", user, host, REMOTE_CMD[0], REMOTE_CMD[1]]
        try:
            proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=dict(ENV_FIXED), start_new_session=True, pass_fds=(rfd,))
        except (OSError, ValueError, subprocess.SubprocessError):
            return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
        rfd = _close_fd(rfd)
        try:
            out, err, how = _collect_bounded(proc, timeout_s)
        except (OSError, ValueError):
            if _terminate_and_reap(proc):
                return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
            return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
        if how == "TIMEOUT":
            if _terminate_and_reap(proc):
                return {"status": "TIMEOUT", "exit": None, "uid": None}
            return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
        if how == "OUT_LIMIT":
            if _terminate_and_reap(proc):
                return {"status": "OUT_LIMIT", "exit": None, "uid": None}
            return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
        if how != "OK":
            if _terminate_and_reap(proc):
                return {"status": "LOCAL_ERROR", "exit": None, "uid": None}
            return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
        code, why = _wait_code(proc)
        if why != "OK":
            _kill_group(getattr(proc, "pid", -1))
            try:
                code2, why2 = _wait_code(proc)
            except (OSError, ValueError, AttributeError):
                return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
            if why2 != "OK":
                return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
            code = code2
        if not isinstance(code, int):
            return {"status": "CLEANUP_FAILED", "exit": None, "uid": None}
        if code == 0:
            if out is None or b"\x00" in out:
                return {"status": "REMOTE", "exit": code, "uid": None}
            try:
                txt = out.decode("ascii")
            except UnicodeError:
                return {"status": "REMOTE", "exit": code, "uid": None}
            if UID_RE.fullmatch(txt) is None:
                return {"status": "REMOTE", "exit": code, "uid": None}
            try:
                uid = int(txt.strip(), 10)
            except ValueError:
                return {"status": "REMOTE", "exit": code, "uid": None}
            return {"status": "OK", "exit": code, "uid": uid}
        eb = err if isinstance(err, bytes) else b""
        return {"status": _classify(code, eb), "exit": code, "uid": None}
    finally:
        rfd = _close_fd(rfd)
        wfd = _close_fd(wfd)
        _close_proc_pipes(proc)
def load_config():
    try:
        with open(PROJECT_ENV, "rb") as fh:
            raw = fh.read(MAX_READ + 1)
    except OSError:
        return None, "READ"
    if not isinstance(raw, bytes) or len(raw) > MAX_READ:
        return None, "LIMIT"
    cfg, code = parse_env_bytes(raw)
    if code != "OK" or not isinstance(cfg, dict):
        return None, code
    if len(cfg) != MAX_NAMES:
        return None, "AMBIGUOUS"
    host = cfg.get("SSH_CISMP_IP")
    user = cfg.get("SSH_CISMP_USER")
    pwd_s = cfg.get("SSH_CISMP_PASSWORD")
    if not isinstance(host, str) or not isinstance(user, str) or not isinstance(pwd_s, str):
        return None, "AMBIGUOUS"
    try:
        pwd = pwd_s.encode("utf-8")
    except UnicodeError:
        return None, "AMBIGUOUS"
    if not validate_host(host):
        return None, "HOST"
    if not validate_user(user):
        return None, "USER"
    if not validate_password_bytes(pwd):
        return None, "AMBIGUOUS"
    return (host, user, pwd), "OK"
def main():
    try:
        cfg, code = load_config()
        if code != "OK":
            print(json.dumps({"status": code, "exit": None, "uid": None}, separators=(",", ":")))
            return 0
        host, user, pwd = cfg
        res = run_probe(host, user, pwd, timeout_s=CONNECT_TIMEOUT_S)
        if not isinstance(res, dict):
            print(json.dumps({"status": "LOCAL_ERROR", "exit": None, "uid": None}, separators=(",", ":")))
            return 0
        st = res.get("status")
        ex = res.get("exit")
        uid = res.get("uid")
        if not isinstance(st, str) or (ex is not None and not isinstance(ex, int)) or (uid is not None and not isinstance(uid, int)):
            print(json.dumps({"status": "LOCAL_ERROR", "exit": None, "uid": None}, separators=(",", ":")))
            return 0
        out = json.dumps({"status": st, "exit": ex, "uid": uid}, separators=(",", ":"))
        if len(out.encode("utf-8")) > MAX_OUT:
            print(json.dumps({"status": "LIMIT_OUTPUT", "exit": None, "uid": None}, separators=(",", ":")))
            return 0
        print(out)
        return 0
    except Exception as exc:
        et = type(exc).__name__
        if not isinstance(et, str) or TYPE_RE.fullmatch(et) is None:
            et = "Unknown"
        print(json.dumps({"status": "LOCAL_ERROR", "exit": None, "uid": None, "error_type": et}, separators=(",", ":")))
        return 0
if __name__ == "__main__":
    sys.exit(main())
