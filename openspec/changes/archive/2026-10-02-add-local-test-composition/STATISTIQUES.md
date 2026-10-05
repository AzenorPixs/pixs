# STATISTIQUES — add-local-test-composition

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T00:30:07.999000+00:00 ; fin après archivage et sonde finale 2026-10-02T01:18:36.012210+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 8.049 s | 111.137 | 654.110 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 96 | 100 % |
| Appels outils | 48 | 100 % |
| Approuvé et exécuté | 48 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 00 h 48 min 28 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 49519733 | 94.8 % |
| cache_write | 0 | 0.0 % |
| input | 2615430 | 5.0 % |
| output | 49110 | 0.1 % |
| reasoning | 25696 | 0.0 % |
| total | 52209969 | 100 % du total API |

Coût agrégé API : 0.375543666 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 19 | 100.0 % |
| TOTAL | 19 | 100 % |

Résultats finaux : 601 tests unitaires et 170 tests d’intégration réussis, sans échec observé. Le Client vérifie santé, shell, assets, document et capacité cohérente, refus privé 403 et inconnu 404, avec trois gardes PG et deux gardes socket à zéro. Le cycle WSGI sur port éphémère conserve les gardes PG et ferme thread/socket après succès et exception du corps. Le harnais sur 127.0.0.1:5173 utilise le helper, vérifie huit GET réels conformes puis Chromium 154.0.8037.92 : criticalOk=true, 21 requêtes autorisées, zéro accès externe bloqué, zéro erreur HTTP ou console et gardes PG [0,0,0]. Navigateur, profil, thread et socket sont fermés ; PID 301594 absent. Quatre sources et quatre fragments AST Python 3.11, UTF-8/LF, 48 empreintes préexistantes et trois fichiers de dist inchangés, append README exact. Huit cases cochées sur preuves ; validations strictes avant code, finale et après cochage réussies. Archive avec --skip-specs et cinq empreintes conservées ; deux blocs normatifs repris mot à mot. Aucune composition P0, activation Kernel/Core, readiness ou production globale revendiquée ; aucun arrêt garanti pour un callback arbitraire qui ne termine pas.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 69 | 71.9 % |
| user | 27 | 28.1 % |
| TOTAL | 96 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 136 | 36.2 % |
| step-finish | 69 | 18.4 % |
| step-start | 69 | 18.4 % |
| text | 54 | 14.4 % |
| tool | 48 | 12.8 % |
| TOTAL | 376 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 27 | 39.1 % |
| tool-calls | 42 | 60.9 % |
| TOTAL | 69 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 8 | 16.7 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 19 | 39.6 % | 19 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 2 | 4.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 9 | 18.8 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 9 | 18.8 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 48 | 100 % | 48 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f06b54883ffe63YLISnmeNo8Pf | 96 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-local-test-composition/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-local-test-composition/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-local-test-composition/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-local-test-composition/specs/initial-application-bootstrap/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-local-test-composition/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/local_test_composition.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/check_local_composition_browser.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_local_test_composition_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_local_test_composition.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 10 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-local-test-composition. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Navigateur local | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 4 | 50.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 37.5 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin:/home/devops/node/current/bin LANG=C.UTF-8 PYTHONPATH=/home/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web OpenCode exécuté. Le Client Django valide santé, shell et assets GET/HEAD/POST, document GET/HEAD/POST, capacité GET, privées GET/HEAD/POST 403 et inconnues 404 en mémoire avec gardes PG et socket à zéro. Un second test réalise le cycle WSGI sur port éphémère en boucle locale, gardes PG actives, puis prouve la fermeture du thread/FD après succès et exception du corps. Ces requêtes réelles sont attendues ; aucun zéro-socket global n’est revendiqué. Le harnais distinct utilise le helper serveur sur 127.0.0.1:5173, contrôle les réponses conjointes puis exécute le script Chromium existant inchangé.

