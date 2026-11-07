/* Artefact de TEST seulement : IO réelles, ESAPI/TCTI/temps simulés.
 * Réutilise les deux conducteurs existants avec une seule horloge commune.
 * Aucun de ces remplacements ni inclusions .c n'entre dans un build produit.
 * Lier nv_secret/nv_anchor/nv_journal/postgresql_contracts/nv_intent, leurs
 * vrais headers générés, -lcrypto et les wrappers documentés dans la recette.
 */
#define _POSIX_C_SOURCE 200809L
#define __wrap_clock_gettime pa01_intent_fixture_nv_clock
#include "nv_public_driver.c"
#undef __wrap_clock_gettime
#define __wrap_clock_gettime pa01_intent_fixture_journal_clock
#include "nv_journal_driver.c"
#undef __wrap_clock_gettime

int __wrap_clock_gettime(clockid_t clock, struct timespec *value) {
    uint64_t now;
    if (clock != CLOCK_MONOTONIC)
        return __real_clock_gettime(clock, value);
    if (fixture_clock_error) return -1;
    /* Les pannes IO et ESAPI peuvent avancer la même échéance observée. */
    now = fixture_now > now_ns ? fixture_now : now_ns;
    value->tv_sec = (time_t)(now / UINT64_C(1000000000));
    value->tv_nsec = (long)(now % UINT64_C(1000000000));
    return 0;
}

void pa01_intent_test_clock(uint64_t now, int error) {
    pa01_test_clock(now, error);
    pa01_journal_test_clock(now);
}

void pa01_intent_test_reset(void) {
    pa01_journal_test_reset();
    pa01_test_clock(UINT64_C(1000000000), 0);
    pa01_test_auth_timing(0, 0);
}

uint32_t pa01_intent_test_nv(void *opaque, const uint8_t *value, size_t size) {
    Fixture *fixture = opaque;
    if (fixture == NULL || value == NULL || size != 32) return 1;
    memcpy(fixture->esys.nv_value, value, 32);
    return 0;
}
