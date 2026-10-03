## Why

La fabrique JSON d'erreur existe ; l'enveloppe de succès data/meta/links et sa représentation JSON Django restent sans preuve. L'exigence API 2 et TECHNICAL.md §25 décrivent cette forme publique et le transport JSON UTF-8.

## What Changes

- Ajouter un constructeur pur d'enveloppe de succès avec validation de JSON fini, types exacts et copie profonde.
- Ajouter une fabrique JsonResponse 200 non streaming, après validation pure puis imports Django paresseux.
- Préserver les façades et documents existants et vérifier le transport dans des processus Django isolés.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `api` : réalisation partielle de « Enveloppes stables et erreurs typées », limitée à l'enveloppe de succès et à sa fabrique JSON 200.

## Impact

Cinq fichiers : success.py, façade et README API ajoutés à la fin, tests unitaires et d'intégration. Aucun autre module, aucune dépendance nouvelle ni mise à jour canonique.

Aucune route, serveur, middleware, authentification, tenant, curseur, idempotence, cache, statut alternatif, suivi asynchrone, génération d'identifiant ou de date, schéma ou publication OpenAPI. Le contrat du module appelant valide le domaine et choisit les seules données publiques non sensibles. Cette fabrique n'est pas un filtre universel de secrets et n'atteste pas la conformité globale API ou P0.
