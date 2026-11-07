# Exigences de réalisation — C18

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| deb-package | Installation des profils de processus configurables | 2 | deb-package-926aeac00173 |
| deb-package | Paquet corrélé à la release | 2 | deb-package-5b3c4661ded9 |
| deb-package | Configuration et secrets hors paquet | 1 | deb-package-74c5e665e921 |
| deb-package | Services alignés sur le lifecycle Pixs | 1 | deb-package-600fdff46383 |
| deb-package | Mise à niveau du paquet sous validation | 1 | deb-package-01f94b4ae1d8 |
| deb-package | Aucune installation de code distant implicite | 1 | deb-package-05b122afbb72 |
| deb-package | Distribution Debian indépendante PA et PBO PFO | 1 | deb-package-4fa707605aa5 |
| deb-package | Trois binaires PA et PZT dans le paquet commun | 1 | deb-package-537d391450a5 |
| deb-package | Première distribution PBO PFO du profil initial | 2 | deb-package-c131fb7ee5bd |
| deb-package | Installation BIND 9 par le PA du rôle serveur DNS Debian | 3 | deb-package-bace0c549172 |
| deb-package | Composition Domaine et responsabilités des services | 1 | deb-package-d49c71ea0d9a |
| pixs-instance | Identité logique et référentiel commun | 1 | pixs-instance-b9b134df059f |
| pixs-instance | Modes Standalone ZT et Domaine | 2 | pixs-instance-18485b8d2051 |
| pixs-instance | ZT entièrement initialisé avant Domaine | 2 | pixs-instance-81a8ae9c0556 |
| pixs-instance | Minima et contrôleurs distincts | 1 | pixs-instance-b189f9cd6424 |
| pixs-instance | Références PG avant et après Domaine | 1 | pixs-instance-9baefb0c5ae7 |
| pixs-instance | Maintenance des écritures pour la transition | 1 | pixs-instance-ebdd233f14af |
| pixs-instance | Administration globale par identités habilitées | 1 | pixs-instance-8c964dc84f92 |
| pixs-instance | Absence de retour Domaine Standalone V1 | 1 | pixs-instance-c159a59d2125 |
| pixs-instance | Habilitations Instance et domaines | 1 | pixs-instance-b7a2b5d23968 |
| reference-composition | Qualification du binaire commun et des profils de ressources P0 | 4 | reference-composition-7131b276f78e |
| reference-composition | Capacités obligatoires du P0 | 1 | reference-composition-0af0b6011293 |
| reference-composition | Capacités hors P0 explicites | 1 | reference-composition-986398c06367 |
| reference-composition | Preuve reproductible | 1 | reference-composition-ab553efe6c54 |
| reference-composition | Profil initial PBO PFO Debian local v1 | 2 | reference-composition-5f1322f3cd28 |
| reference-composition | Garanties du socle conservées dans le profil initial | 1 | reference-composition-70063af8e7b7 |
| reference-composition | Parcours installable et utilisable du profil initial | 1 | reference-composition-2614801b7609 |
| reference-composition | Capacités non sélectionnées du profil initial | 1 | reference-composition-ef9b2d25c156 |
| reference-composition | Preuve de la composition effectivement distribuée | 1 | reference-composition-7961b985d4cc |
| reference-composition | Choix C01 systemd et exception d’amorçage du profil Debian local | 2 | reference-composition-80e3d17e557d |
| reference-composition | Qualification et source de vérité après amorçage | 2 | reference-composition-b86766ab642e |
| reference-composition | Profil Auth standard sans connecteur externe installé | 2 | reference-composition-fa2727180f3d |
| reference-composition | Composition ZT initiale et Domaines | 1 | reference-composition-4f43b97aaed5 |

### Référence courante deb-package-926aeac00173

Source : [deb-package](../../specs/deb-package/spec.md), ligne 8. SHA-256 : `926aeac001739de17ee6fd0d51ee2f9366b343d13d03dc4ea01d0e611f69f809`.

Scénarios : Installation sur deux tailles d'hôte; Paquet PA PZT autonome.

~~~~text
### Requirement: Installation des profils de processus configurables

Le paquet PBO/PFO MUST livrer le binaire PBO commun Nuitka standalone de reference-runtime et les ressources frontend. Les profils PBO et ceux du paquet indépendant PA/PZT MUST suivre runtime et rester configurables hors des artefacts. Les unités de supervision MUST appliquer rôles, instances et budgets déclarés sans installer un démon par module ni déduire un nombre de processus du serveur physique.

#### Scenario: Installation sur deux tailles d'hôte

- **WHEN** le même paquet est installé sur deux environnements aux budgets différents
- **THEN** le binaire reste identique pour la même cible de build et les configurations runtime adaptent les processus sans reconstruire une variante métier

#### Scenario: Paquet PA PZT autonome

- **WHEN** le paquet commun PA/PZT est installé sans PBO local
- **THEN** ses exécutants utilisent leurs profils de ressources propres et un PBO distant autorisé peut les gérer via les contrats existants
~~~~

