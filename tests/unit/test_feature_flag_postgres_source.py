"""Chargeur PostgreSQL des fanions : contrat, paresse, refus fermés et absence d’effets."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_CACHE = str(_ROOT / "frontend" / ".cache")
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
    "TMPDIR": _CACHE,
}

_IMPORT_CHILD = textwrap.dedent(
    r'''
    import builtins
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from importlib.abc import MetaPathFinder
    from pathlib import Path
    from unittest import mock

    sys.path.insert(0, sys.argv[1])

    import django
    from django.conf import settings
    from django.apps import apps
    assert not settings.configured and not apps.ready
    import psycopg
    from psycopg import Connection
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

    _ERROR = "Source de fanions indisponible"

    class ForbiddenLateImports(MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname in {"pixs.backend.models", "django.db.utils"}:
                raise AssertionError("import prématuré du modèle ou de Django DB")
            return None

    finder = ForbiddenLateImports()
    sys.meta_path.insert(0, finder)

    guard_targets = (
        (django, "setup"),
        (type(settings), "configure"),
        (psycopg, "connect"),
        (Connection, "connect"),
        (PGWrapper, "get_new_connection"),
        (socket.socket, "connect"),
        (socket, "create_connection"),
        (subprocess, "Popen"),
        (subprocess, "run"),
        (os, "system"),
        (os, "remove"),
        (os, "rename"),
        (os, "mkdir"),
        (os, "putenv"),
        (type(os.environ), "__setitem__"),
        (builtins, "open"),
        (Path, "open"),
    )
    guards = [
        mock.Mock(side_effect=AssertionError("forbidden"))
        for _ in guard_targets
    ]

    for guard in guards:
        try:
            guard()
        except AssertionError:
            pass
        else:
            raise AssertionError("garde inactive")
        assert guard.call_count == 1
        guard.reset_mock()

    with ExitStack() as stack:
        for (target, name), mock_guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, mock_guard))

        import pixs.backend.feature_flag_postgres_source as loader

        assert tuple(loader.__all__) == (
            "FeatureFlagSourceLoadError",
            "load_feature_flag_source_snapshot",
        )
        assert issubclass(loader.FeatureFlagSourceLoadError, ValueError)
        assert loader.load_feature_flag_source_snapshot.__annotations__ == {
            "expected_configuration_version": "str",
            "return": "FeatureFlagSourceSnapshot",
        }

        direct_error = loader.FeatureFlagSourceLoadError()
        assert str(direct_error) == _ERROR
        assert direct_error.__cause__ is None

        callbacks = []

        class VersionStr(str):
            def __bool__(self):
                callbacks.append("bool")
                raise AssertionError("callback hostile")
            def __str__(self):
                callbacks.append("str")
                raise AssertionError("callback hostile")
            def __eq__(self, other):
                callbacks.append("eq")
                raise AssertionError("callback hostile")

        invalid_versions = (
            None,
            False,
            True,
            1,
            "",
            VersionStr("opaque-version"),
        )

        for invalid_version in invalid_versions:
            try:
                loader.load_feature_flag_source_snapshot(invalid_version)
            except loader.FeatureFlagSourceLoadError as caught:
                assert str(caught) == _ERROR
                assert caught.__cause__ is None
                assert caught.__suppress_context__ is True
            else:
                raise AssertionError("version invalide acceptée")

        assert callbacks == []
        assert not settings.configured and not apps.ready
        assert "pixs.backend.models" not in sys.modules
        assert sys.meta_path[0] is finder
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    sys.meta_path.remove(finder)
    print("FEATURE_FLAG_POSTGRES_SOURCE_IMPORT_OK")
    '''
).strip()

_BEHAVIOUR_CHILD = textwrap.dedent(
    r'''
    import builtins
    import datetime
    import json
    import os
    import socket
    import subprocess
    import sys
    import time
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock

    sys.path.insert(0, sys.argv[1])

    import psycopg
    from psycopg import Connection
    from django.apps import apps
    from django.conf import settings
    from django.db import connection
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from django.db.utils import DatabaseError
    import django

    assert not settings.configured
    assert not apps.ready

    settings.configure(
        DEFAULT_CHARSET="utf-8",
        INSTALLED_APPS=("pixs.backend",),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
            }
        },
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    django.setup()

    from pixs.backend.models import FeatureFlagSourceSnapshotRecord as Record
    from pixs.backend.feature_flag_snapshot_codec import (
        FeatureFlagSnapshotCodecError,
        decode_feature_flag_source_snapshot,
        encode_feature_flag_source_snapshot,
    )
    import pixs.backend.feature_flag_postgres_source as loader
    import pixs.kernel.feature_flag_sources as sources
    from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule
    from pixs.kernel.feature_flags import (
        FeatureFlagAssignment,
        FeatureFlagDefinition,
    )

    _ERROR = "Source de fanions indisponible"
    _CFG = "cfg-source"
    _FLAG = "web.dark_mode"
    _PAST = "2025-01-01T00:00:00Z"
    _FAR = "2099-01-01T00:00:00Z"
    _ROOT_KEYS = (
        "configuration_version",
        "definitions",
        "assignments",
        "cohort_rules",
    )

    import pixs.kernel.feature_flags as flags

    class GuardedDateTime(datetime.datetime):
        pass

    import pixs.backend.feature_flag_snapshot_codec as codec_module
    real_decode = decode_feature_flag_source_snapshot

    class WrongSnapshot(sources.FeatureFlagSourceSnapshot):
        pass

    def _definition(**overrides):
        values = {
            "flag_id": _FLAG,
            "flag_version": "v1",
            "owner_component": "web-main",
            "purpose": "Source PostgreSQL",
            "value_schema": "BOOLEAN",
            "default_value": False,
            "targeting_dimensions": ("TENANT",),
            "cohort_key": None,
            "prerequisites": (),
            "fallback_policy": "DENY",
            "expires_at": _FAR,
            "audit_policy": "standard",
        }
        values.update(overrides)
        return FeatureFlagDefinition(**values)

    def _assignment(version=_CFG, value=False):
        return FeatureFlagAssignment(
            flag_id=_FLAG,
            selector="TENANT",
            selector_value="tenant-a",
            value=value,
            valid_from=_PAST,
            valid_until=_FAR,
            configuration_version=version,
            updated_by="administrator.1",
        )

    def _snapshot(version=_CFG):
        return sources.FeatureFlagSourceSnapshot(
            version,
            (_definition(),),
            (_assignment(version=version),),
            (),
        )

    def _record_for(version, document):
        record = Record()
        record.configuration_version = version
        record.snapshot = document
        return record

    def _copy_document(document):
        return json.loads(json.dumps(document))

    def _copy_record(document, collection):
        result = _copy_document(document)
        records = list(result[collection])
        records[0] = dict(records[0])
        result[collection] = records
        return result

    def _add_root_key(document, key):
        result = _copy_document(document)
        result[key] = "x"
        return result

    def _remove_root_key(document, key):
        result = _copy_document(document)
        result.pop(key)
        return result

    def _set_record_field(document, collection, key, value):
        result = _copy_record(document, collection)
        result[collection][0][key] = value
        return result

    def _decode_spy(calls):
        def decode(document):
            calls.append(document)
            return real_decode(document)

        return decode

    def _assert_load_error(action):
        try:
            action()
        except loader.FeatureFlagSourceLoadError as caught:
            assert str(caught) == _ERROR
            assert caught.__cause__ is None
            assert caught.__suppress_context__ is True
            return
        raise AssertionError("refus normalisé attendu")

    def _expect_runtime(action):
        try:
            action()
        except RuntimeError as caught:
            assert str(caught) == "unexpected"
            return
        raise AssertionError("exception inattendue non propagée")

    guard_targets = (
        (psycopg, "connect"),
        (Connection, "connect"),
        (PGWrapper, "get_new_connection"),
        (socket.socket, "connect"),
        (socket, "create_connection"),
        (subprocess, "Popen"),
        (subprocess, "run"),
        (os, "system"),
        (os, "remove"),
        (os, "rename"),
        (os, "mkdir"),
        (os, "putenv"),
        (type(os.environ), "__setitem__"),
        (builtins, "open"),
        (Path, "open"),
        (GuardedDateTime, "now"),
        (GuardedDateTime, "utcnow"),
        (time, "time"),
        (time, "monotonic"),
    )
    guards = [
        mock.Mock(side_effect=AssertionError("forbidden"))
        for _ in guard_targets
    ]

    for guard in guards:
        try:
            guard()
        except AssertionError:
            pass
        else:
            raise AssertionError("garde inactive")
        assert guard.call_count == 1
        guard.reset_mock()

    with ExitStack() as stack:
        for (target, name), mock_guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, mock_guard))

        stack.enter_context(mock.patch.object(datetime, "datetime", GuardedDateTime))
        stack.enter_context(mock.patch.object(flags, "datetime", GuardedDateTime))

        for target, name in ((Record, "save"), (Record, "delete")):
            stack.enter_context(
                mock.patch.object(
                    target,
                    name,
                    mock.Mock(side_effect=AssertionError("forbidden write")),
                )
            )

        snapshot = _snapshot()
        document = encode_feature_flag_source_snapshot(snapshot)
        get_calls = []

        def fake_get(**kwargs):
            get_calls.append(dict(kwargs))
            return _record_for(_CFG, document)

        with mock.patch.object(Record.objects, "get", side_effect=fake_get):
            result = loader.load_feature_flag_source_snapshot(_CFG)

        assert result == snapshot
        assert type(result) is sources.FeatureFlagSourceSnapshot
        assert get_calls == [{"pk": _CFG}]
        assert result.definitions[0].default_value is False
        assert result.assignments[0].value is False

        validator_calls = []
        real_validator = codec_module.validate_feature_flag_source_snapshot
        def validator_spy(value):
            validator_calls.append(value)
            return real_validator(value)
        with (
            mock.patch.object(codec_module, "validate_feature_flag_source_snapshot", side_effect=validator_spy),
            mock.patch.object(Record.objects, "get", side_effect=fake_get),
        ):
            validated_result = loader.load_feature_flag_source_snapshot(_CFG)
        assert validated_result == snapshot
        assert len(validator_calls) == 1

        whitespace_version = "  "
        whitespace_snapshot = _snapshot(version=whitespace_version)
        whitespace_document = encode_feature_flag_source_snapshot(
            whitespace_snapshot
        )
        whitespace_calls = []

        def whitespace_get(**kwargs):
            whitespace_calls.append(dict(kwargs))
            return _record_for(whitespace_version, whitespace_document)

        with mock.patch.object(Record.objects, "get", side_effect=whitespace_get):
            whitespace_result = loader.load_feature_flag_source_snapshot(
                whitespace_version
            )

        assert whitespace_result == whitespace_snapshot
        assert whitespace_calls == [{"pk": whitespace_version}]
        assert whitespace_result.configuration_version == whitespace_version

        unicode_version = "cfg-🔒-v1.2.3+opaque"
        unicode_snapshot = _snapshot(version=unicode_version)
        unicode_document = encode_feature_flag_source_snapshot(unicode_snapshot)
        unicode_calls = []

        def unicode_get(**kwargs):
            unicode_calls.append(dict(kwargs))
            return _record_for(unicode_version, unicode_document)

        with mock.patch.object(Record.objects, "get", side_effect=unicode_get):
            unicode_result = loader.load_feature_flag_source_snapshot(unicode_version)

        assert unicode_result == unicode_snapshot
        assert unicode_calls == [{"pk": unicode_version}]

        decode_calls = []

        def divergent_get(**kwargs):
            return _record_for("divergent", document)

        with (
            mock.patch.object(loader, "decode_feature_flag_source_snapshot", side_effect=_decode_spy(decode_calls)),
            mock.patch.object(Record.objects, "get", side_effect=divergent_get),
        ):
            _assert_load_error(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )
        assert decode_calls == []

        bad_type_record = _record_for(1, document)

        def bad_type_get(**kwargs):
            return bad_type_record

        decode_calls.clear()
        with (
            mock.patch.object(loader, "decode_feature_flag_source_snapshot", side_effect=_decode_spy(decode_calls)),
            mock.patch.object(Record.objects, "get", side_effect=bad_type_get),
        ):
            _assert_load_error(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )
        assert decode_calls == []

        def missing_get(**kwargs):
            raise Record.DoesNotExist()

        with mock.patch.object(Record.objects, "get", side_effect=missing_get):
            _assert_load_error(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )

        def database_error_get(**kwargs):
            raise DatabaseError("synthetic database failure")

        with mock.patch.object(Record.objects, "get", side_effect=database_error_get):
            _assert_load_error(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )

        def unexpected_get(**kwargs):
            raise RuntimeError("unexpected")

        with mock.patch.object(Record.objects, "get", side_effect=unexpected_get):
            _expect_runtime(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )

        def unexpected_decode_get(**kwargs):
            return _record_for(_CFG, document)

        with (
            mock.patch.object(loader, "decode_feature_flag_source_snapshot", side_effect=RuntimeError("unexpected")),
            mock.patch.object(Record.objects, "get", side_effect=unexpected_decode_get),
        ):
            _expect_runtime(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )

        invalid_documents = (
            _add_root_key(document, "alias"),
            _remove_root_key(document, "definitions"),
            _set_record_field(document, "assignments", "configuration_version", "other"),
            _set_record_field(document, "definitions", "value_schema", "UNKNOWN"),
            _set_record_field(document, "assignments", "flag_id", "web.unknown"),
        )

        for invalid_document in invalid_documents:
            decode_calls.clear()

            def invalid_get(invalid_document=invalid_document, **kwargs):
                return _record_for(_CFG, invalid_document)

            with (
                mock.patch.object(
                    loader,
                    "decode_feature_flag_source_snapshot",
                    side_effect=_decode_spy(decode_calls),
                ),
                mock.patch.object(Record.objects, "get", side_effect=invalid_get),
            ):
                _assert_load_error(
                    lambda: loader.load_feature_flag_source_snapshot(_CFG)
                )
            assert len(decode_calls) == 1

        wrong_document = encode_feature_flag_source_snapshot(_snapshot("other"))

        def wrong_version_get(**kwargs):
            return _record_for(_CFG, wrong_document)

        with mock.patch.object(Record.objects, "get", side_effect=wrong_version_get):
            _assert_load_error(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )

        def wrong_type_get(**kwargs):
            return _record_for(_CFG, document)

        with (
            mock.patch.object(
                loader,
                "decode_feature_flag_source_snapshot",
                side_effect=lambda _document: WrongSnapshot(
                    _CFG,
                    snapshot.definitions,
                    snapshot.assignments,
                    snapshot.cohort_rules,
                ),
            ),
            mock.patch.object(Record.objects, "get", side_effect=wrong_type_get),
        ):
            _assert_load_error(
                lambda: loader.load_feature_flag_source_snapshot(_CFG)
            )

        assert connection.connection is None
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("FEATURE_FLAG_POSTGRES_SOURCE_BEHAVIOUR_OK")
    '''
).strip()


class FeatureFlagPostgresSourceImportTests(unittest.TestCase):
    def test_public_api_and_invalid_versions_without_model_import(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", _IMPORT_CHILD, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "FEATURE_FLAG_POSTGRES_SOURCE_IMPORT_OK\n",
        )


class FeatureFlagPostgresSourceBehaviourTests(unittest.TestCase):
    def test_exact_read_contract_and_closed_refusals(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", _BEHAVIOUR_CHILD, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "FEATURE_FLAG_POSTGRES_SOURCE_BEHAVIOUR_OK\n",
        )


if __name__ == "__main__":
    unittest.main()
