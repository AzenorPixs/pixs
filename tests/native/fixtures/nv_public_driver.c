/* Conducteur ESAPI SIMULE pour nv_anchor, fixtures publiques seulement.
 * A lier exclusivement dans l'extension de test, jamais dans PA/PZT.
 * Les vrais headers tpm2-tss sont requis ; aucune connexion TCTI/TPM.
 * Lien de TEST : -Bsymbolic-functions et wrappers clock_gettime,
 * RAND_bytes_ex et pa01_nv_secret_read32 ; aucun de ces flags en production.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <tss2/tss2_esys.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>
#include <openssl/provider.h>
#include "nv_anchor.h"

#define FIXTURE_INDEX UINT32_C(0x01500001)
#define FIXTURE_HANDLE UINT32_C(0x8000fffe)
#define FIXTURE_SESSION UINT32_C(0x8000fffd)
#define FIXTURE_ATTRIBUTES (TPMA_NV_PLATFORMCREATE | TPMA_NV_POLICY_DELETE | \
    TPMA_NV_AUTHREAD | TPMA_NV_AUTHWRITE | TPMA_NV_WRITTEN | \
    ((uint32_t)TPM2_NT_EXTEND << 4))

/* Structure uniquement simulee : ce conducteur n'utilise pas libtss2-esys. */
struct ESYS_CONTEXT {
    TSS2_TCTI_CONTEXT *tcti;
    int pending;
    unsigned int count[20];
    uint32_t mode[25];
    uint8_t nv_value[32];
    uint8_t extend_head[32];
    int extend_applied;
    int broken;
    int auth_set;
    int session_live;
    int session_metadata;
    TPMA_SESSION session_attributes;
    OSSL_LIB_CTX *crypto;
};

/* L'artefact de test utilise --wrap=clock_gettime ; aucun build produit
 * n'emploie ce conducteur ou ce remplacement d'horloge monotone. */
static uint64_t fixture_now = UINT64_C(1000000000);
static int fixture_clock_error;

void pa01_test_clock(uint64_t now, int error) {
    fixture_now = now;
    fixture_clock_error = error;
}

int __real_clock_gettime(clockid_t clock, struct timespec *value);
int __wrap_clock_gettime(clockid_t clock, struct timespec *value) {
    if (clock != CLOCK_MONOTONIC) return __real_clock_gettime(clock, value);
    if (fixture_clock_error) return -1;
    value->tv_sec = (time_t)(fixture_now / UINT64_C(1000000000));
    value->tv_nsec = (long)(fixture_now % UINT64_C(1000000000));
    return 0;
}

static unsigned int freed_buffers;

unsigned int pa01_test_freed_buffers(void) {
    return freed_buffers;
}

typedef struct {
    ESYS_CONTEXT esys;
    OSSL_LIB_CTX *crypto;
    OSSL_PROVIDER *provider;
} Fixture;

void *pa01_test_fixture_new(void) {
    Fixture *f = calloc(1, sizeof(*f));
    if (!f) return NULL;
    f->crypto = OSSL_LIB_CTX_new();
    if (f->crypto) f->provider = OSSL_PROVIDER_load(f->crypto, "default");
    if (!f->provider) {
        OSSL_LIB_CTX_free(f->crypto);
        free(f);
        return NULL;
    }
    f->esys.crypto = f->crypto;
    memset(f->esys.nv_value, 0xa3, 32);
    return f;
}

uint32_t pa01_test_open(void *fixture, void **state, const uint8_t *name,
                       size_t name_size, uint64_t deadline_ns,
                       uint32_t attributes) {
    Fixture *f = fixture;
    uint8_t policy[32];
    if (!f) return 1;
    memset(policy, 0x31, sizeof(policy));
    return pa01_nv_public_new(state, &f->esys, f->crypto, FIXTURE_INDEX,
        attributes, policy, sizeof(policy), name, name_size, deadline_ns);
}

uint32_t pa01_test_attributes(void) {
    return FIXTURE_ATTRIBUTES;
}

/* Modes : mismatch, from_try, read_try, async_error, finish_error,
 * close_error, settimeout_error, allocation_missing.
 */
int pa01_test_set(void *fixture, unsigned int key, uint32_t value) {
    Fixture *f = fixture;
    if (!f || key >= 25) return -1;
    f->esys.mode[key] = value;
    return 0;
}

