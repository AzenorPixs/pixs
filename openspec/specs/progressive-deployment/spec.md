# progressive-deployment Specification

## Purpose

Le déploiement progressif active des révisions compatibles de manière
contrôlée, observable et réversible sans contourner les garanties de release,
de migration ou de sécurité.

## Requirements

### Requirement: Révisions et stratégies explicitement déclarées

Toute opération de déploiement progressif MUST identifier une release immuable,
sa composition, son environnement, sa stratégie et son périmètre. Canary,
blue/green et activation graduelle MAY être proposés par des adapters, mais une
stratégie MUST NOT être déduite d'un fournisseur ou de l'ordre des instances.

#### Scenario: Stratégie non déclarée

- **WHEN** une révision est prête sans stratégie de promotion approuvée
- **THEN** elle reste non exposée au trafic de production

### Requirement: Prévalidations et health gates obligatoires

Avant chaque promotion, le système MUST vérifier compatibilité, migrations,
configuration, sécurité, disponibilité et health gates déclarées. Une mesure ou
un signal non vérifiable MUST empêcher la promotion automatique.

#### Scenario: Readiness en échec

- **WHEN** la révision canary échoue sa readiness ou son health gate
- **THEN** le trafic n'est pas augmenté et l'état est diagnostiqué

### Requirement: Routage progressif sans élargissement de données

La répartition de trafic MUST préserver tenant, scope, identité, contrat et
résidence. Un déploiement progressif MUST NOT exposer une API incompatible, une
configuration non validée ou une donnée de tenant à une révision non autorisée.

#### Scenario: Client utilisant une majeure antérieure

- **WHEN** une révision active une nouvelle version majeure d'API
- **THEN** le routage conserve le contrat compatible ou refuse explicitement le client

### Requirement: Retour arrière orchestré et audité

Un retour arrière MUST respecter la matrice de compatibilité, les migrations et
l'intégrité des données ; il MUST NOT simuler un rollback par suppression ou
réécriture silencieuse. Chaque promotion, arrêt et retour arrière MUST être
audité et corrélé.

#### Scenario: Migration irréversible appliquée

- **WHEN** la révision a appliqué une migration non réversible
- **THEN** le système bloque le retour arrière non compatible et exige le plan déclaré
