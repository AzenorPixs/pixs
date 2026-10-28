# cython: language_level=3
"""Stockage POSIX privé PA : reçus locaux, jamais autorité ou ancre TPM.

Le propriétaire natif prête un profil protégé et un OSSL_LIB_CTX vivant/exclusif.
Il garantit absence d'alias, de concurrence et de fork pendant les appels.
Le répertoire persistant existe déjà, distinct de la distribution runtime.
Ce module ne crée ni ne répare un journal et ne reçoit aucun secret.
"""
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint32_t, uint64_t
from libc.stdlib cimport malloc, free, calloc
from libc.string cimport memcpy, memcmp, memset

cdef extern from "time.h":
    cdef struct timespec:
        long tv_sec
        long tv_nsec
    int CLOCK_MONOTONIC
    int clock_gettime(int, timespec *) noexcept nogil
cdef extern from "sys/types.h":
    ctypedef long ssize_t
    ctypedef long off_t
cdef extern from "sys/stat.h":
    cdef struct stat:
        unsigned long st_dev
        unsigned long st_ino
        unsigned long st_nlink
        unsigned int st_mode
        unsigned int st_uid
        long st_size
    int fstat(int, stat *) noexcept nogil
    int fstatat(int, const char *, stat *, int) noexcept nogil
    int S_ISREG(unsigned int) noexcept nogil
    int S_ISDIR(unsigned int) noexcept nogil
cdef extern from "fcntl.h":
    int O_RDWR
    int O_APPEND
    int O_NOFOLLOW
    int O_CLOEXEC
    int O_NONBLOCK
    int F_DUPFD_CLOEXEC
    int AT_SYMLINK_NOFOLLOW
    int fcntl(int, int, ...) noexcept nogil
    int openat(int, const char *, int, ...) noexcept nogil
cdef extern from "sys/file.h":
    int flock(int, int) noexcept nogil
    int LOCK_EX
    int LOCK_NB
    int LOCK_UN
cdef extern from "unistd.h":
    unsigned int geteuid() noexcept nogil
    int getpid() noexcept nogil
    ssize_t pread(int, void *, size_t, off_t) noexcept nogil
    ssize_t write(int, const void *, size_t) noexcept nogil
    int close(int) noexcept nogil
    int fsync(int) noexcept nogil
cdef extern from "errno.h":
    int errno
    int EINTR
cdef extern from "openssl/crypto.h":
    void OPENSSL_cleanse(void *, size_t) noexcept nogil
cdef extern from "openssl/evp.h":
    ctypedef struct OSSL_LIB_CTX:
        pass
    int EVP_Q_digest(OSSL_LIB_CTX *, const char *, const char *,
                     const void *, size_t, unsigned char *, size_t *) noexcept nogil

cdef enum:
    J_OK = 0
    J_ARGUMENT = 1
    J_MEMORY = 2
    J_CLOCK = 3
    J_FD = 4
    J_STATE = 5
    J_EXPIRED = 6
    J_VERIFY = 7
    J_IO = 8
    J_IN_DOUBT = 9
    J_LOCK = 10
    J_CRYPTO = 11
    J_CLEANUP = 12
    J_LIVE = 0
    J_DOUBT = 1
    J_FAILED = 2

# Longueurs littérales vérifiées : 22 et 29 octets, LF compris.
cdef const char *_PREFIX = "PIXS:PA:JOURNAL:1.0.0\n"
cdef const char *_REC_PREFIX = "PIXS:PA:JOURNAL:RECORD:1.0.0\n"
cdef struct _Journal:
    int dir_fd
    int file_fd
    int locked
    int owner_pid
    uint32_t uid
    uint64_t deadline
    uint32_t max_record
    uint64_t max_bytes
    uint32_t max_records
    OSSL_LIB_CTX *crypto
    uint8_t receipt[32]
    uint64_t local_size
    uint32_t records
    int health
    uint32_t failure
    void *lease_owner
    unsigned long dir_dev
    unsigned long dir_ino
    unsigned long file_dev
    unsigned long file_ino
    char basename[256]

