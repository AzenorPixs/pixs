## 1. Préparation et implémentation

- [x] 1.1 Fournir quatre artefacts cohérents, delta MODIFIED B03 verbatim sans règle nouvelle ; réussir la validation strict du change avant code.
- [x] 1.2 Ajouter validate_publisher_contract, constantes et export dans src/pixs/backend/bulk_trusted_ports.py, sans modifier les validateurs existants ni compose_bulk_trusted_ports.
- [x] 1.3 Étendre tests/unit/test_bulk_trusted_ports.py par des preuves de non-invocation, refus None/méthode absente/non-Python/propriété/getattr hostile sans hooks ni écho, et acceptation des méthodes Python explorables selon le mécanisme existant.
- [x] 1.4 Compiler séparément les deux fichiers avec le Python .venv du projet ; exécuter les tests unitaires ports et contrats runtime avec le mécanisme unittest existant.
- [x] 1.5 Vérifier strict change sans issue, validation globale OpenSpec sans nouvelle issue (trois WARNING de longueur préexistants qualifiés), UTF-8/LF, delta canonique verbatim, cadrages cohérents et seuls fichiers attendus modifiés.

## Procédure après preuves

Cocher ces tâches seulement après leurs preuves. Sous exclusion intégration, revalider la référence commune puis archiver une seule fois avec --skip-specs. Publier STATISTIQUES.md par un mandat distinct, vérifier six sections, UTF-8/LF et totaux, avant gate, désarmement, libération et retour SÉLECTION du parent CISMP.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Procédure après preuves ».

### B47-SL01 — Fournir quatre artefacts cohérents, delta MODIFIED B03 verbatim sans règle nouvelle ; réussir la validation strict du change avant code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation et implémentation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B47-SL02 — Ajouter validate_publisher_contract, constantes et export dans src/pixs/backend/bulk_trusted_ports.py, sans modifier les validateurs existants ni compose_bulk_trusted_ports.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation et implémentation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B47-SL03 — Étendre tests/unit/test_bulk_trusted_ports.py par des preuves de non-invocation, refus None/méthode absente/non-Python/propriété/getattr hostile sans hooks ni écho, et acceptation des méthodes Python explorables selon le mécanisme existant.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Préparation et implémentation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B47-SL04 — Compiler séparément les deux fichiers avec le Python .venv du projet ; exécuter les tests unitaires ports et contrats runtime avec le mécanisme unittest existant.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Préparation et implémentation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B47-SL05 — Vérifier strict change sans issue, validation globale OpenSpec sans nouvelle issue (trois WARNING de longueur préexistants qualifiés), UTF-8/LF, delta canonique verbatim, cadrages cohérents et seuls fichiers attendus modifiés.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Préparation et implémentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
