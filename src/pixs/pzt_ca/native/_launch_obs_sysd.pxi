# Prive Z12 : faits SELF+PEER, aucune admission et aucun RPC.
# Inclure APRES _monotonic_deadline.pxi, une seule fois ; build -D_GNU_SOURCE.
# Bus emprunte exclusif : son proprietaire maintient sa duree de vie.
# Suite requise : connecteur AF_UNIX, unite/MainPID/InvocationID, artefacts,
# politique/epoque/cible, UTC et D9/D10/D15 avant toute admission.
from libc.stdint cimport uint64_t
from posix.types cimport pid_t, uid_t
cdef extern from "systemd/sd-bus.h" nogil:
    ctypedef struct sd_bus:
        pass

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <unistd.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/un.h>
    #include <sys/pidfd.h>
    #include <poll.h>
    #include <fcntl.h>
    #include <systemd/sd-bus.h>

    enum { Z12_SYSD_NONE=0, Z12_SYSD_ERRNO=1,
           Z12_SYSD_LIBRARY=2, Z12_SYSD_CLOCK=3 };
    typedef struct {
        int primary_kind, primary_code, cleanup_errno;
        int invalid_input, native_output_invalid, foreign_binding;
        int process_unavailable, deadline_expired, clock_failed, clock_errno;
        int must_destroy_bus;
    } Z12SysdDiag;
    typedef struct {
        pid_t self_pid, peer_pid;
        uid_t self_uid, self_euid, peer_euid_at_connect;
        int self_pidfd, peer_pidfd, bus_fd;
        sd_bus *borrowed_bus;
        uint64_t observed_monotonic_ns, expected_end_ns;
    } Z12SysdFacts;

    static void z12_sysd_first(Z12SysdDiag *d, int kind, int code) {
        if (d != NULL && d->primary_kind == Z12_SYSD_NONE) {
            d->primary_kind = kind; d->primary_code = code;
        }
    }
    static int z12_sysd_close_owned(int *fd, Z12SysdDiag *d) {
        int saved, owned;
        if (fd == NULL) return -2;
        owned = *fd; *fd = -1;
        if (owned < 0) return 0;
        if (close(owned) == 0) return 0;
        saved = errno;
        if (d != NULL) {
            if (d->cleanup_errno == 0) d->cleanup_errno = saved;
            d->must_destroy_bus = 1;
        }
        /* Linux : ne pas retenter close, meme apres EINTR. */
        return -1;
    }
    static int z12_sysd_facts_destroy(Z12SysdFacts **pp, Z12SysdDiag *d) {
        Z12SysdFacts *p;
        int first, second;
        if (pp == NULL) return -2;
        p = *pp; *pp = NULL;
        if (p == NULL) return 0;
        first = z12_sysd_close_owned(&p->self_pidfd, d);
        second = z12_sysd_close_owned(&p->peer_pidfd, d);
        /* Aucun close/unref/flush du bus emprunte. */
        explicit_bzero(p, sizeof(*p)); free(p);
        return first != 0 || second != 0 ? -1 : 0;
    }
    static int z12_sysd_deadline(Z12MonotonicDeadline *d, uint64_t expected,
                                 Z12SysdDiag *diag) {
        int32_t ignored_ms = 0;
        int status, saved;
        if (d == NULL || d->started != 1 || d->end_ns == 0 || expected == 0) {
            diag->invalid_input = 1; return -2;
        }
        if (d->end_ns != expected) {
            diag->foreign_binding = 1; diag->must_destroy_bus = 1; return 0;
        }
        status = z12_deadline_remaining(d, &ignored_ms);
        saved = errno;
        if (status == 1) return 1;
        diag->must_destroy_bus = 1;
        if (status == 0) { diag->deadline_expired = 1; return 0; }
        if (status == -1) {
            diag->clock_failed = 1; diag->clock_errno = saved;
            z12_sysd_first(diag, Z12_SYSD_CLOCK, saved); return -1;
        }
        diag->invalid_input = 1; return -2;
    }
    static int z12_sysd_pidfd_live(int fd, Z12SysdDiag *diag) {
        struct pollfd p = {0};
        int flags, r;
        if (fd < 0) { diag->invalid_input = 1; return -2; }
        flags = fcntl(fd, F_GETFD);
        if (flags < 0) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1;
        }
        if ((flags & FD_CLOEXEC) == 0) {
            diag->native_output_invalid = 1; return 0;
        }
        p.fd = fd; p.events = POLLIN;
        r = poll(&p, 1, 0);
        if (r < 0) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1;
        }
        if (r == 0) return 1;
        if ((p.revents & (POLLIN|POLLHUP|POLLERR|POLLNVAL)) != 0) {
            diag->process_unavailable = 1; return 0;
        }
        diag->native_output_invalid = 1; return -1;
    }
    static int z12_sysd_bus_facts(sd_bus *bus, int *fd, struct ucred *peer,
                                  Z12SysdDiag *diag) {
        int r, type = 0, socket_fd;
        socklen_t size = sizeof(type), peer_size = sizeof(*peer);
        struct sockaddr_un address = {0};
        socklen_t address_size = sizeof(address);
        r = sd_bus_is_ready(bus);
        if (r < 0) { z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); return -1; }
        if (r != 1) { diag->foreign_binding = 1; return 0; }
        r = sd_bus_is_bus_client(bus);
        if (r < 0) { z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); return -1; }
        if (r != 0) { diag->foreign_binding = 1; return 0; }
        r = sd_bus_is_server(bus);
        if (r < 0) { z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); return -1; }
        if (r != 0) { diag->foreign_binding = 1; return 0; }
        socket_fd = sd_bus_get_fd(bus);
        if (socket_fd < 0) {
            z12_sysd_first(diag, Z12_SYSD_LIBRARY, socket_fd); return -1;
        }
        if (getsockopt(socket_fd, SOL_SOCKET, SO_TYPE, &type, &size) != 0) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1;
        }
        if (size != sizeof(type)) { diag->native_output_invalid = 1; return -1; }
        if (type != SOCK_STREAM) { diag->foreign_binding = 1; return 0; }
        if (getpeername(socket_fd, (struct sockaddr *)&address, &address_size) != 0) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1;
        }
        if (address_size < sizeof(sa_family_t) || address_size > sizeof(address)) {
            diag->native_output_invalid = 1; return -1;
        }
        if (address.sun_family != AF_UNIX) { diag->foreign_binding = 1; return 0; }
        memset(peer, 0, sizeof(*peer));
        if (getsockopt(socket_fd, SOL_SOCKET, SO_PEERCRED, peer, &peer_size) != 0) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1;
        }
        if (peer_size != sizeof(*peer) || peer->pid <= 0) {
            diag->native_output_invalid = 1; return -1;
        }
        *fd = socket_fd; return 1;
    }
    /* 1 : faits collectes ; 0 : refus ; -1 : erreur ; -2 : contrat invalide.
       Ce resultat ne prouve ni le role manager, ni politique, ni admission. */
    static int z12_sysd_collect(sd_bus *bus, Z12MonotonicDeadline *deadline,
                               uint64_t expected_end, Z12SysdFacts **out,
                               Z12SysdDiag *diag) {
        const uint64_t required = SD_BUS_CREDS_PID|SD_BUS_CREDS_EUID|SD_BUS_CREDS_PIDFD;
        sd_bus_creds *creds = NULL;
        Z12SysdFacts *facts = NULL;
        pid_t self_pid, peer_pid = 0;
        uid_t self_uid, self_euid, peer_euid = (uid_t)-1;
        int self_fd = -1, peer_fd = -1, first_fd = -1, final_fd = -1;
        int result = -1, r, cleanup_failed = 0;
        uint64_t mask, augmented;
        struct ucred before = {0}, after = {0};
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        if (out == NULL || *out != NULL || bus == NULL ||
            bus == SD_BUS_DEFAULT || bus == SD_BUS_DEFAULT_USER ||
            bus == SD_BUS_DEFAULT_SYSTEM) {
            diag->invalid_input = 1; return -2;
        }
        result = z12_sysd_deadline(deadline, expected_end, diag);
        if (result != 1) return result;
        result = z12_sysd_bus_facts(bus, &first_fd, &before, diag);
        if (result != 1) { diag->must_destroy_bus = 1; return result; }
        result = z12_sysd_deadline(deadline, expected_end, diag);
        if (result != 1) return result;
        self_pid = getpid(); self_uid = getuid(); self_euid = geteuid();
        if (self_pid <= 0) { diag->native_output_invalid = 1; return -1; }
        self_fd = pidfd_open(self_pid, 0);
        if (self_fd < 0) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); return -1;
        }
        result = z12_sysd_pidfd_live(self_fd, diag);
        if (result != 1) goto fail;
        result = z12_sysd_deadline(deadline, expected_end, diag);
        if (result != 1) goto fail;
        r = sd_bus_get_owner_creds(bus, required, &creds);
        if (r < 0) z12_sysd_first(diag, Z12_SYSD_LIBRARY, r);
        result = z12_sysd_deadline(deadline, expected_end, diag);
        if (result != 1) goto fail;
        if (r < 0 || creds == NULL) {
            if (r >= 0) diag->native_output_invalid = 1;
            result = -1; goto fail;
        }
        mask = sd_bus_creds_get_mask(creds);
        augmented = sd_bus_creds_get_augmented_mask(creds);
        if ((mask & required) != required || (augmented & required) != 0) {
            diag->foreign_binding = 1; result = 0; goto fail;
        }
        r = sd_bus_creds_get_pid(creds, &peer_pid);
        if (r < 0) {
            z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); result = -1; goto fail;
        }
        r = sd_bus_creds_get_euid(creds, &peer_euid);
        if (r < 0) {
            z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); result = -1; goto fail;
        }
        if (peer_pid <= 0 || before.pid != peer_pid || before.uid != peer_euid) {
            diag->foreign_binding = 1; result = 0; goto fail;
        }
        r = sd_bus_creds_get_pidfd_dup(creds, &peer_fd);
        if (r < 0) {
            z12_sysd_first(diag, Z12_SYSD_LIBRARY, r); result = -1; goto fail;
        }
        sd_bus_creds_unref(creds); creds = NULL;
        result = z12_sysd_pidfd_live(peer_fd, diag);
        if (result != 1) goto fail;
        facts = (Z12SysdFacts *)calloc(1, sizeof(*facts));
        if (facts == NULL) {
            z12_sysd_first(diag, Z12_SYSD_ERRNO, errno); result = -1; goto fail;
        }
        facts->self_pidfd = -1; facts->peer_pidfd = -1;
        result = z12_sysd_bus_facts(bus, &final_fd, &after, diag);
        if (result != 1) goto fail;
        if (final_fd != first_fd || after.pid != before.pid || after.uid != before.uid ||
            self_pid != getpid() || self_uid != getuid() || self_euid != geteuid()) {
            diag->foreign_binding = 1; result = 0; goto fail;
        }
        result = z12_sysd_pidfd_live(self_fd, diag);
        if (result != 1) goto fail;
        result = z12_sysd_pidfd_live(peer_fd, diag);
        if (result != 1) goto fail;
        result = z12_sysd_deadline(deadline, expected_end, diag);
        if (result != 1) goto fail;
        facts->self_pid = self_pid; facts->self_uid = self_uid; facts->self_euid = self_euid;
        facts->peer_pid = peer_pid; facts->peer_euid_at_connect = peer_euid;
        facts->self_pidfd = self_fd; self_fd = -1;
        facts->peer_pidfd = peer_fd; peer_fd = -1;
        facts->bus_fd = first_fd; facts->borrowed_bus = bus;
        facts->observed_monotonic_ns = deadline->last_seen_ns;
        facts->expected_end_ns = expected_end;
        *out = facts; return 1;
    fail:
        diag->must_destroy_bus = 1;
        if (creds != NULL) sd_bus_creds_unref(creds);
        cleanup_failed |= z12_sysd_close_owned(&self_fd, diag) != 0;
        cleanup_failed |= z12_sysd_close_owned(&peer_fd, diag) != 0;
        if (facts != NULL) { explicit_bzero(facts, sizeof(*facts)); free(facts); }
        return cleanup_failed || diag->primary_kind != Z12_SYSD_NONE ? -1 : result;
    }
    """
    ctypedef struct Z12SysdDiag:
        int primary_kind
        int primary_code
        int cleanup_errno
        int invalid_input
        int native_output_invalid
        int foreign_binding
        int process_unavailable
        int deadline_expired
        int clock_failed
        int clock_errno
        int must_destroy_bus
    ctypedef struct Z12SysdFacts:
        pid_t self_pid
        pid_t peer_pid
        uid_t self_uid
        uid_t self_euid
        uid_t peer_euid_at_connect
        int self_pidfd
        int peer_pidfd
        int bus_fd
        sd_bus *borrowed_bus
        uint64_t observed_monotonic_ns
        uint64_t expected_end_ns
    int z12_sysd_collect(sd_bus *bus, Z12MonotonicDeadline *deadline,
                         uint64_t expected_end, Z12SysdFacts **out, Z12SysdDiag *diag)
    int z12_sysd_facts_destroy(Z12SysdFacts **pp, Z12SysdDiag *diag)