int pa01_test_count(void *fixture, unsigned int key) {
    Fixture *f = fixture;
    if (!f || key >= 20) return -1;
    return (int)f->esys.count[key];
}

/* La fin d'un processus de test isole est requise pour une quarantaine.
 * Le conducteur ne fabrique pas de quiescence pour permettre sa destruction.
 */
int pa01_test_fixture_free(void *fixture) {
    Fixture *f = fixture;
    if (!f) return 0;
    if (f->esys.pending || f->esys.broken || f->esys.auth_set
        || f->esys.session_live || f->esys.session_metadata) return -1;
    if (OSSL_PROVIDER_unload(f->provider) != 1) return -2;
    OSSL_LIB_CTX_free(f->crypto);
    free(f);
    return 0;
}

TSS2_RC Esys_GetTcti(ESYS_CONTEXT *c, TSS2_TCTI_CONTEXT **out) {
    if (!c || !out) return TSS2_ESYS_RC_BAD_REFERENCE;
    *out = c->tcti;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_SetTimeout(ESYS_CONTEXT *c, int32_t timeout) {
    c->count[0]++;
    if (timeout != 0) return TSS2_ESYS_RC_BAD_VALUE;
    return c->mode[6];
}

TSS2_RC Esys_TR_FromTPMPublic_Async(ESYS_CONTEXT *c, TPM2_HANDLE index,
                                  ESYS_TR a, ESYS_TR b, ESYS_TR d) {
    c->count[1]++;
    if (c->pending || index != FIXTURE_INDEX
        || a != ESYS_TR_NONE || b != ESYS_TR_NONE || d != ESYS_TR_NONE)
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    c->pending = 1;
    if (c->mode[3]) c->broken = 1;
    return c->mode[3];
}

TSS2_RC Esys_TR_FromTPMPublic_Finish(ESYS_CONTEXT *c, ESYS_TR *handle) {
    c->count[2]++;
    if (c->pending != 1) return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[4]) {
        c->broken = 1;
        return c->mode[4];
    }
    if (c->mode[1]) {
        c->mode[1]--;
        return TSS2_TCTI_RC_TRY_AGAIN;
    }
    c->pending = 0;
    *handle = FIXTURE_HANDLE;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_NV_ReadPublic_Async(ESYS_CONTEXT *c, ESYS_TR handle,
                               ESYS_TR a, ESYS_TR b, ESYS_TR d) {
    c->count[3]++;
    if (c->pending || handle != FIXTURE_HANDLE
        || a != ESYS_TR_NONE || b != ESYS_TR_NONE || d != ESYS_TR_NONE)
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    c->pending = 2;
    if (c->mode[3]) c->broken = 1;
    return c->mode[3];
}

TSS2_RC Esys_NV_ReadPublic_Finish(ESYS_CONTEXT *c,
                                TPM2B_NV_PUBLIC **pub, TPM2B_NAME **name) {
    uint8_t wire[46] = {0x01, 0x50, 0x00, 0x01, 0x00, 0x0b};
    uint32_t attrs = FIXTURE_ATTRIBUTES;
    TPM2B_NV_PUBLIC *p;
    TPM2B_NAME *n;
    size_t size = 0;
    c->count[4]++;
    *pub = NULL;
    *name = NULL;
    if (c->pending != 2) return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[4]) {
        c->broken = 1;
        return c->mode[4];
    }
    if (c->mode[2]) {
        c->mode[2]--;
        return TSS2_ESYS_RC_TRY_AGAIN;
    }
    p = calloc(1, sizeof(*p));
    n = calloc(1, sizeof(*n));
    if (!p || !n) {
        free(p);
        free(n);
        c->broken = 1;
        return TSS2_ESYS_RC_MEMORY;
    }
    p->size = 46;
    p->nvPublic.nvIndex = FIXTURE_INDEX;
    p->nvPublic.nameAlg = TPM2_ALG_SHA256;
    p->nvPublic.attributes = attrs;
    p->nvPublic.authPolicy.size = 32;
    memset(p->nvPublic.authPolicy.buffer, 0x31, 32);
    p->nvPublic.dataSize = 32;
    n->size = 34;
    n->name[0] = 0;
    n->name[1] = TPM2_ALG_SHA256;
    wire[6] = (uint8_t)(attrs >> 24);
    wire[7] = (uint8_t)(attrs >> 16);
    wire[8] = (uint8_t)(attrs >> 8);
    wire[9] = (uint8_t)attrs;
    wire[11] = 32;
    memset(wire + 12, 0x31, 32);
    wire[45] = 32;
    /* Contexte prive du conducteur, aucun recours au contexte global. */
    if (EVP_Q_digest(c->crypto, "SHA256", "provider=default",
                     wire, sizeof(wire), n->name + 2, &size) != 1 || size != 32) {
        free(p);
        free(n);
        c->broken = 1;
        return TSS2_ESYS_RC_GENERAL_FAILURE;
    }
    switch (c->mode[0]) {
        case 1: p->nvPublic.nvIndex++; break;
        case 2: p->nvPublic.nameAlg = TPM2_ALG_SHA384; break;
        case 3: p->nvPublic.attributes ^= TPMA_NV_NO_DA; break;
        case 4: p->nvPublic.dataSize = 31; break;
        case 5: p->nvPublic.authPolicy.buffer[0] ^= 1; break;
        case 6: n->name[2] ^= 1; break;
        case 7: p->size = 45; break;
        default: break;
    }
    c->pending = 0;
    if (c->mode[7] == 1) { free(p); p = NULL; }
    if (c->mode[7] == 2) { free(n); n = NULL; }
    *pub = p;
    *name = n;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_TR_Close(ESYS_CONTEXT *c, ESYS_TR *handle) {
    if (*handle == FIXTURE_SESSION) {
        c->count[16]++;
        if (c->pending || c->session_live || !c->session_metadata)
            return TSS2_ESYS_RC_BAD_SEQUENCE;
        if (c->mode[15]) return c->mode[15];
        c->session_metadata = 0;
        *handle = ESYS_TR_NONE;
        return TSS2_RC_SUCCESS;
    }
    c->count[5]++;
    if (c->pending || *handle != FIXTURE_HANDLE || c->auth_set)
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[5]) return c->mode[5];
    *handle = ESYS_TR_NONE;
    return TSS2_RC_SUCCESS;
}

