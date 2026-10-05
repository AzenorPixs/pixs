"""Adhésion du vocabulaire NotificationChannel à la source canonique des cinq canaux."""

import unittest

from pixs.kernel.notifications import NotificationChannel

CANONICAL_CHANNELS = (
    ("IN_APP", "IN_APP"),
    ("EMAIL", "EMAIL"),
    ("PUSH", "PUSH"),
    ("SMS", "SMS"),
    ("WEBHOOK", "WEBHOOK"),
)


class TestNotificationChannelVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self):
        observed = tuple(
            (member.name, member.value) for member in NotificationChannel
        )
        self.assertEqual(observed, CANONICAL_CHANNELS)

    def test_no_additional_member_and_no_alias(self):
        self.assertEqual(len(NotificationChannel), 5)
        self.assertEqual(len(NotificationChannel.__members__), 5)

    def test_module_exports_only_the_vocabulary(self):
        import pixs.kernel.notifications as notifications_module

        self.assertEqual(notifications_module.__all__, ["NotificationChannel"])
        self.assertIs(notifications_module.NotificationChannel, NotificationChannel)


if __name__ == "__main__":
    unittest.main()
