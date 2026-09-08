## Purpose

La synchronisation réactive propage les états validés vers les clients via un mécanisme optionnel, sans devenir une autorité métier ni contourner l'autorisation.

## ADDED Requirements

### Requirement: Mécanisme réactif optionnel sous autorité applicative

Toute mutation DOIT être validée et transactionnée par l'applicatif avant propagation réactive ; un module sans besoin réactif NE DOIT pas dépendre du mécanisme de synchronisation.

#### Scenario: Mutation non validée non propagée

- **WHEN** une mutation n'a pas été validée par l'applicatif
- **THEN** elle n'est jamais diffusée comme état de référence

### Requirement: Périmètre et autorisation propagés aux projections

Chaque projection synchronisée DOIT porter tenant, scope, version et corrélation, respecter le filtrage autorisé et invalider les données révoquées, supprimées ou purgées via marqueurs.

#### Scenario: Donnée révoquée invalidée

- **WHEN** une révocation ou suppression survient à la source
- **THEN** les projections clientes concernées sont invalidées avant tout nouvel affichage

### Requirement: Cohérence déclarée et échec contrôlé

Cohérence éventuelle, fraîcheur maximale et dégradation sont déclarées par capacité et ressource ; toute incohérence ou perte de fournisseur produit un état contrôlé au lieu d'un succès implicite.

#### Scenario: Fournisseur perdu diagnostiqué

- **WHEN** le mécanisme de synchronisation devient indisponible
- **THEN** le client signale un état périmé ou hors ligne sans valider de mutation locale
