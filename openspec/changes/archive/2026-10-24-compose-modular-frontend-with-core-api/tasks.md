# Tâches — C11

Ce dossier suit le seul change C11, dont la réalisation est autorisée par le RUN persistant. Les cases historiques conservent leurs preuves datées ; les sources nouvelles, dont les précisions de conception, restent à requalifier. Une source présente ou un contrôle syntaxique ne prouve pas la validation fonctionnelle. L’organisation en deux phases définie plus bas applique la demande explicite du développeur.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [x] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

Revalidation technique de 1.2 le 23 octobre 2026 après réouverture : addendum de conception scopes opaques, transport propriétaire injecté et saisies typées examiné ; design.md UTF-8/LF sans BOM, empreinte SHA-256 9ee4a0d5d62d8b770f1c420dd6ac2b5eefdd2167a8ff61d69755a6f9725658d2. Validation OpenSpec stricte ciblée exit 0, message msg_167a7774e0015Gu22F1uzp89Ff / outil Bash. Aucune réalisation de code ni preuve fonctionnelle nouvelle dans cette tâche de conception ; 2.1 reste rouverte et 2.2 suspendue à sa revalidation.

## 2. Réalisation — validation en seconde phase

- [x] 2.1 Définir façades publiques du shell et pont entre facettes de manifest et build.
- [x] 2.2 Implémenter résolution récursive, collisions et composition de modules/sous-modules.
- [x] 2.3 Brancher session, tenant, API et gestion d’intentions/invalidation autorisée.
- [x] 2.4 Tester module/sous-module sans éditer le shell, import privé, collision, versions et équivalence entre la composition de développement et le bundle C11 effectivement construit et chargé dans un environnement d’intégration isolé ; qualification du paquet Debian conservée en C18/C17/C19.

## 3. Preuves et clôture futures

- [x] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [x] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [x] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

Validation technique finale du 24 octobre 2026 : C11-A01–A11 examinés dans VALIDATION.md. 133 Node,106 Python,75 AST/import/profil,6 raccords réels,145 cas par moteur,16 compilations Python, deux builds et8 chargements MODULE/SUBMODULE PASS dans leurs périmètres distincts. Preuves propriétaires/C14 recoupées et bornées. Après deux modifications Core concurrentes, nouvelles recettes réelles HTTPS/PostgreSQL PASS dans Chromium et Firefox :15 critères et14 HTTP200 par moteur,266 empreintes stables avant/après, nettoyage complet. Preuve native c14_current_core_requalification_native_proof dans le checkpoint.

Clavier Root et primitives réelles, contrastes Light/Dark, reflow320 et mouvements réduits contrôlés. Compte rendu humain explicite A à E OK : Orca48.1/AT-SPI2 2.56.2/GNOME Wayland, navigateur intégré de Codex, dont zoom natif200 %. Version du moteur intégré N/A car non exposée. Aucune source produit modifiée par ces contrôles ; serveurs temporaires fermés.

README.md, frontend/README.md, API README, CHANGELOG.md et design.md relus ; PROJECT.md, TECHNICAL.md et BUILD.md cohérents et inchangés. Les anciennes formulations de réouverture/attente ci-dessous conservent l’historique ; le verdict présent les remplace. Aucun P0/paquet/TLS déployé déduit, aucun Git. 3.4 validée : archive unique C11 du24 octobre2026 réussie, STATISTIQUES.md produit par mandat distinct puis vérifié (six sections, UTF8/LF sans BOM, totaux et sources cohérents). Preuve native msg_16b097f82001KvFfoIUurSg7C2 / prt_16b0985e3001c80Db7yhXUL9Ey. Les reçus de publication et du gate CAB sont conservés dans le checkpoint de clôture ; aucun Git ni déploiement engagé.

Rapport vérifié : STATISTIQUES.md, SHA-256 cb22f6d63d75d8aea2e131710bfca2b63b57760b24f94856c49ed8d6810f5b15. Les éditions de clôture et la publication sont hors de sa borne statistique, ce qui est explicitement consigné dans le rapport. Ce RUN se termine après ce seul change ; les autres RUN et les services partagés sont préservés.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Tester module/sous-module sans éditer le shell, import privé, collision, versions et équivalence entre la composition de développement et le bundle C11 effectivement construit et chargé dans un environnement d’intégration isolé ; qualification du paquet Debian conservée en C18/C17/C19. ; Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1.1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 1.2 | Tâche 1.1 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.1 | Tâche 1.2 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.2 | Tâche 2.1 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.4 | Tâche 2.3 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.1 | Tâche 2.4 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.2 | Tâche 3.1 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.3 | Tâche 3.2 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |
| 3.4 | Tâche 3.3 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Réouverture ciblée du 23 octobre 2026

