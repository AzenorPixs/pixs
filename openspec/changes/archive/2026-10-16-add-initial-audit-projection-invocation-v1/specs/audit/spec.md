## MODIFIED Requirements

### Requirement: Portée limitée de l'acquittement observé du port audit v1

L'opération distincte invoke_audit_projection définie par authorization-engine MUST constater uniquement le retour du port PDP fourni pour cet appel. Un résultat True MUST NOT valoir preuve de persistance, d'exhaustivité, de conformité P0, de fraîcheur, de déduplication ou d'accès autorisé.

#### Scenario: Retour du port distinct d'une preuve persistante

- **WHEN** le port fourni retourne True et l'opération reconnaît ce retour
- **THEN** seule cette valeur observée est attestée, sans preuve de persistance ou de conformité P0 et sans autorisation d'accès implicite


### Requirement: Exclusions de l'invocation préparatoire du port audit v1

Cette opération MUST NOT enregistrer ou convertir implicitement l'événement d'audit générique, ni introduire stockage, provider, WORM, rétention, SQL, export, Bulk, Frontend, EventRegistry ou notification.

#### Scenario: Contrats étrangers conservés

- **WHEN** l'opération distincte est invoquée
- **THEN** les décisions, obligations, exceptions Super Admin et formats d'événements existants restent inchangés, sans intégration implicite dans une capacité étrangère


### Requirement: Contrats d'audit et projection pure conservés v1

Les exigences générales d'audit, de minimisation, d'append-only, les deux formats d'événements et les obligations et exceptions Super Admin MUST rester applicables sans modification. La seule validation de la projection MUST rester pure et distincte de cette invocation explicite du port fourni.

#### Scenario: Projection seule sans invocation

- **WHEN** l'appelant construit ou valide seulement la projection sans invoquer l'opération distincte
- **THEN** aucun port n'est appelé et la projection demeure un contrôle structurel préparatoire pur
