"""Fixture TEST C08 E5 : graphes coherents immuables par APIs publiques.
Preuves synthetiques opaques distinguees des hashes de documents TEST reellement calcules, aucune autorite, temps, runtime ou PG prouves.
"""
from __future__ import annotations

from dataclasses import dataclass
import json

from pixs.backend.installation.technical_projection import (
    ProjectionLimits,
    ProjectionService,
    ProjectionRole,
    ProjectionDatabase,
    ProjectionObservation,
    TechnicalProjection,
    projection_sha256,
)
from pixs.backend.installation.planning_bundle import (
    PlanningBundle,
    PlanningBundleLimits,
    planning_bundle_binding,
)
from pixs.backend.installation.exchange_envelope_1_1 import (
    ExchangeRequest,
    ExchangeRequestLimits,
)
from pixs.backend.installation.exchange_response_1_1 import (
    ExchangeResponse,
    ExchangeResponseLimits,
    ObservationPayload,
    PlanningPayload,
)
from pixs.backend.installation.postgresql_confirmation import (
    Confirmation,
    ConfirmationLimits,
    confirmation_binding,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    NativeRequest,
    NativeResult,
    PayloadLimits,
    TechnicalPlan,
    plan_sha256,
)
from pixs.pa_native.postgresql_observation import (
    ObservationManifest,
    ObservationProfileBindings,
    ObservationResource,
    observation_binding,
)
from pixs.pa_native.postgresql_preconditions import (
    PreconditionsManifest,
    PreconditionsLimits,
    ResourceGuard,
    PreconditionCondition,
    preconditions_binding,
)
from pixs.pa_native.postgresql_effects import (
    EffectsManifest,
    effects_binding,
    effects_digest,
)


TEST_MAX_JSON = 65536
TEST_MAX_REF = 128
TEST_MAX_OBS = 16
TEST_MAX_CONDITIONS = 16
TEST_MAX_CORR = 8
TEST_MAX_CAUS = 8
TEST_MAX_BUNDLE = 131072
TEST_MAX_ENVELOPE = 65536
TEST_MAX_RESPONSE = 131072
TEST_MAX_CONFIRM = 32768
TEST_OBSERVED_AT = "2026-01-01T00:00:00.000000Z"
TEST_CONFIRMED_AT = "2026-01-02T00:00:00.000000Z"
TEST_SYNTH_A = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
TEST_SYNTH_B = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEST_SYNTH_C = "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
TEST_SYNTH_D = "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
TEST_SYNTH_E = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"


@dataclass(frozen=True, slots=True, repr=False)
class C08E5Limits:
    payload: PayloadLimits
    projection_limits: ProjectionLimits
    preconditions_limits: PreconditionsLimits
    bundle_limits: PlanningBundleLimits
    confirmation_limits: ConfirmationLimits
    request_limits: ExchangeRequestLimits
    response_limits: ExchangeResponseLimits


@dataclass(frozen=True, slots=True, repr=False)
class C08E5Graph:
    suffix: str
    limits: C08E5Limits
    projection: TechnicalProjection
    projection_binding: ContentBinding
    observation: ObservationManifest
    observation_binding: ContentBinding
    preconditions: PreconditionsManifest
    preconditions_binding: ContentBinding
    effects: EffectsManifest
    effects_binding: ContentBinding
    effects_digest: str
    plan: TechnicalPlan
    plan_binding: ContentBinding
    bundle: PlanningBundle
    bundle_binding: ContentBinding
    confirmation: Confirmation
    confirmation_binding: ContentBinding
    planning_operation_id: str
    preparation_operation_id: str
    obs_operation_id: str
    read_operation_id: str
    correlation_id: str
    installation_ref: str
    target_ref: str


