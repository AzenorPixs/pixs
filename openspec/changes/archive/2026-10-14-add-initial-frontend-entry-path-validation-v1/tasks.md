# Tasks — add-initial-frontend-entry-path-validation-v1

- [x] 1. Créer `src/pixs/kernel/frontend_entry_paths.py` (seul `validate_frontend_entry_path_v1`, `__all__` seul, pur lexical)
- [x] 2. Créer `tests/unit/test_frontend_entry_path.py` (table vrais/faux, non-str, `__all__` seul)
- [x] 3. Créer `tests/integration/test_frontend_entry_path_integration.py` (processus frais sous gardes + contrôles positifs FS + cas valides/invalides)
- [x] 4. `py_compile` séparée des trois fichiers
- [x] 5. Exécuter tests unitaires du périmètre + import frais
- [x] 6. Exécuter régressions vocab ciblées `FrontendContributionType` unit + fresh
- [x] 7. `openspec validate --strict` du change avant/après code + validate canon/global sans nouvelles issues
- [x] 8. Vérifier UTF-8/LF et empreintes des fichiers créés

## Procédure après preuves

Cocher les huit tâches uniquement après leurs preuves. Global canon sous exclusion d'intégration après READY local et tests/strict ; alors preuve global/cochage 8 tâches puis archive unique --skip-specs, statistiques par mandat distinct, pub, gate désarmement libération et retour sélection. Archive/stat/post-procédure hors cases pré-archive.
