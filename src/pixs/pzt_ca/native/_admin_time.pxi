# Prive Z12 : dates UTC structurelles, sans admission ni preuve de temps courant.
# A inclure UNE fois APRES _admin_values, _admin_codec, _admin_profile, _monotonic_deadline.
from libc.stddef cimport size_t
from libc.stdint cimport int32_t, int64_t, uint32_t, uint64_t
from libc.string cimport memcpy, memset

cdef struct Z12SignedUtc:
    int64_t unix_seconds
    uint32_t nanoseconds

cdef struct _AdminTime:
    _AdminValues values
    Z12SignedUtc observed_value
    int has_observed
    Z12SignedUtc from_value
    Z12SignedUtc until_value

cdef int _admin_days_in_month(int64_t year, int64_t month) noexcept nogil:
    if month == 1 or month == 3 or month == 5 or month == 7:
        return 31
    if month == 8 or month == 10 or month == 12:
        return 31
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return 29
    return 28

cdef int _admin_parse_utc(
    const unsigned char *ptr, size_t length,
    Z12SignedUtc *output
) noexcept nogil:
    # 1=valide, 0=format invalide, -2=precondition.
    cdef int64_t year
    cdef int64_t month
    cdef int64_t day
    cdef int64_t hour
    cdef int64_t minute
    cdef int64_t second
    cdef int64_t micro
    cdef int64_t days_before_year
    cdef int64_t days_before_base
    cdef int64_t days_month
    cdef int64_t month_index
    cdef int64_t days_total
    cdef int64_t seconds
    cdef size_t i
    if output != NULL:
        output.unix_seconds = 0
        output.nanoseconds = 0
    if ptr == NULL or output == NULL:
        return -2
    if length != 27:
        return 0
    for i in range(27):
        if ptr[i] > 127:
            return 0
    if ptr[4] != 45 or ptr[7] != 45 or ptr[10] != 84:
        return 0
    if ptr[13] != 58 or ptr[16] != 58 or ptr[19] != 46:
        return 0
    if ptr[26] != 90:
        return 0
    for i in range(27):
        if i == 4 or i == 7 or i == 10:
            continue
        if i == 13 or i == 16 or i == 19:
            continue
        if i == 26:
            continue
        if ptr[i] < 48 or ptr[i] > 57:
            return 0
    year = <int64_t>(ptr[0] - 48) * 1000 + <int64_t>(ptr[1] - 48) * 100 + <int64_t>(ptr[2] - 48) * 10 + <int64_t>(ptr[3] - 48)
    month = <int64_t>(ptr[5] - 48) * 10 + <int64_t>(ptr[6] - 48)
    day = <int64_t>(ptr[8] - 48) * 10 + <int64_t>(ptr[9] - 48)
    hour = <int64_t>(ptr[11] - 48) * 10 + <int64_t>(ptr[12] - 48)
    minute = <int64_t>(ptr[14] - 48) * 10 + <int64_t>(ptr[15] - 48)
    second = <int64_t>(ptr[17] - 48) * 10 + <int64_t>(ptr[18] - 48)
    micro = <int64_t>(ptr[20] - 48) * 100000 + <int64_t>(ptr[21] - 48) * 10000 + <int64_t>(ptr[22] - 48) * 1000 + <int64_t>(ptr[23] - 48) * 100 + <int64_t>(ptr[24] - 48) * 10 + <int64_t>(ptr[25] - 48)
    if year < 1 or year > 9999:
        return 0
    if month < 1 or month > 12:
        return 0
    if day < 1 or day > _admin_days_in_month(year, month):
        return 0
    if hour < 0 or hour > 23:
        return 0
    if minute < 0 or minute > 59:
        return 0
    if second < 0 or second > 59:
        return 0
    # bornes annee 1..9999 => unix_seconds [-62135596800, 253402300799], fraction <= 999999000, arithmetique signee int64 avant diff jours, pas ns int64.
    days_before_year = <int64_t>365 * (year - 1) + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    days_month = 0
    month_index = 1
    while month_index < month:
        days_month = days_month + _admin_days_in_month(year, month_index)
        month_index = month_index + 1
    days_before_base = <int64_t>365 * 1969 + 1969 // 4 - 1969 // 100 + 1969 // 400
    days_total = days_before_year + days_month + (day - 1) - days_before_base
    seconds = days_total * 86400 + hour * 3600 + minute * 60 + second
    output.unix_seconds = seconds
    output.nanoseconds = <uint32_t>(micro * 1000)
    return 1

