"""Checkpoint durable C08 : recettes IO réelles, sans autorité ni PostgreSQL."""
from __future__ import annotations

import json
import multiprocessing
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from pixs.backend.installation.checkpoint import (
    CheckpointConfig, CheckpointLimits, InstallationCheckpointContent,
    CheckpointBusy, CheckpointConflict, CheckpointIssueUnknown,
    CheckpointRefused, CheckpointUnknown, initialize_checkpoint_guard,
    publish_checkpoint, read_checkpoint)
from pixs.backend.installation.marker import MarkerConfig

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "tests" / "c08-checkpoint"


def make_content(revision=1, phase="PLAN_RECORDED"):
    return InstallationCheckpointContent(
        "1", "installation:1", "database:1", "operation:1", "plan:1",
        "00" * 32, "correlation:1", None, "idempotence:1",
        revision, phase, ("confirmation:1",))


def _attempt(config, content, start, queue):
    if not start.wait(5):
        queue.put("start-timeout")
        return
    try:
        publish_checkpoint(config, content)
        queue.put("ok")
    except CheckpointBusy:
        queue.put("busy")
    except CheckpointConflict:
        queue.put("conflict")


class CheckpointCases(unittest.TestCase):
    def setUp(self):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=OUTPUT, prefix="case-")
        self.addCleanup(temporary.cleanup)
        self.parent = Path(temporary.name)
        os.chown(self.parent, -1, os.getegid())
        os.chmod(self.parent, 0o700)
        identities = tuple(dict.fromkeys(
            (p.stat().st_uid, p.stat().st_gid)
            for p in [*reversed(self.parent.parents), self.parent]))
        io = MarkerConfig(str(self.parent / "checkpoint.json"), os.geteuid(),
                          os.getegid(), 4096, 128, ("1",), identities)
        limits = CheckpointLimits(4096, 128, 4, ("1",),
                                  ("PLAN_RECORDED", "PROOF_LINK_OBSERVED",
                                   "INSPECTION_OBSERVED", "RECOVERY_NOTE_RECORDED"))
        self.config = CheckpointConfig(io, "checkpoint.guard", limits)

    def initialize(self):
        initialize_checkpoint_guard(self.config)

    def test_no_guard_means_unknown_without_creation(self):
        with self.assertRaises(CheckpointUnknown):
            read_checkpoint(self.config)
        with self.assertRaises(CheckpointUnknown):
            publish_checkpoint(self.config, make_content())
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_publish_read_idempotent_inode_stable(self):
        self.initialize()
        first = publish_checkpoint(self.config, make_content())
        inode = os.stat(self.config.io.path).st_ino
        self.assertEqual(read_checkpoint(self.config), first)
        self.assertEqual(publish_checkpoint(self.config, make_content()), first)
        self.assertEqual(os.stat(self.config.io.path).st_ino, inode)

    def test_revision_progression_stale_and_jump_refused(self):
        self.initialize()
        first = publish_checkpoint(self.config, make_content())
        self.assertEqual(read_checkpoint(self.config), first)
        with self.assertRaises(CheckpointConflict):
            publish_checkpoint(self.config, replace(make_content(), correlation_id="correlation:2"))
        with self.assertRaises(CheckpointConflict):
            publish_checkpoint(self.config, replace(make_content(), revision=3))
        second = publish_checkpoint(self.config, replace(make_content(), revision=2))
        self.assertEqual(second.revision, 2)
        inode = os.stat(self.config.io.path).st_ino
        self.assertEqual(publish_checkpoint(self.config, replace(make_content(), revision=2)), second)
        self.assertEqual(os.stat(self.config.io.path).st_ino, inode)
        with self.assertRaises(CheckpointConflict):
            publish_checkpoint(self.config, make_content())

    def test_identity_conflicts_each_field(self):
        self.initialize()
        publish_checkpoint(self.config, make_content())
        cases = ({"installation_ref": "installation:2"},
                 {"database_target_ref": "database:2"}, {"operation_id": "operation:2"},
                 {"plan_version": "plan:2"}, {"plan_sha256": "ff" * 32},
                 {"correlation_id": "correlation:2"}, {"causation_id": "causation:2"},
                 {"idempotency_key": "idempotence:2"})
        for change in cases:
            with self.subTest(change=list(change)):
                with self.assertRaises(CheckpointConflict):
                    publish_checkpoint(self.config, replace(make_content(), revision=2, **change))

    def test_guard_symlink_and_hardlink_refused(self):
        self.initialize()
        guard = self.parent / self.config.lock_basename
        other = self.parent / "other"
        os.link(guard, other)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        other.unlink()
        guard.unlink()
        other.write_bytes(b"")
        guard.symlink_to(other)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)

    def test_checkpoint_symlink_and_hardlink_refused(self):
        self.initialize()
        publish_checkpoint(self.config, make_content())
        path = Path(self.config.io.path)
        other = self.parent / "foreign-target"
        other.write_bytes(b"foreign")
        os.link(path, self.parent / "hard")
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        (self.parent / "hard").unlink()
        raw = path.read_bytes()
        path.unlink()
        path.symlink_to(other)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        path.unlink()
        path.write_bytes(raw)

    def test_modes_owner_parent_refused(self):
        self.initialize()
        publish_checkpoint(self.config, make_content())
        path = Path(self.config.io.path)
        os.chmod(path, 0o640)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        os.chmod(path, 0o600)
        bad = replace(self.config.io, owner_uid=self.config.io.owner_uid + 1,
                      owner_gid=self.config.io.owner_gid)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(replace(self.config, io=bad))
        os.chmod(self.parent, 0o750)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        os.chmod(self.parent, 0o700)

    def test_json_duplicates_nan_unknown_digest_bool_nested_refused(self):
        self.initialize()
        from pixs.backend.installation import checkpoint as module
        base = {"format_version": "1", "installation_ref": "installation:1",
                "database_target_ref": "database:1", "operation_id": "operation:1",
                "plan_version": "plan:1", "plan_sha256": "00" * 32,
                "correlation_id": "correlation:1", "causation_id": None,
                "idempotency_key": "idempotence:1", "revision": 1,
                "phase": "PLAN_RECORDED", "confirmation_refs": ["confirmation:1"]}
        duplicated = b'{"revision": 1, "revision": 2}'
        nan = json.dumps({**base, "revision": float("nan")}).encode()
        unknown = json.dumps({**base, "extra": "x"}).encode()
        bad_digest = json.dumps({**base, "plan_sha256": "zz"}).encode()
        boolean = json.dumps({**base, "revision": True}).encode()
        nested = json.dumps({**base, "confirmation_refs": [["nested"]]}).encode()
        for raw in (duplicated, nan, unknown, bad_digest, boolean, nested):
            with self.subTest(raw=raw[:24]):
                with self.assertRaises(CheckpointRefused):
                    module._decode(raw, self.config)

    def test_real_two_process_cas_same_revision(self):
        self.initialize()
        publish_checkpoint(self.config, make_content())
        first = replace(make_content(), revision=2)
        second = replace(make_content(), revision=2, phase="PROOF_LINK_OBSERVED")
        ctx = multiprocessing.get_context("spawn")
        queue, start = ctx.Queue(), ctx.Event()
        children = [
            ctx.Process(target=_attempt, args=(self.config, value, start, queue))
            for value in (first, second)]
        try:
            for child in children:
                child.start()
            start.set()
            for child in children:
                child.join(5)
                self.assertFalse(child.is_alive(), "CHILD_TIMEOUT")
                self.assertEqual(child.exitcode, 0)
            results = [queue.get(timeout=2), queue.get(timeout=2)]
            self.assertEqual(results.count("ok"), 1)
            self.assertTrue(any(value in ("busy", "conflict") for value in results))
            self.assertIn(read_checkpoint(self.config), (first, second))
        finally:
            for child in children:
                if child.pid is not None:
                    if child.is_alive():
                        child.terminate()
                        child.join(2)
                    if child.is_alive():
                        child.kill()
                        child.join(2)
                    if not child.is_alive():
                        child.close()
            queue.close()
            queue.join_thread()

    def test_file_fsync_fault_before_rename_has_no_success(self):
        self.initialize()
        with mock.patch("pixs.backend.installation.checkpoint.os.fsync",
                        side_effect=OSError("fault")):
            with self.assertRaises(CheckpointIssueUnknown):
                publish_checkpoint(self.config, make_content())
        self.assertFalse(Path(self.config.io.path).exists())

    def test_directory_fsync_fault_after_rename_requires_inspection(self):
        self.initialize()
        real = os.fsync
        calls = []
        def fault(descriptor):
            calls.append(descriptor)
            if len(calls) == 2:
                raise OSError("fault")
            return real(descriptor)
        with mock.patch("pixs.backend.installation.checkpoint.os.fsync", side_effect=fault):
            with self.assertRaises(CheckpointIssueUnknown):
                publish_checkpoint(self.config, make_content())
        self.assertEqual(read_checkpoint(self.config), make_content())
        self.assertEqual(publish_checkpoint(self.config, make_content()), make_content())

    def test_replace_fault_does_not_delete_foreign_file(self):
        self.initialize()
        foreign = self.parent / "preserve"
        foreign.write_bytes(b"foreign")
        with mock.patch("pixs.backend.installation.checkpoint.os.replace",
                        side_effect=OSError("fault")):
            with self.assertRaises(CheckpointIssueUnknown):
                publish_checkpoint(self.config, make_content())
        self.assertEqual(foreign.read_bytes(), b"foreign")
        self.assertFalse(Path(self.config.io.path).exists())

    def test_format_version_is_immutable_even_when_both_are_admitted(self):
        self.initialize()
        publish_checkpoint(self.config, make_content())
        config = replace(
            self.config,
            io=replace(self.config.io, allowed_format_versions=("1", "9")),
            limits=replace(self.config.limits, allowed_format_versions=("1", "9")))
        with self.assertRaises(CheckpointConflict):
            publish_checkpoint(config, replace(make_content(), revision=2, format_version="9"))

    def test_phase_is_strict_and_cannot_declare_an_execution_mode(self):
        for phase in ("NORMAL", "INSTALLER", True, ["PLAN_RECORDED"]):
            with self.subTest(phase=repr(phase)):
                with self.assertRaises(CheckpointRefused):
                    replace(self.config.limits, allowed_phases=(phase,))
        self.initialize()
        with self.assertRaises(CheckpointRefused):
            publish_checkpoint(self.config, replace(make_content(), phase=True))

    def test_missing_payload_after_guard_initialization_is_not_created(self):
        self.initialize()
        with self.assertRaises(CheckpointUnknown):
            read_checkpoint(self.config)
        self.assertEqual([p.name for p in self.parent.iterdir()], [self.config.lock_basename])

    def test_guard_mode_and_content_are_not_repaired(self):
        self.initialize()
        guard = self.parent / self.config.lock_basename
        os.chmod(guard, 0o640)
        with self.assertRaises(CheckpointRefused):
            initialize_checkpoint_guard(self.config)
        self.assertEqual(guard.stat().st_mode & 0o7777, 0o640)
        os.chmod(guard, 0o600)
        guard.write_bytes(b"foreign")
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        self.assertEqual(guard.read_bytes(), b"foreign")

    def test_disappearing_or_replaced_guard_after_observation_is_unknown(self):
        from pixs.backend.installation import checkpoint as module
        self.initialize()
        guard = self.parent / self.config.lock_basename
        with self.assertRaises(CheckpointIssueUnknown):
            with module._guard(self.config, write=True):
                guard.unlink()
        self.initialize()
        with self.assertRaises(CheckpointIssueUnknown):
            with module._guard(self.config, write=False):
                guard.unlink()
                descriptor = os.open(guard, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.close(descriptor)

    def test_file_disappearance_after_open_is_unknown(self):
        from pixs.backend.installation import checkpoint as module
        self.initialize()
        publish_checkpoint(self.config, make_content())
        path = Path(self.config.io.path)
        real_stat = os.stat
        def disappearing(name, *args, **kwargs):
            if name == path.name:
                path.unlink()
            return real_stat(name, *args, **kwargs)
        with mock.patch.object(module.os, "stat", side_effect=disappearing):
            with self.assertRaises(CheckpointIssueUnknown):
                read_checkpoint(self.config)

    def test_payload_type_size_and_malformed_file_are_refused(self):
        self.initialize()
        path = Path(self.config.io.path)
        os.mkfifo(path, 0o600)
        with self.assertRaises(CheckpointRefused):
            read_checkpoint(self.config)
        path.unlink()
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
        for raw in (b"x" * (self.config.io.max_bytes + 1), b"\xff", b"not-json"):
            path.write_bytes(raw)
            with self.assertRaises(CheckpointRefused):
                read_checkpoint(self.config)


if __name__ == "__main__":
    unittest.main()
