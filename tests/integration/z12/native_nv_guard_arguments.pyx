# Compile toute la garde NV ; ne teste que les refus avant le premier appel ESAPI.
# Les sentinelles C ne sont pas des contextes : tout usage ESAPI serait une faute.
# Aucun TCTI n'est créé ; aucune preuve positive matérielle ou d'autorité.
include "../../../src/pixs/pzt_ca/native/_openssl_ed25519.pxi"
include "../../../src/pixs/pzt_ca/native/_nv_secret_fd.pxi"
include "../../../src/pixs/pzt_ca/native/_nv_read_guard.pxi"

cdef extern from * nogil:
    r"""
    #include <stddef.h>
    static int z12_test_guard_argument_case(int number) {
        max_align_t esys_sentinel;
        max_align_t openssl_sentinel;
        ESYS_CONTEXT *esys = (ESYS_CONTEXT *)&esys_sentinel;
        OSSL_LIB_CTX *libctx = (OSSL_LIB_CTX *)&openssl_sentinel;
        Z12NvReadBinding binding = {0};
        Z12NvSecret secret = {0};
        Z12MonotonicDeadline deadline = {0};
        Z12NvReadDiagnostic diagnostic;
        const Z12NvReadBinding *binding_arg = &binding;
        const Z12NvSecret *secret_arg = &secret;
        Z12MonotonicDeadline *deadline_arg = &deadline;
        Z12NvReadDiagnostic *diagnostic_arg = &diagnostic;
        unsigned char zero[sizeof(diagnostic)] = {0};
        int result;
        binding.index = UINT32_C(0x01000000);
        secret.loaded = 1;
        memset(secret.value, 0x5a, sizeof(secret.value));
        memset(&diagnostic, 0xa5, sizeof(diagnostic));
        switch (number) {
            case 0: diagnostic_arg = NULL; break;
            case 1: esys = NULL; break;
            case 2: libctx = NULL; break;
            case 3: binding_arg = NULL; break;
            case 4: secret_arg = NULL; break;
            case 5: deadline_arg = NULL; break;
            case 6: secret.loaded = 0; break;
            case 7: secret.loaded = 2; break;
            case 8: binding.index = 0; break;
            case 9: binding.index = UINT32_C(0x80000000); break;
            case 10: binding.index = UINT32_C(0x02000000); break;
            default: z12_nv_secret_destroy(&secret); return 999;
        }
        result = z12_nv_read_guard(esys, libctx, binding_arg, secret_arg, deadline_arg, diagnostic_arg);
        z12_nv_secret_destroy(&secret);
        if (result != -2) return 1;
        if (diagnostic_arg != NULL && memcmp(&diagnostic, zero, sizeof(diagnostic)) != 0) return 2;
        return 0;
    }
    """
    int z12_test_guard_argument_case(int number)


def run_tests():
    """Refus précoces uniquement ; toute ouverture TPM est exclue de ce programme."""
    cdef int number
    cdef int result
    names = (
        "diagnostic_nul", "esys_nul", "openssl_nul", "binding_nul", "secret_nul",
        "echeance_nulle", "secret_non_charge", "etat_secret_etranger", "index_nul",
        "index_objet_persistant", "index_session",
    )
    if globals().get("__pyx_capi__"):
        raise AssertionError("ABI publique Cython inattendue")
    for number in range(len(names)):
        with nogil:
            result = z12_test_guard_argument_case(number)
        if result != 0:
            raise AssertionError("Echec refus precoce NV : " + names[number] + "; code=" + str(result))
    return {"cas": len(names), "garde_positive_qualifiee": False, "effet_tpm_nv": False}


if __name__ == "__main__":
    import json
    print(json.dumps(run_tests(), sort_keys=True))
