# Statistiques — add-initial-bulk-operation-status-v1

Archive : 2026-10-10-add-initial-bulk-operation-status-v1. RUN parent : cismp-pixs-758862ec875d4708. Job CAB : cismp-status-cab-9aee23bff7384503.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash / qwen3.8-flash | N/A — version exacte non exposée | OpenCode Go / opencode-go | xhigh | 1.4364 s | 75.8559 | 402.641 s mesurées ; part N/A |

Agent logiciel OpenCode 1.18.35, distinct de la version du modèle. Une seule configuration observée, PLLM mode 2 forcée. Moyennes des sondes valides uniquement.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A — agent non sondé | N/A — agent non sondé | N/A — durée active non exposée |

Temps de codage : somme des intervalles des parties texte/raisonnement horodatées, hors outils et attentes de permission ; couverture partielle, génération des arguments d’outils non mesurée. Durée active Codex absente : dénominateur global et parts de service N/A. Les activités peuvent se chevaucher ; la durée calendaire est calculée séparément.

## 1. Statistiques générales et décisions

Source : historique natif complet de la session, filtré sur les dates de création des messages dans l’intervalle. Extraction inférieure à 1 000 messages par session, sans troncature. Sondes jetables, prévol initial, RSMP préalable et reset CAB antérieur exclus des chiffres de production ; aucune répartition artificielle des données du RUN parent. Le test CAB de récupération après le refus interne appartient à cet intervalle. Publication du présent rapport postérieure à sa clôture.

| Session de codage | Messages complets à l’extraction |
| --- | --- |
| ses_eda4c5860ffe92YX4LfGqpp067 | 151 |

Intervalle : 2026-10-10T14:06:39.510424+02:00 → 2026-10-10T14:35:54.214693+02:00 ; durée 00 h 29 min 14.704 s, pauses, permissions, récupérations, tests et archivage inclus.

| Production | Nombre |
| --- | --- |
| Messages | 141 |
| Parties | 442 |
| Appels d’outils | 64 |

| Décisions explicites CGPT | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Mandats CAB uniques | 18 | 100.0 % | 17 (94.4 %) | 1 (5.6 %) | 0 (0.0 %) |
| Total | 18 | 100 % | 17 (94.4 %) | 1 (5.6 %) | 0 (0.0 %) |

Décisions relues par requestId dans le contrôleur et corrélées aux entrées MCP natives. Le refus porte sur le titre/résumé reformulés alors qu’ils étaient prescrits, avant tout effet. Les demandes suivantes proposent leurs libellés ; CGPT les examine puis gèle le mandat complet avant décision. Identifiants, cible, commande, session, répertoire et délais restent exacts. Polling d’un même approval_id sans nouveau mandat. Aucun refus n’est assimilé à une approbation.

| Permissions distinctes | Nombre | Part |
| --- | --- | --- |
| Permissions natives once | 17 | 100.0 % |
| Permissions natives rejetées | 0 | 0.0 % |
| Total | 17 | 100 % |

Chaque effet exécuté dispose d’une décision CAB approuvée, d’une permission.asked, d’une permission.replied once et d’un appel natif unique terminé. Les deux événements ne comptent qu’une permission. Un appel completed prouve son succès technique, pas à lui seul une approbation manuelle. Refus CAB et erreur de transport MCP sont distincts.

| Télémétrie de production | Valeur | Couverture / limites |
| --- | --- | --- |
| Tokens entrée hors cache | 582 | 97/97 (100.0 %) |
| Tokens sortie natifs | 37668 | 97/97 (100.0 %) |
| Tokens raisonnement séparés | 0 | Champ natif, sans estimation indépendante |
| Cache lu | 7367271 | 97/97 (100.0 %) |
| Cache écrit | 891234 | 97/97 (100.0 %) |
| Total natif | 8296755 | Entrée + sortie + cache lu + cache écrit |
| Coût natif agrégé | 0.313914396 | 97/97 ; unité monétaire non fournie |
| Compactions observées | 0 | 0.0 % des messages ; hors intervalle non inféré |

