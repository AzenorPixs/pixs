# authorization-engine Specification

## Purpose
Le moteur d'autorisation décide de façon déclarative, déterministe et bornée, avec filtrage autorisé, cohérence de cache et échec fermé.

## Requirements

### Requirement: Exception Super Admin distincte des profils préparatoires

Le traitement applicatif du Super Admin MUST suivre `authorization` et rester distinct du PDP minimal v1 et de `source-filter-plan-v1`. L'exception MUST NOT modifier leurs signatures, sélecteurs, obligations ou résultats. Une décision ou un plan préparatoire MUST NOT être présenté comme une preuve de reconnaissance du compte Super Admin ou de sa dérogation.

#### Scenario: Profils préparatoires sans privilège ajouté

- **WHEN** un profil PDP minimal v1 ou source-filter-plan-v1 reçoit ses entrées habituelles
- **THEN** il conserve ses règles et résultats sans interpréter un rôle ou un identifiant comme un privilège Super Admin

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

Le système MUST respecter les garanties suivantes. Le profil minimal v1 nomme explicitement sa version. Les sélecteurs MUST utiliser l'égalité ou des ensembles finis d'identifiants canoniques déclarés, sans wildcard, préfixe, héritage implicite ni code ; les appartenances sont évaluées uniquement comme faits vérifiés fournis.

#### Scenario: Sélecteur générique refusé

- **WHEN** une politique déclare un wildcard, un préfixe ou un héritage implicite
- **THEN** elle est refusée avant activation

### Requirement: Conditions typées du profil PDP minimal fermé v1

Dans le profil PDP minimal v1, le système MUST respecter les garanties suivantes.

Les conditions sont conjonctives, fermées et typées avec opérateurs eq et in sur attributs déclarés, sans booléen assimilé à un entier.

#### Scenario: Booléen distinct d'un entier

- **WHEN** une condition du profil PDP minimal v1 attend un entier mais reçoit un booléen
- **THEN** le type n'est pas accepté comme un entier

### Requirement: Assurances et faits du profil PDP minimal fermé v1

Les seuils minimum portent sur chacune des trois dimensions exactes identity_assurance CLAIMED | VERIFIED | PROOFED, authentication_assurance SINGLE_FACTOR | MULTI_FACTOR | PHISHING_RESISTANT et federation_trust UNTRUSTED | TRUSTED | STRONGLY_BOUND, avec ordres indiqués et sans substitution entre dimensions ; la fraîcheur maximale est vérifiée ; tout type, attribut ou fait requis inconnu ou absent MUST être refusé avec effet DENY.

#### Scenario: Fait inconnu refusé fermé

- **WHEN** une condition exige un attribut, un type ou un fait d'assurance absent ou inconnu
- **THEN** la décision est d'effet DENY avec le code public DENIED et un audit

#### Scenario: Assurances non substituables

- **WHEN** une condition exige un niveau d'une dimension d'assurance
- **THEN** aucun niveau d'une autre dimension ne peut y satisfaire

### Requirement: Limites et obligations du profil PDP minimal fermé v1

Les limites positives de tailles et coûts sont configurées et validées, sans valeur par défaut non spécifiée. La seule obligation du profil minimal est AUDIT sous forme déclarative normalisée et dédupliquée ; toute obligation inconnue et toute politique mal formée MUST être rejetées avant activation.

#### Scenario: Obligation inconnue rejetée

- **WHEN** une politique déclare une obligation autre que AUDIT
- **THEN** elle est rejetée avant activation

### Requirement: Obligations honorées par le PEP du profil PDP minimal fermé v1

Un ALLOW du PDP MUST NOT valoir accès avant que le PEP ait honoré les obligations ; l'union porte sur les obligations des ALLOW APPLICABLES uniquement et un ALLOW ne dispense jamais l'audit d'un refus.

#### Scenario: ALLOW minimal avec obligation honorée

- **WHEN** une politique ALLOW du profil v1 correspond et que le PEP honore l'obligation AUDIT
- **THEN** l'accès est autorisé avec le code public ALLOWED et l'audit correspondant

### Requirement: Snapshot et priorité du profil PDP minimal fermé v1

