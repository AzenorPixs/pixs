# Privé Z12 : cadrage binaire du mandat, sans admission ni validation temporelle.
# Le propriétaire détient un buffer natif immuable pendant toute la vie des spans.
# output désigne une zone native valide, distincte du buffer payload.
# Il contrôle ensuite UTF-8, types, valeurs et égalités au challenge courant.
from libc.stddef cimport size_t
from libc.string cimport memcmp, memcpy, memset, strlen

cdef struct _OperatorSpan:
    const unsigned char *ptr
    size_t length

cdef struct _OperatorFields:
    # Ordre des 25 champs du §14.3 de contracts.md.
    _OperatorSpan fields[25]

cdef inline bint _operator_span_is(
    const _OperatorSpan *field, const char *expected
) noexcept nogil:
    cdef size_t expected_len = strlen(expected)
    return (field.length == expected_len
            and memcmp(field.ptr, expected, expected_len) == 0)

cdef int _operator_frame_payload(
    const unsigned char *payload, size_t payload_len,
    size_t max_payload_len, size_t max_field_len,
    _OperatorFields *output
) noexcept nogil:
    # 1=cadrage valide, 0=payload invalide/bornes, -2=précondition privée invalide.
    # Aucune allocation ou opération cryptographique ne se produit ici.
    cdef _OperatorFields parsed
    cdef size_t offset
    cdef size_t remaining
    cdef size_t field_len
    cdef size_t i
    cdef const char *prefix = "pixs.z12.initial.operator.payload/v1"
    cdef size_t prefix_len = strlen(prefix) + 1

    if output == NULL:
        return -2
    memset(output, 0, sizeof(_OperatorFields))
    if payload == NULL or max_payload_len == 0 or max_field_len == 0:
        return -2
    if payload_len > max_payload_len or payload_len < prefix_len:
        return 0
    if memcmp(payload, prefix, prefix_len) != 0:
        return 0
    memset(&parsed, 0, sizeof(_OperatorFields))
    offset = prefix_len
    for i in range(25):
        remaining = payload_len - offset
        if remaining < 4:
            return 0
        field_len = (
            ((<size_t>payload[offset]) << 24)
            | ((<size_t>payload[offset + 1]) << 16)
            | ((<size_t>payload[offset + 2]) << 8)
            | (<size_t>payload[offset + 3])
        )
        if field_len == 0 or field_len > max_field_len:
            return 0
        if field_len > remaining - 4:
            return 0
        parsed.fields[i].ptr = payload + offset + 4
        parsed.fields[i].length = field_len
        # Les bornes précédentes prouvent offset + 4 + field_len <= payload_len.
        offset = offset + 4 + field_len
    if offset != payload_len:
        return 0
    if not _operator_span_is(&parsed.fields[0], "z12.initial_operator_payload/v1"):
        return 0
    if not _operator_span_is(&parsed.fields[1], "1.0.0"):
        return 0
    if not _operator_span_is(&parsed.fields[2], "pixs.z12.initial.operator/v1"):
        return 0
    if parsed.fields[5].length != 32:
        return 0
    memcpy(output, &parsed, sizeof(_OperatorFields))
    return 1
