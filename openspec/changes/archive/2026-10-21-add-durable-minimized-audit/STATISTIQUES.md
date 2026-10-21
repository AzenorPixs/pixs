# Statistiques — C05 / CISMP2

Collecte arrêtée après archivage, avant rédaction du rapport, à 2026-10-20T23:35:51.277185+00:00. RUN cismp2-pixs-968e38f3e27b4bbf, contextes434 puis444, même session native ses_ea598af07fferBsu2YA9oOfSGT. Les opérations de rédaction, contrôle du présent rapport et gate/STOP sont postérieures à cette borne et exclues des totaux ci-dessous. Le résultat terminal postérieur se vérifie dans le checkpoint du RUN.

### Agents de codage

Client OpenCode vérifié vivant : 1.19.3.

| Rôle | Fournisseur / modèle | Raisonnement observé | Messages assistant, session principale |
|---|---|---|---|
| OpenCode build | opencode-go / muse-spark-1.3-contributor | high | 326 (99,7 %) |
| OpenCode compaction | opencode-go / muse-spark-1.3-contributor | variant non exposé dans la réponse ; high configuré | 1 (0,3 %) |
| Total principal | même session persistante | sans changement de modèle | 327 (100 %) |

OpenCode assure les écritures et exécutions natives ; CGPT conçoit/revoit les contenus, prescrit les mandats et décide les approbations. Les sondes auxiliaires sont présentées séparément ; elles ne sont pas ajoutées aux 445 messages ou276 outils de la session principale.

### Agents orchestrateurs

| Agent | Identité | Modèle/version/raisonnement, tokens et coût |
|---|---|---|
| Codex / CGPT | 01a15a62-7959-7e81-9263-58958da843bb | N/A — métadonnées détaillées non exposées ; read_thread dépasse la taille retournable du tour |
| Sous-agents | Aucun sous-agent lancé par cet orchestrateur | Sans objet |

## 1. Statistiques générales et décisions

Sources : exports JSON et Markdown CAB filtrés par RUN et contextId434/444, historique HTTP natif OpenCode, journal de mandats/checkpoint, sondes conservées et outil natif de quotas. Les agrégats CAB commencent/finissent selon leurs fenêtres d’observation ; leurs durées ne reconstituent pas les lacunes et ne sont pas une mesure de codage productif.

| Mesure principale | Valeur |
|---|---|
| Durée calendaire instrumentée, pauses/attentes incluses | 05 h 57 min 28 s |
| Messages natifs | 445 |
| Appels d’outils natifs | 276 |
| Outils terminés avec succès | 251 (90,9 %) |
| Refus explicites de permission native | 5 (1,8 %) |
| Erreurs techniques ou contrôles exécutés en échec | 20 (7,2 %) |
| Fichiers édités par outils de fichier | 17 cibles / 34 tentatives |
| Commandes | 24 tentatives / 19 contenus distincts |
| Tests et recette finaux | 224 tests réussis (0 skip),35 scénarios PostgreSQL réussis,9 compilations,9 canons inchangés, strict OpenSpec1/1 |
| Coût déclaré par l’API OpenCode | 0.61893916 ; unité monétaire non exposée, facturation réelle N/A |

Convention : succès signifie outil terminé sans erreur, pas nécessairement approbation manuelle. Un refus natif est explicite ; les erreurs MCP, délais et codes de test non nuls sont classés séparément. Les deux commandes de test exécutées en échec ont ensuite été corrigées et validées. Les pourcentages sont arrondis à une décimale ; les arrondis peuvent ne pas sommer100.

| Décisions CAB, fenêtres propres au RUN | Nombre | Part |
|---|---|---|
| Approuvées | 58 | 95,1 % |
| Refusées | 3 | 4,9 % |
| Clarification | 0 | 0,0 % |
| En attente | 0 | 0,0 % |
| Total | 61 | 100 % |

| Cible de décision | Approuvées | Refusées | Total |
|---|---|---|---|
| Fichier, corrélation MCP terminale | 34 | 0 | 34 |
| Commande, corrélation MCP terminale | 24 | 1 | 25 |
| Cible non documentée dans les réponses terminales conservées | 0 | 2 | 2 |
| Total CAB | 58 | 3 | 61 |

