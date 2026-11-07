# Tâches — PA02

Toutes les tâches sont une réalisation future non lancée. L’autorisation actuelle est limitée à la préparation documentaire ; aucune coche n’est anticipée.

- [x] 1. Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.
- [ ] 2. Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.
- [ ] 3. Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.
- [ ] 4. Définir les contrats, schémas, propriétaires et adapters du périmètre : Identité, références de secrets, ancrages et relations PBO–PA ; plusieurs autorités sans conflit résolu par dernière écriture ; provisionnement distinct du contrôle continu.
- [ ] 5. Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.
- [ ] 6. Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.
- [ ] 7. Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.
- [ ] 8. Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.
- [ ] 9. Vérifier la sortie attendue : Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale.
- [ ] 10. Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Identité, références de secrets, ancrages et relations PBO–PA ; plusieurs autorités sans conflit résolu par dernière écriture ; provisionnement distinct du contrôle continu.
- Résultat de référence : Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale.
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
| 9 | Tâche 8 techniquement validée avec ses propres preuves | Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale. | Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif. |
| 10 | Tâche 9 techniquement validée avec ses propres preuves | Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte. | Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

### Incidence du parcours C08 adopté

Le [parcours C08](../add-installation-and-first-configuration/proposal.md) impose la sélection explicite de PA système et PZT local pour préparer PostgreSQL et initier sa première connexion technique. Le réseau distant et les sessions utilisateur PA ne sont pas activés par ce choix. Dans Docker Pixs, le logiciel PostgreSQL est fourni sans données/cluster/secret dans les couches ; le profil conserve les données persistantes et un propriétaire de préparation admissible unique. L’image contient deux binaires PA système/événements et PZT indépendant, sans binaire utilisateur. Le paquet PA reste distinct du paquet PBO/PFO ; sélectionner l’exécutant ne l’incorpore pas à PBO.

Les qualifications de l’ancien profil sans ces exécutants ne prouvent pas le parcours révisé. Les tests locaux de chaque tâche concernée et la recette finale doivent recouper C08 P01–P10, la politique native pré-base, les secrets et l’audit indépendants, les droits ordinaires après PostgreSQL, la reprise et les budgets réellement accordés. Aucun acteur technique ne réalise l’acte métier R01 ; tous échanges PBO–PA restent via PZT. Le mécanisme de secrets Docker et ses versions/paramètres restent à qualifier, sans équivalence systemd supposée.


## Addendum RSMP — fermeture documentaire restante

Acquis : validation humaine D1A, D2A, D3A. Reste à fermer : détail des contrats sémantiques, champs obligatoires ou conditionnels selon profil, propriétaires, préconditions et refus, sans réécrire numéros ni cocher cases.

Tâche 3 distingue acquis adoptés et fermeture du détail restant avant toute unité codable. Aucune tâche cochée, aucun contrôle présenté comme réussi.

Critères documentaires : cohérence des trois nouveaux documents avec requirements.md recalé et canon courant ; liens relatifs valides ; UTF-8 avec fins de ligne LF ; textes normatifs inchangés ; refus à prévoir nommés par comportement (ancrage absent ou substitué, candidat forgé, approbation autre cible ou octets modifiés, référence de secret non résoluble, expiration ou révocation courante périmée, exposition vers autre relation refusée, restauration obsolète, concurrence, panne et reprise, issue inconnue) ; méthodes par revue documentaire et cas nominaux ou refus du profil ; tous non exécutés.


## Première unité pure — critères — addendum 2026-10-26

Cet addendum précise les critères de la première unité, à effectuer après autorisation. Les dix cases et leurs numéros restent inchangés et aucune case n'est cochée ici. requirements.md est inchangé.

La première unité construit le codec fermé décrit dans contracts.md et ses tests nominaux, de refus et hostiles, avec le diagnostic unique et la matrice aux limites. Aucun test n'est présenté comme passé.

Les contrôles attendus utilisent la bibliothèque standard unittest et l'interpréteur DevOps, sans pytest ni installation : PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m py_compile src/pixs/pa_native/provisioning_contracts.py puis PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p test_pa_provisioning_contracts.py.

Les tests restent non exécutés à ce stade et seront exécutés seulement après autorisation, sur preuves observées.

