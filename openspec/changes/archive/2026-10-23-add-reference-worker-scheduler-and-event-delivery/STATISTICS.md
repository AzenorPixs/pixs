# STATISTIQUES — C09 : worker, scheduler et livraison locale

Change : add-reference-worker-scheduler-and-event-delivery. Archive : openspec/changes/archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery.

RUN : cismp2-pixs-432a76eb96094b9e ; contexte CAB 602. Sessions de production : ses_e9b082829ffej0Anyh8XJrFuyU, ses_e9a270b97ffeeY1eV9tPKT6aWk.

Intervalle figé : 2026-10-22T20:57:43+02:00 à 2026-10-23T06:11:51+02:00. La rédaction du rapport, ses vérifications, la coche finale, la publication et la clôture ultérieures sont exclues des métriques ci-dessous. Aucun autre RUN n’est attribué à cette livraison.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|

| muse-spark-1.3-contributor | N/A : version exacte non exposée | OpenCode Go | high | 3.029 s | 307.65 | N/A : durée active de génération non isolable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|

| Codex / GPT-6 | N/A : identité exacte non exposée | OpenAI | N/A : métadonnée non exposée | N/A : orchestrateur non sondé | N/A : orchestrateur non sondé | N/A : télémétrie active indisponible |

Les taux de service ne sont pas calculés : le dénominateur de temps actif cumulé n’est pas observable pour les deux agents. Les durées de réponse ou busy, attentes, outils et chevauchements ne sont pas assimilés à du temps de génération. Aucun sous-agent Codex n’a été créé. La récupération contrôlée a remplacé la session de codage dans le même RUN ; la session révoquée est conservée dans l’attribution historique.

## 1. Statistiques générales et décisions

Durée calendaire : 09 h 14 min 07 s, pauses, attentes et tests compris. 1703 messages natifs et 1040 appels d’outils de production sont observés dans l’intervalle. Les métriques d’outils/messages de l’orchestrateur principal sont N/A : aucun export natif exhaustif disponible ; elles ne sont pas estimées.

Convention : un outil natif completed est compté réussi et autorisé, automatiquement ou par décision. Ce statut ne prouve ni approbation humaine ni réussite fonctionnelle d’un test (un Bash completed peut retourner exit 1). Un refus exige une preuve explicite de permission refusée ; les timeouts MCP, interruptions sans refus et échecs techniques sont séparés. Les décisions CAB et les once ne sont pas additionnées aux outils natifs.

| Décisions CAB — contexte entier | Nombre | Part |
|---|---:|---:|
| approved | 138 | 100.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| rejected | 0 | 0.0 % |
| **Total** | **138** | **100.0 %** |

Permissions once émises : 138 ; erreurs techniques du suivi de décision : 0. Populations séparées, non additionnées aux décisions.

Les compteurs CAB couvrent tout le contexte 602, initialisation incluse ; ils ont leur propre dénominateur. Le détail natif est filtré sur les bornes ci-dessus : 11 messages antérieurs et 1 postérieurs exclus. Les agrégats historiques globaux des autres RUN ne sont pas utilisés.

| Tokens de production déclarés par OpenCode | Nombre | Part |
|---|---:|---:|
| cache_read | 343473078 | 97.1 % |
| cache_write | 0 | 0.0 % |
| input | 9659761 | 2.7 % |
| output | 616501 | 0.2 % |
| reasoning | 148363 | 0.0 % |
| **Total** | **353897703** | **100.0 %** |

Coût déclaré par la télémétrie OpenCode : 1.805895 USD ; aucune facture ni coût réel du forfait OpenCode Go déduit. Les catégories input/output/reasoning/cache sont affichées telles que la source les fournit ; aucune conversion du quota Codex en tokens ou coût.

Compactages natifs marqués summary dans cet intervalle : 7. Identifiants : msg_1654a90e60014cjxsJdaY6Ah6d, msg_1659d49da001DAD5q3FEvGMMeq, msg_165f61979001hHjkbHXnbvBaFF, msg_166494fc90012bkBQ375B2O0Y3, msg_16699ea04001FL2kQF4MZaGdvF, msg_166c01c37001y49Lcrz0PcKF49, msg_166e731480011HYTFMT3kQMnkx. API native de compactage Codex non exposée : N/A, aucune réussite conjointe inventée.

