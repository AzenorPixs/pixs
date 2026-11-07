## 1. Préparation

- [x] 1.1 Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et les validations OpenSpec applicables.

## 2. Implémentation

- [x] 2.1 Ajouter le module interne pur conforme au profil canonique.
- [x] 2.2 Ajouter les tests unitaires du contrat et des valeurs interdites.
- [x] 2.3 Ajouter l'intégration en processus frais avec gardes vérifiés positivement.

## 3. Validation finale

- [x] 3.1 Compiler les trois fichiers Python avec l'interpréteur retenu.
- [x] 3.2 Réussir les tests unitaires, l'intégration et les régressions audit/diagnostics/façades/pureté.
- [x] 3.3 Vérifier la conformité finale OpenSpec, UTF-8/LF, les seuls fichiers attendus et l'absence d'effets.

Archivage et STATISTIQUES.md : mandats distincts après les sept preuves ; aucune tâche cochée avant sa preuve.

## Preuves de clôture des tâches

- Trois fichiers Python compilés séparément, codes natifs 0.
- Tests : 22 unitaires, 1 intégration fraîche gardée et 56 régressions, soit 79 réussis ; aucun échec, erreur ou skip.
- Intégration : gardes positivement vérifiés puis compteurs zéro ; stdout marqueur exact, stderr vide, sous-processus 0, probe absent et temporaire nettoyé.
- Change strict final : 1/1, code natif 0, aucune issue. Global final : 77/77, code natif 0 ; 21 WARNING de longueur seulement, exclus par instruction développeur.
- Canon audit validé en RSMP : non strict 1/1 et code 0 ; strict code 1 pour le seul WARNING de longueur, jamais présenté comme réussite stricte. Delta MODIFIED identique au canon approuvé.
- Sources UTF-8/LF exactes, empreintes préexistantes ciblées inchangées, façade publique/configuration/dépendances préservées.
- Incident : tentative supplémentaire true refusée avant exécution ; session isolée, absence d'effet prouvée, nouvelle session READY et CAB test inédit /usr/bin/true exit 0. Résultats réussis non rejoués.
- Archivage et rapport statistique restent des mandats distincts après cette clôture des tâches.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Validation finale » ; « Preuves de clôture des tâches ».

### C75-SL01 — Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et les validations OpenSpec applicables.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C75-SL02 — Ajouter le module interne pur conforme au profil canonique.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Implémentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C75-SL03 — Ajouter les tests unitaires du contrat et des valeurs interdites.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Implémentation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C75-SL04 — Ajouter l'intégration en processus frais avec gardes vérifiés positivement.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Implémentation », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C75-SL05 — Compiler les trois fichiers Python avec l'interpréteur retenu.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Validation finale », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C75-SL06 — Réussir les tests unitaires, l'intégration et les régressions audit/diagnostics/façades/pureté.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Validation finale », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C75-SL07 — Vérifier la conformité finale OpenSpec, UTF-8/LF, les seuls fichiers attendus et l'absence d'effets.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Validation finale », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
