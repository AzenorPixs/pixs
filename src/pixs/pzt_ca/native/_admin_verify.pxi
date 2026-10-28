# Prive Z12 : verification Ed25519 structurelle, sans admission.
# A inclure UNE fois APRES _monotonic_deadline, _admin_profile, _operator_verify, _admin_codec.
# LIBCTX emprunte non NULL du vrai proprietaire, tampons natifs immuables meme vie.
# Output distinct des tampons payload et signature, sans recouvrement.
from libc.stddef cimport size_t
from libc.stdint cimport int32_t
from libc.string cimport memcpy, memset

cdef int _admin_verify_signed(
    int kind,
    const unsigned char *payload, size_t payload_len,
    const unsigned char *signature, size_t signature_len,
    OSSL_LIB_CTX *libctx,
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms,
    _AdminFramed *output
) noexcept nogil:
    # 1=CRYPTOGRAPHIQUEMENT_VALIDE_CADRE, 0=format ou signature invalide.
    # -3=expire, -1=horloge, -4=erreur OpenSSL, -2=precondition native.
    cdef _AdminFramed parsed
    cdef Z12AdminView view
    cdef int live
    cdef int observed
    cdef int framed
    cdef int checked
    if output == NULL:
        return -2
    memset(output, 0, sizeof(_AdminFramed))
    memset(&parsed, 0, sizeof(_AdminFramed))
    memset(&view, 0, sizeof(Z12AdminView))
    if timeout_ms != NULL:
        timeout_ms[0] = 0
    if payload == NULL or signature == NULL:
        return -2
    if libctx == NULL or deadline == NULL or timeout_ms == NULL:
        return -2
    if kind != _ADMIN_KIND_PREPUBLICATION and kind != _ADMIN_KIND_PUBLICATION:
        if kind == _ADMIN_KIND_BINDING:
            return 0
        return -2
    if signature_len != 64:
        return 0
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    observed = _admin_profile_observe(&view)
    if observed != 1:
        return -2
    framed = _admin_frame_payload(
        kind, payload, payload_len, deadline, timeout_ms, &parsed
    )
    if framed != 1:
        return framed
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    checked = _ca_verify_ed25519(
        libctx, view.pubkey_ptr, 32,
        signature, signature_len,
        payload, payload_len
    )
    if checked == 1:
        pass
    elif checked == 0:
        return 0
    elif checked == -1:
        return -4
    else:
        return -2
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    memcpy(output, &parsed, sizeof(_AdminFramed))
    return 1
