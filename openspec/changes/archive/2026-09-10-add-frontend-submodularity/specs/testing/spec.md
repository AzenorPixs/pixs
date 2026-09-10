## ADDED Requirements

### Requirement: Conformité de la composition frontend récursive

Les suites de conformité MUST vérifier la résolution récursive des modules et sous-modules frontend, la propriété des contributions, les dépendances publiques, les contraintes SemVer, les collisions, les modes obligatoire et optionnel, ainsi que l'équivalence de composition entre développement et artefacts distribués. Une résolution frontend MUST NOT dépendre de l'ordre des imports, du filesystem ou d'un code distant runtime.

#### Scenario: Composition reproductible avec sous-module

- **WHEN** la même composition incluant un module et un sous-module frontend est construite deux fois
- **THEN** les contributions actives, l'ordre de chargement et les diagnostics produits sont identiques
