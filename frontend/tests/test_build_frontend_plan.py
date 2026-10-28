"""Tests plan C11 : vrai Kernel/FS/CLI, sans scan global ni preuve fabriquee."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

from build_frontend_composition import BuildError, BuildLimits
from build_frontend_plan import PlanEnvelope, PlanError, plan_from_capture, prepare_frontend_plan
from build_frontend_selection import SelectionError, SelectionLimits
from test_build_selection import ENTRY, JS, limits as sel_limits_base, manifest as sel_manifest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "frontend" / "scripts"
SRC = ROOT / "src"
PLAN = SCRIPTS / "build_frontend_plan.py"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def att(owner: str, ver: str = "1.0.0", verdict: str = "PASS", scope: str = "COMPONENT",
        target: str | None = None, tver: str | None = None, idx: int = 0) -> dict:
    tid = target if target is not None else owner
    tv = tver if tver is not None else ver
    return {"component_id": owner, "component_version": ver, "scope": scope,
            "target_id": tid, "target_version": tv, "suite_id": f"fx.{idx}",
            "suite_version": "1.0.0", "verdict": verdict, "proof_ref": f"fixture-only:{owner}:{idx}"}


def manifest_dep(owner: str, ver: str = "1.0.0", kind: str = "MODULE",
                 requires: list[str] | None = None, dep_components: list[str] | None = None) -> bytes:
    base = sel_manifest(owner, version=ver, kind=kind).decode("utf-8")
    if requires is not None:
        req = ", ".join(f'"{r}"' for r in requires)
        base = base.replace("requires=[]", f"requires=[{req}]")
    if dep_components:
        dep = ", ".join(f'"{d}"' for d in dep_components)
        base += f"\n[dependencies]\ncomponents=[{dep}]\n"
    return base.encode("utf-8")


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix=".c11-plan-", dir=str(ROOT / "frontend" / "tests"))
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def _owner(self, leaf: str, name: str, raw: bytes, js: bytes = JS, trust: str = "TRUSTED", ver: str = "1.0.0"):
        folder = self.work / leaf
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "frontend").mkdir(exist_ok=True)
        (folder / "component.toml").write_bytes(raw)
        (folder / ENTRY).write_bytes(js)
        return {"owner": name, "owner_version": ver, "root": folder.relative_to(ROOT).as_posix(),
                "trust": trust, "manifest": {"path": "component.toml", "sha256": sha(raw)},
                "sources": [{"path": ENTRY, "sha256": sha(js)}]}

    def _doc(self, owners: list[dict], off: list[str], req: list[str], prov=None, atts: list[dict] | None = None):
        return {"schema": "pixs.frontend.selection/1.0.0", "environment": "DEVELOPMENT",
                "provenance": {"kind": "LOCAL_OPERATOR_SELECTION", "reference": "fixture-only:c11-plan"},
                "components": owners,
                "composition": {"official_ids": off, "required_ids": req,
                                "configured_providers": prov, "attestations": atts if atts is not None else []}}

    def _blob(self, doc: dict):
        b = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return b, sha(b)

    def _limits(self, **kw):
        v = dict(max_selection_bytes=65536, max_owners=8, max_files_per_owner=8,
                 max_total_files=32, max_bytes_per_file=32768, max_total_bytes=262144)
        v.update(kw)
        return sel_limits_base(**{k: v[k] for k in v})

    def _cli(self, data: bytes, pin: str, timeout: int = 10):
        lim = self._limits()
        argv = [sys.executable, "-B", str(PLAN), "--expected-sha256", pin,
                "--project-root", str(ROOT), "--max-selection-bytes", str(lim.max_selection_bytes),
                "--max-owners", str(lim.max_owners), "--max-files-per-owner", str(lim.max_files_per_owner),
                "--max-total-files", str(lim.max_total_files), "--max-bytes-per-file", str(lim.max_bytes_per_file),
                "--max-total-bytes", str(lim.max_total_bytes)]
        env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(SRC), str(SCRIPTS)]),
                   PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run(argv, input=data, capture_output=True, env=env, shell=False, timeout=timeout, cwd=str(ROOT))

    def test_01_app_lib_reordered_hashes_and_no_activation(self):
        lib_raw = manifest_dep("acme.lib", requires=[])
        app_raw = manifest_dep("acme.app", kind="SUBMODULE", requires=["acme.lib.page >=1.0.0"], dep_components=["acme.lib >=1.0.0"])
        lib = self._owner("lib", "acme.lib", lib_raw)
        app = self._owner("app", "acme.app", app_raw)
        atts = [att("acme.app"), att("acme.lib", idx=1)]
        doc = self._doc([app, lib], ["acme.app", "acme.lib"], ["acme.app", "acme.lib"], None, atts)
        b, pin = self._blob(doc)
        env = prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        self.assertEqual(env.capture.errors, ())
        self.assertEqual(env.ignored_attestation_indices, ())
        self.assertEqual(set(env.plan.order), {"acme.app", "acme.lib"})
        self.assertEqual(env.plan.order[0], "acme.lib")
        by = {o.owner: o.manifest.sha256 for o in env.capture.owners}
        for o, d in env.plan.sources_sha256:
            self.assertEqual(by[o], d)
        self.assertIs(env.plan.globally_compatible, False)
        self.assertNotIn("active", env.to_dict())
        self.assertNotIn("backend_state", env.to_dict())

    def test_02_optional_absent_ignored_and_independent_planned(self):
        good_raw = manifest_dep("acme.good")
        bad_raw = manifest_dep("acme.bad")
        good = self._owner("good", "acme.good", good_raw)
        bad = self._owner("bad", "acme.bad", bad_raw)
        (self.work / "bad" / ENTRY).unlink()
        atts = [att("acme.bad", idx=0), att("acme.good", idx=1)]
        doc = self._doc([bad, good], ["acme.bad", "acme.good"], ["acme.good"], None, atts)
        b, pin = self._blob(doc)
        env = prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        self.assertEqual([o.owner for o in env.capture.owners], ["acme.good"])
        self.assertEqual(env.ignored_attestation_indices, (0,))
        self.assertEqual(tuple(env.plan.order), ("acme.good",))

    def test_03_required_missing_and_no_capture(self):
        good = self._owner("good", "acme.good", manifest_dep("acme.good"))
        doc = self._doc([good], ["acme.good", "acme.absent"], ["acme.good", "acme.absent"], None, [att("acme.good")])
        b, pin = self._blob(doc)
        with self.assertRaises(PlanError) as c:
            prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        self.assertEqual(c.exception.code, "REQUIRED_COMPONENT_UNCAPTURED")
        (ROOT / good["root"] / ENTRY).unlink()
        empty_doc = self._doc([good], [], [], None, [att("acme.good")])
        empty_raw, empty_pin = self._blob(empty_doc)
        with self.assertRaises(PlanError) as missing:
            prepare_frontend_plan(empty_raw, expected_sha256=empty_pin, project_root=ROOT, selection_limits=self._limits())
        self.assertEqual(missing.exception.code, "PLAN_NO_CAPTURE")

    def test_04_common_mandatory_edge_to_absent_kernel_rejected(self):
        surv_raw = manifest_dep("acme.surv", dep_components=["acme.absent"])
        surv = self._owner("surv", "acme.surv", surv_raw)
        doc = self._doc([surv], ["acme.surv"], ["acme.surv"], None, [att("acme.surv")])
        b, pin = self._blob(doc)
        with self.assertRaises(BuildError) as c:
            prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        self.assertEqual(c.exception.code, "BUILD_KERNEL_REJECTED")
        self.assertTrue(c.exception.diagnostics)

    def test_05_survivor_proofs_strict_and_unknown_extra_transmitted(self):
        base = self._owner("one", "acme.one", manifest_dep("acme.one"))
        good = att("acme.one")
        valid = self._doc([base], ["acme.one"], ["acme.one"], None, [good])
        raw, pin = self._blob(valid)
        self.assertEqual(prepare_frontend_plan(raw, expected_sha256=pin, project_root=ROOT,
                         selection_limits=self._limits()).plan.order, ("acme.one",))
        cases = (
            [att("acme.one", verdict="FAIL")],
            [good, att("acme.one", idx=1)],
            [att("acme.one", target="acme.other", idx=2)],
            [good, att("acme.unknown", idx=3)],
        )
        for supplied in cases:
            doc = self._doc([base], ["acme.one"], ["acme.one"], None, supplied)
            raw, pin = self._blob(doc)
            with self.subTest(proofs=len(supplied)):
                with self.assertRaises(BuildError) as caught:
                    prepare_frontend_plan(raw, expected_sha256=pin, project_root=ROOT,
                                          selection_limits=self._limits())
                self.assertEqual(caught.exception.code, "BUILD_KERNEL_REJECTED")
                self.assertTrue(caught.exception.diagnostics)

    def test_06_pin_blob_drift(self):
        owner = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([owner], ["acme.one"], ["acme.one"], None, [att("acme.one")])
        raw, pin = self._blob(doc)
        envelope = prepare_frontend_plan(raw, expected_sha256=pin, project_root=ROOT,
                                         selection_limits=self._limits())
        with self.assertRaises(SelectionError) as caught:
            prepare_frontend_plan(raw + b" ", expected_sha256=pin, project_root=ROOT,
                                  selection_limits=self._limits())
        self.assertEqual(caught.exception.code, "SELECTION_PIN_MISMATCH")
        with self.assertRaises(PlanError) as caught:
            plan_from_capture(envelope.capture, selection_bytes=raw + b" ", limits=envelope.build_limits)
        self.assertEqual(caught.exception.code, "SELECTION_DRIFT")

    def test_07_dto_indices_coverage_tamper(self):
        from build_frontend_selection import CaptureError
        owner = self._owner("one", "acme.one", manifest_dep("acme.one"))
        raw, pin = self._blob(self._doc([owner], ["acme.one"], ["acme.one"], None, [att("acme.one")]))
        envelope = prepare_frontend_plan(raw, expected_sha256=pin, project_root=ROOT,
                                         selection_limits=self._limits())
        capture = envelope.capture
        for modified in (
            replace(capture, errors=(CaptureError(7, "", "", "SOURCE_UNAVAILABLE", ""),)),
            replace(capture, errors=(CaptureError(0, "", "", "SOURCE_UNAVAILABLE", ""),)),
            replace(capture, owners=(), errors=()),
        ):
            with self.assertRaises(PlanError) as caught:
                plan_from_capture(modified, selection_bytes=raw, limits=envelope.build_limits)
            self.assertEqual(caught.exception.code, "PLAN_CAPTURE_INVALID")

    def test_08_snapshot_modified_and_allowed_sources(self):
        o = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([o], ["acme.one"], ["acme.one"], None, [att("acme.one")])
        b, pin = self._blob(doc)
        from build_frontend_selection import capture_selection
        cap = capture_selection(b, expected_sha256=pin, project_root=ROOT, limits=self._limits())
        lim = BuildLimits(8, 32768, 262144, ("elsewhere/component.toml",))
        with self.assertRaises(PlanError) as c:
            plan_from_capture(cap, selection_bytes=b, limits=lim)
        self.assertEqual(c.exception.code, "PLAN_ENVELOPE_INVALID")

    def test_09_checksum_ignored_tamper(self):
        o = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([o], ["acme.one"], ["acme.one"], None, [att("acme.one")])
        b, pin = self._blob(doc)
        env = prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        with self.assertRaises(PlanError):
            PlanEnvelope(env.capture, env.plan, (7,), env.build_limits, env.context_checksum, env.declared_owner_ids)
        with self.assertRaises(PlanError):
            PlanEnvelope(env.capture, env.plan, env.ignored_attestation_indices, env.build_limits, "0" * 64, env.declared_owner_ids)

    def test_10_envelope_frozen_and_deepcopy(self):
        o = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([o], ["acme.one"], ["acme.one"], None, [att("acme.one")])
        b, pin = self._blob(doc)
        env = prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        with self.assertRaises(FrozenInstanceError):
            env.context_checksum = "x"
        v = env.to_dict()
        v["plan"]["order"].append("invented")
        self.assertNotIn("invented", env.to_dict()["plan"]["order"])

    def test_11_unicode_comma_paths_preserved(self):
        raw = manifest_dep("acme.uni")
        leaf = "café,coin"
        folder = self.work / leaf
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "frontend").mkdir(exist_ok=True)
        (folder / "component.toml").write_bytes(raw)
        (folder / ENTRY).write_bytes(JS)
        o = {"owner": "acme.uni", "owner_version": "1.0.0", "root": folder.relative_to(ROOT).as_posix(),
             "trust": "TRUSTED", "manifest": {"path": "component.toml", "sha256": sha(raw)},
             "sources": [{"path": ENTRY, "sha256": sha(JS)}]}
        doc = self._doc([o], ["acme.uni"], ["acme.uni"], None, [att("acme.uni")])
        b, pin = self._blob(doc)
        env = prepare_frontend_plan(b, expected_sha256=pin, project_root=ROOT, selection_limits=self._limits())
        self.assertEqual(env.capture.owners[0].root, folder.relative_to(ROOT).as_posix())
        self.assertIn(",", env.capture.owners[0].root)
        self.assertEqual(len(env.context_checksum), 64)

    def test_12_cli_nominal(self):
        o = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([o], ["acme.one"], ["acme.one"], None, [att("acme.one")])
        b, pin = self._blob(doc)
        r = self._cli(b, pin)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout.decode("utf-8"))
        self.assertEqual(out["ignored_attestation_indices"], [])
        self.assertIs(out["plan"]["globally_compatible"], False)

    def test_13_cli_required_absent(self):
        o = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([o], ["acme.one", "acme.absent"], ["acme.one", "acme.absent"], None, [att("acme.one")])
        b, pin = self._blob(doc)
        r = self._cli(b, pin)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stderr, b"REQUIRED_COMPONENT_UNCAPTURED\n")
        self.assertNotIn(b"C11_PRIVATE", r.stderr)

    def test_14_cli_pin_and_limits_errors(self):
        o = self._owner("one", "acme.one", manifest_dep("acme.one"))
        doc = self._doc([o], ["acme.one"], ["acme.one"], None, [att("acme.one")])
        b, pin = self._blob(doc)
        r = self._cli(b, "0" * 64)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stderr, b"SELECTION_PIN_MISMATCH\n")


    def test_15_composition_snapshot_cannot_override_pinned_document(self):
        owner = self._owner("one", "acme.one", manifest_dep("acme.one"))
        raw, pin = self._blob(self._doc([owner], ["acme.one"], ["acme.one"], None, [att("acme.one")]))
        envelope = prepare_frontend_plan(raw, expected_sha256=pin, project_root=ROOT,
                                         selection_limits=self._limits())
        modified = replace(envelope.capture, composition=replace(envelope.capture.composition, required_ids=()))
        with self.assertRaises(PlanError) as caught:
            plan_from_capture(modified, selection_bytes=raw, limits=envelope.build_limits)
        self.assertEqual(caught.exception.code, "PLAN_CAPTURE_INVALID")


if __name__ == "__main__":
    unittest.main()
