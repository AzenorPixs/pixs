# cython: language_level=3
"""Noyau E3 et primitive Ed25519, sans clé privée, certificat, socket ou admission.

Le contexte privé n'est jamais prêt à communiquer. Les interfaces de matière
et confiance Z12/PZT doivent être livrées avant un raccord de transport réel.
"""
cimport cython
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint32_t, uint64_t
from libc.string cimport strcmp, memcpy, memcmp

from libc.stdlib cimport calloc, free
from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF

cdef extern from "Python.h":
    unsigned long PyThread_get_thread_ident() noexcept

cdef extern from *:
    r"""
    #include <stdint.h>
    #include <time.h>
    #include <unistd.h>
    static int pa01_tls_pid(void) { return (int)getpid(); }
    static uint32_t pa01_tls_time(uint64_t end) {
        struct timespec ts;
        uint64_t sec, now;
        if (end == 0) return 1;
        if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) return 3;
        if (ts.tv_sec < 0 || ts.tv_nsec < 0 || ts.tv_nsec >= 1000000000) return 3;
        sec = (uint64_t)ts.tv_sec;
        if (sec > (UINT64_MAX - (uint64_t)ts.tv_nsec) / UINT64_C(1000000000)) return 3;
        now = sec * UINT64_C(1000000000) + (uint64_t)ts.tv_nsec;
        if (now == 0) return 3;
        return now >= end ? 6 : 0;
    }
    """
    int pa01_tls_pid() noexcept
    uint32_t pa01_tls_time(uint64_t) noexcept


cdef extern from "openssl/types.h":
    ctypedef struct OSSL_LIB_CTX:
        pass
    ctypedef struct OPENSSL_INIT_SETTINGS:
        pass
    ctypedef struct EVP_PKEY:
        pass
    ctypedef struct X509:
        pass
    ctypedef struct X509_STORE_CTX:
        pass

cdef extern from "openssl/crypto.h":
    OSSL_LIB_CTX *OSSL_LIB_CTX_new()
    void OSSL_LIB_CTX_free(OSSL_LIB_CTX *)
    void OPENSSL_thread_stop_ex(OSSL_LIB_CTX *)
    void OPENSSL_cleanse(void *, size_t) noexcept
    int OPENSSL_init_crypto(uint64_t, const OPENSSL_INIT_SETTINGS *)
    uint64_t OPENSSL_INIT_NO_LOAD_CONFIG
    unsigned int OPENSSL_version_major()
    unsigned int OPENSSL_version_minor()
    unsigned int OPENSSL_version_patch()

cdef extern from "openssl/opensslv.h":
    int OPENSSL_VERSION_MAJOR
    int OPENSSL_VERSION_MINOR
    int OPENSSL_VERSION_PATCH


cdef extern from "openssl/params.h":
    ctypedef struct OSSL_PARAM:
        pass

cdef extern from "openssl/evp.h":
    ctypedef struct EVP_MD_CTX:
        pass
    ctypedef struct EVP_PKEY_CTX:
        pass
    EVP_PKEY *EVP_PKEY_new_raw_public_key_ex(
        OSSL_LIB_CTX *, const char *, const char *, const unsigned char *, size_t)
    void EVP_PKEY_free(EVP_PKEY *)
    EVP_MD_CTX *EVP_MD_CTX_new()
    void EVP_MD_CTX_free(EVP_MD_CTX *)
    int EVP_DigestVerifyInit_ex(
        EVP_MD_CTX *, EVP_PKEY_CTX **, const char *, OSSL_LIB_CTX *,
        const char *, EVP_PKEY *, const OSSL_PARAM *)
    int EVP_DigestVerify(
        EVP_MD_CTX *, const unsigned char *, size_t, const unsigned char *, size_t)

cdef extern from "openssl/err.h":
    void ERR_clear_error()

