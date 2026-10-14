# Statistiques — add-initial-data-tombstone-profile-v1

RUN parent : cismp-pixs-20261007-061019. Archive : openspec/changes/archive/2026-10-07-add-initial-data-tombstone-profile-v1. Intervalle de production et récupération du change, après le prévol initial ; inclut les reprises CAB nécessaires. Les sondes sont séparées de la production. La rédaction de ce rapport est hors intervalle.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash (qwen3.8-flash) | Modèle N/A ; OpenCode 1.18.34 | opencode-go | xhigh | 2.029 s | 94.095 | 844.620 s ; part globale N/A |

Trois sondes valides déterminent les moyennes arithmétiques. Le service correspond à l’union des intervalles natifs de texte/raisonnement ; les durées d’outils et attentes ne sont pas ajoutées. Le service de l’orchestrateur n’est pas exposé : le dénominateur global de tous les agents reste N/A, sans assimiler la durée calendaire à leur service.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex (identifiant exact N/A) | N/A — télémétrie non exposée | OpenAI | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

Durée globale : 01 h 09 min 35 s, pauses, outils, attentes et reprises inclus. Messages : 194. Parties : 699. Appels : 134.

Les appels terminés sont classés autorisés/exécutés, y compris les lectures sans permission native et le transport MCP. Un appel réussi ne prouve pas une approbation manuelle. Un refus de mandat CAB est compté séparément des erreurs de schéma/transport ; une consultation réussie d’un mandat refusé reste une lecture réussie. Les commandes peuvent être exécutées et avoir un code non nul : ce résultat est conservé séparément.

| Résultat des appels | Nombre | Part |
|---|---:|---:|
| Autorisés/exécutés | 126 | 94.0 % |
| Permissions natives refusées | 0 | 0.0 % |
| Erreurs techniques | 8 | 6.0 % |
| Total | 134 | 100 % |

| Décisions CAB distinctes observables | Nombre | Part |
|---|---:|---:|
| Approuvées explicitement par CGPT | 26 | 83.9 % |
| Refusées par CGPT | 4 | 12.9 % |
| Aucune décision — schéma ou création non aboutie | 1 | 3.2 % |
| Total des identifiants observés | 31 | 100 % |

Tokens natifs des réponses de production/récupération : entrée 876, sortie 85640, raisonnement déclaré 0, cache lu 12674571, cache écrit 293841. Les tokens de raisonnement séparés valent la valeur fournie par OpenCode et ne sont pas reconstitués depuis le texte. Coût natif total : 0.301943536 (unité OpenCode, devise non exposée). Compactions pendant cet intervalle : aucune invocation native observée.

Résultats livrés : trois fichiers Python ; 21 tests unitaires, 1 intégration fraîche et 108 régressions, soit 130/130 réussis (100 %), zéro échec/erreur/skip. Trois compilations : 3/3 (100 %). Change strict : 1/1, code 0 ; global : 77/77 (100 %), code 0. Vingt WARNING de longueur uniquement, exclus par instruction explicite. Strict du canon : code 1, non annoncé comme réussite ; canon non strict : 1/1, code 0. Sept tâches sur sept cochées (100 %). Archive native : code 0, specsUpdated=false.

| Sonde | UTC | Lignes | Tokens sortie | TTMT | Tokens/s | État |
|---|---|---:|---:|---:|---:|---|
| début | 2026-10-07T20:46:01.171529+00:00 | 20 | 517 | 1.536 s | 84.200 | Invalide — longueur de sortie non conforme |
| unique seconde tentative | 2026-10-07T20:46:08.972795+00:00 | 30 | 658 | 2.635 s | 78.368 | Invalide — longueur de sortie non conforme |
| +30 min | 2026-10-07T21:16:01.305543+00:00 | 40 | 582 | 2.204 s | 116.165 | Valide |
| +60 min | 2026-10-07T21:46:02.084005+00:00 | 40 | 572 | 1.852 s | 72.043 | Valide |
| fin après archive | 2026-10-07T21:55:28.049520+00:00 | 40 | 577 | 2.031 s | 94.077 | Valide |

