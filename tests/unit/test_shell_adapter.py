"""Unit tests shell adapter, no Django configured in parent."""

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
    import pixs.backend
    guard = mock.Mock(side_effect=AssertionError("filesystem access at import"))
    with (
        mock.patch.object(os, "open", guard),
        mock.patch.object(os, "scandir", guard),
        mock.patch.object(Path, "open", guard),
        mock.patch.object(Path, "read_bytes", guard),
    ):
        import pixs.backend.shell_adapter as adapter
        assert tuple(adapter.__all__) == ("ShellAdapterError", "build_shell_views")
    assert "django" not in sys.modules
    assert guard.call_count == 0
    print("PUR")
''')


_FIXTURE_CODE = textwrap.dedent(r'''
    import sys
    import hashlib
    import tempfile
    from pathlib import Path
    src = sys.argv[1]
    cache = sys.argv[2]
    sys.path.insert(0, src)
    from django.conf import settings
    if not settings.configured:
        settings.configure(DEFAULT_CHARSET="utf-8", LOGGING_CONFIG=None)
    from pixs.backend.shell_adapter import build_shell_views

    class FakeRequest:
        def __init__(self, method):
            self.method = method

    with tempfile.TemporaryDirectory(dir=cache, prefix="shell-fixtures-") as tmp:
        root = Path(tmp)
        index_body = b"<html>shell</html>"
        js_body = b"console.log(1)"
        css_body = b"body{}"
        (root / "index.html").write_bytes(index_body)
        assets = root / "assets"
        assets.mkdir()
        (assets / "index-Ab12.js").write_bytes(js_body)
        (assets / "index-Ab12.css").write_bytes(css_body)
        views = build_shell_views(root)
        assert set(views) == {"index.html", "assets/index-Ab12.js", "assets/index-Ab12.css"}
        digests = {key: hashlib.sha256(bytes(handler(FakeRequest("GET")).content)).hexdigest() for key, handler in views.items()}
        assert digests["index.html"] == hashlib.sha256(index_body).hexdigest()
        for key, handler in views.items():
            get_response = handler(FakeRequest("GET"))
            assert get_response.status_code == 200
            assert get_response["Cache-Control"] == "no-store"
            head_response = handler(FakeRequest("HEAD"))
            assert head_response.status_code == 200
            assert bytes(head_response.content) == b""
            assert head_response["Content-Length"] == get_response["Content-Length"]
            denied = handler(FakeRequest("POST"))
            assert denied.status_code == 405
            assert denied["Allow"] == "GET, HEAD"
        assert views["index.html"](FakeRequest("GET"))["Content-Type"] == "text/html; charset=utf-8"
        assert views["assets/index-Ab12.js"](FakeRequest("GET"))["Content-Type"] == "application/javascript"
        assert views["assets/index-Ab12.css"](FakeRequest("GET"))["Content-Type"] == "text/css"
        (root / "index.html").write_bytes(b"<changed></changed>")
        (assets / "index-Ab12.js").unlink()
        assert bytes(views["index.html"](FakeRequest("GET")).content) == index_body
        assert bytes(views["assets/index-Ab12.js"](FakeRequest("GET")).content) == js_body
        after = {key: hashlib.sha256(bytes(handler(FakeRequest("GET")).content)).hexdigest() for key, handler in views.items()}
        assert after == digests
        limit_root = root / "at-limit"
        limit_root.mkdir()
        (limit_root / "index.html").write_bytes(b"x")
        limit_assets = limit_root / "assets"
        limit_assets.mkdir()
        for index in range(63):
            (limit_assets / f"file{index:02d}.js").write_bytes(b"x")
        assert len(build_shell_views(limit_root)) == 64
    print("FIXTURE")
