"""Valeurs C09 : schéma fermé, politique explicite et enveloppe immuable.

Ces validations sont structurelles. Elles n'accordent aucun droit, n'ouvrent
aucune transaction et ne prouvent ni le dispatcher ni la disponibilité d'un
profil. Les références conservent leur ordre et leur contenu exacts.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import dataclass, fields

from pixs.backend.c09_authorization_adapter import (
    C09Identity, C09Refused, validate_c09_identity,
)
from pixs.backend.c09_contracts import C09PolicyV1, validate_c09_policy
from pixs.backend.c09_registry import C09RegistryV1, validate_c09_registry
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.event_contract import DomainEventContract, IntegrationEventContract
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "C09DeliveryPolicyV1", "C09EventSchemaBindingV1", "C09EventEnvelopeV1",
    "validate_c09_delivery_policy", "validate_c09_event_schema_binding",
    "validate_c09_delivery_catalog", "validate_c09_event_envelope",
    "c09_canonical_payload_bytes", "c09_payload_content_sha256",
    "c09_delivery_fingerprint", "c09_envelope_document_without_hash",
    "c09_envelope_canonical_bytes", "c09_envelope_content_sha256",
    "c09_envelope_wire_bytes", "export_c09_event_schema",
    "c09_envelope_from_document", "c09_envelope_from_wire_bytes",
]

_I32 = 2**31 - 1
_I64 = 2**63 - 1


def _diag(element, reason):
    return Diagnostic(step=VALIDATE, element=element, constraint=reason, message=reason)


def _pack(items):
    unique = {(d.element, d.constraint, d.message): d for d in items}
    return [unique[key] for key in sorted(unique)]


def _text(value):
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeError:
        return False
    return True


def _version(value):
    if not _text(value):
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _utc(value):
    return type(value) is dt.datetime and value.tzinfo is dt.timezone.utc


def _hex(value):
    return type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _identity(value):
    if type(value) is not C09Identity:
        return False
    try:
        validate_c09_identity(value)
        context = value.context
        if type(context) is not ScopeContext:
            return False
        validate_structure(context)
    except (C09Refused, ScopeStructureError):
        return False
    return all(part is None or _text(part) for part in (context.tenant_id, context.scope_id))


def _json(document):
    # Appel après validation des valeurs exactes ; aucun default/coercition.
    return json.dumps(document, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


@dataclass(frozen=True, slots=True)
class C09DeliveryPolicyV1:
    base_policy: C09PolicyV1
    delivery_policy_reference: str
    delivery_policy_version: str
    max_event_bytes: int
    max_payload_refs: int
    max_pending_events: int
    max_pending_deliveries: int


@dataclass(frozen=True, slots=True)
class C09EventSchemaBindingV1:
    entry_reference: str
    owner_reference: str
    tenant_context_reference: str | None
    perimeter_reference: str
    kind: str
    event_type: str
    event_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str


@dataclass(frozen=True, slots=True, repr=False)
class C09EventEnvelopeV1:
    event_id: str
    kind: str
    identity: C09Identity
    entry_reference: str
    event_type: str
    event_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str
    causation_id: str | None
    occurred_at: dt.datetime
    sequence_index: int
    payload_refs: tuple[str, ...]
    request_content_sha256: str
    content_sha256: str


def validate_c09_delivery_policy(candidate):
    if type(candidate) is not C09DeliveryPolicyV1:
        return [_diag("c09_delivery_policy", "politique exacte attendue")]
    errors = []
    base = candidate.base_policy
    if validate_c09_policy(base):
        errors.append(_diag("c09_delivery_policy.base_policy", "politique base valide attendue"))
    elif not _text(base.policy_reference) or not _version(base.policy_version):
        errors.append(_diag("c09_delivery_policy.base_policy", "références base représentables attendues"))
    if not _text(candidate.delivery_policy_reference):
        errors.append(_diag("c09_delivery_policy.reference", "référence exacte représentable attendue"))
    if not _version(candidate.delivery_policy_version):
        errors.append(_diag("c09_delivery_policy.version", "version SemVer complète attendue"))
    for name in ("max_event_bytes", "max_payload_refs", "max_pending_events", "max_pending_deliveries"):
        value = getattr(candidate, name)
        if type(value) is not int or not 1 <= value <= _I32:
            errors.append(_diag("c09_delivery_policy." + name, "entier exact borné attendu"))
    # Evénements et livraisons ont des budgets indépendants ; le fan-out est
    # contrôlé atomiquement au stage, sous les deux plafonds.
    return _pack(errors)


def c09_delivery_fingerprint(policy):
    if validate_c09_delivery_policy(policy):
        raise ValueError("Politique livraison C09 invalide.")
    base = {field.name: getattr(policy.base_policy, field.name) for field in fields(C09PolicyV1)}
    base["effective_from"] = policy.base_policy.effective_from.isoformat()
    document = {field.name: getattr(policy, field.name) for field in fields(C09DeliveryPolicyV1)
                if field.name != "base_policy"}
    document["base_policy"] = base
    return hashlib.sha256(_json(document)).hexdigest()


def _binding_errors(candidate):
    if type(candidate) is not C09EventSchemaBindingV1:
        return [_diag("c09_schema_binding", "liaison exacte attendue")]
    errors = []
    for name in ("entry_reference", "owner_reference", "perimeter_reference",
                 "event_type", "producer_reference", "schema_reference", "order_scope_reference"):
        if not _text(getattr(candidate, name)):
            errors.append(_diag("c09_schema_binding." + name, "référence exacte représentable attendue"))
    if candidate.tenant_context_reference is not None and not _text(candidate.tenant_context_reference):
        errors.append(_diag("c09_schema_binding.tenant_context_reference", "référence ou absence explicite attendue"))
    if type(candidate.kind) is not str or candidate.kind not in ("DOMAIN", "INTEGRATION"):
        errors.append(_diag("c09_schema_binding.kind", "genre fermé attendu"))
    if not _version(candidate.event_version):
        errors.append(_diag("c09_schema_binding.event_version", "version SemVer complète attendue"))
    return errors


def validate_c09_event_schema_binding(candidate, registry):
    errors = _binding_errors(candidate)
    if errors:
        return _pack(errors)
    if validate_c09_registry(registry):
        return [_diag("c09_schema_binding.registry", "registre C09 valide attendu")]
    # Toutes les valeurs comparées sont maintenant des types exacts validés.
    linked = next((b for b in registry.bindings if b.entry_reference == candidate.entry_reference), None)
    if linked is None:
        return [_diag("c09_schema_binding.entry_reference", "entrée absente du registre")]
    for name in ("owner_reference", "perimeter_reference", "tenant_context_reference"):
        if getattr(linked, name) != getattr(candidate, name):
            errors.append(_diag("c09_schema_binding." + name, "liaison divergente du registre"))
    contract = linked.contract
    expected_type = DomainEventContract if candidate.kind == "DOMAIN" else IntegrationEventContract
    if type(contract) is not expected_type:
        errors.append(_diag("c09_schema_binding.kind", "contrat du genre déclaré attendu"))
    for target, source in (("event_type", "event_type"), ("event_version", "contract_version"),
                           ("producer_reference", "producer_reference"), ("schema_reference", "schema_reference"),
                           ("order_scope_reference", "order_scope_reference")):
        if getattr(candidate, target) != getattr(contract, source):
            errors.append(_diag("c09_schema_binding." + target, "contrat déclaré divergent"))
    return _pack(errors)


def validate_c09_delivery_catalog(registry, bindings, policy):
    errors = []
    if validate_c09_registry(registry):
        errors.append(_diag("c09_delivery_catalog.registry", "registre C09 valide attendu"))
    if validate_c09_delivery_policy(policy):
        errors.append(_diag("c09_delivery_catalog.policy", "politique livraison valide attendue"))
    if type(bindings) is not tuple or not bindings:
        errors.append(_diag("c09_delivery_catalog.bindings", "tuple exact non vide attendu"))
    if errors:
        return _pack(errors)
    for binding in bindings:
        errors.extend(validate_c09_event_schema_binding(binding, registry))
    if errors:
        return _pack(errors)
    entries = [binding.entry_reference for binding in bindings]
    if len(set(entries)) != len(entries):
        errors.append(_diag("c09_delivery_catalog.bindings", "entrée de schéma répétée refusée"))
    for entry in entries:
        consumers = [c for c in registry.consumers if c.entry_reference == entry]
        if not consumers:
            errors.append(_diag("c09_delivery_catalog.consumers", "consommateur déclaré requis pour livraison locale"))
        for consumer in consumers:
            if not all(_text(v) for v in (consumer.consumer_reference, consumer.entry_reference,
                                         consumer.component_reference)):
                errors.append(_diag("c09_delivery_catalog.consumers", "références consommateur représentables attendues"))
    return _pack(errors)


def _payload(payload_refs):
    if type(payload_refs) is not tuple or not payload_refs:
        return False
    # Aucun hachage avant garde de TOUS les éléments.
    if not all(_text(item) for item in payload_refs):
        return False
    return len(set(payload_refs)) == len(payload_refs)


def c09_canonical_payload_bytes(payload_refs):
    if not _payload(payload_refs):
        raise ValueError("Références payload C09 invalides.")
    return _json({"payload_refs": list(payload_refs)})


def c09_payload_content_sha256(payload_refs):
    return hashlib.sha256(c09_canonical_payload_bytes(payload_refs)).hexdigest()


def _envelope_errors(envelope):
    if type(envelope) is not C09EventEnvelopeV1:
        return [_diag("c09_envelope", "enveloppe exacte attendue")]
    errors = []
    if not _identity(envelope.identity):
        errors.append(_diag("c09_envelope.identity", "identité C09 représentable attendue"))
    for name in ("event_id", "entry_reference", "event_type", "producer_reference",
                 "schema_reference", "order_scope_reference"):
        if not _text(getattr(envelope, name)):
            errors.append(_diag("c09_envelope." + name, "référence exacte représentable attendue"))
    if type(envelope.kind) is not str or envelope.kind not in ("DOMAIN", "INTEGRATION"):
        errors.append(_diag("c09_envelope.kind", "genre fermé attendu"))
    if not _version(envelope.event_version):
        errors.append(_diag("c09_envelope.event_version", "version SemVer complète attendue"))
    if envelope.causation_id is not None and not _text(envelope.causation_id):
        errors.append(_diag("c09_envelope.causation_id", "référence ou absence explicite attendue"))
    if not _utc(envelope.occurred_at):
        errors.append(_diag("c09_envelope.occurred_at", "instant UTC exact attendu"))
    if type(envelope.sequence_index) is not int or not 1 <= envelope.sequence_index <= _I64:
        errors.append(_diag("c09_envelope.sequence_index", "entier exact I64 positif attendu"))
    if not _payload(envelope.payload_refs):
        errors.append(_diag("c09_envelope.payload_refs", "tuple de références exactes distinctes attendu"))
    if not _hex(envelope.request_content_sha256):
        errors.append(_diag("c09_envelope.request_content_sha256", "empreinte source attendue"))
    return errors


def c09_envelope_document_without_hash(envelope):
    if _envelope_errors(envelope):
        raise ValueError("Enveloppe C09 invalide.")
    identity, context = envelope.identity, envelope.identity.context
    return {
        "event_id": envelope.event_id, "kind": envelope.kind,
        "entry_reference": envelope.entry_reference, "event_type": envelope.event_type,
        "event_version": envelope.event_version, "producer_reference": envelope.producer_reference,
        "schema_reference": envelope.schema_reference, "order_scope_reference": envelope.order_scope_reference,
        "perimeter_reference": identity.perimeter_reference, "actor_reference": identity.actor_reference,
        "resource_id": identity.resource_id, "action_id": identity.action_id,
        "request_reference": identity.request_reference, "request_version": identity.request_version,
        "correlation_id": identity.correlation_id, "causation_id": envelope.causation_id,
        "occurred_at": envelope.occurred_at.isoformat(), "sequence_index": envelope.sequence_index,
        "payload": {"payload_refs": list(envelope.payload_refs)},
        "request_content_sha256": envelope.request_content_sha256,
        "context": {"scope_type": context.scope_type.value,
                    "tenant_id": context.tenant_id, "scope_id": context.scope_id},
    }


def c09_envelope_canonical_bytes(envelope):
    """Octets sans content_sha256, uniquement pour le calcul de cette empreinte."""
    return _json(c09_envelope_document_without_hash(envelope))


def c09_envelope_content_sha256(envelope):
    return hashlib.sha256(c09_envelope_canonical_bytes(envelope)).hexdigest()


def c09_envelope_wire_bytes(envelope):
    """Octets de l'enveloppe complète, empreinte incluse."""
    document = c09_envelope_document_without_hash(envelope)
    expected = hashlib.sha256(_json(document)).hexdigest()
    if not _hex(envelope.content_sha256) or envelope.content_sha256 != expected:
        raise ValueError("Empreinte enveloppe C09 invalide.")
    document["content_sha256"] = expected
    return _json(document)


