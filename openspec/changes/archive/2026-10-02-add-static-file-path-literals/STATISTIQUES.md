# STATISTIQUES — add-static-file-path-literals

Périmètre : /home/devops/datas/pixs. Début 2026-10-01T22:13:07.055000+00:00 ; fin après archivage et sonde finale 2026-10-01T22:31:55.347025+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 2.188 s | 141.128 | 121.998 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 89 | 100 % |
| Appels outils | 45 | 100 % |
| Approuvé et exécuté | 45 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 00 h 18 min 48 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 20949169 | 99.5 % |
| cache_write | 0 | 0.0 % |
| input | 67169 | 0.3 % |
| output | 27619 | 0.1 % |
| reasoning | 3093 | 0.0 % |
| total | 21047050 | 100 % du total API |

Coût agrégé API : 0.054757638 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 19 | 100.0 % |
| TOTAL | 19 | 100 % |

Résultats finaux : Baseline native avant code : 590 tests unitaires et 165 tests d’intégration réussis. Après code : 592 tests unitaires et 166 tests d’intégration réussis. AST Python 3.11 des trois sources et trois extraits, exact UTF-8/LF, append seul README et 26 empreintes préservées. Évolution fonctionnelle limitée à _require_path et trois lignes de docstring liées ; les deux tests historiques restent inchangés. Delta Surface HTTP identique à la norme, matrice cadrages complète, huit cases cochées, strict avant code et avant/après cochage valides. Archivage natif --skip-specs réussi : cinq empreintes préservées, change actif absent. Aucun shell servi, URL concrète distribuée, serveur, readiness/startup/P0/global ou cycle CISMP complet revendiqué.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 65 | 73.0 % |
| user | 24 | 27.0 % |
| TOTAL | 89 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 106 | 32.2 % |
| step-finish | 65 | 19.8 % |
| step-start | 65 | 19.8 % |
| text | 48 | 14.6 % |
| tool | 45 | 13.7 % |
| TOTAL | 329 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 24 | 36.9 % |
| tool-calls | 41 | 63.1 % |
| TOTAL | 65 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 9 | 20.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 19 | 42.2 % | 19 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 2.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 2.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 6 | 13.3 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 9 | 20.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 45 | 100 % | 45 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f06b54883ffe63YLISnmeNo8Pf | 89 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-static-file-path-literals/.openspec.yaml | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-static-file-path-literals/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-static-file-path-literals/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-static-file-path-literals/specs/initial-application-bootstrap/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-static-file-path-literals/tasks.md | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/http_route_guard.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_static_file_path_literals_integration.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_static_file_path_literals.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 10 | 100 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-static-file-path-literals. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 33.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

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
| Début | 2026-10-01T22:13:07.055000+00:00 |
| Fin — après archivage | 2026-10-01T22:31:55.347025+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 18 min 48 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-01T22:14:49.145712+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-01T22:32:29.382441+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 26 | 57.8 % | 26 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 9 | 20.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 10 | 22.2 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 45 | 100 % | 45 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-static-file-path-literals | 2026-10-01T22:14:49.167679+00:00 | 2026-10-01T22:14:51.922965+00:00 | 2026-10-01T22:14:56.777267+00:00 | 2.755282 | 104.649427 | 508 | réussie |
| fin — après archivage | 2026-10-01T22:31:50.821020+00:00 | 2026-10-01T22:31:52.441461+00:00 | 2026-10-01T22:31:55.194743+00:00 | 1.620439 | 177.606263 | 489 | réussie |

Relèves prévues : 2 (100 %) ; réussies 2 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 1.620439/2.187860/2.755282 s ; débit min/moy/max : 104.649427/141.127845/177.606263 tok/s.

Surcharge sondes : 18022 tokens total API, 997 tokens sortie, coût API 0.001943000, durées stream mesurées 7.607584 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Incidents CGPT : référence baseline prise comme dictionnaire puis corrigée vers sa preuve RID avant écriture de périmètre ; contrôle AST du brouillon raw sans dedent corrigé avant écriture code. Noms de tests contenant slash corrigés au stade brouillon avant tout test natif ; tests compile-only remplacés par contrôle AST distinct. Des POST contrôleur HTTP400 sans décision stockée ont été suivis d’une approbation exacte unique, sans duplication ni effet natif hors mandat. Aucun échec de test ou outil natif dans ce périmètre.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-static-file-path-literals, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ni réseau applicatif dans les tests observés. Chemins littéraux de fichiers statiques explicitement déclarables, aucun wildcard/converter/URL distribuée/readiness/P0/global. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
