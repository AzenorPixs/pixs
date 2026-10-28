"""Unités cycle de vie §§7.2–7.8, écrites seulement."""

from __future__ import annotations

import datetime
import json
import unittest

from pixs.pzt_ca.ca_lifecycle import (
    CaLifecycleError,
    check_migration_common_plan_fields,
    inventory_from_mapping,
    loss_from_mapping,
    migration_from_mapping,
    observation_from_mapping,
    rotation_from_mapping,
    state_from_mapping,
    succession_from_mapping,
    succession_upper_bound,
)

_DEADLINE = "2026-11-22T09:00:00Z"
_ANCHOR = "2026-11-12T09:00:00Z"
_ENGAGED = "2026-10-23T09:00:00Z"
_WITHDRAW = "2026-11-01T09:00:00Z"
_RETIRED = "2026-11-02T09:00:00Z"
_DETECTED = "2026-10-23T08:00:00Z"


def _inventory() -> dict:
    return {
        "object_type": "z12.ca_inventory/v1",
        "schema_version": "1.0.0",
        "inventory_id": "inv-1",
        "domain": "dom-1",
        "epoch": 3,
        "inventory_version": "invv-1",
        "issuer_refs": [],
        "generation_refs": ["gen-1"],
        "cert_refs": [],
        "anchor_refs": ["anc-1"],
        "engagement_ref": "eng-1",
    }


def _state() -> dict:
    return {
        "object_type": "z12.ca_state/v1",
        "schema_version": "1.0.0",
        "state_id": "st-1",
        "domain": "dom-1",
        "epoch": 3,
        "state_version": "stv-1",
        "admitted_issuer_refs": ["iss-1"],
        "active_generation_refs": ["gen-1"],
        "withdrawn_generation_refs": ["gen-0"],
        "anchor_refs": ["anc-1"],
        "anchor_status": "current_only",
        "current_decision_ref": "dec-1",
        "engagement_ref": "eng-1",
    }


def _rotation(status: str = "prepared") -> dict:
    base = {
        "object_type": "z12.ca_rotation/v1",
        "schema_version": "1.0.0",
        "plan_ref": "plan-1",
        "plan_version": "v1",
        "context_ref": "ctx-1",
        "domain": "dom-1",
        "logical_authority": "aut-1",
        "emission_scope": "scope-1",
        "issuer_ref": "iss-1",
        "from_generation_ref": "gen-0",
        "to_generation_ref": "gen-1",
        "offline_procedure_ref": "off-1",
        "deadline_utc": _DEADLINE,
        "status": status,
    }
    if status in ("engaged", "withdrawn"):
        base.update({
            "engaged_at_utc": _ENGAGED,
            "engagement_ref": "eng-1",
            "exclusion_proof_ref": "exc-1",
        })
    if status == "withdrawn":
        base["withdrawn_at_utc"] = _RETIRED
    return base


def _loss(state: str = "detected") -> dict:
    base = {
        "object_type": "z12.ca_loss/v1",
        "schema_version": "1.0.0",
        "loss_id": "loss-1",
        "incident_version": "v1",
        "context_ref": "ctx-1",
        "issuer_ref": "iss-1",
        "lost_generation_ref": "gen-0",
        "loss_class": "lost",
        "detected_at_utc": _DETECTED,
        "recovery_state": state,
    }
    if state in ("recertification_pending", "reconciled"):
        base["offline_procedure_ref"] = "off-1"
    if state == "reconciled":
        base["reconciliation_ref"] = "rec-1"
    return base


def _succession(status: str = "prepared") -> dict:
    base = {
        "object_type": "z12.ca_succession/v1",
        "schema_version": "1.0.0",
        "plan_ref": "plan-s-1",
        "plan_version": "v1",
        "context_ref": "ctx-1",
        "domain": "dom-1",
        "scope_ref": "scope-1",
        "from_root_ref": "root-0",
        "to_root_ref": "root-1",
        "offline_procedure_ref": "off-1",
        "deadline_utc": _DEADLINE,
        "anchor_bound_at_utc": _ANCHOR,
        "status": status,
    }
    if status in ("engaged", "withdrawn"):
        base.update({
            "engaged_at_utc": _ENGAGED,
            "withdraw_at_utc": _WITHDRAW,
            "engagement_ref": "eng-1",
        })
    if status == "withdrawn":
        base["withdrawn_at_utc"] = _RETIRED
    return base


