"""Entrées HTTP C14 : types stricts et liaison aux requêtes du serveur."""
import copy
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import unittest

from pixs.backend.api_pzt_dns_inputs import C14HttpInputError, parse_c14_http_input
from pixs.core.authz.ports import Request
from pixs.core.command_metadata import CommandMetadata
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.dns.contracts import (
    DeclareDesiredDns, RetireDesiredDns, DeclareName, RetireName,
    GetDesiredDns, GetAppliedDns, ResolveViewPolicy,
)
from pixs.pzt.contracts import DeclareDesiredPzt, RetireDesiredPzt, GetDesiredPzt, GetAppliedPzt
from test_pzt_dns_contracts import _pztcfg, _dnscfg


def wire(value):
    if is_dataclass(value):
        return {f.name: wire(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Enum):
        return value.value
    if type(value) in (tuple, frozenset):
        return [wire(v) for v in value]
    return value


def request(name, *, subject="sujet-http", resource="cible opaque / HTTP", scope=None):
    return Request("decision-http", subject, resource, name,
                   scope or ScopeContext(ScopeType.TENANT, "tenant opaque", "scope/opaque"),
                   "correlation-http")


def metadata(req):
    return CommandMetadata("operation-http", (req.correlation_id,), (), req.context,
                           req.action_id, req.subject_id, "idem-http")


def payload(name):
    if name == "declare_desired_pzt":
        return {"schema_version": "1.0.0", "resource_id": "cible opaque / HTTP",
                "expected_revision": 1, "configuration": wire(_pztcfg())}
    if name == "declare_desired_dns":
        return {"schema_version": "1.0.0", "resource_id": "cible opaque / HTTP",
                "expected_revision": 1, "configuration": wire(_dnscfg())}
    if name in ("retire_desired_pzt", "retire_desired_dns"):
        return {"schema_version": "1.0.0", "resource_id": "cible opaque / HTTP",
                "expected_revision": 1, "reason": "motif HTTP"}
    if name in ("declare_name", "retire_name"):
        data = {"schema_version": "1.0.0", "resource_id": "cible opaque / HTTP",
                "expected_revision": 1, "name": "nom.pzt.test.internal", "view": "vue-test"}
        if name == "declare_name":
            data["target_ref"] = "cible opaque"
        return data
    data = {"resource_id": "cible opaque / HTTP"}
    if name == "resolve_view_policy":
        data.update(view="vue-test", name="nom.pzt.test.internal")
    return data


def parse(owner, kind, name, body=None, req=None, meta=None):
    req = req or request(name)
    if kind == "COMMAND" and meta is None:
        meta = metadata(req)
    return parse_c14_http_input(owner, kind, name, payload(name) if body is None else body,
                               request=req, metadata=meta)


class C14HttpInputTests(unittest.TestCase):
    def test_onze_dto_existants_et_perimetres_opaques_conserves(self):
        cases = [
            ("pixs.pzt", "COMMAND", "declare_desired_pzt", DeclareDesiredPzt),
            ("pixs.pzt", "COMMAND", "retire_desired_pzt", RetireDesiredPzt),
            ("pixs.pzt", "QUERY", "get_desired_pzt", GetDesiredPzt),
            ("pixs.pzt", "QUERY", "get_applied_pzt", GetAppliedPzt),
            ("pixs.dns", "COMMAND", "declare_desired_dns", DeclareDesiredDns),
            ("pixs.dns", "COMMAND", "retire_desired_dns", RetireDesiredDns),
            ("pixs.dns", "COMMAND", "declare_name", DeclareName),
            ("pixs.dns", "COMMAND", "retire_name", RetireName),
            ("pixs.dns", "QUERY", "get_desired_dns", GetDesiredDns),
            ("pixs.dns", "QUERY", "get_applied_dns", GetAppliedDns),
            ("pixs.dns", "QUERY", "resolve_view_policy", ResolveViewPolicy),
        ]
        for owner, kind, name, cls in cases:
            with self.subTest(name=name):
                req = request(name)
                dto = parse(owner, kind, name, req=req)
                self.assertIs(type(dto), cls)
                self.assertIs(dto.request, req)
                self.assertEqual(dto.resource_id, "cible opaque / HTTP")
                self.assertEqual(dto.request.context.tenant_id, "tenant opaque")
                self.assertEqual(dto.request.context.scope_id, "scope/opaque")
                self.assertEqual(dto.schema_version, "1.0.0")

    def test_configuration_sans_coercition_et_collections_adaptees(self):
        dns = payload("declare_desired_dns")
        dns["configuration"]["views"] = ["vue B", "vue A", "vue B"]
        dns["configuration"]["ttl_positive"] = 0
        dns["configuration"]["ttl_negative"] = 0
        dto = parse("pixs.dns", "COMMAND", "declare_desired_dns", dns)
        self.assertEqual(dto.configuration.views, ("vue B", "vue A", "vue B"))
        self.assertEqual(dto.configuration.ttl_positive, 0)
        self.assertEqual(dto.configuration.ttl_negative, 0)
        self.assertIs(type(dto.configuration.secret_refs), tuple)
        self.assertIs(type(dto.configuration.governance.data_classes), frozenset)
        pzt = parse("pixs.pzt", "COMMAND", "declare_desired_pzt")
        self.assertIs(pzt.configuration.v6_enabled, False)
        self.assertEqual(parse("pixs.dns", "COMMAND", "declare_desired_dns").configuration.ttl_positive, 30)

    def test_refus_types_numeriques_booleens_et_ttl_hors_bornes(self):
        for name, owner, field, values in (
            ("declare_desired_pzt", "pixs.pzt", "v6_enabled", [0, 1, "false", None]),
            ("declare_desired_dns", "pixs.dns", "ttl_positive", [True, "30", 30.0, -1, 31]),
            ("declare_desired_dns", "pixs.dns", "ttl_negative", [False, "5", 5.0, -1, 6]),
            ("declare_desired_dns", "pixs.dns", "config_revision", [True, "2", 2.0, 0]),
        ):
            for value in values:
                body = payload(name)
                body["configuration"][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(C14HttpInputError):
                    parse(owner, "COMMAND", name, body)
        for value in (True, False, "1", 1.0, -1, None):
            body = payload("retire_desired_pzt")
            body["expected_revision"] = value
            with self.assertRaises(C14HttpInputError):
                parse("pixs.pzt", "COMMAND", "retire_desired_pzt", body)

    def test_entrees_fermees_et_aucun_parametre_serveur_client(self):
        req = request("retire_desired_pzt")
        for body in (None, [], True, "texte", {}, {"resource_id": req.resource_id}):
            with self.assertRaises(C14HttpInputError):
                parse_c14_http_input("pixs.pzt", "COMMAND", req.action_id, body,
                                     request=req, metadata=metadata(req))
        for field in ("request", "metadata", "context", "subject_id", "extra"):
            body = payload(req.action_id)
            body[field] = {"sujet": "faux"}
            with self.assertRaises(C14HttpInputError):
                parse("pixs.pzt", "COMMAND", req.action_id, body)
        for field in ("schema_version", "resource_id", "expected_revision", "configuration"):
            body = payload("declare_desired_dns")
            del body[field]
            with self.assertRaises(C14HttpInputError):
                parse("pixs.dns", "COMMAND", "declare_desired_dns", body)
        body = payload("get_desired_dns")
        body["schema_version"] = "1.0.0"
        with self.assertRaises(C14HttpInputError):
            parse("pixs.dns", "QUERY", "get_desired_dns", body)

    def test_config_gouvernance_et_secrets_sont_fermes(self):
        cases = []
        base = payload("declare_desired_dns")
        for change in ("extra_config", "no_ttl", "empty_views", "tuple_views", "extra_gov",
                       "missing_gov", "duplicate_gov", "invalid_enum", "raw_secret", "extra_secret"):
            b = copy.deepcopy(base)
            c = b["configuration"]
            if change == "extra_config": c["available"] = True
            elif change == "no_ttl": del c["ttl_negative"]
            elif change == "empty_views": c["views"] = []
            elif change == "tuple_views": c["views"] = ("vue",)
            elif change == "extra_gov": c["governance"]["authority"] = "client"
            elif change == "missing_gov": del c["governance"]
            elif change == "duplicate_gov": c["governance"]["data_classes"] = ["a", "a"]
            elif change == "invalid_enum": c["governance"]["confidentiality"] = "inconnue"
            elif change == "raw_secret": c["secret_refs"] = ["valeur interdite"]
            elif change == "extra_secret": c["secret_refs"][0]["value"] = "valeur interdite"
            cases.append((change, b))
        for label, body in cases:
            with self.subTest(label=label), self.assertRaises(C14HttpInputError):
                parse("pixs.dns", "COMMAND", "declare_desired_dns", body)

    def test_metadonnees_et_requete_serveur_liees(self):
        req = request("retire_desired_dns")
        meta = metadata(req)
        for bad in (replace(meta, subject_id="autre"), replace(meta, command_type="declare_name"),
                    replace(meta, scope_context=ScopeContext(ScopeType.PLATFORM)),
                    replace(meta, correlation_ids=("autre",))):
            with self.assertRaises(C14HttpInputError):
                parse("pixs.dns", "COMMAND", req.action_id, req=req, meta=bad)
        with self.assertRaises(C14HttpInputError):
            parse("pixs.dns", "QUERY", "get_desired_dns", req=request("get_applied_dns"))
        with self.assertRaises(C14HttpInputError):
            parse("pixs.dns", "QUERY", "get_desired_dns", meta=metadata(req))
        with self.assertRaises(C14HttpInputError):
            parse_c14_http_input("pixs.dns", "COMMAND", req.action_id, payload(req.action_id),
                                 request=req, metadata=None)

    def test_texte_utf8_sans_normalisation_ni_echo(self):
        for resource in ("", "a\x00b", "\ud800"):
            body = payload("get_desired_dns")
            body["resource_id"] = resource
            with self.assertRaises(C14HttpInputError) as raised:
                parse("pixs.dns", "QUERY", "get_desired_dns", body)
            self.assertEqual(str(raised.exception), "Entrée HTTP PZT/DNS invalide.")
        req = request("get_desired_dns", resource=" cible à espaces ")
        dto = parse("pixs.dns", "QUERY", req.action_id,
                    {"resource_id": " cible à espaces "}, req=req)
        self.assertEqual(dto.resource_id, " cible à espaces ")


if __name__ == "__main__":
    unittest.main()
