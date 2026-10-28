# Delta — PA04 profil 1A-2B-3A

## ADDED Requirements

### Requirement: Catalogue 1A-2B-3A et cinq opérations conditionnelles

Dans le profil 1A Debian 13 physique/VM système seul, 2B gestion bornée, 3A connecté via PZT, les cinq opérations OBSERVE, PREPARE_PLAN, START, STOP, READ_RESULT MUST respecter les clauses ci-dessous. Toute autre plateforme, session utilisateur, conteneur produit ou hors ligne MUST rester hors de ce profil sans N/A sans justification. L’exception Super Admin canonique reste dans son seul périmètre sans nouvelle dérogation.

#### Scenario: Mandat périmé dans le profil

- **WHEN** un mandat périmé ou révoqué est présenté dans ce profil
- **THEN** l’opération est refusée sans effet

### Requirement: OBSERVE sans effet dans le profil

OBSERVE MUST identifier mandat, cible allowlistée et génération courants et MUST NOT produire de mutation. Une observation MUST être réellement lue avec cible et génération liées. Une identité seule MUST NOT accorder de permission.

#### Scenario: Observation courante

- **WHEN** une observation autorisée est demandée
- **THEN** l’état réellement lu est retourné avec sa cible et génération, sans effet

### Requirement: PREPARE_PLAN sans effet dans le profil

PREPARE_PLAN MUST vérifier mandat et cible courants et MUST NOT appliquer d’effet. Le plan MUST rester versionné à confirmer. Un plan hors mandat MUST NOT être appliqué.

#### Scenario: Plan à confirmer

- **WHEN** un plan est préparé dans ce profil
- **THEN** seul un plan autorisé et courant est proposé, sans effet

### Requirement: START cible et exclusions dans le profil

START MUST viser un service produit explicitement autorisé inscrit au catalogue livré, avec mandat, plan et génération courants. Il MUST NOT viser un nom libre, RESTART, ENABLE, DISABLE, comptes, fichiers, installation, réseau ou service PA/PZT/CAB/SSH/PostgreSQL. Les essais MUST utiliser seulement le factice dédié.

#### Scenario: Cible START interdite refusée

- **WHEN** une cible non autorisée est demandée pour START avec mandat courant
- **THEN** l’opération est refusée sans effet

### Requirement: START postcondition observée et garde-fous

L’effet START MUST être borné et la postcondition native MUST être vraiment observée par le propriétaire courant liée à cible, génération et artefact. Un reçu seul MUST NOT valoir preuve d’effet natif. En perte de contrôle, tout nouvel effet MUST être bloqué. Une compensation hors profil ou plan MUST NOT être tentée. Une permission révoquée MUST NOT être restaurée.

#### Scenario: START nominal avec postcondition observée

- **WHEN** un START autorisé vise le service livré avec mandat et plan courants
- **THEN** l’effet est exécuté puis la postcondition native vraiment observée est rapportée

### Requirement: START reprise après issue incertaine

L’idempotence seule MUST NOT garantir exactement une fois après crash. Une issue incertaine exige une postcondition fiable ou une intervention autorisée avant nouvel effet.

#### Scenario: START incertain réconcilié

- **WHEN** l’effet START reste incertain après crash
- **THEN** la reprise vérifie la postcondition ou attend l’intervention autorisée sans double effet

### Requirement: STOP cible et exclusions dans le profil

STOP MUST viser un service produit explicitement autorisé inscrit au catalogue livré, avec mandat, plan et génération courants. Il MUST respecter les mêmes exclusions de cible et d’opérations que START, sans interdire des contrôles de sécurité supplémentaires. Les essais MUST utiliser seulement le factice dédié.

#### Scenario: Cible STOP interdite refusée

- **WHEN** une cible interdite ou un mandat périmé est présenté pour STOP
- **THEN** l’opération est refusée sans effet

### Requirement: STOP postcondition et reprise

La postcondition d’arrêt MUST être vraiment observée liée à cible, génération et artefact. L’idempotence seule MUST NOT garantir exactement une fois après crash. Une issue incertaine exige une postcondition fiable ou une intervention autorisée avant nouvel effet.

#### Scenario: STOP nominal avec postcondition observée

- **WHEN** un STOP autorisé vise le service livré avec mandat et plan courants
- **THEN** l’arrêt est exécuté puis la postcondition native vraiment observée est rapportée

### Requirement: READ_RESULT avec état durable dont inconnu

READ_RESULT MUST exposer l’état réellement durable succès, échec ou inconnu, distinct du reçu, avec cible, génération et artefact liés, et MUST NOT rejouer l’effet. Si la preuve durable manque, READ_RESULT MUST rapporter inconnu avec ses références et MUST NOT inventer une preuve. Un état incertain MUST rester explicite sans succès inventé.

#### Scenario: Résultat incertain exposé

- **WHEN** l’effet est incertain après crash
- **THEN** READ_RESULT rapporte inconnu avec ses références, sans rejouer ni conclure un succès
