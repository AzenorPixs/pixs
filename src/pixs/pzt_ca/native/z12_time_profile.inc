#ifndef Z12_TIME_PROFILE_INC
#define Z12_TIME_PROFILE_INC

/* Helpers arithmetiques purs du temps Z12 (T1-B1).
 * Calcul entier verifie seulement : aucune observation, aucune
 * admission, aucune entree-sortie, aucune horloge, aucun appel
 * systeme. C11 portable, stdint.h seul, sans __int128.
 * Entrees UTC par valeur : aucun pointeur entrant a deréférencer
 * ni a aliaser. Codes : 1 calcule, 0 refuse, -2 invalide.
 * Toute sortie non nulle est remise a zero avant les controles ;
 * en echec elle reste a zero et inutilisable. Le zero numerique
 * n'est jamais positif sans code 1. Aucune constante
 * d'incertitude ideale, aucun defaut, aucun protocole partage. */

#include <stdint.h>

#define Z12_TIME_MAX_U_NS (1000000000u)
#define Z12_TIME_MAX_NANOS (999999999u)
#define Z12_TIME_NS_PER_S (1000000000u)

typedef struct {
    int64_t seconds; /* pleine plage int64 */
    uint32_t nanos;  /* 0..999999999 */
} Z12TimeUtc;

typedef struct {
    Z12TimeUtc low;
    Z12TimeUtc high;
} Z12TimeWindow;

typedef struct {
    Z12TimeUtc est;
    Z12TimeWindow win;
    uint64_t u;
} Z12TimeResult;

static inline int z12_utc_valid(int64_t seconds, uint32_t nanos) {
    (void)seconds;
    return nanos <= (uint32_t)Z12_TIME_MAX_NANOS ? 1 : 0;
}

