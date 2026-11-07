"""Profil Unix/peer : structure et refus purs, aucune connexion."""
from dataclasses import asdict, replace
import json
import unittest

from pixs.pa_native.postgresql_profile import PeerProfile, PeerProfileError, parse_peer_profile


class PeerProfileTest(unittest.TestCase):
    def setUp(self):
        self.profile = PeerProfile(
            "1.0.0", "profil", "révision", "cible", "règle-peer",
            "/socket-test", 55432, "base-test", "role-test", "compte-serveur-test",
            2, 1000, 500, 1500, 160015)

    def document(self, **changes):
        values = asdict(self.profile) | changes
        return "\n".join(name + " = " + (json.dumps(value, ensure_ascii=False)
                       if type(value) is str else str(value))
                         for name, value in values.items())

    def test_closed_document_and_explicit_arguments(self):
        result = parse_peer_profile(self.document(), max_bytes=4096, max_field_bytes=128)
        self.assertEqual(result, self.profile)
        self.assertEqual(result.native_arguments(), (
            b"/socket-test", b"55432", b"base-test", b"role-test",
            b"compte-serveur-test", b"2", b"1000", b"500", b"1500", b"160015"))

    def test_missing_unknown_credential_and_network_fields_are_rejected(self):
        text = self.document()
        for extra in ('password = "marqueur"', 'dsn = "marqueur"', 'hostaddr = "127.0.0.1"',
                      'tls = true', 'shell = "marqueur"'):
            with self.subTest(extra=extra), self.assertRaises(PeerProfileError):
                parse_peer_profile(text + "\n" + extra, max_bytes=4096, max_field_bytes=128)
        with self.assertRaises(PeerProfileError):
            parse_peer_profile("\n".join(text.splitlines()[1:]), max_bytes=4096, max_field_bytes=128)

    def test_socket_directory_cannot_be_tcp_multihost_relative_or_ambiguous(self):
        for value in ("localhost", "127.0.0.1", "@abstraite", "/a,/b", "/a/../b",
                      "/a/./b", "/a//b", "/a/", "//a", "/a\\b"):
            with self.subTest(value=value), self.assertRaises(PeerProfileError):
                replace(self.profile, socket_directory=value)

    def test_controls_utf8_and_empty_values_are_refused_without_connection(self):
        for value in ("", "a\x00b", "a\x7fb", "\ud800"):
            for field in ("database", "database_user", "server_os_user", "peer_rule_ref"):
                with self.subTest(field=field), self.assertRaises(PeerProfileError):
                    replace(self.profile, **{field: value})

    def test_types_bounds_and_no_implicit_timeout_are_enforced(self):
        for field, value in (
                ("port", True), ("port", 0), ("port", 65536),
                ("connect_timeout_seconds", 0),
                ("statement_timeout_ms", 0), ("lock_timeout_ms", -1), ("io_timeout_ms", 0),
                ("expected_server_version_num", False), ("schema_version", "2.0.0")):
            with self.subTest(field=field, value=value), self.assertRaises(PeerProfileError):
                replace(self.profile, **{field: value})

    def test_document_and_field_limits_are_mandatory_and_checked(self):
        for maximum, field in ((1, 128), (4096, 1), (False, 128), (4096, 0)):
            with self.assertRaises(PeerProfileError):
                parse_peer_profile(self.document(), max_bytes=maximum, max_field_bytes=field)

    def test_duplicate_or_invalid_toml_and_nontext_are_rejected(self):
        for text in (self.document() + '\nport = 55432', "invalid=[", None):
            with self.assertRaises(PeerProfileError):
                parse_peer_profile(text, max_bytes=4096, max_field_bytes=128)

    def test_repr_and_diagnostic_do_not_disclose_profile(self):
        self.assertNotIn("compte-serveur-test", repr(self.profile))
        with self.assertRaises(PeerProfileError) as caught:
            replace(self.profile, socket_directory="marqueur-privé")
        self.assertNotIn("marqueur-privé", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
