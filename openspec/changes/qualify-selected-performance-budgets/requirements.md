# Références normatives — O31

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| performance / 8 | [Mesurer avant d'optimiser](../../specs/performance/spec.md#L8) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| performance / 17 | [Budgets déclarés et vérifiés](../../specs/performance/spec.md#L17) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| performance / 26 | [Objectifs propres au profil](../../specs/performance/spec.md#L26) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| performance / 38 | [Aucune performance au prix des invariants](../../specs/performance/spec.md#L38) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| performance / 47 | [Caches et projections dérivés non autoritaires](../../specs/performance/spec.md#L47) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| service-objectives / 10 | [Objectifs versionnés](../../specs/service-objectives/spec.md#L10) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| service-objectives / 21 | [Absence de seuil universel implicite](../../specs/service-objectives/spec.md#L21) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |
| service-objectives / 32 | [Validation reproductible](../../specs/service-objectives/spec.md#L32) | NE | AUDIT_ET_OBJECTIFS_A_ARRETER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence performance--0f768bb260

Source : `openspec/specs/performance/spec.md`, ligne 8. SHA-256 du bloc : `7393e85af49d33c78bbac1eebc34ce4d3c4f07b76168ab7f6807f0c484ae7a63`.

~~~~text
### Requirement: Mesurer avant d'optimiser

Toute optimisation MUST reposer sur des mesures issues des signaux d'observabilité du composant concerné ; une optimisation sans mesure préalable MUST NOT être retenue comme justification de complexité.

#### Scenario: Optimisation non mesurée

- **WHEN** un changement claimant un gain est proposé sans donnée de mesure
- **THEN** la vérification de performance ne peut valider le changement et l'écart est rapporté
~~~~

### Référence performance--15455e35b5

Source : `openspec/specs/performance/spec.md`, ligne 17. SHA-256 du bloc : `848c4592f9a819cd0ab3d6920c02bb842cc97530616c8bd8c2fe26b5240bacb5`.

~~~~text
### Requirement: Budgets déclarés et vérifiés

Chaque release MUST pouvoir déclarer des budgets et objectifs de performance par surface concernée, vérifiés de façon reproductible ; une régression au-delà du budget déclaré MUST être détectée et remontée explicitement.

#### Scenario: Régression détectée

- **WHEN** une exécution validée dépasse le budget déclaré d'une surface
- **THEN** la régression est signalée avec la référence du budget et l'écart constaté
~~~~

### Référence performance--b5e6edb9da

Source : `openspec/specs/performance/spec.md`, ligne 26. SHA-256 du bloc : `168fea33b0df0d86ed16c050e3331f8e6ffb1c9b22a6634ea57c154b41abce98`.

~~~~text
### Requirement: Objectifs propres au profil

Les budgets de performance et objectifs de latence MUST être associés à une
release ou un profil déclaré. Ils MUST indiquer leur surface, méthode de mesure
et période de validité ; un budget de profil MUST NOT être présenté comme une
garantie universelle de Pixs.

#### Scenario: Budget hors profil

- **WHEN** un résultat est publié sans profil ou release de référence
- **THEN** il reste informatif et ne valide aucune garantie de performance
~~~~

### Référence performance--b744417421

Source : `openspec/specs/performance/spec.md`, ligne 38. SHA-256 du bloc : `2ed9f4ad34ca90b99df5dc5efab065d520b78b612b5d0add79e1309559baf9fd`.

~~~~text
### Requirement: Aucune performance au prix des invariants

Les gains de performance MUST NOT affaiblir l'échec fermé, l'évaluation d'autorisation, l'isolation de tenant ou de périmètre, ni la traçabilité d'audit.

#### Scenario: Cache court-circuitant l'autorisation

- **WHEN** un cache proposé répondrait à une requête sans réévaluation de l'autorisation exigée par le contrat
- **THEN** le mécanisme est refusé comme non conforme
~~~~

### Référence performance--10165ca23e

Source : `openspec/specs/performance/spec.md`, ligne 47. SHA-256 du bloc : `36ccbaf9bfa240a46482151350cdd869732aef862bb4557fa8775df0b4e6d695`.

~~~~text
### Requirement: Caches et projections dérivés non autoritaires

Tout cache, index ou accélération MUST rester une dérivation reconstruisible dont l'absence ou l'obsolescence produit une dégradation contrôlée, jamais une autorité métier implicite.

#### Scenario: Cache périmé indisponible

- **WHEN** un cache tombe ou devient obsolète
- **THEN** le service revient à la source de référence avec un état diagnostiqué et sans résultat erroné servi
~~~~

### Référence service-objectives--274a08a5d0

Source : `openspec/specs/service-objectives/spec.md`, ligne 10. SHA-256 du bloc : `a17ae2f713d1615ca6559182ca738280de2c91682172911df16edbbe53d04918`.

~~~~text
### Requirement: Objectifs versionnés

Une release ou un profil MAY déclarer des objectifs de disponibilité, latence,
invalidation, reprise et compatibilité. Chaque objectif déclaré MUST préciser
son périmètre, seuil, méthode de mesure, période d'évaluation et version.

#### Scenario: Objectif de reprise déclaré

- **WHEN** un profil haute disponibilité déclare un objectif de reprise
- **THEN** sa mesure et son périmètre sont inspectables avec la release concernée
~~~~

### Référence service-objectives--d2ab8609fb

Source : `openspec/specs/service-objectives/spec.md`, ligne 21. SHA-256 du bloc : `c04c26435a2fb0feea7d010bbd60707683581947c2c2e57b852ce7530f4db170`.

~~~~text
### Requirement: Absence de seuil universel implicite

Pixs MUST NOT déduire un seuil universel de disponibilité ou performance du seul
runtime de référence. Un résultat hors de son profil ou de sa release MUST NOT
être présenté comme une garantie générale.

#### Scenario: Mesure locale isolée

- **WHEN** une mesure de latence est exécutée localement
- **THEN** elle reste informative sans objectif du profil qui l'associe à une garantie
~~~~

### Référence service-objectives--ad136b9940

Source : `openspec/specs/service-objectives/spec.md`, ligne 32. SHA-256 du bloc : `0c058bb85a99559611d6436e52925aae478ea004a119b80df63a420670faa443`.

~~~~text
### Requirement: Validation reproductible

La validation d'un objectif déclaré MUST produire une preuve reproductible ou
un diagnostic explicite d'insatisfaction. Elle MUST NOT exposer de secret ou
donnée de production.

#### Scenario: Objectif non satisfait

- **WHEN** une validation dépasse le seuil déclaré
- **THEN** le résultat identifie l'objectif, la mesure et l'écart sans masquer l'échec
~~~~