### Référence courante deb-package-5b3c4661ded9

Source : [deb-package](../../specs/deb-package/spec.md), ligne 22. SHA-256 : `5b3c4661ded958bda4082d235e7871edc1aaf395181a9d4a311c2a1dd0516b01`.

Scénarios : Version de paquet incohérente; Deux paquets indépendants.

~~~~text
### Requirement: Paquet corrélé à la release

Chaque paquet MUST identifier sa release, son périmètre de composition, ses manifests, contrats, compatibilités et garanties. Il MUST rester corrélable aux autres artefacts de cette release pour les capacités communes. Cette corrélation MUST NOT imposer un contenu binaire identique entre le paquet commun PA/PZT, le paquet PBO/PFO et l’image sans fonctions de session ; les noms et versions exactes restent à spécifier.

#### Scenario: Version de paquet incohérente

- **WHEN** un paquet revendique une release différente de l’artefact qu’il installe
- **THEN** l’installation signale l’incohérence et bloque l’activation

#### Scenario: Deux paquets indépendants

- **WHEN** la composition Debian cible est vérifiée
- **THEN** le paquet commun PA/PZT et le paquet PBO/PFO restent distincts selon leurs exigences de composition
~~~~

### Référence courante deb-package-74c5e665e921

Source : [deb-package](../../specs/deb-package/spec.md), ligne 36. SHA-256 : `74c5e665e921aabc9acd2c55b596e47f3df9dcaf8b49c3ea3fc9f5666b87a5ee`.

Scénarios : Secret trouvé dans le paquet.

~~~~text
### Requirement: Configuration et secrets hors paquet

Le paquet MUST NOT embarquer de configuration effective, de référence de secret, de base de données, de volumes persistants ni de fichiers utilisateur ; l'installation MUST consommer une configuration validée et ne rien déduire de l'état accidentel du système de fichiers.

#### Scenario: Secret trouvé dans le paquet

- **WHEN** un artefact de paquet contient une valeur sensible réelle ou apparentée
- **THEN** la publication et l'installation sont refusées avec un diagnostic sans exposition de la valeur
~~~~

### Référence courante deb-package-600fdff46383

Source : [deb-package](../../specs/deb-package/spec.md), ligne 45. SHA-256 : `600fdff463833228f32095565dbd6a432f8ee942f617da406726d4bf6eee7bc6`.

Scénarios : Redémarrage par le gestionnaire de services.

~~~~text
### Requirement: Services alignés sur le lifecycle Pixs

Les unités de service installées MUST alimenter le même lifecycle, les mêmes contrôles de santé et les mêmes signaux d'arrêt que les autres modes de déploiement ; le gestionnaire de services reste un adapter sans autorité métier.

#### Scenario: Redémarrage par le gestionnaire de services

- **WHEN** le gestionnaire de services redémarre une unité
- **THEN** le profil concerné passe par les mêmes étapes de démarrage validé et de mise en service
~~~~

### Référence courante deb-package-01f94b4ae1d8

Source : [deb-package](../../specs/deb-package/spec.md), ligne 54. SHA-256 : `01f94b4ae1d861b6ee1075bb11fa78e57b4a65626bb49806c80aa5b8ede87fe9`.

Scénarios : Mise à niveau interrompue.

~~~~text
### Requirement: Mise à niveau du paquet sous validation

Toute mise à niveau par paquet MUST être une opération explicite soumise à vérification d'identité de distribution, aux contrôles de compatibilité et au plan de migration ; un échec ou un abandon MUST laisser l'ancienne composition ou un état explicitement sûr, sans purge ni activation partielle non diagnostiquée.

#### Scenario: Mise à niveau interrompue

- **WHEN** une mise à niveau de paquet est interrompue après exécution partielle des migrations
- **THEN** le système reste dans un état diagnostiqué et seule une reprise validée ou une restauration autorisée poursuit l'opération
~~~~

### Référence courante deb-package-05b122afbb72

Source : [deb-package](../../specs/deb-package/spec.md), ligne 63. SHA-256 : `05b122afbb72e13b37147e75aa7b400822a4b7091b9d200ccf768f06fb5f96b4`.

Scénarios : Téléchargement proposé à l'installation.

~~~~text
### Requirement: Aucune installation de code distant implicite

Le paquet MUST NOT, par défaut, télécharger, installer ou activer du code distant pendant l'installation ou l'exécution ; un mécanisme de mise à jour de sécurité peut automatiser le déclenchement sans supprimer les validations requises.

#### Scenario: Téléchargement proposé à l'installation

- **WHEN** une routine d'installation tente de récupérer une dépendance distante non vérifiée
- **THEN** l'installation est refusée sauf procédure explicite conforme aux garanties de publication
~~~~

### Référence courante deb-package-4fa707605aa5

Source : [deb-package](../../specs/deb-package/spec.md), ligne 72. SHA-256 : `4fa707605aa505213b7a5fb6970b45819266df4e045b9afebfd1ea1e3a0a3a79`.

