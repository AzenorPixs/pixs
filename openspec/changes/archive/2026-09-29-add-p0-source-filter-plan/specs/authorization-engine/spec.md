# authorization-engine

## MODIFIED Requirements

### Requirement: Profil préparatoire fermé source-filter-plan-v1

Le système MUST fournir un profil nommé `source-filter-plan-v1` avec version explicite. Ce profil MUST NOT modifier le profil PDP minimal v1 existant ni les signatures existantes `authorize`, `build_snapshot`, `validate_snapshot` et ports.

Le lot d'entrée MUST être un objet immuable explicite portant sujet, action, ScopeContext, correlation et un tuple fini de `Request` homogènes. Chaque élément MUST porter un identifiant ressource et un identifiant décision uniques dans le lot, et MUST partager le même sujet, la même action, le même ScopeContext et la même correlation que l'en-tête du lot. Les candidats et le catalogue MUST être déclarés selon le profil PDP v1. Un nouveau paramètre `max_filter_requests` MUST être un entier strictement positif explicitement configuré, sans valeur par défaut inventée ; un lot à zéro demande avec en-tête valide MUST être admis.

Par ressource, l'évaluation MUST utiliser l'opération existante `authorize` avec un seul snapshot validé, les mêmes ports backend de confiance et une horloge UTC fiable capturée une seule fois pour le lot. Un résultat DENY et un fait inconnu MUST NOT devenir candidats.

Le résultat MUST être un plan déclaratif immuable lié au sujet, à l'action et au contexte, portant la version du snapshot (`epoch` plus tuple trié `policy_id` et version), `evaluated_at` UTC fiable, `resource_ids` triés et dédupliqués des seuls ALLOW, l'union dédupliquée des obligations AUDIT des seuls ALLOW, et `expires_at` égal au minimum des échéances de ces décisions. En l'absence de ALLOW, le plan MUST porter un tuple vide, des obligations vides et `expires_at` à None.

Un lot mal formé, inconnu, hétérogène, avec identifiants dupliqués, dépassant la limite, avec erreur de port ou temps non fiable MUST échouer de façon fermée sans plan contenant un identifiant autorisé ; le système MUST NOT ignorer un élément ni fournir un plan positif partiel après une erreur.

La réévaluation courante avant toute mutation et toute action sensible, ainsi que l'invalidation après tout changement de politique, ACL, rôle, appartenance, périmètre, révocation ou assurance, MUST rester obligatoires pour l'usage futur. Le plan MUST NOT être interprété comme preuve de fraîcheur au moment de l'exécution, comme jeton d'accès, ni comme preuve d'obligation AUDIT honorée. Ce profil MUST NOT effectuer de filtrage frontend ni de lecture des données métier, pagination, export ou SQL effectif.

Les exigences générales de PEP Django, de filtrage à la source et d'audit réel MUST être intégralement maintenues pour l'adaptateur futur. Seuls des tests sur ports et doubles mémoire suffisent pour ce profil ; ils MUST NOT être présentés comme preuve du P0 global.

#### Scenario: Lot mixte ALLOW et DENY

- **WHEN** un lot homogène contient des ressources dont certaines sont ALLOW et d'autres DENY par `authorize`
- **THEN** le plan ne contient que les identifiants des ressources ALLOW, triés et dédupliqués, avec l'union AUDIT des seuls ALLOW et l'échéance minimum de ces décisions

#### Scenario: Lot avec DENY seul

- **WHEN** aucune ressource du lot n'est ALLOW
- **THEN** le plan porte un tuple vide, des obligations vides et `expires_at` à None, sans identifiant autorisé

#### Scenario: Tri et déduplication

- **WHEN** les ALLOW portent des identifiants non triés
- **THEN** `resource_ids` est trié et dédupliqué

#### Scenario: Expiration minimum

- **WHEN** plusieurs ALLOW portent des échéances distinctes
- **THEN** `expires_at` est le minimum de ces échéances

#### Scenario: Hétérogénéité refusée

- **WHEN** un élément porte un sujet, une action, un contexte ou une correlation différent de l'en-tête, ou un type ou fait inconnu
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

#### Scenario: Limite dépassée

- **WHEN** le nombre de demandes dépasse `max_filter_requests`
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

#### Scenario: Booléen comme entier refusé

- **WHEN** un attribut booléen est fourni là où un entier est attendu
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

#### Scenario: Erreur backend fermée

- **WHEN** un port backend ou l'horloge échoue ou fournit un temps non fiable
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

#### Scenario: Lot vide admis

- **WHEN** un lot à zéro demande porte un en-tête valide, un snapshot validé et une limite positive configurée
- **THEN** le plan est vide avec obligations vides et `expires_at` à None
