# STATISTIQUES — add-initial-command-metadata-representation

Archive : openspec/changes/archive/2026-10-04-add-initial-command-metadata-representation. Sessions : ses_ef7971176ffeR7zOxqw3EO7ZZB. Historique API complet borné à 2026-10-04T20:13:09.871710+00:00–2026-10-04T21:15:01.665086+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 2.607 s | 92.913 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

195 messages, 129 outils, durée calendaire 01 h 01 min 51 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 22 | 100.0 % |
| Total | 22 | 100 % |

Développement : compilation exit 0 ; 23 tests unitaires des métadonnées de commande, 1 intégration fraîche et 301 régressions, 325/325 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical interactions inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les brouillons ont été revus avant publication ; les précisions de périmètre, bootstrap et gardes ont été intégrées avant publication sans norme nouvelle. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

Pilotage orchestrateur : deux erreurs de construction JavaScript ont été observées avant l’exécution des outils, puis corrigées. Le contrôle AST d’un brouillon d’intégration a aussi détecté une parenthèse superflue, corrigée avant toute publication. Aucun effet de projet ni test applicatif n’en a résulté. Ces faits sont conservés séparément et ne sont pas incorporés artificiellement dans les totaux SDK OpenCode. Les autres totaux orchestrateur restent N/A faute d’historique agrégé exposé.

Une écriture de module a introduit une divergence limitée à une ligne de docstring. CGPT a comparé les octets et confirmé que les 76 baselines et les cinq artefacts restaient exacts ; la compilation n’avait pas commencé. Une édition ciblée sous mandat neuf a rétabli le contenu approuvé, sans rejouer la publication complète. Les transitoires de readiness pending1 ont également été relus jusqu’à READY0, sans répéter les stricts réussis. Ces contrôles de pilotage sont distincts des résultats de compilation et de tests.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 954 |
| Tokens output | 95946 |
| Tokens reasoning | 0 |
| Tokens total | 22000043 |
| Tokens cache_read | 19962984 |
| Tokens cache_write | 1940159 |
| Coût SDK déclaré | 0.75267726 USD |
| Compactions OpenCode observées | 1 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| début — métadonnées de commande | 2026-10-04T20:13:10.056560+00:00 | 2026-10-04T20:13:12.045142+00:00 | 2026-10-04T20:13:19.728248+00:00 | 1.989 s | 7.683 s | 507 | 65.989/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T20:43:12.908562+00:00 | 2026-10-04T20:43:16.234251+00:00 | 2026-10-04T20:43:20.341779+00:00 | 3.326 s | 4.108 s | 527 | 128.301/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T21:13:14.962331+00:00 | 2026-10-04T21:13:18.427190+00:00 | 2026-10-04T21:13:24.105386+00:00 | 3.465 s | 5.678 s | 522 | 91.930/s | valide |
| fin — CommandMetadata après archive | 2026-10-04T21:14:54.001394+00:00 | 2026-10-04T21:14:55.651303+00:00 | 2026-10-04T21:15:01.386959+00:00 | 1.650 s | 5.736 s | 490 | 85.431/s | valide |

Collecte : 4 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 1.650/3.465 s ; débit min/max 65.989/128.301/s. Surcharge : 2046 tokens de sortie, 53486 tokens total SDK, 0.00888328 USD, 33.634 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 159 | 81.5 % |
| user | 36 | 18.5 % |
| Total | 195 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.1 % |
| reasoning | 159 | 23.3 % |
| step-finish | 159 | 23.3 % |
| step-start | 159 | 23.3 % |
| text | 76 | 11.1 % |
| tool | 129 | 18.9 % |
| Total | 683 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 36 | 18.5 % |
| stop | 36 | 18.5 % |
| tool-calls | 123 | 63.1 % |
| Total | 195 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 65 (50.4 %) | 65 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 22 (17.1 %) | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (6.2 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 15 (11.6 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 4 (3.1 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 12 (9.3 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 2 (1.6 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 129 (100 %) | 129 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-command-metadata-representation/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-metadata-representation/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-metadata-representation/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-metadata-representation/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-metadata-representation/specs/interactions/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/command_metadata.py | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_command_metadata.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_command_metadata_integration.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-command-metadata-representation/. Aucun delta canonique effectif (+0/~0/-0). Les modules antérieurs restent byte à byte inchangés. Trois nouvelles sources/tests exactes, soixante-seize fichiers de baseline inchangés. CommandMetadata porte des métadonnées injectées et un ScopeContext public structurellement validé ; aucun flux externe ni runtime.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 5 (41.7 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 (100 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-command-metadata-representation --strict … | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --no-interactive | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/.local/npm/bin:/home/devops/python/current/bin:/usr/bin:/bin LANG… | 4 (33.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 (100 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T20:13:09.871710+00:00 UTC |
| Fin — après archivage | 2026-10-04T21:15:01.665086+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 01 min 51 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T20:13:09.871710+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T21:15:01.665086+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 107 (82.9 %) | 107 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 10 (7.8 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 12 (9.3 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 129 (100 %) | 129 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Bilan : 325 tests sûrs réussis, trois compilations natives exit0 et stricts réussis, toutes tâches du change prouvées, archive contrôlée. CommandMetadata structurel figé à sept champs avec slots, constructeur non validant et deux exports ; validateur explicite à type exact avant callbacks, diagnostics frais triés/dédupliqués sans valeurs ; quatre références opaques trusted ou synthétiques, tuples exacts préservés. ScopeContext et validate_structure publics réutilisés ; seule ScopeStructureError attendue convertie, erreurs inattendues propagées. Aucun sujet/tenant légitime, UUID, topologie, autorisation, clé composée TECH18, comparaison de payload, restitution/conflit de rejeu, déduplication, rétention, transaction, persistance ou exécution prouvés. Les sources AuditEvent/event-contract/Core/scope/identity et suites fanions/backend/PG antérieures restent inchangées ; aucun PG réel supplémentaire. Git non consulté, aucun commit/push, config, dépendance, README ou UI modifié. PLLM mode1 qwen3.8-flash xhigh conservée, processus OpenCode jamais fermé ni redémarré. Les incidents éventuels de pilotage sont distingués des résultats natifs des tests. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|
| paired-d8fc8eb35be245c58be30732c0063819 | 2026-10-04T20:51:31.586318+00:00 | msg_108afa708001bJGWOIy66ZL6VP / 2026-10-04T20:52:59.258851+00:00 | 01a108af-a6f0-79d2-929d-92ab41dff5ae / 2026-10-04T20:57:12.465125+00:00 | RESTORED |

Compteur conjoint documenté : 1. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
