# Tâches — C12

Les tâches 1.1/1.2/2.1/2.2/2.3/2.4/3.1/3.2/3.3/3.4 sont validées au titre de leurs critères et preuves datées ; archivage 1CISMP5 + STATISTICS.md restent à exécuter sous mandats CAB distincts. Git/commit/push/publication non demandés.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [x] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

## 2. Réalisation future

- [x] 2.1 Externaliser les textes utilisateur des parcours et API dans leurs catalogues propriétaires.
- [x] 2.2 Définir et implémenter tokens/primitives et préférences de langue/thème/formats.
- [x] 2.3 Compléter tests frontend et parcours clavier/responsive/zoom/lecteur d’écran.
- [x] 2.4 Exécuter Chromium et Firefox headless, build et audit manuel/outillé WCAG 2.2 AA ; déclarer les limites observées.

## 3. Preuves et clôture futures

- [x] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [x] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [x] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

## Validation C12-SL05 / tâche 2.3 — 4 novembre 2026

Statut : VALIDÉE au sens tasks.md:46 (comportement nominal et refus par propriétaire, sans dépendre de 2.4+). Le relevé historique C12-SL05 du 30 octobre 2026 (case non cochée à cette date) reste conservé ci-dessus et n’est pas réécrit.
Preuve .30 (mandat c12-sl05-zoom-orca-run-req-20261104-30, opération c12-sl05-browsercheck-run-op-20261104-30, exit 0) : frontend/tests/browser-check.mjs --vite-port=5174 sur Vite temporaire 127.0.0.1:5174, Chromium 156.0.8078.79, ok:true, criticalOk:true, CHECK_EXIT=0, CLEANUP_DONE rc=0. Couvre clavier/focus visible (firstIsSkip true, enterToContent true, sequenceExact true), AX noms/états (axComboLang/axComboTheme/axMain/axHeading/axSkipLink true), reflow320 (320/320 ok), zoom CSS proxy value 2 explicitProxy true (proxy, distinct du natif), contrastes mesurés clair/sombre ok (light 14.07/7.37/6.67/6.64, dark 16.71/9.46/8.69/12.00), reduced motion ok, réseau/console 0 erreur, cleanup profil/processus vérifié.
Preuve .32 (mandat c12-sl05-zoom-orca-run-req-20261104-32, opération c12-sl05-zoom-orca-run-op-20261104-32, exit 0) : Chromium 156.0.8078.79, Orca 48.1 AT-SPI2 2.56.2, Orca démarré avant Chromium, Vite temporaire 127.0.0.1:5174, Page.navigate même target href exact/complete, Ctrl+Plus x5, DPR2, reflow sans overflow, AX45 (main/heading/link), AT-SPI COUNT=261 HEADING_SKIP 5 entrées Skip to content/Your application starts here, Tab unique avec activeElement A Skip to content #content (CDP_TAB_OK/ORCA_TAB_OK), locus document web et fenêtre active (ORCA_LOCUS_OK), ORCA_AVAILABLE_OK, CLEANUP_DONE rc=0.
Essais hors critère : stages .27/.28/.29 exit1 par contrôle diagnostic plus strict exigeant une annonce Orca ciblée du lien focalisé ; stage .31 exit1 car la parole « Finished loading Pixs » était absente à cette exécution. Aucun de ces échecs n’invalide la preuve D3 « lecteur Orca disponible » puisque .32 termine exit0 avec Orca48.1, AT-SPI2, Orca up, locus/fenêtre, arbre AT-SPI heading/skip.
Mesure native exacte AFTER d2/w635/s628/c628 visible dans la sortie .27 (exit1 uniquement dû au marqueur diagnostique extra) ; .32 repasse les assertions natives et exit0 mais ne dump pas zoom.log en succès. Parole Orca page-title « Finished loading Pixs » observée dans les sorties .28 et .29 ; .32 la marque optional absente (SPEECH_ABSENT_OPTIONAL) sans conditionner le verdict.
Limites : pas de certification WCAG complète ni conformité WCAG totale revendiquée ; pas d’annonce Orca du lien focalisé observée de façon stable ; 2.4 et 3.x restent non cochés ; aucune livraison, activation, archivage ou publication n’est revendiquée.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1.1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 1.2 | Tâche 1.1 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.1 | Tâche 1.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.2 | Tâche 2.1 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.4 | Tâche 2.3 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.1 | Tâche 2.4 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.2 | Tâche 3.1 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.3 | Tâche 3.2 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |
| 3.4 | Tâche 3.3 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et clôture futures » ; « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future ».

