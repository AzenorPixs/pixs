# STATISTIQUES — add-bulk-export-manifest-persistence-v1

Archive : openspec/changes/archive/2026-10-13-add-bulk-export-manifest-persistence-v1. RUN parent : cismp-pixs-8a57078ff4d44bde.

Périmètre : historique natif de la session du change depuis sa création, borné aux messages créés avant le relevé final après archivage et sonde finale. Sélection préalable, sessions jetables des sondes/prévols et production du présent rapport exclues. Pause et attentes incluses dans la durée calendaire. Télémétrie interne de l’orchestrateur : N/A. Le RUN parent continue.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high | 2.213 s | 280.946 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high configuré ; variant natif absent | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A | N/A | N/A |

Moyennes arithmétiques des quatre sondes build/high valides. Version modèle non déduite de son identifiant. Aucune sonde orchestrateur. Durées actives de génération et temps de service cumulé tous agents non exposés : N/A ; durée calendaire, outils, pauses et attentes ne sont pas assimilés à du temps de génération. Chevauchements possibles avec les sondes.

## 1. Statistiques générales et décisions

Durée calendaire avec pauses et attentes : 02 h 59 min 13 s. 587 messages, 444 appels : 436 terminés (98.2 %), 1 refus (0.2 %), 7 erreurs (1.6 %).

Convention : terminé = état natif completed, sans implication de validation fonctionnelle verte. Refus = règle/permission explicitement refusée ; erreur = échec technique. Global strict exit1 reste un échec strict, même si son invocation est terminée. Décisions CAB, appels et permissions sont comptés séparément.

| Décision CAB unique | Nombre | Part |
| --- | --- | --- |
| rejected | 1 | 3.2 % |
| approved | 30 | 96.8 % |
| Total | 31 | 100.0 % |

31 décisions uniques : 30 approved et 1 rejected. Les 25 décisions post-reprise sont lisibles par HTTP dans le contrôleur courant ; six décisions antérieures au redémarrage renvoient désormais 404 HTTP. Elles ont été réconciliées à partir des réponses MCP terminales corrélées conservées et du checkpoint : cinq approved avec effets natifs vérifiés, une rejected sans effet. Aucun 404 n’est interprété comme une nouvelle autorisation. Aucune décision ni permission consommée n’a été rejouée.

| Réponse native SSE observée après reprise | Nombre | Part |
| --- | --- | --- |
| once | 25 | 96.2 % |
| reject | 1 | 3.8 % |
| Total | 26 | 100.0 % |

30 opérations mutatrices/commandes terminées : 11 écritures et 19 commandes, sous 30 mandats approuvés. Après reprise : 25 once et un rejet de lecture observés/corrélés en SSE. Les cinq permissions antérieures à la pause n’ont pas été conservées dans le checkpoint : total SSE intégral N/A, sans reconstitution ; leurs demandes MCP, décisions et effets natifs restent prouvés. Le rejet de lecture n’est pas une décision CAB rejetée ni un refus de commande.

Validation exécutée : 167 tests unittest sans saut (1 unité persistance, 1 inertie harness PG, 165 régressions). Sept suites PostgreSQL réelles réussies sur serveur 160014 : ExportManifest, ValidationReport, InboxReceipt, EventEnvelope, CommandIdempotency, runtime et AdmissionIdentity. Six sources Python compilées en trois invocations. Contrôle Django du modèle sous gardes offline. Analyse grammaticale outer/child Python 3.12 en mémoire ; exécution réelle avec le venv du projet, aucune exécution Python 3.12 revendiquée.

ExportManifest : 17 valeurs explicites, PK technique distincte, 18 colonnes physiques et 15 CHECKs. Deux compteurs en TEXT décimal privé sans plafond int64, encodage/décodage stdlib à capacité réelle, UTC exact en entrée et conversion DB de confiance réutilisée. Roundtrip, None/False/CSV/NDJSON/SNAPSHOT/WATERMARK, UTC min/max, captures figées/exports owned et grands entiers vérifiés. Plusieurs snapshots pour la même opération ont des ids distincts. Co-commit/co-rollback avec effet propriétaire, observateur indépendant avant/après commit, hydraté modifié refusé, deferred réel sans requête lazy, ids invalides avant ORM, absence de transaction propriétaire sur default/other refusée. Quinze violations SQL 23514 exactes, compteurs malformés refusés, mapping stocké invalide et capacité de rechargement refusés. CHECK temporaire réellement propagé ; transaction propriétaire invalidée et annulée même si l’erreur est capturée, SELECT1 y refusé. Migration0010 forward/reverse seule ; douze tables précédentes, métadonnées publiques, nettoyage du schéma owned et fermeture des connexions préservés.

