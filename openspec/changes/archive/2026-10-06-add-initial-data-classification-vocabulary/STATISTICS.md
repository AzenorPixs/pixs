# Statistiques — add-initial-data-classification-vocabulary

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-data-classification-vocabulary. RUN : cismp-pixs-20261005-2654fe47.

Intervalle : 2026-10-06T09:59:08.284000+00:00 → 2026-10-06T11:11:17.671743+00:00. Pauses et attentes incluses ; production de ce rapport exclue.

Couverture : messages accessibles de la seule session maîtresse ses_eefa39c24ffe1dGvdToTr4NfJh dans cet intervalle, bornes incluses. Les autres changes et les sessions de sondes sont exclus des totaux de production. Les compteurs de l'orchestrateur non exposés sont N/A.

Registre de preuves : output/cismp-state.json, branche data_classification_cycle. Archive native : message msg_110e54cbf001rezkCdGHlCtEy3, part prt_110e5765b001ZXg6eHGQxB9iA2. Tests : cismp-20261006-classification-unit-tests-f3042f33, cismp-20261006-classification-integration-test-2abb3a5b, cismp-20261006-classification-regression-c0373a4c.

Convention : une réussite technique d'outil ne prouve ni la conformité du contenu ni une approbation ; les décisions CAB sont comptées séparément. Un exit CLI 1 reste une erreur de résultat même lorsque les 19 WARNING connus sont qualifiés pour le cycle. Les refus explicites restent distincts des erreurs et interruptions.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A — version non exposée | opencode-go | xhigh | N/A — aucune sonde fixe valide | N/A — aucune sonde fixe valide | 284.726 s observées ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex /root | N/A — télémétrie exacte indisponible | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — génération non exposée |

Temps du codeur : somme des intervalles horodatés des parties text/reasoning, hors outils et attentes. Dénominateur de service de tous les agents inconnu : part N/A. La qualification PLLM antérieure est une mesure distincte, exclue des moyennes de sondes de ce change.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Durée du change | 01 h 12 min 09 s |
| Messages | 139 |
| Appels outils | 79 |
| Tokens entrée hors cache | 624 |
| Tokens sortie | 42343 |
| Tokens raisonnement exposés | 0 |
| Cache lu | 27251326 |
| Cache écrit | 351892 |
| Coût production USD | 0.526394426 |
| Compactions observées | 0 |

| Décision CAB finale observée | Mandats distincts (% décisions) |
| --- | --- |
| APPROVED | 27 (93.1 %) |
| REJECTED | 2 (6.9 %) |
| Total | 29 (100.0 %) |

Résultat : 6/6 tâches prouvées ; 27/27 tests réussis ; trois compilations exit 0. Strict du change et de data-governance : exit 0 avant et après code. Les quatre contrôles globaux retournent réellement 1, uniquement sur les 19 WARNING de longueur qualifiés ; aucune ERROR ni autre issue. Empreintes de référence inchangées.

Incident de contenu : le write du test d'intégration a décalé quatre assertions malgré le CONTENT exact approuvé. Une édition ciblée distincte a rétabli l'empreinte attendue. Le gel protocolaire a été tardif ; cette omission de l'orchestrateur est conservée. Réconciliation puis readiness READY/pending=0 et test CAB true exit 0 ont permis une reprise au premier état non prouvé. Une demande orpheline de prévalidation et une compilation gelée ont été refusées, décisions reçues par MCP, sans exécution native. Aucun rejeu d'écriture ni extension. Un compte rendu d'archive citant une ligne absente du JSON natif a été corrigé à partir des preuves API relues par root, sans réarchivage.

### Sondes et surcharge

Prompt fixe de 48 lignes, même modèle et xhigh, sessions jetables sans outil ni accès projet. Chaque sortie est contrôlée exactement ; aucune moyenne n'est fabriquée pour une sortie divergente.

| Position | Envoi UTC | Statut | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- |
| début classification | 2026-10-06T09:59:48.942428+00:00 | failed | 1174 | 0.00292308 |
| +30 min | 2026-10-06T10:29:49.377010+00:00 | failed | 2193 | 0.00340201 |
| +60 min | 2026-10-06T10:59:49.810242+00:00 | failed | 809 | 0.00275153 |
| fin | 2026-10-06T11:08:56.661540+00:00 | failed | 555 | 0.00263215 |

| Statut sonde | Occurrences (% sondes) |
| --- | --- |
| failed | 4 (100.0 %) |
| Total | 4 (100.0 %) |

| Surcharge télémétrie séparée | Valeur |
| --- | --- |
| Tokens sortie | 4731 |
| Coût connu USD | 0.011708770 |
| Moyennes de performance | N/A — sorties fixes invalides |

