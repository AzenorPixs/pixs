# Statistiques — BulkAuthorityAction v1 — CISMP5

RUN `cismp5-pixs-67c71050f2dd45ce` ; contexte CAB `344` ; session de codage `ses_eaf909b9cffeD4TteINaIPJSqa` ; change `add-initial-bulk-authority-action-v1`. Archive : `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-authority-action-v1`.

Intervalle de collecte fixé avant rédaction : 18/10/2026 21:07:15 UTC+2 (Europe/Paris) → 18/10/2026 21:41:07 UTC+2 (Europe/Paris). Les compteurs natifs portent sur l’historique complet de la seule session du change (créée 18/10/2026 21:13:59 UTC+2 (Europe/Paris)). La présélection antérieure, les sondes jetables et les outils de l’orchestrateur sont séparés ; les appels HTTP de pilotage ne sont pas intégralement instrumentés. Ce rapport et sa vérification sont hors intervalle, sans auto-comptage.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 1.985 s | 435.546 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex / GPT-6 | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version exacte du modèle non exposée : ne pas la déduire de son identifiant. OpenCode observé : 1.19.3 ; CAB : 1.3.0. Temps de service et pourcentage N/A : les durées natives ne séparent pas fiablement génération, outils et attentes ; aucun dénominateur de service ni chevauchement mesuré. Aucune sonde de l’orchestrateur.

## 1. Statistiques générales et décisions

Durée globale : **00 h 33 min 52 s**, pauses et attentes incluses. Une opération native terminée avec succès décrit l’état de l’outil et son autorisation technique ; elle ne prouve pas une approbation manuelle. Une commande strict globale avec exit 1 reste un diagnostic exécuté, pas un succès strict. Les décisions CAB et les appels natifs sont deux dénominateurs distincts, jamais additionnés.

| Décisions CAB | Nombre | Part des décisions |
|---|---:|---:|
| Approuvées | 23 | 92.0 % |
| Refusées | 2 | 8.0 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 25 | 100 % |

Permissions once consommées : **17**, correspondant aux **8 écritures et 9 commandes** exécutées. Certaines décisions approuvées ont fini sans effet après accès périmé ou annulé ; elles ne sont pas des exécutions.

| Appels d’outils natifs | Nombre | Part |
|---|---:|---:|
| Autorisés et terminés | 84 | 97.7 % |
| Refus natifs | 0 | 0.0 % |
| Erreurs techniques MCP | 2 | 2.3 % |
| Total | 86 | 100 % |

Erreurs MCP : une demande -32602 avant enregistrement (manifeste incomplet), et un timeout -32001. Le timeout a été réconcilié sur le même approval_id : PENDING / notification FAILED, puis CANCELLED natif, sans effet. Deux refus CAB pour révisions périmées restent distincts. Le contrôleur recense 13 réponses HTTP techniques : run-not-quiescent=3, native-session-not-quiescent=1, resource-revision-stale=7, decision-run-divergent=1, native-validation-not-correlated=1. Ces événements de transport peuvent recouvrir les attentes et ne s’ajoutent pas aux 86 outils.

Avant le contexte 344 : un candidat déjà qualifié a été libéré sans écriture ; un autre appartenait à CISMP6. Une relance prématurée du superviseur a été interrompue avant effet natif, permission refusée, puis récupération prepare/complete avec prévol once frais. Ces faits de présélection ne sont pas inclus dans les compteurs du change.

| Télémétrie native de production | Valeur |
|---|---:|
| Tokens d’entrée déclarés | 337259 |
| Tokens de sortie déclarés | 36081 |
| Tokens de raisonnement déclarés | 9876 |
| Cache lu | 13237916 |
| Cache écrit | 0 |
| Coût API déclaré, unité monétaire non exposée | 0.069393132 |
| Compactions observées | 0 |

Les compteurs de tokens sont conservés séparément selon la télémétrie ; aucune conversion en coût ou quota n’est estimée.

Sondes jetables, même fournisseur/modèle/high et même prompt fixe (nombres 1 à 160) :

| Relève | Envoi | Premier token SSE | Dernier token SSE | Tokens de sortie | TTMT | Débit de réponse |
|---|---|---|---|---:|---:|---:|
| début mesuré | 18/10/2026 21:15:57 UTC+2 (Europe/Paris) | 18/10/2026 21:15:59 UTC+2 (Europe/Paris) | 18/10/2026 21:16:00 UTC+2 (Europe/Paris) | 328 | 1.944 s | 408.468 tokens/s |
| fin | 18/10/2026 21:40:47 UTC+2 (Europe/Paris) | 18/10/2026 21:40:49 UTC+2 (Europe/Paris) | 18/10/2026 21:40:50 UTC+2 (Europe/Paris) | 328 | 2.026 s | 462.623 tokens/s |

