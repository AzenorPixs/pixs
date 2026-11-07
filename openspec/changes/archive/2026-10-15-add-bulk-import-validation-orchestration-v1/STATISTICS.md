# STATISTIQUES — add-bulk-import-validation-orchestration-v1

RUN : `cismp-pixs-01a13bab2ed7`. Archive réelle : `openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1`. Rapport par archive, avant publication/libération.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | OpenCode Go | high | 2,806 s | 298,7 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; modèle N/A | OpenCode Go | N/A — API summarize sans variant | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Les métriques de débit/TTMT du codage proviennent uniquement des sondes dédiées valides, moyenne arithmétique. Aucune sonde de l’orchestrateur. Version exacte du modèle et temps de génération isolé non exposés : N/A. Les durées natives des messages incluent outils/attentes ; elles ne sont pas assimilées au service du LLM. Dénominateur du temps de service cumulé indisponible, chevauchements non quantifiés. La compaction est une surcharge technique distincte ; le travail métier reste explicitement high. Coordination CISMP2/CISMP3 : sans écriture de ce change et sans attribution arbitraire de leurs coûts.

## 1. Statistiques générales et décisions

Périmètre : historique complet des trois sessions natives de ce change, arrêté au relevé final après archivage et sonde finale. Les sondes jetables et leur coût sont séparés. Aucun événement d’un autre RUN n’est imputé à ce rapport.

| Mesure | Valeur | Part |
| --- | --- | --- |
| Messages natifs | 701 | 100,0 % |
| Appels outils natifs | 572 | 100,0 % |
| Appels achevés/autorisés¹ | 547 | 95,6 % |
| Refus de permission | 2 | 0,3 % |
| Erreurs/interruption outil | 23 | 4,0 % |
| Réponses de compaction | 4 | 0,7 % |

¹ « Achevé/autorisé » désigne un outil à état natif completed, autorisé automatiquement ou via CAB. Cela ne prouve pas une approbation manuelle. Pour Bash, un diagnostic achevé peut retourner 1 : ses échecs de validation sont distingués des refus de permission et des erreurs MCP. Les décisions de mutation passent par CAB et once ; une réservation seule n’approuve rien.

| Tokens natifs | Nombre | Part |
| --- | --- | --- |
| input | 7340082 | 7,0 % |
| output | 301011 | 0,3 % |
| reasoning | 210850 | 0,2 % |
| cache_read | 96528695 | 92,5 % |
| cache_write | 0 | 0,0 % |
| **Total observé** | 104380638 | 100,0 % |

Coût natif déclaré des réponses OpenCode : 1,029438 USD. Il s’agit de télémétrie, pas d’une facture ni d’une conversion de quota. Métadonnées manquantes/interrompues non estimées.

Résultats finaux : 1 915 tests dans 235/235 modules, 0 ignoré, 0 échec, exit 0 ; 578 régressions Bulk et 29 nouveaux unitaires sont inclus dans ce périmètre et ne s’additionnent pas comme tests uniques. PostgreSQL réel : 34/34 critères (100,0 %), exit 0, schéma nettoyé, connexions fermées, tables publiques stables. Les cinq fichiers Python modifiés ont une compilation native exit 0.

OpenSpec : change validé strictement, archive unique exit 0 avec specsUpdated=true et modified=1. Après synchronisation, contrôle global strict exit 1, 79 éléments dont 77 passent et 2 specs ont uniquement quatre WARNING de longueur, zéro ERROR. Aucun succès strict global n’est revendiqué. Issues inchangées : bulk-operations requirements[6], [10], [13] ; identity-assurance requirements[4]. Canon B07 exactement égal au delta approuvé ; aucun de ces anciens requirements de forme n’a été modifié.

Écarts tracés : première suite monolithique 1 901 tests exit 1 (3 échecs/1 erreur), puis diagnostic protégé ; 22 tests API/PDP passent en processus frais avec chemin de helpers adapté. Une seule fixture de cohabitation Django a été corrigée par remplacement exact, sans code FeatureFlag/modèle/migration modifié. Bash hors mandat et seconde édition après once ont été refusés avant application ; récupérations natives du même job/change effectuées. Ressource sans préfixe et commande de 3 531 caractères annulées sans exécution ; contrôles préventifs de couverture/longueur et verrou par type ajoutés au pilote, hors sources.

Discontinuité d’observation : 2026-10-14 23:27 UTC → 2026-10-15 02:23 UTC, cause non établie, corroborée par CISMP2/CISMP3. Archive/canon/référence 11 réconciliés inchangés ; le même mandat post-archive a été approuvé et exécuté, sans duplication ni réarchivage. Cette période figure dans la durée calendaire, pas dans un temps de service estimé.

### Sondes dédiées

| Position | Envoi UTC | Tokens sortie réels | TTMT (s) | Tokens/s | Retard réel (s) | État |
| --- | --- | --- | --- | --- | --- | --- |
| début change avant écriture | 2026-10-14T18:56:22.749184+00:00 | 609 | 5,001 | 155,4 | N/A | réussie |
| +30 min | 2026-10-14T19:28:00.085879+00:00 | 609 | 3,408 | 280,1 | 87,3 | réussie |
| +60 min | 2026-10-14T19:58:35.602134+00:00 | 609 | 3,861 | 301,4 | 122,8 | réussie |
| +90 min | 2026-10-14T20:27:28.319825+00:00 | 609 | 1,685 | 297,7 | 55,5 | réussie |
| +120 min | 2026-10-14T20:56:45.442305+00:00 | 609 | 2,228 | 312,4 | 12,6 | réussie |
| +150 min | 2026-10-14T21:26:38.341452+00:00 | 609 | 2,559 | 345,9 | 5,5 | réussie |
| +180 min | 2026-10-14T21:56:54.158864+00:00 | 609 | 2,504 | 283,3 | 21,3 | réussie |
| +210 min | 2026-10-14T22:28:11.144145+00:00 | 609 | 2,915 | 368,8 | 98,3 | réussie |
| +240 min | 2026-10-14T23:01:14.856104+00:00 | 609 | 1,872 | 368,5 | 282,0 | réussie |
| fin | 2026-10-15T02:27:25.322808+00:00 | 626 | 2,025 | 273,6 | N/A | réussie |

| Relèves | Nombre | Part |
| --- | --- | --- |
| Réussies | 10 | 58,8 % |
| Échouées | 0 | 0,0 % |
| Manquées | 7 | 41,2 % |
| **Total prévu/fin comprise** | 17 | 100,0 % |

Prompt constant : « Sonde de débit déterministe. Sans outil, accès fichier ni réseau. Écris uniquement les nombres entiers de 0001 à 0200 inclus, chacun sur sa propre ligne, avec exactement quatre chiffres. Aucun autre texte. » Les tailles réelles de sortie sont conservées. Les retards ne sont pas cachés. La première relève est consignée après le cadrage initial ; la phase préalable n’est pas reconstituée. Moyennes : TTMT 2,806 s (min 1,685, max 5,001) ; débit 298,7 tokens/s (min 155,4, max 368,8).

| Sonde manquée — horaire prévu UTC | Cause |
| --- | --- |
| 2026-10-14T23:26:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |
| 2026-10-14T23:56:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |
| 2026-10-15T00:26:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |
| 2026-10-15T00:56:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |
| 2026-10-15T01:26:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |
| 2026-10-15T01:56:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |
| 2026-10-15T02:26:32.816273+00:00 | discontinuité temporelle et attente post-archive ; aucune mesure rétroactive |

Surcharge des 10 sondes : 129908 tokens totaux natifs, 6107 tokens de sortie, 0,012358 USD déclarés ; sessions temporaires fermées. Données exclues des totaux de production ci-dessus. Aucune relève absente n’est recréée rétroactivement.

## 2. Types de messages et d’outils

