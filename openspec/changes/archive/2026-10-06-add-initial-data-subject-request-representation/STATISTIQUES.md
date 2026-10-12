# STATISTIQUES — add-initial-data-subject-request-representation

Périmètre : reprise CISMP du 2026-10-06T16:48:19.985000+00:00 au 2026-10-06T17:53:41.817551+00:00, deux sessions maîtresses réellement utilisées. Rapport produit après archivage ; sa rédaction et sa publication sont hors de l’intervalle mesuré.

- `ses_eede2b85bffen28NFlw9Yzb2Dw`
- `ses_eeddcf293ffe0KHaxHxS3Gc5p9`

Les trois artefacts `.openspec.yaml`, `proposal.md` et `design.md` avaient été préparés avant ce RUN. Leurs empreintes ont été vérifiées à la reprise puis à l’archivage ; cette préparation historique n’est pas ajoutée artificiellement aux tentatives, tokens ou temps ci-dessous.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash (`qwen3.8-flash`) | Agent OpenCode 1.18.34 ; version LLM N/A | OpenCode Go (`opencode-go`) | xhigh | N/A — aucune sonde valide | N/A — aucune sonde valide | N/A — durée active de génération non isolée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex /root (GPT6 ; identifiant exact non exposé) | N/A | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — télémétrie native indisponible |

Les temps de service ne sont pas assimilés à la durée calendaire, aux attentes CAB ni aux durées des outils. Dénominateur de service et chevauchements : N/A ; aucun débit pondéré de session fiable n’est disponible.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Messages OC | 160 (100 %) |
| Appels d’outils OC | 115 (100 %) |
| Appels approuvés/exécutés | 106 (92.2 %) |
| Refus explicites | 1 (0.9 %) |
| Erreurs d’outils ou sorties natives non nulles | 8 (7.0 %) |
| Décisions CAB explicites de Codex /root | 27 APPROVED / 27 (100 %) ; zéro décision CAB rejetée |
| Compilations | 3 / 3, code 0 (100 %) |
| Tests | 15 unitaires + 1 intégration + 33 régressions = 49 / 49 (100 %) |
| Tâches | 6 / 6 prouvées puis cochées (100 %) |
| Archivage | 1 / 1, code 0 (100 %) ; specsUpdated=false |
| Compactions | 0 observée dans les sessions OC de l’intervalle ; Codex N/A |

Convention : « approuvé/exécuté » signifie appel terminé avec succès ; une lecture automatiquement permise ne prouve pas une approbation manuelle. Un refus est une permission explicitement rejetée. Une erreur est un échec sans refus ; les quatre validations globales code 1 sont donc comptées comme erreurs CLI, même si leurs 19 WARNING de longueur sont exactement ceux de la référence autorisée et ne bloquent pas ce change. Aucun ERROR OpenSpec nouveau n’a été observé.

Les autres erreurs sont trois délais MCP récupérés par polling corrélé, sans réémission ni exécution doublée, et une lecture d’un chemin absent (`src/pixs/kernel/diagnostics.py`) corrigée par lecture de son package. Le refus concerne uniquement `ls` hors mandat ; cette opération n’a pas été exécutée. La session fautive a été interrompue et la récupération CAB a été prouvée. Un requestId d’édition des cases a été remplacé avant effet ; Codex a examiné et accepté explicitement le nouvel ID, sans élargissement.

| Compteur de production OC | Valeur |
| --- | --- |
| input | 750 |
| output | 86806 |
| reasoning | 0 |
| total | 18256228 |
| cache_read | 17911671 |
| cache_write | 257001 |
| Coût natif agrégé OC | 0.378898256 USD |

Les compteurs sont ceux de l’API OC, sans estimation. Le champ reasoning vaut 0 dans cette télémétrie ; cela ne prouve pas l’absence de réflexion. Le total inclut les caches : 750 + 86 806 + 17 911 671 + 257 001 = 18 256 228. Coût, tokens et durée de sondes restent séparés de la production.

| Relève | Tentatives | Réussies | Échouées | Lignes produites |
| --- | --- | --- | --- | --- |
| Début | 2 | 0 | 2 | 63 puis 1 |
| +30 min | 2 | 0 | 2 | 1 puis 43 |
| Fin | 2 | 0 | 2 | 35 puis 43 |
| Total | 6 (100 %) | 0 (0 %) | 6 (100 %) | Aucune sortie fixe de 200 lignes |

Relèves prévues pendant l’activité de ce change : 3 ; réussies 0, échouées 3, manquées 0. Chaque échec a eu une seule reprise immédiate. La relève +60 min n’est pas due pour ce change : le travail et l’archivage étaient terminés avant son échéance ; la sonde finale a été lancée immédiatement, sans attendre un créneau. Les six tentatives sont invalides et exclues des moyennes/minima/maxima. Sessions jetables, même modèle/fournisseur/xhigh, zéro outil, aucun accès fichier ni réseau par le modèle. Surcharge initiale : coût/tokens exhaustifs N/A, toutes les métadonnées initiales n’ont pas été conservées ; surcharge +30 min : 1 081 tokens de sortie et 0.002931142 USD ; surcharge finale : 1 733 tokens de sortie et 0.003114982 USD. Les mesures brutes invalides restent tracées dans le checkpoint ; aucun apprentissage de performance n’est fabriqué.

## 2. Types de messages et d’outils

| Rôle | Nombre et part |
| --- | --- |
| user | 34 (21.2 %) |
| assistant | 126 (78.8 %) |
| Total | 160 (100 %) |

| Type de partie | Nombre et part |
| --- | --- |
| text | 104 (17.5 %) |
| step-start | 125 (21.0 %) |
| reasoning | 125 (21.0 %) |
| tool | 115 (19.4 %) |
| step-finish | 125 (21.0 %) |
| Total | 594 (100 %) |