Scénarios : Installation sans PBO local.

~~~~text
### Requirement: Distribution Debian indépendante PA et PBO PFO

La distribution Debian MUST conserver un paquet PBO/PFO et un paquet commun
PA/PZT indépendant. PBO/PFO MUST contenir le binaire PBO commun, pixs.core,
pixs.auth, pixs.agent, pixs.pzt et les ressources frontend, sans exécutables PA/PZT.
Le paquet PA/PZT MUST NOT embarquer ni
requérir PBO/PFO locaux comme contenu ; compatibilités et dépendances MUST
rester déclarées. Les noms et versions de paquets restent à spécifier.

#### Scenario: Installation sans PBO local

- **WHEN** PA/PZT est installé sans PBO/PFO locaux
- **THEN** son paquet commun reste indépendant et ses échanges avec un PBO distant autorisé passent par PZT
~~~~

### Référence courante deb-package-537d391450a5

Source : [deb-package](../../specs/deb-package/spec.md), ligne 86. SHA-256 : `537d391450a56e1199d4a3e73481441f7d5cd311431d70bf239698911185fe71`.

Scénarios : Inspection du paquet commun.

~~~~text
### Requirement: Trois binaires PA et PZT dans le paquet commun

Le paquet commun PA/PZT MUST livrer exactement quatre exécutables : trois
binaires PA définis par pixs-agent — démon système, événements de l'hôte,
sessions utilisateur — et le binaire indépendant PZT défini par pzt. Leurs six
modes PA et le mode PZT MUST conserver responsabilités, permissions et cycles
de vie distincts. La séparation MUST NOT ajouter un paquet ou un exécutable.

#### Scenario: Inspection du paquet commun

- **WHEN** le paquet PA/PZT est vérifié
- **THEN** les trois binaires PA et PZT indépendant sont identifiables, sans PBO/PFO embarqués
~~~~

### Référence courante deb-package-c131fb7ee5bd

Source : [deb-package](../../specs/deb-package/spec.md), ligne 99. SHA-256 : `c131fb7ee5bd7c36aff8fd604eab03d55080d3e246ca3d0c286cd8498d7a5d4c`.

Scénarios : Paquet expérimental non vérifiable; Exécution réseau demandée après installation.

~~~~text
### Requirement: Première distribution PBO PFO du profil initial

La première distribution du profil initial MUST être un paquet PBO/PFO indépendant incluant les modules de gestion `pixs.agent` et `pixs.pzt` ainsi que le module DNS essentiel, sans exécutable PA ni PZT embarqué. Son identité expérimentale locale MUST respecter signature, provenance, inventaire, intégrité et révocation exigés par artifact-publication.

#### Scenario: Paquet expérimental non vérifiable

- **WHEN** le paquet initial est local ou expérimental mais son identité de distribution ne peut être vérifiée
- **THEN** il n’est pas installé ni publié comme release qualifiée

#### Scenario: Exécution réseau demandée après installation

- **WHEN** l’opérateur veut activer PZT après installation du paquet PBO/PFO seul
- **THEN** la composition exige un composant PZT admissible et les garanties du profil réseau sélectionné avant cette activation
~~~~

### Référence courante deb-package-bace0c549172

Source : [deb-package](../../specs/deb-package/spec.md), ligne 113. SHA-256 : `bace0c54917252d8ca70995bfa06b5250b576cbb8e1cacf0f93ca1fe8b641bde`.

Scénarios : Installation sous rôle et plan admissibles; PA client sans rôle serveur; Interruption ou version non qualifiée.

~~~~text
### Requirement: Installation BIND 9 par le PA du rôle serveur DNS Debian

Sur Debian, le PA désigné MUST assurer installation et configuration de BIND 9 depuis les paquets de la distribution prise en charge pour un rôle serveur DNS sélectionné et admis. Version du serveur, dépendances et contrôles MUST être identifiables et qualifiés. La présence de PBO ou d'un PA client MUST NOT autoriser cette opération ou activer le rôle serveur.

#### Scenario: Installation sous rôle et plan admissibles

- **WHEN** le PA désigné reçoit une opération courante autorisée d'installation ou de configuration du serveur DNS Debian
- **THEN** il contrôle cible, rôle, version et plan puis applique et rapporte les effets réellement établis
- **AND** une présence admissible déjà vérifiée MUST éviter une réinstallation inutile, sans valoir preuve de configuration ou de service disponible
- **AND** configuration d'instance, données mutables et secrets MUST rester séparés des artefacts immuables selon le profil

#### Scenario: PA client sans rôle serveur

- **WHEN** un PA sans rôle serveur DNS admissible demande l'installation ou l'administration de BIND 9
- **THEN** l'opération est refusée sans transformer ce PA en serveur ni contourner le contrôle par une opération locale directe

#### Scenario: Interruption ou version non qualifiée