def _migration() -> dict:
    return {
        "object_type": "z12.ca_migration/v1",
        "schema_version": "1.0.0",
        "migration_id": "mig-1",
        "succession_plan_ref": "plan-s-1",
        "plan_version": "v1",
        "domain": "dom-1",
        "scope_ref": "scope-1",
        "from_anchor_ref": "anc-0",
        "to_anchor_ref": "anc-1",
        "engagement_ref": "eng-1",
        "engaged_at_utc": _ENGAGED,
        "withdraw_at_utc": _WITHDRAW,
        "anchor_bound_at_utc": _ANCHOR,
        "applied_observation_refs": [],
        "status": "prepared",
    }


def _observation() -> dict:
    return {
        "object_type": "z12.ca_application_observation/v1",
        "schema_version": "1.0.0",
        "observation_id": "obs-1",
        "association_ref": "pa-1",
        "plan_ref": "plan-s-1",
        "plan_version": "v1",
        "domain": "dom-1",
        "scope_ref": "scope-1",
        "target_anchor_ref": "anc-1",
        "target_generation_ref": "gen-1",
        "observed_at_utc": _ENGAGED,
        "applied_proof_ref": "proof-1",
        "epoch": 3,
    }


class InventoryStateTest(unittest.TestCase):
    def test_inventaire_vide_admis_sans_doublon(self) -> None:
        dec = inventory_from_mapping(_inventory())
        self.assertEqual(dec.issuer_refs, ())
        with self.assertRaises(CaLifecycleError):
            bad = _inventory()
            bad["issuer_refs"] = ["a", "a"]
            inventory_from_mapping(bad)

    def test_etat_disjoint_et_plan_coexistence(self) -> None:
        dec = state_from_mapping(_state())
        self.assertEqual(dec.anchor_status, "current_only")
        bad = _state()
        bad["active_generation_refs"] = ["gen-x"]
        bad["withdrawn_generation_refs"] = ["gen-x"]
        with self.assertRaises(CaLifecycleError):
            state_from_mapping(bad)
        need = _state()
        need["anchor_status"] = "coexistence_admitted"
        with self.assertRaises(CaLifecycleError):
            state_from_mapping(need)
        need["succession_plan_ref"] = "plan-s-1"
        dec2 = state_from_mapping(need)
        self.assertEqual(dec2.succession_plan_ref, "plan-s-1")


class RotationLossTest(unittest.TestCase):
    def test_rotation_phases(self) -> None:
        for statut in ("prepared", "engaged", "withdrawn"):
            with self.subTest(statut=statut):
                dec = rotation_from_mapping(_rotation(statut))
                self.assertEqual(dec.status, statut)
        with self.assertRaises(CaLifecycleError):
            bad = _rotation("prepared")
            bad["engaged_at_utc"] = _ENGAGED
            rotation_from_mapping(bad)
        with self.assertRaises(CaLifecycleError):
            bad = _rotation("engaged")
            del bad["exclusion_proof_ref"]
            rotation_from_mapping(bad)

    def test_generation_identique_refusee(self) -> None:
        bad = _rotation("prepared")
        bad["to_generation_ref"] = "gen-0"
        with self.assertRaises(CaLifecycleError):
            rotation_from_mapping(bad)

    def test_perte_optionnelle_et_conditions(self) -> None:
        dec = loss_from_mapping(_loss("detected"))
        self.assertIsNone(dec.replacement_generation_ref)
        with_repl = _loss("detected")
        with_repl["replacement_generation_ref"] = "gen-9"
        dec2 = loss_from_mapping(with_repl)
        self.assertEqual(dec2.replacement_generation_ref, "gen-9")
        admis = _loss("detected")
        admis["offline_procedure_ref"] = "off-1"
        dec_off = loss_from_mapping(admis)
        self.assertEqual(dec_off.offline_procedure_ref, "off-1")
        with self.assertRaises(CaLifecycleError):
            bad = _loss("recertification_pending")
            del bad["offline_procedure_ref"]
            loss_from_mapping(bad)
        dec3 = loss_from_mapping(_loss("reconciled"))
        self.assertEqual(dec3.recovery_state, "reconciled")


