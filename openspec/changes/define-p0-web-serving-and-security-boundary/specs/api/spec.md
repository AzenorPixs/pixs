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

### Requirement: Façade web à cookie et API Bearer explicitement distinctes

Le profil local MUST déclarer une façade web à session serveur et cookie protégé inaccessible au JavaScript, avec CSRF. L’API standard et la CLI MUST conserver Authorization: Bearer avec jeton opaque du profil local. Une route Bearer MUST NOT accepter implicitement un cookie comme substitut.

#### Scenario: Cookie seul sur route Bearer
- **WHEN** un client présente uniquement un cookie sur une route Bearer
- **THEN** la route ne l’utilise pas implicitement et retourne le refus prévu

### Requirement: Contrats de transport et stockage navigateur

Routes, contrats et protections MUST indiquer leur mode d’authentification et une règle explicite pour les justificatifs ambigus sans élargir l’admission. Le navigateur MUST NOT persister de jeton accessible au JavaScript par défaut. Attributs du cookie et transport MUST être qualifiés avant code. Les exceptions Super Admin MUST rester préservées sans transformer un justificatif non vérifié en fait de confiance.

#### Scenario: Façade web authentifiée
- **WHEN** un navigateur utilise une route à session serveur
- **THEN** la session courante et les protections du cookie/CSRF sont vérifiées sans jeton persistant accessible au JavaScript

### Requirement: Limites et cache HTTP du profil P0 installable

Les routes P0 MUST déclarer formats, limites de taille/durée, concurrence et cache. Les limites d’admission MUST être vérifiées avant effet métier ; l’exécution MUST respecter son budget, avec erreur stable sans payload sensible. Les dérogations MUST suivre authorization. Une réponse sensible ou tenant-scoped MUST NOT utiliser un cache partagé implicite. Un traitement long MUST rester provisoire jusqu’à confirmation serveur.

#### Scenario: Corps de requête au-delà de la limite

- **WHEN** une requête dépasse sa limite déclarée sans dérogation applicable
- **THEN** elle est refusée avant la mutation avec l’erreur HTTP et le diagnostic minimisé déclarés

#### Scenario: Cache partagé non déclaré

- **WHEN** un intermédiaire tente de partager une réponse sensible ou tenant-scoped sans politique compatible déclarée
- **THEN** ce partage est refusé sans exposer la réponse à un autre périmètre
