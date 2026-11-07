"""Recettes préconditions 1.0.0 : forme seule, préparées non exécutées."""
from __future__ import annotations
import hashlib
import json
import sys
from dataclasses import replace
import unittest

from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits
from pixs.pa_native.postgresql_contracts import ContractError as PGContractError
from pixs.pa_native import postgresql_preconditions as pre


def _limits(max_json=8192, max_ref=256, max_conditions=8):
    return pre.PreconditionsLimits(
        payload=PayloadLimits(
            max_json_bytes=max_json,
            max_ref_bytes=max_ref,
            max_observation_refs=8,
        ),
        max_conditions=max_conditions,
    )


def _binding(ref="p1", version="1.0.0"):
    return ContentBinding(ref=ref, version=version, sha256="0" * 64)


def _guard(kind, ref, pb_version="1.0.0"):
    return pre.ResourceGuard(
        kind=kind, resource_ref=ref,
        profile_binding=_binding(ref + "-pb", pb_version),
    )


def _base_manifest():
    return pre.PreconditionsManifest(
        schema="pixs.agent.postgresql.preconditions_manifest",
        schema_version="1.0.0",
        preconditions_ref="pre-1",
        installation_ref="inst-1",
        target_ref="tgt-1",
        operation_id="op-1",
        projection_binding=_binding("proj", "1.0.0"),
        observation_binding=_binding("obs", "1.0.0"),
        resource_guards=(
            _guard("SOFTWARE", "sw"),
            _guard("CLUSTER", "cl"),
            _guard("SERVICE", "se"),
            _guard("ROLE", "ro"),
            _guard("DATABASE", "db"),
        ),
        conditions=(),
    )


def _cond(ref="c-001", kind="SERVICE", rref="se", effect="SERVICE_START",
          stage="BEFORE_EFFECT", state="STOPPED", match="MATCH", ev="present"):
    return pre.PreconditionCondition(
        condition_ref=ref, resource_kind=kind, resource_ref=rref,
        profile_binding=_binding(rref + "-pb"),
        effect=effect, check_stage=stage,
        expected_state=state, expected_match=match,
        evidence_binding=_binding("ev") if ev == "present" else None,
    )


