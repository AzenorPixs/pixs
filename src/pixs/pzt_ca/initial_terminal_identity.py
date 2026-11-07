"""Identité terminale initiale, structure seule.

Portée exacte : `z12.initial_terminal_identity/v1` (§13.2).
Réutilise les helpers internes de `ca_identity` pour refs, version,
enum fermé, époque >=0, RFC3339 UTC, clés bornées, enveloppe stricte,
instant UTC exact. Structure seule, sans autorisation, sans preuve
d'autorité, sans entrée/sortie, sans horloge, sans clé/certificat réel,
sans effet natif. Conversion stricte vers `InitialTerminalIdentityError`
sans trace d'entrée. La syntaxe ne garantit pas l'absence de secret ;
la publication appartient au propriétaire. Ne couvre ni le schéma
material §13.3 ni le resolver §13.4, à réaliser après frontière PA01.
"""

from __future__ import annotations

import datetime
import ipaddress
import uuid
from dataclasses import dataclass
from typing import Any

from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_bounded_keys as _base_check_keys
from pixs.pzt_ca.ca_identity import _is_utc_instant as _base_is_utc
from pixs.pzt_ca.ca_identity import _parse_rfc3339_utc as _base_parse_time
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_epoch as _base_require_epoch
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads

__all__ = [
    "InitialTerminalIdentityError",
    "InitialTerminalIdentity",
    "IDENTITY_OBJECT",
    "SCHEMA_VERSION",
    "TLS_USAGES",
    "identity_from_mapping",
    "identity_from_json",
]

SCHEMA_VERSION = "1.0.0"
IDENTITY_OBJECT = "z12.initial_terminal_identity/v1"

TLS_USAGES = ("clientAuth", "serverAuth")

_IDENTITY_REQUIRED = frozenset({
    "object_type", "schema_version", "identity_ref", "installation_ref",
    "target_ref", "terminal_ref", "native_instance_ref", "instance_uuid",
    "role_ref", "tls_usage", "key_ref", "key_generation_ref", "cert_ref",
    "root_authority_ref", "issuer_generation_ref", "policy_ref",
    "policy_version", "plan_ref", "plan_version", "epoch",
    "key_created_at", "not_before", "not_after",
    "hardware_evidence_ref", "possession_evidence_ref",
})
_IDENTITY_ALLOWED = frozenset({
    "object_type", "schema_version", "identity_ref", "installation_ref",
    "target_ref", "terminal_ref", "native_instance_ref", "instance_uuid",
    "role_ref", "tls_usage", "server_ipv4", "key_ref",
    "key_generation_ref", "cert_ref", "root_authority_ref",
    "issuer_generation_ref", "policy_ref", "policy_version",
    "plan_ref", "plan_version", "epoch", "key_created_at",
    "not_before", "not_after", "hardware_evidence_ref",
    "possession_evidence_ref",
})

_REF_FIELDS = (
    "identity_ref", "installation_ref", "target_ref", "terminal_ref",
    "native_instance_ref", "role_ref", "key_ref", "key_generation_ref",
    "cert_ref", "root_authority_ref", "issuer_generation_ref",
    "policy_ref", "policy_version", "plan_ref", "plan_version",
    "hardware_evidence_ref", "possession_evidence_ref",
)


class InitialTerminalIdentityError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> InitialTerminalIdentityError:
    return InitialTerminalIdentityError(code, element)


