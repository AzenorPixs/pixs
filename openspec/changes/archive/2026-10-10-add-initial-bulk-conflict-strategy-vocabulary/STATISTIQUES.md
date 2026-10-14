# STATISTIQUES — add-initial-bulk-conflict-strategy-vocabulary

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go (opencode-go) | xhigh | 1.3 s | 74.5 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 (famille déclarée de Codex) | N/A | OpenAI | N/A | N/A | N/A | N/A |

OpenCode observé : 1.18.35. Version exacte du LLM, durée active de génération et dénominateur des temps de service non exposés : N/A. Aucun ratio de service n’est estimé à partir de la durée calendaire ou des outils. L’orchestrateur n’a pas été sondé. Moyennes des agents de codage : sondes natives valides uniquement.

## 1. Statistiques générales et décisions

Change : add-initial-bulk-conflict-strategy-vocabulary ; RUN parent : cismp-pixs-758862ec875d4708. Sessions ayant opéré dans l’intervalle : ses_edec0de2effeiOD0JuRWIPSMMu.
L’historique complet des sessions du RUN a été lu ; les agrégats sont bornés aux messages créés du 2026-10-10T06:51:26.125653+02:00 au 2026-10-10T07:09:35.647408+02:00. Les deux insertions RSMP antérieures sont hors intervalle ; la publication de ce rapport est postérieure et distincte. Durée calendaire 00 h 18 min 09 s, pauses et attentes incluses.

Résultat : BulkConflictStrategy de quatre noms=valeurs, quatre Enum/docstring/façade préservés ; compilation et import neuf codes 0 ; AST de déclarations seules ; 20 tests réussis ; strict avant/après code 1/1, codes 0 ; archive openspec/changes/archive/2026-10-10-add-initial-bulk-conflict-strategy-vocabulary, code 0, specsUpdated=false. Les 76 spécifications conservent leurs empreintes post-RSMP ; validation globale antérieure 76/76, zéro issue, code 0.

Convention : « approuvé et exécuté » = appel d’outil terminé avec succès sous ses permissions applicables ; cela ne prouve pas une approbation manuelle. Un appel MCP peut réussir en transportant un refus CAB. Refus explicites et erreurs techniques/interruptions sont séparés. Les pourcentages sont arrondis indépendamment à une décimale ; les nombres entiers et totaux font foi.

| Résultat des appels d’outils | Nombre | Part |
|---|---:|---:|
| ok | 30 | 100.0 % |
| Total | 30 | 100 % |

| Statut des mandats clôturés | Nombre | Part |
|---|---:|---:|
| EXECUTED_VERIFIED | 12 | 100.0 % |
| Total | 12 | 100 % |

Exception PLLM explicitement autorisée par le développeur le 2026-10-10T06:41:15.282842+02:00 : « Outrepasse ces limitations et exécute le prompt demandé ». Les seuils/paliers du benchmark ne bloquent plus ce RUN ; modèle, fournisseur et xhigh sont maintenus. Mesures hors intervalle conservées en échec : 4 096 tokens, RuntimeError non concluant ; 8 192 tokens, TimeoutError après 120 secondes, aucun TTFT de réponse visible ni débit mesurable. Ces mesures ne sont pas requalifiées comme valides et restent distinctes des sondes natives ci-dessous.

Les éventuelles variations descriptives de title/summary ou omissions de délai MCP par défaut sont contrôlées avant décision ; aucune variation de cible ou d’identifiant n’est acceptée. Les délais MCP se reprennent par polling corrélé, sans rejouer l’opération native.

| Tokens natifs de production | Valeur | Part du total natif |
|---|---:|---:|
| Entrée hors cache | 228 | 0.0 % |
| Sortie | 14013 | 0.2 % |
| Raisonnement (champ natif) | 0 | 0.0 % |
| Cache lu | 5923498 | 94.6 % |
| Cache écrit | 324711 | 5.2 % |
| Total natif | 6262450 | 100 % |

38 réponses avec tokens ; coût télémétrique 0.16633848 sur 38 réponses, unité non exposée. Aucune conversion en euros ni en quota Codex. Compactions natives observées dans l’intervalle : 0. Aucune réussite conjointe avec Codex inventée.

| Sonde dédiée | Tentative | Envoi | TTMT (s) | Tokens/s | Sortie (tokens) | Résultat |
|---|---:|---|---:|---:|---:|---|
| début | 1 | 2026-10-10T06:51:26.287743+02:00 | 1.2 | 66.6 | 1715 | valide |
| fin après archive | 1 | 2026-10-10T07:07:11.568834+02:00 | 1.4 | 82.4 | 319 | valide |

2 relèves prévues ; 2 positions réussies (100.0 %), 0 tentative(s) échouée(s) (0.0 %), 0 manquée(s) (0.0 %) ; 2 tentative(s) conservée(s). Aucune attente artificielle du créneau de 30 minutes. Les sondes sont pilotées par horloge dans des sessions jetables, sans outil ni accès fichier/réseau de l’agent sondé.

