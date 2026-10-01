# STATISTIQUES — add-p0-example-component

Session persistante : `ses_f1120eca1ffenF5n37NcrleooA`. RUN : `cismp-pixs-20260929-2033`. Racine : `/home/devops/datas/pixs`. Intervalle : 2026-09-29T22:12:03.183651+00:00 à 2026-09-29T22:55:32.434783+00:00 (UTC), fixé après archivage et sonde finale, avant rédaction. Historique natif complet filtré sur messages créés ou terminés dans ces bornes ; la réponse CAB de création, commencée quelques secondes avant la borne, est incluse car achevée dans l'intervalle. Les travaux précédents et la rédaction de ce rapport sont exclus. Les compteurs concernent OpenCode ; les compteurs et temps de génération Codex ne sont pas exposés.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | opencode-go | MEDIUM vérifié | 3.343 s | 95.676 | N/A — durée active complète non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version exacte non exposée | OpenAI | MEDIUM demandé ; télémétrie N/A | N/A | N/A | N/A |

Le temps calendaire, les attentes CAB et les outils ne sont pas du temps de service modèle. Aucun dénominateur fiable de service cumulé n'est exposé : durées, parts et chevauchements N/A.

## 1. Statistiques générales et décisions

150 messages (100 %) : 30 utilisateur (20.0 %) et 120 assistant (80.0 %). 89 appels d'outils (100 %) : 86 réussis (96.6 %), 1 refusé (1.1 %), 2 en erreur (2.2 %). 29 mandats CAB (32.6 % des outils) : 28 APPROVED (96.6 %), 1 REJECTED (3.4 %), chacun unitaire. Les 28 approuvés couvrent 16 éditions (57.1 %) et 12 commandes (42.9 %), toutes réellement exécutées une fois ; une commande autorisée a échoué. Les lectures réussies ne prouvent pas une approbation manuelle. Le REJECTED est la décision explicite de CGPT de geler le mandat TOML avant toute écriture, après le glob d'un répertoire absent ; ce gel opérationnel ne constitue pas un échec de test. Le test de code 1 est une erreur d'exécution autorisée, jamais un refus.

Incidents : glob natif sur nouveau répertoire inexistant (1 erreur) ; test ciblé initial 11 réussites sur 12 (91.7 %), 1 échec (8.3 %) car fixture ALLOW sans chemin audité. Deux récupérations CAB distinctes ont prouvé `true` exit 0 et READY pending0 ; la lecture pending1 transitoire de la seconde récupération a été recontrôlée jusqu'à pending0, sans cause historique affirmée. Correctif du seul test d'audit, puis 12/12 unitaires ciblés et 6/6 intégration mémoire ciblés, tous 100 %. Régressions finales : 361 unitaires + 118 intégration = 479 réussis (100 %), 0 échec (0,0 %). Les exécutions ciblées ne sont pas additionnées aux 479 cas globaux. OpenSpec : 77 valides (100 %), 0 invalide (0,0 %), 14 INFO non bloquantes. AST : 4 Python (100 %). UTF8/LF : 11 fichiers (100 %). Dix tâches prouvées et cochées (100 %). Archive effective, sous-ensemble démonstratif seulement : aucune preuve de P0 global, Developer Kit complet ou intégration de référence réelle.

| Tokens rapportés (production) | Nombre | Part |
|---|---:|---:|
| input | 1395993 | 3.6 % |
| output | 32568 | 0.1 % |
| reasoning | 10389 | 0.0 % |
| cache_read | 37729686 | 96.3 % |
| cache_write | 0 | 0.0 % |
| Total | 39168636 | 100 % |

Somme télémétrique des cinq catégories OpenCode : 39168636 tokens (100 %). Coût rapporté 0.223650072 sur 120 réponses (100.0 %), unité monétaire non exposée N/A. Compactions signalées : 0 (0.0 %). Tokens/coût orchestrateur N/A.

### Sondes de performance (surcharge distincte)

