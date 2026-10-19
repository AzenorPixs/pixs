"""Paquet provider C01, reexport seul sans effet."""
from __future__ import annotations
from pixs.backend.systemd_secret_provider.provider import SecretBundle, resolve_secrets
__all__ = ["SecretBundle", "resolve_secrets"]
