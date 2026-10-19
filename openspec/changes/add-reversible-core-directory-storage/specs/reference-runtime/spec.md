## MODIFIED Requirements

### Requirement: Pile de référence unique

PBO/PFO MUST utiliser Django, PostgreSQL par défaut et TanStack. Le seul déplacement Core autorisé ici MUST suivre core-storage pour OpenLDAP interne après migration réversible qualifiée ; les autres données MUST garder leur stockage déclaré. L'agnosticisme MUST NOT promettre l'interchangeabilité immédiate de la pile. PA, PZT, pixs.agent et pixs.pzt MUST respecter leurs exigences distinctes.

#### Scenario: Runtime décrit

- **WHEN** une release décrit PBO/PFO et les binaires PA
- **THEN** elle identifie Django/PostgreSQL/TanStack pour PBO/PFO et les fonctions locales PA séparément
- **AND** elle déclare le provider Core effectivement engagé si l'option OpenLDAP est sélectionnée

#### Scenario: Réseau désactivé

- **WHEN** une composition PBO désactive l'exécution réseau PZT
- **THEN** le module essentiel de configuration et de supervision reste composé
