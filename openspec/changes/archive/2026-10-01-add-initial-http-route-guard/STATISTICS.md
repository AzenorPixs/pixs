# STATISTIQUES — add-initial-http-route-guard

Périmètre : /home/devops/datas/pixs. Début 2026-10-01T19:40:28.738516+00:00 ; fin après archivage et sonde finale 2026-10-01T21:17:38.448072+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 2.590 s | 144.766 | 382.584 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 219 | 100 % |
| Appels outils | 131 | 100 % |
| Approuvé et exécuté | 127 | 96.9 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 4 | 3.1 % |
| Durée calendaire avec pauses | 01 h 37 min 09 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Le true hors mandat du premier maître reste une erreur de protocole malgré exit0.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 18274389 | 94.5 % |
| cache_write | 0 | 0.0 % |
| input | 988232 | 5.1 % |
| output | 57231 | 0.3 % |
| reasoning | 26731 | 0.1 % |
| total | 19346583 | 100 % du total API |

Coût agrégé API : 0.152164378 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties). Permission native explicitement rejetée par CGPT : 1, per_0f94823dd001AGwVyFhrI3tsRB ; l’outil ayant déjà été aborté, son résultat API demeure erreur technique, sans doublage dans la colonne refus.

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 34 | 97.1 % |
| EXPIRED | 1 | 2.9 % |
| TOTAL | 35 | 100 % |

Résultats finaux : 586 tests unitaires et 163 tests d’intégration réussis ; syntaxe source et snippets Python3.11, UTF-8/LF, trois contenus exacts et 21 empreintes préservées ; strict OpenSpec avant/après cochage ; huit tâches prouvées et cochées, archivage réel. Le premier essai unitaire a échoué (deux erreurs), puis correction minimale sur preuve et succès. Corrections de noms des nouveaux fichiers uniquement, API publiques inchangées.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 166 | 75.8 % |
| user | 53 | 24.2 % |
| TOTAL | 219 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 279 | 33.0 % |
| step-finish | 165 | 19.5 % |
| step-start | 166 | 19.6 % |
| text | 105 | 12.4 % |
| tool | 131 | 15.5 % |
| TOTAL | 846 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| absent | 1 | 0.6 % |
| stop | 52 | 31.3 % |
| tool-calls | 113 | 68.1 % |
| TOTAL | 166 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 19 | 14.5 % | 16 | 84.2 % | 0 | 0.0 % | 3 | 15.8 % |
| cgpt-validation_broker_readiness | 16 | 12.2 % | 16 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 2 | 1.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 0.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 7 | 5.3 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 35 | 26.7 % | 35 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 0.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 3 | 2.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| invalid | 1 | 0.8 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| read | 34 | 26.0 % | 34 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 12 | 9.2 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 131 | 100 % | 127 | 96.9 % | 0 | 0.0 % | 4 | 3.1 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f0714292dffeCF0DSvmDD9qs4U | 39 | oui |
| ses_f06f547f7ffemSE4AmO03mycOl | 134 | oui |
| ses_f06b54883ffe63YLISnmeNo8Pf | 46 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-http-route-guard/.openspec.yaml | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-http-route-guard/design.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-http-route-guard/proposal.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-http-route-guard/specs/initial-application-bootstrap/spec.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-http-route-guard/tasks.md | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/http_route_guard.py | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_initial_http_route_guard_integration.py | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_initial_http_route_guard.py | 3 | 23.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 13 | 100 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 8 chemins distincts (100.0 %). Archivage distinct par commande : openspec/changes/archive/2026-10-01-add-initial-http-route-guard. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 21.1 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 6 | 31.6 % | 5 | 83.3 % | 0 | 0.0 % | 1 | 16.7 % |
| Python vérification | 2 | 10.5 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| Tests intégration | 3 | 15.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 4 | 21.1 % | 3 | 75.0 % | 0 | 0.0 % | 1 | 25.0 % |
| TOTAL | 19 | 100 % | 16 | 84.2 % | 0 | 0.0 % | 3 | 15.8 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 15.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/true | 6 | 31.6 % | 5 | 83.3 % | 0 | 0.0 % | 1 | 16.7 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 2 | 10.5 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 2 | 10.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 2 | 10.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [7] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 5.3 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| [8] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [9] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 19 | 100 % | 16 | 84.2 % | 0 | 0.0 % | 3 | 15.8 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final ; la commande de syntaxe différente a été abortée puis sa permission rejetée par CGPT, preuve per_0f94823dd001AGwVyFhrI3tsRB conservée dans le RUN. L’outil aborté est classé erreur technique.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | 100 % | 0 | N/A | 0 | N/A | 0 | N/A |

