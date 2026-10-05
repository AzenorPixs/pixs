# STATISTIQUES — add-initial-feature-flag-definitions

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T23:25:55.076894+00:00 ; fin après archivage et sonde finale 2026-10-03T00:46:32.071657+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

Baseline de ce change : 144 hashes pris avant préparation, tous préservés avant et après archivage. Les 200 tests sont les résultats finaux réellement réussis ; la première exécution unitaire échouée reste incluse dans les outils/erreurs de production. Syntaxe minimale 3.11 vérifiée par AST, compilation et tests réels effectués sous 3.14.8, aucune exécution Python 3.11 revendiquée. CAB : 20 mandats documentés par observation SSE directe à partir de la première publication de source ; réconciliation HTTP demandes/rapports toutes les 2 secondes. Rédaction/analyses OC contrôlées à pauses fixes de 7 secondes. Sondes toutes les 30 minutes à la prochaine frontière sûre, sans attente du créneau ; sonde finale distincte après archive.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| qwen3.8-flash | N/A — version modèle non exposée | opencode-go | N/A | N/A | N/A | 119.590 s mesurables ; part N/A |
| qwen3.8-flash | N/A — version modèle non exposée | opencode-go | xhigh | 2.710 s | 91.345 | 810.868 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | N/A — version modèle non exposée | OpenAI | high | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 157 | 100 % |
| Appels outils | 72 | 100 % |
| Approuvé et exécuté | 69 | 95.8 % |
| Refusés explicites | 1 | 1.4 % |
| Erreurs techniques/protocole | 2 | 2.8 % |
| Durée calendaire avec pauses | 01 h 20 min 36 s | 100 % de l’intervalle |

| Réponses en erreur ou interrompues | Nombre | Part assistants |
|---|---|---|
| Champ error natif non vide | 0 | 0.0 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 10782254 | 91.1 % |
| cache_write | 970588 | 8.2 % |
| input | 678 | 0.0 % |
| output | 82139 | 0.7 % |
| reasoning | 0 | 0.0 % |
| total | 11835659 | 100 % du total API |

