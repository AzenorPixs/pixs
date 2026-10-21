# authorization Specification

## Purpose
L'autorisation évalue sujets, ressources, actions et contexte avec rôles, ACL et permissions, selon une politique de refus par défaut appliquée côté applicatif.

## Requirements

### Requirement: Portée du contrôle total du Super Admin

Le Super Admin MUST disposer du contrôle total sur la plateforme. Un tenant MUST faire l'objet d'un accès explicite distinct avant toute extension de ce contrôle à ses ressources ; après cet accord, les ACL du tenant, y compris ses refus explicites, MUST NOT limiter ce contrôle. Cet accord MUST NOT ouvrir implicitement les autres tenants.

#### Scenario: Tenant non accordé au Super Admin

- **WHEN** le Super Admin demande une ressource d'un tenant sans accès explicite à ce tenant
- **THEN** la demande est refusée malgré son contrôle total sur la plateforme

#### Scenario: Tenant accordé malgré un refus ACL

- **WHEN** un accès au tenant A a été explicitement accordé au Super Admin et une ACL de A refuse l'action demandée
- **THEN** l'exception permet l'action dans A malgré ce refus
- **AND** aucun accès au tenant B n'est déduit de cet accord

### Requirement: Exception Super Admin dans toutes les interfaces

L'exception Super Admin MUST être disponible dans le panneau, les API, la CLI et les traitements asynchrones demandés par ce compte. Un worker MUST porter l'acteur initial et son périmètre sans s'authentifier avec les credentials du Super Admin ni acquérir ce compte comme identité de service. Cette exécution MUST NOT transférer l'exception à un autre compte.

#### Scenario: Même exception selon la façade

- **WHEN** le Super Admin demande la même opération dans le même périmètre par le panneau, une API, la CLI ou un traitement asynchrone
- **THEN** les mêmes droits de dérogation s'appliquent
- **AND** le worker conserve l'acteur initial sans recevoir les credentials du Super Admin

### Requirement: Contrôles applicatifs dérogeables par le Super Admin

Dans son périmètre autorisé, le Super Admin MUST pouvoir déroger à tous les contrôles applicatifs, notamment refus ACL, règles métier, maintenance, quotas, entitlements, feature flags, gouvernance, résidence, rétention, legal holds, audit et désactivation externe. La possibilité de dérogation MUST NOT étendre son accès à un tenant non accordé ni permettre un second Super Admin ou une délégation.

#### Scenario: Contrôle applicatif dérogé

- **WHEN** le Super Admin utilise une dérogation à un contrôle applicatif dans son périmètre autorisé
- **THEN** le contrôle concerné ne bloque pas cette opération
- **AND** ni un autre compte ni un tenant non accordé ne bénéficient de l'exception

### Requirement: Priorité transversale de l'exception Super Admin

L’exception Super Admin MUST prévaloir sur les contrôles applicatifs dans son seul périmètre autorisé. Profils structurels préparatoires et contrats d’exécution MUST rester distincts. Les comptes ordinaires MUST conserver DENY, refus par défaut et contrôles obligatoires ; seule l’exception d’audit de retrait d’accès Auth définie par audit s’applique sans leur transférer les privilèges Super Admin.

#### Scenario: Compte ordinaire sans exception

- **WHEN** un Administrateur ordinaire rencontre un refus ACL, un audit obligatoire hors retrait d’accès Auth admissible ou un autre contrôle bloquant
- **THEN** le contrôle reste applicable et le rôle administrateur ne donne pas l'exception Super Admin

#### Scenario: Contrat structurel sans privilège

- **WHEN** un profil préparatoire valide une structure d'identité, de périmètre, de politique ou de données
- **THEN** cette validation reste structurelle et n'établit aucune exception Super Admin

### Requirement: Modèle Subject Resource Action Context

Hors de l’exception technique C01 et de la seule branche d’opérateur pré-session R01 définies dans cette capacité, chaque décision MUST évaluer sujet (identité numérique, utilisateur, groupe), ressource et action déclarées par le module, plus contexte incluant le ScopeContext valide ; la propriété, l'appartenance ou un rôle administrateur MUST NOT valoir autorisation implicite.

#### Scenario: Propriété sans politique refusée

- **WHEN** un propriétaire invoque son seul titre sans règle applicable
- **THEN** l'accès est refusé par défaut

#### Scenario: Sujet technique avant identité applicative

- **WHEN** une action technique C01 explicitement autorisée est requise en INSTALLER avant existence de la base et des identités applicatives
- **THEN** seul le sujet OS effectivement vérifié peut être évalué sous sa politique d’amorçage fermée, son contexte PLATFORM et son audit obligatoires
- **AND** aucune identité numérique ou permission métier n’est fabriquée

#### Scenario: Opérateur R01 sans session cible
- **WHEN** une première installation exige un acte R01 avec opérateur vérifié par sa clé préautorisée et un plan autorisé
- **THEN** seul le sujet opérateur borné et son mapping explicite sont évalués selon la branche R01, sans fabriquer de session ou d’identité du futur compte cible

### Requirement: Priorité DENY puis ALLOW puis refus

Hors exception Super Admin, l’évaluation MUST appliquer DENY, puis ALLOW, puis refus par défaut. Tout accès plateforme ou inter-tenant MUST avoir permission et contexte explicites ainsi que l’audit applicable. Seul un retrait d’accès Auth admissible selon audit MAY être confirmé sans audit disponible ; il MUST NOT accorder de nouvel accès ni ignorer un refus d’autorisation.

