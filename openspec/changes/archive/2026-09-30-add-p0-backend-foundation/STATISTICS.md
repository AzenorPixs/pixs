# STATISTIQUES — add-p0-backend-foundation

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-backend-foundation. RUN parent : cismp-pixs-20260929-2033. OpenCode 1.18.33, CAB 0.85.3.

Comptes de production partiels : les deux sessions HIGH disponibles sont agrégées avant rédaction. L'ancienne session de préparation est indisponible (404) : ses messages, outils, coût et provenance détaillée restent N/A. Les sondes conservées sont présentées séparément. Les outils et messages propres à la rédaction du présent rapport sont hors intervalle.

- ses_f0f56871effeGSGeh7E5Tu76wd : 163 messages.
- ses_f0ecd09c8ffeTzzapPYlvxAdPE : 138 messages.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | MEDIUM — préparation | 3.613 s | 264.502 | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | HIGH | 5.939 s | 96.275 | N/A |
| muse-spark-1.3-contributor — compaction | N/A | opencode-go | N/A — absent des métadonnées | N/A | N/A | N/A |

La version exacte du modèle n'est pas exposée ; 1.3 n'est pas utilisée comme version télémétrique. Temps de génération active et dénominateur cumulé N/A : les durées des messages incluent outils/attentes et ne mesurent pas le service du modèle. Les activités simultanées sont possibles. La durée calendaire ci-dessous n'est pas un temps de génération.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root — modèle exact N/A | N/A | N/A — télémétrie modèle indisponible | N/A | N/A | N/A | N/A |
| Contexte Codex de rappel CAB — modèle N/A | N/A | N/A | N/A | N/A | N/A | N/A |

Aucune sonde orchestrateur. Le contexte de rappel a publié recovery06 et strict02 ; ces décisions ne prouvent pas une publication par /root. Prévol recovery07/recovery08 et strict03/strict04 ont ensuite été décidés explicitement par /root.

## 1. Statistiques générales et décisions

Intervalle global : 2026-09-30T03:51:26.327929+00:00 → 2026-09-30T08:46:53.595196+00:00 ; durée 04 h 55 min 27 s (pauses et attentes incluses).

| Rôle des messages | Nombre | Part |
|---|---|---|
| user | 55 | 18.3 % |
| assistant | 246 | 81.7 % |
| Total | 301 | 100.0 % |

| Résultat des appels natifs | Nombre | Part |
|---|---|---|
| completed | 180 | 94.2 % |
| error | 10 | 5.2 % |
| outside | 1 | 0.5 % |
| Total | 191 | 100.0 % |

Convention : completed = appel réussi autorisé nativement ou lecture sans permission, pas preuve d'approbation manuelle. error = erreur technique ou code retour non nul ; refused = refus de permission natif explicite. outside = une lecture externe consommée sans corrélation conforme, conservée à part. Les décisions CAB ne sont pas des appels Bash exécutés.

| Dernier statut CAB par requestId unique | Nombre | Part |
|---|---|---|
| NEEDS_CLARIFICATION | 1 | 2.5 % |
| APPROVED | 37 | 92.5 % |
| REJECTED | 1 | 2.5 % |
| CANCELLED | 1 | 2.5 % |
| Total | 40 | 100.0 % |

Une clarification et un refus CAB n'ont pas été exécutés ; un mandat a été annulé sans exécution. Les six erreurs request_validation sont des incidents de transport, distincts des refus. source-validate01 (2044 caractères) annulé après limite contrôleur 2000 ; source-validate02 (1982) prouvé. Deux décisions issues du contexte de rappel restent signalées ; le total APPROVED ne certifie pas l'identité manuelle de /root.

| Tokens observés (catégories distinctes) | Nombre | Part |
|---|---|---|
| input | 1342090 | 5.6 % |
| output | 63659 | 0.3 % |
| reasoning | 25331 | 0.1 % |
| cache_read | 22749424 | 94.1 % |
| cache_write | 0 | 0.0 % |
| Total | 24180504 | 100.0 % |

Coût de production connu des deux sessions disponibles : 0.197505848 (unité native non exposée). Total toutes phases N/A : préparation perdue. Compactions observées : 2, coût cumulé connu 0.0115162, inclus dans la production. Leurs résumés obsolètes ont été corrigés avant tout nouveau mandat.

