# Conception — C04

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : authorize et source-filter-plan-v1 fournissent un PDP et un plan préparatoires ; l’intégration PEP Django et l’exception Super Admin opérationnelle ne sont pas démontrées.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/core/authz/decision.py](../../../src/pixs/core/authz/decision.py).
- [src/pixs/core/authz/filter_plan.py](../../../src/pixs/core/authz/filter_plan.py).
- [src/pixs/core/authz/snapshot.py](../../../src/pixs/core/authz/snapshot.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Reconnaître le seul compte fonctionnel authentifié à la frontière runtime, avec accords tenant explicites. Conserver les profils structurels sans privilège. Pour comptes ordinaires, appliquer DENY/ALLOW/refus par défaut et obligations PEP ; filtrer à la source avant pagination. Propager acteur initial et périmètre sans credentials délégués.

## Décisions C03 raccordées le 20 octobre 2026

Les [décisions C03 D01–D17](../add-initial-authentication-and-sessions/design.md) conservent les assurances réellement obtenues et toutes les exceptions canoniques du Super Admin. Les durées et plafonds choisis pour les administrateurs ordinaires ne sont pas une restriction nouvelle implicite de ce compte.

Le [delta authorization adopté le 20 octobre 2026](specs/authorization/spec.md) précise la branche R01 pré-session C03/C04/C08/C02 : sujet opérateur distinct du compte cible, clé publique personnelle préautorisée, mapping et politique d’installation versionnée fermée, signature Ed25519 vérifiée avec cryptography. Clé, signature, installation, plan, actions et validité doivent correspondre ; la seule validité cryptographique ne donne aucun droit. Cette branche ne prolonge pas l’exception technique C01 et n’ouvre aucune opération métier ordinaire.

L’autorisation finale de 10 minutes part de la validation du plan final et est consommée avec le commit propriétaire des effets autorisés. La préparation complète n’est pas limitée à dix minutes. Autre plan/cible, expiration ou révocation exigent une nouvelle autorisation ; une réponse perdue impose inspection du résultat, sans second compte ni effet dupliqué. Politique de confiance, enrôlement des clés, sérialisation signée, signatures de ports et mapping exact restent à qualifier avant code.

D14 retire seulement le blocage dû à une panne du seul audit pour une déconnexion/révocation Auth admissible selon le [delta C05](../add-durable-minimized-audit/specs/audit/spec.md). L’acteur, la permission, le périmètre et les invalidations automatiques de confiance restent vérifiés ; DENY et refus par défaut restent applicables. Aucune connexion, élévation ou réactivation sans audit n’en découle. Les deltas de cette décision sont adoptés au canon le 20 octobre 2026, sans implémentation.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Reconnaissance du compte unique, persistance des accords tenant, interprétation des obligations et protocole de dérogation/audit avec C05 ; conception transversale à revoir avant modification du runtime.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).

- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) : dépendance renforcée après revue des obligations d’audit.

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

DENY/ALLOW et refus par défaut ordinaires ; tenant non accordé refusé même au Super Admin ; tenant accordé et dérogations testés ; même sémantique API/CLI/panneau/asynchrone ; obligations PEP réellement honorées.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T06 — Marqueurs externes et états PostgreSQL

Marqueur d’installation et marqueur de désactivation Super Admin ont des fonctions différentes et ne sont pas une transaction atomique avec PostgreSQL. Compléter C08 et les contrats C03/C04/C09 ; N05 vérifie le rapprochement après restauration.

Contrôles à intégrer : Commit base avant marqueur : reprise sans second compte ; Marqueur absent/invalide interdit NORMAL sans relancer INSTALLER ; Désactivation non dérogée refuse nouvelles actions/reprises, transaction engagée préservée ; Secours propre sans MFA imposé.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T09 — Contexte tenant et réponse retardée du navigateur

L’invalidation est prévue ; les réponses en vol, onglets et changements de session doivent être inclus dans le contrat de concurrence UI. Compléter C11 et sa recette ; pas d’offline, cache distribué ou client natif imposé.

