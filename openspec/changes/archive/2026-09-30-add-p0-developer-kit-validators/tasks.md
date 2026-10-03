# Tasks — add-p0-developer-kit-validators

## 1. Façade et sanitisation

- [x] 1.1 `src/pixs/developer_kit/validators.py` : `validate_manifest_text/file`, délégation noyau seul via ports publiés, sanitisation fermée champ/règle + repli, `TypeError` mésusage, erreurs lecture/Unicode/TOML en refus sans valeur. (validators01/02/03 ; relectures intégrales)
- [x] 1.2 Façade publique du rapport : `ValidationReport` défini dans `validators.py` et réexporté par `src/pixs/developer_kit/__init__.py` (anti-cycle, décision CGPT), frozen slots + `__post_init__` ssi, exports bornés, imports sans FS ni activation, docstring limites (pas de Kit complet, pas de conformité production). (init01 ; relecture 28 lignes)
- [x] 1.3 `src/pixs/developer_kit/README.md` : parcours local borné (écrire → valider → lire diagnostics), sans secret/réseau/production. (readme01 ; relecture 50 lignes)

## 2. Tests

- [x] 2.1 `tests/unit/test_developer_kit_validators.py` : enveloppe, immuabilité, sanitisation, adversariaux sans affichage de fixtures. (unit01/02 ; 19 méthodes)
- [x] 2.2 `tests/integration/test_developer_kit_example.py` : exemple P0 validé via le kit, mémoire seule. (integration01/02 ; 7 méthodes)
- [x] 2.3 Tests ciblés 100 % : 19/19 unitaires (unittest02, exit 0) puis 7/7 intégration (integrationtest01, exit 0), `PYTHONPATH=src`, `python3 -B`, chemins absolus DEVOPS. Incident : unittest01 18/19 (brut `TOML invalide` découpé), corrigé validators03, retest 19/19.
- [x] 2.4 Régressions globales 100 % : 380 unit (globalunit01, exit 0) + 125 intégration (globalintegration01, exit 0), sans régression des suites existantes.

## 3. Validations

- [x] 3.1 AST Python du périmètre : 4 fichiers compilent sans erreur. (ast02, exit 0)
- [x] 3.2 UTF-8/LF des 10 fichiers du périmètre, absence de modification hors scope, matrice cadrages/delta exact (delta MODIFIED `developer-experience` : recopie exacte `Parcours local reproductible` + `Diagnostics sans fuite` et leurs scénarios canoniques, aucune exigence nouvelle ; `component-model` en dépendance réutilisée, pas en capacité modifiée). (ast02 : `utf8_lf_files: 10`, `delta_exact: true`, `kernel_imports_public: true` ; AST01 REJECTED avant tout Bash, récupéré recovery02)
- [x] 3.3 `openspec validate --all --strict` : 77 passed, 0 failed, 14 INFO non bloquantes ; change valide. (validatechange01 + validateall01, exit 0)

NOTE de pilotage (pas une tâche d'implémentation) : l'archivage du change et les statistiques restent des mandats CAB distincts à venir, non prouvés pré-archive ; jamais les déclarer faits. Aucune affirmation de Kit complet ni de P0 global.
