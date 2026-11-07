# STATISTIQUES — add-p0-api-error-projection

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-api-error-projection. RUN parent : cismp-pixs-20260929-2033. OpenCode 1.18.33, CAB 0.85.3.

Historique natif complet du change courant, borné au premier message spécifique et à la clôture après archivage ; la sonde finale est mesurée séparément. Les phases backend antérieures, la sélection parent et la rédaction de ce rapport sont exclues des comptes de production. Les sondes sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version télémétrique absente | opencode-go | HIGH | 3.226 s | 308.810 | N/A |

Temps de génération active et dénominateur cumulé N/A : les durées natives incluent outils/attentes. La durée calendaire n'est pas un temps de service. Le nom 1.3 ne constitue pas une version télémétrique indépendante.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root — modèle exact N/A | N/A | N/A — télémétrie indisponible | N/A | N/A | N/A | N/A |

Aucune sonde orchestrateur. Toutes les décisions de ce change ont été publiées explicitement par /root après observation et comparaison du mandat réel. Aucun contexte de rappel n'a fourni une décision de ce change.

## 1. Statistiques générales et décisions

La première session a été interrompue après transcription divergente de readme-fix01 : CGPT a refusé cette commande avant toute exécution. Le timeout MCP initial et le polling interrompu restent dans les comptes natifs. Le refus réel a été récupéré, puis broker_health et readiness ont prouvé zéro attente ; un contrat CAB technique neuf et une nouvelle session HIGH ont repris le seul jalon non prouvé. Aucun mandat consommé ni archivage n’a été rejoué.

Intervalle calendaire : 2026-09-30T11:37:51.588634+00:00 → 2026-09-30T12:45:07.320357+00:00 ; durée 01 h 07 min 15 s, attentes incluses.

Session : ses_f0ecd09c8ffeTzzapPYlvxAdPE ; premier message msg_0f21c3d92001hj4KWoo8KgFdAC ; dernier message msg_0f23b3893001QRCs31ENpoxjv6 ; 64 messages.
Session : ses_f0dc23887fferVi2IWwD6Imuoc ; premier message msg_0f23dc7fd0015bRqXz80DCgMdh ; dernier message msg_0f2580f44001MKxawbnrk28Nuz ; 92 messages.

| Rôle des messages | Nombre | Part |
|---|---|---|
| user | 34 | 21.8 % |
| assistant | 122 | 78.2 % |
| Total | 156 | 100.0 % |

| Résultat des appels natifs | Nombre | Part |
|---|---|---|
| completed | 91 | 96.8 % |
| error | 3 | 3.2 % |
| Total | 94 | 100.0 % |

| Statut CAB par requestId unique | Nombre | Part |
|---|---|---|
| APPROVED | 23 | 95.8 % |
| REJECTED | 1 | 4.2 % |
| Total | 24 | 100.0 % |

Les décisions CAB et les appels natifs sont deux populations distinctes. completed désigne un outil natif réussi ou une lecture autorisée ; un code Bash non nul est une erreur technique. Un refus CAB non exécuté n'est pas ajouté aux commandes exécutées.

| Tokens natifs observés (catégories distinctes) | Nombre | Part |
|---|---|---|
| input | 555843 | 7.4 % |
| output | 35747 | 0.5 % |
| reasoning | 23907 | 0.3 % |
| cache_read | 6895337 | 91.8 % |
| cache_write | 0 | 0.0 % |
| Total | 7510834 | 100.0 % |

Coût de production natif connu : 0.081305774 (unité native non exposée). Entrées, sorties, raisonnement et caches sont additionnés selon leurs champs natifs, sans prétendre mesurer des tokens uniques.

Compactions natives dans cet intervalle : 0. Coût inclus dans la production : 0.000000000. Les compactions antérieures à la borne de début restent hors comptes. Variant du compactor non exposé : N/A, sans inférence de raisonnement.

