"""Unités pures des bornes temporelles CA, dates synthétiques opaques."""

from __future__ import annotations

import datetime
import unittest

from pixs.pzt_ca.durations import (
    DurationsError,
    bound_descendant_not_after,
    coexistence_upper_bound,
    key_age_us,
    preparation_due,
    remaining_to_boundary_us,
    terminal_overlap_upper_bound,
    terminal_renewal_due,
)

UTC = datetime.timezone.utc
DAY = datetime.timedelta(days=1)
MICROSECOND = datetime.timedelta(microseconds=1)
MAX_UTC = datetime.datetime.max.replace(tzinfo=UTC)


class NominalThresholdTests(unittest.TestCase):
    def test_intermediate_365_days(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + 365 * DAY
        threshold = start + 240 * DAY
        self.assertFalse(preparation_due("intermediate", start, end, threshold - MICROSECOND))
        self.assertTrue(preparation_due("intermediate", start, end, threshold))
        self.assertTrue(preparation_due("intermediate", start, end, threshold + MICROSECOND))

    def test_root_7300_days(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + 7300 * DAY
        threshold = start + 5840 * DAY
        self.assertFalse(preparation_due("root", start, end, threshold - MICROSECOND))
        self.assertTrue(preparation_due("root", start, end, threshold))
        self.assertTrue(preparation_due("root", start, end, threshold + MICROSECOND))


class NonRepresentableFractionTests(unittest.TestCase):
    def test_one_second_657534_false_657535_true(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + datetime.timedelta(seconds=1)
        self.assertFalse(
            preparation_due(
                "intermediate", start, end,
                start + datetime.timedelta(microseconds=657534),
            )
        )
        self.assertTrue(
            preparation_due(
                "intermediate", start, end,
                start + datetime.timedelta(microseconds=657535),
            )
        )


class ShortenedValidityTests(unittest.TestCase):
    def test_100_days_between_65_and_66_days(self) -> None:
        # Fraction exacte 4800/73 jours, strictement entre 65 et 66 jours.
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + 100 * DAY
        self.assertFalse(preparation_due("intermediate", start, end, start + 65 * DAY))
        self.assertTrue(preparation_due("intermediate", start, end, start + 66 * DAY))
        self.assertTrue(preparation_due("intermediate", start, end, end - DAY))
        self.assertTrue(preparation_due("intermediate", start, end, end))


class PreparationBeforeAndAfterTests(unittest.TestCase):
    def test_before_not_before_false_after_expiry_true_without_right(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + 365 * DAY
        self.assertFalse(preparation_due("intermediate", start, end, start - DAY))
        self.assertTrue(preparation_due("intermediate", start, end, end + DAY))
        # Le résultat après expiration ne porte aucune admission.
        self.assertIsInstance(preparation_due("intermediate", start, end, end + DAY), bool)


class KeyAgeTests(unittest.TestCase):
    def test_zero_age_and_future_refused(self) -> None:
        created = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        self.assertEqual(key_age_us(created, created), 0)
        self.assertEqual(key_age_us(created, created + 10 * DAY), 10 * 86_400_000_000)
        with self.assertRaises(DurationsError):
            key_age_us(created + DAY, created)


class CoexistenceCapTests(unittest.TestCase):
    def test_30_days_and_shorter_bounds(self) -> None:
        engaged = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        far = engaged + 90 * DAY
        self.assertEqual(
            coexistence_upper_bound(engaged, engaged + 60 * DAY, far),
            engaged + 30 * DAY,
        )
        short_deadline = engaged + 10 * DAY
        self.assertEqual(
            coexistence_upper_bound(engaged, short_deadline, far), short_deadline
        )
        short_anchor = engaged + 5 * DAY
        self.assertEqual(
            coexistence_upper_bound(engaged, engaged + 60 * DAY, short_anchor),
            short_anchor,
        )

    def test_impossible_normal_windows_refused(self) -> None:
        engaged = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        with self.assertRaises(DurationsError):
            coexistence_upper_bound(engaged, engaged, engaged + 10 * DAY)
        with self.assertRaises(DurationsError):
            coexistence_upper_bound(engaged, engaged + 10 * DAY, engaged)

    def test_remaining_before_exact_after_one_microsecond(self) -> None:
        engaged = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        bound = engaged + 30 * DAY
        before = bound - MICROSECOND
        self.assertEqual(remaining_to_boundary_us(bound, before), 1)
        self.assertEqual(remaining_to_boundary_us(bound, bound), 0)
        self.assertEqual(remaining_to_boundary_us(bound, bound + MICROSECOND), 0)


    def test_application_tardive_conserve_le_reliquat_commun(self) -> None:
        engaged = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        bound = coexistence_upper_bound(engaged, engaged + 60 * DAY, engaged + 90 * DAY)
        received_late = engaged + 29 * DAY
        self.assertEqual(bound, engaged + 30 * DAY)
        self.assertEqual(remaining_to_boundary_us(bound, received_late), 86_400_000_000)


class MaxDatetimeTests(unittest.TestCase):
    def test_coexistence_near_max_without_overflow(self) -> None:
        engaged = MAX_UTC - datetime.timedelta(days=60)
        self.assertEqual(
            coexistence_upper_bound(MAX_UTC - datetime.timedelta(days=60), MAX_UTC, MAX_UTC),
            engaged + 30 * DAY,
        )
        late = MAX_UTC - datetime.timedelta(days=10)
        self.assertEqual(coexistence_upper_bound(late, MAX_UTC, MAX_UTC), MAX_UTC)

    def test_terminal_overlap_near_max_without_overflow(self) -> None:
        start = MAX_UTC - datetime.timedelta(minutes=10)
        self.assertEqual(
            terminal_overlap_upper_bound(start, MAX_UTC, MAX_UTC, MAX_UTC),
            start + datetime.timedelta(minutes=5),
        )
        short_start = MAX_UTC - datetime.timedelta(minutes=2)
        self.assertEqual(
            terminal_overlap_upper_bound(short_start, MAX_UTC, MAX_UTC, MAX_UTC),
            MAX_UTC,
        )


class TerminalOverlapTests(unittest.TestCase):
    def test_five_minutes_and_each_shorter_bound(self) -> None:
        start = datetime.datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
        far = start + datetime.timedelta(minutes=10)
        self.assertEqual(
            terminal_overlap_upper_bound(start, far, far, far),
            start + datetime.timedelta(minutes=5),
        )
        short_old = start + datetime.timedelta(minutes=2)
        self.assertEqual(
            terminal_overlap_upper_bound(start, short_old, far, far), short_old
        )
        short_new = start + datetime.timedelta(minutes=3)
        self.assertEqual(
            terminal_overlap_upper_bound(start, far, short_new, far), short_new
        )
        short_auth = start + datetime.timedelta(minutes=4)
        self.assertEqual(
            terminal_overlap_upper_bound(start, far, far, short_auth), short_auth
        )

    def test_ended_or_passed_bound_zero_remaining(self) -> None:
        start = datetime.datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
        far = start + datetime.timedelta(minutes=10)
        self.assertEqual(
            terminal_overlap_upper_bound(start, start, far, far), start
        )
        past = start - datetime.timedelta(minutes=1)
        self.assertEqual(
            terminal_overlap_upper_bound(start, past, far, far), past
        )
        self.assertEqual(remaining_to_boundary_us(start, start), 0)
        self.assertEqual(remaining_to_boundary_us(past, start), 0)


class DescendantBoundTests(unittest.TestCase):
    def test_each_limiting_bound(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        request = start + 365 * DAY
        issuer = start + 100 * DAY
        anchor = start + 200 * DAY
        auth = start + 300 * DAY
        self.assertEqual(
            bound_descendant_not_after(start, request, issuer, anchor, auth), issuer
        )
        self.assertEqual(
            bound_descendant_not_after(start, request, request + DAY, anchor, auth),
            anchor,
        )
        self.assertEqual(
            bound_descendant_not_after(start, request, request + DAY, request + 2 * DAY, auth),
            auth,
        )
        self.assertEqual(
            bound_descendant_not_after(start, request, request + DAY, request + 2 * DAY, request + 3 * DAY),
            request,
        )

    def test_terminal_24h_but_ca_1h_only(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        request = start + datetime.timedelta(hours=24)
        issuer = start + datetime.timedelta(hours=1)
        self.assertEqual(
            bound_descendant_not_after(start, request, issuer, request, request),
            issuer,
        )

    def test_bound_equal_to_not_before_insufficient(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        request = start + 10 * DAY
        with self.assertRaises(DurationsError):
            bound_descendant_not_after(start, request, start, request, request)


class BadTypesTests(unittest.TestCase):
    def test_unknown_role_and_bad_intervals(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + DAY
        with self.assertRaises(DurationsError):
            preparation_due("unknown", start, end, start)
        with self.assertRaises(DurationsError):
            preparation_due("intermediate", end, end, end)
        with self.assertRaises(DurationsError):
            preparation_due("intermediate", end, start, end)

    def test_foreign_naive_non_utc_in_every_position(self) -> None:
        class Foreign(datetime.datetime):
            pass

        valid = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        foreign = Foreign(2026, 1, 1, tzinfo=UTC)
        naive = datetime.datetime(2026, 1, 1)
        offset = datetime.datetime(
            2026, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=1))
        )
        for bad in (foreign, naive, offset, "2026-01-01T00:00:00Z", None, 0):
            with self.assertRaises(DurationsError, msg=str(bad)):
                preparation_due("intermediate", bad, valid + DAY, valid + DAY)
            with self.assertRaises(DurationsError, msg=str(bad)):
                preparation_due("intermediate", valid, bad, valid + DAY)
            with self.assertRaises(DurationsError, msg=str(bad)):
                preparation_due("intermediate", valid, valid + DAY, bad)
            with self.assertRaises(DurationsError, msg=str(bad)):
                key_age_us(bad, valid)
            with self.assertRaises(DurationsError, msg=str(bad)):
                key_age_us(valid, bad)
            with self.assertRaises(DurationsError, msg=str(bad)):
                coexistence_upper_bound(bad, valid + DAY, valid + 2 * DAY)
            with self.assertRaises(DurationsError, msg=str(bad)):
                coexistence_upper_bound(valid, bad, valid + 2 * DAY)
            with self.assertRaises(DurationsError, msg=str(bad)):
                coexistence_upper_bound(valid, valid + DAY, bad)
            with self.assertRaises(DurationsError, msg=str(bad)):
                remaining_to_boundary_us(bad, valid)
            with self.assertRaises(DurationsError, msg=str(bad)):
                remaining_to_boundary_us(valid, bad)
            with self.assertRaises(DurationsError, msg=str(bad)):
                bound_descendant_not_after(
                    bad, valid + DAY, valid + 2 * DAY, valid + 3 * DAY, valid + 4 * DAY
                )
            with self.assertRaises(DurationsError, msg=str(bad)):
                terminal_overlap_upper_bound(
                    bad, valid + DAY, valid + 2 * DAY, valid + 3 * DAY
                )
            with self.assertRaises(DurationsError, msg=str(bad)):
                terminal_overlap_upper_bound(
                    valid, bad, valid + 2 * DAY, valid + 3 * DAY
                )
            descendant_args = (valid, valid + DAY, valid + 2 * DAY, valid + 3 * DAY, valid + 4 * DAY)
            for position in range(len(descendant_args)):
                arguments = list(descendant_args)
                arguments[position] = bad
                with self.subTest(function="descendant", position=position, bad_type=type(bad).__name__):
                    with self.assertRaises(DurationsError):
                        bound_descendant_not_after(*arguments)
            overlap_args = (valid, valid + DAY, valid + 2 * DAY, valid + 3 * DAY)
            for position in range(len(overlap_args)):
                arguments = list(overlap_args)
                arguments[position] = bad
                with self.subTest(function="overlap", position=position, bad_type=type(bad).__name__):
                    with self.assertRaises(DurationsError):
                        terminal_overlap_upper_bound(*arguments)


class TerminalRenewalTests(unittest.TestCase):
    def test_24_heures_seuil_16_heures(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + DAY
        threshold = start + datetime.timedelta(hours=16)
        self.assertFalse(terminal_renewal_due(start, end, threshold - MICROSECOND))
        self.assertTrue(terminal_renewal_due(start, end, threshold))
        self.assertTrue(terminal_renewal_due(start, end, threshold + MICROSECOND))

    def test_validite_raccourcie_6_heures_seuil_4_heures(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + datetime.timedelta(hours=6)
        threshold = start + datetime.timedelta(hours=4)
        self.assertFalse(terminal_renewal_due(start, end, threshold - MICROSECOND))
        self.assertTrue(terminal_renewal_due(start, end, threshold))

    def test_fraction_non_representable_sans_troncature(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + datetime.timedelta(seconds=1)
        self.assertFalse(terminal_renewal_due(
            start, end, start + datetime.timedelta(microseconds=666666)
        ))
        self.assertTrue(terminal_renewal_due(
            start, end, start + datetime.timedelta(microseconds=666667)
        ))
        tiny_end = start + 2 * MICROSECOND
        self.assertFalse(terminal_renewal_due(start, tiny_end, start + MICROSECOND))
        self.assertTrue(terminal_renewal_due(start, tiny_end, tiny_end))

    def test_avant_debut_expiration_et_apres_sans_droit(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        end = start + DAY
        self.assertFalse(terminal_renewal_due(start, end, start - MICROSECOND))
        self.assertFalse(terminal_renewal_due(start, end, start))
        self.assertTrue(terminal_renewal_due(start, end, end))
        self.assertTrue(terminal_renewal_due(start, end, end + MICROSECOND))

    def test_dates_max_sans_debordement(self) -> None:
        start = MAX_UTC - 6 * MICROSECOND
        self.assertFalse(terminal_renewal_due(start, MAX_UTC, start + 3 * MICROSECOND))
        self.assertTrue(terminal_renewal_due(start, MAX_UTC, start + 4 * MICROSECOND))
        self.assertTrue(terminal_renewal_due(start, MAX_UTC, MAX_UTC))

    def test_intervalle_nul_ou_inverse(self) -> None:
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        for end in (start, start - MICROSECOND):
            with self.subTest(end=end):
                with self.assertRaises(DurationsError):
                    terminal_renewal_due(start, end, start)

    def test_types_refuses_dans_chaque_position(self) -> None:
        class Foreign(datetime.datetime):
            pass
        start = datetime.datetime(2026, 1, 1, tzinfo=UTC)
        bads = (
            Foreign(2026, 1, 1, tzinfo=UTC),
            datetime.datetime(2026, 1, 1),
            datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
            None, True, False, 0, 1.5, "2026-01-01T00:00:00Z",
        )
        for position in range(3):
            for bad in bads:
                arguments = [start, start + DAY, start]
                arguments[position] = bad
                with self.subTest(position=position, type=type(bad).__name__):
                    with self.assertRaises(DurationsError):
                        terminal_renewal_due(*arguments)


if __name__ == "__main__":
    unittest.main()
