# Références et décision BIND 9

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pzt | Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs | 2 | pzt-00806e3fd967 |
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
| docker-image | Réplication des profils sous quotas du conteneur | 2 | docker-image-2ba58f2f253f |
| docker-image | Composition reproductible corrélée à la release | 2 | docker-image-276989d88d03 |
| docker-image | Image sans état ni secret | 1 | docker-image-cd1d3b742826 |
| docker-image | Configuration validée à l'exécution | 1 | docker-image-fe93183206ec |
| docker-image | Sondes alignées sur les états de santé | 1 | docker-image-83a4c263b381 |
| docker-image | Arrêt propre et orchestration sans autorité | 1 | docker-image-830a6195e1f2 |
| docker-image | Composition image PBO PFO deux binaires PA et PZT | 1 | docker-image-17e292fd2853 |
| docker-image | Événements PA limités au conteneur | 1 | docker-image-67e439783126 |
| docker-image | PostgreSQL fourni et initialisation PA du profil Docker Pixs | 3 | docker-image-a163e560260b |
| docker-image | Profil Docker initial déclaré et supervisé | 2 | docker-image-5ecbef2bfc17 |
| docker-image | Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite | 3 | docker-image-ceda1e465971 |
| docker-image | Profils Domaine et persistance des services | 1 | docker-image-a889a820ae60 |
| zt-dns-dhcp | DZT obligatoire et base commune indépendante | 1 | zt-dns-dhcp-a6e4d4b82a23 |
| zt-dns-dhcp | Préparation et mise à jour PA configuration PZT | 1 | zt-dns-dhcp-2b6ce945e38b |
| zt-dns-dhcp | Configuration entièrement régénérable | 1 | zt-dns-dhcp-7ead14a72e9a |
| zt-dns-dhcp | Vues dédiées et indépendantes | 1 | zt-dns-dhcp-b60b9b59341f |
| zt-dns-dhcp | Continuité par vue | 1 | zt-dns-dhcp-304243bad5c5 |
| zt-dns-dhcp | Domaine technique et noms stables | 1 | zt-dns-dhcp-bcef34966456 |
| zt-dns-dhcp | Activation DHCP indépendante et désactivée par défaut | 1 | zt-dns-dhcp-43c426b9d645 |
| zt-dns-dhcp | Adressage coordonné et propriétaire par pool | 1 | zt-dns-dhcp-a3fa9a562107 |
| zt-dns-dhcp | Liaison DHCP DNS configurable | 1 | zt-dns-dhcp-17080b1aed7c |
| zt-dns-dhcp | Zones administrables centralement ou par délégation | 1 | zt-dns-dhcp-596cccb2bb0f |
| zt-dns-dhcp | Projections DNS autorisées et bornées | 1 | zt-dns-dhcp-c422747ebce4 |
| zt-dns-dhcp | Notifications réconciliation et retransmission DNS | 1 | zt-dns-dhcp-c160bac67723 |

### Référence courante pzt-00806e3fd967

Source : [pzt](../../specs/pzt/spec.md), ligne 13031. SHA-256 : `00806e3fd96776a0f0e91507c07199ff28f015051f7860d578cfb4b1afeef100`.

Scénarios : Gestion PBO et exécutants séparés; Exécutant requis indisponible.

~~~~text
### Requirement: Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs

Sur Debian et Docker Pixs, BIND 9 fourni par Debian MUST être le fournisseur DNS. PBO/pixs.dns MUST administrer via contrats publics ; PA MUST préparer/installer, maintenir le système et mettre à jour les logiciels ; PZT/DZT MUST configurer et maintenir le fonctionnement logiciel selon zt-dns-dhcp. Cette sélection MUST NOT activer le rôle dans C14 ni rendre un PA client serveur. Les états logiciel présent, souhaité, appliqué et disponible MUST rester distincts.

#### Scenario: Gestion PBO et exécutants séparés

- **WHEN** un DZT BIND 9 est sélectionné et admis
- **THEN** PBO administre, PA prépare et DZT applique/vérifie sans écriture privée inter-modules.

#### Scenario: Exécutant requis indisponible

- **WHEN** une opération exige un PA ou DZT indisponible
- **THEN** elle reste bloquée ou d’issue inconnue selon les faits sans canal ou résultat fabriqué.
~~~~

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

### Référence courante docker-image-2ba58f2f253f

