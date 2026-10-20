## ADDED Requirements

### Requirement: Rôle fournisseur distinct des connecteurs entrants

pixs.auth MUST pouvoir fournir l'identité à des applications clientes par sous-modules émetteurs OIDC et SAML. Chaque protocole MUST être activé explicitement et MUST pouvoir utiliser l'authentification locale PostgreSQL sans connecteur vers un fournisseur externe. Un rôle émetteur MUST NOT être sélectionné comme connecteur entrant par confusion.

#### Scenario: Pixs émetteur autonome

- **WHEN** un client approuvé utilise le rôle OIDC activé sur une installation locale sans fournisseur externe
- **THEN** Pixs peut établir l'authentification et émettre l'identité selon le contrat sélectionné

#### Scenario: Protocole non activé

- **WHEN** un client demande une émission SAML alors que seul OIDC est activé
- **THEN** aucune assertion SAML n'est émise

### Requirement: Confiance explicite des clients et destinations

Toute émission MUST vérifier client, issuer, audience, destinations, validité et protections anti-rejeu du profil sélectionné. Une destination non enregistrée ou une demande ambiguë MUST être refusée avant remise d'un artefact. Les métadonnées découvertes MUST NOT accorder seules la confiance.

#### Scenario: Destination non approuvée

- **WHEN** une demande cible une destination absente de la configuration approuvée
- **THEN** aucun code, jeton ou assertion n'est remis à cette destination

### Requirement: Attributs publiés minimisés et contextualisés

L'émetteur MUST publier seulement les attributs et sujets autorisés pour le client, la finalité et le tenant applicables. Il MUST préserver les dimensions d'assurance réellement obtenues. Un rôle ou l'exception Super Admin Pixs MUST NOT devenir automatiquement un privilège dans l'application cliente.

#### Scenario: Client du tenant A

- **WHEN** un client autorisé seulement dans A demande les appartenances ou attributs du tenant B
- **THEN** l'émission ne divulgue aucun attribut de B ni droit implicite

### Requirement: Clés et révocation d'émission maîtrisées

L'émetteur MUST protéger et tourner ses clés, borner les artefacts et révoquer grants et contextes selon la politique déclarée. Il MUST distinguer révocation locale, notification et effet chez les clients. Une garantie de révocation tierce non prouvée MUST NOT être annoncée.

#### Scenario: Session locale révoquée

- **WHEN** Pixs révoque une session utilisée pour émettre vers un client
- **THEN** les nouvelles émissions et renouvellements concernés sont refusés et les limites de propagation au client sont explicites
