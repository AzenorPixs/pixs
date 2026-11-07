# zt-instances Specification

## Purpose

Une instance ZT est un ensemble identifié d'acteurs techniques, humains et organisationnels et de relations explicites, indépendant de sa localisation.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45 et TECHNICAL.md §46), sans implémentation ni qualification déduite.

## Requirements

### Requirement: Acteurs et identité persistante

ZT MUST distinguer acteurs humains, matériels, logiciels et organisationnels. Un acteur technique MUST avoir identité, responsabilités et cycle de vie distincts de ses rôles, processus et hôte. Hôte, PBO, PA et PZT MUST conserver leurs identités propres ; les rôles MAY être cumulés explicitement sous les incompatibilités applicables.

#### Scenario: Plusieurs composants sur un hôte

- **WHEN** PBO, PA et PZT sont cohébergés
- **THEN** leur cohébergement ne fusionne ni identités ni habilitations.

### Requirement: Appartenances selon la catégorie

Un acteur non humain MUST appartenir à une seule instance ZT à la fois. Un individu Core MAY être admis dans plusieurs ZT ; chaque admission MUST conserver affiliations et permissions indépendantes. Une relation d'approbation MUST NOT changer l'appartenance du représentant ou du partenaire.

#### Scenario: Individu dans deux ZT

- **WHEN** un individu est admis dans deux ZT
- **THEN** chaque ZT décide séparément de ses droits sans copie automatique.

### Requirement: Gouvernance commune et délégations

Chaque ZT MUST avoir une gouvernance commune, éventuellement collective, avec compétences explicites. Admission et gestion des approbations MAY être déléguées par périmètre ; chaque délégataire MUST rester dans son mandat sans élargir l'autorité de l'Instance ou des Domaines.

#### Scenario: Délégation limitée

- **WHEN** un délégué aux approbations d’un périmètre vise un autre périmètre
- **THEN** la création ou modification hors mandat est refusée.

### Requirement: Admission administrative et préautorisation

L'admission administrative MUST être le défaut pour les individus. Une admission automatique MUST exiger une politique explicite. L'enrôlement préautorisé MUST utiliser un jeton individuel temporaire à usage unique, avec engagement et reprise évitant double identité ou réutilisation.

#### Scenario: Rejeu d’enrôlement

- **WHEN** un jeton déjà consommé est présenté pour un nouveau membre
- **THEN** il ne crée pas de seconde admission.

### Requirement: Participations permanentes et temporaires

L'appartenance permanente MUST être proposée par défaut ; les profils temporaires/éphémères MUST avoir échéance finie et renouvellement autorisé. Les autorisations MUST NOT dépasser la participation. Redémarrage ou restauration MUST NOT repousser l'échéance ; la fin d'appartenance MUST NOT supprimer implicitement l'individu ou l'environnement.

#### Scenario: Admission expirée après restauration

- **WHEN** une sauvegarde contient une admission désormais expirée
- **THEN** aucun accès n’est réarmé et les données/hôtes ne sont pas supprimés par déduction.

### Requirement: Approbations directionnelles et bornées

Une approbation MUST déclarer source, destinataire, portée, conditions et délégations autorisées. La réciprocité MUST exiger deux approbations. La transitivité MUST être autorisée explicitement avec profondeur maximale finie configurable ; chaque maillon MUST respecter les limites des relations traversées. Reconnaître une identité MUST NOT accorder des droits sur les ressources.

#### Scenario: Chaîne trop profonde

- **WHEN** une chaîne dépasse la profondeur admise par un maillon
- **THEN** la reconnaissance indirecte est refusée même si les autres maillons l’acceptent.

### Requirement: Politiques durables et autorisations bornées

Les politiques ZT MUST être durables ; les autorisations d'exécution MUST être temporaires et bornées. Permissions individuelles/collectives MUST viser services, directions, protocoles et ports déclarés avec interdiction prioritaire et refus par défaut selon les contrats applicables. L'initiation inverse MUST nécessiter sa propre autorisation et les réponses MUST rester encadrées.

