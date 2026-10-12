"""Adhesion du controle declaratif des destinataires Notification au scenario canonique."""

import unittest

import pixs.kernel.notification_delivery as delivery_module
import pixs.kernel.notification_recipient_declaration as declaration_module
import pixs.kernel.notifications as notifications_module
from pixs.kernel.notification_recipient_declaration import (
    NotificationRecipientDeclarationError,
    require_declared_notification_recipient,
)


class _Hostile:
    def __init__(self):
        self.eq_calls = 0
        self.hash_calls = 0
        self.str_calls = 0
        self.repr_calls = 0

    def __eq__(self, other):
        self.eq_calls += 1
        return NotImplemented

    def __hash__(self):
        self.hash_calls += 1
        return 3

    def __str__(self):
        self.str_calls += 1
        return "HOSTILE_STR_MARKER"

    def __repr__(self):
        self.repr_calls += 1
        return "HOSTILE_REPR_MARKER"


class _SubStr(str):
    pass


class _ExactFrozensetSubclass(frozenset):
    pass


class TestRequireDeclaredNotificationRecipient(unittest.TestCase):
    def test_declared_key_is_returned_identical(self):
        for key in ("ALPHA", "root:recipient:1"):
            declared = frozenset({key})
            self.assertIs(
                require_declared_notification_recipient(key, declared), key
            )

    def test_same_value_distinct_object_accepted_and_returns_input_object(self):
        declared = frozenset({"ALPHA BETA"})
        candidate = "".join(["ALPHA ", "BETA"])
        self.assertIsNot(candidate, next(iter(declared)))
        self.assertIs(
            require_declared_notification_recipient(candidate, declared), candidate
        )

    def test_case_and_spacing_are_not_normalized(self):
        declared = frozenset({"Alpha BETA "})
        result = require_declared_notification_recipient("Alpha BETA ", declared)
        self.assertEqual(result, "Alpha BETA ")
        self.assertTrue(result.endswith(" "))
        for key in ("alpha BETA ", "ALPHA BETA ", "Alpha BETA", " Alpha BETA "):
            with self.assertRaises(NotificationRecipientDeclarationError):
                require_declared_notification_recipient(key, declared)

    def test_empty_declaration_refuses_canonical_keys(self):
        for key in ("ALPHA", "root:recipient:1"):
            with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
                require_declared_notification_recipient(key, frozenset())
            self.assertNotIn("ALPHA", str(ctx.exception))
            self.assertNotIn("root", str(ctx.exception))

    def test_invalid_key_types_refused_without_coercion(self):
        declared = frozenset({"ALPHA", "0", "1", "None", "True"})
        for key in (
            "",
            None,
            True,
            False,
            0,
            1,
            b"ALPHA",
            ["ALPHA"],
            _SubStr("ALPHA"),
            object(),
        ):
            with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
                require_declared_notification_recipient(key, declared)
            self.assertNotIn("ALPHA", str(ctx.exception))

    def test_declaration_type_must_be_exact_frozenset(self):
        for declared in (
            {"ALPHA"},
            ["ALPHA"],
            ("ALPHA",),
            _ExactFrozensetSubclass({"ALPHA"}),
            "ALPHA",
            None,
        ):
            with self.assertRaises(NotificationRecipientDeclarationError):
                require_declared_notification_recipient("ALPHA", declared)

    def test_invalid_declared_elements_refused_even_when_key_declared(self):
        for declared in (
            frozenset({"ALPHA", ""}),
            frozenset({"ALPHA", None}),
            frozenset({"ALPHA", True}),
            frozenset({"ALPHA", 1}),
            frozenset({"ALPHA", _SubStr("BETA")}),
        ):
            with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
                require_declared_notification_recipient("ALPHA", declared)
            self.assertNotIn("ALPHA", str(ctx.exception))
            self.assertNotIn("BETA", str(ctx.exception))

    def test_hostile_element_hash_only_from_caller_construction(self):
        hostile = _Hostile()
        declared = frozenset({hostile, "ALPHA"})
        self.assertEqual(
            (hostile.eq_calls, hostile.hash_calls, hostile.str_calls, hostile.repr_calls),
            (0, 1, 0, 0),
        )
        with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
            require_declared_notification_recipient("ALPHA", declared)
        self.assertEqual(
            (hostile.eq_calls, hostile.hash_calls, hostile.str_calls, hostile.repr_calls),
            (0, 1, 0, 0),
        )
        self.assertNotIn("HOSTILE", str(ctx.exception))

    def test_hostile_key_never_invokes_dunders(self):
        hostile = _Hostile()
        with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
            require_declared_notification_recipient(hostile, frozenset({"ALPHA"}))
        self.assertEqual(hostile.eq_calls, 0)
        self.assertEqual(hostile.hash_calls, 0)
        self.assertEqual(hostile.str_calls, 0)
        self.assertEqual(hostile.repr_calls, 0)
        message = str(ctx.exception)
        self.assertTrue(message)
        self.assertNotIn("HOSTILE", message)

    def test_refusal_messages_do_not_echo_inputs(self):
        with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
            require_declared_notification_recipient(
                "SECRET-KEY", frozenset({"OTHER-ENTRY"})
            )
        message = str(ctx.exception)
        self.assertTrue(message)
        self.assertNotIn("SECRET", message)
        self.assertNotIn("OTHER", message)

    def test_signature_error_remains_standard_type_error(self):
        with self.assertRaises(TypeError):
            require_declared_notification_recipient("ALPHA")

    def test_error_is_a_value_error(self):
        self.assertTrue(
            issubclass(NotificationRecipientDeclarationError, ValueError)
        )

    def test_module_exports_only_error_and_helper(self):
        self.assertEqual(
            declaration_module.__all__,
            [
                "NotificationRecipientDeclarationError",
                "require_declared_notification_recipient",
            ],
        )
        self.assertIs(
            declaration_module.require_declared_notification_recipient,
            require_declared_notification_recipient,
        )
        self.assertIs(
            declaration_module.NotificationRecipientDeclarationError,
            NotificationRecipientDeclarationError,
        )

    def test_delivered_surfaces_are_preserved(self):
        self.assertEqual(notifications_module.__all__, ["NotificationChannel"])
        self.assertEqual(delivery_module.__all__, ["NotificationDeliveryState"])


if __name__ == "__main__":
    unittest.main()
