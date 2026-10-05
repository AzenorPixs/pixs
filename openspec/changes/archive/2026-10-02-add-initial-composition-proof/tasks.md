## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Preuve partielle bornée

- [x] 2.1 Créer `src/pixs/backend/composition_proof.py` seul, helper pur 3 textes exacts, sans FS/config/secret/attestation/compose.
- [x] 2.2 Créer `tests/unit/test_initial_composition_proof.py` avec sous-processus isolés et négatifs génériques.
- [x] 2.3 Créer `tests/integration/test_initial_composition_proof_integration.py` avec pipeline réel joint et déterminisme permutation, plus append README seul.

## 3. Preuves

- [x] 3.1 Réussir tests unitaires et d'intégration réels sous mandats CAB distincts, zéro socket/psycopg/connexion.
- [x] 3.2 Vérifier UTF-8/LF, périmètre helper + 2 tests + append seul, diagnostics sans valeur brute, conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver critères précédents et delta normatif MOTAMOT sans nouveau scenario ; autorisation CGPT d'archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
