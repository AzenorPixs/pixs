# cython: language_level=3
"""Faits natifs SELF/PEER_AT_CONNECT, sans admission ni connexion implicite.
Lookup readonly optionnel d'unité/InvocationID observés depuis une connexion
READY, sans autorité nouvelle.

System seul, compilation Linux Debian 13 avec -D_GNU_SOURCE=1. Le prêteur
conserve sa référence et garantit l'exclusivité du bus pendant l'observation.
Une référence propre conserve le vrai sd_bus ; aucune fermeture/flush du bus.
Ces faits ne prouvent ni manager, unité/MainPID/InvocationID, artefacts,
politique/époque/cible, UTC, guardian D13 ou droit de remettre un secret.
Le lookup, quand DONE, publie seulement path/unit/InvocationID16/observed_ns
réellement lus par GetUnitByPIDFD du SELF : ni MainPID, ni rôle manager,
ni artefacts, ni politique/UTC/fraîcheur, ni guardian/remise D13.
"""
from libc.stddef cimport size_t
from libc.stdint cimport uint32_t, uint64_t, uint8_t

cdef extern from * nogil:
    r"""
    #ifndef _GNU_SOURCE
    #error "PA01_SYSTEMD_REQUIRES_GNU_SOURCE"
    #endif
    #include <stdint.h>
    #include <stddef.h>
    #include <errno.h>
    #include <stdlib.h>
    #include <string.h>
    #include <time.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <poll.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <sys/socket.h>
    #include <sys/un.h>
    #include <sys/pidfd.h>
    #include <sys/ioctl.h>
    #include <linux/nsfs.h>
    #include <sched.h>
    #include <systemd/sd-bus.h>

    enum { PA01SO_OK=0, PA01SO_ARG=1, PA01SO_MEM=2, PA01SO_CLOCK=3,
           PA01SO_STATE=4, PA01SO_EXPIRED=6, PA01SO_VERIFY=7,
           PA01SO_IO=8, PA01SO_CLEANUP=10 };
    typedef struct {
        int fd;
        dev_t dev;
        ino_t ino;
        pid_t pid;
        uid_t uid;
    } PA01SOProbe;
    #define PA01SO_KIND UINT64_C(0x50413031534f0001)
    typedef struct {
        uint64_t kind;
        pid_t pid, tid;
        uid_t uid, euid;
        sd_bus *bus;
        int self_fd, peer_fd;
        PA01SOProbe peer;
        uint64_t end_ns, last_ns;
        uint32_t failure, stage;
        int native_code, cleanup_errno;
    } PA01SOState;

    static uint32_t pa01so_fail(PA01SOState *s, uint32_t status,
                                uint32_t stage, int code) {
        if (s->failure == 0) {
            s->failure = status;
            s->stage = stage;
            s->native_code = code;
        }
        return s->failure;
    }
    static uint32_t pa01so_clock(PA01SOState *s) {
        struct timespec t;
        uint64_t sec, now;
        if (s->failure != 0) return s->failure;
        if (clock_gettime(CLOCK_MONOTONIC, &t) != 0)
            return pa01so_fail(s, PA01SO_CLOCK, 1, errno);
        if (t.tv_sec < 0 || t.tv_nsec < 0 || t.tv_nsec >= 1000000000L)
            return pa01so_fail(s, PA01SO_CLOCK, 1, EINVAL);
        sec = (uint64_t)t.tv_sec;
        if (sec > (UINT64_MAX - (uint64_t)t.tv_nsec) / UINT64_C(1000000000))
            return pa01so_fail(s, PA01SO_CLOCK, 1, EOVERFLOW);
        now = sec * UINT64_C(1000000000) + (uint64_t)t.tv_nsec;
        if (now == 0 || (s->last_ns != 0 && now < s->last_ns))
            return pa01so_fail(s, PA01SO_CLOCK, 1, ERANGE);
        if (now >= s->end_ns)
            return pa01so_fail(s, PA01SO_EXPIRED, 1, ETIMEDOUT);
        s->last_ns = now;
        return 0;
    }
    static int pa01so_owner(PA01SOState *s, int credentials) {
        if (getpid() != s->pid || gettid() != s->tid) return 0;
        return !credentials || (getuid() == s->uid && geteuid() == s->euid);
    }
    static void pa01so_diag(PA01SOState *s, uint32_t *stage,
                             int *code, int *cleanup) {
        *stage = s->stage;
        *code = s->native_code;
        *cleanup = s->cleanup_errno;
    }
    static int pa01so_close_fd(int *fd, PA01SOState *s) {
        int owned = *fd, saved;
        *fd = -1;
        if (owned < 0) return 0;
        if (close(owned) == 0) return 0;
        saved = errno;
        if (s->cleanup_errno == 0) s->cleanup_errno = saved;
        /* Linux : le FD propre est consommé, ne jamais retenter EINTR. */
        return -1;
    }
    static void pa01so_dispose(PA01SOState *s) {
        pa01so_close_fd(&s->self_fd, s);
        pa01so_close_fd(&s->peer_fd, s);
        if (s->bus != NULL) s->bus = sd_bus_unref(s->bus);
        /* Le code appelant copie le diagnostic avant nettoyage mémoire. */
    }
    static uint32_t pa01so_live(PA01SOState *s, int fd, uint32_t stage) {
        struct pollfd p = {0};
        int r;
        if (pa01so_clock(s) != 0) return s->failure;
        r = fcntl(fd, F_GETFD);
        if (r < 0) return pa01so_fail(s, PA01SO_IO, stage, errno);
        if (pa01so_clock(s) != 0) return s->failure;
        if ((r & FD_CLOEXEC) == 0)
            return pa01so_fail(s, PA01SO_VERIFY, stage, EPROTO);
        p.fd = fd;
        p.events = POLLIN;
        if (pa01so_clock(s) != 0) return s->failure;
        r = poll(&p, 1, 0);
        if (r < 0) return pa01so_fail(s, PA01SO_IO, stage, errno);
        if (pa01so_clock(s) != 0) return s->failure;
        if (r != 0)
            return pa01so_fail(s, PA01SO_VERIFY, stage,
                (p.revents & (POLLIN|POLLHUP|POLLERR|POLLNVAL)) ? ESRCH : EPROTO);
        return 0;
    }
    static uint32_t pa01so_socket(PA01SOState *s, PA01SOProbe *out) {
        int r, fd, type = 0;
        socklen_t size;
        struct stat st;
        struct sockaddr_un address = {0};
        struct ucred peer = {0};
        if (pa01so_clock(s) != 0) return s->failure;
        r = sd_bus_is_ready(s->bus);
        if (r < 0) return pa01so_fail(s, PA01SO_IO, 2, r);
        if (pa01so_clock(s) != 0) return s->failure;
        if (r != 1) return pa01so_fail(s, PA01SO_VERIFY, 2, ENOTCONN);
        r = sd_bus_is_bus_client(s->bus);
        if (r < 0) return pa01so_fail(s, PA01SO_IO, 2, r);
        if (pa01so_clock(s) != 0) return s->failure;
        if (r != 0) return pa01so_fail(s, PA01SO_VERIFY, 2, EPROTO);
        r = sd_bus_is_server(s->bus);
        if (r < 0) return pa01so_fail(s, PA01SO_IO, 2, r);
        if (pa01so_clock(s) != 0) return s->failure;
        if (r != 0) return pa01so_fail(s, PA01SO_VERIFY, 2, EPROTO);
        fd = sd_bus_get_fd(s->bus);
        if (fd < 0) return pa01so_fail(s, PA01SO_IO, 2, fd);
        if (pa01so_clock(s) != 0) return s->failure;
        if (fstat(fd, &st) != 0) return pa01so_fail(s, PA01SO_IO, 2, errno);
        if (pa01so_clock(s) != 0) return s->failure;
        if (!S_ISSOCK(st.st_mode))
            return pa01so_fail(s, PA01SO_VERIFY, 2, ENOTSOCK);
        size = sizeof(type);
        if (getsockopt(fd, SOL_SOCKET, SO_TYPE, &type, &size) != 0)
            return pa01so_fail(s, PA01SO_IO, 2, errno);
        if (pa01so_clock(s) != 0) return s->failure;
        if (size != sizeof(type) || type != SOCK_STREAM)
            return pa01so_fail(s, PA01SO_VERIFY, 2, EPROTOTYPE);
        size = sizeof(address);
        if (getpeername(fd, (struct sockaddr *)&address, &size) != 0)
            return pa01so_fail(s, PA01SO_IO, 2, errno);
        if (pa01so_clock(s) != 0) return s->failure;
        if (size < sizeof(sa_family_t) || size > sizeof(address)
                || address.sun_family != AF_UNIX)
            return pa01so_fail(s, PA01SO_VERIFY, 2, EAFNOSUPPORT);
        size = sizeof(peer);
        if (getsockopt(fd, SOL_SOCKET, SO_PEERCRED, &peer, &size) != 0)
            return pa01so_fail(s, PA01SO_IO, 2, errno);
        if (pa01so_clock(s) != 0) return s->failure;
        if (size != sizeof(peer) || peer.pid <= 0)
            return pa01so_fail(s, PA01SO_VERIFY, 2, EPROTO);
        out->fd = fd; out->dev = st.st_dev; out->ino = st.st_ino;
        out->pid = peer.pid; out->uid = peer.uid;
        return 0;
    }
    static int pa01so_same(PA01SOProbe *a, PA01SOProbe *b) {
        return a->fd == b->fd && a->dev == b->dev && a->ino == b->ino
            && a->pid == b->pid && a->uid == b->uid;
    }
    static uint32_t pa01so_creds(PA01SOState *s, pid_t *pid, uid_t *uid,
                                 int *fd) {
        const uint64_t need = SD_BUS_CREDS_PID|SD_BUS_CREDS_EUID|SD_BUS_CREDS_PIDFD;
        sd_bus_creds *c = NULL;
        uint64_t mask, augmented;
        int r;
        if (pa01so_clock(s) != 0) return s->failure;
        r = sd_bus_get_owner_creds(s->bus, need, &c);
        if (r < 0) { pa01so_fail(s, PA01SO_IO, 4, r); goto done; }
        if (pa01so_clock(s) != 0) goto done;
        if (c == NULL) { pa01so_fail(s, PA01SO_VERIFY, 4, EPROTO); goto done; }
        mask = sd_bus_creds_get_mask(c);
        if (pa01so_clock(s) != 0) goto done;
        augmented = sd_bus_creds_get_augmented_mask(c);
        if (pa01so_clock(s) != 0) goto done;
        if ((mask & need) != need || (augmented & need) != 0) {
            pa01so_fail(s, PA01SO_VERIFY, 4, EACCES); goto done;
        }
        r = sd_bus_creds_get_pid(c, pid);
        if (r < 0) { pa01so_fail(s, PA01SO_IO, 4, r); goto done; }
        if (pa01so_clock(s) != 0) goto done;
        r = sd_bus_creds_get_euid(c, uid);
        if (r < 0) { pa01so_fail(s, PA01SO_IO, 4, r); goto done; }
        if (pa01so_clock(s) != 0) goto done;
        r = sd_bus_creds_get_pidfd_dup(c, fd);
        /* Même sur erreur, la sortie FD reste suivie par le propriétaire. */
        if (r < 0) { pa01so_fail(s, PA01SO_IO, 4, r); goto done; }
        if (pa01so_clock(s) != 0) goto done;
    done:
        if (c != NULL) c = sd_bus_creds_unref(c);
        if (s->failure == 0) pa01so_clock(s);
        return s->failure;
    }
    static uint32_t pa01so_probe(PA01SOState *s, int initial) {
        PA01SOProbe before, after;
        pid_t pid = 0;
        uid_t uid = (uid_t)-1;
        int fresh_fd = -1;
        if (pa01so_socket(s, &before) != 0) goto done;
        if (!initial && !pa01so_same(&before, &s->peer)) {
            pa01so_fail(s, PA01SO_VERIFY, 6, ESTALE); goto done;
        }
        if (pa01so_creds(s, &pid, &uid, &fresh_fd) != 0) goto done;
        if (pid <= 0 || pid != before.pid || uid != before.uid) {
            pa01so_fail(s, PA01SO_VERIFY, 4, EPROTO); goto done;
        }
        if (pa01so_live(s, fresh_fd, 5) != 0) goto done;
        if (initial) {
            s->peer_fd = fresh_fd; fresh_fd = -1;
        } else {
            if (pa01so_close_fd(&fresh_fd, s) != 0) {
                pa01so_fail(s, PA01SO_CLEANUP, 7, s->cleanup_errno); goto done;
            }
            if (pa01so_clock(s) != 0) goto done;
        }
        if (pa01so_live(s, s->self_fd, 3) != 0) goto done;
        if (pa01so_live(s, s->peer_fd, 5) != 0) goto done;
        if (pa01so_socket(s, &after) != 0) goto done;
        if (!pa01so_same(&before, &after) || !pa01so_owner(s, 1)) {
            pa01so_fail(s, PA01SO_STATE, 6, ESTALE); goto done;
        }
        if (pa01so_clock(s) != 0) goto done;
        if (initial) s->peer = after;
    done:
        if (fresh_fd >= 0) {
            if (pa01so_close_fd(&fresh_fd, s) != 0 && s->failure == 0)
                pa01so_fail(s, PA01SO_CLEANUP, 7, s->cleanup_errno);
        }
        return s->failure;
    }
    static uint32_t pa01so_open(void **out, void *bus, uint64_t end,
                                uint32_t *stage, int *code, int *cleanup) {
        PA01SOState *s;
        uint32_t result;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (out == NULL || *out != NULL || stage == NULL || code == NULL
                || cleanup == NULL || bus == NULL || end == 0
                || bus == SD_BUS_DEFAULT || bus == SD_BUS_DEFAULT_USER
                || bus == SD_BUS_DEFAULT_SYSTEM) return PA01SO_ARG;
        s = (PA01SOState *)calloc(1, sizeof(*s));
        if (s == NULL) { *stage = 6; *code = ENOMEM; return PA01SO_MEM; }
        s->kind = PA01SO_KIND;
        s->self_fd = -1; s->peer_fd = -1; s->peer.fd = -1;
        s->pid = getpid(); s->tid = gettid();
        s->uid = getuid(); s->euid = geteuid(); s->end_ns = end;
        if (s->pid <= 0 || s->tid <= 0) {
            pa01so_fail(s, PA01SO_VERIFY, 6, EPROTO); goto failed;
        }
        if (pa01so_clock(s) != 0) goto failed;
        s->bus = sd_bus_ref((sd_bus *)bus);
        if (pa01so_clock(s) != 0) goto failed;
        if (s->bus == NULL) {
            pa01so_fail(s, PA01SO_VERIFY, 6, EPROTO); goto failed;
        }
        s->self_fd = pidfd_open(s->pid, 0);
        if (s->self_fd < 0) {
            pa01so_fail(s, PA01SO_IO, 3, errno); goto failed;
        }
        if (pa01so_clock(s) != 0) goto failed;
        if (pa01so_probe(s, 1) != 0) goto failed;
        pa01so_diag(s, stage, code, cleanup);
        *out = s;
        return 0;
    failed:
        result = s->failure;
        pa01so_dispose(s);
        pa01so_diag(s, stage, code, cleanup);
        explicit_bzero(s, sizeof(*s)); free(s);
        return result;
    }
    static uint32_t pa01so_snapshot(void *state, uint64_t *facts, size_t len,
                                    uint32_t *stage, int *code, int *cleanup) {
        PA01SOState *s = (PA01SOState *)state;
        if (facts != NULL && len == 7) memset(facts, 0, 7 * sizeof(*facts));
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (s == NULL || facts == NULL || len != 7
                || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        if (s->kind != PA01SO_KIND) {
            *stage = 6; *code = EINVAL; return PA01SO_STATE;
        }
        if (!pa01so_owner(s, 1)) {
            *stage = 6; *code = ECHILD; return PA01SO_STATE;
        }
        if (s->failure == 0) pa01so_probe(s, 0);
        pa01so_diag(s, stage, code, cleanup);
        if (s->failure != 0) return s->failure;
        facts[0] = (uint64_t)s->pid;
        facts[1] = (uint64_t)s->uid;
        facts[2] = (uint64_t)s->euid;
        facts[3] = (uint64_t)s->peer.pid;
        facts[4] = (uint64_t)s->peer.uid;
        facts[5] = s->last_ns; facts[6] = s->end_ns;
        return 0;
    }
    static uint32_t pa01so_close(void **state, uint32_t *stage,
                                 int *code, int *cleanup) {
        PA01SOState *s;
        uint32_t result;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (state == NULL || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        s = (PA01SOState *)*state;
        if (s == NULL) return 0;
        if (s->kind != PA01SO_KIND) {
            *stage = 6; *code = EINVAL; return PA01SO_STATE;
        }
        /* Après fork, aucune fonction SDK ni fermeture héritée. */
        if (!pa01so_owner(s, 0)) {
            *stage = 6; *code = ECHILD; return PA01SO_STATE;
        }
        pa01so_dispose(s);
        if (s->cleanup_errno != 0 && s->failure == 0)
            pa01so_fail(s, PA01SO_CLEANUP, 7, s->cleanup_errno);
        result = s->failure;
        pa01so_diag(s, stage, code, cleanup);
        explicit_bzero(s, sizeof(*s)); free(s); *state = NULL;
        return result;
    }
    #include <systemd/sd-id128.h>
    #define PA01SOC_KIND UINT64_C(0x5041303153430001)
    enum { PA01SOC_CONNECT=1, PA01SOC_AUTH=2, PA01SOC_READY=3 };
    typedef struct {
        uint64_t kind;
        PA01SOState guard; /* Horloge/owner/diagnostic, aucun bus emprunté. */
        int fd, phase, auth_wait;
        sd_bus *bus;       /* Référence propre créée ici seulement. */
        PA01SOProbe initial;
        void *observation; /* Fille privée, jamais exportée. */
        void *lookup; /* Bail exclusif lookup enfant, jamais exporté. */
    } PA01SOConn;

    static uint32_t pa01soc_guard(PA01SOConn *c) {
        if (c->kind != PA01SOC_KIND)
            return pa01so_fail(&c->guard, PA01SO_STATE, 6, EINVAL);
        if (!pa01so_owner(&c->guard, 1))
            return pa01so_fail(&c->guard, PA01SO_STATE, 6, ECHILD);
        return pa01so_clock(&c->guard);
    }
    static uint32_t pa01soc_result(PA01SOConn *c, uint32_t result,
                                   uint32_t *stage, int *code, int *cleanup) {
        pa01so_diag(&c->guard, stage, code, cleanup);
        return c->guard.failure != 0 ? c->guard.failure : result;
    }
    static void pa01soc_child_failure(PA01SOConn *c, uint32_t result,
                                      uint32_t stage, int code, int cleanup) {
        if (cleanup != 0 && c->guard.cleanup_errno == 0)
            c->guard.cleanup_errno = cleanup;
        if (result != 0)
            pa01so_fail(&c->guard, result, stage != 0 ? stage : 6, code);
    }
    static uint32_t pa01soc_endpoint(PA01SOConn *c, const char *path,
            size_t length, struct sockaddr_un *address, socklen_t *size) {
        size_t i, start;
        if (path == NULL || length < 2 || length >= sizeof(address->sun_path))
            return pa01so_fail(&c->guard, PA01SO_ARG, 6, EINVAL);
        if (path[0] != '/' || path[length - 1] == '/')
            return pa01so_fail(&c->guard, PA01SO_ARG, 6, EINVAL);
        start = 1;
        for (i = 0; i <= length; i++) {
            if (i < length) {
                unsigned char ch = (unsigned char)path[i];
                if (ch == 0 || ch < 32 || ch == 127)
                    return pa01so_fail(&c->guard, PA01SO_ARG, 6, EINVAL);
            }
            if (i > 0 && (i == length || path[i] == '/')) {
                size_t part = i - start;
                if (part == 0 || (part == 1 && path[start] == '.')
                        || (part == 2 && path[start] == '.' && path[start+1] == '.'))
                    return pa01so_fail(&c->guard, PA01SO_ARG, 6, EINVAL);
                start = i + 1;
            }
        }
        memset(address, 0, sizeof(*address));
        address->sun_family = AF_UNIX;
        memcpy(address->sun_path, path, length);
        address->sun_path[length] = 0;
        *size = (socklen_t)(offsetof(struct sockaddr_un, sun_path) + length + 1);
        return 0;
    }
    static uint32_t pa01soc_flags(PA01SOConn *c, int fd) {
        int r;
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        r = fcntl(fd, F_GETFD);
        if (r < 0) return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if ((r & FD_CLOEXEC) == 0)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 8, EPROTO);
        r = fcntl(fd, F_GETFL);
        if (r < 0) return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if ((r & O_NONBLOCK) == 0)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 8, EPROTO);
        return 0;
    }
    static uint32_t pa01soc_fd(PA01SOConn *c, int fd, PA01SOProbe *out,
                               int connected) {
        struct stat st;
        struct sockaddr_un peer = {0};
        struct ucred creds = {0};
        socklen_t size;
        int type = 0, error = 0;
        if (pa01soc_flags(c, fd) != 0) return c->guard.failure;
        if (fstat(fd, &st) != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (!S_ISSOCK(st.st_mode))
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 8, ENOTSOCK);
        size = sizeof(type);
        if (getsockopt(fd, SOL_SOCKET, SO_TYPE, &type, &size) != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (size != sizeof(type) || type != SOCK_STREAM)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 8, EPROTOTYPE);
        memset(out, 0, sizeof(*out));
        out->fd = fd; out->dev = st.st_dev; out->ino = st.st_ino;
        if (!connected) return 0;
        size = sizeof(error);
        if (getsockopt(fd, SOL_SOCKET, SO_ERROR, &error, &size) != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (size != sizeof(error) || error != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 8, error != 0 ? error : EPROTO);
        size = sizeof(peer);
        if (getpeername(fd, (struct sockaddr *)&peer, &size) != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (size < sizeof(sa_family_t) || size > sizeof(peer) || peer.sun_family != AF_UNIX)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 8, EAFNOSUPPORT);
        size = sizeof(creds);
        if (getsockopt(fd, SOL_SOCKET, SO_PEERCRED, &creds, &size) != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 8, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (size != sizeof(creds) || creds.pid <= 0)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 8, EPROTO);
        out->pid = creds.pid; out->uid = creds.uid;
        return 0;
    }
    static uint32_t pa01soc_peek(PA01SOConn *c) {
        PA01SOProbe p;
        int fd;
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        fd = sd_bus_get_fd(c->bus);
        if (fd < 0) return pa01so_fail(&c->guard, PA01SO_IO, 9, fd);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (pa01soc_fd(c, fd, &p, 1) != 0) return c->guard.failure;
        if (!pa01so_same(&p, &c->initial))
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 6, ESTALE);
        return 0;
    }
    static uint32_t pa01soc_setup(PA01SOConn *c) {
        const uint64_t need = SD_BUS_CREDS_PID|SD_BUS_CREDS_EUID|SD_BUS_CREDS_PIDFD;
        int r;
        #define PA01SOC_SETUP(expr) do { \
            if (pa01soc_guard(c) != 0) return c->guard.failure; \
            r = (expr); \
            if (r < 0) return pa01so_fail(&c->guard, PA01SO_IO, 9, r); \
            if (pa01soc_guard(c) != 0) return c->guard.failure; \
        } while (0)
        PA01SOC_SETUP(sd_bus_new(&c->bus));
        if (c->bus == NULL)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 9, EPROTO);
        r = sd_bus_set_fd(c->bus, c->fd, c->fd);
        if (r < 0) return pa01so_fail(&c->guard, PA01SO_IO, 9, r);
        c->fd = -1; /* Transfert réel AVANT tout contrôle ultérieur. */
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        PA01SOC_SETUP(sd_bus_set_bus_client(c->bus, 0));
        PA01SOC_SETUP(sd_bus_set_server(c->bus, 0, SD_ID128_NULL));
        PA01SOC_SETUP(sd_bus_set_anonymous(c->bus, 0));
        PA01SOC_SETUP(sd_bus_set_allow_interactive_authorization(c->bus, 0));
        PA01SOC_SETUP(sd_bus_set_exit_on_disconnect(c->bus, 0));
        PA01SOC_SETUP(sd_bus_set_close_on_exit(c->bus, 1));
        PA01SOC_SETUP(sd_bus_negotiate_fds(c->bus, 1));
        PA01SOC_SETUP(sd_bus_negotiate_creds(c->bus, 1, need));
        PA01SOC_SETUP(sd_bus_start(c->bus));
        #undef PA01SOC_SETUP
        c->phase = PA01SOC_AUTH;
        c->auth_wait = 0;
        return pa01soc_peek(c);
    }
    static uint32_t pa01soc_connected(PA01SOConn *c) {
        PA01SOProbe p;
        if (pa01soc_fd(c, c->fd, &p, 1) != 0) return c->guard.failure;
        if (p.fd != c->initial.fd || p.dev != c->initial.dev || p.ino != c->initial.ino)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 6, ESTALE);
        c->initial = p;
        return pa01soc_setup(c);
    }
    /* Aucun effacement d'une fille encore possédée. */
    static int pa01soc_cleanup(PA01SOConn *c) {
        uint32_t stage = 0, status;
        int code = 0, cleanup = 0;
        if (!pa01so_owner(&c->guard, 0)) return 0;
        if (c->observation != NULL) {
            status = pa01so_close(&c->observation, &stage, &code, &cleanup);
            pa01soc_child_failure(c, status, stage, code, cleanup);
            if (c->observation != NULL) return 0;
        }
        /* Ce bus est le nôtre, pas celui reçu par pa01_sysd_open. */
        if (c->bus != NULL) c->bus = sd_bus_close_unref(c->bus);
        if (pa01so_close_fd(&c->fd, &c->guard) != 0 && c->guard.failure == 0)
            pa01so_fail(&c->guard, PA01SO_CLEANUP, 7, c->guard.cleanup_errno);
        return 1;
    }
    static uint32_t pa01so_conn_start(void **out, const char *path, size_t length,
            uint64_t end, uint32_t *stage, int *code, int *cleanup) {
        PA01SOConn *c;
        struct sockaddr_un address;
        socklen_t size = 0;
        uint32_t result;
        int r, saved;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (out == NULL || *out != NULL || path == NULL || end == 0
                || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        c = (PA01SOConn *)calloc(1, sizeof(*c));
        if (c == NULL) { *stage = 6; *code = ENOMEM; return PA01SO_MEM; }
        c->kind = PA01SOC_KIND;
        c->fd = -1; c->guard.self_fd = -1; c->guard.peer_fd = -1;
        c->guard.pid = getpid(); c->guard.tid = gettid();
        c->guard.uid = getuid(); c->guard.euid = geteuid();
        c->guard.end_ns = end; c->phase = PA01SOC_CONNECT;
        if (c->guard.pid <= 0 || c->guard.tid <= 0) {
            pa01so_fail(&c->guard, PA01SO_VERIFY, 6, EPROTO); goto failed;
        }
        if (pa01soc_guard(c) != 0) goto failed;
        if (pa01soc_endpoint(c, path, length, &address, &size) != 0) goto failed;
        if (pa01soc_guard(c) != 0) goto failed;
        c->fd = socket(AF_UNIX, SOCK_STREAM|SOCK_NONBLOCK|SOCK_CLOEXEC, 0);
        if (c->fd < 0) { pa01so_fail(&c->guard, PA01SO_IO, 8, errno); goto failed; }
        if (pa01soc_guard(c) != 0) goto failed;
        if (pa01soc_fd(c, c->fd, &c->initial, 0) != 0) goto failed;
        r = connect(c->fd, (struct sockaddr *)&address, size);
        saved = errno;
        if (r < 0 && saved != EINPROGRESS) {
            pa01so_fail(&c->guard, PA01SO_IO, 8, saved); goto failed;
        }
        if (pa01soc_guard(c) != 0) goto failed;
        if (r == 0 && pa01soc_connected(c) != 0) goto failed;
        pa01so_diag(&c->guard, stage, code, cleanup);
        *out = c;
        return 5;
    failed:
        if (!pa01soc_cleanup(c)) {
            if (c->guard.failure == 0)
                pa01so_fail(&c->guard, PA01SO_STATE, 6, ECHILD);
            pa01so_diag(&c->guard, stage, code, cleanup);
            *out = c;
            return c->guard.failure;
        }
        result = c->guard.failure;
        pa01so_diag(&c->guard, stage, code, cleanup);
        explicit_bzero(c, sizeof(*c)); free(c);
        return result;
    }
    static uint32_t pa01soc_ready_facts(PA01SOConn *c, uint64_t values[7]) {
        uint32_t stage = 0, result;
        int code = 0, cleanup = 0;
        if (c->observation == NULL)
            return pa01so_fail(&c->guard, PA01SO_STATE, 6, ESTALE);
        if (pa01soc_peek(c) != 0) return c->guard.failure;
        result = pa01so_snapshot(c->observation, values, 7, &stage, &code, &cleanup);
        pa01soc_child_failure(c, result, stage, code, cleanup);
        if (c->guard.failure != 0) return c->guard.failure;
        return pa01soc_guard(c);
    }
    static uint32_t pa01soc_collect(PA01SOConn *c) {
        uint32_t stage = 0, result;
        int code = 0, cleanup = 0;
        uint64_t values[7];
        if (pa01soc_peek(c) != 0) return c->guard.failure;
        result = pa01so_open(&c->observation, c->bus, c->guard.end_ns,
                             &stage, &code, &cleanup);
        pa01soc_child_failure(c, result, stage, code, cleanup);
        if (c->guard.failure != 0) return c->guard.failure;
        if (pa01soc_ready_facts(c, values) != 0) return c->guard.failure;
        c->phase = PA01SOC_READY;
        return 0;
    }
    static uint32_t pa01soc_can_process(PA01SOConn *c, int *ready) {
        uint64_t usec = UINT64_MAX, due = UINT64_MAX;
        struct pollfd p = {0};
        int events, r;
        *ready = 0;
        if (pa01soc_peek(c) != 0) return c->guard.failure;
        events = sd_bus_get_events(c->bus);
        if (events < 0) return pa01so_fail(&c->guard, PA01SO_IO, 10, events);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if ((events & ~(POLLIN|POLLOUT)) != 0)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 10, EPROTO);
        r = sd_bus_get_timeout(c->bus, &usec);
        if (r < 0) return pa01so_fail(&c->guard, PA01SO_IO, 10, r);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (usec != UINT64_MAX) {
            if (usec > UINT64_MAX / UINT64_C(1000))
                return pa01so_fail(&c->guard, PA01SO_VERIFY, 10, EOVERFLOW);
            due = usec * UINT64_C(1000);
        }
        if (due > c->guard.end_ns) due = c->guard.end_ns;
        /* Un timer SDK échu peut avancer le SDK tant que le budget PA est ouvert. */
        if (due <= c->guard.last_ns) { *ready = 1; return 0; }
        p.fd = c->initial.fd; p.events = (short)events;
        r = poll(&p, 1, 0);
        if (r < 0) return pa01so_fail(&c->guard, PA01SO_IO, 10, errno);
        if (pa01soc_guard(c) != 0) return c->guard.failure;
        if (r > 0 && (p.revents & (POLLERR|POLLHUP|POLLNVAL)) != 0)
            return pa01so_fail(&c->guard, PA01SO_IO, 10, ECONNRESET);
        if (r > 0 && (p.revents & ~(POLLIN|POLLOUT)) != 0)
            return pa01so_fail(&c->guard, PA01SO_VERIFY, 10, EPROTO);
        *ready = r > 0;
        return 0;
    }
    static uint32_t pa01so_conn_step(void *state, uint32_t *stage,
                                     int *code, int *cleanup) {
        PA01SOConn *c = state;
        struct pollfd p = {0};
        uint64_t values[7];
        uint32_t result = 5;
        int r, ready = 0;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (c == NULL || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        if (c->kind != PA01SOC_KIND) {
            *stage = 6; *code = EINVAL; return PA01SO_STATE;
        }
        if (!pa01so_owner(&c->guard, 1)) {
            *stage = 6; *code = ECHILD; return PA01SO_STATE;
        }
        if (c->lookup != NULL) {
            *stage = 6; *code = EBUSY; return PA01SO_STATE;
        }
        if (pa01soc_guard(c) != 0) goto done;
        if (c->phase == PA01SOC_READY) {
            result = pa01soc_ready_facts(c, values); goto done;
        }
        if (c->phase == PA01SOC_CONNECT) {
            if (c->fd < 0 || c->bus != NULL) {
                pa01so_fail(&c->guard, PA01SO_STATE, 6, ESTALE); goto done;
            }
            p.fd = c->fd; p.events = POLLOUT;
            r = poll(&p, 1, 0);
            if (r < 0) { pa01so_fail(&c->guard, PA01SO_IO, 8, errno); goto done; }
            if (pa01soc_guard(c) != 0) goto done;
            if (r == 0) goto done;
            if ((p.revents & POLLOUT) == 0
                    || (p.revents & (POLLERR|POLLHUP|POLLNVAL)) != 0) {
                pa01so_fail(&c->guard, PA01SO_IO, 8, ECONNREFUSED); goto done;
            }
            if (pa01soc_connected(c) != 0) goto done;
            /* Un seul changement de phase ; pas de process caché ici. */
            goto done;
        }
        if (c->phase != PA01SOC_AUTH || c->bus == NULL) {
            pa01so_fail(&c->guard, PA01SO_STATE, 6, ESTALE); goto done;
        }
        r = sd_bus_is_ready(c->bus);
        if (r < 0) { pa01so_fail(&c->guard, PA01SO_IO, 10, r); goto done; }
        if (pa01soc_guard(c) != 0) goto done;
        if (r == 1) { result = pa01soc_collect(c); goto done; }
        if (r != 0) {
            pa01so_fail(&c->guard, PA01SO_VERIFY, 10, EPROTO); goto done;
        }
        if (pa01soc_peek(c) != 0) goto done;
        if (c->auth_wait) {
            if (pa01soc_can_process(c, &ready) != 0) goto done;
            if (!ready) goto done;
        }
        r = sd_bus_process(c->bus, NULL); /* Au plus un appel par step. */
        if (r < 0) { pa01so_fail(&c->guard, PA01SO_IO, 10, r); goto done; }
        c->auth_wait = r == 0;
        if (pa01soc_guard(c) != 0) goto done;
        if (pa01soc_peek(c) != 0) goto done;
        r = sd_bus_is_ready(c->bus);
        if (r < 0) { pa01so_fail(&c->guard, PA01SO_IO, 10, r); goto done; }
        if (pa01soc_guard(c) != 0) goto done;
        if (r == 1) result = pa01soc_collect(c);
        else if (r != 0) pa01so_fail(&c->guard, PA01SO_VERIFY, 10, EPROTO);
    done:
        return pa01soc_result(c, result, stage, code, cleanup);
    }
    static uint32_t pa01so_conn_snapshot(void *state, uint64_t *facts, size_t len,
            uint32_t *stage, int *code, int *cleanup) {
        PA01SOConn *c = state;
        uint64_t values[7] = {0};
        uint32_t result;
        if (facts != NULL && len == 7) memset(facts, 0, sizeof(values));
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (c == NULL || facts == NULL || len != 7
                || stage == NULL || code == NULL || cleanup == NULL) return PA01SO_ARG;
        if (c->kind != PA01SOC_KIND) {
            *stage = 6; *code = EINVAL; return PA01SO_STATE;
        }
        if (!pa01so_owner(&c->guard, 1)) {
            *stage = 6; *code = ECHILD; return PA01SO_STATE;
        }
        if (c->lookup != NULL) {
            *stage = 6; *code = EBUSY; return PA01SO_STATE;
        }
        if (pa01soc_guard(c) != 0)
            return pa01soc_result(c, c->guard.failure, stage, code, cleanup);
        if (c->phase != PA01SOC_READY)
            return pa01soc_result(c, PA01SO_STATE, stage, code, cleanup);
        result = pa01soc_ready_facts(c, values);
        if (result == 0) memcpy(facts, values, sizeof(values));
        return pa01soc_result(c, result, stage, code, cleanup);
    }
    static uint32_t pa01so_conn_close(void **state, uint32_t *stage,
                                      int *code, int *cleanup) {
        PA01SOConn *c;
        uint32_t result;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (state == NULL || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        c = *state;
        if (c == NULL) return 0;
        if (c->kind != PA01SOC_KIND) {
            *stage = 6; *code = EINVAL; return PA01SO_STATE;
        }
        if (!pa01so_owner(&c->guard, 0)) {
            *stage = 6; *code = ECHILD; return PA01SO_STATE;
        }
        if (c->lookup != NULL) {
            *stage = 6; *code = EBUSY; return PA01SO_STATE;
        }
        if (!pa01soc_cleanup(c)) {
            if (c->guard.failure == 0)
                pa01so_fail(&c->guard, PA01SO_STATE, 7, EBUSY);
            return pa01soc_result(c, c->guard.failure, stage, code, cleanup);
        }
        result = c->guard.failure;
        pa01so_diag(&c->guard, stage, code, cleanup);
        explicit_bzero(c, sizeof(*c)); free(c); *state = NULL;
        return result;
    }
    #define PA01SOL_KIND UINT64_C(0x50413031534C0001)
    enum { PA01SOL_CALL=1, PA01SOL_SETUP=2, PA01SOL_DONE=3 };
    typedef struct {
        uint64_t kind;
        PA01SOConn *parent;
        void *mpid;
        int pidfd, ns_self, ns_peer;
        sd_bus_slot *slot;
        sd_bus_message *reply;
        char *path; size_t max_path; size_t path_len;
        char *unit; size_t max_unit; size_t unit_len;
        uint8_t invoc[16]; int has_invoc;
        uint64_t observed_ns;
        int phase, replied;
        uint32_t failure, stage;
        int native_code, cleanup_errno;
        dev_t init_ns_dev; ino_t init_ns_ino; int has_init_ns;
    } PA01SOLookup;
    static uint32_t pa01sol_fail(PA01SOLookup *u, uint32_t status,
                                 uint32_t stage, int code) {
        if (u->failure == 0) {
            u->failure = status;
            u->stage = stage;
            u->native_code = code;
        }
        return u->failure;
    }
    static void pa01sol_diag(PA01SOLookup *u, uint32_t *stage,
                             int *code, int *cleanup) {
        *stage = u->stage;
        *code = u->native_code;
        *cleanup = u->cleanup_errno;
    }
    static int pa01sol_close_fd(int *fd, PA01SOLookup *u) {
        int owned = *fd, saved;
        *fd = -1;
        if (owned < 0) return 0;
        if (close(owned) == 0) return 0;
        saved = errno;
        if (u->cleanup_errno == 0) u->cleanup_errno = saved;
        return -1;
    }
    static void pa01sol_dispose(PA01SOLookup *u) {
        if (u->slot != NULL) u->slot = sd_bus_slot_unref(u->slot);
        if (u->reply != NULL) u->reply = sd_bus_message_unref(u->reply);
        pa01sol_close_fd(&u->pidfd, u);
        pa01sol_close_fd(&u->ns_self, u);
        pa01sol_close_fd(&u->ns_peer, u);
        if (u->path != NULL) {
            explicit_bzero(u->path, u->max_path + 1);
            free(u->path); u->path = NULL;
        }
        if (u->unit != NULL) {
            explicit_bzero(u->unit, u->max_unit + 1);
            free(u->unit); u->unit = NULL;
        }
    }
static uint32_t pa01sol_ns_from_pidfds(PA01SOLookup *u, int self_fd,
                                       int peer_fd, int set_init) {
    int ns_s = -1, ns_p = -1, e = 0, r = 0, t = 0;
    struct stat a, b;
#if !defined(PIDFD_GET_PID_NAMESPACE) || !defined(NS_GET_NSTYPE) || !defined(CLONE_NEWPID)
    return pa01sol_fail(u, PA01SO_VERIFY, 6, ENOTSUP);
#else
    if (u == NULL || u->kind != PA01SOL_KIND)
        return PA01SO_STATE;
    if (u->parent == NULL || u->parent->kind != PA01SOC_KIND
            || u->parent->lookup != u)
        return PA01SO_STATE;
    if (!pa01so_owner(&u->parent->guard, 1))
        return PA01SO_STATE;
    if (self_fd < 0 || peer_fd < 0)
        return pa01sol_fail(u, PA01SO_STATE, 6, ESTALE);
    if (pa01soc_guard(u->parent) != 0)
        return pa01sol_fail(u, u->parent->guard.failure,
                            u->parent->guard.stage,
                            u->parent->guard.native_code);
    ns_s = ioctl(self_fd, PIDFD_GET_PID_NAMESPACE, 0);
    if (ns_s < 0) {
        e = errno;
        if (e == ENOTTY || e == ENOSYS || e == EOPNOTSUPP)
            return pa01sol_fail(u, PA01SO_VERIFY, 6, ENOTSUP);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    r = fcntl(ns_s, F_GETFD);
    if (r < 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    if ((r & FD_CLOEXEC) == 0) {
        pa01sol_close_fd(&ns_s, u);
        return pa01sol_fail(u, PA01SO_VERIFY, 6, EPROTO);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    ns_p = ioctl(peer_fd, PIDFD_GET_PID_NAMESPACE, 0);
    if (ns_p < 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        if (e == ENOTTY || e == ENOSYS || e == EOPNOTSUPP)
            return pa01sol_fail(u, PA01SO_VERIFY, 6, ENOTSUP);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    r = fcntl(ns_p, F_GETFD);
    if (r < 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    if ((r & FD_CLOEXEC) == 0) {
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_VERIFY, 6, EPROTO);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    t = ioctl(ns_s, NS_GET_NSTYPE, 0);
    if (t < 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        if (e == ENOTTY || e == ENOSYS || e == EOPNOTSUPP)
            return pa01sol_fail(u, PA01SO_VERIFY, 6, ENOTSUP);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (t != CLONE_NEWPID) {
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_VERIFY, 6, EPROTO);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    t = ioctl(ns_p, NS_GET_NSTYPE, 0);
    if (t < 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        if (e == ENOTTY || e == ENOSYS || e == EOPNOTSUPP)
            return pa01sol_fail(u, PA01SO_VERIFY, 6, ENOTSUP);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (t != CLONE_NEWPID) {
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_VERIFY, 6, EPROTO);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    if (fstat(ns_s, &a) != 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    if (fstat(ns_p, &b) != 0) {
        e = errno;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_IO, 6, e);
    }
    if (pa01soc_guard(u->parent) != 0) {
        e = u->parent->guard.native_code;
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, u->parent->guard.failure, 6, e);
    }
    if (a.st_dev != b.st_dev || a.st_ino != b.st_ino) {
        pa01sol_close_fd(&ns_s, u);
        pa01sol_close_fd(&ns_p, u);
        return pa01sol_fail(u, PA01SO_VERIFY, 6, ESTALE);
    }
    if (set_init && !u->has_init_ns) {
        u->init_ns_dev = a.st_dev;
        u->init_ns_ino = a.st_ino;
        u->has_init_ns = 1;
    } else if (u->has_init_ns) {
        if (a.st_dev != u->init_ns_dev || a.st_ino != u->init_ns_ino) {
            pa01sol_close_fd(&ns_s, u);
            pa01sol_close_fd(&ns_p, u);
            return pa01sol_fail(u, PA01SO_VERIFY, 6, ESTALE);
        }
    }
    pa01sol_close_fd(&u->ns_self, u);
    pa01sol_close_fd(&u->ns_peer, u);
    u->ns_self = ns_s; u->ns_peer = ns_p;
    if (pa01soc_guard(u->parent) != 0)
        return pa01sol_fail(u, u->parent->guard.failure, 6,
                            u->parent->guard.native_code);
    if (u->failure == 0 && u->cleanup_errno != 0)
        return pa01sol_fail(u, PA01SO_CLEANUP, 7, u->cleanup_errno);
    return 0;
#endif
}
static uint32_t pa01sol_recheck(PA01SOLookup *u) {
    PA01SOConn *c;
    PA01SOState *obs;
    uint64_t facts[7];
    int r;
    struct pollfd p = {0};
    if (u == NULL) return PA01SO_ARG;
    if (u->kind != PA01SOL_KIND)
        return PA01SO_STATE;
    c = u->parent;
    if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u)
        return PA01SO_STATE;
    if (!pa01so_owner(&c->guard, 1))
        return PA01SO_STATE;
    obs = (PA01SOState *)c->observation;
    if (obs == NULL || obs->kind != PA01SO_KIND)
        return PA01SO_STATE;
    if (c->phase != PA01SOC_READY || c->bus == NULL)
        return PA01SO_STATE;
    if (u->pidfd < 0 || obs->peer_fd < 0)
        return pa01sol_fail(u, PA01SO_STATE, 6, ESTALE);
    if (pa01soc_guard(c) != 0)
        return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                            c->guard.native_code);
    r = (int)pa01soc_ready_facts(c, facts);
    if (r != 0) {
        if (c->guard.failure != 0)
            return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                                c->guard.native_code);
        return pa01sol_fail(u, PA01SO_STATE, 6, EPROTO);
    }
    if (pa01soc_guard(c) != 0)
        return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                            c->guard.native_code);
    r = fcntl(u->pidfd, F_GETFD);
    if (r < 0)
        return pa01sol_fail(u, PA01SO_IO, 10, errno);
    if (pa01soc_guard(c) != 0)
        return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                            c->guard.native_code);
    if ((r & FD_CLOEXEC) == 0)
        return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
    p.fd = u->pidfd; p.events = POLLIN;
    if (pa01soc_guard(c) != 0)
        return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                            c->guard.native_code);
    r = poll(&p, 1, 0);
    if (r < 0)
        return pa01sol_fail(u, PA01SO_IO, 10, errno);
    if (pa01soc_guard(c) != 0)
        return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                            c->guard.native_code);
    if (r != 0)
        return pa01sol_fail(u, PA01SO_VERIFY, 10, ESRCH);
    {
        uint32_t nr = pa01sol_ns_from_pidfds(u, u->pidfd, obs->peer_fd, 0);
        if (nr != 0) return nr;
    }
    if (pa01soc_guard(c) != 0)
        return pa01sol_fail(u, c->guard.failure, c->guard.stage,
                            c->guard.native_code);
    if (u->failure == 0 && u->cleanup_errno != 0)
        return pa01sol_fail(u, PA01SO_CLEANUP, 7, u->cleanup_errno);
    return 0;
}
    static int pa01sol_on_reply(sd_bus_message *m, void *userdata,
                                sd_bus_error *ret_error) {
        PA01SOLookup *u = (PA01SOLookup *)userdata;
        (void)ret_error;
        if (u == NULL || u->kind != PA01SOL_KIND) return 0;
        if (u->parent == NULL || u->parent->lookup != u) return 0;
        if (m == NULL) {
            pa01sol_fail(u, PA01SO_IO, 10, ECONNRESET);
            return 0;
        }
        if (u->reply != NULL) {
            pa01sol_fail(u, PA01SO_STATE, 10, EPROTO);
            return 0;
        }
        u->reply = sd_bus_message_ref(m);
        if (u->reply == NULL) {
            pa01sol_fail(u, PA01SO_MEM, 10, ENOMEM);
            return 0;
        }
        u->replied = 1;
        return 0;
    }
    static uint32_t pa01sol_parse_held(PA01SOLookup *u) {
        sd_bus_message *m;
        const char *pp = NULL, *pu = NULL;
        const void *pv = NULL;
        size_t vz = 0;
        uint8_t tp = 0;
        int r;
        static const uint8_t zero16[16] = {0};
        static const char prefix[] = "/org/freedesktop/systemd1/unit/";
        size_t lp, lu, i;
        if (u == NULL || u->kind != PA01SOL_KIND)
            return PA01SO_STATE;
        m = u->reply;
        if (m == NULL)
            return pa01sol_fail(u, PA01SO_STATE, 10, ESTALE);
        r = sd_bus_message_get_type(m, &tp);
        if (r < 0)
            return pa01sol_fail(u, PA01SO_IO, 10, r);
        if (tp != SD_BUS_MESSAGE_METHOD_RETURN)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        r = sd_bus_message_has_signature(m, "osay");
        if (r < 0)
            return pa01sol_fail(u, PA01SO_IO, 10, r);
        if (r == 0)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        r = sd_bus_message_read(m, "os", &pp, &pu);
        if (r < 0)
            return pa01sol_fail(u, PA01SO_IO, 10, r);
        if (r == 0 || pp == NULL || pu == NULL)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        r = sd_bus_message_read_array(m, 'y', &pv, &vz);
        if (r < 0)
            return pa01sol_fail(u, PA01SO_IO, 10, r);
        if (r == 0 || pv == NULL || vz != 16)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        r = sd_bus_message_at_end(m, 1);
        if (r < 0)
            return pa01sol_fail(u, PA01SO_IO, 10, r);
        if (r != 1)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        if (u->max_path == 0 || u->max_unit == 0
                || u->max_path == SIZE_MAX || u->max_unit == SIZE_MAX)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        lp = strnlen(pp, u->max_path + 1);
        lu = strnlen(pu, u->max_unit + 1);
        if (lp == 0 || lp > u->max_path || lu == 0 || lu > u->max_unit)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        if (pp[lp] != 0 || pu[lu] != 0)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        if (lp < sizeof(prefix) || memcmp(pp, prefix, sizeof(prefix) - 1) != 0)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        if (strchr(pp + sizeof(prefix) - 1, '/') != NULL)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        for (i = 0; i < lu; i++) {
            unsigned char ch = (unsigned char)pu[i];
            if (ch < 32 || ch == 127 || ch == '/')
                return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        }
        if (memcmp(pv, zero16, 16) == 0)
            return pa01sol_fail(u, PA01SO_VERIFY, 10, EPROTO);
        if (u->path == NULL || u->unit == NULL)
            return pa01sol_fail(u, PA01SO_STATE, 10, ESTALE);
        memcpy(u->path, pp, lp + 1);
        u->path_len = lp;
        memcpy(u->unit, pu, lu + 1);
        u->unit_len = lu;
        memcpy(u->invoc, pv, 16);
        u->has_invoc = 1;
        return 0;
    }
    static uint32_t pa01sol_owned_err(PA01SOLookup *u, uint32_t result,
                                      uint32_t *stage, int *code, int *cleanup) {
        PA01SOConn *c;
        if (u == NULL || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        if (u->kind != PA01SOL_KIND)
            { *stage = 6; *code = EINVAL; return PA01SO_STATE; }
        c = u->parent;
        if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u)
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (!pa01so_owner(&c->guard, 1))
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (pa01soc_guard(c) != 0) {
            if (u->failure == 0) {
                u->failure = c->guard.failure;
                u->stage = c->guard.stage;
                u->native_code = c->guard.native_code;
            }
        }
        if (result != 0 && result != 5 && u->failure == 0)
            pa01sol_fail(u, result, 6, EPROTO);
        if (u->failure == 0 && c->guard.failure != 0) {
            u->failure = c->guard.failure;
            u->stage = c->guard.stage;
            u->native_code = c->guard.native_code;
        }
        if (u->failure == 0 && u->cleanup_errno != 0)
            pa01sol_fail(u, PA01SO_CLEANUP, 7, u->cleanup_errno);
        if (u->failure != 0 || (result != 0 && result != 5)) {
            if (u->slot != NULL) u->slot = sd_bus_slot_unref(u->slot);
            if (u->reply != NULL) u->reply = sd_bus_message_unref(u->reply);
            pa01sol_diag(u, stage, code, cleanup);
            if (u->failure != 0) return u->failure;
            return result;
        }
        if (pa01soc_guard(c) != 0) {
            if (u->failure == 0) {
                u->failure = c->guard.failure;
                u->stage = c->guard.stage;
                u->native_code = c->guard.native_code;
            }
            if (u->slot != NULL) u->slot = sd_bus_slot_unref(u->slot);
            if (u->reply != NULL) u->reply = sd_bus_message_unref(u->reply);
            pa01sol_diag(u, stage, code, cleanup);
            return u->failure;
        }
        pa01sol_diag(u, stage, code, cleanup);
        return result;
    }
    static uint32_t pa01so_lookup_start(void **out, void *conn,
            size_t max_path, size_t max_unit,
            uint32_t *stage, int *code, int *cleanup) {
        PA01SOConn *c = (PA01SOConn *)conn;
        PA01SOLookup *u = NULL;
        uint64_t facts[7];
        int r;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (out == NULL || *out != NULL || c == NULL
                || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        if (max_path == 0 || max_unit == 0
                || max_path == SIZE_MAX || max_unit == SIZE_MAX)
            return PA01SO_ARG;
        if (c->kind != PA01SOC_KIND)
            { *stage = 6; *code = EINVAL; return PA01SO_STATE; }
        if (c->lookup != NULL)
            { *stage = 6; *code = EBUSY; return PA01SO_STATE; }
        if (!pa01so_owner(&c->guard, 1))
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (c->phase != PA01SOC_READY || c->bus == NULL
                || c->observation == NULL)
            { *stage = 6; *code = ESTALE; return PA01SO_STATE; }
        if (pa01soc_guard(c) != 0) {
            *stage = c->guard.stage;
            *code = c->guard.native_code;
            *cleanup = c->guard.cleanup_errno;
            return c->guard.failure;
        }
        r = (int)pa01soc_ready_facts(c, facts);
        if (r != 0) {
            if (c->guard.failure != 0) {
                *stage = c->guard.stage;
                *code = c->guard.native_code;
                *cleanup = c->guard.cleanup_errno;
                return c->guard.failure;
            }
            *stage = 6; *code = EPROTO; return (uint32_t)r;
        }
        u = (PA01SOLookup *)calloc(1, sizeof(*u));
        if (u == NULL) { *stage = 6; *code = ENOMEM; return PA01SO_MEM; }
        u->kind = PA01SOL_KIND;
        u->parent = c;
        u->pidfd = -1; u->ns_self = -1; u->ns_peer = -1;
        u->max_path = max_path; u->max_unit = max_unit;
        u->phase = PA01SOL_SETUP;
        u->has_init_ns = 0;
        u->path = (char *)calloc(u->max_path + 1, 1);
        u->unit = (char *)calloc(u->max_unit + 1, 1);
        if (u->path == NULL || u->unit == NULL) {
            if (u->path != NULL) { free(u->path); u->path = NULL; }
            if (u->unit != NULL) { free(u->unit); u->unit = NULL; }
            explicit_bzero(u, sizeof(*u)); free(u);
            *stage = 6; *code = ENOMEM; return PA01SO_MEM;
        }
        if (pa01soc_guard(c) != 0) {
            uint32_t pr = c->guard.failure;
            uint32_t ps = c->guard.stage;
            int pc = c->guard.native_code, pcl = c->guard.cleanup_errno;
            if (u->path != NULL) {
                explicit_bzero(u->path, u->max_path + 1);
                free(u->path);
            }
            if (u->unit != NULL) {
                explicit_bzero(u->unit, u->max_unit + 1);
                free(u->unit);
            }
            explicit_bzero(u, sizeof(*u)); free(u);
            *stage = ps; *code = pc; *cleanup = pcl;
            return pr;
        }
        c->lookup = u;
        *out = u;
        pa01sol_diag(u, stage, code, cleanup);
        return 5;
    }
    static uint32_t pa01so_lookup_step(void *state, uint32_t *stage,
                                       int *code, int *cleanup) {
        PA01SOLookup *u = (PA01SOLookup *)state;
        PA01SOConn *c;
        PA01SOState *obs;
        int r;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (u == NULL || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        if (u->kind != PA01SOL_KIND)
            { *stage = 6; *code = EINVAL; return PA01SO_STATE; }
        c = u->parent;
        if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u)
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (!pa01so_owner(&c->guard, 1))
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (u->mpid != NULL)
            { *stage = 6; *code = EBUSY; return PA01SO_STATE; }
        obs = (PA01SOState *)c->observation;
        if (obs == NULL || obs->kind != PA01SO_KIND)
            { *stage = 6; *code = ESTALE; return PA01SO_STATE; }
        if (c->phase != PA01SOC_READY || c->bus == NULL)
            { *stage = 6; *code = ESTALE; return PA01SO_STATE; }
        if (u->failure != 0)
            return pa01sol_owned_err(u, u->failure, stage, code, cleanup);
        if (pa01soc_guard(c) != 0)
            return pa01sol_owned_err(u, c->guard.failure, stage, code, cleanup);
        if (u->phase == PA01SOL_DONE) {
            r = (int)pa01sol_recheck(u);
            if (r != 0)
                return pa01sol_owned_err(u, (uint32_t)r, stage, code, cleanup);
            return pa01sol_owned_err(u, 0, stage, code, cleanup);
        }
        if (u->phase == PA01SOL_SETUP) {
            sd_bus_message *m = NULL;
            uint64_t end, last, uu;
            int pfd = -1, fr;
            struct pollfd pl = {0};
            if (!u->has_init_ns && (u->pidfd != -1 || u->slot != NULL
                    || u->reply != NULL))
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_STATE, 8,
                                                         ESTALE),
                                         stage, code, cleanup);
            pfd = pidfd_open(c->guard.pid, 0);
            if (pfd < 0)
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 8,
                                                         errno),
                                         stage, code, cleanup);
            if (pa01soc_guard(c) != 0) {
                pa01sol_close_fd(&pfd, u);
                return pa01sol_owned_err(u, c->guard.failure != 0
                                         ? c->guard.failure : PA01SO_STATE,
                                         stage, code, cleanup);
            }
            u->pidfd = pfd;
            fr = fcntl(u->pidfd, F_GETFD);
            if (fr < 0) {
                int fe = errno;
                u->pidfd = -1;
                pa01sol_close_fd(&pfd, u);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 8, fe),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0)
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            if ((fr & FD_CLOEXEC) == 0) {
                u->pidfd = -1;
                pa01sol_close_fd(&pfd, u);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_VERIFY, 8,
                                                         EPROTO),
                                         stage, code, cleanup);
            }
            pl.fd = u->pidfd; pl.events = POLLIN;
            r = poll(&pl, 1, 0);
            if (r < 0) {
                int pe = errno;
                u->pidfd = -1;
                pa01sol_close_fd(&pfd, u);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 8, pe),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0)
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            if (r != 0) {
                u->pidfd = -1;
                pa01sol_close_fd(&pfd, u);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_VERIFY, 8,
                                                         ESRCH),
                                         stage, code, cleanup);
            }
            r = (int)pa01sol_ns_from_pidfds(u, u->pidfd, obs->peer_fd, 1);
            if (r != 0)
                return pa01sol_owned_err(u, (uint32_t)r, stage, code, cleanup);
            if (!u->has_init_ns)
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_STATE, 8,
                                                         ESTALE),
                                         stage, code, cleanup);
            r = sd_bus_message_new_method_call(c->bus, &m, NULL,
                "/org/freedesktop/systemd1",
                "org.freedesktop.systemd1.Manager",
                "GetUnitByPIDFD");
            if (r < 0 || m == NULL) {
                int e = r < 0 ? r : EPROTO;
                if (m != NULL) m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, e),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0) {
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            }
            r = sd_bus_message_set_auto_start(m, 0);
            if (r < 0) {
                int e = r;
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, e),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0) {
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            }
            r = sd_bus_message_set_allow_interactive_authorization(m, 0);
            if (r < 0) {
                int e = r;
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, e),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0) {
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            }
            r = sd_bus_message_append(m, "h", u->pidfd);
            if (r < 0) {
                int e = r;
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, e),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0) {
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            }
            end = c->guard.end_ns; last = c->guard.last_ns;
            if (end <= last) {
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_EXPIRED, 10,
                                                         ETIMEDOUT),
                                         stage, code, cleanup);
            }
            uu = (end - last) / UINT64_C(1000);
            if (uu == 0) {
                m = sd_bus_message_unref(m);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_EXPIRED, 10,
                                                         ETIMEDOUT),
                                         stage, code, cleanup);
            }
            r = sd_bus_call_async(c->bus, &u->slot, m,
                                  pa01sol_on_reply, u, uu);
            m = sd_bus_message_unref(m);
            if (r < 0 || u->slot == NULL) {
                int e = r < 0 ? r : EPROTO;
                if (u->slot != NULL) u->slot = sd_bus_slot_unref(u->slot);
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, e),
                                         stage, code, cleanup);
            }
            r = sd_bus_slot_set_floating(u->slot, 0);
            if (r < 0) {
                return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, r),
                                         stage, code, cleanup);
            }
            if (pa01soc_guard(c) != 0)
                return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                         cleanup);
            u->phase = PA01SOL_CALL;
            pa01sol_diag(u, stage, code, cleanup);
            return 5;
        }
        if (u->phase != PA01SOL_CALL || u->slot == NULL)
            return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_STATE, 10,
                                                     ESTALE),
                                     stage, code, cleanup);
        r = (int)pa01sol_recheck(u);
        if (r != 0)
            return pa01sol_owned_err(u, (uint32_t)r, stage, code, cleanup);
        {
            int rd = 0;
            uint32_t cr = pa01soc_can_process(c, &rd);
            if (cr != 0)
                return pa01sol_owned_err(u, cr, stage, code, cleanup);
            if (!rd)
                return pa01sol_owned_err(u, 5, stage, code, cleanup);
        }
        r = sd_bus_process(c->bus, NULL);
        if (u->failure != 0)
            return pa01sol_owned_err(u, u->failure, stage, code, cleanup);
        if (r < 0)
            return pa01sol_owned_err(u, pa01sol_fail(u, PA01SO_IO, 10, r),
                                     stage, code, cleanup);
        r = (int)pa01sol_recheck(u);
        if (r != 0)
            return pa01sol_owned_err(u, (uint32_t)r, stage, code, cleanup);
        if (!u->replied || u->reply == NULL)
            return pa01sol_owned_err(u, 5, stage, code, cleanup);
        r = (int)pa01sol_parse_held(u);
        if (r != 0)
            return pa01sol_owned_err(u, (uint32_t)r, stage, code, cleanup);
        r = (int)pa01sol_recheck(u);
        if (r != 0)
            return pa01sol_owned_err(u, (uint32_t)r, stage, code, cleanup);
        if (pa01soc_guard(c) != 0)
            return pa01sol_owned_err(u, c->guard.failure, stage, code,
                                     cleanup);
        u->observed_ns = c->guard.last_ns;
        u->phase = PA01SOL_DONE;
        if (u->slot != NULL) u->slot = sd_bus_slot_unref(u->slot);
        if (u->reply != NULL) u->reply = sd_bus_message_unref(u->reply);
        return pa01sol_owned_err(u, 0, stage, code, cleanup);
    }
    static uint32_t pa01so_lookup_snapshot(void *state, char *path_out,
            size_t path_cap, char *unit_out, size_t unit_cap,
            uint8_t invoc_out[16], uint64_t *observed_ns,
            uint32_t *stage, int *code, int *cleanup) {
        PA01SOLookup *u = (PA01SOLookup *)state;
        PA01SOConn *c;
        int r;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (u == NULL || path_out == NULL || unit_out == NULL
                || invoc_out == NULL || observed_ns == NULL
                || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        if (path_cap == 0 || unit_cap == 0
                || path_cap == SIZE_MAX || unit_cap == SIZE_MAX)
            return PA01SO_ARG;
        memset(path_out, 0, path_cap);
        memset(unit_out, 0, unit_cap);
        memset(invoc_out, 0, 16);
        *observed_ns = 0;
        if (u->kind != PA01SOL_KIND)
            { *stage = 6; *code = EINVAL; return PA01SO_STATE; }
        c = u->parent;
        if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u)
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (!pa01so_owner(&c->guard, 1))
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (u->mpid != NULL)
            { *stage = 6; *code = EBUSY; return PA01SO_STATE; }
        if (u->failure != 0) {
            pa01sol_diag(u, stage, code, cleanup);
            return u->failure;
        }
        if (u->phase != PA01SOL_DONE || !u->has_invoc)
            { *stage = 6; *code = ESTALE; return PA01SO_STATE; }
        if (path_cap < u->path_len + 1 || unit_cap < u->unit_len + 1)
            return PA01SO_ARG;
        r = (int)pa01sol_recheck(u);
        if (r != 0) {
            if (u->failure != 0) {
                pa01sol_diag(u, stage, code, cleanup);
                return u->failure;
            }
            *stage = 6; *code = ECHILD;
            *cleanup = u->cleanup_errno;
            return (uint32_t)r;
        }
        if (pa01soc_guard(c) != 0) {
            if (u->failure != 0) {
                pa01sol_diag(u, stage, code, cleanup);
                return u->failure;
            }
            *stage = c->guard.stage;
            *code = c->guard.native_code;
            *cleanup = c->guard.cleanup_errno;
            return c->guard.failure != 0 ? c->guard.failure : PA01SO_STATE;
        }
        memcpy(path_out, u->path, u->path_len + 1);
        memcpy(unit_out, u->unit, u->unit_len + 1);
        memcpy(invoc_out, u->invoc, 16);
        *observed_ns = u->observed_ns;
        pa01sol_diag(u, stage, code, cleanup);
        return 0;
    }
    static uint32_t pa01so_lookup_close(void **state, uint32_t *stage,
                                        int *code, int *cleanup) {
        PA01SOLookup *u;
        PA01SOConn *c;
        uint32_t result;
        if (stage != NULL) *stage = 0;
        if (code != NULL) *code = 0;
        if (cleanup != NULL) *cleanup = 0;
        if (state == NULL || stage == NULL || code == NULL || cleanup == NULL)
            return PA01SO_ARG;
        u = (PA01SOLookup *)*state;
        if (u == NULL) return 0;
        if (u->kind != PA01SOL_KIND)
            { *stage = 6; *code = EINVAL; return PA01SO_STATE; }
        c = u->parent;
        if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u)
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (!pa01so_owner(&c->guard, 0))
            { *stage = 6; *code = ECHILD; return PA01SO_STATE; }
        if (u->mpid != NULL)
            { *stage = 6; *code = EBUSY; return PA01SO_STATE; }
        if (u->failure == 0 && c->guard.failure != 0) {
            u->failure = c->guard.failure;
            u->stage = c->guard.stage;
            u->native_code = c->guard.native_code;
        }
        if (u->slot != NULL) u->slot = sd_bus_slot_unref(u->slot);
        if (u->reply != NULL) u->reply = sd_bus_message_unref(u->reply);
        pa01sol_dispose(u);
        result = u->failure;
        if (result == 0 && u->cleanup_errno != 0)
            result = pa01sol_fail(u, PA01SO_CLEANUP, 7, u->cleanup_errno);
        pa01sol_diag(u, stage, code, cleanup);
        c->lookup = NULL;
        explicit_bzero(u, sizeof(*u)); free(u); *state = NULL;
        return result;
    }
/* >>> PA01-MPID-BLOCA-START */
#define PA01SOMP_KIND UINT64_C(0x50413031534D0001)
enum {
    PA01SOMP_MAIN1 = 1,
    PA01SOMP_UNIT_MAIN = 2,
    PA01SOMP_UNIT_SELF = 3,
    PA01SOMP_MAIN2 = 4,
    PA01SOMP_INVOC = 5,
    PA01SOMP_DONE = 6
};
typedef struct {
    uint64_t kind;
    PA01SOLookup *parent;
    uint32_t main_pid;
    int main_fd;
    int ns_main;
    sd_bus_slot *slot;
    sd_bus_message *reply;
    uint8_t invoc[16];
    uint64_t observed_ns;
    int phase;
    int replied;
    int has_result;
    uint32_t failure;
    uint32_t stage;
    int native_code;
    int cleanup_errno;
} PA01SOMpid;

static uint32_t pa01somp_fail(PA01SOMpid *m, uint32_t status, uint32_t stage, int code)
{
    if (m->failure == 0) {
        m->failure = status;
        m->stage = stage;
        m->native_code = code;
    }
    return m->failure;
}

static void pa01somp_diag(PA01SOMpid *m, uint32_t *stage, int *code, int *cleanup)
{
    *stage = m->stage;
    *code = m->native_code;
    *cleanup = m->cleanup_errno;
}

static int pa01somp_close_fd(int *fd, PA01SOMpid *m)
{
    int owned = *fd;
    int saved;
    *fd = -1;
    if (owned < 0) {
        return 0;
    }
    if (close(owned) == 0) {
        return 0;
    }
    saved = errno;
    if (m->cleanup_errno == 0) {
        m->cleanup_errno = saved;
    }
    return -1;
}

static void pa01somp_dispose(PA01SOMpid *m)
{
    if (m->slot != NULL) {
        m->slot = sd_bus_slot_unref(m->slot);
    }
    if (m->reply != NULL) {
        m->reply = sd_bus_message_unref(m->reply);
    }
    pa01somp_close_fd(&m->main_fd, m);
    pa01somp_close_fd(&m->ns_main, m);
}

static int pa01somp_on_reply(sd_bus_message *msg, void *userdata, sd_bus_error *err)
{
    PA01SOMpid *m = (PA01SOMpid *)userdata;
    (void)err;
    if (m == NULL) {
        return 0;
    }
    if (m->kind != PA01SOMP_KIND) {
        return 0;
    }
    if (m->parent == NULL) {
        return 0;
    }
    if (m->parent->mpid != m) {
        return 0;
    }
    if (msg == NULL) {
        pa01somp_fail(m, PA01SO_IO, 10, ECONNRESET);
        return 0;
    }
    if (m->reply != NULL) {
        pa01somp_fail(m, PA01SO_STATE, 10, EPROTO);
        return 0;
    }
    m->reply = sd_bus_message_ref(msg);
    if (m->reply == NULL) {
        pa01somp_fail(m, PA01SO_MEM, 10, ENOMEM);
        return 0;
    }
    m->replied = 1;
    return 0;
}

static uint32_t pa01somp_owned_err(PA01SOMpid *m, uint32_t result, uint32_t *stage, int *code, int *cleanup)
{
    PA01SOLookup *u;
    PA01SOConn *c;
    if (m == NULL || stage == NULL || code == NULL || cleanup == NULL) {
        return PA01SO_ARG;
    }
    if (m->kind != PA01SOMP_KIND) {
        *stage = 6;
        *code = EINVAL;
        return PA01SO_STATE;
    }
    u = m->parent;
    if (u == NULL || u->kind != PA01SOL_KIND || u->mpid != m) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    c = u->parent;
    if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (!pa01so_owner(&c->guard, 1)) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (m->failure == 0 && u->failure != 0) {
        m->failure = u->failure;
        m->stage = u->stage;
        m->native_code = u->native_code;
    }
    if (m->failure == 0 && c->guard.failure != 0) {
        m->failure = c->guard.failure;
        m->stage = c->guard.stage;
        m->native_code = c->guard.native_code;
    }
    if (m->cleanup_errno == 0 && u->cleanup_errno != 0) {
        m->cleanup_errno = u->cleanup_errno;
    }
    if (m->cleanup_errno == 0 && c->guard.cleanup_errno != 0) {
        m->cleanup_errno = c->guard.cleanup_errno;
    }
    if (result != 0 && result != 5 && m->failure == 0) {
        pa01somp_fail(m, result, 6, EPROTO);
    }
    if (m->failure == 0 && m->cleanup_errno != 0) {
        pa01somp_fail(m, PA01SO_CLEANUP, 7, m->cleanup_errno);
    }
    if (m->failure != 0 || (result != 0 && result != 5)) {
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        pa01somp_diag(m, stage, code, cleanup);
        if (m->failure != 0) {
            return m->failure;
        }
        return result;
    }
    if (pa01soc_guard(c) != 0) {
        if (m->failure == 0) {
            m->failure = c->guard.failure;
            m->stage = c->guard.stage;
            m->native_code = c->guard.native_code;
        }
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        pa01somp_diag(m, stage, code, cleanup);
        return m->failure;
    }
    pa01somp_diag(m, stage, code, cleanup);
    return result;
}

static uint32_t pa01somp_parse_u(PA01SOMpid *m, uint32_t *out)
{
    sd_bus_message *msg;
    uint8_t tp = 0;
    uint32_t val = 0;
    int r;
    if (m == NULL || out == NULL) {
        return PA01SO_STATE;
    }
    msg = m->reply;
    if (msg == NULL) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    r = sd_bus_message_get_type(msg, &tp);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (tp != SD_BUS_MESSAGE_METHOD_RETURN) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_has_signature(msg, "v");
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_enter_container(msg, 'v', "u");
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_read(msg, "u", &val);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_at_end(msg, 0);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r != 1) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_exit_container(msg);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_at_end(msg, 1);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r != 1) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    *out = val;
    return 0;
}

static uint32_t pa01somp_parse_ay16(PA01SOMpid *m, uint8_t out[16])
{
    sd_bus_message *msg;
    uint8_t tp = 0;
    const void *pv = NULL;
    size_t vz = 0;
    int r;
    static const uint8_t zero[16] = {0};
    if (m == NULL || out == NULL) {
        return PA01SO_STATE;
    }
    msg = m->reply;
    if (msg == NULL) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    r = sd_bus_message_get_type(msg, &tp);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (tp != SD_BUS_MESSAGE_METHOD_RETURN) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_has_signature(msg, "v");
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_enter_container(msg, 'v', "ay");
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_read_array(msg, 'y', &pv, &vz);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0 || pv == NULL || vz != 16) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_at_end(msg, 0);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r != 1) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_exit_container(msg);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_at_end(msg, 1);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r != 1) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    if (memcmp(pv, zero, 16) == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    memcpy(out, pv, 16);
    return 0;
}

static uint32_t pa01somp_parse_osay_cmp(PA01SOMpid *m)
{
    sd_bus_message *msg;
    PA01SOLookup *u;
    const char *pp = NULL;
    const char *pu = NULL;
    const void *pv = NULL;
    size_t vz = 0;
    size_t lp = 0;
    size_t lu = 0;
    uint8_t tp = 0;
    int r;
    if (m == NULL) {
        return PA01SO_STATE;
    }
    u = m->parent;
    if (u == NULL || u->path == NULL || u->unit == NULL) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    if (!u->has_invoc) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    msg = m->reply;
    if (msg == NULL) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    r = sd_bus_message_get_type(msg, &tp);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (tp != SD_BUS_MESSAGE_METHOD_RETURN) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_has_signature(msg, "osay");
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_read(msg, "os", &pp, &pu);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0 || pp == NULL || pu == NULL) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_read_array(msg, 'y', &pv, &vz);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r == 0 || pv == NULL || vz != 16) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    r = sd_bus_message_at_end(msg, 1);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (r != 1) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    lp = strnlen(pp, u->max_path + 1);
    lu = strnlen(pu, u->max_unit + 1);
    if (lp != u->path_len || lu != u->unit_len) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE);
    }
    if (memcmp(pp, u->path, lp + 1) != 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE);
    }
    if (memcmp(pu, u->unit, lu + 1) != 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE);
    }
    if (memcmp(pv, u->invoc, 16) != 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE);
    }
    return 0;
}

static uint32_t pa01somp_main_alive(PA01SOMpid *m)
{
    PA01SOConn *c;
    int flags;
    struct pollfd p = {0};
    int r;
    if (m->main_fd < 0) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    c = m->parent->parent;
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    flags = fcntl(m->main_fd, F_GETFD);
    if (flags < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, errno);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if ((flags & FD_CLOEXEC) == 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    p.fd = m->main_fd;
    p.events = POLLIN;
    r = poll(&p, 1, 0);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, errno);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if (r != 0) {
        return pa01somp_fail(m, PA01SO_VERIFY, 10, ESRCH);
    }
    return 0;
}

static uint32_t pa01somp_ns_joined(PA01SOMpid *m)
{
    PA01SOLookup *u = m->parent;
    PA01SOConn *c = u->parent;
    int ns = -1;
    int nstype = 0;
    int flags;
    struct stat st;
    if (m->main_fd < 0) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    if (!u->has_init_ns) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
#if !defined(PIDFD_GET_PID_NAMESPACE) || !defined(NS_GET_NSTYPE) || !defined(CLONE_NEWPID)
    return pa01somp_fail(m, PA01SO_VERIFY, 10, ENOTSUP);
#else
    ns = ioctl(m->main_fd, PIDFD_GET_PID_NAMESPACE, 0);
    if (ns < 0) {
        int e = errno;
        if (e == ENOTTY || e == ENOSYS || e == EOPNOTSUPP) {
            return pa01somp_fail(m, PA01SO_VERIFY, 10, ENOTSUP);
        }
        return pa01somp_fail(m, PA01SO_IO, 10, e);
    }
    if (pa01soc_guard(c) != 0) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    flags = fcntl(ns, F_GETFD);
    if (flags < 0) {
        int e = errno;
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, PA01SO_IO, 10, e);
    }
    if ((flags & FD_CLOEXEC) == 0) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    if (pa01soc_guard(c) != 0) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    nstype = ioctl(ns, NS_GET_NSTYPE, 0);
    if (nstype < 0) {
        int e = errno;
        pa01somp_close_fd(&ns, m);
        if (e == ENOTTY || e == ENOSYS || e == EOPNOTSUPP) {
            return pa01somp_fail(m, PA01SO_VERIFY, 10, ENOTSUP);
        }
        return pa01somp_fail(m, PA01SO_IO, 10, e);
    }
    if (nstype != CLONE_NEWPID) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, PA01SO_VERIFY, 10, EPROTO);
    }
    if (pa01soc_guard(c) != 0) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if (fstat(ns, &st) != 0) {
        int e = errno;
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, PA01SO_IO, 10, e);
    }
    if (pa01soc_guard(c) != 0) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if (st.st_dev != u->init_ns_dev || st.st_ino != u->init_ns_ino) {
        pa01somp_close_fd(&ns, m);
        return pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE);
    }
    pa01somp_close_fd(&m->ns_main, m);
    m->ns_main = ns;
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    return 0;
#endif
}

static uint32_t pa01somp_recheck_main(PA01SOMpid *m)
{
    PA01SOLookup *u;
    PA01SOConn *c;
    uint32_t r;
    uint32_t ds = 0;
    int dc = 0;
    int dl = 0;
    uint32_t cr;
    if (m == NULL || m->parent == NULL) {
        return PA01SO_STATE;
    }
    u = m->parent;
    c = u->parent;
    if (u->kind != PA01SOL_KIND || c == NULL || c->kind != PA01SOC_KIND) {
        return PA01SO_STATE;
    }
    cr = pa01somp_owned_err(m, 0, &ds, &dc, &dl);
    if (cr != 0) {
        return cr;
    }
    r = pa01sol_recheck(u);
    if (r != 0) {
        if (u->failure != 0) {
            if (m->failure == 0) {
                m->failure = u->failure;
                m->stage = u->stage;
                m->native_code = u->native_code;
            }
            if (m->cleanup_errno == 0 && u->cleanup_errno != 0) {
                m->cleanup_errno = u->cleanup_errno;
            }
            return u->failure;
        }
        if (u->cleanup_errno != 0) {
            if (m->cleanup_errno == 0) {
                m->cleanup_errno = u->cleanup_errno;
            }
            if (m->failure == 0) {
                pa01somp_fail(m, PA01SO_CLEANUP, 7, m->cleanup_errno);
            }
            return m->failure;
        }
        cr = pa01somp_owned_err(m, r, &ds, &dc, &dl);
        if (cr != 0) {
            return cr;
        }
        return r;
    }
    cr = pa01somp_owned_err(m, 0, &ds, &dc, &dl);
    if (cr != 0) {
        return cr;
    }
    r = pa01somp_main_alive(m);
    if (r != 0) {
        return r;
    }
    cr = pa01somp_owned_err(m, 0, &ds, &dc, &dl);
    if (cr != 0) {
        return cr;
    }
    r = pa01somp_ns_joined(m);
    if (r != 0) {
        return r;
    }
    cr = pa01somp_owned_err(m, 0, &ds, &dc, &dl);
    if (cr != 0) {
        return cr;
    }
    return 0;
}

static uint32_t pa01somp_pin_main(PA01SOMpid *m, uint32_t val)
{
    PA01SOLookup *u = m->parent;
    PA01SOConn *c = u->parent;
    int fd = -1;
    int flags;
    struct pollfd p = {0};
    int r;
    if (val == 0) {
        return pa01somp_fail(m, PA01SO_STATE, 8, ESRCH);
    }
    _Static_assert((pid_t)-1 < 0, "PA01SOMP_REQUIRES_SIGNED_PIDT");
    _Static_assert(sizeof(pid_t) == sizeof(int32_t), "PA01SOMP_REQUIRES_PIDT32");
    if (val > (uint32_t)INT32_MAX) {
        return pa01somp_fail(m, PA01SO_VERIFY, 8, ERANGE);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    fd = pidfd_open((pid_t)val, 0);
    if (fd < 0) {
        return pa01somp_fail(m, PA01SO_IO, 8, errno);
    }
    if (pa01soc_guard(c) != 0) {
        pa01somp_close_fd(&fd, m);
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    m->main_fd = fd;
    m->main_pid = val;
    flags = fcntl(m->main_fd, F_GETFD);
    if (flags < 0) {
        int e = errno;
        m->main_fd = -1;
        pa01somp_close_fd(&fd, m);
        return pa01somp_fail(m, PA01SO_IO, 8, e);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if ((flags & FD_CLOEXEC) == 0) {
        m->main_fd = -1;
        pa01somp_close_fd(&fd, m);
        return pa01somp_fail(m, PA01SO_VERIFY, 8, EPROTO);
    }
    p.fd = m->main_fd;
    p.events = POLLIN;
    r = poll(&p, 1, 0);
    if (r < 0) {
        int e = errno;
        m->main_fd = -1;
        pa01somp_close_fd(&fd, m);
        return pa01somp_fail(m, PA01SO_IO, 8, e);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if (r != 0) {
        m->main_fd = -1;
        pa01somp_close_fd(&fd, m);
        return pa01somp_fail(m, PA01SO_VERIFY, 8, ESRCH);
    }
    r = (int)pa01somp_ns_joined(m);
    if (r != 0) {
        m->main_fd = -1;
        pa01somp_close_fd(&fd, m);
        return (uint32_t)r;
    }
    return 0;
}

static uint32_t pa01somp_send(PA01SOMpid *m)
{
    PA01SOLookup *u = m->parent;
    PA01SOConn *c = u->parent;
    sd_bus_message *msg = NULL;
    uint64_t end;
    uint64_t last;
    uint64_t budget;
    int r;
    int fd = -1;
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    if (m->phase != PA01SOMP_MAIN1 && m->phase != PA01SOMP_UNIT_MAIN && m->phase != PA01SOMP_UNIT_SELF && m->phase != PA01SOMP_MAIN2 && m->phase != PA01SOMP_INVOC) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    if (m->slot != NULL) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    if (m->phase == PA01SOMP_UNIT_MAIN) {
        fd = m->main_fd;
    }
    if (m->phase == PA01SOMP_UNIT_SELF) {
        fd = u->pidfd;
    }
    if ((m->phase == PA01SOMP_UNIT_MAIN || m->phase == PA01SOMP_UNIT_SELF) && fd < 0) {
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    if (m->phase == PA01SOMP_MAIN1 || m->phase == PA01SOMP_MAIN2) {
        r = sd_bus_message_new_method_call(c->bus, &msg, NULL, u->path, "org.freedesktop.DBus.Properties", "Get");
        if (r < 0 || msg == NULL) {
            if (msg != NULL) {
                msg = sd_bus_message_unref(msg);
            }
            return pa01somp_fail(m, PA01SO_IO, 10, r < 0 ? r : EPROTO);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_set_auto_start(msg, 0);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_set_allow_interactive_authorization(msg, 0);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_append(msg, "ss", "org.freedesktop.systemd1.Service", "MainPID");
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
    }
    if (m->phase == PA01SOMP_INVOC) {
        r = sd_bus_message_new_method_call(c->bus, &msg, NULL, u->path, "org.freedesktop.DBus.Properties", "Get");
        if (r < 0 || msg == NULL) {
            if (msg != NULL) {
                msg = sd_bus_message_unref(msg);
            }
            return pa01somp_fail(m, PA01SO_IO, 10, r < 0 ? r : EPROTO);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_set_auto_start(msg, 0);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_set_allow_interactive_authorization(msg, 0);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_append(msg, "ss", "org.freedesktop.systemd1.Unit", "InvocationID");
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
    }
    if (m->phase == PA01SOMP_UNIT_MAIN || m->phase == PA01SOMP_UNIT_SELF) {
        r = sd_bus_message_new_method_call(c->bus, &msg, NULL, "/org/freedesktop/systemd1", "org.freedesktop.systemd1.Manager", "GetUnitByPIDFD");
        if (r < 0 || msg == NULL) {
            if (msg != NULL) {
                msg = sd_bus_message_unref(msg);
            }
            return pa01somp_fail(m, PA01SO_IO, 10, r < 0 ? r : EPROTO);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_set_auto_start(msg, 0);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_set_allow_interactive_authorization(msg, 0);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
        if (pa01soc_guard(c) != 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
        }
        r = sd_bus_message_append(msg, "h", fd);
        if (r < 0) {
            msg = sd_bus_message_unref(msg);
            return pa01somp_fail(m, PA01SO_IO, 10, r);
        }
    }
    if (pa01soc_guard(c) != 0) {
        msg = sd_bus_message_unref(msg);
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    end = c->guard.end_ns;
    last = c->guard.last_ns;
    if (end <= last) {
        msg = sd_bus_message_unref(msg);
        return pa01somp_fail(m, PA01SO_EXPIRED, 10, ETIMEDOUT);
    }
    budget = (end - last) / UINT64_C(1000);
    if (budget == 0) {
        msg = sd_bus_message_unref(msg);
        return pa01somp_fail(m, PA01SO_EXPIRED, 10, ETIMEDOUT);
    }
    m->replied = 0;
    if (m->reply != NULL) {
        msg = sd_bus_message_unref(msg);
        return pa01somp_fail(m, PA01SO_STATE, 10, ESTALE);
    }
    r = sd_bus_call_async(c->bus, &m->slot, msg, pa01somp_on_reply, m, budget);
    msg = sd_bus_message_unref(msg);
    if (r < 0 || m->slot == NULL) {
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        return pa01somp_fail(m, PA01SO_IO, 10, r < 0 ? r : EPROTO);
    }
    r = sd_bus_slot_set_floating(m->slot, 0);
    if (r < 0) {
        return pa01somp_fail(m, PA01SO_IO, 10, r);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_fail(m, c->guard.failure, 6, c->guard.native_code);
    }
    return 0;
}
/* <<< PA01-MPID-BLOCA-END */
/* >>> PA01-MPID-BLOCB-START */
static uint32_t pa01so_mpid_start(void **out, void *ld, uint32_t *stage, int *code, int *cleanup)
{
    PA01SOLookup *u = (PA01SOLookup *)ld;
    PA01SOConn *c;
    PA01SOMpid *m = NULL;
    uint32_t rr;
    if (stage != NULL) {
        *stage = 0;
    }
    if (code != NULL) {
        *code = 0;
    }
    if (cleanup != NULL) {
        *cleanup = 0;
    }
    if (out == NULL || *out != NULL || u == NULL || stage == NULL || code == NULL || cleanup == NULL) {
        return PA01SO_ARG;
    }
    if (u->kind != PA01SOL_KIND) {
        *stage = 6;
        *code = EINVAL;
        return PA01SO_STATE;
    }
    c = u->parent;
    if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (!pa01so_owner(&c->guard, 1)) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (u->mpid != NULL) {
        *stage = 6;
        *code = EBUSY;
        return PA01SO_STATE;
    }
    if (u->phase != PA01SOL_DONE || !u->has_invoc) {
        *stage = 6;
        *code = ESTALE;
        return PA01SO_STATE;
    }
    if (c->phase != PA01SOC_READY || c->bus == NULL) {
        *stage = 6;
        *code = ESTALE;
        return PA01SO_STATE;
    }
    if (u->failure != 0) {
        *stage = u->stage;
        *code = u->native_code;
        *cleanup = u->cleanup_errno;
        return u->failure;
    }
    if (u->cleanup_errno != 0) {
        *stage = 7;
        *code = u->cleanup_errno;
        *cleanup = u->cleanup_errno;
        return PA01SO_CLEANUP;
    }
    if (c->guard.failure != 0) {
        *stage = c->guard.stage;
        *code = c->guard.native_code;
        *cleanup = c->guard.cleanup_errno;
        return c->guard.failure;
    }
    if (c->guard.cleanup_errno != 0) {
        *stage = 7;
        *code = c->guard.cleanup_errno;
        *cleanup = c->guard.cleanup_errno;
        return PA01SO_CLEANUP;
    }
    if (pa01soc_guard(c) != 0) {
        *stage = c->guard.stage;
        *code = c->guard.native_code;
        *cleanup = c->guard.cleanup_errno;
        return c->guard.failure;
    }
    rr = pa01sol_recheck(u);
    if (rr != 0) {
        if (u->failure != 0) {
            *stage = u->stage;
            *code = u->native_code;
            *cleanup = u->cleanup_errno;
            return u->failure;
        }
        if (u->cleanup_errno != 0) {
            *stage = 7;
            *code = u->cleanup_errno;
            *cleanup = u->cleanup_errno;
            return PA01SO_CLEANUP;
        }
        if (c->guard.failure != 0) {
            *stage = c->guard.stage;
            *code = c->guard.native_code;
            *cleanup = c->guard.cleanup_errno;
            return c->guard.failure;
        }
        if (c->guard.cleanup_errno != 0) {
            *stage = 7;
            *code = c->guard.cleanup_errno;
            *cleanup = c->guard.cleanup_errno;
            return PA01SO_CLEANUP;
        }
        *stage = 6;
        *code = ECHILD;
        *cleanup = u->cleanup_errno;
        return rr;
    }
    if (u->failure != 0) {
        *stage = u->stage;
        *code = u->native_code;
        *cleanup = u->cleanup_errno;
        return u->failure;
    }
    if (u->cleanup_errno != 0) {
        *stage = 7;
        *code = u->cleanup_errno;
        *cleanup = u->cleanup_errno;
        return PA01SO_CLEANUP;
    }
    if (c->guard.failure != 0) {
        *stage = c->guard.stage;
        *code = c->guard.native_code;
        *cleanup = c->guard.cleanup_errno;
        return c->guard.failure;
    }
    if (c->guard.cleanup_errno != 0) {
        *stage = 7;
        *code = c->guard.cleanup_errno;
        *cleanup = c->guard.cleanup_errno;
        return PA01SO_CLEANUP;
    }
    m = (PA01SOMpid *)calloc(1, sizeof(*m));
    if (m == NULL) {
        *stage = 6;
        *code = ENOMEM;
        return PA01SO_MEM;
    }
    m->kind = PA01SOMP_KIND;
    m->parent = u;
    m->main_fd = -1;
    m->ns_main = -1;
    m->phase = PA01SOMP_MAIN1;
    if (pa01soc_guard(c) != 0) {
        uint32_t pr = c->guard.failure;
        uint32_t ps = c->guard.stage;
        int pc = c->guard.native_code;
        int pl = c->guard.cleanup_errno;
        explicit_bzero(m, sizeof(*m));
        free(m);
        *stage = ps;
        *code = pc;
        *cleanup = pl;
        return pr;
    }
    if (u->failure != 0 || u->cleanup_errno != 0 || c->guard.failure != 0 || c->guard.cleanup_errno != 0) {
        uint32_t ps;
        int pc;
        int pl;
        if (u->failure != 0) {
            ps = u->stage;
            pc = u->native_code;
            pl = u->cleanup_errno;
            explicit_bzero(m, sizeof(*m));
            free(m);
            *stage = ps;
            *code = pc;
            *cleanup = pl;
            return u->failure;
        }
        if (c->guard.failure != 0) {
            ps = c->guard.stage;
            pc = c->guard.native_code;
            pl = c->guard.cleanup_errno;
            explicit_bzero(m, sizeof(*m));
            free(m);
            *stage = ps;
            *code = pc;
            *cleanup = pl;
            return c->guard.failure;
        }
        explicit_bzero(m, sizeof(*m));
        free(m);
        *stage = 7;
        *code = u->cleanup_errno != 0 ? u->cleanup_errno : c->guard.cleanup_errno;
        *cleanup = *code;
        return PA01SO_CLEANUP;
    }
    u->mpid = m;
    *out = m;
    pa01somp_diag(m, stage, code, cleanup);
    return 5;
}

static uint32_t pa01so_mpid_step(void *state, uint32_t *stage, int *code, int *cleanup)
{
    PA01SOMpid *m = (PA01SOMpid *)state;
    PA01SOLookup *u;
    PA01SOConn *c;
    int r;
    int ready = 0;
    uint32_t v = 0;
    uint8_t iv[16] = {0};
    if (stage != NULL) {
        *stage = 0;
    }
    if (code != NULL) {
        *code = 0;
    }
    if (cleanup != NULL) {
        *cleanup = 0;
    }
    if (m == NULL || stage == NULL || code == NULL || cleanup == NULL) {
        return PA01SO_ARG;
    }
    if (m->kind != PA01SOMP_KIND) {
        *stage = 6;
        *code = EINVAL;
        return PA01SO_STATE;
    }
    u = m->parent;
    if (u == NULL || u->kind != PA01SOL_KIND || u->mpid != m) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    c = u->parent;
    if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (!pa01so_owner(&c->guard, 1)) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (m->failure != 0 || m->cleanup_errno != 0 || u->failure != 0 || u->cleanup_errno != 0 || c->guard.failure != 0 || c->guard.cleanup_errno != 0) {
        return pa01somp_owned_err(m, 0, stage, code, cleanup);
    }
    if (pa01soc_guard(c) != 0) {
        return pa01somp_owned_err(m, c->guard.failure, stage, code, cleanup);
    }
    if (m->phase == PA01SOMP_DONE) {
        r = (int)pa01somp_recheck_main(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        return pa01somp_owned_err(m, 0, stage, code, cleanup);
    }
    if (m->slot == NULL) {
        if (m->main_fd >= 0) {
            r = (int)pa01somp_recheck_main(m);
        } else {
            r = (int)pa01sol_recheck(u);
        }
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (m->failure != 0 || m->cleanup_errno != 0 || u->failure != 0 || u->cleanup_errno != 0 || c->guard.failure != 0 || c->guard.cleanup_errno != 0) {
            return pa01somp_owned_err(m, 0, stage, code, cleanup);
        }
        r = (int)pa01somp_send(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    if (m->main_fd >= 0) {
        r = (int)pa01somp_recheck_main(m);
    } else {
        r = (int)pa01sol_recheck(u);
    }
    if (r != 0) {
        return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
    }
    if (m->failure != 0 || m->cleanup_errno != 0 || u->failure != 0 || u->cleanup_errno != 0 || c->guard.failure != 0 || c->guard.cleanup_errno != 0) {
        return pa01somp_owned_err(m, 0, stage, code, cleanup);
    }
    r = (int)pa01soc_can_process(c, &ready);
    if (r != 0) {
        return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
    }
    if (!ready) {
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    r = sd_bus_process(c->bus, NULL);
    if (m->failure != 0) {
        return pa01somp_owned_err(m, m->failure, stage, code, cleanup);
    }
    if (r < 0) {
        return pa01somp_owned_err(m, pa01somp_fail(m, PA01SO_IO, 10, r), stage, code, cleanup);
    }
    if (m->main_fd >= 0) {
        r = (int)pa01somp_recheck_main(m);
    } else {
        r = (int)pa01sol_recheck(u);
    }
    if (r != 0) {
        return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
    }
    if (m->failure != 0 || m->cleanup_errno != 0 || u->failure != 0 || u->cleanup_errno != 0 || c->guard.failure != 0 || c->guard.cleanup_errno != 0) {
        return pa01somp_owned_err(m, 0, stage, code, cleanup);
    }
    if (!m->replied || m->reply == NULL) {
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    if (m->phase == PA01SOMP_MAIN1) {
        r = (int)pa01somp_parse_u(m, &v);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        if (v == 0) {
            return pa01somp_owned_err(m, pa01somp_fail(m, PA01SO_STATE, 10, ESRCH), stage, code, cleanup);
        }
        r = (int)pa01somp_pin_main(m, v);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        r = (int)pa01sol_recheck(u);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        m->phase = PA01SOMP_UNIT_MAIN;
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    if (m->phase == PA01SOMP_UNIT_MAIN) {
        r = (int)pa01somp_parse_osay_cmp(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        r = (int)pa01somp_recheck_main(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        m->phase = PA01SOMP_UNIT_SELF;
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    if (m->phase == PA01SOMP_UNIT_SELF) {
        r = (int)pa01somp_parse_osay_cmp(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        r = (int)pa01somp_recheck_main(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        m->phase = PA01SOMP_MAIN2;
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    if (m->phase == PA01SOMP_MAIN2) {
        r = (int)pa01somp_parse_u(m, &v);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (v != m->main_pid) {
            return pa01somp_owned_err(m, pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE), stage, code, cleanup);
        }
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        r = (int)pa01somp_recheck_main(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        m->phase = PA01SOMP_INVOC;
        return pa01somp_owned_err(m, 5, stage, code, cleanup);
    }
    if (m->phase == PA01SOMP_INVOC) {
        r = (int)pa01somp_parse_ay16(m, iv);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (memcmp(iv, u->invoc, 16) != 0) {
            return pa01somp_owned_err(m, pa01somp_fail(m, PA01SO_VERIFY, 10, ESTALE), stage, code, cleanup);
        }
        memcpy(m->invoc, iv, 16);
        if (m->slot != NULL) {
            m->slot = sd_bus_slot_unref(m->slot);
        }
        if (m->reply != NULL) {
            m->reply = sd_bus_message_unref(m->reply);
        }
        r = (int)pa01somp_recheck_main(m);
        if (r != 0) {
            return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
        }
        if (pa01soc_guard(c) != 0) {
            return pa01somp_owned_err(m, c->guard.failure, stage, code, cleanup);
        }
        m->observed_ns = c->guard.last_ns;
        m->has_result = 1;
        m->phase = PA01SOMP_DONE;
        return pa01somp_owned_err(m, 0, stage, code, cleanup);
    }
    return pa01somp_owned_err(m, pa01somp_fail(m, PA01SO_STATE, 10, ESTALE), stage, code, cleanup);
}

static uint32_t pa01so_mpid_snapshot(void *state, uint32_t *main_pid, uint8_t *invoc16, uint64_t *observed_ns, uint32_t *stage, int *code, int *cleanup)
{
    PA01SOMpid *m = (PA01SOMpid *)state;
    PA01SOLookup *u;
    PA01SOConn *c;
    int r;
    uint32_t gr;
    if (stage != NULL) {
        *stage = 0;
    }
    if (code != NULL) {
        *code = 0;
    }
    if (cleanup != NULL) {
        *cleanup = 0;
    }
    if (m == NULL || main_pid == NULL || invoc16 == NULL || observed_ns == NULL || stage == NULL || code == NULL || cleanup == NULL) {
        return PA01SO_ARG;
    }
    *main_pid = 0;
    memset(invoc16, 0, 16);
    *observed_ns = 0;
    if (m->kind != PA01SOMP_KIND) {
        *stage = 6;
        *code = EINVAL;
        return PA01SO_STATE;
    }
    u = m->parent;
    if (u == NULL || u->kind != PA01SOL_KIND || u->mpid != m) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    c = u->parent;
    if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (!pa01so_owner(&c->guard, 1)) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (m->phase != PA01SOMP_DONE || !m->has_result) {
        *stage = 6;
        *code = ESTALE;
        return PA01SO_STATE;
    }
    r = (int)pa01somp_recheck_main(m);
    if (r != 0) {
        return pa01somp_owned_err(m, (uint32_t)r, stage, code, cleanup);
    }
    gr = pa01somp_owned_err(m, 0, stage, code, cleanup);
    if (gr != 0) {
        *main_pid = 0;
        memset(invoc16, 0, 16);
        *observed_ns = 0;
        return gr;
    }
    if (m->main_pid == 0) {
        *stage = 6;
        *code = ESRCH;
        return PA01SO_STATE;
    }
    *main_pid = m->main_pid;
    memcpy(invoc16, m->invoc, 16);
    *observed_ns = m->observed_ns;
    return 0;
}

static uint32_t pa01so_mpid_close(void **state, uint32_t *stage, int *code, int *cleanup)
{
    PA01SOMpid *m;
    PA01SOLookup *u;
    PA01SOConn *c;
    uint32_t result;
    if (stage != NULL) {
        *stage = 0;
    }
    if (code != NULL) {
        *code = 0;
    }
    if (cleanup != NULL) {
        *cleanup = 0;
    }
    if (state == NULL || stage == NULL || code == NULL || cleanup == NULL) {
        return PA01SO_ARG;
    }
    m = (PA01SOMpid *)*state;
    if (m == NULL) {
        return 0;
    }
    if (m->kind != PA01SOMP_KIND) {
        *stage = 6;
        *code = EINVAL;
        return PA01SO_STATE;
    }
    u = m->parent;
    if (u == NULL || u->kind != PA01SOL_KIND || u->mpid != m) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    c = u->parent;
    if (c == NULL || c->kind != PA01SOC_KIND || c->lookup != u) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (!pa01so_owner(&c->guard, 0)) {
        *stage = 6;
        *code = ECHILD;
        return PA01SO_STATE;
    }
    if (m->failure == 0 && u->failure != 0) {
        m->failure = u->failure;
        m->stage = u->stage;
        m->native_code = u->native_code;
    }
    if (m->failure == 0 && c->guard.failure != 0) {
        m->failure = c->guard.failure;
        m->stage = c->guard.stage;
        m->native_code = c->guard.native_code;
    }
    if (m->cleanup_errno == 0 && u->cleanup_errno != 0) {
        m->cleanup_errno = u->cleanup_errno;
    }
    if (m->cleanup_errno == 0 && c->guard.cleanup_errno != 0) {
        m->cleanup_errno = c->guard.cleanup_errno;
    }
    if (m->slot != NULL) {
        m->slot = sd_bus_slot_unref(m->slot);
    }
    if (m->reply != NULL) {
        m->reply = sd_bus_message_unref(m->reply);
    }
    pa01somp_dispose(m);
    result = m->failure;
    if (result == 0 && m->cleanup_errno != 0) {
        result = pa01somp_fail(m, PA01SO_CLEANUP, 7, m->cleanup_errno);
    }
    pa01somp_diag(m, stage, code, cleanup);
    u->mpid = NULL;
    explicit_bzero(m, sizeof(*m));
    free(m);
    *state = NULL;
    return result;
}
/* <<< PA01-MPID-BLOCB-END */
    """
    uint32_t pa01so_open(void **, void *, uint64_t, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_snapshot(void *, uint64_t *, size_t, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_close(void **, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_conn_start(void **, const char *, size_t, uint64_t, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_conn_step(void *, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_conn_snapshot(void *, uint64_t *, size_t, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_conn_close(void **, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_lookup_start(void **, void *, size_t, size_t, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_lookup_step(void *, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_lookup_snapshot(void *, char *, size_t, char *, size_t, uint8_t *, uint64_t *, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_lookup_close(void **, uint32_t *, int *, int *) noexcept
    uint32_t pa01so_mpid_start(void **out, void *lookup_done, uint32_t *stage, int *code, int *cleanup) noexcept
    uint32_t pa01so_mpid_step(void *state, uint32_t *stage, int *code, int *cleanup) noexcept
    uint32_t pa01so_mpid_snapshot(void *state, uint32_t *main_pid, uint8_t *invoc16, uint64_t *observed_ns, uint32_t *stage, int *code, int *cleanup) noexcept
    uint32_t pa01so_mpid_close(void **state, uint32_t *stage, int *code, int *cleanup) noexcept

cdef public uint32_t pa01_sysd_open(void **out, void *bus, uint64_t deadline_ns,
        uint32_t *stage, int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_open(out, bus, deadline_ns, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_snapshot(void *state, uint64_t *facts, size_t facts_len,
        uint32_t *stage, int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_snapshot(state, facts, facts_len, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_close(void **state, uint32_t *stage,
        int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_close(state, stage, native_code, cleanup_errno)


cdef public uint32_t pa01_sysd_conn_start(void **out, const char *endpoint,
        size_t endpoint_len, uint64_t deadline_ns,
        uint32_t *stage, int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_conn_start(out, endpoint, endpoint_len, deadline_ns,
                             stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_conn_step(void *state, uint32_t *stage,
        int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_conn_step(state, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_conn_snapshot(void *state, uint64_t *facts,
        size_t facts_len, uint32_t *stage, int *native_code,
        int *cleanup_errno) noexcept nogil:
    return pa01so_conn_snapshot(state, facts, facts_len, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_conn_close(void **state, uint32_t *stage,
        int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_conn_close(state, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_lookup_start(void **out, void *conn,
        size_t max_path, size_t max_unit,
        uint32_t *stage, int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_lookup_start(out, conn, max_path, max_unit,
                               stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_lookup_step(void *state, uint32_t *stage,
        int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_lookup_step(state, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_lookup_snapshot(void *state, char *path_out,
        size_t path_cap, char *unit_out, size_t unit_cap, uint8_t *invoc_out,
        uint64_t *observed_ns, uint32_t *stage, int *native_code,
        int *cleanup_errno) noexcept nogil:
    return pa01so_lookup_snapshot(state, path_out, path_cap, unit_out,
                                  unit_cap, invoc_out, observed_ns,
                                  stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_lookup_close(void **state, uint32_t *stage,
        int *native_code, int *cleanup_errno) noexcept nogil:
    return pa01so_lookup_close(state, stage, native_code, cleanup_errno)

cdef public uint32_t pa01_sysd_mpid_start(void **out, void *lookup_done, uint32_t *stage, int *code, int *cleanup) noexcept nogil:
    return pa01so_mpid_start(out, lookup_done, stage, code, cleanup)
cdef public uint32_t pa01_sysd_mpid_step(void *state, uint32_t *stage, int *code, int *cleanup) noexcept nogil:
    return pa01so_mpid_step(state, stage, code, cleanup)
cdef public uint32_t pa01_sysd_mpid_snapshot(void *state, uint32_t *main_pid, uint8_t *invoc16, uint64_t *observed_ns, uint32_t *stage, int *code, int *cleanup) noexcept nogil:
    return pa01so_mpid_snapshot(state, main_pid, invoc16, observed_ns, stage, code, cleanup)
cdef public uint32_t pa01_sysd_mpid_close(void **state, uint32_t *stage, int *code, int *cleanup) noexcept nogil:
    return pa01so_mpid_close(state, stage, code, cleanup)