## Addendum RSMP critères phase fournisseur — A ADOPTÉ, sans coche
Choix A ADOPTÉ le 2026-10-26 ; B non retenu. Principes A ADOPTÉS ; NFDOC, code et qualification restant à réaliser sous revue Codex normale. Dix tâches et numéros conservés, aucune tâche ajoutée, aucune case cochée. Tâche 3 distingue acquis D1A D2A D3A et fermeture fournisseur restant. Tâches 4 à 6 exigeront suite recette nominale refus concurrence crash réouverture sur état durable, simulations distinctes producteurs réels, chemins tests dans racine projet, sans hôte TPM système. Tâches 7 à 10 consolideront sans rejouer preuves valides. Critère documentaire : cohérence 5 docs avec requirements inchangé et canon, liens valides, UTF-8 LF, refus nommés, méthodes revue non exécutées.

## Preuves audit T1 — 2026-10-26
Inventaire: requirements 3 blocs/3 scenarios, specs pixs-agent et pzt lus, existant agent/contracts/identifiers/service/adapter, pzt/contracts/ports, pa_native/postgresql/provisioning_contracts/provisioning_bindings. Ecarts: aucun port/admission/stockage PA02 livre qualifie; verificateurs/proofs/fencing et UTC/Z12 non consommables pour global; provider A non qualifie; Context8 DTO prouves, garanties reelles manquantes; PG non requis initial local. Codecc44/comparateur28 et 5 docs A conservees.


## Bilan de dépendances

[Bilan de dépendances](./BLOCKERS.md)

Résumé : 44 tests codec + 28 tests comparateur + 30 tests backend IO = 102 méthodes distinctes en 3 suites séparées. Preuves locales seules, sans qualification produit, admission, PZT, PG global, UTC ou transport. Dix numéros et coches inchangés, T1 seule cochée.
[Statistiques cumulées du change](./STATISTICS.md)


## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md), [contracts.md](contracts.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future » ; « Preuves audit T1 — 2026-10-26 » ; « Bilan de dépendances ».

### PA02-SL01 — Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — PA02 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 34 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues.
  - Contrôles exigés dans cette tâche et preuve : Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL02 — Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — PA02 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 35 du texte conservé.
  - Prérequis immédiat : Tâche 1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite.
  - Contrôles exigés dans cette tâche et preuve : Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL03 — Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — PA02 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 36 du texte conservé.
  - Prérequis immédiat : Tâche 2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse.
  - Contrôles exigés dans cette tâche et preuve : Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL04 — Définir les contrats, schémas, propriétaires et adapters du périmètre : Identité, références de secrets, ancrages et relations PBO–PA ; plusieurs autorités sans conflit résolu par dernière écriture ; provisionnement distinct du contrôle continu.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — PA02 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 37 du texte conservé.
  - Prérequis immédiat : Tâche 3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites.
  - Contrôles exigés dans cette tâche et preuve : Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL05 — Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — PA02 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 38 du texte conservé.
  - Prérequis immédiat : Tâche 4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu.
  - Contrôles exigés dans cette tâche et preuve : Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL06 — Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — PA02 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 39 du texte conservé.
  - Prérequis immédiat : Tâche 5 techniquement validée avec ses propres preuves
  - Critère observable de validation : Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré.
  - Contrôles exigés dans cette tâche et preuve : Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL07 — Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — PA02 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 40 du texte conservé.
  - Prérequis immédiat : Tâche 6 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible.
  - Contrôles exigés dans cette tâche et preuve : Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL08 — Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

- Ancien repère et tâche rattachée : tâche 8 ; section « Tâches — PA02 », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 41 du texte conservé.
  - Prérequis immédiat : Tâche 7 techniquement validée avec ses propres preuves
  - Critère observable de validation : Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL09 — Vérifier la sortie attendue : Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale.

- Ancien repère et tâche rattachée : tâche 9 ; section « Tâches — PA02 », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 42 du texte conservé.
  - Prérequis immédiat : Tâche 8 techniquement validée avec ses propres preuves
  - Critère observable de validation : Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale.
  - Contrôles exigés dans cette tâche et preuve : Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA02-SL10 — Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

- Ancien repère et tâche rattachée : tâche 10 ; section « Tâches — PA02 », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 43 du texte conservé.
  - Prérequis immédiat : Tâche 9 techniquement validée avec ses propres preuves
  - Critère observable de validation : Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte.
  - Contrôles exigés dans cette tâche et preuve : Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
