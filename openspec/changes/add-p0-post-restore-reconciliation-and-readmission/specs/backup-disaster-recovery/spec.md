## ADDED Requirements

### Requirement: Réadmission contrôlée après restauration

Après restauration, un plan versionné MUST réconcilier composition, gouvernance, références de secrets, sessions, incidents et traitements concernés avant réadmission. L’instance MUST rester en état contrôlé sans exposition ni rejou automatique des effets non réconciliés. Un snapshot ancien MUST NOT suffire à prouver une confiance courante. Les dérogations applicatives MUST suivre authorization sans fabriquer fraîcheur, audit ou effet confirmé.

#### Scenario: Snapshot antérieur à une révocation

- **WHEN** un état restauré précède une révocation et constitue la seule preuve disponible de validité du contexte concerné
- **THEN** le plan signale l’absence de fait courant vérifiable et ne rétablit pas implicitement ce droit
- **AND** la reprise attend une réconciliation ou revalidation applicable selon les contrats propriétaires et les exceptions canoniques

#### Scenario: Effet engagé avant le point restauré

- **WHEN** un traitement restauré peut correspondre à un effet déjà engagé dont le résultat courant est inconnu
- **THEN** son identité d’opération et son incertitude sont conservées pour réconciliation sans réémission automatique comme travail neuf

#### Scenario: Réconciliation interrompue

- **WHEN** une réconciliation de restauration est interrompue puis reprise
- **THEN** elle reprend ses résultats persistants sans réactiver implicitement le trafic ni répéter un effet confirmé

#### Scenario: Secours et faits réellement obtenus

- **WHEN** le compte Super Admin authentifié utilise une dérogation autorisée pendant la reprise
- **THEN** son exception canonique reste applicable sans MFA imposé au secours, sans transfert au worker et sans preuve de fraîcheur ou d’audit inventée
