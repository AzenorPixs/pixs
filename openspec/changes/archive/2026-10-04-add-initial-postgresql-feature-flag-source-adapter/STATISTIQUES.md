# STATISTIQUES — add-initial-postgresql-feature-flag-source-adapter

Archive : openspec/changes/archive/2026-10-04-add-initial-postgresql-feature-flag-source-adapter. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-04T15:04:45.747608+00:00–2026-10-04T16:46:31.809454+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.489 s | 98.014 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

254 messages, 176 outils, durée calendaire 01 h 41 min 46 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 31 | 100.0 % |
| Total | 31 | 100 % |

Développement : compilation exit 0 ; 2 tests unitaires du chargeur PG, 1 intégration fraîche et 189 régressions, 192/192 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 1266 |
| Tokens output | 150454 |
| Tokens reasoning | 0 |
| Tokens total | 34748695 |
| Tokens cache_read | 34044977 |
| Tokens cache_write | 551998 |
| Coût SDK déclaré | 0.72602251 USD |
| Compactions OpenCode observées | 1 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initial — préparation adaptateur PostgreSQL | 2026-10-04T15:05:02.988562+00:00 | 2026-10-04T15:05:06.847116+00:00 | 2026-10-04T15:05:12.765578+00:00 | 3.859 s | 5.918 s | 552 | 93.267/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T15:35:04.283412+00:00 | 2026-10-04T15:35:07.017118+00:00 | 2026-10-04T15:35:13.668338+00:00 | 2.734 s | 6.651 s | 532 | 79.985/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T16:05:06.171021+00:00 | 2026-10-04T16:05:09.975556+00:00 | 2026-10-04T16:05:16.322835+00:00 | 3.805 s | 6.347 s | 614 | 96.734/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T16:35:06.650532+00:00 | 2026-10-04T16:35:09.966624+00:00 | 2026-10-04T16:35:14.149094+00:00 | 3.316 s | 4.182 s | 523 | 125.046/s | valide |
| fin — après archivage source PG | 2026-10-04T16:46:22.571343+00:00 | 2026-10-04T16:46:26.302193+00:00 | 2026-10-04T16:46:31.637061+00:00 | 3.731 s | 5.335 s | 507 | 95.035/s | valide |

Collecte : 5 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 5 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.734/3.859 s ; débit min/max 79.985/125.046/s. Surcharge : 2728 tokens de sortie, 67028 tokens total SDK, 0.01414066 USD, 45.878 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 211 | 83.1 % |
| user | 43 | 16.9 % |
| Total | 254 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.1 % |
| reasoning | 211 | 23.6 % |
| step-finish | 211 | 23.6 % |
| step-start | 211 | 23.6 % |
| text | 85 | 9.5 % |
| tool | 176 | 19.7 % |
| Total | 895 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 43 | 16.9 % |
| stop | 43 | 16.9 % |
| tool-calls | 168 | 66.1 % |
| Total | 254 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 72 (40.9 %) | 72 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 31 (17.6 %) | 31 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 17 (9.7 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 31 (17.6 %) | 31 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 11 (6.2 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 11 (6.2 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 3 (1.7 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 176 (100 %) | 176 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-postgresql-feature-flag-source-adapter/proposal.md | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-postgresql-feature-flag-source-adapter/design.md | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-postgresql-feature-flag-source-adapter/tasks.md | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-postgresql-feature-flag-source-adapter/.openspec.yaml | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-postgresql-feature-flag-source-adapter/specs/feature-flags/spec.md | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/__init__.py | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0001_feature_flag_source_snapshot.py | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/feature_flag_postgres_source.py | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_postgres_source.py | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_postgres_source_integration.py | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 (100 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

12 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-postgresql-feature-flag-source-adapter/. Aucun delta canonique effectif (+0/~0/-0). Les modules antérieurs restent byte à byte inchangés. Six nouvelles sources/test exactes, trente-sept fichiers de baseline inchangés et README backend en append seul. La source PG est lue par version exacte et validée par le codec ; aucun accès multi-tenant ou runtime embarqué.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Tests unittest | 4 (23.5 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 5 (29.4 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 6 (35.3 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test PostgreSQL réel isolé | 1 (5.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (5.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 (100 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 5 (29.4 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-postgresql-feature-flag-source-adapter --… | 3 (17.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --strict | 1 (5.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 6 (35.3 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 1 (5.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-postgresql-feature-flag-source-adapter --y… | 1 (5.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 (100 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée par le codeur. Sources primaires consultées par l’orchestrateur : https://www.djangoproject.com/download/ et documentation officielle Django 6.1 sur JSONField et migrations ; nombre agrégé des appels orchestrateur N/A. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T15:04:45.747608+00:00 UTC |
| Fin — après archivage | 2026-10-04T16:46:31.809454+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 41 min 46 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T15:04:45.747608+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T16:46:31.809454+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 145 (82.4 %) | 145 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 17 (9.7 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 14 (8.0 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 176 (100 %) | 176 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Bilan : 192 tests sûrs réussis ; test PostgreSQL réel distinct exit0, toutes preuves fermées vraies : migration forward/reverse, roundtrip exact, unique SELECT public, refus, cleanup succès et échec simulé, connexions fermées. Six compilations, stricts et tâches prouvés. Source versionnée en lecture uniquement, livraison partielle R4 : administration, audit/corrélation, cache, convergence des rôles, garde de build, contrôle multi-tenant et activation runtime restent hors périmètre. Git non consulté ; aucun commit/push ni changement UI. PLLM mode1 qwen3.8-flash xhigh conservée ; processus OpenCode jamais fermé ni redémarré. Corrections ciblées de brouillons avant publication : version opaque sans strip, gardes réellement armées, transactions/ownership/cleanup/connexions du harnais privé, doc précise sur propagation des erreurs inattendues. Une collision de variable du pilote après publication prouvée de proposal a été réparée et réconciliée sans rejouer cette écriture. Un pending_count transitoire après compilation a été réconcilié par READY0 réel avant le test sûr. Les erreurs de pilotage ne sont pas des échecs des tests natifs. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|
| paired-c891ea79fcfb405b98f9de678c16f85e | 2026-10-04T16:17:51.649874+00:00 | msg_107b51b1c001GVN5mrX0Ezw9dA / 2026-10-04T16:19:40.570080+00:00 | 01a107b5-1a89-7df3-99f5-611fdcfcb6de / 2026-10-04T16:23:21.776954+00:00 | RESTORED |

Compteur conjoint documenté : 1. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
