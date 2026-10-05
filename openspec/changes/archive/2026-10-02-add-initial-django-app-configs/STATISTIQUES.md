# STATISTIQUES — add-initial-django-app-configs

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T01:25:07.538000+00:00 ; fin après archivage et sonde finale 2026-10-02T02:16:40.711602+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 20.527 s | 87.052 | 525.604 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 124 | 100 % |
| Appels outils | 106 | 100 % |
| Approuvé et exécuté | 99 | 93.4 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 7 | 6.6 % |
| Durée calendaire avec pauses | 00 h 51 min 33 s | 100 % de l’intervalle |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 31030398 | 93.9 % |
| cache_write | 0 | 0.0 % |
| input | 1975085 | 6.0 % |
| output | 31820 | 0.1 % |
| reasoning | 19574 | 0.1 % |
| total | 33056877 | 100 % du total API |

Coût agrégé API : 0.269848096 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 20 | 100.0 % |
| TOTAL | 20 | 100 % |

Résultats finaux : 602 tests unitaires et 173 tests d’intégration réels réussis (mandats distincts, exit 0). Contrôle AST Python 3.11 : 3 sources et 4 snippets ; 61 empreintes protégées et 3 artefacts dist inchangés ; UTF-8/LF et texte approuvé exact. Validation OpenSpec stricte avant/après cochage valid true, 0 issues. Registre Django réel TEST pour Kernel/Core/Exemple, import sans configure/setup/FS, connexions PG et sockets gardées à zéro ; négatifs doublon/chemin inconnu observés. Huit tâches prouvées, archivage skip-specs exit 0 ; delta normatif mot-à-mot canonique. Aucun serveur applicatif ni navigateur nécessaire dans ce change ; les preuves navigateur du composant précédent ne lui sont pas attribuées.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 95 | 76.6 % |
| user | 29 | 23.4 % |
| TOTAL | 124 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 154 | 30.5 % |
| step-finish | 94 | 18.6 % |
| step-start | 95 | 18.8 % |
| text | 56 | 11.1 % |
| tool | 106 | 21.0 % |
| TOTAL | 505 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| absent | 1 | 1.1 % |
| stop | 27 | 28.4 % |
| tool-calls | 67 | 70.5 % |
| TOTAL | 95 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 9 | 8.5 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 3 | 2.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 20 | 18.9 % | 20 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 3 | 2.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 5 | 4.7 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % |
| grep | 3 | 2.8 % | 1 | 33.3 % | 0 | 0.0 % | 2 | 66.7 % |
| read | 55 | 51.9 % | 51 | 92.7 % | 0 | 0.0 % | 4 | 7.3 % |
| write | 8 | 7.5 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 106 | 100 % | 99 | 93.4 % | 0 | 0.0 % | 7 | 6.6 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f06b54883ffe63YLISnmeNo8Pf | 42 | oui |
| ses_f05b5f016ffezu6AlQZxDwC27H | 82 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-django-app-configs/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-django-app-configs/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-django-app-configs/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-django-app-configs/specs/initial-application-bootstrap/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-django-app-configs/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/apps.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_initial_django_app_configs_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_initial_django_app_configs.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-django-app-configs. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 33.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/true | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web OpenCode exécuté. Les tests Django remplissent le registre en mémoire, sans requête HTTP ou navigateur ; gardes PG et socket à zéro. Les classes d’adaptation sont chargées par chemins explicites, sans hook de pipeline/P0. Sept outils de l’ancienne session ayant consulté une source exclue .venv sont classés erreurs de protocole, même si l’outil natif a terminé. Ils ne sont jamais comptés comme accès autorisés. La session fautive a été interrompue et remplacée après réconciliation puis readiness et test CAB frais.

| Source officielle consultée par orchestrateur | Attribution |
|---|---|
| https://docs.djangoproject.com/en/5.2/ref/applications/ | Root seulement, hors production OpenCode |
| https://github.com/django/django/blob/stable/5.2.x/django/apps/config.py | Root seulement, hors production OpenCode |
| https://raw.githubusercontent.com/django/django/stable/5.2.x/django/apps/config.py | Root seulement, hors production OpenCode |

3 appels web root identifiés pour ces sources ; horodatages précis par appel non conservés. Volumes globaux des autres outils orchestrateur non exposés dans cette télémétrie : N/A. Aucun de ces accès n’est attribué au codeur.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T01:25:07.538000+00:00 |
| Fin — après archivage | 2026-10-02T02:16:40.711602+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 51 min 33 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T01:33:18.479378+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T02:17:26.343567+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 86 | 81.1 % | 79 | 91.9 % | 0 | 0.0 % | 7 | 8.1 % |
| Commandes | 9 | 8.5 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 11 | 10.4 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 106 | 100 % | 99 | 93.4 % | 0 | 0.0 % | 7 | 6.6 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| début add-initial-django-app-configs | 2026-10-02T01:33:56.259514+00:00 | 2026-10-02T01:34:03.107292+00:00 | 2026-10-02T01:34:13.262807+00:00 | 6.847774 | 51.892950 | 527 | réussie |
| périodique — créneau 2026-10-02T02:03:56.259514+00:00 | 2026-10-02T02:09:37.525977+00:00 | 2026-10-02T02:09:40.104651+00:00 | 2026-10-02T02:09:46.662803+00:00 | 2.578666 | 77.308287 | 507 | réussie |
| finale — après archivage | 2026-10-02T02:15:40.580172+00:00 | 2026-10-02T02:16:32.736185+00:00 | 2026-10-02T02:16:36.775465+00:00 | 52.156010 | 131.954144 | 533 | réussie |

Relèves prévues : 3 (100 %) ; réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 2.578666/20.527483/52.156010 s ; débit min/moy/max : 51.892950/87.051794/131.954144 tok/s.

Surcharge sondes : 28391 tokens total API, 1567 tokens sortie, coût API 0.002372210, durées stream mesurées 20.752963 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Sept outils read/glob/grep de l’ancienne session ont consulté le SDK dans .venv, source explicitement exclue : comptés comme erreurs de protocole malgré statut completed. Session interrompue, aucun Bash/écriture ni permission consommée après le brouillon, 61 empreintes/delta intacts ; nouvelle session persistante et politique de lecture durcie, broker_readiness réel puis test CAB unique réussis. La nouvelle session a d’abord confondu SID et instance broker dans le texte INIT ; corrigé explicitement avant mandats. Surcharge temporaire du fournisseur rétablie automatiquement sans changement de modèle/HIGH et sans répétition d’écriture. README comportait un LF final supplémentaire après son append ; mandat consommé clôturé, READY puis test CAB neuf et correction minimale sous nouveau mandat, hash attendu rétabli. Réponses HTTP 400 de décision avant stockage ont été rapprochées par GET 404 et nouvelle tentative de décision corrélée, cause non établie ; aucune décision persistée dupliquée. Statistiques couvrent les deux SID ; contenus bruts SDK interdits non conservés comme sources ni recopiés.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-django-app-configs, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ni réseau applicatif dans les tests observés. Enregistrement effectif Kernel/Core/exemple dans le registre Django TEST, sans activation pipeline/P0/readiness globale. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
