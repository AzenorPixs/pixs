# Validation de réalisation — C04

Date : 21 octobre 2026. RUN : cismp3-pixs-f2197224acbc47c0.
Change unique : integrate-runtime-authorization-and-super-admin.

## Résultat et périmètre

Les adapters Django Core C04 sont réalisés : source composite de faits,
chargement des policies et permissions de rôles, décision ordinaire,
reconnaissance du compte fonctionnel, accords tenant, dérogations explicites,
filtrage à la source, validation des déclarations et branche R01 disjointe.
Les profils purs restent réutilisés. Une décision d'admission ne confirme
jamais un accès, une consommation ou un commit à elle seule.

Aucun endpoint, panneau, worker, broker, schéma Auth, migration Core nouvelle,
dépendance ou opération Git n'est livré par ce change. Les hôtes de composition
C07, les façades C06/C13, les effets C08/C09/C10 et la qualification C17/C19
conservent leurs propres critères. Aucun P0 global prêt n'est déduit de C04.

## Changements examinés

| Groupe | Fichiers du projet |
|---|---|
| PDP partagé | src/pixs/core/authz/decision.py : préparation interne commune ; authorize et plan_filter publics conservent leur audit et leurs profils |
| R01 sans compte cible | bootstrap_operator.py, services_bootstrap_facts.py, services_runtime_bootstrap.py ; extension disjointe du résultat OperatorProofVerifier ; verify_operator_binding C08 fermé par défaut |
| Gardes PEP | services_common.py, services_transactions.py, services_bootstrap.py ; préparation Core avant Auth, double réévaluation et restauration avant tout nouvel apply |
| Runtime | services_runtime_store.py, services_runtime_decider.py, services_runtime_filter.py, services_runtime_declarations.py, services_runtime_facts.py |
| SQL | services_authorization_guard.py : partage/exclusion catalogue par base/schema, identité native de transaction, aucun droit déduit du verrou |
| Recettes | tests/unit/test_bootstrap_operator.py, test_core_bootstrap_r01.py, test_runtime_authorization_admission.py et huit harnais tests/integration/test_runtime_*.py de C04 |

Les effets natifs unitaires, contenus SHA-256, bases examinées, once et libérations
sont conservés dans le checkpoint du RUN. Les modifications de C01/C03/C05 et
autres RUN ne sont pas attribuées à C04. Aucun commit, branche, push ou diff Git
n'est utilisé comme preuve de cette réalisation.

## Vérifications exécutées

Les commandes ont été exécutées par OpenCode dans la session persistante
ses_ea58912eeffeqSU1dq1rUdGWyZ, après décision CAB explicite et protection
resource-scoped-v1. Python projet .venv, Python >=3.12 conservé ; PostgreSQL
observé 16.14 et Django observé 6.1.2. Les caches sont isolés sous
tests/runtime/c04-cache. Les seuls processus de recette chargent les cinq
variables PG autorisées ; leurs valeurs ne sont pas émises.

| Vérification | Résultat observé | Partie native |
|---|---|---|
| Régressions unitaires Core/PDP/identités/scopes/audit | 192 tests réussis sur le code courant, 25 compilations et 28 fichiers UTF-8/LF | prt_15c1f237e001U4gfistvx75LNk |
| Catalogue SQL partagé/exclusif | 10 cas PG, schémas isolés, rollback et indépendance des namespaces | prt_15b8b6263001jJXvp2NXSHLuQr |
| Store/decider | 27 cas PG, DENY, trois types de rôles, Root, grants, receipts, native TX et savepoints | prt_15ba793b4001iLs1MR16UWQFx5 |
| Filtre et PEP Core/C05 | 18 cas PG, query_core et filter_audit réels, audit commun, absence de faux ack et roster épinglé | prt_15bc90395001fP4VTpF6vCwr9z |
| Déclarations | 14 cas PG : lignes SQL réellement présentes, reçus copiés/rejoués, substitution et version active ambiguë refusées | prt_15bdffff7001g5l3hkACXlYxjT |
| R01 disjoint | 14 cas PG : absence de cible/session au moment d'autoriser, fenêtres/plan/cibles/consommation/reprise, aucune dérogation Root | prt_15bf02f280016PG7tflXE02WfT |
| Composite et contrôle final Auth | 12 +10 cas PG ; répétition des 18 filtres et 27 store : 67 succès, quatre nettoyages et fermetures | prt_15bffd955001ys12tDbICFNx7H |
| Fraîcheur Auth et contrôle final | 8 +10 cas PG, date observée, seuil strict, Root prouvé, expiration conservée | prt_15c0a4237001K1xx2DFDdQ7VK5 |
| Non-régression C02 | Identité20, topologie/authz46, transactions14, queries62, bootstrap58 : 200 cas métier ; migrations complètes et 12 garanties exercées | prt_15c0e317d001delzbV3jCLOkH7 |
| OpenSpec | C04 strict valide ; corpus191/191 (113 changes,78 specs), aucune erreur ; huit exigences du delta déjà identiques au canon | prt_15c10f4cc001lPfHNBqyMPgXk8 |

Les harnais C04 représentent 113 scénarios PG distincts. Les répétitions de
régression ne sont pas additionnées à ce total. Chaque recette est isolée
dans ses propres schémas possédés et ferme ses connexions ; real_pg, cleanup
ou cleanup_ok et conns_closed sont vrais. Les 200 scénarios C02 et la recette
de migrations sont des contrôles de compatibilité séparés.

