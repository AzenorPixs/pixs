# Références normatives — PA06

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Arrêt contrôlé et résultats réellement observés | 1 | pixs-agent-3533ebda136d |
| pixs-agent | Exécution locale et états indéterminés | 1 | pixs-agent-ff6703508e08 |
| pixs-agent | Persistance technique locale bornée | 1 | pixs-agent-a6e65255bc57 |
| pixs-agent | Continuité sans PBO et reprise locale PZT | 1 | pixs-agent-6feb1d62a194 |
| runtime | Modes d'exploitation de l'Instance Pixs | 3 | runtime-70f9ed180e36 |
| runtime | Profil de ressources par environnement d'exécution | 2 | runtime-8ed328ffce88 |
| runtime | Dimensionnement explicite et borné des processus | 2 | runtime-3ce9aec52469 |
| runtime | Proposition de dimensionnement sous configuration | 2 | runtime-de755048420d |
| runtime | Ressources détectées demandées et appliquées distinctes | 1 | runtime-7d3aea0ba45b |
| runtime | Reconfiguration contrôlée des ressources | 2 | runtime-458b3dc08dea |
| runtime | Budgets compatibles avec les garanties du profil | 1 | runtime-8d2bbb39224e |
| runtime | Supervision et qualification des profils de ressources | 2 | runtime-ec9dbe73ece1 |
| runtime | Profils distincts d'un même artefact | 1 | runtime-7512034d8e39 |
| runtime | Profils de déploiement déclarés | 1 | runtime-dca47b251323 |
| runtime | Exposition minimale par défaut | 1 | runtime-319952b35a94 |
| runtime | Processus stateless et coordination persistante | 2 | runtime-26521a951f1b |
| runtime | Lease du scheduler avec clôture de péremption | 1 | runtime-9891d8cc1ee3 |
| runtime | Arrêt, drain et reprise contrôlés | 1 | runtime-f54c7549da9f |
| runtime | États techniques PA et PZT distincts du runtime PBO | 1 | runtime-66409ab97dee |
| runtime | Topologies locales et distantes PA PZT | 3 | runtime-7dccbd5ebdc7 |
| runtime | Contrat commun runtime et Kernel agnostique du FOURNISSEUR | 4 | runtime-9ed7a8c48d44 |
| managed-device-policies | Cibles V1 et exécutants locaux | 1 | managed-device-policies-8a43d725b9c8 |
| managed-device-policies | Gestion ZT et jonction d’authentification distinctes | 1 | managed-device-policies-f3d868c20f8b |
| managed-device-policies | Politiques communes et spécifiques | 1 | managed-device-policies-0fc04bee903f |
| managed-device-policies | Priorités et contradictions | 1 | managed-device-policies-a7f801c0bbd9 |
| managed-device-policies | Application par PA et état vérifié | 1 | managed-device-policies-fc87e0db8071 |
| managed-device-policies | Session hors ligne bornée | 1 | managed-device-policies-53ac3cf3063d |
| managed-device-policies | Rotation des secrets machine et services | 1 | managed-device-policies-0e3d3ee17150 |
| managed-device-policies | Redémarrage par profil et conclusion après reprise | 1 | managed-device-policies-0a228d3c9bf5 |

### Référence courante pixs-agent-3533ebda136d

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 139. SHA-256 : `3533ebda136d4edf853de321bbf9213dea107970252c2d7cae589b6770147394`.

Scénarios : Arrêt contrôlé et résultats réellement observés.

~~~~text
### Requirement: Arrêt contrôlé et résultats réellement observés

Les traitements system-stop et session-stop MUST avoir un budget maximal, un ordre déclaré avec les démons et dépendances, et une protection contre les doublons. PZT MUST être conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt. Panne électrique, arrêt forcé et perte du processus MUST NOT être présentés comme une fermeture exécutée ou un résultat livré.

#### Scenario: Arrêt contrôlé et résultats réellement observés

- **WHEN** le conteneur disparaît avant confirmation du traitement d'arrêt
- **THEN** le résultat reste incomplet ou inconnu et aucun succès n'est inventé
~~~~

### Référence courante pixs-agent-ff6703508e08

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 175. SHA-256 : `ff6703508e08fae91c497ab9d48d344859dcbb01e261dec40a9f0c8004849dd4`.

Scénarios : Exécution locale et états indéterminés.

~~~~text
### Requirement: Exécution locale et états indéterminés

Chaque opération MUST déclarer préconditions, postconditions, effets, codes stables, caractère rejouable et stratégie d'erreur. Après crash entre effet et persistance du résultat, PA MUST vérifier la postcondition ou demander une intervention autorisée avant réexécution. Simulation, préparation, exécution et confirmation MUST rester distinctes ; une simulation MUST NOT produire de mutation.

#### Scenario: Exécution locale et états indéterminés

