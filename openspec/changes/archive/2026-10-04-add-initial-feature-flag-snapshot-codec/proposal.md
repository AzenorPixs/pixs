# Proposition — codec backend pur du snapshot source

## Why
Les normes canoniques R2 et R4 exigent une configuration serveur persistante, versionnée et auditable. Avant le branchement PostgreSQL, ce change fournit uniquement une conversion fidèle entre un `FeatureFlagSourceSnapshot` déjà injecté et un document JSON-compatible, afin d’isoler le formatage de la lecture persistante et de l’administration.

## What Changes
- Ajouter `src/pixs/backend/feature_flag_snapshot_codec.py` avec `encode_feature_flag_source_snapshot(snapshot)` retournant un `dict` et `decode_feature_flag_source_snapshot(document)` retournant un `FeatureFlagSourceSnapshot`.
- Ajouter l’exception `FeatureFlagSnapshotCodecError(ValueError)`, portant un message fixe et ne reproduisant aucune donnée refusée.
- Valider réellement le lot avant toute extraction et après reconstruction complète du modèle.
- Convertir récursivement les tuples canoniques en listes neuves, puis les listes exactes en tuples, sans `asdict`, copie générique ni normalisation.
- Ajouter les suites unitaire et d’intégration correspondantes.
- Ne modifier aucun module, aucune suite, aucun export ni aucune documentation existante.

## Capabilities
### Modified Capabilities
- `feature-flags` : les exigences R2 et R4 sont reproduites mot pour mot dans le delta ; aucune nouvelle norme fonctionnelle n’est introduite.

## Impact
Trois sources nouvelles seulement. Environnement Python 3.12 minimum, exécution sur 3.14.8, 27 baselines et 136 régressions préservées. Aucune E/S, PostgreSQL, horloge, environnement, audit, service runtime, cache, API frontend, README ou dépendance nouvelle. Le codec ne prouve ni la provenance ni la persistance du lot : il en conserve seulement la structure canonique et laisse les résultats `INVALID` de R3 à l’évaluateur existant.
