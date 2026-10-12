# STATISTIQUES — add-initial-notification-contract-declaration-gate

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-declaration-gate. RUN cismp-pixs-20261005-2654fe47. La rédaction/publication de ce rapport est exclue de l'intervalle mesuré.

Sources : messages/parties natifs OpenCode, métadonnées Bash exit, décisions CAB relues par requestId, permissions SSE et empreintes conservées dans le checkpoint. Quatre sessions successives du même change ; sondes jetables séparées.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | OpenCode 1.18.34 ; modèle N/A — non exposé | opencode-go | xhigh ; PLLM mode 1 | 2.1206 s — sondes historiques | 67.4860 — sondes historiques | N/A — durée active non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — identité exacte non exposée | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — non exposé | N/A — durée active non exposée |

Mise en forme rectifiée : tableaux agents avant les six sections, colonnes exactes ; temps de service cumulé N/A, sans substitution par durée calendaire. Données historiques conservées. Agent OpenCode 1.18.34, PLLM mode 1, contexte déclaré 1 000 000 tokens. Pourcentages présentés à une décimale.

## 1. Statistiques générales et décisions

Sessions : ses_ef265fa2fffeFSYCz8fem1VRh5, ses_ef1eaafacffeMzP6aYUptjcQG6, ses_ef1e85e84ffehtSeHAngDabEOU, ses_ef1d91fd9ffe9pMx6g9s8vqb3H. La version précise n'est pas déduite du nom du modèle.

| Sondes valides | Valeur |
| --- | --- |
| TTMT moyen / min / max | 2.1206 / 1.8547 / 2.4584 s |
| Débit moyen arithmétique / min / max | 67.4860 / 49.3937 / 100.2046 tokens/s |
| Relèves prévues | 4 — début, +30 min, +60 min, fin |
| Tentatives observées | 5 |
| Réussies | 4 (80.0 %) |
| Échouées | 1 (20.0 %) — fin expirée puis unique reprise |
| Manquées | 0 (0.0 %) |

Prompt constant : Output exactly 128 identical lines, each containing: 0123456789 abcdefghijklmnopqrstuvwxyz. Do not explain. Do not call tools. Aucun outil dans les quatre succès ; même configuration. Les sondes +30/+60 ont été lancées pendant le travail sans attente d'échéance.

| Position | Envoi UTC | État | Tokens sortie | TTMT s | Génération s | Tokens/s |
| --- | --- | --- | --- | --- | --- | --- |
| début liaison contrat | 2026-10-05T21:40:30.503579+00:00 | success | 232 | 2.1069 | 2.3153 | 100.2046 |
| +30 min | 2026-10-05T22:10:31.050465+00:00 | success | 160 | 2.4584 | 2.3563 | 67.902 |
| +60 min | 2026-10-05T22:40:31.020738+00:00 | success | 145 | 1.8547 | 2.7649 | 52.4437 |
| fin liaison contrat | 2026-10-05T22:52:08.262565+00:00 | timeout | N/A | N/A | N/A | N/A |
| fin liaison contrat retry unique | 2026-10-05T22:56:22.711567+00:00 | success | 193 | 2.0625 | 3.9074 | 49.3937 |

| Position | Premier token UTC | Dernier token UTC |
| --- | --- | --- |
| début liaison contrat | 2026-10-05T21:40:32.610429+00:00 | 2026-10-05T21:40:34.925690+00:00 |
| +30 min | 2026-10-05T22:10:33.508901+00:00 | 2026-10-05T22:10:35.865239+00:00 |
| +60 min | 2026-10-05T22:40:32.875385+00:00 | 2026-10-05T22:40:35.640251+00:00 |
| fin liaison contrat retry unique | 2026-10-05T22:56:24.774057+00:00 | 2026-10-05T22:56:28.681434+00:00 |

Surcharge séparée : 43166 tokens déclarés disponibles, dont 730 sortie. Durée SSE envoi→dernier token des succès : 19.8264 s ; échec borné à 150 s, tokens/coût N/A. Durée totale de collecte N/A (fins des trois premières sondes non conservées), reprise finale observée en 7.0369 s. Coût global N/A (trois premières sondes non capturées avant suppression) ; reprise finale 0.000261258 USD déclarés. Sondes exclues de la production.

