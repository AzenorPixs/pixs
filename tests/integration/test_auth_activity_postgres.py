"""Activité serveur explicite ; producteur C06 remplacé par fixture de recette déclarée."""
from __future__ import annotations
EXPECTED_CASES=("interactive_extends_idle","original_time_preserved","absolute_unchanged","authentication_unchanged","same_event_no_extension","same_event_no_second_operation","boolean_refused","missing_event_refused","other_actor_refused","other_session_refused","future_event_refused","before_login_refused","audit_failure_rolls_back","expired_session_refused","other_session_preserved","audit_committed")

def scenarios():
    import datetime
    from dataclasses import replace
    from pixs.auth import models as m
    from pixs.auth.activity import UserActivityEvidence
    from pixs.auth.contracts import AuthServiceError
    from pixs.auth.identifiers import new_uuid7, identity_reference
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from auth_service_fixture import make_auth_service_fixture
    f=make_auth_service_fixture()
    out={}
    first,other=f["login"]("activity"),f["login"]("activity-other")
    session=m.AuthSession.objects.get(pk=first.session.session_id)
    other_before=m.AuthSession.objects.get(pk=other.session.session_id).last_activity_at
    original_auth,original_abs=session.authenticated_at,session.absolute_expires_at
    class FixtureServerActivitySource:
        # Registre serveur de recette explicite, aucune donnée de requête utilisée comme preuve.
        def __init__(self): self.events={}
        def verify_completed_interactive(self, ref, **kwargs):
            if ref not in self.events: raise AuthServiceError("AUTH_DENIED")
            return self.events[ref]
    source=FixtureServerActivitySource()
    def command(label):
        return f["grant"](f["command"]("pixs.auth.session.activity","pixs.auth.session:"+str(session.pk),label))
    def evidence(ref,when):
        return UserActivityEvidence(ref,f["actor"],session.pk,f["context"],when,"pixs.core.fixture-interactive","interactive-"+ref)
    def rejected(ref,label):
        before=m.AuthSession.objects.get(pk=session.pk)
        try: f["service"]().record_activity(command(label),first.emission.access,activity_reference=ref,activity_source=source)
        except AuthServiceError:
            after=m.AuthSession.objects.get(pk=session.pk)
            return (after.last_activity_at,after.idle_expires_at,after.version)==(before.last_activity_at,before.idle_expires_at,before.version)
        return False
    f["clock"].value += datetime.timedelta(seconds=100)
    source.events["interactive-one"]=evidence("interactive-one",f["clock"].value-datetime.timedelta(seconds=10))
    cmd=command("activity-one")
    result=f["service"]().record_activity(cmd,first.emission.access,activity_reference="interactive-one",activity_source=source)
    session.refresh_from_db()
    out["interactive_extends_idle"]=result.idle_expires_at==source.events["interactive-one"].occurred_at+datetime.timedelta(seconds=3600)
    out["original_time_preserved"]=session.last_activity_at==source.events["interactive-one"].occurred_at
    out["absolute_unchanged"]=session.absolute_expires_at==original_abs
    out["authentication_unchanged"]=session.authenticated_at==original_auth
    out["audit_committed"]=CoreAuditEvent.objects.filter(operation_id=cmd.operation_id).count()==1
    before_idle=session.idle_expires_at
    f["clock"].value += datetime.timedelta(seconds=100)
    repeat=command("activity-repeat-new-http")
    repeated=f["service"]().record_activity(repeat,first.emission.access,activity_reference="interactive-one",activity_source=source)
    out["same_event_no_extension"]=repeated.idle_expires_at==before_idle
    out["same_event_no_second_operation"]=not m.AuthOperation.objects.filter(operation_ref=repeat.operation_id).exists()
    source.events["boolean"]=True
    out["boolean_refused"]=rejected("boolean","activity-boolean")
    out["missing_event_refused"]=rejected("heartbeat","activity-heartbeat")
    base=evidence("wrong-actor",f["clock"].value)
    source.events["wrong-actor"]=replace(base,actor_ref=identity_reference(new_uuid7()))
    out["other_actor_refused"]=rejected("wrong-actor","activity-other-actor")
    source.events["wrong-session"]=replace(base,event_ref="wrong-session",session_id=other.session.session_id)
    out["other_session_refused"]=rejected("wrong-session","activity-wrong-session")
    source.events["future"]=evidence("future",f["clock"].value+datetime.timedelta(seconds=1))
    out["future_event_refused"]=rejected("future","activity-future")
    source.events["before"]=evidence("before",original_auth-datetime.timedelta(microseconds=1))
    out["before_login_refused"]=rejected("before","activity-before")
    source.events["audit-down"]=evidence("audit-down",f["clock"].value)
    down_cmd=command("activity-audit-down")
    before=m.AuthSession.objects.get(pk=session.pk)
    try: f["service"](1).record_activity(down_cmd,first.emission.access,activity_reference="audit-down",activity_source=source)
    except AuthServiceError:
        after=m.AuthSession.objects.get(pk=session.pk)
        out["audit_failure_rolls_back"]=(after.last_activity_at,after.idle_expires_at,after.version)==(before.last_activity_at,before.idle_expires_at,before.version) and not m.AuthOperation.objects.filter(operation_ref=down_cmd.operation_id).exists()
    else: out["audit_failure_rolls_back"]=False
    out["other_session_preserved"]=m.AuthSession.objects.get(pk=other.session.session_id).last_activity_at==other_before
    f["clock"].value=original_auth+datetime.timedelta(seconds=901)
    source.events["expired"]=evidence("expired",f["clock"].value)
    out["expired_session_refused"]=rejected("expired","activity-expired")
    return out

def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result=run_in_auth_schema(root_str,scenarios,EXPECTED_CASES,with_core=True)
    result["activity_source"]="FIXTURE_SERVEUR_EXPLICITE_PRODUCTEUR_C06_NON_LIVRE"
    result["full_p0_activation"]=False
    return result
