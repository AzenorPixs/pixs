# STATISTIQUES — add-bulk-server-cancellation-request-v1
RUN cismp-pixs-01a13bab2ed7 ; archive openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | OpenCode Go | high | 3,479 s | 3541,9 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; modèle N/A | OpenCode Go | N/A — summarize sans variant | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Métriques TTMT/débit : moyenne arithmétique des sondes de codage, aucune sonde orchestrateur. Temps de service et dénominateur cumulé N/A ; les durées messages comprennent outils/attentes et ne sont pas des durées isolées de génération. Chevauchements non quantifiés. Compaction distincte du travail high.

## 1. Statistiques générales et décisions

Historique des 2 sessions natives propres au change, borné au relevé final après archive. Les agrégats CAB 1.1 ne couvrent que les observations depuis maintenance ; aucune reconstruction ou addition des mêmes outils.

| Mesure | Nombre | Part |
| --- | --- | --- |
| Messages | 462 | 100,0 % |
| Outils | 313 | 100,0 % |
| Achevés/autorisés¹ | 284 | 90,7 % |
| Refus permission | 0 | 0,0 % |
| Erreurs outils | 29 | 9,3 % |
| Réponses de compaction | 1 | 0,3 % |

¹ completed indique achevé, autorisé automatiquement ou via CAB ; ce statut seul ne prouve pas une décision manuelle. Bash exit1 est distingué des refus et erreurs d’outil. Les mutations exigent décision explicite et once. États des décisions non exposées N/A.

| État final MCP par requestId unique | Nombre | Part |
| --- | --- | --- |
| APPROVED | 32 | 94,1 % |
| CANCELLED | 1 | 2,9 % |
| REJECTED | 1 | 2,9 % |
| **Total observé** | 34 | 100,0 % |

| Tokens natifs | Valeur |
| --- | --- |
| input | 7743184 |
| output | 96791 |
| reasoning | 37763 |
| cache_read | 85894669 |
| cache_write | 0 |

Raisonnement potentiellement inclus dans output et caches séparés : aucun total artificiel. Coût natif déclaré 0,973019 USD, non assimilé à une facture. Sondes exclues des totaux de production.
### Développement et validations

3 compilations exit0 ; 2 nouveaux unitaires et 1 inertie de harnais réussis ;42 régressions ciblées exit0 ;20/20 propriétés PostgreSQL réelles vraies, nettoyage/connexions fermées prouvés. Les propriétés PG ne sont pas vingt unittest et les sous-ensembles globaux ne s’additionnent pas comme tests uniques.
{"python": {"modules": 241, "tests": 1935, "skipped": 0, "failed": [], "native_exit": 0, "manifest_sha256": "cc370d25a646fdddb0eeabcdf6e3bb6ef54c200b8915c568a15d31a0ee4bc809"}, "postgres_reel": {"criteria": 20, "all_true": true, "exit": 0, "cleanup_ok": true, "conns_closed": true}, "global_openspec_prearchive": {"exit": 1, "items": 79, "passed": 77, "failed": 2, "warnings": [{"id": "bulk-operations", "level": "WARNING", "path": "requirements[6]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior."}, {"id": "bulk-operations", "level": "WARNING", "path": "requirements[10]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior."}, {"id": "bulk-operations", "level": "WARNING", "path": "requirements[13]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior."}, {"id": "identity-assurance", "level": "WARNING", "path": "requirements[4]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior."}], "errors": 0, "proof": "C2 postarchive strict actual native, applicable sous exclusion C1 avant cochage"}, "global_openspec_postarchive": {"exit": 1, "totals": {"items": 78, "passed": 76, "failed": 2}, "issues": [{"level": "WARNING", "path": "requirements[6]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior.", "id": "bulk-operations"}, {"level": "WARNING", "path": "requirements[10]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior.", "id": "bulk-operations"}, {"level": "WARNING", "path": "requirements[13]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior.", "id": "bulk-operations"}, {"level": "WARNING", "path": "requirements[4]", "message": "Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior.", "id": "identity-assurance"}], "errors": 0, "same4historicalWarnings": true}, "strict_cible_post_cochage": {"exit": 0, "items": 1, "issues": []}}
Inventaire DEVOPS actualisé CLI1.14.2/PG16.15 ; versions réellement exécutées CLI1.14.1/PostgreSQL16.14. Aucun upgrade exécuté.
### Continuité et limites