| Position | Envoi UTC | Échéance UTC | Retard s | Succès | Tokens sortie | TTMT s | Tokens/s | Premier texte UTC | Dernier texte UTC |
|---|---|---|---|---|---|---|---|---|---|
| début add-p0-api-error-projection | 2026-09-30T11:37:51.841831+00:00 | 2026-09-30T11:37:51.588634+00:00 | 0.253 | oui | 458 | 2.041 | 444.891 | 2026-09-30T11:37:53.882585+00:00 | 2026-09-30T11:37:54.912050+00:00 |
| +30 min add-p0-api-error-projection | 2026-09-30T12:07:51.897816+00:00 | 2026-09-30T12:07:51.841831+00:00 | 0.056 | oui | 458 | 3.145 | 268.004 | 2026-09-30T12:07:55.042378+00:00 | 2026-09-30T12:07:56.751309+00:00 |
| +60 min add-p0-api-error-projection | 2026-09-30T12:43:28.777594+00:00 | 2026-09-30T12:37:51.897816+00:00 | 336.880 | oui | 458 | 4.077 | 217.785 | 2026-09-30T12:43:32.854876+00:00 | 2026-09-30T12:43:34.957864+00:00 |
| fin add-p0-api-error-projection | 2026-09-30T12:45:07.571734+00:00 | 2026-09-30T12:45:07.544760+00:00 | 0.027 | oui | 458 | 3.642 | 304.559 | 2026-09-30T12:45:11.214009+00:00 | 2026-09-30T12:45:12.717821+00:00 |

| Configuration | Tentatives | Réussies | Échouées | TTMT min/max s | Débit min/max |
|---|---|---|---|---|---|
| HIGH | 4 | 4 | 0 | 2.041 / 4.077 | 217.785 / 444.891 |

Les retards effectifs des relèves sont conservés dans le tableau sans mesure rétroactive. La sonde finale clôt l'intervalle. Les instants UTC proviennent de l'ancrage UTC et des écarts monotones observés sur les seuls événements texte assistant.

Surcharge séparée : 1832 tokens de sortie, coût 0.004041456, durée cumulée observée 19.575 s. Aucun de ces tokens/coûts n'est additionné à la production.

Prompt identique : 3068 caractères UTF-8, SHA256 0d1c4b356ce0fcc754af10151e68a9fbbdf6d5dc8dc688d02da5760439079875, conservé dans output/cismp-state.json. Texte déterministe de 64 lignes numérotées, sans tâche métier. Sessions jetables supprimées, permissions toutes refusées, zéro outil, modèle/fournisseur/HIGH confirmés nativement. Moyennes TTMT et débit arithmétiques sur sondes réussies uniquement.

Quotas avant/après : N/A. get_usage_limits n'est pas exposé parmi les outils disponibles lors des vérifications avant préparation et après archivage ; aucune lecture de secret ou substitution n'a été utilisée. Consommation de quota et solde : N/A ; les tokens natifs ci-dessus ne constituent pas une mesure de quota.

Validations réellement observées : 12 tests unitaires dédiés et 4 d'intégration dédiés ; régressions séparées 515 unitaires + 144 intégration = 659 tests, quatre commandes exit0. Les 16 dédiés sont inclus dans les 659 globaux : 675 exécutions cumulées. AST Python3.11 quatre fichiers et deux exemples README, UTF-8/LF dix fichiers, delta canonique requirement2API identique, strict préparation/final/dossier coché exit0 ; dix tâches cochées après preuves. Projection publique constante seule : aucune intégration HTTP, classification réelle d'infrastructure, pagination, rejeu persistant ni conformité globale de requirement2 ou P0 attestée.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 67 | 11.7 % |
| step-start | 122 | 21.2 % |
| reasoning | 171 | 29.7 % |
| tool | 94 | 16.3 % |
| step-finish | 121 | 21.0 % |
| Total | 575 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
|---|---|---|
| tool-calls | 88 | 72.1 % |
| stop | 33 | 27.0 % |
| in_progress | 1 | 0.8 % |
| Total | 122 | 100.0 % |

