"""Règles privées de configuration et de mode C08, sans autorité.

Ces fonctions calculent des valeurs désirées. Elles ne lisent aucun état,
n'appliquent aucune transition et ne prouvent aucune autorisation ou readiness.
"""
from enum import Enum

from pixs.backend.startup_mode import StartupMode

__all__ = ["ConfigurationState", "ModeOperationKind", "ModeValuesError",
           "validate_state_pair", "transition_state"]


class ConfigurationState(Enum):
    PENDING = "PENDING"
    CONFIGURED = "CONFIGURED"


class ModeOperationKind(Enum):
    FINALIZE_CONFIGURATION = "FINALIZE_CONFIGURATION"
    ENTER_MAINTENANCE = "ENTER_MAINTENANCE"
    EXIT_MAINTENANCE = "EXIT_MAINTENANCE"


class ModeValuesError(ValueError):
    code = "C08_MODE_VALUES_REFUSED"

    def __init__(self) -> None:
        super().__init__("Valeurs de configuration ou de mode refusées.")


_ALLOWED_PAIRS = frozenset({
    (ConfigurationState.PENDING, StartupMode.FIRST_CONFIGURATION),
    (ConfigurationState.PENDING, StartupMode.MAINTENANCE),
    (ConfigurationState.CONFIGURED, StartupMode.NORMAL),
    (ConfigurationState.CONFIGURED, StartupMode.MAINTENANCE),
})


def validate_state_pair(
    configuration_state: ConfigurationState, operating_mode: StartupMode,
) -> tuple[ConfigurationState, StartupMode]:
    """Valide des valeurs seulement, sans consulter de producteur de confiance."""
    if (type(configuration_state) is not ConfigurationState
            or type(operating_mode) is not StartupMode):
        raise ModeValuesError()
    pair = (configuration_state, operating_mode)
    if pair not in _ALLOWED_PAIRS:
        raise ModeValuesError()
    return pair


def transition_state(
    configuration_state: ConfigurationState, operating_mode: StartupMode,
    kind: ModeOperationKind,
) -> tuple[ConfigurationState, StartupMode]:
    """Calcule la paire désirée ; le service propriétaire devra l'autoriser."""
    validate_state_pair(configuration_state, operating_mode)
    if type(kind) is not ModeOperationKind:
        raise ModeValuesError()
    if kind is ModeOperationKind.FINALIZE_CONFIGURATION:
        configuration_state = ConfigurationState.CONFIGURED
        if operating_mode is not StartupMode.MAINTENANCE:
            operating_mode = StartupMode.NORMAL
    elif kind is ModeOperationKind.ENTER_MAINTENANCE:
        operating_mode = StartupMode.MAINTENANCE
    elif kind is ModeOperationKind.EXIT_MAINTENANCE:
        operating_mode = (StartupMode.FIRST_CONFIGURATION
                          if configuration_state is ConfigurationState.PENDING
                          else StartupMode.NORMAL)
    else:
        raise ModeValuesError()
    return validate_state_pair(configuration_state, operating_mode)