| Rôle natif | Nombre | Part |
| --- | --- | --- |
| user | 126 | 18,0 % |
| assistant | 575 | 82,0 % |
| **Total** | 701 | 100,0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| compaction | 4 | 0,1 % |
| reasoning | 652 | 24,2 % |
| step-finish | 571 | 21,2 % |
| step-start | 573 | 21,3 % |
| text | 319 | 11,9 % |
| tool | 572 | 21,3 % |
| **Total** | 2691 | 100,0 % |

| Fin des réponses assistant | Nombre | Part |
| --- | --- | --- |
| interrompue/non exposée | 4 | 0,7 % |
| stop | 79 | 13,7 % |
| tool-calls | 492 | 85,6 % |
| **Total** | 575 | 100,0 % |

| Outil | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| bash | 41 | 7,2 % | 40 (97,6 %) | 1 (2,4 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 1 | 0,2 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 145 | 25,3 % | 145 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_cancel_approval | 2 | 0,3 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 77 | 13,5 % | 77 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 1 | 0,2 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 16 | 2,8 % | 6 (37,5 %) | 0 (0,0 %) | 10 (62,5 %) |
| cgpt-validation_request_validation | 71 | 12,4 % | 62 (87,3 %) | 0 (0,0 %) | 9 (12,7 %) |
| edit | 8 | 1,4 % | 7 (87,5 %) | 1 (12,5 %) | 0 (0,0 %) |
| glob | 8 | 1,4 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 42 | 7,3 % | 41 (97,6 %) | 0 (0,0 %) | 1 (2,4 %) |
| read | 139 | 24,3 % | 136 (97,8 %) | 0 (0,0 %) | 3 (2,2 %) |
| write | 21 | 3,7 % | 21 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| **Total** | 572 | 100,0 % | 547 (95,6 %) | 2 (0,3 %) | 23 (4,0 %) |

| Erreur outil — catégorie | Nombre | Part |
| --- | --- | --- |
| Interruption/autre erreur outil | 6 | 26,1 % |
| MCP timeout | 17 | 73,9 % |
| **Total** | 23 | 100,0 % |


## 3. Fichiers modifiés

Le tableau mesure les tentatives d’écriture natives write/edit, pas les appels système internes au CLI. Les chemins actifs des cinq artefacts OpenSpec sont rattachés ci-dessous à leur destination d’archive réelle.

| Chemin absolu complet | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/design.md | 2 | 6,9 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/proposal.md | 1 | 3,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/specs/bulk-operations/spec.md | 1 | 3,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/tasks.md | 5 | 17,2 % | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_import_validate.py | 4 | 13,8 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_private_object_reader.py | 4 | 13,8 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_import_validate_postgres_integration.py | 8 | 27,6 % | 7 (87,5 %) | 1 (12,5 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_postgres_source_integration.py | 1 | 3,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_import_validate.py | 3 | 10,3 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| **Total** | 29 | 100,0 % | 28 (96,6 %) | 1 (3,4 %) | 0 (0,0 %) |

Le CLI a également créé .openspec.yaml puis déplacé les cinq artefacts vers l’archive et synchronisé /home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md. Ces effets sont vérifiés par empreintes/JSON ; leur nombre d’appels physiques d’écriture est N/A, non instrumenté. Le fichier STATISTIQUES.md lui-même est créé après cette borne de collecte sous mandat distinct et n’est pas inclus dans les tentatives précédentes. Aucun Git utilisé pour déduire les fichiers.

| Fichier présent après archive | Empreinte SHA-256 |
| --- | --- |
| /home/devops/datas/pixs/src/pixs/backend/bulk_private_object_reader.py | c7b6f58dbe7fe4b827402a4918f08b099765a01828f39dd8218e62e3e9a642fc |
| /home/devops/datas/pixs/src/pixs/backend/bulk_import_validate.py | 992beea5413ea15736ba38d972a104971daed45508aada6671136f3ff894aa1c |
| /home/devops/datas/pixs/tests/unit/test_bulk_import_validate.py | 1ac97d44fc476bf210320c15358a53d6a78fbc7f5dde0a4ed52adaf788e8c0e7 |
| /home/devops/datas/pixs/tests/integration/test_bulk_import_validate_postgres_integration.py | 7dfcd1dbe6f2d8b7b9f62a031a74297825d1f8128b60aa3b160fa38127119bf5 |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_postgres_source_integration.py | 5b10a7d75a99422e54693d9bde6148be566299f2787ca493f8d5eb979d662063 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/.openspec.yaml | cd54fe01555559ffd5cf6f7f1d1b06209492e5ba9147cdc3800201c09e2291d0 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/proposal.md | ae3c097e594934bb65ffd076149698fa27a79a0cf0d040d189e4ce2a971b2b63 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/design.md | 2ff063d023094210ed1501ae8c01b7b91ae6b3978c621feb7b778bc16c9ad2bc |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/tasks.md | ca9fd48f5b955d9abb37fc173201da748b1e9f72f359f83650ad8edf88626b35 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-import-validation-orchestration-v1/specs/bulk-operations/spec.md | 34f45ee103b33b19393422e9462e0401035a6230e8f70f50ac37cd492eb976b4 |
| /home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md | 4264d3ffcd13d394e46e62e7b6fadab3022f1f029729852291374d7a287eb424 |

Les 100 fichiers initiaux ciblés ont été comparés sans Git : seul le lecteur privé existant change, plus la fixture additionnelle avec remplacement inverse vérifié ; trois nouveaux fichiers Python. Les modèles de production et bulk_trusted_ports.py restent inchangés. La provenance Git historique demeure non inspectée.

## 4. Commandes

| Famille | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Aide CLI OpenSpec | 1 | 2,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Archive OpenSpec | 1 | 2,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commande hors mandat refusée | 1 | 2,4 % | 0 (0,0 %) | 1 (100,0 %) | 0 (0,0 %) |
| Compilation Python | 8 | 19,5 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Préparation OpenSpec | 1 | 2,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Prévol CAB /usr/bin/true | 10 | 24,4 % | 10 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Tests et diagnostics Python | 15 | 36,6 % | 15 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Validation OpenSpec | 4 | 9,8 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| **Total** | 41 | 100,0 % | 40 (97,6 %) | 1 (2,4 %) | 0 (0,0 %) |

| Code de sortie Bash achevé | Occurrences | Part |
| --- | --- | --- |
| 0 | 34 | 85,0 % |
| 1 | 6 | 15,0 % |
| **Total achevé** | 40 | 100,0 % |

Les codes 1 comprennent les diagnostics/validations échoués conservés dans l’historique ; ils ne sont pas des refus CAB. La validation finale applicable est celle exposée en section 1. La commande globale compacte a lancé 235 sous-processus de modules ; les autres sous-processus internes aux tests ne sont pas instrumentés et ne sont pas inventés.

### Toutes les commandes natives observées

| Libellé (100 caractères max) | Occurrences | Part | Achevées | Refusées | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive --help | 1 | 2,4 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec archive add-bulk-import-validation-orchestration-v1 --yes --js… | 1 | 2,4 % | 1 | 0 | 0 |
| ls /home/devops/datas/pixs/.venv/lib/python*/site-packages/django/db/backends/dummy/ 2>/dev/null \|\|… | 1 | 2,4 % | 0 | 1 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_import_validate.py | 2 | 4,9 % | 2 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_private_object_reader… | 1 | 2,4 % | 1 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_import_validate… | 3 | 7,3 % | 3 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_feature_flag_postgre… | 1 | 2,4 % | 1 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_import_validate.py | 1 | 2,4 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec new change add-bulk-import-validation-orchestration-v1 | 1 | 2,4 % | 1 | 0 | 0 |
| /usr/bin/true | 10 | 24,4 % | 10 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B - <<'DIAGNOSTIC' import contextli… | 1 | 2,4 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s tests -p … | 1 | 2,4 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s tests -p … | 1 | 2,4 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s tests/int… | 2 | 4,9 % | 2 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_import… | 2 | 4,9 % | 2 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_privat… | 2 | 4,9 % | 2 | 0 | 0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/test_bulk_impor… | 3 | 7,3 % | 3 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B - <<'V' import sys,jso… | 1 | 2,4 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integratio… | 1 | 2,4 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integratio… | 1 | 2,4 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 | 4,9 % | 2 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate add-bulk-import-validation-orchestration-v1 --strict | 2 | 4,9 % | 2 | 0 | 0 |
| **Total** | 41 | 100,0 % | 40 | 1 | 0 |

### Commandes refusées regroupées

| Commande refusée (jamais exécutée) | Nombre | Part des refus |
| --- | --- | --- |
| ls /home/devops/datas/pixs/.venv/lib/python*/site-packages/django/db/backends/dummy/ 2>/dev/null \|\|… | 1 | 100,0 % |
| **Total refusé** | 1 | 100,0 % |

La demande de 3 531 caractères dépassait la limite CAB et a été CANCELLED sans appel Bash : elle n’est pas comptée comme commande exécutée. Sa version compacte de 1 702 caractères est celle du passage final complet.

## 5. Accès web

| Résultat outil web | Nombre | Taux |
| --- | --- | --- |
| Achevé/autorisé | 0 | N/A |
| Refusé | 0 | N/A |
| Erreur | 0 | N/A |
| **Total observé** | 0 | N/A |

Aucun outil de consultation web observé dans ces sessions : aucune URL de source visitée ou refusée à lister. Dénominateur nul, taux N/A. Cela ne signifie pas absence de transport réseau : OpenCode Go sert le modèle, CAB/OpenCode utilisent les API locales et le test PostgreSQL la boucle locale. Le nombre de requêtes réseau internes est N/A, non instrumenté ; aucun accès refusé n’est présenté comme visité.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-14T18:51:19.570000+00:00 |
| Fin — après archivage | 2026-10-15T02:33:15+00:00 |
| Durée globale (pauses et attentes incluses) | 07 h 41 min 55 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — relevé initial consigné | 2026-10-14T18:56:22.749184+00:00 | 24 % | 2026-10-20T04:59:31+00:00 |
| Après — après archivage et sonde finale | 2026-10-15 02:33:15 UTC | 31 % | 2026-10-20T04:59:31+00:00 |
| Différence après − avant | — | 7 points de pourcentage | — |

Source : outil natif mcp__codex_app__get_usage_limits, quota codex, fenêtre 10080 minutes, même compte vérifié en mémoire sans identifiant publié, même resetsAt. Le relevé initial est conservé. La différence couvre l’intervalle réel des deux relevés (le cadrage initial précède le relevé consigné) ; elle ne couvre pas la rédaction ultérieure du rapport. Quota partagé par le compte : variation non attribuée exclusivement à ce RUN, sans conversion en tokens/euros.

| Domaine d’outils | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Commandes Bash natives | 41 | 7,2 % | 40 (97,6 %) | 1 (2,4 %) | 0 (0,0 %) |
| MCP et autres outils | 502 | 87,8 % | 479 (95,4 %) | 0 (0,0 %) | 23 (4,6 %) |
| Écritures natives fichier | 29 | 5,1 % | 28 (96,6 %) | 1 (3,4 %) | 0 (0,0 %) |
| **Total** | 572 | 100,0 % | 547 (95,6 %) | 2 (0,3 %) | 23 (4,0 %) |

État observé avant publication : code VALIDATE_ONLY, cinq Python compilés, 1 915 tests sans skip, 34 critères PostgreSQL réels, archive unique synchronisée et vérifiée. Limite explicite : strict global exit 1 sur quatre warnings de forme inchangés, aucune nouvelle erreur. Git non consulté, aucun commit/push/branche ; pas de worker, route, provider de production, migration ou dépendance ajouté. Les secrets PostgreSQL/fournisseur restent dans les seuls processus autorisés ; aucune valeur secrète dans les prompts, le checkpoint ou le rapport. Les refus/erreurs opérationnels sont conservés, aucune réarchive. Publication, gate, désarmement et libération sont à effectuer après validation de ce rapport ; le RUN parent reste non terminal et la fenêtre CISMP3 puis CISMP2 demeure réservée.
