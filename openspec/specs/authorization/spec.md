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

Hors de l’exception technique C01, de la branche d’opérateur pré-session R01 et de la branche technique PA/PZT et lancement PBO définies dans cette capacité, chaque décision MUST évaluer sujet (identité numérique, utilisateur, groupe), ressource et action déclarées par le module, plus contexte incluant le ScopeContext valide ; la propriété, l'appartenance ou un rôle administrateur MUST NOT valoir autorisation implicite.

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

La seule forme du contexte, la propriété ou root OS MUST NOT valoir permission. Cette autorité MUST NOT ouvrir un tenant, créer de droit métier ni transférer ou présumer l’exception Super Admin. Après amorçage, les exigences applicatives ordinaires MUST reprendre pour les décisions métier et le management ordinaire ; seule la remise technique de références de connexion au workload PBO explicitement autorisée par la branche PA/PZT et lancement PBO MAY précéder PostgreSQL à chaque démarrage.

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

### Requirement: Autorité technique PA PZT et lancement PBO sans base applicative

La préparation PA/PZT et la remise au workload PBO de ses seuls secrets de connexion avant ouverture de PostgreSQL MAY utiliser des identités techniques natives vérifiées sous politique protégée indépendante de cette base. Cette branche MUST rester bornée, auditée et sans droit métier selon les garanties ci-dessous ; C01 et R01 MUST conserver leurs limites.

#### Scenario: Garanties de l’autorité technique PA PZT

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** La préparation PostgreSQL par PA, les échanges PZT locaux nécessaires et la remise au workload PBO de ses seuls secrets de connexion avant ouverture de la base MAY évaluer des identités techniques effectivement vérifiées sous une politique native protégée et versionnée indépendante de cette base, au lieu de fabriquer un Subject applicatif. La confiance initiale MUST provenir du provisionnement opérateur explicite ; UID 0, proximité, possession d'une clé ou reçu C01 MUST NOT suffire. Cette branche MUST vérifier exécutant, rôle, cible, mode, action fermée, référence et version, politique courante, validité, révocation, corrélation et audit durable indépendant. Son contexte MUST rester PLATFORM sans tenant_id ni scope_id. Elle MUST NOT exiger C03/C04 ou des tables Auth pour obtenir précisément la connexion PostgreSQL dont ces contrôles dépendent. Elle MUST NOT autoriser migration applicative, création Core/Auth, compte, tenant, permission métier, gestion ordinaire ou exception Super Admin. Ces actes MUST rester sous leurs contrats applicatifs et, pour l'acte initial, R01. Les mandats temporaires de préparation MUST prendre fin après leur résultat rapproché ; à chaque démarrage ultérieur, seule la remise technique minimale au workload et son audit MAY précéder l'autorité PostgreSQL. Cette branche MUST NOT élargir C01 INSTALLER, prolonger R01 ou réétiqueter NORMAL en INSTALLER.

#### Scenario: Démarrage NORMAL sans connexion initiale

- **WHEN** un workload PBO vérifié démarre en NORMAL avant ouverture de PostgreSQL avec une politique native courante autorisant sa seule référence de connexion
- **THEN** la remise technique est évaluée sans dépendance circulaire à Auth PostgreSQL, puis les décisions applicatives attendent leur autorité courante

#### Scenario: Identité technique utilisée pour un tenant

- **WHEN** un exécutant admis au parcours PA/PZT demande une création de tenant ou une décision de management ordinaire
- **THEN** la branche technique refuse et aucun Subject métier ou privilège n’est fabriqué

#### Scenario: Politique native non vérifiable

- **WHEN** une identité est correcte mais la politique est expirée, révoquée ou impossible à vérifier fraîchement
- **THEN** aucun secret ni nouvel effet technique n’est admis et le service reste non prêt

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

### Requirement: Confirmation C08 seize champs et permission distincte

La confirmation C08 MUST lier installation, cible, opération, opérateur et politique à la projection, à l'observation, au plan, aux préconditions et aux effets vérifiés, selon le schéma fermé ci-dessous. Elle MUST rester distincte de la confirmation administrative de retrait PA, sans porter ni tableaux A07 futurs, ni signature, ni digest de futur mandat.

#### Scenario: Confirmation liée sans tableaux futurs

- **WHEN** C08 confirme le plan, les préconditions et les effets
- **THEN** la confirmation lie les cinq bindings projection, observation, plan, préconditions et effets avec la politique sans porter de tableaux A07 futurs, de signature ni de digest de futur mandat

#### Scenario: Seize champs exacts et acyclicité

- **WHEN** la confirmation est présentée
- **THEN** elle porte exactement schema pixs.c08.postgresql-confirmation.v1, schema_version 1.0.0, confirmation_ref, installation_ref, target_ref, operation_id, operator_ref, projection_binding, observation_binding, plan_binding, preconditions_binding, effects_binding, policy_ref, policy_version, confirmed_at et correlation_id, avec ContentBinding exact ref et version chaînes bornées et sha256 minuscule 64, confirmed_at UTC YYYY-MM-DDTHH:MM:SS.ffffffZ, sans coercition ni type nullable implicite
- **AND** l'acyclicité exclut l'acte, la signature et le digest de futur mandat ainsi que les tableaux A07 futurs, sans exclure les bindings de plans déjà publiés, et cible, installation, opération, politique et références sont rapprochées avant consentement
### Requirement: Garde technique du temps indépendante de la base

La branche technique du temps MUST NOT conférer de pouvoir R01/SuperAdmin/droit métier/renouvellement PKI. Elle MUST vérifier ses prérequis d’autorité sous politique protégée, opérateur explicite, catalogue, cible et exécutant vérifiés, sans supposer une validité universelle et sans créer d’auto-autorité, sinon elle MUST refuser. D6 MUST NOT rouvrir une autorité initiale de PKI.

#### Scenario: Prérequis d’autorité non prouvés

- **WHEN** les prérequis d’autorité ne sont pas vérifiés avant temps universel prouvable
- **THEN** la branche est refusée sans auto-autorité
