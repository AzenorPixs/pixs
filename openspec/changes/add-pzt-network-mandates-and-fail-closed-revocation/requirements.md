# Références normatives — Z02

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Continuité sans PBO et reprise locale PZT | 1 | pixs-agent-6feb1d62a194 |
| pzt | Autorités, politiques et délégations distinctes | 1 | pzt-41b67ae97f3a |
| pzt | Expiration, révocation et protection indépendante | 1 | pzt-dd0df6ec99b5 |
| pzt | Contrat A05b — Objectifs initiaux validés, qualification requise | 1 | pzt-b3a8ffad5313 |
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
| zt-controller | CZT obligatoire et périmètre | 1 | zt-controller-0075d78b8361 |
| zt-controller | Base propre chiffrée et initialisation | 1 | zt-controller-99c13d6319c5 |
| zt-controller | Durabilité synchrone et promotion | 1 | zt-controller-a3a1fca8cc08 |
| zt-controller | Continuité bornée sans primaire | 1 | zt-controller-5f13908e4a13 |
| zt-controller | Gestionnaire réseau et propriétaire unique | 1 | zt-controller-a844ba947c3b |
| zt-controller | Backends et protection des échéances | 1 | zt-controller-0b71d7d52f1b |
| zt-controller | Amorçage et opérations multi-rôles | 1 | zt-controller-b3bc36187257 |

### Référence courante pixs-agent-6feb1d62a194

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 211. SHA-256 : `6feb1d62a1942235ad066f7b5e17bda1ec3010cee1c62415549a772ed9d9a556`.

Scénarios : Continuité sans PBO et reprise locale PZT.

~~~~text
### Requirement: Continuité sans PBO et reprise locale PZT

Sans PBO joignable, PA MUST se limiter aux capacités explicitement provisionnées, éligibles et encore valides ; une décision en ligne indisponible MUST bloquer l'action concernée. Diagnostic et reprise depuis PBO MUST passer par PZT, y compris local. Si PZT est entièrement indisponible, une réparation interne/opérateur MUST suivre sa procédure distincte, sans canal de substitution PBO–PA.

#### Scenario: Continuité sans PBO et reprise locale PZT

- **WHEN** PZT est entièrement arrêté
- **THEN** PBO ne reçoit aucun canal de contrôle local de contournement
~~~~

### Référence courante pzt-41b67ae97f3a

Source : [pzt](../../specs/pzt/spec.md), ligne 99. SHA-256 : `41b67ae97f3ad05270d0402c22b544a0a54bd88920ae4b074c8286000d472034`.

Scénarios : Autorités, politiques et délégations distinctes.

~~~~text
### Requirement: Autorités, politiques et délégations distinctes

PZT MUST distinguer identité, permission réseau et permission métier ; une position hiérarchique, clé, adresse ou certificat MUST NOT donner un accès implicite. Les relations verticales/horizontales MUST avoir périmètres et sens déclarés. Une délégation MUST identifier émetteur, bénéficiaire, actions, cible, version, validité, révocation et redélégation ; elle MUST NOT transmettre un pouvoir absent de l'émetteur.

#### Scenario: Autorités, politiques et délégations distinctes

- **WHEN** un pair possède une clé valide sans mandat pour le service
- **THEN** le trafic concerné reste refusé
~~~~

### Référence courante pzt-dd0df6ec99b5

Source : [pzt](../../specs/pzt/spec.md), ligne 131. SHA-256 : `dd0df6ec99b5730852774d736ac4168608d2913a2d10795e48d072ee33afc7fc`.

Scénarios : Expiration, révocation et protection indépendante.

~~~~text
### Requirement: Expiration, révocation et protection indépendante

Les autorisations MUST être bornées, réutilisables seulement selon leur classe et retirées dès révocation connue. Les objectifs initiaux A05b MUST être qualifiés par profil : révocation en 5 s maximum lorsque PA est joignable et fermeture après panne PA en 10 s maximum, détection comprise, avec toute échéance antérieure prioritaire. Une interface noyau persistante après crash MUST NOT prolonger un accès.

#### Scenario: Expiration, révocation et protection indépendante

- **WHEN** l’exécutant PZT plante alors que WireGuard reste actif dans le noyau
- **THEN** la protection indépendante ferme les accès dans le budget qualifié
~~~~

### Référence courante pzt-b3a8ffad5313

