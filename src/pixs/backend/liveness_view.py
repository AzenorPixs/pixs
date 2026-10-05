"""Bounded Django liveness view, request actually handled, zero dependency.

Contract: `liveness_view` accepts real Django requests (`WSGIRequest` /
`ASGIRequest`) through minimal standard validation of the `method`
attribute only. GET or HEAD returns 200 with an empty body. Any other
exact method returns 405 with an empty body and `Allow: GET, HEAD`. All
responses use `text/plain; charset=utf-8` and `Cache-Control: no-store`.
The view proves only that the request was actually handled. No readiness,
startup, P0, composition, persistence or API claim. No public URL is
distributed by this module.

Limits: no Django import or configuration at plain import; no
`settings.configure`, `django.setup`, server, DB, socket or I/O in this
module; no external read; no secret, trace or sensitive payload.
"""

from __future__ import annotations

__all__ = [
    "LivenessError",
    "liveness_view",
]

_ERROR = "Invalid liveness request."
_ALLOW_VALUE = "GET, HEAD"
_CONTENT_TYPE = "text/plain; charset=utf-8"
_NO_STORE = "no-store"


class LivenessError(ValueError):
    """Stable liveness error, without raw value echo."""

    def __init__(self, message: str = _ERROR) -> None:
        super().__init__(message)


def _invalid_request() -> LivenessError:
    return LivenessError(_ERROR)


def _require_method(request: object) -> str:
    try:
        method = getattr(request, "method", None)
    except Exception:
        raise _invalid_request() from None
    if type(method) is not str:
        raise _invalid_request()
    return method


def liveness_view(request: object) -> object:
    """Handle one liveness probe with an empty bounded response."""
    method = _require_method(request)
    from django.http import HttpResponse

    if method == "GET" or method == "HEAD":
        response = HttpResponse(b"", status=200, content_type=_CONTENT_TYPE)
        response["Cache-Control"] = _NO_STORE
        return response
    denied = HttpResponse(b"", status=405, content_type=_CONTENT_TYPE)
    denied["Cache-Control"] = _NO_STORE
    denied["Allow"] = _ALLOW_VALUE
    return denied
