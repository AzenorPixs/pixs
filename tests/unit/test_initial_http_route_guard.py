"""Tests unitaires garde de routes, sans Django configuré dans le parent."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}


def _run(code: str, arg: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, arg],
        timeout=30,
        capture_output=True,
        text=True,
        env=_ENV,
        cwd=str(_ROOT),
    )


_PURE_IMPORT_CODE = textwrap.dedent(f'''
    import sys
    sys.path.insert(0, {repr(_SRC)})
    import importlib.abc

    class BlockDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == "django" or name.startswith("django."):
                raise ImportError("Django bloque en import pur")
            return None

    sys.meta_path.insert(0, BlockDjango())
    import pixs.backend.http_route_guard as guard
    assert "django" not in sys.modules
    assert "django.conf" not in sys.modules
    assert tuple(guard.__all__) == (
        "HttpRouteGuardError", "RouteDeclaration", "build_declared_urlpatterns")
    print("PUR")
''')


_INVALID_DECLARATIONS_CODE = textwrap.dedent(rf'''
    import sys
    sys.path.insert(0, {repr(_SRC)})
    from pixs.backend.http_route_guard import (
        HttpRouteGuardError, RouteDeclaration, build_declared_urlpatterns)

    def handler(request):
        return None

    for invalid in (None, 123, "x", b"x"):
        try:
            build_declared_urlpatterns(invalid)
        except HttpRouteGuardError as error:
            assert str(error) == "Déclaration de route invalide."
        else:
            raise AssertionError("refus attendu")

    class ListSubclass(list):
        pass

    class TupleSubclass(tuple):
        pass

    for invalid in ({{"a": 1}}, {{"a"}}, (x for x in []), ListSubclass(), TupleSubclass()):
        try:
            build_declared_urlpatterns(invalid)
        except HttpRouteGuardError:
            pass
        else:
            raise AssertionError("iterable arbitraire refuse")

    for path in ("/a", "a//b", ".", "..", "a/./b", "a/../b", "a?b", "a#b",
                   "a*b", "<int:a>", "a:b", "a(b)", "a[b]", "a{{b}}", "a^b",
                   "a$b", "a+b", "a|b", "a\\b", "a%b", "a\n", "a\x00",
                   "a b", "a/b?c", "a.", "a..b/"):
        try:
            build_declared_urlpatterns([RouteDeclaration(path, "n", handler, True)])
        except HttpRouteGuardError:
            pass
        else:
            raise AssertionError("chemin refuse")

    for name in (None, 123, "", " x", "x ", "a/b", "a\n"):
        try:
            build_declared_urlpatterns([RouteDeclaration("a", name, handler, True)])
        except HttpRouteGuardError:
            pass
        else:
            raise AssertionError("nom refuse")

    for invalid_handler in (None, 123, "x", {{"a": 1}}):
        try:
            build_declared_urlpatterns([RouteDeclaration("a", "n", invalid_handler, True)])
        except HttpRouteGuardError:
            pass
        else:
            raise AssertionError("handler refuse")

    for invalid_public in (None, 0, 1, "oui"):
        try:
            build_declared_urlpatterns([RouteDeclaration("a", "n", handler, invalid_public)])
        except HttpRouteGuardError:
            pass
        else:
            raise AssertionError("public refuse")

    print("HOSTILE")
''')


_HOSTILE_INPUTS_CODE = textwrap.dedent(f'''
    import sys
    sys.path.insert(0, {repr(_SRC)})
    from pixs.backend.http_route_guard import (
        HttpRouteGuardError, RouteDeclaration, build_declared_urlpatterns)

    triggered = []

    class StringTrap(str):
        def __str__(self):
            triggered.append("str")
            raise AssertionError("hook interdit")
        def __repr__(self):
            triggered.append("repr")
            raise AssertionError("hook interdit")
        def __bool__(self):
            triggered.append("bool")
            raise AssertionError("hook interdit")

    class IterableTrap:
        def __iter__(self):
            triggered.append("iter")
            raise AssertionError("hook interdit")

    def handler(request):
        return None

    for invalid in (StringTrap("a"), IterableTrap(), {{"k": StringTrap("v")}}):
        try:
            build_declared_urlpatterns(invalid)
        except HttpRouteGuardError:
            pass
        else:
            raise AssertionError("piege refuse")
    assert triggered == []

    class StringSubclass(str):
        pass

    try:
        build_declared_urlpatterns([RouteDeclaration(StringSubclass("a"), "n", handler, True)])
    except HttpRouteGuardError:
        pass
    else:
        raise AssertionError("sous-type refuse")

    forged = object.__new__(RouteDeclaration)
    object.__setattr__(forged, "path", "a")
    object.__setattr__(forged, "name", "n")
    object.__setattr__(forged, "handler", "pas-callable")
    object.__setattr__(forged, "public", True)
    try:
        build_declared_urlpatterns([forged])
    except HttpRouteGuardError:
        pass
    else:
        raise AssertionError("forge revalide")

    print("PIEGES")
''')


_COLLISIONS_CODE = textwrap.dedent(f'''
    import sys
    sys.path.insert(0, {repr(_SRC)})
    from pixs.backend.http_route_guard import (
        RouteDeclaration, build_declared_urlpatterns, HttpRouteGuardError)

    def handler(request):
        return None

    try:
        build_declared_urlpatterns([
            RouteDeclaration("a", "n", handler, True),
            RouteDeclaration("a", "m", handler, True),
        ])
    except HttpRouteGuardError:
        pass
    else:
        raise AssertionError("collision path")

    try:
        build_declared_urlpatterns([
            RouteDeclaration("a", "n", handler, True),
            RouteDeclaration("b", "n", handler, True),
        ])
    except HttpRouteGuardError:
        pass
    else:
        raise AssertionError("collision nom")

    patterns = build_declared_urlpatterns([
        RouteDeclaration("", "racine", handler, True),
        RouteDeclaration("ok/", "ok", handler, True),
    ])
    assert len(patterns) == 3
    assert [m.name for m in patterns[:2]] == ["racine", "ok"]
    print("COLLISION")
''')

_SNIPPETS = (_PURE_IMPORT_CODE, _INVALID_DECLARATIONS_CODE, _HOSTILE_INPUTS_CODE, _COLLISIONS_CODE)


class HttpRouteGuardUnitTests(unittest.TestCase):
    def test_snippets_compile(self):
        for snippet in _SNIPPETS:
            compile(snippet, "<snippet>", "exec")

    def test_import_without_django(self):
        result = _run(_PURE_IMPORT_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PUR", result.stdout)

    def test_invalid_declarations_without_value_echo(self):
        result = _run(_INVALID_DECLARATIONS_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("HOSTILE", result.stdout)

    def test_hostile_inputs_without_hooks(self):
        result = _run(_HOSTILE_INPUTS_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PIEGES", result.stdout)

    def test_collisions_and_order(self):
        result = _run(_COLLISIONS_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("COLLISION", result.stdout)


if __name__ == "__main__":
    unittest.main()
