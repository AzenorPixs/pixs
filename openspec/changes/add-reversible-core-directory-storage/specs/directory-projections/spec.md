## MODIFIED Requirements

### Requirement: Autorité PostgreSQL des primitives Core

Dans le mode projection de consultation, PostgreSQL MUST rester la source de vérité ; toute création, modification, révocation ou suppression MUST être décidée par une Command Pixs autorisée avant éligibilité à la projection. Le mode stockage Core OpenLDAP autoritatif MUST suivre core-storage et MUST NOT être sélectionné comme simple projection de ce même périmètre.

#### Scenario: Mutation Core demandée

- **WHEN** une création, modification, révocation ou suppression d'une primitive Core est demandée dans le mode projection
- **THEN** une Command Pixs autorisée décide la mutation avant son éligibilité à la projection

### Requirement: LDAP sans autorité ni écriture métier

La projection LDAP MUST NOT devenir une source d'autorité, accepter une écriture métier ni importer un changement vers les primitives Core. Cette restriction MUST porter sur le rôle de projection ; un provider de stockage Core LDAP distinct ne peut devenir autoritatif qu'après migration engagée selon core-storage.

#### Scenario: Écriture LDAP refusée

- **WHEN** une modification d'identité, de groupe ou d'appartenance est détectée dans une projection LDAP
- **THEN** elle n'est pas importée vers Pixs et un diagnostic auditable signale la divergence

## ADDED Requirements

### Requirement: Projection et stockage Core mutuellement distincts

Un périmètre Core MUST être servi par son stockage de référence engagé. Lorsqu'il est migré vers OpenLDAP, la projection PostgreSQL vers ce même périmètre et son repli de lecture MUST être désactivés ou reconfigurés sous plan explicite. La projection MUST NOT stocker les ACL Pixs par effet de cette option ; leur stockage LDAP relève exclusivement du contrat core-storage.

#### Scenario: Ancienne projection après bascule

- **WHEN** un périmètre auparavant projeté depuis PostgreSQL devient autoritatif dans OpenLDAP
- **THEN** aucun flux de projection ou repli ancien n'écrase ou ne remplace l'état LDAP courant
