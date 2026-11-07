# STATISTIQUES — add-p0-api-success-response

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-api-success-response. RUN parent : cismp-pixs-20260929-2033. OpenCode 1.18.33, CAB 0.85.3.

Historique natif complet du change courant, borné au premier message spécifique et à la clôture après archivage ; la sonde finale est mesurée séparément. Les phases backend antérieures, la sélection parent et la rédaction de ce rapport sont exclues des comptes de production. Les sondes sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version télémétrique absente | opencode-go | HIGH | 4.062 s | 244.273 | N/A |

Temps de génération active et dénominateur cumulé N/A : les durées natives incluent outils/attentes. La durée calendaire n'est pas un temps de service. Le nom 1.3 ne constitue pas une version télémétrique indépendante.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root — modèle exact N/A | N/A | N/A — télémétrie indisponible | N/A | N/A | N/A | N/A |

Aucune sonde orchestrateur. Toutes les décisions de ce change ont été publiées explicitement par /root après observation et comparaison du mandat réel. Aucun contexte de rappel n'a fourni une décision de ce change.

## 1. Statistiques générales et décisions

Le change a été traité dans la session maître HIGH conservée. CGPT a corrigé les premières propositions de tests avant écriture (boucle de clés, tuple de signature, clé hostile construite avant activation et datetime déterministe). Le premier passage de la suite d’intégration a réellement échoué sur une assertion négative Unicode doublement interprétée : exit1, quatre tests dont trois réussis et un échec. Les régressions ont été suspendues. Un CAB test inédit /usr/bin/true a prouvé READY0 initial et final ; un mandat Python frais a remplacé une seule ligne du test par une comparaison d’octets ASCII explicite. Le contenu intégral corrigé a été vérifié, puis testintegration02 a réussi quatre tests. Le code de production et OpenSpec n’ont pas été corrigés. L’échec initial reste dans les comptes natifs et n’est jamais converti en succès.

Intervalle calendaire : 2026-09-30T13:30:35.945000+00:00 → 2026-09-30T14:14:05.917032+00:00 ; durée 00 h 43 min 29 s, attentes incluses.

Session : ses_f0dc23887fferVi2IWwD6Imuoc ; premier message msg_0f2828829001oQbuaoZDwPfHa4 ; dernier message msg_0f2a89ee3001lILp06OTjX1ThO ; 115 messages.

| Rôle des messages | Nombre | Part |
|---|---|---|
| user | 28 | 24.3 % |
| assistant | 87 | 75.7 % |
| Total | 115 | 100.0 % |

| Résultat des appels natifs | Nombre | Part |
|---|---|---|
| completed | 62 | 98.4 % |
| error | 1 | 1.6 % |
| Total | 63 | 100.0 % |

| Statut CAB par requestId unique | Nombre | Part |
|---|---|---|
| APPROVED | 23 | 100.0 % |
| Total | 23 | 100.0 % |

Les décisions CAB et les appels natifs sont deux populations distinctes. completed désigne un outil natif réussi ou une lecture autorisée ; un code Bash non nul est une erreur technique. Un refus CAB non exécuté n'est pas ajouté aux commandes exécutées.

| Tokens natifs observés (catégories distinctes) | Nombre | Part |
|---|---|---|
| input | 273823 | 3.3 % |
| output | 32367 | 0.4 % |
| reasoning | 2443 | 0.0 % |
| cache_read | 7979111 | 96.3 % |
| cache_write | 0 | 0.0 % |
| Total | 8287744 | 100.0 % |

Coût de production natif connu : 0.050302522 (unité native non exposée). Entrées, sorties, raisonnement et caches sont additionnés selon leurs champs natifs, sans prétendre mesurer des tokens uniques.

Compactions natives dans cet intervalle : 0. Coût inclus dans la production : 0.000000000. Les compactions antérieures à la borne de début restent hors comptes. Variant du compactor non exposé : N/A, sans inférence de raisonnement.

