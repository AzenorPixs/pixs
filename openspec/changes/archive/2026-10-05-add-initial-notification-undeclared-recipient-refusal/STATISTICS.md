# STATISTIQUES — add-initial-notification-undeclared-recipient-refusal

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-notification-undeclared-recipient-refusal. Le seul change est clôturé ; le RUN parent demeure ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 FLASH / qwen3.8-flash | N/A — version exacte non exposée ; OpenCode 1.18.34 | opencode-go | xhigh observé | N/A — aucune sonde valide | N/A — aucune sonde valide | N/A — génération isolée non mesurée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A — télémétrie absente | OpenAI | N/A — effort non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — durée active/chevauchements absents |

Les moyennes utilisent uniquement les sondes valides. Les durées des messages incluent outils et permissions ; elles ne mesurent pas le temps de service des agents.

## 1. Statistiques générales et décisions

Début 2026-10-05T13:22:54.380000+00:00 ; fin 2026-10-05T14:25:32.543111+00:00 ; durée calendaire **01h02m38s**, pauses, récupération, outils, tests, sondes et archive inclus. Collecte initialisée avant la première préparation de ce change. Sélection antérieure et publication de ce rapport exclues des bornes.

- Session ses_ef3d756c4ffe3unJqDQg1sYjoh : 42 messages accessibles avant filtrage chronologique ; contexte partagé, aucune attribution fictive des messages antérieurs.
- Session ses_ef3b65eceffeIJ6Js7E3ySjcmY : 58 messages accessibles avant filtrage chronologique ; contexte partagé, aucune attribution fictive des messages antérieurs.
- Session ses_ef398ce55ffeqQ8Vqa53fWKHmD : 66 messages accessibles avant filtrage chronologique ; contexte partagé, aucune attribution fictive des messages antérieurs.

| Indicateur | Effectif et part |
| --- | --- |
| Messages | 142 (100.0 %) |
| Outils | 73 (100.0 %) |
| Réussis | 70 (95.9 %) |
| Refus | 1 (1.4 %) |
| Erreurs | 2 (2.7 %) |
| Requêtes CAB | 33 (100.0 %) |
| Identifiants CAB uniques | 33 (100.0 %) |
| Messages de compaction | 0 (0.0 %) |

| Décision contrôleur | Nombre et part |
| --- | --- |
| approved | 32 (100.0 %) |
| Total | 32 (100.0 %) |

Les lectures permises ne prouvent pas une décision CAB manuelle. Chaque édition/Bash réellement exécutés ont une approbation unitaire corrélée. Le mandat cismp-1a10c471812-a6a665 a expiré côté MCP : APPROVED côté contrôleur, mais non reçu et non exécuté par le codeur. Identifiant gelé, première session interrompue et archivée ; baseline181 et trois artefacts réconciliés, nouvelle SID READY puis CABtest true ; seul premier jalon restant repris. Une tentative Bash true hors mandat a été refusée avant exécution (per_10c6546c3001cV4bpQ2ZDP0PKA), puis session interrompue/archivée et nouvelle session READY avec CABtest réussi. Un CABtest distinct a échoué sur paramètre files omis par le codeur (MCP -32602), sans décision ni Bash ; nouveau RID complet réussi. Aucun effet hors mandat observé.

| Tokens production, caches inclus | Effectif et part |
| --- | --- |
| input | 630 (0.0 %) |
| output | 62688 (1.2 %) |
| reasoning | 0 (0.0 %) |
| cache_write | 237152 (4.7 %) |
| cache_read | 4717938 (94.0 %) |
| Total | 5018408 (100.0 %) |

Coût natif cumulé 0.152475268 ; devise N/A — unité non fournie, aucune conversion en euros. Les tokens de caches reflètent le contexte de session réellement facturé ; leur contenu n'est pas redistribué entre changes.

Sondes dédiées — texte fixe, aucun outil/fichier/réseau :

