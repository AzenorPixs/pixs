"""Bornes temporelles CA, mathématiques pures sur instants UTC explicites.

Portée exacte : seuils `A10i16` (`240/365`) et `A10i17` (`4/5`) sur validité
effective, âge de clé depuis création, plafond commun `A10i19/A10i20`
(`30 jours`), reliquat vers borne, borne descendante par minimum, plafond
de chevauchement terminal `A10i4` (`5 minutes`).

Le module ne lit aucune ressource externe et n’interroge aucune horloge.
Il n’applique aucune politique par défaut. Les instants, la politique, la source courante et l’horloge
qualifiée sont vérifiés par le propriétaire réel extérieur ; ces calculs
ne qualifient ni source, ni horloge, ni autorisation. Les ratios sont ceux
du profil canonique ; les durées `365/7300` sont nominales et configurables.
Aucune cryptopériode ni marge chiffrée inventée. `A07/A12` manquants restent
manquants.

Les comparaisons utilisent des produits croisés entiers en microsecondes,
sans flottant ni perte de précision. Un dépassement de seuil n’autorise ni
émission racine autonome ni bascule. Un résultat `True` ou une borne retournée
ne donne aucune permission.

Le renouvellement terminal A10i4 est dû aux deux tiers de la validité
effective ; 16 heures correspondent seulement à 24 heures effectives.
"""

from __future__ import annotations

import datetime

__all__ = [
    "DurationsError",
    "INTERMEDIATE_PREPARATION_NUMERATOR",
    "INTERMEDIATE_PREPARATION_DENOMINATOR",
    "ROOT_PREPARATION_NUMERATOR",
    "ROOT_PREPARATION_DENOMINATOR",
    "DAY_MICROSECONDS",
    "COEXISTENCE_DAYS",
    "COEXISTENCE_MICROSECONDS",
    "TERMINAL_OVERLAP_MICROSECONDS",
    "TERMINAL_RENEWAL_NUMERATOR",
    "TERMINAL_RENEWAL_DENOMINATOR",
    "preparation_due",
    "key_age_us",
    "coexistence_upper_bound",
    "remaining_to_boundary_us",
    "bound_descendant_not_after",
    "terminal_overlap_upper_bound",
    "terminal_renewal_due",
]

INTERMEDIATE_PREPARATION_NUMERATOR = 240
INTERMEDIATE_PREPARATION_DENOMINATOR = 365
ROOT_PREPARATION_NUMERATOR = 4
ROOT_PREPARATION_DENOMINATOR = 5
DAY_MICROSECONDS = 86_400_000_000
COEXISTENCE_DAYS = 30
COEXISTENCE_MICROSECONDS = 2_592_000_000_000
TERMINAL_OVERLAP_MICROSECONDS = 300_000_000
TERMINAL_RENEWAL_NUMERATOR = 2
TERMINAL_RENEWAL_DENOMINATOR = 3

_VALID_ROLES = ("intermediate", "root")


