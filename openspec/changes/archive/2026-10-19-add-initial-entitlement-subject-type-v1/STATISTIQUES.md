# STATISTIQUES — EntitlementSubjectType v1

RUN : `cismp1-pixs-36356c8a18ce4bb8` ; contexte CAB : **379** ; session de travail : `ses_eabe2a737ffeLNxds1Q0DgJDlW` ; sélection : `ses_eabec7d13ffeZURgFIyY7k4Q81`.
Archive : `openspec/changes/archive/2026-10-19-add-initial-entitlement-subject-type-v1`. Publication technique : `publish-4e49fef0f2e2455d95f803688702918a`, référence **48**.
Collecte de production limitée aux deux sessions identifiées et arrêtée au relevé final ci-dessous. Les trois sondes dédiées sont une surcharge séparée. La rédaction du présent rapport et les opérations ultérieures de clôture sont hors agrégats ; son propre mandat ne se compte pas lui-même. Aucun chiffre d’un RUN voisin n’est ajouté.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version LLM non exposée ; OpenCode 1.19.3 observé | opencode-go | high | 1.777 s | 627.2 | N/A — phases modèle non isolées des attentes/outils |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — télémétrie native indisponible |

Le dénominateur du temps de service cumulé est N/A : il n’est pas possible de séparer les générations des attentes de permission et des outils. Les durées calendaires et busy ne sont pas des temps de service modèle.

## 1. Statistiques générales et décisions

Durée de collecte : **00 h 43 min 41 s**, pauses, prévol, attentes, tests et archivage inclus. Les **3/3 fichiers Python compilent (100 %)** ; **17/17 tests réussissent (100 %)**. Le strict ciblé a réussi après correction de longueur ; strict global avant archive : **186/186 (100 %)** ; après archive et réconciliation : **185/185 (100 %)**. Le strict final vaut exit 0. La variante globale sans --strict n’est pas rejouée : le strict global réussit.

| Décision CAB | Nombre | Part des décisions |
| --- | --- | --- |
| approved | 24 | 100,0 % |
| rejected | 0 | 0,0 % |
| needs_clarification | 0 | 0,0 % |
| pending | 0 | 0,0 % |
| Total | 24 | 100,0 % |

Permissions once observées par CAB : **23** ; effets natifs suivis par les mandats achevés : **23**. Une décision approuvée a été annulée sans effet avant l’édition PROJECT trop large ; elle n’a pas été rejouée. Les refus d’autorisation sont distincts des échecs de validation et des erreurs MCP.

| Tokens de production OpenCode | Nombre | Part des composants |
| --- | --- | --- |
| Entrée hors cache | 471399 | 2,9 % |
| Lecture cache | 15609916 | 96,6 % |
| Écriture cache | 0 | 0,0 % |
| Sortie | 53392 | 0,3 % |
| Raisonnement | 16381 | 0,1 % |
| Total des composants | 16151088 | 100,0 % |
| Total natif exposé | 16151088 | Compteur natif distinct |

Les tokens sont cumulés par appel, pas dédupliqués par document. Coût facturé : **N/A**, facture et bascule sur fonds propres non exposées par les API. Le quota mensuel PLLM1 reste à 100 % ; la poursuite est couverte par l’instruction explicite du développeur. Aucun coût n’est déduit des quotas.
Benchmark réel : TTFT **7.4761 s**, palier réussi **2048 tokens**, borne conservatrice du débit global **203.3 tokens/s** sur la durée totale. Le débit brut calculé sur le seul flux visible n’est pas présenté comme un débit global mesuré : les instants des tokens de raisonnement sont absents.

| Sonde distincte | Envoi | TTMT (s) | Débit sortie (tokens/s) | Tokens sortie | Durée requête (s) |
| --- | --- | --- | --- | --- | --- |
| début | 19/10/2026 14:12:21 CEST | 1.090 | 777.9 | 368 | 1.576 |
| +30 min | 19/10/2026 14:42:54 CEST | 2.098 | 449.8 | 368 | 2.930 |
| fin | 19/10/2026 14:52:12 CEST | 2.144 | 654.0 | 368 | 2.839 |