| Position | Envoi / échéance UTC | Succès | Tokens sortie | TTMT s | Tokens/s | Premier événement | Dernier événement |
|---|---|---|---|---|---|---|---|
| debut | 2026-09-30T03:51:26.327929+00:00 | oui | 458 | 3.613 | 264.502 | 230811.696474183 | 230813.428030205 |
| debut_reprise_HIGH | 2026-09-30T05:59:33.732402+00:00 | échec | 484 | 0.036 | 28.840 | 101091.58137288 | 101108.363726508 |
| debut_reprise_HIGH_retry1 | 2026-09-30T06:01:18.252428+00:00 | oui | 458 | 5.341 | 176.544 | 101201.406343494 | 101204.000603258 |
| +30 minutes | 2026-09-30T06:33:22.476125+00:00 | oui | 499 | 6.814 | 40.826 | N/A | N/A |
| +60 minutes prévue | 2026-09-30T07:03:22.476125+00:00 | manquée | N/A | N/A | N/A | N/A | N/A |
| début reprise2 HIGH avec deny external | 2026-09-30T07:27:39.380704+00:00 | oui | 490 | 5.568 | 48.371 | 2026-09-30T07:27:44.948399+00:00 | 2026-09-30T07:27:55.078533+00:00 |
| +30 min depuis reprise2 HIGH | 2026-09-30T08:09:13.664084+00:00 | oui | 483 | 9.616 | 45.199 | 2026-09-30T08:09:23.280050+00:00 | 2026-09-30T08:09:33.966037+00:00 |
| +60 min depuis reprise2 HIGH | 2026-09-30T08:39:26.191785+00:00 | oui | 504 | 4.909 | 52.795 | 2026-09-30T08:39:31.100985+00:00 | 2026-09-30T08:39:40.647304+00:00 |
| fin après archivage backend | 2026-09-30T08:45:46.063719+00:00 | oui | 474 | 3.383 | 213.916 | 2026-09-30T08:45:49.446659+00:00 | 2026-09-30T08:45:51.662482+00:00 |

| Configuration | Tentatives conservées | Réussies | Échouées | Manquées | TTMT min/max s | Débit min/max |
|---|---|---|---|---|---|---|
| MEDIUM | 1 | 1 | 0 | 0 | 3.613 / 3.613 | 264.502 / 264.502 |
| HIGH | 8 | 6 | 1 | 1 | 3.383 / 9.616 | 40.826 / 213.916 |

Sonde initiale HIGH invalide : événement utilisateur inclus ; exclue de toutes moyennes et retentée une seule fois. +60 min ancien segment manquée pendant récupération, jamais recréée. Retards des relèves conservés dans l'état : +30 initial 116.200 s, +30 reprise2 694.283 s, +60 reprise2 12.528 s. Certains premiers/derniers événements sont des instants monotones, UTC non conservé ; aucune conversion rétroactive inventée.

Surcharge de télémétrie séparée : 3850 tokens de sortie connus, dont 484 pour la tentative invalide ; coût connu 0.005558104 pour quatre relèves, coût complet N/A (premières relèves sans coût conservé). Durée complète de surcharge N/A. Ces tokens/coûts ne sont pas additionnés à la production.

Prompt identique des sondes : 3068 caractères UTF-8, SHA256 0d1c4b356ce0fcc754af10151e68a9fbbdf6d5dc8dc688d02da5760439079875. Sessions jetables, même modèle/fournisseur/raisonnement mesuré, zéro outil, sans accès fichier/web. Texte déterministe conservé dans output/cismp-state.json ; 64 lignes numérotées 01..64 de « calibration constante mesure sortie texte. », instruction de recopier sans introduction, conclusion, raisonnement métier ni outil.

Résultats : 26 tests dédiés initialement réussis ; découverte globale suivante 517 tests / une erreur ModuleNotFoundError test_pdp_decision, exit1. Régressions finales séparées : 404 unit + 127 integration = 531, exit0. AST Python3.11 cinq fichiers, UTF-8/LF treize fichiers, TOML/deltas canoniques conformes, strict04 exit0 ; neuf tâches cochées uniquement après preuve.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 108 | 9.3 % |
| step-start | 247 | 21.2 % |
| reasoning | 372 | 31.9 % |
| tool | 191 | 16.4 % |
| step-finish | 246 | 21.1 % |
| compaction | 2 | 0.2 % |
| Total | 1166 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
|---|---|---|
| tool-calls | 191 | 77.6 % |
| stop | 55 | 22.4 % |
| Total | 246 | 100.0 % |

