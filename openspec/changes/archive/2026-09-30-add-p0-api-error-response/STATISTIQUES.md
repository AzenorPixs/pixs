# STATISTIQUES — add-p0-api-error-response

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-api-error-response. RUN parent : cismp-pixs-20260929-2033. OpenCode 1.18.33, CAB 0.85.3.

Historique natif complet du change courant, borné au premier message spécifique et à la clôture après archivage ; la sonde finale est mesurée séparément. Les phases backend antérieures, la sélection parent et la rédaction de ce rapport sont exclues des comptes de production. Les sondes sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version télémétrique absente | opencode-go | HIGH | 4.730 s | 134.469 | N/A |
| muse-spark-1.3-contributor — compaction | N/A | opencode-go | N/A — variant absent | N/A | N/A | N/A |

Temps de génération active et dénominateur cumulé N/A : les durées natives incluent outils/attentes. La durée calendaire n'est pas un temps de service. Le nom 1.3 ne constitue pas une version télémétrique indépendante.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root — modèle exact N/A | N/A | N/A — télémétrie indisponible | N/A | N/A | N/A | N/A |

Aucune sonde orchestrateur. Toutes les décisions de ce change ont été publiées explicitement par /root après observation et comparaison du mandat réel. Aucun contexte de rappel n'a fourni une décision de ce change.

## 1. Statistiques générales et décisions

Le change a été traité dans une session maître HIGH conservée. Les premières propositions de tests contenaient du code de sous-processus syntaxiquement invalide, puis une assertion tautologique et un diagnostic Unicode incorrect : CGPT les a corrigés avant toute écriture ou exécution. Aucun échec de test ni refus CAB ne découle de ces propositions. Le premier rapport de métadonnée comportait un identifiant textuel erroné accompagné de l’identifiant réel ; le tuple MCP réel a été vérifié et le format corrigé au mandat suivant. Une compaction native a ensuite produit un résumé périmé suggérant de rejouer sourcecheck ; CGPT a transmis les preuves consommées, l’agent a confirmé dix tâches cochées et aucun rejeu, puis seul l’archivage non prouvé a été mandaté.

Intervalle calendaire : 2026-09-30T12:51:12.397000+00:00 → 2026-09-30T13:22:37.511270+00:00 ; durée 00 h 31 min 25 s, attentes incluses.

Session : ses_f0dc23887fferVi2IWwD6Imuoc ; premier message msg_0f25e778d001795UMOrk7bHoUB ; dernier message msg_0f279b7480014DpyAVpE3fuM5P ; 106 messages.

| Rôle des messages | Nombre | Part |
|---|---|---|
| user | 26 | 24.5 % |
| assistant | 80 | 75.5 % |
| Total | 106 | 100.0 % |

| Résultat des appels natifs | Nombre | Part |
|---|---|---|
| completed | 54 | 100.0 % |
| Total | 54 | 100.0 % |

| Statut CAB par requestId unique | Nombre | Part |
|---|---|---|
| APPROVED | 20 | 100.0 % |
| Total | 20 | 100.0 % |

Les décisions CAB et les appels natifs sont deux populations distinctes. completed désigne un outil natif réussi ou une lecture autorisée ; un code Bash non nul est une erreur technique. Un refus CAB non exécuté n'est pas ajouté aux commandes exécutées.

| Tokens natifs observés (catégories distinctes) | Nombre | Part |
|---|---|---|
| input | 331795 | 3.2 % |
| output | 27672 | 0.3 % |
| reasoning | 7300 | 0.1 % |
| cache_read | 10085727 | 96.5 % |
| cache_write | 0 | 0.0 % |
| Total | 10452494 | 100.0 % |

Coût de production natif connu : 0.060345354 (unité native non exposée). Entrées, sorties, raisonnement et caches sont additionnés selon leurs champs natifs, sans prétendre mesurer des tokens uniques.

Compactions natives dans cet intervalle : 1. Coût inclus dans la production : 0.010271200. Les compactions antérieures à la borne de début restent hors comptes. Variant du compactor non exposé : N/A, sans inférence de raisonnement.

| Position | Envoi UTC | Échéance UTC | Retard s | Succès | Tokens sortie | TTMT s | Tokens/s | Premier texte UTC | Dernier texte UTC |
|---|---|---|---|---|---|---|---|---|---|
| début add-p0-api-error-response | 2026-09-30T12:52:44.022732+00:00 | 2026-09-30T12:52:43.847631+00:00 | 0.175 | oui | 478 | 5.609 | 140.632 | 2026-09-30T12:52:49.631383+00:00 | 2026-09-30T12:52:53.030328+00:00 |
| fin add-p0-api-error-response | 2026-09-30T13:22:37.739609+00:00 | 2026-09-30T13:22:37.693945+00:00 | 0.046 | oui | 474 | 3.852 | 128.306 | 2026-09-30T13:22:41.591883+00:00 | 2026-09-30T13:22:45.286186+00:00 |

| Configuration | Tentatives | Réussies | Échouées | TTMT min/max s | Débit min/max |
|---|---|---|---|---|---|
| HIGH | 2 | 2 | 0 | 3.852 / 5.609 | 128.306 / 140.632 |

Les retards effectifs des relèves sont conservés dans le tableau sans mesure rétroactive. La sonde finale clôt l'intervalle. Les instants UTC proviennent de l'ancrage UTC et des écarts monotones observés sur les seuls événements texte assistant.

