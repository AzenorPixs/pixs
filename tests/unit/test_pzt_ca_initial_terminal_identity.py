"""Tests structurels identité terminale §13.2, sans qualification owner."""

from __future__ import annotations

import dataclasses
import datetime
import json
import unittest
from typing import Any

from pixs.pzt_ca.initial_terminal_identity import (
    IDENTITY_OBJECT,
    InitialTerminalIdentity,
    InitialTerminalIdentityError,
    identity_from_json,
    identity_from_mapping,
)

V7_A = "0193e8d5-5c9a-7a1b-8c2d-3e4f5a6b7c8d"
V7_B = "0193e8d6-1111-7c22-8d33-444455556666"
V4_UUID = "550e8400-e29b-41d4-a716-446655440000"
NON_RFC_VARIANT_UUID = "0193e8d5-5c9a-7a1b-ec2d-3e4f5a6b7c8d"
LOOPBACK_FIXTURE = "127.0.0.2"

REQUIRED_25 = [
    "object_type", "schema_version", "identity_ref", "installation_ref",
    "target_ref", "terminal_ref", "native_instance_ref", "instance_uuid",
    "role_ref", "tls_usage", "key_ref", "key_generation_ref", "cert_ref",
    "root_authority_ref", "issuer_generation_ref", "policy_ref",
    "policy_version", "plan_ref", "plan_version", "epoch",
    "key_created_at", "not_before", "not_after",
    "hardware_evidence_ref", "possession_evidence_ref",
]

REF_17 = [
    "identity_ref", "installation_ref", "target_ref", "terminal_ref",
    "native_instance_ref", "role_ref", "key_ref", "key_generation_ref",
    "cert_ref", "root_authority_ref", "issuer_generation_ref",
    "policy_ref", "policy_version", "plan_ref", "plan_version",
    "hardware_evidence_ref", "possession_evidence_ref",
]


def _base(tls_usage: str = "clientAuth") -> dict[str, Any]:
    mapping: dict[str, Any] = {
        "object_type": IDENTITY_OBJECT,
        "schema_version": "1.0.0",
        "identity_ref": "pub:identity:001",
        "installation_ref": "pub:installation:001",
        "target_ref": "pub:target:001",
        "terminal_ref": "pub:terminal:pzt",
        "native_instance_ref": "pub:native:001",
        "instance_uuid": V7_A,
        "role_ref": "pub:role:pzt-terminal",
        "tls_usage": tls_usage,
        "key_ref": "pub:key:term:001",
        "key_generation_ref": "pub:keygen:001",
        "cert_ref": "pub:cert:001",
        "root_authority_ref": "pub:root:d2",
        "issuer_generation_ref": "pub:gen:d2:i1",
        "policy_ref": "pub:policy:z12",
        "policy_version": "pub:policy-v:9",
        "plan_ref": "pub:plan:first-install",
        "plan_version": "pub:plan-v:3",
        "epoch": 4,
        "key_created_at": "2026-10-23T10:00:00Z",
        "not_before": "2026-10-23T10:00:00Z",
        "not_after": "2026-10-24T10:00:00Z",
        "hardware_evidence_ref": "pub:ev:hw:001",
        "possession_evidence_ref": "pub:ev:poss:001",
    }
    if tls_usage == "serverAuth":
        mapping["server_ipv4"] = LOOPBACK_FIXTURE
    return mapping


def _valid_object() -> InitialTerminalIdentity:
    return identity_from_mapping(_base("clientAuth"))


