# Statistiques — C14, modules essentiels PZT et DNS

RUN `cismp4-pixs-86551e9b05914e67` ; change `add-essential-pbo-pzt-and-dns-modules` ; archive `openspec/changes/archive/2026-10-23-add-essential-pbo-pzt-and-dns-modules`.
Rapport préparé après archive réellement observée, sous mandat distinct. Sources : API native des six sessions C14, checkpoint corrélé et agrégats CAB du contexte 904. Les sondes jetables sont séparées de la production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go | high | 2.512 s | 329.331 | N/A — génération seule non isolable |
| muse-spark-1.3-contributor | N/A | OpenCode Go | N/A sur 13 messages de résumé | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex / GPT-6 | N/A — révision exacte non exposée | OpenAI | N/A — métadonnée non exposée | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — durée active de génération absente |

Le temps de service et son dénominateur ne sont pas disponibles : le busy natif, les outils et la durée calendaire comprennent des attentes et ne constituent pas du temps de génération. Aucun pourcentage n’est estimé.

## 1. Statistiques générales et décisions

L’API native retrouve 3948 messages et 2221 outils dans six sessions, sans session manquante. Instantané : 2026-10-23T21:44:40.310822+00:00. Ces compteurs sont un inventaire relu après la borne finale de collecte ; le rapport et sa vérification ultérieurs ne sont pas inclus.

Un outil terminé peut avoir été autorisé automatiquement ; il ne prouve pas une décision manuelle ni un résultat fonctionnel. Un refus exige un rejet explicite de permission ; un exit non nul, une interruption ou une erreur MCP est une erreur technique. Un appel MCP terminé avec une décision REJECTED reste un transport réussi, sans opération approuvée.

| Résultat natif | Nombre | Part |
|---|---|---|
| Réussi au niveau natif | 2147 | 96.7 % |
| Refus explicite | 3 | 0.1 % |
| Erreur technique | 71 | 3.2 % |
| Non terminé | 0 | 0.0 % |
| Total | 2221 | 100 % |

Les décisions CAB suivantes couvrent seulement le contexte 904 ouvert le 23 octobre à 07:30 UTC, et ne s’additionnent pas à l’historique des six sessions :

| Décision CAB | Nombre | Part |
|---|---|---|
| approved | 202 | 99.5 % |
| rejected | 1 | 0.5 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 203 | 100 % |

Permissions once observées dans ce contexte : 197. Les approbations consommées ne sont jamais rejouées. Les interruptions, refus et échecs ont été réconciliés avant la reprise ; la dernière archive a un exit natif 0.

| Configuration native | Messages | Part des réponses | Tokens entrée | Tokens sortie | Raisonnement | Cache lu | Cache écrit | Coût API brut |
|---|---|---|---|---|---|---|---|---|
| opencode-go / muse-spark-1.3-contributor / high | 2357 | 99.5 % | 20617242 | 1297592 | 171634 | 678641846 | 0 | 3.712853092 |
| opencode-go / muse-spark-1.3-contributor / N/A | 13 | 0.5 % | 2100730 | 32851 | 15078 | 0 | 0 | 0.219658800 |

Les champs de tokens et de cache sont ceux du fournisseur, sans addition implicite des champs recouvrants. La devise et la facturation effective ne sont pas exposées ici : le coût API brut n’est pas une facture. Le mode 1 a été conservé sur instruction humaine ; aucune réinitialisation de quota n’a été exécutée par ce RUN.

Sondes valides : 38 ; événements de relève manquée/non exécutée conservés : 9. Aucun créneau n’est recréé rétroactivement. TTMT min/max : 1.328/4.005 s ; débit min/max : 157.107/1212.231 tokens/s. Les moyennes sont arithmétiques et excluent les mesures invalides. Les sondes valides représentent 61352 tokens de sortie et 345.512 s de surcharge, distincts de la production. Leur coût est N/A — non agrégé.

Le contexte CAB observe 20302.407 s busy, 30929.285 s idle et 23.484 s inconnues. Ces durées se rapportent au contexte 904 et ne prouvent aucun gain causal. Les compactages OpenCode sont observés ; l’API native de compactage Codex non exposée empêche de revendiquer un compactage conjoint complet.

## 2. Types de messages et d’outils

