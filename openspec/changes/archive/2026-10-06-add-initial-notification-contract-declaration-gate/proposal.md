# Proposition — Liaison des gardes déclaratives de notification au contrat validé

## Why

L'exigence canonique « Contrats et préférences déclarés » et ses deux scénarios (openspec/specs/notifications/spec.md) imposent le refus d'un canal ou destinataire « non déclaré par le contrat ». Or les gardes `notification_channel_declaration` et `notification_recipient_declaration` opèrent sur tout frozenset fourni par l'appelant, et `notification_contract` ne porte que la représentation structurelle : rien ne relie les refus aux ensembles déclarés DU contrat. La recherche dans les sources confirme l'absence de consommateur croisé. Cette unité ajoute seule cette liaison, sans trancher aucune règle non spécifiée.

## What Changes

- Ajouter `src/pixs/kernel/notification_contract_declaration.py` : deux fonctions publiques `require_contract_declared_channel` et `require_contract_declared_recipient` ; validation intégrale du contrat par `validate_notification_contract` réutilisé, contrat invalide refusé par `NotificationContractDeclarationError(ValueError)` à message fixe sans écho, puis délégation stricte aux deux gardes existantes avec `contract.channels` et `contract.recipient_keys`, classes d'erreur propres préservées ;
- Ajouter un test unitaire et un test d'intégration en processus frais ;
- Delta `specs/notifications/spec.md` MODIFIED reproduisant mot pour mot l'exigence R1 et ses deux scénarios canoniques, sans norme nouvelle.

## Impacts

- Aucun comportement runtime, aucune source, test, façade ou export existant modifié ; aucune logique de validation réinventée ;
- Aucun envoi, provider, file, réessai, déduplication, lettre morte, persistance, résolution des références de préférence ou de périmètre, consentement ni audit réel ; les contrats de réessai/déduplication/persistance relèvent d'un périmètre distinct ultérieur ;
- Effet canonique effectif attendu nul (+0/~0/-0/→0) ; R2 et R3 restent non couverts.
