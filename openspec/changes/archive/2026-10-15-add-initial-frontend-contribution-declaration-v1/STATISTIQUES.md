# Statistiques — FrontendContributionDeclaration v1

RUN cismp-pixs-01a13bac8501 ; change add-initial-frontend-contribution-declaration-v1 ; contexte168 ; job cismp2-frontend-declaration-1febd06a37e3.
Session maître ses_ec039652cffeyYZ1dbejJShk0L. Collecte de la phase13:38UTC du15octobre jusqu’au relevé final après archive/reprise16octobre ; rapport exclu de cette borne.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go | high | 1.603 s | 214.471 | N/A — part native mesurable 762.89 s, orchestrateur non mesuré |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A — version exacte non exposée | OpenAI | N/A — niveau non exposé | N/A — pas de sonde orchestrateur | N/A | N/A — temps actif non exposé |

Le service natif partiel est l’union des intervalles texte/raisonnement par message. La part du temps cumulé entre agents reste N/A faute de mesure orchestrateur. Busy, attente de permission et durée calendaire ne sont pas du temps de génération.

## 1. Statistiques générales et décisions

Durée calendaire 14 h 23 min 28 s, pauses, attentes et interruption incluses.

| Résultat local | Nombre | Part |
| --- | --- | --- |
| Tests réussis | 39 | 100.0 % |
| Tests échoués | 0 | 0.0 % |
| Tests ignorés | 0 | 0.0 % |
| Total tests | 39 | 100 % |
| Compilations réussies | 3 | 100 % des compilations |

Huit modules :18 unitaires dédiés,1 intégration fraîche sous gardes avant import,20 régressions. Trois compilations natives exit0, Python3.14.8/cpython-314 ; support>=3.12 conservé et AST3.12 statique distinct des exécutions. Tests npm/UI/PostgreSQL sans objet pour le validateur Python pur. Les sources n’ont pas changé depuis ces preuves ; aucun test ou archive rejoué après interruption.

Stricts locaux change/canon puis après huit coches : exit0/issues[]. Standard global préarchive80/80,exit0. Strict préarchive80éléments/78valides ; postarchive79éléments/77valides, exit1 dans les deux cas : quatre WARNING historiques identiques, zéro ERROR. Ce résultat ne constitue pas une réussite stricte globale.

| Spécification | Niveau | Chemin | Diagnostic |
| --- | --- | --- | --- |
| bulk-operations | WARNING | requirements[10] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |
| bulk-operations | WARNING | requirements[13] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |
| bulk-operations | WARNING | requirements[6] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |
| identity-assurance | WARNING | requirements[4] | Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. |

| Décision MCP terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 30 | 100.0 % |
| Total | 30 | 100 % |

| Métrique native | Valeur |
| --- | --- |
| Messages | 354 |
| Coût déclaré OpenCode | 0.39226285399999977 |
| Tokens total | 16816231 |
| Tokens input | 3404391 |
| Tokens output | 81557 |
| Tokens reasoning | 44706 |
| Tokens cache_read | 13285577 |
| Tokens cache_write | 0 |

Tokens total/input/output/reasoning/cache conservés tels que fournis, sans addition des dimensions susceptibles de se recouvrir. Le coût natif ne prouve pas une facturation fournisseur ni une conversion en euros.

| Mesure CAB intégrée | Valeur |
| --- | --- |
| reservedMs | 50783501 |
| busyMs | 3657374 |
| idleMs | 46696153 |
| nativeUnknownMs | 429974 |
| integrationMs | 30805547 |
| queueMs | 30805568 |
| staleMs | 183590 |
| decisions | {'approved': 30, 'rejected': 0, 'needs_clarification': 0, 'pending': 0, 'once': 30, 'technicalErrors': 0} |
| httpFailures | {'native-validation-not-correlated': 25, 'evidence-references-required': 1} |

| Latence CAB | Nombre | Moyenne ms | Médiane ms | p95 ms |
| --- | --- | --- | --- | --- |
| requestToDecision | 30 | 62554.46666666667 | 50269 | 208161 |
| decisionToOnce | 30 | 15605.466666666667 | 6907 | 81781 |
| nativeTool | 174 | 11507.936781609196 | 179 | 60007 |

