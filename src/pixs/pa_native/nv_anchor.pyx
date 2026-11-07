# cython: language_level=3
"""Lecture publique ESAPI privée ; ne produit aucune preuve d'admission.

Le propriétaire natif prête des contextes ESYS/OSSL exclusifs et vivants.
Aucun contexte, index, secret, provider ou budget n'est découvert ici.
Une comparaison publique ne prouve ni TPM cible, maintenance, autorité ou UTC.
"""
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint16_t, uint32_t, uint64_t
from libc.stdlib cimport calloc, free
from libc.string cimport memcpy, memcmp, memset

# Initialiser le module Cython fermé avant tout appel de son ABI C privée.
import nv_secret as _nv_secret

cdef extern from "openssl/crypto.h":
    void OPENSSL_cleanse(void *, size_t) noexcept nogil

cdef extern from "nv_secret.h":
    uint32_t pa01_nv_secret_read32(int *, uint8_t *, size_t, int) noexcept nogil

cdef extern from "time.h":
    cdef struct timespec:
        long tv_sec
        long tv_nsec
    int CLOCK_MONOTONIC
    int clock_gettime(int, timespec *) noexcept nogil

cdef extern from "openssl/evp.h":
    ctypedef struct OSSL_LIB_CTX:
        pass
    int EVP_Q_digest(OSSL_LIB_CTX *, const char *, const char *,
                     const void *, size_t, unsigned char *, size_t *) noexcept nogil

cdef extern from "tss2/tss2_esys.h":
    ctypedef struct ESYS_CONTEXT:
        pass
    ctypedef uint32_t ESYS_TR
    ctypedef uint32_t TSS2_RC
    ctypedef struct TPM2B_DIGEST:
        uint16_t size
        uint8_t buffer[64]
    ctypedef struct TPMS_NV_PUBLIC:
        uint32_t nvIndex
        uint16_t nameAlg
        uint32_t attributes
        TPM2B_DIGEST authPolicy
        uint16_t dataSize
    ctypedef struct TPM2B_NV_PUBLIC:
        uint16_t size
        TPMS_NV_PUBLIC nvPublic
    ctypedef struct TPM2B_NAME:
        uint16_t size
        uint8_t name[68]
    enum:
        ESYS_TR_NONE
        TPM2_ALG_SHA256
        TPM2_NT_EXTEND
        TPMA_NV_PLATFORMCREATE
        TPMA_NV_POLICY_DELETE
        TPMA_NV_AUTHREAD
        TPMA_NV_AUTHWRITE
        TPMA_NV_WRITTEN
        TPMA_NV_CLEAR_STCLEAR
        TPMA_NV_ORDERLY
        TPMA_NV_READLOCKED
        TPMA_NV_WRITELOCKED
        TSS2_RC_LAYER_MASK
        TSS2_ESAPI_RC_LAYER
        TSS2_SYS_RC_LAYER
        TSS2_TCTI_RC_LAYER
        TSS2_FEATURE_RC_LAYER
        TSS2_RESMGR_RC_LAYER
        TSS2_BASE_RC_TRY_AGAIN
    TSS2_RC Esys_SetTimeout(ESYS_CONTEXT *, int) noexcept nogil
    TSS2_RC Esys_TR_FromTPMPublic_Async(
        ESYS_CONTEXT *, uint32_t, ESYS_TR, ESYS_TR, ESYS_TR) noexcept nogil
    TSS2_RC Esys_TR_FromTPMPublic_Finish(
        ESYS_CONTEXT *, ESYS_TR *) noexcept nogil
    TSS2_RC Esys_NV_ReadPublic_Async(
        ESYS_CONTEXT *, ESYS_TR, ESYS_TR, ESYS_TR, ESYS_TR) noexcept nogil
    TSS2_RC Esys_NV_ReadPublic_Finish(
        ESYS_CONTEXT *, TPM2B_NV_PUBLIC **, TPM2B_NAME **) noexcept nogil
    TSS2_RC Esys_TR_Close(ESYS_CONTEXT *, ESYS_TR *) noexcept nogil
    void Esys_Free(void *) noexcept nogil

cdef enum:
    OK = 0
    ARGUMENT = 1
    MEMORY = 2
    CLOCK = 3
    STATE = 4
    PENDING = 5
    EXPIRED = 6
    VERIFY = 7
    TSS_ERROR = 8
    IN_DOUBT = 9
    CLEANUP_ERROR = 10
    FD_ERROR = 11
    CRYPTO_ERROR = 12
    READY = 0
    IMPORT_PENDING = 1
    BETWEEN = 2
    READ_PENDING = 3
    COMPLETE = 4
    FAILED = 5
    QUARANTINED = 6
    AUTH_SESSION_PENDING = 7
    AUTH_READ_PENDING = 8
    AUTH_COMPLETE = 9
    CLEANUP_PENDING = 10
    EXTEND_SESSION_PENDING = 11
    EXTEND_READY = 12
    EXTEND_PENDING = 13

cdef struct _PublicRead:
    ESYS_CONTEXT *esys
    OSSL_LIB_CTX *crypto
    uint32_t index
    uint32_t attributes
    uint64_t deadline
    uint8_t policy[32]
    uint8_t name[34]
    ESYS_TR handle
    int has_handle
    int phase
    uint32_t failure
    uint32_t last_rc
    int expired
    ESYS_TR session
    int has_session
    int session_live
    int auth_set
    uint8_t nv_value[32]
    uint64_t read_serial
    int has_value
    uint64_t auth_deadline
    uint64_t cleanup_deadline
    int cleanup_expired
    uint32_t fd_status
    uint32_t cleanup_rc
    uint32_t cleanup_status
    void *guard
    void *intent_owner

cdef uint64_t _now() noexcept nogil:
    cdef timespec value
    cdef uint64_t limit = (~<uint64_t>0) // 1000000000
    if clock_gettime(CLOCK_MONOTONIC, &value) != 0:
        return 0
    if (value.tv_sec < 0 or <uint64_t>value.tv_sec >= limit
            or value.tv_nsec < 0 or value.tv_nsec >= 1000000000):
        return 0
    return <uint64_t>value.tv_sec * 1000000000 + <uint64_t>value.tv_nsec

cdef int _retry(TSS2_RC rc) noexcept nogil:
    cdef uint32_t layer = rc & TSS2_RC_LAYER_MASK
    return ((layer == TSS2_ESAPI_RC_LAYER or layer == TSS2_SYS_RC_LAYER
             or layer == TSS2_TCTI_RC_LAYER or layer == TSS2_FEATURE_RC_LAYER
             or layer == TSS2_RESMGR_RC_LAYER)
            and (rc & ~<uint32_t>TSS2_RC_LAYER_MASK) == TSS2_BASE_RC_TRY_AGAIN)

cdef int _profile(uint32_t attributes) noexcept nogil:
    cdef uint32_t required = (TPMA_NV_PLATFORMCREATE | TPMA_NV_POLICY_DELETE
        | TPMA_NV_AUTHREAD | TPMA_NV_AUTHWRITE | TPMA_NV_WRITTEN)
    cdef uint32_t forbidden = (TPMA_NV_CLEAR_STCLEAR | TPMA_NV_ORDERLY
        | TPMA_NV_READLOCKED | TPMA_NV_WRITELOCKED)
    return ((attributes & required) == required
            and (attributes & forbidden) == 0
            and (attributes & 0xF0) == (<uint32_t>TPM2_NT_EXTEND << 4))

cdef uint32_t _failure(_PublicRead *m, uint32_t status) noexcept nogil:
    m.phase = FAILED
    m.failure = status
    return status

cdef uint32_t _uncertain(_PublicRead *m, TSS2_RC rc) noexcept nogil:
    # Une erreur de transport ne prouve pas la fin de la commande.
    m.phase = QUARANTINED
    m.last_rc = rc
    return IN_DOUBT

cdef void _u16(uint8_t *p, uint16_t value) noexcept nogil:
    p[0] = <uint8_t>(value >> 8)
    p[1] = <uint8_t>value

cdef void _u32(uint8_t *p, uint32_t value) noexcept nogil:
    p[0] = <uint8_t>(value >> 24)
    p[1] = <uint8_t>(value >> 16)
    p[2] = <uint8_t>(value >> 8)
    p[3] = <uint8_t>value

cdef int _matches(_PublicRead *m, TPM2B_NV_PUBLIC *pub,
                  TPM2B_NAME *name) noexcept nogil:
    cdef uint8_t wire[46]
    cdef uint8_t digest[32]
    cdef size_t digest_size = 0
    if pub == NULL or name == NULL:
        return 0
    # TPMS_NV_PUBLIC : 4+2+4+2+32+2 octets, sans padding C.
    if (pub.size != 46 or pub.nvPublic.nvIndex != m.index
            or pub.nvPublic.nameAlg != TPM2_ALG_SHA256
            or pub.nvPublic.attributes != m.attributes
            or pub.nvPublic.dataSize != 32
            or pub.nvPublic.authPolicy.size != 32
            or name.size != 34):
        return 0
    if (memcmp(pub.nvPublic.authPolicy.buffer, m.policy, 32) != 0
            or memcmp(name.name, m.name, 34) != 0):
        return 0
    _u32(wire, pub.nvPublic.nvIndex)
    _u16(wire + 4, pub.nvPublic.nameAlg)
    _u32(wire + 6, pub.nvPublic.attributes)
    _u16(wire + 10, 32)
    memcpy(wire + 12, pub.nvPublic.authPolicy.buffer, 32)
    _u16(wire + 44, 32)
    if EVP_Q_digest(m.crypto, "SHA256", "provider=default",
                    wire, 46, digest, &digest_size) != 1:
        return 0
    return digest_size == 32 and memcmp(digest, name.name + 2, 32) == 0

