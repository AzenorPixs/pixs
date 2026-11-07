# STATISTIQUES — add-initial-job-persistence-record

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-persistence-record. RUN parent cismp-pixs-20261005-2654fe47. Mesures de cette unité, figées avant rédaction/publication du rapport ; sondes séparées de la production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | OpenCode 1.18.34 ; modèle N/A — version non exposée | opencode-go | xhigh natif ; PLLM mode 1 | 1.8779 s — sondes | 68.9158 — sondes | N/A — durée active de production absente |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / famille GPT-6 | N/A — identité exacte non exposée | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — non exposé | N/A — durée active absente |

Temps de service cumulé et sa répartition : N/A, les durées des messages incluent outils/permissions et ne permettent pas d'isoler la génération. Aucun calcul depuis la durée calendaire. Les durées des sondes ci-dessous peuvent chevaucher le travail et ne lui sont pas ajoutées. Sessions de production : ses_ef1d91fd9ffe9pMx6g9s8vqb3H, ses_ef12b41adffeTuZmzycl2bmwZz, ses_ef11b8dedffeVUVvBI6lQGCnsV, ses_ef0ec6a75ffez17s9V3i04UIOb.

## 1. Statistiques générales et décisions

| Mesure | Nombre | Part / base |
| --- | --- | --- |
| Messages | 272 | 100.0 % |
| Parties | 891 | 100.0 % |
| Outils | 150 | 100.0 % |
| Outils terminés | 145 | 96.7 % |
| Erreurs d'outil | 5 | 3.3 % |
| Décisions CAB uniques | 41 | 100.0 % |
| CAB approved | 40 | 97.6 % |
| CAB rejected | 1 | 2.4 % |
| Permissions natives | 41 | 100.0 % |
| once | 39 | 95.1 % |
| reject | 2 | 4.9 % |

| Résultats retenus | Nombre | Part / limite |
| --- | --- | --- |
| Nouveaux parents unittest | 2 | 1 offline + 1 harnais sûr ; 100.0 % réussis |
| Régression de base | 111 | 20 modules ; 100.0 % réussis |
| Suites PG existantes sûres | 8 | 3 modules ; 100.0 % réussis |
| Total unittest final | 121 | 100.0 % — 0 erreur/échec/skip retenu |
| Premier essai unittest en échec | 1 | 1 / 122 exécutions de tests : 0.8 % ; corrigé puis réussi |
| Total unittest toutes tentatives | 122 | 121 réussies : 99.2 % ; 100.0 % des exécutions |
| Validations PG réelles post-code | 3 | JobRecord + fanions + connectivité ; 100.0 % réussies |
| Prévol PG SELECT 1 | 1 | 100.0 % réussi ; séparé des trois validations post-code |
| py_compile | 5 | 100.0 % exit0 |
| Stricts pré/post-code | 6 | 100.0 % exit0 |
| Tâches prouvées/cochées | 7 | 100.0 % |
| Références inchangées | 120 | 100.0 % du périmètre protégé final |
| Fichiers existants adaptés | 2 | models.py + seule assertion FF ; changements approuvés |
| Archive unique vérifiée | 1 | 100.0 % ; canon +0/~0/-0/→0 |

Natif : régression 111 tests / 0.724 s ; suites PG sûres 8 / 0.851 s ; parent offline 1 / 0.199 s ; parent PG sûr 1 / 0.170 s. Détail des cas internes offline : N/A mesuré (sortie enfant capturée) ; 15 cas attendus dans la source, compteur positif contrôlé par le parent, marqueur exact et gardes validés. Ne pas ajouter ces cas internes au total unittest.

PG JobRecord : forward0001/0002, roundtrip13 champs, défaut tentative0, huit CHECK, SQL NULL JSON, doublonPK, limite DB/Python SemVer, suppression de la ligne, reverse0002 seul, identité catalogue FF stable, nettoyage et connexions fermées prouvés par le résultat fermé real_pg=True. Les deux harnais PG existants rendent ok=True avec fermetures/nettoyage requis. Aucun repli simulé présenté comme preuve réelle ; requêtes/durées SQL granulaires N/A — non instrumentées.

