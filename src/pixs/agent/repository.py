"""Dépôt privé Agent : persistance transactionnelle tête/journal/faits, sans transport.

Périmètre 2.1c seul, testable sans service 2.1d. Consomme les types et validateurs 2.1a (AgentManagementInstruction, AgentManagementResult, AgentManagementState, AgentValidationContext, validate_agent_instruction, validate_agent_result, validate_agent_state) et les modèles écrits, plus ScopeContext public et identifiers Agent. Aucun import Core.persistence/Auth privé, aucune autorisation Core ni vérification crypto PZT revendiquée, aucun transport.

Sémantique : tête unique par scope/cible commune aux acteurs, verrouillée avant contrôle ; journal immuable par acteur avec expected_generation précondition et generation résultante (generation == expected_generation + 1) ; faits OBSERVED puis CONFIRMED lié au fait enregistré. Idempotence = scope/tenant/scope/cible/acteur/opération/version/clé ; traces request_operation_id/correlation/causation conservées et restituées, exclues du fingerprint métier. Rejeu identique retrouvé AVANT refus génération ancienne ; contenu divergent toujours refusé, comparaison intégrale après digest, collision refusée. Concurrence par contrainte unique + savepoint/relecture + select_for_update ; génération unique par tête, idem unique. Génération obsolète, borne int64 et erreurs stockage explicites fixes, rollback complet, aucun retour détaché avant commit. Transaction compatible audit externe : atomic sans durable imposé, rejoint la transaction englobante si présente, durabilité seulement au commit le plus externe. Aucune requête hors ScopeContext/cible. Confirmation seulement d'un vrai fait OBSERVED mêmes opération/tête/périmètre/génération, document identique recopié, contexte/preuve/postcondition validés par ports injectés (listes de Diagnostic, jamais booléen) ; une chaîne passée par l'appelant n'est pas une preuve.

Gouvernance inconnue conservée restrictive sans défaut PUBLIC ni durée arbitraire ; l'exposition future exigera politique vérifiée. Refus catalogue, mandats et bornes 2.1a appliqués via validateurs directs. Réponse perdue = souhaité durable + résultat unknown jusqu'à réconciliation, jamais réémission PZT.

Ports injectés, tous obligatoires et None interdit : mandate_trust_port(instruction, context), origin_trust_port(result, context), confirmation_trust_port(state, result, observed_fact_id, observed_source_ref, observed_origin_proof, postcondition_ref, context). Chacun retourne list/tuple de Diagnostic (vide = valide), jamais booléen ; seule l'exception attendue AgentTrustError est convertie en refus fixe, sans cause exposée.

Prérequis signalés, non inventés : appel direct des validateurs 2.1a aux signatures relues du source ; documents observés opaques conformément2.1a ; profil de gouvernance versionné du composant avant activation, que le dépôt n'établit pas.
"""
from __future__ import annotations
import json
from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError, InterfaceError, connections, transaction
from pixs.agent import models as m
from pixs.agent.contracts import AgentManagementInstruction, AgentManagementResult, AgentManagementState, AgentValidationContext, validate_agent_instruction, validate_agent_result, validate_agent_state
from pixs.agent.identifiers import AgentIdentifierError, canonical_head_identity, canonical_idempotence_identity, canonical_operation_content, canonical_params_text, content_digest, head_digest, idempotence_digest, new_agent_uuid7, require_agent_uuid7, require_canonical_instant, require_canonical_trace_list
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.diagnostics import Diagnostic
from django.utils.connection import ConnectionDoesNotExist
from django.utils import timezone
__all__ = ["AgentRepositoryError", "AgentTrustError", "append_observation", "confirm_observation", "persist_desired_instruction", "read_head", "read_history", "read_operation"]
FIXED_MESSAGE = "Dépôt Agent impossible."
TRUST_MESSAGE = "Vérification de confiance Agent impossible."
INT64_MAX = 9223372036854775807
class AgentRepositoryError(ValueError):
    def __init__(self, code="AGENT_REPOSITORY_IMPOSSIBLE"):
        super().__init__(FIXED_MESSAGE)
        self.code = code
        self.element = "agent_repository"
        self.step = "agent_persist"
class AgentTrustError(ValueError):
    def __init__(self, code="AGENT_TRUST_IMPOSSIBLE"):
        super().__init__(TRUST_MESSAGE)
        self.code = code
        self.element = "agent_trust"
        self.step = "agent_verify_trust"
