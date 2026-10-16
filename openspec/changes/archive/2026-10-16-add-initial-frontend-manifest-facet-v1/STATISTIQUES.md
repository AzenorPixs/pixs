# Statistiques — FrontendManifestFacet v1

RUN cismp-pixs-01a13bac8501 ; change add-initial-frontend-manifest-facet-v1 ; contexte217 ; job cismp2-frontend-manifest-facet-2cb385cf339c.
Sessions maîtresses de cette phase : ses_ebcd84836ffe9r7uw4256loxOO, ses_ebca2c867ffe12TMhSkIkpDONu. Collecte bornée avant édition de ce rapport, sondes auxiliaires comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go | high | 1.463 s | 259.972 | N/A — intervalles natifs partiels 243.706 s ; orchestrateur non mesuré |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A — version exacte non exposée | OpenAI | N/A — niveau non exposé | N/A — pas de sonde orchestrateur | N/A | N/A — temps actif non exposé |

Service partiel : union des intervalles texte/raisonnement par message. Les attentes, permissions et durée calendaire ne sont pas du temps de génération ; part cumulée entre agents N/A faute de mesure orchestrateur.

## 1. Statistiques générales et décisions

| Validation métier | Tests | Échecs | Ignorés | Modules |
| --- | --- | --- | --- | --- |
| Testsunitaires39 | 39 | 0 | 0 | 1 |
| Intégration fraîche2 | 2 | 0 | 0 | 1 |
| Régressions manifestFCD48 | 48 | 0 | 0 | 6 |
| Total | 89 | 0 | 0 | 8 |

Trois compilations natives séparées exit0, Python projet3.14.8/cpython-314 ; support>=3.12 conservé, AST3.12 statique distinct. Deux ordres d’import publics frais qualifiés avant tests ; intégration sous gardes avant imports avec canary, contrôles positifs et nettoyage. npm/UI/PostgreSQL : N/A, facette déclarative Python sans interface ni accèsbase.

Durée calendaire 01 h 22 min 28 s, attentes et récupération incluses. Huit tâches cochées uniquement sur preuves. Stricts locaux change/canon et après coches : exit0. Globaux : voir résultats natifs exacts ci-dessous ; quatre WARNING historiques de longueur, zéro ERROR, aucun succès strict global affirmé.

| Contrôle global | Exit natif | Totaux |
| --- | --- | --- |
| frontend_manifest_facet_global_standard_proof | 0 | {'items': 80, 'passed': 80, 'failed': 0} |
| frontend_manifest_facet_global_strict_proof | 1 | {'items': 80, 'passed': 78, 'failed': 2} |
| frontend_manifest_facet_postarchive_strict_proof | 1 | {'items': 79, 'passed': 77, 'failed': 2} |

| Spécification | Niveau | Chemin | Diagnostic |
| --- | --- | --- | --- |
| bulk-operations | WARNING | requirements[6] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |
| bulk-operations | WARNING | requirements[10] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |
| bulk-operations | WARNING | requirements[13] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |
| identity-assurance | WARNING | requirements[4] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |

| Décision MCP terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 28 | 93.3 % |
| REJECTED | 1 | 3.3 % |
| CANCELLED | 1 | 3.3 % |
| Total | 30 | 100 % |

| Mesure native | Valeur |
| --- | --- |
| Messages | 256 |
| Coût déclaré OpenCode | 0.2545040360000001 |
| Tokens total | 14465429 |
| Tokens input | 2098706 |
| Tokens output | 73195 |
| Tokens reasoning | 27310 |
| Tokens cache_read | 12266218 |
| Tokens cache_write | 0 |

Dimensions tokens conservées séparément sans addition susceptible de double compte. Coût déclaré natif : aucune conversion euros ni preuve de facture fournisseur.

