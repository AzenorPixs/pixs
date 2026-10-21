"""Recette C04 PostgreSQL réelle : validation des déclarations et reçus SQL.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Migrations Core et lignes persistantes réelles ; aucun credential ou runtime Auth qualifié.
"""
from __future__ import annotations

import re

_CASES = ("hors_transaction_refuse","permission_proprietaire_catalogue_litteraux","validation_sans_ligne_sql_pas_preuve","permission_sql_reelle_et_commit","recu_copie_refuse","recu_nouvelle_transaction_refuse","contenu_permission_substitue_refuse","savepoint_rollback_recu_invalide","policy_catalogue_erreur_port","policy_sql_reelle","policy_version_active_ambigue_refusee","policy_colonnes_substituees_refusees","operation_alias_substitues_refuses","toutes_les_references_verifiees",)


def run_real_runtime_declarations(root_str: str) -> dict:
    import core_pg_test_support as support

    out = {"real_pg": False, "cases": {}, "cleanup": False,
           "conns_closed": False, "code": "NONE", "pg_version_num": ""}
    refs, failures, schemas = [], [], []
    configured = False
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_REFUSE")
            with support.managed_pg_connection(
                env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures,
            ) as admin:
                try:
                    for _ in range(2):
                        name = support.safe_schema_name()
                        owned, reason = support.create_schema(admin, name)
                        if owned:
                            schemas.append(name)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                    aliases = {}
                    for alias, name in (("default", schemas[0]), ("peer", schemas[0]),
                                        ("other", schemas[1])):
                        aliases[alias] = {
                            "dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"],
                            "password": env["PG_PASSWORD"], "host": env["PG_HOST"],
                            "port": env["PG_PORT"],
                            "options": support.pg_options(support.quote_search_path(admin, name)),
                        }
                    support.configure_django_core_pg(aliases)
                    configured = True
                    import django
                    django.setup()
                    from django.db import connections
                    with connections["default"].cursor() as cursor:
                        cursor.execute("SELECT current_setting('server_version_num')")
                        version = cursor.fetchone()[0]
                    if type(version) is not str or re.fullmatch(r"[0-9]+", version) is None:
                        raise RuntimeError("VERSION_NON_PROUVEE")
                    out["pg_version_num"] = version
                    from pixs.core.migration_lock import run_core_initial
                    run_core_initial("default", origin=None, target="0.1.0")
                    _scenarios(out)
                finally:
                    if configured:
                        support.close_django_connections(refs, failures)
                    cleanup = [support.drop_schema_if_owned(admin, name, True)
                               for name in reversed(schemas)]
                    out["cleanup"] = len(cleanup) == 2 and all(cleanup)
        except Exception as error:
            # Frontière de sortie : aucun message ou détail de connexion.
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            import traceback
            out["trace"] = [(f.filename.rsplit("/", 1)[-1], f.lineno, f.name)
                            for f in traceback.extract_tb(error.__traceback__)[-8:]]
        finally:
            out["conns_closed"] = not failures and all(bool(c.closed) for c in refs)
    out["real_pg"] = (
        out["code"] == "NONE" and out["cleanup"] and out["conns_closed"]
        and set(out["cases"]) == set(_CASES) and all(out["cases"].values())
    )
    if not out["real_pg"] and out["code"] == "NONE":
        out["code"] = "CAS_NON_PROUVE"
    return out