Prompt constant dans trois sessions dédiées et supprimées, même configuration, aucun outil/fichier/réseau demandé :
`Sans outil, fichier ni réseau. Réponds uniquement avec exactement 64 lignes identiques, chacune contenant : alpha beta gamma delta epsilon zeta eta theta. Aucun commentaire, aucune numérotation.`

| Position | Envoi UTC | Message natif | Tokens sortie | TTMT (s) | Durée sortie (s) | Tokens/s |
|---|---|---|---:|---:|---:|---:|
| début | 2026-09-29T22:12:03.194984+00:00 | msg_0ef399404001nOxvvKnGYWv8Aw | 623 | 3.057822 | 6.257304 | 99.563640 |
| +30 minutes | 2026-09-29T22:42:11.492114+00:00 | msg_0ef552bb10013gSQkIH3z5Kjab | 599 | 3.259637 | 6.346856 | 94.377432 |
| fin | 2026-09-29T22:54:24.544639+00:00 | msg_0ef605b2c001JGvpL6OsFrUS9E | 599 | 3.712891 | 6.434764 | 93.088109 |

3 prévues (100 %), 3 réussies (100 %), 0 échouée (0,0 %), 0 manquée (0,0 %). La relève +30 minutes est décalée de 8,3 s, explicitement observée et non reconstruite. TTMT moyen 3.343450 s, min 3.057822, max 3.712891 ; débit moyen arithmétique 95.676394 tokens/s, min 93.088109, max 99.563640. Instants monotoniques envoi/premier/dernier conservés dans l'état parent ; mesure SSE entre premier et dernier delta, tokens de sortie réels. Surcharge séparée : 1821 tokens de sortie (100 %), 29.069275 s envoi–dernier delta (100 %) ; coût et autres catégories de tokens des sondes N/A, non conservés. Aucun mélange avec la production ni temps de service modèle estimé.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part |
|---|---:|---:|
| assistant | 120 | 80.0 % |
| user | 30 | 20.0 % |
| Total | 150 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| step-start | 120 | 20.9 % |
| reasoning | 184 | 32.1 % |
| tool | 89 | 15.5 % |
| step-finish | 120 | 20.9 % |
| text | 61 | 10.6 % |
| Total | 574 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---:|---:|
| tool-calls | 89 | 74.2 % |
| stop | 31 | 25.8 % |
| Total | 120 | 100 % |

| Catégorie | Total | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cgpt-validation_request_validation | 29 | 32.6 % | 28 | 96.6 % | 1 | 3.4 % | 0 | 0.0 % |
| bash | 12 | 13.5 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |
| write | 13 | 14.6 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 20 | 22.5 % | 20 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 3 | 3.4 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 3 | 3.4 % | 2 | 66.7 % | 0 | 0.0 % | 1 | 33.3 % |
| cgpt-validation_broker_readiness | 6 | 6.7 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 2 | 2.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 1.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 89 | 100.0 % | 86 | 96.6 % | 1 | 1.1 % | 2 | 2.2 % |

Le refus de `request_validation` est une décision CAB REJECTED observée, malgré le transport MCP terminé. Le glob en erreur et le Bash exit1 sont classés erreurs. `list_pending` transporte aussi des entrées historiques : son count n'est pas une preuve du nombre de PENDING ; seule la readiness finale et la réconciliation ont validé la reprise.

## 3. Fichiers modifiés

Tentatives natives d'écriture (write/edit), et non nombre de lignes ou fichiers distincts : 16 réussies (100 %), 0 refusée (0,0 %), 0 en erreur (0,0 %), sur 10 chemins distincts. Le refus de mandat TOML est survenu avant l'appel natif ; il est compté séparément dans CAB/autres outils, sans inventer une écriture refusée.

