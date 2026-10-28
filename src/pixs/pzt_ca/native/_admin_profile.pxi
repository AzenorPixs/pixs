# Prive Z12 : observation du profil administratif compile, sans admission.
# A inclure UNE fois APRES _monotonic_deadline.pxi, sans le reinclure.
# Ni openssl ni _monotonic redeclare ici, ordre final controle par l'inclueur.
# Provenance d'installation et admission reelle hors scope, aucun trusted=true.
from libc.stddef cimport size_t
from libc.stdint cimport uint64_t, int32_t
from libc.string cimport memcmp

cdef extern from * nogil:
    r"""
    #include "z12_admin_profile.inc"
    #include <stddef.h>
    #include <stdint.h>
    #include <string.h>
    typedef struct {
        const unsigned char *identity_ptr;
        size_t identity_len;
        const unsigned char *domain_ptr;
        size_t domain_len;
        const unsigned char *version_ptr;
        size_t version_len;
        const unsigned char *pubkey_ptr;
        size_t max_payload_len;
        size_t max_field_len;
        uint64_t budget_ns;
        int fixture_flag;
    } Z12AdminView;
    static int z12_admin_observe(Z12AdminView *out) {
        const char *domain_literal = "pixs.z12.admin/v1";
        size_t domain_expect;
        size_t i;
        unsigned char acc = 0;
        if (out == NULL) return -2;
        out->identity_ptr = NULL; out->identity_len = 0;
        out->domain_ptr = NULL; out->domain_len = 0;
        out->version_ptr = NULL; out->version_len = 0;
        out->pubkey_ptr = NULL;
        out->max_payload_len = 0; out->max_field_len = 0;
        out->budget_ns = 0; out->fixture_flag = 0;
        domain_expect = sizeof("pixs.z12.admin/v1") - 1;
        if (Z12_ADMIN_IDENTITY_LEN < 1 || Z12_ADMIN_IDENTITY_LEN > 256) return 0;
        if (sizeof(kZ12AdminIdentity) != (size_t)Z12_ADMIN_IDENTITY_LEN) return 0;
        if (Z12_ADMIN_DOMAIN_LEN != domain_expect) return 0;
        if (sizeof(kZ12AdminDomain) != domain_expect) return 0;
        if (memcmp(kZ12AdminDomain, domain_literal, domain_expect) != 0) return 0;
        if (Z12_ADMIN_VERSION_LEN < 1 || Z12_ADMIN_VERSION_LEN > 256) return 0;
        if (sizeof(kZ12AdminVersion) != (size_t)Z12_ADMIN_VERSION_LEN) return 0;
        if (Z12_ADMIN_PUBKEY_LEN != 32) return 0;
        if (sizeof(kZ12AdminPubkey) != 32) return 0;
        for (i = 0; i < 32; i++) acc |= kZ12AdminPubkey[i];
        if (acc == 0) return 0;
        if ((uint64_t)Z12_ADMIN_MAX_PAYLOAD_LEN < 1 || (uint64_t)Z12_ADMIN_MAX_PAYLOAD_LEN > (uint64_t)UINT32_MAX) return 0;
        if ((uint64_t)Z12_ADMIN_MAX_FIELD_LEN < 1 || (uint64_t)Z12_ADMIN_MAX_FIELD_LEN > (uint64_t)UINT32_MAX) return 0;
        if ((uint64_t)Z12_ADMIN_MAX_FIELD_LEN > (uint64_t)Z12_ADMIN_MAX_PAYLOAD_LEN) return 0;
        if (Z12_ADMIN_BUDGET_NS == 0) return 0;
        if (Z12_ADMIN_FIXTURE != 0 && Z12_ADMIN_FIXTURE != 1) return 0;
        out->identity_ptr = kZ12AdminIdentity;
        out->identity_len = (size_t)Z12_ADMIN_IDENTITY_LEN;
        out->domain_ptr = kZ12AdminDomain;
        out->domain_len = domain_expect;
        out->version_ptr = kZ12AdminVersion;
        out->version_len = (size_t)Z12_ADMIN_VERSION_LEN;
        out->pubkey_ptr = kZ12AdminPubkey;
        out->max_payload_len = (size_t)Z12_ADMIN_MAX_PAYLOAD_LEN;
        out->max_field_len = (size_t)Z12_ADMIN_MAX_FIELD_LEN;
        out->budget_ns = (uint64_t)Z12_ADMIN_BUDGET_NS;
        out->fixture_flag = (int)Z12_ADMIN_FIXTURE;
        return 1;
    }
    static int z12_admin_require_no_fixture(void) {
        if (Z12_ADMIN_FIXTURE == 0) return 1;
        if (Z12_ADMIN_FIXTURE == 1) return 0;
        return -2;
    }
    """
    ctypedef struct Z12AdminView:
        const unsigned char *identity_ptr
        size_t identity_len
        const unsigned char *domain_ptr
        size_t domain_len
        const unsigned char *version_ptr
        size_t version_len
        const unsigned char *pubkey_ptr
        size_t max_payload_len
        size_t max_field_len
        uint64_t budget_ns
        int fixture_flag
    int z12_admin_observe(Z12AdminView *out)
    int z12_admin_require_no_fixture()

cdef int _admin_profile_observe(Z12AdminView *output) noexcept nogil:
    # 1=observe depuis constantes compilees, 0=invalide public, -2=precondition.
    # Prend SEULEMENT output, aucun choix externe de pointeurs, cle, bornes, fixture.
    # Pointeurs const statiques duree de vie artefact, output seule vue publique interne.
    if output == NULL:
        return -2
    return z12_admin_observe(output)

cdef int _admin_profile_is_fixture(const Z12AdminView *view) noexcept nogil:
    # 1=fixture, 0=non fixture, sans provenance ni admission, -2=precondition. Sans dereference NULL.
    if view == NULL:
        return -2
    if view.fixture_flag != 0 and view.fixture_flag != 1:
        return -2
    if view.fixture_flag == 1:
        return 1
    return 0

cdef int _admin_profile_require_no_fixture() noexcept nogil:
    # Lit la constante compilee, pas un fanion mutable.
    # 1=fixture exclue, 0=fixture presente exclue du prod, -2=build invalide.
    # Aucune admission conferee dans tous les cas.
    return z12_admin_require_no_fixture()

cdef int _admin_profile_check_live(
    Z12MonotonicDeadline *deadline,
    int32_t *timeout_ms
) noexcept nogil:
    # Precondition : _monotonic_deadline.pxi inclus avant, deadline deja demarree
    # UNE seule fois par le proprietaire depuis le budget compile avant toute IO.
    # Constate actuel via z12_deadline_remaining reel, propage 1/0/-1/-2.
    # Ne demarre ni ne remet a zero, n'accepte pas expiree comme valide.
    # Si le type ne prouve pas le plafonnement, le plafonnement reste contrat
    # du proprietaire, non affirme ici.
    if deadline == NULL or timeout_ms == NULL:
        return -2
    return z12_deadline_remaining(deadline, timeout_ms)
