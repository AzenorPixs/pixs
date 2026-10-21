## MODIFIED Requirements

### Requirement: Couche exécutable PA séparée

Les trois binaires PA définis par pixs-agent et le binaire indépendant PZT
défini par pzt MUST rester distincts du runtime applicatif. Ils MUST NOT
remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier
alternatif. Les trois binaires PA et PZT MUST suivre Cython,
avec chaînes et plateformes qualifiées avant construction.

#### Scenario: Exécutants distincts du backend

- **WHEN** une release décrit PA et PZT
- **THEN** elle distingue trois binaires PA et un binaire PZT sans autorité métier alternative

## ADDED Requirements

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
