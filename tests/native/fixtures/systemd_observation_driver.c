/* Conducteur de TEST : objets sd_bus fictifs, vrais sockets/pidfds locaux.
 * Aucun layout SDK de production n'est reproduit. Ne jamais livrer ce fichier.
 * Lier le module réel et ce conducteur avec --wrap pour les API sd_bus ci-dessous,
 * clock_gettime, close, poll et calloc. Aucune libsystemd réelle ni daemon.
 */
#define _GNU_SOURCE 1
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <sys/pidfd.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sched.h>
#include <linux/nsfs.h>
#include <systemd/sd-id128.h>
#include <systemd/sd-bus.h>
#include "systemd_observation.h"

struct sd_bus_slot;
struct sd_bus {
    int fd, other, refs, mode, created, ready, process_count;
    pid_t pid;
    uid_t uid;
    struct sd_bus_slot *pending;
};
struct sd_bus_message {
    int valid;
    int is_reply;
    int no_reply;
    int refcount;
    int fd;
    int fail;
    char path[256];
    char unit[256];
    uint8_t iid[16];
    char ifc[128];
    char mem[64];
    char arg0[128];
    char arg1[128];
    int kind;
    int entered;
    int consumed;
    int exited;
    uint32_t vu;
    uint8_t vay[16];
    char ros[256];
    char ros_unit[256];
    uint8_t ros_iid[16];
    int rkind;
};
struct sd_bus_slot {
    int valid;
    sd_bus *bus;
    sd_bus_message *query;
    sd_bus_message_handler_t cb;
    void *userdata;
    int delivered;
};
struct sd_bus_creds { sd_bus *owner; };

static int lk_async_mode;
static int lk_reply_mode;
static int lk_process_mode;
static unsigned lk_live_queries;
static unsigned lk_live_replies;
static unsigned lk_live_slots;
static unsigned lk_async_calls;
static unsigned lk_callbacks;
static unsigned lk_process_calls;
static int lk_mpid_main0;
static int lk_mpid_change;
static int lk_mpid_unit_main_alt;
static int lk_mpid_unit_self_alt;
static int lk_mpid_invoc_alt;
static int lk_mpid_sdk_err;
static int lk_mpid_type_mode;
static int lk_mpid_sig_mode;
static int lk_mpid_body_mode;
static int lk_mpid_variant_mode;
static int lk_mpid_suffix_mode;
static unsigned lk_mpid_n_main1;
static unsigned lk_mpid_n_unit_main;
static unsigned lk_mpid_n_unit_self;
static unsigned lk_mpid_n_main2;
static unsigned lk_mpid_n_invoc;
static unsigned lk_mpid_seq;
static unsigned lk_mpid_phase;
static int lk_mpid_hist[8];
static unsigned lk_mpid_hist_len;
static int lk_mpid_pid_override;
static int lk_mpid_iid_zero;
static int lk_mpid_ay15;
static int lk_ioctl_mode;
static unsigned lk_ioctl_calls;
#include <stdarg.h>
int __wrap_sd_bus_message_new_method_call(sd_bus *bus, sd_bus_message **ret, const char *destination, const char *path, const char *interface, const char *member);
sd_bus_message *__wrap_sd_bus_message_ref(sd_bus_message *m);
sd_bus_message *__wrap_sd_bus_message_unref(sd_bus_message *m);
int __wrap_sd_bus_message_set_auto_start(sd_bus_message *m, int b);
int __wrap_sd_bus_message_set_allow_interactive_authorization(sd_bus_message *m, int b);
int __wrap_sd_bus_message_append(sd_bus_message *m, const char *types, ...);
int __wrap_sd_bus_slot_set_floating(sd_bus_slot *slot, int b);
int __wrap_sd_bus_call_async(sd_bus *bus, sd_bus_slot **ret_slot, sd_bus_message *m, sd_bus_message_handler_t cb, void *userdata, uint64_t usec);
sd_bus_slot *__wrap_sd_bus_slot_unref(sd_bus_slot *slot);
void pa01_sysdtest_lookup_reset(void);
void pa01_sysdtest_lookup_mode(int async_mode, int reply_mode, int process_mode);
unsigned pa01_sysdtest_lookup_state(unsigned which);
void pa01_sysdtest_mpid_reset(void);
void pa01_sysdtest_mpid_mode(int main0, int change, int unit_main_alt, int unit_self_alt);
void pa01_sysdtest_mpid_mode2(int invoc_alt, int sdk_err, int type_mode, int sig_mode);
void pa01_sysdtest_mpid_mode3(int body_mode, int variant_mode, int suffix_mode);
unsigned pa01_sysdtest_mpid_state(unsigned which);
void pa01_sysdtest_mpid_main_pid(int pid);
void pa01_sysdtest_mpid_iid_modes(int zero, int ay15);
unsigned pa01_sysdtest_mpid_hist(unsigned idx);

int __real_close(int);
int __real_poll(struct pollfd *, nfds_t, int);
void *__real_calloc(size_t, size_t);
static uint64_t test_now = UINT64_C(1000000000);
static int clock_error, close_error, allocation_error;
static unsigned refs_added, refs_removed, creds_live, close_calls, api_calls;
static int poll_dead;
static int sdk_fail, sdk_result = 1, sdk_events = POLLOUT, connect_mode;
static unsigned sdk_ready_after = 2, sdk_news, sdk_setfds, sdk_starts;
static unsigned sdk_processes, sdk_closes, sdk_stage, sdk_connects, sdk_fd_closes, sdk_live;
static uint64_t sdk_timeout = UINT64_MAX, sdk_late;
static sd_bus *sdk_latest;
static void pa01_sysdtest_close_bus(sd_bus *);
int __real_connect(int, const struct sockaddr *, socklen_t);