| Position / envoi UTC | Session / message | Lignes/outils | Valide | TTMT s | Tokens/s |
| --- | --- | --- | --- | --- | --- |
| début 2026-10-05T13:22:54.960783+00:00 | ses_ef3c4b4feffeDbvGSEzjMpiNeS / msg_10c3b4c6a001A6E6lKgdWV0ngc | 1/0 | non — exclue | 2.989282 | 63.109210 |
| début — unique reprise immédiate 2026-10-05T13:23:42.244587+00:00 | ses_ef3c3fbeeffeIWJ29Edli7u57k / msg_10c3c046a001r9Cd7HxPJvWDzD | 9/0 | non — exclue | 1.395424 | 85.311178 |
| +30 min 2026-10-05T13:53:12.442603+00:00 | ses_ef3a8f937ffeZbwaaxycKCyqRz / msg_10c570790001xnRZLPT8vl6ZmK | 1/0 | non — exclue | 3.232365 | 53.982098 |
| +30 min — unique reprise immédiate 2026-10-05T14:00:29.849905+00:00 | ses_ef3a24c8dffeF0oGvglVnO3i4g / msg_10c5db463001eh3pEs6J1Mel1n | 1/0 | non — exclue | 3.356685 | 68.762681 |
| +60 min 2026-10-05T14:23:03.731009+00:00 | ses_ef38da3e5ffePHoqUvq4w4e3Yy / msg_10c725c77001YwvkvhK2cUwewl | 40/0 | non — exclue | 2.079873 | 81.054829 |
| +60 min — unique reprise immédiate 2026-10-05T14:23:23.766203+00:00 | ses_ef38d5597ffe6ZOoLpe2AwrGne / msg_10c72aab4001oVoHMmXbSWqY9T | 1/0 | non — exclue | 2.612639 | 56.399431 |
| fin 2026-10-05T14:24:53.895562+00:00 | ses_ef38bf58cffeh24HqurwiZDpLv / msg_10c740ad8001AXXL0jHNvgnr0h | 1/0 | non — exclue | 2.606863 | 33.569755 |
| fin — unique reprise immédiate 2026-10-05T14:25:14.308200+00:00 | ses_ef38ba5cfffe9tXy4OpKwzV7Xo / msg_10c745a8a001XvdqCNY21slplQ | 1/0 | non — exclue | 2.135251 | 56.864666 |

Tentatives 8 (100.0 %), valides 0 (0.0 %), invalides 8 (100.0 %). Relèves réalisées 4 (100.0 %), réussies 0 (0.0 %), échouées 4 (100.0 %). Chaque position a au plus une reprise ; aucune mesure recréée rétroactivement. La reprise de +30 a été retardée d’environ sept minutes après la première tentative, écart de cadence explicitement conservé. Cadence ancrée à 2026-10-05T13:22:54.960783+00:00. Les débits des essais invalides sont diagnostics, jamais inclus dans les moyennes.

Surcharge distincte : 61.309332 s cumulées d'essais, coût natif 0.010391734 (devise N/A), exclus des tokens/coûts de production.

| Tokens sondes | Effectif et part |
| --- | --- |
| input | 48 (0.1 %) |
| output | 2561 (2.9 %) |
| reasoning | 0 (0.0 %) |
| cache_write | 42504 (48.5 %) |
| cache_read | 42504 (48.5 %) |
| Total | 87617 (100.0 %) |


CAB : 33 requêtes uniques ; 32 décisions approuvées (97,0 % des requêtes), une absence de décision sur erreur de paramètres MCP (3,0 %). Parmi les 32 approbations, 31 opérations exécutées (96,9 %) et une approbation inutilisée gelée après timeout (3,1 %). Les 31 opérations correspondent à 9 écritures et 22 Bash ; la tentative Bash hors mandat refusée est exclue de ces opérations.

Cadence : quatre positions attendues et relevées (début, +30, +60, fin), zéro relève manquée (0,0 %). +30 envoyée 17,48 s après l’échéance ; +60 envoyée 8,77 s après l’échéance. La reprise de +30 est retardée de 437,41 s après son premier envoi ; écart conservé. Huit tentatives invalides (100,0 %), zéro valide (0,0 %) : TTMT et débit moyens N/A motivés. Deux tentatives maximum par position, aucun outil de sonde.

## 2. Types de messages et d'outils

| Rôle | Nombre et part |
| --- | --- |
| assistant | 105 (73.9 %) |
| user | 37 (26.1 %) |
| Total | 142 (100.0 %) |

| Partie | Nombre et part |
| --- | --- |
| reasoning | 105 (22.8 %) |
| step-finish | 105 (22.8 %) |
| step-start | 105 (22.8 %) |
| text | 73 (15.8 %) |
| tool | 73 (15.8 %) |
| Total | 461 (100.0 %) |

| Terminaison assistant | Nombre et part |
| --- | --- |
| stop | 36 (34.3 %) |
| tool-calls | 69 (65.7 %) |
| Total | 105 (100.0 %) |

