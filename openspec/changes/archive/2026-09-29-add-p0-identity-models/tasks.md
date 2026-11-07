# Tasks

## 1. Modèles et contrats

- [x] 1.1 Implémenter les trois modèles immuables, les deux enums et les validations UUIDv7/types/états avec erreurs constantes.
- [x] 1.2 Implémenter la validation des liaisons : références, unicité bidirectionnelle, doublons et absence d'effets.
- [x] 1.3 Publier la façade identity et l'intégrer à core en préservant scope.

## 2. Tests

- [x] 2.1 Prouver les cas modèles, états, types, UUID, immutabilité et entrées invalides avec la suite unitaire modèles.
- [x] 2.2 Prouver les cardinalités, références, doublons et absence de mutation avec la suite unitaire liaisons.
- [x] 2.3 Prouver le contrat via la façade publique et les refus sans valeur brute.

## 3. Validation finale

- [x] 3.1 Réussir les suites complètes, AST, UTF-8/LF et OpenSpec strict ; vérifier conformité normative et absence de modification hors périmètre avant archivage.

## Preuves finales contrôlées par CGPT

- Sources, contrat public et tests relus ; unicité UUID globale conforme à TECHNICAL §13, liaison 0..1 dans chaque sens, références et refus sans valeur brute.
- Unités : `identity-unit02`, outil `msg_0ee92a4380012vGUugsVHriiwR` — 304 tests OK, exit 0, dont 10 modèles et 13 liaisons.
- Intégration : `identity-integration02`, outil `msg_0ee9380840019OYIr0dmscleJx` — 100 tests OK, exit 0, dont 4 tests de façade identité.
- Syntaxe et encodage : `identity-ast03`, outil `msg_0ee9468c0001oEIiVT34cQG6BU` — 6 AST et 10 fichiers UTF-8/LF valides, exit 0.
- OpenSpec : `identity-strict03`, outil `msg_0ee952457001OYXA2wPjEasmjF`, rapport `msg_0ee95302b001DDBpjgCbjpBHh8` — 77 éléments valides, 0 échec, exit 0.
- Contrôle de périmètre : dix fichiers attendus, écritures observées et contenus réconciliés ; cadrages PROJECT/TECHNICAL/BUILD/DEVOPS/README cohérents pour ce socle structurel. Aucune dépendance nouvelle, aucun Git ni effet d'authentification/persistance.
- Incidents tracés : `identity-ast01` refusé pour commande divergente, non exécuté ; découverte globale `identity-alltests01` échouée sur import existant du PDP. Reprise CAB `identity-recovery01` réussie et suites habituelles finales ci-dessus réussies. L'échec antérieur n'est pas présenté comme un succès.
- L'archivage reste une opération distincte à autoriser par CGPT. Les exigences de backend réel, d'authentification et d'audit durable restent hors de ce change.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Validation finale » ; « Preuves finales contrôlées par CGPT ».

### C23-SL01 — Implémenter les trois modèles immuables, les deux enums et les validations UUIDv7/types/états avec erreurs constantes.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Modèles et contrats », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C23-SL02 — Implémenter la validation des liaisons : références, unicité bidirectionnelle, doublons et absence d'effets.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Modèles et contrats », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C23-SL03 — Publier la façade identity et l'intégrer à core en préservant scope.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Modèles et contrats », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C23-SL04 — Prouver les cas modèles, états, types, UUID, immutabilité et entrées invalides avec la suite unitaire modèles.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Tests », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C23-SL05 — Prouver les cardinalités, références, doublons et absence de mutation avec la suite unitaire liaisons.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Tests », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C23-SL06 — Prouver le contrat via la façade publique et les refus sans valeur brute.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Tests », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C23-SL07 — Réussir les suites complètes, AST, UTF-8/LF et OpenSpec strict ; vérifier conformité normative et absence de modification hors périmètre avant archivage.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Validation finale », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
