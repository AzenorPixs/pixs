# Références normatives — PA07

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Supervision PBO et collecte PA | 2 | pixs-agent-33fea834fa00 |
| pixs-agent | Maintenance et quarantaine sans nouveaux droits | 1 | pixs-agent-3847c394dde7 |
| pixs-agent | Audit, confidentialité et exception Super Admin | 1 | pixs-agent-314ad93363d9 |
| pixs-agent | Interfaces et messages cohérents | 1 | pixs-agent-b77b9df6889b |
| pzt | Audit applicable et faits réellement établis | 1 | pzt-13f292d7b8c1 |
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

### Référence courante pixs-agent-33fea834fa00

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 229. SHA-256 : `33fea834fa000e71689e0fc02880468b368455df3d56c7edd066643d87e6a676`.

Scénarios : Collecte PA interrompue; Gestion PZT exclue de pixs.agent.

~~~~text
### Requirement: Supervision PBO et collecte PA

Le module PBO pixs.agent MUST configurer, administrer et superviser toutes les
fonctions PA hors PZT. PA MUST rapporter ses mesures, versions et états réels
via PZT ; pixs.agent MUST distinguer état souhaité, appliqué, dernier état connu
et résultat confirmé. La gestion réseau MUST rester dans pixs.pzt. Une mesure
ancienne MUST être datée et MUST NOT devenir un état courant sans preuve.

#### Scenario: Collecte PA interrompue

- **WHEN** la collecte PA est interrompue alors que le dernier état était sain
- **THEN** pixs.agent signale les mesures périmées sans déduire une disponibilité actuelle

#### Scenario: Gestion PZT exclue de pixs.agent

- **WHEN** une configuration du composant réseau PZT est demandée
- **THEN** la gestion relève de pixs.pzt et aucune mutation PZT n’est attribuée à pixs.agent
~~~~

### Référence courante pixs-agent-3847c394dde7

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 247. SHA-256 : `3847c394dde7300996d611a3fe74085dae93269ce087a18a1e8d6cd2451baef0`.

Scénarios : Maintenance et quarantaine sans nouveaux droits.

~~~~text
### Requirement: Maintenance et quarantaine sans nouveaux droits

Les profils MUST déclarer états normal, surveillance seule, maintenance et quarantaine avec portées, actions permises/interdites et conditions de sortie. Drainage et arrêt MUST être bornés ; les nouvelles modifications incompatibles MUST être refusées. Ces états MUST NOT accorder de droit supplémentaire ni supprimer les contrôles applicables.

#### Scenario: Maintenance et quarantaine sans nouveaux droits

- **WHEN** la cible entre en maintenance pendant une opération
- **THEN** son drainage suit le contrat et les nouvelles mutations incompatibles sont refusées
~~~~

### Référence courante pixs-agent-314ad93363d9

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 256. SHA-256 : `314ad93363d9d818e5a7f225d32947753df0c11207a678f2676b7c2c3c744daf`.

Scénarios : Audit, confidentialité et exception Super Admin.

~~~~text
### Requirement: Audit, confidentialité et exception Super Admin

PA et PBO MUST appliquer les obligations ordinaires de security, authorization et audit sous réserve de l'exception unique définie par initial-administration. Une requête Super Admin MUST conserver acteur initial et tenant explicitement accordé, sans credentials ou exception transférés à un worker/autre compte. Audit ou contrôle dérogé/non réalisé MUST NOT être présenté comme effectué ; profils structurels et contrats d'exécution MUST rester distincts.

#### Scenario: Audit, confidentialité et exception Super Admin

- **WHEN** le Super Admin utilise une dérogation d'audit dans son tenant accordé
- **THEN** l'audit absent n'est pas revendiqué comme réalisé et aucun autre compte n'hérite de la dérogation
~~~~

### Référence courante pixs-agent-b77b9df6889b

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 265. SHA-256 : `b77b9df6889bed717deef3d910db9ea2a1cdc7dfacd7b3425bdb3227f86b1895`.

Scénarios : Interfaces et messages cohérents.

~~~~text
### Requirement: Interfaces et messages cohérents

