"""Cycle de vie de la gestion DNS : PostgreSQL réel, aucun exécutant lancé."""
from __future__ import annotations

import datetime
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import DatabaseError, connections, transaction
from django.db.migrations.recorder import MigrationRecorder
from pixs.core.audit_contracts import (AuditError, apply_redactions_generic, canonical_generic_bytes, serialize_generic)
from pixs.core.scope.context import ScopeContext, validate_structure, ScopeStructureError
from pixs.kernel.lifecycle.state import LifecycleState
from pixs.kernel.lifecycle.availability import CapabilityObservation
from pixs.dns.models import DesiredDnsRecord, DnsNameRecord, DnsIdempotenceRecord
from pixs.dns.services import PostgresDnsService, DnsManagementPolicy, DnsServiceError


class DnsManagementAdapter:
    component_id = "pixs.dns"
    component_version = "0.1.0"

    def __init__(self, *, service, enabled, context, capability_bound):
        if type(service) is not PostgresDnsService or type(enabled) is not bool or type(capability_bound) is not bool:
            raise DnsServiceError("DNS_COMPOSITION_INVALID")
        if type(context) is not ScopeContext:
            raise DnsServiceError("DNS_COMPOSITION_INVALID")
        try:
            validate_structure(context)
        except ScopeStructureError:
            raise DnsServiceError("DNS_COMPOSITION_INVALID") from None
        self._service, self._enabled, self._context = service, enabled, context
        self._capability_bound = capability_bound
        self._active = False

    async def __aenter__(self):
        if self._active:
            raise DnsServiceError("DNS_LIFECYCLE_INVALID")
        self._active = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._active = False
        return False

    def observe_lifecycle(self):
        if not self._active or not apps.is_installed("pixs.dns"):
            return LifecycleState()
        connection = connections[self._service._alias]
        if connection.vendor != "postgresql":
            return LifecycleState()
        installed, configured, healthy = False, False, False
        try:
            with transaction.atomic(using=self._service._alias):
                migrations = MigrationRecorder(connection).applied_migrations()
                tables = connection.introspection.table_names()
                models = (DesiredDnsRecord, DnsNameRecord, DnsIdempotenceRecord,)
                installed = (
                    ("pixs_dns", "0001_initial") in migrations
                    and all(model._meta.db_table in tables for model in models)
                )
                if installed:
                    for model in models:
                        # Lecture des colonnes réelles, jamais affichée ; aucune mutation.
                        tuple(model.objects.using(self._service._alias).values_list(
                            *(field.attname for field in model._meta.concrete_fields))[:1])
                    moment = self._service._clock.now()
                    if (type(moment) is not datetime.datetime
                            or moment.tzinfo is not datetime.timezone.utc):
                        raise DnsServiceError("DNS_CLOCK_INVALID")
                    policy = self._service._policy.resolve(
                        context=self._context, alias=self._service._alias,
                        operation_id="lifecycle:pixs.dns",
                    )
                    if type(policy) is not DnsManagementPolicy:
                        raise DnsServiceError("DNS_DnsManagementPolicy_INVALID")
                    policy.__post_init__()
                    configured = policy.governance is not None
                    audit_policy = self._service._audit.policy(self._context, self._service._alias)
                    self._service._audit.now()
                    probe = self._service._event(
                        actor="UNVERIFIED", context=self._context,
                        action="management_probe", target=self.component_id,
                        result="DENIED", reason="LIFECYCLE_PROBE",
                        correlations=("lifecycle:" + self.component_id,), causations=(),
                    )
                    payload = apply_redactions_generic(serialize_generic(probe), audit_policy.redactions)
                    if len(canonical_generic_bytes(payload)) > audit_policy.max_event_bytes:
                        raise AuditError("AUDIT_EVENT_TOO_LARGE")
                    healthy = True
        except (DatabaseError, ValidationError, AuditError, DnsServiceError):
            # Les dimensions restent fermées ; aucun détail de connexion exposé.
            healthy = False
        enabled = installed and self._enabled
        configured = installed and configured
        return LifecycleState(
            installed, enabled, configured, healthy,
            installed and enabled and configured and healthy,
        )

    def observe_capabilities(self):
        # Sélection de la composition serveur ; le Kernel vérifie aussi la liaison.
        if not self._capability_bound:
            return ()
        state = self.observe_lifecycle()
        return (CapabilityObservation("dns.management", "1.0.0", self.component_id, state.ready),)

    def _guard(self):
        if not self.observe_lifecycle().ready:
            raise DnsServiceError("DNS_MANAGEMENT_UNAVAILABLE")

    def build_hooks(self):
        self._guard()
        # Les hooks recontrôlent les faits ; aucun lancement PA/PZT/DNS.
        return {"configure": self._guard, "start": self._guard}

    def require_execution(self, **kwargs):
        # Aucun port d'exécution qualifié n'est sélectionné dans cette composition.
        raise DnsServiceError("DNS_EXECUTION_UNAVAILABLE")

    def verify_observation(self, **kwargs):
        raise DnsServiceError("DNS_OBSERVATION_UNVERIFIED")

    def execution_status(self):
        return {
            "selection": "NOT_SELECTED", "service_state": "DISABLED",
            "applied_revision": None, "applied_present": None,
            "application_status": "UNKNOWN", "measurement_status": "UNMEASURED",
        }