static inline int z12_utc_compare(Z12TimeUtc a, Z12TimeUtc b, int *out) {
    if (!out) return -2;
    *out = 0;
    if (a.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    if (b.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    if (a.seconds < b.seconds) { *out = -1; return 1; }
    if (a.seconds > b.seconds) { *out = 1; return 1; }
    if (a.nanos < b.nanos) { *out = -1; return 1; }
    if (a.nanos > b.nanos) { *out = 1; return 1; }
    return 1;
}

/* delta / 1e9 <= UINT64_MAX / 1e9 = 18446744073 < 2^63 : le quotient
 * tient dans int64 sans troncature, conversion toujours definie. */
static inline int z12_utc_add_delta(Z12TimeUtc base, uint64_t delta_ns, Z12TimeUtc *out) {
    uint64_t dsec, dnanos, nsum;
    int64_t step;
    unsigned carry;
    if (!out) return -2;
    out->seconds = 0; out->nanos = 0;
    if (base.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    dsec = delta_ns / (uint64_t)Z12_TIME_NS_PER_S;
    dnanos = delta_ns % (uint64_t)Z12_TIME_NS_PER_S;
    nsum = (uint64_t)base.nanos + dnanos; /* < 2e9 : aucun debordement */
    carry = nsum >= (uint64_t)Z12_TIME_NS_PER_S ? 1u : 0u;
    if (dsec > (uint64_t)INT64_MAX - (uint64_t)carry) return 0;
    step = (int64_t)(dsec + (uint64_t)carry); /* 0..INT64_MAX : defini */
    if (base.seconds >= 0) {
        /* int64 - int64 positif : soustraction definie. */
        if (base.seconds > INT64_MAX - step) return 0;
        out->seconds = base.seconds + step;
    } else {
        /* base < 0 et 0 <= step <= INT64_MAX : somme <= step <= MAX
         * et somme >= base >= MIN, aucun debordement possible. */
        out->seconds = base.seconds + step;
    }
    out->nanos = (uint32_t)(nsum % (uint64_t)Z12_TIME_NS_PER_S);
    return 1;
}

static inline int z12_utc_sub_delta(Z12TimeUtc base, uint64_t delta_ns, Z12TimeUtc *out) {
    uint64_t dsec, dnanos;
    int64_t step;
    uint32_t nn;
    unsigned borrow;
    if (!out) return -2;
    out->seconds = 0; out->nanos = 0;
    if (base.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    dsec = delta_ns / (uint64_t)Z12_TIME_NS_PER_S;
    dnanos = delta_ns % (uint64_t)Z12_TIME_NS_PER_S;
    if ((uint64_t)base.nanos >= dnanos) {
        nn = base.nanos - (uint32_t)dnanos; borrow = 0u;
    } else {
        nn = base.nanos + (uint32_t)Z12_TIME_NS_PER_S - (uint32_t)dnanos; borrow = 1u;
    }
    if (dsec > (uint64_t)INT64_MAX - (uint64_t)borrow) return 0;
    step = (int64_t)(dsec + (uint64_t)borrow);
    if (base.seconds <= 0) {
        /* int64 + int64 positif : addition definie. */
        if (base.seconds < INT64_MIN + step) return 0;
        out->seconds = base.seconds - step;
    } else {
        /* base > 0 et step >= 0 : somme >= -step > INT64_MIN. */
        out->seconds = base.seconds - step;
    }
    out->nanos = nn;
    return 1;
}

/* Chaque produit et intermediaire reste <= UINT64_MAX : le refus est
 * decide avant la division, meme si le quotient tiendrait. */
static inline int z12_ceil_mul_div(uint64_t num, uint64_t delta, uint64_t den, uint64_t *out) {
    uint64_t prod, q, r;
    if (!out) return -2;
    *out = 0;
    if (den == 0) return -2;
    if (num != 0 && delta > UINT64_MAX / num) return 0;
    prod = num * delta;
    q = prod / den;
    r = prod % den;
    if (r != 0) {
        if (q == UINT64_MAX) return 0;
        *out = q + 1u;
    } else {
        *out = q;
    }
    return 1;
}

static inline int z12_bound_u(uint64_t uref, uint64_t ecollect, uint64_t econv, uint64_t drift, uint64_t *out) {
    uint64_t sum;
    if (!out) return -2;
    *out = 0;
    if (uref > UINT64_MAX - ecollect) return 0;
    sum = uref + ecollect;
    if (sum > UINT64_MAX - econv) return 0;
    sum += econv;
    if (sum > UINT64_MAX - drift) return 0;
    sum += drift;
    if (sum > (uint64_t)Z12_TIME_MAX_U_NS) return 0;
    *out = sum;
    return 1;
}

static inline int z12_estimate(Z12TimeUtc ref, uint64_t delta_ns, uint64_t max_elapsed_ns, Z12TimeUtc *out) {
    if (!out) return -2;
    out->seconds = 0; out->nanos = 0;
    if (ref.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    if (max_elapsed_ns == 0) return -2;
    if (delta_ns > max_elapsed_ns) return 0;
    return z12_utc_add_delta(ref, delta_ns, out);
}

static inline int z12_window(Z12TimeUtc est, uint64_t u_ns, Z12TimeWindow *out) {
    Z12TimeUtc lo, hi;
    if (!out) return -2;
    out->low.seconds = 0; out->low.nanos = 0;
    out->high.seconds = 0; out->high.nanos = 0;
    if (est.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    if (u_ns > (uint64_t)Z12_TIME_MAX_U_NS) return 0;
    if (z12_utc_sub_delta(est, u_ns, &lo) != 1) return 0;
    if (z12_utc_add_delta(est, u_ns, &hi) != 1) return 0;
    out->low = lo; out->high = hi;
    return 1;
}

/* Pipeline unique : un seul resultat prive, aucun alias possible. */
static inline int z12_bound_estimate(Z12TimeUtc ref, uint64_t delta_ns, uint64_t max_elapsed_ns, uint64_t uref, uint64_t ecollect, uint64_t econv, uint64_t rho_num, uint64_t rho_den, Z12TimeResult *out) {
    uint64_t drift, u;
    Z12TimeUtc est;
    Z12TimeWindow win;
    if (!out) return -2;
    out->est.seconds = 0; out->est.nanos = 0;
    out->win.low.seconds = 0; out->win.low.nanos = 0;
    out->win.high.seconds = 0; out->win.high.nanos = 0;
    out->u = 0;
    if (ref.nanos > (uint32_t)Z12_TIME_MAX_NANOS) return -2;
    if (max_elapsed_ns == 0 || rho_den == 0) return -2;
    if (delta_ns > max_elapsed_ns) return 0;
    if (z12_ceil_mul_div(rho_num, delta_ns, rho_den, &drift) != 1) return 0;
    if (z12_bound_u(uref, ecollect, econv, drift, &u) != 1) return 0;
    if (z12_utc_add_delta(ref, delta_ns, &est) != 1) return 0;
    if (z12_window(est, u, &win) != 1) return 0;
    out->est = est; out->win = win; out->u = u;
    return 1;
}

#endif