Contrôles à intégrer : Réponse du tenant précédent n’alimente pas la vue courante ; Déconnexion et révocation invalident contexte ; Identifiant/header fourni ne remplace pas le tenant canonique.

### T10 — Mutation, audit, idempotence et outbox

Les composants prévoient chacun leur partie ; la frontière transactionnelle et l’échec avant/après commit doivent être explicitement communs. Compléter contrats C05/C06/C09 avec refus distincts et résultat réconcilié ; pas de nouveau broker.

Contrôles à intégrer : Rollback sans événement publié ; Commit puis réponse perdue restituant résultat idempotent ; Double livraison sans double effet propriétaire ; Refus auditable sans mutation métier.

### T16 — Options, profils structurels et renvois Bulk

Un rattachement à un lot P0 n’active pas tout le domaine : Bulk, LDAP, flags avancés, quotas, SDK, sandbox et intégrité avancée restent conditionnés. Déclarer sélection/absence et maintenir les profils structurels existants ; ne pas traiter la non-sélection comme dispense d’une clause applicable.

Contrôles à intégrer : Absent représenté sans readiness fictive ; Contrat consommé réutilisé sans activer tout le catalogue ; Aucun code distant ni composant DEVELOPMENT en production ; Pas de promesse universelle de performance/HA.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.


## Addendum de réalisation ISMP C04 — 20 octobre 2026

Le RUN 1CISMP3 autorise la réalisation de ce seul change, puis ses validations,
son archive et ses statistiques. Le statut de préparation ci-dessus décrit
l’état initial. Cet addendum précise la mise en œuvre des exigences déjà
adoptées ; il ne crée aucune norme, dépendance ni activation supplémentaire.

### Ports et sources de confiance

C04 implémente `AuthorizationDecider`, `SourceFilterProvider` et
`DeclarationValidator` déclarés dans `pixs.core.ports`. Leurs paramètres sont
conservés. Les faits C03 sont résolus par `TrustedFactsProvider.resolve` ;
une forme de DTO correcte ne prouve jamais leur origine ni leur fraîcheur.
Le catalogue, les limites, les policies et la topologie sont explicitement
fournis par la composition backend et recoupés avec les données propriétaires
Core, sans QUERY cliente circulaire. Les limites existantes sont réutilisées,
sans valeur implicite ou variable runtime nouvelle.

Les contrats PDP purs `authorize`, `plan_filter`, `Snapshot`,
`AuthenticationContext` et `TrustedFacts` restent inchangés. L’intégration
runtime appelle ces primitives pour les comptes ordinaires : DENY, ALLOW,
puis refus par défaut ; seules les obligations AUDIT du profil v1 sont
acceptées. Une décision expirée ou des faits non vérifiables sont refusés.
Le PEP réévalue sous verrous avant effet ; aucun résultat d’un frontal ne
constitue une décision backend.

### Compte fonctionnel et dérogations

La reconnaissance du seul Super Admin relie authentification propre C03,
identité Core active et binding unique de l’installation. Aucun rôle déclaré
par l’appelant, compte de service ou autre identité ne reçoit ce privilège.
Le contrôle est total dans PLATFORM. TENANT exige le grant explicite actif
existant ; une fois cet accord vérifié, les refus ACL du tenant ne bloquent
pas ce compte. Aucun autre tenant ni compte n’en bénéficie. Les modèles et
services Core de binding et de grants sont réutilisés.

Les dérogations d’audit et de gouvernance sont demandées explicitement dans
la composition backend liée à la requête, l’acteur, l’alias et l’opération.
`audit_waived` et `governance_waived` les recontrôlent avec la décision fraîche.
Une décision ou un booléen client ne crée pas une dérogation. L’indisponibilité
d’audit ne bloque pas une dérogation Super Admin admissible ; aucun audit
absent n’est présenté comme réalisé. Le privilège du compte reste permanent,
sans mécanisme d’élévation temporaire par opération.

### Filtrage et frontières Django

