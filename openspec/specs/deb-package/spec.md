# deb-package Specification

## Purpose
Le paquet Debian est un mode de livraison d'une release Pixs : il installe l'artefact et ses profils d'exécution sans jamais porter configuration sensible, données ou dérogations aux garanties de la release.

## Requirements

### Requirement: Installation des profils de processus configurables

Le paquet PBO/PFO MUST livrer le binaire PBO commun Nuitka standalone de reference-runtime et les ressources frontend. Les profils PBO et ceux du paquet indépendant PA/PZT MUST suivre runtime et rester configurables hors des artefacts. Les unités de supervision MUST appliquer rôles, instances et budgets déclarés sans installer un démon par module ni déduire un nombre de processus du serveur physique.

#### Scenario: Installation sur deux tailles d'hôte

- **WHEN** le même paquet est installé sur deux environnements aux budgets différents
- **THEN** le binaire reste identique pour la même cible de build et les configurations runtime adaptent les processus sans reconstruire une variante métier

#### Scenario: Paquet PA PZT autonome

- **WHEN** le paquet commun PA/PZT est installé sans PBO local
- **THEN** ses exécutants utilisent leurs profils de ressources propres et un PBO distant autorisé peut les gérer via les contrats existants

### Requirement: Paquet corrélé à la release

Chaque paquet MUST identifier sa release, son périmètre de composition, ses manifests, contrats, compatibilités et garanties. Il MUST rester corrélable aux autres artefacts de cette release pour les capacités communes. Cette corrélation MUST NOT imposer un contenu binaire identique entre le paquet commun PA/PZT, le paquet PBO/PFO et l’image sans fonctions de session ; les noms et versions exactes restent à spécifier.

#### Scenario: Version de paquet incohérente

- **WHEN** un paquet revendique une release différente de l’artefact qu’il installe
- **THEN** l’installation signale l’incohérence et bloque l’activation

#### Scenario: Deux paquets indépendants

- **WHEN** la composition Debian cible est vérifiée
- **THEN** le paquet commun PA/PZT et le paquet PBO/PFO restent distincts selon leurs exigences de composition

### Requirement: Configuration et secrets hors paquet

Le paquet MUST NOT embarquer de configuration effective, de référence de secret, de base de données, de volumes persistants ni de fichiers utilisateur ; l'installation MUST consommer une configuration validée et ne rien déduire de l'état accidentel du système de fichiers.

#### Scenario: Secret trouvé dans le paquet

- **WHEN** un artefact de paquet contient une valeur sensible réelle ou apparentée
- **THEN** la publication et l'installation sont refusées avec un diagnostic sans exposition de la valeur

### Requirement: Services alignés sur le lifecycle Pixs

Les unités de service installées MUST alimenter le même lifecycle, les mêmes contrôles de santé et les mêmes signaux d'arrêt que les autres modes de déploiement ; le gestionnaire de services reste un adapter sans autorité métier.

#### Scenario: Redémarrage par le gestionnaire de services

- **WHEN** le gestionnaire de services redémarre une unité
- **THEN** le profil concerné passe par les mêmes étapes de démarrage validé et de mise en service

### Requirement: Mise à niveau du paquet sous validation

Toute mise à niveau par paquet MUST être une opération explicite soumise à vérification d'identité de distribution, aux contrôles de compatibilité et au plan de migration ; un échec ou un abandon MUST laisser l'ancienne composition ou un état explicitement sûr, sans purge ni activation partielle non diagnostiquée.

#### Scenario: Mise à niveau interrompue

- **WHEN** une mise à niveau de paquet est interrompue après exécution partielle des migrations
- **THEN** le système reste dans un état diagnostiqué et seule une reprise validée ou une restauration autorisée poursuit l'opération

### Requirement: Aucune installation de code distant implicite

Le paquet MUST NOT, par défaut, télécharger, installer ou activer du code distant pendant l'installation ou l'exécution ; un mécanisme de mise à jour de sécurité peut automatiser le déclenchement sans supprimer les validations requises.

#### Scenario: Téléchargement proposé à l'installation

- **WHEN** une routine d'installation tente de récupérer une dépendance distante non vérifiée
- **THEN** l'installation est refusée sauf procédure explicite conforme aux garanties de publication

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

### Requirement: Trois binaires PA et PZT dans le paquet commun

Le paquet commun PA/PZT MUST livrer exactement quatre exécutables : trois
binaires PA définis par pixs-agent — démon système, événements de l'hôte,
sessions utilisateur — et le binaire indépendant PZT défini par pzt. Leurs six
modes PA et le mode PZT MUST conserver responsabilités, permissions et cycles
de vie distincts. La séparation MUST NOT ajouter un paquet ou un exécutable.

#### Scenario: Inspection du paquet commun

- **WHEN** le paquet PA/PZT est vérifié
- **THEN** les trois binaires PA et PZT indépendant sont identifiables, sans PBO/PFO embarqués

### Requirement: Première distribution PBO PFO du profil initial

La première distribution du profil initial MUST être un paquet PBO/PFO indépendant incluant les modules de gestion `pixs.agent` et `pixs.pzt` ainsi que le module DNS essentiel, sans exécutable PA ni PZT embarqué. Son identité expérimentale locale MUST respecter signature, provenance, inventaire, intégrité et révocation exigés par artifact-publication.

#### Scenario: Paquet expérimental non vérifiable

- **WHEN** le paquet initial est local ou expérimental mais son identité de distribution ne peut être vérifiée
- **THEN** il n’est pas installé ni publié comme release qualifiée

#### Scenario: Exécution réseau demandée après installation

- **WHEN** l’opérateur veut activer PZT après installation du paquet PBO/PFO seul
- **THEN** la composition exige un composant PZT admissible et les garanties du profil réseau sélectionné avant cette activation