Source : [docker-image](../../specs/docker-image/spec.md), ligne 8. SHA-256 : `2ba58f2f253f0bea4c11827b5d2e1ad028bef5992ab59a67f014528f9c14688b`.

Scénarios : Plusieurs conteneurs web; Ressources de l'hôte non accordées.

~~~~text
### Requirement: Réplication des profils sous quotas du conteneur

L'image MUST livrer le binaire PBO commun Nuitka standalone avec ses ressources frontend et conserver les exécutants PA/PZT indépendants prévus. Chaque conteneur MUST sélectionner un rôle applicatif PBO explicite, avec processus et concurrence bornés selon runtime ; les réplicas et exécutants cohébergés MUST partager un budget contrôlé. La réplication MUST NOT cloner un propriétaire réseau ni une identité d'exécutant implicitement.

#### Scenario: Plusieurs conteneurs web

- **WHEN** plusieurs conteneurs lancent le rôle web depuis la même image
- **THEN** leurs budgets cumulés et connexions sont contrôlés, sans activation implicite des binaires PA/PZT présents dans l'image

#### Scenario: Ressources de l'hôte non accordées

- **WHEN** le serveur possède plus de CPU ou mémoire que le quota du conteneur
- **THEN** le dimensionnement respecte les limites accordées et les modes de session PA restent exclus
~~~~

### Référence courante docker-image-276989d88d03

Source : [docker-image](../../specs/docker-image/spec.md), ligne 22. SHA-256 : `276989d88d03cfe27f2b79a91dfbc453fb8e6f76b9f50d0a9d2ab63b0353d80d`.

Scénarios : Deux constructions d'une même release; Binaire utilisateur dans l’image.

~~~~text
### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des deux binaires PA système/événements et de PZT indépendant
~~~~

### Référence courante docker-image-cd1d3b742826

Source : [docker-image](../../specs/docker-image/spec.md), ligne 36. SHA-256 : `cd1d3b742826f68ef714ca9c17bbe9ce712addf2a91919998e568a264e9ab7e1`.

Scénarios : Valeur sensible dans l'image.

~~~~text
### Requirement: Image sans état ni secret

L'image MUST NOT contenir de secret, de token, de clé privée, de configuration effective ni de données persistantes ; toute persistance MUST rester hors de l'image via les stockages déclarés.

#### Scenario: Valeur sensible dans l'image

- **WHEN** une analyse détecte une valeur sensible dans une couche ou une métadonnée de l'image
- **THEN** la publication est refusée avec un diagnostic n'exposant pas la valeur
~~~~

### Référence courante docker-image-fe93183206ec

Source : [docker-image](../../specs/docker-image/spec.md), ligne 45. SHA-256 : `fe93183206ec0c04a71c04d61ebaa87e6ac3d79960a60d78f9889e915d777ef2`.

Scénarios : Démarrage avec configuration invalide.

~~~~text
### Requirement: Configuration validée à l'exécution

Le conteneur MUST recevoir sa configuration à l'exécution et la valider avant de passer à l'état de service ; il MUST NOT déduire fournisseur, tenant ou identité de l'état accidentel de l'image ou d'un système de fichiers éphémère.

#### Scenario: Démarrage avec configuration invalide

- **WHEN** un conteneur démarre avec une configuration incomplète ou invalide
- **THEN** il reste hors service avec une raison diagnostiquable au lieu de fonctionner dégradé silencieusement
~~~~

### Référence courante docker-image-83a4c263b381

Source : [docker-image](../../specs/docker-image/spec.md), ligne 54. SHA-256 : `83a4c263b381b1c4873df0b7b772d43620179c335155cc4d41b9de383e80c79a`.

Scénarios : Dépendance optionnelle indisponible.

~~~~text
### Requirement: Sondes alignées sur les états de santé

Les contrôles de santé du conteneur MUST être mappés sur les états distincts du socle et MUST NOT confondre vivacité et capacité à servir ; une dépendance optionnelle absente peut donner un état dégradé explicite, jamais une fausse disponibilité.

#### Scenario: Dépendance optionnelle indisponible

- **WHEN** une intégration optionnelle tombe dans un conteneur par ailleurs sain
- **THEN** la sonde d'exposition reflète l'état dégradé déclaré sans masquer une défaillance de sécurité
~~~~

