# Prive Z12 : cadrage binaire prepublication, publication et binding, sans admission.
# A inclure UNE fois APRES _admin_profile.pxi et _monotonic_deadline.pxi, sans les reinclure.
# Preconditions : le proprietaire detient un tampon natif immuable, output distinct
# du tampon payload sans recouvrement, duree de vie couvrant tous les spans.
# Aucune validation semantique UTF8, hash, date, epoque ou signature ici.
from libc.stddef cimport size_t
from libc.stdint cimport int32_t
from libc.string cimport memcmp, memcpy, memset, strlen

cdef enum _AdminKind:
    _ADMIN_KIND_PREPUBLICATION = 1
    _ADMIN_KIND_PUBLICATION = 2
    _ADMIN_KIND_BINDING = 3

cdef struct _AdminSpan:
    const unsigned char *ptr
    size_t length

cdef struct _AdminFramed:
    int kind
    size_t count
    _AdminSpan fields[18]

cdef inline bint _admin_span_is(
    const _AdminSpan *field, const char *expected
) noexcept nogil:
    cdef size_t expected_len
    if field == NULL or expected == NULL or field.ptr == NULL:
        return 0
    expected_len = strlen(expected)
    if field.length != expected_len:
        return 0
    return memcmp(field.ptr, expected, expected_len) == 0

cdef int _admin_live(
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms
) noexcept nogil:
    # 1=vivant, -3=expire, -1=erreur horloge, -2=precondition.
    cdef int live
    if deadline == NULL or timeout_ms == NULL:
        return -2
    live = _admin_profile_check_live(deadline, timeout_ms)
    if live == 1:
        return 1
    if live == 0:
        return -3
    if live == -1:
        return -1
    return -2

cdef int _admin_frame_payload(
    int kind,
    const unsigned char *payload, size_t payload_len,
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms,
    _AdminFramed *output
) noexcept nogil:
    # 1=cadre, 0=format public, -3=expire, -1=horloge, -2=precondition.
    cdef _AdminFramed parsed
    cdef Z12AdminView view
    cdef const char *prefix
    cdef const char *object_type
    cdef size_t expected_count
    cdef size_t prefix_len
    cdef size_t offset
    cdef size_t remaining
    cdef size_t field_len
    cdef size_t i
    cdef int live
    cdef int observed
    if output == NULL:
        return -2
    memset(output, 0, sizeof(_AdminFramed))
    memset(&parsed, 0, sizeof(_AdminFramed))
    memset(&view, 0, sizeof(Z12AdminView))
    if timeout_ms != NULL:
        timeout_ms[0] = 0
    if payload == NULL or deadline == NULL or timeout_ms == NULL:
        return -2
    if kind != _ADMIN_KIND_PREPUBLICATION and kind != _ADMIN_KIND_PUBLICATION and kind != _ADMIN_KIND_BINDING:
        return -2
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    observed = _admin_profile_observe(&view)
    if observed != 1:
        return -2
    if view.max_payload_len == 0 or view.max_field_len == 0:
        return -2
    if kind == _ADMIN_KIND_PREPUBLICATION:
        prefix = "pixs.z12.admin.prepublication/v1"
        expected_count = 15
        object_type = "z12.admin_prepublication/v1"
    elif kind == _ADMIN_KIND_PUBLICATION:
        prefix = "pixs.z12.admin.publication/v1"
        expected_count = 17
        object_type = "z12.admin_publication/v1"
    else:
        prefix = "pixs.z12.admin.binding/v1"
        expected_count = 18
        object_type = "z12.nv_binding/v1"
    prefix_len = strlen(prefix) + 1
    if payload_len > view.max_payload_len or payload_len < prefix_len:
        return 0
    if memcmp(payload, prefix, prefix_len) != 0:
        return 0
    offset = prefix_len
    for i in range(expected_count):
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        remaining = payload_len - offset
        if remaining < 4:
            return 0
        field_len = (
            ((<size_t>payload[offset]) << 24)
            | ((<size_t>payload[offset + 1]) << 16)
            | ((<size_t>payload[offset + 2]) << 8)
            | (<size_t>payload[offset + 3])
        )
        if field_len == 0 or field_len > view.max_field_len:
            return 0
        if field_len > remaining - 4:
            return 0
        parsed.fields[i].ptr = payload + offset + 4
        parsed.fields[i].length = field_len
        offset = offset + 4 + field_len
    if offset != payload_len:
        return 0
    if not _admin_span_is(&parsed.fields[0], object_type):
        return 0
    if not _admin_span_is(&parsed.fields[1], "1.0.0"):
        return 0
    if kind == _ADMIN_KIND_PREPUBLICATION or kind == _ADMIN_KIND_PUBLICATION:
        if not _admin_span_is(&parsed.fields[5], "policy_admission"):
            return 0
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    parsed.kind = kind
    parsed.count = expected_count
    memcpy(output, &parsed, sizeof(_AdminFramed))
    return 1