cdef public uint32_t pa01_nv_public_new(
        void **state_out, void *esys_context, void *crypto_context,
        uint32_t index, uint32_t attributes,
        const uint8_t *policy, size_t policy_size,
        const uint8_t *name, size_t name_size,
        uint64_t deadline_ns) noexcept nogil:
    """Capacité C opaque ; tous les pointeurs appartiennent au natif de confiance."""
    cdef _PublicRead *m
    cdef uint64_t now
    if (state_out == NULL or state_out[0] != NULL or esys_context == NULL
            or crypto_context == NULL or policy == NULL or name == NULL):
        return ARGUMENT
    if (index < 0x01000000 or index > 0x01FFFFFF
            or policy_size != 32 or name_size != 34
            or name[0] != 0 or name[1] != TPM2_ALG_SHA256
            or not _profile(attributes)):
        return ARGUMENT
    now = _now()
    if now == 0 or deadline_ns <= now:
        return CLOCK
    m = <_PublicRead *>calloc(1, sizeof(_PublicRead))
    if m == NULL:
        return MEMORY
    m.esys = <ESYS_CONTEXT *>esys_context
    m.crypto = <OSSL_LIB_CTX *>crypto_context
    m.index = index
    m.attributes = attributes
    m.deadline = deadline_ns
    m.handle = ESYS_TR_NONE
    m.phase = READY
    memcpy(m.policy, policy, 32)
    memcpy(m.name, name, 34)
    state_out[0] = <void *>m
    return OK

cdef public uint32_t pa01_nv_public_start(void *state) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef TSS2_RC rc
    cdef uint64_t now
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if m.guard != NULL:
        if m.phase == QUARANTINED:
            return IN_DOUBT
        if m.phase == FAILED:
            return m.failure
    if m.phase != READY:
        return STATE
    now = _now()
    if now == 0:
        return _failure(m, CLOCK)
    if now >= m.deadline:
        return _failure(m, EXPIRED)
    rc = Esys_SetTimeout(m.esys, 0)
    if rc != 0:
        m.last_rc = rc
        return _failure(m, TSS_ERROR)
    rc = Esys_TR_FromTPMPublic_Async(
        m.esys, m.index, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE)
    if rc != 0:
        return _uncertain(m, rc)
    m.phase = IMPORT_PENDING
    _observe_guard(m)
    return IN_DOUBT if m.expired or m.phase == QUARANTINED else PENDING

cdef public uint32_t pa01_nv_public_step(void *state) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef TSS2_RC rc
    cdef uint64_t now
    cdef ESYS_TR handle = ESYS_TR_NONE
    cdef TPM2B_NV_PUBLIC *pub = NULL
    cdef TPM2B_NAME *name = NULL
    cdef int matched
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return IN_DOUBT
    if m.phase == COMPLETE:
        return OK
    if m.phase == FAILED:
        return m.failure
    if m.phase != IMPORT_PENDING and m.phase != BETWEEN and m.phase != READ_PENDING:
        return STATE
    now = _now()
    if now == 0:
        m.expired = 1
        m.failure = CLOCK
    elif now >= m.deadline:
        m.expired = 1
        if m.failure == OK:
            m.failure = EXPIRED
    if m.phase == BETWEEN:
        if m.expired:
            return _failure(m, m.failure)
        rc = Esys_NV_ReadPublic_Async(
            m.esys, m.handle, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE)
        if rc != 0:
            return _uncertain(m, rc)
        m.phase = READ_PENDING
        _observe_guard(m)
        return IN_DOUBT if m.expired or m.phase == QUARANTINED else PENDING
    if m.phase == IMPORT_PENDING:
        rc = Esys_TR_FromTPMPublic_Finish(m.esys, &handle)
        m.last_rc = rc
        _observe_guard(m)
        if m.phase == QUARANTINED:
            if rc == 0 and handle != ESYS_TR_NONE:
                m.handle = handle
                m.has_handle = 1
            return IN_DOUBT
        if _retry(rc):
            return IN_DOUBT if m.expired else PENDING
        if rc != 0:
            return _uncertain(m, rc)
        if handle == ESYS_TR_NONE:
            return _uncertain(m, rc)
        m.handle = handle
        m.has_handle = 1
        now = _now()
        if now == 0:
            m.expired = 1
            m.failure = CLOCK
        elif now >= m.deadline:
            m.expired = 1
            if m.failure == OK:
                m.failure = EXPIRED
        if m.expired:
            return _failure(m, m.failure)
        m.phase = BETWEEN
        return PENDING
    rc = Esys_NV_ReadPublic_Finish(m.esys, &pub, &name)
    m.last_rc = rc
    if rc == 0:
        matched = _matches(m, pub, name)
    else:
        matched = 0
    if pub != NULL:
        Esys_Free(pub)
    if name != NULL:
        Esys_Free(name)
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return IN_DOUBT
    if _retry(rc):
        return IN_DOUBT if m.expired else PENDING
    if rc != 0:
        return _uncertain(m, rc)
    now = _now()
    if now == 0:
        m.expired = 1
        m.failure = CLOCK
    elif now >= m.deadline:
        m.expired = 1
        if m.failure == OK:
            m.failure = EXPIRED
    if m.expired:
        return _failure(m, m.failure)
    if not matched:
        return _failure(m, VERIFY)
    m.phase = COMPLETE
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return IN_DOUBT
    return m.failure if m.phase == FAILED else OK

cdef public uint32_t pa01_nv_public_status(
        void *state, uint32_t *last_tss_rc) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if last_tss_rc != NULL:
        last_tss_rc[0] = m.last_rc
    if m.phase == COMPLETE:
        return OK
    if m.phase == FAILED:
        return m.failure
    if m.phase == QUARANTINED or m.expired:
        return IN_DOUBT
    return STATE if m.phase == READY else PENDING

cdef extern from *:
    """
    #include <string.h>
    #include <tss2/tss2_esys.h>
    #include <openssl/crypto.h>
    #include <openssl/rand.h>

    static TSS2_RC pa01_h_clear_auth(ESYS_CONTEXT *context, ESYS_TR handle) {
        TPM2B_AUTH auth;
        TSS2_RC rc;
        memset(&auth, 0, sizeof(auth));
        rc = Esys_TR_SetAuth(context, handle, &auth);
        OPENSSL_cleanse(&auth, sizeof(auth));
        return rc;
    }

    static TSS2_RC pa01_h_set_auth(ESYS_CONTEXT *context, ESYS_TR handle,
                                  const uint8_t *secret) {
        TPM2B_AUTH auth;
        TSS2_RC rc;
        memset(&auth, 0, sizeof(auth));
        auth.size = 32;
        memcpy(auth.buffer, secret, 32);
        rc = Esys_TR_SetAuth(context, handle, &auth);
        OPENSSL_cleanse(&auth, sizeof(auth));
        return rc;
    }

    static int pa01_h_nonce(OSSL_LIB_CTX *context, uint8_t *nonce) {
        return RAND_bytes_ex(context, nonce, 32, 256);
    }

    static TSS2_RC pa01_h_session_async(ESYS_CONTEXT *context, ESYS_TR binding,
                                       const uint8_t *nonce_bytes) {
        TPM2B_NONCE nonce;
        TPMT_SYM_DEF symmetric;
        memset(&nonce, 0, sizeof(nonce));
        memset(&symmetric, 0, sizeof(symmetric));
        nonce.size = 32;
        memcpy(nonce.buffer, nonce_bytes, 32);
        symmetric.algorithm = TPM2_ALG_NULL;
        return Esys_StartAuthSession_Async(context, ESYS_TR_NONE, binding,
            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &nonce,
            TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256);
    }

    static TSS2_RC pa01_h_session_finish(ESYS_CONTEXT *context, ESYS_TR *session) {
        return Esys_StartAuthSession_Finish(context, session);
    }

    static TSS2_RC pa01_h_session_one_use(ESYS_CONTEXT *context, ESYS_TR session) {
        return Esys_TRSess_SetAttributes(
            context, session, 0, TPMA_SESSION_CONTINUESESSION);
    }

    static TSS2_RC pa01_h_read_async(ESYS_CONTEXT *context, ESYS_TR index,
                                    ESYS_TR session) {
        return Esys_NV_Read_Async(context, index, index, session,
                                 ESYS_TR_NONE, ESYS_TR_NONE, 32, 0);
    }

    static TSS2_RC pa01_h_read_finish(ESYS_CONTEXT *context,
                                     uint8_t *value, int *correct_size) {
        TPM2B_MAX_NV_BUFFER *data = NULL;
        TSS2_RC rc;
        *correct_size = 0;
        rc = Esys_NV_Read_Finish(context, &data);
        if (rc == TSS2_RC_SUCCESS && data != NULL && data->size == 32) {
            memcpy(value, data->buffer, 32);
            *correct_size = 1;
        }
        if (data != NULL) Esys_Free(data);
        return rc;
    }

    static TSS2_RC pa01_h_extend_async(ESYS_CONTEXT *context, ESYS_TR index,
                                      ESYS_TR session, const uint8_t *head) {
        TPM2B_MAX_NV_BUFFER data;
        TSS2_RC rc;
        if (head == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
        memset(&data, 0, sizeof(data));
        data.size = 32;
        memcpy(data.buffer, head, 32);
        rc = Esys_NV_Extend_Async(context, index, index, session,
                                 ESYS_TR_NONE, ESYS_TR_NONE, &data);
        OPENSSL_cleanse(&data, sizeof(data));
        return rc;
    }

    static TSS2_RC pa01_h_extend_finish(ESYS_CONTEXT *context) {
        return Esys_NV_Extend_Finish(context);
    }

    static TSS2_RC pa01_h_flush_async(ESYS_CONTEXT *context, ESYS_TR session) {
        return Esys_FlushContext_Async(context, session);
    }

    static TSS2_RC pa01_h_flush_finish(ESYS_CONTEXT *context) {
        return Esys_FlushContext_Finish(context);
    }
    """
    TSS2_RC pa01_h_clear_auth(ESYS_CONTEXT *, ESYS_TR) noexcept nogil
    TSS2_RC pa01_h_set_auth(ESYS_CONTEXT *, ESYS_TR, const uint8_t *) noexcept nogil
    int pa01_h_nonce(OSSL_LIB_CTX *, uint8_t *) noexcept nogil
    TSS2_RC pa01_h_session_async(ESYS_CONTEXT *, ESYS_TR, const uint8_t *) noexcept nogil
    TSS2_RC pa01_h_session_finish(ESYS_CONTEXT *, ESYS_TR *) noexcept nogil
    TSS2_RC pa01_h_session_one_use(ESYS_CONTEXT *, ESYS_TR) noexcept nogil
    TSS2_RC pa01_h_read_async(ESYS_CONTEXT *, ESYS_TR, ESYS_TR) noexcept nogil
    TSS2_RC pa01_h_read_finish(ESYS_CONTEXT *, uint8_t *, int *) noexcept nogil
    TSS2_RC pa01_h_extend_async(ESYS_CONTEXT *, ESYS_TR, ESYS_TR, const uint8_t *) noexcept nogil
    TSS2_RC pa01_h_extend_finish(ESYS_CONTEXT *) noexcept nogil
    TSS2_RC pa01_h_flush_async(ESYS_CONTEXT *, ESYS_TR) noexcept nogil
    TSS2_RC pa01_h_flush_finish(ESYS_CONTEXT *) noexcept nogil

