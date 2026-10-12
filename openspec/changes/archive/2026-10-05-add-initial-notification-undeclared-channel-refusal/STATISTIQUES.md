# STATISTIQUES — add-initial-notification-undeclared-channel-refusal

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-notification-undeclared-channel-refusal. RUN parent cismp-pixs-20260929-2033. Ce rapport clôt le seul change Refusal, sans terminer le RUN parent.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 FLASH / qwen3.8-flash | N/A — version exacte non exposée ; OpenCode 1.18.34 | opencode-go | xhigh observé | 2.248350 s | 87.717178 | N/A — génération isolée non mesurée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A — télémétrie absente | OpenAI | N/A — réglage non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — durées actives et chevauchements absents |

Moyennes arithmétiques sur 3 (50.0 %) tentatives de sonde valides. Les temps des messages comprennent permissions et outils ; ils ne mesurent pas le temps de service. Le compactor natif emploie le même fournisseur/modèle, avec configuration xhigh vérifiée ; sa réponse de résumé ne publie pas le champ variant, ce champ n'est pas inventé.

## 1. Statistiques générales et décisions

Intervalle réel : 2026-10-05T11:39:51.476000+00:00 → 2026-10-05T12:50:06.191458+00:00, durée **01 h 10 min 14 s**, pauses, récupération, outils, validations et archive inclus. Début = création de la collecte avant la première préparation Refusal ; la sélection exploratoire antérieure appartient au cycle parent. La publication de ce rapport est exclue de cette borne finale.

- Session ses_ef455f566ffeFkz33CHYeXiloW : 215 messages natifs accessibles avant filtrage chronologique ; aucune part de ces totaux historiques partagés n'est attribuée fictivement à Refusal.
- Session ses_ef3f47a87ffegajg8Nw2SXyqVo : 39 messages natifs accessibles avant filtrage chronologique ; aucune part de ces totaux historiques partagés n'est attribuée fictivement à Refusal.
- Session ses_ef3eb3925ffe1C7XH0RLJKU1RN : 20 messages natifs accessibles avant filtrage chronologique ; aucune part de ces totaux historiques partagés n'est attribuée fictivement à Refusal.

Les historiques des sessions de production sont filtrés depuis le début de Refusal. Les sondes dédiées sont exclues de production et détaillées séparément. Les tokens de contexte/caches sont ceux réellement facturés par OpenCode, y compris le contexte partagé ; ils ne sont pas redistribués par contenu.

| Indicateur | Nombre et part |
| --- | --- |
| Messages | 142 (100.0 %) |
| Appels outils | 68 (100.0 %) |
| Réussis | 66 (97.1 %) |
| Refus | 2 (2.9 %) |
| Erreurs | 0 (0.0 %) |
| Requêtes CAB uniques | 31 (100.0 %) |
| Appels request_validation | 31 (100.0 %) |

| Décision contrôleur observée | Nombre et part |
| --- | --- |
| approved | 31 (100.0 %) |
| Total | 31 (100.0 %) |

Les lectures autorisées ne sont pas assimilées à des décisions CAB manuelles. Toutes les éditions et commandes exécutées ont une autorisation corrélée unitaire. Deux permissions Bash hors mandat ont été refusées avant exécution ; les sessions fautives ont été interrompues, les empreintes réconciliées puis remplacées après READY et test CAB réel. Aucun effet externe ou fichier divergent observé. Les rapports agent erronés (944 au lieu de 948 tests ; durée intégration transcrite 11.264 au lieu de 11.267 secondes) ne remplacent pas les sorties natives conservées.

| Tokens production, caches inclus | Effectif et part du total |
| --- | --- |
| input | 624 (0.0 %) |
| output | 52150 (0.5 %) |
| reasoning | 0 (0.0 %) |
| cache_write | 289447 (2.6 %) |
| cache_read | 10768740 (96.9 %) |
| Total | 11110961 (100.0 %) |

Coût natif cumulé : 0.254793340. Devise N/A — unité monétaire non fournie dans les métadonnées ; aucune conversion en euros. Estimation énergétique, temps de service et temps actif root : N/A — sources absentes.

Compactions manuelles : 1 (100.0 %) achevées et vérifiées ; entrée utilisateur + réponse résumé peuvent représenter deux messages, pas deux compressions. Identifiants natifs observés : msg_10bfdfe70001ky5nKOq77wFwLH, msg_10bfdfef6001UKqnKJz5pdkh12.