Surcharge séparée : 952 tokens de sortie, coût 0.000355356, durée cumulée observée 16.632 s. Aucun de ces tokens/coûts n'est additionné à la production.

Prompt identique : 3068 caractères UTF-8, SHA256 0d1c4b356ce0fcc754af10151e68a9fbbdf6d5dc8dc688d02da5760439079875, conservé dans output/cismp-state.json. Texte déterministe de 64 lignes numérotées, sans tâche métier. Sessions jetables supprimées, permissions toutes refusées, zéro outil, modèle/fournisseur/HIGH confirmés nativement. Moyennes TTMT et débit arithmétiques sur sondes réussies uniquement.

Quotas avant/après : N/A. get_usage_limits n'est pas exposé parmi les outils disponibles lors des vérifications avant préparation et après archivage ; aucune lecture de secret ou substitution n'a été utilisée. Consommation de quota et solde : N/A ; les tokens natifs ci-dessus ne constituent pas une mesure de quota.

Validations réellement observées : 5 tests unitaires dédiés et 3 d'intégration dédiés ; régressions séparées 520 unitaires + 147 intégration = 667 tests, quatre commandes exit0. Les 8 dédiés sont inclus dans les 667 globaux : 675 exécutions cumulées. AST Python3.11 quatre fichiers et huit programmes de sous-processus, trois exemples README, UTF-8/LF dix fichiers, delta canonique requirement2API identique, strict préparation/final/dossier coché exit0 ; dix tâches cochées après preuves. Fabrique JsonResponse HTTP500 réelle et isolée, corps égal à la projection publique existante, import Django paresseux et garde explicite sur réglages déjà configurés ; aucune route ni serveur, classification métier, pagination, rejeu persistant ou conformité globale de requirement2/P0 attestée. Les cinq gardes de connexion sont restées à zéro et le processus parent n’est pas configuré.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 51 | 13.7 % |
| step-start | 80 | 21.4 % |
| reasoning | 107 | 28.7 % |
| step-finish | 80 | 21.4 % |
| tool | 54 | 14.5 % |
| compaction | 1 | 0.3 % |
| Total | 373 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
|---|---|---|
| stop | 26 | 32.5 % |
| tool-calls | 54 | 67.5 % |
| Total | 80 | 100.0 % |

| Outil | Appels | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| bash | 9 | 16.7 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 5 | 9.3 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 20 | 37.0 % | 20 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 9 | 16.7 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 10 | 18.5 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 54 | 100.0 % | 54 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

## 3. Fichiers modifiés

Les cinq fichiers ont été relus intégralement après leur opération native unique. La façade et le README conservent intégralement leurs préfixes de 593 et 4504 caractères. Les corrections de propositions ont précédé toute écriture : aucun mandat de correction de source ou de document n’a été exécuté dans cet intervalle.

| Chemin absolu | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-response/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-response/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-response/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-response/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-error-response/specs/api/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/responses.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/__init__.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_api_error_response.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_api_error_response_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les tentatives d'édition sont comptées, pas les lignes. Trois nouveaux fichiers d'implémentation : responses.py, test unitaire et test intégration. Deux fichiers existants ont reçu un ajout minimal : façade et README, avec préfixes préexistants préservés. Cinq artefacts OpenSpec créés, tasks.md ensuite coché. L'unique commande d'archive a déplacé les cinq artefacts avec empreintes identiques ; ces écritures internes ne sont pas comptées comme cinq outils edit supplémentaires. Le présent rapport est hors intervalle.

## 4. Commandes

| Famille native | Nombre | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests | 4 | 44.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Contrôle sources | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Commande native (100 caractères max) | Nombre | Part | Résultat |
|---|---|---|---|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-api-error-re… | 3 | 33.3 % | {'completed': 3} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 11.1 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-api-error-res… | 1 | 11.1 % | {'completed': 1} |

Commandes exactes et preuves conservées dans output/cismp-state.json. Aucun regroupement shell ; chaque opération a son requestId unique et une permission distincte. Exécution seule du venv existant pour les régressions, aucune lecture/indexation du venv ni nouvelle installation.

## 5. Accès web

| Périmètre | Réussis | Refusés | Erreurs | Total | Part |
|---|---|---|---|---|---|
| Outils web natifs | 0 | 0 | 0 | 0 | N/A — dénominateur nul |

Aucun outil web ni commande d'installation ou d'accès réseau externe dans ce change. URLs visitées et noms de domaine externes : zéro dans les preuves natives. Les APIs loopback OpenCode/CAB sont du pilotage local, pas des visites web. L'accès normal au fournisseur LLM n'est pas une visite web ni un compteur réseau observé ; aucune requête HTTP globale n'est estimée.

## 6. Synthèse globale

| Domaine | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| Fichiers | 11 | 20.4 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 9 | 16.7 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 34 | 63.0 % | 34 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 54 | 100.0 % | 54 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les totaux par domaines et par outils concordent. Les décisions CAB, sondes, quotas N/A et écritures internes de l'archivage restent séparés des tentatives natives. Aucun secret, Git, PostgreSQL réel, nouvelle dépendance ou activation dans le périmètre observé. Les incidents de pilotage root et les propositions révisées avant écriture ne sont pas présentés comme des outils échoués de l'agent de codage.

Archivage vérifié, rapport produit séparément après l'intervalle ; retour à SÉLECTION du RUN parent avec CAB actif. Aucun état terminal ni fin de session annoncé à ce jalon.
