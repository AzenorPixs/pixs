## MODIFIED Requirements

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

### Requirement: Limites de l’autorité technique d’amorçage

La seule forme du contexte, la propriété ou root OS MUST NOT valoir permission. Cette autorité MUST NOT ouvrir un tenant, créer de droit métier ni transférer ou présumer l’exception Super Admin. Après amorçage, les exigences applicatives ordinaires MUST reprendre pour les décisions métier et le management ordinaire ; seule la remise technique de références de connexion au workload PBO explicitement autorisée par la branche PA/PZT et lancement PBO MAY précéder PostgreSQL à chaque démarrage.

#### Scenario: Action métier hors bootstrap

- **WHEN** une demande dépasse les actions techniques INSTALLER autorisées ou vise une ressource métier
- **THEN** l’exception est refusée et les exigences applicatives ordinaires restent obligatoires

## ADDED Requirements

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
