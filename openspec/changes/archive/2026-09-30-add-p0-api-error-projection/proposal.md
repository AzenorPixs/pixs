# Proposal: add-p0-api-error-projection

## Why

TECHNICAL §25 exige que les erreurs publiques d'infrastructure soient
normalisées par la frontière API sans secret, sans stack trace et sans
détail de persistance (`TECHNICAL.md:1291`). Aucune fondation pure ne
prouve aujourd'hui cette projection. Ce change fournit la seule brique
mûre en stdlib : la projection PUBLIC constante d'une erreur
d'infrastructure vers l'enveloppe d'erreur à 5 champs nommés.

## What Changes

Factory pure `build_infrastructure_error(correlation_id, *,
internal_error) -> dict` dans `src/pixs/backend/api/errors.py` (stdlib
`uuid` seule) : `internal_error` opaque requis mais jamais inspecté,
converti, exécuté ni exposé ; `correlation_id` UUID exact revalidé puis
sérialisé canoniquement ; enveloppe exacte `error_code` /
`message` / `details` / `field_errors` / `correlation_id` avec
constantes publiques documentées et conteneurs frais par appel.

## Capabilities

### New

None.

### Modified

- `api` : ajoute la projection d'erreur d'infrastructure (fondation
  partielle de « Enveloppes stables et erreurs typées », portée
  restreinte ci-dessous).

## Impact

Portée partielle explicite : ce change NE prouve NI le rejeu
d'idempotence (scénario « Rejou identique restitué » toujours non
prouvé, persistance absente), NI la pagination par curseur, NI le
tenant canonique, NI l'authentification, NI le transport HTTP, NI la
génération ou validation OpenAPI, NI aucune attestation de mapping
HTTP. La requirement2 globale reste normative et non achevée ; seule
la projection constante d'erreur d'infrastructure est prouvée. Aucune
nouvelle norme, aucune dépendance, aucun fichier préexistant modifié
hors appends minimaux `__init__.py` et `README.md` (préfixe actuel
conservé intégralement).
