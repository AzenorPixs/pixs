# Statistiques — add-initial-data-subject-request-operations-vocabulary

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-data-subject-request-operations-vocabulary. RUN : cismp-pixs-20261005-2654fe47.

Intervalle : 2026-10-06T12:54:17.420311+00:00 → 2026-10-06T14:01:19.250466+00:00. Pauses et attentes incluses ; production de ce rapport exclue.

La sélection préalable, terminée avant la sonde initiale, est exclue de cet intervalle. Les coûts et comptes de production ci-dessous ne couvrent que ce change.

Couverture : messages accessibles de la seule session maîtresse ses_eefa39c24ffe1dGvdToTr4NfJh dans cet intervalle, bornes incluses. Les autres changes et les sessions de sondes sont exclus des totaux de production. Les compteurs de l'orchestrateur non exposés sont N/A.

Registre de preuves : output/cismp-state.json, branche data_subject_operations_cycle. Archive native : message msg_11183249c001j0lpQqBf1yYYcx, part prt_111835db3001Gf92I7u5isj8GC. Tests : cismp-20261006-operations-unit-6d81a830, cismp-20261006-operations-integration-68c0a776, cismp-20261006-operations-regressions-3e4c4544.

Convention : une réussite technique d'outil ne prouve ni la conformité du contenu ni une approbation ; les décisions CAB sont comptées séparément. Un exit CLI 1 reste une erreur de résultat même lorsque les 19 WARNING connus sont qualifiés pour le cycle. Les refus explicites restent distincts des erreurs et interruptions.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A — version non exposée | opencode-go | xhigh | N/A — aucune sonde fixe valide | N/A — aucune sonde fixe valide | 171.064 s observées ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex /root | N/A — télémétrie exacte indisponible | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — génération non exposée |

Temps du codeur : somme des intervalles horodatés des parties text/reasoning, hors outils et attentes. Dénominateur de service de tous les agents inconnu : part N/A. La qualification PLLM antérieure est une mesure distincte, exclue des moyennes de sondes de ce change.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Durée du change | 01 h 07 min 01 s |
| Messages | 119 |
| Appels outils | 58 |
| Tokens entrée hors cache | 528 |
| Tokens sortie | 35583 |
| Tokens raisonnement exposés | 0 |
| Cache lu | 43785878 |
| Cache écrit | 80689 |
| Coût production USD | 0.733515058 |
| Compactions observées | 0 |

| Décision CAB finale observée | Mandats distincts (% décisions) |
| --- | --- |
| APPROVED | 26 (100.0 %) |
| Total | 26 (100.0 %) |

Résultat : 6/6 tâches prouvées ; 46/46 tests réussis ; trois compilations exit 0. Strict du change et de data-governance : exit 0 avant et après code. Les quatre contrôles globaux retournent réellement 1, uniquement sur les 19 WARNING de longueur qualifiés ; aucune ERROR ni autre issue. Empreintes de référence inchangées.

Incident CAB avant création : un résumé de design dépassait le plafond serveur de 2000 caractères. Le get_approval réel a confirmé l'identifiant inconnu. Même opération resoumise après réduction du résumé, seule demande réellement créée approuvée par root avant un write unique. Les erreurs de schéma et transport, les tailles de résumés observées et le rapport initial de taille erroné sont conservés dans le registre. Aucun écart de contenu observé lors des créations.

### Sondes et surcharge

Prompt fixe de 48 lignes, même modèle et xhigh, sessions jetables sans outil ni accès projet. Chaque sortie est contrôlée exactement ; aucune moyenne n'est fabriquée pour une sortie divergente.

| Position | Envoi UTC | Statut | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- |
| début vocabulaire opérations | 2026-10-06T12:54:17.420311+00:00 | failed | 2572 | 0.00358014 |
| +30 min | 2026-10-06T13:24:17.844125+00:00 | failed | 1317 | 0.00299029 |
| +60 min | 2026-10-06T13:54:18.295378+00:00 | failed | 609 | 0.00265753 |
| fin vocabulaire opérations | 2026-10-06T14:00:15.883006+00:00 | failed | 1234 | 0.00295128 |

| Statut sonde | Occurrences (% sondes) |
| --- | --- |
| failed | 4 (100.0 %) |
| Total | 4 (100.0 %) |

| Surcharge télémétrie séparée | Valeur |
| --- | --- |
| Tokens sortie | 5732 |
| Coût connu USD | 0.012179240 |
| Moyennes de performance | N/A — sorties fixes invalides |

Compactage conjoint périodique : incomplet, API native de compactage de l'orchestrateur non exposée. Aucun agent auxiliaire substitué, aucune réussite conjointe inventée ; les compactions réellement visibles du codeur restent comptées séparément.

