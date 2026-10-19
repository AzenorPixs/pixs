# Références normatives — N04

Les références ci-dessous restent canoniques. Les blocs sont des sources de traçabilité, sans synchronisation ou copie normative concurrente. Les deltas propres au dossier, s’il en contient, restent proposés.

## reference-runtime #1

[Source canonique](../../specs/reference-runtime/spec.md#L10) ; SHA-256 source `4bbbc0451013b7139f3898b4a5aebd592ab1c50b6aa6cce4e1246957e4052351`.

### Requirement: Pile de référence unique

Le runtime applicatif PBO/PFO MUST utiliser Django pour l’autorité métier, PostgreSQL comme source de vérité et TanStack comme frontend de référence. L’agnosticisme MUST concerner domaines, contrats, providers et intégrations et MUST NOT promettre l’interchangeabilité immédiate de cette pile. Les binaires PA et le module essentiel PZT MUST respecter leurs exigences distinctes de cette capacité.

#### Scenario: Runtime décrit

- **WHEN** une release décrit PBO/PFO et les binaires PA
- **THEN** elle identifie Django/PostgreSQL/TanStack pour PBO/PFO et les fonctions locales PA séparément

#### Scenario: Réseau désactivé

- **WHEN** une composition PBO désactive l’exécution réseau PZT
- **THEN** le module essentiel de configuration et de supervision reste composé

## reference-runtime #3

[Source canonique](../../specs/reference-runtime/spec.md#L35) ; SHA-256 source `4bbbc0451013b7139f3898b4a5aebd592ab1c50b6aa6cce4e1246957e4052351`.

### Requirement: Absence de sélection cachée

Le build et le runtime MUST NOT sélectionner une pile alternative selon
l'environnement, l'ordre des imports ou la présence d'un paquet.

#### Scenario: Paquet alternatif présent

- **WHEN** un paquet d'un autre backend est présent dans l'artefact
- **THEN** il ne change pas le runtime effectif sans sélection explicite

## runtime #1

[Source canonique](../../specs/runtime/spec.md#L8) ; SHA-256 source `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

### Requirement: Profils distincts d'un même artefact

Les rôles web, worker et scheduler MUST être des profils d'un même artefact activés par configuration explicite, sans branche fonctionnelle cachée ; le développement peut les regrouper, la production MUST pouvoir les exécuter séparément.

#### Scenario: Profil activé par configuration

- **WHEN** un déploiement produit un worker et un scheduler à partir du même artefact
- **THEN** leurs capacités et limites respectives sont inspectables sans code divergent

## runtime #3

[Source canonique](../../specs/runtime/spec.md#L29) ; SHA-256 source `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

### Requirement: Exposition minimale par défaut

Seul le profil web MUST être exposé à l'entrée publique par défaut ; workers, schedulers, files, stores de coordination et endpoints de management MUST rester sur un réseau privé ou derrière une frontière authentifiée, autorisée et auditée.

#### Scenario: Endpoint de management publiquement joignable

- **WHEN** un endpoint de management se retrouve atteignable depuis le trafic public sans frontière explicite
- **THEN** la composition est déclarée invalide et l'exposition est refusée

## runtime #6

[Source canonique](../../specs/runtime/spec.md#L61) ; SHA-256 source `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

### Requirement: Arrêt, drain et reprise contrôlés

L'arrêt MUST être contrôlé : cesser l'exposition, drainer les traitements en cours dans une durée bornée puis s'éteindre sur un état explicite ; une instance défaillante MUST NOT recevoir de trafic.

#### Scenario: Arrêt pendant traitement

- **WHEN** une instance reçoit un signal d'arrêt pendant un traitement engagé
- **THEN** elle termine ou restitue le traitement selon son contrat et atteint un état final sans perte silencieuse

## api #2

[Source canonique](../../specs/api/spec.md#L18) ; SHA-256 source `58abd35620d8a6e9c65b0f525e8afda12a2291b9a531bba9248643be3afd3152`.

### Requirement: Contrats OpenAPI versionnés par majeure

Chaque capacité exposée MUST disposer d'un contrat OpenAPI publié et versionné ; la majeure figure dans le chemin, les évolutions compatibles conservent l'URL, toute rupture impose une nouvelle majeure avec coexistence déclarée.

#### Scenario: Rupture sans nouvelle majeure bloquée

- **WHEN** une évolution incompatible conserve la même majeure
- **THEN** le build refuse la publication du contrat

## api #3

[Source canonique](../../specs/api/spec.md#L27) ; SHA-256 source `58abd35620d8a6e9c65b0f525e8afda12a2291b9a531bba9248643be3afd3152`.

### Requirement: Enveloppes stables et erreurs typées

Le système MUST respecter les garanties suivantes.

Les succès utilisent données, métadonnées et liens avec pagination par curseur ; les erreurs suivent un code métier versionné, un message, des détails et un identifiant de corrélation, sans secret ni trace interne ; les commandes rejouables portent une clé d'idempotence.

#### Scenario: Rejou identique restitué

- **WHEN** la même clé d'idempotence est rejouée avec un contenu identique
- **THEN** le résultat enregistré est restitué au lieu d'un double effet

## api #4

[Source canonique](../../specs/api/spec.md#L38) ; SHA-256 source `58abd35620d8a6e9c65b0f525e8afda12a2291b9a531bba9248643be3afd3152`.

### Requirement: Périmètre canonique et autorisation à la frontière

Le système MUST respecter les garanties suivantes.

Les ressources de périmètre exposent le tenant dans le chemin et vérifient l'appartenance avant lecture ou mutation ; l'authentification Bearer reste le mode privilégié et tout accès anonyme est explicitement déclaré public.

#### Scenario: Tenant d'en-tête non canonique rejeté

- **WHEN** un client fournit le tenant hors chemin canonique en contradiction avec le contexte
- **THEN** la requête est refusée avec une erreur stable

## initial-application-bootstrap #3

[Source canonique](../../specs/initial-application-bootstrap/spec.md#L39) ; SHA-256 source `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.

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

## initial-application-bootstrap #4

[Source canonique](../../specs/initial-application-bootstrap/spec.md#L54) ; SHA-256 source `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.

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

## initial-application-bootstrap #5

[Source canonique](../../specs/initial-application-bootstrap/spec.md#L68) ; SHA-256 source `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.

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

## security #1

[Source canonique](../../specs/security/spec.md#L8) ; SHA-256 source `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

### Requirement: Exception applicative réservée au Super Admin

Les contrôles applicatifs de sécurité MUST s'appliquer sous réserve de l'exception Super Admin définie par `authorization`. Le compte MUST conserver l'authentification propre définie par `initial-administration`. Un rôle, un drapeau client ou une revendication d'identifiant MUST NOT suffire à reconnaître ce compte ni donner l'exception à une autre identité.

#### Scenario: Revendication root sans authentification propre

- **WHEN** un autre compte ou un client se déclare Super Admin sans authentifier le compte fonctionnel concerné
- **THEN** l'exception est refusée et les contrôles ordinaires restent applicables

## security #3

[Source canonique](../../specs/security/spec.md#L26) ; SHA-256 source `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

### Requirement: Échec fermé sans mode permissif

Le système MUST respecter les garanties suivantes.

Toute authentification, autorisation, signature, secret ou contexte non vérifiable produit un échec fermé ; aucun bascule automatique vers un mode permissif pour préserver la disponibilité.

#### Scenario: Contexte non vérifiable refusé

- **WHEN** un contrôle de sécurité ne peut être vérifié
- **THEN** l'opération est refusée et l'événement est diagnostiqué et audité

## security #4

[Source canonique](../../specs/security/spec.md#L37) ; SHA-256 source `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

### Requirement: Diagnostics sans exposition sensible

Les journaux, diagnostics et inventaires MUST NOT exposer de secret, de jeton ni de donnée personnelle ; révocations, blocages et réactivations restent diagnostiquables et auditables.

#### Scenario: Secret hors journaux

- **WHEN** un diagnostic est produit après un échec de sécurité
- **THEN** il identifie le composant et la cause sans divulguer de valeur sensible

