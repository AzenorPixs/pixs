# Références normatives — O06

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| business-rules / 10 | [Règles métier séparées des contrôles de sécurité](../../specs/business-rules/spec.md#L10) | NE | AUDIT_AVANT_CREATION |
| business-rules / 21 | [Déclarations versionnées et déterministes](../../specs/business-rules/spec.md#L21) | NE | AUDIT_AVANT_CREATION |
| business-rules / 39 | [Effets appliqués par le propriétaire métier](../../specs/business-rules/spec.md#L39) | NE | AUDIT_AVANT_CREATION |
| business-rules / 51 | [Tests, explications et audit](../../specs/business-rules/spec.md#L51) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence business-rules--614c26548e

Source : `openspec/specs/business-rules/spec.md`, ligne 10. SHA-256 du bloc : `c043f03b3acc0e71b58aa51b1eac41f0d2beaeadae518e091ba56f8b8bfa537f`.

~~~~text
### Requirement: Règles métier séparées des contrôles de sécurité

Une règle métier MUST déclarer son propriétaire, son contrat d'entrée, son
résultat et son contexte de version. Elle MUST NOT accorder une permission,
remplacer une décision du PDP ou contourner une garde de workflow.

#### Scenario: Règle invoquée pour une action protégée

- **WHEN** une règle recommande qu'une action soit applicable
- **THEN** l'autorisation et les gardes de workflow sont évaluées séparément
~~~~

### Référence business-rules--3f25b21925

Source : `openspec/specs/business-rules/spec.md`, ligne 21. SHA-256 du bloc : `7bfa00e30ff6d5cd97e04ea351c6e15461502bfe7e1a35a8e3ab6a853964e63b`.

~~~~text
### Requirement: Déclarations versionnées et déterministes

Les règles, tables de décision et dépendances déclarées MUST être versionnées,
validées et évaluées de manière déterministe pour une même entrée et une même
version. Leur DSL MUST être déclaratif et restreint ; une règle MUST NOT
évaluer du code arbitraire au runtime. Une règle ambiguë, incomplète ou
incompatible MUST être refusée avant activation.

#### Scenario: Évaluation rejouée

- **WHEN** une même règle reçoit deux fois le même contexte versionné
- **THEN** elle produit le même résultat ou le même refus explicite

#### Scenario: Expression exécutable proposée

- **WHEN** une règle contient du code ou une expression exécutable non déclarée par le DSL
- **THEN** sa validation échoue avant activation
~~~~

### Référence business-rules--2b5c643b97

Source : `openspec/specs/business-rules/spec.md`, ligne 39. SHA-256 du bloc : `9f6e489333cfc72c6d1e21ff85d237c9f01c7a28f1eb8291233938c2240b4152`.

~~~~text
### Requirement: Effets appliqués par le propriétaire métier

Une évaluation de règle MUST produire une décision ou une proposition
structurée. Toute mutation consécutive MUST passer par une Command autorisée du
module propriétaire ; le moteur de règles MUST NOT écrire directement des
modèles ou données d'un autre composant.

#### Scenario: Décision conduisant à une mutation

- **WHEN** une règle produit une décision de transition métier
- **THEN** le module propriétaire la valide au travers de sa Command publique
~~~~

### Référence business-rules--40aa442ec2

Source : `openspec/specs/business-rules/spec.md`, ligne 51. SHA-256 du bloc : `e7e05cdac29ea36b86544c7cc730756ac6dc8f5ce060a936e1cd7232edf6c8b4`.

~~~~text
### Requirement: Tests, explications et audit

Chaque règle stable MUST disposer de cas de test versionnés. Le système MUST
conserver une explication corrélée de l'évaluation sans enregistrer de secret,
de donnée non nécessaire ou de détail privé de l'implémentation.

#### Scenario: Décision contestée

- **WHEN** un opérateur autorisé consulte une décision tracée
- **THEN** il obtient la version de règle et les motifs autorisés sans exposer le contexte sensible complet
~~~~

