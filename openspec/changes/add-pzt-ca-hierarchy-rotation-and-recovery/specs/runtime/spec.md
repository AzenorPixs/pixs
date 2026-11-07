
## ADDED Requirements

### Requirement: Contrat commun runtime et Kernel agnostique du FOURNISSEUR

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — Contrat runtime commun

Le contrat d’exécution MUST exposer une interface commune en lecture à Kernel, Core, Auth, PA et PZT. Kernel MUST demeurer agnostique du FOURNISSEUR et MUST NOT porter de logique de fournisseur de temps. Les mécanismes génériques de temps demeurent admis lorsqu’ils restent indépendants de tout fournisseur concret. Les dépendances MUST être déclarées et le graphe de démarrage MUST demeurer acyclique. Les fonctions indépendantes du temps MUST pouvoir continuer pendant une dégradation. Seuls les effets dont la fenêtre ou l’exigence ne peut pas être prouvée MUST être refusés. Le présent texte MUST NOT prolonger un certificat ni un mandat par une dégradation du temps.

Le contrat `pixs.time.evidence` version `2.0.0`, catégorie `API`, propriétaire `pixs.kernel` est une déclaration pure. Les quatre méthodes exigées sont `time_diagnostic(use_ref:TimePublicRef)->TimeDiagnostic`, `time_require_use(use_ref:TimePublicRef)->None`, `time_ceremony_diagnostic(ceremony_ref:TimePublicRef)->TimeDiagnostic`, `time_ceremony_require_use(ceremony_ref:TimePublicRef)->None`. `TimePublicRef` est un sélecteur non autoritaire lié à l’opération courante dont l’appelant ne choisit jamais le producteur, le producteur attendu est injecté par composition. `outcome` vaut exactement `OBSERVED`, `REFUSED` ou `IN_DOUBT`. `TimeDiagnostic` comporte exactement `outcome`, `producer_ref`, `clock_domain_ref`, `detail_ref`. Le producteur vérifie nativement au point d’usage, aucun objet Python, pointeur ou descripteur comme preuve transportée. `None`, DTO et ancienne observation ne sont en aucun cas une permission. Core, Auth, Agent et PZT décident sur l’intervalle entier y compris transitions `DENY` et `ALLOW`, avec décisions et gardes métier inchangées.

#### Scenario: Garde d’usage avec intervalle prouvé

- **WHEN** le producteur courant fournit un intervalle vérifié avec incertitude bornée
- **THEN** le consommateur l’emploie pour sa seule décision courante sans le mémoriser comme preuve

#### Scenario: Report distant non probant

- **WHEN** seul un report distant ou monotone étranger est disponible sans corrélation locale qualifiée
- **THEN** le consommateur rend un diagnostic seul sans bail ni observation positive

#### Scenario: Fonction indépendante pendant dégradation

- **WHEN** une fonction ne dépend pas du temps courant et que la preuve de temps est invalide
- **THEN** elle peut continuer sous son propre contrat sans prolongation de droit

#### Scenario: Projection forgée ne prouve pas

- **WHEN** une projection diagnostique, un `None` ou un DTO est réinjecté comme permission
- **THEN** le consommateur refuse sans bail ni observation positive