cdef public uint32_t pa01_nv_public_close(void **state_inout) noexcept nogil:
    cdef _PublicRead *m
    cdef TSS2_RC rc
    if state_inout == NULL:
        return ARGUMENT
    if state_inout[0] == NULL:
        return OK
    m = <_PublicRead *>state_inout[0]
    if m.intent_owner != NULL:
        return IN_DOUBT
    _observe_guard(m)
    if (m.phase == IMPORT_PENDING or m.phase == READ_PENDING
            or m.phase == AUTH_SESSION_PENDING or m.phase == AUTH_READ_PENDING
            or m.phase == CLEANUP_PENDING or m.phase == QUARANTINED
            or m.phase == EXTEND_SESSION_PENDING or m.phase == EXTEND_PENDING):
        return IN_DOUBT
    if m.has_session:
        if m.session_live:
            return IN_DOUBT
        # Session TPM déjà consommée ; seule sa métadonnée locale subsiste.
        rc = Esys_TR_Close(m.esys, &m.session)
        m.cleanup_rc = rc
        if rc != 0:
            m.cleanup_status = CLEANUP_ERROR
            return CLEANUP_ERROR
        m.has_session = 0
        m.session = ESYS_TR_NONE
    if m.has_handle:
        if m.auth_set:
            rc = pa01_h_clear_auth(m.esys, m.handle)
            m.cleanup_rc = rc
            if rc != 0:
                m.cleanup_status = CLEANUP_ERROR
                return CLEANUP_ERROR
            m.auth_set = 0
        rc = Esys_TR_Close(m.esys, &m.handle)
        m.cleanup_rc = rc
        if m.auth_deadline == 0:
            m.last_rc = rc
        if rc != 0:
            m.cleanup_status = CLEANUP_ERROR
            return CLEANUP_ERROR
        m.has_handle = 0
    if m.guard != NULL:
        if pa01_tg_unbind(m.guard, <void *>m) != OK:
            return IN_DOUBT
        m.guard = NULL
    OPENSSL_cleanse(m.nv_value, 32)
    memset(m, 0, sizeof(_PublicRead))
    free(m)
    state_inout[0] = NULL
    return OK


cdef uint32_t _auth_fresh(_PublicRead *m) noexcept nogil:
    cdef uint64_t now
    _observe_guard(m)
    if m.guard != NULL:
        if m.phase == QUARANTINED:
            return IN_DOUBT
        if m.phase == FAILED:
            return m.failure
    if m.phase != AUTH_COMPLETE or not m.has_value:
        return STATE
    now = _now()
    if now == 0 or now >= m.auth_deadline:
        OPENSSL_cleanse(m.nv_value, 32)
        m.has_value = 0
        return _failure(m, CLOCK if now == 0 else EXPIRED)
    return OK


cdef public uint32_t pa01_nv_auth_start(
        void *state, int *fd_inout, int fd_timeout_ms,
        uint64_t auth_deadline_ns) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef uint8_t secret[32]
    cdef uint8_t nonce[32]
    cdef uint32_t status
    cdef TSS2_RC rc
    cdef uint64_t now, remaining_ms
    cdef int effective_ms
    if m == NULL or fd_inout == NULL:
        return ARGUMENT
    _observe_guard(m)
    if m.guard != NULL:
        if m.phase == QUARANTINED:
            return IN_DOUBT
        if m.phase == FAILED:
            return m.failure
    if m.guard != NULL and auth_deadline_ns != m.deadline:
        return ARGUMENT
    if (m.phase != COMPLETE or not m.has_handle
            or m.has_session or m.has_value):
        return STATE
    if fd_timeout_ms <= 0 or auth_deadline_ns == 0:
        return ARGUMENT
    now = _now()
    if now == 0:
        return _failure(m, CLOCK)
    if now >= auth_deadline_ns or auth_deadline_ns > m.deadline:
        return _failure(m, EXPIRED)
    remaining_ms = (auth_deadline_ns - now) // 1000000
    if remaining_ms == 0:
        return _failure(m, EXPIRED)
    effective_ms = (fd_timeout_ms if <uint64_t>fd_timeout_ms <= remaining_ms
                    else <int>remaining_ms)
    m.auth_deadline = auth_deadline_ns
    memset(secret, 0, 32)
    status = pa01_nv_secret_read32(fd_inout, secret, 32, effective_ms)
    m.fd_status = status
    if status != 0:
        OPENSSL_cleanse(secret, 32)
        return _failure(m, FD_ERROR)
    now = _now()
    if now == 0 or now >= m.auth_deadline:
        OPENSSL_cleanse(secret, 32)
        return _failure(m, CLOCK if now == 0 else EXPIRED)
    # Même un échec local de SetAuth impose un effacement à la clôture sûre.
    m.auth_set = 1
    rc = pa01_h_set_auth(m.esys, m.handle, secret)
    OPENSSL_cleanse(secret, 32)
    m.last_rc = rc
    if rc != 0:
        return _failure(m, TSS_ERROR)
    memset(nonce, 0, 32)
    if pa01_h_nonce(m.crypto, nonce) != 1:
        OPENSSL_cleanse(nonce, 32)
        return _failure(m, CRYPTO_ERROR)
    rc = Esys_SetTimeout(m.esys, 0)
    m.last_rc = rc
    if rc != 0:
        OPENSSL_cleanse(nonce, 32)
        return _failure(m, TSS_ERROR)
    now = _now()
    if now == 0 or now >= m.auth_deadline:
        OPENSSL_cleanse(nonce, 32)
        return _failure(m, CLOCK if now == 0 else EXPIRED)
    rc = pa01_h_session_async(m.esys, m.handle, nonce)
    OPENSSL_cleanse(nonce, 32)
    m.last_rc = rc
    if rc != 0:
        return _uncertain(m, rc)
    m.phase = AUTH_SESSION_PENDING
    _observe_guard(m)
    return IN_DOUBT if m.expired or m.phase == QUARANTINED else PENDING


cdef public uint32_t pa01_nv_auth_step(void *state) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef TSS2_RC rc, close_rc
    cdef uint64_t now
    cdef ESYS_TR session = ESYS_TR_NONE
    cdef uint8_t value[32]
    cdef int correct_size = 0
    cdef uint32_t outcome
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return IN_DOUBT
    if m.phase == AUTH_COMPLETE:
        return _auth_fresh(m)
    if m.phase == FAILED:
        return m.failure
    if m.phase != AUTH_SESSION_PENDING and m.phase != AUTH_READ_PENDING:
        return STATE
    now = _now()
    if now == 0:
        m.expired = 1
        m.failure = CLOCK
    elif now >= m.auth_deadline:
        m.expired = 1
        if m.failure == OK:
            m.failure = EXPIRED
    if m.phase == AUTH_SESSION_PENDING:
        rc = pa01_h_session_finish(m.esys, &session)
        m.last_rc = rc
        _observe_guard(m)
        if m.phase == QUARANTINED:
            if rc == 0 and session != ESYS_TR_NONE:
                m.session = session
                m.has_session = 1
                m.session_live = 1
            return IN_DOUBT
        if _retry(rc):
            return IN_DOUBT if m.expired else PENDING
        if rc != 0 or session == ESYS_TR_NONE:
            return _uncertain(m, rc)
        # La session créée reste possédée même si SetAttributes échoue.
        m.session = session
        m.has_session = 1
        m.session_live = 1
        now = _now()
        if now == 0 or now >= m.auth_deadline or m.expired:
            if m.failure == OK:
                m.failure = CLOCK if now == 0 else EXPIRED
            return _failure(m, m.failure)
        rc = pa01_h_session_one_use(m.esys, m.session)
        m.last_rc = rc
        if rc != 0:
            return _failure(m, TSS_ERROR)
        now = _now()
        if now == 0 or now >= m.auth_deadline:
            return _failure(m, CLOCK if now == 0 else EXPIRED)
        rc = pa01_h_read_async(m.esys, m.handle, m.session)
        m.last_rc = rc
        if rc != 0:
            return _uncertain(m, rc)
        m.phase = AUTH_READ_PENDING
        _observe_guard(m)
        return IN_DOUBT if m.expired or m.phase == QUARANTINED else PENDING
    memset(value, 0, 32)
    rc = pa01_h_read_finish(m.esys, value, &correct_size)
    m.last_rc = rc
    _observe_guard(m)
    if m.phase == QUARANTINED:
        OPENSSL_cleanse(value, 32)
        return IN_DOUBT
    if _retry(rc):
        OPENSSL_cleanse(value, 32)
        return IN_DOUBT if m.expired else PENDING
    if rc != 0:
        OPENSSL_cleanse(value, 32)
        return _uncertain(m, rc)
    # Une réponse validée à CONTINUESESSION=0 termine la session TPM.
    # ESAPI 4.1.3 conserve sa métadonnée : fermer localement, sans Flush.
    m.session_live = 0
    close_rc = Esys_TR_Close(m.esys, &m.session)
    m.cleanup_rc = close_rc
    if close_rc == 0:
        m.has_session = 0
        m.session = ESYS_TR_NONE
    else:
        m.cleanup_status = CLEANUP_ERROR
    _observe_guard(m)
    if m.phase == QUARANTINED:
        OPENSSL_cleanse(value, 32)
        return IN_DOUBT
    now = _now()
    outcome = OK
    if now == 0:
        outcome = CLOCK
    elif now >= m.auth_deadline or m.expired:
        outcome = m.failure if m.failure != OK else EXPIRED
    elif not correct_size:
        outcome = VERIFY
    elif close_rc != 0:
        outcome = CLEANUP_ERROR
    if outcome != OK:
        OPENSSL_cleanse(value, 32)
        return _failure(m, outcome)
    if m.read_serial == (~<uint64_t>0):
        OPENSSL_cleanse(value, 32)
        return _failure(m, VERIFY)
    memcpy(m.nv_value, value, 32)
    OPENSSL_cleanse(value, 32)
    m.read_serial += 1
    m.has_value = 1
    m.phase = AUTH_COMPLETE
    return _auth_fresh(m) if m.guard != NULL else OK


