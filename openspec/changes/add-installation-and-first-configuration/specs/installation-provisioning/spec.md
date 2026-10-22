## ADDED Requirements

### Requirement: Gouvernance initiale vérifiée avant création Core

Avant une création Core d’amorçage, C08 MUST obtenir d’une source serveur protégée un profil de gouvernance complet et versionné conforme à data-governance et une attestation liée aux cibles et à la transaction. Cette attestation MUST être revalidée avant commit. Une fixture ou une dispense du compte encore inexistant MUST NOT la remplacer. Profil absent, périmé, révoqué ou incohérent MUST empêcher la création.

#### Scenario: Profil initial déclaré et vérifié

- **WHEN** l’acte R01 dispose d’un profil complet provenant de la source de confiance courante et d’une attestation vérifiée
- **THEN** les contrôles propriétaires peuvent poursuivre la transaction sans dispense anticipée du futur Super Admin

#### Scenario: Profil absent ou substitué avant commit

- **WHEN** le profil initial manque ou diverge lors de la revalidation transactionnelle
- **THEN** aucune création n’est confirmée et les effets liés suivent le rollback propriétaire

### Requirement: Publication externe et références de connexion vérifiées

C08 MUST remplacer les saisies de connexion par les seules références du provider autorisé après une publication externe explicitement contrôlée. Il MUST vérifier la disponibilité, la version et la correspondance à la cible avant mise en service. Une référence seule MUST NOT prouver cette publication ni autoriser C08 à devenir writer de secrets. Les valeurs saisies MUST NOT être persistées dans un artefact, audit ou checkpoint.

#### Scenario: Publication externe non confirmée

- **WHEN** une référence est déclarée sans preuve de disponibilité de la version et de la cible attendues
- **THEN** l’installation reste non prête sans conserver ni exposer la saisie pour la rejouer

#### Scenario: Référence de connexion confirmée

- **WHEN** la publication autorisée et la résolution de la bonne version sont vérifiées
- **THEN** la reprise conserve uniquement les références et métadonnées non secrètes nécessaires

### Requirement: Séquence PA PZT PostgreSQL puis initialisation PBO

Le parcours d’installation MUST séparer provisionnement opérateur PA/PZT, préparation PostgreSQL par PA, connexion et migrations PBO, acte R01 propriétaire puis marqueur et première configuration. Chaque phase MUST avoir propriétaire, plan, résultat et reprise inspectables. Les garanties de transport PZT, de séparation transactionnelle, de non-duplication et de disponibilité ci-dessous MUST être respectées.

#### Scenario: Garanties de la séquence et de la reprise

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** Le parcours d'installation MUST distinguer les phases et propriétaires : provisionnement opérateur local de confiance PA/PZT indépendant de la base Pixs ; préparation PostgreSQL et première connexion technique par PA ; vérification de la cible et remise des seules références applicatives au workload PBO ; inspection et migrations par les contrats propriétaires PBO ; acte initial R01 Core/Auth/audit et résultat C08 ; marqueur externe et première configuration. Tous échanges PBO–PA MUST passer par PZT, même sur le même hôte ou conteneur. Chaque phase MUST posséder plan versionné, identité d'opération, état inspectable, preuves minimisées et conditions de reprise. Un reçu PA MUST attester seulement l'état technique observé et MUST NOT prouver un commit métier ou l'autorisation suivante. Un effet externe de service, rôle ou base MUST NOT être annoncé comme atomique avec la transaction Core/Auth/C05/C08. Après interruption, l'inspection de chaque propriétaire et le rapprochement des résultats MUST précéder tout rejeu ; la compensation d'une préparation externe MUST NOT supprimer une base ou des données sans autorisation destructive distincte. La disponibilité MUST attendre les prérequis, les références vérifiées, l'audit rapproché et les décisions applicatives courantes.

#### Scenario: Panne entre préparation et migration

- **WHEN** PA a confirmé PostgreSQL mais PBO est interrompu avant ses migrations ou son acte R01
- **THEN** la reprise vérifie le résultat technique et la cible puis poursuit la seule phase autorisée sans recréer la base ni déclarer un compte créé

#### Scenario: Commit métier et marqueur perdu

- **WHEN** le commit propriétaire PBO est confirmé mais la réponse ou le marqueur externe est perdu
- **THEN** la reprise inspecte le résultat durable et ne réexécute ni préparation destructive PA ni création Core/Auth ; seule l’étape externe manquante admissible est reprise
