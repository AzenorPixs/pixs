## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et perimetre CGPT.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Classificateur pur

- [x] 2.1 Creer src/pixs/backend/health_classifier.py seul, API classify_health exacte, quatre types separes, PG obligatoire, limite interne 256, refus ValueError("Invalid health snapshot") from None, sans IO ni import Django ni execution de sonde.
- [x] 2.2 Creer tests/unit/test_health_classifier.py avec objets doubles, matrices quatre types, PG obligatoire, optionnels, combos startup/alive, types et repr hostile, grand tuple 257 et objet hostile en premier element, sans reseau ni PG reel ni assertion de temps.
- [x] 2.3 Creer tests/integration/test_health_classifier_integration.py sans reseau, subprocess frais avec gardes IO/sockets/SQL et sans import Django, plus append README seul.

## 3. Preuves

- [x] 3.1 Reussir tests unitaires puis integration sans reseau sur l'executable DEVOPS actuel sous mandats distincts, determinisme et gardes prouves sans fake hard deadline.
- [x] 3.2 Verifier AST 3.11 UTF-8 LF, perimetre 3 sources plus append seul, comptages baseline CGPT exacts, diagnostics sans valeur brute, strict apres preuves, matrice et conformite finale avant tout cochage.
- [x] 3.3 Prouver criteres precedents et delta normatif MOTAMOT sans nouveau scenario ; archivage et statistiques distincts apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.
