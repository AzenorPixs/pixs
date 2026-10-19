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
