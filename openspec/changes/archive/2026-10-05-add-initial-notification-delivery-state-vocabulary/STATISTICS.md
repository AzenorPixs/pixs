# STATISTIQUES — add-initial-notification-delivery-state-vocabulary

Archive : `/home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-notification-delivery-state-vocabulary`. RUN parent `cismp-pixs-20260929-2033`, CISMP mode persistant. Rapport de ce seul change ; sa clôture ne termine pas le cycle parent.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 FLASH / qwen3.8-flash | N/A — version exacte du modèle non exposée ; agent OpenCode 1.18.34 | opencode-go | xhigh observé | 2.199145 s | 80.018185 | N/A — temps de génération isolé non fourni |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A — aucune télémétrie de version | OpenAI | N/A — pas de télémétrie d'effort | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — durée active non exposée |

Les moyennes du codeur reposent uniquement sur les trois sondes valides. Les durées de messages OpenCode incluent outils et permissions : elles ne servent pas à estimer le temps de service. Le dénominateur cumulé des durées actives des agents et leurs chevauchements sont indisponibles ; toutes les parts de service restent N/A.

## 1. Statistiques générales et décisions

Intervalle : 2026-10-05T10:21:04.781000+00:00 → 2026-10-05T11:24:25.902945+00:00, soit **01 h 03 min 21 s**, pauses, récupération, outils, tests et archivage inclus. Début prouvé par le message natif `msg_10b94d18d0013MWlf1Nf5lLUAF` ; initialisation de collecte non secrète à 2026-10-05T10:22:05.982574+00:00. La rédaction et publication du présent rapport sont hors de cet intervalle.

Historiques maîtres complets :
- `ses_ef4a0eddaffelV674mXhFIX6x1` : 155 messages accessibles avant filtrage (historique de session partagé ; parts entre sessions non interprétées comme part du travail).
- `ses_ef455f566ffeFkz33CHYeXiloW` : 116 messages accessibles avant filtrage (historique de session partagé ; parts entre sessions non interprétées comme part du travail).

Les 7 messages de correction du rapport NotificationChannel, reliés à deux parents identifiés, sont exclus par leur parentID. Les anciennes interventions antérieures à la sélection Delivery et les sessions de sondes sont également exclues des statistiques de production. Les frais de contexte conservé par la session réutilisée restent ceux réellement rapportés par OpenCode : aucune attribution fictive de leur contenu entre changes.

| Indicateur | Valeur |
| --- | --- |
| Messages de production | 151 (100.0 %) |
| Appels d'outils de production | 91 (100.0 %) |
| Appels réussis | 88 (96.7 %) |
| Refus explicites | 0 (0.0 %) |
| Erreurs techniques | 3 (3.3 %) |
| Compactions natives observées | 0 (0.0 %) |
| Requêtes CAB uniques | 31 (100.0 %) |
| Requêtes CAB effectuées | 31 (100.0 %) |

Convention : « réussi / approuvé et exécuté » désigne un appel terminé sans refus ni erreur ; pour les lectures permises, cela ne prouve pas une décision CAB manuelle. Chaque écriture et chaque Bash exécutés possèdent leur mandat CAB unitaire corrélé. Un refus de permission serait distinct d'une erreur technique et d'un test en échec.

| Décisions contrôleur observées | Nombre et part |
| --- | --- |
| approved | 31 (100.0 %) |
| Total | 31 (100.0 %) |

30 des 31 décisions approuvées couvrent 30 opérations natives réellement exécutées (9 éditions et 21 commandes), soit 96.8 % des décisions ; la décision résiduelle (3.2 %) est inutilisée. Pour `cismp-1a10ba45099-b891e3`, une approbation existait avant la tentative de publication root, qui a reçu HTTP 400 : son auteur effectif n'est pas attesté. L'appel MCP avait expiré, aucune commande n'a été exécutée sous cette décision et l'identifiant a été gelé. Ne pas la présenter comme une décision émise par cet orchestrateur.

