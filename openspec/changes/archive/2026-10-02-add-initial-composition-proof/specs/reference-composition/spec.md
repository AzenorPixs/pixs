## MODIFIED Requirements

### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents
