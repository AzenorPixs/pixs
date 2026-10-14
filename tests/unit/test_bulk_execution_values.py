"""Tests unitaires purs des validateurs runtime Bulk v1 B02/B09.

Les cas proviennent des annexes approuvées BulkExecutionExtensionV1,
ProgressV1 et PolicyV1 : refus des types étrangers avant tout comportement,
contraintes croisées explicites et diagnostics statiques sans écho de valeur.
"""

import unittest
from datetime import datetime, timedelta, timezone, tzinfo
from unittest import mock

from pixs.backend import bulk_execution_values
from pixs.backend.bulk_execution_values import (
    validate_bulk_execution_values,
    validate_bulk_policy_values,
    validate_bulk_progress_values,
)
from pixs.kernel.bulk_operation_record_values import (
    validate_bulk_operation_record_values,
)
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest.semver import parse_version

_EXECUTION = "bulk_execution_values"
_PROGRESS = "bulk_progress_values"
_POLICY = "bulk_policy_values"

_RECORD_KEYS = (
    "operation_id",
    "bulk_type",
    "bulk_version",
    "status",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
)

_SHA_A = "0123456789abcdef" * 4
_SHA_B = "fedcba9876543210" * 4

_EXECUTION_STR_FIELDS = (
    "operation_id",
    "bulk_type",
    "bulk_version",
    "status",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
    "execution_version",
    "requested_by_reference",
    "resolved_context_reference",
    "mapping_reference",
    "mapping_version",
    "input_reference",
    "input_version",
    "input_sha256",
    "output_reference",
    "output_version",
    "output_sha256",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
    "idempotency_key",
    "correlation_id",
    "causation_id",
    "checkpoint_reference",
    "result_reference",
    "policy_reference",
    "policy_version",
)
_EXECUTION_INT_FIELDS = ("input_size_bytes", "output_size_bytes", "revision")

_PROGRESS_INT_FIELDS = (
    "total_rows",
    "validated_rows",
    "invalid_rows",
    "applied_rows",
    "execution_rejected_rows",
    "exported_rows",
)

_POLICY_INT_FIELDS = (
    "max_input_bytes",
    "max_rows",
    "max_row_bytes",
    "max_columns",
    "max_json_depth",
    "max_json_members",
    "max_diagnostics",
    "read_chunk_bytes",
    "chunk_rows",
    "max_attempts",
    "lease_seconds",
    "renewal_seconds",
    "publish_max_attempts",
    "publish_lease_seconds",
    "publish_renewal_seconds",
    "max_parallel_operations",
    "max_runtime_seconds",
    "replay_window_seconds",
    "idempotency_retention_seconds",
    "staging_retention_seconds",
    "result_retention_seconds",
    "max_download_url_seconds",
)

_LATE_EXPORT_STATES = ("READY", "RUNNING", "COMPLETED", "COMPLETED_WITH_ERRORS")
_EARLY_EXPORT_STATES = ("REQUESTED", "STAGED", "VALIDATING", "FAILED")


class _HostileMeta(type):
    def __eq__(cls, other):
        raise AssertionError("égalité de type étranger utilisée")

    def __hash__(cls):
        raise AssertionError("hash de type étranger utilisé")


class _ForeignDict(dict, metaclass=_HostileMeta):
    def items(self):
        raise AssertionError("items appelé sur une sous-classe dict refusée")

    def keys(self):
        raise AssertionError("keys appelé sur une sous-classe dict refusée")


class _ForeignList(list, metaclass=_HostileMeta):
    def __iter__(self):
        raise AssertionError("itération sur une sous-classe list refusée")


class _Boom:
    def __bool__(self):
        raise AssertionError("__bool__ utilisé")

    def __eq__(self, other):
        raise AssertionError("__eq__ utilisé")

    def __hash__(self):
        raise AssertionError("__hash__ utilisé")

    def __repr__(self):
        raise AssertionError("__repr__ utilisé")

    def __str__(self):
        raise AssertionError("__str__ utilisé")


