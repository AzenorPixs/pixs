"""Recette PG publication Auth/C05 reelle via F1+F2, sans lecture privee C05.

Combine publication_fixture F1 et builders() F2 puis publish_bootstrap_authorization
sur schema jetable c03_* (support auth, with_core 0002_core_audit). Aucun import
pixs/Django a l'import : chemins prepares explicitement (tests + src derives de
la racine verifiee), tout le reste est charge apres setup. Aucune lecture de
project.env : le support charge, masque et redige. Aucune lecture des tables
privees C05 : l'autorite est le contrat public (reference retournee +
verification interne du publisher) ; seuls les faits Auth et les refus sont
observes. Aucun mock. Tout reste NON EXECUTE tant qu'un mandat phase2 distinct
ne l'ordonne pas.
"""
from __future__ import annotations

EXPECTED_CASES = (
    "nominal_publication_reelle",
    "republication_meme_operation_sans_reset_refusee",
    "integrite_fichier_signature_refusee_sans_ligne",
    "integrite_fichier_politique_refusee_sans_ligne",
    "draft_substitue_refuse_sans_ligne",
    "politique_test_courante_divergente_refusee_rollback",
    "session_fermee_refus_diagnostique",
    "cleanup_fermeture_prouves",
)

# Non couvert par conception (API necessaire absente, rien n'est simule) :
# - tamper du plan F2 (chemins internes aux builders, non exposes) ;
# - etat COMMITTED/UNKNOWN force (aucun forcage deterministe sans mock) ;
# - echange E5 1.1 (adopte, non realise, hors lot).
NON_COVERED = (
    "plan_file_tamper",
    "forced_committed_unknown_state",
    "e5_exchange",
)

_FUTURE_COMMAND = ("/home/devops/datas/pixs/.venv/bin/python3 "
                   "/home/devops/datas/pixs/tests/integration/"
                   "test_auth_bootstrap_publication_postgres.py")


def _prepare_project_paths(root_str):
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import core_pg_test_support as support
    from pathlib import Path
    try:
        resolved = str(Path(root_str).resolve())
    except (OSError, RuntimeError, ValueError):
        raise RuntimeError("ROOT_UNPROVED")
    if resolved != support.EXPECTED_ROOT:
        raise RuntimeError("ROOT_UNPROVED")
    src = os.path.join(resolved, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return resolved


def run_real_auth_bootstrap_publication_pg(root_str):
    _prepare_project_paths(root_str)
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": False, "conns_closed": False,
           "code": "NONE", "phase": "INIT", "failure_type": "NONE"}
    with support.mask_output():
        try:
            import auth_pg_test_support as harness
            res = harness.run_in_auth_schema(
                root_str, lambda: _cases(root_str), EXPECTED_CASES,
                with_core=True, core_target="0002_core_audit")
            for key in ("cases", "cleanup", "conns_closed", "code", "failure_type",
                        "pg_version_num", "django_version", "namespace",
                        "migration", "core_migration"):
                if key in res:
                    out[key] = res[key]
            out["phase"] = "HARNESS_DONE"
            ok = (out.get("code") == "NONE"
                  and type(out.get("cases")) is dict
                  and set(out["cases"]) == set(EXPECTED_CASES)
                  and all(type(v) is bool and v for v in out["cases"].values())
                  and out.get("cleanup") is True and out.get("conns_closed") is True)
            out["real_pg"] = bool(ok)
            if not ok and out.get("code") == "NONE":
                out["code"] = "CASE_UNPROVED"
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            out["real_pg"] = False
    return out


