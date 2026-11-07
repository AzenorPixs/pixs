"""Présentation locale privée pure E5, sans autorité ni fraîcheur."""

from __future__ import annotations

import json

from .planning_bundle import (
    PlanningBundleError,
    PlanningBundleLimits,
    parse_planning_bundle,
    planning_bundle_sha256,
)
from .postgresql_confirmation import (
    ConfirmationError,
    ConfirmationLimits,
    match_confirmation_bundle,
    parse_confirmation,
)

__all__ = ["PresentationError", "present_for_confirmation"]


class PresentationError(ValueError):
    def __init__(self) -> None:
        super().__init__("présentation refusée.")


def _j(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def present_for_confirmation(
    *,
    bundle_raw: bytes,
    confirmation_raw: bytes | None,
    bundle_limits: PlanningBundleLimits,
    confirmation_limits: ConfirmationLimits | None,
) -> str:
    try:
        bundle = parse_planning_bundle(bundle_raw, bundle_limits)
    except (PlanningBundleError, ConfirmationError) as e:
        raise PresentationError() from e
    try:
        digest_bundle = planning_bundle_sha256(bundle, bundle_limits)
    except (PlanningBundleError, ConfirmationError) as e:
        raise PresentationError() from e
    if confirmation_raw is None:
        confirmation = None
    else:
        if confirmation_limits is None:
            raise PresentationError()
        try:
            confirmation = parse_confirmation(
                confirmation_raw, confirmation_limits
            )
        except (PlanningBundleError, ConfirmationError) as e:
            raise PresentationError() from e
        try:
            match_confirmation_bundle(
                confirmation, confirmation_limits, bundle, bundle_limits
            )
        except (PlanningBundleError, ConfirmationError) as e:
            raise PresentationError() from e
    lignes = []
    lignes.append("présentation pré-confirmation")
    lignes.append(
        "portée=documents présentés sans preuve de provenance, fraîcheur, consentement ou autorisation"
    )
    lignes.append("bundle schéma-version=" + _j(bundle.schema_version))
    lignes.append("bundle référence=" + _j(bundle.bundle_ref))
    lignes.append("installation référence=" + _j(bundle.installation_ref))
    lignes.append("cible référence=" + _j(bundle.target_ref))
    lignes.append(
        "opération planification=" + _j(bundle.planning_operation_id)
    )
    lignes.append(
        "opération préparation=" + _j(bundle.preparation_operation_id)
    )
    lignes.append("corrélation=" + _j(bundle.correlation_id))
    lignes.append(
        "action service=" + _j(bundle.projection_document.service.action)
    )
    lignes.append(
        "référence service=" + _j(bundle.projection_document.service.ref)
    )
    lignes.append(
        "action rôle=" + _j(bundle.projection_document.role.action)
    )
    lignes.append(
        "référence rôle=" + _j(bundle.projection_document.role.ref)
    )
    lignes.append(
        "action base=" + _j(bundle.projection_document.database.action)
    )
    lignes.append(
        "référence base=" + _j(bundle.projection_document.database.ref)
    )
    lignes.append(
        "effets ordonnés="
        + "["
        + ",".join(
            _j(effet) for effet in bundle.projection_document.allowed_effects
        )
        + "]"
    )
    lignes.append(
        "liaison projection référence=" + _j(bundle.projection_binding.ref)
    )
    lignes.append(
        "liaison projection version=" + _j(bundle.projection_binding.version)
    )
    lignes.append(
        "liaison projection condensat=" + _j(bundle.projection_binding.sha256)
    )
    lignes.append(
        "liaison observation référence=" + _j(bundle.observation_binding.ref)
    )
    lignes.append(
        "liaison observation version=" + _j(bundle.observation_binding.version)
    )
    lignes.append(
        "liaison observation condensat=" + _j(bundle.observation_binding.sha256)
    )
    lignes.append("liaison plan référence=" + _j(bundle.plan_binding.ref))
    lignes.append("liaison plan version=" + _j(bundle.plan_binding.version))
    lignes.append("liaison plan condensat=" + _j(bundle.plan_binding.sha256))
    lignes.append(
        "liaison préconditions référence=" + _j(bundle.preconditions_binding.ref)
    )
    lignes.append(
        "liaison préconditions version="
        + _j(bundle.preconditions_binding.version)
    )
    lignes.append(
        "liaison préconditions condensat="
        + _j(bundle.preconditions_binding.sha256)
    )
    lignes.append(
        "liaison effets référence=" + _j(bundle.effects_binding.ref)
    )
    lignes.append(
        "liaison effets version=" + _j(bundle.effects_binding.version)
    )
    lignes.append(
        "liaison effets condensat=" + _j(bundle.effects_binding.sha256)
    )
    lignes.append("digest effets=" + _j(bundle.effects_digest))
    lignes.append("digest bundle=" + _j(digest_bundle))
    lignes.append(
        "politique observation référence="
        + _j(bundle.observation_document.policy_ref)
    )
    lignes.append(
        "politique observation version="
        + _j(bundle.observation_document.policy_version)
    )
    for ressource in bundle.observation_document.resources:
        lignes.append("observation espèce=" + _j(ressource.kind))
        lignes.append("observation référence=" + _j(ressource.resource_ref))
        lignes.append("observation état=" + _j(ressource.state))
        lignes.append("observation correspondance=" + _j(ressource.match))
    for garde in bundle.preconditions_document.resource_guards:
        lignes.append("garde espèce=" + _j(garde.kind))
        lignes.append("garde référence=" + _j(garde.resource_ref))
    lignes.append(
        "conditions préconditions="
        + "["
        + ",".join(
            "{"
            + "effet="
            + _j(condition.effect)
            + ",espèce ressource="
            + _j(condition.resource_kind)
            + ",référence ressource="
            + _j(condition.resource_ref)
            + ",étape contrôle="
            + _j(condition.check_stage)
            + "}"
            for condition in bundle.preconditions_document.conditions
        )
        + "]"
    )
    if confirmation is None:
        lignes.append("confirmation fournie=aucune")
    else:
        lignes.append("confirmation fournie=données rapprochées seulement")
        lignes.append(
            "confirmation référence=" + _j(confirmation.confirmation_ref)
        )
        lignes.append(
            "confirmation installation=" + _j(confirmation.installation_ref)
        )
        lignes.append("confirmation cible=" + _j(confirmation.target_ref))
        lignes.append(
            "confirmation opération=" + _j(confirmation.operation_id)
        )
        lignes.append(
            "confirmation opérateur=" + _j(confirmation.operator_ref)
        )
        lignes.append(
            "confirmation politique=" + _j(confirmation.policy_ref)
        )
        lignes.append(
            "confirmation version politique=" + _j(confirmation.policy_version)
        )
        lignes.append(
            "confirmation instant=" + _j(confirmation.confirmed_at)
        )
        lignes.append(
            "confirmation corrélation=" + _j(confirmation.correlation_id)
        )
    return "\n".join(lignes) + "\n"
