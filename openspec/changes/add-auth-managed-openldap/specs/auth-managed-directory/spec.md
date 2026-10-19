## ADDED Requirements

### Requirement: OpenLDAP propre provisionnable et activable

pixs.auth MUST pouvoir provisionner, configurer, démarrer, arrêter et superviser son propre service OpenLDAP par un sous-module déclaré. L'activation MUST être explicite et indépendante du KDC et des connecteurs externes. Le service MUST rester non requis et non démarré dans le profil local par défaut.

#### Scenario: Activation de l'annuaire seul

- **WHEN** un plan autorisé sélectionne OpenLDAP sans KDC ni source externe
- **THEN** Auth peut activer le service propre après validation de ses prérequis

#### Scenario: Annuaire existant sur l'hôte

- **WHEN** une installation détecte un service LDAP non géré par Pixs
- **THEN** elle ne l'adopte ni ne modifie sa configuration implicitement

### Requirement: Autorité PostgreSQL et stockage technique déclaré

Les données Core et Auth MUST utiliser PostgreSQL par défaut. Une option de stockage Core OpenLDAP MUST suivre une migration engagée et réversible selon core-storage ; les autres données gardent leur stockage déclaré. OpenLDAP MUST déclarer son stockage et ses protections sans double autorité. Une écriture LDAP directe MUST NOT modifier implicitement une primitive Core hors Command autorisée.

#### Scenario: Entrée modifiée hors Pixs

- **WHEN** une entrée gérée diverge après modification directe dans l'annuaire
- **THEN** la divergence est diagnostiquée et n'est pas importée comme mutation Core autorisée

### Requirement: Projection et authentification LDAP distinctes

La consultation MUST suivre directory-projections. Une authentification LDAP fournie par le service propre MUST utiliser une capacité distincte déclarant confiance, moyens, assurance et révocation. Le repli de consultation vers PostgreSQL MUST NOT autoriser un repli d'authentification ni un bind périmé.

#### Scenario: Projection utilisée comme authentificateur

- **WHEN** une composition propose la seule projection de consultation pour valider un mot de passe
- **THEN** cette sélection est refusée sans attribuer une capacité d'authentification

#### Scenario: Lecture dégradée

- **WHEN** LDAP est indisponible et la consultation revient à PostgreSQL
- **THEN** aucun changement de méthode d'authentification n'est déduit de ce repli

### Requirement: Lifecycle et reprise sécurisés du service LDAP

Le service MUST distinguer états souhaité, appliqué, santé et convergence, protéger transport et credentials et borner ses tentatives. Avant réadmission après restauration, ses dérivés et justificatifs MUST être réconciliés avec les retraits/révocations courants. Les diagnostics et projections MUST NOT publier de secret brut.

#### Scenario: Restauration antérieure à un retrait

- **WHEN** un annuaire restauré contient une identité ou un moyen retiré depuis la sauvegarde
- **THEN** il ne redevient pas admissible avant réconciliation et vérification des bornes de révocation
