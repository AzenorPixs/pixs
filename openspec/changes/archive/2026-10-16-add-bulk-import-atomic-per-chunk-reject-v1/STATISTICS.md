# Statistiques — add-bulk-import-atomic-per-chunk-reject-v1

RUN CISMP1 : `cismp-pixs-01a13bab2ed7` ; contexte CAB **191**, job `cismp1-apply-chunk-745945e0844b`. Projet : /home/devops/datas/pixs. Archive unique du 16 octobre 2026 ; publication commune **référence 30**, reçu `publication-cismp1-bulk-apc-bb54622f010149b4b2fe7d9667eb4340`.

Périmètre des compteurs : historique API natif des trois sessions de ce change et agrégat CAB du contexte 191, arrêtés avant l’édition de ce rapport. Le mandat du rapport et le gate ultérieur sont hors de cette borne ; aucun compteur autoréférentiel inventé. Les données de CISMP2/CISMP3 et des anciens changes de CISMP1 sont exclues des totaux propres. Les catégories globales de concurrence ne sont pas attribuées à CISMP1.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version native non exposée | OpenCode Go | high | 2.767 s | 222.244 | N/A — temps de génération non isolé |

393 réponses build high et 4 réponses compaction du même modèle/fournisseur : variant absent dans ces quatre métadonnées, options de l’agent de compactage high vérifiées. OpenCode 1.19.3, broker/controller CAB 1.2.1, PostgreSQL réel 160014. La version du modèle n’est pas déduite de son nom.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 | N/A — variante native non exposée | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — télémétrie non exposée |

Les moyennes du codeur portent sur les dix sondes valides, dans des sessions dédiées supprimées après mesure. Aucun dénominateur fiable du temps de service cumulé des agents : sa durée et ses pourcentages restent N/A. Busy, attente de permission, tests et durée calendaire ne sont pas du temps de génération.

## 1. Statistiques générales et décisions

Début : 2026-10-15T17:58:46.918712+00:00. Fin après archive et sonde finale : 2026-10-16T20:32:33.094612+00:00. Durée : 26 h 33 min 46 s, pauses et attentes comprises.

| Décisions CAB observées | Nombre | Part |
| --- | --- | --- |
| Approuvées | 56 | 100.0 % |
| Refusées | 0 | 0.0 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 56 | 100.0 % |

Permissions once observées : **55**. Erreurs techniques de validation CAB : 0. Une approbation ne prouve ni consommation ni succès ; les événements manquants ne sont pas reconstruits. Un **rejet natif explicite CGPT** d’une commande divergente est distinct des zéro décisions CAB refusées. Ce rejet a précédé toute exécution ; la commande exacte approuvée a ensuite consommé son unique once.

| Latence CAB observée | Effectif | Moyenne (s) | Médiane (s) | p95 (s) |
| --- | --- | --- | --- | --- |
| requestToDecision | 56 | 10.737 | 2.462 | 62.671 |
| decisionToOnce | 55 | 10.290 | 6.045 | 31.248 |
| nativeTool | 326 | 3.850 | 0.343 | 28.031 |

Quantiles : dernières 2048 observations au maximum, effectifs ci-dessus. Fenêtres observées : réservé 65385.585 s ; busy 5328.493 s ; idle 55620.248 s ; natif inconnu 5253.798 s. Ces horloges ne constituent pas une décomposition exhaustive de la durée calendaire.

| Tokens natifs déclarés, cumul des réponses | Nombre | Part du total |
| --- | --- | --- |
| Entrée hors cache | 13494764 | 11.7 % |
| Lecture cache | 101206355 | 88.0 % |
| Écriture cache | 0 | 0.0 % |
| Sortie | 222842 | 0.2 % |
| Raisonnement | 125007 | 0.1 % |
| Total | 115048968 | 100.0 % |

Le cumul d’entrée comprend les contextes réutilisés à chaque réponse et ne représente pas des tokens uniques de dépôt. Coût cumulé déclaré par l’API des sessions de travail : 1.621458910, devise N/A — non exposée dans ces métadonnées. Coût/tokens des sondes : surcharge séparée, hors consommation de production. Coût de l’orchestrateur : N/A — télémétrie absente.

