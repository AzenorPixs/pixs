# STATISTIQUES — add-initial-bulk-job-link-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go (opencode-go) | xhigh | 1.8 s | 76.6 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 (famille déclarée de Codex) | N/A | OpenAI | N/A | N/A | N/A | N/A |

OpenCode observé : 1.18.35. Version exacte du LLM, durée active de génération et dénominateur des temps de service non exposés : N/A. Aucun ratio de service n’est estimé à partir de la durée calendaire ou des outils. L’orchestrateur n’a pas été sondé. Moyennes des agents de codage : sondes natives valides uniquement.

## 1. Statistiques générales et décisions

Change : add-initial-bulk-job-link-v1 ; RUN parent : cismp-pixs-758862ec875d4708. Sessions ayant opéré dans l’intervalle : ses_edb9a6b14ffebZ7axAa0Jmv994, ses_edba7cd8effePoSNFr9uOaB5kY, ses_edbb72023ffe8CUSWQ2PqwtkOR.
L’historique complet des sessions du RUN a été lu ; les agrégats sont bornés aux messages créés du 2026-10-10T07:31:00.343814+02:00 au 2026-10-10T08:15:01.593159+02:00. Les deux insertions RSMP BulkJobLink et leurs validations appartiennent à cet intervalle ; la publication de ce rapport est postérieure et distincte. Durée calendaire 00 h 44 min 01 s, pauses et attentes incluses.

Résultat : BulkJobLink v1 interne, deux références explicites non vides distinctes, représentation immuable et validateur pur. Tests ciblés/frais et régressions : 29 tests réussis ; compilations et validations OpenSpec codes 0. Seul avertissement de longueur identifié et accepté suivant instruction développeur, aucune ERROR. Archive openspec/changes/archive/2026-10-10-add-initial-bulk-job-link-v1, code 0, specsUpdated=false ; les 76 spécifications conservent leurs empreintes post-RSMP.

Convention : « approuvé et exécuté » = appel d’outil terminé avec succès sous ses permissions applicables ; cela ne prouve pas une approbation manuelle. Un appel MCP peut réussir en transportant un refus CAB. Refus explicites et erreurs techniques/interruptions sont séparés. Les pourcentages sont arrondis indépendamment à une décimale ; les nombres entiers et totaux font foi.

| Résultat des appels d’outils | Nombre | Part |
|---|---:|---:|
| error | 2 | 1.8 % |
| ok | 111 | 97.4 % |
| refused | 1 | 0.9 % |
| Total | 114 | 100 % |

| Statut des mandats clôturés | Nombre | Part |
|---|---:|---:|
| CANCELLED_NO_EXECUTION | 1 | 4.5 % |
| EXECUTED_VERIFIED | 21 | 95.5 % |
| Total | 22 | 100 % |

Exception PLLM explicitement autorisée par le développeur le 2026-10-10T06:41:15.282842+02:00 : « Outrepasse ces limitations et exécute le prompt demandé ». Les seuils/paliers du benchmark ne bloquent plus ce RUN ; modèle, fournisseur et xhigh sont maintenus. Mesures hors intervalle conservées en échec : 4 096 tokens, RuntimeError non concluant ; 8 192 tokens, TimeoutError après 120 secondes, aucun TTFT de réponse visible ni débit mesurable. Ces mesures ne sont pas requalifiées comme valides et restent distinctes des sondes natives ci-dessous.

Incident de protocole dans cet intervalle : tentative Bash true hors mandat après validation préparatoire réussie ; permission refusée et session interrompue sans effet, empreintes conservées. Transfert contrôlé et prévol réservé dans nouvelle session avant reprise ; validation/code déjà prouvés non rejoués. Le refus explicite corrélé à la permission est compté comme tentative refusée, même si le texte natif indique Tool execution aborted.