class _HostileKey(str):
    hash_count = 0

    def __hash__(self):
        self.hash_count += 1
        if self.hash_count > 1:
            raise AssertionError("clé étrangère hachée avant la garde de type")
        return 0


class _StrSub(str):
    pass


class _IntSub(int):
    pass


class _DatetimeSub(datetime):
    @property
    def tzinfo(self):
        raise AssertionError("tzinfo consulté avant identité de type")


class _RaisingTz(tzinfo):
    def __eq__(self, other):
        raise AssertionError("égalité de tzinfo utilisée")

    def utcoffset(self, value):
        raise AssertionError("utcoffset étranger utilisé")

    def dst(self, value):
        raise AssertionError("dst étranger utilisé")

    def tzname(self, value):
        raise AssertionError("tzname étranger utilisé")


def _snapshot(value):
    if type(value) is dict:
        return {key: _snapshot(item) for key, item in value.items()}
    if type(value) is list:
        return [_snapshot(item) for item in value]
    return value


def _valid_progress():
    return {
        "total_rows": 10,
        "validated_rows": 8,
        "invalid_rows": 1,
        "applied_rows": 5,
        "execution_rejected_rows": 2,
        "exported_rows": 0,
    }


def _valid_execution_import():
    return {
        "operation_id": "operation-0001",
        "bulk_type": "IMPORT",
        "bulk_version": "1.0.0",
        "status": "STAGED",
        "tenant_context_reference": "tenant-0001",
        "scope_context_reference": "scope-0001",
        "format": "CSV",
        "conflict_strategy": "REJECT",
        "commit_mode": "ATOMIC_PER_CHUNK",
        "execution_version": "1.0.0",
        "requested_by_reference": "principal-0001",
        "resolved_context_reference": "context-0001",
        "mapping_reference": "mapping-0001",
        "mapping_version": "2.0.0",
        "input_reference": "input-0001",
        "input_version": "1.0.0",
        "input_sha256": _SHA_A,
        "input_size_bytes": 1024,
        "output_reference": None,
        "output_version": None,
        "output_sha256": None,
        "output_size_bytes": None,
        "projection_reference": None,
        "consistency_kind": None,
        "consistency_reference": None,
        "idempotency_key": "idem-0001",
        "correlation_id": "corr-0001",
        "causation_id": None,
        "progress": _valid_progress(),
        "checkpoint_reference": "checkpoint-0001",
        "result_reference": None,
        "expires_at": datetime(2026, 12, 31, tzinfo=timezone.utc),
        "policy_reference": "policy-0001",
        "policy_version": "3.0.0",
        "revision": 1,
        "cancellation_requested": False,
    }


def _valid_execution_export():
    candidate = _valid_execution_import()
    candidate.update(
        {
            "bulk_type": "EXPORT",
            "status": "READY",
            "conflict_strategy": None,
            "commit_mode": None,
            "input_reference": None,
            "input_version": None,
            "input_sha256": None,
            "input_size_bytes": None,
            "projection_reference": "projection-0001",
            "consistency_kind": "SNAPSHOT",
            "consistency_reference": "snapshot-0001",
            "causation_id": "cause-0001",
            "progress": {
                "total_rows": None,
                "validated_rows": 7,
                "invalid_rows": 2,
                "applied_rows": 0,
                "execution_rejected_rows": 0,
                "exported_rows": 5,
            },
        }
    )
    return candidate


def _valid_policy():
    return {
        "max_input_bytes": 1_048_576,
        "max_rows": 1_000_000,
        "max_row_bytes": 8_192,
        "max_columns": 64,
        "max_json_depth": 8,
        "max_json_members": 32,
        "max_diagnostics": 100,
        "read_chunk_bytes": 4_096,
        "chunk_rows": 500,
        "max_attempts": 3,
        "lease_seconds": 60,
        "renewal_seconds": 20,
        "publish_max_attempts": 1,
        "publish_lease_seconds": 50,
        "publish_renewal_seconds": 20,
        "max_parallel_operations": 2,
        "max_runtime_seconds": 3_600,
        "replay_window_seconds": 300,
        "idempotency_retention_seconds": 600,
        "staging_retention_seconds": 900,
        "result_retention_seconds": 1_200,
        "max_download_url_seconds": 60,
        "retry_delays_seconds": [1, 2],
        "publish_retry_delays_seconds": [],
    }