Le snapshot utilise une epoch globale et des tuples policy_id et version triés, sans maximum de versions indépendantes. L'évaluation MUST suivre DENY prioritaire puis ALLOW puis refus, avec union déterministe des obligations des ALLOW APPLICABLES.

#### Scenario: DENY prévaut sur ALLOW mêmes cibles

- **WHEN** un DENY et un ALLOW du profil v1 couvrent les mêmes cibles
- **THEN** la décision est d'effet DENY avec le code public DENIED

### Requirement: Calcul d'expiration du profil PDP minimal fermé v1

Dans le profil PDP minimal v1, le système MUST respecter les garanties suivantes.

Le temps est UTC fiable injecté avec intervalles semi-ouverts [from, until). L'expires_at d'un ALLOW est le minimum de now plus TTL positif configuré, expiration de l'AuthenticationContext, limite de fraîcheur auth_time plus âge maximal requis, et prochaine transition future pouvant modifier le résultat, notamment début futur d'un DENY autrement correspondant ou fin d'un ALLOW.

#### Scenario: Auth expirée malgré TTL

- **WHEN** l'AuthenticationContext expire avant now plus TTL
- **THEN** l'expires_at est borné par cette expiration et le dépassement est refusé

### Requirement: Transitions temporelles et réévaluation du profil PDP minimal fermé v1

La borne temporelle MUST NOT se limiter aux politiques actuellement actives et MUST inclure les politiques autrement correspondantes dont valid_from futur peut changer la décision. Expiration, temps naïf, non fiable ou contradictoire, et révocation inconnue produisent un refus fermé. Toute mutation ET toute action sensible sont réévaluées.

#### Scenario: ALLOW expire à activation future DENY

- **WHEN** un DENY autrement correspondant débute après l'évaluation d'un ALLOW
- **THEN** l'expires_at de l'ALLOW est borné par ce début futur et la décision ultérieure est réévaluée

### Requirement: Confiance backend et diagnostics du profil PDP minimal fermé v1

Dans le profil PDP minimal v1, le système MUST respecter les garanties suivantes.

Les AuthenticationContext proviennent exclusivement de la chaîne backend de confiance ; aucun booléen client verified ne suffit comme preuve ; fraîcheur, révocation et périmètre sont vérifiés et l'inconnu est refusé. Les codes publics sont fermés et minimaux ALLOWED et DENIED, les diagnostics détaillés restant réservés aux diagnostics autorisés ; tout refus est audité sans simuler un PEP effectif.

#### Scenario: Booléen client insuffisant

- **WHEN** un drapeau client verified est fourni sans chaîne backend de confiance
- **THEN** la décision est refusée

### Requirement: Plateforme et intertenant du profil PDP minimal fermé v1

Dans le profil PDP minimal v1, le système MUST respecter les garanties suivantes.

Tout accès plateforme exige contexte, politique et audit explicites ; l'intertenant est refusé dans le profil minimal seulement et reste permis par le contrat général explicite.

#### Scenario: Intertenant minimal refusé

- **WHEN** une demande intertenant est évaluée par le profil minimal v1
- **THEN** elle est refusée avec audit sans préjuger du contrat général explicite

#### Scenario: Plateforme ALLOW explicite

- **WHEN** un accès plateforme dispose d'un contexte, d'une politique et d'un audit explicites
- **THEN** il peut être autorisé avec le code public ALLOWED

#### Scenario: Plateforme sans explicite refusée

- **WHEN** un accès plateforme manque de contexte, de politique ou d'audit explicite
- **THEN** il est refusé avec audit

### Requirement: Profil préparatoire fermé source-filter-plan-v1

Le système MUST fournir un profil nommé `source-filter-plan-v1` avec version explicite. Ce profil MUST NOT modifier le profil PDP minimal v1 existant ni les signatures existantes `authorize`, `build_snapshot`, `validate_snapshot` et ports.

#### Scenario: Profil de filtrage sans rupture du PDP

- **WHEN** le profil source-filter-plan-v1 est fourni
- **THEN** sa version est explicite et les signatures existantes du PDP restent inchangées

### Requirement: Entrées homogènes de source-filter-plan-v1

