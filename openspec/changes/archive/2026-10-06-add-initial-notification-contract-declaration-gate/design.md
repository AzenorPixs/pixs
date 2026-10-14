# Design — Liaison des gardes déclaratives au contrat validé

## Frontière

Le module n'ajoute aucune validation propre. Il compose : `validate_notification_contract` (existant) puis la garde déclarative (existante) sur l'ensemble déclaré DU contrat.

## Contrat technique

- Fichier : `src/pixs/kernel/notification_contract_declaration.py` ;
- exports publics exacts : `NotificationContractDeclarationError`, `require_contract_declared_channel`, `require_contract_declared_recipient` ;
- `NotificationContractDeclarationError(ValueError)` : levée lorsque `validate_notification_contract(contract)` retourne une liste non vide, message fixe unique `« contrat de notification valide exact attendu »`, sans écho d'aucun diagnostic, champ ou valeur ;
- `require_contract_declared_channel(contract, channel) -> NotificationChannel` : valide d'abord le contrat dans son ensemble ; si valide, retourne `require_declared_notification_channel(channel, contract.channels)` ;
- `require_contract_declared_recipient(contract, recipient_key) -> str` : symétrique avec `require_declared_notification_recipient(recipient_key, contract.recipient_keys)` ;
- les erreurs `NotificationChannelDeclarationError` et `NotificationRecipientDeclarationError` des gardes propagent inchangées ; aucun attribut de `contract` n'est lu avant validation du type exact par le validateur ; aucune méthode invoquée sur une valeur non validée ;
- docstring de frontière : aucun envoi, provider, file, réessai, déduplication, lettre morte, persistance, préférence résolue, périmètre résolu, consentement, audit ni exécution.

## Tests

- unitaire : contrat valide déclaré/non déclaré pour chaque garde ; contrat invalide par chacun des cinq champs refusé sans écho ; sous-classes et conteneurs hostiles ; distinction des trois classes d'erreur ;
- intégration : import en processus frais sous gardes d'effets, marqueur fixe, adhésion des exports, modèle des changes archivés du 2026-10-05.