| Rôle | Messages | Part |
|---|---|---|
| user | 1578 | 40.0 % |
| assistant | 2370 | 60.0 % |
| Total | 3948 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 3537 | 27.3 % |
| step-start | 2367 | 18.3 % |
| reasoning | 2449 | 18.9 % |
| tool | 2221 | 17.1 % |
| step-finish | 2364 | 18.3 % |
| compaction | 15 | 0.1 % |
| Total | 12953 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 1468 | 61.9 % |
| stop | 896 | 37.8 % |
| inconnu | 6 | 0.3 % |
| Total | 2370 | 100 % |

| Outil | Total | Part | Réussis | Taux réussite | Refusés | Taux refus | Erreurs | Taux erreur | Non terminés |
|---|---|---|---|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 366 | 16.5 % | 366 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_request_validation | 385 | 17.3 % | 351 | 91.2 % | 0 | 0.0 % | 34 | 8.8 % | 0 |
| cgpt-validation_get_approval | 187 | 8.4 % | 187 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| bash | 301 | 13.6 % | 266 | 88.4 % | 3 | 1.0 % | 32 | 10.6 % | 0 |
| read | 239 | 10.8 % | 239 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| grep | 34 | 1.5 % | 33 | 97.1 % | 0 | 0.0 % | 1 | 2.9 % | 0 |
| glob | 30 | 1.4 % | 30 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_broker_health | 237 | 10.7 % | 237 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| edit | 14 | 0.6 % | 14 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_list_pending | 261 | 11.8 % | 260 | 99.6 % | 0 | 0.0 % | 1 | 0.4 % | 0 |
| cgpt-validation_broker_remediation_registry | 85 | 3.8 % | 85 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_poll_approval | 9 | 0.4 % | 7 | 77.8 % | 0 | 0.0 % | 2 | 22.2 % | 0 |
| write | 58 | 2.6 % | 58 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_broker_evaluate_remediation | 1 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_broker_execute_controlled_remediation | 1 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_cancel_approval | 1 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| todowrite | 11 | 0.5 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| question | 1 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 |
| Total | 2221 | 100 % | 2147 | 96.7 % | 3 | 0.1 % | 71 | 3.2 % | 0 |

## 3. Fichiers modifiés

Le checkpoint corrélé prouve 201 éditions source validées sur 75 chemins. Il s’agit d’opérations, pas de lignes ni de fichiers uniques par tentative. Les erreurs et refus des commandes sont conservés en section 4 ; leur attribution exhaustive à un fichier est N/A lorsque la commande ne désigne pas une édition unitaire.

| Chemin absolu complet au moment de l’édition | Éditions prouvées | Part | Refus/erreurs attribuables |
|---|---|---|---|
| /home/devops/datas/pixs/CHANGELOG.md | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/README.md | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/browser/c14-browser.mjs | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/browser/c14-runner.html | 2 | 1.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/c14-composed-browser.mjs | 8 | 4.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/c14-composed-policy.json | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/c14-composed-selection.json | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/c14-pages.test.mjs | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/c14-profile.test.mjs | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/frontend/tests/c14-resolver.mjs | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/openspec/changes/add-essential-pbo-pzt-and-dns-modules/VALIDATION.md | 10 | 5.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/openspec/changes/add-essential-pbo-pzt-and-dns-modules/design.md | 7 | 3.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/openspec/changes/add-essential-pbo-pzt-and-dns-modules/proposal.md | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/openspec/changes/add-essential-pbo-pzt-and-dns-modules/requirements.md | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/openspec/changes/add-essential-pbo-pzt-and-dns-modules/tasks.md | 10 | 5.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/auth/api_request_source.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/auth/runtime_verifier.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/api_pzt_dns_boundary.py | 2 | 1.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/api_pzt_dns_catalog.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/api_pzt_dns_dispatch.py | 2 | 1.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/api_pzt_dns_errors.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/api_pzt_dns_inputs.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/api_pzt_dns_openapi.py | 6 | 3.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/host_entry.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/backend/host_plan.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/__init__.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/adapters.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/apps.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/component.toml | 2 | 1.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/configuration.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/contracts.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/frontend.mjs | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/identifiers.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/lifecycle.py | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/migrations/0001_initial.py | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/migrations/__init__.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/models.py | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/naming.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/ports.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/dns/services.py | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/__init__.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/adapters.py | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/apps.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/component.toml | 2 | 1.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/configuration.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/contracts.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/frontend.mjs | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/identifiers.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/lifecycle.py | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/migrations/0001_initial.py | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/migrations/__init__.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/models.py | 6 | 3.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/ports.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/src/pixs/pzt/services.py | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/c14_composed_browser_fixture.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/c14_pg_test_support.py | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_agent_manifest_integration.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_backend_host_entry_guards.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_backend_host_entry_systemd.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_c14_composed_browser_postgres.py | 8 | 4.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_c14_http_auth_verifier_postgres.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_c14_http_management_postgres.py | 9 | 4.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_dns_audit_idempotence_postgres.py | 10 | 5.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_pzt_dns_audit_idempotence_postgres.py | 9 | 4.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_pzt_dns_authz_postgres.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/integration/test_pzt_dns_persistence_postgres.py | 3 | 1.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_backend_host_plan.py | 2 | 1.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_backend_host_runtime.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_pzt_dns_configuration.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_pzt_dns_contracts.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_pzt_dns_http_catalog.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_pzt_dns_http_inputs.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_pzt_dns_http_openapi.py | 4 | 2.0 % | N/A — voir commandes et incidents |
| /home/devops/datas/pixs/tests/unit/test_pzt_dns_manifests.py | 1 | 0.5 % | N/A — voir commandes et incidents |
| Total | 201 | 100 % | N/A |