Récupérations : le premier test offline a échoué avant connexion faute de NAME synthétique, corrigé sous mandat distinct. Demande CAB mal typée puis réutilisation de nonce/commande divergente rejetée ; deux Bash hors mandat exact (true et suffixe echo) retenus/refusés avant exécution ; maîtres R5/R6/R7 repris, processus/interface OpenCode préservés. Deux rapports OC inventaient libellés/durée ou clés PG : rectifiés, preuves natives seules retenues. Readiness pending1 transitoire réconcilié à0 ; aucune permission/effect non maîtrisé. Refus, échec de test et erreur technique restent distincts.

| Compteur natif production | Valeur |
| --- | --- |
| input | 1188 |
| output | 145303 |
| reasoning | 0 |
| cache_read | 14023102 |
| cache_write | 854909 |
| Somme disponible | 15024502 |
| Coût déclaré API USD | 0.463822042 |
| Réponses interrompues sans usage final | 3 |

Usage final absent pour msg_10ed11c1b001ajknmerVTRsbv4, msg_10ee0527f001h9eVw2yHK6AhWn, msg_10f120c5c001VQ1Yv9J6Eyc62y: N/A de consommation pour ces réponses, jamais remplacé par zéro. reasoning=0 est le compteur déclaré, pas une preuve d'absence de raisonnement. Cache cumulé au fil des requêtes, pas taille de contexte unique ; coût API déclaré, pas facture Go.

Compaction cismp-pixs-20261005-2654fe47-compaction-0022 : PARTIAL_NON_BLOCKING ; résumé natif N/A achevé ; API orchestrateur non exposée, opération root non exécutée. Configuration xhigh du compacteur vérifiée, variante du message natif non exposée ; état partiel, jamais réussite conjointe. Après réconciliation réelle READY/pending0, le RUN a continué sans dérogation.

Compaction cismp-pixs-20261005-2654fe47-compaction-0208 : NATIVE_COMPLETE_ROOT_PARTIAL ; résumé natif msg_10efc07f3001kHR2IEPbAtVOVO achevé ; API orchestrateur non exposée, opération root non exécutée. Configuration xhigh du compacteur vérifiée, variante du message natif non exposée ; état partiel, jamais réussite conjointe. Après réconciliation réelle READY/pending0, le RUN a continué sans dérogation.

| Sondes | Nombre | Part |
| --- | --- | --- |
| Prévues | 7 | 100.0 % |
| Réussies | 7 | 100.0 % |
| Échouées | 0 | 0.0 % |
| Manquées | 0 | 0.0 % |

| Position | Envoi UTC | État | Sortie tokens | TTMT s | Génération s | Tokens/s |
| --- | --- | --- | --- | --- | --- | --- |
| début JobRecord persistance | 2026-10-06T00:43:45.973075+00:00 | success | 562 | 2.0127 | 5.4221 | 103.6508 |
| +30 min | 2026-10-06T01:13:46.531676+00:00 | success | 1069 | 1.9556 | 21.1278 | 50.5969 |
| +60 min | 2026-10-06T01:43:46.482662+00:00 | success | 270 | 1.6858 | 5.212 | 51.8035 |
| +90 min | 2026-10-06T02:13:46.490394+00:00 | success | 1667 | 2.1852 | 23.7601 | 70.1595 |
| +120 min | 2026-10-06T02:43:46.483561+00:00 | success | 601 | 1.7461 | 6.9654 | 86.2837 |
| +150 min | 2026-10-06T03:13:46.488747+00:00 | success | 139 | 1.7405 | 3.0782 | 45.1566 |
| fin | 2026-10-06T03:33:59.337273+00:00 | success | 225 | 1.8195 | 3.0096 | 74.7599 |

