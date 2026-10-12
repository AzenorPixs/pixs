# Tâches — Représentation déclarative interne du DataSubjectRequest

## 1. Contrat structurel

- [x] 1.1 Valider strictement le change et la spec `data-governance` (exit 0 obligatoire) avant tout code, consigner les sorties et codes réels des validations globales `--specs --strict --json --report findings` et `--all --strict --json --report findings` selon la règle de qualification de design.md, avec résultat natif contrôlé.
- [x] 1.2 Publier `src/pixs/kernel/data_subject_request.py` : `DataSubjectRequest` (dataclass `frozen`, onze champs dans l'ordre de TECHNICAL §14.6) et `validate_data_subject_request` selon les champs, les frontières et les diagnostics définis dans design.md.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_subject_request.py` : adhésion des cas valides, refus par champ, `None` admis pour les cinq éventuels et refusé pour les six requis, membres `DataSubjectOperation` validés par identité, objets hostiles jamais invoqués, diagnostics fixes triés/dédupliqués sans écho, `__all__` exact, dataclass `frozen`.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_subject_request_integration.py` : import et vérification du vocabulaire et de la demande en processus frais `-I -B` sous environnement réduit et gardes finies d'effets réutilisées, marqueur `DATA_SUBJECT_REQUEST_SAFE_INTEGRATION_OK` seul sur stdout, quatre assertions finales hors `with`, absence d'effet limitée aux surfaces gardées (non preuve universelle), sans nouvelle dépendance.
- [x] 1.5 Exécuter les compilations ciblées des trois fichiers et la régression bornée définie dans design.md (`tests/unit/test_data_subject_operations_vocabulary.py`, `tests/unit/test_data_governance_profile.py`, `tests/integration/test_kernel_purity.py`, `tests/integration/test_public_api_facades.py`) ; contrôler les résultats natifs, UTF-8/LF et les empreintes des fichiers non concernés.
- [x] 1.6 Exécuter après code les stricts du change et de la spec `data-governance` (exit 0), reconsigner les validations globales et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
