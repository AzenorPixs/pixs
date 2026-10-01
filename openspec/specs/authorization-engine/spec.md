# authorization-engine Specification

## Purpose
Le moteur d'autorisation décide de façon déclarative, déterministe et bornée, avec filtrage autorisé, cohérence de cache et échec fermé.

## Requirements

### Requirement: Politiques déclaratives versionnées

Chaque politique MUST déclarer identifiant, version, propriétaire, effet DENY ou ALLOW, sélecteurs de sujets, ressources, actions et périmètres, conditions typées, obligations et validité, sans code arbitraire ni expression distante.

#### Scenario: Politique à code rejetée

- **WHEN** une politique embarque du code exécutable ou une expression distante
- **THEN** elle est refusée avant activation

### Requirement: Décisions et filtrage tracés

Le système MUST respecter les garanties suivantes.

Le contrat de décision retourne effet, motif fonctionnel, version de politique et échéance ; le filtrage autorisé traduit la décision en contrainte source avant pagination ou export ; les décisions positives expirent et sont invalidées après tout changement de politique, ACL, rôle, appartenance, périmètre, révocation ou assurance.

#### Scenario: Décision périmée non réutilisée

- **WHEN** une mutation invoque une décision antérieure à un changement de politique
- **THEN** la politique courante est réévaluée avant toute exécution

### Requirement: Groupes bornés et délégation auditée

Le système MUST respecter les garanties suivantes.

Les groupes imbriqués restent acycliques et bornés ; toute délégation, usurpation ou élévation est explicitement accordée, limitée en temps et périmètre, soumise à l'assurance requise et auditée ; l'indisponibilité du moteur échoue fermé pour mutations et données protégées.

#### Scenario: Moteur indisponible

- **WHEN** le moteur ne peut être joint pour une mutation sensible
- **THEN** l'opération est refusée au lieu d'une autorisation implicite

### Requirement: Profil PDP minimal fermé v1

Le système MUST respecter les garanties suivantes.

Le profil minimal v1 nomme explicitement sa version. Les sélecteurs MUST utiliser l'égalité ou des ensembles finis d'identifiants canoniques déclarés, sans wildcard, préfixe, héritage implicite ni code ; les appartenances sont évaluées uniquement comme faits vérifiés fournis.

Les conditions sont conjonctives, fermées et typées avec opérateurs eq et in sur attributs déclarés, sans booléen assimilé à un entier ; les seuils minimum portent sur chacune des trois dimensions exactes identity_assurance CLAIMED | VERIFIED | PROOFED, authentication_assurance SINGLE_FACTOR | MULTI_FACTOR | PHISHING_RESISTANT et federation_trust UNTRUSTED | TRUSTED | STRONGLY_BOUND, avec ordres indiqués et sans substitution entre dimensions ; la fraîcheur maximale est vérifiée ; tout type, attribut ou fait requis inconnu ou absent MUST être refusé avec effet DENY. Les limites positives de tailles et coûts sont configurées et validées, sans valeur par défaut non spécifiée.

La seule obligation du profil minimal est AUDIT sous forme déclarative normalisée et dédupliquée ; toute obligation inconnue et toute politique mal formée MUST être rejetées avant activation. Un ALLOW du PDP MUST NOT valoir accès avant que le PEP ait honoré les obligations ; l'union porte sur les obligations des ALLOW APPLICABLES uniquement et un ALLOW ne dispense jamais l'audit d'un refus.

Le snapshot utilise une epoch globale et des tuples policy_id et version triés, sans maximum de versions indépendantes. L'évaluation MUST suivre DENY prioritaire puis ALLOW puis refus, avec union déterministe des obligations des ALLOW APPLICABLES.

Le temps est UTC fiable injecté avec intervalles semi-ouverts [from, until). L'expires_at d'un ALLOW est le minimum de now plus TTL positif configuré, expiration de l'AuthenticationContext, limite de fraîcheur auth_time plus âge maximal requis, et prochaine transition future pouvant modifier le résultat, notamment début futur d'un DENY autrement correspondant ou fin d'un ALLOW ; la borne temporelle MUST NOT se limiter aux politiques actuellement actives et MUST inclure les politiques autrement correspondantes dont valid_from futur peut changer la décision. Expiration, temps naïf, non fiable ou contradictoire, et révocation inconnue produisent un refus fermé. Toute mutation ET toute action sensible sont réévaluées.

Les AuthenticationContext proviennent exclusivement de la chaîne backend de confiance ; aucun booléen client verified ne suffit comme preuve ; fraîcheur, révocation et périmètre sont vérifiés et l'inconnu est refusé. Les codes publics sont fermés et minimaux ALLOWED et DENIED, les diagnostics détaillés restant réservés aux diagnostics autorisés ; tout refus est audité sans simuler un PEP effectif. Tout accès plateforme exige contexte, politique et audit explicites ; l'intertenant est refusé dans le profil minimal seulement et reste permis par le contrat général explicite.

#### Scenario: ALLOW minimal avec obligation honorée

- **WHEN** une politique ALLOW du profil v1 correspond et que le PEP honore l'obligation AUDIT
- **THEN** l'accès est autorisé avec le code public ALLOWED et l'audit correspondant

#### Scenario: Sélecteur générique refusé

- **WHEN** une politique déclare un wildcard, un préfixe ou un héritage implicite
- **THEN** elle est refusée avant activation

#### Scenario: Fait inconnu refusé fermé

- **WHEN** une condition exige un attribut, un type ou un fait d'assurance absent ou inconnu
- **THEN** la décision est d'effet DENY avec le code public DENIED et un audit

#### Scenario: Obligation inconnue rejetée

- **WHEN** une politique déclare une obligation autre que AUDIT
- **THEN** elle est rejetée avant activation

#### Scenario: Intertenant minimal refusé

- **WHEN** une demande intertenant est évaluée par le profil minimal v1
- **THEN** elle est refusée avec audit sans préjuger du contrat général explicite

#### Scenario: DENY prévaut sur ALLOW mêmes cibles

- **WHEN** un DENY et un ALLOW du profil v1 couvrent les mêmes cibles
- **THEN** la décision est d'effet DENY avec le code public DENIED

#### Scenario: ALLOW expire à activation future DENY

- **WHEN** un DENY autrement correspondant débute après l'évaluation d'un ALLOW
- **THEN** l'expires_at de l'ALLOW est borné par ce début futur et la décision ultérieure est réévaluée

#### Scenario: Auth expirée malgré TTL

- **WHEN** l'AuthenticationContext expire avant now plus TTL
- **THEN** l'expires_at est borné par cette expiration et le dépassement est refusé

#### Scenario: Assurances non substituables

- **WHEN** une condition exige un niveau d'une dimension d'assurance
- **THEN** aucun niveau d'une autre dimension ne peut y satisfaire

#### Scenario: Booléen client insuffisant

- **WHEN** un drapeau client verified est fourni sans chaîne backend de confiance
- **THEN** la décision est refusée

#### Scenario: Plateforme ALLOW explicite

- **WHEN** un accès plateforme dispose d'un contexte, d'une politique et d'un audit explicites
- **THEN** il peut être autorisé avec le code public ALLOWED

#### Scenario: Plateforme sans explicite refusée

- **WHEN** un accès plateforme manque de contexte, de politique ou d'audit explicite
- **THEN** il est refusé avec audit

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