### Référence courante docker-image-830a6195e1f2

Source : [docker-image](../../specs/docker-image/spec.md), ligne 63. SHA-256 : `830a6195e1f28088dcf6d3f11fbedbab68c465fcefdb6734e145eb1aecff3b69`.

Scénarios : Arrêt demandé pendant un traitement.

~~~~text
### Requirement: Arrêt propre et orchestration sans autorité

Le conteneur MUST gérer le signal d'arrêt par un drain contrôlé jusqu'à un état final explicite dans une durée bornée ; l'orchestrateur reste un adapter qui ne devient ni autorité métier ni substitut des validations de composition.

#### Scenario: Arrêt demandé pendant un traitement

- **WHEN** l'orchestrateur demande l'arrêt d'une instance en cours de traitement
- **THEN** l'instance draine selon son contrat et l'état persistant permet la reprise sans double effet
~~~~

### Référence courante docker-image-17e292fd2853

Source : [docker-image](../../specs/docker-image/spec.md), ligne 72. SHA-256 : `17e292fd285356a4b244611861a4a2b1f2022227b81b6679918b6f1fcfaa67f0`.

Scénarios : Inspection de l’image PA PZT.

~~~~text
### Requirement: Composition image PBO PFO deux binaires PA et PZT

L'image Pixs MUST toujours contenir le binaire PBO commun, les ressources PFO,
pixs.core, pixs.auth, pixs.agent, pixs.pzt, deux binaires PA — démon système et
événements du conteneur — et le
binaire indépendant PZT. Elle MUST NOT contenir le binaire utilisateur PA ni
ses modes session-start, session-stop et session-daemon. La séparation PA/PZT
MUST conserver trois exécutables hors PBO/PFO dans l'image.

#### Scenario: Inspection de l’image PA PZT

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO, pixs.agent, pixs.pzt, deux binaires PA et PZT sont présents et le binaire utilisateur PA est absent
~~~~

### Référence courante docker-image-67e439783126

Source : [docker-image](../../specs/docker-image/spec.md), ligne 86. SHA-256 : `67e439783126ef0a8a06f6fccd1b23f938cf3c990e477a02c907cfa37598baab`.

Scénarios : Événements PA limités au conteneur.

~~~~text
### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte
~~~~

### Référence courante docker-image-a163e560260b

Source : [docker-image](../../specs/docker-image/spec.md), ligne 95. SHA-256 : `a163e560260b3dde869579b04669ca5999b0aae00cdfcd9de3a09ae9700488dc`.

Scénarios : Garanties du profil Docker PostgreSQL; Premier démarrage Docker; Redémarrage et réplication Docker.

~~~~text
### Requirement: PostgreSQL fourni et initialisation PA du profil Docker Pixs

L’image Docker Pixs MUST fournir le logiciel PostgreSQL sans cluster, secret ou données effectives embarqués. Le profil MUST sélectionner explicitement PA système, PZT local et PostgreSQL avec stockage persistant hors image et hors couche éphémère. PA MUST initialiser seulement les ressources manquantes, conserver l’existant et respecter les garanties de supervision, reprise et réplication ci-dessous.

#### Scenario: Garanties du profil Docker PostgreSQL

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** L'image Docker Pixs MUST fournir le logiciel PostgreSQL, sans cluster préinitialisé, configuration effective ni données métier intégrés aux couches. Le profil d'exécution MUST sélectionner explicitement PA système, PZT local et le service PostgreSQL cohébergé, avec supervision, ordre de démarrage, arrêt contrôlé et budgets de ressources communs déclarés ; la simple présence des binaires MUST NOT les activer. Les données PostgreSQL MUST résider dans un stockage persistant déclaré hors de l'image et de la couche éphémère du conteneur. PA MUST vérifier l'état réel de ce stockage, initialiser uniquement ce qui manque, puis préparer et contrôler le service avant les opérations propriétaires PBO. Un stockage existant MUST être conservé et une incompatibilité MUST rester non prête sans effacement automatique. L'image, un redémarrage ou une réplication MUST NOT créer de nouveau propriétaire de base, cloner une identité PA/PZT ou réinitialiser le cluster. Les réplicas MUST déclarer leur cible de persistance et un propriétaire admissible unique pour la préparation. Tous échanges PBO–PA MUST rester via PZT ; les permissions du conteneur MUST NOT être étendues implicitement à l'hôte.

