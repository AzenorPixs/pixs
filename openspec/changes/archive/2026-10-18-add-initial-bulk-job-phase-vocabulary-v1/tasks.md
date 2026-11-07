# Tâches — Représentation Enum des phases BulkJob B08

## 1. Vocabulaire structurel pur

- [x] 1.1 Publier `src/pixs/kernel/bulk_job_phase.py` : `BulkJobPhase(Enum)` aux quatre membres canoniques `STAGE`, `VALIDATE`, `APPLY`, `EXPORT`, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.
- [x] 1.2 Publier et exécuter le test unitaire `tests/unit/test_bulk_job_phase.py` : adhésion exacte aux noms/valeurs et à l'ordre canonique B08, absence de membre supplémentaire, refus sans normalisation, frontière explicite entre Enum et chaînes canoniques ; les vrais validateurs existants sont couverts par les régressions distinctes, sans les modifier.
- [x] 1.3 Publier et exécuter le test d'intégration `tests/integration/test_bulk_job_phase_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées, sans effet observable.
- [x] 1.4 Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_bulk_operation_commit_mode`, `test_bulk_operation_status`, `test_bulk_operation_conflict et test_bulk_runtime_records`), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.

- [x] 1.5 Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.
- [x] 1.6 Vérifier le périmètre et les preuves avant décision distincte d'archivage.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et le rapport STATISTIQUES.md relèvent de décisions et mandats CGPT distincts après preuve des tâches.

<!-- DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend. -->

## Preuves exécutées

- Prévol PLLM mode 1 Muse high courant valide ; test CAB exact /usr/bin/true avec once, code 0, READY final.
- Sept fichiers nouveaux aux contenus exacts relus, UTF-8/LF ; empreintes des onze fichiers existants suivis inchangées. Aucun canon, runtime, façade ni __init__ modifié.
- Compilation py_compile des trois fichiers Python : code 0.
- Tests ciblés et régressions : 32/32 OK, dont trois nouveaux tests ; import frais sous gardes éprouvées, modèles/validateurs Bulk existants testés sans connexion PostgreSQL.
- Validation OpenSpec ciblée stricte : code 0 ; skip_specs reconnu, aucun delta fonctionnel.
- Global standard : 186/186, code 0. Global strict : 184/186, code 1 ; quatre WARNING historiques de longueur (bulk-operations exigences 6/10/13 ; identity-assurance exigence 4), zéro ERROR. Résultat conservé sans correction hors périmètre.
- Une demande de proposition à révision inconnue a été annulée avant effet ; demande neuve corrélée ensuite exécutée, sans réutilisation de permission.
- PostgreSQL et frontend : N/A pour ce vocabulaire passif ; aucune dépendance, migration, activation runtime ni opération Git.
- L’archivage et les statistiques restent des mandats distincts, non revendiqués par les coches ci-dessus.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves exécutées ».

### B61-SL01 — Publier `src/pixs/kernel/bulk_job_phase.py` : `BulkJobPhase(Enum)` aux quatre membres canoniques `STAGE`, `VALIDATE`, `APPLY`, `EXPORT`, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Vocabulaire structurel pur », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B61-SL02 — Publier et exécuter le test unitaire `tests/unit/test_bulk_job_phase.py` : adhésion exacte aux noms/valeurs et à l'ordre canonique B08, absence de membre supplémentaire, refus sans normalisation, frontière explicite entre Enum et chaînes canoniques ; les vrais validateurs existants sont couverts par les régressions distinctes, sans les modifier.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Vocabulaire structurel pur », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B61-SL03 — Publier et exécuter le test d'intégration `tests/integration/test_bulk_job_phase_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées, sans effet observable.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Vocabulaire structurel pur », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B61-SL04 — Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_bulk_operation_commit_mode`, `test_bulk_operation_status`, `test_bulk_operation_conflict et test_bulk_runtime_records`), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Vocabulaire structurel pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B61-SL05 — Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Vocabulaire structurel pur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B61-SL06 — Vérifier le périmètre et les preuves avant décision distincte d'archivage.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Vocabulaire structurel pur », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