| Position | Premier token UTC | Dernier token UTC | Durée collecte s | Coût API USD |
| --- | --- | --- | --- | --- |
| début JobRecord persistance | 2026-10-06T00:43:47.985795+00:00 | 2026-10-06T00:43:53.407844+00:00 | 14.042 | 0.00238564 |
| +30 min | 2026-10-06T01:13:48.487273+00:00 | 2026-10-06T01:14:09.615031+00:00 | 28.0693 | 0.00262393 |
| +60 min | 2026-10-06T01:43:48.168470+00:00 | 2026-10-06T01:43:53.380470+00:00 | 7.0285 | 0.0022484 |
| +90 min | 2026-10-06T02:13:48.675591+00:00 | 2026-10-06T02:14:12.435723+00:00 | 28.0588 | 0.00290499 |
| +120 min | 2026-10-06T02:43:48.229650+00:00 | 2026-10-06T02:43:55.195050+00:00 | 14.0433 | 0.00240397 |
| +150 min | 2026-10-06T03:13:48.229223+00:00 | 2026-10-06T03:13:51.307401+00:00 | 7.0341 | 0.00218683 |
| fin | 2026-10-06T03:34:01.156747+00:00 | 2026-10-06T03:34:04.166378+00:00 | 7.0448 | 0.00222725 |

Sondes valides : TTMT moyen/min/max 1.8779/1.6858/2.1852 s ; débit moyen arithmétique/min/max 68.9158/45.1566/103.6508 tokens/s. Surcharge séparée : 78796 tokens déclarés dont 4533 sortie, 105.3208 s de collecte et 0.016981010 USD API. 100.0 % des sondes sans outil, sessions dédiées supprimées. Version modèle non exposée, même identité/configuration native ; conformité aux 128 lignes demandées non mesurée, aucun volume produit revendiqué.

Prompt constant : Output exactly 128 identical lines, each containing: 0123456789 abcdefghijklmnopqrstuvwxyz. Do not explain. Do not call tools. Relèves 30 min concurrentes ; aucune attente de créneau n'a suspendu le travail. La sonde finale a suivi la preuve d'archivage ; son helper a émis par erreur l'étiquette héritée +60 min, reclassée fin sur ses horodatages vérifiables, sans refaire/altérer la mesure.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part messages |
| --- | --- | --- |
| assistant | 201 | 73.9 % |
| user | 71 | 26.1 % |
| Total | 272 | 100.0 % |

| Type de partie | Nombre | Part parties |
| --- | --- | --- |
| compaction | 1 | 0.1 % |
| reasoning | 201 | 22.6 % |
| step-finish | 198 | 22.2 % |
| step-start | 201 | 22.6 % |
| text | 140 | 15.7 % |
| tool | 150 | 16.8 % |
| Total | 891 | 100.0 % |

| Fin réponse assistant | Nombre | Part |
| --- | --- | --- |
| error:MessageAbortedError | 3 | 1.5 % |
| stop | 68 | 33.8 % |
| tool-calls | 130 | 64.7 % |
| Total | 201 | 100.0 % |

| Outil | Appels | Part | Terminés | Erreurs | Autorisation / base |
| --- | --- | --- | --- | --- | --- |
| bash | 26 | 17.3 % | 24 | 2 | 24 once / 2 reject ; exit séparé |
| cgpt-validation_broker_readiness | 11 | 7.3 % | 11 | 0 | N/A — observation/lecture |
| cgpt-validation_get_approval | 2 | 1.3 % | 2 | 0 | N/A — observation/lecture |
| cgpt-validation_poll_approval | 1 | 0.7 % | 0 | 1 | N/A — observation/lecture |
| cgpt-validation_request_validation | 42 | 28.0 % | 40 | 2 | 41 décisions uniques ; 42 demandes dont nonce réutilisé |
| edit | 2 | 1.3 % | 2 | 0 | once : 2 ; aucun refus |
| glob | 6 | 4.0 % | 6 | 0 | N/A — observation/lecture |
| grep | 3 | 2.0 % | 3 | 0 | N/A — observation/lecture |
| read | 44 | 29.3 % | 44 | 0 | N/A — observation/lecture |
| write | 13 | 8.7 % | 13 | 0 | once : 13 ; aucun refus |
| Total | 150 | 100.0 % | 145 | 5 | Permissions et décisions : bases distinctes |

