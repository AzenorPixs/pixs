# Proposition — add-initial-bulk-authorization-decision-v1

## Why

Le canon bulk-operations, clause B03 et schéma logique AuthorityAssessmentV1, définit exactement les décisions ALLOW, DENY et UNAVAILABLE. Le backend les représente actuellement par des chaînes et constantes privées, sans vocabulaire Enum public isolé.

## What Changes

Ajouter BulkAuthorizationDecision, Enum pur avec les trois valeurs canoniques, dans un module autonome. Vérifier son contrat fermé, les refus sans normalisation, son import sans effet et la préservation des validateurs existants qui exigent des chaînes exactes.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative : les décisions sont déjà définies par bulk-operations. skip_specs: true évite un delta artificiel.

## Impact

Trois nouveaux fichiers Python seulement. Aucun consommateur ni export de façade modifié. Le vocabulaire ne prend aucune décision, ne construit aucun contexte, ne fournit aucune autorisation, transition, conversion, persistance ou exécution. GovernanceResolutionV1 et son vocabulaire RESOLVED/DENY/UNAVAILABLE restent distincts. PostgreSQL et frontend sans objet ; Git non autorisé.
