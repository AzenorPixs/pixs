"""Données pures de composition initiale 0.1.0 : déclarations partielles, aucune attestation, activation, P0 ou readiness globale."""

COMPOSITION_VERSION = "0.1.0"
MANIFEST_PATHS = (
    "src/pixs/kernel/component.toml",
    "src/pixs/core/component.toml",
    "src/pixs/example/component.toml",
)
OFFICIAL_IDS = ("pixs.kernel", "pixs.core")
REQUIRED_IDS = ("pixs.kernel", "pixs.core", "example.hello")
