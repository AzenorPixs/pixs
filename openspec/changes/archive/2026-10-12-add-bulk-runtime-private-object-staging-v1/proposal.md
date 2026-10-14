## Why

Les fondations de contrats, ports, parsing et persistance Bulk sont livrées. B04 nécessite maintenant un contrat ObjectMetadataV1 contrôlé et des primitives d'intégrité d'objet bornées avant la future composition du worker, sans confondre références, intégrité et autorisation.

## What Changes

- Valider exactement les onze clés et types ObjectMetadataV1 et produire des snapshots internes détenus.
- Vérifier un flux mémoire fourni en bytes exacts, sa taille et son SHA-256 complet sous PolicyV1, échéance et cancellation serveur explicites.
- Comparer métadonnées observées et attendues fournies par le serveur, sans déduire un contexte d'autorité depuis une référence.
- Examiner statiquement la structure ObjectStoragePort ; absence de garantie de version qualifiée reste explicitement indisponible.
- Qualifier les preuves comme primitives B04 sans provider réel, worker ou objet effectivement créé.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- object-storage : fondations du Requirement Runtime Bulk v1 B04 existant, recopié verbatim avec ses scénarios, sans nouvelle clause ou annexe.

## Impact

Trois nouveaux Python (module backend, tests unitaires, intégration fraîche) et quatre artefacts. Aucun I/O direct, provider de production, copie locale de secours, worker/admission, mutation propriétaire, ORM/migration, idempotence/outbox SQL, HTTP, PA/PZT, dépendance, Git ou infrastructure. Archive unique puis STATISTIQUES distinct et retour SÉLECTION.
