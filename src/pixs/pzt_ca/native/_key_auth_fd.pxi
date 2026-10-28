# Prive Z12/Linux : acquisition d'octets d'autorisation par FD consomme.
# Inclure UNE fois apres _monotonic_deadline.pxi ; _GNU_SOURCE requis au build.
# Taille exacte et limite viennent de la composition/politique, sans valeur par defaut.
# Fstat et sceaux ne prouvent ni provenance, ni host+tpm2, ni autorite D16.
# Composition exclusive : pas de fork/dup/fermeture concurrente pendant acquisition.
# Les syscalls ne sont pas preemptes par l'echeance ; tout retour tardif est refuse.
# Aucun objet Python, API publique, capsule, getter de valeur ou effet a inclusion.
from libc.stddef cimport size_t

cdef extern from "sys/types.h" nogil:
    ctypedef unsigned int uid_t
    ctypedef unsigned int gid_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <fcntl.h>
    #include <limits.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <sys/mman.h>
    #include <sys/stat.h>
    #include <sys/types.h>
    #include <unistd.h>

    typedef struct {
        unsigned char *addr;
        size_t len;
        size_t map_len;
        pid_t creator_pid;
        int loaded;
    } Z12KeyAuthBuf;

    typedef struct {
        int invalid_contract;
        int deadline_expired;
        int clock_failed;
        int clock_errno;
        int cleanup_failed;
        int cleanup_errno;
    } Z12KeyAuthDiag;

    static int z12_key_auth_deadline(
        Z12MonotonicDeadline *deadline, Z12KeyAuthDiag *diag
    ) {
        int32_t remaining_ms = 0;
        int result = z12_deadline_remaining(deadline, &remaining_ms);
        if (result == 0) diag->deadline_expired = 1;
        else if (result == -1) {
            diag->clock_failed = 1;
            diag->clock_errno = errno;
        } else if (result != 1) {
            diag->invalid_contract = 1;
            return -2;
        }
        return result;
    }

    static int z12_key_auth_fd_check(
        int fd, uid_t uid, gid_t gid, size_t length, struct stat *observed
    ) {
        struct stat st;
        int flags, seals;
        const int required = F_SEAL_WRITE | F_SEAL_GROW
                           | F_SEAL_SHRINK | F_SEAL_SEAL;
        if (fstat(fd, &st) != 0) return -1;
        if (!S_ISREG(st.st_mode) || st.st_nlink != 0 || st.st_size < 0
            || (uintmax_t)st.st_size != (uintmax_t)length
            || st.st_uid != uid || st.st_gid != gid
            || (st.st_mode & 07777) != 0400) return 0;
        flags = fcntl(fd, F_GETFD);
        if (flags < 0) return -1;
        if ((flags & FD_CLOEXEC) == 0) return 0;
        flags = fcntl(fd, F_GETFL);
        if (flags < 0) return -1;
        if ((flags & O_ACCMODE) != O_RDONLY) return 0;
        seals = fcntl(fd, F_GET_SEALS);
        if (seals < 0) {
            if (errno == EINVAL || errno == ENOTTY) return 0;
            return -1;
        }
        if ((seals & required) != required) return 0;
        *observed = st;
        return 1;
    }

    /* 1 libere (NULL deja libere compris), -1 conserve *owned, -2 contrat.
       Nettoyage permis apres expiration et dans l'enfant WIPEONFORK.
       Aucun munlock anticipe : munmap reussi retire aussi le verrou.
       En echec, les octets sont effaces mais le mapping reste owned. */
    static int z12_key_auth_buf_destroy(Z12KeyAuthBuf **owned) {
        Z12KeyAuthBuf *buf;
        int saved_errno = errno;
        if (owned == NULL) return -2;
        buf = *owned;
        if (buf == NULL) return 1;
        buf->loaded = 0;
        if (buf->addr != NULL) {
            explicit_bzero(buf->addr, buf->map_len);
            if (munmap(buf->addr, buf->map_len) != 0) return -1;
        }
        explicit_bzero(buf, sizeof(*buf));
        free(buf);
        *owned = NULL;
        errno = saved_errno;
        return 1;
    }

    /* 1 octets acquis, 0 refus, -1 erreur, -2 contrat.
       FD >=0 transfere et consomme exactement une fois, y compris refus.
       *out doit etre NULL en entree. Sur erreur de munmap seulement,
       *out reste un objet loaded=0 a detruire, JAMAIS une capacite utilisable.
       Le futur consommateur C prive doit aussi verifier creator_pid et
       l'autorite/contexte courant ; loaded seul ne prouve aucun de ces faits. */
    static int z12_key_auth_fd_load(
        int fd, uid_t uid, gid_t gid, size_t expected_len, size_t policy_limit,
        Z12MonotonicDeadline *deadline, Z12KeyAuthBuf **out, Z12KeyAuthDiag *diag
    ) {
        const int entry_errno = errno;
        int result = -2, primary_errno = 0, close_errno = 0;
        Z12KeyAuthBuf *buf = NULL;
        struct stat before, after;
        size_t page, rounded, done = 0;
        long page_value;
        ssize_t got;
        off_t last_offset;

        if (diag != NULL) memset(diag, 0, sizeof(*diag));
        if (fd < 0) {
            if (diag != NULL) diag->invalid_contract = 1;
            return -2;
        }
        if (out == NULL || diag == NULL || deadline == NULL || *out != NULL) {
            if (diag != NULL) diag->invalid_contract = 1;
            goto finish;
        }
        last_offset = (off_t)expected_len;
        if (expected_len == 0 || expected_len > policy_limit
            || expected_len > (size_t)SSIZE_MAX || last_offset <= 0
            || (uintmax_t)last_offset != (uintmax_t)expected_len) {
            diag->invalid_contract = 1;
            goto finish;
        }
        result = z12_key_auth_deadline(deadline, diag);
        if (result != 1) {
            if (result == -1) primary_errno = errno;
            goto finish;
        }
        result = z12_key_auth_fd_check(fd, uid, gid, expected_len, &before);
        if (result != 1) {
            if (result == -1) primary_errno = errno;
            goto finish;
        }
        result = z12_key_auth_deadline(deadline, diag);
        if (result != 1) {
            if (result == -1) primary_errno = errno;
            goto finish;
        }

        errno = 0;
        page_value = sysconf(_SC_PAGESIZE);
        if (page_value <= 0) {
            primary_errno = errno != 0 ? errno : EINVAL;
            result = -1;
            goto finish;
        }
        page = (size_t)page_value;
        if (expected_len > SIZE_MAX - (page - 1)) {
            diag->invalid_contract = 1;
            result = -2;
            goto finish;
        }
        rounded = ((expected_len + page - 1) / page) * page;
        buf = calloc(1, sizeof(*buf));
        if (buf == NULL) {
            primary_errno = ENOMEM;
            result = -1;
            goto finish;
        }
        buf->len = expected_len;
        buf->map_len = rounded;
        buf->creator_pid = getpid();
        buf->addr = mmap(NULL, rounded, PROT_READ | PROT_WRITE,
                         MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (buf->addr == MAP_FAILED) {
            primary_errno = errno;
            buf->addr = NULL;
            result = -1;
            goto finish;
        }
        if (mlock(buf->addr, rounded) != 0
            || madvise(buf->addr, rounded, MADV_DONTDUMP) != 0
            || madvise(buf->addr, rounded, MADV_WIPEONFORK) != 0) {
            primary_errno = errno;
            result = -1;
            goto finish;
        }

        while (done < expected_len) {
            result = z12_key_auth_deadline(deadline, diag);
            if (result != 1) {
                if (result == -1) primary_errno = errno;
                goto finish;
            }
            got = pread(fd, buf->addr + done, expected_len - done, (off_t)done);
            if (got < 0) {
                primary_errno = errno; /* EINTR : pas de retry non borne. */
                result = -1;
                goto finish;
            }
            if (got == 0 || (size_t)got > expected_len - done) {
                result = 0;
                goto finish;
            }
            done += (size_t)got;
            result = z12_key_auth_deadline(deadline, diag);
            if (result != 1) {
                if (result == -1) primary_errno = errno;
                goto finish;
            }
        }
        result = z12_key_auth_fd_check(fd, uid, gid, expected_len, &after);
        if (result != 1) {
            if (result == -1) primary_errno = errno;
            goto finish;
        }
        if (before.st_dev != after.st_dev || before.st_ino != after.st_ino) {
            result = 0;
            goto finish;
        }

    finish:
        /* Linux : close consomme le FD meme sur EINTR, aucun second close. */
        if (close(fd) != 0) {
            close_errno = errno;
            if (diag != NULL) {
                diag->cleanup_failed = 1;
                diag->cleanup_errno = close_errno;
            }
            if (primary_errno == 0) primary_errno = close_errno;
            result = -1;
        }
        if (result == 1) {
            result = z12_key_auth_deadline(deadline, diag);
            if (result == -1) primary_errno = errno;
        }
        if (result == 1) {
            buf->loaded = 1;
            *out = buf;
            buf = NULL;
        } else if (buf != NULL) {
            if (z12_key_auth_buf_destroy(&buf) != 1) {
                if (primary_errno == 0) primary_errno = errno;
                diag->cleanup_failed = 1;
                diag->cleanup_errno = errno;
                *out = buf;
                result = -1;
            }
        }
        errno = result == -1 ? primary_errno : entry_errno;
        return result;
    }
    """
    ctypedef struct Z12KeyAuthBuf:
        pass

    ctypedef struct Z12KeyAuthDiag:
        int invalid_contract
        int deadline_expired
        int clock_failed
        int clock_errno
        int cleanup_failed
        int cleanup_errno

    int z12_key_auth_buf_destroy(Z12KeyAuthBuf **owned)
    int z12_key_auth_fd_load(
        int fd, uid_t uid, gid_t gid, size_t expected_len, size_t policy_limit,
        Z12MonotonicDeadline *deadline, Z12KeyAuthBuf **out, Z12KeyAuthDiag *diag
    )
