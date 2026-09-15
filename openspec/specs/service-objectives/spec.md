# service-objectives Specification

## Purpose

Les objectifs de service relient les garanties opérationnelles aux releases et
profils déclarés sans imposer une promesse chiffrée universelle à Pixs.

## Requirements

### Requirement: Objectifs versionnés

Une release ou un profil MAY déclarer des objectifs de disponibilité, latence,
invalidation, reprise et compatibilité. Chaque objectif déclaré MUST préciser
son périmètre, seuil, méthode de mesure, période d'évaluation et version.

#### Scenario: Objectif de reprise déclaré

- **WHEN** un profil haute disponibilité déclare un objectif de reprise
- **THEN** sa mesure et son périmètre sont inspectables avec la release concernée

### Requirement: Absence de seuil universel implicite

Pixs MUST NOT déduire un seuil universel de disponibilité ou performance du seul
runtime de référence. Un résultat hors de son profil ou de sa release MUST NOT
être présenté comme une garantie générale.

#### Scenario: Mesure locale isolée

- **WHEN** une mesure de latence est exécutée localement
- **THEN** elle reste informative sans objectif du profil qui l'associe à une garantie

### Requirement: Validation reproductible

La validation d'un objectif déclaré MUST produire une preuve reproductible ou
un diagnostic explicite d'insatisfaction. Elle MUST NOT exposer de secret ou
donnée de production.

#### Scenario: Objectif non satisfait

- **WHEN** une validation dépasse le seuil déclaré
- **THEN** le résultat identifie l'objectif, la mesure et l'écart sans masquer l'échec
