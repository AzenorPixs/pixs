# Tâches — C01

Réalisation et qualification fonctionnelle prouvées sous le RUN parent CISMP3/ISMP. La RSMP documentaire initiale n’autorisait que sa rédaction ; les réalisations suivantes relèvent du mandat parent. Les états d’archive, de statistiques et de publication sont suivis séparément par le gate terminal du RUN et ne sont pas déduits des coches.

## 1. Revue de conception

- [x] 1.1 Revoir exigences et deltas B01-B09, adoption C00 archivé ; sources et périmètre recoupés avant réalisation.
- [x] 1.2 Valider le contrat systemd-restart, l’audit d’amorçage, PLATFORM + INSTALLER borné, schémas et reçus. Choix et contrat validés explicitement par le développeur.

## 2. Réalisation

- [x] 2.1 Déclarer le provider approuvé, le manifeste PROVIDER 0.1.0, les entrées runtime et les garanties.
- [x] 2.2 Relier les références aux réglages Django sans valeur distribuée. LazySettings.configure réel vérifié dans les consommateurs v1/v2 ; aucun accès base ou django.setup.
- [x] 2.3 Implémenter résolution autorisée, refus fermé, rotation/révocation et audit minimisé. Reçus persistants relus avant succès, sans callback booléen de substitution.
- [x] 2.4 Tester absence de provider, workload non autorisé, révocation, restart et absence de fuite. Cas isolés et harnais réel validés avec fixtures publiques ; mode null limité au transport fonctionnel.

## 3. Preuves et autorisations de clôture

- [x] 3.1 Exécuter syntaxe, contrôles ciblés et suites applicables. Régression globale 1 945 tests réussis ; correctifs/récupération 26 tests ; cinq deltas C01 strictement validés, dont le contenu normatif est conservé pendant synchronisation.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret réel et conformité des scénarios. Qualification indépendante c3-cmd-236584a2-effect : 12 événements, reçus, invocations, versions et absence des deux unités recoupés.
- [x] 3.3 Examiner contenus et empreintes du périmètre. Cinq invariants Kernel/gabarits/contrôles préservés ; aucun état Git inspecté ; aucune disponibilité P0 annoncée.
- [x] 3.4 Vérifier les autorisations des opérations de clôture. Archivage, synchronisation des seuls cinq canons et STATISTIQUES.md sont autorisés par le RUN parent et confirmés par la demande finale du développeur ; chaque effet conserve un mandat CAB distinct. Aucune autorisation Git ou déploiement général n’en découle.

## Barrières terminales indépendantes

Les validations globales d’archivage, l’archive effective, sa publication, le rapport STATISTIQUES.md à six sections et le gate puis désarmement/libération restent obligatoires. Leurs preuves sont consignées dans le checkpoint et le rapport final après leur exécution ; les tâches ci-dessus ne prétendent pas les avoir produites par avance.

Voir [PREUVES-C01.json](PREUVES-C01.json) pour les reçus, identifiants et limites de qualification.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et autorisations de clôture ».

### C01-SL01 — Revoir exigences et deltas B01-B09, adoption C00 archivé ; sources et périmètre recoupés avant réalisation.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL02 — Valider le contrat systemd-restart, l’audit d’amorçage, PLATFORM + INSTALLER borné, schémas et reçus. Choix et contrat validés explicitement par le développeur.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL03 — Déclarer le provider approuvé, le manifeste PROVIDER 0.1.0, les entrées runtime et les garanties.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL04 — Relier les références aux réglages Django sans valeur distribuée. LazySettings.configure réel vérifié dans les consommateurs v1/v2 ; aucun accès base ou django.setup.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL05 — Implémenter résolution autorisée, refus fermé, rotation/révocation et audit minimisé. Reçus persistants relus avant succès, sans callback booléen de substitution.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL06 — Tester absence de provider, workload non autorisé, révocation, restart et absence de fuite. Cas isolés et harnais réel validés avec fixtures publiques ; mode null limité au transport fonctionnel.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL07 — Exécuter syntaxe, contrôles ciblés et suites applicables. Régression globale 1 945 tests réussis ; correctifs/récupération 26 tests ; cinq deltas C01 strictement validés, dont le contenu normatif est conservé pendant synchronisation.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et autorisations de clôture », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL08 — Vérifier isolation, échecs attendus, absence de secret réel et conformité des scénarios. Qualification indépendante c3-cmd-236584a2-effect : 12 événements, reçus, invocations, versions et absence des deux unités recoupés.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et autorisations de clôture », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL09 — Examiner contenus et empreintes du périmètre. Cinq invariants Kernel/gabarits/contrôles préservés ; aucun état Git inspecté ; aucune disponibilité P0 annoncée.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et autorisations de clôture », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C01-SL10 — Vérifier les autorisations des opérations de clôture. Archivage, synchronisation des seuls cinq canons et STATISTIQUES.md sont autorisés par le RUN parent et confirmés par la demande finale du développeur ; chaque effet conserve un mandat CAB distinct. Aucune autorisation Git ou déploiement général n’en découle.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et autorisations de clôture », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