cdef public uint32_t pa01_nv_auth_status(
        void *state, uint32_t *last_tss_rc,
        uint32_t *fd_status_out) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if last_tss_rc != NULL:
        last_tss_rc[0] = m.last_rc
    if fd_status_out != NULL:
        fd_status_out[0] = m.fd_status
    if m.phase == AUTH_COMPLETE:
        return _auth_fresh(m)
    if m.phase == FAILED:
        return m.failure
    if m.phase == QUARANTINED or m.expired:
        return IN_DOUBT
    if m.phase == AUTH_SESSION_PENDING or m.phase == AUTH_READ_PENDING:
        return PENDING
    return STATE


cdef public uint32_t pa01_nv_auth_value(
        void *state, uint8_t *output, size_t output_size) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef uint32_t status
    if output == NULL or output_size != 32:
        return ARGUMENT
    OPENSSL_cleanse(output, 32)
    if m == NULL:
        return ARGUMENT
    status = _auth_fresh(m)
    if status != OK:
        return status
    memcpy(output, m.nv_value, 32)
    return OK


cdef public uint32_t pa01_nv_cleanup_start(
        void *state, uint64_t cleanup_deadline_ns) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef TSS2_RC rc
    cdef uint64_t now
    cdef uint32_t guard_status
    if m == NULL:
        return ARGUMENT
    if m.guard != NULL:
        guard_status = _observe_guard(m)
        if guard_status != OK:
            m.cleanup_status = guard_status
            return guard_status
        if cleanup_deadline_ns > m.deadline:
            m.cleanup_status = ARGUMENT
            return ARGUMENT
    # Seule notre session vivante, créée et sans commande pendante.
    if m.phase != FAILED or not m.has_session or not m.session_live:
        return STATE
    now = _now()
    if now == 0:
        return CLOCK
    if cleanup_deadline_ns <= now:
        return EXPIRED
    m.cleanup_deadline = cleanup_deadline_ns
    m.cleanup_expired = 0
    m.cleanup_status = OK
    rc = Esys_SetTimeout(m.esys, 0)
    m.cleanup_rc = rc
    if rc != 0:
        m.cleanup_status = CLEANUP_ERROR
        return CLEANUP_ERROR
    now = _now()
    if now == 0 or now >= m.cleanup_deadline:
        m.cleanup_status = CLOCK if now == 0 else EXPIRED
        return m.cleanup_status
    rc = pa01_h_flush_async(m.esys, m.session)
    m.cleanup_rc = rc
    if rc != 0:
        m.phase = QUARANTINED
        m.cleanup_status = IN_DOUBT
        return IN_DOUBT
    m.phase = CLEANUP_PENDING
    _observe_guard(m)
    return IN_DOUBT if m.expired or m.phase == QUARANTINED else PENDING


cdef public uint32_t pa01_nv_cleanup_step(void *state) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef TSS2_RC rc
    cdef uint64_t now
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return IN_DOUBT
    if m.phase != CLEANUP_PENDING:
        return STATE
    now = _now()
    if now == 0 or now >= m.cleanup_deadline:
        m.cleanup_expired = 1
        if m.cleanup_status == OK:
            m.cleanup_status = CLOCK if now == 0 else EXPIRED
    # Même après échéance, Finish peut constater la fin ; jamais un nouvel Async.
    rc = pa01_h_flush_finish(m.esys)
    m.cleanup_rc = rc
    _observe_guard(m)
    if m.phase == QUARANTINED:
        m.cleanup_status = IN_DOUBT
        return IN_DOUBT
    if _retry(rc):
        return IN_DOUBT if m.cleanup_expired else PENDING
    if rc != 0:
        m.phase = QUARANTINED
        m.cleanup_status = IN_DOUBT
        return IN_DOUBT
    # FlushContext_Finish 4.1.3 ferme aussi sa métadonnée ESYS.
    m.has_session = 0
    m.session_live = 0
    m.session = ESYS_TR_NONE
    m.phase = FAILED
    now = _now()
    if now == 0 or now >= m.cleanup_deadline:
        m.cleanup_expired = 1
        if m.cleanup_status == OK:
            m.cleanup_status = CLOCK if now == 0 else EXPIRED
    return m.cleanup_status


cdef public uint32_t pa01_nv_cleanup_status(
        void *state, uint32_t *last_cleanup_rc) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    if m == NULL:
        return ARGUMENT
    _observe_guard(m)
    if last_cleanup_rc != NULL:
        last_cleanup_rc[0] = m.cleanup_rc
    if m.phase == QUARANTINED:
        return IN_DOUBT
    if m.phase == CLEANUP_PENDING:
        return IN_DOUBT if m.cleanup_expired else PENDING
    if m.cleanup_deadline != 0 or m.cleanup_status != OK:
        return m.cleanup_status
    return STATE


