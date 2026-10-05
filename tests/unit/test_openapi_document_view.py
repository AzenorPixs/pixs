"""Unit tests OpenAPI document view, no Django configured in parent."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}


def _run(code: str, arg: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, arg],
        timeout=30,
        capture_output=True,
        text=True,
        env=_ENV,
        cwd=str(_ROOT),
    )


_PURE_IMPORT_CODE = textwrap.dedent(r'''
    import sys
    import os
    import importlib.abc
    from pathlib import Path
    from unittest import mock
    src = sys.argv[1]
    sys.path.insert(0, src)

    class BlockDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == "django" or name.startswith("django."):
                raise ImportError("Django blocked in pure import")
            return None

    sys.meta_path.insert(0, BlockDjango())
    guard = mock.Mock(side_effect=AssertionError("filesystem access at import"))
    with (
        mock.patch.object(os, "open", guard),
        mock.patch.object(os, "scandir", guard),
        mock.patch.object(Path, "open", guard),
        mock.patch.object(Path, "read_bytes", guard),
    ):
        import pixs.backend.openapi_document_view as view
        assert tuple(view.__all__) == ("OpenapiDocumentError", "build_openapi_view")
    assert "django" not in sys.modules
    assert guard.call_count == 0
    print("PUR")
''')


_VALID_CODE = textwrap.dedent(r'''
import sys,json
from unittest import mock
sys.path.insert(0,sys.argv[1])
from django.conf import settings
settings.configure(DEFAULT_CHARSET="utf-8",LOGGING_CONFIG=None)
from pixs.backend.api import ApiContractPlan
from pixs.kernel.contracts import ContractCategory,ContractDescriptor
from pixs.backend.openapi_document_view import build_openapi_view

class Request:
    def __init__(self,method):
        self.method=method

def plan_for(version):
    return ApiContractPlan(ContractDescriptor("pixs.contract.synthetic.status",ContractCategory.API,version,"pixs.backend","Synthetic guarantees."),"pixs.api.synthetic.status.v1")

def document_for(version,prefix):
    schema={"type":"object","required":["data","meta","links"],"properties":{
        "data":{"type":"object","required":["status"],"properties":{"status":{"type":"string"}}},
        "meta":{"type":"object","properties":{"signal":{"enum":[True,1,False,0]}}},
        "links":{"type":"object"}}}
    operation={"responses":{"200":{"description":"Status.","content":{"application/json":{"schema":schema}}}}}
    return json.dumps({"openapi":"3.1.0","info":{"title":"Synthetic café","version":version},
        "security":[],"paths":{prefix+"/status":{"get":operation}}},ensure_ascii=False)

for version,prefix in (("1.0.0","/api/v1"),("0.9.0","/api/v0"),("2.3.1","/api/v2")):
    document=document_for(version,prefix)
    first=build_openapi_view(plan_for(version),document)
    second=build_openapi_view(plan_for(version),document)
    assert first is not second
    assert first(Request("GET")).content==second(Request("GET")).content==document.encode("utf-8")

plan=plan_for("1.0.0")
document=document_for("1.0.0","/api/v1")
handler=build_openapi_view(plan,document)
guard=mock.Mock(side_effect=AssertionError("per-request document parse"))
with mock.patch.object(json,"loads",guard):
    get=handler(Request("GET"))
    head=handler(Request("HEAD"))
    assert get.status_code==head.status_code==200
    assert get.content==document.encode("utf-8") and head.content==b""
    assert get["Content-Length"]==head["Content-Length"]==str(len(document.encode("utf-8")))
    for response in (get,head):
        assert response["Content-Type"]=="application/json; charset=utf-8"
        assert response["Cache-Control"]=="no-store"
    for method in ("POST","DELETE","OPTIONS","get"):
        denied=handler(Request(method))
        assert denied.status_code==405 and denied.content==b""
        assert denied["Allow"]=="GET, HEAD" and denied["Cache-Control"]=="no-store"
assert guard.call_count==0

exact=document+" "*(65536-len(document.encode("utf-8")))
assert len(exact.encode("utf-8"))==65536
bound=build_openapi_view(plan,exact)
assert bound(Request("GET")).content==exact.encode("utf-8")
assert bound(Request("HEAD"))["Content-Length"]=="65536"
trailing=json.loads(document)
trailing["paths"]["/api/v1/status/"]=trailing["paths"].pop("/api/v1/status")
build_openapi_view(plan,json.dumps(trailing))
print("VALID")
''')


_REFUSED_CODE = textwrap.dedent(r'''
import sys,json,copy
sys.path.insert(0,sys.argv[1])
from pixs.backend.api import ApiContractPlan
from pixs.kernel.contracts import ContractCategory,ContractDescriptor
from pixs.backend.openapi_document_view import OpenapiDocumentError,build_openapi_view
plan=ApiContractPlan(ContractDescriptor("pixs.contract.synthetic.status",ContractCategory.API,"1.0.0","pixs.backend","Synthetic guarantees."),"pixs.api.synthetic.status.v1")

def document_dict():
    schema={"type":"object","properties":{"status":{"type":"string"}},"required":["status"]}
    operation={"responses":{"200":{"description":"Status.","content":{"application/json":{"schema":schema}}}}}
    return {"openapi":"3.1.0","info":{"title":"Synthetic Status","version":"1.0.0"},"security":[],"paths":{"/api/v1/status":{"get":operation}}}

def operation(doc):
    return doc["paths"]["/api/v1/status"]["get"]

def schema(doc):
    return operation(doc)["responses"]["200"]["content"]["application/json"]["schema"]

def refused(text,target=plan):
    try:
        build_openapi_view(target,text)
    except OpenapiDocumentError as error:
        assert str(error)=="Invalid OpenAPI document."
        assert error.__cause__ is None
        assert "RAW_" not in str(error)
    else:
        raise AssertionError("invalid construction accepted")

def bad_case(mutate):
    doc=document_dict()
    mutate(doc)
    refused(json.dumps(doc))

valid=json.dumps(document_dict())

class HostilePlan:
    def __getattribute__(self,name):
        raise AssertionError("RAW_PLAN_ACCESS")
    def __repr__(self):
        raise AssertionError("RAW_REPR")

class HostileText(str):
    def __len__(self):
        raise AssertionError("RAW_LENGTH")
    def __eq__(self,other):
        raise AssertionError("RAW_COMPARE")
    def __repr__(self):
        raise AssertionError("RAW_REPR")

class PlanSubclass(ApiContractPlan):
    pass

forged=object.__new__(ApiContractPlan)
object.__setattr__(forged,"contract","not-a-descriptor")
object.__setattr__(forged,"openapi_document_ref","pixs.api.synthetic.status.v1")
subclass=object.__new__(PlanSubclass)
object.__setattr__(subclass,"contract",plan.contract)
object.__setattr__(subclass,"openapi_document_ref",plan.openapi_document_ref)
for bad in (None,123,"x",HostilePlan(),forged,subclass):
    refused(valid,bad)

for text in (None,123,b"x","",HostileText(valid),valid+" "*(65537-len(valid.encode())), "{invalid","[NaN]","[Infinity]"):
    refused(text)
bad_case(lambda d:d["info"].update({"title":"é"*33000}))
bad_case(lambda d:d["info"].update({"title":chr(0xD800)}))
bad_case(lambda d:d["info"].update({chr(0xD800):"x"}))
refused(valid.replace("Synthetic Status",chr(0xD800)))
refused(valid.replace('"title": "Synthetic Status"','"title": "Synthetic Status", "title": "RAW_DUPLICATE"'))
overflow=document_dict()
schema(overflow)["enum"]=[99.25]
refused(json.dumps(overflow).replace("99.25","1e999"))

deep={"type":"string"}
for _ in range(40):
    deep={"type":"object","properties":{"n":deep}}
too_deep=document_dict()
operation(too_deep)["responses"]["200"]["content"]["application/json"]["schema"]=deep
refused(json.dumps(too_deep))

for path in ("/api/v2/status","/api/v10/status","/api/v1","/api/v1/","/api/v1//s","/api/v1/.s","/api/v1/s.","/api/v1/..","/api/v1/s..x","/api/v1/%2e","/api/v1/{id}","/api/v1/s?x","/api/v1/s#x","/api/v1/s x","/api/v1/s\\x","/api/v1/é"):
    doc=document_dict()
    doc["paths"]={path:next(iter(doc["paths"].values()))}
    refused(json.dumps(doc))

for mutate in (
    lambda d:d.update({"openapi":"3.1.1"}),
    lambda d:d["info"].update({"version":"1.0.1"}),
    lambda d:d["info"].update({"title":""}),
    lambda d:d.update({"security":[{}]}),
    lambda d:d.update({"servers":[]}),
    lambda d:d.update({"unexpected":True}),
    lambda d:d.update({"paths":{}}),
    lambda d:d["paths"].update({"/api/v1/empty":{}}),
    lambda d:operation(d).update({"summary":123}),
    lambda d:operation(d).update({"description":[]}),
    lambda d:operation(d).update({"operationId":""}),
    lambda d:operation(d).update({"responses":{}}),
    lambda d:operation(d).update({"responses":{"bad":{"description":"D."}}}),
    lambda d:operation(d).update({"responses":{"099":{"description":"D."}}}),
    lambda d:operation(d).update({"responses":{"600":{"description":"D."}}}),
    lambda d:operation(d)["responses"]["200"].update({"description":123}),
    lambda d:operation(d)["responses"]["200"].update({"content":{"text/plain":{"schema":{}}}}),
    lambda d:schema(d).update({"type":"unknown"}),
    lambda d:schema(d).update({"enum":[]}),
    lambda d:schema(d).update({"enum":[1,1.0]}),
    lambda d:schema(d).update({"enum":[True,True]}),
    lambda d:schema(d).update({"required":["status","status"]}),
    lambda d:schema(d).update({"$ref":"https://invalid.example/schema"}),
    lambda d:schema(d).update({"$ref":"#/components/schemas/X"}),
    lambda d:schema(d).update({"items":123}),
    lambda d:schema(d).update({"properties":[]}),
    lambda d:schema(d).update({"format":123}),
    lambda d:schema(d).update({"unexpected":True}),
):
    bad_case(mutate)

duplicate=document_dict()
operation(duplicate)["operationId"]="same-operation"
duplicate["paths"]["/api/v1/second"]={"get":copy.deepcopy(operation(duplicate))}
refused(json.dumps(duplicate))

class Request:
    def __init__(self,method):
        self.method=method

class HostileGetter:
    @property
    def method(self):
        raise ValueError("RAW_HOSTILE_METHOD_MARKER")

handler=build_openapi_view(plan,valid)
for request in (HostileGetter(),Request(HostileText("GET")),Request(None),Request(123),None):
    try:
        handler(request)
    except OpenapiDocumentError as error:
        assert str(error)=="Invalid OpenAPI document." and error.__cause__ is None
    else:
        raise AssertionError("hostile method accepted")
print("REFUSED")
''')


class OpenapiDocumentViewUnitTests(unittest.TestCase):
    def test_pure_import_without_fs(self):
        result = _run(_PURE_IMPORT_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PUR", result.stdout)

    def test_valid_document_served(self):
        result = _run(_VALID_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_refused_documents(self):
        result = _run(_REFUSED_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