class SuccessionMigrationTest(unittest.TestCase):
    def test_succession_phases_et_borne(self) -> None:
        for statut in ("prepared", "engaged", "withdrawn"):
            with self.subTest(statut=statut):
                dec = succession_from_mapping(_succession(statut))
                self.assertEqual(dec.status, statut)
        with self.assertRaises(CaLifecycleError):
            bad = _succession("prepared")
            bad["engaged_at_utc"] = _ENGAGED
            succession_from_mapping(bad)
        with self.assertRaises(CaLifecycleError):
            bad = _succession("engaged")
            bad["to_root_ref"] = "root-0"
            succession_from_mapping(bad)

    def test_borne_reutilise_durations_sans_flottant(self) -> None:
        dec = succession_from_mapping(_succession("engaged"))
        borne = succession_upper_bound(dec)
        self.assertTrue(isinstance(borne, datetime.datetime))
        self.assertLessEqual(dec.withdraw_at_utc, borne)
        bad = _succession("engaged")
        bad["withdraw_at_utc"] = "2026-12-31T09:00:00Z"
        with self.assertRaises(CaLifecycleError):
            succession_from_mapping(bad)

    def test_migration_requise_memeprepared_et_rattachement(self) -> None:
        mig = migration_from_mapping(_migration())
        self.assertEqual(mig.status, "prepared")
        suc = succession_from_mapping(_succession("engaged"))
        check_migration_common_plan_fields(mig, suc)
        import dataclasses

        autre = dataclasses.replace(mig, plan_version="v2")
        with self.assertRaises(CaLifecycleError):
            check_migration_common_plan_fields(autre, suc)
        with self.assertRaises(CaLifecycleError):
            tard = dataclasses.replace(
                mig, withdraw_at_utc=datetime.datetime(2026, 12, 31, 9, 0, 0, tzinfo=datetime.timezone.utc)
            )
            check_migration_common_plan_fields(tard, suc)

    def test_observation_epoch_exacte(self) -> None:
        dec = observation_from_mapping(_observation())
        self.assertEqual(dec.epoch, 3)
        bad = _observation()
        bad["epoch"] = True
        with self.assertRaises(CaLifecycleError):
            observation_from_mapping(bad)

    def test_sans_verification_ni_x509(self) -> None:
        import pixs.pzt_ca.ca_lifecycle as module

        self.assertFalse(hasattr(module, "is_verified"))
        self.assertFalse(hasattr(module, "verify_signature"))


