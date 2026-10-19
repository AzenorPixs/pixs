"""Table normative du validateur lexical pur FrontendContributionId v1."""

import unittest

from pixs.kernel.frontend_contribution_ids import (
    validate_frontend_contribution_id_v1,
)

MESSAGE = "FrontendContributionId v1 invalide"
SENTINEL_NO_ECHO = "SENTINELLE_XYZ_789.SENTINELLE/XYZ_789"

VALID_IDS = (
    "acme.crm.contacts",
    "ACME.crm-2.contacts_1",
    "pixs.contacts",
    "-._",
    "a.B-c_d.e9",
    "0.a",
    "A.0",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.A",
    "a." + "x" * 512 + ".b",
)

INVALID_IDS = (
    "",
    "a",
    ".a",
    "a.",
    "a..b",
    ".",
    "..",
    "a b.c",
    " a.b",
    "a.b ",
    "a\tb.c",
    "a\nb.c",
    "a\x00b.c",
    "a\x7fb.c",
    "données.été",
    "aé.c",
    "a.cé",
    "a․b.c",
    "a。b.c",
    "a/b.c",
    "a\\b.c",
    "a:b.c",
    "a?b.c",
    "a#b.c",
    "a%b.c",
    "a@b.c",
    "a!b.c",
    "a,b.c",
    "a;b.c",
    "a'b.c",
    'a"b.c',
    "a(b.c",
    "a[b.c",
    "a{b.c",
    "a+b.c",
    "a=b.c",
    "a*b.c",
    "a&b.c",
    "a|b.c",
    "a$.c",
    "a€.c",
    "\ud800.c",
)


class EvilSplitStr(str):
    """Sous-classe str dont le hook split doit rester inutilisé."""

    split_calls = 0

    def split(self, sep: str | None = None, maxsplit: int = -1) -> list[str]:
        type(self).split_calls += 1
        raise AssertionError("répartition vers .split utilisateur interdite")


class TrapStr:
    """Non-str dont la coercition magique doit rester inutilisée."""

    def __str__(self) -> str:
        raise AssertionError("coercition __str__ interdite")

    def __repr__(self) -> str:
        return "TrapStr()"


class SpoofedClass:
    """Objet non-str dont l'attribut __class__ reste inutilisé."""

    @property
    def __class__(self) -> type:
        raise AssertionError("accès __class__ interdit")


class TestFrontendContributionIdLexical(unittest.TestCase):
    def test_valid_ids_returned_textually_equal_without_transformation(self):
        for candidate in VALID_IDS:
            with self.subTest(candidate=candidate):
                self.assertEqual(
                    validate_frontend_contribution_id_v1(candidate), candidate
                )

    def test_casing_preserved(self):
        self.assertEqual(
            validate_frontend_contribution_id_v1("ACME.crm-2.contacts_1"),
            "ACME.crm-2.contacts_1",
        )
        self.assertNotEqual(
            validate_frontend_contribution_id_v1("ACME.crm-2.contacts_1"),
            "acme.crm-2.contacts_1",
        )

    def test_invalid_ids_raise_value_error_generic(self):
        for candidate in INVALID_IDS:
            with self.subTest(candidate=repr(candidate)):
                with self.assertRaises(ValueError) as ctx:
                    validate_frontend_contribution_id_v1(candidate)
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_sentinel_proves_no_echo(self):
        with self.assertRaises(ValueError) as ctx:
            validate_frontend_contribution_id_v1(SENTINEL_NO_ECHO)
        self.assertEqual(str(ctx.exception), MESSAGE)
        self.assertNotIn(SENTINEL_NO_ECHO, str(ctx.exception))

    def test_all_c0_and_del_rejected_in_segments(self):
        for code in list(range(0x00, 0x20)) + [0x7F]:
            char = chr(code)
            for candidate in (
                char + "a.bc",
                "a" + char + ".bc",
                "ab." + char + "c",
            ):
                with self.subTest(code=code, candidate=repr(candidate)):
                    with self.assertRaises(ValueError) as ctx:
                        validate_frontend_contribution_id_v1(candidate)
                    self.assertEqual(str(ctx.exception), MESSAGE)

    def test_non_strings_raise_type_error_without_coercion(self):
        for bad in (None, 123, 4.5, b"a.c", ["a.c"], {"id": "a.c"}, TrapStr()):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(TypeError) as ctx:
                    validate_frontend_contribution_id_v1(bad)
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_spoofed_class_attribute_does_not_bypass_real_type_check(self):
        spoofed = SpoofedClass()
        with self.assertRaises(TypeError) as ctx:
            validate_frontend_contribution_id_v1(spoofed)
        self.assertEqual(str(ctx.exception), MESSAGE)

    def test_str_subclass_split_hook_never_dispatched(self):
        EvilSplitStr.split_calls = 0
        candidate = EvilSplitStr("acme.crm.contacts")
        result = validate_frontend_contribution_id_v1(candidate)
        self.assertEqual(result, "acme.crm.contacts")
        self.assertEqual(EvilSplitStr.split_calls, 0)

    def test_module_exports_only_the_validator(self):
        import pixs.kernel.frontend_contribution_ids as module

        self.assertEqual(
            module.__all__, ["validate_frontend_contribution_id_v1"]
        )
        self.assertEqual(
            module.validate_frontend_contribution_id_v1,
            validate_frontend_contribution_id_v1,
        )


if __name__ == "__main__":
    unittest.main()
