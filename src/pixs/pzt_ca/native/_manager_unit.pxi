# Prive Z12 : observation manager/unite SELF, sans admission.
# Faits ponctuels : aucun gel des processus, aucune politique/autorite complete.
# Relation SELF/MainPID observee, admission explicite par proprietaire ulterieur.
# Champs copies bornes par politique ; allocations wire internes libsystemd TCB.
# Contexte exclusif au processus createur, jamais reutilise apres fork.
# Inclure APRES deadline, _launch_obs_sysd.pxi, _systemd_connection.pxi et _process_image.pxi, une fois ; build -D_GNU_SOURCE.
from libc.stddef cimport size_t
from libc.stdint cimport uint64_t, uint32_t

cdef extern from * nogil:
    r"""
    #include <errno.h>
    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>
    #include <limits.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <sys/ioctl.h>
    #include <sys/pidfd.h>
    #include <systemd/sd-bus.h>
    typedef Z12ProcessImageDiag Z12ManagerUnitDiag;
    typedef struct {
        char *object_path;
        char *unit_name;
        unsigned char invocation_id[16];
        uint32_t main_pid;
        pid_t self_pid;
        pid_t manager_pid;
        dev_t ns_dev;
        ino_t ns_ino;
        uint64_t observed_monotonic_ns;
    } Z12ManagerUnit;

    static int z12_unit_guard(Z12ImageCtx *x, Z12ManagerUnitDiag *d) {
        return z12_image_guard(x, (Z12ProcessImageDiag *)d);
    }
    static int z12_unit_verdict(Z12ManagerUnitDiag *d, int r) {
        return z12_image_verdict((Z12ProcessImageDiag *)d, r);
    }
    static int z12_unit_sig(Z12ImageCtx *x, sd_bus_message *m, const char *sig, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), s;
        if (r != 1) return r;
        s = sd_bus_message_has_signature(m, sig);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (s < 0) return -1;
        if (s == 0) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_atend(Z12ImageCtx *x, sd_bus_message *m, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), s;
        if (r != 1) return r;
        s = sd_bus_message_at_end(m, 1);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (s < 0) return -1;
        if (s == 0) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_return_type(Z12ImageCtx *x, sd_bus_message *m, Z12ManagerUnitDiag *d) {
        uint8_t type = 0;
        int code, r = z12_unit_guard(x, d);
        if (r != 1) return r;
        code = sd_bus_message_get_type(m, &type);
        if (code < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, code);
        r = z12_unit_guard(x, d); if (r != 1) return r;
        if (code < 0) return -1;
        if (type != SD_BUS_MESSAGE_METHOD_RETURN) {
            d->native.native_output_invalid = 1; return 0;
        }
        return 1;
    }
    static int z12_unit_remaining_us(Z12ImageCtx *x, Z12ManagerUnitDiag *d, uint64_t *us) {
        uint64_t now, rem;
        int r = z12_unit_guard(x, d);
        if (r != 1) return r;
        now = x->deadline->last_seen_ns;
        if (x->end <= now) { d->native.deadline_expired = 1; return 0; }
        rem = x->end - now;
        *us = rem / UINT64_C(1000);
        if (*us == 0) { d->native.deadline_expired = 1; return 0; }
        return 1;
    }
    static int z12_unit_new_call(Z12ImageCtx *x, const char *path, const char *iface,
                                 const char *member, sd_bus_message **mp, Z12ManagerUnitDiag *d) {
        sd_bus_message *m = NULL;
        int r = z12_unit_guard(x, d), s;
        if (r != 1) return r;
        if (mp == NULL || *mp != NULL) { d->native.invalid_input = 1; return -2; }
        s = sd_bus_message_new_method_call(x->bus, &m, NULL, path, iface, member);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) { if (m != NULL) sd_bus_message_unref(m); return r; }
        if (m == NULL) { d->native.native_output_invalid = 1; return 0; }
        s = sd_bus_message_set_auto_start(m, 0);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) { sd_bus_message_unref(m); return r; }
        if (s < 0) { sd_bus_message_unref(m); return -1; }
        s = sd_bus_message_set_allow_interactive_authorization(m, 0);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) { sd_bus_message_unref(m); return r; }
        if (s < 0) { sd_bus_message_unref(m); return -1; }
        *mp = m; return 1;
    }
    static int z12_unit_append_h(Z12ImageCtx *x, sd_bus_message *m, int fd, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), s;
        if (r != 1) return r;
        s = sd_bus_message_append(m, "h", fd);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (s < 0) return -1;
        return 1;
    }
    static int z12_unit_append_ss(Z12ImageCtx *x, sd_bus_message *m, const char *a, const char *b, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), s;
        if (r != 1) return r;
        s = sd_bus_message_append(m, "ss", a, b);
        if (s < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, s);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (s < 0) return -1;
        return 1;
    }
    static int z12_unit_call(Z12ImageCtx *x, sd_bus_message **mp, sd_bus_message **rp, Z12ManagerUnitDiag *d) {
        sd_bus_message *m;
        sd_bus_error err = SD_BUS_ERROR_NULL;
        uint64_t us = 0;
        int r;
        if (mp == NULL || *mp == NULL || rp == NULL || *rp != NULL) { d->native.invalid_input = 1; return -2; }
        m = *mp; *mp = NULL;
        r = z12_unit_remaining_us(x, d, &us);
        if (r != 1) { sd_bus_message_unref(m); return r; }
        r = sd_bus_call(x->bus, m, us, &err, rp);
        sd_bus_message_unref(m);
        if (r < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, r);
        sd_bus_error_free(&err);
        r = z12_unit_guard(x, d);
        if (r != 1) { if (*rp != NULL) { sd_bus_message_unref(*rp); *rp = NULL; } return r; }
        if (*rp == NULL) { d->native.native_output_invalid = 1; return 0; }
        r = z12_unit_return_type(x, *rp, d);
        if (r != 1) { sd_bus_message_unref(*rp); *rp = NULL; }
        return r;
    }
    static int z12_unit_read_os(Z12ImageCtx *x, sd_bus_message *m, const char **o, const char **s, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), q;
        if (r != 1) return r;
        q = sd_bus_message_read(m, "os", o, s);
        if (q < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, q);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (q < 0) return -1;
        if (q == 0 || *o == NULL || *s == NULL) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_read_ay(Z12ImageCtx *x, sd_bus_message *m, const void **p, size_t *n, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), q;
        if (r != 1) return r;
        q = sd_bus_message_read_array(m, 'y', p, n);
        if (q < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, q);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (q < 0) return -1;
        if (q == 0 || *p == NULL) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_enter(Z12ImageCtx *x, sd_bus_message *m, char t, const char *c, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), q;
        if (r != 1) return r;
        q = sd_bus_message_enter_container(m, t, c);
        if (q < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, q);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (q < 0) return -1;
        if (q == 0) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_exit(Z12ImageCtx *x, sd_bus_message *m, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), q;
        if (r != 1) return r;
        q = sd_bus_message_exit_container(m);
        if (q < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, q);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (q < 0) return -1;
        if (q != 1) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_read_u(Z12ImageCtx *x, sd_bus_message *m, uint32_t *v, Z12ManagerUnitDiag *d) {
        int r = z12_unit_guard(x, d), q;
        if (r != 1) return r;
        q = sd_bus_message_read(m, "u", v);
        if (q < 0) z12_sysd_first(&d->native, Z12_SYSD_LIBRARY, q);
        r = z12_unit_guard(x, d);
        if (r != 1) return r;
        if (q < 0) return -1;
        if (q == 0) { d->native.native_output_invalid = 1; return 0; }
        return 1;
    }
    static int z12_unit_copy(const char *src, size_t max_b, char **dst, Z12ImageCtx *x, Z12ManagerUnitDiag *d) {
        size_t n;
        int r;
        if (src == NULL || dst == NULL || *dst != NULL || max_b == 0 || max_b == SIZE_MAX) { d->native.invalid_input = 1; return -2; }
        r = z12_unit_guard(x, d); if (r != 1) return r;
        n = strnlen(src, max_b + 1);
        if (n == 0 || n > max_b || src[n] != '\0') { d->native.foreign_binding = 1; return 0; }
        r = z12_unit_guard(x, d); if (r != 1) return r;
        *dst = malloc(n + 1);
        if (*dst == NULL) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d);
        if (r != 1 || *dst == NULL) { free(*dst); *dst = NULL; return r != 1 ? r : -1; }
        memcpy(*dst, src, n + 1);
        return z12_unit_guard(x, d);
    }
    static int z12_unit_get_by_pidfd(Z12ImageCtx *x, int pidfd, size_t max_path, size_t max_unit,
                                     char **o, char **s, unsigned char inv[16], Z12ManagerUnitDiag *d) {
        static const char prefix[] = "/org/freedesktop/systemd1/unit/";
        sd_bus_message *m = NULL, *reply = NULL;
        const char *op = NULL, *un = NULL;
        const void *ay = NULL; size_t alen = 0;
        size_t plen = sizeof(prefix) - 1, n;
        int r;
        *o = NULL; *s = NULL;
        r = z12_unit_new_call(x, "/org/freedesktop/systemd1", "org.freedesktop.systemd1.Manager", "GetUnitByPIDFD", &m, d);
        if (r != 1) goto out;
        r = z12_unit_append_h(x, m, pidfd, d);
        if (r != 1) { sd_bus_message_unref(m); m = NULL; goto out; }
        r = z12_unit_call(x, &m, &reply, d); if (r != 1) goto out;
        r = z12_unit_sig(x, reply, "osay", d); if (r != 1) goto out;
        r = z12_unit_read_os(x, reply, &op, &un, d); if (r != 1) goto out;
        r = z12_unit_read_ay(x, reply, &ay, &alen, d); if (r != 1) goto out;
        r = z12_unit_atend(x, reply, d); if (r != 1) goto out;
        if (alen != 16 || ay == NULL) { d->native.native_output_invalid = 1; r = 0; goto out; }
        n = strnlen(op, max_path + 1);
        if (n == 0 || n > max_path || op[n] != '\0' || n <= plen ||
            memcmp(op, prefix, plen) != 0 ||
            memchr(op + plen, '/', n - plen) != NULL) {
            d->native.foreign_binding = 1; r = 0; goto out;
        }
        n = strnlen(un, max_unit + 1);
        if (n == 0 || n > max_unit || un[n] != '\0' ||
            memchr(un, '/', n) != NULL) {
            d->native.foreign_binding = 1; r = 0; goto out;
        }
        r = z12_unit_copy(op, max_path, o, x, d); if (r != 1) goto out;
        r = z12_unit_copy(un, max_unit, s, x, d);
        if (r != 1) { free(*o); *o = NULL; goto out; }
        memcpy(inv, ay, 16);
        {
            int z = 1, i;
            for (i = 0; i < 16; i++) if (inv[i] != 0) z = 0;
            if (z) { d->native.foreign_binding = 1; free(*o); *o = NULL; free(*s); *s = NULL; r = 0; goto out; }
        }
        r = 1;
    out:
        if (m != NULL) sd_bus_message_unref(m);
        if (reply != NULL) sd_bus_message_unref(reply);
        if (r == 1) r = z12_unit_guard(x, d);
        r = z12_unit_verdict(d, r);
        if (r != 1) { free(*o); *o = NULL; free(*s); *s = NULL; }
        return r;
    }
    static int z12_unit_get_mainpid(Z12ImageCtx *x, const char *obj, size_t max_path, uint32_t *pid, Z12ManagerUnitDiag *d) {
        sd_bus_message *m = NULL, *reply = NULL;
        uint32_t v = 0;
        size_t n;
        int r;
        r = z12_unit_guard(x, d); if (r != 1) return r;
        if (obj == NULL || max_path == 0 || max_path == SIZE_MAX) { d->native.invalid_input = 1; return -2; }
        n = strnlen(obj, max_path + 1);
        if (n == 0 || n > max_path || obj[n] != '\0') { d->native.foreign_binding = 1; return 0; }
        r = z12_unit_new_call(x, obj, "org.freedesktop.DBus.Properties", "Get", &m, d);
        if (r != 1) goto out;
        r = z12_unit_append_ss(x, m, "org.freedesktop.systemd1.Service", "MainPID", d);
        if (r != 1) { sd_bus_message_unref(m); m = NULL; goto out; }
        r = z12_unit_call(x, &m, &reply, d); if (r != 1) goto out;
        r = z12_unit_sig(x, reply, "v", d); if (r != 1) goto out;
        r = z12_unit_enter(x, reply, 'v', "u", d); if (r != 1) goto out;
        r = z12_unit_read_u(x, reply, &v, d); if (r != 1) goto out;
        r = z12_unit_exit(x, reply, d); if (r != 1) goto out;
        r = z12_unit_atend(x, reply, d); if (r != 1) goto out;
        if (v == 0 || v > (uint32_t)INT_MAX) { d->native.foreign_binding = 1; r = 0; goto out; }
        *pid = v; r = 1;
    out:
        if (m != NULL) sd_bus_message_unref(m);
        if (reply != NULL) sd_bus_message_unref(reply);
        if (r == 1) r = z12_unit_guard(x, d);
        return z12_unit_verdict(d, r);
    }
    static int z12_unit_get_invocation(Z12ImageCtx *x, const char *obj, size_t max_path, unsigned char inv[16], Z12ManagerUnitDiag *d) {
        sd_bus_message *m = NULL, *reply = NULL;
        const void *ay = NULL; size_t alen = 0, n;
        int r;
        r = z12_unit_guard(x, d); if (r != 1) return r;
        if (obj == NULL || max_path == 0 || max_path == SIZE_MAX) { d->native.invalid_input = 1; return -2; }
        n = strnlen(obj, max_path + 1);
        if (n == 0 || n > max_path || obj[n] != '\0') { d->native.foreign_binding = 1; return 0; }
        r = z12_unit_new_call(x, obj, "org.freedesktop.DBus.Properties", "Get", &m, d);
        if (r != 1) goto out;
        r = z12_unit_append_ss(x, m, "org.freedesktop.systemd1.Unit", "InvocationID", d);
        if (r != 1) { sd_bus_message_unref(m); m = NULL; goto out; }
        r = z12_unit_call(x, &m, &reply, d); if (r != 1) goto out;
        r = z12_unit_sig(x, reply, "v", d); if (r != 1) goto out;
        r = z12_unit_enter(x, reply, 'v', "ay", d); if (r != 1) goto out;
        r = z12_unit_read_ay(x, reply, &ay, &alen, d); if (r != 1) goto out;
        r = z12_unit_exit(x, reply, d); if (r != 1) goto out;
        r = z12_unit_atend(x, reply, d); if (r != 1) goto out;
        if (ay == NULL || alen != 16) { d->native.native_output_invalid = 1; r = 0; goto out; }
        memcpy(inv, ay, 16);
        {
            int z = 1, i;
            for (i = 0; i < 16; i++) if (inv[i] != 0) z = 0;
            if (z) { d->native.foreign_binding = 1; r = 0; goto out; }
            r = 1;
        }
    out:
        if (m != NULL) sd_bus_message_unref(m);
        if (reply != NULL) sd_bus_message_unref(reply);
        if (r == 1) r = z12_unit_guard(x, d);
        return z12_unit_verdict(d, r);
    }
    static int z12_unit_ns_fd(Z12ImageCtx *x, int pidfd, int *ns, Z12ManagerUnitDiag *d) {
        int fd = -1, flags, cleanup, r = z12_unit_guard(x, d);
        if (r != 1) return r;
        *ns = -1;
        fd = ioctl(pidfd, PIDFD_GET_PID_NAMESPACE, 0);
        if (fd < 0) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        flags = fcntl(fd, F_GETFD);
        if (flags < 0) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        if (flags < 0) { r = -1; goto done; }
        if ((flags & FD_CLOEXEC) == 0) {
            d->native.native_output_invalid = 1; r = 0; goto done;
        }
        *ns = fd; fd = -1;
    done:
        cleanup = z12_sysd_close_owned(&fd, &d->native) != 0;
        return z12_unit_verdict(d, cleanup ? -1 : r);
    }
    static int z12_unit_same_ns(Z12ImageCtx *x, int a, int b,
            struct stat *sa, struct stat *sb, Z12ManagerUnitDiag *d) {
        int na = -1, nb = -1, failed, r, cleanup = 0;
        r = z12_unit_ns_fd(x, a, &na, d); if (r != 1) goto done;
        r = z12_unit_ns_fd(x, b, &nb, d); if (r != 1) goto done;
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        failed = fstat(na, sa) != 0;
        if (failed) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        failed = fstat(nb, sb) != 0;
        if (failed) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        if (sa->st_dev != sb->st_dev || sa->st_ino != sb->st_ino) {
            d->native.foreign_binding = 1; r = 0;
        }
    done:
        /* Deux fermetures executees meme si la premiere echoue. */
        cleanup |= z12_sysd_close_owned(&na, &d->native) != 0;
        cleanup |= z12_sysd_close_owned(&nb, &d->native) != 0;
        if (r == 1 && !cleanup) r = z12_unit_guard(x, d);
        return z12_unit_verdict(d, cleanup ? -1 : r);
    }
    static int z12_unit_pidfd_open(Z12ImageCtx *x, pid_t pid, int *fd, Z12ManagerUnitDiag *d) {
        int owned = -1, flags, cleanup, r = z12_unit_guard(x, d);
        if (r != 1) return r;
        *fd = -1;
        owned = pidfd_open(pid, 0);
        if (owned < 0) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        flags = fcntl(owned, F_GETFD);
        if (flags < 0) z12_sysd_first(&d->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        if (flags < 0) { r = -1; goto done; }
        if ((flags & FD_CLOEXEC) == 0) {
            d->native.native_output_invalid = 1; r = 0; goto done;
        }
        r = z12_sysd_pidfd_live(owned, &d->native);
        if (r != 1) goto done;
        r = z12_unit_guard(x, d); if (r != 1) goto done;
        *fd = owned; owned = -1;
    done:
        cleanup = z12_sysd_close_owned(&owned, &d->native) != 0;
        return z12_unit_verdict(d, cleanup ? -1 : r);
    }
    static void z12_manager_unit_destroy(Z12ManagerUnit **pp) {
        if (pp != NULL && *pp != NULL) {
            free((*pp)->object_path); free((*pp)->unit_name);
            explicit_bzero(*pp, sizeof(**pp)); free(*pp); *pp = NULL;
        }
    }
    static int z12_manager_unit_collect(Z12SysdConn *c, size_t max_path_bytes, size_t max_unit_bytes,
            Z12ManagerUnit **out, Z12ManagerUnitDiag *diag) {
        Z12ImageCtx x = {0};
        Z12ManagerUnit *u = NULL;
        char *o1 = NULL, *s1 = NULL, *o2 = NULL, *s2 = NULL, *o3 = NULL, *s3 = NULL;
        unsigned char a1[16] = {0}, a2[16] = {0}, a3[16] = {0}, ap[16] = {0};
        struct stat nsa = {0}, nsb = {0}, nsa_end = {0}, nsb_end = {0};
        uint32_t mp1 = 0, mp2 = 0;
        int mfd = -1, r, cleanup = 0;
        if (diag == NULL) return -2;
        memset(diag, 0, sizeof(*diag));
        if (out == NULL || *out != NULL || c == NULL ||
            max_path_bytes == 0 || max_path_bytes == SIZE_MAX ||
            max_unit_bytes == 0 || max_unit_bytes == SIZE_MAX) {
            diag->native.invalid_input = 1; return -2;
        }
        r = z12_conn_guard(c, &diag->native); if (r != 1) return r;
        if (c->facts == NULL || c->bus == NULL) { diag->native.foreign_binding = 1; return 0; }
        x.conn = c; x.facts = c->facts; memcpy(&x.snapshot, c->facts, sizeof(x.snapshot));
        x.bus = c->bus; x.deadline = c->deadline; x.end = c->expected_end_ns;
        x.pidfd = x.snapshot.self_pidfd;
        r = z12_unit_same_ns(&x, x.snapshot.self_pidfd, x.snapshot.peer_pidfd, &nsa, &nsb, diag);
        if (r != 1) goto done;
        r = z12_unit_get_by_pidfd(&x, x.snapshot.self_pidfd, max_path_bytes, max_unit_bytes, &o1, &s1, a1, diag);
        if (r != 1) goto done;
        r = z12_unit_get_mainpid(&x, o1, max_path_bytes, &mp1, diag); if (r != 1) goto done;
        r = z12_unit_pidfd_open(&x, (pid_t)mp1, &mfd, diag); if (r != 1) goto done;
        r = z12_unit_get_by_pidfd(&x, mfd, max_path_bytes, max_unit_bytes, &o2, &s2, a2, diag);
        if (r != 1) goto done;
        if (strcmp(o1, o2) != 0 || strcmp(s1, s2) != 0 || memcmp(a1, a2, 16) != 0) {
            diag->native.foreign_binding = 1; r = 0; goto done;
        }
        r = z12_unit_get_invocation(&x, o1, max_path_bytes, ap, diag); if (r != 1) goto done;
        if (memcmp(a1, ap, 16) != 0) { diag->native.foreign_binding = 1; r = 0; goto done; }
        r = z12_unit_get_mainpid(&x, o1, max_path_bytes, &mp2, diag); if (r != 1) goto done;
        if (mp1 != mp2) { diag->native.foreign_binding = 1; r = 0; goto done; }
        r = z12_unit_get_by_pidfd(&x, x.snapshot.self_pidfd, max_path_bytes, max_unit_bytes, &o3, &s3, a3, diag);
        if (r != 1) goto done;
        if (strcmp(o1, o3) != 0 || strcmp(s1, s3) != 0 || memcmp(a1, a3, 16) != 0) {
            diag->native.foreign_binding = 1; r = 0; goto done;
        }
        r = z12_sysd_pidfd_live(mfd, &diag->native);
        if (r != 1) goto done;
        r = z12_unit_guard(&x, diag); if (r != 1) goto done;
        r = z12_unit_same_ns(&x, x.snapshot.self_pidfd, x.snapshot.peer_pidfd, &nsa_end, &nsb_end, diag);
        if (r != 1) goto done;
        if (nsa.st_dev != nsa_end.st_dev || nsa.st_ino != nsa_end.st_ino) {
            diag->native.foreign_binding = 1; r = 0; goto done;
        }
        u = calloc(1, sizeof(*u));
        if (u == NULL) z12_sysd_first(&diag->native, Z12_SYSD_ERRNO, errno);
        r = z12_unit_guard(&x, diag);
        if (r != 1 || u == NULL) goto done;
        u->object_path = o1; o1 = NULL; u->unit_name = s1; s1 = NULL;
        memcpy(u->invocation_id, a1, 16); u->main_pid = mp1;
        u->self_pid = x.snapshot.self_pid; u->manager_pid = x.snapshot.peer_pid;
        u->ns_dev = nsa.st_dev; u->ns_ino = nsa.st_ino;
        r = 1;
    done:
        cleanup |= z12_sysd_close_owned(&mfd, &diag->native) != 0;
        free(o1); free(s1); free(o2); free(s2); free(o3); free(s3);
        explicit_bzero(a1, 16); explicit_bzero(a2, 16); explicit_bzero(a3, 16); explicit_bzero(ap, 16);
        if (r == 1 && !cleanup) r = z12_unit_guard(&x, diag);
        r = z12_unit_verdict(diag, cleanup ? -1 : r);
        if (r == 1) { u->observed_monotonic_ns = x.deadline->last_seen_ns; *out = u; }
        else z12_manager_unit_destroy(&u);
        return r;
    }
    """
    ctypedef struct Z12ManagerUnit:
        pass
    ctypedef struct Z12ManagerUnitDiag:
        Z12SysdDiag native
        int openssl_failed
        int openssl_stage
        int openssl_code
    int z12_manager_unit_collect(Z12SysdConn *c, size_t max_path_bytes, size_t max_unit_bytes,
        Z12ManagerUnit **out, Z12ManagerUnitDiag *diag)
    void z12_manager_unit_destroy(Z12ManagerUnit **pp)
