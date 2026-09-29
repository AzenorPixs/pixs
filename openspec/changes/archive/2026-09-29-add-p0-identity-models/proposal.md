# Proposal

## Why

Le profil identité minimal v1 de `core/spec.md` est validé, mais aucun modèle ni validateur de ce profil n'est présent dans `pixs.core`. Ce socle rend vérifiables les identifiants, vocabulaires et cardinalités avant leur intégration persistante.

## What Changes

- Modèles immuables `User`, `DigitalIdentity` et `IdentityLink`, UUIDv7 et enums fermés.
- Validation structurelle défensive des entités et d'un ensemble de liaisons explicites, avec unicité dans chaque sens et références existantes.
- Représentation d'un compte de service par une identité SERVICE, sans exiger de User et sans accorder de droit.
- Façade publique `pixs.core.identity` et tests de conformité sur données synthétiques.
- Aucun état mutable de registre ni opération métier persistante.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune : implémentation du profil déjà normé dans `core/spec.md`, sans delta normatif.

## Impact

- Trois sources : `src/pixs/core/identity/models.py`, `src/pixs/core/identity/__init__.py`, `src/pixs/core/__init__.py`.
- Deux suites unitaires modèles et liaisons ; une suite d'intégration de façade.
- Aucune nouvelle dépendance ; stdlib compatible Python >=3.11, contrôlée avec l'exécutable DEVOPS.
- Exclus : authentification réelle, provider concret, sessions, tokens, génération/parsing d'identifiants externes, transitions d'état, CRUD, migration et persistance.
- Django reste l'autorité métier et transactionnelle, PostgreSQL la source de vérité. Ce socle ne satisfait pas à lui seul les exigences d'authentification, d'audit durable ou de backend complet.
