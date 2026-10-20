# Stockage Core réversible PostgreSQL et OpenLDAP interne

## Why

Le canon actuel autorise une projection LDAP de consultation uniquement, avec PostgreSQL comme source de vérité. Le choix postinstallation de déplacer les utilisateurs, groupes et ACL vers l'OpenLDAP interne puis de revenir à PostgreSQL nécessite un véritable provider de stockage Core et un protocole de migration réversible.

## What Changes

- **BREAKING** : permettre au stockage Core sélectionné d'être PostgreSQL par défaut ou OpenLDAP interne après migration autorisée, sans déplacer l'autorité métier Django.
- Inclure utilisateurs, groupes, ACL et leurs relations nécessaires ; conserver UUID, sémantique des droits, versions et révocations.
- Prévoir sélection postinstallation, préparation, copie vérifiée, clôture des écritures et engagement d'une génération unique.
- Exiger le retour depuis les données LDAP courantes, sans simple réactivation de l'ancienne copie PostgreSQL.
- Distinguer ce stockage de la projection de consultation, des ACL techniques slapd et de l'authentification.
- Conserver PostgreSQL pour les autres données applicatives et Auth par défaut ; ne pas étendre ce choix à AD, à un LDAP externe ou aux secrets.

## Capabilities

### New Capabilities

- `core-storage` : stockage Core sélectionnable et migration réversible PostgreSQL/OpenLDAP interne.

### Modified Capabilities

- `core` : propriété logique indépendante du stockage physique et exception explicite au PostgreSQL exclusif.
- `directory-projections` : portée des interdictions limitée au rôle de projection, distinct du stockage autoritatif.
- `reference-runtime` : PostgreSQL de référence avec exception Core bornée et qualifiée.

## Impact

Préparation documentaire du 19 octobre 2026, sans implémentation, production de code, dépendance installée, migration réelle, modification de données, arrêt de service ou Git. Deltas proposés uniquement, sans synchronisation du canon ni archivage. C02 conserve la réalisation du stockage PostgreSQL initial ; le présent dossier prépare l'option postinstallation et le retour avec OpenLDAP géré par Auth.
