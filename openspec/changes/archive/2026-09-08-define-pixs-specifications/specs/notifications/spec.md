## Purpose

Les notifications acheminent les informations aux destinataires via des canaux déclarés, de façon asynchrone, dédupliquée et confidentielle.

## ADDED Requirements

### Requirement: Contrats et préférences déclarés

Chaque notification DOIT suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée.

#### Scenario: Canal non déclaré refusé

- **WHEN** un envoi vise un canal non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite

### Requirement: Asynchronisme avec réessais bornés

Les envois utilisent des travaux persistants avec réessais bornés, déduplication et lettres mortes ; l'épuisement produit un état diagnostiquable sans perte silencieuse.

#### Scenario: Échec persistant tracé

- **WHEN** les réessais sont épuisés
- **THEN** la notification passe en lettre morte avec audit et sans divulgation de contenu sensible

### Requirement: Confidentialité et audit

Les notifications DOIVENT respecter la classification et la gouvernance, minimiser le contenu, ne jamais exposer de secret, et tracer acteur, action et cible sans journaliser les données sensibles.

#### Scenario: Donnée protégée minimisée

- **WHEN** une notification concerne une donnée classifiée
- **THEN** seuls les champs nécessaires sont transmis et l'envoi est audité