Erreur MCP -32602 de compilation pour identifiants omis, puis refus sans effet et récupération contrôlée du même job/change ; aucune autorisation consommée rejouée. Corrections module/unitaires/harnais avant validations réussies. Timeouts conservés, distincts des refus.
Incident de cochage : première tentative write SchemaError/input vide avant permission ou effet ; seconde tentative exacte, seule effective, une once. Compte rendu initial corrigé et prévol frais once/exit0/READY0 prouvé, sans rejouer les coches.
Pause maintenance humaine : {"begin": "2026-10-15T08:02:08.872608+00:00", "end": "2026-10-15T09:02:59.200916+00:00", "missed_measurements": "N/A — aucune reconstruction"}. Premier prévol non admis pendant FIFO puis annulé nativement sans effet. Prévol inédit ensuite approuvé avec once, /usr/bin/true0, READY0. Même RUN/job/session à la reprise. Compactage OpenCode observé ; API Codex absente, cycle conjoint incomplet sans réussite inventée.
### Sondes dédiées

| Position | Envoi UTC | Sortie tokens | TTMT s | Tokens/s | Retard s | État |
| --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-15T04:09:55.518444+00:00 | 609 | 1.3643083919305354 | 349.18546129853087 | N/A | réussie |
| +30 min | 2026-10-15T04:40:15.361517+00:00 | 609 | 7.264297207002528 | 23705.557785865527 | 40.807321071624756 | réussie |
| +60 min | 2026-10-15T05:11:28.067659+00:00 | 625 | 2.8059116939548403 | 119.8124739005382 | 113.5134630203247 | réussie |
| +90 min | 2026-10-15T05:44:53.161129+00:00 | 626 | 3.295668998034671 | 175.45074852661475 | 318.60693311691284 | réussie |
| +120 min | 2026-10-15T06:20:34.144319+00:00 | 644 | 2.9094928110716864 | 108.9769564111618 | 659.5901231765747 | réussie |
| +330 min | 2026-10-15T09:40:49.324722+00:00 | 609 | 3.9017915300792083 | 129.09391426111225 | 74.78672194480896 | réussie |
| fin | 2026-10-15T09:46:24.976715+00:00 | 609 | 2.8100827110465616 | 205.22959468371963 | N/A | réussie |

| Relèves | Nombre | Part |
| --- | --- | --- |
| Réussies | 7 | 53,8 % |
| Échouées | 0 | 0,0 % |
| Manquées | 6 | 46,2 % |
| **Total prévu/final** | 13 | 100,0 % |

Prompt constant : nombres 0001 à 0200 chacun sur une ligne à 4 chiffres, aucun autre texte/outil/fichier/réseau. Comptages natifs réels. Relève +30 min reçue en rafale (~0,026s) : débit client apparent très élevé, influençant la moyenne, sans preuve de débit réel fournisseur. Conformité textuelle rétrospective des sessions déjà supprimées N/A.

| Mesure des sondes valides | Moyenne | Min | Max |
| --- | --- | --- | --- |
| TTMT s | 3.478793334731433 | 1.3643083919305354 | 7.264297207002528 |
| Tokens/s apparents | 3541.9009907067434 | 108.9769564111618 | 23705.557785865527 |

