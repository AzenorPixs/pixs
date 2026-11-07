# STATISTIQUES — add-initial-job-correlation-representation

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-correlation-representation. RUN parent cismp-pixs-20261005-2654fe47. Rapport de cette unité seulement ; préparation/publication du rapport exclues des mesures figées.

Sources : messages et parties natifs OpenCode, métadonnées exit des Bash, décisions CAB relues par requestId, événements SSE corrélés et empreintes dans le checkpoint. Les sondes dédiées, sans outil et supprimées après collecte, sont séparées de la production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | OpenCode 1.18.34 ; modèle N/A — non exposé | opencode-go | xhigh ; PLLM mode 1 | 2.4940 s — sondes historiques | 88.5817 — sondes historiques | N/A — durée active non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — identité exacte non exposée | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — non exposé | N/A — durée active non exposée |

Mise en forme rectifiée : tableaux agents avant les six sections, colonnes exactes ; temps de service cumulé N/A, sans substitution par durée calendaire. Données historiques conservées. Agent OpenCode 1.18.34, PLLM mode 1, contexte déclaré 1 000 000 tokens. Pourcentages présentés à une décimale.

## 1. Statistiques générales et décisions

Session(s) : ses_ef1d91fd9ffe9pMx6g9s8vqb3H. La version précise n'est pas déduite du nom du modèle.

| Sondes | Valeur |
| --- | --- |
| Prévues | 3 |
| Réussies | 3 / 100.0 % |
| Échouées | 0 / 0.0 % |
| Manquées | 0 / 0.0 % |
| TTMT moyen / min / max | 2.4940 / 2.1126 / 3.0119 s |
| Débit moyen arithmétique / min / max | 88.5817 / 62.5046 / 134.9021 tokens/s |

Même prompt déterministe demandé à chaque relève : Output exactly 128 identical lines, each containing: 0123456789 abcdefghijklmnopqrstuvwxyz. Do not explain. Do not call tools. Même modèle/fournisseur/variante ; zéro appel d'outil observé. La relève +30 minutes est concurrente au travail ; +60 n'était pas due avant la dernière tâche d'archivage. La sonde finale a été lancée immédiatement après cette tâche.

| Position | Envoi UTC | État | Sortie tokens | TTMT s | Génération s | Tokens/s |
| --- | --- | --- | --- | --- | --- | --- |
| début JobCorrelation | 2026-10-05T23:25:30.537286+00:00 | success | 78 | 2.1126 | 1.2479 | 62.5046 |
| +30 min | 2026-10-05T23:55:31.071227+00:00 | success | 266 | 3.0119 | 3.8924 | 68.3383 |
| fin JobCorrelation | 2026-10-06T00:09:22.891090+00:00 | success | 1496 | 2.3575 | 11.0895 | 134.9021 |

| Position | Premier token UTC | Dernier token UTC | Durée collecte s | Coût déclaré USD |
| --- | --- | --- | --- | --- |
| début JobCorrelation | 2026-10-05T23:25:32.649864+00:00 | 2026-10-05T23:25:33.897767+00:00 | 7.0426 | 0.00215816 |
| +30 min | 2026-10-05T23:55:34.083097+00:00 | 2026-10-05T23:55:37.975496+00:00 | 7.036 | 0.00224652 |
| fin JobCorrelation | 2026-10-06T00:09:25.248571+00:00 | 2026-10-06T00:09:36.338089+00:00 | 14.0458 | 0.00282462 |

Surcharge de télémétrie exclue de la production : 33667 tokens déclarés dont 1840 sortie ; 28.1244 s de collecte et 0.007229300 USD déclarés. Ces durées peuvent se chevaucher avec le travail, elles ne sont pas ajoutées à la durée calendaire. La télémétrie de coût n'est pas une facture d'abonnement Go.

Les compteurs du codeur ne sont pas attribués à l'orchestrateur. Ses diagnostics HTTP/lectures ne sont pas des outils OpenCode ; comptage exhaustif de ces actions N/A.

| Mesure production | Nombre | Part pertinente |
| --- | --- | --- |
| Messages | 117 | 100.0 % |
| Parties | 383 | 100.0 % |
| Outils | 61 | 100.0 % |
| Outils terminés | 60 | 98.4 % |
| Outils en erreur | 1 | 1.6 % |
| Décisions CAB uniques | 22 | 100.0 % |
| CAB approved | 22 | 100.0 % |
| CAB rejected | 0 | 0.0 % |
| Permissions once | 22 | 100.0 % |
| Permissions reject | 0 | 0.0 % |

