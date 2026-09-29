# Proposal

## Why

Aucune fondation exécutable du ScopeContext clarifié n'existe : les exigences `scope-context` TENANT/PLATFORM, la topologie tenant/scope et la propriété canonique sont spécifiées mais sans modèle immuable testable. Sans ce socle, `pixs.core`, l'autorisation et la composition P0 ne peuvent pas s'appuyer sur un contexte stable.

## What Changes

- Fondation pure Python stdlib sous `pixs.core` : ScopeContext immuable dès construction (TENANT avec tenant requis, PLATFORM sans tenant ni scope), identifiants mémoire opaques non vides sans exigence namespacée arbitraire ni UUIDv7 (UUIDv7 pour persistance future seulement).
- Validation structurelle distincte de la topologie et de l'autorisation : parent racine explicite via tenant + parent_scope optionnel, refus doublons/référence absente/cycle/inter-tenant, snapshots immuables, ordre déterministe sans dépendre de l'ordre d'entrée.
- Propriété canonique ressource distincte des droits : tenant racine, scope enfant cohérent ou platform hors tenant ; le partage ne change pas le propriétaire.
- Propagation stricte : comparaison de toute prétention au contexte canonique, refus de tout changement explicite aussi (aucune divergence ignorée silencieusement), contrat callback audit injectable pour signaler les refus sans prouver un audit persistant ; un ScopeContext ne donne jamais droit.
- Modularité réduite aux fichiers nécessaires avec `src/pixs/core/__init__.py` et façade publique, sans fonction identité artificielle.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune : le change implémente des exigences normatives existantes (`scope-context`, `core`, `authorization`), sans nouvelle exigence ni modification normative.

## Impact

- Code : `src/pixs/core/__init__.py` et façade, modèles ScopeContext frozen, topologie, propriété, propagation avec callback audit (détail en design).
- Tests : unitaires structure/topologie/propriété, intégration propagation sur fixtures synthétiques sans secret, preuves reproductibles.
- Exclus : stockage PG, Django/ORM, HTTP/API, PDP/PEP concret, audit persistant, providers concrets, frontend, dépendances nouvelles, P0 global.
- Obligations restantes d'intégration : persistance future, PDP applicatif, audit durable et composition de référence relèvent de changes ultérieurs ; ce socle ne simule pas un runtime complet.