Une purge technique des deux espaces CAB a été explicitement validée par le développeur après échec du transfert (409 preflight-permission-not-consumed). Sources, checkpoint et historiques natifs conservés ; nouveau broker réellement observé 0.86.8 et nouveau prévol exact réussi avant code. Les événements et outils antérieurs restent inclus via les historiques natifs des sessions, malgré purge des seuls états CAB.

Les éventuelles variations descriptives de title/summary ou omissions de délai MCP par défaut sont contrôlées avant décision ; aucune variation de cible ou d’identifiant n’est acceptée. Les délais MCP se reprennent par polling corrélé, sans rejouer l’opération native.

| Tokens natifs de production | Valeur | Part du total natif |
|---|---:|---:|
| Entrée hors cache | 714 | 0.0 % |
| Sortie | 65421 | 0.8 % |
| Raisonnement (champ natif) | 0 | 0.0 % |
| Cache lu | 7763229 | 94.1 % |
| Cache écrit | 417056 | 5.1 % |
| Total natif | 8246420 | 100 % |

120 réponses avec tokens ; coût télémétrique 0.23847783 sur 120 réponses, unité non exposée. Aucune conversion en euros ni en quota Codex. Compactions natives observées dans l’intervalle : 0. Aucune réussite conjointe avec Codex inventée.

| Sonde dédiée | Tentative | Envoi | TTMT (s) | Tokens/s | Sortie (tokens) | Résultat |
|---|---:|---|---:|---:|---:|---|
| début | 1 | 2026-10-10T07:31:09.572627+02:00 | 2.5 | 74.5 | 341 | valide |
| arrêt sur blocage, archive en attente | 1 | 2026-10-10T07:50:23.989602+02:00 | 1.8 | 70.3 | 323 | valide |
| +30 min | N/A | N/A | N/A | N/A | N/A | manquée |
| reprise après purge | 1 | 2026-10-10T08:01:26.897023+02:00 | 1.7 | 81.5 | 333 | valide |
| fin après archive | 1 | 2026-10-10T08:14:55.661617+02:00 | 1.4 | 80.2 | 344 | valide |

5 relèves prévues ; 4 positions réussies (80.0 %), 0 tentative(s) échouée(s) (0.0 %), 1 manquée(s) (20.0 %) ; 5 tentative(s) conservée(s). Aucune attente artificielle du créneau de 30 minutes. Les sondes sont pilotées par horloge dans des sessions jetables, sans outil ni accès fichier/réseau de l’agent sondé.

TTMT min/max 1.4/2.5 s ; débit min/max 70.3/81.5 tokens/s. Moyennes arithmétiques des seuls échantillons valides.
Prompt fixe : Écris exclusivement tous les nombres entiers de 1 à 100 séparés par un espace, sur une seule ligne, sans texte ni ellipse.
TTMT = premier delta SSE non vide moins envoi ; débit = tokens de sortie API / durée entre premier et dernier delta. Le comptage natif de sortie peut inclure le raisonnement non distingué par le fournisseur. Surcharge séparée : 1341 tokens de sortie, 25.559 s calendaires et coût natif 0.00522576, unité non exposée ; exclus de la production.

Deux erreurs techniques restent visibles : une lecture de chemin erroné src/pixs/diagnostics/__init__.py (fichier absent), corrigée par lecture du chemin kernel/diagnostics existant, et le timeout MCP du prévol divergent. La tentative Bash true hors mandat est classée refusée via la permission explicitement rejetée ; elle n'a pas été exécutée. Aucun test de code n'a échoué.

## 2. Types de messages et d’outils

| Rôle de message exposé | Nombre | Part |
|---|---:|---:|
| assistant | 120 | 80.0 % |
| user | 30 | 20.0 % |
| Total | 150 | 100 % |

Messages système injectés et historique propre de Codex non exposés par cette API : N/A, non assimilés à zéro.

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 120 | 22.4 % |
| step-finish | 119 | 22.2 % |
| step-start | 120 | 22.4 % |
| text | 63 | 11.8 % |
| tool | 114 | 21.3 % |
| Total | 536 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---:|---:|
| non exposé / interrompu | 1 | 0.8 % |
| stop | 30 | 25.0 % |
| tool-calls | 89 | 74.2 % |
| Total | 120 | 100 % |