def _fail(code):
    raise AgentRepositoryError(code) from None
def _clean_row(row):
    if row is not None:
        try:
            row.clean()
        except (ValidationError, AgentIdentifierError):
            _fail("DONNEE_CORROMPUE")
    return row
def _alias(using):
    if type(using) is not str or using == "":
        _fail("ALIAS_INVALIDE")
    try:
        connection = connections[using]
    except ConnectionDoesNotExist:
        _fail("ALIAS_INCONNU")
    if connection.vendor != "postgresql":
        _fail("MOTEUR_REFUSE")
    return using
def _scope_filter(scope, target_id):
    if type(scope) is not ScopeContext:
        _fail("SCOPE_INVALIDE")
    try:
        validate_structure(scope)
    except ScopeStructureError:
        _fail("SCOPE_INVALIDE")
    if type(target_id) is not str or target_id == "":
        _fail("CIBLE_INVALIDE")
    try:
        canonical_head_identity(scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id)
    except AgentIdentifierError:
        _fail("SCOPE_OU_CIBLE_INVALIDE")
    filt = {"scope_type": scope.scope_type.value, "target_id": target_id}
    if scope.tenant_id is None:
        filt["tenant_id__isnull"] = True
    else:
        filt["tenant_id"] = scope.tenant_id
    if scope.scope_id is None:
        filt["scope_id__isnull"] = True
    else:
        filt["scope_id"] = scope.scope_id
    return filt
def _call_trust_port(port, code, *args):
    if port is None:
        _fail("PORT_MANQUANT")
    if not callable(port):
        _fail("PORT_INVALIDE")
    try:
        outcome = port(*args)
    except AgentTrustError:
        _fail(code)
    if type(outcome) is bool or type(outcome) not in (list, tuple):
        _fail("AUTORITE_BOOLEENNE_REFUSEE")
    for item in outcome:
        if type(item) is not Diagnostic:
            _fail("DIAGNOSTIC_INVALIDE")
    if list(outcome):
        _fail(code)
    return []
def _params_dict(instruction):
    params = instruction.params
    if type(params) is not tuple:
        _fail("PARAMS_INVALIDES")
    mapping = {}
    for item in params:
        name = item.name
        kind = item.kind
        if type(name) is not str or name == "" or name in mapping:
            _fail("PARAMS_INVALIDES")
        if kind == "str":
            value = item.str_value
            if type(value) is not str or item.int_value is not None or item.bool_value is not None:
                _fail("PARAMS_INVALIDES")
        elif kind == "int":
            value = item.int_value
            if type(value) is not int or item.str_value is not None or item.bool_value is not None:
                _fail("PARAMS_INVALIDES")
        elif kind == "bool":
            value = item.bool_value
            if type(value) is not bool or item.str_value is not None or item.int_value is not None:
                _fail("PARAMS_INVALIDES")
        else:
            _fail("PARAMS_INVALIDES")
        mapping[name] = value
    return mapping
