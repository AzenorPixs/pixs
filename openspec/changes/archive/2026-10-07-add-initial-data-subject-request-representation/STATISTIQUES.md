# Statistiques de session — add-initial-data-subject-request-representation

- run_id : `cismp-pixs-20261007-061019` ; session : `ses_eeb040777ffeOEz0loy7R2EtC0` ; archive : `openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation`.
- Périmètre : reprise du 7 octobre ; historique complet de production de cette session avant rédaction du rapport ; phases du 6 octobre hors comptages, histoire native de ces sessions indisponible. Code déjà créé avant ce RUN, vérifié inchangé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash / qwen3.8-flash | N/A (absente de la télémétrie) | opencode-go | xhigh | 2,4518 s | 68,93 | N/A — durées assistant incluent attentes CAB et outils ; télémétrie de génération active insuffisante |

OpenCode 1.18.34. Agent unique identifié sur la spécification.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex /root (famille GPT-6 déclarée par plateforme) | N/A | OpenAI | N/A | N/A | N/A | N/A — pas de télémétrie modèle exploitable ; lecture native du thread tronquée, historique quantifiable indisponible |

## 1. Statistiques générales et décisions

Durée calendaire (pauses, attentes CAB, tests et archivage inclus) : 00 h 30 min 26,254 s. Bornes : début calendaire 2026-10-07T06:10:19.912Z ; début de collecte 2026-10-07T06:16:55.727955+00:00 ; début de production 2026-10-07T06:17:49.530Z ; fin 2026-10-07T06:40:46.166Z (après archivage, avant rédaction). Le temps de service des agents n'est pas la durée calendaire.

| Mesure générale | Valeur | Part |
|---|---:|---:|
| Messages totaux | 74 | 100 % |
| — user | 16 | 21,6 % |
| — assistant | 58 | 78,4 % |
| Décisions CAB explicites | 13 | 100 % |
| — APPROVED | 13 | 100,0 % |
| — REJECTED | 0 | 0,0 % |
| — needs_clarification | 0 | 0,0 % |
| reviewer | Codex /root | — |

Tokens et coût de production : input 348, output 23 223, reasoning 0, cache_read 4 059 249, cache_write 69 775, coût 0,089870 (devise N/A — non publiée par la télémétrie consultée). Compactions : N/A (aucune trace dans les données agrégeées). Quotas mode1 (06:12:54Z) : rolling 5, weekly 65, monthly 52.

Résultats de développement : 49 tests réussis (unitaires 15 : 30,6 % ; intégration 1 : 2,0 % ; régression bornée 33 : 67,3 %, dénominateur 49) ; 3 compilations py_compile exit 0 ; stricts change et spec exit 0 ; globaux exit 1 natif réels QUALIFIÉS (76/77 items, 19 WARNING, 0 ERROR, identité exacte de la baseline) ; 127 empreintes de baseline contrôlées, dérive 0 ; écritures de sources 0.

### Sondes TTMT et débit de l'agent de codage

| Position | Tentative | Valide | Lignes | Tokens | TTMT (s) | Tokens/s | Coût |
|---|---:|---|---:|---:|---:|---:|---:|
| début | 1 | non | 1 | 360 | 2,8505 | 57,05 | 0,002913 |
| début | 2 (reprise unique) | oui | 40 | 497 | 3,1882 | 68,56 | 0,000454 |
| fin | 1 | oui | 40 | 565 | 1,7155 | 69,30 | 0,003009 |

Horodatages d’envoi UTC et identifiants d’audit : début tentative 1, 2026-10-07T06:16:55.727955Z, `ses_eeafdfd64ffeaRIyByf0APzDYr` / `msg_115020304001F3IUOL7dn1630o` ; début tentative 2, 2026-10-07T06:17:04.997012Z, `ses_eeafdd938ffeOwPFlP20ApAD84` / `msg_11502272b00146QhYoithquEs4` ; fin, 2026-10-07T06:39:23.083355Z, `ses_eeae96e75ffeCjsU3qLR8WiEl4` / `msg_115169209001PEuEwrAAcZbRk5`. Durée totale de la sonde invalide : N/A (non conservée) ; TTMT mesuré 2,8505 s.

Moyennes sur sondes valides (n=2) : TTMT 2,4518 s ; débit 68,93 tokens/s. Min/max : TTMT 1,7155–3,1882 s ; débit 68,56–69,30 tokens/s. Relèves : prévues 2, réussies 2, échouées 0, manquées 0 ; tentatives 3, valides 2 (66,7 %), invalides 1 (33,3 %) ; intervalle 1800 s ; aucun créneau +30 min atteint entre la sonde initiale et la fin du change, aucune sonde rétroactive recréée ; collecte stoppée. Surcharge de télémétrie, hors production : 360 tokens, 0,002913 pour la sonde invalide exclue des moyennes ; 1 422 tokens et 0,006376 pour les 3 tentatives.

