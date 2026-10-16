# Proposal — qualify-pdp-authentication-federation-vocabularies-v1

## Why
Les deux enums exactes `AuthenticationAssurance` et `FederationTrust` existent déjà dans `src/pixs/core/authz/policy.py` et sont normées par `authorization-engine` § Assurances et faits du profil PDP minimal fermé v1. Il manque une qualification dédiée de leur fermeture et de l'identité des classes entre consommateurs en processus frais.

## What Changes
Deux tests futurs seuls (`tests/unit/test_authentication_federation_vocab.py` et `tests/integration/test_authentication_federation_vocab_integration.py`), aucune production ni façade changée. Delta de traçabilité reprenant toute l'exigence canonique mot pour mot et les scénarios existants seulement, sans exigence ni scénario nouveau.

## Capabilities
Aucune capacité nouvelle. Capacité existante concernée : `authorization-engine` (conformité des vocabulaires préparatoires `AuthenticationAssurance` et `FederationTrust` v1 qualifiée, traçabilité seule).

## Impact
Seuls artefacts du change et tests dédiés. Aucune authentification, session, accès, audit ou persistance nouveau. Pas de nouvel Enum, ni mapping, ordre ou transition. Les deux tests ne sont pas encore réservés en écriture ; préparation seule maintenant. Archive et STATISTIQUES après preuves, sous mandats séparés.
