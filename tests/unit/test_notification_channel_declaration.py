"""Adhesion du controle declaratif NotificationChannel au scenario canonique."""

import enum
import unittest

import pixs.kernel.notification_channel_declaration as declaration_module
import pixs.kernel.notification_delivery as delivery_module
import pixs.kernel.notifications as notifications_module
from pixs.kernel.notification_channel_declaration import (
    NotificationChannelDeclarationError,
    require_declared_notification_channel,
)
from pixs.kernel.notifications import NotificationChannel

ALL_DECLARED = frozenset(NotificationChannel)


class _OtherChannel(enum.Enum):
    EMAIL = "EMAIL"


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
        return 1

    def __str__(self):
        self.str_calls += 1
        return "HOSTILE_STR_MARKER"

    def __repr__(self):
        self.repr_calls += 1
        return "HOSTILE_REPR_MARKER"


class TestRequireDeclaredNotificationChannel(unittest.TestCase):
    def test_declared_members_are_returned_identical(self):
        for member in NotificationChannel:
            self.assertIs(
                require_declared_notification_channel(member, ALL_DECLARED), member
            )

    def test_canonical_member_not_declared_is_refused_without_echo(self):
        declared = frozenset({NotificationChannel.EMAIL})
        with self.assertRaises(NotificationChannelDeclarationError) as ctx:
            require_declared_notification_channel(NotificationChannel.SMS, declared)
        self.assertNotIn("SMS", str(ctx.exception))
        self.assertNotIn("EMAIL", str(ctx.exception))

    def test_empty_declaration_refuses_every_canonical_member(self):
        for member in NotificationChannel:
            with self.assertRaises(NotificationChannelDeclarationError):
                require_declared_notification_channel(member, frozenset())

    def test_channels_outside_enum_are_refused_without_coercion(self):
        for channel in ("EMAIL", "email", None, 0, _OtherChannel.EMAIL):
            with self.assertRaises(NotificationChannelDeclarationError) as ctx:
                require_declared_notification_channel(channel, ALL_DECLARED)
            self.assertNotIn("EMAIL", str(ctx.exception))

    def test_invalid_declaration_refused_even_when_channel_declared(self):
        for declared in (
            frozenset({NotificationChannel.EMAIL, "EMAIL"}),
            frozenset({None}),
        ):
            with self.assertRaises(NotificationChannelDeclarationError):
                require_declared_notification_channel(
                    NotificationChannel.EMAIL, declared
                )

    def test_declaration_type_must_be_exact_frozenset(self):
        class ExactSubclass(frozenset):
            pass

        for declared in (
            set(NotificationChannel),
            tuple(NotificationChannel),
            list(NotificationChannel),
            {member.value for member in NotificationChannel},
            "EMAIL",
            None,
            ExactSubclass(NotificationChannel),
        ):
            with self.assertRaises(NotificationChannelDeclarationError):
                require_declared_notification_channel(
                    NotificationChannel.EMAIL, declared
                )

    def test_helper_does_not_invoke_dunders_of_unvalidated_element(self):
        hostile = _Hostile()
        declared = frozenset({hostile, NotificationChannel.EMAIL})
        observed = (
            hostile.eq_calls,
            hostile.hash_calls,
            hostile.str_calls,
            hostile.repr_calls,
        )
        with self.assertRaises(NotificationChannelDeclarationError) as ctx:
            require_declared_notification_channel(NotificationChannel.EMAIL, declared)
        self.assertEqual(
            (
                hostile.eq_calls,
                hostile.hash_calls,
                hostile.str_calls,
                hostile.repr_calls,
            ),
            observed,
        )
        self.assertNotIn("HOSTILE", str(ctx.exception))

    def test_helper_does_not_invoke_dunders_of_unvalidated_channel(self):
        hostile = _Hostile()
        with self.assertRaises(NotificationChannelDeclarationError) as ctx:
            require_declared_notification_channel(hostile, ALL_DECLARED)
        self.assertEqual(hostile.eq_calls, 0)
        self.assertEqual(hostile.hash_calls, 0)
        self.assertEqual(hostile.str_calls, 0)
        self.assertEqual(hostile.repr_calls, 0)
        message = str(ctx.exception)
        self.assertTrue(message)
        self.assertNotIn("HOSTILE", message)

    def test_signature_error_remains_standard_type_error(self):
        with self.assertRaises(TypeError):
            require_declared_notification_channel(NotificationChannel.EMAIL)

    def test_error_is_a_value_error(self):
        self.assertTrue(
            issubclass(NotificationChannelDeclarationError, ValueError)
        )

    def test_module_exports_only_error_and_helper(self):
        self.assertEqual(
            declaration_module.__all__,
            [
                "NotificationChannelDeclarationError",
                "require_declared_notification_channel",
            ],
        )
        self.assertIs(
            declaration_module.require_declared_notification_channel,
            require_declared_notification_channel,
        )
        self.assertIs(
            declaration_module.NotificationChannelDeclarationError,
            NotificationChannelDeclarationError,
        )

    def test_delivered_surfaces_are_preserved(self):
        self.assertEqual(notifications_module.__all__, ["NotificationChannel"])
        self.assertIs(notifications_module.NotificationChannel, NotificationChannel)
        self.assertEqual(
            delivery_module.__all__, ["NotificationDeliveryState"]
        )


if __name__ == "__main__":
    unittest.main()
