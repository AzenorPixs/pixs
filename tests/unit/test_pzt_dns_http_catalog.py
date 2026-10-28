"""Recettes de concordance entre contrats métier C14 et liaisons HTTP."""
from dataclasses import FrozenInstanceError
import unittest

from pixs.backend.api import api_major_prefix
from pixs.backend.api_pzt_dns_catalog import (
    C14_HTTP_BINDINGS, C14_HTTP_VERSION, C14HttpCatalogError,
    c14_api_contract_plan, c14_http_binding,
)
from pixs.dns.contracts import DNS_COMMANDS, DNS_QUERIES
from pixs.kernel.contracts import ContractCategory
from pixs.pzt.contracts import PZT_COMMANDS, PZT_QUERIES


class C14HttpCatalogTests(unittest.TestCase):
    def test_catalogue_couvre_exactement_les_operations_metier(self):
        expected = {
            ("pixs.pzt", "COMMAND"): set(PZT_COMMANDS),
            ("pixs.pzt", "QUERY"): set(PZT_QUERIES),
            ("pixs.dns", "COMMAND"): set(DNS_COMMANDS),
            ("pixs.dns", "QUERY"): set(DNS_QUERIES),
        }
        self.assertEqual(len(C14_HTTP_BINDINGS), 11)
        for (owner, kind), names in expected.items():
            self.assertEqual({b.name for b in C14_HTTP_BINDINGS if (b.owner, b.kind) == (owner, kind)}, names)
        self.assertEqual(len({(b.owner, b.kind, b.name) for b in C14_HTTP_BINDINGS}), 11)
        self.assertEqual(len({(b.method, b.segments) for b in C14_HTTP_BINDINGS}), 11)

    def test_contrats_api_distincts_et_proprietaires(self):
        business = {b.contract_id for b in C14_HTTP_BINDINGS}
        for owner, contract, reference in (
            ("pixs.pzt", "pixs.pzt.management.api", "pixs-pzt-management-api-v1"),
            ("pixs.dns", "pixs.dns.management.api", "pixs-dns-management-api-v1"),
        ):
            plan = c14_api_contract_plan(owner)
            self.assertIs(plan.contract.category, ContractCategory.API)
            self.assertEqual(plan.contract.contract_id, contract)
            self.assertEqual(plan.contract.owner_component, owner)
            self.assertEqual(plan.contract.version, "1.0.0")
            self.assertEqual(C14_HTTP_VERSION, "1.0.0")
            self.assertEqual(plan.openapi_document_ref, reference)
            self.assertEqual(api_major_prefix(plan), "/api/v1")
            self.assertNotIn(contract, business)

    def test_declaration_litterale_methodes_suffixes_et_champs(self):
        for b in C14_HTTP_BINDINGS:
            self.assertIs(c14_http_binding(b.owner, b.kind, b.name), b)
            owner_segment = {"pixs.pzt": "pzt", "pixs.dns": "dns"}[b.owner]
            expected_method = {"COMMAND": "POST", "QUERY": "GET"}[b.kind]
            group = {"COMMAND": "commands", "QUERY": "queries"}[b.kind]
            self.assertEqual(b.method, expected_method)
            self.assertEqual(b.segments, (owner_segment, group, b.name))
            fields = () if b.kind == "COMMAND" else ("resource_id",)
            if b.name == "resolve_view_policy":
                fields = ("resource_id", "view", "name")
            self.assertEqual(b.query_fields, fields)
            self.assertTrue(b.contract_id.startswith(b.owner + "."))
        self.assertEqual(c14_http_binding("pixs.dns", "COMMAND", "declare_name").contract_id, "pixs.dns.records.command")
        self.assertEqual(c14_http_binding("pixs.dns", "QUERY", "resolve_view_policy").contract_id, "pixs.dns.policy.query")
        self.assertEqual(c14_http_binding("pixs.pzt", "QUERY", "get_applied_pzt").contract_id, "pixs.pzt.state.query")

    def test_refus_fermes_sans_echo_de_valeurs(self):
        for args in (
            ("pixs.dns", "COMMAND", "report_applied"),
            ("pixs.pzt", "QUERY", "get_desired_dns"),
            ("pixs.dns", "QUERY", "declare_name"),
            ("pixs.dns", "QUERY", "get-desired-dns"),
            ("pixs.dns", "QUERY", "get_desired_dns/extra"),
            ("pixs.dns", "QUERY", " get_desired_dns"),
            ([], "QUERY", "get_desired_dns"),
            ("pixs.dns", True, "get_desired_dns"),
        ):
            with self.subTest(args=args), self.assertRaises(C14HttpCatalogError) as raised:
                c14_http_binding(*args)
            self.assertEqual(str(raised.exception), "Liaison HTTP PZT/DNS invalide.")
        for owner in ("pixs.core", "pixs.dns/extra", None, [], True):
            with self.assertRaises(C14HttpCatalogError):
                c14_api_contract_plan(owner)

    def test_aucune_coercition_et_liaisons_immuables(self):
        class SousTexte(str):
            pass
        with self.assertRaises(C14HttpCatalogError):
            c14_http_binding(SousTexte("pixs.dns"), "QUERY", "get_desired_dns")
        with self.assertRaises(C14HttpCatalogError):
            c14_api_contract_plan(SousTexte("pixs.dns"))
        with self.assertRaises(FrozenInstanceError):
            C14_HTTP_BINDINGS[0].method = "GET"
        with self.assertRaises(FrozenInstanceError):
            c14_api_contract_plan("pixs.dns").contract.owner_component = "pixs.pzt"


if __name__ == "__main__":
    unittest.main()
