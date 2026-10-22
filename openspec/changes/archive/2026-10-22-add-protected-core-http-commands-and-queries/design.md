# Conception — C06

## Statut et périmètre autorisé

RÉALISATION_VÉRIFIÉE_C06 — conception et compléments techniques validés par CGPT avant écriture, dans le canon C00 courant. Les preuves du 22 octobre sont précisées en fin de document. Archivage, rapport post-archive et clôture CAB restent distincts et ne sont pas encore déclarés accomplis.

## État initial de préparation — historique

Constat : Plans OpenAPI et fabriques de réponses sont isolés ; les documents backend indiquent l’absence de routes Core complètes, pagination et idempotence générale.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/api/README.md](../../../../src/pixs/backend/api/README.md).
- [src/pixs/backend/api/contracts.py](../../../../src/pixs/backend/api/contracts.py).
- [src/pixs/backend/api/success.py](../../../../src/pixs/backend/api/success.py).
- [src/pixs/backend/local_test_composition.py](../../../../src/pixs/backend/local_test_composition.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Exposer les services Core propriétaires par API versionnée et contrats publiés. Résoudre tenant du chemin, identité et autorisation avant exposition ; requêtes sans mutation, listes filtrées à la source. Lier clé d’idempotence, empreinte de requête, périmètre et résultat durable ; localiser les messages par catalogue.

## Raccordement C03 des façades du 20 octobre 2026

Le profil retient une façade web explicitement déclarée à session côté serveur et cookie protégé inaccessible au JavaScript, avec CSRF ; l’API standard et la CLI restent Bearer opaque selon les [décisions C03](../2026-10-21-add-initial-authentication-and-sessions/design.md). [N04](../../define-p0-web-serving-and-security-boundary/specs/api/spec.md) possède la déclaration des surfaces et de leurs protections. Une route ne choisit pas implicitement l’un des modes selon les justificatifs reçus ; l’ambiguïté est traitée selon un contrat explicite sans élargir l’admission.

Les façades utilisent les mêmes interfaces Auth spécialisées, puis le même contrôle d’autorisation et ScopeContext canonique. Routes, schémas, erreurs et paramètres de cookie/transport restent à détailler dans les contrats versionnés. Les durées, la fraîcheur et les plafonds ordinaires de C03 s’appliquent sans contournement par changement de façade, sous les exceptions canoniques Super Admin.

La création/rotation de session suit la transaction commune C03/C05. L’exception D14 ne concerne que le retrait d’accès Auth admissible : elle ne rend pas une mutation Core, un changement de justificatif ou une réponse protégée admissible sans ses garanties. Les deltas C03/C04/C05 et les deux clauses N04 liées aux sessions sont adoptés au canon le 20 octobre 2026, sans code ni route effectivement exposée.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions initialement bloquantes avant réalisation

Catalogue exact de routes et commandes, schémas/versions, contrat de curseur et conservation idempotence ; ne pas annoncer Bulk ou SDK optionnels.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-core-postgres-services](../2026-10-20-add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../2026-10-21-add-durable-minimized-audit/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Parcours API sans frontend ; contrat et réponse concordants ; rejeu même clé/même contenu sans double effet, conflit explicite ; tenant du chemin canonique ; accès privé et inter-tenant refusés.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

La préparation initiale ne réalisait aucune migration. La réalisation ajoute 0003_core_idempotence après 0002_core_audit, avec migration/retour testés uniquement dans des schémas PG privés jetables. Le retour refuse les données idempotentes à conserver ; aucun abaissement automatique ni migration d’une base applicative n’est exécuté.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Pour O21, publier un document OpenAPI machine-readable versionné par majeure, associé aux routes et erreurs effectivement exposées. ApiContractPlan référence ce document logiquement mais ne contient pas sa publication ni sa conformité.

Relier chaque opération publique au contexte canonique, authentification, autorisation, pagination, idempotence et statut asynchrone applicable. Validation du document et tests contrat-serveur doivent détecter dérive ou surface privée exposée.

La construction du bundle d’entrée SDK appartient à O21 ; C06 possède contrat et serveur HTTP. Format de publication/version et compatibilité doivent être revus avant code, sans créer ici un nouveau change déjà couvert par ce lot.


Voir [audit individuel et limites des preuves](../2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T08 — Audit exhaustif du panneau et navigation SPA

L’audit de chaque activité du panneau inclut navigation/lecture ; des logs ou un acquittement mémoire n’en prouvent pas la persistance. Compléter protocole C05/C13 et critères de volumétrie/minimisation C15 ; préserver exception Super Admin.

Contrôles à intégrer : Panne sink avant affichage/action ordinaire refusée selon contrat ; Dérogation root sans audit annoncé à tort ; Navigation SPA reliée à une preuve serveur et aucune donnée sensible copiée.

### T09 — Contexte tenant et réponse retardée du navigateur

L’invalidation est prévue ; les réponses en vol, onglets et changements de session doivent être inclus dans le contrat de concurrence UI. Compléter C11 et sa recette ; pas d’offline, cache distribué ou client natif imposé.

Contrôles à intégrer : Réponse du tenant précédent n’alimente pas la vue courante ; Déconnexion et révocation invalident contexte ; Identifiant/header fourni ne remplace pas le tenant canonique.

### T10 — Mutation, audit, idempotence et outbox

Les composants prévoient chacun leur partie ; la frontière transactionnelle et l’échec avant/après commit doivent être explicitement communs. Compléter contrats C05/C06/C09 avec refus distincts et résultat réconcilié ; pas de nouveau broker.

Contrôles à intégrer : Rollback sans événement publié ; Commit puis réponse perdue restituant résultat idempotent ; Double livraison sans double effet propriétaire ; Refus auditable sans mutation métier.

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

### T15 — Langues, thèmes et accessibilité de tous les parcours

Les parcours CLI, erreurs API, management et secours font aussi partie des textes utilisateur ; couverture ne se limite pas à la page du shell. Compléter la matrice C12/C17 et les contrats de messages ; codes stables non localisés.

Contrôles à intégrer : Deux navigateurs déclarés, clavier/zoom/lecteur d’écran ; Erreurs et confirmations d’installation/exploitation localisées ; Thème/session/tenant sans fuite d’état.

Voir [audit transversal durable](../2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Décisions de réalisation du 21 octobre 2026 — C06

Les sections précédentes décrivent la préparation historique. La demande CISMP5 autorise maintenant la réalisation de ce seul change après livraison vérifiée de C02/C03/C04/C05. Les choix ci-dessous sont des décisions d'implémentation du canon courant, validées par CGPT ; aucun résultat de test, d'archive ni de qualification P0 n'est encore acquis. `skip_specs: true` reste applicable ; une contradiction normative réelle impose une RSMP distincte avant l'effet concerné.

### Routes, périmètres et schémas v1

Le préfixe Bearer est `/api/v1` et son miroir web explicite est `/api/v1/web`. Chaque route déclare son mode ; aucun choix automatique par justificatif. Un cookie sur Bearer ne remplace jamais Authorization ; Authorization sur une route web est refusé. Le transport HTTPS et l'hôte approuvé sont vérifiés ; l'origine absente est admissible pour le client API non navigateur, l'origine présente doit être approuvée. La façade web réutilise le cookie et les contrôles CSRF Django C03, avec contrôle d'origine des mutations. Les requêtes GET n'appellent pas la garde Auth réservée aux opérations POST.

Les racines de contexte sont `/platform`, `/tenants/{tenant_id}` et, pour les objets effectivement scopés, `/tenants/{tenant_id}/scopes/{scope_id}`. Le contexte PLATFORM ne reçoit aucun tenant inventé. Le contexte TENANT est construit depuis le chemin et vérifié dans Core ; aucun en-tête, champ acteur, décision ou contexte client ne le remplace. Une contradiction de tenant est refusée avec un code stable.

Une Command possède une route POST distincte `<racine>/commands/<nom>`. Le tableau ci-dessous fixe les noms, services publics, DTO et actions ; command_type est l'action suivie de `:v1`. Toutes les méthodes reçoivent `command, envelope, ports, alias` en paramètres nommés. HTTP ne réimplémente pas leur callback transactionnel et n'appelle pas directement execute_mutation. Les références cibles sont dérivées des identifiants métier du DTO selon les formats canoniques Core ; aucune référence de permission ni action libre ne vient du client.

P = PLATFORM ; T = tenant racine ; S = scope déclaré du tenant. Une famille globale reste P même si son utilisateur possède un accord tenant. Les gardes des services et C04 restent l'autorité, y compris en cas de demande de création ou modification.

| Nom POST | Service Core | DTO | Action | Racines |
|---|---|---|---|---|
| create-user | services_identity.create_user | IdentityCreateUserInput | pixs.core.identity.user.create | P |
| create-identity | services_identity.create_identity | IdentityCreateIdentityInput | pixs.core.identity.identity.create | P |
| link-identity | services_identity.link_identity | IdentityLinkInput | pixs.core.identity.link.create | P |
| unlink-identity | services_identity.unlink_identity | IdentityUnlinkInput | pixs.core.identity.link.unlink | P |
| set-identity-state | services_identity.set_identity_state | IdentitySetStateInput | pixs.core.identity.state.set | P |
| logical-delete-identity | services_identity.logical_delete_identity | LogicalDeleteInput | pixs.core.identity.logical_delete | P |
| create-group | services_groups.create_group | GroupCreateInput | pixs.core.groups.group.create | P/T/S |
| change-group-persistence | services_groups.change_group_persistence | LogicalDeleteInput | pixs.core.groups.group.persistence.change | P/T/S |
| add-user-group | services_groups.add_user_group | UserGroupAddInput | pixs.core.groups.user-group.add | P/T/S |
| remove-user-group | services_groups.remove_user_group | UserGroupRemoveInput | pixs.core.groups.user-group.remove | P/T/S |
| activate-tenant-membership | services_groups.activate_tenant_membership | TenantMembershipAddInput | pixs.core.groups.tenant-membership.activate | T |
| revoke-tenant-membership | services_groups.revoke_tenant_membership | TenantMembershipRevokeInput | pixs.core.groups.tenant-membership.revoke | T |
| create-tenant | services_scope.create_tenant | TenantCreateInput | pixs.core.scope.tenant.create | P |
| create-scope | services_scope.create_scope | ScopeCreateInput | pixs.core.scope.node.create | T |
| move-scope | services_scope.move_scope | ScopeMoveInput | pixs.core.scope.node.move | T |
| declare-permission | services_authz.declare_permission | PermissionDeclareInput | pixs.core.authz.permission.declare | P |
| create-role | services_authz.create_role | RoleCreateInput | pixs.core.authz.role.create | P/T/S |
| set-role-permissions | services_authz.set_role_permissions | RoleCreateInput | pixs.core.authz.role.permissions.set | P/T/S |
| assign-role | services_authz.assign_role | RoleAssignInput | pixs.core.authz.role.assign | P/T/S |
| unassign-role | services_authz.unassign_role | RoleUnassignInput | pixs.core.authz.role.unassign | P/T/S |
| persist-policy | services_authz.persist_policy | PolicyPersistInput | pixs.core.authz.policy.persist | P |
| change-authz-persistence | services_authz.change_authz_persistence | LogicalDeleteInput | pixs.core.authz.state.change | P/T/S (selon la propriété de la référence) |

Schémas de requêtes : objets JSON fermés, champs obligatoires et types exacts des DTO ci-dessous, après retrait des champs `context` et `correlation_id` fournis par le serveur. Un champ tenant déjà déterminé par un chemin tenant est fourni par celui-ci ; une valeur client contradictoire est refusée. Les UUID sont des chaînes UUIDv7 canoniques ; enums par valeurs publiées ; tableaux JSON convertis en tuples après validation des éléments ; booléens distincts des entiers ; null seulement pour les annotations optionnelles. Policy utilise le décodeur public propriétaire fermé, aucun objet arbitraire. Les références métier opaques sont bornées par la configuration injectée et les gardes propriétaires. Aucun import de type ou appel de méthode n'est choisi depuis une chaîne client.

| DTO | Champs propriétaires |
|---|---|
| IdentityCreateUserInput | user_id: uuid.UUID, correlation_id: str |
| IdentityCreateIdentityInput | identity_id: uuid.UUID, identity_type: IdentityType, state: IdentityState, correlation_id: str |
| IdentityLinkInput | user_id: uuid.UUID, identity_id: uuid.UUID, correlation_id: str |
| IdentityUnlinkInput | user_id: uuid.UUID, identity_id: uuid.UUID, correlation_id: str, expected_version: int |
| IdentitySetStateInput | identity_id: uuid.UUID, state: IdentityState, correlation_id: str, expected_version: int |
| GroupCreateInput | group_id: uuid.UUID, context: ScopeContext, correlation_id: str |
| UserGroupAddInput | user_id: uuid.UUID, group_id: uuid.UUID, correlation_id: str |
| UserGroupRemoveInput | user_id: uuid.UUID, group_id: uuid.UUID, correlation_id: str, expected_version: int |
| TenantMembershipAddInput | identity_id: uuid.UUID, tenant_id: str, correlation_id: str, expected_version: int ou None |
| TenantMembershipRevokeInput | identity_id: uuid.UUID, tenant_id: str, correlation_id: str, expected_version: int |
| TenantCreateInput | tenant_id: str, correlation_id: str |
| ScopeCreateInput | scope_id: str, tenant_id: str, parent_scope_id: str ou None, correlation_id: str |
| ScopeMoveInput | scope_id: str, tenant_id: str, parent_scope_id: str ou None, correlation_id: str, expected_version: int |
| PermissionDeclareInput | permission_id: str, owner_component: str, resource_ref: str, action_ref: str, correlation_id: str |
| RoleCreateInput | role_id: str, context: ScopeContext, permission_ids: tuple[str, ...], correlation_id: str, expected_version: int ou None |
| RoleAssignInput | role_id: str, subject_type: str, subject_ref: str, correlation_id: str |
| RoleUnassignInput | role_id: str, subject_type: str, subject_ref: str, correlation_id: str, expected_version: int |
| PolicyPersistInput | policy: Policy, correlation_id: str |
| LogicalDeleteInput | resource_ref: str, target_state: DataPersistenceState, correlation_id: str, expected_version: int |

Idempotency-Key est obligatoire pour les mutations. Les identifiants de décision/opération sont générés serveur, corrélation générée serveur ou valeur opaque strictement bornée et validée ; causalité optionnelle validée. Ils ne deviennent pas des autorités et les identifiants de suivi ne modifient pas l'empreinte métier de rejeu.

Queries GET : P expose users/USER, identities/IDENTITY, links/LINK, permissions/PERMISSION, policies/POLICY, tenants/TENANT, bindings/BINDING, grants/GRANT ; P/T/S exposent groups/GROUP, user-groups/USER_GROUP, roles/ROLE, role-permissions/ROLE_PERMISSION, assignments/ROLE_ASSIGNMENT selon la propriété réelle ; T expose memberships/TENANT_MEMBERSHIP et scopes/SCOPE. Les tombstones ne sont pas exposés dans cette première surface. Chaque Query appelle query_identity, query_groups, query_scope, query_authz_data ou query_bootstrap ; cette dernière est une lecture protégée, jamais un effet R01. Action Query fixe pixs.core.<domaine>.read, domaines identity/groups/scope/authz-data/bootstrap selon services_queries ; référence collection_ref propriétaire.

Auth C03 : GET public `/api/v1/web/auth/csrf` ; sous les racines de contexte, POST `auth/login`, `auth/logout`, `auth/revoke-session`, avec `auth/renew` pour Bearer seulement. `auth/revoke-all` et `auth/change-password` sont publiés uniquement sous PLATFORM car compte et justificatif sont globaux. Le login tenant/scope utilise un intent logique Auth versionné reconnu après vraie preuve mot de passe, sans réétiqueter une identité Core ni modifier le resolver des ressources existantes. Les méthodes publiques login/invoke des façades C03 restent propriétaires de la transaction, des émissions et de leurs règles de rejeu. Le login est déclaré public avec authentification propre, jamais avec des faits d'acteur déclarés par le client ; récupération opérateur et réconciliation administrative ne sont pas publiées ici. Pas de journalisation de corps, mots de passe, tokens ni cookies.

### Pagination, filtrage et activité

Les listes restent filtrées par C04 à la source avant pagination et projection. Une extension interne compatible de CoreQueryInput/query_core/selected_rows ajoute after et page_limit avec défauts legacy inchangés. Le keyset s'applique en SQL à l'ensemble autorisé : WHERE autorisé puis comparaison lexicographique des clés déclarées, ORDER BY identique et LIMIT page_limit + 1 avant matérialisation. La ligne de réserve ne doit pas être exposée ; seule son existence produit un lien suivant. Aucun filtrage d'autorisation HTTP après retour de données. Le plafond de roster C04 reste une borne fermée : dépassement explicite, aucune omission silencieuse.

Le curseur propriétaire v1 est signé par Django avec une clé injectée, distincte des données publiques ; il lie contexte complet, sujet résolu, kind, filtre normalisé, snapshot, ordre, dernière clé et taille. L'expiration est bornée par la politique injectée et la validité de la décision ; toute falsification, expiration ou divergence entraîne une erreur stable et une reprise explicite. Aucun snapshot périmé n'accorde de droit.

C06 produit UserActivityEvidence après une activité interactive réellement terminée et autorisée, depuis un objet serveur non accessible aux entrées HTTP. Acteur/session/contexte/opération/date sont liés ; absence, échec ou répétition ne fabrique pas d'activité nouvelle. Heartbeat et renouvellement ne sont pas des activités. record_activity de C03 reste propriétaire de la prolongation et de sa déduplication. Aucun booléen client ne sert de preuve.

### Participant d'idempotence durable Core

Le participant implémente exactement IdempotenceParticipant. Il rejoint la transaction PostgreSQL du propriétaire et n'ouvre pas de transaction durable imbriquée. La clé conserve tenant résolu, sujet résolu, command_type et clé opaque ; un namespace physique PLATFORM/TENANT évite toute collision, tenant NULL pour PLATFORM, unicité NULLS NOT DISTINCT. ScopeContext et serializer_version sont liés au contenu canonique et une divergence sous même clé refuse tout nouvel effet.

Le sérialiseur public versionné appartient à Core et produit des octets JSON UTF-8 stricts, triés et compacts, sans float, avec règles explicites pour UUID/enums/dates/null/tuples. L'empreinte inclut commande et contexte métier ; exclut les nouveaux identifiants de suivi. Serializer 1.0.0 est figé pour les entrées ; modification incompatible = nouvelle version et stratégie explicite.

check_or_stage vérifie unicité/empreinte et prépare IN_PROGRESS ; restore_confirmed restitue le CoreMutationResult complet enregistré après contrôle actuel ; stage_result n'accepte que le résultat propriétaire confirmé. Les échecs propriétaires suivent rollback et audit de refus existants ; aucune fausse entrée REJECTED n'est fabriquée avec un DTO de succès. Conflit = code stable 409, aucun effet ; report_conflict garde la signature publique. verify_staged exige même alias, transaction physique/xid, jeton, contexte et opération ; une preuve dans un autre savepoint ou une transaction terminée n'est pas un commit.

Une contrainte déclenchée PostgreSQL différée AFTER INSERT OR UPDATE relit la ligne finale et interdit tout IN_PROGRESS engagé. Un CHECK DEFERRABLE inexistant ne sera pas utilisé. La migration additive 0003 dépend de 0002_core_audit ; elle ne réécrit pas les migrations historiques. Retour refusé si données à préserver ; aucune rétrogradation automatique. Le runner initial C02 n'est pas élargi implicitement.

reconcile_unknown ne réexécute jamais la mutation : lecture persistante sur connexion réconciliée, puis chemin restore_only de Core et contrôle actuel des autorités. L'absence de preuve reste ISSUE_INCONNUE. La rétention injectée couvre la fenêtre de rejeu après résultat ; aucune purge C06, donc aucun hold C10 contourné.

### Réponses, contrats et composition

Succès JSON : data/meta/links ; Command 200 seulement après résultat propriétaire connu, aucune route asynchrone ajoutée. Erreurs : error_code versionné stable, message catalogué localisable, details et correlation_id sans valeurs sensibles ni trace interne ; field_errors peut préserver l'extension existante déclarée. Les réponses C06 et Auth restent no-store ; aucun fallback HTML API. Les anciens helpers isolés conservent leur comportement hors nouvelles routes.

Le document OpenAPI 3.1.0 publié à `/api/v1/openapi.json` porte version de contrat 1.0.0, méthodes, chemins, schémas, refus, modes d'authentification et protections réellement exposés. Une comparaison structurelle inspecte retraits de routes/méthodes, auth, required/types/enums et réponses ; elle ne se contente pas du booléen breaking de ApiContractPlan. Une rupture sans nouvelle majeure est refusée par la validation de construction du document et sa recette ; coexistence déclarée pour nouvelle majeure. Le contrôle serveur compare routes et réponses au contrat publié. Réutiliser build_openapi_view et son plafond ; si le contrat complet dépasse la borne, publication par documents de capacités bornés avec index explicite, sans tronquer silencieusement.

La composition reçoit explicitement alias PostgreSQL, ports Core, service/sources Auth C03, horloge, origine/hôte approuvés, politiques de taille/page/curseur/rétention et clé de signature. Aucun bind/listen, settings.configure, secret lu, provider choisi implicitement, ni accès aux tables privées Auth. La requête construit une source AuthInvocationSource vérifiée et les vrais composants C04/C05 ; fermeture et révalidation de l'invocation sont requises. Outbox C09, déclarations/gouvernance C10 restent injectés ; absence d'un port nécessaire = refus fermé. Les doubles des recettes sont nommés comme tels et ne qualifient pas la livraison C09/C10 ni P0.

Les profils de test utilisent des valeurs explicites bornées (page 2/max 10, plafond de payload 64 KiB, curseur 60 s, fenêtre de rejeu 3600 s, références 128 caractères), sans les promouvoir en valeurs par défaut de déploiement. Toute contrainte supérieure C03/C04/C05 prime et est testée. Aucune dépendance nouvelle.

### Fichiers et preuves attendus

Nouveaux :
- src/pixs/backend/api_core_catalog.py
- src/pixs/backend/api_core_views.py
- src/pixs/backend/api_core_composition.py
- src/pixs/backend/api_core_pagination.py
- src/pixs/backend/api_core_errors_catalog.py
- src/pixs/backend/api_core_openapi.py
- src/pixs/backend/api_core_openapi_compare.py
- src/pixs/backend/api_core_activity.py
- src/pixs/core/api_core_serializer_v1.py
- src/pixs/core/api_core_idempotency_values.py
- src/pixs/core/api_core_idempotency_record.py
- src/pixs/core/api_core_idempotency_repository.py
- src/pixs/core/migrations/0003_core_idempotence.py
- tests/unit/test_api_core_pagination.py
- tests/unit/test_api_core_serializer.py
- tests/unit/test_api_core_errors.py
- tests/unit/test_api_core_openapi.py
- tests/integration/test_api_core_idempotence_postgres.py
- tests/integration/test_api_core_platform_postgres.py
- tests/integration/test_api_core_tenant_postgres.py
- tests/integration/test_api_core_auth_postgres.py

Existants : src/pixs/core/dto.py, src/pixs/core/query_source.py, src/pixs/core/services_queries.py, src/pixs/core/models.py ; README du backend API et dossier C06 pour conception, tâches et preuves. Toute nécessité supplémentaire est présentée et validée séparément par CGPT avant écriture. Aucun component.toml ni migration_lock.py modifié sans justification distincte.

Recettes : unitaires des valeurs/serializer/curseurs/erreurs/contrats ; PostgreSQL réel isolé pour commit/rollback/concurrence/conflit/commit perdu/guard final ; parcours ordinaires et Super Admin via Auth C03+C04+C05, filtres SQL avant LIMIT, CSRF/cookie/Bearer/ambiguïtés, refus privés et intertenant, activité admissible, réponses et OpenAPI concordants. Les doubles C09/C10 sont explicitement distingués des intégrations réelles. Régressions pertinentes C02/C03/C04/C05 et helpers API, syntaxe, cohérence OpenSpec stricte et UTF-8/LF sont requises. Une preuve absente reste absente.

Archivage seulement après critères prouvés et revue ; mandat séparé, puis STATISTIQUES.md distinct vérifié à six sections, publication, gate et arrêt ciblé. Aucun Git, prochain change, déploiement de production ou arrêt des services communs.



## Réalisation vérifiée du 22 octobre 2026

La réalisation C06 est autorisée dans le RUN
`cismp5-pixs-1f3e128ad89f45a9`, job
`cismp5-c06-34960d24111a4362`. Les barrières de conception initiales ont
été levées par la conception du 21 octobre et les NFDOC complémentaires
validés par CGPT avant écriture. Aucun delta de canon n'est introduit ;
`.openspec.yaml` déclare `skip_specs`. Les sections historiques datées
restent des constats de préparation, sans valoir résultat actuel.

### Surface et construction contractuelle

Le catalogue public ferme 22 commandes et 15 collections, soit 156 opérations
dans leurs contextes et façades réellement publiés. Les deux fabriques
publiques HTTP exigent la référence contractuelle antérieure approuvée.
La comparaison structurelle précède leur construction et calcule les
ruptures au lieu d'accepter un booléen de l'appelant. OpenAPI 3.1.0,
version de contrat 1.0.0, index et documents de capacités sont préchargés,
chacun limité à 64 Kio avec taille/SHA-256 vérifiables. Le helper historique
conserve signature, exports, profil et comportement ; seuls chargement JSON
et transport privés sont mutualisés.

La catégorie Auth est ADMIN, fixée par le serveur. PLATFORM conserve le
login legacy et les opérations globales de compte/justificatif. Tenant/scope
utilisent les opérations de session. Revoke-all et change-password ne sont
pas publiés dans ces contextes : leurs ressources restent globales.
Les huit routes globales T/S du prototype de conception ont été retirées
avant toute publication ; la référence finale couvre 156 opérations.

### Corrections de raccordement nécessaires

Les NFDOC et décisions préalables sont conservés dans le checkpoint du RUN.

- C03 : avec une horloge réelle, l'authentification précède la création de
  session. Le vérificateur contrôle séparément création et authentification
  antérieures à la dernière activité, elle-même non future ; expiration,
  fraîcheur, générations et assurances ne sont pas diminuées.
- Auth tenant/scope : `session_creation_reference` produit un identifiant
  logique versionné liant sujet et contexte complet. `AuthInvocationSource`
  ne reconnaît cet intent qu'après vraie revalidation de mot de passe,
  sans session/token, pour session.create et sous liaison requête/alias/
  opération. Le resolver des ressources existantes n'est pas modifié.
  L'identité Core n'est jamais réétiquetée. La référence ne donne aucun droit :
  absence de politique et contexte/opération substitués restent refusés.
- C04 : la création/composition d'un rôle revalide une permission déjà
  déclarée. Le validateur accepte sa réutilisation seulement si ACTIVE et
  de définition exactement identique, sous verrou de ligne. Une permission
  différente ou inactive est refusée. Le propriétaire Core conserve sa garde
  de création contre doublon ; les reçus d'objet/TX/savepoint sont inchangés.

Les compléments de fichiers validés concernent
`src/pixs/auth/api_request_source.py`, `identifiers.py`, `invocation.py`,
`services.py`, `runtime_verifier.py`,
`src/pixs/core/services_runtime_declarations.py`,
`src/pixs/backend/openapi_document_view.py` et la recette unitaire dédiée
aux valeurs idempotentes. Aucun fichier généré OpenCode, configuration,
manifest de composant, migration historique ou règle canonique n'est modifié.

### Activité, transaction et reprise

La politique de commandes web interactives est un frozenset serveur
explicite. Après un premier résultat Core confirmé, C06 fournit une preuve
éphémère liée à l'acteur, la session, le contexte, l'opération et la date ;
C03 possède revalidation, déduplication et prolongation. Renew, query
d'arrière-plan et rejeu n'ajoutent pas d'activité. Un échec distinct de suivi
est signalé dans meta.activity sans altérer le résultat Core déjà confirmé
ni prétendre prolonger la session.

Le participant C06 rejoint la transaction propriétaire avec C05 et les
participants requis. Le trigger PostgreSQL différé relit l'état final et
interdit IN_PROGRESS engagé. Le résultat complet initial est conservé.
La perte d'acquittement est réconciliée sur connexion dédiée sans réappliquer
la mutation. Aucune purge de rétention n'est ajoutée ; la migration 0003 est
additive et son retour refuse les données idempotentes à conserver.

### Preuves finales examinées

| Contrôle | Résultat observé | Effet natif |
| --- | --- | --- |
| Neuf recettes PostgreSQL C03/C04/C06 | 192 cas vrais, cleanup et conns_closed vrais | `call_01a1612c0a267426b2a7213b01d628b0` |
| Unitaires C06 et helpers/plans/contrats historiques | 166 tests OK | `call_01a1612dc5ca722cbd04fc7b39425507` |
| Syntaxe de tous fichiers Python modifiés | 33 fichiers compilés, cache de preuves réservé | `call_01a1612f3f457159936f1edc70d3509c` |
| Change OpenSpec avant alignement documentaire | strict valide, zéro delta accepté | `call_01a161311fd4740682a8e9bf65c6c538` |

La recette finale comprend 80 cas PG C06 (30 idempotence, 10 bridge Auth,
19 plateforme et activité, 21 tenant/scope/Root) et 112 cas de régression
(98 C03, 14 C04). Le vérificateur C03 historique déclare ses doubles de
faits/confiance ; les parcours applicatifs C06 exécutent les vrais
C03/C04/C05/Core/C06. Les sorties et empreintes sont conservées dans
`output/cismp/cismp5-pixs-1f3e128ad89f45a9/state.json`.

### Frontières de qualification et clôture

Les schémas PostgreSQL sont privés, jetables et nettoyés ; la version
réellement observée est 16.14 (160014), Django 6.1.2. L'inventaire DEVOPS
d'une autre version ne remplace pas cette preuve. Les requêtes
RequestFactory et ASGI s'exécutent en processus, sans serveur ni TLS réseau.
C09/C10 sont des doubles explicitement nommés dans ces recettes ; les lignes
C08 de binding/grant servent de setup et ne qualifient pas R01.
Le frontend, le packaging/distribution C17/C19, les jobs/Bulk asynchrones et
une activation P0 complète ne sont pas livrés par C06.

Git, déploiement et prochain change ne sont pas autorisés ici. L'archivage
C06 puis STATISTIQUES.md, la publication CAB, le gate, le désarmement et la
libération restent des étapes terminales distinctes : aucune n'est réputée
accomplie par la seule réussite des tests. La garde d'autorisation de 3.4 est
respectée ; le rapport post-archive demeure obligatoire avant TERMINÉ.
