# Tâches — Représentation déclarative interne du DataSubjectRequest

## 1. Contrat structurel

- [x] 1.1 Valider strictement le change et la spec `data-governance` (exit 0 obligatoire) avant tout code, consigner les sorties et codes réels des validations globales `--specs --strict --json --report findings` et `--all --strict --json --report findings` selon la règle de qualification de design.md, avec résultat natif contrôlé.
- [x] 1.2 Publier `src/pixs/kernel/data_subject_request.py` : `DataSubjectRequest` (dataclass `frozen`, onze champs dans l'ordre de TECHNICAL §14.6) et `validate_data_subject_request` selon les champs, les frontières et les diagnostics définis dans design.md.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_subject_request.py` : adhésion des cas valides, refus par champ, `None` admis pour les cinq éventuels et refusé pour les six requis, membres `DataSubjectOperation` validés par identité, objets hostiles jamais invoqués, diagnostics fixes triés/dédupliqués sans écho, `__all__` exact, dataclass `frozen`.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_subject_request_integration.py` : import et vérification du vocabulaire et de la demande en processus frais `-I -B` sous environnement réduit et gardes finies d'effets réutilisées, marqueur `DATA_SUBJECT_REQUEST_SAFE_INTEGRATION_OK` seul sur stdout, quatre assertions finales hors `with`, absence d'effet limitée aux surfaces gardées (non preuve universelle), sans nouvelle dépendance.
- [x] 1.5 Exécuter les compilations ciblées des trois fichiers et la régression bornée définie dans design.md (`tests/unit/test_data_subject_operations_vocabulary.py`, `tests/unit/test_data_governance_profile.py`, `tests/integration/test_kernel_purity.py`, `tests/integration/test_public_api_facades.py`) ; contrôler les résultats natifs, UTF-8/LF et les empreintes des fichiers non concernés.
- [x] 1.6 Exécuter après code les stricts du change et de la spec `data-governance` (exit 0), reconsigner les validations globales et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### C66-SL01 — Valider strictement le change et la spec `data-governance` (exit 0 obligatoire) avant tout code, consigner les sorties et codes réels des validations globales `--specs --strict --json --report findings` et `--all --strict --json --report findings` selon la règle de qualification de design.md, avec résultat natif contrôlé.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Contrat structurel », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C66-SL02 — Publier `src/pixs/kernel/data_subject_request.py` : `DataSubjectRequest` (dataclass `frozen`, onze champs dans l'ordre de TECHNICAL §14.6) et `validate_data_subject_request` selon les champs, les frontières et les diagnostics définis dans design.md.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Contrat structurel », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C66-SL03 — Publier et exécuter `tests/unit/test_data_subject_request.py` : adhésion des cas valides, refus par champ, `None` admis pour les cinq éventuels et refusé pour les six requis, membres `DataSubjectOperation` validés par identité, objets hostiles jamais invoqués, diagnostics fixes triés/dédupliqués sans écho, `__all__` exact, dataclass `frozen`.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Contrat structurel », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C66-SL04 — Publier et exécuter `tests/integration/test_data_subject_request_integration.py` : import et vérification du vocabulaire et de la demande en processus frais `-I -B` sous environnement réduit et gardes finies d'effets réutilisées, marqueur `DATA_SUBJECT_REQUEST_SAFE_INTEGRATION_OK` seul sur stdout, quatre assertions finales hors `with`, absence d'effet limitée aux surfaces gardées (non preuve universelle), sans nouvelle dépendance.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Contrat structurel », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C66-SL05 — Exécuter les compilations ciblées des trois fichiers et la régression bornée définie dans design.md (`tests/unit/test_data_subject_operations_vocabulary.py`, `tests/unit/test_data_governance_profile.py`, `tests/integration/test_kernel_purity.py`, `tests/integration/test_public_api_facades.py`) ; contrôler les résultats natifs, UTF-8/LF et les empreintes des fichiers non concernés.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Contrat structurel », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C66-SL06 — Exécuter après code les stricts du change et de la spec `data-governance` (exit 0), reconsigner les validations globales et leur qualification limitée, résultats natifs contrôlés.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Contrat structurel », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
