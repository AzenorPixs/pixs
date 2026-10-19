"""Table normative du validateur lexical pur FrontendEntryPath v1."""

import unittest

from pixs.kernel.frontend_entry_paths import validate_frontend_entry_path_v1

MESSAGE = "FrontendEntryPath v1 invalide"

VALID_PATHS = (
    "frontend/routes/contacts",
    "contacts",
    "données/été",
    "données/été",
    " a/b",
    "a/b ",
    " a ",
    " ",
    "..hidden/route",
    "a b/c d",
    ".hidden/route",
    ".hidden",
    "a/" + "x" * 512 + "/b",
)

C0_AND_DEL = list(range(0x00, 0x20)) + [0x7F]

CLASSIC_INVALID = (
    "",
    "/a",
    "a//b",
    "/",
    "a/",
    ".",
    "..",
    "a/./b",
    "a/../b",
    "a\\b",
    "a:b",
    "a?b",
    "a#b",
    "a%b",
)

SURROGATES_INVALID = (
    "\ud800",
    "\udc00",
    "\udbff",
    "\udfff",
    "a\ud800b",
    "a\udc00b",
)


class TestFrontendEntryPathLexical(unittest.TestCase):
    def test_valid_paths_returned_equal_without_transformation(self):
        for path in VALID_PATHS:
            with self.subTest(path=path):
                self.assertEqual(validate_frontend_entry_path_v1(path), path)

    def test_classic_invalid_raise_value_error_generic(self):
        for path in CLASSIC_INVALID + SURROGATES_INVALID:
            with self.subTest(path=repr(path)):
                with self.assertRaises(ValueError) as ctx:
                    validate_frontend_entry_path_v1(path)
                self.assertEqual(str(ctx.exception), MESSAGE)
                if path != "":
                    self.assertNotIn(path, str(ctx.exception))

    def test_all_c0_and_del_rejected_at_start_middle_end(self):
        for code in C0_AND_DEL:
            ch = chr(code)
            for path in (
                ch + "ab/cd",
                "a" + ch + "b/cd",
                "ab/cd" + ch,
                "a/" + ch + "/b",
            ):
                with self.subTest(code=code, path=repr(path)):
                    with self.assertRaises(ValueError) as ctx:
                        validate_frontend_entry_path_v1(path)
                    self.assertEqual(str(ctx.exception), MESSAGE)
                    if path != "":
                        self.assertNotIn(path, str(ctx.exception))

    def test_non_strings_raise_type_error_without_coercion(self):
        for bad in (None, 123, 4.5, b"a", ["a"], {"p": "a"}):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(TypeError) as ctx:
                    validate_frontend_entry_path_v1(bad)
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_module_exports_only_the_validator(self):
        import pixs.kernel.frontend_entry_paths as module

        self.assertEqual(module.__all__, ["validate_frontend_entry_path_v1"])
        self.assertEqual(module.validate_frontend_entry_path_v1, validate_frontend_entry_path_v1)


if __name__ == "__main__":
    unittest.main()
