# STATISTIQUES — add-p0-source-filter-plan

Session persistante : `ses_f1120eca1ffenF5n37NcrleooA`. RUN : `cismp-pixs-20260929-2033`. Racine : `/home/devops/datas/pixs`. Intervalle de ce change : 2026-09-29T21:19:11.034367+00:00 à 2026-09-29T21:57:58.169635+00:00 (UTC), fixé après archivage et sonde finale, avant rédaction. Historique natif complet filtré par ces bornes ; les travaux CAB/configuration/RSMP antérieurs et la rédaction de ce rapport sont exclus. Les mesures de l'orchestrateur sont absentes de cette API.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | opencode-go | MEDIUM vérifié | 3.015 s | 411.882 | N/A — durée de génération complète non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version exacte non exposée | OpenAI | MEDIUM demandé ; télémétrie N/A | N/A | N/A | N/A |

Le temps calendaire, les appels d'outils et les attentes CAB ne sont pas du temps de service modèle. Aucun dénominateur fiable pour ce dernier n'est exposé ; ses durées, parts et chevauchements restent N/A.

## 1. Statistiques générales et décisions

160 messages (100 %), dont 30 utilisateur (18.8 %) et 130 assistant (81.3 %). 100 appels d'outils (100 %) : 98 réussis (98,0 %), 0 refusé (0,0 %), 2 en erreur (2,0 %). Les 28 mandats CAB (28.0 % des outils) ont reçu une décision manuelle APPROVED (28/28, 100 %), chacun pour une cible et une exécution. Un outil natif réussi ne prouve pas à lui seul une approbation manuelle : les lectures sans permission sont comptées comme réussites d'exécution. Un test de code 1 est une erreur d'exécution autorisée, jamais un refus de permission.

L'essai ciblé initial a produit 25 erreurs de fixtures sur 27 tests ; la récupération CAB avec requestId neuf a réussi, puis les fixtures corrigées ont passé 33 tests ciblés. Résultats finaux : 349 unitaires et 112 intégration, soit 461 tests réussis (100 %), 0 échec (0,0 %). Neuf tests d'intégration ciblés ont aussi réussi ; ces exécutions ciblées ne sont pas additionnées aux 461 cas de la dernière exécution globale. OpenSpec : 77 éléments valides (100 %), 0 invalide (0,0 %), avec 14 informations de longueur non bloquantes. AST : 5 fichiers Python valides (100 %). UTF-8/LF : 12 fichiers contrôlés (100 %). Dix tâches prouvées (100 %) et archivage effectif.

| Tokens rapportés (production) | Nombre | Part |
|---|---:|---:|
| input | 148663 | 0.6 % |
| output | 60896 | 0.3 % |
| reasoning | 22669 | 0.1 % |
| cache_read | 23263330 | 99.0 % |
| cache_write | 0 | 0.0 % |
| Total | 23495558 | 100 % |

Total télémétrique : 23495558 tokens (100 %). Les catégories entrée, cache lu, sortie, raisonnement et cache écrit sont celles retournées par OpenCode ; leur somme égale ce total. Coût rapporté : 0.07810596 sur 130 réponses (100.0 % des réponses assistant), unité monétaire non exposée donc N/A. Compactions signalées : 0 (0,0 % des messages). Les tokens et coûts de l'orchestrateur sont N/A.

### Sondes de performance (surcharge distincte)

Prompt constant : « Sans outil, fichier ni réseau. Réponds uniquement avec exactement 64 lignes identiques, chacune contenant : alpha beta gamma delta epsilon zeta eta theta. Aucun commentaire, aucune numérotation. » Sessions dédiées jetables, même modèle/fournisseur/MEDIUM, zéro outil. TTMT mesuré du départ client au premier delta texte SSE ; débit = tokens de sortie natifs / (dernier − premier delta). La version exacte n'est jamais déduite du nom.

| Position | Envoi UTC | Premier / dernier delta (horloge monotone, s) | Tokens | TTMT (s) | Débit (tokens/s) | État |
|---|---|---|---:|---:|---:|---|
| début | 2026-09-29T21:19:11.045275+00:00 | 207275.459850 / 207277.126942 | 607 | 2.659 | 364.107 | réussie |
| +30 min | 2026-09-29T21:49:23.682240+00:00 | 209088.446198 / 209090.496220 | 605 | 3.008 | 295.119 | réussie |
| fin | 2026-09-29T21:56:40.573232+00:00 | 209525.706039 / 209526.720926 | 585 | 3.377 | 576.419 | réussie |

Trois relèves prévues et réussies (3/3, 100 %), 0 échouée (0,0 %), 0 manquée (0,0 %). La relève +30 min a été envoyée 12,648 s après son échéance ; ce retard est conservé. TTMT moyen 3.015 s, min 2.659, max 3.377. Débit moyen arithmétique 411.882, min 295.119, max 576.419 tokens/s. Surcharge distincte : 1797 tokens de sortie, 13.776 s mesurées en client ; coût et tokens d'entrée N/A, absents du relevé conservé. Les sondes sont exclues des 160 messages et des tokens de production.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 30 | 18.8 % |
| assistant | 130 | 81.3 % |
| Total | 160 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 60 | 9.5 % |
| step-start | 130 | 20.6 % |
| reasoning | 212 | 33.5 % |
| tool | 100 | 15.8 % |
| step-finish | 130 | 20.6 % |
| Total | 632 | 100 % |

Seuls les comptes des parties de raisonnement sont utilisés, jamais leur contenu.

| Terminaison assistant | Nombre | Part |
|---|---:|---:|
| tool-calls | 100 | 76.9 % |
| stop | 30 | 23.1 % |
| Total | 130 | 100 % |