- **WHEN** un crash survient après un effet système avant son enregistrement
- **THEN** la reprise distingue l'effet inconnu et évite une réexécution aveugle
~~~~

### Référence courante pixs-agent-a6e65255bc57

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 202. SHA-256 : `a6e65255bc577e1dfeea39f5c29665a8520cc4b702939f29a4f169d9d5332ea8`.

Scénarios : Persistance technique locale bornée.

~~~~text
### Requirement: Persistance technique locale bornée

Les seuls états techniques locaux nécessaires à l'exécution, déduplication, résultats en attente et reprise MUST avoir un propriétaire, un contrat de durabilité, des limites, une rétention, une protection et une stratégie de corruption/restauration déclarés. Ils MUST NOT devenir une source de vérité métier. Un stockage requis plein ou corrompu MUST bloquer les opérations sans preuve durable ; en conteneur il MUST NOT dépendre du filesystem éphémère.

#### Scenario: Persistance technique locale bornée

- **WHEN** l'état durable de reprise est corrompu
- **THEN** les traitements dépendants restent bloqués sans état remis à zéro implicitement
~~~~

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

### Référence courante runtime-70f9ed180e36

Source : [runtime](../../specs/runtime/spec.md), ligne 23. SHA-256 : `70f9ed180e36a15dea6dd7a550142c41a0e9bcf7609a02521181d92778856956`.

Scénarios : Standalone avec PA; Premier Domaine; Mode Domaine.

~~~~text
### Requirement: Modes d'exploitation de l'Instance Pixs

Les modes d'exploitation MUST appartenir à l'Instance Pixs selon pixs-instance : Standalone, ZT et Domaine. Ils MUST utiliser le même binaire PBO Nuitka standalone et conserver les modules essentiels. Standalone MAY utiliser PZT pour PA ; le premier Domaine MUST exiger ZT complètement initialisé. Panne ou révocation MUST NOT changer implicitement le mode ou autoriser un canal PBO–PA hors PZT.

#### Scenario: Standalone avec PA

- **WHEN** une Instance Standalone sollicite PA
- **THEN** elle utilise un transport PZT admissible sans devenir automatiquement une Instance en mode ZT.

#### Scenario: Premier Domaine

- **WHEN** une création de Domaine vise une Instance dont le ZT n’est pas complètement initialisé
- **THEN** la transition est bloquée avec ses prérequis manquants.

#### Scenario: Mode Domaine

- **WHEN** une Instance active son premier Domaine après vérifications
- **THEN** son mode devient Domaine et aucune panne ne réactive Standalone.
~~~~

### Référence courante runtime-8ed328ffce88

Source : [runtime](../../specs/runtime/spec.md), ligne 42. SHA-256 : `8ed328ffce8810b53b226a6c80b7f3f8ac05fe14ba5467717a9ed16fc2705c02`.

Scénarios : Quota inférieur aux ressources physiques; Exécutant distant.

~~~~text
### Requirement: Profil de ressources par environnement d'exécution

PBO, chaque rôle PA et PZT MUST disposer de profils de ressources distincts liés à leur environnement d'exécution. Le dimensionnement MUST respecter CPU, mémoire et quotas réellement accordés à la machine, VM, conteneur ou service, ainsi que les dépendances et la marge système déclarées. Les ressources physiques de l'hôte MUST NOT remplacer les limites effectives du profil.

#### Scenario: Quota inférieur aux ressources physiques

- **WHEN** un conteneur dispose d'un quota CPU et mémoire inférieur à celui du serveur
- **THEN** le plan utilise ce quota effectif et conserve une marge déclarée pour les processus et dépendances cohébergés

#### Scenario: Exécutant distant

- **WHEN** un PA ou PZT dépend d'un PBO situé sur une autre machine
- **THEN** son profil utilise les ressources de son propre environnement et non celles de PBO
~~~~

### Référence courante runtime-3ce9aec52469

Source : [runtime](../../specs/runtime/spec.md), ligne 56. SHA-256 : `3ce9aec52469b57c6ac7285c411652f92214f2666ced11badb5d564e06582e93`.

Scénarios : Multiplication des connexions; Rôle inconnu ou budget invalide.

~~~~text
### Requirement: Dimensionnement explicite et borné des processus

Le profil MUST déclarer les rôles actifs, nombres de processus, concurrence, files et buffers bornés, budgets CPU et mémoire et plafonds de connexions requis. La somme des instances et réplicas MUST être contrôlée face au budget accordé et aux dépendances, notamment PostgreSQL. Un nombre de cœurs MUST NOT déterminer seul le nombre de workers. Des rôles supplémentaires MAY être déclarés sous contrats validés.

#### Scenario: Multiplication des connexions

- **WHEN** une configuration augmente les processus web ou worker
- **THEN** les limites cumulées de mémoire, concurrence et connexions sont revalidées avant application

