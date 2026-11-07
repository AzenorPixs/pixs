# Statistiques de session — add-initial-data-outbound-declaration

- run_id : `cismp-pixs-20261007-061019` ; session : `ses_eeb040777ffeOEz0loy7R2EtC0` ; archive : `openspec/changes/archive/2026-10-07-add-initial-data-outbound-declaration` ; message de début : `msg_115219e97001s8D2EOzi8rB1lp`.
- Périmètre : JOB 1 lecture seule, puis préparation, implémentation, correction, validations et archivage de ce change ; seules les bornes closes ci-dessous sont comptées, aucun comptage antérieur, aucune écriture ni rédaction future du rapport.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash / qwen3.8-flash | N/A (absente de la télémétrie) | opencode-go | xhigh | 3,4583 s | 92,48 | N/A — durées de réponses mêlent génération, outils et attentes ; chevauchement avec les sondes ; OpenCode 1.18.34 |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex /root (famille GPT-6 déclarée par plateforme) | N/A | OpenAI | N/A | N/A | N/A | N/A — historique natif du thread tronqué, télémétrie modèle indisponible |

## 1. Statistiques générales et décisions

Durée calendaire (pauses, attentes CAB, tests, échec/corrections et archivage inclus) : 01 h 06 min 55,988 s. Bornes : début 2026-10-07T06:51:27.255Z ; activation native de la collecte 2026-10-07T06:56:16.932217Z ; fin après archivage 2026-10-07T07:58:23.243Z. Le temps de service des agents n'est pas la durée calendaire.

| Mesure générale | Valeur | Part |
|---|---:|---:|
| Messages totaux | 163 | 100 % |
| — user | 36 | 22,1 % |
| — assistant | 127 | 77,9 % |
| Décisions CAB explicites | 30 | 100 % |
| — APPROVED | 30 | 100,0 % |
| — REJECTED | 0 | 0,0 % |
| — needs_clarification | 0 | 0,0 % |
| reviewer | Codex /root | — |

Tokens de production : input 762, output 65 955, reasoning 0, cache_read 26 292 385, cache_write 124 057 ; coût 0,476603 (devise N/A — non publiée par la télémétrie). Compactions : N/A (non fournies). Erreurs techniques d'appels d'outils : 5 sur 100 (lecture, transport MCP et schéma tracés en notes).

Résultats de développement : 46 tests finaux réussis (unitaires 14 : 30,4 % ; intégration 1 : 2,2 % ; régression bornée 31 : 67,4 %, dénominateur 46) ; 92 exécutions de tests au total (100 %), 91 réussites (98,9 %), 1 échec initial (1,1 %) (garde lexicale de pureté) corrigé sous trois éditions ciblées, régressions rejouées 31 OK ; 5 compilations exit 0 sur 3 fichiers (3 initiales + 2 après corrections) ; 4 stricts pré/post-code exit 0 ; globaux exit 1 natifs réels qualifiés (couverture 76/77, 19 WARNING, 0 ERROR) ; 127 empreintes de baseline contrôlées, dérive 0 ; 3 sources nouvelles vérifiées sha256 exactes UTF-8/LF ; aucune garde ni spec canonique affaiblie.

### Sondes TTMT et débit de l'agent de codage

| Position | Tentative | Valide | Lignes | Tokens | TTMT (s) | Tokens/s | Coût |
|---|---:|---|---:|---:|---:|---:|---:|
| début | 1 | non | 3 | 106 | 4,1913 | 1339466,36 (valeur brute invalide, exclue) | 0,002176 |
| début | 2 | non | 1 | 370 | 10,4303 | 2181,74 | 0,000345 |
| +30 min | 1 | non | 1 | 27 | 2,6326 | N/A (durée premier=dernier token nulle) | 0,002139 |
| +30 min | 2 | non | 32 | 17127 | N/A | N/A | 0,008221 |
| +60 min | 1 | non | 40 | 197 | 2,8369 | 151,75 | 0,002219 |
| +60 min | 2 | oui | 40 | 609 | 3,6102 | 101,92 | 0,000457 |
| fin | 1 | oui | 40 | 595 | 3,3065 | 83,04 | 0,000451 |

Horodatages UTC et identifiants d’audit (bornes SSE reçues, aucune durée de génération déduite) :

