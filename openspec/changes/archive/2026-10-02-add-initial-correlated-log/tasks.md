## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Journal local borné

- [x] 2.1 Créer src/pixs/backend/correlated_log.py seul, parse 00 strict et émission unique vers sink caller, sans FS/config/secret/global/compose.
- [x] 2.2 Créer tests/unit/test_correlated_log.py avec subprocess isolés et négatifs génériques sans brut.
- [x] 2.3 Créer tests/integration/test_correlated_log_integration.py avec pipeline réel joint et mêmes IDs sur trois composants, plus append README seul.

## 3. Preuves

- [x] 3.1 Réussir tests unitaires et intégration réels sous mandats CAB distincts, zéro socket/psycopg/connexion hors sink caller.
- [x] 3.2 Vérifier AST 3.11 UTF-8/LF, périmètre 3 sources plus append seul, diagnostics sans valeur brute, matrice et conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver critères précédents et delta normatif MOTAMOT sans nouveau scenario ; autorisation CGPT d archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
