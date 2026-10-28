"""Recettes contractuelles C14 : chemins réels, schémas et absence de mesure inventée."""
import copy
import json
import unittest

from pixs.backend.api_pzt_dns_catalog import C14_HTTP_BINDINGS, C14HttpCatalogError
from pixs.backend.api_pzt_dns_openapi import (
    build_c14_openapi_document, c14_http_request_schema, c14_http_response_schema,
)


class C14OpenApiTests(unittest.TestCase):
    def test_deux_documents_fermes_et_soixante_six_chemins(self):
        ids = set()
        total = 0
        for owner, count in (("pixs.pzt", 24), ("pixs.dns", 42)):
            doc = build_c14_openapi_document(owner)
            self.assertEqual(doc["openapi"], "3.1.0")
            self.assertEqual(doc["info"]["version"], "1.0.0")
            self.assertEqual(doc["x-pixs-contract-id"], owner + ".management.api")
            self.assertEqual(len(doc["paths"]), count)
            total += len(doc["paths"])
            for path, methods in doc["paths"].items():
                self.assertIn("/" + owner.removeprefix("pixs.") + "/", path)
                self.assertEqual(len(methods), 1)
                for operation in methods.values():
                    self.assertNotIn(operation["operationId"], ids)
                    ids.add(operation["operationId"])
            json.dumps(doc, allow_nan=False)
        self.assertEqual(total, 66)

    def test_references_locales_resolues_et_copies_independantes(self):
        for owner in ("pixs.pzt", "pixs.dns"):
            doc = build_c14_openapi_document(owner)
            pending = [doc]
            while pending:
                item = pending.pop()
                if type(item) is dict:
                    if "$ref" in item:
                        self.assertTrue(item["$ref"].startswith("#/components/schemas/"))
                        self.assertIn(item["$ref"].split("/")[-1], doc["components"]["schemas"])
                    pending.extend(item.values())
                elif type(item) is list:
                    pending.extend(item)
            original = copy.deepcopy(doc)
            doc["paths"].clear()
            self.assertEqual(build_c14_openapi_document(owner), original)

    def test_methodes_securite_et_idempotence_ne_se_confondent_pas(self):
        for owner in ("pixs.pzt", "pixs.dns"):
            for path, methods in build_c14_openapi_document(owner)["paths"].items():
                method, op = next(iter(methods.items()))
                parameters = {(p["in"], p["name"]): p for p in op["parameters"]}
                web = "/web/" in path
                self.assertEqual(op["security"], [{"WebSession" if web else "BearerAccess": []}])
                self.assertEqual(("header", "Idempotency-Key") in parameters, method == "post")
                self.assertEqual("requestBody" in op, method == "post")
                self.assertEqual("202" in op["responses"], method == "post")
                self.assertEqual(("header", "X-CSRFToken") in parameters, method == "post" and web)
                if method == "get":
                    for flag in ("waive_audit", "waive_governance"):
                        self.assertFalse(parameters[("query", flag)]["required"])

    def test_session_affichee_optionnelle_seulement_en_web(self):
        from pixs.backend.api_core_catalog import API_UUID7_PATTERN
        web_count = api_count = 0
        for owner in ("pixs.pzt", "pixs.dns"):
            for path, methods in build_c14_openapi_document(owner)["paths"].items():
                operation = next(iter(methods.values()))
                headers = [parameter for parameter in operation["parameters"]
                           if parameter["in"] == "header"
                           and parameter["name"] == "X-Shell-Session-ID"]
                if "/web/" in path:
                    self.assertEqual(len(headers), 1)
                    self.assertIs(headers[0]["required"], False)
                    self.assertEqual(headers[0]["schema"],
                                     {"type": "string", "pattern": API_UUID7_PATTERN})
                    self.assertIn("400", operation["responses"])
                    web_count += 1
                else:
                    self.assertEqual(headers, [])
                    api_count += 1
        self.assertEqual((web_count, api_count), (33, 33))

    def test_dto_client_sans_faits_ni_metadonnees_autoritaires(self):
        for b in C14_HTTP_BINDINGS:
            schema = c14_http_request_schema(b.owner, b.kind, b.name)
            self.assertFalse(schema["additionalProperties"])
            self.assertTrue(set(schema["required"]) <= set(schema["properties"]))
            for forbidden in ("subject_id", "decision_id", "context", "metadata", "authentication"):
                self.assertNotIn(forbidden, schema["properties"])
            self.assertNotIn("authorization_intent", schema["required"])
            if "configuration" in schema["properties"]:
                cfg = schema["properties"]["configuration"]["properties"]
                gov = cfg["governance"]
                self.assertEqual(len(gov["properties"]), 15)
                self.assertEqual(set(gov["required"]), set(gov["properties"]))
                self.assertEqual(set(cfg["secret_refs"]["items"]["properties"]), {"owner_id", "entry_id", "source"})
                if b.owner == "pixs.dns":
                    self.assertEqual(cfg["ttl_positive"]["maximum"], 30)
                    self.assertEqual(cfg["ttl_negative"]["maximum"], 5)
                    self.assertNotIn("uniqueItems", cfg["views"])

    def test_inconnu_non_mesure_et_cible_non_verifiee_explicites(self):
        for b in C14_HTTP_BINDINGS:
            schema = c14_http_response_schema(b.owner, b.kind, b.name)
            data = schema["properties"]["data"]["properties"]
            if b.kind == "COMMAND":
                unknown = c14_http_response_schema(b.owner, b.kind, b.name, unknown=True)
                self.assertEqual(unknown["properties"]["data"]["properties"]["outcome"]["const"], "UNKNOWN")
                self.assertEqual(unknown["properties"]["data"]["properties"]["config_revision"], {"type": "null"})
                self.assertNotIn("activity", unknown["properties"]["meta"]["properties"])
            elif b.name.startswith("get_applied"):
                self.assertEqual(data["application_status"]["const"], "UNKNOWN")
                self.assertEqual(data["measurement_status"]["const"], "UNMEASURED")
                self.assertEqual(data["applied_present"], {"type": "null"})
                self.assertEqual(data["measurements"], {"type": "null"})
            elif b.name == "resolve_view_policy":
                self.assertEqual(data["target_verification"]["const"], "UNVERIFIED")
                self.assertEqual(data["applied_present"], {"type": "null"})
                self.assertNotIn("nxdomain", data)
            if b.kind == "QUERY":
                with self.assertRaises(C14HttpCatalogError):
                    c14_http_response_schema(b.owner, b.kind, b.name, unknown=True)

    def test_proprietaires_et_genres_inconnus_refuses(self):
        for owner in ("pixs.core", "", None, []):
            with self.assertRaises(C14HttpCatalogError):
                build_c14_openapi_document(owner)
        with self.assertRaises(C14HttpCatalogError):
            c14_http_request_schema("pixs.pzt", "COMMAND", "declare_name")

    def test_fragments_publics_bornes_indexes_et_couverture_complete(self):
        from pixs.backend.api_module_openapi import validate_module_openapi_document
        from pixs.backend.api_pzt_dns_catalog import c14_api_contract_plan
        import hashlib
        from pixs.backend.api_pzt_dns_openapi import build_c14_openapi_documents
        for owner in ("pixs.pzt", "pixs.dns"):
            documents = build_c14_openapi_documents(owner)
            self.assertGreater(len(documents), 1)
            by_path = dict(documents)
            self.assertEqual(len(by_path), len(documents))
            self.assertEqual(documents, build_c14_openapi_documents(owner))
            index = json.loads(documents[0][1])
            found = {}
            for path, document in documents:
                validate_module_openapi_document(c14_api_contract_plan(owner), document)
                self.assertLessEqual(len(document.encode("utf-8")), 65536)
                self.assertTrue(path.startswith("/api/v1/openapi/"))
            for entry in index["x-documents"]:
                body = by_path[entry["href"]].encode("utf-8")
                self.assertEqual(entry["bytes"], len(body))
                self.assertEqual(entry["sha256"], hashlib.sha256(body).hexdigest())
                self.assertIn(entry["href"], index["paths"])
                fragment = json.loads(body)
                for path, methods in fragment["paths"].items():
                    self.assertNotIn(path, found)
                    found[path] = methods
            self.assertEqual(found, build_c14_openapi_document(owner)["paths"])
