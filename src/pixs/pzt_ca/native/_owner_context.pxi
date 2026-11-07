# Prive Z12 : constructeur d'observation proprietaire, sans admission.
# Feuille : aucun include de .pxi ici. Ordre exact exige par l'inclueur, une fois chacun :
# _monotonic_deadline.pxi, _admin_profile.pxi, _operator_verify.pxi apportant _openssl_ed25519.pxi une fois, _launch_obs_sysd.pxi,
# _systemd_connection.pxi, _process_image.pxi sans redeclaration OSSL_LIB_CTX, _manager_unit.pxi.
# Seul z12_owner_limits.inc reellement inclus ici. Headers systeme et OpenSSL reentrants autorises.
# OSSL_LIB_CTX suppose apporte par _operator_verify avant _process_image, non redefini ici, sans include _ed explicite en doublon.
# Endpoint fourni seul, sans defaut invente ; liaison au plan authentique avant admission.
# Observation positive n'est pas autorite ; fixture ne qualifie pas la production.
# Convention privee : *out non nul avec valid==0 et quarantine==1 signifie cleanup_only,
# jamais utilisable ; la garde refuse ; l'appelant draine et termine le processus selon l'issue.
# Aucun *pp=NULL avant preuve d'absence de ressource. Apres fork aucun appel libsystemd ni OpenSSL.
# Exclusion liee au PID et TID natifs createurs ; mauvais thread refuse avant libs.
# Build -D_GNU_SOURCE. Contexte exclusif au processus createur.
from libc.stddef cimport size_t
from libc.stdint cimport uint64_t, uint32_t, UINT32_MAX
from posix.types cimport pid_t, uid_t

cdef extern from "openssl/crypto.h" nogil:
    OSSL_LIB_CTX *OSSL_LIB_CTX_new()
    void OSSL_LIB_CTX_free(OSSL_LIB_CTX *ctx)