#### Scenario: Rôle inconnu ou budget invalide

- **WHEN** un profil demande un rôle non déclaré, une limite invalide ou une concurrence hors bornes
- **THEN** le périmètre concerné reste non prêt avec un diagnostic explicite
~~~~

### Référence courante runtime-de755048420d

Source : [runtime](../../specs/runtime/spec.md), ligne 70. SHA-256 : `de755048420d710bd05966aaa359d67dfe97ebb452dbbf96e5d0d53e68a31ecc`.

Scénarios : Détection sans politique d'adaptation; Adaptation sous politique.

~~~~text
### Requirement: Proposition de dimensionnement sous configuration

Une détection des ressources MAY proposer un dimensionnement. Son application MUST résulter d'une configuration explicite et versionnée ou d'une politique d'adaptation préautorisée et bornée. Une variation observée, un redémarrage ou une pression de charge MUST NOT modifier silencieusement les rôles, processus, budgets ou capacités sélectionnées.

#### Scenario: Détection sans politique d'adaptation

- **WHEN** les ressources observées changent sans politique préautorisée applicable
- **THEN** le système rapporte l'écart et ne modifie pas implicitement le plan demandé

#### Scenario: Adaptation sous politique

- **WHEN** une politique autorise une plage de processus et ses conditions de changement
- **THEN** seul un plan dans cette plage et revalidé peut être appliqué, avec suivi de son résultat
~~~~

### Référence courante runtime-7d3aea0ba45b

Source : [runtime](../../specs/runtime/spec.md), ligne 84. SHA-256 : `7d3aea0ba45b5a5cd0210f91ec988793538fe37c49a59ad39fba1f27370387a3`.

Scénarios : Application partielle d'un profil.

~~~~text
### Requirement: Ressources détectées demandées et appliquées distinctes

Le diagnostic MUST distinguer ressources détectées, budget accordé, configuration demandée, configuration effective et état réellement appliqué, avec origine, version et erreurs. Un plan calculé, transmis ou accepté MUST NOT être présenté comme appliqué sans observation vérifiable. PBO MUST suivre séparément les états PA et PZT via leurs contrats de gestion.

#### Scenario: Application partielle d'un profil

- **WHEN** un exécutant reçoit une configuration mais ne peut appliquer une partie du budget ou du nombre de processus
- **THEN** l'état partiel ou en échec est rapporté sans inventer un état appliqué ni masquer la dernière observation connue
~~~~

### Référence courante runtime-458b3dc08dea

Source : [runtime](../../specs/runtime/spec.md), ligne 93. SHA-256 : `458b3dc08dea1291171c412c99ae91ba84ca2f8ab5c18ae63aebc972fa278cad`.

Scénarios : Réduction de workers occupés; Plusieurs schedulers.

~~~~text
### Requirement: Reconfiguration contrôlée des ressources

Tout changement de processus ou de budget MUST être autorisé, validé puis appliqué par le lifecycle et le superviseur déclarés, avec drain borné, reprise et contrôle de l'état appliqué. La réduction de workers MUST préserver les travaux et leur déduplication. La réplication des schedulers MUST conserver bail persistant et clôture de péremption par périmètre.

#### Scenario: Réduction de workers occupés

- **WHEN** le plan réduit la concurrence pendant des travaux engagés
- **THEN** les travaux sont terminés ou restitués selon leur contrat sans perte ni double effet non maîtrisé

#### Scenario: Plusieurs schedulers

- **WHEN** plusieurs processus scheduler sont configurés pour le même périmètre
- **THEN** seul le détenteur d'un bail courant peut déclencher les travaux et un ancien détenteur est refusé
~~~~

### Référence courante runtime-8d2bbb39224e

Source : [runtime](../../specs/runtime/spec.md), ligne 107. SHA-256 : `8d2bbb39224ecd1cd7761f560d6211ddc564ddb63e6a9419ff869001b0f14b1f`.

Scénarios : Ressources insuffisantes pour une garantie.

~~~~text
### Requirement: Budgets compatibles avec les garanties du profil

Un profil de ressources MUST préserver autorisation, isolation, audit, durabilité, révocation, santé et budgets temporels applicables. Une insuffisance initiale MUST bloquer l'admission du profil ; une perte de capacité en service MUST conduire au comportement sûr déclaré. La charge MUST NOT justifier un privilège supplémentaire, une expiration prolongée ou un contournement PZT.

#### Scenario: Ressources insuffisantes pour une garantie

- **WHEN** le budget ne permet pas de respecter une garantie obligatoire de sécurité ou de reprise
- **THEN** le profil est refusé ou le périmètre en service passe à son état sûr déclaré, sans assouplir cette garantie
~~~~

### Référence courante runtime-ec9dbe73ece1

Source : [runtime](../../specs/runtime/spec.md), ligne 116. SHA-256 : `ec9dbe73ece136d8e782486be999a40b386ff77fa1651d101e6312101399df2e`.