# La garde transporte des octets natifs sans leur donner une autorité.
# Le vrai propriétaire fournit un backend qualifié et en conserve la durée de vie.
cdef extern from *:
    """
    #include <tss2/tss2_tcti.h>
    #include <tss2/tss2_tpm2_types.h>
    #include <openssl/crypto.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <time.h>
    #include <unistd.h>

    #define PA01_TG_MAGIC UINT64_C(0x5041303154473031)
    typedef struct {
        TSS2_TCTI_CONTEXT_COMMON_V2 common;
        TSS2_TCTI_CONTEXT *backend;
        uint64_t backend_magic;
        uint32_t backend_version;
        TSS2_TCTI_TRANSMIT_FCN backend_transmit;
        TSS2_TCTI_RECEIVE_FCN backend_receive;
        pid_t pid;
        uint32_t nv_index;
        size_t max_command, max_response;
        uint64_t deadline, tx_calls, rx_calls;
        uint32_t pending, unknown, expired, clock_lost;
        TSS2_RC last_rc;
        void *reader_owner;
    } pa01_tg;

    static uint32_t pa01_tg_be32(const uint8_t *p) {
        return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16)
             | ((uint32_t)p[2] << 8) | (uint32_t)p[3];
    }
    static uint16_t pa01_tg_be16(const uint8_t *p) {
        return (uint16_t)(((uint16_t)p[0] << 8) | p[1]);
    }
    static void pa01_tg_inc(uint64_t *value) {
        if (*value != UINT64_MAX) ++*value;
    }
    static int pa01_tg_now(uint64_t *value) {
        struct timespec ts;
        uint64_t seconds, nanos;
        if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0 ||
            ts.tv_sec < 0 || ts.tv_nsec < 0 || ts.tv_nsec >= 1000000000)
            return 0;
        seconds = (uint64_t)ts.tv_sec;
        nanos = (uint64_t)ts.tv_nsec;
        if (seconds > (UINT64_MAX - nanos) / UINT64_C(1000000000))
            return 0;
        *value = seconds * UINT64_C(1000000000) + nanos;
        return 1;
    }
    static void pa01_tg_observe_time(pa01_tg *g) {
        uint64_t now;
        if (!pa01_tg_now(&now)) g->clock_lost = 1;
        else if (now >= g->deadline) g->expired = 1;
    }
    static int pa01_tg_valid(const pa01_tg *g) {
        return g && g->common.v1.magic == PA01_TG_MAGIC
            && g->common.v1.version == 2 && g->pid == getpid()
            && g->backend;
    }
    static int pa01_tg_backend_valid(pa01_tg *g) {
        const TSS2_TCTI_CONTEXT_COMMON_V1 *b =
            (const TSS2_TCTI_CONTEXT_COMMON_V1 *)g->backend;
        if (b->magic != g->backend_magic || b->version != g->backend_version ||
            b->transmit != g->backend_transmit || b->receive != g->backend_receive) {
            g->unknown = 1;
            g->last_rc = TSS2_TCTI_RC_BAD_CONTEXT;
            return 0;
        }
        return 1;
    }
    static TSS2_RC pa01_tg_command(pa01_tg *g, size_t size,
                                   const uint8_t *command) {
        uint32_t code, a, b;
        uint16_t tag;
        if (!command) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (size < 10 || size > g->max_command ||
            pa01_tg_be32(command + 2) != size) return TSS2_TCTI_RC_BAD_VALUE;
        tag = pa01_tg_be16(command);
        if (tag != TPM2_ST_NO_SESSIONS && tag != TPM2_ST_SESSIONS)
            return TSS2_TCTI_RC_BAD_VALUE;
        code = pa01_tg_be32(command + 6);
        if (code == TPM2_CC_NV_ReadPublic) {
            if (tag != TPM2_ST_NO_SESSIONS || size != 14 ||
                pa01_tg_be32(command + 10) != g->nv_index)
                return TSS2_TCTI_RC_BAD_VALUE;
            return TSS2_RC_SUCCESS;
        }
        if (code == TPM2_CC_NV_Read || code == TPM2_CC_NV_Extend ||
            code == TPM2_CC_StartAuthSession) {
            if (size < 18) return TSS2_TCTI_RC_BAD_VALUE;
            a = pa01_tg_be32(command + 10);
            b = pa01_tg_be32(command + 14);
            if (b != g->nv_index) return TSS2_TCTI_RC_BAD_VALUE;
            if (code == TPM2_CC_StartAuthSession) {
                if (tag != TPM2_ST_NO_SESSIONS || a != TPM2_RH_NULL)
                    return TSS2_TCTI_RC_BAD_VALUE;
            } else if (tag != TPM2_ST_SESSIONS || a != g->nv_index)
                return TSS2_TCTI_RC_BAD_VALUE;
            return TSS2_RC_SUCCESS;
        }
        if (code == TPM2_CC_FlushContext) {
            if (tag != TPM2_ST_NO_SESSIONS || size != 14 ||
                (pa01_tg_be32(command + 10) >> 24) != TPM2_HT_HMAC_SESSION)
                return TSS2_TCTI_RC_BAD_VALUE;
            /* La possession de CETTE session reste vérifiée par ESAPI propriétaire. */
            return TSS2_RC_SUCCESS;
        }
        return TSS2_TCTI_RC_NOT_PERMITTED;
    }
    static TSS2_RC pa01_tg_transmit(TSS2_TCTI_CONTEXT *context, size_t size,
                                    const uint8_t *command) {
        pa01_tg *g = (pa01_tg *)context;
        TSS2_RC rc;
        if (!pa01_tg_valid(g)) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (!pa01_tg_backend_valid(g)) return TSS2_TCTI_RC_BAD_CONTEXT;
        pa01_tg_observe_time(g);
        if (g->unknown) return TSS2_TCTI_RC_BAD_SEQUENCE;
        if (g->clock_lost || g->expired) return TSS2_TCTI_RC_NOT_PERMITTED;
        if (g->pending) return TSS2_TCTI_RC_BAD_SEQUENCE;
        rc = pa01_tg_command(g, size, command);
        if (rc != TSS2_RC_SUCCESS) {
            g->last_rc = rc;
            return rc;
        }
        /* Dernier contrôle avant délégation, sans promesse de latence du backend. */
        pa01_tg_observe_time(g);
        if (g->clock_lost || g->expired) return TSS2_TCTI_RC_NOT_PERMITTED;
        g->pending = 1;
        pa01_tg_inc(&g->tx_calls);
        rc = Tss2_Tcti_Transmit(g->backend, size, command);
        g->last_rc = rc;
        if (rc != TSS2_RC_SUCCESS) g->unknown = 1;
        pa01_tg_observe_time(g);
        /* SUCCESS constate l'acceptation transport, jamais une autorisation. */
        return rc;
    }
    static TSS2_RC pa01_tg_receive(TSS2_TCTI_CONTEXT *context, size_t *size,
                                   uint8_t *response, int32_t timeout) {
        pa01_tg *g = (pa01_tg *)context;
        size_t capacity, amount;
        TSS2_RC rc;
        uint16_t tag;
        (void)timeout;
        if (!pa01_tg_valid(g)) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (!size) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (!g->pending && !g->unknown) return TSS2_TCTI_RC_BAD_SEQUENCE;
        if (!pa01_tg_backend_valid(g)) return TSS2_TCTI_RC_BAD_CONTEXT;
        pa01_tg_observe_time(g);
        capacity = response ? (*size < g->max_response ? *size : g->max_response) : 0;
        if (response && capacity < 10) {
            *size = 10;
            return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
        }
        amount = capacity;
        pa01_tg_inc(&g->rx_calls);
        rc = Tss2_Tcti_Receive(g->backend, &amount, response, 0);
        pa01_tg_observe_time(g);
        if (rc == TSS2_TCTI_RC_TRY_AGAIN) return rc;
        if (rc != TSS2_RC_SUCCESS && rc != TSS2_TCTI_RC_INSUFFICIENT_BUFFER) {
            if (!g->unknown) g->last_rc = rc;
            g->unknown = 1;
            *size = 0;
            return rc;
        }
        if (amount < 10 || amount > g->max_response) {
            g->unknown = 1;
            if (g->last_rc == TSS2_RC_SUCCESS)
                g->last_rc = TSS2_TCTI_RC_MALFORMED_RESPONSE;
            *size = 0;
            return TSS2_TCTI_RC_MALFORMED_RESPONSE;
        }
        *size = amount;
        if (!response || rc == TSS2_TCTI_RC_INSUFFICIENT_BUFFER) return rc;
        if (amount > capacity) {
            g->unknown = 1;
            if (g->last_rc == TSS2_RC_SUCCESS)
                g->last_rc = TSS2_TCTI_RC_MALFORMED_RESPONSE;
            *size = 0;
            return TSS2_TCTI_RC_MALFORMED_RESPONSE;
        }
        tag = pa01_tg_be16(response);
        if ((tag != TPM2_ST_NO_SESSIONS && tag != TPM2_ST_SESSIONS) ||
            pa01_tg_be32(response + 2) != amount) {
            g->unknown = 1;
            if (g->last_rc == TSS2_RC_SUCCESS)
                g->last_rc = TSS2_TCTI_RC_MALFORMED_RESPONSE;
            *size = 0;
            return TSS2_TCTI_RC_MALFORMED_RESPONSE;
        }
        g->pending = 0;
        if (!g->unknown) g->last_rc = TSS2_RC_SUCCESS;
        return TSS2_RC_SUCCESS;
    }
    static void pa01_tg_finalize(TSS2_TCTI_CONTEXT *context) {
        /* Propriété conservée jusqu'à close explicite ; backend jamais finalisé. */
        (void)context;
    }
    static TSS2_RC pa01_tg_cancel(TSS2_TCTI_CONTEXT *c) {
        return pa01_tg_valid((pa01_tg *)c)
            ? TSS2_TCTI_RC_NOT_IMPLEMENTED : TSS2_TCTI_RC_BAD_CONTEXT;
    }
    static TSS2_RC pa01_tg_poll(TSS2_TCTI_CONTEXT *c,
                               TSS2_TCTI_POLL_HANDLE *handles, size_t *count) {
        (void)handles; (void)count;
        return pa01_tg_cancel(c);
    }
    static TSS2_RC pa01_tg_locality(TSS2_TCTI_CONTEXT *c, uint8_t locality) {
        (void)locality;
        return pa01_tg_cancel(c);
    }
    static TSS2_RC pa01_tg_sticky(TSS2_TCTI_CONTEXT *c, TPM2_HANDLE *handle,
                                 uint8_t sticky) {
        (void)handle; (void)sticky;
        return pa01_tg_cancel(c);
    }
    static uint32_t pa01_tg_new(void **state_out, void **tcti_out, void *backend,
            uint32_t index, uint64_t deadline, size_t max_command, size_t max_response) {
        const TSS2_TCTI_CONTEXT_COMMON_V1 *b = backend;
        pa01_tg *g;
        uint64_t now;
        if (!state_out || !tcti_out || state_out == tcti_out ||
            *state_out || *tcti_out || !backend || index < UINT32_C(0x01000000) ||
            index > UINT32_C(0x01ffffff) || max_command < 10 || max_response < 10 ||
            max_command > UINT32_MAX || max_response > UINT32_MAX) return 1;
        if (!pa01_tg_now(&now)) return 3;
        if (deadline <= now) return 6;
        if (!b->magic || (b->version != 1 && b->version != 2) ||
            !b->transmit || !b->receive) return 7;
        g = calloc(1, sizeof(*g));
        if (!g) return 2;
        g->common.v1.magic = PA01_TG_MAGIC;
        g->common.v1.version = 2;
        g->common.v1.transmit = pa01_tg_transmit;
        g->common.v1.receive = pa01_tg_receive;
        g->common.v1.finalize = pa01_tg_finalize;
        g->common.v1.cancel = pa01_tg_cancel;
        g->common.v1.getPollHandles = pa01_tg_poll;
        g->common.v1.setLocality = pa01_tg_locality;
        g->common.makeSticky = pa01_tg_sticky;
        g->backend = backend;
        g->backend_magic = b->magic;
        g->backend_version = b->version;
        g->backend_transmit = b->transmit;
        g->backend_receive = b->receive;
        g->pid = getpid();
        g->nv_index = index;
        g->max_command = max_command;
        g->max_response = max_response;
        g->deadline = deadline;
        *state_out = g;
        *tcti_out = g;
        return 0;
    }
    static uint32_t pa01_tg_status(void *state, uint32_t *flags, uint32_t *last_rc,
                                   uint64_t *tx_calls, uint64_t *rx_calls) {
        pa01_tg *g = state;
        if (flags) *flags = 0;
        if (last_rc) *last_rc = 0;
        if (tx_calls) *tx_calls = 0;
        if (rx_calls) *rx_calls = 0;
        if (!pa01_tg_valid(g) || !flags || !last_rc || !tx_calls || !rx_calls) return 1;
        pa01_tg_backend_valid(g);
        pa01_tg_observe_time(g);
        *flags = g->pending | (g->unknown << 1) | (g->expired << 2) | (g->clock_lost << 3);
        *last_rc = g->last_rc;
        *tx_calls = g->tx_calls;
        *rx_calls = g->rx_calls;
        if (g->unknown) return 9;
        if (g->pending) return 5;
        if (g->clock_lost) return 3;
        if (g->expired) return 6;
        return 0;
    }
    static uint32_t pa01_tg_close(void **state_inout) {
        pa01_tg *g;
        if (!state_inout) return 1;
        g = *state_inout;
        if (!g) return 0;
        if (!pa01_tg_valid(g)) return 4;
        pa01_tg_backend_valid(g);
        if (g->pending || g->unknown || g->reader_owner) return 9;
        OPENSSL_cleanse(g, sizeof(*g));
        free(g);
        *state_inout = NULL;
        return 0;
    }
    """
    uint32_t pa01_tg_new(void **, void **, void *, uint32_t, uint64_t,
                         size_t, size_t) noexcept nogil
    uint32_t pa01_tg_status(void *, uint32_t *, uint32_t *,
                            uint64_t *, uint64_t *) noexcept nogil
    uint32_t pa01_tg_close(void **) noexcept nogil


