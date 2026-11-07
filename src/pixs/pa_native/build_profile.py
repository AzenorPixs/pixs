"""Profil natif PA01 fermé, indépendant du manifest PBO.

Cette validation décrit une composition. Elle ne prouve ni compilation,
ni confiance de l'artefact, ni autorisation d'exécuter une opération.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Mapping

from pixs.kernel.manifest.semver import parse_version

__all__ = ["BuildProfile", "Executable", "Operation", "ProfileError", "check_compiled_catalogue", "parse_profile"]

_ROLES = MappingProxyType({
    "pixs-pa-system": ("pixs.agent", ("system-daemon",)),
    "pixs-pa-events": ("pixs.agent", ("system-start", "system-stop")),
    "pixs-pa-session": ("pixs.agent", ("session-start", "session-stop", "session-daemon")),
    "pzt": ("pixs.pzt", ("pzt-daemon",)),
})
_CATALOGUE = MappingProxyType({
    "inspect_postgresql": "Protégé",
    "prepare_postgresql": "Critique",
    "get_postgresql_result": "Protégé",
})
_SHA256 = re.compile(r"[0-9a-f]{64}")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
# Verrou public PEP 440 normalisé, final ou .postN ; jamais une préversion.
_CYTHON_LOCK = re.compile(
    r"(?:[1-9][0-9]*!)?(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*))*"
    r"(?:\.post(?:0|[1-9][0-9]*))?"
)


class ProfileError(ValueError):
    """Profil invalide ; diagnostic structurel sans restitution des valeurs."""


@dataclass(frozen=True, slots=True)
class Executable:
    name: str
    owner: str
    modes: tuple[str, ...]
    source: str


@dataclass(frozen=True, slots=True)
class Operation:
    name: str
    version: str
    owner: str
    mode: str
    criticality: str
    contract: str
    source: str


@dataclass(frozen=True, slots=True)
class BuildProfile:
    schema_version: str
    profile_version: str
    executables: tuple[Executable, ...]
    operations: tuple[Operation, ...]
    dependencies: tuple[tuple[str, str, str, str, str], ...]
    cython_version: str


def _table(value: object, keys: set[str], field: str) -> dict:
    if type(value) is not dict or set(value) != keys:
        raise ProfileError(field + " : champs obligatoires manquants ou inconnus")
    return value


def _text(value: object, field: str) -> str:
    if type(value) is not str or not value or any(ord(c) < 32 for c in value):
        raise ProfileError(field + " : texte non vide attendu")
    return value


def _version(value: object, field: str) -> str:
    value = _text(value, field)
    try:
        parse_version(value)
    except ValueError as error:
        raise ProfileError(field + " : version SemVer invalide") from error
    return value


def _path(value: object, field: str) -> str:
    value = _text(value, field)
    parts = value.split("/")
    if "\\" in value or PurePosixPath(value).is_absolute() or any(p in ("", ".", "..") for p in parts):
        raise ProfileError(field + " : chemin relatif canonique requis")
    return value


def _list(value: object, field: str) -> list:
    if type(value) is not list:
        raise ProfileError(field + " : liste attendue")
    return value


def parse_profile(text: str) -> BuildProfile:
    """Valide le seul profil Debian 13 x86_64 adopté, sans effet système.

    Les dépendances fournies restent des déclarations : leur présence,
    empreinte, licence et fermeture doivent être contrôlées au build.
    Aucun catalogue, source ou plugin n'est découvert au runtime.
    """
    if type(text) is not str:
        raise ProfileError("profil : texte TOML attendu")
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise ProfileError("profil : syntaxe TOML invalide") from error
    _table(data, {"schema_version", "profile_version", "target", "toolchain",
                  "layout", "executables", "operations", "dependencies"}, "profil")
    if data["schema_version"] != "1.0.0":
        raise ProfileError("schema_version : version incompatible")
    profile_version = _version(data["profile_version"], "profile_version")
    target = _table(data["target"], {"os", "release", "arch", "environments"}, "target")
    if target != {"os": "debian", "release": "13", "arch": "x86_64",
                  "environments": ["physical", "vm", "docker"]}:
        raise ProfileError("target : cible hors du profil adopté")
    toolchain = _table(data["toolchain"], {"cpython", "cython", "gil", "soabi", "linkage"}, "toolchain")
    cython_version = _text(toolchain["cython"], "toolchain.cython")
    if _CYTHON_LOCK.fullmatch(cython_version) is None:
        raise ProfileError("toolchain.cython : version stable exacte normalisée requise")
    fixed_toolchain = {key: value for key, value in toolchain.items() if key != "cython"}
    if fixed_toolchain != {"cpython": "3.14.9", "gil": True,
                           "soabi": "cpython-314-x86_64-linux-gnu", "linkage": "static"} or type(toolchain["gil"]) is not bool:
        raise ProfileError("toolchain : chaîne différente de D1/D7")
    layout = _table(data["layout"], {"bin", "runtime", "lib"}, "layout")
    if layout != {"bin": "bin", "runtime": "runtime", "lib": "lib"}:
        raise ProfileError("layout : arborescence différente de D5")

    executables = []
    names = set()
    for raw in _list(data["executables"], "executables"):
        item = _table(raw, {"name", "owner", "modes", "source"}, "executable")
        name = _text(item["name"], "executable.name")
        if name not in _ROLES or name in names:
            raise ProfileError("executable : nom inconnu ou doublon")
        owner, modes = _ROLES[name]
        if item["owner"] != owner or item["modes"] != list(modes):
            raise ProfileError("executable : propriétaire ou modes incompatibles")
        source = _path(item["source"], "executable.source")
        names.add(name)
        executables.append(Executable(name, owner, modes, source))
    if names != set(_ROLES):
        raise ProfileError("executables : quatre exécutables requis")

    operations = []
    names = set()
    for raw in _list(data["operations"], "operations"):
        item = _table(raw, {"name", "version", "owner", "mode", "criticality", "contract", "source"}, "operation")
        name = _text(item["name"], "operation.name")
        if name not in _CATALOGUE or name in names:
            raise ProfileError("operation : nom absent du catalogue adopté ou doublon")
        if (_version(item["version"], "operation.version") != "1.0.0"
                or item["owner"] != "pixs.agent"
                or item["mode"] != "system-daemon"
                or item["criticality"] != _CATALOGUE[name]):
            raise ProfileError("operation : version, propriétaire, mode ou classe incompatible")
        contract = _text(item["contract"], "operation.contract")
        if _IDENTIFIER.fullmatch(contract) is None or contract != "pixs.agent.postgresql." + name:
            raise ProfileError("operation.contract : identifiant invalide")
        source = _path(item["source"], "operation.source")
        names.add(name)
        operations.append(Operation(name, "1.0.0", "pixs.agent", "system-daemon",
                                    _CATALOGUE[name], contract, source))
    if names != set(_CATALOGUE):
        raise ProfileError("operations : trois opérations du catalogue adopté requises")

    dependencies = []
    names = set()
    for raw in _list(data["dependencies"], "dependencies"):
        item = _table(raw, {"name", "version", "provenance", "license", "sha256"}, "dependency")
        name = _text(item["name"], "dependency.name")
        if name in names:
            raise ProfileError("dependency : nom en doublon")
        version = _text(item["version"], "dependency.version")
        provenance = _text(item["provenance"], "dependency.provenance")
        license_id = _text(item["license"], "dependency.license")
        fingerprint = _text(item["sha256"], "dependency.sha256")
        if _SHA256.fullmatch(fingerprint) is None:
            raise ProfileError("dependency : empreinte SHA256 invalide")
        names.add(name)
        dependencies.append((name, version, provenance, license_id, fingerprint))
    if not dependencies:
        raise ProfileError("dependencies : inventaire explicite requis")
    return BuildProfile("1.0.0", profile_version, tuple(sorted(executables, key=lambda e: e.name)),
                        tuple(sorted(operations, key=lambda o: o.name)), tuple(sorted(dependencies)),
                        cython_version)


def check_compiled_catalogue(profile: BuildProfile, compiled: Mapping[str, Operation]) -> None:
    """Compare le registre issu des objets compilés ; aucune découverte.

    L'appelant de build doit dériver compiled des objets réellement produits.
    Lui fournir le profil lui-même ne constitue pas une preuve de livraison.
    """
    expected = {operation.name: operation for operation in profile.operations}
    if not isinstance(compiled, Mapping) or dict(compiled) != expected:
        raise ProfileError("registre : opération absente, supplémentaire ou incompatible")
