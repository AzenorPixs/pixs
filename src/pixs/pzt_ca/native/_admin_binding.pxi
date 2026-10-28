# Prive Z12 : digest canonique binding, sans ancrage ni admission.
# A inclure UNE fois APRES _admin_values, _admin_codec, _admin_profile et _monotonic_deadline.
# LIBCTX emprunte non NULL du futur proprietaire, tampon natif immuable meme vie.
# Output[32] distinct sans recouvrement, duree explicite.
from libc.stddef cimport size_t
from libc.stdint cimport int32_t
from libc.string cimport memcpy, memset

cdef extern from * nogil:
    r"""
    #include <stddef.h>
    #include <stdint.h>
    #include <string.h>
    #include <openssl/evp.h>
    static int z12_admin_digest_binding(
        const unsigned char *payload, size_t payload_len,
        OSSL_LIB_CTX *libctx, unsigned char out32[32]) {
        EVP_MD *md = NULL;
        EVP_MD_CTX *ctx = NULL;
        unsigned int outlen = 0;
        if (payload == NULL || libctx == NULL || out32 == NULL) return -2;
        if (payload_len == 0) return -2;
        memset(out32, 0, 32);
        md = EVP_MD_fetch(libctx, "SHA256", "provider=default");
        if (md == NULL) return -1;
        ctx = EVP_MD_CTX_new();
        if (ctx == NULL) { EVP_MD_free(md); return -1; }
        if (EVP_DigestInit_ex2(ctx, md, NULL) != 1) {
            EVP_MD_CTX_free(ctx); EVP_MD_free(md); return -1;
        }
        if (EVP_DigestUpdate(ctx, payload, payload_len) != 1) {
            EVP_MD_CTX_free(ctx); EVP_MD_free(md); return -1;
        }
        if (EVP_DigestFinal_ex(ctx, out32, &outlen) != 1) {
            EVP_MD_CTX_free(ctx); EVP_MD_free(md); return -1;
        }
        EVP_MD_CTX_free(ctx);
        EVP_MD_free(md);
        if (outlen != 32) return -1;
        return 1;
    }
    """
    int z12_admin_digest_binding(
        const unsigned char *payload, size_t payload_len,
        OSSL_LIB_CTX *libctx, unsigned char out32[32])

cdef int _admin_binding_digest(
    const unsigned char *payload, size_t payload_len,
    OSSL_LIB_CTX *libctx,
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms,
    unsigned char *output32
) noexcept nogil:
    # 1=DIGEST_CANONIQUE_OBSERVE, 0=format public, -3=expire.
    # -1=horloge, -4=OpenSSL, -2=precondition native.
    cdef _AdminValues values
    cdef unsigned char candidate[32]
    cdef int live
    cdef int observed
    cdef int digested
    cdef int i
    if output32 == NULL:
        return -2
    for i in range(32):
        output32[i] = 0
    memset(&values, 0, sizeof(_AdminValues))
    for i in range(32):
        candidate[i] = 0
    if timeout_ms != NULL:
        timeout_ms[0] = 0
    if payload == NULL or libctx == NULL:
        return -2
    if deadline == NULL or timeout_ms == NULL:
        return -2
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    observed = _admin_values_observe(
        _ADMIN_KIND_BINDING, payload, payload_len,
        deadline, timeout_ms, &values
    )
    if observed != 1:
        return observed
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    digested = z12_admin_digest_binding(payload, payload_len, libctx, candidate)
    if digested == 1:
        pass
    elif digested == -1:
        return -4
    else:
        return -2
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    for i in range(32):
        output32[i] = candidate[i]
    return 1