cdef public uint32_t pa01_tcti_guard_new(void **state_out, void **tcti_out,
        void *backend, uint32_t nv_index, uint64_t deadline_ns,
        size_t max_command, size_t max_response) noexcept nogil:
    return pa01_tg_new(state_out, tcti_out, backend, nv_index,
                      deadline_ns, max_command, max_response)


cdef public uint32_t pa01_tcti_guard_status(void *state, uint32_t *flags_out,
        uint32_t *last_rc_out, uint64_t *tx_calls_out,
        uint64_t *rx_calls_out) noexcept nogil:
    return pa01_tg_status(state, flags_out, last_rc_out, tx_calls_out, rx_calls_out)


cdef public uint32_t pa01_tcti_guard_close(void **state_inout) noexcept nogil:
    return pa01_tg_close(state_inout)


cdef extern from *:
    """
    #include <tss2/tss2_esys.h>
    static uint32_t pa01_tg_pair(void *state, void *esys, uint32_t index,
                                 uint64_t deadline, void *reader, int claim) {
        pa01_tg *g = state;
        TSS2_TCTI_CONTEXT *actual = NULL;
        if (!pa01_tg_valid(g) || !esys || !reader) return 7;
        if (!pa01_tg_backend_valid(g)) return 9;
        pa01_tg_observe_time(g);
        if (g->nv_index != index || g->deadline != deadline ||
            Esys_GetTcti(esys, &actual) != TSS2_RC_SUCCESS ||
            actual != (TSS2_TCTI_CONTEXT *)g) return 7;
        if (claim) {
            if (g->reader_owner) return 4;
            pa01_tg_observe_time(g);
            if (g->unknown || g->pending) return 9;
            if (g->clock_lost) return 3;
            if (g->expired) return 6;
            g->reader_owner = reader;
        } else if (g->reader_owner != reader) return 9;
        return 0;
    }
    static uint32_t pa01_tg_unbind(void *state, void *reader) {
        pa01_tg *g = state;
        if (!pa01_tg_valid(g) || !pa01_tg_backend_valid(g) ||
            g->reader_owner != reader || g->pending || g->unknown) return 9;
        g->reader_owner = NULL;
        return 0;
    }
    """
    uint32_t pa01_tg_pair(void *, void *, uint32_t, uint64_t,
                          void *, int) noexcept nogil
    uint32_t pa01_tg_unbind(void *, void *) noexcept nogil


cdef uint32_t _observe_guard(_PublicRead *m) noexcept nogil:
    cdef uint32_t flags = 0, last = 0, rc, failure
    cdef uint64_t tx = 0, rx = 0
    cdef int pending
    if m.guard == NULL:
        return OK
    rc = pa01_tg_pair(m.guard, m.esys, m.index, m.deadline, <void *>m, 0)
    if rc == OK:
        rc = pa01_tg_status(m.guard, &flags, &last, &tx, &rx)
    pending = (m.phase == IMPORT_PENDING or m.phase == READ_PENDING
        or m.phase == AUTH_SESSION_PENDING or m.phase == AUTH_READ_PENDING
        or m.phase == CLEANUP_PENDING or m.phase == EXTEND_SESSION_PENDING
        or m.phase == EXTEND_PENDING)
    if (rc == ARGUMENT or rc == VERIFY or rc == STATE or rc == IN_DOUBT
            or flags & 2 or (flags & 1 and not pending)):
        OPENSSL_cleanse(m.nv_value, 32)
        m.has_value = 0
        m.phase = QUARANTINED
        if last != 0:
            m.last_rc = last
        return IN_DOUBT
    if flags & 12:
        failure = CLOCK if flags & 8 else EXPIRED
        m.expired = 1
        if m.failure == OK:
            m.failure = failure
        OPENSSL_cleanse(m.nv_value, 32)
        m.has_value = 0
        if m.phase == CLEANUP_PENDING:
            m.cleanup_expired = 1
            if m.cleanup_status == OK:
                m.cleanup_status = failure
        if not pending:
            m.phase = FAILED
        return failure
    return OK


cdef public uint32_t pa01_nv_public_new_guarded(
        void **state_out, void *guard, void *esys_context, void *crypto_context,
        uint32_t index, uint32_t attributes,
        const uint8_t *policy, size_t policy_size,
        const uint8_t *name, size_t name_size, uint64_t deadline_ns) noexcept nogil:
    cdef void *created = NULL
    cdef _PublicRead *m
    cdef uint32_t rc
    if state_out == NULL or state_out[0] != NULL or guard == NULL:
        return ARGUMENT
    rc = pa01_nv_public_new(&created, esys_context, crypto_context, index,
                            attributes, policy, policy_size, name, name_size, deadline_ns)
    if rc != OK:
        return rc
    m = <_PublicRead *>created
    rc = pa01_tg_pair(guard, esys_context, index, deadline_ns, created, 1)
    if rc != OK:
        # Aucun handle, authValue ou IO n'a été créé par l'allocation legacy.
        OPENSSL_cleanse(m, sizeof(_PublicRead))
        free(m)
        return rc
    m.guard = guard
    state_out[0] = created
    return OK


cdef void _nv_lease_clear(uint8_t *value, size_t value_size,
        uint8_t *name, size_t name_size, uint32_t *index,
        uint64_t *deadline) noexcept nogil:
    if value != NULL and value_size == 32:
        OPENSSL_cleanse(value, 32)
    if name != NULL and name_size == 34:
        OPENSSL_cleanse(name, 34)
    if index != NULL:
        index[0] = 0
    if deadline != NULL:
        deadline[0] = 0


cdef uint32_t _nv_lease_export(_PublicRead *m,
        uint8_t *value, size_t value_size, uint8_t *name, size_t name_size,
        uint32_t *index, uint64_t *deadline) noexcept nogil:
    cdef uint32_t status
    _nv_lease_clear(value, value_size, name, name_size, index, deadline)
    if (m == NULL or value == NULL or value_size != 32 or name == NULL
            or name_size != 34 or index == NULL or deadline == NULL):
        return ARGUMENT
    if m.guard == NULL:
        return STATE
    status = _auth_fresh(m)
    if status != OK:
        return status
    if not m.has_handle or m.has_session or m.session_live:
        return STATE
    memcpy(value, m.nv_value, 32)
    memcpy(name, m.name, 34)
    index[0] = m.index
    deadline[0] = m.deadline
    status = _auth_fresh(m)
    if status != OK:
        _nv_lease_clear(value, value_size, name, name_size, index, deadline)
    return status


cdef public uint32_t pa01_nv_lease_acquire(void *state, void *owner,
        uint8_t *value, size_t value_size, uint8_t *name, size_t name_size,
        uint32_t *index, uint64_t *deadline) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef uint32_t status
    _nv_lease_clear(value, value_size, name, name_size, index, deadline)
    if m == NULL or owner == NULL:
        return ARGUMENT
    if m.intent_owner != NULL:
        return STATE
    status = _nv_lease_export(m, value, value_size, name, name_size, index, deadline)
    if status == OK:
        m.intent_owner = owner
    return status


cdef public uint32_t pa01_nv_lease_snapshot(void *state, void *owner,
        uint8_t *value, size_t value_size, uint8_t *name, size_t name_size,
        uint32_t *index, uint64_t *deadline) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    _nv_lease_clear(value, value_size, name, name_size, index, deadline)
    if m == NULL or owner == NULL:
        return ARGUMENT
    if m.intent_owner != owner:
        return STATE
    return _nv_lease_export(m, value, value_size, name, name_size, index, deadline)


cdef public uint32_t pa01_nv_lease_release(void *state, void *owner) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef uint32_t status = pa01_nv_lease_quiescent(state, owner)
    if status != OK:
        return status
    m.intent_owner = NULL
    return OK

cdef public uint32_t pa01_nv_lease_read_serial(void *state, void *owner,
        uint64_t *serial_out) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef uint32_t status
    if serial_out != NULL:
        serial_out[0] = 0
    if m == NULL or owner == NULL or serial_out == NULL:
        return ARGUMENT
    if m.guard == NULL or m.intent_owner != owner:
        return STATE
    status = _auth_fresh(m)
    if status != OK:
        return status
    if (not m.has_handle or not m.auth_set or m.has_session
            or m.session_live or m.read_serial == 0):
        return STATE
    serial_out[0] = m.read_serial
    return OK


cdef public uint32_t pa01_nv_lease_refresh_start(void *state,
        void *owner) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    cdef uint8_t nonce[32]
    cdef uint64_t now
    cdef TSS2_RC rc
    if m == NULL or owner == NULL:
        return ARGUMENT
    if m.guard == NULL or m.intent_owner != owner:
        return STATE
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return IN_DOUBT
    if m.phase == FAILED:
        return m.failure
    if m.phase != AUTH_COMPLETE:
        return STATE
    if (not m.has_handle or not m.auth_set or m.has_session or m.session_live
            or m.read_serial == (~<uint64_t>0)
            or m.auth_deadline != m.deadline):
        return STATE
    memset(nonce, 0, 32)
    if pa01_h_nonce(m.crypto, nonce) != 1:
        OPENSSL_cleanse(nonce, 32)
        return _failure(m, CRYPTO_ERROR)
    rc = Esys_SetTimeout(m.esys, 0)
    m.last_rc = rc
    if rc != 0:
        OPENSSL_cleanse(nonce, 32)
        return _failure(m, TSS_ERROR)
    now = _now()
    if now == 0 or now >= m.auth_deadline:
        OPENSSL_cleanse(nonce, 32)
        return _failure(m, CLOCK if now == 0 else EXPIRED)
    OPENSSL_cleanse(m.nv_value, 32)
    m.has_value = 0
    rc = pa01_h_session_async(m.esys, m.handle, nonce)
    OPENSSL_cleanse(nonce, 32)
    m.last_rc = rc
    if rc != 0:
        return _uncertain(m, rc)
    m.phase = AUTH_SESSION_PENDING
    _observe_guard(m)
    return IN_DOUBT if m.expired or m.phase == QUARANTINED else PENDING


