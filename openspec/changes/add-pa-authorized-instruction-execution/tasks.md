# Tâches — PA04

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Maintien ciblé des unités — ACL-PIXS-2026-10-31-E3-R1

Périmètre courant : Instructions et mandats contextualisés, opérations multi-rôles, revalidation, résultats observés et reprise sans double effet.

Les tâches, libellés, cases et sous-lots existants sont conservés. Lorsque leur texte mentionne une orientation remplacée, il reste un repère historique ; la réalisation future suit la cible courante indiquée ci-dessus et ses scénarios. Une ancienne case cochée n'est pas une validation de cette nouvelle version. Chaque unité future vérifie ses contrats, nominal/refus, persistance, autorisation et reprise nécessaires avant sa propre validation ; aucun test produit n'est exécuté par ce maintien.

Sources : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md).

| Unité existante | Correspondance | Critères à relier lors de la réalisation future |
|---|---|---|
| PA04-SL01 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL02 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL03 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL04 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL05 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL06 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL07 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL08 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL09 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |
| PA04-SL10 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA04, sans nouvelle qualification de la case historique |

La liste ci-dessus n'est pas une nouvelle séquence : les anciens rattachements aux tâches et alias restent ceux des sections conservées. Aucun identifiant n'est attribué à une unité historique absente ou ambiguë.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

L’audit documentaire de la tâche 1 est achevé sur preuves citées ; les tâches 2-10 restent non validées et sans qualification produit. Unité locale réalisée : doc locale contracts.md + module Agent/PBO pa04_service_catalog.py + tests (structure locale seule, catalogue fermé cinq noms, bornes UTF-8, profil explicite ; aucun effet OS/transport/preuve mandat/currentness/trust/déduplication/durabilité ; non importé par PA natif, service.py/ports.py/repository inchangés). Syntaxe 2×exit0, 32 tests locaux exit0 (13 nouveaux + 19 régression). Tâches 2-10 toujours ouvertes, validation locale ne vaut pas native/trust/PZT/effet.

- [x] 1. Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.
- [ ] 2. Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.
- [ ] 3. Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.
- [ ] 4. Définir les contrats, schémas, propriétaires et adapters du périmètre : Contrats publics des instructions, fraîcheur, scopes, idempotence, revalidation, compensation préautorisée et réconciliation après résultat incertain ; aucun code distant implicite.
- [ ] 5. Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.
- [ ] 6. Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.
- [ ] 7. Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.
- [ ] 8. Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.
- [ ] 9. Vérifier la sortie attendue : Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.
- [ ] 10. Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Contrats publics des instructions, fraîcheur, scopes, idempotence, revalidation, compensation préautorisée et réconciliation après résultat incertain ; aucun code distant implicite.
- Résultat de référence : Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.
- Cas de contrôle du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues. | Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts. |
| 2 | Tâche 1 techniquement validée avec ses propres preuves | Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite. | Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet. |
| 3 | Tâche 2 techniquement validée avec ses propres preuves | Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse. | Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code. |
| 4 | Tâche 3 techniquement validée avec ses propres preuves | Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites. | Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve. |
| 5 | Tâche 4 techniquement validée avec ses propres preuves | Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu. | Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici. |
| 6 | Tâche 5 techniquement validée avec ses propres preuves | Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré. | Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante. |
| 7 | Tâche 6 techniquement validée avec ses propres preuves | Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible. | Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux. |
| 8 | Tâche 7 techniquement validée avec ses propres preuves | Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation. | Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément. |
| 9 | Tâche 8 techniquement validée avec ses propres preuves | Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés. | Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif. |
| 10 | Tâche 9 techniquement validée avec ses propres preuves | Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte. | Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Rattachement 1A-2B-3A aux tâches 1-4 restant ouvertes

La décision humaine valide la portée fonctionnelle, elle ne prouve ni tâche 2 ni tâche 3 complètes. Aucune coche, aucun test produit exécuté.

