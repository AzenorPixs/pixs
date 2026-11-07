# Références normatives — Z30

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| zt-instances | Acteurs et identité persistante | 1 | zt-instances-8b936c8ce6e3 |
| zt-instances | Appartenances selon la catégorie | 1 | zt-instances-02f45c3fc9a4 |
| zt-instances | Gouvernance commune et délégations | 1 | zt-instances-6518a8a762d8 |
| zt-instances | Admission administrative et préautorisation | 1 | zt-instances-fe908c4cf04e |
| zt-instances | Participations permanentes et temporaires | 1 | zt-instances-b0acd891069f |
| zt-instances | Approbations directionnelles et bornées | 1 | zt-instances-abd1a7f7a384 |
| zt-instances | Politiques durables et autorisations bornées | 1 | zt-instances-b9367d6d6b27 |
| zt-instances | Appartenance et preuve sans permission implicite | 1 | zt-instances-cc529473dd70 |
| zt-instances | Représentation explicite et indépendante | 1 | zt-instances-4208f537345f |
| zt-instances | Mandats et session | 1 | zt-instances-906ddd8e7c4a |
| zt-instances | Propagation des états autoritatifs | 1 | zt-instances-9e1b32b3ada0 |
| zt-instances | Socle et minima opérationnels ZT | 1 | zt-instances-e45def8cb779 |
| zt-instances | Existence et disponibilité distinctes | 1 | zt-instances-b6e16e2c94a8 |
| zt-instances | Sortie et révocation séparées | 1 | zt-instances-a979db4ef59b |
| pixs-domains | Isolation dans un ZT partagé | 1 | pixs-domains-bd2991264b73 |
| pixs-domains | Approbations internes et externes | 1 | pixs-domains-94814997f512 |

## Blocs sources complets

### Référence zt-instances-8b936c8ce6e3

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 11. SHA-256 du bloc : `8b936c8ce6e344379ce474d3e036ea3c138a8c25a154f7e995d4f69968aee74b`.

Scénarios sources : Plusieurs composants sur un hôte.

~~~~text
### Requirement: Acteurs et identité persistante

ZT MUST distinguer acteurs humains, matériels, logiciels et organisationnels. Un acteur technique MUST avoir identité, responsabilités et cycle de vie distincts de ses rôles, processus et hôte. Hôte, PBO, PA et PZT MUST conserver leurs identités propres ; les rôles MAY être cumulés explicitement sous les incompatibilités applicables.

#### Scenario: Plusieurs composants sur un hôte

- **WHEN** PBO, PA et PZT sont cohébergés
- **THEN** leur cohébergement ne fusionne ni identités ni habilitations.
~~~~

### Référence zt-instances-02f45c3fc9a4

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 20. SHA-256 du bloc : `02f45c3fc9a4f05a2ee8f47761142ae718a760009568649070e52b7e3c6dc4c4`.

Scénarios sources : Individu dans deux ZT.

~~~~text
### Requirement: Appartenances selon la catégorie

Un acteur non humain MUST appartenir à une seule instance ZT à la fois. Un individu Core MAY être admis dans plusieurs ZT ; chaque admission MUST conserver affiliations et permissions indépendantes. Une relation d'approbation MUST NOT changer l'appartenance du représentant ou du partenaire.

#### Scenario: Individu dans deux ZT

- **WHEN** un individu est admis dans deux ZT
- **THEN** chaque ZT décide séparément de ses droits sans copie automatique.
~~~~

### Référence zt-instances-6518a8a762d8

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 29. SHA-256 du bloc : `6518a8a762d878c26443bdc3b6ad94fcb18c14dadc87ac3f5ceb1c9c25f68790`.

Scénarios sources : Délégation limitée.

~~~~text
### Requirement: Gouvernance commune et délégations

Chaque ZT MUST avoir une gouvernance commune, éventuellement collective, avec compétences explicites. Admission et gestion des approbations MAY être déléguées par périmètre ; chaque délégataire MUST rester dans son mandat sans élargir l'autorité de l'Instance ou des Domaines.

#### Scenario: Délégation limitée

- **WHEN** un délégué aux approbations d’un périmètre vise un autre périmètre
- **THEN** la création ou modification hors mandat est refusée.
~~~~

### Référence zt-instances-fe908c4cf04e

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 38. SHA-256 du bloc : `fe908c4cf04e403c81b93c34449ff1ce0bb362d1d81a14a5aa6bd53867698626`.

Scénarios sources : Rejeu d’enrôlement.

~~~~text
### Requirement: Admission administrative et préautorisation

L'admission administrative MUST être le défaut pour les individus. Une admission automatique MUST exiger une politique explicite. L'enrôlement préautorisé MUST utiliser un jeton individuel temporaire à usage unique, avec engagement et reprise évitant double identité ou réutilisation.

#### Scenario: Rejeu d’enrôlement

- **WHEN** un jeton déjà consommé est présenté pour un nouveau membre
- **THEN** il ne crée pas de seconde admission.
~~~~

