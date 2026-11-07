"""Recette C14 : bundle composé, navigateur réel, HTTPS local et schéma PostgreSQL jetable.

Le certificat et les cookies de recette restent dans les processus locaux.
La confiance TLS du navigateur est limitée au profil éphémère de test.
Aucun exécutant réseau, service DNS actif ou P0 global n'est qualifié.
"""
from __future__ import annotations

_BROWSER_DIAGNOSTICS = []
_HTTP_DIAGNOSTICS = []
_TEARDOWN = {}

UI_CASES = (
    "real_renderer_pzt", "real_renderer_dns", "real_http_confirmed_mutations",
    "unknown_unmeasured_honest", "list_record_lf_order_duplicates",
    "retirement_visible", "locales_fr_en", "no_console_errors",
)
EXPECTED_CASES = UI_CASES + (
    "tls_loopback_encryption_observed", "https_bootstrap_web_cookie",
    "pzt_mutation_persisted", "dns_mutation_persisted", "child_cleanup",
    "https_server_closed", "temporary_files_removed",
)


def run(root_str, engine):
    from pathlib import Path
    from c14_pg_test_support import run_in_c14_schema
    root = Path(root_str).resolve()
    if str(root) != "/home/devops/datas/pixs" or engine not in ("chromium", "firefox"):
        return {"real_pg": False, "cleanup": True, "conns_closed": True, "code": "INPUT_REFUSED"}
    _BROWSER_DIAGNOSTICS.clear()
    _HTTP_DIAGNOSTICS.clear()
    _TEARDOWN.clear()
    result = run_in_c14_schema(str(root), lambda: _scenarios(root, engine), EXPECTED_CASES)
    result["browser_diagnostics"] = list(_BROWSER_DIAGNOSTICS)
    result["http_diagnostics"] = list(_HTTP_DIAGNOSTICS)
    result["teardown"] = dict(_TEARDOWN)
    return result


