## 1. Préparation OpenSpec

- [x] 1.1 Vérifier proposal et design dans la seule exigence API2 existante, portée partielle et delta canonique exact sans nouvelle norme.
- [x] 1.2 Préparer les cinq artefacts, valider strict et UTF-8/LF, vérifier la cohérence des cadrages et l'unicité du change.

## 2. Projection publique d'erreur

- [x] 2.1 Préparer errors.py et les exports publics par ajout minimal à la façade, avec signature et version contractuelle fixées.
- [x] 2.2 Revalider UUID exact et entier exact borné, reconstruire la représentation canonique, refuser entrées forgées/incomplètes et sous-classes sans diagnostic brut.
- [x] 2.3 Produire les cinq champs publics constants, détails vides et conteneurs frais ; ne jamais inspecter ou convertir internal_error.
- [x] 2.4 Ajouter au README les exemples synthétiques et limites en préservant intégralement le texte antérieur.
- [x] 2.5 Préparer les tests comportementaux unitaires et d'intégration via la façade, données synthétiques, UUID toutes versions/variants/nil/max et entrées hostiles.

## 3. Preuves et clôture

- [x] 3.1 Exécuter les tests dédiés séparés, observer leurs comptes et sorties réels.
- [x] 3.2 Exécuter les régressions unitaires et d'intégration séparées ; contrôler AST Python3.11, UTF-8/LF, exemples README, delta canonique, strict et périmètre.
- [x] 3.3 Vérifier preuves, critères et cohérence ; obtenir validation explicite CGPT du dossier de clôture avant archivage.

L'archivage exige ensuite un mandat CAB distinct après dix tâches prouvées et cochées et validation stricte du dossier coché. Il ne fait pas partie de la tâche 3.3. STATISTIQUES.md est un mandat distinct après archivage, sonde finale et quotas natifs ou N/A motivés. La requirement2 reste globalement non achevée : rejeu persistant, pagination, HTTP, tenant et authentification non prouvés. À 16h30 Paris, conserver le premier jalon non prouvé sans archivage prématuré.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et clôture ».

### C29-SL01 — Vérifier proposal et design dans la seule exigence API2 existante, portée partielle et delta canonique exact sans nouvelle norme.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation OpenSpec », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL02 — Préparer les cinq artefacts, valider strict et UTF-8/LF, vérifier la cohérence des cadrages et l'unicité du change.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation OpenSpec », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL03 — Préparer errors.py et les exports publics par ajout minimal à la façade, avec signature et version contractuelle fixées.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Projection publique d'erreur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL04 — Revalider UUID exact et entier exact borné, reconstruire la représentation canonique, refuser entrées forgées/incomplètes et sous-classes sans diagnostic brut.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Projection publique d'erreur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL05 — Produire les cinq champs publics constants, détails vides et conteneurs frais ; ne jamais inspecter ou convertir internal_error.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Projection publique d'erreur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL06 — Ajouter au README les exemples synthétiques et limites en préservant intégralement le texte antérieur.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Projection publique d'erreur », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL07 — Préparer les tests comportementaux unitaires et d'intégration via la façade, données synthétiques, UUID toutes versions/variants/nil/max et entrées hostiles.

- Ancien repère et tâche rattachée : tâche 2.5 ; section « 2. Projection publique d'erreur », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL08 — Exécuter les tests dédiés séparés, observer leurs comptes et sorties réels.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL09 — Exécuter les régressions unitaires et d'intégration séparées ; contrôler AST Python3.11, UTF-8/LF, exemples README, delta canonique, strict et périmètre.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C29-SL10 — Vérifier preuves, critères et cohérence ; obtenir validation explicite CGPT du dossier de clôture avant archivage.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
