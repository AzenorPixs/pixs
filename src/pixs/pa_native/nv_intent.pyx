# cython: language_level=3
"""Reçu privé d'intention IO, sans admission ni extension TPM.

Le natif exclusif fournit journal/lecteur réels, pin initial et bornes protégés.
Le codec postgresql_contracts doit être compilé et initialisé explicitement.
Aucun secret, handle Python, capsule ou API de confirmation déclarative.
"""
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint32_t, uint64_t
from libc.stdlib cimport calloc, malloc, free
from libc.string cimport memcpy, memcmp
import postgresql_contracts as _codec

cdef extern from "unistd.h" nogil:
    int getpid() noexcept
    unsigned int geteuid() noexcept

cdef extern from "openssl/crypto.h" nogil:
    void OPENSSL_cleanse(void *, size_t) noexcept

cdef extern from "nv_journal.h" nogil:
    uint32_t pa01_journal_lease_acquire(void *, void *, uint8_t *, size_t,
        uint64_t *, uint32_t *, uint64_t *, uint32_t *) noexcept
    uint32_t pa01_journal_lease_snapshot(void *, void *, uint8_t *, size_t,
        uint64_t *, uint32_t *, uint64_t *, uint32_t *) noexcept
    uint32_t pa01_journal_record_copy(void *, uint32_t, uint8_t *, size_t,
        size_t *, uint8_t *, size_t) noexcept
    uint32_t pa01_journal_append_leased(void *, void *, const uint8_t *, size_t,
        uint64_t, const uint8_t *, size_t, uint8_t *, size_t) noexcept
    uint32_t pa01_journal_lease_release(void *, void *) noexcept

cdef extern from "nv_anchor.h" nogil:
    uint32_t pa01_nv_lease_acquire(void *, void *, uint8_t *, size_t,
        uint8_t *, size_t, uint32_t *, uint64_t *) noexcept
    uint32_t pa01_nv_lease_snapshot(void *, void *, uint8_t *, size_t,
        uint8_t *, size_t, uint32_t *, uint64_t *) noexcept
    uint32_t pa01_nv_lease_release(void *, void *) noexcept
    uint32_t pa01_nv_lease_read_serial(void *, void *, uint64_t *) noexcept
    uint32_t pa01_nv_lease_quiescent(void *, void *) noexcept
    uint32_t pa01_nv_extend_abort_fact(void *, void *, void *) noexcept
    uint32_t pa01_nv_lease_refresh_start(void *, void *) noexcept
    uint32_t pa01_nv_auth_step(void *) noexcept

cdef enum:
    I_OK = 0
    I_ARGUMENT = 1
    I_MEMORY = 2
    I_STATE = 4
    I_VERIFY = 7
    I_IN_DOUBT = 9
    I_CONSUMED = 14
    I_PREPARING = 0
    I_PREPARED = 1
    I_CLAIMED = 2
    I_BROKEN = 3
    I_CONFIRMED = 4
    I_OBSERVING = 5
    I_OBSERVED = 6
    I_OBSERVE_FAILED = 7
    O_HEAD_MATCH = 0
    O_TAIL_UNANCHORED = 1
    O_DIVERGED = 2

cdef struct _Observed:
    uint8_t receipt[32]
    uint64_t size
    uint32_t count
    uint64_t journal_deadline
    uint32_t max_record
    uint8_t nv[32]
    uint8_t name[34]
    uint32_t index
    uint64_t nv_deadline
    uint64_t read_serial

cdef struct _Intent:
    int pid
    unsigned int uid
    int phase
    int journal_held
    int nv_held
    int append_attempted
    void *journal
    void *reader
    void *consumer
    _Observed observed
    uint8_t first_head[32]
    uint8_t head[32]
    uint8_t expected_nv[32]
    uint64_t baseline_serial
    uint32_t observe_class
    uint32_t observe_failure
    uint32_t observe_source
    uint32_t observe_stage
    uint32_t obs_max_json
    uint32_t obs_max_ref
    uint64_t obs_max_epoch
    uint64_t obs_max_sequence
    uint32_t obs_max_correlation
    uint32_t obs_max_causation

cdef void _detail_clear(uint32_t *detail) noexcept nogil:
    cdef int i
    if detail != NULL:
        for i in range(4):
            detail[i] = 0

