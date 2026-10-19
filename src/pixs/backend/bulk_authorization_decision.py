"""Vocabulaire passif des décisions d’autorité Bulk AuthorityAssessmentV1.

Ne décide ni ne résout une autorité, ne fournit aucun contexte ou droit,
aucune conversion, transition, persistance, I/O ni exécution. Les contrats
et validateurs existants conservent leurs chaînes exactes.
"""

from enum import Enum


class BulkAuthorizationDecision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    UNAVAILABLE = "UNAVAILABLE"


__all__ = ["BulkAuthorizationDecision"]
