/* Harnais B2 : cas autonomes budget pur, UBSan. */
#include <stdint.h>
#include <stdio.h>
#include "z12_time_budget.inc"
static int total = 0;
static int echecs = 0;
static void ok(int cond, const char *nom)
{
 total = total + 1;
 if (cond) { printf("ok %s\n", nom); }
 else { echecs = echecs + 1; printf("KO %s\n", nom); }
}
static Z12BudgetState neuf(void)
{
 Z12BudgetState s;
 s.state = Z12_BUDGET_NEW;
 s.started_ns = 0;
 s.parent_end_ns = 0;
 s.global_end_ns = 0;
 s.last_seen_ns = 0;
 s.acquisition_deadline_ns = 0;
 s.attempts = 0;
 s.active = 0;
 return s;
}
int main(void)
{
 Z12BudgetState s;
 Z12BudgetResult r;
 s = neuf();
 ok(z12_budget_init(&s, 0, 1000000000ULL) == 1, "init-1s");
 s = neuf();
 ok(z12_budget_init(&s, 0, 5000000000ULL) == 1, "init-parent-long");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1, "begin-ok");
 ok(z12_budget_end(&s, 250000000ULL) == 1, "fin-250ms-acceptee");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1, "begin-250");
 ok(z12_budget_end(&s, 250000001ULL) == 0, "fin-250ms-plus-1-refusee");
 ok(s.state == Z12_BUDGET_INVALID, "expire-invalide");
 ok(s.attempts == 1, "counter-conserve-apres-echec");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1 && r.deadline_ns == 250000000ULL, "borne-250ms");
 ok(z12_budget_end(&s, 10) == 1, "end-1");
 r = z12_budget_begin(&s, 20);
 ok(r.code == 1, "deuxieme-acq");
 ok(z12_budget_end(&s, 30) == 1, "end-2");
 r = z12_budget_begin(&s, 40);
 ok(r.code == 0 && r.deadline_ns == 0, "troisieme-refusee");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 100);
 ok(r.code == 1, "begin-avant-rollback");
 ok(z12_budget_end(&s, 50) == 0, "rollback-entre-appels-refuse");
 ok(s.state == Z12_BUDGET_INVALID, "rollback-terminal");
 s = neuf();
 z12_budget_init(&s, 0, 1000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1, "begin-1");
 ok(z12_budget_begin(&s, 5).code == 0, "double-begin-refuse");
 ok(z12_budget_end(&s, 6) == 1, "end-1-ok");
 ok(z12_budget_end(&s, 7) == 0, "double-end-refuse");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1, "reinit-base");
 ok(z12_budget_end(&s, 10) == 1, "reinit-end1");
 ok(z12_budget_init(&s, 999, 2000) == 0, "reinit-actif-refuse");
 ok(s.started_ns == 0 && s.global_end_ns == 1000000000ULL && s.attempts == 1, "ancres-compteurs-preserves-apres-1acq");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 750000000ULL);
 ok(r.code == 1, "begin-750ms");
 ok(z12_budget_end(&s, 1000000000ULL) == 1, "fin-globale-exacte-acceptee-parent-long");
 s = neuf();
 z12_budget_init(&s, 0, 1000000000ULL);
 r = z12_budget_begin(&s, 750000000ULL);
 ok(r.code == 1, "begin-750ms-parent-1s");
 ok(z12_budget_end(&s, 1000000000ULL) == 0, "fin-1s-refusee-parent-exclusif");
 ok(s.state == Z12_BUDGET_INVALID, "parent-exclusif-terminal");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 750000000ULL);
 ok(r.code == 1, "begin-750ms-parent-5s");
 ok(z12_budget_end(&s, 1000000001ULL) == 0, "global-plus-1-invalide-actif");
 ok(s.state == Z12_BUDGET_INVALID && s.attempts == 1, "compteur-1-apres-global-plus-1");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1, "dbl-actif-base");
 ok(z12_budget_end(&s, 250000001ULL) == 0, "fin-250ms-plus-1-invalide");
 ok(z12_budget_begin(&s, 250000002ULL).code == 0, "double-begin-apres-depassement-pas-rearme");
 ok(s.attempts == 1 && s.state == Z12_BUDGET_INVALID, "compteur-conserve-apres-double-begin");
 s = neuf();
 z12_budget_init(&s, 0, 5000000000ULL);
 r = z12_budget_begin(&s, 0);
 ok(r.code == 1, "dbl-begin-base");
 ok(z12_budget_begin(&s, 5).code == 0, "dbl-begin-pendant-actif");
 ok(z12_budget_begin(&s, 4).code == 0 && s.state == Z12_BUDGET_INVALID, "rollback-pendant-double-begin-terminal");
 ok(z12_budget_begin(&s, 6).code == 0, "pas-rearmement-apres-rollback");
 s = neuf();
 z12_budget_init(&s, 0, 1000);
 ok(z12_budget_destroy(&s) == 1, "destroy-ok");
 ok(z12_budget_destroy(&s) == 1, "destroy-idempotent");
 ok(z12_budget_init(&s, 0, 1000) == 0, "retire-bloque-reinit");
 ok(z12_budget_begin(&s, 0).code == 0, "pas-rearm-apres-destroy");
 ok(z12_budget_destroy(0) == 1, "destroy-null");
 s = neuf();
 ok(z12_budget_init(&s, 18446744073709551605ULL, 18446744073709551615ULL) == 1, "parent-court-10ns-pres-max");
 r = z12_budget_begin(&s, 18446744073709551605ULL);
 ok(r.code == 1 && r.deadline_ns <= 18446744073709551615ULL, "begin-court-pres-max");
 s = neuf();
 z12_budget_init(&s, 0, 1000000000ULL);
 ok(z12_budget_begin(&s, 1000000000ULL).code == 0, "begin-cutoff-pas-0ns");
 s = neuf();
 z12_budget_init(&s, 0, 1000000000ULL);
 ok(z12_budget_end(&s, 1000000000ULL) == 0, "end-egal-parent-exclusif-refuse");
 ok(z12_budget_init(0, 0, 10) == -2, "init-null-invalide");
 ok(z12_budget_begin(0, 0).code == -2, "begin-null-invalide");
 ok(z12_budget_end(0, 0) == -2, "end-null-invalide");
 printf("total=%d echecs=%d\n", total, echecs);
 return (echecs ? 1 : 0);
}
