# Tâches — C10

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
