"""Intégration sûre de la déclaration passive d'enregistrement : import et validation gardés."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "EVENT_REGISTRATION_SAFE_INTEGRATION_OK\n"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(
    r'''
    import builtins
    import dataclasses
    import datetime
    import importlib.util
    import io
    import os
    import socket
    import subprocess
    import sys
    import time

    sys.path.insert(0, sys.argv[1])

    from unittest import mock

    FORBIDDEN_IMPORT_PREFIXES = ("django", "psycopg", "psycopg2", "psycopg_pool", "psycopg_binary")


    class ForbiddenImportFinder:
        def __init__(self):
            self.calls = []

        def find_spec(self, fullname, path=None, target=None):
            for prefix in FORBIDDEN_IMPORT_PREFIXES:
                if fullname == prefix or fullname.startswith(prefix + "."):
                    self.calls.append(fullname)
                    raise AssertionError("forbidden base import")
            return None


    import_guard = ForbiddenImportFinder()
    sys.meta_path.insert(0, import_guard)

    original_datetime = datetime.datetime
    original_date = datetime.date


    class GuardedDatetime(original_datetime):
        clock_calls = []

        @classmethod
        def now(cls, tz=None):
            cls.clock_calls.append("now")
            raise AssertionError("forbidden clock")

        @classmethod
        def today(cls):
            cls.clock_calls.append("today")
            raise AssertionError("forbidden clock")

        @classmethod
        def utcnow(cls):
            cls.clock_calls.append("utcnow")
            raise AssertionError("forbidden clock")


    datetime.datetime = GuardedDatetime


    class GuardedDate(original_date):
        clock_calls = []

        @classmethod
        def today(cls):
            cls.clock_calls.append("today")
            raise AssertionError("forbidden date clock")

    datetime.date = GuardedDate
    try:
        datetime.date.today()
    except AssertionError:
        pass
    else:
        raise AssertionError("date clock guard inactive")
    assert GuardedDate.clock_calls == ["today"]
    GuardedDate.clock_calls.clear()


    class GuardedEnvironment:
        def __init__(self):
            self.calls = []

        def _forbid(self, name):
            self.calls.append(name)
            raise AssertionError("forbidden environment")

        def __getitem__(self, key):
            self._forbid("getitem")

        def get(self, key, default=None):
            self._forbid("get")


    environment_guard = GuardedEnvironment()
    os.environ = environment_guard

    function_guards = []


    def install_function_guard(target, name, args):
        guard = mock.Mock(side_effect=AssertionError("forbidden"))
        setattr(target, name, guard)
        function_guards.append((target, name, args, guard))


    install_function_guard(socket.socket, "connect", (object(), ("127.0.0.1", 0)))
    install_function_guard(socket, "create_connection", (("127.0.0.1", 0),))
    install_function_guard(subprocess, "Popen", (["true"],))
    install_function_guard(subprocess, "run", (["true"],))
    install_function_guard(os, "system", ("true",))
    install_function_guard(os, "popen", ("true",))
    install_function_guard(os, "getenv", ("PATH",))
    install_function_guard(time, "time", ())
    install_function_guard(time, "monotonic", ())
    install_function_guard(time, "perf_counter", ())
    install_function_guard(time, "sleep", (0,))

    for target, name, args, guard in function_guards:
        try:
            getattr(target, name)(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError("function guard inactive")
        assert guard.call_count == 1
        guard.reset_mock()

    for forbidden in FORBIDDEN_IMPORT_PREFIXES:
        try:
            importlib.util.find_spec(forbidden)
        except AssertionError:
            pass
        else:
            raise AssertionError("import guard inactive")
        assert import_guard.calls == [forbidden]
        import_guard.calls.clear()

    for method_name in ("now", "today", "utcnow"):
        try:
            getattr(datetime.datetime, method_name)()
        except AssertionError:
            pass
        else:
            raise AssertionError("clock guard inactive")

    assert GuardedDatetime.clock_calls == ["now", "today", "utcnow"]
    GuardedDatetime.clock_calls.clear()

    for operation, expected_call in (
        (lambda: os.environ["PATH"], "getitem"),
        (lambda: os.environ.get("PATH"), "get"),
    ):
        try:
            operation()
        except AssertionError:
            pass
        else:
            raise AssertionError("environment guard inactive")
        assert environment_guard.calls[-1] == expected_call

    assert environment_guard.calls == ["getitem", "get"]
    environment_guard.calls.clear()

    from pixs.kernel.diagnostics import VALIDATE
    from pixs.kernel.event_contract import (
        DomainEventContract, IntegrationEventContract,
    )
    from pixs.kernel.event_registration import (
        EventRegistrationDeclarationV1,
        validate_event_registration_declaration,
    )

    # Contrôle après bootstrap : aucun accès applicatif interdit masqué.
    for _, _, _, guard in function_guards:
        assert guard.call_count == 0
    assert environment_guard.calls == []
    assert import_guard.calls == []
    assert GuardedDatetime.clock_calls == []
    assert GuardedDate.clock_calls == []

    # Imports normaux achevés ; sondes fichiers armées pour la validation.
    # Les chargements physiques normaux du loader sont hors scope applicatif.
    file_guard_calls = []


    def make_file_guard(route):
        def forbidden(*args, **kwargs):
            file_guard_calls.append(route)
            raise AssertionError("forbidden file access")

        return forbidden


    file_guard_targets = (
        (builtins, "open"),
        (io, "open"),
        (os, "open"),
    )
    for target, name in file_guard_targets:
        setattr(target, name, make_file_guard(f"{'builtins' if target is builtins else 'io' if target is io else 'os'}.{name}"))

    file_probe_operations = (
        (lambda: builtins.open(os.devnull), "builtins.open"),
        (lambda: io.open(os.devnull), "io.open"),
        (lambda: os.open(os.devnull, os.O_RDONLY), "os.open"),
    )
    for operation, expected_route in file_probe_operations:
        try:
            operation()
        except AssertionError:
            pass
        else:
            raise AssertionError("file guard inactive")
        assert file_guard_calls[-1] == expected_route

    assert file_guard_calls == [expected for _, expected in file_probe_operations]
    file_guard_calls.clear()


    class CountingStr(str):
        def __new__(cls, value):
            instance = super().__new__(cls, value)
            object.__setattr__(instance, "calls", [])
            return instance

        def __bool__(self):
            self.calls.append("bool")
            return True

        def __len__(self):
            self.calls.append("len")
            return str.__len__(self)

        def __str__(self):
            self.calls.append("str")
            return "counting-str"


    def contract_values(**overrides):
        result = {
            "event_type": "synthetic.event",
            "contract_version": "1.2.3",
            "producer_reference": "producer-synthetic",
            "schema_reference": "schema-synthetic",
            "order_scope_reference": "scope-synthetic",
        }
        result.update(overrides)
        return result

    for contract_type in (DomainEventContract, IntegrationEventContract):
        contract = contract_type(**contract_values())
        declaration = EventRegistrationDeclarationV1(
            owner_id="owner-synthetic",
            entry_id="entry-synthetic",
            event_contract=contract,
        )
        assert declaration.event_contract is contract
        before = dataclasses.asdict(contract)
        first = validate_event_registration_declaration(declaration)
        second = validate_event_registration_declaration(declaration)
        assert first == [] and second == [] and first is not second
        first.append("synthetic local mutation")
        assert second == [] and validate_event_registration_declaration(declaration) == []
        assert dataclasses.asdict(contract) == before

    hostile_value = CountingStr("SENTINEL")
    assert bool(hostile_value) is True
    assert len(hostile_value) == len("SENTINEL")
    assert str(hostile_value) == "counting-str"
    assert hostile_value.calls == ["bool", "len", "str"]
    hostile_value.calls.clear()

    foreign_declaration = validate_event_registration_declaration(object())
    assert len(foreign_declaration) == 1
    assert foreign_declaration[0].element == "event_registration.declaration"
    assert foreign_declaration[0].step == VALIDATE

    bad_identifiers = EventRegistrationDeclarationV1(
        owner_id=hostile_value,
        entry_id="",
        event_contract=DomainEventContract(**contract_values()),
    )
    identifier_refusals = validate_event_registration_declaration(bad_identifiers)
    assert {item.element for item in identifier_refusals} == {
        "event_registration.owner_id",
        "event_registration.entry_id",
    }
    assert all(item.step == VALIDATE for item in identifier_refusals)
    assert hostile_value.calls == []
    assert "SENTINEL" not in "".join(
        f"{item.element}{item.constraint}{item.message}{item}"
        for item in identifier_refusals
    )

    foreign_contract = EventRegistrationDeclarationV1(
        owner_id="owner-synthetic",
        entry_id="entry-synthetic",
        event_contract=object(),
    )
    contract_refusal = validate_event_registration_declaration(foreign_contract)
    assert len(contract_refusal) == 1
    assert contract_refusal[0].element == "event_registration.event_contract"
    assert contract_refusal[0].step == VALIDATE

    sentinel = "SENTINEL_SYNTHETIC_INVALID"
    invalid_contract = DomainEventContract(
        **contract_values(contract_version=sentinel)
    )
    invalid_declaration = EventRegistrationDeclarationV1(
        owner_id="owner-synthetic",
        entry_id="entry-synthetic",
        event_contract=invalid_contract,
    )
    invalid_refusals = validate_event_registration_declaration(invalid_declaration)
    assert len(invalid_refusals) == 1
    assert invalid_refusals[0].element == "event_contract.contract_version"
    assert sentinel not in invalid_refusals[0].message
    assert sentinel not in invalid_refusals[0].constraint

    for _, _, _, guard in function_guards:
        assert guard.call_count == 0
    assert environment_guard.calls == []
    assert import_guard.calls == []
    assert GuardedDatetime.clock_calls == []
    assert GuardedDate.clock_calls == []
    assert file_guard_calls == []

    print("EVENT_REGISTRATION_SAFE_INTEGRATION_OK")
    '''
).strip()


class EventRegistrationIntegrationTests(unittest.TestCase):
    def test_fresh_guarded_import_and_validation(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
