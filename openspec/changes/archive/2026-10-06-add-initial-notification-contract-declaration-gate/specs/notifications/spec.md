# notifications

## MODIFIED Requirements

### Requirement: Contrats et préférences déclarés

Chaque notification MUST suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée.

#### Scenario: Canal non déclaré refusé

- **WHEN** un envoi vise un canal non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite

#### Scenario: Destinataire élargi refusé

- **WHEN** un envoi vise un destinataire non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite
