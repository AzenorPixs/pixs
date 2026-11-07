"""D4/D6 : choix de mode seul ; aucun démarrage ou privilège exercé."""
from __future__ import annotations

import unittest

from pixs.pa_native.cli import ModeError, parse_mode


class NativeCliTest(unittest.TestCase):
    def test_seven_modes_in_both_explicit_forms(self):
        roles = {
            "pixs-pa-system": ("system-daemon",),
            "pixs-pa-events": ("system-start", "system-stop"),
            "pixs-pa-session": ("session-start", "session-stop", "session-daemon"),
            "pzt": ("pzt-daemon",),
        }
        for executable, modes in roles.items():
            for mode in modes:
                with self.subTest(executable=executable, mode=mode):
                    self.assertEqual(parse_mode(executable, ["--mode", mode]), mode)
                    self.assertEqual(parse_mode(executable, ["--mode=" + mode]), mode)

    def test_absence_duplicates_and_extra_arguments_are_rejected(self):
        for arguments in ([], ["--mode"], ["--mode="], ["system-daemon"],
                          ["--mod", "system-daemon"],
                          ["--mode", "system-daemon", "--extra"],
                          ["--mode=system-daemon", "--mode=system-daemon"],
                          ["--mode", "system-daemon", "--mode", "system-daemon"],
                          ["-c", "print(1)"]):
            with self.subTest(arguments=arguments), self.assertRaises(ModeError):
                parse_mode("pixs-pa-system", arguments)

    def test_foreign_role_and_unknown_modes_are_rejected(self):
        for executable, mode in (("pixs-pa-system", "pzt-daemon"),
                                 ("pzt", "system-daemon"),
                                 ("pixs-pa-events", "session-start"),
                                 ("pixs-pa-session", "system-stop"),
                                 ("pixs-pa-system", "unknown")):
            with self.subTest(executable=executable), self.assertRaises(ModeError):
                parse_mode(executable, ["--mode", mode])

    def test_no_implicit_identity_from_path_or_wrong_types(self):
        for executable in ("/bin/pixs-pa-system", "renamed", None, 1):
            with self.assertRaises(ModeError):
                parse_mode(executable, ["--mode", "system-daemon"])
        for arguments in ("--mode=system-daemon", None, [1], ["--mode", "system\x00daemon"]):
            with self.assertRaises(ModeError):
                parse_mode("pixs-pa-system", arguments)

    def test_diagnostic_does_not_echo_untrusted_value(self):
        marker = "untrusted-sensitive-marker"
        with self.assertRaises(ModeError) as caught:
            parse_mode("pixs-pa-system", ["--mode", marker])
        self.assertNotIn(marker, str(caught.exception))


if __name__ == "__main__":
    unittest.main()
