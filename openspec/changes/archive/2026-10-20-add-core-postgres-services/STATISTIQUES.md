# Statistiques — C02 add-core-postgres-services

RUN `cismp1-pixs-05379f7c24c9437c` ; contexte CAB 383 ; archive `/home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-core-postgres-services`.

Périmètre : ce seul change, quatre sessions de travail natives successives. Intervalle de développement borné au relevé final après archive ; rédaction du rapport, tâche de clôture, publication et gate ultérieurs exclus des compteurs ci-dessous. Les historiques complets sont dédoublonnés par message/partie native. Les agrégats CAB/SSE ont une couverture différente et restent séparés. Les identifiants et preuves complètes sont dans `/home/devops/datas/pixs/output/cismp/cismp1-pixs-05379f7c24c9437c/state.json`.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée ; OpenCode 1.19.3 | opencode-go | high configuré ; variant absent de certaines métadonnées natives | 2.157 s | 513.519 | N/A — génération active non isolable des outils/attentes |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex / GPT-6 | N/A — version exacte non exposée | OpenAI | N/A — métadonnée de cette conversation non exposée | N/A — aucune sonde orchestrateur | N/A | N/A — télémétrie de génération absente |

Les 17 sondes valides sont isolées de la production, avec même fournisseur/modèle/high et sortie fixe 1 à 200. TTMT : premier delta SSE observable, qui peut inclure un résumé de raisonnement ; débit : tokens.output natifs divisés par intervalle premier/dernier delta texte. Moyennes arithmétiques, pas débits de production. Version exacte du modèle et temps de service cumulé tous agents : N/A ; aucun pourcentage calendaire présenté comme génération.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
|---|---|
| Messages natifs | 2155 (100 %) |
| Appels d’outils natifs | 1051 (100 %) |
| Terminés | 1034 (98.4 %) |
| Refus de permission natifs explicites | 0 (0.0 %) |
| Erreurs techniques natives | 17 (1.6 %) |
| Tokens input / output / reasoning | 10586224 / 735425 / 362144 |
| Cache read / write | 453094410 / 0 |
| Coût déclaré par OpenCode | 2.18432502 — unité/complétude de facturation N/A |
| Compactions natives observées | 6 parties ; cycles coordonnés Codex incomplets car API propriétaire absente |

| Décision CAB | Nombre | Part |
|---|---|---|
| Approuvées | 147 | 98.7 % |
| Refusées | 2 | 1.3 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 149 | 100 % |

Permissions once observées CAB : 145. Une approbation ne prouve pas un effet ; une fin native ne prouve pas seule la réussite métier. Les 58 commandes bash observées ont toutes un exit natif 0. Les demandes mal recopiées, les deux expirations de commandes dépassant la limite 2 000 et l’édition refusée sans effet sont consignées séparément au checkpoint. Aucun ancien once consommé n’est rejoué.

| Collecte isolée | Nombre | Part de 26 relèves |
|---|---|---|
| Valides | 17 | 65.4 % |
| Sans métriques initiales | 1 | 3.8 % |
| Invalides | 8 | 30.8 % |
| Total exécuté | 26 | 100 % |

Cadence prévue : début + 24 échéances de 30 minutes + fin ; un contrôle supplémentaire après application de mode1 est conservé séparément. 1 relève manquée (+120 min), sans reconstruction ; huit invalides conservées, reprises immédiates non effectuées. Limite de collecte signalée, sans transformer une sonde en benchmark PLLM. Min/max TTMT valides 1.114 / 3.537 s ; débit 142.653 / 959.866 tokens/s. Surcharge isolée : 7499 tokens output ; coût de sondes N/A (non collecté).

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 757 | 35.1 % |
| assistant | 1398 | 64.9 % |
| Total | 2155 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 1670 | 24.2 % |
| step-start | 1338 | 19.4 % |
| reasoning | 1498 | 21.7 % |
| tool | 1051 | 15.2 % |
| step-finish | 1335 | 19.4 % |
| compaction | 6 | 0.1 % |
| Total | 6898 | 100 % |

| Fin assistant | Nombre | Part |
|---|---|---|
| tool-calls | 800 | 57.2 % |
| stop | 533 | 38.1 % |
| absent | 63 | 4.5 % |
| length | 2 | 0.1 % |
| Total | 1398 | 100 % |