Le lot d'entrée MUST être un objet immuable explicite portant sujet, action, ScopeContext, correlation et un tuple fini de `Request` homogènes. Chaque élément MUST porter un identifiant ressource et un identifiant décision uniques dans le lot, et MUST partager le même sujet, la même action, le même ScopeContext et la même correlation que l'en-tête du lot. Les candidats et le catalogue MUST être déclarés selon le profil PDP v1.

#### Scenario: Hétérogénéité refusée

- **WHEN** un élément porte un sujet, une action, un contexte ou une correlation différent de l'en-tête, ou un type ou fait inconnu
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

### Requirement: Limite explicite et lot vide de source-filter-plan-v1

Un nouveau paramètre `max_filter_requests` MUST être un entier strictement positif explicitement configuré, sans valeur par défaut inventée ; un lot à zéro demande avec en-tête valide MUST être admis.

#### Scenario: Limite dépassée

- **WHEN** le nombre de demandes dépasse `max_filter_requests`
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

#### Scenario: Lot vide admis

- **WHEN** un lot à zéro demande porte un en-tête valide, un snapshot validé et une limite positive configurée
- **THEN** le plan est vide avec obligations vides et `expires_at` à None

### Requirement: Évaluation par ressource de source-filter-plan-v1

Par ressource, l'évaluation MUST utiliser l'opération existante `authorize` avec un seul snapshot validé, les mêmes ports backend de confiance et une horloge UTC fiable capturée une seule fois pour le lot. Un résultat DENY et un fait inconnu MUST NOT devenir candidats.

#### Scenario: Lot mixte ALLOW et DENY

- **WHEN** un lot homogène contient des ressources dont certaines sont ALLOW et d'autres DENY par `authorize`
- **THEN** le plan ne contient que les identifiants des ressources ALLOW, triés et dédupliqués, avec l'union AUDIT des seuls ALLOW et l'échéance minimum de ces décisions

### Requirement: Résultat déclaratif de source-filter-plan-v1

Le résultat MUST être un plan déclaratif immuable lié au sujet, à l'action et au contexte, portant la version du snapshot (`epoch` plus tuple trié `policy_id` et version), `evaluated_at` UTC fiable, `resource_ids` triés et dédupliqués des seuls ALLOW, l'union dédupliquée des obligations AUDIT des seuls ALLOW, et `expires_at` égal au minimum des échéances de ces décisions. En l'absence de ALLOW, le plan MUST porter un tuple vide, des obligations vides et `expires_at` à None.

#### Scenario: Lot avec DENY seul

- **WHEN** aucune ressource du lot n'est ALLOW
- **THEN** le plan porte un tuple vide, des obligations vides et `expires_at` à None, sans identifiant autorisé

#### Scenario: Tri et déduplication

- **WHEN** les ALLOW portent des identifiants non triés
- **THEN** `resource_ids` est trié et dédupliqué

#### Scenario: Expiration minimum

- **WHEN** plusieurs ALLOW portent des échéances distinctes
- **THEN** `expires_at` est le minimum de ces échéances

### Requirement: Échec fermé du lot de source-filter-plan-v1

Un lot mal formé, inconnu, hétérogène, avec identifiants dupliqués, dépassant la limite, avec erreur de port ou temps non fiable MUST échouer de façon fermée sans plan contenant un identifiant autorisé ; le système MUST NOT ignorer un élément ni fournir un plan positif partiel après une erreur.

#### Scenario: Booléen comme entier refusé

- **WHEN** un attribut booléen est fourni là où un entier est attendu
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

#### Scenario: Erreur backend fermée

- **WHEN** un port backend ou l'horloge échoue ou fournit un temps non fiable
- **THEN** le lot échoue de façon fermée sans plan contenant un identifiant autorisé

### Requirement: Fraîcheur et invalidation de source-filter-plan-v1

La réévaluation courante avant toute mutation et toute action sensible, ainsi que l'invalidation après tout changement de politique, ACL, rôle, appartenance, périmètre, révocation ou assurance, MUST rester obligatoires pour l'usage futur. Le plan MUST NOT être interprété comme preuve de fraîcheur au moment de l'exécution, comme jeton d'accès, ni comme preuve d'obligation AUDIT honorée.