| Outil | Appels | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| bash | 12 | 12.8 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_health | 1 | 1.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 10 | 10.6 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 1.1 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 2 | 2.1 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 24 | 25.5 % | 23 | 95.8 % | 0 | 0.0 % | 1 | 4.2 % | 0 | 0.0 % |
| edit | 1 | 1.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 1.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 32 | 34.0 % | 32 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 10.6 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 94 | 100.0 % | 91 | 96.8 % | 0 | 0.0 % | 3 | 3.2 % | 0 | 0.0 % |

## 3. Fichiers modifiés

Un écart documentaire a été détecté après readme01 : deux noms de suites du préfixe antérieur avaient été remplacés. La sélection des tests a été suspendue avant tout test, CAB a été revalidé avec /usr/bin/true puis un mandat frais a restauré ces deux noms par commande Python. Le contrôle intégral final prouve les préfixes et le contenu attendus. Cette correction figure dans les commandes Bash, sans outil edit supplémentaire ; le succès technique de write ne prouve pas à lui seul la fidélité du contenu.

| Chemin absolu | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-projection/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-projection/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-projection/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-projection/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-projection/specs/api/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/errors.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/__init__.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_api_error_projection.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_api_error_projection_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les tentatives d'édition sont comptées, pas les lignes. Trois nouveaux fichiers d'implémentation : errors.py, test unitaire et test intégration. Deux fichiers existants ont reçu un ajout minimal : façade et README, avec préfixes préexistants préservés. Cinq artefacts OpenSpec créés, tasks.md ensuite coché. L'unique commande d'archive a déplacé les cinq artefacts avec empreintes identiques ; ces écritures internes ne sont pas comptées comme cinq outils edit supplémentaires. Le présent rapport est hors intervalle.

## 4. Commandes

| Famille native | Nombre | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 33.3 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Récupération CAB | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Correction documentaire | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests | 4 | 33.3 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Contrôle sources | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Commande native (100 caractères max) | Nombre | Part | Résultat |
|---|---|---|---|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-api-error-pr… | 3 | 25.0 % | {'completed': 3} |
| /usr/bin/true | 2 | 16.7 % | {'completed': 2} |
| /home/devops/python/current/bin/python3 -c 'from pathlib import Path ↵ import hashlib ↵ p=Path("src… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -c 'i… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-api-error-pro… | 1 | 8.3 % | {'completed': 1} |

Commandes exactes et preuves conservées dans output/cismp-state.json. Aucun regroupement shell ; chaque opération a son requestId unique et une permission distincte. Exécution seule du venv existant pour les régressions, aucune lecture/indexation du venv ni nouvelle installation.

## 5. Accès web

| Périmètre | Réussis | Refusés | Erreurs | Total | Part |
|---|---|---|---|---|---|
| Outils web natifs | 0 | 0 | 0 | 0 | N/A — dénominateur nul |

Aucun outil web ni commande d'installation ou d'accès réseau externe dans ce change. URLs visitées et noms de domaine externes : zéro dans les preuves natives. Les APIs loopback OpenCode/CAB sont du pilotage local, pas des visites web. L'accès normal au fournisseur LLM n'est pas une visite web ni un compteur réseau observé ; aucune requête HTTP globale n'est estimée.

## 6. Synthèse globale

| Domaine | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| Fichiers | 11 | 11.7 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 12 | 12.8 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 71 | 75.5 % | 68 | 95.8 % | 0 | 0.0 % | 3 | 4.2 % | 0 | 0.0 % |
| Total | 94 | 100.0 % | 91 | 96.8 % | 0 | 0.0 % | 3 | 3.2 % | 0 | 0.0 % |

Les totaux par domaines et par outils concordent. Les décisions CAB, sondes, quotas N/A et écritures internes de l'archivage restent séparés des tentatives natives. Aucun secret, Git, PostgreSQL réel, nouvelle dépendance ou activation dans le périmètre observé. Les incidents de pilotage root et les propositions révisées avant écriture ne sont pas présentés comme des outils échoués de l'agent de codage.

Archivage vérifié, rapport produit séparément après l'intervalle ; retour à SÉLECTION du RUN parent avec CAB actif. Aucun état terminal ni fin de session annoncé à ce jalon.