cdef extern from "openssl/provider.h" nogil:
    ctypedef struct OSSL_PROVIDER:
        pass
    OSSL_PROVIDER *OSSL_PROVIDER_load(OSSL_LIB_CTX *libctx, const char *name)
    int OSSL_PROVIDER_unload(OSSL_PROVIDER *prov)

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <limits.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/un.h>
    #include <openssl/crypto.h>
    #include <openssl/provider.h>
    #include <openssl/evp.h>
    #include <systemd/sd-bus.h>
    #include "z12_owner_limits.inc"

    typedef struct {
        Z12MonotonicDeadline deadline;
        uint64_t expected_end;
        OSSL_LIB_CTX *libctx;
        OSSL_PROVIDER *provider;
        Z12SysdConn *conn;
        Z12ProcessImage *self_img;
        Z12ProcessImage *peer_img;
        Z12ManagerUnit *unit;
        Z12ImageCtx imgctx;
        Z12AdminView admin;
        size_t image_exe_max;
        size_t procmeta_max;
        size_t unit_path_max;
        size_t unit_name_max;
        int fixture;
        int admin_fixture;
        pid_t creator_pid;
        pid_t creator_tid;
        uid_t creator_uid;
        uid_t creator_euid;
        int valid;
        int quarantine;
    } Z12OwnerCtx;

    typedef struct {
        Z12ProcessImageDiag img;
        Z12SysdDiag cleanup_native;
        int admin_invalid;
        int limits_invalid;
        int invalid_contract;
        int cleanup_conn;
        int cleanup_provider_stage;
    } Z12OwnerDiag;

    static pid_t z12_owner_gettid(void) {
        return gettid();
    }

    static int z12_owner_same_thread(const Z12OwnerCtx *c) {
        if (c == NULL) return 0;
        if (getpid() != c->creator_pid) return 0;
        if (z12_owner_gettid() != c->creator_tid) return 0;
        if (getuid() != c->creator_uid) return 0;
        if (geteuid() != c->creator_euid) return 0;
        return 1;
    }

    static int z12_owner_verdict(Z12OwnerDiag *d, int r) {
        if (d == NULL) return -2;
        if (d->img.native.primary_kind != Z12_SYSD_NONE) return -1;
        if (d->img.native.cleanup_errno != 0) return -1;
        if (d->img.openssl_failed) return -1;
        if (d->cleanup_native.primary_kind != Z12_SYSD_NONE) return -1;
        if (d->cleanup_native.cleanup_errno != 0) return -1;
        if (d->cleanup_native.must_destroy_bus != 0) return -1;
        if (d->cleanup_conn != 0) return -1;
        if (d->cleanup_provider_stage != 0) return -1;
        if (d->invalid_contract) return -2;
        if (d->img.native.invalid_input) return -2;
        if (d->admin_invalid || d->limits_invalid) return 0;
        if (d->img.native.native_output_invalid || d->img.native.foreign_binding ||
            d->img.native.process_unavailable || d->img.native.deadline_expired ||
            d->img.native.clock_failed || d->img.native.must_destroy_bus) return 0;
        return r;
    }

    static int z12_owner_limits_observe(size_t *exe, size_t *meta,
                                        size_t *path, size_t *unit,
                                        int *fixture, Z12OwnerDiag *d) {
        static const char expect[] = "pixs.z12.owner.limits/v1";
        size_t dexp;
        uint64_t v;
        if (exe == NULL || meta == NULL || path == NULL || unit == NULL ||
            fixture == NULL || d == NULL) return -2;
        *exe = 0; *meta = 0; *path = 0; *unit = 0; *fixture = 0;
        dexp = sizeof(expect) - 1;
        if (Z12_OWNER_LIMITS_IDENTITY_LEN < 1 || Z12_OWNER_LIMITS_IDENTITY_LEN > 256) {
            d->limits_invalid = 1; return 0;
        }
        if (sizeof(Z12_OWNER_LIMITS_IDENTITY_BYTES) != (size_t)Z12_OWNER_LIMITS_IDENTITY_LEN) {
            d->limits_invalid = 1; return 0;
        }
        if ((size_t)Z12_OWNER_LIMITS_DOMAIN_LEN != dexp) { d->limits_invalid = 1; return 0; }
        if (sizeof(Z12_OWNER_LIMITS_DOMAIN_BYTES) != dexp) { d->limits_invalid = 1; return 0; }
        if (memcmp(Z12_OWNER_LIMITS_DOMAIN_BYTES, expect, dexp) != 0) {
            d->limits_invalid = 1; return 0;
        }
        if (Z12_OWNER_LIMITS_VERSION_LEN < 1 || Z12_OWNER_LIMITS_VERSION_LEN > 256) {
            d->limits_invalid = 1; return 0;
        }
        if (sizeof(Z12_OWNER_LIMITS_VERSION_BYTES) != (size_t)Z12_OWNER_LIMITS_VERSION_LEN) {
            d->limits_invalid = 1; return 0;
        }
        v = (uint64_t)Z12_OWNER_IMAGE_EXE_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) {
            d->limits_invalid = 1; return 0;
        }
        v = (uint64_t)Z12_OWNER_PROCMETA_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) {
            d->limits_invalid = 1; return 0;
        }
        v = (uint64_t)Z12_OWNER_UNIT_PATH_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) {
            d->limits_invalid = 1; return 0;
        }
        v = (uint64_t)Z12_OWNER_UNIT_NAME_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) {
            d->limits_invalid = 1; return 0;
        }
        if (Z12_OWNER_LIMITS_FIXTURE != 0 && Z12_OWNER_LIMITS_FIXTURE != 1) {
            d->limits_invalid = 1; return 0;
        }
        *exe = (size_t)Z12_OWNER_IMAGE_EXE_MAX;
        *meta = (size_t)Z12_OWNER_PROCMETA_MAX;
        *path = (size_t)Z12_OWNER_UNIT_PATH_MAX;
        *unit = (size_t)Z12_OWNER_UNIT_NAME_MAX;
        if (*exe == SIZE_MAX || *meta == SIZE_MAX || *path == SIZE_MAX || *unit == SIZE_MAX) {
            d->limits_invalid = 1; return 0;
        }
        *fixture = (int)Z12_OWNER_LIMITS_FIXTURE;
        return 1;
    }

    static int z12_owner_release_owned(Z12OwnerCtx *c, Z12OwnerDiag *d) {
        int conn_r = 0;
        int has_conn = 0;
        if (c == NULL || d == NULL) return -2;
        if (!z12_owner_same_thread(c)) {
            d->img.native.foreign_binding = 1;
            d->img.native.must_destroy_bus = 1;
            return -2;
        }
        if (c->unit != NULL) { z12_manager_unit_destroy(&c->unit); }
        if (c->peer_img != NULL) { z12_process_image_destroy(&c->peer_img); }
        if (c->self_img != NULL) { z12_process_image_destroy(&c->self_img); }
        if (c->conn != NULL) {
            has_conn = 1;
            conn_r = z12_sysd_conn_destroy(&c->conn, &d->cleanup_native);
            if (conn_r == -2) {
                if (d->cleanup_conn == 0) d->cleanup_conn = -2;
                return -2;
            }
            if (conn_r == -1) {
                if (d->cleanup_conn == 0) d->cleanup_conn = -1;
            }
        }
        if (c->provider != NULL) {
            int u = OSSL_PROVIDER_unload(c->provider);
            if (u == 1) {
                c->provider = NULL;
                if (c->libctx != NULL) { OSSL_LIB_CTX_free(c->libctx); c->libctx = NULL; }
            } else {
                if (d->cleanup_provider_stage == 0) d->cleanup_provider_stage = 11;
                return 0;
            }
        } else if (c->libctx != NULL) {
            OSSL_LIB_CTX_free(c->libctx); c->libctx = NULL;
        }
        if (c->conn != NULL) {
            if (d->cleanup_conn == 0) d->cleanup_conn = 1;
            return 0;
        }
        explicit_bzero(&c->imgctx.snapshot, sizeof(c->imgctx.snapshot));
        c->imgctx.conn = NULL; c->imgctx.bus = NULL; c->imgctx.facts = NULL;
        c->imgctx.deadline = NULL; c->imgctx.end = 0; c->imgctx.pidfd = -1;
        if (has_conn && conn_r != 0) return conn_r == -1 ? -1 : conn_r;
        return 1;
    }

    static int z12_owner_create(const char *endpoint, size_t endpoint_size,
                                Z12OwnerCtx **out, Z12OwnerDiag *diag) {
        Z12OwnerCtx *c = NULL;
        Z12AdminView admin = {0};
        Z12ManagerUnitDiag mu = {0};
        Z12MonotonicDeadline tmp = {0};
        Z12SysdDiag tmpd = {0};
        size_t exe = 0, meta = 0, path = 0, uname = 0;
        int fixture = 0;
        int r = -2;
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        if (out == NULL || *out != NULL || endpoint == NULL || endpoint_size == 0) {
            diag->invalid_contract = 1; return -2;
        }
        *out = NULL;
        r = z12_admin_observe(&admin);
        if (r != 1) { diag->admin_invalid = 1; return z12_owner_verdict(diag, 0); }
        if (admin.budget_ns == 0 || admin.identity_ptr == NULL || admin.domain_ptr == NULL ||
            admin.version_ptr == NULL || admin.pubkey_ptr == NULL) {
            diag->admin_invalid = 1; return z12_owner_verdict(diag, 0);
        }
        r = z12_owner_limits_observe(&exe, &meta, &path, &uname, &fixture, diag);
        if (r != 1) return z12_owner_verdict(diag, r);
        r = z12_deadline_start(&tmp, admin.budget_ns);
        if (r != 1) {
            if (r == -1) z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno);
            else diag->invalid_contract = 1;
            explicit_bzero(&tmp, sizeof(tmp));
            return (r == -2) ? -2 : z12_owner_verdict(diag, -1);
        }
        r = z12_sysd_deadline(&tmp, tmp.end_ns, &tmpd);
        if (r != 1) {
            if (r == -1 && diag->img.native.primary_kind == Z12_SYSD_NONE) {
                diag->img.native.clock_failed = 1;
            }
            if (r == -2) diag->invalid_contract = 1;
            else diag->img.native.must_destroy_bus = 1;
            explicit_bzero(&tmp, sizeof(tmp));
            return z12_owner_verdict(diag, r);
        }
        c = (Z12OwnerCtx *)calloc(1, sizeof(*c));
        if (c == NULL) {
            int saved_errno = errno;
            z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, saved_errno);
            r = z12_sysd_deadline(&tmp, tmp.end_ns, &diag->img.native);
            explicit_bzero(&tmp, sizeof(tmp));
            if (r != 1) return z12_owner_verdict(diag, r);
            return z12_owner_verdict(diag, -1);
        }
        c->libctx = NULL; c->provider = NULL; c->conn = NULL;
        c->self_img = NULL; c->peer_img = NULL; c->unit = NULL;
        c->imgctx.pidfd = -1;
        c->valid = 0; c->quarantine = 0;
        c->creator_pid = getpid();
        c->creator_tid = z12_owner_gettid();
        c->creator_uid = getuid(); c->creator_euid = geteuid();
        if (c->creator_pid <= 0 || c->creator_tid <= 0) {
            diag->img.native.native_output_invalid = 1;
            explicit_bzero(&tmp, sizeof(tmp));
            explicit_bzero(c, sizeof(*c)); free(c);
            return z12_owner_verdict(diag, 0);
        }
        memcpy(&c->deadline, &tmp, sizeof(tmp));
        c->expected_end = tmp.end_ns;
        explicit_bzero(&tmp, sizeof(tmp));
        memcpy(&c->admin, &admin, sizeof(admin));
        c->admin_fixture = admin.fixture_flag;
        c->image_exe_max = exe; c->procmeta_max = meta;
        c->unit_path_max = path; c->unit_name_max = uname;
        c->fixture = fixture;
        r = z12_sysd_deadline(&c->deadline, c->expected_end, &diag->img.native);
        if (r != 1) {
            explicit_bzero(c, sizeof(*c)); free(c);
            return z12_owner_verdict(diag, r);
        }
        c->libctx = OSSL_LIB_CTX_new();
        if (c->libctx == NULL) {
            diag->img.openssl_failed = 1; diag->img.openssl_stage = 1;
            r = z12_sysd_deadline(&c->deadline, c->expected_end, &diag->img.native);
            if (r != 1) goto fail;
            r = -1; goto fail;
        }
        r = z12_sysd_deadline(&c->deadline, c->expected_end, &diag->img.native);
        if (r != 1) {
            OSSL_LIB_CTX_free(c->libctx); c->libctx = NULL;
            explicit_bzero(c, sizeof(*c)); free(c);
            return z12_owner_verdict(diag, r);
        }
        c->provider = OSSL_PROVIDER_load(c->libctx, "default");
        if (c->provider == NULL) {
            diag->img.openssl_failed = 1; diag->img.openssl_stage = 2;
            r = z12_sysd_deadline(&c->deadline, c->expected_end, &diag->img.native);
            if (r != 1) goto fail;
            r = -1; goto fail;
        }
        r = z12_sysd_deadline(&c->deadline, c->expected_end, &diag->img.native);
        if (r != 1) goto fail;
        r = z12_sysd_connect(endpoint, endpoint_size, &c->deadline,
                             c->expected_end, &c->conn, &diag->img.native);
        if (r != 1) goto fail;
        if (c->conn == NULL || c->conn->facts == NULL || c->conn->bus == NULL) {
            diag->img.native.foreign_binding = 1; r = 0; goto fail;
        }
        c->imgctx.conn = c->conn;
        c->imgctx.bus = c->conn->bus;
        c->imgctx.facts = c->conn->facts;
        memcpy(&c->imgctx.snapshot, c->conn->facts, sizeof(c->imgctx.snapshot));
        c->imgctx.deadline = &c->deadline;
        c->imgctx.end = c->expected_end;
        c->imgctx.pidfd = c->imgctx.snapshot.self_pidfd;
        if (c->imgctx.pidfd < 0) { diag->img.native.foreign_binding = 1; r = 0; goto fail; }
        r = z12_image_guard(&c->imgctx, &diag->img);
        if (r != 1) goto fail;
        r = z12_process_image_collect(c->conn, c->libctx, Z12_PROCESS_SELF,
                                      c->image_exe_max, c->procmeta_max,
                                      &c->self_img, &diag->img);
        if (r != 1) goto fail;
        r = z12_image_guard(&c->imgctx, &diag->img);
        if (r != 1) goto fail;
        r = z12_process_image_collect(c->conn, c->libctx, Z12_PROCESS_PEER,
                                      c->image_exe_max, c->procmeta_max,
                                      &c->peer_img, &diag->img);
        if (r != 1) goto fail;
        r = z12_image_guard(&c->imgctx, &diag->img);
        if (r != 1) goto fail;
        memset(&mu, 0, sizeof(mu));
        r = z12_manager_unit_collect(c->conn, c->unit_path_max, c->unit_name_max,
                                     &c->unit, &mu);
        diag->img.native = mu.native;
        diag->img.openssl_failed = mu.openssl_failed;
        diag->img.openssl_stage = mu.openssl_stage;
        diag->img.openssl_code = mu.openssl_code;
        if (r != 1) goto fail;
        r = z12_image_guard(&c->imgctx, &diag->img);
        if (r != 1) goto fail;
        if (c->self_img == NULL || c->peer_img == NULL || c->unit == NULL) {
            diag->img.native.native_output_invalid = 1; r = 0; goto fail;
        }
        if (!z12_owner_same_thread(c)) {
            diag->img.native.foreign_binding = 1; r = 0; goto fail;
        }
        c->valid = 1; c->quarantine = 0;
        *out = c;
        return z12_owner_verdict(diag, 1);
    fail:
        {
            int rel;
            if (!z12_owner_same_thread(c)) {
                diag->img.native.foreign_binding = 1;
                diag->img.native.must_destroy_bus = 1;
                c->valid = 0; c->quarantine = 1;
                *out = c;
                return -2;
            }
            c->valid = 0;
            rel = z12_owner_release_owned(c, diag);
            if (rel == 1) {
                int bad = (diag->img.native.primary_kind != Z12_SYSD_NONE ||
                           diag->img.native.cleanup_errno != 0 || diag->img.openssl_failed ||
                           diag->cleanup_native.primary_kind != Z12_SYSD_NONE ||
                           diag->cleanup_native.cleanup_errno != 0 ||
                           diag->cleanup_native.must_destroy_bus != 0 ||
                           diag->cleanup_conn != 0 || diag->cleanup_provider_stage != 0);
                explicit_bzero(c, sizeof(*c)); free(c);
                *out = NULL;
                if (r == -2) return -2;
                if (r == -1 || bad) return z12_owner_verdict(diag, -1);
                return z12_owner_verdict(diag, 0);
            }
            if (c->libctx == NULL && c->provider == NULL && c->conn == NULL &&
                c->self_img == NULL && c->peer_img == NULL && c->unit == NULL) {
                explicit_bzero(c, sizeof(*c)); free(c);
                *out = NULL;
                return z12_owner_verdict(diag, -1);
            }
            c->quarantine = 1;
            *out = c;
            if (rel == -2) return -2;
            return z12_owner_verdict(diag, -1);
        }
    }

    static int z12_owner_guard(Z12OwnerCtx *c, Z12OwnerDiag *d) {
        int r;
        if (c == NULL || d == NULL) return -2;
        if (c->valid != 1 || c->quarantine != 0) return 0;
        if (c->libctx == NULL || c->provider == NULL || c->conn == NULL ||
            c->self_img == NULL || c->peer_img == NULL || c->unit == NULL) {
            d->invalid_contract = 1; return -2;
        }
        if (!z12_owner_same_thread(c)) {
            d->img.native.foreign_binding = 1; return 0;
        }
        r = z12_image_guard(&c->imgctx, &d->img);
        if (r == 1 && (c->valid != 1 || c->quarantine != 0)) return 0;
        return z12_owner_verdict(d, r);
    }

    static int z12_owner_destroy(Z12OwnerCtx **pp, Z12OwnerDiag *d) {
        Z12OwnerCtx *c;
        int rel;
        if (pp == NULL || d == NULL) return -2;
        c = *pp;
        if (c == NULL) return 0;
        if (c->quarantine != 0) return -1;
        if (c->valid != 1) {
            d->invalid_contract = 1; return -2;
        }
        if (!z12_owner_same_thread(c)) {
            d->img.native.foreign_binding = 1;
            d->img.native.must_destroy_bus = 1;
            return -2;
        }
        c->valid = 0;
        rel = z12_owner_release_owned(c, d);
        if (rel == 1) {
            int bad = (d->img.native.primary_kind != Z12_SYSD_NONE ||
                       d->img.native.cleanup_errno != 0 || d->img.openssl_failed ||
                       d->cleanup_native.primary_kind != Z12_SYSD_NONE ||
                       d->cleanup_native.cleanup_errno != 0 ||
                       d->cleanup_native.must_destroy_bus != 0 ||
                       d->cleanup_conn != 0 || d->cleanup_provider_stage != 0);
            explicit_bzero(c, sizeof(*c)); free(c);
            *pp = NULL;
            return bad ? -1 : 1;
        }
        if (c->libctx == NULL && c->provider == NULL && c->conn == NULL &&
            c->self_img == NULL && c->peer_img == NULL && c->unit == NULL) {
            explicit_bzero(c, sizeof(*c)); free(c);
            *pp = NULL;
            return -1;
        }
        c->quarantine = 1;
        return (rel == -2) ? -2 : -1;
    }
    """
    ctypedef struct Z12OwnerCtx:
        pass
    ctypedef struct Z12OwnerDiag:
        Z12ProcessImageDiag img
        Z12SysdDiag cleanup_native
        int admin_invalid
        int limits_invalid
        int invalid_contract
        int cleanup_conn
        int cleanup_provider_stage
    int z12_owner_create(const char *endpoint, size_t endpoint_size,
                         Z12OwnerCtx **out, Z12OwnerDiag *diag)
    int z12_owner_guard(Z12OwnerCtx *c, Z12OwnerDiag *d)
    int z12_owner_destroy(Z12OwnerCtx **pp, Z12OwnerDiag *d)
