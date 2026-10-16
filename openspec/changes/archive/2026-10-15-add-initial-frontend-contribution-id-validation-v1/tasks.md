# Tasks — add-initial-frontend-contribution-id-validation-v1
- [x] 1. Créer `src/pixs/kernel/frontend_contribution_ids.py` (seul validateur, `__all__` seul, pur lexical)
- [x] 2. Créer `tests/unit/test_frontend_contribution_id.py` (table vrais/faux, non-str, `__all__` seul)
- [x] 3. Créer `tests/integration/test_frontend_contribution_id_integration.py` (frais sous gardes + contrôles positifs)
- [x] 4. `py_compile` séparée des 3 fichiers via `.venv/bin/python3`
- [x] 5. Tests unitaires périmètre + import frais
- [x] 6. Régressions ciblées type + path unit/frais
- [x] 7. `openspec validate --strict` change avant/après + global sans nouvelles issues
- [x] 8. Vérifier UTF-8/LF et empreintes
## Procédure après preuves
Cocher après preuves seules. Global canon sous exclusion après READY local ; archive unique `--skip-specs` après égalité canonique prouvée ; STATISTIQUES.md distinct après archive par mandat édition séparé (6 sections, UTF-8/LF, totaux, N/A motivé) ; passage ISMP seulement après change préparé validé.