Orchestrateur : une tentative de mémoriser une fonction non sérialisable a échoué avant tout appel d'outil ou mutation. La préparation suivante a utilisé des textes sérialisables. Les compteurs exhaustifs restent N/A. Aucun incident de la session précédente n'est imputé à ce cycle.

Écart d'exécution au cochage : le mandat dcb1d15d prescrivait les littéraux intégraux de tasks.md ; l'edit natif prt_11178cf28001EfDB41BWs2scIV a utilisé le seul bloc des six tâches. Le fichier final est exactement conforme et le contrôle root a détecté l'écart des arguments. Mandat gelé, session interrompue, READY/pending zéro et approbation réellement relus ; rapport corrigé msg_1117df4b7001AJPvaupEbePyyK. Écriture non répétée, aucune correction de fichier nécessaire, test CAB neuf /usr/bin/true exit 0 avant le strict final. Ce mandat est quarantiné et réconcilié, sans déclaration d'exécution littérale conforme. L'edit reste une réussite technique dans les compteurs, distincte de sa conformité.

## 2. Types de messages et d'outils

| Rôle | Messages (% messages) |
| --- | --- |
| assistant | 88 (73.9 %) |
| user | 31 (26.1 %) |
| Total | 119 (100.0 %) |

| Type de partie | Occurrences (% parties) |
| --- | --- |
| reasoning | 88 (21.3 %) |
| step-finish | 88 (21.3 %) |
| step-start | 88 (21.3 %) |
| text | 92 (22.2 %) |
| tool | 58 (14.0 %) |
| Total | 414 (100.0 %) |

| Terminaison assistant | Messages (% assistants) |
| --- | --- |
| stop | 31 (35.2 %) |
| tool-calls | 57 (64.8 %) |
| Total | 88 (100.0 %) |

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| bash | 17 (29.3 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |
| cgpt-validation_broker_readiness | 1 (1.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 (3.4 %) | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| cgpt-validation_list_pending | 1 (1.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (1.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 27 (46.6 %) | 25 (92.6 %) | 0 (0.0 %) | 2 (7.4 %) |
| edit | 1 (1.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (13.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 58 (100.0 %) | 51 (87.9 %) | 0 (0.0 %) | 7 (12.1 %) |

## 3. Fichiers modifiés

Tentatives natives visibles, pas des lignes modifiées ni une déduction depuis Git. Les artefacts OpenSpec du change et les trois fichiers de code/tests sont inclus ; les essais de création sont comptés séparément des décisions CAB.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-operations-vocabulary/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-operations-vocabulary/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-operations-vocabulary/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-operations-vocabulary/specs/data-governance/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-operations-vocabulary/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_subject_operations.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_subject_operations_vocabulary_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_subject_operations_vocabulary.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

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
| Début | 2026-10-06T12:54:17.420311+00:00 |
| Fin après archive et sondes | 2026-10-06T14:01:19.250466+00:00 |
| Durée globale, pauses incluses | 01 h 07 min 01 s |

| Quota Codex sur 7 jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-06T12:54:17.420311+00:00 | N/A — outil natif get_usage_limits non exposé | N/A |
| Après | 2026-10-06T14:01:19.250466+00:00 | N/A — outil natif get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

| Quota fournisseur observé UTC | Rolling utilisé (%) | Weekly utilisé (%) | Monthly utilisé (%) | Statut |
| --- | --- | --- | --- | --- |
| 2026-10-06T13:16:17.379447+00:00 | 19 | 44 | 42 | OK |
| 2026-10-06T13:53:35.062454+00:00 | 25 | 47 | 43 | OK |
| 2026-10-06T14:00:16.709942+00:00 | 27 | 47 | 44 | OK |

Les quotas sont partagés par le compte ; une différence éventuelle n'aurait pas d'attribution exclusive à cette session. Aucune conversion en tokens ou euros.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| autres | 32 (55.2 %) | 29 (90.6 %) | 0 (0.0 %) | 3 (9.4 %) |
| commandes | 17 (29.3 %) | 13 (76.5 %) | 0 (0.0 %) | 4 (23.5 %) |
| fichiers | 9 (15.5 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 58 (100.0 %) | 51 (87.9 %) | 0 (0.0 %) | 7 (12.1 %) |

Totaux recoupés par outil, fichier et famille de commande. Les totaux de l'orchestrateur sont N/A ; aucune extrapolation.

Tests : 46 réussis ; trois compilations réussies. Archivage : exit 0, 5 fichiers vérifiés, zéro opération normative. Livraison partielle : vocabulaire fermé des cinq opérations relatives aux données. DataSubjectRequest complet, autorisation, audit, idempotence, propagation, holds, rétention et runtime ne sont pas implémentés par ce change. Git : non inspecté, aucun commit/push. PostgreSQL : autorisé, non nécessaire à ce vocabulaire pur, aucun test base exécuté.