Développement : 45 compilations, 946 unités applicables réussies dans 71 modules, dont 120 unités C09 ; 15 recettes PostgreSQL/222 cas distincts réussis et six recettes/76 cas de consolidation réexécutés. Ne pas additionner 120 à 946, ni 76 à 222 comme des cas distincts. PostgreSQL 16.14, Django 6.1.2, Python 3.14.9 réellement observés. Strict C09 réussi et archive CLI exit 0, sans synchronisation de canon.

Le lancement initial élargi (920 tests, quatre échecs et trois erreurs) est conservé : chemins src/tests/unit corrigés dans la commande ; assertion historique Core vide explicitement non applicable au Core C06 actuel. Les cinq capacités, quinze contrats et vingt entrées sont vérifiés par la suite Core actuelle incluse dans les 946 unités. Ce test historique n’est pas déclaré réussi et ses sources restent préservées.

Sondes de performance du codeur uniquement : prompt déterministe constant de 64 lignes, même fournisseur/modèle/high, sessions dédiées sans outils ni fichiers/réseau métier. Le transport vers le fournisseur est nécessaire à la sonde ; aucune navigation ni tâche métier n’est injectée.

| Tentatives de sonde | Nombre | Part |
|---|---:|---:|
| invalides_ou_echouees | 0 | 0.0 % |
| valides | 20 | 100.0 % |
| **Total** | **20** | **100.0 %** |

Cadence : 20 relèves prévues (une initiale, une toutes les 30 minutes puis une finale) ; 2 échéances manquées explicitement enregistrées, jamais reconstruites. Les tentatives et échéances sont deux populations distinctes.

| Mesure valide | Moyenne arithmétique | Minimum | Maximum |
|---|---:|---:|---:|

| TTMT | 3.029 s | 1.308 s | 11.720 s |
| Tokens/s | 307.65 | 135.73 | 762.08 |

| Position | Horodatage | Statut | TTMT (s) | Tokens/s | Tokens sortie |
|---|---|---|---:|---:|---:|

| début | 2026-10-22T18:59:07.443098+00:00 | VALID | 1.308 | 656.970 | 584 |

| +30 min | 2026-10-22T19:28:10.095345+00:00 | VALID | 3.334 | 135.735 | 596 |

| intermédiaire après échéance +60 min manquée | 2026-10-22T20:01:37.991723+00:00 | VALID | 3.310 | 228.552 | 584 |

| périodique observée | 2026-10-22T20:36:07.335625+00:00 | VALID | 1.492 | 762.076 | 585 |

| périodique observée | 2026-10-22T20:57:45.294817+00:00 | VALID | 3.098 | 169.032 | 598 |

| périodique observée | 2026-10-22T21:27:44.382265+00:00 | VALID | 1.950 | 219.562 | 584 |

| périodique observée | 2026-10-22T21:57:43.945361+00:00 | VALID | 2.059 | 251.749 | 585 |

| périodique observée | 2026-10-22T22:27:44.516037+00:00 | VALID | 1.736 | 264.622 | 584 |

| périodique observée | 2026-10-22T22:57:45.032996+00:00 | VALID | 3.389 | 197.355 | 594 |

| périodique observée | 2026-10-22T23:27:45.837864+00:00 | VALID | 2.068 | 248.472 | 584 |

| périodique observée | 2026-10-22T23:57:44.369461+00:00 | VALID | 4.457 | 228.142 | 584 |

| périodique observée | 2026-10-23T00:27:46.188011+00:00 | VALID | 2.293 | 284.553 | 584 |

| périodique observée | 2026-10-23T00:57:44.877414+00:00 | VALID | 11.720 | 255.807 | 593 |

| périodique observée | 2026-10-23T01:27:46.707314+00:00 | VALID | 2.575 | 215.311 | 600 |

| périodique observée | 2026-10-23T01:57:46.327877+00:00 | VALID | 2.942 | 282.474 | 584 |

| périodique observée | 2026-10-23T02:27:45.954640+00:00 | VALID | 3.885 | 223.856 | 600 |