Source CAB intégrée et historique natif se recouvrent : aucun cumul entre les deux. Quantiles sur2048observations maximum ; durées de conditions non additives. Les tentatives HTTP échouées ne sont pas des refus natifs. Certaines anciennes décisions HTTP sont404 après maintenance ; N/A pour leur relecture actuelle, sorties MCP/SSE/effets natifs conservés, aucune autorisation consommée rejouée.

| Sonde dédiée | Position | TTMT s | Débit réponse tokens/s | Statut |
| --- | --- | --- | --- | --- |
| ses_ec03275e0ffeH6k7g0PBtCUMh9 | initiale FrontendContributionDeclarationv1 | 2.2334 | 156.226 | success |
| ses_ec00e37bcffekJaHZ5wCSgbJek | périodique30min différée qualificationSPCMP | 1.3769 | 278.217 | success |
| ses_ebff2014fffeyUZo1FNaUaiQxY | périodique30min préparationartefacts | 1.0415 | 122.795 | success |
| ses_ebfa70585ffe2maKj4tg0hBnlw | reprise après maintenanceCABC3 | 1.3671 | 167.813 | success |
| ses_ebf61e5edffeWP3sAOvIUNePkz | reprise après publicationsREF19et20 | 1.4536 | 175.067 | success |
| ses_ebf32a7ebffeGiKBdcP6jwoXNt | reprise après revue gardes intégration | 1.1004 | 158.253 | success |
| ses_ebf070d9cffeSHIzijzshoIJKQ | périodique différée avant intégration finale | 3.4797 | 268.562 | success |
| ses_ebeff9cc1ffeYLrmZTp3msmOxd | fin après archive et strict global | 1.0127 | 256.536 | success |
| ses_ebd20d98cffeP9aQRONUZp2vVW | fin après reprise et prévolCAB frais | 1.3632 | 346.766 | success |

Relèves exécutées 9, valides 9, échouées 0. Moyennes arithmétiques valides uniquement ; TTMT première partie native non vide texte/raisonnement, débit réponse seule. TTMT min/max 1.013/3.480s ; débit min/max 122.795/346.766.

probe_schedule_delays : [{"scheduled_at": "2026-10-15T14:13:30.324067+00:00", "observed_at": "2026-10-15T14:22:52.468698+00:00", "delay_seconds_at_review": 562.144638, "reason": "InventairesROetrevuequalification ; instantplanifiéN/A,pasdemesurereconstituée"}, {"scheduled_at": "2026-10-15T18:52:51.203227+00:00", "actual_at": "2026-10-15T19:10:19.241453+00:00", "reason": "Revue locale finale, compactage commun et revalidation PLLM ; aucun rattrapage reconstitué."}]

missed_probes : [{"scheduled_at": "2026-10-15T15:23:56.111094+00:00", "status": "N/A — fenêtre non mesurée", "reason": "revue/correction NFDOC et retard de pilotage avant pause", "no_reconstructed_measurement": true}, {"scheduled_at": "2026-10-15T15:53:56.111094+00:00", "status": "N/A — fenêtre non mesurée", "reason": "pause maintenance CAB humainement autorisée,aucunemesurereconstituée", "no_reconstructed_measurement": true}, {"scheduled_at": "2026-10-15T16:45:46.301931+00:00", "status": "N/A — fenêtre non mesurée", "reason": "FIFO puis exclusion C1 prioritaire ; génération de sonde concurrente interdite", "no_reconstructed_measurement": true}, {"scheduled_at": "2026-10-15T17:15:46.301931+00:00", "status": "N/A — fenêtre non mesurée", "reason": "FIFO puis exclusion C1 prioritaire ; génération de sonde concurrente interdite", "no_reconstructed_measurement": true}, {"scheduled_at": "2026-10-15T18:01:18.479347+00:00", "status": "N/A — fenêtre non mesurée", "reason": "revue/correction des gardes du NFDOC intégration ; retard de pilotage, pas de mesure reconstituée", "no_reconstructed_measurement": true}]

Surcharge sondes hors production : {"total": 114452, "input": 88614, "output": 9295, "reasoning": 4518} ; coût N/A, non enregistré. Aucun créneau manqué n’a été reconstitué. Interruption nocturne sans pilotage : relèves non exécutées, pas d’activité supposée.

