# Statistiques — run-frontend-unit-tests-in-headless-browsers

Archive : `openspec/changes/archive/2026-10-03-run-frontend-unit-tests-in-headless-browsers`. Période : 2026-10-03T07:26:03.626487+00:00 → 2026-10-03T12:39:05.323643+00:00. Six sessions de codage couvertes par leur API, aucune manquante. Sessions : `ses_eff76dc54ffetlEtfiUM7cjg63`, `ses_eff493fbfffeDd99zuSmaW065B`, `ses_eff417c77ffe2SD6Duh20hkbEl`, `ses_eff2901b4ffefhfGbgO30y155a`, `ses_efe69653bffeEf2fAEQbgGErda`, `ses_efe62c6d3ffexoBmnIDMta2p7P`. Sondes séparées ; rapport lui-même et outils de l’orchestrateur exclus des agrégats de production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go | xhigh | 2.436 s | 70.943 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex, identifiant de modèle non exporté | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version exacte, temps de génération actif et dénominateur de service non exposés : N/A. Les durées des messages comprennent des attentes/outils et ne servent pas d’estimation du temps de service. Aucun chevauchement chiffrable.

## 1. Statistiques générales et décisions

Messages : 316 (100 %). Appels d’outils : 112 (100 %). Réussis : 108 (96.4 %), refusés : 1 (0.9 %), erreurs techniques : 3 (2.7 %). Un appel terminé sans erreur est classé réussi ; cela ne prouve pas une approbation manuelle. Les appels `invalid` sont des erreurs techniques, même si l’outil de routage retourne completed.

Télémétrie de production retournée : input 1266, output 103722, reasoning 0, cache lecture 9553223, cache écriture 1289547 tokens ; coût observé 0.459700208 USD. Un message assistant interrompu reste sans fin complète ; sa télémétrie peut être incomplète. Compactions : N/A, marqueur fiable non collecté.

| Dernier état de décision observé dans une réponse MCP | Nombre | Part |
|---|---:|---:|
| APPROVED | 36 | 92.3 % |
| REJECTED | 3 | 7.7 % |
| Total des enregistrements lisibles | 39 | 100 % |

39 requestId distincts soumis et réconciliés par leurs réponses MCP : 36 APPROVED et 3 REJECTED. Les retours intermédiaires PENDING ne sont pas comptés comme décisions finales. Les timeouts MCP sont distincts des refus natifs. Readiness actuelle vérifiée READY/pending_count=0.

Résultat : Chromium 3/3 et Firefox 3/3 ; deux réponses corrélées et cleanup prouvés ; build réussi ; diagnostic Node 3/3 ; adaptateur 19 contrôles et 12 contre-exemples refusés. Neuf tâches cochées après preuves. Archive exécutée une seule fois ; canonical conserve strictement son contenu antérieur et ajoute une exigence/deux scénarios ; validation stricte testing après archive : exit 0 (`msg_101c3b16a001OUic7ghzC5sS4O`).

Incidents : délais MCP, refus de commande, erreur de cible d’édition et appel Bash masqué sans exécution ; récupérations et interruptions manuelles consignées. Fermetures/redémarrages d’OpenCode lors d’une reprise ont fait perdre l’interface au développeur. Sa règle désormais applicable interdit tout redémarrage et toute fermeture sans demande explicite en fin de session. Aucun redémarrage après cette instruction.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 104 | 32.9 % |
| assistant | 212 | 67.1 % |
| Total | 316 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 209 | 21.9 % |
| step-start | 212 | 22.2 % |
| reasoning | 212 | 22.2 % |
| step-finish | 211 | 22.1 % |
| tool | 112 | 11.7 % |
| Total | 956 | 100 % |