| Type d’outil | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| bash | 12 (10.5 %) | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 6 (5.3 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 (1.8 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (1.8 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 22 (19.3 %) | 21 (95.5 %) | 0 (0.0 %) | 1 (4.5 %) |
| edit | 3 (2.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 2 (1.8 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 8 (7.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 48 (42.1 %) | 47 (97.9 %) | 0 (0.0 %) | 1 (2.1 %) |
| write | 7 (6.1 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 114 (100.0 %) | 111 (97.4 %) | 1 (0.9 %) | 2 (1.8 %) |

## 3. Fichiers modifiés

Tentatives d’écriture natives, chemins absolus complets. Les déplacements par archive ne sont pas de nouvelles écritures.

| Chemin absolu | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/TECHNICAL.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-link-v1/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-link-v1/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-link-v1/specs/bulk-operations/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-link-v1/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_job_link.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_job_link_integration.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_job_link.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 10 (100.0 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Quatre artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-job-link-v1. STATISTIQUES.md est publié après la borne finale et n’est pas ajouté rétroactivement aux compteurs.

## 4. Commandes

| Famille native | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| Archivage | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol | 2 (16.7 %) | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| Unittest | 2 (16.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 4 (33.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 12 (100.0 %) | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |

| Commande native (100 caractères maximum) | Occurrences | Part |
|---|---:|---:|
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-job-link-v1 --skip-specs --yes --json | 1 | 8.3 % |
| /home/devops/.local/npm/bin/openspec validate --specs --json | 1 | 8.3 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-job-link-v1 --json | 2 | 16.7 % |
| /home/devops/.local/npm/bin/openspec validate bulk-operations --type spec --json | 1 | 8.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_job_link.py | 1 | 8.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_job_link_integr… | 1 | 8.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_job_link.py | 1 | 8.3 % |
| /usr/bin/true | 1 | 8.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v integration.test_kern… | 1 | 8.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v unit.test_bulk_job_li… | 1 | 8.3 % |
| true | 1 | 8.3 % |
| Total | 12 | 100 % |

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
| Début | 2026-10-10T07:31:00.343814+02:00 |
| Fin — après archive et sonde finale | 2026-10-10T08:15:01.593159+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 44 min 01 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-10T07:31:00.343814+02:00 (outil absent) | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-10T08:15:01.593159+02:00 (outil absent) | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux bornes : aucun relevé reconstitué, aucun quota fournisseur substitué. Les horodatages indiquent les bornes du constat d’indisponibilité. Les quotas Codex sont partagés par le compte ; une variation éventuelle pourrait inclure d’autres tâches simultanées.

| Domaine d’outils | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
|---|---:|---:|---:|---:|
| Autres outils | 92 (80.7 %) | 90 (97.8 %) | 0 (0.0 %) | 2 (2.2 %) |
| Commandes | 12 (10.5 %) | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |
| Fichiers | 10 (8.8 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total général | 114 (100.0 %) | 111 (97.4 %) | 1 (0.9 %) | 2 (1.8 %) |

29 tests réussis ; compilations et validations OpenSpec codes 0 ; archive et artefacts vérifiés au contenu exact. Seul WARNING de longueur accepté, aucune ERROR. Aucun commit, push ou inspection Git. PostgreSQL et navigateur non nécessaires et non exécutés pour cette unité purement mémoire. Aucune lecture de fichier sensible observée dans les outils du codage ; secrets fournisseur confinés au processus sécurisé et au stockage natif privé. Aucun rattachement effectif, cardinalité globale, persistance ou autorisation établi. Le cycle CISMP parent reprend sa sélection après contrôle de ce rapport ; il n’est pas déclaré globalement terminé.