| Sonde manquée | Échéance | Cause |
| --- | --- | --- |
| +150 min | N/A | Relève non exécutée pendant attente/quiescence et réconciliation, aucune reconstruction |
| +180 min | N/A | Relève non exécutée pendant attente/réconciliation opérationnelle, aucune reconstruction |
| +210 min | N/A | Relève non exécutée avant pause maintenance, aucune reconstruction |
| +240 min | 2026-10-15T08:09:34.538000+00:00 | Pause maintenance CAB demandée par le développeur ; aucune reconstruction |
| +270 min | 2026-10-15T08:39:34.538000+00:00 | Pause maintenance CAB demandée par le développeur ; aucune reconstruction |
| +300 min | 2026-10-15T09:09:34.538000+00:00 | Quiescence FIFO/exclusion CISMP2 ; pas de nouvelle sonde autorisée, aucune reconstruction |

Surcharge sondes distincte : 91345 tokens natifs, 4331 sortie et 0,009666 USD. Aucune relève reconstruite.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 111 | 24,0 % |
| assistant | 351 | 76,0 % |
| **Total** | 462 | 100,0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 256 | 16,1 % |
| step-start | 351 | 22,0 % |
| reasoning | 323 | 20,3 % |
| tool | 313 | 19,6 % |
| step-finish | 350 | 22,0 % |
| compaction | 1 | 0,1 % |
| **Total** | 1594 | 100,0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 286 | 81,5 % |
| stop | 64 | 18,2 % |
| interrompue/non exposée | 1 | 0,3 % |
| **Total** | 351 | 100,0 % |

| Outil | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| bash | 18 | 5,8 % | 18 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 19 | 6,1 % | 19 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 97 | 31,0 % | 96 (99,0 %) | 0 (0,0 %) | 1 (1,0 %) |
| cgpt-validation_cancel_approval | 1 | 0,3 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 51 | 16,3 % | 51 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 18 | 5,8 % | 18 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 19 | 6,1 % | 7 (36,8 %) | 0 (0,0 %) | 12 (63,2 %) |
| cgpt-validation_request_validation | 35 | 11,2 % | 21 (60,0 %) | 0 (0,0 %) | 14 (40,0 %) |
| read | 40 | 12,8 % | 39 (97,5 %) | 0 (0,0 %) | 1 (2,5 %) |
| write | 15 | 4,8 % | 14 (93,3 %) | 0 (0,0 %) | 1 (6,7 %) |
| **Total** | 313 | 100,0 % | 284 (90,7 %) | 0 (0,0 %) | 29 (9,3 %) |


## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/design.md | 1 | 6,7 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/proposal.md | 1 | 6,7 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/specs/bulk-operations/spec.md | 1 | 6,7 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/tasks.md | 3 | 20,0 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_server_cancellation.py | 2 | 13,3 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_server_cancellation_postgres_integration.py | 3 | 20,0 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_server_cancellation.py | 3 | 20,0 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| N/A | 1 | 6,7 % | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) |
| **Total** | 15 | 100,0 % | 14 (93,3 %) | 0 (0,0 %) | 1 (6,7 %) |

Tentatives natives write/edit seulement, écritures physiques internes CLI N/A. Cinq artefacts OpenSpec déplacés vers archive et canon B06 synchronisé ; rapport créé après borne sous mandat distinct, exclu des compteurs précédents. Trois Python nouveaux ; aucun code existant modifié.28 fichiers de référence contrôlés avant archive, sans divergence hors DEVOPS documenté. Git non inspecté.

