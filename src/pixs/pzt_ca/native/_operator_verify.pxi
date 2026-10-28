# Privé Z12 : vérification cryptographique Ed25519 pure, sans admission.
# Les buffers publics et le contexte empruntés restent valides pendant l’appel.
# Le propriétaire contrôle séparément politique, mandat, identité, temps et ancrage.

include "_openssl_ed25519.pxi"

cdef int _ca_verify_ed25519(
    OSSL_LIB_CTX *libctx,
    const unsigned char *public_key, size_t public_key_len,
    const unsigned char *signature, size_t signature_len,
    const unsigned char *payload, size_t payload_len
) noexcept nogil:
    # 1=valide, 0=invalide, -1=erreur OpenSSL, -2=arguments invalides.
    cdef EVP_PKEY *pkey = NULL
    cdef EVP_MD_CTX *mdctx = NULL
    cdef const unsigned char *message = payload
    cdef unsigned char empty_message = 0
    cdef int result

    if libctx == NULL or public_key == NULL or signature == NULL:
        return -2
    if public_key_len != 32 or signature_len != 64:
        return -2
    if payload == NULL and payload_len != 0:
        return -2
    if payload_len == 0:
        message = &empty_message

    pkey = EVP_PKEY_new_raw_public_key_ex(
        libctx, "ED25519", "provider=default", public_key, public_key_len
    )
    if pkey == NULL:
        return -1
    mdctx = EVP_MD_CTX_new()
    if mdctx == NULL:
        EVP_PKEY_free(pkey)
        return -1
    try:
        if EVP_DigestVerifyInit_ex(
            mdctx, NULL, NULL, libctx, "provider=default", pkey, NULL
        ) != 1:
            return -1
        result = EVP_DigestVerify(
            mdctx, signature, signature_len, message, payload_len
        )
        if result == 1:
            return 1
        if result == 0:
            return 0
        return -1
    finally:
        EVP_MD_CTX_free(mdctx)
        EVP_PKEY_free(pkey)
