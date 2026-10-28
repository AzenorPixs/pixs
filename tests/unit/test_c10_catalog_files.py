"""Catalogue initial : filesystem réel ; aucune qualification du publisher ou de PG."""
from __future__ import annotations

import datetime as dt
import fcntl
import hashlib
import os
import tempfile
import threading
import unittest
from dataclasses import replace
from pathlib import Path

from pixs.backend.c10_catalog import (
    C10Catalog, CatalogConfig, ProfileBinding, CatalogInvalid, CatalogUnknown,
    CatalogBusy, CatalogRevoked)

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "tests" / "c10-catalog"
NOW = dt.datetime(2026, 10, 23, 8, tzinfo=dt.timezone.utc)
HEADER = """[catalog]
schema_version = "1.0.0"
catalog_version = "catalog:1"
publication_ref = "publication:1"
valid_from = 2026-10-23T07:00:00Z
valid_until = 2026-10-24T07:00:00Z
published_at = 2026-10-23T07:30:00Z
revoked = false
"""
PROFILE = """
[profiles.core]
published_version = "1.0.0"
resource_refs = ["pixs.core.bootstrap:installation"]
revoked = false
[profiles.core.profile]
profile_version = "1.0.0"
data_asset_id = "asset:core"
owner_component = "pixs.core"
source_of_truth = "declaration:core"
data_classes = ["identity"]
confidentiality = "RESTRICTED"
personal_data = "PERSONAL"
purpose_refs = ["initialization"]
retention_policy = "retention:qualification-only"
deletion_policy = "deletion:qualification-only"
residency_constraints = ["qualification"]
authorized_consumers = ["pixs.core"]
processor_refs = []
export_policy = "export:qualification-only"
lineage = "lineage:qualification-only"
"""


