"""Unit tests local test composition, no Django configured in parent."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_CACHE = str(_ROOT / "frontend" / ".cache")
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": _CACHE}


def _run(code: str, src: str, cache: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, src, cache],
        timeout=30,
        capture_output=True,
        text=True,
        env=_ENV,
        cwd=str(_ROOT),
    )


_PURE_IMPORT_CODE = textwrap.dedent(r'''
    import sys
    import os
    import importlib.abc
    from pathlib import Path
    from unittest import mock
    src = sys.argv[1]
    sys.path.insert(0, src)

    class BlockDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == "django" or name.startswith("django."):
                raise ImportError("Django blocked in pure import")
            return None

    sys.meta_path.insert(0, BlockDjango())
    guard = mock.Mock(side_effect=AssertionError("filesystem access at import"))
    with (
        mock.patch.object(os, "open", guard),
        mock.patch.object(os, "scandir", guard),
        mock.patch.object(Path, "open", guard),
        mock.patch.object(Path, "read_bytes", guard),
    ):
        import pixs.backend.local_test_composition as composition
        assert tuple(composition.__all__) == ("UNSUPPORTED_TEST_CAPABILITIES", "LocalTestCompositionError", "build_local_test_urlpatterns", "local_test_server")
        assert composition.UNSUPPORTED_TEST_CAPABILITIES == ("kernel-activation", "core-activation", "p0", "readiness", "worker", "scheduler", "pg-connection")
    assert "django" not in sys.modules
    assert guard.call_count == 0
    print("PUR")
''')


_VALID_CODE = textwrap.dedent(r'''
    import sys
    import json
    import tempfile
    from pathlib import Path
    src = sys.argv[1]
    cache = sys.argv[2]
    sys.path.insert(0, src)
    from pixs.backend.api import ApiContractPlan
    from pixs.kernel.contracts import ContractCategory, ContractDescriptor
    from pixs.backend.http_route_guard import RouteDeclaration
    from pixs.backend.local_test_composition import build_local_test_urlpatterns

    def handler(request):
        return None

    def make_case():
        tmp = tempfile.TemporaryDirectory(dir=cache, prefix="composition-fixtures-")
        try:
            root = Path(tmp.name)
            (root / "index.html").write_bytes(b"<html></html>")
            assets = root / "assets"
            assets.mkdir()
            (assets / "index-Ab12.js").write_bytes(b"console.log(1)")
            plan = ApiContractPlan(
                contract=ContractDescriptor(
                    contract_id="pixs.contract.synthetic.status",
                    category=ContractCategory.API,
                    version="1.0.0",
                    owner_component="pixs.backend",
                    guarantees_doc="Synthetic guarantees.",
                ),
                openapi_document_ref="pixs.api.synthetic.status.v1",
            )
            status_schema = {"type": "object",
                "properties": {"status": {"type": "string"}},
                "required": ["status"]}
            media = {"application/json": {"schema": status_schema}}
            operation = {"responses": {"200": {"description": "Status.", "content": media}}}
            document = json.dumps({"openapi": "3.1.0",
                "info": {"title": "Synthetic Status", "version": "1.0.0"},
                "security": [],
                "paths": {"/api/v1/status": {"get": operation}}})
            capacity = RouteDeclaration("api/v1/status", "test-api-status", handler, True)
            return tmp, root, plan, document, capacity
        except BaseException:
            tmp.cleanup()
            raise

    keeper, root, plan, document, capacity = make_case()
    try:
        private = RouteDeclaration("api/v1/private", "test-api-private", handler, False)
        patterns = build_local_test_urlpatterns(root, plan, document, capacity,
            private_routes=(private,), unknown_ui_route="route-inconnue-xyz")
        names = [entry.name for entry in patterns[:-1]]
        assert names == ["test-health-live", "test-shell-root", "test-shell-assets-index-Ab12.js",
            "test-api-document", "test-api-status", "test-api-private", "test-unknown-ui"]
        assert len(patterns) == 8
        bare = build_local_test_urlpatterns(root, plan, document, capacity)
        assert len(bare) == 6
    finally:
        keeper.cleanup()
    print("VALID")
''')


_REFUSED_CODE = textwrap.dedent(r'''
    import sys
    import json
    import tempfile
    from pathlib import Path
    from unittest import mock
    src = sys.argv[1]
    cache = sys.argv[2]
    sys.path.insert(0, src)
    from pixs.backend.api import ApiContractPlan
    from pixs.kernel.contracts import ContractCategory, ContractDescriptor
    from pixs.backend.http_route_guard import RouteDeclaration
    from pixs.backend.local_test_composition import LocalTestCompositionError, build_local_test_urlpatterns, local_test_server

    def handler(request):
        return None

    def make_valid():
        tmp = tempfile.TemporaryDirectory(dir=cache, prefix="composition-fixtures-")
        try:
            root = Path(tmp.name)
            (root / "index.html").write_bytes(b"<html></html>")
            (root / "assets").mkdir()
            document = json.dumps({"openapi": "3.1.0",
                "info": {"title": "T", "version": "1.0.0"},
                "security": [],
                "paths": {"/api/v1/status": {"get": {"responses": {"200": {"description": "D."}}}}}})
            return tmp, root, document
        except BaseException:
            tmp.cleanup()
            raise

    keeper, root, document = make_valid()
    try:
        plan = ApiContractPlan(
            contract=ContractDescriptor(
                contract_id="pixs.contract.synthetic.status",
                category=ContractCategory.API,
                version="1.0.0",
                owner_component="pixs.backend",
                guarantees_doc="Synthetic guarantees.",
            ),
            openapi_document_ref="pixs.api.synthetic.status.v1",
        )
        forged = object.__new__(ApiContractPlan)
        object.__setattr__(forged, "contract", "not-a-descriptor")
        object.__setattr__(forged, "openapi_document_ref", "pixs.api.synthetic.status.v1")
        good_capacity = RouteDeclaration("api/v1/status", "test-api-status", handler, True)
        good_private = RouteDeclaration("api/v1/private", "test-api-private", handler, False)

        class HostileText(str):
            def __eq__(self, other):
                raise AssertionError("comparison forbidden")

        class HostileInt(int):
            def __lt__(self, other):
                raise AssertionError("comparison forbidden")

        class HostileRoute(RouteDeclaration):
            pass

        for bad_capacity in (None, 123, "x", HostileText("api/v1/status"),
                             RouteDeclaration("api/v1/status", "test-api-status", handler, False),
                             RouteDeclaration("api/v9/ghost", "test-api-ghost", handler, True),
                             RouteDeclaration("health/live", "test-api-clash", handler, True),
                             HostileRoute("api/v1/status", "test-api-status", handler, True),
                             RouteDeclaration(HostileText("api/v1/status"), "x", handler, True),
                             RouteDeclaration("api/v1/status", 123, handler, True),
                             RouteDeclaration("api/v1/status", "x", None, True),
                             RouteDeclaration("api/v1/status", "x", handler, 1)):
            try:
                build_local_test_urlpatterns(root, plan, document, bad_capacity)
            except LocalTestCompositionError as error:
                assert str(error) == "Invalid local test composition."
                assert error.__cause__ is None and error.__suppress_context__ is True
            else:
                raise AssertionError("bad capacity refused")
        for bad_plan in (None, forged):
            try:
                build_local_test_urlpatterns(root, bad_plan, document, good_capacity)
            except LocalTestCompositionError as error:
                assert error.__cause__ is None and error.__suppress_context__ is True
            else:
                raise AssertionError("bad plan refused")
        for bad_private in (["not-tuple"], (None,), (good_capacity,),
                            (RouteDeclaration("api/v1/p2", "test-api-p2", handler, True),),
                            (good_private, good_private),
                            (RouteDeclaration("health/live", "private-clash", handler, False),),
                            (RouteDeclaration("api/v1/private", "test-health-live", handler, False),)):
            try:
                build_local_test_urlpatterns(root, plan, document, good_capacity, private_routes=bad_private)
            except LocalTestCompositionError as error:
                assert error.__cause__ is None and error.__suppress_context__ is True
            else:
                raise AssertionError("bad private refused")
        for bad_ui in (123, "", "health/live", "api/v1/status", "has space", "bad%path"):
            try:
                build_local_test_urlpatterns(root, plan, document, good_capacity, unknown_ui_route=bad_ui)
            except LocalTestCompositionError as error:
                assert error.__cause__ is None and error.__suppress_context__ is True
            else:
                raise AssertionError("bad ui route refused")
        missing_document = json.dumps({"openapi": "3.1.0",
            "info": {"title": "T", "version": "1.0.0"},
            "security": [],
            "paths": {"/api/v1/elsewhere": {"get": {"responses": {"200": {"description": "D."}}}}}})
        try:
            build_local_test_urlpatterns(root, plan, missing_document, good_capacity)
        except LocalTestCompositionError as error:
            assert str(error) == "Invalid local test composition."
        else:
            raise AssertionError("missing documented capacity refused")
        for bad_host in (None, "", "localhost", "0.0.0.0", 123, HostileText("127.0.0.1")):
            try:
                with local_test_server(handler, host=bad_host, port=0):
                    pass
            except LocalTestCompositionError as error:
                assert error.__cause__ is None and error.__suppress_context__ is True
            else:
                raise AssertionError("bad host refused")
        for bad_port in (None, True, "5173", -1, 65536, HostileInt(0)):
            try:
                with local_test_server(handler, host="127.0.0.1", port=bad_port):
                    pass
            except LocalTestCompositionError as error:
                assert error.__cause__ is None and error.__suppress_context__ is True
            else:
                raise AssertionError("bad port refused")
        try:
            with local_test_server(None, host="127.0.0.1", port=0):
                pass
        except LocalTestCompositionError as error:
            assert error.__cause__ is None and error.__suppress_context__ is True
        else:
            raise AssertionError("bad application refused")
        with mock.patch("wsgiref.simple_server.make_server") as spy_make:
            fake = mock.Mock()
            fake.server_address = ("127.0.0.1", 0)
            fake.fileno.return_value = -1
            spy_make.return_value = fake
            with mock.patch("threading.Thread", side_effect=AssertionError("thread start failure")):
                try:
                    with local_test_server(handler, host="127.0.0.1", port=0):
                        pass
                except LocalTestCompositionError as error:
                    assert error.__cause__ is None and error.__suppress_context__ is True
                else:
                    raise AssertionError("start failure refused")
            assert fake.server_close.call_count == 1
            assert fake.shutdown.call_count == 0
            fake.reset_mock()
            fake_thread = mock.Mock()
            fake_thread.start.side_effect = AssertionError("thread start failure")
            with mock.patch("threading.Thread", return_value=fake_thread):
                try:
                    with local_test_server(handler, host="127.0.0.1", port=0):
                        pass
                except LocalTestCompositionError as error:
                    assert str(error) == "Invalid local test composition."
                    assert error.__cause__ is None
                else:
                    raise AssertionError("start failure refused")
            assert fake_thread.start.call_count == 1
            assert fake_thread.join.call_count == 0
            assert fake.server_close.call_count == 1
            assert fake.shutdown.call_count == 0
    finally:
        keeper.cleanup()
    print("REFUSED")
''')


class LocalTestCompositionUnitTests(unittest.TestCase):
    def test_pure_import_without_fs(self):
        result = _run(_PURE_IMPORT_CODE, _SRC, _CACHE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PUR", result.stdout)

    def test_valid_composition(self):
        result = _run(_VALID_CODE, _SRC, _CACHE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_refused_compositions(self):
        result = _run(_REFUSED_CODE, _SRC, _CACHE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
