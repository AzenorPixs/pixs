"""Vocabulaire des genres de cohérence d'export BulkExportConsistencyKind.

Représentation seule des deux valeurs canoniques B12 et ExportManifestV1,
sans validation métier, persistance, résolution, transition ou branchement runtime.
"""

from enum import Enum


class BulkExportConsistencyKind(Enum):
    """Deux genres distincts, sans conversion implicite en chaîne."""

    SNAPSHOT = "SNAPSHOT"
    WATERMARK = "WATERMARK"


__all__ = ["BulkExportConsistencyKind"]