class LifecycleExtraCoverageTest(unittest.TestCase):
    def test_all_seven_parsers_valides(self) -> None:
        from pixs.pzt_ca.ca_lifecycle import inventory_from_mapping, observation_from_mapping, state_from_mapping
        for fabrique in (_inventory, _state, _rotation, _loss, _succession, _migration, _observation):
            with self.subTest(fabrique=fabrique.__name__):
                base = fabrique()
                if fabrique is _inventory:
                    dec = inventory_from_mapping(base)
                    self.assertEqual(dec.inventory_id, "inv-1")
                elif fabrique is _state:
                    dec = state_from_mapping(base)
                    self.assertEqual(dec.state_id, "st-1")
                elif fabrique is _rotation:
                    from pixs.pzt_ca.ca_lifecycle import rotation_from_mapping
                    dec = rotation_from_mapping(base)
                    self.assertEqual(dec.plan_ref, "plan-1")
                elif fabrique is _loss:
                    from pixs.pzt_ca.ca_lifecycle import loss_from_mapping
                    dec = loss_from_mapping(base)
                    self.assertEqual(dec.loss_id, "loss-1")
                elif fabrique is _succession:
                    from pixs.pzt_ca.ca_lifecycle import succession_from_mapping
                    dec = succession_from_mapping(base)
                    self.assertEqual(dec.plan_ref, "plan-s-1")
                elif fabrique is _migration:
                    from pixs.pzt_ca.ca_lifecycle import migration_from_mapping
                    dec = migration_from_mapping(base)
                    self.assertEqual(dec.migration_id, "mig-1")
                else:
                    dec = observation_from_mapping(base)
                    self.assertEqual(dec.observation_id, "obs-1")

    def test_negatifs_couvrent_les_sept_parsers(self) -> None:
        from pixs.pzt_ca.ca_lifecycle import inventory_from_json, inventory_from_mapping, loss_from_json, loss_from_mapping, migration_from_json, migration_from_mapping, observation_from_json, observation_from_mapping, rotation_from_json, rotation_from_mapping, state_from_json, state_from_mapping, succession_from_json, succession_from_mapping

        class EvilEq:
            def __eq__(self, other: object) -> bool:
                raise AssertionError("appele")

        table = [(_inventory, inventory_from_mapping, inventory_from_json), (_state, state_from_mapping, state_from_json), (_rotation, rotation_from_mapping, rotation_from_json), (_loss, loss_from_mapping, loss_from_json), (_succession, succession_from_mapping, succession_from_json), (_migration, migration_from_mapping, migration_from_json), (_observation, observation_from_mapping, observation_from_json)]
        for fabrique, parse_map, parse_json in table:
            with self.subTest(parser=parse_map.__name__):
                with self.assertRaises(CaLifecycleError):
                    parse_map({"faux": "objet"})
                complet = fabrique()
                complet["champ_inconnu_xyz"] = "x"
                with self.assertRaises(CaLifecycleError):
                    parse_map(complet)
                mauvais = fabrique()
                mauvais["schema_version"] = "9.9.9"
                with self.assertRaises(CaLifecycleError):
                    parse_map(mauvais)
                mauvais = fabrique()
                cle_nulle = next(k for k in list(mauvais.keys()) if k not in ("object_type", "schema_version"))
                mauvais[cle_nulle] = None
                with self.assertRaises(CaLifecycleError):
                    parse_map(mauvais)
                mauvais = fabrique()
                mauvais["object_type"] = EvilEq()
                with self.assertRaises(CaLifecycleError):
                    parse_map(mauvais)
                with self.assertRaises(CaLifecycleError):
                    parse_json('{"a": 1, "a": 2}')

    def test_alias_listes_immuables_et_dates_naives(self) -> None:
        import dataclasses
        base = _inventory()
        lst = ["gen-1"]
        base["generation_refs"] = lst
        dec = inventory_from_mapping(base)
        lst.append("gen-2")
        self.assertEqual(dec.generation_refs, ("gen-1",))
        rot = rotation_from_mapping(_rotation("engaged"))
        naive = datetime.datetime(2026, 10, 23, 9, 0, 0)
        with self.assertRaises(CaLifecycleError):
            dataclasses.replace(rot, deadline_utc=naive)

    def test_bornes_exactes_et_plus_une_microseconde(self) -> None:
        import dataclasses
        suc = succession_from_mapping(_succession("engaged"))
        borne = succession_upper_bound(suc)
        exact = dataclasses.replace(suc, withdraw_at_utc=borne)
        self.assertEqual(exact.withdraw_at_utc, borne)
        apres = borne + datetime.timedelta(microseconds=1)
        with self.assertRaises(CaLifecycleError):
            succession_from_mapping({**_succession("engaged"), "withdraw_at_utc": apres.isoformat().replace("+00:00", "Z")})

    def test_mismatch_engagement_commun(self) -> None:
        import dataclasses
        from pixs.pzt_ca.ca_lifecycle import check_migration_common_plan_fields
        mig = migration_from_mapping(_migration())
        suc = succession_from_mapping(_succession("engaged"))
        autre = dataclasses.replace(mig, engagement_ref="eng-autre")
        with self.assertRaises(CaLifecycleError) as releve:
            check_migration_common_plan_fields(autre, suc)
        self.assertEqual(releve.exception.code, "ENGAGEMENT_INCOHERENT")

    def test_perte_blocked_conserve_refs_sans_permission(self) -> None:
        base = _loss("blocked")
        base["offline_procedure_ref"] = "off-passe"
        base["reconciliation_ref"] = "rec-passee"
        base["replacement_generation_ref"] = "gen-9"
        dec = loss_from_mapping(base)
        self.assertEqual(dec.recovery_state, "blocked")
        self.assertEqual(dec.replacement_generation_ref, "gen-9")


