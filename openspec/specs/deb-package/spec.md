# deb-package Specification

## Purpose
Le paquet Debian est un mode de livraison d'une release Pixs : il installe l'artefact et ses profils d'exécution sans jamais porter configuration sensible, données ou dérogations aux garanties de la release.

## Requirements

### Requirement: Paquet corrélé à la release

Chaque paquet MUST identifier sa release, son périmètre de composition, ses manifests, contrats, compatibilités et garanties. Il MUST rester corrélable aux autres artefacts de cette release pour les capacités communes. Cette corrélation MUST NOT imposer un contenu binaire identique entre le paquet PA, le paquet PBO/PFO et l’image sans fonctions de session ; les noms et versions exactes restent à spécifier.

#### Scenario: Version de paquet incohérente

- **WHEN** un paquet revendique une release différente de l’artefact qu’il installe
- **THEN** l’installation signale l’incohérence et bloque l’activation

#### Scenario: Deux paquets indépendants

- **WHEN** la composition Debian cible est vérifiée
- **THEN** le paquet PA et le paquet PBO/PFO restent distincts selon leurs exigences de composition

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

La distribution Debian MUST comporter un paquet PBO/PFO et un paquet PA indépendant. Le paquet PBO/PFO MUST contenir le module essentiel PZT et MUST NOT embarquer les quatre binaires PA. L’installation PA seule MUST NOT requérir PBO/PFO locaux comme contenu embarqué ; les compatibilités et dépendances d’installation restent déclarées.

#### Scenario: Distribution Debian indépendante PA et PBO PFO

- **WHEN** PA est installé seul
- **THEN** son paquet reste indépendant et peut joindre un PBO distant autorisé

### Requirement: Quatre binaires dans le paquet PA

Le paquet PA MUST livrer exactement les quatre exécutables définis par pixs-agent : démon système, événements de démarrage/arrêt de l’hôte, sessions utilisateur et exécution PZT. Il MUST conserver la séparation des modes et permissions ; noms/chemins et versions restent à spécifier.

#### Scenario: Quatre binaires dans le paquet PA

- **WHEN** le paquet PA est vérifié
- **THEN** les quatre binaires et leurs responsabilités sont identifiables sans PBO/PFO embarqués
