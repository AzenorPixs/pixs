# STATISTIQUES — add-bulk-runtime-admission-fingerprint-v1

RUN cismp-pixs-758862ec875d4708 ; sessions natives ses_ed1c50eabffeGMizSctGtKy8pG, ses_ed1ba46e9ffeS2NDPqEffQfin2, ses_ed1a45b49ffe4Y5QcubmnYwg6a. Historique complet paginé : 268 messages. Intervalle arrêté après archive et sonde finale, avant rédaction du rapport.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A modèle ; OpenCode 1.19.0 observé | opencode-go mode1 | high | 2.368 s | 199.798 | N/A |

Version exacte du modèle et temps actif hors attentes/outils non exposés : N/A, aucun dénominateur de service inventé. Les moyennes proviennent seulement des sondes valides de cet agent.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex/CGPT, orchestrateur principal identifiable | N/A télémétrie du thread non exposée | N/A | N/A | N/A | N/A | N/A |

Aucune sonde de l’orchestrateur.

## 1. Statistiques générales et décisions

Durée calendaire 00 h 58 min 36 s, pauses/reprises/attentes/outils inclus. 268 messages, 984 parties, 145 appels d’outils. 25 requestId distincts avec APPROVED natif observé.

Convention : succès = outil completed, autorisé automatiquement ou explicitement ; une lecture réussie ne démontre pas une approbation manuelle. Refus = règle native explicite ou réponse MCP terminale REJECTED ; erreur = schéma/transport/interruption. Un appel de schéma rejeté avant permission ne constitue pas une écriture. Un exit1 global strict historiquement qualifié reste un exit1, pas un succès CLI. Les réponses assistant interrompues sont distinguées des erreurs d’outils.

| Modèle / raisonnement | Réponses | Entrée | Sortie | Raisonnement | Cache lu | Cache écrit | Coût natif USD |
|---|---:|---:|---:|---:|---:|---:|---:|
| muse-spark-1.3-contributor / high | 188 (100.0 %) | 1305645 (100.0 %) | 63879 (100.0 %) | 36163 (100.0 %) | 15831593 (100.0 %) | 0 (N/A) | 0.18223609 (100.0 %) |
| Total | 188 (100 %) | 1305645 (100 %) | 63879 (100 %) | 36163 (100 %) | 15831593 (100 %) | 0 (100 %) | 0.18223609 (100 %) |

Tokens/cache conservés distinctement selon télémétrie ; pas d’addition au champ total fournisseur. Erreurs de réponses assistant (catégorie distincte des outils) :

| Catégorie | Nombre | Part |
|---|---:|---:|
| MessageAbortedError | 1 | 100.0 % |
| Total | 1 | 100 % |

 Décisions MCP refusées distinctes : 1. Parties natives compaction : 0. Aucun compactage coordonné exigible avant cette fin d’intervalle ; prochaine échéance 2026-10-12T06:58:49.262204+02:00 ; API Codex non exposée.

| Sonde | État | TTMT | Tokens/s |
|---|---|---:|---:|
| début FingerprintV1 | SUCCESS | 2.312694276100956 | 108.0955327341347 |
| +30min périodique | SUCCESS | 2.453253319952637 | 258.5642503503074 |
| fin après archive FingerprintV1 | SUCCESS | 2.3367694079643115 | 232.73492675858841 |

Minimum/maximum des sondes valides : TTMT 2.313/2.453 s ; débit 108.096/258.564 tokens/s. Trois sondes réussies sur trois (100 %), zéro échec/relève manquée pendant le pilotage actif.

Sondes prévues/observées : 3, résultats {'SUCCESS': 3} ; invalides exclues des moyennes. Surcharge distincte : 2701 tokens de sortie, 0.00407390 USD, exclue des tableaux de production. Pause lors du contrôle PLLM tracée, aucun relevé reconstruit.

Incidents réconciliés : recherches initiales trop larges sans résultat exclu/écriture ; write vide rejeté par schéma avant permission ; course notification et délai MCP traités par polling du même approval_id ; réponse modèle interrompue avant toute exécution d’intégration. Commande de régressions divergente (module omis) refusée sans effet, puis38 modules couverts en deux groupes disjoints de 19. Reprises dans le même job/change, autorisations inutilisées invalidées ; écritures et preuves acquises non rejouées. Benchmark2048 expiré,4096 HTTP429,8192 réussi en high : aucune dérogation finalement nécessaire.