Les deux refus à cible non documentée restent dans le total CAB ; leur type n’est pas reconstruit. Les58 approbations sont documentées :53 ont donné une permission once et cinq n’en ont pas donné. Les53 identifiants de permission sont uniques et les53 opérations sont terminées ; aucun effet n’est rejoué. Les refus CAB et les cinq refus de permission native sont des événements différents.

| Jetons, cumul API de327 réponses principales | Nombre | Part du total API |
|---|---|---|
| input | 3 140 189 | 2,5 % |
| output | 240 833 | 0,2 % |
| reasoning | 38 710 | 0,0 % |
| cache_read | 124 505 830 | 97,3 % |
| cache_write | 0 | 0,0 % |
| Total API | 127 925 562 | 100 % |

Le total API égale ici la somme des cinq champs ; il inclut les contextes répétés et le cache par appel, sans prétention de tokens uniques. Coût et tokens des sondes sont hors de ce total principal.

| Contexte CAB | État à la collecte | Approuvé / refusé / once | Réservé observé | busy / idle / inconnu |
|---|---|---|---|---|
| 434 | ABANDONED / WORK | 4 / 2 / 4 | 00 h 32 min 20 s | 00 h 09 min 45 s / 00 h 22 min 35 s / 77 ms |
| 444 | RESERVED / REPORT | 54 / 1 / 49 | 02 h 01 min 39 s | 01 h 03 min 19 s / 00 h 58 min 20 s / 0 ms |

Les compteurs de messages CAB par contexte ne sont pas additionnés au dénombrement natif par identifiant. Le champ global restartUnknownMs concerne le contrôleur et n’est pas attribué au RUN. Attente de ressource observée : 00 h 01 min 21 s. Détention partagée observée : 00 h 51 min 01 s. Effet sous permission en suivi : 14831 ms. Ces fenêtres peuvent se recouvrir.

### Sondes de l’agent de codage

| Position | Horodatage UTC réel ou attendu | État | TTMT s | Tokens/s | Tokens sortie |
|---|---|---|---|---|---|
| Initiale | 2026-10-20T17:39:46.835557+00:00 | completed | 4.292 | 303.35 | 408 |
| Reprise | 2026-10-20T21:35:10.618242+00:00 | completed | N/A | N/A | 409 |
| Échéance manquée | 2026-10-20T22:05:10.618242+00:00 | MISSED | N/A | N/A | N/A |
| complément après échéance manquée +30min | 2026-10-20T22:07:47.502103+00:00 | completed | 1.453 | 221.86 | 408 |
| +60min reprise | 2026-10-20T22:35:28.142551+00:00 | completed | 1.998 | 234.35 | 408 |
| +90min reprise | 2026-10-20T23:06:35.639121+00:00 | completed | 2.293 | 236.38 | 408 |
| finale après archivage / échéance périodique | 2026-10-20T23:35:28.559031+00:00 | completed | 1.049 | 771.27 | 408 |

Échéance initiale 2026-10-20T18:09:46.835557+00:00 : MISSED — Pilotage suspendu pour intégrité CAB commune, aucun relevé rétroactif.

Mesure : même consigne de200 entiers, bornes natives de parties texte, sans chronométrage SSE token par token. Une échéance manquée n’est pas backdatée ; le complément de22:07 est identifié. La sonde finale a été exécutée après archivage et son échéance périodique avec0,42s de retard. Le TTMT de reprise n’a pas été conservé : N/A. Le benchmark PLLM de reprise (budget2048, TTFT7,474s et débit déclaré1819,136tokens/s) est une autre méthode et ne remplace pas ces sondes.

### Compactage

Un compactage OpenCode natif achevé est conservé : msg_15b81b195001r3wpBvABFHCApO, même session et même modèle. Le compactage coordonné Codex est N/A : API thread/compact/start non exposée. Aucune réussite conjointe n’est inventée.

## 2. Types de messages et d’outils

| Rôle de message OpenCode | Nombre | Part |
|---|---|---|
| user | 118 | 26,5 % |
| assistant | 327 | 73,5 % |
| Total | 445 | 100 % |

Les messages user d’OpenCode sont les mandats/pilotages, pas un décompte de messages humains dans Codex.