| Mesure CAB intégrée | Valeur |
| --- | --- |
| reservedMs | 5115468 |
| busyMs | 1598358 |
| idleMs | 3400387 |
| nativeUnknownMs | 116723 |
| integrationMs | 281011 |
| queueMs | 381256 |
| staleMs | 23538 |
| decisions | {'approved': 28, 'rejected': 1, 'needs_clarification': 0, 'pending': 0, 'once': 28, 'technicalErrors': 0} |
| httpFailures | {'native-validation-not-correlated': 1, 'reservation-version-stale': 5, 'resource-conflict': 1} |

| Latence CAB | Nombre | Moyenne ms | Médiane ms | p95 ms |
| --- | --- | --- | --- | --- |
| requestToDecision | 29 | 15783 | 3863 | 62919 |
| decisionToOnce | 28 | 8091.357142857143 | 6276 | 20995 |
| nativeTool | 151 | 5635.841059602649 | 56 | 53083 |

CAB intégré et messages natifs se recouvrent : ne pas les additionner. Quantiles bornés à2048observations ; durées de conditions non additives, échecsHTTP distincts des refus natifs.

| Session de sonde | Position | TTMT s | Débit réponse tokens/s | Statut |
| --- | --- | --- | --- | --- |
| ses_ebcd39953ffeAV2yLvF0W2Aw5J | début préparation/implémentation FrontendManifestFacet v1 | 1.588 | 472.157 | success |
| ses_ebcb5e817ffew8HsGHmjSrSXyn | périodique après revue modèle avant écriture | 2.415 | 202.326 | success |
| ses_ebc977142ffehAk5ety3kDBfpf | périodique après testsunit39 et revue intégration | 0.931 | 177.754 | success |
| ses_ebc8b99d8ffemuHzhMeVc8iHGC | finale après archive et strictpostarchive | 0.9174 | 187.649 | success |

Sondes exécutées 4, valides 4, échouées 0. Moyennes arithmétiques sur sondes valides seulement ; TTMT première partie texte/raisonnement non vide ; débit réponse seule.

TTMT min/max 0.917/2.415s ; débit réponse min/max 177.754/472.157 tokens/s.

probe_schedule_delays : [{"scheduled_at": "2026-10-16T05:55:49.500000+00:00", "actual_at": "2026-10-16T05:58:11.689977+00:00", "reason": "Revue du modèle et qualification stabilité imports C3 avant écriture, aucune reconstitution rétroactive"}, {"scheduled_at": "2026-10-16T06:28:19.158110+00:00", "actual_at": "2026-10-16T06:31:28.161900+00:00", "reason": "NFDOC intégration en cours puis revueRoot, aucune reconstruction rétroactive"}]

missed_probes : []

Surcharge sondes hors production : {"total": 49883, "input": 44280, "output": 4057, "reasoning": 1094} ; coût N/A noncollecté. Aucun créneau manqué reconstitué.

PLLM de cette invocation 2026-10-16T04:55:23.513005+00:00 : mode1/OpenCodeGo/Muse/high Valide, TTFT visible 8.1996s ; débit global raisonnement+réponse 242.691t/s. Quotas rolling/hebdo/mois [6, 56, 93]%. Benchmark distinct des sondes et tests.

Compactage commun natif05:38:04–05:38:28UTC réussi, high réconcilié ; API Codex absente donc N/A pour compactage conjoint. Historiques et éventuels retards conservés dans checkpoint. La candidate de récupération est un contexte neuf créé 2026-10-16T06:19:04.984000+00:00 : échéance locale 2026-10-16T07:19:04.984000+00:00, cycle commun 2026-10-16T07:08:04.358823+00:00 conservé, aucune compaction fictive. Infrastructure OpenCode1.19.2/CAB1.1.0 ; pas de fermeture/redémarrage pendant le change. DEVOPS régénéré automatiquement par DIU extérieurement au RUN (relevés05:51:18,06:11:08 et06:36:03UTC), chemins runtime/CLI requalifiés sans correction. Dernier relevé natif CLI conservé :1.14.1 ; inventaire :1.14.2, aucune mise à jour par C2.

