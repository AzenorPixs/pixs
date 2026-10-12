# Statistiques — add-initial-bulk-operation-commit-mode-v1

RUN cismp-pixs-758862ec875d4708 ; session de codage ses_ed6abaffdffeIY8xv474pxwUZe. Historique natif complet paginé, filtré par création des messages entre les bornes ci-dessous. RSMP préalable, prévol, sondes dédiées, compactage administratif après collecte et publication du présent rapport exclus des totaux de production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash | N/A : version exacte non exposée | OpenCode Go | xhigh | 1.716 s | 79.941 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A : identifiant exact non exposé | OpenAI | N/A | N/A : aucune sonde orchestrateur | N/A | N/A |

Temps de service N/A : aucun chronométrage de génération active comparable ; les durées des messages incluent permissions et outils. Aucun dénominateur fiable ni estimation des chevauchements. OpenCode 1.18.35 ; broker actif observé 0.87.1, plugin distribué 0.87.2 (versions distinctes).

## 1. Statistiques générales et décisions

129 messages (100 %), 58 appels d’outils enregistrés (100 %), durée calendaire 00 h 40 min 04 s, attentes et pauses incluses.

| Décisions CAB uniques observées | Nombre | Part |
| --- | --- | --- |
| APPROVED | 16 | 88.9 % |
| REJECTED | 2 | 11.1 % |
| Total | 18 | 100 % |

Abouti signifie outil terminé sous permission automatique ou manuelle, pas preuve d’approbation CAB à lui seul. Une requête MCP peut aboutir en retournant REJECTED ; les décisions sont comptées séparément et dédupliquées par approval_id. Les identifiants seulement planifiés, non enregistrés, sont exclus. Les délais de transport restent des erreurs techniques même si un polling résout ensuite la même approbation.

| Compteur natif | Valeur | Limite |
| --- | --- | --- |
| input | 456 | 92 |
| output | 34138 | 92 |
| reasoning | 0 | 92 |
| cache_read | 5599482 | voir cache natif |
| cache_write | 947567 | voir cache natif |
| total | N/A : compteur absent dans 16 réponses | 76 |
| Coût télémétrique observé (USD) | 0.29521837 | facturation réelle N/A |
| Compactions dans la production | 0 | compactage post-collecte exclu |
| Messages interrompus volontairement après outil terminé | 16 | outil terminé reste abouti |

Les compteurs sont reproduits sans addition artificielle de total. Les zéros fournis par la télémétrie et les interruptions de génération ne prouvent pas une facturation exhaustive. Résultat : trois compilations exit0, 10 tests ciblés et 93 régressions OK, soit 103/103 (100 %), stricts pré-code et post-code du change exit0 avec une entrée passée et aucune issue.

Le RSMP précédent a ajouté exactement quatre exigences et une note TECHNICAL. Ses validations ciblée et globale restent exit1 pour exactement trois avertissements historiques de longueur (requirements[6], [10], [13]), zéro erreur nouvelle ; elles ne sont pas déclarées réussies globalement. Ce RSMP est hors intervalle de production.

Deux demandes refusées avant effet : variables OPENSPEC_TELEMETRY/DO_NOT_TRACK remplacées par des variables non prescrites ; puis requestId et approval_id altérés pour le cochage. Aucun Bash ou edit n’a été exécuté sur ces demandes. Les décisions HTTP ont utilisé les identifiants effectivement soumis, jamais les identifiants seulement planifiés. Reprises sous mandats neufs, sans rejouer d’écriture validée. Les erreurs MCP de délai sont distinctes de ces refus.

Le contrôle SSE interrompt volontairement le tour de génération au premier résultat terminal natif pour prévenir un rejeu ; le rapport est demandé séparément. Chaque opération livrée a un unique asked/once corrélé. Le processus OpenCode reste ouvert. Un compactage natif coordonné a été effectué après fermeture de la collecte ; API Codex propriétaire indisponible, cycle PARTIAL, sans perte du contexte.

### Sondes de performance séparées

| Position | Début | État | TTMT (s) | Tokens/s | Tokens sortie | Coût natif USD |
| --- | --- | --- | --- | --- | --- | --- |
| début code BulkOperationCommitMode | 2026-10-11T07:04:36.136309+02:00 | valid | 1.505338 | 96.972775 | 357 | 0.00207849 |
| périodique code BulkOperationCommitMode | 2026-10-11T07:34:36.308072+02:00 | valid | 1.568006 | 74.360361 | 351 | 0.00207567 |
| fin après archivage BulkOperationCommitMode | 2026-10-11T07:43:44.025090+02:00 | valid | 2.074878 | 68.488427 | 400 | 0.0020987 |

Relèves prévues 3, réussies 3 (100.0 %), échouées 0, manquées 0 : début, +30 min, fin après archivage. Moyennes arithmétiques des seules valides ; TTMT min/max 1.505338/2.074878 s ; débit min/max 68.488427/96.972775 tokens/s.