void Esys_Free(void *pointer) {
    if (pointer) freed_buffers++;
    free(pointer);
}

/* Wrappers réservés à l'artefact TEST, sans accès TPM/credential réel. */
static int random_failure;
static uint64_t after_fd_now;
static int last_fd_budget;

void pa01_test_auth_timing(uint64_t after_fd, int fail_random) {
    after_fd_now = after_fd;
    random_failure = fail_random;
    last_fd_budget = 0;
}
int pa01_test_fd_budget(void) { return last_fd_budget; }

int __real_RAND_bytes_ex(OSSL_LIB_CTX *, unsigned char *, size_t, unsigned int);
int __wrap_RAND_bytes_ex(OSSL_LIB_CTX *context, unsigned char *out,
                        size_t size, unsigned int strength) {
    if (random_failure) return 0;
    return __real_RAND_bytes_ex(context, out, size, strength);
}

uint32_t __real_pa01_nv_secret_read32(int *, uint8_t *, size_t, int);
uint32_t __wrap_pa01_nv_secret_read32(int *fd, uint8_t *out,
                                     size_t size, int timeout_ms) {
    uint32_t rc;
    last_fd_budget = timeout_ms;
    rc = __real_pa01_nv_secret_read32(fd, out, size, timeout_ms);
    if (after_fd_now) fixture_now = after_fd_now;
    return rc;
}

