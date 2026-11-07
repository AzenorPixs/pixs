# STATISTIQUES — NotificationChannel

Change : add-initial-notification-channel-vocabulary. Archive : openspec/changes/archive/2026-10-05-add-initial-notification-channel-vocabulary. RUN parent : cismp-pixs-20260929-2033.

Périmètre des chiffres : historique natif intégral des cinq sessions de reprise ci-dessous, arrêté après archivage et sondes finales, avant rédaction. La session de préparation ses_ef7971176ffeR7zOxqw3EO7ZZB renvoie HTTP404 : ses cinq écritures et trois validations restent prouvées dans l’état parent ; ses messages, outils supplémentaires, tokens et coût complets sont N/A. Les tableaux numériques principaux couvrent exclusivement la reprise, sans présenter cette couverture partielle comme exhaustive du cycle. Les sondes et la rédaction de ce rapport sont séparées de la production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A — version du modèle non exposée | opencode-go | xhigh | 3.851 s (2 sondes valides) | 79.206 | N/A — génération non isolée des attentes/outils |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | N/A — identité exacte du modèle non exposée | OpenAI | N/A — télémétrie native absente | N/A — non sondé | N/A — non sondé | N/A — durée active absente |

Les paramètres qwen3.8-flash/opencode-go/xhigh sont attestés par 173 messages assistant de production. Le temps de service cumulé et son dénominateur sont N/A : les durées créées/complétées incluent les attentes CAB et les outils, et ne constituent pas des durées de génération. Aucun pourcentage de service n’est déduit de la durée calendaire. OpenCode 1.18.34 est observé pour la reprise ; ce numéro ne constitue pas une version du modèle.

## 1. Statistiques générales et décisions

Durée calendaire du change, pauses et attentes incluses : 04 h 48 min 51 s. Début 2026-10-05T05:19:20.055492+00:00, fin 2026-10-05T10:08:11.753919+00:00. Préparation interrompue explicitement le 05 octobre à05:30:02 UTC ; première activité de récupération de reprise à08:12:24 UTC ; nouvelle collecte de sondes de codage à08:43:06 UTC.

| Session native | Messages de reprise | Part |
| --- | --- | --- |
| ses_ef4e198b6ffe0UjYsUuNtPdk5W | 12 | 5.1 % |
| ses_ef4da7d24ffeDBPezoDqRzc5yZ | 12 | 5.1 % |
| ses_ef4d1368bffegLLCFezG4PZQU4 | 43 | 18.4 % |
| ses_ef4b9db2cffeVw8wqAjyodfb9d | 67 | 28.6 % |
| ses_ef4a0eddaffelV674mXhFIX6x1 | 100 | 42.7 % |
| Total | 234 | 100 % |

Convention : un appel de transport MCP achevé est compté exécuté, y compris lorsqu’il transporte une décision CAB de refus ; les décisions CAB sont comptées séparément ci-dessous. Une approbation/exécution peut relever des permissions automatiques de lecture ou d’une décision manuelle ; un succès ne prouve pas à lui seul une autorisation manuelle. Un Bash de retour non nul est une erreur de validation. Un refus explicite de permission est distingué d’une interruption/erreur technique.

| Décision CAB finale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 33 | 91.7 % |
| NEEDS_CLARIFICATION | 1 | 2.8 % |
| REJECTED | 2 | 5.6 % |
| Total | 36 | 100 % |

37 appels request_validation ; 36 requestId distincts avec statut disponible ; un appel en erreur technique, et un identifiant réutilisé par l’agent, incidents conservés. Les deux décisions REJECTED ne prouvent pas l’exécution de leurs cibles.

| Télémétrie production de reprise | Valeur |
| --- | --- |
| input | 1038 |
| output | 76097 |
| reasoning | 0 |
| cache_write | 402078 |
| cache_read | 9608152 |
| total | 10087365 |
| Coût natif (champ cost, devise non exposée) | 0.270067322 |
| Compactions observées | 0 |

Résultats : compilations ciblées 3/3 ; tests ciblés 3 UNIT +1 INTEGRATION ; régression conforme 933 UNIT +200 INTEGRATION, tous OK/exit0 ; stricts post-code change valide, specs76/0, all77/0. Premier essai global sans Django : 931 tests, 18 échecs et1 erreur, exit1, conservé ; il ne vaut pas réussite. Les dépendances déjà déclarées ont été vérifiées/résolues, installées uniquement dans un venv temporaire puis contrôlées (pip check/show) et ce seul artefact a été nettoyé.

