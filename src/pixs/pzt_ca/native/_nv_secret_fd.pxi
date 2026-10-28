# Privé Z12/Linux : acquisition native d’un secret NV via FD consommé.
# La provenance du canal et l’autorité courante sont vérifiées par le propriétaire.
# Le caller transfère l’exclusivité du FD et d’une sortie native non exposée à Python.
cdef extern from "sys/types.h" nogil:
    ctypedef unsigned int uid_t
    ctypedef unsigned int gid_t
    ctypedef unsigned int mode_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <fcntl.h>
    #include <stddef.h>
    #include <string.h>
    #include <sys/stat.h>
    #include <sys/types.h>
    #include <unistd.h>

    /* Construction Linux avec _GNU_SOURCE ; aucun remplacement des constantes. */
    typedef struct {
        unsigned char value[32];
        int loaded;
    } Z12NvSecret;

    static void z12_nv_secret_destroy(Z12NvSecret *secret) {
        if (secret != NULL) {
            explicit_bzero(secret->value, sizeof(secret->value));
            secret->loaded = 0;
        }
    }

    static int z12_nv_secret_fd_check(
        int fd, uid_t expected_uid, gid_t expected_gid, mode_t expected_mode
    ) {
        struct stat st;
        int flags;
        int seals;
        const int required_seals = F_SEAL_WRITE | F_SEAL_GROW
                                  | F_SEAL_SHRINK | F_SEAL_SEAL;
        if (fstat(fd, &st) != 0) return -1;
        if (!S_ISREG(st.st_mode) || st.st_nlink != 0 || st.st_size != 32) return 0;
        if (st.st_uid != expected_uid || st.st_gid != expected_gid) return 0;
        if ((st.st_mode & 07777) != expected_mode) return 0;
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
        if ((seals & required_seals) != required_seals) return 0;
        return 1;
    }

    static int z12_nv_secret_load_fd(
        int fd, uid_t expected_uid, gid_t expected_gid,
        mode_t expected_mode, Z12NvSecret *secret
    ) {
        size_t done = 0;
        ssize_t got;
        int result = -2;
        int saved_errno = 0;
        const int entry_errno = errno;
        z12_nv_secret_destroy(secret);
        if (fd < 0) { errno = entry_errno; return -2; }
        if (secret == NULL || expected_mode != 0400) goto finished;
        result = z12_nv_secret_fd_check(fd, expected_uid, expected_gid, expected_mode);
        if (result != 1) {
            if (result == -1) saved_errno = errno;
            goto finished;
        }
        while (done < sizeof(secret->value)) {
            got = pread(fd, secret->value + done, sizeof(secret->value) - done, (off_t)done);
            if (got < 0) {
                /* EINTR ferme cette tentative sans effet NV ; aucun retry non borné. */
                result = -1;
                saved_errno = errno;
                goto finished;
            }
            if (got == 0 || (size_t)got > sizeof(secret->value) - done) {
                result = 0;
                goto finished;
            }
            done += (size_t)got;
        }
        result = z12_nv_secret_fd_check(fd, expected_uid, expected_gid, expected_mode);
        if (result == -1) saved_errno = errno;
    finished:
        /* Linux : le FD est consommé, même après EINTR de close ; ne pas réessayer. */
        if (close(fd) != 0) {
            if (saved_errno == 0) saved_errno = errno;
            result = -1;
        }
        if (result == 1) {
            secret->loaded = 1;
        } else {
            z12_nv_secret_destroy(secret);
        }
        if (result == -1) errno = saved_errno;
        else errno = entry_errno;
        return result;
    }
    """
    ctypedef struct Z12NvSecret:
        unsigned char value[32]
        int loaded

    void z12_nv_secret_destroy(Z12NvSecret *secret)
    int z12_nv_secret_load_fd(
        int fd, uid_t expected_uid, gid_t expected_gid,
        mode_t expected_mode, Z12NvSecret *secret
    )
