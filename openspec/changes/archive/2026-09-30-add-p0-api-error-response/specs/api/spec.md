## MODIFIED Requirements

### Requirement: Enveloppes stables et erreurs typées

Le système MUST respecter les garanties suivantes.

Les succès utilisent données, métadonnées et liens avec pagination par curseur ; les erreurs suivent un code métier versionné, un message, des détails et un identifiant de corrélation, sans secret ni trace interne ; les commandes rejouables portent une clé d'idempotence.

#### Scenario: Rejou identique restitué

- **WHEN** la même clé d'idempotence est rejouée avec un contenu identique
- **THEN** le résultat enregistré est restitué au lieu d'un double effet