## 2. Types de messages et d’outils

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 188 | 70.1 % |
| user | 80 | 29.9 % |
| Total | 268 | 100 % |

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 207 | 21.0 % |
| step-finish | 187 | 19.0 % |
| step-start | 187 | 19.0 % |
| text | 258 | 26.2 % |
| tool | 145 | 14.7 % |
| Total | 984 | 100 % |

Terminaisons assistant :

| Catégorie | Nombre | Part |
|---|---:|---:|
| non fourni | 1 | 0.5 % |
| stop | 74 | 39.4 % |
| tool-calls | 113 | 60.1 % |
| Total | 188 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| bash | 15 | 10.3 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 2 | 1.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 37 | 25.5 % | 37 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 3 | 2.1 % | 2 (66.7 %) | 1 (33.3 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 26 | 17.9 % | 23 (88.5 %) | 0 (0.0 %) | 3 (11.5 %) |
| edit | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 3 | 2.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 2 | 1.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 47 | 32.4 % | 46 (97.9 %) | 0 (0.0 %) | 1 (2.1 %) |
| write | 8 | 5.5 % | 7 (87.5 %) | 0 (0.0 %) | 1 (12.5 %) |
| Total | 145 | 100 % | 139 (95.9 %) | 1 (0.7 %) | 5 (3.4 %) |

## 3. Fichiers modifiés

Tentatives d’écriture par cible absolue, pas nombre de fichiers distincts. Cible manquante d’un appel malformé non reconstruite.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-admission-fingerprint-v1/design.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-admission-fingerprint-v1/proposal.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-admission-fingerprint-v1/specs/interactions/spec.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-admission-fingerprint-v1/tasks.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_admission_fingerprint.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_admission_fingerprint_integration.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_admission_fingerprint.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| N/A — cible absente, appel rejeté par schéma | 1 | 11.1 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| Total | 9 | 100 % | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |

Quatre artefacts déplacés par archive unique vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-fingerprint-v1 (specsUpdated=false) ; trois sources Python ajoutées. Canon, façades, ORM/migrations et références existantes préservés par empreintes ; éventuels rafraîchissements externes signalés dans l’acceptation. Le présent rapport est publié sous mandat distinct après cet intervalle et exclu de ses compteurs.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| Compilation Python | 3 | 20.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 4 | 26.7 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol | 4 | 26.7 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests Python | 4 | 26.7 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 | 100 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères, troncature explicite ; les libellés tronqués identiques sont regroupés, les commandes complètes restent dans l’historique natif :

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_admission_fingerprint… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_admission_finge… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_admission_fingerprint.… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 4 | 26.7 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-a… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 13.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 2 | 13.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_admiss… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 | 100 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucun appel Bash refusé ; 1 intention de commande refusée par CAB avant toute exécution.

Demandes de commande refusées avant exécution (intentions, non ajoutées aux appels Bash ni comptées deux fois dans le total des outils) :

| Commande demandée (100 caractères max) | Nombre | Part |
|---|---:|---:|
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 1 | 100.0 % |
| Total intentions refusées | 1 | 100 % |
 Trois compilations,24 unitaires,1 intégration fraîche et322 régressions en38 modules prouvés. Aucun échec de test ; strict change sans issue ; global exit1 qualifié seulement par les3 tuples WARNING historiques exacts.

## 5. Accès web

Aucun accès webfetch/websearch :0 approuvé,0 refusé,0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Les accès fournisseur du processus dédié (authentification/quotas/benchmark) sont hors session de production, aucun secret transmis au modèle.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-12T05:49:37.239107+02:00 |
| Fin — après archivage | 2026-10-12T06:48:13.477382+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 58 min 36 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-12T05:51:22.669886+02:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-12T06:48:13.477382+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé, aucune source externe substituée. Quota partagé par le compte ; aucune variation attribuée exclusivement à ce change.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| autres | 121 | 83.4 % | 116 (95.9 %) | 1 (0.8 %) | 4 (3.3 %) |
| commandes | 15 | 10.3 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 9 | 6.2 % | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 145 | 100 % | 139 (95.9 %) | 1 (0.7 %) | 5 (3.4 %) |

347 tests sans échec et3 compilations, strict change sans issue ; global conserve3 WARNING historiques de longueur. Archive unique --skip-specs, aucun canon modifié. Primitive pure de snapshot canonique, pas d’admission/autorité/déduplicationSQL ni runtime complet. Pas de PG réel rejoué : seuls harnais isolés/inertes existants dans les régressions. Git non consulté ni modifié ; aucun déploiement ou effet externe de production ; secrets confinés au processus autorisé, jamais transmis au modèle. Fin du change puis clôture CAB/OpenCode demandée par le développeur, sans prochain change ; cycle global Pixs incomplet.