| Incident de phase | Preuve / traitement |
| --- | --- |
| request_validation timeoutclient puis get/poll mêmeapprovalid APPROVED | {"at": "2026-10-16T05:48:21.166502+00:00", "kind": "request_validation timeoutclient puis get/poll mêmeapprovalid APPROVED", "file": "openspec/changes/add-initial-frontend-manifest-facet-v1/tasks.md", "requestId": "cismp2-d7084eefde80406ea34246056d1348ee", "effect": "Un Write exact prouvé, aucun nouveau request_validation ni doublon"} |
| Write unit natif a omis une seule ligne vide GOLDEN ; AST identique ; compilation lancée prématurément parRoot nonapprouvée etrefusée | {"at": "2026-10-16T06:18:24.001182+00:00", "kind": "Write unit natif a omis une seule ligne vide GOLDEN ; AST identique ; compilation lancée prématurément parRoot nonapprouvée etrefusée", "actual_sha256": "455868e811858f536fb6e9a94b81b06a49beda6fb841a135798f9172e73c566b", "expected_sha256": "2dca6f453038125bf794750fca81ed512c7dca14c9fa7fea92f2c035708db8d8", "compilation_request": {"requestId": "cismp2-de8d0f24dcfc44d6b828c8694223a7fc", "approval_id": "approval-1a9fc93607f2481184ee5e4797441325", "statut": "prescrit", "expected_args": {"requestId": "cismp2-de8d0f24dcfc44d6b828c8694223a7fc", "approval_id": "approval-1a9fc93607f2481184ee5e4797441325", "change_id": "add-initial-frontend-manifest-facet-v1", "session_id": "ses_ebcd84836ffe9r7uw4256loxOO", "directory": "/home/devops/datas/pixs", "run_id": "cismp-pixs-01a13bac8501", "reservation_version": 223, "title": "Compilation tests unitaires FrontendManifestFacet", "summary": "Compilation syntaxique native du seul fichier de tests unitaire revu, cache exact réservé.", "files": [], "commands": ["PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile tests/unit/test_frontend_manifest_facet.py"], "timeout_seconds": 120, "interval_seconds": 3, "resources": [{"key": "file:tests/unit/test_frontend_manifest_facet.py", "mode": "read"}, {"key": "file:tests/unit/__pycache__/test_frontend_manifest_facet.cpython-314.pyc", "mode": "write"}, {"key": "resource:python-runtime", "mode": "read"}]}, "files": [], "commands": ["PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile tests/unit/test_frontend_manifest_facet.py"], "resources": [{"key": "file:tests/unit/test_frontend_manifest_facet.py", "mode": "read"}, {"key": "file:tests/unit/__pycache__/test_frontend_manifest_facet.cpython-314.pyc", "mode": "write"}, {"key": "resource:python-runtime", "mode": "read"}]}, "action": "réconciliation effet connu, conservation source sans réécriture, récupération session obligatoire avant reprise"} |
| Après recover complete versionréservationnative225 nonrecopiée, mandatcompilationv223 nonenregistré, aucun Bash exécuté | {"at": "2026-10-16T06:21:49.197660+00:00", "kind": "Après recover complete versionréservationnative225 nonrecopiée, mandatcompilationv223 nonenregistré, aucun Bash exécuté", "action": "Attendre rapport natif, réconcilier sans réécriture ; version225 conservée"} |

La ligne vide omise par Write a été réconciliée sur AST identique et contenu effectif revu, sans réécriture. Compilation prématurée refusée avant effet, session récupérée avec prévol exact0. Version de réservation périmée après transfert : demande non admise, notificationFAILED/PENDING puis annulation administrative Root ciblée prouvéeCANCELLED ; aucun Bash ni once consommé pour cette demande. Ces incidents ne sont pas des tests réussis. Sous exclusion C2, une tentative inutile d’extension project:* read a reçu409resource-conflict sans mutation ; la règle covers autorise directement cette lecture au propriétaire de l’exclusion. La route integration-status absente a retourné404 ; état relu via /runs et /status, sans effet métier.

