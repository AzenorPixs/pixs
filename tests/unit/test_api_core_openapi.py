"""Catalogue C06 : schémas et DTO réellement parsés, sans autorité implicite."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest

from pixs.backend.api_core_catalog import (
    ApiCatalogError, ApiInputLimits, COMMANDS, QUERIES, command_resource_ref,
    command_schema, parse_command_input,
)
from pixs.core.api_core_serializer_v1 import API_CORE_COMMAND_TYPES, canonical_command_bytes
from pixs.core.scope.context import ScopeContext, ScopeType

_U = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f01"
_I = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f02"
_G = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f03"
_P = ScopeContext(ScopeType.PLATFORM)
_T = ScopeContext(ScopeType.TENANT, " t-é ")
_LIMITS = ApiInputLimits(512, 64, 65536, 16)


def parse(name, body, context=_P):
    return parse_command_input(name, body, context=context, correlation_id="server-corr", limits=_LIMITS)


class CoreCatalogTest(unittest.TestCase):
    def test_closed_catalog_matches_owner_command_types(self):
        self.assertEqual(len(COMMANDS), 22)
        self.assertEqual({s["action"] + ":v1" for s in COMMANDS.values()}, set(API_CORE_COMMAND_TYPES))
        self.assertEqual(len(QUERIES), 15)
        self.assertNotIn("TOMBSTONE", {s["kind"] for s in QUERIES.values()})
        with self.assertRaises(TypeError):
            COMMANDS["new-client-command"] = {}
        with self.assertRaises(TypeError):
            COMMANDS["create-user"]["action"] = "client.action"

    def test_twenty_one_wire_commands_and_owner_references(self):
        role = "r/é"
        role_ref = "pixs.core.role:" + role
        assignment = "pixs.core.role-assignment:r%2F%C3%A9/USER/" + _U
        cases = [
            ("create-user", {"user_id": _U}, _P, "pixs.core.user:" + _U),
            ("create-identity", {"identity_id": _I, "identity_type": "HUMAN", "state": "ACTIVE"}, _P, "pixs.core.identity:" + _I),
            ("link-identity", {"user_id": _U, "identity_id": _I}, _P, "pixs.core.identity-link:" + _U + "/" + _I),
            ("unlink-identity", {"user_id": _U, "identity_id": _I, "expected_version": 1}, _P, "pixs.core.identity-link:" + _U + "/" + _I),
            ("set-identity-state", {"identity_id": _I, "state": "SUSPENDED", "expected_version": 1}, _P, "pixs.core.identity:" + _I),
            ("logical-delete-identity", {"resource_ref": "pixs.core.identity:" + _I, "target_state": "SOFT_DELETED", "expected_version": 1}, _P, "pixs.core.identity:" + _I),
            ("create-group", {"group_id": _G}, _T, "pixs.core.group:" + _G),
            ("change-group-persistence", {"resource_ref": "pixs.core.group:" + _G, "target_state": "ARCHIVED", "expected_version": 1}, _T, "pixs.core.group:" + _G),
            ("add-user-group", {"user_id": _U, "group_id": _G}, _T, "pixs.core.user-group:" + _U + "/" + _G),
            ("remove-user-group", {"user_id": _U, "group_id": _G, "expected_version": 1}, _T, "pixs.core.user-group:" + _U + "/" + _G),
            ("activate-tenant-membership", {"identity_id": _I}, _T, "pixs.core.identity-tenant:" + _I + "/ t-é "),
            ("revoke-tenant-membership", {"identity_id": _I, "expected_version": 1}, _T, "pixs.core.identity-tenant:" + _I + "/ t-é "),
            ("create-tenant", {"tenant_id": "nouveau"}, _P, "pixs.core.tenant:nouveau"),
            ("create-scope", {"scope_id": "s-1", "parent_scope_id": None}, _T, "pixs.core.scope:s-1"),
            ("move-scope", {"scope_id": "s-1", "parent_scope_id": None, "expected_version": 1}, _T, "pixs.core.scope:s-1"),
            ("declare-permission", {"permission_id": "perm", "owner_component": "pixs.core", "resource_ref": "resource", "action_ref": "action"}, _P, "pixs.core.permission:perm"),
            ("create-role", {"role_id": role, "permission_ids": ["perm"]}, _T, role_ref),
            ("set-role-permissions", {"role_id": role, "permission_ids": ["perm"], "expected_version": 1}, _T, role_ref),
            ("assign-role", {"role_id": role, "subject_type": "USER", "subject_ref": _U}, _T, assignment),
            ("unassign-role", {"role_id": role, "subject_type": "USER", "subject_ref": _U, "expected_version": 1}, _T, assignment),
            ("change-authz-persistence", {"resource_ref": role_ref, "target_state": "ARCHIVED", "expected_version": 1}, _T, role_ref),
        ]
        for name, body, context, expected in cases:
            with self.subTest(command=name):
                original = copy.deepcopy(body)
                dto = parse(name, body, context)
                self.assertIs(type(dto), COMMANDS[name]["dto"])
                self.assertEqual(dto.correlation_id, "server-corr")
                self.assertEqual(command_resource_ref(name, dto), expected)
                self.assertEqual(body, original)
                self.assertTrue(canonical_command_bytes(command_type=COMMANDS[name]["action"] + ":v1", dto=dto, context=context))

    def test_unknown_and_server_fields_are_rejected(self):
        for key in ("unexpected", "context", "subject_id", "actor", "correlation_id", "request"):
            with self.subTest(field=key), self.assertRaises(ApiCatalogError):
                parse("create-user", {"user_id": _U, key: "client"})
        with self.assertRaises(ApiCatalogError):
            parse("client-selected-method", {"user_id": _U})
        with self.assertRaises(ApiCatalogError):
            parse("create-user", {"user_id": _U}, _T)

    def test_path_tenant_and_server_context_remain_canonical(self):
        value = parse("create-scope", {"scope_id": "s", "parent_scope_id": None, "tenant_id": " t-é "}, _T)
        self.assertEqual(value.tenant_id, " t-é ")
        with self.assertRaises(ApiCatalogError) as error:
            parse("create-scope", {"scope_id": "s", "parent_scope_id": None, "tenant_id": "other"}, _T)
        self.assertEqual(error.exception.code, "API_TENANT_MISMATCH")
        group = parse("create-group", {"group_id": _G}, _T)
        self.assertIs(group.context, _T)

    def test_uuid_version_enum_and_strict_integer(self):
        for value in (_U.upper(), _U.replace("-7a11-", "-4a11-"), 42):
            with self.assertRaises(ApiCatalogError):
                parse("create-user", {"user_id": value})
        for value in (True, 0, -1, "1", 1.0):
            with self.assertRaises(ApiCatalogError):
                parse("set-identity-state", {"identity_id": _I, "state": "ACTIVE", "expected_version": value})
        with self.assertRaises(ApiCatalogError):
            parse("create-identity", {"identity_id": _I, "identity_type": "CLIENT", "state": "ACTIVE"})

    def test_nullable_default_and_operation_specific_cas(self):
        role = parse("create-role", {"role_id": "r", "permission_ids": [], "expected_version": None}, _T)
        self.assertIsNone(role.expected_version)
        for body in ({"role_id": "r", "permission_ids": []},
                     {"role_id": "r", "permission_ids": [], "expected_version": None}):
            with self.assertRaises(ApiCatalogError):
                parse("set-role-permissions", body, _T)
        schema = command_schema("set-role-permissions", root_mode="T", limits=_LIMITS)
        self.assertIn("expected_version", schema["required"])
        self.assertEqual(schema["properties"]["expected_version"]["type"], "integer")

    def test_schema_server_fields_and_path_tenant(self):
        for name, spec in COMMANDS.items():
            for root in spec["roots"]:
                schema = command_schema(name, root_mode=root, limits=_LIMITS)
                self.assertFalse(schema["additionalProperties"])
                self.assertNotIn("context", schema["properties"])
                self.assertNotIn("correlation_id", schema["properties"])
                json.dumps(schema)
        scope = command_schema("create-scope", root_mode="T", limits=_LIMITS)
        self.assertNotIn("tenant_id", scope["required"])
        self.assertEqual(scope["properties"]["parent_scope_id"]["type"], ["string", "null"])

    def test_foreign_objects_are_rejected_before_methods(self):
        calls = []
        class Foreign:
            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("METHODE_ETRANGERE")
            def __str__(self):
                calls.append("str")
                raise AssertionError("METHODE_ETRANGERE")
        for name, body, context in ((Foreign(), {}, _P), ("create-user", {"user_id": Foreign()}, _P),
                                    ("create-user", {"user_id": _U}, Foreign())):
            with self.assertRaises(ApiCatalogError):
                parse(name, body, context)
        with self.assertRaises(ApiCatalogError):
            command_resource_ref("create-user", Foreign())
        self.assertEqual(calls, [])

    def test_complete_policy_owner_codec_in_fresh_process(self):
        script = """