Source : [pzt](../../specs/pzt/spec.md), ligne 310. SHA-256 : `b3a8ffad5313fd737b32a1d81596d1612a43b2804ff10b40724afc124fb2e818`.

Scénarios : Conformité du traitement A05b.

~~~~text
### Requirement: Contrat A05b — Objectifs initiaux validés, qualification requise

Le rôle chargé du traitement A05b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A05b

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026. Ces
valeurs sont les objectifs initiaux du cadrage, à mesurer sur chaque profil ;
elles ne sont ni des performances démontrées ni des valeurs imposées par
WireGuard ou NetBird. Elles sont des paramètres documentés par profil dans
les limites retenues ; leur modification nécessite une décision explicite.
L'affectation détaillée des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

Les renouvellements exigent une nouvelle décision valide ; la répétition d'une
ancienne preuve ne remet pas un compteur à zéro. L'expiration n'ajoute aucune
période de grâce. L'UTC contractuel et la confiance temporelle restent requis.
Pause, reprise, snapshot et restauration doivent empêcher la réactivation
d'un accès périmé avant toute reprise des échanges. Un profil qui ne démontre
pas les délais retenus n'est pas déclaré conforme ; leur modification exige
une décision explicite documentée.

##### Application au PA — A05b

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026, commun
avec le cadrage PZT. Ces objectifs doivent être mesurés sur chaque profil Linux,
Windows, VM, Docker et LXC ; aucune performance n'est présumée démontrée.
Ils sont des paramètres documentés par profil dans les limites retenues ;
leur modification nécessite une décision explicite. L'affectation détaillée
des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

PA ne prolonge aucune échéance en rejouant une preuve et n'ajoute aucune
période de grâce. Pause, reprise, snapshot et restauration doivent empêcher
la réactivation d'un accès périmé avant toute reprise des échanges. La confiance
temporelle reste requise ; un profil sans preuve des délais retenus n'est pas
déclaré conforme. Leur modification exige une décision explicite documentée.

#### Scenario: Conformité du traitement A05b

- **WHEN** un profil revendique le traitement A05b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
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

### Référence courante zt-controller-0075d78b8361

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 11. SHA-256 : `0075d78b83619c5def0567a914d7afbf54e7fb7afa52b4345dbe2a80e6bc8b80`.

Scénarios : Nouvelle configuration.

~~~~text
### Requirement: CZT obligatoire et périmètre

Chaque ZT MUST avoir au moins un CZT exécuté par PZT. CZT MUST gérer enrôlement technique, acteurs et organisation ZT, carte réseau, adressage des pairs, distribution des configurations et réconciliation ; PBO MUST conserver administration et supervision par contrats publics.

#### Scenario: Nouvelle configuration

- **WHEN** une politique réseau est administrée depuis PBO
- **THEN** sa référence est conservée par CZT sans écriture directe PBO dans les tables privées.
~~~~

### Référence courante zt-controller-99c13d6319c5

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 20. SHA-256 : `99c13d6319c59dbbc43992c47acd6cca1d2c2df7f27ece1b9ac68a44f840dc2a`.

Scénarios : Ajout de CZT.

~~~~text
### Requirement: Base propre chiffrée et initialisation

CZT MUST posséder une PG logique indépendante de PBO, des bases Instance/Domaine, DZT et PKIZT, chiffrée localement. Le premier CZT MUST l'initialiser ; chaque CZT supplémentaire MUST synchroniser sa réplique avec le primaire sans créer de source concurrente.

#### Scenario: Ajout de CZT

- **WHEN** un CZT est ajouté
- **THEN** sa base est synchronisée et vérifiée avant l’autorité correspondante.
~~~~

### Référence courante zt-controller-a3a1fca8cc08

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 29. SHA-256 : `a3a1fca8cc08c66028525454eb093f5df69735c8571174ce4b9eac4bbd594e0b`.

Scénarios : Réplique requise absente.

~~~~text
### Requirement: Durabilité synchrone et promotion

CZT MUST confirmer l'écriture après persistance sur le primaire et les répliques synchrones requises. Le minimum MUST être configurable sans diminution automatique en cas de panne. La bascule automatique MUST être encadrée, exclure l'ancien primaire, vérifier le candidat et conserver les écritures confirmées.

#### Scenario: Réplique requise absente

