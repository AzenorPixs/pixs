"""Tests unitaires des primitives d'identité des composants (tâche 2.4)."""

import unittest

from pixs.kernel.manifest.models import ComponentManifest
from pixs.kernel.registry.identity import check_component_identities


def _manifest(component_id: str) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version="1.0.0",
    )


USURPED_ID = "pixs.marqueur-ne-doit-pas-apparaitre"


class TestReservationNamespace(unittest.TestCase):
    def test_usurpation_pixs_hors_officiel_refusee_sans_refleter_la_valeur(
        self,
    ) -> None:
        diagnostics = check_component_identities(
            [_manifest("acme.demo"), _manifest(USURPED_ID)],
            official_ids=(),
        )
        self.assertTrue(
            any("réservé" in d for d in diagnostics),
            f"aucun diagnostic de namespace réservé : {diagnostics}",
        )
        for diagnostic in diagnostics:
            self.assertNotIn(USURPED_ID, diagnostic)

    def test_composition_officielle_valide_sans_diagnostic(self) -> None:
        diagnostics = check_component_identities(
            [_manifest("pixs.core"), _manifest("acme.crm")],
            official_ids=("pixs.core",),
        )
        self.assertEqual(diagnostics, [])


class TestCollisionsIdentifiants(unittest.TestCase):
    def test_collision_de_deux_identifiants_dupliques_refusee(self) -> None:
        diagnostics = check_component_identities(
            [_manifest("acme.dup"), _manifest("acme.dup")]
        )
        self.assertTrue(
            any(
                "dupliqué" in d and "acme.dup" in d for d in diagnostics
            ),
            f"aucun diagnostic nommant l'identifiant dupliqué : {diagnostics}",
        )

    def test_identifiants_distincts_sans_diagnostic(self) -> None:
        diagnostics = check_component_identities(
            [_manifest("acme.one"), _manifest("acme.two")]
        )
        self.assertEqual(diagnostics, [])


if __name__ == "__main__":
    unittest.main()