class _GuardMixin:
    scope = ""

    def factory(self):
        raise NotImplementedError

    def validate(self, candidate):
        raise NotImplementedError

    def assert_shape(self, diags):
        self.assertIsInstance(diags, list)
        for item in diags:
            self.assertIsInstance(item, Diagnostic)
            self.assertIs(item.step, VALIDATE)
            self.assertIsInstance(item.element, str)
            self.assertTrue(item.element)
            self.assertTrue(item.constraint)
            self.assertTrue(item.message)
        keys = [
            (item.element, item.constraint, item.message) for item in diags
        ]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))

    def assert_refused(self, diags, element, *fragments):
        matches = [item for item in diags if item.element == element]
        self.assertTrue(matches, f"refus attendu pour {element}")
        joined = " ".join(
            f"{item.constraint} {item.message}" for item in matches
        )
        for fragment in fragments:
            self.assertIn(fragment, joined)
        return matches

    def assert_absent(self, diags, marker):
        for item in diags:
            self.assertNotIn(marker, item.element)
            self.assertNotIn(marker, item.constraint)
            self.assertNotIn(marker, item.message)

    def test_valide_explicite_acceptee(self):
        diags = self.validate(self.factory())
        self.assert_shape(diags)
        self.assertEqual(diags, [])

    def test_refus_candidat_non_dict(self):
        for candidate in (None, [], (), 42, "chaîne"):
            with self.subTest(opération="candidat non dict"):
                diags = self.validate(candidate)
                self.assert_shape(diags)
                self.assert_refused(
                    diags, f"{self.scope}.mapping", "dict exact attendu"
                )

    def test_refus_sous_classe_dict_avant_iter(self):
        diags = self.validate(_ForeignDict(self.factory()))
        self.assert_shape(diags)
        self.assert_refused(
            diags, f"{self.scope}.mapping", "dict exact attendu"
        )

    def test_refus_clé_etrangere_avant_hash(self):
        base = self.factory()
        hidden = next(iter(base))
        hostile = _HostileKey(hidden)
        candidate = dict(base)
        candidate[hostile] = candidate.pop(hidden)
        diags = self.validate(candidate)
        self.assert_shape(diags)
        self.assert_refused(
            diags, f"{self.scope}.keys", "clés str exactes attendues"
        )
        self.assertEqual(hostile.hash_count, 1)

    def test_refus_champ_manquant(self):
        base = self.factory()
        for field in sorted(base):
            with self.subTest(champ=field):
                candidate = dict(base)
                candidate.pop(field)
                diags = self.validate(candidate)
                self.assert_shape(diags)
                self.assert_refused(
                    diags, f"{self.scope}.{field}", "champ explicite requis"
                )

    def test_refus_clé_inconnue_sans_echo(self):
        candidate = dict(self.factory())
        marker = "CLE_MARQUEUR_INEDITE"
        candidate[marker] = _Boom()
        diags = self.validate(candidate)
        self.assert_shape(diags)
        self.assertTrue(diags)
        self.assert_absent(diags, marker)

    def test_refus_multi_tri_dedup(self):
        candidate = dict(self.factory())
        candidate["INCONNU"] = 1
        candidate.pop(next(iter(candidate)))
        diags = self.validate(candidate)
        self.assert_shape(diags)
        self.assertGreater(len(diags), 1)

    def test_resultat_liste_fraiche(self):
        first = self.validate(self.factory())
        second = self.validate(self.factory())
        self.assertIsNot(first, second)
        first.append("SENTINELLE")
        third = self.validate(self.factory())
        self.assertNotIn("SENTINELLE", third)

    def test_candidat_non_modifie(self):
        base = self.factory()
        snapshot = _snapshot(base)
        identities = {field: id(value) for field, value in base.items()}
        self.validate(base)
        self.assertEqual(base, snapshot)
        self.assertEqual(
            {field: id(value) for field, value in base.items()}, identities
        )
        self.validate({**base, "INCONNU": 1})
        self.assertEqual(base, snapshot)


