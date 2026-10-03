"""Gabarit préparatoire backend Django hors base (fondation P0).

Exposition validée : `SettingsTemplate` immuable et
`build_settings_template`. Aucune lecture d'environnement, de fichier,
de réseau ou de Django. Aucune résolution de secret.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from pixs.kernel.config.resolution import SecretReference

__all__ = [
    "POSTGRES_ENGINE",
    "PROFILES",
    "SettingsTemplate",
    "build_settings_template",
]

POSTGRES_ENGINE = "django.db.backends.postgresql"

PROFILES = ("web", "worker", "scheduler")

_DATABASE_KEYS = frozenset({"name", "user", "host", "port"})


def _refus(message: str) -> ValueError:
    return ValueError(message)


def _exige_profil(profile: object) -> str:
    if not isinstance(profile, str):
        raise _refus("profil invalide : valeur attendue parmi les rôles déclarés")
    if profile not in PROFILES:
        raise _refus("profil invalide : valeur attendue parmi les rôles déclarés")
    return profile


def _exige_texte_non_vide(value: object, message: str) -> str:
    if not isinstance(value, str):
        raise _refus(message)
    if not value.strip():
        raise _refus(message)
    return value


def _exige_port(value: object) -> int:
    if isinstance(value, bool):
        raise _refus("port invalide : entier attendu dans l'intervalle déclaré")
    if not isinstance(value, int):
        raise _refus("port invalide : entier attendu dans l'intervalle déclaré")
    if value < 1 or value > 65535:
        raise _refus("port invalide : entier attendu dans l'intervalle déclaré")
    return value


def _exige_database(database: object) -> dict[str, Any]:
    if not isinstance(database, Mapping):
        raise _refus("configuration de base invalide")
    cles = set(database.keys())
    if cles != set(_DATABASE_KEYS):
        raise _refus("configuration de base invalide")
    nom = _exige_texte_non_vide(
        database["name"], "nom de base invalide"
    )
    utilisateur = _exige_texte_non_vide(
        database["user"], "utilisateur de base invalide"
    )
    hote = _exige_texte_non_vide(
        database["host"], "hôte de base invalide"
    )
    port = _exige_port(database["port"])
    return {"name": nom, "user": utilisateur, "host": hote, "port": port}


def _exige_allowed_hosts(allowed_hosts: object) -> tuple[str, ...]:
    if isinstance(allowed_hosts, (str, bytes, bytearray)):
        raise _refus("hôtes autorisés invalides")
    if not isinstance(allowed_hosts, Sequence):
        raise _refus("hôtes autorisés invalides")
    hotes = tuple(allowed_hosts)
    if not hotes:
        raise _refus("hôtes autorisés invalides")
    for hote in hotes:
        if not isinstance(hote, str):
            raise _refus("hôtes autorisés invalides")
        if hote != hote.strip():
            raise _refus("hôtes autorisés invalides")
        if not hote.strip():
            raise _refus("hôtes autorisés invalides")
        if "*" in hote:
            raise _refus("hôtes autorisés invalides")
        if hote.startswith("."):
            raise _refus("hôtes autorisés invalides")
    return hotes


def _exige_reference(reference: object, message: str) -> SecretReference:
    if not isinstance(reference, SecretReference):
        raise _refus(message)
    if not isinstance(reference.owner_id, str) or not reference.owner_id.strip():
        raise _refus(message)
    if not isinstance(reference.entry_id, str) or not reference.entry_id.strip():
        raise _refus(message)
    if not isinstance(reference.source, str) or not reference.source.strip():
        raise _refus(message)
    return reference


@dataclass(frozen=True)
class SettingsTemplate:
    """Gabarit immuable préparatoire, jamais prêt pour la production."""

    profile: str
    name: str
    user: str
    host: str
    port: int
    allowed_hosts: tuple[str, ...]
    secret_key_ref: SecretReference
    database_password_ref: SecretReference
    engine: str = field(default=POSTGRES_ENGINE, init=False)
    ready: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        _exige_profil(self.profile)
        _exige_texte_non_vide(self.name, "nom de base invalide")
        _exige_texte_non_vide(self.user, "utilisateur de base invalide")
        _exige_texte_non_vide(self.host, "hôte de base invalide")
        _exige_port(self.port)
        valides = _exige_allowed_hosts(self.allowed_hosts)
        object.__setattr__(self, "allowed_hosts", valides)
        _exige_reference(
            self.secret_key_ref, "référence de clé Django invalide"
        )
        _exige_reference(
            self.database_password_ref, "référence de mot de passe invalide"
        )
        if self.secret_key_ref == self.database_password_ref:
            raise _refus("références de secret distinctes attendues")
        object.__setattr__(self, "engine", POSTGRES_ENGINE)
        object.__setattr__(self, "ready", False)

    @property
    def non_secret_settings(self) -> dict[str, Any]:
        """Copie fraîche des seuls réglages Django non secrets.

        Insuffisante pour un démarrage : sans SECRET_KEY ni PASSWORD.
        """
        return {
            "ENGINE": POSTGRES_ENGINE,
            "DEBUG": False,
            "USE_TZ": True,
            "TIME_ZONE": "UTC",
            "INSTALLED_APPS": (),
            "ALLOWED_HOSTS": tuple(self.allowed_hosts),
            "DATABASES": {
                "default": {
                    "ENGINE": POSTGRES_ENGINE,
                    "NAME": self.name,
                    "USER": self.user,
                    "HOST": self.host,
                    "PORT": self.port,
                }
            },
        }


def build_settings_template(
    *,
    profile: object,
    database: object,
    allowed_hosts: object,
    secret_key_ref: object,
    database_password_ref: object,
) -> SettingsTemplate:
    """Construit un gabarit validé, sans effet externe."""
    profil = _exige_profil(profile)
    base = _exige_database(database)
    hotes = _exige_allowed_hosts(allowed_hosts)
    ref_cle = _exige_reference(
        secret_key_ref, "référence de clé Django invalide"
    )
    ref_mot_de_passe = _exige_reference(
        database_password_ref, "référence de mot de passe invalide"
    )
    if ref_cle == ref_mot_de_passe:
        raise _refus("références de secret distinctes attendues")
    return SettingsTemplate(
        profile=profil,
        name=base["name"],
        user=base["user"],
        host=base["host"],
        port=base["port"],
        allowed_hosts=hotes,
        secret_key_ref=ref_cle,
        database_password_ref=ref_mot_de_passe,
    )