#### Scenario: Premier démarrage Docker

- **WHEN** un conteneur reçoit un stockage persistant vide et un profil PA/PZT/PostgreSQL explicitement admis
- **THEN** PA prépare le cluster avec le logiciel déjà fourni et PBO conserve seul ses migrations et initialisations applicatives ; aucun secret n’est ajouté à l’image

#### Scenario: Redémarrage et réplication Docker

- **WHEN** un conteneur redémarre ou un réplica cible une base déjà initialisée
- **THEN** le stockage et ses données sont conservés, les identités et le propriétaire de préparation restent distincts et aucun second cluster n’est créé implicitement
~~~~

### Référence courante docker-image-5ecbef2bfc17

Source : [docker-image](../../specs/docker-image/spec.md), ligne 114. SHA-256 : `5ecbef2bfc1708b352e1948e6893e37e754db62de5f12bd91097ae37e7bdf567`.

Scénarios : Démarrage du profil Docker déclaré; Arrêt des processus cohébergés.

~~~~text
### Requirement: Profil Docker initial déclaré et supervisé

Le profil Docker initial C08 MUST respecter l’intégralité du contrat normatif du scénario « Démarrage du profil Docker déclaré » pour toute construction, préparation, exécution et tout arrêt du profil. Les garanties de processus, supervision, stockage, ressources et droits y sont indissociables ; leur déclaration MUST NOT constituer une qualification.

#### Scenario: Démarrage du profil Docker déclaré

- **WHEN** le profil initial est demandé avec son artefact, sa configuration et son stockage déclarés
- **THEN** PZT et PA sont admis sous leurs contrôles, PA prépare seulement les ressources PostgreSQL manquantes et PBO conserve ses migrations et initialisations
- **AND** aucun entrypoint hérité ni volume anonyme accidentel n’autorise une initialisation ou une disponibilité
- **AND** Le profil Docker initial C08 MUST déclarer Debian 13 Linux amd64, la base Docker Official Image postgres:16.15-trixie verrouillée par digest avant construction, le paquet Supervisor 4.2.5-3 et ses dépendances système verrouillées, l’init Docker et la supervision au premier plan. Il MUST traiter explicitement ENTRYPOINT, CMD, STOPSIGNAL et VOLUME hérités, sans initialisation automatique PostgreSQL. Il MUST sélectionner un rôle applicatif PBO, les exécutants PA système/événements et PZT indépendant et un service PostgreSQL distinct, sous un plan de ressources et un stockage persistant déclarés. Le lifecycle MUST contrôler ordre, readiness, comptes, signaux et drain ; PostgreSQL MUST attendre sa préparation autorisée par PA. Le profil MUST NOT ajouter implicitement privilège, socket Docker, namespace hôte ou montage de cgroups. Les droits de l’hôte et les données persistantes MUST rester préservés ; une métadonnée d’image ou une dépendance installée MUST NOT valoir qualification.

#### Scenario: Arrêt des processus cohébergés

- **WHEN** le conteneur reçoit son signal d’arrêt déclaré
- **THEN** le lifecycle draine PBO avant fermeture PostgreSQL et conserve PA/PZT jusqu’aux étapes qui les requièrent, dans les bornes accordées
- **AND** une étape inconnue ou interrompue reste non prête et inspectable sans perte silencieuse ni réinitialisation du stockage
~~~~

### Référence courante docker-image-ceda1e465971

Source : [docker-image](../../specs/docker-image/spec.md), ligne 131. SHA-256 : `ceda1e465971ab5e0784c8cc3811f171070311b193543d0f868da0e5d48a2d1c`.

Scénarios : Image fournie avec service non sélectionné; État et secrets hors des couches; Activation ultérieure contrôlée.

~~~~text
### Requirement: Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite

L'image Docker Pixs MUST fournir BIND 9 issu de Debian et ses dépendances identifiées. Cette présence MUST NOT activer le serveur sans application et supervision autorisées par le PA désigné. Version et image MUST être corrélées à la release et aux preuves de qualification. Les couches MUST NOT contenir de secret, clé privée ou état DNS propre à une instance.

#### Scenario: Image fournie avec service non sélectionné