Relèves prévues 2, réussies 2 (100 %), échouées 0 (0 %), manquées 0 (0 %). Moins de trente minutes séparent la sonde initiale mesurée et la fin du codage ; aucune relève +30 min n’était échue. TTMT moyen 1.985 s, min 1.944 s, max 2.026 s ; débit moyen 435.546 tokens/s, min 408.468, max 462.623. Comptages réels du fournisseur divisés par la durée entre premier et dernier delta SSE de réponse. Le prévol natif antérieur sans mesure SSE reste exclu des moyennes ; ses métriques TTMT/débit sont N/A.

Surcharge hors production : 984 tokens de sortie des trois sessions temporaires ; ni leur durée ni leurs tokens ne sont mélangés aux compteurs de production. Le benchmark PLLM distinct a échoué au palier 1024 faute de flux complet puis réussi à 2048 : TTFT 5.0177 s, débit global déclaré 2328.458 tokens/s (raisonnement et réponse, non comparable directement aux sondes de réponse).

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---:|---:|
| Utilisateur / mandats | 51 | 35.7 % |
| Assistant | 92 | 64.3 % |
| Total | 143 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 135 | 26.9 % |
| step-start | 92 | 18.4 % |
| reasoning | 96 | 19.2 % |
| tool | 86 | 17.2 % |
| step-finish | 92 | 18.4 % |
| Total | 501 | 100 % |

Terminaisons assistant : tool-calls 59 (64.1 %), stop 33 (35.9 %), total 92 (100 %).

