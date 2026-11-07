"""Suite TEST présentation pré-confirmation E5, source seule non exécutée.
Graphes cohérents immuables par APIs publiques fixture.
Preuves synthétiques opaques, aucune autorité, fraîcheur, transport ou PG prouvés.
"""
from __future__ import annotations

import dataclasses
import json
import unittest
from unittest import mock

from pixs.backend.installation.planning_bundle import (
    PlanningBundleError,
    dump_planning_bundle,
)
from pixs.backend.installation.postgresql_confirmation import (
    ConfirmationError,
    dump_confirmation,
)
from pixs.backend.installation.pre_confirmation_presentation import (
    PresentationError,
    present_for_confirmation,
)

import c08_e5_fixtures


def _j(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


class PreConfirmationPresentationTest(unittest.TestCase):
    def test_reuse_affiche_actions_et_effets_vides_explicites(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-reuse-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        texte = present_for_confirmation(
            bundle_raw=bundle_raw,
            confirmation_raw=None,
            bundle_limits=graph.limits.bundle_limits,
            confirmation_limits=None,
        )
        self.assertIn(
            "portée=documents présentés sans preuve de provenance",
            texte,
        )
        self.assertIn(
            "action service=" + _j(graph.projection.service.action), texte
        )
        self.assertIn(
            "référence service=" + _j(graph.projection.service.ref), texte
        )
        self.assertIn(
            "action rôle=" + _j(graph.projection.role.action), texte
        )
        self.assertIn(
            "action base=" + _j(graph.projection.database.action), texte
        )
        self.assertIn("effets ordonnés=[]", texte)
        self.assertIn("conditions préconditions=[]", texte)
        self.assertIn("confirmation fournie=aucune", texte)

    def test_reuse_affiche_cinq_gardes(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-reuse-02")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        texte = present_for_confirmation(
            bundle_raw=bundle_raw,
            confirmation_raw=None,
            bundle_limits=graph.limits.bundle_limits,
            confirmation_limits=None,
        )
        self.assertEqual(texte.count("garde espèce="), 5)
        for garde in graph.preconditions.resource_guards:
            self.assertIn("garde référence=" + _j(garde.resource_ref), texte)

    def test_differe_conserve_unobservable_et_conditions(self) -> None:
        graph = c08_e5_fixtures.make_deferred_graph("pres-diff-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        texte = present_for_confirmation(
            bundle_raw=bundle_raw,
            confirmation_raw=None,
            bundle_limits=graph.limits.bundle_limits,
            confirmation_limits=None,
        )
        self.assertIn("action service=" + _j("START_EXISTING"), texte)
        self.assertIn("observation état=" + _j("UNOBSERVABLE"), texte)
        self.assertIn(
            "observation correspondance=" + _j("UNDETERMINED"), texte
        )
        self.assertIn(
            "effets ordonnés="
            + '["SERVICE_START","ROLE_CREATE","DATABASE_CREATE"]',
            texte,
        )
        pos_service = texte.index("effet=" + _j("SERVICE_START"))
        pos_role = texte.index("effet=" + _j("ROLE_CREATE"))
        pos_base = texte.index("effet=" + _j("DATABASE_CREATE"))
        self.assertLess(pos_service, pos_role)
        self.assertLess(pos_role, pos_base)

    def test_sans_confirmation_n_exige_pas_limite_confirmation(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-noconf-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        texte = present_for_confirmation(
            bundle_raw=bundle_raw,
            confirmation_raw=None,
            bundle_limits=graph.limits.bundle_limits,
            confirmation_limits=None,
        )
        self.assertIn("confirmation fournie=aucune", texte)
        self.assertNotIn("confirmation référence=", texte)

    def test_confirmation_rapprochee_valide_seulement(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-ok-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        confirmation_raw = dump_confirmation(
            graph.confirmation, graph.limits.confirmation_limits
        )
        texte = present_for_confirmation(
            bundle_raw=bundle_raw,
            confirmation_raw=confirmation_raw,
            bundle_limits=graph.limits.bundle_limits,
            confirmation_limits=graph.limits.confirmation_limits,
        )
        self.assertIn(
            "confirmation fournie=données rapprochées seulement", texte
        )
        self.assertIn(
            "confirmation référence="
            + _j(graph.confirmation.confirmation_ref),
            texte,
        )
        self.assertIn(
            "confirmation installation="
            + _j(graph.confirmation.installation_ref),
            texte,
        )

    def test_confirmation_divergente_refusee_apres_preuves_isolees(self) -> None:
        graph_a = c08_e5_fixtures.make_reuse_graph("pres-div-a01")
        graph_b = c08_e5_fixtures.make_reuse_graph("pres-div-b01")
        bundle_raw_a = dump_planning_bundle(
            graph_a.bundle, graph_a.limits.bundle_limits
        )
        confirmation_raw_a = dump_confirmation(
            graph_a.confirmation, graph_a.limits.confirmation_limits
        )
        bundle_raw_b = dump_planning_bundle(
            graph_b.bundle, graph_b.limits.bundle_limits
        )
        confirmation_raw_b = dump_confirmation(
            graph_b.confirmation, graph_b.limits.confirmation_limits
        )
        texte_a = present_for_confirmation(
            bundle_raw=bundle_raw_a,
            confirmation_raw=confirmation_raw_a,
            bundle_limits=graph_a.limits.bundle_limits,
            confirmation_limits=graph_a.limits.confirmation_limits,
        )
        self.assertIn("confirmation fournie=données rapprochées", texte_a)
        texte_b = present_for_confirmation(
            bundle_raw=bundle_raw_b,
            confirmation_raw=confirmation_raw_b,
            bundle_limits=graph_b.limits.bundle_limits,
            confirmation_limits=graph_b.limits.confirmation_limits,
        )
        self.assertIn("confirmation fournie=données rapprochées", texte_b)
        with self.assertRaises(PresentationError) as ctx:
            present_for_confirmation(
                bundle_raw=bundle_raw_a,
                confirmation_raw=confirmation_raw_b,
                bundle_limits=graph_a.limits.bundle_limits,
                confirmation_limits=graph_a.limits.confirmation_limits,
            )
        self.assertEqual(str(ctx.exception), "présentation refusée.")
        self.assertIsInstance(ctx.exception.__cause__, ConfirmationError)

    def test_confirmation_fournie_sans_limite_refusee(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-nolimit-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        confirmation_raw = dump_confirmation(
            graph.confirmation, graph.limits.confirmation_limits
        )
        with self.assertRaises(PresentationError) as ctx:
            present_for_confirmation(
                bundle_raw=bundle_raw,
                confirmation_raw=confirmation_raw,
                bundle_limits=graph.limits.bundle_limits,
                confirmation_limits=None,
            )
        self.assertEqual(str(ctx.exception), "présentation refusée.")
        self.assertIsNone(ctx.exception.__cause__)

    def test_bundle_ref_valide_c1_csi_bidi_echappee(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-inj-01")
        injectee = (
            "br-" + chr(133) + "-" + chr(155) + "-"
            + chr(8232) + "-" + chr(8234) + "-x"
        )
        mute = dataclasses.replace(graph.bundle, bundle_ref=injectee)
        mute_raw = dump_planning_bundle(mute, graph.limits.bundle_limits)
        texte = present_for_confirmation(
            bundle_raw=mute_raw,
            confirmation_raw=None,
            bundle_limits=graph.limits.bundle_limits,
            confirmation_limits=None,
        )
        attendu = _j(injectee)
        self.assertIn("bundle référence=" + attendu, texte)
        self.assertNotIn(chr(133), texte)
        self.assertNotIn(chr(155), texte)
        self.assertNotIn(chr(8232), texte)
        self.assertNotIn(chr(8234), texte)
        self.assertIn("\\u0085", texte)
        self.assertIn("\\u009b", texte)
        self.assertIn("\\u2028", texte)
        self.assertIn("\\u202a", texte)

    def test_bundle_ref_esc_rejetee_via_entree_wire(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-esc-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        doc = json.loads(bundle_raw.decode("utf-8"))
        doc["bundle_ref"] = "br-" + chr(27) + "-x"
        wire = json.dumps(
            doc,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        with self.assertRaises(PresentationError) as ctx:
            present_for_confirmation(
                bundle_raw=wire,
                confirmation_raw=None,
                bundle_limits=graph.limits.bundle_limits,
                confirmation_limits=None,
            )
        self.assertEqual(str(ctx.exception), "présentation refusée.")
        self.assertIsInstance(ctx.exception.__cause__, PlanningBundleError)

    def test_bundle_corrompu_erreur_fixe_sans_fuite(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-err-01")
        marqueur = "TEST_MARQUEUR_INVALIDE_987"
        with self.assertRaises(PresentationError) as ctx:
            present_for_confirmation(
                bundle_raw=marqueur.encode("utf-8"),
                confirmation_raw=None,
                bundle_limits=graph.limits.bundle_limits,
                confirmation_limits=None,
            )
        self.assertEqual(str(ctx.exception), "présentation refusée.")
        self.assertIsInstance(ctx.exception.__cause__, PlanningBundleError)
        self.assertNotIn(marqueur, str(ctx.exception))

    def test_inattendue_frontiere_codec_non_masquee(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-unexp-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        with mock.patch(
            "pixs.backend.installation.pre_confirmation_presentation.parse_planning_bundle",
            side_effect=RuntimeError("panne-inattendue"),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                present_for_confirmation(
                    bundle_raw=bundle_raw,
                    confirmation_raw=None,
                    bundle_limits=graph.limits.bundle_limits,
                    confirmation_limits=None,
                )
            self.assertEqual(str(ctx.exception), "panne-inattendue")

    def test_borne_deleguee_limite_trop_petite_refusee(self) -> None:
        graph = c08_e5_fixtures.make_reuse_graph("pres-born-01")
        bundle_raw = dump_planning_bundle(
            graph.bundle, graph.limits.bundle_limits
        )
        petites = dataclasses.replace(
            graph.limits.bundle_limits, max_bundle_bytes=1
        )
        with self.assertRaises(PresentationError) as ctx:
            present_for_confirmation(
                bundle_raw=bundle_raw,
                confirmation_raw=None,
                bundle_limits=petites,
                confirmation_limits=None,
            )
        self.assertEqual(str(ctx.exception), "présentation refusée.")
        self.assertIsInstance(ctx.exception.__cause__, PlanningBundleError)


if __name__ == "__main__":
    unittest.main()