## 3. Fichiers modifiés

| Chemin absolu actuel | Tentatives | Part éditions | Approuvées/réussies | Refusées | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-persistence-record/.openspec.yaml | 1 | 6.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-persistence-record/design.md | 2 | 13.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-persistence-record/proposal.md | 2 | 13.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-persistence-record/specs/jobs/spec.md | 1 | 6.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-persistence-record/tasks.md | 3 | 20.0 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0002_job_record.py | 1 | 6.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 6.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_postgres_source_integration.py | 1 | 6.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_job_record_postgres_integration.py | 1 | 6.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_job_record.py | 2 | 13.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Total | 15 | 100.0 % | 15 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

10 fichiers distincts / 15 tentatives : cinq artefacts créés puis déplacés dans l'archive ; proposal/design retouchés pour cohérence, tasks créé/cohérent/coché ; modèle existant étendu, migration et deux tests ajoutés ; NAME unitaire corrigé ; ancienne assertion FF seule adaptée, tous autres octets exacts. Dix cibles SHA/UTF-8/LF vérifiées, 120 empreintes inchangées et classe FF d'origine byte exacte. Caches bytecode régénérables autorisés ; STATISTIQUES.md exclu de cette collecte.

## 4. Commandes

| Famille | Tentatives | Part | Terminées | Exit0 | Exit non0 | Exit absent/abandon |
| --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 3.8 % | 1 | 1 | 0 | 0 |
| OpenSpec validation | 6 | 23.1 % | 6 | 6 | 0 | 0 |
| Python PG réel | 4 | 15.4 % | 4 | 4 | 0 | 0 |
| Python compilation | 5 | 19.2 % | 5 | 5 | 0 | 0 |
| Python unittest | 6 | 23.1 % | 5 | 4 | 1 | 1 |
| Test CAB / autre | 4 | 15.4 % | 3 | 3 | 0 | 1 |
| Total | 26 | 100.0 % | 24 | 23 | 1 | 2 |

