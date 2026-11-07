"""Tests de capture C11 : fixtures déterministes, système de fichiers et CLI réels."""
from __future__ import annotations

import base64
import codecs
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from build_frontend_selection import SelectionError, SelectionLimits, capture_selection, verify_before_publish

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "frontend" / "scripts"
ENTRY = "frontend/main.mjs"
JS = b"export const fixture = 1;\n"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def limits(**over):
    values = dict(max_selection_bytes=65536, max_owners=8, max_files_per_owner=8,
                  max_total_files=32, max_bytes_per_file=32768, max_total_bytes=262144)
    values.update(over)
    return SelectionLimits(**values)


def manifest(owner, version="1.0.0", kind="MODULE"):
    return (
        f'schema_version="1"\nid="{owner}"\ntype="{kind}"\nversion="{version}"\n'
        '[frontend]\nschema_version="1"\n[[frontend.contributions]]\ntype="PAGE"\n'
        f'id="{owner}.page"\nentry="{ENTRY}"\nversion="1.0.0"\nrequires=[]\nscope="PUBLIC"\n'
    ).encode("utf-8")


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix=".c11-selection-", dir=ROOT / "frontend" / "tests")
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def owner(self, leaf="one", name="acme.one", kind="MODULE", data=JS):
        folder = self.work / leaf
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "frontend").mkdir(exist_ok=True)
        raw = manifest(name, kind=kind)
        (folder / "component.toml").write_bytes(raw)
        (folder / ENTRY).write_bytes(data)
        return dict(owner=name, owner_version="1.0.0", root=folder.relative_to(ROOT).as_posix(),
                    trust="TRUSTED", manifest=dict(path="component.toml", sha256=sha(raw)),
                    sources=[dict(path=ENTRY, sha256=sha(data))])

    def document(self, owners, **changes):
        body = dict(schema="pixs.frontend.selection/1.0.0", environment="DEVELOPMENT",
                    provenance=dict(kind="LOCAL_OPERATOR_SELECTION", reference="fixture-only:c11"),
                    components=owners,
                    composition=dict(official_ids=[], required_ids=[], configured_providers=None, attestations=[]))
        body.update(changes)
        return body

    def blob(self, body):
        data = json.dumps(body, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return data, sha(data)

    def cap(self, body, bounds=None):
        data, pin = self.blob(body)
        return capture_selection(data, expected_sha256=pin, project_root=ROOT, limits=bounds or limits())

    def refused(self, body, code, bounds=None):
        with self.assertRaises(SelectionError) as caught:
            self.cap(body, bounds)
        self.assertEqual(caught.exception.code, code)

    def cli(self, data, pin, bounds=None, root=ROOT, timeout=10):
        lim = bounds or limits()
        argv = [sys.executable, "-B", str(SCRIPTS / "build_frontend_selection.py"),
                "--expected-sha256", pin, "--project-root", str(root)]
        for name in ("max_selection_bytes", "max_owners", "max_files_per_owner",
                     "max_total_files", "max_bytes_per_file", "max_total_bytes"):
            argv.extend(["--" + name.replace("_", "-"), str(getattr(lim, name))])
        env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "src"), str(SCRIPTS)]),
                   PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run(argv, input=data, capture_output=True, env=env,
                              shell=False, timeout=timeout, cwd=ROOT)

    def test_nominal_bytes_identity_base64(self):
        owner = self.owner()
        capture = self.cap(self.document([owner]))
        self.assertEqual(capture.errors, ())
        self.assertEqual(len(capture.owners), 1)
        item = capture.owners[0]
        self.assertEqual((item.owner, item.owner_version), ("acme.one", "1.0.0"))
        self.assertEqual(item.manifest.data, manifest("acme.one"))
        self.assertEqual(item.sources[0].data, JS)
        self.assertEqual(base64.b64decode(capture.to_dict()["owners"][0]["sources"][0]["data_b64"]), JS)

    def test_pin_precedes_root_access_and_is_external(self):
        body = self.document([self.owner()])
        data, pin = self.blob(body)
        for wrong, code in (("0" * 64, "SELECTION_PIN_MISMATCH"), ("x", "SELECTION_PIN_INVALID")):
            with self.assertRaises(SelectionError) as caught:
                capture_selection(data, expected_sha256=wrong, project_root=self.work / "absent", limits=limits())
            self.assertEqual(caught.exception.code, code)
        with self.assertRaises(TypeError):
            capture_selection(data, project_root=ROOT, limits=limits())
        body["expected_sha256"] = pin
        self.refused(body, "SELECTION_SCHEMA_INVALID")
        with self.assertRaises(SelectionError) as caught:
            capture_selection("invalid", expected_sha256=pin, project_root=ROOT, limits=limits())
        self.assertEqual(caught.exception.code, "SELECTION_BYTES_INVALID")

    def test_json_duplicate_constants_and_depth(self):
        for data in (b'{"schema":1,"schema":2}', b'{"a":NaN}', b'{"a":Infinity}',
                     b"[" * 2000, b"9" * 6000):
            with self.subTest(size=len(data)):
                with self.assertRaises(SelectionError) as caught:
                    capture_selection(data, expected_sha256=sha(data), project_root=ROOT, limits=limits())
                self.assertEqual(caught.exception.code, "SELECTION_JSON_INVALID")
        data = b"[[[]]]"
        with self.assertRaises(SelectionError) as caught:
            capture_selection(data, expected_sha256=sha(data), project_root=ROOT, limits=limits())
        self.assertEqual(caught.exception.code, "SELECTION_SCHEMA_INVALID")

    def test_selection_encoding_bom_and_cr(self):
        good, _ = self.blob(self.document([self.owner()]))
        for data, code in ((b"\xff", "SELECTION_NOT_UTF8"), (codecs.BOM_UTF8 + good, "SELECTION_BOM"),
                           (good + b"\r\n", "SELECTION_BAD_NEWLINE")):
            with self.assertRaises(SelectionError) as caught:
                capture_selection(data, expected_sha256=sha(data), project_root=ROOT, limits=limits())
            self.assertEqual(caught.exception.code, code)

    def test_schema_rejection_precedes_project_root(self):
        body = self.document([self.owner()])
        body["components"][0]["extra"] = "C11_PRIVATE_SENTINEL"
        data, pin = self.blob(body)
        with self.assertRaises(SelectionError) as caught:
            capture_selection(data, expected_sha256=pin, project_root=self.work / "absent", limits=limits())
        self.assertEqual(caught.exception.code, "SELECTION_SCHEMA_INVALID")
        self.assertNotIn("C11_PRIVATE_SENTINEL", str(caught.exception))

    def test_wrong_project_root_is_rejected(self):
        data, pin = self.blob(self.document([self.owner()]))
        result = self.cli(data, pin, root=self.work)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, b"SELECTION_ROOT_INVALID\n")

    def test_providers_null_and_mapping_preserved(self):
        body = self.document([self.owner()])
        self.assertIsNone(self.cap(body).to_dict()["composition"]["configured_providers"])
        body["composition"]["configured_providers"] = {"capability": "acme.one"}
        self.assertEqual(self.cap(body).to_dict()["composition"]["configured_providers"], {"capability": "acme.one"})
        body["composition"]["configured_providers"] = {"capability": None}
        self.refused(body, "SELECTION_SCHEMA_INVALID")

    def test_attestations_exact_fields_immutable_and_not_created(self):
        body = self.document([self.owner()])
        att = dict(component_id="acme.one", component_version="1.0.0", scope="COMPONENT",
                   target_id="acme.one", target_version="1.0.0", suite_id="fixture.c11",
                   suite_version="1.0.0", verdict="FAIL", proof_ref="fixture-only:unqualified")
        body["composition"]["attestations"] = [att]
        capture = self.cap(body)
        self.assertEqual(capture.composition.attestations[0].verdict, "FAIL")
        with self.assertRaises(FrozenInstanceError):
            capture.composition.attestations[0].verdict = "PASS"
        view = capture.to_dict()
        view["composition"]["attestations"][0]["verdict"] = "PASS"
        self.assertEqual(capture.to_dict()["composition"]["attestations"][0]["verdict"], "FAIL")
        for bad in ({**att, "extra": "x"}, {k: v for k, v in att.items() if k != "scope"},
                    {**att, "verdict": True}):
            body["composition"]["attestations"] = [bad]
            self.refused(body, "SELECTION_SCHEMA_INVALID")

    def test_owner_and_version_mismatch(self):
        for field, value in (("owner", "acme.other"), ("owner_version", "2.0.0")):
            body = self.document([self.owner()])
            body["components"][0][field] = value
            capture = self.cap(body)
            self.assertEqual(capture.owners, ())
            self.assertEqual(capture.errors[0].code, "MANIFEST_MISMATCH")
            self.assertEqual((capture.errors[0].owner, capture.errors[0].path), ("", ""))

    def test_entry_exactly_listed_and_manifest_invalid(self):
        owner = self.owner()
        owner["sources"] = []
        capture = self.cap(self.document([owner]))
        self.assertEqual([e.code for e in capture.errors], ["FRONTEND_ENTRY_UNLISTED"])
        raw = b"invalid = [\n"
        (ROOT / owner["root"] / "component.toml").write_bytes(raw)
        owner["manifest"]["sha256"] = sha(raw)
        capture = self.cap(self.document([owner]))
        self.assertEqual([e.code for e in capture.errors], ["MANIFEST_KERNEL_REFUSED"])

    def test_duplicate_owner_root_and_source_paths(self):
        one = self.owner("one", "acme.one")
        two = self.owner("two", "acme.two")
        self.refused(self.document([one, {**two, "owner": "acme.one"}]), "SELECTION_DUPLICATE")
        self.refused(self.document([one, {**two, "root": one["root"]}]), "SELECTION_DUPLICATE")
        one["sources"].append(dict(one["sources"][0]))
        self.refused(self.document([one]), "SELECTION_DUPLICATE")

    def test_nested_module_submodule_and_private_child_claim(self):
        parent = self.owner("parent", "acme.parent")
        child = self.owner("parent/sub", "acme.child", kind="SUBMODULE")
        capture = self.cap(self.document([parent, child]))
        self.assertEqual([x.owner for x in capture.owners], ["acme.parent", "acme.child"])
        self.assertEqual(capture.errors, ())
        private = ROOT / child["root"] / "private.mjs"
        private.write_bytes(JS)
        parent["sources"].append(dict(path="sub/private.mjs", sha256=sha(JS)))
        self.refused(self.document([parent, child]), "SELECTION_OWNER_CONFLICT")

    def test_paths_and_secret_names_refused_before_source_io(self):
        for path in ("../escape.mjs", "/escape.mjs", "a//b.mjs", "a/./b.mjs",
                     ".git/private.mjs", ".cache/private.mjs", ".idea/private.mjs",
                     "openspec/.generated/private.mjs"):
            body = self.document([self.owner()])
            if path.startswith("openspec/"):
                body["components"][0]["root"] = "openspec/.generated/component"
            else:
                body["components"][0]["sources"][0]["path"] = path
            self.refused(body, "SELECTION_PATH_INVALID")
        for path in ("project.env", "foo.env.extra", "id_rsa", "credentials.json", "private.key"):
            body = self.document([self.owner()])
            body["components"][0]["sources"][0]["path"] = path
            self.refused(body, "SELECTION_SECRET_REFUSED")

    def test_manifest_source_and_directory_symlinks_refused(self):
        for kind in ("manifest", "source", "directory"):
            leaf = "link-" + kind
            owner = self.owner(leaf, "acme." + kind)
            target = self.work / (kind + "-outside.mjs")
            if kind == "manifest":
                target.write_bytes(manifest("acme." + kind))
                link = ROOT / owner["root"] / "component.toml"
                link.unlink()
                link.symlink_to(target)
            elif kind == "source":
                target.write_bytes(JS)
                link = ROOT / owner["root"] / ENTRY
                link.unlink()
                link.symlink_to(target)
            else:
                outside = self.work / "outside-dir"
                outside.mkdir()
                (outside / "main.mjs").write_bytes(JS)
                folder = ROOT / owner["root"] / "frontend"
                (folder / "main.mjs").unlink()
                folder.rmdir()
                folder.symlink_to(outside, target_is_directory=True)
            capture = self.cap(self.document([owner]))
            self.assertEqual(capture.owners, ())
            self.assertEqual([e.code for e in capture.errors], ["SOURCE_UNAVAILABLE"])

    def test_missing_or_directory_source_isolated_with_independent_owner(self):
        for kind in ("missing", "directory"):
            one = self.owner("bad-" + kind, "acme.bad")
            two = self.owner("good-" + kind, "acme.good")
            path = ROOT / one["root"] / ENTRY
            path.unlink()
            if kind == "directory":
                path.mkdir()
            capture = self.cap(self.document([one, two]))
            self.assertEqual([o.index for o in capture.owners], [1])
            self.assertEqual([e.owner_index for e in capture.errors], [0])
            self.assertEqual(capture.errors[0].code, "SOURCE_UNAVAILABLE" if kind == "missing" else "NOT_REGULAR")

    def test_fifo_cli_nonblocking(self):
        owner = self.owner()
        path = ROOT / owner["root"] / ENTRY
        path.unlink()
        os.mkfifo(path)
        data, pin = self.blob(self.document([owner]))
        result = self.cli(data, pin, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([e["code"] for e in json.loads(result.stdout)["errors"]], ["FIFO_REFUSED"])

    def test_source_encoding_errors_preserve_snapshot_rules(self):
        for number, (raw, code) in enumerate(((b"\xff", "UTF8_INVALID"), (codecs.BOM_UTF8 + JS, "BOM_REFUSED"),
                                            (JS.replace(b"\n", b"\r\n"), "CRLF_REFUSED"))):
            owner = self.owner("badtext-" + str(number), "acme.text", data=raw)
            capture = self.cap(self.document([owner]))
            self.assertEqual([e.code for e in capture.errors], [code])
            self.assertEqual(capture.errors[0].observed_sha256, sha(raw))
        owner = self.owner("unicode", "acme.unicode", data='export const title = "é";\n'.encode())
        self.assertEqual(self.cap(self.document([owner])).owners[0].sources[0].data, 'export const title = "é";\n'.encode())

    def test_hash_drift_manifest_and_source(self):
        for kind in ("manifest", "source"):
            owner = self.owner("drift-" + kind, "acme.drift")
            raw = b"changed\n"
            path = ROOT / owner["root"] / ("component.toml" if kind == "manifest" else ENTRY)
            path.write_bytes(raw)
            capture = self.cap(self.document([owner]))
            self.assertEqual(capture.errors[0].code, "MANIFEST_MISMATCH" if kind == "manifest" else "HASH_DRIFT")
            self.assertEqual(capture.errors[0].observed_sha256, sha(raw))

    def test_limits_types_counts_and_selection_bytes(self):
        for over in ({"max_owners": True}, {"max_owners": 0}, {"max_selection_bytes": sys.maxsize}):
            with self.assertRaises(SelectionError) as caught:
                limits(**over)
            self.assertEqual(caught.exception.code, "SELECTION_LIMITS_INVALID")
        body = self.document([self.owner()])
        for over in ({"max_files_per_owner": 1}, {"max_total_files": 1}):
            self.refused(body, "SELECTION_LIMITS_INVALID", limits(**over))
        two = self.owner("two", "acme.two")
        self.refused(self.document(body["components"] + [two]), "SELECTION_SCHEMA_INVALID", limits(max_owners=1))
        raw, pin = self.blob(body)
        with self.assertRaises(SelectionError) as caught:
            capture_selection(raw, expected_sha256=pin, project_root=ROOT,
                              limits=limits(max_selection_bytes=len(raw) - 1))
        self.assertEqual(caught.exception.code, "SELECTION_TOO_LARGE")

    def test_file_and_global_byte_limits_diagnose_every_owner(self):
        one = self.owner("one", "acme.one")
        two = self.owner("two", "acme.two")
        three = self.owner("three", "acme.three")
        capture = self.cap(self.document([one, two, three]), limits(max_total_bytes=8))
        self.assertEqual(capture.owners, ())
        self.assertEqual([e.owner_index for e in capture.errors], [0, 1, 2])
        self.assertEqual([e.code for e in capture.errors], ["QUOTA_EXCEEDED"] * 3)
        capture = self.cap(self.document([one]), limits(max_bytes_per_file=8))
        self.assertEqual(capture.errors[0].code, "QUOTA_EXCEEDED")

    def test_failed_hash_read_is_not_refunded(self):
        one = self.owner("one", "acme.one")
        two = self.owner("two", "acme.two")
        one["sources"][0]["sha256"] = "0" * 64
        spent = len(manifest("acme.one")) + len(JS)
        capture = self.cap(self.document([one, two]), limits(max_total_bytes=spent + 4))
        self.assertEqual([e.code for e in capture.errors], ["HASH_DRIFT", "QUOTA_EXCEEDED"])
        self.assertEqual(capture.owners, ())

    def test_fd_counts_after_success_and_failures(self):
        owner = self.owner()
        body = self.document([owner])
        self.cap(body)
        before = len(os.listdir("/proc/self/fd"))
        for _ in range(3):
            self.cap(body)
        owner["sources"][0]["sha256"] = "0" * 64
        for _ in range(3):
            self.cap(body)
        self.assertEqual(len(os.listdir("/proc/self/fd")), before)

    def test_deep_immutability_and_copies(self):
        capture = self.cap(self.document([self.owner()]))
        with self.assertRaises(FrozenInstanceError):
            capture.environment = "PRODUCTION"
        with self.assertRaises(FrozenInstanceError):
            capture.owners[0].sources[0].data = b"altered"
        view = capture.to_dict()
        view["owners"][0]["sources"][0]["data_b64"] = ""
        view["composition"]["official_ids"].append("invented")
        self.assertEqual(capture.owners[0].sources[0].data, JS)
        self.assertEqual(capture.to_dict()["composition"]["official_ids"], [])

    def test_recheck_valid_returns_original(self):
        data, pin = self.blob(self.document([self.owner()]))
        bound = limits()
        capture = capture_selection(data, expected_sha256=pin, project_root=ROOT, limits=bound)
        self.assertIs(verify_before_publish(capture, selection_bytes=data, expected_sha256=pin,
                                           project_root=ROOT, limits=bound), capture)

    def test_recheck_source_policy_and_limits_drift(self):
        body = self.document([self.owner()])
        data, pin = self.blob(body)
        capture = self.cap(body)
        path = ROOT / body["components"][0]["root"] / ENTRY
        path.write_bytes(JS + b"// changed\n")
        with self.assertRaises(SelectionError) as caught:
            verify_before_publish(capture, selection_bytes=data, expected_sha256=pin,
                                  project_root=ROOT, limits=limits())
        self.assertEqual(caught.exception.code, "SELECTION_DRIFT")
        self.assertEqual(capture.owners[0].sources[0].data, JS)
        path.write_bytes(JS)
        changed = dict(body, provenance=dict(kind="LOCAL_OPERATOR_SELECTION", reference="new-choice"))
        new_data, new_pin = self.blob(changed)
        for raw, digest, bound in ((new_data, new_pin, limits()),
                                   (data, pin, limits(max_total_bytes=262145))):
            with self.assertRaises(SelectionError) as caught:
                verify_before_publish(capture, selection_bytes=raw, expected_sha256=digest,
                                      project_root=ROOT, limits=bound)
            self.assertEqual(caught.exception.code, "SELECTION_DRIFT")

    def test_recheck_owner_reappears(self):
        owner = self.owner()
        path = ROOT / owner["root"] / ENTRY
        path.unlink()
        body = self.document([owner])
        data, pin = self.blob(body)
        capture = self.cap(body)
        self.assertEqual(capture.errors[0].code, "SOURCE_UNAVAILABLE")
        path.write_bytes(JS)
        with self.assertRaises(SelectionError) as caught:
            verify_before_publish(capture, selection_bytes=data, expected_sha256=pin,
                                  project_root=ROOT, limits=limits())
        self.assertEqual(caught.exception.code, "SELECTION_DRIFT")

    def test_cli_nominal_partial_and_pin_failure(self):
        owner = self.owner()
        raw, pin = self.blob(self.document([owner]))
        result = self.cli(raw, pin)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(base64.b64decode(json.loads(result.stdout)["owners"][0]["sources"][0]["data_b64"]), JS)
        (ROOT / owner["root"] / ENTRY).unlink()
        result = self.cli(raw, pin)
        self.assertEqual(result.returncode, 0, result.stderr)
        body = json.loads(result.stdout)
        self.assertEqual([e["code"] for e in body["errors"]], ["SOURCE_UNAVAILABLE"])
        self.assertNotIn("ready", body)
        self.assertNotIn("active", body)
        result = self.cli(raw, "0" * 64)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, b"SELECTION_PIN_MISMATCH\n")


if __name__ == "__main__":
    unittest.main()
