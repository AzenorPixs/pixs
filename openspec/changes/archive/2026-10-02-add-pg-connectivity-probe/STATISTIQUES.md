# STATISTIQUES — add-pg-connectivity-probe

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T04:54:42.780009+00:00 ; fin après archivage et sonde finale 2026-10-02T13:38:16.020842+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| glm-5.3-flash | N/A — version modèle non exposée | opencode-go | high | 10.427 s | 61.251 | 1112.540 s mesurables ; part N/A |
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 5.765 s | 100.979 | 1149.678 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 289 | 100 % |
| Appels outils | 177 | 100 % |
| Approuvé et exécuté | 171 | 96.6 % |
| Refusés explicites | 2 | 1.1 % |
| Erreurs techniques/protocole | 4 | 2.3 % |
| Durée calendaire avec pauses | 08 h 43 min 33 s | 100 % de l’intervalle |

| Réponses hors outil en erreur ou interrompues | Nombre | Part des réponses assistants |
|---|---|---|
| Réponses avec champ error natif | 3 | 1.4 % |
| Dont HTTP 503 | 2 | 0.9 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 24718899 | 86.0 % |
| cache_write | 0 | 0.0 % |
| input | 3843272 | 13.4 % |
| output | 99850 | 0.3 % |
| reasoning | 88034 | 0.3 % |
| total | 28750055 | 100 % du total API |

Coût agrégé API : 0.970141134 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 39 | 97.5 % |
| EXPIRED | 1 | 2.5 % |
| TOTAL | 40 | 100 % |

Résultats finaux : Archivescope PG seul achevé, 8 tâches cochées après preuves. Suites historiques .venv : 612 unitaires OK (6.340s), 180 intégration ordinaires sans PG réel OK (4.257s), preuves API historiques re-vérifiées. PG réel après création externe de base par développeur : SELECT1 unique, exit0, ok/fermeture physique conn+curseur vrais, phaseCOMPLETE reasonNONE, Python3.14.8 Psycopg3.3.6. Échec/annulation/fermeture défaillante par doubles unitaires seulement, pas de harddeadline physique. AST3.11 3sources/5snippets, compile sémantique, UTF8LF, 73preserved et dist3 inchangés, READMEexactbase+append, 5artefacts avantarchive, delta canonique identique octets, strict avantcode et aprèscochage exit0, archivage CLI exit0 --skip-specs --yes puis5artefacts archivés exacts et absence changeactif. Global/P0/readiness/conformité runtime épinglé non revendiqués.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 215 | 74.4 % |
| user | 74 | 25.6 % |
| TOTAL | 289 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 152 | 16.5 % |
| step-finish | 212 | 22.9 % |
| step-start | 219 | 23.7 % |
| text | 164 | 17.7 % |
| tool | 177 | 19.2 % |
| TOTAL | 924 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| absent | 3 | 1.4 % |
| stop | 69 | 32.1 % |
| tool-calls | 142 | 66.0 % |
| unknown | 1 | 0.5 % |
| TOTAL | 215 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 25 | 14.1 % | 20 | 80.0 % | 2 | 8.0 % | 3 | 12.0 % |
| cgpt-validation_broker_health | 1 | 0.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 18 | 10.2 % | 18 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 3 | 1.7 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 0.6 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| cgpt-validation_poll_approval | 1 | 0.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 40 | 22.6 % | 40 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 2 | 1.1 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 13 | 7.3 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 4 | 2.3 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 59 | 33.3 % | 59 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 5.6 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 177 | 100 % | 171 | 96.6 % | 2 | 1.1 % | 4 | 2.3 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f0585b3f8ffemDsCc37O0oMydP | 50 | oui |
| ses_f04cfbeb7ffel8qZPo2131pN15 | 6 | oui |
| ses_f04b6b376ffepjkjUc0U62v3HF | 6 | oui |
| ses_f04a720e7ffedDx49JG1IexZjp | 88 | oui |
| ses_f047f06fcffes7z9xw46eQTdvz | 45 | oui |
| ses_f0366f1d2ffewTVxuNmi4rNsZm | 51 | oui |
| ses_f0342c3e0ffeGjabJTz3rTDfnI | 43 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-pg-connectivity-probe/.openspec.yaml | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pg-connectivity-probe/design.md | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pg-connectivity-probe/proposal.md | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pg-connectivity-probe/specs/initial-application-bootstrap/spec.md | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pg-connectivity-probe/tasks.md | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/pg_connectivity.py | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_pg_connectivity_integration.py | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_pg_connectivity.py | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 12 | 100 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-pg-connectivity-probe. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autre | 1 | 4.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| OpenSpec | 5 | 20.0 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 8 | 32.0 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 8 | 32.0 % | 4 | 50.0 % | 1 | 12.5 % | 3 | 37.5 % |
| Tests intégration | 2 | 8.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 25 | 100 % | 20 | 80.0 % | 2 | 8.0 % | 3 | 12.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [10] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c… | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [11] /usr/bin/timeout --signal=TERM 12s /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=… | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [12] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/python/current/bin/python3 -B -c … | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [13] /home/devops/.local/npm/bin/openspec archive add-pg-connectivity-probe --skip-specs --yes | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [1] /home/devops/.local/npm/bin/openspec validate add-pg-connectivity-probe --strict --json | 4 | 16.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/true && echo "EXIT=$?" | 1 | 4.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| [3] /usr/bin/true | 8 | 32.0 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 2 | 8.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/timeout --signal=TERM 12s /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/… | 2 | 8.0 % | 0 | 0.0 % | 0 | 0.0 % | 2 | 100.0 % |
| [7] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 4.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [8] /usr/bin/timeout --signal=TERM 12s /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/… | 1 | 4.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| [9] /usr/bin/timeout --signal=TERM 12s /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/… | 1 | 4.0 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| TOTAL | 25 | 100 % | 20 | 80.0 % | 2 | 8.0 % | 3 | 12.0 % |

