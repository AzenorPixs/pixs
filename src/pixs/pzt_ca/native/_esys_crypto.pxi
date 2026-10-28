# Privé Z12 : backend ESAPI SHA-256/HMAC/RNG dans le contexte OpenSSL fourni.
# Inclure après _openssl_ed25519.pxi. Aucun secret ou pointeur exposé à Python.
# Installation effective par API publique avant toute session ou authValue.
# Le contexte est neuf/exclusif, construit par le propriétaire natif.
# Le succès du setter ne prouve pas la provenance ni une exclusivité durable.
# Cela ne prouve ni l'autorité du propriétaire ni la fermeture des traces TSS2.
cdef extern from "tss2/tss2_esys.h" nogil:
    ctypedef struct ESYS_CONTEXT:
        pass

cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <string.h>
    #include <tss2/tss2_esys.h>
    #include <openssl/crypto.h>
    #include <openssl/evp.h>
    #include <openssl/core_names.h>
    #include <openssl/params.h>
    #include <openssl/rand.h>

    typedef struct {
        unsigned int kind;
        OSSL_LIB_CTX *owner;
        EVP_MD *digest;
        EVP_MD_CTX *hash;
        EVP_MAC *algorithm;
        EVP_MAC_CTX *hmac;
    } Z12EsysCryptoBlob;

    static void z12_esys_crypto_abort(ESYS_CRYPTO_CONTEXT_BLOB **opaque, void *userdata) {
        Z12EsysCryptoBlob *blob;
        (void)userdata;
        if (opaque == NULL || *opaque == NULL) return;
        blob = (Z12EsysCryptoBlob *)*opaque;
        *opaque = NULL;
        EVP_MD_CTX_free(blob->hash);
        EVP_MD_free(blob->digest);
        EVP_MAC_CTX_free(blob->hmac);
        EVP_MAC_free(blob->algorithm);
        OPENSSL_clear_free(blob, sizeof(*blob));
    }

    static TSS2_RC z12_esys_hash_start(ESYS_CRYPTO_CONTEXT_BLOB **opaque,
                                      TPM2_ALG_ID algorithm, void *userdata) {
        Z12EsysCryptoBlob *blob;
        if (opaque == NULL || userdata == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
        if (*opaque != NULL) return TSS2_ESYS_RC_BAD_SEQUENCE;
        if (algorithm != TPM2_ALG_SHA256) return TSS2_ESYS_RC_NOT_IMPLEMENTED;
        blob = OPENSSL_zalloc(sizeof(*blob));
        if (blob == NULL) return TSS2_ESYS_RC_MEMORY;
        blob->kind = 1;
        blob->owner = (OSSL_LIB_CTX *)userdata;
        *opaque = (ESYS_CRYPTO_CONTEXT_BLOB *)blob;
        blob->digest = EVP_MD_fetch(blob->owner, "SHA256", "provider=default");
        blob->hash = EVP_MD_CTX_new();
        if (blob->digest == NULL || blob->hash == NULL
            || EVP_DigestInit_ex2(blob->hash, blob->digest, NULL) != 1) {
            z12_esys_crypto_abort(opaque, userdata);
            return TSS2_ESYS_RC_GENERAL_FAILURE;
        }
        return TSS2_RC_SUCCESS;
    }

    static TSS2_RC z12_esys_hmac_start(ESYS_CRYPTO_CONTEXT_BLOB **opaque,
        TPM2_ALG_ID algorithm, const uint8_t *key, size_t key_size, void *userdata) {
        Z12EsysCryptoBlob *blob;
        unsigned char empty = 0;
        char digest_name[] = "SHA256";
        char properties[] = "provider=default";
        OSSL_PARAM parameters[3];
        if (opaque == NULL || userdata == NULL || (key == NULL && key_size != 0))
            return TSS2_ESYS_RC_BAD_REFERENCE;
        if (*opaque != NULL) return TSS2_ESYS_RC_BAD_SEQUENCE;
        if (algorithm != TPM2_ALG_SHA256) return TSS2_ESYS_RC_NOT_IMPLEMENTED;
        blob = OPENSSL_zalloc(sizeof(*blob));
        if (blob == NULL) return TSS2_ESYS_RC_MEMORY;
        blob->kind = 2;
        blob->owner = (OSSL_LIB_CTX *)userdata;
        *opaque = (ESYS_CRYPTO_CONTEXT_BLOB *)blob;
        blob->algorithm = EVP_MAC_fetch(blob->owner, "HMAC", "provider=default");
        if (blob->algorithm != NULL) blob->hmac = EVP_MAC_CTX_new(blob->algorithm);
        parameters[0] = OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_DIGEST, digest_name, 0);
        parameters[1] = OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_PROPERTIES, properties, 0);
        parameters[2] = OSSL_PARAM_construct_end();
        if (blob->hmac == NULL || EVP_MAC_init(blob->hmac,
            key == NULL ? &empty : key, key_size, parameters) != 1) {
            z12_esys_crypto_abort(opaque, userdata);
            return TSS2_ESYS_RC_GENERAL_FAILURE;
        }
        return TSS2_RC_SUCCESS;
    }

    static TSS2_RC z12_esys_hash_update(ESYS_CRYPTO_CONTEXT_BLOB *opaque,
        const uint8_t *buffer, size_t size, void *userdata) {
        Z12EsysCryptoBlob *blob = (Z12EsysCryptoBlob *)opaque;
        if (blob == NULL || userdata == NULL || blob->owner != userdata
            || blob->kind != 1 || blob->hash == NULL || (buffer == NULL && size != 0))
            return TSS2_ESYS_RC_BAD_REFERENCE;
        if (size == 0) return TSS2_RC_SUCCESS;
        return EVP_DigestUpdate(blob->hash, buffer, size) == 1
            ? TSS2_RC_SUCCESS : TSS2_ESYS_RC_GENERAL_FAILURE;
    }

    static TSS2_RC z12_esys_hmac_update(ESYS_CRYPTO_CONTEXT_BLOB *opaque,
        const uint8_t *buffer, size_t size, void *userdata) {
        Z12EsysCryptoBlob *blob = (Z12EsysCryptoBlob *)opaque;
        if (blob == NULL || userdata == NULL || blob->owner != userdata
            || blob->kind != 2 || blob->hmac == NULL || (buffer == NULL && size != 0))
            return TSS2_ESYS_RC_BAD_REFERENCE;
        if (size == 0) return TSS2_RC_SUCCESS;
        return EVP_MAC_update(blob->hmac, buffer, size) == 1
            ? TSS2_RC_SUCCESS : TSS2_ESYS_RC_GENERAL_FAILURE;
    }

    static TSS2_RC z12_esys_crypto_finish(ESYS_CRYPTO_CONTEXT_BLOB **opaque,
        uint8_t *buffer, size_t *size, void *userdata, unsigned int expected_kind) {
        Z12EsysCryptoBlob *blob;
        size_t capacity = size == NULL ? 0 : *size;
        unsigned int hash_size = 0;
        size_t hmac_size = 0;
        TSS2_RC result = TSS2_ESYS_RC_BAD_REFERENCE;
        if (size != NULL) *size = 0;
        if (opaque == NULL || *opaque == NULL) return result;
        blob = (Z12EsysCryptoBlob *)*opaque;
        if (buffer == NULL || size == NULL || userdata == NULL
            || blob->owner != userdata || blob->kind != expected_kind) goto cleanup;
        if (capacity < 32) { result = TSS2_ESYS_RC_BAD_SIZE; goto cleanup; }
        result = TSS2_ESYS_RC_GENERAL_FAILURE;
        if (expected_kind == 1) {
            if (blob->hash == NULL || EVP_DigestFinal_ex(blob->hash, buffer, &hash_size) != 1
                || hash_size != 32) goto cleanup;
        } else {
            if (blob->hmac == NULL || EVP_MAC_final(blob->hmac, buffer, &hmac_size, 32) != 1
                || hmac_size != 32) goto cleanup;
        }
        *size = 32;
        result = TSS2_RC_SUCCESS;
    cleanup:
        if (result != TSS2_RC_SUCCESS && buffer != NULL && capacity >= 32)
            OPENSSL_cleanse(buffer, 32);
        z12_esys_crypto_abort(opaque, userdata);
        return result;
    }

    static TSS2_RC z12_esys_hash_finish(ESYS_CRYPTO_CONTEXT_BLOB **opaque,
        uint8_t *buffer, size_t *size, void *userdata) {
        return z12_esys_crypto_finish(opaque, buffer, size, userdata, 1);
    }
    static TSS2_RC z12_esys_hmac_finish(ESYS_CRYPTO_CONTEXT_BLOB **opaque,
        uint8_t *buffer, size_t *size, void *userdata) {
        return z12_esys_crypto_finish(opaque, buffer, size, userdata, 2);
    }
    static TSS2_RC z12_esys_random(TPM2B_NONCE *nonce, size_t count, void *userdata) {
        if (nonce == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
        OPENSSL_cleanse(nonce, sizeof(*nonce));
        if (userdata == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
        if (count == 0 || count > sizeof(nonce->buffer)) return TSS2_ESYS_RC_BAD_SIZE;
        if (RAND_bytes_ex((OSSL_LIB_CTX *)userdata, nonce->buffer, count, 256) != 1) {
            OPENSSL_cleanse(nonce, sizeof(*nonce));
            return TSS2_ESYS_RC_GENERAL_FAILURE;
        }
        nonce->size = (UINT16)count;
        return TSS2_RC_SUCCESS;
    }

    /* Le profil NV utilise une session HMAC liée sans sel ni chiffrement des paramètres.
       Toutes les autres fonctions sont présentes et refusent, sans backend de repli. */
    static TSS2_RC z12_esys_rsa_refuse(TPM2B_PUBLIC *key, size_t input_size,
        BYTE *input, size_t capacity, BYTE *output, size_t *output_size,
        const char *label, void *userdata) {
        (void)key; (void)input_size; (void)input; (void)capacity;
        (void)output; (void)label; (void)userdata;
        if (output_size != NULL) *output_size = 0;
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;
    }
    static TSS2_RC z12_esys_ecdh_refuse(TPM2B_PUBLIC *key, size_t capacity,
        TPM2B_ECC_PARAMETER *secret, TPMS_ECC_POINT *point,
        BYTE *output, size_t *output_size, void *userdata) {
        (void)key; (void)capacity; (void)output; (void)userdata;
        if (secret != NULL) OPENSSL_cleanse(secret, sizeof(*secret));
        if (point != NULL) OPENSSL_cleanse(point, sizeof(*point));
        if (output_size != NULL) *output_size = 0;
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;
    }
    static TSS2_RC z12_esys_cipher_refuse(uint8_t *key, TPM2_ALG_ID algorithm,
        TPMI_AES_KEY_BITS bits, TPM2_ALG_ID mode, uint8_t *buffer,
        size_t size, uint8_t *iv, void *userdata) {
        (void)key; (void)algorithm; (void)bits; (void)mode;
        (void)buffer; (void)size; (void)iv; (void)userdata;
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;
    }
    static TSS2_RC z12_esys_crypto_init(void *userdata) {
        return userdata == NULL ? TSS2_ESYS_RC_BAD_REFERENCE : TSS2_RC_SUCCESS;
    }
    static void z12_esys_crypto_table(ESYS_CRYPTO_CALLBACKS *table, OSSL_LIB_CTX *libctx) {
        memset(table, 0, sizeof(*table));
        table->rsa_pk_encrypt = z12_esys_rsa_refuse;
        table->hash_start = z12_esys_hash_start;
        table->hash_update = z12_esys_hash_update;
        table->hash_finish = z12_esys_hash_finish;
        table->hash_abort = z12_esys_crypto_abort;
        table->hmac_start = z12_esys_hmac_start;
        table->hmac_update = z12_esys_hmac_update;
        table->hmac_finish = z12_esys_hmac_finish;
        table->hmac_abort = z12_esys_crypto_abort;
        table->get_random2b = z12_esys_random;
        table->get_ecdh_point = z12_esys_ecdh_refuse;
        table->aes_encrypt = z12_esys_cipher_refuse;
        table->aes_decrypt = z12_esys_cipher_refuse;
        table->sm4_encrypt = z12_esys_cipher_refuse;
        table->sm4_decrypt = z12_esys_cipher_refuse;
        table->init = z12_esys_crypto_init;
        table->userdata = libctx;
    }
    static TSS2_RC z12_esys_crypto_install(ESYS_CONTEXT *esys, OSSL_LIB_CTX *libctx) {
        ESYS_CRYPTO_CALLBACKS callbacks = {0};
        TSS2_RC result;
        if (esys == NULL || libctx == NULL) return TSS2_ESYS_RC_BAD_REFERENCE;
        z12_esys_crypto_table(&callbacks, libctx);
        result = Esys_SetCryptoCallbacks(esys, &callbacks);
        if (result != TSS2_RC_SUCCESS) return result;
        return TSS2_RC_SUCCESS;
    }
    """
    unsigned int z12_esys_crypto_install(ESYS_CONTEXT *esys, OSSL_LIB_CTX *libctx)
