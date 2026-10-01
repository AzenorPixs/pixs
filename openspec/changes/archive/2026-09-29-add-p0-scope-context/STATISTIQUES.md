# Statistiques — add-p0-scope-context

Session OpenCode `ses_f130e4e87ffeaY8YzgPakaCCOl`, RUN `cismp-pixs-20260929-1134`. Archive : `/home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-scope-context`.
Intervalle mesuré : 2026-09-29T12:13:56.519Z à 2026-09-29T13:02:39.239Z, avant rédaction de ce rapport. Historique persistant du premier message `msg_0ed165fce001etWLWOKzL41P3d` au dernier `msg_0ed41c433001GgYG57ZGUQgvOk`. RSMP, prévols antérieurs, sondes et rédaction du rapport exclus des compteurs de production. Les appels de pilotage de l'orchestrateur ne sont pas agrégés : télémétrie exhaustive exportable indisponible.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Muse Spark (identifiant muse-spark-1.3-contributor) | N/A — version exacte non exposée | opencode-go | low | 2.127 s | 242.259 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — non exposée | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A |

Le temps de service et son dénominateur cumulé sont indisponibles : les durées des messages incluent appels d'outils et attentes. Elles ne sont pas assimilées à du temps de génération. Les versions exactes ne sont pas déduites des noms de modèles. Aucun agent orchestrateur n'a été sondé.

## 1. Statistiques générales et décisions

Durée calendaire : 00 h 48 min 42 s, pauses, attentes, tests et archivage inclus. 190 messages, 123 appels d'outils. Un appel réussi désigne un appel terminé avec succès et autorisé ; cela ne prouve pas à lui seul une approbation manuelle. Les 36 mandats unitaires CAB ont chacun une décision CGPT APPROVED corrélée et une opération native : 22 éditions et 14 commandes. Les lectures natives ne nécessitent pas de mandat d'écriture.

| Catégorie | Nombre | Part |
|---|---|---|
| Appels réussis | 120 | 97.6 % |
| Refus de permission | 0 | 0.0 % |
| Erreurs techniques | 3 | 2.4 % |
| Total | 123 | 100 % |

| Catégorie | Nombre | Part |
|---|---|---|
| Mandats APPROVED | 36 | 100.0 % |
| Mandats REJECTED | 0 | 0.0 % |
| Total | 36 | 100 % |

Les trois erreurs techniques sont deux délais MCP de `scope-design01` (request_validation et poll_approval), récupérés par get_approval corrélé avant une édition unique, et la lecture de l'ancien dossier après archivage, absent comme attendu. Aucun échec de test. Des corrections de revue et un complément après édition partielle ont reçu des mandats neufs ; aucune permission consommée n'a été rejouée.

Compteurs de tokens cumulés fournis par l'API : entrée 1293053, sortie 38616, raisonnement 1798, cache lu 21448517, cache écrit 0. Ces compteurs sont présentés séparément sans supposer leur additivité. Champ `cost` cumulé : 0.180285134 (151 relevés) ; devise et facture réelle non fournies par cette extraction. Compactions observées dans cet intervalle : 0.

| Validation | Résultat | Part du total de tests |
|---|---|---|
| Unitaires | 228/228 réussis (100 %) | 72,6 % |
| Intégration | 86/86 réussis (100 %) | 27,4 % |
| Total tests | 314/314 réussis (100 %) | 100 % |

OpenSpec strict : 77/77 (100 %), zéro échec ; les notes INFO de longueur d'exigences et skip_specs sont conservées comme informations. Syntaxe Python : 10/10 (100 %). UTF-8/LF : 14/14 (100 %). Tâches : 15/15 (100 %).

Sondes isolées, même modèle/fournisseur/raisonnement, zéro outil : 3 prévues, 3 réussies (100 %), 0 échouée (0 %), 0 manquée (0 %). La relève +30 min est partie à 12:44:16 UTC, environ 14 s après son échéance. Le prompt constant demandait exactement 64 lignes « alpha beta gamma delta epsilon zeta eta theta. », sans commentaire ni numérotation.

| Position | Fin UTC | TTMT | Tokens sortie | Durée sortie | Débit tokens/s | Preuve |
|---|---|---|---|---|---|---|
| Début | 2026-09-29T12:14:02.596Z | 2.230 s | 585 | 3.788 s | 154.450 | msg_0ed15fda7001JpIX2YIgmBH4ah |
| +30 min | 2026-09-29T12:44:21.200Z | 2.488 s | 586 | 2.100 s | 279.057 | msg_0ed31c349001BJNP3ls53AsMG8 |
| Fin | 2026-09-29T13:02:31.567Z | 1.664 s | 586 | 1.998 s | 293.269 | msg_0ed426a2c001FRtrDz3208ZygJ |

TTMT moyen 2.127 s (min 1.664, max 2.488). Débit moyen arithmétique 242.259 tokens/s (min 154.450, max 293.269).
Surcharge des sondes séparée : 1757 tokens de sortie, 7.886 s entre premiers et derniers événements de sortie cumulés. Coût et durée totale des sessions de sonde : N/A, relevés insuffisants. Les instants monotoniques envoi/premier/dernier sont conservés pour les sondes périodique et finale dans l'état du RUN ; ceux de la sonde initiale ne sont plus disponibles, ses métriques et sa preuve restent conservées.

## 2. Types de messages et d'outils

| Catégorie | Nombre | Part |
|---|---|---|
| user | 39 | 20.5 % |
| assistant | 151 | 79.5 % |
| Total | 190 | 100 % |

Parties de messages (les parties reasoning sont comptées sans exposer leur contenu) :

