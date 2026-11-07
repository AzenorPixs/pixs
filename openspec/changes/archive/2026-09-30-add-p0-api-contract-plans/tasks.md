## 1. Preparation OpenSpec

- [x] 1.1 Relire proposal et design, vérifier le seul delta canonique API versionné par majeure sans nouvelle norme.
- [x] 1.2 Créer les artefacts nécessaires, valider le change en mode strict et vérifier UTF-8/LF et cohérence des cadrages.

## 2. Fondation plans API

- [x] 2.1 Préparer le paquet pur avec ApiContractPlan figé à deux champs obligatoires et façade publique, ContractDescriptor exact de catégorie API et référence logique nue, sans modification d'API existante.
- [x] 2.2 Préparer api_major_prefix et check_api_evolution réutilisant les APIs publiques de contrat et SemVer, préfixe indépendant des versions runtime, breaking bool exact, refus des ruptures sans majeure et des baisses.
- [x] 2.3 Revalider les objets forgés et champs manquants, imposer document distinct et coexistence non blanche seulement à majeure strictement supérieure, sans attestation réelle ni diagnostic reproduisant une entrée.
- [x] 2.4 Documenter le parcours synthétique et les exclusions, sans I/O, secret, base, réseau ou dépendance nouvelle.
- [x] 2.5 Préparer les tests purs unitaires et d'intégration significatifs avec entrées invalides, immutabilité, sous-classes et objets hostiles, SemVer 0/préversions/builds, majeure/mineure/corrective, références et coexistence.

## 3. Preuves et clôture

- [x] 3.1 Exécuter les tests dédiés unitaires et d'intégration avec données synthétiques ; rapporter leurs comptes réellement observés.
- [x] 3.2 Exécuter les régressions unitaires et d'intégration séparées, contrôler syntaxe AST Python3.11, UTF-8/LF, delta canonique, strict OpenSpec et périmètre.
- [x] 3.3 Vérifier les preuves, les critères, la cohérence et la validation explicite CGPT du dossier de clôture avant archivage.

L'archivage est exigé après toutes les tâches ci-dessus prouvées et cochées, sous mandat CAB distinct après contrôle CGPT ; il ne fait pas partie de la case 3.3.
La production de STATISTIQUES.md est un mandat distinct après archivage effectif, avec sonde finale et quotas réels ou N/A motivés. Aucune case ci-dessus n'est une preuve acquise. Si la session s'arrête à 16h30 Paris, conserver l'état du premier jalon non prouvé sans archivage ni déclaration de réussite.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et clôture ».

### C28-SL01 — Relire proposal et design, vérifier le seul delta canonique API versionné par majeure sans nouvelle norme.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation OpenSpec », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL02 — Créer les artefacts nécessaires, valider le change en mode strict et vérifier UTF-8/LF et cohérence des cadrages.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation OpenSpec », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL03 — Préparer le paquet pur avec ApiContractPlan figé à deux champs obligatoires et façade publique, ContractDescriptor exact de catégorie API et référence logique nue, sans modification d'API existante.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Fondation plans API », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL04 — Préparer api_major_prefix et check_api_evolution réutilisant les APIs publiques de contrat et SemVer, préfixe indépendant des versions runtime, breaking bool exact, refus des ruptures sans majeure et des baisses.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Fondation plans API », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL05 — Revalider les objets forgés et champs manquants, imposer document distinct et coexistence non blanche seulement à majeure strictement supérieure, sans attestation réelle ni diagnostic reproduisant une entrée.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Fondation plans API », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL06 — Documenter le parcours synthétique et les exclusions, sans I/O, secret, base, réseau ou dépendance nouvelle.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Fondation plans API », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL07 — Préparer les tests purs unitaires et d'intégration significatifs avec entrées invalides, immutabilité, sous-classes et objets hostiles, SemVer 0/préversions/builds, majeure/mineure/corrective, références et coexistence.

- Ancien repère et tâche rattachée : tâche 2.5 ; section « 2. Fondation plans API », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL08 — Exécuter les tests dédiés unitaires et d'intégration avec données synthétiques ; rapporter leurs comptes réellement observés.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL09 — Exécuter les régressions unitaires et d'intégration séparées, contrôler syntaxe AST Python3.11, UTF-8/LF, delta canonique, strict OpenSpec et périmètre.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C28-SL10 — Vérifier les preuves, les critères, la cohérence et la validation explicite CGPT du dossier de clôture avant archivage.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