Résultats : 11 tests ciblés + 54 régressions = 65/65 réussites (100 %), 0 échec (0 %). Trois compilations distinctes 3/3 (100 %). OpenSpec avant/après code : deux validations 1/1 exit0, issues[] (2/2, 100 %). Sept tâches cochées après preuves. Archive exécutée une fois, exit0, specsUpdated=false. Trois exigences du delta identiques au canon validé ; 102 fichiers préservés avant archivage.

Sondes dédiées jetables, prompt constant : « Sans outil ni fichier ni réseau. Produis uniquement les 100 lignes CALIBRATION 0001 à CALIBRATION 0100, dans cet ordre, une ligne par numéro, sans explication ni bloc de code. »

| Position / envoi | Fin | État | Tokens sortie | Durée sonde | TTMT | Tokens/s | Coût natif |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début — 2026-10-10T14:06:39.544594+02:00 | 2026-10-10T14:06:53.025799+02:00 | valid | 951 | 13.4768 s | 1.1834 s | 78.0146 | 0.000611230 |
| fin — après archivage — 2026-10-10T14:35:27.576614+02:00 | 2026-10-10T14:35:35.498597+02:00 | invalid | 526 | 7.9179 s | 1.2512 s | 81.3233 | 0.002161320 |
| fin — après archivage — unique nouvelle tentative — 2026-10-10T14:35:35.534276+02:00 | 2026-10-10T14:35:51.443577+02:00 | valid | 1037 | 15.9043 s | 1.6895 s | 73.6972 | 0.000641346 |

| Relèves | Nombre | Part |
| --- | --- | --- |
| Prévues | 2 | 100 % |
| Réussies | 2 | 100.0 % |
| Échouées | 0 | 0.0 % |
| Manquées | 0 | 0.0 % |

Tentatives valides : 2/3 (66.7 %). Tentatives invalides visibles et exclues des moyennes ; une seule reprise immédiate autorisée. Toute échéance manquée reste manquée, sans recréation. Historique natif complet des sondes valides sans outil, configuration vérifiée ; version exacte du modèle N/A. Le réseau fournisseur nécessaire à l’inférence est distinct d’un outil réseau de la sonde.

TTMT : moyenne 1.4364 s, min 1.1834 s, max 1.6895 s. Débit : moyenne 75.8559, min 73.6972, max 78.0146 tokens/s. Mesure monotone premier/dernier événements SSE de texte généré, raisonnement compris ; débit = tokens sortie natifs / cet intervalle. Les fragments SSE ne sont jamais comptés comme tokens. Instants bruts et bornes murales conservés dans le checkpoint.

Surcharge des sondes séparée : 37.2990 s, 2514 tokens sortie, coût natif 0.003413896. Entrée/cache des sondes N/A, non enregistrés. Aucune conversion en euros.

## 2. Types de messages et d’outils

| Rôle des messages | Nombre | Part |
| --- | --- | --- |
| user | 44 | 31.2 % |
| assistant | 97 | 68.8 % |
| Total | 141 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 87 | 19.7 % |
| step-start | 97 | 21.9 % |
| reasoning | 97 | 21.9 % |
| tool | 64 | 14.5 % |
| step-finish | 97 | 21.9 % |
| Total | 442 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 54 | 55.7 % |
| stop | 43 | 44.3 % |
| Total | 97 | 100 % |

| Outil natif / MCP | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| bash | 9 | 14.1 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 10 | 15.6 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 | 1.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 6 | 9.4 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 18 | 28.1 % | 18 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 | 1.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 1 | 1.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 11 | 17.2 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 | 10.9 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 64 | 100 % | 64 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Completed désigne ici un succès technique, y compris pour une consultation qui retourne REJECTED : les décisions CAB sont décomptées séparément. Erreurs techniques et terminaisons absentes restent visibles. Aucun outil running/pending dans la collecte close.

## 3. Fichiers modifiés

| Chemin absolu complet — tentatives CAB d’écriture | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-status-v1/design.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-status-v1/proposal.md | 2 | 22.2 % | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-status-v1/specs/bulk-operations/spec.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-status-v1/tasks.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_status.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_status_integration.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_status.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 8 (88.9 %) | 1 (11.1 %) | 0 (0.0 %) |

