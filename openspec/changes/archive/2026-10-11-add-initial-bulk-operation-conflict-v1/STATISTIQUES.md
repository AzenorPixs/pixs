# Statistiques — add-initial-bulk-operation-conflict-v1

RUN cismp-pixs-758862ec875d4708. Bornes de collecte natives ci-dessous, historique complet paginé par session puis filtré par création du message. RSMP préalable, benchmark PLLM, sondes jetables et publication de ce rapport exclus des totaux de production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash | N/A : version exacte non exposée | OpenCode Go | xhigh | 1.707 s | 85.577 | N/A |
| Qwen3.8 Flash (compaction administrative) | N/A | OpenCode Go | N/A : paramètre absent du contrat summarize | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A : identifiant exact non exposé | OpenAI | N/A | N/A : non sondé | N/A | N/A |

Temps de service N/A : aucun chronométrage comparable de génération active ; les durées des messages incluent outils et permissions. Aucun dénominateur fiable ni estimation des chevauchements. Runtime OpenCode 1.18.35 ; broker actif observé 0.87.1, plugin distribué 0.87.2 (distincts).

## 1. Statistiques générales et décisions

198 messages (100 %), 126 appels natifs/MCP (100 %), durée calendaire 08 h 55 min 46 s, pauses et attentes incluses.

| Décisions CAB uniques observées | Nombre | Part |
| --- | --- | --- |
| APPROVED | 23 | 88.5 % |
| REJECTED | 3 | 11.5 % |
| Total | 26 | 100 % |

Un appel abouti a terminé sous permission automatique ou manuelle ; cela ne prouve pas une approbation CAB. Une demande de validation peut aboutir en renvoyant REJECTED. Les décisions CAB sont dédupliquées par approval_id et distinctes des résultats d’outils. Les erreurs de transport restent enregistrées même lorsqu’un polling résout ensuite la même approbation.

| Compteur natif | Valeur |
| --- | --- |
| cache_read | 7346814 |
| cache_write | 1242942 |
| input | 858 |
| output | 81791 |
| reasoning | 0 |
| total | 8672405 |
| Coût télémétrique production (USD) | 0.40470789 |
| Compactions natives | 2 |

Compteurs input/output/reasoning/cache reproduits sans addition artificielle ; coût réellement facturé N/A. Résultats : trois compilations exit0 ; 10 tests ciblés et 83 régressions OK, soit 93/93 (100 %) ; strict pré-code et post-code du change exit0, une entrée passée sans issue. Les validations canoniques globales préalables restent exit1 pour trois avertissements historiques de longueur, zéro erreur nouvelle : pas de réussite globale déclarée.

Incidents conservés : lecture d’un chemin diagnostics.py inexistant ; erreur MCP -32602 avant enregistrement (hors décisions CAB) ; demande divergente refusée sans exécution ; délais -32001 résolus sur la même approbation ; polling interrompu ; outil list_pending hors protocole après prévol consommé, avec gel technique. Remplacements de contrats gelés explicitement validés par le développeur, sans purge de l’historique.

Un prévol a exécuté /usr/bin/true autorisé puis **sleep 2 hors mandat CAB**, sans permission once correspondante. Effet connu : pause locale de deux secondes, exit0, aucune écriture/externe. Cause de pilotage : le champ tools du message réinitialisait les permissions ; ce champ est désormais entièrement omis, permissions PATCH explicites avant chaque tour. Ne pas assimiler ce succès technique à une autorisation CAB.

Une édition tasks.md fictive (oldString inexistant, newString PROBE_BLOCKED) a échoué sans écriture ; aucun asked/once ne l’a autorisée. Lors de sa récupération, un premier /usr/bin/true autorisé a réussi, puis le second appel identique a été refusé avant exécution ; complete a renvoyé HTTP409 preflight-tool-not-completed. La candidate a été conservée et le contrat remplacé après nouvelle validation développeur. Garde de pilotage ajoutée : interruption volontaire du tour au résultat terminal natif, puis rapport séparé. Les premiers essais séparaient aussi demande et exécution ; le flux a été simplifié en demande CAB et opération unique dans le même tour, avec les neuf arguments intégralement prescrits. Ces interruptions de génération ne rendent pas la commande réussie invalide et ne sont pas une fermeture du processus OpenCode.

La reprise PLLM a rencontré deux requêtes de transport invalides puis une échéance benchmark 120s ; l’attente et les tentatives ultérieures figurent dans le checkpoint, hors appels natifs de production.