- **WHEN** le nombre de confirmations est inférieur au minimum configuré
- **THEN** l’écriture n’est pas confirmée par une réduction automatique du minimum.
~~~~

### Référence courante zt-controller-5f13908e4a13

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 38. SHA-256 : `5f13908e4a13140cc9c13d07a3e2ba28739ea6998ceb41162998bbdce41205a6`.

Scénarios : Échéance pendant panne.

~~~~text
### Requirement: Continuité bornée sans primaire

Sans CZT primaire opérationnel, les échanges MUST rester limités aux autorisations encore valides et aux révocations connues. Les opérations requérant CZT MUST être suspendues ; un cache MUST NOT émettre ou prolonger de nouveaux droits.

#### Scenario: Échéance pendant panne

- **WHEN** une autorisation expire sans primaire disponible
- **THEN** l’accès cesse sans grâce ni renouvellement local.
~~~~

### Référence courante zt-controller-a844ba947c3b

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 47. SHA-256 : `a844ba947c3b675f86146904664b15a71a511bff9a7bba354ee3e5e7446cde46`.

Scénarios : Deux rôles demandent des règles.

~~~~text
### Requirement: Gestionnaire réseau et propriétaire unique

Le socle PZT MUST coordonner interfaces, adressage, routage et pare-feu selon les références CZT, en agrégeant les besoins des rôles sous un propriétaire d'écriture par périmètre. Le profil MUST gérer le périmètre PZT par défaut et MAY gérer globalement l'hôte sur choix explicite.

#### Scenario: Deux rôles demandent des règles

- **WHEN** GZT et DZT demandent des règles sur un même périmètre
- **THEN** le gestionnaire commun les réconcilie sans écrivains concurrents ni écrasement hors mandat.
~~~~

### Référence courante zt-controller-0b71d7d52f1b

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 56. SHA-256 : `0b71d7d52f1b610117e914b3e44b53e11b9824b9ef3da9565f6c8e188849e39d`.

Scénarios : Dérive sans correction autorisée.

~~~~text
### Requirement: Backends et protection des échéances

Les profils MUST qualifier Linux nftables et les capacités demandées iptables/ip6tables/ipset, ainsi que le pare-feu Windows/WFP, sans interchangeabilité présumée. La protection indépendante des autorisations MUST être obligatoire. Configuration déclarative/versionnée/reconstruisible et dérives détectées MUST être distinguées de la correction automatique configurable et désactivée par défaut.

#### Scenario: Dérive sans correction autorisée

- **WHEN** un écart au pare-feu est observé sans politique de réparation
- **THEN** le constat et la mise en sécurité prévue sont rapportés sans correction non autorisée.
~~~~

### Référence courante zt-controller-b3bc36187257

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 65. SHA-256 : `b3bc3618725797ff4d27c7f5f2d60dd14f808c15d04e1aa0b17a068cc4b6cfd8`.

Scénarios : Réponse perdue.

~~~~text
### Requirement: Amorçage et opérations multi-rôles

L'amorçage technique MUST être limité et borné, distinct du contrôle normal. Une opération multi-rôles MUST posséder un propriétaire unique, un suivi durable et une reprise sans double effet, avec revalidation des mandats et préconditions.

#### Scenario: Réponse perdue