cdef uint64_t _now() noexcept nogil:
    cdef timespec value
    if clock_gettime(CLOCK_MONOTONIC, &value) != 0:
        return 0
    if (value.tv_sec < 0 or <uint64_t>value.tv_sec >= ((~<uint64_t>0) // 1000000000)
            or value.tv_nsec < 0 or value.tv_nsec >= 1000000000):
        return 0
    return <uint64_t>value.tv_sec * 1000000000 + <uint64_t>value.tv_nsec

cdef uint32_t _time(_Journal *st) noexcept nogil:
    cdef uint64_t now = _now()
    if now == 0:
        return J_CLOCK
    if now >= st.deadline:
        return J_EXPIRED
    return J_OK

cdef int _basename_ok(const char *name, size_t length) noexcept nogil:
    cdef size_t i
    cdef uint8_t c
    if name == NULL or length == 0 or length > 255:
        return 0
    for i in range(length):
        c = <uint8_t>name[i]
        if not (65 <= c <= 90 or 97 <= c <= 122 or 48 <= c <= 57
                or c == 95 or c == 45 or (i > 0 and c == 46)):
            return 0
    return 1


cdef uint32_t _directory(_Journal *st) noexcept nogil:
    cdef stat info
    cdef uint32_t status = _time(st)
    if status != J_OK:
        return status
    if getpid() != st.owner_pid or geteuid() != st.uid:
        return J_STATE
    if fstat(st.dir_fd, &info) != 0:
        return J_FD
    if (not S_ISDIR(info.st_mode) or info.st_dev != st.dir_dev
            or info.st_ino != st.dir_ino or info.st_uid != st.uid
            or (info.st_mode & 0o7777) != 0o700 or info.st_nlink < 2):
        return J_VERIFY
    return _time(st)

cdef uint32_t _named_file(_Journal *st) noexcept nogil:
    cdef stat info
    if fstatat(st.dir_fd, st.basename, &info, AT_SYMLINK_NOFOLLOW) != 0:
        return J_FD
    if (not S_ISREG(info.st_mode) or info.st_dev != st.file_dev
            or info.st_ino != st.file_ino or info.st_uid != st.uid
            or (info.st_mode & 0o7777) != 0o600 or info.st_nlink != 1):
        return J_VERIFY
    return _time(st)

cdef uint32_t _identity(_Journal *st, uint64_t expected_size) noexcept nogil:
    cdef stat directory, opened, named
    cdef uint32_t status = _time(st)
    if status != J_OK:
        return status
    if getpid() != st.owner_pid or geteuid() != st.uid:
        return J_STATE
    if (fstat(st.dir_fd, &directory) != 0 or fstat(st.file_fd, &opened) != 0
            or fstatat(st.dir_fd, st.basename, &named, AT_SYMLINK_NOFOLLOW) != 0):
        return J_IO
    if (not S_ISDIR(directory.st_mode) or directory.st_dev != st.dir_dev
            or directory.st_ino != st.dir_ino or directory.st_uid != st.uid
            or (directory.st_mode & 0o7777) != 0o700 or directory.st_nlink < 2):
        return J_VERIFY
    if (not S_ISREG(opened.st_mode) or not S_ISREG(named.st_mode)
            or opened.st_dev != st.file_dev or named.st_dev != st.file_dev
            or opened.st_ino != st.file_ino or named.st_ino != st.file_ino
            or opened.st_uid != st.uid or named.st_uid != st.uid
            or (opened.st_mode & 0o7777) != 0o600 or (named.st_mode & 0o7777) != 0o600
            or opened.st_nlink != 1 or named.st_nlink != 1
            or opened.st_size < 0 or named.st_size < 0
            or <uint64_t>opened.st_size != expected_size
            or <uint64_t>named.st_size != expected_size):
        return J_VERIFY
    return _time(st)

cdef uint32_t _pread_exact(_Journal *st, uint8_t *out, size_t length,
                           uint64_t offset) noexcept nogil:
    cdef size_t done = 0
    cdef ssize_t amount
    cdef uint32_t status
    while done < length:
        status = _time(st)
        if status != J_OK:
            return status
        amount = pread(st.file_fd, out + done, length - done, <off_t>(offset + done))
        if amount < 0:
            if errno == EINTR:
                continue
            return J_IO
        if amount == 0 or <size_t>amount > length - done:
            return J_IO
        done += <size_t>amount
    return _time(st)

cdef uint32_t _digest_frame(_Journal *st, const uint8_t *previous,
        const uint8_t *length4, const uint8_t *payload, size_t length,
        uint8_t *out) noexcept nogil:
    cdef size_t total = 29 + 32 + 4 + length
    cdef size_t digest_size = 0
    cdef uint32_t status
    cdef uint8_t *data = <uint8_t *>malloc(total)
    if data == NULL:
        return J_MEMORY
    memcpy(data, _REC_PREFIX, 29)
    memcpy(data + 29, previous, 32)
    memcpy(data + 61, length4, 4)
    memcpy(data + 65, payload, length)
    if EVP_Q_digest(st.crypto, "SHA256", "provider=default",
                    data, total, out, &digest_size) != 1 or digest_size != 32:
        status = J_CRYPTO
        OPENSSL_cleanse(out, 32)
    else:
        status = _time(st)
    OPENSSL_cleanse(data, total)
    free(data)
    return status

cdef uint32_t _scan(_Journal *st, int select_record, uint32_t selected,
        uint8_t *copy, size_t copy_size, size_t *copied,
        uint8_t *selected_receipt, uint8_t *tail, uint64_t *file_size,
        uint32_t *record_count) noexcept nogil:
    cdef stat info
    cdef uint64_t size, offset = 22
    cdef uint32_t count = 0, length, status
    cdef uint8_t previous[32]
    cdef uint8_t length4[4]
    cdef uint8_t expected[32]
    cdef uint8_t actual[32]
    cdef uint8_t prefix[22]
    cdef uint8_t *payload = NULL
    status = _time(st)
    if status != J_OK:
        return status
    if fstat(st.file_fd, &info) != 0:
        return J_IO
    if info.st_size < 59 or <uint64_t>info.st_size > st.max_bytes:
        return J_VERIFY
    size = <uint64_t>info.st_size
    status = _identity(st, size)
    if status != J_OK:
        return status
    status = _pread_exact(st, prefix, 22, 0)
    if status != J_OK:
        return status
    if memcmp(prefix, _PREFIX, 22) != 0:
        return J_VERIFY
    memset(previous, 0, 32)
    if copied != NULL:
        copied[0] = 0
    while offset < size:
        if count >= st.max_records or size - offset < 37:
            return J_VERIFY
        status = _pread_exact(st, length4, 4, offset)
        if status != J_OK:
            return status
        length = ((<uint32_t>length4[0] << 24) | (<uint32_t>length4[1] << 16)
                  | (<uint32_t>length4[2] << 8) | <uint32_t>length4[3])
        if length == 0 or length > st.max_record or <uint64_t>length + 36 > size - offset:
            return J_VERIFY
        if select_record and count == selected and copy_size < length:
            return J_ARGUMENT
        payload = <uint8_t *>malloc(length)
        if payload == NULL:
            return J_MEMORY
        status = _pread_exact(st, payload, length, offset + 4)
        if status == J_OK:
            status = _pread_exact(st, actual, 32, offset + 4 + length)
        if status == J_OK:
            status = _digest_frame(st, previous, length4, payload, length, expected)
        if status == J_OK and memcmp(actual, expected, 32) != 0:
            status = J_VERIFY
        if status == J_OK and select_record and count == selected:
            memcpy(copy, payload, length)
            memcpy(selected_receipt, expected, 32)
            copied[0] = length
        OPENSSL_cleanse(payload, length)
        free(payload)
        payload = NULL
        if status != J_OK:
            return status
        memcpy(previous, expected, 32)
        offset += <uint64_t>length + 36
        count += 1
    if count == 0 or offset != size:
        return J_VERIFY
    status = _identity(st, size)
    if status != J_OK:
        return status
    memcpy(tail, previous, 32)
    file_size[0] = size
    record_count[0] = count
    return J_OK

cdef uint32_t _guard(_Journal *st) noexcept nogil:
    cdef uint32_t status
    if getpid() != st.owner_pid or geteuid() != st.uid:
        return J_STATE
    if st.health == J_DOUBT:
        return J_IN_DOUBT
    if st.health != J_LIVE:
        return st.failure
    status = _time(st)
    if status != J_OK:
        st.health = J_FAILED
        st.failure = status
    return status

cdef uint32_t _same_snapshot(_Journal *st, const uint8_t *tail,
                             uint64_t size, uint32_t count) noexcept nogil:
    if (size != st.local_size or count != st.records
            or memcmp(tail, st.receipt, 32) != 0):
        return J_VERIFY
    return J_OK

cdef uint32_t _failed(_Journal *st, uint32_t status) noexcept nogil:
    if st.health == J_DOUBT:
        st.failure = status
        return J_IN_DOUBT
    if status != J_ARGUMENT:
        st.failure = status
        st.health = J_FAILED
    return status

cdef uint32_t _dispose(_Journal *st) noexcept nogil:
    cdef uint32_t cleanup = J_OK
    # Sous Linux close libère le numéro de FD même sur erreur : aucun rejeu.
    if st.file_fd >= 0:
        if st.locked and flock(st.file_fd, LOCK_UN) != 0:
            cleanup = J_CLEANUP
        if close(st.file_fd) != 0:
            cleanup = J_CLEANUP
    if st.dir_fd >= 0 and close(st.dir_fd) != 0:
        cleanup = J_CLEANUP
    OPENSSL_cleanse(st, sizeof(_Journal))
    free(st)
    return cleanup

cdef public uint32_t pa01_journal_open(void **state_out, int dir_fd,
        const char *basename, size_t basename_len, uint32_t uid_expected,
        unsigned long dir_dev_expected, unsigned long dir_ino_expected,
        unsigned long file_dev_expected, unsigned long file_ino_expected,
        uint64_t max_bytes, uint32_t max_record, uint32_t max_records,
        void *ossl_ctx, uint64_t deadline_ns) noexcept nogil:
    cdef _Journal *st
    cdef uint32_t status, cleanup
    cdef uint8_t tail[32]
    cdef uint64_t size = 0
    cdef uint32_t count = 0
    cdef uint64_t now = _now()
    if state_out == NULL or state_out[0] != NULL:
        return J_ARGUMENT
    if (dir_fd < 3 or not _basename_ok(basename, basename_len) or ossl_ctx == NULL
            or max_bytes < 59 or max_bytes > 0x7fffffffffffffff
            or max_record == 0 or <uint64_t>max_record + 58 > max_bytes
            or <size_t>max_record > (~<size_t>0) - 65 or max_records == 0
            or uid_expected != geteuid()):
        return J_ARGUMENT
    if now == 0:
        return J_CLOCK
    if deadline_ns <= now:
        return J_EXPIRED
    st = <_Journal *>calloc(1, sizeof(_Journal))
    if st == NULL:
        return J_MEMORY
    st.dir_fd = -1
    st.file_fd = -1
    st.owner_pid = getpid()
    st.uid = uid_expected
    st.dir_dev = dir_dev_expected
    st.dir_ino = dir_ino_expected
    st.file_dev = file_dev_expected
    st.file_ino = file_ino_expected
    st.deadline = deadline_ns
    st.max_record = max_record
    st.max_bytes = max_bytes
    st.max_records = max_records
    st.crypto = <OSSL_LIB_CTX *>ossl_ctx
    memcpy(st.basename, basename, basename_len)
    st.basename[basename_len] = 0
    st.dir_fd = fcntl(dir_fd, F_DUPFD_CLOEXEC, 3)
    status = J_FD
    if st.dir_fd >= 0:
        # La validation du répertoire précède l'ouverture du basename.
        status = _directory(st)
        if status == J_OK:
            status = _named_file(st)
        if status == J_OK:
            st.file_fd = openat(st.dir_fd, st.basename,
                O_RDWR | O_APPEND | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK)
            if st.file_fd < 0:
                status = J_FD
            elif flock(st.file_fd, LOCK_EX | LOCK_NB) != 0:
                status = J_LOCK
            else:
                st.locked = 1
                status = _scan(st, 0, 0, NULL, 0, NULL, NULL, tail, &size, &count)
    if status != J_OK:
        cleanup = _dispose(st)
        return cleanup if cleanup != J_OK else status
    memcpy(st.receipt, tail, 32)
    st.local_size = size
    st.records = count
    state_out[0] = st
    return J_OK

cdef public uint32_t pa01_journal_snapshot(void *state, uint8_t *receipt_out,
        size_t receipt_size, uint64_t *size_out, uint32_t *count_out) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    cdef uint8_t tail[32]
    cdef uint64_t size = 0
    cdef uint32_t count = 0, status
    if receipt_out != NULL and receipt_size == 32:
        OPENSSL_cleanse(receipt_out, 32)
    if size_out != NULL:
        size_out[0] = 0
    if count_out != NULL:
        count_out[0] = 0
    if st == NULL or receipt_out == NULL or receipt_size != 32 or size_out == NULL or count_out == NULL:
        return J_ARGUMENT
    status = _guard(st)
    if status != J_OK:
        return status
    status = _scan(st, 0, 0, NULL, 0, NULL, NULL, tail, &size, &count)
    if status == J_OK:
        status = _same_snapshot(st, tail, size, count)
    if status != J_OK:
        return _failed(st, status)
    memcpy(receipt_out, tail, 32)
    size_out[0] = size
    count_out[0] = count
    return J_OK

cdef public uint32_t pa01_journal_record_copy(void *state, uint32_t index,
        uint8_t *output, size_t capacity, size_t *length_out,
        uint8_t *receipt_out, size_t receipt_size) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    cdef uint8_t tail[32]
    cdef uint64_t size = 0
    cdef uint32_t count = 0, status
    if length_out != NULL:
        length_out[0] = 0
    if receipt_out != NULL and receipt_size == 32:
        OPENSSL_cleanse(receipt_out, 32)
    if (st == NULL or output == NULL or capacity == 0 or capacity > st.max_record
            or length_out == NULL or receipt_out == NULL or receipt_size != 32):
        return J_ARGUMENT
    OPENSSL_cleanse(output, capacity)
    status = _guard(st)
    if status != J_OK:
        return status
    if index >= st.records:
        return J_ARGUMENT
    status = _scan(st, 1, index, output, capacity, length_out,
                   receipt_out, tail, &size, &count)
    if status == J_OK:
        status = _same_snapshot(st, tail, size, count)
    if status != J_OK:
        OPENSSL_cleanse(output, capacity)
        OPENSSL_cleanse(receipt_out, 32)
        length_out[0] = 0
        return _failed(st, status)
    return J_OK

cdef uint32_t _write_exact(_Journal *st, const uint8_t *frame, size_t length) noexcept nogil:
    cdef size_t done = 0
    cdef ssize_t amount
    cdef uint32_t status
    while done < length:
        status = _time(st)
        if status != J_OK:
            return status
        amount = write(st.file_fd, frame + done, length - done)
        if amount < 0:
            if errno == EINTR:
                continue
            return J_IO
        if amount == 0 or <size_t>amount > length - done:
            return J_IO
        done += <size_t>amount
    return _time(st)

cdef uint32_t _sync(_Journal *st, int fd) noexcept nogil:
    cdef uint32_t status
    while True:
        status = _time(st)
        if status != J_OK:
            return status
        if fsync(fd) == 0:
            return _time(st)
        if errno != EINTR:
            return J_IO

cdef uint32_t _append_owned(void *state, void *lease_owner,
        const uint8_t *expected_receipt, size_t expected_receipt_size,
        uint64_t expected_size, const uint8_t *payload, size_t payload_len,
        uint8_t *receipt_out, size_t receipt_size) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    cdef uint8_t tail[32]
    cdef uint8_t digest[32]
    cdef uint64_t size = 0, next_size
    cdef uint32_t count = 0, status
    cdef size_t frame_size
    cdef uint8_t *frame
    if receipt_out != NULL and receipt_size == 32:
        OPENSSL_cleanse(receipt_out, 32)
    if (st == NULL or expected_receipt == NULL or expected_receipt_size != 32
            or payload == NULL or payload_len == 0 or payload_len > st.max_record
            or receipt_out == NULL or receipt_size != 32):
        return J_ARGUMENT
    status = _guard(st)
    if status != J_OK:
        return status
    if st.lease_owner != lease_owner:
        return J_STATE
    status = _scan(st, 0, 0, NULL, 0, NULL, NULL, tail, &size, &count)
    if status == J_OK:
        status = _same_snapshot(st, tail, size, count)
    if status != J_OK:
        return _failed(st, status)
    if (expected_size != size or memcmp(expected_receipt, tail, 32) != 0
            or count >= st.max_records or payload_len + 36 > st.max_bytes - size):
        return J_VERIFY
    frame_size = payload_len + 36
    next_size = size + frame_size
    frame = <uint8_t *>malloc(frame_size)
    if frame == NULL:
        return J_MEMORY
    frame[0] = <uint8_t>(payload_len >> 24)
    frame[1] = <uint8_t>(payload_len >> 16)
    frame[2] = <uint8_t>(payload_len >> 8)
    frame[3] = <uint8_t>payload_len
    memcpy(frame + 4, payload, payload_len)
    status = _digest_frame(st, tail, frame, frame + 4, payload_len, digest)
    if status == J_OK:
        memcpy(frame + 4 + payload_len, digest, 32)
        status = _identity(st, size)
    if status == J_OK:
        # Toute tentative d'écriture ferme le rejeu jusqu'à vérification complète.
        st.health = J_DOUBT
        status = _write_exact(st, frame, frame_size)
        if status == J_OK:
            status = _sync(st, st.file_fd)
        if status == J_OK:
            status = _sync(st, st.dir_fd)
        if status == J_OK:
            status = _scan(st, 0, 0, NULL, 0, NULL, NULL, tail, &size, &count)
        if status == J_OK and (size != next_size or count != st.records + 1
                              or memcmp(tail, digest, 32) != 0):
            status = J_VERIFY
        if status == J_OK:
            status = _time(st)
        if status == J_OK:
            memcpy(st.receipt, tail, 32)
            st.local_size = size
            st.records = count
            st.health = J_LIVE
            st.failure = J_OK
            memcpy(receipt_out, tail, 32)
    OPENSSL_cleanse(frame, frame_size)
    free(frame)
    OPENSSL_cleanse(digest, 32)
    if status != J_OK:
        return _failed(st, status)
    return J_OK

cdef public uint32_t pa01_journal_status(void *state, uint32_t *failure_out) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    cdef uint32_t status
    if st == NULL or failure_out == NULL:
        return J_ARGUMENT
    status = _guard(st)
    failure_out[0] = st.failure
    return status

cdef public uint32_t pa01_journal_close(void **state_inout,
                                     uint32_t *cleanup_out) noexcept nogil:
    cdef _Journal *st
    cdef uint32_t primary, cleanup
    if cleanup_out != NULL:
        cleanup_out[0] = J_OK
    if state_inout == NULL or state_inout[0] == NULL or cleanup_out == NULL:
        return J_ARGUMENT
    st = <_Journal *>state_inout[0]
    if getpid() != st.owner_pid:
        return J_STATE
    if st.lease_owner != NULL:
        return J_IN_DOUBT
    primary = st.failure
    if st.health == J_DOUBT:
        primary = J_IN_DOUBT
    cleanup = _dispose(st)
    state_inout[0] = NULL
    cleanup_out[0] = cleanup
    return primary if primary != J_OK else cleanup


cdef void _journal_lease_clear(uint8_t *receipt, size_t receipt_size,
        uint64_t *size, uint32_t *count, uint64_t *deadline,
        uint32_t *max_record) noexcept nogil:
    if receipt != NULL and receipt_size == 32:
        OPENSSL_cleanse(receipt, 32)
    if size != NULL:
        size[0] = 0
    if count != NULL:
        count[0] = 0
    if deadline != NULL:
        deadline[0] = 0
    if max_record != NULL:
        max_record[0] = 0


cdef uint32_t _journal_lease_export(_Journal *st, uint8_t *receipt,
        size_t receipt_size, uint64_t *size_out, uint32_t *count_out,
        uint64_t *deadline_out, uint32_t *max_record_out) noexcept nogil:
    cdef uint8_t tail[32]
    cdef uint64_t size = 0
    cdef uint32_t count = 0, status
    _journal_lease_clear(receipt, receipt_size, size_out, count_out,
                         deadline_out, max_record_out)
    if (st == NULL or receipt == NULL or receipt_size != 32 or size_out == NULL
            or count_out == NULL or deadline_out == NULL or max_record_out == NULL):
        return J_ARGUMENT
    status = _guard(st)
    if status != J_OK:
        return status
    status = _scan(st, 0, 0, NULL, 0, NULL, NULL, tail, &size, &count)
    if status == J_OK:
        status = _same_snapshot(st, tail, size, count)
    if status != J_OK:
        return _failed(st, status)
    memcpy(receipt, tail, 32)
    size_out[0] = size
    count_out[0] = count
    deadline_out[0] = st.deadline
    max_record_out[0] = st.max_record
    status = _time(st)
    if status != J_OK:
        _journal_lease_clear(receipt, receipt_size, size_out, count_out,
                             deadline_out, max_record_out)
        return _failed(st, status)
    return J_OK


cdef public uint32_t pa01_journal_lease_acquire(void *state, void *owner,
        uint8_t *receipt, size_t receipt_size, uint64_t *size,
        uint32_t *count, uint64_t *deadline, uint32_t *max_record) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    cdef uint32_t status
    _journal_lease_clear(receipt, receipt_size, size, count, deadline, max_record)
    if st == NULL or owner == NULL:
        return J_ARGUMENT
    if st.lease_owner != NULL:
        return J_STATE
    status = _journal_lease_export(st, receipt, receipt_size, size, count,
                                   deadline, max_record)
    if status == J_OK:
        st.lease_owner = owner
    return status


cdef public uint32_t pa01_journal_lease_snapshot(void *state, void *owner,
        uint8_t *receipt, size_t receipt_size, uint64_t *size,
        uint32_t *count, uint64_t *deadline, uint32_t *max_record) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    _journal_lease_clear(receipt, receipt_size, size, count, deadline, max_record)
    if st == NULL or owner == NULL:
        return J_ARGUMENT
    if st.lease_owner != owner:
        return J_STATE
    return _journal_lease_export(st, receipt, receipt_size, size, count,
                                 deadline, max_record)


cdef public uint32_t pa01_journal_lease_release(void *state, void *owner) noexcept nogil:
    cdef _Journal *st = <_Journal *>state
    if st == NULL or owner == NULL:
        return J_ARGUMENT
    if getpid() != st.owner_pid or geteuid() != st.uid:
        return J_STATE
    if st.lease_owner != owner:
        return J_STATE
    # IO synchrones connues revenues : libérer le lien ne répare pas le disque.
    st.lease_owner = NULL
    return J_OK


cdef public uint32_t pa01_journal_append(void *state,
        const uint8_t *expected_receipt, size_t expected_receipt_size,
        uint64_t expected_size, const uint8_t *payload, size_t payload_len,
        uint8_t *receipt_out, size_t receipt_size) noexcept nogil:
    return _append_owned(state, NULL, expected_receipt, expected_receipt_size,
                          expected_size, payload, payload_len, receipt_out, receipt_size)


cdef public uint32_t pa01_journal_append_leased(void *state, void *owner,
        const uint8_t *expected_receipt, size_t expected_receipt_size,
        uint64_t expected_size, const uint8_t *payload, size_t payload_len,
        uint8_t *receipt_out, size_t receipt_size) noexcept nogil:
    if owner == NULL:
        if receipt_out != NULL and receipt_size == 32:
            OPENSSL_cleanse(receipt_out, 32)
        return J_ARGUMENT
    return _append_owned(state, owner, expected_receipt, expected_receipt_size,
                          expected_size, payload, payload_len, receipt_out, receipt_size)
