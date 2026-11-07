# STATISTIQUES — add-initial-health-classifier

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T14:19:18.403893+00:00 ; fin après archivage et sonde finale 2026-10-02T15:08:01.522839+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

Collecte active après la sélection conceptuelle et les premières propositions en lecture seule, avant les créations OpenSpec et la première tâche de codage. La phase antérieure reste hors intervalle, sans métriques reconstituées.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| glm-5.3-flash | N/A — version modèle non exposée | opencode-go | high | 1.400 s | 135.503 | 902.590 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 121 | 100 % |
| Appels outils | 62 | 100 % |
| Approuvé et exécuté | 60 | 96.8 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 2 | 3.2 % |
| Durée calendaire avec pauses | 00 h 48 min 43 s | 100 % de l’intervalle |

| Réponses en erreur ou interrompues | Nombre | Part assistants |
|---|---|---|
| Champ error natif non vide | 1 | 1.1 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 18479552 | 89.5 % |
| cache_write | 0 | 0.0 % |
| input | 2102225 | 10.2 % |
| output | 35415 | 0.2 % |
| reasoning | 21056 | 0.1 % |
| total | 20638248 | 100 % du total API |

Coût agrégé API : 0.897955810 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 22 | 100.0 % |
| TOTAL | 22 | 100 % |

Résultats finaux : 13 tests unitaires réussis (0.001s, matrice32souscas distincte),1 test intégration réussi (0.067s, sousprocessus frais,9gardesrefus+2imports bloqués prouvés causalement, zéro IO applicatif/PG/réseau). ASTPython3.11 et exécutionPython3.14.8, UTF8LF,3sources byteexact,READMEappend seul,82empreintes+dist3préservées,5artefacts,deltaobservabilitymotamot,strict avantcode/aprèspreuves/aprèscases exit0. Archives5artefacts bytevérifiés, aucune évolution active. Les612/180 historiques restent inchangés/nonrejoués, aucune conformité globale des pins ou disponibilitéglobale proclamée.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 89 | 73.6 % |
| user | 32 | 26.4 % |
| TOTAL | 121 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 13 | 3.8 % |
| step-finish | 88 | 26.0 % |
| step-start | 89 | 26.3 % |
| text | 86 | 25.4 % |
| tool | 62 | 18.3 % |
| TOTAL | 338 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| absent | 1 | 1.1 % |
| stop | 31 | 34.8 % |
| tool-calls | 57 | 64.0 % |
| TOTAL | 89 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 11 | 17.7 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |
| cgpt-validation_broker_readiness | 7 | 11.3 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 2 | 3.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 1.6 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| cgpt-validation_request_validation | 22 | 35.5 % | 22 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 3 | 4.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 8 | 12.9 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 8 | 12.9 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 62 | 100 % | 60 | 96.8 % | 0 | 0.0 % | 2 | 3.2 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f0342c3e0ffeGjabJTz3rTDfnI | 121 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-health-classifier/.openspec.yaml | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-health-classifier/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-health-classifier/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-health-classifier/specs/observability/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-health-classifier/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/health_classifier.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_health_classifier_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_health_classifier.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-health-classifier. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 5 | 45.5 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % |
| Prévol true | 3 | 27.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/true | 3 | 27.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /home/devops/.local/npm/bin/openspec validate add-initial-health-classifier --strict | 4 | 36.4 % | 3 | 75.0 % | 0 | 0.0 % | 1 | 25.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/python/current/bin/python3 -B -c '… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /home/devops/.local/npm/bin/openspec archive add-initial-health-classifier --skip-specs --yes | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |

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
| Début | 2026-10-02T14:19:18.403893+00:00 |
| Fin — après archivage | 2026-10-02T15:08:01.522839+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 48 min 43 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T14:19:18.403893+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T15:08:01.522826+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 40 | 64.5 % | 39 | 97.5 % | 0 | 0.0 % | 1 | 2.5 % |
| Commandes | 11 | 17.7 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |
| Fichiers | 11 | 17.7 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 62 | 100 % | 60 | 96.8 % | 0 | 0.0 % | 2 | 3.2 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début — add-initial-health-classifier | 2026-10-02T14:19:18.443403+00:00 | 2026-10-02T14:19:19.528550+00:00 | 2026-10-02T14:19:21.901618+00:00 | 1.085146 | 202.690880 | 481 | réussie |
| périodique — créneau 2026-10-02T14:49:28.528052+00:00 | 2026-10-02T14:49:28.558920+00:00 | 2026-10-02T14:49:30.054951+00:00 | 2026-10-02T14:49:38.145686+00:00 | 1.496030 | 58.956276 | 477 | réussie |
| fin — après archivage add-initial-health-classifier | 2026-10-02T15:07:51.446249+00:00 | 2026-10-02T15:07:53.064172+00:00 | 2026-10-02T15:07:56.377694+00:00 | 1.617922 | 144.861162 | 480 | réussie |

Relèves prévues : 3 (100 %) ; réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 1.085146/1.399699/1.617922 s ; débit min/moy/max : 58.956276/135.502773/202.690880 tok/s.

Surcharge sondes : 27778 tokens total API, 1438 tokens sortie, coût API 0.004740350, durées stream mesurées 13.777331 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Préparation stricte initiale exit1 : clé metadata change non supportée, corrigée seule sous nouveau CAB puis strict exit0. Compteur broker transitoire1 revenu réellement0 ; list_pending MCP a expiré sans écriture. CGPT a interrompu un brouillon readonly sur observation devenue dépassée, puis READY/test CAB inédit et reprise du seul brouillon. Template statistiques a été corrigé après SyntaxError local avant sauvegarde/appel natif. Conflit409 de handoff contrôleur résolu par gate de sélection scoped ; parent OPEN. Transitoires HTTP400 sans décision persistée suivis GET404 et d’une décision unique exacte. Aucun échec de test, aucune écriture source hors cible, aucune ancienne suite ou sonde PG rejouée.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-health-classifier, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucune variable PostgreSQL chargée ni connexion applicative dans ce scope ; aucune installation ni modification Git. Sources sensibles exclues des lectures natives de ce scope. Classificateur pur de snapshots de santé, PG obligatoire, quatre types de contrôle, trois sources nouvelles et README append seul; aucune sonde ni Django ni PG réel. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
