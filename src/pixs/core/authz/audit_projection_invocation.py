"""Invocation bornée du port audit v1 : acquittement observé seul.

invoke_audit_projection valide la projection sur le même objet avant tout
accès au port, transmet une seule fois le decision_event original par
identité à sink.record, puis constate uniquement le retour observé.
Seul True exact donne True. Une exception ordinaire d'accès ou d'appel
au port donne False sans écho ni relance. Une exception inattendue du
validateur et une interruption dérivée directement de BaseException se
propagent. Aucune horloge, ressource, déduplication, mutation, persistance
ni branchement implicite dans authorize ou plan_filter.
"""

from __future__ import annotations

from pixs.core.authz.audit_decision_projection import (
    validate_audit_decision_projection,
)
from pixs.core.authz.ports import AuditSink

__all__ = ["invoke_audit_projection"]


def invoke_audit_projection(projection: object, sink: AuditSink) -> bool:
    """Invoquer le port fourni après validation préalable, sans autre effet."""
    diagnostics = validate_audit_decision_projection(projection)
    if diagnostics:
        return False
    decision = object.__getattribute__(projection, "decision_event")
    try:
        result = sink.record(decision)
    except Exception:
        return False
    return result is True
