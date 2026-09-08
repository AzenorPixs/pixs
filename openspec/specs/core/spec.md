# core Specification

## Purpose
Le module obligatoire pixs.core fournit les primitives communes minimales au-dessus du noyau, sans y déplacer la logique métier.

## Requirements

### Requirement: Module obligatoire au-dessus du noyau

Toute composition Pixs DOIT inclure pixs.core comme module requis ; une composition sans pixs.core est invalide.

#### Scenario: Composition sans core refusée

- **WHEN** une composition omet pixs.core
- **THEN** l'activation est refusée avant tout chargement

### Requirement: Primitives minimales communes

pixs.core DOIT exposer utilisateurs, identités numériques, groupes, appartenances, tenants, rôles, ACL et permissions comme capacités communes de bas niveau, consommées via contrats et services.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module a besoin d'une identité ou d'une appartenance
- **THEN** il passe par le contrat ou le service exposé, sans accès direct aux tables internes

### Requirement: Aucun fournisseur concret imposé

Ni le noyau ni pixs.core NE DOIT imposer un annuaire, une authentification, un stockage ou une intégration concrets ; ces apports relèvent des modules, fournisseurs ou extensions.

#### Scenario: Substitution de fournisseur

- **WHEN** un fournisseur compatible remplace un autre sous contrat stable
- **THEN** les consommateurs fonctionnent sans modification de leur code
