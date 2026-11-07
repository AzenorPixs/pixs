# STATISTIQUES — add-bulk-server-cancelled-transition-v1

RUN `cismp-pixs-01a13bab2ed7`, racine `/home/devops/datas/pixs`. Contextes CAB 155 puis 161 pour le même change. Archive `openspec/changes/archive/2026-10-15-add-bulk-server-cancelled-transition-v1`, publication effective référence 20 ; rapport distinct en phase REPORT version 179. Intervalle figé avant rédaction, après archivage et sonde finale : 2026-10-15T10:19:34.969Z → 2026-10-15 17:25:50 UTC.

Sources : exports CAB filtrés contextId 155/161 ; métadonnées natives des quatre sessions ci-dessous ; relevés natifs Codex et six sondes dédiées. Les catégories globales de l’export CAB sont volontairement exclues : elles incluent d’autres RUN. Les événements de rédaction de ce rapport sont hors intervalle. Les compteurs réussis d’outils de lecture/MCP ne sont pas assimilés à des approbations manuelles.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte du modèle non exposée ; OpenCode 1.19.0 vérifié | OpenCode Go | high pour les mandats et sondes ; variante native du résumé non exposée | 5.779068 s | 132.851916 | N/A — durées de génération complètes non isolées |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 — identité système Codex | N/A — version exacte non exposée | OpenAI | N/A — non exposé dans la télémétrie du RUN | N/A — aucune sonde orchestrateur | N/A — aucune sonde orchestrateur | N/A — aucune mesure isolant génération, outils et attentes |

Le dénominateur du temps de service cumulé est indisponible ; aucune durée calendaire, busy CAB ou attente ne lui est substituée. Des activités concurrentes existent dans CISMP2/CISMP3 et le quota de compte. Elles ne sont pas réparties arbitrairement sur ce change.

## 1. Statistiques générales et décisions

L’archive est prouvée par Bash `call_01a14096d2197149a8da99f8c9bb48dd`, native once `per_14096d4e9001L12Gs3rLVueWp2`, exit 0. Seul B06 a été synchronisé (~1 requirement, +0/-0), par deux scénarios de preuve sans nouvelle norme. Canon Bulk après synchronisation : SHA-256 `11d4d910d73f86b3d19f5c86966e599f350916a5a20a4a5e0259adf9d14cebac`.

| Résultat de développement | Réalisé / total | Taux |
|---|---:|---:|
| Compilations Python natives | 3 / 3 | 100,0 % |
| Nouveaux tests ordinaires | 3 / 3 | 100,0 % |
| Régressions locales | 45 / 45 | 100,0 % |
| Propriétés PostgreSQL réel 16.14 | 22 / 22 | 100,0 % |
| Tests combinés — processus frais par module | 1 951 / 1 951 | 100,0 % |
| Modules combinés | 245 / 245 | 100,0 % |
| Sources Python inchangées entre validations et archive | 409 / 409 | 100,0 % |
| Tâches prouvées puis cochées | 7 / 7 | 100,0 % |
| Strict ciblé final | 1 / 1 | 100,0 % |
| Global standard préarchive | 80 / 80 | 100,0 % |
| Global strict préarchive — exit natif 1 | 78 / 80 | 97,5 % |
| Global strict postarchive — exit natif 1 | 77 / 79 | 97,5 % |

Les 22 propriétés PG ne sont pas additionnées aux 48 tests ordinaires comme s’il s’agissait du même dénominateur. Tests combinés : zéro échec, zéro skip. PG : schéma privé supprimé, connexions fermées, tables publiques stables, CAS concurrent sans rebase, rollback et coopérativité prouvés. Les deux stricts globaux ne sont pas déclarés réussis : uniquement quatre WARNING historiques (bulk-operations requirements[6], [10], [13] ; identity-assurance requirements[4]), zéro ERROR. Le CLI archive a aussi signalé un avertissement non bloquant : sections proposal « Why » / « What Changes » attendues ; aucun correctif opportuniste après archive.

| Décisions CAB filtrées | Approuvées | Refusées | Clarification | Pending | Once | Total décidé |
|---|---:|---:|---:|---:|---:|---:|
| 155 | 4 (80.0 %) | 1 (20.0 %) | 0 (0.0 %) | 0 | 4 | 5 (100 %) |
| 161 | 28 (96.6 %) | 1 (3.4 %) | 0 (0.0 %) | 0 | 28 | 29 (100 %) |
| Total des deux contextes | 32 (94,1 %) | 2 (5,9 %) | 0 (0,0 %) | 0 | 32 | 34 (100 %) |