Les tâches 1.2 et 2.1 sont rouvertes après recoupement des contrats Core/C02, C06 et C14. Les références tenant/scope sont opaques et non contraintes à UUIDv7 ; les identifiants de session Auth conservent leur contrat propriétaire. Le routage public des opérations propriétaires et les saisies booléennes, entières et ordonnées restent à formaliser et recontrôler avant publication du client. Les preuves historiques et les unités de 2.2 sont conservées, mais 2.2 reste non validée et sa poursuite fonctionnelle est suspendue à cette réconciliation. Aucun canon ni contrat Core/C14 n’est modifié par cette reprise.

## Organisation en deux phases — instruction du développeur du 23 octobre 2026

Le développeur demande explicitement de réaliser toutes les tâches de développement avant la phase de tests et de validation. Cette instruction remplace, pour ce seul change C11, l'obligation de valider chaque tâche avant de commencer la réalisation suivante. Les critères, scénarios et preuves exigés restent applicables ; les mandats CAB demeurent unitaires et les tâches ne sont cochées qu'après leur validation effective.

La première phase termine les réalisations 2.1, 2.2 et 2.3, avec les artefacts de recette nécessaires à 2.4. La seconde exécute les contrôles de syntaxe, tests ciblés et globaux, builds et intégrations requis, corrige les écarts puis valide les tâches concernées et les preuves 3.x. L'archivage et STATISTIQUES.md interviennent après ces preuves, pour ce seul change.

Les preuves obtenues avant cette instruction sont conservées avec leurs versions : 1.2 revalidée et cochée ; façades 2.1 réalisées, 33 tests Node et 98 cas dans chacun des deux navigateurs réussis. Elles ne valident pas seules la tâche 2.1 complète et sont requalifiées si leurs sources ou dépendances pertinentes changent. Les cases 2.1 et suivantes restent ouvertes dans l'attente de la seconde phase. Aucun code C14, contrat normatif nouveau ni qualification P0 globale n'est autorisé par cette organisation.


## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Réalisation — validation en seconde phase » ; « 3. Preuves et clôture futures » ; « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future ».

### C11-SL01 — Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 52 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL02 — Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 53 du texte conservé.
  - Prérequis immédiat : Tâche 1.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL03 — Définir façades publiques du shell et pont entre facettes de manifest et build.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation — validation en seconde phase », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 54 du texte conservé.
  - Prérequis immédiat : Tâche 1.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante.
  - Contrôles exigés dans cette tâche et preuve : Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL04 — Implémenter résolution récursive, collisions et composition de modules/sous-modules.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation — validation en seconde phase », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 55 du texte conservé.
  - Prérequis immédiat : Tâche 2.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL05 — Brancher session, tenant, API et gestion d’intentions/invalidation autorisée.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation — validation en seconde phase », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 56 du texte conservé.
  - Prérequis immédiat : Tâche 2.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL06 — Tester module/sous-module sans éditer le shell, import privé, collision, versions et équivalence entre la composition de développement et le bundle C11 effectivement construit et chargé dans un environnement d’intégration isolé ; qualification du paquet Debian conservée en C18/C17/C19.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation — validation en seconde phase », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 57 du texte conservé.
  - Prérequis immédiat : Tâche 2.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL07 — Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture futures », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 58 du texte conservé.
  - Prérequis immédiat : Tâche 2.4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL08 — Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture futures », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 59 du texte conservé.
  - Prérequis immédiat : Tâche 3.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL09 — Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture futures », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 60 du texte conservé.
  - Prérequis immédiat : Tâche 3.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C11-SL10 — N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et clôture futures », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 61 du texte conservé.
  - Prérequis immédiat : Tâche 3.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée.
  - Contrôles exigés dans cette tâche et preuve : Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
