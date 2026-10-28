"""Unites offline C09 2.2 : publics stricts et orchestration worker sans SQL."""
from __future__ import annotations

import datetime
import threading
import unittest
from zoneinfo import ZoneInfo

from pixs.backend.c09_authorization_adapter import (
    C09Identity,
    C09Refused,
    c09_text,
    c09_utc,
    validate_c09_identity,
)
from pixs.backend.c09_contracts import (
    C09PolicyV1,
    C09RoleDeclarationV1,
    validate_c09_policy,
    validate_c09_role_declaration,
)
from pixs.backend.c09_job_repository import C09JobRepository
from pixs.backend.c09_job_repository import C09Refused as RepoRefused
from pixs.backend.c09_worker import C09Worker
from pixs.core.scope.context import ScopeContext, ScopeType


def _policy(**over):
    base = dict(
        policy_reference="pol-c09-unit",
        policy_version="1.0.0",
        lease_seconds=30,
        renewal_seconds=5,
        max_attempts=3,
        retry_delays_seconds=(5, 10),
        polling_interval_ms=50,
        polling_max_batch=2,
        max_concurrency=2,
        max_units_per_poll=2,
        drain_seconds=5,
        attempt_timeout_seconds=10,
        job_timeout_seconds=60,
        process_count=1,
        cpu_millicores=100,
        max_connections=5,
        memory_mb=128,
        effective_from=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc),
    )
    base.update(over)
    return C09PolicyV1(**base)


def _context():
    return ScopeContext(ScopeType.PLATFORM, None, None)


def _identity(**over):
    base = dict(
        actor_reference="actor-u1",
        perimeter_reference="perim-u1",
        request_reference="req-u1",
        request_version="1.0.0",
        resource_id="res-u1",
        action_id="act-u1",
        context=_context(),
        correlation_id="corr-u1",
    )
    base.update(over)
    return C09Identity(**base)


def _repo_stub():
    repo = object.__new__(C09JobRepository)
    repo.calls = []
    return repo


class C09TextTests(unittest.TestCase):
    def test_accept(self):
        self.assertEqual(c09_text("ok"), "ok")

    def test_refuse_hostile(self):
        class SubStr(str):
            pass

        for bad in (None, "", 0, 1.5, b"x", ["x"], SubStr("ok"), "a\x00b"):
            with self.assertRaises(C09Refused):
                c09_text(bad)


class C09UtcTests(unittest.TestCase):
    def test_accept_utc(self):
        good = datetime.datetime(2026, 5, 1, tzinfo=datetime.timezone.utc)
        self.assertIs(c09_utc(good), good)

    def test_refuse_naive_and_offset(self):
        naive = datetime.datetime(2026, 5, 1)
        offset = datetime.datetime(
            2026, 5, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=1))
        )
        for bad in (None, "x", 1, naive, offset):
            with self.assertRaises(C09Refused):
                c09_utc(bad)

    def test_refuse_subclass_sans_appel(self):
        class Hostile(datetime.datetime):
            @property
            def tzinfo(self):  # ne doit jamais etre appele
                raise AssertionError("appel etranger interdit")

        # type exact d abord : l acces tzinfo n a pas lieu
        with self.assertRaises(C09Refused):
            c09_utc(Hostile(2026, 5, 1, tzinfo=datetime.timezone.utc))

    def test_refuse_zone_etrangere(self):
        paris = datetime.datetime(2026, 5, 1, tzinfo=ZoneInfo("Europe/Paris"))
        with self.assertRaises(C09Refused):
            c09_utc(paris)
        with self.assertRaises(C09Refused):
            c09_utc(paris, database=True)

    def test_database_seule_normalisation_utc(self):
        zoned = datetime.datetime(2026, 5, 1, tzinfo=ZoneInfo("UTC"))
        with self.assertRaises(C09Refused):
            c09_utc(zoned)
        out = c09_utc(zoned, database=True)
        self.assertIs(out.tzinfo, datetime.timezone.utc)
        etc = datetime.datetime(2026, 5, 1, tzinfo=ZoneInfo("Etc/UTC"))
        out = c09_utc(etc, database=True)
        self.assertIs(out.tzinfo, datetime.timezone.utc)


class C09IdentityTests(unittest.TestCase):
    def test_accept_retourne_meme_objet(self):
        value = _identity()
        self.assertIs(validate_c09_identity(value), value)

    def test_refuse_type(self):
        with self.assertRaises(C09Refused):
            validate_c09_identity(object())

    def test_refuse_champ_vide(self):
        with self.assertRaises(C09Refused):
            validate_c09_identity(_identity(actor_reference=""))

    def test_refuse_version(self):
        with self.assertRaises(C09Refused):
            validate_c09_identity(_identity(request_version="01.2.3"))

    def test_refuse_contexte(self):
        with self.assertRaises(C09Refused):
            validate_c09_identity(_identity(context="ctx"))


