# STATISTIQUES — add-initial-data-persistence-state-vocabulary

Intervalle audité : 2026-10-06T18:10:35.951059+00:00 → 2026-10-06T19:45:41.616984+00:00. Deux sessions de codage du même RUN : `ses_eeddcf293ffe0KHaxHxS3Gc5p9`, `ses_eed633581ffeOeSPxYZNclbGnr`. Rédaction/publication du rapport hors intervalle ; sondes séparées des compteurs de production mais incluses dans la durée calendaire.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash (build) | Agent OpenCode 1.18.34 ; LLM N/A | OpenCode Go | xhigh | N/A — sondes invalides | N/A — sondes invalides | N/A — génération active non isolée |
| Qwen3.8 Flash (compactage natif) | Agent OpenCode 1.18.34 ; LLM N/A | OpenCode Go | N/A en message ; configuration xhigh vérifiée | N/A — non sondé | N/A — non mesurable isolément | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex /root (GPT6, ID exact non exposé) | N/A | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A |

Aucune version LLM n’est déduite du nom commercial. Les temps de service et leur dénominateur sont N/A ; les timestamps de message incluent outils/attentes et ne prouvent pas une durée active de génération. Aucun débit pondéré fiable n’est reconstitué.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Messages OC | 208 (100 %) |
| Outils OC | 159 (100 %) |
| Approuvé/exécuté | 144 (90.6 %) |
| Refus explicites | 1 (0.6 %) |
| Erreurs | 14 (8.8 %) |
| Décisions CAB observées | 33 APPROVED (97.1 %) ; 1 REJECTED (2.9 %) ; total 34 (100 %) |
| Éditions natives réussies | 9 (100 % des éditions) sur 8 fichiers |
| Tests | 2 unitaires + 1 intégration + 14 régressions = 17 / 17 (100 %), code 0 |
| Compilations | 3 / 3 (100 %), code 0 |
| Tâches | 6 / 6 prouvées puis cochées (100 %) |
| Archive | 1 / 1 (100 %), code 0 ; specsUpdated=false |
| Compactages dans l’intervalle | 1 natif OC ; zéro compactage Codex exécuté (API non exposée) |

Convention : un appel terminé avec succès est approuvé/exécuté ; les lectures permises automatiquement ne prouvent pas une décision manuelle. Un refus est une permission explicitement rejetée. Les quatre CLI globaux code 1 restent quatre erreurs de commande dans les chiffres ; seuls leurs 19 WARNING de longueur exactement historiques, zéro ERROR et la couverture 76/77 ont été qualifiés pour ce change. Cela ne convertit jamais 1 en 0. Les dix autres erreurs sont des appels MCP en échec/interrompus : request_validation 7, poll_approval 3.

Incidents tracés : délai MCP récupéré par polling corrélé sans réémission ; entrée sans session_id puis resoumission autonome rejetée avant écriture ; variation de requestId avant effet examinée explicitement par ROOT ; rapport de création du module sans outil natif ni fichier réel invalidé, ancien contexte gelé, reprise en R2 ; commande de test aux backslash-n littéraux tenue par le garde strict, permission rejetée avant exécution, récupération puis nouveau programme une ligne ; une variation typographique d’apostrophe dans design.md explicitement acceptée après diff, sans changement normatif. Aucune écriture source hors périmètre ni effet inconnu observé.

Deux décisions APPROVED n’ont pas produit l’opération annoncée : module de l’ancien contexte et ancien programme de test divergent. Elles ne sont pas comptées comme écritures ou tests réussis. Leurs autorisations locales inutilisées ont été effacées par rechargement contrôlé du contrôleur à une borne réconciliée. Les 31 autres opérations autorisées sont réellement outillées (9 éditions + 22 commandes terminées, dont quatre sorties CLI 1) ; le refus natif de la commande divergente reste distinct du rejet d’un mandat CAB. OpenCode est resté ouvert.

| Compteur natif de production OC | Valeur |
| --- | --- |
| input | 984 |
| output | 62319 |
| reasoning | 0 |
| total | 14192960 |
| cache_read | 13654243 |
| cache_write | 475414 |
| Coût natif OC | 0.342988218 USD |

