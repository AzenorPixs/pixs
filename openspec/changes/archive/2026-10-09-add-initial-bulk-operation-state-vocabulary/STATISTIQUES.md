# STATISTIQUES — add-initial-bulk-operation-state-vocabulary

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go (opencode-go) | xhigh | 3.0 s | 105.1 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 (famille déclarée de Codex) | N/A | OpenAI | N/A | N/A | N/A | N/A |

OpenCode observé : 1.18.35. Version exacte du LLM et durées actives de génération non exposées : N/A. Aucun dénominateur de temps de service ni ratio ne peut être calculé. La durée calendaire, les outils et les attentes ne sont pas assimilés à de la génération. L’orchestrateur n’a pas été sondé.

## 1. Statistiques générales et décisions

Intervalle du change : 2026-10-09T17:05:46.063757+02:00 → 2026-10-09T17:34:31.128421+02:00, durée 00 h 28 min 45 s, pauses, récupération et attentes incluses. L’historique API complet des deux sessions a été lu ; les agrégats retiennent les messages créés dans ces bornes. La préparation NFDOC et la RSMP antérieures sont hors intervalle ; la publication du présent rapport est postérieure et distincte.

Sessions de codage : ses_edeed7e59ffep3KKWjtS3obNej, ses_edec0de2effeiOD0JuRWIPSMMu. Même RUN parent cismp-pixs-758862ec875d4708.

Résultat : Enum BulkOperationState à dix noms=valeurs, trois Enum et façade préservés. Compilation et import neuf codes 0, revue AST de déclarations seules, 20 tests réussis, validation stricte avant et après code 1/1 codes 0. Archive openspec/changes/archive/2026-10-09-add-initial-bulk-operation-state-vocabulary, code 0, sans synchronisation normative. Les 76 spécifications sont identiques à la baseline post-RSMP validée 76/76, zéro issue, code 0.

Les pourcentages sont arrondis indépendamment à une décimale ; leur somme peut valoir 99,9 % ou 100,1 %. Les nombres entiers et les totaux sont la référence.

Convention des outils : « approuvé et exécuté » désigne un appel terminé avec succès sous ses permissions applicables ; cela ne prouve pas une approbation manuelle. Un résultat MCP réussi peut transporter un refus CAB. Les refus explicites sont séparés des erreurs techniques, interruptions et délais.

| Résultat des appels d’outils | Nombre | Part |
|---|---:|---:|
| Approuvés et exécutés | 43 | 89.6 % |
| Refusés | 1 | 2.1 % |
| Erreurs techniques | 4 | 8.3 % |
| Total | 48 | 100 % |

| Tentatives de mandat clôturées dans l’intervalle | Nombre | Part |
|---|---:|---:|
| Annulées sans exécution | 1 | 5.9 % |
| Approuvées et exécutées, preuves vérifiées | 14 | 82.4 % |
| Type MCP invalide, aucune approbation créée | 1 | 5.9 % |
| Refus CAB avant exécution | 1 | 5.9 % |
| Total tentatives | 17 | 100 % |

Incidents conservés : garde de 2 150 caractères dépassant la limite de transport CAB de 2 000, annulée sans exécution ; commande réécrite refusée avant exécution ; récupération native du même job vers une nouvelle session avec prévol exact /usr/bin/true, permission once et exit 0 ; argument commands mal typé refusé par le schéma MCP avant création ; permission glob annulée avant rétablissement des recherches autorisées. La compilation et les éditions prouvées n’ont pas été rejouées. Le compte modèle 19 tests a été corrigé par la sortie native « Ran 20 tests … OK ». Les variations de title/summary ont été examinées séparément ; aucune variation de cible n’a été approuvée.

| Tokens natifs des réponses de production | Valeur | Part du total natif |
|---|---:|---:|
| Entrée hors cache | 372 | 0.0 % |
| Sortie | 27012 | 0.5 % |
| Raisonnement (champ natif) | 0 | 0.0 % |
| Cache lu | 5500119 | 95.9 % |
| Cache écrit | 209218 | 3.6 % |
| Total natif | 5736721 | 100 % |

64 réponses avec relevé tokens ; coût télémétrique cumulé 0.14259694 sur 64 réponses, unité non exposée. Aucune conversion en euros ni attribution au quota Codex. Compactions exécutées : aucune pendant cet intervalle inférieur à 1 h 30 ; aucune réussite native inventée.

| Sondes dédiées du change | Envoi | TTMT | Tokens/s | Sortie | Résultat |
|---|---|---:|---:|---:|---|
| début | 2026-10-09T17:05:46.180936+02:00 | 4.1 s | 115.2 | 328 | valide |
| fin après archive | 2026-10-09T17:32:55.906816+02:00 | 1.9 s | 95.1 | 331 | valide |

Sondes : 2 prévues, 2 réussies (100.0 %), 0 échouées (0.0 %), 0 manquée. Aucune échéance de 30 minutes n’est survenue avant la fin de l’activité ; aucune attente artificielle. Deux sondes d’analyse antérieures, non conformes et hors intervalle, ne sont pas recyclées.
TTMT min/max : 1.9/4.1 s ; débit min/max : 95.1/115.2 tokens/s. Moyennes arithmétiques sur les seules sondes valides.
Prompt fixe de ce change : Écris exclusivement tous les nombres entiers de 1 à 100 séparés par un espace, sur une seule ligne, sans texte ni ellipse.
Mesure : premier delta SSE non vide moins envoi ; débit = tokens de sortie de l’API divisés par la durée entre premier et dernier delta. Sessions jetables sans outil, fichier ou réseau de l’agent sondé, supprimées après contrôle. Surcharge séparée : 659 tokens de sortie, 12.988 s calendaires, coût natif 0.00455033, unité non exposée ; exclus de la production.

