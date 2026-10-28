# Prive Z12 : valeurs non temporelles, sans admission.
# A inclure UNE fois APRES _admin_codec, _admin_profile et _monotonic_deadline.
# Tampon natif immuable, output distinct sans recouvrement, duree explicite.
# Dates explicitement SKIP, jamais reputees validees.
from libc.stddef cimport size_t
from libc.stdint cimport int32_t, uint64_t, uint32_t, UINT64_MAX, UINT32_MAX
from libc.string cimport memcpy, memset

cdef struct _AdminValues:
    _AdminFramed framed
    uint64_t epoch_value
    uint32_t nv_index_value

cdef enum _AdminFieldType:
    _ADMIN_SKIP = 0
    _ADMIN_REF = 1
    _ADMIN_HASH = 2
    _ADMIN_U64 = 3
    _ADMIN_U32 = 4

cdef int _admin_field_type(int kind, size_t index) noexcept nogil:
    if kind == _ADMIN_KIND_PREPUBLICATION:
        if index == 2 or index == 3 or index == 4:
            return _ADMIN_REF
        if index == 6 or index == 7:
            return _ADMIN_REF
        if index == 9 or index == 10:
            return _ADMIN_REF
        if index == 8 or index == 11:
            return _ADMIN_HASH
        if index == 14:
            return _ADMIN_U64
        return _ADMIN_SKIP
    elif kind == _ADMIN_KIND_PUBLICATION:
        if index == 2 or index == 3 or index == 4:
            return _ADMIN_REF
        if index == 6 or index == 7:
            return _ADMIN_REF
        if index == 9 or index == 10:
            return _ADMIN_REF
        if index == 8 or index == 11 or index == 12:
            return _ADMIN_HASH
        if index == 16:
            return _ADMIN_U64
        return _ADMIN_SKIP
    elif kind == _ADMIN_KIND_BINDING:
        if index == 2 or index == 3 or index == 4:
            return _ADMIN_REF
        if index == 5 or index == 6:
            return _ADMIN_REF
        if index == 8 or index == 9:
            return _ADMIN_REF
        if index == 14 or index == 17:
            return _ADMIN_REF
        if index == 7 or index == 10:
            return _ADMIN_HASH
        if index == 12 or index == 13:
            return _ADMIN_HASH
        if index == 15 or index == 16:
            return _ADMIN_HASH
        if index == 11:
            return _ADMIN_U32
        return _ADMIN_SKIP
    return -2

cdef int _admin_check_utf8_strict(
    const unsigned char *ptr, size_t length,
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms
) noexcept nogil:
    cdef size_t i = 0
    cdef unsigned char byte
    cdef unsigned char lower
    cdef unsigned char upper
    cdef size_t trailing
    cdef unsigned int codepoint
    cdef int live
    if ptr == NULL:
        return -2
    if length == 0:
        return 0
    while i < length:
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        byte = ptr[i]
        if byte <= 0x7F:
            i += 1
            continue
        elif byte >= 0xC2 and byte <= 0xDF:
            trailing = 1
            lower = 0x80
            upper = 0xBF
            codepoint = byte & 0x1F
        elif byte >= 0xE0 and byte <= 0xEF:
            trailing = 2
            if byte == 0xE0:
                lower = 0xA0
            else:
                lower = 0x80
            if byte == 0xED:
                upper = 0x9F
            else:
                upper = 0xBF
            codepoint = byte & 0x0F
        elif byte >= 0xF0 and byte <= 0xF4:
            trailing = 3
            if byte == 0xF0:
                lower = 0x90
            else:
                lower = 0x80
            if byte == 0xF4:
                upper = 0x8F
            else:
                upper = 0xBF
            codepoint = byte & 0x07
        else:
            return 0
        if trailing > length - i - 1:
            return 0
        if ptr[i + 1] < lower or ptr[i + 1] > upper:
            return 0
        if trailing >= 2:
            if ptr[i + 2] < 0x80 or ptr[i + 2] > 0xBF:
                return 0
        if trailing >= 3:
            if ptr[i + 3] < 0x80 or ptr[i + 3] > 0xBF:
                return 0
        if trailing == 1:
            codepoint = (codepoint << 6) | (ptr[i + 1] & 0x3F)
        elif trailing == 2:
            codepoint = (codepoint << 12) | ((ptr[i + 1] & 0x3F) << 6) | (ptr[i + 2] & 0x3F)
        else:
            codepoint = (codepoint << 18) | ((ptr[i + 1] & 0x3F) << 12) | ((ptr[i + 2] & 0x3F) << 6) | (ptr[i + 3] & 0x3F)
        if codepoint > 0x10FFFF:
            return 0
        i += 1 + trailing
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    return 1

