# cython: language_level=3
"""Lecteur de FD NV privé : aucun secret ni handle exposé par une API Python.

L'appelant natif authentifié remet un FD unique et un tampon natif de 32 octets.
Ce lecteur ne vérifie ni provenance du FD, autorité, politique, mandat ou TPM.
Il ne génère rien, n'ouvre aucun chemin et ne contacte aucun périphérique.
Les symboles C/header sont générés par Cython, pour composition privée seulement.
"""
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint32_t, uint64_t

cdef extern from "sys/types.h":
    ctypedef long ssize_t

cdef extern from "time.h":
    cdef struct timespec:
        long tv_sec
        long tv_nsec
    int CLOCK_MONOTONIC
    int clock_gettime(int, timespec *) noexcept nogil

cdef extern from "sys/stat.h":
    cdef struct stat:
        unsigned long st_dev
        unsigned long st_ino
        unsigned long st_nlink
        unsigned int st_mode
        long st_size
        timespec st_mtim
        timespec st_ctim
    int fstat(int, stat *) noexcept nogil
    int S_ISREG(unsigned int) noexcept nogil
    int S_ISFIFO(unsigned int) noexcept nogil

cdef extern from "fcntl.h":
    int F_GETFL
    int F_SETFL
    int F_GETFD
    int F_SETFD
    int FD_CLOEXEC
    int O_ACCMODE
    int O_RDONLY
    int O_NONBLOCK
    int fcntl(int, int, ...) noexcept nogil

cdef extern from "poll.h":
    ctypedef unsigned long nfds_t
    cdef struct pollfd:
        int fd
        short events
        short revents
    int POLLIN
    int POLLHUP
    int POLLERR
    int POLLNVAL
    int poll(pollfd *, nfds_t, int) noexcept nogil

cdef extern from "unistd.h":
    ssize_t read(int, void *, size_t) noexcept nogil
    int close(int) noexcept nogil
    long lseek(int, long, int) noexcept nogil
    int SEEK_CUR

cdef extern from "errno.h":
    int errno
    int EINTR
    int EAGAIN
    int EWOULDBLOCK

cdef extern from "openssl/crypto.h":
    void OPENSSL_cleanse(void *, size_t) noexcept nogil

cdef enum:
    SECRET_OK = 0
    SECRET_ARGUMENT = 1
    SECRET_CLOCK = 2
    SECRET_FD = 3
    SECRET_SHORT = 4
    SECRET_EXTRA = 5
    SECRET_TIMEOUT = 6
    SECRET_IO = 7
    SECRET_CHANGED = 8
    SECRET_CLOSE_FAILED = 0x10000


cdef uint64_t _now_ns() noexcept nogil:
    cdef timespec value
    if clock_gettime(CLOCK_MONOTONIC, &value) != 0:
        return 0
    if value.tv_sec < 0 or value.tv_nsec < 0 or value.tv_nsec >= 1000000000:
        return 0
    return <uint64_t>value.tv_sec * 1000000000 + <uint64_t>value.tv_nsec


cdef uint32_t _finish(int fd, uint8_t *output, uint8_t *extra,
                      uint32_t status) noexcept nogil:
    # Sous Linux, ne pas réessayer close après EINTR : le FD peut être réutilisé.
    if close(fd) != 0:
        status |= SECRET_CLOSE_FAILED
    if status != SECRET_OK:
        OPENSSL_cleanse(output, 32)
    OPENSSL_cleanse(extra, 1)
    return status


