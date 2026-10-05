# STATISTIQUES — add-initial-command-idempotency-dimensions

Archive : openspec/changes/archive/2026-10-05-add-initial-command-idempotency-dimensions. Sessions : ses_ef7971176ffeR7zOxqw3EO7ZZB. Historique API complet borné à 2026-10-04T21:31:28.681735+00:00–2026-10-04T22:39:08.999958+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 2.368 s | 91.964 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

169 messages, 108 outils, durée calendaire 01 h 07 min 40 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 21 | 100.0 % |
| Total | 21 | 100 % |

Développement : compilation exit 0 ; 13 tests unitaires du collecteur de dimensions, 1 intégration fraîche et 325 régressions, 339/339 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical interactions inchangé. Le transitoire pending_count 1 après archive a été réconcilié par un appel MCP réel READY pending0 sans répéter l’archivage. Les brouillons ont été revus avant publication ; les précisions de périmètre, bootstrap et gardes ont été intégrées avant publication sans norme nouvelle. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

Pilotage orchestrateur : des filtres de récupération de brouillon et de chemin de sortie ont été corrigés avant toute opération suivante ; aucun effet de source ni test n'en a résulté. Un brouillon unitaire présentait un identifiant Python avec le signe §, des assertions inactives et des attentes erronées : corrections ciblées et AST Python 3.12 avant publication. Le contrôle natif conjoint a rencontré une réponse WebSocket de 17,6 Mo dépassant la borne locale de 16 Mo, avant toute demande de compactage ; la borne a été portée à 64 Mo puis le compactage natif des deux sessions a été prouvé et les contextes restaurés sans redémarrage OpenCode. Une sonde finale produisant 39 lignes au lieu de 40 est conservée invalide et exclue des moyennes ; une seule reprise est comptabilisée. Ces contrôles sont séparés des totaux SDK OpenCode. Les autres totaux orchestrateur restent N/A faute d'historique agrégé exposé.

Les comptes annoncés dans les brouillons ont été corrigés après lecture réelle : 43 tâches au lieu de 44, 13 méthodes unitaires au lieu de 17. Ces nombres sont des observations, aucun objectif de qualité ou de volume. Un rapport a déclaré pending_count 1 alors que son appel MCP final enregistré indiquait 0 ; la preuve native a prévalu et aucun effet n'a été répété. La sortie verbose des régressions a été tronquée dans l'affichage et les métadonnées : le seul artefact de sortie contrôlé a été relu intégralement, 51 954 octets et 325 lignes réussies, sans rejouer les tests. Ces faits de pilotage ne sont pas des échecs de tests.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 828 |
| Tokens output | 70743 |
| Tokens reasoning | 0 |
| Tokens total | 29413005 |
| Tokens cache_read | 26335595 |
| Tokens cache_write | 3005839 |
| Coût SDK déclaré | 1.05591073 USD |
| Compactions OpenCode observées | 1 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| début — dimensions idempotence | 2026-10-04T21:31:28.865785+00:00 | 2026-10-04T21:31:31.394330+00:00 | 2026-10-04T21:31:35.480199+00:00 | 2.529 s | 4.086 s | 554 | 135.589/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T22:01:31.030432+00:00 | 2026-10-04T22:01:33.730105+00:00 | 2026-10-04T22:01:40.909672+00:00 | 2.700 s | 7.180 s | 521 | 72.567/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T22:31:32.111344+00:00 | 2026-10-04T22:31:34.546584+00:00 | 2026-10-04T22:31:40.898477+00:00 | 2.435 s | 6.352 s | 535 | 84.227/s | valide |
| final | 2026-10-04T22:38:26.826640+00:00 | 2026-10-04T22:38:29.454351+00:00 | 2026-10-04T22:38:35.770242+00:00 | 2.628 s | 6.316 s | 549 | 86.924/s | invalide |
| final — reprise unique après 39 lignes au lieu de40 | 2026-10-04T22:39:00.301778+00:00 | 2026-10-04T22:39:02.110191+00:00 | 2026-10-04T22:39:08.880894+00:00 | 1.808 s | 6.771 s | 511 | 75.472/s | valide |

