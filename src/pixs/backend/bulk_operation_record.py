"""Socle préparatoire Django BulkOperationRecord v1, sans exécution métier."""

from django.core.exceptions import ValidationError
from django.db import models

from pixs.kernel.bulk_operation_record_values import (
    validate_bulk_operation_record_values,
)
from pixs.kernel.bulk_operations import (
    BulkCommitMode,
    BulkConflictStrategy,
    BulkOperationState,
    BulkOperationVariant,
    BulkReferenceFormat,
)

__all__ = ["BulkOperationRecord"]

_FIELDS = (
    "operation_id", "bulk_type", "bulk_version", "status",
    "tenant_context_reference", "scope_context_reference", "format",
    "conflict_strategy", "commit_mode",
)
_INVALID = "valeurs de persistance bulk invalides"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_operation_record_invalid")


class BulkOperationRecord(models.Model):
    """Neuf colonnes préparatoires, références opaques et validation explicite.

    from_values ne sauvegarde pas. full_clean contrôle les types avant toute
    conversion ; save conserve le comportement Django sans validation implicite.
    Les contraintes SQL ne prouvent ni SemVer, type Python exact ou autorisation.
    """

    operation_id = models.TextField(primary_key=True, serialize=False)
    bulk_type = models.TextField(
        choices=[(item.value, item.value) for item in BulkOperationVariant],
    )
    bulk_version = models.TextField()
    status = models.TextField(
        choices=[(item.value, item.value) for item in BulkOperationState],
    )
    tenant_context_reference = models.TextField()
    scope_context_reference = models.TextField(blank=True, null=True)
    format = models.TextField(
        choices=[(item.value, item.value) for item in BulkReferenceFormat],
    )
    conflict_strategy = models.TextField(
        blank=True, null=True,
        choices=[(item.value, item.value) for item in BulkConflictStrategy],
    )
    commit_mode = models.TextField(
        blank=True, null=True,
        choices=[(item.value, item.value) for item in BulkCommitMode],
    )

    @classmethod
    def from_values(cls, values: object) -> "BulkOperationRecord":
        """Construit sans DB depuis un snapshot du dict explicite validé."""
        if type(values) is not dict:
            raise _invalid()
        snapshot = values.copy()
        if validate_bulk_operation_record_values(snapshot):
            raise _invalid()
        return cls(**snapshot)

    def full_clean(
        self, exclude=None, validate_unique=True, validate_constraints=True,
    ):
        values = {name: getattr(self, name) for name in _FIELDS}
        if validate_bulk_operation_record_values(values):
            raise _invalid()
        try:
            return super().full_clean(
                exclude=exclude,
                validate_unique=validate_unique,
                validate_constraints=validate_constraints,
            )
        except ValidationError:
            raise _invalid() from None

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="bulkrecord_operation_id_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(bulk_version=""),
                name="bulkrecord_version_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(tenant_context_reference=""),
                name="bulkrecord_tenant_ref_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(scope_context_reference__isnull=True)
                | ~models.Q(scope_context_reference=""),
                name="bulkrecord_scope_ref_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    bulk_type__in=[item.value for item in BulkOperationVariant],
                ),
                name="bulkrecord_type_member",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[item.value for item in BulkOperationState],
                ),
                name="bulkrecord_status_member",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    format__in=[item.value for item in BulkReferenceFormat],
                ),
                name="bulkrecord_format_member",
            ),
            models.CheckConstraint(
                condition=models.Q(conflict_strategy__isnull=True)
                | models.Q(
                    conflict_strategy__in=[
                        item.value for item in BulkConflictStrategy
                    ],
                ),
                name="bulkrecord_conflict_member",
            ),
            models.CheckConstraint(
                condition=models.Q(commit_mode__isnull=True)
                | models.Q(
                    commit_mode__in=[item.value for item in BulkCommitMode],
                ),
                name="bulkrecord_commit_member",
            ),
        ]
