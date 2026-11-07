# Tâches futures — coffre d’exploitation distribué

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Maintien ciblé des unités — ACL-PIXS-2026-10-31-E3-R1

Périmètre courant : Coffre et moyens protégés distincts des clés opérationnelles PKIZT chiffrées en PG ; ne pas déplacer leur autorité ou leur stockage par simple sélection du coffre.

Les tâches, libellés, cases et sous-lots existants sont conservés. Lorsque leur texte mentionne une orientation remplacée, il reste un repère historique ; la réalisation future suit la cible courante indiquée ci-dessus et ses scénarios. Une ancienne case cochée n'est pas une validation de cette nouvelle version. Chaque unité future vérifie ses contrats, nominal/refus, persistance, autorisation et reprise nécessaires avant sa propre validation ; aucun test produit n'est exécuté par ce maintien.

Sources : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md).

| Unité existante | Correspondance | Critères à relier lors de la réalisation future |
|---|---|---|
| O40-SL01 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL02 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL03 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL04 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL05 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL06 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL07 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL08 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL09 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |
| O40-SL10 | Repère et libellé conservés | Cible et scénarios courants du périmètre O40, sans nouvelle qualification de la case historique |

La liste ci-dessus n'est pas une nouvelle séquence : les anciens rattachements aux tâches et alias restent ceux des sections conservées. Aucun identifiant n'est attribué à une unité historique absente ou ambiguë.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Toutes les tâches restent non cochées. La présente préparation ne lance ni implémentation, ni installation de coffre, ni manipulation de secrets.

## 1. Conception de réalisation

- [ ] 1.1 Inventorier les secrets locaux minimaux et ceux d’exploitation ; vérifier l’absence de dépendance circulaire de démarrage et de récupération.
- [ ] 1.2 Faire valider produit/version, identité initiale, droits par service, protection des clés, durées, topologie, résidence et objectifs de reprise, puis le mandat de réalisation.

## 2. Réalisation sous mandat distinct

- [ ] 2.1 Intégrer le provider de coffre choisi au contrat SecretProvider et aux références existantes, sans le rendre obligatoire pour le P0 local.
- [ ] 2.2 Intégrer authentification des workloads, droits minimaux, credentials courts compatibles, renouvellement et révocation avec arrêt contrôlé des copies si requis.
- [ ] 2.3 Intégrer transport vérifié, audit, refus sans repli implicite et procédures protégées de démarrage/sauvegarde/récupération.

## 3. Qualification future

- [ ] 3.1 Tester refus inter-services et inter-périmètres, identité non vérifiable, rotation, expiration et révocation sans prolongation par cache.
- [ ] 3.2 Tester panne réseau/coffre, perte d’instance, reprise et restauration isolée avec état de confiance courant ; mesurer disponibilité et RPO/RTO déclarés.
- [ ] 3.3 Exécuter syntaxe, régressions, OpenSpec et contrôles de non-exposition sur le périmètre réellement implémenté, sans présenter des mocks comme qualification réelle.

## 4. Intégration et clôture futures

- [ ] 4.1 Relier les preuves à la composition distribuée effectivement sélectionnée et à sa recette, sans activer implicitement ce profil ou modifier C01 archivé.
- [ ] 4.2 Examiner le périmètre et les limites ; ne synchroniser, archiver ou publier que sous autorisation ultérieure, avec statistiques si archivage réussi.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Tester refus inter-services et inter-périmètres, identité non vérifiable, rotation, expiration et révocation sans prolongation par cache. ; Tester panne réseau/coffre, perte d’instance, reprise et restauration isolée avec état de confiance courant ; mesurer disponibilité et RPO/RTO déclarés.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1.1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 1.2 | Tâche 1.1 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.1 | Tâche 1.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.2 | Tâche 2.1 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 3.1 | Tâche 2.3 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.2 | Tâche 3.1 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.3 | Tâche 3.2 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 4.1 | Tâche 3.3 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 4.2 | Tâche 4.1 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Qualification future » ; « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future ».

### O40-SL01 — Inventorier les secrets locaux minimaux et ceux d’exploitation ; vérifier l’absence de dépendance circulaire de démarrage et de récupération.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Conception de réalisation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 45 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL02 — Faire valider produit/version, identité initiale, droits par service, protection des clés, durées, topologie, résidence et objectifs de reprise, puis le mandat de réalisation.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Conception de réalisation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 46 du texte conservé.
  - Prérequis immédiat : Tâche 1.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL03 — Intégrer le provider de coffre choisi au contrat SecretProvider et aux références existantes, sans le rendre obligatoire pour le P0 local.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation sous mandat distinct », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 47 du texte conservé.
  - Prérequis immédiat : Tâche 1.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL04 — Intégrer authentification des workloads, droits minimaux, credentials courts compatibles, renouvellement et révocation avec arrêt contrôlé des copies si requis.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation sous mandat distinct », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 48 du texte conservé.
  - Prérequis immédiat : Tâche 2.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL05 — Intégrer transport vérifié, audit, refus sans repli implicite et procédures protégées de démarrage/sauvegarde/récupération.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation sous mandat distinct », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 49 du texte conservé.
  - Prérequis immédiat : Tâche 2.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL06 — Tester refus inter-services et inter-périmètres, identité non vérifiable, rotation, expiration et révocation sans prolongation par cache.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Qualification future », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 50 du texte conservé.
  - Prérequis immédiat : Tâche 2.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL07 — Tester panne réseau/coffre, perte d’instance, reprise et restauration isolée avec état de confiance courant ; mesurer disponibilité et RPO/RTO déclarés.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Qualification future », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 51 du texte conservé.
  - Prérequis immédiat : Tâche 3.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL08 — Exécuter syntaxe, régressions, OpenSpec et contrôles de non-exposition sur le périmètre réellement implémenté, sans présenter des mocks comme qualification réelle.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Qualification future », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 52 du texte conservé.
  - Prérequis immédiat : Tâche 3.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL09 — Relier les preuves à la composition distribuée effectivement sélectionnée et à sa recette, sans activer implicitement ce profil ou modifier C01 archivé.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Intégration et clôture futures », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 53 du texte conservé.
  - Prérequis immédiat : Tâche 3.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O40-SL10 — Examiner le périmètre et les limites ; ne synchroniser, archiver ou publier que sous autorisation ultérieure, avec statistiques si archivage réussi.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Intégration et clôture futures », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 54 du texte conservé.
  - Prérequis immédiat : Tâche 4.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
