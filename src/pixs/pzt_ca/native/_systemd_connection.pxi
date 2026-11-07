# Prive Z12 : connexion locale effective, sans admission ni RPC metier.
# Inclure apres deadline puis _launch_obs_sysd.pxi, une seule fois ; -D_GNU_SOURCE.
# Endpoint interne resolu par composition native ; politique/artefacts/manager,
# unite/InvocationID, UTC et D9/D10/D15 restent requis avant admission.
# Les contextes sont exclusifs au processus createur et ne traversent pas fork.
# En cas de fork, l'enfant doit abandonner son processus ; aucun exit ici.
from libc.stddef cimport size_t
from libc.stdint cimport uint64_t
from posix.types cimport pid_t, uid_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stddef.h>
    #include <limits.h>
    #include <time.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <poll.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/un.h>
    #include <systemd/sd-bus.h>
    #include <systemd/sd-id128.h>
    typedef struct {
        sd_bus *bus;
        Z12SysdFacts *facts;
        pid_t creator_pid;
        uid_t creator_uid, creator_euid;
        Z12MonotonicDeadline *deadline;
        uint64_t expected_end_ns;
    } Z12SysdConn;

    static int z12_conn_guard(Z12SysdConn *c, Z12SysdDiag *d) {
        if (c == NULL || d == NULL) return -2;
        if (getpid() != c->creator_pid || getuid() != c->creator_uid ||
            geteuid() != c->creator_euid) {
            d->foreign_binding = 1; d->must_destroy_bus = 1; return 0;
        }
        return z12_sysd_deadline(c->deadline, c->expected_end_ns, d);
    }
    static int z12_sysd_conn_destroy(Z12SysdConn **pp, Z12SysdDiag *d) {
        Z12SysdConn *c;
        int failed = 0;
        if (pp == NULL || d == NULL) return -2;
        c = *pp;
        if (c == NULL) return 0;
        if (getpid() != c->creator_pid) {
            /* Ne pas perdre la reference ni appeler libsystemd apres fork.
               Le proprietaire doit faire terminer son enfant, sans toucher
               au processus parent. Aucune fermeture complete n'est revendiquee. */
            d->foreign_binding = 1; d->must_destroy_bus = 1; return -2;
        }
        *pp = NULL;
        if (z12_sysd_facts_destroy(&c->facts, d) != 0) failed = 1;
        if (c->bus != NULL) c->bus = sd_bus_close_unref(c->bus);
        explicit_bzero(c, sizeof(*c)); free(c);
        return failed ? -1 : 0;
    }
    static int z12_conn_endpoint(const char *bytes, size_t length,
                                 struct sockaddr_un *address, socklen_t *addrlen,
                                 Z12SysdDiag *diag) {
        size_t body;
        if (bytes == NULL || address == NULL || addrlen == NULL) {
            if (diag != NULL) diag->invalid_input = 1;
            return -2;
        }
        if (length < 2 || length > sizeof(address->sun_path)) {
            if (diag != NULL) diag->invalid_input = 1;
            return -2;
        }
        if (bytes[0] != '/') {
            if (diag != NULL) diag->foreign_binding = 1;
            return 0;
        }
        if (bytes[length - 1] != '\0') {
            if (diag != NULL) diag->invalid_input = 1;
            return -2;
        }
        body = strnlen(bytes, length);
        if (body != length - 1) {
            if (diag != NULL) diag->invalid_input = 1;
            return -2;
        }
        memset(address, 0, sizeof(*address));
        address->sun_family = AF_UNIX;
        memcpy(address->sun_path, bytes, length);
        if ((size_t)offsetof(struct sockaddr_un, sun_path) > (size_t)INT_MAX - length) {
            if (diag != NULL) diag->native_output_invalid = 1;
            return -1;
        }
        *addrlen = (socklen_t)(offsetof(struct sockaddr_un, sun_path) + length);
        if (*addrlen > (socklen_t)sizeof(*address) ||
            *addrlen <= (socklen_t)sizeof(sa_family_t)) {
            if (diag != NULL) diag->native_output_invalid = 1;
            return -1;
        }
        return 1;
    }
    static int z12_conn_flags(int fd, Z12SysdDiag *diag) {
        int fl, fdf;
        fl = fcntl(fd, F_GETFL);
        if (fl < 0) { if (diag != NULL) z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1; }
        if ((fl & O_NONBLOCK) == 0) {
            if (diag != NULL) diag->native_output_invalid = 1;
            return -1;
        }
        fdf = fcntl(fd, F_GETFD);
        if (fdf < 0) { if (diag != NULL) z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1; }
        if ((fdf & FD_CLOEXEC) == 0) {
            if (diag != NULL) diag->native_output_invalid = 1;
            return -1;
        }
        return 1;
    }
    static int z12_conn_check_connected(int fd, Z12SysdDiag *diag) {
        int value = -1;
        socklen_t size = sizeof(value);
        struct sockaddr_un peer = {0};
        socklen_t peerlen = sizeof(peer);
        if (getsockopt(fd, SOL_SOCKET, SO_ERROR, &value, &size) != 0) {
            if (diag != NULL) z12_sysd_first(diag, Z12_SYSD_ERRNO, errno);
            return -1;
        }
        if (size != sizeof(value)) {
            if (diag != NULL) diag->native_output_invalid = 1;
            return -1;
        }
        if (value != 0) {
            if (diag != NULL) z12_sysd_first(diag, Z12_SYSD_ERRNO, value);
            return -1;
        }
        if (getpeername(fd, (struct sockaddr *)&peer, &peerlen) != 0) {
            if (diag != NULL) z12_sysd_first(diag, Z12_SYSD_ERRNO, errno);
            return -1;
        }
        if (peerlen < (socklen_t)sizeof(sa_family_t) || peerlen > (socklen_t)sizeof(peer)) {
            if (diag != NULL) diag->native_output_invalid = 1;
            return -1;
        }
        if (peer.sun_family != AF_UNIX) {
            if (diag != NULL) diag->foreign_binding = 1;
            return 0;
        }
        return 1;
    }

    static int z12_conn_timespec(uint64_t ns, struct timespec *t,
                                 Z12SysdDiag *d) {
        uint64_t seconds = ns / UINT64_C(1000000000);
        t->tv_sec = (time_t)seconds;
        t->tv_nsec = (long)(ns % UINT64_C(1000000000));
        if (t->tv_sec < 0 || (uint64_t)t->tv_sec != seconds) {
            d->native_output_invalid = 1; return -1;
        }
        return 1;
    }
    static int z12_conn_wait_connect(int fd, Z12SysdConn *c, Z12SysdDiag *d) {
        struct pollfd p = {0};
        struct timespec t;
        int r, status;
        status = z12_conn_guard(c, d);
        if (status != 1) return status;
        status = z12_conn_timespec(c->expected_end_ns - c->deadline->last_seen_ns, &t, d);
        if (status != 1) return status;
        p.fd = fd; p.events = POLLOUT;
        r = ppoll(&p, 1, &t, NULL);
        if (r < 0) z12_sysd_first(d, Z12_SYSD_ERRNO, errno);
        status = z12_conn_guard(c, d);
        if (r < 0) return -1;
        if (status != 1) return status;
        if (r == 0 || (p.revents & (POLLERR|POLLHUP|POLLNVAL)) != 0 ||
            (p.revents & POLLOUT) == 0) {
            d->native_output_invalid = 1; return 0;
        }
        status = z12_conn_check_connected(fd, d);
        if (status != 1) return status;
        return z12_conn_guard(c, d);
    }
    static int z12_conn_wait_auth(Z12SysdConn *c, Z12SysdDiag *d) {
        struct pollfd p = {0};
        struct timespec t;
        uint64_t lib_usec, end, now, delta;
        int fd, events, r, status;
        status = z12_conn_guard(c, d);
        if (status != 1) return status;
        fd = sd_bus_get_fd(c->bus);
        if (fd < 0) { z12_sysd_first(d, Z12_SYSD_LIBRARY, fd); return -1; }
        events = sd_bus_get_events(c->bus);
        if (events < 0) { z12_sysd_first(d, Z12_SYSD_LIBRARY, events); return -1; }
        if ((events & ~(POLLIN|POLLOUT)) != 0) {
            d->native_output_invalid = 1; return -1;
        }
        lib_usec = UINT64_MAX;
        r = sd_bus_get_timeout(c->bus, &lib_usec);
        if (r < 0) z12_sysd_first(d, Z12_SYSD_LIBRARY, r);
        status = z12_conn_guard(c, d);
        if (r < 0) return -1;
        if (status != 1) return status;
        now = c->deadline->last_seen_ns; end = c->expected_end_ns;
        if (lib_usec != UINT64_MAX) {
            if (lib_usec > UINT64_MAX / UINT64_C(1000)) {
                d->native_output_invalid = 1; return -1;
            }
            /* Echeance de libsystemd deja absolue, jamais ajouter now. */
            if (lib_usec * UINT64_C(1000) < end) end = lib_usec * UINT64_C(1000);
        }
        delta = end <= now ? 0 : end - now;
        status = z12_conn_timespec(delta, &t, d);
        if (status != 1) return status;
        p.fd = fd; p.events = (short)events;
        r = ppoll(&p, 1, &t, NULL);
        if (r < 0) z12_sysd_first(d, Z12_SYSD_ERRNO, errno);
        status = z12_conn_guard(c, d);
        if (r < 0) return -1;
        if (status != 1) return status;
        if (r > 0 && (p.revents & (POLLERR|POLLHUP|POLLNVAL)) != 0) {
            d->process_unavailable = 1; return 0;
        }
        if (r > 0 && (p.revents & ~(POLLIN|POLLOUT)) != 0) {
            d->native_output_invalid = 1; return -1;
        }
        /* Timeout interne de libsystemd : traiter au prochain process(). */
        return 1;
    }
    /* Source intermediaire ; l'endpoint et le manager restent a authentifier
       par le proprietaire complet. Longueur endpoint incluant le NUL final. */
    static int z12_sysd_connect(const char *endpoint, size_t endpoint_size,
                                Z12MonotonicDeadline *deadline, uint64_t expected,
                                Z12SysdConn **out, Z12SysdDiag *diag) {
        Z12SysdConn *c = NULL;
        Z12SysdDiag observed = {0};
        struct sockaddr_un address = {0};
        socklen_t address_size = 0;
        pid_t entered;
        uid_t uid, euid;
        int fd = -1, r, result = -1, saved, cleanup_failed = 0;
        uint64_t required = SD_BUS_CREDS_PID|SD_BUS_CREDS_EUID|SD_BUS_CREDS_PIDFD;
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        if (out == NULL || *out != NULL || deadline == NULL) {
            diag->invalid_input = 1; return -2;
        }
        entered = getpid(); uid = getuid(); euid = geteuid();
        if (entered <= 0) { diag->native_output_invalid = 1; return -1; }
        result = z12_sysd_deadline(deadline, expected, diag);
        if (result != 1) return result;
        result = z12_conn_endpoint(endpoint, endpoint_size, &address, &address_size, diag);
        if (result != 1) return result;
        c = (Z12SysdConn *)calloc(1, sizeof(*c));
        if (c == NULL) { z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1; }
        c->creator_pid = entered; c->creator_uid = uid; c->creator_euid = euid;
        c->deadline = deadline; c->expected_end_ns = expected;
        result = z12_conn_guard(c, diag);
        if (result != 1) goto fail;
        fd = socket(AF_UNIX, SOCK_STREAM|SOCK_NONBLOCK|SOCK_CLOEXEC, 0);
        if (fd < 0) { z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); result = -1; goto fail; }
        result = z12_conn_flags(fd, diag);
        if (result != 1) goto fail;
        result = z12_conn_guard(c, diag);
        if (result != 1) goto fail;
        r = connect(fd, (struct sockaddr *)&address, address_size);
        saved = errno;
        if (r < 0 && saved != EINPROGRESS) z12_sysd_first(diag, Z12_SYSD_ERRNO, saved);
        result = z12_conn_guard(c, diag);
        if (r < 0 && saved != EINPROGRESS) { result = -1; goto fail; }
        if (result != 1) goto fail;
        if (r < 0) result = z12_conn_wait_connect(fd, c, diag);
        else result = z12_conn_check_connected(fd, diag);
        if (result != 1) goto fail;
        result = z12_conn_guard(c, diag);
        if (result != 1) goto fail;

        /* Chaque appel de configuration est encadre ; aucune RPC metier. */
        #define Z12_CONN_SETUP(expression) do { \
            result = z12_conn_guard(c, diag); if (result != 1) goto fail; \
            r = (expression); \
            if (r < 0) { z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); result = -1; goto fail; } \
            result = z12_conn_guard(c, diag); if (result != 1) goto fail; \
        } while (0)
        Z12_CONN_SETUP(sd_bus_new(&c->bus));
        if (c->bus == NULL) { diag->native_output_invalid = 1; result = -1; goto fail; }
        result = z12_conn_guard(c, diag);
        if (result != 1) goto fail;
        r = sd_bus_set_fd(c->bus, fd, fd);
        if (r < 0) { z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); result = -1; goto fail; }
        /* Transfert immediat, meme si le controle suivant refuse. */
        fd = -1;
        result = z12_conn_guard(c, diag);
        if (result != 1) goto fail;
        Z12_CONN_SETUP(sd_bus_set_bus_client(c->bus, 0));
        Z12_CONN_SETUP(sd_bus_set_server(c->bus, 0, SD_ID128_NULL));
        Z12_CONN_SETUP(sd_bus_set_anonymous(c->bus, 0));
        Z12_CONN_SETUP(sd_bus_set_allow_interactive_authorization(c->bus, 0));
        Z12_CONN_SETUP(sd_bus_set_exit_on_disconnect(c->bus, 0));
        Z12_CONN_SETUP(sd_bus_negotiate_fds(c->bus, 1));
        Z12_CONN_SETUP(sd_bus_negotiate_creds(c->bus, 1, required));
        Z12_CONN_SETUP(sd_bus_start(c->bus));
        #undef Z12_CONN_SETUP

        for (;;) {
            result = z12_conn_guard(c, diag);
            if (result != 1) goto fail;
            r = sd_bus_is_ready(c->bus);
            if (r < 0) z12_sysd_first(diag, Z12_SYSD_LIBRARY, r);
            result = z12_conn_guard(c, diag);
            if (r < 0) { result = -1; goto fail; }
            if (result != 1) goto fail;
            if (r == 1) break;
            r = sd_bus_process(c->bus, NULL);
            if (r < 0) z12_sysd_first(diag, Z12_SYSD_LIBRARY, r);
            result = z12_conn_guard(c, diag);
            if (r < 0) { result = -1; goto fail; }
            if (result != 1) goto fail;
            if (r > 0) continue;
            result = z12_conn_wait_auth(c, diag);
            if (result != 1) goto fail;
        }
        result = z12_conn_guard(c, diag);
        if (result != 1) goto fail;
        if (diag->primary_kind != Z12_SYSD_NONE || diag->cleanup_errno != 0) {
            result = -1; goto fail;
        }
        r = z12_sysd_collect(c->bus, deadline, expected, &c->facts, &observed);
        /* Aucun diagnostic precedent a ecraser : les etapes ont toutes reussi. */
        memcpy(diag, &observed, sizeof(*diag));
        result = z12_conn_guard(c, diag);
        if (r != 1) { result = r; goto fail; }
        if (result != 1) goto fail;
        if (diag->primary_kind != Z12_SYSD_NONE || diag->cleanup_errno != 0 ||
            diag->must_destroy_bus != 0 || c->facts == NULL) {
            diag->native_output_invalid = 1; result = -1; goto fail;
        }
        *out = c; return 1;
    fail:
        diag->must_destroy_bus = 1;
        cleanup_failed |= z12_sysd_close_owned(&fd, diag) != 0;
        if (c != NULL && getpid() != c->creator_pid) {
            /* Contrat de processus viole : libsystemd ne libere pas apres
               fork. Ressources heritees retenues jusqu'a la sortie de
               l'enfant, que le proprietaire doit imposer sans shutdown parent.
               Aucun contexte favorable ni fausse fermeture complete. */
            diag->foreign_binding = 1; return -2;
        }
        cleanup_failed |= z12_sysd_conn_destroy(&c, diag) != 0;
        return cleanup_failed || diag->primary_kind != Z12_SYSD_NONE ? -1 : result;
    }
    """
    ctypedef struct Z12SysdConn:
        sd_bus *bus
        Z12SysdFacts *facts
        pid_t creator_pid
        uid_t creator_uid
        uid_t creator_euid
        Z12MonotonicDeadline *deadline
        uint64_t expected_end_ns
    int z12_sysd_connect(const char *endpoint, size_t endpoint_size,
                         Z12MonotonicDeadline *deadline, uint64_t expected,
                         Z12SysdConn **out, Z12SysdDiag *diag)
    int z12_sysd_conn_destroy(Z12SysdConn **pp, Z12SysdDiag *diag)