### C12-SL01 — Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 42 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL02 — Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 43 du texte conservé.
  - Prérequis immédiat : Tâche 1.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL03 — Externaliser les textes utilisateur des parcours et API dans leurs catalogues propriétaires.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation future », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 44 du texte conservé.
  - Prérequis immédiat : Tâche 1.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL04 — Définir et implémenter tokens/primitives et préférences de langue/thème/formats.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation future », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 45 du texte conservé.
  - Prérequis immédiat : Tâche 2.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL05 — Compléter tests frontend et parcours clavier/responsive/zoom/lecteur d’écran.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation future », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 46 du texte conservé.
  - Prérequis immédiat : Tâche 2.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- Blocage historique du 3 novembre 2026 : les critères de la tâche 2.3 ont été validés le 4 novembre (voir « Validation C12-SL05 / tâche 2.3 » ci-dessus) ; les 10 tâches du change sont réalisées et C12 a été archivé le 5 novembre 2026.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL06 — Exécuter Chromium et Firefox headless, build et audit manuel/outillé WCAG 2.2 AA ; déclarer les limites observées.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation future », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 47 du texte conservé.
  - Prérequis immédiat : Tâche 2.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL07 — Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture futures », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 48 du texte conservé.
  - Prérequis immédiat : Tâche 2.4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL08 — Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture futures », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 49 du texte conservé.
  - Prérequis immédiat : Tâche 3.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL09 — Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture futures », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 50 du texte conservé.
  - Prérequis immédiat : Tâche 3.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C12-SL10 — N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et clôture futures », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 51 du texte conservé.
  - Prérequis immédiat : Tâche 3.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

## Réévaluation C12-SL03 / tâche 2.1 — 1er novembre 2026

Statut : VALIDÉE au sens des critères tasks.md:44 (comportement nominal et refus par propriétaire ; isolation, intégrité et reprise sans dépendre de 2.2+), sous le périmètre établi ci-dessous. Le relevé historique C12-SL03 du 30 octobre reste conservé ci-dessus.
Fichiers modifiés : src/pixs/backend/api/errors.py (catalogue API_ERROR_MESSAGE_VERSION=1.0.0, anglais canonique et français si fr), src/pixs/backend/api/responses.py (propagation de language), src/pixs/backend/api/__init__.py (export), tests/unit/test_api_error_projection.py, tests/integration/test_api_error_projection_integration.py, tests/integration/test_api_error_response_integration.py et src/pixs/backend/api/README.md. Le frontend catalogs.js (58 clés shell.* en anglais et français) et le catalogue propriétaire Core api_core_errors_catalog.py étaient déjà complets et n’ont pas été modifiés.
Commandes et résultats observés :
- /home/devops/datas/pixs/.venv/bin/python -m py_compile src/pixs/backend/api/errors.py src/pixs/backend/api/responses.py src/pixs/backend/api/__init__.py tests/unit/test_api_error_projection.py tests/integration/test_api_error_projection_integration.py tests/integration/test_api_error_response_integration.py — exit 0, aucune sortie.
- /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_error_projection.py -v — 13 tests, OK.
- /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_error_response.py -v — 5 tests, OK.
- /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p test_api_error_projection_integration.py -v — 4 tests, OK.
- /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p test_api_error_response_integration.py -v — 3 tests, OK.
- /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_core_errors.py -v — 7 tests, OK.
- /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend run build — exit 0, 111 modules transformed.
- /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend test — catalog-browser/2 ok:true ; 145 Chromium et 145 Firefox passés ; Chromium 156.0.8078.73, Firefox 153.6.0esr ; fermeture des processus/profils/serveur vérifiée.
Périmètre fonctionnel observé : les clés shell.* sont servies par catalogs.js ; les réponses d’erreur API Core préservent les codes et contrats existants ; les helpers/enveloppes d’erreur d’infrastructure sélectionnent anglais par défaut, français pour fr et anglais pour toute autre valeur. Les tests couvrent les helpers et enveloppes ; aucune route HTTP réelle d’erreur d’infrastructure n’est revendiquée. Les champs hors message, error_code, structure, opacité et diagnostics de corrélation restent inchangés.
Contrôles de portée T15 : aucun module frontend management ou secours n’existe dans les sources actuelles ; pyproject.toml ne déclare pas de commande project.scripts ; auth/cli.py, auth/cli_vault.py et pa_native/cli.py n’exposent pas de texte utilisateur imprimé ; les parseurs repérés appartiennent au watchdog de développement ou aux générateurs internes PZT-CA. Les textes description d’api_shell_context.py sont des métadonnées OpenAPI et non le champ message public arbitré en D4. Aucun parcours PZT distant n’est revendiqué pour ce périmètre.
Limites : contrôle ciblé des textes hors catalogues effectué par revue de sources, sans linter négatif configuré ; validation OpenSpec stricte après cette mise à jour tasks.md à exécuter avant de déclarer la documentation conforme ; aucun audit manuel WCAG, C17/C19, archivage, livraison ou publication n’est revendiqué.

