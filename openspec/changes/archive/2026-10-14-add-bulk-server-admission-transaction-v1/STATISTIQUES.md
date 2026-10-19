# Statistiques — admission serveur Bulk B01

Change : `add-bulk-server-admission-transaction-v1`. RUN : `cismp-pixs-6d45ca1d322c4c05`.
Périmètre : préparation de B01, reprise normative validée GovernanceResolutionV1, implémentation et archive. Les huit sessions natives ci-dessous sont incluses ; les autres changes et les RUN CISMP2/CISMP3 sont exclus.
Sources : historiques HTTP natifs OpenCode, preuves CAB du checkpoint et relevés natifs de quota Codex. L’intervalle est figé avant cette rédaction ; l’écriture de ce rapport, sa vérification et la clôture CAB ultérieure sont exclues. Aucun contenu de message, raisonnement interne, secret ou sortie SQL brute n’est reproduit.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version LLM non fournie | OpenCode Go (opencode-go) | high | 3.817 s | 299.752 | N/A |
| muse-spark-1.3-contributor — compactages | N/A — version LLM non fournie | OpenCode Go (opencode-go) | N/A — API summarize sans variant | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — identifiant exact du LLM non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Les moyennes de Muse portent sur les 15 sondes dédiées valides, avec le même prompt et la même configuration high. Aucun orchestrateur n’a été sondé. La génération active des interventions de production n’est pas chronométrée de façon complète : dénominateur du temps de service indisponible, chevauchements non quantifiables, pourcentages N/A. Les durées API, les pauses, les outils et les attentes de permission ne sont pas assimilés au temps de génération. OpenCode 1.19.0 est la version du runtime observé, pas une version du LLM.

## 1. Statistiques générales et décisions

Convention : « exécutée » désigne un appel d’outil natif terminé, avec autorisation automatique ou manuelle. Un appel MCP réussi ne prouve pas une approbation manuelle. Un code de commande non nul reste une commande exécutée ; il ne devient pas une validation réussie. « refusée » exige un refus explicite de permission. Les interruptions, erreurs de schéma et échecs de transport sans refus sont des erreurs techniques.

| Catégorie | Nombre | Part |
| --- | --- | --- |
| Messages utilisateur, contexte et mandats | 323 | 35.7 % |
| Messages assistant | 582 | 64.3 % |
| **Total** | 905 | 100.0 % |

| Catégorie | Tentatives | Part | Exécutées (taux) | Refusées (taux) | Erreurs (taux) |
| --- | --- | --- | --- | --- | --- |
| Tous les appels d’outils | 526 | 100.0 % | 506 (96.2 %) | 2 (0.4 %) | 18 (3.4 %) |
| **Total** | 526 | 100.0 % | 506 (96.2 %) | 2 (0.4 %) | 18 (3.4 %) |

| Catégorie | Nombre | Part |
| --- | --- | --- |
| APPROVED | 78 | 95.1 % |
| Échec de transmission ou schéma | 4 | 4.9 % |
| **Total** | 82 | 100.0 % |

Les 78 réponses APPROVED de request_validation sont distinctes des 78 appels natifs exécutés soumis à permission : 46 commandes et 32 écritures. L’égalité des totaux ne constitue pas une corrélation unitaire ; les identifiants et les preuves natives conservés dans le checkpoint font autorité. Un mandat d’écriture approuvé a notamment été gelé après une demande Bash parasite refusée. Les contrôles globaux stricts ont conservé leurs codes réels.

Résultats finaux : 523 tests Bulk réussis ; preuve PostgreSQL complète réussie pour IMPORT/EXPORT × CSV/NDJSON, identité B10, rejeu, conflit, concurrence, rollback tardif, échec COMMIT réel et visibilité avant COMMIT. Nettoyage du schéma et fermeture des connexions prouvés. Compilation finale des cinq fichiers réussie. B01 strict : valide sans issue. Global standard avant archive : 79/79 ; global strict avant archive : 77/79, code 1 ; après archive : 76/78, code 1. Ces deux spécifications conservent quatre warnings de longueur connus, sans ERROR ni issue nouvelle : Bulk requirements[6],[10],[13] et IdentityAssurance requirements[4].

Incidents conservés : refus du chemin absolu dans un mandat, commande Bash hors mandat refusée, échec unitaire sur les exports publics puis correction, deux exécutions PostgreSQL partielles nettoyées avant la preuve finale. La faute du délimiteur SQL du harnais a été corrigée ; aucune réussite historique n’est reconstruite. Le serveur PostgreSQL réel est 16.14, contre 16.15 déclaré dans DEVOPS ; ce drift hors périmètre est signalé, sans changement de version ni correction documentaire silencieuse.

