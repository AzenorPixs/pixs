"""Composition Core HTTP : dépendances propriétaires explicites, sans activation serveur."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from pixs.auth.api_request_source import ApiRequestSource
from pixs.auth.facades import ApiAuthFacade, WebAuthFacade
from pixs.auth.services import PostgresLocalAuthService
from pixs.backend.api_core_catalog import ApiInputLimits, COMMANDS
from pixs.backend.api_core_errors_catalog import CoreApiError
from pixs.backend.api_core_pagination import CoreCursorCodec

__all__ = ["CoreHttpLimits", "CoreApiComposition"]


@dataclass(frozen=True, slots=True, repr=False)
class CoreHttpLimits:
    max_payload_bytes: int
    max_query_chars: int
    default_page_size: int
    max_page_size: int
    def __post_init__(self):
        for name in ("max_payload_bytes", "max_query_chars", "default_page_size", "max_page_size"):
            value = object.__getattribute__(self, name)
            if type(value) is not int or value < 1:
                raise ValueError("Limite HTTP Core invalide.")
        if self.default_page_size > self.max_page_size:
            raise ValueError("Limite HTTP Core invalide.")


@dataclass(frozen=True, slots=True, repr=False)
class CoreApiComposition:
    alias: str
    peer_alias: str
    request_source: ApiRequestSource
    auth_service: PostgresLocalAuthService
    core_ports_factory: object
    clock: object
    approved_host: str
    approved_origin: str
    limits: CoreHttpLimits
    input_limits: ApiInputLimits
    cursor_codec: CoreCursorCodec
    interactive_commands: frozenset[str]

    def __post_init__(self):
        for value in (self.alias, self.peer_alias, self.approved_host, self.approved_origin):
            if type(value) is not str or not value or chr(0) in value:
                raise ValueError("Composition HTTP Core invalide.")
        if self.alias == self.peer_alias:
            raise ValueError("Alias HTTP Core distincts requis.")
        origin = urlsplit(self.approved_origin)
        if (origin.scheme != "https" or origin.netloc != self.approved_host
                or origin.username is not None or origin.password is not None
                or origin.path or origin.query or origin.fragment):
            raise ValueError("Origine HTTPS Core invalide.")
        if type(self.request_source) is not ApiRequestSource or type(self.auth_service) is not PostgresLocalAuthService:
            raise ValueError("Propriétaire Auth explicite requis.")
        if not callable(self.core_ports_factory) or not callable(getattr(self.clock, "now", None)):
            raise ValueError("Ports HTTP Core manquants.")
        if (type(self.limits) is not CoreHttpLimits or type(self.input_limits) is not ApiInputLimits
                or type(self.cursor_codec) is not CoreCursorCodec):
            raise ValueError("Contrats HTTP Core invalides.")
        self.limits.__post_init__()
        self.input_limits.__post_init__()
        cursor = self.cursor_codec.config
        if (self.limits.max_page_size > cursor.max_page_size
                or self.input_limits.max_reference_chars > cursor.max_reference_chars
                or self.input_limits.max_collection_items > cursor.max_filter_refs):
            raise ValueError("Politiques HTTP et curseur contradictoires.")
        if (type(self.interactive_commands) is not frozenset
                or any(type(name) is not str or name not in COMMANDS for name in self.interactive_commands)):
            raise ValueError("Activités interactives serveur invalides.")

    def facades(self):
        return (
            ApiAuthFacade(service=self.auth_service, approved_host=self.approved_host,
                          approved_origin=self.approved_origin),
            WebAuthFacade(service=self.auth_service, approved_host=self.approved_host,
                          approved_origin=self.approved_origin, clock=self.clock),
        )

    def core_ports(self, *, request, operation_id, authentication_source):
        from pixs.auth.invocation import AuthInvocationSource
        from pixs.core.api_core_idempotency_repository import CoreApiIdempotencyRepository
        from pixs.core.audit_sink import PostgresAuditParticipant
        from pixs.core.authz.ports import Request
        from pixs.core.ports import CoreServicePorts
        from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
        from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider
        from pixs.core.services_runtime_filter import RuntimeSourceFilterProvider
        from pixs.core.services_runtime_declarations import RuntimeDeclarationValidator

        if type(request) is not Request or type(authentication_source) is not AuthInvocationSource:
            raise CoreApiError("SERVICE_UNAVAILABLE")
        ports = self.core_ports_factory(request=request, operation_id=operation_id,
                                        authentication_source=authentication_source)
        if type(ports) is not CoreServicePorts:
            raise CoreApiError("SERVICE_UNAVAILABLE")
        ports.__post_init__()
        if (type(ports.facts_provider) is not RuntimeTrustedFactsProvider
                or type(ports.decider) is not RuntimeAuthorizationDecider
                or type(ports.filter_provider) is not RuntimeSourceFilterProvider
                or type(ports.idempotence) is not CoreApiIdempotencyRepository
                or (ports.declarations is not None and type(ports.declarations) is not RuntimeDeclarationValidator)
                or (ports.audit is not None and type(ports.audit) is not PostgresAuditParticipant)):
            raise CoreApiError("SERVICE_UNAVAILABLE")
        return ports
