"""Chargeur en lecture d’une source de fanions PostgreSQL versionnée."""

from __future__ import annotations

from typing import NoReturn

from pixs.backend.feature_flag_snapshot_codec import (
    FeatureFlagSnapshotCodecError,
    decode_feature_flag_source_snapshot,
)
from pixs.kernel.feature_flag_sources import FeatureFlagSourceSnapshot

__all__ = [
    "FeatureFlagSourceLoadError",
    "load_feature_flag_source_snapshot",
]


class FeatureFlagSourceLoadError(ValueError):
    """Refus fermé sans écho de la source ni de l’entrée."""

    def __init__(self) -> None:
        super().__init__("Source de fanions indisponible")


def _refuser_source() -> NoReturn:
    raise FeatureFlagSourceLoadError() from None


def load_feature_flag_source_snapshot(
    expected_configuration_version: str,
) -> FeatureFlagSourceSnapshot:
    if type(expected_configuration_version) is not str or not expected_configuration_version:
        _refuser_source()

    from django.db.utils import DatabaseError
    from pixs.backend.models import FeatureFlagSourceSnapshotRecord

    try:
        record = FeatureFlagSourceSnapshotRecord.objects.get(
            pk=expected_configuration_version
        )
        if (
            type(record.configuration_version) is not str
            or record.configuration_version != expected_configuration_version
        ):
            _refuser_source()

        snapshot = decode_feature_flag_source_snapshot(record.snapshot)
    except (
        FeatureFlagSourceSnapshotRecord.DoesNotExist,
        DatabaseError,
        FeatureFlagSnapshotCodecError,
    ):
        _refuser_source()

    if (
        type(snapshot) is not FeatureFlagSourceSnapshot
        or snapshot.configuration_version != expected_configuration_version
    ):
        _refuser_source()

    return snapshot
