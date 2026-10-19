## ADDED Requirements

### Requirement: Origines et sessions du profil P0 installable

Le profil P0 installable MUST déclarer origines, méthodes, en-têtes et credentials autorisés ; CORS MUST être refusé par défaut et une origine générique MUST NOT autoriser des credentials. Une authentification par cookie MUST activer la protection CSRF et déclarer ses attributs de sécurité. Les en-têtes d’un intermédiaire MUST NOT établir une confiance hors configuration explicite. Les exceptions applicatives MUST suivre authorization.

#### Scenario: Origine non autorisée

- **WHEN** un navigateur utilise une origine non autorisée par le profil
- **THEN** le contrôle CORS refuse cette origine sans élargir le périmètre ni divulguer une réponse protégée

#### Scenario: Mutation par cookie sans preuve CSRF

- **WHEN** une mutation protégée utilise une session par cookie sans la preuve CSRF requise et sans dérogation applicable
- **THEN** elle est refusée avant tout effet métier

#### Scenario: En-tête d’intermédiaire non fiable

- **WHEN** une requête fournit un en-tête prétendant provenir d’un intermédiaire non approuvé
- **THEN** cet en-tête ne suffit pas à établir une identité, une origine de confiance ou un droit d’accès

### Requirement: Limites et cache HTTP du profil P0 installable

Les routes P0 MUST déclarer formats, limites de taille/durée, concurrence et cache. Les limites d’admission MUST être vérifiées avant effet métier ; l’exécution MUST respecter son budget, avec erreur stable sans payload sensible. Les dérogations MUST suivre authorization. Une réponse sensible ou tenant-scoped MUST NOT utiliser un cache partagé implicite. Un traitement long MUST rester provisoire jusqu’à confirmation serveur.

#### Scenario: Corps de requête au-delà de la limite

- **WHEN** une requête dépasse sa limite déclarée sans dérogation applicable
- **THEN** elle est refusée avant la mutation avec l’erreur HTTP et le diagnostic minimisé déclarés

#### Scenario: Cache partagé non déclaré

- **WHEN** un intermédiaire tente de partager une réponse sensible ou tenant-scoped sans politique compatible déclarée
- **THEN** ce partage est refusé sans exposer la réponse à un autre périmètre
