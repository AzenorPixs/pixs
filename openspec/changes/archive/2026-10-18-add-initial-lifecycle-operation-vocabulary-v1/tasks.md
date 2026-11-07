# Tâches — Représentation Enum des opérations Lifecycle

## 1. Vocabulaire structurel pur

- [x] 1.1 Publier `src/pixs/kernel/lifecycle/operation.py` : `LifecycleOperation(Enum)` aux onze membres canoniques `DISCOVER`→`PURGE` de valeurs lowercase, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.
- [x] 1.2 Publier et exécuter le test unitaire `tests/unit/test_lifecycle_operation.py` : adhésion exacte aux noms/valeurs lowercase et à l'ordre canonique `LIFECYCLE_OPERATIONS`, Enum seul sans `str`, absence d'alias, refus sans normalisation des inconnus, cohérence exacte avec `LIFECYCLE_OPERATIONS`, préservation P0 (`state.py` inchangé, 11 opérations, hors-périmètre inchangé) ; les vraies transitions existantes restent couvertes par les régressions distinctes, sans les modifier.
- [x] 1.3 Publier et exécuter le test d'intégration `tests/integration/test_lifecycle_operation_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées (absence d’E/S applicative observée, de réseau, processus, accès à l’environnement, DB et core), sans effet observable, avec contrôle de façade inchangée.
- [x] 1.4 Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_lifecycle_state`, `test_bulk_job_phase` comme garde de patron), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.
- [x] 1.5 Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.
- [x] 1.6 Vérifier le périmètre et les preuves avant décision distincte d'archivage.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage avec `--skip-specs` et le rapport STATISTIQUES.md relèvent de décisions et mandats CGPT distincts après preuve des tâches.

<!-- DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend. -->

## Preuves exécutées

- 25 tests réussis : 4 du contrat, 1 import isolé, 18 du cycle mécanique et 2 du vocabulaire BulkJobPhase.
- Trois compilations Python : code 0 ; ciblé OpenSpec strict : code 0 ; global standard : 186/186.
- Global strict : code 1, 184/186 ; uniquement quatre WARNING historiques de longueur (bulk-operations 6/10/13 et identity-assurance 4), zéro ERROR ; aucune réussite stricte globale revendiquée.
- Contenus nouveaux relus, UTF-8/LF vérifiés ; empreintes des cadrages, du canon et des fichiers lifecycle existants inchangées.
- Archivage unique sans modification du canon autorisé distinctement par CGPT après ces preuves ; STATISTIQUES.md reste obligatoire avant clôture.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves exécutées ».

### C94-SL01 — Publier `src/pixs/kernel/lifecycle/operation.py` : `LifecycleOperation(Enum)` aux onze membres canoniques `DISCOVER`→`PURGE` de valeurs lowercase, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Vocabulaire structurel pur », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C94-SL02 — Publier et exécuter le test unitaire `tests/unit/test_lifecycle_operation.py` : adhésion exacte aux noms/valeurs lowercase et à l'ordre canonique `LIFECYCLE_OPERATIONS`, Enum seul sans `str`, absence d'alias, refus sans normalisation des inconnus, cohérence exacte avec `LIFECYCLE_OPERATIONS`, préservation P0 (`state.py` inchangé, 11 opérations, hors-périmètre inchangé) ; les vraies transitions existantes restent couvertes par les régressions distinctes, sans les modifier.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Vocabulaire structurel pur », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C94-SL03 — Publier et exécuter le test d'intégration `tests/integration/test_lifecycle_operation_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées (absence d’E/S applicative observée, de réseau, processus, accès à l’environnement, DB et core), sans effet observable, avec contrôle de façade inchangée.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Vocabulaire structurel pur », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C94-SL04 — Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_lifecycle_state`, `test_bulk_job_phase` comme garde de patron), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Vocabulaire structurel pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C94-SL05 — Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Vocabulaire structurel pur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C94-SL06 — Vérifier le périmètre et les preuves avant décision distincte d'archivage.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Vocabulaire structurel pur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
