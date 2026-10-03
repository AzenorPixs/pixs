"""Tests unitaires enveloppe succès, sans Django configuré."""

import subprocess
import sys
import unittest


def _run(code):
    return subprocess.run(
        [sys.executable, "-B", "-c", code],
        capture_output=True,
        text=True,
        timeout=30,
    )


_CODE_PUR = """
import sys
assert "django" not in sys.modules
import pixs.backend.api
assert "django" not in sys.modules
import pixs.backend.api.success
assert "django" not in sys.modules
assert "django.http" not in sys.modules
"""

_CODE_VALID = """
from pixs.backend.api import build_success_envelope
e = build_success_envelope([{"a": [1, True, None, "café 真"]}], meta={}, links={})
assert e == {"data": [{"a": [1, True, None, "café 真"]}], "meta": {}, "links": {}}
assert build_success_envelope(None, meta={}, links={})["data"] is None
assert build_success_envelope(True, meta={}, links={})["data"] is True
assert build_success_envelope(False, meta={}, links={})["data"] is False
assert build_success_envelope(10**40, meta={}, links={})["data"] == 10**40
assert build_success_envelope(1.5, meta={}, links={})["data"] == 1.5
"""

_CODE_SUBTYPE = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
class SInt(int): pass
class SStr(str): pass
class SList(list): pass
class SDict(dict): pass
class SBool(int): pass
for bad in (SInt(1), SStr("x"), SList([1]), SDict({"a": 1})):
    try:
        build_success_envelope(bad, meta={}, links={})
    except ApiSuccessEnvelopeError:
        pass
    else:
        raise AssertionError("sous-type rejeté attendu")
import datetime, uuid, decimal
for bad in (datetime.datetime(2026, 1, 1), uuid.UUID(int=1), decimal.Decimal("1.1"), object(), {"a"}, frozenset()):
    try:
        build_success_envelope(bad, meta={}, links={})
    except ApiSuccessEnvelopeError:
        pass
    else:
        raise AssertionError("custom rejeté attendu")
"""

_CODE_HOSTILE_NOSTR = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
class Hostile:
    def __getattribute__(self, name):
        raise AssertionError("inspection interdite")
    def __str__(self):
        raise AssertionError("inspection interdite")
    def __repr__(self):
        raise AssertionError("inspection interdite")
    def __bool__(self):
        raise AssertionError("inspection interdite")
    def __iter__(self):
        raise AssertionError("inspection interdite")
for bad in (Hostile(),):
    try:
        build_success_envelope(bad, meta={}, links={})
    except ApiSuccessEnvelopeError:
        pass
    else:
        raise AssertionError("hostile rejeté attendu")
"""

_CODE_KEYS_FINITE = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
for bad in (float("nan"), float("inf"), float("-inf")):
    try:
        build_success_envelope(bad, meta={}, links={})
    except ApiSuccessEnvelopeError:
        pass
    else:
        raise AssertionError("fini attendu")
    try:
        build_success_envelope({"a": bad}, meta={}, links={})
    except ApiSuccessEnvelopeError:
        pass
    else:
        raise AssertionError("fini imbriqué attendu")
for k in (1, True, None, ("a",), frozenset({"a"})):
    try:
        build_success_envelope({k: 1}, meta={}, links={})
    except ApiSuccessEnvelopeError:
        pass
    else:
        raise AssertionError("clé str exacte attendue")
"""

_CODE_HOSTILE_KEY = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
guard = False
class Evil:
    def __eq__(self, other):
        raise AssertionError("__eq__ interdit")
    def __hash__(self):
        if guard:
            raise AssertionError("__hash__ interdit")
        return 42
bad = {Evil(): 1}
guard = True
try:
    build_success_envelope(bad, meta={}, links={})
except ApiSuccessEnvelopeError:
    pass
else:
    raise AssertionError("clé hostile rejetée attendue")
class HostileMeta(type):
    def __eq__(self, other):
        raise AssertionError("égalité de type interdite")
    def __hash__(self):
        raise AssertionError("hachage de type interdit")
class Opaque(metaclass=HostileMeta):
    pass
try:
    build_success_envelope(Opaque(), meta={}, links={})
except ApiSuccessEnvelopeError:
    pass
else:
    raise AssertionError("type hostile rejeté attendu")
"""

