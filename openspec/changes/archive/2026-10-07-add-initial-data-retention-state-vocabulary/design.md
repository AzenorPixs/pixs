# Design — Vocabulaire Enum des états communs de rétention des données

## Contexte et source normative
Source unique : `openspec/specs/data-lifecycle/spec.md`, requirement « Dimensions et
états distincts », tuple `(RETAINED, LEGAL_HOLD, ELIGIBLE_FOR_PURGE)` dans cet ordre,
corroboré par TECHNICAL.md §14.1. Les garanties d'ordre et d'unicité des membres sont
celles de la stdlib `enum` et ne sont pas re-testées.

## Décisions
- Représentation : `class DataRetentionState(Enum)` avec trois membres
  `RETAINED = "RETAINED"`, `LEGAL_HOLD = "LEGAL_HOLD"`, `ELIGIBLE_FOR_PURGE = "ELIGIBLE_FOR_PURGE"` ;
  `__all__ = ["DataRetentionState"]` ; docstring de frontière (aucun défaut, aucune
  transition, aucun calcul d'éligibilité, aucune politique, aucune autorisation de purge,
  aucun état `PURGE_PENDING`/`PURGED` repris ici).
- Module dédié `src/pixs/kernel/data_retention_states.py` ; pas de réexport dans
  `pixs.kernel.__init__` (convention observée : la façade du paquet ne liste que
  `composition`, `config`, `diagnostics`, `lifecycle`, `manifest`, `registry`).
- Compatibilité de la garde de pureté du noyau : les trois valeurs sont en anglais et ne
  correspondent à aucun concept métier interdit de `tests/integration/test_kernel_purity.py`
  (`utilisateur, groupe, acl, organisation, annuaire, oidc, saml, document, flux`) ;
  `pixs.core` n'est pas codé en dur.
- Tests unitaires : adhésion exacte des noms/valeurs/ordre via
  `DataRetentionState.__members__.items()`, absence de membre ou d'alias supplémentaire,
  `__all__` exact.
- Test d'intégration : import en processus frais `-I -B` sous `FIXED_ENV` réduit, gardes
  ouvertes/sockets/processus/environnement/DB réutilisées, contrôles positifs avant remise
  à zéro, couples et `__all__` vérifiés sous gardes, marqueur
  `DATA_RETENTION_STATES_SAFE_INTEGRATION_OK` seul sur stdout, assertions finales hors du
  `with`, sans nouvelle dépendance.
- Régression minimale : `tests.integration.test_kernel_purity` (3 tests) et
  `tests.integration.test_public_api_facades` (11 tests), soit 14 tests ; aucune autre
  suite n'est exécutée sans raison.

## Règle de qualification des validations globales
Les CLI globaux conservent leur résultat natif : exit 1 n'est jamais converti en succès.
`--specs --strict --json --report findings` (couverture 76 capacités) et
`--all --strict --json --report findings` (couverture 77 items : 76 capacités et ce seul change) sont qualifiables uniquement si les findings
observés sont exactement les 19 tuples WARNING préexistants
(« Requirement text is very long (>500 characters) », id/type/level/path/message identiques
à la référence), zéro ERROR et aucun finding nouveau ; tout écart est consigné sans correctif.
Les stricts ciblés du change et de `data-lifecycle` doivent être exit 0 avant et après code.
UTF-8/LF des artefacts et empreintes des fichiers non concernés sont sous contrôle CGPT.

## Sorties attendues
L'archivage de ce delta doit laisser la spec canonique inchangée au byte près (effet attendu 0),
le delta n'introduisant aucun texte normatif nouveau.

## Limites

Fondation partielle de vocabulaire uniquement : aucune clôture de l’exigence entière ni des scénarios de suppression, purge ou restauration. Aucun défaut, transition, calcul d’éligibilité, politique, autorisation de purge, runtime, DB ou métadonnée ajouté. Référence des 19 tuples : archive `2026-10-06-add-initial-notification-contract-representation`, comparaison par CGPT ; toute divergence de la baseline hors périmètre impose réconciliation avant poursuite.