class TestValidateBulkExecutionValues(_GuardMixin, unittest.TestCase):
    scope = _EXECUTION

    def factory(self):
        return _valid_execution_import()

    def validate(self, candidate):
        return validate_bulk_execution_values(candidate)

    def test_export_valide_accepte(self):
        diags = validate_bulk_execution_values(_valid_execution_export())
        self.assert_shape(diags)
        self.assertEqual(diags, [])

    def test_commit_et_conflict_none_admis_en_memoire(self):
        candidate = self.factory()
        candidate["commit_mode"] = None
        candidate["conflict_strategy"] = None
        self.assertEqual(validate_bulk_execution_values(candidate), [])

    def test_refus_sous_classe_str_avant_comportement(self):
        for field in _EXECUTION_STR_FIELDS:
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = _StrSub("valeur")
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_refus_bool_et_str_sur_champs_int(self):
        for field in _EXECUTION_INT_FIELDS + _PROGRESS_INT_FIELDS[:0]:
            with self.subTest(champ=field):
                for hostile in (True, "1", 1.0, _IntSub(1)):
                    candidate = dict(self.factory())
                    candidate[field] = hostile
                    diags = validate_bulk_execution_values(candidate)
                    self.assert_refused(diags, f"{self.scope}.{field}")

    def test_bool_exige_pour_cancellation(self):
        candidate = self.factory()
        candidate["cancellation_requested"] = 0
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(
            diags, f"{self.scope}.cancellation_requested", "bool exact attendu"
        )

    def test_none_refuse_sur_champs_requis(self):
        for field in (
            "operation_id",
            "execution_version",
            "requested_by_reference",
            "resolved_context_reference",
            "mapping_reference",
            "mapping_version",
            "idempotency_key",
            "correlation_id",
            "policy_reference",
            "policy_version",
            "revision",
            "expires_at",
            "cancellation_requested",
        ):
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = None
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_textes_vides_nul_surrogate_refuses_sans_echo(self):
        cases = (
            ("operation_id", ""),
            ("correlation_id", "a\x00b"),
            ("causation_id", "\ud800"),
            ("idempotency_key", "IDEM_MARQUEUR_\ud800"),
        )
        for field, hostile in cases:
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = hostile
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")
                self.assert_absent(diags, "IDEM_MARQUEUR_")

    def test_textes_unicode_espaces_et_egalite_admis(self):
        candidate = self.factory()
        candidate["correlation_id"] = "café-ñ-✓"
        candidate["policy_reference"] = " po\tlicy "
        candidate["mapping_reference"] = candidate["idempotency_key"]
        candidate["causation_id"] = "causation-0001"
        self.assertEqual(validate_bulk_execution_values(candidate), [])

    def test_sha256_exactement_64_minuscules(self):
        for hostile in (_SHA_A[:-1], _SHA_A + "0", _SHA_A.upper(), "g" * 64):
            with self.subTest(longueur=len(hostile)):
                candidate = dict(self.factory())
                candidate["input_sha256"] = hostile
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.input_sha256")

    def test_tailes_non_negatives_sans_plafond(self):
        candidate = self.factory()
        candidate["input_size_bytes"] = 0
        candidate["output_size_bytes"] = 10**30
        candidate["revision"] = 10**25
        self.assertEqual(validate_bulk_execution_values(candidate), [])
        for hostile in (-1, -10**20):
            candidate = dict(self.factory())
            candidate["output_size_bytes"] = hostile
            diags = validate_bulk_execution_values(candidate)
            self.assert_refused(
                diags,
                f"{self.scope}.output_size_bytes",
                "supérieur ou égal à zéro",
            )

    def test_revision_au_moins_un(self):
        candidate = dict(self.factory())
        candidate["revision"] = 0
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(
            diags, f"{self.scope}.revision", "supérieur ou égal à un"
        )

    def test_datetime_utc_canonique_sans_hook(self):
        past = datetime(2000, 1, 1, 12, 30, 45, 500_000, tzinfo=timezone.utc)
        candidate = self.factory()
        candidate["expires_at"] = past
        self.assertEqual(validate_bulk_execution_values(candidate), [])
        for hostile in (
            datetime(2030, 1, 1),
            datetime(2030, 1, 1, tzinfo=timezone(timedelta(hours=2))),
            datetime(2030, 1, 1, tzinfo=_RaisingTz()),
            _DatetimeSub(2030, 1, 1, tzinfo=timezone.utc),
        ):
            with self.subTest(opération="datetime étranger"):
                candidate = dict(self.factory())
                candidate["expires_at"] = hostile
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.expires_at")

    def test_execution_version_uniquement_1_0_0(self):
        candidate = dict(self.factory())
        candidate["execution_version"] = "2.0.0"
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(
            diags, f"{self.scope}.execution_version", "1.0.0 exact attendu"
        )

    def test_semver_reel_reutilise_apres_garde(self):
        for field in ("mapping_version", "policy_version"):
            for hostile in ("1.0", "01.0.0", "x"):
                with self.subTest(champ=field, valeur="invalide"):
                    candidate = dict(self.factory())
                    candidate[field] = hostile
                    diags = validate_bulk_execution_values(candidate)
                    self.assert_refused(diags, f"{self.scope}.{field}")

    def test_garde_globale_avant_record_et_semver(self):
        hostiles = (
            ("operation_id", _Boom()),
            ("revision", True),
            ("expires_at", datetime(2030, 1, 1)),
            ("causation_id", _IntSub(7)),
        )
        for field, hostile in hostiles:
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = hostile
                with (
                    mock.patch.object(
                        bulk_execution_values,
                        "validate_bulk_operation_record_values",
                        side_effect=AssertionError(
                            "Record appelé avant garde complète"
                        ),
                    ),
                    mock.patch.object(
                        bulk_execution_values,
                        "parse_version",
                        side_effect=AssertionError(
                            "parse_version appelé avant garde complète"
                        ),
                    ),
                ):
                    diags = validate_bulk_execution_values(candidate)
                self.assert_shape(diags)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_progress_imbrique_garde_avant_parsing(self):
        cases = (
            (_ForeignDict(_valid_progress()), "progress"),
            ({**_valid_progress(), "validated_rows": _Boom()},
             "progress.validated_rows"),
        )
        for progress, expected_field in cases:
            candidate = self.factory()
            candidate["progress"] = progress
            with (
                mock.patch.object(
                    bulk_execution_values, "validate_bulk_operation_record_values",
                    side_effect=AssertionError("Record avant garde imbriquée"),
                ),
                mock.patch.object(
                    bulk_execution_values, "parse_version",
                    side_effect=AssertionError("parse avant garde imbriquée"),
                ),
            ):
                diags = validate_bulk_execution_values(candidate)
            self.assert_refused(diags, f"{self.scope}.{expected_field}")

    def test_garde_avant_parsing_malgre_semver_invalide(self):
        candidate = dict(self.factory())
        candidate["mapping_version"] = "1.0"
        candidate["revision"] = True
        with (
            mock.patch.object(
                bulk_execution_values,
                "validate_bulk_operation_record_values",
                side_effect=AssertionError("Record appelé avant garde"),
            ),
            mock.patch.object(
                bulk_execution_values,
                "parse_version",
                side_effect=AssertionError("parse_version appelé avant garde"),
            ),
        ):
            diags = validate_bulk_execution_values(candidate)
        self.assert_refused(diags, f"{self.scope}.revision")

    def test_valeurs_canoniques_du_record_et_refus_des_aliases(self):
        for field, allowed in (
            ("format", ("CSV", "NDJSON")),
            ("status", ("REQUESTED", "STAGED", "VALIDATING", "READY", "RUNNING",
                        "COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED",
                        "CANCELLED", "EXPIRED")),
            ("conflict_strategy", ("REJECT", "CREATE_ONLY", "UPDATE_ONLY", "UPSERT")),
            ("commit_mode", ("VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT")),
        ):
            for value in allowed:
                with self.subTest(champ=field, valeur=value):
                    candidate = self.factory()
                    candidate[field] = value
                    if field == "commit_mode" and value == "VALIDATE_ONLY":
                        candidate["progress"]["applied_rows"] = 0
                    self.assertEqual(validate_bulk_execution_values(candidate), [])
            candidate = self.factory()
            candidate[field] = "ALIAS_INTERDIT"
            diags = validate_bulk_execution_values(candidate)
            self.assertTrue(any(item.element.endswith("." + field) for item in diags))

    def test_versions_semver_completes_et_refus(self):
        for field in ("bulk_version", "mapping_version", "policy_version"):
            candidate = self.factory()
            candidate[field] = "1.2.3-rc.1+build"
            self.assertEqual(validate_bulk_execution_values(candidate), [])
            candidate[field] = "1.0"
            diags = validate_bulk_execution_values(candidate)
            self.assertTrue(any(item.element.endswith("." + field) for item in diags))

    def test_import_exige_quatre_inputs_non_nuls(self):
        for field in (
            "input_reference",
            "input_version",
            "input_sha256",
            "input_size_bytes",
        ):
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = None
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_import_refuse_projection_et_consistency(self):
        for field in (
            "projection_reference",
            "consistency_kind",
            "consistency_reference",
        ):
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = "valeur-export"
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_export_exige_inputs_nuls_et_projection(self):
        candidate = _valid_execution_export()
        candidate["input_size_bytes"] = 0
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(diags, f"{self.scope}.input_size_bytes")
        candidate = _valid_execution_export()
        candidate["projection_reference"] = None
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(diags, f"{self.scope}.projection_reference")

    def test_export_consistency_kind_canonique(self):
        for hostile in (None, "FOO"):
            with self.subTest(valeur="hors canon"):
                candidate = _valid_execution_export()
                candidate["consistency_kind"] = hostile
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(diags, f"{self.scope}.consistency_kind")

    def test_export_consistency_reference_selon_etat(self):
        for state in _LATE_EXPORT_STATES:
            with self.subTest(etat=state):
                candidate = _valid_execution_export()
                candidate["status"] = state
                candidate["consistency_reference"] = None
                diags = validate_bulk_execution_values(candidate)
                self.assert_refused(
                    diags, f"{self.scope}.consistency_reference"
                )
        for state in _EARLY_EXPORT_STATES:
            with self.subTest(etat=state):
                candidate = _valid_execution_export()
                candidate["status"] = state
                candidate["consistency_reference"] = None
                diags = validate_bulk_execution_values(candidate)
                self.assert_shape(diags)
                self.assertEqual(diags, [])

    def test_execution_interdit_applied_export_et_validate_only(self):
        candidate = _valid_execution_export()
        candidate["progress"] = {
            **_valid_progress(),
            "applied_rows": 3,
            "execution_rejected_rows": 0,
            "exported_rows": 0,
        }
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(
            diags,
            f"{self.scope}.progress.applied_rows",
            "applied_rows nul attendu pour EXPORT ou VALIDATE_ONLY",
        )
        candidate = self.factory()
        candidate["commit_mode"] = "VALIDATE_ONLY"
        candidate["progress"] = {
            **_valid_progress(),
            "validated_rows": 8,
            "invalid_rows": 0,
            "applied_rows": 2,
            "execution_rejected_rows": 0,
            "exported_rows": 0,
        }
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(diags, f"{self.scope}.progress.applied_rows")

    def test_execution_interdit_exported_poUR_IMPORT(self):
        candidate = self.factory()
        candidate["progress"] = {
            **_valid_progress(),
            "validated_rows": 8,
            "invalid_rows": 0,
            "applied_rows": 5,
            "execution_rejected_rows": 3,
            "exported_rows": 1,
        }
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(
            diags,
            f"{self.scope}.progress.exported_rows",
            "exported_rows nul attendu pour IMPORT",
        )

    def test_execution_admet_rejected_non_nul_et_total_inconnu(self):
        candidate = self.factory()
        candidate["progress"] = {
            "total_rows": None,
            "validated_rows": 8,
            "invalid_rows": 0,
            "applied_rows": 5,
            "execution_rejected_rows": 3,
            "exported_rows": 0,
        }
        self.assertEqual(validate_bulk_execution_values(candidate), [])

    def test_execution_progress_interdit_validated_sup_total(self):
        candidate = self.factory()
        candidate["progress"] = {
            **_valid_progress(),
            "total_rows": 1,
            "validated_rows": 8,
            "invalid_rows": 0,
            "applied_rows": 1,
            "execution_rejected_rows": 0,
            "exported_rows": 0,
        }
        self.assertEqual(validate_bulk_execution_values(candidate), [])

    def test_progress_imbrique_refuse_sans_echo(self):
        marker = "CLE_MARQUEUR_PROGRESS"
        candidate = dict(self.factory())
        progress = dict(candidate["progress"])
        progress.pop(marker, None)
        progress[marker] = 1
        candidate["progress"] = progress
        diags = validate_bulk_execution_values(candidate)
        self.assert_shape(diags)
        self.assert_refused(diags, f"{self.scope}.progress.mapping")
        self.assert_absent(diags, marker)

    def test_progress_imbrique_refuse_types_negatifs_et_bool(self):
        for field in _PROGRESS_INT_FIELDS:
            for hostile in (True, "5", _IntSub(5), -1):
                with self.subTest(champ=field):
                    candidate = dict(self.factory())
                    progress = dict(candidate["progress"])
                    progress[field] = hostile
                    candidate["progress"] = progress
                    diags = validate_bulk_execution_values(candidate)
                    self.assert_refused(
                        diags, f"{self.scope}.progress.{field}"
                    )

    def test_progress_imbrique_sous_classe_dict_refusee(self):
        candidate = dict(self.factory())
        candidate["progress"] = _ForeignDict(_valid_progress())
        diags = validate_bulk_execution_values(candidate)
        self.assert_refused(diags, f"{self.scope}.progress")


