# STATISTIQUES — add-initial-feature-flag-assignments

Archive : `2026-10-03-add-initial-feature-flag-assignments`. Session : `ses_efe62c6d3ffexoBmnIDMta2p7P`. Intervalle de production : 2026-10-03T13:46:45.165596+00:00 à 2026-10-03T18:31:49.031704+00:00, UTC. Historique API OpenCode complet filtré par ces bornes ; rapport lui-même exclu. Le parent CISMP reste ouvert après ce change.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte non fournie | opencode-go | xhigh | 3.844 s | 118.253 | N/A — durées actives absentes |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — identifiant exact non télémétré | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Les moyennes du codeur utilisent les quatre sondes valides, hors production. Le dénominateur du temps de service cumulé et les chevauchements actifs sont inconnus ; aucune durée calendaire ou attente CAB n'est assimilée à une génération. OpenCode 1.18.34 est la version du logiciel, pas du modèle.

## 1. Statistiques générales et décisions

Durée calendaire : 04 h 45 min 03 s, pauses, attentes, tests et archivage inclus. 132 messages ; 85 appels d'outils. Convention : un outil terminé avec succès constitue une exécution observée ; il ne prouve pas seul une approbation manuelle. Les mandats CAB sont corrélés séparément par requestId. Un refus explicite diffère d'une erreur technique ou d'une expiration sans exécution.

Décisions CAB finales uniques observées

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 18 | 94.7 % |
| EXPIRED | 1 | 5.3 % |
| Total | 19 | 100 % |

18 opérations natives autorisées et exécutées : neuf écritures et neuf commandes. Le mandat YAML expiré n’a exécuté aucune écriture et a été remplacé par un identifiant inédit. Quatre erreurs techniques MCP : request_validation, poll_approval, list_pending et broker_readiness (délais dépassés), aucune exécution native échouée.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 648 |
| Tokens output | 53747 |
| Tokens reasoning | 0 |
| Tokens total | 18543904 |
| Tokens cache_read | 16190235 |
| Tokens cache_write | 2299274 |
| Coût SDK déclaré | 0.74425685 USD |
| Compactions OpenCode observées | 0 |
| Compactions de l’orchestrateur | N/A — compteur non exposé |

Résultats : compilation exit 0 ; 19 tests unitaires nouveaux, 1 intégration nouvelle et 25 tests R1, tous réussis (45/45, 100 %). Trois validations OpenSpec strictes réussies ; neuf tâches cochées après preuves. Archivage exit 0, avertissement non bloquant sur les en-têtes anglais attendus de proposal.md ; spécification canonique inchangée, hash contrôlé.

Sondes hors production : prompt constant de 40 lignes, même modèle/fournisseur/xhigh, sessions jetables sans outil, effacées après relève. Version précise absente.

| Position | Envoi UTC | TTMT | Premier événement après envoi | Durée premier–dernier | Tokens sortie | Débit | Résultat |
|---|---|---:|---:|---:|---:|---:|---|
| début — affectations déclaratives, avant écritures | 2026-10-03T13:49:22.204160+00:00 | 5.837 s | +5.837115 s | 4.135032 s | 758 | 183.312/s | valide |
| périodique — relève réelle après frontière sûre, créneau antérieur manqué | 2026-10-03T14:44:43.096828+00:00 | 2.606 s | +2.606006 s | 5.215372 s | 498 | 95.487/s | valide |
| périodique — relève réelle après publication du module | 2026-10-03T15:17:38.736399+00:00 | 4.513 s | +4.512908 s | 6.047059 s | 597 | 98.726/s | valide |
| fin — archivage contrôlé avant rapport | 2026-10-03T18:31:40.840562+00:00 | 2.421 s | +2.420654 s | 5.560893 s | 531 | 95.488/s | valide |

Collecte : 4 réussites, 0 échec et 7 créneaux manqués ; 11 relèves comptabilisées (36.4 % réussies). La cadence demandée n'a pas été respectée partout. Dates manquées UTC : 2026-10-03T14:19:22.204160+00:00; 2026-10-03T15:47:38.736399+00:00; 2026-10-03T16:17:38.736399+00:00; 2026-10-03T16:47:38.736399+00:00; 2026-10-03T17:17:38.736399+00:00; 2026-10-03T17:47:38.736399+00:00; 2026-10-03T18:17:38.736399+00:00. Aucune mesure rétroactive.