| périodique observée | 2026-10-23T02:57:46.075739+00:00 | VALID | 1.619 | 752.441 | 585 |

| périodique observée | 2026-10-23T03:27:45.682467+00:00 | VALID | 2.613 | 285.529 | 584 |

| périodique observée | 2026-10-23T03:57:45.820966+00:00 | VALID | 2.507 | 231.643 | 593 |

| fin | 2026-10-23T04:11:01.102981+00:00 | VALID | 2.218 | 259.187 | 584 |

Échéance manquée : 2026-10-22T19:57:43.661649+00:00 ; Échéance +60 min dépassée pendant revue ; sonde supplémentaire actuelle, sans reconstruction rétroactive.

Échéance manquée : 2026-10-22T20:27:43.661649+00:00 ; Échéance dépassée ; sonde supplémentaire réelle, aucune reconstruction.

Surcharge des sondes, séparée de la production : 11769 tokens de sortie, 0.028661 USD déclarés ; durée calendaire cumulée des réponses de sonde 107.407 s (latence incluse, pas un temps de service du modèle). Les sessions de sonde sont archivées nativement. Version exacte du modèle N/A.

## 2. Types de messages et d’outils

| Rôle des messages | Nombre | Part |
|---|---:|---:|
| assistant | 1192 | 70.0 % |
| user | 511 | 30.0 % |
| **Total** | **1703** | **100.0 %** |

| Type de partie native | Nombre | Part |
|---|---:|---:|
| compaction | 7 | 0.1 % |
| reasoning | 1288 | 22.3 % |
| step-finish | 1190 | 20.6 % |
| step-start | 1192 | 20.6 % |
| text | 1067 | 18.4 % |
| tool | 1040 | 18.0 % |
| **Total** | **5784** | **100.0 %** |

| Terminaison des réponses assistant | Nombre | Part |
|---|---:|---:|
| incomplète | 2 | 0.2 % |
| stop | 331 | 27.8 % |
| tool-calls | 859 | 72.1 % |
| **Total** | **1192** | **100.0 %** |

| Outil natif | Total | Part | Réussis / approuvés | Taux | Refusés | Taux | Erreurs techniques | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bash | 109 | 10.5 % | 108 | 99.1 % | 1 | 0.9 % | 0 | 0.0 % |
| cgpt-validation_broker_health | 74 | 7.1 % | 74 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 146 | 14.0 % | 146 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 31 | 3.0 % | 31 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 118 | 11.3 % | 118 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 19 | 1.8 % | 11 | 57.9 % | 0 | 0.0 % | 8 | 42.1 % |
| cgpt-validation_request_validation | 137 | 13.2 % | 120 | 87.6 % | 0 | 0.0 % | 17 | 12.4 % |
| edit | 7 | 0.7 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 141 | 13.6 % | 141 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 42 | 4.0 % | 42 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 189 | 18.2 % | 186 | 98.4 % | 0 | 0.0 % | 3 | 1.6 % |
| todowrite | 5 | 0.5 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 22 | 2.1 % | 22 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| **Total** | **1040** | **100.0 %** | **1011** | **97.2 %** | **1** | **0.1 %** | **28** | **2.7 %** |

Les décisions sont présentées au §1. Les 1 185 réponses de production renseignent high ; les sept résumés natifs ne renseignent pas variant et ne sont pas artificiellement attribués à un niveau de raisonnement. Les outils CAB MCP comprennent les consultations et demandes d’approbation ; une erreur de timeout MCP n’est pas un refus de permission. Aucun temps ou gain causal de codage n’est déduit de ces effectifs.

## 3. Fichiers modifiés

Chaque ligne compte des tentatives d’écriture sur une cible, pas des fichiers distincts ni des lignes modifiées. Les écritures write/edit natives et les transports Python unitaires épinglés par SHA sont classés ici ; ces derniers restent Bash dans le tableau des types natifs, mais ne sont pas recomptés dans le domaine Commandes. Les lectures seules restent dans Autres outils.

