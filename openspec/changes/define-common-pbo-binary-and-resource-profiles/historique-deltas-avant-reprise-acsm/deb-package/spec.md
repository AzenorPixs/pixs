## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Installation des profils de processus configurables

Le paquet PBO/PFO MUST livrer le binaire PBO commun Nuitka standalone de reference-runtime et les ressources frontend. Les profils PBO et ceux du paquet indépendant PA/PZT MUST suivre runtime et rester configurables hors des artefacts. Les unités de supervision MUST appliquer rôles, instances et budgets déclarés sans installer un démon par module ni déduire un nombre de processus du serveur physique.

#### Scenario: Installation sur deux tailles d'hôte

- **WHEN** le même paquet est installé sur deux environnements aux budgets différents
- **THEN** le binaire reste identique pour la même cible de build et les configurations runtime adaptent les processus sans reconstruire une variante métier

#### Scenario: Paquet PA PZT autonome

- **WHEN** le paquet commun PA/PZT est installé sans PBO local
- **THEN** ses exécutants utilisent leurs profils de ressources propres et un PBO distant autorisé peut les gérer via les contrats existants
