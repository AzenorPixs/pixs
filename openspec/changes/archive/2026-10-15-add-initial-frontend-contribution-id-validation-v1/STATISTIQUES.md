# STATISTIQUES — add-initial-frontend-contribution-id-validation-v1

RUN cismp-pixs-01a13bac8501 ; contexte CAB 124 ; job cismp2-frontend-id-1b487d5272b0.
Sessions du change : ses_ec2476a87ffeAfFHnGVmvjbnA3, ses_ec1c499d1ffeHWUouDR2QucP6A, ses_ec17c814bffe5QTJPz5xSF26Dj.
Bornes : 2026-10-15 06:05:05 CEST → 2026-10-15 11:17:05 CEST. Le présent rapport et sa vérification sont postérieurs à la fin de collecte et exclus des agrégats de production. La RSMP précédente est exclue.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte du modèle non exposée | OpenCode Go | high | 0.869 s | 232.912 | N/A — service de tous agents non instrumenté |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex — modèle exact non exposé | N/A | OpenAI | N/A — télémétrie non exposée | N/A — non sondé | N/A — non sondé | N/A — non instrumenté |

OpenCode 1.19.0 observé. Somme partielle des intervalles natifs text/reasoning : 520.661 s, sans attente outil ou permission. Les chevauchements dans un message sont fusionnés ; couverture partielle et service de Codex absent : dénominateur tous agents et pourcentage N/A. La durée calendaire inclut les pauses et attentes.

## 1. Statistiques générales et décisions

Le brouillon déterministe CAB1.1.0 a été lu puis complété avec les historiques publics natifs des trois sessions. La collecte intégrée commence après la mise à jour et recouvre partiellement ces historiques : ne pas additionner les deux ensembles.
Messages 525 ; appels d’outils 183. Completed décrit une terminaison native, sans prouver une décision manuelle ou une réussite fonctionnelle. Refus = rejet explicite de permission ; erreur technique distincte d’un résultat de test ou OpenSpec non nul.

| États terminaux MCP distincts observés | Nombre | Part |
|---|---|---|
| APPROVED | 30 | 93.8 % |
| CANCELLED | 2 | 6.2 % |
| Total | 32 | 100.0 % |

| Décisions restaurées accessibles du contrôleur | Nombre | Part |
|---|---|---|
| Absente après maintenance — historique MCP conservé | 24 | 75.0 % |
| approved | 8 | 25.0 % |
| Total | 32 | 100.0 % |

Les 30 approbations sont observées dans les réponses terminales MCP ; les deux annulations administratives ne sont pas des refus CAB. Le contrôleur après maintenance ne restaure pas toutes les décisions historiques, dont les preuves MCP restent conservées. Les deux tableaux se recouvrent et ne s’additionnent pas. Une approbation CAB peut être suivie d’un refus de permission native divergente ; les deux compteurs ont des dénominateurs différents.
Tokens exposés : total 20431281, input 3075450, output 78708, reasoning 28910, cache read 17248213, cache write 0. Ces champs suivent la convention native et ne sont pas additionnés arbitrairement. Coût natif rapporté 0.36356503 ; devise/facturation réelle de l’abonnement N/A.

Résultats : 3 compilations séparées exit0 ; 9 tests unitaires, 1 intégration fraîche sous gardes et 10 régressions, tous exit0 sans skip. Strict ciblé préparatoire et post-code exit0/issues[]. Global standard exit0 ; global strict avant/après archive exit1, quatre WARNING préexistants de longueur, zéro ERROR, aucune nouvelle issue. Ce résultat non nul n’est pas déclaré réussite stricte.
| Spec | Chemin natif | Issue |
|---|---|---|
| bulk-operations | requirements[6] | WARNING historique : texte d’exigence >500 caractères ; diagnostic intégral dans le checkpoint |
| bulk-operations | requirements[10] | WARNING historique : texte d’exigence >500 caractères ; diagnostic intégral dans le checkpoint |
| bulk-operations | requirements[13] | WARNING historique : texte d’exigence >500 caractères ; diagnostic intégral dans le checkpoint |
| identity-assurance | requirements[4] | WARNING historique : texte d’exigence >500 caractères ; diagnostic intégral dans le checkpoint |