Production — compteurs natifs cumulés, cache inclus dans le total retourné :
| Compteur natif de tokens | Nombre | Part du total natif |
| --- | --- | --- |
| input | 6117432 | 7.6 % |
| output | 247205 | 0.3 % |
| reasoning | 122819 | 0.2 % |
| cache_read | 73984370 | 91.9 % |
| cache_write | 0 | 0.0 % |
| **Total natif** | 80471826 | 100.0 % |

Couverture des compteurs : 582 réponses sur 582 (100.0 %). Coût natif de production : 0.83371674, couverture 582/582 (100.0 %) ; devise N/A, aucun montant en euros ou conversion déduite.

Compactages : 3 résumés natifs achevés ; coût natif 0.02035000, devise N/A. Ils sont exclus des compteurs de production ci-dessus. Le compactage conjoint Codex reste partiel : API propriétaire de compactage non exposée, aucun succès conjoint inventé.
| Compteur natif de tokens | Nombre | Part du total natif |
| --- | --- | --- |
| input | 190260 | 96.6 % |
| output | 3597 | 1.8 % |
| reasoning | 3023 | 1.5 % |
| cache_read | 0 | 0.0 % |
| cache_write | 0 | 0.0 % |
| **Total natif** | 196880 | 100.0 % |

Sondes — surcharge séparée de la production :

| Catégorie | Nombre | Part |
| --- | --- | --- |
| Relèves nominales réussies | 12 | 80.0 % |
| Relèves nominales échouées | 0 | 0.0 % |
| Relèves nominales manquées | 3 | 20.0 % |
| **Total** | 15 | 100.0 % |

Relèves prévues selon les échéances consignées : 15. Sondes supplémentaires : 3 ; total de sondes exécutées : 15, dont 15 valides (100.0 %). Les trois relèves manquées ne sont pas recréées rétroactivement.
Tokens de sortie des sondes : 18186 (100,0 % des sorties de sondes consignées). Coût natif partiel : 0.00944840, couverture 6/15 (40.0 %), devise N/A. Durée de génération textuelle mesurée partielle : 26.812343 s, couverture 6/15 (40.0 %). Les ancrages monotones, tokens d’entrée, coût et durée non conservés des anciennes sondes restent N/A ; ils ne sont pas reconstitués à partir d’un débit.

| Mesure sur sondes valides | Minimum | Moyenne arithmétique | Maximum |
| --- | --- | --- | --- |
| TTMT (s) | 1.360 | 3.817 | 14.479 |
| Tokens/seconde | 174.258 | 299.752 | 526.650 |

| Phase | Position | Horodatage réel | TTMT (s) | Tokens/s | Sortie | Ancrages bruts |
| --- | --- | --- | --- | --- | --- | --- |
| reprise | début-reprise | 2026-10-14 05:46:18 +0200 | 1.360 | 526.650 | 1210 | N/A |
| reprise | relève périodique | 2026-10-14 06:17:33 +0200 | 2.427 | 272.275 | 1210 | N/A |
| reprise | fin de préparation B01 — attente RSMP | 2026-10-14 06:44:35 +0200 | 14.479 | 260.930 | 1210 | N/A |
| rsmp_governance | début-reprise | 2026-10-14 07:32:27 +0200 | 4.301 | 313.296 | 1246 | N/A |
| rsmp_governance | sonde supplémentaire après relève +30 min manquée | 2026-10-14 08:19:35 +0200 | 1.859 | 487.308 | 1210 | N/A |
| rsmp_governance | sonde supplémentaire après relève manquée | 2026-10-14 08:36:51 +0200 | 2.692 | 274.106 | 1210 | N/A |
| rsmp_governance | relève périodique | 2026-10-14 09:02:30 +0200 | 2.179 | 287.084 | 1210 | N/A |
| rsmp_governance | fin du sous-job RSMP | 2026-10-14 09:12:01 +0200 | 2.383 | 245.961 | 1210 | N/A |
| b01_after_governance | début-reprise | 2026-10-14 09:19:28 +0200 | 1.970 | 174.258 | 1210 | N/A |
| b01_after_governance | relève périodique | 2026-10-14 09:49:55 +0200 | 1.557 | 311.051 | 1210 | présents |
| b01_after_governance | relève périodique | 2026-10-14 10:20:18 +0200 | 2.277 | 310.441 | 1210 | présents |
| b01_after_governance | sonde supplémentaire après relève manquée | 2026-10-14 10:52:46 +0200 | 4.141 | 223.098 | 1210 | présents |
| b01_after_governance | relève périodique | 2026-10-14 11:20:06 +0200 | 8.011 | 290.045 | 1210 | présents |
| b01_after_governance | relève périodique | 2026-10-14 11:49:28 +0200 | 4.979 | 230.860 | 1210 | présents |
| b01_after_governance | fin après archivage B01 | 2026-10-14 12:09:19 +0200 | 2.635 | 288.923 | 1210 | présents |