Les interfaces CLI et les contributions PBO/PFO MUST utiliser les contrats publics, des erreurs stables et les traductions des composants propriétaires ; codes et champs MUST rester non localisés. PFO MUST adresser ses demandes à PBO ; une liaison directe PFO–PA MUST NOT être introduite par ces spécifications. Les interfaces MUST respecter accessibilité, thèmes et confidentialité déclarés.

#### Scenario: Interfaces et messages cohérents

- **WHEN** une action est présentée dans PFO
- **THEN** son autorisation reste évaluée par PBO avant transmission éventuelle à PA via PZT
~~~~

### Référence courante pzt-13f292d7b8c1

Source : [pzt](../../specs/pzt/spec.md), ligne 212. SHA-256 : `13f292d7b8c1a3cc992386ce4a6a9fcf06cd3597a67d2a666dabceb45dc3a843`.

Scénarios : Audit applicable et faits réellement établis.

~~~~text
### Requirement: Audit applicable et faits réellement établis

Les contrôles applicatifs PZT MUST suivre security, authorization, initial-administration et audit, y compris l'exception Super Admin dans son seul périmètre reconnu. Un worker MUST NOT recevoir ses credentials ou devenir Super Admin. Une dérogation MUST NOT fabriquer un dossier, audit, contrôle, signature, mesure ou effet absent ; les contrats structurels et d'exécution MUST rester distincts.

#### Scenario: Audit applicable et faits réellement établis

- **WHEN** une opération utilise une dérogation sans audit persistant
- **THEN** l'absence est déclarée et aucune preuve d'audit effectuée n'est annoncée
~~~~

### Référence courante zt-instances-8b936c8ce6e3

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 11. SHA-256 : `8b936c8ce6e344379ce474d3e036ea3c138a8c25a154f7e995d4f69968aee74b`.

Scénarios : Plusieurs composants sur un hôte.

~~~~text
### Requirement: Acteurs et identité persistante

ZT MUST distinguer acteurs humains, matériels, logiciels et organisationnels. Un acteur technique MUST avoir identité, responsabilités et cycle de vie distincts de ses rôles, processus et hôte. Hôte, PBO, PA et PZT MUST conserver leurs identités propres ; les rôles MAY être cumulés explicitement sous les incompatibilités applicables.

#### Scenario: Plusieurs composants sur un hôte

- **WHEN** PBO, PA et PZT sont cohébergés
- **THEN** leur cohébergement ne fusionne ni identités ni habilitations.
~~~~

### Référence courante zt-instances-02f45c3fc9a4

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 20. SHA-256 : `02f45c3fc9a4f05a2ee8f47761142ae718a760009568649070e52b7e3c6dc4c4`.

Scénarios : Individu dans deux ZT.

~~~~text
### Requirement: Appartenances selon la catégorie

Un acteur non humain MUST appartenir à une seule instance ZT à la fois. Un individu Core MAY être admis dans plusieurs ZT ; chaque admission MUST conserver affiliations et permissions indépendantes. Une relation d'approbation MUST NOT changer l'appartenance du représentant ou du partenaire.

#### Scenario: Individu dans deux ZT

- **WHEN** un individu est admis dans deux ZT
- **THEN** chaque ZT décide séparément de ses droits sans copie automatique.
~~~~

### Référence courante zt-instances-6518a8a762d8

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 29. SHA-256 : `6518a8a762d878c26443bdc3b6ad94fcb18c14dadc87ac3f5ceb1c9c25f68790`.

Scénarios : Délégation limitée.

~~~~text
### Requirement: Gouvernance commune et délégations

Chaque ZT MUST avoir une gouvernance commune, éventuellement collective, avec compétences explicites. Admission et gestion des approbations MAY être déléguées par périmètre ; chaque délégataire MUST rester dans son mandat sans élargir l'autorité de l'Instance ou des Domaines.

#### Scenario: Délégation limitée

- **WHEN** un délégué aux approbations d’un périmètre vise un autre périmètre
- **THEN** la création ou modification hors mandat est refusée.
~~~~

### Référence courante zt-instances-fe908c4cf04e

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 38. SHA-256 : `fe908c4cf04e403c81b93c34449ff1ce0bb362d1d81a14a5aa6bd53867698626`.

Scénarios : Rejeu d’enrôlement.

~~~~text
### Requirement: Admission administrative et préautorisation