Incidents tracés : summary LF non admis puis annulation administrative ; commande de test à quoting divergent refusée avant exécution ; deux transferts contrôlés de session, sources et tests conservés ; notification strictpost non admise puis annulée. Refus de revue automatique côté orchestrateur résolus après preuves : comptage exhaustif N/A, distinct des permissions natives. Première demande FIFO après maintenance retirée car bloquant le prévol C1, puis réinscrite après prévols de la cohorte ; aucun effet ni exclusion pendant la première file.
Maintenance humaine : 2026-10-15 10:01:06 CEST → 2026-10-15 10:50:11 CEST. Aucun service commun arrêté par C2. Compactages natifs prouvés dans le checkpoint ; API de compactage Codex absente, cycles communs partiels conservés.

### Sondes de performance

Prompt constant de 100 lignes, sessions jetables sans outil/source/navigation. TTMT = premier événement natif généré non vide (texte ou raisonnement) ; SSE client non instrumenté. Débit réponse seule ; moyennes arithmétiques sur seules sondes valides, distinctes des benchmarks PLLM globaux.
| Position | État | TTMT(s) | Tokens/s réponse | Tokens sortie |
|---|---|---|---|---|
| début FrontendContributionId v1 | failed | 1.546 | 295.508 | 1000 |
| début FrontendContributionId v1 tentative2 | success | 0.691 | 238.250 | 1024 |
| +30 min FrontendContributionId (retard repriseCAB tracé) | failed | 9.667 | 436.833 | 1065 |
| +60 min FrontendContributionId | success | 1.020 | 293.509 | 1022 |
| +90 min FrontendContributionId (retard écritures tracé) | success | 0.684 | 204.740 | 1028 |
| fin FrontendContributionId v1 après archive et strictpost | success | 1.082 | 195.150 | 1022 |

| Relève manquée | Mesures | Cause |
|---|---|---|
| 2026-10-15 08:16:40 CEST | N/A | Permissioncommande divergente refusée etrécupérationprévolréservé ; aucunsondependantgel |
| 2026-10-15 08:46:40 CEST | N/A | ExclusionC3 puisréconciliationet revueactualisationDEVOPS ; pasdereconstruction |
| 2026-10-15 09:16:40 CEST | N/A | Reprise transport puis pause maintenance CAB et prévol de reprise ; aucune reconstruction rétroactive |
| 2026-10-15 09:46:40 CEST | N/A | Reprise transport puis pause maintenance CAB et prévol de reprise ; aucune reconstruction rétroactive |
| 2026-10-15 10:16:40 CEST | N/A | Reprise transport puis pause maintenance CAB et prévol de reprise ; aucune reconstruction rétroactive |
| 2026-10-15 10:46:40 CEST | N/A | Reprise transport puis pause maintenance CAB et prévol de reprise ; aucune reconstruction rétroactive |

Relèves prévues documentées 11 ; réussies 4 ; échouées sans réussite 1 ; manquées 6. Une tentative initiale supplémentaire échouée puis retentée une fois est conservée : 6 tentatives, 2 échecs techniques/contrat. Aucune reconstruction rétroactive.
TTMT min/max 0.684/1.082 s ; débit min/max 195.150/293.509. Surcharge sondes séparée de la production : 8822 tokens générés exposés ; durée partielle des réponses 54.296 s ; facturation réelle N/A.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part |
|---|---|---|
| assistant | 299 | 57.0 % |
| user | 226 | 43.0 % |
| Total | 525 | 100.0 % |

| Type de partie | Nombre | Part |
|---|---|---|
| compaction | 4 | 0.3 % |
| reasoning | 306 | 19.7 % |
| step-finish | 299 | 19.3 % |
| step-start | 299 | 19.3 % |
| text | 462 | 29.7 % |
| tool | 183 | 11.8 % |
| Total | 1553 | 100.0 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| stop | 171 | 57.2 % |
| tool-calls | 128 | 42.8 % |
| Total | 299 | 100.0 % |

