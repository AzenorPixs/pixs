# Tasks — add-initial-frontend-contribution-type-vocabulary

- [x] 1. Créer `src/pixs/kernel/frontend_contribution_types.py` (Enum pur 8 noms, `__all__` seul)
- [x] 2. Créer `tests/unit/test_frontend_contribution_type.py` (canon, sans alias, `__all__` seul)
- [x] 3. Créer `tests/integration/test_frontend_contribution_type_integration.py` (processus frais sous gardes + contrôles positifs)
- [x] 4. `py_compile` séparée des trois fichiers
- [x] 5. Exécuter tests unitaires du périmètre + import frais
- [x] 6. Exécuter régressions Enum ciblées `notification_channel`, `job_state`, `notification_delivery_state`
- [x] 7. `openspec validate --strict` du change avant/après code + validate global sans nouvelles issues
- [x] 8. Vérifier UTF-8/LF et empreintes des fichiers créés

## Procédure après preuves

Cocher les huit tâches uniquement après leurs preuves. Sous exclusion d’intégration, revalider la base courante, archiver une seule fois avec --skip-specs, puis produire STATISTIQUES.md par mandat d’édition distinct. Vérifier ses six sections, UTF-8/LF et totaux, publier, obtenir le gate individuel, désarmer et libérer avant retour à SÉLECTION du parent CISMP.
