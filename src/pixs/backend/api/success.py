"""Enveloppe publique de succès et fabrique JSON 200 (fondation isolée).

`build_success_envelope` valide du JSON public fini aux types exacts,
copie profondément tous les conteneurs, puis retourne une enveloppe
fraîche `{"data":..., "meta":..., "links":...}`. `build_success_response`
valide d'abord, exige des réglages Django déjà configurés, puis
matérialise un `JsonResponse` non streaming statut 200 fixe. Imports
Django locaux seuls, sans configure/setup ni fallback, sans lecture
d'environnement. Ne modifie ni responses.py ni errors.py ni Kernel.
"""

from __future__ import annotations

import math

__all__ = [
    "ApiSuccessEnvelopeError",
    "build_success_envelope",
    "build_success_response",
]

_ERROR_ENVELOPE = "Enveloppe de succès invalide."
_ERROR_UNCONFIGURED = "Réglages Django non configurés."


class ApiSuccessEnvelopeError(ValueError):
    """Erreur d'enveloppe stable, sans écho de valeurs brutes."""

    def __init__(self, message=_ERROR_ENVELOPE):
        super().__init__(message)


def _fail():
    raise ApiSuccessEnvelopeError(_ERROR_ENVELOPE) from None


def _copy_json(value, ancestors):
    if value is None:
        return None
    if type(value) is bool:
        return value
    if type(value) is int:
        return value
    if type(value) is float:
        if math.isfinite(value) is False:
            _fail()
        return value
    if type(value) is str:
        return value
    if type(value) is list:
        vid = id(value)
        if vid in ancestors:
            _fail()
        ancestors.add(vid)
        try:
            out = []
            for item in value:
                out.append(_copy_json(item, ancestors))
        finally:
            ancestors.discard(vid)
        return out
    if type(value) is dict:
        vid = id(value)
        if vid in ancestors:
            _fail()
        ancestors.add(vid)
        try:
            out = {}
            for k, v in value.items():
                if type(k) is not str:
                    _fail()
                out[k] = _copy_json(v, ancestors)
        finally:
            ancestors.discard(vid)
        return out
    _fail()


def _check_envelope_parts(data, meta, links):
    if type(meta) is not dict:
        _fail()
    if type(links) is not dict:
        _fail()
    try:
        fresh = {
            "data": _copy_json(data, set()),
            "meta": _copy_json(meta, set()),
            "links": _copy_json(links, set()),
        }
    except RecursionError:
        raise ApiSuccessEnvelopeError(_ERROR_ENVELOPE) from None
    return fresh


def build_success_envelope(data: object, *, meta: object, links: object) -> dict:
    """Construit une enveloppe de succès publique isolée de ses entrées."""
    return _check_envelope_parts(data, meta, links)


def build_success_response(data: object, *, meta: object, links: object) -> object:
    """Construit la réponse JSON de succès 200 non streaming."""
    envelope = build_success_envelope(data, meta=meta, links=links)
    from django.conf import settings

    if not settings.configured:
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured(_ERROR_UNCONFIGURED)
    from django.http import JsonResponse

    return JsonResponse(
        envelope,
        status=200,
        content_type="application/json; charset=utf-8",
        json_dumps_params={"ensure_ascii": False},
    )