cdef int _admin_check_hex64(const unsigned char *ptr, size_t length) noexcept nogil:
    cdef size_t i
    cdef unsigned char byte
    if ptr == NULL:
        return -2
    if length != 64:
        return 0
    for i in range(64):
        byte = ptr[i]
        if not ((byte >= 48 and byte <= 57) or (byte >= 97 and byte <= 102)):
            return 0
    return 1

cdef int _admin_check_u64_canonical(
    const unsigned char *ptr, size_t length, uint64_t *out
) noexcept nogil:
    cdef size_t i
    cdef uint64_t value = 0
    cdef uint64_t digit
    if out != NULL:
        out[0] = 0
    if ptr == NULL or out == NULL:
        return -2
    if length == 0 or length > 20:
        return 0
    if length > 1 and ptr[0] == 48:
        return 0
    for i in range(length):
        if ptr[i] < 48 or ptr[i] > 57:
            return 0
        digit = <uint64_t>(ptr[i] - 48)
        if value > (UINT64_MAX - digit) // 10:
            return 0
        value = value * 10 + digit
    out[0] = value
    return 1

cdef int _admin_check_u32_canonical(
    const unsigned char *ptr, size_t length, uint32_t *out
) noexcept nogil:
    cdef size_t i
    cdef uint32_t value = 0
    cdef uint32_t digit
    if out != NULL:
        out[0] = 0
    if ptr == NULL or out == NULL:
        return -2
    if length == 0 or length > 10:
        return 0
    if length > 1 and ptr[0] == 48:
        return 0
    for i in range(length):
        if ptr[i] < 48 or ptr[i] > 57:
            return 0
        digit = <uint32_t>(ptr[i] - 48)
        if value > (UINT32_MAX - digit) // 10:
            return 0
        value = value * 10 + digit
    out[0] = value
    return 1

cdef int _admin_values_observe(
    int kind,
    const unsigned char *payload, size_t payload_len,
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms,
    _AdminValues *output
) noexcept nogil:
    # 1=champs non temporels valides, 0=champ public invalide.
    # -3=expire, -1=horloge, -2=precondition. Aucune admission.
    cdef _AdminFramed framed
    cdef _AdminValues parsed
    cdef size_t i
    cdef int field_type
    cdef int live
    cdef int framed_code
    cdef int checked
    cdef uint64_t epoch_tmp
    cdef uint32_t nv_tmp
    if output == NULL:
        return -2
    memset(output, 0, sizeof(_AdminValues))
    memset(&parsed, 0, sizeof(_AdminValues))
    memset(&framed, 0, sizeof(_AdminFramed))
    if timeout_ms != NULL:
        timeout_ms[0] = 0
    if payload == NULL or deadline == NULL or timeout_ms == NULL:
        return -2
    if kind != _ADMIN_KIND_PREPUBLICATION and kind != _ADMIN_KIND_PUBLICATION and kind != _ADMIN_KIND_BINDING:
        return -2
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    framed_code = _admin_frame_payload(kind, payload, payload_len, deadline, timeout_ms, &framed)
    if framed_code != 1:
        return framed_code
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    for i in range(framed.count):
        field_type = _admin_field_type(kind, i)
        if field_type == -2:
            return -2
        if field_type == _ADMIN_SKIP:
            continue
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        if field_type == _ADMIN_REF:
            checked = _admin_check_utf8_strict(framed.fields[i].ptr, framed.fields[i].length, deadline, timeout_ms)
            if checked != 1:
                return checked
        elif field_type == _ADMIN_HASH:
            checked = _admin_check_hex64(framed.fields[i].ptr, framed.fields[i].length)
            if checked != 1:
                if checked == -2:
                    return -2
                return 0
        elif field_type == _ADMIN_U64:
            epoch_tmp = 0
            checked = _admin_check_u64_canonical(framed.fields[i].ptr, framed.fields[i].length, &epoch_tmp)
            if checked != 1:
                if checked == -2:
                    return -2
                return 0
            parsed.epoch_value = epoch_tmp
        else:
            nv_tmp = 0
            checked = _admin_check_u32_canonical(framed.fields[i].ptr, framed.fields[i].length, &nv_tmp)
            if checked != 1:
                if checked == -2:
                    return -2
                return 0
            parsed.nv_index_value = nv_tmp
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    memcpy(&parsed.framed, &framed, sizeof(_AdminFramed))
    memcpy(output, &parsed, sizeof(_AdminValues))
    return 1
