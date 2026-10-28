"""Recette structurelle S1 de l'enveloppe de campagne PA01.

Exerce le vrai parseur sur des textes TOML, sans miroir de sa logique :
positifs, refus precis, cas limites et gardes d'absence d'entree-sortie.
Aucune preuve S2, aucun raccord S3, aucune qualification de binaire.
"""
from __future__ import annotations

import json
import os
import pathlib
import socket
import subprocess
import traceback
import unittest
import urllib.request
from unittest.mock import patch

from pixs.pa_native.build_profile import ProfileError
from pixs.pa_native.campaign_envelope import CampaignEnvelope, CampaignEnvelopeError, parse_envelope

NOMINAL = (
    'schema_version = "1.0.0"\n'
    '[campaign]\n'
    'id = "pa01-2026-10-26-c1"\n'
    'component = "pa01"\n'
    '[toolchain]\n'
    'cython = "3.3.0"\n'
    '[selection]\n'
    'verified_at = "2026-10-26T21:11:03Z"\n'
    'source_url = "https://pypi.org/pypi/Cython/json"\n'
    'snapshot = "evidence/cython-2026-10-26.json"\n'
    'snapshot_sha256 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n'
    '[[distributions]]\n'
    'filename = "cython-3.3.0-py3-none-any.whl"\n'
    'url = "https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl"\n'
    'sha256 = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"\n'
)

_CODE = "PA01_CAMPAIGN_METADATA_INVALID"


def _replace_line(text: str, start: str, replacement: str) -> str:
    lines = text.split("\n")
    found = [line for line in lines if line.startswith(start)]
    assert len(found) == 1
    return "\n".join(replacement if line.startswith(start) else line for line in lines)


