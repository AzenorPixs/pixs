## MODIFIED Requirements

### Requirement: Définition versionnée et bornée

Chaque fanion MUST déclarer identifiant, version, propriétaire, finalité, type BOOLEAN ou VARIANT, défaut, dimensions, cohorte éventuelle, prérequis, repli, expiration et audit ; les règles sont déclaratives, bornées et déterministes, sans code arbitraire.

#### Scenario: Règle à expression rejetée

- **WHEN** une règle embarque du code ou une expression distante
- **THEN** la définition est refusée avant activation