| Phase | Échéance nominale manquée | État |
| --- | --- | --- |
| rsmp_governance | 2026-10-14 08:02:27 +0200 | MANQUÉE — aucune mesure rétroactive |
| rsmp_governance | 2026-10-14 08:32:27 +0200 | MANQUÉE — aucune mesure rétroactive |
| b01_after_governance | 2026-10-14 10:49:28 +0200 | MANQUÉE — aucune mesure rétroactive |

Prompt commun : « Écris exactement 80 lignes, sans autre texte. Chaque ligne suit ce modèle : Ligne 001 : mesure déterministe du débit de génération. Numérote les lignes de 001 à 080. Aucun outil. »
SHA-256 du prompt : `101ca6c633f11d1db2201abf533e7eeef51916169f8a021455cd915e236d8ff8`. Les TTMT concernent le premier contenu textuel SSE ; le débit utilise les tokens de sortie réels divisés par l’intervalle premier/dernier texte. Les sessions de sondes étaient dédiées, sans outils, puis supprimées.

## 2. Types de messages et d’outils

Rôles des messages :
| Catégorie | Nombre | Part |
| --- | --- | --- |
| user | 323 | 35.7 % |
| assistant | 582 | 64.3 % |
| **Total** | 905 | 100.0 % |

Types de parties, sans reproduction de leur contenu :
| Catégorie | Nombre | Part |
| --- | --- | --- |
| text | 788 | 25.1 % |
| step-start | 578 | 18.4 % |
| reasoning | 672 | 21.4 % |
| tool | 526 | 16.7 % |
| step-finish | 576 | 18.3 % |
| compaction | 3 | 0.1 % |
| **Total** | 3143 | 100.0 % |

Terminaisons des réponses assistant :
| Catégorie | Nombre | Part |
| --- | --- | --- |
| tool-calls | 374 | 64.3 % |
| stop | 202 | 34.7 % |
| erreur | 6 | 1.0 % |
| **Total** | 582 | 100.0 % |