def _cases(root_str):
    import dataclasses
    import datetime
    import os
    import shutil
    import tempfile
    from pixs.auth.bootstrap_publication import (
        BootstrapPublicationError, BootstrapPublicationReference,
        publish_bootstrap_authorization)
    from pixs.auth.bootstrap_session import AuthBootstrapSessionError
    from pixs.auth.configuration import InitialLocalAuthSelection
    from pixs.auth.identifiers import new_uuid7
    from pixs.auth.policy import SessionCategory, default_rule
    from pixs.auth.runtime_verifier import (
        FederationTrust, IdentityAssurance, LocalTrustProfile)
    from pixs.core.audit_contracts import AuditError, AuditPolicy
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from auth_bootstrap_builders import builders
    from auth_bootstrap_publication_fixture import publication_fixture

    cases = {}
    pairs = []
    ctx = ScopeContext(ScopeType.PLATFORM)

    class Clock:
        def now(self):
            return datetime.datetime.now(datetime.timezone.utc)

    class SwitchableAuditPolicySource:
        """Double declare : P1 a la premiere resolution, P2 ensuite.

        Protocole public resolve(context, alias) uniquement. Instrumente en
        local TEST : trace des versions et observation reelle de la ligne
        Auth (table possedee par cette recette) a la premiere resolution,
        le publisher appelant audit.policy apres row.save.
        """

        def __init__(self, approved_context, first_policy, later_policy, operation_id):
            if type(approved_context) is not ScopeContext:
                raise AuditError()
            if type(first_policy) is not AuditPolicy or type(later_policy) is not AuditPolicy:
                raise AuditError()
            first_policy.__post_init__()
            later_policy.__post_init__()
            if type(operation_id) is not str or not operation_id:
                raise AuditError()
            self._approved = approved_context
            self._first, self._later = first_policy, later_policy
            self._operation_id = operation_id
            self._calls = 0
            self.trace = []
            self.observed = {"row_present_at_first_resolve": None}

        def resolve(self, *, context, alias):
            if type(alias) is not str or alias == "" or type(context) is not ScopeContext:
                raise AuditError()
            if context != self._approved:
                raise AuditError()
            self._calls += 1
            policy = self._first if self._calls == 1 else self._later
            self.trace.append(policy.policy_version)
            if self._calls == 1:
                from pixs.auth import models as m
                self.observed["row_present_at_first_resolve"] = m.AuthBootstrapAuthorization.objects.using(alias).filter(operation_ref=self._operation_id).exists()
            return policy

    clock = Clock()

    def refused(name, action, kinds):
        try:
            action()
        except kinds:
            cases[name] = True
        else:
            cases[name] = False

    now = clock.now()
    profile = LocalTrustProfile(
        "pixs.auth.local", "1.0.0", "local", "qualified.local", FederationTrust.TRUSTED)
    selection = InitialLocalAuthSelection(
        profile, "fixture-authpub-pg", now, now + datetime.timedelta(days=1),
        IdentityAssurance.CLAIMED, "authpub-pg-initial-claim",
        (default_rule(SessionCategory.ORDINARY), default_rule(SessionCategory.ADMIN)))
    policy = AuditPolicy(
        "authpub:c05", "1", "authpub:fixture", 1, 65536, 50, (),
        "authpub:asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
    tmpdir = tempfile.mkdtemp(prefix="authpub-pg-", dir=root_str)
    try:
        base = dict(alias="default", clock=clock, max_password_bytes=1024, workdir=tmpdir,
                    installation_ref="installation-authpub-pg", key_id="key-authpub-pg",
                    trust_policy_version="1.0.0", selection=selection, audit_policy=policy,
                    peer_alias="peer", component_version="1.0.0",
                    closed_effects=("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"))

        def fixture_kwargs(operation_id, target_identity_ref):
            return dict(base, operation_id=operation_id,
                        target_identity_ref=target_identity_ref)

        def target_ref():
            return "pixs.core.identity:" + str(new_uuid7())

        from pixs.auth import models as m

        def count_for(operation_id):
            return m.AuthBootstrapAuthorization.objects.using("default").filter(
                operation_ref=operation_id).count()

        # 1. nominal.
        op1, tgt1 = "operation-authpub-pg-1", target_ref()
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op1, tgt1)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                ref = publish_bootstrap_authorization(**fx["kwargs"])
                ok = type(ref) is BootstrapPublicationReference
                ok = ok and all(type(getattr(ref, n)) is str and getattr(ref, n)
                                for n in ("authorization_ref", "operator_proof_ref",
                                          "resource_ref", "operation_id", "audit_event_ref"))
                row = m.AuthBootstrapAuthorization.objects.using("default").get(
                    authorization_ref=ref.authorization_ref)
                ok = ok and row.version == 1 and row.persistence_state == "ACTIVE"
                ok = ok and row.retention_state == "RETAINED"
                ok = ok and row.plan_sha256 == fx["challenge"].facts.plan_sha256
                ok = ok and row.operation_ref == op1 and row.target_identity_ref == tgt1
                ok = ok and row.consumed_operation_ref is None
                ok = ok and count_for(op1) == 1
                stable = fx["plan_binding"].resolve_challenge(
                    fx["draft"], alias=fx["session"].using,
                    operation_id=fx["draft"].operation_id)
                ok = ok and stable is fx["challenge"]
                cases["nominal_publication_reelle"] = bool(ok)

        # 2. republication meme operation sans reset.
        op2, tgt2 = "operation-authpub-pg-2", target_ref()
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op2, tgt2)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                publish_bootstrap_authorization(**fx["kwargs"])
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op2, target_ref())) as fx:
                pairs.append((fx["session"], fx["draft"]))
                refused("republication_meme_operation_sans_reset_refusee",
                        lambda: publish_bootstrap_authorization(**fx["kwargs"]),
                        (BootstrapPublicationError,))
        if cases.get("republication_meme_operation_sans_reset_refusee") is True:
            cases["republication_meme_operation_sans_reset_refusee"] = count_for(op2) == 1

        # 3. integrite fichier signature (pas cryptographie).
        op3, tgt3 = "operation-authpub-pg-3", target_ref()
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op3, tgt3)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                with open(fx["dir"] + "/signature.bin", "r+b") as handle:
                    handle.write(b"\x00" * 64)
                refused("integrite_fichier_signature_refusee_sans_ligne",
                        lambda: publish_bootstrap_authorization(**fx["kwargs"]),
                        (BootstrapPublicationError,))
        if cases.get("integrite_fichier_signature_refusee_sans_ligne") is True:
            cases["integrite_fichier_signature_refusee_sans_ligne"] = count_for(op3) == 0

        # 4. integrite fichier politique (pas politique courante semantique).
        op4, tgt4 = "operation-authpub-pg-4", target_ref()
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op4, tgt4)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                with open(fx["dir"] + "/policy.json", "wb") as handle:
                    handle.write(b"{}")
                refused("integrite_fichier_politique_refusee_sans_ligne",
                        lambda: publish_bootstrap_authorization(**fx["kwargs"]),
                        (BootstrapPublicationError,))
        if cases.get("integrite_fichier_politique_refusee_sans_ligne") is True:
            cases["integrite_fichier_politique_refusee_sans_ligne"] = count_for(op4) == 0

        # 5. draft etranger : copie VALIDE, champs identiques, autre instance.
        op5, tgt5 = "operation-authpub-pg-5", target_ref()
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op5, tgt5)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                foreign = dataclasses.replace(fx["draft"])
                kwargs_sub = dict(fx["kwargs"])
                kwargs_sub["draft"] = foreign
                try:
                    publish_bootstrap_authorization(**kwargs_sub)
                    cases["draft_substitue_refuse_sans_ligne"] = False
                except AuthBootstrapSessionError:
                    cases["draft_substitue_refuse_sans_ligne"] = count_for(op5) == 0

        # 6. politique TEST divergente : P1 puis P2, rollback prouve.
        op6, tgt6 = "operation-authpub-pg-6", target_ref()
        later = dataclasses.replace(policy, policy_version="2")
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op6, tgt6)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                switch = SwitchableAuditPolicySource(ctx, policy, later, op6)
                participant = PostgresAuditParticipant(switch, clock, "peer")
                kwargs_sw = dict(fx["kwargs"])
                kwargs_sw["audit"] = participant
                try:
                    publish_bootstrap_authorization(**kwargs_sw)
                    cases["politique_test_courante_divergente_refusee_rollback"] = False
                except BootstrapPublicationError as error:
                    cases["politique_test_courante_divergente_refusee_rollback"] = bool(
                        error.code == "AUTH_BOOTSTRAP_PUBLICATION_INVALID"
                        and switch.trace[:2] == ["1", "2"]
                        and switch.observed["row_present_at_first_resolve"] is True
                        and count_for(op6) == 0)

        # 7. session fermee.
        op7, tgt7 = "operation-authpub-pg-7", target_ref()
        with builders(workdir=tmpdir) as (mw, mc):
            with publication_fixture(make_writer=mw, make_classification=mc,
                                     **fixture_kwargs(op7, tgt7)) as fx:
                pairs.append((fx["session"], fx["draft"]))
                fx["session"].close()
                refused("session_fermee_refus_diagnostique",
                        lambda: publish_bootstrap_authorization(**fx["kwargs"]),
                        (BootstrapPublicationError, AuthBootstrapSessionError))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=False)

    # 8. cleanup/fermeture prouves sur chemins de la recette seule.
    tmpdir_gone = not os.path.exists(tmpdir)
    closed = True
    for session, draft in pairs:
        try:
            session.describe(draft)
            closed = False
        except AuthBootstrapSessionError:
            pass
    cases["cleanup_fermeture_prouves"] = bool(tmpdir_gone and closed)
    return cases


