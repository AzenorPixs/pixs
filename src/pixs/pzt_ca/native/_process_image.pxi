# Prive Z12 : observation de l'image executable, sans admission.
# Inclure apres deadline, _launch_obs_sysd.pxi et _systemd_connection.pxi.
# Build -D_GNU_SOURCE ; contexte exclusif au processus createur, sans fork.
# Faits ponctuels : ne prouve ni modules charges, ni politique, ni autorite.
# Domaine procfs/namespace, manifeste et proprietaire complet restent requis.
from libc.stddef cimport size_t
# Type OSSL_LIB_CTX apporte une fois par l'inclueur via _operator_verify (qui inclut _openssl_ed25519.pxi) ou _openssl_ed25519.pxi seule ; aucune redefinition ici.

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <limits.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/stat.h>
    #include <sys/vfs.h>
    #include <linux/magic.h>
    #include <openssl/evp.h>
    enum { Z12_PROCESS_SELF=0, Z12_PROCESS_PEER=1 };
    enum { Z12_IMG_FETCH=1, Z12_IMG_NEW=2, Z12_IMG_INIT=3,
           Z12_IMG_UPDATE=4, Z12_IMG_FINAL=5 };
    typedef struct {
        unsigned char sha256[32];
        int selector;
        pid_t kernel_proc_pid, pid_at_connect;
        struct stat artifact;
        uint64_t observed_monotonic_ns;
    } Z12ProcessImage;
    typedef struct {
        Z12SysdDiag native;
        int openssl_failed, openssl_stage, openssl_code;
    } Z12ProcessImageDiag;
    typedef struct {
        Z12SysdConn *conn;
        sd_bus *bus;
        Z12SysdFacts *facts;
        Z12SysdFacts snapshot;
        Z12MonotonicDeadline *deadline;
        uint64_t end;
        int pidfd;
    } Z12ImageCtx;

    static int z12_image_verdict(Z12ProcessImageDiag *d, int r) {
        Z12SysdDiag *n = &d->native;
        if (n->primary_kind != Z12_SYSD_NONE || n->cleanup_errno != 0 ||
            d->openssl_failed) return -1;
        if (n->invalid_input) return -2;
        if (n->native_output_invalid || n->foreign_binding ||
            n->process_unavailable || n->deadline_expired ||
            n->clock_failed || n->must_destroy_bus) return 0;
        return r;
    }
    static int z12_image_guard(Z12ImageCtx *x, Z12ProcessImageDiag *d) {
        int r, fd = -1;
        struct ucred peer = {0};
        if (x == NULL || d == NULL) return -2;
        if (x->conn == NULL || x->facts == NULL || x->bus == NULL ||
            x->deadline == NULL) { d->native.invalid_input = 1; return -2; }
        r = z12_conn_guard(x->conn, &d->native);
        if (r != 1) return z12_image_verdict(d, r);
        if (x->conn->facts != x->facts || x->conn->bus != x->bus ||
            x->conn->deadline != x->deadline || x->conn->expected_end_ns != x->end ||
            x->facts->self_pid != x->snapshot.self_pid ||
            x->facts->peer_pid != x->snapshot.peer_pid ||
            x->facts->self_uid != x->snapshot.self_uid ||
            x->facts->self_euid != x->snapshot.self_euid ||
            x->facts->peer_euid_at_connect != x->snapshot.peer_euid_at_connect ||
            x->facts->self_pidfd != x->snapshot.self_pidfd ||
            x->facts->peer_pidfd != x->snapshot.peer_pidfd ||
            x->facts->bus_fd != x->snapshot.bus_fd ||
            x->facts->borrowed_bus != x->snapshot.borrowed_bus ||
            x->facts->observed_monotonic_ns != x->snapshot.observed_monotonic_ns ||
            x->facts->expected_end_ns != x->snapshot.expected_end_ns ||
            x->snapshot.self_pid != x->conn->creator_pid ||
            x->snapshot.self_uid != x->conn->creator_uid ||
            x->snapshot.self_euid != x->conn->creator_euid ||
            x->snapshot.borrowed_bus != x->bus ||
            x->snapshot.expected_end_ns != x->end) {
            d->native.foreign_binding = 1; return 0;
        }
        /* Ces primitives locales n'envoient aucun RPC ; garde avant/apres. */
        r = z12_sysd_bus_facts(x->bus, &fd, &peer, &d->native);
        if (r != 1) return z12_image_verdict(d, r);
        if (fd != x->snapshot.bus_fd || peer.pid != x->snapshot.peer_pid ||
            peer.uid != x->snapshot.peer_euid_at_connect) {
            d->native.foreign_binding = 1; return 0;
        }
        r = z12_sysd_pidfd_live(x->snapshot.self_pidfd, &d->native);
        if (r != 1) return z12_image_verdict(d, r);
        r = z12_sysd_pidfd_live(x->snapshot.peer_pidfd, &d->native);
        if (r != 1) return z12_image_verdict(d, r);
        r = z12_sysd_deadline(x->deadline, x->end, &d->native);
        return z12_image_verdict(d, r);
    }
    static int z12_image_open(Z12ImageCtx *x, int parent, const char *name,
                              int flags, int *out, Z12ProcessImageDiag *d) {
        int r = z12_image_guard(x, d), failed;
        if (r != 1) return r;
        *out = openat(parent, name, flags);
        failed = *out < 0;
        if (failed) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_image_guard(x, d);
        return failed ? -1 : r;
    }
    static int z12_image_stat(Z12ImageCtx *x, int fd, struct stat *s,
                              Z12ProcessImageDiag *d) {
        int r = z12_image_guard(x, d), failed;
        if (r != 1) return r;
        failed = fstat(fd, s) != 0;
        if (failed) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_image_guard(x, d);
        return failed ? -1 : r;
    }
    static int z12_image_read(Z12ImageCtx *x, int fd, void *buf, size_t size,
                              ssize_t *count, Z12ProcessImageDiag *d) {
        int r = z12_image_guard(x, d), failed;
        if (r != 1) return r;
        *count = read(fd, buf, size);
        failed = *count < 0;
        if (failed) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_image_guard(x, d);
        return failed ? -1 : r;
    }
    static int z12_image_close(int *fd, Z12ProcessImageDiag *d) {
        /* Le nettoyage reste obligatoire apres expiration, sans retry close. */
        return z12_sysd_close_owned(fd, &d->native);
    }
    static int z12_image_mapping(Z12ImageCtx *x, int root, size_t bound,
                                 pid_t *pid, Z12ProcessImageDiag *d) {
        char name[64], *data = NULL, extra;
        int fd = -1, r = 0, printed, found = 0, failed = 0;
        size_t used = 0, wanted, i, end, j;
        unsigned long value, digit;
        ssize_t n = 0;
        pid_t parsed = -1;
        if (bound == 0 || bound == SIZE_MAX) { d->native.invalid_input = 1; return -2; }
        printed = snprintf(name, sizeof(name), "self/fdinfo/%d", x->pidfd);
        if (printed < 0 || (size_t)printed >= sizeof(name)) {
            d->native.native_output_invalid = 1; return 0;
        }
        r = z12_image_guard(x, d); if (r != 1) return r;
        data = malloc(bound + 1);
        if (data == NULL) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_image_guard(x, d);
        if (data == NULL || r != 1) goto done;
        r = z12_image_open(x, root, name,
            O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK|O_NOCTTY, &fd, d);
        if (r != 1) goto done;
        while (used < bound) {
            wanted = bound - used; if (wanted > 256) wanted = 256;
            r = z12_image_read(x, fd, data + used, wanted, &n, d);
            if (r != 1) goto done;
            if (n == 0) break;
            if ((size_t)n > wanted) { d->native.native_output_invalid = 1; r = 0; goto done; }
            used += (size_t)n;
        }
        if (used == bound) {
            r = z12_image_read(x, fd, &extra, 1, &n, d);
            if (r != 1) goto done;
            if (n != 0) { d->native.native_output_invalid = 1; r = 0; goto done; }
        }
        if (used == 0 || data[used - 1] != '\n') {
            d->native.native_output_invalid = 1; r = 0; goto done;
        }
        data[used] = '\0';
        i = 0;
        while (i < used) {
            r = z12_image_guard(x, d); if (r != 1) goto done;
            end = i;
            while (end < used && data[end] != '\n') {
                if (data[end] == '\0' || data[end] == '\r') {
                    d->native.native_output_invalid = 1; r = 0; goto done;
                }
                if ((end - i) % 256 == 0) {
                    r = z12_image_guard(x, d); if (r != 1) goto done;
                }
                end++;
            }
            if (end - i >= 4 && memcmp(data + i, "Pid:", 4) == 0) {
                if (++found != 1) { d->native.foreign_binding = 1; r = 0; goto done; }
                j = i + 4;
                while (j < end && (data[j] == ' ' || data[j] == '\t')) {
                    if ((j - i) % 256 == 0) {
                        r = z12_image_guard(x, d); if (r != 1) goto done;
                    }
                    j++;
                }
                if (j == end) { d->native.native_output_invalid = 1; r = 0; goto done; }
                value = 0;
                for (; j < end; j++) {
                    if (data[j] < '0' || data[j] > '9') {
                        d->native.native_output_invalid = 1; r = 0; goto done;
                    }
                    digit = (unsigned long)(data[j] - '0');
                    if (value > ((unsigned long)INT_MAX - digit) / 10) {
                        d->native.native_output_invalid = 1; r = 0; goto done;
                    }
                    value = value * 10 + digit;
                    if ((j - i) % 256 == 0) {
                        r = z12_image_guard(x, d); if (r != 1) goto done;
                    }
                }
                if (value == 0) { d->native.process_unavailable = 1; r = 0; goto done; }
                parsed = (pid_t)value;
                if (parsed <= 0 || (unsigned long)parsed != value) {
                    d->native.native_output_invalid = 1; r = 0; goto done;
                }
            }
            i = end + 1;
        }
        if (found != 1) { d->native.foreign_binding = 1; r = 0; goto done; }
        r = 1;
    done:
        failed = z12_image_close(&fd, d) != 0;
        free(data);
        if (r == 1 && !failed) r = z12_image_guard(x, d);
        r = z12_image_verdict(d, failed ? -1 : r);
        if (r == 1) *pid = parsed;
        return r;
    }
    static int z12_image_same_stat(const struct stat *a, const struct stat *b) {
        return a->st_dev == b->st_dev && a->st_ino == b->st_ino &&
            a->st_mode == b->st_mode && a->st_uid == b->st_uid &&
            a->st_gid == b->st_gid && a->st_nlink == b->st_nlink &&
            a->st_size == b->st_size &&
            a->st_mtim.tv_sec == b->st_mtim.tv_sec &&
            a->st_mtim.tv_nsec == b->st_mtim.tv_nsec &&
            a->st_ctim.tv_sec == b->st_ctim.tv_sec &&
            a->st_ctim.tv_nsec == b->st_ctim.tv_nsec;
    }
    static void z12_image_crypto_error(Z12ProcessImageDiag *d, int stage, int code) {
        if (!d->openssl_failed) {
            d->openssl_failed = 1; d->openssl_stage = stage; d->openssl_code = code;
        }
    }
    static int z12_image_hash(Z12ImageCtx *x, int fd, size_t length,
                              OSSL_LIB_CTX *libctx, unsigned char digest[32],
                              Z12ProcessImageDiag *d) {
        EVP_MD *md = NULL;
        EVP_MD_CTX *ctx = NULL;
        unsigned char block[4096];
        size_t total = 0, wanted;
        ssize_t n;
        unsigned int size = 0;
        int r, code;
        r = z12_image_guard(x, d); if (r != 1) return r;
        md = EVP_MD_fetch(libctx, "SHA256", "provider=default");
        if (md == NULL) z12_image_crypto_error(d, Z12_IMG_FETCH, 0);
        r = z12_image_guard(x, d); if (md == NULL || r != 1) goto done;
        ctx = EVP_MD_CTX_new();
        if (ctx == NULL) z12_image_crypto_error(d, Z12_IMG_NEW, 0);
        r = z12_image_guard(x, d); if (ctx == NULL || r != 1) goto done;
        code = EVP_DigestInit_ex2(ctx, md, NULL);
        if (code != 1) z12_image_crypto_error(d, Z12_IMG_INIT, code);
        r = z12_image_guard(x, d); if (r != 1) goto done;
        while (total < length) {
            wanted = length - total; if (wanted > sizeof(block)) wanted = sizeof(block);
            r = z12_image_read(x, fd, block, wanted, &n, d);
            if (r != 1) goto done;
            if (n == 0 || (size_t)n > wanted) {
                d->native.native_output_invalid = 1; r = 0; goto done;
            }
            code = EVP_DigestUpdate(ctx, block, (size_t)n);
            if (code != 1) z12_image_crypto_error(d, Z12_IMG_UPDATE, code);
            r = z12_image_guard(x, d); if (r != 1) goto done;
            total += (size_t)n;
        }
        r = z12_image_read(x, fd, block, 1, &n, d);
        if (r != 1) goto done;
        if (n != 0) { d->native.native_output_invalid = 1; r = 0; goto done; }
        code = EVP_DigestFinal_ex(ctx, digest, &size);
        if (code != 1) z12_image_crypto_error(d, Z12_IMG_FINAL, code);
        r = z12_image_guard(x, d); if (r != 1) goto done;
        if (size != 32) { d->native.native_output_invalid = 1; r = 0; goto done; }
        r = 1;
    done:
        EVP_MD_CTX_free(ctx); EVP_MD_free(md);
        if (r == 1) r = z12_image_guard(x, d);
        return z12_image_verdict(d, r);
    }
    static void z12_process_image_destroy(Z12ProcessImage **pp) {
        if (pp != NULL && *pp != NULL) { free(*pp); *pp = NULL; }
    }
    /* Les sorties sont privees. Aucun EVP_PKEY/capsule/PID libre Python. */
    static int z12_process_image_collect(Z12SysdConn *c, OSSL_LIB_CTX *libctx,
            int selector, size_t max_bytes, size_t max_procmeta_bytes,
            Z12ProcessImage **out, Z12ProcessImageDiag *diag) {
        Z12ImageCtx x = {0};
        Z12ProcessImage *img = NULL;
        struct stat first, after, reopened;
        struct statfs fs;
        pid_t pid = -1, final_pid = -1, at_connect;
        char name[32];
        int root = -1, dirfd = -1, exefd = -1, second = -1;
        int r = -2, printed, failed, cleanup = 0;
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        if (out == NULL || *out != NULL || c == NULL || libctx == NULL ||
            max_bytes == 0 || max_procmeta_bytes == 0 || max_procmeta_bytes == SIZE_MAX ||
            (selector != Z12_PROCESS_SELF && selector != Z12_PROCESS_PEER)) {
            diag->native.invalid_input = 1; return -2;
        }
        r = z12_conn_guard(c, &diag->native); if (r != 1) return r;
        if (c->facts == NULL || c->bus == NULL) {
            diag->native.foreign_binding = 1; return 0;
        }
        x.conn = c; x.facts = c->facts;
        memcpy(&x.snapshot, c->facts, sizeof(x.snapshot));
        x.bus = c->bus; x.deadline = c->deadline; x.end = c->expected_end_ns;
        x.pidfd = selector == Z12_PROCESS_SELF ? x.snapshot.self_pidfd : x.snapshot.peer_pidfd;
        at_connect = selector == Z12_PROCESS_SELF ? x.snapshot.self_pid : x.snapshot.peer_pid;
        if (x.pidfd < 0 || at_connect <= 0) { diag->native.foreign_binding = 1; return 0; }
        r = z12_image_open(&x, AT_FDCWD, "/proc",
            O_RDONLY|O_DIRECTORY|O_CLOEXEC|O_NOFOLLOW, &root, diag);
        if (r != 1) goto done;
        failed = fstatfs(root, &fs) != 0;
        if (failed) z12_sysd_first(&diag->native, Z12_SYSD_ERRNO, errno);
        r = z12_image_guard(&x, diag); if (r != 1 || failed) goto done;
        if (fs.f_type != PROC_SUPER_MAGIC) { diag->native.foreign_binding = 1; r = 0; goto done; }
        r = z12_image_mapping(&x, root, max_procmeta_bytes, &pid, diag);
        if (r != 1) goto done;
        printed = snprintf(name, sizeof(name), "%d", (int)pid);
        if (printed < 0 || (size_t)printed >= sizeof(name)) {
            diag->native.native_output_invalid = 1; r = 0; goto done;
        }
        r = z12_image_open(&x, root, name,
            O_RDONLY|O_DIRECTORY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK|O_NOCTTY, &dirfd, diag);
        if (r != 1) goto done;
        /* Seul ce composant magique du procfs verifie est suivi. */
        r = z12_image_open(&x, dirfd, "exe", O_RDONLY|O_CLOEXEC|O_NONBLOCK|O_NOCTTY, &exefd, diag);
        if (r != 1) goto done;
        r = z12_image_stat(&x, exefd, &first, diag); if (r != 1) goto done;
        if (!S_ISREG(first.st_mode) || first.st_nlink == 0 || first.st_size < 0 ||
            (uintmax_t)first.st_size > (uintmax_t)max_bytes) {
            diag->native.foreign_binding = 1; r = 0; goto done;
        }
        img = calloc(1, sizeof(*img));
        if (img == NULL) z12_sysd_first(&diag->native, Z12_SYSD_ERRNO, errno);
        r = z12_image_guard(&x, diag); if (img == NULL || r != 1) goto done;
        r = z12_image_hash(&x, exefd, (size_t)first.st_size, libctx, img->sha256, diag);
        if (r != 1) goto done;
        r = z12_image_stat(&x, exefd, &after, diag); if (r != 1) goto done;
        r = z12_image_open(&x, dirfd, "exe", O_RDONLY|O_CLOEXEC|O_NONBLOCK|O_NOCTTY, &second, diag);
        if (r != 1) goto done;
        r = z12_image_stat(&x, second, &reopened, diag); if (r != 1) goto done;
        if (!z12_image_same_stat(&first, &after) || !z12_image_same_stat(&first, &reopened)) {
            diag->native.foreign_binding = 1; r = 0; goto done;
        }
        r = z12_image_mapping(&x, root, max_procmeta_bytes, &final_pid, diag);
        if (r != 1) goto done;
        if (pid != final_pid) { diag->native.foreign_binding = 1; r = 0; goto done; }
        img->selector = selector; img->kernel_proc_pid = pid;
        img->pid_at_connect = at_connect; img->artifact = first;
        r = 1;
    done:
        cleanup |= z12_image_close(&second, diag) != 0;
        cleanup |= z12_image_close(&exefd, diag) != 0;
        cleanup |= z12_image_close(&dirfd, diag) != 0;
        cleanup |= z12_image_close(&root, diag) != 0;
        if (r == 1 && !cleanup) r = z12_image_guard(&x, diag);
        r = z12_image_verdict(diag, cleanup ? -1 : r);
        if (r == 1) {
            img->observed_monotonic_ns = x.deadline->last_seen_ns;
            *out = img;
        } else z12_process_image_destroy(&img);
        return r;
    }
    """
    ctypedef struct Z12ProcessImage:
        pass
    ctypedef struct Z12ProcessImageDiag:
        Z12SysdDiag native
        int openssl_failed
        int openssl_stage
        int openssl_code
    int z12_process_image_collect(Z12SysdConn *c, OSSL_LIB_CTX *libctx,
        int selector, size_t max_bytes, size_t max_procmeta_bytes,
        Z12ProcessImage **out, Z12ProcessImageDiag *diag)
    void z12_process_image_destroy(Z12ProcessImage **pp)