| Chemin absolu complet | Total | Part | Réussis / approuvés | Taux | Refusés | Taux | Erreurs techniques | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-reference-worker-scheduler-and-event-delivery/design.md | 3 | 3.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-reference-worker-scheduler-and-event-delivery/requirements.md | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-reference-worker-scheduler-and-event-delivery/tasks.md | 9 | 11.2 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery/design.md | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery/requirements.md | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery/tasks.md | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_authorization_adapter.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_contracts.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_dispatch.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_entry.py | 3 | 3.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_event_records.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_event_values.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_inbox_repository.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_job_records.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_job_repository.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_outbox_repository.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_registry.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_runtime_plan.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_runtime_repository.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_scheduler.py | 3 | 3.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/c09_worker.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0012_c09_jobs.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0013_c09_events_scheduler.py | 3 | 3.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/c09_outbox_participant.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/c09_owner_participant.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/c09_core_fixture.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/c09_entry_fixture.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/c09_event_fixture.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/c09_pg_delivery_support.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/c09_pg_process_support.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/c09_pg_test_support.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_core_inbox_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_core_job_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_dispatch_postgres.py | 3 | 3.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_entry_process_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_entry_signals_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_entry_web_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_inbox_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_migration_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_outbox_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_runtime_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_scheduler_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_scheduler_resilience_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_worker_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_worker_resilience_postgres.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_c09_worker_superadmin_postgres.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_c09_contracts.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_c09_events_scheduler.py | 2 | 2.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_c09_runtime_plan.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_c09_worker.py | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| **Total** | **80** | **100.0 %** | **80** | **100.0 %** | **0** | **0.0 %** | **0** | **0.0 %** |

51 chemins d’écriture distincts observés avant la borne finale. Le déplacement unique de openspec/changes/add-reference-worker-scheduler-and-event-delivery vers openspec/changes/archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery est une commande d’archivage distincte ; les deux chemins historiques d’un même document peuvent apparaître. Les cinq fichiers ont été conservés bit à bit par le déplacement, puis seuls les chemins relatifs des liens ont été ajustés (12 design, 26 requirements, deux tasks), mêmes cibles et ancres. Les caches régénérables et schémas PG jetables ne sont pas des sources livrées.

L’écriture de ce STATISTIQUES.md et la coche finale de 3.4 sont postérieures à la borne de collecte : elles sont exclues des tentatives chiffrées de ce rapport. Leurs preuves natives sont conservées au checkpoint de clôture. Aucun Git inspecté pour établir ce manifeste.

## 4. Commandes

| Famille de commandes | Total | Part | Réussis / approuvés | Taux | Refusés | Taux | Erreurs techniques | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| /usr/bin/true | 6 | 10.3 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Git non exécuté | 1 | 1.7 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| OpenSpec | 3 | 5.2 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src | 5 | 8.6 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests/integration | 7 | 12.1 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/c09-cache | 12 | 20.7 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPYCACHEPREFIX=tests/runtime/c09-cache | 1 | 1.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python | 23 | 39.7 % | 23 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| **Total** | **58** | **100.0 %** | **57** | **98.3 %** | **1** | **1.7 %** | **0** | **0.0 %** |

Commandes refusées regroupées — libellés limités à 100 caractères :

| Commande demandée, non exécutée | Nombre | Part |
|---|---:|---:|
| git status --porcelain=v1 --untracked-files=no; printf '\n---DIFF-STAT---\n'; git diff --stat; prin… | 1 | 100.0 % |
| **Total** | **1** | **100.0 %** |

La tentative Git issue d’une relance automatique du superviseur est restée en attente de permission native : abort, rejet ciblé, aucun once ni exécution, puis prévol /usr/bin/true frais réussi. Le refus est conservé comme tel ; aucune sortie Git n’a été produite ou exploitée. Les retours de tests et erreurs SQL de préparation ne sont pas classés comme refus d’autorisation.

## 5. Accès web

| URL / requête | Total | Part | Réussis / approuvés | Taux | Refusés | Taux | Erreurs techniques | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Aucun accès web natif observé | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| **Total** | **0** | **N/A** | **0** | **N/A** | **0** | **N/A** | **0** | **N/A** |

