# Statistiques — add-initial-bulk-operation-header-v1

Archive : 2026-10-10-add-initial-bulk-operation-header-v1. RUN parent : cismp-pixs-758862ec875d4708.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash / qwen3.8-flash | N/A — version exacte du modèle non exposée | OpenCode Go / opencode-go | xhigh | 2.5237 s | 82.3206 | 965.790 s mesurées ; part N/A |

Agent logiciel OpenCode 1.18.35, distinct de la version du modèle. Une seule configuration observée. Moyennes des deux sondes valides ; les deux tentatives initiales invalides sont exclues.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | N/A — version exacte non fournie par télémétrie native | OpenAI | N/A — non exposé | N/A — agent non sondé | N/A — agent non sondé | N/A — durée active non exposée |

Les 965.790 s de codage sont la somme des intervalles natifs des parties texte/raisonnement horodatées, hors outils et attentes de permission. La durée active de l’orchestrateur manque : dénominateur de service global et pourcentage entre agents N/A. Les activités peuvent se chevaucher ; elles ne sont pas additionnées pour la durée calendaire.

## 1. Statistiques générales et décisions

Source : historique natif complet des trois sessions ci-dessous, limité aux messages créés entre les bornes de collecte. Chaque requête a rendu moins de 1 000 messages ; aucune pagination tronquée. Sondes jetables, diagnostics hors sessions et rédaction du rapport sont exclus des chiffres de production. La reprise après interruption et son prévol, postérieurs à la clôture, sont exclus. Le RSMP préalable appartient au RUN parent ; ses données ne sont pas réparties artificiellement dans cette archive.

| Session de codage | Messages complets observés à l’extraction |
| --- | --- |
| ses_edb6b3ed3ffeUtLb07gLRQglV3 | 22 |
| ses_edb615d7bffe4ZN1ruN2YiMnyZ | 65 |
| ses_edb539f98ffeIZRjJp7YTMtj2O | 122 |

Intervalle : 2026-10-10T08:53:28.559260+02:00 → 2026-10-10T09:52:27.283151+02:00 ; durée 00 h 58 min 58.724 s, pauses, permissions, récupérations, tests et archive inclus. Production : 189 messages, 668 parties, 124 appels d’outils.

| Décisions explicites CGPT | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Mandats CAB uniques | 20 | 100.0 % | 18 (90.0 %) | 2 (10.0 %) | 0 (0.0 %) |
| Total | 20 | 100 % | 18 (90.0 %) | 2 (10.0 %) | 0 (0.0 %) |

Les vingt décisions sont relues par requestId dans le contrôleur et corrélées aux appels MCP natifs. Dix-huit opérations ont une permission native once et un effet unique observés : huit écritures et dix commandes. Deux demandes d’écriture altérées ont été refusées avant effet (identifiants/titre/résumé, puis délai) ; récupérations et prévols ont précédé la poursuite. Ce ne sont pas des refus automatiques de la plateforme. Consultation/polling ne créent pas de nouveaux mandats.

| Permissions distinctes | Nombre | Part |
| --- | --- | --- |
| Permissions natives answered once | 18 | 100.0 % |
| Permissions natives rejetées | 0 | 0.0 % |
| Total | 18 | 100 % |

Les 18 permission.asked et 18 permission.replied/once sont deux événements pour chacune des dix-huit permissions, pas trente-six autorisations. Un outil completed prouve son succès technique, pas à lui seul une approbation manuelle. Les lectures natives sont sans permission ; les dix-huit effets sont reliés aux décisions CAB et permissions. Refus CAB et erreurs de transport MCP sont des dimensions différentes.

| Télémétrie de production | Valeur | Couverture / limites |
| --- | --- | --- |
| Tokens entrée hors cache | 792 | 133/133 messages assistant (100 %) |
| Tokens sortie natifs | 70272 | 133/133 (100 %) |
| Tokens raisonnement séparés | 0 | Champ natif nul ; aucun raisonnement indépendant inféré |
| Cache lu | 8437579 | 133/133 (100 %) |
| Cache écrit | 1935860 | 133/133 (100 %) |
| Total natif | 10444503 | 100 % ; entrée + sortie + cache lu + cache écrit |
| Coût natif agrégé | 0.555319904 | 133/133 (100 %) ; unité monétaire non fournie |
| Compactions observées | 0 | 0/189 messages (0.0 %) ; aucune extrapolation hors intervalle |

Résultats : 11 tests ciblés + 43 régressions = 54/54 réussites (100 %), 0 échec (0 %). Trois compilations distinctes réussies (3/3, 100 %). Deux validations OpenSpec avant/après code, chacune 1/1 exit0, issues[] (2/2, 100 %). Archive autorisée distinctement : une exécution exit0, specsUpdated=false. Sept tâches cochées après preuves. Les alertes textuelles non confirmées de circuit CAB et de validation ont été écartées par les sorties natives ; les changements externes AGENTS.md/ORCHESTRATED_CODING.md ont été lus et réconciliés, sans être attribués à cet agent.

