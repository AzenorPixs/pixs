# STATISTIQUES — add-bulk-inbox-receipt-persistence-v1

Archive : openspec/changes/archive/2026-10-13-add-bulk-inbox-receipt-persistence-v1. RUN parent : cismp-pixs-8a57078ff4d44bde.

Périmètre : historiques natifs complets des deux sessions du même change, jusqu’au relevé final après archive et sonde finale. Préflight et compaction inclus ; sélection préalable, sondes jetables et production du présent rapport exclues. Télémétrie interne de l’orchestrateur non exposée : N/A. Aucune clôture du RUN parent déduite.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high | 2.385 s | 290.259 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high configuré ; valeur native absente | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A | N/A | N/A |

Moyennes arithmétiques des quatre sondes valides build/high. Aucune sonde orchestrateur. Version modèle, durées actives de génération et dénominateur cumulé de service tous agents : N/A, non exposés. Durée calendaire, pauses, outils et attentes ne sont pas du temps de génération ; chevauchements possibles.

## 1. Statistiques générales et décisions

Durée calendaire, pauses et attentes incluses : 01 h 16 min 38 s. 266 messages, 146 appels : 139 terminés (95.2 %), 1 refus (0.7 %), 6 erreurs (4.1 %).

Convention : terminé = état natif completed ; ce compteur ne prouve ni approbation manuelle ni validation fonctionnelle verte. Refus = règle/permission explicitement refusée ; erreur = incident technique sans refus. Global strict retourne 1 tout en étant une invocation terminée. Décisions CAB et effets natifs sont comptés séparément.

| Décision CAB unique | Nombre | Part |
| --- | --- | --- |
| approved | 28 | 100.0 % |
| Total | 28 | 100.0 % |

| Réponse permission native SSE | Nombre | Part |
| --- | --- | --- |
| once | 27 | 100.0 % |
| Total | 27 | 100.0 % |

28 décisions approved, 0 rejected (0.0 %). Une approbation de proposition est restée inutilisée faute d’outil natif rapporté, puis invalidée par la récupération ; elle n’est pas une écriture. Les 27 opérations exécutées (11 écritures, 16 commandes) ont 27 permissions once corrélées. Aucun refus de permission mutatrice ; le refus de lecture par règle locale est distinct.

Validation : 125 tests unittest réussis sans ignoré (2 cibles + 123 régressions), cinq suites PostgreSQL réelles réussies sur serveur 160014, six fichiers Python compilés en trois commandes. Nouvelle suite Inbox : 26 contrôles booléens vrais, huit clés logiques et PK technique distincte, clé composée consumer/event, version ET SHA comparées, Duplicate/Divergence exacts sans écrasement, originaux préservés, rollback propriétaire et JobRecord même si refus capturé, co-commit/co-rollback, observation indépendante avant/après commit et propre ligne inflight non assimilée à un ack, race deux workers bloqués/un gagnant et perdant annulé, autre contrainte unique réellement propagée, migration0008 forward/reverse seule, nettoyage/connexions/public et dix tables préexistantes préservés dans le périmètre contrôlé. Python 3.12 : analyse grammaticale en mémoire seulement ; tests exécutés avec le venv du projet, pas de test d’exécution Python 3.12 annoncé.

Strict ciblé précode et final : 1/1 sans issue exit0. Global strict : exit1, 77/78, seules trois WARNING historiques exactes bulk-operations requirements[6], [10], [13] de longueur, aucune nouvelle issue ; aucune réussite globale stricte annoncée. La longueur n’est pas un critère de qualité. Archive unique --skip-specs exit0 sans nouvel avertissement de proposition.

Incident : après compaction, l’agent rapportait seuls outils MCP malgré registre natif disponible ; aucune première écriture effectuée. Réexposition sans génération puis ASK rétabli sans résultat, approbation inutilisée conservée/infirmée comme effet nul. Récupération même job dans nouvelle session, ancien mandat invalidé, préflight /usr/bin/true exact une seule exécution sous once et READY final0/0, puis mandat de proposition neuf et écriture prouvée. OpenCode n’a pas été fermé/redémarré. Les deux délais MCP côté client ont été récupérés par poll_approval du même approval_id sans seconde décision ni exécution. Quatre lectures de cibles encore inexistantes sont des erreurs techniques ; une lecture masquée est un refus de règle.

Corrections éditoriales CGPT avant écritures : brouillon design aux noms de champs inventés remplacé par les huit canons, savepoint autour INSERT et tâches non circulaires ; guillemets de docstrings Python invalides corrigés ; retours repository convertis en capture pure figée ; test deferred réel et Unicode positif ; harness PG corrigé (préfixe de schéma helper, DDL hors rollback, observer réel, divergences avec owner/Job annulés, propre duplicata capturé sans panne artificielle, gagnant owner/Job exact, huit violations SQL, index temporaire à constante statique et nom 23505 exact). OpenCode réalise les écritures sous mandats ; ces révisions ne sont pas des refus natifs.