| Outil | Appels | Part globale | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|---:|
| cgpt-validation_request_validation | 39 | 34.8 % | 38 (97.4 %) | 0 (0.0 %) | 1 (2.6 %) |
| bash | 32 | 28.6 % | 31 (96.9 %) | 1 (3.1 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 6 | 5.4 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 24 | 21.4 % | 24 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 5 | 4.5 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 2 | 1.8 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 3 | 2.7 % | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| invalid | 1 | 0.9 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| Total | 112 | 100.0 % | 108 (96.4 %) | 1 (0.9 %) | 3 (2.7 %) |

Terminaisons assistant observées : stop=100 (47.2 %), tool-calls=111 (52.4 %), None=1 (0.5 %).

## 3. Fichiers modifiés

Tentatives d’écriture attribuables à une cible unique : éditions natives plus publications confirmées par les sorties/hash des commandes. Les déplacements d’archive sont signalés sans compter une nouvelle écriture de contenu. Le rapport actuel, les checkpoints et les artefacts régénérables ne sont pas inclus dans ce tableau.

| Chemin absolu final | Tentatives | Part | Réussies (taux) | Refusées (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-run-frontend-unit-tests-in-headless-browsers/.openspec.yaml | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-run-frontend-unit-tests-in-headless-browsers/proposal.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-run-frontend-unit-tests-in-headless-browsers/design.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-run-frontend-unit-tests-in-headless-browsers/tasks.md | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-03-run-frontend-unit-tests-in-headless-browsers/specs/testing/spec.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/test-adapter.mjs | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/assert-adapter.mjs | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/runner.html | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/tests/browser/catalog-browser.mjs | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/package.json | 2 | 14.3 % | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| /home/devops/datas/pixs/frontend/README.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/specs/testing/spec.md | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total, 12 fichiers | 14 | 100 % | 13 (92.9 %) | 0 (0.0 %) | 1 (7.1 %) |

Les cinq artefacts ont été déplacés depuis openspec/changes/run-frontend-unit-tests-in-headless-browsers/. Caches, profils jetables et dist sont hors comptage des sources. Aucune attribution de commande refusée à une écriture effectivement réalisée. AGENTS.md et DEVOPS.md sont indiqués comme gérés par le développeur ; le hash actuel AGENTS.md diffère du baseline historique, sans attribution à ce change ni correction appliquée par ce pilotage.

## 4. Commandes

| Famille | Appels | Part | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|---:|
| Python, wrappers de publication/validation | 14 | 43.8 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 5 | 15.6 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Shell builtin/diagnostic | 13 | 40.6 % | 12 (92.3 %) | 1 (7.7 %) | 0 (0.0 %) |
| Total | 32 | 100 % | 31 (96.9 %) | 1 (3.1 %) | 0 (0.0 %) |

Commandes refusées, libellé limité à 100 caractères :

| Commande | Occurrences | Part des commandes |
|---|---:|---:|
| `ls -la /home/devops/datas/pixs/frontend/tests/browser/assert-adapter.mjs` | 1 | 3.1 % |

Les wrappers Python exécutent aussi les tests npm et les diagnostics Node. Une commande refusée est comptée comme une tentative native sans effet exécuté.

## 5. Accès web

| Résultat | Nombre | Part |
|---|---:|---:|
| Approuvés/exécutés | 0 | N/A |
| Refusés | 0 | N/A |
| Erreurs | 0 | N/A |
| Total web de l’agent de codage | 0 | N/A |

Aucun webfetch/websearch ni URL visitée par le codage dans l’historique retenu. Les appels API locaux CAB/OpenCode, le loopback des tests et le transport LLM sont distincts ; historique exhaustif des outils de l’orchestrateur : N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-03T07:26:03.626487+00:00 |
| Fin — après archivage et sonde finale, avant rapport | 2026-10-03T12:39:05.323643+00:00 |
| Durée globale, pauses et attentes incluses | 05 h 13 min 01 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A — relevé natif indisponible | N/A | N/A |
| Après — après archivage | N/A — relevé natif indisponible | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : aucun relevé réel substitué. Quotas partagés par le compte ; aucune consommation exclusive ni conversion en tokens/euros supposée.

| Domaine d’outils | Appels | Part globale | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|---:|
| Commandes | 32 | 28.6 % | 31 (96.9 %) | 1 (3.1 %) | 0 (0.0 %) |
| Éditions | 3 | 2.7 % | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres, MCP/lectures/routage | 77 | 68.8 % | 75 (97.4 %) | 0 (0.0 %) | 2 (2.6 %) |
| Global | 112 | 100.0 % | 108 (96.4 %) | 1 (0.9 %) | 3 (2.7 %) |

Sondes : 5 exécutées, 2 réussies, 3 invalides/échouées ; 5 créneaux manqués explicitement consignés, jamais recréés. Plan exhaustif pendant les interruptions : N/A. Moyennes uniquement sur les 2 sondes valides ; TTMT min/max 2.069/2.804 s, débit min/max 68.137/73.749 tokens/s. Les trois sondes invalides restent visibles dans le checkpoint ; relèves tardives non présentées comme mesures faites au créneau prévu.

| Relève | Heure UTC d’envoi | Résultat | TTMT | Tokens/s |
|---|---|---|---:|---:|
| début — unités frontend deux navigateurs, avant écritures | 2026-10-03T07:26:03.694973+00:00 | valide | 2.069 s | 68.137 |
| périodique — créneau 2026-10-03T07:56:03.626512+00:00 | 2026-10-03T08:08:32.515939+00:00 | invalide | 3.211 s | N/A |
| périodique — créneau 2026-10-03T08:26:03.626512+00:00 | 2026-10-03T08:26:44.688973+00:00 | invalide | 2.101 s | N/A |
| périodique — créneau 2026-10-03T11:26:03.626512+00:00 | 2026-10-03T11:55:55.066373+00:00 | invalide | 2.062 s | N/A |
| fin après dernière tâche et archivage, avant rapport | 2026-10-03T12:38:55.275001+00:00 | valide | 2.804 s | 73.749 |

Surcharge de télémétrie disponible, séparée de la production : 1654 tokens de sortie, 0.00968258 USD ; sonde interrompue sans usage final : N/A, pas zéro supposé.

Les tests browsers/build et diagnostics sont prouvés ; aucune réexécution d’archive. Git non inspecté, aucun commit/push demandé. Aucune valeur de secret, profil personnel ou source exclue dans ce rapport. Contrôle syntaxique des trois modules et cleanup des profils/processus de test consignés. Statistiques publiées par mandat distinct après archive ; le cycle parent retourne ensuite à SÉLECTION, sans présenter ce seul change comme l’achèvement global de Pixs.

Références : six session_ids et preuves détaillées dans output/cismp-state.json, bloc frontend_headless_units_20261003 ; appel d’archive msg_101acb2e7001HjBzM6dDuhG8j0, rapport de reprise msg_101b115d0001EKpt9TCbzg4ZVg. Les pourcentages sont calculés sur le total de leur tableau ou de leur ligne et arrondis à une décimale.
