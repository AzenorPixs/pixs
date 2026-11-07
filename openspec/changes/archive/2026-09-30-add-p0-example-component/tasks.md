# Tasks — add-p0-example-component

## 1. Sources et façade

- [x] 1.1 Source TOML provider : `src/pixs/example/component.toml` schéma 1, MODULE `example.hello` 1.0.0, capacité/contrat `example.hello[.contract]` 1.0.0 — preuve : parse/validate OK
- [x] 1.2 Démo pure : `src/pixs/example/demo.py` (`example_texts/provider_text`, `example_scope`, `example_plan`, `example_compose`), APIs publiques réutilisées, ports injectés — preuve : revue + tests wiring
- [x] 1.3 Façade isolée : `src/pixs/example/__init__.py` sans side-effect, sans import production — preuve : import public
- [x] 1.4 README parcours borné : `src/pixs/example/README.md` commandes DEVOPS exactes + limitations — preuve : relecture

## 2. Tests

- [x] 2.1 Tests unitaires wiring : `tests/unit/test_example_component.py` (manifests, résolution déterministe, attestations, TENANT/cross-tenant, ALLOW/DENY, audit, clock/provider, non-mutation) — preuve : suite verte
- [x] 2.2 Tests intégration mémoire : `tests/integration/test_example_composition.py` (`compose` + `plan_filter`, attestations test-only, audit mémoire) — preuve : suite verte
- [x] 2.3 Tests ciblés exécutés : deux commandes DEVOPS exactes unit + intégration — preuve : exits 0
- [x] 2.4 Régressions globales : suites complètes unit + intégration via chemins DEVOPS — preuve : exits 0

## 3. Validations

- [x] 3.1 AST/UTF-8/LF + delta exact + OpenSpec strict via exécutable DEVOPS — preuve : 0 échec
- [x] 3.2 Revue matrice/nondep/nosecrets/périmètre + preuves CAB — preuve : rapport

Limites : backend Django, PostgreSQL, CLI/Developer Kit complet, providers concrets, frontend, persistance, audit durable, dépendances nouvelles, runtime complet et P0 global hors périmètre. Archivage sur mandat distinct après tout prouvé.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Validations ».

### C35-SL01 — Source TOML provider : `src/pixs/example/component.toml` schéma 1, MODULE `example.hello` 1.0.0, capacité/contrat `example.hello[.contract]` 1.0.0 — preuve : parse/validate OK

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Sources et façade », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL02 — Démo pure : `src/pixs/example/demo.py` (`example_texts/provider_text`, `example_scope`, `example_plan`, `example_compose`), APIs publiques réutilisées, ports injectés — preuve : revue + tests wiring

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Sources et façade », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL03 — Façade isolée : `src/pixs/example/__init__.py` sans side-effect, sans import production — preuve : import public

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Sources et façade », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL04 — README parcours borné : `src/pixs/example/README.md` commandes DEVOPS exactes + limitations — preuve : relecture

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Sources et façade », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL05 — Tests unitaires wiring : `tests/unit/test_example_component.py` (manifests, résolution déterministe, attestations, TENANT/cross-tenant, ALLOW/DENY, audit, clock/provider, non-mutation) — preuve : suite verte

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Tests », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL06 — Tests intégration mémoire : `tests/integration/test_example_composition.py` (`compose` + `plan_filter`, attestations test-only, audit mémoire) — preuve : suite verte

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Tests », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL07 — Tests ciblés exécutés : deux commandes DEVOPS exactes unit + intégration — preuve : exits 0

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL08 — Régressions globales : suites complètes unit + intégration via chemins DEVOPS — preuve : exits 0

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Tests », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL09 — AST/UTF-8/LF + delta exact + OpenSpec strict via exécutable DEVOPS — preuve : 0 échec

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Validations », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C35-SL10 — Revue matrice/nondep/nosecrets/périmètre + preuves CAB — preuve : rapport

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Validations », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
