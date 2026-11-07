# Tâches — C04

Le RUN CISMP3 autorise la réalisation de ce seul change. Les preuves
exécutées, leurs limites et les propriétaires sont détaillés dans
VALIDATION.md. Une archive, un inventaire ou une coche ne remplace pas une
validation actuelle. La qualification commune du composite a été recoupée directement :
21 PG avec Auth, Core et C05 réels ; trust/assurance et plan restent des fixtures déclarées.

## 1. Revue de conception

- [x] 1.1 Revoir requirements.md, le profil C00 et les sources actuelles : matrice, canons et profils purs recoupés ; OpenSpec strict 191/191.
- [x] 1.2 Qualifier les contrats R01 D15/D16 : DTO opérateur disjoint, Ed25519 C03, plan/hash/cibles C08, 600 s, consommation au commit et inspection ; banc commun R0114 réel, C08/classification/assurance fixtures explicites.

## 2. Réalisation

- [x] 2.1 Relier faits Auth, contexte, policies et ressources aux frontières Django : code et12 PG C04 validés ; banc commun21 PG RuntimeTrustedFactsProvider/AuthInvocationSource/CoreFactSource/CoreAuthorizationStore/RuntimeAuthorizationDecider et C05 réels, incluant7 scénarios du composite.
- [x] 2.2 PEP, filtre SQL, obligations/fraîcheur et réévaluations : Core query et C05 filter_audit réels, 18PG ; ports de contrôle final et fraîcheur10+8PG.
- [x] 2.3 Compte fonctionnel actif/Binding unique d'installation, PLATFORM et accords tenant explicites, sans transfert ; store/decider27PG.
- [x] 2.4 DENY ordinaire, tenant non accordé/accordé malgré ACL, dérogations et façades Core : 192 tests purs, 113 PG C04 distincts, 200 scénarios Core C02 et migrations. Les interfaces C06/C09/C13 non activées restent hors de cette preuve.

## 3. Vérifications de réalisation

- [x] 3.1 Syntaxe et suites applicables exécutées : 25 Python compilés,192 tests et recettes PG isolées, preuves natives dans VALIDATION.md.
- [x] 3.2 Isolation, échecs, refus fermés et absence de valeur secrète exposée : schémas propres détruits, connexions fermées, doubles identifiés ; contraintes des consommateurs déclarées.
- [x] 3.3 Effets/fichiers examinés et sources préexistantes préservées : SHA/natifs unitaires/CAB, aucun Git ou P0 global annoncé, impacts et limites documentés.
- [x] 3.4 Périmètre des opérations de clôture vérifié : archivage/synchronisation OpenSpec nécessaires délégués par CISMP/ISMP ; aucun commit, push, déploiement ou autre change autorisé dans ce RUN.

## 4. Obligations de clôture suivies par le gate

Après les critères de réalisation, observer l'archive réussie et la
publication resource-scoped-v1, puis produire et vérifier le rapport propre
STATISTIQUES.md à six sections UTF-8/LF. Le gate individuel, le désarmement
et la libération du seul RUN restent obligatoires. Cette liste décrit des
obligations post-archivage et ne les présente pas comme déjà réalisées.
Aucun état TERMINÉ n'est admis avant leurs preuves.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### C04-SL01 — Revoir requirements.md, le profil C00 et les sources actuelles : matrice, canons et profils purs recoupés ; OpenSpec strict 191/191.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL02 — Qualifier les contrats R01 D15/D16 : DTO opérateur disjoint, Ed25519 C03, plan/hash/cibles C08, 600 s, consommation au commit et inspection ; banc commun R0114 réel, C08/classification/assurance fixtures explicites.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL03 — Relier faits Auth, contexte, policies et ressources aux frontières Django : code et12 PG C04 validés ; banc commun21 PG RuntimeTrustedFactsProvider/AuthInvocationSource/CoreFactSource/CoreAuthorizationStore/RuntimeAuthorizationDecider et C05 réels, incluant7 scénarios du composite.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL04 — PEP, filtre SQL, obligations/fraîcheur et réévaluations : Core query et C05 filter_audit réels, 18PG ; ports de contrôle final et fraîcheur10+8PG.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL05 — Compte fonctionnel actif/Binding unique d'installation, PLATFORM et accords tenant explicites, sans transfert ; store/decider27PG.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL06 — DENY ordinaire, tenant non accordé/accordé malgré ACL, dérogations et façades Core : 192 tests purs, 113 PG C04 distincts, 200 scénarios Core C02 et migrations. Les interfaces C06/C09/C13 non activées restent hors de cette preuve.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL07 — Syntaxe et suites applicables exécutées : 25 Python compilés,192 tests et recettes PG isolées, preuves natives dans VALIDATION.md.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Vérifications de réalisation », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL08 — Isolation, échecs, refus fermés et absence de valeur secrète exposée : schémas propres détruits, connexions fermées, doubles identifiés ; contraintes des consommateurs déclarées.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Vérifications de réalisation », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL09 — Effets/fichiers examinés et sources préexistantes préservées : SHA/natifs unitaires/CAB, aucun Git ou P0 global annoncé, impacts et limites documentés.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Vérifications de réalisation », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C04-SL10 — Périmètre des opérations de clôture vérifié : archivage/synchronisation OpenSpec nécessaires délégués par CISMP/ISMP ; aucun commit, push, déploiement ou autre change autorisé dans ce RUN.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Vérifications de réalisation », ligne 26 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
