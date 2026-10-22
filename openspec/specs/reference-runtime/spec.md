# reference-runtime Specification

## Purpose

Le runtime de référence fixe le binaire PBO commun et sa pile applicative, avec
modules composés dans une même application et exécutants PA/PZT indépendants.
Les profils de processus suivent runtime ; les contrats du Kernel restent ouverts
à des adapters futurs explicitement spécifiés.

## Requirements

### Requirement: Binaire PBO commun et socle modulaire

PBO MUST être livré comme un binaire applicatif commun regroupant le Kernel, pixs.core, pixs.auth, pixs.agent et pixs.pzt dans une même application modulaire. Les modules MUST conserver contrats publics, données et permissions propres ; leur présence MUST NOT imposer un démon par module. Les profils de processus MUST suivre runtime sans remplacer Django ni embarquer les exécutants PA/PZT.

#### Scenario: Socle partagé par plusieurs rôles

- **WHEN** la même release démarre des processus PBO web et worker
- **THEN** ils utilisent le même binaire et le même graphe de composition, avec une activation de rôle explicite

#### Scenario: Contrats conservés dans un processus

- **WHEN** Auth ou un module de gestion consomme une primitive Core dans le même processus
- **THEN** il utilise son contrat public sans accès aux données privées ni canal IPC imposé entre ces modules

### Requirement: Compilation PBO Nuitka standalone

PBO MUST être compilé avec Nuitka en mode standalone. Les livraisons Debian/Docker MUST contenir l'exécutable PBO commun, ses bibliothèques, runtime et ressources déclarés, sans imposer un fichier autoextractible unique. Le mode onefile MUST NOT remplacer standalone sans évolution approuvée. Les versions, options, imports dynamiques Django et données de package MUST être qualifiés explicitement.

#### Scenario: Distribution autonome complète

- **WHEN** une distribution du binaire PBO est qualifiée
- **THEN** les rôles web, worker et scheduler, imports Django, migrations, catalogues et ressources nécessaires fonctionnent avec les dépendances livrées et la configuration externe déclarée

#### Scenario: Mode onefile substitué

- **WHEN** un build utilise onefile à la place du mode standalone retenu sans évolution approuvée
- **THEN** il ne satisfait pas le profil de construction PBO

### Requirement: Cython ciblé et mesuré dans PBO

Dans PBO, Cython MUST être réservé aux optimisations ciblées dont le profilage identifie le coût et dont des mesures comparables démontrent un gain selon des critères définis avant recette. La qualification MUST vérifier ressources, contrats, sécurité, maintenabilité et non-régression ; Cython MUST NOT remplacer la chaîne Nuitka du PBO complet. Les exécutants indépendants PA/PZT MUST suivre leurs chaînes Cython distinctes.

#### Scenario: Optimisation sans preuve

- **WHEN** un module Cython est proposé dans PBO sans profilage ni comparaison mesurée du périmètre optimisé
- **THEN** il n'est pas admis dans une composition qualifiée sur cette seule proposition

#### Scenario: Gain ciblé qualifié

- **WHEN** une optimisation Cython est évaluée à code fonctionnel, données, environnement, configuration et charge comparables
- **THEN** les mesures mémoire, CPU, latence ou débit pertinents et les contrôles de non-régression justifient son admission sans affaiblir les contrats ou la sécurité

### Requirement: Qualification du binaire PBO

La construction du binaire PBO MUST qualifier versions de Nuitka, Python, dépendances, compilateur C, ABI, plateformes et options du profil standalone avant distribution. Le nom du fichier et les options CLI MUST être documentés explicitement. Un binaire compilé MUST NOT prouver à lui seul une réduction mémoire, un gain de débit ou une exécution Python parallèle sur plusieurs cœurs.

#### Scenario: Compilation sans mesure de performance

- **WHEN** un binaire PBO est construit sans recette de charge ni de ressources
- **THEN** aucun gain de performance ni support multicœur effectif n'est annoncé sur cette seule base

### Requirement: Pile de référence unique

Le runtime applicatif PBO/PFO MUST utiliser Django pour l’autorité métier, PostgreSQL comme source de vérité et TanStack comme frontend de référence. L’agnosticisme MUST concerner domaines, contrats, providers et intégrations et MUST NOT promettre l’interchangeabilité immédiate de cette pile. PA, PZT, pixs.agent et pixs.pzt MUST respecter leurs exigences distinctes.

#### Scenario: Runtime décrit