def _scenarios(result):
    import datetime
    from dataclasses import replace
    from django.db import transaction
    from pixs.core.authz.policy import Policy, Effect, Selector, ScopeSelector, Obligation
    from pixs.core.authz.ports import Request
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_identity import CoreIdentity, CoreSuperAdminBinding
    from pixs.core.persistence.models_authz import CorePermission, CorePolicy, encode_policy
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.ports import StagedRef, TransactionProof, CorePortError
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_declarations import RuntimeDeclarationValidator

    context = ScopeContext(ScopeType.PLATFORM)
    identity = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="HUMAN", state="ACTIVE")
    CoreSuperAdminBinding.objects.create(installation_ref="declaration-install", identity=identity)
    subject = "pixs.core.identity:" + str(identity.pk)
    request = Request("declaration:decision", subject, "r:declare", "declare", context, "corr:declaration")
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    catalog = Catalog((subject,), ("r:declare", "r:business"), ("declare", "execute"), (context,), ())
    store = CoreAuthorizationStore(alias="default", installation_ref="declaration-install",
        base_epoch="declaration-epoch", catalog=catalog, limits=limits)
    validator = RuntimeDeclarationValidator(store=store, request=request, operation_id="op:declaration",
        owners=("pixs.core",))
    def mark(name): result["phase"] = name
    def passed(): result["cases"][result["phase"]] = True
    def refuse(fn):
        try: fn()
        except (CorePortError, CoreServiceError): return
        raise AssertionError("REFUS_ATTENDU")
    def permission(pid="perm-one", **changes):
        data = dict(permission_id=pid, owner="pixs.core", resource_ref="r:business",
            action_ref="execute", alias="default", operation_id="op:declaration",
            transaction_token="tx:declaration", context=context)
        data.update(changes)
        return validator.validate_permission(**data)
    def proof(ref, token="tx:declaration"):
        return TransactionProof("op:declaration", "default", token, context,
            (ref,), datetime.datetime.now(datetime.timezone.utc))
    def persist_permission(pid="perm-one", **changes):
        data = dict(permission_id=pid, owner="pixs.core", resource_ref="r:business", action_ref="execute")
        data.update(changes)
        return CorePermission.objects.create(**data)
    def policy(pid="policy-one", version="v1", resource="r:business"):
        return Policy(pid, version, "pixs.core", Effect.ALLOW, Selector("subject", (subject,)),
            Selector("resource", (resource,)), Selector("action", ("execute",)),
            ScopeSelector((context,)), obligations=(Obligation("AUDIT"),))
    def validate_policy(value):
        return validator.validate_policy(policy=value, alias="default", operation_id="op:declaration",
            transaction_token="tx:declaration", context=context)
    def persist_policy(value):
        return CorePolicy.objects.create(policy_id=value.policy_id, policy_version=value.policy_version,
            owner=value.owner, effect=value.effect.value, definition=encode_policy(value))

    mark("hors_transaction_refuse")
    refuse(permission)
    passed()
    mark("permission_proprietaire_catalogue_litteraux")
    with transaction.atomic():
        refuse(lambda: permission(owner="unknown.owner"))
        refuse(lambda: permission(resource_ref="r:unknown"))
        refuse(lambda: permission(action_ref="unknown"))
        refuse(lambda: permission(resource_ref="*"))
        refuse(lambda: permission(permission_id="resourceType:alias"))
        passed()

    mark("validation_sans_ligne_sql_pas_preuve")
    with transaction.atomic():
        ref = permission()
        refuse(lambda: validator.verify_staged(proof(ref)))
        passed()

    mark("permission_sql_reelle_et_commit")
    with transaction.atomic():
        ref = permission()
        persist_permission()
        assert validator.verify_staged(proof(ref)) is None
        assert not CorePermission.objects.using("peer").filter(permission_id="perm-one").exists()
    assert CorePermission.objects.using("peer").filter(permission_id="perm-one").exists()
    passed()

    mark("recu_copie_refuse")
    with transaction.atomic():
        ref = permission("perm-copy")
        persist_permission("perm-copy")
        refuse(lambda: validator.verify_staged(proof(replace(ref))))
        passed()
        transaction.set_rollback(True)

    mark("recu_nouvelle_transaction_refuse")
    with transaction.atomic():
        ref = permission("perm-tx")
        persist_permission("perm-tx")
    with transaction.atomic():
        refuse(lambda: validator.verify_staged(proof(ref)))
        passed()

    mark("contenu_permission_substitue_refuse")
    with transaction.atomic():
        ref = permission("perm-swap")
        persist_permission("perm-swap", resource_ref="r:declare")
        refuse(lambda: validator.verify_staged(proof(ref)))
        passed()
        transaction.set_rollback(True)

    mark("savepoint_rollback_recu_invalide")
    with transaction.atomic():
        try:
            with transaction.atomic():
                ref = permission("perm-savepoint")
                persist_permission("perm-savepoint")
                raise LookupError("SYNTHETIC_ROLLBACK")
        except LookupError:
            pass
        refuse(lambda: validator.verify_staged(proof(ref)))
        assert not CorePermission.objects.filter(permission_id="perm-savepoint").exists()
        passed()

    mark("policy_catalogue_erreur_port")
    with transaction.atomic():
        refuse(lambda: validate_policy(policy(resource="r:unknown")))
        passed()

    mark("policy_sql_reelle")
    with transaction.atomic():
        value = policy()
        ref = validate_policy(value)
        refuse(lambda: validator.verify_staged(proof(ref)))
        persist_policy(value)
        assert validator.verify_staged(proof(ref)) is None
    passed()

    mark("policy_version_active_ambigue_refusee")
    with transaction.atomic():
        refuse(lambda: validate_policy(policy(version="v2")))
        passed()

    mark("policy_colonnes_substituees_refusees")
    with transaction.atomic():
        value = policy(pid="policy-substituted")
        ref = validate_policy(value)
        row = persist_policy(value)
        row.owner = "other.owner"
        row.save(update_fields=("owner",))
        refuse(lambda: validator.verify_staged(proof(ref)))
        passed()
        transaction.set_rollback(True)

    mark("operation_alias_substitues_refuses")
    with transaction.atomic():
        refuse(lambda: permission("perm-op", operation_id="other"))
        refuse(lambda: permission("perm-alias", alias="peer"))
        passed()

    mark("toutes_les_references_verifiees")
    with transaction.atomic():
        one = permission("perm-all-one")
        two = permission("perm-all-two")
        persist_permission("perm-all-one")
        assembled = TransactionProof("op:declaration", "default", "tx:declaration", context,
            (one, two), datetime.datetime.now(datetime.timezone.utc))
        refuse(lambda: validator.verify_staged(assembled))
        persist_permission("perm-all-two")
        assert validator.verify_staged(assembled) is None
        passed()
        transaction.set_rollback(True)
