# Tâches — C03

Les tâches de réalisation sont prouvées par VALIDATION.md et les résultats natifs du 21 octobre 2026. La tâche postérieure à l’archivage, 3.4, est prouvée par la création effective et la vérification des six sections/totaux de STATISTIQUES.md. Aucun état global P0 n’est déduit.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [x] 1.2 Appliquer les décisions D01–D17 déjà arrêtées ; détailler contrats/schémas, prendre en compte les deltas adoptés le 20 octobre 2026 et qualifier versions stables, coûts Argon2id, profil Django/OpenLDAP, cookie/transport, trousseau et preuve R01 avant écriture de code.

## 2. Réalisation qualifiée

- [x] 2.1 Décliner le provider local autonome de pixs.auth sur PostgreSQL par défaut après adoption des deltas Auth ; préciser confiance et contrats sans installer de source externe ni activer IdP/OpenLDAP/KDC implicitement.
- [x] 2.2 Implémenter les contrats spécialisés Auth, connexion/déconnexion, façade web cookie/CSRF et API/CLI Bearer opaque ; respecter stockage par empreinte, trousseau CLI ou mémoire et plafonds D03–D06/D09.
- [x] 2.3 Traiter rotation à usage unique, concurrence/réutilisation, révocation dérivée et globale D07–D10 ; raccorder transaction C05, exception limitée au retrait et réconciliation, sans audit ou commit inventé.
- [x] 2.4 Tester assurance réelle et exceptions Super Admin, frontières temporelles, réponse de renouvellement perdue, limite de sessions, changement de mot de passe, échecs d’audit/Auth et signature R01 de 10 minutes ; qualifier la vérification Argon2id croisée Django/OpenLDAP sans activation implicite.

## 3. Preuves et clôture

- [x] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [x] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [x] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et clôture ».

### C03-SL01 — Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL02 — Appliquer les décisions D01–D17 déjà arrêtées ; détailler contrats/schémas, prendre en compte les deltas adoptés le 20 octobre 2026 et qualifier versions stables, coûts Argon2id, profil Django/OpenLDAP, cookie/transport, trousseau et preuve R01 avant écriture de code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL03 — Décliner le provider local autonome de pixs.auth sur PostgreSQL par défaut après adoption des deltas Auth ; préciser confiance et contrats sans installer de source externe ni activer IdP/OpenLDAP/KDC implicitement.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation qualifiée », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL04 — Implémenter les contrats spécialisés Auth, connexion/déconnexion, façade web cookie/CSRF et API/CLI Bearer opaque ; respecter stockage par empreinte, trousseau CLI ou mémoire et plafonds D03–D06/D09.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation qualifiée », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL05 — Traiter rotation à usage unique, concurrence/réutilisation, révocation dérivée et globale D07–D10 ; raccorder transaction C05, exception limitée au retrait et réconciliation, sans audit ou commit inventé.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation qualifiée », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL06 — Tester assurance réelle et exceptions Super Admin, frontières temporelles, réponse de renouvellement perdue, limite de sessions, changement de mot de passe, échecs d’audit/Auth et signature R01 de 10 minutes ; qualifier la vérification Argon2id croisée Django/OpenLDAP sans activation implicite.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation qualifiée », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL07 — Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et clôture », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL08 — Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et clôture », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL09 — Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et clôture », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C03-SL10 — N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et clôture », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
