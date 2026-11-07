"""Syntaxe des noms souhaités : aucun générateur de nom PA ni accès DNS.

Le profil de saisie utilise des labels ASCII lettre/chiffre/tiret. La
qualification de clients et la dérivation du nom technique A06i restent
distinctes. L'original reste stocké ; la clé ne sert qu'à comparer/réserver.
"""
from __future__ import annotations
import re

_LABEL = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\Z")


def dns_name_key(value):
    if type(value) is not str or not value or "\x00" in value:
        raise ValueError("Nom DNS souhaité invalide.")
    name = value[:-1] if value.endswith(".") else value
    try:
        encoded = name.encode("ascii")
    except UnicodeError:
        raise ValueError("Profil de nom DNS souhaité non pris en charge.") from None
    labels = name.split(".")
    if (not encoded or any(_LABEL.fullmatch(label) is None for label in labels)
            or sum(len(label.encode("ascii")) + 1 for label in labels) + 1 > 255):
        raise ValueError("Nom DNS souhaité invalide.")
    return name.lower()


__all__ = ["dns_name_key"]