cdef int _admin_utc_less(Z12SignedUtc left, Z12SignedUtc right) noexcept nogil:
    # valeurs calendaires validees non preuve temps courant.
    if left.unix_seconds < right.unix_seconds:
        return 1
    if left.unix_seconds > right.unix_seconds:
        return 0
    if left.nanoseconds < right.nanoseconds:
        return 1
    return 0

cdef int _admin_time_observe(
    int kind,
    const unsigned char *payload, size_t payload_len,
    Z12MonotonicDeadline *deadline, int32_t *timeout_ms,
    _AdminTime *output
) noexcept nogil:
    # 1=dates et types structurellement valides, 0=format ou fenetre invalide.
    # -3=expire, -1=horloge, -2=precondition. Aucune admission.
    cdef _AdminValues values
    cdef _AdminTime parsed
    cdef Z12SignedUtc observed_tmp
    cdef Z12SignedUtc from_tmp
    cdef Z12SignedUtc until_tmp
    cdef int live
    cdef int observed
    cdef int checked
    if output == NULL:
        return -2
    memset(output, 0, sizeof(_AdminTime))
    memset(&parsed, 0, sizeof(_AdminTime))
    memset(&values, 0, sizeof(_AdminValues))
    if timeout_ms != NULL:
        timeout_ms[0] = 0
    if payload == NULL or deadline == NULL or timeout_ms == NULL:
        return -2
    if kind != _ADMIN_KIND_PREPUBLICATION and kind != _ADMIN_KIND_PUBLICATION:
        return -2
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    observed = _admin_values_observe(kind, payload, payload_len, deadline, timeout_ms, &values)
    if observed != 1:
        return observed
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    if kind == _ADMIN_KIND_PREPUBLICATION:
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        checked = _admin_parse_utc(values.framed.fields[12].ptr, values.framed.fields[12].length, &from_tmp)
        if checked != 1:
            if checked == -2:
                return -2
            return 0
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        checked = _admin_parse_utc(values.framed.fields[13].ptr, values.framed.fields[13].length, &until_tmp)
        if checked != 1:
            if checked == -2:
                return -2
            return 0
        if _admin_utc_less(from_tmp, until_tmp) != 1:
            return 0
        parsed.from_value = from_tmp
        parsed.until_value = until_tmp
        parsed.has_observed = 0
    else:
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        checked = _admin_parse_utc(values.framed.fields[13].ptr, values.framed.fields[13].length, &observed_tmp)
        if checked != 1:
            if checked == -2:
                return -2
            return 0
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        checked = _admin_parse_utc(values.framed.fields[14].ptr, values.framed.fields[14].length, &from_tmp)
        if checked != 1:
            if checked == -2:
                return -2
            return 0
        live = _admin_live(deadline, timeout_ms)
        if live != 1:
            return live
        checked = _admin_parse_utc(values.framed.fields[15].ptr, values.framed.fields[15].length, &until_tmp)
        if checked != 1:
            if checked == -2:
                return -2
            return 0
        if _admin_utc_less(from_tmp, until_tmp) != 1:
            return 0
        parsed.observed_value = observed_tmp
        parsed.from_value = from_tmp
        parsed.until_value = until_tmp
        parsed.has_observed = 1
    live = _admin_live(deadline, timeout_ms)
    if live != 1:
        return live
    memcpy(&parsed.values, &values, sizeof(_AdminValues))
    memcpy(output, &parsed, sizeof(_AdminTime))
    return 1
