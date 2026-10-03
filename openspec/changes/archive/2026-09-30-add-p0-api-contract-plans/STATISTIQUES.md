# STATISTIQUES — add-p0-api-contract-plans

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-api-contract-plans. RUN parent : cismp-pixs-20260929-2033. OpenCode 1.18.33, CAB 0.85.3.

Historique natif complet du change courant, borné au premier message spécifique et à la clôture après archivage ; la sonde finale est mesurée séparément. Les phases backend antérieures, la sélection parent et la rédaction de ce rapport sont exclues des comptes de production. Les sondes sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version télémétrique absente | opencode-go | HIGH | 5.073 s | 239.143 | N/A |

Temps de génération active et dénominateur cumulé N/A : les durées natives incluent outils/attentes. La durée calendaire n'est pas un temps de service. Le nom 1.3 ne constitue pas une version télémétrique indépendante.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root — modèle exact N/A | N/A | N/A — télémétrie indisponible | N/A | N/A | N/A | N/A |

Aucune sonde orchestrateur. Toutes les décisions de ce change ont été publiées explicitement par /root après observation et comparaison du mandat réel. Aucun contexte de rappel n'a fourni une décision de ce change.

## 1. Statistiques générales et décisions

Intervalle calendaire : 2026-09-30T10:34:53.275567+00:00 → 2026-09-30T11:25:55.312725+00:00 ; durée 00 h 51 min 02 s, attentes incluses.

Session : ses_f0ecd09c8ffeTzzapPYlvxAdPE ; premier message msg_0f1e2ac3a0017LoGDpMw6ELHUc ; dernier message msg_0f20fdffd001JSpG1cCp2TErmr ; 107 messages.

| Rôle des messages | Nombre | Part |
|---|---|---|
| user | 29 | 27.1 % |
| assistant | 78 | 72.9 % |
| Total | 107 | 100.0 % |

| Résultat des appels natifs | Nombre | Part |
|---|---|---|
| completed | 59 | 100.0 % |
| Total | 59 | 100.0 % |

| Statut CAB par requestId unique | Nombre | Part |
|---|---|---|
| APPROVED | 21 | 100.0 % |
| Total | 21 | 100.0 % |

Les décisions CAB et les appels natifs sont deux populations distinctes. completed désigne un outil natif réussi ou une lecture autorisée ; un code Bash non nul est une erreur technique. Un refus CAB non exécuté n'est pas ajouté aux commandes exécutées.

| Tokens natifs observés (catégories distinctes) | Nombre | Part |
|---|---|---|
| input | 368434 | 4.8 % |
| output | 40572 | 0.5 % |
| reasoning | 26860 | 0.3 % |
| cache_read | 7240558 | 94.3 % |
| cache_write | 0 | 0.0 % |
| Total | 7676424 | 100.0 % |

Coût de production natif connu : 0.064810916 (unité native non exposée). Entrées, sorties, raisonnement et caches sont additionnés selon leurs champs natifs, sans prétendre mesurer des tokens uniques.

Compactions natives dans cet intervalle : 0. Coût inclus dans la production : 0.000000000. Les compactions antérieures à la borne de début restent hors comptes. Variant du compactor non exposé : N/A, sans inférence de raisonnement.

| Position | Envoi UTC | Échéance UTC | Retard s | Succès | Tokens sortie | TTMT s | Tokens/s | Premier texte UTC | Dernier texte UTC |
|---|---|---|---|---|---|---|---|---|---|
| début add-p0-api-contract-plans | 2026-09-30T10:34:53.522211+00:00 | 2026-09-30T10:34:53.275567+00:00 | 0.247 | oui | 485 | 6.401 | 63.856 | 2026-09-30T10:34:59.923218+00:00 | 2026-09-30T10:35:07.518469+00:00 |
| +30 min add-p0-api-contract-plans | 2026-09-30T11:05:05.384646+00:00 | 2026-09-30T11:04:53.522211+00:00 | 11.862 | oui | 474 | 4.598 | 292.814 | 2026-09-30T11:05:09.982573+00:00 | 2026-09-30T11:05:11.601350+00:00 |
| fin add-p0-api-contract-plans | 2026-09-30T11:25:55.505909+00:00 | 2026-09-30T11:25:55.468784+00:00 | 0.037 | oui | 458 | 4.221 | 360.759 | 2026-09-30T11:25:59.726903+00:00 | 2026-09-30T11:26:00.996449+00:00 |

| Configuration | Tentatives | Réussies | Échouées | TTMT min/max s | Débit min/max |
|---|---|---|---|---|---|
| HIGH | 3 | 3 | 0 | 4.221 / 6.401 | 63.856 / 360.759 |

Les retards effectifs des relèves sont conservés dans le tableau sans mesure rétroactive. La sonde finale clôt l'intervalle. Les instants UTC proviennent de l'ancrage UTC et des écarts monotones observés sur les seuls événements texte assistant.

Surcharge séparée : 1417 tokens de sortie, coût 0.004020878, durée cumulée observée 25.958 s. Aucun de ces tokens/coûts n'est additionné à la production.

