"""Entrée Django réelle minimale : jalon partiel, sans réglage par défaut."""

import sys

from django.core.exceptions import ImproperlyConfigured
from django.core.management import execute_from_command_line


def main(argv=None) -> int:
    """Délègue à Django ; refuse sans configuration par message fixe."""
    try:
        execute_from_command_line(sys.argv if argv is None else argv)
    except ImproperlyConfigured:
        print(
            "Configuration Django requise; aucun réglage par défaut.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
