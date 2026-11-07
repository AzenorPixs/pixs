# Tasks

## 1. Modèles et contrat

- [x] 1.1 Implémenter Group et Membership immuables avec UUIDv7, contexte explicite et erreurs stables.
- [x] 1.2 Implémenter la validation ensembliste n:m : références, doublons, unicité d'identifiants et non-mutation.
- [x] 1.3 Étendre la façade identity et adapter uniquement les exports attendus du test existant.

## 2. Tests et conformité

- [x] 2.1 Prouver les cas valides et invalides des groupes/appartenances, dont contextes et données hostiles, via la suite unitaire.
- [x] 2.2 Prouver l'usage de la façade avec User et ScopeContext sans accès implicite.
- [x] 2.3 Réussir les suites complètes séparées, AST, UTF-8/LF et OpenSpec strict ; contrôler cohérence et périmètre avant archivage.

## Preuves finales contrôlées par CGPT

- Modèles et contrats relus : Group porte UUIDv7 et ScopeContext explicite ; Membership reste une relation de paire n:m. Réutilisation des validateurs identité/scope, références et unicité dans l'ensemble fourni, aucun état conservé.
- Unités : `groups-unit01`, outil `msg_0eeb054ce001ido650hzodg3Wv` — 316 tests OK, exit 0, dont 12 nouveaux tests groupes.
- Intégration : `groups-integration01`, outil `msg_0eeb1d205001C1KoqA05AtP7mp` — 103 tests OK, exit 0, dont 3 nouveaux tests groupes ; contrat identité existant préservé.
- Syntaxe et encodage : `groups-ast01`, outil `msg_0eeb34555001SScPRfZpw7SuvD` — 5 AST et 9 fichiers UTF-8/LF valides, exit 0.
- OpenSpec : `groups-strict02`, outil `msg_0eeb49602001y74Wbnm1qd0W5j`, rapport `msg_0eeb4a56a001xxidX0u41ZbQwU` — 77 éléments valides, 0 échec, exit 0.
- Périmètre : neuf fichiers attendus réconciliés avec leurs écritures observées ; identity/models.py inchangé (SHA-256 `253bac3be28375e78f8ca406a790e7e504a0b53d480785e5cb319baef2fe1a57`). Cohérence PROJECT §18, TECHNICAL §§11/13, core, scope et cadrages généraux contrôlée.
- Les tests ont été corrigés avant exécution pour employer une vraie sous-classe de tuple et couvrir les contextes incomplets/altérés et la revalidation ensembliste. Toutes les commandes de validation du change ont réussi.
- L'archivage et le rapport STATISTIQUES restent deux mandats distincts. Le développeur a demandé l'arrêt après archivage de ce change ; aucune sélection suivante ne doit être lancée après contrôle du rapport.
- Topologie, autorisation, persistance Django/PostgreSQL, groupes imbriqués et audit durable restent hors périmètre ; le projet global n'est pas déclaré terminé.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves finales contrôlées par CGPT ».

### C22-SL01 — Implémenter Group et Membership immuables avec UUIDv7, contexte explicite et erreurs stables.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Modèles et contrat », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C22-SL02 — Implémenter la validation ensembliste n:m : références, doublons, unicité d'identifiants et non-mutation.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Modèles et contrat », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C22-SL03 — Étendre la façade identity et adapter uniquement les exports attendus du test existant.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Modèles et contrat », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C22-SL04 — Prouver les cas valides et invalides des groupes/appartenances, dont contextes et données hostiles, via la suite unitaire.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Tests et conformité », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C22-SL05 — Prouver l'usage de la façade avec User et ScopeContext sans accès implicite.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Tests et conformité », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C22-SL06 — Réussir les suites complètes séparées, AST, UTF-8/LF et OpenSpec strict ; contrôler cohérence et périmètre avant archivage.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Tests et conformité », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