L'admission administrative MUST être le défaut pour les individus. Une admission automatique MUST exiger une politique explicite. L'enrôlement préautorisé MUST utiliser un jeton individuel temporaire à usage unique, avec engagement et reprise évitant double identité ou réutilisation.

#### Scenario: Rejeu d’enrôlement

- **WHEN** un jeton déjà consommé est présenté pour un nouveau membre
- **THEN** il ne crée pas de seconde admission.
~~~~

### Référence courante zt-instances-b0acd891069f

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 47. SHA-256 : `b0acd891069f982f41c1860ebc7a698a5c3fec2141afbaea754cce16f6c6d4bd`.

Scénarios : Admission expirée après restauration.

~~~~text
### Requirement: Participations permanentes et temporaires

L'appartenance permanente MUST être proposée par défaut ; les profils temporaires/éphémères MUST avoir échéance finie et renouvellement autorisé. Les autorisations MUST NOT dépasser la participation. Redémarrage ou restauration MUST NOT repousser l'échéance ; la fin d'appartenance MUST NOT supprimer implicitement l'individu ou l'environnement.

#### Scenario: Admission expirée après restauration

- **WHEN** une sauvegarde contient une admission désormais expirée
- **THEN** aucun accès n’est réarmé et les données/hôtes ne sont pas supprimés par déduction.
~~~~

### Référence courante zt-instances-abd1a7f7a384

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 56. SHA-256 : `abd1a7f7a3844fc63953eda5d7ff8c95f8f0b01b94f94ab592c0eeb2ce7414c7`.

Scénarios : Chaîne trop profonde.

~~~~text
### Requirement: Approbations directionnelles et bornées

Une approbation MUST déclarer source, destinataire, portée, conditions et délégations autorisées. La réciprocité MUST exiger deux approbations. La transitivité MUST être autorisée explicitement avec profondeur maximale finie configurable ; chaque maillon MUST respecter les limites des relations traversées. Reconnaître une identité MUST NOT accorder des droits sur les ressources.

#### Scenario: Chaîne trop profonde

- **WHEN** une chaîne dépasse la profondeur admise par un maillon
- **THEN** la reconnaissance indirecte est refusée même si les autres maillons l’acceptent.
~~~~

### Référence courante zt-instances-b9367d6d6b27

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 65. SHA-256 : `b9367d6d6b279030ffb9cb85e35b97d72f23d1b94a5b5665c53bb22ca15dcd19`.

Scénarios : Sens inverse.

~~~~text
### Requirement: Politiques durables et autorisations bornées

Les politiques ZT MUST être durables ; les autorisations d'exécution MUST être temporaires et bornées. Permissions individuelles/collectives MUST viser services, directions, protocoles et ports déclarés avec interdiction prioritaire et refus par défaut selon les contrats applicables. L'initiation inverse MUST nécessiter sa propre autorisation et les réponses MUST rester encadrées.

#### Scenario: Sens inverse

- **WHEN** une destination autorisée à répondre initie une nouvelle communication inverse
- **THEN** cette initiation est refusée sans permission distincte.
~~~~

### Référence courante zt-instances-cc529473dd70

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 74. SHA-256 : `cc529473dd70e8a2099d093781f28835b1adfc0e367f27415468e48745448114`.

Scénarios : Logiciel sans droit.

~~~~text
### Requirement: Appartenance et preuve sans permission implicite

Un certificat, une IP, un rôle administratif, une affiliation ou un positionnement hiérarchique MUST NOT suffire à accorder l'accès. Les permissions d'utilisation et d'administration MUST être distinguées. Lorsqu'un contexte humain est requis, les droits de l'individu et ceux de l'acteur technique MUST être vérifiés conjointement.

#### Scenario: Logiciel sans droit

- **WHEN** un individu habilité agit par un logiciel non habilité sur la cible
- **THEN** l’action nécessitant les deux permissions est refusée.
~~~~

### Référence courante zt-instances-4208f537345f

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 83. SHA-256 : `4208f537345fc9a96a01cd5319734cc7a9788e7e3ca565903ba89532d908db50`.

Scénarios : Relais non mandaté.

~~~~text
### Requirement: Représentation explicite et indépendante

La participation MAY être directe ou représentée. Le mandat MUST identifier représenté, représentant, actions, ressources, durée, révocation et éventuelle redélégation. Le représenté MUST conserver son identité ; le représentant MUST utiliser ses moyens propres sans recevoir les secrets personnels de l'individu et sans transférer un pouvoir absent du représenté.

