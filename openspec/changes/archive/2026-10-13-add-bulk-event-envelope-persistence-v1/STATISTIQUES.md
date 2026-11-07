# STATISTIQUES — add-bulk-event-envelope-persistence-v1

Archive : openspec/changes/archive/2026-10-13-add-bulk-event-envelope-persistence-v1. RUN parent : cismp-pixs-8a57078ff4d44bde.

Périmètre : historiques natifs complets des trois sessions du même change, jusqu’au relevé final après archive et correction de présentation. Préflights et compaction inclus ; sondes jetables, sélections précédentes et production du présent rapport exclues. Télémétrie interne Codex non exposée : N/A. Les bornes et comptes ne sont pas une clôture du RUN parent.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 3.634 s | 226.716 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; modèle N/A | opencode-go | high configuré ; valeur native absente | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A | N/A | N/A |

Moyennes arithmétiques des six sondes valides de la configuration build/high. Aucune sonde orchestrateur. Version modèle, temps actif de génération et dénominateur de service cumulé tous agents non exposés : N/A ; pauses, outils, attentes et durée calendaire ne sont pas du temps de génération. Chevauchements possibles. La compaction a sa propre ligne sans métrique inventée.

## 1. Statistiques générales et décisions

Durée calendaire, pauses et attentes incluses : 02 h 01 min 15 s. 394 messages ; 217 appels : 204 terminés (94.0 %), 2 refus (0.9 %), 11 erreurs (5.1 %).

Convention : terminé = état natif completed ; cela ne prouve ni approbation manuelle ni validation fonctionnelle verte. Global strict retourne 1 et une écriture de test a produit une source invalide corrigée ensuite. Refus = permission explicitement refusée, y compris une règle locale de lecture ; erreur = incident technique sans refus. Les décisions CAB sont comptées séparément des résultats d’outils.

| Décision CAB unique | Nombre | Part |
| --- | --- | --- |
| approved | 30 | 96.8 % |
| rejected | 1 | 3.2 % |
| Total | 31 | 100.0 % |

| Réponse permission native SSE | Nombre | Part |
| --- | --- | --- |
| once | 30 | 100.0 % |
| Total | 30 | 100.0 % |

31 décisions uniques : 30 approved et 1 rejected. Les 30 opérations natives exécutées (14 écritures, 16 commandes) ont chacune une permission once corrélée. Le mandat design incomplet a été rejeté avant tout appel natif : aucune écriture refusée n’est fabriquée dans les compteurs. Deux refus de lecture par règle locale restent distincts de ce refus CAB.

Résultats : 106 tests unittest réussis sans ignoré (2 cibles + 104 régressions pertinentes), quatre suites PostgreSQL réelles réussies sur serveur 160014, schémas possédés supprimés et connexions fermées. La nouvelle suite Envelope prouve 23 contrôles booléens : physique 13 champs, payload TEXT et UTC, NUL/scalaires/−0.0/grand int, copies/gels, alias/transaction active, co-commit/co-rollback, duplicata sans écrasement avec rollback capturé, erreur CHECK réellement propagée, deux workers réellement bloqués avant une seule création, migration 0007 forward/reverse seule et tables préexistantes/public préservées dans le périmètre contrôlé. Six sources distinctes compilées en trois commandes. Python 3.12 : grammaire analysée en mémoire seulement ; exécution avec le Python du venv du projet, pas de test d’exécution Python 3.12 annoncé.

Strict ciblé avant et après code : 1/1 sans issue, exit 0. Global strict : exit 1, 77/78, uniquement trois WARNING historiques exacts bulk-operations requirements[6], [10], [13] de longueur, aucune nouvelle issue. Aucune réussite globale stricte annoncée ; la longueur n’est pas un critère de qualité.

Incidents conservés : une écriture native du test a réinterprété des échappements en quatre NUL ; fichier seul contrôlé, aucun test/compile de cette version lancé, autres octets préservés. Récupération même job puis correctif chr sous nouveau mandat, source exacte compilée et test passé. Une demande design a omis commands: [] : décision rejected, zéro effet, récupération même job puis demande complète. Deux préflights /usr/bin/true distincts, chacun une seule exécution, READY final 0/0 ; un READY transitoire pending 1 a été recontrôlé sans rejeu.