- **WHEN** l'installation ou la mise à niveau est interrompue, incertaine ou porte une version non qualifiée pour la cible
- **THEN** l'état reste inspectable et non prêt jusqu'au rapprochement et aux validations nécessaires
- **AND** mise à niveau et reprise MUST préserver droits, révisions et résultats rapprochés, sans rejeu aveugle ni résurrection d'un état ou d'une autorité retirés
~~~~

### Référence courante deb-package-d49c71ea0d9a

Source : [deb-package](../../specs/deb-package/spec.md), ligne 135. SHA-256 : `d49c71ea0d9aa3a4315c7c8d2cf09b697013992a1b32ee51e1298f53a3095a46`.

Scénarios : Installation de paquet.

~~~~text
### Requirement: Composition Domaine et responsabilités des services

Les profils Debian Domaine MUST déclarer les capacités ZT et services LZT/KZT requis ainsi que logiciels, versions et exécutants qualifiés. La distribution PA/PZT MUST conserver trois binaires PA et PZT indépendant. Installation ou mise à jour par PA MUST rester distincte de la configuration/exploitation DNS/DHCP par DZT ; une dépendance présente MUST NOT être présentée comme service actif.

#### Scenario: Installation de paquet

- **WHEN** un paquet fournit les logiciels Domaine
- **THEN** la recette distingue contenu livré, rôles autorisés et services effectivement vérifiés.
~~~~

### Référence courante pixs-instance-b9b134df059f

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 11. SHA-256 : `b9b134df059f8bf6661d4623bae95e040e6f1461c35dd19d5d91ec4cd68c99bc`.

Scénarios : Ajout de PBO.

~~~~text
### Requirement: Identité logique et référentiel commun

L'Instance Pixs MUST posséder une identité stable distincte de ses PBO, processus, hôtes et ZT. Tous ses PBO MUST utiliser le même référentiel d'individus Core ; un nouveau PBO MUST NOT créer une liste concurrente d'individus.

#### Scenario: Ajout de PBO

- **WHEN** un second PBO est admis dans la même Instance
- **THEN** il référence les individus communs tout en conservant les données et responsabilités de ses modules.
~~~~

### Référence courante pixs-instance-18485b8d2051

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 20. SHA-256 : `18485b8d20510d544246b6d9c7efd51c9479aedb4fd4f839499c3e12bed5f82b`.

Scénarios : Transport pré-domaine; Mode ZT.

~~~~text
### Requirement: Modes Standalone ZT et Domaine

L'Instance MUST distinguer Standalone sans Domaine et avec une application PBO logique éventuellement redondée, ZT sans Domaine avec un ZT d'Instance, et Domaine avec un ou plusieurs Domaines utilisant ZT. Plusieurs PBO fonctionnellement distincts MAY exister en ZT et Domaine. Ces modes MUST rester distincts de Nuitka standalone et de l'activation du transport PZT.

#### Scenario: Transport pré-domaine

- **WHEN** Standalone utilise PZT pour joindre PA
- **THEN** le mode reste Standalone et les contrôles réseau et applicatifs restent nécessaires.

#### Scenario: Mode ZT

- **WHEN** ZT est initialisé sans création de Domaine
- **THEN** le référentiel des individus et les données pré-domaine restent au niveau Instance.
~~~~

### Référence courante pixs-instance-81a8ae9c0556

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 34. SHA-256 : `81a8ae9c0556560bcabef991ba7a8b2259c107021aadecec007049cbc2a8898f`.

Scénarios : ZT incomplet; Préconditions vérifiées.

~~~~text
### Requirement: ZT entièrement initialisé avant Domaine

La création du premier Domaine MUST exiger un mode ZT complètement initialisé, avec rôles essentiels opérationnels, identités, stockage et politiques vérifiés. Un état administratif créé ou un processus vivant MUST NOT suffire. La transition MUST être explicite et suivie durablement.

#### Scenario: ZT incomplet

- **WHEN** le rôle PKIZT essentiel manque lors de la demande du premier Domaine
- **THEN** la transition reste bloquée avec les capacités manquantes identifiées.

#### Scenario: Préconditions vérifiées

- **WHEN** le ZT et les autres préconditions de transition sont vérifiés
- **THEN** la procédure autorisée peut préparer puis activer le premier Domaine.
~~~~

### Référence courante pixs-instance-b189f9cd6424

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 48. SHA-256 : `b189f9cd6424f6b3127b840e6d069becb563c5a7942465fed2bd469482045888`.

Scénarios : Contrôleurs regroupés.

~~~~text
### Requirement: Minima et contrôleurs distincts

Chaque Instance MUST disposer d'au moins un PBO et un PA, déployés selon les environnements à administrer. Les contrôleurs d'Instance et de Domaine MUST être distingués du CZT. Leur regroupement ou séparation sur des PBO MUST être configurable sans fusion de bases ni habilitations.

#### Scenario: Contrôleurs regroupés

- **WHEN** un PBO assure les fonctions Instance et Domaine
- **THEN** les propriétaires des bases, identités et autorisations restent distincts.
~~~~

