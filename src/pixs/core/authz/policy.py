"""Types de politiques PDP minimal : structure seule, activation par snapshot.

Distinction : la construction vérifie conteneurs et scalaires constants ;
la validation élémentaire exhaustive et la normalisation ont lieu dans
build_snapshot une fois les limites de tailles vérifiées.
"""

import datetime
from dataclasses import dataclass
from enum import Enum

from ..scope.context import ScopeContext, validate_structure


class PolicyError(ValueError):
    def __init__(self):
        super().__init__("Politique invalide.")
        self.code = "PDP_POLICY_INVALID"
        self.element = "pdp_policy"
        self.step = "validate_policy"


class Effect(Enum):
    DENY = "DENY"
    ALLOW = "ALLOW"


class IdentityAssurance(Enum):
    CLAIMED = "CLAIMED"
    VERIFIED = "VERIFIED"
    PROOFED = "PROOFED"


class AuthenticationAssurance(Enum):
    SINGLE_FACTOR = "SINGLE_FACTOR"
    MULTI_FACTOR = "MULTI_FACTOR"
    PHISHING_RESISTANT = "PHISHING_RESISTANT"


class FederationTrust(Enum):
    UNTRUSTED = "UNTRUSTED"
    TRUSTED = "TRUSTED"
    STRONGLY_BOUND = "STRONGLY_BOUND"


def _is_id(value):
    return type(value) is str and value != ""


def _is_utc_aware(value):
    return (
        type(value) is datetime.datetime
        and value.tzinfo is datetime.timezone.utc
    )


@dataclass(frozen=True, slots=True, repr=False)
class Selector:
    kind: str
    values: tuple

    def __post_init__(self):
        kind = object.__getattribute__(self, "kind")
        values = object.__getattribute__(self, "values")
        if type(kind) is not str or kind not in (
            "subject",
            "resource",
            "action",
        ):
            raise PolicyError()
        if type(values) is not tuple or len(values) == 0:
            raise PolicyError()


@dataclass(frozen=True, slots=True, repr=False)
class ScopeSelector:
    contexts: tuple

    def __post_init__(self):
        contexts = object.__getattribute__(self, "contexts")
        if type(contexts) is not tuple or len(contexts) == 0:
            raise PolicyError()


@dataclass(frozen=True, slots=True, repr=False)
class Condition:
    attr: str
    op: str
    value: object

    def __post_init__(self):
        attr = object.__getattribute__(self, "attr")
        op = object.__getattribute__(self, "op")
        if type(attr) is not str or attr == "":
            raise PolicyError()
        if type(op) is not str or op not in ("eq", "in"):
            raise PolicyError()
        if type(object.__getattribute__(self, "value")) is bool:
            raise PolicyError()


@dataclass(frozen=True, slots=True, repr=False)
class Obligation:
    kind: str

    def __post_init__(self):
        kind = object.__getattribute__(self, "kind")
        if type(kind) is not str or kind != "AUDIT":
            raise PolicyError()


@dataclass(frozen=True, slots=True, repr=False)
class Policy:
    policy_id: str
    policy_version: str
    owner: str
    effect: Effect
    subject: Selector
    resource: Selector
    action: Selector
    scope: ScopeSelector
    conditions: tuple = ()
    obligations: tuple = ()
    valid_from: object = None
    valid_until: object = None
    min_identity_assurance: object = None
    min_authentication_assurance: object = None
    min_federation_trust: object = None
    max_auth_age_seconds: object = None

    def __post_init__(self):
        if not _is_id(object.__getattribute__(self, "policy_id")):
            raise PolicyError()
        if not _is_id(object.__getattribute__(self, "policy_version")):
            raise PolicyError()
        if not _is_id(object.__getattribute__(self, "owner")):
            raise PolicyError()
        if type(object.__getattribute__(self, "effect")) is not Effect:
            raise PolicyError()
        for name in ("subject", "resource", "action"):
            if type(object.__getattribute__(self, name)) is not Selector:
                raise PolicyError()
        if type(object.__getattribute__(self, "scope")) is not ScopeSelector:
            raise PolicyError()
        if type(object.__getattribute__(self, "conditions")) is not tuple:
            raise PolicyError()
        if type(object.__getattribute__(self, "obligations")) is not tuple:
            raise PolicyError()
        vfrom = object.__getattribute__(self, "valid_from")
        vuntil = object.__getattribute__(self, "valid_until")
        for bound in (vfrom, vuntil):
            if bound is not None and not _is_utc_aware(bound):
                raise PolicyError()
        if vfrom is not None and vuntil is not None and vfrom >= vuntil:
            raise PolicyError()
        if not isinstance(
            object.__getattribute__(self, "min_identity_assurance"),
            (IdentityAssurance, type(None)),
        ):
            raise PolicyError()
        if not isinstance(
            object.__getattribute__(self, "min_authentication_assurance"),
            (AuthenticationAssurance, type(None)),
        ):
            raise PolicyError()
        if not isinstance(
            object.__getattribute__(self, "min_federation_trust"),
            (FederationTrust, type(None)),
        ):
            raise PolicyError()
        max_age = object.__getattribute__(self, "max_auth_age_seconds")
        if max_age is not None and (
            type(max_age) is bool or type(max_age) is not int or max_age <= 0
        ):
            raise PolicyError()


__all__ = [
    "PolicyError",
    "Effect",
    "IdentityAssurance",
    "AuthenticationAssurance",
    "FederationTrust",
    "Selector",
    "ScopeSelector",
    "Condition",
    "Obligation",
    "Policy",
]