| Outil | Appels | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| bash | 21 | 11.0 % | 20 | 95.2 % | 0 | 0.0 % | 1 | 4.8 % | 0 | 0.0 % |
| cgpt-validation_broker_health | 1 | 0.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 25 | 13.1 % | 25 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_cancel_approval | 1 | 0.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 8 | 4.2 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 0.5 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 5 | 2.6 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 40 | 20.9 % | 34 | 85.0 % | 0 | 0.0 % | 6 | 15.0 % | 0 | 0.0 % |
| edit | 8 | 4.2 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 10 | 5.2 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 0.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 62 | 32.5 % | 60 | 96.8 % | 0 | 0.0 % | 1 | 1.6 % | 1 | 1.6 % |
| write | 8 | 4.2 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 191 | 100.0 % | 180 | 94.2 % | 0 | 0.0 % | 10 | 5.2 % | 1 | 0.5 % |

## 3. Fichiers modifiés

| Chemin absolu | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-backend-foundation/specs/reference-runtime/spec.md | 1 | 6.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-backend-foundation/specs/runtime/spec.md | 1 | 6.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-backend-foundation/design.md | 1 | 6.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/pyproject.toml | 1 | 6.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/settings.py | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/checks.py | 1 | 6.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/__init__.py | 1 | 6.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_backend_settings.py | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_backend_foundation.py | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-backend-foundation/tasks.md | 2 | 12.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total tentatives natives | 16 | 100.0 % | 16 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Il s'agit de tentatives natives d'édition, pas de lignes modifiées. Les créations initiales de proposal/tasks/.openspec.yaml dans la session perdue sont N/A. pyproject.toml, quatre fichiers backend et deux tests sont les sept fichiers d'implémentation du périmètre. Six artefacts OpenSpec déplacés par l'unique commande archive01 : .openspec.yaml, proposal.md, design.md, tasks.md et deux deltas specs ; hashes identiques après déplacement, répertoire actif disparu. Les écritures internes de CLI ne sont pas comptées comme six appels edit. Une lecture externe non corrélée est comptée dans Autres outils, sans écriture source. Ce rapport est écrit après la borne et exclu des tentatives ci-dessus.

## 4. Commandes

| Famille native | Nombre | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| Prévols inoffensifs | 7 | 33.3 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Configuration OpenCode | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 7 | 33.3 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Environnement isolé | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Installation isolée | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests | 4 | 19.0 % | 3 | 75.0 % | 0 | 0.0 % | 1 | 25.0 % |
| Total | 21 | 100.0 % | 20 | 95.2 % | 0 | 0.0 % | 1 | 4.8 % |

| Commande native (100 caractères max) | Nombre | Part | Résultat |
|---|---|---|---|
| /usr/bin/true | 7 | 33.3 % | {'completed': 7} |
| /home/devops/python/current/bin/python3 -c "import json; from pathlib import Path; p=Path('.opencod… | 1 | 4.8 % | {'completed': 1} |
| /home/devops/.local/npm/bin/openspec validate add-p0-backend-foundation --strict | 1 | 4.8 % | {'completed': 1} |
| /home/devops/python/current/bin/python3 -m venv .venv-backend-foundation | 1 | 4.8 % | {'completed': 1} |
| /home/devops/datas/pixs/.venv-backend-foundation/bin/python -m pip --isolated install --index-url h… | 1 | 4.8 % | {'completed': 1} |
| /home/devops/datas/pixs/.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.i… | 1 | 4.8 % | {'completed': 1} |
| /home/devops/datas/pixs/.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.i… | 1 | 4.8 % | {'error': 1} |
| /home/devops/datas/pixs/.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.i… | 1 | 4.8 % | {'completed': 1} |
| /home/devops/datas/pixs/.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.i… | 1 | 4.8 % | {'completed': 1} |
| /home/devops/python/current/bin/python3 -B -c 'import ast, hashlib, json, re, tomllib ↵ from pathli… | 1 | 4.8 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-backend-foun… | 3 | 14.3 % | {'completed': 3} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive --help | 1 | 4.8 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-backend-found… | 1 | 4.8 % | {'completed': 1} |

