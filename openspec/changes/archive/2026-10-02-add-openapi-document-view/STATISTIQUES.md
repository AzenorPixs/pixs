# STATISTIQUES — add-openapi-document-view

Périmètre : /home/devops/datas/pixs. Début 2026-10-01T23:29:06.900000+00:00 ; fin après archivage et sonde finale 2026-10-02T00:21:38.645946+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 5.821 s | 96.082 | 557.080 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 97 | 100 % |
| Appels outils | 54 | 100 % |
| Approuvé et exécuté | 54 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 00 h 52 min 31 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 38880486 | 91.1 % |
| cache_write | 0 | 0.0 % |
| input | 3743835 | 8.8 % |
| output | 48027 | 0.1 % |
| reasoning | 28674 | 0.1 % |
| total | 42701022 | 100 % du total API |

Coût agrégé API : 0.467484672 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 18 | 100.0 % |
| TOTAL | 18 | 100 % |

Résultats finaux : 598 tests unitaires et 168 tests d’intégration réussis, première exécution réelle après récupération CAB. Document OpenAPI3.1.0 du sous-ensemble borné publié dans DjangoClient en mémoire, corps exactGET/HEAD vide et longueurGET/POST405Allow, capacitéGETenveloppe cohérente avec schéma déclaré, resolve/public403/404autremajeure et guardsPG/socket0. ASTPython3.11 trois sources/quatre snippets, UTF8LF,44 empreintes préexistantes et trois dist préservés. Huit tâches cochées sur preuves, strict préparation/final/aprèscochage tous validtruefailed0. Archive skip-specs réussie, cinq empreintes d’artefacts conservées. Pas de preuve de compatibilité comportementale, d’enforcement build des ruptures, ni de composition P0 ou mise en production.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 70 | 72.2 % |
| user | 27 | 27.8 % |
| TOTAL | 97 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 137 | 35.6 % |
| step-finish | 70 | 18.2 % |
| step-start | 70 | 18.2 % |
| text | 54 | 14.0 % |
| tool | 54 | 14.0 % |
| TOTAL | 385 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 27 | 38.6 % |
| tool-calls | 43 | 61.4 % |
| TOTAL | 70 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 8 | 14.8 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 18 | 33.3 % | 18 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 4 | 7.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 12 | 22.2 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 18.5 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 54 | 100 % | 54 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f06b54883ffe63YLISnmeNo8Pf | 97 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-openapi-document-view/.openspec.yaml | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-openapi-document-view/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-openapi-document-view/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-openapi-document-view/specs/api/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-openapi-document-view/tasks.md | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/openapi_document_view.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_openapi_document_view_integration.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_openapi_document_view.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 10 | 100 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-openapi-document-view. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 50.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 37.5 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/true | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/pixs/.venv/bin/python -B -c … | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web OpenCode exécuté. Les requêtes Client Django encapsulées dans les tests Bash sont en mémoire, gardes socket/psycopg zéro ; elles ne sont pas des visites navigateur ou connexions externes. Chemins réellement testés : /api/v1/openapi.json (GET/HEAD/POST), /api/v1/status (GET), /api/v1/private (GET/POST/HEAD), /api/v2/openapi.json (GET).

| Source officielle consultée par orchestrateur | Attribution |
|---|---|
| https://json-schema.org/draft/2020-12/json-schema-core | Root seulement, hors production OpenCode |
| https://json-schema.org/draft/2020-12/json-schema-validation | Root seulement, hors production OpenCode |
| https://spec.openapis.org/oas/v3.1.0.html | Root seulement, hors production OpenCode |

3 appels web root identifiés pour ces sources ; horodatages précis par appel non conservés. Volumes globaux des autres outils orchestrateur non exposés dans cette télémétrie : N/A. Aucun de ces accès n’est attribué au codeur.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-01T23:29:06.900000+00:00 |
| Fin — après archivage | 2026-10-02T00:21:38.645946+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 52 min 31 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-01T23:34:56.291370+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T00:23:45.591895+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 36 | 66.7 % | 36 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 8 | 14.8 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 10 | 18.5 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 54 | 100 % | 54 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-openapi-document-view | 2026-10-01T23:34:56.315030+00:00 | 2026-10-01T23:34:58.461194+00:00 | 2026-10-01T23:35:02.353279+00:00 | 2.146159 | 133.861283 | 521 | réussie |
| périodique — créneau 2026-10-02T00:04:56.315030+00:00 | N/A — observateur interrompu | N/A — non mesuré | N/A — non mesuré | N/A | N/A | 525 | échouée |
| finale après archivage add-openapi-document-view | 2026-10-02T00:21:18.571608+00:00 | 2026-10-02T00:21:28.067256+00:00 | 2026-10-02T00:21:36.763137+00:00 | 9.495647 | 58.303427 | 507 | réussie |

Relèves prévues : 3 (100 %) ; réussies 2 (66.7 %), échouées 1 (33.3 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 2.146159/5.820903/9.495647 s ; débit min/moy/max : 58.303427/96.082355/133.861283 tok/s.

Surcharge sondes : 28002 tokens total API, 1553 tokens sortie, coût API 0.002294410, durées stream mesurées 12.587976 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Brouillons corrigés avant toute source: deux snippets mal fermés, plan invalide construit avant try, schéma capacité ne décrivant pas enveloppe, validations chemins/code/media/structure insuffisantes, classe_FakeRequest indéfinie et appelée avant settings.configure, faux positif64KiB ajoutant pad interdit. Roota remplacé scénarios de bornes/refus pertinents, harmonisé enum numérique/bool/required/trailing slash et assertions Client. Une réserve NDOC relisait anciencorps: source authoritative vérifiée par API ne contenait aucun_FakeRequest; correctionconfirmée et bytes exacts troisécritures. Deux NameErrorroot re manquant pendant extractionbrouillons, aucun effetsource; helper explicite corrigé. Plusieurs400contrôleur avant GETdecision404 puis décision unique corrélée approuvée; cause non prouvée. Sonde +30 envoyée aprèssource3 a timeout55s observateur, sortie40lignes nativement terminée87.553s aprèsentréeAPI, timingSSE perdu doncTTMT/débitN/A sansreconstruction. Sessionjetable supprimée; récupérationobservée brokerREADY0IDLE/CABtestneuf puis suites nonprouvées seulement, aucuneéditionrejouée. Observateur async/pollsbornés180s tentative durable/finallycleanup fonctionne sondefinale. Pas d’erreur d’outil natif/code ni testfailed observé danslesbornesproduction; erreur observateur et draft distinctes. Copier-coller matrice 'Clientdist' corrigé: Client enmémoire seulement et distpréservé; strictOpenSpec ne prouvepas enforcementbuildruptures.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-openapi-document-view, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ni réseau applicatif dans les tests observés. Publication HTTP document OpenAPI borné pour contrat explicite; preuve Client TEST seule, aucune compatibilité comportementale/composition P0/production globale revendiquée. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
