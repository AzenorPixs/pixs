"""Comportement sans connexion, aucun connect appele."""
from __future__ import annotations

import copy
import os
import pickle
import subprocess
import sys
import threading
import unittest

try:
    import libpq_inspection as inspection
except ImportError as error:
    raise RuntimeError("PA01_TEST_LIBPQ_INSPECTION_BUILD_REQUIRED") from error

def valid_arguments():
    return (b"/socket-test", b"55432", b"base-test", b"role-test", b"compte-test", b"2", b"1000", b"500", b"1500", b"160015")

class InspectionBehaviorTest(unittest.TestCase):
    def test_valid_construction_and_close_idempotent(self):
        item = inspection.LibpqInspection(valid_arguments())
        item.close()
        item.close()

    def test_rejects_types_and_empty(self):
        for bad in (None, "texte", valid_arguments()[:9], valid_arguments() + (b"x",)):
            with self.subTest(bad=type(bad)):
                with self.assertRaises(inspection.InspectionError):
                    inspection.LibpqInspection(bad)

    def test_rejects_controls_and_nul(self):
        for value in (b"a\x00b", b"a\x1fb", b"a\x7fb"):
            with self.subTest():
                with self.assertRaises(inspection.InspectionError):
                    inspection.LibpqInspection((b"/s", b"55432", value, b"u", b"o", b"2", b"1", b"1", b"1", b"170011"))

    def test_rejects_multihost_and_relative_socket(self):
        for value in (b"localhost", b"/a,/b", b"relative", b"/a/../b", b"/a//b"):
            with self.subTest(value=value):
                with self.assertRaises(inspection.InspectionError):
                    inspection.LibpqInspection((value, b"55432", b"d", b"u", b"o", b"2", b"1", b"1", b"1", b"170011"))

    def test_rejects_non_ascii_and_out_of_range_numbers(self):
        with self.assertRaises(inspection.InspectionError):
            inspection.LibpqInspection((b"/s", b"caf\xc3\xa9", b"d", b"u", b"o", b"2", b"1", b"1", b"1", b"170011"))
        for field, value in ((1, b"0"), (1, b"65536"), (5, b"0"), (9, b"0")):
            arguments = list(valid_arguments())
            arguments[field] = value
            with self.assertRaises(inspection.InspectionError):
                inspection.LibpqInspection(tuple(arguments))

    def test_no_sql_ddl_public_api(self):
        item = inspection.LibpqInspection(valid_arguments())
        try:
            for name in ("execute", "sql", "ddl", "query", "mutate", "pzt_handler"):
                self.assertFalse(hasattr(item, name))
        finally:
            item.close()

    def test_repr_pickle_copy_subclass_closed(self):
        item = inspection.LibpqInspection(valid_arguments())
        try:
            self.assertNotIn("role-test", repr(item))
            with self.assertRaises(TypeError):
                pickle.dumps(item)
            with self.assertRaises(TypeError):
                copy.copy(item)
            with self.assertRaises(TypeError):
                copy.deepcopy(item)
            with self.assertRaises(TypeError):
                type("SousClasse", (type(item),), {})()
            item.close()
            with self.assertRaises(inspection.InspectionError):
                item.inspect_technical(b"role", b"database", 4096)
        finally:
            item.close()

    def test_context_and_cross_thread_owner(self):
        item = inspection.LibpqInspection(valid_arguments())
        try:
            with item:
                pass
            errors = []
            def other():
                try:
                    item.close()
                except inspection.InspectionError as error:
                    errors.append(error)
            thread = threading.Thread(target=other)
            thread.start()
            thread.join()
            self.assertEqual(len(errors), 1)
        finally:
            item.close()

    def test_invalid_result_budget_is_rejected_without_connecting(self):
        item = inspection.LibpqInspection(valid_arguments())
        try:
            for budget in (None, False, 0, -1, 2147483648):
                with self.subTest(budget=budget):
                    with self.assertRaisesRegex(inspection.InspectionError, "PA01_SQL_ARGUMENT_INVALID"):
                        item.inspect_technical(b"role", b"base", budget)
        finally:
            item.close()

    def test_context_propagates_body_exception_and_closes(self):
        item = inspection.LibpqInspection(valid_arguments())
        with self.assertRaisesRegex(ValueError, "erreur du corps"):
            with item:
                raise ValueError("erreur du corps")
        with self.assertRaisesRegex(inspection.InspectionError, "PA01_SQL_CLOSED"):
            item.inspect_technical(b"role", b"base", 4096)

    def test_postgres_c_environment_is_refused_in_controlled_subprocess(self):
        from pathlib import Path
        folder = str(Path(inspection.__file__).resolve().parent)
        arguments = repr(valid_arguments())
        prefix = "import sys; sys.path.insert(0, sys.argv[1]); import libpq_inspection as m; "
        base = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}
        for setting, environment, marker, extra in (
                ("", base | {"PGHOST": "marqueur-serveur"}, "marqueur-serveur", []),
                ("import os, sys; os.putenv('PGHOST', sys.argv[2]); ", base, "marqueur-putenv", ["marqueur-putenv"])):
            code = setting + prefix + "m.LibpqInspection(" + arguments + ")"
            result = subprocess.run(
                [sys.executable, "-I", "-S", "-B", "-c", code, folder, *extra],
                capture_output=True, text=True, timeout=15, env=environment, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PA01_SQL_ENVIRONMENT_FORBIDDEN", result.stderr)
            self.assertNotIn(marker, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