#### Scenario: Conflit DENY contre ALLOW

- **WHEN** une règle de refus et une règle d'autorisation couvrent la même demande
- **THEN** le refus l'emporte avec une erreur stable minimale

### Requirement: Évaluation applicative avant exposition

Django reste l'autorité d'évaluation ; frontal, caches, projections et synchronisation MUST uniquement refléter la décision ; les listes appliquent le filtrage autorisé à la source.

#### Scenario: Liste filtrée à la source

- **WHEN** une collection mêle ressources autorisées et interdites
- **THEN** seules les autorisées sont retournées, sans filtrage frontal

### Requirement: Autorisation technique C01 bornée sans extension métier

Avant existence de la base et des identités applicatives, les seules actions techniques d’amorçage C01 en mode INSTALLER explicitement demandé MAY employer un sujet OS effectivement vérifié au lieu d’un Subject applicatif. Cette exception MUST exiger une politique de confiance versionnée, un ensemble fermé d’actions et références, le refus par défaut, un contexte PLATFORM sans tenant_id ni scope_id et un audit explicites.

#### Scenario: Action métier hors bootstrap

- **WHEN** une demande dépasse les actions techniques INSTALLER autorisées ou vise une ressource métier
- **THEN** l’exception est refusée et les exigences applicatives ordinaires restent obligatoires

### Requirement: Limites de l’autorité technique d’amorçage

La seule forme du contexte, la propriété ou root OS MUST NOT valoir permission. Cette autorité MUST NOT ouvrir un tenant, créer de droit métier ni transférer ou présumer l’exception Super Admin. Après amorçage, les exigences applicatives ordinaires MUST reprendre.

#### Scenario: Action métier hors bootstrap

- **WHEN** une demande dépasse les actions techniques INSTALLER autorisées ou vise une ressource métier
- **THEN** l’exception est refusée et les exigences applicatives ordinaires restent obligatoires

### Requirement: Opérateur pré-session R01 lié à une confiance explicite

La branche propriétaire C08/C02 MAY employer avant session Pixs et compte cible un sujet opérateur vérifié par C03/C04, à partir d’une clé publique personnelle préautorisée et d’un mapping explicite. Une politique d’installation versionnée à actions fermées MUST encadrer ce sujet. Il MUST NOT être employé pour une opération ordinaire ni présumer l’identité ou l’assurance du futur compte.

#### Scenario: Première installation sans session
- **WHEN** clé préautorisée, mapping et politique sont vérifiés pour un plan INSTALLER éligible
- **THEN** C04 peut autoriser les seuls effets fermés R01 sans session du compte cible

### Requirement: Signature Ed25519 de la preuve d’amorçage

La preuve R01 MUST utiliser une signature Ed25519 vérifiée avec cryptography sur des données liant opérateur, installation, version du plan, actions et validité. La clé privée MUST rester sous contrôle de l’opérateur. La sérialisation et les bornes temporelles MUST être qualifiées avant réalisation.

#### Scenario: Plan substitué
- **WHEN** une signature est présentée pour un plan différent de celui soumis
- **THEN** la preuve est refusée avant effet métier

### Requirement: Aucune autorité implicite de bootstrap

Une clé fournie par l’appelant, UID 0, les credentials PostgreSQL, une confirmation de mot de passe ou un reçu C01 MUST NOT établir seuls confiance ou permission métier. C01 MUST conserver sa seule autorité technique et ses contrôles, sans transfert de l’exception Super Admin.

#### Scenario: Clé autoautorisée
- **WHEN** une signature valide utilise une clé non préautorisée ou sans mapping et politique
- **THEN** l’acte est refusé sans droit déduit de la seule validité cryptographique

### Requirement: Autorisation finale R01 de dix minutes et usage unique

L’autorisation finale R01 MUST valoir 10 minutes à partir de la validation du plan final et MUST être liée à un opérateur, une installation, une version de plan et ses actions fermées. Sa consommation MUST être liée au commit propriétaire des effets et MUST NOT permettre un second effet concurrent ou repris. Cette durée MUST NOT limiter toute la préparation ni créer d’autorité permanente.

#### Scenario: Consommation au commit
- **WHEN** des appels concurrents présentent la même autorisation finale
- **THEN** au plus un acte est committé et l’autorisation ne permet pas de second effet

### Requirement: Revalidation et reprise de l’amorçage

Preuve expirée, révoquée ou substituée, plan modifié ou autre cible MUST exiger une nouvelle autorisation R01. Après réponse perdue, la reprise MUST consulter le résultat persistant et revalider ses conditions ; une issue inconnue MUST être réconciliée avant rejeu.

#### Scenario: Expiration ou nouveau plan
- **WHEN** la fenêtre de 10 minutes est atteinte ou le plan signé modifié avant admission finale
- **THEN** aucun nouvel effet n’est engagé et une nouvelle autorisation est requise

#### Scenario: Commit puis réponse perdue
- **WHEN** le commit a consommé l’autorisation mais la réponse ou le marqueur est perdu
- **THEN** la reprise inspecte le résultat et ne crée ni second compte ni identité ou autorisation dupliquée