Aucune URL approuvée ou refusée de navigation web dans les outils natifs attribués ; aucune visite n’est déduite d’une simple requête. Les appels locaux de pilotage OpenCode/CAB et le transport des modèles ne sont pas des visites web métier. Les quotas fournisseurs sont interrogés localement via le mécanisme privé autorisé, sans exposer de clé. Les statistiques exhaustives d’accès réseau de l’orchestrateur sont N/A : aucune trace réseau complète disponible. Aucune absence globale de trafic n’est déduite de ce tableau.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|

| Début | 2026-10-22T20:57:43+02:00 |
| Fin — après archivage | 2026-10-23T06:11:51+02:00 |
| Durée globale (pauses et attentes incluses) | 09 h 14 min 07 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|

| Avant — début de session | 2026-10-22T20:57:43+02:00 | 2 % | 2026-10-29T18:09:38+01:00 |
| Après — après archivage de la spécification | 2026-10-23T06:11:51+02:00 | 100 % | 2026-10-29T18:09:39+01:00 |

| Différence après − avant | — | N/A — fenêtre/réinitialisation/comparaison divergente | — |

Relevés natifs mcp__codex_app__get_usage_limits, quota codex/fenêtre 10080 minutes. Le compte et son quota sont partagés : cette variation inclut potentiellement d’autres tâches simultanées et n’est pas attribuée exclusivement à C09. Aucun secret n’est lu pour ces relevés. La consommation ultérieure de rédaction du rapport est exclue. Même compte confirmé ; resetsAt diffère d’une seconde entre les deux relevés. La différence reste N/A conformément à la règle de comparaison, sans supposer un reset ni reconstruire une consommation.

| Domaine — production native | Total | Part | Réussis / approuvés | Taux | Refusés | Taux | Erreurs techniques | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Autres outils | 902 | 86.7 % | 874 | 96.9 % | 0 | 0.0 % | 28 | 3.1 % |
| Commandes | 58 | 5.6 % | 57 | 98.3 % | 1 | 1.7 % | 0 | 0.0 % |
| Fichiers | 80 | 7.7 % | 80 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| **Total** | **1040** | **100.0 %** | **1011** | **97.2 %** | **1** | **0.1 %** | **28** | **2.7 %** |

Vérification des totaux : somme par type natif = somme par domaine = 1040. Les fichiers et commandes sont attribués une seule fois. Effectifs et pourcentages sont conservés ; N/A si dénominateur nul.

Coordination CAB 1.7.1 (contexte602, depuis 2026-10-22T20:56:05+02:00) : attente ressources 358377 ms ; détention partagée 12143905 ms ; suivi des effets émis 286299 ms ; réconciliations 0. Ces durées peuvent se recouvrir et ne sont pas additionnées. Aucun gel global demandé par ce RUN. Busy ne prouve pas une activité productive.

Les tentatives HTTP du contrôleur sont distinctes des refus de permission : {"native-session-not-quiescent": 2, "native-validation-not-correlated": 48, "evidence-references-required": 1, "run-accesses-unresolved": 1, "decision-run-divergent": 1}. Les gaps d’observation SSE de l’orchestrateur ne sont pas reconstruits ; l’historique HTTP natif et les audits CAB fournissent les résultats corrélés disponibles. Exhaustivité des événements manquants : N/A. Statistiques globales des autres RUN exclues.

Livraison : worker, scheduler lease/fencing, outbox/inbox et entrées bornées C09 éprouvés localement, canons inchangés, archive unique réussie. Migrations appliquées/rejouées/retournées sur schémas vides jetables ; retour sur données non vides refusé sans perte. Aucun déploiement de base de production. C03/N05/observations PBO et certains adaptateurs restent des doubles nommés ; modes PA/PZT distants, dimensionnement physique et distribution C17/C18/C19 non qualifiés. Aucun P0 complet annoncé. Frontend inchangé, npm/navigateurs sans objet ; lint/types non configurés.

À la borne de ce rapport, la vérification de son contenu, la coche3.4, la publication et le gate sont encore des étapes de clôture ; leur réussite sera prouvée au checkpoint, jamais déduite de la présence du rapport. Git non exécuté, aucun secret ajouté ou exposé observé, aucun accès externe métier ni nouvelle dépendance, aucun arrêt d’OpenCode/CAB/services partagés. Arrêt demandé après ce seul change ; cycle Pixs global non déclaré achevé.
