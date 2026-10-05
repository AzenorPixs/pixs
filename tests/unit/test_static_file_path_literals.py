"""Unit tests static file path literals, no Django configured in parent."""

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


_ACCEPTED_LITERALS_CODE = textwrap.dedent(r'''
    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    from pixs.backend.http_route_guard import RouteDeclaration, build_declared_urlpatterns

    def handler(request):
        return None

    for literal in ("index.html", "assets/index-Ab12.js", "assets/index-Ab12.css",
                    "assets/app.min.js", "ok/", "a-b_c/"):
        patterns = build_declared_urlpatterns([RouteDeclaration(literal, "n-" + literal.replace("/", "-"), handler, True)])
        assert len(patterns) == 2
    print("LITERALS")
''')


_REFUSED_LITERALS_CODE = textwrap.dedent(r'''
    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    from pixs.backend.http_route_guard import HttpRouteGuardError, RouteDeclaration, build_declared_urlpatterns

    def handler(request):
        return None

    for refused in (".", "..", ".htaccess", ".a", "a.", "a..b", "a/./b", "a/../b",
                    "a//b", "/a", "a*b", "<int:x>", "a%b", "a\\b", "a b", "a\n",
                    "assets/.hidden.js", "assets/..", "assets/a..b.js"):
        try:
            build_declared_urlpatterns([RouteDeclaration(refused, "n", handler, True)])
        except HttpRouteGuardError as error:
            assert str(error) == "Déclaration de route invalide."
        else:
            raise AssertionError("refused literal accepted")
    print("REFUSED")
''')


class StaticFilePathLiteralsUnitTests(unittest.TestCase):
    def test_accepted_literals(self):
        result = _run(_ACCEPTED_LITERALS_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("LITERALS", result.stdout)

    def test_refused_literals(self):
        result = _run(_REFUSED_LITERALS_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