Scénarios : Profil sans recette de ressources; Redémarrage supervisé.

~~~~text
### Requirement: Supervision et qualification des profils de ressources

Le superviseur OS ou conteneur déclaré MUST assurer lancement, limites, signaux et redémarrages sous lifecycle Pixs, sans autorité métier ni privilège implicite. La qualification MUST relier binaire, configuration et environnement aux mesures de mémoire, CPU au repos et en charge, latence, débit, saturation et reprise ; une simple compilation MUST NOT valoir qualification.

#### Scenario: Profil sans recette de ressources

- **WHEN** un profil dispose d'un binaire et d'une configuration mais d'aucune mesure sur la cible
- **THEN** il reste non qualifié pour ses performances et limites annoncées

#### Scenario: Redémarrage supervisé

- **WHEN** un superviseur redémarre un processus défaillant
- **THEN** les identités, préconditions, budgets et états de reprise sont revalidés sans octroi de droits ni remise à zéro des garanties
~~~~

### Référence courante runtime-7512034d8e39

Source : [runtime](../../specs/runtime/spec.md), ligne 130. SHA-256 : `7512034d8e3909ce0e73c0f55455a6d3945f4a8151cd43eb278abad5201e6d88`.

Scénarios : Profil activé par configuration.

~~~~text
### Requirement: Profils distincts d'un même artefact

Les rôles web, worker et scheduler MUST être des profils du même binaire PBO commun, activés par configuration explicite sans branche fonctionnelle cachée. Le développement MAY les regrouper ; la production MUST permettre plusieurs processus par rôle selon le plan de ressources, les capacités sélectionnées et les règles de coordination, sans imposer un processus par module.

#### Scenario: Profil activé par configuration

- **WHEN** un déploiement produit un worker et un scheduler à partir du même artefact
- **THEN** leurs capacités et limites respectives sont inspectables sans code divergent
~~~~

### Référence courante runtime-dca47b251323

Source : [runtime](../../specs/runtime/spec.md), ligne 139. SHA-256 : `dca47b251323064d659c1023ea4e0aaf5615f09a68def2ecf4a0a70f3002343c`.

Scénarios : Capacité absente dans un profil local.

~~~~text
### Requirement: Profils de déploiement déclarés

Une release MAY déclarer des profils tels que développement local, mono-tenant,
multi-tenant ou haute disponibilité. Chaque profil MUST identifier ses
capacités garanties, dépendances obligatoires, limites et capacités désactivées
et MUST NOT modifier silencieusement les invariants de sécurité ou de périmètre.

#### Scenario: Capacité absente dans un profil local

- **WHEN** un profil de développement n'active pas une capacité optionnelle
- **THEN** cette absence est déclarée et le profil ne prétend pas fournir la garantie associée
~~~~

### Référence courante runtime-319952b35a94

Source : [runtime](../../specs/runtime/spec.md), ligne 151. SHA-256 : `319952b35a94da3d6bac370d0f7363cff682a26aee34b8a84d017e3edc042ff1`.

Scénarios : Endpoint de management publiquement joignable.

~~~~text
### Requirement: Exposition minimale par défaut

Seul le profil web MUST être exposé à l'entrée publique par défaut ; workers, schedulers, files, stores de coordination et endpoints de management MUST rester sur un réseau privé ou derrière une frontière authentifiée, autorisée et auditée.

#### Scenario: Endpoint de management publiquement joignable

- **WHEN** un endpoint de management se retrouve atteignable depuis le trafic public sans frontière explicite
- **THEN** la composition est déclarée invalide et l'exposition est refusée
~~~~

### Référence courante runtime-26521a951f1b

Source : [runtime](../../specs/runtime/spec.md), ligne 160. SHA-256 : `26521a951f1b63d4d7a2cd62c6a6889fb1ca3f381068d718d86947d134990920`.

Scénarios : Redémarrage d'un worker; État technique PA requis en conteneur.

~~~~text
### Requirement: Processus stateless et coordination persistante

Les processus du runtime applicatif PBO web, worker et scheduler MUST NOT conserver en mémoire ou sur disque local un état nécessaire à l’autorité métier, à l’idempotence, à la reprise ou aux sessions. Leur coordination MUST reposer sur la persistance de référence ; un verrou mémoire n’est qu’une optimisation sans garantie. Les états techniques PA MUST suivre leur exigence distincte ci-dessous.

#### Scenario: Redémarrage d'un worker

- **WHEN** un worker PBO est redémarré en cours de traitement
- **THEN** ses travaux reprennent depuis la persistance de référence sans double effet non maîtrisé

#### Scenario: État technique PA requis en conteneur

- **WHEN** un profil PA nécessite un état durable de reprise
- **THEN** l’exigence distincte des états techniques PA est satisfaite sans autorité métier locale
~~~~

