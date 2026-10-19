## ADDED Requirements

### Requirement: Stockage Core PostgreSQL par défaut et option OpenLDAP interne

Le stockage des utilisateurs, groupes et ACL Pixs MUST utiliser PostgreSQL par défaut. Une opération postinstallation autorisée MUST permettre de sélectionner l'OpenLDAP interne géré par Pixs comme stockage de référence pour le périmètre migré. Le retour OpenLDAP vers PostgreSQL MUST être prévu et qualifié avant toute activation de cette option.

#### Scenario: Installation initiale

- **WHEN** aucune migration vers OpenLDAP n'a été engagée
- **THEN** les utilisateurs, groupes et ACL restent stockés et servis depuis PostgreSQL

#### Scenario: Retour non qualifié

- **WHEN** le provider sait recevoir les données PostgreSQL mais ne sait pas restituer fidèlement les données LDAP courantes
- **THEN** la sélection comme stockage de référence est refusée

### Requirement: Propriété Core et fidélité du périmètre migré

Core MUST rester propriétaire logique des données, schémas et contrats indépendamment du stockage physique. Le plan MUST inclure utilisateurs, groupes, ACL et la fermeture de leurs relations nécessaires, en préservant UUID, cardinalités, appartenances, permissions, portées, versions, états, révocations et tombstones. Un attribut non représentable MUST bloquer la migration sans perte silencieuse.

#### Scenario: ACL non représentable

- **WHEN** le mapping LDAP ne peut conserver un effet DENY ou une condition d'une ACL source
- **THEN** le plan est refusé sans tronquer la politique ni activer la cible

### Requirement: Stockage des ACL distinct du moteur de décision

Le stockage LDAP des ACL Pixs MUST conserver leur sémantique applicative. Django et le moteur d'autorisation Pixs MUST continuer à évaluer les décisions et le filtrage. Les ACL techniques slapd MUST NOT remplacer les ACL Pixs ni créer des droits applicatifs ; les écritures Core MUST passer par Commands autorisées.

#### Scenario: Droit technique LDAP

- **WHEN** un compte technique peut lire une entrée LDAP sans permission Pixs correspondante
- **THEN** ce droit technique ne lui donne aucun accès applicatif Pixs

### Requirement: Plan de migration versionné et contrôles préalables

Toute migration dans l'un ou l'autre sens MUST déclarer opération, acteur, périmètre, source, cible, versions, mapping, impacts, sauvegarde, reprise et retour. La capacité cible, le transport, les accès, la cohérence et le maintien des garanties de concurrence/audit MUST être vérifiés avant copie. Installer ou démarrer OpenLDAP MUST NOT basculer l'autorité.

#### Scenario: Activation du service sans migration

- **WHEN** OpenLDAP devient sain mais aucun plan de changement de stockage n'est engagé
- **THEN** PostgreSQL conserve son rôle de stockage de référence

### Requirement: Exclusion des écritures et source unique pendant la bascule

Le changement de stockage MUST empêcher les écritures concurrentes non maîtrisées du périmètre pendant la réconciliation finale et l'engagement. Il MUST conserver une seule source de référence admise et clôturer les anciens écrivains. Les accès LDAP directs hors contrat MUST être empêchés ou détectés avant réadmission ; aucune double autorité implicite n'est admise.

#### Scenario: Ancien worker pendant bascule

- **WHEN** un worker tente une mutation avec une génération de stockage périmée
- **THEN** sa mutation est refusée avant effet sur l'ancien stockage

### Requirement: Copie vérifiée et réconciliation sans résurrection

Avant bascule, la copie MUST être contrôlée par identités, contenu canonique, relations, versions et états de sécurité, avec rapprochement des mutations confirmées jusqu'à la barrière finale. Les retraits, révocations et tombstones MUST être appliqués. Une cible partielle, divergente ou non vérifiable MUST NOT être admise comme référence.

#### Scenario: Copie incomplète

