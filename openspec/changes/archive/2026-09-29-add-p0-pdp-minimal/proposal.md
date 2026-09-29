# Proposal

## Why

Aucun PDP exécutable du profil minimal v1 n'existe : les exigences `authorization-engine` et `TECHNICAL §12.5` sont validées mais sans moteur mémoire testable. Sans ce socle, l'évaluation DENY prioritaire, les obligations et l'échéance ne peuvent être vérifiées avant le backend réel.

## What Changes

- PDP mémoire pur stdlib sous `pixs.core/authz` : `authorize` recalcule réellement à CHAQUE appel, sans cache ni argument de décision précédente.
- Faits exclusivement via port backend `TrustedFactsProvider` injecté par composition de confiance, jamais paramètre HTTP ni dict booléen ; sujet, ressource, action et ScopeContext canoniques appariés, contexte d'auth vérifié frais et non révoqué fourni par le port, avec validation défensive.
- Ports horloge et snapshot cohérents ; fin d'ALLOW à l'horizon incluant tout DENY futur autrement correspondant.
- Limites positives explicitement requises et validées, sans défaut inventé.
- Audit via port injecté, refus observables et audités, échecs du port fermés ; un ALLOW reste une proposition d'accès avec obligations à honorer par le PEP, sans revendiquer un audit durable.
- ScopeContext topologiquement validé via snapshot existant, PLATFORM et intertenant conformes au profil minimal.
- Vocabulaire source faisant autorité ; types et noms d'API techniques détaillés dans le design avant code.
- Tests sur ports simulés, qui ne prouvent pas la sécurité du backend réel.
- Entrées invalides refusées sans disparaître pour laisser un ALLOW d'une autre politique.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune : le change implémente des exigences normatives existantes, sans nouvelle exigence ni modification normative.

## Impact

- Code : `src/pixs/core/authz/` (façade, politiques, snapshot, décision, ports), détail en design.
- Tests : unitaires politiques/décision/temps, intégration audit sur doubles mémoire, fixtures synthétiques sans secret.
- Exclus : PEP Django, PostgreSQL, filtrage source, caches, audit durable, providers concrets, frontend, dépendances nouvelles, runtime complet et P0 global.
- Obligations restantes d'intégration : construction réelle des AuthenticationContext par le backend, PEP effectif, persistance, audit durable et composition de référence relèvent de changes ultérieurs ; ce socle ne simule pas un runtime complet.