Huit délais MCP côté client : sept demandes approuvées récupérées par poll_approval du même approval_id, une demande documentaire incomplète ensuite rejetée sans effet. Trois lectures de fichiers encore inexistants sont des erreurs techniques ; deux lectures de répertoires masqués sont des refus de politique. Aucun incident présenté comme réussite de source ou permission supplémentaire.

CGPT a corrigé matériellement les brouillons record/repository et tests avant écriture : double-échappement LF, argument loads invalide, copie récursive non bornée, gel absent, full_clean ouvrant potentiellement une requête, PK trop largement reconnue ; assertions vacues/NUL/−0.0 du test ; race PG bloquante, physique date incorrect, clôtures/cleanup présumés et erreur CHECK masquée. OpenCode a réalisé les écritures sous mandats. Ces révisions éditoriales ne sont pas des refus natifs.

Archivage unique --skip-specs réussi. Un avertissement non bloquant de proposition manquant les titres Why/What Changes a été observé ; deux titres corrigés dans l’archive sous mandat distinct, corps/norme/code inchangés, présence des deux titres et UTF-8/LF vérifiée. Aucune réarchive et aucun effacement de cette preuve d’avertissement.

Compactions OpenCode : 1 (0.1 % des parties), résumé fini, SSE corrélé, hashes des six sources et quatre artefacts préservés à ce checkpoint, READY final 0/0. Configuration Muse/high observée, variant absent des métadonnées de résumé : N/A. API native de compaction orchestrateur indisponible, aucune réussite conjointe annoncée.

| Outil incident | Résultat | callID | Diagnostic |
| --- | --- | --- | --- |
| read | refused | call_01a13207229570e99dba900091a118c0 | The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permis |
| read | error | call_01a13207776b749c8b9d998ba467fea0 | File not found: /home/devops/datas/pixs/src/pixs/backend/bulk_event_envelope_record.py |
| read | error | call_01a13207785e777da0845a13bb950e7e | File not found: /home/devops/datas/pixs/src/pixs/backend/bulk_event_envelope_repository.py |
| read | error | call_01a13207795376e6b22dbd7136ebe2c3 | File not found: /home/devops/datas/pixs/src/pixs/backend/migrations/0007_bulk_event_envelope.py |
| read | refused | call_01a1322d42ef7451b1db461944b19a63 | The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permis |
| cgpt-validation_request_validation | error | call_01a1322fbc1b718fa8e0aec3bda8af4b | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a13243ad2e75519401852107ed343d | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a132480d0b72e08d5641da2709d337 | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a13251cffc77b2a72c5edda87d8766 | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a13255c4437535b1da441aa46005a0 | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a13259e78c771e900f7fbae6ae2840 | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a13263a4f772499dea282975e13ea8 | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a132665c6f71678573d9b8f189a531 | MCP error -32001: Request timed out |

Cadence de sondes : cinq relèves exigibles pendant le codage (initiale, +30, +60, +90 et finale), cinq réussies (100.0 %), zéro échouée (0.0 %), zéro manquée pendant le codage (0.0 %). Une sonde supplémentaire après archive, d’abord étiquetée fin, a précédé la correction des titres ; elle est conservée et une nouvelle finale a suivi la dernière tâche. Six mesures valides au total. Aucun créneau recréé rétroactivement ; retards réels ci-dessous.
Fin des tâches de codage vérifiées : 2026-10-13T01:25:34.159739+02:00. La clôture de collecte 2026-10-13T01:31:10.490039+02:00 inclut ensuite une attente ; l’échéance +120 min à 01:30:08 était après la fin du codage et n’est pas présentée comme une sonde manquée ni reconstruite.

