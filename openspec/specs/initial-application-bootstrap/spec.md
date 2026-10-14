# initial-application-bootstrap Specification

## Purpose

La composition initiale définit une première application de développement
vérifiable, sans introduire de domaine métier, de fournisseur concret ni de
configuration sensible distribuée.

## Requirements

### Requirement: Composition Django initiale déclarée

L'application initiale MUST fournir un projet Django exécutable par
`manage.py` et déclarer une composition P0 conforme à
`reference-composition`. Ses réglages MUST sélectionner PostgreSQL comme
persistance de référence et charger `pixs.kernel` ainsi que `pixs.core` dans
une composition explicite. La composition MUST inclure un composant d'exemple
technique qui démontre la composition et ses contrats sans créer de domaine,
de donnée métier ou de fournisseur concret.

#### Scenario: Composition initiale valide

- **WHEN** le profil de développement valide la composition Django initiale
- **THEN** il identifie `manage.py`, PostgreSQL, `pixs.kernel`, `pixs.core` et
  le composant d'exemple P0 sans exposer de valeur sensible ni de donnée métier

### Requirement: Configuration sensible de la composition Django initiale

Les paramètres de connexion
PostgreSQL et toute valeur sensible MUST provenir de la configuration runtime
ou de références de secrets ; ils MUST NOT être codés dans le dépôt, les
réglages distribués ou les artefacts de test.

#### Scenario: Connexion fournie par configuration runtime

- **WHEN** la composition Django initiale reçoit ses paramètres PostgreSQL et valeurs sensibles
- **THEN** ils proviennent de la configuration runtime ou de références de secrets sans être codés dans les sources, réglages distribués ou artefacts de test

### Requirement: Surface HTTP initiale minimale

L'application initiale MUST déclarer des routes et des vues de base séparant
la vérification de santé du shell et de l'API versionnée. Toute route publique
MUST être explicitement déclarée ; toute route non déclarée publique MUST être
protégée ou refusée. Les réponses API initiales MUST respecter les contrats
HTTP publics applicables et MUST NOT simuler une capacité métier, une
autorisation ou une identité inexistante.

#### Scenario: Route initiale non déclarée

- **WHEN** une requête vise une route qui n'est ni une route de santé, ni une
  route du shell, ni une route API explicitement déclarée
- **THEN** l'application la refuse avec une réponse sans information sensible

### Requirement: Shell TanStack initial intégré

Le frontend initial MUST fournir un shell TanStack construit séparément et
servi par la composition de développement déclarée. Le shell MUST consommer
uniquement la surface HTTP publique déclarée et MUST NOT accéder directement à
PostgreSQL, aux secrets, aux réglages Django privés ou aux implémentations
internes de `pixs.kernel` et `pixs.core`.

#### Scenario: Démarrage du shell initial

- **WHEN** la composition de développement démarre avec le frontend initial
- **THEN** le shell est accessible et ses appels utilisent exclusivement les
  routes HTTP déclarées

### Requirement: Profil de test intégré isolé

Le projet MUST déclarer un profil de test local permettant de vérifier le
backend Django et le shell TanStack ensemble. Ce profil MUST expliciter les
dépendances nécessaires, l'adresse d'écoute, les capacités absentes et son
cycle de démarrage et d'arrêt ; il MUST NOT être présenté comme un déploiement
de production, initialiser des données métier permanentes ou élargir les
frontières de sécurité.

#### Scenario: Vérification locale conjointe

- **WHEN** le profil de test local est lancé avec une configuration valide
- **THEN** il permet de vérifier la santé, l'accès au shell et une réponse API
  déclarée sans dépendance de production ni secret
