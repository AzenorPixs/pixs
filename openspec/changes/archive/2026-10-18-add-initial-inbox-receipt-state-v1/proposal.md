# Proposal — add-initial-inbox-receipt-state-v1

## Why

La spécification canonique `events` B11 et l'annexe `InboxReceiptV1` imposent l'état unique `CONSUMED`, mais aucun module Python ne représente ce vocabulaire (grep `InboxReceiptState` sans résultat en `src/` et `tests/` ciblés). Sans représentation unique, chaque futur consommateur reproduirait l'état par des chaînes libres, source de divergences silencieuses.

## What Changes

- Publier `src/pixs/backend/inbox_receipt_state.py` : contrat générique pur `InboxReceiptState(Enum)` avec le seul membre `CONSUMED = "CONSUMED"`, sans mixin `str`, alias, défaut, validation ni runtime.
- Publier un test unitaire significatif du vocabulaire et un test d'intégration d'import en processus frais sans effet, prouvant aussi que la chaîne `CONSUMED` reste admise par `validate_bulk_inbox_receipt_values` existant et que le membre Enum direct reste refusé sans modifier le validateur.
- Aucun fichier existant modifié, aucune façade ni `__init__` touché.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification de texte canonique. `skip_specs: true` évite un delta identique artificiel.

## Impact

Fondation partielle : représente l'état, ne prouve ni persistance, déduplication, transaction, autorisation ni exécution. La convention Enum standard n'offre pas d'immutabilité profonde et il n'en est promis aucune. Pas de tests PostgreSQL pour ce vocabulaire pur ; DB/frontend non pertinents (N/A).
