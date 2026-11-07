# STATISTICS.md — add-installation-and-first-configuration

Statut : change ouvert — dépendances manquantes — archivage en attente. Voir [Bilan des blocages](BLOCKERS.md). Borne : 2026-10-30T06:32:00.858Z. Texte final de collecte ; vérification et livraison au checkpoint /home/devops/datas/pixs/output/cismp/cismp1-pixs-02716fc18b3546c0/state.json. Clôture et gate en attente à la borne, sans acquis futur.

Périmètre : tout le change depuis création 2026-10-17 (jour seul, heure initiale N/A). Lacune 17-21 octobre : aucune activité attribuable, N/A, corpus global non exhaustif sur cette période. Production depuis le 22/10 dédupliquée, tous contextes ; sessions dédupliquées : 8. Premier natif 2026-10-22T03:21:59.211Z.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A (version non exposée) | opencode-go | high | 2.7 | 430.5 | N/A (temps de service non estimé) |
| muse-spark-1.3-contributor | N/A (version non exposée) | opencode-go | medium | 2.4 | 901.4 | N/A (temps de service non estimé) |

Sondes strictes retenues : 51 sur 96 (fournisseur, modèle, raisonnement connus, text_bounds, validité !== false, TTMT et débit finis strictement positifs ; autres exclues N/A, sans conversion des absences en 0). Aucune rétrosonde ajoutée.

Détail strict par config (sans valeur inférée) :

| config | n valides | min TTMT | max TTMT | min débit | max débit |
|---|---|---|---|---|---|
| opencode-go/muse-spark-1.3-contributor/high | 49 | 1.7 | 6.4 | 70.1 | 8570.6 |
| opencode-go/muse-spark-1.3-contributor/medium | 2 | 1.6 | 3.1 | 197.9 | 1604.9 |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A (compteurs non exposés) | N/A | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

Tokens, cache et coûts par config native (tokens absents N/A, coût sans devise ni facturation inventée) :

| config | messages | input | output | reasoning | cache_read | cache_write | coût |
|---|---|---:|---:|---:|---:|---:|---|
| opencode-go/muse-spark-1.3-contributor/high | 6189 | 62441396 | 2197376 | 1098371 | 2270801408 | 0 | 11.444891815999977 |
| opencode-go/muse-spark-1.3-contributor/medium | 67 | 4206341 | 44612 | 15660 | 34479341 | 0 | 0 |
| total | 6256 | 66647737 | 2241988 | 1114031 | 2305280749 | 0 | 11.444891815999977 |

Décisions natives historiques OBSERVÉES (dernières réponses, un PENDING historique ne prouve pas une attente actuelle ; état courant dans current_proofs, compteurs CAB non additionnés au natif) :

| statut | effectif | part |
|---|---:|---|
| APPROVED | 361 | 92.6% |
| PENDING | 8 | 2.1% |
| REJECTED | 16 | 4.1% |
| UNKNOWN | 5 | 1.3% |
| total | 390 | 100.0% |

Décisions CAB par contexte (distinctes, non additionnées) :

| contextId | état | approuvées / rejetées / clarification / en attente | sessions |
|---|---|---|---|
| 1370 | RESERVED | 5 / 1 / 0 / 0 | ses_e874794edffeIyYWDpUCIAN2MG |
| 592 | ABANDONED | 209 / 9 / 0 / 0 | ses_e9e5f0de2ffeiVX4NJuQJfjP9n |
| 1147 | ABANDONED | 143 / 5 / 0 / 0 | ses_e9e5f0de2ffeiVX4NJuQJfjP9n, ses_e920c15b3ffe3gHhY7ZpCHu14o, ses_e91cd3c92ffekDV8jpJsGxH9O7, ses_e90f4d2ffffe5JtAqkUyZmJPfq, ses_e89a31cbbffeDj0b1KHMdw4RSN, ses_e879e0308ffeXiApWelZVKR55z |
| 1286 | ABANDONED | 4 / 0 / 0 / 0 | ses_e874f068cffeuLKwCWgowx3mi7, ses_e874794edffeIyYWDpUCIAN2MG |

