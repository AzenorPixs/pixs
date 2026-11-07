/* Budget math pur D11 : sans horloge, sans profil, sans admission. */
/* Etat NEW -> ACTIVE -> INVALID / RETIRED terminal. */
/* global = start + min(parent_end - start, 1s), sans debordement. */
/* Acquisition <= 250ms, 2 max, echeance = min(global, parent, now + 250ms). */
/* Pas de rearmement, parent emprunte jamais invalide arbitrairement. */
#ifndef Z12_TIME_BUDGET_INC
#define Z12_TIME_BUDGET_INC
#include <stdint.h>
#define Z12_BUDGET_GLOBAL_NS 1000000000ULL
#define Z12_BUDGET_ACQ_NS 250000000ULL
#define Z12_BUDGET_ACQ_MAX 2u
#define Z12_BUDGET_NEW 0
#define Z12_BUDGET_ACTIVE 1
#define Z12_BUDGET_INVALID 2
#define Z12_BUDGET_RETIRED 3
typedef struct {
 int state;
 uint64_t started_ns;
 uint64_t parent_end_ns;
 uint64_t global_end_ns;
 uint64_t last_seen_ns;
 uint64_t acquisition_deadline_ns;
 uint32_t attempts;
 int active;
} Z12BudgetState;
typedef struct {
 int code;
 uint64_t deadline_ns;
} Z12BudgetResult;
/* Init seule depuis NEW, ne touche rien si deja ACTIVE/INVALID/RETIRED. */
static inline int z12_budget_init(Z12BudgetState *s, uint64_t start, uint64_t parent_end)
{
 uint64_t remaining;
 uint64_t duration;
 if (s == 0) return -2;
 if (s->state == Z12_BUDGET_RETIRED) return 0;
 if (s->state != Z12_BUDGET_NEW) return 0;
 if (parent_end <= start) return 0;
 remaining = parent_end - start;
 duration = (remaining < Z12_BUDGET_GLOBAL_NS) ? remaining : Z12_BUDGET_GLOBAL_NS;
 if (duration == 0) return 0;
 s->started_ns = start;
 s->parent_end_ns = parent_end;
 s->global_end_ns = start + duration;
 s->last_seen_ns = start;
 s->acquisition_deadline_ns = 0;
 s->attempts = 0;
 s->active = 0;
 s->state = Z12_BUDGET_ACTIVE;
 return 1;
}
/* Begin rend deadline par valeur, jamais d alias sur state. */
static inline Z12BudgetResult z12_budget_begin(Z12BudgetState *s, uint64_t now)
{
 Z12BudgetResult r;
 uint64_t rem_global;
 uint64_t rem_parent;
 uint64_t duration;
 r.code = 0;
 r.deadline_ns = 0;
 if (s == 0) { r.code = -2; return r; }
 if (s->state != Z12_BUDGET_ACTIVE) return r;
 if (now < s->last_seen_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return r; }
 s->last_seen_ns = now;
 if (now >= s->parent_end_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return r; }
 if (now > s->global_end_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return r; }
 if (s->active && now > s->acquisition_deadline_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return r; }
 if (s->active) return r;
 if (s->attempts >= Z12_BUDGET_ACQ_MAX) return r;
 rem_global = s->global_end_ns - now;
 rem_parent = s->parent_end_ns - now;
 duration = rem_global;
 if (rem_parent < duration) duration = rem_parent;
 if (Z12_BUDGET_ACQ_NS < duration) duration = Z12_BUDGET_ACQ_NS;
 if (duration == 0) return r;
 if (duration > 18446744073709551615ULL - now) return r;
 { uint64_t computed = now + duration;
 if (computed <= now) return r;
 if (computed > s->global_end_ns) return r;
 if (computed > s->parent_end_ns) return r;
 r.deadline_ns = computed; }
 s->acquisition_deadline_ns = r.deadline_ns;
 s->attempts = s->attempts + 1;
 s->active = 1;
 r.code = 1;
 return r;
}
/* End verifie borne 250ms memorisee, parent exclusif, monotonie. */
static inline int z12_budget_end(Z12BudgetState *s, uint64_t now)
{
 if (s == 0) return -2;
 if (s->state != Z12_BUDGET_ACTIVE) return 0;
 if (now < s->last_seen_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return 0; }
 s->last_seen_ns = now;
 if (now >= s->parent_end_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return 0; }
 if (now > s->global_end_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return 0; }
 if (!s->active) return 0;
 if (now > s->acquisition_deadline_ns) { s->state = Z12_BUDGET_INVALID; s->active = 0; return 0; }
 s->active = 0;
 return 1;
}
static inline int z12_budget_destroy(Z12BudgetState *s)
{
 if (s == 0) return 1;
 if (s->state == Z12_BUDGET_RETIRED) return 1;
 s->state = Z12_BUDGET_RETIRED;
 s->active = 0;
 return 1;
}
#endif