void *__wrap_calloc(size_t count, size_t size) {
    if (allocation_error) {
        allocation_error = 0; errno = ENOMEM; return NULL;
    }
    return __real_calloc(count, size);
}
int __wrap_clock_gettime(clockid_t clock, struct timespec *out) {
    if (clock != CLOCK_MONOTONIC || clock_error || out == NULL) {
        errno = EIO; return -1;
    }
    out->tv_sec = (time_t)(test_now / UINT64_C(1000000000));
    out->tv_nsec = (long)(test_now % UINT64_C(1000000000));
    return 0;
}
int __wrap_close(int fd) {
    int r = __real_close(fd);
    close_calls++;
    if (r == 0 && close_error > 0) {
        close_error--; errno = EINTR; return -1;
    }
    return r;
}
int __wrap_poll(struct pollfd *fds, nfds_t count, int timeout) {
    if (poll_dead && count == 1 && timeout == 0) {
        fds[0].revents = POLLIN; return 1;
    }
    return __real_poll(fds, count, timeout);
}
void pa01_sysdtest_clock(uint64_t now, int fail) { test_now = now; clock_error = fail; }
void pa01_sysdtest_close_error(int count) { close_error = count; }
void pa01_sysdtest_alloc_error(void) { allocation_error = 1; }
void pa01_sysdtest_poll_dead(int value) { poll_dead = value; }
void pa01_sysdtest_reset(void) {
    test_now = UINT64_C(1000000000);
    clock_error = close_error = allocation_error = poll_dead = 0;
    refs_added = refs_removed = creds_live = close_calls = api_calls = 0;
    sdk_fail = connect_mode = 0; sdk_result = 1; sdk_events = POLLOUT;
    sdk_ready_after = 2; sdk_timeout = UINT64_MAX; sdk_late = 0;
    sdk_news = sdk_setfds = sdk_starts = sdk_processes = sdk_closes = sdk_stage = 0;
    sdk_connects = sdk_fd_closes = sdk_live = 0; sdk_latest = NULL;
    lk_async_mode = 0;
    lk_reply_mode = 0;
    lk_process_mode = 0;
    lk_live_queries = 0;
    lk_live_replies = 0;
    lk_live_slots = 0;
    lk_async_calls = 0;
    lk_callbacks = 0;
    lk_process_calls = 0;
    lk_ioctl_mode = 0;
    lk_ioctl_calls = 0;
    lk_mpid_main0 = 0;
    lk_mpid_change = 0;
    lk_mpid_unit_main_alt = 0;
    lk_mpid_unit_self_alt = 0;
    lk_mpid_invoc_alt = 0;
    lk_mpid_sdk_err = 0;
    lk_mpid_type_mode = 0;
    lk_mpid_sig_mode = 0;
    lk_mpid_body_mode = 0;
    lk_mpid_variant_mode = 0;
    lk_mpid_suffix_mode = 0;
    lk_mpid_n_main1 = 0;
    lk_mpid_n_unit_main = 0;
    lk_mpid_n_unit_self = 0;
    lk_mpid_n_main2 = 0;
    lk_mpid_n_invoc = 0;
    lk_mpid_seq = 0;
    lk_mpid_phase = 0;
    lk_mpid_hist_len = 0;
    memset(lk_mpid_hist, 0, sizeof lk_mpid_hist);
    lk_mpid_pid_override = 0;
    lk_mpid_iid_zero = 0;
    lk_mpid_ay15 = 0;
}
unsigned pa01_sysdtest_count(unsigned which) {
    switch (which) {
    case 0: return refs_added;
    case 1: return refs_removed;
    case 2: return creds_live;
    case 3: return close_calls;
    case 4: return api_calls;
    case 5: return sdk_news;
    case 6: return sdk_setfds;
    case 7: return sdk_starts;
    case 8: return sdk_processes;
    case 9: return sdk_closes;
    case 10: return sdk_stage;
    case 11: return sdk_connects;
    case 12: return sdk_fd_closes;
    case 13: return sdk_live;
    default: return UINT32_MAX;
    }
}
void *pa01_sysdtest_new(int mode) {
    sd_bus *b = __real_calloc(1, sizeof(*b));
    int pair[2] = {-1, -1};
    if (b == NULL) return NULL;
    if (socketpair(AF_UNIX,
            (mode == 14 ? SOCK_DGRAM : SOCK_STREAM) | SOCK_CLOEXEC, 0, pair) != 0) {
        free(b); return NULL;
    }
    b->fd = pair[0]; b->other = pair[1]; b->refs = 1;
    b->pid = getpid(); b->uid = geteuid(); b->mode = mode;
    return b;
}
int pa01_sysdtest_free(void *pointer) {
    sd_bus *b = pointer;
    int r1, r2;
    if (b == NULL || b->refs != 1) return -1;
    r1 = __real_close(b->fd); r2 = __real_close(b->other);
    free(b);
    return r1 == 0 && r2 == 0 ? 0 : -1;
}
void pa01_sysdtest_mode(void *pointer, int mode) { ((sd_bus *)pointer)->mode = mode; }
int pa01_sysdtest_replace(void *pointer) {
    sd_bus *b = pointer;
    int pair[2];
    if (socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0, pair) != 0) return -1;
    if (__real_close(b->fd) != 0 || (b->other >= 0 && __real_close(b->other) != 0)) {
        __real_close(pair[0]); __real_close(pair[1]); return -1;
    }
    b->fd = pair[0]; b->other = pair[1];
    return 0;
}
sd_bus *__wrap_sd_bus_ref(sd_bus *b) {
    api_calls++; refs_added++; b->refs++; return b;
}
sd_bus *__wrap_sd_bus_unref(sd_bus *b) {
    api_calls++; refs_removed++; b->refs--;
    if (b->created && b->refs == 0) {
        pa01_sysdtest_close_bus(b);
        if (sdk_latest == b) sdk_latest = NULL;
        sdk_live--; free(b);
    }
    return NULL;
}
int __wrap_sd_bus_is_ready(sd_bus *b) { api_calls++; return b->mode == 1 ? 0 : (b->created ? b->ready : 1); }
int __wrap_sd_bus_is_bus_client(sd_bus *b) { api_calls++; return b->mode == 2; }
int __wrap_sd_bus_is_server(sd_bus *b) { api_calls++; return b->mode == 3; }
int __wrap_sd_bus_get_fd(sd_bus *b) { api_calls++; return b->fd; }
int __wrap_sd_bus_get_owner_creds(sd_bus *b, uint64_t mask, sd_bus_creds **out) {
    sd_bus_creds *c;
    (void)mask; api_calls++;
    c = __real_calloc(1, sizeof(*c));
    if (c == NULL) return -ENOMEM;
    c->owner = b; *out = c; creds_live++;
    return b->mode == 8 ? -EIO : 0;
}
uint64_t __wrap_sd_bus_creds_get_mask(const sd_bus_creds *c) {
    uint64_t mask = SD_BUS_CREDS_PID | SD_BUS_CREDS_EUID | SD_BUS_CREDS_PIDFD;
    api_calls++;
    return c->owner->mode == 5 ? mask & ~SD_BUS_CREDS_PIDFD : mask;
}
uint64_t __wrap_sd_bus_creds_get_augmented_mask(const sd_bus_creds *c) {
    api_calls++; return c->owner->mode == 4 ? SD_BUS_CREDS_PID : 0;
}
int __wrap_sd_bus_creds_get_pid(sd_bus_creds *c, pid_t *out) {
    api_calls++; *out = c->owner->pid + (c->owner->mode == 6 ? 1 : 0); return 0;
}
int __wrap_sd_bus_creds_get_euid(sd_bus_creds *c, uid_t *out) {
    api_calls++;
    *out = c->owner->uid ^ (c->owner->mode == 7 ? (uid_t)1 : 0);
    return 0;
}
int __wrap_sd_bus_creds_get_pidfd_dup(sd_bus_creds *c, int *out) {
    int fd;
    api_calls++;
    fd = pidfd_open(c->owner->pid, 0);
    if (fd < 0) return -errno;
    *out = fd;
    if (c->owner->mode == 12 && fcntl(fd, F_SETFD, 0) != 0) return -errno;
    return c->owner->mode == 9 ? -EIO : 0;
}
sd_bus_creds *__wrap_sd_bus_creds_unref(sd_bus_creds *c) {
    api_calls++; creds_live--; free(c); return NULL;
}