Sondes : cinq relèves prévues (initiale préparation, initiale reprise, +30, +60, finale), toutes tentées ; deux relèves réussies, trois échouées, zéro relève manquée. Neuf tentatives dont deux valides et sept invalides ; invalides exclues des moyennes, chaque relève échouée retentée une seule fois. +30 démarrée 51s après échéance ; relève suivante 3min05s après échéance : relevés tardifs réels, aucune mesure reconstruite rétroactivement. La première tentative de reprise est invalide car l’observateur incluait du texte utilisateur ; les autres invalides ne produisent pas les 40 lignes attendues.

| Position/essai | Horodatage UTC | Lignes | Validité | TTMT s | Tokens/s | Sortie tokens |
| --- | --- | --- | --- | --- | --- | --- |
| initiale NotificationChannel vocabulaire | 2026-10-05T05:20:13.479199+00:00 | 40 | valide | 5.219 | 90.879 | 643 |
| début reprise | 2026-10-05T08:43:06.702766+00:00 | 40 | invalide | 0.046 | 44.408 | 545 |
| début reprise, seconde tentative | 2026-10-05T08:44:36.077101+00:00 | 40 | valide | 2.482 | 67.534 | 532 |
| +30 min reprise | 2026-10-05T09:15:27.322310+00:00 | 37 | invalide | 3.098 | 57.648 | 866 |
| +30 min reprise, seconde tentative | 2026-10-05T09:16:36.534541+00:00 | 1 | invalide | 2.250 | 69.709 | 169 |
| periodique_20261005_0950_apres_refus | 2026-10-05T09:49:41.466063+00:00 | 1 | invalide | 2.189 | 32.306 | 99 |
| periodique_20261005_0950_un_seul_retry | 2026-10-05T09:50:29.191918+00:00 | 1 | invalide | 1.628 | 77.605 | 34 |
| fin_apres_archive_notifications_20261005 | 2026-10-05T10:05:56.645032+00:00 | 121 | invalide | 3.366 | 88.493 | 1020 |
| fin_apres_archive_notifications_unique_retry_20261005 | 2026-10-05T10:06:26.915343+00:00 | 1 | invalide | 10.881 | 66.305 | 142 |

Sondes valides : TTMT min/max 2.482/5.219 s ; débit min/max 67.534/90.879 tokens/s. Surcharge séparée, neuf tentatives : 4050 tokens de sortie, 61.842 s de flux mesuré, coût natif 0.013663264. Aucun outil appelé par les sondes. Version modèle N/A ; prompt déterministe identique dans l’état parent. Les erreurs de format sont conservées, les chiffres bruts invalides ne sont pas des mesures de performance utilisables.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 61 | 26.1 % |
| assistant | 173 | 73.9 % |
| Total | 234 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 184 | 21.3 % |
| step-start | 173 | 20.0 % |
| reasoning | 173 | 20.0 % |
| tool | 161 | 18.6 % |
| step-finish | 173 | 20.0 % |
| Total | 864 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 115 | 66.5 % |
| stop | 58 | 33.5 % |
| Total | 173 | 100 % |

| Catégorie | Total | Part | Approuvé/exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 15 | 9.3 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 37 | 23.0 % | 36 (97.3 %) | 0 (0.0 %) | 1 (2.7 %) |
| bash | 29 | 18.0 % | 26 (89.7 %) | 2 (6.9 %) | 1 (3.4 %) |
| cgpt-validation_get_approval | 3 | 1.9 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 0.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 48 | 29.8 % | 47 (97.9 %) | 1 (2.1 %) | 0 (0.0 %) |
| grep | 11 | 6.8 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 13 | 8.1 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 4 | 2.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 161 | 100 % | 156 (96.9 %) | 3 (1.9 %) | 2 (1.2 %) |

## 3. Fichiers modifiés

Tentatives d’écriture de reprise, chemins avant archivage :

| Chemin absolu complet | Total | Part | Approuvé/exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/src/pixs/kernel/notifications.py | 1 | 25.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_notification_channel.py | 1 | 25.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_notification_channel_integration.py | 1 | 25.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-channel-vocabulary/tasks.md | 1 | 25.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 4 | 100 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Préparation historique, séparée des quatre écritures ci-dessus : cinq écritures natives réussies (100 %), zéro refus (0 %), zéro erreur (0 %), prouvées par l’état parent malgré HTTP404 de la session. Chaque fichier représente1/5=20,0 % :