class TestValidateBulkProgressValues(_GuardMixin, unittest.TestCase):
    scope = _PROGRESS

    def factory(self):
        return _valid_progress()

    def validate(self, candidate):
        return validate_bulk_progress_values(candidate)

    def test_independant_du_contexte_bulk(self):
        candidate = {
            "total_rows": 3,
            "validated_rows": 5,
            "invalid_rows": 0,
            "applied_rows": 2,
            "execution_rejected_rows": 3,
            "exported_rows": 5,
        }
        self.assertEqual(validate_bulk_progress_values(candidate), [])

    def test_inegalites_canoniques(self):
        cases = (
            ({"invalid_rows": 9, "validated_rows": 8}, "invalid_rows"),
            (
                {
                    "invalid_rows": 0,
                    "applied_rows": 5,
                    "execution_rejected_rows": 4,
                },
                "applied_rows",
            ),
            ({"exported_rows": 9}, "exported_rows"),
        )
        for override, field in cases:
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate.update(override)
                diags = validate_bulk_progress_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_compteurs_negatifs_refuses(self):
        for field in _PROGRESS_INT_FIELDS:
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = -1
                diags = validate_bulk_progress_values(candidate)
                self.assert_refused(
                    diags,
                    f"{self.scope}.{field}",
                    "supérieur ou égal à zéro",
                )

    def test_bool_ne_vaut_int(self):
        for field in _PROGRESS_INT_FIELDS:
            with self.subTest(champ=field):
                candidate = dict(self.factory())
                candidate[field] = True
                diags = validate_bulk_progress_values(candidate)
                self.assert_refused(diags, f"{self.scope}.{field}")

    def test_valeurs_enormes_acceptees(self):
        candidate = {
            "total_rows": 10**30,
            "validated_rows": 10**25,
            "invalid_rows": 0,
            "applied_rows": 10**25,
            "execution_rejected_rows": 0,
            "exported_rows": 10**25,
        }
        self.assertEqual(validate_bulk_progress_values(candidate), [])


