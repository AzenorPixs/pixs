# STATISTIQUES — add-initial-liveness-view

Périmètre : /home/devops/datas/pixs. Début 2026-10-01T21:31:53.057578+00:00 ; fin après archivage et sonde finale 2026-10-01T22:02:21.774264+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 9.348 s | 70.332 | 99.504 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 86 | 100 % |
| Appels outils | 46 | 100 % |
| Approuvé et exécuté | 46 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 00 h 30 min 28 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 13855266 | 97.8 % |
| cache_write | 0 | 0.0 % |
| input | 289321 | 2.0 % |
| output | 25629 | 0.2 % |
| reasoning | 3746 | 0.0 % |
| total | 14173962 | 100 % du total API |

Coût agrégé API : 0.062517632 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 17 | 100.0 % |
| TOTAL | 17 | 100 % |

Résultats finaux : 590 tests unitaires et 165 tests d’intégration réussis ; syntaxe AST Python 3.11 des sources et extraits exécutables, UTF-8/LF, contenu exact des trois sources et de la documentation, 24 empreintes préservées ; delta identique au bloc normatif validé ; huit tâches cochées sur preuves ; validations OpenSpec strictes avant et après cochage réussies ; archivage natif avec --skip-specs réussi, cinq empreintes inchangées, change actif absent. Aucun résultat global P0, readiness, PostgreSQL réel, route publique distribuée ou cycle CISMP complet n’est revendiqué.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 66 | 76.7 % |
| user | 20 | 23.3 % |
| TOTAL | 86 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 99 | 31.2 % |
| step-finish | 66 | 20.8 % |
| step-start | 66 | 20.8 % |
| text | 40 | 12.6 % |
| tool | 46 | 14.5 % |
| TOTAL | 317 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 20 | 30.3 % |
| tool-calls | 46 | 69.7 % |
| TOTAL | 66 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 7 | 15.2 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 2 | 4.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 17 | 37.0 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 2.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 10 | 21.7 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 9 | 19.6 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 46 | 100 % | 46 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f06b54883ffe63YLISnmeNo8Pf | 86 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-liveness-view/.openspec.yaml | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-liveness-view/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-liveness-view/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-liveness-view/specs/initial-application-bootstrap/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-liveness-view/tasks.md | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/liveness_view.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_liveness_view_integration.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_liveness_view.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 10 | 100 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-01-add-initial-liveness-view. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 57.1 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 7 | 100 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 42.9 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 14.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 7 | 100 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucune URL visitée par l’agent de codage dans cet intervalle, aucun outil web exécuté. Les recherches techniques de l’orchestrateur et l’évaluation fournisseur PLLM restent hors de la télémétrie de production OpenCode ; elles sont déclarées séparément et ne sont pas attribuées au codeur. Volumes d’outils orchestrateur non exposés dans cette télémétrie : N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-01T21:31:53.057578+00:00 |
| Fin — après archivage | 2026-10-01T22:02:21.774264+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 30 min 28 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-01T21:31:53.057578+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-01T22:02:21.774251+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 29 | 63.0 % | 29 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 7 | 15.2 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 10 | 21.7 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 46 | 100 % | 46 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-initial-liveness-view | 2026-10-01T21:32:04.436287+00:00 | 2026-10-01T21:32:20.511889+00:00 | 2026-10-01T21:32:30.240247+00:00 | 16.075603 | 54.582685 | 531 | réussie |
| fin — après archivage | 2026-10-01T22:02:12.758889+00:00 | 2026-10-01T22:02:15.380129+00:00 | 2026-10-01T22:02:21.525452+00:00 | 2.621235 | 86.081615 | 529 | réussie |

Relèves prévues : 2 (100 %) ; réussies 2 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 2.621235/9.348419/16.075603 s ; débit min/moy/max : 54.582685/70.332150/86.081615 tok/s.

Surcharge sondes : 19270 tokens total API, 1060 tokens sortie, coût API 0.002192600, durées stream mesurées 15.873691 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Incidents d’orchestration : une première réponse HTTP 400 Validation inconnue avant présence de décision stockée ; le même mandat toujours non consommé a ensuite reçu une décision unique corrélée et l’écriture native a réussi. Une erreur de concaténation Path/str lors d’un contrôle en lecture après cochage a été corrigée sans rejouer l’écriture. Aucun échec de test ou outil natif dans ce périmètre.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-01-add-initial-liveness-view, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ni réseau applicatif dans les tests observés. Vue liveness uniquement, réponse réellement traitée, aucun état readiness/startup/P0/global. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
