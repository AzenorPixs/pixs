# Statistiques — add-initial-data-governance-profile-representation

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-data-governance-profile-representation. RUN : cismp-pixs-20261005-2654fe47.

Intervalle : 2026-10-06T11:30:41.303152+00:00 → 2026-10-06T12:44:14.811952+00:00. Pauses et attentes incluses ; production de ce rapport exclue.

Couverture : messages accessibles de la seule session maîtresse ses_eefa39c24ffe1dGvdToTr4NfJh dans cet intervalle, bornes incluses. Les autres changes et les sessions de sondes sont exclus des totaux de production. L'analyse de sélection antérieure au début du cycle est exclue. Les compteurs de l'orchestrateur non exposés sont N/A.

Registre de preuves : output/cismp-state.json, branche data_governance_profile_cycle. Archive native : message msg_1113c1fcf001KL3Pptb4m8VTuF, part prt_1113c53fb001dgZ43xcCOH6NQ0. Tests : cismp-20261006-profile-unit-3ccf900c, cismp-20261006-profile-integration-2c1cea5d, cismp-20261006-profile-regressions-91922269.

Convention : une réussite technique d'outil ne prouve ni la conformité du contenu ni une approbation ; les décisions CAB sont comptées séparément. Un exit CLI 1 reste une erreur de résultat même lorsque les 19 WARNING connus sont qualifiés pour le cycle. Les refus explicites restent distincts des erreurs et interruptions.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A — version non exposée | opencode-go | xhigh | N/A — aucune sonde fixe valide | N/A — aucune sonde fixe valide | 340.825 s observées ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex /root | N/A — télémétrie exacte indisponible | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — génération non exposée |

Temps du codeur : somme des intervalles horodatés des parties text/reasoning, hors outils et attentes. Dénominateur de service de tous les agents inconnu : part N/A. La qualification PLLM antérieure est une mesure distincte, exclue des moyennes de sondes de ce change.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Durée du change | 01 h 13 min 33 s |
| Messages | 125 |
| Appels outils | 62 |
| Tokens entrée hors cache | 558 |
| Tokens sortie | 56173 |
| Tokens raisonnement exposés | 0 |
| Cache lu | 35306043 |
| Cache écrit | 808527 |
| Coût production USD | 0.753087098 |
| Compactions observées | 0 |

| Décision CAB finale observée | Mandats distincts (% décisions) |
| --- | --- |
| APPROVED | 27 (100.0 %) |
| Total | 27 (100.0 %) |

Résultat : 6/6 tâches prouvées ; 92/92 tests réussis ; trois compilations exit 0. Strict du change et de data-governance : exit 0 avant et après code. Les quatre contrôles globaux retournent réellement 1, uniquement sur les 19 WARNING de longueur qualifiés ; aucune ERROR ni autre issue. Empreintes de référence inchangées.

Incident de contenu : une ligne vide approuvée a été omise lors du write unitaire. Root a gelé et aborté immédiatement à la détection, rapproché les preuves MCP et corrigé cette seule ligne sous mandat distinct. Contenu exact rétabli puis readiness READY/pending=0 et test CAB /usr/bin/true exit0 avant reprise. Aucun test ni opération hors récupération pendant le gel. Les timeouts MCP et le rapport initial d'exactitude erroné sont conservés ; le rapport a été corrigé sans rejeu du write. Aucun RSMP normatif ni extension de périmètre.

### Sondes et surcharge

Prompt fixe de 48 lignes, même modèle et xhigh, sessions jetables sans outil ni accès projet. Chaque sortie est contrôlée exactement ; aucune moyenne n'est fabriquée pour une sortie divergente.

| Position | Envoi UTC | Statut | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- |
| début profil gouvernance | 2026-10-06T11:30:41.303152+00:00 | failed | 557 | 0.00263309 |
| +30 min | 2026-10-06T12:00:41.706856+00:00 | failed | 5945 | 0.00516545 |
| +60 min | 2026-10-06T12:30:42.147794+00:00 | failed | 1270 | 0.0029682 |
| fin | 2026-10-06T12:43:07.772447+00:00 | failed | 559 | 0.00263403 |

| Statut sonde | Occurrences (% sondes) |
| --- | --- |
| failed | 4 (100.0 %) |
| Total | 4 (100.0 %) |

| Surcharge télémétrie séparée | Valeur |
| --- | --- |
| Tokens sortie | 8331 |
| Coût connu USD | 0.013400770 |
| Moyennes de performance | N/A — sorties fixes invalides |

Compactage conjoint périodique : incomplet, API native de compactage de l'orchestrateur non exposée. Aucun agent auxiliaire substitué, aucune réussite conjointe inventée ; les compactions réellement visibles du codeur restent comptées séparément.

