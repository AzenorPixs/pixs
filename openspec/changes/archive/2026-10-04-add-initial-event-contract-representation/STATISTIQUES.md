# STATISTIQUES — add-initial-event-contract-representation

Archive : openspec/changes/archive/2026-10-04-add-initial-event-contract-representation. Sessions : ses_ef7eb7d79ffeuBiziOyVOpqd18, ses_ef7971176ffeR7zOxqw3EO7ZZB. Historique API complet borné à 2026-10-04T18:34:32.344609+00:00–2026-10-04T19:59:42.459146+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 2.975 s | 76.471 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

230 messages, 142 outils, durée calendaire 01 h 25 min 10 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 25 | 100.0 % |
| Total | 25 | 100 % |

Développement : compilation exit 0 ; 14 tests unitaires des contrats d’événement, 1 intégration fraîche et 257 régressions, 272/272 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical events inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les brouillons ont été revus avant publication; la précision du design après publication a reçu un mandat distinct et une validation stricte réussie. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

Réconciliation opérationnelle observée : le strict du change après la précision ciblée du design était prouvé exit0. Un pending_count transitoire de 1 persistait encore à la première relecture MCP ; le contrôle du pilote a suspendu le mandat suivant. Une seconde relecture native broker_readiness a prouvé READY pending0. La correction publiée et le strict acquis n’ont pas été répétés. Ces attentes ne sont pas des échecs de test ni des refus de permissions.

Un appel de compilation a ajouté un suffixe echo non mandaté : permission explicitement refusée, tour seul interrompu, aucune compilation exécutée. Les 58 baselines, cinq artefacts et trois sources ont été reconfirmés exacts avant nouvelle session et contrat strict. La restauration a aussi corrigé un simple décompte de rapport : 58 tâches et 94 lignes, sans changement de fichier. Des délais MCP puis une absence d’injection ont été constatés pendant la récupération native du seul contexte. Ces erreurs de pilotage restent distinctes des tests applicatifs. Les preuves de disponibilité réelle et du nouveau test CAB sont conservées séparément ; aucun processus OpenCode fermé ni redémarré.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 1092 |
| Tokens output | 124740 |
| Tokens reasoning | 0 |
| Tokens total | 27013910 |
| Tokens cache_read | 23428995 |
| Tokens cache_write | 3459083 |
| Coût SDK déclaré | 1.12547212 USD |
| Compactions OpenCode observées | 1 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| début — contrats événement déclaratifs | 2026-10-04T18:34:32.635464+00:00 | 2026-10-04T18:34:37.443591+00:00 | 2026-10-04T18:34:46.243813+00:00 | 4.808 s | 8.800 s | 597 | 67.839/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T19:04:33.736985+00:00 | 2026-10-04T19:04:36.510547+00:00 | 2026-10-04T19:04:42.079104+00:00 | 2.774 s | 5.569 s | 498 | 89.431/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T19:34:35.915802+00:00 | 2026-10-04T19:34:37.916850+00:00 | 2026-10-04T19:34:45.809839+00:00 | 2.001 s | 7.893 s | 499 | 63.221/s | valide |
| fin — après archive événements déclaratifs | 2026-10-04T19:59:33.716858+00:00 | 2026-10-04T19:59:36.035819+00:00 | 2026-10-04T19:59:42.265727+00:00 | 2.319 s | 6.230 s | 532 | 85.395/s | valide |

Collecte : 4 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.001/4.808 s ; débit min/max 63.221/89.431/s. Surcharge : 2126 tokens de sortie, 53566 tokens total SDK, 0.01128602 USD, 40.393 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 184 | 80.0 % |
| user | 46 | 20.0 % |
| Total | 230 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.1 % |
| reasoning | 183 | 23.1 % |
| step-finish | 182 | 23.0 % |
| step-start | 183 | 23.1 % |
| text | 101 | 12.8 % |
| tool | 142 | 17.9 % |
| Total | 792 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 48 | 20.9 % |
| stop | 44 | 19.1 % |
| tool-calls | 138 | 60.0 % |
| Total | 230 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 72 (50.7 %) | 68 (94.4 %) | 0 (0.0 %) | 4 (5.6 %) |
| cgpt-validation_request_validation | 25 (17.6 %) | 25 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (5.6 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 9 (6.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 15 (10.6 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |
| edit | 2 (1.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 7 (4.9 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 (0.7 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| cgpt-validation_broker_health | 1 (0.7 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| invalid | 1 (0.7 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| grep | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 142 (100 %) | 134 (94.4 %) | 1 (0.7 %) | 7 (4.9 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-event-contract-representation/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-contract-representation/design.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-contract-representation/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-contract-representation/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-contract-representation/specs/events/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/event_contract.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_event_contract.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_event_contract_integration.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-event-contract-representation/. Aucun delta canonique effectif (+0/~0/-0). Les modules antérieurs restent byte à byte inchangés. Trois nouvelles sources/tests exactes, cinquante-huit fichiers de baseline inchangés. DomainEventContract et IntegrationEventContract représentent des métadonnées injectées; aucun flux externe ni runtime.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 6 (40.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 4 (26.7 %) | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test CAB sans effet | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-event-contract-representation --strict --… | 4 (26.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --no-interactive | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 4 (26.7 %) | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict --no-interactive | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-event-contract-representation --yes | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T18:34:32.344609+00:00 UTC |
| Fin — après archivage | 2026-10-04T19:59:42.459146+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 25 min 10 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T18:34:32.344609+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T19:59:42.459146+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 117 (82.4 %) | 110 (94.0 %) | 0 (0.0 %) | 7 (6.0 %) |
| Fichiers | 10 (7.0 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 15 (10.6 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 142 (100 %) | 134 (94.4 %) | 1 (0.7 %) | 7 (4.9 %) |

Bilan : 272 tests sûrs réussis, trois compilations natives exit0 et stricts réussis, toutes tâches du change prouvées, archive contrôlée. Deux contrats déclaratifs figés distincts à cinq champs, constructeurs structurels non validants, deux validateurs explicites à type exact avant callbacks, diagnostics freshlist triés/dédupliqués sans valeurs; quatre références opaques trusted ou synthétiques, version SemVer via parse_version public. Les refus croisés assurent la seule séparation structurelle des types. Aucune exposition extérieure réelle, enveloppe complète, payload, validation de schéma effectif, ordre effectif, transaction, outbox, publisher, idempotence, persistance ou classification de secret prouvée. Les trois sources AuditEvent et les suites fanions/backend/PG antérieures restent inchangées; aucun PG réel supplémentaire. Git non consulté, aucun commit/push, config, dépendance, README ou UI modifié. PLLM mode1 qwen3.8-flash xhigh conservée, processus OpenCode jamais fermé ni redémarré. Les incidents éventuels de pilotage sont distingués des résultats natifs des tests. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|
| paired-a5d8e8dd1ab74b7e8a5f4b49ded01e87 | 2026-10-04T19:21:29.167107+00:00 | msg_1085d37d2001a1R7rs6Ig5soo5 / 2026-10-04T19:23:27.151054+00:00 | 01a1085d-37b6-7b83-9d6d-a11a02e9ead0 / 2026-10-04T19:27:06.763679+00:00 | RESTORED |

Compteur conjoint documenté : 1. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
