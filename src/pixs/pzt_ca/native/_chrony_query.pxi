# Prive Z12 : pilote requete chrony readonly, sans NTS/UTC.
# Inclure UNE fois apres deadline, launch_obs, systemd_connection, process_image, receive, socket, protocol, request ; build -D_GNU_SOURCE.
from libc.stddef cimport size_t
from libc.stdint cimport uint16_t, uint32_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <poll.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <sys/socket.h>
    #include <sys/stat.h>
    #include <sys/types.h>
    #include <time.h>
    #include <unistd.h>
    typedef struct {
        Z12CRep decoded;
        struct ucred cred;
        dev_t sender_dev;
        ino_t sender_ino;
        uint64_t send_before_ns;
        uint64_t send_after_ns;
        uint64_t recv_observed_ns;
        Z12ReceiveSocketFacts binding;
        uint32_t seq;
        uint16_t command;
        uint16_t reply;
        pid_t creator_pid;
        int loaded;
    } Z12ChronyQueryReply;
    typedef struct {
        Z12ChronySocketDiag sock;
        Z12ChronyReceiveDiag recv;
        Z12ChronyRequestDiag req;
        Z12CDiag dec;
        int invalid_contract;
        int busy;
        int send_would_block;
        int seq_mismatch;
        int peer_mismatch;
    } Z12ChronyQueryDiag;
    static int z12_q_to(Z12MonotonicDeadline *d, uint64_t end, struct timespec *ts, Z12ChronyQueryDiag *dg) {
        uint64_t last, rem;
        if (d == NULL || ts == NULL || dg == NULL) return -2;
        if (d->started != 1 || d->end_ns == 0 || d->end_ns != end) { dg->sock.native.foreign_binding = 1; return 0; }
        last = d->last_seen_ns;
        if (end <= last) { dg->sock.native.deadline_expired = 1; return 0; }
        rem = end - last;
        ts->tv_sec = (time_t)(rem / 1000000000ULL);
        ts->tv_nsec = (long)(rem % 1000000000ULL);
        if (ts->tv_sec < 0 || (uint64_t)ts->tv_sec != rem / 1000000000ULL) { dg->sock.native.native_output_invalid = 1; return -1; }
        return 1;
    }
    static int z12_q_poll4(Z12ChronySocket *s, Z12MonotonicDeadline *d, uint64_t end, Z12ChronyQueryDiag *dg) {
        struct pollfd f[4];
        struct timespec ts;
        int n = 0, pr, r;
        for (int k = 0; k < 4; k++) { f[k].fd = -1; f[k].events = 0; f[k].revents = 0; }
        r = z12_chrony_socket_guard(s, &dg->sock);
        if (r != 1) return r;
        if (d != s->owner.deadline) { dg->sock.native.foreign_binding = 1; return 0; }
        r = z12_q_to(d, end, &ts, dg);
        if (r != 1) return r;
        if (s->owner.facts == NULL) { dg->sock.native.foreign_binding = 1; return 0; }
        f[0].fd = s->socket_fd; f[0].events = POLLIN | POLLERR | POLLHUP | POLLNVAL; n = 1;
        f[1].fd = s->owner.facts->self_pidfd; f[1].events = POLLIN | POLLERR | POLLHUP | POLLNVAL; n = 2;
        f[2].fd = s->owner.facts->peer_pidfd; f[2].events = POLLIN | POLLERR | POLLHUP | POLLNVAL; n = 3;
        f[3].fd = -1; f[3].events = 0; n = 3;
        if (s->peer_fd >= 0) { f[3].fd = s->peer_fd; f[3].events = POLLIN | POLLERR | POLLHUP | POLLNVAL; n = 4; }
        pr = ppoll(f, (nfds_t)n, &ts, NULL);
        if (pr < 0) {
            int se = errno;
            z12_sysd_first(&dg->sock.native, Z12_SYSD_ERRNO, se);
            r = z12_chrony_socket_guard(s, &dg->sock);
            return -1;
        }
        r = z12_chrony_socket_guard(s, &dg->sock);
        if (r != 1) return r;
        if (pr == 0) return 2;
        for (int k = 1; k < n; k++) {
            if (f[k].fd >= 0 && (f[k].revents & (POLLIN | POLLERR | POLLHUP | POLLNVAL))) { dg->sock.native.process_unavailable = 1; return 0; }
        }
        if (f[0].revents & (POLLERR | POLLHUP | POLLNVAL)) { dg->sock.native.native_output_invalid = 1; return 0; }
        if (f[0].revents & POLLIN) return 1;
        return 2;
    }
    static int z12_chrony_query_reply_destroy(Z12ChronyQueryReply **owned) {
        Z12ChronyQueryReply *b;
        int e = errno;
        if (owned == NULL) return -2;
        b = *owned;
        if (b == NULL) return 1;
        b->loaded = 0;
        explicit_bzero(b, sizeof(*b));
        free((void *)b);
        *owned = NULL;
        errno = e;
        return 1;
    }
    static int z12_chrony_query_once(Z12ChronySocket *s, uint16_t command, uint32_t source_index, const Z12CIP *address, Z12MonotonicDeadline *deadline, Z12ChronyQueryReply **out, Z12ChronyQueryDiag *diag) {
        int r;
        uint32_t seq = 0;
        uint64_t end = 0;
        Z12ChronyRequest req;
        Z12ChronyDatagram *dg = NULL;
        Z12ChronyQueryReply *rp = NULL;
        uint64_t t0 = 0, t1 = 0, t2 = 0;
        ssize_t sn;
        struct stat pst;
        if (diag != NULL) memset(diag, 0, sizeof(*diag));
        if (s == NULL || deadline == NULL || out == NULL || diag == NULL) { if (diag != NULL) diag->invalid_contract = 1; return -2; }
        if (*out != NULL) { diag->invalid_contract = 1; return -2; }
        end = s->owner.end;
        r = z12_chrony_socket_guard(s, &diag->sock);
        if (r != 1) return r;
        if (deadline != s->owner.deadline) { diag->sock.native.foreign_binding = 1; return 0; }
        if (s->active != 0) { diag->busy = 1; return 0; }
        if (s->counter64 >= (UINT64_C(1) << 32)) { s->unusable = 1; return 0; }
        seq = (uint32_t)(s->seed32 + (uint32_t)s->counter64);
        s->counter64++;
        memset(&req, 0, sizeof(req));
        r = z12_chrony_request_encode(command, source_index, address, seq, &req, &diag->req);
        if (r != 1) return (r == -2) ? -2 : 0;
        s->active = 1;
        r = z12_chrony_socket_guard(s, &diag->sock);
        if (r != 1) goto fail;
        t0 = deadline->last_seen_ns;
        sn = send(s->socket_fd, req.wire, req.length, MSG_NOSIGNAL | MSG_DONTWAIT);
        if (sn < 0) {
            int se = errno;
            if (se == EAGAIN || se == EWOULDBLOCK) {
                diag->send_would_block = 1;
                r = z12_chrony_socket_guard(s, &diag->sock);
                r = (r == 1) ? 0 : r;
                goto fail;
            }
            z12_sysd_first(&diag->sock.native, Z12_SYSD_ERRNO, se);
            r = z12_chrony_socket_guard(s, &diag->sock);
            r = -1;
            goto fail;
        }
        if ((size_t)sn != req.length) {
            diag->sock.native.native_output_invalid = 1;
            r = z12_chrony_socket_guard(s, &diag->sock);
            r = (r == 1) ? 0 : r;
            goto fail;
        }
        r = z12_chrony_socket_guard(s, &diag->sock);
        if (r != 1) goto fail;
        t1 = deadline->last_seen_ns;
        if (t1 < t0) { r = 0; goto fail; }
        for (;;) {
            int pr = z12_q_poll4(s, deadline, end, diag);
            if (pr == 1) break;
            if (pr == 2) continue;
            r = (pr == -2) ? -2 : 0;
            if (pr < 0) r = -1;
            goto fail;
        }
        for (;;) {
            Z12ChronyReceiveDiag rd;
            memset(&rd, 0, sizeof(rd));
            r = z12_chrony_receive(&s->owner, s->socket_fd, &dg, &rd);
            diag->recv = rd;
            if (r == 1) break;
            if (r == 2) {
                int pr = z12_q_poll4(s, deadline, end, diag);
                if (pr == 1) continue;
                if (pr == 2) continue;
                r = (pr == -2) ? -2 : 0;
                if (pr < 0) r = -1;
                goto fail;
            }
            goto fail;
        }
        r = z12_chrony_socket_guard(s, &diag->sock);
        if (r != 1) goto fail;
        t2 = deadline->last_seen_ns;
        if (t2 < t1) { r = 0; goto fail; }
        {
            Z12CDiag dd;
            Z12CRep rep;
            memset(&dd, 0, sizeof(dd));
            memset(&rep, 0, sizeof(rep));
            r = z12_chrony_decode(dg->payload, dg->length, req.command, req.reply, req.sequence, s->max_name, &rep, &dd);
            diag->dec = dd;
            if (r != 1) goto fail;
            if (rep.cmd != req.command || rep.reply != req.reply || rep.seq != req.sequence) { diag->seq_mismatch = 1; r = 0; goto fail; }
            r = z12_chrony_socket_guard(s, &diag->sock);
            if (r != 1) goto fail;
            rp = (Z12ChronyQueryReply *)calloc(1, sizeof(*rp));
            if (rp == NULL) {
                z12_sysd_first(&diag->sock.native, Z12_SYSD_ERRNO, errno);
                r = z12_chrony_socket_guard(s, &diag->sock);
                r = -1;
                goto fail;
            }
            r = z12_chrony_socket_guard(s, &diag->sock);
            if (r != 1) goto fail;
            rp->decoded = rep;
            rp->cred = dg->credentials;
            rp->sender_dev = dg->peer_dev;
            rp->sender_ino = dg->peer_ino;
            rp->send_before_ns = t0;
            rp->send_after_ns = t1;
            rp->recv_observed_ns = t2;
            rp->binding = s->sock_snapshot;
            rp->seq = seq; rp->command = req.command; rp->reply = req.reply;
            rp->creator_pid = getpid();
            if (s->peer_fd < 0) {
                s->peer_fd = dg->peer_fd;
                dg->peer_fd = -1;
                if (s->peer_fd < 0) { r = 0; goto fail; }
                r = z12_chrony_socket_guard(s, &diag->sock);
                if (r != 1) goto fail;
                if (fstat(s->peer_fd, &pst) != 0) {
                    z12_sysd_first(&diag->sock.native, Z12_SYSD_ERRNO, errno);
                    r = z12_chrony_socket_guard(s, &diag->sock);
                    r = -1;
                    goto fail;
                }
                r = z12_chrony_socket_guard(s, &diag->sock);
                if (r != 1) goto fail;
                if (pst.st_dev != rp->sender_dev || pst.st_ino != rp->sender_ino) { diag->peer_mismatch = 1; r = 0; goto fail; }
            } else {
                r = z12_chrony_socket_guard(s, &diag->sock);
                if (r != 1) goto fail;
                if (fstat(s->peer_fd, &pst) != 0) {
                    z12_sysd_first(&diag->sock.native, Z12_SYSD_ERRNO, errno);
                    r = z12_chrony_socket_guard(s, &diag->sock);
                    r = -1;
                    goto fail;
                }
                r = z12_chrony_socket_guard(s, &diag->sock);
                if (r != 1) goto fail;
                if (pst.st_dev != rp->sender_dev || pst.st_ino != rp->sender_ino) { diag->peer_mismatch = 1; r = 0; goto fail; }
            }
        }
        {
            Z12ChronyReceiveDiag td;
            memset(&td, 0, sizeof(td));
            int cr = z12_chrony_datagram_destroy(&dg, &td);
            diag->sock.native.must_destroy_bus |= td.base.native.must_destroy_bus;
            if (cr != 0) {
                if (diag->sock.native.cleanup_errno == 0) diag->sock.native.cleanup_errno = td.base.native.cleanup_errno;
                r = -1; goto fail;
            }
        }
        r = z12_chrony_socket_guard(s, &diag->sock);
        if (r != 1) goto fail;
        rp->loaded = 1;
        *out = rp; rp = NULL;
        s->active = 0;
        return 1;
    fail:
        if (dg != NULL) {
            Z12ChronyReceiveDiag td;
            memset(&td, 0, sizeof(td));
            int cr = z12_chrony_datagram_destroy(&dg, &td);
            diag->sock.native.must_destroy_bus |= td.base.native.must_destroy_bus;
            if (cr != 0) {
                if (diag->sock.native.cleanup_errno == 0) diag->sock.native.cleanup_errno = td.base.native.cleanup_errno;
                r = -1;
            }
        }
        if (rp != NULL) { explicit_bzero(rp, sizeof(*rp)); free(rp); rp = NULL; }
        s->unusable = 1;
        s->active = 0;
        if (r == 1) r = 0;
        return (r == -2) ? -2 : (r == -1 ? -1 : 0);
    }
    """
    ctypedef struct Z12ChronyQueryReply:
        pass
    ctypedef struct Z12ChronyQueryDiag:
        Z12ChronySocketDiag sock
        Z12ChronyReceiveDiag recv
        Z12ChronyRequestDiag req
        Z12CDiag dec
        int invalid_contract
        int busy
        int send_would_block
        int seq_mismatch
        int peer_mismatch
    int z12_chrony_query_once(Z12ChronySocket *s, uint16_t command, uint32_t source_index, const Z12CIP *address, Z12MonotonicDeadline *deadline, Z12ChronyQueryReply **out, Z12ChronyQueryDiag *diag)
    int z12_chrony_query_reply_destroy(Z12ChronyQueryReply **owned)
