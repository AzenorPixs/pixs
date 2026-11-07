# Tasks

## 1. Préparation

- [x] 1.1 Confirmer l’absence de change actif, les 27 baselines, les 136 tests et les normes R2/R4 ; publier les cinq artefacts dont le delta reproduit R2/R4 mot pour mot, puis réussir les stricts du change et canonique avant tout code.

## 2. Codec

- [x] 2.1 Ajouter l’exception à message fixe et `encode_feature_flag_source_snapshot` : type exact, validation réelle intégrale du lot avant extraction, copies récursives neuves, pas d’asdict, pas de copie générique, pas d’écho d’erreur.
- [x] 2.2 Ajouter `decode_feature_flag_source_snapshot` : clés et types exacts avant hachage ou hook, reconstruction des dataclasses canoniques, appel réel du validateur de lot complet, aucune normalisation ni alias.

## 3. Tests

- [x] 3.1 Créer la suite unitaire causale : aller-retours, scalaires opaques, `False`, Unicode, conteneurs frais, hostiles sans hook, clés et formes invalides, liaisons invalides, absence d’écho et conservation de la valeur structurellement valide mais évaluée `INVALID`.
- [x] 3.2 Créer la suite d’intégration en processus frais avec gardes éprouvées : composition réelle, validateurs réellement appelés et comptes nuls pour filesystem, réseau, sous-processus, horloge, PostgreSQL et secrets.

## 4. Preuves

- [x] 4.1 Réussir les trois compilations, la nouvelle suite unitaire, la nouvelle intégration et les 136 régressions dans l’environnement Python explicite.
- [x] 4.2 Vérifier les 27 baselines inchangées, les anciens modules et tests non modifiés, UTF-8/LF, limites sans persistance, PostgreSQL, audit, cache, dépendance, export ou README, puis le delta canonique exact.
- [x] 4.3 Réussir les stricts après preuves et faire contrôler les critères, les résultats et la cohérence du change par CGPT avant son autorisation distincte d’archivage.

Après cochage sous mandat distinct et strict réussi, l’archivage exige sa propre autorisation CGPT et son mandat CAB. Le rapport STATISTIQUES.md est produit après archivage sous un mandat séparé ; sa preuve reste obligatoire avant de déclarer le sous-job terminé.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 4. Preuves ».

### O51-SL01 — Confirmer l’absence de change actif, les 27 baselines, les 136 tests et les normes R2/R4 ; publier les cinq artefacts dont le delta reproduit R2/R4 mot pour mot, puis réussir les stricts du change et canonique avant tout code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL02 — Ajouter l’exception à message fixe et `encode_feature_flag_source_snapshot` : type exact, validation réelle intégrale du lot avant extraction, copies récursives neuves, pas d’asdict, pas de copie générique, pas d’écho d’erreur.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Codec », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL03 — Ajouter `decode_feature_flag_source_snapshot` : clés et types exacts avant hachage ou hook, reconstruction des dataclasses canoniques, appel réel du validateur de lot complet, aucune normalisation ni alias.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Codec », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL04 — Créer la suite unitaire causale : aller-retours, scalaires opaques, `False`, Unicode, conteneurs frais, hostiles sans hook, clés et formes invalides, liaisons invalides, absence d’écho et conservation de la valeur structurellement valide mais évaluée `INVALID`.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL05 — Créer la suite d’intégration en processus frais avec gardes éprouvées : composition réelle, validateurs réellement appelés et comptes nuls pour filesystem, réseau, sous-processus, horloge, PostgreSQL et secrets.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Tests », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL06 — Réussir les trois compilations, la nouvelle suite unitaire, la nouvelle intégration et les 136 régressions dans l’environnement Python explicite.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Preuves », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL07 — Vérifier les 27 baselines inchangées, les anciens modules et tests non modifiés, UTF-8/LF, limites sans persistance, PostgreSQL, audit, cache, dépendance, export ou README, puis le delta canonique exact.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Preuves », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O51-SL08 — Réussir les stricts après preuves et faire contrôler les critères, les résultats et la cohérence du change par CGPT avant son autorisation distincte d’archivage.

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Preuves », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