#### Scenario: Sens inverse

- **WHEN** une destination autorisée à répondre initie une nouvelle communication inverse
- **THEN** cette initiation est refusée sans permission distincte.

### Requirement: Appartenance et preuve sans permission implicite

Un certificat, une IP, un rôle administratif, une affiliation ou un positionnement hiérarchique MUST NOT suffire à accorder l'accès. Les permissions d'utilisation et d'administration MUST être distinguées. Lorsqu'un contexte humain est requis, les droits de l'individu et ceux de l'acteur technique MUST être vérifiés conjointement.

#### Scenario: Logiciel sans droit

- **WHEN** un individu habilité agit par un logiciel non habilité sur la cible
- **THEN** l’action nécessitant les deux permissions est refusée.

### Requirement: Représentation explicite et indépendante

La participation MAY être directe ou représentée. Le mandat MUST identifier représenté, représentant, actions, ressources, durée, révocation et éventuelle redélégation. Le représenté MUST conserver son identité ; le représentant MUST utiliser ses moyens propres sans recevoir les secrets personnels de l'individu et sans transférer un pouvoir absent du représenté.

#### Scenario: Relais non mandaté

- **WHEN** un logiciel relaie une requête sans mandat de représentation
- **THEN** ce relais n’établit pas le droit d’agir au nom de l’individu.

### Requirement: Mandats et session

Le mandat humain MUST dépendre de la session par défaut. Une indépendance de session MAY être autorisée explicitement avec ses propres bornes. Suspension de l'individu, retrait des droits ou révocation MUST conserver leurs effets sur le mandat indépendant.

#### Scenario: Tâche longue

- **WHEN** un mandat indépendant autorisé continue après une déconnexion ordinaire
- **THEN** il reste limité à sa durée et cesse si ses droits ou son mandat sont révoqués.

### Requirement: Propagation des états autoritatifs

Une suspension Core MUST suspendre l'exercice des droits dépendants et réévaluer les mandats. La révocation de session MUST invalider les autorisations qui en dépendent. Une panne Core/Auth MUST suivre la continuité bornée sans valoir révocation ou nouvelle permission. La remise en activité MUST réévaluer l'état courant sans restauration implicite.

#### Scenario: Auth indisponible

- **WHEN** Auth devient temporairement injoignable
- **THEN** seules les opérations encore admissibles dans leur continuité bornée restent possibles.

### Requirement: Socle et minima opérationnels ZT

Chaque ZT MUST disposer d'au moins un PZT portant initialement CZT, SZT, RZT, STZT, DZT et PKIZT. Les rôles MAY être répartis et redondés. Le premier PZT complet V1 MUST cibler Debian/Linux ; les suivants MUST porter seulement les rôles qualifiés pour leur plateforme. GZT, EZT et RPZT MUST être optionnels et désactivés par défaut.

#### Scenario: Minima partagés

- **WHEN** deux Domaines utilisent le même ZT
- **THEN** les minima sont évalués sur ce ZT réel et les périmètres restent séparés.

### Requirement: Existence et disponibilité distinctes

La gestion MUST distinguer rôle déclaré, admis, configuré et opérationnel vérifié. Une panne MUST dégrader seulement les capacités concernées lorsque leur isolation est démontrée. Une mesure ancienne ou un processus vivant MUST NOT prouver le service actuel.

#### Scenario: Rôle déclaré sans exécutant

- **WHEN** DZT est déclaré mais aucun service admissible ne répond
- **THEN** la gestion expose l’indisponibilité au lieu d’un DNS actif fictif.

### Requirement: Sortie et révocation séparées

La sortie planifiée, la révocation et le changement de mode MUST avoir des procédures distinctes et explicites. Le retrait MUST préserver les historiques et traiter les dépendances sans créer un changement de mode implicite ni détruire les ressources hors mandat.

#### Scenario: Révocation d’un PZT

- **WHEN** un PZT est révoqué
- **THEN** ses accès sont retirés selon le contrat sans bascule automatique de l’Instance en Standalone.
