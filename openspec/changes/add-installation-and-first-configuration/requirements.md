# Exigences de réalisation — C08

## Portée et traçabilité R01

Le complément documentaire du 19 octobre 2026 conserve les exigences et scénarios canoniques et précise leur rattachement aux tâches et à la recette R01 B01–B10 de `design.md`. Ces cas sont des critères de recette futurs, pas de nouveaux scénarios OpenSpec ni des tests exécutés. D01–D04 de C02 restent validés ; aucun code ou delta n’a été produit par ce complément historique. La reprise documentaire du 22 octobre 2026 présente deux deltas distincts, désormais adoptés après décision explicite ; leur traçabilité figure en fin de fichier.

Les 27 références du relevé initial sont conservées avec leurs statuts ND/P historiques. Les neuf références supplémentaires R01 portent « non évalué » ; aucun statut ne constitue un verdict fonctionnel actuel. Titres, lignes, scénarios et empreintes sont recoupés avec le canon courant. Chaque texte complet, et pas seulement son titre ou son scénario, reste applicable selon ses conditions.

| Repère | Source canonique et exigence | Scénarios sources | Tâches C08 | Critères / preuves futures | Responsabilité et applicabilité | Statut historique |
|---|---|---|---|---|---|---|
| C08-R01 | [initial-administration / 11 — Compte Super Admin unique de paramétrage et de secours](../../specs/initial-administration/spec.md#L11) | Compte fonctionnel non nominatif ; Second compte et transfert refusés | 2.3, 2.4 | B03, B05, B06 | C08/C02 ; unicité | ND |
| C08-R02 | [initial-administration / 25 — Exception liée au compte actif](../../specs/initial-administration/spec.md#L25) | Privilège permanent du compte actif | 2.3, 2.4 | B05, B09 | C03/C04 ; compte existant actif | ND |
| C08-R03 | [initial-administration / 34 — Absence de MFA obligatoire au démarrage et au secours](../../specs/initial-administration/spec.md#L34) | Premier démarrage sans MFA ; Réactivation de secours sans MFA | 2.3, 2.4 | B03, B10 ; recette C03 | C03/C04 ; absence de MFA imposé au compte | ND |
| C08-R04 | [initial-administration / 49 — Modes de démarrage explicites](../../specs/initial-administration/spec.md#L49) | Marqueur externe indisponible | 2.1, 2.4 | B01, B09, B10 | C08 ; modes explicites | ND |
| C08-R05 | [initial-administration / 63 — Première configuration et transitions de mode](../../specs/initial-administration/spec.md#L63) | État initial en base distinct du marqueur | 2.1, 2.4 | B07, B10 | C08 ; état initial et marqueur | ND |
| C08-R06 | [initial-administration / 75 — Provisionnement interactif de la base](../../specs/initial-administration/spec.md#L75) | Base migrable | 2.2, 2.4 | B03, B04 ; recette des plans de base | C08 ; création/conservation/migration/recréation | ND |
| C08-R07 | [initial-administration / 99 — Reprise et références de secrets après provisionnement](../../specs/initial-administration/spec.md#L99) | Référence de secret après provisionnement | 2.1, 2.2, 3.2 | B04, B10 ; recette de conversion en références | C01/C03/C08 ; aucun secret livré | ND |
| C08-R08 | [initial-administration / 114 — Création conditionnelle du Super Admin](../../specs/initial-administration/spec.md#L114) | Mots de passe différents ; Compte fonctionnel créé explicitement | 1.2, 2.3, 2.4 | B01, B03, B04 | C08 R01 ; écritures C02, credential C03 | ND |
| C08-R09 | [initial-administration / 135 — Réutilisation du Super Admin d'une base conservée](../../specs/initial-administration/spec.md#L135) | Base conforme conservée | 2.3, 2.4 | B05, B06, B07 | C08 R01 ; compte conservé | ND |
| C08-R10 | [initial-administration / 145 — Marqueur externe et première configuration](../../specs/initial-administration/spec.md#L145) | Configuration initiale inachevée | 2.1, 2.4 | B07, B10 | C08 ; finalisation distincte du commit | ND |
| C08-R11 | [initial-administration / 161 — Panneau d'administration contrôlé](../../specs/initial-administration/spec.md#L161) | Administrateur ordinaire soumis aux ACL | 3.2 | Recette de panneau C13 après provisionnement | C13/C04 ; hors réalisation R01 | ND |
| C08-R12 | [initial-administration / 174 — Changement contrôlé de la route d'administration](../../specs/initial-administration/spec.md#L174) | Ancienne route d'administration | 3.2 | Recette de route C13 après provisionnement | C13 ; hors réalisation R01 | ND |
| C08-R13 | [initial-administration / 186 — Expérience et état du panneau](../../specs/initial-administration/spec.md#L186) | Santé réservée au root | 3.2 | Recettes UI C12/C13/C17 | C12/C13 ; hors réalisation R01 | ND |
| C08-R14 | [initial-administration / 201 — Désactivation externe du Super Admin](../../specs/initial-administration/spec.md#L201) | Connexion root désactivée ; Secours malgré le marqueur de désactivation ; Transaction engagée lors de la désactivation | 2.1, 2.4, 3.2 | B10 ; recette de désactivation C03/C04 | C08 distingue les marqueurs ; C04/N05 application | ND |
| C08-R15 | [initial-application-bootstrap / 11 — Composition Django initiale déclarée](../../specs/initial-application-bootstrap/spec.md#L11) | Composition initiale valide | 1.1, 3.2 | Recette de composition C07/C17 | C07/C17 ; aucune readiness par C08 seul | P |
| C08-R16 | [initial-application-bootstrap / 27 — Configuration sensible de la composition Django initiale](../../specs/initial-application-bootstrap/spec.md#L27) | Connexion fournie par configuration runtime | 2.1, 2.2, 3.2 | B04, B10 ; recette des secrets | C01/C08 ; références externes | P |
| C08-R17 | [initial-application-bootstrap / 39 — Surface HTTP initiale minimale](../../specs/initial-application-bootstrap/spec.md#L39) | Route initiale non déclarée | 3.2 | Recette HTTP C06/C07 | C06/C07 ; hors réalisation R01 | P |
| C08-R18 | [initial-application-bootstrap / 54 — Shell TanStack initial intégré](../../specs/initial-application-bootstrap/spec.md#L54) | Démarrage du shell initial | 3.2 | Recette de shell C07/C11 | C07/C11 ; hors réalisation R01 | P |
| C08-R19 | [installation-provisioning / 9 — Provisionnement du compte fonctionnel de secours](../../specs/installation-provisioning/spec.md#L9) | Provisionnement sans compte nominatif ni MFA | 2.3, 2.4 | B03, B05 | C08/C02/C03/C04 | ND |
| C08-R20 | [installation-provisioning / 18 — Provisionnement explicite et états inspectables](../../specs/installation-provisioning/spec.md#L18) | Installation non provisionnée | 2.1, 2.4 | B07, B10 | C08 ; pas de trafic métier non prêt | ND |
| C08-R21 | [installation-provisioning / 30 — Configuration et secrets vérifiés avant mise en service](../../specs/installation-provisioning/spec.md#L30) | Référence de secret indisponible | 2.1, 2.2, 3.2 | B04, B10 ; recette de résolution | C01/C08 ; secrets par références | ND |
| C08-R22 | [installation-provisioning / 42 — Opérateur initial explicite et sans privilège implicite](../../specs/installation-provisioning/spec.md#L42) | Identité opérateur absente | 1.2, 2.3, 2.4 | B01, B02, B09 | C08 R01 ; identité et autorité explicites | ND |
| C08-R23 | [installation-provisioning / 55 — Création tenant-scoped contrôlée](../../specs/installation-provisioning/spec.md#L55) | Rejou du provisionnement du premier tenant | 2.3, 2.4 | B03, B06, B09 | C08 R01 ; tenant contrôlé | ND |
| C08-R24 | [installation-provisioning / 68 — Reprise contrôlée et auditée](../../specs/installation-provisioning/spec.md#L68) | Interruption avant mise en service | 2.1, 2.4 | B06, B07, B10 | C08 R01 ; reprise auditée | ND |
| C08-R25 | [reference-composition / 35 — Capacités obligatoires du P0](../../specs/reference-composition/spec.md#L35) | Capacité P0 absente | 1.1, 3.2, 3.3 | Recette du P0 C17 | C07/C17 ; apport C08 seulement | P |
| C08-R26 | [reference-composition / 44 — Capacités hors P0 explicites](../../specs/reference-composition/spec.md#L44) | Synchronisation non sélectionnée | 1.1, 3.2 | Recette du profil C00/C17 | C00/C17 ; aucune option sélectionnée | P |
| C08-R27 | [reference-composition / 55 — Preuve reproductible](../../specs/reference-composition/spec.md#L55) | Deux validations identiques | 3.2, 3.3 | Recette de composition C07/C17 | C07/C17 ; preuves reproductibles | P |
| C08-R28 | [initial-administration / 227 — Opérateur technique INSTALLER avant base et sessions](../../specs/initial-administration/spec.md#L227) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | B02, B08, B09 ; recette C01 distincte | C01 technique ; R01 sans transfert | R01 — non évalué |
| C08-R29 | [initial-administration / 241 — Limites et refus de la phase technique INSTALLER](../../specs/initial-administration/spec.md#L241) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | B02, B08, B09 | C01 interdit de créer identité/compte | R01 — non évalué |
| C08-R30 | [authorization / 57 — Modèle Subject Resource Action Context](../../specs/authorization/spec.md#L57) | Propriété sans politique refusée ; Sujet technique avant identité applicative | 1.2, 2.3, 2.4 | B01, B02, B09 | C03/C04 ; sujet canonique pour acte C08 | R01 — non évalué |
| C08-R31 | [authorization / 94 — Autorisation technique C01 bornée sans extension métier](../../specs/authorization/spec.md#L94) | Action métier hors bootstrap | 1.2, 2.3, 2.4 | B02, B08, B09 | C01 seulement ; refus d’extension métier | R01 — non évalué |
| C08-R32 | [authorization / 103 — Limites de l’autorité technique d’amorçage](../../specs/authorization/spec.md#L103) | Action métier hors bootstrap | 1.2, 2.3, 2.4 | B02, B09 | C04 ; UID 0 et forme PLATFORM sans permission | R01 — non évalué |
| C08-R33 | [services / 28 — Traçabilité et sécurité des appels](../../specs/services/spec.md#L28) | Contexte non vérifiable | 2.3, 2.4 | B01, B02, B09 | C02/C08 ; provenance et périmètre contrôlés | R01 — non évalué |
| C08-R34 | [audit / 41 — Contenu minimal d'un événement d'audit](../../specs/audit/spec.md#L41) | Refus d'autorisation tracé | 2.3, 2.4, 3.2 | B02, B03, B08 | C05 ; acteur/cible/effet distincts et minimisés | R01 — non évalué |
| C08-R35 | [audit / 50 — Périmètre obligatoire d'audit](../../specs/audit/spec.md#L50) | Opération destructive sans audit | 2.3, 2.4 | B03, B07, B08 | C05 ; pas de privilège anticipé du compte futur | R01 — non évalué |
| C08-R36 | [interactions / 18 — Commandes validées et autorisées](../../specs/interactions/spec.md#L18) | Mutation sans autorisation refusée | 2.3, 2.4 | B02, B04, B09 | C02/C08 ; autorisation avant mutation | R01 — non évalué |

## Critères et limites

- B01/B02 vérifient la preuve d’opérateur, le mapping de sujet et la décision liée au plan avant toute mutation Core ; un booléen caller, UID 0, le mot de passe cible ou un reçu C01 ne suffisent pas.
- B03/B04 couvrent la création conditionnelle confirmée et les saisies de mot de passe ; B05 conserve le compte d’une base conforme sans reset ni seconde identité.
- B06/B07 couvrent l’exclusion, l’idempotence et les interruptions avant/après commit ou marqueur. Une issue inconnue exige inspection avant rejeu ; les secrets restent hors des checkpoints et empreintes publiques.
- B08/B09 vérifient audit applicable, limites C01 et fin de l’autorité d’initialisation. B10 couvre le rapprochement du marqueur, les états inspectables et l’authentification propre du compte pour FIRST_CONFIGURATION.
- Les lignes de composition, HTTP, shell, panneau et désactivation restent attribuées à leurs lots propriétaires. Elles ne transforment pas R01 en réalisation de C06/C07/C11/C12/C13/C17.
- Les preuves locales C02 V05/V07 et les preuves intégrées C03/C04/C05/C08 sont distinctes. Aucune branche de provisionnement n’est activée tant qu’une preuve, un mapping conforme ou un port obligatoire manque. Toute précision normative nécessaire est présentée avant code, sans exception inventée.
- Les tâches 3.1 à 3.4 consolident chaque ligne : commandes et résultats observés, scénarios applicables, portée des preuves, limites et conditions de clôture. Une preuve partagée conserve une seule identité ; aucune tâche ne devient achevée du seul fait du présent rattachement.

## Empreintes SHA-256 du canon — relevé antérieur à la présente adoption

Les empreintes identifient les sources courantes du complément, sans réécrire les preuves historiques ni valider une réalisation. Une dérive exige une nouvelle lecture du périmètre affecté.

- `openspec/specs/initial-administration/spec.md` : `a875dfd4e48cc2920ea38242b02c46aab386a7a77b645165d009d9fa47f4cc4a`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/installation-provisioning/spec.md` : `b5a8760659f847f663521718e7d8b27d4808dc4aface049a1da84c4e0e967ef6`.
- `openspec/specs/reference-composition/spec.md` : `53f1d388d6999fcf7af05317a9774d2c4e708a90157fe1666b4210e0d1314a4c`.
- `openspec/specs/authorization/spec.md` : `c09e4dac79ecbe6bdb16550d8a4d1566307127818cdeaf9dfbe9224f50858310`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.
- `openspec/specs/audit/spec.md` : `19c58dc8b16e537967c46e69fca4132867e98ada591980b67872ee8c382a5eb1`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.

## Comptage et état des preuves — relevé historique

La matrice contient 36 exigences distinctes et 44 références de scénarios. Les dix cas B01–B10 précisent leur recette ; ils ne s’ajoutent pas aux compteurs du canon. Les dix tâches de réalisation restent non cochées. Aucun test produit, migration, code, nouveau change, synchronisation ou archivage n’est exécuté par ce complément.


## Reprise documentaire du 22 octobre 2026 — exigences adoptées, recettes futures

Les références R01–R36 ci-dessus restent canoniques. Les quatre exigences et huit scénarios des deux deltas locaux ont été adoptés sous accord distinct du développeur ; leurs recettes ne sont pas exécutées. Les dénominateurs historiques de 36 exigences / 44 références sont conservés comme relevé historique, sans assimiler les ajouts à des preuves produit.

| Cas | Référence canonique adoptée | Critère de recette future | Tâches |
|---|---|---|---|
| S01 | [Résolution technique après INSTALLER explicitement autorisée](../../specs/secrets-providers/spec.md) | Chaque mode FIRST_CONFIGURATION/NORMAL/MAINTENANCE et rôle déclaré passe sous preuves réelles ; mode, rôle, finalité ou référence non autorisé échoue sans secret. | 1.3, 2.5, 3.1, 3.2 |
| S02 | [Continuité auditée du démarrage avant PostgreSQL](../../specs/secrets-providers/spec.md) | Preuve d’audit indépendante avant remise de valeur ; import C05 idempotent de la bonne invocation avant disponibilité ; doublon, crash et relais indisponible restent inspectables. | 1.3, 2.5, 3.2 |
| S03 | [Publication externe et références de connexion vérifiées](../../specs/installation-provisioning/spec.md) | Référence absente ou version/cible divergente garde l’installation non prête ; aucune saisie, credential ou empreinte sensible dans artefact, audit ou checkpoint. | 1.3, 2.5, 3.2 |
| S04 | Secrets-providers / cycle de vie C01 canonique | Rotation/révocation et consommateurs encore actifs ne sont pas réputés traités par un changement de mode ; refus et reprise sans bypass INSTALLER. | 2.5, 3.2 |
| G01 | [Gouvernance initiale vérifiée avant création Core](../../specs/installation-provisioning/spec.md) et data-governance canonique | Source protégée et profil complet/versionné, attestation réellement produite et liée aux cibles avant création. Aucun producteur de test présenté comme source déployée. | 1.4, 2.6, 3.2 |
| G02 | Même delta adopté ; B01/B02/B08 | Profil absent, révoqué, périmé ou incohérent : aucune création ; audit applicable sans dispense du futur compte. | 2.6, 2.4, 3.2 |
| G03 | Même delta adopté ; B06/B07 | Substitution/concurrence/panne : revalidation avant commit, rollback commun Core/Auth/audit/résultat C08 et reprise sans duplication. | 2.6, 2.4, 3.2 |

Les scénarios S04 et B01–B10 renvoient aux exigences complètes existantes, sans les assouplir. C01 reste technique, R01 Ed25519/600 secondes est conservé, les deux marqueurs sont distincts et le résultat C08 reste dans la transaction propriétaire.

Le besoin C10 est limité au profil et au fournisseur de gouvernance initiale effectivement requis. Ce lot ne prétend ni livrer C10, ni choisir ses rétentions, ni implémenter purge/effacement ou demandes de données. La procédure externe de publication du credential reste à vérifier séparément, sans nouveau writer.

Aucune tâche de réalisation n’est cochée. .openspec.yaml a été aligné sous autorisation distincte : schema et created sont conservés et skip_specs est retiré. Les contrôles documentaires distinguent adoption et validation des exigences de toute preuve d’implémentation. Les recettes S01–S04/G01–G03 complètent B01–B10 sans démontrer une livraison C08.

- `openspec/specs/secrets-providers/spec.md` : `e666a47aae86b91ed6d43d32dd8dce7b1451cb43662e5625f26a40470abf94bd` (source du delta adopté ; aucune recette produit déduite).

La synchronisation ajoute deux exigences/quatre scénarios dans secrets-providers et deux exigences/quatre scénarios dans installation-provisioning ; les scénarios antérieurs restent inchangés. S04 renvoie au cycle de vie C01 canonique existant.

## Limite de l’adoption antérieure — autorité du démarrage

Les quatre ajouts adoptés ne modifient pas [authorization](../../specs/authorization/spec.md). Son exception de sujet OS C01 reste limitée aux seules actions techniques INSTALLER avant existence de la base et des identités ; après amorçage, les contrôles applicatifs ordinaires reprennent.

S01 doit donc démontrer le sujet applicatif et la décision courante effectivement vérifiables pour une résolution post-INSTALLER, en plus des preuves UID/unité/workload. Ces preuves techniques seules ne créent aucune nouvelle exception. Si le raccord avant ouverture de PostgreSQL ne peut satisfaire ce contrat, il reste refusé et exige un arbitrage de spécification avant code ; l’adoption du présent lot ne résout pas implicitement ce point.


## Parcours PA/PZT adopté — références canoniques et recettes futures

Le parcours PA/PZT → PostgreSQL → PBO est adopté au canon le 22 octobre 2026. Les huit deltas locaux conservent quatre exigences déjà intégrées et tracent six exigences modifiées, six nouvelles et vingt-sept scénarios supplémentaires nets (dont quatre de présentation des garanties). La branche technique de authorization remplace la limite historique pré-base ci-dessus dans son seul périmètre ; les autres résolutions restent sous leurs contrôles applicatifs. Aucun cas P01–P10, B01–B10, S01–S04 ou G01–G03 n’est réputé exécuté par cette adoption.

| Cas | Delta concerné | Critère de recette future | Tâches |
|---|---|---|---|
| P01 | [Administration initiale](specs/initial-administration/spec.md), [PA](specs/pixs-agent/spec.md) | Sur physique/VM sans PG préparé, PA prépare le service et initie la première connexion technique ; PBO seul réalise les migrations et effets applicatifs après contrôles. | 1.5, 1.6, 2.7 |
| P02 | [Docker](specs/docker-image/spec.md), administration initiale | Logiciel PG dans l’image sans données/secret ; stockage externe vide initialisé par PA ; stockage existant conservé, incompatibilité non prête sans suppression implicite. | 1.5, 2.7 |
| P03 | [PZT](specs/pzt/spec.md), [autorisation](specs/authorization/spec.md) | Avant PG, provisionnement opérateur vérifié, identités/ancrages/politique locaux contrôlés ; tout échange PBO–PA via PZT mTLS ; premier PBO non auto-approuvé. | 1.6, 2.7 |
| P04 | PZT, autorisation | PZT absent, politique absente/périmée/révoquée ou fraîcheur invérifiable : refus, aucun repli Unix/loopback/fichier hors PZT ni ouverture réseau distante. | 1.6, 2.7 |
| P05 | [Secrets](specs/secrets-providers/spec.md), autorisation | Redémarrage réel en NORMAL sans connexion PG préalable : remise du seul secret de connexion au workload sous politique native indépendante d’Auth PG ; droits métier attendent C04/PG et aucun mode n’est réétiqueté. | 1.3, 2.5, 2.7 |
| P06 | Secrets, [provisionnement](specs/installation-provisioning/spec.md) | Publication externe et consommateur vérifiés, aucun writer implicite, credential absent des messages PZT/artefacts/checkpoints ; rotation/révocation/copies/audit pré-base et relais C05 rapprochés avant disponibilité. | 1.3, 2.5, 2.7 |
| P07 | PA, provisionnement | Réponse PA perdue ou panne avant migration : inspection des résultats et de la cible avant reprise, aucun double effet ; un reçu technique n’est ni commit métier ni autorisation d’étape suivante. | 2.1, 2.7 |
| P08 | Provisionnement, PZT | Relais ou commit puis marqueur perdus : réconciliation par propriétaire, aucun second compte/tenant, aucune atomicité inventée entre service PG externe et transaction Core/Auth/C05/C08 ; pas de compensation destructive implicite. | 2.1, 2.4, 2.7 |
| P09 | Autorisation, PA | Sujet technique demande une création tenant, table métier, shell arbitraire ou code reçu : refus ; R01 Ed25519/600 s et gouvernance G01–G03 restent requis pour les effets applicatifs. | 1.6, 2.3, 2.7 |
| P10 | [Composition](specs/reference-composition/spec.md), Docker | PA système/PZT local explicitement sélectionnés et qualifiés, réseau distant et sessions PA non activés implicitement ; réplicas, budgets et propriétaire de base/PZT distincts, profil historique sans exécutants non présenté comme preuve. | 1.5, 2.7 |

P01–P10 sont des critères de recette future, tous non exécutés. Ils complètent B01–B10, S01–S04 et G01–G03 sans les remplacer. Le nouveau cas P05 distingue la remise technique de connexion avant PG des autres résolutions post-INSTALLER exigeant le sujet et les décisions applicatifs courants.

L’adoption modifie les huit canons et les quatre documents C08, avec alignement de BUILD/PROJECT/TECHNICAL. Les deltas, corrigés uniquement pour deux interdictions RFC 2119, restent la trace de cette adoption ; la métadonnée conserve schema et created, avec son seul commentaire aligné sur l’adoption. Les autres exigences canoniques, archives, tâches historiques, code, migrations, configuration d’exploitation et Git sont préservés. Les recettes et qualifications restent futures.

## Traçabilité de l’adoption PA/PZT courante

Les douze exigences ci-dessous sont adoptées ; leurs recettes demeurent futures. Quatre descriptions trop longues sont résumées et leurs corps normatifs complets conservés dans quatre scénarios dédiés ; aucun comportement n’est ajouté. Les quatre ajouts C08 antérieurs sont identiques avant/après adoption.

| Capacité | Exigence adoptée | Opération | Scénarios canoniques | Recettes futures |
|---|---|---|---|---|
| [authorization](../../specs/authorization/spec.md) | Modèle Subject Resource Action Context | MODIFIED | Propriété sans politique refusée ; Sujet technique avant identité applicative ; Opérateur R01 sans session cible | P03, P04, P05, P09 |
| [authorization](../../specs/authorization/spec.md) | Limites de l’autorité technique d’amorçage | MODIFIED | Action métier hors bootstrap | P03, P04, P05, P09 |
| [authorization](../../specs/authorization/spec.md) | Autorité technique PA PZT et lancement PBO sans base applicative | ADDED | Garanties de l’autorité technique PA PZT ; Démarrage NORMAL sans connexion initiale ; Identité technique utilisée pour un tenant ; Politique native non vérifiable | P03, P04, P05, P09 |
| [docker-image](../../specs/docker-image/spec.md) | PostgreSQL fourni et initialisation PA du profil Docker Pixs | ADDED | Garanties du profil Docker PostgreSQL ; Premier démarrage Docker ; Redémarrage et réplication Docker | P02, P10 |
| [initial-administration](../../specs/initial-administration/spec.md) | Provisionnement interactif de la base | MODIFIED | Garanties du provisionnement interactif PA PBO ; Base migrable ; Premier accès technique PostgreSQL ; Stockage Docker existant | B03, B04, P01, P02 |
| [installation-provisioning](../../specs/installation-provisioning/spec.md) | Séquence PA PZT PostgreSQL puis initialisation PBO | ADDED | Garanties de la séquence et de la reprise ; Panne entre préparation et migration ; Commit métier et marqueur perdu | P06, P07, P08 |
| [pixs-agent](../../specs/pixs-agent/spec.md) | Préparation PostgreSQL par le PA système | ADDED | Garanties de la préparation PA ; Rejeu après préparation technique ; Demande hors rôle technique | P01, P07, P09 |
| [pzt](../../specs/pzt/spec.md) | Autorité métier et état de contrôle cohérents | MODIFIED | Garanties de séparation du contrôle technique et applicatif ; Autorité métier et état de contrôle cohérents | P03, P04, P08 |
| [pzt](../../specs/pzt/spec.md) | Amorçage local PA PZT indépendant de PostgreSQL | ADDED | Garanties de l’amorçage local PZT ; PZT local avant la base ; Autorité d’amorçage périmée ; Relais de contrôle incomplet | P03, P04, P08 |
| [reference-composition](../../specs/reference-composition/spec.md) | Qualification du binaire commun et des profils de ressources P0 | MODIFIED | Garanties de qualification du parcours initial PA PZT ; P0 sans exécution réseau ; P0 sans réseau distant ; Plan de ressources sans preuve sur cible | P10 |
| [reference-composition](../../specs/reference-composition/spec.md) | Profil initial PBO PFO Debian local v1 | MODIFIED | Garanties du profil Debian local avec préparation PA ; Architecture seulement observée | P10 |
| [secrets-providers](../../specs/secrets-providers/spec.md) | Remise de connexion PBO indépendante de la base à ouvrir | ADDED | Garanties de la remise technique de connexion ; Redémarrage sans Auth disponible ; Référence présente sans remise admissible | S01–S04, P05, P06 |

### Empreintes après adoption du 22 octobre 2026

- `openspec/specs/authorization/spec.md` : `7dcd542b1e89020ba0363b6b74d3d0bc8fbd592af5b55226d7e2c00845a413de`.
- `openspec/specs/docker-image/spec.md` : `3de79ba509408479fd31bac6111a1c93dd446cb5c429b2614a2c3fee6421bdd2`.
- `openspec/specs/initial-administration/spec.md` : `d1c08603168461ce11c7b0d967b2112106b59a1cc4aa89d90a3d00b4888b6879`.
- `openspec/specs/installation-provisioning/spec.md` : `7ba4fceced05ac89a62258d76ebecfb3848fac91e8608d6c9ab0e998f7268f3f`.
- `openspec/specs/pixs-agent/spec.md` : `c6ed3e0ac08d37f5d9101ed05dd877f27fee160985a5ee568ec3bc35f6dde7ef`.
- `openspec/specs/pzt/spec.md` : `5a5aea7ef86c061905f17cb3acc36cc841acb4d9e4ffa122735793a12a022e0c`.
- `openspec/specs/reference-composition/spec.md` : `f450bba906d70a42021eec31a917fc85f04ef4c6d973d1f469bc7d6b424b6a2b`.
- `openspec/specs/secrets-providers/spec.md` : `dad482529040d64679a83fa059460e115a0f6f358203eb92a1545e8444ac93ad`.

## Complément D1–D3 adopté le 23 octobre 2026 — profils 1.5

Les compteurs et empreintes précédents conservent leur valeur historique datée. Le présent complément ajoute exactement deux exigences et cinq scénarios, sans duplication des quatre ajouts C08 antérieurs ni des clauses PA/PZT déjà adoptées. La déclaration documentaire ne qualifie aucune réalisation.

| Référence adoptée | Scénarios supplémentaires | Tâches propriétaires | Cas et preuves futures |
|---|---|---|---|
| [docker-image — Profil Docker initial déclaré et supervisé](../../specs/docker-image/spec.md) | Démarrage du profil Docker déclaré ; Arrêt des processus cohébergés | 1.5 déclaration ; 1.6 contrôles d’admission ; 2.7 raccord technique ; 3.1/3.3 qualification | P01/P02/P10 : Debian 13 x86_64 physique/VM et Docker amd64 ; artefacts/digest/dépendances verrouillés avant build ; ENTRYPOINT/CMD/STOPSIGNAL/VOLUME traités, aucun init automatique ; init Docker/Supervisor au premier plan, ordres/readiness/comptes/signaux/drain, stockage conservé, propriétaires uniques et budgets partagés explicites. |
| [secrets-providers — Secrets Docker par fichiers versionnés](../../specs/secrets-providers/spec.md) | Workload Docker et politique courants ; Fichier présent sans identité fiable ; Rotation ou relais non confirmé | 1.3 politiques ; 1.5 choix explicite ; 1.6 confiance ; 2.5 fournisseur réel ; 3.1/3.3 qualification | S01–S04 et P05/P06/P10 : preuve native et politique fraîche, mode/rôle/finalité/cible/référence/version/révocation/bornes ; arrêt attesté avant remplacement/remontage ou recréation, absence de copie prolongeant l’accès ; audit durable pré-base et rapprochement C05 avant disponibilité. |

D1–D3 sont adoptés uniquement dans les dix fichiers du design et les deux canons ci-dessus, avec un paragraphe BUILD. Supervisor 4.2.5-3 est une nouvelle dépendance de l’image seulement ; aucun paquet ou artefact n’est installé ou construit. Le fournisseur Docker est distinct de C01 Debian ; ni UID/fichier seul, ni fixture, ni preuve systemd ne qualifie sa confiance. Les secrets restent dans le seul processus consommateur. R01 Ed25519/600 secondes, C01, les gabarits purs et le contrat minimal C10 de 1.4 sont conservés.

Les contrôles de 1.5 portent sur cette déclaration, sa cohérence P01/P02/P10, les profils purs existants et la validation stricte C08/deux canons. Les paramètres de confiance et de ressources restent obligatoires sans valeur inventée ; leur provisionnement et les tests réels appartiennent aux tâches dépendantes. Aucun résultat PostgreSQL, Docker, PA/PZT ou fournisseur de secrets réel n’est déduit de ces contrôles documentaires.

### Empreintes des deux canons après complément D1–D3 du 23 octobre 2026

- `openspec/specs/docker-image/spec.md` : `c760213be749fc9deef1ce0cd9cf7b1783a6d879c173452cf4b9a2eb25283a0b`.
- `openspec/specs/secrets-providers/spec.md` : `d5b79c1c0f9d337f3f672fa54feac2f984d0dfb3d1dcaa3deca83ee31f313218`.

Les deux corps normatifs adoptés sont conservés intégralement dans leur premier scénario, avec un renvoi obligatoire depuis chaque énoncé pour toute phase concernée. Cette présentation satisfait la limite du validateur strict sans modifier les deux exigences, les cinq scénarios ni leurs garanties ; elle ne qualifie aucune réalisation.

## Q1.6-PKI — autonomie de la première installation validée le 23 octobre 2026

Exigence confirmée : « L’installation première doit être totalement autonome ». Terme corrigé : **hôte**. Aucun Pixs, PostgreSQL Pixs ou service privé de certification PZT déjà opérationnel, ni paquet PZT préémis ailleurs ne doit être requis. La confiance initiale doit pouvoir être établie localement sous contrôle opérateur avant PostgreSQL, sans premier PBO auto-approuvé.

| Repère | Responsabilités et traçabilité | Critères et preuves futures | Tâches |
|---|---|---|---|
| Q1.6-PKI | [Design — autonomie](design.md) ; C08 parcours, PA préparation, PZT transport/PKI sous leurs propriétaires, Core/Auth/C05 effets applicatifs | Sur physique/VM ou Docker sélectionné : départ sans Pixs/PG/PKI opérationnels ni paquet PZT préémis ; préparation locale contrôlée des identités, puis PZT → PA → PostgreSQL → initialisation PBO. Absence de dépendance circulaire, données existantes conservées. | 1.6, 2.5, 2.7, 3.1/3.3 |
| P03/P04/P07/P09 — autonomie | Même répartition canonique ; aucun canal PBO–PA hors PZT ni autorité métier technique | Refus de provenance/politique/identité/fraîcheur invérifiables ; inspection avant reprise d’une issue inconnue ; aucun shell ou effet métier implicite ; rapprochement des preuves/résultats et fin des mandats temporaires avant contrôle ordinaire PostgreSQL. | 1.6, 2.7 et tâches propriétaires |

Ces critères restent des recettes futures non exécutées, sans nouveau scénario OpenSpec par leur rédaction. L'autonomie est acquise. E1 consomme le contrat initial Z12 documentaire 1.0.0 §12 publié sous référence 69 ; E2 noms/version 1.0.0/mode/classes du catalogue PA01 sont adoptés et publiés sous référence 70 ; E3 Cython libssl/libcrypto OpenSSL 3 TLS 1.3/mTLS est explicitement validé par le développeur. Leurs schémas de raccord, API/runtime et exécutants manquants restent à réaliser et qualifier, sans installation sur l'hôte actuel déduite de ce choix. Les sous-lots marqueur et plan privés 2.1 et leurs unittest sont écrits, non testés, avec MarkerConfig et PlanLimits obligatoires ; stockage protégé plan/checkpoint, résultat PostgreSQL et lecteur réel restent à réaliser. C01, R01 Ed25519/600 secondes, raccord minimal C10, clauses et compteurs historiques sont conservés. 1.6 et 2.1 restent non cochées, 2.5/2.7 non commencées ; aucune recette produit ni disponibilité P0 n'est qualifiée.

## Reprise du 23 octobre 2026 — choix E4 adoptés et limites courantes

E3 et les choix E4 sont adoptés. Le [design, section E4](design.md) précise
l'usage technique supplémentaire de la clé opérateur Ed25519 préautorisée,
le mandat distinct de R01 lié au plan/confirmation et le registre durable PA
avec ancrage TPM NV propre, distinct de la PKI Z12. L'accord humain est
documentaire ; formats conditionnels exacts, résolution, protection matérielle,
machine de reprise et qualification restent à réaliser. Aucune installation
ni opération TPM/NV sur l'hôte actuel n'est autorisée ; aucun canon n'est modifié.

Les sources C08/C10 et les migrations additives 0014/0015 sont préparées ; le
modèle de résultat C08 est déclaré auprès de Django. Aucun test produit,
import de qualification ou SQL de migration n'a été exécuté par cette reprise.
Cette préparation ne prouve ni résultat engagé, ni disponibilité PA/PZT, ni
admission FIRST_CONFIGURATION/NORMAL. Les tâches après 1.5 et les contrôles
B/S/G/P restent ouverts jusqu'aux preuves propres à la phase de tests/validation.

## Retrait de la préparation initiale PA — principes adoptés

Le retrait irréversible de la nouvelle préparation initiale PA est vérifié avant toute admission s'appuyant sur sa fin. La remise technique minimale canonique de connexion PBO est conservée. Aucune autorité ordinaire déjà admise n'est inventée par ce retrait.

Les critères observent l'action withdraw_initial_authority, de classe Critique, dans le domaine PA_POSTGRESQL_WITHDRAWAL, sous la permission WITHDRAW_PA_INITIAL, avec un mandat signé nouveau distinct de R01 et E4. Ils observent la confirmation C08 avec C03 et C04 courants et mapping vérifié vers le signataire, ainsi que les vérifications PA de signature, politique, révocation, validité et fraîcheur UTC, identités, cible, plan, contexte, anti-rejeu, quiescence et ancrage durable. Un DTO à l'état RETIRED, un résultat PG_SUCCEEDED, un mode NORMAL ou D6 seul ne vaut pas preuve du retrait.

L'inspection administrative Protégé sous autorisation courante, distincte de get_postgresql_result, sans ré-extension ni préparation ni retrait rejoué, et la fermeture des contrats de topologie D8/D6, de wire et de résolveurs en revue commune avant leur code, avec qualifications réelles en phase 2 après réalisation, font partie des conditions. Les prérequis applicatifs, les migrations, R01, Core, Auth et les audits rapprochés sont présentés, sans exiger une autorité ordinaire PA déjà active. Les propriétaires PA et Z12 et leurs deux retraits restent distincts. Aucune recette n'est exécutée par ce texte. L'adoption des principes ne vaut pas réalisation.

E5 est adopté documentairement et reste non réalisé ni qualifié. PA retourne l'observation puis le planning avant toute confirmation C08. Les cinq gardes ressources s'appliquent même en REUSE ou effets vides, UNOBSERVABLE impose UNDETERMINED, la preuve actuelle d'ABSENT est obligatoire avant chaque CREATE après SERVICE_START et la conformité complète avant SUCCEEDED. Les tableaux A07 restent complets avec ordre et doublons de leurs invocations réelles. Toute divergence impose refus ou replanification sans compensation destructive ni rejeu d'issue inconnue. Aucune garantie producteur, code, test ou infrastructure n'est anticipée.