Réconciliation finale tasks.md : l’autorisation cismp-final-37508ade4e02, approuvée avant compactage et encore non consommée, a servi une seule fois à l’édition exacte des sept cases. L’intention ultérieure cismp-final-df17d9996b59 n’avait pas été enregistrée ; aucun succès CAB ne lui est attribué. Un mandat d’archive a ensuite réutilisé cet identifiant périmé et a été refusé sans exécution ; l’archive réelle utilise cismp-final-f3d1eba3433c, neuf champs exacts, une permission once et exit0. Les appels à des outils non exposés sont conservés comme erreurs techniques, sans effet natif autorisé déduit. Le benchmark relancé immédiatement sur instruction développeur a finalement réussi (TTFT 53.6568s, 52.291 tokens/s) ; aucune réussite n’a été inventée pendant la dérogation temporaire.

### Sondes de performance séparées

Relèves prévues 4 : début, reprise après pause manuelle, reprise finalisation et fin ; réussies 4 (100 %), échouées 0, manquées 0. Fenêtres actives : 2026-10-10T21:33:24.699852+02:00 → 22:02:41.796499+02:00 ; 2026-10-11T05:21:00.528886+02:00 → 05:35:40.046911+02:00 ; reprise finalisation 2026-10-11T06:11:10.447424+02:00 → 2026-10-11T06:29:11.591611+02:00. Cadence périodique réarmée à +30min à chaque reprise ; aucune échéance périodique dans ces fenêtres. Les pauses de décision et d’attente PLLM ne sont pas reconstituées. Les horodatages de cadence exacts sont conservés au checkpoint.

| Position | Horodatage | État | TTMT (s) | Tokens/s | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- | --- | --- |
| début BulkOperationConflict | 2026-10-10T21:33:24.744106+02:00 | valid | 1.414244 | 66.702645 | 401 | 0.00209917 |
| reprise après pause manuelle | 2026-10-11T05:21:29.204097+02:00 | valid | 1.359385 | 112.594952 | 358 | 0.00207896 |
| reprise finalisation après prévol gardé | 2026-10-11T06:11:10.501335+02:00 | valid | 2.378103 | 85.837010 | 350 | 0.0020752 |
| fin après archivage BulkConflict | 2026-10-11T06:28:37.808863+02:00 | valid | 1.674611 | 77.172608 | 403 | 0.00210011 |

Moyennes arithmétiques des seules relèves valides : TTMT 1.706586 s (min/max 1.359385/2.378103) ; débit 85.576804 tokens/s (min/max 66.702645/112.594952).

Relèves tentées 4, valides 4 (100.0 %), invalides 0. Relèves prévues/manquées : voir cadence active et pauses consignées au checkpoint ; aucune reconstitution rétroactive. Prompt constant : « Écris uniquement les entiers de 0001 à 0064 inclus, un par ligne sur quatre chiffres. Aucun commentaire, aucun outil. »

TTMT/débit issus du premier/dernier delta text natif (raisonnement/réponse si présents), compteur output non ventilé. Sondes dédiées sans outil, fichier ni réseau par le modèle. Surcharge séparée : 39732 tokens natifs totaux, 0.00835344 USD ; durées et horodatages individuels conservés au checkpoint.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 148 | 74.7 % |
| user | 50 | 25.3 % |
| Total | 198 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| compaction | 2 | 0.3 % |
| reasoning | 144 | 22.1 % |
| step-finish | 143 | 21.9 % |
| step-start | 144 | 22.1 % |
| text | 93 | 14.3 % |
| tool | 126 | 19.3 % |
| Total | 652 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| absent / tour interrompu | 5 | 3.4 % |
| stop | 45 | 30.4 % |
| tool-calls | 98 | 66.2 % |
| Total | 148 | 100 % |

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| bash | 17 | 13.5 % | 15 (88.2 %) | 1 (5.9 %) | 1 (5.9 %) |
| cgpt-validation_broker_readiness | 20 | 15.9 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 14 | 11.1 % | 13 (92.9 %) | 0 (0.0 %) | 1 (7.1 %) |
| cgpt-validation_list_pending | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 3 | 2.4 % | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| cgpt-validation_request_validation | 26 | 20.6 % | 22 (84.6 %) | 0 (0.0 %) | 4 (15.4 %) |
| edit | 2 | 1.6 % | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| glob | 6 | 4.8 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 6 | 4.8 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 24 | 19.0 % | 22 (91.7 %) | 0 (0.0 %) | 2 (8.3 %) |
| write | 7 | 5.6 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 126 | 100 % | 115 (91.3 %) | 1 (0.8 %) | 10 (7.9 %) |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-conflict-v1/design.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-conflict-v1/proposal.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-conflict-v1/specs/bulk-operations/spec.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-conflict-v1/tasks.md | 3 | 33.3 % | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_conflict.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_conflict_integration.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_conflict.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |

Tentatives d’écriture native, pas fichiers uniques. Trois nouveaux Python et quatre artefacts préparatoires ; tasks.md est ensuite coché sur preuves. L’archive déplace ces quatre artefacts vers openspec/changes/archive/2026-10-11-add-initial-bulk-operation-conflict-v1. Canon et TECHNICAL.md modifiés au RSMP préalable, hors intervalle de production. Les 305 fichiers existants ont été vérifiés, PA/PZT conservés.

Opérations de contrôle hors outils de codage : remplacements autorisés du seul fichier /home/devops/datas/pixs/.opencode/state/cgpt-approval-bridge/controller-job.json depuis métadonnées API publiques, sans lecture de l’ancien fichier exclu, sans purge. Mises à jour du checkpoint par l’orchestrateur : nombre exact N/A, non compté comme écritures natives. Publication du présent fichier : mandat distinct, hors intervalle scellé.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 3 | 17.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Pause locale hors mandat | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol true | 8 | 47.1 % | 6 (75.0 %) | 1 (12.5 %) | 1 (12.5 %) |
| Python | 5 | 29.4 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 | 100 % | 15 (88.2 %) | 1 (5.9 %) | 1 (5.9 %) |

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| 1. OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-initial-bu… | 2 | 11.8 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 2. /usr/bin/true | 8 | 47.1 % | 6 (75.0 %) | 1 (12.5 %) | 1 (12.5 %) |
| 3. /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_operation_conflict.… | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 4. sleep 2 | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 5. /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_operation_conflict.… | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 6. /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_operation_co… | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 7. PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_bulk_… | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 8. PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_semve… | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 9. OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-initial-bul… | 1 | 5.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 | 100 % | 15 (88.2 %) | 1 (5.9 %) | 1 (5.9 %) |

Libellés limités à 100 caractères ; commandes intégrales dans l’historique et le checkpoint. Refus regroupés : compilation du test unitaire refusée au stade mandat divergent, sans Bash ; seconde tentative /usr/bin/true refusée au stade permission native, sans exécution. Le refus de mandat n’est pas converti en appel Bash inexistant.

## 5. Accès web

0 appel web (0 % des outils), 0 abouti, 0 refusé, 0 erreur ; taux web N/A, dénominateur nul. Aucune URL visitée ou refusée par l’agent de codage. API CAB/SSE locaux et transport fournisseur distincts des outils web.

Diagnostic orchestrateur distinct, hors totaux de production : consultation de sources publiques OpenCode ; aucune écriture externe. URLs de référence (tronquées à 100 caractères) :

| URL | Statut |
| --- | --- |
| https://github.com/anomalyco/opencode/blob/v1.18.35/packages/opencode/src/permission/index.ts | Lecture publique orchestrateur, hors intervalle natif |
| https://github.com/anomalyco/opencode/blob/v1.18.35/packages/opencode/src/session/llm/request.ts | Lecture publique orchestrateur, hors intervalle natif |
| https://github.com/anomalyco/opencode/blob/v1.18.35/packages/opencode/src/session/tools.ts | Lecture publique orchestrateur, hors intervalle natif |

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-10T21:33:24.699852+02:00 |
| Fin — après archivage | 2026-10-11T06:29:11.591611+02:00 |
| Durée globale (pauses et attentes incluses) | 08 h 55 min 46 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-10T21:33:24.699876+02:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-11T06:29:11.591587+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux bornes ; identité/fenêtre non vérifiables, aucun quota externe substitué. Les quotas sont partagés par le compte ; une variation pourrait inclure d’autres tâches simultanées.

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Autres outils | 100 | 79.4 % | 92 (92.0 %) | 0 (0.0 %) | 8 (8.0 %) |
| Commandes | 17 | 13.5 % | 15 (88.2 %) | 1 (5.9 %) | 1 (5.9 %) |
| Fichiers | 9 | 7.1 % | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 126 | 100 % | 115 (91.3 %) | 1 (0.8 %) | 10 (7.9 %) |

Archive vérifiée : openspec/changes/archive/2026-10-11-add-initial-bulk-operation-conflict-v1, specsUpdated=false. Rapport publié ensuite sous mandat fichier distinct. Git : aucune inspection/opération dans ce périmètre. Aucun secret inclus dans les nouveaux contenus vérifiés. Aucun effet externe mutable observé ; les traces ne prouvent pas toute activité extérieure au RUN. Change livré ; cycle global incomplet, sélection suivante bornée aux spécifications validées.