| URL locale réellement demandée par harnais | Méthode | Statut HTTP |
|---|---|---|
| http://127.0.0.1:5173/health/live | GET | 200 |
| http://127.0.0.1:5173/ | GET | 200 |
| http://127.0.0.1:5173/assets/index-Big655uI.js | GET | 200 |
| http://127.0.0.1:5173/assets/index-CEeMJxYe.css | GET | 200 |
| http://127.0.0.1:5173/api/v1/openapi.json | GET | 200 |
| http://127.0.0.1:5173/api/v1/status | GET | 200 |
| http://127.0.0.1:5173/api/v1/private | GET | 403 |
| http://127.0.0.1:5173/absent-joint-xyz/ | GET | 404 |

Navigateur : {"cleanup": {"processClosed": true, "profileRemoved": true}, "serverClosed": true, "threadJoined": true, "guards": [0, 0, 0]}. Les détails Chromium, verdicts UI, requêtes autorisées/refusées et stderr sont conservés dans la preuve CAB du harnais et le checkpoint ; Webtools et réseau de test restent comptés séparément.

| Source officielle consultée par orchestrateur | Attribution |
|---|---|
| https://docs.python.org/3.11/library/socketserver.html | Root seulement, hors production OpenCode |

1 appels web root identifiés pour ces sources ; horodatages précis par appel non conservés. Volumes globaux des autres outils orchestrateur non exposés dans cette télémétrie : N/A. Aucun de ces accès n’est attribué au codeur.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T00:30:07.999000+00:00 |
| Fin — après archivage | 2026-10-02T01:18:36.012210+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 48 min 28 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T00:42:08.620132+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T01:19:16.346674+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 29 | 60.4 % | 29 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 8 | 16.7 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 11 | 22.9 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 48 | 100 % | 48 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-local-test-composition | 2026-10-02T00:42:20.150898+00:00 | 2026-10-02T00:42:26.437471+00:00 | 2026-10-02T00:42:30.466863+00:00 | 6.286572 | 121.358186 | 489 | réussie |
| périodique — créneau 2026-10-02T01:12:20.150898+00:00 | 2026-10-02T01:15:34.265994+00:00 | 2026-10-02T01:15:45.994478+00:00 | 2026-10-02T01:15:51.349540+00:00 | 11.728480 | 95.610302 | 512 | réussie |
| finale après archivage add-local-test-composition | 2026-10-02T01:18:15.928579+00:00 | 2026-10-02T01:18:22.060917+00:00 | 2026-10-02T01:18:26.260358+00:00 | 6.132338 | 116.443971 | 489 | réussie |

Relèves prévues : 3 (100 %) ; réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 6.132338/8.049130/11.728480 s ; débit min/moy/max : 95.610302/111.137486/121.358186 tok/s.

Surcharge sondes : 27437 tokens total API, 1490 tokens sortie, coût API 0.002995300, durées stream mesurées 13.583910 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Brouillons corrigés avant écritures : tests contextmanager sans entrée effective, import Path, attente de calls et MIME incorrects, harnais contournant le helper, traitement HTTP 403, rapport de nettoyage trop tôt, schéma d’enveloppe et gardes PG du cycle. Les fausses alertes OpenCode concernant HTTPError/mode et l’append déjà observé ont été réconciliées avec le contenu natif, les messages, la décision et l’empreinte exacts ; aucune écriture répétée. Le début statistique a été corrigé avec l’horodatage du message SPCMP natif. Quatre réponses HTTP 400 du contrôleur avant décision stockée, GET 404 puis décision unique ; cause non établie. Sonde périodique exécutée à la frontière de mandat sûre avec retard réel de 194,115 s ; aucune relève manquée, trois sondes valides. Warnings D-Bus Chromium conservés en stderr, non fatals ; tous les tests et appels natifs ont réussi. Outil natif de quota Codex absent au début et à la fin : N/A, aucune substitution.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-local-test-composition, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ; requêtes HTTP applicatives limitées à la boucle locale dans le cycle et le navigateur observés. Composition HTTP TEST jointe et cycle WSGI loopback réel, sans composition P0/production globale. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