class CatalogCases(unittest.TestCase):
    def setUp(self):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=OUTPUT, prefix="case-")
        self.addCleanup(temporary.cleanup)
        self.parent = Path(temporary.name)
        os.chown(self.parent, -1, os.getegid())
        os.chmod(self.parent, 0o700)
        self.path = self.parent / "catalog.toml"
        self.guard = self.parent / "catalog.guard"
        self.guard.write_bytes(b"")
        os.chmod(self.guard, 0o600)
        self.body = HEADER + PROFILE
        self.write(self.body)
        identities = tuple(dict.fromkeys(
            (p.stat().st_uid, p.stat().st_gid)
            for p in [*reversed(self.parent.parents), self.parent]))
        self.config = CatalogConfig(
            str(self.path), str(self.guard), os.geteuid(), os.getegid(), identities,
            8192, 128, 8, 8, 90000, 3600, 0, 1,
            "catalog:1", "publication:1", self.digest(),
            ProfileBinding("core", "asset:core", "pixs.core", "declaration:core", "1.0.0"))

    def write(self, text):
        self.path.write_bytes(text.encode("utf-8"))
        os.chmod(self.path, 0o600)

    def digest(self):
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    def catalog(self, config=None, now=NOW):
        return C10Catalog(self.config if config is None else config, now=lambda: now)

    def load(self, config=None, now=NOW):
        with self.catalog(config, now).guard() as lease:
            return lease.profile()

    def repin(self, text):
        self.write(text)
        return replace(self.config, expected_sha256=self.digest())

    def test_reads_bound_profile_from_actual_file(self):
        entry = self.load()
        self.assertEqual(entry.profile.owner_component, "pixs.core")
        self.assertEqual(entry.published_version, "1.0.0")
        self.assertEqual(entry.resource_refs, ("pixs.core.bootstrap:installation",))
        self.assertEqual(entry.raw_sha256, self.digest())
        self.assertEqual(entry.profile.processor_refs, frozenset())

    def test_multiple_shared_readers_and_exclusive_publisher_conflict(self):
        with self.catalog().guard(), self.catalog().guard():
            with self.guard.open("rb") as handle:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        with self.guard.open("rb") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(CatalogBusy):
                self.load()
        self.load()

    def test_one_lease_per_service_and_no_use_after_release(self):
        service = self.catalog()
        with service.guard() as lease:
            lease.profile()
            with self.assertRaises(CatalogBusy):
                with service.guard():
                    self.fail("garde imbriquée admise")
        with self.assertRaises(CatalogInvalid):
            lease.profile()

    def test_other_thread_cannot_use_live_lease(self):
        errors = []
        with self.catalog().guard() as lease:
            def attempt():
                try:
                    lease.profile()
                except CatalogInvalid:
                    errors.append("refused")
            worker = threading.Thread(target=attempt)
            worker.start()
            worker.join(timeout=5)
            self.assertFalse(worker.is_alive())
        self.assertEqual(errors, ["refused"])

    def test_publication_and_profile_binding_must_match(self):
        for change in ({"expected_catalog_version": "different"},
                       {"expected_publication_ref": "different"},
                       {"expected_sha256": "f" * 64},
                       {"binding": replace(self.config.binding, data_asset_id="other")},
                       {"binding": replace(self.config.binding, owner_component="other")},
                       {"binding": replace(self.config.binding, source_of_truth="other")},
                       {"binding": replace(self.config.binding, profile_version="2.0.0")}):
            with self.subTest(change=list(change)):
                with self.assertRaises(CatalogInvalid):
                    self.load(replace(self.config, **change))

    def test_revocation_and_missing_profile(self):
        for text in (self.body.replace("revoked = false", "revoked = true", 1),
                     self.body.replace("[profiles.core]", "[profiles.other]").replace(
                         "[profiles.core.profile]", "[profiles.other.profile]")):
            config = self.repin(text)
            with self.assertRaises(CatalogInvalid):
                self.load(config)
        config = self.repin(self.body.replace(
            'resource_refs = ["pixs.core.bootstrap:installation"]\nrevoked = false',
            'resource_refs = ["pixs.core.bootstrap:installation"]\nrevoked = true'))
        with self.assertRaises(CatalogRevoked):
            self.load(config)

    def test_expiration_future_and_stale_publication(self):
        for now in (NOW - dt.timedelta(hours=2), NOW + dt.timedelta(days=1),
                    NOW + dt.timedelta(hours=2), NOW.replace(tzinfo=None)):
            with self.subTest(now=now):
                with self.assertRaises(CatalogInvalid):
                    self.load(now=now)
        config = self.repin(self.body.replace("07:00:00Z", "07:00:00+01:00"))
        with self.assertRaises(CatalogInvalid):
            self.load(config)

    def test_closed_toml_schema_and_strict_types(self):
        candidates = [
            self.body + "unknown = 1\n",
            self.body.replace('catalog_version = "catalog:1"',
                              'catalog_version = "catalog:1"\ncatalog_version = "duplicate"'),
            self.body.replace('profile_version = "1.0.0"', 'profile_version = "invalid"'),
            self.body.replace('data_classes = ["identity"]', 'data_classes = [true]'),
            self.body.replace('data_classes = ["identity"]', 'data_classes = ["identity","identity"]'),
            self.body.replace('personal_data = "PERSONAL"', 'personal_data = nan'),
            self.body.replace('confidentiality = "RESTRICTED"', 'confidentiality = "invalid"'),
            self.body.replace('revoked = false', 'revoked = 0'),
            self.body.replace('published_version = "1.0.0"', 'published_version = "2.0.0"')]
        for text in candidates:
            with self.subTest(text_size=len(text)):
                config = self.repin(text)
                with self.assertRaises(CatalogInvalid):
                    self.load(config)

    def test_strict_configuration_and_bounds(self):
        for change in ({"max_bytes": True}, {"max_refs": 0}, {"owner_uid": False},
                       {"lock_timeout_ms": -1}, {"parent_identities": ()},
                       {"expected_sha256": "not-a-digest"}, {"catalog_path": "relative"},
                       {"guard_path": str(self.path)}):
            with self.subTest(change=list(change)):
                with self.assertRaises(CatalogInvalid):
                    replace(self.config, **change)
        for change in ({"max_bytes": 64}, {"max_ref_len": 12}, {"max_ttl_seconds": 1}):
            with self.subTest(change=list(change)):
                with self.assertRaises(CatalogInvalid):
                    self.load(replace(self.config, **change))

    def test_source_permissions_symlink_hardlink_and_fifo(self):
        os.chmod(self.path, 0o640)
        with self.assertRaises(CatalogInvalid):
            self.load()
        os.chmod(self.path, 0o600)
        other = self.parent / "other"
        os.link(self.path, other)
        with self.assertRaises(CatalogInvalid):
            self.load()
        other.unlink()
        self.path.unlink()
        self.path.symlink_to(self.guard)
        with self.assertRaises(CatalogInvalid):
            self.load()
        self.path.unlink()
        os.mkfifo(self.path, 0o600)
        with self.assertRaises(CatalogInvalid):
            self.load()

    def test_missing_catalog_and_guard_are_not_repaired(self):
        self.path.unlink()
        with self.assertRaises(CatalogUnknown):
            self.load()
        self.write(self.body)
        self.guard.unlink()
        with self.assertRaises(CatalogUnknown):
            self.load()
        self.assertFalse(self.guard.exists())

    def test_guard_replacement_and_source_substitution_fail_closed(self):
        with self.catalog().guard() as lease:
            lease.profile()
            replacement = self.parent / "replacement"
            replacement.write_bytes(b"")
            os.chmod(replacement, 0o600)
            os.replace(replacement, self.guard)
            with self.assertRaises(CatalogInvalid):
                lease.profile()
        with self.catalog().guard() as lease:
            self.write(self.body.replace("publication:1", "publication:other"))
            with self.assertRaises(CatalogInvalid):
                lease.profile()

    def test_private_parent_and_parent_symlink(self):
        os.chmod(self.parent, 0o750)
        with self.assertRaises(CatalogInvalid):
            self.load()
        os.chmod(self.parent, 0o700)
        alias = self.parent / "alias"
        alias.symlink_to(self.parent, target_is_directory=True)
        config = replace(self.config, catalog_path=str(alias / self.path.name),
                         guard_path=str(alias / self.guard.name))
        with self.assertRaises(CatalogInvalid):
            self.load(config)

    def test_errors_hide_raw_document(self):
        self.write("private-value-invalid")
        with self.assertRaises(CatalogInvalid) as raised:
            self.load()
        self.assertNotIn("private-value-invalid", str(raised.exception))
        self.assertNotIn(str(self.path), str(raised.exception))


if __name__ == "__main__":
    unittest.main()
