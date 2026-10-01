# Premier shell TanStack local

## Why

La spécification initial-application-bootstrap requiert un shell TanStack, alors qu’aucun frontend compilable n’est présent. Le développeur a validé séparément les quatre dépendances exactes proposées.

## What Changes

- Fournir un premier shell local construit séparément, avec une unique route publique `/`, un refus des chemins inconnus et aucun appel API.
- Externaliser les textes dans des catalogues canoniques anglais et français vérifiés au build, et fournir les modes clair/sombre avec préférences en mémoire.
- Déclarer les dépendances exactes, le build, les tests natifs et le cycle de vérification sur loopback.
- Documenter le jalon partiel : aucune composition Django/P0 prête ni vérification intégrée backend/frontend n’est acquise.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : premier jalon de l’exigence existante « Shell TanStack initial intégré », reprise normative inchangée.

## Impact

Nouveaux fichiers sous frontend/ uniquement, plus artefacts de ce change. Dépendances directes autorisées : @tanstack/react-router 1.170.41, react 19.3.0, react-dom 19.3.0 et vite 8.3.1. Aucun PostgreSQL, secret, Git, déploiement, provider LLM ou configuration OpenCode.
