"""Adaptateur plan→checkpoint C08 : recettes IO réelles, sans PG ni autorité."""
from __future__ import annotations

import json
import multiprocessing
import os
import tempfile
import unittest
import uuid
from dataclasses import replace
from pathlib import Path
from unittest import mock

from pixs.backend.installation import checkpoint as _ckpt
from pixs.backend.installation import storage as _store
from pixs.backend.installation.checkpoint_binding import C08CheckpointBinding
from pixs.backend.installation.marker import MarkerConfig
from pixs.backend.installation.plan import (
    InstallationPlan, PlanLimits, bind_confirmation, canonical_plan_bytes, plan_sha256)
from pixs.core.dto import BootstrapTargetSpec
from pixs.core.identity.models import IdentityType, IdentityState

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "tests" / "c08-checkpoint-binding"


def make_plan(operation="operation:1", installation="installation:1"):
    identity = uuid.UUID("0194f3b2-4a1e-7f3a-8b4c-9d5e6f7a8b9c")
    spec = BootstrapTargetSpec(identity, IdentityType.HUMAN, IdentityState.ACTIVE,
                               None, None, None, None)
    return InstallationPlan("1", "plan:1", operation, installation, "database:1",
                            "ABSENT", "PREPARATION", "operator:1",
                            "pixs.core.identity:" + str(identity), None, spec,
                            ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"),
                            "credential-intent:1", "correlation:1", None, "idempotence:1")


def _child_publish(plan_store, plan, queue):
    try:
        _store.publish_plan(plan_store, plan)
        queue.put("ok")
    except _store.PlanStoreBusy:
        queue.put("busy")
    except _store.PlanStoreConflict:
        queue.put("conflict")