Sondes : **3 prévues, 3 réussies (100 %), 0 échouée (0 %), 0 manquée (0 %)**. La relève +30 min a été exécutée avec environ 34 s de retard, sans reconstruction rétroactive. TTMT min/max : 1.090/2.144 s ; débit min/max : 449.8/777.9 tokens/s. Surcharge : **39376 tokens natifs**, coût N/A ; moyennes arithmétiques sur 3 relèves valides.
Compactions OpenCode observées : 0 ; compactions Codex : N/A, API non exposée. L’intervalle est inférieur à l’échéance coordonnée de 90 minutes.
Coordination du seul contexte 379 : attente de ressources 0 ms ; détention partagée 779198 ms ; temps d’effet émis 5606 ms. Ces intervalles peuvent se recouvrir et ne mesurent pas un gain de productivité.

Incidents conservés : quota mensuel épuisé puis dérogation humaine ; premier palier PLLM 1024 sans réponse complète avant réussite à 2048 ; deux timeouts MCP de sélection pendant la réconciliation du broker ; timeout MCP du même mandat puis polling corrélé ; premier strict ciblé exit 1 pour une clause >500 caractères, corrigée sans changer son sens ; avertissement non bloquant d’archivage sur les en-têtes français Why/What Changes attendus par la CLI ; édition PROJECT trop large annulée avant effet ; écritures documentaires C02 concurrentes préservées et compteurs réconciliés. Aucun réarchivage.

## 2. Types de messages et d’outils

| Rôle | Messages | Part |
| --- | --- | --- |
| assistant | 124 | 68,5 % |
| user | 57 | 31,5 % |
| Total | 181 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 130 | 19,4 % |
| step-finish | 124 | 18,5 % |
| step-start | 124 | 18,5 % |
| text | 156 | 23,3 % |
| tool | 136 | 20,3 % |
| Total | 670 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| stop | 31 | 25,0 % |
| tool-calls | 93 | 75,0 % |