Historique vérifié : contrôlées 6 sur 17, ouvertes 11, 232 PASS / 0 FAIL / 15 suites historiques non rejoués (sous-ensemble connu, pas exhaustif depuis le 17). Réconciliation courante : Rejet explicite de la demande interrompue, lookup natif REJECTED, READY propre0 puis nouveau prévol2.1.15 avec once et exit0, accès relâché.. Rapports déjà enregistrés distingués des opérations finales pas encore réalisées.

## 2. Types de messages et d'outils

| rôle | effectif | part de 9276 |
|---|---:|---|
| user | 3020 | 32.6% |
| assistant | 6256 | 67.4% |
| total | 9276 | 100.0% |

| partie | effectif | part de 18949 |
|---|---:|---|
| reasoning | 7141 | 37.7% |
| text | 7054 | 37.2% |
| tool | 4754 | 25.1% |
| total | 18949 | 100.0% |

| fin | effectif | part de assistant (6256) |
|---|---|---|
| length | 1 | 0.0% |
| stop | 2427 | 38.8% |
| tool-calls | 3813 | 60.9% |
| non exposés (assistant moins somme connue, pas succès) | 15 | 0.2% |
| total | 6256 | 100.0% |

Outils (completed = fin de transport, pas succès de test ; tout taux sur dénominateur 0 vaut N/A motivé) :

| outil | completed | error | refused | running | total | part globale | taux completed | taux error | taux refused |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| bash | 301 | 1 | 3 | 0 | 305 | 6.4% | 98.7% | 0.3% | 1.0% |
| cab_codemode_discovery | 2 | 0 | 0 | 0 | 2 | 0.0% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_broker_auto_remediation_policy | 1 | 0 | 0 | 0 | 1 | 0.0% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_broker_health | 669 | 0 | 0 | 0 | 669 | 14.1% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_broker_readiness | 1188 | 1 | 0 | 0 | 1189 | 25.0% | 99.9% | 0.1% | 0.0% |
| cgpt-validation_broker_remediation_registry | 5 | 0 | 0 | 0 | 5 | 0.1% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_cancel_approval | 7 | 0 | 0 | 0 | 7 | 0.1% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_get_approval | 17 | 1 | 0 | 0 | 18 | 0.4% | 94.4% | 5.6% | 0.0% |
| cgpt-validation_list_pending | 826 | 0 | 0 | 0 | 826 | 17.4% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_poll_approval | 104 | 18 | 0 | 0 | 122 | 2.6% | 85.2% | 14.8% | 0.0% |
| cgpt-validation_reject | 1 | 0 | 0 | 0 | 1 | 0.0% | 100.0% | 0.0% | 0.0% |
| cgpt-validation_request_validation | 357 | 33 | 0 | 0 | 390 | 8.2% | 91.5% | 8.5% | 0.0% |
| edit | 33 | 0 | 0 | 0 | 33 | 0.7% | 100.0% | 0.0% | 0.0% |
| glob | 74 | 1 | 0 | 0 | 75 | 1.6% | 98.7% | 1.3% | 0.0% |
| grep | 124 | 1 | 1 | 0 | 126 | 2.7% | 98.4% | 0.8% | 0.8% |
| read | 936 | 7 | 1 | 0 | 944 | 19.9% | 99.2% | 0.7% | 0.1% |
| todowrite | 20 | 0 | 0 | 0 | 20 | 0.4% | 100.0% | 0.0% | 0.0% |
| write | 21 | 0 | 0 | 0 | 21 | 0.4% | 100.0% | 0.0% | 0.0% |
| total | 4686 | 63 | 5 | 0 | 4754 | 100.0% | 98.6% | 1.3% | 0.1% |

## 3. Fichiers modifiés

Union triée ABS complète sans troncature : natif 54 + Bash ciblé 178 = 232 lignes ; 94 distinctes par union dédupliquée (Union dedupliquee par appel natif et chemin : cibles fichier declarees en ecriture dans le manifeste CAB de la commande EXACTE precedente, completees par analyse AST litterale sans execution. Ce sont des tentatives ciblees ; resultat de commande distinct de preuve native fichier. Cibles dynamiques ou repertoires non determines restent N/A. Ne pas ajouter ces cibles aux commandes comme outils supplementaires.). Cibles Bash = manifestes CAB declared WRITE pour commande exacte + compléments AST littéraux, jamais outils en plus ni effets déduits. Sans archive ni renommage actuel.

