/* Harnais B1 : cas autonomes nommes, compteur d'erreurs, sans assert.
 * 1 = calcul technique reussi, jamais observation ni qualification.
 * Aucune fixture continuite, TCB, suspension ni provenance. */
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include "z12_time_profile.inc"

static int failures = 0;
static int total = 0;
#define CHECK(name, cond) do { ++total; if (!(cond)) { ++failures; printf("ECHEC %s ligne %d\n", name, __LINE__); } else { printf("ok %s\n", name); } } while (0)

static void t_valid(void) {
    CHECK("nanos-limite-ok", z12_utc_valid(0, 999999999u) == 1);
    CHECK("nanos-hors-limite", z12_utc_valid(0, 1000000000u) == 0);
    CHECK("nanos-uint32-max", z12_utc_valid(0, UINT32_MAX) == 0);
    CHECK("null-out-compare", z12_utc_compare((Z12TimeUtc){0, 0}, (Z12TimeUtc){0, 0}, 0) == -2);
}

static void t_compare(void) {
    int o = 0;
    CHECK("compare-moins", z12_utc_compare((Z12TimeUtc){5, 0}, (Z12TimeUtc){5, 1}, &o) == 1 && o == -1);
    CHECK("compare-plus", z12_utc_compare((Z12TimeUtc){5, 1}, (Z12TimeUtc){5, 0}, &o) == 1 && o == 1);
    CHECK("compare-egal", z12_utc_compare((Z12TimeUtc){5, 0}, (Z12TimeUtc){5, 0}, &o) == 1 && o == 0);
    CHECK("compare-nanos-invalides", z12_utc_compare((Z12TimeUtc){0, 1000000000u}, (Z12TimeUtc){0, 0}, &o) == -2 && o == 0);
}

static void t_add_sub(void) {
    Z12TimeUtc out = {0, 0};
    CHECK("add-1s-exact", z12_utc_add_delta((Z12TimeUtc){10, 0}, 1000000000ull, &out) == 1 && out.seconds == 11 && out.nanos == 0);
    CHECK("add-1ns-retenue", z12_utc_add_delta((Z12TimeUtc){10, 999999999u}, 1ull, &out) == 1 && out.seconds == 11 && out.nanos == 0);
    CHECK("sub-1ns-emprunt", z12_utc_sub_delta((Z12TimeUtc){10, 0}, 1ull, &out) == 1 && out.seconds == 9 && out.nanos == 999999999u);
    CHECK("epoque-negative", z12_utc_add_delta((Z12TimeUtc){-3, 500000000u}, 2000000000ull, &out) == 1 && out.seconds == -1 && out.nanos == 500000000u);
    CHECK("epoque-negative-emprunt", z12_utc_sub_delta((Z12TimeUtc){-3, 100u}, 200ull, &out) == 1 && out.seconds == -4 && out.nanos == 999999900u);
    CHECK("null-out-add", z12_utc_add_delta((Z12TimeUtc){0, 0}, 1ull, 0) == -2);
    CHECK("null-out-sub", z12_utc_sub_delta((Z12TimeUtc){0, 0}, 1ull, 0) == -2);
}

static void t_bornes(void) {
    Z12TimeUtc m1 = {0, 0}, m2 = {0, 0};
    CHECK("max-5-plus-5s", z12_utc_add_delta((Z12TimeUtc){INT64_MAX - 5, 999999999u}, 5000000000ull, &m1) == 1 && m1.seconds == INT64_MAX && m1.nanos == 999999999u);
    CHECK("max-plus-1ns-refus", z12_utc_add_delta((Z12TimeUtc){INT64_MAX, 999999999u}, 1ull, &m2) == 0 && m2.seconds == 0 && m2.nanos == 0);
    CHECK("int64min-sub-refus", z12_utc_sub_delta((Z12TimeUtc){INT64_MIN, 0}, 1ull, &m2) == 0 && m2.seconds == 0 && m2.nanos == 0);
    CHECK("int64min-add-nul", z12_utc_add_delta((Z12TimeUtc){INT64_MIN, 0}, 0ull, &m2) == 1 && m2.seconds == INT64_MIN);
    CHECK("int64max-retenue-refus", z12_utc_add_delta((Z12TimeUtc){INT64_MAX, 999999998u}, 2ull, &m2) == 0);
    CHECK("duree-600s-arithmetique", z12_estimate((Z12TimeUtc){0, 0}, 600000000000ull, 600000000000ull, &m2) == 1 && m2.seconds == 600 && m2.nanos == 0);
    CHECK("depassement-duree", z12_estimate((Z12TimeUtc){0, 0}, 600000000001ull, 600000000000ull, &m2) == 0 && m2.seconds == 0);
    CHECK("duree-max-nulle", z12_estimate((Z12TimeUtc){0, 0}, 0ull, 0ull, &m2) == -2);
    CHECK("duree-exacte", z12_estimate((Z12TimeUtc){7, 0}, 5ull, 5ull, &m2) == 1 && m2.seconds == 7 && m2.nanos == 5);
    CHECK("duree-plus-un", z12_estimate((Z12TimeUtc){7, 0}, 6ull, 5ull, &m2) == 0);
    CHECK("delta-max", z12_estimate((Z12TimeUtc){0, 0}, UINT64_MAX, UINT64_MAX, &m2) == 1 && m2.seconds == 18446744073ll && m2.nanos == 709551615u);
    CHECK("null-out-estimate", z12_estimate((Z12TimeUtc){0, 0}, 1ull, 9ull, 0) == -2);
}