Les données OpenCode ne sont pas attribuées à l'orchestrateur. Ses diagnostics HTTP/lectures techniques ne sont pas comptés comme outils du codeur.

| Mesure | Nombre | Part pertinente |
| --- | --- | --- |
| Messages | 178 | 100.0 % |
| Parties | 570 | 100.0 % |
| Outils | 91 | 100.0 % |
| Outils terminés | 84 | 92.3 % |
| Outils en erreur | 7 | 7.7 % |
| Décisions CAB uniques | 25 | 100.0 % |
| CAB approved | 25 | 100.0 % |
| CAB rejected | 0 | 0.0 % |
| Permissions once | 25 | 92.6 % |
| Permissions reject | 2 | 7.4 % |

Les deux refus natifs concernent un grep sans mandat et une seconde tentative du test CAB R2 après consommation de la permission. Interrompues/refusées avant exécution, elles ne sont pas des échecs de tests. Cinq autres erreurs d'outil sont des délais MCP récupérés par lecture/polling corrélé, sans double décision ni rejeu. Un approval_id distinct a été accepté explicitement par CGPT après vérification de son unicité, du requestId et de la cible inchangée.

| Télémétrie disponible | Valeur |
| --- | --- |
| input | 756 |
| output | 66390 |
| reasoning | 0 |
| cache_read | 9658536 |
| cache_write | 672175 |
| Somme des compteurs observés | 10397857 |
| Coût déclaré OpenCode, USD | 0.320288276 |
| Réponses interrompues sans usage final | 4 |

Totaux non exhaustifs : quatre réponses interrompues ont des compteurs finaux absents/zéro, donc une consommation réelle N/A. reasoning=0 est le compteur déclaré, pas une preuve d'absence de raisonnement. Le coût est une télémétrie, pas une facture de l'abonnement Go.

| Compactage de l'intervalle | Preuve native | État |
| --- | --- | --- |
| Opérationnel | msg_10e20cd5f001m8SEnvp7ibZ9j3 | Codeur terminé ; orchestrateur non exécuté, API absente |
| Périodique | msg_10e44ea8f001RQ6bwdexW4f70o | Codeur terminé ; orchestrateur non exécuté, API absente |

Deux compactages natifs du codeur sont prouvés ; aucune réussite conjointe revendiquée. Les omissions de jalons dans les résumés ont été réconciliées avec checkpoint/preuves. API orchestrateur absente : cycles partiels, aucun arrêt du RUN ni report des statistiques pour cette cause.

| Validation | Réussies | Part |
| --- | --- | --- |
| Tests nouveaux | 12 | 11 unitaires + 1 intégration |
| Régressions | 91 | 16 modules existants |
| Exécutions de tests | 103 | 100.0 % ; 0 échec/erreur/skip |
| py_compile | 3 | 100.0 % exit 0 |
| Stricts pré/post-code | 6 | 100.0 % exit 0 |
| Tâches cochées après preuve | 6 | 100.0 % |
| Références inchangées | 98 | 100.0 % |
| Archive nouvelle | 1 | 100.0 % — exécution unique |

Stricts avant/après : change valide, 76/76 specs, 77/77 éléments. Dix-neuf notices INFO préexistantes signalées sans correction hors périmètre. Régression native complète prt_10e38b523001OHAgR2fUA5mJ2H : exit0, Ran 91 tests in 0.573s, OK ; visibilité partielle côté codeur, pas de rejeu. Intégration nouvelle 0.070 s ; recopie erronée 0.001 s corrigée dans le rapport suivant.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part des messages |
| --- | --- | --- |
| assistant | 130 | 73.0 % |
| user | 48 | 27.0 % |

| Partie | Nombre | Part des parties |
| --- | --- | --- |
| compaction | 2 | 0.3 % |
| reasoning | 130 | 22.8 % |
| step-finish | 126 | 22.1 % |
| step-start | 130 | 22.8 % |
| text | 91 | 16.0 % |
| tool | 91 | 16.0 % |

| Fin de réponse assistant | Nombre | Part |
| --- | --- | --- |
| error:MessageAbortedError | 4 | 3.1 % |
| stop | 44 | 33.9 % |
| tool-calls | 82 | 63.1 % |

