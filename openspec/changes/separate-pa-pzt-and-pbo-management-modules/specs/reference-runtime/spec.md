## RENAMED Requirements

- FROM: `### Requirement: Module PZT essentiel dans PBO`
- TO: `### Requirement: Modules de gestion pixs.agent et pixs.pzt dans PBO`

## MODIFIED Requirements

### Requirement: Pile de référence unique

Le runtime applicatif PBO/PFO MUST utiliser Django pour l’autorité métier, PostgreSQL comme source de vérité et TanStack comme frontend de référence. L’agnosticisme MUST concerner domaines, contrats, providers et intégrations et MUST NOT promettre l’interchangeabilité immédiate de cette pile. PA, PZT, pixs.agent et pixs.pzt MUST respecter leurs exigences distinctes.

#### Scenario: Runtime décrit

- **WHEN** une release décrit PBO/PFO et les binaires PA
- **THEN** elle identifie Django/PostgreSQL/TanStack pour PBO/PFO et les fonctions locales PA séparément

#### Scenario: Réseau désactivé

- **WHEN** une composition PBO désactive l’exécution réseau PZT
- **THEN** le module essentiel de configuration et de supervision reste composé

### Requirement: Couche exécutable PA séparée

Les trois binaires PA définis par pixs-agent et le binaire indépendant PZT
défini par pzt MUST rester distincts du runtime applicatif. Ils MUST NOT
remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier
alternatif. Les trois binaires PA MUST suivre Nuitka et PZT MUST suivre Cython,
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
