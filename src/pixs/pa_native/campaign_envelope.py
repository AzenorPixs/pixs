"""Enveloppe de campagne PA01, structure pure S1.

Validation de la forme TOML fermee v1, sans entree-sortie, sans reseau,
sans environnement, sans processus et sans compilation. Aucune preuve
S2 ni raccord S3. L'unicite historique, la preuve officielle et les
liens symboliques ne sont ni verifies ni affirmes ici.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from datetime import date, time
from pathlib import PurePosixPath
from typing import Any, Mapping
from urllib.parse import urlsplit

from pixs.pa_native.build_profile import ProfileError, _CYTHON_LOCK as _PROFILE_CYTHON_LOCK

__all__ = [
    "CampaignEnvelope",
    "CampaignEnvelopeError",
    "CampaignIdentity",
    "Distribution",
    "SelectionProof",
    "ToolchainLock",
    "parse_envelope",
]

_CODE = "PA01_CAMPAIGN_METADATA_INVALID"
_SCHEMA = "1.0.0"
_COMPONENT = "pa01"
_SOURCE_URL = "https://pypi.org/pypi/Cython/json"
_ROOTS = frozenset({"schema_version", "campaign", "toolchain", "selection", "distributions"})
_CAMPAIGN_KEYS = frozenset({"id", "component"})
_TOOLCHAIN_KEYS = frozenset({"cython"})
_SELECTION_KEYS = frozenset({"verified_at", "source_url", "snapshot", "snapshot_sha256"})
_DISTRIBUTION_KEYS = frozenset({"filename", "url", "sha256"})
_SHA256 = re.compile(r"[0-9a-f]{64}")
_VERIFIED_AT = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]+))?Z")


class CampaignEnvelopeError(ProfileError):
    """Enveloppe invalide ; diagnostic structurel sans restitution des valeurs."""


@dataclass(frozen=True, slots=True)
class CampaignIdentity:
    id: str
    component: str


@dataclass(frozen=True, slots=True)
class ToolchainLock:
    cython: str


@dataclass(frozen=True, slots=True)
class SelectionProof:
    verified_at: str
    source_url: str
    snapshot: str
    snapshot_sha256: str


@dataclass(frozen=True, slots=True)
class Distribution:
    filename: str
    url: str
    sha256: str


@dataclass(frozen=True, slots=True)
class CampaignEnvelope:
    schema_version: str
    campaign: CampaignIdentity
    toolchain: ToolchainLock
    selection: SelectionProof
    distributions: tuple[Distribution, ...]


def _fail(detail: str) -> CampaignEnvelopeError:
    return CampaignEnvelopeError(_CODE + " : " + detail)


def _is_forbidden_control(value: str) -> bool:
    for c in value:
        o = ord(c)
        if o < 32 or 127 <= o <= 159 or 0xD800 <= o <= 0xDFFF:
            return True
    return False


def _text(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise _fail(field + " : texte non vide attendu") from None
    if _is_forbidden_control(value):
        raise _fail(field + " : texte non vide attendu") from None
    return value


def _closed_table(value: Any, keys: frozenset, field: str) -> Mapping[str, Any]:
    if type(value) is not dict or set(value) != set(keys):
        raise _fail(field + " : champs obligatoires manquants ou inconnus") from None
    return value


def _verified_at(value: Any) -> str:
    text = _text(value, "selection.verified_at")
    match = _VERIFIED_AT.fullmatch(text)
    if match is None:
        raise _fail("selection.verified_at : instant UTC textuel attendu") from None
    year = int(match.group(1))
    month = int(match.group(2))
    day = int(match.group(3))
    hour = int(match.group(4))
    minute = int(match.group(5))
    second = int(match.group(6))
    if year < 1 or year > 9999:
        raise _fail("selection.verified_at : instant UTC textuel attendu") from None
    try:
        date(year, month, day)
    except ValueError as error:
        raise _fail("selection.verified_at : instant UTC textuel attendu") from error
    try:
        time(hour, minute, second)
    except ValueError as error:
        raise _fail("selection.verified_at : instant UTC textuel attendu") from error
    return text


def _snapshot(value: Any) -> str:
    text = _text(value, "selection.snapshot")
    if "\\" in text:
        raise _fail("selection.snapshot : chemin relatif canonique requis") from None
    pure = PurePosixPath(text)
    if pure.is_absolute():
        raise _fail("selection.snapshot : chemin relatif canonique requis") from None
    parts = text.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise _fail("selection.snapshot : chemin relatif canonique requis") from None
    return text


def _filename(value: Any, field: str) -> str:
    text = _text(value, field)
    if "/" in text or "\\" in text:
        raise _fail(field + " : nom simple attendu") from None
    if text in (".", ".."):
        raise _fail(field + " : nom simple attendu") from None
    if PurePosixPath(text).is_absolute():
        raise _fail(field + " : nom simple attendu") from None
    return text


def _https_url(value: Any, field: str) -> str:
    text = _text(value, field)
    if any(c.isspace() for c in text) or "\\" in text:
        raise _fail(field + " : URL HTTPS attendue") from None
    try:
        parts = urlsplit(text)
    except ValueError:
        raise _fail(field + " : URL HTTPS attendue") from None
    if parts.scheme != "https":
        raise _fail(field + " : URL HTTPS attendue") from None
    if not parts.netloc or not parts.hostname:
        raise _fail(field + " : URL HTTPS attendue") from None
    if parts.username is not None or parts.password is not None:
        raise _fail(field + " : URL HTTPS attendue") from None
    if "@" in parts.netloc:
        raise _fail(field + " : URL HTTPS attendue") from None
    try:
        _port = parts.port
    except ValueError:
        raise _fail(field + " : URL HTTPS attendue") from None
    return text


def _sha256(value: Any, field: str) -> str:
    text = _text(value, field)
    if _SHA256.fullmatch(text) is None:
        raise _fail(field + " : SHA-256 hexadecimal attendu") from None
    return text


def _cython_lock(value: Any) -> str:
    text = _text(value, "toolchain.cython")
    if _PROFILE_CYTHON_LOCK.fullmatch(text) is None:
        raise _fail("toolchain.cython : version stable exacte normalisee requise") from None
    return text


def parse_envelope(text: str) -> CampaignEnvelope:
    """Valide une enveloppe de campagne v1 a partir de son texte TOML.

    Purement structurel : aucune entree-sortie, aucun acces reseau, aucune
    lecture d'environnement, aucun sous-processus, aucune compilation.
    """
    if type(text) is not str:
        raise _fail("enveloppe : texte TOML attendu") from None
    try:
        text.encode("utf-8", "strict")
    except UnicodeEncodeError as error:
        raise _fail("enveloppe : texte UTF-8 strict attendu") from error
    if "\r" in text:
        raise _fail("enveloppe : fins de ligne LF attendues") from None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise _fail("enveloppe : syntaxe TOML invalide") from error
    _closed_table(data, _ROOTS, "enveloppe")
    if data["schema_version"] != _SCHEMA:
        raise _fail("schema_version : version exacte 1.0.0 attendue") from None
    if type(data["schema_version"]) is not str:
        raise _fail("schema_version : version exacte 1.0.0 attendue") from None
    campaign_table = _closed_table(data["campaign"], _CAMPAIGN_KEYS, "campaign")
    campaign_id = _text(campaign_table["id"], "campaign.id")
    if campaign_table["component"] != _COMPONENT:
        raise _fail("campaign.component : valeur exacte pa01 attendue") from None
    toolchain_table = _closed_table(data["toolchain"], _TOOLCHAIN_KEYS, "toolchain")
    cython = _cython_lock(toolchain_table["cython"])
    selection_table = _closed_table(data["selection"], _SELECTION_KEYS, "selection")
    verified_at = _verified_at(selection_table["verified_at"])
    if selection_table["source_url"] != _SOURCE_URL:
        raise _fail("selection.source_url : source exacte attendue") from None
    snapshot = _snapshot(selection_table["snapshot"])
    snapshot_sha256 = _sha256(selection_table["snapshot_sha256"], "selection.snapshot_sha256")
    raw_distributions = data["distributions"]
    if type(raw_distributions) is not list or not raw_distributions:
        raise _fail("distributions : liste non vide attendue") from None
    seen: set[str] = set()
    distributions: list[Distribution] = []
    for item in raw_distributions:
        _closed_table(item, _DISTRIBUTION_KEYS, "distributions[]")
        filename = _filename(item["filename"], "distributions[].filename")
        if filename in seen:
            raise _fail("distributions[].filename : nom simple unique attendu") from None
        seen.add(filename)
        url = _https_url(item["url"], "distributions[].url")
        digest = _sha256(item["sha256"], "distributions[].sha256")
        distributions.append(Distribution(filename=filename, url=url, sha256=digest))
    return CampaignEnvelope(
        schema_version=_SCHEMA,
        campaign=CampaignIdentity(id=campaign_id, component=_COMPONENT),
        toolchain=ToolchainLock(cython=cython),
        selection=SelectionProof(
            verified_at=verified_at,
            source_url=_SOURCE_URL,
            snapshot=snapshot,
            snapshot_sha256=snapshot_sha256,
        ),
        distributions=tuple(distributions),
    )
