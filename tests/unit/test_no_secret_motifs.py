"""Contrôle 6.3 : artefacts produits par le noyau sans motif sensible.

Scanne exclusivement les artefacts produits par le moteur (diagnostics et
repr/str des résultats de composition) sur un corpus de scénarios de refus et de
succès. N'ouvre JAMAIS de fichier et ne lit AUCUNE source exclue (project.env,
clés, secrets) : le contrôle est purement mémoire, sans effet de bord.

Les fixtures de détection embarquent volontairement des placeholders (ex. la
valeur AWS d'exemple AKIA…EXAMPLE) pour prouver que le garde les refuse sans les
reproduire ; ce sont des entrées de test, pas des artefacts produits. Le scanner
contrôle donc les sorties du moteur, et non leurs entrées.

Les sentinelles synthétiques (fournisseur configuré, proof_ref) sont des
marqueurs détectables séparés des échantillons de contrôle : elles prouvent
que les refus n'échoïsent aucune valeur d'entrée sensible.

Garde non muet : échoue si aucun artefact admissible n'est inspecté ou si aucun
motif n'est actif ; un échantillon de contrôle prouve que chaque motif détecte.
"""

import re
import unittest

from pixs.kernel.composition import ConformityAttestation, compose
from tests.conformity_fixtures import synthetic_attestations

APP_TOML = 'schema_version = "1"\nid = "acme.app"\ntype = "MODULE"\nversion = "1.0.0"\n'
MISSING_TYPE_TOML = 'schema_version = "1"\nid = "acme.app"\nversion = "1.0.0"\n'
WRONG_ID_TOML = 'schema_version = "1"\nid = 42\ntype = "MODULE"\nversion = "1.0.0"\n'
BAD_TYPE_TOML = 'schema_version = "1"\nid = "acme.app"\ntype = "APPLICATION"\nversion = "1.0.0"\n'
BAD_VERSION_TOML = 'schema_version = "1"\nid = "acme.app"\ntype = "MODULE"\nversion = "1.0"\n'
UNKNOWN_SCHEMA_TOML = 'schema_version = "2"\nid = "acme.app"\ntype = "MODULE"\nversion = "1.0.0"\n'
SECRET_TOML = (
    'schema_version = "1"\nid = "acme.app"\ntype = "MODULE"\nversion = "1.0.0"\n'
    'name = "AKIAIOSFODNN7EXAMPLE"\n'
)
EXECUTABLE_TOML = (
    'schema_version = "1"\nid = "acme.app"\ntype = "MODULE"\nversion = "1.0.0"\n'
    'name = "${DEPLOIEMENT_TOKEN}"\n'
)
USURPER_TOML = 'schema_version = "1"\nid = "pixs.usurpe"\ntype = "MODULE"\nversion = "1.0.0"\n'

P1_TOML = (
    'schema_version = "1"\nid = "t.web"\ntype = "MODULE"\nversion = "1.0.0"\n'
    '[dependencies]\ncapabilities = ["audit >=1.0.0"]\n'
)
PROV1_TOML = (
    'schema_version = "1"\nid = "t.p1"\ntype = "PROVIDER"\nversion = "1.0.0"\n'
    '[provides]\n[[provides.capabilities]]\n'
    'id = "audit"\nversion = "1.0.0"\ncontracts = []\n'
    'criticality = "REQUIRED"\nfallback = "none"\n'
)
PROV2_TOML = (
    'schema_version = "1"\nid = "t.p2"\ntype = "PROVIDER"\nversion = "1.0.0"\n'
    '[provides]\n[[provides.capabilities]]\n'
    'id = "audit"\nversion = "1.0.0"\ncontracts = []\n'
    'criticality = "REQUIRED"\nfallback = "none"\n'
)
DEP_TOML = (
    'schema_version = "1"\nid = "acme.dep"\ntype = "MODULE"\nversion = "1.0.0"\n'
    '[dependencies]\ncomponents = ["acme.absent >=1.0.0"]\n'
)

SYNTHETIC_PROVIDER_SENTINEL = "synthetic:absent-provider-001"
SYNTHETIC_PROOF_SENTINEL = "synthetic:proof-001"


def _preuve_ephemere_sentinelle() -> ConformityAttestation:
    """Double en échec portant une proof_ref sentinelle détectable."""
    return ConformityAttestation(
        component_id="acme.app",
        component_version="1.0.0",
        scope="COMPONENT",
        target_id="acme.app",
        target_version="1.0.0",
        suite_id="synthetic.fixture",
        suite_version="1.0.0",
        verdict="FAIL",
        proof_ref=SYNTHETIC_PROOF_SENTINEL,
    )