### Référence courante pixs-instance-9baefb0c5ae7

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 57. SHA-256 : `9baefb0c5ae783cb168944c78c34b6f7bc7814b244f9c8888e21389eef0e6e37`.

Scénarios : Activation du premier Domaine.

~~~~text
### Requirement: Références PG avant et après Domaine

Avant le premier Domaine, PG Instance MUST porter individus, identités numériques, organigrammes Core, groupes, ACL et données métier pré-domaine. Après activation, PG Instance MUST conserver les individus et données communes sans identité numérique d'Instance ; les identités et données reprises MUST appartenir à PG du premier Domaine, avec identifiants et relations préservés.

#### Scenario: Activation du premier Domaine

- **WHEN** le transfert pré-domaine est confirmé
- **THEN** l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.
~~~~

### Référence courante pixs-instance-ebdd233f14af

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 66. SHA-256 : `ebdd233f14afcc75b3a6a94757dd20a6eb5ec1c9e93b692f109025695c0b8e33`.

Scénarios : Interruption de transfert.

~~~~text
### Requirement: Maintenance des écritures pour la transition

La transition pré-domaine vers Domaine MUST planifier une maintenance des écritures, vérifier données, relations et authentification cible et traiter toute issue inconnue avant reprise. Elle MUST NOT déclarer la bascule réussie sur un accusé de réception ou un seul effet technique PA.

#### Scenario: Interruption de transfert

- **WHEN** le résultat du transfert ou de son engagement est inconnu
- **THEN** la procédure réconcilie les états propriétaires avant toute répétition ou reprise des écritures.
~~~~

### Référence courante pixs-instance-8c964dc84f92

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 75. SHA-256 : `8c964dc84f92c940b5c3ba094d124ffaeb003db84c0f5617cc9487e8d70c38e3`.

Scénarios : Domaine d’authentification non habilité.

~~~~text
### Requirement: Administration globale par identités habilitées

Après activation du premier Domaine, l'administration globale MUST utiliser des identités de Domaines explicitement habilitées. Plusieurs Domaines d'authentification MAY être autorisés. Une panne LDAP/Kerberos MAY être traitée par un profil PG Domaine explicitement autorisé et qualifié ; elle MUST NOT recréer d'identité numérique d'Instance ni réduire l'assurance exigée.

#### Scenario: Domaine d’authentification non habilité

- **WHEN** un utilisateur authentifié par un Domaine non habilité demande l’administration globale
- **THEN** la demande est refusée malgré la validité de son authentification.
~~~~

### Référence courante pixs-instance-c159a59d2125

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 84. SHA-256 : `c159a59d212509364156279d995f289887b68dc5fde0e1bc12244c0f317d5cfa`.

Scénarios : Ancienne sauvegarde.

~~~~text
### Requirement: Absence de retour Domaine Standalone V1

Après activation du premier Domaine, l'Instance MUST rester en mode Domaine en V1. Panne, restauration, retrait de domaine ou révocation MUST NOT provoquer un retour Standalone ou réactiver les anciennes identités. Les autres transitions inverses non spécifiées MUST NOT être introduites implicitement.

#### Scenario: Ancienne sauvegarde

- **WHEN** une reprise utilise des données antérieures à la transition
- **THEN** les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.
~~~~

### Référence courante pixs-instance-b7a2b5d23968

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 93. SHA-256 : `b7a2b5d2396839fee82af4ccc545e2c2c542dcbef6458888992a032fce8e929f`.

Scénarios : PBO mutualisé.

~~~~text
### Requirement: Habilitations Instance et domaines

Les habilitations globales Instance et celles de chaque Domaine MUST être séparées et vérifiées. Le partage d'un PBO, PA, stockage physique ou réseau MUST NOT les transmettre implicitement.

#### Scenario: PBO mutualisé

- **WHEN** un administrateur d’un Domaine utilise un PBO servant plusieurs Domaines
- **THEN** son action reste limitée aux périmètres explicitement autorisés.
~~~~

### Référence courante reference-composition-7131b276f78e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 10. SHA-256 : `7131b276f78ec528ebd8d3dc65dca30cc41d7a9b3f3ae193754cb02b3e8ea9e6`.

Scénarios : Garanties de qualification du parcours initial PA PZT; P0 sans exécution réseau; P0 sans réseau distant; Plan de ressources sans preuve sur cible.

~~~~text
### Requirement: Qualification du binaire commun et des profils de ressources P0

Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et ses ressources selon reference-runtime et runtime. Il MUST sélectionner et qualifier PA système/PZT local pour préparer PostgreSQL, sans activation déduite de la présence des modules ni confusion avec le réseau distant. La preuve MUST respecter les garanties détaillées du scénario ci-dessous.

#### Scenario: Garanties de qualification du parcours initial PA PZT