| Commande (100 caractères max) | Occurrences | Part Bash | Terminées | Erreurs outil | Exit |
| --- | --- | --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-job-persistence-record --yes | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 7.7 % | 2 | 0 | {'0': 2} |
| /home/devops/.local/npm/bin/openspec validate --specs --strict | 2 | 7.7 % | 2 | 0 | {'0': 2} |
| /home/devops/.local/npm/bin/openspec validate add-initial-job-persistence-record --strict | 2 | 7.7 % | 2 | 0 | {'0': 2} |
| /home/devops/python/current/bin/python3 -B -c 'print(1)' | 3 | 11.5 % | 3 | 0 | {'0': 3} |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/backend/migrations/0002_job_record.py | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/backend/models.py | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_feature_flag_postgres_… | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_job_record_postgres_in… | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_job_record.py | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integrati… | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integrati… | 1 | 3.8 % | 0 | 1 | {'None': 1} |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p t… | 2 | 7.7 % | 2 | 0 | {'1': 1, '0': 1} |
| PYTHONPATH=src:tests/integration:. /home/devops/python/current/bin/python3 -B -c 'print(__import__(… | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:tests/integration:. /home/devops/python/current/bin/python3 -B -c 'print(outcome := … | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:tests/integration:. /home/devops/python/current/bin/python3 -B -c 'print(outcome := … | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:tests/integration:. /home/devops/python/current/bin/python3 -B -c 'print(outcome := … | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:tests/unit:tests/integration:. /home/devops/python/current/bin/python3 -B -m unittes… | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| PYTHONPATH=src:tests/unit:tests/integration:. /home/devops/python/current/bin/python3 -B -m unittes… | 1 | 3.8 % | 1 | 0 | {'0': 1} |
| true | 1 | 3.8 % | 0 | 1 | {'None': 1} |

| Commandes refusées regroupées | Occurrences | Part des refus | Statut |
| --- | --- | --- | --- |
| /home/devops/python/current/bin/python3 -B -c 'print("CAB_JOB_RECORD_RECOVERY_OK")' | 1 | 33.3 % | CAB rejected — non exécutée |
| true | 1 | 33.3 % | Permission native reject — non exécutée |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integrati… | 1 | 33.3 % | Permission native reject — non exécutée |
| Total | 3 | 100.0 % | Refus CAB et natifs distincts, pas échecs de tests |

Commandes exactes et requestId conservés dans le checkpoint/parties natives ; libellés seuls tronqués. 24 Bash exécutés : 23 exit0 et 1 exit1 (premier offline corrigé) ; deux Bash interrompus avant effet. Trois tests CAB print(1) réussis lors des reprises. La décision CAB approuvée du harnais PG sûr -01 n'a pas autorisé le suffixe echo et n'a produit aucune exécution conforme ; -02 est un nouveau mandat réussi.

## 5. Accès web

| Web du codeur | Nombre | Part / base |
| --- | --- | --- |
| Outils web | 0 | 0.0 % |
| URL approuvées/visitées | 0 | N/A — aucune demande |
| URL refusées | 0 | N/A — aucune demande |
| Erreurs web | 0 | N/A — aucune requête |

Aucune URL web demandée ou visitée par le codeur dans ce périmètre. Inférence fournisseur, transport CAB/HTTP local et réseau des tests PostgreSQL autorisés sont distincts. L'orchestrateur a consulté le quota Go à https://opencode.ai/zen/go/v1/usage via un processus sécurisé ; nombre exhaustif d'accès root N/A, non attribué au codeur.

## 6. Synthèse globale

| Mesure de durée globale | Horodatage / durée |
| --- | --- |
| Début UTC | 2026-10-06T00:43:45.267868+00:00 |
| Fin après archivage/sonde/collecte UTC | 2026-10-06T03:36:35.442718+00:00 |
| Durée calendaire | 02:52:50 — 10370.175 s |

Périmètre : préparation, implémentation, vérification, reprises, attentes/pauses et archivage. Rédaction/publication du rapport exclues ; durée calendaire, jamais durée de génération.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-06T00:43:45.267868+00:00 | N/A — mcp__codex_app__get_usage_limits non exposé | N/A |
| Après — après archive et sonde finale | 2026-10-06T03:36:35.170985+00:00 | N/A — catalogue revérifié, outil non exposé | N/A |
| Différence après − avant | — | N/A — absence de relevés natifs comparables | — |

Identité attendue codex, fenêtre 10080 minutes. Aucun quota Go/Spark/historique substitué ; quotas partagés par le compte, une variation disponible pourrait inclure d'autres tâches. Quotas Go séparés contrôlés au 03:22:18 UTC : rolling 13 %, weekly 28 %, monthly 34 %, tous status ok ; ne mesurent pas consommation Codex.

| Domaine | Appels | Part globale | Approbations natives | Refus natifs | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 15 | 10.0 % | 15 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Commandes | 26 | 17.3 % | 24 / 92.3 % | 2 / 7.7 % | 2 / 7.7 % |
| Web | 0 | 0.0 % | N/A | N/A | N/A |
| Autres | 109 | 72.7 % | N/A — lectures/MCP | N/A | 3 / 2.8 % |
| Global | 150 | 100.0 % | 39 / 95.1 % des permissions | 2 / 4.9 % des permissions | 5 / 3.3 % |

Bases : outils pour parts globales et erreurs, permissions natives pour once/reject, décisions CAB uniques pour approbations logiques. Arrondis à une décimale ; sommes arrondies possiblement différentes de 100 %. Autorisation technique ne vaut pas preuve d'exécution, statut outil completed ne vaut pas exit0.

Unité de persistance délivrée : 121 unittest finaux réussis, cinq compilations et six stricts exit0, trois validations PG réelles post-code positives, sept tâches prouvées, archive unique/canon inchangé. Git non inspecté, aucun commit/push observé. Valeurs de secrets non exposées dans les preuves observées ; project.env utilisé uniquement par les processus PG explicitement autorisés. Aucun worker, politique de bail/réessai, autorisation réévaluée, déduplication active, activation production ou contrat Job complet revendiqué. Le RUN parent reste OPEN et poursuit les exigences restantes.