import datetime,json
from django.conf import settings
settings.configure(DEFAULT_CHARSET='utf-8', INSTALLED_APPS=['pixs.backend.apps.PixsCoreConfig'],
                   SECRET_KEY='vecteur-public-synthetique', DATABASES={}, LOGGING_CONFIG=None, USE_TZ=True)
import django
django.setup()
from pixs.core.authz.policy import Policy,Effect,Selector,ScopeSelector,Condition,Obligation,IdentityAssurance,AuthenticationAssurance,FederationTrust
from pixs.core.scope.context import ScopeContext,ScopeType
from pixs.core.persistence.models_authz import encode_policy
from pixs.backend.api_core_catalog import ApiInputLimits,parse_command_input,command_resource_ref
ctx=ScopeContext(ScopeType.PLATFORM)
policy=Policy('policy/é','1.0.0','pixs.core',Effect.ALLOW,Selector('subject',('u',)),
              Selector('resource',('r',)),Selector('action',('a',)),ScopeSelector((ctx,)),
              conditions=(Condition('tenant','eq','tenant-a'),),obligations=(Obligation('AUDIT'),),
              valid_from=datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc),
              valid_until=datetime.datetime(2026,2,1,tzinfo=datetime.timezone.utc),
              min_identity_assurance=IdentityAssurance.VERIFIED,
              min_authentication_assurance=AuthenticationAssurance.MULTI_FACTOR,
              min_federation_trust=FederationTrust.TRUSTED,max_auth_age_seconds=60)