- **WHEN** le profil initial PBO et son parcours de préparation PostgreSQL sont évalués
- **THEN** Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et son plan de processus selon reference-runtime et runtime. La preuve MUST relier budgets accordés, configuration demandée, état appliqué, mesures et scénarios de panne. Les modules essentiels MUST rester composés et leur présence MUST NOT valoir activation. Le parcours initial de préparation PostgreSQL par PA MUST sélectionner explicitement les exécutants PA système et PZT local avec leurs profils propres à qualifier ; une absence de réseau distant MUST NOT être confondue avec l'absence de ce transport local obligatoire.

#### Scenario: P0 sans exécution réseau

- **WHEN** le profil initial conserve le réseau désactivé
- **THEN** les modules essentiels restent présents dans le binaire PBO et aucun exécutant PA/PZT ni résultat réseau n'est inventé
- **AND** l’absence de PZT local empêche de qualifier le parcours de préparation PostgreSQL par PA

#### Scenario: P0 sans réseau distant

- **WHEN** le profil initial sélectionne la préparation PostgreSQL par PA sans réseau distant
- **THEN** les modules essentiels et les exécutants PA système/PZT local nécessaires sont explicitement sélectionnés et qualifiés sans revendiquer de résultat de réseau distant

#### Scenario: Plan de ressources sans preuve sur cible

- **WHEN** une composition P0 possède un plan mais pas de recette sur l'environnement distribué
- **THEN** elle ne revendique pas un binaire ou un dimensionnement qualifié sur cette seule déclaration
~~~~

### Référence courante reference-composition-0af0b6011293

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 35. SHA-256 : `0af0b601129367e64eba64554f480dd9d5a1b93ee2348a0ba66ad4ac964e8671`.

Scénarios : Capacité P0 absente.

~~~~text
### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, `pixs.auth` essentiel avec son authentification locale autonome et PostgreSQL par défaut, le contexte tenant/scope, l'autorisation, les API et contrats publics, migrations, runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance, cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication
~~~~

### Référence courante reference-composition-986398c06367

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 44. SHA-256 : `986398c063671a966f8bc20f7e0d7706fe89595ff960a233fa8fbc266c49ad03`.

Scénarios : Synchronisation non sélectionnée.

~~~~text
### Requirement: Capacités hors P0 explicites

Toute capacité hors P0 MAY être ajoutée par sélection explicite. Son absence
MUST être déclarée ou représentée par un état compatible et MUST NOT affaiblir
les garanties du P0.

#### Scenario: Synchronisation non sélectionnée

- **WHEN** une composition P0 n'inclut aucun provider de synchronisation
- **THEN** elle reste valide sans annoncer de capacité réactive
~~~~

### Référence courante reference-composition-ab553efe6c54

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 55. SHA-256 : `ab553efe6c54a415ee9b8e42bbb9e9d009d3681dce99c2210ada04af4ef236b4`.

Scénarios : Deux validations identiques.

~~~~text
### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents
~~~~

### Référence courante reference-composition-5f1322f3cd28

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 66. SHA-256 : `5f1322f3cd28af91090d23c44e81cab453f1e264e606a48d7fbaa4ea3853d90e`.

Scénarios : Garanties du profil Debian local avec préparation PA; Architecture seulement observée.

~~~~text
### Requirement: Profil initial PBO PFO Debian local v1

Le profil pbo-p0-debian-local-v1 MUST identifier PBO/PFO, Debian 13 local, Django/TanStack et PostgreSQL distinct de PBO, préparé par PA système via PZT local. Il MUST déclarer et qualifier ses versions, architectures et exécutants selon le scénario ci-dessous ; un relevé de développement ou une preuve sans ces exécutants MUST NOT qualifier ce profil révisé.

#### Scenario: Garanties du profil Debian local avec préparation PA

- **WHEN** la première livraison du profil pbo-p0-debian-local-v1 est évaluée
- **THEN** La première livraison de profil `pbo-p0-debian-local-v1` MUST identifier PBO/PFO, Debian 13 local, Django, TanStack et PostgreSQL comme service distinct du processus PBO, préparé par le PA système de cet hôte via le parcours PA/PZT déclaré. Le profil MUST sélectionner les exécutants PA système et PZT local nécessaires à ce parcours ; une qualification historique sans ces exécutants MUST NOT prouver ce profil révisé. Elle MUST déclarer ses architectures et versions qualifiées avant distribution ; le relevé de développement MUST NOT tenir lieu de qualification.

#### Scenario: Architecture seulement observée

- **WHEN** une architecture apparaît dans l’environnement de développement sans recette correspondante
- **THEN** elle n’est pas annoncée comme supportée par le profil livré
~~~~

### Référence courante reference-composition-70063af8e7b7

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 80. SHA-256 : `70063af8e7b7f3ec61cbf3a60e111e20b60fcc09b6574df183ec392d1f1dce56`.

Scénarios : Module essentiel absent.

~~~~text
### Requirement: Garanties du socle conservées dans le profil initial

Le profil initial MUST satisfaire les capacités obligatoires P0 et composer les modules de gestion `pixs.agent` (PA hors PZT) et `pixs.pzt` (PZT), ainsi que le module DNS essentiel côté PBO. La désactivation réseau MUST NOT retirer ces modules ni affaiblir identité, périmètre, autorisation, audit, gouvernance ou reprise applicables.