class CampaignEnvelopeTest(unittest.TestCase):
    def test_valid_nominal(self) -> None:
        envelope = parse_envelope(NOMINAL)
        self.assertIs(type(envelope), CampaignEnvelope)
        self.assertEqual(envelope.schema_version, "1.0.0")
        self.assertEqual(envelope.toolchain.cython, "3.3.0")
        self.assertEqual(len(envelope.distributions), 1)

    def test_fraction_seven_decimals_preserved(self) -> None:
        text = _replace_line(NOMINAL, "verified_at =", 'verified_at = "2026-10-26T21:11:03.1234567Z"')
        envelope = parse_envelope(text)
        self.assertEqual(envelope.selection.verified_at, "2026-10-26T21:11:03.1234567Z")

    def test_epoch_and_post_locks(self) -> None:
        for lock in ("1!3.3.0", "3.3.0.post1"):
            text = _replace_line(NOMINAL, 'cython =', 'cython = "' + lock + '"')
            envelope = parse_envelope(text)
            self.assertEqual(envelope.toolchain.cython, lock)

    def test_missing_table_refused(self) -> None:
        text = "\n".join(line for line in NOMINAL.split("\n") if not line.startswith("[toolchain]")) + "\n"
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : enveloppe"):
            parse_envelope(text)

    def test_unknown_root_refused(self) -> None:
        text = NOMINAL.replace('schema_version = "1.0.0"\n', 'schema_version = "1.0.0"\nextra = 1\n', 1)
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : enveloppe"):
            parse_envelope(text)

    def test_unknown_nested_key_refused(self) -> None:
        text = NOMINAL.replace('component = "pa01"', 'component = "pa01"\nlabel = "x"', 1)
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : campaign"):
            parse_envelope(text)

    def test_absent_field_refused(self) -> None:
        text = "\n".join(line for line in NOMINAL.split("\n") if not line.startswith('component =')) + "\n"
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : campaign"):
            parse_envelope(text)

    def test_mixed_type_refused(self) -> None:
        text = _replace_line(NOMINAL, 'id =', "id = 42")
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : campaign.id"):
            parse_envelope(text)

    def test_wrong_schema_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : schema_version"):
            parse_envelope(_replace_line(NOMINAL, "schema_version =", 'schema_version = "2.0.0"'))

    def test_wrong_component_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : campaign.component"):
            parse_envelope(NOMINAL.replace('component = "pa01"', 'component = "pbo"', 1))

    def test_open_constraint_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : toolchain.cython"):
            parse_envelope(_replace_line(NOMINAL, "cython =", 'cython = ">=3.3.0"'))

    def test_prerelease_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : toolchain.cython"):
            parse_envelope(_replace_line(NOMINAL, "cython =", 'cython = "3.3.0rc1"'))

    def test_dev_release_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : toolchain.cython"):
            parse_envelope(_replace_line(NOMINAL, "cython =", 'cython = "3.3.0.dev0"'))

    def test_local_version_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : toolchain.cython"):
            parse_envelope(_replace_line(NOMINAL, "cython =", 'cython = "3.3.0+local"'))

    def test_non_normalized_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : toolchain.cython"):
            parse_envelope(_replace_line(NOMINAL, "cython =", 'cython = "03.3.0"'))

    def test_native_toml_date_refused(self) -> None:
        text = NOMINAL.replace('verified_at = "2026-10-26T21:11:03Z"', "verified_at = 2026-10-26T21:11:03Z", 1)
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.verified_at"):
            parse_envelope(text)

    def test_year_zero_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.verified_at"):
            parse_envelope(_replace_line(NOMINAL, "verified_at =", 'verified_at = "0000-01-01T00:00:00Z"'))

    def test_non_leap_1900_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.verified_at"):
            parse_envelope(_replace_line(NOMINAL, "verified_at =", 'verified_at = "1900-02-29T00:00:00Z"'))

    def test_leap_2000_accepted(self) -> None:
        envelope = parse_envelope(_replace_line(NOMINAL, "verified_at =", 'verified_at = "2000-02-29T00:00:00Z"'))
        self.assertEqual(envelope.selection.verified_at, "2000-02-29T00:00:00Z")

    def test_unicode_digits_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.verified_at"):
            parse_envelope(_replace_line(NOMINAL, "verified_at =", 'verified_at = "\u0662\u0660\u0662\u0666-10-26T21:11:03Z"'))

    def test_second_60_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.verified_at"):
            parse_envelope(_replace_line(NOMINAL, "verified_at =", 'verified_at = "2026-10-26T21:11:60Z"'))

    def test_hour_24_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.verified_at"):
            parse_envelope(_replace_line(NOMINAL, "verified_at =", 'verified_at = "2026-10-26T24:00:00Z"'))

    def test_crlf_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : enveloppe"):
            parse_envelope(NOMINAL.replace("\n", "\r\n"))

    def test_control_del_refused(self) -> None:
        replacement = "id = " + json.dumps("a\u007f")
        text = NOMINAL.replace('id = "pa01-2026-10-26-c1"', replacement, 1)
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : campaign.id"):
            parse_envelope(text)

    def test_control_c1_refused(self) -> None:
        replacement = "id = " + json.dumps("a\u0085")
        text = NOMINAL.replace('id = "pa01-2026-10-26-c1"', replacement, 1)
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : campaign.id"):
            parse_envelope(text)

    def test_surrogate_envelope_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : enveloppe"):
            parse_envelope(NOMINAL + "# \ud800\n")

    def test_absolute_snapshot_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.snapshot"):
            parse_envelope(NOMINAL.replace("evidence/cython-2026-10-26.json", "/tmp/evidence.json", 1))

    def test_escaping_snapshot_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.snapshot"):
            parse_envelope(NOMINAL.replace("evidence/cython-2026-10-26.json", "../evidence.json", 1))

    def test_backslash_snapshot_refused(self) -> None:
        text = _replace_line(NOMINAL, "snapshot =", 'snapshot = "a\\\\b.json"')
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : selection.snapshot"):
            parse_envelope(text)

    def test_duplicate_filename_refused(self) -> None:
        extra = '[[distributions]]\nfilename = "cython-3.3.0-py3-none-any.whl"\nurl = "https://files.pythonhosted.org/packages/autre.whl"\nsha256 = "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"\n'
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(NOMINAL + extra)

    def test_path_at_allowed(self) -> None:
        text = NOMINAL.replace("https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", "https://files.pythonhosted.org/packages/dir@name/cython-3.3.0-py3-none-any.whl", 1)
        envelope = parse_envelope(text)
        self.assertEqual(envelope.distributions[0].url, "https://files.pythonhosted.org/packages/dir@name/cython-3.3.0-py3-none-any.whl")

    def test_userinfo_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(NOMINAL.replace("https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", "https://user@files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", 1))

    def test_triple_slash_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(NOMINAL.replace("https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", "https:///x", 1))

    def test_malformed_port_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(NOMINAL.replace("https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", "https://files.pythonhosted.org:bad/cython.whl", 1))

    def test_malformed_url_hides_marker(self) -> None:
        marker = "MARQUEUR_SYNTHETIQUE_TEST_７Ｆ３Ａ９"
        text = NOMINAL.replace("https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", "https://files.pythonhosted.org:" + marker + "/cython.whl", 1)
        try:
            parse_envelope(text)
        except CampaignEnvelopeError as error:
            self.assertNotIn(marker, str(error))
            formatted = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            self.assertNotIn(marker, formatted)
        else:
            self.fail("CampaignEnvelopeError attendue")

    def test_short_sha_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(NOMINAL.replace("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "bbbb", 1))

    def test_long_sha_refused(self) -> None:
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(NOMINAL.replace("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "b" * 65, 1))

    def test_empty_distributions_refused(self) -> None:
        text = "distributions = []\n" + NOMINAL.split("[[distributions]]\n")[0]
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : distributions"):
            parse_envelope(text)

    def test_duplicate_toml_key_refused(self) -> None:
        text = NOMINAL.replace('[campaign]\n', '[campaign]\ncomponent = "pa01"\n', 1)
        with self.assertRaisesRegex(CampaignEnvelopeError, _CODE + " : enveloppe"):
            parse_envelope(text)

    def test_frozen_dto(self) -> None:
        envelope = parse_envelope(NOMINAL)
        with self.assertRaises(AttributeError):
            envelope.schema_version = "2.0.0"  # type: ignore[misc]

    def test_subclasses_profile_error(self) -> None:
        with self.assertRaisesRegex(ProfileError, _CODE + " : schema_version"):
            parse_envelope(_replace_line(NOMINAL, "schema_version =", 'schema_version = "2.0.0"'))

    def test_no_file_or_process_io(self) -> None:
        class _NoEnviron:
            def __getitem__(self, key):
                raise AssertionError("environ")
            def get(self, *args, **kwargs):
                raise AssertionError("environ")
            def items(self):
                raise AssertionError("environ")
            def __iter__(self):
                raise AssertionError("environ")
            def copy(self):
                raise AssertionError("environ")
        with patch("builtins.open", side_effect=AssertionError("open")) as mock_open, patch("pathlib.Path.open", side_effect=AssertionError("Path.open")) as mock_path_open, patch("pathlib.Path.read_text", side_effect=AssertionError("read_text")) as mock_read_text, patch("pathlib.Path.read_bytes", side_effect=AssertionError("read_bytes")) as mock_read_bytes, patch("os.open", side_effect=AssertionError("os.open")) as mock_os_open, patch("os.getenv", side_effect=AssertionError("getenv")) as mock_getenv, patch.object(os, "environ", new=_NoEnviron()), patch("socket.create_connection", side_effect=AssertionError("socket")) as mock_socket, patch("urllib.request.urlopen", side_effect=AssertionError("urlopen")) as mock_urlopen, patch("subprocess.Popen", side_effect=AssertionError("Popen")) as mock_popen:
            envelope = parse_envelope(NOMINAL)
        self.assertEqual(envelope.toolchain.cython, "3.3.0")
        mock_open.assert_not_called()
        mock_path_open.assert_not_called()
        mock_read_text.assert_not_called()
        mock_read_bytes.assert_not_called()
        mock_os_open.assert_not_called()
        mock_getenv.assert_not_called()
        mock_socket.assert_not_called()
        mock_urlopen.assert_not_called()
        mock_popen.assert_not_called()

    def test_no_network_but_url_kept(self) -> None:
        text = NOMINAL.replace("https://files.pythonhosted.org/packages/cython-3.3.0-py3-none-any.whl", "https://files.pythonhosted.org/packages/injoignable-999.whl", 1)
        with patch("urllib.request.urlopen", side_effect=AssertionError("urlopen")), patch("socket.create_connection", side_effect=AssertionError("socket")):
            envelope = parse_envelope(text)
        self.assertEqual(envelope.distributions[0].url, "https://files.pythonhosted.org/packages/injoignable-999.whl")


if __name__ == "__main__":
    unittest.main()