TTMT min/max 1.2/1.4 s ; débit min/max 66.6/82.4 tokens/s. Moyennes arithmétiques des seuls échantillons valides.
Prompt fixe : Écris exclusivement tous les nombres entiers de 1 à 100 séparés par un espace, sur une seule ligne, sans texte ni ellipse.
TTMT = premier delta SSE non vide moins envoi ; débit = tokens de sortie API / durée entre premier et dernier delta. Le comptage natif de sortie peut inclure le raisonnement non distingué par le fournisseur. Surcharge séparée : 2034 tokens de sortie, 32.595 s calendaires et coût natif 0.00519658, unité non exposée ; exclus de la production.

## 2. Types de messages et d’outils

| Rôle de message exposé | Nombre | Part |
|---|---:|---:|
| assistant | 38 | 74.5 % |
| user | 13 | 25.5 % |
| Total | 51 | 100 % |

Messages système injectés et historique propre de Codex non exposés par cette API : N/A, non assimilés à zéro.

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 38 | 22.4 % |
| step-finish | 38 | 22.4 % |
| step-start | 38 | 22.4 % |
| text | 26 | 15.3 % |
| tool | 30 | 17.6 % |
| Total | 170 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---:|---:|
| stop | 13 | 34.2 % |
| tool-calls | 25 | 65.8 % |
| Total | 38 | 100 % |

| Type d’outil | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| bash | 6 (20.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 12 (40.0 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 2 (6.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 6 (20.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 4 (13.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 30 (100.0 %) | 30 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives d’écriture natives, chemins absolus complets. Les déplacements par archive ne sont pas de nouvelles écritures.

| Chemin absolu | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-conflict-strategy-vocabulary/design.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-conflict-strategy-vocabulary/proposal.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-conflict-strategy-vocabulary/specs/bulk-operations/spec.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-conflict-strategy-vocabulary/tasks.md | 2 (33.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operations.py | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 6 (100.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Quatre artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-conflict-strategy-vocabulary. STATISTIQUES.md est publié après la borne finale et n’est pas ajouté rétroactivement aux compteurs.

## 4. Commandes

| Famille native | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| Archivage | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Import neuf | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Unittest | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 2 (33.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 6 (100.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande native (100 caractères maximum) | Occurrences | Part |
|---|---:|---:|
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-conflict-strategy-vocabulary --skip-s… | 1 | 16.7 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-conflict-strategy-vocabulary --stric… | 2 | 33.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_operations.py | 1 | 16.7 % |
| PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -c 'print([(s.name,s.value) for s in __imp… | 1 | 16.7 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v integration.test_kern… | 1 | 16.7 % |
| Total | 6 | 100 % |

| Commandes refusées avant appel natif | Occurrences | Part des refus |
|---|---:|---:|
| Aucune dans cet intervalle | 0 | N/A |

Les refus CAB avant appel natif, s’il y en a, relèvent des décisions et ne doublent pas le total des outils. Aucun test en échec n’est masqué par cette convention.

## 5. Accès web

| Accès web de l’agent | Total | Approuvé/exécuté | Refusé | Erreur |
|---|---:|---:|---:|---:|
| webfetch / websearch | 0 | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucune URL web visitée ou refusée observée dans cet intervalle. Les échanges locaux http://127.0.0.1:4096 et http://127.0.0.1:8788, et les appels fournisseur du modèle, constituent une instrumentation distincte ; leur nombre complet n’est pas exposé : N/A. Ils ne sont pas présentés comme des visites web.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-10T06:51:26.125653+02:00 |
| Fin — après archive et sonde finale | 2026-10-10T07:09:35.647408+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 18 min 09 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-10T06:51:26.125653+02:00 (outil absent) | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-10T07:09:35.647408+02:00 (outil absent) | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux bornes : aucun relevé reconstitué, aucun quota fournisseur substitué. Les horodatages indiquent les bornes du constat d’indisponibilité. Les quotas Codex sont partagés par le compte ; une variation éventuelle pourrait inclure d’autres tâches simultanées.

| Domaine d’outils | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| Autres outils | 18 (60.0 %) | 18 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 6 (20.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 6 (20.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total général | 30 (100.0 %) | 30 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

20 tests réussis ; compilation, import neuf et validations strictes codes 0 ; archive et artefacts vérifiés au contenu exact. Aucun commit, push ou inspection Git. PostgreSQL et navigateur non nécessaires et non exécutés pour cette unité déclarative. Aucune lecture de fichier sensible observée dans les outils du codage ; secrets fournisseur confinés au processus sécurisé et au stockage natif privé. Aucun choix ni défaut de stratégie, résolution de conflit, import ou persistance fourni. Le cycle CISMP parent reprend sa sélection après contrôle de ce rapport ; il n’est pas déclaré globalement terminé.