Quatre positions prévues : début, +30 min, +60 min, fin. Trois réussies (75 %), une échouée (25 %), zéro manquée (0 %). Cinq tentatives : trois valides (60 %), deux invalides (40 %), unique seconde tentative initiale conservée. Moyennes excluent les deux invalides ; TTMT min/max : 1.852/2.204 s ; débit min/max : 72.043/116.165. Surcharge distincte : 2906 tokens sortie, 44.553 s calendaires cumulées, coût natif 0.008087216. Aucune attente du créneau n’a arrêté le travail.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 47 | 24.2 % |
| assistant | 147 | 75.8 % |
| Total | 194 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 147 | 21.0 % |
| step-finish | 146 | 20.9 % |
| step-start | 147 | 21.0 % |
| text | 125 | 17.9 % |
| tool | 134 | 19.2 % |
| Total | 699 | 100 % |

| Outil | Appels et part | Autorisés/exécutés et taux | Refusés et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| bash | 17 (12.7 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 10 (7.5 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 8 (6.0 %) | 7 (87.5 %) | 0 (0.0 %) | 1 (12.5 %) |
| cgpt-validation_list_pending | 2 (1.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 32 (23.9 %) | 27 (84.4 %) | 0 (0.0 %) | 5 (15.6 %) |
| edit | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 12 (9.0 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 4 (3.0 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 39 (29.1 %) | 37 (94.9 %) | 0 (0.0 %) | 2 (5.1 %) |
| write | 8 (6.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 134 (100.0 %) | 126 (94.0 %) | 0 (0.0 %) | 8 (6.0 %) |

| Terminaison des réponses assistant | Nombre | Part |
|---|---:|---:|
| tool-calls | 106 | 72.1 % |
| stop | 40 | 27.2 % |
| non renseignée/interrompue | 1 | 0.7 % |
| Total | 147 | 100 % |

## 3. Fichiers modifiés

Les effectifs représentent les tentatives natives write/edit, et non un inventaire Git. Les sept chemins sont indiqués au lieu d’écriture ; les artefacts OpenSpec ont ensuite été déplacés par l’archive autorisée.

| Chemin absolu | Tentatives et part | Autorisées/exécutées et taux | Refusées et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-data-tombstone-profile-v1/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-tombstone-profile-v1/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-tombstone-profile-v1/specs/data-lifecycle/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-tombstone-profile-v1/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_tombstone_profile.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_tombstone_profile_integration.py | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_tombstone_profile.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Métadonnée générée par la CLI : /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-tombstone-profile-v1/.openspec.yaml. Archive autorisée : /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-tombstone-profile-v1/. Les trois fichiers Python restent à leurs chemins src/tests. Ce rapport STATISTIQUES.md est produit après la borne finale et ne gonfle pas les totaux de production. Aucun fichier de référence modifié : 198 empreintes intactes ; nouveau contenu conforme à la revue, UTF-8/LF.

## 4. Commandes

| Famille | Appels et part | Autorisés/exécutés et taux | Refusés et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| OpenSpec | 8 (47.1 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol inoffensif | 3 (17.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 6 (35.3 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 (100.0 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande exécutée (libellé ≤100 caractères) | Nombre | Part | Code natif |
|---|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec new change add-initial-data-tombstone-profile-v1 | 1 | 5.9 % | [0] |
| /usr/bin/true | 1 | 5.9 % | [0] |
| /home/devops/.local/npm/bin/openspec validate add-initial-data-tombstone-profile-v1 --strict --json | 2 | 11.8 % | [0] |
| true | 2 | 11.8 % | [0] |
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --type spec --strict --json | 1 | 5.9 % | [1] |
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --type spec --json | 1 | 5.9 % | [0] |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_tombstone_profile.py | 1 | 5.9 % | [0] |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_tombstone_profile.py | 1 | 5.9 % | [0] |
| /home/devops/python/current/bin/python3 -B -c 'import sys import unittest sys.path[:0] = ["src", "t… | 1 | 5.9 % | [0] |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_tombstone_profile… | 1 | 5.9 % | [0] |
| /home/devops/python/current/bin/python3 -B -c 'import sys import unittest sys.path[:0] = ["src", "t… | 1 | 5.9 % | [0] |
| /home/devops/python/current/bin/python3 -B -c 'import sys import unittest sys.path[:0] = ["src", "t… | 1 | 5.9 % | [0] |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 5.9 % | [0] |
| /home/devops/.local/npm/bin/openspec archive --help | 1 | 5.9 % | [0] |
| /home/devops/.local/npm/bin/openspec archive add-initial-data-tombstone-profile-v1 --skip-specs --y… | 1 | 5.9 % | [0] |
| Total | 17 | 100 % | — |

Les commandes refusées ci-dessous proviennent des décisions CAB : elles n’ont pas été exécutées. Le refus du mandat resté en attente est une clôture technique préalable à sa reprise sûre.

| Commande de mandat refusé (≤100 caractères) | Occurrences | Part des refus |
|---|---:|---:|
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --strict --json | 1 | 20.0 % |
| true | 3 | 60.0 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-data-tombstone-profile-v1 --strict --json | 1 | 20.0 % |
| Total | 5 | 100 % |

Incidents conservés : résumé MCP >2000 caractères et title manquant (schéma), champs/identifiants de prévol divergents refusés avant exécution, délais MCP et course d’enregistrement contrôleur suivis de réconciliation/test CAB neuf. Rapports textuels erronés sur seconde commande, options CLI, codes et compteurs corrigés à partir des parties natives. Aucune écriture ni permission consommée hors mandat observée.

## 5. Accès web

| Accès web natifs de production | Nombre | Part | Approuvés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| Outils webfetch/websearch | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucune URL visitée par un outil web dans cet historique. Les appels natifs du fournisseur, le quota PLLM et les sondes sont des opérations de service séparées ; aucune valeur de secret n’est publiée. Aucun profil navigateur ni test web n’est nécessaire au profil mémoire.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-07T20:46:01.171529+00:00 (UTC) |
| Fin — après archivage et sonde finale | 2026-10-07T21:55:36.419500+00:00 (UTC) |
| Durée globale (pauses et attentes incluses) | 01 h 09 min 35 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-07T20:46:01.171529+00:00 | N/A | N/A |
| Après — après archivage | 2026-10-07T21:55:36.419500+00:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif Codex get_usage_limits absent : aucun relevé de la fenêtre codex/10080 minutes n’est disponible. Aucune conversion en tokens ou monnaie et aucune reconstruction. Les quotas sont partagés par le compte ; une variation, si mesurable, pourrait inclure d’autres tâches.

| Domaine | Appels et part globale | Autorisés/exécutés et taux | Refusés et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| Fichiers | 9 (6.7 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 17 (12.7 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 108 (80.6 %) | 100 (92.6 %) | 0 (0.0 %) | 8 (7.4 %) |
| Total général | 134 (100.0 %) | 126 (94.0 %) | 0 (0.0 %) | 8 (6.0 %) |

Bilans : 130 tests réussis ; trois compilations réussies ; validation du change stricte et globale réussie selon les critères applicables, seuil de longueur exclu et code strict canon 1 qualifié. Archive réussie sans mise à jour des canons. Git non inspecté, aucun commit/push/branche. Aucun test PostgreSQL ou effet métier, aucune dépendance ni façade ajoutée. Secrets PLLM utilisés seulement par le processus sécurisé et l’authentification native, sans valeur transmise au modèle ou aux sources. Cadences de pilotage : SSE direct, contrôle 3 s, rédaction 7 s, sondes 30 min. Ce jalon mémoire ne réalise ni purge ni persistance durable ni propagation/restauration sans résurrection ; le cycle CISMP parent reste à poursuivre.

Preuves principales : état non secret output/cismp-state.json et historiques natifs des deux sessions listées ci-dessous. Les sondes jetables sont documentées dans leur tableau.

- ses_ee7e5b06fffeuSdw6vP3oIjrG0
- ses_ee7d5a17bffeFr0I2iT6pQFZAg
