"""Adhésion du vocabulaire FrontendContributionType à la source canonique des huit types."""

import unittest

from pixs.kernel.frontend_contribution_types import FrontendContributionType

CANONICAL_TYPES = (
    ("ROUTE", "ROUTE"),
    ("PAGE", "PAGE"),
    ("NAVIGATION", "NAVIGATION"),
    ("COMPONENT", "COMPONENT"),
    ("FORM", "FORM"),
    ("TRANSLATION", "TRANSLATION"),
    ("UI_PERMISSION", "UI_PERMISSION"),
    ("UI_SLOT", "UI_SLOT"),
)


class TestFrontendContributionTypeVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self):
        observed = tuple(
            (member.name, member.value) for member in FrontendContributionType
        )
        self.assertEqual(observed, CANONICAL_TYPES)

    def test_no_additional_member_and_no_alias(self):
        self.assertEqual(len(FrontendContributionType), 8)
        self.assertEqual(len(FrontendContributionType.__members__), 8)

    def test_module_exports_only_the_vocabulary(self):
        import pixs.kernel.frontend_contribution_types as types_module

        self.assertEqual(types_module.__all__, ["FrontendContributionType"])
        self.assertIs(types_module.FrontendContributionType, FrontendContributionType)


if __name__ == "__main__":
    unittest.main()