| Fichier final à la publication | SHA-256 |
| --- | --- |
| /home/devops/datas/pixs/src/pixs/backend/bulk_server_cancellation.py | ba86d66755437d7aa4d47d6f7aefc3132ef5d7a88e6a6478d4dfc77951da4334 |
| /home/devops/datas/pixs/tests/unit/test_bulk_server_cancellation.py | 40866bdb094803b84c95fd86c54ef7fb4364c7715e63d53459177f932db6457f |
| /home/devops/datas/pixs/tests/integration/test_bulk_server_cancellation_postgres_integration.py | 024241f8c117ebaed421394befbd689761c277125297d1865e710138cb7ba1d6 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/.openspec.yaml | c5936a7e8ac90455175dd905c9e8fb9d33cf82476be795f24133b51ef95c3d96 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/proposal.md | 4830c195b1a9baf0988be844c8925a70051d17fd681b81e981284d2a58cf8eb1 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/design.md | dfb2c1f711dbfbcf6a7034fbc8169716327d5af639305aafc6fb30d541404b37 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/tasks.md | 580b336f6246c699136c95ba896dbd7711e56639795b8e51572d402cc59b3175 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-bulk-server-cancellation-request-v1/specs/bulk-operations/spec.md | 8db9fec55f64e401316046d34803b664639752c6eea174cdda5a54509273476a |
| /home/devops/datas/pixs/openspec/specs/bulk-operations/spec.md | dd581551f06712338da20ea703101adc11c6390584a272c0175e70aae97a6580 |


## 4. Commandes

| Famille | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Archive OpenSpec | 1 | 5,6 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Compilation Python | 3 | 16,7 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Préparation OpenSpec | 1 | 5,6 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Prévol CAB /usr/bin/true | 4 | 22,2 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Tests et diagnostics Python | 5 | 27,8 % | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Validation OpenSpec | 4 | 22,2 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| **Total** | 18 | 100,0 % | 18 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

| Exit Bash achevé | Nombre | Part |
| --- | --- | --- |
| 0 | 17 | 94,4 % |
| 1 | 1 | 5,6 % |
| **Total** | 18 | 100,0 % |

| Commande 100 caractères max | Nombre | Part | Achevée | Refusée | Erreur |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 4 | 22,2 % | 4 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec new change add-bulk-server-cancellation-request-v1 | 1 | 5,6 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate add-bulk-server-cancellation-request-v1 --strict --js… | 2 | 11,1 % | 2 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile src/pixs/backend/bulk_server_cancellatio… | 1 | 5,6 % | 1 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile tests/unit/test_bulk_server_cancellation… | 1 | 5,6 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v tests.u… | 1 | 5,6 % | 1 | 0 | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m py_compile tests/integration/test_bulk_server_cance… | 1 | 5,6 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v tests.i… | 1 | 5,6 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec --version | 1 | 5,6 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/test… | 1 | 5,6 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v tests.u… | 1 | 5,6 % | 1 | 0 | 0 |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B - <<'V' import sys,jso… | 1 | 5,6 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec archive add-bulk-server-cancellation-request-v1 --yes --json | 1 | 5,6 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 1 | 5,6 % | 1 | 0 | 0 |
| **Total** | 18 | 100,0 % | 18 | 0 | 0 |

### Commandes refusées regroupées

| Commande refusée | Nombre | Part refus |
| --- | --- | --- |
| **Total refus** | 0 | N/A |

Les sous-processus internes de tests ne constituent pas des mandats indépendants. Exits non nuls de diagnostics distincts des refus.

## 5. Accès web

| Résultat web | Nombre | Taux |
| --- | --- | --- |
| Achevé/autorisé | 0 | N/A |
| Refusé | 0 | N/A |
| Erreur | 0 | N/A |
| **Total** | 0 | N/A |

Aucun outil web observé ; aucune URL visitée/refusée à lister. Transports fournisseur/CAB/PG distincts des consultations de sources web ; requêtes réseau internes N/A, non instrumentées.

## 6. Synthèse globale

| Durée de session | Valeur |
| --- | --- |
| Début | 2026-10-15T04:09:34.538000+00:00 |
| Fin après archive et sonde finale | 2026-10-15T09:47:42.938000+00:00 |
| Durée globale, pauses/attentes incluses | 05 h 38 min 08 s |

| Quota Codex sur 7 jours | Horodatage UTC | Utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-15T04:09:31.747Z | 34 % | 2026-10-20T04:59:31+00:00 |
| Après archive/sonde finale | 2026-10-15T09:47:42.938Z | 5 % | 2026-10-22T06:12:56+00:00 |
| Différence après−avant | — | N/A — compte/fenêtre non comparable | — |