| Outil | Total | Part | Terminé réussi | Refusé | Erreur technique | En cours |
|---|---|---|---|---|---|---|
| bash | 22 | 12.0 % | 21 (95.5 %) | 1 (4.5 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 15 | 8.2 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 30 | 16.4 % | 30 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 0.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 2 | 1.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 15 | 8.2 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 0.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 5 | 2.7 % | 1 (20.0 %) | 0 (0.0 %) | 4 (80.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 32 | 17.5 % | 27 (84.4 %) | 0 (0.0 %) | 5 (15.6 %) | 0 (0.0 %) |
| glob | 11 | 6.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 39 | 21.3 % | 39 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 2 | 1.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 4.4 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 183 | 100.0 % | 173 (94.5 %) | 1 (0.5 %) | 9 (4.9 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives Write/Edit seulement ; chemins absolus complets. Les créations par CLI et déplacements d’archive sont distincts.
| Fichier | Total | Part | Terminé réussi | Refusé | Erreur technique | En cours |
|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-id-validation-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-id-validation-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-id-validation-v1/specs/frontend/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-id-validation-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/frontend_contribution_ids.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_frontend_contribution_id_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_frontend_contribution_id.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |

La métadonnée .openspec.yaml a été créée par CLI autorisée, sans édition manuelle. Les cinq artefacts ont été déplacés dans /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-frontend-contribution-id-validation-v1. Les trois sources Python conservent leur emplacement. STATISTIQUES.md est une publication distincte après la borne, exclue des totaux. Canon frontend, TECHNICAL.md et fichiers partagés inchangés pendant ce change ; note RSMP antérieure exclue.

## 4. Commandes

| Famille | Total | Part | Terminé réussi | Refusé | Erreur technique | En cours |
|---|---|---|---|---|---|---|
| OpenSpec | 10 | 45.5 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol /usr/bin/true | 5 | 22.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python syntaxe | 3 | 13.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python tests | 4 | 18.2 % | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 22 | 100.0 % | 21 (95.5 %) | 1 (4.5 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande (100 caractères max) | Issue native | Exit natif |
|---|---|---|
| /usr/bin/true | réussi | 0 |
| /home/devops/.local/npm/bin/openspec new change --help | réussi | 0 |
| /home/devops/.local/npm/bin/openspec new change add-initial-frontend-contribution-id-validation-v1 … | réussi | 0 |
| /usr/bin/true | réussi | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-frontend-contribution-id-validation-v1 --… | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m py_compile src/pixs/kernel/frontend_contribution… | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m py_compile tests/unit/test_frontend_contribution… | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m py_compile tests/integration/test_frontend_contr… | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys sys.path[:0] = ["src", "."] import u… | refusé | N/A — non exécutée ou absent |
| /usr/bin/true | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys sys.path[:0] = sys.argv[1:3] import … | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys sys.path[:0] = sys.argv[1:3] import … | réussi | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys sys.path[:0] = sys.argv[1:3] import … | réussi | 0 |
| /home/devops/.local/npm/bin/openspec --version | réussi | 0 |
| /usr/bin/true | réussi | 0 |
| /usr/bin/true | réussi | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-frontend-contribution-id-validation-v1 --… | réussi | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --json | réussi | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | réussi | 1 |
| /home/devops/.local/npm/bin/openspec archive --help | réussi | 0 |
| /home/devops/.local/npm/bin/openspec archive add-initial-frontend-contribution-id-validation-v1 --y… | réussi | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | réussi | 1 |

| Commandes refusées regroupées | Occurrences | Part des refus |
|---|---|---|
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys sys.path[:0] = ["src", "."] import u… | 1 | 100.0 % |

Une commande refusée avant création du processus ne devient pas un test exécuté. Les codes stricts OpenSpec1 et leurs WARNING sont conservés, distincts des refus de permission.

## 5. Accès web

| Accès web natifs | Total | Part | Terminé réussi | Refusé | Erreur technique | En cours |
|---|---|---|---|---|---|---|
| web | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web du codeur observé : aucune visite déduite d’une requête. Communications techniques distinctes : loopback CAB/OpenCode, benchmark/authentification PLLM autorisés vers https://opencode.ai/zen/go/v1/usage et https://opencode.ai/zen/go/v1/responses. Aucun secret reproduit. Les requêtes fournisseur du runtime ne sont pas instrumentées comme navigation du codeur.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-15 06:05:05 CEST |
| Fin — après archivage | 2026-10-15 11:17:05 CEST |
| Durée globale (pauses et attentes incluses) | 05 h 11 min 59 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A — heure native non conservée ; capture avant début ci-dessus | 33 % | 2026-10-20 06:59:31 CEST |
| Après — après archivage de la spécification | 2026-10-15 11:17:05 CEST | 4 % | 2026-10-22 08:12:56 CEST |
| Différence après − avant | — | N/A — Même compte vérifié, mais horodatage de réinitialisation différent et différence négative ; nouvelle fenêtre non comparable, aucune consommation reconstruite | — |

Source native get_usage_limits, entrée codex/fenêtre10080min ; compte/fenêtre comparés uniquement si identifiables. Quota partagé : variation pouvant inclure les autres tâches, pauses et maintenance, sans attribution exclusive à C2, conversion tokens/euros ni ventilation entre RUN.
| Domaine global | Total | Part | Terminé réussi | Refusé | Erreur technique | En cours |
|---|---|---|---|---|---|---|
| autres | 153 | 83.6 % | 144 (94.1 %) | 0 (0.0 %) | 9 (5.9 %) | 0 (0.0 %) |
| commandes | 22 | 12.0 % | 21 (95.5 %) | 1 (4.5 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 4.4 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 183 | 100.0 % | 173 (94.5 %) | 1 (0.5 %) | 9 (4.9 %) | 0 (0.0 %) |

Archive unique réussie, cinq artefacts déplacés et trois sources Python conservées ; aucune synchronisation canon (delta exactement identique aux deux exigences/trois scénarios validés). Rapport distinct à vérifier avant gate/désarmement/livraison. Git non inspecté, aucun commit/push. Aucun secret lu par les agents ou transmis au modèle ; seul le processus sécurisé PLLM a consommé l’authentification fournisseur autorisée sans copie ni journalisation.

### Couverture des statistiques intégrées CAB1.1.0

Snapshot complémentaire du contrôleur lu après la borne de production. Il peut inclure la clôture technique postérieure et ne doit pas être additionné aux totaux natifs ci-dessus. Les bornes de production, tokens et outils restent figées au relevé final.
Version 1.1.0 ; début intégré 2026-10-15T08:05:20.851Z ; dernière observation 2026-10-15T09:22:18.549Z ; persistance {'status': 'READY', 'cause': None, 'writes': 923}. Busy ne prouve pas du codage productif. Conditions concurrentes susceptibles de se recouvrir, sans addition ni gain causal. Les quantiles portent sur les dernières2048observations au plus ; les détails intégrés et natifs sont conservés dans le checkpoint.

| Contexte124 intégré | Valeur |
|---|---|
| reservedMs | 4617.677 s |
| busyMs | 602.551 s |
| idleMs | 4015.102 s |
| nativeUnknownMs | 0.024 s |
| integrationMs | 752.572 s |
| queueMs | 870.315 s |
| staleMs | 0.000 s |

| Décisions intégrées — sous-fenêtre1.1.0 | Nombre | Part |
|---|---|---|
| approved | 8 | 100.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| rejected | 0 | 0.0 % |
| Total | 8 | 100.0 % |

| Latence intégrée | Nombre | Moyenne(s) | Médiane(s) | p95(s) |
|---|---|---|---|---|
| requestToDecision | 8 | 27.371 | 18.920 | 51.779 |
| decisionToOnce | 8 | 5.909 | 4.406 | 14.577 |
| nativeTool | 56 | 4.728 | 0.588 | 37.898 |

Permissions once intégrées : 8 ; erreurs techniques intégrées : 0. Ce sous-ensemble n’est pas ajouté aux états MCP historiques. Durées queue/exclusion/stale peuvent se recouvrir ; aucun temps de service modèle n’en est déduit.
Preuves non secrètes : /home/devops/datas/pixs/output/cismp/cismp-pixs-01a13bac8501/state.json. Ce checkpoint n’est pas une source de vérité normative.