- /home/devops/datas/pixs/openspec/changes/add-initial-notification-channel-vocabulary/proposal.md — 1 écriture réussie (20,0 % du sous-total ; taux100 %).
- /home/devops/datas/pixs/openspec/changes/add-initial-notification-channel-vocabulary/design.md — 1 écriture réussie (20,0 % du sous-total ; taux100 %).
- /home/devops/datas/pixs/openspec/changes/add-initial-notification-channel-vocabulary/.openspec.yaml — 1 écriture réussie (20,0 % du sous-total ; taux100 %).
- /home/devops/datas/pixs/openspec/changes/add-initial-notification-channel-vocabulary/specs/notifications/spec.md — 1 écriture réussie (20,0 % du sous-total ; taux100 %).
- /home/devops/datas/pixs/openspec/changes/add-initial-notification-channel-vocabulary/tasks.md — 1 écriture réussie (20,0 % du sous-total ; taux100 %).

L’archivage natif a déplacé ces cinq artefacts vers openspec/changes/archive/2026-10-05-add-initial-notification-channel-vocabulary ; leurs cinq empreintes sont conservées. Les 76 spécifications canoniques et les 88 fichiers de référence sont inchangés. La mise à jour des tâches est limitée aux six cases prouvées. STATISTIQUES.md est une écriture administrative postérieure à la borne de collecte, sous mandat distinct, exclue de ces totaux. Le venv temporaire, artefact régénérable, a été créé puis supprimé ; il n’est pas une source ni une modification d’un environnement existant.

## 4. Commandes

| Catégorie | Total | Part | Approuvé/exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- | --- |
| diagnostic Python | 9 | 31.0 % | 8 (88.9 %) | 1 (11.1 %) | 0 (0.0 %) |
| compilation Python | 4 | 13.8 % | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) |
| tests UNIT | 3 | 10.3 % | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| tests INTEGRATION | 2 | 6.9 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| CABtest true | 1 | 3.4 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| venv temporaire | 1 | 3.4 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| pip | 4 | 13.8 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| nettoyage temporaire | 1 | 3.4 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 4 | 13.8 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 29 | 100 % | 26 (89.7 %) | 2 (6.9 %) | 1 (3.4 %) |

Occurrences natives, libellés tronqués à100 caractères ; commandes exactes et requestId conservés dans l’état parent :

| Libellé ≤100 caractères | Nombre | Part |
| --- | --- | --- |
| true | 6 | 20.7 % |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/notifications.py; printf 'EXI… | 1 | 3.4 % |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/notifications.py | 1 | 3.4 % |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_notification_channel.py | 1 | 3.4 % |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_notification_channel_i… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PIP_CONFIG_FILE=/de… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PIP_CONFIG_FILE=/de… | 1 | 3.4 % |
| /usr/bin/true | 1 | 3.4 % |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/python/current/bin/python3 -I -B -m ve… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 | 3.4 % |
| /usr/bin/rm -r -- /home/devops/datas/pixs/.venv-cismp-notifications-20261005 | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 | 3.4 % |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 | 3.4 % |
| Total | 29 | 100 % |

Toutes les commandes refusées (permissions natives, sans exécution) :

| Libellé ≤100 caractères | Occurrences | Part des refus |
| --- | --- | --- |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/notifications.py; printf 'EXI… | 1 | 50.0 % |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/datas/… | 1 | 50.0 % |

Les deux refus portent sur une compilation avec suffixe printf/commande composée, et sur des guillemets de diagnostic différents du mandat. Ils ont été interrompus avant exécution puis réconciliés. Une cible de compilation erronée et une création venv ont aussi été refusées au niveau CAB avant Bash. Deux décisions CAB REJECTED sont donc distinctes des deux refus natifs Bash. Un appel read visant un artefact hors racine a été refusé : aucune lecture de ce contenu effectuée. Les validations pré-code historiques (trois commandes OpenSpec réussies, 100 %, zéro refus/erreur) sont prouvées dans l’état parent mais séparées de cette table de reprise.

## 5. Accès web

Outils web de l’agent de codage dans les historiques de reprise : aucun appel (0) ; approbations, refus et erreurs0, pourcentages N/A (dénominateur zéro). Cela ne signifie pas absence de réseau : les deux commandes pip approuvées ont consulté PyPI et téléchargé des wheels publiques. Les fichiers réseau sont des dépendances déjà déclarées du seul environnement de test temporaire, nettoyé ensuite. Les URL exactes des téléchargements de wheels ne sont pas exposées par les sorties pip : N/A, aucun lien reconstruit.

