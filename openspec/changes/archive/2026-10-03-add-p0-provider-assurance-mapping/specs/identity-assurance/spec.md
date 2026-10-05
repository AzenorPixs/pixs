## MODIFIED Requirements

### Requirement: Contexte vérifié et dimensions distinctes

Le système MUST respecter les garanties suivantes.

Toute authentification réussie produit un contexte vérifié, limité dans le temps, rattaché à une identité numérique et au périmètre applicable, avec assurance d'identité, assurance d'authentification et confiance fédérée évaluées séparément selon le mapping déclaré du fournisseur.

#### Scenario: Claim absent sans surclassement

- **WHEN** une preuve ou un claim est absent, ambigu ou expiré
- **THEN** le niveau d'assurance n'est jamais augmenté implicitement