#### Scenario: Module essentiel absent

- **WHEN** le réseau est désactivé mais `pixs.agent`, `pixs.pzt` ou le module DNS essentiel manque à la composition PBO
- **THEN** la qualification du profil échoue avant publication
~~~~

### Référence courante reference-composition-2614801b7609

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 89. SHA-256 : `2614801b7609ab3d7e337158b1a189846ac07b7308a13f21974f0e532efc17de`.

Scénarios : Démonstration mémoire seule.

~~~~text
### Requirement: Parcours installable et utilisable du profil initial

Le profil MUST permettre installation, première configuration, authentification, administration et opérations Core via contrats publics. Les rôles web, worker et scheduler MUST utiliser le même artefact et la persistance de référence ; une composition de test seule MUST NOT prouver ces parcours.

#### Scenario: Démonstration mémoire seule

- **WHEN** les seuls contrôles réussis utilisent des fixtures mémoire sans installation ni dépendance réelle
- **THEN** le profil ne revendique pas un parcours installable et utilisable qualifié
~~~~

### Référence courante reference-composition-ef9b2d25c156

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 98. SHA-256 : `ef9b2d25c1563c4766241a4a4b0e5df4f4188397774c38481e8c1f9e7bd395ab`.

Scénarios : Option absente sans dépendance obligatoire.

~~~~text
### Requirement: Capacités non sélectionnées du profil initial

Le profil MUST déclarer les capacités non sélectionnées et leurs limites sans annoncer leurs garanties. Une dépendance obligatoire d’une capacité sélectionnée MUST NOT être exclue sous prétexte d’option ; son absence bloque la qualification concernée.

#### Scenario: Option absente sans dépendance obligatoire

- **WHEN** aucun provider de synchronisation n’est sélectionné et aucune capacité retenue ne l’exige
- **THEN** son absence est déclarée sans annoncer de synchronisation ni affaiblir le P0
~~~~

### Référence courante reference-composition-7961b985d4cc

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 107. SHA-256 : `7961b985d4cc6e4533276d182585f4d018bce58499a8d3ce46b8b3ae71f2da57`.

Scénarios : Sources et paquet divergents.

~~~~text
### Requirement: Preuve de la composition effectivement distribuée

La preuve initiale MUST relier exigences applicables, scénarios exécutés, composants, versions et artefact installé. Elle MUST distinguer code présent, déclarations, dimensions non évaluées et verdicts observés, sans secret ni compatibilité globale supposée.

#### Scenario: Sources et paquet divergents

- **WHEN** la recette porte sur des sources différentes de celles du paquet proposé
- **THEN** elle ne suffit pas à qualifier la composition distribuée
~~~~

### Référence courante reference-composition-80e3d17e557d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 116. SHA-256 : `80e3d17e557db39ab0b1f163e3b9be60f18df6f7f0cdd4ef4555404d6256b8c9`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Choix C01 systemd et exception d’amorçage du profil Debian local

Le profil pbo-p0-debian-local-v1 MUST sélectionner le transport C01 LoadCredentialEncrypted systemd avec rotation par arrêt attesté et redémarrage contrôlé. Avant disponibilité de la base Pixs et du sink C05, il MUST déclarer explicitement l’exception limitée du journal fonctionnel local d’amorçage, ses politiques et son autorisation INSTALLER.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-b86766ab642e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 130. SHA-256 : `b86766ab642ec0550cf7661ba1d162a50901d633d9bb6948cc548c4cb0225c3e`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Qualification et source de vérité après amorçage

Cette exception MUST NOT devenir une source de vérité métier parallèle après reprise dans PostgreSQL. Les architectures, versions, capacités de stockage et politiques MUST être qualifiées avant distribution ; DEVOPS.md, un test isolé ou un reçu mémoire MUST NOT valoir qualification du paquet.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-fa2727180f3d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 144. SHA-256 : `fa2727180f3d824fbb7e3619a5b0196d02d52df210f1022887c5b3578875e857`.

Scénarios : Profil livré sans connecteurs externes; Profil Domaine.

~~~~text
### Requirement: Profil Auth standard sans connecteur externe installé

Le profil pré-domaine MUST sélectionner Auth local PG et garder les connecteurs externes absents sauf sélection explicite. Le mode Domaine MUST composer les capacités LZT/OpenLDAP et KZT/MIT Kerberos requises par Domaine ; IdP sortant et connecteurs externes MUST rester distincts et non activés implicitement. Présence de logiciel et service opérationnel MUST rester séparés.

#### Scenario: Profil livré sans connecteurs externes

- **WHEN** un profil Standalone standard est installé
- **THEN** Auth PG fonctionne selon sa politique sans service LDAP/KDC ou émission sortante implicite.

#### Scenario: Profil Domaine