Source outil natif mcp__codex_app__get_usage_limits, quota codex/fenêtre10 080 min, même compte vérifié sans identifiant publié. Comparaison admise seulement si même resetsAt et compteur non décroissant. Ici resetsAt a changé entre les deux relevés et le compteur passe de 34 % à 5 % : différence N/A, aucune consommation reconstruite à travers ce changement de fenêtre. Compte partagé : aucune attribution exclusive ni conversion tokens/euros. Rédaction du rapport hors intervalle.

| Domaine | Total | Part | Achevés/autorisés¹ | Refus permission | Erreurs outil |
| --- | --- | --- | --- | --- | --- |
| Commandes Bash natives | 18 | 5,8 % | 18 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| MCP et autres outils | 280 | 89,5 % | 252 (90,0 %) | 0 (0,0 %) | 28 (10,0 %) |
| Écritures natives fichier | 15 | 4,8 % | 14 (93,3 %) | 0 (0,0 %) | 1 (6,7 %) |
| **Total** | 313 | 100,0 % | 284 (90,7 %) | 0 (0,0 %) | 29 (9,3 %) |

### Agrégats intégrés CAB 1.1.0

| Mesure CAB depuis maintenance | Valeur |
| --- | --- |
| reservedMs | 6144321 |
| busyMs | 888037 |
| idleMs | 5256260 |
| nativeUnknownMs | 24 |
| integrationMs | 1291382 |
| queueMs | 2440415 |
| staleMs | 99115 |
| Persistance | READY |
| Tentatives HTTP | {"integration-draining": 4, "decision-run-divergent": 2, "native-validation-not-correlated": 2, "integration-cohort-not-ready": 2, "run-not-quiescent": 1, "native-session-not-quiescent": 1} |

| Latence CAB | Total | Médiane ms | p95 ms | Échantillon |
| --- | --- | --- | --- | --- |
| requestToDecision | 7 | 22233 | 61352 | 7 |
| decisionToOnce | 7 | 12075 | 44016 | 7 |
| nativeTool | 56 | 303 | 60003 | 56 |

Busy ne prouve pas du codage productif. Observations antérieures à CAB 1.1 non reconstruites ; quantiles sur les 2 048 dernières observations au maximum. Tentatives HTTP distinctes des refus. Aucune addition de ces durées recouvrantes.
Publication technique : {"published_at": "2026-10-15T09:49:01.073374+00:00", "referenceVersion": 17, "integration_released": true, "archive_native_exit": 0, "canon_sha256": "dd581551f06712338da20ea703101adc11c6390584a272c0175e70aae97a6580", "report_required_after_release": true, "evidence": ["Archive unique2026-10-15-add-bulk-server-cancellation-request-v1, nativecall_01a13ef13ffc7664bd5c1aec4c974392, once per_13ef143a1001xrFaX7t9c3yaCh,exit0,specsUpdatedtrue modified1", "CanonexactB06 SHA256dd581551f06712338da20ea703101adc11c6390584a272c0175e70aae97a6580 ;5artefacts exacts,7tâchescochées", "1935tests241modules0skip0échec,20critèresPGréelcleanup0,403 sourcesinchangées,strictciblé0", "Globalstrictpostarchive78items76pass4WARNINGhistoriquesexactes0ERRORexit1consigné ; sonde finale valide etquotanatif relevé"]}. Exclusion libérée avant phaseREPORT ; rapport soumis à mandat distinct. Gate/désarmement/libération restent à vérifier après ce rapport ; parent CISMP poursuit ensuite.
Tests et archives prouvés dans /home/devops/datas/pixs/output/cismp/cismp-pixs-01a13bab2ed7/state.json. Aucun Git, commit, push ou branche. Aucun secret lu par les agents ; chargement fournisseur/PG limité aux seuls processus autorisés, sans valeur dans prompts/checkpoint/rapport. Aucun worker, route, migration, dépendance ou infrastructure métier ajouté.
