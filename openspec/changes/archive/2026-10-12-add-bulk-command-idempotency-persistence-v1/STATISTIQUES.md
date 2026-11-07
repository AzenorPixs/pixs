# STATISTIQUES — add-bulk-command-idempotency-persistence-v1

Archive : openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-persistence-v1. RUN parent : cismp-pixs-8a57078ff4d44bde.

Périmètre : historiques natifs complets des quatre sessions du même change, jusqu’au relevé final après archive. Préflights de récupération et compactions inclus ; sondes jetables, sélections précédentes et production du présent rapport exclues. Aucune répartition inventée de la télémétrie interne Codex.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high configuré ; métadonnée absente pour compactions | 3.192 s | 326.067 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A | N/A | N/A |

Moyennes arithmétiques des sondes valides. Version modèle, temps de génération actif et dénominateur cumulé de service tous agents non exposés : N/A. Durée calendaire, pauses, outils et attentes ne sont pas du temps de service ; chevauchements possibles.

## 1. Statistiques générales et décisions

Durée calendaire, pauses et attentes incluses : 03 h 07 min 10 s. 592 messages ; 296 appels : 288 terminés (97.3 %), 1 refus (0.3 %), 7 erreurs (2.4 %).

Convention : terminé = état natif completed, hors outil invalid qui représente une erreur de schéma. Une invocation terminée ne prouve ni approbation manuelle ni test vert : un premier test et global strict ont retourné 1. Refus = permission explicitement rejetée ; erreur = échec technique sans refus. Toutes les écritures et commandes exécutées ont une décision CGPT unitaire.

| Décision CAB unique | Nombre | Part |
| --- | --- | --- |
| approved | 31 | 100.0 % |
| Total | 31 | 100.0 % |

| Réponse permission native dans sous-ensemble SSE | Nombre | Part |
| --- | --- | --- |
| once | 18 | 100.0 % |
| Total | 18 | 100.0 % |

SSE conservé partiellement : 18 demandes et réponses once corrélées observées. Ce sous-ensemble ne constitue pas le total des permissions du change ; historique SSE exhaustif N/A. L’historique natif prouve 30 opérations exécutées sous 30 mandats, plus une tentative explicitement refusée, prouvée par erreur native et checkpoint ; les 31 décisions approuvées ne valent donc pas 31 exécutions.

Validation : six sources Python distinctes compilées (repository recompilé après correction) ; 58 tests unittest réussis sans ignoré (2 nouveaux + 56 régressions pertinentes). Premier essai unitaire échoué, conservé et corrigé, non inclus dans les 58 succès. Trois suites PostgreSQL réelles réussies, serveur 160014, nettoyage des schémas propres et connexions fermées. Nouvelle suite : 32 contrôles métier vrais ; migration 0006 forward/reverse, race réelle, co-transaction/checkpoint, CAS et rollback prouvés. Strict change avant et après code : 1/1 sans issue. Global strict : exit 1, 77/78, uniquement trois WARNING historiques exacts bulk-operations requirements[6], [10], [13] de longueur, aucune nouvelle issue ; aucune réussite globale stricte annoncée. La longueur ne sert pas de critère de qualité.

Incidents et corrections : deux write {} rejetés par le schéma avant permission/effet, puis une seule écriture valide. Trois récupérations CAB du même job, chacune préflight inédit /usr/bin/true et READY ; aucun effet source rejoué. Défaut local de trois gardes exact-str devant _is_runtime_text révélé par test hostile, corrigé avant I/O, recompilé et test repassé. Commande de régression dont les guillemets ont dérivé : permission native rejetée, aucune exécution ; nouveau mandat exact et 56 tests verts après récupération. Catalogue read absent : sources autorisées transmises comme texte, sans fausse preuve de lecture native. Une variation de mise en forme du seul test PG est acceptée après équivalence AST ; ses octets ne sont pas ceux du brouillon initial. CGPT a reconstruit/revu le repository et corrigé matériellement les tests PG ; OpenCode a réalisé les écritures sous CAB. Ces révisions éditoriales ne sont pas des refus natifs.

| Outil en incident | Résultat | callID | Diagnostic |
| --- | --- | --- | --- |
| write | error | call_01a1316beb5572f9acf27038ccdd49a6 | The write tool was called with invalid arguments: SchemaError(Missing key   at ["content"]). Please rewrite the input so it satisfies the expected schema. |
| write | error | call_01a1316c01d47330bab1e13f80da5f6d | The write tool was called with invalid arguments: SchemaError(Missing key   at ["content"]). Please rewrite the input so it satisfies the expected schema. |
| read | error | call_01a131851e2070f28c92bec3debdc8f0 | The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"read","patter |
| read | error | call_01a131adbcc67782bf16ba9f35adefe6 | The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"read","patter |
| read | error | call_01a131ade327733ba07072deb058281e | File not found: /home/devops/datas/pixs/tests/unit/test_bulk_command_idempotency_persistence.py |
| read | error | call_01a131ade3ff73888062d076468dcd18 | File not found: /home/devops/datas/pixs/tests/integration/test_bulk_command_idempotency_persistence_integration.py |
| read | error | call_01a131c2913974a48fd6167142706e3d | The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"read","patter |
| bash | refused | call_01a131e6cff4707791d8688624490068 | The user rejected permission to use this specific tool call with the following feedback: CGPT refuse commande non strictement identique au mandat. Aucun test autorisé sous cette variation. Attendre ré |

