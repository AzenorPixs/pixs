## MODIFIED Requirements

### Requirement: Portée préparatoire de la projection décision et audit v1

AuditDecisionProjectionV1, défini par authorization-engine, MUST rester un contrôle structurel préparatoire entre deux objets fournis. Sa validation MUST NOT constituer un acquittement d’audit, une persistance, une preuve d’exhaustivité ou une conformité P0. Les contrats existants d’événements, signatures PDP/PEP, obligations ordinaires et exceptions Super Admin MUST rester inchangés.

#### Scenario: Projection distincte d’un audit réalisé

- **WHEN** la projection est structurellement valide
- **THEN** aucune preuve d’audit réalisé, persistant, exhaustif ou P0 n’est annoncée

#### Scenario: Obligations et exceptions conservées

- **WHEN** une opération ordinaire ou Super Admin est évaluée
- **THEN** ses obligations et exceptions existantes restent applicables sans dérogation induite par le profil


### Requirement: Limites de la projection décision et audit v1

Ce profil MUST NOT introduire stockage, cryptographie, WORM, rétention, export, provider, valeur par défaut ou privilège. Il MUST NOT ouvrir EventRegistry, un schéma de manifeste, Bulk ou Frontend. Il MUST préserver les deux formats d’événements intentionnellement distincts et les exigences générales d’audit.

#### Scenario: Aucune ouverture runtime

- **WHEN** le profil est utilisé ou validé
- **THEN** aucune persistance, exécution runtime, ouverture P0 ou modification d’un contrat étranger au profil n’est effectuée