| Outil | Appels | Part | Terminés | Erreurs | Décisions / autorisations |
| --- | --- | --- | --- | --- | --- |
| bash | 18 | 19.8 % | 16 | 2 | 16 once ; 2 reject avant exécution |
| cgpt-validation_broker_readiness | 6 | 6.6 % | 6 | 0 | N/A — lecture/contrôle |
| cgpt-validation_get_approval | 2 | 2.2 % | 2 | 0 | N/A — lecture/contrôle |
| cgpt-validation_poll_approval | 4 | 4.4 % | 3 | 1 | N/A — lecture/contrôle |
| cgpt-validation_request_validation | 25 | 27.5 % | 21 | 4 | 25 CAB approved ; 4 retours MCP en erreur |
| edit | 1 | 1.1 % | 1 | 0 | 1 once |
| read | 27 | 29.7 % | 27 | 0 | N/A — lecture/contrôle |
| write | 8 | 8.8 % | 8 | 0 | 8 once |

Polls/get_approval observent des décisions existantes, sans nouvelle approbation. Refus natifs et erreurs techniques peuvent concerner la même tentative, sans constituer deux autorisations disjointes.

## 3. Fichiers modifiés

| Chemin absolu actuel | Tentatives | Part des éditions | Approuvées/réussies | Refusées | En erreur |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-declaration-gate/.openspec.yaml | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-declaration-gate/design.md | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-declaration-gate/proposal.md | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-declaration-gate/specs/notifications/spec.md | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-notification-contract-declaration-gate/tasks.md | 2 | 22.2 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/notification_contract_declaration.py | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_notification_contract_declaration_integration.py | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_notification_contract_declaration.py | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

8 fichiers distincts, 9 éditions (9.9 % des outils) : tasks.md créé puis coché, autres fichiers une fois. Les cinq artefacts ont été édités sous le change actif puis déplacés par archivage aux chemins actuels affichés. Trois Python demeurés en place. STATISTIQUES.md publié après cet intervalle, exclu ici.

Ancien dossier du change absent ; cinq hashes archivés conformes, six cases cochées. Delta canonique +0 / ~0 / -0 / →0 confirmé par empreintes. Caches bytecode régénérables et temporaires des harnais seuls autorisés, temporaires nettoyés.

## 4. Commandes

| Famille | Tentatives | Part | Exécutées exit0 | Interrompues avant exécution |
| --- | --- | --- | --- | --- |
| Lecture shell hors mandat | 1 | 5.6 % | 0 | 1 |
| OpenSpec archivage | 1 | 5.6 % | 1 | 0 |
| OpenSpec validation | 6 | 33.3 % | 6 | 0 |
| Python compilation | 3 | 16.7 % | 3 | 0 |
| Python tests | 3 | 16.7 % | 3 | 0 |
| Test CAB inoffensif | 4 | 22.2 % | 3 | 1 |

| Commande affichée (100 caractères maximum) | Occurrences | Part | Terminées | Erreurs outil |
| --- | --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-notification-contract-declaration-gate --y… | 1 | 5.6 % | 1 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 11.1 % | 2 | 0 |
| /home/devops/.local/npm/bin/openspec validate --specs --strict | 2 | 11.1 % | 2 | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-notification-contract-declaration-gate --… | 2 | 11.1 % | 2 | 0 |
| /home/devops/python/current/bin/python3 -B -c 'print("CAB_DECLARATION_RECOVERY_R2_OK")' | 2 | 11.1 % | 1 | 1 |
| /home/devops/python/current/bin/python3 -B -c 'print("CAB_DECLARATION_RECOVERY_R3_OK")' | 1 | 5.6 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -B -c 'print("CAB_DECLARATION_RECOVERY_R4_OK")' | 1 | 5.6 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/notification_contract_declara… | 1 | 5.6 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_notification_contract_… | 1 | 5.6 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_notification_contract_declara… | 1 | 5.6 % | 1 | 0 |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integrati… | 1 | 5.6 % | 1 | 0 |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p t… | 1 | 5.6 % | 1 | 0 |
| PYTHONPATH=src:tests/unit:tests/integration:. /home/devops/python/current/bin/python3 -B -m unittes… | 1 | 5.6 % | 1 | 0 |
| grep -n "_MSG" src/pixs/kernel/notification_channel_declaration.py src/pixs/kernel/notification_rec… | 1 | 5.6 % | 0 | 1 |