| Sondes de performance | Nombre | Part des tentatives |
| --- | --- | --- |
| Valides | 10 | 90.9 % |
| Échec conservé | 1 | 9.1 % |
| Total | 11 | 100.0 % |

Une reprise immédiate unique a suivi la sonde échouée. Créneaux manqués consignés : 19 lors de l’interruption initiale, 22 pendant interruption/pause maintenance/reprise, 3 avant la sonde périodique préarchive ; aucun relevé rétrospectif. Les autres décalages coordonnés restent explicités dans le checkpoint. Compactages OpenCode du contexte : 4 observés nativement ; 3 cycles consignés dans la liste de suivi. Compactage natif Codex : N/A — API non exposée. Le benchmark PLLM échoué reste un échec : seule sa barrière a été levée par dérogation humaine explicite. Quotas fournisseur frais disponibles le 2026-10-16T20:20:38.238761+00:00 : rolling10 %, weekly63 %, monthly96 %, tous ok ; ces quotas partagés ne sont pas une consommation propre.

## 2. Types de messages et d’outils

| Rôle natif | Nombre | Part |
| --- | --- | --- |
| user | 214 | 35.0 % |
| assistant | 397 | 65.0 % |
| Total | 611 | 100.0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 482 | 23.1 % |
| step-start | 396 | 19.0 % |
| reasoning | 477 | 22.8 % |
| tool | 336 | 16.1 % |
| step-finish | 393 | 18.8 % |
| compaction | 4 | 0.2 % |
| Total | 2088 | 100.0 % |

| Terminaison des réponses assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 276 | 69.5 % |
| stop | 117 | 29.5 % |
| absent | 4 | 1.0 % |
| Total | 397 | 100.0 % |

