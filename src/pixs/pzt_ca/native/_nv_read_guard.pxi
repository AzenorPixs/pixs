# Privé Z12 : lecture NV authentifiée, sans admission applicative ou opérateur.
# Inclure après _openssl_ed25519.pxi et _nv_secret_fd.pxi, une seule fois par unité.
# Contexte ESYS neuf/exclusif et binding issus des sources natives protégées du propriétaire.
# Le propriétaire contrôle cible device, politique, temps, journal et durée de vie.
# Il détruit son contexte/TCTI exclusif si must_destroy_context vaut 1.
# Les attentes Finish sont bornées ; transmission et destruction restent à qualifier.
include "_esys_crypto.pxi"
include "_monotonic_deadline.pxi"
# Inclut le TCTI une seule fois, apres son echeance monotone.
include "_tcti_deadline.pxi"
from libc.stdint cimport uint32_t

cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <string.h>
    #include <tss2/tss2_esys.h>
    #include <tss2/tss2_mu.h>
    #include <openssl/crypto.h>
    #include <openssl/evp.h>
    #include <openssl/rand.h>

    typedef struct {
        uint32_t index;
        unsigned char public_sha256[32];
        unsigned char name_sha256[32];
        unsigned char expected_value[32];
    } Z12NvReadBinding;

    typedef struct {
        uint32_t primary_tss_rc;
        uint32_t cleanup_tss_rc;
        int openssl_failed;
        int invalid_library_output;
        int deadline_expired;
        int clock_failed;
        int clock_errno;
        int must_destroy_context;
        int transport_unusable;
    } Z12NvReadDiagnostic;

    static void z12_nv_read_cleanup_result(
        TSS2_RC rc, int *result, Z12NvReadDiagnostic *diagnostic
    ) {
        if (rc != TSS2_RC_SUCCESS) {
            if (diagnostic->cleanup_tss_rc == TSS2_RC_SUCCESS)
                diagnostic->cleanup_tss_rc = rc;
            *result = -1;
        }
    }


    enum Z12NvStage {
        Z12_NV_FROM_PUBLIC, Z12_NV_READ_PUBLIC, Z12_NV_START_SESSION,
        Z12_NV_READ_VALUE, Z12_NV_FLUSH_SESSION
    };
    static int z12_nv_read_deadline(Z12MonotonicDeadline *deadline,
        Z12NvReadDiagnostic *diagnostic, int32_t *timeout_ms) {
        int status = z12_deadline_remaining(deadline, timeout_ms);
        if (status != 1) {
            diagnostic->must_destroy_context = 1;
            if (status == 0) diagnostic->deadline_expired = 1;
            else {
                diagnostic->clock_failed = 1;
                diagnostic->clock_errno = status == -1 ? errno : EINVAL;
            }
            return -1;
        }
        return 1;
    }
    static int z12_nv_read_check_transport(ESYS_CONTEXT *esys, Z12MonotonicDeadline *deadline, Z12NvReadDiagnostic *diagnostic);
    static int z12_nv_read_check_transport(ESYS_CONTEXT *esys, Z12MonotonicDeadline *deadline, Z12NvReadDiagnostic *diagnostic) {
        TSS2_TCTI_CONTEXT *tcti = NULL;
        TSS2_RC rc;
        rc = Esys_GetTcti(esys, &tcti);
        if (rc != TSS2_RC_SUCCESS) {
            if (diagnostic->primary_tss_rc == TSS2_RC_SUCCESS) diagnostic->primary_tss_rc = rc;
            diagnostic->transport_unusable = 1;
            diagnostic->must_destroy_context = 1;
            return -1;
        }
        if (z12_tcti_is_bound_for_deadline(tcti, deadline) != 1) {
            diagnostic->transport_unusable = 1;
            diagnostic->must_destroy_context = 1;
            return -1;
        }
        return 1;
    }

    static int z12_nv_read_budget(ESYS_CONTEXT *esys, Z12MonotonicDeadline *deadline,
                                  Z12NvReadDiagnostic *diagnostic) {
        int32_t timeout_ms = 0;
        TSS2_RC rc;
        if (z12_nv_read_deadline(deadline, diagnostic, &timeout_ms) != 1) return -1;
        if (z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) return -1;
        rc = Esys_SetTimeout(esys, timeout_ms);
        if (rc != TSS2_RC_SUCCESS) {
            if (diagnostic->primary_tss_rc == TSS2_RC_SUCCESS) diagnostic->primary_tss_rc = rc;
            diagnostic->must_destroy_context = 1;
            return -1;
        }
        return 1;
    }
    static int z12_nv_read_finish(ESYS_CONTEXT *esys, enum Z12NvStage stage,
        Z12MonotonicDeadline *deadline, Z12NvReadDiagnostic *diagnostic,
        int *pending, ESYS_TR *handle, TPM2B_NV_PUBLIC **nv_public,
        TPM2B_NAME **nv_name, TPM2B_MAX_NV_BUFFER **data) {
        TSS2_RC rc;
        int32_t remaining_ms = 0;
        for (;;) {
            if (z12_nv_read_budget(esys, deadline, diagnostic) != 1) return -1;
            switch (stage) {
                case Z12_NV_FROM_PUBLIC: rc = Esys_TR_FromTPMPublic_Finish(esys, handle); break;
                case Z12_NV_READ_PUBLIC: rc = Esys_NV_ReadPublic_Finish(esys, nv_public, nv_name); break;
                case Z12_NV_START_SESSION: rc = Esys_StartAuthSession_Finish(esys, handle); break;
                case Z12_NV_READ_VALUE: rc = Esys_NV_Read_Finish(esys, data); break;
                case Z12_NV_FLUSH_SESSION: rc = Esys_FlushContext_Finish(esys); break;
                default:
                    diagnostic->invalid_library_output = 1;
                    diagnostic->must_destroy_context = 1;
                    return -1;
            }
            if ((rc & ~TSS2_RC_LAYER_MASK) == TSS2_BASE_RC_TRY_AGAIN) {
                if (z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) return -1;
                continue;
            }
            if (rc != TSS2_RC_SUCCESS) {
                if (diagnostic->primary_tss_rc == TSS2_RC_SUCCESS) diagnostic->primary_tss_rc = rc;
                diagnostic->must_destroy_context = 1;
                return -1;
            }
            if (z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) return -1;
            *pending = 0;
            /* Un succès reçu après l'échéance ne peut jamais être accepté. */
            return z12_nv_read_deadline(deadline, diagnostic, &remaining_ms);
        }
    }

    static int z12_nv_read_guard(
        ESYS_CONTEXT *esys, OSSL_LIB_CTX *libctx,
        const Z12NvReadBinding *binding, const Z12NvSecret *secret,
        Z12MonotonicDeadline *deadline, Z12NvReadDiagnostic *diagnostic
    ) {
        int result = -2;
        int pending = 0;
        int32_t final_remaining_ms = 0;
        ESYS_TR nv_handle = ESYS_TR_NONE;
        ESYS_TR session = ESYS_TR_NONE;
        TPM2B_NV_PUBLIC *nv_public = NULL;
        TPM2B_NAME *nv_name = NULL;
        TPM2B_NAME *resource_name = NULL;
        TPM2B_MAX_NV_BUFFER *data = NULL;
        TSS2_RC rc;
        TPMA_NV attrs;
        const TPMA_NV required = TPMA_NV_PLATFORMCREATE | TPMA_NV_POLICY_DELETE
                                | TPMA_NV_WRITTEN | TPMA_NV_AUTHREAD | TPMA_NV_AUTHWRITE;
        const TPMA_NV allowed = required | TPMA_NV_TPM2_NT_MASK | TPMA_NV_NO_DA;
        unsigned char public_bytes[sizeof(TPMS_NV_PUBLIC)] = {0};
        unsigned char public_digest[32] = {0};
        unsigned char name_digest[32] = {0};
        unsigned char calculated_name[34] = {0};
        size_t public_size = 0;
        size_t digest_size = 0;
        TPM2B_NONCE nonce = {0};
        TPM2B_AUTH auth = {0};
        TPM2B_AUTH empty_auth = {0};
        TPMT_SYM_DEF symmetric = {0};

        if (diagnostic == NULL) return -2;
        memset(diagnostic, 0, sizeof(*diagnostic));
        if (esys == NULL || libctx == NULL || binding == NULL || secret == NULL || deadline == NULL) return -2;
        if (secret->loaded != 1) return -2;
        if ((binding->index & TPM2_HR_RANGE_MASK) != TPM2_HR_NV_INDEX) return -2;
        if (z12_nv_read_deadline(deadline, diagnostic, &final_remaining_ms) != 1) return -1;
        if (z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) return -1;

        rc = z12_esys_crypto_install(esys, libctx);
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; diagnostic->must_destroy_context = 1; return -1; }
        if (z12_nv_read_budget(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        rc = Esys_TR_FromTPMPublic_Async(esys, binding->index,
            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
        pending = 1;
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; diagnostic->must_destroy_context = 1; result = -1; goto cleanup; }
        if (z12_nv_read_finish(esys, Z12_NV_FROM_PUBLIC, deadline, diagnostic,
            &pending, &nv_handle, NULL, NULL, NULL) != 1) { result = -1; goto cleanup; }
        if (z12_nv_read_budget(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        rc = Esys_NV_ReadPublic_Async(esys, nv_handle,
            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
        pending = 1;
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; diagnostic->must_destroy_context = 1; result = -1; goto cleanup; }
        if (z12_nv_read_finish(esys, Z12_NV_READ_PUBLIC, deadline, diagnostic,
            &pending, NULL, &nv_public, &nv_name, NULL) != 1) { result = -1; goto cleanup; }
        if (nv_public == NULL || nv_name == NULL) {
            diagnostic->invalid_library_output = 1; result = -1; goto cleanup;
        }
        if (z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        if (z12_nv_read_deadline(deadline, diagnostic, &final_remaining_ms) != 1) { result = -1; goto cleanup; }
        result = 0;
        if (nv_public->nvPublic.nvIndex != binding->index
            || nv_public->nvPublic.nameAlg != TPM2_ALG_SHA256
            || nv_public->nvPublic.dataSize != 32
            || nv_public->nvPublic.authPolicy.size != 32) goto cleanup;
        attrs = nv_public->nvPublic.attributes;
        if ((attrs & required) != required || (attrs & ~allowed) != 0) goto cleanup;
        if (((attrs & TPMA_NV_TPM2_NT_MASK) >> TPMA_NV_TPM2_NT_SHIFT) != TPM2_NT_EXTEND) goto cleanup;

        rc = Tss2_MU_TPMS_NV_PUBLIC_Marshal(&nv_public->nvPublic,
            public_bytes, sizeof(public_bytes), &public_size);
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; result = -1; goto cleanup; }
        if (EVP_Q_digest(libctx, "SHA256", "provider=default", public_bytes,
            public_size, public_digest, &digest_size) != 1) {
            diagnostic->openssl_failed = 1; result = -1; goto cleanup;
        }
        if (digest_size != 32) { diagnostic->invalid_library_output = 1; result = -1; goto cleanup; }
        if (CRYPTO_memcmp(public_digest, binding->public_sha256, 32) != 0) goto cleanup;
        calculated_name[0] = (unsigned char)(TPM2_ALG_SHA256 >> 8);
        calculated_name[1] = (unsigned char)(TPM2_ALG_SHA256 & 0xff);
        memcpy(calculated_name + 2, public_digest, 32);
        if (nv_name->size != sizeof(calculated_name)
            || CRYPTO_memcmp(nv_name->name, calculated_name, sizeof(calculated_name)) != 0) goto cleanup;
        digest_size = 0;
        if (EVP_Q_digest(libctx, "SHA256", "provider=default", calculated_name,
            sizeof(calculated_name), name_digest, &digest_size) != 1) {
            diagnostic->openssl_failed = 1; result = -1; goto cleanup;
        }
        if (digest_size != 32) { diagnostic->invalid_library_output = 1; result = -1; goto cleanup; }
        if (CRYPTO_memcmp(name_digest, binding->name_sha256, 32) != 0) goto cleanup;
        rc = Esys_TR_GetName(esys, nv_handle, &resource_name);
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; result = -1; goto cleanup; }
        if (resource_name == NULL) { diagnostic->invalid_library_output = 1; result = -1; goto cleanup; }
        if (resource_name->size != sizeof(calculated_name)
            || CRYPTO_memcmp(resource_name->name, calculated_name, sizeof(calculated_name)) != 0) goto cleanup;

        if (z12_nv_read_budget(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        /* L’authValue du bind est fixée AVANT la création de la session liée. */
        auth.size = 32;
        memcpy(auth.buffer, secret->value, 32);
        rc = Esys_TR_SetAuth(esys, nv_handle, &auth);
        explicit_bzero(&auth, sizeof(auth));
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; result = -1; goto cleanup; }
        nonce.size = 32;
        if (RAND_bytes_ex(libctx, nonce.buffer, 32, 256) != 1) {
            diagnostic->openssl_failed = 1; result = -1; goto cleanup;
        }
        symmetric.algorithm = TPM2_ALG_NULL;
        if (z12_nv_read_budget(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        rc = Esys_StartAuthSession_Async(esys, ESYS_TR_NONE, nv_handle,
            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &nonce,
            TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256);
        pending = 1;
        explicit_bzero(&nonce, sizeof(nonce));
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; diagnostic->must_destroy_context = 1; result = -1; goto cleanup; }
        if (z12_nv_read_finish(esys, Z12_NV_START_SESSION, deadline, diagnostic,
            &pending, &session, NULL, NULL, NULL) != 1) { result = -1; goto cleanup; }
        rc = Esys_TRSess_SetAttributes(esys, session,
            TPMA_SESSION_CONTINUESESSION, (TPMA_SESSION)0xff);
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; result = -1; goto cleanup; }
        if (z12_nv_read_budget(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        rc = Esys_NV_Read_Async(esys, nv_handle, nv_handle,
            session, ESYS_TR_NONE, ESYS_TR_NONE, 32, 0);
        pending = 1;
        if (rc != TSS2_RC_SUCCESS) { diagnostic->primary_tss_rc = rc; diagnostic->must_destroy_context = 1; result = -1; goto cleanup; }
        if (z12_nv_read_finish(esys, Z12_NV_READ_VALUE, deadline, diagnostic,
            &pending, NULL, NULL, NULL, &data) != 1) { result = -1; goto cleanup; }
        if (data == NULL) { diagnostic->invalid_library_output = 1; result = -1; goto cleanup; }
        if (z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) { result = -1; goto cleanup; }
        if (z12_nv_read_deadline(deadline, diagnostic, &final_remaining_ms) != 1) { result = -1; goto cleanup; }
        if (data->size != 32 || CRYPTO_memcmp(data->buffer, binding->expected_value, 32) != 0) goto cleanup;
        result = 1;

    cleanup:
        if (session != ESYS_TR_NONE) {
            if (!pending && !diagnostic->must_destroy_context
                && z12_nv_read_budget(esys, deadline, diagnostic) == 1) {
                rc = Esys_FlushContext_Async(esys, session);
                pending = 1;
                z12_nv_read_cleanup_result(rc, &result, diagnostic);
                if (rc == TSS2_RC_SUCCESS && z12_nv_read_finish(esys,
                    Z12_NV_FLUSH_SESSION, deadline, diagnostic, &pending,
                    NULL, NULL, NULL, NULL) == 1) {
                    session = ESYS_TR_NONE;
                } else {
                    diagnostic->must_destroy_context = 1;
                    result = -1;
                }
            } else {
                diagnostic->must_destroy_context = 1;
                result = -1;
            }
            session = ESYS_TR_NONE;
        }
        if (nv_handle != ESYS_TR_NONE && !pending && !diagnostic->must_destroy_context) {
            rc = Esys_TR_SetAuth(esys, nv_handle, &empty_auth);
            z12_nv_read_cleanup_result(rc, &result, diagnostic);
            rc = Esys_TR_Close(esys, &nv_handle);
            z12_nv_read_cleanup_result(rc, &result, diagnostic);
        }
        if (pending) { diagnostic->must_destroy_context = 1; result = -1; }
        /* Aucune autre commande ni manipulation ESYS après une attente incertaine.
           Les ressources et copies ESAPI restent attachées au contexte exclusif ;
           le propriétaire doit le détruire avec son TCTI avant toute autre activité. */
        if (diagnostic->transport_unusable) { diagnostic->must_destroy_context = 1; result = -1; }
        if (result == 1 && z12_nv_read_check_transport(esys, deadline, diagnostic) != 1) result = -1;
        if (result == 1 && z12_nv_read_deadline(deadline, diagnostic, &final_remaining_ms) != 1) result = -1;
        if (result < 0 || diagnostic->must_destroy_context) diagnostic->must_destroy_context = 1;
        Esys_Free(data);
        Esys_Free(resource_name);
        Esys_Free(nv_name);
        Esys_Free(nv_public);
        explicit_bzero(&nonce, sizeof(nonce));
        explicit_bzero(&auth, sizeof(auth));
        explicit_bzero(&empty_auth, sizeof(empty_auth));
        explicit_bzero(&symmetric, sizeof(symmetric));
        explicit_bzero(public_bytes, sizeof(public_bytes));
        explicit_bzero(public_digest, sizeof(public_digest));
        explicit_bzero(name_digest, sizeof(name_digest));
        explicit_bzero(calculated_name, sizeof(calculated_name));
        return result;
    }
    """
    ctypedef struct Z12NvReadBinding:
        uint32_t index
        unsigned char public_sha256[32]
        unsigned char name_sha256[32]
        unsigned char expected_value[32]

    ctypedef struct Z12NvReadDiagnostic:
        uint32_t primary_tss_rc
        uint32_t cleanup_tss_rc
        int openssl_failed
        int invalid_library_output
        int deadline_expired
        int clock_failed
        int clock_errno
        int must_destroy_context
        int transport_unusable

    int z12_nv_read_guard(
        ESYS_CONTEXT *esys, OSSL_LIB_CTX *libctx,
        const Z12NvReadBinding *binding, const Z12NvSecret *secret,
        Z12MonotonicDeadline *deadline, Z12NvReadDiagnostic *diagnostic
    )
