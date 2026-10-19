## MODIFIED Requirements

### Requirement: Assurances et faits du profil PDP minimal fermé v1

Les seuils minimum portent sur chacune des trois dimensions exactes identity_assurance CLAIMED | VERIFIED | PROOFED, authentication_assurance SINGLE_FACTOR | MULTI_FACTOR | PHISHING_RESISTANT et federation_trust UNTRUSTED | TRUSTED | STRONGLY_BOUND, avec ordres indiqués et sans substitution entre dimensions ; la fraîcheur maximale est vérifiée ; tout type, attribut ou fait requis inconnu ou absent MUST être refusé avec effet DENY.

#### Scenario: Fait inconnu refusé fermé

- **WHEN** une condition exige un attribut, un type ou un fait d'assurance absent ou inconnu
- **THEN** la décision est d'effet DENY avec le code public DENIED et un audit

#### Scenario: Assurances non substituables

- **WHEN** une condition exige un niveau d'une dimension d'assurance
- **THEN** aucun niveau d'une autre dimension ne peut y satisfaire
