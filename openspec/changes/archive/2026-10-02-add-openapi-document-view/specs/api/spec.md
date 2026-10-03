## MODIFIED Requirements

### Requirement: Contrats OpenAPI versionnés par majeure

Chaque capacité exposée MUST disposer d'un contrat OpenAPI publié et versionné ; la majeure figure dans le chemin, les évolutions compatibles conservent l'URL, toute rupture impose une nouvelle majeure avec coexistence déclarée.

#### Scenario: Rupture sans nouvelle majeure bloquée

- **WHEN** une évolution incompatible conserve la même majeure
- **THEN** le build refuse la publication du contrat