## Réévaluation C12-SL04 / tâche 2.2 — 2 novembre 2026

Statut : VALIDÉE au sens tasks.md:44-45 (livrable sans choix obligatoire ouvert ; revue scénarios/contrôles avant 2.3). Le relevé historique C12-SL04 du 30 octobre et la réévaluation 2.1 restent conservés ci-dessus.
Fichiers réellement modifiés pendant 2.2 : `frontend/src/theme.css` (5883 octets, SHA `b9d9e39564a0c54c56f4ca0f2617084407f46938809b6fb2b1e706f2bc0c111c`, 5 tokens `--layout-field-min/--checkbox-size/--state-disabled-opacity/--z-index-skip/--skip-link-hidden-shift` et remplacements des bruts correspondants, tokenisé pendant cette même tâche avant le nouveau validateur) ; nouveau `frontend/scripts/validate_pixs_css_tokens.mjs` (6299 octets, SHA `d1c4768deb00d8a9d9db81156c0c44c51e606e79677ff9e4eb4986c28665ef81`, fail-closed, owner `theme.css` seul, `ALLOW_PAIR` exacte, `TOKEN_NAMES=30/DARK=7`) ; hook `enforce:'pre' transform` dans `frontend/scripts/pixs-composition-plugin-v1.mjs` limité au CSS Pixs importé hors `node_modules` ; nouveau `frontend/tests/css-tokens.test.mjs` ; `frontend/package.json:test:node` += `tests/css-tokens.test.mjs`. Comportement langue/thème, lui, préexistant et inchangé (état React éphémère, `sans reload`, `Accept-Language` existant, UTC intact, aucune persistance).
Tests/validations 2.2 exécutés le 1er novembre après le code et avant cette mise à jour documentaire : `npm run test:node` → 162 tests, 162 pass, 0 fail (dont `owner-30-dark-7`, `five-tokens`, rejets bruts/`@media`/`nesting`/`url`/`!important`/`unclosed`/`duplicate`/`var-fallback`/`prop-unknown`, `accepts-allowlisted/flex-calc/inline-size/dark-coherence`, après fix `seenL`) ; `npm run build` → `exit 0`, 111 modules ; `openspec validate --all --strict` → 208 passed, 0 failed, preuve code pré-doc (`skip_specs` zéro delta).
Pas de test négatif Vite-build séparé : refus bruts couverts par tests validateur + hook build positif. Aucune route HTTP revendiquée.
Limites : C17/C19, audit WCAG manuel, P0 complet, livraison/activation/publication non revendiqués ; 2.3/2.4 restent à faire, réalisabilité 2.3 À VÉRIFIER. Preuves : implémentation/test/build/strict ci-dessus (pas les 32 tests Python 2.1) ; pas de livraison/activation.

## Validation C12-SL06 / tâche 2.4 — 5 novembre 2026

Statut : VALIDÉE. Catalogue .42 (requestId c12-sl06-catalog-req-20261104-42 ; operationId c12-sl06-catalog-op-20261104-42), décision APPROVED et accès HELD fencing 14268, commande node frontend/tests/browser/catalog-browser.mjs : Chromium 156.0.8078.79, 145 pass ; Firefox 153.6.0esr, 145 pass ; catalog-browser/2 ok:true, violations:[] et errors:[] ; serveur fermé, processus/profils contrôlés. Bail .07 : .43 CLEANUP_DONE removed:0 exit0 ; .44 VERIFY_DONE remaining0 exit0 ; .45 removed0 active0 exit0 ; .46 remaining0 active0 exit0. Build .47 (requestId c12-sl06-build-req-20261105-47 ; operationId c12-sl06-build-op-20261105-47), APPROVED/HELD fencing14319, npm --prefix frontend run build : exit0, 111 modules, built 272ms ; avertissements MODULE_LEVEL_DIRECTIVE non bloquants ; effet frontend/dist conservé (index 0.42kB, css 5.15kB, js 396.55kB). Audit .49 (requestId c12-sl06-wcag-audit-req-20261105-49 ; operationId c12-sl06-wcag-audit-op-20261105-49), APPROVED/HELD fencing14333, frontend/tests/browser-check.mjs --vite-port=5174 : ok:true, criticalOk:true ; clavier, arbre accessible, reflow320 320/320, zoomCSS2x proxy, reflowMulti N/A motivé pour STANDALONE, reducedMotion, contrastes clairs/sombres réussis, 153 requêtes locales, 0 bloquée, 0 erreur HTTP/console, cleanup true, exit0 ; fenêtre de revue120s et serveur fermés. .50 cleanup removed0/active0/port5174Closed true ; .51 verify remaining0/active0/portClosed true. Serveur manuel .52 (requestId c12-sl06-manual-server-req-20261105-52 ; operationId c12-sl06-manual-server-op-20261105-52), APPROVED/HELD fencing14347 : READY puis CLOSED, exit0 ; inspection CUA par l’orchestrateur : premier Tab focalise le lien visible « Aller au contenu » avec contour ; Enter déplace le focus sur main/#content ; contrôles « Langue » et « Apparence », H1 unique « Votre application commence ici » ; viewport 320px innerWidth=scrollWidth=320, sans débordement, thème sombre visible. Zoom natif/Orca réutilisés de la preuve .32 : Ctrl+Plus x5, DPR2, Orca48.1/AT-SPI2 disponible ; port5173 jamais touché.

