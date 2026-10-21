"""Groupes et appartenances utilisateur-groupe, structure seule."""

import uuid
from dataclasses import dataclass

from ..scope import (
    ScopeContext,
    ScopeStructureError,
    validate_structure,
)
from .models import IdentityError, _check_uuid, validate_user


class GroupError(ValueError):
    """Erreur structurelle stable sans valeur brute."""

    def __init__(self):
        super().__init__("Groupe ou appartenance invalide.")
        self.code = "GROUP_INVALID"
        self.element = "group_membership"
        self.step = "validate_group_membership"


@dataclass(frozen=True, slots=True, repr=False)
class Group:
    """Groupe minimal avec contexte explicite obligatoire."""

    group_id: uuid.UUID
    context: ScopeContext

    def __post_init__(self):
        validate_group(self)


@dataclass(frozen=True, slots=True, repr=False)
class Membership:
    """Relation de paire utilisateur-groupe, sans persistance."""

    user_id: uuid.UUID
    group_id: uuid.UUID

    def __post_init__(self):
        validate_membership(self)


def _check_context(value):
    """Valide un ScopeContext exact structurellement, sans topologie."""
    if type(value) is not ScopeContext:
        raise GroupError()
    try:
        validate_structure(value)
    except ScopeStructureError:
        raise GroupError() from None
    except Exception:
        raise GroupError() from None
    return True


def validate_group(value):
    """Valide un Group exact, son UUIDv7 et son contexte explicite."""
    if type(value) is not Group:
        raise GroupError()
    try:
        gid = object.__getattribute__(value, "group_id")
        ctx = object.__getattribute__(value, "context")
    except Exception:
        raise GroupError() from None
    try:
        _check_uuid(gid)
    except IdentityError:
        raise GroupError() from None
    _check_context(ctx)
    return True


def validate_membership(value):
    """Valide une Membership exacte et ses deux UUIDv7."""
    if type(value) is not Membership:
        raise GroupError()
    try:
        uid = object.__getattribute__(value, "user_id")
        gid = object.__getattribute__(value, "group_id")
    except Exception:
        raise GroupError() from None
    try:
        _check_uuid(uid)
        _check_uuid(gid)
    except IdentityError:
        raise GroupError() from None
    return True


def validate_memberships(users, groups, memberships):
    """Valide un ensemble n:m sans effet, conservation ni topologie."""
    if type(users) is not tuple:
        raise GroupError()
    if type(groups) is not tuple:
        raise GroupError()
    if type(memberships) is not tuple:
        raise GroupError()
    user_ints = []
    for user in users:
        try:
            validate_user(user)
        except IdentityError:
            raise GroupError() from None
        try:
            uid = object.__getattribute__(user, "user_id")
            user_ints.append(object.__getattribute__(uid, "int"))
        except Exception:
            raise GroupError() from None
    group_ints = []
    for group in groups:
        validate_group(group)
        try:
            gid = object.__getattribute__(group, "group_id")
            group_ints.append(object.__getattribute__(gid, "int"))
        except Exception:
            raise GroupError() from None
    if len(set(user_ints)) != len(user_ints):
        raise GroupError()
    if len(set(group_ints)) != len(group_ints):
        raise GroupError()
    user_set = set(user_ints)
    group_set = set(group_ints)
    if user_set & group_set:
        raise GroupError()
    seen_pairs = set()
    for membership in memberships:
        validate_membership(membership)
        try:
            uid = object.__getattribute__(membership, "user_id")
            gid = object.__getattribute__(membership, "group_id")
            uid_int = object.__getattribute__(uid, "int")
            gid_int = object.__getattribute__(gid, "int")
        except Exception:
            raise GroupError() from None
        if uid_int not in user_set:
            raise GroupError()
        if gid_int not in group_set:
            raise GroupError()
        pair = (uid_int, gid_int)
        if pair in seen_pairs:
            raise GroupError()
        seen_pairs.add(pair)
    return True


__all__ = [
    "GroupError",
    "Group",
    "Membership",
    "validate_group",
    "validate_membership",
    "validate_memberships",
]
