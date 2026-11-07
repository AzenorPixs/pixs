/* Lanceur Debian 13 x86_64 PA01 : initialisation isolée, sans autorité métier. */
#define _XOPEN_SOURCE 700
#define PY_SSIZE_T_CLEAN
#include "launcher.h"
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#if !defined(__linux__) || !defined(__x86_64__)
#error "PA01 : cible non qualifiee par ce lanceur"
#endif
#if PY_MAJOR_VERSION != 3 || PY_MINOR_VERSION != 14 || PY_MICRO_VERSION != 9
#error "PA01 : CPython 3.14.9 requis par le candidat D1"
#endif
#ifdef Py_GIL_DISABLED
#error "PA01 : candidat avec GIL requis"
#endif

static int fail(const char *code)
{
    fprintf(stderr, "%s\n", code);
    return 70;
}

static int known_executable(const char *name)
{
    return name != NULL &&
        (strcmp(name, "pixs-pa-system") == 0 ||
         strcmp(name, "pixs-pa-events") == 0 ||
         strcmp(name, "pixs-pa-session") == 0 ||
         strcmp(name, "pzt") == 0);
}

static int directory_without_link(const char *path)
{
    struct stat info;
    return lstat(path, &info) == 0 && S_ISDIR(info.st_mode);
}

static int join_path(char *out, size_t size, const char *base, const char *suffix)
{
    int count = snprintf(out, size, "%s/%s", base, suffix);
    return count >= 0 && (size_t)count < size;
}

static int append_search_path(PyConfig *config, const char *path)
{
    wchar_t *wide = Py_DecodeLocale(path, NULL);
    PyStatus status;
    if (wide == NULL)
        return 0;
    status = PyWideStringList_Append(&config->module_search_paths, wide);
    PyMem_RawFree(wide);
    return !PyStatus_Exception(status);
}

static int set_path(PyConfig *config, wchar_t **field, const char *value)
{
    return !PyStatus_Exception(PyConfig_SetBytesString(config, field, value));
}

int main(int argc, char **argv)
{
    char native[PATH_MAX], executable[PATH_MAX], bundle[PATH_MAX];
    char runtime[PATH_MAX], runtime_lib[PATH_MAX];
    char stdlib[PATH_MAX], extensions[PATH_MAX];
    struct stat running, installed;
    char *separator;
    ssize_t count;
    PyPreConfig preconfig;
    PyConfig config;
    PyStatus status;
    PyObject *module = NULL, *callable = NULL, *role = NULL, *result = NULL;
    int exit_code = 70;
    long returned;

    if (pa01_program.schema_version != 1 ||
        !known_executable(pa01_program.executable) ||
        pa01_program.entry_module == NULL || pa01_program.modules == NULL)
        return fail("PA01_BUILD_DESCRIPTOR_INVALID");

    count = readlink("/proc/self/exe", native, sizeof(native) - 1);
    if (count <= 0 || (size_t)count >= sizeof(native) - 1)
        return fail("PA01_EXECUTABLE_PATH_UNAVAILABLE");
    native[count] = '\0';
    if (realpath(native, executable) == NULL ||
        stat("/proc/self/exe", &running) != 0 ||
        stat(executable, &installed) != 0 ||
        !S_ISREG(installed.st_mode) ||
        running.st_dev != installed.st_dev || running.st_ino != installed.st_ino)
        return fail("PA01_EXECUTABLE_IDENTITY_MISMATCH");

    separator = strrchr(executable, '/');
    if (separator == NULL || strcmp(separator + 1, pa01_program.executable) != 0)
        return fail("PA01_EXECUTABLE_NAME_MISMATCH");
    memcpy(bundle, executable, strlen(executable) + 1);
    separator = strrchr(bundle, '/');
    *separator = '\0';
    separator = strrchr(bundle, '/');
    if (separator == NULL || strcmp(separator + 1, "bin") != 0)
        return fail("PA01_BUNDLE_LAYOUT_INVALID");
    *separator = '\0';
    if (bundle[0] == '\0' ||
        !join_path(runtime, sizeof(runtime), bundle, "runtime") ||
        !join_path(runtime_lib, sizeof(runtime_lib), runtime, "lib") ||
        !join_path(stdlib, sizeof(stdlib), runtime_lib, "python3.14") ||
        !join_path(extensions, sizeof(extensions), stdlib, "lib-dynload") ||
        !directory_without_link(runtime) || !directory_without_link(runtime_lib) ||
        !directory_without_link(stdlib) || !directory_without_link(extensions))
        return fail("PA01_RUNTIME_LAYOUT_UNAVAILABLE");

    if (PyImport_ExtendInittab(pa01_program.modules) != 0)
        return fail("PA01_BUILTIN_REGISTRY_UNAVAILABLE");

    PyPreConfig_InitIsolatedConfig(&preconfig);
    preconfig.utf8_mode = 1;
    preconfig.configure_locale = 0;
    status = Py_PreInitialize(&preconfig);
    if (PyStatus_Exception(status))
        return fail("PA01_PREINITIALIZATION_FAILED");

    PyConfig_InitIsolatedConfig(&config);
    config.use_environment = 0;
    config.user_site_directory = 0;
    config.site_import = 0;
    config.write_bytecode = 0;
    config.safe_path = 1;
    config.parse_argv = 0;
    config.install_signal_handlers = 0;
    config.module_search_paths_set = 1;
    if (!set_path(&config, &config.program_name, executable) ||
        !set_path(&config, &config.executable, executable) ||
        !set_path(&config, &config.home, runtime) ||
        !set_path(&config, &config.prefix, runtime) ||
        !set_path(&config, &config.base_prefix, runtime) ||
        !set_path(&config, &config.exec_prefix, runtime) ||
        !set_path(&config, &config.base_exec_prefix, runtime) ||
        !set_path(&config, &config.stdlib_dir, stdlib) ||
        !append_search_path(&config, stdlib) ||
        !append_search_path(&config, extensions)) {
        PyConfig_Clear(&config);
        return fail("PA01_RUNTIME_CONFIGURATION_FAILED");
    }
    status = PyConfig_SetBytesArgv(&config, argc, argv);
    if (!PyStatus_Exception(status))
        status = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(status))
        return fail("PA01_INITIALIZATION_FAILED");

    module = PyImport_ImportModule(pa01_program.entry_module);
    if (module == NULL) {
        fail("PA01_ENTRY_MODULE_UNAVAILABLE");
        goto cleanup;
    }
    callable = PyObject_GetAttrString(module, "main");
    role = PyUnicode_FromString(pa01_program.executable);
    if (callable == NULL || !PyCallable_Check(callable) || role == NULL) {
        fail("PA01_ENTRY_CONTRACT_INVALID");
        goto cleanup;
    }
    result = PyObject_CallOneArg(callable, role);
    if (result == NULL || !PyLong_CheckExact(result)) {
        fail("PA01_ENTRY_EXECUTION_FAILED");
        goto cleanup;
    }
    returned = PyLong_AsLong(result);
    if (PyErr_Occurred() || returned < 0 || returned > 255) {
        fail("PA01_ENTRY_STATUS_INVALID");
        goto cleanup;
    }
    exit_code = (int)returned;

cleanup:
    Py_XDECREF(result);
    Py_XDECREF(role);
    Py_XDECREF(callable);
    Py_XDECREF(module);
    PyErr_Clear();
    if (Py_FinalizeEx() < 0 && exit_code == 0)
        exit_code = 120;
    return exit_code;
}
