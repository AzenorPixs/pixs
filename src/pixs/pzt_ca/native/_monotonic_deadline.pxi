# Privé Z12 : échéance monotone unique, sans source UTC ni autorisation implicite.
# Le budget positif provient de la politique courante vérifiée par le propriétaire.
from libc.stdint cimport uint64_t, int32_t

cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <limits.h>
    #include <errno.h>
    #include <time.h>

    typedef struct {
        uint64_t end_ns;
        uint64_t last_seen_ns;
        int started;
    } Z12MonotonicDeadline;

    static int z12_monotonic_now(uint64_t *result) {
        struct timespec value;
        uint64_t seconds;
        if (result == NULL) return -2;
        *result = 0;
        if (clock_gettime(CLOCK_MONOTONIC, &value) != 0) return -1;
        if (value.tv_sec < 0 || value.tv_nsec < 0 || value.tv_nsec >= 1000000000L) {
            errno = EIO; return -1;
        }
        seconds = (uint64_t)value.tv_sec;
        if (seconds > (UINT64_MAX - (uint64_t)value.tv_nsec) / UINT64_C(1000000000)) {
            errno = EOVERFLOW; return -1;
        }
        *result = seconds * UINT64_C(1000000000) + (uint64_t)value.tv_nsec;
        return 1;
    }
    static int z12_deadline_start(Z12MonotonicDeadline *deadline, uint64_t budget_ns) {
        uint64_t now = 0;
        int result;
        if (deadline == NULL) return -2;
        deadline->end_ns = 0;
        deadline->last_seen_ns = 0;
        deadline->started = 0;
        if (budget_ns == 0) return -2;
        result = z12_monotonic_now(&now);
        if (result != 1) return result;
        if (budget_ns > UINT64_MAX - now) { errno = EOVERFLOW; return -1; }
        deadline->end_ns = now + budget_ns;
        deadline->last_seen_ns = now;
        deadline->started = 1;
        return 1;
    }
    /* 1 : vivante ; 0 : expirée ; -1 : horloge ; -2 : contrat invalide.
       L'arrondi inférieur évite d'ajouter une milliseconde au budget restant.
       Un timeout nul impose un Finish non bloquant ; l'appelant relit ensuite
       l'échéance même après un succès et ne la recommence jamais par étape. */
    static int z12_deadline_remaining(Z12MonotonicDeadline *deadline, int32_t *timeout_ms) {
        uint64_t now = 0;
        uint64_t milliseconds;
        int result;
        if (timeout_ms == NULL) return -2;
        *timeout_ms = 0;
        if (deadline == NULL || deadline->started != 1 || deadline->end_ns == 0) return -2;
        result = z12_monotonic_now(&now);
        if (result != 1) return result;
        if (now < deadline->last_seen_ns) { errno = EIO; return -1; }
        deadline->last_seen_ns = now;
        if (now >= deadline->end_ns) return 0;
        milliseconds = (deadline->end_ns - now) / UINT64_C(1000000);
        *timeout_ms = milliseconds > (uint64_t)INT32_MAX ? INT32_MAX : (int32_t)milliseconds;
        return 1;
    }
    """
    ctypedef struct Z12MonotonicDeadline:
        uint64_t end_ns
        uint64_t last_seen_ns
        int started

    int z12_deadline_start(Z12MonotonicDeadline *deadline, uint64_t budget_ns)
    int z12_deadline_remaining(Z12MonotonicDeadline *deadline, int32_t *timeout_ms)
