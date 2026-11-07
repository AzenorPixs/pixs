# Tâches — C10

État courant : le développeur valide techniquement 1.1 sur sa portée documentaire ; sa case reste non cochée sur instruction explicite. 1.2 reste OUVERTE avec ses barrières. La [validation technique documentaire](design.md#validation-technique-documentaire-de-la-tâche-11) précise cette décision ; les mentions antérieures d’absence de validation complète ou de tâches ouvertes décrivent leurs états historiques, sans annuler cet acquis ni valoir qualification produit.

Ces tâches décrivent la livraison C10 encore non validée. La réconciliation documentaire du 26 octobre 2026 est autorisée pour les quatre documents actifs uniquement ; elle inventorie les raccords partiels préexistants suivis dans C08, sans lancer leur réalisation ou qualification. Toutes les cases restent non cochées ; ni la préparation initiale ni cette réconciliation ne prouvent la satisfaction complète d'une tâche.

## 1. Revue de conception

- [ ] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [ ] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

## 2. Réalisation future

- [ ] 2.1 Publier classification, propriété, finalité, rétention et consommateurs des données effectivement livrées.
- [ ] 2.2 Implémenter demandes relatives aux données et états de suppression logique/rétention.
- [ ] 2.3 Implémenter purge autorisée et tombstones durables avec propagation aux dérivés présents.
- [ ] 2.4 Tester hold/rétention, dérogation Super Admin, rejou, fuite de données non classifiées et restauration sans résurrection avec C16.

## 3. Preuves et clôture futures

- [ ] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [ ] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [ ] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [ ] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

## Raccordement documentaire du 26 octobre 2026

La [matrice R-01 à R-08](requirements.md#traçabilité-des-objectifs-scénarios-contrats-et-tâches) relie objectifs, exigences, scénarios, tâches et critères. La [matrice CP-01 à CP-08](design.md#matrice-des-contrats-propriétaires) distingue contrats propriétaires archivés, interfaces actuelles et relations avec C08/C16/N05 actifs. L'[inventaire des sources et preuves](design.md#inventaire-des-sources-partielles-et-des-preuves) conserve la limite du raccord initial ; aucun contrat archivé n'est rouvert ou modifié.

| Tâche conservée | Références à recouper et critère propre au raccord |
|---|---|
| 1.1 | R-01 à R-08 ; CP-01 à CP-08 : vérifier les clauses courantes, les différences depuis les archives et les seules preuves réellement réutilisables. |
| 1.2 | R-01 à R-08 ; CP-01 à CP-08 : préciser les raccords et refus, les droits/politiques restant ouverts, la publication autorisée déjà adoptée et la source des effacements post-snapshot, avant réalisation dépendante. |
| 2.1 | R-01/R-06/R-07 ; CP-01/CP-02/CP-06/CP-07/CP-08 avec CP-03/CP-04 aux points de contrôle : qualifier profils, classification, publication autorisée et revalidation transactionnelle pour le périmètre livré. |
| 2.2 | R-02/R-03/R-06/R-07 ; CP-01 à CP-07 applicables : réaliser les demandes et transitions chez les propriétaires avec autorisation, audit, CAS et idempotence ; ne pas assimiler les structures mémoire à leur traitement. |
| 2.3 | R-02/R-04/R-05/R-07 ; CP-01/CP-03 à CP-07 : qualifier purge propriétaire par Job, tombstones, rétention/holds et propagation aux dérivés présents, sans publication avant commit ni double effet. |
| 2.4 | R-01 à R-08 ; CP-01 à CP-08 : consolider les preuves de chaque raccord nécessaire, y compris G01–G03 du raccord initial et restauration C16/N05, sans remplacer les contrôles locaux de chaque réalisation. |
| 3.1 | Contrôles configurés applicables au périmètre final, en complément des preuves obtenues pour chaque unité ; aucun test produit exécuté par la présente réconciliation. |
| 3.2 | Revue bidirectionnelle R-01 à R-08 / CP-01 à CP-08 / preuves de tâches, avec isolement, refus, dérogations, absence de secret et non-applicabilités motivées. |
| 3.3 | Examiner fichiers, périmètre, impacts, liens, empreintes et preuves affectées ; conserver les changements préexistants et les limites de livraison. |
| 3.4 | Opérations finales uniquement après les preuves et autorisations nécessaires ; la validation documentaire actuelle n'autorise aucun archivage ni opération Git. |

Les décisions Q1.4-GOV-SOURCE et Q1.4-C10-PUBLISH sont déjà adoptées documentairement dans C08 ; leur réalisation et qualification restent distinctes. Les barrières restantes de design.md ne sont pas levées par cette table. Les dix tâches restent ouvertes, y compris 1.1/1.2 dont les critères dépassent le seul inventaire et la correction des références.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Tester hold/rétention, dérogation Super Admin, rejou, fuite de données non classifiées et restauration sans résurrection avec C16. ; Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1.1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 1.2 | Tâche 1.1 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.1 | Tâche 1.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.2 | Tâche 2.1 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.4 | Tâche 2.3 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.1 | Tâche 2.4 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.2 | Tâche 3.1 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.3 | Tâche 3.2 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |
| 3.4 | Tâche 3.3 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## C10-CONCEPTION-R1 — suivi du 28 octobre 2026

D1, les orientations D2/D3 et les quatre écritures documentaires sont validés par le développeur, sans implémentation ni coche. Les dix cases et leurs identifiants restent inchangés. Cette édition ne valide pas complètement les tâches 1.1/1.2.

| Tâche | Revue consignée | Conditions ouvertes |
|---|---|---|
| 1.1 | [19 exigences et 20 scénarios](requirements.md#c10-conception-r1--couverture-exhaustive-du-canon), C00, CP-01 à CP-08 et complément Agent dans [la revue](design.md#c10-conception-r1--revue-du-28-octobre-2026). | D1 : ressources, consommateurs, opérations et première unité ; preuves réutilisables à vérifier sur les versions effectivement consommées. Tâche non cochée. |
| 1.2 | [Décisions D1–D3](design.md#registre-des-décisions-et-paramètres-ouverts), décisions Q1.4 conservées, refus et propriété explicités ; aucun nouveau delta normatif établi. | D2 : droits/politiques, durées et conditions par ressource ; D3 : propriétaire, stockage, accès, conservation et preuves post-snapshot. Paramètres et contrats requis à valider avant réalisation dépendante. Tâche non cochée. |

Les tâches 2.x/3.x restent futures. Une orientation adoptée ne lève pas globalement les barrières ; aucun paramètre ouvert remplacé par une valeur de test. Cette édition se limite aux quatre documents C10 ; registre, cartographie, canon et archives restent inchangés.

## C10-CONCEPTION-R2 — inventaire et unité retenue

Le développeur valide l’inventaire D1, l’unité users/PLATFORM et les orientations D2, uniquement pour consignation dans les quatre documents. Les dix cases et identifiants de tâches restent inchangés ; aucune implémentation ni coche.

| Tâche | Complément documentaire acquis | Conditions restant ouvertes |
|---|---|---|
| 1.1 | [Inventaire D1](design.md#c10-conception-r2--inventaire-d1-et-unité-usersplatform) : 68 modèles, ressources durables hors SQL identifiées, consommateurs observés et opérations ; première unité CoreUser/users/PLATFORM retenue. | Consommateurs effectivement autorisés et références de profil à arrêter ; disponibilité runtime et réutilisabilité des preuves non déduites de l’inventaire. Tâche non cochée. |
| 1.2 | CONFIDENTIAL/PERSONAL, chemin serveur Core autorisé, profil versionné couvrant explicitement les ressources, réutilisation C04/C05 et transaction propriétaire, exception canonique conservée ; [traçabilité](requirements.md#c10-conception-r2--traçabilité-usersplatform). | Finalité, références, politiques de rétention/suppression/export, résidence, processeurs et configuration protégée ouverts avant réalisation dépendante. D3 reste ouvert pour ses phases futures, sans réadmission post-restauration déduite. Tâche non cochée. |

L’unité users/PLATFORM est une réalisation future bornée du raccord de lecture, avec ses contrôles et intégrations PostgreSQL dès réalisation ; elle ne valide pas tout 2.1 et ne réalise pas une demande ACCESS complète. Les tâches 2.x/3.x ne sont pas engagées. L’inventaire et le choix de première unité remplacent les points D1 laissés ouverts dans le suivi R1 ; les paramètres D2/D3 restants sont conservés. Registre, cartographie, canon et archives restent hors de cette édition limitée aux quatre documents C10.

## D2-USERS-R1 — suivi des paramètres

Le développeur valide D2-USERS-R1 pour consignation dans les seuls proposal.md, design.md, requirements.md et tasks.md, sans implémentation ni coche. Les noms des références, consommateurs serveur, finalité et politiques sont maintenant adoptés documentairement ; les mentions ouvertes correspondantes de R1/R2 décrivent l’état antérieur.

| Tâche | Complément acquis | Conditions restant ouvertes |
|---|---|---|
| 1.1 | Inventaire D1 et unité users/PLATFORM conservés ; [profil et consommateurs D2](design.md#d2-users-r1--profil-consommateurs-et-politiques) documentés. | Compatibilité governance_ref/data_asset_id ; liaisons aux composants et versions ; destinataire HTTP final et emplacements à établir. Tâche non cochée. |
| 1.2 | [Références et politiques adoptées](requirements.md#d2-users-r1--références-adoptées-et-preuves-futures), finalité et lignée explicites ; audit/reçus distincts et exception canonique conservée. | Durées/critères de rétention utilisateurs/audit/reçus, publication autorisée effective, versions/empreintes, autorités, fraîcheur et configuration protégée. D3 demeure ouvert pour ses phases futures. Tâche non cochée. |

Les dix cases restent inchangées et ouvertes ; les tâches 2.x/3.x ne sont pas engagées. Une référence validée documentairement ne constitue pas une politique déployée, un droit d’accès ou une disponibilité qualifiée. Cette édition ne modifie ni sources produit, ni canon, archives, registre ou cartographie.

## D2-USERS-COMPAT-R1 — suivi des décisions C1–C5

Le développeur valide C1–C5 et les seules quatre écritures documentaires C10. L’inspection des données et le reclassement éventuel restent ouverts et non exécutés ; les dix cases et leurs identifiants sont conservés, sans implémentation ni coche.

| Tâche | Choix documentaire acquis | Conditions restant ouvertes |
|---|---|---|
| 1.1 | [C1–C5](design.md#d2-users-compat-r1--compatibilité-des-classifications) : égalité exacte, réutilisation des lignes compatibles, conservation des divergences/NULL, cohérence des producteurs et reclassement séparé. | Inspection propriétaire de la cible : accès autorisé, méthode, périmètre et agrégats réels ; aucune compatibilité des données persistées démontrée. Tâche non cochée. |
| 1.2 | [Traçabilité de compatibilité](requirements.md#d2-users-compat-r1--traçabilité-de-la-compatibilité) et première unité users/PLATFORM maintenue ; aucun alias ni migration implicite. | Nécessité/plan/autorisation d’un reclassement et adaptation éventuelle des producteurs à examiner séparément ; autres paramètres opérationnels D2 et D3 toujours ouverts. Tâche non cochée. |

La qualification future d’un jeu classifié et l’observation des données réelles sont deux preuves distinctes. Aucun accès de base, migration, reclassement ni réalisation 2.x/3.x engagé. Registre, cartographie, canon, archives et sources produit ne sont pas modifiés par cette édition limitée aux quatre documents.

## C10-INSPECTION-R1 — suivi du plan adopté

Le développeur valide le plan et les bornes 1 s / 5 s / 15 s sans réessai automatique, pour consignation dans les seuls quatre documents C10. Aucun accès à la base, implémentation ou coche ; les dix cases et leurs identifiants sont conservés.

| Tâche | Complément documentaire acquis | Conditions restant ouvertes |
|---|---|---|
| 1.1 | [Plan agrégé](design.md#c10-inspection-r1--plan-dinspection-agrégée), catégories disjointes, snapshot, contrôles de sommes/visibilité et minimisation adoptés. | Base, environnement, schéma et cible effectifs ; rôle existant, droits, mécanisme d’accès et preuve de visibilité complète ; données réelles non observées. Tâche non cochée. |
| 1.2 | [Traçabilité du plan](requirements.md#c10-inspection-r1--traçabilité-du-plan-agrégé), lecture seule, bornes et traitement des sorties partielles/non concluantes. | Périmètre de restitution et accès à arrêter avant exécution ; besoin/plan/autorisation du reclassement restent ouverts ; autres paramètres D2/D3 inchangés. Tâche non cochée. |

La méthode et les bornes précisent les mentions antérieures de méthode à définir, sans fermer cible, accès ou inspection réelle. Aucune compatibilité démontrée, aucun raccord ou producteur qualifié. Les tâches 2.x/3.x restent futures ; sources produit, canon, archives, registre et cartographie restent hors de cette édition documentaire.

## C10-INSPECTION-CIBLE-R1 — suivi des informations manquantes

Le développeur valide la consignation du cadrage de cible et d’accès dans les seuls quatre documents C10. Aucun accès à la base, lecture de secrets, implémentation ni coche ; les dix cases et identifiants restent inchangés.

| Tâche | Complément documentaire acquis | Conditions ouvertes |
|---|---|---|
| 1.1 | [Descriptif non secret de cible](design.md#c10-inspection-cible-r1--cible-et-accès), distinction endpoint/machine/déploiement et exigences de visibilité. | Environnement/déploiement, machine, serveur approuvé, base et schéma ; aucune cible effective ni données réelles vérifiées. Tâche non cochée. |
| 1.2 | [Traçabilité accès/visibilité](requirements.md#c10-inspection-cible-r1--traçabilité-de-la-cible-et-des-accès), accès existant et opérateur recommandés ; alternative agent conditionnelle ; bornes antérieures conservées. | Référence et droits d’accès, profil de connexion, opérateur ou mécanisme existant, responsable/preuve de visibilité, autorisation de périmètre et restitution dans la conversation. Tâche non cochée. |

Les informations manquantes sont à fournir ou confirmer sans secret. Validation documentaire distincte de l’autorisation de connexion ; aucune lecture de project.env. Inspection réelle, reclassement éventuel et autres paramètres D2/D3 restent ouverts selon leur phase. Aucune réalisation 2.x/3.x ; sources produit, canon, archives, registre et cartographie restent inchangés.

## C10-INSPECTION-VISIBILITE-R1 — suivi de la preuve attendue

Le développeur valide le protocole de visibilité pour les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés.

| Tâche | Complément documentaire acquis | Conditions ouvertes |
|---|---|---|
| 1.1 | [Protocole de preuve](design.md#c10-inspection-visibilite-r1--preuve-de-visibilité) : relation précise, rôle, droits effectifs, RLS/politiques, contexte et stabilité ; preuve distincte des agrégats. | Cible, accès, structure, rôle/droits, RLS et politiques réels non observés ; opérateur et preuves à établir. Tâche non cochée. |
| 1.2 | [Traçabilité](requirements.md#c10-inspection-visibilite-r1--traçabilité-de-la-preuve) : exemptions constatées sans modification, conclusions complète/PARTIEL/NON CONCLUANT bornées, restitution minimale. | Portée totale, stabilité et autorisation de restitution à démontrer ; aucun changement de rôle ou contournement RLS ; autres paramètres D2/D3 ouverts. Tâche non cochée. |

Aucune inspection réelle ni qualification de compatibilité ; aucun reclassement ou réalisation 2.x/3.x. Bornes 1 s / 5 s / 15 s sans réessai conservées. Sources produit, canon, archives, registre et cartographie restent hors de cette édition.

## C10-INSPECTION-RAPPORT-R1 — suivi du format adopté

Le développeur valide la consignation du format dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés.

| Tâche | Complément documentaire acquis | Conditions ouvertes |
|---|---|---|
| 1.1 | [Format en six parties](design.md#c10-inspection-rapport-r1--format-du-rapport), agrégats minimisés, preuve distincte de visibilité, contrôles de sommes et interprétation du zéro/N/A. | Cible, accès, opérateur et autorisation de restitution ; données et preuves effectives absentes. Tâche non cochée. |
| 1.2 | [Traçabilité des verdicts](requirements.md#c10-inspection-rapport-r1--traçabilité-du-format), séparation exécution/visibilité/cohérence/classification et suites non assimilées à une autorisation. | Inspection non exécutée, compatibilité non démontrée ; paramètres D2/D3 et reclassement éventuel toujours ouverts selon leur phase. Tâche non cochée. |

Aucun rapport de résultats créé ; état actuel NON EXÉCUTÉE, sans compte inventé. Les bornes 1 s / 5 s / 15 s sans réessai restent acquises. Aucune réalisation 2.x/3.x ; sources produit, canon, archives, registre et cartographie restent inchangés.

## C10-INSPECTION-ACCEPTATION-R1 — suivi de la grille adoptée

Le développeur valide la consignation des critères A01–A16 dans les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés.

| Tâche | Complément documentaire acquis | Conditions ouvertes |
|---|---|---|
| 1.1 | [Cas A01–A16](design.md#c10-inspection-acceptation-r1--critères-du-rapport), cas nominaux/partiels/non concluants et recevabilité distincte de conclusion favorable. | Aucun cas exécuté ; cible, accès, données, preuves de visibilité et autorisation de restitution à établir. Tâche non cochée. |
| 1.2 | [Traçabilité et priorité des verdicts](requirements.md#c10-inspection-acceptation-r1--traçabilité-des-critères), confidentialité et absence d’extrapolation. | Inspection NON EXÉCUTÉE, critères non testés, paramètres D2/D3 et besoin/autorisation de reclassement toujours ouverts. Tâche non cochée. |

Aucun rapport de résultats ou preuve produit créé ; aucun raccord, producteur ou restauration qualifié. Bornes 1 s / 5 s / 15 s sans réessai conservées. Aucune réalisation 2.x/3.x ; sources produit, canon, archives, registre et cartographie restent hors de cette édition.

## C10-INSPECTION-SYNTHETIQUES-R1 — suivi des supports fictifs

Le développeur valide les quatre écritures documentaires des maquettes, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés.

| Tâche | Complément documentaire acquis | Conditions ouvertes |
|---|---|---|
| 1.1 | [SYNTH-A01 à SYNTH-A16](design.md#c10-inspection-synthetiques-r1--maquettes-documentaires) : nombres/preuves fictifs, verdicts attendus et variantes négatives, enveloppe commune en six parties. | Maquettes non exécutées ; aucun accès/cible/visibilité réel ni donnée d’exploitation établi. Tâche non cochée. |
| 1.2 | [Traçabilité des maquettes](requirements.md#c10-inspection-synthetiques-r1--traçabilité-des-maquettes) distinguant recevabilité, verdict attendu et limites ; incohérence A11 volontaire et A16 sans valeur interdite. | Inspection réelle NON EXÉCUTÉE ; autres paramètres D2/D3, restitution et reclassement éventuel ouverts. Tâche non cochée. |

Ces supports ne sont ni résultats de tests ni preuves de qualification. Aucun rapport réel ou fichier de tests créé, aucune réalisation 2.x/3.x. Bornes 1 s / 5 s / 15 s sans réessai conservées ; sources produit, canon, archives, registre et cartographie inchangés.

## C10-INSPECTION-SYNTHETIQUES-REVUE-R1 — suivi des corrections

Le développeur valide les corrections dans les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés.

| Tâche | Complément documentaire acquis | Conditions ouvertes |
|---|---|---|
| 1.1 | [Six parties par maquette et variantes](design.md#c10-inspection-synthetiques-revue-r1--maquettes-complétées), comptes détaillés, métadonnées et preuves fictives explicites ; nombres initiaux conservés. | Tous les cas et variantes NON EXÉCUTÉS réellement ; aucune cible/accès/donnée réelle ni preuve de visibilité établi. Tâche non cochée. |
| 1.2 | [Traçabilité](requirements.md#c10-inspection-synthetiques-revue-r1--traçabilité-des-corrections), A12 NON VÉRIFIÉS, hypothèses A06, variantes négatives et limites de recevabilité explicites. | Paramètres D2/D3, restitution et reclassement éventuel toujours ouverts ; aucun contrôle produit ou raccord qualifié. Tâche non cochée. |

La relecture documentaire et ses vérifications arithmétiques ne valent pas exécution d’A01–A16. Inspection réelle NON EXÉCUTÉE ; bornes 1 s / 5 s / 15 s sans réessai conservées, aucune réalisation 2.x/3.x. Sources produit, canon, archives, registre et cartographie restent inchangés.

## Corrections finales des variantes A14 et A15 négatives

Le développeur valide les corrections dans les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés.

| Tâche | Correction documentaire acquise | Conditions ouvertes |
|---|---|---|
| 1.1 | [Hypothèses négatives corrigées](design.md#corrections-finales-des-variantes-a14-et-a15-négatives) : A14 INTERROMPUE sans agrégat complet ; A15 sans preuve de désactivation RLS héritée, portée non établie sous RLS applicable. | Tous les cas fictifs et réellement NON EXÉCUTÉS ; cible, accès, opérateur et preuves de visibilité réels à établir. Tâche non cochée. |
| 1.2 | [Traçabilité finale](requirements.md#corrections-finales-des-variantes-a14-et-a15-négatives), candidat non recevable distingué du diagnostic attendu ; positifs et nombres conservés. | Autorisation de restitution, paramètres D2/D3, classifications réelles et reclassement éventuel toujours ouverts. Tâche non cochée. |

Aucun test produit ni rapport réel ; aucune réalisation 2.x/3.x. Bornes 1 s / 5 s / 15 s sans réessai inchangées ; sources produit, canon, archives, registre et cartographie préservés.

## Revue finale validée des maquettes A01–A16

Le développeur valide la revue documentaire finale et les seules écritures des quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés ouverts.

| Tâche | Conclusion documentaire acquise | Conditions encore ouvertes |
|---|---|---|
| 1.1 | [Revue finale](design.md#revue-finale-validée-des-maquettes-a01a16) achevée : 16 maquettes en six parties et 16 variantes conformes aux critères examinés, comptes fictifs vérifiés et corrections A14/A15 intégrées. | Cible, accès, opérateur, données réelles et preuve de visibilité/stabilité restent à établir. Tâche non cochée. |
| 1.2 | [Traçabilité des conclusions](requirements.md#revue-finale-validée-des-maquettes-a01a16), priorité des verdicts, séparation recevabilité/inspection et absence d’extrapolation confirmées documentairement. | Restitution, autres paramètres D2/D3 et éventuel reclassement toujours ouverts selon leur phase. Tâche non cochée. |

Aucune correction documentaire supplémentaire nécessaire identifiée pour les maquettes examinées. Cela ne démontre ni exécution des cas ni qualification de users/PLATFORM ; aucune validation complète de 1.1/1.2 ou réalisation 2.x/3.x. Inspection réelle NON EXÉCUTÉE ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Sources produit, canon, archives, registre et cartographie préservés.

## C10-CLOTURE-CONCEPTION-R1 — suivi des conditions de passage

Le développeur valide la consignation du plan dans les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases, libellés et critères existants sont conservés ; cette décision ne clôture aucune tâche.

| Tâche | Acquis documentaires | Conditions de clôture encore à satisfaire |
|---|---|---|
| 1.1 | Canon/C00, R-01–R-08, CP-01–CP-08, inventaire et décisions consignés ; revue finale des maquettes validée. | Préparer puis faire valider le [bilan consolidé de revue](design.md#c10-cloture-conception-r1--acquis-et-barrières) avec sources, applicabilité, preuves réutilisables/fixtures, écarts et dépendances non vérifiées. Bilan C10-BILAN-1.1-R1 désormais consigné et validé documentairement ; tâche non cochée. |
| 1.2 | users/PLATFORM, D2-USERS-R1, C1–C5 et choix Q1.4 acquis dans leurs portées. | 1.1 validée ; lever les sept barrières du plan avant réalisation dépendante et présenter fichiers/contrats/éventuel delta. Acquis de l’unité distincts d’une clôture globale ; tâche non cochée. |

La [traçabilité de clôture](requirements.md#c10-cloture-conception-r1--traçabilité-des-conditions-de-clôture) sépare preuves de revue et qualification future, sans masquer les inconnues. Progression : bilan 1.1 d’abord, barrières 1.2 par phase ensuite ; pas de nouvelle série de maquettes. Aucun bilan réputé produit par ce tableau, aucune réalisation 2.x/3.x. Points D2/D3, cible/accès/visibilité/restitution et reclassement éventuel restent ouverts ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Sources produit, canon, archives, registre et cartographie préservés.

## C10-BILAN-1.1-R1 — suivi du bilan documentaire validé

Le développeur valide le bilan consolidé et les quatre écritures documentaires C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés ouverts. Le bilan n’est plus à préparer ou à faire valider documentairement ; ne pas confondre cette validation avec la clôture complète de la tâche.

| Tâche | Acquis désormais consigné | Conditions encore ouvertes |
|---|---|---|
| 1.1 | [Bilan R-01–R-08](design.md#c10-bilan-11-r1--rapprochement-consolidé) présenté et validé sur la portée documentaire, avec sources, acquis, preuves historiques/fixtures et dépendances non vérifiées. | Aucune satisfaction de prérequis de réalisation ni clôture automatique de 1.1 ; dix cases inchangées. Tâche non cochée. |
| 1.2 | [Traçabilité consolidée](requirements.md#c10-bilan-11-r1--traçabilité-consolidée-validée) et choix users/PLATFORM conservés, sans réduction de la tâche globale. | Sept barrières de conception ouvertes selon C10-CLOTURE-CONCEPTION-R1 ; contrats et paramètres requis avant réalisation dépendante. Tâche non cochée. |

Cible réelle, accès, opérateur, droits/RLS/stabilité, preuve de visibilité, restitution, classifications et reclassement éventuel restent ouverts ; paramètres D2/D3 non arrêtés conservés. Inspection NON EXÉCUTÉE, aucun raccord/producteur/restauration qualifié. Aucune réalisation 2.x/3.x ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Sources produit, canon, archives, registre et cartographie préservés.

## Validation technique documentaire de la tâche 1.1

Validation explicite du développeur : 1.1 est VALIDÉE TECHNIQUEMENT SUR SA PORTÉE DOCUMENTAIRE après bilan consolidé et revue finale. Consignation autorisée dans les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases, libellés et identifiants sont conservés.

| Tâche | État de validation courant | État de case et limites |
|---|---|---|
| 1.1 | Validation technique documentaire ACQUISE sur la revue R-01–R-08/canon/C00/sources/contrats et limites des preuves ; [décision](design.md#validation-technique-documentaire-de-la-tâche-11). | NON COCHÉE sur instruction explicite ; absence de coche ne signifie pas absence de validation. Aucun prérequis runtime réputé satisfait. |
| 1.2 | OUVERTE ; préalable de validation documentaire de 1.1 acquis, sans levée de ses propres barrières. | NON COCHÉE ; sept barrières, paramètres D2/D3 et dépendances non vérifiées conservés. Aucune clôture implicite. |

La [traçabilité de validation](requirements.md#validation-technique-documentaire-de-la-tâche-11) actualise les formulations historiques limitées à la seule validation du bilan. Cette même validation documentaire 1.1 n’est pas à redemander ; aucune autorisation de réalisation 2.x/3.x, d’inspection ou de qualification n’en découle. Cible/accès/preuves/restitution/classifications réelles et reclassement éventuel ouverts. Inspection et maquettes NON EXÉCUTÉES, bornes 1 s / 5 s / 15 s sans réessai conservées. Sources produit, canon, archives, registre et cartographie inchangés.

## C10-POLITIQUES-OPERATIONNELLES-R1 — suivi des politiques

Le développeur valide les quatre écritures documentaires, sans accès à la base, lecture de secrets, implémentation ni coche. La validation technique documentaire 1.1 est conservée ; sa case et les neuf autres restent non cochées. 1.2 demeure OUVERTE.

| Tâche | Acquis courant | Conditions ouvertes |
|---|---|---|
| 1.1 | Validation technique documentaire déjà acquise et conservée, sans nouvelle demande de validation de la même revue. | Case volontairement non cochée ; aucune disponibilité produit réputée acquise. |
| 1.2 | [Politiques utilisateurs/audit/reçus et P1–P6](design.md#c10-politiques-operationnelles-r1--utilisateurs-audit-et-reçus), références et séparation des responsabilités documentées ; [traçabilité](requirements.md#c10-politiques-operationnelles-r1--traçabilité-des-politiques). | Durées/départs, classifications techniques, autorités, consommateurs, limites/occultations d’audit et mécanisme de fin de conservation des reçus à arrêter. Barrière non entièrement levée ; tâche non cochée. |

Les autres barrières de 1.2, paramètres D2/D3 et points cible/accès/visibilité/restitution/reclassement restent ouverts. Aucun mécanisme de purge, configuration, publication ou durée de conservation chiffrée appliqué ; inspection/maquettes NON EXÉCUTÉES. Aucune réalisation 2.x/3.x ; bornes d’inspection 1 s / 5 s / 15 s sans réessai inchangées. Sources produit, canon, archives, registre et cartographie préservés.

## C10-CONSERVATION-R1 — suivi des ancres et paramètres ouverts

Le développeur valide C10-CONSERVATION-R1 pour les quatre documents uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés ; 1.1 reste validée techniquement sur sa portée documentaire et 1.2 OUVERTE.

| Tâche | Acquis courant | Conditions ouvertes |
|---|---|---|
| 1.1 | Validation technique documentaire conservée sans redemande pour la même portée. | Case non cochée sur instruction explicite, aucune qualification produit déduite. |
| 1.2 | [Ancres et DUR1–DUR6](design.md#c10-conservation-r1--événements-durées-et-maintenance), stabilité/historique et séparation échéance/maintenance ; [traçabilité](requirements.md#c10-conservation-r1--traçabilité-des-ancres-et-durées). | Durées chiffrées/finalités/départs vérifiables, états archivés, catégories d’audit, clôture et réconciliation des reçus, responsable et mécanisme de fin de conservation à arrêter. Barrière non close ; tâche non cochée. |

Paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel toujours ouverts selon leur phase. Aucun champ/migration/journal ou mécanisme de purge réalisé ; inspection/maquettes NON EXÉCUTÉES. Bornes 1 s / 5 s / 15 s sans réessai conservées et distinctes de la rétention ; aucune réalisation 2.x/3.x. Sources produit, canon, archives, registre et cartographie inchangés.

## C10-DUREES-R1 — suivi des valeurs adoptées

Le développeur valide les valeurs et CH1–CH6 pour les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés ; 1.1 reste validée techniquement sur sa portée documentaire, 1.2 OUVERTE.

| Tâche | Acquis courant | Conditions ouvertes |
|---|---|---|
| 1.1 | Validation technique documentaire conservée, sans nouvelle demande pour la même portée. | Case non cochée sur instruction explicite ; aucune preuve produit déduite. |
| 1.2 | [30/186/90 jours et CH1–CH6](design.md#c10-durees-r1--valeurs-justifications-et-décisions), réexamens à 90 jours distincts des durées de vie ; [traçabilité](requirements.md#c10-durees-r1--traçabilité-des-valeurs-et-ch1ch6). | Déploiement/versions applicables, responsables et premier réexamen, contrats/preuves d’ancrage, minimisation et maintenance compatible avec les propriétaires. Barrière non close ; tâche non cochée. |

Les anciennes mentions de durées chiffrées non choisies décrivent les étapes précédentes ; seules les valeurs et règles présentées sont désormais adoptées documentairement, pas une politique déployée. Autres paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel ouverts. Aucun scheduler, migration, occultation ou purge activé, aucune réalisation 2.x/3.x ; inspection/maquettes NON EXÉCUTÉES. Bornes d’inspection 1 s / 5 s / 15 s sans réessai conservées ; sources produit, canon, archives, registre et cartographie inchangés.

## C10-MINIMISATION-R1 — suivi des règles adoptées

Le développeur valide les règles de champs et MIN1–MIN6 pour les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les dix cases et identifiants sont conservés ; validation technique documentaire 1.1 acquise et 1.2 OUVERTE.

| Tâche | Acquis courant | Conditions ouvertes |
|---|---|---|
| 1.1 | Validation documentaire conservée sans redemande pour la même portée. | Case volontairement non cochée ; aucune qualification produit déduite. |
| 1.2 | [Champs audits/reçus et MIN1–MIN6](design.md#c10-minimisation-r1--audits-et-reçus-après-suppression), maintenance C05 distincte de restitution des reçus immuables ; [traçabilité](requirements.md#c10-minimisation-r1--traçabilité-des-champs-et-min1min6). | Sélection, preuves des liens d’identité, pseudonymisation de confiance, nécessité résiduelle, C01/champs non modifiables et fin de conservation compatibles avec les propriétaires à arrêter. Tâche non cochée. |

Durées et ancres 30/186/90 jours conservées sans remise à zéro ; autres paramètres D2/D3 et cible/accès/visibilité/restitution/reclassement éventuel ouverts. Aucun traitement, occultation, purge ou contrat de sortie implémenté, aucune réalisation 2.x/3.x ; inspection/maquettes NON EXÉCUTÉES. Bornes d’inspection 1 s / 5 s / 15 s sans réessai inchangées ; sources produit, canon, archives, registre et cartographie préservés.

## C10-RAPPROCHEMENT-R1 — suivi de la sélection documentaire

Le développeur valide les quatre écritures documentaires, sans accès à la base, lecture de secrets, implémentation ni coche. Dix cases et identifiants inchangés ; validation technique documentaire 1.1 acquise et 1.2 OUVERTE.

| Tâche | Acquis courant | Conditions ouvertes |
|---|---|---|
| 1.1 | Validation technique documentaire conservée, sans redemande pour la même portée. | Case volontairement non cochée ; aucun raccord réel qualifié. |
| 1.2 | [Critères, preuves et RAP1–RAP6](design.md#c10-rapprochement-r1--sélection-et-preuves-propriétaires), références exactes, temporalité, reçus indirects, statuts d’incertitude et passage séparé à MIN1–MIN6 ; [traçabilité](requirements.md#c10-rapprochement-r1--traçabilité-des-critères-et-preuves). | Interfaces de preuve, historique, conflits, conservation des preuves et exhaustivité à arrêter ; sélection et minimisation non réalisées. Tâche non cochée. |

Autres paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel ouverts ; durées 30/186/90 jours, ancres et réexamens conservés. Aucun droit ou mécanisme déduit du rapprochement, aucun traitement des données ou réalisation 2.x/3.x. Inspection/maquettes NON EXÉCUTÉES ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Sources produit, canon, archives, registre et cartographie préservés.

## C10-HISTORIQUE-LIENS-R1 — suivi de la preuve historique

Le développeur valide les quatre écritures documentaires, sans accès à la base, lecture de secrets, implémentation ni coche. Dix cases et identifiants conservés ; validation technique documentaire 1.1 acquise et 1.2 OUVERTE.

| Tâche | Acquis courant | Conditions ouvertes |
|---|---|---|
| 1.1 | Validation technique documentaire conservée, sans nouvelle demande pour la même portée. | Case volontairement non cochée ; aucune disponibilité historique qualifiée. |
| 1.2 | [Sources/contrôles et HIST1–HIST6](design.md#c10-historique-liens-r1--sources-et-contrôles-historiques), limites du courant/audit/rejeu et preuve Core bornée ; [traçabilité](requirements.md#c10-historique-liens-r1--traçabilité-des-sources-historiques). | Interface, faits disponibles, précision temporelle, exhaustivité, déduplication contractuelle, conflits et conservation de preuve à arrêter. Tâche non cochée. |

Durées 30/186/90 jours non étendues automatiquement aux preuves historiques ; autres paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel ouverts. Aucun nouveau journal ou mécanisme de preuve/minimisation implémenté, aucune réalisation 2.x/3.x. Inspection/maquettes NON EXÉCUTÉES ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Sources produit, canon, archives, registre et cartographie préservés.

## C10-1.2-PUBLICATION-CADRE-R2 — suivi

1.1 validée techniquement, case non cochée, conservée. 1.2 OUVERTE.
Barrière 2 cadrée par checklist design, non levée. Autres barrières 1,3,4,5,6,7 et points cible/accès/visibilité/restitution/D2/D3 ouverts. Dix cases ouvertes, 2.x/3.x futures. Inspection NON EXÉCUTÉE.

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et clôture futures » ; « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future » ; « C10-INSPECTION-VISIBILITE-R1 — suivi de la preuve attendue » ; « C10-BILAN-1.1-R1 — suivi du bilan documentaire validé » ; « Validation technique documentaire de la tâche 1.1 » ; « C10-HISTORIQUE-LIENS-R1 — suivi de la preuve historique ».

### C10-SL01 — Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 32 du texte conservé.
  - Références à recouper et critère propre au raccord : R-01 à R-08 ; CP-01 à CP-08 : vérifier les clauses courantes, les différences depuis les archives et les seules preuves réellement réutilisables.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 63 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Dépendances, critères et contrôles sourcés : tableau « C10-CONCEPTION-R1 — suivi du 28 octobre 2026 », ligne 84 du texte conservé.
  - Revue consignée : [19 exigences et 20 scénarios](requirements.md#c10-conception-r1--couverture-exhaustive-du-canon), C00, CP-01 à CP-08 et complément Agent dans [la revue](design.md#c10-conception-r1--revue-du-28-octobre-2026).
  - Conditions ouvertes : D1 : ressources, consommateurs, opérations et première unité ; preuves réutilisables à vérifier sur les versions effectivement consommées. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-CONCEPTION-R2 — inventaire et unité retenue », ligne 95 du texte conservé.
  - Complément documentaire acquis : [Inventaire D1](design.md#c10-conception-r2--inventaire-d1-et-unité-usersplatform) : 68 modèles, ressources durables hors SQL identifiées, consommateurs observés et opérations ; première unité CoreUser/users/PLATFORM retenue.
  - Conditions restant ouvertes : Consommateurs effectivement autorisés et références de profil à arrêter ; disponibilité runtime et réutilisabilité des preuves non déduites de l’inventaire. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « D2-USERS-R1 — suivi des paramètres », ligne 106 du texte conservé.
  - Complément acquis : Inventaire D1 et unité users/PLATFORM conservés ; [profil et consommateurs D2](design.md#d2-users-r1--profil-consommateurs-et-politiques) documentés.
  - Conditions restant ouvertes : Compatibilité governance_ref/data_asset_id ; liaisons aux composants et versions ; destinataire HTTP final et emplacements à établir. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « D2-USERS-COMPAT-R1 — suivi des décisions C1–C5 », ligne 117 du texte conservé.
  - Choix documentaire acquis : [C1–C5](design.md#d2-users-compat-r1--compatibilité-des-classifications) : égalité exacte, réutilisation des lignes compatibles, conservation des divergences/NULL, cohérence des producteurs et reclassement séparé.
  - Conditions restant ouvertes : Inspection propriétaire de la cible : accès autorisé, méthode, périmètre et agrégats réels ; aucune compatibilité des données persistées démontrée. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-R1 — suivi du plan adopté », ligne 128 du texte conservé.
  - Complément documentaire acquis : [Plan agrégé](design.md#c10-inspection-r1--plan-dinspection-agrégée), catégories disjointes, snapshot, contrôles de sommes/visibilité et minimisation adoptés.
  - Conditions restant ouvertes : Base, environnement, schéma et cible effectifs ; rôle existant, droits, mécanisme d’accès et preuve de visibilité complète ; données réelles non observées. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-CIBLE-R1 — suivi des informations manquantes », ligne 139 du texte conservé.
  - Complément documentaire acquis : [Descriptif non secret de cible](design.md#c10-inspection-cible-r1--cible-et-accès), distinction endpoint/machine/déploiement et exigences de visibilité.
  - Conditions ouvertes : Environnement/déploiement, machine, serveur approuvé, base et schéma ; aucune cible effective ni données réelles vérifiées. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-VISIBILITE-R1 — suivi de la preuve attendue », ligne 150 du texte conservé.
  - Complément documentaire acquis : [Protocole de preuve](design.md#c10-inspection-visibilite-r1--preuve-de-visibilité) : relation précise, rôle, droits effectifs, RLS/politiques, contexte et stabilité ; preuve distincte des agrégats.
  - Conditions ouvertes : Cible, accès, structure, rôle/droits, RLS et politiques réels non observés ; opérateur et preuves à établir. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-RAPPORT-R1 — suivi du format adopté », ligne 161 du texte conservé.
  - Complément documentaire acquis : [Format en six parties](design.md#c10-inspection-rapport-r1--format-du-rapport), agrégats minimisés, preuve distincte de visibilité, contrôles de sommes et interprétation du zéro/N/A.
  - Conditions ouvertes : Cible, accès, opérateur et autorisation de restitution ; données et preuves effectives absentes. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-ACCEPTATION-R1 — suivi de la grille adoptée », ligne 172 du texte conservé.
  - Complément documentaire acquis : [Cas A01–A16](design.md#c10-inspection-acceptation-r1--critères-du-rapport), cas nominaux/partiels/non concluants et recevabilité distincte de conclusion favorable.
  - Conditions ouvertes : Aucun cas exécuté ; cible, accès, données, preuves de visibilité et autorisation de restitution à établir. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-SYNTHETIQUES-R1 — suivi des supports fictifs », ligne 183 du texte conservé.
  - Complément documentaire acquis : [SYNTH-A01 à SYNTH-A16](design.md#c10-inspection-synthetiques-r1--maquettes-documentaires) : nombres/preuves fictifs, verdicts attendus et variantes négatives, enveloppe commune en six parties.
  - Conditions ouvertes : Maquettes non exécutées ; aucun accès/cible/visibilité réel ni donnée d’exploitation établi. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-SYNTHETIQUES-REVUE-R1 — suivi des corrections », ligne 194 du texte conservé.
  - Complément documentaire acquis : [Six parties par maquette et variantes](design.md#c10-inspection-synthetiques-revue-r1--maquettes-complétées), comptes détaillés, métadonnées et preuves fictives explicites ; nombres initiaux conservés.
  - Conditions ouvertes : Tous les cas et variantes NON EXÉCUTÉS réellement ; aucune cible/accès/donnée réelle ni preuve de visibilité établi. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Corrections finales des variantes A14 et A15 négatives », ligne 205 du texte conservé.
  - Correction documentaire acquise : [Hypothèses négatives corrigées](design.md#corrections-finales-des-variantes-a14-et-a15-négatives) : A14 INTERROMPUE sans agrégat complet ; A15 sans preuve de désactivation RLS héritée, portée non établie sous RLS applicable.
  - Conditions ouvertes : Tous les cas fictifs et réellement NON EXÉCUTÉS ; cible, accès, opérateur et preuves de visibilité réels à établir. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Revue finale validée des maquettes A01–A16 », ligne 216 du texte conservé.
  - Conclusion documentaire acquise : [Revue finale](design.md#revue-finale-validée-des-maquettes-a01a16) achevée : 16 maquettes en six parties et 16 variantes conformes aux critères examinés, comptes fictifs vérifiés et corrections A14/A15 intégrées.
  - Conditions encore ouvertes : Cible, accès, opérateur, données réelles et preuve de visibilité/stabilité restent à établir. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-CLOTURE-CONCEPTION-R1 — suivi des conditions de passage », ligne 227 du texte conservé.
  - Acquis documentaires : Canon/C00, R-01–R-08, CP-01–CP-08, inventaire et décisions consignés ; revue finale des maquettes validée.
  - Conditions de clôture encore à satisfaire : Préparer puis faire valider le [bilan consolidé de revue](design.md#c10-cloture-conception-r1--acquis-et-barrières) avec sources, applicabilité, preuves réutilisables/fixtures, écarts et dépendances non vérifiées. Bilan C10-BILAN-1.1-R1 désormais consigné et validé documentairement ; tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-BILAN-1.1-R1 — suivi du bilan documentaire validé », ligne 238 du texte conservé.
  - Acquis désormais consigné : [Bilan R-01–R-08](design.md#c10-bilan-11-r1--rapprochement-consolidé) présenté et validé sur la portée documentaire, avec sources, acquis, preuves historiques/fixtures et dépendances non vérifiées.
  - Conditions encore ouvertes : Aucune satisfaction de prérequis de réalisation ni clôture automatique de 1.1 ; dix cases inchangées. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Validation technique documentaire de la tâche 1.1 », ligne 249 du texte conservé.
  - État de validation courant : Validation technique documentaire ACQUISE sur la revue R-01–R-08/canon/C00/sources/contrats et limites des preuves ; [décision](design.md#validation-technique-documentaire-de-la-tâche-11).
  - État de case et limites : NON COCHÉE sur instruction explicite ; absence de coche ne signifie pas absence de validation. Aucun prérequis runtime réputé satisfait.
- Dépendances, critères et contrôles sourcés : tableau « C10-POLITIQUES-OPERATIONNELLES-R1 — suivi des politiques », ligne 260 du texte conservé.
  - Acquis courant : Validation technique documentaire déjà acquise et conservée, sans nouvelle demande de validation de la même revue.
  - Conditions ouvertes : Case volontairement non cochée ; aucune disponibilité produit réputée acquise.
- Dépendances, critères et contrôles sourcés : tableau « C10-CONSERVATION-R1 — suivi des ancres et paramètres ouverts », ligne 271 du texte conservé.
  - Acquis courant : Validation technique documentaire conservée sans redemande pour la même portée.
  - Conditions ouvertes : Case non cochée sur instruction explicite, aucune qualification produit déduite.
- Dépendances, critères et contrôles sourcés : tableau « C10-DUREES-R1 — suivi des valeurs adoptées », ligne 282 du texte conservé.
  - Acquis courant : Validation technique documentaire conservée, sans nouvelle demande pour la même portée.
  - Conditions ouvertes : Case non cochée sur instruction explicite ; aucune preuve produit déduite.
- Dépendances, critères et contrôles sourcés : tableau « C10-MINIMISATION-R1 — suivi des règles adoptées », ligne 293 du texte conservé.
  - Acquis courant : Validation documentaire conservée sans redemande pour la même portée.
  - Conditions ouvertes : Case volontairement non cochée ; aucune qualification produit déduite.
- Dépendances, critères et contrôles sourcés : tableau « C10-RAPPROCHEMENT-R1 — suivi de la sélection documentaire », ligne 304 du texte conservé.
  - Acquis courant : Validation technique documentaire conservée, sans redemande pour la même portée.
  - Conditions ouvertes : Case volontairement non cochée ; aucun raccord réel qualifié.
- Dépendances, critères et contrôles sourcés : tableau « C10-HISTORIQUE-LIENS-R1 — suivi de la preuve historique », ligne 315 du texte conservé.
  - Acquis courant : Validation technique documentaire conservée, sans nouvelle demande pour la même portée.
  - Conditions ouvertes : Case volontairement non cochée ; aucune disponibilité historique qualifiée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État documentaire : VALIDÉ sur la seule portée de revue documentaire 1.1, attestée dans [design.md](design.md), section « Validation technique documentaire de la tâche 1.1 », et constatée le 30 octobre 2026. La case reste non cochée ; cette validation ne qualifie aucun raccord runtime.

### C10-SL02 — Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 33 du texte conservé.
  - Références à recouper et critère propre au raccord : R-01 à R-08 ; CP-01 à CP-08 : préciser les raccords et refus, les droits/politiques restant ouverts, la publication autorisée déjà adoptée et la source des effacements post-snapshot, avant réalisation dépendante.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 64 du texte conservé.
  - Prérequis immédiat : Tâche 1.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Dépendances, critères et contrôles sourcés : tableau « C10-CONCEPTION-R1 — suivi du 28 octobre 2026 », ligne 85 du texte conservé.
  - Revue consignée : [Décisions D1–D3](design.md#registre-des-décisions-et-paramètres-ouverts), décisions Q1.4 conservées, refus et propriété explicités ; aucun nouveau delta normatif établi.
  - Conditions ouvertes : D2 : droits/politiques, durées et conditions par ressource ; D3 : propriétaire, stockage, accès, conservation et preuves post-snapshot. Paramètres et contrats requis à valider avant réalisation dépendante. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-CONCEPTION-R2 — inventaire et unité retenue », ligne 96 du texte conservé.
  - Complément documentaire acquis : CONFIDENTIAL/PERSONAL, chemin serveur Core autorisé, profil versionné couvrant explicitement les ressources, réutilisation C04/C05 et transaction propriétaire, exception canonique conservée ; [traçabilité](requirements.md#c10-conception-r2--traçabilité-usersplatform).
  - Conditions restant ouvertes : Finalité, références, politiques de rétention/suppression/export, résidence, processeurs et configuration protégée ouverts avant réalisation dépendante. D3 reste ouvert pour ses phases futures, sans réadmission post-restauration déduite. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « D2-USERS-R1 — suivi des paramètres », ligne 107 du texte conservé.
  - Complément acquis : [Références et politiques adoptées](requirements.md#d2-users-r1--références-adoptées-et-preuves-futures), finalité et lignée explicites ; audit/reçus distincts et exception canonique conservée.
  - Conditions restant ouvertes : Durées/critères de rétention utilisateurs/audit/reçus, publication autorisée effective, versions/empreintes, autorités, fraîcheur et configuration protégée. D3 demeure ouvert pour ses phases futures. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « D2-USERS-COMPAT-R1 — suivi des décisions C1–C5 », ligne 118 du texte conservé.
  - Choix documentaire acquis : [Traçabilité de compatibilité](requirements.md#d2-users-compat-r1--traçabilité-de-la-compatibilité) et première unité users/PLATFORM maintenue ; aucun alias ni migration implicite.
  - Conditions restant ouvertes : Nécessité/plan/autorisation d’un reclassement et adaptation éventuelle des producteurs à examiner séparément ; autres paramètres opérationnels D2 et D3 toujours ouverts. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-R1 — suivi du plan adopté », ligne 129 du texte conservé.
  - Complément documentaire acquis : [Traçabilité du plan](requirements.md#c10-inspection-r1--traçabilité-du-plan-agrégé), lecture seule, bornes et traitement des sorties partielles/non concluantes.
  - Conditions restant ouvertes : Périmètre de restitution et accès à arrêter avant exécution ; besoin/plan/autorisation du reclassement restent ouverts ; autres paramètres D2/D3 inchangés. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-CIBLE-R1 — suivi des informations manquantes », ligne 140 du texte conservé.
  - Complément documentaire acquis : [Traçabilité accès/visibilité](requirements.md#c10-inspection-cible-r1--traçabilité-de-la-cible-et-des-accès), accès existant et opérateur recommandés ; alternative agent conditionnelle ; bornes antérieures conservées.
  - Conditions ouvertes : Référence et droits d’accès, profil de connexion, opérateur ou mécanisme existant, responsable/preuve de visibilité, autorisation de périmètre et restitution dans la conversation. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-VISIBILITE-R1 — suivi de la preuve attendue », ligne 151 du texte conservé.
  - Complément documentaire acquis : [Traçabilité](requirements.md#c10-inspection-visibilite-r1--traçabilité-de-la-preuve) : exemptions constatées sans modification, conclusions complète/PARTIEL/NON CONCLUANT bornées, restitution minimale.
  - Conditions ouvertes : Portée totale, stabilité et autorisation de restitution à démontrer ; aucun changement de rôle ou contournement RLS ; autres paramètres D2/D3 ouverts. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-RAPPORT-R1 — suivi du format adopté », ligne 162 du texte conservé.
  - Complément documentaire acquis : [Traçabilité des verdicts](requirements.md#c10-inspection-rapport-r1--traçabilité-du-format), séparation exécution/visibilité/cohérence/classification et suites non assimilées à une autorisation.
  - Conditions ouvertes : Inspection non exécutée, compatibilité non démontrée ; paramètres D2/D3 et reclassement éventuel toujours ouverts selon leur phase. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-ACCEPTATION-R1 — suivi de la grille adoptée », ligne 173 du texte conservé.
  - Complément documentaire acquis : [Traçabilité et priorité des verdicts](requirements.md#c10-inspection-acceptation-r1--traçabilité-des-critères), confidentialité et absence d’extrapolation.
  - Conditions ouvertes : Inspection NON EXÉCUTÉE, critères non testés, paramètres D2/D3 et besoin/autorisation de reclassement toujours ouverts. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-SYNTHETIQUES-R1 — suivi des supports fictifs », ligne 184 du texte conservé.
  - Complément documentaire acquis : [Traçabilité des maquettes](requirements.md#c10-inspection-synthetiques-r1--traçabilité-des-maquettes) distinguant recevabilité, verdict attendu et limites ; incohérence A11 volontaire et A16 sans valeur interdite.
  - Conditions ouvertes : Inspection réelle NON EXÉCUTÉE ; autres paramètres D2/D3, restitution et reclassement éventuel ouverts. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-INSPECTION-SYNTHETIQUES-REVUE-R1 — suivi des corrections », ligne 195 du texte conservé.
  - Complément documentaire acquis : [Traçabilité](requirements.md#c10-inspection-synthetiques-revue-r1--traçabilité-des-corrections), A12 NON VÉRIFIÉS, hypothèses A06, variantes négatives et limites de recevabilité explicites.
  - Conditions ouvertes : Paramètres D2/D3, restitution et reclassement éventuel toujours ouverts ; aucun contrôle produit ou raccord qualifié. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Corrections finales des variantes A14 et A15 négatives », ligne 206 du texte conservé.
  - Correction documentaire acquise : [Traçabilité finale](requirements.md#corrections-finales-des-variantes-a14-et-a15-négatives), candidat non recevable distingué du diagnostic attendu ; positifs et nombres conservés.
  - Conditions ouvertes : Autorisation de restitution, paramètres D2/D3, classifications réelles et reclassement éventuel toujours ouverts. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Revue finale validée des maquettes A01–A16 », ligne 217 du texte conservé.
  - Conclusion documentaire acquise : [Traçabilité des conclusions](requirements.md#revue-finale-validée-des-maquettes-a01a16), priorité des verdicts, séparation recevabilité/inspection et absence d’extrapolation confirmées documentairement.
  - Conditions encore ouvertes : Restitution, autres paramètres D2/D3 et éventuel reclassement toujours ouverts selon leur phase. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-CLOTURE-CONCEPTION-R1 — suivi des conditions de passage », ligne 228 du texte conservé.
  - Acquis documentaires : users/PLATFORM, D2-USERS-R1, C1–C5 et choix Q1.4 acquis dans leurs portées.
  - Conditions de clôture encore à satisfaire : 1.1 validée ; lever les sept barrières du plan avant réalisation dépendante et présenter fichiers/contrats/éventuel delta. Acquis de l’unité distincts d’une clôture globale ; tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-BILAN-1.1-R1 — suivi du bilan documentaire validé », ligne 239 du texte conservé.
  - Acquis désormais consigné : [Traçabilité consolidée](requirements.md#c10-bilan-11-r1--traçabilité-consolidée-validée) et choix users/PLATFORM conservés, sans réduction de la tâche globale.
  - Conditions encore ouvertes : Sept barrières de conception ouvertes selon C10-CLOTURE-CONCEPTION-R1 ; contrats et paramètres requis avant réalisation dépendante. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Validation technique documentaire de la tâche 1.1 », ligne 250 du texte conservé.
  - État de validation courant : OUVERTE ; préalable de validation documentaire de 1.1 acquis, sans levée de ses propres barrières.
  - État de case et limites : NON COCHÉE ; sept barrières, paramètres D2/D3 et dépendances non vérifiées conservés. Aucune clôture implicite.
- Dépendances, critères et contrôles sourcés : tableau « C10-POLITIQUES-OPERATIONNELLES-R1 — suivi des politiques », ligne 261 du texte conservé.
  - Acquis courant : [Politiques utilisateurs/audit/reçus et P1–P6](design.md#c10-politiques-operationnelles-r1--utilisateurs-audit-et-reçus), références et séparation des responsabilités documentées ; [traçabilité](requirements.md#c10-politiques-operationnelles-r1--traçabilité-des-politiques).
  - Conditions ouvertes : Durées/départs, classifications techniques, autorités, consommateurs, limites/occultations d’audit et mécanisme de fin de conservation des reçus à arrêter. Barrière non entièrement levée ; tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-CONSERVATION-R1 — suivi des ancres et paramètres ouverts », ligne 272 du texte conservé.
  - Acquis courant : [Ancres et DUR1–DUR6](design.md#c10-conservation-r1--événements-durées-et-maintenance), stabilité/historique et séparation échéance/maintenance ; [traçabilité](requirements.md#c10-conservation-r1--traçabilité-des-ancres-et-durées).
  - Conditions ouvertes : Durées chiffrées/finalités/départs vérifiables, états archivés, catégories d’audit, clôture et réconciliation des reçus, responsable et mécanisme de fin de conservation à arrêter. Barrière non close ; tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-DUREES-R1 — suivi des valeurs adoptées », ligne 283 du texte conservé.
  - Acquis courant : [30/186/90 jours et CH1–CH6](design.md#c10-durees-r1--valeurs-justifications-et-décisions), réexamens à 90 jours distincts des durées de vie ; [traçabilité](requirements.md#c10-durees-r1--traçabilité-des-valeurs-et-ch1ch6).
  - Conditions ouvertes : Déploiement/versions applicables, responsables et premier réexamen, contrats/preuves d’ancrage, minimisation et maintenance compatible avec les propriétaires. Barrière non close ; tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-MINIMISATION-R1 — suivi des règles adoptées », ligne 294 du texte conservé.
  - Acquis courant : [Champs audits/reçus et MIN1–MIN6](design.md#c10-minimisation-r1--audits-et-reçus-après-suppression), maintenance C05 distincte de restitution des reçus immuables ; [traçabilité](requirements.md#c10-minimisation-r1--traçabilité-des-champs-et-min1min6).
  - Conditions ouvertes : Sélection, preuves des liens d’identité, pseudonymisation de confiance, nécessité résiduelle, C01/champs non modifiables et fin de conservation compatibles avec les propriétaires à arrêter. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-RAPPROCHEMENT-R1 — suivi de la sélection documentaire », ligne 305 du texte conservé.
  - Acquis courant : [Critères, preuves et RAP1–RAP6](design.md#c10-rapprochement-r1--sélection-et-preuves-propriétaires), références exactes, temporalité, reçus indirects, statuts d’incertitude et passage séparé à MIN1–MIN6 ; [traçabilité](requirements.md#c10-rapprochement-r1--traçabilité-des-critères-et-preuves).
  - Conditions ouvertes : Interfaces de preuve, historique, conflits, conservation des preuves et exhaustivité à arrêter ; sélection et minimisation non réalisées. Tâche non cochée.
- Dépendances, critères et contrôles sourcés : tableau « C10-HISTORIQUE-LIENS-R1 — suivi de la preuve historique », ligne 316 du texte conservé.
  - Acquis courant : [Sources/contrôles et HIST1–HIST6](design.md#c10-historique-liens-r1--sources-et-contrôles-historiques), limites du courant/audit/rejeu et preuve Core bornée ; [traçabilité](requirements.md#c10-historique-liens-r1--traçabilité-des-sources-historiques).
  - Conditions ouvertes : Interface, faits disponibles, précision temporelle, exhaustivité, déduplication contractuelle, conflits et conservation de preuve à arrêter. Tâche non cochée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL03 — Publier classification, propriété, finalité, rétention et consommateurs des données effectivement livrées.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation future », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 34 du texte conservé.
  - Références à recouper et critère propre au raccord : R-01/R-06/R-07 ; CP-01/CP-02/CP-06/CP-07/CP-08 avec CP-03/CP-04 aux points de contrôle : qualifier profils, classification, publication autorisée et revalidation transactionnelle pour le périmètre livré.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 65 du texte conservé.
  - Prérequis immédiat : Tâche 1.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL04 — Implémenter demandes relatives aux données et états de suppression logique/rétention.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation future », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 35 du texte conservé.
  - Références à recouper et critère propre au raccord : R-02/R-03/R-06/R-07 ; CP-01 à CP-07 applicables : réaliser les demandes et transitions chez les propriétaires avec autorisation, audit, CAS et idempotence ; ne pas assimiler les structures mémoire à leur traitement.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 66 du texte conservé.
  - Prérequis immédiat : Tâche 2.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL05 — Implémenter purge autorisée et tombstones durables avec propagation aux dérivés présents.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation future », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 36 du texte conservé.
  - Références à recouper et critère propre au raccord : R-02/R-04/R-05/R-07 ; CP-01/CP-03 à CP-07 : qualifier purge propriétaire par Job, tombstones, rétention/holds et propagation aux dérivés présents, sans publication avant commit ni double effet.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 67 du texte conservé.
  - Prérequis immédiat : Tâche 2.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL06 — Tester hold/rétention, dérogation Super Admin, rejou, fuite de données non classifiées et restauration sans résurrection avec C16.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation future », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 37 du texte conservé.
  - Références à recouper et critère propre au raccord : R-01 à R-08 ; CP-01 à CP-08 : consolider les preuves de chaque raccord nécessaire, y compris G01–G03 du raccord initial et restauration C16/N05, sans remplacer les contrôles locaux de chaque réalisation.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 68 du texte conservé.
  - Prérequis immédiat : Tâche 2.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL07 — Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture futures », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 38 du texte conservé.
  - Références à recouper et critère propre au raccord : Contrôles configurés applicables au périmètre final, en complément des preuves obtenues pour chaque unité ; aucun test produit exécuté par la présente réconciliation.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 69 du texte conservé.
  - Prérequis immédiat : Tâche 2.4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL08 — Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture futures », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 39 du texte conservé.
  - Références à recouper et critère propre au raccord : Revue bidirectionnelle R-01 à R-08 / CP-01 à CP-08 / preuves de tâches, avec isolement, refus, dérogations, absence de secret et non-applicabilités motivées.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 70 du texte conservé.
  - Prérequis immédiat : Tâche 3.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL09 — Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture futures », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 40 du texte conservé.
  - Références à recouper et critère propre au raccord : Examiner fichiers, périmètre, impacts, liens, empreintes et preuves affectées ; conserver les changements préexistants et les limites de livraison.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 71 du texte conservé.
  - Prérequis immédiat : Tâche 3.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C10-SL10 — N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et clôture futures », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Raccordement documentaire du 26 octobre 2026 », ligne 41 du texte conservé.
  - Références à recouper et critère propre au raccord : Opérations finales uniquement après les preuves et autorisations nécessaires ; la validation documentaire actuelle n'autorise aucun archivage ni opération Git.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 72 du texte conservé.
  - Prérequis immédiat : Tâche 3.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