Sondes dédiées jetables, même configuration et prompt constant : « Sans outil ni fichier ni réseau. Produis uniquement les 100 lignes CALIBRATION 0001 à CALIBRATION 0100, dans cet ordre, une ligne par numéro, sans explication ni bloc de code. »

| Position / envoi | Fin | État | Tokens sortie natifs | Durée sonde | TTMT | Tokens/s | Coût natif |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début — 2026-10-10T08:53:28.579243+02:00 | 2026-10-10T08:53:39.672150+02:00 | invalid | 889 | 11.0929 s | 1.1619 s | 90.6041 | 0.000647482 |
| début — unique nouvelle tentative — 2026-10-10T08:53:50.221219+02:00 | 2026-10-10T08:55:12.126439+02:00 | invalid | 5015 | 81.9052 s | 1.4537 s | 62.3603 | 0.002576398 |
| +30 min — 2026-10-10T09:23:28.598963+02:00 | 2026-10-10T09:23:42.842998+02:00 | valid | 988 | 14.2384 s | 1.6373 s | 79.1946 | 0.002588260 |
| fin — après archivage — 2026-10-10T09:52:12.349587+02:00 | 2026-10-10T09:52:27.252215+02:00 | valid | 945 | 14.8978 s | 3.4101 s | 85.4465 | 0.002358250 |

Trois échéances prévues : début, +30 min, fin ; deux réussies (66.7 %), une échouée (33.3 %), zéro manquée (0 %). Quatre tentatives avec l’unique reprise immédiate initiale autorisée : deux valides (50 %), deux invalides (50 %). Les sorties initiales ne respectent pas les cent lignes fixes : visibles mais exclues des moyennes. Pour +30 min et fin, l’historique natif complet confirme zéro outil ; ce contrôle complet n’a pas été enregistré pour les tentatives initiales (N/A), sans inférer un accès. Aucune sonde +60 min due avant clôture.

TTMT valide : moyenne 2.5237 s, min 1.6373 s, max 3.4101 s. Débit valide : moyenne 82.3206, min 79.1946, max 85.4465 tokens/s. TTMT au premier événement de texte généré, raisonnement compris ; débit = tokens sortie natifs / intervalle monotone entre premier et dernier événements de texte généré. Les fragments SSE ne servent jamais de tokens. Instants monotones bruts N/A : seules leurs différences et les bornes murales ont été conservées.

Surcharge distincte des quatre sondes : 122.1343 s, 7837 tokens sortie natifs, coût natif 0.008170390. Entrée/cache des sondes N/A, non enregistrés. Aucun coût converti en euros.

## 2. Types de messages et d’outils

| Rôle des messages | Nombre | Part |
| --- | --- | --- |
| user | 56 | 29.6 % |
| assistant | 133 | 70.4 % |
| Total | 189 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 146 | 21.9 % |
| step-start | 133 | 19.9 % |
| reasoning | 133 | 19.9 % |
| tool | 124 | 18.6 % |
| step-finish | 132 | 19.8 % |
| Total | 668 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 83 | 62.4 % |
| stop | 49 | 36.8 % |
| absent | 1 | 0.8 % |
| Total | 133 | 100 % |

| Outil natif / MCP | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| bash | 10 | 8.1 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 27 | 21.8 % | 27 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 5 | 4.0 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 2 | 1.6 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 20 | 16.1 % | 18 (90.0 %) | 0 (0.0 %) | 2 (10.0 %) |
| edit | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 51 | 41.1 % | 51 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 | 5.6 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 124 | 100 % | 122 (98.4 %) | 0 (0.0 %) | 2 (1.6 %) |

Ici « réussi » signifie completed natif. Deux erreurs request_validation : abandon avant effet lors d’un refus CGPT, et transport interrompu puis récupéré par polling corrélé. Un refus CAB peut apparaître dans un MCP techniquement completed : les deux refus restent dans les décisions sans double comptage. Aucun outil running/pending à la clôture ; la terminaison assistant absente est un message interrompu conservé.

## 3. Fichiers modifiés

| Chemin absolu complet — tentatives CAB d’écriture | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-header-v1/design.md | 1 | 10.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-header-v1/proposal.md | 2 | 20.0 % | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-header-v1/specs/bulk-operations/spec.md | 1 | 10.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-header-v1/tasks.md | 2 | 20.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_header.py | 2 | 20.0 % | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_header_integration.py | 1 | 10.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_header.py | 1 | 10.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 | 100 % | 8 (80.0 %) | 2 (20.0 %) | 0 (0.0 %) |

