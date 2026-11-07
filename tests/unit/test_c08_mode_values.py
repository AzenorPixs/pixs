"""Matrice des règles pures C08 ; aucune qualification de runtime ou d'autorité."""
from enum import Enum
import unittest

from pixs.backend.installation.mode_values import (
    ConfigurationState as C, ModeOperationKind as K, ModeValuesError,
    transition_state, validate_state_pair)
from pixs.backend.startup_mode import StartupMode as M


class Foreign(Enum):
    PENDING = "PENDING"
    NORMAL = "NORMAL"
    FINALIZE_CONFIGURATION = "FINALIZE_CONFIGURATION"


MATRIX = (
    (C.PENDING, M.FIRST_CONFIGURATION, K.FINALIZE_CONFIGURATION, C.CONFIGURED, M.NORMAL),
    (C.PENDING, M.MAINTENANCE, K.FINALIZE_CONFIGURATION, C.CONFIGURED, M.MAINTENANCE),
    (C.CONFIGURED, M.NORMAL, K.FINALIZE_CONFIGURATION, C.CONFIGURED, M.NORMAL),
    (C.CONFIGURED, M.MAINTENANCE, K.FINALIZE_CONFIGURATION, C.CONFIGURED, M.MAINTENANCE),
    (C.PENDING, M.FIRST_CONFIGURATION, K.ENTER_MAINTENANCE, C.PENDING, M.MAINTENANCE),
    (C.PENDING, M.MAINTENANCE, K.ENTER_MAINTENANCE, C.PENDING, M.MAINTENANCE),
    (C.CONFIGURED, M.NORMAL, K.ENTER_MAINTENANCE, C.CONFIGURED, M.MAINTENANCE),
    (C.CONFIGURED, M.MAINTENANCE, K.ENTER_MAINTENANCE, C.CONFIGURED, M.MAINTENANCE),
    (C.PENDING, M.FIRST_CONFIGURATION, K.EXIT_MAINTENANCE, C.PENDING, M.FIRST_CONFIGURATION),
    (C.PENDING, M.MAINTENANCE, K.EXIT_MAINTENANCE, C.PENDING, M.FIRST_CONFIGURATION),
    (C.CONFIGURED, M.NORMAL, K.EXIT_MAINTENANCE, C.CONFIGURED, M.NORMAL),
    (C.CONFIGURED, M.MAINTENANCE, K.EXIT_MAINTENANCE, C.CONFIGURED, M.NORMAL),
)


class ModeValuesCases(unittest.TestCase):
    def test_canonical_transition_matrix(self):
        for state, mode, kind, expected_state, expected_mode in MATRIX:
            with self.subTest(state=state, mode=mode, kind=kind):
                self.assertEqual(validate_state_pair(state, mode), (state, mode))
                self.assertEqual(transition_state(state, mode, kind),
                                 (expected_state, expected_mode))

    def test_repeating_a_pure_operation_has_same_result(self):
        for state, mode, kind, *_ in MATRIX:
            with self.subTest(state=state, mode=mode, kind=kind):
                result = transition_state(state, mode, kind)
                self.assertEqual(transition_state(*result, kind), result)

    def test_configuration_and_mode_are_distinct_dimensions(self):
        self.assertEqual(
            transition_state(C.PENDING, M.FIRST_CONFIGURATION, K.ENTER_MAINTENANCE),
            (C.PENDING, M.MAINTENANCE))
        self.assertEqual(
            transition_state(C.PENDING, M.MAINTENANCE, K.FINALIZE_CONFIGURATION),
            (C.CONFIGURED, M.MAINTENANCE))
        self.assertEqual(
            transition_state(C.CONFIGURED, M.MAINTENANCE, K.EXIT_MAINTENANCE),
            (C.CONFIGURED, M.NORMAL))

    def test_incoherent_pairs_and_installer_are_refused(self):
        invalid = ((C.PENDING, M.NORMAL), (C.CONFIGURED, M.FIRST_CONFIGURATION),
                   (C.PENDING, M.INSTALLER), (C.CONFIGURED, M.INSTALLER))
        for state, mode in invalid:
            with self.subTest(state=state, mode=mode):
                with self.assertRaises(ModeValuesError):
                    validate_state_pair(state, mode)
                for kind in K:
                    with self.assertRaises(ModeValuesError):
                        transition_state(state, mode, kind)

    def test_types_and_foreign_enums_are_refused(self):
        values = ("PENDING", "NORMAL", "", True, False, None, 0, 1, [], {}, (),
                  Foreign.PENDING, Foreign.NORMAL, Foreign.FINALIZE_CONFIGURATION)
        for value in values:
            with self.subTest(value_type=type(value).__name__):
                with self.assertRaises(ModeValuesError):
                    validate_state_pair(value, M.FIRST_CONFIGURATION)
                with self.assertRaises(ModeValuesError):
                    validate_state_pair(C.PENDING, value)
                with self.assertRaises(ModeValuesError):
                    transition_state(C.PENDING, M.FIRST_CONFIGURATION, value)

    def test_diagnostic_does_not_format_the_rejected_value(self):
        class Opaque:
            def __str__(self):
                raise AssertionError("VALUE_MUST_NOT_BE_FORMATTED")
            def __repr__(self):
                raise AssertionError("VALUE_MUST_NOT_BE_FORMATTED")
        with self.assertRaises(ModeValuesError) as refused:
            transition_state(C.PENDING, M.FIRST_CONFIGURATION, Opaque())
        self.assertEqual(refused.exception.code, "C08_MODE_VALUES_REFUSED")


if __name__ == "__main__":
    unittest.main()
