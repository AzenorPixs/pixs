"""Classificateur pur de snapshots santé, borné et déterministe, sans IO."""

__all__ = [
    "classify_health",
]

_MAX_TUPLE_LENGTH = 256
_INVALID_MESSAGE = "Invalid health snapshot"


def _refuse() -> None:
    raise ValueError(_INVALID_MESSAGE) from None


def classify_health(*, alive, startup_complete, pg_available, required=(), optional=()):
    if type(alive) is not bool or type(startup_complete) is not bool or type(pg_available) is not bool:
        _refuse()
    if type(required) is not tuple or type(optional) is not tuple:
        _refuse()
    if len(required) > _MAX_TUPLE_LENGTH or len(optional) > _MAX_TUPLE_LENGTH:
        _refuse()
    for value in required:
        if type(value) is not bool:
            _refuse()
    for value in optional:
        if type(value) is not bool:
            _refuse()
    required_ok = all(required)
    optional_ok_count = sum(optional)
    availability = alive and startup_complete and pg_available and required_ok
    return {
        "liveness": alive,
        "startup": startup_complete,
        "availability": availability,
        "degraded": optional_ok_count != len(optional),
        "pg_available": pg_available,
        "required_count": 1 + len(required),
        "required_ok_count": int(pg_available) + sum(required),
        "optional_count": len(optional),
        "optional_ok_count": optional_ok_count,
    }