class DurationsError(ValueError):
    """Refus temporel sans exposer les entrées."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_durations"


def _deny(code: str, element: str) -> DurationsError:
    return DurationsError(code, element)


def _require_role(value: object, element: str) -> str:
    if type(value) is not str or value not in _VALID_ROLES:
        raise _deny("ROLE_INCONNU", element)
    return value


def _require_utc(value: object, element: str) -> datetime.datetime:
    if type(value) is not datetime.datetime:
        raise _deny("HORODATAGE_NON_UTC", element)
    if value.tzinfo is not datetime.timezone.utc:
        raise _deny("HORODATAGE_NON_UTC", element)
    return value


def _delta_us(before: datetime.datetime, after: datetime.datetime) -> int:
    delta = after - before
    return (
        delta.days * DAY_MICROSECONDS
        + delta.seconds * 1_000_000
        + delta.microseconds
    )


def preparation_due(
    role: object,
    not_before: object,
    not_after: object,
    observed_at: object,
) -> bool:
    """Préparation due dès que la fraction effective est atteinte.

    Un certificat préparé peut avoir un début futur : avant ce début, la
    préparation n’est pas due et le résultat vaut `False`. Après expiration,
    le résultat vaut `True` sans accorder aucun droit.
    """
    name = _require_role(role, "durations.role")
    start = _require_utc(not_before, "durations.not_before")
    end = _require_utc(not_after, "durations.not_after")
    observed = _require_utc(observed_at, "durations.observed_at")
    if end <= start:
        raise _deny("INTERVALLE_INVALIDE", "durations.validite")
    if observed < start:
        return False
    effective = _delta_us(start, end)
    elapsed = _delta_us(start, observed)
    if name == "intermediate":
        return (
            elapsed * INTERMEDIATE_PREPARATION_DENOMINATOR
            >= effective * INTERMEDIATE_PREPARATION_NUMERATOR
        )
    return (
        elapsed * ROOT_PREPARATION_DENOMINATOR
        >= effective * ROOT_PREPARATION_NUMERATOR
    )


def key_age_us(created_at: object, observed_at: object) -> int:
    """Âge de paire depuis création, sans remise à zéro."""
    created = _require_utc(created_at, "durations.created_at")
    observed = _require_utc(observed_at, "durations.observed_at")
    if observed < created:
        raise _deny("HORODATAGE_INCOHERENT", "durations.observed_at")
    return _delta_us(created, observed)


def coexistence_upper_bound(
    common_engaged_at: object,
    plan_deadline: object,
    old_anchor_bound: object,
) -> datetime.datetime:
    """Minimum entre engagement plus `30 jours` et bornes plus courtes.

    Le minimum des fins fournies est examiné d’abord ; l’addition du plafond
    n’a lieu que si cette borne existante est plus tardive, donc l’addition
    reste représentable, y compris près de `datetime.max UTC`.
    """
    engaged = _require_utc(
        common_engaged_at, "durations.common_engaged_at"
    )
    deadline = _require_utc(plan_deadline, "durations.plan_deadline")
    anchor = _require_utc(old_anchor_bound, "durations.old_anchor_bound")
    if deadline <= engaged:
        raise _deny("INTERVALLE_INVALIDE", "durations.plan_deadline")
    if anchor <= engaged:
        raise _deny("INTERVALLE_INVALIDE", "durations.old_anchor_bound")
    earliest = deadline
    if anchor < earliest:
        earliest = anchor
    if _delta_us(engaged, earliest) > COEXISTENCE_MICROSECONDS:
        return engaged + datetime.timedelta(microseconds=COEXISTENCE_MICROSECONDS)
    return earliest


def remaining_to_boundary_us(bound: object, observed_at: object) -> int:
    """Reliquat vers borne commune, zéro si atteinte, sans permission."""
    limit = _require_utc(bound, "durations.bound")
    observed = _require_utc(observed_at, "durations.observed_at")
    if limit <= observed:
        return 0
    return _delta_us(observed, limit)


def bound_descendant_not_after(
    requested_not_before: object,
    requested_not_after: object,
    issuer_end: object,
    anchor_end: object,
    authorization_end: object,
) -> datetime.datetime:
    """Borne descendante au minimum des échéances, sans durée implicite."""
    request_start = _require_utc(
        requested_not_before, "durations.requested_not_before"
    )
    request_end = _require_utc(
        requested_not_after, "durations.requested_not_after"
    )
    issuer = _require_utc(issuer_end, "durations.issuer_end")
    anchor = _require_utc(anchor_end, "durations.anchor_end")
    authorization = _require_utc(
        authorization_end, "durations.authorization_end"
    )
    if request_end <= request_start:
        raise _deny("INTERVALLE_INVALIDE", "durations.demande")
    bound = request_end
    if issuer < bound:
        bound = issuer
    if anchor < bound:
        bound = anchor
    if authorization < bound:
        bound = authorization
    if bound <= request_start:
        raise _deny(
            "DUREE_DESCENDANTE_INSUFFISANTE", "durations.descendant"
        )
    return bound


def terminal_overlap_upper_bound(
    overlap_start: object,
    old_end: object,
    new_end: object,
    authorization_end: object,
) -> datetime.datetime:
    """Plafond de chevauchement terminal, au plus `5 minutes` et bornes.

    Maximum canonique, pas minimum positif imposé. Si une fin fournie est
    déjà atteinte ou passée, la borne retournée l’est aussi et le reliquat
    vaut `0` via `remaining_to_boundary_us`, sans nouvelle grâce. Cette
    fonction ne donne aucune autorisation de récupération ni de nouveau
    certificat.
    """
    start = _require_utc(overlap_start, "durations.overlap_start")
    old = _require_utc(old_end, "durations.old_end")
    new = _require_utc(new_end, "durations.new_end")
    authorization = _require_utc(
        authorization_end, "durations.authorization_end"
    )
    earliest = old
    if new < earliest:
        earliest = new
    if authorization < earliest:
        earliest = authorization
    if earliest <= start:
        return earliest
    if _delta_us(start, earliest) > TERMINAL_OVERLAP_MICROSECONDS:
        return start + datetime.timedelta(
            microseconds=TERMINAL_OVERLAP_MICROSECONDS
        )
    return earliest


def terminal_renewal_due(
    not_before: object,
    not_after: object,
    observed_at: object,
) -> bool:
    """Seuil A10i4 aux deux tiers effectifs, sans droit ni horloge.

    Avant le début, le seuil n'est pas atteint. À partir de l'expiration,
    il est dépassé sans autoriser de renouvellement ou récupération.
    Les produits croisés entiers évitent toute troncature ou flottant.
    """
    start = _require_utc(not_before, "durations.not_before")
    end = _require_utc(not_after, "durations.not_after")
    observed = _require_utc(observed_at, "durations.observed_at")
    if end <= start:
        raise _deny("INTERVALLE_INVALIDE", "durations.validite")
    if observed < start:
        return False
    effective = _delta_us(start, end)
    elapsed = _delta_us(start, observed)
    return (
        elapsed * TERMINAL_RENEWAL_DENOMINATOR
        >= effective * TERMINAL_RENEWAL_NUMERATOR
    )