| Outil natif | Total | Part | Terminé | Refus natif | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| bash | 50 | 14.9 % | 49 (98.0 %) | 1 (2.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 85 | 25.3 % | 84 (98.8 %) | 0 (0.0 %) | 1 (1.2 %) |
| cgpt-validation_cancel_approval | 3 | 0.9 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 15 | 4.5 % | 14 (93.3 %) | 0 (0.0 %) | 1 (6.7 %) |
| cgpt-validation_poll_approval | 7 | 2.1 % | 3 (42.9 %) | 0 (0.0 %) | 4 (57.1 %) |
| cgpt-validation_request_validation | 60 | 17.9 % | 53 (88.3 %) | 0 (0.0 %) | 7 (11.7 %) |
| edit | 2 | 0.6 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 108 | 32.1 % | 103 (95.4 %) | 0 (0.0 %) | 5 (4.6 %) |
| write | 5 | 1.5 % | 4 (80.0 %) | 0 (0.0 %) | 1 (20.0 %) |
| Total | 336 | 100.0 % | 316 (94.0 %) | 1 (0.3 %) | 19 (5.7 %) |

« Terminé » décrit un appel natif terminé ; les quatre commandes exit1 restent des résultats de contrôle/tests échoués, pas des refus de permission. Les 19 erreurs techniques comprennent les erreurs MCP, lectures et l’appel write sans champ content ; aucun effet d’écriture n’est déduit d’un appel invalide. Approbations manuelles par lecture/outils de diagnostic : N/A — non inférées d’un completed. Les décisions explicites unitaires sont le tableau CAB précédent.

## 3. Fichiers modifiés

| Artefact logique final, chemin absolu | Lignes finales | SHA-256 |
| --- | --- | --- |
| /home/devops/datas/pixs/src/pixs/backend/bulk_runtime_repository.py | 1093 | 1ba9c42eeeebaed99fd855c22591140fe2bccff10797fb3af242ccfe064bab73 |
| /home/devops/datas/pixs/src/pixs/backend/bulk_server_apply.py | 1638 | 8f8646949929d757f08af596b5caeed5869b5dd7ff36dba563670f4067fad3ad |
| /home/devops/datas/pixs/tests/unit/test_bulk_server_apply.py | 514 | 84fc35fc74a3c224801bbf370a3a83181ecce555fe906435bb239966eeba3eb9 |
| /home/devops/datas/pixs/tests/integration/test_bulk_server_apply_postgres_integration.py | 1171 | 34fdc9c7aa24533be81da33a9da77efecae565a431857fa6b5e253a92b669052 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-bulk-import-atomic-per-chunk-reject-v1/.openspec.yaml | 2 | c5936a7e8ac90455175dd905c9e8fb9d33cf82476be795f24133b51ef95c3d96 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-bulk-import-atomic-per-chunk-reject-v1/proposal.md | 9 | 1591369b5edd935a9aa8ae19ea947aed822bedd319b7f5022feb57d7af280dde |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-bulk-import-atomic-per-chunk-reject-v1/design.md | 27 | 66833d250439a2c5a036b87993414f033f330a876b5e12e7fcbc2caac8382fbd |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-bulk-import-atomic-per-chunk-reject-v1/tasks.md | 13 | 345d0ebd4606b66add0457a5b72f678ae146c9f4628824bab872dbc068b7d829 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-bulk-import-atomic-per-chunk-reject-v1/specs/bulk-operations/spec.md | 30 | 5dc52b7e4dd17d65cadcffc4204974d686b90e063dfd8aba616a6320c4616c9f |
| /home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md | 1496 | 11178aee9f1206cd47a3774c6aadb26b793262ac15bfda4e092cb5a5440f7111 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-bulk-import-atomic-per-chunk-reject-v1/STATISTIQUES.md | N/A — édition distincte après cette borne | N/A — empreinte vérifiée et conservée dans le checkpoint après écriture |

Périmètre : **11 artefacts logiques** = 4 sources/tests (36.4 %) + 5 artefacts OpenSpec déplacés (45.5 %) + 1 canon (9.1 %) + 1 rapport (9.1 %). Les cinq artefacts ont été déplacés depuis /home/devops/datas/pixs/openspec/changes/add-bulk-import-atomic-per-chunk-reject-v1/ vers l’archive ci-dessus, octets préservés ; tâches passées à 7/7 avant déplacement. Seul B07 du canon a reçu un cinquième scénario ; son requirement et quatre scénarios préexistants sont préservés. Arrondis à 0.1 point : la somme peut différer de 100 %.

| Tentatives d’édition directe observées, chemin absolu | Total | Part des 7 | Terminées | Refusées | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-import-atomic-per-chunk-reject-v1/proposal.md | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-import-atomic-per-chunk-reject-v1/design.md | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-import-atomic-per-chunk-reject-v1/tasks.md | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-import-atomic-per-chunk-reject-v1/specs/bulk-operations/spec.md | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_runtime_repository.py | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| N/A — appel write invalide sans fichier attribuable | 1 | 14.3 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_server_apply.py | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 7 | 100.0 % | 6 (85.7 %) | 0 (0.0 %) | 1 (14.3 %) |

Ce tableau compte les appels write/edit, pas les écritures effectuées par des commandes CAB gardées ni la CLI OpenSpec. Ventilation exhaustive des tentatives shell par fichier : N/A — non inférée des arguments ; leurs commandes, preuves pré/postSHA et effets sont dans native_ledger. L’édition de ce rapport est hors borne. UTF-8/LF et les 132 empreintes de la base requalifiée ont été contrôlés, avec les seuls changements/mouvements autorisés.

## 4. Commandes

| Famille de commande | Nombre | Part des 50 | Exit0 | Exit1 | Refus natif avant effet |
| --- | --- | --- | --- | --- | --- |
| Prévol CAB sans effet | 8 | 16.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Création du change OpenSpec | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 7 | 14.0 % | 4 (57.1 %) | 2 (28.6 %) | 1 (14.3 %) |
| Compilation Python | 9 | 18.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Éditions gardées et contrôles Python | 10 | 20.0 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests ordinaires | 9 | 18.0 % | 7 (77.8 %) | 2 (22.2 %) | 0 (0.0 %) |
| Qualification PostgreSQL réelle privée | 5 | 10.0 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archive et synchronisation OpenSpec | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 50 | 100.0 % | 45 (90.0 %) | 4 (8.0 %) | 1 (2.0 %) |

Ces 50 tentatives comprennent 49 exécutions natives achevées et un refus avant effet. Les quatre exit1 : premier lot unitaire avant correction (15 pass/1 fail/1 erreur), découverte générale monolithique (2054 tests,2 échecs/1 erreur), strict global préarchive et postarchive (4 warnings historiques). Les corrections et relances réussies restent visibles ; aucun échec n’est effacé.

| Commande native, libellé limité à 100 caractères | Occurrences | Part des 50 |
| --- | --- | --- |
| /usr/bin/true | 8 | 16.0 % |
| /home/devops/.local/npm/bin/openspec new change add-bulk-import-atomic-per-chunk-reject-v1 | 1 | 2.0 % |
| /home/devops/.local/npm/bin/openspec validate add-bulk-import-atomic-per-chunk-reject-v1 --strict... | 2 | 4.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile src/pixs/backend/bulk_runtime_reposito... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import hashlib,json,urllib.request from pathlib ... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,hashlib,json,urllib.request from path... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile src/pixs/backend/bulk_server_apply.py | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,hashlib,json,urllib.request from path... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile tests/unit/test_bulk_server_apply.py | 1 | 2.0 % |
| /usr/bin/env PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/pyt... | 2 | 4.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,hashlib from pathlib import Path p=Pa... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile src/pixs/backend/bulk_server_apply.py ... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,hashlib,json,urllib.request from path... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile tests/integration/test_bulk_server_app... | 5 | 10.0 % |
| /usr/bin/env PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/pyt... | 5 | 10.0 % |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 /h... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,json,hashlib,urllib.request from path... | 1 | 2.0 % |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 /h... | 4 | 8.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,json,hashlib,urllib.request from path... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,json,hashlib,urllib.request from path... | 1 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import ast,json,hashlib,urllib.request from path... | 1 | 2.0 % |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 /h... | 1 | 2.0 % |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src:tests:tests/unit PYTHONDONTWRITEBY... | 1 | 2.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --json | 2 | 4.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 | 4.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'from pathlib import Path;import hashlib;p=Path('... | 1 | 2.0 % |
| /home/devops/.local/npm/bin/openspec archive add-bulk-import-atomic-per-chunk-reject-v1 --yes | 1 | 2.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json; printf '\nNATIVE_EXIT:%s\n' ... | 1 | 2.0 % |
| Total | 50 | 100.0 % |

Commande refusée, une occurrence (2.0 % des tentatives) : `/home/devops/.local/npm/bin/openspec validate --all --strict --json; printf '\nNATIVE_EXIT:%s\n' ...`. Ajout printf non autorisé ; rejet CGPT natif per_146652f600012ZGHn31liaX1W9 avant exécution. La décision approuvée initiale non consommée a ensuite servi une seule fois à la commande exacte sans suffixe, exit1 strict conservé. Aucun réarchivage.

## 5. Accès web

| Accès web natifs codeur | Nombre | Part du domaine |
| --- | --- | --- |
| Approuvés/visités | 0 | N/A — total nul |
| Refusés | 0 | N/A — total nul |
| Erreurs | 0 | N/A — total nul |
| Total | 0 | N/A — total nul |

Aucun appel webfetch/websearch ni URL effectivement visitée par le codeur n’est enregistré dans ces trois sessions. Les appels d’orchestration locaux utilisent http://127.0.0.1:4096 et http://127.0.0.1:8788 ; les contrôles fournisseur autorisés utilisent https://opencode.ai/zen/go/v1/usage et l’API de génération OpenCode Go. Ces accès techniques ne sont pas de la navigation web. Effectifs HTTP précis de l’orchestrateur et des sondes : N/A — historique exhaustif non disponible, non reconstruits. Aucun secret ni argument d’authentification n’est reproduit. Les tentatives HTTP échouées du contrôleur sont distinctes des refus de permission.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-15T17:58:46.918712+00:00 |
| Fin — après archivage et sonde finale, avant rapport | 2026-10-16T20:32:33.094612+00:00 |
| Durée globale, pauses et attentes incluses | 26 h 33 min 46 s |

| Quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-15 17:56:00 UTC | 15 % | 2026-10-22T06:12:56+00:00 |
| Après archive | 2026-10-16T20:32:33.094609+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — relevé final indisponible | — |

Identité codex, fenêtre10080 minutes. Le relevé initial de15 % provient de l’outil natif enregistré ; l’identité privée n’est pas publiée. L’outil natif get_usage_limits/rateLimitsByLimitId n’est pas exposé dans cette reprise : aucun accès aux fichiers d’authentification, aucune estimation ni substitution par le quota Go. Les quotas sont partagés par compte ; aucune consommation exclusive n’est attribuée à ce RUN.

| Domaine des appels natifs | Nombre | Part globale | Terminés | Refus natifs | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Fichiers, write/edit | 7 | 2.1 % | 6 (85.7 %) | 0 (0.0 %) | 1 (14.3 %) |
| Commandes, bash | 50 | 14.9 % | 49 (98.0 %) | 1 (2.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils, dont MCP/lectures | 279 | 83.0 % | 261 (93.5 %) | 0 (0.0 %) | 18 (6.5 %) |
| Total | 336 | 100.0 % | 316 (94.0 %) | 1 (0.3 %) | 19 (5.7 %) |

Les taux de décisions explicites CAB portent séparément sur56 décisions :56 approuvées(100.0 %),0 refusée,0 clarification,0 attente ;55 once observées. Les 336 appels d’outils ne sont pas 336 approbations manuelles. Persistance statistique CAB : READY ; événements abandonnés : 0. Interruption globale du contrôleur : 29450.061 s inconnues, valeur globale non attribuable à ce RUN. Exclusion propre observée : 409.982 s ; file 548.433 s ; attente de référence 1003.966 s. Ces conditions peuvent se recouvrir et ne s’additionnent pas.

**Résultats prouvés** : quatre fichiers Python compilés ;17 tests unitaires ciblés réussis ;257 modules ordinaires frais,2068 tests réussis,0 skip ;35 scénarios PostgreSQL réels réussis avec rollback/CAS/baux/reprise/rejeu/annulation/expiration, suppression des schémas privés et fermeture des connexions, tables publiques stables. La composition propriétaire des tests est synthétique déclarée ; aucune capacité de provider production n’est revendiquée.

OpenSpec : strict ciblé préarchive1/1exit0 ; combiné standard79/79exit0 ; postarchive standard78/78exit0. Strict global préarchive et postarchive **exit1**,4 WARNING de longueur préexistants et **0 ERROR** : bulk-operations requirements[6],[10],[13], identity-assurance requirements[4]. Aucun succès strict global n’est annoncé. Sept tâches cochées uniquement après revue des preuves.

Archive unique, cinq artefacts déplacés sans altération, synchronisation B07 seule, publication référence30 prouvée ; exclusion libérée avant statistiques. Rapport édité sous mandat distinct et contrôlé par empreinte dans le checkpoint avant gate. La borne humaine impose ensuite gate individuel, désarmement/libération de CISMP1 et aucun prochain change. OpenCode, controller et services communs restent actifs. Aucun Git, installation de dépendance, migration de source ou modification d’infrastructure exécuté dans ce sous-lot ; aucun secret affiché ni transmis au modèle.

Preuves : checkpoint /home/devops/datas/pixs/output/cismp/cismp-pixs-01a13bab2ed7/state.json, native_ledger, pg_thirty_five_case_proof_current, ordinary_all_modules_proof_current, prearchive_review_current, archive_proof_current, strict_global_postarchive_current, standard_global_postarchive_current et publication_receipt_current. Les identifiants natifs et permissions once sont conservés dans ces preuves ; les mesures absentes restent N/A motivés.
