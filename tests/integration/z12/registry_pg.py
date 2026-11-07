"""Recette du stockage CA dans un schéma PostgreSQL explicitement réservé.

Programme autonome : --schema c02_<16 hex> obligatoire. Aucun effet à l'import.
Les clés logicielles éphémères ne servent qu'aux certificats de test publics ;
elles ne qualifient ni matériel, autorité courante, restauration ou concurrence.
Les identifiants PG restent dans le processus autorisé ; aucun diagnostic brut.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import re
import sys
import traceback
import unittest
import uuid
from decimal import Decimal

EXPECTED_ROOT = pathlib.Path("/home/devops/datas/pixs")


def _safe_error(error_info):
    return {
        "classe": error_info[0].__name__,
        "cadres": [
            {"fichier": pathlib.Path(frame.f_code.co_filename).name, "ligne": line, "fonction": frame.f_code.co_name}
            for frame, line in list(traceback.walk_tb(error_info[2]))[-8:]
        ],
    }


class _SafeResult(unittest.TestResult):
    def addError(self, test, err):
        self.errors.append((test.id(), _safe_error(err)))

    def addFailure(self, test, err):
        self.failures.append((test.id(), _safe_error(err)))


def _suite():
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID
    from django.db import IntegrityError, connections, transaction
    from django.db.models import F
    from pixs.pzt_ca import models as m
    from pixs.pzt.identifiers import new_uuid7
    from pixs.pzt_ca.registry_bindings import DjangoCertificateOwnerBindings
    from psycopg import sql

    clock = datetime.datetime(2026, 10, 23, 9, tzinfo=datetime.timezone.utc)
    certificate_end = clock + datetime.timedelta(days=365)

    def store(model, **values):
        row = model(created_at=clock, updated_at=clock, **values)
        row._state.db = "default"
        row.clean()
        row.save(using="default", force_insert=True)
        return row

    def public_key(key):
        return key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)

    def material(key, prefix, kind):
        raw = public_key(key)
        return store(m.CaKeyMaterial, key_ref=prefix + "-key", key_material_ref=prefix + "-material",
            spki_sha256=hashlib.sha256(raw).hexdigest(), spki_der=raw, key_created_at=clock, ca_kind=kind)

    def certificate(subject, issuer, subject_key, signer_key, serial, path_len, issuer_key=None, issuer_serial=None):
        builder = (x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)
            .public_key(subject_key.public_key()).serial_number(serial)
            .not_valid_before(clock).not_valid_after(certificate_end)
            .add_extension(x509.BasicConstraints(ca=True, path_length=path_len), critical=True)
            .add_extension(x509.KeyUsage(digital_signature=False, content_commitment=False,
                key_encipherment=False, data_encipherment=False, key_agreement=False,
                key_cert_sign=True, crl_sign=False, encipher_only=False, decipher_only=False), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(subject_key.public_key()), critical=False))
        if issuer_key is not None:
            ski = x509.SubjectKeyIdentifier.from_public_key(issuer_key.public_key()).digest
            builder = builder.add_extension(x509.AuthorityKeyIdentifier(ski,
                [x509.DirectoryName(issuer)], issuer_serial), critical=False)
        return builder.sign(signer_key, hashes.SHA256())

    def fixture(root_serial=42, intermediate_serial=43):
        prefix = "z12-pg-test-" + uuid.uuid4().hex
        root_key = ec.generate_private_key(ec.SECP256R1())
        issuer_key = ec.generate_private_key(ec.SECP256R1())
        root_material = material(root_key, prefix + "-root", "root")
        issuer_material = material(issuer_key, prefix + "-issuer", "intermediate")
        root = store(m.CaRoot, domain=prefix, root_ref=prefix + "-root",
            root_generation_id=prefix + "-root-gen", root_cert_ref=prefix + "-root-cert",
            key_material=root_material, status="active")
        issuer = store(m.CaIssuer, domain=prefix, logical_authority=prefix + "-authority",
            emission_scope=prefix + "-scope", issuer_id=prefix + "-issuer", issuer_role="principal")
        generation = store(m.CaGeneration, issuer=issuer, root=root, key_material=issuer_material,
            generation_id=prefix + "-generation", created_epoch="1", status="active")
        root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Racine test registre Z12")])
        issuer_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Intermediaire test registre Z12")])
        root_x509 = certificate(root_name, root_name, root_key, root_key, root_serial, 1)
        issuer_x509 = certificate(issuer_name, root_name, issuer_key, root_key, intermediate_serial, 0,
            issuer_key=root_key, issuer_serial=root_serial)
        root_der = root_x509.public_bytes(serialization.Encoding.DER)

        def record(cert, role, key, ref, generation_row=None):
            der = cert.public_bytes(serialization.Encoding.DER)
            ski = cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value.digest
            aki = None if role == "root" else cert.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier).value.key_identifier
            return store(m.CaCertificate, cert_ref=ref, cert_bytes_ref=ref + "-bytes", ca_kind=role,
                root=root, intermediate_generation=generation_row, serial_number=Decimal(cert.serial_number),
                serial_public=ref + "-serial", not_before_utc=clock, not_after_utc=certificate_end,
                fingerprint_public=ref + "-fingerprint", fingerprint_sha256=hashlib.sha256(der).digest(),
                subject_key_id=ref + "-ski", ski=ski, authority_key_id=None if aki is None else ref + "-aki",
                aki=aki, certificate_der=der, root_der=root_der, subject_spki_der=public_key(key),
                root_spki_der=public_key(root_key), anchor_ref=prefix + "-anchor")

        root_cert = record(root_x509, "root", root_key, root.root_cert_ref)
        issuer_cert = record(issuer_x509, "intermediate", issuer_key, prefix + "-issuer-cert", generation)
        selection = store(m.CaActiveSelection, domain=prefix, logical_authority=issuer.logical_authority,
            emission_scope=issuer.emission_scope, generation=generation, epoch="1", engagement_ref=prefix + "-engaged")
        operation = store(m.CaOperationLink, domain=prefix, logical_authority=issuer.logical_authority,
            emission_scope=issuer.emission_scope, operation_id=prefix + "-operation", operation_version="1.0.0",
            request_id=prefix + "-request", context_ref=prefix + "-context", input_fingerprint=prefix + "-input",
            epoch="1", policy_ref=prefix + "-policy", content_sha256="1" * 64, serializer_version="1.0.0")
        result = store(m.CaResultRecord, result_id=prefix + "-result", operation_link=operation,
            recorded_at=clock, result_kind="current_operation", validation="valid", engagement="engaged",
            effect="applied", error_code="ok", engagement_ref=selection.engagement_ref,
            effect_evidence_ref=prefix + "-effect")
        retired_material = material(ec.generate_private_key(ec.SECP256R1()), prefix + "-retired", "intermediate")
        retired_generation = store(m.CaGeneration, issuer=issuer, root=root, key_material=retired_material,
            generation_id=prefix + "-retired-generation", created_epoch="1", status="retired")
        retirement = store(m.CaRetirementRecord, retirement_ref=prefix + "-retirement",
            target_generation=retired_generation, operation_link=operation, retired_at=clock,
            epoch="1", retirement_evidence_ref=prefix + "-retirement-proof")
        return {"prefix": prefix, "key_material": root_material, "root": root, "issuer": issuer,
            "generation": generation, "certificate": issuer_cert, "root_certificate": root_cert,
            "selection": selection, "operation": operation, "result": result, "retirement": retirement,
            "retired_generation": retired_generation}

    class RegistryStorageTests(unittest.TestCase):
        def setUp(self):
            self.atomic = transaction.atomic(using="default")
            self.atomic.__enter__()
            self.addCleanup(self.rollback)
            self.graph = fixture()

        def rollback(self):
            transaction.set_rollback(True, using="default")
            self.atomic.__exit__(None, None, None)

        def immutable_rows(self):
            return [self.graph[name] for name in (
                "key_material", "root", "issuer", "generation", "certificate", "operation", "result", "retirement")]

        def refused(self, action, state="23514", marker=None, constraint=None):
            try:
                with transaction.atomic(using="default"):
                    action()
            except IntegrityError as exc:
                cause = exc.__cause__
                self.assertEqual(getattr(cause, "sqlstate", None), state)
                if marker is not None:
                    self.assertEqual(getattr(getattr(cause, "diag", None), "message_primary", None), marker)
                if constraint is not None:
                    self.assertEqual(getattr(getattr(cause, "diag", None), "constraint_name", None), constraint)
            else:
                self.fail("Refus SQL attendu")

        def test_roundtrip_all_models_and_public_chain(self):
            for row in self.graph.values():
                if not hasattr(row, "_meta"):
                    continue
                loaded = type(row).objects.using("default").get(pk=row.pk)
                loaded.clean()
                self.assertEqual(loaded.pk, row.pk)
            bindings = DjangoCertificateOwnerBindings("default")
            for name in ("root_certificate", "certificate"):
                row = self.graph[name]
                actual = bindings.resolve_certificate(row.cert_ref)
                self.assertEqual(actual.certificate_der, row.certificate_der)
                self.assertEqual(actual.fingerprint_sha256, row.fingerprint_sha256)
                self.assertEqual(actual.serial_number, int(row.serial_number))

        def test_business_fields_and_identity_are_immutable(self):
            fields = ("key_ref", "root_ref", "issuer_id", "generation_id", "cert_bytes_ref",
                "input_fingerprint", "error_code", "retirement_evidence_ref")
            for row, field in zip(self.immutable_rows(), fields, strict=True):
                original = getattr(row, field)
                self.refused(lambda row=row, field=field, original=original: type(row).objects.filter(pk=row.pk).update(**{field: original + "-other"}), marker="PZT_CA_IMMUTABLE")
                self.refused(lambda row=row: type(row).objects.filter(pk=row.pk).update(id=new_uuid7()), marker="PZT_CA_IMMUTABLE")
                self.refused(lambda row=row: type(row).objects.filter(pk=row.pk).update(created_at=clock - datetime.timedelta(seconds=1)), marker="PZT_CA_IMMUTABLE")
                self.assertEqual(type(row).objects.get(pk=row.pk).__dict__[field], original)

        def test_metadata_updates_remain_possible(self):
            later = clock + datetime.timedelta(seconds=1)
            for row in self.immutable_rows():
                self.assertEqual(type(row).objects.filter(pk=row.pk).update(version=F("version") + 1, updated_at=later), 1)
                loaded = type(row).objects.get(pk=row.pk)
                self.assertEqual(loaded.version, 2)
                self.assertEqual(loaded.updated_at, later)

        def test_direct_deletes_rejected_before_foreign_key_checks(self):
            for row in self.immutable_rows():
                def deletion():
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(row._meta.db_table)), [row.pk])
                self.refused(deletion, marker="PZT_CA_DELETE_FORBIDDEN")
                self.assertTrue(type(row).objects.filter(pk=row.pk).exists())

        def test_truncate_leaf_tables_rejected(self):
            for name in ("result", "retirement"):
                table = self.graph[name]._meta.db_table
                def truncation():
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table)))
                self.refused(truncation, marker="PZT_CA_DELETE_FORBIDDEN")

        def test_trigger_catalog_covers_eight_tables_in_owned_schema(self):
            tables = {row._meta.db_table for row in self.immutable_rows()}
            with connections["default"].cursor() as cursor:
                cursor.execute("""SELECT c.relname, t.tgtype, t.tgenabled, pn.nspname
                    FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid
                    JOIN pg_namespace n ON n.oid=c.relnamespace
                    JOIN pg_proc p ON p.oid=t.tgfoid JOIN pg_namespace pn ON pn.oid=p.pronamespace
                    WHERE n.nspname=current_schema() AND c.relname=ANY(%s) AND NOT t.tgisinternal""", [list(tables)])
                rows = cursor.fetchall()
                cursor.execute("SELECT current_schema()")
                schema = cursor.fetchone()[0]
            self.assertEqual(len(rows), 24)
            for table in tables:
                selected = [row for row in rows if row[0] == table]
                self.assertEqual({row[1] for row in selected}, {11, 19, 34})
                self.assertTrue(all(row[2] == "O" and row[3] == schema for row in selected))

        def test_retirement_status_cannot_be_reactivated(self):
            for name in ("root", "generation"):
                row = self.graph[name]
                type(row).objects.filter(pk=row.pk).update(status="retired")
                self.refused(lambda row=row: type(row).objects.filter(pk=row.pk).update(status="active"), marker="PZT_CA_RETIRED_TERMINAL")
                self.assertEqual(type(row).objects.get(pk=row.pk).status, "retired")

        def test_selection_compare_and_swap_sequential(self):
            row = self.graph["selection"]
            changed = type(row).objects.filter(pk=row.pk, version=1, epoch="1").update(version=2, epoch="2", engagement_ref="engagement-test-2")
            stale = type(row).objects.filter(pk=row.pk, version=1, epoch="1").update(version=2, epoch="3", engagement_ref="engagement-test-3")
            self.assertEqual((changed, stale), (1, 0))
            loaded = type(row).objects.get(pk=row.pk)
            self.assertEqual((loaded.version, loaded.epoch), (2, "2"))
            loaded.clean()

        def test_epoch_above_64_bits_and_noncanonical_values(self):
            source = self.graph["operation"]
            fields = ("domain", "logical_authority", "emission_scope", "operation_version", "request_id", "context_ref",
                "input_fingerprint", "policy_ref", "content_sha256", "serializer_version")
            values = {field: getattr(source, field) for field in fields}
            big = store(m.CaOperationLink, **values, operation_id=source.operation_id + "-large", epoch=str(2**80))
            loaded = m.CaOperationLink.objects.get(pk=big.pk)
            loaded.clean()
            self.assertEqual(loaded.epoch, str(2**80))
            for index, invalid in enumerate(("01", "-1", "1.0", " 1", "١")):
                self.refused(lambda index=index, invalid=invalid: m.CaOperationLink.objects.create(**values,
                    operation_id=source.operation_id + "-invalid-" + str(index), epoch=invalid), constraint="pzt_ca_oplink_epoch_format")

        def test_serial_159_bit_boundary_and_sql_limits(self):
            extra = fixture(root_serial=m.SERIAL_MAX, intermediate_serial=m.SERIAL_MAX - 1)
            row = m.CaCertificate.objects.get(pk=extra["root_certificate"].pk)
            row.clean()
            self.assertEqual(row.serial_number, Decimal(m.SERIAL_MAX))
            source = self.graph["root_certificate"]
            values = {field.attname: getattr(source, field.attname)
                for field in source._meta.concrete_fields if field.name not in ("id", "cert_ref", "serial_number")}
            for number, constraint in ((0, "pzt_ca_cert_serial_positive"), (m.SERIAL_MAX + 1, "pzt_ca_cert_serial_max")):
                self.refused(lambda number=number: m.CaCertificate.objects.create(**values,
                    cert_ref=source.cert_ref + "-limit-" + str(number), serial_number=Decimal(number)), constraint=constraint)

        def test_uuid_v4_rejected_by_postgresql_constraint(self):
            issuer = self.graph["issuer"]
            self.refused(lambda: m.CaIssuer.objects.create(id=uuid.uuid4(), domain=issuer.domain,
                logical_authority=issuer.logical_authority + "-uuid4", emission_scope=issuer.emission_scope + "-uuid4",
                issuer_id=issuer.issuer_id + "-uuid4", issuer_role="principal"), constraint="pzt_ca_issuer_id_uuid7")

    return unittest.defaultTestLoader.loadTestsFromTestCase(RegistryStorageTests)


def main(arguments):
    if len(arguments) != 2 or arguments[0] != "--schema" or re.fullmatch(r"c02_[0-9a-f]{16}", arguments[1]) is None:
        return {"statut": "REFUS", "raison": "SCHEMA_EXPLICITE_REQUIS"}, 2
    if pathlib.Path(__file__).resolve().parents[3] != EXPECTED_ROOT:
        return {"statut": "REFUS", "raison": "RACINE_INATTENDUE"}, 2
    schema = arguments[1]
    sys.path.insert(0, str(EXPECTED_ROOT / "src"))
    sys.path.insert(0, str(EXPECTED_ROOT / "tests" / "integration"))
    from core_pg_test_support import (close_django_connections, create_schema, drop_schema_if_owned,
        managed_pg_connection, mask_output, pg_options, quote_search_path, read_project_env)

    refs = []
    close_failures = []
    result = None
    report = {"statut": "ECHEC", "phase": "configuration", "schema_supprime": False,
        "materiel_qualifie": False, "autorite_qualifiee": False, "concurrence_qualifiee": False,
        "crash_reprise_qualifiee": False, "restauration_qualifiee": False}
    django_ready = False
    with mask_output():
        try:
            config = read_project_env(str(EXPECTED_ROOT))
            if config is None:
                raise RuntimeError("CONFIGURATION_TEST_INDISPONIBLE")
            report["phase"] = "connexion"
            with managed_pg_connection(config["PG_HOST"], int(config["PG_PORT"]), config["PG_DATABASE"],
                config["PG_USERNAME"], config["PG_PASSWORD"], refs, close_failures, options=pg_options()) as admin:
                owned = False
                try:
                    report["phase"] = "creation_schema"
                    owned, code = create_schema(admin, schema)
                    if not owned or code != "NONE":
                        raise RuntimeError("CREATION_SCHEMA_REFUSEE")
                    options = pg_options(quote_search_path(admin, schema))
                    report["phase"] = "configuration_django"
                    from django.conf import settings
                    if settings.configured:
                        raise RuntimeError("PROCESSUS_DJANGO_NON_ISOLE")
                    settings.configure(SECRET_KEY="z12-test-public-fixture-never-production",
                        INSTALLED_APPS=["pixs.pzt_ca.apps.PixsPztCaConfig"], USE_TZ=True, TIME_ZONE="UTC",
                        LOGGING_CONFIG=None, MIDDLEWARE=(), DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
                        DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": config["PG_DATABASE"],
                            "USER": config["PG_USERNAME"], "PASSWORD": config["PG_PASSWORD"], "HOST": config["PG_HOST"],
                            "PORT": config["PG_PORT"], "CONN_MAX_AGE": 0, "ATOMIC_REQUESTS": False,
                            "OPTIONS": {"connect_timeout": 2, "options": options}}})
                    django_ready = True
                    import django
                    django.setup()
                    from django.db import connections
                    connection = connections["default"]
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT current_schema(), current_schemas(false)")
                        actual_schema, actual_path = cursor.fetchone()
                        if actual_schema != schema or actual_path != [schema]:
                            raise RuntimeError("ISOLATION_SCHEMA_INVALIDE")
                    report["phase"] = "migrations_schema_jetable"
                    from django.db.migrations.executor import MigrationExecutor
                    MigrationExecutor(connection).migrate([("pixs_pzt_ca", "0002_registry_guards")])
                    report["phase"] = "tests_stockage"
                    result = _SafeResult()
                    _suite().run(result)
                finally:
                    if django_ready:
                        try:
                            close_django_connections(refs, close_failures)
                        except Exception:
                            close_failures.append("ORM_CLOSE_UNEXPECTED")
                            report["fermeture_erreur"] = _safe_error(sys.exc_info())
                    if owned:
                        try:
                            report["schema_supprime"] = drop_schema_if_owned(admin, schema, owned)
                        except Exception:
                            report["suppression_erreur"] = _safe_error(sys.exc_info())
        except Exception:
            report["erreur"] = _safe_error(sys.exc_info())
    report["echecs_fermeture"] = len(close_failures)
    report["connexions_encore_ouvertes"] = sum(not bool(connection.closed) for connection in refs)
    report["cas_executes"] = 0 if result is None else result.testsRun
    report["erreurs"] = [] if result is None else result.errors
    report["echecs"] = [] if result is None else result.failures
    report["cas_ignores"] = 0 if result is None else len(result.skipped)
    success = (result is not None and result.testsRun == 11 and result.wasSuccessful()
        and not result.skipped and report["schema_supprime"] and not close_failures
        and report["connexions_encore_ouvertes"] == 0 and "erreur" not in report)
    report["statut"] = "REUSSI" if success else "ECHEC"
    return report, 0 if success else 1


if __name__ == "__main__":
    summary, exit_code = main(sys.argv[1:])
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    raise SystemExit(exit_code)