def validate_c09_event_envelope(candidate, binding, delivery):
    errors = _envelope_errors(candidate) + _binding_errors(binding)
    if validate_c09_delivery_policy(delivery):
        errors.append(_diag("c09_envelope.delivery", "politique livraison valide attendue"))
    if errors:
        return _pack(errors)
    for name in ("entry_reference", "event_type", "event_version", "producer_reference",
                 "schema_reference", "order_scope_reference", "kind"):
        if getattr(candidate, name) != getattr(binding, name):
            errors.append(_diag("c09_envelope." + name, "liaison de schéma divergente"))
    if candidate.identity.perimeter_reference != binding.perimeter_reference:
        errors.append(_diag("c09_envelope.perimeter_reference", "périmètre de liaison divergent"))
    if len(candidate.payload_refs) > delivery.max_payload_refs:
        errors.append(_diag("c09_envelope.payload_refs", "plafond de références dépassé"))
    try:
        wire = c09_envelope_wire_bytes(candidate)
    except ValueError:
        errors.append(_diag("c09_envelope.content_sha256", "empreinte enveloppe complète attendue"))
    else:
        if len(wire) > delivery.max_event_bytes:
            errors.append(_diag("c09_envelope.document", "plafond enveloppe complète dépassé"))
    return _pack(errors)