Les six fichiers du dossier C14 ont été déplacés vers l’archive, sans réarchivage. Les liens relatifs du dossier et les liens entrants de quatorze documents actifs ont été rétablis mécaniquement, sans modification fonctionnelle des autres changes ; leurs SHA avant/après sont au checkpoint. Les archives historiques n’ont pas été réécrites. Les captures et rapports temporaires sous output restent hors Git.

## 4. Commandes

Chaque libellé est borné à 100 caractères ; plusieurs commandes exactes peuvent partager ce libellé. La commande complète et son mandat restent dans les preuves natives.

| Famille ou première ligne bornée | Résultat | Nombre | Part |
|---|---|---|---|
| /usr/bin/true | success | 23 | 7.6 % |
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path | refused | 1 | 0.3 % |
| /home/devops/python/current/bin/python3 -B -c 'exec(__import__("zlib").decompress(__import__("base64 | refused | 1 | 0.3 % |
| /home/devops/.local/npm/bin/openspec validate add-essential-pbo-pzt-and-dns-modules --strict | success | 9 | 3.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B -X pycache_prefix=/home/devops/datas/pixs/.cache/cismp4 | success | 14 | 4.7 % |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pzt_dns_mani | success | 1 | 0.3 % |
| /usr/bin/rm -r -- /home/devops/datas/pixs/.cache/cismp4-pixs-86551e9b05914e67-pycompile | success | 8 | 2.7 % |
| PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/c14_ | success | 18 | 6.0 % |
| PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/c14_ | error | 5 | 1.7 % |
| python3 -c "import pathlib; p=pathlib.Path('tests/integration/test_pzt_dns_audit_idempotence_postgre | error | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14SOURCE' | success | 131 | 43.5 % |
| PYTHONPATH=.:src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_pzt_dns_ma | error | 1 | 0.3 % |
| PYTHONPATH=.:src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_pzt_dns_ma | success | 1 | 0.3 % |
| PYTHONPATH=.:src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/c1 | error | 2 | 0.7 % |
| PYTHONPATH=.:src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/c1 | success | 2 | 0.7 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14FIDELITY' | success | 6 | 2.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14CANON' | success | 2 | 0.7 % |
| /home/devops/node/current/bin/node --input-type=module - <<'C14CLIENTPROBE' | success | 1 | 0.3 % |
| /home/devops/python/current/bin/python3 -B - <<'PYCODE' | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'PYCODE' | success | 6 | 2.0 % |
| PYTHONPATH=src:tests/unit .venv/bin/python3 -B -m unittest test_pzt_dns_http_catalog test_pzt_dns_ht | success | 2 | 0.7 % |
| /home/devops/node/current/bin/node --test frontend/tests/c14-pages.test.mjs | error | 1 | 0.3 % |
| /home/devops/node/current/bin/node --test frontend/tests/c14-pages.test.mjs frontend/tests/c14-profi | error | 1 | 0.3 % |
| /home/devops/node/current/bin/node --test frontend/tests/c14-pages.test.mjs | success | 1 | 0.3 % |
| /home/devops/node/current/bin/node frontend/tests/browser/c14-browser.mjs | error | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14CHECK' | success | 1 | 0.3 % |
| /home/devops/node/current/bin/node frontend/tests/browser/c14-browser.mjs | success | 2 | 0.7 % |
| PYTHONPATH=src:tests/unit .venv/bin/python3 -B -m unittest test_pzt_dns_manifests test_backend_host_ | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14CANON' | error | 1 | 0.3 % |
| PYTHONPATH=.:src:tests/integration:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14H | error | 7 | 2.3 % |
| PYTHONPATH=.:src:tests/integration:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14H | success | 3 | 1.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14FINALCOMPILE' | success | 1 | 0.3 % |
| /home/devops/node/current/bin/node --test frontend/tests/c14-profile.test.mjs | success | 1 | 0.3 % |
| /home/devops/node/current/bin/node --test frontend/tests/c14-pages.test.mjs frontend/tests/c14-profi | success | 1 | 0.3 % |
| PYTHONPATH=.:src /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14RESOLVER' | success | 1 | 0.3 % |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14OPENAPI' | success | 2 | 0.7 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14POLICY' | success | 1 | 0.3 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14C | success | 4 | 1.3 % |
| PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14COREPG' | refused | 1 | 0.3 % |
| PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14COREPG' | success | 1 | 0.3 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14M | success | 3 | 1.0 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14F | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14HTTPSSYNTAX' | success | 2 | 0.7 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14M | error | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14FRONTENDCONFORMITY' | success | 1 | 0.3 % |
| PATH=/home/devops/node/current/bin:/usr/bin:/bin /home/devops/node/current/bin/npm --prefix frontend | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14STANDALONE' | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14COMPOSEDBUILD' | error | 2 | 0.7 % |
| /home/devops/node/current/bin/node --input-type=module - <<'C14IMPORTDIAG' | success | 2 | 0.7 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14COMPOSEDBUILD' | success | 2 | 0.7 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14C | error | 7 | 2.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14SNAPSHOT' | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14PROFILECLEANUP' | success | 1 | 0.3 % |
| PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14GATES' | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14FINAL31' | success | 1 | 0.3 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14V | error | 1 | 0.3 % |
| PYTHONPATH=.:src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14V | success | 2 | 0.7 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14FINAL33' | error | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14FINAL33' | success | 1 | 0.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14ARCHIVE' | success | 1 | 0.3 % |
| Total | Tous | 301 | 100 % |