Compactions natives OpenCode : 2 (0.1 % des parties). Config compaction Muse/high observée ; variant effectif absent des métadonnées, N/A. API native de compaction orchestrateur indisponible : aucune réussite conjointe annoncée. Checkpoints, sources préservées et événements SSE corrélés conservés dans le RUN.

Sondes : 8 relevés réels, 8 réussis (100.0 %), 0 échoués (0.0 %). Initiale, six périodiques +30 à +180 et finale ; aucun créneau reconstruit rétroactivement. Les retards réels sont affichés. Instants absolus premier/dernier delta non persistés individuellement : N/A ; durées mesurées en direct via horloge monotone et SSE.

| Position | Envoi réel | Retard (s) | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-12T20:15:00.786096+02:00 | None | 3.0685 | 503.659 | 890 |
| +30 min | 2026-10-12T20:46:49.725580+02:00 | 108.94 | 2.3383 | 310.161 | 890 |
| +60 min | 2026-10-12T21:27:38.805708+02:00 | 758.02 | 3.8954 | 279.381 | 890 |
| +90 min | 2026-10-12T21:47:43.208832+02:00 | 162.423 | 6.2745 | 262.622 | 890 |
| +120 min | 2026-10-12T22:16:31.568022+02:00 | 90.782 | 2.0747 | 266.645 | 916 |
| +150 min | 2026-10-12T22:45:17.986674+02:00 | 17.201 | 2.073 | 332.581 | 890 |
| +180 min | 2026-10-12T23:15:13.814839+02:00 | 13.029 | 2.5381 | 377.587 | 890 |
| fin | 2026-10-12T23:17:39.203495+02:00 | None | 3.2754 | 275.903 | 902 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT = envoi au premier delta texte ; débit = output natif / durée premier–dernier delta texte, hors raisonnement.
TTMT min/max 2.073/6.274 s ; débit min/max 262.622/503.659. Surcharge sondes séparée : entrée 95559, sortie 7158, raisonnement 2190, coût natif 0.011425726.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 207 | 35.0 % |
| assistant | 385 | 65.0 % |
| Total | 592 | 100.0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 515 | 25.8 % |
| step-start | 384 | 19.2 % |
| reasoning | 415 | 20.8 % |
| tool | 296 | 14.8 % |
| step-finish | 384 | 19.2 % |
| compaction | 2 | 0.1 % |
| Total | 1996 | 100.0 % |

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 71 | 24.0 % | 71 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 114 | 38.5 % | 109 (95.6 %) | 0 (0.0 %) | 5 (4.4 %) |
| glob | 9 | 3.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 2 | 0.7 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 31 | 10.5 % | 31 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 13 | 4.4 % | 11 (84.6 %) | 0 (0.0 %) | 2 (15.4 %) |
| bash | 19 | 6.4 % | 18 (94.7 %) | 1 (5.3 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 13 | 4.4 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 14 | 4.7 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 8 | 2.7 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_auto_remediation_policy | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 296 | 100.0 % | 288 (97.3 %) | 1 (0.3 %) | 7 (2.4 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 222 | 57.7 % |
| stop | 162 | 42.1 % |
| None | 1 | 0.3 % |
| Total | 385 | 100.0 % |

| Composante tokens native | Nombre | Part des composantes |
| --- | --- | --- |
| input | 2894192 | 7.1 % |
| output | 130036 | 0.3 % |
| reasoning | 66143 | 0.2 % |
| cache_read | 37740181 | 92.4 % |
| cache_write | 0 | 0.0 % |
| Total | 40830552 | 100.0 % |

Coût natif cumulé 0.404135362 ; devise/unité non exposée, aucune conversion. Cache séparé des tokens input/output/raisonnement ; total des composantes présenté sans affirmer une facturation équivalente. Arrondis à une décimale, écarts possibles.

| Configuration native provider/model/variant | Messages assistant | Part |
| --- | --- | --- |
| opencode-go / muse-spark-1.3-contributor / high | 383 | 99.5 % |
| opencode-go / muse-spark-1.3-contributor / None | 2 | 0.5 % |
| Total | 385 | 100.0 % |

## 3. Fichiers modifiés

| Chemin absolu après archivage | Tentatives | Part | Terminées | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| N/A — arguments absents avant effet | 2 | 14.3 % | 0 (0.0 %) | 0 (0.0 %) | 2 (100.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-persistence-v1/proposal.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-persistence-v1/design.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-persistence-v1/tasks.md | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-persistence-v1/specs/interactions/spec.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_command_idempotency_record.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_command_idempotency_repository.py | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0006_bulk_command_idempotency.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_command_idempotency_persistence.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_command_idempotency_persistence_integration.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 | 100.0 % | 12 (85.7 %) | 0 (0.0 %) | 2 (14.3 %) |

Compteurs = tentatives natives write/edit/patch, pas lignes. Les deux appels sans arguments n’ont aucune cible ni effet ; les six sources réelles sont listées. Quatre artefacts déplacés par archive, tasks coché après preuves. Rapport publié après bornes sous mandat distinct et exclu de son auto-comptage. Cadres, canon et anciennes sources préservés sauf import minimal dans models.py.

## 4. Commandes

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Préflight CAB inoffensif | 3 | 15.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 4 | 21.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 4 | 21.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 5 | 26.3 % | 4 (80.0 %) | 1 (20.0 %) | 0 (0.0 %) |
| PostgreSQL réel | 3 | 15.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 19 | 100.0 % | 18 (94.7 %) | 1 (5.3 %) | 0 (0.0 %) |

Commandes refusées, regroupées ; libellés limités à 100 caractères, commande exacte conservée dans historique natif et checkpoint :

| Commande refusée, non exécutée | Occurrences | Part des refus |
| --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 100.0 % |
| Total | 1 | 100.0 % |

Autres commandes exactes et leurs occurrences (libellés tronqués à 100 caractères ; famille détaillée ci-dessus) :

| Commande | Tentatives | Part |
| --- | --- | --- |
| /usr/bin/true | 3 | 15.8 % |
| /home/devops/.local/npm/bin/openspec validate add-bulk-command-idempotency-persistence-v1 --strict … | 2 | 10.5 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_command_idempotency_r… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_command_idempotency_pe… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/unit -p test_bulk_com… | 2 | 10.5 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_command_idempotency_r… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_command_idempot… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/integration -p test_b… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.3 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 5.3 % |
| /home/devops/.local/npm/bin/openspec archive add-bulk-command-idempotency-persistence-v1 --yes --sk… | 1 | 5.3 % |
| Total | 19 | 100.0 % |

Le premier unittest exit 1 est un échec fonctionnel corrigé et retesté. Global strict exit 1 est qualifié historiquement ; ces commandes restent terminées techniquement. Aucun résultat absent assimilé à un succès.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; taux N/A, dénominateur nul. Aucune URL visitée/refusée. Inférence/quotas et API locales d’instrumentation autorisées hors de ce domaine ; aucun déploiement ni service métier externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif | 2026-10-12T20:12:06.540000+02:00 |
| Fin — après archivage et sonde finale | 2026-10-12T23:19:17.476528+02:00 |
| Durée globale, pauses et attentes incluses | 03 h 07 min 10 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de collecte | 2026-10-12T20:15:00.511989+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T23:19:17.476528+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux contrôles avant/après : identité codex/window10080, usedPercent et resetsAt indisponibles. Aucune valeur ancienne ni autre fournisseur substitué. Quotas partagés par compte ; aucune attribution exclusive à ce change et aucune conversion en tokens/euros.

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| others | 263 | 88.9 % | 258 (98.1 %) | 0 (0.0 %) | 5 (1.9 %) |
| files | 14 | 4.7 % | 12 (85.7 %) | 0 (0.0 %) | 2 (14.3 %) |
| commands | 19 | 6.4 % | 18 (94.7 %) | 1 (5.3 %) | 0 (0.0 %) |
| Total | 296 | 100.0 % | 288 (97.3 %) | 1 (0.3 %) | 7 (2.4 %) |

Totaux croisés vérifiés : 296 appels = somme des outils = somme des domaines ; 288 terminés + 1 refus + 7 erreurs. Historiques complets : ses_eceaf6cf3ffeowpZo5ruPoyobA (99 messages), ses_ece8dc16fffeh7KTcspw22Ry8y (232 messages), ses_ece3ff95bffekrWOBpXsQedalP (182 messages), ses_ece151846fferhOTHHBaPC8iUO (79 messages).

Livraison : persistance interne des 12 clés logiques CommandIdempotencyV1, PK technique distincte, unicité quatre colonnes, unité transactionnelle privée et finalize CAS, rejeu stable/divergent, rollback sans IN_PROGRESS engagé via API. Migration 0006 réversible, trois suites PG réelles, 58 unittest et compilations ci-dessus. Archive unique --skip-specs, rapport distinct vérifié avant retour SÉLECTION. Aucune preuve d’exécution autoritative owner ni de runtime Bulk global complet. Pas de frontend concerné, navigateur sans objet. Git non inspecté, aucun commit/push. Aucune nouvelle dépendance ni norme. Secrets confinés aux seuls processus autorisés et auth native, aucune valeur dans sources/prompt/rapport. RUN parent continue après contrôle du rapport.