void *pa01_sysdtest_default(unsigned which) {
    if (which == 0) return SD_BUS_DEFAULT;
    if (which == 1) return SD_BUS_DEFAULT_USER;
    return SD_BUS_DEFAULT_SYSTEM;
}

/* Extensions de TEST du constructeur propre : aucune authentification SDK réelle. */
static int pa01_sysdtest_setup(unsigned stage) {
    api_calls++; sdk_stage = stage;
    return sdk_fail == (int)stage ? -EIO : 0;
}
void pa01_sysdtest_conn_options(int fail, int result, unsigned after, int events,
                                uint64_t timeout, int connect, uint64_t late) {
    sdk_fail = fail; sdk_result = result; sdk_ready_after = after; sdk_events = events;
    sdk_timeout = timeout; connect_mode = connect; sdk_late = late; sdk_stage = 0;
}
void pa01_sysdtest_timeout(uint64_t value) { sdk_timeout = value; }
void *pa01_sysdtest_latest(void) { return sdk_latest; }
size_t pa01_sysdtest_path_limit(void) { struct sockaddr_un a; return sizeof(a.sun_path); }
int __wrap_connect(int fd, const struct sockaddr *address, socklen_t size) {
    int r;
    sdk_connects++;
    if (connect_mode == 2) { errno = EAGAIN; return -1; }
    r = __real_connect(fd, address, size);
    if (r == 0 && connect_mode == 1) { errno = EINPROGRESS; return -1; }
    return r;
}
static void pa01_sysdtest_close_bus(sd_bus *b) {
    if (b->fd >= 0) { __real_close(b->fd); sdk_fd_closes++; b->fd = -1; }
    if (b->other >= 0) { __real_close(b->other); sdk_fd_closes++; b->other = -1; }
}
int __wrap_sd_bus_new(sd_bus **out) {
    sd_bus *b = __real_calloc(1, sizeof(*b));
    int status = pa01_sysdtest_setup(1);
    if (b == NULL) return -ENOMEM;
    b->fd = b->other = -1; b->refs = 1; b->created = 1;
    b->pid = getpid(); b->uid = geteuid(); *out = b;
    sdk_latest = b; sdk_news++; sdk_live++; refs_added++;
    return status; /* Sortie allouée même sur erreur : vérifier le cleanup. */
}
int __wrap_sd_bus_set_fd(sd_bus *b, int input, int output) {
    struct ucred peer;
    socklen_t size = sizeof(peer);
    int status = pa01_sysdtest_setup(2);
    sdk_setfds++;
    if (status < 0) return status; /* Pas de transfert sur échec. */
    if (input < 0 || input != output) return -EBADF;
    if (getsockopt(input, SOL_SOCKET, SO_PEERCRED, &peer, &size) != 0) return -errno;
    if (size != sizeof(peer)) return -EPROTO;
    b->fd = input; b->pid = peer.pid; b->uid = peer.uid;
    if (sdk_late != 0) test_now = sdk_late;
    return 0;
}
int __wrap_sd_bus_set_bus_client(sd_bus *b, int value) {
    (void)b;
    return value == 0 ? pa01_sysdtest_setup(3) : -EINVAL;
}
int __wrap_sd_bus_set_server(sd_bus *b, int value, sd_id128_t id) {
    sd_id128_t empty = SD_ID128_NULL;
    (void)b;
    return value == 0 && memcmp(&id, &empty, sizeof(id)) == 0
        ? pa01_sysdtest_setup(4) : -EINVAL;
}
int __wrap_sd_bus_set_anonymous(sd_bus *b, int value) {
    (void)b;
    return value == 0 ? pa01_sysdtest_setup(5) : -EINVAL;
}
int __wrap_sd_bus_set_allow_interactive_authorization(sd_bus *b, int value) {
    (void)b;
    return value == 0 ? pa01_sysdtest_setup(6) : -EINVAL;
}
int __wrap_sd_bus_set_exit_on_disconnect(sd_bus *b, int value) {
    (void)b;
    return value == 0 ? pa01_sysdtest_setup(7) : -EINVAL;
}
int __wrap_sd_bus_set_close_on_exit(sd_bus *b, int value) {
    (void)b;
    return value == 1 ? pa01_sysdtest_setup(8) : -EINVAL;
}
int __wrap_sd_bus_negotiate_fds(sd_bus *b, int value) {
    (void)b;
    return value == 1 ? pa01_sysdtest_setup(9) : -EINVAL;
}
int __wrap_sd_bus_negotiate_creds(sd_bus *b, int value, uint64_t mask) {
    uint64_t need = SD_BUS_CREDS_PID | SD_BUS_CREDS_EUID | SD_BUS_CREDS_PIDFD;
    (void)b;
    return value == 1 && mask == need ? pa01_sysdtest_setup(10) : -EINVAL;
}
int __wrap_sd_bus_start(sd_bus *b) { (void)b; sdk_starts++; return pa01_sysdtest_setup(11); }
int __wrap_sd_bus_process(sd_bus *b, sd_bus_message **message) {
    sd_bus_slot *slot;
    sd_bus_message *q;
    sd_bus_message *reply;
    sd_bus_message_handler_t cb;
    void *ud;
    int cb_rc;
    static const uint8_t k_iid[16] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
    static const uint8_t k_iid_alt[16] = {16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1};
    api_calls++; sdk_processes++; b->process_count++;
    lk_process_calls++;
    if (message != NULL) *message = NULL;
    if (sdk_result < 0) return sdk_result;
    if (sdk_result > 0 && (unsigned)b->process_count >= sdk_ready_after) b->ready = 1;
    slot = b->pending;
    if (!slot || !slot->valid || slot->delivered) return sdk_result;
    if (!slot->query || !slot->query->valid || slot->query->no_reply) return sdk_result;
    if (lk_process_mode != 0) return sdk_result;
    if (lk_async_mode != 0) return sdk_result;
    if (lk_mpid_sdk_err == 2) return -EIO;
    q = slot->query;
    reply = __real_calloc(1, sizeof *reply);
    if (!reply) return -ENOMEM;
    reply->valid = 1;
    reply->is_reply = 1;
    reply->no_reply = 0;
    reply->refcount = 1;
    reply->fd = -1;
    reply->fail = (lk_reply_mode == 2) ? 1 : 0;
    reply->entered = 0;
    reply->consumed = 0;
    reply->exited = 0;
    reply->vu = 0;
    memset(reply->vay, 0, sizeof reply->vay);
    reply->ros[0] = '\0';
    reply->ros_unit[0] = '\0';
    memset(reply->ros_iid, 0, sizeof reply->ros_iid);
    reply->rkind = 0;
    reply->path[0] = '\0';
    reply->unit[0] = '\0';
    memset(reply->iid, 0, sizeof reply->iid);
    if (q->kind == 1) {
        int is_second = (lk_mpid_n_main2 > 0) ? 1 : 0;
        uint32_t base = lk_mpid_pid_override != 0 ? (uint32_t)lk_mpid_pid_override : (uint32_t)getpid();
        uint32_t v = base;
        if (!is_second && lk_mpid_main0) v = 0;
        else if (is_second && lk_mpid_change) v = base + 1;
        reply->rkind = 1;
        reply->vu = v;
    } else if (q->kind == 3) {
        reply->rkind = 2;
        if (lk_mpid_iid_zero) memset(reply->vay, 0, sizeof reply->vay);
        else if (lk_mpid_invoc_alt) memcpy(reply->vay, k_iid_alt, sizeof reply->vay);
        else memcpy(reply->vay, k_iid, sizeof reply->vay);
    } else if (q->kind == 2) {
        int is_self = (lk_mpid_n_unit_self > 0) ? 1 : 0;
        int alt = is_self ? lk_mpid_unit_self_alt : lk_mpid_unit_main_alt;
        reply->rkind = 0;
        if (alt == 1) {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/alt_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "alt.service");
            memcpy(reply->ros_iid, k_iid, sizeof reply->ros_iid);
        } else if (alt == 2) {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/test_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "alt.service");
            memcpy(reply->ros_iid, k_iid, sizeof reply->ros_iid);
        } else if (alt == 3) {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/test_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "test.service");
            memcpy(reply->ros_iid, k_iid_alt, sizeof reply->ros_iid);
        } else if (lk_reply_mode == 1) {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/alt_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "alt.service");
            memcpy(reply->ros_iid, k_iid, sizeof reply->ros_iid);
        } else {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/test_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "test.service");
            memcpy(reply->ros_iid, k_iid, sizeof reply->ros_iid);
        }
        snprintf(reply->path, sizeof reply->path, "%s", reply->ros);
        snprintf(reply->unit, sizeof reply->unit, "%s", reply->ros_unit);
        memcpy(reply->iid, reply->ros_iid, sizeof reply->iid);
    } else {
        reply->rkind = 0;
        if (lk_reply_mode == 1) {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/alt_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "alt.service");
        } else {
            snprintf(reply->ros, sizeof reply->ros, "/org/freedesktop/systemd1/unit/test_2eservice");
            snprintf(reply->ros_unit, sizeof reply->ros_unit, "test.service");
        }
        memcpy(reply->ros_iid, k_iid, sizeof reply->ros_iid);
        snprintf(reply->path, sizeof reply->path, "%s", reply->ros);
        snprintf(reply->unit, sizeof reply->unit, "%s", reply->ros_unit);
        memcpy(reply->iid, reply->ros_iid, sizeof reply->iid);
    }
    lk_live_replies++;
    slot->delivered = 1;
    cb = slot->cb;
    ud = slot->userdata;
    cb_rc = cb(reply, ud, NULL);
    (void)cb_rc;
    lk_callbacks++;
    __wrap_sd_bus_message_unref(reply);
    return 1;
}
int __wrap_sd_bus_get_events(sd_bus *b) { (void)b; api_calls++; return sdk_events; }
int __wrap_sd_bus_get_timeout(sd_bus *b, uint64_t *out) {
    (void)b; api_calls++; *out = sdk_timeout; return 0;
}
sd_bus *__wrap_sd_bus_close_unref(sd_bus *b) {
    api_calls++; sdk_closes++;
    pa01_sysdtest_close_bus(b);
    return __wrap_sd_bus_unref(b);
}

