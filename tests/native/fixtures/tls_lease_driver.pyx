# cython: language_level=3
"""Conducteur de TEST du port privé ; aucun client Z12 ou matériel réel.

Inclure le vrai module, compiler seulement cet artefact sous le nom
tls_lease_driver avec --wrap=clock_gettime et les bibliothèques OpenSSL
explicitement sélectionnées. Ne jamais livrer ce conducteur dans PA.
"""
include "../../../src/pixs/pa_native/tls_context.pyx"

cdef extern from *:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <time.h>
    static uint64_t pa01_test_now = UINT64_C(1000000000);
    static int pa01_test_clock_error = 0;
    void pa01_tls_test_clock(uint64_t now, int fail) {
        pa01_test_now = now;
        pa01_test_clock_error = fail;
    }
    int __wrap_clock_gettime(clockid_t which, struct timespec *out) {
        if (which != CLOCK_MONOTONIC || out == NULL || pa01_test_clock_error) {
            errno = EIO;
            return -1;
        }
        out->tv_sec = (time_t)(pa01_test_now / UINT64_C(1000000000));
        out->tv_nsec = (long)(pa01_test_now % UINT64_C(1000000000));
        return 0;
    }
    """
    void pa01_tls_test_clock(uint64_t, int) noexcept

cdef public uint32_t pa01_tls_test_new(void **out, PyObject *subject,
        void *owner, int side, uint32_t usage, const uint8_t *operation,
        size_t size, uint64_t deadline) noexcept with gil:
    return _tls_lease_new(out, subject, owner, side, usage, operation, size, deadline)

cdef public uint32_t pa01_tls_test_get(void *state, void *owner, int side,
        uint32_t usage, const uint8_t *operation, size_t size,
        int *consistent) noexcept with gil:
    cdef OSSL_LIB_CTX *library = <OSSL_LIB_CTX *>1
    cdef SSL_CTX *ssl = <SSL_CTX *>1
    cdef uint32_t status
    cdef TLS13Context context
    if consistent == NULL:
        return 1
    consistent[0] = 0
    status = _tls_lease_context(state, owner, side, usage, operation,
                               size, &library, &ssl)
    if status != 0:
        consistent[0] = library == NULL and ssl == NULL
        return status
    context = <TLS13Context><object>(<_TLSLease *>state).subject
    consistent[0] = library == context._library and ssl == context._ctx
    return status

cdef public uint32_t pa01_tls_test_withdraw(void *state, void *owner) noexcept with gil:
    return _tls_lease_withdraw(state, owner)

cdef public uint32_t pa01_tls_test_close(void **state, void *owner) noexcept with gil:
    return _tls_lease_close(state, owner)