Prompt constant : « Écris uniquement les entiers de 0001 à 0064 inclus, un par ligne sur quatre chiffres. Aucun commentaire, aucun outil. ». Même configuration native opencode-go/qwen3.8-flash/xhigh, sessions sans outil ni accès fichier/réseau par le modèle. TTMT = premier delta text SSE natif − envoi ; débit = tokens output natifs / (dernier delta − premier delta), raisonnement/réponse si présents, compteur output non ventilé.

Surcharge de télémétrie exclue de la production : 29773 tokens totaux natifs (si total disponible), 1108 tokens output, 0.00625286 USD, 20.033 s de durée cumulée. Aucune sonde orchestrateur.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 92 | 71.3 % |
| user | 37 | 28.7 % |
| Total | 129 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 76 | 21.1 % |
| step-finish | 76 | 21.1 % |
| step-start | 76 | 21.1 % |
| text | 75 | 20.8 % |
| tool | 58 | 16.1 % |
| Total | 361 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| absent / interruption contrôlée | 16 | 17.4 % |
| stop | 21 | 22.8 % |
| tool-calls | 55 | 59.8 % |
| Total | 92 | 100 % |

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| bash | 8 | 13.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 15 | 25.9 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 2 | 3.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 18 | 31.0 % | 16 (88.9 %) | 0 (0.0 %) | 2 (11.1 %) |
| edit | 1 | 1.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 7 | 12.1 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 | 12.1 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 58 | 100 % | 56 (96.6 %) | 0 (0.0 %) | 2 (3.4 %) |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-commit-mode-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-commit-mode-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-commit-mode-v1/specs/bulk-operations/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-commit-mode-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_commit_mode.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_commit_mode_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_commit_mode.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Ces effectifs sont des tentatives natives, pas des fichiers uniques. Quatre artefacts et trois nouveaux Python, puis une édition de tasks.md sur preuves. Un mandat tasks.md a été refusé avant permission : 1 refus (100 % des mandats fichiers refusés), aucune tentative native d’écriture associée. Aucun fichier existant hors artefacts n’a été modifié. Les 313 références et les ensembles de fichiers Python des trois répertoires ont été comparés ; PA/PZT, enums et façades préservés.

L’archivage déplace les quatre artefacts vers openspec/changes/archive/2026-10-11-add-initial-bulk-operation-commit-mode-v1. Les deux fichiers canoniques du RSMP sont hors intervalle et préservés pendant l’implémentation. Rapport STATISTIQUES.md publié ensuite sous mandat distinct, hors intervalle scellé ; les mises à jour du checkpoint par l’orchestrateur ne sont pas des écritures natives de l’agent de codage.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 3 | 37.5 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 5 | 62.5 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| 1. OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-initial-bu… | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 2. /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_operation_commit_mo… | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 3. /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_operation_commit_mo… | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 4. /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_operation_co… | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 5. PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_bulk_… | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 6. PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_semve… | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| 7. OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-initial-bul… | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées au stade mandat, sans exécution native :

| Commande (≤100 caractères) | Demandes refusées | Part | Effet |
| --- | --- | --- | --- |
| OP_REMEDIATE=1 DO_REMEDIATE=1 /home/devops/.local/npm/bin/openspec validate add-initial-bulk-operat… | 1 | 100.0 % | Aucun |

Les libellés sont tronqués à 100 caractères maximum, indicateur compris ; commandes intégrales dans les preuves natives et le checkpoint. Les refus de mandat ne sont pas transformés en appels Bash inexistants. Les huit commandes effectivement exécutées sont distinguées des propositions refusées.

## 5. Accès web

0 appel web (0 % des outils), 0 abouti, 0 refusé, 0 erreur ; taux web N/A (dénominateur nul). Aucune URL approuvée, refusée ou visitée par l’agent de codage ; aucune requête web. Transport fournisseur, API CAB et SSE locaux distincts des outils web. Aucun accès web orchestrateur dans ce change observé.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T07:04:36.136279+02:00 |
| Fin — après archivage | 2026-10-11T07:44:40.327988+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 40 min 04 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-11T07:04:36.136303+02:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-11T07:44:40.327959+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux bornes ; identité et fenêtre non vérifiables, aucun quota externe substitué. Les quotas sont partagés par le compte ; une variation pourrait inclure d’autres tâches simultanées.

| Catégorie | Total | Part | Aboutis | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Autres outils | 42 | 72.4 % | 40 (95.2 %) | 0 (0.0 %) | 2 (4.8 %) |
| Commandes | 8 | 13.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 8 | 13.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 58 | 100 % | 56 (96.6 %) | 0 (0.0 %) | 2 (3.4 %) |

Totaux croisés vérifiés par type et domaine. Archive réussie, specsUpdated=false ; rapport publié ensuite, six sections UTF-8/LF vérifiées. Git : aucune inspection ni opération. Aucun secret inclus dans les nouveaux contenus byte-exact ; aucun effet externe mutable observé. Ces traces ne démontrent pas toute activité hors RUN. Change livré ; cycle global incomplet, retour SÉLECTION pour la prochaine décision normative.
