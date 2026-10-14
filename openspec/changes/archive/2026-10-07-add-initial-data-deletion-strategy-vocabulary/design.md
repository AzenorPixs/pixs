# Conception — Vocabulaire commun des stratégies de suppression

## Source et représentation

Source normative : `openspec/specs/data-lifecycle/spec.md`, exigence « Vocabulaire commun des stratégies de suppression » et scénario « Vocabulaire déclaratif distinct de la persistance ». Les quatre stratégies sont distinctes des états de persistance ; aucune n'autorise seule un effacement.

- `DataDeletionStrategy(Enum)` standard, sans mixin : `SOFT_DELETE = "SOFT_DELETE"`, `PHYSICAL_DELETE = "PHYSICAL_DELETE"`, `ARCHIVE = "ARCHIVE"`, `IMMUTABLE = "IMMUTABLE"`, dans l'ordre canonique.
- Module `src/pixs/kernel/data_deletion_strategies.py`, `__all__ = ["DataDeletionStrategy"]`, docstring de frontière, aucun réexport ni fichier existant modifié.
- Aucun membre supplémentaire, alias, défaut, constructeur, parseur, méthode, transition, calcul, politique, autorisation ou effet d'effacement ; aucune immutabilité de ressource dérivée du nom `IMMUTABLE`.
- Delta MODIFIED byte-identique du seul requirement et de son scénario ; archive attendue +0/~0/-0/→0 et spec canonique inchangée.

## Validation

- Stricts ciblés du change et de `data-lifecycle` : exit 0 obligatoire avant et après code, puis strict final après cochage prouvé.
- Globaux `--specs --strict --json --report findings` (76 capacités) et `--all --strict --json --report findings` (77 items : 76 capacités et ce seul change) : conserver sorties et codes natifs. Exit 1 qualifiable uniquement avec les 19 tuples WARNING préexistants exactement identiques (id/type/level/path/message) à la référence de l'archive `2026-10-06-add-initial-notification-contract-representation`, zéro ERROR, aucun autre finding, couverture complète et baseline hors périmètre inchangée. Le code CLI 1 n'est jamais converti en succès. Tout écart impose réconciliation avant poursuite, sans correctif global.
- Trois compilations `py_compile` ciblées, avec l'interpréteur DEVOPS.
- Deux tests unitaires : adhésion normative des noms/valeurs/ordre via `__members__.items()` et export unique ; pas de test des garanties de la stdlib.
- Un test d'intégration `tests/integration/test_data_deletion_strategies_integration.py` : processus frais `-I -B`, environnement réduit `FIXED_ENV`, tempdir sous racine nettoyée, gardes finies open/socket/popen/system/environnement/DB réutilisées ; contrôles positifs avant remise à zéro ; import, tuple canonique et `__all__` vérifiés sous gardes ; compteurs nuls et aucun module DB chargé ; marqueur `DATA_DELETION_STRATEGIES_SAFE_INTEGRATION_OK` seul sur stdout ; assertions finales du parent hors du `with`.
- Régression minimale : `tests.integration.test_kernel_purity` (3 tests) et `tests.integration.test_public_api_facades` (11 tests), total prévu 17 avec les nouveaux tests.
- UTF-8/LF, comparaison des textes autorisés, empreintes des fichiers non concernés sous contrôle CGPT.

## Limites

Vocabulaire pur uniquement, sans runtime, stratégie concrète, défaut, politique, transition, effacement, suppression, purge, restauration, DB ou immutabilité de ressource. Aucun scénario de cycle de vie exécutable livré ni revendiqué. Archivage et statistiques restent des décisions et mandats distincts après preuve des tâches.