def _req_ref(value: object, element: str) -> None:
    try:
        _base_require_ref(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_ver(value: object, element: str) -> None:
    try:
        _base_require_ver(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_enum(value: object, expected: tuple[str, ...], element: str) -> None:
    try:
        _base_require_enum(value, expected, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_epoch(value: object, element: str) -> None:
    if type(value) is not int:
        raise _deny("EPOQUE_INVALIDE", element)
    try:
        _base_require_epoch(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _parse_time(value: object, element: str) -> datetime.datetime:
    try:
        return _base_parse_time(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _loads_mapping(text: object) -> dict[str, Any]:
    try:
        mapping = _base_loads(text)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping")
    return mapping


def _check_keys(mapping: dict[str, Any]) -> None:
    try:
        _base_check_keys(mapping, _IDENTITY_REQUIRED, _IDENTITY_ALLOWED)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_uuid(value: object, element: str) -> None:
    if type(value) is not str:
        raise _deny("UUID_INVALIDE", element)
    try:
        parsed = uuid.UUID(value)
    except ValueError:
        raise _deny("UUID_INVALIDE", element) from None
    if parsed.variant != uuid.RFC_4122:
        raise _deny("UUID_VARIANTE_INVALIDE", element)
    if parsed.version != 7:
        raise _deny("UUID_VERSION_INVALIDE", element)
    if str(parsed) != value:
        raise _deny("UUID_NON_CANONIQUE", element)


def _req_ipv4(value: object, element: str) -> None:
    if type(value) is not str:
        raise _deny("IP_INVALIDE", element)
    try:
        addr = ipaddress.IPv4Address(value)
    except ipaddress.AddressValueError:
        raise _deny("IP_INVALIDE", element) from None
    if str(addr) != value:
        raise _deny("IP_NON_CANONIQUE", element)
    if not addr.is_loopback:
        raise _deny("IP_NON_LOOPBACK", element)


def _req_instant(value: object, element: str) -> None:
    if type(value) is not datetime.datetime:
        raise _deny("HORODATAGE_NON_UTC", element)
    if not _base_is_utc(value):
        raise _deny("HORODATAGE_NON_UTC", element)


@dataclass(frozen=True, slots=True, repr=False)
class InitialTerminalIdentity:
    """Identité terminale §13.2, sans droit accordé."""

    object_type: str
    schema_version: str
    identity_ref: str
    installation_ref: str
    target_ref: str
    terminal_ref: str
    native_instance_ref: str
    instance_uuid: str
    role_ref: str
    tls_usage: str
    key_ref: str
    key_generation_ref: str
    cert_ref: str
    root_authority_ref: str
    issuer_generation_ref: str
    policy_ref: str
    policy_version: str
    plan_ref: str
    plan_version: str
    epoch: int
    key_created_at: datetime.datetime
    not_before: datetime.datetime
    not_after: datetime.datetime
    hardware_evidence_ref: str
    possession_evidence_ref: str
    server_ipv4: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny(
                "DISCRIMINATEUR_INVALIDE",
                "initial_terminal_identity.object_type",
            )
        if ot != IDENTITY_OBJECT:
            raise _deny(
                "DISCRIMINATEUR_INVALIDE",
                "initial_terminal_identity.object_type",
            )
        _req_ver(
            current(self, "schema_version"),
            "initial_terminal_identity.schema_version",
        )
        for name in _REF_FIELDS:
            _req_ref(
                current(self, name),
                f"initial_terminal_identity.{name}",
            )
        _req_enum(
            current(self, "tls_usage"), TLS_USAGES,
            "initial_terminal_identity.tls_usage",
        )
        _req_uuid(
            current(self, "instance_uuid"),
            "initial_terminal_identity.instance_uuid",
        )
        _req_epoch(
            current(self, "epoch"), "initial_terminal_identity.epoch"
        )
        for name in ("key_created_at", "not_before", "not_after"):
            _req_instant(
                current(self, name),
                f"initial_terminal_identity.{name}",
            )
        if current(self, "not_after") <= current(self, "not_before"):
            raise _deny(
                "PERIODE_INVALIDE", "initial_terminal_identity.not_after"
            )
        tls = current(self, "tls_usage")
        ip = current(self, "server_ipv4")
        if tls == "serverAuth":
            if ip is None:
                raise _deny(
                    "IP_ABSENTE",
                    "initial_terminal_identity.server_ipv4",
                )
            _req_ipv4(ip, "initial_terminal_identity.server_ipv4")
        else:
            if ip is not None:
                raise _deny(
                    "IP_INTERDITE",
                    "initial_terminal_identity.server_ipv4",
                )


def identity_from_mapping(mapping: dict[str, Any]) -> InitialTerminalIdentity:
    """Construit une identité depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "initial_terminal_identity")
    _check_keys(mapping)
    return InitialTerminalIdentity(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        identity_ref=mapping["identity_ref"],
        installation_ref=mapping["installation_ref"],
        target_ref=mapping["target_ref"],
        terminal_ref=mapping["terminal_ref"],
        native_instance_ref=mapping["native_instance_ref"],
        instance_uuid=mapping["instance_uuid"],
        role_ref=mapping["role_ref"],
        tls_usage=mapping["tls_usage"],
        key_ref=mapping["key_ref"],
        key_generation_ref=mapping["key_generation_ref"],
        cert_ref=mapping["cert_ref"],
        root_authority_ref=mapping["root_authority_ref"],
        issuer_generation_ref=mapping["issuer_generation_ref"],
        policy_ref=mapping["policy_ref"],
        policy_version=mapping["policy_version"],
        plan_ref=mapping["plan_ref"],
        plan_version=mapping["plan_version"],
        epoch=mapping["epoch"],
        key_created_at=_parse_time(
            mapping["key_created_at"],
            "initial_terminal_identity.key_created_at",
        ),
        not_before=_parse_time(
            mapping["not_before"],
            "initial_terminal_identity.not_before",
        ),
        not_after=_parse_time(
            mapping["not_after"],
            "initial_terminal_identity.not_after",
        ),
        hardware_evidence_ref=mapping["hardware_evidence_ref"],
        possession_evidence_ref=mapping["possession_evidence_ref"],
        server_ipv4=mapping.get("server_ipv4"),
    )


def identity_from_json(text: object) -> InitialTerminalIdentity:
    """Analyse JSON strict puis construit, sans normalisation."""
    return identity_from_mapping(_loads_mapping(text))
