"""Decideur runtime C04 : Root distinct, ordinaire partage, sans audit reel.

Chaque instance est liee a Request exacte, alias du store et operation_id.
Source C03 proprietaire injectee, jamais DTO client. Preparation Core avant
tout appel C03, sous vraie TX PG. Ordinaire via _prepare_detailed reel avec
conversion AUDIT vers Obligation. UNGRANTED refuse meme si ACL ALLOW.
PERMITTED branche racine sans seuils ordinaires, assurances preservees.
Derogations backend seulement pour PERMITTED, liees a Decision reellement
emise. Aucun audit reel ici : ALLOW ne confirme ni acces ni commit.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass

from django.db import connections, transaction

from pixs.core.authz.decision import Decision, _prepare_detailed
from pixs.core.authz.policy import Effect, Obligation, PolicyError
from pixs.core.authz.ports import (
    AuthenticationContext,
    PortError,
    Request,
    RevocationStatus,
    TrustedFacts,
)
from pixs.core.scope.context import validate_structure, ScopeStructureError
from pixs.core.scope.ownership import ResourceOwnership, OwnershipError
from pixs.core.services_common import CoreServiceError

__all__ = ["RuntimeWaiverRequest", "RuntimeAuthorizationDecider"]


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeWaiverRequest:
    """Demande backend explicite, liee a Request, alias et operation."""

    request: Request
    alias: str
    operation_id: str
    audit: bool
    governance: bool

    def __post_init__(self) -> None:
        if type(object.__getattribute__(self, "request")) is not Request:
            raise PortError()
        for name in ("alias", "operation_id"):
            value = object.__getattribute__(self, name)
            if type(value) is not str or value == "":
                raise PortError()
        for name in ("audit", "governance"):
            value = object.__getattribute__(self, name)
            if type(value) is not bool:
                raise PortError()


class _FixedProvider:
    def __init__(self, facts: TrustedFacts) -> None:
        self._facts = facts

    def resolve(self, request: Request) -> TrustedFacts:
        return self._facts


class RuntimeAuthorizationDecider:
    """Decideur lie : store + source C03 + horloge + requete + operation."""

    def __init__(self, *, store, facts_provider, clock, request: Request, operation_id: str, waiver_request=None) -> None:
        from pixs.core.services_runtime_store import CoreAuthorizationStore

        if type(store) is not CoreAuthorizationStore:
            raise PortError()
        if not callable(getattr(facts_provider, "resolve", None)):
            raise PortError()
        if not callable(getattr(clock, "now", None)):
            raise PortError()
        if type(request) is not Request:
            raise PortError()
        try:
            request.__post_init__()
            validate_structure(request.context)
        except (PortError, ScopeStructureError):
            raise PortError() from None
        if type(operation_id) is not str or operation_id == "":
            raise PortError()
        if waiver_request is not None and type(waiver_request) is not RuntimeWaiverRequest:
            raise PortError()
        if waiver_request is not None:
            if waiver_request.request != request:
                raise PortError()
            if waiver_request.alias != store.alias:
                raise PortError()
            if waiver_request.operation_id != operation_id:
                raise PortError()
        self._store = store
        self._provider = facts_provider
        self._clock = clock
        self._request = request
        self._operation_id = operation_id
        self._waiver = waiver_request
        self._receipts: dict = {}
        self._prepared = None

    def _check_binding(self, request: Request, alias: str, operation_id: str) -> None:
        if type(request) is not Request or request != self._request:
            raise PortError()
        if (request.resource_id not in self._store.catalog.resource_ids
                or request.action_id not in self._store.catalog.action_ids):
            raise PortError()
        if type(alias) is not str or alias != self._store.alias:
            raise PortError()
        if type(operation_id) is not str or operation_id != self._operation_id:
            raise PortError()

    def prepare_core_under_locks(self, request: Request, alias: str, operation_id: str):
        """Exige vraie TX PG et epingle snapshot avant tout appel C03."""
        self._check_binding(request, alias, operation_id)
        snapshot, topology, pin, epoch, state = self._store.pinned_snapshot(
            context=request.context, actor_ref=request.subject_id
        )
        self._prepared = (snapshot, topology, pin, epoch, state)
        return self._prepared

    def _now(self):
        try:
            now = self._clock.now()
        except Exception:
            raise PortError() from None
        if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
            raise PortError()
        return now

    def _deny(self, request: Request, version, now) -> Decision:
        return Decision(request.decision_id, Effect.DENY, "DENIED", version, (), now, now)

    def _verify_root_facts(self, facts: TrustedFacts, request: Request, now: datetime.datetime) -> None:
        if type(facts) is not TrustedFacts:
            raise PortError()
        try:
            facts.__post_init__()
            object.__getattribute__(facts, "auth").__post_init__()
            object.__getattribute__(facts, "ownership").__post_init__()
            validate_structure(facts.context)
        except (PortError, OwnershipError, ScopeStructureError):
            raise PortError() from None
        auth = object.__getattribute__(facts, "auth")
        own = object.__getattribute__(facts, "ownership")
        if type(auth) is not AuthenticationContext or type(own) is not ResourceOwnership:
            raise PortError()
        if object.__getattribute__(facts, "subject_id") != request.subject_id:
            raise PortError()
        if object.__getattribute__(auth, "digital_identity_id") != request.subject_id:
            raise PortError()
        if object.__getattribute__(facts, "resource_id") != request.resource_id:
            raise PortError()
        if object.__getattribute__(own, "resource_id") != request.resource_id:
            raise PortError()
        if object.__getattribute__(facts, "action_id") != request.action_id:
            raise PortError()
        if object.__getattribute__(facts, "context") != request.context:
            raise PortError()
        if object.__getattribute__(auth, "context") != request.context:
            raise PortError()
        if object.__getattribute__(own, "context") != request.context:
            raise PortError()
        if object.__getattribute__(facts, "revocation_status") is not RevocationStatus.ACTIVE:
            raise PortError()
        auth_time = object.__getattribute__(auth, "authentication_time")
        auth_exp = object.__getattribute__(auth, "expires_at")
        if not (type(auth_time) is datetime.datetime and auth_time.tzinfo is datetime.timezone.utc):
            raise PortError()
        if not (type(auth_exp) is datetime.datetime and auth_exp.tzinfo is datetime.timezone.utc):
            raise PortError()
        if not (auth_time <= now < auth_exp):
            raise PortError()

    def _decide_locked(self, request: Request, alias: str, operation_id: str) -> Decision:
        snapshot, topology, pin, epoch, state = self.prepare_core_under_locks(request, alias, operation_id)
        try:
            facts = self._provider.resolve(request)
        except Exception:
            raise PortError() from None
        now = self._now()
        if state == "UNGRANTED":
            decision = self._deny(request, snapshot.version, now)
            self._receipts[(request.decision_id, alias, operation_id)] = {
                "decision": decision, "pin": pin, "state": state, "version": snapshot.version,
                "physical": connections[alias].connection, "savepoints": tuple(connections[alias].savepoint_ids),
                "authenticated_at": facts.auth.authentication_time if type(facts) is TrustedFacts and type(facts.auth) is AuthenticationContext else None,
            }
            return decision
        if state == "PERMITTED":
            try:
                self._verify_root_facts(facts, request, now)
            except PortError:
                decision = self._deny(request, snapshot.version, now)
                self._receipts[(request.decision_id, alias, operation_id)] = {
                    "decision": decision, "pin": pin, "state": state, "version": snapshot.version,
                "physical": connections[alias].connection, "savepoints": tuple(connections[alias].savepoint_ids),
                "authenticated_at": facts.auth.authentication_time if type(facts) is TrustedFacts and type(facts.auth) is AuthenticationContext else None,
                }
                return decision
            auth = object.__getattribute__(facts, "auth")
            auth_exp = object.__getattribute__(auth, "expires_at")
            ttl = self._store.limits.ttl_seconds
            candidate = now + datetime.timedelta(seconds=ttl)
            expires = auth_exp if auth_exp < candidate else candidate
            if not (now < expires):
                decision = self._deny(request, snapshot.version, now)
                self._receipts[(request.decision_id, alias, operation_id)] = {
                    "decision": decision, "pin": pin, "state": state, "version": snapshot.version,
                "physical": connections[alias].connection, "savepoints": tuple(connections[alias].savepoint_ids),
                "authenticated_at": facts.auth.authentication_time if type(facts) is TrustedFacts and type(facts.auth) is AuthenticationContext else None,
                }
                return decision
            decision = Decision(request.decision_id, Effect.ALLOW, "ALLOWED", snapshot.version, (), now, expires)
            self._receipts[(request.decision_id, alias, operation_id)] = {
                "decision": decision, "pin": pin, "state": state, "version": snapshot.version,
                "physical": connections[alias].connection, "savepoints": tuple(connections[alias].savepoint_ids),
                "authenticated_at": facts.auth.authentication_time if type(facts) is TrustedFacts and type(facts.auth) is AuthenticationContext else None,
            }
            return decision
        fixed = _FixedProvider(facts)
        try:
            prepared, status, _view = _prepare_detailed(request, snapshot, fixed, self._clock, topology)
        except Exception:
            raise PortError() from None
        if status != "ALLOW":
            decision = self._deny(request, snapshot.version, prepared.evaluated_at)
            self._receipts[(request.decision_id, alias, operation_id)] = {
                "decision": decision, "pin": pin, "state": state, "version": snapshot.version,
                "physical": connections[alias].connection, "savepoints": tuple(connections[alias].savepoint_ids),
                "authenticated_at": facts.auth.authentication_time if type(facts) is TrustedFacts and type(facts.auth) is AuthenticationContext else None,
            }
            return decision
        try:
            converted = tuple(
                Obligation(kind=o) if type(o) is str else o
                for o in object.__getattribute__(prepared, "obligations")
            )
            for obligation in converted:
                if type(obligation) is not Obligation or obligation.kind != "AUDIT":
                    raise PortError()
        except Exception:
            raise PortError() from None
        decision = Decision(
            object.__getattribute__(prepared, "decision_id"),
            object.__getattribute__(prepared, "effect"),
            object.__getattribute__(prepared, "reason_code"),
            object.__getattribute__(prepared, "policy_version"),
            converted,
            object.__getattribute__(prepared, "evaluated_at"),
            object.__getattribute__(prepared, "expires_at"),
        )
        self._receipts[(request.decision_id, alias, operation_id)] = {
            "decision": decision, "pin": pin, "state": state, "version": snapshot.version,
                "physical": connections[alias].connection, "savepoints": tuple(connections[alias].savepoint_ids),
                "authenticated_at": facts.auth.authentication_time if type(facts) is TrustedFacts and type(facts.auth) is AuthenticationContext else None,
        }
        return decision

    def revalidate_under_locks(self, request: Request, *, alias: str, operation_id: str) -> Decision:
        return self._decide_locked(request, alias, operation_id)

    def decide(self, request: Request) -> Decision:
        self._check_binding(request, self._store.alias, self._operation_id)
        if connections[self._store.alias].in_atomic_block:
            return self._decide_locked(request, self._store.alias, self._operation_id)
        with transaction.atomic(using=self._store.alias):
            return self._decide_locked(request, self._store.alias, self._operation_id)

    def _waiver_allows(self, request: Request, decision: Decision, *, alias: str, operation_id: str, kind: str) -> bool:
        try:
            self._check_binding(request, alias, operation_id)
        except PortError:
            return False
        if type(decision) is not Decision or decision.effect is not Effect.ALLOW:
            return False
        receipt = self._receipts.get((request.decision_id, alias, operation_id))
        if receipt is None or receipt["decision"] is not decision:
            return False
        waiver = self._waiver
        if (receipt["state"] != "PERMITTED" or waiver is None
                or waiver.request != request or waiver.alias != alias
                or waiver.operation_id != operation_id):
            return False
        if kind not in ("audit", "governance") or getattr(waiver, kind) is not True:
            return False
        if decision.policy_version != receipt["version"]:
            return False
        # Une lecture fraîche hors TX ne dispense que le refus sans effet existant.
        # Dans la TX propriétaire, le reçu doit provenir de cette même identité SQL.
        outer = connections[alias].in_atomic_block
        if outer:
            return self._fresh_waiver(request, decision, receipt, alias, operation_id, True)
        with transaction.atomic(using=alias):
            return self._fresh_waiver(request, decision, receipt, alias, operation_id, False)

    def _fresh_waiver(self, request, decision, receipt, alias, operation_id, require_same_pin):
        try:
            snapshot, _topology, pin, _epoch, state = self.prepare_core_under_locks(
                request, alias, operation_id)
            if state != "PERMITTED" or snapshot.version != decision.policy_version:
                return False
            if require_same_pin and pin != receipt["pin"]:
                return False
            now = self._now()
            if not (type(decision.evaluated_at) is datetime.datetime
                    and decision.evaluated_at.tzinfo is datetime.timezone.utc
                    and type(decision.expires_at) is datetime.datetime
                    and decision.expires_at.tzinfo is datetime.timezone.utc
                    and decision.evaluated_at <= now < decision.expires_at):
                return False
            # Recontrôle C03 après préparation Core ; aucun reçu DTO n'établit sa fraîcheur.
            facts = self._provider.resolve(request)
            self._verify_root_facts(facts, request, now)
        except (PortError, CoreServiceError):
            return False
        return True

    def audit_waived(self, request: Request, decision: Decision, *, alias: str, operation_id: str) -> bool:
        return self._waiver_allows(request, decision, alias=alias, operation_id=operation_id, kind="audit")

    def governance_waived(self, request: Request, decision: Decision, *, alias: str, operation_id: str) -> bool:
        return self._waiver_allows(request, decision, alias=alias, operation_id=operation_id, kind="governance")


    def verify_final_transition(self, request: Request, decision: Decision, *,
                                alias: str, operation_id: str, transition_verifier) -> None:
        """Contrôle final d'une transition Auth déjà autorisée, jamais un nouvel accès."""
        from pixs.core.services_authorization_guard import transaction_identity

        actions = (
            "pixs.auth.session.renew", "pixs.auth.session.logout",
            "pixs.auth.session.revoke", "pixs.auth.session.revoke_all",
            "pixs.auth.credential.change", "pixs.auth.credential.recover",
        )
        self._check_binding(request, alias, operation_id)
        if request.action_id not in actions or type(decision) is not Decision:
            raise PortError()
        receipt = self._receipts.get((request.decision_id, alias, operation_id))
        if (receipt is None or receipt["decision"] is not decision
                or decision.effect is not Effect.ALLOW
                or decision.decision_id != request.decision_id
                or decision.policy_version != receipt["version"]):
            raise PortError()
        connection = connections[alias]
        current = transaction_identity(alias)
        if (current != receipt["pin"] or connection.connection is not receipt["physical"]
                or tuple(connection.savepoint_ids) != receipt["savepoints"]):
            raise PortError()
        now = self._now()
        if not (type(decision.evaluated_at) is datetime.datetime
                and decision.evaluated_at.tzinfo is datetime.timezone.utc
                and type(decision.expires_at) is datetime.datetime
                and decision.expires_at.tzinfo is datetime.timezone.utc
                and decision.evaluated_at <= now < decision.expires_at):
            raise PortError()
        snapshot, _topology, pin, _epoch, state = self.prepare_core_under_locks(
            request, alias, operation_id)
        if (pin != receipt["pin"] or snapshot.version != receipt["version"]
                or state != receipt["state"]):
            raise PortError()
        verify = getattr(transition_verifier, "verify_final_transition", None)
        if not callable(verify):
            raise PortError()
        # Le propriétaire Auth contrôle ses versions et lignes attendues dans cette TX.
        # Un None confirme seulement ces contrôles, pas le commit ni une authentification.
        if verify(request, decision, alias=alias, operation_id=operation_id) is not None:
            raise PortError()
        if (transaction_identity(alias) != receipt["pin"]
                or connection.connection is not receipt["physical"]
                or tuple(connection.savepoint_ids) != receipt["savepoints"]
                or not decision.evaluated_at <= self._now() < decision.expires_at):
            raise PortError()
        return None


    def verify_auth_freshness(self, request: Request, decision: Decision, *, alias: str,
                              operation_id: str, authenticated_at, max_age_seconds) -> None:
        """Vérifie un seuil Auth configuré ; aucune assurance ni date n'est inventée."""
        from pixs.core.services_authorization_guard import transaction_identity

        self._check_binding(request, alias, operation_id)
        if (type(decision) is not Decision or decision.effect is not Effect.ALLOW
                or type(max_age_seconds) is not int or max_age_seconds <= 0):
            raise PortError()
        receipt = self._receipts.get((request.decision_id, alias, operation_id))
        if (receipt is None or receipt["decision"] is not decision
                or type(authenticated_at) is not datetime.datetime
                or authenticated_at.tzinfo is not datetime.timezone.utc
                or authenticated_at != receipt["authenticated_at"]):
            raise PortError()
        connection = connections[alias]
        if (transaction_identity(alias) != receipt["pin"]
                or connection.connection is not receipt["physical"]
                or tuple(connection.savepoint_ids) != receipt["savepoints"]):
            raise PortError()
        now = self._now()
        if not decision.evaluated_at <= now < decision.expires_at:
            raise PortError()
        snapshot, _topology, pin, _epoch, state = self.prepare_core_under_locks(
            request, alias, operation_id)
        if (pin != receipt["pin"] or snapshot.version != receipt["version"]
                or state != receipt["state"] or decision.policy_version != receipt["version"]):
            raise PortError()
        age = (now - authenticated_at).total_seconds()
        if age < 0 or (state != "PERMITTED" and age >= max_age_seconds):
            raise PortError()
        return None
