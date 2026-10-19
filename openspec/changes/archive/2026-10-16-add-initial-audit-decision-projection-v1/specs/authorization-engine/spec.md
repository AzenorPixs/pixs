## MODIFIED Requirements

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