#### Scenario: Plan distinct d'une autorisation courante

- **WHEN** une intégration future utilise un plan avant une mutation ou une action sensible
- **THEN** elle réévalue l'autorisation courante et ne traite pas le plan comme un jeton d'accès ou une preuve d'AUDIT honorée

### Requirement: Frontières préparatoires de source-filter-plan-v1

Ce profil MUST NOT effectuer de filtrage frontend ni de lecture des données métier, pagination, export ou SQL effectif. Les exigences générales de PEP Django, de filtrage à la source et d'audit réel MUST être intégralement maintenues pour l'adaptateur futur. Seuls des tests sur ports et doubles mémoire suffisent pour ce profil ; ils MUST NOT être présentés comme preuve du P0 global.

#### Scenario: Doubles mémoire sans preuve de P0

- **WHEN** le profil source-filter-plan-v1 est vérifié sur ports et doubles mémoire
- **THEN** ces tests ne prouvent ni P0 global ni filtrage SQL effectif et les obligations de l'adaptateur futur restent applicables

### Requirement: Structure préparatoire AuditDecisionProjectionV1

Le Core MUST définir AuditDecisionProjectionV1 comme une représentation mémoire immuable à slots avec exactement decision_event et audit_event, tous deux explicites sans défaut. Les objets MUST être conservés par identité, sans copie, conversion ni normalisation. Le Kernel MUST rester indépendant du PDP.

#### Scenario: Deux objets originaux conservés

- **WHEN** un appelant de confiance fournit les deux événements exacts
- **THEN** la représentation conserve les mêmes objets et ne produit aucun événement


### Requirement: Types exacts des événements de la projection audit v1

decision_event MUST être un pixs.core.authz.ports.AuditEvent exact et audit_event un pixs.kernel.audit_event.AuditEvent exact. Le profil et ses objets imbriqués MUST être contrôlés par type exact avant accès aux attributs étrangers. bool, sous-classes et objets hostiles MUST être refusés sans appel à leurs méthodes.

#### Scenario: Objets étrangers refusés avant accès

- **WHEN** un objet étranger ou une sous-classe est fourni à la place du profil ou de ses événements
- **THEN** il est refusé sans accès à ses attributs ni appel à ses méthodes


### Requirement: Sous-ensemble PDP complet de la projection audit v1

decision_id, subject_id, resource_id, action_id et correlation_id MUST être des str exactes non vides, opaques et non normalisées. context MUST être un ScopeContext exact validé par validate_structure sur le même objet. Toute donnée incomplète MUST être refusée sans placeholder ni résolution de référence.

#### Scenario: Décision incomplète refusée

- **WHEN** un identifiant requis est absent, vide ou de type interdit, ou le contexte est absent ou structurellement invalide
- **THEN** la validation refuse la projection sans fabriquer la donnée manquante


### Requirement: Effet et motif cohérents de la projection audit v1

effect MUST être un membre exact de Effect. reason_code MUST être une str exacte égale à ALLOWED pour Effect.ALLOW et DENIED pour Effect.DENY. La projection MUST conserver les valeurs et les résultats des contrats PDP existants.

#### Scenario: Deux correspondances fermées

- **WHEN** la décision porte ALLOW/ALLOWED ou DENY/DENIED
- **THEN** la paire est admissible sans modifier la décision

#### Scenario: Motif incohérent refusé

- **WHEN** le motif ne correspond pas exactement à son effet
- **THEN** la projection est refusée sans coercition


### Requirement: Version de politique et instant explicites de la projection audit v1

policy_version MUST être un tuple exact non None conservé dans le même objet décision, sans copie ni interprétation de son contenu comme SemVer. evaluated_at MUST être un datetime.datetime exact dont tzinfo is datetime.timezone.utc. None, une sous-classe ou un autre tzinfo MUST être refusé sans callback ni lecture d’horloge.

#### Scenario: Version ou instant incomplet refusé

- **WHEN** la version ou l’instant est absent ou ne satisfait pas les types exacts
- **THEN** la validation refuse la projection sans valeur par défaut

#### Scenario: Version politique indépendante