- **WHEN** une image Pixs contenant BIND 9 est construite ou démarrée sans rôle serveur DNS sélectionné et admis
- **THEN** la présence du logiciel est vérifiable sans lancement ou disponibilité DNS implicites
- **AND** le choix BIND 9 MUST NOT autoriser implicitement un port, montage, utilisateur ou privilège supplémentaire

#### Scenario: État et secrets hors des couches

- **WHEN** la composition de l'image et les effets de l'installation du paquet sont contrôlés
- **THEN** aucune couche ne contient de clé privée, secret ou état DNS d'instance
- **AND** l'effacement dans une couche ultérieure n'est pas assimilé à l'absence de la donnée dans l'image

#### Scenario: Activation ultérieure contrôlée

- **WHEN** le rôle serveur DNS est ultérieurement sélectionné et admis dans le conteneur
- **THEN** le PA désigné applique et supervise le processus BIND 9 distinct avec les configurations et ressources effectivement autorisées
- **AND** configuration d'instance, données persistantes et références de secrets MUST suivre les plans et propriétaires du profil
- **AND** seul un résultat réel vérifié permet de déclarer état appliqué ou disponibilité
~~~~

### Référence courante docker-image-a889a820ae60

Source : [docker-image](../../specs/docker-image/spec.md), ligne 154. SHA-256 : `a889a820ae600423c7b5f29e9f38b3d84c48fc37ad2f9e536cbb04706c3cc7b2`.

Scénarios : Rôles répartis.

~~~~text
### Requirement: Profils Domaine et persistance des services

Un profil Docker Domaine MUST déclarer ses services PG propriétaires, LDAP/Kerberos et ZT, comptes, dépendances et persistances sans montage ni privilège implicite. L'image MUST conserver deux binaires PA système/événements et PZT, sans sessions PA utilisateur. Les minima requis MUST être vérifiés sur la composition effective et MUST NOT imposer tous les rôles dans chaque conteneur.

#### Scenario: Rôles répartis

- **WHEN** un Domaine répartit ses rôles sur plusieurs conteneurs autorisés
- **THEN** chaque profil conserve son périmètre et ses stockages sans duplication d’identité ni attribution de droit hôte implicite.
~~~~

### Référence courante zt-dns-dhcp-a6e4d4b82a23

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 11. SHA-256 : `a6e4d4b82a23d0d4194faa5e5bc977d55dd4e10d2015293d1cdb5dad391f56d3`.

Scénarios : Plusieurs DZT.

~~~~text
### Requirement: DZT obligatoire et base commune indépendante

Chaque ZT MUST disposer d'au moins un DZT exécuté par PZT. BIND 9 MUST fournir DNS v4/v6 et ISC DHCP MUST fournir DHCPv4 et DHCPv6 par processus distincts. Une PG DZT MUST conserver la référence commune à ces fonctions, indépendante de CZT, PKIZT et PBO, avec réplication synchrone et primaire unique selon zt-controller et brick-redundancy.

#### Scenario: Plusieurs DZT

- **WHEN** une réplique DZT est ajoutée
- **THEN** elle rejoint le même référentiel logique sans source de configuration concurrente.
~~~~

### Référence courante zt-dns-dhcp-2b6ce945e38b

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 20. SHA-256 : `2b6ce945e38b1456b0c994124e8b62d091fd1a2c036cf2d5bfd22940c5cff008`.

Scénarios : Mise à jour BIND.

~~~~text
### Requirement: Préparation et mise à jour PA configuration PZT

PA MUST assurer préparation, installation, maintenance système et mise à jour des logiciels DNS/DHCP. PZT/DZT MUST assurer configuration et maintenance logicielle du fonctionnement, validation, application et contrôle des services. PBO MUST administrer séparément les périmètres. Ces interventions MUST être coordonnées et leurs résultats distingués.

#### Scenario: Mise à jour BIND

- **WHEN** PA termine une mise à jour autorisée
- **THEN** DZT revalide la compatibilité, réapplique si nécessaire la configuration et vérifie le fonctionnement avant succès du service.
~~~~

### Référence courante zt-dns-dhcp-7ead14a72e9a

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 29. SHA-256 : `7ead14a72e9af3424f562f2087ddbb48654a73f7b60db2fd1fadd8dc6fde5968`.

Scénarios : Régénération après panne.

~~~~text
### Requirement: Configuration entièrement régénérable