## 2. Types de messages et d’outils

| Rôle de message | Nombre | Part |
| --- | --- | --- |
| user | 117 | 45.7 % |
| assistant | 139 | 54.3 % |
| Total | 256 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 255 | 30.3 % |
| step-start | 140 | 16.6 % |
| reasoning | 156 | 18.5 % |
| tool | 151 | 17.9 % |
| step-finish | 139 | 16.5 % |
| compaction | 1 | 0.1 % |
| Total | 842 | 100 % |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 98 | 70.5 % |
| stop | 41 | 29.5 % |
| Total | 139 | 100 % |

| Outil | Total (part) | Réussi (taux) | Refusé (taux) | Erreur (taux) |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 9 (6.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 30 (19.9 %) | 27 (90.0 %) | 0 (0.0 %) | 3 (10.0 %) |
| bash | 20 (13.2 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 5 (3.3 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 70 (46.4 %) | 70 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (5.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 3 (2.0 %) | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| cgpt-validation_broker_health | 3 (2.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (1.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 151 (100.0 %) | 147 (97.4 %) | 0 (0.0 %) | 4 (2.6 %) |

Réussi = completed natif ; les lectures automatiquement permises ne prouvent pas une décision manuelle. Refusé exige un diagnostic explicite. Timeouts et interruptions = erreurs techniques. Exits des Bash vérifiés séparément.

## 3. Fichiers modifiés

| Chemin absolu complet — tentatives | Total (part) | Réussi (taux) | Refusé (taux) | Erreur (taux) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-manifest-facet-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-manifest-facet-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-manifest-facet-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-manifest-facet-v1/specs/frontend/spec.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/manifest/models.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_frontend_manifest_facet.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_frontend_manifest_facet_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 (100.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Source finale | SHA256 |
| --- | --- |
| /home/devops/datas/pixs/src/pixs/kernel/manifest/models.py | 9c0ea7236d5166c15345260a4b0fd0f43731e023a07dd901630c98c7a088b5e0 |
| /home/devops/datas/pixs/tests/unit/test_frontend_manifest_facet.py | 455868e811858f536fb6e9a94b81b06a49beda6fb841a135798f9172e73c566b |
| /home/devops/datas/pixs/tests/integration/test_frontend_manifest_facet_integration.py | f95912706a205d14b78d86122f9728adc0736ac2ad66d440c6395054a343ec01 |

EffetsCLI new/py_compile/archive distincts des éditions natives. Checkpoint et caches exacts régénérables ne sont pas des sources fonctionnelles. Archive /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-frontend-manifest-facet-v1 unique, cinq artefacts déplacés exacts, --skip-specs/canon préservé. Rapport distinct hors borne, aucune réarchive.

## 4. Commandes

| Famille de commande | Nombre | Part |
| --- | --- | --- |
| Prévol | 2 | 10.0 % |
| OpenSpec | 9 | 45.0 % |
| Autre | 3 | 15.0 % |
| Compilation Python | 3 | 15.0 % |
| Tests Python | 3 | 15.0 % |
| Total | 20 | 100 % |

| Commande (100 caractères max) | État | Exit natif | Occurrences | Part |
| --- | --- | --- | --- | --- |
| /usr/bin/true | réussi | 0 | 2 | 10.0 % |
| /home/devops/.local/npm/bin/openspec new change add-initial-frontend-manifest-facet-v1 | réussi | 0 | 1 | 5.0 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-frontend-manifest-facet-v1 --strict --json | réussi | 0 | 3 | 15.0 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -c 'print(__impo… | réussi | 0 | 1 | 5.0 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile sr… | réussi | 0 | 1 | 5.0 % |
| PYTHONPATH=src TMPDIR=/home/devops/datas/pixs PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/da… | réussi | 0 | 1 | 5.0 % |
| PYTHONPATH=src TMPDIR=/home/devops/datas/pixs PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/da… | réussi | 0 | 1 | 5.0 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile te… | réussi | 0 | 1 | 5.0 % |
| PYTHONPATH=src TMPDIR=/home/devops/datas/pixs PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/da… | réussi | 0 | 1 | 5.0 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile te… | réussi | 0 | 1 | 5.0 % |
| PYTHONPATH=src TMPDIR=/home/devops/datas/pixs PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/da… | réussi | 0 | 1 | 5.0 % |
| PYTHONPATH=src TMPDIR=/home/devops/datas/pixs PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/da… | réussi | 0 | 1 | 5.0 % |
| /home/devops/.local/npm/bin/openspec validate frontend --type spec --strict --json | réussi | 0 | 1 | 5.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --json | réussi | 0 | 1 | 5.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | réussi | 1 | 2 | 10.0 % |
| /home/devops/.local/npm/bin/openspec archive add-initial-frontend-manifest-facet-v1 --yes --skip-sp… | réussi | 0 | 1 | 5.0 % |

Commandes complètes/corrélations/exits dans frontend_manifest_facet_command_results et historique natif. Prévol technique distinct des tests métier. Exits1 de strict global = résultats de validation, pas des refus de permission. Demandes refusées/annulées sans Bash ne sont pas comptées comme commandes exécutées.

## 5. Accès web

Outils web du codeur :0 ; taux N/A, dénominateur nul. Aucune URL visitée par ces outils. Transports locaux CAB/OpenCode et appels fournisseur autorisés comptés séparément.

## 6. Synthèse globale

| Durée de session de codage | Valeur |
| --- | --- |
| Début | 2026-10-16T05:22:31.517980+00:00 |
| Fin après archivage | 2026-10-16T06:45:00.482550+00:00 |
| Durée globale | 01 h 22 min 28 s |

| Quota Codex sur7jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant début | 2026-10-16T05:20:36.389Z | 20% | 2026-10-22T06:12:56+00:00 |
| Après archivage | 2026-10-16T06:44:58.348Z | 22% | 2026-10-22T06:12:56+00:00 |
| Différence après−avant | — | 2 points | — |

Relevés natifs codex/10080min, compte partagé : variation potentiellement due aux autres tâches, aucune attribution exclusive ni conversion tokens/euros. Empreinte privée de comparabilité seulement dans checkpoint, aucun identifiant de compte dans ce rapport.

| Domaine global | Total (part) | Réussi (taux) | Refusé (taux) | Erreur (taux) |
| --- | --- | --- | --- | --- |
| fichiers | 8 (5.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commandes | 20 (13.2 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| autres | 123 (81.5 %) | 119 (96.7 %) | 0 (0.0 %) | 4 (3.3 %) |
| Total | 151 (100.0 %) | 147 (97.4 %) | 0 (0.0 %) | 4 (2.6 %) |

89tests/8modules réussis, aucun échec/skip,3compilations0, une archive prouvée ; strict global1/quatreWARNING historiques0ERROR. Git jamais utilisé. Aucun secret source lu ; exception PLLM uniquement dans processus sécurisé, jamais valeur affichée/transmise au modèle. Publication/rapport/gate vérifiés séparément. Arrêt humain après ce change et ses statistiques, sans sélection suivante ; cycleglobal non déclaré terminé et services partagés préservés.

Preuves : /home/devops/datas/pixs/output/cismp/cismp-pixs-01a13bac8501/state.json ; frontend_manifest_facet_archive_proof, frontend_manifest_facet_postarchive_strict_proof, frontend_manifest_facet_command_results, frontend_manifest_facet_statistics_native_aggregate, frontend_manifest_facet_statistics_integrated_json, phase_statistics.add-initial-frontend-manifest-facet-v1.

Bornes distinctes : natif05:22:31–06:45:00UTC ; CAB observé06:45:54UTC depuis réservation05:20:38UTC, durées non additives. Réparation du rapport horscollecte : première copie total4erreurs changéen0, corrigée ; récupération etcommande trop longue annulée sansBash exclues des151outils. Aucunrejeuarchive ni tests.