- **WHEN** la projection est valide
- **THEN** le tuple politique demeure dans la décision originale sans devenir la version du composant


### Requirement: Validation de l’événement générique fourni pour la projection audit v1

L’événement générique fourni MUST être validé sur le même objet par validate_audit_event, sans réécriture ni duplication des grammaires date ou SemVer. occurred_at MUST être fourni par l’appelant, jamais généré depuis evaluated_at. Après cette validation, occurred_at MUST représenter le même instant UTC que evaluated_at.

#### Scenario: Instant divergent refusé

- **WHEN** les deux horodatages valides représentent des instants différents
- **THEN** la projection est refusée sans ajuster les horodatages

#### Scenario: Notations UTC équivalentes

- **WHEN** les deux horodatages valides représentent le même instant UTC
- **THEN** la comparaison accepte leur équivalence sans normaliser la chaîne fournie


### Requirement: Correspondances métier de la projection audit v1

Dans audit_event, actor_reference MUST égaler decision_event.subject_id, resource_id MUST égaler decision_event.resource_id et action MUST égaler decision_event.action_id, par égalité exacte des chaînes opaques. result MUST égaler effect.value, soit ALLOW ou DENY, et reason_or_error MUST égaler reason_code, soit ALLOWED ou DENIED.

#### Scenario: Cible ou résultat divergent refusé

- **WHEN** une des correspondances acteur, ressource, action, résultat ou motif diverge
- **THEN** la projection est refusée sans modifier les deux événements


### Requirement: Correspondance tenant de la projection audit v1

Pour un contexte TENANT valide, audit_event.tenant_reference MUST égaler exactement context.tenant_id. Pour un contexte PLATFORM valide, audit_event.tenant_reference MUST être None explicite. La projection MUST NOT inférer un tenant ni déduire un privilège du contexte.

#### Scenario: Tenant exact requis

- **WHEN** un contexte TENANT est fourni
- **THEN** seule la référence exacte du tenant est admissible

#### Scenario: Plateforme sans tenant

- **WHEN** un contexte PLATFORM est fourni
- **THEN** une référence tenant non None est refusée sans déduire de privilège


### Requirement: Corrélation et causalité de la projection audit v1

audit_event.correlation_ids MUST contenir exactement la chaîne decision_event.correlation_id et audit_event.causation_ids MUST contenir exactement la chaîne decision_event.decision_id. Les tuples fournis par l’appelant MUST préserver ordre, doublons et autres références. La validation MUST NOT ajouter automatiquement de référence.

#### Scenario: Référence requise absente

- **WHEN** la corrélation ou la causalité requise est absente de son tuple
- **THEN** la projection est refusée sans compléter le tuple

#### Scenario: Ordre et références conservés

- **WHEN** les références requises sont présentes avec des doublons et autres références valides
- **THEN** les tuples originaux restent inchangés


### Requirement: Métadonnées indépendantes de la projection audit v1

event_id, resource_type, component_id et component_version MUST être fournis explicitement dans l’événement générique. event_id MUST rester indépendant, sans génération ni copie automatique de decision_id. component_id et component_version MUST NOT être déduits de policy_version. Les contrats existants de ces champs MUST rester inchangés.

#### Scenario: Métadonnées sans inférence

- **WHEN** des métadonnées requises sont absentes ou invalides
- **THEN** la projection est refusée sans les fabriquer depuis la décision


### Requirement: Diagnostics et pureté de la projection audit v1

La validation MUST produire des diagnostics VALIDATE statiques, frais, triés et dédupliqués, sans valeur brute, str ou repr d’un objet étranger. Une structure valide MUST produire une liste vide. Les exceptions inattendues MUST se propager. La validation MUST NOT effectuer d’IO, appeler de callback, lire d’horloge ou modifier un objet.

#### Scenario: Refus sans écho ni effet

- **WHEN** une structure, un champ ou une correspondance est invalide
- **THEN** les diagnostics restent statiques sans valeur brute ni effet externe

#### Scenario: Erreur inattendue non masquée

- **WHEN** un validateur public soulève une exception inattendue
- **THEN** elle se propage sans être transformée en réussite ou silence