TSS2_RC Esys_TR_SetAuth(ESYS_CONTEXT *c, ESYS_TR handle,
                       const TPM2B_AUTH *auth) {
    static const uint8_t public_fixture[32] =
        "0123456789abcdef0123456789abcdef";
    if (c->pending || handle != FIXTURE_HANDLE || !auth)
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (auth->size == 0) {
        c->count[8]++;
        if (c->mode[16]) return c->mode[16];
        c->auth_set = 0;
        return TSS2_RC_SUCCESS;
    }
    c->count[7]++;
    if (auth->size != 32 || memcmp(auth->buffer, public_fixture, 32) != 0)
        return TSS2_ESYS_RC_BAD_VALUE;
    c->auth_set = 1;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_StartAuthSession_Async(
        ESYS_CONTEXT *c, ESYS_TR key, ESYS_TR bind,
        ESYS_TR a, ESYS_TR b, ESYS_TR d, const TPM2B_NONCE *nonce,
        TPM2_SE type, const TPMT_SYM_DEF *symmetric, TPMI_ALG_HASH hash) {
    c->count[9]++;
    if (c->pending || c->session_live || c->session_metadata || !c->auth_set
        || key != ESYS_TR_NONE || bind != FIXTURE_HANDLE
        || a != ESYS_TR_NONE || b != ESYS_TR_NONE || d != ESYS_TR_NONE
        || !nonce || nonce->size != 32 || !symmetric
        || symmetric->algorithm != TPM2_ALG_NULL
        || type != TPM2_SE_HMAC || hash != TPM2_ALG_SHA256)
        return TSS2_ESYS_RC_BAD_VALUE;
    c->pending = 3;
    if (c->mode[17]) c->broken = 1;
    return c->mode[17];
}

TSS2_RC Esys_StartAuthSession_Finish(ESYS_CONTEXT *c, ESYS_TR *session) {
    c->count[10]++;
    if (c->pending != 3) return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[18]) { c->broken = 1; return c->mode[18]; }
    if (c->mode[8]) { c->mode[8]--; return TSS2_TCTI_RC_TRY_AGAIN; }
    c->pending = 0;
    c->session_live = 1;
    c->session_metadata = 1;
    c->session_attributes = TPMA_SESSION_CONTINUESESSION;
    *session = FIXTURE_SESSION;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_TRSess_SetAttributes(ESYS_CONTEXT *c, ESYS_TR session,
                                 TPMA_SESSION flags, TPMA_SESSION mask) {
    c->count[11]++;
    if (c->pending || !c->session_live || !c->session_metadata
        || session != FIXTURE_SESSION || flags != 0
        || mask != TPMA_SESSION_CONTINUESESSION)
        return TSS2_ESYS_RC_BAD_VALUE;
    if (c->mode[10]) return c->mode[10];
    c->session_attributes = 0;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_NV_Read_Async(
        ESYS_CONTEXT *c, ESYS_TR auth, ESYS_TR index, ESYS_TR session,
        ESYS_TR b, ESYS_TR d, UINT16 size, UINT16 offset) {
    c->count[12]++;
    if (c->pending || !c->session_live || !c->session_metadata
        || !c->auth_set || c->session_attributes != 0
        || auth != FIXTURE_HANDLE || index != FIXTURE_HANDLE
        || session != FIXTURE_SESSION || b != ESYS_TR_NONE || d != ESYS_TR_NONE
        || size != 32 || offset != 0)
        return TSS2_ESYS_RC_BAD_VALUE;
    c->pending = 4;
    if (c->mode[19]) c->broken = 1;
    return c->mode[19];
}

TSS2_RC Esys_NV_Read_Finish(ESYS_CONTEXT *c, TPM2B_MAX_NV_BUFFER **out) {
    TPM2B_MAX_NV_BUFFER *data;
    c->count[13]++;
    *out = NULL;
    if (c->pending != 4) return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[11]) { c->broken = 1; return c->mode[11]; }
    if (c->mode[9]) { c->mode[9]--; return TSS2_ESYS_RC_TRY_AGAIN; }
    data = calloc(1, sizeof(*data));
    if (!data) { c->broken = 1; return TSS2_ESYS_RC_MEMORY; }
    data->size = c->mode[12] ? (uint16_t)c->mode[12] : 32;
    memcpy(data->buffer, c->nv_value, 32);
    c->pending = 0;
    c->session_live = 0;
    /* La métadonnée ESYS subsiste après Read, conformément à TSS4.1.3. */
    *out = data;
    return TSS2_RC_SUCCESS;
}

TSS2_RC Esys_FlushContext_Async(ESYS_CONTEXT *c, ESYS_TR session) {
    c->count[14]++;
    if (c->pending || !c->session_live || !c->session_metadata
        || session != FIXTURE_SESSION)
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    c->pending = 5;
    if (c->mode[14]) c->broken = 1;
    return c->mode[14];
}

TSS2_RC Esys_FlushContext_Finish(ESYS_CONTEXT *c) {
    c->count[15]++;
    if (c->pending != 5) return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[20]) { c->broken = 1; return c->mode[20]; }
    if (c->mode[13]) { c->mode[13]--; return TSS2_TCTI_RC_TRY_AGAIN; }
    c->pending = 0;
    c->session_live = 0;
    /* FlushContext_Finish supprime aussi sa métadonnée dans TSS4.1.3. */
    c->count[16]++;
    if (c->mode[15]) { c->broken = 1; return c->mode[15]; }
    c->session_metadata = 0;
    return TSS2_RC_SUCCESS;
}


