# Statistiques — add-initial-notification-contract-representation

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-representation. RUN : cismp-pixs-20261005-2654fe47.
Intervalle : 2026-10-05T18:41:08.488858+00:00 → 2026-10-06T09:42:26.445631+00:00. Les pauses et attentes sont incluses ; la rédaction de ce rapport est exclue.
Couverture : historique intégral accessible des maîtres ses_ef0164a8affe0oQD8vnPicLqgV, ses_eefa39c24ffe1dGvdToTr4NfJh. Les deux anciens maîtres ses_ef2a4f92bffeGuqEcFcTaBn3mG, ses_ef29f5ae8ffe375Eo4U42lDPvR répondent HTTP 404 ; leurs messages, tokens et outils exhaustifs sont N/A. Leurs mandats prouvés conservés sont distingués des comptages accessibles. Les totaux ci-dessous portent seulement sur ce corpus accessible, jamais sur un historique reconstitué.
Convention : une exécution sans erreur technique ne prouve pas une approbation manuelle ; les décisions CAB sont comptées séparément. Un refus explicite est distingué d'une erreur, interruption, abandon ou échec CLI. Les échecs OpenSpec de longueur restent des exits 1, même lorsque leur qualification documentaire autorise le cycle.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A — version non exposée | opencode-go | xhigh | N/A — sondes comparables invalides | N/A — sondes comparables invalides | 863.363 s de parties générées observées ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex /root | N/A — télémétrie exacte non exposée | OpenAI | N/A — télémétrie non exposée | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — télémétrie de génération indisponible |

Le temps mesuré du codeur additionne les intervalles horodatés des parties reasoning/text, sans les appels outils ni les attentes de permission. Il ne couvre pas les maîtres disparus. Le dénominateur de service de tous les agents est inconnu ; les parts sont N/A. Les sessions de sondes sont séparées de la production et peuvent se chevaucher.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Durée calendaire du change | 15 h 01 min 17 s |
| Messages accessibles | 184 (100.0 %) |
| Appels outils accessibles | 146 (100.0 %) |
| Tokens entrée (hors cache) | 834 |
| Tokens sortie | 71763 |
| Tokens raisonnement exposés | 0 |
| Cache lu | 14090971 |
| Cache écrit | 491620 |
| Coût API production accessible (USD) | 0.357633246 |
| Compactions | 0 observées ; historique manquant N/A |

| Décision CAB finale observée | Mandats distincts (% décisions observées) |
| --- | --- |
| APPROVED | 28 (93.3 %) |
| NEEDS_CLARIFICATION | 1 (3.3 %) |
| REJECTED | 1 (3.3 %) |
| Total | 30 (100.0 %) |

Résultat : 6/6 tâches prouvées (100,0 %) ; 91/91 tests réussis (100,0 %), zéro échec ni erreur de test ; trois compilations réussies. Prévalidations historiques avant code : trois exits 0 conservés. Validation stricte actuelle du change : exit 0. Global : 77 éléments, 66 passés (85,7 %) et 11 échoués (14,3 %) ; uniquement 19 WARNING de longueur autorisés, aucun ERROR ni autre issue. La qualification ne transforme pas le CLI global en réussite.
Les incidents CAB antérieurs (dont décisions auxiliaires), demandes abandonnées et corrections de rapports restent dans le registre du RUN. Les validations du présent change ont été reprises sous décisions root corrélées. Le rapport d'archivage inexact a été rectifié ; le JSON natif établit specsUpdated=false et zéro opération normative.

### Sondes et surcharge de télémétrie

Le protocole actuel conserve le même prompt fixe de 48 lignes : quatre relèves (début, +30 min, +60 min, fin), quatre échecs (100,0 %), zéro relève valide (0,0 %) et zéro manquée (0,0 %). Elles ont utilisé zéro outil ; les sessions jetables ont été supprimées. Aucune moyenne n'est calculée sur ces sorties divergentes.
| Position | Envoi UTC | Statut | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- |
| début | 2026-10-06T08:40:48.486798+00:00 | failed | 267 | 0.000553934 |
| +30 min | 2026-10-06T09:10:48.744080+00:00 | failed | 5180 | 0.0048059 |
| fin | 2026-10-06T09:40:21.685961+00:00 | failed | 745 | 0.00272145 |
| +60 min | 2026-10-06T09:40:49.167213+00:00 | failed | 607 | 0.000475822 |

Historique antérieur : une sonde du 5 octobre déclarée success (522 tokens, TTMT 1,8942 s, débit 80,0022 tokens/s), mais prompt différent de 128 lignes et conformité exacte non conservée : exclue des moyennes comparables. Reprise du 6 octobre matin : trois tentatives invalides (560 + 653 + 779 tokens) et une relève +30 min manquée, sans reconstruction rétroactive. Les échéances supplémentaires des maîtres disparus sont N/A. Ces données ne sont pas mélangées à la production.

| Surcharge actuelle de sondes | Valeur |
| --- | --- |
| Tokens sortie | 6799 |
| Coût connu USD | 0.008557106 |
| Durée de génération fiable | N/A — sorties fixes invalides ou horodatages insuffisants |

## 2. Types de messages et d'outils

| Rôle | Messages (% messages) |
| --- | --- |
| assistant | 141 (76.6 %) |
| user | 43 (23.4 %) |
| Total | 184 (100.0 %) |

