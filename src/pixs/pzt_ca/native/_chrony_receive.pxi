# Prive Z12 : reception native d'un datagramme, sans confiance NTS/UTC.
# Inclure apres deadline, launch_obs, systemd_connection et process_image.
# Appelant natif exclusif : socket emprunte, aucun descripteur fourni par Python.
# Les credentials restent soumis aux privileges du noyau ; aucune attestation
# contre un acteur privilegie. Role/politique/artefacts/temps restent requis.
from libc.stddef cimport size_t

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
    #include <sys/uio.h>
    #include <sys/un.h>
    #include <sys/stat.h>
    #include <sys/vfs.h>
    #include <sys/pidfd.h>
    #include <linux/magic.h>
    #if !defined(SCM_PIDFD) || !defined(SO_PASSPIDFD) || !defined(PID_FS_MAGIC)
    #error "Z12 requires the selected glibc 2.41 / Linux 6.12 socket-pidfd ABI"
    #endif
    /* Limites de format chrony et SCM Linux, aucune valeur d'exploitation. */
    enum { Z12_R_WIRE=284, Z12_R_RIGHTS=253, Z12_R_FDS=254 };
    typedef struct {
        uint8_t payload[Z12_R_WIRE];
        size_t length;
        struct ucred credentials;
        int peer_fd;
        dev_t peer_dev;
        ino_t peer_ino;
        uint64_t observed_monotonic_ns;
    } Z12ChronyDatagram;
    typedef struct {
        Z12ProcessImageDiag base;
        int would_block, transient_errno;
        int truncated, ancillary_invalid, cleanup_unverified;
        int rights_seen, pidfd_delivery_present, pidfd_delivery_value;
    } Z12ChronyReceiveDiag;
    typedef struct {
        dev_t dev; ino_t ino;
        uint64_t cookie;
        struct sockaddr_un peer;
        socklen_t peer_length;
    } Z12ReceiveSocketFacts;
    typedef struct {
        int fds[Z12_R_FDS];
        size_t count;
        int peer_slot, credential_count, pidfd_count, invalid;
        struct ucred credentials;
    } Z12ReceiveInventory;

    static int z12_r_guard(Z12ImageCtx *owner, Z12ChronyReceiveDiag *d) {
        return z12_image_guard(owner, &d->base);
    }
    static int z12_r_verdict(Z12ChronyReceiveDiag *d, int status) {
        int r = z12_image_verdict(&d->base, status);
        if (r != 1 && r != 2) return r;
        if (d->truncated || d->ancillary_invalid || d->cleanup_unverified || d->rights_seen)
            return 0;
        return r;
    }
    /* Appeler immediatement apres la primitive POSIX, avant autre appel. */
    static int z12_r_post(Z12ImageCtx *o, Z12ChronyReceiveDiag *d, int code) {
        if (code < 0) z12_sysd_first(&d->base.native, Z12_SYSD_ERRNO, errno);
        return z12_r_guard(o, d);
    }
    static int z12_r_flags(Z12ImageCtx *o, int fd, int command, int *value,
                           Z12ChronyReceiveDiag *d) {
        int code, r = z12_r_guard(o, d);
        if (r != 1) return r;
        code = fcntl(fd, command);
        r = z12_r_post(o, d, code);
        if (r == 1) *value = code;
        return r;
    }
    static int z12_r_option(Z12ImageCtx *o, int fd, int option, int expected,
                            Z12ChronyReceiveDiag *d) {
        int value = 0, code, r = z12_r_guard(o, d);
        socklen_t length = sizeof(value);
        if (r != 1) return r;
        code = getsockopt(fd, SOL_SOCKET, option, &value, &length);
        r = z12_r_post(o, d, code); if (r != 1) return r;
        if (length != sizeof(value) || value != expected) {
            d->base.native.foreign_binding = 1; return 0;
        }
        return 1;
    }
    static int z12_r_stat(Z12ImageCtx *o, int fd, struct stat *s,
                          Z12ChronyReceiveDiag *d) {
        int code, r = z12_r_guard(o, d);
        if (r != 1) return r;
        code = fstat(fd, s);
        return z12_r_post(o, d, code);
    }
    static int z12_r_statfs(Z12ImageCtx *o, int fd, struct statfs *s,
                            Z12ChronyReceiveDiag *d) {
        int code, r = z12_r_guard(o, d);
        if (r != 1) return r;
        code = fstatfs(fd, s);
        return z12_r_post(o, d, code);
    }
    static int z12_r_live(Z12ImageCtx *o, int fd, Z12ChronyReceiveDiag *d) {
        int r, after;
        r = z12_r_guard(o, d); if (r != 1) return r;
        r = z12_sysd_pidfd_live(fd, &d->base.native);
        after = z12_r_guard(o, d);
        return r != 1 ? z12_r_verdict(d, r) : after;
    }
    static int z12_r_socket(Z12ImageCtx *o, int fd, Z12ReceiveSocketFacts *out,
                            Z12ChronyReceiveDiag *d) {
        struct stat st;
        int flags, code, r;
        socklen_t length;
        memset(out, 0, sizeof(*out));
        r = z12_r_flags(o, fd, F_GETFD, &flags, d); if (r != 1) return r;
        if ((flags & FD_CLOEXEC) == 0) { d->base.native.foreign_binding = 1; return 0; }
        r = z12_r_flags(o, fd, F_GETFL, &flags, d); if (r != 1) return r;
        if ((flags & O_NONBLOCK) == 0) { d->base.native.foreign_binding = 1; return 0; }
        r = z12_r_option(o, fd, SO_TYPE, SOCK_DGRAM, d); if (r != 1) return r;
        r = z12_r_option(o, fd, SO_DOMAIN, AF_UNIX, d); if (r != 1) return r;
        r = z12_r_option(o, fd, SO_PASSCRED, 1, d); if (r != 1) return r;
        r = z12_r_option(o, fd, SO_PASSPIDFD, 1, d); if (r != 1) return r;
        r = z12_r_stat(o, fd, &st, d); if (r != 1) return r;
        if (!S_ISSOCK(st.st_mode)) { d->base.native.foreign_binding = 1; return 0; }
        out->dev = st.st_dev; out->ino = st.st_ino;
        length = sizeof(out->cookie);
        code = getsockopt(fd, SOL_SOCKET, SO_COOKIE, &out->cookie, &length);
        r = z12_r_post(o, d, code); if (r != 1) return r;
        if (length != sizeof(out->cookie)) { d->base.native.native_output_invalid = 1; return 0; }
        out->peer_length = sizeof(out->peer);
        code = getpeername(fd, (struct sockaddr *)&out->peer, &out->peer_length);
        r = z12_r_post(o, d, code); if (r != 1) return r;
        if (out->peer.sun_family != AF_UNIX ||
            out->peer_length < offsetof(struct sockaddr_un, sun_path) ||
            out->peer_length > sizeof(out->peer)) {
            d->base.native.foreign_binding = 1; return 0;
        }
        return 1;
    }
    static int z12_r_same_socket(const Z12ReceiveSocketFacts *a,
                                 const Z12ReceiveSocketFacts *b) {
        return a->dev == b->dev && a->ino == b->ino && a->cookie == b->cookie &&
            a->peer_length == b->peer_length && a->peer.sun_family == b->peer.sun_family &&
            memcmp(a->peer.sun_path, b->peer.sun_path,
                   a->peer_length - offsetof(struct sockaddr_un, sun_path)) == 0;
    }
    static int z12_r_own_fd(Z12ReceiveInventory *i, int fd, Z12ChronyReceiveDiag *d) {
        size_t slot;
        if (fd < 0) { i->invalid = 1; return -1; }
        if (i->count == Z12_R_FDS) {
            /* Nettoyage obligatoire meme si une ABI inattendue depasse la borne. */
            z12_sysd_close_owned(&fd, &d->base.native);
            i->invalid = 1; return -1;
        }
        slot = i->count++; i->fds[slot] = fd;
        return (int)slot;
    }
    /* Uniquement le buffer controle de NOTRE recvmsg reel ; aucun CMSG client. */
    static void z12_r_inventory(struct msghdr *m, const unsigned char *bytes,
                                size_t capacity, Z12ReceiveInventory *i,
                                Z12ChronyReceiveDiag *d) {
        struct cmsghdr h;
        size_t total = m->msg_controllen, offset = 0, payload, step, k;
        const unsigned char *data;
        int fd, slot;
        if (total > capacity) {
            total = capacity; i->invalid = 1; d->cleanup_unverified = 1;
        }
        while (total - offset >= sizeof(h)) {
            memcpy(&h, bytes + offset, sizeof(h));
            if (h.cmsg_len < CMSG_LEN(0) || h.cmsg_len > total - offset) {
                i->invalid = 1; d->cleanup_unverified = 1; break;
            }
            payload = h.cmsg_len - CMSG_LEN(0);
            data = bytes + offset + CMSG_LEN(0);
            if (h.cmsg_level != SOL_SOCKET) i->invalid = 1;
            else if (h.cmsg_type == SCM_CREDENTIALS) {
                i->credential_count++;
                if (payload != sizeof(struct ucred) || i->credential_count != 1)
                    i->invalid = 1;
                else memcpy(&i->credentials, data, sizeof(i->credentials));
            } else if (h.cmsg_type == SCM_RIGHTS || h.cmsg_type == SCM_PIDFD) {
                if (payload % sizeof(int) != 0) i->invalid = 1;
                if (h.cmsg_type == SCM_RIGHTS) {
                    d->rights_seen++; i->invalid = 1;
                } else {
                    i->pidfd_count++;
                    if (payload != sizeof(int) || i->pidfd_count != 1) i->invalid = 1;
                }
                /* Inventorier aussi les entiers complets d'une taille inattendue. */
                for (k = 0; k < payload / sizeof(int); k++) {
                    memcpy(&fd, data + k * sizeof(int), sizeof(fd));
                    if (h.cmsg_type == SCM_PIDFD && !d->pidfd_delivery_present) {
                        d->pidfd_delivery_present = 1; d->pidfd_delivery_value = fd;
                    }
                    slot = z12_r_own_fd(i, fd, d);
                    if (h.cmsg_type == SCM_PIDFD && i->pidfd_count == 1 &&
                        payload == sizeof(int) && slot >= 0) i->peer_slot = slot;
                }
            } else i->invalid = 1;
            step = CMSG_ALIGN(h.cmsg_len);
            if (step < h.cmsg_len) {
                i->invalid = 1; d->cleanup_unverified = 1; break;
            }
            if (step > total - offset) break; /* Dernier en-tete sans padding complet. */
            offset += step;
        }
    }
    static int z12_chrony_datagram_destroy(Z12ChronyDatagram **pp,
                                           Z12ChronyReceiveDiag *d) {
        Z12ChronyDatagram *p;
        int closed;
        if (pp == NULL || d == NULL) return -2;
        p = *pp; if (p == NULL) return 0;
        *pp = NULL;
        closed = z12_sysd_close_owned(&p->peer_fd, &d->base.native);
        explicit_bzero(p, sizeof(*p)); free(p);
        return closed != 0 ? -1 : 0;
    }
    /* 1 paquet/faits ; 2 EAGAIN sans paquet ; 0 refus ; -1 erreur ; -2 contrat. */
    static int z12_chrony_receive(Z12ImageCtx *owner, int socket_fd,
            Z12ChronyDatagram **out, Z12ChronyReceiveDiag *diag) {
        union {
            struct cmsghdr alignment;
            unsigned char bytes[CMSG_SPACE(sizeof(struct ucred)) + CMSG_SPACE(sizeof(int)) +
                                CMSG_SPACE(Z12_R_RIGHTS * sizeof(int))];
        } control;
        unsigned char payload[Z12_R_WIRE];
        struct msghdr message = {0};
        struct iovec vector = {0};
        Z12ReceiveInventory inventory = {0};
        Z12ReceiveSocketFacts before, after;
        Z12ChronyDatagram *result = NULL;
        struct stat a, b;
        struct statfs afs, bfs;
        ssize_t count;
        int r, saved, peer = -1, duplicate = -1, cleanup = 0, wanted;
        size_t k;
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        diag->pidfd_delivery_value = -1;
        if (owner == NULL || socket_fd < 0 || out == NULL || *out != NULL) {
            diag->base.native.invalid_input = 1; return -2;
        }
        inventory.peer_slot = -1;
        for (k = 0; k < Z12_R_FDS; k++) inventory.fds[k] = -1;
        r = z12_r_socket(owner, socket_fd, &before, diag); if (r != 1) return r;
        memset(&control, 0, sizeof(control));
        vector.iov_base = payload; vector.iov_len = sizeof(payload);
        message.msg_iov = &vector; message.msg_iovlen = 1;
        message.msg_control = control.bytes; message.msg_controllen = sizeof(control.bytes);
        r = z12_r_guard(owner, diag); if (r != 1) return r;
        count = recvmsg(socket_fd, &message, MSG_CMSG_CLOEXEC|MSG_DONTWAIT|MSG_TRUNC);
        saved = errno;
        if (count < 0) {
            if (saved == EAGAIN || saved == EWOULDBLOCK) {
                diag->would_block = 1; diag->transient_errno = saved;
                r = z12_r_guard(owner, diag); if (r == 1) r = 2;
            } else {
                z12_sysd_first(&diag->base.native, Z12_SYSD_ERRNO, saved);
                r = z12_r_guard(owner, diag);
            }
            goto done;
        }
        /* Aucun retour ou garde avant l'inventaire des FD effectivement recus. */
        z12_r_inventory(&message, control.bytes, sizeof(control.bytes), &inventory, diag);
        diag->truncated = (message.msg_flags & (MSG_TRUNC|MSG_CTRUNC)) != 0;
        if (inventory.invalid || inventory.credential_count != 1 || inventory.pidfd_count != 1 ||
            inventory.peer_slot < 0 || inventory.credentials.pid <= 0 ||
            (size_t)count > sizeof(payload)) diag->ancillary_invalid = 1;
        r = z12_r_guard(owner, diag); if (r != 1) goto done;
        if (diag->truncated || diag->ancillary_invalid || diag->rights_seen || diag->cleanup_unverified) {
            r = 0; goto done;
        }
        peer = inventory.fds[inventory.peer_slot];
        r = z12_r_live(owner, peer, diag); if (r != 1) goto done;
        duplicate = pidfd_open(inventory.credentials.pid, 0);
        r = z12_r_post(owner, diag, duplicate); if (r != 1) goto done;
        r = z12_r_live(owner, duplicate, diag); if (r != 1) goto done;
        r = z12_r_statfs(owner, peer, &afs, diag); if (r != 1) goto done;
        r = z12_r_statfs(owner, duplicate, &bfs, diag); if (r != 1) goto done;
        if (afs.f_type != PID_FS_MAGIC || bfs.f_type != PID_FS_MAGIC) {
            diag->base.native.foreign_binding = 1; r = 0; goto done;
        }
        r = z12_r_stat(owner, peer, &a, diag); if (r != 1) goto done;
        r = z12_r_stat(owner, duplicate, &b, diag); if (r != 1) goto done;
        if (a.st_dev != b.st_dev || a.st_ino != b.st_ino) {
            diag->base.native.foreign_binding = 1; r = 0; goto done;
        }
        r = z12_r_live(owner, peer, diag); if (r != 1) goto done;
        r = z12_r_live(owner, duplicate, diag); if (r != 1) goto done;
        r = z12_r_socket(owner, socket_fd, &after, diag); if (r != 1) goto done;
        if (!z12_r_same_socket(&before, &after)) {
            diag->base.native.foreign_binding = 1; r = 0; goto done;
        }
        result = calloc(1, sizeof(*result));
        if (result != NULL) result->peer_fd = -1;
        r = z12_r_post(owner, diag, result != NULL ? 0 : -1);
        if (result == NULL || r != 1) goto done;
        memcpy(result->payload, payload, (size_t)count);
        result->length = (size_t)count;
        result->credentials = inventory.credentials;
        result->peer_dev = a.st_dev; result->peer_ino = a.st_ino;
        result->peer_fd = peer; inventory.fds[inventory.peer_slot] = -1;
        r = 1;
    done:
        cleanup |= z12_sysd_close_owned(&duplicate, &diag->base.native) != 0;
        for (k = 0; k < inventory.count; k++)
            cleanup |= z12_sysd_close_owned(&inventory.fds[k], &diag->base.native) != 0;
        wanted = r;
        if ((r == 1 || r == 2) && !cleanup) {
            r = z12_r_guard(owner, diag);
            if (r == 1) r = wanted;
        }
        r = z12_r_verdict(diag, cleanup ? -1 : r);
        if (r == 1) {
            result->observed_monotonic_ns = owner->deadline->last_seen_ns;
            *out = result; result = NULL;
        }
        if (result != NULL && z12_chrony_datagram_destroy(&result, diag) != 0) r = -1;
        return z12_r_verdict(diag, r);
    }
    """
    ctypedef struct Z12ImageCtx:
        pass
    ctypedef struct Z12ChronyDatagram:
        pass
    ctypedef struct Z12ChronyReceiveDiag:
        Z12ProcessImageDiag base
        int would_block
        int transient_errno
        int truncated
        int ancillary_invalid
        int cleanup_unverified
        int rights_seen
        int pidfd_delivery_present
        int pidfd_delivery_value
    int z12_chrony_receive(Z12ImageCtx *owner, int socket_fd,
        Z12ChronyDatagram **out, Z12ChronyReceiveDiag *diag)
    int z12_chrony_datagram_destroy(Z12ChronyDatagram **pp, Z12ChronyReceiveDiag *diag)
