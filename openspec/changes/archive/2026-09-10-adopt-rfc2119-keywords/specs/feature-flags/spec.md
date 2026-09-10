## MODIFIED Requirements

### Requirement: Définition versionnée et bornée

Chaque fanion MUST déclarer identifiant, version, propriétaire, finalité, type BOOLEAN ou VARIANT, défaut, dimensions, cohorte éventuelle, prérequis, repli, expiration et audit ; les règles sont déclaratives, bornées et déterministes, sans code arbitraire.

#### Scenario: Règle à expression rejetée

- **WHEN** une règle embarque du code ou une expression distante
- **THEN** la définition est refusée avant activation

### Requirement: Ciblage et cohorte déterministes

Le système MUST respecter les garanties suivantes.

L'évaluation utilise uniquement les dimensions déclarées (installation, environnement, tenant, scope enfant) avec priorité du général au spécifique et cohorte stable sans tirage par requête.

#### Scenario: Même contexte même décision

- **WHEN** le même contexte est évalué deux fois
- **THEN** le résultat est identique

### Requirement: Échec fermé pour le sensible

Le système MUST respecter les garanties suivantes.

Une valeur absente, invalide ou périmée applique le repli ; l'échec est fermé pour permission, mutation, donnée protégée ou contrat ; le frontal réévalue toujours côté applicatif avant exposition protégée.

#### Scenario: Fanion d'autorisation indisponible

- **WHEN** le fanion requis pour une mutation est indisponible
- **THEN** l'opération est refusée au lieu d'un repli permissif

### Requirement: Affectations hors artefacts

Le système MUST respecter les garanties suivantes.

Les affectations runtime proviennent d'une source persistante versionnée ; aucun paquet, image ni bundle n'embarque d'affectation ; les changements sont administrés, corrélés et audités.

#### Scenario: Affectation embarquée rejetée

- **WHEN** un artefact contient une affectation d'installation ou de production
- **THEN** le build refuse la composition
