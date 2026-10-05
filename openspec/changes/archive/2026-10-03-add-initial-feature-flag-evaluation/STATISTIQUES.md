# STATISTIQUES — add-initial-feature-flag-evaluation

Archive : openspec/changes/archive/2026-10-03-add-initial-feature-flag-evaluation. Session : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-03T18:47:46.473569+00:00–2026-10-03T19:31:59.359844+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.298 s | 98.101 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

131 messages, 85 outils, durée calendaire 00 h 44 min 12 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 20 | 100.0 % |
| Total | 20 | 100 % |

Développement : compilation exit 0 ; 15 nouveaux tests unitaires, 1 intégration fraîche et 45 régressions, 61/61 réussis (100 %). Trois stricts réussis et un strict initial en échec (75,0 % / 25,0 %) à cause de six numéros de tâches incohérents ; correction ciblée sous nouveau mandat, pas de changement normatif. Huit cases cochées après preuves. Archivage exit 0 sans avertissement, canonical feature-flags inchangé. Les transitoires pending_count 1 après certaines opérations ont été réconciliés sans répéter l’effet observé. Les quatre corrections des brouillons de code ont précédé toute publication.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 648 |
| Tokens output | 66070 |
| Tokens reasoning | 0 |
| Tokens total | 34798684 |
| Tokens cache_read | 34615578 |
| Tokens cache_write | 116388 |
| Coût SDK déclaré | 0.60827695 USD |
| Compactions OpenCode observées | 0 |
| Compactions orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Les horodatages absolus SSE n’avaient pas été conservés pour les deux premières relèves ; TTMT et durée premier–dernier sont mesurés, pas reconstruits. La relève finale conserve les deux horodatages.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| début — résolution pure avant artefacts | 2026-10-03T18:47:46.630997+00:00 | N/A — relatif seul | N/A — relatif seul | 2.579 s | 4.918 s | 507 | 103.082/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-03T19:17:47.917637+00:00 | N/A — relatif seul | N/A — relatif seul | 2.795 s | 6.675 s | 515 | 77.149/s | valide |
| fin — après archivage vérifié, avant statistiques | 2026-10-03T19:31:50.076329+00:00 | 2026-10-03T19:31:54.595425+00:00 | 2026-10-03T19:31:59.188963+00:00 | 4.519 s | 4.594 s | 524 | 114.073/s | valide |

Collecte : 3 relèves comptabilisées, 3 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.579/4.519 s ; débit min/max 77.149/114.073/s. Surcharge : 1546 tokens de sortie, 40126 tokens total SDK, 0.00844172 USD, 26.081 s d’intervalle envoi–dernier événement (pas durée active).

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 108 | 82.4 % |
| user | 23 | 17.6 % |
| Total | 131 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 108 | 23.6 % |
| step-finish | 108 | 23.6 % |
| step-start | 108 | 23.6 % |
| text | 48 | 10.5 % |
| tool | 85 | 18.6 % |
| Total | 457 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 23 | 17.6 % |
| stop | 23 | 17.6 % |
| tool-calls | 85 | 64.9 % |
| Total | 131 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 40 (47.1 %) | 40 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 20 (23.5 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 (8.2 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 9 (10.6 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| read | 5 (5.9 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 4 (4.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 85 (100 %) | 84 (98.8 %) | 0 (0.0 %) | 1 (1.2 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-evaluation/.openspec.yaml | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-evaluation/proposal.md | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-evaluation/design.md | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-evaluation/tasks.md | 3 (27.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-evaluation/specs/feature-flags/spec.md | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flags.py | 2 (18.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_evaluation.py | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_evaluation_integration.py | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 (100 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-initial-feature-flag-evaluation/. Aucun delta canonique effectif (+0/~0/-0). Anciennes classes et fonctions R1/C1a byte à byte conservées ; exports anciens dans le même ordre. Trois sources exactes, dix autres fichiers de baseline inchangés. Aucune affectation runtime réelle dans le module.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 4 (44.4 %) | 3 (75.0 %) | 0 (0.0 %) | 1 (25.0 %) |
| Compilation Python | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (33.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-evaluation --strict | 4 (44.4 %) | 3 (75.0 %) | 0 (0.0 %) | 1 (25.0 %) |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/feature_flags.py tests/unit/t… | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (33.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-evaluation --yes | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |

Commandes refusées : aucune. L’échec du strict initial est une erreur technique exit 1 après approbation, pas un refus CAB. Le strict a été rejoué avec un nouveau requestId après correction.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-03T18:47:46.473569+00:00 UTC |
| Fin — après archivage | 2026-10-03T19:31:59.359844+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 00 h 44 min 12 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-03T18:47:46.473569+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-03T19:31:59.359844+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 65 (76.5 %) | 65 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 11 (12.9 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 9 (10.6 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 85 (100 %) | 84 (98.8 %) | 0 (0.0 %) | 1 (1.2 %) |

Bilan : 61 tests réussis, compilation réussie, strict corrigé réussi avant code/après preuves/après cochage, huit tâches prouvées, archive contrôlée. R2 complète, cohorte/prérequis/repli, persistance/administration/audit et non-embarquement restent non livrés. Git non consulté, aucun commit/push de ce cycle ; aucune DB ni modification UI, aucun test navigateur applicable. Authentification mode 2 comparée en processus dédié sans sortie sensible ni fichier. OpenCode jamais fermé ni redémarré par ce cycle. Aucune valeur sensible dans le rapport. Parent CISMP retourne à SÉLECTION après relecture de ce rapport.