static void t_ceil(void) {
    uint64_t o = 0;
    CHECK("rho-zero", z12_ceil_mul_div(0ull, 999ull, 7ull, &o) == 1 && o == 0);
    CHECK("rho-un", z12_ceil_mul_div(1ull, 9ull, 1ull, &o) == 1 && o == 9);
    CHECK("arrondi-vers-large", z12_ceil_mul_div(1ull, 1ull, 3ull, &o) == 1 && o == 1);
    CHECK("division-exacte", z12_ceil_mul_div(2ull, 3ull, 3ull, &o) == 1 && o == 2);
    CHECK("ratio-max", z12_ceil_mul_div(UINT64_MAX, 1ull, 1ull, &o) == 1 && o == UINT64_MAX);
    CHECK("produit-max-valide", z12_ceil_mul_div(UINT64_MAX, 1ull, UINT64_MAX, &o) == 1 && o == 1);
    CHECK("produit-overflow-den-max", z12_ceil_mul_div(UINT64_MAX, UINT64_MAX, UINT64_MAX, &o) == 0 && o == 0);
    CHECK("den-zero", z12_ceil_mul_div(1ull, 1ull, 0ull, &o) == -2);
    CHECK("null-out-ceil", z12_ceil_mul_div(1ull, 1ull, 1ull, 0) == -2);
}

static void t_borne_u(void) {
    uint64_t o = 0;
    CHECK("borne-exacte-1s", z12_bound_u(1000000000ull, 0ull, 0ull, 0ull, &o) == 1 && o == 1000000000ull);
    CHECK("borne-depassee", z12_bound_u(1000000000ull, 1ull, 0ull, 0ull, &o) == 0 && o == 0);
    CHECK("somme-etape1-overflow", z12_bound_u(UINT64_MAX, 1ull, 0ull, 0ull, &o) == 0);
    CHECK("somme-etape2-overflow", z12_bound_u(UINT64_MAX - 1ull, 1ull, 1ull, 0ull, &o) == 0);
    CHECK("somme-etape3-overflow", z12_bound_u(UINT64_MAX - 2ull, 1ull, 1ull, 1ull, &o) == 0);
    CHECK("null-out-bound", z12_bound_u(0ull, 0ull, 0ull, 0ull, 0) == -2);
}

static void t_fenetre_pipeline(void) {
    Z12TimeWindow w = {0};
    Z12TimeResult r = {0};
    CHECK("fenetre-plus-moins-1s", z12_window((Z12TimeUtc){100, 0}, 1000000000ull, &w) == 1 && w.low.seconds == 99 && w.low.nanos == 0 && w.high.seconds == 101 && w.high.nanos == 0);
    CHECK("fenetre-borne-depassee", z12_window((Z12TimeUtc){100, 0}, 1000000001ull, &w) == 0);
    CHECK("null-out-window", z12_window((Z12TimeUtc){0, 0}, 0ull, 0) == -2);
    CHECK("pipeline-calcule", z12_bound_estimate((Z12TimeUtc){1000, 0}, 1000ull, 600000000000ull, 100ull, 50ull, 25ull, 1ull, 3ull, &r) == 1 && r.u == 509ull && r.est.seconds == 1000 && r.est.nanos == 1000);
    CHECK("fenetre-basse", r.win.low.seconds == 1000 && r.win.low.nanos == 491);
    CHECK("fenetre-haute", r.win.high.seconds == 1000 && r.win.high.nanos == 1509);
    CHECK("null-out-pipeline", z12_bound_estimate((Z12TimeUtc){0, 0}, 0ull, 1ull, 0ull, 0ull, 0ull, 0ull, 1ull, 0) == -2);
}

