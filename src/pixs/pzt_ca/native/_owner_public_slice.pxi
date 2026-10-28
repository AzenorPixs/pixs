# Prive Z12 : tranche publique pre-admission, fichier complet prive, observation seule.
# Inclure UNE fois APRES deadline, admin_profile, operator_verify, launch_obs,
# systemd_connection, process_image, manager_unit, owner_context, policy_bytes,
# admin_codec, admin_values, admin_verify, admin_time. Build -D_GNU_SOURCE.
# Preconditions privees : dg vie fixe caller-owned jusqu'a cleanup_all reussi,
# zero avant premier usage, aucun recouvrement out/dg/payload/signature/owner,
# interdiction de copier ou remettre a zero dg tant que pending_cleanup != NULL,
# destruction obligatoire avant owner, jamais free owner/CTX empruntes.
# Zero-init + pending=NULL existants suffisent, aucun helper public ajoute.
from libc.stddef cimport size_t
from libc.stdint cimport uint64_t, uint32_t, int32_t, UINT32_MAX
from libc.string cimport memcpy, memset, memcmp
from libc.errno cimport errno
from posix.types cimport pid_t, uid_t, gid_t, mode_t
from posix.unistd cimport getpid, close

cdef extern from "sys/mman.h" nogil:
    void *MAP_FAILED

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
    #include <sys/mman.h>
    #include <sys/stat.h>
    #include "z12_owner_build.inc"
    static const int Z12_SLICE_PROT_READ = PROT_READ;
    typedef struct {
        size_t policy_max; size_t plan_max; size_t journal_max;
        uint32_t uid32; uint32_t gid32; uint32_t mode32; int fixture;
        size_t identity_len; size_t domain_len; size_t version_len;
    } Z12SliceLimits;
    typedef struct {
        unsigned char policy_sha256[32];
        unsigned char plan_sha256[32];
        unsigned char journal_sha256[32];
        uint64_t epoch_value; uint32_t uid_value; uint32_t gid_value;
        uint32_t mode_value; int fixture_observed;
        uint64_t observed_ns; int valid;
    } Z12SliceObsMeta;
    typedef struct {
        int pfd; int lfd; int jfd; int fds_transferred;
        unsigned char *payload_map; size_t payload_len; int payload_mapped;
        unsigned char *sig_map; size_t sig_len; int sig_mapped;
        Z12PolicyBytes *bytes; Z12OwnerCtx *borrowed;
        pid_t creator_pid; pid_t creator_tid; int cleanup_poisoned;
    } Z12SlicePendingStore;
    typedef struct {
        int invalid_contract; int foreign_binding;
        int deadline_expired; int clock_failed;
        int map_failed; int map_stage; int build_failed;
        int crypto_failed; int crypto_stage;
        int digest_mismatch; int cleanup_errno; int cleanup_map_failed; int map_errno;
        Z12OwnerDiag owner_diag;
        Z12PolicyBytesDiag reader_diag;
        int owner_failure_recorded; int owner_failure_result;
        Z12SlicePendingStore store;
        Z12SlicePendingStore *pending_cleanup;
    } Z12SliceDiag;
    static pid_t z12_slice_gettid(void) { return gettid(); }
    static int z12_slice_build_observe(Z12SliceLimits *lim) {
        static const char expd[] = "pixs.z12.owner.build/v1";
        size_t dexp; uint64_t v; uint32_t u; mode_t m;
        if (lim == NULL) return -2;
        memset(lim, 0, sizeof(*lim));
        dexp = sizeof(expd) - 1;
        if (Z12_OWNER_BUILD_IDENTITY_LEN < 1 || Z12_OWNER_BUILD_IDENTITY_LEN > 256) return 0;
        if (sizeof(Z12_OWNER_BUILD_IDENTITY_BYTES) != (size_t)Z12_OWNER_BUILD_IDENTITY_LEN) return 0;
        if ((size_t)Z12_OWNER_BUILD_DOMAIN_LEN != dexp) return 0;
        if (sizeof(Z12_OWNER_BUILD_DOMAIN_BYTES) != dexp) return 0;
        if (memcmp(Z12_OWNER_BUILD_DOMAIN_BYTES, expd, dexp) != 0) return 0;
        if (Z12_OWNER_BUILD_VERSION_LEN < 1 || Z12_OWNER_BUILD_VERSION_LEN > 256) return 0;
        if (sizeof(Z12_OWNER_BUILD_VERSION_BYTES) != (size_t)Z12_OWNER_BUILD_VERSION_LEN) return 0;
        v = (uint64_t)Z12_OWNER_BUILD_POLICY_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) return 0;
        if (v > (uint64_t)SSIZE_MAX) return 0;
        lim->policy_max = (size_t)v;
        v = (uint64_t)Z12_OWNER_BUILD_PLAN_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) return 0;
        if (v > (uint64_t)SSIZE_MAX) return 0;
        lim->plan_max = (size_t)v;
        v = (uint64_t)Z12_OWNER_BUILD_JOURNAL_MAX;
        if (v < 1 || v > (uint64_t)UINT32_MAX || v >= (uint64_t)SIZE_MAX) return 0;
        if (v > (uint64_t)SSIZE_MAX) return 0;
        lim->journal_max = (size_t)v;
        v = (uint64_t)Z12_OWNER_BUILD_UID;
        if (v > (uint64_t)UINT32_MAX) return 0;
        u = (uint32_t)v;
        { uid_t uu = (uid_t)u; if ((uint32_t)uu != u) return 0; }
        lim->uid32 = u;
        v = (uint64_t)Z12_OWNER_BUILD_GID;
        if (v > (uint64_t)UINT32_MAX) return 0;
        u = (uint32_t)v;
        { gid_t gg = (gid_t)u; if ((uint32_t)gg != u) return 0; }
        lim->gid32 = u;
        v = (uint64_t)Z12_OWNER_BUILD_MODE;
        if (v > 0777) return 0;
        m = (mode_t)(uint32_t)v;
        if (((uint32_t)m & ~0777u) != 0) return 0;
        if (((uint32_t)m & 0400u) == 0) return 0;
        if (((uint32_t)m & 0133u) != 0) return 0;
        if ((uint32_t)m != (uint32_t)v) return 0;
        lim->mode32 = (uint32_t)v;
        if (Z12_OWNER_BUILD_FIXTURE != 0 && Z12_OWNER_BUILD_FIXTURE != 1) return 0;
        lim->fixture = (int)Z12_OWNER_BUILD_FIXTURE;
        lim->identity_len = (size_t)Z12_OWNER_BUILD_IDENTITY_LEN;
        lim->domain_len = dexp;
        lim->version_len = (size_t)Z12_OWNER_BUILD_VERSION_LEN;
        return 1;
    }
    static int z12_slice_store_init(Z12SlicePendingStore *st, Z12OwnerCtx *o) {
        pid_t p; pid_t t;
        if (st == NULL || o == NULL) return -2;
        p = getpid(); t = gettid();
        if (p <= 0 || t <= 0) return -2;
        memset(st, 0, sizeof(*st));
        st->pfd = -1; st->lfd = -1; st->jfd = -1;
        st->borrowed = o;
        st->creator_pid = p; st->creator_tid = t;
        return 1;
    }
    static int z12_slice_drain3(int a, int b, int c, int *cerrno_out) {
        int fds[3]; int uniq[3]; int n = 0; int rc = 0; int se = 0;
        int i; int k;
        fds[0] = a; fds[1] = b; fds[2] = c;
        for (i = 0; i < 3; i++) {
            int fd = fds[i]; int seen = 0;
            if (fd < 0) continue;
            for (k = 0; k < n; k++) if (uniq[k] == fd) { seen = 1; break; }
            if (seen) continue;
            uniq[n++] = fd;
        }
        for (k = 0; k < n; k++) {
            if (close(uniq[k]) != 0) { if (se == 0) se = errno; rc = -1; }
        }
        if (cerrno_out != NULL) *cerrno_out = se;
        return rc;
    }
    static int z12_slice_size_ok(size_t n) {
        if (n == 0 || n == SIZE_MAX) return 0;
        if (n > (size_t)SSIZE_MAX) return 0;
        return 1;
    }
    static int z12_slice_close3_owned(Z12SlicePendingStore *st, int *cerrno_out) {
        int uniq[3]; int n = 0; int rc = 0; int se = 0;
        int i; int k; int fds[3];
        if (st == NULL) return -2;
        if (st->fds_transferred != 0) return 1;
        fds[0] = st->pfd; fds[1] = st->lfd; fds[2] = st->jfd;
        for (i = 0; i < 3; i++) {
            int fd = fds[i]; int seen = 0;
            if (fd < 0) continue;
            for (k = 0; k < n; k++) if (uniq[k] == fd) { seen = 1; break; }
            if (seen) continue;
            uniq[n++] = fd;
        }
        for (k = 0; k < n; k++) {
            int fd = uniq[k];
            if (st->pfd == fd) st->pfd = -1;
            if (st->lfd == fd) st->lfd = -1;
            if (st->jfd == fd) st->jfd = -1;
            if (close(fd) != 0) { if (se == 0) se = errno; rc = -1; }
        }
        st->pfd = -1; st->lfd = -1; st->jfd = -1;
        if (cerrno_out != NULL) *cerrno_out = se;
        return rc;
    }
    static int z12_slice_map_install(Z12SlicePendingStore *st, size_t len, int which) {
        void *m;
        if (st == NULL) return -2;
        if (st->cleanup_poisoned != 0) return -1;
        if (len == 0 || len == SIZE_MAX || len > (size_t)SSIZE_MAX) return -2;
        if (which != 0 && which != 1) return -2;
        if (which == 0 && st->payload_mapped != 0) return -2;
        if (which == 1 && st->sig_mapped != 0) return -2;
        m = mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (m == MAP_FAILED) return -1;
        if (which == 0) { st->payload_map = (unsigned char *)m; st->payload_len = len; st->payload_mapped = 1; }
        else { st->sig_map = (unsigned char *)m; st->sig_len = len; st->sig_mapped = 1; }
        return 1;
    }
    static int z12_slice_protect_ro(Z12SlicePendingStore *st, int which) {
        int r;
        if (st == NULL) return -2;
        if (which == 0) {
            if (!st->payload_mapped) return -2;
            r = mprotect(st->payload_map, st->payload_len, PROT_READ);
        } else if (which == 1) {
            if (!st->sig_mapped) return -2;
            r = mprotect(st->sig_map, st->sig_len, PROT_READ);
        } else return -2;
        if (r != 0) return -1;
        return 1;
    }
    static int z12_slice_unmap_once_inner(unsigned char **pmap, size_t *plen, int *mapped, int *cerrno_out) {
        void *addr; size_t len;
        if (pmap == NULL || plen == NULL || mapped == NULL) return -2;
        if (*mapped == 0) return 1;
        addr = *pmap; len = *plen;
        if (len == 0 || len == SIZE_MAX) return -2;
        if (munmap(addr, len) == 0) { *pmap = NULL; *plen = 0; *mapped = 0; return 1; }
        if (cerrno_out != NULL && *cerrno_out == 0) *cerrno_out = errno;
        return -1;
    }
    static int z12_slice_copy_shas(Z12SlicePendingStore *st, unsigned char out_p[32], unsigned char out_l[32], unsigned char out_j[32]) {
        if (st == NULL || out_p == NULL || out_l == NULL || out_j == NULL) return -2;
        if (st->bytes == NULL || st->bytes->loaded != 1) return -2;
        if (st->creator_pid <= 0 || getpid() != st->creator_pid) return 0;
        memcpy(out_p, st->bytes->policy_sha256, 32);
        memcpy(out_l, st->bytes->plan_sha256, 32);
        memcpy(out_j, st->bytes->journal_sha256, 32);
        return 1;
    }
    static OSSL_LIB_CTX *z12_slice_v_ctx(Z12OwnerCtx *o) { if (o == NULL) return NULL; return o->libctx; }
    static Z12ImageCtx *z12_slice_v_img(Z12OwnerCtx *o) { if (o == NULL) return NULL; return &o->imgctx; }
    static Z12MonotonicDeadline *z12_slice_v_dl(Z12OwnerCtx *o) { if (o == NULL) return NULL; return &o->deadline; }
    static uint64_t z12_slice_v_end(Z12OwnerCtx *o) { if (o == NULL) return 0; return o->expected_end; }
    static int z12_slice_guard_owner(Z12OwnerCtx *o, Z12SliceDiag *dg) {
        Z12OwnerDiag tmp; int r; pid_t p; pid_t t;
        if (o == NULL || dg == NULL) return -2;
        p = getpid(); t = gettid();
        if (p <= 0 || t <= 0) return -2;
        memset(&tmp, 0, sizeof(tmp));
        r = z12_owner_guard(o, &tmp);
        if (tmp.img.native.foreign_binding && !dg->foreign_binding) dg->foreign_binding = 1;
        if (tmp.img.native.deadline_expired && !dg->deadline_expired) dg->deadline_expired = 1;
        if (tmp.img.native.clock_failed && !dg->clock_failed) dg->clock_failed = 1;
        if (tmp.invalid_contract && !dg->invalid_contract) dg->invalid_contract = 1;
        if (r != 1 && dg->owner_failure_recorded == 0) {
            memcpy(&dg->owner_diag, &tmp, sizeof(tmp));
            dg->owner_failure_recorded = 1;
            dg->owner_failure_result = r;
        }
        return r;
    }
    static int z12_slice_check_deadline(Z12OwnerCtx *o, Z12SliceDiag *dg) {
        Z12SysdDiag t2; int r;
        if (o == NULL || dg == NULL) return -2;
        memset(&t2, 0, sizeof(t2));
        r = z12_sysd_deadline(&o->deadline, o->expected_end, &t2);
        if (t2.foreign_binding && !dg->foreign_binding) dg->foreign_binding = 1;
        if (t2.deadline_expired && !dg->deadline_expired) dg->deadline_expired = 1;
        if (t2.clock_failed && !dg->clock_failed) dg->clock_failed = 1;
        return r;
    }
    static int z12_slice_cleanup_all(Z12SliceDiag *dg, Z12SliceObsMeta *out) {
        int ce = 0; int u;
        if (dg == NULL) return -2;
        if (dg->store.creator_pid <= 0 || dg->store.creator_tid <= 0) return -2;
        if (getpid() != dg->store.creator_pid || gettid() != dg->store.creator_tid) {
            if (!dg->foreign_binding) dg->foreign_binding = 1;
            if (out != NULL) memset(out, 0, sizeof(*out));
            return 0;
        }
        if (out != NULL) memset(out, 0, sizeof(*out));
        if (dg->store.cleanup_poisoned != 0) return -1;
        if (dg->pending_cleanup != &dg->store && dg->pending_cleanup != NULL) {
            if (!dg->invalid_contract) dg->invalid_contract = 1;
            return -2;
        }
        if (dg->pending_cleanup == NULL) return 1;
        if (dg->store.fds_transferred == 0) {
            u = z12_slice_close3_owned(&dg->store, &ce);
            if (u != 0) { if (!dg->cleanup_errno) dg->cleanup_errno = ce; }
        }
        if (dg->store.bytes != NULL) z12_policy_bytes_destroy(&dg->store.bytes);
        u = z12_slice_unmap_once_inner(&dg->store.payload_map, &dg->store.payload_len, &dg->store.payload_mapped, &dg->cleanup_errno);
        if (u != 1) { dg->cleanup_map_failed = 1; dg->store.cleanup_poisoned = 1; return -1; }
        u = z12_slice_unmap_once_inner(&dg->store.sig_map, &dg->store.sig_len, &dg->store.sig_mapped, &dg->cleanup_errno);
        if (u != 1) { dg->cleanup_map_failed = 1; dg->store.cleanup_poisoned = 1; return -1; }
        dg->store.pfd = -1; dg->store.lfd = -1; dg->store.jfd = -1;
        dg->pending_cleanup = NULL;
        return (dg->cleanup_errno != 0) ? -1 : 1;
    }
    """
    ctypedef struct Z12SliceLimits:
        size_t policy_max
        size_t plan_max
        size_t journal_max
        uint32_t uid32
        uint32_t gid32
        uint32_t mode32
        int fixture
        size_t identity_len
        size_t domain_len
        size_t version_len
    ctypedef struct Z12SliceObsMeta:
        unsigned char policy_sha256[32]
        unsigned char plan_sha256[32]
        unsigned char journal_sha256[32]
        uint64_t epoch_value
        uint32_t uid_value
        uint32_t gid_value
        uint32_t mode_value
        int fixture_observed
        uint64_t observed_ns
        int valid
    ctypedef struct Z12SlicePendingStore:
        int pfd
        int lfd
        int jfd
        int fds_transferred
        unsigned char *payload_map
        size_t payload_len
        int payload_mapped
        unsigned char *sig_map
        size_t sig_len
        int sig_mapped
        Z12PolicyBytes *bytes
        Z12OwnerCtx *borrowed
        pid_t creator_pid
        pid_t creator_tid
        int cleanup_poisoned
    ctypedef struct Z12SliceDiag:
        int invalid_contract
        int foreign_binding
        int deadline_expired
        int clock_failed
        int map_failed
        int map_stage
        int build_failed
        int crypto_failed
        int crypto_stage
        int digest_mismatch
        int cleanup_errno
        int cleanup_map_failed
        int map_errno
        Z12OwnerDiag owner_diag
        Z12PolicyBytesDiag reader_diag
        int owner_failure_recorded
        int owner_failure_result
        Z12SlicePendingStore store
        Z12SlicePendingStore *pending_cleanup
    pid_t z12_slice_gettid()
    int z12_slice_build_observe(Z12SliceLimits *lim)
    int z12_slice_store_init(Z12SlicePendingStore *st, Z12OwnerCtx *o)
    int z12_slice_drain3(int a, int b, int c, int *cerrno_out)
    int z12_slice_size_ok(size_t n)
    int z12_slice_close3_owned(Z12SlicePendingStore *st, int *cerrno_out)
    int z12_slice_map_install(Z12SlicePendingStore *st, size_t len, int which)
    int z12_slice_protect_ro(Z12SlicePendingStore *st, int which)
    int z12_slice_unmap_once_inner(unsigned char **pmap, size_t *plen, int *mapped, int *cerrno_out)
    int z12_slice_copy_shas(Z12SlicePendingStore *st, unsigned char out_p[32], unsigned char out_l[32], unsigned char out_j[32])
    OSSL_LIB_CTX *z12_slice_v_ctx(Z12OwnerCtx *o)
    Z12ImageCtx *z12_slice_v_img(Z12OwnerCtx *o)
    Z12MonotonicDeadline *z12_slice_v_dl(Z12OwnerCtx *o)
    uint64_t z12_slice_v_end(Z12OwnerCtx *o)
    int z12_slice_guard_owner(Z12OwnerCtx *o, Z12SliceDiag *dg)
    int z12_slice_check_deadline(Z12OwnerCtx *o, Z12SliceDiag *dg)
    int z12_slice_cleanup_all(Z12SliceDiag *dg, Z12SliceObsMeta *out)

cdef int _slice_hex_of(const unsigned char *raw32, char *hex64) noexcept nogil:
    cdef size_t i
    cdef size_t n
    cdef unsigned char v
    cdef unsigned char hi
    cdef unsigned char lo
    if raw32 == NULL or hex64 == NULL:
        return -2
    i = 0
    n = 32
    while i < n:
        v = raw32[i]
        hi = (v >> 4) & 0xF
        lo = v & 0xF
        hex64[i * 2] = <char>(48 + hi if hi < 10 else 87 + hi)
        hex64[i * 2 + 1] = <char>(48 + lo if lo < 10 else 87 + lo)
        i = i + 1
    return 1

cdef int _slice_norm_crypto(int r, Z12SliceDiag *dg, int stage) noexcept nogil:
    if dg == NULL:
        return -2
    if r == 1 or r == 0:
        return r
    if r == -2:
        dg.invalid_contract = 1
        return -2
    if r == -1:
        dg.clock_failed = 1
        return -1
    if r == -3:
        dg.deadline_expired = 1
        return 0
    if r == -4:
        dg.crypto_failed = 1
        if dg.crypto_stage == 0:
            dg.crypto_stage = stage
        return -1
    dg.crypto_failed = 1
    if dg.crypto_stage == 0:
        dg.crypto_stage = stage
    return -1

cdef int _slice_copy_into(Z12SlicePendingStore *st, int which, const unsigned char *src, size_t n) noexcept nogil:
    cdef int saved
    cdef unsigned char *dst
    cdef size_t cap
    if st == NULL or src == NULL:
        return -2
    if which == 0:
        dst = st.payload_map
        cap = st.payload_len
        if st.payload_mapped == 0 or dst == NULL:
            return -2
    elif which == 1:
        dst = st.sig_map
        cap = st.sig_len
        if st.sig_mapped == 0 or dst == NULL:
            return -2
    else:
        return -2
    if n == 0 or n != cap:
        return -2
    saved = errno
    memcpy(dst, src, n)
    errno = saved
    return 1

cdef int _slice_protect_one(Z12SlicePendingStore *st, int which) noexcept nogil:
    if st == NULL:
        return -2
    if which != 0 and which != 1:
        return -2
    return z12_slice_protect_ro(st, which)

cdef int _slice_core(Z12OwnerCtx *owner, int pfd0, size_t plen0, int lfd0, size_t llen0, int jfd0, size_t jlen0, const unsigned char *payload, size_t payload_len, const unsigned char *signature, Z12SliceObsMeta *out, Z12SliceDiag *dg) noexcept nogil:
    cdef Z12SliceLimits lim
    cdef Z12AdminView av
    cdef OSSL_LIB_CTX *lc
    cdef Z12ImageCtx *img
    cdef Z12MonotonicDeadline *dl
    cdef uint64_t endv
    cdef int32_t to
    cdef _AdminFramed fr
    cdef _AdminValues va
    cdef _AdminTime ti
    cdef int op
    cdef int gr
    cdef int eafter
    cdef Z12PolicyBytes *b
    cdef char phe[64]
    cdef char plh[64]
    cdef unsigned char rp[32]
    cdef unsigned char rl[32]
    cdef unsigned char rj[32]
    memset(&lim, 0, sizeof(lim))
    memset(&av, 0, sizeof(av))
    memset(&fr, 0, sizeof(fr))
    memset(&va, 0, sizeof(va))
    memset(&ti, 0, sizeof(ti))
    memset(phe, 0, sizeof(phe))
    memset(plh, 0, sizeof(plh))
    memset(rp, 0, sizeof(rp))
    memset(rl, 0, sizeof(rl))
    memset(rj, 0, sizeof(rj))
    lc = NULL
    img = NULL
    dl = NULL
    endv = 0
    to = 0
    b = NULL
    op = -2
    gr = -2
    eafter = 0
    op = z12_slice_guard_owner(owner, dg)
    if op != 1:
        return op
    op = z12_slice_check_deadline(owner, dg)
    if op != 1:
        return op
    op = _admin_profile_observe(&av)
    if op != 1:
        return -2
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    if payload == NULL or signature == NULL:
        dg.invalid_contract = 1
        return -2
    if z12_slice_size_ok(payload_len) == 0:
        dg.invalid_contract = 1
        return -2
    if payload_len > av.max_payload_len:
        return 0
    op = z12_slice_build_observe(&lim)
    if op != 1:
        dg.build_failed = 1
        return op
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    if z12_slice_size_ok(plen0) == 0 or z12_slice_size_ok(llen0) == 0 or z12_slice_size_ok(jlen0) == 0:
        dg.invalid_contract = 1
        return -2
    if plen0 > lim.policy_max or llen0 > lim.plan_max or jlen0 > lim.journal_max:
        return 0
    lc = z12_slice_v_ctx(owner)
    img = z12_slice_v_img(owner)
    dl = z12_slice_v_dl(owner)
    endv = z12_slice_v_end(owner)
    if lc == NULL or img == NULL or dl == NULL or endv == 0:
        dg.invalid_contract = 1
        return -2
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    op = z12_slice_map_install(&dg.store, payload_len, 0)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op == -2:
        dg.invalid_contract = 1
        return -2
    if op != 1:
        dg.map_failed = 1
        if dg.map_stage == 0:
            dg.map_stage = 30
        if dg.map_errno == 0:
            dg.map_errno = eafter
        return -1
    if gr != 1:
        return gr
    op = z12_slice_map_install(&dg.store, 64, 1)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op == -2:
        dg.invalid_contract = 1
        return -2
    if op != 1:
        dg.map_failed = 1
        if dg.map_stage == 0:
            dg.map_stage = 31
        if dg.map_errno == 0:
            dg.map_errno = eafter
        return -1
    if gr != 1:
        return gr
    if dg.store.payload_map == NULL or dg.store.sig_map == NULL:
        dg.invalid_contract = 1
        return -2
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    op = _slice_copy_into(&dg.store, 0, payload, payload_len)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op != 1:
        dg.invalid_contract = 1
        return -2
    if gr != 1:
        return gr
    op = _slice_protect_one(&dg.store, 0)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op != 1:
        dg.map_failed = 1
        if dg.map_stage == 0:
            dg.map_stage = 32
        if dg.map_errno == 0:
            dg.map_errno = eafter
        return -1
    if gr != 1:
        return gr
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    op = _slice_copy_into(&dg.store, 1, signature, 64)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op != 1:
        dg.invalid_contract = 1
        return -2
    if gr != 1:
        return gr
    op = _slice_protect_one(&dg.store, 1)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op != 1:
        dg.map_failed = 1
        if dg.map_stage == 0:
            dg.map_stage = 33
        if dg.map_errno == 0:
            dg.map_errno = eafter
        return -1
    if gr != 1:
        return gr
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    dg.store.fds_transferred = 1
    dg.store.pfd = -1
    dg.store.lfd = -1
    dg.store.jfd = -1
    memset(&dg.reader_diag, 0, sizeof(dg.reader_diag))
    op = z12_policy_bytes_load_with_ctx(lc, pfd0, plen0, lim.policy_max, lfd0, llen0, lim.plan_max, jfd0, jlen0, lim.journal_max, <uid_t>lim.uid32, <gid_t>lim.gid32, <mode_t>lim.mode32, img, dl, endv, &b, &dg.reader_diag)
    eafter = errno
    if op == 1:
        if b == NULL:
            dg.invalid_contract = 1
            return -2
        dg.store.bytes = b
        b = NULL
    gr = z12_slice_guard_owner(owner, dg)
    if op != 1:
        if op == 0:
            return 0
        return -1 if op == -1 else op
    if gr != 1:
        return gr
    op = z12_slice_guard_owner(owner, dg)
    if op != 1:
        return op
    op = z12_slice_check_deadline(owner, dg)
    if op != 1:
        return op
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    op = _admin_verify_signed(_ADMIN_KIND_PREPUBLICATION, dg.store.payload_map, payload_len, dg.store.sig_map, 64, lc, dl, &to, &fr)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    op = _slice_norm_crypto(op, dg, 20)
    if op != 1:
        return op
    if gr != 1:
        return gr
    op = _admin_values_observe(_ADMIN_KIND_PREPUBLICATION, dg.store.payload_map, payload_len, dl, &to, &va)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    op = _slice_norm_crypto(op, dg, 21)
    if op != 1:
        return op
    if gr != 1:
        return gr
    op = _admin_time_observe(_ADMIN_KIND_PREPUBLICATION, dg.store.payload_map, payload_len, dl, &to, &ti)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    op = _slice_norm_crypto(op, dg, 22)
    if op != 1:
        return op
    if gr != 1:
        return gr
    if fr.count != 15:
        return 0
    op = z12_slice_copy_shas(&dg.store, rp, rl, rj)
    eafter = errno
    gr = z12_slice_guard_owner(owner, dg)
    if op != 1:
        if op == -2:
            dg.invalid_contract = 1
            return -2
        dg.digest_mismatch = 1
        return 0
    if gr != 1:
        return gr
    if _slice_hex_of(rp, phe) != 1 or _slice_hex_of(rl, plh) != 1:
        dg.invalid_contract = 1
        return -2
    gr = z12_slice_guard_owner(owner, dg)
    if gr != 1:
        return gr
    if fr.fields[8].length != 64 or memcmp(fr.fields[8].ptr, phe, 64) != 0:
        dg.digest_mismatch = 1
        return 0
    if fr.fields[11].length != 64 or memcmp(fr.fields[11].ptr, plh, 64) != 0:
        dg.digest_mismatch = 1
        return 0
    op = z12_slice_guard_owner(owner, dg)
    if op != 1:
        return op
    op = z12_slice_check_deadline(owner, dg)
    if op != 1:
        return op
    memcpy(out.policy_sha256, rp, 32)
    memcpy(out.plan_sha256, rl, 32)
    memcpy(out.journal_sha256, rj, 32)
    out.epoch_value = va.epoch_value
    out.uid_value = lim.uid32
    out.gid_value = lim.gid32
    out.mode_value = lim.mode32
    out.fixture_observed = lim.fixture
    out.observed_ns = dl.last_seen_ns
    op = z12_slice_guard_owner(owner, dg)
    if op != 1:
        memset(out, 0, sizeof(Z12SliceObsMeta))
        return op
    op = z12_slice_check_deadline(owner, dg)
    if op != 1:
        memset(out, 0, sizeof(Z12SliceObsMeta))
        return op
    out.valid = 1
    return 1

cdef int z12_slice_observe_prepub(Z12OwnerCtx *owner, int pfd, size_t plen, int lfd, size_t llen, int jfd, size_t jlen, const unsigned char *payload, size_t payload_len, const unsigned char *signature, size_t sig_len, Z12SliceObsMeta *out, Z12SliceDiag *dg) noexcept nogil:
    cdef int dr
    cdef int cerr
    cdef int op
    cdef int cr
    if out != NULL:
        memset(out, 0, sizeof(Z12SliceObsMeta))
    if owner == NULL or out == NULL or dg == NULL:
        cerr = 0
        dr = z12_slice_drain3(pfd, lfd, jfd, &cerr)
        if dg != NULL and dg.pending_cleanup == NULL:
            dg.invalid_contract = 1
            if cerr != 0 and dg.cleanup_errno == 0:
                dg.cleanup_errno = cerr
        return -1 if dr != 0 else (-2)
    if dg.pending_cleanup != NULL:
        cerr = 0
        dr = z12_slice_drain3(pfd, lfd, jfd, &cerr)
        dg.invalid_contract = 1
        if cerr != 0 and dg.cleanup_errno == 0:
            dg.cleanup_errno = cerr
        return -1 if dr != 0 else (-2)
    if payload == NULL or signature == NULL:
        cerr = 0
        dr = z12_slice_drain3(pfd, lfd, jfd, &cerr)
        dg.invalid_contract = 1
        if cerr != 0 and dg.cleanup_errno == 0:
            dg.cleanup_errno = cerr
        return -1 if dr != 0 else (-2)
    if sig_len != 64:
        cerr = 0
        dr = z12_slice_drain3(pfd, lfd, jfd, &cerr)
        if cerr != 0 and dg.cleanup_errno == 0:
            dg.cleanup_errno = cerr
        return -1 if dr != 0 else 0
    memset(dg, 0, sizeof(Z12SliceDiag))
    memset(out, 0, sizeof(Z12SliceObsMeta))
    dg.pending_cleanup = NULL
    if z12_slice_store_init(&dg.store, owner) != 1:
        cerr = 0
        dr = z12_slice_drain3(pfd, lfd, jfd, &cerr)
        dg.invalid_contract = 1
        if cerr != 0 and dg.cleanup_errno == 0:
            dg.cleanup_errno = cerr
        return -1 if dr != 0 else (-2)
    if pfd < 0 or lfd < 0 or jfd < 0 or pfd == lfd or pfd == jfd or lfd == jfd:
        cerr = 0
        dr = z12_slice_drain3(pfd, lfd, jfd, &cerr)
        dg.invalid_contract = 1
        if cerr != 0 and dg.cleanup_errno == 0:
            dg.cleanup_errno = cerr
        dg.store.pfd = -1
        dg.store.lfd = -1
        dg.store.jfd = -1
        return -1 if dr != 0 else (-2)
    dg.store.pfd = pfd
    dg.store.lfd = lfd
    dg.store.jfd = jfd
    dg.store.fds_transferred = 0
    dg.pending_cleanup = &dg.store
    op = _slice_core(owner, pfd, plen, lfd, llen, jfd, jlen, payload, payload_len, signature, out, dg)
    if op == 1:
        return 1
    memset(out, 0, sizeof(Z12SliceObsMeta))
    cr = z12_slice_cleanup_all(dg, out)
    if cr != 1:
        return -1
    return op