#### Scenario: Relais non mandaté

- **WHEN** un logiciel relaie une requête sans mandat de représentation
- **THEN** ce relais n’établit pas le droit d’agir au nom de l’individu.
~~~~

### Référence courante zt-instances-906ddd8e7c4a

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 92. SHA-256 : `906ddd8e7c4a0c8c888a6fd2b2b733e2490664201a2f103475502d14f07797a0`.

Scénarios : Tâche longue.

~~~~text
### Requirement: Mandats et session

Le mandat humain MUST dépendre de la session par défaut. Une indépendance de session MAY être autorisée explicitement avec ses propres bornes. Suspension de l'individu, retrait des droits ou révocation MUST conserver leurs effets sur le mandat indépendant.

#### Scenario: Tâche longue

- **WHEN** un mandat indépendant autorisé continue après une déconnexion ordinaire
- **THEN** il reste limité à sa durée et cesse si ses droits ou son mandat sont révoqués.
~~~~

### Référence courante zt-instances-9e1b32b3ada0

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 101. SHA-256 : `9e1b32b3ada0a358695a5cc175a08e55c41d59556cb16a12ba7c2b867b28ea03`.

Scénarios : Auth indisponible.

~~~~text
### Requirement: Propagation des états autoritatifs

Une suspension Core MUST suspendre l'exercice des droits dépendants et réévaluer les mandats. La révocation de session MUST invalider les autorisations qui en dépendent. Une panne Core/Auth MUST suivre la continuité bornée sans valoir révocation ou nouvelle permission. La remise en activité MUST réévaluer l'état courant sans restauration implicite.

#### Scenario: Auth indisponible

- **WHEN** Auth devient temporairement injoignable
- **THEN** seules les opérations encore admissibles dans leur continuité bornée restent possibles.
~~~~

### Référence courante zt-instances-e45def8cb779

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 110. SHA-256 : `e45def8cb77933a3585cbf97fcda38c225e26cd984dffdd430237d9eef23ca30`.

Scénarios : Minima partagés.

~~~~text
### Requirement: Socle et minima opérationnels ZT

Chaque ZT MUST disposer d'au moins un PZT portant initialement CZT, SZT, RZT, STZT, DZT et PKIZT. Les rôles MAY être répartis et redondés. Le premier PZT complet V1 MUST cibler Debian/Linux ; les suivants MUST porter seulement les rôles qualifiés pour leur plateforme. GZT, EZT et RPZT MUST être optionnels et désactivés par défaut.

#### Scenario: Minima partagés

- **WHEN** deux Domaines utilisent le même ZT
- **THEN** les minima sont évalués sur ce ZT réel et les périmètres restent séparés.
~~~~

### Référence courante zt-instances-b6e16e2c94a8

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 119. SHA-256 : `b6e16e2c94a830d2873dca9721345de994a8de38ac26a6907f369aecc1958398`.

Scénarios : Rôle déclaré sans exécutant.

~~~~text
### Requirement: Existence et disponibilité distinctes

La gestion MUST distinguer rôle déclaré, admis, configuré et opérationnel vérifié. Une panne MUST dégrader seulement les capacités concernées lorsque leur isolation est démontrée. Une mesure ancienne ou un processus vivant MUST NOT prouver le service actuel.

#### Scenario: Rôle déclaré sans exécutant

- **WHEN** DZT est déclaré mais aucun service admissible ne répond
- **THEN** la gestion expose l’indisponibilité au lieu d’un DNS actif fictif.
~~~~

### Référence courante zt-instances-a979db4ef59b

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 128. SHA-256 : `a979db4ef59bb6aadfac590f7db6187897b89e571759f190851cf3022afe88c9`.

Scénarios : Révocation d’un PZT.

~~~~text
### Requirement: Sortie et révocation séparées

La sortie planifiée, la révocation et le changement de mode MUST avoir des procédures distinctes et explicites. Le retrait MUST préserver les historiques et traiter les dépendances sans créer un changement de mode implicite ni détruire les ressources hors mandat.

#### Scenario: Révocation d’un PZT

