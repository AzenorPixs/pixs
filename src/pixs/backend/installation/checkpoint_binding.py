"""Adaptateur privé plan→checkpoint C08, sans autorité ni sélection de mode.

Rattache le checkpoint réellement au plan privé courant. Ne prouve ni commit,
ni autorisation, ni disponibilité. Digest et champs restent une liaison
structurelle rapprochée du plan immuable courant.
"""
from __future__ import annotations

import os

from pixs.backend.installation import checkpoint as _ckpt
from pixs.backend.installation import storage as _store
from pixs.backend.installation.plan import (
    PlanInvalid, PlanConfirmationLink, check_confirmation_link, plan_sha256)
from pixs.backend.installation.marker import MarkerInvalid

__all__ = ["C08CheckpointBinding"]


class C08CheckpointBinding:
    def __init__(self, *, plan_store: _store.PlanStoreConfig,
                 checkpoint: _ckpt.CheckpointConfig,
                 format_version: str) -> None:
        if (type(plan_store) is not _store.PlanStoreConfig
                or type(checkpoint) is not _ckpt.CheckpointConfig
                or type(format_version) is not str):
            raise _ckpt.CheckpointRefused()
        try:
            _store._config(plan_store)
            _ckpt._config(checkpoint)
        except (PlanInvalid, MarkerInvalid):
            raise _ckpt.CheckpointRefused() from None
        if format_version not in checkpoint.limits.allowed_format_versions:
            raise _ckpt.CheckpointRefused()
        plan_file = plan_store.io.path
        ckpt_file = checkpoint.io.path
        plan_dir = os.path.dirname(plan_file)
        ckpt_dir = os.path.dirname(ckpt_file)
        plan_guard = (plan_dir + "/" + plan_store.lock_basename
                      if plan_dir else plan_store.lock_basename)
        ckpt_guard = (ckpt_dir + "/" + checkpoint.lock_basename
                      if ckpt_dir else checkpoint.lock_basename)
        files = {plan_file, ckpt_file, plan_guard, ckpt_guard}
        if len(files) != 4:
            raise _ckpt.CheckpointRefused()
        try:
            plan = _store.read_plan(plan_store)
        except _store.PlanStoreBusy:
            raise _ckpt.CheckpointBusy() from None
        except _store.PlanStoreUnknown:
            raise _ckpt.CheckpointIssueUnknown() from None
        except (PlanInvalid, MarkerInvalid):
            raise _ckpt.CheckpointIssueUnknown() from None
        digest = plan_sha256(plan, plan_store.limits)
        self._plan_store = plan_store
        self._checkpoint = checkpoint
        self._format_version = format_version
        self._plan_digest = digest

    def initialize_checkpoint_guard(self) -> None:
        try:
            with _store._guard(self._plan_store, write=False):
                plan = self._checked_plan()
                _ckpt.initialize_checkpoint_guard(self._checkpoint)
                if self._checked_plan() != plan:
                    raise _ckpt.CheckpointIssueUnknown()
        except _ckpt.CheckpointRefused:
            raise
        except _store.PlanStoreBusy:
            raise _ckpt.CheckpointBusy() from None
        except (PlanInvalid, MarkerInvalid, OSError):
            raise _ckpt.CheckpointIssueUnknown() from None

    def _checked_plan(self):
        try:
            plan = _store.read_plan(self._plan_store)
        except _store.PlanStoreBusy:
            raise _ckpt.CheckpointBusy() from None
        except _store.PlanStoreUnknown:
            raise _ckpt.CheckpointIssueUnknown() from None
        except (PlanInvalid, MarkerInvalid):
            raise _ckpt.CheckpointIssueUnknown() from None
        if plan_sha256(plan, self._plan_store.limits) != self._plan_digest:
            raise _ckpt.CheckpointIssueUnknown()
        return plan

    def _check_bound(self, plan, content: _ckpt.InstallationCheckpointContent) -> None:
        if (content.format_version != self._format_version
                or content.installation_ref != plan.installation_ref
                or content.database_target_ref != plan.database_target_ref
                or content.operation_id != plan.operation_id
                or content.plan_version != plan.plan_version
                or content.plan_sha256 != self._plan_digest
                or content.correlation_id != plan.correlation_id
                or content.causation_id != plan.causation_id
                or content.idempotency_key != plan.idempotency_key):
            raise _ckpt.CheckpointConflict()
        if (type(content.phase) is not str
                or content.phase in ("NORMAL", "INSTALLER")
                or content.phase not in self._checkpoint.limits.allowed_phases):
            raise _ckpt.CheckpointRefused()

    def read_bound(self) -> _ckpt.InstallationCheckpointContent:
        try:
            with _store._guard(self._plan_store, write=False):
                plan = self._checked_plan()
                try:
                    content = _ckpt.read_checkpoint(self._checkpoint)
                except _ckpt.CheckpointUnknown:
                    raise
                except _ckpt.CheckpointBusy:
                    raise
                except _ckpt.CheckpointRefused:
                    raise
                self._check_bound(plan, content)
                after = self._checked_plan()
                if after != plan:
                    raise _ckpt.CheckpointIssueUnknown()
                return content
        except (_ckpt.CheckpointBusy, _ckpt.CheckpointUnknown,
                _ckpt.CheckpointConflict, _ckpt.CheckpointIssueUnknown,
                _ckpt.CheckpointRefused):
            raise
        except _store.PlanStoreBusy:
            raise _ckpt.CheckpointBusy() from None
        except (PlanInvalid, MarkerInvalid, OSError):
            raise _ckpt.CheckpointIssueUnknown() from None

    def record(self, *, revision: int, phase: str,
               confirmations: tuple[PlanConfirmationLink, ...]
               ) -> _ckpt.InstallationCheckpointContent:
        if type(revision) is not int or revision < 1:
            raise _ckpt.CheckpointRefused()
        if type(phase) is not str or phase in ("NORMAL", "INSTALLER"):
            raise _ckpt.CheckpointRefused()
        if (type(confirmations) is not tuple
                or len(confirmations) > self._checkpoint.limits.max_confirmations):
            raise _ckpt.CheckpointRefused()
        try:
            with _store._guard(self._plan_store, write=False):
                plan = self._checked_plan()
                refs: list[str] = []
                for link in confirmations:
                    if type(link) is not PlanConfirmationLink:
                        raise _ckpt.CheckpointRefused()
                    try:
                        check_confirmation_link(plan, link, self._plan_store.limits)
                    except PlanInvalid:
                        raise _ckpt.CheckpointRefused() from None
                    refs.append(link.confirmation_ref)
                content = _ckpt.InstallationCheckpointContent(
                    self._format_version, plan.installation_ref,
                    plan.database_target_ref, plan.operation_id,
                    plan.plan_version, self._plan_digest,
                    plan.correlation_id, plan.causation_id,
                    plan.idempotency_key, revision, phase, tuple(refs))
                try:
                    stored = _ckpt.publish_checkpoint(self._checkpoint, content)
                except (_ckpt.CheckpointBusy, _ckpt.CheckpointUnknown,
                        _ckpt.CheckpointConflict, _ckpt.CheckpointIssueUnknown,
                        _ckpt.CheckpointRefused):
                    raise
                after = self._checked_plan()
                if after != plan:
                    raise _ckpt.CheckpointIssueUnknown()
                self._check_bound(plan, stored)
                return stored
        except (_ckpt.CheckpointBusy, _ckpt.CheckpointUnknown,
                _ckpt.CheckpointConflict, _ckpt.CheckpointIssueUnknown,
                _ckpt.CheckpointRefused):
            raise
        except _store.PlanStoreBusy:
            raise _ckpt.CheckpointBusy() from None
        except (PlanInvalid, MarkerInvalid, OSError):
            raise _ckpt.CheckpointIssueUnknown() from None
