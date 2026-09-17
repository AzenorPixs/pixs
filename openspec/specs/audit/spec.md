# audit Specification

## Purpose
L'audit fonctionnel trace les événements métier significatifs, séparés des logs techniques, persistants, append-only et soumis à des politiques de rétention et de minimisation.

## Requirements

### Requirement: Audit fonctionnel distinct des logs techniques

L'audit MUST être un flux fonctionnel séparé des journaux, métriques et traces techniques ; un événement d.audit MUST NOT être reconstitué implicitement à partir de logs.

#### Scenario: Perte de télémétrie technique

- **WHEN** la collecte de logs techniques est indisponible
- **THEN** les événements d'audit requis restent persistés et aucune mutation métier conforme n'est bloquée par cette indisponibilité

### Requirement: Contenu minimal d'un événement d'audit

Un événement d'audit MUST pouvoir représenter au minimum un identifiant, l'instant, l'acteur ou sa référence, le tenant pertinent, l'action, le type et l'identifiant de ressource, le résultat, la raison ou code d'erreur éventuel, les identifiants de corrélation et de causalité, et le composant avec sa version.

#### Scenario: Refus d'autorisation tracé

- **WHEN** une opération autorisée est refusée par l'évaluation d'autorisation
- **THEN** l'événement d'audit contient acteur, action, cible, résultat et corrélation sans attribut confidentiel superflu

### Requirement: Périmètre obligatoire d'audit

Les authentifications, changements d'identité, autorisations sensibles, accès inter-tenants, mutations métier significatives, modifications de configuration et opérations destructives MUST produire un audit persistant, contrôlé et soumis à une politique de rétention.

#### Scenario: Opération destructive sans audit

- **WHEN** une opération destructive ne peut pas enregistrer son événement d'audit
- **THEN** l'opération est refusée en échec fermé avec un diagnostic explicite

### Requirement: Append-only et réécriture contrôlée

L'audit MUST être append-only dans son usage normal ; toute suppression ou minimisation imposée MUST passer par une procédure explicite et auditable d'anonymisation ou de purge de champs autorisés, sans présenter une réécriture comme un événement nouveau.

#### Scenario: Obligation d'effacement

- **WHEN** une obligation légale impose la suppression d'un champ d'audit
- **THEN** la procédure autorisée anonymise le champ et l'opération reste elle-même traçable

### Requirement: Minimisation et non-duplication des données

Les valeurs avant/après MUST être limitées aux champs nécessaires et redacted lorsqu'elles sont sensibles ; l'audit MUST NOT devenir une copie de la base métier ni contenir de secret.

#### Scenario: Payload sensible détecté

- **WHEN** une valeur sensible est proposée pour un champ avant/après
- **THEN** elle est redacted ou remplacée par une référence pseudonymisée dans l'événement d'audit

### Requirement: Audit exhaustif du panneau d'administration

Toute activité du panneau d'administration MUST produire un audit persistant :
connexion, déconnexion, lecture, navigation entre affichages, création,
modification, suppression, refus, changement de configuration, de route ou de
marqueur externe. Une action administrative qui ne peut pas produire cet audit
MUST être refusée. La politique d'audit MUST déclarer l'événement minimal, la
rétention, l'intégrité, les droits de consultation et la capacité de traitement
requise pour cette volumétrie.

#### Scenario: Navigation non auditable

- **WHEN** le panneau ne peut pas persister l'événement de navigation demandé
- **THEN** il refuse l'accès à l'affichage concerné sans exposer de donnée
  sensible
