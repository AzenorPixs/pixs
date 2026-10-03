## MODIFIED Requirements

### Requirement: États de disponibilité distincts

Le système MUST respecter les garanties suivantes.

La disponibilité SUIT DECLARED vers RESOLVED vers AVAILABLE, avec DEGRADED, DISABLED et BLOCKED ; une capacité obligatoire non AVAILABLE bloque l'activation, une optionnelle reste isolée avec repli déclaré.

#### Scenario: Capacité optionnelle indisponible isolée

- **WHEN** une capacité optionnelle est absente ou incompatible
- **THEN** le composant reste valide avec un comportement dégradé déclaré et diagnostiqué
