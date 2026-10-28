"""Suite TEST stockage prive PlanningBundle, source seule non executee."""
from __future__ import annotations

import dataclasses
import fcntl
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import c08_e5_fixtures
from pixs.backend.installation import marker as _io
from pixs.backend.installation.planning_bundle import (
    PlanningBundleError,
    dump_planning_bundle,
    planning_bundle_binding,
    planning_bundle_sha256,
)
from pixs.backend.installation.planning_bundle_store import (
    PlanningBundleStoreBusy,
    PlanningBundleStoreConflict,
    PlanningBundleStoreConfig,
    PlanningBundleStoreIssueUnknown,
    PlanningBundleStoreRefused,
    PlanningBundleStoreUnknown,
    initialize_bundle_guard,
    publish_bundle,
    read_bundle,
)

import pixs.backend.installation.planning_bundle_store as _store


def _write_exact(path: Path, data: bytes) -> None:
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    try:
        off = 0
        while off < len(data):
            n = os.write(fd, data[off:])
            if n == 0:
                raise OSError("write nul")
            off += n
        os.fsync(fd)
    finally:
        os.close(fd)
    if path.stat().st_size != len(data):
        raise OSError("taille inexacte")


class BundleStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        base = Path(__file__).resolve().parent
        tmp = tempfile.TemporaryDirectory(prefix="TEST-bundle-store-", dir=str(base))
        self._tmp = tmp
        self.addCleanup(tmp.cleanup)
        os.chmod(tmp.name, 0o700)
        self.tmp = Path(tmp.name)
        self.euid = os.geteuid()
        self.egid = os.getegid()
        ids: set[tuple[int, int]] = set()
        cur = Path(tmp.name).resolve()
        while True:
            st = cur.stat()
            ids.add((st.st_uid, st.st_gid))
            if str(cur) == "/":
                break
            cur = cur.parent
        ids.add((self.euid, self.egid))
        self.parent_ids = tuple(sorted(ids))
        limits = c08_e5_fixtures.make_limits().bundle_limits
        self.limits = limits
        self.doc_name = "bundle-test.dat"
        self.lock_name = "guard-test.lock"
        self.doc_path = str(self.tmp / self.doc_name)
        self.io = _io.MarkerConfig(
            path=self.doc_path,
            owner_uid=self.euid,
            owner_gid=self.egid,
            max_bytes=limits.max_bundle_bytes + 8192,
            max_ref_len=c08_e5_fixtures.TEST_MAX_REF,
            allowed_format_versions=("1.0.0",),
            parent_identities=self.parent_ids,
        )
        self.config = PlanningBundleStoreConfig(
            io=self.io,
            lock_basename=self.lock_name,
            bundle_limits=limits,
        )

    def test_config_rejette_types_et_locks(self) -> None:
        with self.assertRaises(PlanningBundleStoreRefused):
            PlanningBundleStoreConfig(
                io="x",  # type: ignore[arg-type]
                lock_basename=self.lock_name,
                bundle_limits=self.limits,
            )
        for bad in ("", ".", "..", "a/b", "x\x00y"):
            with self.assertRaises(PlanningBundleStoreRefused):
                PlanningBundleStoreConfig(
                    io=self.io, lock_basename=bad, bundle_limits=self.limits
                )
        bad = "x" * (self.io.max_ref_len + 1)
        with self.assertRaises(PlanningBundleStoreRefused):
            PlanningBundleStoreConfig(
                io=self.io, lock_basename=bad, bundle_limits=self.limits
            )
        with self.assertRaises(PlanningBundleStoreRefused):
            PlanningBundleStoreConfig(
                io=self.io,
                lock_basename=os.path.basename(self.io.path),
                bundle_limits=self.limits,
            )
        small = dataclasses.replace(self.io, max_bytes=1)
        with self.assertRaises(PlanningBundleStoreRefused):
            PlanningBundleStoreConfig(
                io=small, lock_basename=self.lock_name, bundle_limits=self.limits
            )
        badv = dataclasses.replace(self.io, allowed_format_versions=("9.9.9",))
        with self.assertRaises(PlanningBundleStoreRefused):
            PlanningBundleStoreConfig(
                io=badv, lock_basename=self.lock_name, bundle_limits=self.limits
            )

    def test_init_garde_seule_idempotente_inode(self) -> None:
        initialize_bundle_guard(self.config)
        g1 = (self.tmp / self.lock_name).stat()
        self.assertFalse((self.tmp / self.doc_name).exists())
        initialize_bundle_guard(self.config)
        g2 = (self.tmp / self.lock_name).stat()
        self.assertEqual((g1.st_dev, g1.st_ino), (g2.st_dev, g2.st_ino))
        self.assertFalse((self.tmp / self.doc_name).exists())

    def test_garde_absente_sans_init(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-noinit-01")
        raw = dump_planning_bundle(g.bundle, self.limits)
        self.assertTrue(raw)
        with self.assertRaises(PlanningBundleStoreUnknown):
            read_bundle(self.config)
        with self.assertRaises(PlanningBundleStoreUnknown):
            publish_bundle(self.config, g.bundle)
        self.assertFalse((self.tmp / self.doc_name).exists())

    def test_garde_chmod_0644_sans_repair(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-chmod-01")
        raw = dump_planning_bundle(g.bundle, self.limits)
        self.assertTrue(raw)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        os.chmod(str(self.tmp / self.lock_name), 0o644)
        with self.assertRaises(PlanningBundleStoreRefused):
            read_bundle(self.config)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)
        self.assertEqual(stat.S_IMODE((self.tmp / self.lock_name).stat().st_mode), 0o644)

    def test_garde_corrompue(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-gcorr-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        _write_exact(self.tmp / self.lock_name, b"corrupt")
        self.assertEqual((self.tmp / self.lock_name).stat().st_size, len(b"corrupt"))
        with self.assertRaises(PlanningBundleStoreRefused):
            read_bundle(self.config)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)

    def test_garde_symlink_fermee_sans_troncature(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-gsym-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        guard = self.tmp / self.lock_name
        real = self.tmp / "real-guard.dat"
        os.rename(str(guard), str(real))
        try:
            os.symlink("real-guard.dat", str(guard))
            with self.assertRaises(PlanningBundleStoreRefused):
                read_bundle(self.config)
        finally:
            os.unlink(str(guard))
            os.rename(str(real), str(guard))
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)

    def test_read_absent(self) -> None:
        initialize_bundle_guard(self.config)
        with self.assertRaises(PlanningBundleStoreUnknown) as ctx:
            read_bundle(self.config)
        self.assertEqual(ctx.exception.code, "C08_BUNDLE_STORE_UNKNOWN")

    def test_publish_read_durable(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-pub-01")
        raw = dump_planning_bundle(g.bundle, self.limits)
        self.assertTrue(raw)
        initialize_bundle_guard(self.config)
        digest = publish_bundle(self.config, g.bundle)
        self.assertEqual(digest, planning_bundle_sha256(g.bundle, self.limits))
        back = read_bundle(self.config)
        self.assertEqual(dump_planning_bundle(back, self.limits), raw)
        bind = planning_bundle_binding(back, self.limits)
        self.assertEqual(bind.ref, back.bundle_ref)
        self.assertEqual(bind.version, "1.0.0")
        self.assertEqual(back.plan_document.plan_version, g.bundle.plan_document.plan_version)
        self.assertEqual(back.projection_document.correlation_ids, g.bundle.projection_document.correlation_ids)
        self.assertEqual(back.projection_document.causation_ids, g.bundle.projection_document.causation_ids)

    def test_identique_idempotent_et_publish_unique(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-idem-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        real = _io._publish
        calls: list[int] = []
        def counting(parent: int, name: str, payload: bytes, cfg) -> None:
            calls.append(1)
            return real(parent, name, payload, cfg)
        with mock.patch.object(_io, "_publish", side_effect=counting):
            publish_bundle(self.config, g.bundle)
            self.assertEqual(len(calls), 1)
            st1 = (self.tmp / self.doc_name).stat()
            publish_bundle(self.config, g.bundle)
            self.assertEqual(len(calls), 1)
            st2 = (self.tmp / self.doc_name).stat()
        self.assertEqual((st1.st_dev, st1.st_ino), (st2.st_dev, st2.st_ino))

    def test_divergent_valide_conflit(self) -> None:
        a = c08_e5_fixtures.make_reuse_graph("store-div-a02")
        b = c08_e5_fixtures.make_reuse_graph("store-div-b02")
        ra = dump_planning_bundle(a.bundle, self.limits)
        rb = dump_planning_bundle(b.bundle, self.limits)
        self.assertTrue(ra)
        self.assertTrue(rb)
        self.assertNotEqual(ra, rb)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, a.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        with self.assertRaises(PlanningBundleStoreConflict) as ctx:
            publish_bundle(self.config, b.bundle)
        self.assertEqual(ctx.exception.code, "C08_BUNDLE_STORE_CONFLICT")
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)

    def test_document_symlink(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-sym-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        os.rename(str(self.tmp / self.doc_name), str(self.tmp / "real.dat"))
        os.symlink("real.dat", str(self.tmp / self.doc_name))
        try:
            with self.assertRaises(PlanningBundleStoreRefused):
                read_bundle(self.config)
        finally:
            os.unlink(str(self.tmp / self.doc_name))
            os.rename(str(self.tmp / "real.dat"), str(self.tmp / self.doc_name))
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)

    def test_document_droits(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-right-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        os.chmod(str(self.tmp / self.doc_name), 0o644)
        try:
            with self.assertRaises(PlanningBundleStoreRefused):
                read_bundle(self.config)
        finally:
            os.chmod(str(self.tmp / self.doc_name), 0o600)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)

    def test_document_hardlink(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-hard-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        os.link(str(self.tmp / self.doc_name), str(self.tmp / "hard2.dat"))
        try:
            with self.assertRaises(PlanningBundleStoreRefused):
                read_bundle(self.config)
        finally:
            os.unlink(str(self.tmp / "hard2.dat"))
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)

    def test_oversize_borne_max_plus_un(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-over-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        limit = self.limits.max_bundle_bytes
        data = b"X" * (limit + 1)
        _write_exact(self.tmp / self.doc_name, data)
        real_read = os.read
        total = 0
        count = 0
        requested: list[int] = []
        def counting(fd: int, n: int) -> bytes:
            nonlocal total, count
            requested.append(n)
            out = real_read(fd, n)
            count += 1
            total += len(out)
            return out
        with mock.patch("os.read", side_effect=counting):
            with self.assertRaises(PlanningBundleStoreRefused):
                read_bundle(self.config)
        self.assertEqual(total, limit + 1)
        self.assertGreater(count, 0)
        self.assertEqual(len(requested), count)
        for req in requested:
            self.assertLessEqual(req, limit + 1)

    def test_vrai_flock_bloque(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-flock-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        fd = os.open(str(self.tmp / self.lock_name), os.O_RDONLY | os.O_NOFOLLOW)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(PlanningBundleStoreBusy):
                read_bundle(self.config)
            with self.assertRaises(PlanningBundleStoreBusy):
                publish_bundle(self.config, g.bundle)
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    def test_codes_et_causes(self) -> None:
        with self.assertRaises(PlanningBundleStoreRefused) as ctx:
            PlanningBundleStoreConfig(io=self.io, lock_basename="", bundle_limits=self.limits)
        self.assertEqual(ctx.exception.code, "C08_BUNDLE_STORE_REFUSED")
        self.assertNotIn(self.doc_path, str(ctx.exception))
        g = c08_e5_fixtures.make_reuse_graph("store-cause-02")
        initialize_bundle_guard(self.config)
        with mock.patch.object(_store, "dump_planning_bundle", side_effect=PlanningBundleError()):
            with self.assertRaises(PlanningBundleStoreRefused) as ctx2:
                publish_bundle(self.config, g.bundle)
            self.assertIsInstance(ctx2.exception.__cause__, PlanningBundleError)

    def test_regression_hierarchie_publish_atteint(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-hier-01")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        with mock.patch.object(_io, "_publish", side_effect=_io.MarkerIssueUnknown()) as m:
            with self.assertRaises(PlanningBundleStoreIssueUnknown) as ctx:
                publish_bundle(self.config, g.bundle)
            self.assertEqual(m.call_count, 1)
            self.assertIsInstance(ctx.exception.__cause__, _io.MarkerIssueUnknown)
            self.assertEqual(ctx.exception.code, "C08_BUNDLE_STORE_ISSUE_UNKNOWN")

    def test_perte_apres_vrai_publish(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-loss-02")
        expected = dump_planning_bundle(g.bundle, self.limits)
        self.assertTrue(expected)
        initialize_bundle_guard(self.config)
        real = _io._publish
        calls: list[int] = []
        def flaky(parent: int, name: str, payload: bytes, cfg) -> None:
            calls.append(1)
            real(parent, name, payload, cfg)
            raise _io.MarkerIssueUnknown()
        with mock.patch.object(_io, "_publish", side_effect=flaky):
            with self.assertRaises(PlanningBundleStoreIssueUnknown):
                publish_bundle(self.config, g.bundle)
            self.assertEqual(len(calls), 1)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), expected)
        back = read_bundle(self.config)
        self.assertEqual(dump_planning_bundle(back, self.limits), expected)
        self.assertEqual(len(calls), 1)

    def test_verification_durable_apres_publish(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-dur-02")
        expected = dump_planning_bundle(g.bundle, self.limits)
        self.assertTrue(expected)
        initialize_bundle_guard(self.config)
        real_read = _store._read_raw
        def flaky(parent: int, name: str, config, *, durable: bool):
            if not durable:
                return real_read(parent, name, config, durable=durable)
            raise OSError("durable-test")
        with mock.patch.object(_store, "_read_raw", side_effect=flaky):
            with self.assertRaises(PlanningBundleStoreIssueUnknown):
                publish_bundle(self.config, g.bundle)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), expected)

    def test_garde_postpublication_invalide(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-gpost-01")
        expected = dump_planning_bundle(g.bundle, self.limits)
        self.assertTrue(expected)
        initialize_bundle_guard(self.config)
        self.assertFalse((self.tmp / self.doc_name).exists())
        real_same = _io._same_parent
        def flaky(cfg, directory: int):
            real_same(cfg, directory)
            if (self.tmp / self.doc_name).exists():
                raise _io.MarkerInvalid()
        with mock.patch.object(_io, "_same_parent", side_effect=flaky):
            with self.assertRaises(PlanningBundleStoreIssueUnknown) as ctx:
                publish_bundle(self.config, g.bundle)
            self.assertIsInstance(ctx.exception.__cause__, _io.MarkerInvalid)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), expected)
        back = read_bundle(self.config)
        self.assertEqual(dump_planning_bundle(back, self.limits), expected)

    def test_inattendue_parse_apres_publish_reel(self) -> None:
        g = c08_e5_fixtures.make_reuse_graph("store-unexp-02")
        dump_planning_bundle(g.bundle, self.limits)
        initialize_bundle_guard(self.config)
        publish_bundle(self.config, g.bundle)
        before = (self.tmp / self.doc_name).read_bytes()
        with mock.patch.object(_store, "parse_planning_bundle", side_effect=RuntimeError("panne-inattendue")) as m:
            with self.assertRaises(RuntimeError):
                read_bundle(self.config)
            self.assertEqual(m.call_count, 1)
        self.assertEqual((self.tmp / self.doc_name).read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