`CoreFactReader.candidates/read_facts` fournit les seules données internes
nécessaires. Les lots sont homogènes, bornés et déterministes. Le plan source
est appliqué en SQL avant pagination, comptage ou export ; les ressources
interdites ne sont jamais chargées puis filtrées dans le frontal. Snapshot,
contexte, version et fraîcheur sont recontrôlés avant restitution ou mutation.
Une erreur ou un dépassement de borne produit un refus fermé.

Les adapters Django de C04 constituent le PEP commun consommable par les
façades API, CLI, panneau et asynchrone. C04 ne crée aucun endpoint, worker ou
panneau appartenant à C06/C09/C13. La propagation future conserve l’acteur
initial et son périmètre, sans transmettre ses credentials ni transférer le
compte Super Admin.

### Opérateur R01 disjoint — accord technique C03/C04

Le chemin commun Core exigeait `TrustedFacts.auth` de type exact
`AuthenticationContext` et une identité applicative. Pour respecter R01 sans
fabriquer cette identité, C04 fournit le DTO pur disjoint
`pixs.core.bootstrap_operator.BootstrapOperatorFacts`, immuable, sans repr des
valeurs, ni identité/session/assurance applicative. Il porte sans défaut :
`operator_subject_ref`, `resource_id`, `action_id`, `context`,
`installation_ref`, `plan_version`, `authorized_actions`, `closed_effects`,
`operator_proof_ref`, `authorization_ref`, `operation_id`,
`target_identity_ref`, `target_tenant_ref`, `plan_sha256`, `valid_from`,
`expires_at`, `key_id`, `trust_policy_version`, `consumed_operation_id`.

`authorized_actions` désigne les actions publiques permises ; `closed_effects`
désigne les seuls effets du plan propriétaire. Le contexte est PLATFORM sans
tenant/scope. `valid_from` est la validation du plan final ; `expires_at` vaut
`valid_from + 600 secondes`. C03 vérifie Ed25519, clé préautorisée, mapping et
confiance courants avant de construire ces faits ; le validateur structurel
ne réalise ni cette preuve ni l’autorisation C04.

Seul le retour d’`OperatorProofVerifier.verify` est étendu à
`TrustedFacts | BootstrapOperatorFacts` ; ses paramètres sont conservés.
L’adaptation minimale des services Core accepte le nouveau type uniquement
avec `BootstrapServicePorts` et sa source propriétaire R01. Voie ordinaire et
PDP purs le refusent. L’acte, le plan final, l’opération, l’installation,
les cibles, actions et effets sont comparés avant décision et sous verrous.
Le hash du plan n’est pas assimilé sans preuve au hash de l’enveloppe.

C03 conserve la preuve et sa consommation chez Auth. `CredentialStamper`
participe au commit propriétaire avec l’opération ; la consommation R01 est
atomique avec les effets Core/C08. Aucun acquittement mémoire ne vaut commit.
Une preuve consommée ne permet aucun nouvel effet. Une reprise de la même
opération inspecte le résultat persistant avec C08 et réconcilie toute issue
inconnue avant restitution ; aucun second compte ou double effet. Autre plan,
cible, expiration ou révocation exige une autorisation nouvelle.

### Audit et preuves de sortie

C05 conserve ses signatures `AuditParticipant.stage/verify_staged/` 
`reconcile_unknown`. `stage` participe à la transaction PostgreSQL propriétaire
déjà ouverte ; `verify_staged` ne prouve que sa présence dans cette transaction.
Le commit est prouvé après la frontière propriétaire. La réconciliation
indépendante retourne CONFIRMED, ABSENT ou UNKNOWN sans rejouer la mutation.
Le retrait Auth D14 reste propriété C03 ; aucune panne d’audit ne permet de
connexion, élévation ou autorisation ordinaire nouvelle.

Les recettes C04 couvrent primitives existantes, runtime ordinaire, binding,
grants, dérogations, filtrage SQL, refus fermés et branche R01. Les doubles
C03/C05/C08/C09/C10 éventuels sont explicitement identifiés comme tests et ne
prouvent pas la livraison de ces propriétaires. L’intégration effective attend
leurs contrats et conditions prouvés ; aucun P0 complet n’est annoncé.
La syntaxe, les suites applicables, PostgreSQL réel isolé et les empreintes
des canons sont vérifiés avant archive. Aucune tâche n’est cochée sans preuve.