cdef public uint32_t pa01_nv_secret_read32(
        int *fd_inout, uint8_t *output, size_t output_size,
        int timeout_ms) noexcept nogil:
    """ABI C privée v1 ; statut bas16bits, close_failed bit16.

    Forme/clock invalide avant transfert : FD inchangé. Après transfert,
    *fd_inout vaut -1 et le lecteur ferme son FD sur tous les chemins.
    La sortie contient 32 octets seulement pour statut 0 ; sinon elle est
    nettoyée dès lors que son pointeur/taille étaient valides.
    Le propriétaire garantit absence d'alias et lifetime des pointeurs/FD.
    """
    cdef uint64_t now, duration, deadline, remaining
    cdef int fd, flags, descriptor_flags, wait_ms, wait_result, regular
    cdef ssize_t amount
    cdef size_t used = 0
    cdef uint8_t extra = 0
    cdef uint32_t result
    cdef stat before, after
    cdef pollfd descriptor

    if fd_inout == NULL or output == NULL or output_size != 32:
        return SECRET_ARGUMENT
    OPENSSL_cleanse(output, 32)
    if fd_inout[0] < 3 or timeout_ms <= 0:
        return SECRET_ARGUMENT
    now = _now_ns()
    duration = <uint64_t>timeout_ms * 1000000
    if now == 0 or now > (~<uint64_t>0) - duration:
        return SECRET_CLOCK
    deadline = now + duration
    fd = fd_inout[0]
    fd_inout[0] = -1

    if fstat(fd, &before) != 0:
        return _finish(fd, output, &extra, SECRET_FD)
    regular = S_ISREG(before.st_mode)
    if not regular and not S_ISFIFO(before.st_mode):
        return _finish(fd, output, &extra, SECRET_FD)
    if regular:
        if before.st_nlink > 1 or lseek(fd, 0, SEEK_CUR) != 0:
            return _finish(fd, output, &extra, SECRET_FD)
        if before.st_size < 32:
            return _finish(fd, output, &extra, SECRET_SHORT)
        if before.st_size > 32:
            return _finish(fd, output, &extra, SECRET_EXTRA)
    flags = fcntl(fd, F_GETFL)
    descriptor_flags = fcntl(fd, F_GETFD)
    if flags < 0 or descriptor_flags < 0 or (flags & O_ACCMODE) != O_RDONLY:
        return _finish(fd, output, &extra, SECRET_FD)
    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) != 0
            or fcntl(fd, F_SETFD, descriptor_flags | FD_CLOEXEC) != 0):
        return _finish(fd, output, &extra, SECRET_FD)

    while True:
        now = _now_ns()
        if now == 0:
            return _finish(fd, output, &extra, SECRET_CLOCK)
        if now >= deadline:
            return _finish(fd, output, &extra, SECRET_TIMEOUT)
        if used < 32:
            amount = read(fd, output + used, 32 - used)
        else:
            amount = read(fd, &extra, 1)
        if amount > 0:
            if used == 32:
                return _finish(fd, output, &extra, SECRET_EXTRA)
            used += <size_t>amount
            continue
        if amount == 0:
            result = SECRET_OK if used == 32 else SECRET_SHORT
            break
        if errno == EINTR:
            continue
        if errno != EAGAIN and errno != EWOULDBLOCK:
            return _finish(fd, output, &extra, SECRET_IO)
        now = _now_ns()
        if now == 0:
            return _finish(fd, output, &extra, SECRET_CLOCK)
        if now >= deadline:
            return _finish(fd, output, &extra, SECRET_TIMEOUT)
        remaining = deadline - now
        wait_ms = <int>((remaining + 999999) // 1000000)
        descriptor.fd = fd
        descriptor.events = POLLIN
        descriptor.revents = 0
        wait_result = poll(&descriptor, 1, wait_ms)
        if wait_result < 0:
            if errno == EINTR:
                continue
            return _finish(fd, output, &extra, SECRET_IO)
        if wait_result == 0:
            return _finish(fd, output, &extra, SECRET_TIMEOUT)
        if descriptor.revents & (POLLERR | POLLNVAL):
            return _finish(fd, output, &extra, SECRET_IO)
        # POLLHUP permet la lecture finale d'EOF ; aucun succès par poll seul.

    if result == SECRET_OK and regular:
        if fstat(fd, &after) != 0:
            result = SECRET_IO
        elif (before.st_dev != after.st_dev or before.st_ino != after.st_ino
              or before.st_size != after.st_size or before.st_nlink != after.st_nlink
              or before.st_mtim.tv_sec != after.st_mtim.tv_sec
              or before.st_mtim.tv_nsec != after.st_mtim.tv_nsec
              or before.st_ctim.tv_sec != after.st_ctim.tv_sec
              or before.st_ctim.tv_nsec != after.st_ctim.tv_nsec):
            result = SECRET_CHANGED
    return _finish(fd, output, &extra, result)


cdef public const char *pa01_nv_secret_diagnostic(uint32_t status) noexcept nogil:
    if status & SECRET_CLOSE_FAILED:
        return "PA01_NV_SECRET_CLOSE_FAILED"
    if status == SECRET_OK:
        return "PA01_NV_SECRET_OK"
    if status == SECRET_ARGUMENT:
        return "PA01_NV_SECRET_ARGUMENT"
    if status == SECRET_CLOCK:
        return "PA01_NV_SECRET_CLOCK"
    if status == SECRET_FD:
        return "PA01_NV_SECRET_FD"
    if status == SECRET_SHORT:
        return "PA01_NV_SECRET_SHORT"
    if status == SECRET_EXTRA:
        return "PA01_NV_SECRET_EXTRA"
    if status == SECRET_TIMEOUT:
        return "PA01_NV_SECRET_TIMEOUT"
    if status == SECRET_IO:
        return "PA01_NV_SECRET_IO"
    if status == SECRET_CHANGED:
        return "PA01_NV_SECRET_CHANGED"
    return "PA01_NV_SECRET_ERROR"


# Adaptateur de ressource seulement ; le lanceur vérifié reste propriétaire.
cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <stddef.h>
    #include <string.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <sys/stat.h>
    #include <time.h>
    #include <errno.h>

    static uint32_t pa01_cr_time(uint64_t end, int *primary_errno) {
        struct timespec value;
        uint64_t seconds, now;
        if (clock_gettime(CLOCK_MONOTONIC, &value) != 0) {
            *primary_errno = errno; return 2;
        }
        if (value.tv_sec < 0 || value.tv_nsec < 0 || value.tv_nsec >= 1000000000) {
            *primary_errno = EOVERFLOW; return 2;
        }
        seconds = (uint64_t)value.tv_sec;
        if (seconds > (UINT64_MAX - (uint64_t)value.tv_nsec) / UINT64_C(1000000000)) {
            *primary_errno = EOVERFLOW; return 2;
        }
        now = seconds * UINT64_C(1000000000) + (uint64_t)value.tv_nsec;
        if (now == 0) { *primary_errno = EOVERFLOW; return 2; }
        return now >= end ? 6 : 0;
    }
    static void pa01_cr_close(int *owned, int *cleanup_errno) {
        int fd = *owned, saved;
        *owned = -1;
        if (fd >= 0 && close(fd) != 0) {
            saved = errno;
            if (*cleanup_errno == 0) *cleanup_errno = saved;
        }
    }
    static int pa01_cr_dir(const struct stat *st, unsigned int uid,
                          unsigned long dev, unsigned long ino, unsigned int mode) {
        return S_ISDIR(st->st_mode) && st->st_uid == uid
            && st->st_dev == dev && st->st_ino == ino
            && (st->st_mode & 07777) == mode;
    }
    static int pa01_cr_file(const struct stat *st, unsigned int uid) {
        return S_ISREG(st->st_mode) && st->st_uid == uid
            && (st->st_mode & 07777) == 0400 && st->st_nlink == 1
            && st->st_size == 32;
    }
    static int pa01_cr_same(const struct stat *a, const struct stat *b) {
        return a->st_dev == b->st_dev && a->st_ino == b->st_ino
            && a->st_mode == b->st_mode && a->st_uid == b->st_uid
            && a->st_nlink == b->st_nlink && a->st_size == b->st_size
            && a->st_mtim.tv_sec == b->st_mtim.tv_sec
            && a->st_mtim.tv_nsec == b->st_mtim.tv_nsec
            && a->st_ctim.tv_sec == b->st_ctim.tv_sec
            && a->st_ctim.tv_nsec == b->st_ctim.tv_nsec;
    }
    static uint32_t pa01_cr_open(int *out, int parent, const char *name, size_t length,
            unsigned int uid, unsigned long dev, unsigned long ino,
            unsigned int mode, uint64_t end, int *primary_errno, int *cleanup_errno) {
        int directory = -1, file = -1, flags;
        off_t offset;
        uint32_t status = 0;
        size_t i;
        char basename[256];
        struct stat first, opened, last, dir;
        if (primary_errno != NULL) *primary_errno = 0;
        if (cleanup_errno != NULL) *cleanup_errno = 0;
        if (out == NULL || primary_errno == NULL || cleanup_errno == NULL
                || *out != -1 || parent < 3 || name == NULL || length == 0
                || length > 255 || ino == 0 || end == 0
                || (mode != 0500 && mode != 0700))
            return 1;
        for (i = 0; i < length; ++i) {
            unsigned char c = (unsigned char)name[i];
            if (!((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')
                    || (c >= '0' && c <= '9') || c == '_' || c == '-'
                    || (i > 0 && c == '.')))
                return 1;
        }
        memcpy(basename, name, length); basename[length] = 0;
        #define PA01_CR_TIME() do { status = pa01_cr_time(end, primary_errno); \
            if (status != 0) goto cleanup; } while (0)
        #define PA01_CR_CALL(expr) do { PA01_CR_TIME(); if ((expr) < 0) { \
            *primary_errno = errno; status = 3; goto cleanup; } PA01_CR_TIME(); } while (0)
        PA01_CR_CALL(directory = fcntl(parent, F_DUPFD_CLOEXEC, 3));
        PA01_CR_CALL(fstat(directory, &dir));
        if (!pa01_cr_dir(&dir, uid, dev, ino, mode)) { status = 3; goto cleanup; }
        PA01_CR_CALL(fstatat(directory, basename, &first, AT_SYMLINK_NOFOLLOW));
        if (!pa01_cr_file(&first, uid)) { status = 3; goto cleanup; }
        PA01_CR_CALL(file = openat(directory, basename,
                                  O_RDONLY | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK));
        PA01_CR_CALL(fstat(file, &opened));
        if (!pa01_cr_file(&opened, uid) || !pa01_cr_same(&first, &opened)) {
            status = 8; goto cleanup;
        }
        PA01_CR_CALL(flags = fcntl(file, F_GETFL));
        if ((flags & O_ACCMODE) != O_RDONLY) { status = 3; goto cleanup; }
        PA01_CR_CALL(flags = fcntl(file, F_GETFD));
        if (!(flags & FD_CLOEXEC)) { status = 3; goto cleanup; }
        PA01_CR_TIME();
        offset = lseek(file, 0, SEEK_CUR);
        if (offset != 0) {
            if (offset < 0) *primary_errno = errno;
            status = 3; goto cleanup;
        }
        PA01_CR_TIME();
        PA01_CR_CALL(fstatat(directory, basename, &last, AT_SYMLINK_NOFOLLOW));
        if (!pa01_cr_file(&last, uid) || !pa01_cr_same(&opened, &last)) {
            status = 8; goto cleanup;
        }
        PA01_CR_CALL(fstat(directory, &dir));
        if (!pa01_cr_dir(&dir, uid, dev, ino, mode)) { status = 8; goto cleanup; }
        cleanup:
        pa01_cr_close(&directory, cleanup_errno);
        if (status == 0 && *cleanup_errno == 0)
            status = pa01_cr_time(end, primary_errno);
        if (status == 0 && *cleanup_errno == 0) {
            *out = file; file = -1;
        }
        pa01_cr_close(&file, cleanup_errno);
        #undef PA01_CR_CALL
        #undef PA01_CR_TIME
        return status | (*cleanup_errno != 0 ? UINT32_C(0x10000) : 0);
    }
    """
    uint32_t pa01_cr_open(int *, int, const char *, size_t, unsigned int,
        unsigned long, unsigned long, unsigned int, uint64_t, int *, int *) noexcept


cdef public uint32_t pa01_nv_credential_open32(int *fd_out, int dir_fd,
        const char *basename, size_t basename_len, uint32_t expected_uid,
        unsigned long expected_dev, unsigned long expected_ino,
        uint32_t expected_dir_mode, uint64_t deadline_ns,
        int *primary_errno_out, int *cleanup_errno_out) noexcept nogil:
    """Forme/identité de ressource seulement ; aucune provenance/admission."""
    return pa01_cr_open(fd_out, dir_fd, basename, basename_len, expected_uid,
        expected_dev, expected_ino, expected_dir_mode, deadline_ns,
        primary_errno_out, cleanup_errno_out)