FORBIDDEN_PATTERNS: dict[str, re.Pattern[str]] = {
    "aws_access_key_id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "pem_private_key": re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    "jwt_token": re.compile(
        r"\beyJ[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}"
    ),
    "env_interpolation": re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}"),
    "template_interpolation": re.compile(r"\{\{.*?\}\}"),
    "secret_assignment": re.compile(
        r"(?i)\b(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|"
        r"private[_-]?key)\b\s*[:=]\s*[\"'][^\"']{8,}[\"']"
    ),
}

CONTROL_SAMPLES: dict[str, str] = {
    "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "pem_private_key": "-----BEGIN RSA PRIVATE KEY-----",
    "jwt_token": (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcDEF123"
    ),
    "env_interpolation": "prefix ${DEPLOIEMENT_TOKEN} suffix",
    "template_interpolation": "value {{ lookup }} end",
    "secret_assignment": 'password = "s3cr3t-value-long"',
}


def _engine_artifacts() -> list[str]:
    """Collecte les sorties texte produites par le moteur (aucune lecture fichier)."""
    results = [
        compose([APP_TOML], attestations=synthetic_attestations([APP_TOML])),
        compose([MISSING_TYPE_TOML]),
        compose([WRONG_ID_TOML]),
        compose([BAD_TYPE_TOML]),
        compose([BAD_VERSION_TOML]),
        compose([UNKNOWN_SCHEMA_TOML]),
        compose([SECRET_TOML]),
        compose([EXECUTABLE_TOML]),
        compose([USURPER_TOML, APP_TOML]),
        compose([DEP_TOML]),
        compose([P1_TOML, PROV1_TOML, PROV2_TOML]),
        compose(
            [P1_TOML, PROV1_TOML, PROV2_TOML],
            configured_providers={"audit": "t.absent"},
        ),
        compose(
            [P1_TOML, PROV1_TOML, PROV2_TOML],
            configured_providers={"audit": SYNTHETIC_PROVIDER_SENTINEL},
        ),
        compose(
            [APP_TOML],
            attestations=[_preuve_ephemere_sentinelle()],
        ),
        compose([PROV1_TOML], required_ids=("acme.absent",)),
        compose([42]),
    ]
    artifacts: list[str] = []
    for result in results:
        artifacts.extend(str(diagnostic) for diagnostic in result.diagnostics)
        artifacts.extend(str(warning) for warning in result.warnings)
        artifacts.append(repr(result))
    return artifacts


ARTIFACTS = _engine_artifacts()


class TestScannerNonMuet(unittest.TestCase):
    def test_motifs_actifs(self) -> None:
        self.assertGreater(len(FORBIDDEN_PATTERNS), 0)

    def test_artefacts_admissibles_non_vides(self) -> None:
        self.assertGreater(len(ARTIFACTS), 0, "aucun artefact admissible inspecté")
        for artifact in ARTIFACTS:
            self.assertIsInstance(artifact, str)
            self.assertTrue(artifact)

    def test_echantillons_de_controle_detectes(self) -> None:
        self.assertEqual(set(CONTROL_SAMPLES), set(FORBIDDEN_PATTERNS))
        for name, sample in CONTROL_SAMPLES.items():
            self.assertRegex(sample, FORBIDDEN_PATTERNS[name])


class TestArtefactsSansSecret(unittest.TestCase):
    def test_aucun_motif_sensible_dans_les_artefacts_moteur(self) -> None:
        violations: list[str] = []
        for artifact in ARTIFACTS:
            for name, pattern in FORBIDDEN_PATTERNS.items():
                if pattern.search(artifact):
                    violations.append(f"{name} dans {artifact[:80]!r}")
        self.assertEqual(
            violations, [], f"motif sensible dans un artefact : {violations}"
        )

    def test_succes_app_active_explicitement(self) -> None:
        result = compose(
            [APP_TOML], attestations=synthetic_attestations([APP_TOML])
        )
        self.assertTrue(result.activated)
        self.assertEqual(result.stage, "activated")
        self.assertEqual(result.diagnostics, ())

    def test_aucun_echo_sentinelles_synthétiques(self) -> None:
        refuse_configure = compose(
            [P1_TOML, PROV1_TOML, PROV2_TOML],
            configured_providers={"audit": SYNTHETIC_PROVIDER_SENTINEL},
        )
        self.assertFalse(refuse_configure.activated)
        refuse_preuve = compose(
            [APP_TOML],
            attestations=[_preuve_ephemere_sentinelle()],
        )
        self.assertFalse(refuse_preuve.activated)
        sorties = []
        for result in (refuse_configure, refuse_preuve):
            sorties.extend(str(d) for d in result.diagnostics)
            sorties.extend(str(w) for w in result.warnings)
            sorties.append(repr(result))
        texte = "\n".join(sorties)
        for sentinelle in (
            SYNTHETIC_PROVIDER_SENTINEL,
            SYNTHETIC_PROOF_SENTINEL,
        ):
            self.assertNotIn(
                sentinelle, texte, f"écho de sentinelle : {sentinelle}"
            )


if __name__ == "__main__":
    unittest.main()
