# Proposition — contrat de source de fanions

## Why
R2 exige une configuration canonique de cohorte et R4 exige une source persistante versionnée. L'évaluation actuelle attend des affectations et une règle injectées séparément. Ce contrat ajoute une validation de snapshot fermé sans livrer la persistance.

## What Changes
- Ajouter `FeatureFlagSourceSnapshot` figé à quatre champs et son validateur.
- Ajouter une évaluation bornée à partir d'un snapshot : vérification complète du lot, du numéro attendu, de la définition, des affectations et de la règle exacte, puis appel réel à la composition existante.
- Deux suites nouvelles ; aucune source préexistante modifiée.

## Capabilities
### Modified Capabilities
- `feature-flags` : R2 et R4 déjà validées ; le delta reproduit le canonique sans nouvelle norme.

## Impact
Trois nouvelles sources : module, unit et intégration. Les 22 baselines et les 119 tests restent inchangés. Aucun PostgreSQL, cache, TTL, rôle web/worker/scheduler, administration, audit, frontend, migration, secret ou nouvelle dépendance. Le snapshot valide une cohérence injectée, mais sa provenance persistante reste confiance de l'appelant jusqu'à une unité suivante.