### Référence zt-instances-b0acd891069f

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 47. SHA-256 du bloc : `b0acd891069f982f41c1860ebc7a698a5c3fec2141afbaea754cce16f6c6d4bd`.

Scénarios sources : Admission expirée après restauration.

~~~~text
### Requirement: Participations permanentes et temporaires

L'appartenance permanente MUST être proposée par défaut ; les profils temporaires/éphémères MUST avoir échéance finie et renouvellement autorisé. Les autorisations MUST NOT dépasser la participation. Redémarrage ou restauration MUST NOT repousser l'échéance ; la fin d'appartenance MUST NOT supprimer implicitement l'individu ou l'environnement.

#### Scenario: Admission expirée après restauration

- **WHEN** une sauvegarde contient une admission désormais expirée
- **THEN** aucun accès n’est réarmé et les données/hôtes ne sont pas supprimés par déduction.
~~~~

### Référence zt-instances-abd1a7f7a384

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 56. SHA-256 du bloc : `abd1a7f7a3844fc63953eda5d7ff8c95f8f0b01b94f94ab592c0eeb2ce7414c7`.

Scénarios sources : Chaîne trop profonde.

~~~~text
### Requirement: Approbations directionnelles et bornées

Une approbation MUST déclarer source, destinataire, portée, conditions et délégations autorisées. La réciprocité MUST exiger deux approbations. La transitivité MUST être autorisée explicitement avec profondeur maximale finie configurable ; chaque maillon MUST respecter les limites des relations traversées. Reconnaître une identité MUST NOT accorder des droits sur les ressources.

#### Scenario: Chaîne trop profonde

- **WHEN** une chaîne dépasse la profondeur admise par un maillon
- **THEN** la reconnaissance indirecte est refusée même si les autres maillons l’acceptent.
~~~~

### Référence zt-instances-b9367d6d6b27

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 65. SHA-256 du bloc : `b9367d6d6b279030ffb9cb85e35b97d72f23d1b94a5b5665c53bb22ca15dcd19`.

Scénarios sources : Sens inverse.

~~~~text
### Requirement: Politiques durables et autorisations bornées

Les politiques ZT MUST être durables ; les autorisations d'exécution MUST être temporaires et bornées. Permissions individuelles/collectives MUST viser services, directions, protocoles et ports déclarés avec interdiction prioritaire et refus par défaut selon les contrats applicables. L'initiation inverse MUST nécessiter sa propre autorisation et les réponses MUST rester encadrées.

#### Scenario: Sens inverse

- **WHEN** une destination autorisée à répondre initie une nouvelle communication inverse
- **THEN** cette initiation est refusée sans permission distincte.
~~~~

### Référence zt-instances-cc529473dd70

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 74. SHA-256 du bloc : `cc529473dd70e8a2099d093781f28835b1adfc0e367f27415468e48745448114`.

Scénarios sources : Logiciel sans droit.

~~~~text
### Requirement: Appartenance et preuve sans permission implicite

Un certificat, une IP, un rôle administratif, une affiliation ou un positionnement hiérarchique MUST NOT suffire à accorder l'accès. Les permissions d'utilisation et d'administration MUST être distinguées. Lorsqu'un contexte humain est requis, les droits de l'individu et ceux de l'acteur technique MUST être vérifiés conjointement.

#### Scenario: Logiciel sans droit

- **WHEN** un individu habilité agit par un logiciel non habilité sur la cible
- **THEN** l’action nécessitant les deux permissions est refusée.
~~~~

### Référence zt-instances-4208f537345f

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 83. SHA-256 du bloc : `4208f537345fc9a96a01cd5319734cc7a9788e7e3ca565903ba89532d908db50`.

Scénarios sources : Relais non mandaté.

~~~~text
### Requirement: Représentation explicite et indépendante

La participation MAY être directe ou représentée. Le mandat MUST identifier représenté, représentant, actions, ressources, durée, révocation et éventuelle redélégation. Le représenté MUST conserver son identité ; le représentant MUST utiliser ses moyens propres sans recevoir les secrets personnels de l'individu et sans transférer un pouvoir absent du représenté.

#### Scenario: Relais non mandaté

- **WHEN** un logiciel relaie une requête sans mandat de représentation
- **THEN** ce relais n’établit pas le droit d’agir au nom de l’individu.
~~~~

### Référence zt-instances-906ddd8e7c4a

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 92. SHA-256 du bloc : `906ddd8e7c4a0c8c888a6fd2b2b733e2490664201a2f103475502d14f07797a0`.

Scénarios sources : Tâche longue.

~~~~text
### Requirement: Mandats et session

Le mandat humain MUST dépendre de la session par défaut. Une indépendance de session MAY être autorisée explicitement avec ses propres bornes. Suspension de l'individu, retrait des droits ou révocation MUST conserver leurs effets sur le mandat indépendant.

#### Scenario: Tâche longue