DZT MUST produire et pouvoir rejouer intégralement les configurations depuis une révision cohérente de sa PG, sans traiter les modifications manuelles des fichiers comme vérité. Baux, mises à jour dynamiques, journaux nécessaires et clés DNSSEC MUST être préservés par des contrats de durabilité/reprise explicites.

#### Scenario: Régénération après panne

- **WHEN** les fichiers générés sont reconstruits
- **THEN** l’état natif durable n’est ni effacé ni supposé recréé par la configuration seule.
~~~~

### Référence courante zt-dns-dhcp-b60b9b59341f

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 38. SHA-256 : `b60b9b59341f4623766d298140c48c097c9732d00f3ff93bef2fbf90546ff258`.

Scénarios : Vue externe au ZT.

~~~~text
### Requirement: Vues dédiées et indépendantes

BIND MUST permettre au moins une vue dédiée au ZT, plusieurs vues ZT et des vues hors ZT administrées séparément par PBO. Plusieurs DZT MAY être actifs et servir une même vue pour la redondance ; les droits, zones, visibilité et délégations MUST rester propres au périmètre.

#### Scenario: Vue externe au ZT

- **WHEN** une vue hors ZT partage un BIND avec les vues ZT
- **THEN** elle conserve ses politiques et ne devient pas accessible aux acteurs ZT par cohébergement.
~~~~

### Référence courante zt-dns-dhcp-304243bad5c5

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 47. SHA-256 : `304243bad5c5998ac7e7da0895267f27dc586e5d2ab72f19fa26a2042e8be6ca`.

Scénarios : Contrôle indisponible.

~~~~text
### Requirement: Continuité par vue

Chaque vue MUST déclarer ses conditions et limites de continuité/fraîcheur. Les données déjà appliquées MAY être servies dans ces limites ; une expiration MUST arrêter le service concerné, sans nouvelle modification ou validité déduite de l'indisponibilité. Les autres vues encore admissibles MUST rester indépendantes.

#### Scenario: Contrôle indisponible

- **WHEN** la validité d’une vue expire tandis qu’une autre reste admissible
- **THEN** la première cesse d’être servie sans arrêt injustifié de la seconde.
~~~~

### Référence courante zt-dns-dhcp-bcef34966456

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 56. SHA-256 : `bcef34966456039806ec43fc1d8821085990ddc5bee030a1c13d3df80dc02be5`.

Scénarios : Alias renommé.

~~~~text
### Requirement: Domaine technique et noms stables

Chaque ZT MUST déclarer à l'initialisation au moins un domaine DNS dédié. Les cibles MUST avoir des noms techniques stables et MAY posséder des alias lisibles administrés depuis PBO. Un changement d'adresse ou d'alias MUST NOT changer l'identité canonique. Le partage avec les Domaines MUST respecter pixs-domains.

#### Scenario: Alias renommé

- **WHEN** un alias lisible est modifié
- **THEN** la cible conserve son identité et les politiques vérifient toujours la destination attendue.
~~~~

### Référence courante zt-dns-dhcp-43c426b9d645

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 65. SHA-256 : `43c426b9d6456cb755fb4972337fd0e477a48d4d20272893874aad0ed48c3f5b`.

Scénarios : DZT initialisé.

~~~~text
### Requirement: Activation DHCP indépendante et désactivée par défaut

DHCPv4 et DHCPv6 MUST être désactivés par défaut et activés explicitement, indépendamment par réseau, depuis PBO. La présence obligatoire du DZT MUST NOT démarrer l'attribution DHCP sur un réseau non autorisé.

#### Scenario: DZT initialisé

- **WHEN** un DZT est initialisé sans réseau DHCP activé
- **THEN** aucun bail DHCPv4 ou DHCPv6 n’est attribué.
~~~~

### Référence courante zt-dns-dhcp-a3fa9a562107

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 74. SHA-256 : `a3fa9a56210702924906d9035b25f98c9f643efb265199f0158abe66ec74dd1f`.

Scénarios : Reprise sans baux fiables.

~~~~text
### Requirement: Adressage coordonné et propriétaire par pool

CZT MUST gérer l'adressage des pairs PZT ; DZT MUST gérer les réseaux DHCP avec coordination des préfixes/pools. Un pool MUST avoir un seul DZT autorisé à attribuer ou renouveler ses baux à un instant donné ; les pools MAY être répartis. La reprise MUST vérifier les baux et exclure l'ancien propriétaire.