class C09PolicyTests(unittest.TestCase):
    def test_accept(self):
        self.assertEqual(validate_c09_policy(_policy()), [])

    def test_refuse_type(self):
        self.assertTrue(validate_c09_policy(object()))

    def test_marge_renouvellement(self):
        self.assertTrue(validate_c09_policy(_policy(renewal_seconds=20)))

    def test_coherence_tentative_travail(self):
        self.assertTrue(
            validate_c09_policy(
                _policy(attempt_timeout_seconds=120, job_timeout_seconds=60)
            )
        )

    def test_coherence_lot_unites(self):
        self.assertTrue(
            validate_c09_policy(
                _policy(polling_max_batch=3, max_units_per_poll=2)
            )
        )

    def test_longueur_delais(self):
        self.assertTrue(validate_c09_policy(_policy(retry_delays_seconds=(5,))))


class C09RoleTests(unittest.TestCase):
    def test_worker_accepte(self):
        good = C09RoleDeclarationV1("worker", "h-1", "1.0.0", "c-1")
        self.assertEqual(validate_c09_role_declaration(good), [])

    def test_role_ferme(self):
        from dataclasses import replace

        good = C09RoleDeclarationV1("worker", "h-1", "1.0.0", "c-1")
        bad = replace(good, role="unknown")
        self.assertTrue(validate_c09_role_declaration(bad))


class C09WorkerTests(unittest.TestCase):
    def test_init_type_exact(self):
        with self.assertRaises(RepoRefused):
            C09Worker(repository=object())
        worker = C09Worker(repository=_repo_stub())
        self.assertFalse(worker.admission_closed)

    def test_stop_avant_acquire_ne_restitue_pas(self):
        repo = _repo_stub()

        def _acquire(*, owner, policy):
            repo.calls.append("acquire")
            return object()

        def _restitute(*, handle, policy):  # ne doit pas etre appele
            raise AssertionError("restitution inattendue")

        repo.acquire_next = _acquire
        repo.restitute = _restitute
        worker = C09Worker(repository=repo)
        worker.request_stop()
        self.assertTrue(worker.admission_closed)
        self.assertIsNone(worker.run_once(owner="o-1", policy=_policy()))
        self.assertEqual(repo.calls, [])

    def test_stop_dans_acquire_restitue(self):
        repo = _repo_stub()
        lease = object()
        worker_ref = {}

        def _acquire(*, owner, policy):
            worker_ref["w"].request_stop()
            return lease

        seen = {}

        def _restitute(*, handle, policy):
            seen["handle"] = handle
            return ("restituted", handle)

        def _run_unit(*, handle, policy):  # ne doit pas etre appele
            raise AssertionError("unite inattendue")

        repo.acquire_next = _acquire
        repo.restitute = _restitute
        repo.run_unit = _run_unit
        worker = C09Worker(repository=repo)
        worker_ref["w"] = worker
        out = worker.run_once(owner="o-1", policy=_policy())
        self.assertEqual(out[0], "restituted")
        self.assertIs(seen["handle"], lease)

    def test_run_once_nominal(self):
        repo = _repo_stub()
        lease = object()
        repo.acquire_next = lambda *, owner, policy: lease
        repo.run_unit = lambda *, handle, policy: ("ran", handle)
        repo.restitute = lambda *, handle, policy: (_ for _ in ()).throw(
            AssertionError("restitution inattendue")
        )
        worker = C09Worker(repository=repo)
        out = worker.run_once(owner="o-1", policy=_policy())
        self.assertEqual(out, ("ran", lease))

    def test_run_once_sans_bail(self):
        repo = _repo_stub()
        repo.acquire_next = lambda *, owner, policy: None
        worker = C09Worker(repository=repo)
        self.assertIsNone(worker.run_once(owner="o-1", policy=_policy()))

    def test_run_once_policy_invalide(self):
        repo = _repo_stub()
        worker = C09Worker(repository=repo)
        with self.assertRaises(RepoRefused):
            worker.run_once(owner="o-1", policy=object())

    def test_run_batch_borne(self):
        repo = _repo_stub()
        repo.acquire_next = lambda *, owner, policy: object()
        repo.run_unit = lambda *, handle, policy: ("ran", handle)
        repo.restitute = lambda *, handle, policy: ("back", handle)
        worker = C09Worker(repository=repo)
        out = worker.run_batch(owner="o-1", policy=_policy(max_units_per_poll=2))
        self.assertEqual(len(out), 2)
        worker.request_stop()
        self.assertEqual(
            worker.run_batch(owner="o-1", policy=_policy(max_units_per_poll=2)), ()
        )


if __name__ == "__main__":
    unittest.main()
