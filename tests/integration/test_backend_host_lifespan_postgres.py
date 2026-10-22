"""Lifespan Auth sur PG isole, sept controles reels."""
from __future__ import annotations

import json
import asyncio
from pathlib import Path
import subprocess
import sys
import unittest

_ROOT = Path(__file__).parents[2]
_THIS = Path(__file__)
_CHILD = "--child-lifespan"
_EXPECTED = (
    "acquire_profile_close", "bad_profile_partial_cleanup", "bad_alias_closed",
    "cancel_during_yield", "cancel_during_acquire", "caller_preserved",
    "missing_table_refused",
)

if _CHILD in sys.argv:
    sys.path.insert(0, str(_ROOT / "src"))
    sys.path.insert(0, str(_ROOT / "tests" / "integration"))
    from auth_pg_test_support import run_in_auth_schema

    def scenarios():
        import asyncio
        import threading
        from asgiref.sync import ThreadSensitiveContext, sync_to_async
        from django.db.backends.signals import connection_created
        from auth_service_fixture import make_auth_service_fixture
        from pixs.auth.runtime_verifier import AuthVerificationError
        from pixs.backend.host_lifespan import (
            AuthHostConfig, HostLifespanError, host_auth_lifespan, _HostAuthState,
        )
        from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
        from pixs.core.authz.snapshot import Catalog, Limits
        from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
        from pixs.auth.contracts import AuthDataClassification

        f = make_auth_service_fixture()
        actor, context, clock = f["actor"], f["context"], f["clock"]
        profile_id = f["profile"].profile_id
        account = "pixs.auth.account:" + str(f["identity"])
        actions = ("pixs.auth.session.create", "pixs.auth.session.logout")
        catalog = Catalog((actor,), tuple(sorted((actor, account))), actions, (context,), ())
        limits = Limits(128, 128, 10, 100, 100, 128, 256, 256, 10000000, 60, 3600)
        policy = AuditPolicy("c07-life", "1.0.0", "fixture", 1, 65536, 100, (),
            "c07-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
        policy_source = ExplicitAuditPolicySource(context, policy)

        class ClassificationC10:
            def resolve(self, **kw):
                return AuthDataClassification("c07", ConfidentialityLevel.CONFIDENTIAL,
                    PersonalDataLevel.PERSONAL)

        def make_config(**over):
            kw = dict(alias="default", peer_alias="peer", profile_id=profile_id,
                clock=clock, installation_ref="c07-life", base_epoch="c07-v1",
                catalog=catalog, limits=limits, policy_source=policy_source,
                classification_source=ClassificationC10())
            kw.update(over)
            return AuthHostConfig(**kw)

        raw_refs = []

        def receiver(sender, connection, **kwargs):
            assert connection.connection is not None
            raw_refs.append(connection.connection)

        async def run_all():
            from django.utils.connection import ConnectionDoesNotExist
            out = {}

            def closed_since(start, count):
                refs = raw_refs[start:]
                assert len(refs) == count
                assert all(ref.closed for ref in refs)

            async def require_cancel(task):
                try:
                    await asyncio.wait_for(task, 10)
                except asyncio.CancelledError:
                    return
                raise AssertionError("Annulation non propagee")

            start = len(raw_refs)
            async with host_auth_lifespan(make_config(), context=context) as bundle:
                current = await sync_to_async(bundle.trust_source.current_profile, thread_sensitive=True)(context)
                assert current == f["profile"]
                assert bundle.service is not None
            closed_since(start, 2)
            out["acquire_profile_close"] = True

            start = len(raw_refs)
            try:
                async with host_auth_lifespan(make_config(profile_id="c07-absent"), context=context):
                    raise AssertionError("Profil absent accepte")
            except AuthVerificationError:
                closed_since(start, 2)
            out["bad_profile_partial_cleanup"] = True

            for override, expected in ((dict(alias="c07-no-alias"), ConnectionDoesNotExist),
                                       (dict(peer_alias="default"), HostLifespanError)):
                start = len(raw_refs)
                try:
                    async with host_auth_lifespan(make_config(**override), context=context):
                        raise AssertionError("Alias invalide accepte")
                except expected:
                    assert len(raw_refs) == start
            out["bad_alias_closed"] = True

            entered = asyncio.Event()
            async def held_context():
                async with host_auth_lifespan(make_config(), context=context):
                    entered.set()
                    await asyncio.Event().wait()
            start = len(raw_refs)
            task = asyncio.create_task(held_context())
            try:
                await asyncio.wait_for(entered.wait(), 10)
                task.cancel()
                await require_cancel(task)
            finally:
                if not task.done():
                    task.cancel()
                    await require_cancel(task)
            closed_since(start, 2)
            out["cancel_during_yield"] = True

            acquired, release = threading.Event(), threading.Event()
            original = _HostAuthState.acquire
            def delayed_acquire(self, config, scope):
                bundle = original(self, config, scope)
                acquired.set()
                if not release.wait(10):
                    raise AssertionError("Acquisition non liberee")
                return bundle
            async def acquire_context():
                async with host_auth_lifespan(make_config(), context=context):
                    raise AssertionError("Annulation acquisition perdue")
            start = len(raw_refs)
            _HostAuthState.acquire = delayed_acquire
            task = asyncio.create_task(acquire_context())
            try:
                assert await asyncio.to_thread(acquired.wait, 10)
                task.cancel()
                release.set()
                await require_cancel(task)
            finally:
                release.set()
                try:
                    if not task.done():
                        task.cancel()
                        await require_cancel(task)
                finally:
                    _HostAuthState.acquire = original
            closed_since(start, 2)
            out["cancel_during_acquire"] = True

            def open_peer():
                from django.db import connections
                conn = connections["peer"]
                conn.ensure_connection()
                return conn.connection
            def peer_usable():
                from django.db import connections
                return connections["peer"].is_usable()
            def close_all():
                from django.db import connections
                connections.close_all()
            async with ThreadSensitiveContext():
                raw_peer = await sync_to_async(open_peer, thread_sensitive=True)()
                try:
                    start = len(raw_refs)
                    async with host_auth_lifespan(make_config(), context=context):
                        assert not raw_peer.closed
                    closed_since(start, 1)
                    assert not raw_peer.closed
                    assert await sync_to_async(peer_usable, thread_sensitive=True)()
                finally:
                    await sync_to_async(close_all, thread_sensitive=True)()
                assert raw_peer.closed
            out["caller_preserved"] = True

            def alter_pending(*, create):
                from django.apps import apps
                from django.db import connections
                model = apps.get_model("pixs_auth", "AuthAuditPending")
                if not create:
                    assert model.objects.count() == 0
                with connections["default"].schema_editor() as editor:
                    if create:
                        editor.create_model(model)
                    else:
                        editor.delete_model(model)
            async with ThreadSensitiveContext():
                try:
                    await sync_to_async(alter_pending, thread_sensitive=True)(create=False)
                    try:
                        try:
                            async with host_auth_lifespan(make_config(), context=context):
                                raise AssertionError("Table absente acceptee")
                        except HostLifespanError:
                            out["missing_table_refused"] = True
                    finally:
                        await sync_to_async(alter_pending, thread_sensitive=True)(create=True)
                finally:
                    await sync_to_async(close_all, thread_sensitive=True)()
            assert set(out) == set(_EXPECTED) and all(out.values())
            return out

        connection_created.connect(receiver, dispatch_uid="c07-lifespan", weak=False)
        try:
            return asyncio.run(run_all())
        finally:
            connection_created.disconnect(dispatch_uid="c07-lifespan")

    result = run_in_auth_schema(str(_ROOT), scenarios, _EXPECTED, with_core=True, core_target="0003_core_idempotence")
    safe = ("real_pg", "code", "failure_type", "failure_frames", "cases",
        "pg_version_num", "django_version", "cleanup", "conns_closed",
        "migration", "core_migration", "namespace")
    print(json.dumps({k: result[k] for k in safe}, ensure_ascii=False))
    sys.exit(0 if result["real_pg"] else 1)


class ParentTests(unittest.TestCase):
    def test_wiring(self):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run([sys.executable, "-B", str(_THIS), _CHILD],
            timeout=300, capture_output=True, text=True, env=env, cwd=str(_ROOT))
        self.assertTrue(bool(r.stdout.strip()), "Reponse absente")
        payload = json.loads(r.stdout.strip().splitlines()[-1])
        self.assertEqual(r.returncode, 0, json.dumps(payload, ensure_ascii=False))
        self.assertTrue(payload["real_pg"] and payload["cleanup"] and payload["conns_closed"])
        self.assertEqual(set(payload["cases"]), set(_EXPECTED))
        self.assertTrue(all(payload["cases"].values()))
        print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
