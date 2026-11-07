## 1. Preparation OpenSpec

- [x] 1.1 Relire proposal et design, vérifier le delta canonique contracts sans nouvelle norme.
- [x] 1.2 Créer le seul delta requis et valider le change en mode strict ; vérifier UTF-8/LF et cohérence des cadrages.

## 2. Fondation descripteurs

- [x] 2.1 Préparer le paquet pur contracts avec `ContractCategory` à sept valeurs et `ContractDescriptor` figé à cinq champs obligatoires, sans parseur divergent ni modification d’API existante.
- [x] 2.2 Préparer `require_category` à catégorie exacte avec retour du membre validé et `check_evolution` avec `breaking` bool exact, ruptures id/catégorie en majeure indépendamment du build/préversion, idempotence à précédence égale limitée aux mêmes champs hors version, refus des baisses et des changements propriétaire/doc à même précédence.
- [x] 2.3 Préparer `DeprecationNotice` séparé lié au descripteur annonçant en identité exacte build inclus, annonce normale stable seulement en mineure avec remplacement documenté obligatoire, préversions refusées, puis `check_retirement` stable en majeure strictement supérieure, sans suppression réelle ni exception critique.
- [x] 2.4 Documenter le parcours synthétique et les exclusions ; aucun effet externe, secret, base ou dépendance nouvelle.
- [x] 2.5 Préparer les tests purs unitaires/integration avec entrées invalides réelles, immutabilité, SemVer avec préversions/build, category mismatch, baisse/rupture, `breaking` non bool refusé, idempotence build seul, dépréciation/retrait normaux stables, refus des annonces en préversion, des retraits anticipés et des chemins non supportés.

## 3. Preuves et clôture

- [x] 3.1 Exécuter les tests dédiés unitaires/integration avec données synthétiques et refus des entrées invalides.
- [x] 3.2 Exécuter les régressions applicables, contrôles de syntaxe, UTF-8/LF et validation OpenSpec stricte, puis vérifier le périmètre.
- [x] 3.3 Vérifier les preuves, les critères, la cohérence et la validation CGPT du dossier de clôture avant archivage.

L’archivage est exigé après toutes les tâches ci-dessus prouvées et cochées, sous mandat CAB distinct après contrôle CGPT ; il ne fait pas partie de la case 3.3.
La production de STATISTIQUES.md est un mandat distinct après archivage effectif, avec sonde finale et quotas réels ou N/A motivés. Aucune case ci-dessus n’est une preuve acquise. Si la session s’arrête à 16h30 Paris, conserver l’état du premier jalon non prouvé sans archivage ni déclaration de réussite.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et clôture ».

### C34-SL01 — Relire proposal et design, vérifier le delta canonique contracts sans nouvelle norme.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation OpenSpec », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL02 — Créer le seul delta requis et valider le change en mode strict ; vérifier UTF-8/LF et cohérence des cadrages.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation OpenSpec », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL03 — Préparer le paquet pur contracts avec `ContractCategory` à sept valeurs et `ContractDescriptor` figé à cinq champs obligatoires, sans parseur divergent ni modification d’API existante.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Fondation descripteurs », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL04 — Préparer `require_category` à catégorie exacte avec retour du membre validé et `check_evolution` avec `breaking` bool exact, ruptures id/catégorie en majeure indépendamment du build/préversion, idempotence à précédence égale limitée aux mêmes champs hors version, refus des baisses et des changements propriétaire/doc à même précédence.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Fondation descripteurs », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL05 — Préparer `DeprecationNotice` séparé lié au descripteur annonçant en identité exacte build inclus, annonce normale stable seulement en mineure avec remplacement documenté obligatoire, préversions refusées, puis `check_retirement` stable en majeure strictement supérieure, sans suppression réelle ni exception critique.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Fondation descripteurs », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL06 — Documenter le parcours synthétique et les exclusions ; aucun effet externe, secret, base ou dépendance nouvelle.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Fondation descripteurs », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL07 — Préparer les tests purs unitaires/integration avec entrées invalides réelles, immutabilité, SemVer avec préversions/build, category mismatch, baisse/rupture, `breaking` non bool refusé, idempotence build seul, dépréciation/retrait normaux stables, refus des annonces en préversion, des retraits anticipés et des chemins non supportés.

- Ancien repère et tâche rattachée : tâche 2.5 ; section « 2. Fondation descripteurs », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL08 — Exécuter les tests dédiés unitaires/integration avec données synthétiques et refus des entrées invalides.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL09 — Exécuter les régressions applicables, contrôles de syntaxe, UTF-8/LF et validation OpenSpec stricte, puis vérifier le périmètre.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C34-SL10 — Vérifier les preuves, les critères, la cohérence et la validation CGPT du dossier de clôture avant archivage.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
