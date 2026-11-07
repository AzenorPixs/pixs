Le plan ci-dessous est le plan historique commun aux treize exigences.
Il est conservé sans nouvelle coche : tâches 1.1–3.2 pour le bootstrap,
4.1–4.3 et 5.1 pour le lot compagnon ; 5.2–5.3 sont des contrôles communs
comptés une seule fois dans le rapport de revalidation. Les coches historiques
ne valent pas preuve actuelle de présentation ni de qualification produit.

## 1. Composition P0 initiale

- [x] 1.1 Décrire la conformité de la composition initiale à
  `reference-composition`, y compris son composant d'exemple technique non
  métier.
- [x] 1.2 Vérifier que les exigences de composition préservent Django,
  PostgreSQL, `pixs.kernel`, `pixs.core`, les contrats publics et l'absence de
  valeur sensible distribuée.

## 2. Surface et shell initialement spécifiés

- [x] 2.1 Définir les frontières documentaires des routes de santé, du shell et
  de l'API versionnée sans introduire de ressource métier fictive.
- [x] 2.2 Vérifier la cohérence de ces frontières avec les capacités API,
  frontend, sécurité et contrats publics existantes.

## 3. Profil local de référence

- [x] 3.1 Décrire le profil local comme cible de validation future, ses
  dépendances, son adresse d'écoute, son cycle et ses limites non productives.
- [x] 3.2 Vérifier qu'aucune exigence du profil ne requiert de secret, de
  donnée métier permanente ou de dépendance de production.

## 4. Installation et administration spécifiées

- [x] 4.1 Vérifier les transitions documentées entre INSTALLER,
  FIRST_CONFIGURATION, NORMAL et MAINTENANCE ainsi que les marqueurs externes.
- [x] 4.2 Vérifier que le Super Admin est l'opérateur initial doté d'une
  identité numérique vérifiée et d'une politique d'autorisation déclarée, avec
  un bypass ACL limité au panneau d'administration.
- [x] 4.3 Vérifier que toute valeur PostgreSQL saisie par l'installateur devient
  une référence `SecretProvider` sans persistance ni exposition de credential.

## 5. Audit, maintenance et conformité documentaire

- [x] 5.1 Vérifier les exigences de maintenance hiérarchisée et d'audit
  persistant des interactions administratives contre les capacités actives.
- [x] 5.2 Exécuter les validations OpenSpec strictes applicables et vérifier
  que ce change ne requiert ni code, ni dépendance, ni configuration
  exécutable.
- [x] 5.3 Présenter les spécifications consolidées au développeur avant toute
  demande d'archivage ; toute implémentation future relèvera d'un change
  distinct autorisé.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### SP05-SL01 — Décrire la conformité de la composition initiale à

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Composition P0 initiale », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL02 — Vérifier que les exigences de composition préservent Django,

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Composition P0 initiale », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL03 — Définir les frontières documentaires des routes de santé, du shell et

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Surface et shell initialement spécifiés », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL04 — Vérifier la cohérence de ces frontières avec les capacités API,

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Surface et shell initialement spécifiés », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL05 — Décrire le profil local comme cible de validation future, ses

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Profil local de référence », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL06 — Vérifier qu'aucune exigence du profil ne requiert de secret, de

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Profil local de référence », ligne 27 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL07 — Vérifier les transitions documentées entre INSTALLER,

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Installation et administration spécifiées », ligne 32 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL08 — Vérifier que le Super Admin est l'opérateur initial doté d'une

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Installation et administration spécifiées », ligne 34 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL09 — Vérifier que toute valeur PostgreSQL saisie par l'installateur devient

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Installation et administration spécifiées », ligne 37 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL10 — Vérifier les exigences de maintenance hiérarchisée et d'audit

- Ancien repère et tâche rattachée : tâche 5.1 ; section « 5. Audit, maintenance et conformité documentaire », ligne 42 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL11 — Exécuter les validations OpenSpec strictes applicables et vérifier

- Ancien repère et tâche rattachée : tâche 5.2 ; section « 5. Audit, maintenance et conformité documentaire », ligne 44 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### SP05-SL12 — Présenter les spécifications consolidées au développeur avant toute

- Ancien repère et tâche rattachée : tâche 5.3 ; section « 5. Audit, maintenance et conformité documentaire », ligne 47 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