_CODE_COPY_ALIAS = """
from pixs.backend.api import build_success_envelope
inner = {"x": [1, 2]}
data = [inner, inner]
meta = {"m": [7]}
links = {"next": {"label": ["x"]}}
e = build_success_envelope(data, meta=meta, links=links)
assert e["data"][0] == e["data"][1] == {"x": [1, 2]}
assert e["data"][0] is not e["data"][1]
assert e["data"][0] is not inner and e["data"][0]["x"] is not inner["x"]
data[0]["x"].append(99)
inner["x"].append(100)
assert e["data"] == [{"x": [1, 2]}, {"x": [1, 2]}]
meta["m"].append(8)
links["next"]["label"].append("y")
assert e["meta"] == {"m": [7]}
assert e["links"] == {"next": {"label": ["x"]}}
e["data"][0]["x"].append(3)
assert e["data"][1]["x"] == [1, 2]
assert inner["x"] == [1, 2, 99, 100]
"""

_CODE_CYCLE = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
a = []
a.append(a)
try:
    build_success_envelope(a, meta={}, links={})
except ApiSuccessEnvelopeError as exc:
    assert str(exc) == "Enveloppe de succès invalide."
else:
    raise AssertionError("cycle list attendu")
b = {}
b["self"] = b
try:
    build_success_envelope(b, meta={}, links={})
except ApiSuccessEnvelopeError:
    pass
else:
    raise AssertionError("cycle dict attendu")
"""

_CODE_DEPTH = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
v = []
for _ in range(10000):
    v = [v]
try:
    build_success_envelope(v, meta={}, links={})
except ApiSuccessEnvelopeError as exc:
    assert str(exc) == "Enveloppe de succès invalide."
    assert "RecursionError" not in type(exc).__name__
else:
    raise AssertionError("profondeur rejetée attendue")
"""

_CODE_KW = """
import inspect
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
sig = inspect.signature(build_success_envelope)
assert sig.parameters["meta"].kind is inspect.Parameter.KEYWORD_ONLY
assert sig.parameters["links"].kind is inspect.Parameter.KEYWORD_ONLY
assert sig.parameters["meta"].default is inspect.Parameter.empty
assert sig.parameters["links"].default is inspect.Parameter.empty
for args, kw in (((), {}), ((1,), {}), ((1,), {"meta": {}}), ((1, {}, {}), {})):
    try:
        build_success_envelope(*args, **kw)
    except TypeError:
        pass
    else:
        raise AssertionError("TypeError attendu")
for bad in (None, [], "x", True):
    for kw in ({"meta": bad, "links": {}}, {"meta": {}, "links": bad}):
        try:
            build_success_envelope(1, **kw)
        except ApiSuccessEnvelopeError:
            pass
        else:
            raise AssertionError("dict exact attendu")
"""

_CODE_DIAG = """
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope
try:
    build_success_envelope(object(), meta={}, links={})
except ApiSuccessEnvelopeError as exc:
    assert str(exc) == "Enveloppe de succès invalide."
    assert exc.__cause__ is None
    assert exc.__context__ is None
else:
    raise AssertionError("diagnostic attendu")
assert issubclass(ApiSuccessEnvelopeError, ValueError)
"""

_CODE_LAZY = """
import sys
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_envelope, build_success_response
try:
    build_success_response(object(), meta={}, links={})
except ApiSuccessEnvelopeError:
    pass
else:
    raise AssertionError("pur avant Django attendu")
assert "django" not in sys.modules
assert "django.conf" not in sys.modules
assert "django.http" not in sys.modules
"""

_CODE_NODJANGO = """
import sys
sys.modules["django"] = None
sys.modules["django.conf"] = None
sys.modules["django.http"] = None
sys.modules["django.core"] = None
sys.modules["django.core.exceptions"] = None
from pixs.backend.api import build_success_response
try:
    build_success_response(1, meta={}, links={})
except ImportError:
    pass
else:
    raise AssertionError("ImportError attendue")
"""


class SuccessUnit(unittest.TestCase):
    def test_import_pur(self):
        proc = _run(_CODE_PUR)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_valeurs_json_finies(self):
        proc = _run(_CODE_VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_sous_types_et_custom_rejetes(self):
        proc = _run(_CODE_SUBTYPE)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_hostile_sans_str_repr(self):
        proc = _run(_CODE_HOSTILE_NOSTR)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_cles_et_finitude(self):
        proc = _run(_CODE_KEYS_FINITE)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_cle_hostile_sans_eq_hash(self):
        proc = _run(_CODE_HOSTILE_KEY)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_copie_profonde_alias(self):
        proc = _run(_CODE_COPY_ALIAS)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_cycles_rejetes(self):
        proc = _run(_CODE_CYCLE)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_profondeur_native_convertie(self):
        proc = _run(_CODE_DEPTH)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_signature_keyword_required(self):
        proc = _run(_CODE_KW)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_diagnostic_constant(self):
        proc = _run(_CODE_DIAG)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_validation_avant_django(self):
        proc = _run(_CODE_LAZY)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_sans_django_importerror(self):
        proc = _run(_CODE_NODJANGO)
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