/* Backend TCTI de TEST, sans périphérique, réseau ou ESAPI réel.
 * Les pointeurs en quarantaine sont conservés dans un processus de test isolé.
 */
#include <tss2/tss2_tcti.h>
typedef struct {
    TSS2_TCTI_CONTEXT_COMMON_V2 common;
    void *guard;
    void *tcti;
    TSS2_RC tx_rc, rx_rc;
    uint32_t tries, reply_size, bad_length;
    uint64_t after_tx;
    int clock_error_after_tx;
    uint32_t tx_calls, rx_calls, controls, finalizes;
    int32_t last_timeout;
    size_t last_capacity;
} Pa01TgFixture;

static void pa01_tgtest_be32(uint8_t *out, uint32_t value) {
    out[0] = (uint8_t)(value >> 24); out[1] = (uint8_t)(value >> 16);
    out[2] = (uint8_t)(value >> 8); out[3] = (uint8_t)value;
}
static TSS2_RC pa01_tgtest_backend_tx(TSS2_TCTI_CONTEXT *c, size_t size,
                                      const uint8_t *command) {
    Pa01TgFixture *f = (Pa01TgFixture *)c;
    (void)size; (void)command;
    if (f->tx_calls != UINT32_MAX) ++f->tx_calls;
    if (f->after_tx) fixture_now = f->after_tx;
    if (f->clock_error_after_tx) fixture_clock_error = 1;
    return f->tx_rc;
}
static TSS2_RC pa01_tgtest_backend_rx(TSS2_TCTI_CONTEXT *c, size_t *size,
                                      uint8_t *response, int32_t timeout) {
    Pa01TgFixture *f = (Pa01TgFixture *)c;
    size_t capacity = *size;
    uint8_t packet[128] = {0};
    if (f->rx_calls != UINT32_MAX) ++f->rx_calls;
    f->last_timeout = timeout;
    f->last_capacity = response ? capacity : 0;
    if (f->tries) {
        --f->tries;
        return TSS2_TCTI_RC_TRY_AGAIN;
    }
    if (f->rx_rc != TSS2_RC_SUCCESS) {
        if (f->rx_rc == TSS2_TCTI_RC_INSUFFICIENT_BUFFER) *size = f->reply_size;
        return f->rx_rc;
    }
    *size = f->reply_size;
    if (!response) return TSS2_RC_SUCCESS;
    if (capacity < f->reply_size || f->reply_size > sizeof(packet))
        return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
    packet[0] = 0x80; packet[1] = 0x01;
    pa01_tgtest_be32(packet + 2, f->reply_size + (f->bad_length ? 1 : 0));
    memcpy(response, packet, f->reply_size);
    return TSS2_RC_SUCCESS;
}
static void pa01_tgtest_backend_final(TSS2_TCTI_CONTEXT *c) {
    Pa01TgFixture *f = (Pa01TgFixture *)c;
    if (f->finalizes != UINT32_MAX) ++f->finalizes;
}
static TSS2_RC pa01_tgtest_backend_control(TSS2_TCTI_CONTEXT *c) {
    Pa01TgFixture *f = (Pa01TgFixture *)c;
    if (f->controls != UINT32_MAX) ++f->controls;
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}
static TSS2_RC pa01_tgtest_backend_poll(TSS2_TCTI_CONTEXT *c,
                                       TSS2_TCTI_POLL_HANDLE *h, size_t *n) {
    (void)h; (void)n;
    return pa01_tgtest_backend_control(c);
}
static TSS2_RC pa01_tgtest_backend_locality(TSS2_TCTI_CONTEXT *c, uint8_t locality) {
    (void)locality;
    return pa01_tgtest_backend_control(c);
}
static TSS2_RC pa01_tgtest_backend_sticky(TSS2_TCTI_CONTEXT *c,
                                         TPM2_HANDLE *h, uint8_t sticky) {
    (void)h; (void)sticky;
    return pa01_tgtest_backend_control(c);
}
void *pa01_tgtest_new(void) {
    Pa01TgFixture *f = calloc(1, sizeof(*f));
    if (!f) return NULL;
    f->common.v1.magic = UINT64_C(0x5443544954455354);
    f->common.v1.version = 2;
    f->common.v1.transmit = pa01_tgtest_backend_tx;
    f->common.v1.receive = pa01_tgtest_backend_rx;
    f->common.v1.finalize = pa01_tgtest_backend_final;
    f->common.v1.cancel = pa01_tgtest_backend_control;
    f->common.v1.getPollHandles = pa01_tgtest_backend_poll;
    f->common.v1.setLocality = pa01_tgtest_backend_locality;
    f->common.makeSticky = pa01_tgtest_backend_sticky;
    f->reply_size = 10;
    return f;
}
uint32_t pa01_tgtest_open(void *fixture, uint32_t index, uint64_t deadline,
                          size_t max_command, size_t max_response) {
    Pa01TgFixture *f = fixture;
    if (!f) return 1;
    return pa01_tcti_guard_new(&f->guard, &f->tcti, f, index,
                               deadline, max_command, max_response);
}
uint32_t pa01_tgtest_status(void *fixture, uint32_t *flags, uint32_t *rc,
                            uint64_t *tx, uint64_t *rx) {
    Pa01TgFixture *f = fixture;
    return pa01_tcti_guard_status(f ? f->guard : NULL, flags, rc, tx, rx);
}
uint32_t pa01_tgtest_close(void *fixture) {
    Pa01TgFixture *f = fixture;
    uint32_t rc;
    if (!f) return 1;
    rc = pa01_tcti_guard_close(&f->guard);
    if (!rc) f->tcti = NULL;
    return rc;
}
int pa01_tgtest_free(void *fixture) {
    Pa01TgFixture *f = fixture;
    if (!f) return -1;
    if (pa01_tgtest_close(f) != 0) return -1;
    free(f);
    return 0;
}
uint32_t pa01_tgtest_tx(void *fixture, const uint8_t *data, size_t size) {
    Pa01TgFixture *f = fixture;
    TSS2_TCTI_CONTEXT *tcti_ctx = f ? f->tcti : NULL;
    return Tss2_Tcti_Transmit(tcti_ctx, size, data);
}
uint32_t pa01_tgtest_rx(void *fixture, uint8_t *data, size_t *size, int32_t timeout) {
    Pa01TgFixture *f = fixture;
    TSS2_TCTI_CONTEXT *tcti_ctx = f ? f->tcti : NULL;
    return Tss2_Tcti_Receive(tcti_ctx, size, data, timeout);
}
int pa01_tgtest_set(void *fixture, unsigned field, uint64_t value) {
    Pa01TgFixture *f = fixture;
    if (!f) return -1;
    switch (field) {
    case 0: f->tx_rc = (TSS2_RC)value; break;
    case 1: f->rx_rc = (TSS2_RC)value; break;
    case 2: f->tries = (uint32_t)value; break;
    case 3: f->reply_size = (uint32_t)value; break;
    case 4: f->bad_length = value != 0; break;
    case 5: f->after_tx = value; break;
    case 6: f->clock_error_after_tx = value != 0; break;
    case 7: f->common.v1.magic = value; break;
    case 8: f->common.v1.version = (uint32_t)value; break;
    case 9: f->common.v1.transmit = value ? NULL : pa01_tgtest_backend_tx; break;
    case 10: f->common.v1.receive = value ? NULL : pa01_tgtest_backend_rx; break;
    default: return -1;
    }
    return 0;
}
uint64_t pa01_tgtest_count(void *fixture, unsigned field) {
    Pa01TgFixture *f = fixture;
    if (!f) return UINT64_MAX;
    switch (field) {
    case 0: return f->tx_calls;
    case 1: return f->rx_calls;
    case 2: return f->controls;
    case 3: return f->finalizes;
    case 4: return (uint32_t)f->last_timeout;
    case 5: return f->last_capacity;
    default: return UINT64_MAX;
    }
}
uint32_t pa01_tgtest_control(void *fixture, unsigned which) {
    Pa01TgFixture *f = fixture;
    size_t count = 0;
    TPM2_HANDLE handle = 0;
    if (!f || !f->tcti) return TSS2_TCTI_RC_BAD_REFERENCE;
    switch (which) {
    case 0: Tss2_Tcti_Finalize((TSS2_TCTI_CONTEXT *)f->tcti); return 0;
    case 1: return Tss2_Tcti_Cancel((TSS2_TCTI_CONTEXT *)f->tcti);
    case 2: return Tss2_Tcti_GetPollHandles((TSS2_TCTI_CONTEXT *)f->tcti, NULL, &count);
    case 3: return Tss2_Tcti_SetLocality((TSS2_TCTI_CONTEXT *)f->tcti, 1);
    case 4: return Tss2_Tcti_MakeSticky((TSS2_TCTI_CONTEXT *)f->tcti, &handle, 1);
    default: return TSS2_TCTI_RC_BAD_VALUE;
    }
}


