"""Participant R01 Auth sur PG ; plan/Core/classification doublés explicitement."""
from __future__ import annotations

EXPECTED_CASES = ("verify_no_mutation", "outside_tx_refused", "stamp_real_rows", "consumption_real", "final_projection_private", "proof_real", "proof_wrong_token", "other_invocation_no_projection", "after_commit_consumed", "after_commit_no_restamp", "rollback_real", "rollback_old_receipt_refused", "rollback_new_invocation_retry", "expiry_boundary_refused", "revoked_key_refused", "key_withdrawn_after_stage", "plan_changed_refused", "prepared_mapping_bound", "target_missing_refused", "classification_missing_refused", "wrong_target_refused", "wrong_alias_refused", "classification_changed_refused", "concurrent_single_consumer")


def scenarios():
    import datetime
    import hashlib
    import secrets
    import threading
    import time
    from dataclasses import replace
    from django.db import connections, transaction, DatabaseError
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    from pixs.auth import models as m
    from pixs.auth.identifiers import new_uuid7, identity_reference, parse_identity_reference
    from pixs.auth.passwords import hash_password, verify_password
    from pixs.auth.bootstrap_backend import (AuthBootstrapBackend, AuthBootstrapBackendError, PreparedBootstrapCredential, prepared_credential_digest, BootstrapAuthClassification)
    from pixs.auth.r01 import (AuthBootstrapError, BootstrapTrustKey, BootstrapTrustPolicy, SignedBootstrapProof, canonical_bootstrap_bytes, bootstrap_challenge_sha256)
    from pixs.auth.runtime_verifier import AuthVerificationError, _native
    from pixs.core.bootstrap_operator import BootstrapOperatorFacts, BOOTSTRAP_ACTION
    from pixs.core.dto import CorePageItem
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.ports import StagedRef, TransactionProof
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

    cases = {}
    start = datetime.datetime.now(datetime.timezone.utc)
    ctx = ScopeContext(ScopeType.PLATFORM)
    signer = Ed25519PrivateKey.generate()
    public = signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    test_password = "Vecteur R01 public de qualification, aucun secret réel"
    password_hash = hash_password(test_password)
    classification = BootstrapAuthClassification("auth-data-asset-fixture", ConfidentialityLevel.CONFIDENTIAL, PersonalDataLevel.PERSONAL)

    class Clock:
        def __init__(self):
            self.value = start
        def now(self):
            return self.value
    class Proofs:
        def __init__(self, proof):
            self.value = proof
        def resolve(self, ref):
            if ref != self.value.facts.operator_proof_ref:
                raise AssertionError("PROOF_REF")
            return self.value
    class Trust:
        def __init__(self, policy):
            self.value = policy
        def resolve(self, version):
            return self.value
    class Facts:
        def __init__(self, ref):
            self.ref, self.present = ref, True
        def read_facts(self, kind, refs, context, alias, limit):
            if (kind, refs, context, limit) != ("IDENTITY", (self.ref,), ctx, 1):
                raise AssertionError("FACT_PORT")
            if not self.present:
                return ()
            return (CorePageItem("IDENTITY", self.ref, ctx, 1, "ACTIVE", "RETAINED", None, None, None, (("identity_id", str(parse_identity_reference(self.ref))), ("identity_type", "HUMAN"), ("state", "ACTIVE"))),)
    class Classification:
        def __init__(self):
            self.value = classification
        def resolve(self, *, context, alias, operation_id):
            return self.value

    def fixture(label):
        target = identity_reference(new_uuid7())
        facts = BootstrapOperatorFacts("operator-fixture", "pixs.core.bootstrap:installation-fixture", BOOTSTRAP_ACTION, ctx, "installation-fixture", "1.0.0", (BOOTSTRAP_ACTION,), ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"), "proof-"+label, "authorization-"+label, "operation-"+label, target, None, hashlib.sha256(label.encode("ascii")).hexdigest(), start, start+datetime.timedelta(seconds=600), "key-fixture", "1.0.0", None)
        nonce = secrets.token_bytes(32)
        proof = SignedBootstrapProof(facts, nonce, signer.sign(canonical_bootstrap_bytes(facts, nonce)))
        prepared = PreparedBootstrapCredential("local-fixture", "issuer-fixture", "subject-"+label, password_hash)
        key = BootstrapTrustKey("key-fixture", facts.operator_subject_ref, facts.installation_ref, facts.authorized_actions, public, start-datetime.timedelta(days=1), start+datetime.timedelta(days=1), False)
        clock, proofs, trust, reader, cls = Clock(), Proofs(proof), Trust(BootstrapTrustPolicy("1.0.0", (key,))), Facts(target), Classification()
        row = m.AuthBootstrapAuthorization.objects.create(authorization_ref=facts.authorization_ref, operator_proof_ref=facts.operator_proof_ref, operator_subject_ref=facts.operator_subject_ref, installation_ref=facts.installation_ref, plan_version=facts.plan_version, plan_sha256=facts.plan_sha256, operation_ref=facts.operation_id, target_identity_ref=target, closed_effects=list(facts.closed_effects), authorized_actions=list(facts.authorized_actions), key_id=facts.key_id, trust_policy_version=facts.trust_policy_version, challenge_sha256=bootstrap_challenge_sha256(facts, nonce), credential_prepared_digest=prepared_credential_digest(prepared), valid_from=start, expires_at=facts.expires_at)
        def backend(alias="default", prepared_value=prepared):
            return AuthBootstrapBackend(alias=alias, proofs=proofs, trust=trust, facts_reader=reader, classification_source=cls, clock=clock, prepared=prepared_value)
        return dict(facts=facts, row=row, prepared=prepared, clock=clock, proofs=proofs, trust=trust, reader=reader, classification=cls, backend=backend)

    def verify(b, f):
        return b.verify(operator_subject_ref=f.operator_subject_ref, operator_proof_ref=f.operator_proof_ref, plan_version=f.plan_version, installation_ref=f.installation_ref, context=ctx)
    def stamp(b, f, **updates):
        args = dict(alias="default", operation_id=f.operation_id, transaction_token="token-"+f.operation_id, target_identity_ref=f.target_identity_ref, context=ctx)
        args.update(updates)
        return b.stamp(**args)
    def proof(f, ref):
        return TransactionProof(f.operation_id, ref.alias, ref.transaction_token, ctx, (ref,), start)
    def refused(name, action):
        try:
            action()
        except (AuthBootstrapBackendError, AuthBootstrapError, AuthVerificationError):
            cases[name] = True
        else:
            cases[name] = False
    def absent(f):
        return not m.AuthAccountGate.objects.filter(pk=parse_identity_reference(f.target_identity_ref)).exists()

    item = fixture("happy")
    f, b = item["facts"], item["backend"]()
    verified = verify(b, f)
    item["row"].refresh_from_db()
    cases["verify_no_mutation"] = verified.consumed_operation_id is None and item["row"].version == 1 and absent(f)
    refused("outside_tx_refused", lambda: stamp(b, f))
    with transaction.atomic(durable=True):
        ref = stamp(b, f)
        row = m.AuthBootstrapAuthorization.objects.get(pk=item["row"].pk)
        gate = m.AuthAccountGate.objects.get(pk=parse_identity_reference(f.target_identity_ref))
        binding = m.AuthBinding.objects.get(identity=gate)
        credential = m.AuthPasswordCredential.objects.get(binding=binding)
        cases["stamp_real_rows"] = gate.core_identity_version == 1 and binding.external_subject == item["prepared"].external_subject and verify_password(test_password, credential.password_hash)
        cases["consumption_real"] = row.version == 2 and row.consumed_operation_ref == f.operation_id and row.consumed_xid == _native("default")[1][1]
        cases["final_projection_private"] = verify(b, f).consumed_operation_id is None and m.AuthBootstrapAuthorization.objects.get(pk=row.pk).consumed_operation_ref == f.operation_id
        cases["proof_real"] = b.verify_staged(proof(f, ref)) is None
        other_ref = replace(ref, transaction_token="forged-token")
        refused("proof_wrong_token", lambda: b.verify_staged(proof(f, other_ref)))
        other = item["backend"]()
        cases["other_invocation_no_projection"] = verify(other, f).consumed_operation_id == f.operation_id
        other.close()
    inspector = item["backend"](prepared_value=None)
    cases["after_commit_consumed"] = verify(inspector, f).consumed_operation_id == f.operation_id
    inspector.close()
    with transaction.atomic(durable=True):
        refused("after_commit_no_restamp", lambda: stamp(b, f))
    b.close()

    item = fixture("rollback")
    f, b = item["facts"], item["backend"]()
    verify(b, f)
    with transaction.atomic(durable=True):
        stamp(b, f)
        transaction.set_rollback(True)
    item["row"].refresh_from_db()
    cases["rollback_real"] = absent(f) and item["row"].consumed_operation_ref is None and item["row"].version == 1
    with transaction.atomic(durable=True):
        refused("rollback_old_receipt_refused", lambda: stamp(b, f))
    b.close()
    fresh = item["backend"]()
    verify(fresh, f)
    with transaction.atomic(durable=True):
        ref = stamp(fresh, f)
        cases["rollback_new_invocation_retry"] = fresh.verify_staged(proof(f, ref)) is None
    fresh.close()

    for label, name, change in (("expired", "expiry_boundary_refused", "clock"), ("revoked", "revoked_key_refused", "key"), ("plan", "plan_changed_refused", "plan")):
        item = fixture(label)
        f, b = item["facts"], item["backend"]()
        if change == "clock":
            item["clock"].value = start+datetime.timedelta(seconds=600)
        elif change == "key":
            item["trust"].value = replace(item["trust"].value, keys=(replace(item["trust"].value.keys[0], revoked=True),))
        else:
            m.AuthBootstrapAuthorization.objects.filter(pk=item["row"].pk).update(plan_sha256="f"*64)
        refused(name, lambda: verify(b, f))
        cases[name] = cases[name] and absent(f)
        b.close()

    for label, name, change in (("prepared", "prepared_mapping_bound", "prepared"), ("missing", "target_missing_refused", "target"), ("classmissing", "classification_missing_refused", "classification"), ("wrongtarget", "wrong_target_refused", "wrongtarget"), ("wrongalias", "wrong_alias_refused", "wrongalias")):
        item = fixture(label)
        f = item["facts"]
        prepared = replace(item["prepared"], external_subject="divergent") if change == "prepared" else item["prepared"]
        b = item["backend"](prepared_value=prepared)
        verify(b, f)
        if change == "target":
            item["reader"].present = False
        elif change == "classification":
            item["classification"].value = None
        updates = {"target_identity_ref": identity_reference(new_uuid7())} if change == "wrongtarget" else ({"alias": "peer"} if change == "wrongalias" else {})
        with transaction.atomic(durable=True):
            refused(name, lambda: stamp(b, f, **updates))
        cases[name] = cases[name] and absent(f)
        b.close()

    for label, name in (("keyafter", "key_withdrawn_after_stage"), ("classafter", "classification_changed_refused")):
        item = fixture(label)
        f, b = item["facts"], item["backend"]()
        verify(b, f)
        with transaction.atomic(durable=True):
            ref = stamp(b, f)
            if label == "keyafter":
                item["trust"].value = replace(item["trust"].value, keys=(replace(item["trust"].value.keys[0], revoked=True),))
            else:
                item["classification"].value = replace(classification, governance_ref="changed-asset")
            refused(name, lambda: b.verify_staged(proof(f, ref)))
            transaction.set_rollback(True)
        cases[name] = cases[name] and absent(f)
        b.close()

    item = fixture("concurrent")
    f, first, second = item["facts"], item["backend"](), item["backend"]("contender")
    verify(first, f)
    verify(second, f)
    started = threading.Event()
    outcome = {"refused": False, "closed": False, "pid": None, "failure": None}
    def contender():
        raw = None
        try:
            with transaction.atomic(using="contender", durable=True):
                raw, native = _native("contender")
                outcome["pid"] = native[0]
                started.set()
                stamp(second, f, alias="contender")
        except AuthBootstrapBackendError:
            outcome["refused"] = True
        except Exception as error:
            outcome["failure"] = type(error).__name__
            started.set()
        finally:
            conn = connections["contender"]
            if raw is None:
                raw = conn.connection
            conn.close()
            outcome["closed"] = raw is None or bool(raw.closed)
    worker = threading.Thread(target=contender)
    blocked = False
    with transaction.atomic(durable=True):
        stamp(first, f)
        worker.start()
        if not started.wait(2):
            raise RuntimeError("CONTENDER_NOT_STARTED")
        deadline = time.monotonic()+0.9
        while time.monotonic() < deadline and outcome["pid"] is not None:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT wait_event_type FROM pg_stat_activity WHERE pid=%s", (outcome["pid"],))
                found = cursor.fetchone()
            if found is not None and found[0] == "Lock":
                blocked = True
                break
            threading.Event().wait(0.01)
    worker.join(5)
    row = m.AuthBootstrapAuthorization.objects.get(pk=item["row"].pk)
    cases["concurrent_single_consumer"] = blocked and not worker.is_alive() and outcome["refused"] and outcome["closed"] and outcome["failure"] is None and row.version == 2 and row.consumed_operation_ref == f.operation_id and m.AuthBinding.objects.filter(identity_id=parse_identity_reference(f.target_identity_ref)).count() == 1
    first.close()
    second.close()
    return cases


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES)
    result["plan_core_classification_ports"] = "DOUBLES_EXPLICITES"
    result["common_c08_qualification"] = False
    return result
