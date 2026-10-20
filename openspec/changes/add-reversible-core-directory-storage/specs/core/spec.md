## MODIFIED Requirements

### Requirement: Primitives minimales communes

pixs.core MUST exposer utilisateurs, identités numériques, groupes, appartenances, tenants, rôles, ACL et permissions via contrats publics. PostgreSQL MUST être le stockage par défaut. Une migration postinstallation conforme à core-storage MAY sélectionner l'OpenLDAP interne comme référence du périmètre engagé, avec retour obligatoire. La projection de consultation MUST rester distincte et son repli PostgreSQL MUST NOT s'appliquer à un stockage LDAP autoritatif.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module a besoin d'une identité ou d'une appartenance
- **THEN** il passe par le contrat ou le service exposé, sans accès direct aux tables internes

### Requirement: Autorités et limites du profil identité structurel

Django MUST rester l'autorité métier et transactionnelle selon les garanties qualifiées du provider. PostgreSQL MUST rester la source applicative sauf le périmètre Core explicitement engagé vers OpenLDAP interne selon core-storage. Les mutations MUST conserver persistance, autorisation et audit. Le profil structurel MUST NOT déduire transitions, temps ou assurance du seul type ou état.

#### Scenario: Identité structurelle sans assurance implicite

- **WHEN** un modèle satisfait le profil structurel d'identité
- **THEN** son type ou son état ne définit pas implicitement de transition, règle temporelle ou niveau d'assurance, et les mutations restent sous l'autorité backend
