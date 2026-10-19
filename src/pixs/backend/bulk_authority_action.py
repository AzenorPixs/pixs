"""Actions d’autorité Bulk v1 : représentation structurelle seule.

Ne réalise aucun contrôle d’autorisation, admission, exécution, annulation,
accès au résultat, persistance ou branchement runtime.
"""

from enum import Enum


class BulkAuthorityAction(Enum):
    ADMIT = "ADMIT"
    EXECUTE = "EXECUTE"
    CANCEL = "CANCEL"
    READ_RESULT = "READ_RESULT"


__all__ = ["BulkAuthorityAction"]