| Catégorie | Nombre | Part |
|---|---|---|
| text | 78 | 10.3 % |
| step-start | 151 | 20.0 % |
| reasoning | 252 | 33.4 % |
| tool | 123 | 16.3 % |
| step-finish | 151 | 20.0 % |
| Total | 755 | 100 % |

Terminaisons des réponses assistant :

| Catégorie | Nombre | Part |
|---|---|---|
| tool-calls | 112 | 74.2 % |
| stop | 39 | 25.8 % |
| Total | 151 | 100 % |

| Type | Total | Part | Réussis | Refusés | Erreurs |
|---|---|---|---|---|---|
| cgpt-validation_request_validation | 36 | 29.3 % | 35 (97.2 %) | 0 (0.0 %) | 1 (2.8 %) |
| bash | 14 | 11.4 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 15 | 12.2 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 44 | 35.8 % | 43 (97.7 %) | 0 (0.0 %) | 1 (2.3 %) |
| edit | 7 | 5.7 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 3 | 2.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 0.8 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| glob | 2 | 1.6 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 123 | 100 % | 120 (97.6 %) | 0 (0.0 %) | 3 (2.4 %) |

## 3. Fichiers modifiés

Les chiffres sont des tentatives d'édition natives, pas des lignes modifiées. 14 cibles distinctes, 22 éditions réussies autorisées CAB. Les fichiers créés ou déplacés par une commande sont comptés dans les commandes pour éviter un double comptage.

| Type | Total | Part | Réussis | Refusés | Erreurs |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-scope-context/proposal.md | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-scope-context/.openspec.yaml | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-scope-context/design.md | 2 | 9.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-scope-context/tasks.md | 2 | 9.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/scope/context.py | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/scope/topology.py | 2 | 9.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/scope/ownership.py | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/scope/propagation.py | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/scope/__init__.py | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/__init__.py | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_scope_context_structure.py | 2 | 9.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_scope_topology.py | 3 | 13.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_scope_ownership.py | 1 | 4.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_scope_propagation.py | 3 | 13.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 22 | 100 % | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

La création CLI a produit .openspec.yaml, puis ce fichier a été édité sous mandat. L'archivage a déplacé les quatre artefacts de `/home/devops/datas/pixs/openspec/changes/add-p0-scope-context/` vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-scope-context/`. Les quatre empreintes SHA-256 sont identiques avant/après, la source est absente. Aucun delta normatif synchronisé. Ce rapport, produit après la borne finale, n'est pas inclus dans les 22 éditions.

## 4. Commandes

| Type | Total | Part | Réussis | Refusés | Erreurs |
|---|---|---|---|---|---|
| OpenSpec | 11 | 78.6 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python tests et AST | 3 | 21.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 | 100 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères, occurrences réelles :

| Commande | Occurrences | Part | Réussite | Refus | Erreur |
|---|---|---|---|---|---|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec list --json | 2 | 14.3 % | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec new change add-p0-scope-cont… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec status --change add-p0-scope… | 2 | 14.3 % | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec instructions proposal --chan… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 14.3 % | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/python/current/bin/python3 -B -c 'import ast from pathlib import Path files = ["src/pi… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec instructions archive --chang… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive --help | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-scope-context… | 1 | 7.1 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| Total | 14 | 100 % | 14 (100 %) | 0 (0 %) | 0 (0 %) |

Aucune commande refusée (0/14, 0 %). Aucun test Bash/shellcheck applicable : aucun script shell créé ou modifié. Toutes les commandes observées ont le code de sortie 0.

## 5. Accès web

Aucun outil web ni URL visitée ou refusée dans la session de codage sur cet intervalle. Les requêtes locales de pilotage OpenCode/CAB de l'orchestrateur sont distinctes d'accès web de recherche et exclues des compteurs de production.

| Statut | Nombre | Taux |
|---|---|---|
| Approuvés/exécutés | 0 | N/A |
| Refusés | 0 | N/A |
| Erreurs | 0 | N/A |
| Total | 0 | N/A — dénominateur nul |

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-29T12:13:56.519Z |
| Fin — après archivage | 2026-09-29T13:02:39.239Z |
| Durée globale (pauses et attentes incluses) | 00 h 48 min 42 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A — outil natif non exposé | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-29T13:02:39.239Z (constat d'indisponibilité) | N/A | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | — |

Les quotas sont partagés par le compte. Une variation pourrait inclure d'autres tâches simultanées ; aucune attribution exclusive n'est faite. Aucun quota Spark ou restant n'a été substitué au quota Codex hebdomadaire.

| Type | Total | Part | Réussis | Refusés | Erreurs |
|---|---|---|---|---|---|
| autres | 87 | 70.7 % | 84 (96.6 %) | 0 (0.0 %) | 3 (3.4 %) |
| commandes | 14 | 11.4 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 22 | 17.9 % | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 123 | 100 % | 120 (97.6 %) | 0 (0.0 %) | 3 (2.4 %) |

Totaux croisés : 22 fichiers + 14 commandes + 0 web + 87 autres = 123 outils ; 120 réussis + 0 refusés + 3 erreurs = 123. Les 36 mandats tous approuvés correspondent aux 36 opérations mutantes ou commandes, sans doublon.

Résultat : bibliothèque scope immuable, topologie, propriété et propagation stricte, 314 tests verts et 15 tâches terminées. Archive vérifiée, spécifications principales inchangées par l'archivage. Git non inspecté, aucun commit/push. Aucune lecture de source secrète ni accès externe par l'agent de codage observé dans ce périmètre. La provenance Git reste non évaluée. Persistance, PDP/PEP, audit durable, runtime et composition P0 restent hors de ce change. Le RUN CISMP parent poursuit ensuite la sélection.