| Catégorie | Total | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-p0-example-component/proposal.md | 1 | 6.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-example-component/design.md | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-example-component/tasks.md | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-example-component/specs/testing/spec.md | 1 | 6.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/example/component.toml | 1 | 6.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/example/demo.py | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/example/__init__.py | 1 | 6.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/example/README.md | 1 | 6.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_example_component.py | 3 | 18.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_example_composition.py | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 16 | 100.0 % | 16 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Le refus préalable `cismp-pixs-20260929-example-toml01` visait `/home/devops/datas/pixs/src/pixs/example/component.toml`, sans appel d'édition. L'archive a déplacé les quatre artefacts et `.openspec.yaml` vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-example-component/` ; opération générateur sous mandat distinct. Les six sources/test/docs sont restées à leurs chemins. La rédaction ultérieure de ce rapport est exclue de ces compteurs.

## 4. Commandes

| Catégorie | Total | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OpenSpec | 4 | 33.3 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 5 | 41.7 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % |
| CAB test true | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| AST et encodage | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 12 | 100.0 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |

Libellés des commandes (espaces normalisés, tronqués à 100 caractères maximum) ; parts par occurrence sur les 12 commandes réellement exécutées :

| Catégorie | Total | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/n…openspec new change add-p0-example-component` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/n…-example-component --strict --no-interactive` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/true` | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current…s tests/unit -p test_example_component.py -v` | 2 | 16.7 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current…ntegration -p test_example_composition.py -v` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current…on3 -B -m unittest discover -s tests/unit -v` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current…-m unittest discover -s tests/integration -v` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/home/devops/python/current/bin/python3 -B -c 'import a… 11 fichiers / delta canonique exact : OK")'` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/n…pec validate --all --strict --no-interactive` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/n… add-p0-example-component --yes --skip-specs` | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 12 | 100 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |

Commandes refusées : 0 (0,0 % des 12 commandes). Le mandat gelé concernait une édition TOML, aucune commande. Le code 1 est l'essai unitaire initial, puis repris avec requestId inédit ; aucune permission consommée n'a été rejouée.

## 5. Accès web

Outils d'accès web OpenCode dans l'intervalle : 0 ; approuvés 0, refusés 0, erreurs 0, pourcentages N/A (dénominateur nul). Aucune URL effectivement visitée par un outil web, aucune URL refusée. Communications locales de pilotage distinctes : API OpenCode `http://127.0.0.1:4096`, contrôleur `http://127.0.0.1:8788`, superviseur `http://127.0.0.1:8789`, sans secret. Le trafic fournisseur des modèles n'est pas un accès web explicite de l'agent ni quantifié par ces outils.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-29T22:12:03.183651+00:00 (UTC) |
| Fin — après archivage | 2026-09-29T22:55:32.434783+00:00 (UTC) |
| Durée globale (pauses et attentes incluses) | 0 h 43 min 29 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-09-29T22:12:03.183651+00:00 (UTC), contrôle d'exposition | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-29T22:55:32.434783+00:00 (UTC), contrôle d'exposition | N/A | N/A |
| Différence après − avant | — | N/A | — |

Cause : outil natif `mcp__codex_app__get_usage_limits` non exposé dans cette session aux deux contrôles, aucun relevé fabriqué. Les quotas sont partagés par compte ; toute variation éventuelle pourrait inclure d'autres travaux. Aucun quota restant/Spark, fichier de profil ou secret n'a été substitué. Bornes finales fixées après archive et sonde, avant rapport.

| Catégorie | Total | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fichiers natifs | 16 | 18.0 % | 16 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 12 | 13.5 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils (CAB compris) | 61 | 68.5 % | 59 | 96.7 % | 1 | 1.6 % | 1 | 1.6 % |
| Total | 89 | 100.0 % | 86 | 96.6 % | 1 | 1.1 % | 2 | 2.2 % |

Totaux croisés : 16 fichiers + 12 commandes + 0 web + 61 autres = 89 appels ; 86 réussis + 1 refusé + 2 erreurs = 89. Sommes types/parties/rôles/terminaisons et tokens vérifiées. Tests finaux 479/479 (100 %), OpenSpec 77/77 (100 %), archive réussie. Git non inspecté, aucun commit/push ; aucun accès à secret ou source exclue observé dans les outils de ce périmètre. Aucune modification des 44 chemins de fondations/cadrages vérifiés, aucun import de l'exemple depuis core/kernel. Les garanties globales P0/Kit/runtime et audit durable restent non prouvées. Le cycle parent CISMP doit poursuivre la sélection après validation de ce rapport.
