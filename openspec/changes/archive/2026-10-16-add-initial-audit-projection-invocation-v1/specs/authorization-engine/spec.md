## MODIFIED Requirements

### Requirement: Validation préalable de la projection audit avant invocation v1

Le Core MUST proposer l'opération distincte invoke_audit_projection(projection, sink) avec deux entrées explicites : une AuditDecisionProjectionV1 et un AuditSink PDP fourni par un appelant backend de confiance. L'opération MUST appeler validate_audit_decision_projection sur la même projection avant tout accès au port. Une projection invalide MUST produire False sans appeler sink.record.

#### Scenario: Projection invalide refusée avant le port

- **WHEN** la validation de la projection produit des diagnostics, notamment pour un profil ou événement étranger ou hostile
- **THEN** l'opération retourne False sans accéder au port ni appeler record et sans contourner les contrôles de types de la projection


### Requirement: Erreurs du validateur de projection audit propagées v1

Une exception inattendue du validateur MUST se propager.

#### Scenario: Erreur inattendue du validateur propagée

- **WHEN** le validateur public de projection soulève une exception inattendue
- **THEN** l'exception se propage et aucun appel au port n'a lieu


### Requirement: Invocation unique du port pour une projection audit valide v1

Une projection valide MUST conduire à exactement un appel de sink.record avec le decision_event original, conservé par identité, sans copie, conversion ou enregistrement implicite de l'audit_event générique. Cette opération MUST NOT modifier la construction ou la validation pure de la projection.

#### Scenario: Projection valide transmise une fois

- **WHEN** une projection valide et un port explicite sont fournis
- **THEN** le port reçoit exactement une fois le même objet decision_event et aucun événement générique n'est enregistré par l'opération


### Requirement: Acquittement booléen exact du port audit v1

invoke_audit_projection MUST retourner un bool exact. Son résultat MUST être True uniquement lorsque le retour observé de record est True exact. False, None, 1 ou toute autre valeur MUST produire False sans conversion ni appel aux méthodes de cette valeur.

#### Scenario: Retour True exact reconnu

- **WHEN** l'unique appel du port retourne True exact
- **THEN** l'opération retourne True sans autre appel ni effet ajouté

#### Scenario: Autre retour refusé sans coercition

- **WHEN** l'unique appel du port retourne False, None, 1 ou un objet arbitraire
- **THEN** l'opération retourne False sans appeler les méthodes du retour ni relancer record


### Requirement: Exceptions du port audit sans relance v1

Une exception ordinaire lors de l'accès ou de l'appel du port MUST produire False sans exposition de son contenu ni relance. Les interruptions dérivées directement de BaseException MUST NOT être masquées.

#### Scenario: Exception du port sans relance

- **WHEN** l'accès ou l'appel du port soulève une exception ordinaire
- **THEN** l'opération retourne False sans exposer l'exception ni relancer l'opération

#### Scenario: Interruption système propagée

- **WHEN** l'accès ou l'appel du port soulève une interruption dérivée directement de BaseException
- **THEN** l'interruption se propage sans être transformée en acquittement ou refus silencieux


### Requirement: Frontières de l'invocation du port audit v1

L'opération MUST NOT lire d'horloge, exécuter un accès ressource, enregistrer un état de déduplication, modifier un objet fourni ou être branchée implicitement dans authorize ou plan_filter. Leurs signatures, décisions, obligations et règles Super Admin MUST rester inchangées.

#### Scenario: Deux invocations explicites distinctes

- **WHEN** l'appelant invoque deux fois l'opération avec la même projection valide
- **THEN** chaque invocation effectue son unique appel explicite, sans garantie globale de déduplication ou d'exécution unique entre invocations
