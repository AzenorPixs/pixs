## MODIFIED Requirements

### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, `pixs.auth` essentiel avec son authentification locale autonome et PostgreSQL par défaut, le contexte tenant/scope, l'autorisation, les API et contrats publics, migrations, runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance, cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication

## ADDED Requirements

### Requirement: Profil Auth standard sans connecteur externe installé

Le profil standard MUST sélectionner explicitement la capacité locale Auth PostgreSQL. Les connecteurs vers LDAP, Kerberos ou autres sources externes MUST être absents de l'installation standard et installés seulement sur sélection explicite. Les services OpenLDAP, KDC et Active Directory propres ainsi que l'émission d'identité sortante MUST rester non activés par défaut et MUST NOT conditionner l'autonomie locale.

#### Scenario: Profil livré sans connecteurs externes
- **WHEN** le profil standard est installé
- **THEN** la recette vérifie le fonctionnement local sur PostgreSQL, l'absence des connecteurs externes et l'absence de service LDAP/KDC/AD ou d'émission sortante activé implicitement
