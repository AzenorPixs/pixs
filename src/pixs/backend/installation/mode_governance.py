"""Fournisseur C10 privé des modes, sans droit ni dispense.

Les deux gardes du catalogue protégé restent actives jusqu'au retour de
l'acte. Les reçus conservent les faits réels des profils modes et métadonnées.
Aucune purge ni fonctionnalité C10 globale n'est fournie ici.
"""
from __future__ import annotations

import hashlib
import os
import threading
from urllib.parse import quote

from pixs.backend.c10_catalog import CatalogInvalid, _Lease
from pixs.backend.c10_governance_adapter import (
    C10GovernanceAdapter, _bytes, _scope, _text,
)
from pixs.backend.installation.mode_commands import mode_action_ref
from pixs.backend.installation.mode_values import ModeOperationKind
from pixs.core.authz.ports import Clock, PortError, Request
from pixs.core.ports import CorePortError

__all__ = ["C10ModeGovernanceAdapter"]


class C10ModeGovernanceAdapter(C10GovernanceAdapter):
    """Profil modes backend et profil de métadonnées distincts, réellement publiés."""

    def __init__(self, *, using: str, installation_ref: str,
                 mode_lease: _Lease, metadata_lease: _Lease, clock: Clock) -> None:
        super().__init__(
            using=using, installation_ref=installation_ref,
            core_lease=mode_lease, metadata_lease=metadata_lease, clock=clock,
        )

    def _profiles(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()
        try:
            mode, metadata = self._core.profile(), self._metadata.profile()
        except CatalogInvalid:
            raise CorePortError() from None
        if (
            (mode.publication_ref, mode.catalog_version, mode.raw_sha256)
            != (metadata.publication_ref, metadata.catalog_version, metadata.raw_sha256)
            or mode.profile.owner_component != "pixs.backend"
            or mode.profile.data_asset_id == metadata.profile.data_asset_id
            or self._core.owner.config.binding.profile_ref
               == self._metadata.owner.config.binding.profile_ref
        ):
            raise CorePortError()
        return mode, metadata

    def _request(self, request, alias, operation, token):
        if type(request) is not Request:
            raise CorePortError()
        try:
            request.__post_init__()
        except PortError:
            raise CorePortError() from None
        _scope(request.context)
        for value in (
            operation, token, request.decision_id, request.subject_id,
            request.resource_id, request.action_id, request.correlation_id,
        ):
            _text(value, self._limit)
        try:
            expected_resource = (
                "pixs.backend.modes:" + quote(self._installation, safe="")
            )
        except (ValueError, UnicodeError):
            raise CorePortError() from None
        allowed = (
            mode_action_ref(ModeOperationKind.FINALIZE_CONFIGURATION),
            mode_action_ref(ModeOperationKind.ENTER_MAINTENANCE),
            mode_action_ref(ModeOperationKind.EXIT_MAINTENANCE),
        )
        if request.resource_id != expected_resource or request.action_id not in allowed:
            raise CorePortError()
        if self._operation is not None and self._operation != operation:
            raise CorePortError()
        native = self._native(alias)
        mode, metadata = self._profiles()
        if request.resource_id not in mode.resource_refs:
            raise CorePortError()
        digest = hashlib.sha256(_bytes([
            request.decision_id, request.subject_id, request.resource_id,
            request.action_id, "PLATFORM", request.correlation_id,
        ])).hexdigest()
        return native, mode, metadata, digest