def _trace_canonical(ids):
    if type(ids) is not tuple:
        _fail("TRACE_INVALIDE")
    for item in ids:
        if type(item) is not str or item == "":
            _fail("TRACE_INVALIDE")
    try:
        text = json.dumps(list(ids), separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail("TRACE_INVALIDE")
    try:
        require_canonical_trace_list(text)
    except AgentIdentifierError:
        _fail("TRACE_INVALIDE")
    return text
def _stored_trace_tuple(canonical_text):
    try:
        require_canonical_trace_list(canonical_text)
        parsed = json.loads(canonical_text)
    except (ValueError, RecursionError):
        _fail("TRACE_CORROMPUE")
    if type(parsed) is not list:
        _fail("TRACE_CORROMPUE")
    return tuple(parsed)
def persist_desired_instruction(*, using, scope, target_id, instruction, context, allowed_catalog, mandate_trust_port):
    alias = _alias(using)
    filt_scope = _scope_filter(scope, target_id)
    if type(instruction) is not AgentManagementInstruction:
        _fail("INSTRUCTION_INVALIDE")
    if type(context) is not AgentValidationContext:
        _fail("CONTEXTE_INVALIDE")
    if type(allowed_catalog) is not tuple:
        _fail("CATALOGUE_INVALIDE")
    if context.expected_scope != scope or context.expected_target != target_id:
        _fail("LIAISON_CONTEXTE")
    diagnostics = validate_agent_instruction(instruction, allowed_catalog, context)
    if diagnostics:
        _fail("INSTRUCTION_REFUSEE")
    _call_trust_port(mandate_trust_port, "MANDAT_REFUSE", instruction, context)
    expected = instruction.expected_generation
    if type(expected) is not int or not 0 <= expected <= INT64_MAX - 1:
        _fail("GENERATION_MAX")
    try:
        mapping = _params_dict(instruction)
        params_canonical = canonical_params_text(mapping)
    except AgentIdentifierError:
        _fail("PARAMS_INVALIDES")
    try:
        identity_canonical = canonical_idempotence_identity(scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id, subject_id=instruction.initial_actor, operation_name=instruction.catalog_operation, operation_version=instruction.catalog_version, idempotency_key=instruction.idempotency_key)
        head_canonical = canonical_head_identity(scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id)
        content_canonical = canonical_operation_content(schema_version=instruction.schema_version, operation_name=instruction.catalog_operation, operation_version=instruction.catalog_version, subject_id=instruction.initial_actor, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id, expected_generation=expected, params_canonical=params_canonical, mandate_ref=instruction.mandate_ref, expires_at=instruction.expires_at, scope_type=scope.scope_type.value)
    except AgentIdentifierError:
        _fail("CANONIQUE_IMPOSSIBLE")
    identity_ref = idempotence_digest(identity_canonical)
    head_ref = head_digest(head_canonical)
    content_ref = content_digest(content_canonical)
    correlation_canonical = _trace_canonical(instruction.correlation_ids)
    causation_canonical = _trace_canonical(instruction.causation_ids)
    filt_head = dict(filt_scope)
    filt_head["head_digest"] = head_ref
    try:
        with transaction.atomic(using=alias):
            known = m.AgentOperation.objects.using(alias).filter(identity_digest=identity_ref, **filt_scope).first()
            if known is not None:
                _clean_row(known)
                if known.identity_canonical != identity_canonical:
                    _fail("COLLISION_IDENTITE")
                if known.content_canonical != content_canonical or known.content_digest != content_ref:
                    _fail("REJEU_DIVERGENT")
                return {"head": None, "operation": known, "replay": True, "request_operation_id": known.request_operation_id, "correlation_ids": _stored_trace_tuple(known.correlation_ids_canonical), "causation_ids": _stored_trace_tuple(known.causation_ids_canonical)}
            head = m.AgentHead.objects.using(alias).select_for_update().filter(**filt_head).first()
            if head is None:
                if expected != 0:
                    _fail("GENERATION_ECART")
                candidate = m.AgentHead(id=new_agent_uuid7(), scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id, current_generation=0, desired_entry=None, head_identity_canonical=head_canonical, head_digest=head_ref)
                try:
                    candidate.clean()
                except (ValidationError, AgentIdentifierError):
                    _fail("TETE_INVALIDE")
                try:
                    with transaction.atomic(using=alias):
                        candidate.save(using=alias)
                except IntegrityError:
                    head = m.AgentHead.objects.using(alias).select_for_update().filter(**filt_head).first()
                    if head is None:
                        _fail("STOCKAGE_INDISPONIBLE")
                else:
                    head = m.AgentHead.objects.using(alias).select_for_update().filter(**filt_head).first()
                    if head is None:
                        _fail("RELECTURE_DIVERGENTE")
            _clean_row(head)
            if head.head_identity_canonical != head_canonical:
                _fail("COLLISION_IDENTITE")
            known = m.AgentOperation.objects.using(alias).filter(identity_digest=identity_ref, **filt_scope).first()
            if known is not None:
                _clean_row(known)
                if known.identity_canonical != identity_canonical:
                    _fail("COLLISION_IDENTITE")
                if known.content_canonical != content_canonical or known.content_digest != content_ref:
                    _fail("REJEU_DIVERGENT")
                return {"head": head, "operation": known, "replay": True, "request_operation_id": known.request_operation_id, "correlation_ids": _stored_trace_tuple(known.correlation_ids_canonical), "causation_ids": _stored_trace_tuple(known.causation_ids_canonical)}
            if expected != head.current_generation:
                if expected < head.current_generation:
                    _fail("GENERATION_OBSOLETE")
                _fail("GENERATION_ECART")
            resulting = expected + 1
            operation = m.AgentOperation(id=new_agent_uuid7(), scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id, subject_id=instruction.initial_actor, operation_name=instruction.catalog_operation, operation_version=instruction.catalog_version, idempotency_key=instruction.idempotency_key, expected_generation=expected, generation=resulting, head_digest=head_ref, schema_version=instruction.schema_version, params_canonical=params_canonical, mandate_ref=instruction.mandate_ref, expires_at=instruction.expires_at, request_operation_id=instruction.operation_id, correlation_ids_canonical=correlation_canonical, causation_ids_canonical=causation_canonical, identity_canonical=identity_canonical, identity_digest=identity_ref, content_canonical=content_canonical, content_digest=content_ref)
            try:
                operation.clean()
            except (ValidationError, AgentIdentifierError):
                _fail("OPERATION_INVALIDE")
            try:
                with transaction.atomic(using=alias):
                    operation.save(using=alias)
            except IntegrityError:
                rival = m.AgentOperation.objects.using(alias).filter(identity_digest=identity_ref, **filt_scope).first()
                if rival is not None:
                    _clean_row(rival)
                    if rival.identity_canonical != identity_canonical:
                        _fail("COLLISION_IDENTITE")
                    if rival.content_canonical != content_canonical or rival.content_digest != content_ref:
                        _fail("REJEU_DIVERGENT")
                    return {"head": head, "operation": rival, "replay": True, "request_operation_id": rival.request_operation_id, "correlation_ids": _stored_trace_tuple(rival.correlation_ids_canonical), "causation_ids": _stored_trace_tuple(rival.causation_ids_canonical)}
                occupant = m.AgentOperation.objects.using(alias).filter(head_digest=head_ref, generation=resulting, **filt_scope).first()
                if occupant is not None:
                    _fail("GENERATION_OCCUPEE")
                _fail("STOCKAGE_INDISPONIBLE")
            head.current_generation = resulting
            head.desired_entry = operation
            head.version += 1
            head.updated_at = timezone.now()
            try:
                head.clean()
            except (ValidationError, AgentIdentifierError):
                _fail("TETE_INVALIDE")
            head.save(using=alias)
            stored = m.AgentOperation.objects.using(alias).filter(pk=operation.pk, **filt_scope).first()
            if stored is None or stored.identity_digest != identity_ref or stored.content_digest != content_ref:
                _fail("RELECTURE_DIVERGENTE")
            _clean_row(stored)
            return {"head": head, "operation": stored, "replay": False, "request_operation_id": stored.request_operation_id, "correlation_ids": _stored_trace_tuple(stored.correlation_ids_canonical), "causation_ids": _stored_trace_tuple(stored.causation_ids_canonical)}
    except (DatabaseError, InterfaceError):
        raise AgentRepositoryError("STOCKAGE_INDISPONIBLE") from None
def read_head(*, using, scope, target_id):
    alias = _alias(using)
    filt_scope = _scope_filter(scope, target_id)
    try:
        head = _clean_row(m.AgentHead.objects.using(alias).filter(**filt_scope).first())
        if head is None:
            return None
        if head.current_generation == 0:
            if head.desired_entry_id is not None:
                _fail("DONNEE_CORROMPUE")
        else:
            operation = m.AgentOperation.objects.using(alias).filter(pk=head.desired_entry_id, generation=head.current_generation, head_digest=head.head_digest, **filt_scope).first()
            if operation is None:
                _fail("DONNEE_CORROMPUE")
            _clean_row(operation)
        return head
    except (DatabaseError, InterfaceError):
        raise AgentRepositoryError("LECTURE_IMPOSSIBLE") from None
def read_operation(*, using, scope, target_id, identity_digest):
    alias = _alias(using)
    filt_scope = _scope_filter(scope, target_id)
    if type(identity_digest) is not str or len(identity_digest) != 64 or any(c not in "0123456789abcdef" for c in identity_digest):
        _fail("IDENTITE_INVALIDE")
    try:
        return _clean_row(m.AgentOperation.objects.using(alias).filter(identity_digest=identity_digest, **filt_scope).first())
    except (DatabaseError, InterfaceError):
        raise AgentRepositoryError("LECTURE_IMPOSSIBLE") from None
def append_observation(*, using, scope, target_id, result, context, observed_document, observed_at, source_ref, origin_trust_port):
    alias = _alias(using)
    filt_scope = _scope_filter(scope, target_id)
    if type(result) is not AgentManagementResult:
        _fail("RESULTAT_INVALIDE")
    if type(context) is not AgentValidationContext:
        _fail("CONTEXTE_INVALIDE")
    if context.expected_scope != scope or context.expected_target != target_id:
        _fail("LIAISON_CONTEXTE")
    if type(result.generation) is not int or not 1 <= result.generation <= INT64_MAX:
        _fail("GENERATION_MAX")
    diagnostics = validate_agent_result(result, context)
    if diagnostics:
        _fail("RESULTAT_REFUSE")
    _call_trust_port(origin_trust_port, "ORIGINE_REFUSEE", result, context)
    if observed_document is None:
        if observed_at is not None:
            _fail("DOCUMENT_INCOHERENT")
    else:
        if type(observed_document) is not str or observed_document == "":
            _fail("DOCUMENT_INVALIDE")
        if len(observed_document) > context.max_doc_len:
            _fail("DOCUMENT_TROP_LONG")
        try:
            require_canonical_instant(observed_at)
        except AgentIdentifierError:
            _fail("DOCUMENT_INVALIDE")
    if type(source_ref) is not str or source_ref == "" or len(source_ref) > context.max_id_len:
        _fail("SOURCE_INVALIDE")
    try:
        with transaction.atomic(using=alias):
            operation = m.AgentOperation.objects.using(alias).select_for_update().filter(generation=result.generation, **filt_scope).first()
            if operation is None:
                _fail("OPERATION_INTROUVABLE")
            _clean_row(operation)
            if operation.request_operation_id != result.operation_id:
                _fail("LIAISON_TRACE_DIVERGENTE")
            if _stored_trace_tuple(operation.correlation_ids_canonical) != result.correlation_ids:
                _fail("LIAISON_CORRELATION_DIVERGENTE")
            state = AgentManagementState(operation_id=operation.request_operation_id, pa_target=target_id, generation=operation.generation, scope_context=scope, desired_doc=operation.content_canonical, observed_doc=observed_document, observed_at=observed_at, last_known_doc=None, last_known_at=None, confirmation_proof=None)
            if validate_agent_state(state, context):
                _fail("ETAT_REFUSE")
            fact = m.AgentFact(id=new_agent_uuid7(), scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id, operation=operation, observed_fact=None, generation=result.generation, kind="OBSERVED", outcome=result.outcome, occurred_at=result.occurred_at, observed_at=observed_at, origin_proof=result.origin_proof, observed_document=observed_document, source_ref=source_ref, proof_ref=None, postcondition_ref=None)
            try:
                fact.clean()
            except (ValidationError, AgentIdentifierError):
                _fail("FAIT_INVALIDE")
            fact.save(using=alias)
            return m.AgentFact.objects.using(alias).filter(pk=fact.pk, **filt_scope).first()
    except (DatabaseError, InterfaceError):
        raise AgentRepositoryError("STOCKAGE_INDISPONIBLE") from None
def confirm_observation(*, using, scope, target_id, observed_fact_id, proof_ref, postcondition_ref, result, context, confirmation_trust_port):
    alias = _alias(using)
    filt_scope = _scope_filter(scope, target_id)
    if type(result) is not AgentManagementResult:
        _fail("RESULTAT_INVALIDE")
    if type(context) is not AgentValidationContext:
        _fail("CONTEXTE_INVALIDE")
    if type(result.generation) is not int or not 1 <= result.generation <= INT64_MAX:
        _fail("GENERATION_MAX")
    try:
        require_agent_uuid7(observed_fact_id)
    except AgentIdentifierError:
        _fail("FAIT_IDENTIFIANT_INVALIDE")
    if result.outcome != "confirmed":
        _fail("RESULTAT_NON_CONFIRME")
    if type(proof_ref) is not str or proof_ref == "":
        _fail("PREUVE_INVALIDE")
    if type(postcondition_ref) is not str or postcondition_ref == "" or len(postcondition_ref) > context.max_id_len:
        _fail("PREUVE_INVALIDE")
    if context.expected_scope != scope or context.expected_target != target_id:
        _fail("LIAISON_CONTEXTE")
    try:
        with transaction.atomic(using=alias):
            observed = m.AgentFact.objects.using(alias).select_for_update().filter(pk=observed_fact_id, kind="OBSERVED", **filt_scope).first()
            if observed is None:
                _fail("FAIT_INTROUVABLE")
            _clean_row(observed)
            if observed.observed_document is None:
                _fail("CONFIRMATION_SANS_OBSERVE")
            operation = m.AgentOperation.objects.using(alias).select_for_update().filter(pk=observed.operation_id, **filt_scope).first()
            if operation is None:
                _fail("OPERATION_INTROUVABLE")
            _clean_row(operation)
            if observed.generation != operation.generation or observed.target_id != target_id:
                _fail("LIAISON_FAIT_DIVERGENTE")
            state = AgentManagementState(operation_id=operation.request_operation_id, pa_target=target_id, generation=operation.generation, scope_context=scope, desired_doc=operation.content_canonical, observed_doc=observed.observed_document, observed_at=observed.observed_at, last_known_doc=None, last_known_at=None, confirmation_proof=proof_ref)
            diagnostics = validate_agent_state(state, context)
            if diagnostics:
                _fail("ETAT_REFUSE")
            diagnostics = validate_agent_result(result, context)
            if diagnostics:
                _fail("RESULTAT_REFUSE")
            if result.operation_id != operation.request_operation_id or result.generation != operation.generation:
                _fail("LIAISON_RESULTAT_DIVERGENTE")
            if _stored_trace_tuple(operation.correlation_ids_canonical) != result.correlation_ids:
                _fail("LIAISON_CORRELATION_DIVERGENTE")
            _call_trust_port(confirmation_trust_port, "CONFIANCE_REFUSEE", state, result, observed.id, observed.source_ref, observed.origin_proof, postcondition_ref, context)
            fact = m.AgentFact(id=new_agent_uuid7(), scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target_id, operation=operation, observed_fact=observed, generation=operation.generation, kind="CONFIRMED", outcome="confirmed", occurred_at=result.occurred_at, observed_at=observed.observed_at, origin_proof=result.origin_proof, observed_document=observed.observed_document, source_ref=observed.source_ref, proof_ref=proof_ref, postcondition_ref=postcondition_ref)
            try:
                fact.clean()
            except (ValidationError, AgentIdentifierError):
                _fail("FAIT_INVALIDE")
            fact.save(using=alias)
            return m.AgentFact.objects.using(alias).filter(pk=fact.pk, **filt_scope).first()
    except (DatabaseError, InterfaceError):
        raise AgentRepositoryError("STOCKAGE_INDISPONIBLE") from None
def read_history(*, using, scope, target_id, limit):
    alias = _alias(using)
    filt_scope = _scope_filter(scope, target_id)
    if type(limit) is not int or limit < 1:
        _fail("LIMITE_INVALIDE")
    try:
        operations = list(m.AgentOperation.objects.using(alias).filter(**filt_scope).order_by("-generation", "-id")[:limit])
        facts = list(m.AgentFact.objects.using(alias).filter(**filt_scope).order_by("-generation", "-id")[:limit])
        for operation in operations:
            _clean_row(operation)
        for fact in facts:
            _clean_row(fact)
            operation = m.AgentOperation.objects.using(alias).filter(pk=fact.operation_id, generation=fact.generation, **filt_scope).first()
            if operation is None:
                _fail("DONNEE_CORROMPUE")
            _clean_row(operation)
            if fact.kind == "CONFIRMED":
                observed = m.AgentFact.objects.using(alias).filter(pk=fact.observed_fact_id, operation_id=fact.operation_id, generation=fact.generation, kind="OBSERVED", **filt_scope).first()
                if observed is None:
                    _fail("DONNEE_CORROMPUE")
                _clean_row(observed)
                if observed.observed_document != fact.observed_document or observed.observed_at != fact.observed_at or observed.source_ref != fact.source_ref:
                    _fail("DONNEE_CORROMPUE")
    except (DatabaseError, InterfaceError):
        raise AgentRepositoryError("LECTURE_IMPOSSIBLE") from None
    generations = [operation.generation for operation in operations]
    return {"operations": operations, "facts": facts, "latest_generation": max(generations) if generations else None}