| Outil incident | Résultat | callID | Diagnostic |
| --- | --- | --- | --- |
| read | refused | call_01a132ad6599740c97dd9a3d90f57992 | The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permis |
| cgpt-validation_request_validation | error | call_01a132afd3a27677a4c2f6be0e22edc0 | MCP error -32001: Request timed out |
| cgpt-validation_request_validation | error | call_01a132b1d54975f3972c718244408265 | MCP error -32001: Request timed out |
| read | error | call_01a132b86f3c720a86034f2c307ba190 | File not found: /home/devops/datas/pixs/src/pixs/backend/bulk_inbox_receipt_record.py |
| read | error | call_01a132b8715d744dab341a7a9161d040 | File not found: /home/devops/datas/pixs/src/pixs/backend/bulk_inbox_receipt_repository.py |
| read | error | call_01a132b872fb75e0a464e4972106bbb6 | File not found: /home/devops/datas/pixs/src/pixs/backend/migrations/0008_bulk_inbox_receipt.py |
| read | error | call_01a132c28ed872ca860efa55aaf7942a | File not found: /home/devops/datas/pixs/tests/unit/test_bulk_inbox_receipt_persistence.py |

Compaction native OpenCode : 1 (0.1 % des parties), résumé fini/SSE corrélé/hashes des sources existantes préservés, avant toute création Inbox. Configuration Muse/high observée, variant natif du résumé absent : N/A. API native de compaction orchestrateur indisponible, aucune réussite conjointe annoncée.

Sondes : initiale, +30 min, +60 min, finale, soit 4 exigibles ; 4 réussies (100.0 %), 0 échouée (0.0 %), 0 manquée (0.0 %). Prochaine +90 après la fin du codage/collecte. Retards réels affichés, aucun créneau recréé rétroactivement.