Les trois erreurs techniques conservées : expiration MCP du mandat non prescrit, interrogation avec un approval_id erroné ensuite corrigé, lecture d'un nom de test inexistant ensuite remplacée par le fichier réel. La session fautive a été interrompue ; 163 références et les cinq artefacts ont été réconciliés avant une nouvelle session, broker READY et CABtest réel `/usr/bin/true` exit 0. Aucun effet hors périmètre constaté.

| Télémétrie tokens production | Nombre et part du total |
| --- | --- |
| input | 684 (0.0 %) |
| output | 47724 (0.4 %) |
| reasoning | 0 (0.0 %) |
| cache_write | 196257 (1.8 %) |
| cache_read | 10953700 (97.8 %) |
| Total | 11198365 (100.0 %) |

Coût natif agrégé : 0.237043480, unité monétaire non exposée par cette API (N/A ; aucune conversion en euros). Zéro token reasoning dans la télémétrie ne change pas le réglage xhigh effectivement observé.

Télémétrie textuelle : prompt constant, sessions dédiées tous outils interdits, aucune lecture/écriture ou outil dans les sondes. TTMT issu du premier événement textuel SSE assistant après émission ; débit = tokens de sortie natifs / intervalle entre premier et dernier événement assistant. Le prompt est le même pour les quatre tentatives :

> Sonde de télémétrie textuelle. Aucun outil, fichier, réseau ni raisonnement explicatif. Sans introduction ni conclusion, écris exactement 40 lignes. Chaque ligne contient : alpha beta gamma delta epsilon zeta eta theta iota kappa. Répète cette ligne identique 40 fois.

| Relève / tentative | Envoi UTC | Session | Premier événement UTC | Dernier événement UTC | Tokens sortie | TTMT | Tokens/s | Résultat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| initiale_delivery_preparation_20261005 | 2026-10-05T10:23:14.511502+00:00 | ses_ef46933c7ffe3t3Xx2Zq9I3PZF | 2026-10-05T10:23:16.734143+00:00 | 2026-10-05T10:23:17.680061+00:00 | 57 | Exclu — sonde invalide | Exclu — sonde invalide | Échec : 1 ligne au lieu de 40 |
| initiale_delivery_unique_retry_20261005 | 2026-10-05T10:23:48.857799+00:00 | ses_ef468ad94ffemXeOxYAeYPOkqS | 2026-10-05T10:23:50.959655+00:00 | 2026-10-05T10:23:57.469899+00:00 | 615 | 2.101856 s | 94.466504 | Valide |
| +30min_delivery_20261005 | 2026-10-05T10:54:12.199996+00:00 | ses_ef44cdb2bffe3BnzAveDeBU9am | 2026-10-05T10:54:14.472787+00:00 | 2026-10-05T10:54:22.111773+00:00 | 535 | 2.272791 s | 70.035472 | Valide |
| fin | 2026-10-05T11:22:04.732260+00:00 | ses_ef43355d8ffeXRqG32y6ROsEI7 | 2026-10-05T11:22:06.955049+00:00 | 2026-10-05T11:22:23.195395+00:00 | 1227 | 2.222788 s | 75.552578 | Valide |

Toutes les tentatives : opencode-go / qwen3.8-flash / xhigh ; version modèle exacte N/A. Trois relèves prévues et réussies (début, +30 min, fin), soit 3/3 (100 %) ; zéro relève finalement échouée (0 %), zéro manquée (0 %). Quatre tentatives : 3 valides (75 %), 1 invalide (25 %), unique reprise immédiate du début conservée. La relève +30 min est effectuée 23,342 s après son échéance calculée depuis la reprise initiale ; retard signalé, aucune relève recréée rétroactivement. L'activité de codage et l'archivage se terminent avant l'échéance suivante 11:24:12, donc aucune relève +60 min n'est due.