PLLM de reprise 2026-10-16T03:53:09.975547+00:00 : mode1/Muse/high, Valide, TTFT28.4494s, débit global85.58. Quotas5h/hebdo/mois [0, 53, 91]%. Benchmark séparé des sondes et tests.

Compactages : historiques locaux/communs dans le checkpoint ; cycle commun15octobre19:00UTC réconcilié high/READY. API Codex non exposée : N/A pour compactage conjoint. Retards dus à interruption/récupération conservés, sans compaction fictive. Deux maintenances CAB ont été approuvées séparément ; OpenCode/broker préservés alors. Reprise16octobre : services initialement absents, récupération commune coordonnée par C1 sans purge ; OpenCode vivant1.19.2, session historique1.19.0 conservée. DEVOPS a changé extérieurement, cause non prouvée ; aucune correction C2. CLI native1.14.1 versus déclaration1.14.2 conservée.

## 2. Types de messages et d’outils

| Rôle de message | Nombre | Part |
| --- | --- | --- |
| user | 131 | 37.0 % |
| assistant | 223 | 63.0 % |
| Total | 354 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 258 | 22.7 % |
| step-start | 223 | 19.6 % |
| reasoning | 250 | 22.0 % |
| tool | 175 | 15.4 % |
| step-finish | 223 | 19.6 % |
| compaction | 6 | 0.5 % |
| Total | 1135 | 100 % |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 155 | 69.5 % |
| stop | 68 | 30.5 % |
| Total | 223 | 100 % |