int __wrap_sd_bus_message_new_method_call(sd_bus *bus, sd_bus_message **ret, const char *destination, const char *path, const char *interface, const char *member) {
    sd_bus_message *m;
    api_calls++;
    if (!bus || !ret) return -EINVAL;
    if (destination != NULL) return -EINVAL;
    if (!path || !interface || !member) return -EINVAL;
    if (strcmp(interface, "org.freedesktop.DBus.Properties") == 0 && strcmp(member, "Get") == 0) {
        if (strcmp(path, "/org/freedesktop/systemd1/unit/test_2eservice") != 0) return -EINVAL;
    } else if (strcmp(interface, "org.freedesktop.systemd1.Manager") == 0 && strcmp(member, "GetUnitByPIDFD") == 0) {
        if (strcmp(path, "/org/freedesktop/systemd1") != 0) return -EINVAL;
    } else {
        return -EINVAL;
    }
    m = __real_calloc(1, sizeof *m);
    if (!m) return -ENOMEM;
    m->valid = 1;
    m->is_reply = 0;
    m->no_reply = 0;
    m->refcount = 1;
    m->fd = -1;
    m->fail = 0;
    snprintf(m->path, sizeof m->path, "%s", path);
    m->unit[0] = '\0';
    memset(m->iid, 0, sizeof m->iid);
    snprintf(m->ifc, sizeof m->ifc, "%s", interface);
    snprintf(m->mem, sizeof m->mem, "%s", member);
    m->arg0[0] = '\0';
    m->arg1[0] = '\0';
    m->kind = 0;
    m->entered = 0;
    m->consumed = 0;
    m->exited = 0;
    m->rkind = 0;
    lk_live_queries++;
    *ret = m;
    return 0;
}

