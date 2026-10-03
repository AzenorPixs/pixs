## Why

La projection publique d'erreur d'infrastructure est disponible, mais aucune fabrique de réponse JSON Django ne la matérialise. TECHNICAL.md §25 impose la normalisation à la frontière API, le statut HTTP complémentaire et le format JSON UTF-8 ; le runtime Django est déjà retenu.

## What Changes

- Ajouter une fabrique backend de JsonResponse HTTP 500 non streaming, dont le corps est exactement l'enveloppe publique existante.
- Importer Django seulement lors de l'appel, après validation de la projection publique, sans configurer le runtime.
- Préserver les façades et documents existants par ajout minimal et vérifier les réponses dans des processus synthétiques isolés.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `api` : réalisation partielle de « Enveloppes stables et erreurs typées », limitée à la fabrique de réponse d'infrastructure.

## Impact

Cinq fichiers d'implémentation : responses.py, façade et README API, deux suites de tests. Les cinq artefacts OpenSpec préparent ce seul change ; aucune modification canonique.

Aucune route, serveur, middleware, authentification, tenant, génération UUID, en-tête de corrélation, cache, rejeu persistant, pagination, publication OpenAPI, connexion PostgreSQL, secret, nouvelle dépendance ou activation. Le statut fixe 500 est un choix d'implémentation pour l'erreur serveur inattendue, sans classification métier. L'exigence API complète et P0 restent partiellement réalisés.
