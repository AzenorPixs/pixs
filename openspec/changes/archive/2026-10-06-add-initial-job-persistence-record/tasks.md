# Tâches — Unité de persistance JobRecord pour les travaux

## 1. Persistance JobRecord

- [x] 1.1 Valider strictement le change, les 76 spécifications canoniques et les éléments OpenSpec avant le code.
- [x] 1.2 Éditer models.py selon le contrat et les frontières de design.md : JobRecord treize champs, _validate_job_version, Meta constraints, __all__ ; classe des fanions préservée octet pour octet.
- [x] 1.3 Ajouter migrations/0002_job_record.py dépendant de 0001, CreateModel réversible avec PK serialize=False et constraints.
- [x] 1.4 Ajouter et exécuter les tests unitaires offline (cas ciblés, validate_unique=False et validate_constraints=False, preuve zéro connexion, save sans full_clean, message fixe sans écho).
- [x] 1.5 Ajouter et exécuter le test d'intégration PostgreSQL réel : loader borné du processus de test, schéma unique, forward 0001/0002, roundtrip JSON, refus CHECK, limite SemVer DB, reverse 0002, tables FeatureFlag d'origine inchangées, cleanup et connexions fermées, résultat fermé `real_pg=True` distinct du marqueur du harnais sûr.
- [x] 1.6 Adapter la seule assertion d'inventaire du harnais fanions aux deux modèles ; compiler les cinq fichiers Python ; exécuter la régression des 20 modules (111 tests), les deux tests PG existants et les nouveaux tests (comptes natifs séparés) ; vérifier UTF-8/LF et l'intégrité byte à byte de settings.py, apps.py, 0001 et de la classe des fanions, ainsi que les 120 empreintes de référence inchangées hors models.py et hors l'assertion du harnais fanions adaptée sous mandat distinct.
- [x] 1.7 Valider strictement le change, les spécifications canoniques (76) et les éléments OpenSpec après le code et les tests, avec effet jobs attendu +0/~0/-0/→0.

L'archivage et STATISTIQUES.md nécessitent des décisions et mandats CGPT distincts après preuve des tâches.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### C68-SL01 — Valider strictement le change, les 76 spécifications canoniques et les éléments OpenSpec avant le code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Persistance JobRecord », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C68-SL02 — Éditer models.py selon le contrat et les frontières de design.md : JobRecord treize champs, _validate_job_version, Meta constraints, __all__ ; classe des fanions préservée octet pour octet.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Persistance JobRecord », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C68-SL03 — Ajouter migrations/0002_job_record.py dépendant de 0001, CreateModel réversible avec PK serialize=False et constraints.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Persistance JobRecord », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C68-SL04 — Ajouter et exécuter les tests unitaires offline (cas ciblés, validate_unique=False et validate_constraints=False, preuve zéro connexion, save sans full_clean, message fixe sans écho).

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Persistance JobRecord », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C68-SL05 — Ajouter et exécuter le test d'intégration PostgreSQL réel : loader borné du processus de test, schéma unique, forward 0001/0002, roundtrip JSON, refus CHECK, limite SemVer DB, reverse 0002, tables FeatureFlag d'origine inchangées, cleanup et connexions fermées, résultat fermé `real_pg=True` distinct du marqueur du harnais sûr.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Persistance JobRecord », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C68-SL06 — Adapter la seule assertion d'inventaire du harnais fanions aux deux modèles ; compiler les cinq fichiers Python ; exécuter la régression des 20 modules (111 tests), les deux tests PG existants et les nouveaux tests (comptes natifs séparés) ; vérifier UTF-8/LF et l'intégrité byte à byte de settings.py, apps.py, 0001 et de la classe des fanions, ainsi que les 120 empreintes de référence inchangées hors models.py et hors l'assertion du harnais fanions adaptée sous mandat distinct.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Persistance JobRecord », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C68-SL07 — Valider strictement le change, les spécifications canoniques (76) et les éléments OpenSpec après le code et les tests, avec effet jobs attendu +0/~0/-0/→0.

- Ancien repère et tâche rattachée : tâche 1.7 ; section « 1. Persistance JobRecord », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
