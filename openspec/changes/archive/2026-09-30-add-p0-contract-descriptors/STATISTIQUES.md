# STATISTIQUES — add-p0-contract-descriptors

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-contract-descriptors. RUN parent : cismp-pixs-20260929-2033. OpenCode 1.18.33, CAB 0.85.3.

Historique natif complet du change courant, borné au premier message spécifique et à la fin après archivage/sonde finale. Les phases backend antérieures, la sélection parent et la rédaction de ce rapport sont exclues des comptes de production. Les sondes sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version télémétrique absente | opencode-go | HIGH | 4.166 s | 248.672 | N/A |
| muse-spark-1.3-contributor — compaction | N/A | opencode-go | N/A — variant absent | N/A | N/A | N/A |

Temps de génération active et dénominateur cumulé N/A : les durées natives incluent outils/attentes. La durée calendaire n'est pas un temps de service. Le nom 1.3 ne constitue pas une version télémétrique indépendante.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root — modèle exact N/A | N/A | N/A — télémétrie indisponible | N/A | N/A | N/A | N/A |

Aucune sonde orchestrateur. Toutes les décisions de ce change ont été publiées explicitement par /root après observation et comparaison du mandat réel. Aucun contexte de rappel n'a fourni une décision de ce change.

## 1. Statistiques générales et décisions

Intervalle calendaire : 2026-09-30T09:10:34.647122+00:00 → 2026-09-30T10:15:36.676626+00:00 ; durée 01 h 05 min 02 s, attentes incluses.

Session : ses_f0ecd09c8ffeTzzapPYlvxAdPE ; premier message msg_0f19691110015bL2OQkOFyECQk ; dernier message msg_0f1cea524001atpnl8CMp0A6wq ; 117 messages.

| Rôle des messages | Nombre | Part |
|---|---|---|
| user | 30 | 25.6 % |
| assistant | 87 | 74.4 % |
| Total | 117 | 100.0 % |

| Résultat des appels natifs | Nombre | Part |
|---|---|---|
| completed | 74 | 100.0 % |
| Total | 74 | 100.0 % |

| Statut CAB par requestId unique | Nombre | Part |
|---|---|---|
| APPROVED | 20 | 100.0 % |
| Total | 20 | 100.0 % |

Les décisions CAB et les appels natifs sont deux populations distinctes. completed désigne un outil natif réussi ou une lecture autorisée ; un code Bash non nul est une erreur technique. Un refus CAB non exécuté n'est pas ajouté aux commandes exécutées.

| Tokens natifs observés (catégories distinctes) | Nombre | Part |
|---|---|---|
| input | 512284 | 5.8 % |
| output | 54595 | 0.6 % |
| reasoning | 20945 | 0.2 % |
| cache_read | 8248182 | 93.3 % |
| cache_write | 0 | 0.0 % |
| Total | 8836006 | 100.0 % |

Coût de production natif connu : 0.082832764 (unité native non exposée). Entrées, sorties, raisonnement et caches sont additionnés selon leurs champs natifs, sans prétendre mesurer des tokens uniques.

Compactions natives : 1. Coût inclus dans la production : 0.007642200. Le résumé msg_0f1ae93a40012Bs1sgXb4W6Nvx était périmé sur tasks/delta : corrigé par message msg_0f1b5bb23001GplZrUrm5ZQ8Lf et acquitté msg_0f1b5eacf001gmoue1llog7oBL avant écriture. Aucun mandat consommé rejoué.

| Position | Envoi UTC | Échéance UTC | Retard s | Succès | Tokens sortie | TTMT s | Tokens/s | Premier texte UTC | Dernier texte UTC |
|---|---|---|---|---|---|---|---|---|---|
| début add-p0-contract-descriptors | 2026-09-30T09:10:35.276853+00:00 | 2026-09-30T09:10:34.647122+00:00 | 0.630 | oui | 458 | 3.488 | 142.931 | 2026-09-30T09:10:38.764482+00:00 | 2026-09-30T09:10:41.968836+00:00 |
| +30 min add-p0-contract-descriptors | 2026-09-30T09:47:16.729709+00:00 | 2026-09-30T09:40:35.276853+00:00 | 401.453 | oui | 475 | 6.439 | 272.086 | 2026-09-30T09:47:23.168573+00:00 | 2026-09-30T09:47:24.914345+00:00 |
| finale add-p0-contract-descriptors | 2026-09-30T10:14:56.429032+00:00 | 2026-09-30T10:14:56.392974+00:00 | 0.036 | oui | 458 | 2.571 | 330.998 | 2026-09-30T10:14:59.000515+00:00 | 2026-09-30T10:15:00.384208+00:00 |

| Configuration | Tentatives | Réussies | Échouées | TTMT min/max s | Débit min/max |
|---|---|---|---|---|---|
| HIGH | 3 | 3 | 0 | 2.571 / 6.439 | 142.931 / 330.998 |

La relève +30 min a été envoyée avec 401.453 s de retard, conservé explicitement ; aucune mesure rétroactive inventée. La sonde finale clôt l'intervalle. Les instants UTC proviennent de l'ancrage UTC et des écarts monotones effectivement observés sur les seuls événements texte assistant.