TTMT valides : moyenne 2.199145 s, minimum 2.101856, maximum 2.272791. Débit valides : moyenne arithmétique 80.018185 tokens/s, minimum 70.035472, maximum 94.466504.

| Surcharge sondes séparée | Valeur et part |
| --- | --- |
| input | 24 (0.1 %) |
| output | 2434 (5.4 %) |
| reasoning | 0 (0.0 %) |
| cache_write | 31878 (70.9 %) |
| cache_read | 10626 (23.6 %) |
| Total | 44962 (100.0 %) |

Durée mesurable des sondes cumulée (envoi → dernier événement) : 40.155571 s ; coût natif 0.007693196, devise N/A. Hors chiffres de production. Total alloué aux sondes : 4 tentatives (100 %).

Résultats du développement : six états lexicaux canoniques, sans machine à états ni effet à l'import. Compilations : 3/3 (100 %) ; tests ciblés : 4/4 (100 %), dont 3 unitaires et 1 intégration ; régression : 1137/1137 (100 %), dont 936 unitaires (82,3 %) et 201 intégrations (17,7 %). Stricts pré-code puis post-code : 6/6 invocations réussies (100 %) ; à chaque phase change valide, specs 76/76 (100 %) et all 77/77 (100 %).

## 2. Types de messages et d'outils

| Rôle | Nombre et part |
| --- | --- |
| assistant | 114 (75.5 %) |
| user | 37 (24.5 %) |
| Total | 151 (100.0 %) |

| Type de partie | Nombre et part |
| --- | --- |
| reasoning | 114 (21.2 %) |
| step-finish | 114 (21.2 %) |
| step-start | 114 (21.2 %) |
| text | 105 (19.5 %) |
| tool | 91 (16.9 %) |
| Total | 538 (100.0 %) |

| Fin de réponse assistant | Nombre et part |
| --- | --- |
| stop | 37 (32.5 %) |
| tool-calls | 77 (67.5 %) |
| Total | 114 (100.0 %) |

