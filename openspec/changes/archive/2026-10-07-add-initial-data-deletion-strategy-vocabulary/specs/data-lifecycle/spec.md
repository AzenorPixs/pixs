# data-lifecycle

## MODIFIED Requirements

### Requirement: Vocabulaire commun des stratégies de suppression

Le vocabulaire commun des stratégies de suppression MUST contenir exactement SOFT_DELETE, PHYSICAL_DELETE, ARCHIVE et IMMUTABLE ; ces noms MUST NOT ajouter de défaut, transition, calcul, politique ni autorisation d'effacement.

#### Scenario: Vocabulaire déclaratif distinct de la persistance

- **WHEN** un consommateur désigne la stratégie de suppression déclarée d'une ressource
- **THEN** il emploie l'une des quatre valeurs communes SOFT_DELETE, PHYSICAL_DELETE, ARCHIVE et IMMUTABLE, sans la confondre avec un état de persistance
- **AND** aucune valeur ne vaut à elle seule autorisation de suppression physique ou de purge