### Référence courante runtime-9891d8cc1ee3

Source : [runtime](../../specs/runtime/spec.md), ligne 174. SHA-256 : `9891d8cc1ee3009493fdce3b402d5d67ee2f82f3cae035090fe1f0f2d26b5deb`.

Scénarios : Ancien détenteur toujours actif.

~~~~text
### Requirement: Lease du scheduler avec clôture de péremption

Le scheduler MUST acquérir un lease persistant borné, renouvelable et expirant, avec un mécanisme vérifiable empêchant un ancien détenteur d'agir après expiration.

#### Scenario: Ancien détenteur toujours actif

- **WHEN** une instance perd son lease puis tente de déclencher un traitement
- **THEN** sa requête est rejetée par la clôture de péremption et l'état reste diagnostiquable
~~~~

### Référence courante runtime-f54c7549da9f

Source : [runtime](../../specs/runtime/spec.md), ligne 183. SHA-256 : `f54c7549da9f971f61196dca4352a8deaa9357fc14bd4f55585d02121d6df251`.

Scénarios : Arrêt pendant traitement.

~~~~text
### Requirement: Arrêt, drain et reprise contrôlés

L'arrêt MUST être contrôlé : cesser l'exposition, drainer les traitements en cours dans une durée bornée puis s'éteindre sur un état explicite ; une instance défaillante MUST NOT recevoir de trafic.

#### Scenario: Arrêt pendant traitement

- **WHEN** une instance reçoit un signal d'arrêt pendant un traitement engagé
- **THEN** elle termine ou restitue le traitement selon son contrat et atteint un état final sans perte silencieuse
~~~~

### Référence courante runtime-66409ab97dee

Source : [runtime](../../specs/runtime/spec.md), ligne 192. SHA-256 : `66409ab97dee43b14196460aa53853628c9cfed2fee35dfceb2dd56f701af6f8`.

Scénarios : Recréation du conteneur PA PZT.

~~~~text
### Requirement: États techniques PA et PZT distincts du runtime PBO

PA et PZT MUST conserver des états techniques locaux distincts selon leurs
contrats, bornés, protégés et durables lorsque requis, sans autorité métier ni
stockage implicite du runtime PBO. Leurs états de reprise MUST NOT dépendre
du filesystem éphémère d'un conteneur. Leurs profils MUST déclarer propriétaires,
comptes, signaux, préconditions et séquencement d'arrêt sans lancer de rôle implicite.

#### Scenario: Recréation du conteneur PA PZT

- **WHEN** un conteneur PA/PZT est recréé
- **THEN** les exécutants reprennent depuis leurs stockages déclarés sans fusion des états ou autorité métier locale
~~~~

### Référence courante runtime-7dccbd5ebdc7

Source : [runtime](../../specs/runtime/spec.md), ligne 205. SHA-256 : `7dccbd5ebdc79c1450ccd870a5e0797c433cf7f0a4932b567f5ce8a756a38ca6`.

Scénarios : Hôte local avec tous les composants; Hôte distant sans backend local; Hôte distant avec backend local.

~~~~text
### Requirement: Topologies locales et distantes PA PZT

Les profils MUST permettre la colivraison PA/PZT avec ou sans PBO/PFO locaux.
Un hôte distant MAY héberger aussi PBO/PFO ; cette présence MUST NOT accorder
un droit sur un autre exécutant. Chaque relation PBO–PA/PZT MUST déclarer
périmètre, autorité et contrats. Les échanges PBO–PA MUST toujours utiliser
PZT ; le contrôle PBO–PZT MUST conserver ses interfaces sécurisées.

#### Scenario: Hôte local avec tous les composants

- **WHEN** PBO/PFO, PA et PZT partagent un environnement d'exécution
- **THEN** pixs.agent gère PA hors PZT, pixs.pzt gère PZT et le profil local conserve les contrôles PZT

#### Scenario: Hôte distant sans backend local

- **WHEN** PA/PZT est déployé sur un hôte sans PBO/PFO
- **THEN** le PBO distant autorisé gère les exécutants par les contrats de pixs.agent et pixs.pzt via PZT

#### Scenario: Hôte distant avec backend local

- **WHEN** un hôte distant comprend PBO/PFO, PA et PZT
- **THEN** son PBO peut gérer les exécutants locaux ou distants dans ses seuls périmètres autorisés, sans priorité implicite sur un autre PBO
~~~~

### Référence courante runtime-9ed7a8c48d44

Source : [runtime](../../specs/runtime/spec.md), ligne 227. SHA-256 : `9ed7a8c48d448b3e568c04091394dae49576118ab2e51750256784e92d96e97e`.

Scénarios : Garde d’usage avec intervalle prouvé; Report distant non probant; Fonction indépendante pendant dégradation; Projection forgée ne prouve pas.

