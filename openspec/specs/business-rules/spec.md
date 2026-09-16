# business-rules Specification

## Purpose

Le moteur de règles métier fournit des décisions déclaratives, versionnées et
testables, distinctes de l'autorisation et de l'orchestration de workflows.

## Requirements

### Requirement: Règles métier séparées des contrôles de sécurité

Une règle métier MUST déclarer son propriétaire, son contrat d'entrée, son
résultat et son contexte de version. Elle MUST NOT accorder une permission,
remplacer une décision du PDP ou contourner une garde de workflow.

#### Scenario: Règle invoquée pour une action protégée

- **WHEN** une règle recommande qu'une action soit applicable
- **THEN** l'autorisation et les gardes de workflow sont évaluées séparément

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

### Requirement: Effets appliqués par le propriétaire métier

Une évaluation de règle MUST produire une décision ou une proposition
structurée. Toute mutation consécutive MUST passer par une Command autorisée du
module propriétaire ; le moteur de règles MUST NOT écrire directement des
modèles ou données d'un autre composant.

#### Scenario: Décision conduisant à une mutation

- **WHEN** une règle produit une décision de transition métier
- **THEN** le module propriétaire la valide au travers de sa Command publique

### Requirement: Tests, explications et audit

Chaque règle stable MUST disposer de cas de test versionnés. Le système MUST
conserver une explication corrélée de l'évaluation sans enregistrer de secret,
de donnée non nécessaire ou de détail privé de l'implémentation.

#### Scenario: Décision contestée

- **WHEN** un opérateur autorisé consulte une décision tracée
- **THEN** il obtient la version de règle et les motifs autorisés sans exposer le contexte sensible complet