| Position | Envoi UTC | Échéance UTC | Retard s | Succès | Tokens sortie | TTMT s | Tokens/s | Premier texte UTC | Dernier texte UTC |
|---|---|---|---|---|---|---|---|---|---|
| début add-p0-api-success-response | 2026-09-30T13:33:23.315287+00:00 | 2026-09-30T13:33:23.112167+00:00 | 0.203 | oui | 458 | 6.088 | 217.022 | 2026-09-30T13:33:29.403586+00:00 | 2026-09-30T13:33:31.513967+00:00 |
| +30 min add-p0-api-success-response | 2026-09-30T14:03:58.727724+00:00 | 2026-09-30T14:03:23.315287+00:00 | 35.412 | oui | 458 | 2.460 | 304.890 | 2026-09-30T14:04:01.187315+00:00 | 2026-09-30T14:04:02.689494+00:00 |
| fin add-p0-api-success-response | 2026-09-30T14:14:06.121608+00:00 | 2026-09-30T14:14:06.084774+00:00 | 0.037 | oui | 458 | 3.637 | 210.908 | 2026-09-30T14:14:09.758429+00:00 | 2026-09-30T14:14:11.929997+00:00 |

| Configuration | Tentatives | Réussies | Échouées | TTMT min/max s | Débit min/max |
|---|---|---|---|---|---|
| HIGH | 3 | 3 | 0 | 2.460 / 6.088 | 210.908 / 304.890 |

Les retards effectifs des relèves sont conservés dans le tableau sans mesure rétroactive. La sonde finale clôt l'intervalle. Les instants UTC proviennent de l'ancrage UTC et des écarts monotones observés sur les seuls événements texte assistant.

Surcharge séparée : 1374 tokens de sortie, coût 0.002758430, durée cumulée observée 18.261 s. Aucun de ces tokens/coûts n'est additionné à la production.

Prompt identique : 3068 caractères UTF-8, SHA256 0d1c4b356ce0fcc754af10151e68a9fbbdf6d5dc8dc688d02da5760439079875, conservé dans output/cismp-state.json. Texte déterministe de 64 lignes numérotées, sans tâche métier. Sessions jetables supprimées, permissions toutes refusées, zéro outil, modèle/fournisseur/HIGH confirmés nativement. Moyennes TTMT et débit arithmétiques sur sondes réussies uniquement.

Quotas avant/après : N/A. get_usage_limits n'est pas exposé parmi les outils disponibles lors des vérifications avant préparation et après archivage ; aucune lecture de secret ou substitution n'a été utilisée. Consommation de quota et solde : N/A ; les tokens natifs ci-dessus ne constituent pas une mesure de quota.

Validations réellement observées : 13 tests unitaires dédiés et 4 d'intégration dédiés ; régressions séparées 533 unitaires + 151 intégration = 684 tests, quatre commandes exit0. Les 17 dédiés sont inclus dans les 684 globaux : 701 exécutions dans les quatre commandes réussies ; le passage initial échoué ajoute quatre exécutions, soit 705 exécutions de tests au total, 704 réussies et une échouée, sans augmenter les 684 tests uniques globaux. AST Python3.11 quatre fichiers et dix-sept programmes de sous-processus, six exemples README, UTF-8/LF dix fichiers, delta canonique requirement2API identique, strict préparation/final/dossier coché exit0 ; dix tâches cochées après preuves. Constructeur public data/meta/links avec validation JSON fini, types exacts et copie profonde ; JsonResponse HTTP200 réel et isolé, Unicode UTF-8 et grand entier conservés, import Django paresseux et garde explicite sur réglages déjà configurés. Les cinq gardes de connexion sont restées à zéro et le parent n’est pas configuré. Aucune route ni serveur, validation métier, pagination, rejeu persistant ou conformité globale requirement2/P0 attestée ; le module appelant choisit les données publiques non sensibles.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 56 | 13.8 % |
| step-start | 87 | 21.4 % |
| reasoning | 114 | 28.0 % |
| step-finish | 87 | 21.4 % |
| tool | 63 | 15.5 % |
| Total | 407 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
|---|---|---|
| stop | 28 | 32.2 % |
| tool-calls | 59 | 67.8 % |
| Total | 87 | 100.0 % |

| Outil | Appels | Part | Réussis | Taux | Refusés | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| bash | 12 | 19.0 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 6 | 9.5 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 23 | 36.5 % | 23 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 2 | 3.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 11 | 17.5 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 9 | 14.3 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 63 | 100.0 % | 62 | 98.4 % | 0 | 0.0 % | 1 | 1.6 % | 0 | 0.0 % |

