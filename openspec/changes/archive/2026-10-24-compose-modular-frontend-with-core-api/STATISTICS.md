# Statistiques de la session C11

Change : compose-modular-frontend-with-core-api. RUN : cismp3-pixs-c4b2bfe2c6614f3f. Session native : ses_e9aee1487ffeMYlvAO9vuYRysx. Job : job-resume-ce4c194c548a4090ad2f52894e9c34d4.
Archive unique prouvée : /home/devops/datas/pixs/openspec/changes/archive/2026-10-24-compose-modular-frontend-with-core-api. Rapport préparé après archivage ; la rédaction, sa vérification, la mise à jour finale de tasks.md et la clôture CAB sont hors de la borne statistique 2026-10-24 01:07:19 CEST.

Le brouillon GET /runs/<runId>/statistics?format=markdown et ses exports JSON filtrés ont été consultés en premier. Les contextes609 et899 sont deux périodes disjointes du même RUN et du même SID ; aucun chiffre global des autres RUN n’est imputé à C11. L’historique natif API complet disponible contient 2978 messages, sous la limite5000 ; les sondes dédiées sont séparées. Le checkpoint conserve commandes, sorties, identifiants, empreintes et exports sans recopier ici les contenus sensibles.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go (opencode-go) | high ; métadonnée absente sur19 messages historiques | 2.7317 s,2 sondes SSE complètes | 399.6071, moyenne arithmétique de2 sondes | N/A — durée de génération par agent absente |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex, famille GPT-6 | N/A — version exacte non exposée | OpenAI | N/A — télémétrie non exposée | N/A — non sondé | N/A — non sondé | N/A — durée de génération absente |

Aucun sous-agent de délégation n’a été lancé dans cette reprise. Le temps busy, les attentes CAB, les outils et la durée calendaire ne sont pas assimilés au temps de génération. Le dénominateur de service cumulé est N/A ; aucun pourcentage de service n’est estimé. Mode1 et Muse/high conservés selon instruction du développeur, sans réinitialisation des contextes ou des services.

## 1. Statistiques générales et décisions

Durée calendaire : 27 h 43 min 23 s, pauses et attentes incluses. Intervalle vérifiable de création de la session native à la lecture finale du quota après archive. Les appels terminés sans erreur sont classés « réussis » ; cela inclut les lectures automatiquement autorisées et ne prouve pas une approbation manuelle. Un appel MCP techniquement terminé peut porter une décision métier refusée : ces décisions sont comptées séparément. Les permissions explicitement refusées sont distinctes des erreurs techniques et des codes de sortie de tests.

| Décisions CAB, deux contextes | Nombre | Part |
|---|---:|---:|
| Approuvées | 228 | 98,7 % |
| Refusées | 3 | 1,3 % |
| Clarification | 0 | 0,0 % |
| En attente | 0 | 0,0 % |
| Total | 231 | 100 % |

Permissions once observées : 224 ; erreurs techniques du compteur de décisions : 0. Les décisions, appels d’outils, émissions once et commandes ne sont pas des dénominateurs identiques. Les refus de schéma avant admission et les tentatives HTTP sont conservés à part dans les exports CAB ; aucun refus n’est transformé en exécution.

| Messages natifs | Nombre | Part |
|---|---:|---:|
| user | 1236 | 41,5 % |
| assistant | 1742 | 58,5 % |
| Total | 2978 | 100 % |

| Télémétrie de requêtes de production | Valeur |
|---|---:|
| Tokens total | 562530998 |
| Tokens input | 27913527 |
| Tokens output | 1226426 |
| Tokens reasoning | 435003 |
| Tokens cache.read | 532956042 |
| Tokens cache.write | 0 |
| Compactions natives achevées ou marquées summary dans l’historique | 17 |
| Somme du champ coût OpenCode déclaré | 4.189550584 sur1742 messages |
| Coût facturé réel et répartition du crédit fournisseur | N/A — non exposés |