def make_limits() -> C08E5Limits:
    payload = PayloadLimits(
        max_json_bytes=TEST_MAX_JSON,
        max_ref_bytes=TEST_MAX_REF,
        max_observation_refs=TEST_MAX_OBS,
    )
    projection_limits = ProjectionLimits(
        max_bytes=32768,
        max_ref_bytes=TEST_MAX_REF,
        max_correlation_refs=TEST_MAX_CORR,
        max_causation_refs=TEST_MAX_CAUS,
    )
    preconditions_limits = PreconditionsLimits(
        payload=payload,
        max_conditions=TEST_MAX_CONDITIONS,
    )
    bundle_limits = PlanningBundleLimits(
        payload=payload,
        projection_limits=projection_limits,
        preconditions_limits=preconditions_limits,
        max_bundle_bytes=TEST_MAX_BUNDLE,
    )
    confirmation_limits = ConfirmationLimits(
        payload=payload,
        max_confirmation_bytes=TEST_MAX_CONFIRM,
    )
    request_limits = ExchangeRequestLimits(
        payload=payload,
        projection_limits=projection_limits,
        max_envelope_bytes=TEST_MAX_ENVELOPE,
    )
    response_limits = ExchangeResponseLimits(
        payload=payload,
        bundle_limits=bundle_limits,
        max_response_bytes=TEST_MAX_RESPONSE,
    )
    return C08E5Limits(
        payload=payload,
        projection_limits=projection_limits,
        preconditions_limits=preconditions_limits,
        bundle_limits=bundle_limits,
        confirmation_limits=confirmation_limits,
        request_limits=request_limits,
        response_limits=response_limits,
    )


def _synth_binding(
    ref: str,
    version: str,
    digest: str,
) -> ContentBinding:
    return ContentBinding(
        ref=ref,
        version=version,
        sha256=digest,
    )


def _profile_bindings(
    suffix: str,
) -> ObservationProfileBindings:
    return ObservationProfileBindings(
        runtime=_synth_binding(
            "runtime-profile-test-" + suffix,
            "1.0.0",
            TEST_SYNTH_A,
        ),
        service=_synth_binding(
            "service-profile-test-" + suffix,
            "1.0.0",
            TEST_SYNTH_B,
        ),
        role=_synth_binding(
            "role-profile-test-" + suffix,
            "1.0.0",
            TEST_SYNTH_C,
        ),
        database=_synth_binding(
            "database-profile-test-" + suffix,
            "1.0.0",
            TEST_SYNTH_D,
        ),
    )


