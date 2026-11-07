# Statistiques — add-initial-bulk-commit-mode-vocabulary

RUN cismp-pixs-20261008-125817. Périmètre : préparation, pilotage, récupération et livraison de cette première archive dans les quatre sessions maîtresses du RUN. La rédaction/publication de ce rapport est hors intervalle. Aucun état Git inspecté.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go | xhigh | 1.99 s | 84.45 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex GPT-6 | N/A | OpenAI | N/A | N/A | N/A | N/A |

Versions exactes et temps de génération actifs non exposés ; aucun dénominateur de service fiable. Les durées de tours incluent des outils/attentes et ne sont pas utilisées comme temps de service. Orchestrateur non sondé.

## 1. Statistiques générales et décisions

Durée calendaire 01 h 37 min 50 s, pauses et attentes incluses. Résultat : Enum de quatre modes, 20 tests réussis, compilation/chargement et stricts code 0, archive réussie sans modification du canon.

Messages : 171 ; outils : 146. Décisions CAB : approved=21 (95.5 %), rejected=1 (4.5 %). Une décision refusée pour commande divergente, deux appels natifs refusés sans effet et trois récupérations natives de session ; délais MCP récupérés par polling corrélé.

Tokens natifs agrégés : input=840, output=71843, reasoning=0, cache_read=6451665, cache_write=879007. Coût natif agrégé info.cost=0.31292025, unité/devise non précisée par la source. Compactages : aucun appel natif observé ; échéance 1 h 30 non exécutée, APIs conjointes non exposées dans cette session.

Convention : succès = appel terminé avec succès (catégorie approuvé/exécuté), sans preuve implicite d’approbation manuelle pour les lectures ; refus = permission explicitement bloquée ; erreur = délai/interruption/autre échec technique. Les décisions CAB sont comptées séparément des résultats d’outils.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 30 | 17.5 % |
| assistant | 141 | 82.5 % |
| Total | 171 | 100 % |

Parties : text=119 (17.4 %), step-start=140 (20.4 %), reasoning=140 (20.4 %), tool=146 (21.3 %), step-finish=140 (20.4 %). Terminaisons : tool-calls=112 (79.4 %), stop=28 (19.9 %), interrompu/incomplet=1 (0.7 %).

| Catégorie | Total | Part | Succès | Refus | Erreur |
|---|---:|---:|---:|---:|---:|
| bash | 14 | 9.6 % | 13 (92.9 %) | 1 (7.1 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 32 | 21.9 % | 32 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 12 | 8.2 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 22 | 15.1 % | 18 (81.8 %) | 0 (0.0 %) | 4 (18.2 %) |
| glob | 6 | 4.1 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 25 | 17.1 % | 25 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 26 | 17.8 % | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 | 4.8 % | 6 (85.7 %) | 1 (14.3 %) | 0 (0.0 %) |
| Total | 146 | 100 % | 140 (95.9 %) | 2 (1.4 %) | 4 (2.7 %) |

## 3. Fichiers modifiés

Tentatives d’écriture natives, et non nombre de fichiers uniques.

| Catégorie | Total | Part | Succès | Refus | Erreur |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-commit-mode-vocabulary/design.md | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-commit-mode-vocabulary/proposal.md | 2 | 28.6 % | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-commit-mode-vocabulary/specs/bulk-operations/spec.md | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-commit-mode-vocabulary/tasks.md | 2 | 28.6 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operations.py | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 7 | 100 % | 6 (85.7 %) | 1 (14.3 %) | 0 (0.0 %) |

Les quatre artefacts OpenSpec ont été déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-08-add-initial-bulk-commit-mode-vocabulary. Un seul module Python ajouté ; cadrages, dépendances, façade et canon inchangés. STATISTIQUES.md est la publication distincte hors des totaux ci-dessus.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreur |
|---|---:|---:|---:|---:|---:|
| OpenSpec | 4 | 28.6 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol true | 5 | 35.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 5 | 35.7 % | 4 (80.0 %) | 1 (20.0 %) | 0 (0.0 %) |
| Total | 14 | 100 % | 13 (92.9 %) | 1 (7.1 %) | 0 (0.0 %) |

Commandes natives refusées (libellés ≤100 caractères) :

| Commande | Nombre | Part des appels Bash | Statut |
|---|---:|---:|---|
| /home/devops/python/current/bin/python3 -I -B -c 'import sys\nsys.path.insert(0, "src")\nimport jso… | 1 | 7.1 % | Refusée avant exécution |

Le mandat composé divergent rejeté au niveau CAB n’a produit aucun appel Bash et n’est pas ajouté aux commandes exécutées.

## 5. Accès web

Aucun appel webfetch/websearch : 0 succès, 0 refus, 0 erreur ; pourcentages N/A (dénominateur zéro). Aucune URL effectivement visitée par ces outils. Les transports LLM, quotas et APIs locales ne sont pas assimilés à des visites web ; leur nombre HTTP exhaustif est N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — première session maîtresse | 08/10/2026 14:59:12 +0200 |
| Fin — après archive et sonde finale | 08/10/2026 16:37:03 +0200 |
| Durée globale (pauses et attentes incluses) | 01 h 37 min 50 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits absent : aucun quota reconstitué ni quota OpenCode substitué. Le quota est partagé par le compte ; sa variation éventuelle ne serait pas attribuable exclusivement à ce change.

| Catégorie | Total | Part | Succès | Refus | Erreur |
|---|---:|---:|---:|---:|---:|
| Autres outils | 125 | 85.6 % | 121 (96.8 %) | 0 (0.0 %) | 4 (3.2 %) |
| Commandes | 14 | 9.6 % | 13 (92.9 %) | 1 (7.1 %) | 0 (0.0 %) |
| Fichiers | 7 | 4.8 % | 6 (85.7 %) | 1 (14.3 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 146 | 100 % | 140 (95.9 %) | 2 (1.4 %) | 4 (2.7 %) |

Sondes dédiées sans outils, même modèle/fournisseur/xhigh et prompt fixe :

| Position | Envoi UTC | TTMT | Tokens/s | Tokens sortie | Résultat |
|---|---|---:|---:|---:|---|
| début | 2026-10-08T13:02:01.314417+00:00 | 1.90 s | 79.53 | 3279 | Réussie |
| +30 min | 2026-10-08T13:32:49.422320+00:00 | 1.66 s | 89.27 | 3222 | Réussie |
| +60 min | 2026-10-08T14:02:33.746048+00:00 | 2.10 s | 78.28 | 3405 | Réussie |
| fin change / +90 min | 2026-10-08T14:32:34.933806+00:00 | 2.29 s | 90.71 | 3175 | Réussie |

4 prévues/relevées, 4 réussies, 0 échouée, 0 manquée ; décalages réels de démarrage visibles dans les horodatages. TTMT min/max 1.66/2.29 s ; débit min/max 78.28/90.71 tokens/s. Surcharge de télémétrie : 13081 tokens de sortie, hors production ; coût initial N/A donc coût total des sondes N/A.

Tests : 20 réussis, aucun échec/skip ; PostgreSQL et navigateur non applicables au module pur. Archive réalisée code 0. Avertissement non bloquant de proposition : entêtes français non reconnus comme Why/What Changes par la CLI ; aucune nouvelle norme. Git non inspecté/modifié. Secret PLLM utilisé seulement par le processus sécurisé autorisé, jamais fourni au modèle ou au rapport. Cycle global incomplet : reprise de sélection et arrêt/fermeture OpenCode demandés à 16 h 40 Paris.