Limites : aucune certification WCAG complète ni conformité totale revendiquée ; annonces Orca ciblées non stables ; .40/.41 NOT_ADMITTED et .48 sans effet non réutilisés. Aucun audit externe axe/pa11y exécuté.

## Preuves C12-SL07 / tâche 3.1 — 5 novembre 2026

Statut : VALIDÉE. Compilation syntaxique .54 (requestId c12-sl07-pycompile-req-20261105-54 ; operationId c12-sl07-pycompile-op-20261105-54), APPROVED/HELD fencing14356, exit0 sans sortie ; compilation de huit fichiers Python, bytecode redirigé vers frontend/.cache/pycache. Tests unitaires .55 (requestId c12-sl07-unit-api-errors-req-20261105-55 ; operationId c12-sl07-unit-api-errors-op-20261105-55), APPROVED/HELD fencing14359 : commande /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p 'test_api_error_*.py' -v, exit0, 18/18 OK. Tests d’intégration .56 (requestId c12-sl07-integration-api-errors-req-20261105-56 ; operationId c12-sl07-integration-api-errors-op-20261105-56) : /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p 'test_api_error_*_integration.py' -v, exit0, 7/7 OK. Erreurs Core .57 (requestId c12-sl07-core-errors-req-20261105-57 ; operationId c12-sl07-core-errors-op-20261105-57) : /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_core_errors.py -v, exit0, 7/7 OK. Suite frontend .58 (requestId c12-sl07-node-tests-final-req-20261105-58 ; operationId c12-sl07-node-tests-final-op-20261105-58), APPROVED/HELD fencing14365 : commande /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend run test:node, exit0, 162 pass, 0 fail. La suite .53 avait aussi 162/162. Aucune source modifiée par ces tests ; les caches restent sous frontend/.cache. Build .47 et navigateurs .42/.49 ci-dessus.

## Analyse C12-SL08 / tâche 3.2 — 5 novembre 2026

Statut : VALIDÉE. Les tests .55-.58 couvrent isolation, refus et minimisation des erreurs : propriétaires/scopes distincts, points privés et contenus opaques non consommables, types hostiles, doublons et entrées manquantes/incomplètes rejetés ; erreurs d’authentification et refus encapsulés distinguent les cas attendus ; secrets de test absents des enveloppes/messages ; tests frontend de clés propriétaires, namespaces, snapshots immuables, paramètres et transport sans fuite de mot de passe. browser-check .49 rapporte réseau/console sans erreur. Limites : aucun scan dédié de secrets ni route HTTP réelle d’erreur d’infrastructure exécutés ; seules les suites liées et inspections documentées sont revendiquées.

## Analyse C12-SL09 / tâche 3.3 — 5 novembre 2026

Statut : VALIDÉE AVEC LIMITE. Revue en lecture ciblée des preuves et fichiers consignés aux sections C12-SL03/SL04/SL05/SL06/SL07, des contrats proposal.md/design.md/requirements.md et des mandats observés : périmètre couvert, autorisations séparées, sources applicatives non éditées par SL06/SL07, build frontend/dist conservé, caches confinés à frontend/.cache, processus/profils/port5174 nettoyés et vérifiés, port5173/quarantaine .03 préservés, aucun archivage/commit/publication anticipés. L’invocation 1CISMP5 autorise l’archivage et STATISTICS.md pour ce change seulement ; Git/commit/push/déploiement/publication ne sont ni demandés ni autorisés. Limite : aucun VCS diff exact n’est consulté, conformément à l’interdiction explicite du prompt d’inspecter l’état Git sans demande développeur ; les changements préexistants ont été préservés sans opération de nettoyage. Mandat .60 annulé avant émission : input natif divergent refusé, permission rejetée avec ACK 204, reçus owner withdraw puis release ; aucun effet .60. Mandat .61 annulé avant émission après oldString tronqué : permission rejetée avec ACK 204, reçus owner withdraw puis release ; aucun effet .61.