Libellés tronqués ; commandes exactes dans checkpoint/parties natives. Les 16 commandes exécutées ont exit0. Les deux autres tentatives n'ont jamais exécuté le shell.

Commandes refusées regroupées :

| Commande refusée | Nombre | Part des tentatives Bash | Cause |
| --- | --- | --- | --- |
| grep -n "_MSG" src/pixs/kernel/notification_channel_declaration.py src/pixs/kernel/notification_rec… | 1 | 5.6 % | hors mandat |
| /home/devops/python/current/bin/python3 -B -c 'print("CAB_DECLARATION_RECOVERY_R2_OK")' | 1 | 5.6 % | seconde tentative après once consommée |

## 5. Accès web

| Accès web du codeur | Nombre | Part |
| --- | --- | --- |
| Outils web | 0 | 0.0 % des outils |
| URL visitées | 0 | N/A — aucune base |
| Approbations | 0 | N/A — aucune demande |
| Refus | 0 | N/A — aucune demande |
| Erreurs | 0 | N/A — aucune requête |

Aucune URL approuvée, refusée ou visitée par les sessions de codage dans l'intervalle. Le transport d'inférence n'est pas un outil web du codeur. Gardes réseau d'intégration testées avant effet. Les consultations documentaires de l'orchestrateur ne sont pas attribuées au codeur ; comptage exhaustif N/A.

## 6. Synthèse globale

| Durée globale mesurée | Valeur |
| --- | --- |
| Début UTC | 2026-10-05T21:40:29.767503+00:00 |
| Fin UTC | 2026-10-05T22:59:55.914540+00:00 |
| Durée calendaire | 01:19:26 — 4766.147 s |
| Périmètre | Préparation/implémentation de ce change, récupérations, validation, archivage et collecte finale ; rapport exclu |

Durée incluant analyse, attentes modèle, récupérations, délais MCP et compactages. Aucune attente d'échéance statistique n'a suspendu le codage.

| Quota natif Codex sur 7 jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — mcp__codex_app__get_usage_limits | 2026-10-05T21:40:29.767503+00:00 | N/A — outil absent | N/A |
| Après tâches/archivage/sonde finale — même outil | 2026-10-05T22:57:55.166262+00:00 | N/A — outil absent | N/A |
| Différence en points | N/A | N/A — relevés absents/non comparables | N/A |

Aucun quota Go, Spark ni ancienne valeur substitué. Quotas partagés par compte : même une différence disponible ne prouverait pas une attribution exclusive au change.

| Domaine | Appels | Part globale | Approbations natives | Refus natifs | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 9 | 9.9 % | 9 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Commandes | 18 | 19.8 % | 16 / 88.9 % | 2 / 11.1 % | 2 / 11.1 % |
| Web | 0 | 0.0 % | N/A | N/A | N/A |
| Autres | 64 | 70.3 % | N/A — lectures/MCP | N/A | 5 / 7.8 % |
| Global | 91 | 100.0 % | 25 / 92.6 % de 27 permissions | 2 / 7.4 % de 27 permissions | 7 / 7.7 % des outils |

Bases explicites : parts globales sur 91 appels, autorisations globales sur 27 permissions ; 25 mandats CAB distincts tous approuvés. Arrondis à deux décimales, somme arrondie possiblement différente de 100 %. Les deux erreurs outil des refus représentent les mêmes tentatives, pas des échecs supplémentaires.

Résultat : 103 tests, 3 compilations et 6 stricts exit0, 6 tâches prouvées/cochées, archive unique sans effet canonique, 98 références préservées. Git non inspecté, aucun commit/push observé. PostgreSQL, navigateur, envoi/provider runtime non requis pour cette liaison pure, non exécutés. Aucun secret/fichier sensible transmis au codeur dans le périmètre observé. Refus et télémétrie manquante déclarés ; cette unité rend le contrôle au RUN parent sans affirmer que tout Pixs est terminé.
