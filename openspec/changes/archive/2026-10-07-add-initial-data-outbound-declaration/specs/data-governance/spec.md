# data-governance

## MODIFIED Requirements

### Requirement: Profil de gouvernance versionné par composant

Chaque composant qui introduit, dérive ou transfère des données MUST publier un profil versionné avec propriétaire, source de vérité, classes, confidentialité, données personnelles, finalités, rétention, suppression, consommateurs, processeurs, contraintes de résidence ou transfert, export et lignée.

#### Scenario: Flux sortant sans consommateur refusé

- **WHEN** un transfert déclare une destination sans consommateur ni garantie documentée
- **THEN** le flux est refusé avant activation