cdef extern from "openssl/ssl.h":
    ctypedef struct SSL_CTX:
        pass
    ctypedef struct SSL_METHOD:
        pass
    ctypedef struct SSL_CIPHER:
        pass
    cdef struct stack_st_SSL_CIPHER:
        pass
    ctypedef int (*verify_callback)(int, X509_STORE_CTX *) noexcept
    const SSL_METHOD *TLS_client_method()
    const SSL_METHOD *TLS_server_method()
    SSL_CTX *SSL_CTX_new_ex(OSSL_LIB_CTX *, const char *, const SSL_METHOD *)
    void SSL_CTX_free(SSL_CTX *)
    long SSL_CTX_set_min_proto_version(SSL_CTX *, int)
    long SSL_CTX_set_max_proto_version(SSL_CTX *, int)
    long SSL_CTX_get_min_proto_version(const SSL_CTX *)
    long SSL_CTX_get_max_proto_version(const SSL_CTX *)
    int SSL_CTX_set_ciphersuites(SSL_CTX *, const char *)
    void SSL_CTX_set_verify(SSL_CTX *, int, verify_callback)
    int SSL_CTX_get_verify_mode(const SSL_CTX *)
    int SSL_CTX_set_max_early_data(SSL_CTX *, uint32_t)
    uint32_t SSL_CTX_get_max_early_data(const SSL_CTX *)
    stack_st_SSL_CIPHER *SSL_CTX_get_ciphers(const SSL_CTX *)
    int sk_SSL_CIPHER_num(const stack_st_SSL_CIPHER *)
    const SSL_CIPHER *sk_SSL_CIPHER_value(const stack_st_SSL_CIPHER *, int)
    const char *SSL_CIPHER_get_version(const SSL_CIPHER *)
    const char *SSL_CIPHER_get_name(const SSL_CIPHER *)
    X509 *SSL_CTX_get0_certificate(const SSL_CTX *)
    EVP_PKEY *SSL_CTX_get0_privatekey(const SSL_CTX *)
    int TLS1_3_VERSION
    int SSL_VERIFY_PEER
    int SSL_VERIFY_FAIL_IF_NO_PEER_CERT


class TLSConfigurationError(RuntimeError):
    """Erreur de configuration sans donnée reçue ni erreur OpenSSL brute."""