Incidents orchestrateur : deux erreurs de préparation (syntaxe Python, chemin de diagnostics) corrigées avant les premiers mandats, sans écriture de source. Après compaction, un contrôle Python transmis au shell a échoué sans effet ; il a été réémis avec le bon interpréteur. Une lecture de script de quotas trop large a affiché des identifiants de compte ; aucune clé/jeton/mot de passe affiché, aucun identifiant recopié dans les livrables. La lecture suivante a été limitée à la fonction de quota et le lookup utilisé sans sortie sensible. Les compteurs exhaustifs de l'orchestrateur restent N/A.

## 2. Types de messages et d'outils

| Rôle | Messages (% messages) |
| --- | --- |
| assistant | 93 (74.4 %) |
| user | 32 (25.6 %) |
| Total | 125 (100.0 %) |

| Type de partie | Occurrences (% parties) |
| --- | --- |
| reasoning | 93 (21.3 %) |
| step-finish | 93 (21.3 %) |
| step-start | 93 (21.3 %) |
| text | 96 (22.0 %) |
| tool | 62 (14.2 %) |
| Total | 437 (100.0 %) |

| Terminaison assistant | Messages (% assistants) |
| --- | --- |
| stop | 32 (34.4 %) |
| tool-calls | 61 (65.6 %) |
| Total | 93 (100.0 %) |

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| bash | 17 (27.4 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |
| cgpt-validation_broker_readiness | 1 (1.6 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 (1.6 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 (1.6 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 5 (8.1 %) | 4 (80.0 %) | 0 (0.0 %) | 1 (20.0 %) |
| cgpt-validation_request_validation | 27 (43.5 %) | 24 (88.9 %) | 0 (0.0 %) | 3 (11.1 %) |
| edit | 2 (3.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (12.9 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 62 (100.0 %) | 54 (87.1 %) | 0 (0.0 %) | 8 (12.9 %) |

## 3. Fichiers modifiés

Tentatives natives visibles, pas des lignes modifiées ni une déduction depuis Git. Les artefacts OpenSpec du change et les trois fichiers de code/tests sont inclus ; le rétablissement d'une ligne vide est une tentative distincte.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-governance-profile-representation/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-governance-profile-representation/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-governance-profile-representation/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-governance-profile-representation/specs/data-governance/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-governance-profile-representation/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_governance_profile.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_governance_profile_integration.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_governance_profile.py | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100.0 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Archivage : 5 fichiers déplacés, empreintes vérifiées ; specsUpdated=false et zéro opération normative. Les 76 specs canoniques et les fichiers de référence restent inchangés. Le déplacement n'est pas compté comme des éditions natives. Ce rapport est produit ensuite sous un mandat distinct, hors intervalle.

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

Orchestrateur : échanges locaux OpenCode/CAB via http://127.0.0.1:4096 et http://127.0.0.1:8788 ; contrôle de quotas fournisseur autorisé séparément. Nombre exhaustif HTTP et télémétrie d'outils orchestrateur : N/A. Aucune valeur d'accès ou secret incluse dans les livrables ; relevés de quotas filtrés au statut et au pourcentage.

## 6. Synthèse globale

| Durée de session de codage | Valeur |
| --- | --- |
| Début | 2026-10-06T11:30:41.303152+00:00 |
| Fin après archive et sondes | 2026-10-06T12:44:14.811952+00:00 |
| Durée globale, pauses incluses | 01 h 13 min 33 s |

| Quota Codex sur 7 jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-06T11:30:41.303152+00:00 | N/A — outil natif get_usage_limits non exposé | N/A |
| Après | 2026-10-06T12:44:14.811952+00:00 | N/A — outil natif get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

| Quota fournisseur observé UTC | Rolling (%) | Weekly (%) | Monthly (%) | Statut |
| --- | --- | --- | --- | --- |
| 2026-10-06T12:26:03.564195+00:00 | 10 | 40 | 40 | OK |
| 2026-10-06T12:43:08.618409+00:00 | 14 | 42 | 41 | OK |

Les quotas sont partagés par le compte ; une différence éventuelle n'aurait pas d'attribution exclusive à cette session. Aucune conversion en tokens ou euros.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| autres | 35 (56.5 %) | 31 (88.6 %) | 0 (0.0 %) | 4 (11.4 %) |
| commandes | 17 (27.4 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |
| fichiers | 10 (16.1 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 62 (100.0 %) | 54 (87.1 %) | 0 (0.0 %) | 8 (12.9 %) |

Totaux recoupés par outil, fichier et famille de commande. Les totaux de l'orchestrateur sont N/A ; aucune extrapolation.

Tests : 92 réussis ; trois compilations réussies. Archivage : exit 0, 5 fichiers vérifiés, zéro opération normative. Livraison partielle : représentation interne des quinze champs du profil et validateur structurel fermé. Les obligations de publication, politique, résolution, contrôle des flux et runtime ne sont pas implémentées par ce change. Git : non inspecté, aucun commit/push. PostgreSQL : autorisé, non nécessaire à cette représentation structurelle pure, aucun test base exécuté.