sd_bus_message *__wrap_sd_bus_message_ref(sd_bus_message *m) {
    api_calls++;
    if (!m || !m->valid) return NULL;
    if (m->refcount <= 0) return NULL;
    m->refcount++;
    return m;
}
sd_bus_message *__wrap_sd_bus_message_unref(sd_bus_message *m) {
    api_calls++;
    if (!m || !m->valid) return NULL;
    if (m->refcount <= 0) return NULL;
    m->refcount--;
    if (m->refcount > 0) return NULL;
    if (m->fd >= 0) { __real_close(m->fd); m->fd = -1; }
    if (m->is_reply) { if (lk_live_replies > 0) lk_live_replies--; }
    else { if (lk_live_queries > 0) lk_live_queries--; }
    m->valid = 0;
    free(m);
    return NULL;
}

int __wrap_sd_bus_message_set_auto_start(sd_bus_message *m, int b) {
    api_calls++;
    if (!m || !m->valid) return -EINVAL;
    if (b != 0) return -EINVAL;
    return 0;
}
int __wrap_sd_bus_message_set_allow_interactive_authorization(sd_bus_message *m, int b) {
    api_calls++;
    if (!m || !m->valid) return -EINVAL;
    if (b != 0) return -EINVAL;
    return 0;
}
int __wrap_sd_bus_message_append(sd_bus_message *m, const char *types, ...) {
    va_list ap;
    api_calls++;
    if (!m || !m->valid) return -EINVAL;
    if (!types) return -EINVAL;
    if (strcmp(types, "h") == 0) {
        int fd;
        int dupfd;
        if (strcmp(m->mem, "GetUnitByPIDFD") != 0) return -EINVAL;
        if (strcmp(m->ifc, "org.freedesktop.systemd1.Manager") != 0) return -EINVAL;
        va_start(ap, types);
        fd = va_arg(ap, int);
        va_end(ap);
        if (fd < 0) return -EBADF;
        dupfd = fcntl(fd, F_DUPFD_CLOEXEC, 3);
        if (dupfd < 0) return -errno;
        if (m->fd >= 0) __real_close(m->fd);
        m->fd = dupfd;
        m->kind = 2;
        return 0;
    }
    if (strcmp(types, "ss") == 0) {
        const char *a0;
        const char *a1;
        if (strcmp(m->mem, "Get") != 0) return -EINVAL;
        if (strcmp(m->ifc, "org.freedesktop.DBus.Properties") != 0) return -EINVAL;
        va_start(ap, types);
        a0 = va_arg(ap, const char *);
        a1 = va_arg(ap, const char *);
        va_end(ap);
        if (!a0 || !a1) return -EINVAL;
        if (!((strcmp(a0, "org.freedesktop.systemd1.Service") == 0 && strcmp(a1, "MainPID") == 0) || (strcmp(a0, "org.freedesktop.systemd1.Unit") == 0 && strcmp(a1, "InvocationID") == 0))) return -EINVAL;
        snprintf(m->arg0, sizeof m->arg0, "%s", a0);
        snprintf(m->arg1, sizeof m->arg1, "%s", a1);
        if (strcmp(a1, "MainPID") == 0) m->kind = 1;
        else m->kind = 3;
        return 0;
    }
    return -EINVAL;
}
int __wrap_sd_bus_slot_set_floating(sd_bus_slot *slot, int b) {
    api_calls++;
    if (!slot || !slot->valid) return -EINVAL;
    if (b != 0) return -EINVAL;
    return 0;
}