TTMT min/max : 2.421/5.837 s ; débit min/max : 95.487/183.312 tokens/s. Surcharge : 2384 tokens de sortie, 0.01140728 USD, 36.335 s d'intervalle envoi–dernier événement (pas un temps actif de génération).

## 2. Types de messages et d’outils

Messages par rôle

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 108 | 81.8 % |
| user | 24 | 18.2 % |
| Total | 132 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 108 | 23.6 % |
| step-finish | 108 | 23.6 % |
| step-start | 108 | 23.6 % |
| text | 48 | 10.5 % |
| tool | 85 | 18.6 % |
| Total | 457 | 100 % |

Terminaisons des messages (user inclus sous N/A)

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 24 | 18.2 % |
| stop | 23 | 17.4 % |
| tool-calls | 85 | 64.4 % |
| Total | 132 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 38 (44.7 %) | 37 (97.4 %) | 0 (0.0 %) | 1 (2.6 %) |
| cgpt-validation_request_validation | 19 (22.4 %) | 18 (94.7 %) | 0 (0.0 %) | 1 (5.3 %) |
| bash | 9 (10.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 4 (4.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (1.2 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| write | 9 (10.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 (1.2 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| read | 4 (4.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 85 (100 %) | 81 (95.3 %) | 0 (0.0 %) | 4 (4.7 %) |

## 3. Fichiers modifiés

Tentatives natives d’écriture, et non nombre de fichiers uniques : neuf écritures réussies sur huit chemins. Le rapport présent est hors intervalle.

Écritures observées

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-assignments/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-assignments/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-assignments/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-assignments/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-assignments/specs/feature-flags/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flags.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_assignments.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_assignments_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

La commande d’archive a déplacé les cinq artefacts vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-add-initial-feature-flag-assignments/. Aucun delta canonique effectif (+0, ~0, -0). Les versions du module et des deux nouvelles suites sont exactes ; les tests R1 et huit fichiers de référence restent identiques aux empreintes initiales. Artefacts py_compile régénérables exclus du décompte des écritures source.

## 4. Commandes

Commandes par famille

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Précontrôle CAB (true) | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 3 (33.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (33.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères (préfixes tronqués identiques regroupés ; commandes exactes dans les mandats)

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| true | 1 (11.1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-assignments --strict | 3 (33.3 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/feature_flags.py tests/unit/t… | 1 (11.1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (33.3 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-assignments --yes | 1 (11.1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 9 (100 %) | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Commandes refusées : aucune (0/9, 0,0 %). Neuf sorties natives exit 0 ; aucune commande rejouée sous un mandat consommé.

## 5. Accès web

Aucun appel webfetch/websearch dans la session de production : 0 accès approuvé, 0 refusé, 0 erreur ; parts et taux N/A, dénominateur zéro. Aucune URL visitée à lister. Les API locales de pilotage et les appels du fournisseur LLM sont du transport, pas des visites web du codeur ; leur coût réseau détaillé est N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-03T13:46:45.165596+00:00 UTC |
| Fin — après archivage | 2026-10-03T18:31:49.031704+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 04 h 45 min 03 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-03T13:46:45.165596+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-03T18:31:49.031704+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits non exposé : compte, fenêtre codex/10080 minutes et réinitialisation non vérifiables. Aucune substitution par le quota OpenCode. Les quotas Codex sont partagés ; aucune variation ne peut être attribuée à ce change.

Total des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 67 (78.8 %) | 63 (94.0 %) | 0 (0.0 %) | 4 (6.0 %) |
| Commandes | 9 (10.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 9 (10.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 85 (100 %) | 81 (95.3 %) | 0 (0.0 %) | 4 (4.7 %) |

Bilan : 45 tests réussis, compilation et trois contrôles stricts réussis, archivage constaté et vérifié. Git non consulté et aucun commit/push réalisé par ce cycle. Aucun outil web ; aucune valeur sensible incluse dans le rapport. Authentification existante contrôlée uniquement par comparaison en processus dédié, sans sortie sensible ni redémarrage OpenCode. Le change sera clos après vérification de ce rapport ; le parent CISMP poursuivra la sélection.
