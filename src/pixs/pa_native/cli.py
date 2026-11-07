"""Sélection explicite du mode PA/PZT, sans effet ni autorité."""
from __future__ import annotations

from types import MappingProxyType

__all__ = ["ModeError", "parse_mode"]

_MODES = MappingProxyType({
    "pixs-pa-system": ("system-daemon",),
    "pixs-pa-events": ("system-start", "system-stop"),
    "pixs-pa-session": ("session-start", "session-stop", "session-daemon"),
    "pzt": ("pzt-daemon",),
})


class ModeError(ValueError):
    """CLI refusée ; le diagnostic n'expose aucune valeur reçue."""


def parse_mode(executable: str, arguments: list[str] | tuple[str, ...]) -> str:
    """Accepte un seul --mode du rôle compilé, jamais dérivé d'argv[0].

    L'appelant fournit l'identité fixe issue du build. Le mode sélectionné
    ne prouve ni configuration, autorisation, disponibilité ni exécution.
    """
    if type(executable) is not str or executable not in _MODES:
        raise ModeError("PA01_CLI_EXECUTABLE_INVALID")
    if type(arguments) not in (list, tuple) or any(type(a) is not str or "\x00" in a for a in arguments):
        raise ModeError("PA01_CLI_ARGUMENTS_INVALID")
    if len(arguments) == 2 and arguments[0] == "--mode":
        mode = arguments[1]
    elif len(arguments) == 1 and arguments[0].startswith("--mode="):
        mode = arguments[0][len("--mode="):]
    else:
        raise ModeError("PA01_CLI_MODE_REQUIRED")
    if mode not in _MODES[executable]:
        raise ModeError("PA01_CLI_MODE_FORBIDDEN")
    return mode