Collecte : 5 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (80.0 %), 1 échouées (20.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 1.808/2.700 s ; débit min/max 72.567/135.589/s. Surcharge : 2670 tokens de sortie, 66970 tokens total SDK, 0.01174826 USD, 42.804 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 138 | 81.7 % |
| user | 31 | 18.3 % |
| Total | 169 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.2 % |
| reasoning | 138 | 23.4 % |
| step-finish | 138 | 23.4 % |
| step-start | 138 | 23.4 % |
| text | 66 | 11.2 % |
| tool | 108 | 18.3 % |
| Total | 589 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 31 | 18.3 % |
| stop | 31 | 18.3 % |
| tool-calls | 107 | 63.3 % |
| Total | 169 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 59 (54.6 %) | 59 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 21 (19.4 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (7.4 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 5 (4.6 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 12 (11.1 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 1 (0.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 108 (100 %) | 108 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-command-idempotency-dimensions/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-idempotency-dimensions/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-idempotency-dimensions/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-idempotency-dimensions/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-command-idempotency-dimensions/specs/interactions/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/idempotency_dimensions.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_command_idempotency_dimensions.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_command_idempotency_dimensions_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-command-idempotency-dimensions/. Aucun delta canonique effectif (+0/~0/-0). Les modules antérieurs restent byte à byte inchangés. Trois nouvelles sources/tests exactes, soixante-dix-neuf fichiers de baseline inchangés. CommandIdempotencyDimensions collecte quatre valeurs existantes après un appel au validateur public de CommandMetadata ; None PLATFORM est conservé comme donnée légale, sans clé de lookup ni politique de déduplication.

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
| /usr/bin/env -i PATH=/home/devops/.local/npm/bin:/home/devops/python/current/bin:/usr/bin:/bin LANG… | 6 (50.0 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 (100 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T21:31:28.681735+00:00 UTC |
| Fin — après archivage | 2026-10-04T22:39:08.999958+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 07 min 40 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T21:31:28.681735+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T22:39:08.999958+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 87 (80.6 %) | 87 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 9 (8.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 12 (11.1 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 108 (100 %) | 108 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Bilan : 339 tests sûrs réussis, trois compilations natives exit0 et stricts réussis, toutes tâches du change prouvées, archive contrôlée. CommandIdempotencyDimensions est structurel, frozen/slots, à quatre champs obligatoires et deux exports. Le collecteur appelle le validate_command_metadata public une seule fois avant lecture locale ; les diagnostics et leur liste traversent à l'identique, l'instance de dimensions est nouvelle. tenant_id None du contexte PLATFORM légal est conservé sans sentinelle. Aucune règle metadata/scope, aucun diagnostic, tri ou copie n'est dupliqué. Erreurs inattendues propagées à l'identique. Aucun lookup, format durable/wire, hash, sérialisation, concaténation, déduplication, rejeu/conflit effectif, rétention, persistance, autorisation ou exécution prouvés. Les sources AuditEvent/event-contract/Core/scope/identity et suites fanions/backend/PG antérieures restent inchangées ; aucun PG réel supplémentaire. Git non consulté, aucun commit/push, config, dépendance, README ou UI modifié. PLLM mode1 qwen3.8-flash xhigh conservée, processus OpenCode jamais fermé ni redémarré. Les incidents éventuels de pilotage sont distingués des résultats natifs des tests. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|
| paired-987bd6ba781548b9af4390be4b9f0769 | 2026-10-04T22:27:28.616637+00:00 | msg_109077f8a001PaBhr66AAFoLvX / 2026-10-04T22:28:50.039651+00:00 | 01a10907-7f5f-76e0-a641-d5adb1391f76 / 2026-10-04T22:33:08.083376+00:00 | RESTORED |

Compteur conjoint documenté : 1. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