| Type de partie | Occurrences (% parties) |
| --- | --- |
| reasoning | 141 (19.7 %) |
| step-finish | 139 (19.4 %) |
| step-start | 141 (19.7 %) |
| text | 148 (20.7 %) |
| tool | 146 (20.4 %) |
| Total | 715 (100.0 %) |

| Terminaison assistant | Messages (% assistants) |
| --- | --- |
| absent | 2 (1.4 %) |
| stop | 39 (27.7 %) |
| tool-calls | 100 (70.9 %) |
| Total | 141 (100.0 %) |

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| bash | 21 (14.4 %) | 18 (85.7 %) | 0 (0.0 %) | 3 (14.3 %) |
| cgpt-validation_broker_readiness | 25 (17.1 %) | 25 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 12 (8.2 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 11 (7.5 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 5 (3.4 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 30 (20.5 %) | 28 (93.3 %) | 0 (0.0 %) | 2 (6.7 %) |
| edit | 3 (2.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 11 (7.5 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 2 (1.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| invalid | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 24 (16.4 %) | 23 (95.8 %) | 0 (0.0 %) | 1 (4.2 %) |
| write | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 146 (100.0 %) | 140 (95.9 %) | 0 (0.0 %) | 6 (4.1 %) |

## 3. Fichiers modifiés

Les nombres sont des tentatives natives visibles, non des lignes modifiées ni une déduction depuis Git.
| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/design.md | 1 (25.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/tasks.md | 2 (50.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_notification_contract_integration.py | 1 (25.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 4 (100.0 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Preuves historiques conservées hors corpus exhaustif : création du module /home/devops/datas/pixs/src/pixs/kernel/notification_contract.py et du test /home/devops/datas/pixs/tests/unit/test_notification_contract.py ; création des cinq artefacts OpenSpec du change. Leur nombre total de tentatives/refus/erreurs est N/A (maîtres HTTP 404). Le test d'intégration est visible dans le corpus et dans le registre.
Archivage : six fichiers déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-representation, tous vérifiés identiques ; aucune spec canonique modifiée (76/76 inchangées, 100,0 %). Ce déplacement n'est pas compté comme six éditions natives. STATISTIQUES.md est écrit ensuite par un mandat séparé et reste hors intervalle de mesure.

## 4. Commandes

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| OpenSpec | 6 (28.6 %) | 3 (50.0 %) | 0 (0.0 %) | 3 (50.0 %) |
| Prévol true | 7 (33.3 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 8 (38.1 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 21 (100.0 %) | 18 (85.7 %) | 0 (0.0 %) | 3 (14.3 %) |

Commandes refusées :
Aucune commande native refusée visible : 0 occurrence ; taux sur les refus N/A. Les décisions CAB REJECTED ou needs_clarification sans exécution ne sont pas des commandes exécutées.

Échecs CLI observés : les validations globales strictes retournent 1 sur les avertissements de longueur ; elles restent dans les erreurs de résultat du tableau, distinctes d'un refus de permission. Les autres erreurs/interruption d'outil sont également distinguées des tests réussis.

## 5. Accès web

Codeur : aucun appel webfetch/websearch visible, 0 accès ; approbations 0, refus 0, erreurs 0, taux internes N/A (dénominateur nul). Aucune URL refusée observée.
Orchestrateur : la qualification PLLM autorisée utilise https://opencode.ai/zen/go/v1/messages ; les échanges opérationnels OpenCode/CAB utilisent http://127.0.0.1:4096 et http://127.0.0.1:8788. Ces endpoints autorisés sont distingués du web du codeur. Le nombre exhaustif d'échanges HTTP de pilotage est N/A ; aucune lecture de secret n'est représentée par ces URL.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-05T18:41:08.488858+00:00 |
| Fin — après archivage et sondes | 2026-10-06T09:42:26.445631+00:00 |
| Durée globale (pauses et attentes incluses) | 15 h 01 min 17 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A | N/A — outil get_usage_limits non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-06T09:42:26.445631+00:00 | N/A — outil get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

Les quotas sont partagés par le compte ; une différence représenterait sa variation pendant l'intervalle, sans attribution exclusive. Aucune conversion en tokens ou en euros n'est effectuée.

| Catégorie | Tentatives (% tableau) | Exécutées sans erreur outil/CLI (% ligne) | Refusées (% ligne) | Erreurs (% ligne) |
| --- | --- | --- | --- | --- |
| autres | 121 (82.9 %) | 118 (97.5 %) | 0 (0.0 %) | 3 (2.5 %) |
| commandes | 21 (14.4 %) | 18 (85.7 %) | 0 (0.0 %) | 3 (14.3 %) |
| fichiers | 4 (2.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 146 (100.0 %) | 140 (95.9 %) | 0 (0.0 %) | 6 (4.1 %) |

Ces totaux recoupent exactement les tableaux par outil, fichier et famille de commande du corpus accessible. Les totaux globaux du RUN incluant les maîtres disparus et l'orchestrateur sont N/A, jamais extrapolés.
Tests : 91 réussis, trois compilations réussies. Archivage : réussi, exit 0, six fichiers vérifiés, zéro opération normative. Git : non inspecté ; aucun commit/push mandaté. PostgreSQL : autorisé, non nécessaire pour ce contrat pur, aucun test base exécuté. Accès externes : qualification fournisseur documentée ; tests d'intégration sans réseau, process non autorisé, modification d'environnement, écriture ni base. Secrets : aucun ajouté dans les fichiers livrés ; les valeurs d'authentification sont restées hors du modèle et du rapport.