Commandes refusées explicitement :

| Commande (100 caractères max) | Occurrences | Part des refus |
|---|---|---|
| /usr/bin/true && echo "EXIT=$?" | 1 | 50.0 % |
| /usr/bin/timeout --signal=TERM 12s /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home… | 1 | 50.0 % |

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Test PostgreSQL réel en lecture seule sous mandat distinct, vers le serveur local documenté ; aucun serveur HTTP ni navigateur lancé par ce change. Aucun outil web de production OpenCode exécuté. Recherche primaire CGPT séparée : 5 appels web.run réussis, documentation PostgreSQL16/libpq, Psycopg officielle et sources officielles version3.3.5, pendant sélection/conception ; non attribués au codeur ni ajoutés aux sommes de production. Évaluation fournisseur PLLM antérieure hors bornes. Autres outils orchestrateur : N/A, télémétrie complète non exposée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T04:54:42.780009+00:00 |
| Fin — après archivage | 2026-10-02T13:38:16.020842+00:00 |
| Durée globale (pauses et attentes incluses) | 08 h 43 min 33 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — préparation après sélection | 2026-10-02T05:05:49.441099+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T13:38:16.020829+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 140 | 79.1 % | 139 | 99.3 % | 0 | 0.0 % | 1 | 0.7 % |
| Commandes | 25 | 14.1 % | 20 | 80.0 % | 2 | 8.0 % | 3 | 12.0 % |
| Fichiers | 12 | 6.8 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 177 | 100 % | 171 | 96.6 % | 2 | 1.1 % | 4 | 2.3 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Modèle | Fournisseur | Raisonnement | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|---|---|---|
| initial — préparation après sélection | muse-spark-1.3-contributor | opencode-go | high | 2026-10-02T05:07:52.488128+00:00 | 2026-10-02T05:07:59.546025+00:00 | 2026-10-02T05:08:04.361786+00:00 | 7.057892 | 105.486859 | 508 | réussie |
| périodique — créneau 2026-10-02T05:37:52.488128+00:00 | muse-spark-1.3-contributor | opencode-go | high | 2026-10-02T05:39:48.314783+00:00 | 2026-10-02T05:39:55.751183+00:00 | 2026-10-02T05:39:59.500042+00:00 | 7.436393 | 135.241162 | 507 | réussie |
| prévol récupération fournisseur503 — contexte neuf | muse-spark-1.3-contributor | opencode-go | high | 2026-10-02T05:56:58.692504+00:00 | 2026-10-02T05:57:01.492229+00:00 | 2026-10-02T05:57:10.012013+00:00 | 2.799718 | 62.208077 | 530 | réussie |
| prévol candidat Go HIGH après503 — longcat-2.5-preview-free | longcat-2.5-preview-free | opencode-go | high | 2026-10-02T06:14:24.185612+00:00 | 2026-10-02T06:14:27.224945+00:00 | 2026-10-02T06:14:36.729517+00:00 | 3.039332 | N/A | 470 | échouée |
| prévol admissible TFL Go HIGH après503 — glm-5.3-flash | glm-5.3-flash | opencode-go | high | 2026-10-02T06:16:39.457712+00:00 | 2026-10-02T06:16:40.522995+00:00 | 2026-10-02T06:16:45.047523+00:00 | 1.065277 | 105.867200 | 479 | réussie |
| périodique — créneau 2026-10-02T06:07:52.488128+00:00 | glm-5.3-flash | opencode-go | high | 2026-10-02T06:28:05.525335+00:00 | 2026-10-02T06:28:06.661166+00:00 | 2026-10-02T06:28:13.281062+00:00 | 1.135828 | 72.357574 | 479 | réussie |
| périodique — créneau 2026-10-02T06:37:52.488128+00:00 | glm-5.3-flash | opencode-go | high | 2026-10-02T06:43:49.631245+00:00 | 2026-10-02T06:43:51.147237+00:00 | 2026-10-02T06:44:04.057309+00:00 | 1.515991 | 37.257735 | 481 | réussie |
| périodique — créneau 2026-10-02T07:07:52.488128+00:00 | glm-5.3-flash | opencode-go | high | 2026-10-02T07:10:42.185985+00:00 | 2026-10-02T07:10:46.603558+00:00 | 2026-10-02T07:11:00.068963+00:00 | 4.417571 | 35.572641 | 479 | réussie |
| périodique — créneau 2026-10-02T07:37:52.488128+00:00 | glm-5.3-flash | opencode-go | high | 2026-10-02T07:41:58.127329+00:00 | 2026-10-02T07:43:02.570656+00:00 | 2026-10-02T07:43:08.545799+00:00 | 64.443326 | 80.332760 | 480 | réussie |
| prévol reprise après création DB développeur — Go HIGH | glm-5.3-flash | opencode-go | high | 2026-10-02T12:23:25.077612+00:00 | 2026-10-02T12:23:26.885937+00:00 | 2026-10-02T12:23:45.815558+00:00 | 1.808322 | 25.198599 | 477 | réussie |
| périodique — créneau 2026-10-02T12:53:25.040560+00:00 | glm-5.3-flash | opencode-go | high | 2026-10-02T12:56:17.763754+00:00 | 2026-10-02T12:56:18.792793+00:00 | 2026-10-02T12:56:22.291513+00:00 | 1.029037 | 136.907134 | 479 | réussie |
| périodique — créneau 2026-10-02T13:23:25.040560+00:00 | glm-5.3-flash | opencode-go | high | 2026-10-02T13:27:46.105273+00:00 | 2026-10-02T13:27:47.360092+00:00 | 2026-10-02T13:27:57.607368+00:00 | 1.254816 | 46.548948 | 477 | réussie |
| après archivage — finale | glm-5.3-flash | opencode-go | high | 2026-10-02T13:37:05.870791+00:00 | 2026-10-02T13:37:23.048101+00:00 | 2026-10-02T13:38:05.661259+00:00 | 17.177306 | 11.217191 | 478 | réussie |

