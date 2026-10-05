# STATISTIQUES — add-initial-feature-flag-source-contract

Archive : openspec/changes/archive/2026-10-04-add-initial-feature-flag-source-contract. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-04T11:15:12.617805+00:00–2026-10-04T12:46:15.265481+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.020 s | 82.124 | N/A |
| qwen3.8-flash — compactage | N/A — version exacte absente | opencode-go | xhigh configuré ; variante non exposée par API summarize | N/A — pas de sonde distincte | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

175 messages, 118 outils, durée calendaire 01 h 31 min 02 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 22 | 95.7 % |
| REJECTED | 1 | 4.3 % |
| Total | 23 | 100 % |

Développement : compilation exit 0 ; 16 tests unitaires du contrat de source, 1 intégration fraîche et 119 régressions, 136/136 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 870 |
| Tokens output | 91209 |
| Tokens reasoning | 0 |
| Tokens total | 37909515 |
| Tokens cache_read | 36698764 |
| Tokens cache_write | 1118672 |
| Coût SDK déclaré | 0.85391335 USD |
| Compactions OpenCode observées | 1 |
| Compactions orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale contrat snapshot | 2026-10-04T11:15:12.824990+00:00 | 2026-10-04T11:15:16.855976+00:00 | 2026-10-04T11:15:23.084899+00:00 | 4.031 s | 6.229 s | 546 | 87.656/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T11:45:14.931597+00:00 | 2026-10-04T11:45:19.193933+00:00 | 2026-10-04T11:45:25.464152+00:00 | 4.262 s | 6.270 s | 584 | 93.139/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T12:15:16.464475+00:00 | 2026-10-04T12:15:19.206527+00:00 | 2026-10-04T12:15:26.110767+00:00 | 2.742 s | 6.904 s | 551 | 79.806/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T12:45:18.092873+00:00 | 2026-10-04T12:45:19.853961+00:00 | 2026-10-04T12:45:26.200113+00:00 | 1.761 s | 6.346 s | 497 | 78.315/s | valide |
| finale après archive snapshot | 2026-10-04T12:46:05.382746+00:00 | 2026-10-04T12:46:07.685900+00:00 | 2026-10-04T12:46:15.146816+00:00 | 2.303 s | 7.461 s | 535 | 71.707/s | valide |

Collecte : 5 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 5 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 1.761/4.262 s ; débit min/max 71.707/93.139/s. Surcharge : 2713 tokens de sortie, 67013 tokens total SDK, 0.01176847 USD, 48.310 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 146 | 83.4 % |
| user | 29 | 16.6 % |
| Total | 175 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.2 % |
| reasoning | 146 | 23.9 % |
| step-finish | 145 | 23.7 % |
| step-start | 146 | 23.9 % |
| text | 56 | 9.2 % |
| tool | 118 | 19.3 % |
| Total | 612 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 30 | 17.1 % |
| length | 1 | 0.6 % |
| stop | 27 | 15.4 % |
| tool-calls | 117 | 66.9 % |
| Total | 175 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 57 (48.3 %) | 56 (98.2 %) | 0 (0.0 %) | 1 (1.8 %) |
| read | 12 (10.2 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 23 (19.5 %) | 22 (95.7 %) | 0 (0.0 %) | 1 (4.3 %) |
| write | 9 (7.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 13 (11.0 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 (1.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 118 (100 %) | 116 (98.3 %) | 0 (0.0 %) | 2 (1.7 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-source-contract/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-source-contract/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-source-contract/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-source-contract/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-source-contract/specs/feature-flags/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flag_sources.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_sources.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_sources_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-feature-flag-source-contract/. Aucun delta canonique effectif (+0/~0/-0). Les deux modules antérieurs de fanions et de cohorte restent byte à byte inchangés. Trois nouvelles sources exactes, vingt-deux fichiers de baseline inchangés. Le contrat valide un snapshot injecté ; aucune affectation runtime réelle embarquée.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 5 (38.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test CAB sans effet | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 (100 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-source-contract --strict | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate feature-flags --type spec --strict | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-source-contract --yes | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 (100 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T11:15:12.617805+00:00 UTC |
| Fin — après archivage | 2026-10-04T12:46:15.265481+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 31 min 02 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T11:15:12.617805+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T12:46:15.265481+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 96 (81.4 %) | 94 (97.9 %) | 0 (0.0 %) | 2 (2.1 %) |
| Fichiers | 9 (7.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 13 (11.0 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 118 (100 %) | 116 (98.3 %) | 0 (0.0 %) | 2 (1.7 %) |

Bilan : 136 tests réussis, compilation et contrôles stricts réussis, toutes les tâches du change prouvées, archive contrôlée. Contrat pur de snapshot livré dans un profil borné : types exacts, validation complète du lot, liaisons de définitions/affectations/règles et version attendue avant délégation réelle à l'évaluateur de cohorte. Jamais une autorisation positive. Provenance persistante du snapshot, persistance/administration/audit, cache/convergence des rôles, résolution de prérequis, autre lifecycle et réévaluation applicative de bout en bout restent hors périmètre. Git non consulté, aucun commit/push de ce cycle ; aucune DB ni modification UI, aucun test navigateur applicable. Authentification contrôlée en processus dédié sans sortie sensible ni transmission au modèle ; bascule mode 2 vers mode 1 pendant ce change, stockage privé standard et rechargement interne explicitement autorisés par le développeur. Le processus OpenCode et l'interface restent ouverts, sans arrêt ni redémarrage. Aucune valeur sensible dans le rapport. Une demande de compilation ajoutant -B a été refusée avant tout Bash puis récupérée sous mandat neuf ; une rédaction tronquée a été complétée uniquement pour le fichier manquant et un délai de readiness après rechargement a été repris. Ces incidents restent visibles. Compactage natif de la session de codage observé ; le compactage conjoint avec l'orchestrateur n'est pas déclaré réussi, le contrôle natif du thread réel ayant été identifié mais aucun cycle commun n’ayant encore été exécuté. Les amendements documentaires CAB/tools-codex demandés séparément sont hors du périmètre fonctionnel Pixs et de ses comptes de production OpenCode. Parent CISMP revient à SÉLECTION après relecture de ce rapport.