Surcharge séparée : 1391 tokens de sortie, coût 0.003931878, durée cumulée observée 19.079 s. Aucun de ces tokens/coûts n'est additionné à la production.

Prompt identique : 3068 caractères UTF-8, SHA256 0d1c4b356ce0fcc754af10151e68a9fbbdf6d5dc8dc688d02da5760439079875, conservé dans output/cismp-state.json. Texte déterministe de 64 lignes numérotées, sans tâche métier. Sessions jetables supprimées, permissions toutes refusées, zéro outil, modèle/fournisseur/HIGH confirmés nativement. Moyennes TTMT et débit arithmétiques sur sondes réussies uniquement.

Quotas avant/après : N/A. get_usage_limits n'est pas exposé parmi les outils disponibles lors des vérifications avant préparation et après archivage ; aucune lecture de secret ou substitution n'a été utilisée. Consommation de quota et solde : N/A ; les tokens natifs ci-dessus ne constituent pas une mesure de quota.

Validations réellement observées : 43 tests unitaires dédiés et 4 d'intégration dédiés ; régressions séparées 447 unitaires + 131 intégration = 578 tests, quatre commandes exit0. Les 47 dédiés sont inclus dans les 578 globaux : 625 exécutions cumulées, pas 625 tests distincts. AST Python3.11 quatre fichiers et exemple README, UTF-8/LF dix fichiers, delta canonique identique, strict préparation/final/dossier coché exit0 ; dix tâches cochées après preuves. Fondation déclarative partielle, sans preuve de P0 achevé ni de conformité comportementale globale.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 59 | 12.8 % |
| step-start | 87 | 18.9 % |
| reasoning | 152 | 33.0 % |
| tool | 74 | 16.1 % |
| step-finish | 87 | 18.9 % |
| compaction | 1 | 0.2 % |
| Total | 460 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
|---|---|---|
| tool-calls | 57 | 65.5 % |
| stop | 30 | 34.5 % |
| Total | 87 | 100.0 % |

| Outil | Appels | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| bash | 9 | 12.2 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 7 | 9.5 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 20 | 27.0 % | 20 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 1.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 27 | 36.5 % | 27 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 13.5 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 74 | 100.0 % | 74 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Chemin absolu | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-contract-descriptors/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-contract-descriptors/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-contract-descriptors/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-contract-descriptors/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-contract-descriptors/specs/contracts/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/contracts/models.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/contracts/__init__.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/contracts/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_contract_descriptors.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_contract_descriptors_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les tentatives d'édition sont comptées, pas les lignes. Cinq nouveaux fichiers d'implémentation : models.py, façade, README, test unitaire et test intégration. Cinq artefacts OpenSpec créés, tasks.md ensuite coché. L'unique commande d'archive a déplacé les cinq artefacts avec empreintes identiques ; ces écritures internes ne sont pas comptées comme cinq outils edit supplémentaires. Le présent rapport est hors intervalle.

## 4. Commandes

| Famille native | Nombre | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Contrôle sources | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Commande native (100 caractères max) | Nombre | Part | Résultat |
|---|---|---|---|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-contract-des… | 3 | 33.3 % | {'completed': 3} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 11.1 % | {'completed': 1} |
| /home/devops/python/current/bin/python3 -c 'import ast,hashlib,re ↵ from pathlib import Path ↵ p=Pa… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-contract-desc… | 1 | 11.1 % | {'completed': 1} |

Commandes exactes et preuves conservées dans output/cismp-state.json. Aucun regroupement shell ; chaque opération a son requestId unique et une permission distincte. Exécution seule du venv existant pour les régressions, aucune lecture/indexation du venv ni nouvelle installation.

## 5. Accès web

| Périmètre | Réussis | Refusés | Erreurs | Total | Part |
|---|---|---|---|---|---|
| Outils web natifs | 0 | 0 | 0 | 0 | N/A — dénominateur nul |

Aucun outil web ni commande d'installation ou d'accès réseau externe dans ce change. URLs visitées et noms de domaine externes : zéro dans les preuves natives. Les APIs loopback OpenCode/CAB sont du pilotage local, pas des visites web. L'accès normal au fournisseur LLM n'est pas une visite web ni un compteur réseau observé ; aucune requête HTTP globale n'est estimée.

## 6. Synthèse globale

| Domaine | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| Fichiers | 11 | 14.9 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 9 | 12.2 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 54 | 73.0 % | 54 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 74 | 100.0 % | 74 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les totaux par domaines et par outils concordent. Les décisions CAB, sondes, quotas N/A et écritures internes de l'archivage restent séparés des tentatives natives. Aucun secret, Git, PostgreSQL réel, nouvelle dépendance ou activation dans le périmètre observé. Les incidents de pilotage root et les propositions révisées avant écriture ne sont pas présentés comme des outils échoués de l'agent de codage.

Archivage vérifié, rapport produit séparément après l'intervalle ; retour à SÉLECTION du RUN parent avec CAB actif. Aucun état terminal ni fin de session annoncé à ce jalon.

