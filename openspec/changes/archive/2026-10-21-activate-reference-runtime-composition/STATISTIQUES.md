# Statistiques de la session C07

Change : `activate-reference-runtime-composition`. Archive : `2026-10-21-activate-reference-runtime-composition`. RUN : `cismp4-pixs-04b6968c4b2249d8`. Contextes CAB 440 et 553 ; trois sessions natives : `ses_ea588b5e2ffe1r67qQCBCkFv54`, `ses_ea4b5e64effe9uXxXNSZZENuWt`, `ses_e9ff60618ffeBzNdN4M7cIc1Ne`.

Fenêtre de production : 2026-10-20T17:58:57.820Z → 2026-10-21T20:59:43.043Z (UTC), fixée après archive et sonde finale, avant rédaction. Messages dédupliqués par identifiant, outils par callID. Sondes, rédaction du rapport, publication et gate ultérieurs exclus.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte du modèle non exposée ; agent OpenCode 1.19.3 | opencode-go | high, selon mandats et sondes ; champ absent sur certaines réponses | 3.696 s | 300.032 | N/A — génération seule non mesurée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex / CGPT | N/A — version exacte non exposée | OpenAI | N/A — télémétrie non exposée | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — durée active non exposée |

Dénominateur de temps de service cumulé : N/A. Les bornes de messages et busy CAB incluent outils/attentes ; elles ne mesurent pas la génération seule. Chevauchements et durée calendaire ne sont pas convertis en temps de service.

## 1. Statistiques générales et décisions

Durée calendaire : **27 h 00 min 45 s**, pauses, attentes, tests et archive inclus. Début : réservation C07 contexte 440, avant premier message natif à 2026-10-20T17:59:15.414Z. Fin : relevé natif de quota après archive.

Le brouillon intégré a été consulté d’abord par GET /runs/cismp4-pixs-04b6968c4b2249d8/statistics?format=markdown puis JSON ; contextId=440 restitue l’historique. Les décisions viennent de ces deux contextes, distinctes des appels natifs : request_validation peut échouer avant enregistrement ; poll/get ne créent pas une nouvelle décision. Les anciens GET de décision devenus indisponibles ne sont pas traités comme une absence ; les compteurs historiques sont conservés.

| Décision CAB enregistrée | Nombre | Part |
|---|---:|---:|
| approved | 83 | 95.4 % |
| rejected | 4 | 4.6 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 87 | 100.0 % |


| Provenance CAB | Approuvées | Refusées | Total décisions | Once | Bornes UTC |
|---|---:|---:|---:|---:|---|
| Contexte 440 | 58 (95.1 %) | 3 (4.9 %) | 61 (100.0 %) | 57 | 2026-10-20T17:58:57.820Z → 2026-10-21T19:25:49.067Z |
| Contexte 553 | 25 (96.2 %) | 1 (3.8 %) | 26 (100.0 %) | 23 | 2026-10-21T19:37:01.838Z → 2026-10-21T21:00:03.923Z |

Les compteurs CAB de messages/outils sont des observations et ne sont pas additionnés à l’historique natif. « Terminé autorisé » désigne une fin native sous autorisation automatique ou manuelle, sans prouver une approbation humaine ni un succès métier. Refus = décision de permission explicitement enregistrée ; interruption, timeout et EACCES restent des erreurs techniques sauf preuve distincte de refus.

| Métadonnée native de production | Valeur |
|---|---:|
| Messages | 1340 (100.0 %) |
| Outils dédupliqués | 935 (100.0 %) |
| Tokens input | 9268227 |
| Tokens output | 353131 |
| Tokens reasoning | 124132 |
| Cache read | 248488838 |
| Cache write | 0 |
| Somme du champ cost | 1.519252976 |
| Facturation réelle | N/A — devise et facture non exposées |
| Parties compaction natives | 8 |
| Cycles coordonnés consignés | 8 |

Tokens et cache sont reproduits séparément, sans somme présentée comme tokens uniques. Le champ cost ne constitue pas une facture. Les huit compactages OpenCode sont achevés ; la réussite conjointe est N/A, l’API propriétaire Codex n’étant pas exposée. Checkpoints préservés.

