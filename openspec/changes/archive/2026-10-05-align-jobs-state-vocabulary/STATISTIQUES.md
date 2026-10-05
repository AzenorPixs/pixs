# STATISTIQUES — align-jobs-state-vocabulary

Archive : openspec/changes/archive/2026-10-05-align-jobs-state-vocabulary. Sessions : ses_ef7971176ffeR7zOxqw3EO7ZZB. Historique API complet borné à 2026-10-05T03:44:57.254072+00:00–2026-10-05T04:11:48.172680+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 2.980 s | 109.197 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

105 messages, 68 outils, durée calendaire 00 h 26 min 50 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 13 | 100.0 % |
| Total | 13 | 100 % |

Validation documentaire : stricts du change, des spécifications et de tous les éléments exécutés avec résultat natif contrôlé ; validation du change après preuve des quatre tâches. Tests runtime et compilations N/A : aucun fichier de code modifié, reprise uniquement normative et documentaire. Archive réussie : +0/~1/-0, jobs seul.


Pilotage : deux contextes réconciliés après compactage conjoint natif paired-a0d53c1642d14aa590140d6bfdc73c0e, sans rejeu du change de dimensions déjà archivé. CAB réel READY pending0 et test de reprise réussi avant le cycle. Arrêt de codage prévu le 2026-10-05 à 07h30 Europe/Paris sur instruction explicite ; ce rapport précède cet arrêt.


Les comptes OpenSpec reposent sur les résultats réellement observés. Un appel list_pending puis des contrôles broker_readiness ont expiré après la première écriture. Le driver et les seuls tours ont été arrêtés ; le fichier exact et son outil natif ont été conservés sans rejeu. La reconnexion MCP puis le dispose du seul contexte ont préservé le processus OpenCode. Après sortie de l’ancien enfant, le nouveau broker a été observé en réconciliation CPU ; les lectures privées n’ont concerné aucun contenu. Les erreurs MCP observées figurent dans les compteurs SDK, sans être assimilées à des refus ou à des tests runtime.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 492 |
| Tokens output | 16907 |
| Tokens reasoning | 0 |
| Tokens total | 5093465 |
| Tokens cache_read | 4783257 |
| Tokens cache_write | 292809 |
| Coût SDK déclaré | 0.14311400 USD |
| Compactions OpenCode observées | 0 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale RSMP Jobs | 2026-10-05T03:45:40.155663+00:00 | 2026-10-05T03:45:43.255770+00:00 | 2026-10-05T03:45:49.020381+00:00 | 3.100 s | 5.765 s | 520 | 90.206/s | valide |
| finale après archivage RSMP Jobs | 2026-10-05T04:11:40.482087+00:00 | 2026-10-05T04:11:43.342123+00:00 | 2026-10-05T04:11:47.882341+00:00 | 2.860 s | 4.540 s | 582 | 128.188/s | valide |

Collecte : 2 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 2 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.860/3.100 s ; débit min/max 90.206/128.188/s. Surcharge : 1102 tokens de sortie, 26822 tokens total SDK, 0.00566134 USD, 16.265 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 84 | 80.0 % |
| user | 21 | 20.0 % |
| Total | 105 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 83 | 23.3 % |
| step-finish | 82 | 23.0 % |
| step-start | 83 | 23.3 % |
| text | 40 | 11.2 % |
| tool | 68 | 19.1 % |
| Total | 356 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 23 | 21.9 % |
| stop | 19 | 18.1 % |
| tool-calls | 63 | 60.0 % |
| Total | 105 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 35 (51.5 %) | 31 (88.6 %) | 0 (0.0 %) | 4 (11.4 %) |
| read | 5 (7.4 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 13 (19.1 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 5 (7.4 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 (1.5 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| invalid | 1 (1.5 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| bash | 6 (8.8 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 2 (2.9 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 68 (100 %) | 62 (91.2 %) | 0 (0.0 %) | 6 (8.8 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; aucune compilation dans ce cycle documentaire.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/align-jobs-state-vocabulary/proposal.md | 1 (14.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/align-jobs-state-vocabulary/design.md | 1 (14.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/align-jobs-state-vocabulary/.openspec.yaml | 1 (14.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/align-jobs-state-vocabulary/specs/jobs/spec.md | 1 (14.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/align-jobs-state-vocabulary/tasks.md | 2 (28.6 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/BUILD.md | 1 (14.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 7 (100 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

6 chemins uniques. Cinq artefacts déplacés par archivage dans /home/devops/datas/pixs/openspec/changes/archive/2026-10-05-align-jobs-state-vocabulary/. Canonique Jobs modifié uniquement par les deux insertions SUCCEEDED et PAUSED ; BUILD.md modifié par ces mêmes insertions. Scénario inchangé. 82 fichiers de référence inchangés, TECHNICAL.md conservé. Aucun code, transition ni comportement runtime implémenté.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Test CAB sans effet | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 4 (66.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 6 (100 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /usr/bin/true | 1 (16.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/.local/npm/bin:/home/devops/python/current/bin:/usr/bin:/bin LANG… | 5 (83.3 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 6 (100 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-05T03:44:57.254072+00:00 UTC |
| Fin — après archivage | 2026-10-05T04:11:48.172680+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 00 h 26 min 50 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-05T03:44:57.254072+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-05T04:11:48.172680+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 55 (80.9 %) | 49 (89.1 %) | 0 (0.0 %) | 6 (10.9 %) |
| Fichiers | 7 (10.3 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 6 (8.8 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 68 (100 %) | 62 (91.2 %) | 0 (0.0 %) | 6 (8.8 %) |

Bilan : vocabulaire neuf états aligné dans Jobs et BUILD uniquement, quatre tâches prouvées et cochées, validations strictes réussies et archive contrôlée. Aucun test runtime ni compilation exécuté pour cette correction documentaire sans code ; aucune persistance, transition, exécution ou reprise effective revendiquée. Git non consulté, aucun commit/push, secret ou configuration modifié. PLLM mode1 qwen3.8-flash xhigh conservée. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|

Compteur conjoint documenté : 0. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