Incident observé : request_validation de la compilation intégration a expiré côté client. POST de décision contrôleur 400, GET décision 404 : aucune décision ni commande exécutée. get_approval réel PENDING a confirmé identifiants et cible ; rappel de notification livré, décision CGPT unique, get_approval APPROVED puis exécution unique exit0. Aucun nouveau requestId pour rejouer cette commande, aucune permission hors mandat, aucun échec de test. Les diagnostics HTTP root sont hors compteurs du codeur.

| Télémétrie native | Valeur |
| --- | --- |
| input | 528 |
| output | 43823 |
| reasoning | 0 |
| cache_read | 13338849 |
| cache_write | 203927 |
| Somme des compteurs | 13587127 |
| Coût déclaré production USD | 0.274882994 |
| Réponses sans usage final | 0 |

reasoning=0 est le compteur natif déclaré, pas une preuve d'absence de raisonnement. Les sondes ne sont pas ajoutées. Aucun compactage de la session de codage observé dans cet intervalle ; le cycle périodique antérieur, partiel faute d'API orchestrateur, est hors intervalle.

| Résultat de l'unité | Réussies | Part |
| --- | --- | --- |
| Nouveaux tests | 8 | 7 unitaires + 1 intégration |
| Régressions | 103 | 18 modules existants |
| Toutes exécutions de tests | 111 | 100.0 % — 0 échec, erreur ou skip |
| py_compile | 3 | 100.0 % exit0 |
| Stricts pré/post-code | 6 | 100.0 % exit0 |
| Tâches après preuves | 6 | 100.0 % |
| Baselines préservées | 107 | 100.0 % |
| Archive unique | 1 | 100.0 % |

Stricts : change valide, 76/76 specs, 77/77 éléments avant et après le code. Dix-neuf notices INFO préexistantes signalées sans correction hors périmètre. Régressions natives : Ran 103 tests in 0.656s, OK, exit0. Durées natives : nouveaux unitaires 0.000s, intégration 0.069s. Recopies de durée/compte dans certains rapports corrigées par les preuves natives : source 77 lignes, 7 tests unitaires ; une assertion hasattr sur objet hostile a été remplacée par identité avant écriture, sans changer la source métier.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part messages |
| --- | --- | --- |
| assistant | 88 | 75.2 % |
| user | 29 | 24.8 % |

| Partie | Nombre | Part parties |
| --- | --- | --- |
| reasoning | 88 | 23.0 % |
| step-finish | 88 | 23.0 % |
| step-start | 88 | 23.0 % |
| text | 58 | 15.1 % |
| tool | 61 | 15.9 % |

| Fin réponse assistant | Nombre | Part |
| --- | --- | --- |
| stop | 29 | 33.0 % |
| tool-calls | 59 | 67.0 % |

| Outil | Appels | Part | Terminés | Erreurs | Décisions / autorisations |
| --- | --- | --- | --- | --- | --- |
| bash | 13 | 21.3 % | 13 | 0 | 13 once |
| cgpt-validation_get_approval | 2 | 3.3 % | 2 | 0 | N/A — lecture/observation |
| cgpt-validation_request_validation | 22 | 36.1 % | 21 | 1 | 22 CAB approved, un délai MCP |
| edit | 1 | 1.6 % | 1 | 0 | 1 once |
| read | 15 | 24.6 % | 15 | 0 | N/A — lecture/observation |
| write | 8 | 13.1 % | 8 | 0 | 8 once |

Deux get_approval observent une décision du même mandat, sans constituer des autorisations supplémentaires. Les états d'outil et décisions CAB sont deux bases distinctes.

## 3. Fichiers modifiés

| Chemin absolu actuel | Tentatives | Part éditions | Approuvées/réussies | Refusées | En erreur |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-correlation-representation/.openspec.yaml | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-correlation-representation/design.md | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-correlation-representation/proposal.md | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-correlation-representation/specs/jobs/spec.md | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-06-add-initial-job-correlation-representation/tasks.md | 2 | 22.2 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/job_correlation.py | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_job_correlation_integration.py | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_job_correlation.py | 1 | 11.1 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

8 fichiers distincts, 9 tentatives d'édition : tasks.md créé puis coché, autres fichiers une fois. Les cinq artefacts ont été édités sous le change actif puis déplacés par la commande d'archivage aux chemins actuels affichés ; les trois Python restent en place. STATISTIQUES.md, publié après cette collecte, exclu de ces compteurs.

Ancien dossier absent, cinq hashes d'archive conformes, tâches cochées. Delta canonique +0 / ~0 / -0 / →0, empreintes confirmées. Aucun fichier antérieur du périmètre fonctionnel modifié ; caches bytecode régénérables autorisés, temporaires des harnais nettoyés.

## 4. Commandes