- **WHEN** une composition revendique un Domaine opérationnel
- **THEN** ses LZT/KZT et son ZT admissible doivent être vérifiés, même si aucune source externe n’est installée.
~~~~

### Référence courante reference-composition-4f43b97aaed5

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 158. SHA-256 : `4f43b97aaed55b2b87629f7cc9dfae67e927a01213a4051882f1cc89c67f335e`.

Scénarios : PBO seul disponible.

~~~~text
### Requirement: Composition ZT initiale et Domaines

La qualification MUST distinguer PBO composé, PA/PZT disponibles, ZT entièrement initialisé et Domaine opérationnel. Les minima MUST suivre pixs-instance, pixs-domains et zt-instances ; un contrat pur ou artefact présent MUST NOT prouver ces états. Le premier PZT complet MUST cibler Debian/Linux et les autres profils MUST déclarer leurs rôles qualifiés.

#### Scenario: PBO seul disponible

- **WHEN** PBO est qualifié mais aucun exécutant CZT/DZT/PKIZT n’est admissible
- **THEN** la composition ne revendique pas ZT initialisé ni création de Domaine admissible.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| artifact-publication / 8 | [Canaux comme contextes de confiance distincts](../../specs/artifact-publication/spec.md#L8) | ND | Artefact du mauvais canal |
| artifact-publication / 17 | [Immuabilité et corrélation des corrections](../../specs/artifact-publication/spec.md#L17) | ND | Écrasement d'un artefact publié |
| artifact-publication / 26 | [Identité vérifiable avant installation](../../specs/artifact-publication/spec.md#L26) | ND | Emprunte discordante |
| artifact-publication / 35 | [Signature, provenance et inventaire bloquants](../../specs/artifact-publication/spec.md#L35) | ND | Signature révoquée |
| artifact-publication / 44 | [Autorités distinctes et gestion des clés](../../specs/artifact-publication/spec.md#L44) | ND | Dépôt de publication indisponible |
| deb-package / 8 | [Paquet corrélé à la release](../../specs/deb-package/spec.md#L8) | ND | Version de paquet incohérente ; Deux paquets indépendants |
| deb-package / 22 | [Configuration et secrets hors paquet](../../specs/deb-package/spec.md#L22) | ND | Secret trouvé dans le paquet |
| deb-package / 31 | [Services alignés sur le lifecycle Pixs](../../specs/deb-package/spec.md#L31) | ND | Redémarrage par le gestionnaire de services |
| deb-package / 40 | [Mise à niveau du paquet sous validation](../../specs/deb-package/spec.md#L40) | ND | Mise à niveau interrompue |
| deb-package / 49 | [Aucune installation de code distant implicite](../../specs/deb-package/spec.md#L49) | ND | Téléchargement proposé à l'installation |
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | Distribution Debian indépendante PA et PBO PFO |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | Quatre binaires dans le paquet PA |
| release-management / 8 | [Définition et support d'une release](../../specs/release-management/spec.md#L8) | ND | Release sans déclaration de support |
| release-management / 17 | [Chemin de migration vérifiable](../../specs/release-management/spec.md#L17) | ND | Saut non prouvé |
| release-management / 26 | [Mise à niveau orchestrée par prévalidations](../../specs/release-management/spec.md#L26) | ND | Étape de prévalidation échouée |
| release-management / 35 | [Coexistence transitoire N et N+1](../../specs/release-management/spec.md#L35) | ND | Contraction pendant la fenêtre |
| release-management / 44 | [Retour arrière soumis à la matrice](../../specs/release-management/spec.md#L44) | ND | Retour arrière non garanti |
| release-management / 55 | [Activation, retrait et instance non valide](../../specs/release-management/spec.md#L55) | ND | Instance échouant aux contrôles |

## Empreintes SHA-256 du canon

- `openspec/specs/artifact-publication/spec.md` : `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.
- `openspec/specs/deb-package/spec.md` : `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.
- `openspec/specs/release-management/spec.md` : `0fd7fc3720214df3741c8eed94e0db460b2fd67101cee3310c08b952672f6e3f`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.


## Référence BIND 9 adoptée le 24 octobre 2026

La sélection BIND 9 et sa distribution sont désormais normatives, selon
le [choix BIND 9 adopté](../adopt-bind9-managed-dns-and-packaging/proposal.md) et les exigences courantes suivantes :

- [Installation BIND 9 par le PA du rôle serveur DNS Debian](../../specs/deb-package/spec.md#L113).
- [Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs](../../specs/pzt/spec.md#requirement-fournisseur-bind-9-du-dns-géré-sur-debian-et-docker-pixs).

Le [raccord propre à ce lot](design.md#choix-bind-9-adopté-le-24-octobre-2026)
précise ses responsabilités et les qualifications futures. Ce complément
est une référence au canon adopté, sans copie normative concurrente. Les
relevés historiques ci-dessus conservent leur date ; leurs autres clauses,
lignes et preuves restent à réconcilier avant réalisation. Aucune coche
d'implémentation, installation, construction ou activation n'est ajoutée.
