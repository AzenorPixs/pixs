"""Table comportementale du validateur composite FrontendContributionDeclaration v1."""

import traceback
import unittest

from pixs.kernel.frontend_contribution_declarations import (
    validate_frontend_contribution_declaration_v1,
)

MESSAGE = "FrontendContributionDeclaration v1 invalide"
SENTINEL_NO_ECHO = "SENTINELLE_XYZ_789.SENTINELLE/XYZ_789"

CANONICAL_TYPES = (
    "ROUTE",
    "PAGE",
    "NAVIGATION",
    "COMPONENT",
    "FORM",
    "TRANSLATION",
    "UI_PERMISSION",
    "UI_SLOT",
)

CANONICAL_SCOPES = (
    "PUBLIC",
    "AUTHENTICATED",
    "TENANT_SCOPED",
    "PLATFORM_SCOPED",
)


def make_valid(**overrides):
    base = {
        "type": "ROUTE",
        "id": "acme.crm.contacts",
        "entry": "frontend/routes/contacts",
        "version": "1.0.0",
        "requires": [],
        "scope": "PUBLIC",
    }
    base.update(overrides)
    return base


class EvilStr(str):
    calls = 0

    def __str__(self):
        type(self).calls += 1
        raise AssertionError("coercition __str__ interdite")

    def __repr__(self):
        type(self).calls += 1
        raise AssertionError("coercition __repr__ interdite")

    def __hash__(self):
        type(self).calls += 1
        raise AssertionError("hachage interdit")

    def __eq__(self, other):
        type(self).calls += 1
        raise AssertionError("egalite interdite")


class EvilDict(dict):
    calls = 0

    def __iter__(self):
        type(self).calls += 1
        raise AssertionError("iteration interdite")

    def keys(self):
        type(self).calls += 1
        raise AssertionError("acces keys interdit")

    def __getitem__(self, key):
        type(self).calls += 1
        raise AssertionError("acces getitem interdit")

    def copy(self):
        type(self).calls += 1
        raise AssertionError("acces copy interdit")


class EvilList(list):
    calls = 0

    def __iter__(self):
        type(self).calls += 1
        raise AssertionError("iteration interdite")

    def __len__(self):
        type(self).calls += 1
        raise AssertionError("acces len interdit")

    def __getitem__(self, index):
        type(self).calls += 1
        raise AssertionError("acces getitem interdit")


class TrapObject:
    calls = 0

    def __str__(self):
        type(self).calls += 1
        raise AssertionError("coercition __str__ interdite")

    def __repr__(self):
        type(self).calls += 1
        raise AssertionError("coercition __repr__ interdite")

    def __hash__(self):
        type(self).calls += 1
        raise AssertionError("hachage interdit")

    def __eq__(self, other):
        type(self).calls += 1
        raise AssertionError("egalite interdite")


class HashCountingKey:
    hash_calls = 0
    eq_calls = 0

    def __hash__(self):
        type(self).hash_calls += 1
        return 1234567

    def __eq__(self, other):
        type(self).eq_calls += 1
        return self is other


class SpoofedClass:
    class_calls = 0

    @property
    def __class__(self):
        type(self).class_calls += 1
        raise AssertionError("acces __class__ interdit")


class TestFrontendContributionDeclarationValid(unittest.TestCase):
    def test_all_types_and_scopes_accepted_without_resolution(self):
        for type_name in CANONICAL_TYPES:
            for scope in CANONICAL_SCOPES:
                with self.subTest(type=type_name, scope=scope):
                    snapshot = validate_frontend_contribution_declaration_v1(
                        make_valid(type=type_name, scope=scope)
                    )
                    self.assertEqual(snapshot.type, type_name)
                    self.assertEqual(snapshot.scope, scope)
                    self.assertEqual(snapshot.id, "acme.crm.contacts")
                    self.assertEqual(snapshot.entry, "frontend/routes/contacts")
                    self.assertEqual(snapshot.version, "1.0.0")
                    self.assertEqual(snapshot.requires, ())

    def test_texts_order_duplicates_and_pixs_contacts_preserved(self):
        declaration = make_valid(
            type="PAGE",
            id="pixs.contacts",
            entry="frontend/routes/contacts",
            version="1.2.3-alpha.1+build.11",
            requires=["pkg-a >=1.0.0", "pkg-b ==2.0.0", "pkg-a >=1.0.0"],
            scope="TENANT_SCOPED",
        )
        snapshot = validate_frontend_contribution_declaration_v1(declaration)
        self.assertEqual(snapshot.id, "pixs.contacts")
        self.assertEqual(snapshot.version, "1.2.3-alpha.1+build.11")
        self.assertEqual(
            snapshot.requires,
            ("pkg-a >=1.0.0", "pkg-b ==2.0.0", "pkg-a >=1.0.0"),
        )
        self.assertIs(type(snapshot.requires), tuple)

    def test_casing_preserved(self):
        snapshot = validate_frontend_contribution_declaration_v1(
            make_valid(id="ACME.crm-2.contacts_1")
        )
        self.assertEqual(snapshot.id, "ACME.crm-2.contacts_1")
        self.assertNotEqual(snapshot.id, "acme.crm-2.contacts_1")

    def test_version_spellings_refused(self):
        for version in ("^1.0.0", ">=1.0.0", "1.0"):
            with self.subTest(version=version):
                with self.assertRaises(ValueError) as ctx:
                    validate_frontend_contribution_declaration_v1(
                        make_valid(version=version)
                    )
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_requires_spellings_refused(self):
        for expression in (
            "pkg-a ^1.0.0",
            "pkg-b ~1.2.0",
            "pkg-c *",
            "pkg-a >=1.0.0 || pkg-a ==2.0.0",
        ):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError) as ctx:
                    validate_frontend_contribution_declaration_v1(
                        make_valid(requires=[expression])
                    )
                self.assertEqual(str(ctx.exception), MESSAGE)


