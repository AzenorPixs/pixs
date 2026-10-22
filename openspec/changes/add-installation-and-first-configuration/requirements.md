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
| C08-R07 | [initial-administration / 90 — Reprise et références de secrets après provisionnement](../../specs/initial-administration/spec.md#L90) | Référence de secret après provisionnement | 2.1, 2.2, 3.2 | B04, B10 ; recette de conversion en références | C01/C03/C08 ; aucun secret livré | ND |
| C08-R08 | [initial-administration / 105 — Création conditionnelle du Super Admin](../../specs/initial-administration/spec.md#L105) | Mots de passe différents ; Compte fonctionnel créé explicitement | 1.2, 2.3, 2.4 | B01, B03, B04 | C08 R01 ; écritures C02, credential C03 | ND |
| C08-R09 | [initial-administration / 126 — Réutilisation du Super Admin d'une base conservée](../../specs/initial-administration/spec.md#L126) | Base conforme conservée | 2.3, 2.4 | B05, B06, B07 | C08 R01 ; compte conservé | ND |
| C08-R10 | [initial-administration / 136 — Marqueur externe et première configuration](../../specs/initial-administration/spec.md#L136) | Configuration initiale inachevée | 2.1, 2.4 | B07, B10 | C08 ; finalisation distincte du commit | ND |
| C08-R11 | [initial-administration / 152 — Panneau d'administration contrôlé](../../specs/initial-administration/spec.md#L152) | Administrateur ordinaire soumis aux ACL | 3.2 | Recette de panneau C13 après provisionnement | C13/C04 ; hors réalisation R01 | ND |
| C08-R12 | [initial-administration / 165 — Changement contrôlé de la route d'administration](../../specs/initial-administration/spec.md#L165) | Ancienne route d'administration | 3.2 | Recette de route C13 après provisionnement | C13 ; hors réalisation R01 | ND |
| C08-R13 | [initial-administration / 177 — Expérience et état du panneau](../../specs/initial-administration/spec.md#L177) | Santé réservée au root | 3.2 | Recettes UI C12/C13/C17 | C12/C13 ; hors réalisation R01 | ND |
| C08-R14 | [initial-administration / 192 — Désactivation externe du Super Admin](../../specs/initial-administration/spec.md#L192) | Connexion root désactivée ; Secours malgré le marqueur de désactivation ; Transaction engagée lors de la désactivation | 2.1, 2.4, 3.2 | B10 ; recette de désactivation C03/C04 | C08 distingue les marqueurs ; C04/N05 application | ND |
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
| C08-R25 | [reference-composition / 10 — Capacités obligatoires du P0](../../specs/reference-composition/spec.md#L10) | Capacité P0 absente | 1.1, 3.2, 3.3 | Recette du P0 C17 | C07/C17 ; apport C08 seulement | P |
| C08-R26 | [reference-composition / 22 — Capacités hors P0 explicites](../../specs/reference-composition/spec.md#L22) | Synchronisation non sélectionnée | 1.1, 3.2 | Recette du profil C00/C17 | C00/C17 ; aucune option sélectionnée | P |
| C08-R27 | [reference-composition / 33 — Preuve reproductible](../../specs/reference-composition/spec.md#L33) | Deux validations identiques | 3.2, 3.3 | Recette de composition C07/C17 | C07/C17 ; preuves reproductibles | P |
| C08-R28 | [initial-administration / 218 — Opérateur technique INSTALLER avant base et sessions](../../specs/initial-administration/spec.md#L218) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | B02, B08, B09 ; recette C01 distincte | C01 technique ; R01 sans transfert | R01 — non évalué |
| C08-R29 | [initial-administration / 232 — Limites et refus de la phase technique INSTALLER](../../specs/initial-administration/spec.md#L232) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | B02, B08, B09 | C01 interdit de créer identité/compte | R01 — non évalué |
| C08-R30 | [authorization / 57 — Modèle Subject Resource Action Context](../../specs/authorization/spec.md#L57) | Propriété sans politique refusée ; Sujet technique avant identité applicative | 1.2, 2.3, 2.4 | B01, B02, B09 | C03/C04 ; sujet canonique pour acte C08 | R01 — non évalué |
| C08-R31 | [authorization / 92 — Autorisation technique C01 bornée sans extension métier](../../specs/authorization/spec.md#L92) | Action métier hors bootstrap | 1.2, 2.3, 2.4 | B02, B08, B09 | C01 seulement ; refus d’extension métier | R01 — non évalué |
| C08-R32 | [authorization / 101 — Limites de l’autorité technique d’amorçage](../../specs/authorization/spec.md#L101) | Action métier hors bootstrap | 1.2, 2.3, 2.4 | B02, B09 | UID 0 et forme PLATFORM sans permission | R01 — non évalué |
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

## Empreintes SHA-256 du canon

Les empreintes identifient les sources courantes du complément, sans réécrire les preuves historiques ni valider une réalisation. Une dérive exige une nouvelle lecture du périmètre affecté.

- `openspec/specs/initial-administration/spec.md` : `a875dfd4e48cc2920ea38242b02c46aab386a7a77b645165d009d9fa47f4cc4a`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/installation-provisioning/spec.md` : `b5a8760659f847f663521718e7d8b27d4808dc4aface049a1da84c4e0e967ef6`.
- `openspec/specs/reference-composition/spec.md` : `53f1d388d6999fcf7af05317a9774d2c4e708a90157fe1666b4210e0d1314a4c`.
- `openspec/specs/authorization/spec.md` : `c09e4dac79ecbe6bdb16550d8a4d1566307127818cdeaf9dfbe9224f50858310`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.
- `openspec/specs/audit/spec.md` : `19c58dc8b16e537967c46e69fca4132867e98ada591980b67872ee8c382a5eb1`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.

## Comptage et état des preuves

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


## Parcours PA/PZT validé — deltas proposés et recettes futures

Le parcours PA/PZT → PostgreSQL → PBO a été validé pour formalisation documentaire. Les huit deltas locaux contiennent quatre exigences déjà adoptées (conservées) et le nouveau complément proposé : six exigences modifiées, six exigences ajoutées et vingt-trois scénarios nouveaux nets par rapport aux canons courants. Ces ajouts ne sont pas encore intégrés aux canons et ne sont pas des preuves produit. La branche technique proposée dans authorization répond explicitement à la limite historique ci-dessus ; les règles canoniques actuelles restent applicables jusqu’à adoption.

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

Le périmètre documentaire est de treize fichiers C08 : quatre documents, huit deltas et le seul commentaire de métadonnée. Les empreintes des huit canons sont conservées dans le checkpoint du RUN et doivent rester inchangées à ce jalon ; le code, les migrations, la configuration d’exploitation, BUILD/PROJECT/TECHNICAL et Git ne sont pas modifiés. Les alignements racine sont identifiés dans design.md pour la phase d’adoption.
