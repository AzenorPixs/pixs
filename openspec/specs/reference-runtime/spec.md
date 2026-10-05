# reference-runtime Specification

## Purpose

Le runtime de référence fixe une pile implémentable sans fermer les contrats du
Kernel à des adapters futurs explicitement spécifiés.

## Requirements

### Requirement: Pile de référence unique

Le runtime de référence MUST utiliser Django pour l'autorité métier,
PostgreSQL comme source de vérité applicative et TanStack comme frontend de
référence. L'agnosticisme de Pixs MUST concerner domaines, contrats, providers
et intégrations, et MUST NOT promettre une interchangeabilité immédiate de la pile.

#### Scenario: Runtime décrit

- **WHEN** une release décrit son runtime de référence
- **THEN** elle identifie Django, PostgreSQL et TanStack sans les confondre avec des providers optionnels

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
Le projet MUST adapter l'intégralité de son code, ses migrations, ses tests,
son runtime Python, ses dépendances directes et transitives et ses déclarations
de compatibilité aux besoins de cette version.

#### Scenario: Nouvelle version stable officielle

- **WHEN** Django publie une nouvelle version stable supportée
- **THEN** Pixs doit actualiser sa cible et adapter le code, le runtime et toutes les dépendances concernés
- **AND** toute incompatibilité restante doit être déclarée comme un travail de migration et ne justifie pas une cible ancienne implicite

#### Scenario: Migration encore non qualifiée

- **WHEN** les dépendances déclarées ou les validations portent encore sur une version antérieure
- **THEN** le projet doit rendre cet écart explicite et ne peut pas déclarer une conformité à la stable courante sans les preuves de qualification applicables

### Requirement: Relevé et qualification de la stable courante

Pixs MUST vérifier la cible dans les sources officielles Django à chaque
nouvelle stable et avant la qualification d'une nouvelle release.
`TECHNICAL.md` MUST rapporter la version stable supportée observée, l'horodatage
de vérification avec son fuseau et les liens officiels. Le relevé MUST
distinguer cible vérifiée, versions déclarées et migration effectivement
qualifiée. La qualification MUST fixer les versions exactes pour préserver la
reproductibilité et MUST vérifier le graphe de dépendances, les tests et les
migrations applicables ; elle MUST NOT procéder par mise à niveau silencieuse.
La politique des dépendances Python MUST s'appliquer à toutes les dépendances
sans exception, psycopg compris. Un pin historique MUST NOT constituer une
dérogation à la priorité des contraintes Django et à la cohérence du graphe.

#### Scenario: Relevé horodaté

- **WHEN** la stable officielle est vérifiée
- **THEN** TECHNICAL.md enregistre la version, l'instant de consultation avec fuseau et les sources officielles sans présenter cette consultation comme une installation ou une qualification

#### Scenario: Build reproductible et nouvelle qualification

- **WHEN** une nouvelle release est qualifiée sur la stable courante
- **THEN** ses versions sont fixées exactement et sa compatibilité complète est validée, tout écart restant empêchant la déclaration de conformité
- **AND** les versions figées des artefacts historiques restent reconstructibles sans constituer une dérogation à la cible de la nouvelle release

### Requirement: Dépendances Python les plus récentes compatibles avec Django

Les dépendances Python nécessaires au projet, directes et transitives, MUST
utiliser leur dernière version disponible compatible avec la stable Django
ciblée et avec l'ensemble du graphe installé dans l'environnement du projet.
Une version exacte ou une plage supportée indiquée par Django MUST prévaloir
sur la dernière version disponible du paquet. Une version exacte imposée MUST
être respectée ; une plage MUST conduire à la version admissible la plus récente,
sans traiter une borne minimale comme un verrouillage exact. En l'absence de
contrainte Django explicite, la compatibilité MUST être qualifiée par les
métadonnées et les tests applicables. La qualification MUST conserver les
sources et versions retenues et MUST vérifier ensemble les dépendances directes
et transitives. Toute incompatibilité restante MUST être explicite et conduire
à l'adaptation du code ou de l'environnement ; le projet MUST NOT installer de
force une version refusée par Django ni revenir à un ancien Django pour adopter
une dépendance plus récente.

#### Scenario: Version imposée par Django

- **WHEN** la dernière version disponible d'une dépendance ne respecte pas la version exacte ou la plage supportée imposée par Django
- **THEN** la contrainte Django prévaut et la dernière version admissible est retenue sous réserve de la cohérence du graphe complet

#### Scenario: Plage et borne minimale

- **WHEN** Django indique une plage supportée contenant plusieurs versions disponibles
- **THEN** la version compatible la plus récente est retenue et une simple borne minimale ne devient pas une version exacte imposée

#### Scenario: Graphe incompatible ou contrainte absente

- **WHEN** une dépendance n'a pas de contrainte Django explicite ou que le graphe complet présente une incompatibilité
- **THEN** les métadonnées et tests applicables doivent qualifier la compatibilité, tout conflit restant empêchant une déclaration de conformité sans forcer l'installation ni rétrograder la cible Django

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