Les deux refus CAB concernent la création OpenSpec initiale (MCP -32602 avant effet) puis l’omission de commands: [] dans une demande tasks.md. Un refus natif supplémentaire concerne le Bash d’inventaire hors mandat : permission rejetée, aucun effet. Ce refus n’est pas un troisième ticket CAB. Le contexte 155 a fini BLOQUÉ/ABANDONED avant la reprise humaine approuvée et la réparation CAB ; il n’a livré aucun code. Le contexte 161 conserve les effets prouvés et leurs autorisations propres. Deux récupérations sans effet ont ensuite transféré le même job vers de nouvelles sessions, avec prévol /usr/bin/true, once, exit0 et READY0.

| Contexte CAB | Réservation observée | Busy | Idle | Inconnu natif | Exclusion | File | Stale |
|---|---:|---:|---:|---:|---:|---:|---:|
| 155 | 0 h 58 min 27 s (100 %) | 0 h 7 min 24 s (12.7 %) | 0 h 49 min 54 s (85.4 %) | 0 h 1 min 8 s (2.0 %) | 0 h 0 min 0 s (0.0 %) | 0 h 0 min 0 s (0.0 %) | 0 h 0 min 0 s (0.0 %) |
| 161 | 4 h 51 min 41 s (100 %) | 1 h 19 min 29 s (27.3 %) | 3 h 30 min 12 s (72.1 %) | 0 h 1 min 58 s (0.7 %) | 0 h 37 min 17 s (12.8 %) | 0 h 41 min 4 s (14.1 %) | 0 h 3 min 53 s (1.3 %) |

Exclusion, file et stale sont des indicateurs qui se recouvrent avec busy/idle, pas des catégories additives de génération. Les totaux CAB reposent sur l’horodatage de réception du contrôleur. Aucune reconstruction de temps manquant.

| Latence CAB request→décision | Nombre | Moyenne | Médiane | p95 |
|---|---:|---:|---:|---:|
| 155 | 5 | 119.508 s | 122.658 s | 240.436 s |
| 161 | 29 | 88.306 s | 46.329 s | 442.391 s |

La lenteur de décisions CGPT a contribué aux timeouts MCP ; aucune latence réseau n’est inférée. Les compteurs HTTP techniques sont séparés des refus : ctx155 native-validation-not-correlated=3 ; ctx161 native-validation-not-correlated=48, run-not-quiescent=2, resource-conflict=1. Total 54 tentatives HTTP techniques (100 %), dont 51 corrélation (94,4 %), 2 quiescence (3,7 %), 1 ressource (1,9 %). Ils ne représentent pas 54 effets exécutés.

Métadonnées natives : 5 511 955 tokens input, 89 474 output, 27 107 reasoning, 67 966 545 cache read, 0 cache write. Coût natif cumulé déclaré : 0.710444790 ; monnaie et débit facturé non exposés, donc N/A pour une dépense monétaire réelle. Total token univoque N/A : ne pas additionner des champs dont les conventions de recouvrement ne sont pas exposées. Les sondes sont exclues de ces compteurs de production : 63 806 tokens total natifs de sondes, dont 3 833 output, coût déclaré 0.007068226.

Un compactage OpenCode natif est observé à 14:24:47–14:25:19 UTC, résumé msg_13ff388d3001Hvpcr0QiD3Qff2 ; agent compaction configuré Muse/high, variante du message non exposée. Cycle commun incomplet : API propriétaire Codex thread/compact/start non exposée ; aucune réussite conjointe fabriquée. Échéance suivante 15:35:15 UTC non servie pendant maintenance/récupérations. Les compactages automatiques de contexte de Codex ne sont pas assimilés à cet item API.

| Sonde dédiée — même configuration high sans outil | Horodatage UTC | Output tokens | TTMT s | Génération s | Tokens/s |
|---|---|---:|---:|---:|---:|
| début | 2026-10-15T10:22:39.644695+00:00 | 638 | 6.033134 | 5.894760 | 108.231719 |
| +30 min | 2026-10-15T10:52:46.263609+00:00 | 635 | 12.124954 | 2.053883 | 309.170515 |
| reprise après maintenance CAB | 2026-10-15T12:37:17.261881+00:00 | 626 | 5.540065 | 4.560987 | 137.251005 |
| +30 min différée après RSMP C2 | 2026-10-15T13:23:06.365987+00:00 | 644 | 3.019062 | 8.423489 | 76.452882 |
| +périodique après reprise locale/compactage | 2026-10-15T14:34:03.260666+00:00 | 652 | 4.427012 | 15.877516 | 41.064358 |
| fin après archive et contrôle global | 2026-10-15T17:25:02.698544+00:00 | 638 | 3.530182 | 5.106410 | 124.941018 |

