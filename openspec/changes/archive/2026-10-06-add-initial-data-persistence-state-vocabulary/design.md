# Conception — Vocabulaire Enum des états de persistance des données

## Contexte

Source canonique des noms : `openspec/specs/data-lifecycle/spec.md`, exigence « Dimensions et états distincts » : `ACTIVE`, `ARCHIVED`, `SOFT_DELETED`, `PURGE_PENDING`, dans cet ordre. Corroboration `PROJECT.md §2.15` (mêmes quatre états ; `PURGED` peut être représenté par tombstone/journal, hors de cette unité). Patron de couche : `JobState(Enum)` (`src/pixs/kernel/jobs.py`) et `DataSubjectOperation(Enum)` (`src/pixs/kernel/data_subject_operations.py`) — Enum standard sans mixin, module stdlib pur, `__all__`, docstring de frontière. Décision CGPT : `src/pixs/kernel/data_persistence_states.py`, `DataPersistenceState`, sans modification de façade.

## Règles livrées

- `class DataPersistenceState(Enum)` : `ACTIVE = "ACTIVE"`, `ARCHIVED = "ARCHIVED"`, `SOFT_DELETED = "SOFT_DELETED"`, `PURGE_PENDING = "PURGE_PENDING"`, dans cet ordre ;
- `__all__ = ["DataPersistenceState"]`, exactement cette classe ; docstring de frontière : vocabulaire interne des états de persistance seulement ; les noms ne constituent aucune autorisation, obligation juridique, décision de politique, transition, métadonnée ni exécution ;
- Aucun membre supplémentaire (notamment `PURGED`), alias, valeur par défaut, constructeur, wrapper, parseur, variante, méthode, persistance, flux, runtime, purge ni référence exporté.

## Décisions

- `PURGED` est exclu du seul enum des quatre états communs explicitement listés par la source ; cette unité n'affirme pas qu'il ne peut jamais être un état de persistance — `PROJECT.md §2.15` décrit sa représentation par tombstone/journal, hors de ce change ;
- Enum standard sans mixin `str` ; le test unitaire porte sur l'adhésion normative des quatre noms/valeurs/ordre aux sources citées, non sur des garanties propres à la stdlib ;
- Le delta MODIFIED reproduit mot pour mot l'exigence et son scénario ; effet d'archive attendu nul (+0/~0/-0/→0) ; les scénarios « Purge prématurée refusée » et « Restauration sans résurrection » restent non couverts et ne sont pas imputables au vocabulaire ;
- Régression ciblée : les gardes de pureté du Kernel et des façades publiques couvrent l'ajout isolé, sans consommateur existant ;
- La séparation des dimensions métier/rétention/projection et toute sémantique de cycle de vie des données restent hors périmètre.

## Validation prévue (décision technique root explicite pour CE change)

- `openspec validate` strict du change et de la spec `data-lifecycle` : exit 0 obligatoire, avant le code puis après les tests ;
- Contrôles globaux `--specs --strict --json --report findings` et `--all --strict --json --report findings` : sorties brutes et codes réels consignés à chaque passe ; qualification des 19 WARNING de longueur admise pour CE change seulement si exit natif réellement 1, couverture 76 (specs) / 77 (all) complète, identité exacte des issues de la table validée de l'archive `2026-10-06-add-initial-notification-contract-representation`, zéro ERROR et aucun autre texte/emplacement, et baseline des 136 empreintes du présent change inchangée ; toute ERROR, autre WARNING, divergence d'empreinte ou couverture incomplète bloque et déclenche la reprise de récupération hors qualification ; le code CLI 1 n'est jamais converti en succès ;
- Compilations ciblées des trois nouveaux fichiers, résultats natifs ;
- Test unitaire : couples exacts via `__members__.items()`, ordre, pas d'alias, `__all__` ;
- Test d'intégration : processus frais `-I -B`, `FIXED_ENV` réduit (`LANG=C.UTF-8`, `PATH=/usr/bin:/bin`), cwd projet, tempdir sous racine, gardes finies d'effets réutilisées à l'identique des modèles livrés, contrôles positifs avant remise à zéro des compteurs, quatre couples/noms et `__all__` vérifiés sous gardes, compteurs à 0 après usage, aucun module DB chargé, marqueur `DATA_PERSISTENCE_STATES_SAFE_INTEGRATION_OK` seul sur stdout, les quatre assertions finales du parent hors du `with` (sonde dans le `with`) ;
- Régression minimale : `tests/integration/test_kernel_purity.py`, `tests/integration/test_public_api_facades.py` ;
- UTF-8/LF des trois nouveaux fichiers et empreintes des fichiers non concernés.

## Critères observables

Quatre couples `(nom, valeur)` exactement dans l'ordre canonique `ACTIVE`, `ARCHIVED`, `SOFT_DELETED`, `PURGE_PENDING` ; `len(DataPersistenceState) == 4` et `len(__members__) == 4` sans alias ; `__all__` exactement `["DataPersistenceState"]` ; import et vérification en processus frais sans effet observé sur les surfaces gardées ; façade `pixs.kernel.__all__` inchangée.

## Non-goal

Aucune exécution, file, purge, transition, métadonnée de cycle de vie, autorisation, audit, idempotence, propagation, hold, rétention, tombstone, anti‑résurrection, base, runtime, `DataGovernanceProfile`, `DataSubjectRequest` ni immutabilité profonde revendiqués.