## Preuves communes et limites des doubles

C05 est livré à la référence CAB51. Les sources effectivement consommées
audit_sink.py et audit_access.py ont été recoupées avec leurs empreintes
8114fd5768b1633ae8c0e0d065b8d820b51cdd1b6db46d8f27f8696a46320926 et
c38a79104ead9b7bbf657ad7e54174ab39f51e8a2ea87713d8a2e7981527ee8e.
L'archive C05 du 21 octobre, VALIDATION.md et STATISTIQUES.md existent.

Le banc commun propriétaire C03 test_auth_core_audit_postgres.py a réussi
14 cas PG réels avec Auth, CoreFactSource, RuntimeBootstrapDecider et
PostgresAuditParticipant. Partie native prt_15bfd60b6001vzTaD692eOPNek,
recoupée directement : code0, migrations Core/Auth, namespace, nettoyage et
fermetures vrais. Signature invalide et plan substitué sont refusés ;
l'audit est durable ; une capacité C05 insuffisante annule Core/Auth et
consommation ; le peer ne voit pas le stage avant commit. Le plan C08,
la classification et l'assurance restent des fixtures explicites :
full_c08_c10_delivery=false.

Dans les harnais propres C04, Auth/C08/C10/Idempotence/Outbox sont des doubles
lorsqu'ils ne sont pas annoncés comme composants réels dans le tableau.
Ils ne prouvent pas les sessions ni les services Auth, un plan C08 de
production, une classification C10 ou un outbox C09 livré.
Le même banc commun a ensuite réussi 21 cas, dont les sept cas supplémentaires
du composite réel RuntimeTrustedFactsProvider/AuthInvocationSource,
CoreAuthorizationStore/RuntimeAuthorizationDecider : préadmission hors TX puis
transaction propriétaire, propriété Auth réelle, revalidation finale, fraîcheur,
audit commun et révocation Core après frontière. Partie native
prt_15c219d16001TUYoqUW4d5vuXs recoupée directement, code0, migrations,
namespace, nettoyage et fermetures vrais. Ces 21 cas réexécutent les 14
précédents : ils ne sont pas additionnés comme 35 cas distincts. Catalogue et
Policy persistées sont des fixtures déclarées, ainsi que trust/assurance ;
aucune session, C08/C10 complet ou disponibilité de l'hôte n'en est déduite.

## Allocation aux critères

| Critères C04 | Réalisation/propriété et preuves |
|---|---|
| SRAC, DENY puis ALLOW puis refus, conditions/assurances/temps/limites | Profils purs inchangés, 192 tests et store/decider27 ; aucune dimension d'assurance inventée par Core |
| Compte fonctionnel unique actif, plateforme et accords tenant | Identité Core active non SERVICE et Binding d'installation ; tenant non accordé refusé même avec ACL ALLOW ; accordé malgré DENY ; tests store27 |
| Dérogations audit/gouvernance | Intent backend lié à requête/alias/op, Decision exacte et native TX ; ordinaire sans exception ; tests store27 et filtre18 |
| PEP avant exposition, filtre SQL avant matérialisation | Propriété obtenue des colonnes/owners réels, ressources contextuellement incompatibles exclues, plan propriétaire et double gate ; query_core et filter_audit réels |
| Fraîcheur et retrait Auth | Timestamp réellement observé ; dérogation Root prouvée ; contrôle final séparé de l'authentification pour six actions fermées ; 8 +10 PG |
| R01 sans cible applicative fabriquée | DTO disjoint, action/installation/plan/hash/cibles/effets/temps/op exacts ; consommation committée séparée du stage privé ; R01 propre14 et commun14 |
| Façades et consommateurs | Quinze contrats Core et registre existants conservés, tests de manifest et six familles C02 ; HTTP/CLI/panneau/asynchrone à qualifier par C06/C07/C09/C13 selon leur sélection |
| Frontières propriétaires | Core ne lit pas les tables privées Auth/Audit ; C03/C05 exposent leurs API de faits ; aucun credential transitant dans le modèle ou le rapport |

## Écarts, reprises et clôture

La première recette runtime a détecté une compilation de rôles sans AUDIT
pour un ALLOW PLATFORM. La source et les fixtures ont été corrigées ; la
recette27 puis les régressions sont vertes. Les brouillons non approuvés,
mandats refusés avant effet, erreurs RPC de forme et timeout MCP ne sont pas
des exécutions réussies ni des livraisons. Aucune once consommée n'a été rejouée.

Les 25 Python courants compilent et les 192 tests unitaires ont été réexécutés
après ajout du contrôle de fraîcheur ; les 28 fichiers contrôlés sont UTF-8/LF.

La base CAB a été réconciliée sur C05 publié. Le manifeste a été dédupliqué de
256 entrées vers116 clés sans changement de portée ; les protections de test
déclarent les dépendances réellement importées. Aucun service partagé ou
processus OpenCode n'a été redémarré ou arrêté par C04.

Le delta C04 avait déjà été adopté le 20 octobre. skip_specs reste false ;
la présence de ce delta ne justifie ni nouvelle norme ni contournement de
synchronisation. Tâches, archive, publication, STATISTIQUES.md à six sections,
gate individuel et libération du RUN doivent encore être prouvés pour une
clôture complète. Ce rapport n'est pas à lui seul une clôture.