def export_c09_event_schema(binding, delivery, registry):
    if validate_c09_event_schema_binding(binding, registry) or validate_c09_delivery_policy(delivery):
        raise ValueError("Schéma événement C09 invalide.")
    return {
        "schema_reference": binding.schema_reference, "entry_reference": binding.entry_reference,
        "kind": binding.kind, "event_type": binding.event_type, "event_version": binding.event_version,
        "format": "JSON_SCHEMA_2020_12",
        "payload": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object", "properties": {
                "payload_refs": {"type": "array", "items": {
                    "type": "string", "minLength": 1, "pattern": "^[^\\u0000]+$",
                }, "minItems": 1, "uniqueItems": True, "maxItems": delivery.max_payload_refs},
            }, "required": ["payload_refs"], "additionalProperties": False,
        },
        "max_event_bytes": delivery.max_event_bytes,
    }

def c09_envelope_from_document(document, binding, delivery, registry):
    """Reconstruit strictement une enveloppe wire V1, sans normalisation."""
    from pixs.core.scope.context import ScopeType
    if validate_c09_event_schema_binding(binding, registry) or validate_c09_delivery_policy(delivery):
        raise ValueError("Catalogue événement C09 invalide.")
    names = {
        "event_id", "kind", "entry_reference", "event_type", "event_version",
        "producer_reference", "schema_reference", "order_scope_reference",
        "perimeter_reference", "actor_reference", "resource_id", "action_id",
        "request_reference", "request_version", "correlation_id", "causation_id",
        "occurred_at", "sequence_index", "payload", "request_content_sha256",
        "context", "content_sha256",
    }
    def mapping(value, keys):
        if type(value) is not dict or not all(type(k) is str for k in value):
            raise ValueError("Document événement C09 invalide.")
        if set(value) != keys:
            raise ValueError("Document événement C09 invalide.")
        return value
    doc = mapping(document, names)
    context = mapping(doc["context"], {"scope_type", "tenant_id", "scope_id"})
    if type(context["scope_type"]) is not str or context["scope_type"] not in ("PLATFORM", "TENANT"):
        raise ValueError("Contexte événement C09 invalide.")
    for part in (context["tenant_id"], context["scope_id"]):
        if part is not None and not _text(part):
            raise ValueError("Contexte événement C09 invalide.")
    try:
        scope = ScopeContext(ScopeType(context["scope_type"]), context["tenant_id"], context["scope_id"])
    except ScopeStructureError:
        raise ValueError("Contexte événement C09 invalide.") from None
    identity = C09Identity(
        doc["actor_reference"], doc["perimeter_reference"], doc["request_reference"],
        doc["request_version"], doc["resource_id"], doc["action_id"], scope, doc["correlation_id"],
    )
    if not _identity(identity):
        raise ValueError("Identité événement C09 invalide.")
    payload = mapping(doc["payload"], {"payload_refs"})
    refs = payload["payload_refs"]
    if type(refs) is not list or not 1 <= len(refs) <= delivery.max_payload_refs:
        raise ValueError("Payload événement C09 invalide.")
    refs = tuple(refs)
    if not _payload(refs):
        raise ValueError("Payload événement C09 invalide.")
    occurred = doc["occurred_at"]
    if not _text(occurred) or len(occurred) not in (25, 32):
        raise ValueError("Instant événement C09 invalide.")
    try:
        instant = dt.datetime.fromisoformat(occurred)
    except ValueError:
        raise ValueError("Instant événement C09 invalide.") from None
    if not _utc(instant) or instant.isoformat() != occurred:
        raise ValueError("Instant événement C09 invalide.")
    event = C09EventEnvelopeV1(
        doc["event_id"], doc["kind"], identity, doc["entry_reference"], doc["event_type"],
        doc["event_version"], doc["producer_reference"], doc["schema_reference"],
        doc["order_scope_reference"], doc["causation_id"], instant, doc["sequence_index"],
        refs, doc["request_content_sha256"], doc["content_sha256"],
    )
    if validate_c09_event_envelope(event, binding, delivery):
        raise ValueError("Enveloppe événement C09 invalide.")
    # Toutes les valeurs sont désormais des types exacts validés.
    if json.loads(c09_envelope_wire_bytes(event)) != document:
        raise ValueError("Document événement C09 non canonique.")
    return event


def c09_envelope_from_wire_bytes(raw, binding, delivery, registry):
    """Décode des octets bornés, sans doublon de clé ou coercition."""
    if validate_c09_delivery_policy(delivery) or type(raw) is not bytes:
        raise ValueError("Octets événement C09 invalides.")
    if not 1 <= len(raw) <= delivery.max_event_bytes:
        raise ValueError("Octets événement C09 invalides.")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Clé événement C09 répétée.")
            result[key] = value
        return result
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeError, ValueError, RecursionError):
        raise ValueError("Octets événement C09 invalides.") from None
    return c09_envelope_from_document(document, binding, delivery, registry)
