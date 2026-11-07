# STATISTIQUES — add-initial-capability-availability-gate

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T19:08:11.249505+00:00 ; fin après archivage et sonde finale 2026-10-02T22:07:14.191024+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

Les trois sources et le réglage LLM dans opencode.json ont été publiés par des commandes natives unitaires, distinguées des outils write. Le modèle est passé de GLM5.3 Flash/HIGH à Qwen3.8 Flash/XHIGH sur instruction explicite, avec les mêmes accès Go en mémoire. Les deux sondes non conformes au prompt restent des échecs de mesure, avec débit N/A. AGENTS.md (854 lignes) a été relu intégralement par CGPT et OpenCode ; les trois py_compile obligatoires ont été exécutés. Les quotas Codex indisponibles ne sont pas remplacés par ceux de Go.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| glm-5.3-flash | N/A — version modèle non exposée | opencode-go | N/A | N/A | N/A | 76.177 s mesurables ; part N/A |
| glm-5.3-flash | N/A — version modèle non exposée | opencode-go | high | 2.452 s | 91.554 | 3742.446 s mesurables ; part N/A |
| qwen3.8-flash | N/A — version modèle non exposée | opencode-go | N/A | N/A | N/A | 118.373 s mesurables ; part N/A |
| qwen3.8-flash | N/A — version modèle non exposée | opencode-go | xhigh | 2.951 s | 74.092 | 282.839 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | N/A — version modèle non exposée | OpenAI | high | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 186 | 100 % |
| Appels outils | 94 | 100 % |
| Approuvé et exécuté | 93 | 98.9 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 1 | 1.1 % |
| Durée calendaire avec pauses | 02 h 59 min 02 s | 100 % de l’intervalle |

| Réponses en erreur ou interrompues | Nombre | Part assistants |
|---|---|---|
| Champ error natif non vide | 0 | 0.0 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 7604897 | 79.7 % |
| cache_write | 563264 | 5.9 % |
| input | 1122777 | 11.8 % |
| output | 93454 | 1.0 % |
| reasoning | 162395 | 1.7 % |
| total | 9546787 | 100 % du total API |