cdef uint32_t _source_failure(uint32_t rc, uint32_t stage,
        uint32_t *detail) noexcept nogil:
    detail[0] = stage
    detail[1] = rc
    return I_IN_DOUBT if rc == 9 else I_STATE

cdef uint32_t _observe(_Intent *it, _Observed *value,
        uint32_t *detail) noexcept nogil:
    cdef uint32_t rc
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    rc = pa01_journal_lease_snapshot(it.journal, <void *>it,
        value.receipt, 32, &value.size, &value.count,
        &value.journal_deadline, &value.max_record)
    if rc != 0:
        return _source_failure(rc, 1, detail)
    rc = pa01_nv_lease_snapshot(it.reader, <void *>it, value.nv, 32,
        value.name, 34, &value.index, &value.nv_deadline)
    if rc != 0:
        return _source_failure(rc, 2, detail)
    rc = pa01_nv_lease_read_serial(it.reader, <void *>it, &value.read_serial)
    if rc != 0:
        return _source_failure(rc, 2, detail)
    if value.journal_deadline != value.nv_deadline:
        return I_VERIFY
    return I_OK

cdef int _same_nv(_Observed *a, _Observed *b) noexcept nogil:
    return (a.nv_deadline == b.nv_deadline and a.read_serial == b.read_serial
        and a.journal_deadline == b.journal_deadline
        and a.index == b.index and memcmp(a.nv, b.nv, 32) == 0
        and memcmp(a.name, b.name, 34) == 0)

cdef int _same(_Observed *a, _Observed *b) noexcept nogil:
    return (_same_nv(a, b) and a.size == b.size and a.count == b.count
        and a.max_record == b.max_record
        and memcmp(a.receipt, b.receipt, 32) == 0)

cdef uint32_t _detach(_Intent *it, uint32_t *detail) noexcept nogil:
    cdef uint32_t rc
    # Ne jamais libérer la mémoire owner tant qu'un lien subsiste.
    if getpid() != it.pid or geteuid() != it.uid:
        detail[2] = I_STATE
        detail[3] = I_STATE
        return I_IN_DOUBT
    if it.nv_held:
        rc = pa01_nv_lease_release(it.reader, <void *>it)
        detail[3] = rc
        if rc != 0:
            return I_IN_DOUBT
        it.nv_held = 0
    if it.journal_held:
        rc = pa01_journal_lease_release(it.journal, <void *>it)
        detail[2] = rc
        if rc != 0:
            return I_IN_DOUBT
        it.journal_held = 0
    return I_OK

cdef void _dispose(_Intent *it) noexcept nogil:
    OPENSSL_cleanse(it, sizeof(_Intent))
    free(it)

cdef object _canonical(bytes raw, object limits):
    cdef object transition = _codec.decode_journal_transition(
        raw.decode("utf-8"), limits)
    if _codec.encode_journal_transition(transition, limits).encode("utf-8") != raw:
        raise _codec.ContractError("PA01_INTENT_CANONICAL_REQUIRED")
    return transition

cdef object _context(object transition):
    return (transition.installation_ref, transition.target_ref,
        transition.registry_ref, transition.registry_generation_ref,
        transition.epoch)

cdef object _scan_history(_Intent *it, const uint8_t *pin, uint8_t *buffer, size_t capacity, object limits, uint32_t *detail):
    cdef uint32_t i, rc
    cdef size_t copied = 0
    cdef uint8_t receipt[32]
    cdef object previous = None
    cdef object context = None
    cdef object seen = set()
    cdef object previous_head = None
    cdef object previous_nv = None
    cdef object transition, head, expected, raw
    for i in range(it.observed.count):
        rc = pa01_journal_record_copy(it.journal, i, buffer, capacity, &copied, receipt, 32)
        if rc != 0:
            _source_failure(rc, 1, detail)
            return None
        raw = (<char *>buffer)[:copied]
        transition = _canonical(raw, limits)
        head = _codec.journal_transition_head_sha256(transition, limits)
        expected = _codec.journal_expected_nv_sha256(transition, limits)
        if i == 0:
            if bytes.fromhex(head) != (<char *>pin)[:32]:
                raise _codec.ContractError("PA01_INTENT_FIRST_PIN_MISMATCH")
            context = _context(transition)
        elif (_context(transition) != context or transition.sequence != previous.sequence + 1 or transition.previous_head_sha256 != previous_head or transition.previous_nv_value_sha256 != previous_nv):
            raise _codec.ContractError("PA01_INTENT_HISTORY_MISMATCH")
        if transition.transition_ref in seen:
            raise _codec.ContractError("PA01_INTENT_DUPLICATE_TRANSITION")
        seen.add(transition.transition_ref)
        previous = transition
        previous_head, previous_nv = head, expected
    if previous is None:
        raise _codec.ContractError("PA01_INTENT_EXISTING_HISTORY_REQUIRED")
    return (previous, previous_head, previous_nv, context, seen)