static void t_complements(void) {
    Z12TimeUtc m = {10, 500};
    Z12TimeUtc o = {0, 0};
    Z12TimeWindow w = {0};
    Z12TimeResult r = {0};
    int c = 0;
    CHECK("u-1s-moins-1ns", z12_window((Z12TimeUtc){100, 0}, 999999999ull, &w) == 1 && w.low.seconds == 99 && w.low.nanos == 1 && w.high.seconds == 100 && w.high.nanos == 999999999u);
    CHECK("compare-min-max", z12_utc_compare((Z12TimeUtc){INT64_MIN, 999999999u}, (Z12TimeUtc){INT64_MAX, 0}, &c) == 1 && c == -1);
    CHECK("compare-max-min", z12_utc_compare((Z12TimeUtc){INT64_MAX, 0}, (Z12TimeUtc){INT64_MIN, 999999999u}, &c) == 1 && c == 1);
    CHECK("add-en-place", z12_utc_add_delta(m, 600ull, &m) == 1 && m.seconds == 10 && m.nanos == 1100);
    CHECK("sub-en-place", z12_utc_sub_delta(m, 700ull, &m) == 1 && m.seconds == 10 && m.nanos == 400);
    CHECK("pipeline-calcule", z12_bound_estimate((Z12TimeUtc){1000, 0}, 1000ull, 600000000000ull, 100ull, 50ull, 25ull, 1ull, 3ull, &r) == 1 && r.u == 509ull && r.est.seconds == 1000 && r.est.nanos == 1000);
    CHECK("pipeline-reutilise-record", z12_bound_estimate(r.est, 1000ull, 600000000000ull, 100ull, 50ull, 25ull, 1ull, 3ull, &r) == 1 && r.est.seconds == 1000 && r.est.nanos == 2000 && r.u == 509ull && r.win.low.seconds == 1000 && r.win.low.nanos == 1491 && r.win.high.seconds == 1000 && r.win.high.nanos == 2509);
    o.seconds = 9; o.nanos = 9;
    CHECK("add-nanos-invalide-efface", z12_utc_add_delta((Z12TimeUtc){1, 1000000000u}, 5ull, &o) == -2 && o.seconds == 0 && o.nanos == 0);
    o.seconds = 9; o.nanos = 9;
    CHECK("sub-nanos-invalide-efface", z12_utc_sub_delta((Z12TimeUtc){1, 1000000000u}, 5ull, &o) == -2 && o.seconds == 0 && o.nanos == 0);
    w.low.seconds = 9; w.low.nanos = 9; w.high.seconds = 9; w.high.nanos = 9;
    CHECK("window-nanos-invalide-efface", z12_window((Z12TimeUtc){1, 1000000000u}, 5ull, &w) == -2 && w.low.seconds == 0 && w.low.nanos == 0 && w.high.seconds == 0 && w.high.nanos == 0);
    r.est.seconds = 5; r.est.nanos = 5; r.win.low.seconds = 6; r.win.low.nanos = 6; r.win.high.seconds = 7; r.win.high.nanos = 7; r.u = 42;
    CHECK("pipeline-denom-zero-efface", z12_bound_estimate((Z12TimeUtc){1, 0}, 5ull, 9ull, 0ull, 0ull, 0ull, 1ull, 0ull, &r) == -2 && r.est.seconds == 0 && r.est.nanos == 0 && r.win.low.seconds == 0 && r.win.low.nanos == 0 && r.win.high.seconds == 0 && r.win.high.nanos == 0 && r.u == 0);
    CHECK("window-max-deborde-refus", z12_window((Z12TimeUtc){INT64_MAX, 999999998u}, 2ull, &w) == 0 && w.low.seconds == 0 && w.low.nanos == 0 && w.high.seconds == 0 && w.high.nanos == 0);
}

int main(void) {
    t_valid();
    t_compare();
    t_add_sub();
    t_bornes();
    t_ceil();
    t_borne_u();
    t_fenetre_pipeline();
    t_complements();
    printf("total=%d echecs=%d\n", total, failures);
    return failures != 0 ? 1 : 0;
}