int __wrap_sd_bus_call_async(sd_bus *bus, sd_bus_slot **ret_slot, sd_bus_message *m, sd_bus_message_handler_t cb, void *userdata, uint64_t usec) {
    sd_bus_slot *slot;
    api_calls++;
    if (!bus || !ret_slot || !m || !m->valid || !cb) return -EINVAL;
    if (usec == 0) return -EINVAL;
    if (lk_async_mode == 1) return -ETIMEDOUT;
    if (lk_async_mode == 2) return -EIO;
    if (lk_mpid_sdk_err == 1) return -EIO;
    if (bus->pending && bus->pending->valid) return -EBUSY;
    if (m->kind == 2) {
        if (m->fd < 0) return -EBADF;
    } else if (m->kind == 1 || m->kind == 3) {
        if (m->arg0[0] == '\0' || m->arg1[0] == '\0') return -EINVAL;
    } else {
        return -EINVAL;
    }
    slot = __real_calloc(1, sizeof *slot);
    if (!slot) return -ENOMEM;
    slot->bus = __wrap_sd_bus_ref(bus);
    if (!slot->bus) { free(slot); return -ENOMEM; }
    slot->query = __wrap_sd_bus_message_ref(m);
    if (!slot->query) { __wrap_sd_bus_unref(slot->bus); free(slot); return -ENOMEM; }
    slot->valid = 1;
    slot->cb = cb;
    slot->userdata = userdata;
    slot->delivered = 0;
    bus->pending = slot;
    lk_live_slots++;
    lk_async_calls++;
    lk_mpid_seq++;
    if (m->kind == 1) {
        if (lk_mpid_n_main1 == 0) lk_mpid_n_main1++;
        else lk_mpid_n_main2++;
    } else if (m->kind == 2) {
        if (lk_mpid_n_unit_main == 0) lk_mpid_n_unit_main++;
        else lk_mpid_n_unit_self++;
    } else if (m->kind == 3) {
        lk_mpid_n_invoc++;
    }
    lk_mpid_phase = lk_mpid_seq;
    if (lk_mpid_hist_len < 8) lk_mpid_hist[lk_mpid_hist_len++] = m->kind;
    *ret_slot = slot;
    return 0;
}

sd_bus_slot *__wrap_sd_bus_slot_unref(sd_bus_slot *slot) {
    api_calls++;
    if (!slot || !slot->valid) return NULL;
    if (slot->bus && slot->bus->pending == slot) slot->bus->pending = NULL;
    slot->valid = 0;
    slot->cb = NULL;
    slot->userdata = NULL;
    if (slot->query) { __wrap_sd_bus_message_unref(slot->query); slot->query = NULL; }
    if (slot->bus) { __wrap_sd_bus_unref(slot->bus); slot->bus = NULL; }
    free(slot);
    if (lk_live_slots > 0) lk_live_slots--;
    return NULL;
}

int __wrap_sd_bus_message_get_type(sd_bus_message *m, uint8_t *type) {
    api_calls++;
    if (!m || !m->valid || !type) return -EINVAL;
    if (m->refcount <= 0) return -EINVAL;
    if (!m->is_reply || m->fail) return -EIO;
    if (lk_mpid_type_mode != 0) {
        *type = (uint8_t)SD_BUS_MESSAGE_METHOD_ERROR;
        return 0;
    }
    *type = (uint8_t)SD_BUS_MESSAGE_METHOD_RETURN;
    return 0;
}
int __wrap_sd_bus_message_has_signature(sd_bus_message *m, const char *signature) {
    api_calls++;
    if (!m || !m->valid || !signature) return 0;
    if (!m->is_reply || m->fail) return 0;
    if (lk_mpid_sig_mode != 0) return 0;
    if (m->rkind == 0) return strcmp(signature, "osay") == 0 ? 1 : 0;
    return strcmp(signature, "v") == 0 ? 1 : 0;
}
int __wrap_sd_bus_message_read(sd_bus_message *m, const char *types, ...) {
    va_list ap;
    api_calls++;
    if (!m || !m->valid || !types) return -EINVAL;
    if (!m->is_reply || m->fail) return -EIO;
    if (lk_mpid_body_mode != 0) return 0;
    if (strcmp(types, "u") == 0) {
        uint32_t *out;
        if (m->rkind != 1) return -EINVAL;
        if (!m->entered || m->exited || m->consumed) return -EINVAL;
        va_start(ap, types);
        out = va_arg(ap, uint32_t *);
        va_end(ap);
        if (!out) return -EINVAL;
        *out = m->vu;
        m->consumed = 1;
        return 1;
    }
    if (strcmp(types, "os") == 0) {
        const char **out_path;
        const char **out_unit;
        if (m->rkind != 0) return -EINVAL;
        if (m->consumed != 0) return -EINVAL;
        if (m->ros[0] == '\0' || m->ros_unit[0] == '\0') return -EIO;
        va_start(ap, types);
        out_path = va_arg(ap, const char **);
        out_unit = va_arg(ap, const char **);
        va_end(ap);
        if (!out_path || !out_unit) return -EINVAL;
        *out_path = m->ros;
        *out_unit = m->ros_unit;
        m->consumed = 1;
        return 1;
    }
    return -EINVAL;
}
int __wrap_sd_bus_message_read_array(sd_bus_message *m, char type, const void **ptr, size_t *size) {
    api_calls++;
    if (!m || !m->valid || !ptr || !size) return -EINVAL;
    if (!m->is_reply || m->fail) return -EIO;
    if (lk_mpid_body_mode != 0) return 0;
    if (type != 'y') return -EINVAL;
    if (m->rkind == 2) {
        if (!m->entered || m->exited || m->consumed) return -EINVAL;
        *ptr = m->vay;
        *size = lk_mpid_ay15 ? 15 : sizeof m->vay;
        m->consumed = 1;
        return 1;
    }
    if (m->rkind == 0) {
        if (m->consumed != 1) return -EINVAL;
        *ptr = m->ros_iid;
        *size = sizeof m->ros_iid;
        m->consumed = 2;
        return 1;
    }
    return -EINVAL;
}
int __wrap_sd_bus_message_at_end(sd_bus_message *m, int complete) {
    api_calls++;
    if (!m || !m->valid) return 0;
    if (!m->is_reply || m->fail) return 0;
    if (m->rkind == 1 || m->rkind == 2) {
        if (!m->entered) return 0;
        if (!m->consumed) return 0;
        if (!m->exited) {
            if (complete) return 0;
            return 1;
        }
        if (lk_mpid_suffix_mode != 0) return 0;
        return 1;
    }
    if (m->rkind == 0) {
        if (m->consumed != 2) return 0;
        if (lk_mpid_suffix_mode != 0) return 0;
        return 1;
    }
    return 0;
}