Résultats par outil natif :
| Catégorie | Tentatives | Part | Exécutées (taux) | Refusées (taux) | Erreurs (taux) |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 107 | 20.3 % | 104 (97.2 %) | 0 (0.0 %) | 3 (2.8 %) |
| cgpt-validation_request_validation | 82 | 15.6 % | 78 (95.1 %) | 0 (0.0 %) | 4 (4.9 %) |
| bash | 47 | 8.9 % | 46 (97.9 %) | 1 (2.1 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 12 | 2.3 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 149 | 28.3 % | 146 (98.0 %) | 0 (0.0 %) | 3 (2.0 %) |
| grep | 10 | 1.9 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 15 | 2.9 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 43 | 8.2 % | 41 (95.3 %) | 0 (0.0 %) | 2 (4.7 %) |
| cgpt-validation_poll_approval | 6 | 1.1 % | 0 (0.0 %) | 0 (0.0 %) | 6 (100.0 %) |
| cgpt-validation_cancel_approval | 2 | 0.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 20 | 3.8 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 1 | 0.2 % | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| glob | 20 | 3.8 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 12 | 2.3 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| **Total** | 526 | 100.0 % | 506 (96.2 %) | 2 (0.4 %) | 18 (3.4 %) |

Répartition native par configuration observée :
| Catégorie | Nombre | Part |
| --- | --- | --- |
| muse-spark-1.3-contributor / opencode-go / high | 579 | 99.5 % |
| muse-spark-1.3-contributor / opencode-go / N/A | 3 | 0.5 % |
| **Total** | 582 | 100.0 % |

Sessions effectivement incluses :
| Session native | Titre | Messages | Part |
| --- | --- | --- | --- |
| ses_ec77e1e1affedNH5uGbZjWiajZ | CISMP1 — admission Bulk B01 | 190 | 21.0 % |
| ses_ec71fd835ffe3vvU7S5XbYWUNP | CISMP1 — RSMP GovernanceResolutionV1 | 11 | 1.2 % |
| ses_ec71c9877ffel7eYMbCONDODwl | CISMP1 — récupération RSMP gouvernance | 162 | 17.9 % |
| ses_ec6b8f1b2ffepXQSREEuii5bvP | CISMP1 — B01 admission transactionnelle | 108 | 11.9 % |
| ses_ec6923c98ffeslc2ORt95K109s | CISMP1 — reprise B01 après test des exports | 254 | 28.1 % |
| ses_ec63a7e22ffeGViMFYsr2zdqK9 | CISMP1 — reprise B01 après commande hors mandat | 38 | 4.2 % |
| ses_ec6320b6dffehyHPDaS2tEdNSc | CISMP1 — reprise B01 et preuves PostgreSQL | 28 | 3.1 % |
| ses_ec62e03b0ffetCuqTWFdoZwWmQ | CISMP1 — reprise B01 et preuves PostgreSQL | 114 | 12.6 % |
| **Total** | 8 sessions | 905 | 100.0 % |

Les appels de l’orchestrateur, messages de coordination entre chats, événements natifs de permissions et commandes hôte ne sont pas comptés comme appels OpenCode. Leur métrique exhaustive n’est pas exposée : N/A. Les décisions et incidents explicitement prouvés sont conservés séparément dans l’état du RUN. Les arrondis à une décimale peuvent produire une somme affichée légèrement différente de 100 %.

## 3. Fichiers modifiés

Il s’agit des tentatives d’écriture natives directes, pas d’un nombre de fichiers uniques ni d’un diff Git. Les lectures, artefacts de compilation et déplacements réalisés par la commande d’archivage sont exclus de ces 32 écritures et classés selon leur appel d’origine.
| Catégorie | Tentatives | Part | Exécutées (taux) | Refusées (taux) | Erreurs (taux) |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-admission-transaction-v1/proposal.md | 2 | 6.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-admission-transaction-v1/design.md | 5 | 15.6 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md | 1 | 3.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/TECHNICAL.md | 1 | 3.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-admission-transaction-v1/specs/bulk-operations/spec.md | 1 | 3.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-server-admission-transaction-v1/tasks.md | 3 | 9.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_trusted_ports.py | 5 | 15.6 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_trusted_ports.py | 4 | 12.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_server_admission.py | 3 | 9.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_server_admission.py | 2 | 6.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_server_admission_postgres_integration.py | 5 | 15.6 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| **Total** | 32 | 100.0 % | 32 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Onze chemins ont reçu une écriture directe. Les quatre artefacts du change ont ensuite été déplacés vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-bulk-server-admission-transaction-v1` par l’archivage autorisé ; leurs empreintes ont été préservées, ainsi que celle du canon. La modification de TECHNICAL et du canon appartient à la reprise normative approuvée ; ces cadrages n’ont plus changé pendant l’implémentation. Aucune suppression ou modification fonctionnelle hors périmètre n’a été constatée dans la comparaison ciblée des 125 fichiers de référence. Git n’a pas été inspecté.

## 4. Commandes

| Catégorie | Tentatives | Part | Exécutées (taux) | Refusées (taux) | Erreurs (taux) |
| --- | --- | --- | --- | --- | --- |
| Prévol CAB | 14 | 29.8 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests | 11 | 23.4 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 14 | 29.8 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 7 | 14.9 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Autres commandes | 1 | 2.1 % | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| **Total** | 47 | 100.0 % | 46 (97.9 %) | 1 (2.1 %) | 0 (0.0 %) |

Codes de sortie des seules commandes exécutées :
| Catégorie | Nombre | Part |
| --- | --- | --- |
| 0 | 37 | 80.4 % |
| 2 | 1 | 2.2 % |
| 1 | 8 | 17.4 % |
| **Total** | 46 | 100.0 % |

Toutes les commandes refusées, regroupées par libellé (100 caractères maximum) :
| Commande refusée | Occurrences | Part des commandes refusées |
| --- | --- | --- |
| python3 -c "print('decode-check')" | 1 | 100.0 % |
| **Total** | 1 | 100.0 % |

Commandes exécutées avec code non nul ; les libellés tronqués ne remplacent pas les commandes exactes conservées dans l’historique :
| Libellé (100 caractères maximum) | Code réel | Occurrences | Part des sorties non nulles |
| --- | --- | --- | --- |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.ve… | 2 | 1 | 11.1 % |
| /usr/bin/env OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate bulk… | 1 | 1 | 11.1 % |
| /home/devops/.local/npm/bin/openspec validate bulk-operations --type spec --strict --json --no-inte… | 1 | 1 | 11.1 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json --no-interactive | 1 | 1 | 11.1 % |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/devops/datas/pixs/src:/home/devops/datas/pi… | 1 | 1 | 11.1 % |
| PYTHONPATH=src:tests PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/python3 -B -c 'imp… | 1 | 2 | 22.2 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 1 | 2 | 22.2 % |
| **Total** | — | 9 | 100.0 % |

Les codes 1 des contrôles stricts restent non réussis : leurs avertissements sont qualifiés séparément. L’échec unitaire et les deux tentatives PostgreSQL incomplètes ont précédé les preuves finales réussies. Le code 2 historique reste visible ; il ne prouve pas une livraison. Les 523 tests de la dernière régression incluent des tests déjà exécutés : aucun total de tests uniques n’est inventé.

## 5. Accès web

| Statut | Nombre | Part / taux |
| --- | --- | --- |
| Approuvés et visités | 0 | N/A — aucun accès |
| Refusés | 0 | N/A — aucun accès |
| Erreurs | 0 | N/A — aucun accès |
| **Total** | 0 | N/A — dénominateur nul |

Aucun accès web natif ni URL effectivement visitée dans les huit sessions du périmètre. Les API locales OpenCode/CAB et PostgreSQL ne sont pas des accès web de l’agent de codage. Aucun résultat de recherche ne vaut preuve de visite.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-14 05:38:43 +0200 |
| Fin — après archivage | 2026-10-14 12:09:56 +0200 |
| Durée globale (pauses et attentes incluses) | 06 h 31 min 12 s |

Cette durée est calendaire et inclut préparation, pauses de validation, reprises, tests et archive. Elle n’additionne pas les durées d’agents simultanés et n’est pas leur temps de service. La rédaction, la vérification du présent rapport et la clôture CAB sont postérieures à la fin de collecte et exclues.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — heure exacte non conservée ; collecte 2026-10-14 05:38:43 +0200 | 11 % | 2026-10-20 06:59:31 +0200 |
| Après — après archivage de la spécification | 2026-10-14 12:09:56 +0200 | 18 % | 2026-10-20 06:59:31 +0200 |
| Différence après − avant | — | N/A — identité du compte initial non conservée | — |

Les deux relevés natifs conservés portent sur codex / 10080 minutes, avec la même réinitialisation. L’écart arithmétique est 7 points, mais la comparaison stricte de l’identité du compte initial n’est pas vérifiable dans les données sauvegardées : différence auditée N/A. Les quotas sont partagés par le compte ; leur variation peut inclure d’autres tâches et n’est jamais attribuée exclusivement à B01. Aucune conversion en tokens ou euros.

| Catégorie | Tentatives | Part | Exécutées (taux) | Refusées (taux) | Erreurs (taux) |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 32 | 6.1 % | 32 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 47 | 8.9 % | 46 (97.9 %) | 1 (2.1 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 447 | 85.0 % | 428 (95.7 %) | 1 (0.2 %) | 18 (4.0 %) |
| **Total** | 526 | 100.0 % | 506 (96.2 %) | 2 (0.4 %) | 18 (3.4 %) |

Bilan livré : admission interne B01, 523 tests de régression réussis, preuve PostgreSQL complète et compilation finale réussies, huit tâches cochées après preuve. Archive réelle : `/home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-bulk-server-admission-transaction-v1`, sortie 0, artefacts et canon préservés. Strict global après archive : code 1 uniquement pour les quatre warnings déjà connus ; aucun ERROR ni issue nouvelle. Aucun commit, push, branche ni consultation de Git. Aucun accès web natif. Aucune lecture native de project.env observée ; les variables de connexion sont restées dans le processus de test dédié, sans valeur dans les prompts, journaux ou rapport.
La fin du RUN est limitée par l’instruction du développeur à ce change archivé et à ses statistiques vérifiées. Elle ne prétend pas que toutes les exigences futures de Pixs sont implémentées. La clôture CAB, le désarmement et la libération seront réconciliés après vérification de ce fichier ; OpenCode ne sera ni fermé ni redémarré.