Tâche 1 : compléter inventaire exigences et existant réel, sans affirmer d'absence depuis sources incomplètes. Tâche 2 : consigner sélection 1A et dépendances PA03 et PZT exigibles selon chemin réel. Tâche 3 : consigner barrières restantes et refus du premier lot, sessions utilisateur différées sans obligation supprimée. Tâche 4 : identifiants API, schémas, paramètres, effets, postconditions, durabilité et budgets du seul objet 2B à fermer ultérieurement, sans valeur ni opération inventée.

Ordre par unité : réaliser, tester, corriger, retester, valider, puis cocher sur preuves exactes. Ensuite validation globale finale avant archivage. Réduction éventuelle de périmètre exige delta documentaire validé.

## Lien tâches 3-4 vers delta et contrats proposés

Tâches 1-4 restant ouvertes, aucune coche. Tâche 3 : revoir delta et refus du profil 1A-2B-3A. Tâche 4 : fermer schémas, propriétaires et preuves du seul objet 2B à partir des textes proposés. Validation documentaire distincte requise avant toute écriture suivante.

Note d’audit 1 : 23 sources, six blocs recoupés, complément PA04 identifié, validation OpenSpec stricte exit0 après correction longueur, sans produit ni transport. Differences depuis audit documentees : generator ajout controle bootstrap_resource_profile, annexe PA03 precisee, sans changer constat catalogue PG ni absence chemin PZT. Mentions 1-4 ouvertes ci-dessus historiques de preparation. Unite locale suivante examinee par CGPT, non ecrite ni testee.

[Bilan des dépendances et conditions de reprise](./BLOCKERS.md)

[Statistiques du change](./STATISTICS.md)

Note 2026-10-30T04:44:35.230Z : revalidation sans coche — 1/10 conservé, 2-10 TOUJOURS BLOQUÉ confirmés, voir BLOCKERS ; STATISTICS couvre le suivi cumulé depuis le début du change ; archivage en attente.

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md), [contracts.md](contracts.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future ».

### PA04-SL01 — Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — PA04 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 34 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues.
  - Contrôles exigés dans cette tâche et preuve : Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL02 — Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — PA04 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 35 du texte conservé.
  - Prérequis immédiat : Tâche 1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite.
  - Contrôles exigés dans cette tâche et preuve : Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL03 — Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — PA04 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 36 du texte conservé.
  - Prérequis immédiat : Tâche 2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse.
  - Contrôles exigés dans cette tâche et preuve : Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL04 — Définir les contrats, schémas, propriétaires et adapters du périmètre : Contrats publics des instructions, fraîcheur, scopes, idempotence, revalidation, compensation préautorisée et réconciliation après résultat incertain ; aucun code distant implicite.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — PA04 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 37 du texte conservé.
  - Prérequis immédiat : Tâche 3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites.
  - Contrôles exigés dans cette tâche et preuve : Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL05 — Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — PA04 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 38 du texte conservé.
  - Prérequis immédiat : Tâche 4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu.
  - Contrôles exigés dans cette tâche et preuve : Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL06 — Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — PA04 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 39 du texte conservé.
  - Prérequis immédiat : Tâche 5 techniquement validée avec ses propres preuves
  - Critère observable de validation : Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré.
  - Contrôles exigés dans cette tâche et preuve : Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL07 — Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — PA04 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 40 du texte conservé.
  - Prérequis immédiat : Tâche 6 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible.
  - Contrôles exigés dans cette tâche et preuve : Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL08 — Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

- Ancien repère et tâche rattachée : tâche 8 ; section « Tâches — PA04 », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 41 du texte conservé.
  - Prérequis immédiat : Tâche 7 techniquement validée avec ses propres preuves
  - Critère observable de validation : Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL09 — Vérifier la sortie attendue : Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.

- Ancien repère et tâche rattachée : tâche 9 ; section « Tâches — PA04 », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 42 du texte conservé.
  - Prérequis immédiat : Tâche 8 techniquement validée avec ses propres preuves
  - Critère observable de validation : Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.
  - Contrôles exigés dans cette tâche et preuve : Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA04-SL10 — Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

- Ancien repère et tâche rattachée : tâche 10 ; section « Tâches — PA04 », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 43 du texte conservé.
  - Prérequis immédiat : Tâche 9 techniquement validée avec ses propres preuves
  - Critère observable de validation : Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte.
  - Contrôles exigés dans cette tâche et preuve : Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