cdef object _history(_Intent *it, const uint8_t *pin, const uint8_t *payload, size_t length, uint8_t *buffer, size_t capacity, object limits, uint32_t *detail):
    cdef object scanned = _scan_history(it, pin, buffer, capacity, limits, detail)
    cdef object previous, previous_head, previous_nv, context, seen, proposed
    if scanned is None:
        return None
    previous, previous_head, previous_nv, context, seen = scanned
    if bytes.fromhex(previous_nv) != (<char *>it.observed.nv)[:32]:
        detail[0] = 4
        detail[1] = I_IN_DOUBT
        return None
    proposed = _canonical((<char *>payload)[:length], limits)
    if (_context(proposed) != context or proposed.sequence != previous.sequence + 1 or proposed.previous_head_sha256 != previous_head or proposed.previous_nv_value_sha256 != previous_nv or proposed.transition_ref in seen):
        raise _codec.ContractError("PA01_INTENT_NEXT_MISMATCH")
    return (bytes.fromhex(_codec.journal_transition_head_sha256(proposed, limits)), bytes.fromhex(_codec.journal_expected_nv_sha256(proposed, limits)))

cdef public uint32_t pa01_intent_prepare(void **intent_out,
        void **quarantine_out, void *journal, void *reader,
        const uint8_t *first_head, size_t first_head_size,
        const uint8_t *payload, size_t payload_len,
        uint32_t max_json, uint32_t max_ref,
        uint64_t max_epoch, uint64_t max_sequence,
        uint32_t max_correlation, uint32_t max_causation,
        uint32_t *detail_out) except? 0xffffffff with gil:
    cdef _Intent *it = NULL
    cdef _Observed current
    cdef uint8_t receipt[32]
    cdef uint8_t *buffer = NULL
    cdef size_t capacity = 0
    cdef uint32_t rc = I_STATE
    cdef int success = 0
    cdef object limits, result
    cdef bytes head, expected, candidate
    _detail_clear(detail_out)
    if (intent_out == NULL or quarantine_out == NULL or detail_out == NULL
            or intent_out[0] != NULL or quarantine_out[0] != NULL
            or intent_out == quarantine_out or journal == NULL or reader == NULL
            or first_head == NULL or first_head_size != 32 or payload == NULL
            or payload_len == 0 or max_json == 0 or payload_len > max_json
            or max_ref == 0 or max_correlation == 0 or max_causation == 0):
        return I_ARGUMENT
    it = <_Intent *>calloc(1, sizeof(_Intent))
    if it == NULL:
        return I_MEMORY
    it.pid = getpid()
    it.uid = geteuid()
    it.journal = journal
    it.reader = reader
    memcpy(it.first_head, first_head, 32)
    try:
        candidate = (<char *>payload)[:payload_len]
        limits = _codec.JournalLimits(
            _codec.PayloadLimits(max_json, max_ref, max_correlation),
            max_epoch, max_sequence, max_correlation, max_causation)
        rc = pa01_journal_lease_acquire(journal, <void *>it,
            it.observed.receipt, 32, &it.observed.size, &it.observed.count,
            &it.observed.journal_deadline, &it.observed.max_record)
        if rc != 0:
            return _source_failure(rc, 1, detail_out)
        it.journal_held = 1
        rc = pa01_nv_lease_acquire(reader, <void *>it, it.observed.nv, 32,
            it.observed.name, 34, &it.observed.index, &it.observed.nv_deadline)
        if rc != 0:
            return _source_failure(rc, 2, detail_out)
        it.nv_held = 1
        rc = pa01_nv_lease_read_serial(reader, <void *>it, &it.observed.read_serial)
        if rc != 0:
            return _source_failure(rc, 2, detail_out)
        if (it.observed.journal_deadline != it.observed.nv_deadline
                or it.observed.count == 0 or payload_len > it.observed.max_record):
            return I_VERIFY
        capacity = min(it.observed.max_record, max_json)
        buffer = <uint8_t *>malloc(capacity)
        if buffer == NULL:
            return I_MEMORY
        result = _history(it, it.first_head, <const uint8_t *><const char *>candidate, payload_len,
                           buffer, capacity, limits, detail_out)
        if result is None:
            return I_IN_DOUBT if detail_out[1] == 9 else I_STATE
        head, expected = result
        memcpy(it.head, <const char *>head, 32)
        memcpy(it.expected_nv, <const char *>expected, 32)
        # Dernier contrôle avant l'unique tentative d'ajout.
        rc = _observe(it, &current, detail_out)
        if rc != I_OK:
            return rc
        if not _same(&it.observed, &current):
            return I_IN_DOUBT
        it.append_attempted = 1
        rc = pa01_journal_append_leased(journal, <void *>it,
            it.observed.receipt, 32, it.observed.size,
            <const uint8_t *><const char *>candidate, payload_len, receipt, 32)
        if rc != 0:
            _source_failure(rc, 1, detail_out)
            return I_IN_DOUBT
        rc = _observe(it, &current, detail_out)
        if rc != I_OK:
            return I_IN_DOUBT
        if (not _same_nv(&it.observed, &current)
                or current.count != <uint64_t>it.observed.count + 1
                or current.size != it.observed.size + payload_len + 36
                or current.max_record != it.observed.max_record
                or memcmp(current.receipt, receipt, 32) != 0):
            return I_IN_DOUBT
        it.observed = current
        it.phase = I_PREPARED
        intent_out[0] = <void *>it
        success = 1
        return I_OK
    except (_codec.ContractError, UnicodeDecodeError, UnicodeEncodeError):
        detail_out[0] = 3
        detail_out[1] = I_VERIFY
        return I_VERIFY
    except MemoryError:
        return I_IN_DOUBT if it.append_attempted else I_MEMORY
    finally:
        if buffer != NULL:
            OPENSSL_cleanse(buffer, capacity)
            free(buffer)
        if not success:
            it.phase = I_BROKEN
            if _detach(it, detail_out) != I_OK:
                # Capacité de nettoyage seulement ; claim refuse cet état.
                quarantine_out[0] = <void *>it
            else:
                _dispose(it)