| Position | Envoi réel | Retard (s) | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T02:13:37.174613+02:00 | None | 2.4147 | 155.873 | 928 |
| +30 min | 2026-10-13T02:44:10.139020+02:00 | 32.964 | 2.6123 | 461.235 | 905 |
| +60 min | 2026-10-13T03:14:02.606469+02:00 | 25.432 | 2.4489 | 245.483 | 905 |
| fin | 2026-10-13T03:28:00.009932+02:00 | None | 2.0661 | 298.444 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT = envoi au premier delta texte ; débit = output natif / durée premier–dernier delta texte, hors raisonnement. Horodatages envoi/premier/dernier delta conservés, sessions jetables supprimées, aucun outil/fichier/accès métier réseau.
TTMT min/max 2.066/2.612 s ; débit min/max 155.873/461.235. Surcharge séparée : entrée 47723, sortie 3628, raisonnement 1783, coût natif 0.005854726.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 103 | 38.7 % |
| assistant | 163 | 61.3 % |
| Total | 266 | 100.0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 229 | 26.0 % |
| step-start | 163 | 18.5 % |
| reasoning | 180 | 20.4 % |
| tool | 146 | 16.6 % |
| step-finish | 163 | 18.5 % |
| compaction | 1 | 0.1 % |
| Total | 882 | 100.0 % |

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 28 | 19.2 % | 28 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 3 | 2.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 18 | 12.3 % | 18 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_auto_remediation_policy | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 28 | 19.2 % | 26 (92.9 %) | 0 (0.0 %) | 2 (7.1 %) |
| cgpt-validation_get_approval | 3 | 2.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 16 | 11.0 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 35 | 24.0 % | 30 (85.7 %) | 1 (2.9 %) | 4 (11.4 %) |
| cgpt-validation_poll_approval | 2 | 1.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 11 | 7.5 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 146 | 100.0 % | 139 (95.2 %) | 1 (0.7 %) | 6 (4.1 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 99 | 60.7 % |
| stop | 64 | 39.3 % |
| Total | 163 | 100.0 % |

| Composante tokens native | Nombre | Part des composantes |
| --- | --- | --- |
| input | 3625241 | 13.3 % |
| output | 77793 | 0.3 % |
| reasoning | 27183 | 0.1 % |
| cache_read | 23588097 | 86.3 % |
| cache_write | 0 | 0.0 % |
| Total | 27318314 | 100.0 % |

Coût natif cumulé 0.430695494 ; devise/unité non exposée, aucune conversion. Cache séparé des tokens, somme des composantes sans équivalence de facturation inventée. Pourcentages à une décimale, écarts d’arrondi possibles.

| Configuration native provider/model/variant | Messages assistant | Part |
| --- | --- | --- |
| opencode-go / muse-spark-1.3-contributor / high | 162 | 99.4 % |
| opencode-go / muse-spark-1.3-contributor / None | 1 | 0.6 % |
| Total | 163 | 100.0 % |

## 3. Fichiers modifiés

| Chemin absolu après archivage | Tentatives | Part | Terminées | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-inbox-receipt-persistence-v1/proposal.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-inbox-receipt-persistence-v1/design.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-inbox-receipt-persistence-v1/tasks.md | 2 | 18.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-inbox-receipt-persistence-v1/specs/events/spec.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_inbox_receipt_record.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_inbox_receipt_repository.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0008_bulk_inbox_receipt.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_inbox_receipt_persistence.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_inbox_receipt_persistence_integration.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 | 100.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

11 tentatives natives sur 10 chemins : six sources Python (cinq nouvelles et models.py import minimal) et quatre artefacts OpenSpec déplacés par archive, tasks écrit puis coché après preuves. Approbation de proposition inutilisée : zéro tentative native ajoutée. Présent rapport hors bornes et sous mandat distinct, sans auto-comptage. État cismp-state de l’orchestrateur hors télémétrie OpenCode. Autres octets/cadrages/canon/purs/runtime/CommandIdempotency/Envelope du périmètre contrôlé préservés ; Git non inspecté.

## 4. Commandes

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Préflight CAB | 1 | 6.2 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 4 | 25.0 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 18.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 3 | 18.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PostgreSQL réel | 5 | 31.2 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 16 | 100.0 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : aucune, 0 (0.0 %). Libellés limités à 100 caractères, commandes exactes/requestId dans historique natif/checkpoint.

| Commande, libellé tronqué si nécessaire | Exécutions | Part |
| --- | --- | --- |
| /usr/bin/true | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec validate add-bulk-inbox-receipt-persistence-v1 --strict --json | 2 | 12.5 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_inbox_receipt_record.… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_inbox_receipt_persiste… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/unit -p test_bulk_inb… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_inbox_receipt_p… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/integration -p test_b… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec archive add-bulk-inbox-receipt-persistence-v1 --yes --skip-spe… | 1 | 6.2 % |
| Total | 16 | 100.0 % |

Seul global strict exit1, qualifié historiquement ; autres commandes exit0. Strict ciblé contrôlé avant et après code, deux occurrences distinctes autorisées. Aucun rejeu de permission consommée, aucun test interrompu ou ignoré compté vert.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur, taux N/A (dénominateur nul). Aucune URL visitée/refusée. Inférence/quotas autorisés, API locales et PostgreSQL de test hors de ce domaine ; aucun déploiement ni effet métier externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif | 2026-10-13T02:12:32.351000+02:00 |
| Fin — après archivage et sonde finale | 2026-10-13T03:29:10.610217+02:00 |
| Durée globale, pauses et attentes incluses | 01 h 16 min 38 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de collecte | 2026-10-13T02:12:32.358501+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-13T03:29:10.610217+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux contrôles live ; codex/window10080/usedPercent/resetsAt indisponibles. Aucun quota Go ou autre source substitué. Quotas partagés par compte, aucune attribution exclusive ni conversion en tokens/euros.

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 119 | 81.5 % | 112 (94.1 %) | 1 (0.8 %) | 6 (5.0 %) |
| commandes | 16 | 11.0 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 11 | 7.5 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 146 | 100.0 % | 139 (95.2 %) | 1 (0.7 %) | 6 (4.1 %) |

Totaux croisés : 146 = 139 terminés + 1 refus + 6 erreurs = 119 autres + 11 fichiers + 16 commandes ; 28 décisions approved dont une inutilisée, 27 opérations exécutées et 27 once corrélées. Historiques complets : ses_ecd657120ffeiVQBJPzYirLl9X (54 messages), ses_ecd563a88ffe1mUtt7sGbCiS0b (212 messages).

Livraison : primitive append-only InboxReceiptV1 huit clés, PK technique hors huit, unicité consumer/event, version/empreinte comparées, refus Duplicate/Divergence et rollback owner/Job même capturé. get/insert retournent données figées, CONSUMED n’est pas un ack avant commit. Migration0008 réversible, 125 unittest et cinq suites PG réelles, six sources compilées. Archive unique --skip-specs, rapport distinct vérifié avant retour SÉLECTION. Pas de receiver/provider/authority/catalogue/callback/hachage/serializer nouveau, aucun Outbox/publisher/séquence/bail/effet externe ou B11 global complet revendiqué. Aucune norme/dépendance/cadrage ajoutés. Frontend/navigateur sans objet. Git non inspecté, aucun commit/push. Secrets confinés aux processus autorisés et auth native, aucune valeur dans modèle/sources/rapport. RUN parent continue.