| Famille | Tentatives | Part | Terminées exit0 | Erreurs |
| --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 7.7 % | 1 | 0 |
| OpenSpec validation | 6 | 46.1 % | 6 | 0 |
| Python compilation | 3 | 23.1 % | 3 | 0 |
| Python tests | 3 | 23.1 % | 3 | 0 |

| Commande affichée (100 caractères maximum) | Occurrences | Part | Terminées | Erreurs |
| --- | --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-job-correlation-representation --yes | 1 | 7.7 % | 1 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 15.4 % | 2 | 0 |
| /home/devops/.local/npm/bin/openspec validate --specs --strict | 2 | 15.4 % | 2 | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-job-correlation-representation --strict | 2 | 15.4 % | 2 | 0 |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/job_correlation.py | 1 | 7.7 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_job_correlation_integr… | 1 | 7.7 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_job_correlation.py | 1 | 7.7 % | 1 | 0 |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integrati… | 1 | 7.7 % | 1 | 0 |
| PYTHONPATH=src:. /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p t… | 1 | 7.7 % | 1 | 0 |
| PYTHONPATH=src:tests/unit:tests/integration:. /home/devops/python/current/bin/python3 -B -m unittes… | 1 | 7.7 % | 1 | 0 |

Libellés tronqués ; commandes exactes corrélées dans checkpoint/parties natives. 13 invocations Bash terminées exit0, aucune commande refusée. Commandes refusées regroupées : aucune (0 / 0.0 % des tentatives). Une compilation a attendu récupération de transport puis a été exécutée une seule fois.

## 5. Accès web

| Web du codeur | Nombre | Part |
| --- | --- | --- |
| Outils web | 0 | 0.0 % des outils |
| URL approuvées/visitées | 0 | N/A — aucune base |
| Demandes refusées | 0 | N/A — aucune demande |
| Erreurs | 0 | N/A — aucune requête |

Aucune URL approuvée, refusée ou visitée par la session de codage pendant cet intervalle. Transport d'inférence et contrôle CAB séparés du web du codeur. Gardes réseau d'intégration testées positivement avant effet. Diagnostics/consultations de l'orchestrateur non attribués au codeur, comptage exhaustif N/A.

## 6. Synthèse globale

| Durée globale | Valeur |
| --- | --- |
| Début UTC | 2026-10-05T23:25:29.825780+00:00 |
| Fin UTC | 2026-10-06T00:10:25.593614+00:00 |
| Durée calendaire | 00:44:55 — 2695.768s |
| Périmètre | Préparation/implémentation/validation/archivage/récupération et collecte finale ; rédaction/publication du rapport exclues |

Durée incluant analyse, attentes modèle et récupération MCP ; aucune attente d'échéance statistique n'a suspendu le travail.

| Quota natif Codex sur 7 jours | Horodatage | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — mcp__codex_app__get_usage_limits | 2026-10-05T23:25:29.825780+00:00 | N/A — outil non exposé | N/A |
| Après tâches/archivage/sonde finale — même outil | 2026-10-06T00:10:25.319345+00:00 | N/A — outil non exposé | N/A |
| Différence en points | N/A | N/A — relevés absents/non comparables | N/A |

Aucun quota Go, Spark ou historique substitué au quota Codex. Quotas partagés par compte ; une variation disponible ne prouverait pas une attribution exclusive.

| Domaine | Appels | Part globale | Approbations natives | Refus | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 9 | 14.8 % | 9 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Commandes | 13 | 21.3 % | 13 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Web | 0 | 0.0 % | N/A | N/A | N/A |
| Autres | 39 | 63.9 % | N/A — lectures/MCP | N/A | 1 / 2.6 % |
| Global | 61 | 100.0 % | 22 / 100.0 % de 22 permissions | 0 / 0.0 % de 22 permissions | 1 / 1.6 % des outils |

Bases explicites : outils pour parts globales/erreurs, permissions pour autorisations, décisions CAB distinctes pour mandats. Arrondis à deux décimales ; somme arrondie possiblement différente de 100 %. Une permission de régression est observée/corrélée par SSE mais son identifiant complet n'a pas été retenu à cause de la troncature d'affichage ; préfixe et partie native conservés, aucun identifiant complet inventé.

Résultat : 111 tests réussis, 3 compilations/6 stricts exit0, 6 tâches prouvées/cochées, archive unique vérifiée, 107 références préservées et canon inchangé. Git non inspecté, aucun commit/push observé. PostgreSQL, navigateur, worker, bail, envoi/provider et runtime métier non requis par cette représentation partielle, non exécutés. Aucun secret/fichier sensible transmis au codeur dans le périmètre observé. La requirement jobs R3 et son scénario de déduplication persistante restent partiellement implémentés : cette unité est un fragment structurel, pas un Job complet. Le RUN parent continue, aucune fin globale revendiquée.
