"""ASGI Django réel C09 : lifecycle C07, refus surcharge, tailles bornées et drain UNKNOWN."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT=Path(__file__).parents[2]
_ENV={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8",
      "PYTHONPATH":str(_ROOT/"src")+":"+str(_ROOT/"tests"/"integration"),"PYTHONDONTWRITEBYTECODE":"1"}
_EXPECTED=(
    "before_start_http_503","normal_lifespan_enters_c07","liveness_real_django_200",
    "private_route_403_never_handler","web_no_wait_queue_overload_503",
    "web_one_inflight_persisted","oversized_body_413_before_view",
    "normal_shutdown_stopped_and_after_http_503","second_asgi_instance_refused",
    "source_lost_closes_new_http","source_lost_shutdown_not_faked",
    "unfinished_http_drain_failed_unknown","late_http_completion_does_not_rewrite_unknown",
)


def scenarios(ctx):
    import asyncio
    import types
    from django.conf import settings
    from django.http import HttpResponse
    from django.db import connections
    from asgiref.testing import ApplicationCommunicator
    from c09_entry_fixture import build_entry
    from pixs.backend.http_route_guard import RouteDeclaration,build_declared_urlpatterns
    from pixs.backend.liveness_view import liveness_view
    from pixs.backend.c09_authorization_adapter import C09Refused
    from pixs.backend.c09_event_records import C09RuntimeInstanceRecord as Slot
    calls=[]
    holders={}
    async def slow(request):
        calls.append("slow")
        holders["started"].set()
        await holders["release"].wait()
        return HttpResponse(b"ok",status=200)
    def private(request):
        calls.append("private")
        return HttpResponse(b"forbidden",status=200)
    def body_probe(request):
        calls.append("body")
        return HttpResponse(b"ok",status=200)
    urlconf=types.ModuleType("synthetic_c09_entry_web_urls")
    urlconf.urlpatterns=build_declared_urlpatterns((
        RouteDeclaration("health/live","live",liveness_view,True),
        RouteDeclaration("private","private",private,False),
        RouteDeclaration("slow","slow",slow,True),
        RouteDeclaration("body","body",body_probe,True)))
    settings.ROOT_URLCONF=urlconf
    settings.ALLOWED_HOSTS=["testserver"]
    settings.MIDDLEWARE=["pixs.backend.host_entry.HostBoundaryMiddleware","django.middleware.security.SecurityMiddleware"]
    settings.USE_X_FORWARDED_HOST=False
    settings.SECURE_PROXY_SSL_HEADER=None
    cases={}
    def scope(path,method="GET"):
        return dict(type="http",http_version="1.1",method=method,scheme="http",path=path,
                    raw_path=path.encode(),query_string=b"",headers=[(b"host",b"testserver")])
    async def request(host,path,body=b""):
        comm=ApplicationCommunicator(host,scope(path,"POST" if body else "GET"))
        await comm.send_input({"type":"http.request","body":body,"more_body":False})
        start=await comm.receive_output(timeout=10)
        chunks=[]
        while True:
            message=await comm.receive_output(timeout=10)
            chunks.append(message.get("body",b""))
            if not message.get("more_body",False):
                break
        await comm.wait(timeout=10)
        return start["status"],b"".join(chunks)
    class Life:
        def __init__(self,host):
            self.comm=ApplicationCommunicator(host,{"type":"lifespan"})
        async def start(self):
            await self.comm.send_input({"type":"lifespan.startup"})
            return await self.comm.receive_output(timeout=15)
        async def stop(self):
            await self.comm.send_input({"type":"lifespan.shutdown"})
            message=await self.comm.receive_output(timeout=10)
            await self.comm.wait(timeout=10)
            return message
    async def inspect(entry):
        def read():
            try:
                return entry.repository.inspect()
            finally:
                connections.close_all()
        return await asyncio.to_thread(read)
    async def async_cases():
        entry,events,adapters=build_entry(role="WEB",case="web-clean",driver_factory=None,
                                         flags={},process_reference="process:web-clean")
        host=entry.build_asgi()
        if (await request(host,"/health/live"))[0]!=503:
            raise RuntimeError("HTTP_AVANT_START_ADMIS")
        cases["before_start_http_503"]=True
        life=Life(host)
        if (await life.start())["type"]!="lifespan.startup.complete" or not [e for e in events if e.startswith("hook:")]:
            raise RuntimeError("LIFESPAN_C07_NON_ACTIVE")
        cases["normal_lifespan_enters_c07"]=True
        if (await request(host,"/health/live"))[0]!=200:
            raise RuntimeError("VIVACITE_DJANGO_NON_REELLE")
        cases["liveness_real_django_200"]=True
        if (await request(host,"/private"))[0]!=403 or "private" in calls:
            raise RuntimeError("ROUTE_PRIVEE_A_EXECUTE_HANDLER")
        cases["private_route_403_never_handler"]=True
        holders["started"],holders["release"]=asyncio.Event(),asyncio.Event()
        running=asyncio.create_task(request(host,"/slow"))
        await asyncio.wait_for(holders["started"].wait(),timeout=10)
        if (await request(host,"/health/live"))[0]!=503:
            raise RuntimeError("SURCHARGE_WEB_MISE_EN_FILE")
        cases["web_no_wait_queue_overload_503"]=True
        if (await inspect(entry)).inflight_count!=1:
            raise RuntimeError("INFLIGHT_WEB_NON_PERSISTE")
        holders["release"].set()
        if (await running)[0]!=200:
            raise RuntimeError("UNITE_HTTP_ENGAGEE_PERDUE")
        cases["web_one_inflight_persisted"]=True
        if (await request(host,"/body",b"x"*(entry.plan.queues.buffer_bytes+1)))[0]!=413 or "body" in calls:
            raise RuntimeError("CORPS_NON_BORNE_OU_VUE_DEJA_INVOQUEE")
        cases["oversized_body_413_before_view"]=True
        if (await life.stop())["type"]!="lifespan.shutdown.complete":
            raise RuntimeError("ARRET_WEB_QUIESCENT_REFUSE")
        stopped=await inspect(entry)
        if stopped.stop_state!="STOPPED" or stopped.inflight_count!=0 or (await request(host,"/health/live"))[0]!=503:
            raise RuntimeError("HTTP_APRES_STOP_OU_FAUX_QUIESCENT")
        cases["normal_shutdown_stopped_and_after_http_503"]=True
        try:
            entry.build_asgi()
        except C09Refused:
            pass
        else:
            raise RuntimeError("SECOND_WRAPPER_ASGI_ACCEPTE")
        cases["second_asgi_instance_refused"]=True

        flags={}
        lost,_,_=build_entry(role="WEB",case="web-source-lost",driver_factory=None,
                              flags=flags,process_reference="process:web-source-lost",drain_seconds=2)
        lost_host=lost.build_asgi()
        lost_life=Life(lost_host)
        if (await lost_life.start())["type"]!="lifespan.startup.complete":
            raise RuntimeError("WEB_SOURCE_START_ECHEC")
        flags["readmission_state"]="STALE"
        if (await request(lost_host,"/health/live"))[0]!=503:
            raise RuntimeError("SOURCE_PERIMEE_HTTP_ADMIS")
        cases["source_lost_closes_new_http"]=True
        if (await lost_life.stop())["type"]!="lifespan.shutdown.failed" or (await inspect(lost)).stop_state!="UNKNOWN":
            raise RuntimeError("SOURCE_INCONNUE_FAUSSEMENT_STOPPED")
        cases["source_lost_shutdown_not_faked"]=True

        unfinished,_,_=build_entry(role="WEB",case="web-unfinished",driver_factory=None,
            flags={},process_reference="process:web-unfinished",drain_seconds=1)
        unfinished_host=unfinished.build_asgi()
        unfinished_life=Life(unfinished_host)
        if (await unfinished_life.start())["type"]!="lifespan.startup.complete":
            raise RuntimeError("WEB_UNFINISHED_START_ECHEC")
        holders["started"],holders["release"]=asyncio.Event(),asyncio.Event()
        late=asyncio.create_task(request(unfinished_host,"/slow"))
        await asyncio.wait_for(holders["started"].wait(),timeout=10)
        stopped_message=await unfinished_life.stop()
        unknown=await inspect(unfinished)
        if stopped_message["type"]!="lifespan.shutdown.failed" or unknown.stop_state!="UNKNOWN" or unknown.inflight_count!=1:
            raise RuntimeError("HTTP_DRAIN_EXPIRE_FAUX_SUCCES")
        cases["unfinished_http_drain_failed_unknown"]=True
        holders["release"].set()
        await late
        after=await inspect(unfinished)
        if after.stop_state!="UNKNOWN" or after.inflight_count!=0:
            raise RuntimeError("HTTP_TARDIF_A_REECRIT_UNKNOWN_EN_STOPPED")
        cases["late_http_completion_does_not_rewrite_unknown"]=True
    asyncio.run(async_cases())
    return cases


class TestC09EntryWebPostgres(unittest.TestCase):
    def test_real(self):
        code=("import json;import test_c09_entry_web_postgres as m;import c09_pg_delivery_support as h;"
              "print(json.dumps(h.run_real("+repr(str(_ROOT))+",m.scenarios)))")
        try:
            proc=subprocess.run([sys.executable,"-B","-c",code],cwd=str(_ROOT),env=_ENV,
                                 timeout=180,capture_output=True,text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode,0,"PROCESSUS_RECETTE_ECHEC")
        payload=None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload=json.loads(line)
        self.assertIsNotNone(payload,"RESULTAT_ABSENT")
        print("C09_ENTRY_WEB_PG "+json.dumps(payload,sort_keys=True))
        self.assertTrue(payload.get("real_pg"),"PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"),"NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"),"FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases",{})),set(_EXPECTED),"CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()),"CAS_NON_VALIDES")


if __name__=="__main__":
    unittest.main()