/* Liaison LOCALE de test : ESAPI simulé, pas identité/transport TPM qualifié. */
uint32_t pa01_tgtest_open_reader(void *tg_fixture, void *nv_fixture,
        void **out, const uint8_t *name, size_t name_size,
        uint64_t deadline, uint32_t index, int associate) {
    Pa01TgFixture *g = tg_fixture;
    Fixture *f = nv_fixture;
    uint8_t policy[32];
    if (!g || !f || !out || !name) return 1;
    f->esys.tcti = associate ? g->tcti : NULL;
    memset(policy, 0x31, sizeof(policy));
    return pa01_nv_public_new_guarded(out, g->guard, &f->esys, f->crypto,
        index, FIXTURE_ATTRIBUTES, policy, sizeof(policy), name, name_size, deadline);
}


/* NV_Extend SIMULÉ : aucune commande TPM, aucune preuve HMAC réelle.
 * Modes21/22 : erreurs Async/Finish ; 23 : TRY_AGAIN borné ;
 * 24 : valeur modifiée puis réponse perdue, état conservé inconnu.
 * Compteurs17/18 : Async/Finish ; 19 : applications simulées effectives.
 */
TSS2_RC Esys_NV_Extend_Async(ESYS_CONTEXT *c, ESYS_TR auth, ESYS_TR index,
        ESYS_TR first, ESYS_TR second, ESYS_TR third,
        const TPM2B_MAX_NV_BUFFER *data) {
    if (c == NULL || data == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
    c->count[17]++;
    if (c->pending || c->broken || !c->auth_set || !c->session_live
            || !c->session_metadata || c->session_attributes != 0
            || auth != FIXTURE_HANDLE || index != FIXTURE_HANDLE
            || first != FIXTURE_SESSION || second != ESYS_TR_NONE
            || third != ESYS_TR_NONE || data->size != 32)
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    memcpy(c->extend_head, data->buffer, 32);
    c->extend_applied = 0;
    c->pending = 6;
    if (c->mode[21]) c->broken = 1;
    return c->mode[21];
}

TSS2_RC Esys_NV_Extend_Finish(ESYS_CONTEXT *c) {
    uint8_t input[64], digest[32];
    size_t size = 0;
    int good;
    if (c == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
    c->count[18]++;
    if (c->pending != 6) return TSS2_ESYS_RC_BAD_SEQUENCE;
    if (c->mode[22]) { c->broken = 1; return c->mode[22]; }
    if (c->mode[23]) { c->mode[23]--; return TSS2_ESYS_RC_TRY_AGAIN; }
    if (!c->extend_applied) {
        memcpy(input, c->nv_value, 32);
        memcpy(input + 32, c->extend_head, 32);
        good = EVP_Q_digest(c->crypto, "SHA256", NULL, input, sizeof(input),
                           digest, &size);
        OPENSSL_cleanse(input, sizeof(input));
        if (good != 1 || size != 32) {
            OPENSSL_cleanse(digest, sizeof(digest));
            c->broken = 1;
            return TSS2_ESYS_RC_GENERAL_FAILURE;
        }
        memcpy(c->nv_value, digest, 32);
        OPENSSL_cleanse(digest, sizeof(digest));
        c->extend_applied = 1;
        c->session_live = 0;
        c->count[19]++;
    }
    if (c->mode[24]) { c->broken = 1; return c->mode[24]; }
    c->pending = 0;
    /* Session TPM consommée ; métadonnée ESYS à fermer localement. */
    return TSS2_RC_SUCCESS;
}