| Outil | Appels (% globaux) | Réussis (% outil) | Refus (% outil) | Erreurs (% outil) |
| --- | --- | --- | --- | --- |
| bash | 23 (31.5 %) | 22 (95.7 %) | 1 (4.3 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 2 (2.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 33 (45.2 %) | 31 (93.9 %) | 0 (0.0 %) | 2 (6.1 %) |
| read | 6 (8.2 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 9 (12.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 73 (100.0 %) | 70 (95.9 %) | 1 (1.4 %) | 2 (2.7 %) |

## 3. Fichiers modifiés

Tentatives write/edit natives, pas lectures ni fichiers uniques. Chemins complets conservés.

| Chemin absolu | Tentatives (% éditions) | Réussies | Refus | Erreurs |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-recipient-refusal/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-recipient-refusal/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-recipient-refusal/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-recipient-refusal/specs/notifications/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-undeclared-recipient-refusal/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/notification_recipient_declaration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_notification_recipient_declaration_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_notification_recipient_declaration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Archive : cinq artefacts déplacés sans changement de contenu (5/5, 100,0 %), trois sources préservées à leur chemin (3/3, 100,0 %). Seule canonical openspec/specs/notifications/spec.md ajoute le scénario autorisé ; requirement et scénario Canal restent identiques. Baseline : 180/181 (99,4 %) fichiers inchangés ; canonical 75/76 (98,7 %) inchangées. Tous les travaux antérieurs sont conservés. Venv temporaire créé puis nettoyé et pycache régénérables exclus. Seul output/cismp-state.json est écrit directement par CGPT, métadonnées de reprise hors outils natifs. STATISTIQUES.md est publié après cette collecte, son édition n'est pas ajoutée rétroactivement.

## 4. Commandes

| Famille | Appels (% commandes) | Réussis | Refus | Erreurs |
| --- | --- | --- | --- | --- |
| CABtest | 3 (13.0 %) | 2 (66.7 %) | 1 (33.3 %) | 0 (0.0 %) |
| Nettoyage artefact régénérable | 1 (4.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (4.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec strict | 6 (26.1 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python syntaxe | 3 (13.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python tests | 4 (17.4 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Venv temporaire | 1 (4.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| pip pins déclarés | 4 (17.4 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 23 (100.0 %) | 22 (95.7 %) | 1 (4.3 %) | 0 (0.0 %) |

Commandes success regroupées, libellés ≤100 caractères (exact disponible dans preuves natives/état) :

| Commande | Occurrences (% statut) |
| --- | --- |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
| /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/.local/n… | 1 (4.5 %) |
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
| /usr/bin/rm -r -- /home/devops/datas/pixs/.venv-cismp-recipient-20261005 | 1 (4.5 %) |
| true | 2 (9.1 %) |

Commandes rejected regroupées, libellés ≤100 caractères (exact disponible dans preuves natives/état) :

| Commande | Occurrences (% statut) |
| --- | --- |
| true | 1 (100.0 %) |

Commandes error regroupées, libellés ≤100 caractères (exact disponible dans preuves natives/état) :

0 ; taux N/A — dénominateur nul.

## 5. Accès web

Outils web natifs : 0 (0,0 % des outils). Deux commandes pip public PyPI approuvées et exécutées : 2/2 (100,0 %) réussies, 0/2 refus (0,0 %), 0/2 erreurs (0,0 %). URL effectivement utilisée : https://pypi.org/simple (2/2, 100,0 % des opérations attestées). Aucune URL refusée ; sous-requêtes/wheels/redirections N/A — non mesurées. Les liens de métadonnées pip show ne sont pas des pages visitées. HTTP/SSE local OpenCode/CAB est du transport. Aucun outil web dans les sondes.

## 6. Synthèse globale

Début 2026-10-05T13:22:54.380000+00:00 ; fin 2026-10-05T14:25:32.543111+00:00 ; durée 01h02m38s, pauses incluses. La rédaction/publication ultérieure est exclue.

| Quota Codex codex /10080min | Horodatage | Utilisé / reset |
| --- | --- | --- |
| Avant | 2026-10-05T13:22:54.380861+00:00 | N/A — mcp__codex_app__get_usage_limits absent ; reset N/A |
| Après | 2026-10-05T14:25:32.543111+00:00 | N/A — même outil absent ; reset N/A |
| Après−avant | — | N/A — deux relevés natifs absents, aucun quota remplacé |

| Domaine | Appels (% total) | Réussis | Refus | Erreurs |
| --- | --- | --- | --- | --- |
| Fichiers | 9 (12.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 23 (31.5 %) | 22 (95.7 %) | 1 (4.3 %) | 0 (0.0 %) |
| Web natif | 0 (0,0 %) | N/A — aucun appel | N/A — aucun appel | N/A — aucun appel |
| Autres | 41 (56.2 %) | 39 (95.1 %) | 0 (0.0 %) | 2 (4.9 %) |
| Global | 73 (100.0 %) | 70 (95.9 %) | 1 (1.4 %) | 2 (2.7 %) |

| Validation native | Tests / part | Résultat |
| --- | --- | --- |
| Unitaires complets | 962 (82.6 %) | exit0 / 10.613 s |
| Intégration complète | 203 (17.4 %) | exit0 / 11.205 s |
| Total complet | 1165 (100.0 %) | 100,0 % réussis |
| Ciblés | 15 (100.0 %) | 100,0 % réussis |
| Compilations | 3/3 (100,0 %) | exit0 |
| Stricts pré/post | 6/6 (100,0 %) | change/76specs/77all |
| Archivage | 1/1 (100,0 %) | delta ~1 autorisé vérifié |

Aucun commit/push ni accès .git ; aucun Docker ou PostgreSQL externe. project.env non lu : aucune opération PostgreSQL n'était nécessaire. Aucun secret exposé dans code/mandats/rapport. Accès externe : seuls pins déjà déclarés sur PyPI ; aucun environnement existant modifié. Le helper est interne, déclaratif, sans normalisation ni envoi. Contrat complet, préférences/consentements, périmètre, runtime/réessais/audit demeurent des exigences résiduelles ; ce change ne les déclare pas implémentées.