Relèves prévues : 13 (100 %) ; réussies 12 (92.3 %), échouées 1 (7.7 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 1.029037/9.261790/64.443326 s ; débit min/moy/max : 11.217191/71.182990/136.907134 tok/s.

Surcharge sondes : 121007 tokens total API, 6324 tokens sortie, coût API 0.017377850, durées stream mesurées 145.372840 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/raisonnement de chaque sonde explicités ci-dessus ; moyennes des agents calculées séparément par configuration, agrégats suivants toutes configurations valides confondues ; candidate inadmissible exclue des moyennes et de la production ; aucune sonde orchestrateur.

Incidents du périmètre : Deux réponses Muse503 sans outil projet et repli temporaire GoGLM HIGH après test admissible; candidat Free inadmissible de prévol exclu de production/moyennes valides. Deux écarts Bash antérieurs refusés sans exécution, sessions renouvelées. Trois testsPG antérieurs en échec générique, classement final DB_UNAVAILABLE, TCP accessible; arrêt global conforme à07:45:18 puis développeur a créébase, reprise12:23:25 sans opération DB par agent, intervalle inactif exclu de cadence sondes. DEVOPS changé extérieurement, seules références runtime et dépendances non sensibles transférées; ancien agent a cependant lu une portion contenant la sectionPG contreconsigne : contexte retiré et accès natif DEVOPS ensuite interdit, aucun contenu d’accès recopié dans ce rapport. PG actuel réel a réussi à12:47:17. Une transcription README a altéré un mot antérieur : contrôle byteexact a échoué, READY et nouveauCABtrue puis correction minimale files→finis seule, appendjamaisrejoué, ciblefinale byteexact vérifiée. Dernière demande checker a omis readme_before : refus contrôleur avant touteapprobation/exécution, brokerEXPIRED observé aprèspoll, READY0 puis contexte renouvelé et CABtrue; vérificateur SHA256 inchangé exécuté ensuite exit0. QuelquesHTTP400 transitoires sans décision stockée avant approbation unique, un gate409 pending1 nonvalidé jusqu’au READY0 réel; codeRoot de préparationprompt en erreur syntaxe avant touteAPI/écriture puis corrigé. Assertions de rapport reflow et sessionsdistinctes retirées explicitement : deltaexactoctets et unit/int mêmeSID sousmandatsdistincts. Aucun Git, déploiement, installation ou mutation PG métier/configpersistante.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-pg-connectivity-probe, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Un incident de lecture native DEVOPS incluant la section PG contreconsigne est déclaré ci-dessus ; le contexte a été retiré et aucune donnée d’accès n’est reproduite dans ce rapport. Le chargement autorisé pour les tests réels reste limité à trois variables en mémoire du seul processus de test, sans impression ni artefact de credentials. Connexion réelle locale et SELECT 1 autorisés et observés ; aucune installation ni mutation métier/config persistante. Sonde ASYNC PG SELECT 1 seule ; credentials processus caller ; délais bornés et fermeture ; aucune disponibilité globale revendiquée. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
