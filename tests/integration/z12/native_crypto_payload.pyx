# Programme de tests Z12 uniquement ; aucune admission, clé privée ou commande TPM.
# Compiler séparément avec le répertoire native/ dans le chemin des inclusions.
# Vecteur public et signature : RFC 8032 §7.1, TEST 1.
include "_operator_verify.pxi"
include "_operator_payload.pxi"
from libc.stdint cimport uintptr_t

cdef extern from "openssl/crypto.h" nogil:
    OSSL_LIB_CTX *OSSL_LIB_CTX_new()
    void OSSL_LIB_CTX_free(OSSL_LIB_CTX *context)

cdef extern from "openssl/provider.h" nogil:
    ctypedef struct OSSL_PROVIDER:
        pass
    OSSL_PROVIDER *OSSL_PROVIDER_load(OSSL_LIB_CTX *context, const char *name)
    int OSSL_PROVIDER_unload(OSSL_PROVIDER *provider)

def _expect(int actual, int expected, str name):
    if actual != expected:
        raise AssertionError(name)
    return 1

def _crypto_cases():
    cdef bytes public_key = bytes.fromhex(
        "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
    )
    cdef bytes signature = bytes.fromhex(
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    )
    cdef bytes altered_signature = signature[:32] + bytes([signature[32] ^ 1]) + signature[33:]
    cdef bytes altered_payload = b"x"
    cdef const unsigned char *key_ptr = <const unsigned char *>public_key
    cdef const unsigned char *signature_ptr = <const unsigned char *>signature
    cdef const unsigned char *altered_signature_ptr = <const unsigned char *>altered_signature
    cdef const unsigned char *altered_payload_ptr = <const unsigned char *>altered_payload
    cdef OSSL_LIB_CTX *context = NULL
    cdef OSSL_LIB_CTX *unavailable_context = NULL
    cdef OSSL_PROVIDER *provider = NULL
    cdef OSSL_PROVIDER *null_provider = NULL
    cdef int cases = 0
    cdef int cleanup_failed = 0
    if len(public_key) != 32 or len(signature) != 64:
        raise AssertionError("dimensions_vecteur_RFC")
    context = OSSL_LIB_CTX_new()
    if context == NULL:
        raise RuntimeError("allocation_contexte_test")
    try:
        provider = OSSL_PROVIDER_load(context, "default")
        if provider == NULL:
            raise RuntimeError("chargement_provider_test")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, signature_ptr, 64, NULL, 0), 1, "RFC8032_vide")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, altered_signature_ptr, 64, NULL, 0), 0, "signature_alteree")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, signature_ptr, 64, altered_payload_ptr, 1), 0, "payload_altere")
        cases += _expect(_ca_verify_ed25519(NULL, key_ptr, 32, signature_ptr, 64, NULL, 0), -2, "contexte_NULL")
        cases += _expect(_ca_verify_ed25519(context, NULL, 32, signature_ptr, 64, NULL, 0), -2, "cle_NULL")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, NULL, 64, NULL, 0), -2, "signature_NULL")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, signature_ptr, 64, NULL, 1), -2, "payload_NULL_non_vide")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 31, signature_ptr, 64, NULL, 0), -2, "cle_31")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 33, signature_ptr, 64, NULL, 0), -2, "cle_33")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, signature_ptr, 63, NULL, 0), -2, "signature_63")
        cases += _expect(_ca_verify_ed25519(context, key_ptr, 32, signature_ptr, 65, NULL, 0), -2, "signature_65")
        unavailable_context = OSSL_LIB_CTX_new()
        if unavailable_context == NULL:
            raise RuntimeError("allocation_contexte_provider_absent")
        null_provider = OSSL_PROVIDER_load(unavailable_context, "null")
        if null_provider == NULL:
            raise RuntimeError("chargement_provider_null_test")
        cases += _expect(_ca_verify_ed25519(unavailable_context, key_ptr, 32, signature_ptr, 64, NULL, 0), -1, "provider_indisponible")
    finally:
        if null_provider != NULL and OSSL_PROVIDER_unload(null_provider) != 1:
            cleanup_failed = 1
        if unavailable_context != NULL:
            OSSL_LIB_CTX_free(unavailable_context)
        if provider != NULL and OSSL_PROVIDER_unload(provider) != 1:
            cleanup_failed = 1
        OSSL_LIB_CTX_free(context)
    if cleanup_failed:
        raise RuntimeError("liberation_provider_test")
    return cases

def _public_fields():
    fields = [b"test-reference"] * 25
    fields[0] = b"z12.initial_operator_payload/v1"
    fields[1] = b"1.0.0"
    fields[2] = b"pixs.z12.initial.operator/v1"
    fields[5] = bytes(range(32))  # Nonce public de fixture, pas secret NV.
    for index in (9, 13, 17, 20):
        fields[index] = b"0" * 64
    fields[11] = b"prepare_initial_trust"
    fields[12] = b"1.0.0"
    fields[21] = b"0"
    fields[22] = b"2026-10-23T10:00:00.000000Z"
    fields[23] = b"2026-10-23T10:00:00.000000Z"
    fields[24] = b"2026-10-23T10:01:00.000000Z"
    return fields

