"""Adhésion du vocabulaire NotificationDeliveryState à la source canonique des six états."""

import unittest

from pixs.kernel.notification_delivery import NotificationDeliveryState

CANONICAL_STATES = (
    ("QUEUED", "QUEUED"),
    ("SENDING", "SENDING"),
    ("SENT", "SENT"),
    ("DELIVERED", "DELIVERED"),
    ("FAILED", "FAILED"),
    ("CANCELLED", "CANCELLED"),
)


class TestNotificationDeliveryStateVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self):
        observed = tuple(
            (member.name, member.value) for member in NotificationDeliveryState
        )
        self.assertEqual(observed, CANONICAL_STATES)

    def test_no_additional_member_and_no_alias(self):
        self.assertEqual(len(NotificationDeliveryState), 6)
        self.assertEqual(len(NotificationDeliveryState.__members__), 6)

    def test_module_exports_only_the_vocabulary(self):
        import pixs.kernel.notification_delivery as delivery_module

        self.assertEqual(delivery_module.__all__, ["NotificationDeliveryState"])
        self.assertIs(delivery_module.NotificationDeliveryState, NotificationDeliveryState)


if __name__ == "__main__":
    unittest.main()
