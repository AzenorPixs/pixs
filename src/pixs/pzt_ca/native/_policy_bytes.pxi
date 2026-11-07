# Prive Z12 : lecteur octets publics politique/plan/journal, sans admission.
# Inclure UNE fois apres _monotonic_deadline, _launch_obs_sysd, _systemd_connection, _process_image ; build -D_GNU_SOURCE.
# FD transferes exclusifs, tailles/limites/UID/GID/mode du plan, owner/deadline/end deja demarres.
from libc.stddef cimport size_t
from libc.stdint cimport uint64_t
from posix.types cimport uid_t, gid_t
from posix.types cimport mode_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <fcntl.h>
    #include <limits.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <sys/stat.h>
    #include <sys/types.h>
    #include <unistd.h>
    #include <openssl/crypto.h>
    #include <openssl/evp.h>
    typedef struct {
        unsigned char *policy_addr; size_t policy_len; unsigned char policy_sha256[32];
        dev_t policy_dev; ino_t policy_ino; uid_t policy_uid; gid_t policy_gid; mode_t policy_mode; nlink_t policy_nlink; off_t policy_size; struct timespec policy_mtim_before; struct timespec policy_mtim_after; struct timespec policy_ctim_before; struct timespec policy_ctim_after;
        unsigned char *plan_addr; size_t plan_len; unsigned char plan_sha256[32];
        dev_t plan_dev; ino_t plan_ino; uid_t plan_uid; gid_t plan_gid; mode_t plan_mode; nlink_t plan_nlink; off_t plan_size; struct timespec plan_mtim_before; struct timespec plan_mtim_after; struct timespec plan_ctim_before; struct timespec plan_ctim_after;
        unsigned char *journal_addr; size_t journal_len; unsigned char journal_sha256[32];
        dev_t journal_dev; ino_t journal_ino; uid_t journal_uid; gid_t journal_gid; mode_t journal_mode; nlink_t journal_nlink; off_t journal_size; struct timespec journal_mtim_before; struct timespec journal_mtim_after; struct timespec journal_ctim_before; struct timespec journal_ctim_after;
        pid_t creator_pid;
        Z12ImageCtx *owner;
        Z12MonotonicDeadline *deadline;
        uint64_t end_ns;
        uint64_t observed_ns;
        int loaded;
    } Z12PolicyBytes;
    typedef struct {
        Z12ProcessImageDiag img;
        int invalid_contract;
    } Z12PolicyBytesDiag;
    static int z12_pb_guard(Z12ImageCtx *o, Z12MonotonicDeadline *d, uint64_t end, Z12PolicyBytesDiag *dg) {
        if (o == NULL || d == NULL || dg == NULL) return -2;
        if (d != o->deadline) { dg->img.native.foreign_binding = 1; return 0; }
        if (end != o->end) { dg->img.native.foreign_binding = 1; return 0; }
        return z12_image_guard(o, &dg->img);
    }
    static int z12_pb_stat(int fd, uid_t u, gid_t g, mode_t m, size_t el, struct stat *st) {
        int fl, seals;
        if (fstat(fd, st) != 0) return -1;
        if (!S_ISREG(st->st_mode)) return 0;
        if (st->st_size < 0 || (uintmax_t)st->st_size != (uintmax_t)el) return 0;
        if (st->st_uid != u || st->st_gid != g) return 0;
        if ((st->st_mode & 07777) != m) return 0;
        fl = fcntl(fd, F_GETFD);
        if (fl < 0) return -1;
        if ((fl & FD_CLOEXEC) == 0) return 0;
        fl = fcntl(fd, F_GETFL);
        if (fl < 0) return -1;
#ifdef O_PATH
        if ((fl & O_PATH) != 0) return 0;
#endif
        if ((fl & O_ACCMODE) != O_RDONLY) return 0;
        seals = fcntl(fd, F_GET_SEALS);
        if (seals >= 0) {
            const int req = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL;
            if ((seals & req) != req) return 0;
        } else {
            if (errno != EINVAL && errno != ENOTTY) return -1;
        }
        return 1;
    }
    static int z12_pb_same(const struct stat *a, const struct stat *b) {
        if (a->st_dev != b->st_dev || a->st_ino != b->st_ino) return 0;
        if (a->st_uid != b->st_uid || a->st_gid != b->st_gid) return 0;
        if ((a->st_mode & 07777) != (b->st_mode & 07777)) return 0;
        if (a->st_nlink != b->st_nlink) return 0;
        if (a->st_size != b->st_size) return 0;
        if (a->st_mtim.tv_sec != b->st_mtim.tv_sec || a->st_mtim.tv_nsec != b->st_mtim.tv_nsec) return 0;
        if (a->st_ctim.tv_sec != b->st_ctim.tv_sec || a->st_ctim.tv_nsec != b->st_ctim.tv_nsec) return 0;
        return 1;
    }
    static int z12_pb_close_unique(int fds[3], Z12PolicyBytesDiag *dg) {
        int uniq[3]; int n = 0; int rc = 0; int se = 0;
        for (int i = 0; i < 3; i++) {
            int fd = fds[i];
            int seen = 0;
            if (fd < 0) continue;
            for (int k = 0; k < n; k++) if (uniq[k] == fd) { seen = 1; break; }
            if (seen) continue;
            uniq[n++] = fd;
        }
        for (int k = 0; k < n; k++) {
            int fd = uniq[k];
            for (int i = 0; i < 3; i++) if (fds[i] == fd) fds[i] = -1;
            if (close(fd) != 0) {
                if (se == 0) se = errno;
                rc = -1;
            }
        }
        if (rc != 0 && dg != NULL) {
            if (dg->img.native.cleanup_errno == 0) dg->img.native.cleanup_errno = se;
            dg->img.native.must_destroy_bus = 1;
        }
        return rc;
    }
    static int z12_pb_read_exact(int fd, unsigned char *dst, size_t el, Z12ImageCtx *o, Z12MonotonicDeadline *d, uint64_t end, Z12PolicyBytesDiag *dg) {
        size_t done = 0;
        int r = z12_pb_guard(o, d, end, dg);
        if (r != 1) return r;
        while (done < el) {
            ssize_t got;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) return r;
            got = pread(fd, dst + done, el - done, (off_t)done);
            if (got < 0) { z12_sysd_first(&dg->img.native, Z12_SYSD_ERRNO, errno); return -1; }
            if (got == 0 || (size_t)got > el - done) return 0;
            done += (size_t)got;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) return r;
        }
        {
            unsigned char one = 0;
            ssize_t got;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) return r;
            got = pread(fd, &one, 1, (off_t)el);
            if (got < 0) { z12_sysd_first(&dg->img.native, Z12_SYSD_ERRNO, errno); return -1; }
            if (got != 0) return 0;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) return r;
        }
        return 1;
    }
    static int z12_pb_sha256(unsigned char *data, size_t el, unsigned char out32[32], Z12ImageCtx *o, Z12MonotonicDeadline *d, uint64_t end, Z12PolicyBytesDiag *dg) {
        OSSL_LIB_CTX *lc = NULL;
        EVP_MD *md = NULL;
        EVP_MD_CTX *mc = NULL;
        size_t off = 0;
        int r;
        lc = OSSL_LIB_CTX_new();
        if (lc == NULL) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 1; return -1; }
        md = EVP_MD_fetch(lc, "SHA256", "provider=default");
        if (md == NULL || EVP_MD_get_size(md) != 32) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 2; r = -1; goto done; }
        mc = EVP_MD_CTX_new();
        if (mc == NULL) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 3; r = -1; goto done; }
        if (EVP_DigestInit_ex2(mc, md, NULL) != 1) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 4; dg->img.openssl_code = 0; r = -1; goto done; }
        while (off < el) {
            size_t chunk = el - off > 4096 ? 4096 : el - off;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) goto done;
            if (EVP_DigestUpdate(mc, data + off, chunk) != 1) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 5; r = -1; goto done; }
            off += chunk;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) goto done;
        }
        {
            unsigned int sl = 0;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) goto done;
            if (EVP_DigestFinal_ex(mc, out32, &sl) != 1 || sl != 32) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 6; r = -1; goto done; }
        }
        r = 1;
    done:
        if (mc != NULL) EVP_MD_CTX_free(mc);
        if (md != NULL) EVP_MD_free(md);
        if (lc != NULL) OSSL_LIB_CTX_free(lc);
        return r;
    }
    static int z12_pb_sha256_with_ctx(OSSL_LIB_CTX *libctx, unsigned char *data, size_t el, unsigned char out32[32], Z12ImageCtx *o, Z12MonotonicDeadline *d, uint64_t end, Z12PolicyBytesDiag *dg) {
        EVP_MD *md = NULL;
        EVP_MD_CTX *mc = NULL;
        unsigned char local[32] = {0};
        size_t off = 0;
        int r;
        int gr;
        int crypto_rc = 1;
        int guard_err = 1;
        int digest_done = 0;
        int size_ret = -1;
        if (libctx == NULL || data == NULL || out32 == NULL || o == NULL || d == NULL || dg == NULL) {
            if (out32 != NULL) memset(out32, 0, 32);
            if (dg != NULL) dg->invalid_contract = 1;
            return -2;
        }
        if (el == 0) {
            memset(out32, 0, 32);
            dg->invalid_contract = 1;
            return -2;
        }
        memset(out32, 0, 32);
        memset(local, 0, sizeof(local));
        r = z12_pb_guard(o, d, end, dg);
        if (r != 1) {
            if (guard_err == 1) guard_err = r;
            goto done_ctx;
        }
        md = EVP_MD_fetch(libctx, "SHA256", "provider=default");
        if (md != NULL) size_ret = EVP_MD_get_size(md);
        else size_ret = -1;
        gr = z12_pb_guard(o, d, end, dg);
        if (gr != 1) {
            if (guard_err == 1) guard_err = gr;
        }
        if (md == NULL || size_ret != 32) {
            if (!dg->img.openssl_failed) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 2; }
            crypto_rc = -1;
            goto done_ctx;
        }
        if (gr != 1) goto done_ctx;
        mc = EVP_MD_CTX_new();
        gr = z12_pb_guard(o, d, end, dg);
        if (gr != 1) {
            if (guard_err == 1) guard_err = gr;
        }
        if (mc == NULL) {
            if (!dg->img.openssl_failed) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 3; }
            crypto_rc = -1;
            goto done_ctx;
        }
        if (gr != 1) goto done_ctx;
        {
            int ok_init = EVP_DigestInit_ex2(mc, md, NULL);
            gr = z12_pb_guard(o, d, end, dg);
            if (gr != 1) {
                if (guard_err == 1) guard_err = gr;
            }
            if (ok_init != 1) {
                if (!dg->img.openssl_failed) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 4; dg->img.openssl_code = 0; }
                crypto_rc = -1;
                goto done_ctx;
            }
            if (gr != 1) goto done_ctx;
        }
        while (off < el) {
            size_t chunk = el - off > 4096 ? 4096 : el - off;
            int ok_upd;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) {
                if (guard_err == 1) guard_err = r;
                goto done_ctx;
            }
            ok_upd = EVP_DigestUpdate(mc, data + off, chunk);
            gr = z12_pb_guard(o, d, end, dg);
            if (gr != 1) {
                if (guard_err == 1) guard_err = gr;
            }
            if (ok_upd != 1) {
                if (!dg->img.openssl_failed) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 5; }
                crypto_rc = -1;
                goto done_ctx;
            }
            if (gr != 1) goto done_ctx;
            off += chunk;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) {
                if (guard_err == 1) guard_err = r;
                goto done_ctx;
            }
        }
        {
            unsigned int sl = 0;
            int ok_fin;
            r = z12_pb_guard(o, d, end, dg);
            if (r != 1) {
                if (guard_err == 1) guard_err = r;
                goto done_ctx;
            }
            ok_fin = EVP_DigestFinal_ex(mc, local, &sl);
            gr = z12_pb_guard(o, d, end, dg);
            if (gr != 1) {
                if (guard_err == 1) guard_err = gr;
            }
            if (ok_fin != 1 || sl != 32) {
                if (!dg->img.openssl_failed) { dg->img.openssl_failed = 1; dg->img.openssl_stage = 6; }
                crypto_rc = -1;
                goto done_ctx;
            }
            if (gr != 1) goto done_ctx;
            digest_done = 1;
        }
    done_ctx:
        if (mc != NULL) EVP_MD_CTX_free(mc);
        if (md != NULL) EVP_MD_free(md);
        mc = NULL; md = NULL;
        r = z12_pb_guard(o, d, end, dg);
        if (r != 1) {
            if (guard_err == 1) guard_err = r;
        }
        if (crypto_rc != 1) {
            memset(out32, 0, 32);
            explicit_bzero(local, sizeof(local));
            return -1;
        }
        if (guard_err != 1) {
            memset(out32, 0, 32);
            explicit_bzero(local, sizeof(local));
            return guard_err;
        }
        if (!digest_done) {
            memset(out32, 0, 32);
            explicit_bzero(local, sizeof(local));
            return -1;
        }
        if (r != 1) {
            memset(out32, 0, 32);
            explicit_bzero(local, sizeof(local));
            return r;
        }
        memcpy(out32, local, 32);
        explicit_bzero(local, sizeof(local));
        r = z12_pb_guard(o, d, end, dg);
        if (r != 1) {
            memset(out32, 0, 32);
            return r;
        }
        return 1;
    }
    static int z12_policy_bytes_destroy(Z12PolicyBytes **owned) {
        Z12PolicyBytes *b;
        if (owned == NULL) return -2;
        b = *owned;
        if (b == NULL) return 1;
        b->loaded = 0;
        if (b->policy_addr != NULL) { explicit_bzero(b->policy_addr, b->policy_len); free(b->policy_addr); }
        if (b->plan_addr != NULL) { explicit_bzero(b->plan_addr, b->plan_len); free(b->plan_addr); }
        if (b->journal_addr != NULL) { explicit_bzero(b->journal_addr, b->journal_len); free(b->journal_addr); }
        explicit_bzero(b, sizeof(*b));
        free((void *)b);
        *owned = NULL;
        return 1;
    }
    static int z12_policy_bytes_load_inner(int pfd, size_t plen, size_t plim, int lfd, size_t llen, size_t llim, int jfd, size_t jlen, size_t jlim, uid_t uid, gid_t gid, mode_t mode, Z12ImageCtx *owner, Z12MonotonicDeadline *deadline, uint64_t end, Z12PolicyBytes **out, Z12PolicyBytesDiag *diag, OSSL_LIB_CTX *borrowed, int use_borrowed) {
        int fds[3];
        int r = -2;
        int primary = -2;
        Z12PolicyBytes *b = NULL;
        struct stat pst0, pst1, lst0, lst1, jst0, jst1;
        off_t off;
        if (diag != NULL) memset(diag, 0, sizeof(*diag));
        fds[0] = pfd; fds[1] = lfd; fds[2] = jfd;
        if (out == NULL || diag == NULL || owner == NULL || deadline == NULL) {
            if (diag != NULL) diag->invalid_contract = 1;
            primary = -2;
            goto finish;
        }
        if (*out != NULL) { diag->invalid_contract = 1; primary = -2; goto finish; }
        if (pfd < 0 || lfd < 0 || jfd < 0) { diag->invalid_contract = 1; primary = -2; goto finish; }
        if (pfd == lfd || pfd == jfd || lfd == jfd) { diag->invalid_contract = 1; primary = -2; goto finish; }
        if (plen == 0 || llen == 0 || jlen == 0 || plen > plim || llen > llim || jlen > jlim) { diag->invalid_contract = 1; primary = -2; goto finish; }
        if (plen > (size_t)SSIZE_MAX || llen > (size_t)SSIZE_MAX || jlen > (size_t)SSIZE_MAX) { diag->invalid_contract = 1; primary = -2; goto finish; }
        off = (off_t)plen; if (off <= 0 || (uintmax_t)off != (uintmax_t)plen) { diag->invalid_contract = 1; primary = -2; goto finish; }
        off = (off_t)llen; if (off <= 0 || (uintmax_t)off != (uintmax_t)llen) { diag->invalid_contract = 1; primary = -2; goto finish; }
        off = (off_t)jlen; if (off <= 0 || (uintmax_t)off != (uintmax_t)jlen) { diag->invalid_contract = 1; primary = -2; goto finish; }
        if (deadline != owner->deadline || end != owner->end) { diag->img.native.foreign_binding = 1; primary = 0; goto finish; }
        if (use_borrowed != 0 && use_borrowed != 1) { diag->invalid_contract = 1; primary = -2; goto finish; }
        if (use_borrowed == 1 && borrowed == NULL) { diag->invalid_contract = 1; primary = -2; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_stat(pfd, uid, gid, mode, plen, &pst0);
        if (r < 0) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = (r == 1) ? -1 : r; goto finish; }
        if (r == 0) { primary = 0; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_stat(lfd, uid, gid, mode, llen, &lst0);
        if (r < 0) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = (r == 1) ? -1 : r; goto finish; }
        if (r == 0) { primary = 0; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_stat(jfd, uid, gid, mode, jlen, &jst0);
        if (r < 0) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = (r == 1) ? -1 : r; goto finish; }
        if (r == 0) { primary = 0; goto finish; }
        b = (Z12PolicyBytes *)calloc(1, sizeof(*b));
        if (b == NULL) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = -1; goto finish; }
        b->policy_len = plen; b->plan_len = llen; b->journal_len = jlen;
        b->policy_addr = NULL; b->plan_addr = NULL; b->journal_addr = NULL;
        b->owner = owner; b->deadline = deadline; b->end_ns = end;
        b->policy_addr = (unsigned char *)malloc(plen ? plen : 1);
        if (b->policy_addr == NULL) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = -1; goto finish; }
        b->plan_addr = (unsigned char *)malloc(llen ? llen : 1);
        if (b->plan_addr == NULL) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = -1; goto finish; }
        b->journal_addr = (unsigned char *)malloc(jlen ? jlen : 1);
        if (b->journal_addr == NULL) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = -1; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_read_exact(pfd, b->policy_addr, plen, owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_read_exact(lfd, b->plan_addr, llen, owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_read_exact(jfd, b->journal_addr, jlen, owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_stat(pfd, uid, gid, mode, plen, &pst1);
        if (r < 0) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = (r == 1) ? -1 : r; goto finish; }
        if (r == 0) { primary = 0; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_stat(lfd, uid, gid, mode, llen, &lst1);
        if (r < 0) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = (r == 1) ? -1 : r; goto finish; }
        if (r == 0) { primary = 0; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        r = z12_pb_stat(jfd, uid, gid, mode, jlen, &jst1);
        if (r < 0) { z12_sysd_first(&diag->img.native, Z12_SYSD_ERRNO, errno); r = z12_pb_guard(owner, deadline, end, diag); primary = (r == 1) ? -1 : r; goto finish; }
        if (r == 0) { primary = 0; goto finish; }
        if (!z12_pb_same(&pst0, &pst1) || !z12_pb_same(&lst0, &lst1) || !z12_pb_same(&jst0, &jst1)) { primary = 0; goto finish; }
        r = z12_pb_guard(owner, deadline, end, diag);
        if (r != 1) { primary = r; goto finish; }
        if (use_borrowed) {
            r = z12_pb_sha256_with_ctx(borrowed, b->policy_addr, plen, b->policy_sha256, owner, deadline, end, diag);
        } else {
            r = z12_pb_sha256(b->policy_addr, plen, b->policy_sha256, owner, deadline, end, diag);
        }
        if (r != 1) { primary = r; goto finish; }
        if (use_borrowed) {
            r = z12_pb_sha256_with_ctx(borrowed, b->plan_addr, llen, b->plan_sha256, owner, deadline, end, diag);
        } else {
            r = z12_pb_sha256(b->plan_addr, llen, b->plan_sha256, owner, deadline, end, diag);
        }
        if (r != 1) { primary = r; goto finish; }
        if (use_borrowed) {
            r = z12_pb_sha256_with_ctx(borrowed, b->journal_addr, jlen, b->journal_sha256, owner, deadline, end, diag);
        } else {
            r = z12_pb_sha256(b->journal_addr, jlen, b->journal_sha256, owner, deadline, end, diag);
        }
        if (r != 1) { primary = r; goto finish; }
        b->policy_dev = pst1.st_dev; b->policy_ino = pst1.st_ino; b->policy_uid = pst1.st_uid; b->policy_gid = pst1.st_gid; b->policy_mode = pst1.st_mode & 07777; b->policy_nlink = pst1.st_nlink; b->policy_size = pst1.st_size; b->policy_mtim_before = pst0.st_mtim; b->policy_mtim_after = pst1.st_mtim; b->policy_ctim_before = pst0.st_ctim; b->policy_ctim_after = pst1.st_ctim;
        b->plan_dev = lst1.st_dev; b->plan_ino = lst1.st_ino; b->plan_uid = lst1.st_uid; b->plan_gid = lst1.st_gid; b->plan_mode = lst1.st_mode & 07777; b->plan_nlink = lst1.st_nlink; b->plan_size = lst1.st_size; b->plan_mtim_before = lst0.st_mtim; b->plan_mtim_after = lst1.st_mtim; b->plan_ctim_before = lst0.st_ctim; b->plan_ctim_after = lst1.st_ctim;
        b->journal_dev = jst1.st_dev; b->journal_ino = jst1.st_ino; b->journal_uid = jst1.st_uid; b->journal_gid = jst1.st_gid; b->journal_mode = jst1.st_mode & 07777; b->journal_nlink = jst1.st_nlink; b->journal_size = jst1.st_size; b->journal_mtim_before = jst0.st_mtim; b->journal_mtim_after = jst1.st_mtim; b->journal_ctim_before = jst0.st_ctim; b->journal_ctim_after = jst1.st_ctim;
        b->creator_pid = getpid();
        b->observed_ns = deadline->last_seen_ns;
        primary = 1;
    finish:
        {
            int cr = z12_pb_close_unique(fds, diag);
            if (cr != 0) primary = -1;
        }
        if (primary == 1) {
            int gr = z12_pb_guard(owner, deadline, end, diag);
            if (gr != 1) {
                primary = gr;
                if (b != NULL) {
                    if (b->policy_addr != NULL) { explicit_bzero(b->policy_addr, b->policy_len); free(b->policy_addr); }
                    if (b->plan_addr != NULL) { explicit_bzero(b->plan_addr, b->plan_len); free(b->plan_addr); }
                    if (b->journal_addr != NULL) { explicit_bzero(b->journal_addr, b->journal_len); free(b->journal_addr); }
                    explicit_bzero(b, sizeof(*b));
                    free((void *)b);
                    b = NULL;
                }
            }
        }
        if (primary == 1) {
            b->observed_ns = deadline->last_seen_ns;
            b->loaded = 1;
            *out = b; b = NULL;
            return 1;
        }
        if (b != NULL) {
            if (b->policy_addr != NULL) { explicit_bzero(b->policy_addr, b->policy_len); free(b->policy_addr); }
            if (b->plan_addr != NULL) { explicit_bzero(b->plan_addr, b->plan_len); free(b->plan_addr); }
            if (b->journal_addr != NULL) { explicit_bzero(b->journal_addr, b->journal_len); free(b->journal_addr); }
            explicit_bzero(b, sizeof(*b));
            free((void *)b);
        }
        return (primary == -2) ? -2 : (primary == -1 ? -1 : 0);
    }
    static int z12_policy_bytes_load(int pfd, size_t plen, size_t plim, int lfd, size_t llen, size_t llim, int jfd, size_t jlen, size_t jlim, uid_t uid, gid_t gid, mode_t mode, Z12ImageCtx *owner, Z12MonotonicDeadline *deadline, uint64_t end, Z12PolicyBytes **out, Z12PolicyBytesDiag *diag) {
        return z12_policy_bytes_load_inner(pfd, plen, plim, lfd, llen, llim, jfd, jlen, jlim, uid, gid, mode, owner, deadline, end, out, diag, NULL, 0);
    }
    static int z12_policy_bytes_load_with_ctx(OSSL_LIB_CTX *libctx, int pfd, size_t plen, size_t plim, int lfd, size_t llen, size_t llim, int jfd, size_t jlen, size_t jlim, uid_t uid, gid_t gid, mode_t mode, Z12ImageCtx *owner, Z12MonotonicDeadline *deadline, uint64_t end, Z12PolicyBytes **out, Z12PolicyBytesDiag *diag) {
        return z12_policy_bytes_load_inner(pfd, plen, plim, lfd, llen, llim, jfd, jlen, jlim, uid, gid, mode, owner, deadline, end, out, diag, libctx, 1);
    }
    """
    ctypedef struct Z12ImageCtx:
        pass
    ctypedef struct Z12PolicyBytes:
        pass
    ctypedef struct Z12PolicyBytesDiag:
        Z12ProcessImageDiag img
        int invalid_contract
    int z12_policy_bytes_load(int pfd, size_t plen, size_t plim, int lfd, size_t llen, size_t llim, int jfd, size_t jlen, size_t jlim, uid_t uid, gid_t gid, mode_t mode, Z12ImageCtx *owner, Z12MonotonicDeadline *deadline, uint64_t end, Z12PolicyBytes **out, Z12PolicyBytesDiag *diag)
    int z12_policy_bytes_load_with_ctx(OSSL_LIB_CTX *libctx, int pfd, size_t plen, size_t plim, int lfd, size_t llen, size_t llim, int jfd, size_t jlen, size_t jlim, uid_t uid, gid_t gid, mode_t mode, Z12ImageCtx *owner, Z12MonotonicDeadline *deadline, uint64_t end, Z12PolicyBytes **out, Z12PolicyBytesDiag *diag)
    int z12_policy_bytes_destroy(Z12PolicyBytes **owned)