Compteurs bruts sans estimation ; le champ reasoning=0 ne prouve pas l’absence de réflexion. Total = 984 + 62 319 + 13 654 243 + 475 414 = 14 192 960. Tokens/coût de sondes ci-dessous séparés.

| Relève | Tentatives | Réussies | Échouées | Lignes |
| --- | --- | --- | --- | --- |
| Début | 2 | 0 | 2 | 1 puis 43 |
| +30 min | 2 | 0 | 2 | 45 puis 43 |
| +60 min | 2 | 0 | 2 | 43 puis 43 |
| +90 min | 2 | 0 | 2 | 47 puis 1 |
| Fin | 2 | 0 | 2 | 57 puis 3 |
| Total | 10 (100 %) | 0 (0 %) | 10 (100 %) | Aucune sortie fixe de 200 lignes |

Relèves prévues 5, réussies 0, échouées 5, manquées 0 ; une seule reprise immédiate par relève. Dix tentatives invalides exclues des moyennes/minima/maxima, tous N/A motivés par la sortie non conforme. Sessions dédiées jetables, Qwen3.8 Flash/OpenCode Go/xhigh, zéro outil, aucun accès fichier ou réseau par le modèle. Surcharge complète de sonde : 7039 tokens de sortie et 0.012852562 USD ; timing brut conservé dans le checkpoint, aucune moyenne fabriquée. Les sondes périodiques ont été exécutées aux créneaux en parallèle du pilotage ; le travail n’a jamais été arrêté pour attendre un créneau.

Compactage natif observé : `msg_11270a1fc001OzbyiUcfKcLxsx`, provider opencode-go/model qwen3.8-flash, summary=true/finish=stop et réponse native 200 true. Le champ variant du message n’est pas exposé ; configuration de l’agent compaction xhigh vérifiée. Résumé obsolète sur la sélection/metadata : corrigé par réinjection de faits et readiness MCP réelle avant poursuite. Codex API absente : succès conjoint non déclaré ; cette absence n’a pas bloqué le RUN.

## 2. Types de messages et d’outils

| Rôle | Nombre et part |
| --- | --- |
| user | 42 (20.2 %) |
| assistant | 166 (79.8 %) |
| Total | 208 (100 %) |

| Type de partie | Nombre et part |
| --- | --- |
| text | 139 (17.5 %) |
| step-start | 165 (20.8 %) |
| reasoning | 165 (20.8 %) |
| tool | 159 (20.1 %) |
| step-finish | 164 (20.7 %) |
| compaction | 1 (0.1 %) |
| Total | 793 (100 %) |

| Fin assistant | Nombre et part |
| --- | --- |
| tool-calls | 124 (74.7 %) |
| stop | 40 (24.1 %) |
| incomplete | 2 (1.2 %) |
| Total | 166 (100 %) |