| Position | Envoi réel | Retard (s) | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-12T23:30:08.856027+02:00 | None | 10.8594 | 164.506 | 927 |
| +30 min | 2026-10-13T00:00:56.272959+02:00 | 47.417 | 2.4479 | 164.385 | 910 |
| +60 min | 2026-10-13T00:30:31.191894+02:00 | 22.336 | 1.6219 | 311.016 | 890 |
| +90 min | 2026-10-13T01:01:31.767357+02:00 | 82.911 | 2.4565 | 220.85 | 912 |
| après archive avant correction titres | 2026-10-13T01:18:07.940706+02:00 | None | 2.5421 | 167.0 | 906 |
| fin | 2026-10-13T01:25:35.265935+02:00 | None | 1.8776 | 332.542 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT = envoi au premier delta texte ; débit = output natif / durée premier–dernier delta texte, hors raisonnement. Sondes sans outil, fichier ou accès métier réseau, sessions jetables supprimées. Instants absolus premier/dernier delta persistés à partir de +30 ; initiale N/A pour ces instants, durées mesurées disponibles.
TTMT min/max 1.622/10.859 s ; débit min/max 164.385/332.542. Surcharge distincte : entrée 71754, sortie 5435, raisonnement 2039, coût natif 0.008670200.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 138 | 35.0 % |
| assistant | 256 | 65.0 % |
| Total | 394 | 100.0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 355 | 25.7 % |
| step-start | 256 | 18.6 % |
| reasoning | 294 | 21.3 % |
| tool | 217 | 15.7 % |
| step-finish | 256 | 18.6 % |
| compaction | 1 | 0.1 % |
| Total | 1379 | 100.0 % |

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 46 | 21.2 % | 46 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 12 | 5.5 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 17 | 7.8 % | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 72 | 33.2 % | 67 (93.1 %) | 2 (2.8 %) | 3 (4.2 %) |
| cgpt-validation_request_validation | 31 | 14.3 % | 23 (74.2 %) | 0 (0.0 %) | 8 (25.8 %) |
| write | 14 | 6.5 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 16 | 7.4 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 9 | 4.1 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 217 | 100.0 % | 204 (94.0 %) | 2 (0.9 %) | 11 (5.1 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 158 | 61.7 % |
| stop | 98 | 38.3 % |
| Total | 256 | 100.0 % |

| Composante tokens native | Nombre | Part des composantes |
| --- | --- | --- |
| input | 5130363 | 14.6 % |
| output | 106719 | 0.3 % |
| reasoning | 61616 | 0.2 % |
| cache_read | 29870508 | 84.9 % |
| cache_write | 0 | 0.0 % |
| Total | 35169206 | 100.0 % |

Coût natif 0.606444316 ; devise/unité non exposée, aucune conversion. Total des composantes présenté sans assimiler cache et tokens à une facturation identique. Pourcentages à une décimale, écarts d’arrondi possibles.

| Configuration native provider/model/variant | Messages assistant | Part |
| --- | --- | --- |
| opencode-go / muse-spark-1.3-contributor / high | 255 | 99.6 % |
| opencode-go / muse-spark-1.3-contributor / None | 1 | 0.4 % |
| Total | 256 | 100.0 % |

## 3. Fichiers modifiés

| Chemin absolu après archivage | Tentatives | Part | Terminées | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-event-envelope-persistence-v1/proposal.md | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-event-envelope-persistence-v1/design.md | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-event-envelope-persistence-v1/tasks.md | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-event-envelope-persistence-v1/specs/events/spec.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_event_envelope_record.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_event_envelope_repository.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0007_bulk_event_envelope.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_event_envelope_persistence.py | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_event_envelope_persistence_integration.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 | 100.0 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

14 tentatives natives sur 10 chemins distincts, dont six sources Python (cinq nouvelles et models.py import minimal) et quatre artefacts OpenSpec déplacés par archive. unit écrit puis corrigé, design clarifié, tasks coché après preuves, proposal titres corrigés après archive. L’écriture NUL est techniquement terminée et reste signalée comme invalide avant correction. Un mandat design rejeté avant appel natif n’ajoute aucune tentative de fichier. Rapport publié hors bornes sous mandat distinct ; état cismp-state de l’orchestrateur hors télémétrie OpenCode. Périmètre contrôlé/cadrages/canon et autres octets préservés ; Git non inspecté.

## 4. Commandes

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 4 | 25.0 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 18.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Préflight CAB inoffensif | 2 | 12.5 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 3 | 18.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PostgreSQL réel | 4 | 25.0 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 16 | 100.0 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : aucune, 0 (0.0 %). Aucune commande du mandat documentaire rejeté. Libellés ci-dessous limités à 100 caractères ; commandes exactes/requestId conservés dans historique natif et checkpoint.

| Commande, libellé tronqué si nécessaire | Exécutions | Part |
| --- | --- | --- |
| /home/devops/.local/npm/bin/openspec validate add-bulk-event-envelope-persistence-v1 --strict --json | 2 | 12.5 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_event_envelope_record… | 1 | 6.2 % |
| /usr/bin/true | 2 | 12.5 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_event_envelope_persist… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/unit -p test_bulk_eve… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_event_envelope_… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/integration -p test_b… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec archive add-bulk-event-envelope-persistence-v1 --yes --skip-sp… | 1 | 6.2 % |
| Total | 16 | 100.0 % |

Seul le global strict retourne 1, qualifié historiquement ; les autres commandes retournent 0. Deux validations ciblées et deux préflights sont des occurrences distinctes autorisées, pas des rejeux de permissions. Les appels terminés ne deviennent pas des tests verts par ce seul compteur.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur, taux N/A (dénominateur nul). Aucune URL visitée ou refusée. API locales, inférence/quotas autorisés et PostgreSQL de test séparés de ce domaine. Aucun déploiement ou effet métier externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif | 2026-10-12T23:29:55.421000+02:00 |
| Fin — après archive, correction titres et sonde finale | 2026-10-13T01:31:10.490039+02:00 |
| Durée globale, pauses et attentes incluses | 02 h 01 min 15 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de collecte | 2026-10-12T23:29:55.436013+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-13T01:31:10.490039+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux contrôles avant/après : codex/window10080/usedPercent/resetsAt indisponibles. Aucun quota Go, autre fournisseur ou ancien relevé substitué. Quotas partagés par compte, aucune attribution exclusive ni conversion en tokens/euros.

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 187 | 86.2 % | 174 (93.0 %) | 2 (1.1 %) | 11 (5.9 %) |
| fichiers | 14 | 6.5 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commandes | 16 | 7.4 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 217 | 100.0 % | 204 (94.0 %) | 2 (0.9 %) | 11 (5.1 %) |

Totaux croisés : 217 = 204 terminés + 2 refus + 11 erreurs = 187 autres + 14 fichiers + 16 commandes + 0 web ; 31 décisions = 30 approved + 1 rejected ; 30 opérations et 30 once corrélées. Historiques complets : ses_ecdfa5222ffe8NiI1InpLO1PUH (126 messages), ses_ecdd63b16ffe30J2EqpcJyTaL6 (178 messages), ses_ecda67090ffeqieUsrq47fgvjI (90 messages).

Livraison : primitive interne append-only EventEnvelopeV1 de treize clés, codec TEXT JSON privé, captures figées/copies owned, insertion uniquement dans transaction propriétaire active et doublon refusé sans écrasement avec rollback même capturé. Migration 0007 réversible, six compilations de fichiers, 106 unittest et quatre suites PostgreSQL réelles vertes. Strict ciblé vert, global strict qualifié. Archive unique et rapport distinct contrôlé avant retour SÉLECTION. Aucun Outbox/Inbox/publisher/séquence, exécution owner autoritative, schéma métier/minimisation/secrets attestés, provider production ou runtime Bulk global complet annoncé. Aucune dépendance/norme/cadrage ajoutés, frontend/navigateur sans objet. Git non inspecté, aucun commit/push. Secrets confinés aux processus de test autorisés et auth native, aucune valeur dans modèle, sources ou rapport. Le RUN parent continue.