| Outil | Total (part) | Réussi (taux) | Refusé (taux) | Erreur (taux) |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 20 (11.4 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 30 (17.1 %) | 24 (80.0 %) | 0 (0.0 %) | 6 (20.0 %) |
| bash | 22 (12.6 %) | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 2 (1.1 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 5 (2.9 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 (0.6 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 14 (8.0 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 66 (37.7 %) | 65 (98.5 %) | 1 (1.5 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 7 (4.0 %) | 1 (14.3 %) | 0 (0.0 %) | 6 (85.7 %) |
| write | 8 (4.6 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 175 (100 %) | 162 (92.6 %) | 1 (0.6 %) | 12 (6.9 %) |

Réussi = état natif completed ; une lecture peut être autorisée automatiquement. Cela ne prouve ni approbation manuelle ni test réussi ; les exits Bash sont vérifiés séparément. Refusé exige un diagnostic natif explicite de permission. Timeout MCP et interruption sont des erreurs techniques.

## 3. Fichiers modifiés

| Chemin absolu complet — tentatives | Total (part) | Réussi (taux) | Refusé (taux) | Erreur (taux) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-declaration-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-declaration-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-declaration-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-declaration-v1/specs/frontend/spec.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/frontend_contribution_declarations.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_frontend_contribution_declaration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_frontend_contribution_declaration_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 (100 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Les effectifs représentent des tentatives, pas des fichiers uniques. Les commandes CLI new/py_compile/archive ont leurs effets propres approuvés. Le checkpoint et les caches régénérables ne sont pas des sources fonctionnelles.

| Source exacte | SHA256 |
| --- | --- |
| /home/devops/datas/pixs/src/pixs/kernel/frontend_contribution_declarations.py | db36d79a14da543250741947801f15a7625e8f924588416614b9c41b33642567 |
| /home/devops/datas/pixs/tests/unit/test_frontend_contribution_declaration.py | 93bfb59f37ddda1fbc406f12e3904fa7f32759ea33f146fbda03e7d3ceb7cb1b |
| /home/devops/datas/pixs/tests/integration/test_frontend_contribution_declaration_integration.py | f06cea67b297ce9986cfec80bb424caeb9c8547c76256f479eb6359c7022ad83 |

Archive unique /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-frontend-contribution-declaration-v1 : cinq artefacts déplacés à octets identiques, --skip-specs/specsUpdated=false, canon et trois sources préservés. STATISTIQUES.md est un mandat distinct hors borne ; aucune réarchive.

## 4. Commandes

| Famille de commande | Nombre | Part |
| --- | --- | --- |
| Prévol | 4 | 18.2 % |
| OpenSpec | 11 | 50.0 % |
| Autre | 1 | 4.5 % |
| Compilation Python | 3 | 13.6 % |
| Tests Python | 3 | 13.6 % |
| Total | 22 | 100 % |

| Commande (100 caractères max) | État | Exit natif | Occurrences | Part |
| --- | --- | --- | --- | --- |
| /usr/bin/true | réussi | 0 | 4 | 18.2 % |
| /home/devops/.local/npm/bin/openspec --version | réussi | 0 | 1 | 4.5 % |
| /home/devops/.local/npm/bin/openspec new change add-initial-frontend-contribution-declaration-v1 | réussi | 0 | 1 | 4.5 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-frontend-contribution-declaration-v1 --ty… | réussi | 0 | 3 | 13.6 % |
| /home/devops/.local/npm/bin/openspec validate frontend --type spec --strict --json | réussi | 0 | 2 | 9.1 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'print(__import__("sys").version.split()[0],__impor… | réussi | 0 | 1 | 4.5 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile sr… | réussi | 0 | 1 | 4.5 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile te… | réussi | 0 | 1 | 4.5 % |
| PYTHONPATH=src PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -… | réussi | 0 | 1 | 4.5 % |
| PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile te… | réussi | 0 | 1 | 4.5 % |
| PYTHONPATH=src PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -… | réussi | 0 | 1 | 4.5 % |
| PYTHONPATH=src PYTHONPYCACHEPREFIX= PYTHONOPTIMIZE=0 /home/devops/datas/pixs/.venv/bin/python3 -B -… | réussi | 0 | 1 | 4.5 % |
| /home/devops/.local/npm/bin/openspec validate --all --json | réussi | 0 | 1 | 4.5 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | réussi | 1 | 2 | 9.1 % |
| /home/devops/.local/npm/bin/openspec archive add-initial-frontend-contribution-declaration-v1 --yes… | réussi | 0 | 1 | 4.5 % |

Commandes refusées :0,0.0% des commandes. Les exits1 stricts sont des résultats de validation, pas des refus de permission.

Commandes complètes/corrélations/exits conservés dans frontend_decl_command_results et historique natif ; prévol de reprise distinct des tests métier.

## 5. Accès web

Outils web du codeur :0 ; parts et taux N/A, dénominateur nul. Aucune URL visitée par ces outils. Transports locaux CAB/OpenCode et appels fournisseur autorisés sont séparés.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-15T13:38:29.177412+00:00 |
| Fin — après archivage et reprise | 2026-10-16T04:01:57.521Z |
| Durée globale (pauses et attentes incluses) | 14 h 23 min 28 s |

| Mesure du quota Codex sur7jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-15T13:38:53.207Z | 10% | 2026-10-22T06:12:56+00:00 |
| Après — après archivage | 2026-10-16T04:01:57.521Z | 18% | 2026-10-22T06:12:56+00:00 |
| Différence après−avant | — | 8 points | — |

Relevés natifs get_usage_limits du quota codex/10080minutes. Le compte est partagé : variation potentiellement due à d’autres tâches, sans ventilation exclusive ni conversion en tokens/euros. Relevé final avant interruption non persisté : N/A pour cette ancienne borne ; relevé réel de reprise conservé.

| Domaine global | Total (part) | Réussi (taux) | Refusé (taux) | Erreur (taux) |
| --- | --- | --- | --- | --- |
| fichiers | 8 (4.6 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commandes | 22 (12.6 %) | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| autres | 145 (82.9 %) | 132 (91.0 %) | 1 (0.7 %) | 12 (8.3 %) |
| Total | 175 (100 %) | 162 (92.6 %) | 1 (0.6 %) | 12 (6.9 %) |

39tests/8modules réussis sans skip,3compilations exit0, une archive prouvée ; strict global exit1/quatre warnings historiques. Huit tâches cochées sur preuves. Git jamais utilisé. Aucun secret lu dans les sources projet ; exception PLLM limitée au processus sécurisé, sans valeur affichée, journalisée ou envoyée au modèle. Publication et clôture du rapport sont vérifiées séparément par l’orchestrateur ; le présent rapport ne signifie pas la fin du cycle parent.

Preuves : /home/devops/datas/pixs/output/cismp/cismp-pixs-01a13bac8501/state.json ; frontend_decl_archive_proof, frontend_decl_postarchive_strict_proof, frontend_decl_command_results, frontend_decl_statistics_native_aggregate, frontend_decl_statistics_integrated_json, phase_statistics.add-initial-frontend-contribution-declaration-v1.