- **WHEN** un PZT est révoqué
- **THEN** ses accès sont retirés selon le contrat sans bascule automatique de l’Instance en Standalone.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 164 | [Supervision PBO et collecte PA](../../specs/pixs-agent/spec.md#L164) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 173 | [Maintenance et quarantaine sans nouveaux droits](../../specs/pixs-agent/spec.md#L173) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 191 | [Interfaces et messages cohérents](../../specs/pixs-agent/spec.md#L191) | ND | CANDIDAT_PROFIL_PA |
| pzt / 147 | [Audit applicable et faits réellement établis](../../specs/pzt/spec.md#L147) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--9c56e42aad

Source : `openspec/specs/pixs-agent/spec.md`, ligne 164. SHA-256 du bloc : `aa149c5fbf55f46a5c6f96edd12c63fb92994dc70c95b1b47283cacd23ccbef3`.

~~~~text
### Requirement: Supervision PBO et collecte PA

Configuration, visualisation, supervision et monitoring PZT MUST toujours relever de PBO. PA MUST collecter et remonter les mesures et états réellement observés via PZT. Vivacité, disponibilité, démarrage, diagnostic et résultat métier MUST rester distincts ; une mesure ancienne MUST être datée et MUST NOT devenir un état courant par absence de nouvelle information.

#### Scenario: Supervision PBO et collecte PA

- **WHEN** la collecte est interrompue alors que le dernier état était sain
- **THEN** PBO signale les mesures périmées et ne déduit pas une disponibilité actuelle
~~~~

### Référence pixs-agent--5b1af8f5b9

Source : `openspec/specs/pixs-agent/spec.md`, ligne 173. SHA-256 du bloc : `22837bf1d6a8eaad369b982b893a18f8cfd30af14efc62e6f8674dd89abe30d8`.

~~~~text
### Requirement: Maintenance et quarantaine sans nouveaux droits

Les profils MUST déclarer états normal, surveillance seule, maintenance et quarantaine avec portées, actions permises/interdites et conditions de sortie. Drainage et arrêt MUST être bornés ; les nouvelles modifications incompatibles MUST être refusées. Ces états MUST NOT accorder de droit supplémentaire ni supprimer les contrôles applicables.

#### Scenario: Maintenance et quarantaine sans nouveaux droits

- **WHEN** la cible entre en maintenance pendant une opération
- **THEN** son drainage suit le contrat et les nouvelles mutations incompatibles sont refusées
~~~~

### Référence pixs-agent--df6fedb5de

Source : `openspec/specs/pixs-agent/spec.md`, ligne 191. SHA-256 du bloc : `e32fa647dde73362fa0d805f8baa9b8f7b888563b7ebdd92de397deda7bbd06c`.

~~~~text
### Requirement: Interfaces et messages cohérents

Les interfaces CLI et les contributions PBO/PFO MUST utiliser les contrats publics, des erreurs stables et les traductions des composants propriétaires ; codes et champs MUST rester non localisés. PFO MUST adresser ses demandes à PBO ; aucune liaison directe PFO–PA MUST être introduite par ces spécifications. Les interfaces MUST respecter accessibilité, thèmes et confidentialité déclarés.

#### Scenario: Interfaces et messages cohérents

- **WHEN** une action est présentée dans PFO
- **THEN** son autorisation reste évaluée par PBO avant transmission éventuelle à PA via PZT
~~~~

### Référence pzt--82a0e6c439

Source : `openspec/specs/pzt/spec.md`, ligne 147. SHA-256 du bloc : `bc7545fffd89f97f8278ddfd75e3a0e388c7291bebe64612552dc59554458b29`.

~~~~text
### Requirement: Audit applicable et faits réellement établis

Les contrôles applicatifs PZT MUST suivre security, authorization, initial-administration et audit, y compris l'exception Super Admin dans son seul périmètre reconnu. Aucun worker MUST recevoir ses credentials ou devenir Super Admin. Une dérogation MUST NOT fabriquer un dossier, audit, contrôle, signature, mesure ou effet absent ; les contrats structurels et d'exécution MUST rester distincts.

#### Scenario: Audit applicable et faits réellement établis

- **WHEN** une opération utilise une dérogation sans audit persistant
- **THEN** l'absence est déclarée et aucune preuve d'audit effectuée n'est annoncée
~~~~

