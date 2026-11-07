# Tests du backend crypto privé ; aucun TPM, index NV ou secret d'installation.
# RFC4231 cas1 : données de test publiques conservées uniquement dans le code C.
include "../../../src/pixs/pzt_ca/native/_openssl_ed25519.pxi"
include "../../../src/pixs/pzt_ca/native/_esys_crypto.pxi"

cdef extern from * nogil:
    r"""
    #include <openssl/provider.h>
    static int z12_test_bytes_equal(const unsigned char *buffer, size_t count, unsigned char byte) {
        size_t index;
        for (index = 0; index < count; index++) if (buffer[index] != byte) return 0;
        return 1;
    }
    static int z12_test_esys_crypto_case(int number) {
        OSSL_LIB_CTX *libctx = NULL;
        OSSL_LIB_CTX *foreign = NULL;
        OSSL_PROVIDER *provider = NULL;
        OSSL_PROVIDER *null_provider = NULL;
        ESYS_CRYPTO_CONTEXT_BLOB *blob = NULL;
        ESYS_CRYPTO_CONTEXT_BLOB *saved = NULL;
        TPM2B_NONCE nonce;
        unsigned char output[64];
        unsigned char key[20];
        static const unsigned char message[] = "Hi There";
        static const unsigned char expected[32] = {
            0xb0,0x34,0x4c,0x61,0xd8,0xdb,0x38,0x53,0x5c,0xa8,0xaf,0xce,0xaf,0x0b,0xf1,0x2b,
            0x88,0x1d,0xc2,0x00,0xc9,0x83,0x3d,0xa7,0x26,0xe9,0x37,0x6c,0x2e,0x32,0xcf,0xf7
        };
        static const unsigned char sha_abc[32] = {
            0xba,0x78,0x16,0xbf,0x8f,0x01,0xcf,0xea,0x41,0x41,0x40,0xde,0x5d,0xae,0x22,0x23,
            0xb0,0x03,0x61,0xa3,0x96,0x17,0x7a,0x9c,0xb4,0x10,0xff,0x61,0xf2,0x00,0x15,0xad
        };
        size_t size = sizeof(output);
        TSS2_RC rc;
        int result = 1000;
        memset(key, 0x0b, sizeof(key));
        memset(output, 0xa5, sizeof(output));
        memset(&nonce, 0xa5, sizeof(nonce));
        libctx = OSSL_LIB_CTX_new();
        foreign = OSSL_LIB_CTX_new();
        if (libctx == NULL || foreign == NULL) goto cleanup;
        provider = OSSL_PROVIDER_load(libctx, "default");
        null_provider = OSSL_PROVIDER_load(foreign, "null");
        if (provider == NULL || null_provider == NULL) goto cleanup;
        result = 1;
        switch (number) {
        case 0:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            if (z12_esys_hash_update(blob, (const uint8_t *)"a", 1, libctx) != TSS2_RC_SUCCESS
                || z12_esys_hash_update(blob, NULL, 0, libctx) != TSS2_RC_SUCCESS
                || z12_esys_hash_update(blob, (const uint8_t *)"bc", 2, libctx) != TSS2_RC_SUCCESS) break;
            rc = z12_esys_hash_finish(&blob, output, &size, libctx);
            result = !(rc == TSS2_RC_SUCCESS && size == 32 && blob == NULL
                && CRYPTO_memcmp(output, sha_abc, 32) == 0
                && z12_test_bytes_equal(output + 32, 32, 0xa5));
            break;
        case 1:
            if (z12_esys_hmac_start(&blob, TPM2_ALG_SHA256, key, sizeof(key), libctx) != TSS2_RC_SUCCESS) break;
            if (z12_esys_hmac_update(blob, message, 3, libctx) != TSS2_RC_SUCCESS
                || z12_esys_hmac_update(blob, NULL, 0, libctx) != TSS2_RC_SUCCESS
                || z12_esys_hmac_update(blob, message + 3, sizeof(message) - 4, libctx) != TSS2_RC_SUCCESS) break;
            rc = z12_esys_hmac_finish(&blob, output, &size, libctx);
            result = !(rc == TSS2_RC_SUCCESS && size == 32 && blob == NULL
                && CRYPTO_memcmp(output, expected, 32) == 0
                && z12_test_bytes_equal(output + 32, 32, 0xa5));
            break;
        case 2:
            result = !(z12_esys_hash_start(&blob, TPM2_ALG_SHA1, libctx) == TSS2_ESYS_RC_NOT_IMPLEMENTED && blob == NULL);
            break;
        case 3:
            result = !(z12_esys_hmac_start(&blob, TPM2_ALG_SHA384, key, sizeof(key), libctx) == TSS2_ESYS_RC_NOT_IMPLEMENTED && blob == NULL);
            break;
        case 4:
            result = !(z12_esys_hmac_start(&blob, TPM2_ALG_SHA256, NULL, 1, libctx) == TSS2_ESYS_RC_BAD_REFERENCE && blob == NULL);
            break;
        case 5:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            size = 31;
            rc = z12_esys_hash_finish(&blob, output, &size, libctx);
            result = !(rc == TSS2_ESYS_RC_BAD_SIZE && blob == NULL && size == 0
                && z12_test_bytes_equal(output, sizeof(output), 0xa5));
            break;
        case 6:
            if (z12_esys_hmac_start(&blob, TPM2_ALG_SHA256, key, sizeof(key), libctx) != TSS2_RC_SUCCESS) break;
            size = 31;
            rc = z12_esys_hmac_finish(&blob, output, &size, libctx);
            result = !(rc == TSS2_ESYS_RC_BAD_SIZE && blob == NULL && size == 0
                && z12_test_bytes_equal(output, sizeof(output), 0xa5));
            break;
        case 7:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            rc = z12_esys_hash_finish(&blob, output, &size, foreign);
            result = !(rc == TSS2_ESYS_RC_BAD_REFERENCE && blob == NULL && size == 0
                && z12_test_bytes_equal(output, 32, 0) && z12_test_bytes_equal(output + 32, 32, 0xa5));
            break;
        case 8:
            if (z12_esys_hmac_start(&blob, TPM2_ALG_SHA256, key, sizeof(key), libctx) != TSS2_RC_SUCCESS) break;
            rc = z12_esys_hmac_finish(&blob, output, &size, foreign);
            result = !(rc == TSS2_ESYS_RC_BAD_REFERENCE && blob == NULL && size == 0
                && z12_test_bytes_equal(output, 32, 0) && z12_test_bytes_equal(output + 32, 32, 0xa5));
            break;
        case 9:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            result = !(z12_esys_hash_update(blob, NULL, 1, libctx) == TSS2_ESYS_RC_BAD_REFERENCE);
            break;
        case 10:
            if (z12_esys_hmac_start(&blob, TPM2_ALG_SHA256, key, sizeof(key), libctx) != TSS2_RC_SUCCESS) break;
            result = !(z12_esys_hmac_update(blob, NULL, 1, libctx) == TSS2_ESYS_RC_BAD_REFERENCE);
            break;
        case 11:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            saved = blob;
            rc = z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx);
            result = !(rc == TSS2_ESYS_RC_BAD_SEQUENCE && blob == saved);
            break;
        case 12:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            rc = z12_esys_hmac_finish(&blob, output, &size, libctx);
            result = !(rc == TSS2_ESYS_RC_BAD_REFERENCE && blob == NULL && size == 0
                && z12_test_bytes_equal(output, 32, 0));
            break;
        case 13:
            result = !(z12_esys_hash_start(&blob, TPM2_ALG_SHA256, foreign) == TSS2_ESYS_RC_GENERAL_FAILURE && blob == NULL);
            break;
        case 14:
            result = !(z12_esys_hmac_start(&blob, TPM2_ALG_SHA256, key, sizeof(key), foreign) == TSS2_ESYS_RC_GENERAL_FAILURE && blob == NULL);
            break;
        case 15:
            rc = z12_esys_random(&nonce, 0, libctx);
            result = !(rc == TSS2_ESYS_RC_BAD_SIZE && z12_test_bytes_equal((const unsigned char *)&nonce, sizeof(nonce), 0));
            break;
        case 16:
            rc = z12_esys_random(&nonce, sizeof(nonce.buffer) + 1, libctx);
            result = !(rc == TSS2_ESYS_RC_BAD_SIZE && z12_test_bytes_equal((const unsigned char *)&nonce, sizeof(nonce), 0));
            break;
        case 17:
            rc = z12_esys_random(&nonce, 32, NULL);
            result = !(rc == TSS2_ESYS_RC_BAD_REFERENCE && z12_test_bytes_equal((const unsigned char *)&nonce, sizeof(nonce), 0));
            break;
        case 18:
            rc = z12_esys_random(&nonce, 32, foreign);
            result = !(rc == TSS2_ESYS_RC_GENERAL_FAILURE && z12_test_bytes_equal((const unsigned char *)&nonce, sizeof(nonce), 0));
            break;
        case 19:
            rc = z12_esys_random(&nonce, 32, libctx);
            result = !(rc == TSS2_RC_SUCCESS && nonce.size == 32
                && z12_test_bytes_equal(nonce.buffer + 32, sizeof(nonce.buffer) - 32, 0));
            break;
        case 20:
            size = 99;
            rc = z12_esys_rsa_refuse(NULL, 0, NULL, 0, NULL, &size, NULL, libctx);
            result = !(rc == TSS2_ESYS_RC_NOT_IMPLEMENTED && size == 0);
            break;
        case 21:
            size = 99;
            rc = z12_esys_ecdh_refuse(NULL, 0, NULL, NULL, NULL, &size, libctx);
            result = !(rc == TSS2_ESYS_RC_NOT_IMPLEMENTED && size == 0);
            break;
        case 22:
            result = !(z12_esys_cipher_refuse(NULL, TPM2_ALG_AES, 128, TPM2_ALG_CFB,
                output, sizeof(output), NULL, libctx) == TSS2_ESYS_RC_NOT_IMPLEMENTED
                && z12_test_bytes_equal(output, sizeof(output), 0xa5));
            break;
        case 23:
            result = !(z12_esys_crypto_install(NULL, libctx) == TSS2_ESYS_RC_BAD_REFERENCE
                && z12_esys_crypto_install(NULL, NULL) == TSS2_ESYS_RC_BAD_REFERENCE);
            break;
        case 24:
            if (z12_esys_hash_start(&blob, TPM2_ALG_SHA256, libctx) != TSS2_RC_SUCCESS) break;
            z12_esys_crypto_abort(&blob, libctx);
            z12_esys_crypto_abort(&blob, libctx);
            z12_esys_crypto_abort(NULL, libctx);
            result = blob != NULL;
            break;
        default:
            result = 999;
        }
    cleanup:
        z12_esys_crypto_abort(&blob, libctx);
        OPENSSL_cleanse(key, sizeof(key));
        OPENSSL_cleanse(output, sizeof(output));
        OPENSSL_cleanse(&nonce, sizeof(nonce));
        if (null_provider != NULL && OSSL_PROVIDER_unload(null_provider) != 1) result = 1001;
        if (provider != NULL && OSSL_PROVIDER_unload(provider) != 1) result = 1002;
        OSSL_LIB_CTX_free(foreign);
        OSSL_LIB_CTX_free(libctx);
        return result;
    }
    """
    int z12_test_esys_crypto_case(int number)