Coût agrégé API : 0.578242004 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 3 (part 0.5 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 23 | 100.0 % |
| TOTAL | 23 | 100 % |

Résultats finaux : 175 tests réussis sous Python 3.14.8 : 35 nouveaux unitaires, 1 intégration dans un processus frais gardé et 139 régressions ciblées. Trois py_compile ont réussi, ainsi que le vérificateur des hashes, de la syntaxe 3.11 du parent et du programme enfant, de l’UTF-8/LF, des cinq DTO figés et des signatures publiques. Les 133 hashes de référence sont préservés après prise en compte de la mise à jour développeur d’AGENTS.md. R2 est repris mot à mot ; les validations strictes après code et après cochage ont réussi. Cela ne prouve ni une disponibilité de production ni le P0 global.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 134 | 72.0 % |
| user | 52 | 28.0 % |
| TOTAL | 186 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| compaction | 3 | 0.5 % |
| reasoning | 101 | 17.5 % |
| step-finish | 134 | 23.2 % |
| step-start | 134 | 23.2 % |
| text | 112 | 19.4 % |
| tool | 94 | 16.3 % |
| TOTAL | 578 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| length | 1 | 0.7 % |
| stop | 51 | 38.1 % |
| tool-calls | 81 | 60.4 % |
| unknown | 1 | 0.7 % |
| TOTAL | 134 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 17 | 18.1 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 8 | 8.5 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 7 | 7.4 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 3 | 3.2 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 24 | 25.5 % | 23 | 95.8 % | 0 | 0.0 % | 1 | 4.2 % |
| glob | 2 | 2.1 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 6 | 6.4 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 21 | 22.3 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 6 | 6.4 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 94 | 100 % | 93 | 98.9 % | 0 | 0.0 % | 1 | 1.1 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f022b133fffe9xGy4geWvAaJN6 | 186 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-availability-gate/.openspec.yaml | 1 | 16.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-availability-gate/design.md | 1 | 16.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-availability-gate/proposal.md | 1 | 16.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-availability-gate/specs/capabilities/spec.md | 1 | 16.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-availability-gate/tasks.md | 2 | 33.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 6 | 100 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 5 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-initial-capability-availability-gate. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

Effets fichiers des commandes :

| Chemin absolu complet | Mandat exact | SHA observé | Convention de comptage |
|---|---|---|---|
| /home/devops/datas/pixs/src/pixs/kernel/lifecycle/availability.py | cismp-pixs-20261001-1e3dbe56cada | 6b97191a0514e442104650c0e0b674521fcb75aa747c835454c6d89493727503 | création exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/unit/test_capability_availability_gate.py | cismp-pixs-20261001-01d499f0b909 | 2d31627fd16c4c2e543e30f1314debcc3247ada5bc54473d887d1a6aaae8cf61 | création exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/tests/integration/test_capability_availability_gate_integration.py | cismp-pixs-20261001-4f1496cf127f | 0212d11c14e21b36b0536a3c599329c90fd2f2105a97a508db714e0b227128b6 | création exacte par commande, déjà comptée Commandes |
| /home/devops/datas/pixs/opencode.json | cismp-pixs-20261001-4e507974ef27 | a0e3503b9af4feb38454f49dbe0ba0e6bfe7d58b42baf8ae5d80279e1405cc8b | réglage LLM explicitement demandé, déjà compté Commandes |

Les quatre effets ci-dessus sont prouvés par les commandes natives et leurs hashes ; ils ne doublent pas les totaux des outils fichiers. Archivage : cinq artefacts déplacés par la commande OpenSpec, sans déplacement manuel. Mise à jour développeur AGENTS.md reconnue avant la relecture, sans écriture de cet agent.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 23.5 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 8 | 47.1 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 17 | 100 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [10] PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [11] PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integr… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [12] PYTHONPATH=src:tests/unit:tests/integration /home/devops/python/current/bin/python3 -B -m unit… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [13] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib;from pathlib import Path;c=… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [14] /home/devops/.local/npm/bin/openspec archive add-initial-capability-availability-gate --yes | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [1] true | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /home/devops/.local/npm/bin/openspec validate add-initial-capability-availability-gate --strict | 3 | 17.6 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib,copy from pathlib import Pat… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /home/devops/python/current/bin/python3 -B -c 'import hashlib,json from pathlib import Path ass… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /home/devops/python/current/bin/python3 -B -c 'import hashlib,json from pathlib import Path ass… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /home/devops/python/current/bin/python3 -B -c 'import hashlib,json from pathlib import Path ass… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [7] /home/devops/python/current/bin/python3 -B -m py_compile src/pixs/kernel/lifecycle/availability… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [8] /home/devops/python/current/bin/python3 -B -m py_compile tests/unit/test_capability_availabilit… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [9] /home/devops/python/current/bin/python3 -B -m py_compile tests/integration/test_capability_avai… | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 17 | 100 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

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
| Début | 2026-10-02T19:08:11.249505+00:00 |
| Fin — après archivage | 2026-10-02T22:07:14.191024+00:00 |
| Durée globale (pauses et attentes incluses) | 02 h 59 min 02 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T19:08:11.249514+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T22:07:14.191004+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 71 | 75.5 % | 70 | 98.6 % | 0 | 0.0 % | 1 | 1.4 % |
| Commandes | 17 | 18.1 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 6 | 6.4 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 94 | 100 % | 93 | 98.9 % | 0 | 0.0 % | 1 | 1.1 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| initiale | 2026-10-02T19:08:11.290676+00:00 | 2026-10-02T19:08:13.159055+00:00 | 2026-10-02T19:08:32.763531+00:00 | 1.868378 | 24.331178 | 477 | réussie |
| périodique — créneau 2026-10-02T19:38:32.763531+00:00 | 2026-10-02T19:38:32.951463+00:00 | 2026-10-02T19:38:34.142008+00:00 | 2026-10-02T19:38:36.086729+00:00 | 1.190519 | 247.333219 | 481 | réussie |
| periodic | 2026-10-02T20:09:45.351239+00:00 | 2026-10-02T20:09:47.372623+00:00 | 2026-10-02T20:09:56.293251+00:00 | 2.021383 | 53.919941 | 481 | réussie |
| periodic | 2026-10-02T20:39:18.798008+00:00 | 2026-10-02T20:39:23.570203+00:00 | 2026-10-02T20:39:29.925269+00:00 | 4.772194 | 75.530313 | 480 | réussie |
| periodic | 2026-10-02T21:10:49.521724+00:00 | 2026-10-02T21:10:51.930807+00:00 | 2026-10-02T21:11:00.350308+00:00 | 2.409082 | 56.654180 | 477 | réussie |
| model_switch_preflight | 2026-10-02T21:27:50.619296+00:00 | 2026-10-02T21:27:53.570063+00:00 | 2026-10-02T21:28:00.669328+00:00 | 2.950766 | 74.092147 | 526 | réussie |
| périodique — créneau 2026-10-02T21:38:32.763531+00:00 | 2026-10-02T21:39:35.482789+00:00 | 2026-10-02T21:39:36.895191+00:00 | 2026-10-02T21:39:39.285874+00:00 | 1.412399 | N/A | 185 | échouée |
| final_after_archive | 2026-10-02T22:07:04.082511+00:00 | 2026-10-02T22:07:06.824308+00:00 | 2026-10-02T22:07:11.552846+00:00 | 2.741797 | N/A | 381 | échouée |

Relèves prévues : 8 (100 %) ; réussies 6 (75.0 %), échouées 2 (25.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 1.190519/2.535387/4.772194 s ; débit min/moy/max : 24.331178/88.643496/247.333219 tok/s.

| Relève prévue UTC | Envoi réel UTC | Retard secondes |
|---|---|---|
| 2026-10-02T19:38:32.763531+00:00 | 2026-10-02T19:38:32.951463+00:00 | 0.188 |
| 2026-10-02T20:08:32.763531+00:00 | 2026-10-02T20:09:45.351239+00:00 | 72.588 |
| 2026-10-02T20:38:32.763531+00:00 | 2026-10-02T20:39:18.798008+00:00 | 46.034 |
| 2026-10-02T21:08:32.763531+00:00 | 2026-10-02T21:10:49.521724+00:00 | 136.758 |
| 2026-10-02T21:38:32.763531+00:00 | 2026-10-02T21:39:35.482789+00:00 | 62.719 |

Surcharge sondes : 79770 tokens total API, 3488 tokens sortie, coût API 0.014860340, durées stream mesurées 59.462909 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json. Changement explicite de modèle : GLM5.3Flash/HIGH puis Qwen3.8Flash/XHIGH ; moyennes comparables groupées par configuration, sondes invalides exclues du débit. Aucune sonde orchestrateur.

Incidents du périmètre : Une proposition de module terminée avec finish=length a été récupérée en fragments, avant toute écriture. Les erreurs de signatures, de projection, de repli hôte et de fixtures ont été corrigées pendant la revue. Un appel MCP avec commands sous forme de chaîne a été rejeté par le schéma (-32602) avant enregistrement au broker ; seule la demande ensuite enregistrée avec la cible exacte a reçu une décision. Des HTTP 400 transitoires sans décision stockée ont été réconciliés avant approbation unique. Un NDOC allégant un requestId antérieur non observé a été rectifié après contrôle de l’historique complet (zéro appel concerné) et GET /decision en 404 ; la première soumission réelle a ensuite été approuvée une fois. Deux sondes Qwen ont échoué au protocole textuel (débit N/A). Les 175 tests fonctionnels ont tous réussi. La mise à jour des défauts par API ne s’est pas reflétée ; un mandat ciblé sur opencode.json puis la relecture des agents ont confirmé Qwen/XHIGH. Les opérations d’API de l’orchestrateur sont hors des compteurs natifs et décrites ici.

Hors des bornes de production : le premier mandat de publication STATISTIQUES, feabae258497, a été refusé par CGPT parce que la commande reçue omettait le deux-points d’un with. Aucun Bash ni fichier n’a été exécuté/créé. Le rapport a ensuite été publié sous un nouveau mandat exact, via un programme figé vérifié par SHA. Ces opérations ne changent pas les compteurs de production ci-dessus.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-initial-capability-availability-gate, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucune variable PostgreSQL chargée ni connexion applicative dans ce scope ; aucune installation ni modification Git. Sources sensibles exclues des lectures natives de ce scope. Gate host lifecycle borné, provenance des observations explicitement hôte ; aucun état déduit de résolution/conformité seules ; aucun Django/PG/IO ni P0/global. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
