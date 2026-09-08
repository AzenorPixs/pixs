# events Specification

## Purpose
Les événements notifient des faits déjà survenus, versionnés et immuables, sans remplacer les garanties transactionnelles synchrones.

## Requirements

### Requirement: Événements immuables versionnés

Chaque événement DOIT porter type, version, producteur, schéma et périmètre d'ordre déclaré ; les événements de domaine internes et d'intégration publics restent des contrats distincts.

#### Scenario: Contrat d'intégration séparé

- **WHEN** un événement de domaine est exposé vers l'extérieur
- **THEN** il passe par un contrat d'intégration versionné distinct, jamais par exposition directe

### Requirement: Publication après validation transactionnelle

Un événement issu d'une mutation NE DOIT être publié qu'après validation de la transaction ; en cas d'échec, il reste absent du mécanisme de diffusion.

#### Scenario: Transaction échouée sans événement

- **WHEN** la transaction métier échoue
- **THEN** aucun événement d'acquisition n'est publié

### Requirement: Consommateurs idempotents et ordonnés

La garantie générale est au-moins-une-fois ; l'ordre n'est garanti que par agrégat ou partition déclaré ; les consommateurs DOIVENT supporter les rejou sans double effet métier.

#### Scenario: Rejou sans double effet

- **WHEN** un événement est livré deux fois
- **THEN** le consommateur le déduplique et ne produit qu'un seul effet confirmé
