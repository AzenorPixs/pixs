## MODIFIED Requirements

### Requirement: Idempotence et traçabilité des commandes

Toute commande rejouable MUST porter identifiant, corrélation, causalité, contexte de périmètre et clé d'idempotence ; un rejou à contenu identique restitue le résultat, à contenu divergent produit un conflit explicite.

#### Scenario: Rejou divergent

- **WHEN** la même clé d'idempotence est réutilisée avec un contenu différent
- **THEN** le système retourne un conflit explicite au lieu d'un double effet
