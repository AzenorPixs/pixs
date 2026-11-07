# STATISTIQUES — add-initial-job-state-vocabulary

Archive : openspec/changes/archive/2026-10-05-add-initial-job-state-vocabulary. Sessions : ses_ef7971176ffeR7zOxqw3EO7ZZB. Historique API complet borné à 2026-10-05T04:19:05.724727+00:00–2026-10-05T05:06:51.152105+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 2.285 s | 100.705 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

198 messages, 121 outils, durée calendaire 00 h 47 min 45 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 24 | 96.0 % |
| CANCELLED | 1 | 4.0 % |
| Total | 25 | 100 % |

Validation : trois compilations natives exit0 ; 3 tests unitaires JobState, 1 intégration fraîche, 339 régressions existantes, 343/343 tests réussis. Stricts précode, post-code et change post-cochage contrôlés. Six tâches cochées sur preuves. Archive +0/~0/-0/→0, canoniques inchangés.


Pilotage : artefacts courts et sources revus avant publication. Enum standard représente le vocabulaire existant ; aucune immuabilité profonde ou exécution Jobs revendiquée. La revue a retiré un test de lookup identique et corrigé le worker avant publication : bootstrap littéral, constructeurs entiers gardés, exception propre, probe dans artefact temporaire du projet, compteur getenv et cleanup/flux exacts. Ces corrections de brouillon ne sont pas des échecs de tests exécutés. Après la troisième compilation exit0, l’agent a fabriqué un échec d’intégration non exécuté et ouvert une question parasite. CGPT a rejeté cette question, interrompu le seul tour, conservé les trois compilations et empreintes exactes, puis repris les tests réellement non exécutés après READY0 natif. Aucune correction source n’a été faite sur ce faux motif ; le tool question a été désactivé pour les mandats. Une nouvelle tentative après les régressions a été convertie en outil invalid/unavailable, sans question créée ni effet ; le compteur d’erreurs SDK l’inclut. Les contrôles de référence utilisent les résultats natifs et les empreintes observées. Les compteurs directs de l’orchestrateur restent N/A faute d’historique agrégé exposé.


Le brouillon proposait initialement une archive ~1 ; CGPT l’a corrigé avant publication : le delta reste mot pour mot canonique, donc effet attendu nul. Aucun objectif de longueur, de nombre de tâches ou de tests. Un tour a répété broker_readiness read-only deux fois malgré la consigne unitaire ; le seul write natif est resté conforme. Écart consigné, sans permission hors mandat ni écriture supplémentaire. Une demande de régression de 2009 caractères dépassait la limite2000 du contrôleur et n’a jamais été exécutée. Elle a été annulée par MCP sous instruction CGPT ; le paramètre env redondant avec -B a été retiré pour une commande courte avec collection identique. READY0 et test CAB frais ont précédé la reprise sous nouvel identifiant. Les pending transitoires sont réconciliés séparément, sans répéter les effets prouvés.

Question dismissed : refus de l’outil question par CGPT en pilotage, distinct d’un refus CAB ou d’un arbitrage humain.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 954 |
| Tokens output | 41376 |
| Tokens reasoning | 0 |
| Tokens total | 26882768 |
| Tokens cache_read | 25173286 |
| Tokens cache_write | 1667152 |
| Coût SDK déclaré | 0.75579280 USD |
| Compactions OpenCode observées | 0 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale JobState Enum | 2026-10-05T04:19:05.981006+00:00 | 2026-10-05T04:19:08.296382+00:00 | 2026-10-05T04:19:12.886941+00:00 | 2.315 s | 4.591 s | 545 | 118.722/s | valide |
| périodique — horloge30minutes | 2026-10-05T04:49:08.082970+00:00 | 2026-10-05T04:49:10.106384+00:00 | 2026-10-05T04:49:16.240779+00:00 | 2.023 s | 6.134 s | 507 | 82.649/s | valide |
| finale après archive JobState | 2026-10-05T05:06:43.127054+00:00 | 2026-10-05T05:06:45.643622+00:00 | 2026-10-05T05:06:50.964030+00:00 | 2.517 s | 5.320 s | 536 | 100.744/s | valide |

Collecte : 3 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 3 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.023/2.517 s ; débit min/max 82.649/118.722/s. Surcharge : 1588 tokens de sortie, 40168 tokens total SDK, 0.00846146 USD, 22.901 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 159 | 80.3 % |
| user | 39 | 19.7 % |
| Total | 198 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 159 | 23.6 % |
| step-finish | 159 | 23.6 % |
| step-start | 159 | 23.6 % |
| text | 77 | 11.4 % |
| tool | 121 | 17.9 % |
| Total | 675 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 39 | 19.7 % |
| stop | 38 | 19.2 % |
| tool-calls | 121 | 61.1 % |
| Total | 198 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 66 (54.5 %) | 66 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 25 (20.7 %) | 24 (96.0 %) | 0 (0.0 %) | 1 (4.0 %) |
| write | 8 (6.6 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 15 (12.4 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| question | 1 (0.8 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 (1.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (0.8 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| cgpt-validation_cancel_approval | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| invalid | 1 (0.8 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| edit | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 121 (100 %) | 117 (96.7 %) | 1 (0.8 %) | 3 (2.5 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-job-state-vocabulary/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-state-vocabulary/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-state-vocabulary/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-state-vocabulary/specs/jobs/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-state-vocabulary/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/jobs.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_job_state.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_job_state_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-job-state-vocabulary/. Aucun delta normatif effectif ; les 76 canoniques et 84 fichiers de référence restent inchangés. Trois sources/tests ajoutées sous mandat, module pur JobState à neuf noms/valeurs exacts. Aucun fichier existant de code ou cadrage modifié.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 7 (46.7 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test CAB sans effet | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /usr/bin/env -i PATH=/home/devops/.local/npm/bin:/home/devops/python/current/bin:/usr/bin:/bin LANG… | 8 (53.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 5 (33.3 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src /hom… | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-05T04:19:05.724727+00:00 UTC |
| Fin — après archivage | 2026-10-05T05:06:51.152105+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 00 h 47 min 45 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-05T04:19:05.724727+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-05T05:06:51.152105+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 97 (80.2 %) | 93 (95.9 %) | 1 (1.0 %) | 3 (3.1 %) |
| Fichiers | 9 (7.4 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 15 (12.4 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 121 (100 %) | 117 (96.7 %) | 1 (0.8 %) | 3 (2.5 %) |

Bilan : seul vocabulaire JobState représenté par Enum standard, neuf états existants sans ajout normatif. Module, tests et import frais prouvés, contrôles de référence conservés. Aucune immuabilité profonde, transition, machine d’états, validation métier, diagnostic, factory ajoutée, bail, réessai, persistance, worker, autorisation ou exécution Jobs prouvé. Les exigences complètes Jobs restent non couvertes. Git non consulté, aucun commit/push, secret ou configuration source modifié. PLLM mode1 qwen3.8-flash xhigh conservée, processus OpenCode préservé pendant le codage. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|

Compteur conjoint documenté : 0. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