Aucune URL visitée par l’agent de codage dans cet intervalle, aucun outil web exécuté. Les recherches techniques de l’orchestrateur et l’évaluation fournisseur PLLM restent hors de la télémétrie de production OpenCode ; elles sont déclarées séparément et ne sont pas attribuées au codeur. Vérification technique orchestrateur : sources officielles GitHub anomalyco/opencode v1.18.34, chemins permission et session (accès approuvés lecture seule ; volumes d’outils orchestrateur N/A).

Accès techniques orchestrateur hors comptage production, URL distinctes de référence (libellés ≤100 caractères, effectif global orchestrateur N/A) :

| URL | Statut observé |
|---|---|
| https://raw.githubusercontent.com/anomalyco/opencode/v1.18.34/packages/opencode/src/permission/inde… | Approuvé, contenu lu |
| https://raw.githubusercontent.com/anomalyco/opencode/v1.18.34/packages/opencode/src/session/prompt.… | Approuvé, contenu lu |
| https://raw.githubusercontent.com/anomalyco/opencode/v1.18.34/packages/opencode/src/session/llm/req… | Approuvé, contenu lu |
| https://raw.githubusercontent.com/anomalyco/opencode/v1.18.34/packages/opencode/src/tool/registry.ts | Approuvé, contenu lu |
| https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/permission/next.ts | Erreur HTTP404, contenu non lu |

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-01T19:40:28.738516+00:00 |
| Fin — après archivage | 2026-10-01T21:17:38.448072+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 37 min 09 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-01T19:40:28.738527+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-01T21:17:38.448072+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 99 | 75.6 % | 98 | 99.0 % | 0 | 0.0 % | 1 | 1.0 % |
| Commandes | 19 | 14.5 % | 16 | 84.2 % | 0 | 0.0 % | 3 | 15.8 % |
| Fichiers | 13 | 9.9 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 131 | 100 % | 127 | 96.9 % | 0 | 0.0 % | 4 | 3.1 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-initial-http-route-guard | 2026-10-01T19:40:41.537270+00:00 | N/A — champ non conservé | N/A — champ non conservé | 2.845775 | 191.513175 | 489 | réussie |
| +30 min — relève réelle différée, horodatage conservé | 2026-10-01T20:11:43.486128+00:00 | N/A — champ non conservé | N/A — champ non conservé | 2.223234 | 197.147458 | 489 | réussie |
| +90 min — relève réelle | 2026-10-01T21:11:02.702957+00:00 | 2026-10-01T21:11:05.737168+00:00 | 2026-10-01T21:11:10.555513+00:00 | 3.034210 | 106.883117 | 515 | réussie |
| fin — après archivage | 2026-10-01T21:16:56.556169+00:00 | 2026-10-01T21:16:58.811070+00:00 | 2026-10-01T21:17:05.156771+00:00 | 2.254896 | 83.521049 | 530 | réussie |

Relèves prévues : 5 (100 %) ; réussies 4 (80.0 %), échouées 0 (0.0 %), manquées 1 (20.0 %). +30 réelle différée, horaire conservé. +60 manquée pendant interruption/reprise daemon, jamais reconstruite rétroactivement.

TTMT min/moy/max : 2.223234/2.589529/3.034210 s ; débit min/moy/max : 83.521049/144.766200/197.147458 tok/s.

Surcharge sondes : 41060 tokens total API, 2023 tokens sortie, coût API 0.004451252, durées stream mesurées 16.197779 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents conservés : true hors cible par premier maître (sans écriture), parsing racine incorrect de summary OpenSpec corrigé sans réexécution, fixture unitaire échappée corrigée sur échec observé, expiration d’un mandat pendant interruption daemon sans écriture, qualification prématurée du contrôle final pending1 corrigée puis READY0, tour ancien à outils deny puis ancien manifeste inféré à tort, commande de syntaxe reformulée bloquée par permission ASK et refusée. Changements de sessions/contrats CAB purement techniques, sans clôture globale CISMP. Aucun mandat consommé rejoué.

Archivage : openspec/changes/archive/2026-10-01-add-initial-http-route-guard, preuves dans le RUN parent. Git non inspecté et aucun commit/push autorisé ou effectué. Aucun secret lu ; aucune installation/dépendance, aucune connexion PostgreSQL ou réseau applicatif dans les tests observés, gardes à zéro. Ce jalon prouve seulement la déclaration et le refus des routes, sans publier de route ni attester toute la norme HTTP ou le cycle CISMP complet.