| Fin de réponse assistant | Nombre et part |
| --- | --- |
| tool-calls | 92 (73.0 %) |
| stop | 33 (26.2 %) |
| incomplete | 1 (0.8 %) |
| Total | 126 (100 %) |

| Outil | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 11 (9.6 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 27 (23.5 %) | 24 (88.9 %) | 0 (0.0 %) | 3 (11.1 %) |
| cgpt-validation_get_approval | 6 (5.2 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 4 (3.5 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 22 (19.1 %) | 17 (77.3 %) | 1 (4.5 %) | 4 (18.2 %) |
| cgpt-validation_list_pending | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 30 (26.1 %) | 29 (96.7 %) | 0 (0.0 %) | 1 (3.3 %) |
| glob | 7 (6.1 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 5 (4.3 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 115 (100.0 %) | 106 (92.2 %) | 1 (0.9 %) | 8 (7.0 %) |


## 3. Fichiers modifiés

| Chemin absolu pendant l’édition | Tentatives et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-representation/tasks.md | 2 (33.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-subject-request-representation/specs/data-governance/spec.md | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_subject_request.py | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_subject_request.py | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_subject_request_integration.py | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 6 (100.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Ces nombres décrivent des tentatives d’édition : cinq fichiers distincts, six éditions réussies. Le seul changement supplémentaire de tasks.md est le cochage des six cases, vérifié octet à octet. Les cinq artefacts du change ont été déplacés vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-data-subject-request-representation/` ; empreintes des cinq artefacts, trois fichiers source/test et 127 références inchangées après archive. Aucun fichier de spec principal modifié. DEVOPS.md avait changé avant ce RUN ; son empreinte actuelle a été isolée et figée avant les opérations.

## 4. Commandes

| Famille (libellé ≤100 caractères) | Total et part | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| CAB /usr/bin/true | 5 (22.7 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Lecture ls hors mandat | 1 (4.5 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 9 (40.9 %) | 5 (55.6 %) | 0 (0.0 %) | 4 (44.4 %) |
| Compilation py_compile | 3 (13.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (13.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archivage OpenSpec | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 22 (100.0 %) | 17 (77.3 %) | 1 (4.5 %) | 4 (18.2 %) |

Toutes les commandes refusées :

| Commande refusée (≤100 caractères) | Occurrences et part des commandes |
| --- | --- |
| ls /home/devops/datas/pixs/openspec/changes | 1 (4.5 %) |

Aucune commande composée ni suffixe autorisé. Les programmes Python multiligne sont un argument unique de `-c`. Quatre sorties code 1 appartiennent seulement aux validations globales avant/après code ; 5 validations ciblées code 0, 3 compilations code 0, 3 commandes de tests code 0 et 1 archive code 0.

## 5. Accès web

| Outils web des agents OC | Total | Approuvé | Refusé | Erreur |
| --- | --- | --- | --- | --- |
| webfetch / websearch | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucune URL visitée ou refusée par un outil web OC. Les HTTP techniques de l’orchestrateur sont hors de ce dénominateur : inventaire quantitatif N/A faute d’historique natif Codex accessible. Endpoints réellement utilisés et autorisés : `http://127.0.0.1:4096`, `http://127.0.0.1:8788`, `https://opencode.ai/zen/go/v1/usage`, `https://opencode.ai/zen/go/v1/messages`. Leur statut est « utilisé/autorisé », jamais déduit d’une simple requête. Paramètre directory et session corrélés au projet pour les API de contexte. Aucune valeur d’authentification n’est reproduite.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-06T16:48:19.985000+00:00 |
| Fin — après archivage et sonde finale | 2026-10-06T17:53:41.817551+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 05 min 22 s (3 921.832551 s) |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil natif non exposé | N/A | N/A |
| Après — après archivage | N/A — outil natif non exposé | N/A | N/A |
| Différence après − avant | — | N/A — deux relevés manquants | — |

Les quotas sont partagés par le compte ; même une variation disponible ne pourrait être attribuée exclusivement à ce RUN sans preuve. Aucun quota Spark, ancien relevé ou calcul de tokens ne se substitue au quota Codex hebdomadaire.

| Domaine | Total et part globale | Approuvé/exécuté et taux | Refusé et taux | Erreur et taux |
| --- | --- | --- | --- | --- |
| Fichiers | 6 (5.2 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 22 (19.1 %) | 17 (77.3 %) | 1 (4.5 %) | 4 (18.2 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 87 (75.7 %) | 83 (95.4 %) | 0 (0.0 %) | 4 (4.6 %) |
| Global | 115 (100.0 %) | 106 (92.2 %) | 1 (0.9 %) | 8 (7.0 %) |

Totaux croisés : 6 éditions + 22 commandes + 0 outil web + 87 autres outils = 115. Les proportions sont arrondies à une décimale ; un dénominateur nul est N/A. Les statistiques natives Codex hors décisions CAB sont N/A et ne sont pas reconstituées.

Résultat du change : représentation déclarative interne et partielle livrée ; 49 tests et trois compilations réussis, six tâches prouvées, archive vérifiée sans modification normative des specs. Cette unité ne prouve aucun traitement, autorisation, audit, idempotence, propagation, legal hold ni rétention. Git n’a pas été inspecté ni modifié ; aucun commit/push. Tests PostgreSQL et navigateur sans objet pour ce module pur. Aucun secret dans les trois nouveaux fichiers relus ; les accès fournisseur ont été confinés aux processus dédiés et au stockage natif autorisé. Le RUN parent reste actif et doit revenir à SÉLECTION après publication vérifiée de ce rapport.