Strict ciblé précode et final : 1/1 zéro issue exit0. Global strict : 77/78, exit1, seules trois WARNING historiques exactes bulk-operations requirements[6], [10], [13], aucune nouvelle issue. Aucune réussite globale stricte annoncée ; longueur non utilisée comme critère de qualité. Archivage unique --skip-specs exit0, canon conservé.

Incidents : premier input request_validation avec ttl_seconds=0 refusé par schéma -32602 sans création ; seconde soumission sans TTL enregistrée, délais client request/poll, puis rejet CGPT avant effet et nouveau mandat inédit. Aucun fichier écrit sous la demande rejetée. Après pause explicitement demandée, CAB arrêté et OpenCode conservé ; reprise du même job/session après PLLM fraîche, prévol natif Muse/high et test /usr/bin/true exact. Quatre lectures sans filePath ont échoué au schéma et une lecture a été avortée avec rejet explicite de permission dans les métadonnées parentes ; réconciliation sans effet, outils de lecture masqués, nouveau test CAB exact puis transmission directe des sources. Une réponse NFDOC unittest finish=length était tronquée : aucune écriture/exécution de ce texte, fragments complets ensuite revus. Les deux tests CAB ont exit0 et once corrélée ; un premier contrôle final transitoirement pending1 n’a pas été accepté, nouveau readiness0/0 sans rejeu.

Révisions CGPT des brouillons avant écriture : artefacts vers 17 noms, 15 TEXT + UTC + bool hors PK, codec décimal sans JSON, CHECKs dérivés et delta MODIFIED B12 verbatim ; modèle typegate17/UTC avant décodage, export ordonné, retrait reraise/constante inutiles et retour capture pure annoté. Unité : parenthèse enfant, imports de migrations, contrôle ciblé du miroir, UTC min/foreign callbacks, spies/typegates, aliases/forces et deux compteurs. PG : h._query inexistant retiré, état initial owned après0009 au lieu de public, helper de schéma conservé, observateur rapport+owner réel, hydraté/deferred/queryguards, diagnostics Django via __cause__, capacité réelle, rollback avec erreur capturée sans reraise. OpenCode réalise les écritures ; ces contributions matérielles de l’orchestrateur ne sont pas des refus natifs.

Actualisation externe de DEVOPS.md : seul horodatage DIU ligne6 passé de 2026-10-12T16:30:42Z à 2026-10-13T04:56:18Z ; chemins/versions inchangés, aucun écrit par l’agent. Empreintes ancienne/nouvelle et comparaison enregistrées ; baseline réconciliée après revue. Les autres cadrages, canon et sources existantes du périmètre sont conservés.

| Outil incident | Résultat | callID | Diagnostic |
| --- | --- | --- | --- |
| cgpt-validation_request_validation | error | call_01a133432dc277188a126a2805e5e534 | MCP error -32602: parametre 'ttl_seconds' : entier entre 60 et 604800 |
| cgpt-validation_request_validation | error | call_01a133433b69710180bfd09dd1a5443a | MCP error -32001: Request timed out |
| cgpt-validation_poll_approval | error | call_01a133442c1c720898f75b4e1ba05888 | MCP error -32001: Request timed out |
| read | error | call_01a133ace92371b2b59a8a8df09ebd31 | The read tool was called with invalid arguments: SchemaError(Missing key   at ["filePath"]). Please rewrite the input so it satisfies the expected schema. |
| read | error | call_01a133ace9bc72c1b233180f4e476586 | The read tool was called with invalid arguments: SchemaError(Missing key   at ["filePath"]). Please rewrite the input so it satisfies the expected schema. |
| read | error | call_01a133acea54732b8a01af145b049640 | The read tool was called with invalid arguments: SchemaError(Missing key   at ["filePath"]). Please rewrite the input so it satisfies the expected schema. |
| read | error | call_01a133aceb0070cbb75ab69a8a85b682 | The read tool was called with invalid arguments: SchemaError(Missing key   at ["filePath"]). Please rewrite the input so it satisfies the expected schema. |
| read | refused | call_01a133acebab7474a49ec238f4ac70db | Tool execution aborted |

Trois résumés natifs de compaction observés, tous variant absent : N/A effectif malgré high configuré. Deux cycles explicitement tracés avec HTTP/SSE/hashes réconciliés ; un résumé supplémentaire auto=false observé vers06:53, initiateur non attribuable aux preuves de l’orchestrateur. API native orchestrateur non exposée ; aucune réussite conjointe revendiquée. Aucune fermeture/redémarrage OpenCode.

| Résumé natif | Création UTC ms | Variant effectif |
| --- | --- | --- |
| msg_1334bbf24001JIySotz9FarWLP | 1791861964580 | N/A |
| msg_1339bae650011iqTZ5p179E5iF | 1791867203173 | N/A |
| msg_133a4e8da001Wmcdx1wJvUL3wP | 1791867807962 | N/A |