Commandes explicitement refusées :

| Libellé borné | Nombre | Part des commandes |
|---|---|---|
| /home/devops/python/current/bin/python3 -B -c 'from pathlib import Path | 1 | 0.3 % |
| /home/devops/python/current/bin/python3 -B -c 'exec(__import__("zlib").decompress(__import__("base64 | 1 | 0.3 % |
| PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B - <<'C14COREPG' | 1 | 0.3 % |

Les contrôles qui ont échoué, dont des harnais, bases de fixture, imports, limites de profil et empreintes canoniques devenues anciennes, sont conservés dans ces totaux. Leurs corrections et nouvelles exécutions utilisent des mandats distincts ; les échecs ne deviennent jamais des réussites. Les libérations reposent sur les fins natives et les effets/nettoyages connus.

## 5. Accès web

Les six sessions de codage exposent zéro outil webfetch/websearch : total 0, taux N/A (dénominateur nul). Cela n’annule pas les échanges fournisseur autorisés ni les requêtes locales HTTPS des tests. L’historique web complet de l’orchestrateur n’a pas été agrégé : N/A. Le sous-ensemble documentaire explicitement observé pendant la reprise est le suivant ; aucune visite n’est déduite d’une simple requête échouée.

| URL affichée, 100 caractères maximum | État | Requêtes | Part du sous-ensemble |
|---|---|---|---|
| https://chromedevtools.github.io/devtools-protocol/tot/Page/ | Consulté | 1 | 20.0 % |
| https://developer.mozilla.org/en-US/docs/Web/WebDriver/Reference/BiDi/Modules/browsingContext/setVi… | Consulté | 1 | 20.0 % |
| https://developer.mozilla.org/en-US/docs/Web/WebDriver/Reference/BiDi/Modules/browsingContext/captu… | Consulté | 1 | 20.0 % |
| https://w3c.github.io/webdriver-bidi/ | Échec de récupération, contenu trop grand | 2 | 40.0 % |
| Total | 3 consultations ; 2 erreurs | 5 | 100 % |

