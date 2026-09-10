# secrets-providers Specification

## Purpose

Les fournisseurs de secrets résolvent au runtime des références externes avec
rotation, révocation, contrôle d'accès et audit, sans intégrer de secret aux
sources ou artefacts.

## Requirements

### Requirement: Références externes sans valeur persistée

La configuration, les manifests, les rapports, les diagnostics et les artefacts
MUST contenir uniquement des références de secrets autorisées. Une valeur de
secret, credential ou jeton MUST NOT être sérialisée, journalisée ou publiée.

#### Scenario: Diagnostic de référence indisponible

- **WHEN** un fournisseur ne peut pas résoudre une référence obligatoire
- **THEN** il signale la référence et l'erreur sans révéler de valeur attendue

### Requirement: Accès runtime associé à une identité de workload

Un SecretProvider MUST vérifier l'identité de workload, le composant, le tenant
ou scope lorsque requis, la finalité et la politique d'accès avant résolution.
Une référence valide MUST NOT donner accès à un secret hors du contexte autorisé.

#### Scenario: Worker non autorisé

- **WHEN** un worker demande une référence réservée au profil web
- **THEN** la résolution est refusée et auditée

### Requirement: Rotation, durée de vie et révocation contrôlées

Le fournisseur MUST déclarer la durée de vie, la rotation, la révocation et le
comportement de rafraîchissement applicables. Une révocation MUST empêcher les
nouvelles utilisations dans le délai déclaré sans laisser un cache prolonger
silencieusement un accès interdit. Le fournisseur MUST privilégier des
credentials courts associés à une identité de workload ; un secret statique
MUST NOT être utilisé lorsqu'un credential court compatible est disponible.

#### Scenario: Secret tourné

- **WHEN** une référence est remplacée par une version rotée
- **THEN** les consommateurs autorisés rafraîchissent leur accès sans placer la valeur dans un artefact

### Requirement: Audit minimisé et échec fermé

Les résolutions, refus, rotations et révocations MUST être auditables avec une
identité, une référence et une corrélation. Une indisponibilité ou une politique
non vérifiable MUST échouer fermé pour une capacité protégée.

#### Scenario: Provider indisponible

- **WHEN** un secret requis ne peut pas être résolu au démarrage
- **THEN** le composant concerné ne devient pas prêt
