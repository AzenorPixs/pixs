# STATISTIQUES — add-p0-provider-assurance-mapping

Périmètre : /home/devops/datas/pixs. Début 2026-10-03T01:11:23.405765+00:00 ; fin après archivage et sonde finale 2026-10-03T01:49:40.138869+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

Baseline prise avant préparation : 168 hashes (153 hérités +15 sources publiques core explicitement ciblées), tous préservés avant et après archivage. Exactement3 sources nouvelles, core/authz/__init__.py et tous consommateurs existants inchangés. Les 117 tests de ce change sont les seuls tests finaux revendiqués ici :25 unitaires,1 intégration enfant frais,91 régressions PDP/identité/périmètre. Les 200 tests du change précédent sont déjà prouvés dans leur propre rapport, aucun rejeu ni doublecompte. Syntaxe minimale3.11 contrôlée par AST ; compilation et tests réellement sous3.14.8. CAB : 21 mandats documentés par SSE direct, demandes/rapports HTTP toutes2s ; rédaction/analyses contrôlées à pauses fixes7s. Sonde30min à frontière sûre sans attente du créneau ; finale distincte après archive.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| qwen3.8-flash | N/A — version modèle non exposée | opencode-go | xhigh | 2.520 s | 88.789 | 480.034 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | N/A — version modèle non exposée | OpenAI | high | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 106 | 100 % |
| Appels outils | 44 | 100 % |
| Approuvé et exécuté | 44 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 00 h 38 min 16 s | 100 % de l’intervalle |

| Réponses en erreur ou interrompues | Nombre | Part assistants |
|---|---|---|
| Champ error natif non vide | 0 | 0.0 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 18276336 | 94.1 % |
| cache_write | 1087180 | 5.6 % |
| input | 450 | 0.0 % |
| output | 51767 | 0.3 % |
| reasoning | 0 | 0.0 % |
| total | 19415733 | 100 % du total API |

Coût agrégé API : 0.534255366 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 21 | 100.0 % |
| TOTAL | 21 | 100 % |

Résultats finaux : 117 tests réussis sous Python 3.14.8 : 25 unitaires nouveaux, 1 intégration enfant frais sous gardes causales, 91 régressions PDP/identité/périmètre. py_compile réel des trois fichiers, AST minimum3.11 trois parents et enfant, API et quatre DTO frozen sans défaut 3/7/6/3, enums/UTC helper existants réutilisés, baseline168 préservée, delta R1 literal seul et strict pré-cochage réussi. Portion mapping de R1 seulement : aucune authentification réelle, vérification crypto, session, permission ou P0 global livré. Preuves finales : unit cismp-pixs-20261001-982a28e245c2 ; intégration cismp-pixs-20261001-5aed5a93027c ; régression cismp-pixs-20261001-8def5bc1d495 ; checker cismp-pixs-20261001-5614f3533ffc ; strict après cochage cismp-pixs-20261001-2a101d6e9d2e ; archive cismp-pixs-20261001-5af70874ee0a.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 75 | 70.8 % |
| user | 31 | 29.2 % |
| TOTAL | 106 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 75 | 22.7 % |
| step-finish | 75 | 22.7 % |
| step-start | 75 | 22.7 % |
| text | 62 | 18.7 % |
| tool | 44 | 13.3 % |
| TOTAL | 331 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 31 | 41.3 % |
| tool-calls | 44 | 58.7 % |
| TOTAL | 75 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 21 | 47.7 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 2 | 4.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 21 | 47.7 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 44 | 100 % | 44 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f022b133fffe9xGy4geWvAaJN6 | 106 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 0 chemins distincts (N/A). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-p0-provider-assurance-mapping. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

Effets fichiers des commandes :