| Type de partie native | Nombre | Part |
|---|---|---|
| text | 403 | 23,9 % |
| step-start | 327 | 19,4 % |
| reasoning | 352 | 20,9 % |
| tool | 276 | 16,4 % |
| step-finish | 327 | 19,4 % |
| compaction | 1 | 0,1 % |
| Total | 1686 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 222 | 67,9 % |
| stop | 105 | 32,1 % |
| Total | 327 | 100 % |

| Outil natif | Total | Part globale | Succès outil | Refus natif | Erreur |
|---|---|---|---|---|---|
| bash | 24 | 8,7 % | 17 (70,8 %) | 5 (20,8 %) | 2 (8,3 %) |
| cgpt-validation_broker_evaluate_remediation | 1 | 0,4 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 8 | 2,9 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 29 | 10,5 % | 29 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_cancel_approval | 3 | 1,1 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 5 | 1,8 % | 3 (60,0 %) | 0 (0,0 %) | 2 (40,0 %) |
| cgpt-validation_list_pending | 17 | 6,2 % | 17 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 11 | 4,0 % | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 67 | 24,3 % | 51 (76,1 %) | 0 (0,0 %) | 16 (23,9 %) |
| edit | 15 | 5,4 % | 15 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| glob | 11 | 4,0 % | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 6 | 2,2 % | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 55 | 19,9 % | 55 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| todowrite | 5 | 1,8 % | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 19 | 6,9 % | 19 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 276 | 100 % | 251 | 5 | 20 |

Pour les outils MCP de validation, succès désigne la réponse technique de l’outil ; la décision métier CAB est dans le tableau séparé de la section1.

## 3. Fichiers modifiés

| Chemin absolu au moment de l’écriture | Tentatives | Part | Écritures accordées/terminées | Refusées | En erreur |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/PROJECT.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/README.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/TECHNICAL.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-durable-minimized-audit/VALIDATION.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-durable-minimized-audit/design.md | 2 | 5,9 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-durable-minimized-audit/proposal.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-durable-minimized-audit/requirements.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-durable-minimized-audit/tasks.md | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/audit_access.py | 5 | 14,7 % | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/audit_bootstrap_import.py | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/audit_contracts.py | 2 | 5,9 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/audit_sink.py | 2 | 5,9 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/migrations/0002_core_audit.py | 2 | 5,9 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/models.py | 1 | 2,9 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/persistence/models_audit.py | 3 | 8,8 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_core_audit_durable.py | 7 | 20,6 % | 7 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_core_audit_sink.py | 2 | 5,9 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 34 | 100 % | 34 | 0 | 0 |

Ce sont des tentatives d’outils de fichier, pas des lignes modifiées. La génération initiale de0002_core_audit.py par Bash et les caches temporaires appartiennent aux commandes ; ils ne sont pas doublement ajoutés au total global. Une séquence Unicode a été corrigée avant tests ; une ligne blanche supplémentaire sans différence fonctionnelle est tracée au checkpoint.

Archivage réel : /home/devops/datas/pixs/openspec/changes/add-durable-minimized-audit/ vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-durable-minimized-audit/ ; sept artefacts conservés à empreinte identique. Les chemins historiques du tableau sous le change actif se résolvent désormais dans ce dossier. Le delta specs/audit/spec.md et .openspec.yaml ont été déplacés sans édition. Le présent STATISTIQUES.md est postérieur à la borne de collecte.

## 4. Commandes

| Famille | Tentatives | Part | Succès | Refus | Échec exécuté |
|---|---|---|---|---|---|
| OpenSpec | 3 | 12,5 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Prévol true | 3 | 12,5 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python | 18 | 75,0 % | 11 (61,1 %) | 5 (27,8 %) | 2 (11,1 %) |
| Total | 24 | 100 % | 17 | 5 | 2 |

### Toutes les commandes refusées, regroupées par contenu exact

| Libellé (100 caractères maximum, empreinte courte incluse) | Occurrences refusées | Part des refus |
|---|---|---|
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import dataclasses import json im… [e2f663b2] | 1 | 20,0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import pathlib import sys sys.pat… [47710d13] | 1 | 20,0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C05_MIGRATION' import pathlib im… [186485e2] | 1 | 20,0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import pathlib import sys sys.pat… [0786a975] | 1 | 20,0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import json import sys sys.path[:… [9bff9df5] | 1 | 20,0 % |
| Total | 5 | 100 % |