## 2. Types de messages et d'outils

Parties (total 267, dénominateur de la ligne) :

| Type de partie | Effectif | Part |
|---|---:|---:|
| text | 39 | 14,6 % |
| step-start | 58 | 21,7 % |
| reasoning | 58 | 21,7 % |
| tool | 54 | 20,2 % |
| step-finish | 58 | 21,7 % |
| Total | 267 | 100 % |

Terminaisons des 58 réponses assistant : tool-calls 42 (72,4 %), stop 16 (27,6 %).

Outils (total 54 appels ; convention : un appel « completed » n'implique pas une approbation manuelle — les 13 approbations CAB explicites couvrent les 13 request_validation, et les 12 bash sont des exécutions après `APPROVED`) :

| Outil | Effectif | Part |
|---|---:|---:|
| read | 17 | 31,5 % |
| cgpt-validation_request_validation | 13 | 24,1 % |
| bash | 12 | 22,2 % |
| grep | 5 | 9,3 % |
| glob | 4 | 7,4 % |
| edit | 1 | 1,9 % |
| cgpt-validation_broker_readiness | 1 | 1,9 % |
| cgpt-validation_list_pending | 1 | 1,9 % |
| Total | 54 | 100 % |

Les pourcentages sont arrondis à une décimale ; leur somme peut différer de 100 % de 0,2 point.

## 3. Fichiers modifiés

| Chemin absolu | Tentatives d'écriture | Approuvées | Refusées | Erreur |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation/tasks.md | 1 (100 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |

Une seule invocation d'édition, six cases `[ ] → [x]` exactement (tâches 1.1–1.6 prouvées), autres octets inchangés. Source d'origine : /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-representation/tasks.md. Aucune écriture de code source : les trois fichiers livrés sont vérifiés inchangés et UTF-8/LF — /home/devops/datas/pixs/src/pixs/kernel/data_subject_request.py, /home/devops/datas/pixs/tests/unit/test_data_subject_request.py, /home/devops/datas/pixs/tests/integration/test_data_subject_request_integration.py.

Déplacement d'archivage (5 fichiers, 100 % effectués par la commande archive autorisée) :
- /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation/.openspec.yaml
- /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation/proposal.md
- /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation/design.md
- /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation/tasks.md
- /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-subject-request-representation/specs/data-governance/spec.md

## 4. Commandes

12 commandes natives exécutées, toutes sous mandat CAB `APPROVED` distinct : exit 0 sur 10 (83,3 %), exit 1 natif réel sur 2 (16,7 %) — les globaux qualifiés (couverture 76/77, 19 WARNING/0 ERROR, identité exacte des issues et totaux historiques), jamais comptés comme exit 0. Aucun refus, aucune erreur technique d'exécution. Libellés tronqués à 100 caractères quand nécessaire (indiqué `…`).

| Famille | Effectif | Part | exit 0 | exit 1 |
|---|---:|---:|---:|---:|
| py_compile (3 fichiers) | 3 | 25,0 % | 3 | 0 |
| Exécutions de tests | 3 | 25,0 % | 3 | 0 |
| openspec validate stricts ciblés | 2 | 16,7 % | 2 | 0 |
| openspec validate globaux | 2 | 16,7 % | 0 | 2 |
| openspec archive --help | 1 | 8,3 % | 1 | 0 |
| openspec archive du change | 1 | 8,3 % | 1 | 0 |
| Total | 12 | 100 % | 10 | 2 |

Détail (requestId → commande, exit) :

- cismp-pixs-20261007-061019-syntax-source-01 → /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_subject_request.py → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-syntax-unit-02 → /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_subject_request.py → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-syntax-integration-03 → /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_subject_request_i… → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-unit-test-04 → /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0] = ["src", "tests/unit"] impo… → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-integration-test-05 → /home/devops/python/current/bin/python3 -B tests/integration/test_data_subject_request_integration.… → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-regression-bounded-06 → /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0] = ["src", "tests/unit", "tes… → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-openspec-change-final-07 → /home/devops/.local/npm/bin/openspec validate add-initial-data-subject-request-representation --str… → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-openspec-spec-final-08 → /home/devops/.local/npm/bin/openspec validate data-governance --type spec --strict → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-openspec-global-specs-09 → /home/devops/.local/npm/bin/openspec validate --specs --strict --json --report findings → exit 1 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-openspec-global-all-10 → /home/devops/.local/npm/bin/openspec validate --all --strict --json --report findings → exit 1 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-archive-contract-help-11 → /home/devops/.local/npm/bin/openspec archive --help → exit 0 ; 1 occurrence (8,3 % des 12 commandes)
- cismp-pixs-20261007-061019-archive-approved-change-12 → /home/devops/.local/npm/bin/openspec archive add-initial-data-subject-request-representation --yes … → exit 0 ; 1 occurrence (8,3 % des 12 commandes)

Commandes refusées : aucune (0, 0 %).

## 5. Accès web

Agent de codage (sur les 54 appels OpenCode) : 0 accès web, part globale 0,0 %. Résultats : 0 approuvé, 0 refusé, 0 erreur ; taux internes N/A (dénominateur nul).

Orchestrateur, hors des 54 appels OpenCode, identification séparée : 2 accès HTTP autorisés et exécutés par le processus sécurisé (100 % ; 0 refusé, 0 erreur) :
- https://opencode.ai/zen/go/v1/usage (approuvé/exécuté — évaluation PLLM sécurisée native, hors comptages OpenCode)
- https://opencode.ai/zen/go/v1/messages (approuvé/exécuté — idem)

Aucune URL n'est présentée comme visitée par l'agent lui-même.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-07 06:10:19.912Z (UTC) |
| Fin — après archivage | 2026-10-07 06:40:46.166Z (UTC) |
| Durée globale (pauses et attentes incluses) | 00 h 30 min 26 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A | N/A — relevé initial absent | N/A |
| Après — après archivage de la spécification | N/A | N/A — lecture impossible | N/A |
| Différence après − avant | — | N/A | — |

Cause : l'outil natif `mcp__codex_app__get_usage_limits` est absent des outils exposés de cette session ; fenêtres et compte non vérifiables ; aucune valeur reconstituée. Quotas mode1 relevés par l'orchestrateur (06:12:54Z) : rolling 5, weekly 65, monthly 52. Les quotas étant partagés par le compte, une différence eût pu inclure d'autres tâches ; exclusivité non vérifiable.

Agrégation des domaines sur les 54 appels d'outils OpenCode :

| Domaine | Appels | Part globale | Approuvés/exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| Éditions de fichiers | 1 | 1,9 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| Commandes natives (bash) | 12 | 22,2 % | 10 exit 0 (83,3 %) | 0 (0 %) | 0 technique (0 %) ; 2 exit 1 qualifiés (16,7 %) |
| Accès web | 0 | 0,0 % | N/A (aucun) | N/A | N/A |
| Autres outils (read/grep/glob/CAB) | 41 | 75,9 % | 41 (100 %) | 0 (0 %) | 0 (0 %) |
| Total | 54 | 100 % | 52 retours réussis (96,3 %) | 0 (0 %) | 0 technique (0 %) ; 2 retours non nuls qualifiés (3,7 %) |

Pourcentages internes des commandes : 10 exit 0 (83,3 %), 2 exit 1 natifs réels qualifiés (16,7 %), distincts des erreurs techniques (0). Les décisions CAB : 13/13 APPROVED (100 %), 0 rejet, 0 clarification, aucune décision réutilisée.

Conclusion vérifiable : tests 49 réussis (15+1+33) et 3 compilations exit 0 ; stricts ciblés exit 0 ; globaux exit 1 qualifiés selon la règle de design.md (19 WARNING/0 ERROR, baseline 127 empreintes inchangées) ; delta identique au canon ; archivage réussi (exit 0, `--skip-specs` justifié par l'absence de changement normatif, validation conservée) ; tâches 1.1–1.6 cochées sur preuves sous mandat distinct ; aucune écriture de sources. Git : non inspecté, aucun commit ni push. Navigateur et PostgreSQL : non nécessaires à cette représentation pure, aucun test de base exécuté. Secrets : le secret PLLM a été utilisé exclusivement par le processus sécurisé (quotas/performance/auth native), jamais transmis au modèle, affiché, journalisé ni écrit aux sources. Périmètre fonctionnel : la représentation livrée reste partielle et interne — aucun traitement autorisé, audité, idempotent ou propagé, ni le scénario « Effacement propagé », ne sont livrés par ce change.

### Notes de protocole

- Le statut `completed` des 54 outils ne recouvre pas les retours natifs : les deux exit 1 globaux sont comptés séparément comme retours non nuls qualifiés, jamais comme exit 0.
- Les bornes premier/dernier événement SSE ne sont pas conservées comme horodatages bruts dans les relevés ; TTMT et débit mesurés réellement par horloge monotone ; ces bornes valent N/A.
- Phase de rédaction du présent rapport et écritures futures exclues des bornes closes.
- Données communes au lot : non applicables (rapport par archive unique).