| Cycle explicite | Échéance | Début réel | Retard (s) | Résultat |
| --- | --- | --- | --- | --- |
| cismp-compact-e5d0db051eb6 | 2026-10-13T05:23:08.028497+02:00 | 2026-10-13T05:26:04.255954+02:00 | 176.227 | OC_COMPLETED_ROOT_API_UNAVAILABLE |
| cismp-compact-f1104eb5a585 | 2026-10-13T06:56:04.255954+02:00 | 2026-10-13T07:03:27.628406+02:00 | 443.372 | OC_COMPLETED_ROOT_API_UNAVAILABLE |

Sondes exigibles retenues : 7, dont 4 réussies (57.1 %), 0 échouée (0.0 %), 3 manquées avant pause (42.9 %). Aucun créneau reconstruit. Initiale, reprise, +30 de reprise et finale mesurées ; prochaine +60 de reprise à08:06 postérieure à la fin du codage/archivage08:03 et à la sonde finale08:05, non exigible après fin du codage.

| Position | Envoi réel | Retard (s) | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T05:10:13.014200+02:00 | None | 2.5309 | 383.205 | 905 |
| reprise | 2026-10-13T07:06:25.232493+02:00 | None | 1.6992 | 243.891 | 927 |
| +30 min (reprise) | 2026-10-13T07:38:31.782443+02:00 | 126.55 | 2.3141 | 219.342 | 905 |
| finale | 2026-10-13T08:05:29.718783+02:00 | None | 2.306 | 277.346 | 910 |