class LifecycleChronologyIndependenceExtraTest(unittest.TestCase):
    def test_rotation_engaged_egal_deadline_refuse(self) -> None:
        import dataclasses
        base = rotation_from_mapping(_rotation("engaged"))
        with self.assertRaises(CaLifecycleError):
            dataclasses.replace(base, deadline_utc=base.engaged_at_utc)

    def test_succession_chronologie_et_retrait_tardif_representable(self) -> None:
        import dataclasses
        suc = succession_from_mapping(_succession("engaged"))
        with self.assertRaises(CaLifecycleError):
            dataclasses.replace(suc, withdraw_at_utc=suc.engaged_at_utc)
        tardif = dataclasses.replace(suc, status="withdrawn", withdrawn_at_utc=datetime.datetime(2027, 6, 1, 9, 0, 0, tzinfo=datetime.timezone.utc))
        self.assertEqual(tardif.withdrawn_at_utc.year, 2027)
        with self.assertRaises(CaLifecycleError):
            dataclasses.replace(suc, status="withdrawn", withdrawn_at_utc=datetime.datetime(2026, 1, 1, 9, 0, 0, tzinfo=datetime.timezone.utc))

    def test_migration_chronologie_refusee(self) -> None:
        import dataclasses
        mig = migration_from_mapping(_migration())
        with self.assertRaises(CaLifecycleError):
            dataclasses.replace(mig, withdraw_at_utc=mig.engaged_at_utc)

    def test_bornes_exactes_et_plus_une_microseconde(self) -> None:
        suc = succession_from_mapping(_succession("engaged"))
        borne = succession_upper_bound(suc)
        self.assertLessEqual(suc.withdraw_at_utc, borne)
        with self.assertRaises(CaLifecycleError):
            succession_from_mapping({**_succession("engaged"), "withdraw_at_utc": (borne + datetime.timedelta(microseconds=1)).isoformat().replace("+00:00", "Z")})

    def test_egalites_exactes_refusees(self) -> None:
        with self.assertRaises(CaLifecycleError):
            bad = _loss("detected")
            bad["replacement_generation_ref"] = bad["lost_generation_ref"]
            loss_from_mapping(bad)
        with self.assertRaises(CaLifecycleError):
            bad = _migration()
            bad["to_anchor_ref"] = bad["from_anchor_ref"]
            migration_from_mapping(bad)

    def test_sets_dupliques_et_alias(self) -> None:
        bad = _inventory()
        bad["issuer_refs"] = ["a", "a"]
        with self.assertRaises(CaLifecycleError):
            inventory_from_mapping(bad)
        base = _inventory()
        lst = ["gen-1"]
        base["generation_refs"] = lst
        dec = inventory_from_mapping(base)
        lst.append("gen-2")
        self.assertEqual(dec.generation_refs, ("gen-1",))
        bad = _state()
        bad["active_generation_refs"] = ["x", "x"]
        with self.assertRaises(CaLifecycleError):
            state_from_mapping(bad)
        bad = _migration()
        bad["applied_observation_refs"] = ["o1", "o1"]
        with self.assertRaises(CaLifecycleError):
            migration_from_mapping(bad)


if __name__ == "__main__":
    unittest.main()