9 tentatives sur 7 fichiers distincts : 8 exécutées (88.9 %), 1 refusées avant effet (11.1 %). tasks.md créé puis coché par mandats distincts. L’archive déplace les quatre artefacts sous /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-operation-status-v1 ; trois sources Python restent en place. Déplacement compté dans la commande d’archive, sans éditions inventées. Caches py_compile régénérables ; checkpoint parent et publication du présent rapport exclus des écritures de production de l’agent.

## 4. Commandes

| Famille de commandes exécutées | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Test CAB de récupération | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 33.3 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archivage OpenSpec | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande affichée (100 caractères maximum) | Occurrences | Part | Résultat |
| --- | --- | --- | --- |
| /usr/bin/true | 1 | 11.1 % | exit0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-operation-status-v1 --json | 2 | 22.2 % | exit0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_operation_status.py | 1 | 11.1 % | exit0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_operation_status.py | 1 | 11.1 % | exit0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_operation_statu… | 1 | 11.1 % | exit0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v unit.test_bulk_operat… | 1 | 11.1 % | exit0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v unit.test_semver_cons… | 1 | 11.1 % | exit0 |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-operation-status-v1 --yes --skip-spec… | 1 | 11.1 % | exit0 |
| Total | 9 | 100 % | 9/9 exit0 (100 %) |

Commandes refusées : aucune ; le refus CAB cible un fichier.

Textes exacts conservés dans les mandats et l’historique. PostgreSQL et frontend sans objet pour ce profil Kernel pur ; aucune exécution revendiquée.

## 5. Accès web

| Accès observés | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Outils web de l’agent de codage | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 0 | 100 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Zéro webfetch/websearch sur 64 appels (0 %), aucune URL visitée ou refusée par ces outils. Taux de résultat N/A (dénominateur zéro), total100 % par convention. API OpenCode/CAB et fournisseur distinctes de la navigation ; journal réseau exhaustif de l’orchestrateur N/A. Aucune absence globale de réseau inférée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-10T14:06:39.510424+02:00 |
| Fin — après archivage | 2026-10-10T14:35:54.214693+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 29 min 14.704 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil natif indisponible | N/A | N/A |
| Après — après archivage de la spécification | N/A — outil natif indisponible | N/A | N/A |
| Différence après − avant | — | N/A — deux lectures natives indisponibles | — |

mcp__codex_app__get_usage_limits non exposé : compte, fenêtre codex/10080 et réinitialisation N/A. Disponibilité contrôlée au début et après archivage ; aucun profil ni quota OpenCode Go substitué. Les quotas sont partagés par compte, et une variation peut inclure d’autres tâches simultanées ; exclusivité non vérifiable.

| Domaines des appels natifs | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Commandes — bash | 9 | 14.1 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Autres — lecture et CAB | 47 | 73.4 % | 47 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web — webfetch/websearch | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Fichiers — write/edit | 8 | 12.5 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 64 | 100 % | 64 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Croisements : 141 messages ; 442 parties ; 64 succès techniques + 0 erreurs = 64 outils ; 17 approbations + 1 refus = 18 décisions ; 8 écritures + 9 commandes = 17 permissions once. Tokens : 582 + 37668 + 7367271 + 891234 = 8296755. Les tentatives par mandat ne s’ajoutent pas aux appels.

BulkOperationStatus v1 : profil interne immuable à deux champs obligatoires, dix états canoniques, validation pure sans transition ni IO, diagnostics statiques et refus des faux membres Enum. 65 tests et trois compilations réussis, façades et dépendances préservées. Archive réalisée une fois avec --skip-specs ; preuve de publication du rapport recueillie ensuite sans réarchiver. Aucun outil ni commande Git observé ; état Git non inspecté. Sources et sorties contrôlées sans secret ; aucune assertion exhaustive sur les sources exclues. Cette archive ne prouve pas l’achèvement du cycle parent CISMP.