@cython.final
cdef class TLS13Context:
    cdef SSL_CTX *_ctx
    cdef OSSL_LIB_CTX *_library
    cdef object _side
    cdef void *_lease
    cdef int _creator_pid

    def __cinit__(self, suite, side):
        cdef bytes encoded
        cdef int verify
        cdef const SSL_METHOD *method
        self._ctx = NULL
        self._library = NULL
        self._lease = NULL
        self._creator_pid = pa01_tls_pid()
        if type(suite) is not str or suite not in (
                "TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"):
            raise TLSConfigurationError("PA01_TLS_SUITE_REQUIRED")
        if type(side) is not str or side not in ("client", "server"):
            raise TLSConfigurationError("PA01_TLS_SIDE_INVALID")
        if OPENSSL_init_crypto(OPENSSL_INIT_NO_LOAD_CONFIG, NULL) != 1:
            raise TLSConfigurationError("PA01_TLS_LIBRARY_INITIALIZATION_FAILED")
        if OPENSSL_VERSION_MAJOR != 3 or (
                OPENSSL_version_major() != OPENSSL_VERSION_MAJOR or
                OPENSSL_version_minor() != OPENSSL_VERSION_MINOR or
                OPENSSL_version_patch() != OPENSSL_VERSION_PATCH):
            raise TLSConfigurationError("PA01_TLS_LIBRARY_VERSION_MISMATCH")
        self._library = OSSL_LIB_CTX_new()
        if self._library == NULL:
            raise TLSConfigurationError("PA01_TLS_LIBRARY_CONTEXT_FAILED")
        try:
            method = TLS_server_method() if side == "server" else TLS_client_method()
            self._ctx = SSL_CTX_new_ex(self._library, NULL, method)
            if self._ctx == NULL:
                raise TLSConfigurationError("PA01_TLS_CONTEXT_CREATION_FAILED")
            if (SSL_CTX_set_min_proto_version(self._ctx, TLS1_3_VERSION) != 1 or
                    SSL_CTX_set_max_proto_version(self._ctx, TLS1_3_VERSION) != 1):
                raise TLSConfigurationError("PA01_TLS_PROTOCOL_CONFIGURATION_FAILED")
            encoded = suite.encode("ascii")
            if SSL_CTX_set_ciphersuites(self._ctx, encoded) != 1:
                raise TLSConfigurationError("PA01_TLS_SUITE_UNAVAILABLE")
            verify = SSL_VERIFY_PEER
            if side == "server":
                verify |= SSL_VERIFY_FAIL_IF_NO_PEER_CERT
            SSL_CTX_set_verify(self._ctx, verify, NULL)
            if SSL_CTX_set_max_early_data(self._ctx, 0) != 1:
                raise TLSConfigurationError("PA01_TLS_EARLY_DATA_CONFIGURATION_FAILED")
            if self._tls13_suites() != (suite,):
                raise TLSConfigurationError("PA01_TLS_EFFECTIVE_SUITE_MISMATCH")
            self._side = side
        finally:
            OPENSSL_thread_stop_ex(self._library)

    cdef tuple _tls13_suites(self):
        cdef stack_st_SSL_CIPHER *stack = SSL_CTX_get_ciphers(self._ctx)
        cdef const SSL_CIPHER *cipher
        cdef const char *version
        cdef const char *name
        cdef int count, index
        if stack == NULL:
            raise TLSConfigurationError("PA01_TLS_CIPHER_INVENTORY_UNAVAILABLE")
        count = sk_SSL_CIPHER_num(stack)
        if count < 0:
            raise TLSConfigurationError("PA01_TLS_CIPHER_INVENTORY_UNAVAILABLE")
        result = []
        for index in range(count):
            cipher = sk_SSL_CIPHER_value(stack, index)
            if cipher == NULL:
                raise TLSConfigurationError("PA01_TLS_CIPHER_INVENTORY_INVALID")
            version = SSL_CIPHER_get_version(cipher)
            if version != NULL and strcmp(version, "TLSv1.3") == 0:
                name = SSL_CIPHER_get_name(cipher)
                if name == NULL:
                    raise TLSConfigurationError("PA01_TLS_CIPHER_INVENTORY_INVALID")
                result.append(name.decode("ascii"))
        return tuple(result)

    cdef uint32_t _release(self) noexcept:
        if self._lease != NULL:
            return 4
        if self._ctx != NULL:
            SSL_CTX_free(self._ctx)
            self._ctx = NULL
        if self._library != NULL:
            OPENSSL_thread_stop_ex(self._library)
            OSSL_LIB_CTX_free(self._library)
            self._library = NULL
        return 0


    def verify_ed25519(self, public_key, signature, message, max_message_bytes):
        """Vérifie seulement une signature, sans accorder aucun droit.

        La clé publique fournie n'est pas authentifiée par cette primitive.
        Le propriétaire d'admission doit résoudre la clé préautorisée et
        construire les octets E4 exacts ; politique, cible, validité, état
        durable et toutes les autres conditions restent indépendants.
        Aucun objet clé ou pointeur n'est retourné.
        """
        cdef EVP_PKEY *key = NULL
        cdef EVP_MD_CTX *digest = NULL
        cdef bytes key_bytes, signature_bytes, message_bytes
        cdef int result
        if self._lease != NULL:
            raise TLSConfigurationError("PA01_TLS_LEASE_ACTIVE")
        if self._ctx == NULL or self._library == NULL:
            raise TLSConfigurationError("PA01_TLS_CONTEXT_CLOSED")
        if type(max_message_bytes) is not int or max_message_bytes <= 0:
            raise TLSConfigurationError("PA01_ED25519_BUDGET_INVALID")
        if type(public_key) is not bytes or len(public_key) != 32:
            raise TLSConfigurationError("PA01_ED25519_PUBLIC_KEY_INVALID")
        if type(signature) is not bytes or len(signature) != 64:
            raise TLSConfigurationError("PA01_ED25519_SIGNATURE_SHAPE_INVALID")
        if type(message) is not bytes or len(message) > max_message_bytes:
            raise TLSConfigurationError("PA01_ED25519_MESSAGE_INVALID")
        key_bytes = public_key
        signature_bytes = signature
        message_bytes = message
        ERR_clear_error()
        try:
            key = EVP_PKEY_new_raw_public_key_ex(
                self._library, "ED25519", "provider=default",
                <const unsigned char *> key_bytes, 32)
            if key == NULL:
                raise TLSConfigurationError("PA01_ED25519_PUBLIC_KEY_UNAVAILABLE")
            digest = EVP_MD_CTX_new()
            if digest == NULL:
                raise TLSConfigurationError("PA01_ED25519_CONTEXT_UNAVAILABLE")
            if EVP_DigestVerifyInit_ex(
                    digest, NULL, NULL, self._library, "provider=default", key, NULL) != 1:
                raise TLSConfigurationError("PA01_ED25519_INITIALIZATION_FAILED")
            result = EVP_DigestVerify(
                digest, <const unsigned char *> signature_bytes, 64,
                <const unsigned char *> message_bytes, len(message_bytes))
            if result == 0:
                raise TLSConfigurationError("PA01_ED25519_SIGNATURE_INVALID")
            if result != 1:
                raise TLSConfigurationError("PA01_ED25519_VERIFICATION_FAILED")
            return None
        finally:
            EVP_MD_CTX_free(digest)
            EVP_PKEY_free(key)
            ERR_clear_error()
            OPENSSL_thread_stop_ex(self._library)

    def configuration(self):
        if self._lease != NULL:
            raise TLSConfigurationError("PA01_TLS_LEASE_ACTIVE")
        if self._ctx == NULL:
            raise TLSConfigurationError("PA01_TLS_CONTEXT_CLOSED")
        mode = SSL_CTX_get_verify_mode(self._ctx)
        return {
            "side": self._side,
            "tls13_suites": self._tls13_suites(),
            "minimum_protocol": SSL_CTX_get_min_proto_version(self._ctx),
            "maximum_protocol": SSL_CTX_get_max_proto_version(self._ctx),
            "peer_verification": bool(mode & SSL_VERIFY_PEER),
            "client_certificate_required": bool(mode & SSL_VERIFY_FAIL_IF_NO_PEER_CERT),
            "max_early_data": SSL_CTX_get_max_early_data(self._ctx),
            "certificate_loaded": SSL_CTX_get0_certificate(self._ctx) != NULL,
            "private_key_loaded": SSL_CTX_get0_privatekey(self._ctx) != NULL,
            "ready_for_transport": False,
        }

    def close(self):
        if self._lease != NULL:
            raise TLSConfigurationError("PA01_TLS_LEASE_ACTIVE")
        self._release()

    def __enter__(self):
        if self._lease != NULL:
            raise TLSConfigurationError("PA01_TLS_LEASE_ACTIVE")
        if self._ctx == NULL:
            raise TLSConfigurationError("PA01_TLS_CONTEXT_CLOSED")
        return self

    def __exit__(self, *ignored):
        if self._lease != NULL:
            raise TLSConfigurationError("PA01_TLS_LEASE_ACTIVE")
        self._release()

    def __dealloc__(self):
        self._release()

    def __reduce__(self):
        raise TypeError("PA01_TLS_CONTEXT_NOT_SERIALIZABLE")

    def __repr__(self):
        return "TLS13Context(<redacted>)"


