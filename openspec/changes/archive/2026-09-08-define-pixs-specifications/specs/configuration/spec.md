## Purpose

La configuration déclarative, typée et validable garantit une activation déterministe sans exposer de secret.

## ADDED Requirements

### Requirement: Schémas typés validés avant activation

Chaque composant DOIT déclarer le schéma de sa configuration avec types, valeurs requises, défauts, contraintes et validations ; toute configuration invalide bloque l'activation ou le passage à ready.

#### Scenario: Configuration invalide bloquée

- **WHEN** une valeur viole le schéma déclaré
- **THEN** l'activation est refusée avec un diagnostic explicite

### Requirement: Priorité déterministe des sources

La résolution SUIT schéma, défauts du composant, configuration statique, configuration runtime, puis références de secrets ; une source prioritaire remplace l'inférieure sans fusion ambiguë.

#### Scenario: Surcharge déterministe

- **WHEN** plusieurs sources définissent la même clé
- **THEN** la valeur prioritaire s'applique de façon reproductible

### Requirement: Secrets par référence hors artefacts

Les secrets NE DOIVENT figurer ni dans les manifests, ni dans les paquets, images ou journaux ; seules des références contrôlées sont résolues au runtime.

#### Scenario: Secret embarqué refusé

- **WHEN** un artefact contient une valeur de secret
- **THEN** le build refuse la composition