- **WHEN** un mandat indépendant autorisé continue après une déconnexion ordinaire
- **THEN** il reste limité à sa durée et cesse si ses droits ou son mandat sont révoqués.
~~~~

### Référence zt-instances-9e1b32b3ada0

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 101. SHA-256 du bloc : `9e1b32b3ada0a358695a5cc175a08e55c41d59556cb16a12ba7c2b867b28ea03`.

Scénarios sources : Auth indisponible.

~~~~text
### Requirement: Propagation des états autoritatifs

Une suspension Core MUST suspendre l'exercice des droits dépendants et réévaluer les mandats. La révocation de session MUST invalider les autorisations qui en dépendent. Une panne Core/Auth MUST suivre la continuité bornée sans valoir révocation ou nouvelle permission. La remise en activité MUST réévaluer l'état courant sans restauration implicite.

#### Scenario: Auth indisponible

- **WHEN** Auth devient temporairement injoignable
- **THEN** seules les opérations encore admissibles dans leur continuité bornée restent possibles.
~~~~

### Référence zt-instances-e45def8cb779

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 110. SHA-256 du bloc : `e45def8cb77933a3585cbf97fcda38c225e26cd984dffdd430237d9eef23ca30`.

Scénarios sources : Minima partagés.

~~~~text
### Requirement: Socle et minima opérationnels ZT

Chaque ZT MUST disposer d'au moins un PZT portant initialement CZT, SZT, RZT, STZT, DZT et PKIZT. Les rôles MAY être répartis et redondés. Le premier PZT complet V1 MUST cibler Debian/Linux ; les suivants MUST porter seulement les rôles qualifiés pour leur plateforme. GZT, EZT et RPZT MUST être optionnels et désactivés par défaut.

#### Scenario: Minima partagés

- **WHEN** deux Domaines utilisent le même ZT
- **THEN** les minima sont évalués sur ce ZT réel et les périmètres restent séparés.
~~~~

### Référence zt-instances-b6e16e2c94a8

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 119. SHA-256 du bloc : `b6e16e2c94a830d2873dca9721345de994a8de38ac26a6907f369aecc1958398`.

Scénarios sources : Rôle déclaré sans exécutant.

~~~~text
### Requirement: Existence et disponibilité distinctes

La gestion MUST distinguer rôle déclaré, admis, configuré et opérationnel vérifié. Une panne MUST dégrader seulement les capacités concernées lorsque leur isolation est démontrée. Une mesure ancienne ou un processus vivant MUST NOT prouver le service actuel.

#### Scenario: Rôle déclaré sans exécutant

- **WHEN** DZT est déclaré mais aucun service admissible ne répond
- **THEN** la gestion expose l’indisponibilité au lieu d’un DNS actif fictif.
~~~~

### Référence zt-instances-a979db4ef59b

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 128. SHA-256 du bloc : `a979db4ef59bb6aadfac590f7db6187897b89e571759f190851cf3022afe88c9`.

Scénarios sources : Révocation d’un PZT.

~~~~text
### Requirement: Sortie et révocation séparées

La sortie planifiée, la révocation et le changement de mode MUST avoir des procédures distinctes et explicites. Le retrait MUST préserver les historiques et traiter les dépendances sans créer un changement de mode implicite ni détruire les ressources hors mandat.

#### Scenario: Révocation d’un PZT

- **WHEN** un PZT est révoqué
- **THEN** ses accès sont retirés selon le contrat sans bascule automatique de l’Instance en Standalone.
~~~~

### Référence pixs-domains-bd2991264b73

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 34. SHA-256 du bloc : `bd2991264b73d60314f90b7bb3d936bee405c507992fe50e7ff2e06fb1da6fc6`.

Scénarios sources : Même ZT sans politique.

~~~~text
### Requirement: Isolation dans un ZT partagé

Les politiques MUST pouvoir être propres à un Domaine ou partagées explicitement. Les communications inter-domaines MUST être refusées par défaut et nécessiter une politique explicite. Le partage du ZT MUST NOT fusionner les identités, ACL applicatives, annuaires ou realms.

#### Scenario: Même ZT sans politique

- **WHEN** deux acteurs de Domaines différents partagent ZT sans autorisation de communication
- **THEN** l’initiation inter-domaines est refusée.
~~~~

### Référence pixs-domains-94814997f512

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 102. SHA-256 du bloc : `94814997f512912fbd83b186f7db3bf2f0771d0e37c0e5ecfc7fe81a41c5562f`.

Scénarios sources : Individu externe reconnu.

~~~~text
### Requirement: Approbations internes et externes

Les Domaines MUST pouvoir établir des approbations dans une même Instance ou entre Instances selon zt-instances. Un individu externe MUST conserver son identité d'origine ; la cible MUST conserver une référence et décider séparément de ses admissions et droits. Les composantes DNS et Kerberos MUST être explicites.

#### Scenario: Individu externe reconnu

- **WHEN** une approbation permet de reconnaître l’identité externe
- **THEN** la reconnaissance ne crée pas d’identité locale indépendante ou de droits automatiques.
~~~~
