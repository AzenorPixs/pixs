"""Modèle Django interne EventEnvelopeV1, codec TEXT privé, insert-only.

Treize clés exactes sans défaut logique, event_id clé primaire explicite.
Payload en TEXT JSON privé, sans wire, canon, hash ou JSONB.
Limites explicites de l'appelant, capture exacte bornée avant serializer,
snapshot frozen MappingProxy/tuple, exports thaw owned.
save exige un alias explicite et une transaction propriétaire active ;
QuerySet.update/SQL brut hors primitive, pas d’immuabilité globale DB.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType

from django.core.exceptions import ValidationError
from django.db import models, transaction

from pixs.backend.bulk_event_envelope_values import validate_bulk_event_envelope_values
from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_runtime_records import _TrustedUtcDateTimeField

__all__ = ["BulkEventEnvelopeRecord"]

_FIELDS = (
    "event_id", "kind", "event_type", "event_version",
    "producer_reference", "schema_reference", "order_scope_reference",
    "occurred_at", "subject_reference", "tenant_context_reference",
    "correlation_id", "causation_id", "payload",
)

_INVALID = "valeurs event envelope bulk invalides"
_CAPACITY = "capacite JSON de persistance non supportee"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_event_envelope_invalid")


def _capacity() -> ValidationError:
    return ValidationError(_CAPACITY, code="bulk_event_envelope_capacity_unsupported")


def _check_limits(max_depth: object, max_members: object, non_tenant_authorized: object) -> None:
    if type(max_depth) is not int or max_depth <= 0:
        raise _invalid()
    if type(max_members) is not int or max_members <= 0:
        raise _invalid()
    if type(non_tenant_authorized) is not bool:
        raise _invalid()


def _parse_int(text: object) -> int:
    try:
        return int(text)
    except ValueError:
        raise _capacity() from None


def _reject_const(value: object) -> object:
    raise ValueError("constante refusee")


def _no_dup_object(pairs: object) -> dict:
    items = tuple(pairs)
    if len({key for key, _value in items}) != len(items):
        raise ValueError("doublon refuse")
    return dict(items)


def _capture_payload(node: object, *, max_depth: int, max_members: int, depth: int, seen: set) -> object:
    node_type = type(node)
    if node is None or node_type is bool or node_type is int:
        return node
    if node_type is float:
        if not math.isfinite(node):
            raise _invalid()
        return node
    if node_type is str:
        try:
            node.encode("utf-8")
        except UnicodeEncodeError:
            raise _invalid() from None
        return node
    if node_type is list:
        if depth > max_depth:
            raise _invalid()
        if len(node) > max_members:
            raise _invalid()
        if id(node) in seen:
            raise _invalid()
        seen.add(id(node))
        try:
            return [_capture_payload(item, max_depth=max_depth, max_members=max_members, depth=depth + 1, seen=seen) for item in node]
        finally:
            seen.discard(id(node))
    if node_type is dict:
        if depth > max_depth:
            raise _invalid()
        if len(node) > max_members:
            raise _invalid()
        if id(node) in seen:
            raise _invalid()
        items = tuple(node.items())
        if any(type(key) is not str for key, _value in items):
            raise _invalid()
        for key, _value in items:
            try:
                key.encode("utf-8")
            except UnicodeEncodeError:
                raise _invalid() from None
        seen.add(id(node))
        try:
            return {key: _capture_payload(value, max_depth=max_depth, max_members=max_members, depth=depth + 1, seen=seen) for key, value in items}
        finally:
            seen.discard(id(node))
    raise _invalid()


def _capture_root(payload: object, *, max_depth: int, max_members: int) -> object:
    try:
        return _capture_payload(payload, max_depth=max_depth, max_members=max_members, depth=1, seen=set())
    except RecursionError:
        raise _capacity() from None


def _freeze_json(node: object) -> object:
    node_type = type(node)
    if node is None or node_type is bool or node_type is int or node_type is float or node_type is str:
        return node
    if node_type is list:
        return tuple(_freeze_json(item) for item in node)
    if node_type is dict:
        return MappingProxyType({key: _freeze_json(value) for key, value in tuple(node.items())})
    raise _invalid()


def _thaw_json(node: object) -> object:
    node_type = type(node)
    if node is None or node_type is bool or node_type is int or node_type is float or node_type is str:
        return node
    if node_type is tuple:
        return [_thaw_json(item) for item in node]
    if node_type is MappingProxyType:
        return {key: _thaw_json(value) for key, value in tuple(node.items())}
    raise _invalid()


def _encode_payload(payload: object) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    except (ValueError, RecursionError):
        raise _capacity() from None


def _decode_trusted(text: object) -> object:
    if type(text) is not str:
        raise _invalid()
    try:
        return json.loads(text, object_pairs_hook=_no_dup_object, parse_constant=_reject_const, parse_int=_parse_int)
    except RecursionError:
        raise _capacity() from None
    except ValueError:
        raise _invalid() from None


@dataclass(frozen=True, slots=True)
class _EventEnvelopeSnapshot:
    event_id: str
    kind: str
    event_type: str
    event_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str
    occurred_at: datetime
    subject_reference: str
    tenant_context_reference: str | None
    correlation_id: str
    causation_id: str | None
    payload: object

    def as_values(self) -> dict:
        try:
            return {
                "event_id": self.event_id,
                "kind": self.kind,
                "event_type": self.event_type,
                "event_version": self.event_version,
                "producer_reference": self.producer_reference,
                "schema_reference": self.schema_reference,
                "order_scope_reference": self.order_scope_reference,
                "occurred_at": self.occurred_at,
                "subject_reference": self.subject_reference,
                "tenant_context_reference": self.tenant_context_reference,
                "correlation_id": self.correlation_id,
                "causation_id": self.causation_id,
                "payload": _thaw_json(self.payload),
            }
        except RecursionError:
            raise _capacity() from None


def _resolve_limits(stored: object, max_depth: object, max_members: object, non_tenant_authorized: object):
    if max_depth is None and max_members is None and non_tenant_authorized is None:
        if type(stored) is not tuple or len(stored) != 3:
            raise _invalid()
        depth, members, flag = stored
        _check_limits(depth, members, flag)
        return depth, members, flag
    _check_limits(max_depth, max_members, non_tenant_authorized)
    return max_depth, max_members, non_tenant_authorized


class BulkEventEnvelopeRecord(models.Model):
    event_id = models.TextField(primary_key=True, serialize=False)
    kind = models.TextField(choices=[("DOMAIN", "DOMAIN"), ("INTEGRATION", "INTEGRATION")])
    event_type = models.TextField()
    event_version = models.TextField()
    producer_reference = models.TextField()
    schema_reference = models.TextField()
    order_scope_reference = models.TextField()
    occurred_at = _TrustedUtcDateTimeField()
    subject_reference = models.TextField()
    tenant_context_reference = models.TextField(blank=True, null=True)
    correlation_id = models.TextField()
    causation_id = models.TextField(blank=True, null=True)
    payload = models.TextField()

    @classmethod
    def from_values(cls, values: object, *, max_depth: object, max_members: object, non_tenant_authorized: object) -> "BulkEventEnvelopeRecord":
        if cls is not BulkEventEnvelopeRecord:
            raise _invalid()
        _check_limits(max_depth, max_members, non_tenant_authorized)
        if type(values) is not dict:
            raise _invalid()
        items = tuple(values.items())
        if any(type(key) is not str for key, _value in items):
            raise _invalid()
        snapshot = dict(items)
        if len(snapshot) != 13 or any(field not in snapshot for field in _FIELDS):
            raise _invalid()
        copied = {field: snapshot[field] for field in _FIELDS}
        copied["payload"] = _capture_root(snapshot["payload"], max_depth=max_depth, max_members=max_members)
        if validate_bulk_event_envelope_values(copied, max_depth=max_depth, max_members=max_members, non_tenant_authorized=non_tenant_authorized):
            raise _invalid()
        encoded = _encode_payload(copied["payload"])
        row = cls(
            event_id=copied["event_id"], kind=copied["kind"], event_type=copied["event_type"],
            event_version=copied["event_version"], producer_reference=copied["producer_reference"],
            schema_reference=copied["schema_reference"], order_scope_reference=copied["order_scope_reference"],
            occurred_at=copied["occurred_at"], subject_reference=copied["subject_reference"],
            tenant_context_reference=copied["tenant_context_reference"],
            correlation_id=copied["correlation_id"], causation_id=copied["causation_id"],
            payload=encoded,
        )
        row._envelope_limits = (max_depth, max_members, non_tenant_authorized)
        return row

    def _locked_snapshot(self, *, max_depth: object = None, max_members: object = None, non_tenant_authorized: object = None) -> _EventEnvelopeSnapshot:
        state = self.__dict__
        stored = state.get("_envelope_limits")
        depth, members, flag = _resolve_limits(stored, max_depth, max_members, non_tenant_authorized)
        for field in _FIELDS:
            if field not in state:
                raise _invalid()
        payload_text = state.get("payload")
        decoded = _decode_trusted(payload_text)
        logical = {
            "event_id": state.get("event_id"), "kind": state.get("kind"),
            "event_type": state.get("event_type"), "event_version": state.get("event_version"),
            "producer_reference": state.get("producer_reference"),
            "schema_reference": state.get("schema_reference"),
            "order_scope_reference": state.get("order_scope_reference"),
            "occurred_at": state.get("occurred_at"),
            "subject_reference": state.get("subject_reference"),
            "tenant_context_reference": state.get("tenant_context_reference"),
            "correlation_id": state.get("correlation_id"),
            "causation_id": state.get("causation_id"),
            "payload": decoded,
        }
        if validate_bulk_event_envelope_values(logical, max_depth=depth, max_members=members, non_tenant_authorized=flag):
            raise _invalid()
        try:
            frozen = _freeze_json(logical["payload"])
        except RecursionError:
            raise _capacity() from None
        return _EventEnvelopeSnapshot(
            event_id=logical["event_id"], kind=logical["kind"],
            event_type=logical["event_type"], event_version=logical["event_version"],
            producer_reference=logical["producer_reference"],
            schema_reference=logical["schema_reference"],
            order_scope_reference=logical["order_scope_reference"],
            occurred_at=logical["occurred_at"],
            subject_reference=logical["subject_reference"],
            tenant_context_reference=logical["tenant_context_reference"],
            correlation_id=logical["correlation_id"],
            causation_id=logical["causation_id"], payload=frozen,
        )

    def as_values(self, *, max_depth: object = None, max_members: object = None, non_tenant_authorized: object = None) -> dict:
        return self._locked_snapshot(max_depth=max_depth, max_members=max_members, non_tenant_authorized=non_tenant_authorized).as_values()

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True, *, max_depth: object = None, max_members: object = None, non_tenant_authorized: object = None):
        self._locked_snapshot(max_depth=max_depth, max_members=max_members, non_tenant_authorized=non_tenant_authorized)
        try:
            return super().full_clean(exclude=exclude, validate_unique=False, validate_constraints=False)
        except ValidationError as exc:
            raise _invalid() from exc

    def save(self, *args, force_insert=None, force_update=False, using=None, update_fields=None) -> None:
        if args:
            raise _invalid()
        if force_insert is not True:
            raise _invalid()
        if force_update is not False:
            raise _invalid()
        if update_fields is not None:
            raise _invalid()
        if type(using) is not str:
            raise _invalid()
        if not _is_runtime_text(using):
            raise _invalid()
        if self._state.adding is not True:
            raise _invalid()
        stored = self.__dict__.get("_envelope_limits")
        _resolve_limits(stored, None, None, None)
        self._locked_snapshot()
        if transaction.get_connection(using).in_atomic_block is not True:
            raise _invalid()
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(event_id=""), name="bulkeventenvelope_event_non_empty"),
            models.CheckConstraint(condition=models.Q(kind__in=["DOMAIN", "INTEGRATION"]), name="bulkeventenvelope_kind_member"),
            models.CheckConstraint(condition=~models.Q(event_type=""), name="bulkeventenvelope_type_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_version=""), name="bulkeventenvelope_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(producer_reference=""), name="bulkeventenvelope_producer_non_empty"),
            models.CheckConstraint(condition=~models.Q(schema_reference=""), name="bulkeventenvelope_schema_non_empty"),
            models.CheckConstraint(condition=~models.Q(order_scope_reference=""), name="bulkeventenvelope_scope_non_empty"),
            models.CheckConstraint(condition=~models.Q(subject_reference=""), name="bulkeventenvelope_subject_non_empty"),
            models.CheckConstraint(condition=(models.Q(tenant_context_reference__isnull=True) | ~models.Q(tenant_context_reference="")), name="bulkeventenvelope_tenant_non_empty"),
            models.CheckConstraint(condition=~models.Q(correlation_id=""), name="bulkeventenvelope_correlation_non_empty"),
            models.CheckConstraint(condition=(models.Q(causation_id__isnull=True) | ~models.Q(causation_id="")), name="bulkeventenvelope_causation_non_empty"),
            models.CheckConstraint(condition=~models.Q(payload=""), name="bulkeventenvelope_payload_non_empty"),
        ]