Prompt identique : 3068 caractères UTF-8, SHA256 0d1c4b356ce0fcc754af10151e68a9fbbdf6d5dc8dc688d02da5760439079875, conservé dans output/cismp-state.json. Texte déterministe de 64 lignes numérotées, sans tâche métier. Sessions jetables supprimées, permissions toutes refusées, zéro outil, modèle/fournisseur/HIGH confirmés nativement. Moyennes TTMT et débit arithmétiques sur sondes réussies uniquement.

Quotas avant/après : N/A. get_usage_limits n'est pas exposé parmi les outils disponibles lors des vérifications avant préparation et après archivage ; aucune lecture de secret ou substitution n'a été utilisée. Consommation de quota et solde : N/A ; les tokens natifs ci-dessus ne constituent pas une mesure de quota.

Validations réellement observées : 56 tests unitaires dédiés et 9 d'intégration dédiés ; régressions séparées 503 unitaires + 140 intégration = 643 tests, quatre commandes exit0. Les 65 dédiés sont inclus dans les 643 globaux : 708 exécutions cumulées. AST Python3.11 quatre fichiers et exemple README, UTF-8/LF dix fichiers, delta canonique requirement1API identique, strict préparation/final/dossier coché exit0 ; dix tâches cochées après preuves. Plans de métadonnées seulement : aucune publication, coexistence effective, validation complète OpenAPI ou P0 achevé attesté.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 58 | 14.6 % |
| step-start | 78 | 19.6 % |
| reasoning | 124 | 31.2 % |
| tool | 59 | 14.9 % |
| step-finish | 78 | 19.6 % |
| Total | 397 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
|---|---|---|
| tool-calls | 49 | 62.8 % |
| stop | 29 | 37.2 % |
| Total | 78 | 100.0 % |

| Outil | Appels | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| bash | 10 | 16.9 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 4 | 6.8 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 21 | 35.6 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 1.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 2 | 3.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 11 | 18.6 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 16.9 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 59 | 100.0 % | 59 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

## 3. Fichiers modifiés

La correction préventive de neuf levées ApiContractPlanError a été réalisée sous mandat unitaire par une commande Python. Elle est comptée parmi les commandes Bash, sans ajouter une édition native aux comptes fichiers ; le fichier source concerné reste contracts.py. Aucun test n’avait échoué avant cette correction.

| Chemin absolu | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-api-contract-plans/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-contract-plans/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-contract-plans/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-contract-plans/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-contract-plans/specs/api/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/contracts.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/__init__.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_api_contract_plans.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_api_contract_plans_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les tentatives d'édition sont comptées, pas les lignes. Cinq nouveaux fichiers d'implémentation : contracts.py, façade, README, test unitaire et test intégration. Cinq artefacts OpenSpec créés, tasks.md ensuite coché. L'unique commande d'archive a déplacé les cinq artefacts avec empreintes identiques ; ces écritures internes ne sont pas comptées comme cinq outils edit supplémentaires. Le présent rapport est hors intervalle.

## 4. Commandes

| Famille native | Nombre | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 40.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Correction source | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests | 4 | 40.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Contrôle sources | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Commande native (100 caractères max) | Nombre | Part | Résultat |
|---|---|---|---|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-api-contract… | 3 | 30.0 % | {'completed': 3} |
| /home/devops/python/current/bin/python3 -c 'from pathlib import Path ↵ import hashlib,ast ↵ p=Path(… | 1 | 10.0 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 10.0 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 10.0 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 10.0 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 10.0 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -c 'i… | 1 | 10.0 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-api-contract-… | 1 | 10.0 % | {'completed': 1} |

Commandes exactes et preuves conservées dans output/cismp-state.json. Aucun regroupement shell ; chaque opération a son requestId unique et une permission distincte. Exécution seule du venv existant pour les régressions, aucune lecture/indexation du venv ni nouvelle installation.

## 5. Accès web

| Périmètre | Réussis | Refusés | Erreurs | Total | Part |
|---|---|---|---|---|---|
| Outils web natifs | 0 | 0 | 0 | 0 | N/A — dénominateur nul |

Aucun outil web ni commande d'installation ou d'accès réseau externe dans ce change. URLs visitées et noms de domaine externes : zéro dans les preuves natives. Les APIs loopback OpenCode/CAB sont du pilotage local, pas des visites web. L'accès normal au fournisseur LLM n'est pas une visite web ni un compteur réseau observé ; aucune requête HTTP globale n'est estimée.

## 6. Synthèse globale

| Domaine | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| Fichiers | 11 | 18.6 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 10 | 16.9 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 38 | 64.4 % | 38 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 59 | 100.0 % | 59 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les totaux par domaines et par outils concordent. Les décisions CAB, sondes, quotas N/A et écritures internes de l'archivage restent séparés des tentatives natives. Aucun secret, Git, PostgreSQL réel, nouvelle dépendance ou activation dans le périmètre observé. Les incidents de pilotage root et les propositions révisées avant écriture ne sont pas présentés comme des outils échoués de l'agent de codage.

Archivage vérifié, rapport produit séparément après l'intervalle ; retour à SÉLECTION du RUN parent avec CAB actif. Aucun état terminal ni fin de session annoncé à ce jalon.

