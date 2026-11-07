# Références normatives — PA09

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
| pixs-agent | Trois binaires PA et six modes distincts de PZT | 1 | pixs-agent-5cd5cae10cd4 |
| pixs-agent | Indépendance d'installation et autorité applicative | 1 | pixs-agent-11bc72405973 |
| pixs-agent | Publications locales expérimentales et sécurité de distribution | 1 | pixs-agent-7ee8f12438a7 |
| pixs-agent | Périmètre système et utilisateur complet | 1 | pixs-agent-720e16859540 |

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

### Référence courante pixs-agent-5cd5cae10cd4

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 64. SHA-256 : `5cd5cae10cd478a8ffb30c4e15180dfdc341506019583f78882f62ec99106408`.

Scénarios : Répartition PA et PZT.

~~~~text
### Requirement: Trois binaires PA et six modes distincts de PZT

PA MUST comporter exactement trois binaires : démon système pour system-daemon ;
événements système pour system-start et system-stop ; sessions utilisateur pour
session-start, session-stop et session-daemon. PZT et son mode pzt-daemon MUST
rester un composant exécutable indépendant, colivré selon deb-package et
docker-image. Le démon de session MUST NOT créer un binaire supplémentaire.
Les chemins et options CLI restent à spécifier.

#### Scenario: Répartition PA et PZT

- **WHEN** la composition complète PA/PZT est décrite
- **THEN** elle distingue trois binaires et six modes PA du binaire indépendant PZT et de son mode pzt-daemon
~~~~

### Référence courante pixs-agent-11bc72405973

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 99. SHA-256 : `11bc724059737a471a2b86bbc1006b05c8107ae72698caab16094add8b31b1ca`.

Scénarios : Indépendance d'installation et autorité applicative.

~~~~text
### Requirement: Indépendance d'installation et autorité applicative

Les binaires PA MUST pouvoir être installés sans PBO, PFO ou navigateur locaux et joindre un PBO distant autorisé. PA MUST NOT embarquer Django/PostgreSQL comme autorité métier, accéder directement aux tables métier ni confirmer une mutation de sa propre initiative. PBO/Django MUST conserver les décisions applicatives et PostgreSQL leur persistance de référence.

#### Scenario: Indépendance d'installation et autorité applicative

- **WHEN** PA est installé seul sur une cible
- **THEN** ses opérations restent liées à leurs mandats et à l'autorité PBO compétente
~~~~

### Référence courante pixs-agent-7ee8f12438a7

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 287. SHA-256 : `7ee8f12438a73c715d27284fe7be338ea634057f8ba35c34b3d7a5416867cfa2`.

Scénarios : Publications locales expérimentales et sécurité de distribution.

~~~~text
### Requirement: Publications locales expérimentales et sécurité de distribution

La première livraison envisagée MUST rester locale sur canal expérimental, avec capacités, versions, limites et preuves déclarées. Elle MUST satisfaire artifact-publication, notamment signature, provenance, inventaire, intégrité, immuabilité et révocation ; locale ou expérimentale MUST NOT dispenser de ces garanties ni autoriser une clé secrète dans un artefact. La présente formalisation MUST NOT construire, signer ou publier un artefact.

#### Scenario: Publications locales expérimentales et sécurité de distribution

- **WHEN** un artefact local expérimental ne dispose pas d'une signature admissible
- **THEN** il ne peut pas être déclaré publiable ou installable conformément à artifact-publication
~~~~

### Référence courante pixs-agent-720e16859540

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 1309. SHA-256 : `720e1685954099752b0bc6df1578dd0da9cd52a959f0bf160d9a34d6ad37b60d`.

Scénarios : Fonction de session.

~~~~text
### Requirement: Périmètre système et utilisateur complet

PA MUST conserver trois binaires et six modes pour fonctionnement, paramétrage, contrôle, collecte, surveillance et dérives dans les contextes système et utilisateur. Les modules MUST solliciter le catalogue livré via pixs.agent en conservant leur métier. Les rôles LZT/KZT et opérations de managed-device-policies MUST suivre ces frontières sans transférer à PA l'autorité applicative.

#### Scenario: Fonction de session