cdef public uint32_t pa01_nv_lease_quiescent(void *state,
        void *owner) noexcept nogil:
    cdef _PublicRead *m = <_PublicRead *>state
    if m == NULL or owner == NULL:
        return ARGUMENT
    if m.guard == NULL or m.intent_owner != owner:
        return STATE
    _observe_guard(m)
    if (m.phase != AUTH_COMPLETE and m.phase != FAILED
            or m.has_session or m.session_live or not m.has_handle):
        return IN_DOUBT
    # Expiration connue permise pour détachement seulement, jamais pour une IO.
    return OK


cdef extern from "nv_intent.h" nogil:
    uint32_t pa01_intent_claim_owned(void *, void *, uint8_t *, size_t,
        uint8_t *, size_t, uint8_t *, size_t, void **, void **, uint32_t *) noexcept
    uint32_t pa01_intent_confirm_owned(void *, void *, void *, uint32_t *) noexcept
    uint32_t pa01_intent_consumer_release(void *, void *, uint32_t *) noexcept
    uint32_t pa01_intent_journal_current_owned(void *, void *, uint32_t *) noexcept
    uint32_t pa01_intent_abandon_owned(void *, void *, void *, uint32_t *) noexcept

cdef enum:
    X_REFRESH = 1
    X_SESSION = 2
    X_READY = 3
    X_EXTEND = 4
    X_CONFIRM = 5
    X_DONE = 6
    X_FAILED = 7
    X_IN_DOUBT = 8
    X_CANCEL_PENDING = 9
    X_CANCELLED = 10

cdef struct _Extend:
    void *intent
    void *journal
    _PublicRead *reader
    uint8_t head[32]
    uint8_t old_nv[32]
    uint8_t expected_nv[32]
    uint8_t name[34]
    uint32_t index
    uint64_t deadline
    uint64_t initial_serial
    uint64_t fresh_serial
    uint32_t phase
    uint32_t primary
    uint32_t first_tss
    uint32_t cleanup
    uint32_t cleanup_tss
    uint32_t detail[4]
    int attempted
    int cancelled

cdef void _x_note(_Extend *e, uint32_t code) noexcept nogil:
    if e.primary == OK or e.primary == PENDING:
        e.primary = code

cdef uint32_t _x_fail(_Extend *e, uint32_t code, int unknown) noexcept nogil:
    _x_note(e, code)
    e.phase = X_IN_DOUBT if unknown or e.attempted else X_FAILED
    return IN_DOUBT if e.phase == X_IN_DOUBT else e.primary

cdef uint32_t _x_tss_fail(_Extend *e, TSS2_RC rc) noexcept nogil:
    if e.first_tss == 0:
        e.first_tss = rc
    _uncertain(e.reader, rc)
    return _x_fail(e, TSS_ERROR, 1)

cdef uint32_t _x_guard(_Extend *e, int allow_finish) noexcept nogil:
    cdef _PublicRead *m = e.reader
    cdef uint32_t code
    if (m == NULL or m.guard == NULL or m.intent_owner != e.intent
            or m.index != e.index or m.deadline != e.deadline
            or m.auth_deadline != e.deadline or memcmp(m.name, e.name, 34) != 0):
        return _x_fail(e, STATE, 1)
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return _x_fail(e, IN_DOUBT, 1)
    if m.phase == FAILED:
        return _x_fail(e, m.failure if m.failure != OK else STATE, 0)
    if m.expired:
        code = m.failure if m.failure != OK else EXPIRED
        _x_note(e, code)
        if not allow_finish:
            _failure(m, code)
            return _x_fail(e, code, 0)
    return OK

cdef uint32_t _x_refresh_start(_Extend *e, uint32_t phase) noexcept nogil:
    cdef uint32_t rc
    e.phase = phase
    rc = pa01_nv_lease_refresh_start(<void *>e.reader, e.intent)
    if rc == PENDING:
        return PENDING
    if (rc == IN_DOUBT and e.reader.phase != QUARANTINED
            and (e.reader.phase == AUTH_SESSION_PENDING
                 or e.reader.phase == AUTH_READ_PENDING)):
        _x_note(e, e.reader.failure if e.reader.failure != OK else EXPIRED)
        return IN_DOUBT
    return _x_fail(e, rc, rc == IN_DOUBT)

cdef public uint32_t pa01_nv_extend_start(void **state_out,
        void *intent) noexcept nogil:
    cdef _Extend *e
    cdef void *reader = NULL
    cdef uint32_t rc
    if state_out == NULL or state_out[0] != NULL or intent == NULL:
        return ARGUMENT
    e = <_Extend *>calloc(1, sizeof(_Extend))
    if e == NULL:
        return MEMORY
    e.intent = intent
    e.primary = PENDING
    rc = pa01_intent_claim_owned(intent, <void *>e, e.head, 32,
        e.old_nv, 32, e.expected_nv, 32, &e.journal, &reader, e.detail)
    if rc != OK:
        OPENSSL_cleanse(e, sizeof(_Extend))
        free(e)
        return rc
    # Après claim, l'adresse consumer doit rester vivante sur tout échec.
    e.reader = <_PublicRead *>reader
    e.phase = X_FAILED
    state_out[0] = <void *>e
    if e.reader == NULL or e.journal == NULL:
        return _x_fail(e, STATE, 1)
    e.index = e.reader.index
    e.deadline = e.reader.deadline
    memcpy(e.name, e.reader.name, 34)
    rc = _x_guard(e, 0)
    if rc != OK:
        return rc
    rc = pa01_nv_lease_read_serial(reader, intent, &e.initial_serial)
    if rc != OK:
        return _x_fail(e, rc, rc == IN_DOUBT)
    return _x_refresh_start(e, X_REFRESH)

cdef uint32_t _x_session_start(_Extend *e) noexcept nogil:
    cdef _PublicRead *m = e.reader
    cdef uint8_t nonce[32]
    cdef TSS2_RC rc
    cdef uint32_t status
    status = _x_guard(e, 0)
    if status != OK:
        return status
    if (m.phase != AUTH_COMPLETE or not m.has_handle or not m.auth_set
            or m.has_session or m.session_live or not m.has_value):
        return _x_fail(e, STATE, 1)
    memset(nonce, 0, 32)
    if pa01_h_nonce(m.crypto, nonce) != 1:
        OPENSSL_cleanse(nonce, 32)
        _failure(m, CRYPTO_ERROR)
        return _x_fail(e, CRYPTO_ERROR, 0)
    rc = Esys_SetTimeout(m.esys, 0)
    m.last_rc = rc
    if rc != 0:
        OPENSSL_cleanse(nonce, 32)
        if e.first_tss == 0:
            e.first_tss = rc
        _failure(m, TSS_ERROR)
        return _x_fail(e, TSS_ERROR, 0)
    status = _x_guard(e, 0)
    if status != OK:
        OPENSSL_cleanse(nonce, 32)
        return status
    m.phase = EXTEND_SESSION_PENDING
    e.phase = X_SESSION
    rc = pa01_h_session_async(m.esys, m.handle, nonce)
    OPENSSL_cleanse(nonce, 32)
    m.last_rc = rc
    if rc != 0:
        return _x_tss_fail(e, rc)
    status = _x_guard(e, 1)
    if status != OK:
        return status
    return IN_DOUBT if m.expired else PENDING

cdef public uint32_t pa01_nv_extend_step(void *state) noexcept nogil:
    cdef _Extend *e = <_Extend *>state
    cdef _PublicRead *m
    cdef uint32_t status
    cdef TSS2_RC rc, close_rc
    cdef ESYS_TR session = ESYS_TR_NONE
    if e == NULL:
        return ARGUMENT
    if e.cancelled:
        return pa01_nv_extend_cancel_step(state)
    if e.phase == X_DONE:
        return OK
    if e.phase == X_IN_DOUBT:
        return IN_DOUBT
    if e.phase == X_FAILED:
        return e.primary
    status = _x_guard(e, 1)
    if status != OK:
        return status
    m = e.reader
    if e.phase == X_REFRESH or e.phase == X_CONFIRM:
        rc = pa01_nv_auth_step(<void *>m)
        if rc == PENDING:
            return PENDING
        if (rc == IN_DOUBT and m.phase != QUARANTINED
                and (m.phase == AUTH_SESSION_PENDING or m.phase == AUTH_READ_PENDING)):
            _x_note(e, m.failure if m.failure != OK else EXPIRED)
            return IN_DOUBT
        if rc != OK:
            if m.last_rc != 0 and not _retry(m.last_rc) and e.first_tss == 0:
                e.first_tss = m.last_rc
            return _x_fail(e, rc, rc == IN_DOUBT)
        if e.phase == X_CONFIRM:
            if memcmp(m.nv_value, e.expected_nv, 32) != 0:
                return _x_fail(e, VERIFY, 1)
            status = pa01_intent_confirm_owned(e.intent, <void *>e, <void *>m, e.detail)
            if status != OK:
                return _x_fail(e, status, 1)
            e.phase = X_DONE
            e.primary = OK
            return OK
        status = pa01_nv_lease_read_serial(<void *>m, e.intent, &e.fresh_serial)
        if status != OK:
            return _x_fail(e, status, status == IN_DOUBT)
        if (e.fresh_serial <= e.initial_serial
                or memcmp(m.nv_value, e.old_nv, 32) != 0):
            return _x_fail(e, VERIFY, 1)
        return _x_session_start(e)
    if e.phase == X_SESSION:
        if m.phase != EXTEND_SESSION_PENDING:
            return _x_fail(e, STATE, 1)
        rc = pa01_h_session_finish(m.esys, &session)
        m.last_rc = rc
        # Toute session effectivement renvoyée demeure possédée, même tardive.
        if rc == 0 and session != ESYS_TR_NONE:
            m.session = session
            m.has_session = 1
            m.session_live = 1
        status = _x_guard(e, 1)
        if status != OK:
            return status
        if _retry(rc):
            return IN_DOUBT if m.expired else PENDING
        if rc != 0 or session == ESYS_TR_NONE:
            return _x_tss_fail(e, rc)
        status = _x_guard(e, 0)
        if status != OK:
            return status
        rc = pa01_h_session_one_use(m.esys, m.session)
        m.last_rc = rc
        if rc != 0:
            if e.first_tss == 0:
                e.first_tss = rc
            _failure(m, TSS_ERROR)
            return _x_fail(e, TSS_ERROR, 0)
        status = _x_guard(e, 0)
        if status != OK:
            return status
        m.phase = EXTEND_READY
        e.phase = X_READY
        return PENDING
    if e.phase == X_READY:
        status = _x_guard(e, 0)
        return status if status != OK else PENDING
    if e.phase != X_EXTEND or m.phase != EXTEND_PENDING:
        return _x_fail(e, STATE, 1)
    rc = pa01_h_extend_finish(m.esys)
    m.last_rc = rc
    if rc == 0:
        m.session_live = 0
    status = _x_guard(e, 1)
    if status != OK:
        return status
    if _retry(rc):
        return IN_DOUBT if m.expired else PENDING
    if rc != 0:
        return _x_tss_fail(e, rc)
    close_rc = Esys_TR_Close(m.esys, &m.session)
    m.cleanup_rc = close_rc
    if close_rc != 0:
        m.cleanup_status = CLEANUP_ERROR
        e.cleanup = CLEANUP_ERROR
        e.cleanup_tss = close_rc
        _failure(m, CLEANUP_ERROR)
        return _x_fail(e, CLEANUP_ERROR, 1)
    m.has_session = 0
    m.session = ESYS_TR_NONE
    m.phase = AUTH_COMPLETE
    status = _x_guard(e, 0)
    if status != OK:
        return status
    return _x_refresh_start(e, X_CONFIRM)

