# path: tests/integration/test_agent_payload_provenance_postgres.py
"""PG reel provenance D-S1 3.6/3.7 : structure inerte seule, namespace ag10 isole.

Extensions partielles phy5, pas M1 complet ni classification M2 reelle.
Refs producteur/redacteur/preuve = stubs de fixture, aucune authenticite.
"""
from __future__ import annotations
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
EXPECTED_CASES = ("trois_cibles_valides", "formes_xor_partiels", "classified_null_pg", "contraintes_validation", "source_hash_divergent", "succession", "voies_refusees", "course_meme_revision", "contraintes_pg_physiques", "rollback", "reverse_apres_donnees", "registre_graphe_drift")
VALID_CLASSIFIED_AT = "2026-10-26T12:00:01.000001Z"
def _callback(refs, failures, tracked_threads, cases):
    from django.core.exceptions import ValidationError
    from django.core.management import call_command
    from django.db import IntegrityError, connections, transaction
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.recorder import MigrationRecorder
    from django.db.migrations.state import ProjectState
    from pixs.agent import models as m
    from pixs.agent.identifiers import new_agent_uuid7
    import test_agent_storage_postgres as stor
    from pixs.agent.repository import persist_desired_instruction, append_observation
    def ok(name, cond):
        cases[name] = bool(cond)
        if not cond:
            raise AssertionError(name)
        return True
    def _cname(exc):
        cur = exc
        for _ in range(3):
            diag = getattr(cur, "diag", None)
            if diag is not None and getattr(diag, "constraint_name", None):
                return diag.constraint_name
            cur = getattr(cur, "__cause__", None)
            if cur is None:
                break
        return None
    S = stor._scope("tenant-prov-a", "scope-prov-a")
    CAT = stor._catalog()
    _seq = {"n": 0}
    def _uniq(prefix):
        _seq["n"] += 1
        return "%s-%d-%s" % (prefix, _seq["n"], new_agent_uuid7().hex[:8])
    def _new_op():
        t = _uniq("pa-prov")
        oid = _uniq("op-prov")
        key = _uniq("key-prov")
        corr = ("corr-%s" % _uniq("c"),)
        ctx = stor._context(S, t, 0, oid, key, corr)
        ins = stor._instruction(S, t, 0, oid, key, corr)
        r = persist_desired_instruction(using="default", scope=S, target_id=t, instruction=ins, context=ctx, allowed_catalog=CAT, mandate_trust_port=stor._allow)
        return r["operation"]
    def _new_fact(op):
        corr = tuple(json.loads(op.correlation_ids_canonical))
        res = stor._result(S, op.target_id, op.generation, op.request_operation_id, corr, "ack", occurred="2029-12-31T23:00:00Z")
        ctx = stor._context(S, op.target_id, op.generation, op.request_operation_id, op.idempotency_key, corr)
        return append_observation(using="default", scope=S, target_id=op.target_id, result=res, context=ctx, observed_document="doc-%s" % _uniq("d"), observed_at="2029-12-31T23:30:00Z", source_ref="src-%s" % _uniq("s"), origin_trust_port=stor._allow)
    def _new_doc():
        from pixs.agent import documents as doc
        raw = doc.canonical_trace(request_operation_id=_uniq("prov-doc"), correlation_ids=("c1",), causation_ids=()).encode("utf-8")
        return m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=raw, byte_length=len(raw), bytes_sha256=hashlib.sha256(raw).hexdigest())
    def _op_sha(op):
        return hashlib.sha256(op.content_canonical.encode("utf-8")).hexdigest()
    def _fact_sha(fact):
        from pixs.agent import fact_inventory as inv
        canon = inv.canonical_fact_inventory(id=fact.id, operation_id=fact.operation_id, observed_fact_id=fact.observed_fact_id, scope_type=fact.scope_type, tenant_id=fact.tenant_id, scope_id=fact.scope_id, target_id=fact.target_id, generation=fact.generation, kind=fact.kind, outcome=fact.outcome, occurred_at=fact.occurred_at, observed_at=fact.observed_at, origin_proof=fact.origin_proof, observed_document=fact.observed_document, source_ref=fact.source_ref, proof_ref=fact.proof_ref, postcondition_ref=fact.postcondition_ref)
        return hashlib.sha256(canon.encode("utf-8")).hexdigest()
    def _mk_prov(*, operation_id=None, fact_id=None, document_id=None, revision=1, sup=None, state="CLASSIFIED", version="1.0.0", codec="agent-content.v1", precision="SECOND", prod="prod-stub-1", writer="w-1.0", ev="ev-stub-1", sha=None, at=VALID_CLASSIFIED_AT):
        return m.PayloadProvenance(id=new_agent_uuid7(), operation_id=operation_id, fact_id=fact_id, document_id=document_id, classification_revision=revision, supersedes_id=sup, classification_state=state, payload_contract_version=version, codec=codec, source_precision=precision, producer_ref=prod, writer_version=writer, evidence_ref=ev, source_bytes_sha256=sha, classified_at=at)
    op0 = _new_op()
    fact0 = _new_fact(op0)
    doc0 = _new_doc()
    p_op = _mk_prov(operation_id=op0.pk, sha=_op_sha(op0))
    p_op.save(using="default")
    p_fact = _mk_prov(fact_id=fact0.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=_fact_sha(fact0))
    p_fact.save(using="default")
    p_doc = _mk_prov(document_id=doc0.pk, state="INVALID", version=None, codec=None, precision="NOT_APPLICABLE", prod=None, writer=None, ev=None, sha=hashlib.sha256(doc0.payload_bytes).hexdigest())
    p_doc.save(using="default")
    ok("trois_cibles_valides", m.PayloadProvenance.objects.filter(pk=p_op.pk).count() == 1 and m.PayloadProvenance.objects.filter(pk=p_fact.pk).count() == 1 and m.PayloadProvenance.objects.filter(pk=p_doc.pk).count() == 1)
    xor = 0
    opX = _new_op()
    factX = _new_fact(opX)
    shaX = _op_sha(opX)
    for kw in (dict(operation_id=opX.pk, fact_id=factX.pk), dict(), dict(operation_id=opX.pk, fact_id=factX.pk, document_id=doc0.pk)):
        try:
            _mk_prov(sha=shaX, **kw).save(using="default")
        except ValidationError:
            xor += 1
    try:
        _mk_prov(operation_id=opX.pk, sha=shaX).save(using="default")
        _mk_prov(operation_id=opX.pk, sha=shaX).save(using="default")
    except (ValidationError, IntegrityError):
        xor += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,operation_id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), str(opX.pk), shaX, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_op_rev_uq":
            xor += 1
    ok("formes_xor_partiels", xor == 5)
    pg_null = 0
    opN1 = _new_op()
    shaN1 = _op_sha(opN1)
    opN2 = _new_op()
    shaN2 = _op_sha(opN2)
    _cols = "version,created_at,updated_at,persistence_state,retention_state,id,operation_id,classification_revision,classification_state,payload_contract_version,codec,source_precision,producer_ref,writer_version,evidence_ref,source_bytes_sha256,classified_at"
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (" + _cols + ") VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'CLASSIFIED',NULL,'agent-content.v1','SECOND','prod-stub-1','w-1.0','ev-stub-1',%s,%s);", [str(new_agent_uuid7()), str(opN1.pk), shaN1, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_classified_ck":
            pg_null += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (" + _cols + ") VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'CLASSIFIED','1.0.0','agent-content.v1',NULL,'prod-stub-1','w-1.0','ev-stub-1',%s,%s);", [str(new_agent_uuid7()), str(opN2.pk), shaN2, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_classified_ck":
            pg_null += 1
    ok("classified_null_pg", pg_null == 2)
    bad = 0
    opB = _new_op()
    shaB = _op_sha(opB)
    cases_bad = [
        _mk_prov(operation_id=opB.pk, state="NOPE", sha=shaB),
        _mk_prov(operation_id=opB.pk, revision=0, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB),
        _mk_prov(operation_id=__import__("uuid").uuid4(), revision=1, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB),
        _mk_prov(operation_id=opB.pk, revision=True, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB),
        _mk_prov(operation_id=opB.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB.upper(), revision=1),
        _mk_prov(operation_id=opB.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB, at="2026-10-26T12:00:01Z"),
        _mk_prov(operation_id=opB.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB, at="2026-13-99T99:99:99.000001Z"),
    ]
    for obj in cases_bad:
        try:
            obj.save(using="default")
        except ValidationError:
            bad += 1
    ok("contraintes_validation", bad == 7)
    opH = _new_op()
    shaH = _op_sha(opH)
    n_before = m.PayloadProvenance.objects.count()
    try:
        _mk_prov(operation_id=opH.pk, sha="0" * 64).save(using="default")
        diverged = False
    except ValidationError:
        diverged = True
    ok("source_hash_divergent", diverged and m.PayloadProvenance.objects.count() == n_before)
    docS = _new_doc()
    shaS = hashlib.sha256(docS.payload_bytes).hexdigest()
    r1 = _mk_prov(document_id=docS.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaS)
    r1.save(using="default")
    r2 = _mk_prov(document_id=docS.pk, revision=2, sup=r1.pk, codec="agent-content.v1", precision="NOT_APPLICABLE", sha=shaS)
    r2.save(using="default")
    rej = 0
    try:
        _mk_prov(document_id=docS.pk, revision=3, sup=p_op.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaS).save(using="default")
    except ValidationError:
        rej += 1
    try:
        _mk_prov(document_id=docS.pk, revision=1, sup=r2.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaS).save(using="default")
    except (ValidationError, IntegrityError):
        rej += 1
    try:
        _mk_prov(operation_id=op0.pk, revision=2, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=_op_sha(op0)).save(using="default")
    except ValidationError:
        rej += 1
    ok("succession", rej == 3 and m.PayloadProvenance.objects.filter(pk=r2.pk).count() == 1)
    voies = 0
    opV = _new_op()
    shaV = _op_sha(opV)
    try:
        m.PayloadProvenance.objects.bulk_create([_mk_prov(operation_id=opV.pk, revision=11, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaV)])
    except ValidationError:
        voies += 1
    try:
        m.PayloadProvenance.objects.filter(pk=p_op.pk).update(codec="x")
    except ValidationError:
        voies += 1
    try:
        m.PayloadProvenance.objects.filter(pk=p_op.pk).delete()
    except ValidationError:
        voies += 1
    try:
        m.PayloadProvenance._base_manager.bulk_create([_mk_prov(operation_id=opV.pk, revision=12, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaV)])
    except ValidationError:
        voies += 1
    try:
        m.PayloadProvenance.objects.db_manager("default").bulk_create([_mk_prov(operation_id=opV.pk, revision=13, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaV)])
    except ValidationError:
        voies += 1
    try:
        m.PayloadProvenance.objects.bulk_update([p_op], fields=["codec"])
    except ValidationError:
        voies += 1
    asyn = 0
    import asyncio as _asyncio
    async def _ta():
        await _mk_prov(operation_id=opV.pk, revision=14, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaV).asave()
    async def _tc():
        await m.PayloadProvenance.objects.acreate(id=new_agent_uuid7(), operation_id=opV.pk, classification_revision=15, supersedes_id=None, classification_state="AMBIGUOUS", payload_contract_version=None, codec=None, source_precision=None, producer_ref=None, writer_version=None, evidence_ref=None, source_bytes_sha256=shaV, classified_at=VALID_CLASSIFIED_AT)
    for coro in (_ta(), _tc()):
        try:
            _asyncio.run(coro)
        except ValidationError:
            asyn += 1
    stored = m.PayloadProvenance.objects.filter(pk=p_op.pk).first()
    snap = m.PayloadProvenance.objects.filter(pk=p_op.pk).values().get()
    try:
        stored.save(using="default")
        mod_refused = False
    except ValidationError:
        mod_refused = True
    opC = _new_op()
    shaC = _op_sha(opC)
    clone = m.PayloadProvenance(id=p_op.pk, operation_id=opC.pk, classification_revision=1, supersedes_id=None, classification_state="CLASSIFIED", payload_contract_version="1.0.0", codec="agent-content.v1", source_precision="SECOND", producer_ref="prod-stub-1", writer_version="w-1.0", evidence_ref="ev-stub-1", source_bytes_sha256=shaC, classified_at=VALID_CLASSIFIED_AT)
    try:
        clone.save(using="default")
        clone_refused = False
    except (ValidationError, IntegrityError):
        clone_refused = True
    fresh = m.PayloadProvenance.objects.filter(pk=p_op.pk).values().get()
    ok("voies_refusees", voies == 6 and asyn == 2 and mod_refused and clone_refused and fresh == snap and m.PayloadProvenance.objects.filter(pk=p_op.pk).count() == 1)
    opR = _new_op()
    shaR = _op_sha(opR)
    barrier = threading.Barrier(2)
    outcomes, errors, pids = {}, {}, {}
    def _worker(alias, slot):
        w = connections[alias]
        try:
            w.ensure_connection()
            if w.connection not in refs:
                refs.append(w.connection)
            with w.cursor() as cur:
                cur.execute("SELECT pg_backend_pid();")
                pids[slot] = int(cur.fetchone()[0])
            barrier.wait(timeout=10)
            outcomes[slot] = m.PayloadProvenance.objects.db_manager(alias).create(id=new_agent_uuid7(), operation_id=opR.pk, classification_revision=1, classification_state="CLASSIFIED", payload_contract_version="1.0.0", codec="agent-content.v1", source_precision="SECOND", producer_ref="prod-stub-1", writer_version="w-1.0", evidence_ref="ev-stub-1", source_bytes_sha256=shaR, classified_at=VALID_CLASSIFIED_AT)
        except Exception as e:
            errors[slot] = e
        finally:
            try:
                import core_pg_test_support as _core
                _core.close_django_connections(refs, failures)
            except Exception:
                failures.append("WORKER_CLOSE_FAILED")
    ta = threading.Thread(target=_worker, args=("peer", "a"))
    tb = threading.Thread(target=_worker, args=("contender", "b"))
    tracked_threads.append(ta)
    tracked_threads.append(tb)
    ta.start()
    tb.start()
    ta.join(timeout=30)
    tb.join(timeout=30)
    n_race = m.PayloadProvenance.objects.filter(operation_id=opR.pk, classification_revision=1).count()
    race_err = next(iter(errors.values()), None) if errors else None
    ok("course_meme_revision", len(outcomes) == 1 and len(errors) == 1 and isinstance(race_err, (ValidationError, IntegrityError)) and n_race == 1 and pids.get("a") != pids.get("b") and not ta.is_alive() and not tb.is_alive())
    phys = 0
    opP = _new_op()
    shaP = _op_sha(opP)
    dup = _mk_prov(operation_id=opP.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaP)
    dup.save(using="default")
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), shaP, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_target_ck":
            phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,operation_id,fact_id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), str(opP.pk), str(fact0.pk), shaP, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_target_ck":
            phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,operation_id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), str(opP.pk), shaP, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_op_rev_uq":
            phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,fact_id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), str(fact0.pk), _fact_sha(fact0), VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_fact_rev_uq":
            phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,document_id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), str(doc0.pk), hashlib.sha256(doc0.payload_bytes).hexdigest(), VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        if _cname(e) == "prov_doc_rev_uq":
            phys += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_payload_provenance (version,created_at,updated_at,persistence_state,retention_state,id,operation_id,classification_revision,classification_state,source_bytes_sha256,classified_at) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,%s,1,'AMBIGUOUS',%s,%s);", [str(new_agent_uuid7()), str(new_agent_uuid7()), shaP, VALID_CLASSIFIED_AT])
    except IntegrityError as e:
        _cause = getattr(e, "__cause__", None)
        _state = getattr(_cause, "sqlstate", None)
        _cls = type(_cause).__name__ if _cause is not None else ""
        if _state == "23503" or _cls == "ForeignKeyViolation":
            phys += 1
    ok("contraintes_pg_physiques", phys == 6)
    opB2 = _new_op()
    shaB2 = _op_sha(opB2)
    n_p_before = m.PayloadProvenance.objects.count()
    try:
        with transaction.atomic(using="default"):
            _mk_prov(operation_id=opB2.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaB2).save(using="default")
            raise RuntimeError("rollback-prov")
    except RuntimeError:
        pass
    ok("rollback", m.PayloadProvenance.objects.count() == n_p_before)
    opG = _new_op()
    shaG = _op_sha(opG)
    _mk_prov(operation_id=opG.pk, state="AMBIGUOUS", version=None, codec=None, precision=None, prod=None, writer=None, ev=None, sha=shaG).save(using="default")
    with connections["default"].cursor() as cur:
        tables_before = set(connections["default"].introspection.table_names(cur))
    rec_before = set(MigrationRecorder(connections["default"]).applied_migrations())
    rows_before = m.PayloadProvenance.objects.count()
    try:
        call_command("migrate", "pixs_agent", "0002", verbosity=0, interactive=False)
        raised = None
    except Exception as error:
        raised = error
    with connections["default"].cursor() as cur:
        tables_after = set(connections["default"].introspection.table_names(cur))
    rec_after = set(MigrationRecorder(connections["default"]).applied_migrations())
    ok("reverse_apres_donnees", type(raised) is RuntimeError and str(raised) == "MIGRATION_PROVENANCE_IRREVERSIBLE" and tables_after == tables_before and rec_after == rec_before and m.PayloadProvenance.objects.count() == rows_before)
    from django.apps import apps as _apps
    from pixs.agent import _registry_support as _reg
    _registered = list(_apps.get_app_config("pixs_agent").get_models())
    _by_name = {mm.__name__: mm for mm in _registered}
    _loader = MigrationExecutor(connections["default"]).loader
    reg_ok = _reg.check_registry_five(_apps, _by_name, m, _loader) is True
    tampered = dict(_by_name)
    tampered["PayloadProvenance"] = tampered["PayloadDocument"]
    sub_ok = _reg.check_registry_five(_apps, tampered, m, _loader) is False
    extra = dict(_by_name)
    extra["Inconnu"] = tampered["PayloadDocument"]
    unk_ok = _reg.check_registry_five(_apps, extra, m, _loader) is False
    _latest = _reg.WHITELIST[-1]
    _frozen = _loader.project_state([("pixs_agent", _latest)])
    _installed = ProjectState.from_apps(_apps)
    drift0 = MigrationAutodetector(_frozen, _installed).changes(graph=_loader.graph)
    drift_ok = not drift0.get("pixs_agent")
    _real_table = m.PayloadProvenance._meta.db_table
    try:
        m.PayloadProvenance._meta.db_table = "pixs_agent_bidon"
        altered_ok = _reg.check_registry_five(_apps, _by_name, m, _loader) is False
    finally:
        m.PayloadProvenance._meta.db_table = _real_table
    _sha_field = m.PayloadProvenance._meta.get_field("source_bytes_sha256")
    _real_max = _sha_field.max_length
    try:
        _sha_field.max_length = 32
        field_ok = _reg.check_registry_five(_apps, _by_name, m, _loader) is False
    finally:
        _sha_field.max_length = _real_max
    restored_ok = _reg.check_registry_five(_apps, _by_name, m, _loader) is True and field_ok
    _real_nodes = dict(_loader.graph.nodes)
    try:
        _loader.graph.nodes[("pixs_agent", "0001_bidon")] = _real_nodes[("pixs_agent", "0001_agent_initial")]
        inter_ok = _reg.check_frozen_states(_loader) is False
    finally:
        try:
            del _loader.graph.nodes[("pixs_agent", "0001_bidon")]
        except KeyError:
            pass
    _node3 = _loader.graph.node_map[("pixs_agent", "0003_agent_payload_provenance")]
    _real_parents = set(_node3.parents)
    class _FakeChild:
        def __init__(self, key):
            self.key = key
    try:
        _node3.parents = set(_real_parents) | {_FakeChild(("crime", "x"))}
        foreign_ok = _reg.check_frozen_states(_loader) is False
    finally:
        _node3.parents = _real_parents
    ok("registre_graphe_drift", reg_ok and sub_ok and unk_ok and drift_ok and altered_ok and restored_ok and inter_ok and foreign_ok)
    return cases