class TestFrontendContributionDeclarationShape(unittest.TestCase):
    def test_non_dict_inputs_refused_without_hooks(self):
        TrapObject.calls = 0
        EvilStr.calls = 0
        SpoofedClass.class_calls = 0
        for bad in (None, 123, "x", b"x", ["type"], ("type",), TrapObject(), SpoofedClass()):
            with self.subTest():
                with self.assertRaises(TypeError) as ctx:
                    validate_frontend_contribution_declaration_v1(bad)
                self.assertEqual(str(ctx.exception), MESSAGE)
        self.assertEqual(TrapObject.calls, 0)
        self.assertEqual(EvilStr.calls, 0)
        self.assertEqual(SpoofedClass.class_calls, 0)

    def test_dict_subclass_refused_without_hooks(self):
        evil = EvilDict(make_valid())
        EvilDict.calls = 0
        with self.subTest():
            with self.assertRaises(TypeError) as ctx:
                validate_frontend_contribution_declaration_v1(evil)
            self.assertEqual(str(ctx.exception), MESSAGE)
        self.assertEqual(EvilDict.calls, 0)

    def test_missing_extra_and_empty_refused(self):
        base = make_valid()
        missing = dict(base)
        del missing["scope"]
        with self.assertRaises(ValueError) as ctx:
            validate_frontend_contribution_declaration_v1(missing)
        self.assertEqual(str(ctx.exception), MESSAGE)
        extra = dict(base)
        extra["extra"] = "x"
        with self.assertRaises(ValueError) as ctx:
            validate_frontend_contribution_declaration_v1(extra)
        self.assertEqual(str(ctx.exception), MESSAGE)
        with self.assertRaises(ValueError) as ctx:
            validate_frontend_contribution_declaration_v1({})
        self.assertEqual(str(ctx.exception), MESSAGE)

    def test_non_str_key_refused_before_set(self):
        key = HashCountingKey()
        hostile = {key: "x", "type": "x", "id": "x", "entry": "x", "version": "x", "requires": [], "scope": "x"}
        HashCountingKey.hash_calls = 0
        HashCountingKey.eq_calls = 0
        with self.subTest():
            with self.assertRaises(TypeError) as ctx:
                validate_frontend_contribution_declaration_v1(hostile)
            self.assertEqual(str(ctx.exception), MESSAGE)
        self.assertEqual(HashCountingKey.hash_calls, 0)
        self.assertEqual(HashCountingKey.eq_calls, 0)

    def test_bad_text_field_types_without_coercion(self):
        for field in ("type", "id", "entry", "version", "scope"):
            for bad in (None, 123, 4.5, b"x", ["x"], {"x": "y"}, TrapObject()):
                TrapObject.calls = 0
                with self.subTest():
                    candidate = make_valid(**{field: bad})
                    with self.assertRaises(TypeError) as ctx:
                        validate_frontend_contribution_declaration_v1(candidate)
                    self.assertEqual(str(ctx.exception), MESSAGE)
                self.assertEqual(TrapObject.calls, 0)

    def test_str_subclass_fields_refused_without_hooks(self):
        for field, text in (
            ("type", "ROUTE"),
            ("id", "acme.crm.contacts"),
            ("entry", "frontend/routes/contacts"),
            ("version", "1.0.0"),
            ("scope", "PUBLIC"),
        ):
            EvilStr.calls = 0
            candidate = make_valid(**{field: EvilStr(text)})
            with self.subTest(field=field):
                with self.assertRaises(TypeError) as ctx:
                    validate_frontend_contribution_declaration_v1(candidate)
                self.assertEqual(str(ctx.exception), MESSAGE)
            self.assertEqual(EvilStr.calls, 0)

    def test_requires_must_be_exact_list_without_hooks(self):
        evil = EvilList([])
        EvilList.calls = 0
        with self.subTest():
            with self.assertRaises(TypeError) as ctx:
                validate_frontend_contribution_declaration_v1(make_valid(requires=evil))
            self.assertEqual(str(ctx.exception), MESSAGE)
        self.assertEqual(EvilList.calls, 0)
        for bad in (None, "x", b"x", ("pkg-a >=1.0.0",), {"x"}, {"r": []}):
            with self.subTest():
                with self.assertRaises(TypeError) as ctx:
                    validate_frontend_contribution_declaration_v1(make_valid(requires=bad))
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_requires_elements_must_be_exact_str_without_hooks(self):
        TrapObject.calls = 0
        EvilStr.calls = 0
        for bad in ([None], [123], [b"x"], [["x"]], [TrapObject()], [EvilStr("pkg-a >=1.0.0")]):
            with self.subTest():
                with self.assertRaises(TypeError) as ctx:
                    validate_frontend_contribution_declaration_v1(make_valid(requires=bad))
                self.assertEqual(str(ctx.exception), MESSAGE)
        self.assertEqual(TrapObject.calls, 0)
        self.assertEqual(EvilStr.calls, 0)