| Commande refusée par CAB, non exécutée (100 caractères max) | Demandes | Part des demandes refusées |
|---|---|---|
| /home/devops/python/current/bin/python3 -c 'import json; from pathlib import Path; p=Path(".opencod… | 1 | 100.0 % |
| Total demandes refusées, hors appels natifs | 1 | 100.0 % |

Le refus CAB highconfig-read01 n'a créé aucun appel Bash ; il n'est pas ajouté aux 21 appels natifs. La demande source-validate01 annulée sans exécution est également hors appels natifs. Pas de rejeu de permission consommée. Le code retour 1 des tests est une erreur technique, pas un refus.

## 5. Accès web

| Périmètre | Approuvés/visités | Refusés | Erreurs | Total | Part |
|---|---|---|---|---|---|
| Outils web agents de codage | 0 | 0 | 0 | 0 | N/A |
| Total outils web | 0 | 0 | 0 | 0 | N/A — dénominateur zéro |

Aucune URL visitée ou refusée par webfetch/websearch dans les deux historiques. Politique native deny webfetch/websearch/task/external_directory vérifiée après reprise. L'installation pip antérieure avait été autorisée séparément sur https://pypi.org/simple ; c'est un effet réseau d'une commande, pas un appel webfetch. L'inférence auprès du fournisseur n'est pas une navigation de l'agent.

| Accès orchestrateur connu, comptes complets N/A | Statut |
|---|---|
| https://pypi.org/pypi/Django/5.2.17/json | visité auparavant — métadonnées officielles |
| https://pypi.org/pypi/psycopg/3.3.5/json | visité auparavant — métadonnées officielles |

Ces deux visites connues ne constituent pas un décompte complet du pilotage et ne sont pas ajoutées aux totaux natifs de codage. Aucune URL refusée n'est présentée comme visitée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-30T03:51:26.327929+00:00 |
| Fin — après archivage et sonde finale | 2026-09-30T08:46:53.595196+00:00 |
| Durée globale (pauses et attentes incluses) | 04 h 55 min 27 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-09-30T03:51:26.327929+00:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-30T08:46:53.595196+00:00 | N/A | N/A |
| Différence après − avant | — | N/A points de pourcentage | — |

Outil natif get_usage_limits non exposé, vérifié avant et après. Aucune lecture de remplacement : quota codex, fenêtre10080min, usedPercent/resetsAt N/A. Quotas partagés par le compte ; exclusivité de cette session et identité de fenêtre non vérifiables, aucune consommation reconstruite.

| Domaine | Total | Part globale | Réussis | Taux | Refusés natifs | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| Fichiers (éditions) | 16 | 8.4 % | 16 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes natives | 21 | 11.0 % | 20 | 95.2 % | 0 | 0.0 % | 1 | 4.8 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 154 | 80.6 % | 144 | 93.5 % | 0 | 0.0 % | 9 | 5.8 % | 1 | 0.6 % |
| Total global | 191 | 100.0 % | 180 | 94.2 % | 0 | 0.0 % | 10 | 5.2 % | 1 | 0.5 % |

Totaux croisés : types d'outils = domaines = 191 appels ; messages 301 ; décisions CAB 40 requestId distincts. Décisions CAB et appels natifs ont des dénominateurs distincts, sans double comptage.

531 régressions finales passent, strict04 et archive01 exit0. Archive réelle vérifiée : six artefacts identiques, canoniques inchangés, neuf tâches prouvées cochées. Fondation partielle hors base uniquement : aucun service opérationnel, persistance PostgreSQL, résolution de secrets ou conformité globale P0 prouvés. Incident de lecture externe : session interrompue, reprise développeur autorisée, nouvelle session HIGH avec deny externe et tests séparés. Reprise documentaire ultérieure explicitement validée, circularité3.3 corrigée avant cochage. Aucun Git inspecté/commit/push dans ce RUN selon les preuves conservées ; provenance complète N/A sans inspection Git. Aucun secret réel ni opération PostgreSQL réel dans les mandats observés. Le cycle parent poursuit SÉLECTION sans arrêt CAB à ce jalon.
