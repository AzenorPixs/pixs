# Prive Z12 : encodeur requete chrony pur, aucun syscall/envoi/poll/query/UTC.
# Inclure apres _chrony_protocol.pxi, une fois ; build -D_GNU_SOURCE.
# Sequence fournie par futur driver, aucune generation/RNG ici.
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint16_t, uint32_t

cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <string.h>
    #include <stddef.h>
    #define Z12_Q_WIRE 284
    typedef struct {
        uint8_t wire[Z12_Q_WIRE];
        size_t length;
        uint16_t command;
        uint16_t reply;
        uint32_t sequence;
    } Z12ChronyRequest;
    typedef struct {
        int invalid_input;
        int unsupported_command;
        int inconsistent_protocol;
    } Z12ChronyRequestDiag;
    static void z12_q_put_u16(uint8_t *p, uint16_t v) {
        p[0] = (uint8_t)(v >> 8); p[1] = (uint8_t)(v & 0xFFu);
    }
    static void z12_q_put_u32(uint8_t *p, uint32_t v) {
        p[0] = (uint8_t)(v >> 24); p[1] = (uint8_t)((v >> 16) & 0xFFu);
        p[2] = (uint8_t)((v >> 8) & 0xFFu); p[3] = (uint8_t)(v & 0xFFu);
    }
    static uint16_t z12_q_reply_for(uint16_t cmd) {
        if (cmd == 14) return 2; if (cmd == 15) return 3;
        if (cmd == 33) return 5; if (cmd == 57) return 26;
        if (cmd == 65) return 19; if (cmd == 67) return 20;
        if (cmd == 69) return 23; return 0;
    }
    static int z12_chrony_request_encode(uint16_t command, uint32_t source_index,
            const Z12CIP *address, uint32_t sequence,
            Z12ChronyRequest *out, Z12ChronyRequestDiag *diag) {
        uint8_t tmp[Z12_Q_WIRE];
        uint16_t reply = 0;
        size_t w = 0;
        uint16_t fam = 0;
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        if (out == NULL) { diag->invalid_input = 1; return -2; }
        memset(out, 0, sizeof(*out));
        memset(tmp, 0, sizeof(tmp));
        reply = z12_q_reply_for(command);
        if (reply == 0) { diag->unsupported_command = 1; return 0; }
        w = z12_chr_wire_length(command, reply);
        if (w == 0 || w > (size_t)Z12_Q_WIRE) { diag->inconsistent_protocol = 1; return 0; }
        if (w < 20) { diag->inconsistent_protocol = 1; return 0; }
        tmp[0] = 6; tmp[1] = 1; tmp[2] = 0; tmp[3] = 0;
        z12_q_put_u16(tmp + 4, command);
        z12_q_put_u16(tmp + 6, 0);
        z12_q_put_u32(tmp + 8, sequence);
        tmp[12] = 0; tmp[13] = 0; tmp[14] = 0; tmp[15] = 0;
        tmp[16] = 0; tmp[17] = 0; tmp[18] = 0; tmp[19] = 0;
        if (command == 14 || command == 33) {
            if (source_index != 0 || address != NULL) { diag->inconsistent_protocol = 1; return 0; }
        } else if (command == 15 || command == 69) {
            if (w < 24) { diag->inconsistent_protocol = 1; return 0; }
            if (address != NULL) { diag->inconsistent_protocol = 1; return 0; }
            z12_q_put_u32(tmp + 20, source_index);
        } else if (command == 57 || command == 65 || command == 67) {
            if (w < 40) { diag->inconsistent_protocol = 1; return 0; }
            if (source_index != 0) { diag->inconsistent_protocol = 1; return 0; }
            if (address == NULL) { diag->invalid_input = 1; return -2; }
            fam = address->fam;
            if (fam != 1 && fam != 2) { diag->inconsistent_protocol = 1; return 0; }
            if (fam == 1) {
                tmp[20] = address->b[0]; tmp[21] = address->b[1];
                tmp[22] = address->b[2]; tmp[23] = address->b[3];
            } else {
                size_t k;
                for (k = 0; k < 16; k++) tmp[20 + k] = address->b[k];
            }
            z12_q_put_u16(tmp + 36, fam);
            tmp[38] = 0; tmp[39] = 0;
        } else { diag->unsupported_command = 1; return 0; }
        memcpy(out->wire, tmp, w);
        out->length = w; out->command = command; out->reply = reply; out->sequence = sequence;
        explicit_bzero(tmp, sizeof(tmp));
        return 1;
    }
    """
    ctypedef struct Z12CIP:
        pass
    ctypedef struct Z12ChronyRequest:
        pass
    ctypedef struct Z12ChronyRequestDiag:
        int invalid_input
        int unsupported_command
        int inconsistent_protocol
    int z12_chrony_request_encode(uint16_t command, uint32_t source_index, const Z12CIP *address, uint32_t sequence, Z12ChronyRequest *out, Z12ChronyRequestDiag *diag)
