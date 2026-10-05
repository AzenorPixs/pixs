# STATISTIQUES — add-initial-correlated-log

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T03:25:17.521539+00:00 ; fin après archivage et sonde finale 2026-10-02T04:32:13.273159+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 4.988 s | 187.587 | 393.059 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 148 | 100 % |
| Appels outils | 89 | 100 % |
| Approuvé et exécuté | 88 | 98.9 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 1 | 1.1 % |
| Durée calendaire avec pauses | 01 h 06 min 55 s | 100 % de l’intervalle |

| Erreur de réponse fournisseur hors outil | Nombre | Part des réponses assistants |
|---|---|---|
| Réponses avec erreur API native | 0 | 0.0 % |
| Dont HTTP 503 | 0 | 0.0 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 33406877 | 96.3 % |
| cache_write | 0 | 0.0 % |
| input | 1197678 | 3.5 % |
| output | 52636 | 0.2 % |
| reasoning | 23155 | 0.1 % |
| total | 34680346 | 100 % du total API |

Coût agrégé API : 0.201739754 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 23 | 95.8 % |
| EXPIRED | 1 | 4.2 % |
| TOTAL | 24 | 100 % |

Résultats finaux : 608 tests unitaires en 3,606 s et 175 tests d’intégration en 4,167 s, sous mandats distincts avec sortie 0. Import du helper sans Django : aucune tentative et dix gardes FS/PG/socket à zéro. Appels valides, rejets et échecs des sinks sous treize gardes FS/PG/socket/setup/configure à zéro ; settings.configured et apps.ready restent faux. Le parseur version 00 accepte les 256 valeurs de flags avec sampled calculé par masque, dont 09 ; les UUID de toutes versions/variantes, nil et max conservent la forme canonique de l’API existante. Les types incorrects et objets forgés échouent avant accès au sink. JSON canonique de six champs réellement émis vers StringIO ; les sinks défaillants observent un seul appel, un effet éventuellement partiel, aucune relance, aucun flush ni close et un diagnostic fixe sans valeur brute. Intégration des trois manifests réels par discover/validate/resolve, trois lignes partageant leurs identifiants dans un StringIO joint, double appel byte-identique. AST Python 3.11 des trois sources et quatre programmes de test, UTF-8/LF, 70 empreintes et trois fichiers du build intacts, README en append seul. Validations OpenSpec strictes avant code et avant/après cochage : valid true, aucune erreur. Huit tâches prouvées puis archivage skip-specs réussi, delta observability identique à la norme. Ce sous-jalon prouve seulement le journal local ; métriques, traces, propagation, activation, P0 et disponibilité globale restent à prouver.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 109 | 73.6 % |
| user | 39 | 26.4 % |
| TOTAL | 148 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 186 | 32.6 % |
| step-finish | 109 | 19.1 % |
| step-start | 109 | 19.1 % |
| text | 78 | 13.7 % |
| tool | 89 | 15.6 % |
| TOTAL | 571 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| stop | 39 | 35.8 % |
| tool-calls | 70 | 64.2 % |
| TOTAL | 109 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 12 | 13.5 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |
| cgpt-validation_broker_readiness | 9 | 10.1 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 4 | 4.5 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 24 | 27.0 % | 24 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 1.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 6 | 6.7 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 4 | 4.5 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 19 | 21.3 % | 19 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 11.2 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 89 | 100 % | 88 | 98.9 % | 0 | 0.0 % | 1 | 1.1 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f0585b3f8ffemDsCc37O0oMydP | 148 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-correlated-log/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-correlated-log/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-correlated-log/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-correlated-log/specs/observability/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-correlated-log/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/correlated_log.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_correlated_log_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_correlated_log.py | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-correlated-log. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autre | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 4 | 33.3 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 3 | 25.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 2 | 16.7 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| Tests intégration | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 12 | 100 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /home/devops/node/current/bin/node --input-type=module -e 'import{readFile}from"node:fs/promise… | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 25.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/true | 3 | 25.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 8.3 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| [7] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [8] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 12 | 100 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Journal local vers StringIO fourni caller : aucun serveur HTTP ni navigateur nécessaire ou lancé par ce change. Aucun outil web de production OpenCode exécuté. Recherche primaire orchestrateur séparée : 1 appel web.open https://www.w3.org/TR/trace-context/ (W3C Recommendation 23Nov2021) pendant sélection, réussi ; pas attribué au codeur ni ajouté aux sommes de production. Évaluation fournisseur PLLM antérieure hors bornes. Volumes complets autres outils orchestrateur non exposés dans cette télémétrie : N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T03:25:17.521539+00:00 |
| Fin — après archivage | 2026-10-02T04:32:13.273159+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 06 min 55 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — préparation après sélection | 2026-10-02T03:39:52.349081+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T04:34:56.904689+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 66 | 74.2 % | 66 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 12 | 13.5 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |
| Fichiers | 11 | 12.4 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 89 | 100 % | 88 | 98.9 % | 0 | 0.0 % | 1 | 1.1 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| initiale — journal corrélé local | 2026-10-02T03:39:52.383202+00:00 | 2026-10-02T03:39:58.384700+00:00 | 2026-10-02T03:40:00.120821+00:00 | 6.001498 | 281.661937 | 489 | réussie |
| périodique — créneau 2026-10-02T04:09:52.383202+00:00 | 2026-10-02T04:15:14.308938+00:00 | 2026-10-02T04:15:17.452796+00:00 | 2026-10-02T04:15:20.940902+00:00 | 3.143857 | 140.190737 | 489 | réussie |
| finale — après archivage journal corrélé | 2026-10-02T04:31:53.186807+00:00 | 2026-10-02T04:31:59.005580+00:00 | 2026-10-02T04:32:02.617892+00:00 | 5.818770 | 140.906974 | 509 | réussie |