def _encode_fields(fields):
    # Encodeur de fixture publique indépendant de la lecture native.
    return b"pixs.z12.initial.operator.payload/v1\x00" + b"".join(
        len(value).to_bytes(4, "big") + value for value in fields
    )

def _frame_case(bytes record, int expected, str name, size_t maximum, size_t field_maximum, expected_fields=None):
    cdef _OperatorFields output
    cdef const unsigned char *record_ptr = <const unsigned char *>record
    cdef int actual
    cdef size_t index
    cdef uintptr_t start = <uintptr_t>record_ptr
    cdef uintptr_t address
    cdef size_t field_offset
    cdef size_t record_length = len(record)
    memset(&output, 0x5a, sizeof(_OperatorFields))
    actual = _operator_frame_payload(record_ptr, len(record), maximum, field_maximum, &output)
    _expect(actual, expected, name)
    if expected != 1:
        for index in range(25):
            if output.fields[index].ptr != NULL or output.fields[index].length != 0:
                raise AssertionError("sortie_non_videe_" + name)
    elif expected_fields is not None:
        for index in range(25):
            address = <uintptr_t>output.fields[index].ptr
            if address < start:
                raise AssertionError("span_avant_buffer_" + name)
            field_offset = address - start
            if field_offset > record_length:
                raise AssertionError("span_apres_buffer_" + name)
            if output.fields[index].length > record_length - field_offset:
                raise AssertionError("span_hors_buffer_" + name)
            if (<const char *>output.fields[index].ptr)[:output.fields[index].length] != expected_fields[index]:
                raise AssertionError("span_incorrect_" + name)
    return 1

def _framing_cases():
    cdef _OperatorFields output
    cdef bytes record
    cdef const unsigned char *record_ptr
    cdef size_t index
    cdef int cases = 0
    fields = _public_fields()
    record = _encode_fields(fields)
    record_ptr = <const unsigned char *>record
    # Bornes EXPLICITES de fixture ; elles ne deviennent jamais une politique runtime.
    cases += _frame_case(record, 1, "cadrage_valide", 4096, 256, fields)
    for index in range(len(record)):
        cases += _frame_case(record[:index], 0, "troncature_" + str(index), 4096, 256)
    for index in range(25):
        empty = fields.copy()
        empty[index] = b""
        cases += _frame_case(_encode_fields(empty), 0, "champ_vide_" + str(index), 4096, 256)
    for index, value in ((0, b"z12.autre/v1"), (1, b"1.0.1"), (2, b"pixs.pg.initial.operator/v1"), (5, bytes(31)), (5, bytes(33))):
        changed = fields.copy()
        changed[index] = value
        cases += _frame_case(_encode_fields(changed), 0, "discriminateur_ou_nonce", 4096, 256)
    cases += _frame_case(b"X" + record[1:], 0, "prefixe_altere", 4096, 256)
    cases += _frame_case(record[:36] + b"X" + record[37:], 0, "NUL_prefixe_absent", 4096, 256)
    cases += _frame_case(record + b"x", 0, "octet_final", 4096, 256)
    cases += _frame_case(record + b"\x00\x00\x00\x01x", 0, "champ_supplementaire", 4096, 256)
    cases += _frame_case(b"pixs.z12.initial.operator.payload/v1\x00" + b"\xff" * 4 + b"x", 0, "longueur_u32_max", 4096, 4294967295)
    cases += _frame_case(record, 0, "payload_hors_borne", len(record) - 1, 256)
    cases += _frame_case(record, 0, "champ_hors_borne", 4096, 31)
    cases += _frame_case(record, -2, "borne_payload_nulle", 0, 256)
    cases += _frame_case(record, -2, "borne_champ_nulle", 4096, 0)
    memset(&output, 0x5a, sizeof(_OperatorFields))
    cases += _expect(_operator_frame_payload(NULL, 0, 4096, 256, &output), -2, "buffer_NULL")
    for index in range(25):
        if output.fields[index].ptr != NULL or output.fields[index].length != 0:
            raise AssertionError("sortie_non_videe_buffer_NULL")
    cases += _expect(_operator_frame_payload(record_ptr, len(record), 4096, 256, NULL), -2, "sortie_NULL")
    return cases

def main():
    import json
    if globals().get("__pyx_capi__"):
        raise AssertionError("CAPI_inattendue_dans_programme_test")
    result = {"crypto_cases": _crypto_cases(), "framing_cases": _framing_cases(),
              "qualification_proprietaire": False, "effet_TPM_NV": False}
    print(json.dumps(result, sort_keys=True))
    return result

if __name__ == "__main__":
    main()