- Résumé msg_10bfdfef6001UKqnKJz5pdkh12 achevé à 2026-10-05T12:17:11.301000+00:00, coût 0.030223970, tokens 145288 (1,3 % des tokens production), inclus dans la production et pas dans les sondes.

Résultats de développement : régressions complètes **948 unitaires + 202 intégration = 1150 réussis (100,0 %)** ; répartition unitaires 82.4 %, intégration 17.6 %. Ciblés : 12 unitaires (92,3 %) + 1 intégration (7,7 %) = 13 réussis (100,0 %). Compilations : 3/3 (100,0 %). OpenSpec : 6 validations strictes pré/post réussies (100,0 %), précode 3 (50,0 %), postcode 3 (50,0 %), canonical 76/0 et all 77/0 ; archivage distinct réussi, delta +0/~0/-0/→0. Les INFO préexistants de longueur de requirements ne sont pas des échecs.

Sondes de performance — texte fixe, sessions dédiées sans outils :

| Position et horodatage UTC | Session / message | Format / outils | Valide | TTMT | Débit |
| --- | --- | --- | --- | --- | --- |
| début 2026-10-05T11:39:51.961942+00:00 | ses_ef4230d01ffexb2DUmTdIbNPfk / msg_10bdcf36900142yxnfbZyWzDft | 40 lignes / 0 outils | oui | 2.312479 s | 71.957159 |
| +30 min 2026-10-05T12:10:26.485901+00:00 | ses_ef4070ee3ffevsSlY1t6yKC24i / msg_10bf8f1a3001SeoVgWMSvoGFVK | 1 lignes / 0 outils | non — exclue des moyennes | 2.406177 s | 57.994884 |
| +30 min — unique reprise immédiate 2026-10-05T12:11:57.178312+00:00 | ses_ef405ac99ffelhaF5HcoP9pQdk / msg_10bfa53bf001BRGtR45qMM3Guk | 1 lignes / 0 outils | non — exclue des moyennes | 2.162319 s | 59.997554 |
| +60 min 2026-10-05T12:40:00.070637+00:00 | ses_ef3ebfed1ffeTawVqK8nhy0J7F / msg_10c1401af001gv0IZlmTJhtUdC | 1 lignes / 0 outils | non — exclue des moyennes | 2.616458 s | 93.122613 |
| +60 min — unique reprise immédiate 2026-10-05T12:40:14.800511+00:00 | ses_ef3ebc53bffe7PMQsLco4mieW0 / msg_10c143b10001YqOwPvmisSV1SH | 40 lignes / 0 outils | oui | 1.932719 s | 102.635469 |
| fin 2026-10-05T12:49:36.155345+00:00 | ses_ef3e33487ffe03XAemFrA8ryCM / msg_10c1ccbf9001iV3Ze2Nwk8OVvZ | 40 lignes / 0 outils | oui | 2.499851 s | 88.558907 |

Tentatives : 6 (100.0 %) ; valides 3 (50.0 %) ; invalides 3 (50.0 %). Les débits affichés des essais invalides sont diagnostiques uniquement. Version exacte du modèle N/A partout, identité provider/model/variant conservée pour chaque sonde. Aucun outil natif dans ces sessions.

Cadence initiale ancrée à 2026-10-05T11:39:51.961942+00:00. +30 min : deux tentatives invalides, relève échouée, premier envoi retardé de 34.523959 s. +60 min : premier envoi à 12:40:00.070637UTC, retard 8.108695 s, première tentative invalide puis unique reprise immédiate valide. Aucune reprise supplémentaire ni sonde rétroactive. Relèves prévues avant la fin : 4/4 (100,0 %) — début, +30, +60, fin ; réussies 3/4 (75,0 %), échouées 1/4 (25,0 %), manquées 0/4 (0,0 %). Tentatives 6/6 (100,0 %) : début 1/6 (16,7 %), +30 2/6 (33,3 %), +60 2/6 (33,3 %), fin 1/6 (16,7 %). La sonde finale intervient après le dernier travail et l'archive. Toute relève ultérieure non due avant la fin n'est pas une relève manquée.

| Surcharge télémétrie distincte | Valeur |
| --- | --- |
| Durée calendaire cumulée des essais | 57.116036 s |
| Tokens total | 67264 (100.0 %) |
| Coût natif séparé | 0.010478072 — devise N/A |