''')


_REFUSED_CODE = textwrap.dedent(r'''
    import sys
    import os
    import tempfile
    from pathlib import Path
    src = sys.argv[1]
    cache = sys.argv[2]
    sys.path.insert(0, src)
    from django.conf import settings
    if not settings.configured:
        settings.configure(DEFAULT_CHARSET="utf-8", LOGGING_CONFIG=None)
    from pixs.backend.shell_adapter import ShellAdapterError, build_shell_views

    class HostileGetter:
        @property
        def method(self):
            raise ValueError("RAW_HOSTILE_METHOD_MARKER")
        def __repr__(self):
            raise AssertionError("repr forbidden")

    class HostileMethod(str):
        def __eq__(self, other):
            raise AssertionError("comparison forbidden")

    with tempfile.TemporaryDirectory(dir=cache, prefix="shell-fixtures-") as tmp:
        root = Path(tmp)
        (root / "index.html").write_bytes(b"x")
        (root / "assets").mkdir()
        handler = build_shell_views(root)["index.html"]
        for hostile in (HostileGetter(), __import__("types").SimpleNamespace(method=HostileMethod("GET"))):
            try:
                handler(hostile)
            except ShellAdapterError as error:
                assert str(error) == "Invalid shell distribution."
                assert "RAW_HOSTILE_METHOD_MARKER" not in str(error)
            else:
                raise AssertionError("hostile refused")
        for bad in (None, 123, {"method": "GET"}):
            try:
                handler(bad)
            except ShellAdapterError:
                pass
            else:
                raise AssertionError("bad request refused")

    def expect_refused(maker):
        with tempfile.TemporaryDirectory(dir=cache, prefix="shell-fixtures-") as tmp:
            root = Path(tmp)
            maker(root)
            try:
                build_shell_views(root)
            except ShellAdapterError as error:
                assert str(error) == "Invalid shell distribution."
            else:
                raise AssertionError("refused distribution accepted")

    def make_hidden(root):
        (root / "index.html").write_bytes(b"x")
        (root / "assets").mkdir()
        ((root / "assets") / ".hidden.js").write_bytes(b"x")

    def make_big(root):
        (root / "index.html").write_bytes(b"x")
        assets = root / "assets"
        assets.mkdir()
        ((assets) / "big.js").write_bytes(b"y" * (1048576 + 1))

    def make_many(root):
        (root / "index.html").write_bytes(b"x")
        assets = root / "assets"
        assets.mkdir()
        for index in range(64):
            ((assets) / f"file{index:02d}.js").write_bytes(b"x")

    def make_over_total(root):
        (root / "index.html").write_bytes(b"y" * 1048576)
        assets = root / "assets"
        assets.mkdir()
        for index in range(8):
            ((assets) / f"chunk{index}.js").write_bytes(b"z" * 1048576)

    def make_bad_name(root):
        (root / "index.html").write_bytes(b"x")
        assets = root / "assets"
        assets.mkdir()
        ((assets) / "bad name.js").write_bytes(b"x")

    for maker in (make_hidden, make_big, make_many, make_over_total, make_bad_name):
        expect_refused(maker)

    with tempfile.TemporaryDirectory(dir=cache, prefix="shell-fixtures-") as tmp:
        real = Path(tmp) / "real-root"
        real.mkdir()
        (real / "index.html").write_bytes(b"x")
        (real / "assets").mkdir()
        link = Path(tmp) / "root-link"
        os.symlink(str(real), str(link))
        try:
            build_shell_views(link)
        except ShellAdapterError:
            pass
        else:
            raise AssertionError("symlink root refused")
    with tempfile.TemporaryDirectory(dir=cache, prefix="shell-fixtures-") as tmp:
        root = Path(tmp)
        (root / "index.html").write_bytes(b"x")
        assets = root / "assets"
        assets.mkdir()
        target = root / "real-asset.js"
        target.write_bytes(b"x")
        os.symlink(str(target), str(assets / "link.js"))
        try:
            build_shell_views(root)
        except ShellAdapterError:
            pass
        else:
            raise AssertionError("symlink leaf refused")
    with tempfile.TemporaryDirectory(dir=cache, prefix="shell-fixtures-") as tmp:
        parent = Path(tmp)
        root = parent / "dist"
        root.mkdir()
        (root / "index.html").write_bytes(b"x")
        outside_assets = parent / "outside-assets"
        outside_assets.mkdir()
        os.symlink(str(outside_assets), str(root / "assets"))
        try:
            build_shell_views(root)
        except ShellAdapterError:
            pass
        else:
            raise AssertionError("symlink directory accepted")
    for filename in ("bad..js", "bad%.js", "bad\\name.js", "bad\nname.js", "unsupported.txt"):
        def make_invalid(root):
            (root / "index.html").write_bytes(b"x")
            assets = root / "assets"
            assets.mkdir()
            (assets / filename).write_bytes(b"x")
        expect_refused(make_invalid)
    for bad_root in (None, 123, "", b"x"):
        try:
            build_shell_views(bad_root)
        except ShellAdapterError:
            pass
        else:
            raise AssertionError("invalid root accepted")
    print("REFUSED")
''')


class ShellAdapterUnitTests(unittest.TestCase):
    def test_pure_import_without_fs(self):
        result = _run(_PURE_IMPORT_CODE, _SRC, _CACHE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PUR", result.stdout)

    def test_fixture_handlers(self):
        result = _run(_FIXTURE_CODE, _SRC, _CACHE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FIXTURE", result.stdout)

    def test_refused_distributions(self):
        result = _run(_REFUSED_CODE, _SRC, _CACHE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
