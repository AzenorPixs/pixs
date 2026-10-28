"""Plan protégé C08 : recettes IO réelles, sans autorité ou PostgreSQL."""
from __future__ import annotations

import os
import tempfile
import unittest
import uuid
from dataclasses import replace
from pathlib import Path
from unittest import mock

from pixs.backend.installation.marker import MarkerConfig
from pixs.backend.installation.plan import InstallationPlan, PlanLimits, plan_sha256
from pixs.backend.installation import storage
from pixs.core.dto import BootstrapTargetSpec
from pixs.core.identity.models import IdentityType, IdentityState

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "tests" / "c08-plan-store"


def make_plan():
    identity = uuid.UUID("0194f3b2-4a1e-7f3a-8b4c-9d5e6f7a8b9c")
    spec = BootstrapTargetSpec(identity, IdentityType.HUMAN, IdentityState.ACTIVE,
                               None, None, None, None)
    return InstallationPlan("1", "plan:1", "operation:1", "installation:1", "database:1",
                            "ABSENT", "PREPARATION", "operator:1",
                            "pixs.core.identity:" + str(identity), None, spec,
                            ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"),
                            "credential-intent:1", "correlation:1", None, "idempotence:1")


class PlanStoreCases(unittest.TestCase):
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
        limits = PlanLimits(4096, 128, 6, ("1",), ("plan:1",))
        io = MarkerConfig(str(self.parent / "plan.json"), os.geteuid(), os.getegid(),
                          4096, 128, ("1",), identities)
        self.config = storage.PlanStoreConfig(io, "plan.guard", limits)
        self.plan = make_plan()

    def initialize(self):
        storage.initialize_plan_guard(self.config)

    def test_no_implicit_initialization_or_plan(self):
        with self.assertRaises(storage.PlanStoreUnknown):
            storage.read_plan(self.config)
        self.assertEqual(list(self.parent.iterdir()), [])
        self.initialize()
        with self.assertRaises(storage.PlanStoreUnknown):
            storage.read_plan(self.config)
        self.assertFalse(Path(self.config.io.path).exists())

    def test_initialize_is_idempotent_and_private(self):
        self.initialize()
        guard = self.parent / self.config.lock_basename
        inode = guard.stat().st_ino
        self.initialize()
        self.assertEqual(guard.stat().st_ino, inode)
        self.assertEqual(guard.stat().st_mode & 0o7777, 0o600)
        self.assertEqual(guard.read_bytes(), b"")

    def test_publish_read_and_idempotent_without_second_write(self):
        self.initialize()
        digest = storage.publish_plan(self.config, self.plan)
        self.assertEqual(digest, plan_sha256(self.plan, self.config.limits))
        inode = os.stat(self.config.io.path).st_ino
        self.assertEqual(storage.read_plan(self.config), self.plan)
        self.assertEqual(storage.publish_plan(self.config, self.plan), digest)
        self.assertEqual(os.stat(self.config.io.path).st_ino, inode)

    def test_conflicting_plan_is_never_overwritten(self):
        self.initialize()
        storage.publish_plan(self.config, self.plan)
        before = Path(self.config.io.path).read_bytes()
        with self.assertRaises(storage.PlanStoreConflict):
            storage.publish_plan(self.config, replace(self.plan, database_target_ref="database:2"))
        self.assertEqual(Path(self.config.io.path).read_bytes(), before)

    def test_actual_exclusion_and_shared_readers(self):
        self.initialize()
        storage.publish_plan(self.config, self.plan)
        with storage._guard(self.config, write=False):
            self.assertEqual(storage.read_plan(self.config), self.plan)
            with self.assertRaises(storage.PlanStoreBusy):
                storage.publish_plan(self.config, self.plan)
        with storage._guard(self.config, write=True):
            with self.assertRaises(storage.PlanStoreBusy):
                storage.publish_plan(self.config, self.plan)

    def test_invalid_guard_is_not_repaired(self):
        self.initialize()
        guard = self.parent / self.config.lock_basename
        os.chmod(guard, 0o640)
        with self.assertRaises(storage.PlanStoreRefused):
            self.initialize()
        self.assertEqual(guard.stat().st_mode & 0o7777, 0o640)
        os.chmod(guard, 0o600)
        guard.write_bytes(b"foreign")
        with self.assertRaises(storage.PlanStoreRefused):
            self.initialize()
        self.assertEqual(guard.read_bytes(), b"foreign")

    def test_guard_symlink_and_hardlink_refused(self):
        self.initialize()
        guard = self.parent / self.config.lock_basename
        other = self.parent / "other"
        os.link(guard, other)
        with self.assertRaises(storage.PlanStoreRefused):
            storage.read_plan(self.config)
        other.unlink()
        guard.unlink()
        other.write_bytes(b"")
        guard.symlink_to(other)
        with self.assertRaises(storage.PlanStoreRefused):
            storage.read_plan(self.config)

    def test_plan_mode_and_symlink_refused(self):
        self.initialize()
        storage.publish_plan(self.config, self.plan)
        path = Path(self.config.io.path)
        os.chmod(path, 0o640)
        with self.assertRaises(storage.PlanStoreRefused):
            storage.read_plan(self.config)
        path.unlink()
        path.symlink_to(self.parent / self.config.lock_basename)
        with self.assertRaises(storage.PlanStoreRefused):
            storage.read_plan(self.config)

    def test_invalid_configuration_cannot_alias_guard_and_plan(self):
        for change in ({"lock_basename": "plan.json"}, {"lock_basename": "../guard"},
                       {"lock_basename": ""}, {"limits": replace(self.config.limits, max_bytes=1)}):
            with self.subTest(change=list(change)):
                with self.assertRaises(storage.PlanStoreRefused):
                    replace(self.config, **change)

    def test_file_fsync_fault_has_no_success_or_repair(self):
        self.initialize()
        with mock.patch.object(storage.os, "fsync", side_effect=OSError("fault")):
            with self.assertRaises(storage.PlanStoreIssueUnknown):
                storage.publish_plan(self.config, self.plan)
        self.assertFalse(Path(self.config.io.path).exists())
        self.assertEqual([p.name for p in self.parent.iterdir()], [self.config.lock_basename])

    def test_directory_fsync_fault_requires_inspection_before_retry(self):
        self.initialize()
        fsync = os.fsync
        calls = []
        def fault(descriptor):
            calls.append(descriptor)
            if len(calls) == 2:
                raise OSError("fault")
            return fsync(descriptor)
        with mock.patch.object(storage.os, "fsync", side_effect=fault):
            with self.assertRaises(storage.PlanStoreIssueUnknown):
                storage.publish_plan(self.config, self.plan)
        self.assertEqual(storage.read_plan(self.config), self.plan)
        self.assertEqual(storage.publish_plan(self.config, self.plan),
                         plan_sha256(self.plan, self.config.limits))

    def test_replace_fault_does_not_delete_foreign_file(self):
        self.initialize()
        foreign = self.parent / "preserve"
        foreign.write_bytes(b"foreign")
        with mock.patch.object(storage.os, "replace", side_effect=OSError("fault")):
            with self.assertRaises(storage.PlanStoreIssueUnknown):
                storage.publish_plan(self.config, self.plan)
        self.assertEqual(foreign.read_bytes(), b"foreign")
        self.assertFalse(Path(self.config.io.path).exists())

    def test_parent_permissions_are_checked(self):
        self.initialize()
        os.chmod(self.parent, 0o750)
        with self.assertRaises(storage.PlanStoreRefused):
            storage.publish_plan(self.config, self.plan)


if __name__ == "__main__":
    unittest.main()
