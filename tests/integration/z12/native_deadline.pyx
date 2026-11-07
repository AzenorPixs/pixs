# Tests de durée monotone : horloge réelle puis fautes injectées dans cette unité seule.
# Aucun temps injecté ne constitue une preuve d'autorisation UTC ou une donnée produit.
cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <errno.h>
    #include <time.h>
    static int z12_test_clock_mode = 0;
    static struct timespec z12_test_clock_value;
    static int z12_test_clock_gettime(clockid_t which, struct timespec *value) {
        if (z12_test_clock_mode == 0) return clock_gettime(which, value);
        if (which != CLOCK_MONOTONIC || value == NULL || z12_test_clock_mode == 2) {
            errno = EIO; return -1;
        }
        *value = z12_test_clock_value;
        return 0;
    }
    #define clock_gettime z12_test_clock_gettime
    """

include "../../../src/pixs/pzt_ca/native/_monotonic_deadline.pxi"
include "../../../src/pixs/pzt_ca/native/_tcti_deadline.pxi"

cdef extern from * nogil:
    r"""
    #undef clock_gettime
    static int z12_test_deadline_case(int number) {
        Z12MonotonicDeadline deadline = {0};
        int32_t timeout = 123;
        uint64_t initial_end;
        int rc;
        int result = 1;
        z12_test_clock_mode = 1;
        z12_test_clock_value.tv_sec = 100;
        z12_test_clock_value.tv_nsec = 0;
        switch (number) {
        case 0:
            z12_test_clock_mode = 0;
            if (z12_deadline_start(&deadline, UINT64_C(1000000000)) != 1) break;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 1
                && timeout >= 0 && timeout <= 1000 && deadline.started == 1);
            break;
        case 1:
            deadline.end_ns = 55; deadline.last_seen_ns = 44; deadline.started = 1;
            rc = z12_deadline_start(&deadline, 0);
            result = !(rc == -2 && deadline.end_ns == 0 && deadline.last_seen_ns == 0 && deadline.started == 0);
            break;
        case 2:
            result = z12_deadline_start(NULL, 1) != -2;
            break;
        case 3:
            result = !(z12_deadline_remaining(NULL, &timeout) == -2 && timeout == 0);
            break;
        case 4:
            result = z12_deadline_remaining(&deadline, NULL) != -2;
            break;
        case 5:
            result = !(z12_deadline_remaining(&deadline, &timeout) == -2 && timeout == 0);
            break;
        case 6:
            if (z12_deadline_start(&deadline, 123) != 1) break;
            z12_test_clock_value.tv_nsec = 124;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 0 && timeout == 0
                && z12_deadline_remaining(&deadline, &timeout) == 0 && timeout == 0);
            break;
        case 7:
            if (z12_deadline_start(&deadline, UINT64_C(4500000)) != 1) break;
            initial_end = deadline.end_ns;
            z12_test_clock_value.tv_nsec = 1250000;
            if (z12_deadline_remaining(&deadline, &timeout) != 1 || timeout != 3) break;
            z12_test_clock_value.tv_nsec = 4490000;
            if (z12_deadline_remaining(&deadline, &timeout) != 1 || timeout != 0) break;
            z12_test_clock_value.tv_nsec = 4500000;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 0 && timeout == 0
                && deadline.end_ns == initial_end);
            break;
        case 8:
            if (z12_deadline_start(&deadline, UINT64_C(1000000000)) != 1) break;
            z12_test_clock_value.tv_sec = 99;
            errno = 0;
            rc = z12_deadline_remaining(&deadline, &timeout);
            result = !(rc == -1 && errno == EIO && timeout == 0);
            break;
        case 9:
            z12_test_clock_mode = 2;
            errno = 0;
            rc = z12_deadline_start(&deadline, 1);
            result = !(rc == -1 && errno == EIO && deadline.started == 0 && deadline.end_ns == 0);
            break;
        case 10:
            if (z12_deadline_start(&deadline, 1) != 1) break;
            z12_test_clock_mode = 2;
            errno = 0;
            rc = z12_deadline_remaining(&deadline, &timeout);
            result = !(rc == -1 && errno == EIO && timeout == 0);
            break;
        case 11:
            z12_test_clock_value.tv_nsec = -1;
            errno = 0;
            rc = z12_deadline_start(&deadline, 1);
            result = !(rc == -1 && errno == EIO && deadline.started == 0);
            break;
        case 12:
            z12_test_clock_value.tv_nsec = 1000000000L;
            errno = 0;
            rc = z12_deadline_start(&deadline, 1);
            result = !(rc == -1 && errno == EIO && deadline.started == 0);
            break;
        case 13:
            z12_test_clock_value.tv_sec = -1;
            errno = 0;
            rc = z12_deadline_start(&deadline, 1);
            result = !(rc == -1 && errno == EIO && deadline.started == 0);
            break;
        case 14:
            z12_test_clock_value.tv_sec = (time_t)(UINT64_MAX / UINT64_C(1000000000) + 1);
            errno = 0;
            rc = z12_deadline_start(&deadline, 1);
            result = !(rc == -1 && errno == EOVERFLOW && deadline.started == 0);
            break;
        case 15:
            errno = 0;
            rc = z12_deadline_start(&deadline, UINT64_MAX);
            result = !(rc == -1 && errno == EOVERFLOW && deadline.started == 0 && deadline.end_ns == 0);
            break;
        case 16:
            if (z12_deadline_start(&deadline, ((uint64_t)INT32_MAX + 1000) * UINT64_C(1000000)) != 1) break;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 1 && timeout == INT32_MAX);
            break;
        case 17:
            if (z12_deadline_start(&deadline, 1) != 1) break;
            if (z12_deadline_remaining(&deadline, &timeout) != 1 || timeout != 0) break;
            z12_test_clock_value.tv_nsec = 1;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 0 && timeout == 0);
            break;
        case 18:
            deadline.started = 1;
            result = !(z12_deadline_remaining(&deadline, &timeout) == -2 && timeout == 0);
            break;
        case 19:
            if (z12_deadline_start(&deadline, 1) != 1) break;
            z12_test_clock_value.tv_nsec = 2;
            timeout = 999;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 0 && timeout == 0);
            break;
        case 20:
            if (z12_deadline_start(&deadline, UINT64_C(10000000)) != 1) break;
            z12_test_clock_value.tv_nsec = 1000000;
            if (z12_deadline_remaining(&deadline, &timeout) != 1) break;
            z12_test_clock_value.tv_nsec = 500000;
            errno = 0;
            rc = z12_deadline_remaining(&deadline, &timeout);
            result = !(rc == -1 && errno == EIO && timeout == 0);
            break;
        case 21:
            if (z12_deadline_start(&deadline, UINT64_C(1000000)) != 1) break;
            result = !(z12_deadline_remaining(&deadline, &timeout) == 1 && timeout == 1
                && z12_deadline_remaining(&deadline, &timeout) == 1 && timeout == 1);
            break;
        default:
            result = 999;
        }
        z12_test_clock_mode = 0;
        return result;
    }
    """
    int z12_test_deadline_case(int number)


# Parent TCTI simulé : logique locale seule, sans qualification matérielle/ESYS.
cdef extern from * nogil:
    r"""
    #include <string.h>
    #define Z12_FAKE_PARENT_MAGIC UINT64_C(0x5a313246414B4531)
    typedef struct {
        TSS2_TCTI_CONTEXT_COMMON_V2 common;
        int transmit_count;
        int receive_count;
        int finalize_count;
        int advance_on_transmit;
        int advance_on_receive;
        uint64_t advance_ns;
        TSS2_RC forced_receive_rc;
        int32_t last_receive_timeout;
    } Z12FakeParent;
    static void z12_fake_advance_clock(uint64_t delta_ns) {
        uint64_t sec_add;
        uint64_t nsec;
        if (delta_ns == 0) return;
        sec_add = delta_ns / UINT64_C(1000000000);
        nsec = (uint64_t)z12_test_clock_value.tv_nsec + (delta_ns % UINT64_C(1000000000));
        z12_test_clock_value.tv_sec += (time_t)sec_add + (time_t)(nsec / UINT64_C(1000000000));
        z12_test_clock_value.tv_nsec = (long)(nsec % UINT64_C(1000000000));
    }
    static TSS2_RC z12_fake_transmit(TSS2_TCTI_CONTEXT *ctx, size_t size, const uint8_t *cmd) {
        Z12FakeParent *fake = (Z12FakeParent *)ctx;
        if (fake == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (fake->common.v1.magic != (uint64_t)Z12_FAKE_PARENT_MAGIC) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (size == 0 || cmd == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        fake->transmit_count += 1;
        if (fake->advance_on_transmit != 0) z12_fake_advance_clock(fake->advance_ns);
        return TSS2_RC_SUCCESS;
    }
    static TSS2_RC z12_fake_receive(TSS2_TCTI_CONTEXT *ctx, size_t *size, uint8_t *resp, int32_t timeout) {
        Z12FakeParent *fake = (Z12FakeParent *)ctx;
        if (fake == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (fake->common.v1.magic != (uint64_t)Z12_FAKE_PARENT_MAGIC) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (size == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        fake->last_receive_timeout = timeout;
        if (fake->forced_receive_rc != TSS2_RC_SUCCESS) {
            fake->receive_count += 1;
            return fake->forced_receive_rc;
        }
        if (resp == NULL) {
            *size = (size_t)4;
            fake->receive_count += 1;
            return TSS2_RC_SUCCESS;
        }
        if (*size < (size_t)4) {
            *size = (size_t)4;
            fake->receive_count += 1;
            return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
        }
        fake->receive_count += 1;
        if (fake->advance_on_receive != 0) z12_fake_advance_clock(fake->advance_ns);
        resp[0] = 0x54; resp[1] = 0x33; resp[2] = 0x12; resp[3] = 0x00;
        *size = (size_t)4;
        return TSS2_RC_SUCCESS;
    }
    static void z12_fake_finalize(TSS2_TCTI_CONTEXT *ctx) {
        Z12FakeParent *fake = (Z12FakeParent *)ctx;
        if (fake == NULL) return;
        if (fake->common.v1.magic != (uint64_t)Z12_FAKE_PARENT_MAGIC) return;
        fake->finalize_count += 1;
    }
    static TSS2_RC z12_fake_cancel(TSS2_TCTI_CONTEXT *ctx) { (void)ctx; return TSS2_TCTI_RC_NOT_IMPLEMENTED; }
    static TSS2_RC z12_fake_getpoll(TSS2_TCTI_CONTEXT *ctx, TSS2_TCTI_POLL_HANDLE *h, size_t *n) { (void)ctx; (void)h; (void)n; return TSS2_TCTI_RC_NOT_IMPLEMENTED; }
    static TSS2_RC z12_fake_setloc(TSS2_TCTI_CONTEXT *ctx, uint8_t l) { (void)ctx; (void)l; return TSS2_TCTI_RC_NOT_IMPLEMENTED; }
    static TSS2_RC z12_fake_sticky(TSS2_TCTI_CONTEXT *ctx, TPM2_HANDLE *hd, uint8_t s) { (void)ctx; (void)hd; (void)s; return TSS2_TCTI_RC_NOT_IMPLEMENTED; }
    static void z12_fake_init(Z12FakeParent *fake, int adv_tx, int adv_rx, uint64_t adv_ns) {
        memset((void *)fake, 0, sizeof(*fake));
        fake->common.v1.magic = (uint64_t)Z12_FAKE_PARENT_MAGIC;
        fake->common.v1.version = (uint32_t)2;
        fake->common.v1.transmit = z12_fake_transmit;
        fake->common.v1.receive = z12_fake_receive;
        fake->common.v1.finalize = z12_fake_finalize;
        fake->common.v1.cancel = z12_fake_cancel;
        fake->common.v1.getPollHandles = z12_fake_getpoll;
        fake->common.v1.setLocality = z12_fake_setloc;
        fake->common.makeSticky = z12_fake_sticky;
        fake->advance_on_transmit = adv_tx;
        fake->advance_on_receive = adv_rx;
        fake->advance_ns = adv_ns;
    }
    static int z12_test_tcti_case(int number) {
        Z12FakeParent fake;
        Z12MonotonicDeadline deadline = {0};
        Z12TctiDeadline *guard = NULL;
        TSS2_TCTI_CONTEXT *wctx = NULL;
        uint8_t cmd[4] = {0x80, 0x01, 0x00, 0x0A};
        uint8_t resp[8];
        size_t sz = 0;
        TSS2_RC rc;
        TSS2_RC frc;
        int result = 1;
        z12_test_clock_mode = 1;
        z12_test_clock_value.tv_sec = 100;
        z12_test_clock_value.tv_nsec = 0;
        if (number == 0) z12_fake_init(&fake, 0, 0, 0);
        else if (number == 1) z12_fake_init(&fake, 0, 0, 0);
        else if (number == 2) z12_fake_init(&fake, 1, 0, UINT64_C(1000000));
        else if (number == 3) z12_fake_init(&fake, 0, 1, UINT64_C(1000000));
        else if (number == 4) z12_fake_init(&fake, 0, 0, 0);
        else if (number == 5) z12_fake_init(&fake, 0, 0, 0);
        else if (number == 6) z12_fake_init(&fake, 0, 0, 0);
        else if (number == 7) z12_fake_init(&fake, 0, 0, 0);
        else { z12_test_clock_mode = 0; return 999; }
        guard = z12_tcti_alloc();
        if (guard == NULL) { result = 2; goto cleanup; }
        switch (number) {
        case 0: {
            if (z12_deadline_start(&deadline, UINT64_C(1000000000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            if (z12_tcti_is_engaged(guard) != 1) break;
            if (fake.transmit_count != 1) break;
            sz = 0;
            if (Tss2_Tcti_Receive(wctx, &sz, NULL, TSS2_TCTI_TIMEOUT_BLOCK) != TSS2_RC_SUCCESS) break;
            if (sz != (size_t)4) break;
            if (z12_tcti_is_engaged(guard) != 1) break;
            memset(resp, 0xAA, sizeof(resp));
            sz = sizeof(resp);
            if (Tss2_Tcti_Receive(wctx, &sz, resp, TSS2_TCTI_TIMEOUT_BLOCK) != TSS2_RC_SUCCESS) break;
            if (sz != (size_t)4) break;
            if (!(resp[0] == 0x54 && resp[1] == 0x33 && resp[2] == 0x12 && resp[3] == 0x00)) break;
            if (z12_tcti_is_engaged(guard) != 0) break;
            if (fake.transmit_count != 1 || fake.receive_count != 2) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            if (fake.transmit_count != 2) break;
            if (z12_tcti_deny_transmit(guard) != 0 || z12_tcti_must_destroy(guard) != 0) break;
            result = 0;
            break;
        }
        case 1: {
            if (z12_deadline_start(&deadline, UINT64_C(1000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            z12_test_clock_value.tv_sec = (time_t)(deadline.end_ns / UINT64_C(1000000000));
            z12_test_clock_value.tv_nsec = (long)(deadline.end_ns % UINT64_C(1000000000));
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 0) break;
            if (z12_tcti_is_engaged(guard) != 0) break;
            if (z12_tcti_deny_transmit(guard) != 1) break;
            if (z12_tcti_must_destroy(guard) != 1) break;
            result = 0;
            break;
        }
        case 2: {
            if (z12_deadline_start(&deadline, UINT64_C(1000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 1) break;
            if (z12_tcti_is_engaged(guard) != 1) break;
            if (z12_tcti_deny_transmit(guard) != 1) break;
            if (z12_tcti_must_destroy(guard) != 1) break;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 1) break;
            result = 0;
            break;
        }
        case 3: {
            if (z12_deadline_start(&deadline, UINT64_C(100000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            if (fake.transmit_count != 1) break;
            memset(resp, 0xAA, sizeof(resp));
            sz = sizeof(resp);
            rc = Tss2_Tcti_Receive(wctx, &sz, resp, TSS2_TCTI_TIMEOUT_BLOCK);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (sz != (size_t)4) break;
            if (z12_tcti_is_engaged(guard) != 0) break;
            if (z12_tcti_deny_transmit(guard) != 1) break;
            if (z12_tcti_must_destroy(guard) != 1) break;
            if (fake.transmit_count != 1 || fake.receive_count != 1) break;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 1 || fake.receive_count != 1) break;
            result = 0;
            break;
        }
        case 4: {
            if (z12_deadline_start(&deadline, UINT64_C(10000000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            fake.forced_receive_rc = TSS2_TCTI_RC_TRY_AGAIN;
            memset(resp, 0xAA, sizeof(resp));
            sz = sizeof(resp);
            rc = Tss2_Tcti_Receive(wctx, &sz, resp, TSS2_TCTI_TIMEOUT_BLOCK);
            if (rc != TSS2_TCTI_RC_TRY_AGAIN) break;
            if (z12_tcti_deny_transmit(guard) != 0 || z12_tcti_must_destroy(guard) != 0) break;
            if (z12_tcti_is_engaged(guard) != 1) break;
            fake.forced_receive_rc = TSS2_RC_SUCCESS;
            sz = (size_t)2;
            rc = Tss2_Tcti_Receive(wctx, &sz, resp, TSS2_TCTI_TIMEOUT_BLOCK);
            if (rc != TSS2_TCTI_RC_INSUFFICIENT_BUFFER) break;
            if (sz != (size_t)4) break;
            if (z12_tcti_deny_transmit(guard) != 0 || z12_tcti_must_destroy(guard) != 0) break;
            if (z12_tcti_is_engaged(guard) != 1) break;
            memset(resp, 0xAA, sizeof(resp));
            sz = sizeof(resp);
            if (Tss2_Tcti_Receive(wctx, &sz, resp, TSS2_TCTI_TIMEOUT_BLOCK) != TSS2_RC_SUCCESS) break;
            if (sz != (size_t)4) break;
            if (!(resp[0]==0x54 && resp[1]==0x33 && resp[2]==0x12 && resp[3]==0x00)) break;
            if (z12_tcti_is_engaged(guard) != 0) break;
            if (z12_tcti_deny_transmit(guard) != 0 || z12_tcti_must_destroy(guard) != 0) break;
            if (fake.transmit_count != 1 || fake.receive_count != 3) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            if (fake.transmit_count != 2) break;
            if (z12_tcti_deny_transmit(guard) != 0 || z12_tcti_must_destroy(guard) != 0) break;
            result = 0;
            break;
        }
        case 5: {
            if (z12_deadline_start(&deadline, UINT64_C(10000000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            z12_test_clock_mode = 2;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 0) break;
            if (z12_tcti_is_engaged(guard) != 0) break;
            if (z12_tcti_deny_transmit(guard) != 1 || z12_tcti_must_destroy(guard) != 1) break;
            z12_test_clock_mode = 1;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 0) break;
            if (z12_tcti_deny_transmit(guard) != 1 || z12_tcti_must_destroy(guard) != 1) break;
            result = 0;
            break;
        }
        case 6: {
            if (z12_deadline_start(&deadline, UINT64_C(10000000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            memset(resp, 0xAA, sizeof(resp));
            sz = sizeof(resp);
            if (Tss2_Tcti_Receive(wctx, &sz, resp, TSS2_TCTI_TIMEOUT_BLOCK) != TSS2_RC_SUCCESS) break;
            if (fake.last_receive_timeout != 10 || fake.last_receive_timeout == TSS2_TCTI_TIMEOUT_BLOCK) break;
            if (Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd) != TSS2_RC_SUCCESS) break;
            sz = sizeof(resp);
            rc = Tss2_Tcti_Receive(wctx, &sz, resp, (int32_t)-2);
            if (rc != TSS2_TCTI_RC_BAD_VALUE) break;
            if (fake.receive_count != 1) break;
            if (fake.last_receive_timeout != 10) break;
            if (z12_tcti_deny_transmit(guard) != 1 || z12_tcti_must_destroy(guard) != 1) break;
            if (fake.transmit_count != 2 || fake.receive_count != 1) break;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 2 || fake.receive_count != 1) break;
            result = 0;
            break;
        }
        case 7: {
            uint64_t saved_end = 0;
            if (z12_deadline_start(&deadline, UINT64_C(100000)) != 1) break;
            if (z12_tcti_wrap(guard, (TSS2_TCTI_CONTEXT *)&fake, &deadline) != TSS2_RC_SUCCESS) break;
            wctx = z12_tcti_context(guard);
            if (wctx == NULL) break;
            saved_end = deadline.end_ns;
            deadline.end_ns = saved_end + UINT64_C(1);
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 0) break;
            if (z12_tcti_deny_transmit(guard) != 1 || z12_tcti_must_destroy(guard) != 1) break;
            deadline.end_ns = saved_end;
            rc = Tss2_Tcti_Transmit(wctx, sizeof(cmd), cmd);
            if (rc != TSS2_TCTI_RC_GENERAL_FAILURE) break;
            if (fake.transmit_count != 0) break;
            result = 0;
            break;
        }
        default:
            result = 999;
            break;
        }
    cleanup: {
        TSS2_TCTI_CONTEXT *fctx = NULL;
        int fres = 0;
        if (guard != NULL) {
            fctx = wctx != NULL ? wctx : (TSS2_TCTI_CONTEXT *)guard;
            if (z12_tcti_is_finalized(guard) == 0) Tss2_Tcti_Finalize(fctx);
            if (z12_tcti_is_finalized(guard) == 0) fres = 20;
            frc = z12_tcti_free_private(&guard);
            if (frc != TSS2_RC_SUCCESS || guard != NULL) fres = 21;
            if (fake.finalize_count != 0) fres = 22;
            if (fres != 0 && result == 0) result = fres;
        } else {
            if (fake.finalize_count != 0 && result == 0) result = 23;
        }
        z12_test_clock_mode = 0;
        return result;
    }
    }
    """
    int z12_test_tcti_case(int number)


def run_tests():
    """Durées et garde TCTI à parent simulé ; aucune qualification UTC ou TPM."""
    cdef int number
    cdef int result
    names = (
        "horloge_monotone_reelle", "budget_nul_efface_etat", "destination_nulle",
        "echeance_nulle", "sortie_nulle", "echeance_non_initialisee",
        "expiration_repetee", "budget_partage_sans_reinitialisation", "recul_initial",
        "erreur_horloge_debut", "erreur_horloge_lecture", "nanosecondes_negatives",
        "nanosecondes_hors_borne", "secondes_negatives", "debordement_horodatage",
        "debordement_budget", "timeout_plafonne", "budget_une_nanoseconde",
        "etat_incomplet", "timeout_perime_efface", "recul_entre_deux_etapes",
        "lectures_monotones_egales",
    )
    tcti_names = (
        "tcti_T0_wrap_transmit_query_receive_renvoi",
        "tcti_T1_expiration_exacte_compteur_parent_nul",
        "tcti_T2_transmit_tardif_sticky_renvoi_refuse",
        "tcti_T3_receive_tardif_pending_traite_sans_renvoi",
        "tcti_T4_tryagain_insuffisant_succession_sans_deny",
        "tcti_T5_horloge_erreur_sans_reouverture",
        "tcti_T6_block_fini_exact_puis_invalide_refuse",
        "tcti_T7_end_lie_modifie_sticky_apres_restauration",
    )
    if globals().get("__pyx_capi__"):
        raise AssertionError("ABI publique Cython inattendue")
    for number in range(len(names)):
        result = z12_test_deadline_case(number)
        if result != 0:
            raise AssertionError("Echec echeance native : " + names[number] + "; code=" + str(result))
    for number in range(len(tcti_names)):
        result = z12_test_tcti_case(number)
        if result != 0:
            raise AssertionError("Echec TCTI natif : " + tcti_names[number] + "; code=" + str(result))
    return {"cas": len(names) + len(tcti_names), "cas_monotones": len(names), "cas_tcti": len(tcti_names), "source_utc_qualifiee": False, "effet_tpm_nv": False}


if __name__ == "__main__":
    import json
    print(json.dumps(run_tests(), sort_keys=True))
