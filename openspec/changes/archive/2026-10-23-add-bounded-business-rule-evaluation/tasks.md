# Tâches — O06

Le plan a été établi sans coche pendant la RSMP du 22 octobre 2026. Les coches suivantes correspondent aux validations techniques ultérieures des tâches successives et à leurs preuves dans requirements.md ; aucun test nécessaire n'est reporté à une suivante.

- [x] 1. Auditer exigences, canon et existant, recouper le contrat v1 adopté
  Prérequis : requirements.md historique, canon actuel, sources du lot.
  Critère : inventaire daté des quatre exigences et de leurs scénarios, écarts réels séparés de l'historique, contrat v1 adopté et traçable aux six documents et à la métadonnée de la RSMP.
  Contrôles dans cette tâche : relecture des blocs complets et des liens, liste des écarts, revue documentaire, conservation des versions et preuves.

- [x] 2. Parseur et validateurs stricts du profil v1 avec tests dans la même tâche
  Prérequis : tâche 1 validée.
  Critère : documents valides acceptés, documents à champ inconnu, opérateur hors liste, type hors liste, UTF-8 invalide ou dépassement des plafonds inclusifs 65536 octets, 8 niveaux, 256 nœuds refusés avant activation avec erreur typée.
  Contrôles dans cette tâche : syntaxe Python par py_compile, suite configurée du périmètre, cas nominaux et refus, erreurs sans donnée sensible complète, revue du diff.

- [x] 3. Moteur déterministe borné du profil v1 avec tests dans la même tâche
  Prérequis : tâche 2 validée.
  Critère : même entrée et même version donnent même résultat ou même refus explicite, sans accès réseau, sans horloge implicite, sans entrée-sortie, sans code, avec bornes respectées.
  Contrôles dans cette tâche : syntaxe, unités déterministes, rejeu, refus hors bornes, absence de coercition boolean et integer, preuves natives conservées.

- [x] 4. Intégration publique propriétaires, autorisation, audit et explications avec tests réels applicables dans la même tâche
  Prérequis : tâche 3 validée.
  Critère : proposition évaluée puis décision écrite seule par la Command autorisée du propriétaire après réévaluation autorisation, garde et version ; explication corrélée avec les sept champs de résultat, la corrélation fournie et les motifs minimisés sans entrée sensible complète ; autorisation distincte conservée.
  Contrôles dans cette tâche : syntaxe, intégrations réelles du profil sur dépendance réelle, refus sans permission, isolation tenant et scope, audit minimisé, tests navigateur si interface web concernée.

- [x] 5. Non-régression, revue croisée et éligibilité d'archive
  Prérequis : tâche 4 validée.
  Critère : corpus par version rejoué, matrice de preuves reliée aux versions et artefacts, périmètre relu, UTF-8 et fins de ligne vérifiés, aucune opération finale sans autorisation distincte.
  Contrôles dans cette tâche : consolidation des preuves des tâches 1 à 4, réexécution des seuls contrôles invalidés, vérification OpenSpec stricte, examen du diff et des limites, décision d'éligibilité à l'archivage.

Les vérifications utilisent les outils et versions du projet selon AGENTS.md et DEVOPS.md. La syntaxe seule ne valide aucun comportement. La seule préparation documentaire ne valait pas exécution ; les contrôles ultérieurs et leurs limites sont consignés dans requirements.md.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### O06-SL01 — Auditer exigences, canon et existant, recouper le contrat v1 adopté

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — O06 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O06-SL02 — Parseur et validateurs stricts du profil v1 avec tests dans la même tâche

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — O06 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O06-SL03 — Moteur déterministe borné du profil v1 avec tests dans la même tâche

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — O06 », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O06-SL04 — Intégration publique propriétaires, autorisation, audit et explications avec tests réels applicables dans la même tâche

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — O06 », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O06-SL05 — Non-régression, revue croisée et éligibilité d'archive

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — O06 », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