Compactage conjoint périodique : incomplet, API native de compactage de l'orchestrateur non exposée. Aucun agent auxiliaire substitué, aucune réussite conjointe inventée ; les compactions réellement visibles du codeur restent comptées séparément.

## 2. Types de messages et d'outils

| Rôle | Messages (% messages) |
| --- | --- |
| assistant | 105 (75.5 %) |
| user | 34 (24.5 %) |
| Total | 139 (100.0 %) |

| Type de partie | Occurrences (% parties) |
| --- | --- |
| reasoning | 105 (21.0 %) |
| step-finish | 104 (20.8 %) |
| step-start | 105 (21.0 %) |
| text | 106 (21.2 %) |
| tool | 79 (15.8 %) |
| Total | 499 (100.0 %) |

| Terminaison assistant | Messages (% assistants) |
| --- | --- |
| absent | 1 (1.0 %) |
| stop | 33 (31.4 %) |
| tool-calls | 71 (67.6 %) |
| Total | 105 (100.0 %) |

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| bash | 17 (21.5 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |
| cgpt-validation_broker_readiness | 2 (2.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 (1.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (2.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 10 (12.7 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 29 (36.7 %) | 19 (65.5 %) | 0 (0.0 %) | 10 (34.5 %) |
| edit | 2 (2.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 2 (2.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 6 (7.6 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (10.1 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 79 (100.0 %) | 65 (82.3 %) | 0 (0.0 %) | 14 (17.7 %) |

## 3. Fichiers modifiés

Tentatives natives visibles, pas des lignes modifiées ni une déduction depuis Git. Les artefacts OpenSpec du change et les trois fichiers de code/tests sont inclus ; le correctif d'indentation est une tentative distincte.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-classification-vocabulary/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-classification-vocabulary/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-classification-vocabulary/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-classification-vocabulary/specs/data-governance/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-classification-vocabulary/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_governance.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_governance_vocabulary_integration.py | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_governance_vocabulary.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100.0 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Archivage : 5 fichiers déplacés, empreintes vérifiées ; specsUpdated=false et zéro opération normative. Les 76 specs canoniques et les fichiers de référence restent inchangés. Le déplacement n'est pas compté comme six éditions natives. Ce rapport est produit ensuite sous un mandat distinct, hors intervalle.

## 4. Commandes

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| OpenSpec | 10 (58.8 %) | 6 (60.0 %) | 0 (0.0 %) | 4 (40.0 %) |
| Prévol true | 1 (5.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 6 (35.3 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 (100.0 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |

Les résultats CLI globaux exit 1 et erreurs/interruption MCP sont conservés comme erreurs techniques, distinctes des refus CAB. Les demandes rejetées sans outil Bash ne sont pas des commandes exécutées.

Commandes natives refusées visibles : 0 ; taux sur refus N/A (dénominateur nul).

## 5. Accès web

Codeur : 0 appel web visible. URL refusées : aucune observée. Taux sur accès web N/A en l'absence d'appel.

Orchestrateur : échanges locaux OpenCode/CAB via http://127.0.0.1:4096 et http://127.0.0.1:8788 ; contrôle de quotas fournisseur autorisé séparément. Nombre exhaustif HTTP et télémétrie d'outils orchestrateur : N/A. Aucun secret affiché, analysé ni ajouté aux livrables.

## 6. Synthèse globale

| Durée de session de codage | Valeur |
| --- | --- |
| Début | 2026-10-06T09:59:08.284000+00:00 |
| Fin après archive et sondes | 2026-10-06T11:11:17.671743+00:00 |
| Durée globale, pauses incluses | 01 h 12 min 09 s |

| Quota Codex sur 7 jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-06T09:59:08.284000+00:00 | N/A — outil natif get_usage_limits non exposé | N/A |
| Après | 2026-10-06T11:11:17.671743+00:00 | N/A — outil natif get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

Les quotas sont partagés par le compte ; une différence éventuelle n'aurait pas d'attribution exclusive à cette session. Aucune conversion en tokens ou euros.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| autres | 52 (65.8 %) | 42 (80.8 %) | 0 (0.0 %) | 10 (19.2 %) |
| commandes | 17 (21.5 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |
| fichiers | 10 (12.7 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 79 (100.0 %) | 65 (82.3 %) | 0 (0.0 %) | 14 (17.7 %) |

Totaux recoupés par outil, fichier et famille de commande. Les totaux de l'orchestrateur sont N/A ; aucune extrapolation.

Tests : 27 réussis ; trois compilations réussies. Archivage : exit 0, 5 fichiers vérifiés, zéro opération normative. Livraison : vocabulaire structurel de deux dimensions, sans classification automatique, profil complet, décision d'export ni runtime. Git : non inspecté, aucun commit/push. PostgreSQL : autorisé, non nécessaire à ce vocabulaire pur, aucun test base exécuté.