class TestValidateBulkPolicyValues(_GuardMixin, unittest.TestCase):
    scope = _POLICY

    def factory(self):
        return _valid_policy()

    def validate(self, candidate):
        return validate_bulk_policy_values(candidate)

    def test_entiers_non_positifs_refuses(self):
        for field in _POLICY_INT_FIELDS:
            for hostile in (0, -1):
                with self.subTest(champ=field):
                    candidate = dict(self.factory())
                    candidate[field] = hostile
                    diags = validate_bulk_policy_values(candidate)
                    self.assert_refused(
                        diags,
                        f"{self.scope}.{field}",
                        "strictement positif",
                    )

    def test_entiers_bool_et_sous_classes_refuses(self):
        for field in _POLICY_INT_FIELDS:
            for hostile in (True, _IntSub(1), _Boom()):
                with self.subTest(champ=field):
                    candidate = dict(self.factory())
                    candidate[field] = hostile
                    diags = validate_bulk_policy_values(candidate)
                    self.assert_refused(diags, f"{self.scope}.{field}")

    def test_listes_types_et_elements(self):
        for field in ("retry_delays_seconds", "publish_retry_delays_seconds"):
            for hostile in ((), _ForeignList([1]), [True], [-1], [0], ["1"]):
                with self.subTest(champ=field):
                    candidate = dict(self.factory())
                    candidate[field] = hostile
                    diags = validate_bulk_policy_values(candidate)
                    self.assert_refused(diags, f"{self.scope}.{field}")

    def test_longueurs_attentes_minus_un(self):
        candidate = dict(self.factory())
        candidate["retry_delays_seconds"] = [1]
        diags = validate_bulk_policy_values(candidate)
        self.assert_refused(diags, f"{self.scope}.retry_delays_seconds")
        candidate = dict(self.factory())
        candidate["publish_retry_delays_seconds"] = [1]
        diags = validate_bulk_policy_values(candidate)
        self.assert_refused(diags, f"{self.scope}.publish_retry_delays_seconds")

    def test_listes_vides_si_attentes_un(self):
        candidate = dict(self.factory())
        candidate["max_attempts"] = 1
        candidate["retry_delays_seconds"] = []
        self.assertEqual(validate_bulk_policy_values(candidate), [])

    def test_inegalites_strictes_de_renewal(self):
        candidate = dict(self.factory())
        candidate["renewal_seconds"] = 30
        diags = validate_bulk_policy_values(candidate)
        self.assert_refused(
            diags,
            f"{self.scope}.renewal_seconds",
            "strictement inférieur à lease_seconds",
        )
        candidate = dict(self.factory())
        candidate["publish_renewal_seconds"] = 25
        diags = validate_bulk_policy_values(candidate)
        self.assert_refused(
            diags,
            f"{self.scope}.publish_renewal_seconds",
            "strictement inférieur à publish_lease_seconds",
        )

    def test_retention_superieure_ou_egale_au_replay(self):
        candidate = dict(self.factory())
        candidate["idempotency_retention_seconds"] = 300
        self.assertEqual(validate_bulk_policy_values(candidate), [])
        candidate = dict(self.factory())
        candidate["idempotency_retention_seconds"] = 299
        diags = validate_bulk_policy_values(candidate)
        self.assert_refused(
            diags,
            f"{self.scope}.idempotency_retention_seconds",
            "supérieur ou égal à replay_window_seconds",
        )

    def test_entiers_enormes_acceptes(self):
        candidate = dict(self.factory())
        candidate["max_input_bytes"] = 10**30
        candidate["lease_seconds"] = 10**30
        candidate["retry_delays_seconds"] = [1, 2]
        self.assertEqual(validate_bulk_policy_values(candidate), [])


if __name__ == "__main__":
    unittest.main()