| Chemin absolu complet | Mandat exact | SHA observé | Convention de comptage |
|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-provider-assurance-mapping/.openspec.yaml | cismp-pixs-20261001-fc9622869d4e | 5f734986346dad86a56f91476441377d77de7b13c8917bcc685059135d55fe75 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-p0-provider-assurance-mapping/proposal.md | cismp-pixs-20261001-4e022b8c872c | ba6f7f07361c8ceb09c22be3efc1a720a800cb0de1fe070e41d83aa1095acb73 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-p0-provider-assurance-mapping/design.md | cismp-pixs-20261001-b062f484b731 | c3ba8a62a2aab9127451ce25b4e69f6bace245b11c3d2bcca6f96ee9ba7dca80 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-p0-provider-assurance-mapping/tasks.md | cismp-pixs-20261001-8f4b5c154305 | 5b10394fdfce90fac6654d77fe357ef76fa400a3389b586ddefbcda0be67a6fd | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-p0-provider-assurance-mapping/specs/identity-assurance/spec.md | cismp-pixs-20261001-480233841e65 | d4839f408dc758614bb420bec1abdf173cb4572bc7d8a020013c545ac17570b8 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/openspec/changes/add-p0-provider-assurance-mapping/tasks.md | cismp-pixs-20261001-d7169b6da323 | 5bcaec82eb792c1b855070e7d4d50c3a1a5c87b3ffeae779b1e1eb18a4765667 | écriture exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/src/pixs/core/authz/assurance_mapping.py | cismp-pixs-20261001-0f757968a28b | 9f630106df19c9687e846580eeca3bd6da8cba36b4493b2674775e3374394331 | création/correction exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/unit/test_provider_assurance_mapping.py | cismp-pixs-20261001-2f23c76241f4 | ff0ed4008a873f84bf2bb43642eb728ebc4434d80a04fa3e6acb4b0cf32937d2 | création/correction exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/integration/test_provider_assurance_mapping_integration.py | cismp-pixs-20261001-f681843250ff | ce59d632c57e087766174ed7a390d7b34497dc674c788a7fa72a3707c24e6c2f | création/correction exacte par commande, déjà comptée Commandes |

Les effets ci-dessus sont prouvés par les commandes natives et leurs hashes ; leurs chemins sont ceux au moment de l’opération avant archivage. Ils ne doublent pas les totaux des outils fichiers : 9 écritures sur 8 chemins distincts, dont 5 créations OpenSpec, 3 créations Python et 1 cochage ; aucune correction de source après publication. Archivage : cinq artefacts déplacés par la commande OpenSpec, sans déplacement manuel. La mise à jour développeur AGENTS.md précède ce change et fait déjà partie de sa baseline de 168 hashes, incluant 15 sources publiques core ajoutées explicitement après constat de la règle d’ignore ; aucune modification de .gitignore ; aucun AGENTS.md modifié dans cet intervalle.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Compilation Python | 3 | 14.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 4 | 19.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Publication/correction Python | 9 | 42.9 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Régression PDP/identité/périmètre | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 21 | 100 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [10] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;f… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [11] /home/devops/python/current/bin/python3 -B -m py_compile src/pixs/core/authz/assurance_mapping… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [12] /home/devops/python/current/bin/python3 -B -m py_compile tests/unit/test_provider_assurance_ma… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [13] /home/devops/python/current/bin/python3 -B -m py_compile tests/integration/test_provider_assur… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [14] PYTHONPATH=src:tests/unit /home/devops/python/current/bin/python3 -B -m unittest -v test_provi… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [15] PYTHONPATH=src:tests/integration /home/devops/python/current/bin/python3 -B -m unittest -v tes… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [16] PYTHONPATH=src:tests/unit /home/devops/python/current/bin/python3 -B -m unittest -v test_pdp_p… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [17] PYTHONPATH=src /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [18] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [19] /home/devops/.local/npm/bin/openspec archive add-p0-provider-assurance-mapping --yes | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [1] true | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=j… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=j… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=j… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=j… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;r=j… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [7] /home/devops/.local/npm/bin/openspec validate add-p0-provider-assurance-mapping --strict | 3 | 14.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [8] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;fr… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [9] PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;fr… | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 21 | 100 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucune URL visitée par l’agent de codage dans cet intervalle, aucun outil web exécuté. Les recherches techniques de l’orchestrateur et l’évaluation fournisseur PLLM restent hors de la télémétrie de production OpenCode ; elles sont déclarées séparément et ne sont pas attribuées au codeur. Volumes d’outils orchestrateur non exposés dans cette télémétrie : N/A.