| Outil natif | Total / part | Terminé / taux | Refus / taux | Erreur / taux |
|---|---|---|---|---|
| cgpt-validation_broker_readiness | 141 / 13.4 % | 140 / 99.3 % | 0 / 0.0 % | 1 / 0.7 % |
| cgpt-validation_request_validation | 155 / 14.7 % | 144 / 92.9 % | 0 / 0.0 % | 11 / 7.1 % |
| bash | 58 / 5.5 % | 58 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| todowrite | 8 / 0.8 % | 8 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| read | 347 / 33.0 % | 346 / 99.7 % | 0 / 0.0 % | 1 / 0.3 % |
| glob | 46 / 4.4 % | 46 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| grep | 42 / 4.0 % | 42 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| edit | 38 / 3.6 % | 37 / 97.4 % | 0 / 0.0 % | 1 / 2.6 % |
| cgpt-validation_list_pending | 114 / 10.8 % | 114 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| cgpt-validation_poll_approval | 7 / 0.7 % | 4 / 57.1 % | 0 / 0.0 % | 3 / 42.9 % |
| cgpt-validation_cancel_approval | 2 / 0.2 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| cgpt-validation_get_approval | 10 / 1.0 % | 10 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| write | 50 / 4.8 % | 50 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| cgpt-validation_broker_health | 30 / 2.9 % | 30 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| cgpt-validation_broker_remediation_registry | 2 / 0.2 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| cgpt-validation_broker_auto_remediation_policy | 1 / 0.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

Les décisions CAB ci-dessus ne sont pas réparties artificiellement par type d’outil : corrélation exhaustive de tous les refus historiques N/A.

## 3. Fichiers modifiés

Tentatives natives edit/write : 88, dont 87 terminées et une erreur technique ; 48 chemins historiques (certains désignent le même fichier avant/après archivage). Le dernier contrôle source prouve 45 fichiers distincts écrits à cette frontière. Les écritures du checkpoint par l’orchestrateur et les déplacements CLI sont séparés des appels edit/write.

| Chemin absolu | Tentatives / part des 88 | Terminées / taux | Refusées / taux | Erreur / taux |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-core-postgres-services/design.md | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/__init__.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/uuid7.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/contracts.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/dto.py | 7 / 8.0 % | 7 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/ports.py | 7 / 8.0 % | 7 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_core_persistence_contracts.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/base.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/models_scope.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/models_identity.py | 4 / 4.5 % | 3 / 75.0 % | 0 / 0.0 % | 1 / 25.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/models_group.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/persistence/models_authz.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/models.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/migrations/__init__.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/migrations/0001_core_initial.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/migration_lock.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/core_pg_test_support.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_core_postgres_migrations.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_common.py | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_transaction_types.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_transactions.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/core_pg_participants.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_core_postgres_transactions.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_identity.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_core_postgres_identity.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_scope.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_groups.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_core_postgres_topology_authz.py | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_authz.py | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/query_source.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_queries.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_core_postgres_queries.py | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/services_bootstrap.py | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/core_pg_bootstrap_participants.py | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_core_postgres_bootstrap.py | 3 / 3.4 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/component.toml | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_core_service_manifest.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/core_delivery_checks.py | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-core-postgres-services/VALIDATION.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-core-postgres-services/requirements.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-core-postgres-services/proposal.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-core-postgres-services/tasks.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-core-postgres-services/design.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-core-postgres-services/requirements.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-core-postgres-services/proposal.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/README.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/TECHNICAL.md | 1 / 1.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/PROJECT.md | 2 / 2.3 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