class TestFrontendContributionDeclarationGrammars(unittest.TestCase):
    def test_invalid_shared_grammars_raise_generic(self):
        cases = [
            make_valid(type="UNKNOWN_TYPE"),
            make_valid(id="a"),
            make_valid(entry="/a"),
            make_valid(version=""),
            make_valid(requires=[""]),
            make_valid(scope="UNKNOWN"),
        ]
        for candidate in cases:
            with self.subTest():
                with self.assertRaises(ValueError) as ctx:
                    validate_frontend_contribution_declaration_v1(candidate)
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_scope_aliases_and_casing_refused(self):
        for scope in ("public", "Public", "PUBLIC ", "ADMIN", ""):
            with self.subTest(scope=scope):
                with self.assertRaises(ValueError) as ctx:
                    validate_frontend_contribution_declaration_v1(make_valid(scope=scope))
                self.assertEqual(str(ctx.exception), MESSAGE)

    def test_sentinel_proves_no_echo_in_message_and_traceback(self):
        for candidate in (
            make_valid(id=SENTINEL_NO_ECHO),
            make_valid(version=SENTINEL_NO_ECHO),
            make_valid(requires=[SENTINEL_NO_ECHO]),
            make_valid(scope=SENTINEL_NO_ECHO),
        ):
            with self.subTest():
                try:
                    validate_frontend_contribution_declaration_v1(candidate)
                except ValueError as exc:
                    self.assertEqual(str(exc), MESSAGE)
                    self.assertNotIn(SENTINEL_NO_ECHO, str(exc))
                    formatted = "".join(
                        traceback.format_exception(type(exc), exc, exc.__traceback__)
                    )
                    self.assertNotIn(SENTINEL_NO_ECHO, formatted)
                    self.assertIsNone(exc.__cause__)
                else:
                    self.fail("ValueError attendue")


class TestFrontendContributionDeclarationSnapshot(unittest.TestCase):
    def test_input_unchanged_then_mutations_detached(self):
        declaration = make_valid(requires=["pkg-a >=1.0.0"])
        before = dict(declaration)
        requires_before = list(declaration["requires"])
        snapshot = validate_frontend_contribution_declaration_v1(declaration)
        self.assertEqual(declaration, before)
        self.assertEqual(declaration["requires"], requires_before)
        declaration["type"] = "PAGE"
        declaration["requires"].append("pkg-b ==2.0.0")
        self.assertEqual(snapshot.type, "ROUTE")
        self.assertEqual(snapshot.requires, ("pkg-a >=1.0.0",))
        self.assertEqual(declaration["type"], "PAGE")
        self.assertEqual(declaration["requires"], ["pkg-a >=1.0.0", "pkg-b ==2.0.0"])
        self.assertEqual(before["type"], "ROUTE")
        self.assertEqual(requires_before, ["pkg-a >=1.0.0"])
        self.assertEqual(declaration["id"], before["id"])
        with self.assertRaises(AttributeError):
            snapshot.type = "PAGE"  # type: ignore[misc]

    def test_module_exports_only_the_validator(self):
        import pixs.kernel.frontend_contribution_declarations as module

        self.assertEqual(
            module.__all__, ["validate_frontend_contribution_declaration_v1"]
        )
        self.assertIs(
            module.validate_frontend_contribution_declaration_v1,
            validate_frontend_contribution_declaration_v1,
        )


if __name__ == "__main__":
    unittest.main()
