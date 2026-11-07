"""PG reel documents payload D-S1 3.4 : table seule, namespace ag10 isole.

Modele synchrone seulement : asave/acreate explicitement refuses par conception
et exerces ci-dessous. Helper namespaces jetables, option
with_payload_document=True explicite ici ; la compatibilite False (profil
historique 0001, 3 tables, _installed_sync True) est prouvee par les suites
existantes (14 adapter PG + 20 stockage PG) dans des processus isoles, plus le
gate historique pre-0002 de ce run (tables==3, recorder=={0001} avant
migration 0002). Aucune FK fictive, aucun transport, temps, provenance,
autorite ou activation Agent 2.0.0 revendiques.
"""
from __future__ import annotations
import asyncio
import hashlib
import json
import os
import sys
import threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
sys.path.insert(0, os.path.join(ROOT, "tests", "integration"))
from agent_pg_test_support import EXPECTED_ROOT, run_in_agent_schema
EXPECTED_CASES = ("aller_retour_v1_v2", "vecteurs_trace_observation", "refus_fermes", "contraintes_pg_physiques", "append_only", "course_meme_pk", "voies_bulk_refusees", "async_refuse", "rollback", "reverse_apres_insertion", "etats_migration")
GOLDEN_TRACE = '{"causation_ids":["z"],"correlation_ids":["café","café","a b"],"request_operation_id":"req-1"}'
def _content_v1():
    from pixs.agent import identifiers as ids
    params = ids.canonical_params_text({})
    return ids.canonical_operation_content(schema_version="1.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="s", tenant_id=None, scope_id=None, target_id="t", expected_generation=0, params_canonical=params, mandate_ref="m", expires_at="2026-10-27T12:00:01Z", scope_type="PLATFORM")
def _content_v2():
    from pixs.agent import identifiers as ids
    params = ids.canonical_params_text({})
    return ids.canonical_operation_content_v2(schema_version="2.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="s", tenant_id=None, scope_id=None, target_id="t", expected_generation=0, params_canonical=params, mandate_ref="m", expires_at="2026-10-27T12:00:01.000001Z", scope_type="PLATFORM")
def _kwargs(kind, version, codec, raw, doc_id):
    return dict(id=doc_id, document_kind=kind, payload_contract_version=version, codec=codec, payload_bytes=raw, byte_length=len(raw), bytes_sha256=hashlib.sha256(raw).hexdigest())
def _callback(refs, failures, tracked_threads, cases):
    import uuid
    from django.core.exceptions import ValidationError
    from django.core.management import call_command
    from django.db import IntegrityError, connections, transaction
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.recorder import MigrationRecorder
    from pixs.agent import documents as doc
    from pixs.agent import models as m
    from pixs.agent.identifiers import new_agent_uuid7
    def ok(name, cond):
        cases[name] = bool(cond)
        if not cond:
            raise AssertionError(name)
        return True
    r1 = _content_v1().encode("utf-8")
    r2 = _content_v2().encode("utf-8")
    d1 = m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_CONTENT, "1.0.0", "agent-content.v1", r1, new_agent_uuid7()))
    d2 = m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_CONTENT, "2.0.0", "agent-content.v2", r2, new_agent_uuid7()))
    got1 = m.PayloadDocument.objects.filter(pk=d1.pk).first()
    got2 = m.PayloadDocument.objects.filter(pk=d2.pk).first()
    ok("aller_retour_v1_v2", got1 is not None and got1.payload_bytes == r1 and got2 is not None and got2.payload_bytes == r2)
    traw = GOLDEN_TRACE.encode("utf-8")
    oraw = "café \U0001F600".encode("utf-8")
    dt = m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))
    do = m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_OBSERVATION, "2.0.0", doc.OBSERVED_CODEC, oraw, new_agent_uuid7()))
    _dt_db = m.PayloadDocument.objects.filter(pk=dt.pk).first()
    _do_db = m.PayloadDocument.objects.filter(pk=do.pk).first()
    ok("vecteurs_trace_observation", _dt_db is not None and _do_db is not None and _dt_db.payload_bytes.decode("utf-8") == GOLDEN_TRACE and _do_db.payload_bytes.decode("utf-8") == "café \U0001F600")
    bad = 0
    for kw in (dict(_kwargs("AUTRE", "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7())), dict(_kwargs(doc.AGENT_TRACE, "9.9.9", doc.TRACE_CODEC, traw, new_agent_uuid7())), dict(_kwargs(doc.AGENT_TRACE, "1.0.0", doc.OBSERVED_CODEC, traw, new_agent_uuid7()))):
        try:
            m.PayloadDocument.objects.create(**kw)
        except ValidationError:
            bad += 1
    corrupt = bytearray(r1)
    corrupt[0] ^= 1
    try:
        m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_CONTENT, payload_contract_version="1.0.0", codec="agent-content.v1", payload_bytes=bytes(corrupt), byte_length=len(corrupt), bytes_sha256=hashlib.sha256(r1).hexdigest())
    except ValidationError:
        bad += 1
    try:
        m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=True, bytes_sha256=hashlib.sha256(traw).hexdigest())
    except ValidationError:
        bad += 1
    try:
        m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=9223372036854775808, bytes_sha256=hashlib.sha256(traw).hexdigest())
    except ValidationError:
        bad += 1
    try:
        m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_OBSERVATION, payload_contract_version="1.0.0", codec=doc.OBSERVED_CODEC, payload_bytes=b"x", byte_length=True, bytes_sha256=hashlib.sha256(b"x").hexdigest())
    except ValidationError:
        bad += 1
    try:
        _vkw = _kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7())
        _vkw["version"] = True
        m.PayloadDocument.objects.create(**_vkw)
    except ValidationError:
        bad += 1
    ok("refus_fermes", bad == 8)
    phys = 0
    _cols = "version,created_at,updated_at,governance_ref,confidentiality,personal,persistence_state,retention_state,id,document_kind,payload_contract_version,codec,payload_bytes,byte_length,bytes_sha256"
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_document (" + _cols + ") VALUES (1, now(), now(), NULL, NULL, NULL, 'ACTIVE', 'RETAINED', %s, 'AGENT_TRACE', '1.0.0', 'agent-traces.v1', %s, %s, %s);", [str(uuid.uuid4()), traw, len(traw), hashlib.sha256(traw).hexdigest()])
    except IntegrityError:
        phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_document (" + _cols + ") VALUES (1, now(), now(), NULL, NULL, NULL, 'ACTIVE', 'RETAINED', %s, 'AGENT_TRACE', '1.0.0', 'agent-traces.v1', %s, 0, %s);", [str(new_agent_uuid7()), traw, hashlib.sha256(traw).hexdigest()])
    except IntegrityError:
        phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_document (" + _cols + ") VALUES (1, now(), now(), NULL, NULL, NULL, 'ACTIVE', 'RETAINED', %s, 'AGENT_TRACE', '1.0.0', 'agent-traces.v1', %s, %s, %s);", [str(new_agent_uuid7()), traw, len(traw), hashlib.sha256(traw).hexdigest().upper()])
    except IntegrityError:
        phys += 1
    dup_id = new_agent_uuid7()
    m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, dup_id))
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_document (" + _cols + ") VALUES (1, now(), now(), NULL, NULL, NULL, 'ACTIVE', 'RETAINED', %s, 'AGENT_TRACE', '1.0.0', 'agent-traces.v1', %s, %s, %s);", [str(dup_id), traw, len(traw), hashlib.sha256(traw).hexdigest()])
    except IntegrityError:
        phys += 1
    ok("contraintes_pg_physiques", phys == 4)
    stored = m.PayloadDocument.objects.filter(pk=d1.pk).first()
    created, updated = stored.created_at, stored.updated_at
    stored.payload_bytes = r2
    try:
        stored.save()
        append_refused = False
    except ValidationError:
        append_refused = True
    clone = m.PayloadDocument(id=d1.pk, document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=r2, byte_length=len(r2), bytes_sha256=hashlib.sha256(r2).hexdigest())
    try:
        clone.save()
        clone_refused = False
    except IntegrityError:
        clone_refused = True
    except ValidationError:
        clone_refused = True
    fresh = m.PayloadDocument.objects.filter(pk=d1.pk).first()
    ok("append_only", append_refused and clone_refused and fresh.payload_bytes == r1 and fresh.created_at == created and fresh.updated_at == updated)
    race_id = new_agent_uuid7()
    raw_a = doc.canonical_trace(request_operation_id="race-a", correlation_ids=("a",), causation_ids=()).encode("utf-8")
    raw_b = doc.canonical_trace(request_operation_id="race-b", correlation_ids=("b",), causation_ids=()).encode("utf-8")
    barrier = threading.Barrier(2)
    outcomes, errors, pids = {}, {}, {}
    def _worker(alias, raw, slot):
        w = connections[alias]
        try:
            w.ensure_connection()
            if w.connection not in refs:
                refs.append(w.connection)
            with w.cursor() as cur:
                cur.execute("SELECT pg_backend_pid();")
                pids[slot] = int(cur.fetchone()[0])
            barrier.wait(timeout=10)
            outcomes[slot] = m.PayloadDocument.objects.db_manager(alias).create(id=race_id, document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=raw, byte_length=len(raw), bytes_sha256=hashlib.sha256(raw).hexdigest())
        except Exception as e:
            errors[slot] = e
        finally:
            try:
                import core_pg_test_support as _core
                _core.close_django_connections(refs, failures)
            except Exception:
                failures.append("WORKER_CLOSE_FAILED")
    ta = threading.Thread(target=_worker, args=("peer", raw_a, "a"))
    tb = threading.Thread(target=_worker, args=("contender", raw_b, "b"))
    tracked_threads.append(ta)
    tracked_threads.append(tb)
    ta.start()
    tb.start()
    ta.join(timeout=30)
    tb.join(timeout=30)
    n_race = m.PayloadDocument.objects.filter(pk=race_id).count()
    race_err = next(iter(errors.values()), None) if errors else None
    winner = next(iter(outcomes.values()), None) if outcomes else None
    kept = m.PayloadDocument.objects.filter(pk=race_id).first()
    ok("course_meme_pk", len(outcomes) == 1 and len(errors) == 1 and isinstance(race_err, IntegrityError) and n_race == 1 and pids.get("a") != pids.get("b") and not ta.is_alive() and not tb.is_alive() and kept is not None and winner is not None and kept.payload_bytes == winner.payload_bytes and kept.created_at == winner.created_at and kept.updated_at == winner.updated_at)
    bulk = 0
    try:
        m.PayloadDocument.objects.bulk_create([m.PayloadDocument(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))])
    except ValidationError:
        bulk += 1
    try:
        m.PayloadDocument.objects.filter(pk=d2.pk).bulk_create([m.PayloadDocument(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))])
    except ValidationError:
        bulk += 1
    try:
        m.PayloadDocument.objects.filter(pk=d2.pk).update(codec="x")
    except ValidationError:
        bulk += 1
    try:
        m.PayloadDocument.objects.bulk_update([d2], fields=["codec"])
    except ValidationError:
        bulk += 1
    try:
        m.PayloadDocument.objects.filter(pk=d2.pk).delete()
    except ValidationError:
        bulk += 1
    try:
        m.PayloadDocument._base_manager.bulk_create([m.PayloadDocument(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))])
    except ValidationError:
        bulk += 1
    try:
        m.PayloadDocument.objects.db_manager("default").bulk_create([m.PayloadDocument(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))])
    except ValidationError:
        bulk += 1
    ok("voies_bulk_refusees", bulk == 7 and m.PayloadDocument.objects.filter(pk=d2.pk).first() is not None)
    asyn = 0
    async def _try_asave():
        obj = m.PayloadDocument(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))
        await obj.asave()
    async def _try_acreate():
        await m.PayloadDocument.objects.acreate(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))
    for coro in (_try_asave(), _try_acreate()):
        try:
            asyncio.run(coro)
        except ValidationError:
            asyn += 1
    ok("async_refuse", asyn == 2)
    n_before = m.PayloadDocument.objects.count()
    try:
        with transaction.atomic(using="default"):
            m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, new_agent_uuid7()))
            raise RuntimeError("rollback-fixture")
    except RuntimeError:
        pass
    ok("rollback", m.PayloadDocument.objects.count() == n_before)
    rev_id = new_agent_uuid7()
    m.PayloadDocument.objects.create(**_kwargs(doc.AGENT_TRACE, "1.0.0", doc.TRACE_CODEC, traw, rev_id))
    with connections["default"].cursor() as cur:
        tables_before = set(connections["default"].introspection.table_names(cur))
    rec_before = set(MigrationRecorder(connections["default"]).applied_migrations())
    try:
        call_command("migrate", "pixs_agent", "0001", verbosity=0, interactive=False)
        reverse_raised = None
    except Exception as error:
        reverse_raised = error
    with connections["default"].cursor() as cur:
        tables_after = set(connections["default"].introspection.table_names(cur))
    rec_after = set(MigrationRecorder(connections["default"]).applied_migrations())
    ok("reverse_apres_insertion", type(reverse_raised) is RuntimeError and str(reverse_raised) == "MIGRATION_DOCUMENT_IRREVERSIBLE" and tables_after == tables_before and rec_after == rec_before and m.PayloadDocument.objects.filter(pk=rev_id).first() is not None)
    from django.apps import apps as _apps
    _registered = list(_apps.get_app_config("pixs_agent").get_models())
    _by_name = {mm.__name__: mm for mm in _registered}
    _loader = MigrationExecutor(connections["default"]).loader
    _historical = _loader.project_state([("pixs_agent", "0001_agent_initial")]).apps.get_app_config("pixs_agent")
    _target = _loader.project_state([("pixs_agent", "0002_agent_payload_document")]).apps.get_app_config("pixs_agent")
    ok("etats_migration", _by_name.get("PayloadDocument") is m.PayloadDocument and {_mm._meta.db_table for _mm in _historical.get_models()} == {"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact"} and {_mm._meta.db_table for _mm in _target.get_models()} == {"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document"})
    return cases
def main():
    sys.path.insert(0, "src")
    sys.path.insert(0, "tests/integration")
    import agent_pg_test_support as helper
    out = helper.run_in_agent_schema(EXPECTED_ROOT, _callback, EXPECTED_CASES, with_payload_document=True)
    safe = {"real_pg": bool(out.get("real_pg")), "code": str(out.get("code")), "failure_type": str(out.get("failure_type")), "failure_frames": list(out.get("failure_frames", [])), "pg_version_num": str(out.get("pg_version_num", "")), "django_version": str(out.get("django_version", "")), "cases": {k: bool(v) for k, v in dict(out.get("cases", {})).items()}, "expected": list(EXPECTED_CASES), "migration": bool(out.get("migration")), "namespace": bool(out.get("namespace")), "cleanup": bool(out.get("cleanup")), "conns_closed": bool(out.get("conns_closed")), "threads_closed": bool(out.get("threads_closed", False))}
    if out.get("remaining_namespace") is not None:
        safe["remaining_namespace"] = out["remaining_namespace"]
    print(json.dumps(safe, sort_keys=True))
    if not safe["real_pg"] or set(safe["cases"]) != set(EXPECTED_CASES) or not all(safe["cases"].values()):
        return 1
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