# Port privé de INITIAL_MATERIAL : seul le client Z12 inclus dans ce
# module peut l'appeler. Le prêt ne confère aucune autorité d'admission.
# Le client doit enregistrer ses acquisitions natives et effectuer les
# transferts/libérations OpenSSL réels avant _tls_lease_close ; aucun
# booléen fourni par un appelant ne prouve cette terminaison. Une issue
# inconnue conserve son état, le prêt et les références pour réconciliation.
# Un transport futur doit conserver le vrai propriétaire de OSSL_LIB_CTX
# tant que ses SSL en dépendent ; SSL_CTX_up_ref seul ne le remplace pas.
# PID/thread imposent une exclusivité locale, pas une identité PKI forte.
cdef struct _TLSLease:
    PyObject *subject
    void *owner
    OSSL_LIB_CTX *library
    SSL_CTX *ssl
    int pid
    unsigned long thread
    uint64_t deadline
    uint32_t usage
    uint8_t operation[32]
    int side
    int withdrawn

cdef uint32_t _tls_lease_new(void **out, PyObject *subject, void *owner,
        int expected_side, uint32_t usage, const uint8_t *operation,
        size_t operation_size, uint64_t deadline) noexcept with gil:
    cdef TLS13Context context
    cdef _TLSLease *lease
    cdef uint32_t status
    if (out == NULL or out[0] != NULL or subject == NULL or owner == NULL
            or operation == NULL or operation_size != 32 or usage != 1
            or expected_side not in (1, 2)):
        return 1
    if type(<object>subject) is not TLS13Context:
        return 1
    context = <TLS13Context><object>subject
    if (context._ctx == NULL or context._library == NULL or context._lease != NULL
            or context._creator_pid != pa01_tls_pid()):
        return 4
    if (expected_side == 1 and context._side != "client"
            or expected_side == 2 and context._side != "server"):
        return 4
    status = pa01_tls_time(deadline)
    if status != 0:
        return status
    lease = <_TLSLease *>calloc(1, sizeof(_TLSLease))
    if lease == NULL:
        return 2
    lease.subject = subject
    lease.owner = owner
    lease.library = context._library
    lease.ssl = context._ctx
    lease.pid = context._creator_pid
    lease.thread = PyThread_get_thread_ident()
    if lease.thread == 0:
        OPENSSL_cleanse(lease, sizeof(_TLSLease))
        free(lease)
        return 4
    lease.deadline = deadline
    lease.usage = usage
    lease.side = expected_side
    memcpy(lease.operation, operation, 32)
    status = pa01_tls_time(deadline)
    if status != 0:
        OPENSSL_cleanse(lease, sizeof(_TLSLease))
        free(lease)
        return status
    Py_INCREF(<object>subject)
    context._lease = <void *>lease
    out[0] = <void *>lease
    return 0