| Outil | Total | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 4 | 4.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 2 | 2.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 37 | 37.0 % | 36 | 97.3 % | 0 | 0.0 % | 1 | 2.7 % |
| cgpt-validation_request_validation | 28 | 28.0 % | 28 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| bash | 11 | 11.0 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |
| write | 14 | 14.0 % | 14 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 3 | 3.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 1.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 100 | 100 % | 98 | 98.0 % | 0 | 0.0 % | 2 | 2.0 % |

## 3. Fichiers modifiés

Ces valeurs comptent 17 tentatives d'écriture sur 9 chemins distincts, pas des lignes modifiées. Toutes sont autorisées par CAB et exécutées (17/17, 100 %), aucune refusée ou en erreur. Les lectures natives figurent dans les autres outils. La création du change et son déplacement par OpenSpec sont des commandes, sans duplication dans ce tableau.

| Chemin absolu complet | Total | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-p0-source-filter-plan/proposal.md | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-source-filter-plan/design.md | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-source-filter-plan/tasks.md | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-source-filter-plan/specs/authorization-engine/spec.md | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/authz/decision.py | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/authz/filter_plan.py | 3 | 17.6 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/authz/__init__.py | 1 | 5.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_filter_plan.py | 3 | 17.6 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_filter_plan_audit.py | 2 | 11.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 17 | 100 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Le générateur a créé `openspec/changes/add-p0-source-filter-plan/.openspec.yaml`. L'archivage a déplacé les artefacts vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-source-filter-plan`, avec `--skip-specs` car le delta était byte-équivalent au canonique déjà validé. Aucune dépendance nouvelle ; `pyproject.toml` est inchangé. Les deux fichiers RSMP spec canonique/TECHNICAL modifiés avant cet intervalle sont exclus de ces comptes.

## 4. Commandes

| Famille | Total | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OpenSpec | 4 | 36.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python unittest | 5 | 45.5 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % |
| Python AST/UTF-8/LF | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Test CAB true | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 11 | 100 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |

Les libellés ci-dessous sont limités à 100 caractères. Les commandes complètes exactes et leurs sorties restent dans l'historique natif ; la troncature est signalée.

| Commande (libellé tronqué) | Total | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec new change add-p0-source-fil… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-source-filte… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/python/current/bin/python3 -B -c 'import ast
from pathlib import Path
files = ["src/pi… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate --all --strict --no… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-source-filter… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 11 | 100 % | 7 | 63.6 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées : aucune (0/11, 0,0 %). Erreur : un essai unittest approuvé, code 1 pour fixtures invalides ; l'exécution de reprise a réussi sous nouveau mandat. Aucune permission consommée n'a été rejouée.

## 5. Accès web

Aucun outil web ni URL visitée/refusée observé : 0 accès, 0 approbation, 0 refus, 0 erreur ; les taux au sein du domaine vide sont N/A (dénominateur zéro). Part des accès web dans les 100 outils : 0,0 %. Les communications locales HTTP/SSE de pilotage ne sont pas des visites web de l'agent et ne sont pas incluses. Aucun accès externe de l'agent de codage n'est observé dans cet intervalle ; le trafic du service fournisseur n'est pas une métrique web exposée par cette API.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-29T21:19:11.034367+00:00 (UTC) |
| Fin — après archivage | 2026-09-29T21:57:58.169635+00:00 (UTC) |
| Durée globale (pauses et attentes incluses) | 0 h 38 min 47 s |

Les bornes concernent ce change dans la session persistante. Elles incluent sélection, revues, attentes, tests et archivage, sans addition de durées d'agents.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | Contrôle d'indisponibilité : 2026-09-29T21:19:11.034367+00:00 | N/A | N/A |
| Après — après archivage de la spécification | Contrôle d'indisponibilité : 2026-09-29T21:57:58.169635+00:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

L'outil natif `mcp__codex_app__get_usage_limits` n'est pas exposé ; aucune valeur n'a été substituée ou recréée. Identité du quota codex, fenêtre 10080 minutes, compte et réinitialisation non vérifiables : comparaison N/A. Ces quotas sont partagés par le compte et leur variation pourrait inclure d'autres travaux ; aucune consommation n'est attribuée exclusivement au change.

| Domaine | Total | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fichiers | 17 | 17.0 % | 17 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| commandes | 11 | 11.0 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % |
| web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| autres | 72 | 72.0 % | 71 | 98.6 % | 0 | 0.0 % | 1 | 1.4 % |
| Total | 100 | 100 % | 98 | 98.0 % | 0 | 0.0 % | 2 | 2.0 % |

Totaux croisés vérifiés : 17 écritures + 11 commandes + 0 web + 72 autres = 100 outils ; 98 réussites + 0 refus + 2 erreurs = 100. Les 28 décisions CAB APPROVED correspondent aux 17 écritures et 11 commandes ; les autres outils sont principalement lectures et transport CAB. Une lecture d'un artefact absent et l'essai unittest échoué constituent les deux erreurs d'exécution.

État final de ce change : tests, syntaxe, UTF-8/LF et OpenSpec valides, dix tâches prouvées et archive confirmée (`msg_0ef2b1359001cKY868ZY8Tw2jV`). Le RUN parent reste en SÉLECTION, gate OPEN : aucune fin globale n'est déduite de cet archivage. Le profil produit seulement un plan déclaratif ; PEP Django, filtrage à la source et audit durable restent non implémentés. Git n'a été ni inspecté ni modifié ; aucun commit/push. Aucun secret n'a été lu ou transmis par les outils observés de cet intervalle.
