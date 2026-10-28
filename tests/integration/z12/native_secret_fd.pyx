# Tests Z12 uniquement : fixtures de secrets produites et détruites en C.
# Aucun secret ne passe par Python, argv, environnement, journal ou fichier nommé.
# Aucune commande TPM/NV ; ce programme ne qualifie pas la provenance du lanceur.
# Construction Linux : le compilateur doit recevoir -D_GNU_SOURCE.
include "_nv_secret_fd.pxi"

cdef extern from * nogil:
    r"""
    #ifndef _GNU_SOURCE
    #error "Construire les tests FD avec -D_GNU_SOURCE"
    #endif
    #include <errno.h>
    #include <fcntl.h>
    #include <stdio.h>
    #include <string.h>
    #include <sys/mman.h>
    #include <sys/random.h>
    #include <sys/stat.h>
    #include <sys/types.h>
    #include <unistd.h>

    static int z12_test_nv_zero(const Z12NvSecret *secret) {
        size_t i;
        if (secret->loaded != 0) return 0;
        for (i = 0; i < sizeof(secret->value); i++)
            if (secret->value[i] != 0) return 0;
        return 1;
    }

    static int z12_test_nv_fd_case(int variant) {
        unsigned char fixture[33] = {0};
        Z12NvSecret received;
        char descriptor_path[64] = {0};
        int writer = -1, reader = -1, consumed = -1;
        int result = -1, actual, expected = 0;
        int descriptor_status, descriptor_errno;
        int path_size;
        int flags, seals;
        size_t have = 0, written = 0, wanted = 32;
        ssize_t amount;
        uid_t expected_uid = geteuid();
        gid_t expected_gid = getegid();
        mode_t expected_mode = 0400;
        mode_t fixture_mode = 0400;
        memset(&received, 0xa5, sizeof(received));
        received.loaded = 1;
        if (variant < 0 || variant > 16) goto cleanup;
        if (variant == 13) {
            actual = z12_nv_secret_load_fd(-1, expected_uid, expected_gid, 0400, &received);
            result = actual == -2 && z12_test_nv_zero(&received);
            goto cleanup;
        }
        if (variant == 16) {
            reader = open("/dev/null", O_RDONLY | O_CLOEXEC);
            if (reader < 0) goto cleanup;
            goto invoke;
        }
        /* Entropie indisponible : recette indisponible, sans repli ni attente infinie. */
        while (have < sizeof(fixture)) {
            amount = getrandom(fixture + have, sizeof(fixture) - have, GRND_NONBLOCK);
            if (amount <= 0 || (size_t)amount > sizeof(fixture) - have) goto cleanup;
            have += (size_t)amount;
        }
        writer = memfd_create("z12-test-fixture", MFD_CLOEXEC | MFD_ALLOW_SEALING);
        if (writer < 0) goto cleanup;
        if (variant == 7) wanted = 31;
        if (variant == 8) wanted = 33;
        while (written < wanted) {
            amount = write(writer, fixture + written, wanted - written);
            if (amount <= 0 || (size_t)amount > wanted - written) goto cleanup;
            written += (size_t)amount;
        }
        if (variant == 9) fixture_mode = 0600;
        if (fchmod(writer, fixture_mode) != 0) goto cleanup;
        seals = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL;
        if (variant == 1) seals &= ~F_SEAL_WRITE;
        if (variant == 2) seals &= ~F_SEAL_GROW;
        if (variant == 3) seals &= ~F_SEAL_SHRINK;
        if (variant == 4) seals &= ~F_SEAL_SEAL;
        if (fcntl(writer, F_ADD_SEALS, seals) != 0) goto cleanup;
        if (variant == 5) {
            reader = writer;
            writer = -1;
        } else {
            path_size = snprintf(descriptor_path, sizeof(descriptor_path), "/proc/self/fd/%d", writer);
            if (path_size < 0 || (size_t)path_size >= sizeof(descriptor_path)) goto cleanup;
            flags = O_RDONLY | O_CLOEXEC;
            if (variant == 6) flags &= ~O_CLOEXEC;
            reader = open(descriptor_path, flags);
            if (reader < 0) goto cleanup;
            actual = close(writer);
            writer = -1;
            if (actual != 0) goto cleanup;
        }
        if (variant == 10) expected_uid = expected_uid == 0 ? 1 : 0;
        if (variant == 11) expected_gid = expected_gid == 0 ? 1 : 0;
        if (variant == 12) { expected_mode = 0600; expected = -2; }
        if (variant == 14) expected = -2;
        if (variant == 15) {
            actual = close(reader);
            consumed = reader;
            reader = -1;
            if (actual != 0) goto cleanup;
            /* Aucun appel allouant un FD entre close et cette invocation privée. */
            errno = 0;
            actual = z12_nv_secret_load_fd(consumed, expected_uid, expected_gid, 0400, &received);
            result = actual == -1 && errno == EBADF && z12_test_nv_zero(&received);
            consumed = -1;
            goto cleanup;
        }
        if (variant == 0) expected = 1;
    invoke:
        consumed = reader;
        reader = -1;
        if (variant == 14)
            actual = z12_nv_secret_load_fd(consumed, expected_uid, expected_gid, expected_mode, NULL);
        else
            actual = z12_nv_secret_load_fd(consumed, expected_uid, expected_gid, expected_mode, &received);
        /* Le FD est transféré : le test ne le referme pas après consommation. */
        errno = 0;
        descriptor_status = fcntl(consumed, F_GETFD);
        descriptor_errno = errno;
        if (descriptor_status >= 0) {
            /* Si la primitive fuit le FD, l’échec du test reste nettoyé. */
            reader = consumed;
            result = 0;
            goto cleanup;
        }
        consumed = -1;
        if (descriptor_errno != EBADF || actual != expected) { result = 0; goto cleanup; }
        if (variant == 0) {
            if (received.loaded != 1 || memcmp(received.value, fixture, 32) != 0) { result = 0; goto cleanup; }
            z12_nv_secret_destroy(&received);
            result = z12_test_nv_zero(&received);
            z12_nv_secret_destroy(&received);
            if (!z12_test_nv_zero(&received)) result = 0;
        } else if (variant == 14) {
            result = 1; /* Sortie NULL : seule la consommation du FD est vérifiée. */
        } else {
            result = z12_test_nv_zero(&received);
        }
    cleanup:
        if (writer >= 0) {
            actual = close(writer);
            writer = -1;
            if (actual != 0) result = -1;
        }
        if (reader >= 0) {
            actual = close(reader);
            reader = -1;
            if (actual != 0) result = -1;
        }
        z12_nv_secret_destroy(&received);
        explicit_bzero(fixture, sizeof(fixture));
        explicit_bzero(descriptor_path, sizeof(descriptor_path));
        return result;
    }
    """
    int z12_test_nv_fd_case(int variant)

def main():
    import json
    cdef int variant
    cdef int actual
    cdef int passed = 0
    labels = (
        "valide", "sans_seal_write", "sans_seal_grow", "sans_seal_shrink",
        "sans_seal_seal", "descripteur_ecriture", "sans_cloexec", "taille31",
        "taille33", "mode0600", "uid_etranger", "gid_etranger",
        "mode_attendu_inadmissible", "fd_negatif", "sortie_NULL",
        "fd_deja_ferme", "type_non_regulier",
    )
    if globals().get("__pyx_capi__"):
        raise AssertionError("CAPI_inattendue_dans_programme_test")
    for variant in range(17):
        actual = z12_test_nv_fd_case(variant)
        if actual < 0:
            raise RuntimeError("fixture_systeme_" + labels[variant])
        if actual != 1:
            raise AssertionError(labels[variant])
        passed += 1
    result = {"fd_cases": passed, "qualification_provenance": False, "effet_TPM_NV": False}
    print(json.dumps(result, sort_keys=True))
    return result

if __name__ == "__main__":
    main()