cdef public uint32_t pa01_nv_extend_commit(void *state) noexcept nogil:
    cdef _Extend *e = <_Extend *>state
    cdef _PublicRead *m
    cdef uint32_t status
    cdef TSS2_RC rc
    if e == NULL:
        return ARGUMENT
    if e.phase != X_READY or e.attempted or e.cancelled:
        return STATE
    status = _x_guard(e, 0)
    if status != OK:
        return status
    m = e.reader
    if (m.phase != EXTEND_READY or not m.has_handle or not m.auth_set
            or not m.has_session or not m.session_live or not m.has_value
            or m.read_serial != e.fresh_serial or memcmp(m.nv_value, e.old_nv, 32) != 0):
        return _x_fail(e, STATE, 1)
    status = pa01_intent_journal_current_owned(e.intent, <void *>e, e.detail)
    if status != OK:
        return _x_fail(e, status, status == IN_DOUBT)
    status = _x_guard(e, 0)
    if status != OK:
        return status
    # Tentative irréversible enregistrée avant Async ; aucun second commit.
    e.attempted = 1
    e.phase = X_EXTEND
    m.phase = EXTEND_PENDING
    OPENSSL_cleanse(m.nv_value, 32)
    m.has_value = 0
    rc = pa01_h_extend_async(m.esys, m.handle, m.session, e.head)
    m.last_rc = rc
    if rc != 0:
        return _x_tss_fail(e, rc)
    status = _x_guard(e, 1)
    if status != OK:
        return status
    return IN_DOUBT if m.expired else PENDING

cdef public uint32_t pa01_nv_extend_status(void *state, uint32_t *phase_out,
        uint32_t *primary_out, uint32_t *tss_out, uint32_t *cleanup_out,
        uint32_t *cleanup_tss_out) noexcept nogil:
    cdef _Extend *e = <_Extend *>state
    if phase_out != NULL:
        phase_out[0] = 0
    if primary_out != NULL:
        primary_out[0] = 0
    if tss_out != NULL:
        tss_out[0] = 0
    if cleanup_out != NULL:
        cleanup_out[0] = 0
    if cleanup_tss_out != NULL:
        cleanup_tss_out[0] = 0
    if (e == NULL or phase_out == NULL or primary_out == NULL or tss_out == NULL
            or cleanup_out == NULL or cleanup_tss_out == NULL):
        return ARGUMENT
    phase_out[0] = e.phase
    primary_out[0] = e.primary
    tss_out[0] = e.first_tss
    cleanup_out[0] = e.cleanup
    cleanup_tss_out[0] = e.cleanup_tss
    # État historique uniquement : aucune autorisation actuelle n'en découle.
    if e.phase == X_DONE:
        return OK
    if e.phase == X_IN_DOUBT:
        return IN_DOUBT
    if e.phase == X_FAILED or e.phase == X_CANCELLED:
        return e.primary
    return IN_DOUBT if e.reader != NULL and e.reader.expired else PENDING

cdef public uint32_t pa01_nv_extend_close(void **state_inout) noexcept nogil:
    cdef _Extend *e
    cdef uint32_t rc
    if state_inout == NULL:
        return ARGUMENT
    if state_inout[0] == NULL:
        return OK
    e = <_Extend *>state_inout[0]
    if e.phase == X_DONE:
        rc = pa01_intent_consumer_release(e.intent, <void *>e, e.detail)
        if rc != OK:
            return IN_DOUBT
        OPENSSL_cleanse(e, sizeof(_Extend))
        free(e)
        state_inout[0] = NULL
        return OK
    if e.attempted:
        return IN_DOUBT
    rc = pa01_intent_abandon_owned(e.intent, <void *>e, <void *>e.reader, e.detail)
    if rc != OK:
        return IN_DOUBT
    OPENSSL_cleanse(e, sizeof(_Extend))
    free(e)
    state_inout[0] = NULL
    # Liens détachés sans effet NV : l'intention durable reste non ancrée.
    return IN_DOUBT


cdef public uint32_t pa01_nv_extend_abort_fact(void *state, void *intent,
        void *reader) noexcept nogil:
    cdef _Extend *e = <_Extend *>state
    if e == NULL or intent == NULL or reader == NULL:
        return ARGUMENT
    if (e.intent != intent or <void *>e.reader != reader or e.attempted
            or e.phase == X_DONE):
        return STATE
    # Fait du consommateur réel, pas une déclaration de succès de l'appelant.
    return pa01_nv_lease_quiescent(reader, intent)


cdef void _x_cleanup_note(_Extend *e, uint32_t code,
        uint32_t native_rc) noexcept nogil:
    if code != OK and code != PENDING and e.cleanup == OK:
        e.cleanup = code
        e.cleanup_tss = native_rc


cdef public uint32_t pa01_nv_extend_cancel_step(void *state) noexcept nogil:
    cdef _Extend *e = <_Extend *>state
    cdef _PublicRead *m
    cdef TSS2_RC rc
    cdef ESYS_TR session = ESYS_TR_NONE
    cdef uint32_t status
    if e == NULL:
        return ARGUMENT
    if e.attempted or e.phase == X_DONE:
        return STATE
    e.cancelled = 1
    _x_note(e, STATE)
    e.phase = X_CANCEL_PENDING
    m = e.reader
    if (m == NULL or m.guard == NULL or m.intent_owner != e.intent
            or m.index != e.index or m.deadline != e.deadline
            or memcmp(m.name, e.name, 34) != 0):
        return _x_fail(e, STATE, 1)
    _observe_guard(m)
    if m.phase == QUARANTINED:
        return _x_fail(e, IN_DOUBT, 1)
    if m.phase == AUTH_SESSION_PENDING or m.phase == EXTEND_SESSION_PENDING:
        # Drainage de la création déjà émise, sans démarrer NV_Read.
        rc = pa01_h_session_finish(m.esys, &session)
        m.last_rc = rc
        if rc == 0 and session != ESYS_TR_NONE:
            m.session = session
            m.has_session = 1
            m.session_live = 1
        _observe_guard(m)
        if m.phase == QUARANTINED:
            return _x_fail(e, IN_DOUBT, 1)
        if _retry(rc):
            return IN_DOUBT if m.expired else PENDING
        if rc != 0 or session == ESYS_TR_NONE:
            return _x_tss_fail(e, rc)
        m.phase = FAILED
        if m.failure == OK:
            m.failure = e.primary
    elif m.phase == AUTH_READ_PENDING:
        # Ici AuthStep termine seulement le Read déjà envoyé et sa métadonnée.
        status = pa01_nv_auth_step(<void *>m)
        if m.phase == QUARANTINED:
            return _x_fail(e, IN_DOUBT, 1)
        if status == PENDING:
            return PENDING
        if status == IN_DOUBT and m.phase == AUTH_READ_PENDING:
            return IN_DOUBT
        if m.phase != FAILED and m.phase != AUTH_COMPLETE:
            return _x_fail(e, status, 1)
    elif m.phase == CLEANUP_PENDING:
        status = pa01_nv_cleanup_step(<void *>m)
        if status == PENDING:
            return PENDING
        _x_cleanup_note(e, status, m.cleanup_rc)
        if m.phase == QUARANTINED:
            return _x_fail(e, IN_DOUBT, 1)
        if status == IN_DOUBT and m.phase == CLEANUP_PENDING:
            return IN_DOUBT
        if m.has_session or m.session_live:
            return IN_DOUBT
    if (m.phase != AUTH_COMPLETE and m.phase != FAILED
            and m.phase != EXTEND_READY):
        return STATE
    if m.has_session and m.session_live:
        m.phase = FAILED
        if m.failure == OK:
            m.failure = e.primary
        # Aucun budget nouveau ; le garde refuse tout Flush tardif.
        status = pa01_nv_cleanup_start(<void *>m, m.deadline)
        _x_cleanup_note(e, status, m.cleanup_rc)
        return status
    if m.has_session:
        # Session TPM déjà consommée : fermeture de métadonnée locale seulement.
        rc = Esys_TR_Close(m.esys, &m.session)
        m.cleanup_rc = rc
        if rc != 0:
            m.cleanup_status = CLEANUP_ERROR
            _x_cleanup_note(e, CLEANUP_ERROR, rc)
            return CLEANUP_ERROR
        m.has_session = 0
        m.session = ESYS_TR_NONE
    m.phase = FAILED
    if m.failure == OK:
        m.failure = e.primary
    OPENSSL_cleanse(m.nv_value, 32)
    m.has_value = 0
    status = pa01_nv_lease_quiescent(<void *>m, e.intent)
    if status != OK:
        return status
    e.phase = X_CANCELLED
    return OK