Chaque libellé est tronqué et porte une empreinte du contenu complet conservé dans le mandat/checkpoint. Les refus de quoting ou de révision sont intervenus avant once ; les deux échecs exécutés concernent la fixture PDP et le PYTHONPATH du harnais, corrigés puis validés. L’unique archivage a réussi, sans skip-specs ni no-validate ; specsUpdated=false car le delta était déjà synchronisé.

## 5. Accès web

| Domaine observé | Total | Accordés | Refusés | Erreurs |
|---|---|---|---|---|
| Outils web natifs | 0 | N/A | N/A | N/A |

Aucune URL documentaire approuvée ou refusée n’est observée, aucune page visitée à déclarer. Les appels modèles Go et les API locales de pilotage/quotas sont des services techniques utilisés par la session ; aucun accès web documentaire n’en est déduit. Les outils de l’orchestrateur ne disposent pas d’un export exhaustif comparable : N/A, non reconstruit.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début instrumenté retenu — relevé quota initial | 2026-10-20T19:38:23.060716+02:00 |
| Fin — après archivage, avant rédaction | 2026-10-21T01:35:51.277185+02:00 |
| Durée globale entre ces bornes, pauses et attentes incluses | 05 h 57 min 28 s |

La préparation antérieure à la première borne n’est pas horodatée par ces sources : N/A. Les durées d’agents parallèles ne sont pas additionnées à cette durée calendaire.

| Quota Codex sur7jours | Horodatage UTC | Utilisé | Fenêtre / réinitialisation |
|---|---|---|---|
| Avant | 2026-10-20T17:38:23.060716+00:00 | 31 % | 10080 min / 1793082828 |
| Reprise | 2026-10-20T21:34:58.424760+00:00 | 40 % | 10080 min / 1793082828 |
| Après archivage | 2026-10-20T23:35:51.277185+00:00 | 61 % | 10080 min / 1793082828 |
| Différence hebdomadaire | N/A | N/A | Identité du compte absente des relevés avant/reprise ; comparaison non certifiable |

Les trois relevés portent sur10080minutes avec la même réinitialisation, mais l’identité initiale n’a pas été conservée ; aucune consommation n’est calculée ni attribuée. Le quota est partagé par le compte et peut inclure les autres travaux simultanés. La rédaction ultérieure du rapport est hors de l’intervalle.

| Domaine | Nombre | Part globale | Succès / accord technique | Refus | Erreur |
|---|---|---|---|---|---|
| Fichiers (outils dédiés) | 34 | 12,3 % | 34 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commandes | 24 | 8,7 % | 17 (70,8 %) | 5 (20,8 %) | 2 (8,3 %) |
| Web | 0 | 0,0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils / lecture / MCP | 218 | 79,0 % | 200 (91,7 %) | 0 (0,0 %) | 18 (8,3 %) |
| GLOBAL | 276 | 100 % | 251 (90,9 %) | 5 (1,8 %) | 20 (7,2 %) |

Résultat livré au gel : propriétaire C05 testé, archive openspec/changes/archive/2026-10-21-add-durable-minimized-audit vérifiée, publication CAB référence51.35casPG réels et224régressions réussis ; les owners Auth/C4/C10/Jobs synthétiques ne qualifient pas leur runtime ni P0. Aucun Git, push ou déploiement mandaté ; pas de secret dans les sorties de test, cinq valeurs PG confinées au processus masqué. Les services partagés restent disponibles. La validation du présent rapport et le gate/STOP ciblés sont postérieurs au gel et se consultent dans le checkpoint.

<!-- CAB_REPORT_TOTALS {"archive_artifacts":7,"cab_approved":58,"cab_rejected":3,"cab_total":61,"canonical_unchanged":9,"command_attempts":24,"domains":{"commands":{"error":2,"refused":5,"success":17},"files":{"success":34},"other":{"error":18,"success":200}},"file_attempts":34,"messages":445,"once":53,"outcomes":{"error":20,"refused":5,"success":251},"parts_total":1686,"pg_cases":35,"quota_difference":null,"regression_tests":224,"roles":{"assistant":327,"user":118},"tool_total":276,"unique_permissions":53,"web_attempts":0} -->