| Outil | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| read | 29 (18.2 %) | 29 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 10 (6.3 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 35 (22.0 %) | 28 (80.0 %) | 0 (0.0 %) | 7 (20.0 %) |
| write | 8 (5.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 16 (10.1 %) | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 15 (9.4 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 8 (5.0 %) | 5 (62.5 %) | 0 (0.0 %) | 3 (37.5 %) |
| bash | 23 (14.5 %) | 18 (78.3 %) | 1 (4.3 %) | 4 (17.4 %) |
| cgpt-validation_list_pending | 2 (1.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 (0.6 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 11 (6.9 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (0.6 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 159 (100.0 %) | 144 (90.6 %) | 1 (0.6 %) | 14 (8.8 %) |


## 3. Fichiers modifiés

| Chemin absolu pendant l’édition | Tentatives et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-persistence-state-vocabulary/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-persistence-state-vocabulary/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-persistence-state-vocabulary/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-persistence-state-vocabulary/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-persistence-state-vocabulary/specs/data-lifecycle/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_persistence_states.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_persistence_states.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_persistence_states_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Il s’agit de tentatives d’édition réellement outillées. Les cinq artefacts du change ont été déplacés vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-data-persistence-state-vocabulary/`. Le cochage des six cases est la seule modification supplémentaire de tasks.md, vérifiée octet à octet. Trois fichiers source/test, cinq artefacts archivés et 136 références contrôlés inchangés après archive ; aucune spec principale modifiée. Aucun write fantôme ajouté au tableau.

## 4. Commandes

| Famille (≤100 caractères) | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| CAB /usr/bin/true | 6 (26.1 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validations OpenSpec | 9 (39.1 %) | 5 (55.6 %) | 0 (0.0 %) | 4 (44.4 %) |
| Compilations py_compile | 3 (13.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 4 (17.4 %) | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) |
| Archivage OpenSpec | 1 (4.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 23 (100.0 %) | 18 (78.3 %) | 1 (4.3 %) | 4 (17.4 %) |

Toutes les commandes refusées, regroupées :

| Commande (tronquée à 100 caractères) | Occurrences et part des commandes |
| --- | --- |
| /home/devops/python/current/bin/python3 -B -c 'import sys\nsys.path.insert(0, "src")\nimport unitte… | 1 (4.3 %) |

Une commande aux escapes divergents a été refusée AVANT exécution ; aucun test n’a commencé pour ce mandat. Le programme de remplacement est une seule expression Python, pas une composition shell. Quatre CLI globaux natifs 1 restent qualifiés uniquement selon leurs issues historiques ; toutes les compilations, commandes de tests effectifs et l’archive ont code 0.

## 5. Accès web

| Outils web OC | Total | Approuvé | Refusé | Erreur |
| --- | --- | --- | --- | --- |
| webfetch / websearch | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucune URL visitée ou refusée par un outil web OC dans l’intervalle. HTTP techniques de l’orchestrateur hors de ce dénominateur : quantitatif N/A, historique natif Codex non accessible. Endpoints réellement utilisés/autorisés : `http://127.0.0.1:4096`, `http://127.0.0.1:8788`, `https://opencode.ai/zen/go/v1/usage`. Le directory et les sessions ont été corrélés au projet ; aucun header ou secret reproduit.

## 6. Synthèse globale

| Durée de session de codage | Valeur |
| --- | --- |
| Début | 2026-10-06T18:10:35.951059+00:00 |
| Fin — après archivage et sonde finale | 2026-10-06T19:45:41.616984+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 35 min 06 s (5705.665925 s) |

| Mesure quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début | N/A — outil natif non exposé | N/A | N/A |
| Après — après archivage | N/A — outil natif non exposé | N/A | N/A |
| Différence après − avant | — | N/A — deux relevés manquants | — |

Quotas partagés par le compte ; aucune consommation exclusivement attribuée au RUN. Aucun quota Spark, ancien quota ni conversion token/monnaie substitué au relevé Codex.

| Domaine | Total et part globale | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| Fichiers | 9 (5.7 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 23 (14.5 %) | 18 (78.3 %) | 1 (4.3 %) | 4 (17.4 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 127 (79.9 %) | 117 (92.1 %) | 0 (0.0 %) | 10 (7.9 %) |
| Global | 159 (100.0 %) | 144 (90.6 %) | 1 (0.6 %) | 14 (8.8 %) |

Totaux croisés : 9 éditions + 23 commandes + 0 web + 127 autres outils = 159. Pourcentages arrondis à une décimale ; dénominateur zéro = N/A. Télémétrie Codex hors décisions CAB : N/A, non reconstituée.

Résultat : enum interne partiel des quatre états communs livré, 17 tests/3 compilations réussis, six tâches prouvées, archive vérifiée sans changement normatif. Ce vocabulaire ne prouve ni transition, suppression logique, purge, métadonnée, rétention, legal hold, tombstone, anti-résurrection ni runtime. Git non inspecté ni modifié par les agents, aucun commit/push. PostgreSQL et navigateur sans objet pour ce module pur. Les nouveaux fichiers relus ne contiennent aucun secret ; accès fournisseurs confinés aux processus dédiés/stockage natif autorisé. Le rapport de création non prouvé a été refusé comme preuve ; seule l’écriture native réelle en R2 est comptée. RUN parent actif : retour SÉLECTION après publication vérifiée du rapport.