Dix tentatives sur sept fichiers distincts : huit exécutées (80 %), deux refusées avant effet (20 %), zéro erreur finale d’écriture (0 %). tasks.md est créé puis coché par deux mandats. L’archive déplace les quatre artefacts sous /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-operation-header-v1 ; les trois fichiers Python restent en place. Le déplacement est compté dans la commande d’archive, sans inventer quatre éditions supplémentaires. Les caches py_compile sont régénérables. Le présent STATISTIQUES.md a un mandat distinct après l’intervalle et n’est pas compté rétroactivement. Le checkpoint parent est hors écritures de l’agent de codage.

## 4. Commandes

| Famille de commandes exécutées | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Prévol / récupération | 2 | 20.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 2 | 20.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 30.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 2 | 20.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archivage OpenSpec | 1 | 10.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 | 100 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande affichée (100 caractères maximum) | Occurrences | Part des 10 exécutions | Résultat |
| --- | --- | --- | --- |
| /usr/bin/true | 2 | 20.0 % | exit0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-operation-header-v1 --json | 2 | 20.0 % | exit0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_operation_header.py | 1 | 10.0 % | exit0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_operation_header.py | 1 | 10.0 % | exit0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_operation_heade… | 1 | 10.0 % | exit0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v unit.test_bulk_operat… | 1 | 10.0 % | exit0 |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest -v unit.test_semver_cons… | 1 | 10.0 % | exit0 |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-operation-header-v1 --yes --skip-spec… | 1 | 10.0 % | exit0 |
| Total | 10 | 100 % | 10/10 exit0 (100 %) |

Les commandes longues sont tronquées pour l’affichage ; leur texte exact est dans les mandats et l’historique natif. Commandes refusées : aucune, 0/10 exécutions (0 %) ; les deux refus CAB ciblent des fichiers. Les validations avant/après sont deux requestId pour la même commande. PostgreSQL et frontend sans objet pour ce profil Kernel pur ; aucune exécution revendiquée.

## 5. Accès web

| Accès observés | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Outils web de l’agent de codage | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 0 | 100 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Zéro webfetch/websearch sur 124 appels (0 %), aucune URL visitée ou refusée par ces outils. Taux de résultat N/A : dénominateur zéro. Total à 100 % par convention de tableau, sans visite implicite. Échanges API OpenCode/CAB et appels fournisseur distincts de la navigation : journal réseau exhaustif de l’orchestrateur N/A. Aucune absence globale de réseau n’est inférée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-10T08:53:28.559260+02:00 |
| Fin — après archivage | 2026-10-10T09:52:27.283151+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 58 min 58.724 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil natif indisponible | N/A | N/A |
| Après — après archivage de la spécification | N/A — outil natif indisponible | N/A | N/A |
| Différence après − avant | — | N/A — deux lectures natives indisponibles | — |

mcp__codex_app__get_usage_limits non exposé : compte, fenêtre codex/10080 et réinitialisation N/A. Les quotas sont partagés par compte ; une variation peut inclure des tâches simultanées, exclusivité non vérifiable. Aucun quota Spark, OpenCode Go, profil ou secret ne remplace ces relevés.

| Domaines des appels natifs | Total | Part | Réussis / approuvés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Fichiers — write/edit | 8 | 6.5 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes — bash | 10 | 8.1 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web — webfetch/websearch | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres — lecture et CAB | 106 | 85.5 % | 104 (98.1 %) | 0 (0.0 %) | 2 (1.9 %) |
| Total | 124 | 100 % | 122 (98.4 %) | 0 (0.0 %) | 2 (1.6 %) |

Base : 124 appels sans duplication. Dix tentatives d’écriture et vingt décisions sont des analyses par cible/mandat et ne s’ajoutent pas aux appels. Croisements : 133 + 56 = 189 messages ; 146 + 133 + 133 + 132 + 124 = 668 parties ; 122 réussites techniques + 2 erreurs = 124 outils ; 18 approbations + 2 refus = 20 décisions ; 8 écritures + 10 commandes = 18 permissions once. Tokens : 792 + 70 272 + 8 437 579 + 1 935 860 = 10 444 503.

BulkOperationHeader v1 : profil interne immuable à trois champs obligatoires, validateur sans effet de bord, 54 tests réussis et trois compilations. Façades et dépendances préservées ; delta de quatre exigences identique au canon validé. Archive réussie une seule fois avec --skip-specs, specsUpdated=false. Preuves de publication du rapport recueillies ensuite par l’orchestrateur sans réarchiver. Aucun outil ni commande Git observé ; état Git non inspecté. Les sources et sorties contrôlées n'exposent pas de secret ; aucune assertion exhaustive sur des sources exclues ou un journal réseau absent. Cette archive ne prouve pas l'achèvement global du RUN parent CISMP.