Coût agrégé API : 0.405340694 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 1 (part 0.2 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 27 | 96.4 % |
| EXPIRED | 1 | 3.6 % |
| TOTAL | 28 | 100 % |

Résultats finaux : 200 tests réussis sous Python 3.14.8 : 24 unitaires, 1 intégration nouvelle sous gardes causales, 175 de régression. py_compile des trois fichiers (module/unitaire recompilés après correction), AST minimale 3.11 des trois parents et enfant, baseline144 préservée, delta R1 literal seul, strict pré-cochage réussi. Aucun runtime de fanions ni R3 capabilities livré. Preuves finales : unit cismp-pixs-20261001-d377c79e3f33 ; intégration cismp-pixs-20261001-aaefbe04e5fd ; régression cismp-pixs-20261001-020c4cf28aef ; checker cismp-pixs-20261001-51cb60abce79 ; strict post-cochage cismp-pixs-20261001-548aae12ffb1 ; archive cismp-pixs-20261001-15c28a1c578b. Les deux erreurs techniques/protocole comprennent le test unitaire échoué et une tentative Bash pendant la proposition en lecture seule, outil indisponible et classé invalid avant exécution, distincts du refus natif de commande non identique.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 113 | 72.0 % |
| user | 44 | 28.0 % |
| TOTAL | 157 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| compaction | 1 | 0.2 % |
| reasoning | 113 | 22.6 % |
| step-finish | 113 | 22.6 % |
| step-start | 113 | 22.6 % |
| text | 88 | 17.6 % |
| tool | 72 | 14.4 % |
| TOTAL | 500 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 43 | 38.1 % |
| tool-calls | 70 | 61.9 % |
| TOTAL | 113 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 27 | 37.5 % | 25 | 92.6 % | 1 | 3.7 % | 1 | 3.7 % |
| cgpt-validation_broker_readiness | 6 | 8.3 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 1 | 1.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 1 | 1.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 28 | 38.9 % | 28 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 2 | 2.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 1.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| invalid | 1 | 1.4 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| read | 5 | 6.9 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 72 | 100 % | 69 | 95.8 % | 1 | 1.4 % | 2 | 2.8 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f022b133fffe9xGy4geWvAaJN6 | 157 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 0 chemins distincts (N/A). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-initial-feature-flag-definitions. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

Effets fichiers des commandes :

| Chemin absolu complet | Mandat exact | SHA observé | Convention de comptage |
|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definitions/.openspec.yaml | cismp-pixs-20261001-1706d2b75c43 | 5f734986346dad86a56f91476441377d77de7b13c8917bcc685059135d55fe75 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definitions/proposal.md | cismp-pixs-20261001-60f9f0478623 | 7c4c49d92c1f62d03c465aeeebe585016c7fe4339ef6637a455c680941ccb4e3 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definitions/specs/feature-flags/spec.md | cismp-pixs-20261001-1477be36cb9e | 68c9dbfb3dc5ab8a90119d974c333f80b0539a643f3ae4977761e9f326b69fff | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definitions/design.md | cismp-pixs-20261001-450040ddb17d | c3d62f072910438d4ed98cb8e5a8d164c9a7e313b527e46224eb2d4c78689674 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definitions/tasks.md | cismp-pixs-20261001-d63ed0352d96 | 54659b3f73ab3eb257b441d77005a1e38f2cee008ec2e335e44385a477916fea | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definitions/tasks.md | cismp-pixs-20261001-e8dd0ef9a6a7 | e5c62f0c6e8d5dcbb51feab3e1e83d9b8c57d1f26dcaa0f1b167acdc0ddd3b2c | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flags.py | cismp-pixs-20261001-7a6bd5419dbe | 40d4798b549f3710cc2ae78a76921fdef0c97d1c82fb2c616fb5526a06f624d1 | création/correction exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flags.py | cismp-pixs-20261001-88dcf1a98623 | a64123f36a3e41a434511fa19ad3aff33344701560086bb6d671ff3e69dd74b8 | création/correction exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_definitions.py | cismp-pixs-20261001-dbd7620fbfbb | 96e7064f87d115f3c6a7a7b5d61bef131d90c77056eaafbe75c0b28c9b391932 | création/correction exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_definitions.py | cismp-pixs-20261001-e50edb09b6e4 | 5a1f7e5c789e6006b5ccf7c8a69263ebd01dbb3daf36a807cff20c6de8fa5a09 | création/correction exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_definitions_integration.py | cismp-pixs-20261001-02bbd6af7e78 | 2bf5c8759d8ec37e5883524e80fbbb69821c87d59d965ecba4fd98127eb44e80 | création/correction exacte par commande, déjà comptée Commandes |

Les effets ci-dessus sont prouvés par les commandes natives et leurs hashes ; leurs chemins sont ceux au moment de l’opération avant archivage. Ils ne doublent pas les totaux des outils fichiers : 11 écritures sur 8 chemins distincts, dont 5 créations OpenSpec, 3 créations Python, 2 corrections Python et 1 cochage. Archivage : cinq artefacts déplacés par la commande OpenSpec, sans déplacement manuel. La mise à jour développeur AGENTS.md précède ce change et fait déjà partie de sa baseline de 144 hashes ; aucun AGENTS.md modifié dans cet intervalle.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Compilation Python | 5 | 18.5 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 4 | 14.8 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Publication/correction Python | 12 | 44.4 % | 11 | 91.7 % | 1 | 8.3 % | 0 | 0.0 % |
| Python vérification | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Régression du noyau | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 2 | 7.4 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| TOTAL | 27 | 100 % | 25 | 92.6 % | 1 | 3.7 % | 1 | 3.7 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [10] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;f… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [11] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;f… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [12] /home/devops/python/current/bin/python3 -B -m py_compile src/pixs/kernel/feature_flags.py | 2 | 7.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [13] /home/devops/python/current/bin/python3 -B -m py_compile tests/unit/test_feature_flag_definiti… | 2 | 7.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [14] /home/devops/python/current/bin/python3 -B -m py_compile tests/integration/test_feature_flag_d… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [15] PYTHONPATH=src:tests/unit /home/devops/python/current/bin/python3 -B -m unittest -v test_featu… | 2 | 7.4 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| [16] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;f… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [17] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;f… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [18] PYTHONPATH=src:tests/integration /home/devops/python/current/bin/python3 -B -m unittest -v tes… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [19] PYTHONPATH=src:tests/unit:tests/integration /home/devops/python/current/bin/python3 -B -m unit… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [1] true | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [20] PYTHONPATH=src /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [21] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [22] /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-definitions --yes | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;c=j… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;c=j… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;c=j… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;c=j… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;c=j… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [7] /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-definitions --strict | 3 | 11.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [8] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;fr… | 1 | 3.7 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| [9] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;fr… | 1 | 3.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 27 | 100 % | 25 | 92.6 % | 1 | 3.7 % | 1 | 3.7 % |

Commandes refusées explicitement :

| Commande (100 caractères max) | Occurrences | Part des refus |
|---|---|---|
| PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from p… | 1 | 100.0 % |

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucune URL visitée par l’agent de codage dans cet intervalle, aucun outil web exécuté. Les recherches techniques de l’orchestrateur et l’évaluation fournisseur PLLM restent hors de la télémétrie de production OpenCode ; elles sont déclarées séparément et ne sont pas attribuées au codeur. Volumes d’outils orchestrateur non exposés dans cette télémétrie : N/A.

Lectures web de l’orchestrateur dans ce scope : 0 appel(s) (100 % des appels enregistrés de ce sous-périmètre) ; statut approuvé et lu. URL : . Hors comptages natifs OpenCode ; autres volumes orchestrateur N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T23:25:55.076894+00:00 |
| Fin — après archivage | 2026-10-03T00:46:32.071657+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 20 min 36 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T23:25:55.076894+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-03T00:46:32.071657+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 45 | 62.5 % | 44 | 97.8 % | 0 | 0.0 % | 1 | 2.2 % |
| Commandes | 27 | 37.5 % | 25 | 92.6 % | 1 | 3.7 % | 1 | 3.7 % |
| Fichiers | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 72 | 100 % | 69 | 95.8 % | 1 | 1.4 % | 2 | 2.8 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| initial_feature_flag_definitions | 2026-10-02T23:28:18.569176+00:00 | 2026-10-02T23:28:21.165584+00:00 | 2026-10-02T23:28:23.227925+00:00 | 2.596408 | N/A | 146 | échouée |
| périodique — créneau 2026-10-02T23:58:18.569176+00:00 | 2026-10-03T00:07:07.969230+00:00 | 2026-10-03T00:07:11.099828+00:00 | 2026-10-03T00:07:16.519378+00:00 | 3.130596 | 99.454735 | 539 | réussie |
| périodique — créneau 2026-10-03T00:28:18.569176+00:00 | 2026-10-03T00:28:26.225253+00:00 | 2026-10-03T00:28:28.513820+00:00 | 2026-10-03T00:28:36.599401+00:00 | 2.288563 | 83.234537 | 673 | réussie |
| final_feature_flag_definitions_after_archive | 2026-10-03T00:46:11.975334+00:00 | 2026-10-03T00:46:13.892507+00:00 | 2026-10-03T00:46:20.737271+00:00 | 1.917172 | N/A | 596 | échouée |

Relèves prévues : 4 (100 %) ; réussies 2 (50.0 %), échouées 2 (50.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 2.288563/2.709580/3.130596 s ; débit min/moy/max : 83.234537/91.344636/99.454735 tok/s.

| Relève prévue UTC | Envoi réel UTC | Retard secondes |
|---|---|---|
| 2026-10-02T23:58:18.569176+00:00 | 2026-10-03T00:07:07.969230+00:00 | 529.400 |
| 2026-10-03T00:28:18.569176+00:00 | 2026-10-03T00:28:26.225253+00:00 | 7.656 |

Surcharge sondes : 43854 tokens total API, 1954 tokens sortie, coût API 0.009297180, durées stream mesurées 22.412245 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json. Modèle de codage de ce change : Qwen3.8Flash OpenCode Go/XHIGH, choix explicite du développeur appliqué avant le début. Les variantes non exposées des opérations de compaction sont N/A, jamais assimilées à XHIGH. Moyennes groupées par configuration, sondes invalides exclues du débit et du TTMT moyen. Deux sondes valides sur quatre tentatives ; les sondes initiale et finale ont échoué au contrôle de format, sans débit valide, et ne sont pas rejouées rétroactivement. Aucune sonde orchestrateur.

Incidents du périmètre : Préparation : mandat strict 80d3364c328e avec approval_id/commande non identiques rejeté avant opération, record broker ensuite EXPIRED ; reprise READY/0 puis nouveau strict 80eb973801b3 réussi. Publication module 823f7b9db05a : opérateur Bash altéré, permission native rejetée avant exécution, cible absente ; nouveau mandat 7a6bd5419dbe command simplifiée réussie. Validation unitaire f0a7f12118f1 : 24 tests dont 2 échecs (heure 24 acceptée par datetime Python 3.14 ; l’attendu ajouté par CGPT d’agrégation oubliait les identifiants dupliqués des témoins), corrections source et fixtures puis 24+1+175 réussis sous de nouveaux mandats. Horodatage readiness cité à tort 00:28:25 : seul checked_at outil réel 00:26:12.821933 fait autorité. Incidents POST 400 sans décision stockée réconciliés par GET 404 avant décision corrélée ; aucune réutilisation de décision ni effet hors cible. Archivage : avertissement non bloquant sur en-têtes anglais attendus de proposal.md rédigé en français ; exit 0, 5 artefacts exacts, zéro changement canonique. Sondes initiale/finale invalides au format : résultats conservés N/A sans débit inventé.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-initial-feature-flag-definitions, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucune variable PostgreSQL chargée ni connexion applicative dans ce scope ; aucune installation ni modification Git. Sources sensibles exclues des lectures natives de ce scope. 3 new sources only; readonly declarations and validation; other source/norms preserved; no actual flags runtime/P2 complete/P0 global. Ce change livre la fondation déclarative de définitions de fanions R1 uniquement ; il ne prouve ni P2 fanions complet, ni R2–R4 feature-flags, ni R3 capabilities, ni cycle CISMP complet.
