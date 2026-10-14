## MODIFIED Requirements

### Requirement: Contenu minimal d'un événement d'audit

Un événement d'audit MUST pouvoir représenter au minimum un identifiant, l'instant, l'acteur ou sa référence, le tenant pertinent, l'action, le type et l'identifiant de ressource, le résultat, la raison ou code d'erreur éventuel, les identifiants de corrélation et de causalité, et le composant avec sa version.

#### Scenario: Refus d'autorisation tracé

- **WHEN** une opération autorisée est refusée par l'évaluation d'autorisation
- **THEN** l'événement d'audit contient acteur, action, cible, résultat et corrélation sans attribut confidentiel superflu
