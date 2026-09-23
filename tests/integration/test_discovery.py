"""Test neutre de découverte du niveau d'intégration (tâche 1.3)."""

import importlib
import unittest


class TestDecouverteIntegration(unittest.TestCase):
    def test_import_paquet_noyau(self) -> None:
        module = importlib.import_module("pixs.kernel")
        self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