| chemin ABS | natif C | natif E | natif R | natif Ru | bash C | bash E | bash R | bash Ru | total | part | taux C | taux E | taux R |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| /home/devops/datas/pixs/BUILD.md | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/.openspec.yaml | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 4 | 1.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/BLOCKERS.md | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/VALIDATION.md | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/design.md | 6 | 0 | 0 | 0 | 39 | 0 | 1 | 0 | 46 | 19.8% | 97.8% | 0.0% | 2.2% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/projection-contract.md | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 4 | 1.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/proposal.md | 4 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 11 | 4.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/requirements.md | 4 | 0 | 0 | 0 | 11 | 0 | 0 | 0 | 15 | 6.5% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/authorization/spec.md | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 5 | 2.2% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/docker-image/spec.md | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 4 | 1.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/initial-administration/spec.md | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/installation-provisioning/spec.md | 4 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 6 | 2.6% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/pixs-agent/spec.md | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 5 | 2.2% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/pzt/spec.md | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 5 | 2.2% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/reference-composition/spec.md | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/specs/secrets-providers/spec.md | 1 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 5 | 2.2% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/changes/add-installation-and-first-configuration/tasks.md | 6 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 15 | 6.5% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/specs/authorization/spec.md | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/specs/docker-image/spec.md | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/specs/installation-provisioning/spec.md | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/specs/pixs-agent/spec.md | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/specs/pzt/spec.md | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/openspec/specs/secrets-providers/spec.md | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 3 | 1.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_backend.py | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_file_sources.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_metadata.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_publication.py | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 | 1.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_session.py | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_tty.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/apps.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c08_act_receipt_record.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c08_installation_result_record.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c08_mode_operation_receipt_record.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c08_mode_snapshot_record.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c10_catalog.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c10_governance_adapter.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/c10_receipt_record.py | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/__init__.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/act_content.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/act_idempotence.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/auth_classification.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/auth_creation_bridge.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/auth_plan_binding.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/checkpoint.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/checkpoint_binding.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/marker.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_commands.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_governance.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_participant.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_reader.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_service.py | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_transition_factory.py | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/mode_values.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/plan.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/plan_source.py | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 | 1.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/result_reader.py | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/result_writer.py | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 | 1.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/reuse_result.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/storage.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/installation/technical_projection.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0014_c10_initial_governance_receipts.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0015_c08_installation_result.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0016_c08_mode_storage.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0017_c08_act_receipt.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 4 | 1.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/core/audit_sink.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/core/services_common.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/core/services_mode_transition.py | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/src/pixs/core/services_transactions.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/auth_bootstrap_builders.py | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/auth_bootstrap_publication_fixture.py | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/c08_modes_fixture.py | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 4 | 1.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/c08_modes_pg_harness.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/c08_modes_process_worker.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/c08_modes_worker.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_auth_bootstrap_publication_postgres.py | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 0.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_c05_public_receipt_postgres.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_c08_mode_storage_inputs_postgres.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_c08_mode_storage_postgres.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_c08_modes_pg.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_c08_modes_processes_pg.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_c08_modes_public_boundary_pg.py | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/integration/test_initial_governance_postgres.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_c08_mode_commands.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_c08_mode_values.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_c08_technical_projection.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_c10_catalog_files.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_installation_act_content.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_installation_checkpoint.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_installation_checkpoint_binding.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_installation_marker.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_installation_plan.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/tests/unit/test_installation_plan_storage.py | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0.4% | 100.0% | 0.0% | 0.0% |
| total | 54 | 0 | 0 | 0 | 177 | 0 | 1 | 0 | 232 | 100.0% | 99.6% | 0.0% | 0.4% |

## 4. Commandes

| famille lexicale | effectif | part de 305 |
|---|---|---|
| OpenSpec | 137 | 44.9% |
| Python autre | 130 | 42.6% |
| autres commandes | 1 | 0.3% |
| lecture shell | 1 | 0.3% |
| prévol true | 25 | 8.2% |
| tests Python | 11 | 3.6% |
| total | 305 | 100.0% |

