"""Liaisons structurelles R01, sans authentification ni autorisation implicite."""

from __future__ import annotations

import datetime

from pixs.core.authz.ports import PortError, Request
from pixs.core.bootstrap_operator import (
    BootstrapOperatorError,
    BootstrapOperatorFacts,
    validate_bootstrap_window_current,
)
from pixs.core.dto import BootstrapActInput, CoreInputInvalid

__all__ = [
    "BootstrapBindingError",
    "check_request_binding",
    "check_act_binding",
    "check_consumed_policy",
    "require_current_window",
]


class BootstrapBindingError(ValueError):
    def __init__(self) -> None:
        super().__init__("Liaison R01 invalide.")
        self.code = "BOOTSTRAP_BINDING_INVALID"
        self.element = "bootstrap_binding"
        self.step = "check_bootstrap_binding"


def _validate_facts(facts: BootstrapOperatorFacts) -> None:
    if type(facts) is not BootstrapOperatorFacts:
        raise BootstrapBindingError()
    try:
        facts.__post_init__()
    except (BootstrapOperatorError, AttributeError) as error:
        raise BootstrapBindingError() from error


def require_current_window(facts: BootstrapOperatorFacts, now: datetime.datetime) -> None:
    _validate_facts(facts)
    try:
        validate_bootstrap_window_current(facts, now)
    except BootstrapOperatorError as error:
        raise BootstrapBindingError() from error


def check_request_binding(
    facts: BootstrapOperatorFacts, request: Request, *, operation_id: str
) -> None:
    _validate_facts(facts)
    if type(request) is not Request or type(operation_id) is not str or not operation_id:
        raise BootstrapBindingError()
    try:
        request.__post_init__()
    except (PortError, AttributeError) as error:
        raise BootstrapBindingError() from error
    expected = (
        facts.operator_subject_ref, facts.resource_id, facts.action_id,
        facts.context, facts.authorization_ref,
    )
    actual = (
        request.subject_id, request.resource_id, request.action_id,
        request.context, request.decision_id,
    )
    if actual != expected or facts.operation_id != operation_id:
        raise BootstrapBindingError()
    if facts.consumed_operation_id is not None and facts.consumed_operation_id != operation_id:
        raise BootstrapBindingError()


def check_act_binding(act: BootstrapActInput, facts: BootstrapOperatorFacts) -> None:
    _validate_facts(facts)
    if type(act) is not BootstrapActInput:
        raise BootstrapBindingError()
    try:
        act.__post_init__()
    except (CoreInputInvalid, AttributeError) as error:
        raise BootstrapBindingError() from error
    expected = (
        facts.operator_subject_ref, facts.operator_proof_ref,
        facts.installation_ref, facts.plan_version, facts.authorization_ref,
        facts.operation_id, facts.target_identity_ref, facts.target_tenant_ref,
        facts.context, facts.closed_effects,
    )
    actual = (
        act.operator_subject_ref, act.operator_proof_ref,
        act.installation_ref, act.plan_version, act.authorization_ref,
        act.operation_id, act.target_identity_ref, act.target_tenant_ref,
        act.context, act.closed_effects,
    )
    if actual != expected:
        raise BootstrapBindingError()


def check_consumed_policy(
    facts: BootstrapOperatorFacts, operation_id: str, inspect_confirmed: str | None
) -> str:
    _validate_facts(facts)
    if type(operation_id) is not str or not operation_id or facts.operation_id != operation_id:
        raise BootstrapBindingError()
    consumed = facts.consumed_operation_id
    if consumed is None:
        return "FRESH"
    if (consumed != operation_id or type(inspect_confirmed) is not str
            or not inspect_confirmed):
        raise BootstrapBindingError()
    return "RESTORE_ONLY"
