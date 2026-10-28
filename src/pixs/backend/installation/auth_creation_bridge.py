"""Métadonnées C10 de création pour une réservation réellement émise par Auth.

Le descripteur reste une intention : ce pont ne déclare aucune ligne existante,
ne publie pas d'autorisation et ne remplace pas le contrôle cryptographique.
"""
from __future__ import annotations

import os
import threading

from pixs.auth.bootstrap_session import (
    AuthBootstrapSession, BootstrapDraft, PlannedBootstrapResource)
from pixs.auth.contracts import AuthDataClassification
from pixs.auth.identifiers import require_uuid7, AuthIdentifierError
from pixs.backend.c10_catalog import C10Catalog, CatalogInvalid, _Lease
from pixs.core.ports import CorePortError

__all__ = ["C10AuthCreationBridge"]


class C10AuthCreationBridge:
    def __init__(self, *, using: str, session: AuthBootstrapSession,
                 draft: BootstrapDraft, metadata_lease: _Lease):
        if (type(using) is not str or not using
                or type(session) is not AuthBootstrapSession
                or type(draft) is not BootstrapDraft or session.using != using
                or type(metadata_lease) is not _Lease
                or type(metadata_lease.owner) is not C10Catalog):
            raise CorePortError()
        self._using, self._session, self._draft = using, session, draft
        self._metadata = metadata_lease
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._target = None
        self._pin = None
        self._profile()
        self._describe()

    @property
    def binding(self):
        return self._using, self._session, self._draft

    def _guard(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()

    def _describe(self):
        self._guard()
        target = self._session.describe(self._draft)
        if (type(target) is not PlannedBootstrapResource
                or target.kind != "CREATION_INTENT" or target.owner_component != "pixs.auth"
                or target.resource_ref != "pixs.auth.bootstrap:" + str(target.pk)
                or target.pk != self._draft.pk
                or target.operation_id != self._draft.operation_id
                or target.installation_ref != self._draft.installation_ref
                or target.target_identity_ref != self._draft.target_identity_ref):
            raise CorePortError()
        try:
            require_uuid7(target.pk)
        except AuthIdentifierError:
            raise CorePortError() from None
        if self._target is None:
            self._target = target
        elif self._target != target:
            raise CorePortError()
        return target

    def _profile(self):
        self._guard()
        try:
            entry = self._metadata.profile()
        except CatalogInvalid:
            raise CorePortError() from None
        binding = self._metadata.owner.config.binding
        if (entry.profile.owner_component != "pixs.auth"
                or binding.owner_component != "pixs.auth"
                or binding.data_asset_id != entry.profile.data_asset_id):
            raise CorePortError()
        pin = (entry.publication_ref, entry.catalog_version, entry.raw_sha256,
               entry.published_version, binding.profile_ref, entry.profile)
        if self._pin is None:
            self._pin = pin
        elif self._pin != pin:
            raise CorePortError()
        return entry

    def expected_for(self, draft: BootstrapDraft, *, alias: str,
                     operation_id: str) -> AuthDataClassification:
        self._guard()
        if (draft is not self._draft or type(alias) is not str or alias != self._using
                or type(operation_id) is not str or operation_id != self._draft.operation_id):
            raise CorePortError()
        target, entry = self._describe(), self._profile()
        if target.resource_ref not in entry.resource_refs:
            raise CorePortError()
        result = AuthDataClassification(entry.profile.data_asset_id,
                                        entry.profile.confidentiality,
                                        entry.profile.personal_data)
        result.values()
        if self._describe() != target or self._profile() != entry:
            raise CorePortError()
        return result