Lectures web de l’orchestrateur dans ce scope : 0 appel(s) (100 % des appels enregistrés de ce sous-périmètre) ; statut approuvé et lu. URL : . Hors comptages natifs OpenCode ; autres volumes orchestrateur N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-03T01:11:23.405765+00:00 |
| Fin — après archivage | 2026-10-03T01:49:40.138869+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 38 min 16 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-03T01:11:23.405785+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-03T01:49:40.138869+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 23 | 52.3 % | 23 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 21 | 47.7 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 44 | 100 % | 44 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| initial_provider_assurance_mapping | 2026-10-03T01:11:23.465542+00:00 | 2026-10-03T01:11:26.629125+00:00 | 2026-10-03T01:11:34.415496+00:00 | 3.163579 | N/A | 571 | échouée |
| périodique — créneau 2026-10-03T01:41:23.465542+00:00 | 2026-10-03T01:42:17.491399+00:00 | 2026-10-03T01:42:19.461901+00:00 | 2026-10-03T01:42:24.897836+00:00 | 1.970498 | 101.730346 | 553 | réussie |
| final_provider_assurance_mapping_after_archive | 2026-10-03T01:49:20.034565+00:00 | 2026-10-03T01:49:23.104241+00:00 | 2026-10-03T01:49:30.105059+00:00 | 3.069674 | 75.848275 | 531 | réussie |

Relèves prévues : 3 (100 %) ; réussies 2 (66.7 %), échouées 1 (33.3 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 1.970498/2.520086/3.069674 s ; débit min/moy/max : 75.848275/88.789311/101.730346 tok/s.

| Relève prévue UTC | Envoi réel UTC | Retard secondes |
|---|---|---|
| 2026-10-03T01:41:23.465542+00:00 | 2026-10-03T01:42:17.491399+00:00 | 54.026 |

Surcharge sondes : 33080 tokens total API, 1655 tokens sortie, coût API 0.007061950, durées stream mesurées 20.223135 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json. Modèle de codage de ce change : Qwen3.8Flash OpenCode Go/XHIGH, choix explicite du développeur appliqué avant le début. Les variantes non exposées des opérations de compaction sont N/A, jamais assimilées à XHIGH. Moyennes groupées par configuration, sondes invalides exclues du débit et du TTMT moyen. 2 sonde(s) valide(s) sur 3 tentative(s) ; les sondes invalides restent sans débit valide et ne sont pas rejouées rétroactivement. Aucune sonde orchestrateur.

Incidents du périmètre : La revue des propositions a corrigé avant toute publication : identité des membres enum avant hash/ordinal, attributs obligatoires manquants en erreur constante, mapping hors fenêtre au minimum après validation, témoins de fenêtres, timezone non sous-classable remplacé par tzinfo, suppression de code mort, contrôles réels de permutations et compteurs de pièges, accès __dict__ incompatible avec slots remplacé. Aucun de ces brouillons n’a été exécuté ou publié. Toutes les exécutions natives de source, compilation et tests ont réussi au premier mandat. Le rapport de readiness initial citait01:01:07.258722 au lieu du checked_at outil01:12:21.430488 ; rectifié explicitement, toutes décisions basées sur l’outil réel. POST400 sans décision stockée réconciliés par GET404 puis décision corrélée, aucune réutilisation d’autorisation. Sonde initiale invalide au format, sonde périodique et finale valides ; aucun débit invalide inventé. La règle d’ignore core était constatée durant la sélection précédente : 15 sources existantes sont incluses dans la nouvelle baseline168, .gitignore intact.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-p0-provider-assurance-mapping, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucune variable PostgreSQL chargée ni connexion applicative dans ce scope ; aucune installation ni modification Git. Sources sensibles exclues des lectures natives de ce scope. 3 new sources only; inherited 153 plus 15 public core files explicitly included; baseline168; no source legacy or __init__ writes. Ce change livre uniquement la portion mapping fournisseur de R1 identity-assurance ; il ne prouve pas une authentification réelle produisant un contexte, la vérification cryptographique, une session, une permission ou le P0 global. Les contrôles PDP existants de seuil, temps et révocation sont préservés ; les intégrations réelles R2/R3 ne sont pas livrées ici. Le cycle CISMP parent reste ouvert.