def _main(argv):
    import json as _json
    import sys as _sys
    if type(argv) is not list or argv != []:
        print(_json.dumps({"real_pg": False, "code": "ARGS_INVALID"}))
        return 2
    here = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
    if here not in _sys.path:
        _sys.path.insert(0, here)
    import core_pg_test_support as _support
    from pathlib import Path as _Path
    root = str(_Path(__file__).resolve().parent.parent.parent)
    if root != _support.EXPECTED_ROOT:
        print(_json.dumps({"real_pg": False, "code": "ROOT_UNPROVED"}))
        return 2
    src = __import__("os").path.join(root, "src")
    if src not in _sys.path:
        _sys.path.insert(0, src)
    out = run_real_auth_bootstrap_publication_pg(root)
    public = {}
    for key in ("real_pg", "cases", "cleanup", "conns_closed", "code", "phase",
                "failure_type", "pg_version_num", "django_version", "namespace",
                "migration", "core_migration"):
        value = out.get(key)
        if type(value) in (bool, str) or value is None:
            public[key] = value
        elif key == "cases" and type(value) is dict and all(
                type(k) is str and type(v) is bool for k, v in value.items()):
            public[key] = dict(value)
    print(_json.dumps(public, sort_keys=True))
    return 0 if out.get("real_pg") is True else 1


if __name__ == "__main__":
    import sys as _sys_main
    raise SystemExit(_main(_sys_main.argv[1:]))