| Outil | Appels | Part globale | Terminés | Refusés | Erreurs techniques | En cours/inconnus |
| --- | --- | --- | --- | --- | --- | --- |
| bash | 9 | 6,6 % | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 1 | 0,7 % | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 11 | 8,1 % | 10 (90,9 %) | 0 (0,0 %) | 1 (9,1 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 3 | 2,2 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 1 | 0,7 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 24 | 17,6 % | 23 (95,8 %) | 0 (0,0 %) | 1 (4,2 %) | 0 (0,0 %) |
| edit | 2 | 1,5 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| glob | 5 | 3,7 % | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 11 | 8,1 % | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| question | 1 | 0,7 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 56 | 41,2 % | 56 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 12 | 8,8 % | 12 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 136 | 100 % | 133 (97,8 %) | 0 (0,0 %) | 3 (2,2 %) | 0 (0,0 %) |

Les parts sont arrondies à une décimale ; leur somme affichée peut légèrement différer de 100 %.

Convention : un outil terminé prouve l’exécution de l’appel, pas nécessairement une approbation manuelle. Les lectures et MCP aboutis sont autorisés automatiquement ; les écritures et Bash restent corrélés aux décisions CAB/once. Une commande terminée en exit 1 est un échec de validation, pas un refus de permission ni une panne de l’outil. Les erreurs techniques de cette collecte concernent les délais MCP.

## 3. Fichiers modifiés

| Chemin absolu de la tentative | Tentatives | Part | Exécutées | Refusées | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/PROJECT.md | 2 | 14,3 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/README.md | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-entitlement-subject-type-v1/.openspec.yaml | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-entitlement-subject-type-v1/design.md | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-entitlement-subject-type-v1/proposal.md | 2 | 14,3 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-entitlement-subject-type-v1/specs/quotas-entitlements/spec.md | 2 | 14,3 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-entitlement-subject-type-v1/tasks.md | 2 | 14,3 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/entitlement_subject_type.py | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_entitlement_subject_type_integration.py | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_entitlement_subject_type.py | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 14 | 100 % | 14 | 0 | 0 |

Les nombres sont des tentatives natives d’édition, pas des fichiers uniques : **10 cibles uniques**. Les cinq artefacts du change ont été déplacés sous **/home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-initial-entitlement-subject-type-v1** par l’unique commande d’archive ; cette commande a synchronisé **/home/devops/datas/pixs/openspec/specs/quotas-entitlements/spec.md** (+4 exigences/+4 scénarios, exigences précédentes inchangées). Les caches py_compile sont des artefacts régénérables et ne sont pas des éditions natives séparées. Le présent **/home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-initial-entitlement-subject-type-v1/STATISTIQUES.md** est produit hors intervalle, sous mandat distinct.
README.md et PROJECT.md ont été actualisés uniquement pour le suivi de la livraison ; les décisions documentaires concurrentes C02 ont été conservées et ne sont pas attribuées à CISMP1.

## 4. Commandes

| Famille | Exécutions | Part |
| --- | --- | --- |
| OpenSpec — archivage | 1 | 11,1 % |
| OpenSpec — validation | 5 | 55,6 % |
| Prévol sans effet | 1 | 11,1 % |
| Python — compilation | 1 | 11,1 % |
| Python — tests | 1 | 11,1 % |
| Total | 9 | 100 % |

| Commande exécutée, libellé borné à 100 caractères | Occurrences | Part |
| --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-entitlement-subject-type-v1 --yes | 1 | 11,1 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 3 | 33,3 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-entitlement-subject-type-v1 --strict | 2 | 22,2 % |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/entitlement_subject_type.py t… | 1 | 11,1 % |
| /usr/bin/true | 1 | 11,1 % |
| PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest tests.unit.test_entitlement_s… | 1 | 11,1 % |

Codes de sortie natifs : **8 exit 0 (88,9 %)**, **1 exit 1 (11,1 %)** ; l’exit 1 concerne le premier strict ciblé corrigé. Commandes refusées : **0 (0,0 %)** ; aucune commande refusée à regrouper. Tests PostgreSQL, build frontend et migrations : non applicables à ce profil passif ; seuls les tests Python ciblés et de régression ci-dessus sont revendiqués.

## 5. Accès web

| Statut des outils web | Nombre | Part |
| --- | --- | --- |
| approuvé/exécuté | 0 | N/A |
| refusé | 0 | N/A |
| erreur technique | 0 | N/A |
| Total | 0 | N/A |

Aucun webfetch/websearch, aucune URL visitée ou refusée par ces outils. Les appels locaux de pilotage et les transmissions au fournisseur LLM sont distincts de cette catégorie et ne sont pas convertis en visites web. Transmission Pixs à Muse couverte par l’accord durable et la demande de RUN ; valeurs des secrets confinées aux processus sécurisés et au stockage natif d’authentification. Aucun message externe envoyé.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 19/10/2026 14:09:05 CEST |
| Fin — après archivage | 19/10/2026 14:52:46 CEST |
| Durée globale (pauses et attentes incluses) | 00 h 43 min 41 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 19/10/2026 14:09:24 CEST | 56 % | 25/10/2026 01:23:28 CEST |
| Après — après archivage de la spécification | 19/10/2026 14:52:46 CEST | 60 % | 25/10/2026 01:23:28 CEST |
| Différence après − avant | — | 4 points | — |

Les quotas sont partagés par le compte. Leur variation pendant cet intervalle peut inclure d’autres tâches simultanées ; elle n’est pas attribuée exclusivement à ce RUN. Aucune conversion de quota en tokens ou coût. Le relevé final précède la rédaction du rapport et la clôture technique.

| Domaine | Appels | Part globale | Terminés/autorisés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| fichiers | 14 | 10,3 % | 14 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| commandes | 9 | 6,6 % | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| web | 0 | 0,0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| autres outils | 113 | 83,1 % | 110 (97,3 %) | 0 (0,0 %) | 3 (2,7 %) |
| Global | 136 | 100 % | 133 (97,8 %) | 0 (0,0 %) | 3 (2,2 %) |

Résultat livré : Enum passive à quatre sujets, 3 compilations et 17 tests verts, canon synchronisé, archive unique et publication durable. Inventaire : **78 capacités, 772 exigences, 892 scénarios ; 153 archivés + 107 ouverts = 260 changes ; 58,85 %** selon la méthode documentaire, sans mesure de qualification fonctionnelle. Git non inspecté et non modifié ; aucun commit/push, déploiement, provider runtime ou droit supplémentaire. Le cycle global reste incomplet. La vérification du rapport précède gate, désarmement, libération et arrêt ciblé. Les preuves de clôture, postérieures à la borne statistique, sont conservées dans le checkpoint du RUN ; elles ne sont pas anticipées par ces agrégats.
