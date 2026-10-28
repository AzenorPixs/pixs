## MODIFIED Requirements

### Requirement: Mesurer avant d'optimiser

Toute optimisation MUST reposer sur des mesures issues des signaux d'observabilité du composant concerné ; une optimisation sans mesure préalable MUST NOT être retenue comme justification de complexité.

#### Scenario: Optimisation non mesurée

- **WHEN** un changement claimant un gain est proposé sans donnée de mesure
- **THEN** la vérification de performance ne peut valider le changement et l'écart est rapporté

### Requirement: Budgets déclarés et vérifiés

Chaque release MUST pouvoir déclarer des budgets et objectifs de performance par surface concernée, vérifiés de façon reproductible ; une régression au-delà du budget déclaré MUST être détectée et remontée explicitement.

#### Scenario: Régression détectée

- **WHEN** une exécution validée dépasse le budget déclaré d'une surface
- **THEN** la régression est signalée avec la référence du budget et l'écart constaté

### Requirement: Aucune performance au prix des invariants

Les gains de performance MUST NOT affaiblir l'échec fermé, l'évaluation d'autorisation, l'isolation de tenant ou de périmètre, ni la traçabilité d'audit.

#### Scenario: Cache court-circuitant l'autorisation

- **WHEN** un cache proposé répondrait à une requête sans réévaluation de l'autorisation exigée par le contrat
- **THEN** le mécanisme est refusé comme non conforme

### Requirement: Caches et projections dérivés non autoritaires

Tout cache, index ou accélération MUST rester une dérivation reconstruisible dont l'absence ou l'obsolescence produit une dégradation contrôlée, jamais une autorité métier implicite.

#### Scenario: Cache périmé indisponible

- **WHEN** un cache tombe ou devient obsolète
- **THEN** le service revient à la source de référence avec un état diagnostiqué et sans résultat erroné servi
