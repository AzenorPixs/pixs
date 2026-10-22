"""Base abstraite Core : champs communs seuls, sans dépendance nouvelle."""
from __future__ import annotations

from django.db import models
from django.utils import timezone

from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState

# Regex UUIDv7 canonique minuscule, centralisée et réutilisée par les modèles.
# Contrainte réelle à valider sur PG16 : lookup regex sur UUID casté en texte par l'ORM.
UUID7_RE = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"


class CoreBase(models.Model):
    """Abstraite : version CAS, horodatage UTC fourni par le Clock propriétaire, gouvernance restrictive."""

    version = models.IntegerField(default=1)
    # default=timezone.now : la valeur du Clock propriétaire est acceptée ;
    # auto_now/auto_now_add interdits car ils écraseraient cette valeur.
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    governance_ref = models.TextField(null=True, blank=True, default=None)
    confidentiality = models.TextField(null=True, blank=True, default=None)
    personal = models.TextField(null=True, blank=True, default=None)
    persistence_state = models.TextField(default=DataPersistenceState.ACTIVE.value)
    retention_state = models.TextField(default=DataRetentionState.RETAINED.value)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(condition=models.Q(version__gte=1), name="%(class)s_ver_gte1"),
            models.CheckConstraint(
                condition=models.Q(governance_ref__isnull=True) | ~models.Q(governance_ref=""),
                name="%(class)s_govref_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(persistence_state__in=[s.value for s in DataPersistenceState]),
                name="%(class)s_pers_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(retention_state__in=[s.value for s in DataRetentionState]),
                name="%(class)s_reten_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(confidentiality__isnull=True)
                | models.Q(confidentiality__in=[c.value for c in ConfidentialityLevel]),
                name="%(class)s_conf_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(personal__isnull=True)
                | models.Q(personal__in=[p.value for p in PersonalDataLevel]),
                name="%(class)s_persdata_vocab",
            ),
        ]

    # Aucun save() imposant full_clean : les services appellent full_clean()
    # explicitement sous verrou ; la DB reste le dernier ressort.
