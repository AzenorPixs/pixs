"""Modeles identité minimale v1 : structure seule, sans effet applicatif."""

import uuid
from dataclasses import dataclass
from enum import Enum


class IdentityError(ValueError):
    """Erreur structurelle stable sans valeur brute."""

    def __init__(self):
        super().__init__("Identite minimale invalide.")
        self.code = "IDENTITY_INVALID"
        self.element = "identity"
        self.step = "validate_identity"


class IdentityType(Enum):
    """Categorie fonctionnelle fermee du profil v1."""

    HUMAN = "HUMAN"
    SERVICE = "SERVICE"
    DEVICE = "DEVICE"
    FEDERATED = "FEDERATED"


class IdentityState(Enum):
    """Etat structurel ferme du profil v1, sans transition definie."""

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


def _check_uuid(value):
    """Valide un UUIDv7 exact sans appel hostile."""
    if type(value) is not uuid.UUID:
        raise IdentityError()
    try:
        int_val = object.__getattribute__(value, "int")
    except Exception:
        raise IdentityError() from None
    if type(int_val) is not int:
        raise IdentityError()
    if not 0 <= int_val < 2 ** 128:
        raise IdentityError()
    try:
        version = object.__getattribute__(value, "version")
        variant = object.__getattribute__(value, "variant")
    except Exception:
        raise IdentityError() from None
    if version != 7:
        raise IdentityError()
    if variant != uuid.RFC_4122:
        raise IdentityError()
    return True


def _check_type(value):
    """Valide le type d'identite par identite stricte."""
    for member in IdentityType:
        if value is member:
            return True
    raise IdentityError()


def _check_state(value):
    """Valide l'etat d'identite par identite stricte."""
    for member in IdentityState:
        if value is member:
            return True
    raise IdentityError()


@dataclass(frozen=True, slots=True, repr=False)
class User:
    """Utilisateur minimal porte par son identifiant UUIDv7."""

    user_id: uuid.UUID

    def __post_init__(self):
        validate_user(self)


@dataclass(frozen=True, slots=True, repr=False)
class DigitalIdentity:
    """Identite numerique minimale, sans droit ni assurance deduits."""

    identity_id: uuid.UUID
    identity_type: IdentityType
    state: IdentityState

    def __post_init__(self):
        validate_identity(self)


@dataclass(frozen=True, slots=True, repr=False)
class IdentityLink:
    """Liaison explicite entre un utilisateur et une identite."""

    user_id: uuid.UUID
    identity_id: uuid.UUID

    def __post_init__(self):
        validate_link(self)


def validate_user(value):
    """Valide un User exact et son identifiant UUIDv7."""
    if type(value) is not User:
        raise IdentityError()
    try:
        uid = object.__getattribute__(value, "user_id")
    except Exception:
        raise IdentityError() from None
    _check_uuid(uid)
    return True


def validate_identity(value):
    """Valide une DigitalIdentity exacte et tous ses champs."""
    if type(value) is not DigitalIdentity:
        raise IdentityError()
    try:
        iid = object.__getattribute__(value, "identity_id")
        itype = object.__getattribute__(value, "identity_type")
        state = object.__getattribute__(value, "state")
    except Exception:
        raise IdentityError() from None
    _check_uuid(iid)
    _check_type(itype)
    _check_state(state)
    return True


def validate_link(value):
    """Valide un IdentityLink exact et ses deux identifiants."""
    if type(value) is not IdentityLink:
        raise IdentityError()
    try:
        uid = object.__getattribute__(value, "user_id")
        iid = object.__getattribute__(value, "identity_id")
    except Exception:
        raise IdentityError() from None
    _check_uuid(uid)
    _check_uuid(iid)
    return True


def validate_links(users, identities, links):
    """Valide un ensemble explicite de liaisons sans effet ni conservation."""
    if type(users) is not tuple:
        raise IdentityError()
    if type(identities) is not tuple:
        raise IdentityError()
    if type(links) is not tuple:
        raise IdentityError()
    user_ints = []
    for user in users:
        validate_user(user)
        uid = object.__getattribute__(user, "user_id")
        user_ints.append(object.__getattribute__(uid, "int"))
    identity_ints = []
    for identity in identities:
        validate_identity(identity)
        iid = object.__getattribute__(identity, "identity_id")
        identity_ints.append(object.__getattribute__(iid, "int"))
    if len(set(user_ints)) != len(user_ints):
        raise IdentityError()
    if len(set(identity_ints)) != len(identity_ints):
        raise IdentityError()
    user_set = set(user_ints)
    identity_set = set(identity_ints)
    if user_set & identity_set:
        raise IdentityError()
    seen_users = set()
    seen_identities = set()
    for link in links:
        validate_link(link)
        uid = object.__getattribute__(link, "user_id")
        iid = object.__getattribute__(link, "identity_id")
        uid_int = object.__getattribute__(uid, "int")
        iid_int = object.__getattribute__(iid, "int")
        if uid_int not in user_set:
            raise IdentityError()
        if iid_int not in identity_set:
            raise IdentityError()
        if uid_int in seen_users:
            raise IdentityError()
        if iid_int in seen_identities:
            raise IdentityError()
        seen_users.add(uid_int)
        seen_identities.add(iid_int)
    return True


__all__ = [
    "IdentityError",
    "IdentityType",
    "IdentityState",
    "User",
    "DigitalIdentity",
    "IdentityLink",
    "validate_user",
    "validate_identity",
    "validate_link",
    "validate_links",
]