class BindingCases(unittest.TestCase):
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
        plan_io = MarkerConfig(str(self.parent / "plan.json"), os.geteuid(),
                               os.getegid(), 4096, 128, ("1",), identities)
        ckpt_io = MarkerConfig(str(self.parent / "checkpoint.json"), os.geteuid(),
                               os.getegid(), 4096, 128, ("1",), identities)
        plan_limits = PlanLimits(4096, 128, 6, ("1",), ("plan:1",))
        ckpt_limits = _ckpt.CheckpointLimits(4096, 128, 4, ("1",),
                                             ("PLAN_RECORDED", "PROOF_LINK_OBSERVED",
                                              "INSPECTION_OBSERVED", "RECOVERY_NOTE_RECORDED"))
        self.plan_store = _store.PlanStoreConfig(plan_io, "plan.guard", plan_limits)
        self.ckpt = _ckpt.CheckpointConfig(ckpt_io, "checkpoint.guard", ckpt_limits)
        _store.initialize_plan_guard(self.plan_store)
        self.plan = make_plan()
        _store.publish_plan(self.plan_store, self.plan)
        self.binding = C08CheckpointBinding(plan_store=self.plan_store,
                                            checkpoint=self.ckpt, format_version="1")

    def test_same_files_or_guards_refused(self):
        with self.assertRaises(_ckpt.CheckpointRefused):
            C08CheckpointBinding(plan_store=self.plan_store,
                                 checkpoint=replace(self.ckpt, io=self.plan_store.io),
                                 format_version="1")
        with self.assertRaises(_ckpt.CheckpointRefused):
            C08CheckpointBinding(plan_store=self.plan_store,
                                 checkpoint=replace(self.ckpt, lock_basename="plan.guard"),
                                 format_version="1")

    def test_initialize_only_checkpoint_guard(self):
        self.binding.initialize_checkpoint_guard()
        self.assertTrue((self.parent / "checkpoint.guard").exists())
        self.assertFalse((self.parent / "checkpoint.json").exists())

    def test_record_derives_identities_and_digest(self):
        self.binding.initialize_checkpoint_guard()
        link = bind_confirmation(self.plan, "confirmation:1", self.plan_store.limits)
        stored = self.binding.record(revision=1, phase="PLAN_RECORDED",
                                     confirmations=(link,))
        self.assertEqual(self.binding.read_bound(), stored)
        self.assertEqual(stored.plan_sha256, plan_sha256(self.plan, self.plan_store.limits))
        self.assertEqual(stored.confirmation_refs, ("confirmation:1",))

    def test_confirmation_other_plan_refused(self):
        self.binding.initialize_checkpoint_guard()
        other = make_plan(operation="operation:2")
        link = bind_confirmation(other, "confirmation:2", self.plan_store.limits)
        with self.assertRaises(_ckpt.CheckpointRefused):
            self.binding.record(revision=1, phase="PLAN_RECORDED", confirmations=(link,))

    def test_checkpoint_other_plan_is_not_absent(self):
        self.binding.initialize_checkpoint_guard()
        link = bind_confirmation(self.plan, "confirmation:1", self.plan_store.limits)
        self.binding.record(revision=1, phase="PLAN_RECORDED", confirmations=(link,))
        path = Path(self.ckpt.io.path)
        document = json.loads(path.read_bytes())
        document["plan_sha256"] = "ff" * 32
        path.write_text(json.dumps(document, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        with self.assertRaises(_ckpt.CheckpointConflict):
            self.binding.read_bound()

    def test_ex_plan_lock_blocks_binding(self):
        self.binding.initialize_checkpoint_guard()
        with _store._guard(self.plan_store, write=True):
            with self.assertRaises(_ckpt.CheckpointBusy):
                self.binding.read_bound()

    def test_sh_held_during_checkpoint_publication_blocks_plan_writer(self):
        self.binding.initialize_checkpoint_guard()
        ctx = multiprocessing.get_context("spawn")
        queue = ctx.Queue()
        child = ctx.Process(
            target=_child_publish,
            args=(self.plan_store, make_plan(operation="operation:2"), queue))
        real_publish = _ckpt._io._publish
        observed = []
        def during_publication(*args, **kwargs):
            child.start()
            child.join(5)
            self.assertFalse(child.is_alive(), "CHILD_TIMEOUT")
            self.assertEqual(child.exitcode, 0)
            observed.append(queue.get(timeout=2))
            self.assertEqual(observed, ["busy"])
            return real_publish(*args, **kwargs)
        try:
            with mock.patch.object(_ckpt._io, "_publish", side_effect=during_publication):
                self.binding.record(revision=1, phase="PLAN_RECORDED", confirmations=())
            self.assertEqual(observed, ["busy"])
        finally:
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

    def test_plan_modified_during_real_io_keeps_issue_unknown(self):
        self.binding.initialize_checkpoint_guard()
        link = bind_confirmation(self.plan, "confirmation:1", self.plan_store.limits)
        real_publish = _ckpt._io._publish
        def changed_plan(*args, **kwargs):
            real_publish(*args, **kwargs)
            changed = make_plan(operation="operation:9")
            Path(self.plan_store.io.path).write_bytes(
                canonical_plan_bytes(changed, self.plan_store.limits))
        with mock.patch.object(_ckpt._io, "_publish", side_effect=changed_plan):
            with self.assertRaises(_ckpt.CheckpointIssueUnknown):
                self.binding.record(revision=1, phase="PLAN_RECORDED",
                                    confirmations=(link,))
        self.assertTrue(Path(self.ckpt.io.path).exists())

    def test_missing_plan_prevents_checkpoint_guard_initialization(self):
        Path(self.plan_store.io.path).unlink()
        with self.assertRaises(_ckpt.CheckpointRefused) as refused:
            self.binding.initialize_checkpoint_guard()
        self.assertNotIsInstance(refused.exception, _ckpt.CheckpointUnknown)
        self.assertFalse((self.parent / "checkpoint.guard").exists())

    def test_invalid_plan_is_not_missing_checkpoint(self):
        self.binding.initialize_checkpoint_guard()
        Path(self.plan_store.io.path).write_bytes(b"not-json")
        with self.assertRaises(_ckpt.CheckpointRefused) as refused:
            self.binding.read_bound()
        self.assertNotIsInstance(refused.exception, _ckpt.CheckpointUnknown)

    def test_io_fault_only_no_authority_mock(self):
        self.binding.initialize_checkpoint_guard()
        link = bind_confirmation(self.plan, "confirmation:1", self.plan_store.limits)
        with mock.patch.object(_ckpt.os, "fsync", side_effect=OSError("fault")):
            with self.assertRaises(_ckpt.CheckpointIssueUnknown):
                self.binding.record(revision=1, phase="PLAN_RECORDED",
                                    confirmations=(link,))


if __name__ == "__main__":
    unittest.main()