| Tokens sondes | Nombre et part |
| --- | --- |
| input | 36 (0.1 %) |
| output | 3472 (5.2 %) |
| reasoning | 0 (0.0 %) |
| cache_write | 42504 (63.2 %) |
| cache_read | 21252 (31.6 %) |
| Total | 67264 (100.0 %) |

## 2. Types de messages et d'outils

| Rôle messages | Nombre et part |
| --- | --- |
| assistant | 104 (73.2 %) |
| user | 38 (26.8 %) |
| Total | 142 (100.0 %) |

| Type de partie | Nombre et part |
| --- | --- |
| compaction | 1 (0.2 %) |
| reasoning | 104 (22.3 %) |
| step-finish | 104 (22.3 %) |
| step-start | 104 (22.3 %) |
| text | 85 (18.2 %) |
| tool | 68 (14.6 %) |
| Total | 466 (100.0 %) |

| Terminaison assistant | Nombre et part |
| --- | --- |
| stop | 36 (34.6 %) |
| tool-calls | 68 (65.4 %) |
| Total | 104 (100.0 %) |

| Outil | Appels (% tous outils) | Réussis (% outil) | Refus (% outil) | Erreurs (% outil) |
| --- | --- | --- | --- | --- |
| bash | 24 (35.3 %) | 22 (91.7 %) | 2 (8.3 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 3 (4.4 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 31 (45.6 %) | 31 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (1.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 1 (1.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (11.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 68 (100.0 %) | 66 (97.1 %) | 2 (2.9 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Ces nombres comptent des tentatives natives write/edit, pas des fichiers uniques ni des accès en lecture. Les chemins restent intégraux.

| Chemin absolu complet | Tentatives (% éditions) | Réussies (% fichier) | Refus (% fichier) | Erreurs (% fichier) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-channel-refusal/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-channel-refusal/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-channel-refusal/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-channel-refusal/specs/notifications/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-channel-refusal/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/notification_channel_declaration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_notification_channel_declaration_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_notification_channel_declaration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

L'archivage a déplacé les cinq artefacts approuvés sans modifier leur contenu (5/5, 100,0 %) ; les trois sources restent à leur chemin (3/3, 100,0 %). Les 172 références de départ (100,0 %) et les 76 canonical (100,0 %) restent identiques. Le venv créé et nettoyé était régénérable, exclu des fichiers fonctionnels. Les pycache de compilation, régénérables, sont exclus. Le seul fichier directement écrit par CGPT est output/cismp-state.json, métadonnées de reprise autorisées hors décompte natif. STATISTIQUES.md sera publié après cette collecte par un mandat distinct ; sa propre édition est hors périmètre de ces chiffres.

## 4. Commandes

| Famille | Tentatives (% commandes) | Réussies | Refus | Erreurs |
| --- | --- | --- | --- | --- |
| CAB test | 2 (8.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Diagnostic hors mandat refusé | 1 (4.2 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| Nettoyage artefact régénérable | 1 (4.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (4.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec strict | 6 (25.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python syntaxe | 3 (12.5 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python tests | 5 (20.8 %) | 4 (80.0 %) | 1 (20.0 %) | 0 (0.0 %) |
| pip versions déclarées | 4 (16.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| venv temporaire | 1 (4.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 24 (100.0 %) | 22 (91.7 %) | 2 (8.3 %) | 0 (0.0 %) |

Commandes success regroupées (libellés ≤100 caractères, commande exacte disponible dans preuves natives et état non secret) :

| Libellé | Occurrences (% commandes du statut) |
| --- | --- |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 2 (9.1 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 2 (9.1 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 2 (9.1 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 TMPDIR=/home/devops… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/python/current/bin/python3 -I -B -m ve… | 1 (4.5 %) |
| /usr/bin/rm -r -- /home/devops/datas/pixs/.venv-cismp-notification-refusal-20261005 | 1 (4.5 %) |
| true | 2 (9.1 %) |

Commandes rejected regroupées (libellés ≤100 caractères, commande exacte disponible dans preuves natives et état non secret) :

| Libellé | Occurrences (% commandes du statut) |
| --- | --- |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /home/devops/python/current/bin/python3 -I -B -m un… | 1 (50.0 %) |
| ls -la /tmp/opencode/ 2>/dev/null; ls -la /tmp/ 2>/dev/null / grep -i -E "out/cap/trunc"  | 1 (50.0 %) |

Commandes error regroupées (libellés ≤100 caractères, commande exacte disponible dans preuves natives et état non secret) :

Aucune — 0 ; pourcentage N/A, dénominateur nul.

Les deux commandes refusées n'ont jamais été exécutées. L'option -I de la tentative unitaire refusée n'appartient pas à la régression exécutée dans le venv. Aucun projet.env n'a été lu, aucun SQL externe, Docker, Git commit/push ni modification des environnements existants.

## 5. Accès web

| Domaine réseau | Nombre et part / statut |
| --- | --- |
| Outils web natifs production | 0 — 0.0 % des outils |
| Bash pip accès public réellement exécutés | 2/2 (100,0 %) approuvés et réussis ; 0/2 refus (0,0 %) ; 0/2 erreurs (0,0 %) |

URL approuvée et effectivement utilisée par les deux commandes pip : https://pypi.org/simple (2/2, 100,0 % des opérations réseau attestées). Les sous-requêtes HTTP, les URL individuelles de wheels et les redirections ne sont pas mesurées : N/A, aucun nombre inventé. Aucune URL refusée. Les liens Home-page/Author de pip show sont des métadonnées affichées, pas des pages visitées. HTTP natif local OpenCode/CAB et SSE sont du transport, pas de navigation web externe. Aucun outil web de sonde.

## 6. Synthèse globale

Début : 2026-10-05T11:39:51.476000+00:00 ; fin : 2026-10-05T12:50:06.191458+00:00 ; durée calendaire : 01 h 10 min 14 s, pauses incluses. La préparation/publication du rapport est postérieure et exclue.

| Quota Codex codex /10080min | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-05T11:39:51.476837+00:00 | N/A — outil natif mcp__codex_app__get_usage_limits absent | N/A |
| Après | 2026-10-05T12:50:06.191458+00:00 | N/A — même outil absent | N/A |
| Différence après−avant | — | N/A — deux relevés natifs absents | — |

Aucun quota Spark, restant, ancien, ni fournisseur substitué. Les quotas OpenCode Go éventuellement relevés dans le cycle parent sont distincts et ne permettent pas de calculer une consommation Codex ; aucune conversion en tokens ou monnaie.

| Domaine natif | Nombre (% outils globaux) | Réussis (% domaine) | Refus (% domaine) | Erreurs (% domaine) |
| --- | --- | --- | --- | --- |
| Fichiers | 9 (13.2 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 24 (35.3 %) | 22 (91.7 %) | 2 (8.3 %) | 0 (0.0 %) |
| Web natif | 0 (0.0 %) | N/A — aucun appel | N/A — aucun appel | N/A — aucun appel |
| Autres outils | 35 (51.5 %) | 35 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Global | 68 (100.0 %) | 66 (97.1 %) | 2 (2.9 %) | 0 (0.0 %) |

1150 tests complets réussis (100,0 %), ciblés 13/13 (100,0 %), syntaxe 3/3 (100,0 %), stricts 6/6 (100,0 %). Archive réelle +0 vérifiée, fichiers exacts et canonical conservés. Aucun commit, push ou accès .git. Accès externes attestés : PyPI pour les seuls pins déjà déclarés ; aucun PostgreSQL externe. project.env demeure non lu dans ce change. Aucun secret dans le contenu des mandats, du code, des preuves ni du présent rapport ; l'autorisation PLLM de configuration sécurisée reste distincte. Les contrôles root d'intégrité ne sont pas des outils OpenCode et ne sont pas attribués au codeur.

Le helper livré est un contrôle Kernel interne de déclaration du canal. Il ne crée ni contrat de notification complet, préférence utilisateur, élargissement des destinataires, service d'envoi ou fournisseur. Les exigences restantes sont réexaminées par SPCMP ; l'archivage de ce change ne prouve pas leur implémentation.

Après la borne finale de collecte, deux tentatives de publication supplémentaires n’ont pas créé le rapport : cismp-1a10c1e7c5d-1f5f7b (ancien outil propose_approval puis poll_approval expiré et NEEDS_CLARIFICATION ; identifiant gelé) et cismp-1a10c2364ba-4b4a96 (APPROVED, mais write indisponible avant exécution car restriction d’outillage trop large ; identifiant gelé). Le contenu exact et les preuves ont été revus par CGPT. READY et un CAB test true ont été revérifiés ; les permissions natives sous CAB ont été restaurées, et les outils MCP historiques restent désactivés. Ces opérations de publication sont postérieures aux bornes des 142 messages et 68 outils ci-dessus, et exclues de leurs tokens/coûts/durée. Aucun réarchivage, aucune écriture partielle ni effet non maîtrisé.
