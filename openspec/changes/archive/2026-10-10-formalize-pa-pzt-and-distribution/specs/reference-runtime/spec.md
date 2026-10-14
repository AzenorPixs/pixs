## MODIFIED Requirements

### Requirement: Pile de référence unique

Le runtime applicatif PBO/PFO MUST utiliser Django pour l’autorité métier, PostgreSQL comme source de vérité et TanStack comme frontend de référence. L’agnosticisme MUST concerner domaines, contrats, providers et intégrations et MUST NOT promettre l’interchangeabilité immédiate de cette pile. Les binaires PA et le module essentiel PZT MUST respecter leurs exigences distinctes de cette capacité.

#### Scenario: Runtime décrit

- **WHEN** une release décrit PBO/PFO et les binaires PA
- **THEN** elle identifie Django/PostgreSQL/TanStack pour PBO/PFO et les fonctions locales PA séparément

#### Scenario: Réseau désactivé

- **WHEN** une composition PBO désactive l’exécution réseau PZT
- **THEN** le module essentiel de configuration et de supervision reste composé

## ADDED Requirements

### Requirement: Couche exécutable PA séparée

Les binaires PA définis par pixs-agent MUST constituer une couche d’exécution locale distincte et MUST NOT remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier alternatif. Leur compilation MUST suivre le choix Nuitka pour trois binaires et Cython pour PZT.

#### Scenario: Couche exécutable PA séparée

- **WHEN** un binaire PA est décrit
- **THEN** il ne devient pas une implémentation alternative de l’autorité métier PBO

### Requirement: Module PZT essentiel dans PBO

La composition cible PBO MUST inclure le module essentiel PZT défini par pzt, même lorsque le réseau est désactivé. Configuration, visualisation, supervision et monitoring MUST rester dans PBO ; le réseau activé/configuré MUST être exécuté par le binaire PZT de PA.

#### Scenario: Module PZT essentiel dans PBO

- **WHEN** l’opérateur désactive le réseau PZT
- **THEN** le binaire réseau se ferme et le module essentiel demeure dans PBO
