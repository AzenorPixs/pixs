# Prive Z12 : fabrique socket chrony locale, sans requete/envoi/query/poll/UTC.
# Inclure apres deadline, launch_obs, systemd_connection, process_image et _chrony_receive.pxi, une fois ; build -D_GNU_SOURCE.
# Endpoint filesystem politique native, bind AUTOBIND abstrait local, connect seul endpoint.
# Aucune source NTS/UTC, aucun default path/IP/port, aucun fichier/unlink, aucune admission.
from libc.stddef cimport size_t
from libc.stdint cimport uint32_t, uint64_t
from posix.types cimport pid_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stddef.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/un.h>
    #include <sys/stat.h>
    #include <sys/random.h>
    #include <sys/pidfd.h>
    #if !defined(SCM_PIDFD) || !defined(SO_PASSPIDFD) || !defined(SO_PASSCRED)
    #error "Z12 requires the selected glibc 2.41 / Linux 6.12 socket-pidfd ABI"
    #endif
    typedef Z12ProcessImageDiag Z12ChronySocketDiag;
    typedef struct {
        Z12ImageCtx owner;
        Z12SysdConn *manager;
        int socket_fd;
        int peer_fd;
        pid_t creator_pid;
        pid_t creator_tid;
        uint32_t seed32;
        uint64_t counter64;
        int seed_ready;
        int active;
        int unusable;
        size_t max_name;
        Z12ReceiveSocketFacts sock_snapshot;
        int has_sock_snapshot;
    } Z12ChronySocket;

    static int z12_s_guard(Z12ChronySocket *s, Z12ChronySocketDiag *d) {
        if (s == NULL || d == NULL) return -2;
        if (getpid() != s->creator_pid || gettid() != s->creator_tid) {
            d->native.foreign_binding = 1; return 0;
        }
        return z12_image_guard(&s->owner, d);
    }
    static int z12_s_verdict(Z12ChronySocketDiag *d, int r) {
        return z12_image_verdict(d, r);
    }
    static int z12_s_post(Z12ChronySocket *s, Z12ChronySocketDiag *d, int code) {
        if (code < 0) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        return z12_s_guard(s, d);
    }
    static int z12_s_flags(Z12ChronySocket *s, int fd, int cmd, int *v, Z12ChronySocketDiag *d) {
        int code, r = z12_s_guard(s, d);
        if (r != 1) return r;
        code = fcntl(fd, cmd);
        r = z12_s_post(s, d, code);
        if (r == 1) *v = code;
        return r;
    }
    static int z12_s_set_verify(Z12ChronySocket *s, int fd, int opt, Z12ChronySocketDiag *d) {
        int one = 1, got = 0, code, r;
        socklen_t len;
        r = z12_s_guard(s, d); if (r != 1) return r;
        code = setsockopt(fd, SOL_SOCKET, opt, &one, sizeof(one));
        r = z12_s_post(s, d, code); if (r != 1) return r;
        if (code != 0) { d->native.native_output_invalid = 1; return 0; }
        len = sizeof(got);
        r = z12_s_guard(s, d); if (r != 1) return r;
        code = getsockopt(fd, SOL_SOCKET, opt, &got, &len);
        r = z12_s_post(s, d, code); if (r != 1) return r;
        if (code != 0) { d->native.native_output_invalid = 1; return 0; }
        if (len != sizeof(got) || got != 1) { d->native.foreign_binding = 1; return 0; }
        return 1;
    }
    static int z12_s_facts(Z12ChronySocket *s, int fd,
                            Z12ReceiveSocketFacts *out, Z12ChronySocketDiag *d) {
        Z12ChronyReceiveDiag receive_diag = {0};
        int r;
        receive_diag.base = *d;
        r = z12_r_socket(&s->owner, fd, out, &receive_diag);
        *d = receive_diag.base;
        return r;
    }
    static int z12_chrony_socket_guard(Z12ChronySocket *s, Z12ChronySocketDiag *d) {
        int r;
        Z12ReceiveSocketFacts cur;
        if (s == NULL || d == NULL) return -2;
        if (getpid() != s->creator_pid || gettid() != s->creator_tid) {
            d->native.foreign_binding = 1; return 0;
        }
        if (s->manager == NULL || s->manager != s->owner.conn) { d->native.foreign_binding = 1; return 0; }
        r = z12_image_guard(&s->owner, d);
        if (r != 1) return r;
        if ((s->active != 0 && s->active != 1) || s->unusable != 0) { d->native.foreign_binding = 1; return 0; }
        if (s->seed_ready != 1) { d->native.foreign_binding = 1; return 0; }
        if (s->socket_fd < 0) { d->native.foreign_binding = 1; return 0; }
        if (s->peer_fd >= 0) {
            r = z12_sysd_pidfd_live(s->peer_fd, &d->native);
            if (r != 1) return z12_s_verdict(d, r);
            r = z12_s_guard(s, d);
            if (r != 1) return r;
        }
        if (s->has_sock_snapshot != 1) { d->native.foreign_binding = 1; return 0; }
        {
            r = z12_s_facts(s, s->socket_fd, &cur, d);
            if (r != 1) return r;
            if (!z12_r_same_socket(&s->sock_snapshot, &cur)) {
                d->native.foreign_binding = 1; return 0;
            }
        }
        return z12_s_guard(s, d);
    }
    static int z12_chrony_socket_destroy(Z12ChronySocket **pp, Z12ChronySocketDiag *d) {
        Z12ChronySocket *p;
        int sc, pc, failed;
        if (pp == NULL || d == NULL) return -2;
        p = *pp;
        if (p == NULL) return 0;
        if (getpid() != p->creator_pid || gettid() != p->creator_tid) {
            d->native.foreign_binding = 1; return -2;
        }
        if (p->active != 0) { d->native.foreign_binding = 1; return -2; }
        *pp = NULL;
        sc = z12_sysd_close_owned(&p->socket_fd, &d->native);
        pc = z12_sysd_close_owned(&p->peer_fd, &d->native);
        failed = (sc != 0) || (pc != 0) || (d->native.cleanup_errno != 0);
        explicit_bzero(p, sizeof(*p)); free(p);
        return failed ? -1 : 0;
    }
    static int z12_chrony_socket_create(Z12SysdConn *manager, const char *endpoint, size_t endpoint_len,
                                        size_t max_name, Z12ChronySocket **out, Z12ChronySocketDiag *d) {
        Z12ChronySocket *c = NULL;
        Z12ImageCtx x = {0};
        struct sockaddr_un exp_addr = {0};
        socklen_t exp_len = 0;
        struct sockaddr_un local = {0};
        struct sockaddr_un got_local = {0};
        struct sockaddr_un got_peer = {0};
        socklen_t got_len = 0;
        Z12ReceiveSocketFacts snap = {0};
        int sock = -1, r, cleanup = 0;
        ssize_t gr;
        uint32_t seed = 0;
        socklen_t addrlen;
        size_t explen;
        if (d == NULL) return -2;
        memset(d, 0, sizeof(*d));
        if (out == NULL || *out != NULL || manager == NULL || endpoint == NULL ||
            endpoint_len == 0 || max_name == 0 || max_name > 256) {
            d->native.invalid_input = 1; return -2;
        }
        r = z12_conn_guard(manager, &d->native); if (r != 1) return r;
        if (manager->facts == NULL || manager->bus == NULL) { d->native.foreign_binding = 1; return 0; }
        x.conn = manager; x.facts = manager->facts;
        memcpy(&x.snapshot, manager->facts, sizeof(x.snapshot));
        x.bus = manager->bus; x.deadline = manager->deadline; x.end = manager->expected_end_ns;
        x.pidfd = x.snapshot.self_pidfd;
        r = z12_conn_endpoint(endpoint, endpoint_len, &exp_addr, &exp_len, &d->native);
        if (r != 1) return r;
        explen = (size_t)exp_len;
        c = (Z12ChronySocket *)calloc(1, sizeof(*c));
        if (c == NULL) { z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno); return -1; }
        c->socket_fd = -1; c->peer_fd = -1;
        c->manager = manager;
        memcpy(&c->owner, &x, sizeof(x));
        c->creator_pid = getpid(); c->creator_tid = gettid();
        c->max_name = max_name; c->counter64 = 0;
        c->seed_ready = 0; c->active = 0; c->unusable = 0;
        c->has_sock_snapshot = 0;
        memset(&c->sock_snapshot, 0, sizeof(c->sock_snapshot));
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        sock = socket(AF_UNIX, SOCK_DGRAM|SOCK_NONBLOCK|SOCK_CLOEXEC, 0);
        r = z12_s_post(c, d, sock); if (r != 1) goto fail;
        if (sock < 0) { r = -1; goto fail; }
        {
            int fl = 0;
            r = z12_s_flags(c, sock, F_GETFD, &fl, d); if (r != 1) goto fail;
            if ((fl & FD_CLOEXEC) == 0) { d->native.foreign_binding = 1; r = 0; goto fail; }
            r = z12_s_flags(c, sock, F_GETFL, &fl, d); if (r != 1) goto fail;
            if ((fl & O_NONBLOCK) == 0) { d->native.foreign_binding = 1; r = 0; goto fail; }
        }
        memset(&local, 0, sizeof(local));
        local.sun_family = AF_UNIX;
        addrlen = (socklen_t)sizeof(sa_family_t);
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        r = bind(sock, (struct sockaddr *)&local, addrlen);
        r = z12_s_post(c, d, r == 0 ? 0 : -1); if (r != 1) goto fail;
        r = z12_s_set_verify(c, sock, SO_PASSCRED, d); if (r != 1) goto fail;
        r = z12_s_set_verify(c, sock, SO_PASSPIDFD, d); if (r != 1) goto fail;
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        r = connect(sock, (struct sockaddr *)&exp_addr, exp_len);
        r = z12_s_post(c, d, r == 0 ? 0 : -1); if (r != 1) goto fail;
        got_len = sizeof(got_local);
        memset(&got_local, 0, sizeof(got_local));
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        r = getsockname(sock, (struct sockaddr *)&got_local, &got_len);
        r = z12_s_post(c, d, r == 0 ? 0 : -1); if (r != 1) goto fail;
        if (got_local.sun_family != AF_UNIX || got_len <= (socklen_t)sizeof(sa_family_t) ||
            got_len > (socklen_t)sizeof(got_local) || got_local.sun_path[0] != '\0') {
            d->native.foreign_binding = 1; r = 0; goto fail;
        }
        got_len = sizeof(got_peer);
        memset(&got_peer, 0, sizeof(got_peer));
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        r = getpeername(sock, (struct sockaddr *)&got_peer, &got_len);
        r = z12_s_post(c, d, r == 0 ? 0 : -1); if (r != 1) goto fail;
        if (got_len != exp_len || got_peer.sun_family != AF_UNIX ||
            memcmp(got_peer.sun_path, exp_addr.sun_path,
                   explen - offsetof(struct sockaddr_un, sun_path)) != 0) {
            d->native.foreign_binding = 1; r = 0; goto fail;
        }
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        gr = getrandom(&seed, sizeof(seed), GRND_NONBLOCK);
        if (gr < 0) { z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno); r = z12_s_guard(c, d); goto fail; }
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        if ((size_t)gr != sizeof(seed)) { d->native.native_output_invalid = 1; r = 0; goto fail; }
        c->seed32 = seed; c->seed_ready = 1;
        r = z12_s_facts(c, sock, &snap, d); if (r != 1) goto fail;
        if (snap.peer_length != exp_len ||
            memcmp(snap.peer.sun_path, exp_addr.sun_path,
                   explen - offsetof(struct sockaddr_un, sun_path)) != 0) {
            d->native.foreign_binding = 1; r = 0; goto fail;
        }
        memcpy(&c->sock_snapshot, &snap, sizeof(snap));
        c->has_sock_snapshot = 1;
        explicit_bzero(&seed, sizeof(seed));
        explicit_bzero(&snap, sizeof(snap));
        r = z12_s_guard(c, d); if (r != 1) goto fail;
        c->socket_fd = sock; sock = -1;
        c->active = 0;
        r = z12_chrony_socket_guard(c, d); if (r != 1) goto fail;
        r = z12_s_verdict(d, r); if (r != 1) goto fail;
        *out = c; c = NULL; return 1;
    fail:
        explicit_bzero(&seed, sizeof(seed));
        explicit_bzero(&snap, sizeof(snap));
        if (c != NULL) {
            cleanup |= z12_sysd_close_owned(&c->socket_fd, &d->native) != 0;
            cleanup |= z12_sysd_close_owned(&c->peer_fd, &d->native) != 0;
            explicit_bzero(c, sizeof(*c)); free(c);
        }
        cleanup |= z12_sysd_close_owned(&sock, &d->native) != 0;
        r = z12_s_verdict(d, cleanup ? -1 : r);
        return r;
    }
    """
    ctypedef struct Z12ChronySocket:
        pass
    ctypedef struct Z12ChronySocketDiag:
        Z12SysdDiag native
        int openssl_failed
        int openssl_stage
        int openssl_code
    int z12_chrony_socket_create(Z12SysdConn *manager, const char *endpoint, size_t endpoint_len, size_t max_name, Z12ChronySocket **out, Z12ChronySocketDiag *diag)
    int z12_chrony_socket_guard(Z12ChronySocket *s, Z12ChronySocketDiag *diag)
    int z12_chrony_socket_destroy(Z12ChronySocket **pp, Z12ChronySocketDiag *diag)
