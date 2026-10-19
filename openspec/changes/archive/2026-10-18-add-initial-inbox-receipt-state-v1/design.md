# Design — add-initial-inbox-receipt-state-v1

## Context

État unique `CONSUMED` canonique : `openspec/specs/events/spec.md` B11 et annexe `InboxReceiptV1`, `src/pixs/backend/bulk_inbox_receipt_values.py` (`_STATES`, chaîne exacte), `src/pixs/backend/bulk_inbox_receipt_record.py` (`choices`, `CheckConstraint`) et tests cibles. Patron de vocabulaire fermé observé : `EventPublicationState(Enum)` de `src/pixs/backend/event_publication_state.py` (membres NOM="NOM", module stdlib pur, `__all__`, docstring de frontière). Décision CGPT : contrat générique pur en `src/pixs/backend/inbox_receipt_state.py`, sans modification de façade ni `__init__`.

## Goals / Non-Goals

Représenter exactement le seul nom/valeur existant `CONSUMED`. Non objectifs : transition, machine d'états, validation métier, diagnostic, factory, persistance, déduplication, transaction, autorisation, exécution, immutabilité profonde.

## Decisions

`class InboxReceiptState(Enum)` à un membre `CONSUMED = "CONSUMED"`, sans mixin `str`, alias, défaut ni comportement ajouté au-delà d'Enum. `validate_bulk_inbox_receipt_values` existant préservé à chaînes exactes ; déduplication métier non dupliquée et restant au repository. Aucun delta normatif ; archivage sans modification du canon attendu.

## Risks / Trade-offs

Un Enum de vocabulaire ne prouve ni la consommation effective ni la déduplication ; la garantie B11 reste portée par l'inbox persistante existante. Un code de sortie non nul de l’archivage reste un échec à diagnostiquer.

## Validation

Compilations ciblées des trois nouveaux fichiers ; tests unitaires significatifs portant sur l'adhésion du vocabulaire à la source canonique citée et sur l'interopérabilité en lecture seule avec le validateur existant, non sur la stdlib ; test d'intégration en processus frais, sans effet ni sortie durables ; régressions structurelles utiles uniquement, sans PostgreSQL ; contrôle UTF-8/LF et empreintes des sources non concernées.
