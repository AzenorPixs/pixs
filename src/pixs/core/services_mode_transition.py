"""Entree publique Core dediee modes C08 : selectionne fabrique connue, sans acces prive."""
from __future__ import annotations
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CoreMutationResult
from pixs.core.ports import CorePortError
__all__ = ["execute_modes_transition"]
_EXPECTED_OWNER = "pixs.backend"
def execute_modes_transition(*, using: str, inspection_using: str, clock: object, envelope: CommandEnvelope, command: object, reader: object, store: object, authentication_source: object, audit: object, filter_config: object, governance: object, waiver_request: object) -> CoreMutationResult:
    from pixs.backend.installation.mode_commands import MODE_SERIALIZER_VERSION, ModeCommandInput, check_mode_command, mode_action_ref, mode_command_type, mode_content_sha256, mode_resource_ref
    from pixs.backend.installation.mode_transition_factory import ModesTransition, build_modes_transition
    from pixs.core.services_transactions import _execute_mutation_for_owner
    if type(envelope) is not CommandEnvelope:
        raise CorePortError()
    if type(command) is not ModeCommandInput:
        raise CorePortError()
    try:
        envelope.__post_init__()
    except CoreInputInvalid as error:
        raise CorePortError() from error
    result = build_modes_transition(using=using, inspection_using=inspection_using, clock=clock, envelope=envelope, command=command, reader=reader, store=store, authentication_source=authentication_source, audit=audit, filter_config=filter_config, governance=governance, waiver_request=waiver_request)
    if type(result) is not ModesTransition:
        raise CorePortError()
    bound = result.max_ref_len
    if type(bound) is bool or type(bound) is not int or bound <= 0:
        raise CorePortError()
    try:
        check_mode_command(command, max_ref_len=bound)
    except ValueError as error:
        raise CorePortError() from error
    try:
        exp_res = mode_resource_ref(command, max_ref_len=bound)
        exp_act = mode_action_ref(command.kind)
        exp_hash = mode_content_sha256(command, max_ref_len=bound)
        exp_type = mode_command_type(command.kind)
    except ValueError as error:
        raise CorePortError() from error
    if envelope.content_sha256 != exp_hash or envelope.serializer_version != MODE_SERIALIZER_VERSION:
        raise CorePortError()
    if envelope.request.resource_id != exp_res or envelope.request.action_id != exp_act:
        raise CorePortError()
    if result.resource_id != exp_res or result.action_id != exp_act or result.command_type != exp_type or result.content_sha256 != exp_hash:
        raise CorePortError()
    if type(result.lock_scopes) is not tuple or len(result.lock_scopes) == 0:
        raise CorePortError()
    if result.lock_scopes != tuple(sorted(set(result.lock_scopes))):
        raise CorePortError()
    if ("installation:" + command.installation_ref) not in result.lock_scopes:
        raise CorePortError()
    if not callable(result.apply):
        raise CorePortError()
    return _execute_mutation_for_owner(ports=result.ports, alias=using, envelope=envelope, resource_id=result.resource_id, action_id=result.action_id, correlation_id=envelope.correlation_id, command_type=result.command_type, lock_scopes=result.lock_scopes, apply=result.apply, outbox_payload_refs=(), _facts_source=None, expected_owner=_EXPECTED_OWNER)