Les compteurs de tokens sont cumulés par réponse, avec cache de contexte répété ; ils ne mesurent ni des tokens uniques ni une consommation convertible en prix. Le champ total n’est pas additionné une seconde fois aux sous-compteurs. Un coût déclaré nul ne prouve pas la gratuité. Les durées actives et parallèles CAB peuvent se recouvrir ; pas d’addition en temps de génération. La compaction principale Codex n’est pas exposée par API : N/A, checkpoint préservé ; compactions OpenCode et prévols frais prouvés séparément.

| Collecte des sondes, occurrences tracées | Nombre | Part des occurrences tracées |
|---|---:|---:|
| Exécutées avec bornes texte SSE complètes | 2 | 4,2 % |
| Historiques exclues des moyennes faute de borne dernier delta conservée | 36 | 75,0 % |
| Manquées explicitement enregistrées | 10 | 20,8 % |
| Total tracé | 48 | 100 % |

Le nombre de relèves théoriques sur toute la durée, interruptions incluses, est N/A : la couverture de cadence n’est pas complète. Les relèves manquées ne sont pas recréées. Les anciens débits utilisaient parfois la fin du polling HTTP au lieu du dernier token ; ils restent dans le checkpoint et sont exclus, sans masquer cette limite. Les moyennes ci-dessus portent uniquement sur les deux sondes dont les bornes SSE sont enregistrées. Les métriques de production et de l’orchestrateur restent N/A lorsqu’elles ne sont pas disponibles.

| Sonde dédiée | TTMT | Débit tokens/s | Sortie tokens | Deltas texte |
|---|---:|---:|---:|---:|
| 2026-10-24 00:53:14 CEST — complémentaire réelle ; échéance 22:29 manquée | 4.076031 | 242.702914 | 328 | 41 |
| 2026-10-24 01:06:19 CEST — fin après archive avant statistiques | 1.387380 | 556.511331 | 328 | 41 |

TTMT min/max : 1.387380/4.076031 s ; débit min/max : 242.702914/556.511331. Les deux sorties sont exactement les entiers1–160, sans outil ; première et dernière sorties texte SSE, tokens réels et paramètres Muse/high sont conservés. Ces sondes ne font pas partie des compteurs de production. Leur sortie connue est656 tokens au total ; coût et surcharge complète des sondes historiques N/A faute de télémétrie exhaustive validée.

## 2. Types de messages et d’outils

