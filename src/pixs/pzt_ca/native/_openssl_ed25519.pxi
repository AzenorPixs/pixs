from libc.stddef cimport size_t

# Privé Z12. Déclarations OpenSSL3 minimales pour vérification Ed25519 pure.
# Aucune définition Python, aucune API exportée.

cdef extern from "openssl/evp.h" nogil:
    ctypedef struct OSSL_LIB_CTX:
        pass
    ctypedef struct EVP_PKEY:
        pass
    ctypedef struct EVP_MD_CTX:
        pass
    ctypedef struct EVP_PKEY_CTX:
        pass
    ctypedef struct OSSL_PARAM:
        pass

    EVP_PKEY *EVP_PKEY_new_raw_public_key_ex(
        OSSL_LIB_CTX *libctx,
        const char *keytype,
        const char *propq,
        const unsigned char *key,
        size_t keylen)

    void EVP_PKEY_free(EVP_PKEY *pkey)

    EVP_MD_CTX *EVP_MD_CTX_new()
    void EVP_MD_CTX_free(EVP_MD_CTX *ctx)

    int EVP_DigestVerifyInit_ex(
        EVP_MD_CTX *ctx,
        EVP_PKEY_CTX **pctx,
        const char *mdname,
        OSSL_LIB_CTX *libctx,
        const char *propq,
        EVP_PKEY *pkey,
        const OSSL_PARAM params[])

    int EVP_DigestVerify(
        EVP_MD_CTX *ctx,
        const unsigned char *sig,
        size_t siglen,
        const unsigned char *tbs,
        size_t tbslen)