| Position | Envoi | Premier / dernier événement SSE texte | Session / message |
|---|---|---|---|
| début #1 | 2026-10-07T06:56:16.961058+00:00 | 2026-10-07T06:56:21.152325+00:00 / 2026-10-07T06:56:21.152400+00:00 | ses_eead9f5caffeo7Q6Q2Z79hL5ZL / msg_115260aa3001Hp6gEUrrNDAT47 |
| début #2 | 2026-10-07T06:56:21.676982+00:00 | 2026-10-07T06:56:32.107265+00:00 / 2026-10-07T06:56:32.276858+00:00 | ses_eead9e374ffeRqm1etN6wPTDRj / msg_115261d2a0019fQlBs8Uv7FwP3 |
| +30 min #1 | 2026-10-07T07:26:17.058468+00:00 | 2026-10-07T07:26:19.690453+00:00 / 2026-10-07T07:26:19.690453+00:00 | ses_eeabe7e57ffeCe1TiBA9dq4Vs6 / msg_115418254001qWRi32UHQX1ory |
| +30 min #2 | N/A collecte | N/A / N/A | ses_eeabe7375ffegR0wCNSb7S3Hc0 / msg_115418cf8001Ff2DAOrLCwrS1z |
| +60 min #1 | 2026-10-07T07:56:17.061680+00:00 | 2026-10-07T07:56:19.897696+00:00 / 2026-10-07T07:56:21.195875+00:00 | ses_eeaa30717ffe1gLED20tfjCjz5 / msg_1155cf972001WFnEmMzqqfD1xO |
| +60 min #2 | 2026-10-07T07:56:21.305497+00:00 | 2026-10-07T07:56:24.915698+00:00 / 2026-10-07T07:56:30.890807+00:00 | ses_eeaa2f654ffeo4TcxTgeyJzLoO / msg_1155d0a37001jwysJeMJ8pin34 |
| fin #1 | 2026-10-07T07:56:35.056409+00:00 | 2026-10-07T07:56:38.362854+00:00 / 2026-10-07T07:56:45.528159+00:00 | ses_eeaa2c095ffeyqt6RRlPkvghtS / msg_1155d3f970013KHAy9rBQJ4Kgq |

Relèves : prévues 4 (100 %), réussies 2 (50 %), échouées 2 (50 %), manquées 0 (0 %) ; tentatives 7, valides 2 (28,6 %), invalides 5 (71,4 %). Moyennes sur sondes valides (n=2) : TTMT 3,4583 s ; débit 92,48 tokens/s ; min/max TTMT 3,3065–3,6102 s ; min/max débit 83,04–101,92 tokens/s. Surcharge de télémétrie, hors production : sondes invalides 17 827 tokens, coût 0,015099 ; total 7 tentatives 19 031 tokens, coût 0,016007 ; somme des durées connues 42,425 s. La sonde +30 min tentative 2 reste en N/A de durée : délai HTTP côté collecte, bornes SSE non conservées, aucune mesure reconstituée. Chaque position échouée a reçu sa reprise unique immédiate prévue, les deux tentatives restent visibles.

## 2. Types de messages et d'outils

Parties (total 556, dénominateur de la ligne) :

| Type de partie | Effectif | Part |
|---|---:|---:|
| text | 75 | 13,5 % |
| step-start | 127 | 22,8 % |
| reasoning | 127 | 22,8 % |
| tool | 100 | 18,0 % |
| step-finish | 127 | 22,8 % |
| Total | 556 | 100 % |

Terminaisons des 127 réponses assistant : tool-calls 91 (71,7 %), stop 36 (28,3 %).