cdef uint32_t _tls_lease_context(void *state, void *owner,
        int expected_side, uint32_t usage, const uint8_t *operation,
        size_t operation_size, OSSL_LIB_CTX **library_out, SSL_CTX **ssl_out) noexcept with gil:
    cdef _TLSLease *lease = <_TLSLease *>state
    cdef TLS13Context context
    cdef uint32_t status
    if library_out != NULL:
        library_out[0] = NULL
    if ssl_out != NULL:
        ssl_out[0] = NULL
    if (lease == NULL or owner == NULL or operation == NULL or operation_size != 32
            or library_out == NULL or ssl_out == NULL or <void *>library_out == <void *>ssl_out):
        return 1
    if (lease.owner != owner or lease.pid != pa01_tls_pid()
            or lease.thread != PyThread_get_thread_ident() or lease.withdrawn
            or lease.side != expected_side or lease.usage != usage
            or memcmp(lease.operation, operation, 32) != 0):
        return 4
    status = pa01_tls_time(lease.deadline)
    if status != 0:
        return status
    context = <TLS13Context><object>lease.subject
    if (context._lease != state or context._ctx != lease.ssl
            or context._library != lease.library
            or context._ctx == NULL or context._library == NULL):
        return 4
    library_out[0] = lease.library
    ssl_out[0] = lease.ssl
    return 0

cdef uint32_t _tls_lease_withdraw(void *state, void *owner) noexcept with gil:
    cdef _TLSLease *lease = <_TLSLease *>state
    if lease == NULL or owner == NULL:
        return 1
    if (lease.owner != owner or lease.pid != pa01_tls_pid()
            or lease.thread != PyThread_get_thread_ident()):
        return 4
    lease.withdrawn = 1
    return 0

# Précondition du graphe fermé : l'unique client inclus a réellement
# détruit/consommé son état après transfert/libération de ses références.
# Ce port ne connaît pas les objets d'un emprunteur arbitraire et ne doit
# jamais être exporté en cdef public/api ou capsule Python.
cdef uint32_t _tls_lease_close(void **state, void *owner) noexcept with gil:
    cdef _TLSLease *lease
    cdef TLS13Context context
    if state == NULL or owner == NULL:
        return 1
    if state[0] == NULL:
        return 0
    lease = <_TLSLease *>state[0]
    if (lease.owner != owner or lease.pid != pa01_tls_pid()
            or lease.thread != PyThread_get_thread_ident()):
        return 4
    context = <TLS13Context><object>lease.subject
    if (context._lease != state[0] or context._ctx != lease.ssl
            or context._library != lease.library):
        return 4
    context._lease = NULL
    Py_DECREF(<object>lease.subject)
    OPENSSL_cleanse(lease, sizeof(_TLSLease))
    free(lease)
    state[0] = NULL
    return 0