### Raccordement concret Auth et propriété des métadonnées — 21 octobre 2026

Le producteur de TrustedFacts est C04. AuthInvocationSource, propriétaire
C03, fournit revalidate(origin_request, alias, operation_id) avec les seuls
AuthenticationContext et RevocationStatus réellement vérifiés, ainsi qu'un
resolver de propriété Auth depuis ses lignes. Le composite C04 n'invente
aucun niveau d'assurance. Pour les candidats d'un lot, acteur, action,
contexte et corrélation restent ceux de l'invocation ; la preuve Auth est
toujours revérifiée sur sa requête d'origine. close appartient au finally
du traitement serveur englobant. Les namespaces externes sont enregistrés
explicitement ; aucune table privée Auth/Audit n'est importée dans Core.

La propriété du registre de contrôle ne se confond pas avec l'identifiant du
périmètre qu'il décrit. Le contrat interne retenu pour les métadonnées Core
est le suivant, d'après les opérations propriétaires déjà livrées :

| Métadonnée | Propriété de son enregistrement de contrôle |
|---|---|
| User, Identity, Link, Permission, Policy, Binding | PLATFORM |
| Tenant du registre et accord tenant du Binding | PLATFORM ; le tenant référencé est une cible de gestion |
| Nœud de scope du registre topologique | TENANT racine, scope_id absent ; le scope_id de la ligne désigne le nœud décrit |
| Group, Role, RoleAssignment | Colonnes scope_type, tenant_id et scope_id de la ligne |
| UserGroup et RolePermission | Périmètre du Group ou du Role propriétaire |
| IdentityTenantMembership | TENANT racine désigné par la relation |
| Tombstone | Références tenant/scope propres, ou PLATFORM si absentes |

create_tenant exige déjà PLATFORM ; create_scope/move_scope exigent le
tenant racine ; les accords du Binding sont gérés depuis le contrôle de
l'installation. Cette qualification concrétise la propriété unique du canon.
Elle ne donne aucun accès au contenu métier d'un tenant non accordé.
CorePageItem.context reste une donnée typée de projection C02, jamais la
preuve d'une autorisation. Le filtre vérifie les seules colonnes de
propriété avant de matérialiser les données autorisées.

Une création sans ligne préexistante n'est résolue que pour les actions Core
fermées de création et les références canoniques qu'accepte le service
propriétaire. Pour les relations, les parents réellement existants sont
recoupés. Cet intent ne constitue ni authentification, permission ou preuve
de création réussie ; les DTO et gardes du service Core bornent les effets.
Toute autre ressource absente ou sans propriétaire enregistré reste fermée.
La propriété pré-effet est épinglée à l'invocation, la connexion et la
transaction/savepoint natifs ; aucun jeton client ne prouve ce contexte.
Auth et révocation sont revérifiés à chaque appel, sans cache de DTO admis
entre transactions.

### Finalisation des transitions Auth déjà admises

Pour renew, logout, revoke, revoke_all, credential.change et
credential.recover dans le namespace pixs.auth, un contrôle final distinct
verify_final_transition est disponible sur le decider runtime. Il exige la
Decision ALLOW exacte émise avant effet sous la même connexion, identité
SQL et pile de savepoints, la même requête et opération, une décision encore
valide et les gardes/snapshot Core inchangés. Le vérificateur privé Auth
recoupe ensuite l'intent, ses versions et l'état SQL réellement attendu ;
son retour doit être exactement None. Les contrôles sont répétés avant
sortie. Cette opération n'accorde ni nouvel accès ni acquittement de commit.

Le justificatif retiré n'est jamais projeté ACTIVE pour les appels ordinaires.
session.create et toute autre action gardent la revalidation complète. C03
reste propriétaire des effets, du résultat distinct de retrait D14, des
preuves C05 et du commit. Une réaction défensive à un refresh déjà consommé
ne fabrique aucune authentification ou décision ALLOW depuis ce refresh.