- **WHEN** une étape multi-rôles a pu produire son effet sans réponse
- **THEN** la reprise réconcilie les propriétaires avant répétition.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 146 | [Continuité sans PBO et reprise locale PZT](../../specs/pixs-agent/spec.md#L146) | ND | CANDIDAT_PROFIL_PA |
| pzt / 39 | [Autorités, politiques et délégations distinctes](../../specs/pzt/spec.md#L39) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 66 | [Expiration, révocation et protection indépendante](../../specs/pzt/spec.md#L66) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 188 | [Contrat A05b — Objectifs initiaux validés, qualification requise](../../specs/pzt/spec.md#L188) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--aacfb93718

Source : `openspec/specs/pixs-agent/spec.md`, ligne 146. SHA-256 du bloc : `8665641b1007fe45d2b73eb02d5a74fbfbac235ce440d82853ca6540720fbe11`.

~~~~text
### Requirement: Continuité sans PBO et reprise locale PZT

Sans PBO joignable, PA MUST se limiter aux capacités explicitement provisionnées, éligibles et encore valides ; une décision en ligne indisponible MUST bloquer l'action concernée. Diagnostic et reprise depuis PBO MUST passer par PZT, y compris local. Si PZT est entièrement indisponible, une réparation interne/opérateur MUST suivre sa procédure distincte, sans canal de substitution PBO–PA.

#### Scenario: Continuité sans PBO et reprise locale PZT

- **WHEN** PZT est entièrement arrêté
- **THEN** PBO ne reçoit aucun canal de contrôle local de contournement
~~~~

### Référence pzt--95cfbef9df

Source : `openspec/specs/pzt/spec.md`, ligne 39. SHA-256 du bloc : `f1987b9216a3f46255e32ac5aae8ba18a9ac0c2c66f476b0cc8f0fcc810d5c25`.

~~~~text
### Requirement: Autorités, politiques et délégations distinctes

PZT MUST distinguer identité, permission réseau et permission métier ; une position hiérarchique, clé, adresse ou certificat MUST NOT donner un accès implicite. Les relations verticales/horizontales MUST avoir périmètres et sens déclarés. Une délégation MUST identifier émetteur, bénéficiaire, actions, cible, version, validité, révocation et redélégation ; elle MUST NOT transmettre un pouvoir absent de l'émetteur.

#### Scenario: Autorités, politiques et délégations distinctes

- **WHEN** un pair possède une clé valide sans mandat pour le service
- **THEN** le trafic concerné reste refusé
~~~~

### Référence pzt--36bde46b8d

Source : `openspec/specs/pzt/spec.md`, ligne 66. SHA-256 du bloc : `b219ac819e98d78acee76394f5d430a65cb534e017dd32fc8795a6ddf942dbcc`.

~~~~text
### Requirement: Expiration, révocation et protection indépendante

Les autorisations MUST être bornées, réutilisables seulement selon leur classe et retirées dès révocation connue. Les objectifs initiaux A05b MUST être qualifiés par profil : révocation en 5 s maximum lorsque PA est joignable et fermeture après panne PA en 10 s maximum, détection comprise, avec toute échéance antérieure prioritaire. Une interface noyau persistante après crash MUST NOT prolonger un accès.

#### Scenario: Expiration, révocation et protection indépendante

- **WHEN** PA plante alors que WireGuard reste actif dans le noyau
- **THEN** la protection indépendante ferme les accès dans le budget qualifié
~~~~

### Référence pzt--4b8f11c8f2

Source : `openspec/specs/pzt/spec.md`, ligne 188. SHA-256 du bloc : `a99a9136e3e01efb3750e0bab2dd913bcdaae49a9d3a7accad8d14b60e5c9695`.

~~~~text
### Requirement: Contrat A05b — Objectifs initiaux validés, qualification requise

Le rôle chargé du traitement A05b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A05b

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026. Ces
valeurs sont les objectifs initiaux du cadrage, à mesurer sur chaque profil ;
elles ne sont ni des performances démontrées ni des valeurs imposées par
WireGuard ou NetBird. Elles sont des paramètres documentés par profil dans
les limites retenues ; leur modification nécessite une décision explicite.
L'affectation détaillée des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

Les renouvellements exigent une nouvelle décision valide ; la répétition d'une
ancienne preuve ne remet pas un compteur à zéro. L'expiration n'ajoute aucune
période de grâce. L'UTC contractuel et la confiance temporelle restent requis.
Pause, reprise, snapshot et restauration doivent empêcher la réactivation
d'un accès périmé avant toute reprise des échanges. Un profil qui ne démontre
pas les délais retenus n'est pas déclaré conforme ; leur modification exige
une décision explicite documentée.

##### Application au PA — A05b

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026, commun
avec le cadrage PZT. Ces objectifs doivent être mesurés sur chaque profil Linux,
Windows, VM, Docker et LXC ; aucune performance n'est présumée démontrée.
Ils sont des paramètres documentés par profil dans les limites retenues ;
leur modification nécessite une décision explicite. L'affectation détaillée
des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

PA ne prolonge aucune échéance en rejouant une preuve et n'ajoute aucune
période de grâce. Pause, reprise, snapshot et restauration doivent empêcher
la réactivation d'un accès périmé avant toute reprise des échanges. La confiance
temporelle reste requise ; un profil sans preuve des délais retenus n'est pas
déclaré conforme. Leur modification exige une décision explicite documentée.

#### Scenario: Conformité du traitement A05b

- **WHEN** un profil revendique le traitement A05b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

