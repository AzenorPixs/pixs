"""Repository interne insert/get de l'identité d'admission, sans mutation."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from pixs.backend.bulk_admission_identity_record import (
    BulkAdmissionIdentityRecord,
)

__all__ = [
    "AdmissionIdentityConstraintRefused",
    "BulkAdmissionIdentityRepository",
]

_VARIANTS = frozenset({"IMPORT", "EXPORT"})


class AdmissionIdentityConstraintRefused(Exception):
    """Contrainte persistante refusée, message statique sans écho."""


def _is_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


class BulkAdmissionIdentityRepository:
    """Insert/get seuls, internes, sans update ni purge ni autorité."""

    def __init__(self, using: str = "default") -> None:
        if not _is_text(using):
            raise ValidationError("alias de base invalide", code="bulk_admission_identity_alias_invalid")
        self._using = using

    def insert_identity(self, *, values: object) -> None:
        """Valide avant ORM puis insère en force_insert dans un atomic imbriquable."""
        record = BulkAdmissionIdentityRecord.from_values(values)
        try:
            with transaction.atomic(using=self._using):
                record.save(force_insert=True, using=self._using)
        except IntegrityError as exc:
            raise AdmissionIdentityConstraintRefused(
                "contrainte persistante d'identité d'admission refusée"
            ) from exc

    def get_identity(
        self,
        *,
        resolved_tenant_id: object,
        resolved_subject_id: object,
        bulk_type: object,
        idempotency_key: object,
    ) -> dict | None:
        """Valide les 4 composants avant query, rend une copie owned ou None."""
        candidates = (
            resolved_tenant_id,
            resolved_subject_id,
            bulk_type,
            idempotency_key,
        )
        if any(not _is_text(value) for value in candidates):
            raise ValidationError(
                "clé d'identité d'admission invalide",
                code="bulk_admission_identity_key_invalid",
            )
        if bulk_type not in _VARIANTS:
            raise ValidationError(
                "clé d'identité d'admission invalide",
                code="bulk_admission_identity_key_invalid",
            )
        try:
            found = BulkAdmissionIdentityRecord.objects.using(self._using).get(
                resolved_tenant_id=resolved_tenant_id,
                resolved_subject_id=resolved_subject_id,
                bulk_type=bulk_type,
                idempotency_key=idempotency_key,
            )
        except BulkAdmissionIdentityRecord.DoesNotExist:
            return None
        return found.as_values()