Résultat : 80 cas/contrôles du socle réussis (100.0 %) et une recette C01 à 17 contrôles vrais (100.0 %), sans additionner wrappers ni préparations C03. Trois Bash terminés ont historiquement retourné exit 1 (6.0 % des 50 Bash) ; les recettes ont été corrigées puis réussies. Trois écritures terminées ont divergé du contenu préparé et ont été corrigées sous nouveaux mandats. Les tests et empreintes de [VALIDATION.md](VALIDATION.md) restent les preuves fonctionnelles.

Sondes : 25 relevés valides (100.0 % des relevés conservés), 0 échec conservé (0.0 %). Nombre exhaustif prévu/manqué : N/A — calendrier incomplet pendant pauses/interruption ; aucun relevé rétrospectif reconstruit. TTMT moyen arithmétique 3.696 s, min 1.567 s, max 8.883 s ; débit moyen 300.032 tokens/s, min 75.733, max 1001.580. La sonde initiale utilise les bornes natives texte ; les 24 suivantes le SSE texte et l’horloge monotone.

| Position | Envoi UTC | TTMT s | Tokens/s | Retard connu s | Résultat |
|---|---|---:|---:|---:|---|
| début | 2026-10-20T18:02:14.997Z | 1.567 | 350.214 | N/A | completed |
| reprise +30 min | 2026-10-20T22:06:08.696Z | 1.887 | 605.843 | N/A | completed |
| reprise +60 min | 2026-10-20T22:37:05.850Z | 3.739 | 114.218 | N/A | completed |
| reprise +90 min | 2026-10-20T23:08:24.890Z | 2.528 | 230.101 | 71.494 | completed |
| reprise +120 min | 2026-10-20T23:39:39.283Z | 2.138 | 321.557 | 70.071 | completed |
| reprise +150 min | 2026-10-21T00:10:03.351Z | 2.425 | 93.209 | 20.575 | completed |
| reprise +180 min | 2026-10-21T00:40:24.441Z | 2.747 | 95.429 | 13.832 | completed |
| reprise +210 min | 2026-10-21T01:13:19.029Z | 2.144 | 136.480 | 167.147 | completed |
| reprise +240 min | 2026-10-21T01:43:35.043Z | 2.964 | 264.001 | 10.641 | completed |
| reprise +270 min | 2026-10-21T02:13:44.793Z | 3.433 | 127.565 | 5.133 | completed |
| reprise +300 min | 2026-10-21T02:44:04.537Z | 1.798 | 527.421 | 12.8 | completed |
| reprise +330 min | 2026-10-21T03:14:16.785Z | 2.973 | 82.850 | 9.628 | completed |
| reprise +360 min | 2026-10-21T03:44:31.419Z | 2.727 | 105.023 | 6.236 | completed |
| reprise +390 min | 2026-10-21T04:17:23.845Z | 1.918 | 256.619 | 165.365 | completed |
| reprise +420 min | 2026-10-21T04:49:33.691Z | 3.643 | 75.733 | 126.252 | completed |
| reprise +450 min | 2026-10-21T05:26:27.683Z | 2.606 | 543.490 | 404.289 | completed |
| reprise +480 min | 2026-10-21T06:04:12.874Z | 2.212 | 857.283 | 461.639 | completed |
| reprise +30 min | 2026-10-21T17:37:12.278Z | 5.715 | 272.091 | 19.158 | completed |
| reprise +60 min | 2026-10-21T18:07:33.671Z | 7.134 | 263.705 | 13.726 | completed |
| reprise +90 min | 2026-10-21T18:38:20.655Z | 8.883 | 207.971 | N/A | completed |
| reprise+120min | 2026-10-21T19:10:34.976Z | 6.942 | 236.516 | N/A | completed |
| reprise-sudo | 2026-10-21T19:37:01.988Z | 6.096 | 247.086 | N/A | completed |
| reprise-sudo+30min | 2026-10-21T20:11:09.281Z | 2.247 | 1001.580 | 239.037 | completed |
| périodique-20h41-frontière-compactage | 2026-10-21T20:46:15.427Z | 7.141 | 247.601 | N/A | completed |
| fin-après-archive-C07 | 2026-10-21T20:59:17.019Z | 4.808 | 237.220 | N/A | completed |

