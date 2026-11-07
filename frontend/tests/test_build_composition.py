"""C11 tâche 2.1 — pont manifest->build testable sur Kernel réel, sans mock."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

_BRIDGE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_frontend_composition.py"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_TESTS_DIR = _PROJECT_ROOT / "frontend" / "tests"
_GENERATED_DIR = _PROJECT_ROOT / "frontend" / ".generated"

_spec = importlib.util.spec_from_file_location("build_frontend_composition", str(_BRIDGE_PATH))
assert _spec is not None and _spec.loader is not None
_bridge = importlib.util.module_from_spec(_spec)
sys.modules["build_frontend_composition"] = _bridge
_spec.loader.exec_module(_bridge)

BuildLimits = _bridge.BuildLimits
BuildError = _bridge.BuildError
BuildPlan = _bridge.BuildPlan
PlanDiagnostic = _bridge.PlanDiagnostic
PlanFacet = _bridge.PlanFacet
build_plan = _bridge.build_plan
read_manifest_texts = _bridge.read_manifest_texts
write_plan = _bridge.write_plan

from pixs.kernel.composition import compose
from pixs.kernel.conformity import ConformityAttestation


def _pure_limits(**over):
    kw = dict(max_manifests=8, max_manifest_bytes=32768, max_total_bytes=262144,
              allowed_sources=("frontend/tests/component.toml",))
    kw.update(over)
    return BuildLimits(**kw)


def _toml(*, mid, mtype="MODULE", version="1.0.0", deps=(), frontend=None):
    lines = [f'schema_version = "1"', f'id = "{mid}"', f'type = "{mtype}"', f'version = "{version}"']
    if deps:
        quoted = ", ".join(f'"{d}"' for d in deps)
        lines += ["[dependencies]", f"components = [{quoted}]"]
    if frontend is not None:
        lines += ['[frontend]', 'schema_version = "1"']
        if frontend:
            for c in frontend:
                req = ", ".join(f'"{r}"' for r in c.get("requires", []))
                lines += ['[[frontend.contributions]]', f'type = "{c["type"]}"',
                          f'id = "{c["id"]}"', f'entry = "{c["entry"]}"',
                          f'version = "{c["version"]}"', f"requires = [{req}]",
                          f'scope = "{c["scope"]}"']
        else:
            lines += ["contributions = []"]
    return "\n".join(lines) + "\n"


def _facet(*, ftype="ROUTE", fid="acme.crm.contacts", entry="frontend/routes/contacts",
           version="1.0.0", requires=(), scope="TENANT_SCOPED"):
    return {"type": ftype, "id": fid, "entry": entry, "version": version,
            "requires": list(requires), "scope": scope}


def _att(mid, version="1.0.0"):
    return ConformityAttestation(component_id=mid, component_version=version,
                                 scope="COMPONENT", target_id=mid, target_version=version,
                                 suite_id="acme.suite", suite_version="1.0.0",
                                 verdict="PASS", proof_ref="proof:acme:" + mid)


def _assert_diag(test, diag):
    test.assertIs(type(diag.stage), str)
    test.assertIs(type(diag.element), str)
    test.assertIs(type(diag.constraint), str)
    test.assertIs(type(diag.message), str)
    d = diag.to_dict()
    test.assertEqual(set(d), {"stage", "element", "constraint", "message"})


class TestBuildLimits(unittest.TestCase):
    def test_bool_zero_and_types_rejected(self):
        for kw in (dict(max_manifests=True), dict(max_manifests=0),
                   dict(max_manifest_bytes="1"), dict(max_total_bytes=0),
                   dict(max_manifests=1.0)):
            with self.subTest(kw=kw):
                with self.assertRaises(BuildError) as ctx:
                    _pure_limits(**kw)
                self.assertEqual(ctx.exception.code, "BUILD_LIMITS_INVALID")

    def test_allowed_sources_empty_duplicate_forbidden(self):
        with self.assertRaises(BuildError):
            _pure_limits(allowed_sources=())
        with self.assertRaises(BuildError):
            _pure_limits(allowed_sources=("frontend/tests/component.toml",
                                          "frontend/tests/component.toml"))
        for bad in ("frontend/.cache/a/component.toml", "frontend/.git/a/component.toml",
                    "frontend/tests/other.txt", "../frontend/tests/component.toml",
                    "/frontend/tests/component.toml", "frontend//tests/component.toml"):
            with self.subTest(bad=bad):
                with self.assertRaises(BuildError):
                    _pure_limits(allowed_sources=(bad,))

    def test_bytes_count_nul_non_str(self):
        lim = _pure_limits(max_manifests=2, max_manifest_bytes=10, max_total_bytes=12)
        with self.assertRaises(BuildError) as ctx:
            build_plan(("x" * 11,), official_ids=(), required_ids=(),
                       configured_providers={}, attestations=(), limits=lim)
        self.assertEqual(ctx.exception.code, "BUILD_MANIFEST_TOO_LARGE")
        with self.assertRaises(BuildError) as ctx:
            build_plan(("a\x00b",), official_ids=(), required_ids=(),
                       configured_providers={}, attestations=(), limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_TEXT_INVALID")
        with self.assertRaises(BuildError):
            build_plan(("ok", 1), official_ids=(), required_ids=(),
                       configured_providers={}, attestations=(), limits=_pure_limits())

    def test_utf8_multibyte_exact_and_exceed(self):
        base = _toml(mid="acme.a", frontend=[])
        text = base + "# é\n"
        n = len(text.encode("utf-8"))
        lim_exact = _pure_limits(max_manifest_bytes=n, max_total_bytes=n)
        plan = build_plan((text,), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=lim_exact)
        self.assertEqual(plan.order, ("acme.a",))
        lim_short = _pure_limits(max_manifest_bytes=n - 1, max_total_bytes=262144)
        with self.assertRaises(BuildError) as ctx:
            build_plan((text,), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(_att("acme.a"),), limits=lim_short)
        self.assertEqual(ctx.exception.code, "BUILD_MANIFEST_TOO_LARGE")

    def test_total_distinct_from_count(self):
        a = _toml(mid="acme.a", frontend=[])
        b = _toml(mid="acme.b", frontend=[])
        total = len(a.encode()) + len(b.encode())
        lim = _pure_limits(max_manifests=8, max_manifest_bytes=32768, max_total_bytes=total - 1)
        with self.assertRaises(BuildError) as ctx:
            build_plan((a, b), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(_att("acme.a"), _att("acme.b")), limits=lim)
        self.assertEqual(ctx.exception.code, "BUILD_TOTAL_TOO_LARGE")


    def test_count_limit_distinct_from_bytes(self):
        with self.assertRaises(BuildError) as ctx:
            build_plan((_toml(mid="acme.a"), _toml(mid="acme.b")), official_ids=(),
                       required_ids=(), configured_providers={}, attestations=(),
                       limits=_pure_limits(max_manifests=1))
        self.assertEqual(ctx.exception.code, "BUILD_MANIFEST_COUNT_INVALID")


class TestSelection(unittest.TestCase):
    def test_official_required_strict(self):
        for bad in (["a"], ("a", "a"), ("",), ("a\x00",), (1,), "a"):
            with self.subTest(bad=bad):
                with self.assertRaises(BuildError) as ctx:
                    build_plan((_toml(mid="acme.a"),), official_ids=bad, required_ids=(),
                               configured_providers={}, attestations=(), limits=_pure_limits())
                self.assertEqual(ctx.exception.code, "BUILD_SELECTION_INVALID")
                with self.assertRaises(BuildError):
                    build_plan((_toml(mid="acme.a"),), official_ids=(), required_ids=bad,
                               configured_providers={}, attestations=(), limits=_pure_limits())

    def test_providers_mapping_strict(self):
        for bad in ({"": "v"}, {"k": ""}, {"k\x00": "v"}, {"k": 1}, [("k", "v")], "x"):
            with self.subTest(bad=bad):
                with self.assertRaises(BuildError) as ctx:
                    build_plan((_toml(mid="acme.a"),), official_ids=(), required_ids=(),
                               configured_providers=bad, attestations=(), limits=_pure_limits())
                self.assertEqual(ctx.exception.code, "BUILD_SELECTION_INVALID")

    def test_attestations_must_be_tuple(self):
        with self.assertRaises(BuildError) as ctx:
            build_plan((_toml(mid="acme.a"),), official_ids=(), required_ids=(),
                       configured_providers={}, attestations=[], limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_ATTESTATIONS_INVALID")


class TestTrueManifests(unittest.TestCase):
    def test_module_and_submodule_empty_frontend(self):
        a = _toml(mid="acme.app", mtype="MODULE", frontend=[])
        b = _toml(mid="acme.sub", mtype="SUBMODULE", frontend=[])
        plan = build_plan((a, b), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.app"), _att("acme.sub")), limits=_pure_limits())
        self.assertEqual(set(plan.order), {"acme.app", "acme.sub"})
        self.assertEqual(plan.facets, ())
        self.assertFalse(plan.globally_compatible)
        self.assertEqual(len(plan.sources_sha256), 2)

    def test_order_edges_facets_requires_preserved(self):
        lib = _toml(mid="acme.lib", frontend=[_facet(fid="acme.lib.home", entry="frontend/lib/home")])
        app = _toml(mid="acme.app", deps=("acme.lib >=1.0.0 <2.0.0",),
                    frontend=[_facet(fid="acme.app.main", entry="frontend/app/main")])
        plan = build_plan((app, lib), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.app"), _att("acme.lib")), limits=_pure_limits())
        self.assertEqual(plan.order, ("acme.lib", "acme.app"))
        self.assertIn(("acme.app", "acme.lib"), plan.edges)
        by_owner = {f.owner: f for f in plan.facets}
        self.assertEqual(by_owner["acme.app"].id, "acme.app.main")
        self.assertEqual(by_owner["acme.lib"].entry, "frontend/lib/home")

    def test_frontend_requires_text_multiplicity_not_graph(self):
        txt = _toml(mid="acme.a", frontend=[_facet(requires=("audit >=1.0.0 <2.0.0",
                                                             "audit >=1.0.0 <2.0.0"))])
        plan = build_plan((txt,), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=_pure_limits())
        self.assertEqual(len(plan.facets), 1)
        self.assertEqual(plan.facets[0].requires,
                         ("audit >=1.0.0 <2.0.0", "audit >=1.0.0 <2.0.0"))
        self.assertIs(type(plan.facets[0].requires), tuple)
        self.assertEqual(plan.edges, ())
        self.assertEqual(plan.order, ("acme.a",))

    def test_determinism_same_and_permuted(self):
        a = _toml(mid="acme.a", frontend=[])
        b = _toml(mid="acme.b", frontend=[])
        kw = dict(official_ids=(), required_ids=(), configured_providers={},
                  attestations=(_att("acme.a"), _att("acme.b")), limits=_pure_limits())
        first = build_plan((a, b), **kw)
        second = build_plan((a, b), **kw)
        self.assertEqual(first.to_dict(), second.to_dict())
        swapped = build_plan((b, a), official_ids=(), required_ids=(), configured_providers={},
                             attestations=(_att("acme.b"), _att("acme.a")), limits=_pure_limits())
        self.assertEqual(first.order, swapped.order)
        self.assertEqual(first.to_dict(), swapped.to_dict())

    def test_hashes_trace_without_auth(self):
        a = _toml(mid="acme.a", frontend=[])
        plan = build_plan((a,), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=_pure_limits())
        self.assertEqual(plan.sources_sha256, (("acme.a", hashlib.sha256(a.encode()).hexdigest()),))

    def test_simple_module_missing_then_with_attestation(self):
        txt = _toml(mid="acme.a", frontend=[])
        with self.assertRaises(BuildError) as ctx:
            build_plan((txt,), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(), limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_KERNEL_REJECTED")
        self.assertTrue(ctx.exception.diagnostics)
        joined = ";".join(d.message for d in ctx.exception.diagnostics)
        self.assertIn("preuve manquante", joined)
        self.assertIn("acme.a", joined)
        for d in ctx.exception.diagnostics:
            _assert_diag(self, d)
        plan = build_plan((txt,), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=_pure_limits())
        self.assertEqual(plan.order, ("acme.a",))

    def test_cycle_targeted(self):
        a = _toml(mid="acme.a", deps=("acme.b",), frontend=[])
        b = _toml(mid="acme.b", deps=("acme.a",), frontend=[])
        with self.assertRaises(BuildError) as ctx:
            build_plan((a, b), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(_att("acme.a"), _att("acme.b")), limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_KERNEL_REJECTED")
        self.assertTrue(ctx.exception.diagnostics)
        joined = ";".join(d.message + d.constraint for d in ctx.exception.diagnostics)
        self.assertIn("cycle", joined)
        self.assertIn("acme.a", joined)
        self.assertIn("acme.b", joined)

    def test_absent_targeted(self):
        ghost = _toml(mid="acme.a", deps=("acme.ghost >=1.0.0",), frontend=[])
        with self.assertRaises(BuildError) as ctx:
            build_plan((ghost,), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(_att("acme.a"),), limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_KERNEL_REJECTED")
        joined = ";".join(d.message for d in ctx.exception.diagnostics)
        self.assertIn("absent", joined)
        self.assertIn("acme.ghost", joined)

    def test_incompatible_version_targeted(self):
        lib = _toml(mid="acme.lib", version="1.0.0", frontend=[])
        app = _toml(mid="acme.app", deps=("acme.lib ==9.0.0",), frontend=[])
        with self.assertRaises(BuildError) as ctx:
            build_plan((app, lib), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(_att("acme.app"), _att("acme.lib")), limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_KERNEL_REJECTED")
        self.assertTrue(ctx.exception.diagnostics)
        joined = ";".join(d.message + d.constraint for d in ctx.exception.diagnostics)
        self.assertIn("acme.lib", joined)

    def test_duplicate_identity_targeted(self):
        dup = _toml(mid="acme.dup", frontend=[])
        with self.assertRaises(BuildError) as ctx:
            build_plan((dup, dup), official_ids=(), required_ids=(), configured_providers={},
                       attestations=(_att("acme.dup"),), limits=_pure_limits())
        self.assertEqual(ctx.exception.code, "BUILD_KERNEL_REJECTED")
        self.assertTrue(ctx.exception.diagnostics)
        joined = ";".join(d.message + d.element for d in ctx.exception.diagnostics)
        self.assertIn("acme.dup", joined)

    def test_warnings_projected_from_compose(self):
        txt = (_toml(mid="acme.a", frontend=[])
               + '[optional_dependencies]\ncomponents = ["acme.ghost >=1.0.0"]\n')
        texts = (txt,)
        plan = build_plan(texts, official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=_pure_limits())
        self.assertEqual(plan.order, ("acme.a",))
        result = compose(texts, official_ids=(), required_ids=(), configured_providers={},
                         attestations=(_att("acme.a"),))
        expected_w = tuple(PlanDiagnostic.from_kernel(w) for w in result.warnings)
        self.assertEqual(plan.warnings, expected_w)
        self.assertEqual(plan.evaluation_scope, tuple(result.evaluation_scope))
        self.assertEqual(plan.unevaluated_dimensions, tuple(result.unevaluated_dimensions))

    def test_dto_frozen_and_deep_copies(self):
        from dataclasses import FrozenInstanceError
        txt = _toml(mid="acme.a", frontend=[_facet(requires=("audit >=1.0.0",))])
        plan = build_plan((txt,), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=_pure_limits())
        self.assertTrue(plan.facets)
        facet = plan.facets[0]
        with self.assertRaises(FrozenInstanceError):
            facet.id = "x"
        with self.assertRaises(FrozenInstanceError):
            plan.order = ()
        diag = PlanDiagnostic("s", "e", "c", "m")
        with self.assertRaises(FrozenInstanceError):
            diag.message = "y"
        d1 = plan.to_dict()
        d1["facets"][0]["requires"].append("injected")
        d1["facets"].clear()
        d1["warnings"].clear()
        d1["order"].append("x")
        d2 = plan.to_dict()
        self.assertEqual(d2["facets"][0]["requires"], ["audit >=1.0.0"])
        self.assertEqual(len(d2["facets"]), 1)
        self.assertEqual(d2["order"], ["acme.a"])
        self.assertEqual(d2["schema"], "pixs.frontend.build-plan/1")
        self.assertEqual(d2["diagnostics"], [])


class _FsCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix=".c11-bridge-", dir=str(_TESTS_DIR))
        self.addCleanup(self.tmp.cleanup)
        self.root = _PROJECT_ROOT
        self.tmp_path = Path(self.tmp.name)
        self.created_outputs = []
        _GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        self.output_tmp = tempfile.TemporaryDirectory(prefix="c11-", dir=str(_GENERATED_DIR))
        self.addCleanup(self.output_tmp.cleanup)
        self.output_path = Path(self.output_tmp.name)

    def tearDown(self):
        for rel in self.created_outputs:
            p = self.root / rel
            if p.exists():
                p.unlink()
        self.assertEqual(list(self.output_path.glob(".composition-*.tmp")), [])

    def _rel(self, *parts):
        return (self.tmp_path.joinpath(*parts).relative_to(self.root)).as_posix()

    def _write(self, rel, data: bytes):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return rel

    def _output(self):
        return (self.output_path / (uuid.uuid4().hex + ".json")).relative_to(self.root).as_posix()

    def _track(self, rel):
        self.created_outputs.append(rel)
        return rel


class TestReadManifestTexts(_FsCase):
    def test_explicit_selection_only(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", frontend=[]).encode())
        lim = BuildLimits(8, 32768, 262144, (rel,))
        self.assertIn('id = "acme.a"', read_manifest_texts((rel,), project_root=self.root, limits=lim)[0])
        other = self._rel("b", "component.toml")
        self._write(other, _toml(mid="acme.b", frontend=[]).encode())
        with self.assertRaises(BuildError) as ctx:
            read_manifest_texts((other,), project_root=self.root, limits=lim)
        self.assertEqual(ctx.exception.code, "BUILD_SOURCE_FORBIDDEN")

    def test_invalid_utf8_and_too_large(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, b'schema_version = "1"\nid = "\xff"\n')
        lim = BuildLimits(8, 32768, 262144, (rel,))
        with self.assertRaises(BuildError) as ctx:
            read_manifest_texts((rel,), project_root=self.root, limits=lim)
        self.assertEqual(ctx.exception.code, "BUILD_TEXT_INVALID")
        rel2 = self._rel("b", "component.toml")
        self._write(rel2, _toml(mid="acme.b", frontend=[]).encode())
        small = BuildLimits(8, 10, 100000, (rel2,))
        with self.assertRaises(BuildError) as ctx:
            read_manifest_texts((rel2,), project_root=self.root, limits=small)
        self.assertEqual(ctx.exception.code, "BUILD_SOURCE_TOO_LARGE")

    def test_dotdot_absolute_cache_forbidden(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", frontend=[]).encode())
        lim = BuildLimits(8, 32768, 262144, (rel,))
        for bad in ("../frontend/tests/x/component.toml", "/frontend/tests/x/component.toml",
                    "frontend/.cache/x/component.toml"):
            with self.subTest(bad=bad):
                with self.assertRaises(BuildError):
                    read_manifest_texts((bad,), project_root=self.root, limits=lim)

    def test_symlink_file_and_dir_refused(self):
        target_rel = self._rel("real", "component.toml")
        self._write(target_rel, _toml(mid="acme.a", frontend=[]).encode())
        link_rel = self._rel("link", "component.toml")
        (self.root / link_rel).parent.mkdir(parents=True, exist_ok=True)
        os.symlink(self.root / target_rel, self.root / link_rel)
        lim = BuildLimits(8, 32768, 262144, (link_rel,))
        with self.assertRaises(BuildError):
            read_manifest_texts((link_rel,), project_root=self.root, limits=lim)
        dir_target = self.tmp_path / "realdir"
        dir_target.mkdir()
        (dir_target / "component.toml").write_bytes(_toml(mid="acme.b", frontend=[]).encode())
        dir_link = self.tmp_path / "linkdir"
        os.symlink(str(dir_target), str(dir_link))
        dir_rel = dir_link.joinpath("component.toml").relative_to(self.root).as_posix()
        lim2 = BuildLimits(8, 32768, 262144, (dir_rel,))
        with self.assertRaises(BuildError):
            read_manifest_texts((dir_rel,), project_root=self.root, limits=lim2)


class TestWritePlan(_FsCase):
    def _plan(self):
        return build_plan((_toml(mid="acme.a", frontend=[]),), official_ids=(), required_ids=(),
                          configured_providers={}, attestations=(_att("acme.a"),),
                          limits=_pure_limits())

    def test_output_only_generated_json(self):
        plan = self._plan()
        for bad in ("frontend/tests/out.json", "frontend/.generated/out.txt",
                    "frontend/.generated/../tests/out.json", "/frontend/.generated/out.json"):
            with self.subTest(bad=bad):
                with self.assertRaises(BuildError):
                    write_plan(plan, project_root=self.root, output=bad)

    def test_symlink_output_refused(self):
        plan = self._plan()
        out = self._track(self._output())
        link = self.root / out
        link.parent.mkdir(parents=True, exist_ok=True)
        outside = self.tmp_path / "outside.json"
        outside.write_text("{}", encoding="utf-8")
        os.symlink(str(outside), str(link))
        with self.assertRaises(BuildError):
            write_plan(plan, project_root=self.root, output=out)
        link.unlink()
        self.created_outputs.remove(out)

    def test_nominal_write_then_reread(self):
        plan = self._plan()
        out = self._track(self._output())
        write_plan(plan, project_root=self.root, output=out)
        payload = json.loads((self.root / out).read_text(encoding="utf-8"))
        self.assertEqual(payload["order"], ["acme.a"])
        self.assertEqual(payload["globally_compatible"], False)


    def test_atomic_replacement_and_output_directory_symlink(self):
        plan = self._plan()
        out = self._track(self._output())
        target = self.root / out
        target.write_text('{"old":true}', encoding="utf-8")
        before_inode = target.stat().st_ino
        write_plan(plan, project_root=self.root, output=out)
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")), plan.to_dict())
        self.assertNotEqual(target.stat().st_ino, before_inode)
        link = self.output_path / "linked"
        link.symlink_to(self.tmp_path, target_is_directory=True)
        bad = (link / "out.json").relative_to(self.root).as_posix()
        with self.assertRaises(BuildError):
            write_plan(plan, project_root=self.root, output=bad)
        self.assertFalse((self.tmp_path / "out.json").exists())


class TestMainCLI(_FsCase):
    def _run(self, argv):
        return subprocess.run([sys.executable, str(_BRIDGE_PATH), *argv],
                              cwd=str(self.root), capture_output=True, text=True,
                              timeout=30, shell=False)

    def _args(self, rels, out, allowed, official=(), required=(), providers=None):
        if providers is None:
            providers = {}
        argv = []
        for r in rels:
            argv += ["--manifest", r]
        argv += ["--project-root", str(self.root), "--out", out,
                 "--allowed-sources-json", json.dumps(list(allowed)),
                 "--official-ids-json", json.dumps(list(official)),
                 "--required-ids-json", json.dumps(list(required)),
                 "--configured-providers-json", json.dumps(dict(providers)),
                 "--max-manifests", "8", "--max-manifest-bytes", "32768",
                 "--max-total-bytes", "262144"]
        return argv

    def test_cli_valid_manifest_refused_without_attestation(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", frontend=[]).encode())
        out = self._output()
        proc = self._run(self._args((rel,), out, (rel,)))
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("BUILD_KERNEL_REJECTED", proc.stderr)
        self.assertFalse((self.root / out).exists())

    def test_cli_same_manifest_api_with_attestation_succeeds(self):
        rel = self._rel("a", "component.toml")
        text = _toml(mid="acme.a", frontend=[])
        self._write(rel, text.encode())
        plan = build_plan((text,), official_ids=(), required_ids=(), configured_providers={},
                          attestations=(_att("acme.a"),), limits=_pure_limits())
        out = self._track(self._output())
        write_plan(plan, project_root=self.root, output=out)
        payload = json.loads((self.root / out).read_text(encoding="utf-8"))
        self.assertEqual(payload["order"], ["acme.a"])

    def test_cli_refusal_leaves_no_file(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", deps=("acme.ghost >=1.0.0",), frontend=[]).encode())
        out = self._output()
        proc = self._run(self._args((rel,), out, (rel,)))
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(proc.stderr.strip())
        self.assertFalse((self.root / out).exists())

    def test_cli_atomic_replace_preserves_on_refusal(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", frontend=[]).encode())
        plan = build_plan((_toml(mid="acme.a", frontend=[]),), official_ids=(), required_ids=(),
                          configured_providers={}, attestations=(_att("acme.a"),),
                          limits=_pure_limits())
        out = self._track(self._output())
        write_plan(plan, project_root=self.root, output=out)
        before = (self.root / out).read_text(encoding="utf-8")
        (self.root / rel).write_bytes(_toml(mid="acme.a", deps=("acme.ghost >=1.0.0",),
                                            frontend=[]).encode())
        proc = self._run(self._args((rel,), out, (rel,)))
        self.assertEqual(proc.returncode, 2)
        self.assertEqual((self.root / out).read_text(encoding="utf-8"), before)

    def test_cli_root_isolated(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", frontend=[]).encode())
        out = self._output()
        argv = self._args((rel,), out, (rel,))
        idx = argv.index("--project-root") + 1
        argv[idx] = "/nope"
        proc = self._run(argv)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("BUILD_ROOT_INVALID", proc.stderr)
        self.assertFalse((self.root / out).exists())

    def test_cli_flags_required_and_json_invalid(self):
        rel = self._rel("a", "component.toml")
        self._write(rel, _toml(mid="acme.a", frontend=[]).encode())
        out = self._output()
        proc = subprocess.run([sys.executable, str(_BRIDGE_PATH), "--manifest", rel],
                              cwd=str(self.root), capture_output=True, text=True,
                              timeout=30, shell=False)
        self.assertEqual(proc.returncode, 2)
        bad_dup = self._args((rel,), out, (rel,), providers={"k": "1"})
        # Duplique la clé JSON brute pour _pairs.
        dup_json = '{"k": "1", "k": "2"}'
        argv = list(bad_dup)
        argv[argv.index("--configured-providers-json") + 1] = dup_json
        proc2 = self._run(argv)
        self.assertEqual(proc2.returncode, 2)
        self.assertIn("BUILD_SELECTION_INVALID", proc2.stderr)
        argv3 = list(bad_dup)
        argv3[argv3.index("--allowed-sources-json") + 1] = '{"not": "alist"}'
        proc3 = self._run(argv3)
        self.assertEqual(proc3.returncode, 2)
        argv4 = list(bad_dup)
        argv4[argv4.index("--official-ids-json") + 1] = "not json{"
        proc4 = self._run(argv4)
        self.assertEqual(proc4.returncode, 2)
        for p in (out,):
            self.assertFalse((self.root / p).exists())


if __name__ == "__main__":
    unittest.main()