#### Scenario: Reprise sans baux fiables

- **WHEN** un secours ne peut vérifier l’état des baux du pool
- **THEN** il ne devient pas allocateur actif sur la seule panne de l’ancien DZT.
~~~~

### Référence courante zt-dns-dhcp-17080b1aed7c

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 83. SHA-256 : `17080b1aed7cd6b13ddd795989aa792216bef304a46a3306be0f2b2a1db8ded7`.

Scénarios : Publication échouée.

~~~~text
### Requirement: Liaison DHCP DNS configurable

Le lien DHCP–DNS MUST pouvoir être automatique et configurable par périmètre. Le bail et son état de publication DNS MUST être suivis séparément, avec idempotence, retrait et reprise selon leurs politiques ; la réussite de l'un MUST NOT prouver celle de l'autre.

#### Scenario: Publication échouée

- **WHEN** un bail est accordé mais sa publication DNS échoue
- **THEN** les deux états sont visibles et la reprise ne réattribue pas aveuglément le bail.
~~~~

### Référence courante zt-dns-dhcp-596cccb2bb0f

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 92. SHA-256 : `596cccb2bb0f6d7ad183c264030375e09bba365b7ae51645af90b14caea83eb0`.

Scénarios : Délégué de zone.

~~~~text
### Requirement: Zones administrables centralement ou par délégation

Dans un ZT partagé, les zones MUST pouvoir être administrées centralement ou déléguées selon des habilitations explicites. Une délégation MUST préciser ses zones et actions et MUST NOT autoriser une modification des zones des autres Domaines.

#### Scenario: Délégué de zone

- **WHEN** un administrateur d’association.pixs.fr tente de modifier recherche.pixs.fr
- **THEN** la modification est refusée sans délégation correspondante.
~~~~

### Référence courante zt-dns-dhcp-c422747ebce4

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 101. SHA-256 : `c422747ebce42bcdd5d967f4e38db9aa5c60a4f1b1a7a1c552043c1471f74301`.

Scénarios : Projection expirée.

~~~~text
### Requirement: Projections DNS autorisées et bornées

La résolution entre ZT approuvés MUST exiger une permission DNS précisant bénéficiaires, noms/zones et sens. Le destinataire MUST conserver une projection séparée, versionnée, liée à son origine et à une échéance renouvelable seulement par autorisation de l'origine. TTL MUST être bornés par cette échéance et révocations connues MUST être appliquées.

#### Scenario: Projection expirée

- **WHEN** le propriétaire reste injoignable après échéance de sa projection
- **THEN** DZT cesse de servir ces données sans prolongation par cache ou TTL.
~~~~

### Référence courante zt-dns-dhcp-c160bac67723

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 110. SHA-256 : `c160bac677235ccdc0558d9bbd496d164db2007eb4d931c36d8c757d8a468fc1`.

Scénarios : Projection retransmise.

~~~~text
### Requirement: Notifications réconciliation et retransmission DNS

La synchronisation MUST utiliser notifications, réconciliation et contrôle périodique complémentaire, avec état complet si une révision manque. La retransmission MAY être autorisée explicitement si toute la chaîne conserve origine, portée, restrictions, profondeur et échéances. Une notification MUST NOT suffire à prouver mise à jour ou renouvellement.

#### Scenario: Projection retransmise

- **WHEN** un intermédiaire est habilité à retransmettre un sous-ensemble
- **THEN** il préserve l’origine et ne prolonge aucune limite du propriétaire.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Source de la décision

Le développeur a retenu BIND 9 fourni par Debian, installé et configuré par PA,
avec présence dans Docker Pixs. Il a confirmé « Choix BIND 9 et packaging ;
activation ultérieure », puis demandé un dossier OpenSpec distinct. Aucun
numéro de version, topologie, port ou droit d'infrastructure n'est ajouté
par interprétation.

Le 24 octobre 2026, le développeur a validé la spécification présentée et
autorisé l'ouverture de ce change sans implémentation ni production de code.
Cet accord confirme les trois exigences et neuf scénarios du dossier ;
il ne lance aucune réalisation ni activation. La synchronisation a ensuite été
explicitement autorisée le même jour avec les renvois Z05/Debian/Docker,
toujours sans implémentation ni production de code.

## Références normatives existantes