- **WHEN** la copie omet une appartenance ou une ACL
- **THEN** la source conserve l'autorité et la cible reste non admissible

#### Scenario: Révocation après copie préparatoire

- **WHEN** une révocation est confirmée à la source avant la barrière finale
- **THEN** elle est réconciliée avant activation de la cible et n'est pas perdue

### Requirement: Engagement durable de génération de stockage

La bascule MUST engager durablement une référence unique source/cible avec génération et preuve de validation. Lecteurs, écrivains, caches, sessions et traitements différés MUST prendre en compte cette génération avant réutilisation de faits sensibles. Une bascule d'issue inconnue MUST être réconciliée avant nouvel engagement ou reprise d'écritures.

#### Scenario: Réponse de bascule perdue

- **WHEN** la demande perd sa réponse après engagement possible
- **THEN** la reprise consulte l'état autoritatif sans basculer une seconde fois ni deviner la source

#### Scenario: Ancien ALLOW en cache

- **WHEN** un cache conserve une décision antérieure au changement de génération
- **THEN** elle n'autorise pas une opération sensible sans revalidation des faits applicables

### Requirement: Reprise idempotente sans double application

Les checkpoints, résultats et preuves nécessaires à la migration MUST être persistants et consultables. Une reprise MUST distinguer source active, cible préparée, engagement confirmé et issue inconnue. Le rejeu MUST NOT créer de doublon, réactiver un accès retiré ou effacer une donnée source sans acte distinct.

#### Scenario: Interruption pendant copie

- **WHEN** la migration est interrompue après copie d'une partie des données
- **THEN** elle reprend depuis l'état vérifié sans doublon et sans changement d'autorité supposé

### Requirement: Retour depuis les données LDAP courantes sans repli automatique

Le retour vers PostgreSQL MUST migrer l'état courant OpenLDAP, y compris les mutations depuis l'aller, et suivre les mêmes contrôles de copie et d'engagement. Il MUST NOT simplement réactiver l'ancienne copie PostgreSQL. Une panne OpenLDAP MUST NOT déclencher une bascule automatique vers une copie PostgreSQL périmée.

#### Scenario: Retour après modification LDAP

- **WHEN** des utilisateurs, groupes ou ACL ont été modifiés via Pixs pendant qu'OpenLDAP était référence
- **THEN** le retour conserve ces modifications dans PostgreSQL avant sa réactivation

#### Scenario: LDAP indisponible

- **WHEN** OpenLDAP est référence mais devient indisponible et PostgreSQL contient seulement un ancien état
- **THEN** les opérations protégées échouent fermées sans utiliser cet ancien état comme référence

### Requirement: Garanties de persistance et domaines exclus

Le provider LDAP MUST prouver les garanties des mutations Core sélectionnées : unicité, intégrité, concurrence, idempotence, audit et publication. Une capacité insuffisante MUST bloquer la sélection. Le déplacement Core MUST NOT migrer implicitement sessions Auth, secrets, données métier, audit ou coordination ; ces domaines conservent leurs stockages déclarés.

#### Scenario: Mutation LDAP sans garantie requise

- **WHEN** le provider ne peut préserver l'atomicité d'une mutation Core multi-objets exigée
- **THEN** la capacité concernée reste non admissible sans prétendre à une transaction PostgreSQL équivalente

### Requirement: Conservation et retrait distincts de la migration

La bascule MUST déclarer la conservation protégée et l'état non autoritatif de l'ancienne copie. Son retrait ou effacement MUST relever d'un acte séparé respectant références, rétention, audit et retour. La désactivation du module OpenLDAP MUST être refusée tant qu'il reste le stockage de référence sans retour engagé et vérifié.

#### Scenario: Désactivation avant retour

- **WHEN** un opérateur demande l'arrêt définitif du sous-module hébergeant le stockage Core actif
- **THEN** la désactivation est refusée jusqu'au transfert vérifié ou au plan d'arrêt autorisé applicable