- **WHEN** une release décrit PBO/PFO et les binaires PA
- **THEN** elle identifie Django/PostgreSQL/TanStack pour PBO/PFO et les fonctions locales PA séparément

#### Scenario: Réseau désactivé

- **WHEN** une composition PBO désactive l’exécution réseau PZT
- **THEN** le module essentiel de configuration et de supervision reste composé

### Requirement: Adapter explicite

Un adapter de runtime futur MAY être proposé comme composant distinct. Il MUST
déclarer contrats, compatibilités, limites et preuves de conformité et MUST NOT
modifier implicitement les garanties du runtime de référence.

#### Scenario: Runtime alternatif non déclaré

- **WHEN** un artefact remplace un élément de la pile sans adapter validé
- **THEN** il ne peut pas être déclaré compatible avec le profil de référence

### Requirement: Absence de sélection cachée

Le build et le runtime MUST NOT sélectionner une pile alternative selon
l'environnement, l'ordre des imports ou la présence d'un paquet.

#### Scenario: Paquet alternatif présent

- **WHEN** un paquet d'un autre backend est présent dans l'artefact
- **THEN** il ne change pas le runtime effectif sans sélection explicite

### Requirement: Version stable actuelle de Django

Pixs MUST cibler en permanence la dernière version stable officielle encore
supportée par le projet Django, avec ses correctifs et ses évolutions mineures
ou majeures. Une préversion ou une branche de développement MUST NOT constituer
cette cible ; une ancienne série LTS MUST NOT remplacer la stable courante.

#### Scenario: Nouvelle version stable officielle

- **WHEN** Django publie une nouvelle version stable supportée
- **THEN** Pixs doit actualiser sa cible et adapter le code, le runtime et toutes les dépendances concernés
- **AND** toute incompatibilité restante doit être déclarée comme un travail de migration et ne justifie pas une cible ancienne implicite

### Requirement: Adaptation complète à la stable Django ciblée

Le projet MUST adapter l'intégralité de son code, ses migrations, ses tests,
son runtime Python, ses dépendances directes et transitives et ses déclarations
de compatibilité aux besoins de cette version.

#### Scenario: Migration encore non qualifiée

- **WHEN** les dépendances déclarées ou les validations portent encore sur une version antérieure
- **THEN** le projet doit rendre cet écart explicite et ne peut pas déclarer une conformité à la stable courante sans les preuves de qualification applicables

### Requirement: Relevé et qualification de la stable courante

Pixs MUST vérifier la cible dans les sources officielles Django à chaque
nouvelle stable et avant la qualification d'une nouvelle release. `TECHNICAL.md` MUST rapporter la version stable supportée observée, l'horodatage
de vérification avec son fuseau et les liens officiels. Le relevé MUST
distinguer cible vérifiée, versions déclarées et migration effectivement
qualifiée.

#### Scenario: Relevé horodaté

- **WHEN** la stable officielle est vérifiée
- **THEN** TECHNICAL.md enregistre la version, l'instant de consultation avec fuseau et les sources officielles sans présenter cette consultation comme une installation ou une qualification

### Requirement: Qualification reproductible et politique sans dérogation

La qualification MUST fixer les versions exactes pour préserver la
reproductibilité et MUST vérifier le graphe de dépendances, les tests et les
migrations applicables ; elle MUST NOT procéder par mise à niveau silencieuse. La politique des dépendances Python MUST s'appliquer à toutes les dépendances
sans exception, psycopg compris. Un pin historique MUST NOT constituer une
dérogation à la priorité des contraintes Django et à la cohérence du graphe.

#### Scenario: Build reproductible et nouvelle qualification

- **WHEN** une nouvelle release est qualifiée sur la stable courante
- **THEN** ses versions sont fixées exactement et sa compatibilité complète est validée, tout écart restant empêchant la déclaration de conformité
- **AND** les versions figées des artefacts historiques restent reconstructibles sans constituer une dérogation à la cible de la nouvelle release

### Requirement: Dépendances Python les plus récentes compatibles avec Django

Les dépendances Python nécessaires au projet, directes et transitives, MUST
utiliser leur dernière version disponible compatible avec la stable Django
ciblée et avec l'ensemble du graphe installé dans l'environnement du projet. Une version exacte ou une plage supportée indiquée par Django MUST prévaloir
sur la dernière version disponible du paquet.

#### Scenario: Version imposée par Django

- **WHEN** la dernière version disponible d'une dépendance ne respecte pas la version exacte ou la plage supportée imposée par Django
- **THEN** la contrainte Django prévaut et la dernière version admissible est retenue sous réserve de la cohérence du graphe complet