| Commande (100 caractères max) | completed | error | refused | total | part | taux C | taux E | taux R |
|---|---:|---:|---:|---:|---|---|---|---|
| /home/devops/.local/npm/bin/openspec validate --help | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/.local/npm/bin/openspec validate --strict --type change add-installation-and-first-conf | 5 | 0 | 0 | 5 | 1.6% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib,json,base64,z | 17 | 0 | 1 | 18 | 5.9% | 94.4% | 0.0% | 5.6% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib,json,fcntl;f= | 24 | 0 | 0 | 24 | 7.9% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib,json;p=Path(' | 3 | 0 | 0 | 3 | 1.0% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib;assert hashli | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import json,hashlib,fcntl;f= | 31 | 0 | 1 | 32 | 10.5% | 96.9% | 0.0% | 3.1% |
| /home/devops/python/current/bin/python3 -B -c 'import sys import json import hashlib import urllib.r | 2 | 0 | 0 | 2 | 0.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -I -B -c 'import os,sys,json,hashlib,fcntl;IDX=0;PE="openspe | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-installation-and-first-config | 23 | 0 | 0 | 23 | 7.5% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate docker-image --type spec --strict | 2 | 0 | 0 | 2 | 0.7% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate initial-administration --type spe | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate installation-provisioning --type  | 2 | 0 | 0 | 2 | 0.7% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate pixs-agent --type spec --strict | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate pzt --type spec --strict | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate reference-composition --type spec | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| [commande masquée : données potentiellement sensibles] | 19 | 0 | 0 | 19 | 6.2% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile /home/devops/datas/pixs/src/pixs/backend/ins | 7 | 0 | 0 | 7 | 2.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile /home/devops/datas/pixs/tests/unit/c08_e5_fi | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile /home/devops/datas/pixs/tests/unit/test_c08_ | 2 | 0 | 0 | 2 | 0.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path paths=["/home/devops/datas/p | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib,json,fcntl;f= | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib;assert hashli | 9 | 0 | 0 | 9 | 3.0% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import json,hashlib,fcntl;f= | 67 | 0 | 0 | 67 | 22.0% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'import hashlib import json import os import re import | 0 | 0 | 1 | 1 | 0.3% | 0.0% | 0.0% | 100.0% |
| /home/devops/python/current/bin/python3 -B -c 'import json,fcntl,hashlib from pathlib import Path wi | 2 | 0 | 0 | 2 | 0.7% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'import pathlib,json,hashlib,fcntl;f=pathlib.Path("/ho | 4 | 0 | 0 | 4 | 1.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -B -c 'import sys import json import hashlib import urllib.r | 14 | 0 | 0 | 14 | 4.6% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -I -B -c 'import os,json,hashlib,fcntl;R="/home/devops/datas | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -I -B -c 'import os,sys,json,hashlib,fcntl;IDX=1;PE="src/pix | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -I -B -c 'import os,sys,json,hashlib,fcntl;IDX=2;PE="src/pix | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /home/devops/python/current/bin/python3 -I -B <<'PYEOF' import json,os,hashlib,fcntl ckpt="/home/dev | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import pathlib,json,hashl | 11 | 0 | 0 | 11 | 3.6% | 100.0% | 0.0% | 0.0% |
| PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/src/pixs/backend/installation/__pycache__/c08-validation | 5 | 0 | 0 | 5 | 1.6% | 100.0% | 0.0% | 0.0% |
| python3 -c "import json, pathlib; p=pathlib.Path('/home/devops/datas/pixs/output/cismp/cismp1-pixs-0 | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| /usr/bin/rmdir /home/devops/datas/pixs/output/tests/c08-marker /home/devops/datas/pixs/output/tests/ | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| ls -la .opencode/state/cgpt-approval-bridge/ 2>&1; echo ---; cat .opencode/state/cgpt-approval-bridg | 0 | 1 | 0 | 1 | 0.3% | 0.0% | 100.0% | 0.0% |
| /usr/bin/true | 25 | 0 | 0 | 25 | 8.2% | 100.0% | 0.0% | 0.0% |
| PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/p | 6 | 0 | 0 | 6 | 2.0% | 100.0% | 0.0% | 0.0% |
| PYTHONPATH=/home/devops/datas/pixs/src:/home/devops/datas/pixs/tests/unit PYTHONDONTWRITEBYTECODE=1  | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_auth_r01 tes | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_data_governa | 1 | 0 | 0 | 1 | 0.3% | 100.0% | 0.0% | 0.0% |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_runtime_prof | 2 | 0 | 0 | 2 | 0.7% | 100.0% | 0.0% | 0.0% |
| total | 301 | 1 | 3 | 305 | 100.0% | 98.7% | 0.3% | 1.0% |

| commande refusée (<=100) | refused | part des refus |
|---|---:|---|
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import hashlib,json,base64,z | 1 | 33.3% |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path;import json,hashlib,fcntl;f= | 1 | 33.3% |
| /home/devops/python/current/bin/python3 -B -c 'import hashlib import json import os import re import | 1 | 33.3% |
| total refus | 3 | 100.0% |

Sorties et échecs (exit non zéro distinct d'un transport completed échoué) :

- native_error : 1
- nonzero : 6
- refused : 3
- unknown : 0
- zero : 295
- autre code de sortie non nul : 4
- tests en echec : 2

Famille lexicale OpenSpec différente d'un nombre de validations réelles ; source tronquée ou masquée conservée telle quelle.

## 5. Accès web

| libellé (<=100) | effectif | taux |
|---|---:|---|
| (aucun outil web natif à cette borne, aucune URL inventée ; réseau via Bash N/A non collecté) | 0 | N/A |
| total | 0 | N/A |

## 6. Synthèse globale

| jalon | valeur |
|---|---|
| création change (jour seul, heure N/A) | 2026-10-17 |
| début RUN distinct | 2026-10-22T03:18:51.485469+00:00 |
| borne de collecte | 2026-10-30T06:32:00.858Z |
| fin / archivage | EN ATTENTE |
| durée exacte du change | N/A (heure initiale absente) |
| durée calendaire provisoire RUN vers borne | 195h13min09s (inclut pauses, sans temps de service estimé) |

| relevé quota | usedPercent | windowDurationMins | resetsAt ISO | horodatage |
|---|---|---|---|---|
| initial (2026-10-22T03:20:30.061871+00:00) | 100 | 10080 | 2026-10-27T06:33:48.000Z | 2026-10-22T03:20:30.061871+00:00 |
| courant authentique (2026-10-30T06:32:29Z) | 78 | 10080 | 2026-11-04T06:45:53.000Z | 2026-10-30T06:32:29Z |
| différence (curUsed-qi.usedPercent si compte et fenêtre attestés et delta>=0) | N/A — compte, fenêtre ou reset non attestés identiques, quota partagé | — | — | — |

Quotas partagés sans crédit, solde ni plan ; aucune donnée privée.

| domaine exclusif | completed | error | refused | running | total | part globale | taux C | taux E | taux R |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| fichiers (write/edit/apply_patch) | 54 | 0 | 0 | 0 | 54 | 1.1% | 100.0% | 0.0% | 0.0% |
| commandes (bash) | 301 | 1 | 3 | 0 | 305 | 6.4% | 98.7% | 0.3% | 1.0% |
| web (webfetch/websearch) | 0 | 0 | 0 | 0 | 0 | 0.0% | N/A | N/A | N/A |
| autres (read/MCP/grep/glob/todo/discovery…) | 4331 | 62 | 2 | 0 | 4395 | 92.4% | 98.5% | 1.4% | 0.0% |
| total | 4686 | 63 | 5 | 0 | 4754 | 100.0% | 98.6% | 1.3% | 0.1% |

Cibles Bash (178) non comptées comme outils en plus ; edit/write hors autres. Contrôles : lectures API/sources, prévol true once exit 0, readiness 0 ; aucun test produit. BLOCKERS, lien TASKS et MAP effectivement écrits et vérifiés au cutoff. Seuls gate de clôture, libération et archivage ne sont pas encore faits à la borne, preuves finales dans checkpoint. Faits à la borne : blockers=true, lien tasks=true, carte=true, écriture en attente=true.
