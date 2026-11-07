"""Tests unitaires requirement facts contributions (tache 2.2, build seul)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from composition_requirements_v1 import (
    RequirementCandidate,
    RequirementFact,
    RequirementFacts,
    RequirementsError,
    RequirementsLimits,
    analyze_contribution_requirements,
)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SCRIPTS = ROOT / "frontend" / "scripts"


def _limits(**over):
    kw = dict(max_contributions=8, max_requirements_per_contribution=8, max_total_requirements=32)
    kw.update(over)
    return RequirementsLimits(**kw)


def _facet(*, owner="acme.app", owner_version="1.0.0", type_="ROUTE",
           fid="acme.app.home", entry="frontend/routes/home", version="1.0.0",
           requires=(), scope="TENANT_SCOPED"):
    return {
        "owner": owner,
        "owner_version": owner_version,
        "type": type_,
        "id": fid,
        "entry": entry,
        "version": version,
        "requires": list(requires),
        "scope": scope,
    }


def _order(*names):
    return tuple(names)


def _edges(*pairs):
    return tuple((a, b) for a, b in pairs)


def _codes(result):
    return [item.code for item in result.facts]


class TestSatisfiedEdges(unittest.TestCase):
    def test_same_owner_satisfied_with_edge_included(self):
        facets = (
            _facet(fid="acme.app.a", requires=["acme.app.b >=1.0.0"]),
            _facet(fid="acme.app.b"),
        )
        result = analyze_contribution_requirements(
            facets, component_order=_order("acme.app"), component_edges=_edges(),
            limits=_limits(),
        )
        self.assertEqual(_codes(result), ["SATISFIED"])
        self.assertIn(("acme.app", "acme.app.a", "acme.app", "acme.app.b"), result.frontend_edges)
        self.assertTrue(result.all_satisfied)

    def test_self_and_ab_cycle_kept_as_facts(self):
        facets = (
            _facet(fid="acme.app.a", requires=["acme.app.a >=1.0.0"]),
            _facet(fid="acme.app.b", requires=["acme.app.c >=1.0.0"]),
            _facet(fid="acme.app.c", requires=["acme.app.b >=1.0.0"]),
        )
        result = analyze_contribution_requirements(
            facets, component_order=_order("acme.app"), component_edges=_edges(),
            limits=_limits(),
        )
        self.assertTrue(all(code == "SATISFIED" for code in _codes(result)))
        self.assertIn(("acme.app", "acme.app.a", "acme.app", "acme.app.a"), result.frontend_edges)
        self.assertIn(("acme.app", "acme.app.b", "acme.app", "acme.app.c"), result.frontend_edges)
        self.assertIn(("acme.app", "acme.app.c", "acme.app", "acme.app.b"), result.frontend_edges)

    def test_direct_and_transitive_satisfied(self):
        facets = (
            _facet(owner="acme.lib", fid="acme.lib.home"),
            _facet(owner="acme.mid", fid="acme.mid.page", requires=["acme.lib.home >=1.0.0"]),
            _facet(owner="acme.app", fid="acme.app.main", requires=["acme.mid.page >=1.0.0", "acme.lib.home >=1.0.0"]),
        )
        order = _order("acme.lib", "acme.mid", "acme.app")
        edges = _edges(("acme.mid", "acme.lib"), ("acme.app", "acme.mid"))
        result = analyze_contribution_requirements(
            facets, component_order=order, component_edges=edges, limits=_limits(),
        )
        self.assertEqual(_codes(result), ["SATISFIED", "SATISFIED", "SATISFIED"])
        self.assertIn(("acme.app", "acme.app.main", "acme.mid", "acme.mid.page"), result.frontend_edges)
        self.assertIn(("acme.app", "acme.app.main", "acme.lib", "acme.lib.home"), result.frontend_edges)


class TestPreciseCodes(unittest.TestCase):
    def test_owner_without_common_dependency(self):
        facets = (
            _facet(owner="acme.lib", fid="acme.lib.home"),
            _facet(owner="acme.app", fid="acme.app.main", requires=["acme.lib.home >=1.0.0"]),
        )
        result = analyze_contribution_requirements(
            facets, component_order=_order("acme.lib", "acme.app"),
            component_edges=_edges(), limits=_limits(),
        )
        self.assertEqual(_codes(result), ["OWNER_DEPENDENCY_UNDECLARED"])
        self.assertFalse(result.all_satisfied)

    def test_missing_exact(self):
        facets = (_facet(requires=["acme.ghost >=1.0.0"]),)
        result = analyze_contribution_requirements(
            facets, component_order=_order("acme.app"), component_edges=_edges(),
            limits=_limits(),
        )
        self.assertEqual(_codes(result), ["MISSING"])
        self.assertEqual(result.frontend_edges, ())
        self.assertFalse(result.all_satisfied)

    def test_ambiguous_no_implicit_selection(self):
        facets = (
            _facet(owner="acme.a", fid="acme.shared", version="1.0.0"),
            _facet(owner="acme.b", fid="acme.shared", version="9.0.0"),
            _facet(owner="acme.app", fid="acme.app.main", requires=["acme.shared ==1.0.0"]),
        )
        order = _order("acme.a", "acme.b", "acme.app")
        edges = _edges(("acme.app", "acme.a"), ("acme.app", "acme.b"))
        result = analyze_contribution_requirements(
            facets, component_order=order, component_edges=edges, limits=_limits(),
        )
        target = [item for item in result.facts if item.id == "acme.app.main"][0]
        self.assertEqual(target.code, "AMBIGUOUS")
        self.assertEqual(len(target.candidates), 2)

    def test_incompatible_exact(self):
        facets = (
            _facet(owner="acme.lib", fid="acme.lib.home", version="1.0.0"),
            _facet(owner="acme.app", fid="acme.app.main", requires=["acme.lib.home ==9.0.0"]),
        )
        order = _order("acme.lib", "acme.app")
        edges = _edges(("acme.app", "acme.lib"))
        result = analyze_contribution_requirements(
            facets, component_order=order, component_edges=edges, limits=_limits(),
        )
        self.assertEqual(_codes(result)[-1], "INCOMPATIBLE")

    def test_semver_prerelease_build_conjunction_operators(self):
        facets = (
            _facet(owner="acme.lib", fid="acme.lib.v", version="1.0.0-beta+b1"),
            _facet(owner="acme.app", fid="acme.app.a", requires=["acme.lib.v >=1.0.0-alpha <2.0.0"]),
            _facet(owner="acme.app", fid="acme.app.b", requires=["acme.lib.v !=9.0.0"]),
            _facet(owner="acme.app", fid="acme.app.c", requires=["acme.lib.v >0.9.0"]),
            _facet(owner="acme.app", fid="acme.app.d", requires=["acme.lib.v <2.0.0"]),
        )
        order = _order("acme.lib", "acme.app")
        edges = _edges(("acme.app", "acme.lib"))
        result = analyze_contribution_requirements(
            facets, component_order=order, component_edges=edges, limits=_limits(),
        )
        self.assertTrue(all(code == "SATISFIED" for code in _codes(result)))


class TestCopiesDeterminism(unittest.TestCase):
    def test_texts_multiplicity_dedup_permutation(self):
        first = _facet(fid="acme.app.a", requires=["acme.app.audit >=1.0.0 <2.0.0", "acme.app.audit >=1.0.0 <2.0.0"])
        audit = _facet(fid="acme.app.audit", entry="frontend/audit")
        facets = (first, audit)
        order = _order("acme.app")
        kwargs = dict(component_order=order, component_edges=_edges(), limits=_limits())
        first_result = analyze_contribution_requirements(facets, **kwargs)
        swapped = analyze_contribution_requirements((audit, first), **kwargs)
        self.assertEqual(first_result.to_dict(), swapped.to_dict())
        self.assertEqual(len(first_result.facts), 2)
        self.assertEqual(first_result.facts[0].requirement, first_result.facts[1].requirement)
        self.assertEqual(first_result.facts[0].index, 0)
        self.assertEqual(first_result.facts[1].index, 1)


class TestIntegrationBuildPlan(unittest.TestCase):
    def test_true_build_plan_module_submodule_fixtures(self):
        from build_frontend_composition import build_plan, BuildLimits

        module_text = (
            'schema_version = "1"\nid = "acme.app"\ntype = "MODULE"\nversion = "1.0.0"\n'
            '[dependencies]\ncomponents = []\n[frontend]\nschema_version = "1"\n'
            '[[frontend.contributions]]\ntype = "ROUTE"\nid = "acme.app.home"\n'
            'entry = "frontend/routes/home"\nversion = "1.0.0"\nrequires = []\nscope = "TENANT_SCOPED"\n'
        )
        submodule_text = (
            'schema_version = "1"\nid = "acme.sub"\ntype = "SUBMODULE"\nversion = "1.0.0"\n'
            '[dependencies]\ncomponents = ["acme.app >=1.0.0"]\n[frontend]\nschema_version = "1"\n'
            '[[frontend.contributions]]\ntype = "PAGE"\nid = "acme.sub.page"\n'
            'entry = "frontend/pages/main"\nversion = "1.0.0"\nrequires = ["acme.app.home >=1.0.0"]\nscope = "TENANT_SCOPED"\n'
        )
        from pixs.kernel.conformity import ConformityAttestation

        def _att(mid):
            return ConformityAttestation(
                component_id=mid, component_version="1.0.0", scope="COMPONENT",
                target_id=mid, target_version="1.0.0", suite_id="acme.suite",
                suite_version="1.0.0", verdict="PASS", proof_ref="proof:acme:" + mid,
            )

        limits = BuildLimits(8, 32768, 262144, ("frontend/tests/component.toml",))
        plan = build_plan(
            (module_text, submodule_text), official_ids=(), required_ids=(),
            configured_providers={}, attestations=(_att("acme.app"), _att("acme.sub")),
            limits=limits,
        )
        payload = plan.to_dict()
        facets = tuple(payload["facets"])
        result = analyze_contribution_requirements(
            facets, component_order=tuple(payload["order"]),
            component_edges=tuple(tuple(edge) for edge in payload["edges"]),
            limits=_limits(),
        )
        self.assertTrue(result.all_satisfied)
        self.assertEqual(result.frontend_edges, (("acme.sub", "acme.sub.page", "acme.app", "acme.app.home"),))


class TestInputErrors(unittest.TestCase):
    def test_dto_cardinality_and_codes(self):
        with self.assertRaises(RequirementsError) as ctx:
            RequirementFact("o", "a.b", 0, "a.b >=1.0.0", "a.b", (), "SATISFIED")
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        with self.assertRaises(RequirementsError) as ctx:
            RequirementFacts((), (("a", "b", "c"),))
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        with self.assertRaises(RequirementsError) as ctx:
            RequirementsLimits(0, 1, 1)
        self.assertEqual(ctx.exception.code, "REQ_LIMITS_INVALID")

    def test_owner_version_inconsistent(self):
        facets = (
            _facet(owner="acme.app", owner_version="1.0.0", fid="acme.app.a"),
            _facet(owner="acme.app", owner_version="2.0.0", fid="acme.app.b"),
        )
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                facets, component_order=_order("acme.app"),
                component_edges=_edges(), limits=_limits(),
            )
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")

    def test_duplicate_owner_id(self):
        facets = (_facet(fid="acme.app.a"), _facet(fid="acme.app.a"))
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                facets, component_order=_order("acme.app"),
                component_edges=_edges(), limits=_limits(),
            )
        self.assertEqual(ctx.exception.code, "REQ_DUPLICATE_CONTRIBUTION")

    def test_invalid_id_version_owner(self):
        for bad in ("single", "a b", ""):
            with self.subTest(bad=bad):
                with self.assertRaises(RequirementsError) as ctx:
                    analyze_contribution_requirements(
                        (_facet(fid=bad),),
                        component_order=_order("acme.app"), component_edges=_edges(),
                        limits=_limits(),
                    )
                self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (_facet(version="^1.0.0"),),
                component_order=_order("acme.app"), component_edges=_edges(),
                limits=_limits(),
            )
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (_facet(owner=""),),
                component_order=_order("acme.app"), component_edges=_edges(),
                limits=_limits(),
            )
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")

    def test_surrogate_rejected(self):
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (_facet(fid="acme.\ud800"),),
                component_order=_order("acme.app"), component_edges=_edges(),
                limits=_limits(),
            )
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")

    def test_hostile_keys_subclasses_no_hooks(self):
        calls: list[str] = []

        class EvilDict(dict):
            def __getitem__(self, key):
                calls.append(str(key))
                return "x"

        evil = EvilDict({
            "owner": "acme.app", "owner_version": "1.0.0", "type": "ROUTE",
            "id": "acme.app.home", "entry": "frontend/routes/home",
            "version": "1.0.0", "requires": [], "scope": "TENANT_SCOPED",
        })
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (evil,), component_order=_order("acme.app"),
                component_edges=_edges(), limits=_limits(),
            )
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        self.assertEqual(calls, [])

        class EvilList(list):
            pass

        bad = _facet()
        bad["requires"] = EvilList()
        with self.assertRaises(RequirementsError):
            analyze_contribution_requirements(
                (bad,), component_order=_order("acme.app"),
                component_edges=_edges(), limits=_limits(),
            )

        class EvilStr(str):
            pass

        with self.assertRaises(RequirementsError):
            analyze_contribution_requirements(
                (_facet(fid=EvilStr("acme.app.home")),),
                component_order=_order("acme.app"), component_edges=_edges(),
                limits=_limits(),
            )

    def test_limits_before_factory(self):
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (_facet(),), component_order=_order("acme.app"),
                component_edges=_edges(), limits=RequirementsLimits(True, 8, 32),
            )
        self.assertEqual(ctx.exception.code, "REQ_LIMITS_INVALID")
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (_facet(), _facet(fid="acme.app.b")),
                component_order=_order("acme.app"), component_edges=_edges(),
                limits=_limits(max_contributions=1),
            )
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        many = _facet(requires=["audit >=1.0.0"] * 3)
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements(
                (many,), component_order=_order("acme.app"),
                component_edges=_edges(),
                limits=_limits(max_requirements_per_contribution=2, max_total_requirements=32),
            )
        self.assertEqual(ctx.exception.code, "REQ_LIMITS_INVALID")


class TestImmutability(unittest.TestCase):
    def test_frozen_and_copies(self):
        result = analyze_contribution_requirements(
            (_facet(requires=["acme.none >=1.0.0"]),), component_order=_order("acme.app"),
            component_edges=_edges(), limits=_limits(),
        )
        with self.assertRaises(FrozenInstanceError):
            result.facts = ()
        with self.assertRaises(FrozenInstanceError):
            result.facts[0].code = "MISSING"
        first = result.to_dict()
        first["facts"].append({"injected": True})
        first["frontend_edges"].append(["x", "y", "z", "w"])
        second = result.to_dict()
        self.assertEqual(len(second["facts"]), 1)
        self.assertEqual(second["frontend_edges"], [])
        self.assertEqual(second["schema"], "pixs.frontend.requirement-facts/1.0.0")

    def test_zero_facts_activates_nothing(self):
        result = analyze_contribution_requirements(
            (), component_order=_order("acme.app"),
            component_edges=_edges(), limits=_limits(),
        )
        self.assertEqual(result.facts, ())
        self.assertEqual(result.frontend_edges, ())
        self.assertTrue(result.all_satisfied)


def _run_cli(payload: bytes, *args: str):
    script = SCRIPTS / "composition_requirements_v1.py"
    env = dict(
        os.environ,
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONPATH=os.pathsep.join([str(SRC), str(SCRIPTS)]),
    )
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        input=payload, capture_output=True, timeout=30, shell=False, env=env,
    )


def _cli_base_args(**over):
    args = {
        "--max-input-bytes": "8192",
        "--max-contributions": "8",
        "--max-requirements-per-contribution": "8",
        "--max-total-requirements": "32",
    }
    args.update(over)
    out: list[str] = []
    for key, value in args.items():
        out.extend([key, str(value)])
    return out


class TestCli(unittest.TestCase):
    def test_cli_missing_exit0_valid(self):
        facet = _facet(requires=["acme.ghost >=1.0.0"])
        payload = json.dumps({
            "facets": [facet],
            "component_order": ["acme.app"],
            "component_edges": [],
        }).encode("utf-8")
        proc = _run_cli(payload, *_cli_base_args())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        body = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(body["schema"], "pixs.frontend.requirement-facts/1.0.0")
        self.assertFalse(body["all_satisfied"])
        self.assertEqual(body["facts"][0]["code"], "MISSING")

    def test_cli_nominal_true_edges(self):
        lib = _facet(owner="acme.lib", fid="acme.lib.home")
        app = _facet(fid="acme.app.main", requires=["acme.lib.home >=1.0.0"])
        payload = json.dumps({
            "facets": [lib, app],
            "component_order": ["acme.lib", "acme.app"],
            "component_edges": [["acme.app", "acme.lib"]],
        }).encode("utf-8")
        proc = _run_cli(payload, *_cli_base_args())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        body = json.loads(proc.stdout.decode("utf-8"))
        self.assertTrue(body["all_satisfied"])
        self.assertEqual(body["frontend_edges"], [["acme.app", "acme.app.main", "acme.lib", "acme.lib.home"]])

    def test_cli_input_refusals(self):
        good = json.dumps({
            "facets": [_facet()], "component_order": ["acme.app"], "component_edges": [],
        }).encode("utf-8")
        proc = _run_cli(b"\xff\xfe", *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")
        proc = _run_cli(b'{"a":1,"a":2}', *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")
        for raw in (b"NaN", b"Infinity"):
            proc = _run_cli(raw, *_cli_base_args())
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")
        proc = _run_cli(b"1e999", *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")
        proc = _run_cli(b'{"facets":1}', *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        proc = _run_cli(b"[" * 40 + b"]" * 40, *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        long_int = b'{"facets": [], "component_order": ["acme.app"], "component_edges": [], "n": ' + b"9" * 6000 + b"}"
        proc = _run_cli(long_int, *_cli_base_args(**{"--max-input-bytes": "16384"}))
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")
        proc = _run_cli(good, *_cli_base_args(**{"--max-input-bytes": "4"}))
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_TOO_LARGE\n")
        proc = _run_cli(good, *["--max-input-bytes", str(sys.maxsize + 1),
                                "--max-contributions", "8",
                                "--max-requirements-per-contribution", "8",
                                "--max-total-requirements", "32"])
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_LIMITS_INVALID\n")
        proc = _run_cli(good, *["--max-input-bytes", "8192"])
        self.assertEqual(proc.returncode, 2)

    def test_cli_sentinel_not_in_stderr(self):
        sentinel = "C11_PRIVATE_SENTINEL_9f8a"
        proc = _run_cli(
            ('{"oops":"' + sentinel + '"').encode("utf-8"), *_cli_base_args(),
        )
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn(sentinel, proc.stderr.decode("utf-8", "replace"))
        self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")


class TestAdditionalInvariants(unittest.TestCase):
    def test_dto_targets_counts_and_nonhashable_code(self):
        candidate = RequirementCandidate("acme.app", "acme.app.target", "1.0.0")
        for code, candidates, target in (
            ([], (), "acme.app.target"),
            ("MISSING", (candidate,), "acme.app.target"),
            ("AMBIGUOUS", (candidate,), "acme.app.target"),
            ("SATISFIED", (candidate,), "acme.app.other"),
        ):
            with self.subTest(code=code):
                with self.assertRaises(RequirementsError):
                    RequirementFact("acme.app", "acme.app.source", 0,
                                    "acme.app.target >=1.0.0", target, candidates, code)
        fact = RequirementFact("acme.app", "acme.app.source", 0,
                               "acme.app.target >=1.0.0", "acme.app.target",
                               (candidate,), "SATISFIED")
        edge = ("acme.app", "acme.app.source", "acme.app", "acme.app.target")
        for edges in ((), (edge, edge), (("acme.app", "wrong", "acme.app", "acme.app.target"),)):
            with self.assertRaises(RequirementsError):
                RequirementFacts((fact,), edges)
        with self.assertRaises(FrozenInstanceError):
            candidate.version = "2.0.0"
        result = RequirementFacts((fact,), (edge,))
        first = result.to_dict()
        first["facts"][0]["candidates"][0]["version"] = "99.0.0"
        self.assertEqual(result.to_dict()["facts"][0]["candidates"][0]["version"], "1.0.0")

    def test_component_order_and_edges_are_validated(self):
        for order in ([], (), ("acme.app", "acme.app"), ("acme.\ud800",)):
            with self.assertRaises(RequirementsError) as ctx:
                analyze_contribution_requirements((), component_order=order,
                                                 component_edges=(), limits=_limits())
            self.assertEqual(ctx.exception.code, "REQ_ORDER_INVALID")
        order = ("acme.lib", "acme.app")
        for edges in ([("acme.app", "acme.lib")],
                      (("acme.lib", "acme.app"),),
                      (("acme.app", "acme.ghost"),),
                      (("acme.app", "acme.lib"), ("acme.app", "acme.lib"))):
            with self.assertRaises(RequirementsError) as ctx:
                analyze_contribution_requirements((), component_order=order,
                                                 component_edges=edges, limits=_limits())
            self.assertEqual(ctx.exception.code, "REQ_EDGES_INVALID")

    def test_release_prerelease_and_build_metadata_use_kernel(self):
        source = _facet(fid="acme.app.source", requires=["acme.app.target >=1.0.0"])
        target = _facet(fid="acme.app.target", version="1.0.0-beta.1")
        result = analyze_contribution_requirements((source, target),
            component_order=("acme.app",), component_edges=(), limits=_limits())
        self.assertEqual(_codes(result), ["INCOMPATIBLE"])
        source["requires"] = ["acme.app.target ==1.0.0+build.1"]
        target["version"] = "1.0.0+build.2"
        result = analyze_contribution_requirements((target, source),
            component_order=("acme.app",), component_edges=(), limits=_limits())
        self.assertEqual(_codes(result), ["SATISFIED"])
        self.assertEqual(result.facts[0].requirement, "acme.app.target ==1.0.0+build.1")
        self.assertEqual(result.facts[0].candidates[0].version, "1.0.0+build.2")

    def test_hostile_key_is_rejected_before_hash_hook(self):
        calls = []
        class Key:
            def __hash__(self):
                calls.append("hash")
                return 193
        facet = _facet()
        facet[Key()] = "x"
        calls.clear()
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements((facet,), component_order=("acme.app",),
                                             component_edges=(), limits=_limits())
        self.assertEqual(ctx.exception.code, "REQ_FACET_INVALID")
        self.assertEqual(calls, [])

    def test_total_limit_and_raw_input_mutation(self):
        a = _facet(fid="acme.app.a", requires=["acme.none"] * 3)
        b = _facet(fid="acme.app.b", requires=["acme.none"] * 3)
        with self.assertRaises(RequirementsError) as ctx:
            analyze_contribution_requirements((a, b), component_order=("acme.app",),
                component_edges=(), limits=_limits(max_total_requirements=5))
        self.assertEqual(ctx.exception.code, "REQ_LIMITS_INVALID")
        result = analyze_contribution_requirements((a,), component_order=("acme.app",),
            component_edges=(), limits=_limits())
        a["requires"].clear()
        a["id"] = "acme.changed"
        self.assertEqual(len(result.facts), 3)
        self.assertEqual(result.facts[0].id, "acme.app.a")


class TestCliAdditional(unittest.TestCase):
    def test_utf8_exact_bytes_surrogate_depth_and_zero_limits(self):
        payload = json.dumps({"facets": [_facet(entry="frontend/routes/é")],
            "component_order": ["acme.app"], "component_edges": []},
            ensure_ascii=False).encode("utf-8")
        proc = _run_cli(payload, *_cli_base_args(**{"--max-input-bytes": len(payload)}))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(json.loads(proc.stdout)["all_satisfied"])
        proc = _run_cli(payload, *_cli_base_args(**{"--max-input-bytes": len(payload) - 1}))
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_TOO_LARGE\n")
        bad = json.dumps({"facets": [_facet(owner="\ud800")],
            "component_order": ["acme.app"], "component_edges": []}).encode("utf-8")
        proc = _run_cli(bad, *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_FACET_INVALID\n")
        proc = _run_cli(b"[" * 2000 + b"]" * 2000, *_cli_base_args())
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stderr, b"REQ_INPUT_INVALID\n")
        for option in ("--max-input-bytes", "--max-contributions",
                       "--max-requirements-per-contribution", "--max-total-requirements"):
            proc = _run_cli(payload, *_cli_base_args(**{option: 0}))
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(proc.stderr, b"REQ_LIMITS_INVALID\n")


if __name__ == "__main__":
    unittest.main()
