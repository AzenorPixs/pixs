"""Représentation déclarative partielle de la corrélation des travaux du Kernel.

Les valeurs sont fournies par un caller trusted ou par des fixtures
synthétiques. La validation vérifie seulement la structure déclarative exigée
par la norme canonique ``jobs`` ; elle ne prouve ni l'existence, ni la
légitimité, ni la canonicité, ni l'autorisation, ni la sensibilité d'une
référence.

Cette représentation n'est pas le contrat ``Job`` complet. Elle ne porte
aucune comparaison d'identifiants, aucun état, aucune tentative, aucun bail,
aucun horodatage, aucun payload, aucune version SemVer, aucune authentification,
aucune déduplication, aucune persistance, aucun runtime, aucune configuration
et aucune nouvelle dépendance. ``perimeter_reference`` est une référence
opaque du périmètre, distincte du ``tenant_context``, sans résolution ni
permission.
"""

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic

__all__ = [
    "JobCorrelation",
    "validate_job_correlation",
]

_CORRELATION_FIELDS = (
    "job_id",
    "correlation_id",
    "causation_id",
    "perimeter_reference",
)


@dataclass(frozen=True)
class JobCorrelation:
    job_id: str
    correlation_id: str
    causation_id: str
    perimeter_reference: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"job_correlation.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque_reference(value: object) -> bool:
    return type(value) is str and bool(value)


def validate_job_correlation(candidate: object) -> list[Diagnostic]:
    """Valide la structure déclarative d'une corrélation de travail, sans écho."""
    if type(candidate) is not JobCorrelation:
        return [_refusal("correlation", "corrélation de travail exacte attendue")]

    refusals: list[Diagnostic] = []

    for field in _CORRELATION_FIELDS:
        if not _is_opaque_reference(getattr(candidate, field)):
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )

    return _pack(refusals)