cdef uint32_t _intent_claim(void *state, void *consumer,
        uint8_t *head, size_t head_size, uint8_t *old_nv, size_t old_nv_size,
        uint8_t *expected_nv, size_t expected_nv_size,
        void **journal_out, void **reader_out, uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it = <_Intent *>state
    cdef _Observed current
    cdef uint32_t rc
    # Les sorties valides sont effacées même lors d'un second claim.
    if head != NULL and head_size == 32:
        OPENSSL_cleanse(head, 32)
    if old_nv != NULL and old_nv_size == 32:
        OPENSSL_cleanse(old_nv, 32)
    if expected_nv != NULL and expected_nv_size == 32:
        OPENSSL_cleanse(expected_nv, 32)
    if journal_out != NULL:
        journal_out[0] = NULL
    if reader_out != NULL:
        reader_out[0] = NULL
    _detail_clear(detail_out)
    if (it == NULL or consumer == NULL or head == NULL or head_size != 32 or old_nv == NULL
            or old_nv_size != 32 or expected_nv == NULL or expected_nv_size != 32
            or journal_out == NULL or reader_out == NULL or detail_out == NULL
            or journal_out == reader_out):
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if it.phase == I_CLAIMED or it.phase == I_CONFIRMED:
        return I_CONSUMED
    if it.phase != I_PREPARED:
        return I_STATE
    rc = _observe(it, &current, detail_out)
    if rc != I_OK:
        return rc
    if not _same(&it.observed, &current):
        it.phase = I_BROKEN
        return I_IN_DOUBT
    it.consumer = consumer
    it.phase = I_CLAIMED
    memcpy(head, it.head, 32)
    memcpy(old_nv, it.observed.nv, 32)
    memcpy(expected_nv, it.expected_nv, 32)
    journal_out[0] = it.journal
    reader_out[0] = it.reader
    return I_OK

cdef public uint32_t pa01_intent_close(void **state_inout,
        uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it
    cdef uint32_t rc
    cdef int attempted
    _detail_clear(detail_out)
    if state_inout == NULL or detail_out == NULL:
        return I_ARGUMENT
    if state_inout[0] == NULL:
        return I_OK
    it = <_Intent *>state_inout[0]
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if (it.phase == I_CLAIMED
            or it.consumer != NULL and it.consumer != <void *>it):
        # Le consommateur C reste vivant même après confirmation, jusqu’à son détachement.
        return I_IN_DOUBT
    attempted = it.append_attempted and it.phase != I_CONFIRMED
    rc = _detach(it, detail_out)
    if rc != I_OK:
        return I_IN_DOUBT
    _dispose(it)
    state_inout[0] = NULL
    return I_IN_DOUBT if attempted else I_OK


cdef uint32_t _intent_confirm(void *state, void *consumer, void *reader,
        uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it = <_Intent *>state
    cdef _Observed current
    cdef uint32_t rc
    _detail_clear(detail_out)
    if it == NULL or consumer == NULL or reader == NULL or detail_out == NULL:
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if it.phase != I_CLAIMED or it.reader != reader or it.consumer != consumer:
        return I_STATE
    rc = _observe(it, &current, detail_out)
    if rc != I_OK:
        return rc
    if (current.size != it.observed.size or current.count != it.observed.count
            or current.max_record != it.observed.max_record
            or current.journal_deadline != it.observed.journal_deadline
            or current.nv_deadline != it.observed.nv_deadline
            or current.index != it.observed.index
            or memcmp(current.name, it.observed.name, 34) != 0
            or memcmp(current.receipt, it.observed.receipt, 32) != 0
            or current.read_serial <= it.observed.read_serial
            or memcmp(current.nv, it.expected_nv, 32) != 0):
        return I_IN_DOUBT
    it.observed = current
    it.phase = I_CONFIRMED
    return I_OK


cdef public uint32_t pa01_intent_claim(void *state,
        uint8_t *head, size_t head_size, uint8_t *old_nv, size_t old_nv_size,
        uint8_t *expected_nv, size_t expected_nv_size,
        void **journal_out, void **reader_out, uint32_t *detail_out) noexcept nogil:
    return _intent_claim(state, state, head, head_size, old_nv, old_nv_size,
        expected_nv, expected_nv_size, journal_out, reader_out, detail_out)


cdef public uint32_t pa01_intent_claim_owned(void *state, void *consumer,
        uint8_t *head, size_t head_size, uint8_t *old_nv, size_t old_nv_size,
        uint8_t *expected_nv, size_t expected_nv_size,
        void **journal_out, void **reader_out, uint32_t *detail_out) noexcept nogil:
    return _intent_claim(state, consumer, head, head_size, old_nv, old_nv_size,
        expected_nv, expected_nv_size, journal_out, reader_out, detail_out)


cdef public uint32_t pa01_intent_confirm(void *state, void *reader,
        uint32_t *detail_out) noexcept nogil:
    return _intent_confirm(state, state, reader, detail_out)


cdef public uint32_t pa01_intent_confirm_owned(void *state, void *consumer,
        void *reader, uint32_t *detail_out) noexcept nogil:
    return _intent_confirm(state, consumer, reader, detail_out)


cdef public uint32_t pa01_intent_consumer_release(void *state,
        void *consumer, uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it = <_Intent *>state
    cdef uint32_t rc
    _detail_clear(detail_out)
    if it == NULL or consumer == NULL or detail_out == NULL:
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if (it.phase != I_CONFIRMED or it.consumer != consumer
            or not it.journal_held or not it.nv_held):
        return I_STATE
    rc = pa01_nv_lease_quiescent(it.reader, <void *>it)
    if rc != 0:
        return _source_failure(rc, 2, detail_out)
    it.consumer = NULL
    return I_OK


cdef public uint32_t pa01_intent_journal_current_owned(void *state,
        void *consumer, uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it = <_Intent *>state
    cdef _Observed current
    cdef uint32_t rc
    _detail_clear(detail_out)
    if it == NULL or consumer == NULL or detail_out == NULL:
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if (it.phase != I_CLAIMED or it.consumer != consumer
            or not it.journal_held or not it.nv_held):
        return I_STATE
    rc = pa01_journal_lease_snapshot(it.journal, <void *>it, current.receipt, 32,
        &current.size, &current.count, &current.journal_deadline, &current.max_record)
    if rc != 0:
        return _source_failure(rc, 1, detail_out)
    if (current.size != it.observed.size or current.count != it.observed.count
            or current.max_record != it.observed.max_record
            or current.journal_deadline != it.observed.journal_deadline
            or memcmp(current.receipt, it.observed.receipt, 32) != 0):
        return I_IN_DOUBT
    return I_OK


cdef public uint32_t pa01_intent_abandon_owned(void *state, void *consumer,
        void *reader, uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it = <_Intent *>state
    cdef uint32_t rc
    _detail_clear(detail_out)
    if it == NULL or consumer == NULL or reader == NULL or detail_out == NULL:
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if (it.phase != I_CLAIMED or it.consumer != consumer or it.reader != reader
            or not it.journal_held or not it.nv_held):
        return I_STATE
    rc = pa01_nv_extend_abort_fact(consumer, state, reader)
    if rc != 0:
        return _source_failure(rc, 2, detail_out)
    # Ce détachement ne répare ni n'ancre le journal, ne rend aucun droit.
    it.consumer = NULL
    it.phase = I_BROKEN
    return I_OK


# Observation de reprise seulement : aucun ancien contexte rendu quiescent,
# aucun append/Extend, droit d'effet, résultat SQL ou confirmation déduit.
cdef uint32_t _o_fail(_Intent *it, uint32_t outcome, uint32_t source,
        uint32_t stage, uint32_t *detail) noexcept nogil:
    if stage == 0:
        stage = 4
    if source == 0:
        source = outcome
    if it.observe_failure == 0:
        it.observe_failure = outcome
        it.observe_source = source
        it.observe_stage = stage
    it.phase = I_OBSERVE_FAILED
    detail[0] = it.observe_stage
    detail[1] = it.observe_source
    return it.observe_failure

cdef int _o_same_scope(_Observed *a, _Observed *b) noexcept nogil:
    # La valeur/serial NV doivent changer pendant notre lecture fraîche.
    return (a.size == b.size and a.count == b.count
        and a.max_record == b.max_record
        and a.journal_deadline == b.journal_deadline
        and a.nv_deadline == b.nv_deadline and a.index == b.index
        and memcmp(a.receipt, b.receipt, 32) == 0
        and memcmp(a.name, b.name, 34) == 0)

cdef public uint32_t pa01_observe_start(void **obs_out,
        void **quarantine_out, void *journal, void *reader,
        const uint8_t *first_head, size_t first_head_size,
        uint32_t max_json, uint32_t max_ref,
        uint64_t max_epoch, uint64_t max_sequence,
        uint32_t max_correlation, uint32_t max_causation,
        uint32_t *detail_out) except? 0xffffffff with gil:
    cdef _Intent *it = NULL
    cdef _Observed current
    cdef uint32_t rc
    cdef int retained = 0
    cdef object limits
    _detail_clear(detail_out)
    if (obs_out == NULL or quarantine_out == NULL or detail_out == NULL
            or obs_out == quarantine_out or obs_out[0] != NULL
            or quarantine_out[0] != NULL or journal == NULL or reader == NULL
            or first_head == NULL or first_head_size != 32
            or max_json == 0 or max_ref == 0
            or max_correlation == 0 or max_causation == 0):
        return I_ARGUMENT
    it = <_Intent *>calloc(1, sizeof(_Intent))
    if it == NULL:
        return I_MEMORY
    it.pid, it.uid = getpid(), geteuid()
    it.journal, it.reader = journal, reader
    it.phase = I_OBSERVING
    it.observe_class = O_DIVERGED
    it.obs_max_json, it.obs_max_ref = max_json, max_ref
    it.obs_max_epoch, it.obs_max_sequence = max_epoch, max_sequence
    it.obs_max_correlation, it.obs_max_causation = max_correlation, max_causation
    memcpy(it.first_head, first_head, 32)
    try:
        limits = _codec.JournalLimits(
            _codec.PayloadLimits(max_json, max_ref, max_correlation),
            max_epoch, max_sequence, max_correlation, max_causation)
        rc = pa01_journal_lease_acquire(journal, <void *>it,
            it.observed.receipt, 32, &it.observed.size, &it.observed.count,
            &it.observed.journal_deadline, &it.observed.max_record)
        if rc != 0:
            return _o_fail(it, I_IN_DOUBT if rc == 9 else I_STATE,
                           rc, 1, detail_out)
        it.journal_held = 1
        rc = pa01_nv_lease_acquire(reader, <void *>it,
            it.observed.nv, 32, it.observed.name, 34,
            &it.observed.index, &it.observed.nv_deadline)
        if rc != 0:
            return _o_fail(it, I_IN_DOUBT if rc == 9 else I_STATE,
                           rc, 2, detail_out)
        it.nv_held = 1
        rc = pa01_nv_lease_read_serial(reader, <void *>it,
                                      &it.observed.read_serial)
        if rc != 0:
            return _o_fail(it, I_IN_DOUBT if rc == 9 else I_STATE,
                           rc, 2, detail_out)
        if (it.observed.journal_deadline != it.observed.nv_deadline
                or it.observed.count == 0 or it.observed.max_record == 0):
            return _o_fail(it, I_VERIFY, I_VERIFY, 4, detail_out)
        rc = _observe(it, &current, detail_out)
        if rc != I_OK:
            return _o_fail(it, rc, detail_out[1], detail_out[0], detail_out)
        if not _same(&it.observed, &current):
            return _o_fail(it, I_IN_DOUBT, I_IN_DOUBT, 4, detail_out)
        it.baseline_serial = it.observed.read_serial
        # Aucun propriétaire n'est libéré après la tentative asynchrone.
        obs_out[0] = <void *>it
        retained = 1
        rc = pa01_nv_lease_refresh_start(reader, <void *>it)
        if rc == 5:
            return 5
        return _o_fail(it, I_IN_DOUBT if rc == 9 else I_STATE,
                       rc, 2, detail_out)
    except (_codec.ContractError, UnicodeDecodeError, UnicodeEncodeError):
        return _o_fail(it, I_VERIFY, I_VERIFY, 3, detail_out)
    except MemoryError:
        return _o_fail(it, I_MEMORY, I_MEMORY, 3, detail_out)
    finally:
        if not retained:
            it.phase = I_OBSERVE_FAILED
            if _detach(it, detail_out) != I_OK:
                quarantine_out[0] = <void *>it
            else:
                _dispose(it)

cdef public uint32_t pa01_observe_step(void *state,
        uint32_t *detail_out) except? 0xffffffff with gil:
    cdef _Intent *it = <_Intent *>state
    cdef _Observed fresh, after
    cdef uint32_t rc
    cdef uint8_t *buffer = NULL
    cdef size_t capacity = 0
    cdef object limits, scanned, last, head_hex, expected_hex, context, seen
    cdef bytes head, expected, previous
    cdef uint32_t classification
    _detail_clear(detail_out)
    if it == NULL or detail_out == NULL:
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if it.phase == I_OBSERVE_FAILED:
        # Le vrai propriétaire conserve le lecteur et ses APIs de drainage
        # et cleanup. Aucun refresh ou effet n’est réémis par cet observateur.
        detail_out[0] = it.observe_stage
        detail_out[1] = it.observe_source
        return it.observe_failure
    if (it.phase != I_OBSERVING or not it.journal_held or not it.nv_held):
        return I_STATE
    rc = pa01_nv_auth_step(it.reader)
    if rc == 5:
        return 5
    if rc != I_OK:
        return _o_fail(it, I_IN_DOUBT if rc == 9 else I_STATE,
                       rc, 2, detail_out)
    rc = _observe(it, &fresh, detail_out)
    if rc != I_OK:
        return _o_fail(it, rc, detail_out[1], detail_out[0], detail_out)
    if (not _o_same_scope(&it.observed, &fresh)
            or fresh.read_serial <= it.baseline_serial):
        return _o_fail(it, I_IN_DOUBT, I_IN_DOUBT, 4, detail_out)
    try:
        limits = _codec.JournalLimits(
            _codec.PayloadLimits(it.obs_max_json, it.obs_max_ref,
                                 it.obs_max_correlation),
            it.obs_max_epoch, it.obs_max_sequence,
            it.obs_max_correlation, it.obs_max_causation)
        capacity = min(it.observed.max_record, it.obs_max_json)
        buffer = <uint8_t *>malloc(capacity)
        if buffer == NULL:
            return _o_fail(it, I_MEMORY, I_MEMORY, 3, detail_out)
        scanned = _scan_history(it, it.first_head, buffer,
                                capacity, limits, detail_out)
        if scanned is None:
            return _o_fail(it, I_IN_DOUBT if detail_out[1] == 9 else I_STATE,
                           detail_out[1], detail_out[0], detail_out)
        last, head_hex, expected_hex, context, seen = scanned
        head, expected = bytes.fromhex(head_hex), bytes.fromhex(expected_hex)
        previous = bytes.fromhex(last.previous_nv_value_sha256)
        if len(head) != 32 or len(expected) != 32 or len(previous) != 32:
            return _o_fail(it, I_VERIFY, I_VERIFY, 3, detail_out)
        if memcmp(fresh.nv, <const char *>expected, 32) == 0:
            classification = O_HEAD_MATCH
        elif memcmp(fresh.nv, <const char *>previous, 32) == 0:
            classification = O_TAIL_UNANCHORED
        else:
            classification = O_DIVERGED
        rc = _observe(it, &after, detail_out)
        if rc != I_OK:
            return _o_fail(it, rc, detail_out[1], detail_out[0], detail_out)
        if not _same(&fresh, &after):
            return _o_fail(it, I_IN_DOUBT, I_IN_DOUBT, 4, detail_out)
        memcpy(it.head, <const char *>head, 32)
        memcpy(it.expected_nv, <const char *>expected, 32)
        it.observed = after
        it.observe_class = classification
        it.phase = I_OBSERVED
        return I_OK
    except (_codec.ContractError, UnicodeDecodeError, UnicodeEncodeError):
        return _o_fail(it, I_VERIFY, I_VERIFY, 3, detail_out)
    except MemoryError:
        return _o_fail(it, I_MEMORY, I_MEMORY, 3, detail_out)
    finally:
        if buffer != NULL:
            OPENSSL_cleanse(buffer, capacity)
            free(buffer)

cdef public uint32_t pa01_observe_snapshot(void *state,
        uint32_t *class_out, uint32_t *count_out,
        uint8_t *head_out, size_t head_size,
        uint8_t *expected_out, size_t expected_size,
        uint8_t *observed_out, size_t observed_size,
        uint64_t *serial_out, uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it = <_Intent *>state
    cdef _Observed current
    cdef uint32_t rc
    if class_out != NULL:
        class_out[0] = ~<uint32_t>0
    if count_out != NULL:
        count_out[0] = 0
    if serial_out != NULL:
        serial_out[0] = 0
    if head_out != NULL and head_size == 32:
        OPENSSL_cleanse(head_out, 32)
    if expected_out != NULL and expected_size == 32:
        OPENSSL_cleanse(expected_out, 32)
    if observed_out != NULL and observed_size == 32:
        OPENSSL_cleanse(observed_out, 32)
    _detail_clear(detail_out)
    if (it == NULL or class_out == NULL or count_out == NULL
            or head_out == NULL or head_size != 32
            or expected_out == NULL or expected_size != 32
            or observed_out == NULL or observed_size != 32
            or serial_out == NULL or detail_out == NULL):
        return I_ARGUMENT
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if it.phase == I_OBSERVE_FAILED:
        detail_out[0] = it.observe_stage
        detail_out[1] = it.observe_source
        return it.observe_failure
    if it.phase != I_OBSERVED or not it.journal_held or not it.nv_held:
        return I_STATE
    rc = _observe(it, &current, detail_out)
    if rc != I_OK:
        return _o_fail(it, rc, detail_out[1], detail_out[0], detail_out)
    if not _same(&it.observed, &current):
        return _o_fail(it, I_IN_DOUBT, I_IN_DOUBT, 4, detail_out)
    memcpy(head_out, it.head, 32)
    memcpy(expected_out, it.expected_nv, 32)
    memcpy(observed_out, it.observed.nv, 32)
    class_out[0] = it.observe_class
    count_out[0] = it.observed.count
    serial_out[0] = it.observed.read_serial
    return I_OK

cdef public uint32_t pa01_observe_close(void **state_inout,
        uint32_t *detail_out) noexcept nogil:
    cdef _Intent *it
    _detail_clear(detail_out)
    if state_inout == NULL or detail_out == NULL:
        return I_ARGUMENT
    if state_inout[0] == NULL:
        return I_OK
    it = <_Intent *>state_inout[0]
    if getpid() != it.pid or geteuid() != it.uid:
        return I_STATE
    if (it.phase != I_OBSERVING and it.phase != I_OBSERVED
            and it.phase != I_OBSERVE_FAILED):
        return I_STATE
    if it.phase == I_OBSERVE_FAILED:
        detail_out[0] = it.observe_stage
        detail_out[1] = it.observe_source
    if _detach(it, detail_out) != I_OK:
        return I_IN_DOUBT
    _dispose(it)
    state_inout[0] = NULL
    return I_OK