## 3. Fichiers modifiés

Les cinq fichiers ont été relus intégralement après leur opération native unique. La façade et le README conservent leurs préfixes de 693 et 6998 caractères. Le seul fichier d’intégration a ensuite reçu une correction d’une ligne par commande Python, hash initial 54c896cdf816756bc6a0d6b19b8a247625f6ae56f5c1b3426fb8332c43eac8b6, hash corrigé 9d9ba9a211ddeb8b35ba4ab43310be77396d7c113a9786ca43849e27229fafff. Cette écriture figure dans les commandes, sans inventer un outil edit supplémentaire.

| Chemin absolu | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-api-success-response/.openspec.yaml | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-success-response/proposal.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-success-response/design.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-success-response/tasks.md | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-success-response/specs/api/spec.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/success.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/__init__.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_api_success_envelope.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_api_success_response_integration.py | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les tentatives d'édition sont comptées, pas les lignes. Trois nouveaux fichiers d'implémentation : success.py, test unitaire et test intégration. Deux fichiers existants ont reçu un ajout minimal : façade et README, avec préfixes préexistants préservés. Cinq artefacts OpenSpec créés, tasks.md ensuite coché. L'unique commande d'archive a déplacé les cinq artefacts avec empreintes identiques ; ces écritures internes ne sont pas comptées comme cinq outils edit supplémentaires. Le présent rapport est hors intervalle.

## 4. Commandes

| Famille native | Nombre | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 33.3 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests | 5 | 41.7 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % |
| Récupération CAB | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Correction de test | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Contrôle sources | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Commande native (100 caractères max) | Nombre | Part | Résultat |
|---|---|---|---|
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-api-success-… | 3 | 25.0 % | {'completed': 3} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m un… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 2 | 16.7 % | {'error': 1, 'completed': 1} |
| /usr/bin/true | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 /home/devops/python/current/bin/python3 -c 'from pathlib imp… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundat… | 1 | 8.3 % | {'completed': 1} |
| /usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-api-success-r… | 1 | 8.3 % | {'completed': 1} |

Commandes exactes et preuves conservées dans output/cismp-state.json. Aucun regroupement shell ; chaque opération a son requestId unique et une permission distincte. Exécution seule du venv existant pour les régressions, aucune lecture/indexation du venv ni nouvelle installation.

## 5. Accès web

| Périmètre | Réussis | Refusés | Erreurs | Total | Part |
|---|---|---|---|---|---|
| Outils web natifs | 0 | 0 | 0 | 0 | N/A — dénominateur nul |

Aucun outil web ni commande d'installation ou d'accès réseau externe dans ce change. URLs visitées et noms de domaine externes : zéro dans les preuves natives. Les APIs loopback OpenCode/CAB sont du pilotage local, pas des visites web. L'accès normal au fournisseur LLM n'est pas une visite web ni un compteur réseau observé ; aucune requête HTTP globale n'est estimée.

## 6. Synthèse globale

| Domaine | Tentatives | Part | Réussies | Taux | Refusées | Taux | Erreurs | Taux | Hors mandat | Taux |
|---|---|---|---|---|---|---|---|---|---|---|
| Fichiers | 11 | 17.5 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 12 | 19.0 % | 11 | 91.7 % | 0 | 0.0 % | 1 | 8.3 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 40 | 63.5 % | 40 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 63 | 100.0 % | 62 | 98.4 % | 0 | 0.0 % | 1 | 1.6 % | 0 | 0.0 % |

Les totaux par domaines et par outils concordent. Les décisions CAB, sondes, quotas N/A et écritures internes de l'archivage restent séparés des tentatives natives. Aucun secret, Git, PostgreSQL réel, nouvelle dépendance ou activation dans le périmètre observé. Les incidents de pilotage root et les propositions révisées avant écriture ne sont pas présentés comme des outils échoués de l'agent de codage.

Archivage vérifié, rapport produit séparément après l'intervalle ; retour à SÉLECTION du RUN parent avec CAB actif. Aucun état terminal ni fin de session annoncé à ce jalon.