~~~~text
### Requirement: Contrat commun runtime et Kernel agnostique du FOURNISSEUR

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — Contrat runtime commun

Le contrat d’exécution MUST exposer une interface commune en lecture à Kernel, Core, Auth, PA et PZT. Kernel MUST demeurer agnostique du FOURNISSEUR et MUST NOT porter de logique de fournisseur de temps. Les mécanismes génériques de temps demeurent admis lorsqu’ils restent indépendants de tout fournisseur concret. Les dépendances MUST être déclarées et le graphe de démarrage MUST demeurer acyclique. Les fonctions indépendantes du temps MUST pouvoir continuer pendant une dégradation. Seuls les effets dont la fenêtre ou l’exigence ne peut pas être prouvée MUST être refusés. Le présent texte MUST NOT prolonger un certificat ni un mandat par une dégradation du temps.

Le contrat `pixs.time.evidence` version `2.0.0`, catégorie `API`, propriétaire `pixs.kernel` est une déclaration pure. Les quatre méthodes exigées sont `time_diagnostic(use_ref:TimePublicRef)->TimeDiagnostic`, `time_require_use(use_ref:TimePublicRef)->None`, `time_ceremony_diagnostic(ceremony_ref:TimePublicRef)->TimeDiagnostic`, `time_ceremony_require_use(ceremony_ref:TimePublicRef)->None`. `TimePublicRef` est un sélecteur non autoritaire lié à l’opération courante dont l’appelant ne choisit jamais le producteur, le producteur attendu est injecté par composition. `outcome` vaut exactement `OBSERVED`, `REFUSED` ou `IN_DOUBT`. `TimeDiagnostic` comporte exactement `outcome`, `producer_ref`, `clock_domain_ref`, `detail_ref`. Le producteur vérifie nativement au point d’usage, aucun objet Python, pointeur ou descripteur comme preuve transportée. `None`, DTO et ancienne observation ne sont en aucun cas une permission. Core, Auth, Agent et PZT décident sur l’intervalle entier y compris transitions `DENY` et `ALLOW`, avec décisions et gardes métier inchangées.

#### Scenario: Garde d’usage avec intervalle prouvé

- **WHEN** le producteur courant fournit un intervalle vérifié avec incertitude bornée
- **THEN** le consommateur l’emploie pour sa seule décision courante sans le mémoriser comme preuve

#### Scenario: Report distant non probant

- **WHEN** seul un report distant ou monotone étranger est disponible sans corrélation locale qualifiée
- **THEN** le consommateur rend un diagnostic seul sans bail ni observation positive

#### Scenario: Fonction indépendante pendant dégradation

- **WHEN** une fonction ne dépend pas du temps courant et que la preuve de temps est invalide
- **THEN** elle peut continuer sous son propre contrat sans prolongation de droit

#### Scenario: Projection forgée ne prouve pas

- **WHEN** une projection diagnostique, un `None` ou un DTO est réinjecté comme permission
- **THEN** le consommateur refuse sans bail ni observation positive
~~~~

### Référence courante managed-device-policies-8a43d725b9c8

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 11. SHA-256 : `8a43d725b9c8f9f725eb22c048e5e91d1ee208d3af98a44e61ea75cfae643633`.

Scénarios : Poste administré.

~~~~text
### Requirement: Cibles V1 et exécutants locaux

Les profils V1 MUST couvrir postes Linux/Windows et serveurs Linux membres, avec Debian stable et Windows 10/11 admissibles à qualifier. Les postes administrés et serveurs Linux soumis aux politiques MUST disposer de PA/PZT locaux. Les rôles serveur de domaine MUST NOT être imposés sur chaque poste.

#### Scenario: Poste administré

- **WHEN** un poste reçoit une politique Pixs
- **THEN** les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
~~~~

### Référence courante managed-device-policies-f3d868c20f8b

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 20. SHA-256 : `f3d868c20f8b51c27e721a1df72180c8508e9cfdf1ff06948b8294b817119a29`.

Scénarios : Hôte tiers géré.

~~~~text
### Requirement: Gestion ZT et jonction d’authentification distinctes

Un hôte MAY être intégré à ZT et administré sans jonction de domaine pour l'authentification de ses utilisateurs. Cette jonction MUST rester facultative mais exiger l'intégration ZT préalable lorsqu'elle est demandée. Le passage du PA en mode Domaine MUST NOT joindre automatiquement l'hôte au domaine d'authentification.

#### Scenario: Hôte tiers géré

- **WHEN** un hôte rejoint ZT sans jonction d’authentification
- **THEN** PA peut gérer ses capacités autorisées tandis que les utilisateurs conservent l’authentification configurée sur l’hôte.
~~~~

### Référence courante managed-device-policies-0fc04bee903f

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 29. SHA-256 : `0fc04bee903fa7c526db55656c40db141fc78bd93e1a2f658507d54be92da507`.

