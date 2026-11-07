## ADDED Requirements

### Requirement: Autorité technique PKI Z12 bornée à la première installation

La cérémonie Z12 de première installation MAY évaluer une identité native et une autorité technique protégée, indépendantes de la base cible, pour ses seules opérations PKI initiales. Cette exception MUST respecter les garanties ci-dessous, sans Subject métier, pouvoir R01 ou admission ordinaire ; sa clôture MUST précéder le contrôle courant.

#### Scenario: Sujet natif et mandat initial positivement vérifiés

- **WHEN** Z12 reçoit une opération PKI initiale nécessaire au parcours de préparation PostgreSQL avant existence de son autorité applicative
- **THEN** une composition de confiance MUST vérifier identité native, provenance du lanceur opérateur, politique protégée/versionnée, mandat courant distinct de R01 et ses liens installation/cible/exécutants/rôles/plan/opération, plus validité, révocation, fraîcheur, audit et ancrage anti-restauration qualifié
- **AND** le contexte MUST rester PLATFORM sans tenant_id ni scope_id ; UID 0, premier PBO, proximité, booléen client, clé, certificat ou fichier simplement présent MUST NOT constituer seuls cette autorité
- **AND** cette branche MUST autoriser uniquement les opérations PKI initiales fermées du propriétaire Z12 ; renouvellement, bascule et management ordinaires, effets Core/Auth, droits métier, pouvoirs R01 ou exception Super Admin MUST NOT en être déduits ; C01 et R01 MUST conserver leurs limites

#### Scenario: État ancien ou autorité retirée sans droit restauré

- **WHEN** identité, mandat, politique, cible, version, époque, validité, révocation, audit ou ancrage sont invérifiables, qu’une concurrence est contradictoire, qu’une réponse/issue est perdue, qu’un état est restauré, ou que l’autorité initiale est retirée
- **THEN** le système MUST refuser le nouvel effet et conserver une situation bloquée ou incertaine inspectable ; il MUST réconcilier preuves, effets réels et conditions courantes avant toute reprise, sans rejouer un mandat consommé, produire une seconde PKI ou réactiver un droit
- **AND** absence de PostgreSQL, de journal ou de fichier MUST NOT prouver une première installation ; une restauration, un clone ou une perte de l’ancrage MUST NOT rouvrir automatiquement la cérémonie ou convertir le contrôle ordinaire en autorité technique initiale
### Requirement: Garde technique du temps indépendante de la base

La branche technique du temps MUST NOT conférer de pouvoir R01/SuperAdmin/droit métier/renouvellement PKI. Elle MUST vérifier ses prérequis d’autorité sous politique protégée, opérateur explicite, catalogue, cible et exécutant vérifiés, sans supposer une validité universelle et sans créer d’auto-autorité, sinon elle MUST refuser. D6 MUST NOT rouvrir une autorité initiale de PKI.

#### Scenario: Prérequis d’autorité non prouvés

- **WHEN** les prérequis d’autorité ne sont pas vérifiés avant temps universel prouvable
- **THEN** la branche est refusée sans auto-autorité