| Relève manquée avant pause | État | Motif |
| --- | --- | --- |
| 2026-10-13T05:40:13.014200+02:00 | MISSED | Non executee avant pause ; aucun rattrapage retroactif |
| 2026-10-13T06:10:13.014200+02:00 | MISSED | Non executee avant pause ; aucun rattrapage retroactif |
| 2026-10-13T06:40:13.014200+02:00 | MISSED | Non executee avant pause ; aucun rattrapage retroactif |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT = envoi au premier delta texte ; débit = output natif / durée premier–dernier delta texte, hors raisonnement. Horodatages conservés, sessions jetables supprimées, aucun outil/fichier/accès métier réseau.
TTMT min/max 1.699/2.531 s ; débit min/max 219.342/383.205. Surcharge séparée : entrée 47610, sortie 3647, raisonnement 2282, coût natif 0.005947252.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 206 | 35.1 % |
| assistant | 381 | 64.9 % |
| Total | 587 | 100.0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 554 | 25.3 % |
| step-start | 381 | 17.4 % |
| reasoning | 429 | 19.6 % |
| tool | 444 | 20.3 % |
| step-finish | 379 | 17.3 % |
| compaction | 3 | 0.1 % |
| Total | 2190 | 100.0 % |

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 121 | 27.3 % | 121 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 113 | 25.5 % | 113 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 113 | 25.5 % | 113 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 32 | 7.2 % | 27 (84.4 %) | 1 (3.1 %) | 4 (12.5 %) |
| cgpt-validation_request_validation | 32 | 7.2 % | 30 (93.8 %) | 0 (0.0 %) | 2 (6.2 %) |
| cgpt-validation_poll_approval | 2 | 0.5 % | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| cgpt-validation_get_approval | 1 | 0.2 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 11 | 2.5 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 19 | 4.3 % | 19 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 444 | 100.0 % | 436 (98.2 %) | 1 (0.2 %) | 7 (1.6 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 213 | 55.9 % |
| stop | 165 | 43.3 % |
| None | 2 | 0.5 % |
| length | 1 | 0.3 % |
| Total | 381 | 100.0 % |

| Composante tokens native | Nombre | Part des composantes |
| --- | --- | --- |
| input | 2392404 | 3.7 % |
| output | 133589 | 0.2 % |
| reasoning | 84439 | 0.1 % |
| cache_read | 62476777 | 96.0 % |
| cache_write | 0 | 0.0 % |
| Total | 65087209 | 100.0 % |

Coût natif cumulé 0.407799554 ; devise/unité non exposée, aucune conversion. Cache séparé ; somme des composantes sans équivalence de facturation inventée. Pourcentages à une décimale, écarts d’arrondi possibles.

| Provider/model/variant natifs | Messages assistant | Part |
| --- | --- | --- |
| opencode-go / muse-spark-1.3-contributor / high | 378 | 99.2 % |
| opencode-go / muse-spark-1.3-contributor / None | 3 | 0.8 % |
| Total | 381 | 100.0 % |

## 3. Fichiers modifiés

| Chemin absolu après archive | Tentatives | Part | Terminées | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-export-manifest-persistence-v1/proposal.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-export-manifest-persistence-v1/design.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-export-manifest-persistence-v1/tasks.md | 2 | 18.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-export-manifest-persistence-v1/specs/bulk-operations/spec.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_export_manifest_record.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_export_manifest_repository.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0010_bulk_export_manifest.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_export_manifest_persistence.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_export_manifest_persistence_integration.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 | 100.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

11 tentatives sur dix chemins : six sources (cinq nouvelles et import minimal models.py) plus quatre artefacts déplacés par archive, tasks écrit puis coché après preuves. Présent rapport hors intervalle et sous mandat distinct ; checkpoint orchestrateur hors télémétrie OpenCode. Horodatage DEVOPS actualisé par DIU hors agent, identifié séparément ; aucune autre modification hors périmètre observée. Git non inspecté.

## 4. Commandes

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 4 | 21.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test CAB | 2 | 10.5 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 15.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 3 | 15.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PostgreSQL réel | 7 | 36.8 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 19 | 100.0 % | 19 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : zéro (0.0 %). Libellés limités à100 caractères ; commandes exactes/requestId dans historique/checkpoint.

| Commande, libellé | Exécutions | Part |
| --- | --- | --- |
| /home/devops/.local/npm/bin/openspec validate add-bulk-export-manifest-persistence-v1 --strict --js… | 2 | 10.5 % |
| /usr/bin/true | 2 | 10.5 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_export_manifest_recor… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_export_manifest_persis… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/unit -p test_bulk_exp… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_export_manifest… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.3 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 5.3 % |
| /home/devops/.local/npm/bin/openspec archive add-bulk-export-manifest-persistence-v1 --yes --skip-s… | 1 | 5.3 % |
| Total | 19 | 100.0 % |

Seul global strict exit1 ; toutes les autres commandes exit0. Les prévols distincts utilisent des requestId neufs et ne rejouent aucune permission. Aucun test ignoré/interrompu compté vert.

## 5. Accès web

Aucun webfetch/websearch : zéro succès/refus/erreur ; taux N/A, dénominateur nul. Aucune URL visitée/refusée par ces outils. API locales, fournisseur d’inférence/quotas autorisé et PostgreSQL de test hors de ce domaine ; aucun déploiement ni effet métier externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif | 2026-10-13T05:09:49.927000+02:00 |
| Fin du codage et archivage | 2026-10-13T08:03:37.525970+02:00 |
| Fin après sonde et quota natif | 2026-10-13T08:09:03.191000+02:00 |
| Durée globale avec pauses/attentes | 02 h 59 min 13 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début du change | 2026-10-13T05:09:49.935552+02:00 | N/A | N/A |
| Reprise — avant code | 2026-10-13T06:56:22.594910+02:00 | 22 % | 2026-10-18T05:58:02+02:00 |
| Après — après archivage | 2026-10-13T08:09:03.191000+02:00 | 1 % | 2026-10-20T06:59:31+02:00 |
| Différence après − avant | — | N/A | — |
| Différence depuis reprise | — | N/A | Fenêtre différente |

Outil natif get_usage_limits absent au début du change, puis exposé à la reprise et à la fin. Source codex/window10080 utilisée, aucun quota Go substitué. Valeurs utilisées22 % puis1 %, resetsAt différents : aucune soustraction ni consommation négative inventée. Identité de compte comparée par empreinte non secrète. Quotas partagés par compte ; aucune attribution exclusive ni conversion en tokens/euros.

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| others | 414 | 93.2 % | 406 (98.1 %) | 1 (0.2 %) | 7 (1.7 %) |
| files | 11 | 2.5 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commands | 19 | 4.3 % | 19 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 444 | 100.0 % | 436 (98.2 %) | 1 (0.2 %) | 7 (1.6 %) |

Totaux croisés : 444 = 436 terminés + 1 refus + 7 erreurs = 414 autres + 11 fichiers + 19 commandes ; 31 décisions uniques dont30approved/1rejected, 30 effets natifs, SSE reprise25once/1reject et cinq permissions anciennes N/A. Historique complet borné : ses_eccc32018ffesxjkrX26FMr36l (587 messages).

Livraison : primitive ExportManifestV1 append-only 17 clés, PK technique hors17, compteurs TEXT privés, captures pures figées, transaction propriétaire et migration0010 réversible. Données complete/références/compteurs/versions/classification/consistance ne prouvent ni finalisation, disponibilité READY ni autorisation READ_RESULT. 167 unittest, sept suites PG, six sources compilées, archive unique et rapport distinct. B12 global reste partiel ; pas de producteur export, URL signée, hash calculé, horloge, provider, endpoint, Outbox ou nouvelle norme/dépendance/cadrage. Frontend/navigateur sans objet. Git non inspecté, aucun commit/push. Secrets confinés aux processus de test/authentification/quota autorisés, aucune valeur dans modèle/sources/rapport. Le RUN parent continue après la clôture du seul sous-job.