Surcharge exclue de la production : 10720 tokens de sortie ; champ cost partiel 0.031690650 sur 23/25 relevés, coût complet N/A (2 absents). Intervalles de texte cumulés ≈58.200 s ; occupation complète N/A, sans assimilation au temps de service. La relève prévue à 20:41 a été envoyée à 20:46 à la frontière de compactage ; son retard est conservé.

## 2. Types de messages et d’outils

| Rôle des messages | Nombre | Part |
|---|---:|---:|
| user | 446 | 33.3 % |
| assistant | 894 | 66.7 % |
| Total | 1340 | 100.0 % |


| Type de partie native | Nombre | Part |
|---|---:|---:|
| text | 1118 | 23.3 % |
| step-start | 893 | 18.6 % |
| reasoning | 957 | 19.9 % |
| tool | 935 | 19.5 % |
| step-finish | 886 | 18.5 % |
| compaction | 8 | 0.2 % |
| Total | 4797 | 100.0 % |


| Terminaison des messages assistant | Nombre | Part |
|---|---:|---:|
| sans terminaison | 8 | 0.9 % |
| tool-calls | 536 | 60.0 % |
| stop | 350 | 39.1 % |
| Total | 894 | 100.0 % |


| Catégorie | Total (part) | Terminé autorisé (taux) | Refus explicite (taux) | Erreur technique (taux) | En cours |
|---|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 145 (15.5 %) | 144 (99.3 %) | 0 (0.0 %) | 1 (0.7 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 101 (10.8 %) | 101 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 79 (8.4 %) | 79 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 285 (30.5 %) | 280 (98.2 %) | 1 (0.4 %) | 4 (1.4 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 91 (9.7 %) | 74 (81.3 %) | 0 (0.0 %) | 17 (18.7 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 21 (2.2 %) | 18 (85.7 %) | 0 (0.0 %) | 3 (14.3 %) | 0 (0.0 %) |
| bash | 50 (5.3 %) | 48 (96.0 %) | 0 (0.0 %) | 2 (4.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 39 (4.2 %) | 39 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 46 (4.9 %) | 46 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 43 (4.6 %) | 43 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 28 (3.0 %) | 27 (96.4 %) | 0 (0.0 %) | 1 (3.6 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 2 (0.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 5 (0.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 935 (100.0 %) | 906 (96.9 %) | 1 (0.1 %) | 28 (3.0 %) | 0 (0.0 %) |


Les trois codes de test exit 1 sont inclus dans les fins natives Bash, sans être des refus. Les timeouts MCP restent visibles, même si la même approval_id a ensuite été acquittée. Les refus de lecture des reçus UID 1000 restent conservés ; CGPT les a attestés séparément sans relâcher leurs permissions.

## 3. Fichiers modifiés

Le tableau compte des **tentatives**, pas des lignes : 33 Write/Edit et 13 Bash à cible littérale d’écriture identifiée, soit 46 (100.0 %), dont 44 terminées (95.7 %), 0 refus explicite dans ce sous-ensemble (0.0 %) et 2 erreurs techniques (4.3 %). Le Write interrompu avant arguments n’est pas attribué à un faux chemin. Les autres effets de fixtures/cache restent dans Bash, sans déduire un nombre d’écritures par fichier.

| Catégorie | Total (part) | Terminé autorisé (taux) | Refus explicite (taux) | Erreur technique (taux) | En cours |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/activate-reference-runtime-composition/proposal.md | 5 (10.9 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/activate-reference-runtime-composition/design.md | 5 (10.9 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/activate-reference-runtime-composition/requirements.md | 4 (8.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/host_asgi.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_backend_host_asgi_closed.py | 2 (4.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/host_composition.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_backend_host_composition_postgres.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/host_lifespan.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_backend_host_lifespan_postgres.py | 2 (4.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/auth_pg_test_support.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/host_plan.py | 2 (4.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_backend_host_plan.py | 2 (4.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/host_runtime.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_backend_host_runtime.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/host_entry.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_backend_host_entry_guards.py | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_backend_host_entry_systemd.py | 7 (15.2 %) | 6 (85.7 %) | 0 (0.0 %) | 1 (14.3 %) | 0 (0.0 %) |
| N/A — Write interrompu avant arguments | 1 (2.2 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/activate-reference-runtime-composition/tasks.md | 2 (4.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/activate-reference-runtime-composition/VALIDATION.md | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/proposal.md | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/design.md | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/requirements.md | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/VALIDATION.md | 1 (2.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 46 (100.0 %) | 44 (95.7 %) | 0 (0.0 %) | 2 (4.3 %) | 0 (0.0 %) |


Les 14 fichiers source/recette et leurs empreintes sont dans [VALIDATION.md](VALIDATION.md). Cinq documents C07 sont modifiés : proposal.md, design.md, requirements.md, tasks.md et VALIDATION.md ; ce rapport est créé après la fenêtre. `.openspec.yaml` est seulement déplacé. Le déplacement unique de six fichiers vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-21-activate-reference-runtime-composition` est attesté par `call_01a1603f8eed7667ac86418fe021906d`. Les liens déplacés sont corrigés, aucun canon modifié. Artefacts régénérables : tests/runtime/c07-cache ; reçus publics : output/cismp/cismp4-pixs-04b6968c4b2249d8. Aucune opération Git.

## 4. Commandes

50 Bash natifs (100.0 %) : 48 fins natives (96.0 %), 0 refus explicitement typé par l’outil (0.0 %), 2 erreurs/interruption (4.0 %). Les quatre mandats refusés avant effet constituent la série distincte ci-dessous.

| Catégorie | Total (part) | Terminé autorisé (taux) | Refus explicite (taux) | Erreur technique (taux) | En cours |
|---|---:|---:|---:|---:|---:|
| Prévol /usr/bin/true | 13 (26.0 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 5 (10.0 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python : contenu borné et empreintes | 15 (30.0 %) | 14 (93.3 %) | 0 (0.0 %) | 1 (6.7 %) | 0 (0.0 %) |
| Python : syntaxe et recettes | 16 (32.0 %) | 15 (93.8 %) | 0 (0.0 %) | 1 (6.3 %) | 0 (0.0 %) |
| Archivage OpenSpec | 1 (2.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 50 (100.0 %) | 48 (96.0 %) | 0 (0.0 %) | 2 (4.0 %) | 0 (0.0 %) |


| Mandat refusé avant effet | Libellé ≤100 caractères | Occurrences et part | Statut conservé |
|---|---|---:|---|
| `req-c4-check-b7ad9aeb` | `/home/devops/python/current/bin/python3 -B -c 'import hashlib,json,re from pathlib import Path p=Pa…` | 1 (25.0 %) | REFUSED_NO_EFFECT |
| `req-c4-check-748a0a16` | `/usr/bin/true` | 1 (25.0 %) | REJECTED_NO_EFFECT |
| `req-c4-08d69e50` | `/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src:/home/devops…` | 1 (25.0 %) | REJECTED_BEFORE_EFFECT |
| `req-c4-60c87147` | `/home/devops/python/current/bin/python3 -B -c 'import hashlib,json,py_compile from pathlib import P…` | 1 (25.0 %) | REJECTED_DIVERGENT_NATIVE_NO_EFFECT |
| Total | — | 4 (100.0 %) | Sans effet prouvé |

Les commandes reformulées restent refusées sans normalisation. Aucun suffixe, alias ni nouvelle permission ne remplace une once consommée. Un seul appel CLI d’archive ; corrections de liens distinctes. Aucun Git ni déploiement.

Exception hôte autorisée distinctement : bancs temporaires de 45 s par sudo pour la seule unité `pixs-c07-c4-entry-0593a443.service`, contrôleur UID 0 / consommateur UID 1000. Les premiers essais ont échoué et sont conservés ; le final réussit 17/17, arrêt natif attesté et sudo-k exit 0. Ces actions hors OpenCode ne sont ajoutées ni aux 50 Bash ni aux once. Nombre exhaustif des commandes internes systemd/sudo : N/A ; reçus terminal et parent/enfant conservés. Fixtures publiques, mode null fonctionnel, aucun secret réel ni connexion PG dans cette recette.

## 5. Accès web

OpenCode : 0 outil webfetch/websearch dans les trois sessions. Taux par résultat N/A — dénominateur zéro. Les deux consultations publiques connues de l’orchestrateur sont une série séparée ; elles ne prétendent pas couvrir toutes ses activités de conversation.

| URL consultée (≤100 caractères) | Acteur | Statut | Nombre et part |
|---|---|---|---:|
| https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/ | CGPT | Approuvée et consultée — web.run open | 1 (50.0 %) |
| https://asgi.readthedocs.io/en/stable/specs/lifespan.html | CGPT | Approuvée et consultée — web.run open | 1 (50.0 %) |
| Total connu | CGPT | 2 approuvées (100.0 %), 0 refus (0.0 %), 0 erreur (0.0 %) | 2 (100.0 %) |

Aucune URL refusée enregistrée dans ces observations. Aucun contenu projet ni secret transmis selon les reçus. Les API locales OpenCode/CAB ne sont pas présentées comme des visites externes.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-20T17:58:57.820Z (UTC) |
| Fin — après archivage | 2026-10-21T20:59:43.043Z (UTC) |
| Durée globale (pauses et attentes incluses) | 27 h 00 min 45 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-20T17:58:49.631637+00:00 (UTC) | 34 % | 2026-10-27T06:33:48.000Z (UTC) |
| Après — après archivage de la spécification | 2026-10-21T20:59:43.043Z (UTC) | 100 % | 2026-10-27T06:33:48.000Z (UTC) |
| Différence après − avant | — | 66 points de pourcentage | — |

Source : `mcp__codex_app__get_usage_limits`, quota codex, fenêtre 10080 min ; même compte et même reset vérifiés sans publier l’identifiant. Le quota est partagé : cette variation pendant 27 h 00 min 45 s peut inclure d’autres tâches simultanées. Aucune attribution exclusive à C07, conversion en tokens ou en coût.

Totaux par domaine **des 935 outils natifs**, sans doublon : Write/Edit dans fichiers ; toute commande Bash dans commandes, même si elle écrit un fichier. Les 46 tentatives de section 3 recouvrent 13 Bash et ne sont donc pas réadditionnées. Les deux visites web CGPT et les 25 sondes restent séparées.

| Catégorie | Total (part) | Terminé autorisé (taux) | Refus explicite (taux) | Erreur technique (taux) | En cours |
|---|---:|---:|---:|---:|---:|
| Fichiers natifs Write/Edit | 33 (3.5 %) | 32 (97.0 %) | 0 (0.0 %) | 1 (3.0 %) | 0 (0.0 %) |
| Commandes Bash | 50 (5.3 %) | 48 (96.0 %) | 0 (0.0 %) | 2 (4.0 %) | 0 (0.0 %) |
| Web natif OpenCode | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 852 (91.1 %) | 826 (96.9 %) | 1 (0.1 %) | 25 (2.9 %) | 0 (0.0 %) |
| Total | 935 (100.0 %) | 906 (96.9 %) | 1 (0.1 %) | 28 (3.0 %) | 0 (0.0 %) |


| Contexte CAB | Réservé s | Busy s | Idle s | Natif inconnu s | Attente ressource s | Détention partagée s | Gels exceptionnels s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 440 | 91611.247 | 6110.778 | 85492.066 | 8.403 | 17.613 | 5226.783 | 12185.846 |
| 553 | 4982.086 | 1624.519 | 3357.389 | 0.178 | 0.000 | 1555.216 | 0.000 |

Durées d’observation distinctes du temps de génération ; elles peuvent se recouvrir. Les interruptions du contrôleur conservent une lacune inconnue, sans inventer productivité ni gain causal.

À la borne : 80 cas/contrôles et recette native C01 17/17 réussis ; OpenSpec strict valide, archive unique réussie, 14 empreintes sources conservées. Les 107 exigences/131 scénarios de traçabilité ne sont pas 131 succès. P0, C14/C17/C18/C19, binaire, ressources et drain global non qualifiés. Git, push et déploiement non exécutés. OpenCode/CAB et les autres RUN préservés. Fixtures et reçus sans secret réel ; aucun mot de passe enregistré, autorisation sudo invalidée.

Ce rapport, son contrôle natif, la publication CAB et le gate local sont effectués après la fenêtre de mesure. Aucun état terminal n’est déduit de ce brouillon. La réservation reste conservée jusqu’à leurs preuves et à la libération ciblée, sans second change ni arrêt des services communs.