class TestInitialTerminalIdentity(unittest.TestCase):
    def test_client_ok(self) -> None:
        obj = identity_from_mapping(_base("clientAuth"))
        self.assertEqual(obj.tls_usage, "clientAuth")
        self.assertIsNone(obj.server_ipv4)

    def test_serveur_ok(self) -> None:
        obj = identity_from_mapping(_base("serverAuth"))
        self.assertEqual(obj.server_ipv4, LOOPBACK_FIXTURE)

    def test_json_rond(self) -> None:
        text = json.dumps(_base("serverAuth"), separators=(",", ":"))
        self.assertEqual(identity_from_json(text).server_ipv4, LOOPBACK_FIXTURE)

    def test_manquant_chacun_des_25_requis(self) -> None:
        for field in REQUIRED_25:
            with self.subTest(field=field):
                mapping = _base("clientAuth")
                del mapping[field]
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_null_chacun_requis_et_ip_optionnelle(self) -> None:
        for field in REQUIRED_25:
            with self.subTest(field=field):
                mapping = _base("clientAuth")
                mapping[field] = None
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)
        mapping = _base("serverAuth")
        mapping["server_ipv4"] = None
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_mapping(mapping)

    def test_refs_vides_et_types(self) -> None:
        bads: list[Any] = ["", 0, 123, ["x"], {"r": "x"}, True]
        for field in REF_17:
            for bad in bads:
                with self.subTest(field=field, bad=repr(bad)):
                    mapping = _base("clientAuth")
                    mapping[field] = bad
                    with self.assertRaises(InitialTerminalIdentityError):
                        identity_from_mapping(mapping)

    def test_discriminateur_spoofes(self) -> None:
        for bad in [123, None, True, ["x"], "z12.ca_request/v1", ""]:
            with self.subTest(bad=repr(bad)):
                mapping = _base("clientAuth")
                mapping["object_type"] = bad
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_versions_spoofees(self) -> None:
        for bad in [123, None, True, "2.0.0", "1.0", "", {"v": "1"}]:
            with self.subTest(bad=repr(bad)):
                mapping = _base("clientAuth")
                mapping["schema_version"] = bad
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_tls_usages_spoofes(self) -> None:
        for bad in ["client", "server", "", None, 123, True, "ANY"]:
            with self.subTest(bad=repr(bad)):
                mapping = _base("clientAuth")
                mapping["tls_usage"] = bad
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_uuid_spoofes(self) -> None:
        cases = [
            V7_A.upper(), V4_UUID, NON_RFC_VARIANT_UUID,
            "not-an-uuid", "", 123, None, True,
        ]
        for bad in cases:
            with self.subTest(bad=repr(bad)):
                mapping = _base("clientAuth")
                mapping["instance_uuid"] = bad
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_ip_spoofees_serveur(self) -> None:
        cases: list[Any] = [
            "::1", "192.168.1.10", "8.8.8.8", "127.000.0.2",
            "127.0.0.2/32", "999.999.999.999", 123, ["127.0.0.2"],
            True, None,
        ]
        for bad in cases:
            with self.subTest(bad=repr(bad)):
                mapping = _base("serverAuth")
                mapping["server_ipv4"] = bad
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_ip_absente_serveur_et_interdite_client(self) -> None:
        mapping = _base("serverAuth")
        del mapping["server_ipv4"]
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_mapping(mapping)
        mapping = _base("clientAuth")
        mapping["server_ipv4"] = LOOPBACK_FIXTURE
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_mapping(mapping)

    def test_epoch_spoofes(self) -> None:
        for bad in [True, False, 1.0, "4", None, -1, -100]:
            with self.subTest(bad=repr(bad)):
                mapping = _base("clientAuth")
                mapping["epoch"] = bad
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_dates_string_invalides(self) -> None:
        bads = [
            "2026-10-23T10:00:00", "2026-10-23T10:00:00+02:00",
            "2026-10-23 10:00:00Z", "not-a-date", 1234567890, None,
        ]
        for field in ("key_created_at", "not_before", "not_after"):
            for bad in bads:
                with self.subTest(field=field, bad=repr(bad)):
                    mapping = _base("clientAuth")
                    mapping[field] = bad
                    with self.assertRaises(InitialTerminalIdentityError):
                        identity_from_mapping(mapping)

    def test_dates_directes_naive_non_utc_subclasse(self) -> None:
        base = _valid_object()
        naive = datetime.datetime(2026, 10, 23, 10, 0, 0)
        non_utc = datetime.datetime(
            2026, 10, 23, 10, 0, 0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=2)),
        )
        class SpoofedInstant(datetime.datetime):
            pass
        spoofed = SpoofedInstant(
            2026, 10, 23, 10, 0, 0, tzinfo=datetime.timezone.utc
        )
        for bad in (naive, non_utc, spoofed):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(InitialTerminalIdentityError):
                    dataclasses.replace(base, not_before=bad)

    def test_periode_inversee(self) -> None:
        for not_before, not_after in [
            ("2026-10-24T10:00:00Z", "2026-10-23T10:00:00Z"),
            ("2026-10-23T10:00:00Z", "2026-10-23T10:00:00Z"),
        ]:
            with self.subTest(not_before=not_before, not_after=not_after):
                mapping = _base("clientAuth")
                mapping["not_before"] = not_before
                mapping["not_after"] = not_after
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_mapping(mapping)

    def test_spoof_subclass_direct(self) -> None:
        base = _valid_object()
        class SpoofedStr(str):
            pass
        class SpoofedInt(int):
            pass
        with self.subTest(kind="str-subclass-ref"):
            with self.assertRaises(InitialTerminalIdentityError):
                dataclasses.replace(
                    base, identity_ref=SpoofedStr("pub:identity:001")
                )
        with self.subTest(kind="bool-epoch"):
            with self.assertRaises(InitialTerminalIdentityError):
                dataclasses.replace(base, epoch=True)
        with self.subTest(kind="int-subclass-epoch"):
            with self.assertRaises(InitialTerminalIdentityError):
                dataclasses.replace(base, epoch=SpoofedInt(4))

    def test_construction_directe_client_sans_arg_ip(self) -> None:
        base = _base("clientAuth")
        valid = identity_from_mapping(base)
        obj = InitialTerminalIdentity(
            object_type=base["object_type"],
            schema_version=base["schema_version"],
            identity_ref=base["identity_ref"],
            installation_ref=base["installation_ref"],
            target_ref=base["target_ref"],
            terminal_ref=base["terminal_ref"],
            native_instance_ref=base["native_instance_ref"],
            instance_uuid=base["instance_uuid"],
            role_ref=base["role_ref"],
            tls_usage="clientAuth",
            key_ref=base["key_ref"],
            key_generation_ref=base["key_generation_ref"],
            cert_ref=base["cert_ref"],
            root_authority_ref=base["root_authority_ref"],
            issuer_generation_ref=base["issuer_generation_ref"],
            policy_ref=base["policy_ref"],
            policy_version=base["policy_version"],
            plan_ref=base["plan_ref"],
            plan_version=base["plan_version"],
            epoch=4,
            key_created_at=valid.key_created_at,
            not_before=valid.not_before,
            not_after=valid.not_after,
            hardware_evidence_ref=base["hardware_evidence_ref"],
            possession_evidence_ref=base["possession_evidence_ref"],
        )
        self.assertIsNone(obj.server_ipv4)

    def test_immutabilite_et_slots(self) -> None:
        obj = _valid_object()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            obj.epoch = 99
        self.assertFalse(hasattr(obj, "__dict__"))
        self.assertIn("server_ipv4", InitialTerminalIdentity.__slots__)

    def test_json_doublon_sur_objet_complet(self) -> None:
        text = json.dumps(_base("serverAuth"), separators=(",", ":"))
        dup = text[:-1] + ',"identity_ref":"pub:spoof:002"}'
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_json(dup)

    def test_json_null_et_schema_wrong(self) -> None:
        mapping = _base("clientAuth")
        mapping["key_ref"] = None
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_json(json.dumps(mapping))
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_json(json.dumps({"unexpected": "envelope"}))

    def test_json_nan_infinity_dans_objet_complet(self) -> None:
        for token in ["NaN", "Infinity", "-Infinity"]:
            with self.subTest(token=token):
                text = json.dumps(_base("clientAuth"), separators=(",", ":"))
                bad = text.replace('"epoch":4', '"epoch":' + token)
                with self.assertRaises(InitialTerminalIdentityError):
                    identity_from_json(bad)

    def test_json_non_dict_array_nested(self) -> None:
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_json("[1,2,3]")
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_json("42")
        mapping = _base("clientAuth")
        mapping["identity_ref"] = {"op": "inject"}
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_mapping(mapping)

    def test_diagnostic_sans_valeur_rejetee(self) -> None:
        marker = "VALEUR_SYNTHETIQUE_REJETEE_9f8e7d6c"
        mapping = _base("clientAuth")
        mapping["identity_ref"] = {"invalid": marker}
        try:
            identity_from_mapping(mapping)
        except InitialTerminalIdentityError as exc:
            self.assertNotIn(marker, str(exc))
            self.assertNotIn(marker, exc.code)
            self.assertNotIn(marker, exc.element)
        else:
            self.fail("refus attendu")


    def test_champ_etranger_sur_objet_complet(self) -> None:
        mapping = _base("clientAuth")
        mapping["extra_ref"] = "pub:etranger:001"
        with self.assertRaises(InitialTerminalIdentityError):
            identity_from_mapping(mapping)

    def test_controles_directs_sans_parser(self) -> None:
        base = _valid_object()
        class SpoofedStr(str):
            pass
        cases = [
            {"object_type": SpoofedStr(IDENTITY_OBJECT)},
            {"schema_version": SpoofedStr("1.0.0")},
            {"tls_usage": True},
            {"instance_uuid": 123},
            {"not_after": base.not_before},
            {"tls_usage": "serverAuth", "server_ipv4": None},
            {"tls_usage": "serverAuth", "server_ipv4": SpoofedStr(LOOPBACK_FIXTURE)},
            {"server_ipv4": LOOPBACK_FIXTURE},
        ]
        for change in cases:
            with self.subTest(fields=tuple(change)):
                with self.assertRaises(InitialTerminalIdentityError):
                    dataclasses.replace(base, **change)


if __name__ == "__main__":
    unittest.main()
