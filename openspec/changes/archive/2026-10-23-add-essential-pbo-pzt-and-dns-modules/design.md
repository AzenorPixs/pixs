# Conception — C14

## Statut et périmètre autorisé

RÉALISATION ET VALIDATION TECHNIQUE C14. Les barrières 1.1/1.2 ont été levées dans le canon adopté, puis les modules de gestion et leurs surfaces ont été réalisés. Les preuves natives et limites figurent dans VALIDATION.md ; aucune qualification de l’exécutant ou du P0 global n’en est déduite. Les sections datées de préparation ci-dessous conservent leur portée historique.

## Constat initial de préparation

Constat : Le canon impose les modules PZT et DNS essentiels ; aucun module produit PZT/DNS n’est identifié aux emplacements consultés. La spécification seule ne les fournit pas.

Sources consultées et empreintes recoupées avec la matrice :

- [openspec/specs/pzt/spec.md](../../../specs/pzt/spec.md).
- [openspec/specs/reference-runtime/spec.md](../../../specs/reference-runtime/spec.md).
- [README.md](../../../../README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture retenue

Composer deux responsabilités de gestion PBO propriétaires, pixs.pzt et pixs.dns, via les mécanismes communs ; les manifests et contrats sont décrits dans la conception 1.2 et les preuves de réalisation. Conserver configuration souhaitée, versions et états d’absence d’exécutant ; appliquer les choix validés pertinents à la configuration. N’engager aucun PA, service DNS ou réseau non sélectionné, ni canal de substitution.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Barrières initiales, levées en revue 1.2

Identifiants canoniques et contrats de gestion, sous-modules et schémas ; recouper chaque clause applicable de la table C00. Toute obligation active non conditionnelle rejoint le chemin critique ; aucune exemption supposée.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-first-installable-pbo-profile](../2026-10-18-define-first-installable-pbo-profile/proposal.md).
- [add-core-postgres-services](../2026-10-20-add-core-postgres-services/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../2026-10-21-add-durable-minimized-audit/proposal.md).
- [add-protected-core-http-commands-and-queries](../2026-10-22-add-protected-core-http-commands-and-queries/proposal.md).
- [compose-modular-frontend-with-core-api](../../compose-modular-frontend-with-core-api/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Critères de vérification et limites

Modules composés même réseau désactivé ; absence essentielle bloquante ; configuration/visualisation/supervision honnêtes ; aucune mesure ni application réseau inventée ; aucun canal PBO–PA de substitution ; chaque clause conservée, motivée ou renvoyée vers évolution normative approuvée.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Les migrations initiales PZT/DNS ont été réalisées et exercées dans des schémas PostgreSQL jetables. Le retrait métier est logique et versionné, sans purge ni remise à zéro. Aucun abaissement automatique de base ni restauration d’une installation existante n’a été exécuté.

## Hors profil

Le parcours C08 adopté sélectionne PA système et PZT local pour préparer PostgreSQL et initier sa première connexion technique. Cette sélection ne prouve ni livraison ni qualification des exécutants. Elle reste distincte de l’activation du réseau distant, des sessions utilisateur PA et du service DNS actif, qui ne sont pas sélectionnés par ce parcours. C14 conserve leurs contrats et obligations de gestion sans exécuter une opération hôte, réseau ou DNS par cette reprise documentaire. La qualification Docker et des capacités optionnelles reste distincte ; toute obligation active non conditionnelle démontrée rejoint le chemin critique applicable.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T14 — Gestion PZT/DNS et frontière d’exécution C08

La table C00 est un relevé historique à recouper, par titre et clause, avec le canon courant avant réalisation ; ses lignes et effectifs ne définissent pas une exemption. Un classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire des responsabilités PZT/DNS, avec contrats, schémas et valeurs administrées explicités avant code. La sélection locale PA système/PZT de C08 ne sélectionne pas le réseau distant ni le service DNS actif et ne prouve aucun scénario runtime.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

Voir [audit transversal durable](../2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Identifiant et séparation validés le 17 octobre 2026

pixs.pzt est le nom canonique adopté du module essentiel PZT. Ce lot conserve
sa gestion réseau et DNS ; le nouveau lot [PA10](../../separate-pa-pzt-and-pbo-management-modules/design.md)
porte pixs.agent, qui gère PA hors PZT. L'exécutant réseau est PZT indépendant,
colivré avec PA. Le nom pixs.pzt n'est plus un arbitrage ouvert ; les contrats
concrets et le nom du module DNS restent à qualifier. Relire les instantanés
requirements.md contre le canon actuel avant reprise ; aucune tâche produit
n'est réalisée par cet alignement documentaire.

## Réconciliation documentaire CISMP4 du 22 octobre 2026

Les références et empreintes de `requirements.md` sont recoupées avec le canon courant ; la matrice C00 archivée reste historique et inchangée. La composition actuelle impose `pixs.agent` et `pixs.pzt` comme responsabilités distinctes : PA10 conserve la gestion PA hors PZT, C14 la gestion PZT/DNS. Aucun travail PA10 n’est réputé livré par cette reprise.

Les choix déjà adoptés A06d, A06g et A06j sont conservés : IPv6 désactivé initialement sans modifier l’hôte, plafonds DNS positif de 30 secondes et négatif de 5 secondes sous les autres bornes de validité, suffixe privé explicitement provisionné et contrôlé. Les modalités, valeurs concrètes et preuves encore absentes restent à qualifier ; elles ne deviennent ni de nouveaux défauts implicites ni des garanties de produit. Les arbitrages impactants suivent §45.4, sans rouvrir les décisions acquises.

## 1.2 Conception de réalisation dans le canon adopté

Décisions C1/C2/C3 couvertes par le canon : module distinct `pixs.dns` premier identifiant
de mise en œuvre sans renommage, mutations par Commands idempotentes auditées avec
Queries de lecture et facade Service à garanties égales, persistance Django/PostgreSQL
propriétaires distincts. Les propriétaires, données, migrations, permissions et cycles de vie restent distincts. Aucun stockage concurrent ni suppression de garantie n’est retenu.

### 1.2.1 Identités et DAG de contrats réel, snake_case
Manifests `schema_version="1"` (chaîne schéma manifest) distincte de `version` SemVer composant
et de `config_revision:int` monotone CAS. Exemple : `id="pixs.pzt" type="MODULE" version="0.1.0"`,
`id="pixs.dns" type="MODULE" version="0.1.0"`, dépendances `pixs.kernel==0.1.0`, `pixs.core==0.1.0`.
Capacités : `pzt.management 1.0.0`, `dns.management 1.0.0`, `REQUIRED`, `fallback="none"`.
`[implements].contracts` exacts `{id, version}` SemVer 1.0.0.
DAG de dépendances : `pixs.dns -> pixs.kernel/pixs.core` ; `pixs.pzt -> pixs.kernel/pixs.core/pixs.dns`. PZT déclare et consomme les Queries publiques DNS exigées par le canon,
sans dépendance inverse `dns -> pzt`. Ports d’exécution PZT/PA = capacités sélectionnées et
définies dans les contrats C14 et injectées par la composition serveur, jamais valeurs clientes ;
absence ferme les opérations dépendantes. Rien supposé de PA10 en cours.
Les contrats 1.0.0 sont `pixs.pzt.control.command`, `pixs.pzt.control.query`, `pixs.pzt.state.query`, `pixs.dns.zones.command`, `pixs.dns.records.command`, `pixs.dns.views.query` et `pixs.dns.policy.query`. Les deux Queries DNS sont déclarées parmi les dépendances contractuelles de PZT, sans dépendance inverse.

Catalogue fermé C14, snake_case : Commands `declare_desired_pzt`, `retire_desired_pzt`,
`declare_desired_dns`, `retire_desired_dns`, `declare_name`, `retire_name` ; Queries
`get_desired_pzt`, `get_applied_pzt`, `get_desired_dns`, `get_applied_dns`, `resolve_view_policy`.
`validate_desired`/`refuse_incomplete` = validation/erreur `INCOMPLETE_CONFIG`, non mutations.
Inconnue → `UNKNOWN_OPERATION` refusée. Les déclarations de noms modifient l’état souhaité propriétaire, sans annoncer une publication dans le service DNS. Les retraits sont logiques et versionnés, sans purge de données. Aucune activation réseau, écoute, résolution ni modification hôte n’est réalisée par ces Commands.

### 1.2.2 Requêtes, faits et autorisation au moment de l’effet (C04)
Réutiliser `CommandMetadata{command_id,
correlation_ids, causation_ids, scope_context:ScopeContext, command_type, subject_id,
idempotency_key}` (`src/pixs/core/command_metadata.py` : structure seule, ne prouve ni
sujet/tenant ni autorisation) et `collect_command_idempotency_dimensions ->
{tenant_id from scope_context, subject_id, command_type, idempotency_key}`
(`src/pixs/core/idempotency_dimensions.py` : sans clé durable ni déduplication).
Réutiliser `Request{decision_id, subject_id, resource_id, action_id, context, correlation_id}`,
`AuthenticationContext`, `TrustedFacts{subject_id, resource_id, action_id, auth, ownership,
context, revocation_status}` (`src/pixs/core/authz/ports.py`, `src/pixs/core/ports.py`).
La structure seule ne prouve pas l’autorisation ; sujet/tenant/politique/révocation vérifiés
à l’effet par C04 (`AuthorizationDecider.decide/revalidate_under_locks`), DENY puis ALLOW
puis refus, contexte PLATFORM/TENANT validé. Aucun privilège Super Admin transféré à service/worker ;
worker conserve acteur initial sans credentials Super Admin.

### 1.2.3 Schémas versionnés vs révisions, bornes canon conservées
`schema_version` SemVer du contrat/schéma distincte de `config_revision:int` monotone avec
`expected_revision` CAS (`N+1`, refus sinon, patron `bulk_*_repository.py`,
`bulk_server_*`). TTL 30/5 A06g = plafonds initiaux, non rétention ni TTL uniforme :
conserver autres bornes, TTL zéro possible, minimum plafonds/données/validités, invalidation
immédiate retrait/révocation/vue/IPv6, pas de service après expiration. Aucune valeur de
rétention/budget inventée ; D3/budgets à mesurer/qualifier par profil.

### 1.2.4 États appliqués/mesurés par admission interne, preuve authentifiée
Aucun `Proof{origin,...}` client ne prouve. `report_applied`/`report_measured` = admissions
internes via port vérificateur de confiance lié à `owner/tenant/config_revision/generation/validite`
par une interface C14 de vérification des observations d’exécution. Elle authentifie la provenance et contrôle les preuves réelles selon le profil courant ; une référence ou un DTO client ne suffit pas. Les `TransactionProof/StagedRef` Core lient uniquement les participants d’une transaction et ne remplacent aucune preuve cryptographique PA/PZT. Toute preuve absente, incohérente ou périmée bloque l’admission. Aucun endpoint client déclarant `AVAILABLE/applied`. Absence de mesure = `null/inconnu`,
jamais zéro/réussite. Disponibilité gestion découplée exécutants : DNS non sélectionné → service
`DISABLED`, `dns.management` peut rester `AVAILABLE` pour gestion ; préserver absence essentielle
bloquante et absence de readiness globale sans attestations `host_plan` (`AttestationPort`,
composition sans attestations refuse P0).

### 1.2.5 Audit et idempotence par propriétaires

C14 consomme l’interface publique C05 `core.audit_sink.PostgresAuditParticipant.stage_generic(event, *, alias, operation_id, transaction_token, context)`, avec `verify_staged` et `reconcile_unknown`, ainsi que les références transactionnelles publiques `core.ports.StagedRef/TransactionProof`. Le propriétaire C05 conserve toute écriture de ses tables ; C14 n’importe pas ses modèles ni ses fonctions privées.

Les résultats et enregistrements d’idempotence des Commands PZT/DNS appartiennent à leur module. Ils respectent les quatre dimensions publiques Core et le contenu canonique versionné, sans prétendre que le participant Core limité à ses DTO métier est déjà un adaptateur générique PZT/DNS. Les interfaces et adaptateurs propriétaires nécessaires sont définis en 2.1 et réalisés/testés en 2.2.

La transaction Django/PostgreSQL locale lie configuration ou retrait logique, résultat d’idempotence et audit applicable par le même contexte, alias et identifiant d’opération. Une base obsolète ou un contenu divergent est refusé ; un rejeu identique restitue le résultat confirmé sans double effet, après contrôles courants d’accès. Une issue inconnue reste à rapprocher des faits persistants, sans annonce de réussite ni réexécution aveugle. Aucun SQL ni écriture privée inter-modules, aucun secret dans l’audit. L’audit d’amorçage indépendant de PostgreSQL appartient au parcours C08 et n’est pas simulé par cette transaction ordinaire.

### 1.2.6 Fichiers minimaux et gouvernance, sans nouvelle dépendance
2.1 : `src/pixs/pzt/__init__.py`, `src/pixs/dns/__init__.py`, `src/pixs/pzt/component.toml`, `src/pixs/pzt/contracts.py`, `src/pixs/pzt/configuration.py`,
`src/pixs/pzt/ports.py`, `src/pixs/dns/...` idem, `tests/unit/test_pzt_dns_contracts.py`,
`tests/unit/test_pzt_dns_configuration.py`. 2.2 : `src/pixs/pzt/apps.py`, `models.py`, `services.py`,
`migrations/`, idem DNS, intégration de composition publique dans `src/pixs/backend/host_plan.py` et adaptateurs serveur explicites vers les ports C04/C05, sans nouvel argument fictif à `CoreServicePorts`.
2.3 : surfaces gestion `backend`/`frontend` raccordées aux contrats C11 sans anticiper ses fichiers
instables. Classification/gouvernance des nouvelles données explicite, exposition refusée sans
politique classifiée ; secrets uniquement références `SecretReference`, jamais valeurs.
Aucune dépendance ajoutée. Paramètres A06d/g/j, A06f/h/i, A10h repris, incomplet refusé.

### 1.2.7 Tests immédiats par tâche, sans stubs d’exécution
2.1 : pureté validateurs, refus contractuels (manifest/contrat/schéma invalides, inconnue, incomplet).
2.2 : vraies transactions PostgreSQL/config/audit/idempotence/isolation/CAS/crash, refus sans
vérificateur, `reconcile_unknown`. 2.3 : interfaces/build, Chromium+Firefox headless si UI, sondes/erreurs.
Exécution mTLS/PA/DNS = qualification lots PA01/PA10/C08/Z05, non promise par stubs ; refus honnête
testé vraiment (opération dépendante bloquée sans PZT admissible, sans repli fichier/socket/loopback).

Aucun delta : comportements déjà exigés ; tout indispensable nouveau serait cité avec exigence/écart avant delta.


## Raccords de gestion réalisés pour la recette 2.3 — 23 octobre 2026

Les fichiers api_pzt_dns_catalog.py, api_pzt_dns_inputs.py,
api_pzt_dns_openapi.py, api_pzt_dns_dispatch.py,
api_pzt_dns_errors.py et api_pzt_dns_boundary.py du propriétaire backend
portent les onze liaisons explicites de gestion PZT/DNS. Les plans API
pixs.pzt.management.api et pixs.dns.management.api version 1.0.0 sont
distincts des sept contrats métier. Le raccord consomme les exports publics
ModuleHttp de C11/C06 ; ses gardes transport, acteur et CSRF ne sont pas
réimplémentées dans les modules. Les URL C14 spécifiques doivent précéder
le catchall Core dans l'assemblage de l'hôte.

Le serveur construit Request et CommandMetadata et relie un vérificateur
Auth public à la transaction courante avant sa première revalidation.
Les intentions de dispense restent de simples demandes ; elles ne sont
jamais des faits ni des autorisations. Une activité interactive WEB confirmée
est transmise à C03 ; un rejeu n'ajoute pas d'activité, et son éventuel refus
reste distinct du résultat métier déjà confirmé.

Les entrées src/pixs/pzt/frontend.mjs et src/pixs/dns/frontend.mjs
déclarent chacune traduction, page, trois routes et trois navigations.
Les pages produisent des arbres de présentation, sans DOM, store privé,
jeton ou transport. Les corps sont construits par champs littéraux ; les
révisions proviennent d'une lecture du contexte courant. L'issue inconnue
conserve le formulaire concerné pour rapprochement. Les références secrètes
restent des records de références, les vues conservent leur ordre et leurs
doublons, et les valeurs existantes multiligne ne sont pas normalisées par
une entrée texte monoligne.

Les preuves ciblées, PostgreSQL, HTTP, build composé et renderer réel dans
Chromium/Firefox sont maintenant consignées dans VALIDATION.md, avec leurs
versions et empreintes. Le pipeline/runtime C11 est qualifié ici dans le seul
profil DEVELOPMENT de la recette ; sa livraison globale reste distincte.
Un RequestFactory HTTPS et un TLS loopback avec bypass de chaîne ne
qualifient pas un TLS déployé. Aucun exécutant PZT, transport PA
ni service DNS actif n'est qualifié par ces surfaces de gestion.


### Recoupement de l'amorçage initial Z12/C08

Le canon PZT courant distingue désormais explicitement la cérémonie PKI
initiale Z12 avant PostgreSQL, son adoption puis le retrait de l'autorité
initiale avant admission ordinaire. C08 documente les cinq ports initiaux
propriétaires et leurs preuves séparées. Aucun de ces ports n'appartient au
catalogue fermé des onze opérations de gestion C14 ; aucune émission PKI,
écriture TPM/NV, préparation PostgreSQL ou voie PBO–PA de substitution
n'est ajoutée par ce raccord. Les surfaces ordinaires restent fermées sans
leurs propriétaires Auth/Core/PostgreSQL courants. Ce recoupement actualise
la référence normative sans promettre la qualification de l'amorçage.


### Publication documentaire bornée

Les deux URL principales de gestion sont des index OpenAPI. Chaque index
référence par x-documents ses fragments déterministes -management-N.json,
avec SHA-256 et nombre d'octets calculés sur les octets effectivement servis.
Chaque document respecte la limite commune de 64 Kio ; aucune limite n'est
relevée pour faire entrer le catalogue complet. L'union des fragments conserve
les 24 chemins PZT et 42 chemins DNS du document logique, sans doublon ni
suppression de schéma, de réponse ou de garde. Le même plan API propriétaire
1.0.0 est vérifié à la construction de chaque document. Les index et fragments
sont soumis aux gardes publiques HTTPS/Host/Origin, aux références locales et
au profil documentaire module fourni par C11.

### Choix BIND 9 et activation ultérieure

Le développeur a retenu BIND 9 fourni par Debian, présent dans l'image
Docker Pixs, avec installation et configuration par le PA désigné.
Le [dossier distinct BIND 9](../../adopt-bind9-managed-dns-and-packaging/proposal.md)
prépare les exigences logiciel et distribution ; Z05 conserve la réalisation
du service DNS et des adapters PA. La présence du logiciel dans une image
ne sélectionne ni n'active le service. C14 reste limité à la gestion :
aucune installation BIND 9, ouverture réseau ou activation n'y est ajoutée.