## 2. Types de messages et d’outils

| Rôle de message exposé | Nombre | Part |
|---|---:|---:|
| assistant | 64 | 74.4 % |
| user | 22 | 25.6 % |
| Total | 86 | 100 % |

Messages système injectés et historique propre de Codex non exposés par cette API : N/A, non assimilés à zéro.

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 63 | 22.7 % |
| step-finish | 62 | 22.4 % |
| step-start | 63 | 22.7 % |
| text | 41 | 14.8 % |
| tool | 48 | 17.3 % |
| Total | 277 | 100 % |

| Terminaison des réponses assistant | Nombre | Part |
|---|---:|---:|
| non exposé / interrompu | 2 | 3.1 % |
| stop | 19 | 29.7 % |
| tool-calls | 43 | 67.2 % |
| Total | 64 | 100 % |

| Type d’outil | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| bash | 8 (16.7 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 4 (8.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 (2.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 5 (10.4 %) | 4 (80.0 %) | 0 (0.0 %) | 1 (20.0 %) |
| cgpt-validation_list_pending | 1 (2.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (2.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 17 (35.4 %) | 14 (82.4 %) | 0 (0.0 %) | 3 (17.6 %) |
| edit | 2 (4.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 1 (2.1 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| read | 4 (8.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 4 (8.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 48 (100.0 %) | 43 (89.6 %) | 1 (2.1 %) | 4 (8.3 %) |

## 3. Fichiers modifiés

Tentatives d’écriture natives de l’intervalle, chemins absolus complets. Les déplacements par archive ne sont pas comptés comme de nouvelles écritures. Les deux fichiers RSMP ont été modifiés avant cet intervalle et figurent dans l’état parent.

| Chemin absolu | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-state-vocabulary/design.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-state-vocabulary/proposal.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-state-vocabulary/specs/bulk-operations/spec.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-state-vocabulary/tasks.md | 2 (33.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operations.py | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total écritures | 6 (100.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Quatre artefacts OpenSpec déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-09-add-initial-bulk-operation-state-vocabulary. Le rapport STATISTIQUES.md est une publication distincte après la borne finale et n’est pas ajouté rétroactivement à ces compteurs.

## 4. Commandes

| Famille native | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| Aide CLI archive | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archivage | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Import neuf | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol récupération | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Régressions unittest | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total commandes natives | 8 (100.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées avant appel Bash, déjà incluses dans les décisions CAB et non ajoutées une seconde fois au total d’outils :

| Commande (100 caractères maximum) | Occurrences refusées | Part des commandes refusées |
|---|---:|---:|
| /home/devops/datas/pixs/.venv/bin/python3 -c 'import ast,json,sys from pathlib import Path sys.path… | 1 | 100.0 % |

La commande trop longue a été annulée, non refusée par une décision CAB ; la soumission de type MCP invalide n’a créé aucun mandat. Aucun test en échec n’est masqué dans ces catégories.

## 5. Accès web

| Domaine web de l’agent de codage | Total | Approuvé/exécuté | Refusé | Erreur |
|---|---:|---:|---:|---:|
| webfetch / websearch | 0 | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun appel web de l’agent ni URL web visitée ou refusée observé dans l’intervalle. Les échanges de contrôle locaux http://127.0.0.1:4096 et http://127.0.0.1:8788, et les appels fournisseur inhérents au modèle, sont de l’instrumentation distincte ; leur nombre complet n’est pas exposé : N/A. Ils ne sont pas présentés comme des visites web.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-09T17:05:46.063757+02:00 |
| Fin — après archivage et sonde finale | 2026-10-09T17:34:31.128421+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 28 min 45 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-09T17:05:46.063757+02:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-09T17:34:31.128421+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux bornes : aucune mesure reconstituée, aucun quota fournisseur substitué. Les quotas Codex sont partagés par le compte ; une différence, si disponible, pourrait inclure d’autres tâches simultanées et ne serait pas attribuable exclusivement à ce change sans preuve.

| Domaine d’outils | Total et part globale | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| Fichiers | 6 (12.5 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 8 (16.7 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 34 (70.8 %) | 29 (85.3 %) | 1 (2.9 %) | 4 (11.8 %) |
| Total général | 48 (100.0 %) | 43 (89.6 %) | 1 (2.1 %) | 4 (8.3 %) |

20 tests réussis, compilation/import et validations strictes codes 0, archive prouvée ; artefacts et canon vérifiés par empreintes et contenu exact. Aucun commit, push ou examen de l’état Git. PostgreSQL et navigateur non nécessaires et non exécutés pour cette unité déclarative. Aucune lecture de fichier sensible observée dans les outils du codage ; les accès fournisseur restent dans leur processus sécurisé et le stockage natif privé. Ce change ne fournit aucun runtime, transition, ordre sémantique, terminalité, Job, import/export ni persistance. Le cycle CISMP parent poursuit sa sélection après vérification de ce rapport et n’est pas déclaré globalement terminé.