def make_reuse_graph(
    suffix: str,
) -> C08E5Graph:
    if type(suffix) is not str or not suffix:
        raise ValueError("suffix TEST explicite non vide requis")
    limits = make_limits()
    installation = "installation-test-" + suffix
    target = "target-test-" + suffix
    correlation = "correlation-test-" + suffix
    obs_op = "obs-test-" + suffix
    planning_op = "planning-test-" + suffix
    prep_op = "prep-test-" + suffix
    read_op = "read-test-" + suffix
    policy = "policy-test-" + suffix
    profiles = _profile_bindings(suffix)
    resources = (
        ObservationResource(
            kind="SOFTWARE",
            resource_ref="software-test-" + suffix,
            state="PRESENT",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-soft-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="CLUSTER",
            resource_ref="cluster-test-" + suffix,
            state="PRESENT",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-cluster-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="SERVICE",
            resource_ref="service-test-" + suffix,
            state="RUNNING",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-service-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="ROLE",
            resource_ref="role-test-" + suffix,
            state="PRESENT",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-role-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="DATABASE",
            resource_ref="database-test-" + suffix,
            state="PRESENT",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-db-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
    )
    obs_doc = ObservationManifest(
        schema="pixs.agent.postgresql.observation_manifest",
        schema_version="1.0.0",
        observation_ref="observation-test-" + suffix,
        inspection_operation_id=obs_op,
        installation_ref=installation,
        target_ref=target,
        policy_ref=policy,
        policy_version="1.0.0",
        profile_bindings=profiles,
        resources=resources,
        observed_at=TEST_OBSERVED_AT,
        time_evidence_binding=_synth_binding(
            "time-test-" + suffix,
            "1.0.0",
            TEST_SYNTH_A,
        ),
    )
    return _finish_graph(
        suffix,
        limits,
        installation,
        target,
        correlation,
        obs_op,
        planning_op,
        prep_op,
        read_op,
        policy,
        obs_doc,
        (),
        (
            "c2-" + suffix,
            "c1-" + suffix,
            "c2-" + suffix,
        ),
        (
            "a1-" + suffix,
            "a1-" + suffix,
        ),
    )


def make_deferred_graph(
    suffix: str,
) -> C08E5Graph:
    if type(suffix) is not str or not suffix:
        raise ValueError("suffix TEST explicite non vide requis")
    limits = make_limits()
    installation = "installation-test-" + suffix
    target = "target-test-" + suffix
    correlation = "correlation-test-" + suffix
    obs_op = "obs-test-" + suffix
    planning_op = "planning-test-" + suffix
    prep_op = "prep-test-" + suffix
    read_op = "read-test-" + suffix
    policy = "policy-test-" + suffix
    profiles = _profile_bindings(suffix)
    resources = (
        ObservationResource(
            kind="SOFTWARE",
            resource_ref="software-test-" + suffix,
            state="PRESENT",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-soft-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="CLUSTER",
            resource_ref="cluster-test-" + suffix,
            state="PRESENT",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-cluster-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="SERVICE",
            resource_ref="service-test-" + suffix,
            state="STOPPED",
            match="MATCH",
            evidence_binding=_synth_binding(
                "ev-service-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="ROLE",
            resource_ref="role-test-" + suffix,
            state="UNOBSERVABLE",
            match="UNDETERMINED",
            evidence_binding=_synth_binding(
                "ev-role-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
        ObservationResource(
            kind="DATABASE",
            resource_ref="database-test-" + suffix,
            state="UNOBSERVABLE",
            match="UNDETERMINED",
            evidence_binding=_synth_binding(
                "ev-db-" + suffix,
                "1.0.0",
                TEST_SYNTH_E,
            ),
        ),
    )
    obs_doc = ObservationManifest(
        schema="pixs.agent.postgresql.observation_manifest",
        schema_version="1.0.0",
        observation_ref="observation-test-" + suffix,
        inspection_operation_id=obs_op,
        installation_ref=installation,
        target_ref=target,
        policy_ref=policy,
        policy_version="1.0.0",
        profile_bindings=profiles,
        resources=resources,
        observed_at=TEST_OBSERVED_AT,
        time_evidence_binding=_synth_binding(
            "time-test-" + suffix,
            "1.0.0",
            TEST_SYNTH_A,
        ),
    )
    return _finish_graph(
        suffix,
        limits,
        installation,
        target,
        correlation,
        obs_op,
        planning_op,
        prep_op,
        read_op,
        policy,
        obs_doc,
        (
            "SERVICE_START",
            "ROLE_CREATE",
            "DATABASE_CREATE",
        ),
        (
            "c2-" + suffix,
            "c1-" + suffix,
            "c2-" + suffix,
        ),
        (
            "a1-" + suffix,
            "a1-" + suffix,
        ),
    )


def _finish_graph(
    suffix: str,
    limits: C08E5Limits,
    installation: str,
    target: str,
    correlation: str,
    obs_op: str,
    planning_op: str,
    prep_op: str,
    read_op: str,
    policy: str,
    obs_doc: ObservationManifest,
    allowed: tuple,
    corr_ids: tuple,
    caus_ids: tuple,
) -> C08E5Graph:
    obs_bind = observation_binding(
        obs_doc,
        limits.payload,
    )
    proj_obs = ProjectionObservation(
        ref=obs_bind.ref,
        version=obs_bind.version,
        sha256=obs_bind.sha256,
    )
    if len(allowed) == 0:
        svc_action = "REUSE_RUNNING"
        role_action = "REUSE"
        db_action = "REUSE"
    else:
        svc_action = "START_EXISTING"
        role_action = "CREATE"
        db_action = "CREATE"
    proj = TechnicalProjection(
        projection_ref="projection-test-" + suffix,
        operation_id=prep_op,
        installation_ref=installation,
        target_ref=target,
        runtime_profile_ref="runtime-profile-test-" + suffix,
        runtime_profile_version="1.0.0",
        service=ProjectionService(
            ref="service-test-" + suffix,
            action=svc_action,
            profile_ref="service-profile-test-" + suffix,
            profile_version="1.0.0",
        ),
        role=ProjectionRole(
            ref="role-test-" + suffix,
            action=role_action,
            profile_ref="role-profile-test-" + suffix,
            profile_version="1.0.0",
            credential_binding_ref="binding-test-" + suffix,
            credential_binding_version="1.0.0",
        ),
        database=ProjectionDatabase(
            ref="database-test-" + suffix,
            action=db_action,
            profile_ref="database-profile-test-" + suffix,
            profile_version="1.0.0",
        ),
        observation=proj_obs,
        allowed_effects=tuple(allowed),
        correlation_id=correlation,
        idempotency_key="key-test-" + suffix,
        causation_id=None,
        correlation_ids=tuple(corr_ids),
        causation_ids=tuple(caus_ids),
    )
    proj_bind = ContentBinding(
        ref=proj.projection_ref,
        version="1.0.0",
        sha256=projection_sha256(
            proj,
            limits.projection_limits,
        ),
    )
    guards = (
        ResourceGuard(
            kind="SOFTWARE",
            resource_ref="software-test-" + suffix,
            profile_binding=obs_doc.profile_bindings.service,
        ),
        ResourceGuard(
            kind="CLUSTER",
            resource_ref="cluster-test-" + suffix,
            profile_binding=obs_doc.profile_bindings.service,
        ),
        ResourceGuard(
            kind="SERVICE",
            resource_ref="service-test-" + suffix,
            profile_binding=obs_doc.profile_bindings.service,
        ),
        ResourceGuard(
            kind="ROLE",
            resource_ref="role-test-" + suffix,
            profile_binding=obs_doc.profile_bindings.role,
        ),
        ResourceGuard(
            kind="DATABASE",
            resource_ref="database-test-" + suffix,
            profile_binding=obs_doc.profile_bindings.database,
        ),
    )
    if len(allowed) == 0:
        conds: tuple = ()
    else:
        conds = (
            PreconditionCondition(
                condition_ref="cond-service-" + suffix,
                resource_kind="SERVICE",
                resource_ref="service-test-" + suffix,
                profile_binding=obs_doc.profile_bindings.service,
                effect="SERVICE_START",
                check_stage="BEFORE_EFFECT",
                expected_state="STOPPED",
                expected_match="MATCH",
                evidence_binding=_synth_binding(
                    "ev-cond-service-" + suffix,
                    "1.0.0",
                    TEST_SYNTH_B,
                ),
            ),
            PreconditionCondition(
                condition_ref="cond-role-" + suffix,
                resource_kind="ROLE",
                resource_ref="role-test-" + suffix,
                profile_binding=obs_doc.profile_bindings.role,
                effect="ROLE_CREATE",
                check_stage="AFTER_SERVICE_START_BEFORE_EFFECT",
                expected_state="ABSENT",
                expected_match="MATCH",
                evidence_binding=None,
            ),
            PreconditionCondition(
                condition_ref="cond-db-" + suffix,
                resource_kind="DATABASE",
                resource_ref="database-test-" + suffix,
                profile_binding=obs_doc.profile_bindings.database,
                effect="DATABASE_CREATE",
                check_stage="AFTER_SERVICE_START_BEFORE_EFFECT",
                expected_state="ABSENT",
                expected_match="MATCH",
                evidence_binding=None,
            ),
        )
    pre = PreconditionsManifest(
        schema="pixs.agent.postgresql.preconditions_manifest",
        schema_version="1.0.0",
        preconditions_ref="preconditions-test-" + suffix,
        installation_ref=installation,
        target_ref=target,
        operation_id=prep_op,
        projection_binding=proj_bind,
        observation_binding=obs_bind,
        resource_guards=guards,
        conditions=conds,
    )
    pre_bind = preconditions_binding(
        pre,
        limits.preconditions_limits,
    )
    eff = EffectsManifest(
        schema="pixs.agent.postgresql.effects_manifest",
        schema_version="1.0.0",
        effects_ref="effects-test-" + suffix,
        installation_ref=installation,
        target_ref=target,
        operation_id=prep_op,
        projection_binding=proj_bind,
        allowed_effects=tuple(allowed),
    )
    eff_bind = effects_binding(
        eff,
        limits.payload,
    )
    eff_digest = effects_digest(
        eff,
        limits.payload,
    )
    confirmation_ref = "confirmation-test-" + suffix
    plan = TechnicalPlan(
        schema_version="1.0.0",
        catalog_operation="prepare_postgresql",
        catalog_version="1.0.0",
        operation_id=prep_op,
        idempotency_key="key-test-" + suffix,
        correlation_id=correlation,
        plan_ref="plan-test-" + suffix,
        plan_version="plan-version-test-" + suffix,
        installation_ref=installation,
        target_ref=target,
        projection_ref=proj.projection_ref,
        confirmation_ref=confirmation_ref,
        policy_ref=policy,
        preconditions_ref=pre.preconditions_ref,
        service_ref=proj.service.ref,
        role_ref=proj.role.ref,
        database_ref=proj.database.ref,
    )
    plan_bind = ContentBinding(
        ref=plan.plan_ref,
        version=plan.plan_version,
        sha256=plan_sha256(
            plan,
            limits.payload,
        ),
    )
    bundle = PlanningBundle(
        schema="pixs.agent.postgresql.planning_bundle",
        schema_version="1.0.0",
        bundle_ref="bundle-test-" + suffix,
        installation_ref=installation,
        target_ref=target,
        planning_operation_id=planning_op,
        preparation_operation_id=prep_op,
        correlation_id=correlation,
        projection_document=proj,
        projection_binding=proj_bind,
        observation_document=obs_doc,
        observation_binding=obs_bind,
        plan_document=plan,
        plan_binding=plan_bind,
        preconditions_document=pre,
        preconditions_binding=pre_bind,
        effects_document=eff,
        effects_binding=eff_bind,
        effects_digest=eff_digest,
    )
    bundle_bind = planning_bundle_binding(
        bundle,
        limits.bundle_limits,
    )
    confirmation = Confirmation(
        schema="pixs.c08.postgresql-confirmation.v1",
        schema_version="1.0.0",
        confirmation_ref=confirmation_ref,
        installation_ref=installation,
        target_ref=target,
        operation_id=prep_op,
        operator_ref="operator-test-" + suffix,
        projection_binding=proj_bind,
        observation_binding=obs_bind,
        plan_binding=plan_bind,
        preconditions_binding=pre_bind,
        effects_binding=eff_bind,
        policy_ref=policy,
        policy_version="1.0.0",
        confirmed_at=TEST_CONFIRMED_AT,
        correlation_id=correlation,
    )
    confirmation_bind = confirmation_binding(
        confirmation,
        limits.confirmation_limits,
    )
    return C08E5Graph(
        suffix=suffix,
        limits=limits,
        projection=proj,
        projection_binding=proj_bind,
        observation=obs_doc,
        observation_binding=obs_bind,
        preconditions=pre,
        preconditions_binding=pre_bind,
        effects=eff,
        effects_binding=eff_bind,
        effects_digest=eff_digest,
        plan=plan,
        plan_binding=plan_bind,
        bundle=bundle,
        bundle_binding=bundle_bind,
        confirmation=confirmation,
        confirmation_binding=confirmation_bind,
        planning_operation_id=planning_op,
        preparation_operation_id=prep_op,
        obs_operation_id=obs_op,
        read_operation_id=read_op,
        correlation_id=correlation,
        installation_ref=installation,
        target_ref=target,
    )


def make_request(
    purpose: str,
    graph: C08E5Graph,
) -> ExchangeRequest:
    if type(purpose) is not str or purpose not in (
        "OBSERVE",
        "PREPARE_PLAN",
        "PREPARE",
        "READ_RESULT",
    ):
        raise ValueError("purpose TEST hors ensemble")
    if purpose == "OBSERVE":
        native = NativeRequest(
            schema_version="1.0.0",
            catalog_operation="inspect_postgresql",
            catalog_version="1.0.0",
            operation_id=graph.obs_operation_id,
            idempotency_key="idem-obs-" + graph.suffix,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            mandate_ref="mandate-obs-" + graph.suffix,
            params=(),
        )
        return ExchangeRequest(
            schema="pixs.agent.postgresql.exchange.request",
            schema_version="1.1.0",
            purpose=purpose,
            request=native,
            projection_document=None,
            projection_binding=None,
            confirmation_ref=None,
        )
    if purpose == "PREPARE_PLAN":
        native = NativeRequest(
            schema_version="1.0.0",
            catalog_operation="inspect_postgresql",
            catalog_version="1.0.0",
            operation_id=graph.planning_operation_id,
            idempotency_key="idem-planning-" + graph.suffix,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            mandate_ref="mandate-planning-" + graph.suffix,
            params=(),
        )
        return ExchangeRequest(
            schema="pixs.agent.postgresql.exchange.request",
            schema_version="1.1.0",
            purpose=purpose,
            request=native,
            projection_document=graph.projection,
            projection_binding=graph.projection_binding,
            confirmation_ref=graph.confirmation.confirmation_ref,
        )
    if purpose == "PREPARE":
        digest = graph.plan_binding.sha256
        native = NativeRequest(
            schema_version="1.0.0",
            catalog_operation="prepare_postgresql",
            catalog_version="1.0.0",
            operation_id=graph.preparation_operation_id,
            idempotency_key="key-test-" + graph.suffix,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            mandate_ref="mandate-prep-" + graph.suffix,
            params=(
                ("plan_digest", digest),
                ("plan_ref", graph.plan.plan_ref),
                ("plan_version", graph.plan.plan_version),
            ),
        )
        return ExchangeRequest(
            schema="pixs.agent.postgresql.exchange.request",
            schema_version="1.1.0",
            purpose=purpose,
            request=native,
            projection_document=None,
            projection_binding=None,
            confirmation_ref=None,
        )
    native = NativeRequest(
        schema_version="1.0.0",
        catalog_operation="get_postgresql_result",
        catalog_version="1.0.0",
        operation_id=graph.read_operation_id,
        idempotency_key="idem-read-" + graph.suffix,
        correlation_id=graph.correlation_id,
        installation_ref=graph.installation_ref,
        target_ref=graph.target_ref,
        mandate_ref="mandate-read-" + graph.suffix,
        params=(("operation_ref", graph.preparation_operation_id),),
    )
    return ExchangeRequest(
        schema="pixs.agent.postgresql.exchange.request",
        schema_version="1.1.0",
        purpose=purpose,
        request=native,
        projection_document=None,
        projection_binding=None,
        confirmation_ref=None,
    )


def make_response_empty(
    purpose: str,
    graph: C08E5Graph,
    phase: str,
) -> ExchangeResponse:
    if type(purpose) is not str or purpose not in (
        "OBSERVE",
        "PREPARE_PLAN",
        "PREPARE",
        "READ_RESULT",
    ):
        raise ValueError("purpose TEST hors ensemble")
    if type(phase) is not str or phase not in (
        "RECEIVED",
        "RUNNING",
        "SUCCEEDED",
        "FAILED",
        "IN_DOUBT",
        "BLOCKED",
    ):
        raise ValueError("phase TEST hors ensemble")
    if purpose in ("OBSERVE", "PREPARE_PLAN") and phase == "SUCCEEDED":
        raise ValueError("utiliser helper SUCCEEDED dedie")
    if purpose == "READ_RESULT":
        result = NativeResult(
            schema_version="1.0.0",
            catalog_operation="get_postgresql_result",
            catalog_version="1.0.0",
            operation_id=graph.read_operation_id,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            subject_operation_ref=graph.preparation_operation_id,
            phase=phase,
            result_ref=None if phase in ("RECEIVED", "BLOCKED") else "result-test-" + graph.suffix,
            observation_refs=() if phase != "SUCCEEDED" else (graph.observation.observation_ref,),
            plan_ref=None if phase != "SUCCEEDED" else graph.plan.plan_ref,
            plan_version=None if phase != "SUCCEEDED" else graph.plan.plan_version,
            plan_digest=None if phase != "SUCCEEDED" else graph.plan_binding.sha256,
            diagnostic_code="DIAG_TEST" if phase in ("FAILED", "IN_DOUBT", "BLOCKED") else None,
        )
    elif purpose == "PREPARE":
        result = NativeResult(
            schema_version="1.0.0",
            catalog_operation="prepare_postgresql",
            catalog_version="1.0.0",
            operation_id=graph.preparation_operation_id,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            subject_operation_ref=None,
            phase=phase,
            result_ref=None if phase in ("RECEIVED", "BLOCKED") else "result-test-" + graph.suffix,
            observation_refs=() if phase != "SUCCEEDED" else (graph.observation.observation_ref,),
            plan_ref=None if phase != "SUCCEEDED" else graph.plan.plan_ref,
            plan_version=None if phase != "SUCCEEDED" else graph.plan.plan_version,
            plan_digest=None if phase != "SUCCEEDED" else graph.plan_binding.sha256,
            diagnostic_code="DIAG_TEST" if phase in ("FAILED", "IN_DOUBT", "BLOCKED") else None,
        )
    elif purpose == "OBSERVE":
        result = NativeResult(
            schema_version="1.0.0",
            catalog_operation="inspect_postgresql",
            catalog_version="1.0.0",
            operation_id=graph.obs_operation_id,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            subject_operation_ref=None,
            phase=phase,
            result_ref=None if phase in ("RECEIVED", "BLOCKED") else "result-test-" + graph.suffix,
            observation_refs=(),
            plan_ref=None,
            plan_version=None,
            plan_digest=None,
            diagnostic_code="DIAG_TEST" if phase in ("FAILED", "IN_DOUBT", "BLOCKED") else None,
        )
    else:
        result = NativeResult(
            schema_version="1.0.0",
            catalog_operation="inspect_postgresql",
            catalog_version="1.0.0",
            operation_id=graph.planning_operation_id,
            correlation_id=graph.correlation_id,
            installation_ref=graph.installation_ref,
            target_ref=graph.target_ref,
            subject_operation_ref=None,
            phase=phase,
            result_ref=None if phase in ("RECEIVED", "BLOCKED") else "result-test-" + graph.suffix,
            observation_refs=(),
            plan_ref=None,
            plan_version=None,
            plan_digest=None,
            diagnostic_code="DIAG_TEST" if phase in ("FAILED", "IN_DOUBT", "BLOCKED") else None,
        )
    return ExchangeResponse(
        schema="pixs.agent.postgresql.exchange.response",
        schema_version="1.1.0",
        purpose=purpose,
        result=result,
        payload=None,
    )


def make_response_observe_succeeded(
    graph: C08E5Graph,
) -> ExchangeResponse:
    result = NativeResult(
        schema_version="1.0.0",
        catalog_operation="inspect_postgresql",
        catalog_version="1.0.0",
        operation_id=graph.obs_operation_id,
        correlation_id=graph.correlation_id,
        installation_ref=graph.installation_ref,
        target_ref=graph.target_ref,
        subject_operation_ref=None,
        phase="SUCCEEDED",
        result_ref="result-obs-" + graph.suffix,
        observation_refs=(graph.observation.observation_ref,),
        plan_ref=None,
        plan_version=None,
        plan_digest=None,
        diagnostic_code=None,
    )
    payload = ObservationPayload(
        observation_document=graph.observation,
        observation_binding=graph.observation_binding,
    )
    return ExchangeResponse(
        schema="pixs.agent.postgresql.exchange.response",
        schema_version="1.1.0",
        purpose="OBSERVE",
        result=result,
        payload=payload,
    )


def make_response_planning_succeeded(
    graph: C08E5Graph,
) -> ExchangeResponse:
    result = NativeResult(
        schema_version="1.0.0",
        catalog_operation="inspect_postgresql",
        catalog_version="1.0.0",
        operation_id=graph.planning_operation_id,
        correlation_id=graph.correlation_id,
        installation_ref=graph.installation_ref,
        target_ref=graph.target_ref,
        subject_operation_ref=None,
        phase="SUCCEEDED",
        result_ref="result-planning-" + graph.suffix,
        observation_refs=(graph.observation.observation_ref,),
        plan_ref=graph.plan.plan_ref,
        plan_version=graph.plan.plan_version,
        plan_digest=graph.plan_binding.sha256,
        diagnostic_code=None,
    )
    payload = PlanningPayload(
        planning_bundle=graph.bundle,
        planning_binding=graph.bundle_binding,
    )
    return ExchangeResponse(
        schema="pixs.agent.postgresql.exchange.response",
        schema_version="1.1.0",
        purpose="PREPARE_PLAN",
        result=result,
        payload=payload,
    )


def canonical_bytes(
    doc: dict,
) -> bytes:
    return json.dumps(
        doc,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