def _scenarios(root, engine):
    import hashlib
    import io
    import json
    import mimetypes
    import os
    import signal
    import shutil
    import ssl
    import subprocess
    import tempfile
    import time
    import pathlib
    from pathlib import PurePosixPath
    from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
    from django.conf import settings
    from django.core.handlers.wsgi import WSGIRequest
    from django.urls import resolve
    from c14_composed_browser_fixture import build_fixture
    from test_pzt_dns_contracts import _pztcfg, _dnscfg
    from test_pzt_dns_http_inputs import wire

    cases = {name: False for name in EXPECTED_CASES}
    state_path = root / "output/cismp/cismp4-pixs-86551e9b05914e67/state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    build = state["task_2_3_composed_build_proof"]
    if build["exit"] != 0 or build["mode"] != "COMPOSED":
        raise RuntimeError("COMPOSED_BUILD_NOT_PROVED")
    artifact_prefix = "frontend/dist/"
    artifacts = build["artifacts"]
    if "isolated_artifacts" in build:
        artifact_prefix = ("output/cismp/cismp4-pixs-86551e9b05914e67/composed-artifacts/"
                           + build["native_call_id"] + "/")
        if build.get("artifact_prefix") != artifact_prefix:
            raise RuntimeError("BUILD_SNAPSHOT_PREFIX_INVALID")
        artifacts = build["isolated_artifacts"]
    if type(artifacts) is not dict or artifact_prefix + "index.html" not in artifacts:
        raise RuntimeError("BUILD_ARTIFACTS_INVALID")
    assets = {}
    for relative, digest in artifacts.items():
        rel = PurePosixPath(relative)
        if (not relative.startswith(artifact_prefix) or ".." in rel.parts
                or rel.is_absolute() or type(digest) is not str or len(digest) != 64):
            raise RuntimeError("BUILD_ARTIFACT_PATH_INVALID")
        target = root / relative
        if target.is_symlink() or target.resolve() != target or not target.is_file():
            raise RuntimeError("BUILD_ARTIFACT_INVALID")
        content = target.read_bytes()
        if hashlib.sha256(content).hexdigest() != digest:
            raise RuntimeError("BUILD_ARTIFACT_CHANGED")
        suffix = relative.removeprefix(artifact_prefix)
        assets["/" + suffix] = (content, mimetypes.guess_type(suffix)[0] or "application/octet-stream")

    tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls.minimum_version = ssl.TLSVersion.TLSv1_2
    observed = {"tls": False, "bootstrap": False, "server_error": False}
    diagnostics = io.StringIO()

    class Server(WSGIServer):
        def get_request(self):
            raw, address = self.socket.accept()
            raw.settimeout(5)
            try:
                connection = tls.wrap_socket(raw, server_side=True)
            except (ssl.SSLError, OSError):
                raw.close()
                raise
            observed["tls"] = bool(connection.cipher())
            return connection, address

        def handle_error(self, request, client_address):
            observed["server_error"] = True

    class Handler(WSGIRequestHandler):
        def log_message(self, format, *args):
            return

        def get_stderr(self):
            return diagnostics

        def get_environ(self):
            environ = super().get_environ()
            if not isinstance(self.connection, ssl.SSLSocket) or not self.connection.cipher():
                raise RuntimeError("TLS_NOT_PROVED")
            environ["HTTPS"] = "on"
            environ["wsgi.url_scheme"] = "https"
            environ["RAW_URI"] = self.path
            return environ

    settings.ALLOWED_HOSTS = ["127.0.0.1"]
    settings.SECRET_KEY = "Vecteur public C14 de test, sans secret de déploiement"
    cache = root / "frontend/.cache"
    cache.mkdir(exist_ok=True)
    child = None
    browser_directory = None
    server = None
    group = None
    group_closed = False
    server_closed = False
    temporary = None
    with tempfile.TemporaryDirectory(prefix="c14-composed-https-", dir=cache) as temporary:
        directory = root / temporary
        certificate, private_key = directory / "certificate.pem", directory / "private-key.pem"
        generated = subprocess.run(
            ["/usr/bin/openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
             "-days", "1", "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1",
             "-keyout", str(private_key), "-out", str(certificate)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15, check=False,
        )
        if generated.returncode != 0:
            raise RuntimeError("TEST_CERTIFICATE_GENERATION_FAILED")
        private_key.chmod(0o600)
        tls.load_cert_chain(str(certificate), str(private_key))
        try:
            with Server(("127.0.0.1", 0), Handler) as server:
                server.timeout = 0.25
                host = "127.0.0.1:" + str(server.server_address[1])
                origin = "https://" + host
                settings.CSRF_TRUSTED_ORIGINS = [origin]
                fixture = build_fixture(origin, host)
                configurations = {"pzt": wire(_pztcfg(1)), "dns": wire(_dnscfg(1))}
                for owner, configuration in configurations.items():
                    reference = {"owner_id": "pixs." + owner, "entry_id": "entrée-fixture",
                                 "source": "source\nfixture"}
                    configuration["secret_refs"] = [dict(reference), {**reference, "entry_id": "seconde-fixture"}, dict(reference)]
                vectors = {
                    "origin": origin, "pzt_ref": fixture["pzt_ref"], "dns_ref": fixture["dns_ref"],
                    "pzt_configuration": configurations["pzt"], "dns_configuration": configurations["dns"],
                }
                browser_directory = root / tempfile.mkdtemp(prefix="c4-" + engine[0] + "-", dir=cache)
                vectors["browser_directory"] = str(browser_directory)
                spa_routes = {"/", "/login", "/platform", "/platform/pzt", "/platform/dns"}

                def answer(start_response, status, content=b"", content_type="application/json", extra=()):
                    headers = [("Content-Type", content_type), ("Content-Length", str(len(content))),
                               ("Cache-Control", "no-store"), ("X-Content-Type-Options", "nosniff")]
                    start_response(status, headers + list(extra))
                    return [content]

                def app(environ, start_response):
                    if (environ.get("wsgi.url_scheme") != "https" or environ.get("HTTP_HOST") != host
                            or environ.get("REMOTE_ADDR") != "127.0.0.1"):
                        return answer(start_response, "403 Forbidden")
                    request = WSGIRequest(environ)
                    path = request.path_info
                    if path == "/__c14/bootstrap":
                        if request.method != "GET" or request.META.get("QUERY_STRING"):
                            return answer(start_response, "405 Method Not Allowed")
                        observed["bootstrap"] = True
                        return answer(start_response, "302 Found", extra=[
                            ("Location", "/platform/pzt"),
                            ("Set-Cookie", fixture["web_cookie_name"] + "=" + fixture["web_cookie"]
                             + "; Path=/; HttpOnly; Secure; SameSite=Strict"),
                            ("Set-Cookie", "csrftoken=" + fixture["csrf"]
                             + "; Path=/; Secure; SameSite=Strict"),
                        ])
                    if path == "/favicon.ico":
                        return answer(start_response, "204 No Content")
                    if path.startswith("/api/v1/"):
                        try:
                            matched = resolve(path, urlconf=tuple(fixture["urls"]))
                            response = matched.func(request, *matched.args, **matched.kwargs)
                        except Exception:
                            observed["server_error"] = True
                            return answer(start_response, "500 Internal Server Error")
                        category = ("SHELL_CONTEXT" if path.endswith("/shell/context")
                                    else "CSRF" if path.endswith("/auth/csrf")
                                    else "PZT" if "/pzt/" in path
                                    else "DNS" if "/dns/" in path else "CORE_OTHER")
                        _HTTP_DIAGNOSTICS.append({"category": category,
                                                  "method": request.method, "status": response.status_code})
                        if len(_HTTP_DIAGNOSTICS) > 64:
                            del _HTTP_DIAGNOSTICS[:-64]
                        body = response.content
                        headers = list(response.items())
                        for cookie in response.cookies.values():
                            headers.append(("Set-Cookie", cookie.OutputString()))
                        start_response(str(response.status_code) + " " + response.reason_phrase, headers)
                        return [body]
                    if request.method not in ("GET", "HEAD") or request.META.get("QUERY_STRING"):
                        return answer(start_response, "404 Not Found")
                    entry = assets.get("/index.html") if path in spa_routes else assets.get(path)
                    if entry is None:
                        return answer(start_response, "404 Not Found")
                    content, media = entry
                    return answer(start_response, "200 OK", b"" if request.method == "HEAD" else content, media)

                server.set_app(app)
                report_path = directory / "runner.json"
                with report_path.open("w+", encoding="utf-8") as report_file:
                    runner = root / "frontend/tests/c14-composed-browser.mjs"
                    child = subprocess.Popen(
                        ["/home/devops/node/current/bin/node", str(runner), engine, origin],
                        stdin=subprocess.PIPE, stdout=report_file, stderr=subprocess.DEVNULL,
                        text=True, cwd=root, start_new_session=True,
                    )
                    group = child.pid
                    child.stdin.write(json.dumps(vectors, ensure_ascii=False))
                    child.stdin.close()
                    child.stdin = None
                    deadline = time.monotonic() + 105
                    while child.poll() is None and time.monotonic() < deadline:
                        server.handle_request()
                    if child.poll() is None:
                        raise RuntimeError("BROWSER_DEADLINE")
                    child.wait(timeout=5)
                    if child.returncode not in (0, 1):
                        raise RuntimeError("BROWSER_RUN_FAILED")
                    report_file.flush()
                    size = report_file.tell()
                    if not 0 < size <= 65536:
                        raise RuntimeError("BROWSER_REPORT_SIZE_INVALID")
                    report_file.seek(0)
                    report = json.loads(report_file.read(65537))
                if (type(report) is not dict or set(report) != {"schema", "engine", "cases", "cleanup", "diagnostic"}
                        or report["schema"] != "pixs.c14.composed.browser/1.0.0"
                        or report["engine"] != engine or type(report["cleanup"]) is not bool
                        or type(report["cases"]) is not dict or set(report["cases"]) != set(UI_CASES)
                        or any(type(value) is not bool for value in report["cases"].values())):
                    raise RuntimeError("BROWSER_REPORT_INVALID")
                diagnostic = report["diagnostic"]
                if diagnostic is not None:
                    if (type(diagnostic) is not dict or set(diagnostic) != {"phase", "code", "route", "field_names", "console_errors", "runtime_codes"}
                            or diagnostic["phase"] not in {"INPUT", "SPAWN", "ENDPOINT", "CONNECT",
                                "CDP_CREATE_TARGET", "CDP_ATTACH", "CDP_ENABLE", "BIDI_SESSION",
                                "BOOTSTRAP_NAVIGATE", "DOM_PZT", "DOM_DNS", "NAVIGATE_DNS"}
                            or type(diagnostic["code"]) is not str
                            or not __import__("re").fullmatch(r"C14_[A-Z_]+", diagnostic["code"])):
                        raise RuntimeError("BROWSER_DIAGNOSTIC_INVALID")
                    if (diagnostic["route"] not in {"UNKNOWN", "PZT", "DNS", "LOGIN", "PLATFORM", "OTHER"}
                            or type(diagnostic["field_names"]) is not list
                            or len(diagnostic["field_names"]) > 64
                            or any(type(name) is not str or not __import__("re").fullmatch(r"[a-z][a-z0-9_]{0,63}", name)
                                   for name in diagnostic["field_names"])
                            or type(diagnostic["console_errors"]) is not int
                            or not 0 <= diagnostic["console_errors"] <= 1000):
                        raise RuntimeError("BROWSER_DIAGNOSTIC_INVALID")
                    if (type(diagnostic["runtime_codes"]) is not list or len(diagnostic["runtime_codes"]) > 16
                            or any(type(code) is not str or not __import__("re").fullmatch(
                                r"(?:C14|COMPOSITION|SESSION|SHELL|PRESENTATION|ADAPTER)_[A-Z0-9_]+", code)
                                   for code in diagnostic["runtime_codes"])):
                        raise RuntimeError("BROWSER_DIAGNOSTIC_INVALID")
                    _BROWSER_DIAGNOSTICS.append(diagnostic)
                cases.update(report["cases"])
                cases["tls_loopback_encryption_observed"] = observed["tls"] is True
                cases["https_bootstrap_web_cookie"] = observed["bootstrap"] is True
                from pixs.pzt.models import DesiredPztRecord
                from pixs.dns.models import DesiredDnsRecord
                for owner, model in (("pzt", DesiredPztRecord), ("dns", DesiredDnsRecord)):
                    row = model.objects.filter(resource_id=fixture[owner + "_ref"]).first()
                    cases[owner + "_mutation_persisted"] = (
                        row is not None and row.business_state == "RETIRED" and row.persistence_state == "ACTIVE"
                        and row.retention_state == "RETAINED" and row.config_revision >= 2
                        and row.secret_refs == configurations[owner]["secret_refs"])
                if observed["server_error"]:
                    raise RuntimeError("SERVER_REQUEST_FAILED")
            server_closed = server.socket.fileno() == -1
        finally:
            if group is not None:
                try:
                    os.killpg(group, signal.SIGTERM)
                except ProcessLookupError:
                    group_closed = True
                if child is not None:
                    try:
                        child.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        os.killpg(group, signal.SIGKILL)
                        child.wait(timeout=3)
                def live_group():
                    for process in pathlib.Path("/proc").iterdir():
                        if not process.name.isdigit():
                            continue
                        try:
                            if process.stat().st_uid != os.getuid():
                                continue
                            fields = (process / "stat").read_text().rsplit(")", 1)[1].split()
                            if int(fields[2]) == group and fields[0] != "Z":
                                return True
                        except (OSError, ValueError, IndexError):
                            continue
                    return False
                until = time.monotonic() + 3
                while live_group() and time.monotonic() < until:
                    time.sleep(0.05)
                if live_group():
                    try:
                        os.killpg(group, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    until = time.monotonic() + 3
                    while live_group() and time.monotonic() < until:
                        time.sleep(0.05)
                group_closed = not live_group()
            if browser_directory is not None and group_closed:
                if browser_directory.exists():
                    if (browser_directory.parent != cache or browser_directory.resolve() != browser_directory
                            or browser_directory.is_symlink() or browser_directory.stat().st_uid != os.getuid()):
                        raise RuntimeError("OWNED_BROWSER_DIRECTORY_INVALID")
                    shutil.rmtree(browser_directory)
            server_closed = server is None or server.socket.fileno() == -1
            _TEARDOWN.update(child_group_quiescent=group_closed,
                             browser_profile_removed=browser_directory is None or not browser_directory.exists(),
                             server_closed=server_closed)
            diagnostics.close()
    cases["child_cleanup"] = group_closed
    cases["https_server_closed"] = server_closed
    cases["temporary_files_removed"] = temporary is not None and not (root / temporary).exists() and (browser_directory is None or not browser_directory.exists())
    for relative, digest in artifacts.items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest:
            raise RuntimeError("BUILD_ARTIFACT_CHANGED")
    return cases