Six sondes exécutées, six valides (100 %), zéro échec (0 %). Moyenne arithmétique TTMT 5.779068 s, min 3.019062, max 12.124954 ; débit moyen 132.851916 tokens/s, min 41.064358, max 309.170515. Prompt identique 0001 à 0200, format/configuration/no-tools vérifiés, sessions jetables supprimées. Les relèves +30 min différées sont des mesures réelles retardées, pas des mesures rétroactives.

Créneaux actifs manqués : 13:35:15, 15:04:03, 15:34:03 UTC consignés ; 16:04:03, 16:34:03 et 17:04:03 UTC également non servis avant la sonde finale. Six créneaux manqués N/A, zéro mesure reconstruite. Total de collecte déclaré : 12 relèves actives prévues (100 %), 6 valides (50 %), 6 manquées (50 %), 0 échouée (0 %). La pause 11:18:02–12:35:15 UTC interrompt la collecte ; ses créneaux 11:19/11:49/12:19 ne sont pas comptés comme sondes actives. Maintenance coordonnée 15:50:00–16:11:35 UTC. Ces limites de cadence restent visibles.

## 2. Types de messages et d’outils

Sessions natives dédiées au change analysées :

- `ses_ebf6e16c5ffeRhJVV8i0N2VX2k`
- `ses_ebf817648ffeX6xVfXnzyDOkgF`
- `ses_ec070c03affe75I7f1Kdz7kJf4`
- `ses_ec0ecf55cffeC529goWbl91cU8`

| Messages natifs | Nombre | Part |
|---|---:|---:|
| user | 126 | 26.3 % |
| assistant | 354 | 73.8 % |
| Total | 480 | 100 % |

| Parties natives | Nombre | Part |
|---|---:|---:|
| text | 321 | 19.0 % |
| step-start | 354 | 21.0 % |
| reasoning | 368 | 21.8 % |
| tool | 288 | 17.1 % |
| step-finish | 354 | 21.0 % |
| compaction | 1 | 0.1 % |
| Total | 1686 | 100 % |

| Terminaisons assistant | Nombre | Part |
|---|---:|---:|
| tool-calls | 270 | 76.3 % |
| stop | 84 | 23.7 % |
| Total | 354 | 100 % |