Scénarios : Règle propre à Windows.

~~~~text
### Requirement: Politiques communes et spécifiques

Les politiques MUST permettre des intentions communes Windows/Linux et des règles propres aux plateformes, avec politiques de poste et d'utilisateur et ciblage explicite. Les capacités non qualifiées MUST être déclarées non applicables ou indisponibles, sans simulation de succès.

#### Scenario: Règle propre à Windows

- **WHEN** une politique commune comporte une règle GPO Windows
- **THEN** l’application Linux ne prétend pas avoir appliqué cette règle native.
~~~~

### Référence courante managed-device-policies-a7f801c0bbd9

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 38. SHA-256 : `a7f801c0bbd9d9343d1e85e137ebc5eb30e56d499daabeba1006d7fe6d26ebbe`.

Scénarios : Deux valeurs au même niveau.

~~~~text
### Requirement: Priorités et contradictions

Les politiques de configuration MUST avoir des priorités explicites ; les contradictions à priorité égale MUST être signalées sans règle implicite du dernier reçu. La résolution MUST respecter les contrats de propriété et autorisations de chaque périmètre.

#### Scenario: Deux valeurs au même niveau

- **WHEN** deux politiques de même priorité imposent des valeurs incompatibles
- **THEN** l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.
~~~~

### Référence courante managed-device-policies-fc87e0db8071

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 47. SHA-256 : `fc87e0db80717cda5b2c979b05d5045ee0bf334a5dd2cf6559bb9d13857e9c0e`.

Scénarios : Configuration reçue sans effet.

~~~~text
### Requirement: Application par PA et état vérifié

PA MUST appliquer les opérations livrées et autorisées dans le contexte système ou utilisateur approprié via pixs.agent. Réception, application, dérive et résultat confirmé MUST rester distincts. Les corrections automatiques MUST posséder leur propre politique et mandat.

#### Scenario: Configuration reçue sans effet

- **WHEN** PA reçoit une politique mais échoue à la mettre en place
- **THEN** PBO affiche l’échec sans état appliqué fictif.
~~~~

### Référence courante managed-device-policies-53ac3cf3063d

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 56. SHA-256 : `53ac3cf3063d580b57f56441ca276f52645441d643d76c41f8e4077b7e5882e7`.

Scénarios : Pas de profil hors ligne.

~~~~text
### Requirement: Session hors ligne bornée

L'ouverture de session hors ligne MAY être permise par profil explicite et borné. Elle MUST conserver les exigences de validité, protection locale et retraits connus ; une panne MUST NOT activer ce profil ni repousser ses échéances.

#### Scenario: Pas de profil hors ligne

- **WHEN** le contrôleur est indisponible sans profil hors ligne autorisé
- **THEN** aucune nouvelle permission de connexion locale n’est déduite de la panne.
~~~~

### Référence courante managed-device-policies-0e3d3ee17150

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 65. SHA-256 : `0e3d3ee171504e6660c5650982a199dc41378de37affda7cbe83cb40f3506336`.

Scénarios : Rotation native autorisée.

~~~~text
### Requirement: Rotation des secrets machine et services

La rotation des secrets machine MUST être sélectionnable par profil entre pilotage Pixs/PBO/PA et rotation native qualifiée. Les services techniques MUST pouvoir utiliser un moyen propre ou une représentation habilitée selon profil. Ces secrets MUST rester distincts du mot de passe des individus changé depuis PBO.

#### Scenario: Rotation native autorisée

- **WHEN** un poste utilise la rotation machine native qualifiée
- **THEN** elle suit son profil et sa cohérence contrôleurs sans autoriser un changement natif du mot de passe individuel.
~~~~

### Référence courante managed-device-policies-0a228d3c9bf5

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 74. SHA-256 : `0a228d3c9bf5969235d9a1b17bf8161742513eb0cd8bfd88e93f3901641b2177`.

Scénarios : Jonction exigeant redémarrage.

~~~~text
### Requirement: Redémarrage par profil et conclusion après reprise

Le profil MUST choisir redémarrage manuel ou automatique sous fenêtre autorisée, avec manuel par défaut. PBO MUST distinguer redémarrage requis et opération terminée ; les vérifications après redémarrage MUST précéder la conclusion de jonction ou de politique.

#### Scenario: Jonction exigeant redémarrage