def main():
    sys.path.insert(0, "src")
    sys.path.insert(0, "tests/integration")
    import agent_pg_test_support as helper
    import inspect
    _sig = inspect.signature(helper.run_in_agent_schema)
    assert "with_payload_document" in _sig.parameters and "with_provenance" in _sig.parameters
    assert _sig.parameters["with_payload_document"].default is False and _sig.parameters["with_provenance"].default is False
    out = helper.run_in_agent_schema(EXPECTED_ROOT, _callback, EXPECTED_CASES, with_payload_document=True, with_provenance=True)
    safe = {"real_pg": bool(out.get("real_pg")), "code": str(out.get("code")), "failure_type": str(out.get("failure_type")), "failure_frames": list(out.get("failure_frames", [])), "pg_version_num": str(out.get("pg_version_num", "")), "django_version": str(out.get("django_version", "")), "cases": {k: bool(v) for k, v in dict(out.get("cases", {})).items()}, "expected": list(EXPECTED_CASES), "migration": bool(out.get("migration")), "namespace": bool(out.get("namespace")), "cleanup": bool(out.get("cleanup")), "conns_closed": bool(out.get("conns_closed")), "threads_closed": bool(out.get("threads_closed", False))}
    if out.get("remaining_namespace") is not None:
        safe["remaining_namespace"] = out["remaining_namespace"]
    print(json.dumps(safe, sort_keys=True))
    if not safe["real_pg"] or set(safe["cases"]) != set(EXPECTED_CASES) or not all(safe["cases"].values()):
        return 1
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
