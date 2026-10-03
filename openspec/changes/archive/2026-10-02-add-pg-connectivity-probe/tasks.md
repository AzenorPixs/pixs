## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et perimetre CGPT.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Sonde ASYNC bornee

- [x] 2.1 Creer src/pixs/backend/pg_connectivity.py seul, SELECT 1 ASYNC borne avec fermeture avant cancel, sans secret journalise ni DDL.
- [x] 2.2 Creer tests/unit/test_pg_connectivity.py avec doubles cooperatifs et negatifs generiques sans PG reel.
- [x] 2.3 Creer tests/integration/test_pg_connectivity_integration.py avec PG reel borne et vars processus seul, plus append README seul.

## 3. Preuves

- [x] 3.1 Reussir tests unitaires sans PG puis integration PG reelle sous mandats distincts, fermeture prouvee sur succes echec et annulation.
- [x] 3.2 Verifier AST 3.11 UTF-8 LF, perimetre 3 sources plus append seul, diagnostics sans valeur brute, matrice et conformite finale avant tout cochage.
- [x] 3.3 Prouver criteres precedents et delta normatif MOTAMOT sans nouveau scenario ; archivage distinct apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.