class PreconditionsFormTest(unittest.TestCase):
    def test_nominal_empty(self):
        m = _base_manifest()
        text = pre.encode_preconditions(m, _limits())
        self.assertEqual(pre.decode_preconditions(text, _limits()), m)

    def test_nominal_conditions_ordre_preserve(self):
        m = _base_manifest()
        c_b = _cond(ref="c-b")
        c_a = _cond(ref="c-a")
        with self.subTest(order="b,a"):
            m2 = replace(m, conditions=(c_b, c_a))
            text = pre.encode_preconditions(m2, _limits())
            back = pre.decode_preconditions(text, _limits())
            self.assertEqual([c.condition_ref for c in back.conditions], ["c-b", "c-a"])
            self.assertEqual(back, m2)

    def test_nominal_null_etroit_role_database(self):
        m = _base_manifest()
        for kind, eff, rref in (("ROLE", "ROLE_CREATE", "ro"),
                                ("DATABASE", "DATABASE_CREATE", "db")):
            with self.subTest(kind=kind):
                c = _cond(ref="c-" + kind, kind=kind, rref=rref, effect=eff,
                          stage="AFTER_SERVICE_START_BEFORE_EFFECT",
                          state="ABSENT", match="UNDETERMINED", ev=None)
                m2 = replace(m, conditions=(c,))
                text = pre.encode_preconditions(m2, _limits())
                self.assertEqual(pre.decode_preconditions(text, _limits()), m2)

    def test_digest_binding_engage_octets(self):
        m = replace(_base_manifest(), conditions=(_cond(),))
        lim = _limits()
        text = pre.encode_preconditions(m, lim)
        b = pre.preconditions_binding(m, lim)
        self.assertEqual(b.ref, "pre-1")
        self.assertEqual(b.version, "1.0.0")
        self.assertEqual(b.sha256, hashlib.sha256(text.encode("utf-8")).hexdigest())

    def test_refus_schema_version(self):
        m, lim = _base_manifest(), _limits()
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, schema_version="1.1.0")
            pre.encode_preconditions(bad, lim)

    def test_refus_versions_fixees(self):
        m, lim = _base_manifest(), _limits()
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, projection_binding=_binding("proj", "2.0.0"))
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, observation_binding=_binding("obs", "9.9.9"))
            pre.encode_preconditions(bad, lim)

    def test_versions_profils_opaques_admises(self):
        m, lim = _base_manifest(), _limits()
        guards = (
            _guard("SOFTWARE", "sw", "2.3.4"), _guard("CLUSTER", "cl", "opaque-v7"),
            _guard("SERVICE", "se", "1.0.0"), _guard("ROLE", "ro", "x"),
            _guard("DATABASE", "db", "99"),
        )
        m2 = replace(m, resource_guards=guards)
        self.assertEqual(pre.decode_preconditions(pre.encode_preconditions(m2, lim), lim), m2)

    def test_refus_guards(self):
        m, lim = _base_manifest(), _limits()
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, resource_guards=m.resource_guards[:4])
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, resource_guards=(
                _guard("CLUSTER", "cl"), _guard("SOFTWARE", "sw"),
                _guard("SERVICE", "se"), _guard("ROLE", "ro"),
                _guard("DATABASE", "db")))
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, resource_guards=(
                _guard("SOFTWARE", "sw"), _guard("SOFTWARE", "sw2"),
                _guard("SERVICE", "se"), _guard("ROLE", "ro"),
                _guard("DATABASE", "db")))
            pre.encode_preconditions(bad, lim)

    def test_refus_doublon_et_borne_conditions(self):
        m, lim = _base_manifest(), _limits()
        c = _cond(ref="c-dup")
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, conditions=(c, replace(c, resource_ref="se2")))
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, conditions=(c, _cond(ref="c-next")))
            pre.encode_preconditions(bad, _limits(max_conditions=1))

    def test_refus_null_elargi(self):
        with self.assertRaises(pre.PreconditionsContractError):
            _cond(ref="c-x", kind="SERVICE", rref="se", effect="SERVICE_START",
                  stage="AFTER_SERVICE_START_BEFORE_EFFECT",
                  state="UNOBSERVABLE", match="UNDETERMINED", ev=None)
        with self.assertRaises(pre.PreconditionsContractError):
            _cond(ref="c-y", kind="ROLE", rref="ro", effect="SERVICE_START",
                  stage="AFTER_SERVICE_START_BEFORE_EFFECT",
                  state="UNOBSERVABLE", match="UNDETERMINED", ev=None)
        with self.assertRaises(pre.PreconditionsContractError):
            _cond(ref="c-z", kind="ROLE", rref="ro", effect="ROLE_CREATE",
                  stage="BEFORE_EFFECT",
                  state="UNOBSERVABLE", match="UNDETERMINED", ev=None)

    def test_refus_bool_et_null_champs_connus(self):
        m, lim = _base_manifest(), _limits()
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, preconditions_ref=True)
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad_guard = pre.ResourceGuard(
                kind="SOFTWARE", resource_ref=True,
                profile_binding=_binding("x"))
            bad = replace(m, resource_guards=(
                bad_guard, _guard("CLUSTER", "cl"),
                _guard("SERVICE", "se"), _guard("ROLE", "ro"),
                _guard("DATABASE", "db")))
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, projection_binding=None)
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, conditions=(replace(_cond(), evidence_binding="ev"),))
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, conditions=(replace(_cond(), evidence_binding=None),))
            pre.encode_preconditions(bad, lim)

    def test_refus_mutables_et_null(self):
        m, lim = _base_manifest(), _limits()
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, conditions=[_cond()])
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, resource_guards=list(m.resource_guards))
            pre.encode_preconditions(bad, lim)
        with self.assertRaises(pre.PreconditionsContractError):
            bad = replace(m, preconditions_ref=None)
            pre.encode_preconditions(bad, lim)

    def test_refus_json_nombres_bool_inconnu(self):
        lim = _limits()
        for text in ('{"a": 1}', '{"a": 1.5}', '{"a": NaN}',
                     '{"a": true}', '{"a": null}'):
            with self.subTest(text=text):
                with self.assertRaises(pre.PreconditionsContractError):
                    pre.decode_preconditions(text, lim)

    def test_refus_json_doublons(self):
        lim = _limits()
        with self.assertRaises(pre.PreconditionsContractError):
            pre.decode_preconditions('{"schema": "a", "schema": "b"}', lim)
        m = _base_manifest()
        text = pre.encode_preconditions(m, lim)
        obj = json.loads(text)
        obj["resource_guards"][0]["kind"] = "SOFTWARE"
        obj["resource_guards"][0]["extra"] = "x"
        with self.assertRaises(pre.PreconditionsContractError):
            pre.decode_preconditions(json.dumps(obj), lim)
        obj2 = json.loads(text)
        obj2["projection_binding"]["extra_nested"] = 1
        with self.assertRaises(pre.PreconditionsContractError):
            pre.decode_preconditions(json.dumps(obj2), lim)
        obj3 = json.loads(text)
        obj3["unexpected_top"] = 1
        with self.assertRaises(pre.PreconditionsContractError):
            pre.decode_preconditions(json.dumps(obj3), lim)

    def test_seuils_exact_et_depassement_utf8(self):
        m = _base_manifest()
        lim_wide = _limits()
        text = pre.encode_preconditions(m, lim_wide)
        n = len(text.encode("utf-8"))
        lim_exact = _limits(max_json=n)
        self.assertEqual(
            pre.decode_preconditions(
                pre.encode_preconditions(m, lim_exact), lim_exact), m)
        lim_minus = _limits(max_json=n - 1)
        with self.assertRaises(pre.PreconditionsContractError):
            pre.encode_preconditions(m, lim_minus)
        with self.assertRaises(pre.PreconditionsContractError):
            pre.decode_preconditions(text, lim_minus)
        lim6 = _limits(max_ref=6)
        ok_guard = pre.ResourceGuard(
            kind="SOFTWARE", resource_ref="ééé",
            profile_binding=_binding("pb"))
        m2 = replace(m, resource_guards=(
            ok_guard, _guard("CLUSTER", "cl"),
            _guard("SERVICE", "se"), _guard("ROLE", "ro"),
            _guard("DATABASE", "db")))
        self.assertEqual(
            pre.decode_preconditions(
                pre.encode_preconditions(m2, lim6), lim6), m2)
        with self.assertRaises(pre.PreconditionsContractError):
            bad_guard = pre.ResourceGuard(
                kind="SOFTWARE", resource_ref="éééé",
                profile_binding=_binding("pb"))
            bad = replace(m, resource_guards=(
                bad_guard, _guard("CLUSTER", "cl"),
                _guard("SERVICE", "se"), _guard("ROLE", "ro"),
                _guard("DATABASE", "db")))
            pre.encode_preconditions(bad, lim6)

    def test_refus_limites_invalides(self):
        good = _limits().payload
        for bad_max in (-1, 0, True, False, "8", 8.0, None):
            with self.subTest(bad=repr(bad_max)):
                with self.assertRaises(PGContractError):
                    PayloadLimits(max_json_bytes=bad_max, max_ref_bytes=256, max_observation_refs=8)
                with self.assertRaises(pre.PreconditionsContractError):
                    pre.PreconditionsLimits(payload=good, max_conditions=bad_max)
        with self.assertRaises(pre.PreconditionsContractError):
            pre.PreconditionsLimits(payload="not-limits", max_conditions=8)
        with self.assertRaises(pre.PreconditionsContractError):
            pre.PreconditionsLimits(payload=None, max_conditions=8)

    def test_reuse_pg_direct_et_contexte(self):
        self.assertIs(pre.PayloadLimits, PayloadLimits)
        self.assertIs(pre.ContentBinding, ContentBinding)
        import pathlib
        src = pathlib.Path(pre.__file__).read_text(encoding="utf-8")
        self.assertIn("PA01_PRECONDITIONS_CONTEXT_REFUSED", src)
        self.assertIn("PA01_PRECONDITIONS_PG_BUILTIN_MISSING", src)
        # Contexte étranger refusé par exec contrôlé, sans toucher au paquet réel.
        g = {"__package__": "etranger", "__name__": "pre_foreign"}
        with self.assertRaises(ImportError):
            exec(compile(src, pre.__file__, "exec"), g)
        # Chemin builtin absent : postgresql_contracts non builtin => ImportError attendu.
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        g2 = {"__package__": "", "__name__": "pre_flat"}
        with self.assertRaises(ImportError):
            exec(compile(src, pre.__file__, "exec"), g2)
        # Builtin compilé réel reste phase2 LXC, non revendiqué ici.


if __name__ == "__main__":
    unittest.main()