| Source | Obligations conservées | SHA-256 du relevé |
|---|---|---|
| [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md) | A06c–A06k : gestion essentielle, exécution PA distincte, DoT, cache/TTL, vues, suffixe et absence de repli | 6a666454ee45da31cdd1c61e1bf4d9d1383311b3cea19c01b028f340bc1e1349 |
| [openspec/specs/deb-package/spec.md](../../specs/deb-package/spec.md) | Paquets, versions, données/secrets hors paquet, lifecycle et distribution PA/PBO séparée | 0451c3c94bf4c99e30578780dc2f4ac2c3b6367b9d4d3da493a12dc9f56874a3 |
| [openspec/specs/docker-image/spec.md](../../specs/docker-image/spec.md) | Image sans état/secret, activation et supervision selon le profil, processus PA/PZT présents | 4267e07ceeaea6a456d8a04a0af35cbf78c2df68c799221cc1d1cc0c47aa4c9b |

Les empreintes du tableau désignent le canon après synchronisation BIND 9
du 24 octobre 2026 ; elles ne qualifient pas le logiciel. Toute nouvelle
dérive impose relecture des clauses affectées.
Les deltas ajoutent trois exigences et neuf scénarios : un choix logiciel
et deux règles de distribution. Ils ne réécrivent pas les contrats détaillés
A06c–A06k ni leur exception Super Admin applicative.

### Recoupement à l'ouverture du 24 octobre 2026

Les trois canons et les quinze liens internes ont été contrôlés à nouveau.
Les empreintes deb-package et docker-image sont inchangées. Le canon PZT
ajoute le profil X.509 des terminaux initiaux Z12 et la résolution locale
du matériel TLS sous propriétaire courant. Son préfixe antérieur est
reconstitué octet pour octet et retrouve l'empreinte
652aeb4b9ab911bbafb7b3f9f3c7ad582b5bed8af5a806ce9925579caaf7aba5.
Les clauses DNS A06c–A06k sont donc conservées ; aucune émission de certificat,
résolution de matériel TLS ou autorité initiale n'est ajoutée par BIND 9.
Ce recoupement décrit le relevé d'ouverture, antérieur à l'ajout des trois
exigences BIND 9 ; le tableau ci-dessus est actualisé après synchronisation.

## Répartition des preuves

| Objet | Propriétaire / dossier | Ce que ce dossier ne prouve pas |
|---|---|---|
| Gestion souhaitée et contrats | [C14](../archive/2026-10-23-add-essential-pbo-pzt-and-dns-modules/proposal.md) | BIND installé ou service actif |
| Exécution DNS et adapters PA | [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md) | Transport, DoT, vues ou états appliqués qualifiés |
| Instruction autorisée | [PA01](../add-pa-authorized-instruction-execution/proposal.md) | Mandat/exécutant disponibles par leur seule documentation |
| Gestion Agent | [PA10](../separate-pa-pzt-and-pbo-management-modules/proposal.md) | Garantie d'un exécutant ou canal PZT réel |
| Image | [Docker Pixs](../build-and-qualify-pixs-docker-image/proposal.md) | Artefact construit, état/secret absent de toutes les couches |

Aucune absence de dépendance, non-sélection ou fixture n'est marquée PASS.
Le canon est synchronisé pour les trois exigences BIND 9 validées. Les cadrages
communs et les archives existantes sont conservés ; aucune archive nouvelle
ni réalisation n'est produite par cette adoption documentaire.


## Correspondance exacte entre les deltas validés et le canon synchronisé

| Capacité | Exigence canonique | Scénarios intégrés |
|---|---|---|
| pzt | [Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs](../../specs/pzt/spec.md#requirement-fournisseur-bind-9-du-dns-géré-sur-debian-et-docker-pixs) | 3 |
| deb-package | [Installation BIND 9 par le PA du rôle serveur DNS Debian](../../specs/deb-package/spec.md#L113) | 3 |
| docker-image | [Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite](../../specs/docker-image/spec.md#L131) | 3 |


Les trois blocs sont copiés intégralement depuis les deltas validés, sans
modifier les clauses canoniques préexistantes. Les deltas sont conservés
comme provenance de la décision ; aucune seconde application ni archive
n'est engagée. Les renvois de conception et d'exigences de Z05, C18, PA09
et X01 sont raccordés à ces exigences, sans cocher leurs tâches produit.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
