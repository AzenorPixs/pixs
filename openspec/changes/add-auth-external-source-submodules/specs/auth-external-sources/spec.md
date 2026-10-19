## ADDED Requirements

### Requirement: Sources externes absentes de l'installation standard

Les connecteurs vers LDAP, Kerberos, OIDC, SAML ou autres sources externes MUST être des sous-modules installables séparément de pixs.auth. Ils MUST être absents de l'installation standard. L'authentification locale PostgreSQL et les services propres OpenLDAP/KDC MUST NOT dépendre de leur installation.

#### Scenario: Inventaire standard

- **WHEN** une installation utilise le profil autonome standard
- **THEN** son inventaire ne contient aucun sous-module de source externe

#### Scenario: Activation du KDC propre

- **WHEN** le KDC propre est sélectionné sans connecteur Kerberos externe
- **THEN** l'absence de ce connecteur n'empêche pas son activation conforme

### Requirement: Installation sans activation ni confiance implicite

Chaque source MUST déclarer contrats, versions, capacités et instances. Installation, confiance configurée et activation MUST être distinctes. La découverte d'un endpoint, d'un domaine ou d'une bibliothèque MUST NOT installer ou approuver une source. Une ambiguïté de sélection MUST échouer explicitement.

#### Scenario: Connecteur installé seulement

- **WHEN** un connecteur LDAP est installé sans confiance configurée
- **THEN** il reste inutilisable pour authentifier

#### Scenario: Deux instances sans sélection

- **WHEN** deux sources compatibles existent sans sélection déterministe
- **THEN** Auth refuse la demande ambiguë

### Requirement: Mapping multi-source explicite et persistant

Chaque source MUST produire un triplet fournisseur, émetteur, sujet stable selon son contrat, lié explicitement à une DigitalIdentity. Les mappings MUST être persistants et uniques, PostgreSQL par défaut. E-mail, DN mutable ou nom Kerberos similaire MUST NOT suffire à fusionner des identités.

#### Scenario: Deux annuaires même adresse

- **WHEN** deux sources LDAP présentent la même adresse sans liaison approuvée
- **THEN** leurs comptes ne sont pas fusionnés automatiquement

### Requirement: Assurance externe vérifiée sans droit importé

Une source MUST vérifier les preuves et la confiance avant de produire un contexte et MUST déclarer son assurance maximale. L'import d'attributs/groupes MUST suivre les Commands propriétaires distinctes. Une authentification réussie MUST NOT accorder directement une ACL ni compter deux fois le même facteur.

#### Scenario: Groupe administrateur retourné

- **WHEN** une source authentifie un compte et retourne un groupe nommé administrateur
- **THEN** aucune permission n'est créée sans mapping et Command autorisés

#### Scenario: MFA non vérifiable

- **WHEN** la source annonce un niveau MFA sans preuve conforme à son mapping
- **THEN** le contexte n'est pas surclassé

### Requirement: Panne retrait et déprovisionnement sans repli permissif

Une panne ou suppression de confiance MUST invalider ou refuser les contextes concernés selon les bornes déclarées sans repli local implicite. Le retrait du connecteur MUST traiter sessions et liaisons sous plan explicite et MUST NOT supprimer les identités, droits ou données métier Core par effet de bord.

#### Scenario: Source retirée

- **WHEN** un connecteur est retiré sous plan autorisé alors que des sessions l'utilisent
- **THEN** les accès concernés sont traités selon révocation et les identités Core sont conservées

#### Scenario: Panne Kerberos externe

- **WHEN** le realm externe requis devient injoignable
- **THEN** la demande échoue ou suit un parcours déjà autorisé sans activer une méthode plus faible par cette seule panne