Refus explicites dans ce sous-ensemble : 0 (0,0 %) ; consultations 3 (60,0 %) ; erreurs 2 (40,0 %). Aucun refus n’est présenté comme une visite.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-22T19:30:18.851Z |
| Fin — après archivage | 2026-10-23T21:43:35+00:00 |
| Durée globale, pauses et attentes incluses | 26 h 13 min 16 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-22T19:30:18.851Z | 7 % | 2026-10-29T17:09:38+00:00 |
| Après — après archivage | 2026-10-23T21:43:35+00:00 | 5 % | 2026-10-30T21:13:45+00:00 |
| Différence après − avant | — | N/A — fenêtres différentes | — |

Les deux lectures natives concernent le même compte et une fenêtre de 10080 minutes, mais leurs resetsAt diffèrent ; aucune consommation ne peut être reconstituée par soustraction. Les quotas sont partagés et ne sont pas attribuables exclusivement à ce RUN. Aucun crédit de réinitialisation n’a été consommé par ce pilotage.

| Domaine natif | Total | Part globale | Réussis | Taux réussite | Refusés | Taux refus | Erreurs | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils et lectures | 1848 | 83.2 % | 1809 | 97.9 % | 0 | 0.0 % | 39 | 2.1 % |
| Commandes | 301 | 13.6 % | 266 | 88.4 % | 3 | 1.0 % | 32 | 10.6 % |
| Fichiers — outils natifs edit/write | 72 | 3.2 % | 72 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Global | 2221 | 100 % | 2147 | 96.7 % | 3 | 0.1 % | 71 | 3.2 % |

Les 201 éditions source par commandes et outils ne sont pas ajoutées une deuxième fois au total natif. L’archive est une commande ; ses déplacements et corrections de liens sont décrits séparément. Les statistiques CAB ne s’additionnent pas aux statistiques API des mêmes appels.

Résultats de développement : modules PZT/DNS, onze liaisons HTTP, sept contrats métier, deux plans API et pages de gestion réalisés. Preuves retenues, sans additionner les réexécutions : Kernel/Core 988 tests, Core PostgreSQL 200 cas, gestion 38 unités + 104 cas PostgreSQL, HTTP/PG 43 cas, DTO/OpenAPI 20 unités, frontend propriétaire 12 cas, suite configurée 145 par navigateur. Build COMPOSED et STANDALONE réels ; recettes composées Chromium/Firefox quinze critères chacune, huit captures desktop/mobile relues, schémas/processus/profils nettoyés. Syntaxe finale : 55 Python et 41 JavaScript.

La revue de 373 sources avant archive et le contrôle protégé de 388 sources/liens après archive ont réussi. OpenSpec strict : 187 éléments avant archive, 186 après, zéro échec. L’archive a émis un avertissement non bloquant sur les intitulés français Why/What Changes ; skip_specs conserve l’absence de delta normatif. Un message INFO tiers sur un delta déjà présent n’autorise ni ne prouve l’archive de ce tiers.

Archive prouvée par call_01a16ab78bd8746ea3cdbb0c7dcd86d1. Publication CAB durable publish-c14-c218b238987c4b76, référence 71. Le gate final, le désarmement et la libération sont encore à exécuter après vérification de ce rapport ; ils ne sont pas inventés dans ce document. Les dix cases tasks.md sont cochées ; la note 3.4 distingue l’admission de clôture des preuves terminales.

Garanties limitées : HTTP et GUI réels PLATFORM ; isolation tenant/scope du domaine PostgreSQL distincte. TLS loopback chiffré avec bypass de chaîne dans les seuls profils jetables : aucun TLS déployé, PKI, exécutant PA/PZT, DNS actif, matériel, paquet installé ou P0 global qualifié. Audit manuel exhaustif d’accessibilité non réalisé ; les labels, focus programmatique, rendu responsive et captures ne le remplacent pas. Le lien Sign in visible avec une session vérifiée a été signalé à C11, sans modification hors responsabilité C14. BIND 9 reste un choix logiciel/packaging spécifié séparément, activation ultérieure. Aucun Git, push ou déploiement exécuté ; aucun secret reçu par le modèle ni ajouté aux sources. Les données privées de recette restent locales et sont nettoyées.
