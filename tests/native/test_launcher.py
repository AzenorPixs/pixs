"""Recette dédiée du lanceur isolé, à lancer explicitement en phase de tests.

Cette fixture C ne réalise aucune opération PA/PZT, réseau ou PostgreSQL.
Elle qualifie seulement le lanceur avec un runtime minimal de test.
"""
from __future__ import annotations

import ast
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
PROBE = r'''
#include "launcher.h"
#include <string.h>

static PyObject *probe_main(PyObject *self, PyObject *role)
{
    PyObject *argv = PySys_GetObject("argv");
    PyObject *flags = PySys_GetObject("flags");
    PyObject *report = NULL, *representation = NULL, *value = NULL;
    const char *option = "";
    const char *names[] = {"isolated", "ignore_environment", "no_site",
                          "no_user_site", "safe_path", "dont_write_bytecode", NULL};
    int i;
    (void)self;
    if (argv == NULL || flags == NULL) return NULL;
    if (PyList_Size(argv) > 1) {
        option = PyUnicode_AsUTF8(PyList_GetItem(argv, 1));
        if (option == NULL) return NULL;
    }
    if (strcmp(option, "__bool__") == 0) Py_RETURN_TRUE;
    if (strcmp(option, "__negative__") == 0) return PyLong_FromLong(-1);
    if (strcmp(option, "__large__") == 0) return PyLong_FromLong(256);
    if (strcmp(option, "__none__") == 0) Py_RETURN_NONE;
    if (strcmp(option, "__raise__") == 0) {
        PyErr_SetString(PyExc_RuntimeError, "marqueur privé de la fixture");
        return NULL;
    }
    report = PyDict_New();
    if (report == NULL) goto error;
    if (PyDict_SetItemString(report, "role", role) < 0) goto error;
    for (i = 0; names[i] != NULL; i++) {
        value = PyObject_GetAttrString(flags, names[i]);
        if (value == NULL || PyDict_SetItemString(report, names[i], value) < 0) goto error;
        Py_CLEAR(value);
    }
    if (PyDict_SetItemString(report, "path", PySys_GetObject("path")) < 0 ||
        PyDict_SetItemString(report, "prefix", PySys_GetObject("prefix")) < 0 ||
        PyDict_SetItemString(report, "executable", PySys_GetObject("executable")) < 0 ||
        PyDict_SetItemString(report, "argv", argv) < 0) goto error;
    representation = PyObject_Repr(report);
    if (representation == NULL) goto error;
    option = PyUnicode_AsUTF8(representation);
    if (option == NULL) goto error;
    PySys_WriteStdout("%s\n", option);
    Py_DECREF(representation);
    Py_DECREF(report);
    return PyLong_FromLong(0);
error:
    Py_XDECREF(value);
    Py_XDECREF(representation);
    Py_XDECREF(report);
    return NULL;
}
static PyMethodDef methods[] = {
    {"main", probe_main, METH_O, NULL},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef definition = {
    PyModuleDef_HEAD_INIT, "pa01_launcher_probe", NULL, -1, methods,
    NULL, NULL, NULL, NULL
};
PyMODINIT_FUNC PyInit_pa01_launcher_probe(void)
{
    return PyModule_Create(&definition);
}
static struct _inittab builtins[] = {
    {"pa01_launcher_probe", PyInit_pa01_launcher_probe}, {NULL, NULL}
};
const struct pa01_embedded_program pa01_program = {
    1, "pixs-pa-system", "pa01_launcher_probe", builtins
};
'''


class LauncherNativeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.version_info[:3] != (3, 14, 9) or sysconfig.get_config_var("Py_GIL_DISABLED"):
            raise RuntimeError("PA01_TEST_CPYTHON_3149_GIL_REQUIRED")
        if sysconfig.get_config_var("Py_ENABLE_SHARED") != 0:
            raise RuntimeError("PA01_TEST_STATIC_LIBPYTHON_REQUIRED")
        output = ROOT / "output" / "tests" / "pa01-launcher"
        output.mkdir(parents=True, exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(prefix="lanceur-", dir=output)
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.work = Path(cls.temporary.name)
        cls.bundle = cls.work / "bundle"
        (cls.bundle / "bin").mkdir(parents=True)
        standard = cls.bundle / "runtime" / "lib" / "python3.14"
        standard.mkdir(parents=True)
        # Encodings suffit à cette fixture native ; ce n'est pas le runtime D7.
        source = Path(sysconfig.get_path("stdlib")) / "encodings"
        shutil.copytree(source, standard / "encodings",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (standard / "lib-dynload").mkdir()
        fixture = cls.work / "probe.c"
        fixture.write_text(PROBE, encoding="utf-8")
        library = Path(sysconfig.get_config_var("LIBDIR")) / sysconfig.get_config_var("LIBRARY")
        if not library.is_file() or library.suffix != ".a":
            raise RuntimeError("PA01_TEST_STATIC_LIBRARY_UNAVAILABLE")
        cls.executable = cls.bundle / "bin" / "pixs-pa-system"
        result = subprocess.run(
            ["/usr/bin/cc", "-std=c11", "-Wall", "-Wextra",
             "-I" + str(ROOT / "native" / "pa01"),
             "-I" + sysconfig.get_path("include"),
             str(ROOT / "native" / "pa01" / "launcher.c"), str(fixture),
             str(library), "-ldl", "-lm", "-o", str(cls.executable)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60,
            env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}, check=False)
        if result.returncode:
            raise RuntimeError("PA01_TEST_LAUNCHER_BUILD_FAILED\n" + result.stderr)

    def run_probe(self, *arguments, executable=None, cwd=None, environment=None, argv0=None):
        target = self.executable if executable is None else executable
        return subprocess.run(
            [str(target) if argv0 is None else argv0, *arguments],
            executable=str(target), cwd=self.work if cwd is None else cwd,
            env={"PATH": "/aucun-python-hote", "LANG": "C.UTF-8"}
                if environment is None else environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            timeout=15, check=False)

    def assert_report(self, result, bundle, expected_argv):
        self.assertEqual(result.returncode, 0, result.stderr)
        report = ast.literal_eval(result.stdout.strip())
        self.assertEqual(report["role"], "pixs-pa-system")
        self.assertEqual(report["prefix"], str(bundle / "runtime"))
        self.assertEqual(report["executable"], str(bundle / "bin" / "pixs-pa-system"))
        self.assertEqual(report["path"], [
            str(bundle / "runtime" / "lib" / "python3.14"),
            str(bundle / "runtime" / "lib" / "python3.14" / "lib-dynload")])
        self.assertEqual(report["argv"], expected_argv)
        for key in ("isolated", "ignore_environment", "no_site", "no_user_site",
                    "safe_path", "dont_write_bytecode"):
            self.assertTrue(report[key], key)
        return report

    def test_isolated_paths_and_unparsed_arguments(self):
        arguments = ["--mode", "system-daemon", "--arbitrary-probe-argument"]
        self.assert_report(self.run_probe(*arguments), self.bundle,
                           [str(self.executable), *arguments])

    def test_role_does_not_come_from_argv_zero(self):
        self.assert_report(self.run_probe(argv0="identité-falsifiée"), self.bundle,
                           ["identité-falsifiée"])

    def test_relocation_with_spaces_and_unicode_uses_new_relative_runtime(self):
        relocated = self.work / "autre répertoire"
        shutil.copytree(self.bundle, relocated)
        executable = relocated / "bin" / "pixs-pa-system"
        self.assert_report(self.run_probe(executable=executable), relocated, [str(executable)])

    def test_python_environment_and_working_directory_do_not_inject_startup(self):
        hostile = self.work / "hostile"
        hostile.mkdir(exist_ok=True)
        for name in ("sitecustomize.py", "usercustomize.py", "startup.py"):
            (hostile / name).write_text(
                "raise RuntimeError('PA01_TEST_HOSTILE_STARTUP')\n", encoding="utf-8")
        environment = {
            "PATH": "/aucun-python-hote", "LANG": "C.UTF-8",
            "PYTHONPATH": str(hostile), "PYTHONHOME": str(hostile),
            "PYTHONSTARTUP": str(hostile / "startup.py"), "PYTHONINSPECT": "1",
            "PYTHONUSERBASE": str(hostile)}
        self.assert_report(self.run_probe(cwd=hostile, environment=environment),
                           self.bundle, [str(self.executable)])

    def test_wrong_executable_basename_is_rejected_before_python(self):
        alternate = self.bundle / "bin" / "autre-nom"
        shutil.copy2(self.executable, alternate)
        result = self.run_probe(executable=alternate)
        self.assertEqual(result.returncode, 70)
        self.assertEqual(result.stderr.strip(), "PA01_EXECUTABLE_NAME_MISMATCH")

    def test_missing_or_symlinked_runtime_directory_is_rejected(self):
        for kind in ("absent", "lien"):
            relocated = self.work / ("runtime-" + kind)
            shutil.copytree(self.bundle, relocated)
            extensions = relocated / "runtime" / "lib" / "python3.14" / "lib-dynload"
            extensions.rmdir()
            if kind == "lien":
                extensions.symlink_to(self.bundle / "runtime" / "lib" / "python3.14" / "lib-dynload")
            result = self.run_probe(executable=relocated / "bin" / "pixs-pa-system")
            self.assertEqual(result.returncode, 70)
            self.assertEqual(result.stderr.strip(), "PA01_RUNTIME_LAYOUT_UNAVAILABLE")

    def test_invalid_entry_results_and_exception_have_stable_diagnostics(self):
        for argument, diagnostic in (
                ("__bool__", "PA01_ENTRY_EXECUTION_FAILED"),
                ("__none__", "PA01_ENTRY_EXECUTION_FAILED"),
                ("__raise__", "PA01_ENTRY_EXECUTION_FAILED"),
                ("__negative__", "PA01_ENTRY_STATUS_INVALID"),
                ("__large__", "PA01_ENTRY_STATUS_INVALID")):
            with self.subTest(argument=argument):
                result = self.run_probe(argument)
                self.assertEqual(result.returncode, 70)
                self.assertEqual(result.stderr.strip(), diagnostic)
                self.assertNotIn("marqueur privé", result.stderr)


if __name__ == "__main__":
    unittest.main()