### Requirement: Versions exactes, plages et bornes minimales Django

Une version exacte imposée MUST
être respectée ; une plage MUST conduire à la version admissible la plus récente,
sans traiter une borne minimale comme un verrouillage exact.

#### Scenario: Plage et borne minimale

- **WHEN** Django indique une plage supportée contenant plusieurs versions disponibles
- **THEN** la version compatible la plus récente est retenue et une simple borne minimale ne devient pas une version exacte imposée

### Requirement: Qualification du graphe Python et incompatibilités explicites

En l'absence de
contrainte Django explicite, la compatibilité MUST être qualifiée par les
métadonnées et les tests applicables. La qualification MUST conserver les
sources et versions retenues et MUST vérifier ensemble les dépendances directes
et transitives. Toute incompatibilité restante MUST être explicite et conduire
à l'adaptation du code ou de l'environnement.

#### Scenario: Graphe incompatible ou contrainte absente

- **WHEN** une dépendance n'a pas de contrainte Django explicite ou que le graphe complet présente une incompatibilité
- **THEN** les métadonnées et tests applicables doivent qualifier la compatibilité, tout conflit restant empêchant une déclaration de conformité sans forcer l'installation ni rétrograder la cible Django

### Requirement: Absence d'installation forcée ou de recul Django

Le projet MUST NOT installer de
force une version refusée par Django ni revenir à un ancien Django pour adopter
une dépendance plus récente.

#### Scenario: Version de dépendance refusée par Django

- **WHEN** une version candidate exige de forcer une dépendance refusée ou de revenir à un ancien Django
- **THEN** le projet ne l'installe pas de force et ne recule pas sa cible Django pour adopter cette dépendance

### Requirement: Compatibilité avec le Python actuel du projet

Toute évolution de dépendance Python MUST être supportée par le Python actuel
du projet déclaré dans `DEVOPS.md`. Une incompatibilité MUST suspendre
l'évolution jusqu'à validation ou refus explicite du développeur. Les agents
MUST NOT valider cette exception, changer Python ou masquer le conflit.
La solution retenue MUST être qualifiée avant installation.

#### Scenario: Version compatible

- **WHEN** une évolution de dépendance est proposée
- **THEN** ses contraintes Requires-Python, ses wheels et ses tests doivent confirmer son support du Python actuel, en complément des contraintes Django et du graphe complet

#### Scenario: Incompatibilité avec Python actuel

- **WHEN** la version candidate n'est pas supportée par le Python actuel du projet
- **THEN** l'évolution reste suspendue et seul le développeur peut la valider ou la refuser, y compris tout changement de version Python nécessaire
- **AND** les agents ne forcent pas l'installation et ne modifient pas implicitement la cible pour masquer l'incompatibilité

#### Scenario: Solution validée par le développeur

- **WHEN** le développeur valide une solution après une incompatibilité
- **THEN** la solution choisie doit être qualifiée techniquement avant installation, la validation humaine ne constituant pas en soi une preuve de compatibilité

### Requirement: Couche exécutable PA séparée

Les trois binaires PA définis par pixs-agent et le binaire indépendant PZT
défini par pzt MUST rester distincts du runtime applicatif. Ils MUST NOT
remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier
alternatif. Les trois binaires PA et PZT MUST suivre Cython,
avec chaînes et plateformes qualifiées avant construction.

#### Scenario: Exécutants distincts du backend

- **WHEN** une release décrit PA et PZT
- **THEN** elle distingue trois binaires PA et un binaire PZT sans autorité métier alternative

### Requirement: Modules de gestion pixs.agent et pixs.pzt dans PBO

La composition cible PBO MUST inclure pixs.agent pour la gestion PA hors PZT
selon pixs-agent et le module essentiel pixs.pzt selon pzt, même réseau
désactivé. Les deux modules MUST utiliser les mécanismes communs et les
primitives pixs.core par contrats publics. La gestion PZT MUST rester dans
pixs.pzt et son exécution dans le binaire indépendant PZT.

#### Scenario: Composition des deux modules de gestion

- **WHEN** la composition PBO est décrite
- **THEN** pixs.agent et pixs.pzt ont des responsabilités et contrats distincts au-dessus du Kernel et de pixs.core

#### Scenario: Réseau désactivé

- **WHEN** l’opérateur désactive le réseau PZT
- **THEN** le binaire réseau se ferme et pixs.pzt demeure dans PBO