int __wrap_sd_bus_message_enter_container(sd_bus_message *m, char type, const char *contents) {
    api_calls++;
    if (!m || !m->valid || !contents) return -EINVAL;
    if (!m->is_reply || m->fail) return -EIO;
    if (lk_mpid_variant_mode != 0) return 0;
    if (type != 'v') return -EINVAL;
    if (m->rkind == 1) {
        if (strcmp(contents, "u") != 0) return -EINVAL;
        if (m->entered) return -EINVAL;
        m->entered = 1;
        m->consumed = 0;
        m->exited = 0;
        return 1;
    }
    if (m->rkind == 2) {
        if (strcmp(contents, "ay") != 0) return -EINVAL;
        if (m->entered) return -EINVAL;
        m->entered = 1;
        m->consumed = 0;
        m->exited = 0;
        return 1;
    }
    return -EINVAL;
}
int __wrap_sd_bus_message_exit_container(sd_bus_message *m) {
    api_calls++;
    if (!m || !m->valid) return -EINVAL;
    if (!m->is_reply || m->fail) return -EIO;
    if (m->rkind != 1 && m->rkind != 2) return -EINVAL;
    if (!m->entered || m->exited) return -EINVAL;
    if (!m->consumed) return -EINVAL;
    m->exited = 1;
    return 1;
}

int __wrap_ioctl(int fd, unsigned long request, ...) {
    api_calls++;
    lk_ioctl_calls++;
    if (request == (unsigned long)PIDFD_GET_PID_NAMESPACE) {
        int nsfd;
        if (fd < 0) { errno = EBADF; return -1; }
        if (lk_ioctl_mode == 1) { errno = ENOTTY; return -1; }
        if (lk_ioctl_mode == 2 && (lk_ioctl_calls % 2) == 0) nsfd = open("/dev/zero", O_RDONLY | O_CLOEXEC);
        else nsfd = open("/dev/null", O_RDONLY | O_CLOEXEC);
        if (nsfd < 0) return -1;
        return nsfd;
    }
    if (request == (unsigned long)NS_GET_NSTYPE) {
        if (fd < 0) { errno = EBADF; return -1; }
        if (lk_ioctl_mode == 1) { errno = ENOTTY; return -1; }
        if (lk_ioctl_mode == 3) return CLONE_NEWNET;
        return CLONE_NEWPID;
    }
    errno = ENOTTY;
    return -1;
}
void pa01_sysdtest_ioctl_mode(int mode) { lk_ioctl_mode = mode; }
unsigned pa01_sysdtest_ioctl_state(unsigned which) {
    if (which == 0) return (unsigned)lk_ioctl_mode;
    if (which == 1) return lk_ioctl_calls;
    return UINT32_MAX;
}
void pa01_sysdtest_ioctl_reset(void) { lk_ioctl_mode = 0; lk_ioctl_calls = 0; }

