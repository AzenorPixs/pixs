'''Pure unit tests for the bounded health snapshot classifier.'''

import builtins
import itertools
import unittest
from unittest import mock

import pixs.backend.health_classifier as target_module
from pixs.backend.health_classifier import classify_health

_FIELDS = [
    "liveness",
    "startup",
    "availability",
    "degraded",
    "pg_available",
    "required_count",
    "required_ok_count",
    "optional_count",
    "optional_ok_count",
]


class Hostile:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def _record(self, hook: str) -> int:
        self.calls.append(hook)
        return 0

    def __len__(self) -> int:
        return self._record("__len__")

    def __iter__(self):
        self._record("__iter__")
        return iter(())

    def __bool__(self) -> bool:
        return bool(self._record("__bool__"))

    def __int__(self) -> int:
        return self._record("__int__")

    def __index__(self) -> int:
        return self._record("__index__")

    def __hash__(self) -> int:
        return self._record("__hash__")

    def __repr__(self) -> str:
        self._record("__repr__")
        return "hostile"

    def __eq__(self, other: object) -> bool:
        self._record("__eq__")
        return True

    def __getitem__(self, index: object) -> bool:
        self._record("__getitem__")
        return True


class SubTuple(tuple):
    pass


class TestMatriceCombinatoire(unittest.TestCase):
    def test_matrice_32_cas(self) -> None:
        for alive, startup, pg, req_b, opt_b in itertools.product((True, False), repeat=5):
            with self.subTest(alive=alive, startup=startup, pg=pg, req_b=req_b, opt_b=opt_b):
                result = classify_health(alive=alive, startup_complete=startup, pg_available=pg, required=(req_b,), optional=(opt_b,))
                expected = {
                    "liveness": alive,
                    "startup": startup,
                    "availability": alive and startup and pg and req_b,
                    "degraded": not opt_b,
                    "pg_available": pg,
                    "required_count": 2,
                    "required_ok_count": int(pg) + int(req_b),
                    "optional_count": 1,
                    "optional_ok_count": int(opt_b),
                }
                self.assertEqual(result, expected)


class TestTypesExactRefuses(unittest.TestCase):
    def test_scalaires_non_bool_refuses_chaque_slot(self) -> None:
        for bad in (1, 0, "x", None, [], {}, 1.5):
            for name in ("alive", "startup_complete", "pg_available"):
                with self.subTest(bad=bad, slot=name):
                    kwargs = {"alive": True, "startup_complete": True, "pg_available": True}
                    kwargs[name] = bad
                    with self.assertRaises(ValueError) as ctx:
                        classify_health(**kwargs)
                    self.assertEqual(str(ctx.exception), "Invalid health snapshot")
                    self.assertIsNone(ctx.exception.__cause__)

    def test_non_tuple_refuses(self) -> None:
        for bad in (None, [True], "x", {}, iter((True,)), frozenset((True,))):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    classify_health(alive=True, startup_complete=True, pg_available=True, required=bad)

    def test_tuple_subclass_refuse_requis_et_optionnel(self) -> None:
        with self.assertRaises(ValueError):
            classify_health(alive=True, startup_complete=True, pg_available=True, required=SubTuple((True,)))
        with self.assertRaises(ValueError):
            classify_health(alive=True, startup_complete=True, pg_available=True, optional=SubTuple((True,)))

    def test_hooks_hostiles_non_appelles_scalaires(self) -> None:
        for name in ("alive", "startup_complete", "pg_available"):
            hostile = Hostile()
            kwargs = {"alive": True, "startup_complete": True, "pg_available": True}
            kwargs[name] = hostile
            with self.assertRaises(ValueError):
                classify_health(**kwargs)
            self.assertEqual(hostile.calls, [])

    def test_hooks_hostiles_non_appelles_tuples(self) -> None:
        for name in ("required", "optional"):
            hostile = Hostile()
            kwargs = {"alive": True, "startup_complete": True, "pg_available": True}
            kwargs[name] = hostile
            with self.assertRaises(ValueError):
                classify_health(**kwargs)
            self.assertEqual(hostile.calls, [])

    def test_element_hostile_refuse_sans_hooks(self) -> None:
        for name in ("required", "optional"):
            hostile = Hostile()
            kwargs = {"alive": True, "startup_complete": True, "pg_available": True}
            kwargs[name] = (hostile,)
            with self.assertRaises(ValueError):
                classify_health(**kwargs)
            self.assertEqual(hostile.calls, [])


class TestBornesInternes(unittest.TestCase):
    def test_longueur_256_acceptee(self) -> None:
        full = (True,) * 256
        result = classify_health(alive=True, startup_complete=True, pg_available=True, required=full, optional=full)
        self.assertEqual(result["required_count"], 257)
        self.assertEqual(result["required_ok_count"], 257)
        self.assertEqual(result["optional_count"], 256)
        self.assertEqual(result["optional_ok_count"], 256)
        self.assertEqual(result["availability"], True)

    def test_longueur_257_refusee_deux_tuples(self) -> None:
        big = (True,) * 257
        for name in ("required", "optional"):
            kwargs = {"alive": True, "startup_complete": True, "pg_available": True}
            kwargs[name] = big
            with self.assertRaises(ValueError) as ctx:
                classify_health(**kwargs)
            self.assertEqual(str(ctx.exception), "Invalid health snapshot")
            self.assertIsNone(ctx.exception.__cause__)

    def test_espion_type_garde_longueur_avant_elements(self) -> None:
        big = (True,) * 257
        hostile = Hostile()
        cases = (
            ((hostile,), big),
            (big, (hostile,)),
            ((hostile,) + (True,) * 256, ()),
            ((), (hostile,) + (True,) * 256),
        )
        for required, optional in cases:
            spy = mock.Mock(side_effect=lambda obj: builtins.type(obj))
            with mock.patch.object(target_module, "type", create=True, side_effect=spy):
                with self.assertRaises(ValueError):
                    classify_health(alive=True, startup_complete=True, pg_available=True, required=required, optional=optional)
            self.assertEqual(hostile.calls, [])
            self.assertEqual(spy.call_count, 5)
            self.assertTrue(all(call.args[0] is not hostile for call in spy.call_args_list))


class TestFreshDictEtDeterminisme(unittest.TestCase):
    def test_dict_neuf_independant(self) -> None:
        first = classify_health(alive=True, startup_complete=True, pg_available=True, required=(True,), optional=(False,))
        second = classify_health(alive=True, startup_complete=True, pg_available=True, required=(True,), optional=(False,))
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        first["liveness"] = False
        self.assertEqual(second["liveness"], True)

    def test_ordre_champs_fixe(self) -> None:
        result = classify_health(alive=True, startup_complete=True, pg_available=True)
        self.assertEqual(list(result.keys()), _FIELDS)
        again = classify_health(alive=True, startup_complete=True, pg_available=True)
        self.assertEqual(list(result.items()), list(again.items()))

    def test_toutes_valeurs_primitives(self) -> None:
        result = classify_health(alive=True, startup_complete=False, pg_available=True, required=(False,), optional=(True, False))
        for key, value in result.items():
            self.assertIn(type(value), (bool, int), key)
        self.assertEqual(result["availability"], False)
        self.assertEqual(result["degraded"], True)