Accès primaires observés de l’orchestrateur avant qualification (les métadonnées ne contiennent aucun secret ; historique complet de ses outils non exposé donc total complet N/A) :

| URL approuvée et effectivement consultée ≤100 caractères | Statut |
| --- | --- |
| https://pypi.org/pypi/Django/json | consultée, lecture métadonnées publiques |
| https://pypi.org/pypi/psycopg/json | consultée, lecture métadonnées publiques |
| https://pypi.org/pypi/psycopg-binary/json | consultée, lecture métadonnées publiques |
| https://pypi.org/pypi/asgiref/json | consultée, lecture métadonnées publiques |
| https://pypi.org/pypi/sqlparse/json | consultée, lecture métadonnées publiques |
| https://www.djangoproject.com/download/ | consultée, source officielle |

Aucune URL refusée n’est observée dans le périmètre recensé ; l’exhaustivité des outils de l’orchestrateur reste N/A. Ces accès ne sont pas ajoutés aux161 outils natifs de production de l’agent, afin de conserver les totaux sur un même dénominateur vérifiable.

## 6. Synthèse globale

Complément des pourcentages de sous-totaux : cinq relèves prévues (100 %), deux réussies (40,0 %), trois échouées (60,0 %), zéro manquée (0,0 %) ; neuf tentatives (100 %), deux valides (22,2 %), sept invalides (77,8 %). Tokens natifs de production de reprise, dénominateur10 087 365 (100 %) : entrée1038 (0,0 %), sortie76097 (0,8 %), cache écrit402078 (4,0 %), cache lu9608152 (95,2 %), raisonnement0 (0,0 %). Les champs de tokens sont additionnés selon la télémétrie native ; le total ne constitue pas un contexte unique. Opérations explicitement prouvées reprise+préparation :169 (100 %),164 réussies (97,0 %), trois refusées (1,8 %), deux en erreur (1,2 %), couverture historique partielle conservée. Les coûts, durées et quotas ne partagent pas ce dénominateur de compteurs.

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-05T05:19:20.055492+00:00 |
| Fin — après archivage | 2026-10-05T10:08:11.753919+00:00 |
| Durée globale (pauses et attentes incluses) | 04 h 48 min 51 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-05T05:19:20.055492+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-05T10:08:11.753919+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs absents | — |

Aucun quota fournisseur ou Spark ne remplace le quota Codex sur10080 minutes. Les quotas sont partagés par le compte : une variation, si elle était disponible, pourrait comprendre d’autres travaux simultanés. Ici aucune consommation Codex n’est reconstituée.

| Catégorie | Total | Part | Approuvé/exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- | --- |
| files | 4 | 2.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commands | 29 | 18.0 % | 26 (89.7 %) | 2 (6.9 %) | 1 (3.4 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| other | 128 | 79.5 % | 126 (98.4 %) | 1 (0.8 %) | 1 (0.8 %) |
| Total | 161 | 100 % | 156 (96.9 %) | 3 (1.9 %) | 2 (1.2 %) |

Contrôle croisé des outils de reprise : fichiers4 + commandes29 + web0 + autres128 =161 ; succès156 + refus3 + erreurs2 =161. Messages234 =61 utilisateur +173 assistant. Les pourcentages arrondis à une décimale peuvent totaliser100,1 %. La préparation attestée ajoute séparément cinq écritures et trois stricts : bilan d’opérations explicitement prouvées reprise+préparation169, dont164 réussies, trois refusées, deux en erreur ; ce nombre reste un minimum attesté et ne reconstitue pas les autres outils/messages de la session historique manquante.

État : six tâches prouvées/cochées ; 933 tests UNIT +200 INTEGRATION OK, trois compilations et six stricts pré/post réussis ; archive native réussie à10:05:20 UTC, cinq artefacts présents, ancien change actif absent, +0/~0/-0/→0 et aucune modification canonique. Avertissement archive non bloquant conservé : sections françaises de proposal.md, outil attend Why/What Changes ; aucune correction hors périmètre. Git non inspecté, aucun commit/push mandaté. Secrets PLLM limités au processus sécurisé de mise en place ; aucune valeur transmise au modèle/rapport ; project.env non chargé pour ce change. Réseau pip public décrit ci-dessus. Le RUN CISMP parent reste ouvert pour la sélection suivante, cette archive ne prouve pas l’achèvement global de Pixs.