- **WHEN** une opération autorisée s’exécute dans une session graphique
- **THEN** elle utilise ses droits et états isolés sans recevoir de privilèges système implicites.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | COMPLETER_OU_INTEGRER |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | COMPLETER_OU_INTEGRER |
| pixs-agent / 11 | [Quatre binaires et sept modes explicitement répartis](../../specs/pixs-agent/spec.md#L11) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 38 | [Indépendance d'installation et autorité applicative](../../specs/pixs-agent/spec.md#L38) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 209 | [Publications locales expérimentales et sécurité de distribution](../../specs/pixs-agent/spec.md#L209) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence deb-package--9112fb78b5

Source : `openspec/specs/deb-package/spec.md`, ligne 58. SHA-256 du bloc : `093f3bb6a9b35ad099decdd39ded1a7a9654a93e094cf52a59d6d33d3c3bb2c3`.

~~~~text
### Requirement: Distribution Debian indépendante PA et PBO PFO

La distribution Debian MUST comporter un paquet PBO/PFO et un paquet PA indépendant. Le paquet PBO/PFO MUST contenir le module essentiel PZT et MUST NOT embarquer les quatre binaires PA. L’installation PA seule MUST NOT requérir PBO/PFO locaux comme contenu embarqué ; les compatibilités et dépendances d’installation restent déclarées.

#### Scenario: Distribution Debian indépendante PA et PBO PFO

- **WHEN** PA est installé seul
- **THEN** son paquet reste indépendant et peut joindre un PBO distant autorisé
~~~~

### Référence deb-package--477adcdbb1

Source : `openspec/specs/deb-package/spec.md`, ligne 67. SHA-256 du bloc : `e049d00b76c48e5d87aed01ad83927a13fa52686eb940213167e99ad4936f6c4`.

~~~~text
### Requirement: Quatre binaires dans le paquet PA

Le paquet PA MUST livrer exactement les quatre exécutables définis par pixs-agent : démon système, événements de démarrage/arrêt de l’hôte, sessions utilisateur et exécution PZT. Il MUST conserver la séparation des modes et permissions ; noms/chemins et versions restent à spécifier.

#### Scenario: Quatre binaires dans le paquet PA

- **WHEN** le paquet PA est vérifié
- **THEN** les quatre binaires et leurs responsabilités sont identifiables sans PBO/PFO embarqués
~~~~

### Référence pixs-agent--24f2ceb983

Source : `openspec/specs/pixs-agent/spec.md`, ligne 11. SHA-256 du bloc : `7d77582c9257ea14c361d203416f60c56bc861c3552acc98a217d029ad22e615`.

~~~~text
### Requirement: Quatre binaires et sept modes explicitement répartis

PA MUST comporter exactement quatre binaires dédiés : démon système pour system-daemon ; événements système pour system-start et system-stop ; sessions utilisateur pour session-start, session-stop et session-daemon ; exécution PZT pour pzt-daemon. Les noms d'exécutables, chemins et options CLI restent à spécifier. Le découpage MUST NOT créer un cinquième binaire pour le démon de session.

#### Scenario: Quatre binaires et sept modes explicitement répartis

- **WHEN** une distribution PA complète décrit ses exécutables
- **THEN** elle identifie les quatre responsabilités et les sept modes sans les confondre
~~~~

### Référence pixs-agent--5c3c0eb52d

Source : `openspec/specs/pixs-agent/spec.md`, ligne 38. SHA-256 du bloc : `db38cd6d3d6d07cd9b02dc070c47ce83fa1ac4262c41dbefc28ef736d48ebac0`.

~~~~text
### Requirement: Indépendance d'installation et autorité applicative

Les binaires PA MUST pouvoir être installés sans PBO, PFO ou navigateur locaux et joindre un PBO distant autorisé. PA MUST NOT embarquer Django/PostgreSQL comme autorité métier, accéder directement aux tables métier ni confirmer une mutation de sa propre initiative. PBO/Django MUST conserver les décisions applicatives et PostgreSQL leur persistance de référence.

#### Scenario: Indépendance d'installation et autorité applicative

- **WHEN** PA est installé seul sur une cible
- **THEN** ses opérations restent liées à leurs mandats et à l'autorité PBO compétente
~~~~

### Référence pixs-agent--2706087935

Source : `openspec/specs/pixs-agent/spec.md`, ligne 209. SHA-256 du bloc : `0375ec260b62cb401a7dbb81be02385cb44193a19105a6bfb3c72b0bfd628d35`.

~~~~text
### Requirement: Publications locales expérimentales et sécurité de distribution

La première livraison envisagée MUST rester locale sur canal expérimental, avec capacités, versions, limites et preuves déclarées. Elle MUST satisfaire artifact-publication, notamment signature, provenance, inventaire, intégrité, immuabilité et révocation ; locale ou expérimentale MUST NOT dispenser de ces garanties ni autoriser une clé secrète dans un artefact. La présente formalisation MUST NOT construire, signer ou publier un artefact.

#### Scenario: Publications locales expérimentales et sécurité de distribution

- **WHEN** un artefact local expérimental ne dispose pas d'une signature admissible
- **THEN** il ne peut pas être déclaré publiable ou installable conformément à artifact-publication
~~~~



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
