"""Conformité du profil identité v1 via sa façade publique."""

import dataclasses
from enum import Enum
import unittest
import uuid

from pixs.core import identity as I


def u7(n=1):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


class ModelsTest(unittest.TestCase):
    def assert_invalid_id(self, value):
        factories = (
            lambda: I.User(value),
            lambda: I.DigitalIdentity(value, I.IdentityType.HUMAN, I.IdentityState.ACTIVE),
            lambda: I.IdentityLink(value, u7(2)),
            lambda: I.IdentityLink(u7(2), value),
        )
        for factory in factories:
            with self.assertRaises(I.IdentityError):
                factory()

    def test_valid_models_and_all_vocabularies(self):
        self.assertEqual({x.value for x in I.IdentityType},
                         {"HUMAN", "SERVICE", "DEVICE", "FEDERATED"})
        self.assertEqual({x.value for x in I.IdentityState},
                         {"ACTIVE", "SUSPENDED", "REVOKED", "EXPIRED"})
        self.assertIs(I.validate_user(I.User(u7())), True)
        self.assertIs(I.validate_link(I.IdentityLink(u7(), u7(2))), True)
        for kind in I.IdentityType:
            for state in I.IdentityState:
                with self.subTest(kind=kind, state=state):
                    self.assertIs(I.validate_identity(I.DigitalIdentity(u7(), kind, state)), True)

    def test_other_uuid_versions_and_variants_rejected(self):
        for version in (1, 4, 6, 8):
            with self.subTest(version=version):
                self.assert_invalid_id(uuid.UUID(int=(version << 76) | (2 << 62) | 1))
        for variant in (0, 1, 3):
            with self.subTest(variant=variant):
                self.assert_invalid_id(uuid.UUID(int=(7 << 76) | (variant << 62) | 1))

    def test_non_uuid_and_subclasses_rejected(self):
        class SubUUID(uuid.UUID):
            pass
        for value in (str(u7()), 1, True, None, b"uuid", SubUUID(int=u7().int)):
            self.assert_invalid_id(value)

    def test_incomplete_and_altered_uuid_rejected(self):
        self.assert_invalid_id(object.__new__(uuid.UUID))
        for raw in (True, -1, 2 ** 128, "bad", None):
            with self.subTest(raw_type=type(raw).__name__):
                altered = u7()
                object.__setattr__(altered, "int", raw)
                self.assert_invalid_id(altered)

    def test_foreign_enums_and_implicit_conversions_rejected(self):
        class Foreign(Enum):
            HUMAN = "HUMAN"
            ACTIVE = "ACTIVE"
        for kind in ("HUMAN", 1, True, None, Foreign.HUMAN, I.IdentityState.ACTIVE):
            with self.assertRaises(I.IdentityError):
                I.DigitalIdentity(u7(), kind, I.IdentityState.ACTIVE)
        for state in ("ACTIVE", 1, True, None, Foreign.ACTIVE, I.IdentityType.HUMAN):
            with self.assertRaises(I.IdentityError):
                I.DigitalIdentity(u7(), I.IdentityType.HUMAN, state)

    def test_incomplete_and_wrong_model_classes_rejected(self):
        cases = ((I.User, I.validate_user), (I.DigitalIdentity, I.validate_identity),
                 (I.IdentityLink, I.validate_link))
        for cls, validate in cases:
            with self.subTest(model=cls.__name__):
                for value in (None, (), "synthetic-invalid", object.__new__(cls)):
                    with self.assertRaises(I.IdentityError):
                        validate(value)
                subclass = type("Subclass", (cls,), {})
                with self.assertRaises(I.IdentityError):
                    validate(object.__new__(subclass))

    def test_altered_fields_are_revalidated(self):
        cases = (
            (I.User(u7()), I.validate_user, "user_id", "bad"),
            (I.DigitalIdentity(u7(), I.IdentityType.HUMAN, I.IdentityState.ACTIVE),
             I.validate_identity, "identity_id", "bad"),
            (I.DigitalIdentity(u7(), I.IdentityType.HUMAN, I.IdentityState.ACTIVE),
             I.validate_identity, "identity_type", "HUMAN"),
            (I.DigitalIdentity(u7(), I.IdentityType.HUMAN, I.IdentityState.ACTIVE),
             I.validate_identity, "state", "ACTIVE"),
            (I.IdentityLink(u7(), u7(2)), I.validate_link, "user_id", "bad"),
            (I.IdentityLink(u7(), u7(2)), I.validate_link, "identity_id", "bad"),
        )
        for value, validate, field, bad in cases:
            object.__setattr__(value, field, bad)
            with self.assertRaises(I.IdentityError):
                validate(value)

    def test_all_models_are_frozen_and_slotted(self):
        cases = ((I.User(u7()), "user_id", u7(2)),
                 (I.DigitalIdentity(u7(), I.IdentityType.SERVICE, I.IdentityState.ACTIVE),
                  "state", I.IdentityState.REVOKED),
                 (I.IdentityLink(u7(), u7(2)), "identity_id", u7(3)))
        for value, field, replacement in cases:
            self.assertFalse(hasattr(value, "__dict__"))
            with self.assertRaises(dataclasses.FrozenInstanceError):
                setattr(value, field, replacement)
            self.assertNotIn(str(u7()), repr(value))

    def test_errors_do_not_echo_invalid_values(self):
        marker = "synthetic-sensitive-marker"
        with self.assertRaises(I.IdentityError) as caught:
            I.User(marker)
        self.assertEqual(caught.exception.code, "IDENTITY_INVALID")
        self.assertEqual(str(caught.exception), "Identite minimale invalide.")
        self.assertNotIn(marker, repr(caught.exception))

    def test_hostile_methods_are_never_called(self):
        calls = []
        class Evil:
            def fail(self, name):
                calls.append(name)
                raise AssertionError(name)
            def __str__(self):
                return self.fail("str")
            def __repr__(self):
                return self.fail("repr")
            def __eq__(self, other):
                return self.fail("eq")
            def __hash__(self):
                return self.fail("hash")
        evil = Evil()
        self.assert_invalid_id(evil)
        for kind, state in ((evil, I.IdentityState.ACTIVE), (I.IdentityType.HUMAN, evil)):
            with self.assertRaises(I.IdentityError):
                I.DigitalIdentity(u7(), kind, state)
        altered = u7()
        object.__setattr__(altered, "int", evil)
        self.assert_invalid_id(altered)
        for validate in (I.validate_user, I.validate_identity, I.validate_link):
            with self.assertRaises(I.IdentityError):
                validate(evil)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
