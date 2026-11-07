## 1. Lecteur privé en lecture actuelle

- [x] 1.1 Implémenter l'API asynchrone privée avec trusted_ports exact, server_context opaque, operation_reference serveur, check EXECUTE puis gouvernance RESOLVED sur ObjectMetadataV1 attendu, sans preuve par snapshots reçus ni callback du payload.
- [x] 1.2 Factoriser à strict nécessaire le contrôle de réponse GovernanceResolutionV1 dans bulk_trusted_ports.py avec helper commun, conserver le comportement MappingDescriptorV1 B01, éviter tout cycle ; modification soumise à un mandat CAB distinct.
- [x] 1.3 Implémenter qualification résolue qualify liée instance/version, invocation bornée stat_private/iter_bytes par deadline UTC et asyncio.Event avec asyncio.wait, alimentation du vérificateur existant, fermeture itérateur/tâches/ressources sur toute sortie, aucun octet remis ni copie complète.

## 2. Preuves

- [x] 2.1 Réussir unitaires avec provider synthétique déclaré, bornes PolicyV1 existantes, versions divergentes, authority/governance refusés, types hostiles, absence de fuite ou d'effet après refus.
- [x] 2.2 Réussir intégration fraîche, compiler les Python concernés, prouver sous gardes l'absence d'import ORM et la non-applicabilité PostgreSQL sans test SQL artificiel, vérifier compatibilité B01.
- [x] 2.3 Vérifier strict change/global, UTF-8/LF, cohérence et absence de modification hors périmètre.

## Procédure après preuves

Cocher seulement après preuve. Archiver une seule fois, publier STATISTIQUES.md sous mandat distinct, vérifier six sections/totaux puis revenir à SÉLECTION sans fin globale.

## Résultats des contrôles combinés

Les 545 tests Bulk réussissent sous exclusion d’intégration. OpenSpec standard valide 79/79 éléments ; le strict global est 77/79 avec les quatre WARNING de longueur préexistants inchangés (bulk-operations exigences 6, 10, 13 et identity-assurance exigence 4), sans ERROR ni nouvelle anomalie. Le change B04 est strictement valide sans issue. Ces avertissements extérieurs ne sont pas présentés comme une réussite stricte globale et ne sont pas corrigés dans ce change.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Preuves » ; « Procédure après preuves » ; « Résultats des contrôles combinés ».

### B50-SL01 — Implémenter l'API asynchrone privée avec trusted_ports exact, server_context opaque, operation_reference serveur, check EXECUTE puis gouvernance RESOLVED sur ObjectMetadataV1 attendu, sans preuve par snapshots reçus ni callback du payload.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Lecteur privé en lecture actuelle », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B50-SL02 — Factoriser à strict nécessaire le contrôle de réponse GovernanceResolutionV1 dans bulk_trusted_ports.py avec helper commun, conserver le comportement MappingDescriptorV1 B01, éviter tout cycle ; modification soumise à un mandat CAB distinct.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Lecteur privé en lecture actuelle », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B50-SL03 — Implémenter qualification résolue qualify liée instance/version, invocation bornée stat_private/iter_bytes par deadline UTC et asyncio.Event avec asyncio.wait, alimentation du vérificateur existant, fermeture itérateur/tâches/ressources sur toute sortie, aucun octet remis ni copie complète.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Lecteur privé en lecture actuelle », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B50-SL04 — Réussir unitaires avec provider synthétique déclaré, bornes PolicyV1 existantes, versions divergentes, authority/governance refusés, types hostiles, absence de fuite ou d'effet après refus.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Preuves », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B50-SL05 — Réussir intégration fraîche, compiler les Python concernés, prouver sous gardes l'absence d'import ORM et la non-applicabilité PostgreSQL sans test SQL artificiel, vérifier compatibilité B01.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Preuves », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B50-SL06 — Vérifier strict change/global, UTF-8/LF, cohérence et absence de modification hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Preuves », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