Total : 88 (100 %), 87 terminées (98.9 %), 0 refusées (0.0 %), 1 erreur (1.1 %). Déplacement autorisé de `/home/devops/datas/pixs/openspec/changes/add-core-postgres-services` vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-core-postgres-services`, outil natif prt_1582b96b1001qI9Zv16yvADu5I, exit 0. Les liens propres ont été rebasés. Les références historiques des autres changes restent historiques et ne sont pas massivement réécrites.

## 4. Commandes

| Famille | Nombre / part des 58 | Exit 0 / taux | Refus natif / taux | Erreur native / taux |
|---|---|---|---|---|
| Prévol true | 10 / 17.2 % | 10 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| OpenSpec | 7 / 12.1 % | 7 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Syntaxe Python | 11 / 19.0 % | 11 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Autres commandes | 3 / 5.2 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Recette PostgreSQL | 23 / 39.7 % | 23 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Traçabilité documentaire | 3 / 5.2 % | 3 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Unités Python | 1 / 1.7 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

Total 58 (100 %), exit 0 : 58 (100 %). Les occurrences comprennent les prévols et rejeux contrôlés ; elles ne s’additionnent pas aux cas de recette uniques. Commandes refusées par permission bash native : aucune observée (0). Les deux refus CAB ne sont pas attribués à une commande sans corrélation prouvée ; libellé exact des commandes CAB refusées : N/A. Les deux demandes de contrôle documentaire expirées avant effet (limite 2 000) ne comptent pas comme commandes exécutées. Aucune commande Git.

## 5. Accès web

| Accès web natif observé | Approuvé/terminé | Refusé | Erreur | Total |
|---|---|---|---|---|
| webfetch/websearch | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Dénominateur nul : N/A pour les parts. Aucune URL visitée ou refusée par un outil web natif dans ces quatre historiques ; aucune URL déduite d’un texte. Les API locales OpenCode/CAB et leurs SSE sont de l’orchestration, pas des visites web. Télémétrie exhaustive des accès de l’orchestrateur : N/A ; aucune répartition fictive.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-19T19:13:55.140373+00:00 (UTC) |
| Fin — après archivage | 2026-10-20T07:26:28Z (UTC) |
| Durée globale, pauses/attentes incluses | 12 h 12 min 32 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-19T19:13:55.140374+00:00 | 68 % | 2026-10-24T23:23:28.000Z |
| Après — après archivage de la spécification | 2026-10-20T07:26:28Z | 4 % | 2026-10-27T06:33:48.000Z |
| Différence après − avant | — | N/A — réinitialisation entre relevés | — |

Compte identique et quota codex/10080 minutes ; resetsAt différents : aucune consommation reconstruite à travers la réinitialisation. Quotas partagés avec d’autres tâches, aucune attribution exclusive à C02.

| Domaine natif | Total / part | Terminé / taux | Refus / taux | Erreur / taux |
|---|---|---|---|---|
| autres | 905 / 86.1 % | 889 / 98.2 % | 0 / 0.0 % | 16 / 1.8 % |
| commandes | 58 / 5.5 % | 58 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| fichiers | 88 / 8.4 % | 87 / 98.9 % | 0 / 0.0 % | 1 / 1.1 % |
| web | 0 / 0.0 % | 0 / N/A | 0 / N/A | 0 / N/A |
| Total | 1051 / 100 % | 1034 / 98.4 % | 0 / 0.0 % | 17 / 1.6 % |

CAB/SSE : attente de ressource 0 s, détention partagée 7122.18 s, gel global 0 s ; busy/idle ne prouvent pas un gain causal. Interruption de contrôleur inconnue cumulée 29478.735 s, distincte de la durée de ce RUN et de ses historiques natifs.

Résultat produit : 346 tests purs, PostgreSQL réel transactions14/identité20/topologie46/QUERY62/R0158 et 12 indicateurs de migration réussis. Nettoyage et connexions fermées prouvés. Syntaxe36 fichiers Python, matrice72/89 et18SHA canoniques inchangés, 45 sources finales contrôlées (prt_15833d2b70014h41Xapb1ruygr). OpenSpec global standard/strict préarchive194 éléments et strict postarchive193 éléments, exit0, aucun avertissement ; seules INFO skip_specs. Détails et limites par exigence : VALIDATION.md.

Archive unique réalisée, canon non modifié ; aucun Git ni déploiement. Sources sensibles non ouvertes par le modèle ; seul le processus de recette extrait localement les cinq clés PostgreSQL autorisées, sans valeur en sortie ou argument. C02 reste borné : intégrations C03–C10 et qualification P0 distinctes. À la borne de rédaction, publication/gate/libération/arrêt ciblé restent à prouver au checkpoint ; aucune réussite anticipée de ces étapes.
