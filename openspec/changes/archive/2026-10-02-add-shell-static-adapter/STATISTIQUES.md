# STATISTIQUES — add-shell-static-adapter

Périmètre : /home/devops/datas/pixs. Début 2026-10-01T22:37:50.647000+00:00 ; fin après archivage et sonde finale 2026-10-01T23:22:30.076997+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 2.568 s | 113.853 | 332.000 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 98 | 100 % |
| Appels outils | 50 | 100 % |
| Approuvé et exécuté | 50 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 00 h 44 min 39 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 29318103 | 92.8 % |
| cache_write | 0 | 0.0 % |
| input | 2205216 | 7.0 % |
| output | 55961 | 0.2 % |
| reasoning | 13238 | 0.0 % |
| total | 31592518 | 100 % du total API |

Coût agrégé API : 0.292997606 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 20 | 100.0 % |
| TOTAL | 20 | 100 % |

Résultats finaux : 595 tests unitaires et 167 tests intégration réussis; Chromium 154.0.8037.92 shell réel loopback: checks critiques réussis, HTTP/console zéro erreur, 21 accès navigateur autorisés, zéro externe bloqué/tenté observé, guards PG [0,0,0]. Profil supprimé, processus fermé et absence PID227197 observée, serveur fermé/thread joint. AST Python3.11 4 sources/4 extraits, UTF8 LF et 35 empreintes préservées; build Vite réel trois fichiers. Huit tâches cochées uniquement après preuves; OpenSpec strict préparation/final/aprèscochage tous valid=true failed=0. Archivage réussi sous mandat distinct skip-specs, cinq empreintes d’artefacts conservées.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 71 | 72.4 % |
| user | 27 | 27.6 % |
| TOTAL | 98 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 125 | 33.7 % |
| step-finish | 71 | 19.1 % |
| step-start | 71 | 19.1 % |
| text | 54 | 14.6 % |
| tool | 50 | 13.5 % |
| TOTAL | 371 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 27 | 38.0 % |
| tool-calls | 44 | 62.0 % |
| TOTAL | 71 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 9 | 18.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 20 | 40.0 % | 20 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 1 | 2.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 9 | 18.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 11 | 22.0 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 50 | 100 % | 50 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f06b54883ffe63YLISnmeNo8Pf | 98 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-shell-static-adapter/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-shell-static-adapter/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-shell-static-adapter/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-shell-static-adapter/specs/initial-application-bootstrap/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-shell-static-adapter/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/shell_adapter.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/check_shell_adapter_browser.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_shell_adapter_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_shell_adapter.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 10 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-shell-static-adapter. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Build frontend | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Navigateur local | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 33.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin:/home/devops/node/current/bin LANG=C.UTF-8 PYTHONPATH=/home/… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [7] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web OpenCode exécuté. Le harnais Bash a réellement visité le serveur WSGI local, séparément des outils web. Accès applicatifs loopback et CDP local, sans connexion PostgreSQL ni accès externe observé.

| Origine / chemin observé | Preuve |
|---|---|
| http://127.0.0.1:5173/ | Shell accueil 200 |
| http://127.0.0.1:5173/route-inconnue-xyz | Route TEST explicite, UI inconnue 200 |
| http://127.0.0.1:5173/assets/index-Big655uI.js | JS construit 200 |
| http://127.0.0.1:5173/assets/index-CEeMJxYe.css | CSS construit 200 |
| Réseau navigateur | {'allowed': 21, 'blockedExternal': 0, 'blockedSample': []} |
| Erreurs HTTP | 0 |
| Nettoyage | {'processClosed': True, 'profileRemoved': True} |
| Serveur / thread | [True, True] |

Recherches et évaluations fournisseur de l’orchestrateur hors production OpenCode. Volumes d’outils orchestrateur non exposés : N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-01T22:37:50.647000+00:00 |
| Fin — après archivage | 2026-10-01T23:22:30.076997+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 44 min 39 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-01T22:39:16.443508+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-01T23:22:30.076983+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 30 | 60.0 % | 30 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 9 | 18.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 11 | 22.0 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 50 | 100 % | 50 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-shell-static-adapter | 2026-10-01T22:39:16.470152+00:00 | 2026-10-01T22:39:18.891895+00:00 | 2026-10-01T22:39:22.067190+00:00 | 2.421740 | 159.669914 | 507 | réussie |
| périodique — créneau 2026-10-01T23:09:16.470152+00:00 | 2026-10-01T23:09:33.896055+00:00 | 2026-10-01T23:09:36.610418+00:00 | 2026-10-01T23:09:44.490480+00:00 | 2.714355 | 65.735442 | 518 | réussie |
| finale après archivage | 2026-10-01T23:22:22.968379+00:00 | 2026-10-01T23:22:25.536589+00:00 | 2026-10-01T23:22:30.030664+00:00 | 2.568204 | 116.152713 | 522 | réussie |

Relèves prévues : 3 (100 %) ; réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 2.421740/2.568100/2.714355 s ; débit min/moy/max : 65.735442/113.852690/159.669914 tok/s.

Surcharge sondes : 28106 tokens total API, 1547 tokens sortie, coût API 0.003129100, durées stream mesurées 15.549456 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Écarts de brouillons corrigés avant écritures: syntaxe invalide, type Path concret, argv test, bornes/collecte/fichiers symlink, import WSGI et gardes pureté placées après import. Correction d’une interprétation erronée de CGPT: le script Node avait déjà une sortie JSON monoligne; aucune fausse attribution au codeur. Deux HTTP400 contrôleur à corps vide, GET décision404 puis décision corrélée unique et opérations réussies; cause non prouvée. Une erreur ValueError CGPT de chemin relatif/absolu à la préparation des hashes d’archive, sans mutation, corrigée. Build: avertissements TanStack MODULE_LEVEL_DIRECTIVE use client; navigateur: stderr D-Bus; verdicts et nettoyages observés positifs. Aucun échec de test ou écriture hors périmètre observé dans ce change. Sonde périodique décalée de 17,426 s pour attendre le mandat unitaire en cours; créneau conservé, aucune relève rétroactive.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-shell-static-adapter, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL observée ; le test navigateur utilise HTTP loopback et CDP local. Adaptateur borné de shell statique réellement servi, validation Client et Chromium loopback ; aucune composition P0/readiness/startup/global ni production revendiquée. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