Outils (total 100 appels ; convention : un appel « completed » n'implique pas une approbation manuelle — les 30 décisions CAB explicites couvrent les 30 mandats enregistrés ; les 19 bash sont des exécutions après `APPROVED`) :

| Outil | Total | Completed | Erreur technique | Part du total |
|---|---:|---:|---:|---:|
| cgpt-validation_request_validation | 31 | 28 | 3 | 31,0 % |
| read | 23 | 22 | 1 | 23,0 % |
| bash | 19 | 19 | 0 | 19,0 % |
| glob | 8 | 8 | 0 | 8,0 % |
| write | 7 | 7 | 0 | 7,0 % |
| edit | 4 | 4 | 0 | 4,0 % |
| grep | 2 | 2 | 0 | 2,0 % |
| cgpt-validation_get_approval | 3 | 2 | 1 | 3,0 % |
| cgpt-validation_poll_approval | 1 | 1 | 0 | 1,0 % |
| cgpt-validation_broker_readiness | 1 | 1 | 0 | 1,0 % |
| cgpt-validation_list_pending | 1 | 1 | 0 | 1,0 % |
| Total | 100 | 95 | 5 | 100 % |

Statuts d'appel (95 completed / 5 erreur) et retours fonctionnels (92 succès / 6 erreurs / 2 qualifiés, total 100) sont distincts : la régression initiale est un appel completed au retour fonctionnel exit1, les deux globaux sont des exit1 natifs qualifiés jamais recomptés en exit0. Pourcentages arrondis à une décimale ; somme possible à ±0,2 point.

## 3. Fichiers modifiés

11 tentatives d'édition OpenCode (7 write + 4 edit), toutes approuvées et réussies : 11/11 (100 %), 0 refus, 0 erreur technique.

| Chemin absolu | Tentatives (part des 11) | Approuvées et réussies | Refusées | En erreur |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-outbound-declaration/proposal.md | 1 (9,1 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-outbound-declaration/design.md | 2 (18,2 %) | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-outbound-declaration/tasks.md | 2 (18,2 %) | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-outbound-declaration/specs/data-governance/spec.md | 1 (9,1 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_outbound_declaration.py | 2 (18,2 %) | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_outbound_declaration.py | 2 (18,2 %) | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_outbound_declaration_integration.py | 1 (9,1 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| Total | 11 (100 %) | 11 (100 %) | 0 (0 %) | 0 (0 %) |

Hors des 11 éditions : création native de /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-outbound-declaration/.openspec.yaml par la commande `openspec new change`, puis déplacement des 5 artefacts vers l'archive par la commande d'archivage autorisée. Sources antérieures inchangées ; fichier d'état orchestrateur /home/devops/datas/pixs/output/cismp-state.json mis à jour hors des 100 appels OpenCode (compteurs orchestrateur N/A, historique tronqué).

## 4. Commandes

19 commandes natives, chacune sous mandat CAB `APPROVED` distinct : 16 exit 0 (84,2 %), 3 exit 1 natifs réels (15,8 %) — jamais recomptés en exit 0 : la régression initiale (échec fonctionnel de garde, corrigé sous 3 éditions puis rejouée 31 OK) et les 2 globaux qualifiés (76/77 items, 19 WARNING/0 ERROR, identité baseline, 127 empreintes). Aucun refus, aucune erreur d'exécution technique. Libellés ≤100 caractères (`…` = troncature).

| Famille | Effectif | Part | exit 0 | exit 1 |
|---|---:|---:|---:|---:|
| openspec new change | 1 | 5,3 % | 1 | 0 |
| openspec validate stricts ciblés (change+spec, pré et post) | 4 | 21,1 % | 4 | 0 |
| py_compile (3 fichiers ; module et unitaire rejoués après correction) | 5 | 26,3 % | 5 | 0 |
| Exécutions de tests (unit ×2, intégration ×2, régression ×2) | 6 | 31,6 % | 5 | 1 |
| openspec validate globaux | 2 | 10,5 % | 0 | 2 |
| openspec archive du change | 1 | 5,3 % | 1 | 0 |
| Total | 19 | 100 % | 16 | 3 |

Détail des 19 mandats clôturés (requestId → commande, exit) :

- cismp-pixs-20261007-061019-outbound-new-change-16 → /home/devops/.local/npm/bin/openspec new change add-initial-data-outbound-declaration → exit 0 ; 1 occurrence (5,3 % des 19 commandes)
- cismp-pixs-20261007-061019-outbound-strict-pre-change-21 → /home/devops/.local/npm/bin/openspec validate add-initial-data-outbound-declaration --strict → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-strict-pre-spec-22 → /home/devops/.local/npm/bin/openspec validate data-governance --type spec --strict → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-syntax-module-24 → /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_outbound_declaration.py → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-syntax-unit-26 → /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_outbound_declaration.py → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-unit-run-27 → /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0] = ["src", "tests/unit"] impo… → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-syntax-integration-29 → /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_outbound_declarat… → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-integration-run-30 → /home/devops/python/current/bin/python3 -B tests/integration/test_data_outbound_declaration_integra… → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-regression-31 → /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0] = ["src", "tests/unit", "tes… → exit 1 fonctionnel ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-syntax-module-afterfix-35 → /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_outbound_declaration.py → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-syntax-unit-afterfix-36 → /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_outbound_declaration.py → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-unit-afterfix-37 → /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0] = ["src", "tests/unit"] impo… → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-integration-afterfix-38 → /home/devops/python/current/bin/python3 -B tests/integration/test_data_outbound_declaration_integra… → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-regression-afterfix-39 → /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0] = ["src", "tests/unit", "tes… → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-strict-final-change-40 → /home/devops/.local/npm/bin/openspec validate add-initial-data-outbound-declaration --strict → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-strict-final-spec-41 → /home/devops/.local/npm/bin/openspec validate data-governance --type spec --strict → exit 0 ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-global-specs-42 → /home/devops/.local/npm/bin/openspec validate --specs --strict --json --report findings → exit 1 qualifié ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-global-all-43 → /home/devops/.local/npm/bin/openspec validate --all --strict --json --report findings → exit 1 qualifié ; 1 occurrence (5,3 %)
- cismp-pixs-20261007-061019-outbound-archive-45 → /home/devops/.local/npm/bin/openspec archive add-initial-data-outbound-declaration --yes --skip-spe… → exit 0 ; 1 occurrence (5,3 %)

(Renvois complets des requestId dans le détail CAB de la session ; mandats d'édition 17-20, 23, 25, 28, 32-34, 44 non listés ici car sans commande.)

Commandes refusées : aucune (0, 0 %).

## 5. Accès web

Agent de codage (sur les 100 appels OpenCode de ces bornes) : 0 accès web, part 0,0 %. Résultats : 0 approuvé, 0 refusé, 0 erreur ; taux internes N/A (dénominateur nul). Aucune requête sans URL effectivement visitée n'est comptée.

Orchestrateur, pendant ce même intervalle : 0 accès HTTP externe mesuré ; N/A interne réseau modèle (non mesuré comme outil web) ; les 2 accès HTTP d'évaluation PLLM de la session maîtresse sont antérieurs à ces bornes et non réattribués.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-07 06:51:27.255Z (UTC) |
| Fin — après archivage | 2026-10-07 07:58:23.243Z (UTC) |
| Durée globale (pauses et attentes incluses) | 01 h 06 min 56 s (arrondi à la seconde) |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A | N/A — outil indisponible | N/A |
| Après — après archivage de la spécification | 2026-10-07T07:58:23.243Z (tentative) | N/A — outil indisponible | N/A |
| Différence après − avant | — | N/A | — |

Cause : l'outil natif `mcp__codex_app__get_usage_limits` est absent des outils exposés de cette session ; compte et fenêtre de 10 080 minutes invérifiables ; aucune valeur reconstituée. Quotas partagés par le compte : toute différence eût pu inclure d'autres tâches ; exclusivité non vérifiable.

Agrégation des domaines sur les 100 appels d'outils OpenCode :

| Domaine | Appels | Part globale | Succès fonctionnels | Refusés | Erreurs | Qualifiés |
|---|---:|---:|---:|---:|---:|---:|
| Éditions de fichiers | 11 | 11,0 % | 11 (100 %) | 0 (0 %) | 0 (0 %) | 0 (0 %) |
| Commandes natives (bash) | 19 | 19,0 % | 16 (84,2 %) | 0 (0 %) | 1 (5,3 %, corrigée puis rejouée OK) | 2 (10,5 %, exit1 natifs) |
| Accès web | 0 | 0,0 % | N/A (aucun) | N/A | N/A | N/A |
| Autres outils (read/glob/grep/CAB) | 70 | 70,0 % | 65 (92,9 %) | 0 (0 %) | 5 (7,1 %, lecture/transport/schéma) | 0 (0 %) |
| Total | 100 | 100 % | 92 (92,0 %) | 0 (0 %) | 6 (6,0 %) | 2 (2,0 %) |

Décisions CAB : 30/30 APPROVED (100 %), 0 rejet, 0 clarification, aucune décision réutilisée. Les deux délais request_validation sont récupérés par réponse MCP corrélée sans resoumission de demande enregistrée. L’appel de schéma invalide n’a créé aucun enregistrement ; une soumission corrigée unique lui a succédé. Le get_approval inconnu est tracé séparément ; aucun mandat parasite.

Conclusion vérifiable : 46 tests finaux réussis (14+1+31), 5 compilations exit 0, stricts pré/post exit 0, globaux exit 1 qualifiés (19 WARNING/0 ERROR, 76/77, 127 empreintes sans dérive), delta identique au canon, archivage exit 0 avec `--skip-specs` (aucune norme changée) et validation conservée, cinq tâches cochées sur preuves sous mandat distinct. Git : non inspecté, aucun commit, push ni branche. Navigateur et PostgreSQL : non nécessaires, non exécutés. Secrets : aucun lu par l'agent de codage ; aucun accès secret de l'orchestrateur pendant cet intervalle. Périmètre fonctionnel : représentation déclarative interne partielle ; l'activation refusée, l'audit et les garanties réelles du scénario ne sont pas livrés par ce change. Le présent rapport est un jalon de retour au parent en état SÉLECTION ; il ne déclare aucun cycle global TERMINÉ.

### Notes de protocole

- Incident de lecture initial : `src/pixs/kernel/diagnostics.py` absent (c'était le package `diagnostics/__init__.py`), relu sans effet ni permission consommée.
- Échec initial de la garde lexicale sur le terme « flux » (31 tests, 1 FAIL) : correction technique limitée à trois éditions de deux messages fixes vers le mot « transfert » du scénario canonique (design.md, module, test unitaire) ; garde et canon inchangés ; 46 contrôles finaux OK.
- Statuts d'outils ≠ retours fonctionnels : 3 exit 1 natifs (1 échec fonctionnel + 2 globaux qualifiés) jamais présentés comme exit 0.
- Phase de rédaction du présent rapport et écritures futures exclues des bornes closes ; anciennes sources et lots précédents inchangés ; prévol PLLM et rapport statistique du change archivé antérieur hors de ces bornes ; données communes au lot : non applicables (rapport par archive unique).