| Type d’outil | Total et part | Terminés autorisés (taux) | Refus natifs (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 3 (3.5 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 27 (31.4 %) | 25 (92.6 %) | 0 (0.0 %) | 2 (7.4 %) |
| bash | 9 (10.5 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 2 (2.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 20 (23.3 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 9 (10.5 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 4 (4.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (9.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 86 (100 %) | 84 (97.7 %) | 0 (0.0 %) | 2 (2.3 %) |

## 3. Fichiers modifiés

Écritures natives tentées dans l’intervalle : 8, toutes approuvées et terminées (100 %), aucun refus natif ni erreur (0 %). Sept fichiers distincts ; tasks.md a été écrit deux fois, les coches seulement après preuves.

| Chemin absolu avant archivage | Écritures et part | Approuvées / taux | Refusées / taux | En erreur / taux |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-authority-action-v1/.openspec.yaml | 1 (12.5 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-authority-action-v1/proposal.md | 1 (12.5 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-authority-action-v1/design.md | 1 (12.5 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-authority-action-v1/tasks.md | 2 (25.0 %) | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_authority_action.py | 1 (12.5 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_authority_action.py | 1 (12.5 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_authority_action_integration.py | 1 (12.5 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| Total | 8 (100 %) | 8 (100 %) | 0 (0 %) | 0 (0 %) |

Les quatre artefacts OpenSpec ont été déplacés une seule fois vers **/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-authority-action-v1/** ; les trois fichiers Python conservent leur chemin. Les sorties __pycache__ régénérables de py_compile sont déclarées dans le manifeste, sans lecture de leur contenu. Empreintes des ports, contrats, canon Bulk et cadrages concernés inchangées. Le présent fichier /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-authority-action-v1/STATISTIQUES.md est rédigé ensuite sous mandat distinct, hors des 8 écritures mesurées.

## 4. Commandes

Neuf commandes effectivement exécutées et autorisées ; neuf outils natifs terminés (100 %). Sept exits 0 (77.8 %), deux exits 1 de diagnostic strict (22.2 %). Aucun refus natif ni erreur de transport Bash. Libellés limités à 100 caractères, troncature incluse.

| Famille / commande exécutée | Occurrences | Part |
|---|---:|---:|
| Prévol CAB — `/usr/bin/true` | 1 | 11.1 % |
| Syntaxe Python — `/home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_authority_action.py...` | 1 | 11.1 % |
| Tests et régressions — `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_auth...` | 1 | 11.1 % |
| OpenSpec ciblé strict — `/home/devops/.local/npm/bin/openspec validate add-initial-bulk-authority-action-v1 --strict` | 2 | 22.2 % |
| OpenSpec global standard — `/home/devops/.local/npm/bin/openspec validate --all` | 1 | 11.1 % |
| OpenSpec global strict — `/home/devops/.local/npm/bin/openspec validate --all --strict --json` | 2 | 22.2 % |
| Archivage OpenSpec — `/home/devops/.local/npm/bin/openspec archive add-initial-bulk-authority-action-v1 --yes --skip-specs` | 1 | 11.1 % |
| Total | 9 | 100 % |

Commandes refusées par décision CAB avant toute exécution de ces demandes :

| Commande refusée | Occurrences | Part des refus |
|---|---:|---:|
| `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_auth...` | 1 | 50.0 % |
| `/home/devops/.local/npm/bin/openspec validate --all` | 1 | 50.0 % |
| Total | 2 | 100 % |

Les réémissions ultérieures ont des identifiants et décisions neufs ; les commandes exécutées ci-dessus ne réutilisent aucune permission. Les demandes annulées ou invalides sans Bash ne sont pas comptées comme commandes exécutées.

## 5. Accès web

Dans la session de codage mesurée : zéro outil web et aucune URL visitée observée ; approuvés 0, refusés 0, erreurs 0, taux N/A (dénominateur nul). Les échanges de génération avec le fournisseur ne sont pas des visites web de l’agent.

Prévol PLLM authentifié de l’orchestrateur, distinct et hors compteurs natifs, autorisé par l’invocation :

| URL effectivement appelée | Requêtes | Part | Statut |
|---|---:|---:|---|
| https://opencode.ai/zen/go/v1/usage | 3 | 50.0 % | accès autorisé, réponses reçues |
| https://opencode.ai/zen/go/v1/models | 1 | 16.7 % | accès autorisé, réponse reçue |
| https://opencode.ai/zen/go/v1/responses | 2 | 33.3 % | accès autorisé, réponses reçues |
| Total | 6 | 100 % | 0 refus HTTP observé |

Le premier flux de benchmark était incomplet : échec de mesure distinct d’un refus HTTP. Aucune URL refusée observée. Aucun en-tête, valeur de secret ou identifiant de session fournisseur n’est publié.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début du RUN enregistré | 18/10/2026 21:07:15 UTC+2 (Europe/Paris) |
| Fin — après archivage, sonde finale et publication | 18/10/2026 21:41:07 UTC+2 (Europe/Paris) |
| Durée globale (pauses et attentes incluses) | 00 h 33 min 52 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 18/10/2026 21:07:15 UTC+2 (Europe/Paris) | 25 % | 25/10/2026 01:23:28 UTC+2 (Europe/Paris) |
| Après — après archivage de la spécification | 18/10/2026 21:41:07 UTC+2 (Europe/Paris) | 37 % | 25/10/2026 01:23:28 UTC+2 (Europe/Paris) |
| Différence après − avant | — | 12 points de pourcentage | — |

Relevés directs mcp__codex_app__get_usage_limits, quota codex, fenêtre 10080 minutes, même compte et même réinitialisation vérifiés. Horaires de consignation dans le checkpoint ; l’outil ne fournit pas l’instant interne de mesure ni un identifiant natif de relevé (N/A). Le quota est partagé : ces 12 points couvrent aussi les autres tâches simultanées ; aucune attribution exclusive à CISMP5, conversion en tokens ou coût.

| Domaine natif | Nombre / part globale | Autorisés et terminés / taux | Refus natifs / taux | Erreurs / taux |
|---|---:|---:|---:|---:|
| Fichiers, lectures et recherches | 41 (47.7 %) | 41 (100 %) | 0 (0 %) | 0 (0 %) |
| Commandes | 9 (10.5 %) | 9 (100 %) | 0 (0 %) | 0 (0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| CAB MCP et autres outils | 36 (41.9 %) | 34 (94.4 %) | 0 (0 %) | 2 (5.6 %) |
| Total | 86 (100 %) | 84 (97.7 %) | 0 (0 %) | 2 (2.3 %) |

Arrondis à une décimale ; leurs sommes peuvent différer de 100 % de 0.1 point. Attente de ressource observée 348.831 s ; détention partagée 466.140 s. Ces durées et la durée calendaire ne sont pas des temps de génération et ne s’additionnent pas. Aucun gel global de ce contexte (quatre causes : 0 s). Busy natif 722.128 s, idle 905.339 s ; aucun gain causal déduit.

Résultats : 76 tests OK (6 nouveaux, 70 régressions), trois compilations OK ; ciblé strict OK après coches ; global standard avant archive 186/186 ; strict après archive 182/184, exit 1 uniquement pour quatre warnings historiques de longueur, zéro ERROR. Archive unique vérifiée et publication durable `publish-1214581b-fe79-4c6a-94e6-8f02aa6b692f`, référence 46, phase REPORT, protections métier libérées. Rapport produit avant gate et arrêt ciblé, dont les preuves finales sont conservées au checkpoint /home/devops/datas/pixs/output/cismp/cismp5-pixs-67c71050f2dd45ce/state.json. Le cycle global reste incomplet : aucun change suivant ne sera sélectionné.

Git non inspecté, aucun commit ni push. Aucun fichier existant de production ou canon Bulk modifié par ce change. Aucun secret dans les sept contenus approuvés relus ni dans ce rapport ; l’accès PLLM est resté dans le processus sécurisé. Aucun test PostgreSQL, navigateur ou effet externe métier : sans objet pour ce vocabulaire passif. Les deux chats voisins coordonnés ont été recoupés avec leurs checkpoints et le registre avant message ; leurs objectifs et décisions restent indépendants.
