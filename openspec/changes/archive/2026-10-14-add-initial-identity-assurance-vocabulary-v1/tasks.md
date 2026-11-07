# Tasks — add-initial-identity-assurance-vocabulary-v1

- [x] Créer le seul fichier tests/unit/test_identity_assurance.py avec unittest et stdlib existante, sans dépendance nouvelle.
- [x] Tester en unitaire la fermeture exacte CLAIMED, VERIFIED, PROOFED avec type et littéral, le refus FOREIGN, None et absence sans défaut, et l'absence d'ordre intrinsèque.
- [x] Créer le seul fichier tests/integration/test_identity_assurance_integration.py avec unittest et stdlib existante.
- [x] Tester en intégration l'import frais et l'identité nominale avec consommateurs authz ; bloquer imports de modules DB non déjà chargés, sockets et écritures observables, sans invocation des ports horloge, audit ou auth ; noter que l'import lit nécessairement des modules Python.
- [x] Vérifier les régressions identité et authz et la préservation des garanties existantes.
- [x] Compiler chacun avec py_compile, contrôler UTF-8 et fins de ligne LF, vérifier production et façades existantes inchangées par contrôle des contenus et empreintes, sans inspection Git.
- [x] Exécuter les validations OpenSpec applicables sans affirmer de strict sans observation ; seule alerte de longueur canonique exacte acceptée.
- [x] Préparer l'archivage du change et le rapport STATISTIQUES, sans Git.

## Preuves de qualification avant archivage

- Tests dédiés : 6 unitaires et 1 intégration fraîche, codes natifs 0.
- Régressions identité/authz : 91 tests, code natif 0 ; total réussi 98.
- Syntaxe : py_compile de chacun des deux fichiers, deux codes natifs 0.
- UTF-8/LF et contenus natifs vérifiés ; production et façades existantes inchangées par empreintes, sans inspection Git.
- Validation ciblée stricte du change préparé : 1/1, code natif 0 ; contrôle final et global à réexécuter avant publication.
- Incident de lancement : import pixs absent du venv, résolu par PYTHONPATH=src limité au processus après prévol neuf ; aucun changement source.
- Archivage prévu sous exclusion avec --skip-specs : canon déjà identique préservé. Rapport STATISTIQUES.md séparé après archive et collecte finale ; aucune preuve d’archive ou de rapport n’est anticipée ici.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves de qualification avant archivage ».

### C78-SL01 — Créer le seul fichier tests/unit/test_identity_assurance.py avec unittest et stdlib existante, sans dépendance nouvelle.

- Ancien repère et tâche rattachée : tâche sans numéro « Créer le seul fichier tests/unit/test_identity_assurance.py avec unittest et stdlib existante, sans dépendance nouvelle. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL02 — Tester en unitaire la fermeture exacte CLAIMED, VERIFIED, PROOFED avec type et littéral, le refus FOREIGN, None et absence sans défaut, et l'absence d'ordre intrinsèque.

- Ancien repère et tâche rattachée : tâche sans numéro « Tester en unitaire la fermeture exacte CLAIMED, VERIFIED, PROOFED avec type et littéral, le refus FOREIGN, None et absence sans défaut, et l'absence d'ordre intrinsèque. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL03 — Créer le seul fichier tests/integration/test_identity_assurance_integration.py avec unittest et stdlib existante.

- Ancien repère et tâche rattachée : tâche sans numéro « Créer le seul fichier tests/integration/test_identity_assurance_integration.py avec unittest et stdlib existante. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL04 — Tester en intégration l'import frais et l'identité nominale avec consommateurs authz ; bloquer imports de modules DB non déjà chargés, sockets et écritures observables, sans invocation des ports horloge, audit ou auth ; noter que l'import lit nécessairement des modules Python.

- Ancien repère et tâche rattachée : tâche sans numéro « Tester en intégration l'import frais et l'identité nominale avec consommateurs authz ; bloquer imports de modules DB non déjà chargés, sockets et écritures observables, sans invocation des ports horloge, audit ou auth ; noter que l'import lit nécessairement des modules Python. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL05 — Vérifier les régressions identité et authz et la préservation des garanties existantes.

- Ancien repère et tâche rattachée : tâche sans numéro « Vérifier les régressions identité et authz et la préservation des garanties existantes. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL06 — Compiler chacun avec py_compile, contrôler UTF-8 et fins de ligne LF, vérifier production et façades existantes inchangées par contrôle des contenus et empreintes, sans inspection Git.

- Ancien repère et tâche rattachée : tâche sans numéro « Compiler chacun avec py_compile, contrôler UTF-8 et fins de ligne LF, vérifier production et façades existantes inchangées par contrôle des contenus et empreintes, sans inspection Git. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL07 — Exécuter les validations OpenSpec applicables sans affirmer de strict sans observation ; seule alerte de longueur canonique exacte acceptée.

- Ancien repère et tâche rattachée : tâche sans numéro « Exécuter les validations OpenSpec applicables sans affirmer de strict sans observation ; seule alerte de longueur canonique exacte acceptée. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C78-SL08 — Préparer l'archivage du change et le rapport STATISTIQUES, sans Git.

- Ancien repère et tâche rattachée : tâche sans numéro « Préparer l'archivage du change et le rapport STATISTIQUES, sans Git. » ; section « Tasks — add-initial-identity-assurance-vocabulary-v1 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