Relèves prévues : 3 (100 %) ; réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 3.143857/4.988042/6.001498 s ; débit min/moy/max : 140.190737/187.586549/281.661937 tok/s.

Surcharge sondes : 27753 tokens total API, 1487 tokens sortie, coût API 0.002244610, durées stream mesurées 8.836541 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Le développeur a annulé le minuteur de 07 h 30 et la fermeture OpenCode. Mandat 91699c1a5ca2 : worker identifié PID 78043 terminé par SIGTERM (état Z), OpenCode PID 37087/start130319 toujours vivant. Le RUN continue sans échéance jusqu’à la clôture conforme globale. La première proposition de simple JSON sans émission a été rejetée avant écriture ; les brouillons ont ensuite été complétés avant autorisation pour couvrir les gardes, les UUID, les sinks et le contenu émis. L’écriture unitaire 1193a27e405d visait le fichier autorisé mais a changé un échappement Unicode : réconciliation des seules cibles, READY et test true 05151236220e, correction minimale 728436fff5d0 vers chr(0xD800), puis suites 608/175 réussies. Le mandat de contrôle 04282e71e0e2 comptait 2 142 caractères pour une limite du contrôleur de 2 000 : notification FAILED, GET décision 404, polls puis EXPIRED observé, aucune exécution native ; clôture et progression effacée, récupération READY/test true 702fe622bcc7/READY. Une limite de longueur est maintenant vérifiée avant chaque soumission. Le premier contrôle raccourci cb409c30cfe8 contenait une erreur de remplacement introduite par CGPT : exit 1 dès la lecture d’un chemin inexistant, aucune écriture ni exécution des sources. Correction par tokens, équivalence AST statique, récupération READY/test true 67f75f0ef97d, réconciliation d’un pending transitoire, puis contrôle 433bfd88b288 réussi. Cet échec Bash concerne le contrôle préparé par CGPT, pas les suites du projet. Un TypeError du compacteur et un format de métadonnées statistiques ont été corrigés avant toute publication, sans effet projet. Les autres HTTP 400 temporaires lors de la décision ont été rapprochés d’un GET 404 puis d’une décision unique ; leur cause reste inconnue. La sonde prévue à 04:09:52 a été lancée à 04:15:14 après la récupération CAB, avec son retard réel conservé ; aucune relève manquée recréée. Les tests PostgreSQL ont été autorisés pour les prochains jalons ; aucune variable de project.env ni connexion PostgreSQL n’a été utilisée dans ce change. Aucun read/glob/grep sur une source SDK ou exclue ; le traceback du contrôle a seulement montré les chemins du runtime Python.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-correlated-log, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ni réseau applicatif dans les tests observés. Journal local initial réellement émis vers sink caller avec corrélation UUID existante et traceparent W3C00 ; sans métriques/traces/propagation ni activation globales. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
