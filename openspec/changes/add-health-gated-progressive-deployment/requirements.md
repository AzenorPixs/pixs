# Références normatives — O30

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| progressive-deployment / 11 | [Révisions et stratégies explicitement déclarées](../../specs/progressive-deployment/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| progressive-deployment / 23 | [Prévalidations et health gates obligatoires](../../specs/progressive-deployment/spec.md#L23) | NE | AUDIT_AVANT_CREATION |
| progressive-deployment / 34 | [Routage progressif sans élargissement de données](../../specs/progressive-deployment/spec.md#L34) | NE | AUDIT_AVANT_CREATION |
| progressive-deployment / 45 | [Retour arrière orchestré et audité](../../specs/progressive-deployment/spec.md#L45) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence progressive-deployment--62734fd18f

Source : `openspec/specs/progressive-deployment/spec.md`, ligne 11. SHA-256 du bloc : `6f7fbfb773305d367f4f41d82c569799f965d8dc2dc05fc34201619bf817ac7d`.

~~~~text
### Requirement: Révisions et stratégies explicitement déclarées

Toute opération de déploiement progressif MUST identifier une release immuable,
sa composition, son environnement, sa stratégie et son périmètre. Canary,
blue/green et activation graduelle MAY être proposés par des adapters, mais une
stratégie MUST NOT être déduite d'un fournisseur ou de l'ordre des instances.

#### Scenario: Stratégie non déclarée

- **WHEN** une révision est prête sans stratégie de promotion approuvée
- **THEN** elle reste non exposée au trafic de production
~~~~

### Référence progressive-deployment--8b8585fbee

Source : `openspec/specs/progressive-deployment/spec.md`, ligne 23. SHA-256 du bloc : `62a79511340b7679ed57f1615cd1604d85805e2897363d0d1ce61e7ddbec694e`.

~~~~text
### Requirement: Prévalidations et health gates obligatoires

Avant chaque promotion, le système MUST vérifier compatibilité, migrations,
configuration, sécurité, disponibilité et health gates déclarées. Une mesure ou
un signal non vérifiable MUST empêcher la promotion automatique.

#### Scenario: Readiness en échec

- **WHEN** la révision canary échoue sa readiness ou son health gate
- **THEN** le trafic n'est pas augmenté et l'état est diagnostiqué
~~~~

### Référence progressive-deployment--150f11a0d0

Source : `openspec/specs/progressive-deployment/spec.md`, ligne 34. SHA-256 du bloc : `377a8962a80137f9a031738e2178dfa2038954cd37c3387f6513fe3df8eab870`.

~~~~text
### Requirement: Routage progressif sans élargissement de données

La répartition de trafic MUST préserver tenant, scope, identité, contrat et
résidence. Un déploiement progressif MUST NOT exposer une API incompatible, une
configuration non validée ou une donnée de tenant à une révision non autorisée.

#### Scenario: Client utilisant une majeure antérieure

- **WHEN** une révision active une nouvelle version majeure d'API
- **THEN** le routage conserve le contrat compatible ou refuse explicitement le client
~~~~

### Référence progressive-deployment--627e3aab24

Source : `openspec/specs/progressive-deployment/spec.md`, ligne 45. SHA-256 du bloc : `f5c49d050e3f7349d0e5bd04fbd137ca070d3de6ca2525624db57ac7ee1a02fd`.

~~~~text
### Requirement: Retour arrière orchestré et audité

Un retour arrière MUST respecter la matrice de compatibilité, les migrations et
l'intégrité des données ; il MUST NOT simuler un rollback par suppression ou
réécriture silencieuse. Chaque promotion, arrêt et retour arrière MUST être
audité et corrélé.

#### Scenario: Migration irréversible appliquée

- **WHEN** la révision a appliqué une migration non réversible
- **THEN** le système bloque le retour arrière non compatible et exige le plan déclaré
~~~~

