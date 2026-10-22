"""Contrats Core HTTP 1.0.0 : documents bornés, schémas fermés et recettes de concordance."""
from __future__ import annotations

import copy
import hashlib
import json
import re

from pixs.backend.api import ApiContractPlan, api_major_prefix
from pixs.backend.api_core_catalog import COMMANDS, QUERIES, API_UUID7_PATTERN, command_schema
from pixs.backend.api_core_errors_catalog import error_schema
from pixs.backend.openapi_document_view import (
    OpenapiDocumentError, _bounded_json_document, _preloaded_json_view,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor

__all__ = ["CORE_API_VERSION", "core_api_contract_plan", "build_core_openapi_documents",
           "validate_core_openapi_document", "build_core_openapi_view", "validate_core_api_response"]

CORE_API_VERSION = "1.0.0"
_MAX_SIZE = 65536
_SCHEMA_KEYS = frozenset(("type","properties","required","additionalProperties","items","enum",
    "const","format","pattern","minimum","maximum","minLength","maxLength","minItems","maxItems",
    "uniqueItems","default","description","anyOf","oneOf","allOf","$ref"))
_METHODS = frozenset(("get","post","head"))
_ROOTS = {"P":"/platform","T":"/tenants/{tenant_id}","S":"/tenants/{tenant_id}/scopes/{scope_id}"}


def _invalid():
    raise OpenapiDocumentError("Document OpenAPI Core invalide.")


def _dump(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)


def core_api_contract_plan():
    return ApiContractPlan(ContractDescriptor("pixs.core.api",ContractCategory.API,CORE_API_VERSION,
        "pixs.core","Contrat Core HTTP public versionné, identité/autorisation propriétaires réévaluées."),
        "pixs-core-api-v1")


def _object(properties, required=None):
    return {"type":"object","additionalProperties":False,"properties":properties,
            "required":list(properties) if required is None else list(required)}


def _reference(name):
    return {"$ref":"#/components/schemas/"+name}


def _nullable(schema):
    return {"anyOf":[schema,{"type":"null"}]}


def _schemas(composition):
    from pixs.core.authz.policy import IdentityAssurance, AuthenticationAssurance, FederationTrust
    from pixs.core.identity.models import IdentityState, IdentityType
    from pixs.kernel.data_persistence_states import DataPersistenceState
    from pixs.kernel.data_retention_states import DataRetentionState
    limits=composition.input_limits
    text={"type":"string","minLength":1}
    uuid7={"type":"string","pattern":API_UUID7_PATTERN}
    correlation={"type":"string","minLength":1,"maxLength":128}
    context=_object({"scope_type":{"type":"string","enum":["PLATFORM","TENANT"]},
                     "tenant_id":_nullable(text),"scope_id":_nullable(text)})
    meta=_object({"correlation_id":correlation,"context":_reference("ScopeContext")})
    page_meta=_object({**meta["properties"],"page_size":{"type":"integer","minimum":1,
                                                        "maximum":composition.limits.max_page_size}})
    mutation=_object({"operation_id":text,"result_ref":text,"version":{"type":"integer","minimum":1},
                      "persistence_state":{"type":"string","enum":[v.value for v in DataPersistenceState]},
                      "correlation_id":correlation})
    scalar={"anyOf":[{"type":"string","minLength":1},{"type":"integer"}]}
    policy_fields={"policy_id":text,"policy_version":text,"owner":text,
        "effect":{"type":"string","enum":["ALLOW","DENY"]},
        "scope":_object({"contexts":{"type":"array","items":_reference("ScopeContext"),"minItems":1,"maxItems":limits.max_collection_items}}),
        "conditions":{"type":"array","items":{"oneOf":[
            _object({"attr":text,"op":{"type":"string","const":"eq"},"value":scalar}),
            _object({"attr":text,"op":{"type":"string","const":"in"},"value":{"oneOf":[
                {"type":"array","items":{"type":"string","minLength":1},"minItems":1,"maxItems":limits.max_collection_items},
                {"type":"array","items":{"type":"integer"},"minItems":1,"maxItems":limits.max_collection_items}]}})]},
            "maxItems":limits.max_collection_items},
        "obligations":{"type":"array","items":_object({"kind":{"type":"string","const":"AUDIT"}}),"maxItems":limits.max_collection_items},
        "valid_from":_nullable({"type":"string","format":"date-time"}),
        "valid_until":_nullable({"type":"string","format":"date-time"}),
        "min_identity_assurance":_nullable({"type":"string","enum":[v.value for v in IdentityAssurance]}),
        "min_authentication_assurance":_nullable({"type":"string","enum":[v.value for v in AuthenticationAssurance]}),
        "min_federation_trust":_nullable({"type":"string","enum":[v.value for v in FederationTrust]}),
        "max_auth_age_seconds":_nullable({"type":"integer","minimum":1})}
    for name in ("subject","resource","action"):
        policy_fields[name]=_object({"kind":{"type":"string","const":name},
            "values":{"type":"array","items":text,"minItems":1,"maxItems":limits.max_collection_items}})
    activity={"oneOf":[
        _object({"status":{"type":"string","enum":["RECORDED","REPLAY_IGNORED"]}}),
        _object({"status":{"type":"string","const":"NOT_RECORDED"},"error_code":error_schema()["properties"]["error_code"]})]}
    mutation_meta=_object({**meta["properties"],"activity":activity},("correlation_id","context"))
    schemas={"Error":error_schema(),"ScopeContext":context,"Meta":meta,"PageMeta":page_meta,"MutationMeta":mutation_meta,
             "Mutation":mutation,"CorePolicy":_object(policy_fields)}
    schemas["MutationEnvelope"]=_object({"data":_reference("Mutation"),"meta":_reference("MutationMeta"),"links":_object({})})
    attributes={
        "USER":{"user_id":uuid7},
        "IDENTITY":{"identity_id":uuid7,"identity_type":{"type":"string","enum":[v.value for v in IdentityType]},
                    "state":{"type":"string","enum":[v.value for v in IdentityState]}},
        "LINK":{"user_id":uuid7,"identity_id":uuid7},
        "GROUP":{"group_id":uuid7,"scope_type":context["properties"]["scope_type"],
                 "tenant_id":_nullable(text),"scope_id":_nullable(text)},
        "USER_GROUP":{"user_id":uuid7,"group_id":uuid7},
        "TENANT_MEMBERSHIP":{"identity_id":uuid7,"tenant_id":text,"activation":{"type":"string"}},
        "TENANT":{"tenant_id":text},
        "SCOPE":{"scope_id":text,"tenant_id":text,"parent_scope_id":_nullable(text)},
        "PERMISSION":{"permission_id":text,"owner":text,"resource_ref":text,"action_ref":text},
        "ROLE":{"role_id":text,"scope_type":context["properties"]["scope_type"],
                "tenant_id":_nullable(text),"scope_id":_nullable(text)},
        "ROLE_PERMISSION":{"role_id":text,"permission_id":text},
        "ROLE_ASSIGNMENT":{"role_id":text,"subject_type":{"type":"string","enum":["USER","IDENTITY","GROUP"]},
             "subject_ref":uuid7,"scope_type":context["properties"]["scope_type"],"tenant_id":_nullable(text),"scope_id":_nullable(text)},
        "POLICY":{"policy_id":text,"policy_version":text,"owner":text,"effect":{"type":"string","enum":["ALLOW","DENY"]},
                  "definition":_reference("CorePolicy")},
        "BINDING":{"installation_ref":text,"identity_id":uuid7},
        "GRANT":{"installation_ref":text,"tenant_id":text},
    }
    for kind,fields in attributes.items():
        item=_object({"kind":{"type":"string","const":kind},"ref":text,"context":_reference("ScopeContext"),
            "version":{"type":"integer","minimum":1},
            "persistence_state":{"type":"string","enum":[v.value for v in DataPersistenceState]},
            "retention_state":{"type":"string","enum":[v.value for v in DataRetentionState]},
            "governance_ref":_nullable(text),"confidentiality":_nullable({"type":"string"}),
            "personal":_nullable({"type":"string"}),"attributes":_object(fields)})
        schemas["Page"+kind]=_object({"data":{"type":"array","items":item,"maxItems":composition.limits.max_page_size},
            "meta":_reference("PageMeta"),"links":_object({"next":{"type":"string","minLength":1}},())})
    instant={"type":"string","format":"date-time"}
    session=_object({"id":uuid7,"authenticated_at":instant,"idle_expires_at":instant,"absolute_expires_at":instant})
    auth=_object({"outcome":{"type":"string"},"audit":{"type":"string"},"operation_id":text,
        "session":session,"credential":{"type":"string"},"pending_audit_ref":text,
        "access_token":{"type":"string","minLength":1},"refresh_token":{"type":"string","minLength":1},
        "token_type":{"type":"string","const":"Bearer"}},("outcome","audit","operation_id"))
    schemas["AuthEnvelope"]=_object({"data":auth,"meta":_reference("Meta"),"links":_object({})})
    schemas["CsrfEnvelope"]=_object({"data":_object({"csrf_token":{"type":"string","minLength":1}}),
                                  "meta":_reference("Meta"),"links":_object({})})
    schemas["PublicDocument"]={"type":"object"}
    return schemas


def _schemes():
    return {
        "BearerAccess":{"type":"http","scheme":"bearer","bearerFormat":"C03 ACCESS"},
        "BearerRefresh":{"type":"http","scheme":"bearer","bearerFormat":"C03 REFRESH"},
        "WebSession":{"type":"apiKey","in":"cookie","name":"__Host-pixs-session"},
    }


def _parameter(name, location, schema, required):
    return {"name":name,"in":location,"required":required,"schema":schema}


def _operation(composition, *, mode, web, response, body=None, login=False, renew=False, query=False, csrf=False):
    text={"type":"string","minLength":1,"maxLength":composition.input_limits.max_reference_chars}
    parameters=[_parameter("X-Correlation-ID","header",{"type":"string","minLength":1,"maxLength":128},False)]
    if mode in ("T","S"):
        parameters.append(_parameter("tenant_id","path",text,True))
    if mode=="S":
        parameters.append(_parameter("scope_id","path",text,True))
    if body is not None:
        parameters.append(_parameter("Idempotency-Key","header",text,True))
        if web:
            parameters.extend([_parameter("Origin","header",{"type":"string","const":composition.approved_origin},True),
                               _parameter("X-CSRFToken","header",{"type":"string","minLength":1},True)])
    if query:
        parameters.extend([
            _parameter("limit","query",{"type":"integer","minimum":1,"maximum":composition.limits.max_page_size,
                                       "default":composition.limits.default_page_size},False),
            _parameter("cursor","query",{"type":"string","minLength":1,"maxLength":composition.cursor_codec.config.max_cursor_chars},False),
            {**_parameter("ref","query",{"type":"array","items":text,"maxItems":composition.input_limits.max_collection_items,
                                        "uniqueItems":True},False),"style":"form","explode":True},
        ])
    responses={"200":{"description":"Résultat propriétaire confirmé.","content":{"application/json":{"schema":_reference(response)}}}}
    for status in ("400","401","403","404","405","409","413","500","503"):
        responses[status]={"description":"Refus public stable.","content":{"application/json":{"schema":_reference("Error")}}}
    operation={"parameters":parameters,"security":[] if login or csrf else [
        {"WebSession" if web else "BearerRefresh" if renew else "BearerAccess":[]}],
        "responses":responses}
    if body is not None:
        operation["requestBody"]={"required":True,"content":{"application/json":{"schema":body}}}
    return operation


def _prune(paths, schemas):
    used=set()
    def visit(node):
        if type(node) is dict:
            if "$ref" in node:
                name=node["$ref"].removeprefix("#/components/schemas/")
                if name not in schemas:
                    _invalid()
                if name not in used:
                    used.add(name);visit(schemas[name])
            else:
                for value in node.values():visit(value)
        elif type(node) is list:
            for value in node:visit(value)
    visit(paths)
    return {name:schemas[name] for name in sorted(used)}


def _document(plan, paths, schemas, *, index=None):
    root={"openapi":"3.1.0","info":{"title":"Pixs Core HTTP","version":plan.contract.version},
          "paths":paths,"components":{"schemas":_prune(paths,schemas),"securitySchemes":_schemes()}}
    if index is not None:
        root["x-documents"]=index
    return _dump(root)


def build_core_openapi_documents(composition):
    """Retourne (chemin, JSON) immuables ; aucun accès disque, clé ou serveur."""
    from pixs.backend.api_core_composition import CoreApiComposition
    if type(composition) is not CoreApiComposition:
        _invalid()
    composition.__post_init__()
    plan=core_api_contract_plan();prefix=api_major_prefix(plan)
    schemas=_schemas(composition)
    capabilities={}
    for web in (False,True):
        for mode,root in _ROOTS.items():
            base=prefix+("/web" if web else "")+root
            for name,spec in COMMANDS.items():
                if mode not in spec["roots"]:continue
                action=spec["action"].split(".")[2]
                capabilities.setdefault(action,{})[base+"/commands/"+name]={"post":_operation(
                    composition,mode=mode,web=web,response="MutationEnvelope",
                    body=command_schema(name,root_mode=mode,limits=composition.input_limits))}
            for name,spec in QUERIES.items():
                if mode not in spec["roots"]:continue
                capabilities.setdefault(spec["domain"],{})[base+"/"+name]={"get":_operation(
                    composition,mode=mode,web=web,response="Page"+spec["kind"],query=True)}
            text={"type":"string","minLength":1,"maxLength":composition.input_limits.max_reference_chars}
            password={"type":"string","minLength":1,"maxLength":composition.limits.max_payload_bytes}
            auth_bodies={
                "login":_object({"external_subject":text,"password":password,
                    "replace_session_id":_nullable({"type":"string","pattern":API_UUID7_PATTERN})},("external_subject","password")),
                "logout":_object({}),"revoke-all":_object({}),
                "revoke-session":_object({"session_id":{"type":"string","pattern":API_UUID7_PATTERN}}),
                "change-password":_object({"new_password":password}),
            }
            if mode!="P":
                auth_bodies.pop("revoke-all")
                auth_bodies.pop("change-password")
            if not web:auth_bodies["renew"]=_object({})
            for name,body in auth_bodies.items():
                capabilities.setdefault("auth",{})[base+"/auth/"+name]={"post":_operation(composition,
                    mode=mode,web=web,response="AuthEnvelope",body=body,login=name=="login",renew=name=="renew")}
    capabilities.setdefault("auth",{})[prefix+"/web/auth/csrf"]={"get":_operation(composition,
        mode="P",web=True,response="CsrfEnvelope",csrf=True)}
    documents=[]
    for capability,paths in sorted(capabilities.items()):
        chunk={};number=1
        for path,methods in sorted(paths.items()):
            candidate={**chunk,path:methods}
            if len(_document(plan,candidate,schemas).encode("utf-8"))>_MAX_SIZE:
                if not chunk:_invalid()
                documents.append((prefix+"/openapi/"+capability+"-"+str(number)+".json",_document(plan,chunk,schemas)))
                number+=1;chunk={path:methods}
            else:chunk=candidate
        if chunk:
            document=_document(plan,chunk,schemas)
            if len(document.encode("utf-8"))>_MAX_SIZE:_invalid()
            documents.append((prefix+"/openapi/"+capability+"-"+str(number)+".json",document))
    doc_operation={"parameters":[],"security":[],"responses":{
        "200":{"description":"Document public borné.","content":{"application/json":{"schema":_reference("PublicDocument")}}},
        "403":{"description":"Transport ou origine refusé.","content":{"application/json":{"schema":_reference("Error")}}},
        "405":{"description":"Méthode non admise, corps vide."}}}
    index_paths={prefix+"/openapi.json":{"get":copy.deepcopy(doc_operation),"head":copy.deepcopy(doc_operation)}}
    for path,_ in documents:
        index_paths[path]={"get":copy.deepcopy(doc_operation),"head":copy.deepcopy(doc_operation)}
    index=[{"href":path,"sha256":hashlib.sha256(doc.encode("utf-8")).hexdigest(),"bytes":len(doc.encode("utf-8"))}
           for path,doc in documents]
    documents.insert(0,(prefix+"/openapi.json",_document(plan,index_paths,schemas,index=index)))
    for _,document in documents:
        validate_core_openapi_document(plan,document)
    return tuple(documents)


def _schema(node, names, depth=0):
    if depth>32 or type(node) is not dict or not set(node)<=_SCHEMA_KEYS:
        _invalid()
    if "$ref" in node:
        if set(node)!={"$ref"} or node["$ref"] not in {"#/components/schemas/"+n for n in names}:
            _invalid()
        return
    if "type" in node:
        declared=node["type"] if type(node["type"]) is list else [node["type"]]
        if (not declared or any(type(t) is not str or t not in
                ("object","array","string","integer","number","boolean","null") for t in declared)
                or len(set(declared))!=len(declared)):
            _invalid()
    props=node.get("properties",{})
    if type(props) is not dict or any(type(k) is not str or not k for k in props):
        _invalid()
    for value in props.values():_schema(value,names,depth+1)
    required=node.get("required",[])
    if type(required) is not list or len(set(required))!=len(required) or not set(required)<=set(props):
        _invalid()
    if "additionalProperties" in node and type(node["additionalProperties"]) is not bool:
        _invalid()
    if "items" in node:_schema(node["items"],names,depth+1)
    for keyword in ("anyOf","oneOf","allOf"):
        if keyword in node:
            if type(node[keyword]) is not list or not node[keyword]:_invalid()
            for item in node[keyword]:_schema(item,names,depth+1)
    for keyword in ("minLength","maxLength","minItems","maxItems"):
        if keyword in node and (type(node[keyword]) is not int or node[keyword]<0):_invalid()
    for keyword in ("minimum","maximum"):
        if keyword in node and type(node[keyword]) not in (int,float):_invalid()
    if "enum" in node and (type(node["enum"]) is not list or not node["enum"]):_invalid()
    for keyword in ("pattern","format","description"):
        if keyword in node and type(node[keyword]) is not str:_invalid()
    if "uniqueItems" in node and type(node["uniqueItems"]) is not bool:_invalid()
    if "pattern" in node:
        try:re.compile(node["pattern"])
        except re.error:_invalid()


def validate_core_openapi_document(plan, document):
    """Valide notre vocabulaire OpenAPI/JSON Schema fermé, sans bibliothèque nouvelle."""
    try:
        prefix=api_major_prefix(plan)
        _,root=_bounded_json_document(document,local_references=True)
        if (type(root) is not dict or set(root)-{"openapi","info","paths","components","x-documents"}
                or root.get("openapi")!="3.1.0" or type(root.get("info")) is not dict
                or set(root["info"])!={"title","version"} or type(root["info"]["title"]) is not str
                or not root["info"]["title"] or root["info"]["title"].strip()!=root["info"]["title"]
                or root["info"]["version"]!=plan.contract.version):
            _invalid()
        components=root.get("components")
        if type(components) is not dict or set(components)!={"schemas","securitySchemes"}:_invalid()
        schemas,schemes=components["schemas"],components["securitySchemes"]
        if type(schemas) is not dict or type(schemes) is not dict or schemes!=_schemes():_invalid()
        for name,node in schemas.items():
            if type(name) is not str or not re.fullmatch("[A-Za-z][A-Za-z0-9_]*",name):_invalid()
            _schema(node,set(schemas))
        paths=root.get("paths")
        if type(paths) is not dict or not paths:_invalid()
        for path,methods in paths.items():
            if type(path) is not str or not path.startswith(prefix+"/"):_invalid()
            parameters=set()
            for segment in path[len(prefix)+1:].split("/"):
                if re.fullmatch(r"\{(?:tenant_id|scope_id)\}",segment):
                    parameters.add(segment[1:-1])
                elif not re.fullmatch(r"[A-Za-z0-9_-]+(?:[.][A-Za-z0-9_-]+)*",segment):_invalid()
            if type(methods) is not dict or not methods or not set(methods)<=_METHODS:_invalid()
            for method,operation in methods.items():
                if type(operation) is not dict or set(operation)-{"parameters","security","responses","requestBody"}:_invalid()
                security=operation.get("security")
                if type(security) is not list or any(type(r) is not dict or len(r)!=1
                        or any(k not in schemes or v!=[] for k,v in r.items()) for r in security):_invalid()
                params=operation.get("parameters")
                if type(params) is not list:_invalid()
                seen=set();declared=set()
                for parameter in params:
                    if (type(parameter) is not dict or set(parameter)-{"name","in","required","schema","style","explode"}
                            or not {"name","in","required","schema"}<=set(parameter)
                            or parameter["in"] not in ("path","query","header") or type(parameter["name"]) is not str
                            or not parameter["name"] or type(parameter["required"]) is not bool):_invalid()
                    key=(parameter["in"],parameter["name"].lower() if parameter["in"]=="header" else parameter["name"])
                    if key in seen:_invalid()
                    seen.add(key)
                    if parameter["in"]=="path":
                        if not parameter["required"]:_invalid()
                        declared.add(parameter["name"])
                    if "style" in parameter and (parameter["style"]!="form" or parameter.get("explode") is not True):_invalid()
                    _schema(parameter["schema"],set(schemas))
                if declared!=parameters:_invalid()
                body=operation.get("requestBody")
                if body is not None:
                    if type(body) is not dict or set(body)!={"required","content"} or body["required"] is not True:_invalid()
                    _content(body["content"],schemas)
                responses=operation.get("responses")
                if type(responses) is not dict or "200" not in responses:_invalid()
                for status,response in responses.items():
                    if (type(status) is not str or not re.fullmatch("[1-5][0-9]{2}",status)
                            or type(response) is not dict or set(response)-{"description","content"}
                            or type(response.get("description")) is not str):_invalid()
                    if "content" in response:_content(response["content"],schemas)
        if "x-documents" in root:
            if type(root["x-documents"]) is not list or not root["x-documents"]:_invalid()
            seen=set()
            for item in root["x-documents"]:
                if (type(item) is not dict or set(item)!={"href","sha256","bytes"}
                        or item["href"] not in paths or item["href"] in seen
                        or type(item["sha256"]) is not str or not re.fullmatch("[0-9a-f]{64}",item["sha256"])
                        or type(item["bytes"]) is not int or not 1<=item["bytes"]<=_MAX_SIZE):_invalid()
                seen.add(item["href"])
    except OpenapiDocumentError:
        raise
    except (ValueError,TypeError,KeyError,AttributeError,RecursionError):
        _invalid()
    return root


def _content(content, schemas):
    if type(content) is not dict or set(content)!={"application/json"}:
        _invalid()
    media=content["application/json"]
    if type(media) is not dict or set(media)!={"schema"}:_invalid()
    _schema(media["schema"],set(schemas))


def build_core_openapi_view(plan, document):
    validate_core_openapi_document(plan,document)
    body,_=_bounded_json_document(document,local_references=True)
    return _preloaded_json_view(body)


def _matches(value, schema, components, depth=0):
    if depth>32:return False
    if "$ref" in schema:
        return _matches(value,components[schema["$ref"].removeprefix("#/components/schemas/")],components,depth+1)
    if "anyOf" in schema and not any(_matches(value,s,components,depth+1) for s in schema["anyOf"]):return False
    if "oneOf" in schema and sum(_matches(value,s,components,depth+1) for s in schema["oneOf"])!=1:return False
    if "allOf" in schema and not all(_matches(value,s,components,depth+1) for s in schema["allOf"]):return False
    types={"object":dict,"array":list,"string":str,"integer":int,"number":(int,float),"boolean":bool,"null":type(None)}
    if "type" in schema:
        declared=schema["type"] if type(schema["type"]) is list else [schema["type"]]
        if not any(type(value) in types[t] if type(types[t]) is tuple else type(value) is types[t] for t in declared):
            return False
    if "enum" in schema and not any(type(value) is type(item) and value==item for item in schema["enum"]):return False
    if "const" in schema and (type(value) is not type(schema["const"]) or value!=schema["const"]):return False
    if type(value) is dict:
        props=schema.get("properties",{})
        if set(schema.get("required",()))-set(value):return False
        if schema.get("additionalProperties") is False and set(value)-set(props):return False
        if not all(_matches(value[k],sub,components,depth+1) for k,sub in props.items() if k in value):return False
    if type(value) is list:
        if not schema.get("minItems",0)<=len(value)<=schema.get("maxItems",len(value)):return False
        if schema.get("uniqueItems") and len({_dump(item) for item in value})!=len(value):return False
        if "items" in schema and not all(_matches(item,schema["items"],components,depth+1) for item in value):return False
    if type(value) is str:
        if not schema.get("minLength",0)<=len(value)<=schema.get("maxLength",len(value)):return False
        if "pattern" in schema and re.search(schema["pattern"],value) is None:return False
        if schema.get("format")=="date-time":
            import datetime
            try:
                if datetime.datetime.fromisoformat(value).tzinfo is None:return False
            except ValueError:return False
    if type(value) in (int,float):
        if "minimum" in schema and value<schema["minimum"]:return False
        if "maximum" in schema and value>schema["maximum"]:return False
    return True


def validate_core_api_response(plan, documents, *, path_template, method, response):
    """Concordance de recette avec les octets effectivement publiés ; erreur fixe sans corps."""
    try:
        matches=[]
        for document in documents:
            root=validate_core_openapi_document(plan,document)
            if path_template in root["paths"] and method.lower() in root["paths"][path_template]:
                matches.append((root,root["paths"][path_template][method.lower()]))
        if len(matches)!=1:_invalid()
        root,operation=matches[0]
        specification=operation["responses"].get(str(response.status_code))
        if specification is None:_invalid()
        if method.upper()=="HEAD":
            if response.content:_invalid()
            return True
        content=specification.get("content")
        if content is None:
            if response.content:_invalid()
            return True
        if response.headers.get("Content-Type","").split(";",1)[0]!="application/json":_invalid()
        value=json.loads(response.content.decode("utf-8"))
        if not _matches(value,content["application/json"]["schema"],root["components"]["schemas"]):_invalid()
    except OpenapiDocumentError:
        raise
    except (ValueError,TypeError,KeyError,AttributeError,RecursionError):
        _invalid()
    return True
