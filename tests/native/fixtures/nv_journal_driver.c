/* Conducteur de TEST : IO nominales réelles, pannes explicites, aucun TPM. */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <openssl/crypto.h>
#include <openssl/provider.h>

typedef struct {
    OSSL_LIB_CTX *context;
    OSSL_PROVIDER *provider;
} JournalTestCrypto;

static uint64_t now_ns = UINT64_C(1000000000);
static unsigned write_mode, write_calls, sync_calls, sync_failure, sync_expiry;
static unsigned close_calls, close_failure;

int __real_clock_gettime(clockid_t, struct timespec *);
ssize_t __real_write(int, const void *, size_t);
int __real_fsync(int);
int __real_close(int);

int __wrap_clock_gettime(clockid_t clock, struct timespec *out) {
    if (clock != CLOCK_MONOTONIC) return __real_clock_gettime(clock, out);
    out->tv_sec = (time_t)(now_ns / UINT64_C(1000000000));
    out->tv_nsec = (long)(now_ns % UINT64_C(1000000000));
    return 0;
}

ssize_t __wrap_write(int fd, const void *data, size_t length) {
    ++write_calls;
    if (write_mode == 2 && write_calls == 1) return 0;
    if (write_mode == 3 && write_calls == 2) {
        errno = EIO;
        return -1;
    }
    if ((write_mode == 4 && write_calls == 1) || write_mode == 5) {
        if (write_mode == 5) now_ns += UINT64_C(100000000);
        errno = EINTR;
        return -1;
    }
    if ((write_mode == 1 || write_mode == 3) && write_calls == 1 && length > 3)
        length = 3;
    return __real_write(fd, data, length);
}

int __wrap_fsync(int fd) {
    int result;
    ++sync_calls;
    if (sync_failure && sync_calls == sync_failure) {
        errno = EIO;
        return -1;
    }
    result = __real_fsync(fd);
    if (sync_expiry && sync_calls == sync_expiry)
        now_ns = UINT64_C(3000000000);
    return result;
}

int __wrap_close(int fd) {
    int result = __real_close(fd);
    ++close_calls;
    if (close_failure && close_calls == close_failure) {
        errno = EIO;
        return -1;
    }
    return result;
}

void pa01_journal_test_reset(void) {
    now_ns = UINT64_C(1000000000);
    write_mode = write_calls = sync_calls = sync_failure = sync_expiry = 0;
    close_calls = close_failure = 0;
}
void pa01_journal_test_write(unsigned mode) { write_mode = mode; }
void pa01_journal_test_sync(unsigned failure, unsigned expiry) {
    sync_failure = failure;
    sync_expiry = expiry;
}
void pa01_journal_test_close_failure(unsigned call) { close_failure = call; }
void pa01_journal_test_clock(uint64_t value) { now_ns = value; }
unsigned pa01_journal_test_writes(void) { return write_calls; }
unsigned pa01_journal_test_syncs(void) { return sync_calls; }

void *pa01_journal_test_crypto_new(void) {
    JournalTestCrypto *value = calloc(1, sizeof(*value));
    if (!value) return NULL;
    value->context = OSSL_LIB_CTX_new();
    if (value->context)
        value->provider = OSSL_PROVIDER_load(value->context, "default");
    if (!value->context || !value->provider) {
        OSSL_LIB_CTX_free(value->context);
        free(value);
        return NULL;
    }
    return value;
}
void *pa01_journal_test_crypto_context(void *opaque) {
    JournalTestCrypto *value = opaque;
    return value ? value->context : NULL;
}
int pa01_journal_test_crypto_free(void *opaque) {
    JournalTestCrypto *value = opaque;
    int result;
    if (!value) return 0;
    result = OSSL_PROVIDER_unload(value->provider);
    OSSL_LIB_CTX_free(value->context);
    free(value);
    return result;
}
