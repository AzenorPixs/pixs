"""Lien interne préparatoire BulkJobLink v1 et validation structurelle pure.

Références fournies par un appelant de confiance ou des fixtures synthétiques.
Ce profil ne prouve ni rattachement effectif, existence, autorisation, périmètre,
cardinalité ou unicité globales, corrélation, causalité, déduplication ou persistance.
"""

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic

__all__ = ["BulkJobLink", "validate_bulk_job_link"]

_FIELDS = ("operation_id", "job_id")


@dataclass(frozen=True)
class BulkJobLink:
    operation_id: str
    job_id: str


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_job_link.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_job_link(candidate: object) -> list[Diagnostic]:
    """Valide le type exact puis les références, sans effet ni écho."""
    if type(candidate) is not BulkJobLink:
        return [_refusal("link", "lien BulkJobLink exact attendu")]

    values = tuple(getattr(candidate, field, None) for field in _FIELDS)
    refusals: list[Diagnostic] = []
    for field, value in zip(_FIELDS, values):
        if type(value) is not str or not value:
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )

    if not refusals and values[0] == values[1]:
        refusals.append(_refusal("distinction", "références distinctes attendues"))
    return _pack(refusals)