| Outil | Total / part des appels | Réussi / taux ligne | Refusé / taux ligne | Erreur / taux ligne |
| --- | --- | --- | --- | --- |
| bash | 21 (23.1 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 3 (3.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 3 (3.3 %) | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| cgpt-validation_request_validation | 31 (34.1 %) | 30 (96.8 %) | 0 (0.0 %) | 1 (3.2 %) |
| edit | 1 (1.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 5 (5.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 19 (20.9 %) | 18 (94.7 %) | 0 (0.0 %) | 1 (5.3 %) |
| write | 8 (8.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 91 (100.0 %) | 88 (96.7 %) | 0 (0.0 %) | 3 (3.3 %) |

Les 114 parties reasoning sont des parties de message, et non un nombre de tokens de raisonnement. La ligne request_validation compte le timeout MCP comme erreur, indépendamment de la décision ultérieure inutilisée du contrôleur.

## 3. Fichiers modifiés

Les chiffres ci-dessous comptent les tentatives natives d'édition, et non toutes les écritures internes d'un outil ou du runtime. Création de venv, pip, nettoyage et archivage relèvent des commandes. Les fichiers temporaires de tests sont régénérables et nettoyés.

| Chemin absolu complet de la tentative | Total / part des éditions | Approuvée exécutée / taux ligne | Refusée / taux ligne | Erreur / taux ligne |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-delivery-state-vocabulary/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-delivery-state-vocabulary/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-delivery-state-vocabulary/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-delivery-state-vocabulary/specs/notifications/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-delivery-state-vocabulary/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/notification_delivery.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_notification_delivery_state_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_notification_delivery_state.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 créations (88,9 %) et 1 modification de tasks.md (11,1 %) : 9 éditions (100 %). L'archive déplace les cinq artefacts du change vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-notification-delivery-state-vocabulary`, empreintes préservées (5/5, 100 %). Les 76 spécifications canoniques (100 %) et les 163 références de périmètre (100 %) restent identiques. Les trois nouvelles sources correspondent exactement au NFDOC revu, UTF-8/LF ; l'environnement `.venv-cismp-delivery-20261005` a été supprimé et son absence contrôlée.

Le présent STATISTIQUES.md est publié après la borne finale : son mandat d'édition distinct et sa vérification ne sont pas inclus dans ces 9 tentatives afin de conserver des bornes stables.

## 4. Commandes

| Famille | Total / part commandes | Réussie / taux ligne | Refusée / taux ligne | Erreur / taux ligne |
| --- | --- | --- | --- | --- |
| CABtest inoffensif | 1 (4.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Nettoyage temporaire | 1 (4.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archivage | 1 (4.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec stricts | 6 (28.6 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python environnement temporaire | 1 (4.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python syntaxe | 3 (14.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python tests | 4 (19.0 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| pip déclaré : résolution, installation et diagnostics | 4 (19.0 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 21 (100.0 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Toutes les commandes Bash sont exécutées une seule fois par mandat, sans chaîne de commandes, avec executable absolu déclaré. Les 21 résultats natifs donnent exit 0 (100 %). Les libellés d'inventaire suivants sont des résumés limités à 100 caractères ; les commandes exactes et identifiants restent dans l'état de reprise.

| Libellé de commande ≤100 caractères | Occurrences et part |
| --- | --- |
| openspec validate add-initial-notification-delivery-state-vocabulary --strict | 2 (9.5 %) |
| /usr/bin/true | 1 (4.8 %) |
| openspec validate --specs --strict | 2 (9.5 %) |
| openspec validate --all --strict | 2 (9.5 %) |
| python3 -m py_compile src/pixs/kernel/notification_delivery.py | 1 (4.8 %) |
| python3 -m py_compile tests/unit/test_notification_delivery_state.py | 1 (4.8 %) |
| python3 -m py_compile tests/integration/test_notification_delivery_state_integration.py | 1 (4.8 %) |
| python -m unittest discover -s tests/unit -p test_notification_delivery_state.py -q | 1 (4.8 %) |
| python -m unittest discover -s tests/integration -p test_notification_delivery_state_integration.py… | 1 (4.8 %) |
| python3 -I -B -m venv --without-pip <venv Delivery neuf> | 1 (4.8 %) |
| pip3 --python <venv Delivery> install --dry-run --only-binary=:all: --no-input --disable-pip-versio… | 1 (4.8 %) |
| pip3 --python <venv Delivery> install --only-binary=:all: --no-input --disable-pip-version-check --… | 1 (4.8 %) |
| pip3 --python <venv Delivery> show Django psycopg psycopg-binary asgiref sqlparse | 1 (4.8 %) |
| pip3 --python <venv Delivery> check | 1 (4.8 %) |
| python -m unittest discover -s tests/unit -q | 1 (4.8 %) |
| python -m unittest discover -s tests/integration -q | 1 (4.8 %) |
| rm -r -- /home/devops/datas/pixs/.venv-cismp-delivery-20261005 | 1 (4.8 %) |
| openspec archive add-initial-notification-delivery-state-vocabulary --yes | 1 (4.8 %) |
| Total | 21 (100.0 %) |

Commandes refusées : aucune (0/21, 0 %). Le mandat MCP expiré n'a jamais produit de Bash et n'est pas compté comme commande exécutée. Les deux invocations pip en réseau (résolution puis installation) sont autorisées et confinées au temporaire ; diagnostics show/check sans accès réseau demandé.

## 5. Accès web

| Appels d'outil web natif du codeur | Nombre et part / taux |
| --- | --- |
| Approuvés et exécutés | 0 — N/A, dénominateur nul |
| Refusés | 0 — N/A, dénominateur nul |
| Erreurs | 0 — N/A, dénominateur nul |
| Total | 0 — N/A, dénominateur nul |

Aucun outil web du codeur : ce zéro ne signifie pas absence de réseau. Deux commandes pip approuvées accèdent à PyPI public. Les sorties observées prouvent la résolution des métadonnées et le téléchargement des cinq wheels ; aucun secret, keyring, netrc ou index privé n'est utilisé. Les URL exactes des wheels ne sont pas exposées dans les sorties, N/A sans reconstruction.

| Accès externe autorisé observé | Statut | Opérations et part des 3 accès connus |
| --- | --- | --- |
| https://pypi.org/simple | Approuvé, effectivement utilisé par pip public | 2 (66,7 %) |
| https://opencode.ai/zen/go/v1/usage | Approuvé, relevé PLLM par processus opaque de l'orchestrateur | 1 (33,3 %) |
| Total | 3 réussis (100 %), 0 refus (0 %), 0 erreur (0 %) | 3 (100 %) |

Relevé PLLM observé à 10:51:24 UTC : rolling 6 %, weekly 11 %, monthly 25 %, statut OK. Ces quotas OpenCode Go sont distincts du quota Codex et ne lui sont jamais substitués. Aucun outil web de l'orchestrateur n'est utilisé dans l'intervalle Delivery ; les vérifications primaires du cycle précédent restent hors de ce bilan. URL refusées : aucune connue ; aucune URL de wheel inventée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-05T10:21:04.781000+00:00 |
| Fin — après archivage | 2026-10-05T11:24:25.902945+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 03 min 21 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil absent dès préparation | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-05T11:24:25.902945+00:00 (inventaire d'outils, pas un relevé) | N/A — outil natif absent | N/A |
| Différence après − avant | — | N/A — aucun couple natif comparable | — |

L'outil natif mcp__codex_app__get_usage_limits n'est pas exposé : aucun relevé ni appel prétendu, aucune ancienne valeur ou quota fournisseur de substitution. Les quotas Codex seraient partagés par le compte ; aucune exclusivité de consommation n'est vérifiée.

| Domaine | Total / part globale | Approuvé exécuté / taux ligne | Refusé / taux ligne | Erreur / taux ligne |
| --- | --- | --- | --- | --- |
| Fichiers | 9 (9.9 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 21 (23.1 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web natif | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 61 (67.0 %) | 58 (95.1 %) | 0 (0.0 %) | 3 (4.9 %) |
| Total général | 91 (100.0 %) | 88 (96.7 %) | 0 (0.0 %) | 3 (3.3 %) |

Les accès réseau encapsulés dans Bash restent comptés dans Commandes et ne sont pas doublés dans Web natif. Les trois accès connus sont détaillés séparément en section 5. Les métriques des sondes sont une surcharge distincte, hors total général.

Bilan : 6/6 tâches prouvées puis cochées (100 %), 3/3 compilations (100 %), 4/4 tests ciblés (100 %), 1137/1137 tests complets (100 %), 6/6 stricts pré/post (100 %), 1/1 archivage réussi (100 %), delta normatif +0/~0/-0/→0, cinq artefacts archivés intacts (100 %), 76/76 spécifications canoniques et 163/163 références intactes (100 %). Trois erreurs techniques visibles et résolues ; aucun refus, aucune commande non autorisée exécutée. Aucun changement de version, cadrage ou dépendance déclarée.

Git : aucun état Git inspecté, aucun commit, push ou modification de configuration Git effectué dans ce change. PostgreSQL externe : aucune opération nécessaire, aucun chargement de project.env. Secrets : aucun secret lu par le modèle, affiché ou copié ; l'autorisation PLLM durable est exercée exclusivement par le processus sécurisé de quota, hors télémétrie des modèles. Aucun environnement préexistant modifié.

Le change Delivery est archivé ; la conformité du rapport reste à vérifier après son écriture distincte. Le cycle CISMP parent conserve son gate OPEN et revient à SÉLECTION après cette preuve, sans annoncer une fin globale.