void pa01_sysdtest_lookup_reset(void) {
    lk_async_mode = 0;
    lk_reply_mode = 0;
    lk_process_mode = 0;
}
void pa01_sysdtest_mpid_reset(void) {
    lk_mpid_main0 = 0;
    lk_mpid_change = 0;
    lk_mpid_unit_main_alt = 0;
    lk_mpid_unit_self_alt = 0;
    lk_mpid_invoc_alt = 0;
    lk_mpid_sdk_err = 0;
    lk_mpid_type_mode = 0;
    lk_mpid_sig_mode = 0;
    lk_mpid_body_mode = 0;
    lk_mpid_variant_mode = 0;
    lk_mpid_suffix_mode = 0;
    lk_mpid_n_main1 = 0;
    lk_mpid_n_unit_main = 0;
    lk_mpid_n_unit_self = 0;
    lk_mpid_n_main2 = 0;
    lk_mpid_n_invoc = 0;
    lk_mpid_seq = 0;
    lk_mpid_phase = 0;
    lk_mpid_hist_len = 0;
    memset(lk_mpid_hist, 0, sizeof lk_mpid_hist);
    lk_mpid_pid_override = 0;
    lk_mpid_iid_zero = 0;
    lk_mpid_ay15 = 0;
}
void pa01_sysdtest_mpid_main_pid(int pid) {
    lk_mpid_pid_override = pid;
}
void pa01_sysdtest_mpid_iid_modes(int zero, int ay15) {
    lk_mpid_iid_zero = zero;
    lk_mpid_ay15 = ay15;
}
unsigned pa01_sysdtest_mpid_hist(unsigned idx) {
    if (idx >= 8) return (unsigned)UINT32_MAX;
    if (idx >= lk_mpid_hist_len) return (unsigned)UINT32_MAX;
    return (unsigned)lk_mpid_hist[idx];
}
void pa01_sysdtest_mpid_mode(int main0, int change, int unit_main_alt, int unit_self_alt) {
    lk_mpid_main0 = main0;
    lk_mpid_change = change;
    lk_mpid_unit_main_alt = unit_main_alt;
    lk_mpid_unit_self_alt = unit_self_alt;
}
void pa01_sysdtest_mpid_mode2(int invoc_alt, int sdk_err, int type_mode, int sig_mode) {
    lk_mpid_invoc_alt = invoc_alt;
    lk_mpid_sdk_err = sdk_err;
    lk_mpid_type_mode = type_mode;
    lk_mpid_sig_mode = sig_mode;
}
void pa01_sysdtest_mpid_mode3(int body_mode, int variant_mode, int suffix_mode) {
    lk_mpid_body_mode = body_mode;
    lk_mpid_variant_mode = variant_mode;
    lk_mpid_suffix_mode = suffix_mode;
}
unsigned pa01_sysdtest_mpid_state(unsigned which) {
    switch (which) {
    case 0: return lk_mpid_n_main1;
    case 1: return lk_mpid_n_unit_main;
    case 2: return lk_mpid_n_unit_self;
    case 3: return lk_mpid_n_main2;
    case 4: return lk_mpid_n_invoc;
    case 5: return lk_mpid_seq;
    case 6: return lk_callbacks;
    case 7: return lk_live_slots;
    case 8: return lk_live_queries;
    case 9: return lk_live_replies;
    case 10: return lk_mpid_hist_len;
    case 11: return lk_mpid_hist_len > 0 ? (unsigned)lk_mpid_hist[0] : (unsigned)UINT32_MAX;
    case 12: return lk_mpid_hist_len > 1 ? (unsigned)lk_mpid_hist[1] : (unsigned)UINT32_MAX;
    case 13: return lk_mpid_hist_len > 2 ? (unsigned)lk_mpid_hist[2] : (unsigned)UINT32_MAX;
    case 14: return lk_mpid_hist_len > 3 ? (unsigned)lk_mpid_hist[3] : (unsigned)UINT32_MAX;
    case 15: return lk_mpid_hist_len > 4 ? (unsigned)lk_mpid_hist[4] : (unsigned)UINT32_MAX;
    case 16: return (unsigned)lk_mpid_pid_override;
    default: return UINT32_MAX;
    }
}
void pa01_sysdtest_lookup_mode(int async_mode, int reply_mode, int process_mode) {
    lk_async_mode = async_mode;
    lk_reply_mode = reply_mode;
    lk_process_mode = process_mode;
}
unsigned pa01_sysdtest_lookup_state(unsigned which) {
    switch (which) {
    case 0: return lk_live_queries;
    case 1: return lk_live_replies;
    case 2: return lk_live_slots;
    case 3: return lk_async_calls;
    case 4: return lk_callbacks;
    case 5: return (unsigned)lk_process_calls;
    default: return UINT32_MAX;
    }
}

/* Options de lien TEST obligatoires :
 * -Wl,--wrap=calloc
 * -Wl,--wrap=clock_gettime
 * -Wl,--wrap=close
 * -Wl,--wrap=connect
 * -Wl,--wrap=ioctl
 * -Wl,--wrap=poll
 * -Wl,--wrap=sd_bus_call_async
 * -Wl,--wrap=sd_bus_close_unref
 * -Wl,--wrap=sd_bus_creds_get_augmented_mask
 * -Wl,--wrap=sd_bus_creds_get_euid
 * -Wl,--wrap=sd_bus_creds_get_mask
 * -Wl,--wrap=sd_bus_creds_get_pid
 * -Wl,--wrap=sd_bus_creds_get_pidfd_dup
 * -Wl,--wrap=sd_bus_creds_unref
 * -Wl,--wrap=sd_bus_get_events
 * -Wl,--wrap=sd_bus_get_fd
 * -Wl,--wrap=sd_bus_get_owner_creds
 * -Wl,--wrap=sd_bus_get_timeout
 * -Wl,--wrap=sd_bus_is_bus_client
 * -Wl,--wrap=sd_bus_is_ready
 * -Wl,--wrap=sd_bus_is_server
 * -Wl,--wrap=sd_bus_message_append
 * -Wl,--wrap=sd_bus_message_at_end
 * -Wl,--wrap=sd_bus_message_enter_container
 * -Wl,--wrap=sd_bus_message_exit_container
 * -Wl,--wrap=sd_bus_message_get_type
 * -Wl,--wrap=sd_bus_message_has_signature
 * -Wl,--wrap=sd_bus_message_new_method_call
 * -Wl,--wrap=sd_bus_message_read
 * -Wl,--wrap=sd_bus_message_read_array
 * -Wl,--wrap=sd_bus_message_ref
 * -Wl,--wrap=sd_bus_message_set_allow_interactive_authorization
 * -Wl,--wrap=sd_bus_message_set_auto_start
 * -Wl,--wrap=sd_bus_message_unref
 * -Wl,--wrap=sd_bus_negotiate_creds
 * -Wl,--wrap=sd_bus_negotiate_fds
 * -Wl,--wrap=sd_bus_new
 * -Wl,--wrap=sd_bus_process
 * -Wl,--wrap=sd_bus_ref
 * -Wl,--wrap=sd_bus_set_allow_interactive_authorization
 * -Wl,--wrap=sd_bus_set_anonymous
 * -Wl,--wrap=sd_bus_set_bus_client
 * -Wl,--wrap=sd_bus_set_close_on_exit
 * -Wl,--wrap=sd_bus_set_exit_on_disconnect
 * -Wl,--wrap=sd_bus_set_fd
 * -Wl,--wrap=sd_bus_set_server
 * -Wl,--wrap=sd_bus_slot_set_floating
 * -Wl,--wrap=sd_bus_slot_unref
 * -Wl,--wrap=sd_bus_start
 * -Wl,--wrap=sd_bus_unref
 */
