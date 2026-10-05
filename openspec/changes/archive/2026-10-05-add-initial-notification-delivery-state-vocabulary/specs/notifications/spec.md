# notifications

## MODIFIED Requirements

### Requirement: Asynchronisme avec réessais bornés

Le système MUST respecter les garanties suivantes.

Les envois utilisent des travaux persistants avec réessais bornés, déduplication et lettres mortes ; l'épuisement produit un état diagnostiquable sans perte silencieuse.

#### Scenario: Échec persistant tracé

- **WHEN** les réessais sont épuisés
- **THEN** la notification passe en lettre morte avec audit et sans divulgation de contenu sensible
