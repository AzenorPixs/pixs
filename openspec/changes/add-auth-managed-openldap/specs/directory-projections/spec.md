## ADDED Requirements

### Requirement: Service LDAP propre distinct de la projection

Un même service OpenLDAP MAY héberger projection de consultation et authentification propre, mais chaque capacité MUST être déclarée et sélectionnée séparément. Le contrat directory-projections MUST rester sans authentification, permission ou décision de révocation. Le partage de processus MUST NOT étendre les données et droits autorisés de la projection.

#### Scenario: Processus commun deux capacités

- **WHEN** un OpenLDAP géré fournit une projection et une authentification déclarées séparément
- **THEN** la consultation garde ses règles de projection et aucune confiance d'authentification n'est déduite de son repli PostgreSQL
