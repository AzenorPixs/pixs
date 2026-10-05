"""Adhésion du vocabulaire JobState à la source canonique des neuf états."""

import unittest

from pixs.kernel.jobs import JobState

CANONICAL_STATES = (
    ("PENDING", "PENDING"),
    ("SCHEDULED", "SCHEDULED"),
    ("RUNNING", "RUNNING"),
    ("SUCCEEDED", "SUCCEEDED"),
    ("RETRYING", "RETRYING"),
    ("FAILED", "FAILED"),
    ("PAUSED", "PAUSED"),
    ("CANCELLED", "CANCELLED"),
    ("DEAD_LETTER", "DEAD_LETTER"),
)


class TestJobStateVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self):
        observed = tuple(
            (member.name, member.value) for member in JobState
        )
        self.assertEqual(observed, CANONICAL_STATES)

    def test_no_additional_member_and_no_alias(self):
        self.assertEqual(len(JobState), 9)
        self.assertEqual(len(JobState.__members__), 9)

    def test_module_exports_only_the_vocabulary(self):
        import pixs.kernel.jobs as jobs_module

        self.assertEqual(jobs_module.__all__, ["JobState"])
        self.assertIs(jobs_module.JobState, JobState)


if __name__ == "__main__":
    unittest.main()
