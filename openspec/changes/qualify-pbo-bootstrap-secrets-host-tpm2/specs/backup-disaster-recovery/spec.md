## ADDED Requirements

### Requirement: Secours indépendant des secrets liés à une machine

Le plan de reprise MUST distinguer ciphertexts locaux, clé hôte, dépendance au TPM et mécanisme indépendant de réémission ou de récupération protégée. Il MUST déclarer autorité, accès, conservation et RPO/RTO. Une sauvegarde du seul ciphertext ou de la clé hôte MUST NOT être présentée comme récupérable sans le TPM d’origine ; une clé de secours MUST NOT être conservée en clair avec sa sauvegarde.

#### Scenario: Sauvegarde locale seule

- **WHEN** le dossier de secours contient seulement les credentials liés à la machine et sa clé hôte
- **THEN** la capacité de reprise après perte du TPM est déclarée non démontrée et bloque la qualification de récupération

#### Scenario: Matériel de récupération non séparé

- **WHEN** la clé permettant d’ouvrir une sauvegarde de secours est stockée en clair dans le même périmètre accessible
- **THEN** ce plan ne satisfait pas la protection du secours et ne reçoit pas de verdict conforme

### Requirement: Récupération testée sans hôte ni TPM d’origine

Avant admission en production, la procédure MUST être testée en environnement isolé avec l’ancien hôte et son TPM indisponibles. Un opérateur habilité MUST pouvoir réémettre ou récupérer les secrets nécessaires puis les protéger pour le nouvel hôte selon la politique autorisée. Les preuves MUST conserver versions, actions et objectifs de reprise mesurés sans valeur secrète ni export supposé d’une clé TPM non exportable.

#### Scenario: Remplacement complet de machine

- **WHEN** l’ancien hôte et son TPM ne sont plus accessibles pendant l’exercice
- **THEN** la procédure retrouve les accès nécessaires par le mécanisme indépendant prévu, chiffre pour le nouvel hôte et démontre la reprise dans les objectifs déclarés

#### Scenario: Récupération interrompue

- **WHEN** la procédure s’interrompt avant validation des nouvelles liaisons et des contrôles du consommateur
- **THEN** elle conserve un état diagnostiquable et ne réadmet pas le service sur une preuve partielle

### Requirement: Réadmission des consommateurs après récupération de secrets

La récupération MUST revalider les références, versions, identités de workload, révocations courantes et contrôles d’audit avant réadmission. Elle MUST traiter les effets de réémission propres aux secrets et MUST NOT réactiver une version révoquée ou une identité clonée depuis une sauvegarde. L’absence de faits courants MUST laisser la reprise concernée bloquée selon les contrats propriétaires.

#### Scenario: Snapshot antérieur à une révocation

- **WHEN** le matériel de secours contient une version révoquée après sa sauvegarde
- **THEN** cette version n’est pas réadmise comme valide et la procédure requiert une référence ou une version courante autorisée

#### Scenario: Changement de secret de signature ou d’accès base

- **WHEN** la reprise réémet un secret dont le changement affecte les sessions, signatures ou droits PostgreSQL
- **THEN** ces effets sont traités par leurs contrats propriétaires et la remise en service ne présume pas leur continuité
