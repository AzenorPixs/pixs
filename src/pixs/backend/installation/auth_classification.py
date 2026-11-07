"""Pont C10 vers les métadonnées réelles de l'autorisation R01 chez Auth.

Il ne publie ni politique ni autorisation. Les baux et sources de confiance
sont ouverts par la composition protégée, séparément du lecteur.
"""
from __future__ import annotations

import os
import threading

from pixs.auth.bootstrap_metadata import (
    BootstrapAuthorizationMetadata, BootstrapAuthorizationMetadataReader)
from pixs.auth.contracts import AuthDataClassification
from pixs.backend.c10_catalog import C10Catalog, CatalogInvalid, _Lease
from pixs.core.dto import BootstrapActInput
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext, ScopeType

__all__ = ["C10BootstrapAuthClassificationSource"]


class C10BootstrapAuthClassificationSource:
    def __init__(self, *, using: str, act: BootstrapActInput,
                 reader: BootstrapAuthorizationMetadataReader,
                 metadata_lease: _Lease) -> None:
        if (type(using) is not str or not using
                or type(act) is not BootstrapActInput
                or type(reader) is not BootstrapAuthorizationMetadataReader
                or getattr(reader, "binding", None) != (using, act)
                or type(metadata_lease) is not _Lease
                or type(metadata_lease.owner) is not C10Catalog
                or act.context != ScopeContext(ScopeType.PLATFORM)):
            raise CorePortError()
        self._using, self._act, self._reader = using, act, reader
        self._metadata = metadata_lease
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._pin = None
        self._profile()

    def _profile(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()
        try:
            entry = self._metadata.profile()
        except CatalogInvalid:
            raise CorePortError() from None
        binding = self._metadata.owner.config.binding
        if (entry.profile.owner_component != "pixs.auth"
                or binding.owner_component != "pixs.auth"
                or entry.profile.data_asset_id != binding.data_asset_id):
            raise CorePortError()
        pin = (entry.publication_ref, entry.catalog_version, entry.raw_sha256,
               entry.published_version, binding.profile_ref, entry.profile)
        if self._pin is None:
            self._pin = pin
        elif self._pin != pin:
            raise CorePortError()
        return entry

    def resolve(self, *, context: ScopeContext, alias: str,
                operation_id: str) -> AuthDataClassification:
        if (type(context) is not ScopeContext or context != self._act.context
                or type(alias) is not str or alias != self._using
                or type(operation_id) is not str or operation_id != self._act.operation_id):
            raise CorePortError()
        entry = self._profile()
        metadata = self._reader.read(context=context, alias=alias, operation_id=operation_id)
        if type(metadata) is not BootstrapAuthorizationMetadata:
            raise CorePortError()
        metadata.__post_init__()
        expected = AuthDataClassification(entry.profile.data_asset_id,
                                          entry.profile.confidentiality,
                                          entry.profile.personal_data)
        expected.values()
        if (metadata.owner_component != entry.profile.owner_component
                or metadata.context != context
                or metadata.resource_ref not in entry.resource_refs
                or metadata.classification != expected):
            raise CorePortError()
        if self._profile() != entry:
            raise CorePortError()
        return expected