- **WHEN** la configuration est appliquée mais le poste n’a pas redémarré
- **THEN** l’opération reste à terminer jusqu’aux contrôles après reprise.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 74 | [Arrêt contrôlé et résultats réellement observés](../../specs/pixs-agent/spec.md#L74) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 110 | [Exécution locale et états indéterminés](../../specs/pixs-agent/spec.md#L110) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 137 | [Persistance technique locale bornée](../../specs/pixs-agent/spec.md#L137) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 146 | [Continuité sans PBO et reprise locale PZT](../../specs/pixs-agent/spec.md#L146) | ND | CANDIDAT_PROFIL_PA |
| runtime / 70 | [États techniques PA distincts du runtime PBO](../../specs/runtime/spec.md#L70) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--ecb0f8d963

Source : `openspec/specs/pixs-agent/spec.md`, ligne 74. SHA-256 du bloc : `aed31e04d823e8fbc0d9c3e5cbd3ba326db9fc422077de59ced3026065096002`.

~~~~text
### Requirement: Arrêt contrôlé et résultats réellement observés

Les traitements system-stop et session-stop MUST avoir un budget maximal, un ordre déclaré avec les démons et dépendances, et une protection contre les doublons. PZT MUST être conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt. Panne électrique, arrêt forcé et perte du processus MUST NOT être présentés comme une fermeture exécutée ou un résultat livré.

#### Scenario: Arrêt contrôlé et résultats réellement observés

- **WHEN** le conteneur disparaît avant confirmation du traitement d'arrêt
- **THEN** le résultat reste incomplet ou inconnu et aucun succès n'est inventé
~~~~

### Référence pixs-agent--13250f4b84

Source : `openspec/specs/pixs-agent/spec.md`, ligne 110. SHA-256 du bloc : `ba23e50b4d683e00934ba0b17353a922954d7198013e34a9c52a41d803a5d47b`.

~~~~text
### Requirement: Exécution locale et états indéterminés

Chaque opération MUST déclarer préconditions, postconditions, effets, codes stables, caractère rejouable et stratégie d'erreur. Après crash entre effet et persistance du résultat, PA MUST vérifier la postcondition ou demander une intervention autorisée avant réexécution. Simulation, préparation, exécution et confirmation MUST rester distinctes ; une simulation MUST NOT produire de mutation.

#### Scenario: Exécution locale et états indéterminés

- **WHEN** un crash survient après un effet système avant son enregistrement
- **THEN** la reprise distingue l'effet inconnu et évite une réexécution aveugle
~~~~

### Référence pixs-agent--de6f014038

Source : `openspec/specs/pixs-agent/spec.md`, ligne 137. SHA-256 du bloc : `a2a8cd5382218bdaa810f9d7a390cb550133f43108228b82823d06832e8aa078`.

~~~~text
### Requirement: Persistance technique locale bornée

Les seuls états techniques locaux nécessaires à l'exécution, déduplication, résultats en attente et reprise MUST avoir un propriétaire, un contrat de durabilité, des limites, une rétention, une protection et une stratégie de corruption/restauration déclarés. Ils MUST NOT devenir une source de vérité métier. Un stockage requis plein ou corrompu MUST bloquer les opérations sans preuve durable ; en conteneur il MUST NOT dépendre du filesystem éphémère.

#### Scenario: Persistance technique locale bornée

- **WHEN** l'état durable de reprise est corrompu
- **THEN** les traitements dépendants restent bloqués sans état remis à zéro implicitement
~~~~

### Référence pixs-agent--aacfb93718

Source : `openspec/specs/pixs-agent/spec.md`, ligne 146. SHA-256 du bloc : `8665641b1007fe45d2b73eb02d5a74fbfbac235ce440d82853ca6540720fbe11`.

~~~~text
### Requirement: Continuité sans PBO et reprise locale PZT

Sans PBO joignable, PA MUST se limiter aux capacités explicitement provisionnées, éligibles et encore valides ; une décision en ligne indisponible MUST bloquer l'action concernée. Diagnostic et reprise depuis PBO MUST passer par PZT, y compris local. Si PZT est entièrement indisponible, une réparation interne/opérateur MUST suivre sa procédure distincte, sans canal de substitution PBO–PA.

#### Scenario: Continuité sans PBO et reprise locale PZT

- **WHEN** PZT est entièrement arrêté
- **THEN** PBO ne reçoit aucun canal de contrôle local de contournement
~~~~

### Référence runtime--cc587c5666

Source : `openspec/specs/runtime/spec.md`, ligne 70. SHA-256 du bloc : `76fa9581b4885e8367327b804aae834ad5ddd7fdacbbf5a6c920c6458095b65f`.

~~~~text
### Requirement: États techniques PA distincts du runtime PBO

Les binaires PA MUST rester une couche distincte. Leurs seuls états techniques locaux déclarés par pixs-agent MUST être bornés, protégés et durables lorsque requis, sans autorité métier ni stockage implicite du runtime PBO. Un état PA nécessaire à la reprise MUST NOT dépendre du filesystem éphémère d’un conteneur.

#### Scenario: États techniques PA distincts du runtime PBO

- **WHEN** le conteneur PA est recréé
- **THEN** les états nécessaires reprennent depuis leur stockage déclaré sans données métier rendues autoritatives localement
~~~~

