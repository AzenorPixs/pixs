"""Intégration synthétique du vocabulaire, sans autorisation de production."""

import unittest

from pixs.backend.bulk_authority_action import BulkAuthorityAction
from pixs.kernel.diagnostics import VALIDATE
from unit.test_bulk_trusted_ports import _Authority, _compose


class BulkAuthorityActionIntegrationTests(unittest.TestCase):
    def test_explicit_value_reaches_synthetic_port_unchanged(self):
        for action in BulkAuthorityAction:
            with self.subTest(action=action.name):
                authority = _Authority()
                bundle, _ = _compose(authority)
                server_context = object()
                result, diagnostics = bundle.check_authority(
                    server_context=server_context, action=action.value,
                    operation_reference="operation-test", resource_reference=None,
                )
                self.assertEqual(diagnostics, [])
                self.assertIsNotNone(result)
                self.assertEqual(len(authority.calls), 1)
                self.assertIs(authority.calls[0][0], server_context)
                self.assertIs(authority.calls[0][1], action.value)
                self.assertEqual(authority.calls[0][2:], ("operation-test", None))

    def test_enum_is_refused_before_synthetic_provider(self):
        for action in BulkAuthorityAction:
            with self.subTest(action=action.name):
                authority = _Authority()
                bundle, _ = _compose(authority)
                result, diagnostics = bundle.check_authority(
                    server_context=object(), action=action,
                    operation_reference="operation-test", resource_reference=None,
                )
                self.assertIsNone(result)
                self.assertTrue(diagnostics)
                self.assertTrue(all(item.step == VALIDATE for item in diagnostics))
                self.assertEqual(authority.calls, [])


if __name__ == "__main__":
    unittest.main()