| Type d’outil natif | Total | Part | Terminés | Refusés | Erreurs techniques |
|---|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 121 | 42.0 % | 121 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 33 | 11.5 % | 20 (60.6 %) | 0 (0.0 %) | 13 (39.4 %) |
| bash | 24 | 8.3 % | 23 (95.8 %) | 1 (4.2 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 45 | 15.6 % | 45 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 2.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 4 | 1.4 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 5 | 1.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 24 | 8.3 % | 9 (37.5 %) | 0 (0.0 %) | 15 (62.5 %) |
| glob | 4 | 1.4 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 19 | 6.6 % | 17 (89.5 %) | 0 (0.0 %) | 2 (10.5 %) |
| grep | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 288 | 100 % | 257 (89.2 %) | 1 (0.3 %) | 30 (10.4 %) |

Les 257 outils terminés (89,2 %) ne sont pas 257 permissions manuelles. Les 30 erreurs techniques (10,4 %) comprennent 13 request_validation, 15 poll_approval et 2 read ; le Bash refusé (0,3 %) est distingué. Deux commandes strictes terminées avec exit1 sont des validations non réussies, sans erreur de transport native. Le périmètre CAB agrégé contient 277 appels, le snapshot natif 288 : périmètres de collecte distincts, notamment prévols avant rattachement. Les quatre sessions natives totalisent 23 Bash terminés +8 write terminés =31 effets natifs once documentés ; un prévol de candidate du contexte155 supplémentaire, call_01a13f3d13a17735998ff23a8305446d /usr/bin/true exit0, est prouvé dans l’historique mais hors des quatre sessions listées. Les 32 once CAB ne sont donc pas réduits arbitrairement à31. La couverture détaillée des autres outils de cette candidate reste N/A.

## 3. Fichiers modifiés

Ce tableau compte les tentatives write natives avant rapport. Un fichier écrit deux fois compte deux tentatives ; les refus CAB avant write sont séparés.

| Chemin absolu | Tentatives | Part des 8 | Approuvées et terminées | Refusées natives | Erreur native |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-cancelled-transition-v1/tasks.md | 2 | 25.0 % | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-cancelled-transition-v1/proposal.md | 1 | 12.5 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-cancelled-transition-v1/design.md | 1 | 12.5 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-cancelled-transition-v1/specs/bulk-operations/spec.md | 1 | 12.5 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_server_cancelled_transition.py | 1 | 12.5 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_server_cancelled_transition.py | 1 | 12.5 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_server_cancelled_transition_postgres_integration.py | 1 | 12.5 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| Total — 7 chemins distincts | 8 | 100 % | 8 (100 %) | 0 (0 %) | 0 (0 %) |

La demande tasks.md refusée avant write n’est pas une neuvième tentative native. Le CLI new a créé .openspec.yaml ; le CLI archive a déplacé les cinq artefacts vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancelled-transition-v1` et synchronisé `/home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md`. Ce sont les effets de commandes distinctes, pas des write supplémentaires inventés. Le présent STATISTIQUES.md est une écriture ultérieure distincte hors intervalle. Aucun fichier source Python existant n’a été modifié : trois nouveaux fichiers source/test. Les empreintes des 409 Python ont été revérifiées. DEVOPS.md a subi seulement des actualisations externes de son horodatage d’inventaire ; comparaison normalisée intégrale et filiation des SHA consignées, aucune écriture C1 de ce fichier.

La maintenance CAB approuvée séparément a touché le job-context et son test recovery dans le projet CAB, hors fichiers Pixs de ce tableau. Syntaxe/recovery36/36 puis maintenance C3 séparée81/81 et strict1/1 : preuves techniques distinctes, pas tests fonctionnels Pixs. Suite CAB globale150 :148passed,1failed préexistant documentaire reproduit sur ancien code,1skip opt-in ; aucun « tout passe » fabriqué.

## 4. Commandes

| Famille native | Total | Part | Terminées | Refusées | Erreurs techniques |
|---|---:|---:|---:|---:|---:|
| Prévol /usr/bin/true | 6 | 25.0 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 9 | 37,5 % | 9 (100 %) | 0 (0 %) | 0 (0 %) |
| Inventaire hors mandat | 1 | 4,2 % | 0 (0 %) | 1 (100 %) | 0 (0 %) |
| Tests Python | 5 | 20.8 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 12.5 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 24 | 100 % | 23 (95.8 %) | 1 (4.2 %) | 0 (0 %) |

| Libellé natif limité à 100 caractères | Occurrences | Part des Bash | Résultat |
|---|---:|---:|---|
| /usr/bin/true | 6 | 25.0 % | exit 0, exit 0, exit 0, exit 0, exit 0, exit 0 |
| /home/devops/.local/npm/bin/openspec validate add-bulk-server-cancelled-transition-v1 --strict --js… | 2 | 8.3 % | exit 0, exit 0 |
| /home/devops/.local/npm/bin/openspec archive add-bulk-server-cancelled-transition-v1 --yes | 1 | 4.2 % | exit 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 | 8.3 % | exit 1, exit 1 |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 /home/devop… | 1 | 4.2 % | exit 0 |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 4.2 % | exit 0 |
| /home/devops/.local/npm/bin/openspec --version | 1 | 4.2 % | exit 0 |
| /home/devops/.local/npm/bin/openspec new change add-bulk-server-cancelled-transition-v1 | 1 | 4.2 % | exit 0 |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/backend/bulk_server_cancelled_transi… | 1 | 4.2 % | exit 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_bulk_server_cancelled_transit… | 1 | 4.2 % | exit 0 |
| /usr/bin/env PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 /home/devops/python/c… | 1 | 4.2 % | exit 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_bulk_server_cancelled_… | 1 | 4.2 % | exit 0 |
| /usr/bin/env PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 /hom… | 1 | 4.2 % | exit 0 |
| /usr/bin/env PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 /hom… | 1 | 4.2 % | exit 0 |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 /home/devop… | 1 | 4.2 % | exit 0 |
| ls -R openspec/changes/add-bulk-server-cancelled-transition-v1 2>&1; echo ---; ls -l src/pixs/backe… | 1 | 4.2 % | refus avant effet |
| /home/devops/.local/npm/bin/openspec validate bulk-operations --json | 1 | 4.2 % | exit 0 |

Commandes refusées regroupées : inventaire ls groupé hors mandat, une occurrence native (4,2 % des24Bash), aucune exécution ; création OpenSpec initiale refusée au niveau CAB avant Bash, une demande (2,9 % des34décisions). La création a ensuite réussi sous une nouvelle autorisation après récupération, sans rejeu d’effet déjà produit. Les commandes tronquées sont des libellés, pas des instructions à réexécuter. Aucun Git.

## 5. Accès web

| Web natif des quatre sessions | Total | Part | Approuvé | Refusé | Erreur |
|---|---:|---:|---:|---:|---:|
| Outils webfetch/websearch/browser observés | 0 | N/A — total nul | 0 / N/A | 0 / N/A | 0 / N/A |

Aucune URL visitée ou refusée par un outil web natif n’est observée dans ce périmètre. Aucun accès web n’est déduit d’un simple texte. La vérification sécurisée PLLM utilise séparément le fournisseur Go (quotas puis benchmark high) et les tests PostgreSQL utilisent le service de test autorisé : ces accès réseau ne sont pas des outils web natifs et n’en gonflent pas le tableau. URL, compteurs d’octets et durée réseau spécifiques N/A — non collectés. Les secrets n’ont été employés que par les processus sécurisés autorisés, jamais transmis au modèle ou au rapport. Aucun accès navigateur fonctionnel requis pour cette façade interne.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-15T10:19:34.969Z |
| Fin — après archivage et sonde finale | 2026-10-15 17:25:50 UTC |
| Durée globale (pauses et attentes incluses) | 7 h 6 min 15 s |

La période inclut le contexte initial bloqué, la maintenance, la reprise et les attentes ; aucune addition des temps concurrents. Le relevé quota initial précède le début technique de collecte de sept minutes environ ; la variation du quota porte exactement sur ses deux relevés.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-15T10:12:09.697Z | 5 % | 2026-10-22T06:12:56.000Z |
| Après — après archivage de la spécification et sonde finale | 2026-10-15 17:25:50 UTC | 15 % | 2026-10-22T06:12:56.000Z |
| Différence après − avant | — | 10 points de pourcentage | — |

Outil natif mcp__codex_app__get_usage_limits, quota codex, fenêtre10080min. Même compte et même reset vérifiés sans publier son identité. Quota partagé : ces10points peuvent inclure les autres tâches simultanées, sans attribution exclusive à CISMP1 ni conversion en tokens/euros.

| Domaine natif | Total | Part globale | Terminés | Refusés | Erreurs techniques |
|---|---:|---:|---:|---:|---:|
| Fichiers write | 8 | 2.8 % | 8 (100 %) | 0 (0 %) | 0 (0 %) |
| Commandes Bash | 24 | 8.3 % | 23 (95.8 %) | 1 (4.2 %) | 0 (0 %) |
| Web natif | 0 | 0,0 % | 0 / N/A | 0 / N/A | 0 / N/A |
| Autres outils — lecture/MCP | 256 | 88.9 % | 226 (88.3 %) | 0 (0 %) | 30 (11.7 %) |
| Total global | 288 | 100 % | 257 (89.2 %) | 1 (0.3 %) | 30 (10.4 %) |

Totaux croisés :8+24+0+256=288,257+1+30=288. Un outil terminé ne prouve pas à lui seul une approbation manuelle ; les32once et34décisionsCAB ont leur propre tableau. Rapport produit après gel, sous mandat distinct ; sa propre écriture, son gate et sa libération restent à prouver hors intervalle, sans résultat anticipé.

Livraison fonctionnelle : façade interne de transition CANCELLED et deux fichiers de tests ; tests1951/1951,PG22/22,archive native0 et référence20 prouvés. Strict global reste exit1 avec quatre warnings historiques, zéroERROR. Git non inspecté/non modifié. Pas de worker, HTTP, provider production, migration, dépendance ou nouvelle priorité d’expiration. Secrets absents des sources, prompts, état et présent rapport selon les opérations observées. La clôture individuelle ne vaut pas fin globale du parent CISMP, qui revient à SÉLECTION après gate/désarmement/release prouvés.