| Catégorie | Total | Part | Réussis | Refusés | Erreurs | En cours |
|---|---:|---:|---:|---:|---:|---:|
| bash | 97 | 5,3 % | 94 (96,9 %) | 2 (2,1 %) | 1 (1,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 256 | 14,0 % | 255 (99,6 %) | 0 (0,0 %) | 1 (0,4 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 343 | 18,8 % | 342 (99,7 %) | 0 (0,0 %) | 1 (0,3 %) | 0 (0,0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 0,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_cancel_approval | 1 | 0,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 28 | 1,5 % | 28 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 257 | 14,1 % | 256 (99,6 %) | 0 (0,0 %) | 1 (0,4 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 12 | 0,7 % | 9 (75,0 %) | 0 (0,0 %) | 3 (25,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 238 | 13,0 % | 211 (88,7 %) | 0 (0,0 %) | 27 (11,3 %) | 0 (0,0 %) |
| edit | 80 | 4,4 % | 79 (98,8 %) | 0 (0,0 %) | 1 (1,2 %) | 0 (0,0 %) |
| glob | 36 | 2,0 % | 36 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 22 | 1,2 % | 21 (95,5 %) | 0 (0,0 %) | 1 (4,5 %) | 0 (0,0 %) |
| question | 1 | 0,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 402 | 22,0 % | 398 (99,0 %) | 0 (0,0 %) | 4 (1,0 %) | 0 (0,0 %) |
| write | 51 | 2,8 % | 51 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total appels natifs | 1825 | 100,0 % | 1783 (97,7 %) | 2 (0,1 %) | 40 (2,2 %) | 0 (0,0 %) |

| Type de partie native | Nombre | Part |
|---|---:|---:|
| compaction | 17 | 0,2 % |
| reasoning | 2055 | 20,7 % |
| step-finish | 1737 | 17,5 % |
| step-start | 1739 | 17,5 % |
| text | 2551 | 25,7 % |
| tool | 1825 | 18,4 % |
| Total parties | 9924 | 100 % |

| Fin de réponse ou métadonnée absente | Nombre | Part |
|---|---:|---:|
| absent | 1241 | 41,7 % |
| tool-calls | 1071 | 36,0 % |
| stop | 666 | 22,4 % |
| Total messages | 2978 | 100 % |

La ligne « absent » comprend notamment les messages utilisateurs ; elle n’est pas une erreur de réponse. Les outils CAB ne décident pas : l’orchestrateur examine le mandat et rend la décision. Les erreurs d’outil et les tentatives HTTP rejetées ne sont pas des échecs de test produit par défaut.

## 3. Fichiers modifiés

Le tableau compte les tentatives natives edit/write du SID, par chemin absolu ; il ne prétend pas compter des lignes modifiées ni déduire les fichiers affectés par une commande Bash. Les écritures par commande et l’archivage sont identifiés séparément. Les chemins sont conservés intégralement ; les pourcentages portent sur les tentatives de ce tableau.

| Catégorie | Total | Part | Réussis | Refusés | Erreurs | En cours |
|---|---:|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/CHANGELOG.md | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/README.md | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/README.md | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/package.json | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/build_frontend_composition.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/build_frontend_plan.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/build_frontend_selection.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/composition-imports-v1.mjs | 4 | 3,1 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/composition-syntax-v1.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/composition_requirements_v1.py | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/frontend_composition_bridge.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/pixs-composition-plugin-v1.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/prepare_frontend_composition.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/presentation-profile-v1.mjs | 3 | 2,3 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/scripts/run_frontend_build.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/catalogs.js | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/main.js | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/api-v1.js | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/composition-descriptor-v1.js | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/composition-graph-v1.js | 3 | 2,3 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/composition-runtime-v1.js | 4 | 3,1 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/presentation-adapter-v1.js | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/presentation-contract-v1.js | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/presentation-fields-v1.js | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/shell/session-runtime-v1.js | 3 | 2,3 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/src/theme.css | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/assert-adapter.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/catalog-browser.mjs | 8 | 6,1 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/runner.html | 8 | 6,1 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composed-pipeline.test.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composed-submodule.test.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composition-graph-integration.test.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composition-graph.test.mjs | 3 | 2,3 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composition-imports.test.mjs | 3 | 2,3 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composition-runtime.test.mjs | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/composition-syntax.test.mjs | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/presentation-adapter.test.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/presentation-contract.test.mjs | 3 | 2,3 % | 2 (66,7 %) | 0 (0,0 %) | 1 (33,3 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/presentation-fields.test.mjs | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/presentation-profile.test.mjs | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/session-runtime.test.mjs | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/shell-contracts.test.mjs | 4 | 3,1 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/test_build_composition.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/test_build_frontend_plan.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/test_build_selection.py | 6 | 4,6 % | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/tests/test_composition_requirements.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/frontend/vite.config.js | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/compose-modular-frontend-with-core-api/VALIDATION.md | 7 | 5,3 % | 7 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/compose-modular-frontend-with-core-api/design.md | 4 | 3,1 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/compose-modular-frontend-with-core-api/requirements.md | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/compose-modular-frontend-with-core-api/tasks.md | 9 | 6,9 % | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/auth/shell_context.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api_core_openapi.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api_core_views.py | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api_module_openapi.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api_module_views.py | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api_shell_context.py | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api_shell_transports.py | 1 | 0,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total tentatives natives edit/write | 131 | 100,0 % | 130 (99,2 %) | 0 (0,0 %) | 1 (0,8 %) | 0 (0,0 %) |

Chemins distincts : 59. Déplacement autorisé : openspec/changes/compose-modular-frontend-with-core-api vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-24-compose-modular-frontend-with-core-api. Aucun second archivage. Les artefacts temporaires/cache/profils sont régénérables et ont été nettoyés selon les reçus. Le présent rapport sera produit par un mandat séparé après la borne ; il n’est pas inclus dans ces tentatives. Les effets Bash ne sont pas arbitrairement répartis sur des fichiers.

## 4. Commandes

Familles des appels Bash natifs, libellés limités à100 caractères. Les résultats ci-dessous sont ceux des appels natifs : un appel terminé peut contenir une sortie de test non nulle ; seul le reçu fonctionnel final fait foi pour le verdict produit. Le contrôle de pins arrêté avant recette, les premiers échecs de harnais puis leurs corrections sont conservés dans le checkpoint.

| Catégorie | Total | Part | Réussis | Refusés | Erreurs | En cours |
|---|---:|---:|---:|---:|---:|---:|
| Node.js | 33 | 34,0 % | 32 (97,0 %) | 1 (3,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| OpenSpec | 9 | 9,3 % | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Prévol /usr/bin/true | 19 | 19,6 % | 18 (94,7 %) | 1 (5,3 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python | 22 | 22,7 % | 21 (95,5 %) | 0 (0,0 %) | 1 (4,5 %) | 0 (0,0 %) |
| npm frontend | 14 | 14,4 % | 14 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total commandes natives | 97 | 100,0 % | 94 (96,9 %) | 2 (2,1 %) | 1 (1,0 %) | 0 (0,0 %) |

| Commande refusée nativement, non exécutée | Occurrences | Part des refus natifs |
|---|---:|---:|
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/cur… | 1 | 50,0 % |
| /usr/bin/true | 1 | 50,0 % |
| Total refus natifs de commande | 2 | 100 % |

Un mandat d’archive divergent a été refusé avant permission/Bash : entrée read ajoutée à un parent write, puis nouveau manifeste examiné. La commande d’archive finalement exécutée est réussie et l’ancienne demande n’a pas été rejouée. Les autres refus CAB et schémas invalident seulement leurs tentatives ; aucune approbation consommée n’a été recyclée.

## 5. Accès web

| Périmètre mesuré | Approuvés/exécutés | Refusés | Erreurs | Part |
|---|---:|---:|---:|---:|
| Outils web natifs OpenCode recensés | 0 (N/A) | 0 (N/A) | 0 (N/A) | N/A — aucun appel |
| Total natif OpenCode | 0 (N/A) | 0 (N/A) | 0 (N/A) | N/A — dénominateur nul |

Root a consulté des références officielles et la recette locale avec CUA. Le nombre exhaustif de requêtes HTTP, ressources secondaires ou tentatives refusées Root est N/A : les compteurs CAB ne collectent pas ces URL et ne couvrent pas les outils Root. Les URL attestées ci-dessous sont des destinations consultées, pas des compteurs de requêtes. Aucun URL refusé n’est établi ; N/A pour leur inventaire complet.

| URL attestée, ≤100 caractères | Statut et périmètre |
|---|---|
| https://www.w3.org/TR/WCAG22/ | Consulté — référence des seuils, pas un test produit |
| https://gnome.pages.gitlab.gnome.org/orca/help/introduction.html | Consulté — référence Orca |
| https://help.gnome.org/gnome-help/a11y-screen-reader.html.pa | Consulté — aide GNOME |
| http://127.0.0.1:14902/ | Visité CUA — shell STANDALONE réel |
| http://127.0.0.1:14902/__c11_a11y | Visité CUA — harnais des cinq primitives, deux serveurs ensuite fermés |

Les recettes C14 ont effectué14 transactions HTTP200 par moteur vers un serveur HTTPS loopback temporaire ; hôte/port exacts des anciennes relèves non conservés ici : N/A. Le bypass de chaîne TLS était limité aux profils jetables de test ; aucune garantie de TLS déployé n’est revendiquée. Aucun secret n’est ajouté à cette liste.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — création native du SID | 2026-10-22 21:23:55 CEST |
| Fin — après archivage et sonde finale, relevé quota | 2026-10-24 01:07:19 CEST |
| Durée globale, pauses et attentes incluses | 27 h 43 min 23 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A — horodatage précis non conservé dans le relevé initial | 4 % | 2026-10-29 18:09:38 CET |
| Après — après archivage de la spécification | 2026-10-24 01:07:19 CEST | 17 % | 2026-10-30 22:13:45 CET |
| Différence après − avant | — | N/A — fenêtres de réinitialisation différentes | — |

Les relevés proviennent du quota natif codex, fenêtre10080 minutes. Le relevé initial reste conservé indépendamment. Les quotas sont partagés par le compte et peuvent inclure d’autres chats ; aucune consommation exclusive C11 n’est déduite. Une réinitialisation distincte entre les bornes interdit de soustraire les deux pourcentages, même si le compte est resté le même. Aucune réinitialisation ni achat de crédit n’a été déclenché par cette clôture.

| Catégorie | Total | Part | Réussis | Refusés | Erreurs | En cours |
|---|---:|---:|---:|---:|---:|---:|
| Fichiers — appels edit/write | 131 | 7,2 % | 130 (99,2 %) | 0 (0,0 %) | 1 (0,8 %) | 0 (0,0 %) |
| Commandes — Bash | 97 | 5,3 % | 94 (96,9 %) | 2 (2,1 %) | 1 (1,0 %) | 0 (0,0 %) |
| Web natif OpenCode | 0 | 0,0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils — lecture, recherche, CAB et question | 1597 | 87,5 % | 1559 (97,6 %) | 0 (0,0 %) | 38 (2,4 %) | 0 (0,0 %) |
| Total global appels natifs | 1825 | 100,0 % | 1783 (97,7 %) | 2 (0,1 %) | 40 (2,2 %) | 0 (0,0 %) |

Validation produit finale :133 Node,106 Python,75 AST/import/profil,6 raccords réels,16 compilations Python,145 cas Chromium et145 Firefox, deux builds et8 chargements DOM MODULE/SUBMODULE PASS dans leurs périmètres. Ces résultats se chevauchent et ne sont pas additionnés en scénarios uniques. Après deux modifications Core concurrentes, requalification fraîche réelle HTTPS/PostgreSQL :15 critères et14 HTTP200 par moteur,266 empreintes stables avant/après, nettoyage complet.

Accessibilité : clavier Root, contraste Light/Dark mesuré, reflow320 et mouvements réduits observés ; compte rendu humain A à E OK avec Orca48.1, AT-SPI2 2.56.2, GNOME Wayland et navigateur intégré de Codex, y compris zoom natif200 %. Version exacte du moteur intégré N/A car non exposée. Les échantillons ne constituent pas une certification exhaustive de profils/contributions non sélectionnés.

Archive unique réussie : msg_16b037d9400110PyaqbqHRjjAN / prt_16b0385f6001oCycEoVjDmBj6Q, exit0. Avertissements non bloquants conservés : proposition en français et9/10 tâches au moment d’archiver ;3.4 reste liée au présent rapport et sera cochée après sa vérification. Zéro delta canonique volontaire, --skip-specs ; dernier OpenSpec strict ciblé PASS. Publication et gate CAB seront vérifiés après ce rapport et gardent leurs reçus dans le checkpoint, jamais déduits de sa seule présence.

Bilan documentaire : README.md, frontend/README.md, src/pixs/backend/api/README.md, CHANGELOG.md et design.md concernés ; PROJECT.md, TECHNICAL.md et BUILD.md relus, cohérents et inchangés. AGENTS.md, DEVOPS.md et protocole préservés. Aucun Git, commit, push, branche ou déploiement ; aucun autre change engagé. Aucun fichier sensible exclu ouvert ni secret transmis au modèle selon les opérations examinées ; chargement PostgreSQL par les seuls processus de test. La revue bornée n’est pas une recherche exhaustive de secrets sur tout le dépôt. OpenCode et les services CAB partagés restent ouverts.

Preuves : /home/devops/datas/pixs/output/cismp/cismp3-pixs-c4b2bfe2c6614f3f/state.json ; VALIDATION.md et tasks.md dans cette archive. Les sources et métriques absentes sont N/A motivées. Le rapport décrit l’intervalle fixé avant sa rédaction ; sa vérification, la publication durable, le gate et la libération ciblée seront des étapes de clôture distinctes.