def run_tests():
    """Vecteurs et refus du backend uniquement ; aucune qualification du propriétaire."""
    cdef int number
    cdef int result
    names = (
        "sha256_abc_fragmente", "hmac_rfc4231_cas1_fragmente",
        "sha1_refuse", "hmac_sha384_refuse", "cle_nulle_non_vide_refusee",
        "hash_sortie_courte", "hmac_sortie_courte", "hash_contexte_etranger",
        "hmac_contexte_etranger", "hash_entree_nulle_non_vide", "hmac_entree_nulle_non_vide",
        "debut_sur_contexte_vivant", "finish_mauvais_type", "hash_sans_fournisseur",
        "hmac_sans_fournisseur", "rng_taille_nulle", "rng_taille_excessive",
        "rng_contexte_nul", "rng_sans_fournisseur", "rng_taille_exacte",
        "rsa_refuse", "ecdh_refuse", "chiffrement_refuse", "installation_contexte_nul",
        "abandon_idempotent",
    )
    if globals().get("__pyx_capi__"):
        raise AssertionError("ABI publique Cython inattendue")
    for number in range(len(names)):
        with nogil:
            result = z12_test_esys_crypto_case(number)
        if result != 0:
            raise AssertionError("Echec backend ESAPI : " + names[number] + "; code=" + str(result))
    return {"cas": len(names), "proprietaire_qualifie": False, "effet_tpm_nv": False}


if __name__ == "__main__":
    import json
    print(json.dumps(run_tests(), sort_keys=True))
