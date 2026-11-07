"""Recettes IO réelles C08 ; doubles de résultat limités au contrat du fichier.

Ces recettes ne qualifient pas un commit PostgreSQL ni l'acte Core/Auth.
"""
from __future__ import annotations

import dataclasses
import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

from pixs.backend.installation import marker

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "tests" / "c08-marker"


class Source:
    def __init__(self, result):
        self.result = result
        self.entered = self.released = False

    @contextmanager
    def guard_confirmed(self, *, installation_ref):
        if self.result is None:
            raise marker.MarkerResultUnavailable()
        self.entered = True
        try:
            yield self.result
        finally:
            self.released = True


class MarkerCases(unittest.TestCase):
    def setUp(self):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=OUTPUT, prefix="case-")
        self.addCleanup(temporary.cleanup)
        self.parent = Path(temporary.name)
        # Groupe de la fixture privée uniquement, sans privilège ni chown hôte.
        os.chown(self.parent, -1, os.getegid())
        os.chmod(self.parent, 0o700)
        identities = tuple(dict.fromkeys(
            (p.stat().st_uid, p.stat().st_gid)
            for p in [*reversed(self.parent.parents), self.parent]))
        self.config = marker.MarkerConfig(
            path=str(self.parent / "installation.marker"), owner_uid=os.geteuid(),
            owner_gid=os.getegid(), max_bytes=4096, max_ref_len=128,
            allowed_format_versions=("1",), parent_identities=identities)
        self.result = marker.InstallationMarkerContent("1", "installation:a", "result:a", 1)

    def publish(self, result=None):
        return marker.publish_installation_marker(
            config=self.config, installation_ref="installation:a",
            source=Source(self.result if result is None else result))

    def raw(self, value):
        Path(self.config.path).write_bytes(value)
        os.chmod(self.config.path, 0o600)

    def test_publish_read_idempotent(self):
        self.assertEqual(self.publish(), self.result)
        inode = os.stat(self.config.path).st_ino
        self.assertEqual(self.publish(), self.result)
        self.assertEqual(os.stat(self.config.path).st_ino, inode)
        self.assertEqual(marker.read_installation_marker(self.config), self.result)

    def test_missing_is_unknown_without_installer_selection(self):
        with self.assertRaises(marker.MarkerUnknown):
            marker.read_installation_marker(self.config)

    def test_missing_source_and_unconfirmed_result(self):
        for source in (None, Source(None), Source(False)):
            with self.subTest(source=type(source).__name__):
                with self.assertRaises(marker.MarkerInvalid):
                    marker.publish_installation_marker(
                        config=self.config, installation_ref="installation:a", source=source)
        self.assertFalse(Path(self.config.path).exists())

    def test_divergent_source_installation(self):
        with self.assertRaises(marker.MarkerDivergent):
            self.publish(dataclasses.replace(self.result, installation_ref="installation:b"))

    def test_divergent_existing_result_is_preserved(self):
        self.publish()
        before = Path(self.config.path).read_bytes()
        with self.assertRaises(marker.MarkerDivergent):
            self.publish(dataclasses.replace(self.result, result_ref="result:b"))
        self.assertEqual(Path(self.config.path).read_bytes(), before)

    def test_private_file_mode_and_owner(self):
        self.publish()
        st = os.stat(self.config.path)
        self.assertEqual(st.st_mode & 0o7777, 0o600)
        self.assertEqual((st.st_uid, st.st_gid), (self.config.owner_uid, self.config.owner_gid))
        os.chmod(self.config.path, 0o640)
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(self.config)

    def test_wrong_owner_and_group(self):
        self.publish()
        for name in ("owner_uid", "owner_gid"):
            config = dataclasses.replace(self.config, **{name: getattr(self.config, name) + 1})
            with self.subTest(name=name):
                with self.assertRaises(marker.MarkerInvalid):
                    marker.read_installation_marker(config)

    def test_hardlink_refused(self):
        self.publish()
        os.link(self.config.path, self.parent / "other")
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(self.config)

    def test_symlink_refused(self):
        target = self.parent / "target"
        target.write_bytes(b"data")
        Path(self.config.path).symlink_to(target)
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(self.config)
        self.assertEqual(target.read_bytes(), b"data")

    def test_directory_and_fifo_refused_without_blocking(self):
        Path(self.config.path).mkdir(mode=0o700)
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(self.config)
        Path(self.config.path).rmdir()
        os.mkfifo(self.config.path, 0o600)
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(self.config)

    def test_parent_permissions_and_identity(self):
        os.chmod(self.parent, 0o750)
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(self.config)
        os.chmod(self.parent, 0o700)
        config = dataclasses.replace(self.config, parent_identities=((999999, 999999),))
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(config)

    def test_parent_symlink_refused(self):
        alias = self.parent / "alias"
        alias.symlink_to(self.parent, target_is_directory=True)
        config = dataclasses.replace(self.config, path=str(alias / "installation.marker"))
        with self.assertRaises(marker.MarkerInvalid):
            marker.read_installation_marker(config)

    def test_config_has_no_coercion_or_path_traversal(self):
        changes = [{"owner_uid": True}, {"owner_gid": False}, {"max_bytes": True},
                   {"max_bytes": 0}, {"max_ref_len": 0}, {"allowed_format_versions": ()},
                   {"allowed_format_versions": ("1", "1")}, {"parent_identities": ()},
                   {"path": "relative"}, {"path": str(self.parent / ".." / "marker")}]
        for change in changes:
            with self.subTest(change=change):
                with self.assertRaises(marker.MarkerInvalid):
                    dataclasses.replace(self.config, **change)

    def test_closed_schema_and_strict_json(self):
        document = dataclasses.asdict(self.result)
        candidates = [b"", b"[]", b"null", b"\xff", b"{",
                      b'{"format_version":"1","format_version":"1"}',
                      json.dumps({**document, "extra": "ref"}).encode(),
                      json.dumps({**document, "result_version": True}).encode(),
                      json.dumps({**document, "result_version": 1.0}).encode(),
                      json.dumps({**document, "result_version": 0}).encode(),
                      json.dumps({**document, "result_version": float("nan")}).encode(),
                      json.dumps({**document, "format_version": "unknown"}).encode(),
                      json.dumps({**document, "result_ref": ""}).encode(),
                      b"x" * (self.config.max_bytes + 1)]
        for raw in candidates:
            with self.subTest(size=len(raw)):
                self.raw(raw)
                with self.assertRaises(marker.MarkerInvalid):
                    marker.read_installation_marker(self.config)

    def test_reference_bounds_and_result_types(self):
        for result in (False, dataclasses.replace(self.result, result_version=True),
                       dataclasses.replace(self.result, result_ref="x" * 129)):
            with self.subTest(result_type=type(result).__name__):
                with self.assertRaises(marker.MarkerInvalid):
                    self.publish(result)

    def test_guard_retained_until_all_fsyncs(self):
        source = Source(self.result)
        fsync = os.fsync
        observed = []
        def inspect(descriptor):
            self.assertTrue(source.entered)
            self.assertFalse(source.released)
            observed.append(descriptor)
            return fsync(descriptor)
        with mock.patch.object(marker.os, "fsync", side_effect=inspect):
            marker.publish_installation_marker(
                config=self.config, installation_ref="installation:a", source=source)
        self.assertTrue(source.released)
        self.assertGreaterEqual(len(observed), 4)

    def test_file_fsync_failure_leaves_no_published_file(self):
        with mock.patch.object(marker.os, "fsync", side_effect=OSError("fault")):
            with self.assertRaises(marker.MarkerIssueUnknown):
                self.publish()
        self.assertFalse(Path(self.config.path).exists())
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_replace_failure_removes_only_own_temporary(self):
        foreign = self.parent / ".foreign"
        foreign.write_bytes(b"preserve")
        with mock.patch.object(marker.os, "replace", side_effect=OSError("fault")):
            with self.assertRaises(marker.MarkerIssueUnknown):
                self.publish()
        self.assertEqual(list(self.parent.iterdir()), [foreign])
        self.assertEqual(foreign.read_bytes(), b"preserve")

    def test_directory_fsync_failure_requires_inspection_then_retry(self):
        fsync = os.fsync
        calls = []
        def fault(descriptor):
            calls.append(descriptor)
            if len(calls) == 2:
                raise OSError("fault")
            return fsync(descriptor)
        with mock.patch.object(marker.os, "fsync", side_effect=fault):
            with self.assertRaises(marker.MarkerIssueUnknown):
                self.publish()
        self.assertTrue(Path(self.config.path).exists())
        self.assertEqual(self.publish(), self.result)

    def test_errors_do_not_include_file_content(self):
        self.raw(b"private-value-invalid")
        with self.assertRaises(marker.MarkerInvalid) as raised:
            marker.read_installation_marker(self.config)
        self.assertNotIn("private-value-invalid", str(raised.exception))
        self.assertNotIn(self.config.path, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