dto=parse_command_input('persist-policy',{'policy':json.loads(encode_policy(policy))},context=ctx,
                        correlation_id='server',limits=ApiInputLimits(512,64,65536,16))
assert dto.policy==policy
assert command_resource_ref('persist-policy',dto)=='pixs.core.policy:policy%2F%C3%A9/1.0.0'
print('POLICY_CATALOG_OK')
"""
        result = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True,
                                env={"PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "POLICY_CATALOG_OK")




def documentation_composition():
    """Composition de schéma seulement : tout appel propriétaire serait un échec."""
    import datetime
    from pixs.auth.api_request_source import ApiRequestSource
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.backend.api_core_composition import CoreApiComposition, CoreHttpLimits
    from pixs.backend.api_core_pagination import CoreCursorCodec, CoreCursorConfig
    from pixs.core.audit_sink import PostgresAuditParticipant
    class Clock:
        def now(self):
            return datetime.datetime.now(datetime.timezone.utc)
    class ClosedPort:
        def resolve(self, **kwargs):
            raise AssertionError("APPEL_PROPRIETAIRE_INTERDIT_DANS_RECETTE_DOCUMENT")
        def current_profile(self, context):
            raise AssertionError("APPEL_PROPRIETAIRE_INTERDIT_DANS_RECETTE_DOCUMENT")
        def read_facts(self, *args, **kwargs):
            raise AssertionError("APPEL_PROPRIETAIRE_INTERDIT_DANS_RECETTE_DOCUMENT")
    def closed_factory(**kwargs):
        raise AssertionError("APPEL_PROPRIETAIRE_INTERDIT_DANS_RECETTE_DOCUMENT")
    clock,port=Clock(),ClosedPort()
    audit=PostgresAuditParticipant(port,clock,"peer")
    source=ApiRequestSource(alias="default",profile_id="document-only",trust_source=port,
        assurance_source=port,facts_reader=port,clock=clock,max_identifier_chars=128)
    service=PostgresLocalAuthService(alias="default",peer_alias="peer",profile_id="document-only",
        trust_source=port,assurance_source=port,facts_reader=port,clock=clock,audit=audit,
        classification_source=port,decider_factory=closed_factory)
    return CoreApiComposition(alias="default",peer_alias="peer",request_source=source,
        auth_service=service,core_ports_factory=closed_factory,clock=clock,
        approved_host="api.example.test",approved_origin="https://api.example.test",
        limits=CoreHttpLimits(65536,8192,2,10),input_limits=ApiInputLimits(128,128,32768,16),
        cursor_codec=CoreCursorCodec(config=CoreCursorConfig(60,8192,128,128,10),
            key=b"Vecteur public document C06 sans secret de deploiement",clock=clock),
        interactive_commands=frozenset())


def contract_variant(pairs, version, mutate=lambda roots:None):
    """Document proposé cohérent : version, préfixe et index recalculés."""
    import hashlib
    major=version.split(".")[0]
    prefix="/api/v"+major
    roots={}
    for path,text in pairs:
        root=json.loads(text)
        root["info"]["version"]=version
        root["paths"]={p.replace("/api/v1",prefix,1):v for p,v in root["paths"].items()}
        if "x-documents" in root:
            for item in root["x-documents"]:
                item["href"]=item["href"].replace("/api/v1",prefix,1)
        roots[path.replace("/api/v1",prefix,1)]=root
    mutate(roots)
    def dump(value):
        return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    serialized={path:dump(root) for path,root in roots.items() if "x-documents" not in root}
    for path,root in roots.items():
        if "x-documents" in root:
            for item in root["x-documents"]:
                body=serialized[item["href"]].encode()
                item["bytes"],item["sha256"]=len(body),hashlib.sha256(body).hexdigest()
            serialized[path]=dump(root)
    return tuple((path,serialized[path]) for path in roots)


class CoreOpenapiDocumentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from django.conf import settings
        if not settings.configured:
            settings.configure(SECRET_KEY="Vecteur public de recette documentaire C06",
                ALLOWED_HOSTS=["api.example.test"],DEFAULT_CHARSET="utf-8",USE_TZ=True,LOGGING_CONFIG=None)
        from pixs.backend.api_core_openapi import build_core_openapi_documents,core_api_contract_plan
        cls.composition=documentation_composition()
        cls.plan=core_api_contract_plan()
        cls.pairs=build_core_openapi_documents(cls.composition)
        cls.documents=tuple(text for _,text in cls.pairs)

    def operation(self, path, method="post", pairs=None):
        for _,text in self.pairs if pairs is None else pairs:
            root=json.loads(text)
            if path in root["paths"]:
                return root,root["paths"][path][method]
        self.fail("ROUTE_DE_CONTRAT_ABSENTE")

    def test_bounded_reproducible_documents_and_verified_index(self):
        import hashlib
        from pixs.backend.api_core_openapi import build_core_openapi_documents,validate_core_openapi_document
        self.assertEqual(self.pairs,build_core_openapi_documents(self.composition))
        self.assertGreater(len(self.pairs),2)
        for _,text in self.pairs:
            self.assertLessEqual(len(text.encode()),65536)
            validate_core_openapi_document(self.plan,text)
        index=json.loads(self.pairs[0][1])
        self.assertEqual({item["href"] for item in index["x-documents"]},{path for path,_ in self.pairs[1:]})
        bodies=dict(self.pairs)
        for item in index["x-documents"]:
            raw=bodies[item["href"]].encode()
            self.assertEqual((item["bytes"],item["sha256"]),(len(raw),hashlib.sha256(raw).hexdigest()))
        operations=[(path,method) for text in self.documents for path,methods in json.loads(text)["paths"].items()
                    for method in methods if "/openapi" not in path]
        self.assertEqual(len(operations),156)
        self.assertEqual(len(set(operations)),156)

    def test_auth_parameters_and_wire_schemas_are_explicit(self):
        _,command=self.operation("/api/v1/platform/commands/create-user")
        schema=command["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(set(schema["properties"]),{"user_id"})
        self.assertEqual(command["security"],[{"BearerAccess":[]}])
        _,browser=self.operation("/api/v1/web/platform/commands/create-user")
        headers={p["name"]:p for p in browser["parameters"] if p["in"]=="header"}
        self.assertTrue(headers["Origin"]["required"] and headers["X-CSRFToken"]["required"])
        _,renew=self.operation("/api/v1/platform/auth/renew")
        self.assertEqual(renew["security"],[{"BearerRefresh":[]}])
        _,csrf=self.operation("/api/v1/web/auth/csrf","get")
        self.assertEqual(csrf["security"],[])
        _,query=self.operation("/api/v1/tenants/{tenant_id}/scopes/{scope_id}/groups","get")
        self.assertEqual({p["name"] for p in query["parameters"] if p["in"]=="path"},{"tenant_id","scope_id"})

    def test_all_declared_routes_and_responses_without_owner_calls(self):
        from django.test import RequestFactory
        from pixs.backend.api_core_views import build_core_api_view
        from pixs.backend.api_core_openapi import validate_core_api_response
        rf=RequestFactory()
        view=build_core_api_view(self.composition,previous_plan=self.plan,previous_documents=self.documents)
        for text in self.documents:
            root=json.loads(text)
            for template,methods in root["paths"].items():
                path=template.replace("{tenant_id}","tenant-probe").replace("{scope_id}","scope-probe")
                for method in methods:
                    request=rf.generic(method.upper(),path,data=b"{}",content_type="application/json",
                        secure=True,HTTP_HOST="api.example.test",HTTP_ORIGIN="https://api.example.test")
                    request.META["RAW_URI"]=path
                    response=view(request)
                    with self.subTest(path=template,method=method):
                        if "/openapi" not in path:
                            self.assertIn(response.status_code,(200,400,401,403))
                        else:
                            self.assertEqual(response.status_code,200)
                        self.assertTrue(validate_core_api_response(self.plan,self.documents,path_template=template,
                            method=method,response=response))

    def test_global_auth_routes_are_not_published_in_tenant_or_scope(self):
        from django.test import RequestFactory
        from pixs.backend.api_core_views import build_core_api_view
        rf=RequestFactory()
        view=build_core_api_view(self.composition,previous_plan=self.plan,previous_documents=self.documents)
        published={path for text in self.documents for path in json.loads(text)["paths"]}
        for web in ("","/web"):
            for suffix in ("", "/scopes/scope-probe"):
                for action in ("revoke-all","change-password"):
                    path="/api/v1"+web+"/tenants/tenant-probe"+suffix+"/auth/"+action
                    template=path.replace("tenant-probe","{tenant_id}").replace("scope-probe","{scope_id}")
                    self.assertNotIn(template,published)
                    request=rf.post(path,data="{}",content_type="application/json",secure=True,
                        HTTP_HOST="api.example.test",HTTP_ORIGIN="https://api.example.test")
                    request.META["RAW_URI"]=path
                    self.assertEqual(view(request).status_code,404)

    def test_creation_reference_binds_actor_and_full_context_without_authority(self):
        from pixs.auth.identifiers import session_creation_reference,AuthIdentifierError
        actor="pixs.core.identity:"+_I
        reference=session_creation_reference(actor,_T)
        self.assertEqual(reference,session_creation_reference(actor,ScopeContext(ScopeType.TENANT," t-é ")))
        for subject,context in (("pixs.core.identity:"+_U,_T),(actor,_P),
                (actor,ScopeContext(ScopeType.TENANT," t-é ","scope/a")),
                (actor,ScopeContext(ScopeType.TENANT,"t-é"))):
            self.assertNotEqual(reference,session_creation_reference(subject,context))
        for subject,context in ((_I,_T),(object(),_T),(actor,{"scope_type":"TENANT"})):
            with self.assertRaises(AuthIdentifierError):
                session_creation_reference(subject,context)

    def test_malformed_document_external_ref_and_nonstring_title_refused(self):
        from pixs.backend.api_core_openapi import validate_core_openapi_document
        from pixs.backend.openapi_document_view import OpenapiDocumentError
        baseline=json.loads(self.pairs[1][1])
        changes=[
            lambda root:root.update(openapi="3.0.0"),
            lambda root:root["info"].update(title=1),
            lambda root:root.update(private=True),
            lambda root:root["components"]["schemas"].update(Foreign={"$ref":"https://example.invalid/schema"}),
        ]
        for change in changes:
            root=copy.deepcopy(baseline);change(root)
            with self.subTest(change=changes.index(change)),self.assertRaises(OpenapiDocumentError):
                validate_core_openapi_document(self.plan,json.dumps(root))

    def test_schema_conformance_rejects_bool_version_and_extra_field(self):
        from django.http import JsonResponse
        from pixs.backend.api_core_openapi import validate_core_api_response
        from pixs.backend.openapi_document_view import OpenapiDocumentError
        body={"data":{"operation_id":_U,"result_ref":"pixs.core.user:"+_U,"version":1,
              "persistence_state":"ACTIVE","correlation_id":"corr"},
              "meta":{"correlation_id":"corr","context":{"scope_type":"PLATFORM","tenant_id":None,"scope_id":None}},"links":{}}
        def check(value):
            return validate_core_api_response(self.plan,self.documents,
                path_template="/api/v1/platform/commands/create-user",method="post",response=JsonResponse(value))
        self.assertTrue(check(body))
        for mutate in (lambda x:x["data"].update(version=True),lambda x:x["data"].update(private="vecteur-public")):
            bad=copy.deepcopy(body);mutate(bad)
            with self.assertRaises(OpenapiDocumentError):
                check(bad)

    def evolution(self, pairs, version="1.1.0", coexistence=None):
        from dataclasses import replace
        from pixs.backend.api_core_openapi_compare import check_core_openapi_evolution
        proposed=replace(self.plan,contract=replace(self.plan.contract,version=version),
                         openapi_document_ref="pixs-core-api-v"+version.replace(".","-"))
        return check_core_openapi_evolution(self.plan,proposed,self.documents,
            tuple(text for _,text in pairs),coexistence_doc=coexistence)

    def test_compatible_optional_input_and_unchanged_document(self):
        self.evolution(contract_variant(self.pairs,"1.1.0"))
        def optional(roots):
            for root in roots.values():
                op=root["paths"].get("/api/v1/platform/commands/create-user",{}).get("post")
                if op:
                    op["requestBody"]["content"]["application/json"]["schema"]["properties"]["optional_new"]={"type":"string"}
        self.evolution(contract_variant(self.pairs,"1.1.0",optional))

    def test_breaking_route_security_required_type_enum_and_response_blocked(self):
        from pixs.backend.api_core_openapi_compare import CoreOpenApiEvolutionError
        def mutate(roots, case):
            for root in roots.values():
                paths=root["paths"]
                if case=="route":paths.pop("/api/v1/platform/users",None)
                op=paths.get("/api/v1/platform/commands/create-user",{}).get("post")
                if op:
                    schema=op["requestBody"]["content"]["application/json"]["schema"]
                    if case=="security":op["security"]=[]
                    if case=="required":
                        schema["properties"]["new_required"]={"type":"string"}
                        schema["required"].append("new_required")
                    if case=="type":schema["properties"]["user_id"]={"type":"integer"}
                    if case=="response":op["responses"].pop("409")
                identity=paths.get("/api/v1/platform/commands/create-identity",{}).get("post")
                if case=="enum" and identity:
                    schema=identity["requestBody"]["content"]["application/json"]["schema"]["properties"]["state"]
                    schema["enum"]=schema["enum"][:1]
        for case in ("route","security","required","type","enum","response"):
            pairs=contract_variant(self.pairs,"1.1.0",lambda roots:mutate(roots,case))
            with self.subTest(case=case),self.assertRaises(CoreOpenApiEvolutionError):
                self.evolution(pairs)

    def test_major_upgrade_requires_declared_coexistence(self):
        from pixs.backend.api_core_openapi_compare import CoreOpenApiEvolutionError
        def remove(roots):
            for root in roots.values():root["paths"].pop("/api/v2/platform/users",None)
        pairs=contract_variant(self.pairs,"2.0.0",remove)
        with self.assertRaises(CoreOpenApiEvolutionError):
            self.evolution(pairs,"2.0.0")
        self.evolution(pairs,"2.0.0","Coexistence déclarée v1 et v2 sous responsabilité de la composition hôte.")

    def test_real_url_builder_requires_baseline_and_runs_structural_guard(self):
        from unittest.mock import patch
        from pixs.backend.api_core_views import build_core_api_urls
        from pixs.backend.api_core_openapi_compare import CoreOpenApiEvolutionError
        with self.assertRaises(TypeError):
            build_core_api_urls(self.composition)
        with self.assertRaises(CoreOpenApiEvolutionError):
            build_core_api_urls(self.composition,previous_plan=self.plan,previous_documents=())
        def remove(roots):
            for root in roots.values():root["paths"].pop("/api/v1/platform/users",None)
        changed=contract_variant(self.pairs,"1.0.0",remove)
        with patch("pixs.backend.api_core_openapi.build_core_openapi_documents",return_value=changed):
            with self.assertRaises(CoreOpenApiEvolutionError):
                build_core_api_urls(self.composition,previous_plan=self.plan,previous_documents=self.documents)

    def test_document_head_transport_and_method_keep_bounded_transport(self):
        from django.test import RequestFactory
        from pixs.backend.api_core_views import build_core_api_view
        rf=RequestFactory()
        view=build_core_api_view(self.composition,previous_plan=self.plan,previous_documents=self.documents)
        get=view(rf.get("/api/v1/openapi.json",secure=True,HTTP_HOST="api.example.test"))
        head=view(rf.head("/api/v1/openapi.json",secure=True,HTTP_HOST="api.example.test"))
        self.assertEqual(head.content,b"")
        self.assertEqual(int(head["Content-Length"]),len(get.content))
        self.assertEqual(view(rf.get("/api/v1/openapi.json",HTTP_HOST="api.example.test")).status_code,403)
        denied=view(rf.post("/api/v1/openapi.json",secure=True,HTTP_HOST="api.example.test"))
        self.assertEqual((denied.status_code,denied.content,denied["Allow"]),(405,b"","GET, HEAD"))

    def test_inconsistent_composition_and_client_activity_policy_refused(self):
        from dataclasses import replace
        from pixs.backend.api_core_composition import CoreHttpLimits
        for fields in ({"limits":CoreHttpLimits(65536,8192,2,20)},
                       {"interactive_commands":{"create-user"}},
                       {"interactive_commands":frozenset({"client-chosen"})}):
            with self.subTest(fields=list(fields)),self.assertRaises(ValueError):
                replace(self.composition,**fields)


if __name__ == "__main__":
    unittest.main()
