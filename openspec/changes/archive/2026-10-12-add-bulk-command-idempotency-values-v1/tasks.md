## 1. Préparation et implémentation

- [x] 1.1 Préparer quatre artefacts, delta MODIFIED B10 verbatim ; réussir contrôle strict avant code.
- [x] 1.2 Implémenter `src/pixs/backend/bulk_command_idempotency_values.py` pur : 12 clés exactes, types exacts avant valeurs, hex64, SemVer libre complète, états exacts, `revision >= 1`, owned frozen, sans effet.
- [x] 1.3 Implémenter `tests/unit/test_bulk_command_idempotency_values.py` comportemental (unittest seul) : forme 12 clés, sous-classes/hostiles sans hooks, UTC exact, hex/SemVer/états/revision, déterminisme diagnostics, frozen owned.
- [x] 1.4 Implémenter `tests/integration/test_bulk_command_idempotency_integration.py` en processus frais sous gardes de référence (fichiers/réseau/processus/environnement/DB/Core), import sans effets, contrôles positifs puis comportement mémoire.
- [x] 1.5 Compiler séparément les 3 Python ; réussir tests ciblés puis régressions Bulk/Kernel applicables.
- [x] 1.6 Vérifier contrôle strict sans issue, UTF-8/LF, canon/exports/sources préservés, aucun ancien code modifié, acceptation complète.

## Procédure après preuves

Cocher seulement après preuves ; archive unique `--skip-specs` puis `STATISTIQUES.md` sous mandat distinct. Vérifier six sections et totaux avant retour. Aucune persistance/transaction ni preuve inventée annoncée.
