# Prive Z12 : garde TCTI interposable a echeance absolue, COMMON_V2.
# A inclure APRES _monotonic_deadline.pxi seul, UNE SEULE FOIS.
# _nv_read_guard.pxi inclut deadline puis TCTI ; ne pas les re-inclure a part.
# Standalone : deadline puis TCTI ; ne pas ensuite inclure _nv_read_guard.pxi.
# Ne re-inclut jamais _monotonic_deadline.pxi (double definition interdite).
# Parent TCTI natif deja initialise, reellement possede par le futur proprietaire.
# Le wrapper ne construit ni n'initialise le parent, ne le finalise pas,
# ne prouve ni autorite, ni provenance, ni fermeture des logs.
# Preemption possible entre lecture horloge et appel parent ; aucune garantie
# dure d'interruption syscall ni d'heure reelle d'arrivee TPM.
# Aucun secret, objet Python, pointeur public ou capsule ; aucun effet a inclusion.
# Aucun budget/device/config parent/privilege par defaut.
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint64_t, int32_t

cdef extern from "tss2/tss2_tcti.h" nogil:
    ctypedef struct TSS2_TCTI_CONTEXT:
        pass

cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <stddef.h>
    #include <stdlib.h>
    #include <errno.h>
    #include <limits.h>
    #include <tss2/tss2_tcti.h>
    #include <tss2/tss2_rc.h>

    #define Z12_TCTI_MAGIC UINT64_C(0x5a31325443544931)

    typedef struct {
        TSS2_TCTI_CONTEXT_COMMON_V2 common;
        TSS2_TCTI_CONTEXT *parent;
        Z12MonotonicDeadline *deadline;
        uint64_t expected_end_ns;
        int deny_transmit;
        int uncertain;
        int finalized;
        int engaged;
        int bound;
    } Z12TctiDeadline;

    static TSS2_RC z12_tcti_on_cancel_refuse(TSS2_TCTI_CONTEXT *ctx) {
        (void)ctx;
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    static TSS2_RC z12_tcti_on_getpoll_refuse(TSS2_TCTI_CONTEXT *ctx,
                                              TSS2_TCTI_POLL_HANDLE *handles,
                                              size_t *num_handles) {
        (void)ctx; (void)handles; (void)num_handles;
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    static TSS2_RC z12_tcti_on_setlocality_refuse(TSS2_TCTI_CONTEXT *ctx,
                                                  uint8_t locality) {
        (void)ctx; (void)locality;
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    static TSS2_RC z12_tcti_on_makesticky_refuse(TSS2_TCTI_CONTEXT *ctx,
                                                 TPM2_HANDLE *handle,
                                                 uint8_t sticky) {
        (void)ctx; (void)handle; (void)sticky;
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    static void z12_tcti_on_finalize(TSS2_TCTI_CONTEXT *ctx) {
        Z12TctiDeadline *guard = (Z12TctiDeadline *)ctx;
        if (guard == NULL) return;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) return;
        if (guard->finalized != 0) return;
        guard->finalized = 1;
        guard->deny_transmit = 1;
        guard->uncertain = 1;
    }

    static int z12_tcti_deadline_unchanged(const Z12TctiDeadline *guard) {
        if (guard == NULL) return 0;
        if (guard->deadline == NULL) return 0;
        if (guard->deadline->started != 1) return 0;
        if (guard->deadline->end_ns == (uint64_t)0) return 0;
        if (guard->deadline->end_ns != guard->expected_end_ns) return 0;
        return 1;
    }

    static TSS2_RC z12_tcti_on_transmit(TSS2_TCTI_CONTEXT *ctx,
                                        size_t size,
                                        const uint8_t *command) {
        Z12TctiDeadline *guard = (Z12TctiDeadline *)ctx;
        int32_t remaining_ms = 0;
        int before;
        int after;
        int32_t after_ms = 0;
        TSS2_RC rc;
        if (guard == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) {
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (guard->bound != 1) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (guard->finalized != 0) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (guard->parent == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->deadline == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->deny_transmit != 0) return TSS2_TCTI_RC_GENERAL_FAILURE;
        if (guard->engaged != 0) return TSS2_TCTI_RC_BAD_SEQUENCE;
        if (size == 0 || command == NULL) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (z12_tcti_deadline_unchanged(guard) == 0) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return TSS2_TCTI_RC_GENERAL_FAILURE;
        }
        before = z12_deadline_remaining(guard->deadline, &remaining_ms);
        if (before != 1) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return TSS2_TCTI_RC_GENERAL_FAILURE;
        }
        if (z12_tcti_deadline_unchanged(guard) == 0) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return TSS2_TCTI_RC_GENERAL_FAILURE;
        }
        guard->engaged = 1;
        rc = Tss2_Tcti_Transmit(guard->parent, size, command);
        after = z12_deadline_remaining(guard->deadline, &after_ms);
        if (after != 1 || z12_tcti_deadline_unchanged(guard) == 0) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            if (rc == TSS2_RC_SUCCESS) return TSS2_TCTI_RC_GENERAL_FAILURE;
            return rc;
        }
        if (rc == TSS2_RC_SUCCESS) return rc;
        guard->deny_transmit = 1;
        guard->uncertain = 1;
        return rc;
    }

    static TSS2_RC z12_tcti_on_receive(TSS2_TCTI_CONTEXT *ctx,
                                       size_t *size,
                                       uint8_t *response,
                                       int32_t timeout_ms) {
        Z12TctiDeadline *guard = (Z12TctiDeadline *)ctx;
        int32_t remaining_ms = 0;
        int before;
        int after;
        int32_t after_ms = 0;
        int32_t effective_ms;
        TSS2_RC rc;
        if (guard == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) {
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (guard->bound != 1) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (guard->finalized != 0) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (guard->parent == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->deadline == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (size == NULL) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (guard->engaged != 1) return TSS2_TCTI_RC_BAD_SEQUENCE;
        if (timeout_ms < 0 && timeout_ms != TSS2_TCTI_TIMEOUT_BLOCK) {
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        before = z12_deadline_remaining(guard->deadline, &remaining_ms);
        if (guard->deny_transmit == 0 && before == 1
                && z12_tcti_deadline_unchanged(guard) != 0) {
            if (timeout_ms == TSS2_TCTI_TIMEOUT_BLOCK) effective_ms = remaining_ms;
            else if (timeout_ms < 0) effective_ms = remaining_ms;
            else effective_ms = timeout_ms <= remaining_ms ? timeout_ms : remaining_ms;
            rc = Tss2_Tcti_Receive(guard->parent, size, response, effective_ms);
            after = z12_deadline_remaining(guard->deadline, &after_ms);
            if (after != 1 || z12_tcti_deadline_unchanged(guard) == 0) {
                if (rc == TSS2_RC_SUCCESS && response != NULL) guard->engaged = 0;
                guard->deny_transmit = 1;
                guard->uncertain = 1;
                if (rc == TSS2_RC_SUCCESS) return TSS2_TCTI_RC_GENERAL_FAILURE;
                if (rc == TSS2_TCTI_RC_TRY_AGAIN) return rc;
                if (rc == TSS2_TCTI_RC_INSUFFICIENT_BUFFER) return rc;
                return rc;
            }
            if (rc == TSS2_RC_SUCCESS) {
                if (response != NULL) guard->engaged = 0;
                return rc;
            }
            if (rc == TSS2_TCTI_RC_TRY_AGAIN) return rc;
            if (rc == TSS2_TCTI_RC_INSUFFICIENT_BUFFER) return rc;
            guard->deny_transmit = 1;
            guard->uncertain = 1;
            return rc;
        }
        guard->deny_transmit = 1;
        guard->uncertain = 1;
        if (timeout_ms == TSS2_TCTI_TIMEOUT_BLOCK) timeout_ms = 0;
        if (timeout_ms != TSS2_TCTI_TIMEOUT_NONE) {
            return TSS2_TCTI_RC_GENERAL_FAILURE;
        }
        rc = Tss2_Tcti_Receive(guard->parent, size, response,
                               TSS2_TCTI_TIMEOUT_NONE);
        after = z12_deadline_remaining(guard->deadline, &after_ms);
        guard->deny_transmit = 1;
        guard->uncertain = 1;
        if (rc == TSS2_RC_SUCCESS) {
            if (response != NULL) guard->engaged = 0;
            return TSS2_TCTI_RC_GENERAL_FAILURE;
        }
        if (rc == TSS2_TCTI_RC_TRY_AGAIN) return rc;
        if (rc == TSS2_TCTI_RC_INSUFFICIENT_BUFFER) return rc;
        return rc;
    }

    static Z12TctiDeadline *z12_tcti_alloc(void) {
        Z12TctiDeadline *guard;
        guard = (Z12TctiDeadline *)calloc((size_t)1, sizeof(Z12TctiDeadline));
        if (guard == NULL) return NULL;
        guard->common.v1.magic = (uint64_t)Z12_TCTI_MAGIC;
        guard->common.v1.version = (uint32_t)0;
        guard->parent = NULL;
        guard->deadline = NULL;
        guard->expected_end_ns = (uint64_t)0;
        guard->deny_transmit = 0;
        guard->uncertain = 0;
        guard->finalized = 0;
        guard->engaged = 0;
        guard->bound = 0;
        return guard;
    }

    static TSS2_TCTI_CONTEXT *z12_tcti_context(Z12TctiDeadline *guard) {
        if (guard == NULL) return NULL;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) return NULL;
        if (guard->bound != 1) return NULL;
        if (guard->finalized != 0) return NULL;
        return (TSS2_TCTI_CONTEXT *)guard;
    }

    static TSS2_RC z12_tcti_wrap(Z12TctiDeadline *guard,
                                 TSS2_TCTI_CONTEXT *parent,
                                 Z12MonotonicDeadline *deadline) {
        TSS2_TCTI_CONTEXT_COMMON_V1 *pcommon;
        int32_t probe_ms = 0;
        int alive;
        if (guard == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) {
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (guard->bound != 0) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (guard->finalized != 0) return TSS2_TCTI_RC_BAD_CONTEXT;
        if (parent == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (deadline == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (parent == (TSS2_TCTI_CONTEXT *)guard) {
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        pcommon = (TSS2_TCTI_CONTEXT_COMMON_V1 *)parent;
        if (pcommon->magic == (uint64_t)Z12_TCTI_MAGIC) {
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (pcommon->version < (uint32_t)1) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (pcommon->transmit == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (pcommon->receive == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (deadline->started != 1) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (deadline->end_ns == (uint64_t)0) return TSS2_TCTI_RC_BAD_REFERENCE;
        alive = z12_deadline_remaining(deadline, &probe_ms);
        if (alive != 1) return TSS2_TCTI_RC_GENERAL_FAILURE;
        if (deadline->started != 1) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (deadline->end_ns == (uint64_t)0) return TSS2_TCTI_RC_BAD_REFERENCE;
        guard->parent = parent;
        guard->deadline = deadline;
        guard->expected_end_ns = deadline->end_ns;
        guard->deny_transmit = 0;
        guard->uncertain = 0;
        guard->finalized = 0;
        guard->engaged = 0;
        guard->bound = 0;
        guard->common.v1.magic = (uint64_t)Z12_TCTI_MAGIC;
        guard->common.v1.version = (uint32_t)2;
        guard->common.v1.transmit = z12_tcti_on_transmit;
        guard->common.v1.receive = z12_tcti_on_receive;
        guard->common.v1.finalize = z12_tcti_on_finalize;
        guard->common.v1.cancel = z12_tcti_on_cancel_refuse;
        guard->common.v1.getPollHandles = z12_tcti_on_getpoll_refuse;
        guard->common.v1.setLocality = z12_tcti_on_setlocality_refuse;
        guard->common.makeSticky = z12_tcti_on_makesticky_refuse;
        guard->bound = 1;
        return TSS2_RC_SUCCESS;
    }

    static int z12_tcti_deny_transmit(const Z12TctiDeadline *guard) {
        if (guard == NULL) return 1;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) return 1;
        return guard->deny_transmit != 0 ? 1 : 0;
    }

    static int z12_tcti_must_destroy(const Z12TctiDeadline *guard) {
        if (guard == NULL) return 1;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) return 1;
        return guard->uncertain != 0 ? 1 : 0;
    }

    static int z12_tcti_is_finalized(const Z12TctiDeadline *guard) {
        if (guard == NULL) return 1;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) return 1;
        return guard->finalized != 0 ? 1 : 0;
    }

    static int z12_tcti_is_engaged(const Z12TctiDeadline *guard) {
        if (guard == NULL) return 0;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) return 0;
        return guard->engaged != 0 ? 1 : 0;
    }

    static TSS2_RC z12_tcti_free_private(Z12TctiDeadline **pguard) {
        Z12TctiDeadline *guard;
        if (pguard == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        guard = *pguard;
        if (guard == NULL) return TSS2_TCTI_RC_BAD_REFERENCE;
        if (guard->common.v1.magic != (uint64_t)Z12_TCTI_MAGIC) {
            return TSS2_TCTI_RC_BAD_REFERENCE;
        }
        if (guard->bound != 0 && guard->finalized == 0) {
            return TSS2_TCTI_RC_BAD_CONTEXT;
        }
        *pguard = NULL;
        free((void *)guard);
        return TSS2_RC_SUCCESS;
    }
    static int z12_tcti_is_bound_for_deadline(const TSS2_TCTI_CONTEXT *ctx, const Z12MonotonicDeadline *deadline) {
        const TSS2_TCTI_CONTEXT_COMMON_V1 *v1;
        const TSS2_TCTI_CONTEXT_COMMON_V2 *v2;
        const Z12TctiDeadline *guard;
        const TSS2_TCTI_CONTEXT_COMMON_V1 *p1;
        if (ctx == NULL || deadline == NULL) return 0;
        v1 = (const TSS2_TCTI_CONTEXT_COMMON_V1 *)ctx;
        if (v1->magic != (uint64_t)Z12_TCTI_MAGIC) return 0;
        if (v1->version != (uint32_t)2) return 0;
        if (v1->transmit != z12_tcti_on_transmit) return 0;
        if (v1->receive != z12_tcti_on_receive) return 0;
        if (v1->finalize != z12_tcti_on_finalize) return 0;
        if (v1->cancel != z12_tcti_on_cancel_refuse) return 0;
        if (v1->getPollHandles != z12_tcti_on_getpoll_refuse) return 0;
        if (v1->setLocality != z12_tcti_on_setlocality_refuse) return 0;
        v2 = (const TSS2_TCTI_CONTEXT_COMMON_V2 *)ctx;
        if (v2->makeSticky != z12_tcti_on_makesticky_refuse) return 0;
        guard = (const Z12TctiDeadline *)ctx;
        if (guard->bound != 1) return 0;
        if (guard->finalized != 0) return 0;
        if (guard->deny_transmit != 0) return 0;
        if (guard->uncertain != 0) return 0;
        if (guard->parent == NULL) return 0;
        if (guard->parent == ctx) return 0;
        p1 = (const TSS2_TCTI_CONTEXT_COMMON_V1 *)guard->parent;
        if (p1->magic == (uint64_t)Z12_TCTI_MAGIC) return 0;
        if (p1->version < (uint32_t)1) return 0;
        if (p1->transmit == NULL || p1->receive == NULL) return 0;
        if (guard->deadline != deadline) return 0;
        if (deadline->started != 1) return 0;
        if (deadline->end_ns == (uint64_t)0) return 0;
        if (guard->expected_end_ns != deadline->end_ns) return 0;
        return 1;
    }
    """
    ctypedef struct Z12TctiDeadline:
        pass
    Z12TctiDeadline *z12_tcti_alloc() noexcept
    TSS2_TCTI_CONTEXT *z12_tcti_context(Z12TctiDeadline *guard) noexcept
    unsigned int z12_tcti_wrap(Z12TctiDeadline *guard, TSS2_TCTI_CONTEXT *parent, Z12MonotonicDeadline *deadline) noexcept
    int z12_tcti_deny_transmit(const Z12TctiDeadline *guard) noexcept
    int z12_tcti_must_destroy(const Z12TctiDeadline *guard) noexcept
    int z12_tcti_is_finalized(const Z12TctiDeadline *guard) noexcept
    int z12_tcti_is_engaged(const Z12TctiDeadline *guard) noexcept
    unsigned int z12_tcti_free_private(Z12TctiDeadline **pguard) noexcept
