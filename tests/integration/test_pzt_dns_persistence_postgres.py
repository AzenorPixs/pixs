"""Contraintes PZT/DNS sur PostgreSQL réel ; fixtures de stockage sans autorisation."""
from __future__ import annotations

EXPECTED_CASES = (
    "uuid7_generators", "uuid4_model_refused", "uuid4_database_refused",
    "pzt_platform_unique", "dns_platform_unique", "tenant_targets_separated",
    "scope_not_second_target", "platform_scope_refused", "negative_revision_refused",
    "dns_positive_ttl_refused", "dns_negative_ttl_refused", "dns_zero_ttl_roundtrip",
    "bool_ttl_model_refused", "text_v6_model_refused", "governance_collections_typed",
    "empty_governance_sets_accepted", "secret_references_roundtrip",
    "idempotence_platform_unique", "idempotence_tenant_separated",
    "idempotence_scope_not_dimension", "idempotence_result_roundtrip",
    "nulls_not_distinct_indexes", "name_unique", "zone_reference_protected",
    "owner_storage_rollback", "data_soft_deletion_no_duplicate", "migration_repeat", "business_state_separate", "opaque_scope_references_roundtrip",
)


def scenarios():
    import copy
    import datetime
    import uuid
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connection, transaction
    from django.db.models.deletion import ProtectedError
    from django.db.migrations.executor import MigrationExecutor
    from pixs.pzt import models as pzt
    from pixs.dns import models as dns
    from pixs.pzt.identifiers import new_uuid7, require_uuid7, PztIdentifierError
    from pixs.dns.identifiers import new_uuid7 as dns_uuid7, require_uuid7 as dns_require_uuid7

    cases = {}
    now = datetime.datetime.now(datetime.timezone.utc)
    tenant, other_tenant = "tenant-c14-opaque", " tenant-c14-autre "
    scope, other_scope = "scope-c14-opaque", " scope-c14-autre "

    def governance(owner):
        return {
            "profile_version": "1.0.0", "data_asset_id": owner + ".fixture-asset",
            "owner_component": owner, "source_of_truth": owner + ".postgresql",
            "data_classes": ["CONFIGURATION"], "confidentiality": "INTERNAL",
            "personal_data": "NONE", "purpose_refs": [], "retention_policy": "fixture-retention",
            "deletion_policy": "fixture-deletion", "residency_constraints": [],
            "authorized_consumers": [], "processor_refs": [],
            "export_policy": "fixture-export", "lineage": "fixture-lineage",
        }

    def desired(model, resource, tenant_id=None, scope_id=None, **updates):
        owner = "pixs.pzt" if model is pzt.DesiredPztRecord else "pixs.dns"
        values = dict(
            resource_id=resource, tenant_id=tenant_id, scope_id=scope_id,
            scope_type="PLATFORM" if tenant_id is None else "TENANT", config_revision=1,
            governance=governance(owner), secret_refs=[], payload_sha256="a" * 64,
            serializer_version="1.0.0", created_at=now, updated_at=now,
            governance_ref=owner + ".fixture-asset", confidentiality="INTERNAL", personal="NONE",
        )
        if model is pzt.DesiredPztRecord:
            values.update(v6_enabled=False, plan_ref="fixture-plan", budget_ref="fixture-budget")
            values["config"] = dict(schema_version="1.0.0", plan_ref="fixture-plan",
                                    budget_ref="fixture-budget", v6_enabled=False)
        else:
            values.update(suffix="fixture.invalid", ttl_positive=0, ttl_negative=0, views=["private"])
            values["config"] = dict(schema_version="1.0.0", suffix="fixture.invalid",
                                    ttl_positive=0, ttl_negative=0, views=["private"])
        values.update(updates)
        return model(**values)

    def save(row):
        row.full_clean()
        row.save()
        return row

    def clone(row, **updates):
        fields = {f.attname: copy.deepcopy(getattr(row, f.attname))
                  for f in row._meta.concrete_fields if not f.primary_key}
        fields.update(updates)
        return type(row)(**fields)

    def rejected_database(name, action, state, constraint=None):
        try:
            with transaction.atomic():
                action()
        except IntegrityError as error:
            cause = error.__cause__
            diag = getattr(cause, "diag", None)
            cases[name] = (getattr(cause, "sqlstate", None) == state and
                           (constraint is None or getattr(diag, "constraint_name", None) == constraint))
        else:
            cases[name] = False

    def rejected_model(name, row):
        try:
            row.clean()
        except ValidationError:
            cases[name] = True
        else:
            cases[name] = False

    identifiers = [new_uuid7() for _ in range(32)] + [dns_uuid7() for _ in range(32)]
    cases["uuid7_generators"] = (len(set(identifiers)) == 64 and
        all(require_uuid7(value) == value and dns_require_uuid7(value) == value for value in identifiers))
    try:
        require_uuid7(uuid.uuid4())
    except PztIdentifierError:
        invalid_uuid = True
    else:
        invalid_uuid = False
    invalid = desired(pzt.DesiredPztRecord, "pixs.pzt.fixture:bad-uuid", id=uuid.uuid4())
    rejected_model("uuid4_model_refused", invalid)
    cases["uuid4_model_refused"] = cases["uuid4_model_refused"] and invalid_uuid

    platform_pzt = save(desired(pzt.DesiredPztRecord, "pixs.pzt.fixture:shared"))
    platform_dns = save(desired(dns.DesiredDnsRecord, "pixs.dns.fixture:shared"))
    rejected_database("uuid4_database_refused",
        lambda: clone(platform_pzt, resource_id="pixs.pzt.fixture:uuid4", id=uuid.uuid4()).save(),
        "23514", "desiredpztrecord_id_uuid7")
    rejected_database("pzt_platform_unique", lambda: clone(platform_pzt).save(),
                      "23505", "pzt_desired_tenant_res_uq")
    rejected_database("dns_platform_unique", lambda: clone(platform_dns).save(),
                      "23505", "dns_desired_tenant_res_uq")
    tenant_pzt = save(desired(pzt.DesiredPztRecord, platform_pzt.resource_id, tenant, scope))
    other_pzt = save(desired(pzt.DesiredPztRecord, platform_pzt.resource_id, other_tenant))
    cases["tenant_targets_separated"] = len({platform_pzt.pk, tenant_pzt.pk, other_pzt.pk}) == 3
    tenant_pzt.refresh_from_db()
    other_pzt.refresh_from_db()
    cases["opaque_scope_references_roundtrip"] = (
        tenant_pzt.tenant_id == tenant and tenant_pzt.scope_id == scope
        and other_pzt.tenant_id == other_tenant
    )
    rejected_database("scope_not_second_target", lambda: clone(tenant_pzt, scope_id=other_scope).save(),
                      "23505", "pzt_desired_tenant_res_uq")
    rejected_database("platform_scope_refused",
        lambda: clone(platform_pzt, resource_id="pixs.pzt.fixture:scope", scope_id=scope).save(),
        "23514", "pzt_desired_scope_coherence")
    rejected_database("negative_revision_refused",
        lambda: clone(platform_pzt, resource_id="pixs.pzt.fixture:revision", config_revision=0).save(),
        "23514", "pzt_desired_rev_gte1")
    rejected_database("dns_positive_ttl_refused",
        lambda: clone(platform_dns, resource_id="pixs.dns.fixture:ttl-positive", ttl_positive=31).save(),
        "23514", "dns_desired_ttl_pos_0_30")
    rejected_database("dns_negative_ttl_refused",
        lambda: clone(platform_dns, resource_id="pixs.dns.fixture:ttl-negative", ttl_negative=6).save(),
        "23514", "dns_desired_ttl_neg_0_5")
    platform_dns.refresh_from_db()
    cases["dns_zero_ttl_roundtrip"] = platform_dns.ttl_positive == platform_dns.ttl_negative == 0
    rejected_model("bool_ttl_model_refused", clone(platform_dns, ttl_positive=True))
    rejected_model("text_v6_model_refused", clone(platform_pzt, v6_enabled="false"))
    invalid_gov = governance("pixs.pzt")
    invalid_gov["data_classes"] = "CONFIGURATION"
    rejected_model("governance_collections_typed", clone(platform_pzt, governance=invalid_gov))
    empty = governance("pixs.pzt")
    empty["data_classes"] = []
    empty_record = save(desired(pzt.DesiredPztRecord, "pixs.pzt.fixture:empty", governance=empty))
    cases["empty_governance_sets_accepted"] = empty_record.governance["data_classes"] == []
    refs = [{"owner_id": "pixs.pzt", "entry_id": "fixture-reference", "source": "fixture-port"}]
    referenced = save(desired(pzt.DesiredPztRecord, "pixs.pzt.fixture:refs", secret_refs=refs))
    referenced.refresh_from_db()
    cases["secret_references_roundtrip"] = referenced.secret_refs == refs

    def idem(model, tenant_id=None, scope_id=None, **updates):
        with connection.cursor() as cursor:
            cursor.execute("SELECT txid_current()")
            xid = cursor.fetchone()[0]
        values = dict(
            tenant_id=tenant_id, subject_id="fixture-subject", command_type="fixture-command",
            idempotency_key="fixture-key", payload_sha256="b" * 64, serializer_version="1.0.0",
            operation_id="fixture-operation", transaction_token="fixture-transaction",
            staged_xid=xid, scope_type="PLATFORM" if tenant_id is None else "TENANT", scope_id=scope_id,
            # Durée synthétique de fixture, aucune politique de production déduite.
            expires_at=now + datetime.timedelta(minutes=1), state="IN_PROGRESS", result={},
            result_version=1, created_at=now, updated_at=now,
        )
        values.update(updates)
        return model(**values)

    for model, prefix in ((pzt.PztIdempotenceRecord, "pzt"), (dns.DnsIdempotenceRecord, "dns")):
        first = save(idem(model))
        rejected_database("idempotence_platform_unique_" + prefix, lambda: clone(first).save(),
                          "23505", prefix + "_idem_4dim_uq")
        scoped = save(idem(model, tenant, scope))
        second = save(idem(model, other_tenant))
        cases["idempotence_tenant_separated_" + prefix] = len({first.pk, scoped.pk, second.pk}) == 3
        rejected_database("idempotence_scope_not_dimension_" + prefix,
            lambda: clone(scoped, scope_id=other_scope, payload_sha256="c" * 64).save(),
            "23505", prefix + "_idem_4dim_uq")
        first.state = "SUCCEEDED"
        first.result = dict(operation_id=first.operation_id, resource_id=(platform_pzt.resource_id if prefix == "pzt" else platform_dns.resource_id),
                            config_revision=1, outcome="SUCCEEDED", audit_disposition="AUDITED")
        save(first)
        first.refresh_from_db()
        cases["idempotence_result_roundtrip_" + prefix] = first.result["outcome"] == "SUCCEEDED"
    for case in ("idempotence_platform_unique", "idempotence_tenant_separated",
                 "idempotence_scope_not_dimension", "idempotence_result_roundtrip"):
        pzt_result, dns_result = cases.pop(case + "_pzt"), cases.pop(case + "_dns")
        cases[case] = pzt_result and dns_result

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT c.relname,i.indnullsnotdistinct FROM pg_index i "
            "JOIN pg_class c ON c.oid=i.indexrelid "
            "JOIN pg_namespace n ON n.oid=c.relnamespace "
            "WHERE n.nspname=current_schema() AND c.relname IN (%s,%s)",
            ("pzt_idem_4dim_uq", "dns_idem_4dim_uq"),
        )
        indexes = dict(cursor.fetchall())
    cases["nulls_not_distinct_indexes"] = indexes == {
        "pzt_idem_4dim_uq": True, "dns_idem_4dim_uq": True,
    }

    name = save(dns.DnsNameRecord(
        zone=platform_dns, name="fixture", name_key="fixture", view="private", target_ref="fixture-target",
        created_at=now, updated_at=now,
    ))
    rejected_database("name_unique", lambda: clone(name).save(),
                      "23505", "dns_name_zone_name_view_uq")
    try:
        platform_dns.delete()
    except ProtectedError:
        cases["zone_reference_protected"] = True
    else:
        cases["zone_reference_protected"] = False

    class FixtureRollback(Exception):
        pass

    try:
        with transaction.atomic():
            save(desired(pzt.DesiredPztRecord, "pixs.pzt.fixture:rollback"))
            save(desired(dns.DesiredDnsRecord, "pixs.dns.fixture:rollback"))
            raise FixtureRollback()
    except FixtureRollback:
        cases["owner_storage_rollback"] = (
            not pzt.DesiredPztRecord.objects.filter(resource_id="pixs.pzt.fixture:rollback").exists()
            and not dns.DesiredDnsRecord.objects.filter(resource_id="pixs.dns.fixture:rollback").exists()
        )
    retired = save(desired(
        pzt.DesiredPztRecord, "pixs.pzt.fixture:retired",
        business_state="RETIRED", version=2, config_revision=2,
    ))
    cases["business_state_separate"] = (
        retired.business_state == "RETIRED" and retired.persistence_state == "ACTIVE"
        and retired.retention_state == "RETAINED"
    )
    platform_pzt.persistence_state = "SOFT_DELETED"
    save(platform_pzt)
    rejected_database("data_soft_deletion_no_duplicate", lambda: clone(platform_pzt).save(),
                      "23505", "pzt_desired_tenant_res_uq")
    targets = [("pixs_pzt", "0001_initial"), ("pixs_dns", "0001_initial")]
    cases["migration_repeat"] = MigrationExecutor(connection).migration_plan(targets) == []
    return cases


def run(root_str):
    from c14_pg_test_support import run_in_c14_schema
    return run_in_c14_schema(root_str, scenarios, EXPECTED_CASES)
