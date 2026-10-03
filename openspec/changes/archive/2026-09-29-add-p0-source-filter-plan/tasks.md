# Tasks — add-p0-source-filter-plan

## 1. Moteur commun sans changement public

- [x] 1.1 Extraire `_authorize_detailed` dans `decision.py`, `authorize` enveloppe à appel unique, mêmes `Decision`/comportements/audit — preuve : suites PDP existantes 0 échec + revue diff borné
- [x] 1.2 Créer `src/pixs/core/authz/filter_plan.py` : FilterConfig/Lot/Plan frozen, `FilterPlanError`, `plan_filter` à helper unique, enveloppe/limite/horloge/snapshot figés — preuve : tests unitaires
- [x] 1.3 Étendre `__init__.py` : exports bornés seuls — preuve : import public

## 2. Tests

- [x] 2.1 `tests/unit/test_filter_plan.py` : 9 scénarios + bornes + immuabilité — preuve : suite verte
- [x] 2.2 `tests/integration/test_filter_plan_audit.py` : doubles mémoire, sans persistance — preuve : suite verte
- [x] 2.3 Matrice : régression PDP + partial-unknown-after-ALLOW + port-latefail + audit-failed + cost-overflow, tous fermés sans ID — preuve : cas dédiés verts
- [x] 2.4 Suites complètes unit + intégration via chemins DEVOPS — preuve : exits 0

## 3. Validations

- [x] 3.1 AST mémoire, UTF-8/LF ciblés — preuve : contrôles
- [x] 3.2 OpenSpec strict via exécutable DEVOPS — preuve : 0 échec
- [x] 3.3 Revue specs/cadrages/hors périmètre — preuve : rapport

Limites : PEP, PostgreSQL, filtrage exécuté, caches, audit durable, providers, frontend, dépendances nouvelles et P0 global hors périmètre.

## Preuves

- Seul le profil préparatoire `source-filter-plan-v1` est prouvé ; les exigences générales authorization/PEP/filtrage source/audit durable RESTENT non implémentées et ne sont jamais présentées comme couvertes globalement.
- Ciblés : 33 unit OK, 9 intégration OK ; globaux : 349 unit OK, 112 intégration OK ; AST 5, UTF-8/LF 12, OpenSpec 77/0 strict code 0.
- Rapports : msg_0ef28cf43001jU0v2W6GbIhhrJ, msg_0ef27f63d001PQWPWs4vdNplp8.
- Exclusions maintenues.
