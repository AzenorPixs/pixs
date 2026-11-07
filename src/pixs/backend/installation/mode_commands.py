"""Commandes privees C08 modes, valeurs pures sans autorite."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from urllib.parse import quote

from pixs.backend.installation.mode_values import ModeOperationKind

__all__ = ["MODE_SERIALIZER_VERSION", "ModeCommandInput",
           "check_mode_command", "mode_resource_ref",
           "mode_action_ref", "mode_command_type",
           "canonical_mode_bytes", "mode_content_sha256"]

MODE_SERIALIZER_VERSION = "1.0.0"
_MAX_INT = 2 ** 63 - 1


@dataclass(frozen=True, slots=True, repr=False)
class ModeCommandInput:
    installation_ref: str
    actor_ref: str
    kind: ModeOperationKind
    expected_version: int
    idempotency_key: str

    def __post_init__(self) -> None:
        if type(object.__getattribute__(self, "installation_ref")) is not str:
            raise ValueError("Commande C08 refusee.")
        if type(object.__getattribute__(self, "actor_ref")) is not str:
            raise ValueError("Commande C08 refusee.")
        if type(object.__getattribute__(self, "kind")) is not ModeOperationKind:
            raise ValueError("Commande C08 refusee.")
        version = object.__getattribute__(self, "expected_version")
        if type(version) is not int or not 1 <= version <= _MAX_INT:
            raise ValueError("Commande C08 refusee.")
        if type(object.__getattribute__(self, "idempotency_key")) is not str:
            raise ValueError("Commande C08 refusee.")


def _check_str(value: object, limit: int) -> None:
    if type(value) is not str or not value:
        raise ValueError("Commande C08 refusee.")
    if "\x00" in value or not value.isprintable():
        raise ValueError("Commande C08 refusee.")
    if type(limit) is not int or limit < 1:
        raise ValueError("Commande C08 refusee.")
    if len(value) > limit:
        raise ValueError("Commande C08 refusee.")


def check_mode_command(value: object, *, max_ref_len: int) -> None:
    if type(value) is not ModeCommandInput:
        raise ValueError("Commande C08 refusee.")
    if type(max_ref_len) is not int or max_ref_len < 1:
        raise ValueError("Commande C08 refusee.")
    _check_str(value.installation_ref, max_ref_len)
    _check_str(value.actor_ref, max_ref_len)
    _check_str(value.idempotency_key, max_ref_len)
    if type(value.kind) is not ModeOperationKind:
        raise ValueError("Commande C08 refusee.")
    if type(value.expected_version) is not int or isinstance(value.expected_version, bool):
        raise ValueError("Commande C08 refusee.")
    if not 1 <= value.expected_version <= _MAX_INT:
        raise ValueError("Commande C08 refusee.")


def mode_resource_ref(value: ModeCommandInput, *, max_ref_len: int) -> str:
    check_mode_command(value, max_ref_len=max_ref_len)
    try:
        return "pixs.backend.modes:" + quote(value.installation_ref, safe="")
    except (ValueError, UnicodeError):
        raise ValueError("Commande C08 refusee.") from None


def mode_action_ref(kind: ModeOperationKind) -> str:
    if kind is ModeOperationKind.FINALIZE_CONFIGURATION:
        return "pixs.backend.modes.finalize"
    if kind is ModeOperationKind.ENTER_MAINTENANCE:
        return "pixs.backend.modes.enter_maintenance"
    if kind is ModeOperationKind.EXIT_MAINTENANCE:
        return "pixs.backend.modes.exit_maintenance"
    raise ValueError("Commande C08 refusee.")


def mode_command_type(kind: ModeOperationKind) -> str:
    if kind is ModeOperationKind.FINALIZE_CONFIGURATION:
        return "pixs.backend.modes.finalize:v1"
    if kind is ModeOperationKind.ENTER_MAINTENANCE:
        return "pixs.backend.modes.enter_maintenance:v1"
    if kind is ModeOperationKind.EXIT_MAINTENANCE:
        return "pixs.backend.modes.exit_maintenance:v1"
    raise ValueError("Commande C08 refusee.")


def canonical_mode_bytes(value: ModeCommandInput, *, max_ref_len: int) -> bytes:
    check_mode_command(value, max_ref_len=max_ref_len)
    payload = {"installation_ref": value.installation_ref,
               "actor_ref": value.actor_ref,
               "kind": value.kind.value,
               "expected_version": value.expected_version,
               "idempotency_key": value.idempotency_key,
               "serializer_version": MODE_SERIALIZER_VERSION}
    try:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        raise ValueError("Commande C08 refusee.") from None
    if not raw:
        raise ValueError("Commande C08 refusee.")
    return raw


def mode_content_sha256(value: ModeCommandInput, *, max_ref_len: int) -> str:
    return hashlib.sha256(
        canonical_mode_bytes(value, max_ref_len=max_ref_len)
    ).hexdigest()
