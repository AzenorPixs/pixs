# Statistiques — C03 authentification locale et sessions

RUN cismp1-pixs-d4031c8c16a3409d, contexte CAB 433, session reconstruite ses_ea598d5c9ffee1IM7aJ25LQ2Oe. Archive réelle : /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions. Relevé figé le 2026-10-21T04:37:04.511Z, après archivage et avant rédaction du présent rapport. Les écritures/vérifications du rapport et opérations de clôture ultérieures sont hors de cette borne ; elles restent dans le checkpoint. L'ancien historique de session 404 n'est pas reconstitué.

### Agents de codage

| Agent | Modèle et raisonnement observés | Mesures |
|---|---|---|
| OpenCode 1.19.3 | opencode-go / muse-spark-1.3-contributor ; high pour les messages exposant variant ; trois compactions sans variant exposé | 828 messages assistant ; 15 sondes de reprise séparées ; TTMT moyen 2.357 s ; débit moyen 257.880 tokens/s |

Les sondes utilisent un prompt déterministe, sans outil, et sont exclues des tokens de production ci-dessous. TTMT désigne le premier événement SSE, raisonnement éventuellement inclus ; le débit mesure le flux fourni, pas un débit physique garanti. Version exacte du modèle au-delà de son identifiant : N/A, non exposée.

### Agents orchestrateurs

Codex pilote et examine les preuves. Version/build précis, raisonnement effectif, tokens et coût de l'orchestrateur : N/A, aucune API propriétaire de télémétrie de ce chat n'est disponible. Les outils et lectures de l'orchestrateur ne sont pas ajoutés artificiellement aux compteurs OpenCode. Aucun sous-agent supplémentaire n'est créé.

## 1. Statistiques générales et décisions

| Mesure native OpenCode | Nombre | Part |
|---|---:|---:|
| Messages | 1334 | 100,0 % |
| Appels d'outils | 596 | 100,0 % |
| Outils terminés nativement | 584 | 98.0 % |
| Outils en erreur native | 12 | 2.0 % |
| Bash terminé avec code non nul | 9 | 9.2 % des Bash ; distinct des erreurs d'outil |
| Entrée hors cache | 8983468 | 3.0 % |
| Sortie | 539604 | 0.2 % |
| Raisonnement | 31480 | 0.0 % |
| Cache lu | 285870437 | 96.8 % |
| Cache écrit | 0 | 0.0 % |
| Total tokens natif | 295424989 | 100,0 % |

Le total natif égale entrée + sortie + raisonnement + cache lu + cache écrit. Champ coût natif cumulé : 1.58430447 ; unité/facturation réelle non attestée par cette télémétrie. Coût monétaire réellement attribuable et euros : N/A ; aucune conversion tokens/coût n'est inventée.

| Décisions du contrôleur CAB, contexte 433 | Nombre | Part des décisions terminales |
|---|---:|---:|
| Approuvées | 165 | 100.0 % |
| Refusées CAB | 0 | 0.0 % |
| Clarification | 0 | 0.0 % |
| Pending au snapshot | 0 | N/A — état, pas décision terminale |
| Permissions once émises | 163 | 98.8 % des approbations |

Approbation CAB, permission once et résultat exécuté sont distincts. Les refus natifs de permission et les codes Bash non nuls ne sont pas des refus CAB. Le contrôleur observé à 2026-10-21T04:37:04.774Z fournit un instantané distinct de l'historique natif ; les lectures de diagnostic arrivées entre snapshots expliquent les écarts de compteurs, sans les sommer.

Développement final : 116 tests unitaires Auth réussis ; 243 cas PostgreSQL réussis dans 11 recettes, avec tous schémas nettoyés/connexions fermées ; 49 compilations/checks Django sans diagnostic ni dérive de migration ; 4 tests OpenLDAP réels réussis sur les fonctions inchangées. Les catégories se chevauchent parfois par préconditions et ne sont pas additionnées en un faux total de tests uniques. Les 78 canons et le change C03 passent le strict ; 117 renvois locaux/UTF-8/LF sont vérifiés. Le trousseau natif non qualifié choisit MEMORY, sans fichier clair.

Compactions : 3 parties natives et 3 cycles OpenCode documentés ; l'API propriétaire de compaction Codex est indisponible, coordinated_complete=false. Les retards sont conservés dans le checkpoint, jamais présentés comme ponctuels. Aucune approbation consommée n'a été rejouée.

| Sonde séparée | Début UTC | TTMT s | Débit tokens/s | Retard s |
|---|---|---:|---:|---:|
| début | 2026-10-20T17:49:40.428Z | 2.572 | 174.026 | N/A |
| +30min après reprise | 2026-10-20T22:01:40.756Z | 1.585 | 382.634 | N/A |
| +60min après reprise | 2026-10-20T22:32:08.239Z | 2.555 | 241.523 | N/A |
| +90min après reprise | 2026-10-20T23:06:46.874Z | 2.452 | 101.704 | 310.874 |
| +120min après reprise | 2026-10-20T23:38:44.662Z | 2.176 | 266.121 | 428.662 |
| +150min après reprise | 2026-10-21T00:04:05.822Z | 2.692 | 135.325 | 149.822 |
| +180min après reprise | 2026-10-21T00:32:06.881Z | 2.613 | 181.049 | 30.881 |
| +210min après reprise | 2026-10-21T01:02:29.960Z | 3.085 | 104.273 | 53.960 |
| +240min après reprise | 2026-10-21T01:41:24.699Z | 1.221 | 845.528 | 588.699 |
| +270min après reprise | 2026-10-21T02:02:05.939Z | 2.087 | 263.025 | 29.939 |
| +300min après reprise | 2026-10-21T02:32:19.742Z | 2.567 | 172.748 | 43.742 |
| +330min après reprise | 2026-10-21T03:02:22.317Z | 2.863 | 206.157 | 46.317 |
| +360min après reprise | 2026-10-21T03:31:41.696Z | 2.750 | 96.390 | 5.696 |
| +390min après reprise | 2026-10-21T04:02:11.787Z | 1.686 | 539.619 | 35.787 |
| +420min après reprise | 2026-10-21T04:31:45.206Z | 2.452 | 158.081 | 9.206 |

Les 15 sondes de reconstruction réussissent avec sortie exacte et zéro outil ; sortie cumulée 8002 tokens, surcharge exclue de la production. Trois anciennes sondes du parent (13:14, 13:50 et 16:06 UTC le 20 octobre) sont conservées dans l'état, mais ne sont pas fusionnées avec la nouvelle session. La période de gel/maintenance n'est pas reconstruite en sondes fictives ; les retards réels de reprise restent visibles. Dernier PLLM réel : 2026-10-21T04:31:38.240874Z, Muse/high, valide ; quotas Go rolling4 %, semaine21 %, mois10 %, TTFT9,3562 s ; débit SSE raisonnement+réponse1540,349 tokens/s. Aucun modèle de substitution.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part des messages |
|---|---:|---:|
| user | 506 | 37.9 % |
| assistant | 828 | 62.1 % |

| Type de partie | Nombre | Part des parties |
|---|---:|---:|
| text | 1259 | 28.9 % |
| step-start | 828 | 19.0 % |
| reasoning | 842 | 19.3 % |
| tool | 596 | 13.7 % |
| step-finish | 827 | 19.0 % |
| compaction | 3 | 0.1 % |

| Terminaison assistant | Nombre | Part des assistants |
|---|---:|---:|
| tool-calls | 515 | 62.2 % |
| stop | 312 | 37.7 % |
| Non exposée/part active au snapshot | 1 | 0.1 % |

| Outil natif | Terminés | Erreurs | Total | Part des appels |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 116 | 0 | 116 | 19.5 % |
| cgpt-validation_request_validation | 163 | 9 | 172 | 28.9 % |
| cgpt-validation_get_approval | 8 | 0 | 8 | 1.3 % |
| cgpt-validation_cancel_approval | 4 | 0 | 4 | 0.7 % |
| bash | 96 | 2 | 98 | 16.4 % |
| read | 71 | 1 | 72 | 12.1 % |
| glob | 10 | 0 | 10 | 1.7 % |
| write | 67 | 0 | 67 | 11.2 % |
| cgpt-validation_list_pending | 22 | 0 | 22 | 3.7 % |
| cgpt-validation_broker_health | 27 | 0 | 27 | 4.5 % |

Les demandes request_validation en erreur incluent les délais de transport et validations refusées avant admission ; elles ne sont pas converties en décisions CAB. Les annulations, lectures de statut, once et effets ont leurs traces distinctes.

## 3. Fichiers modifiés

Table des tentatives d'effet de fichier attribuables aux outils write/edit et aux manifestes Bash avec cible de fichier explicite. Les fins natives réussies ne constituent pas à elles seules une validation métier. Les cibles de répertoire, binaires extraits et fichiers individuels non observables ne sont pas inventés. Les pourcentages portent sur 113 tentatives observées, pas sur les lignes de code.

| Chemin absolu actuel ou historique remappé après archive | Réussies après autorisation | Refus natif | Erreur d'exécution | Part des tentatives |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions/design.md | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 8.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) | 1.8 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions/requirements.md | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions/tasks.md | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions/VALIDATION.md | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/pyproject.toml | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/__init__.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/activity.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/src/pixs/auth/apps.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/src/pixs/auth/bootstrap_backend.py | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 3.5 % |
| /home/devops/datas/pixs/src/pixs/auth/cli_vault.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/cli.py | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2.7 % |
| /home/devops/datas/pixs/src/pixs/auth/component.toml | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/configuration.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/src/pixs/auth/contracts.py | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2.7 % |
| /home/devops/datas/pixs/src/pixs/auth/credentials.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/facades.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/identifiers.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/invocation.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/migration_lock.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/src/pixs/auth/migrations/__init__.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/migrations/0001_auth_initial.py | 5 (71.4 %) | 0 (0.0 %) | 2 (28.6 %) | 6.2 % |
| /home/devops/datas/pixs/src/pixs/auth/models.py | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 5.3 % |
| /home/devops/datas/pixs/src/pixs/auth/mutation_guard.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/passwords.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/policy.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/r01.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/README.md | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/reconciliation.py | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2.7 % |
| /home/devops/datas/pixs/src/pixs/auth/refresh.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/src/pixs/auth/resource_metadata.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/runtime_verifier.py | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2.7 % |
| /home/devops/datas/pixs/src/pixs/auth/services.py | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 6.2 % |
| /home/devops/datas/pixs/src/pixs/auth/tokens.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/src/pixs/auth/withdrawals.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/TECHNICAL.md | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/auth_pg_test_support.py | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 4.4 % |
| /home/devops/datas/pixs/tests/integration/auth_service_fixture.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_activity_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_bootstrap_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_configuration_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_core_audit_postgres.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/tests/integration/test_auth_credentials_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_facades_postgres.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/tests/integration/test_auth_login_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_password_ldap_integration.py | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2.7 % |
| /home/devops/datas/pixs/tests/integration/test_auth_refresh_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/integration/test_auth_storage_postgres.py | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1.8 % |
| /home/devops/datas/pixs/tests/integration/test_auth_verifier_postgres.py | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 3.5 % |
| /home/devops/datas/pixs/tests/integration/test_auth_withdrawal_postgres.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_cli_vault.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_component.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_facades.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_identifiers.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_passwords.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_policy.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_r01.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| /home/devops/datas/pixs/tests/unit/test_auth_tokens.py | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 0.9 % |
| Total | 110 (97.3 %) | 0 (0.0 %) | 3 (2.7 %) | 100,0 % |

Déplacement réel unique : /home/devops/datas/pixs/openspec/changes/add-initial-authentication-and-sessions vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-add-initial-authentication-and-sessions, natif prt_15cb95b79001jdK7mqOBJc6OYs. Les chemins historiques correspondants sont remappés dans cette table. Les corrections de transcription et le refus sûr du pilote documentaire sont conservés, puis les contenus finaux sont vérifiés exactement. Les exclusions Syncthing autorisées et les corrections du dépôt CAB relèvent du rapport CAB séparé ; elles ne sont pas attribuées aux écritures natives de cette session.

## 4. Commandes

| Famille | Nombre | Part des Bash | Fins natives completed | Erreurs d'outil | Codes non nuls |
|---|---:|---:|---:|---:|---:|
| Prévol sans effet | 5 | 5.1 % | 5 | 0 | 0 |
| Dépendances et qualification D11 | 4 | 4.1 % | 4 | 0 | 1 |
| Tests et syntaxe Python | 19 | 19.4 % | 19 | 0 | 3 |
| Autres qualifications | 6 | 6.1 % | 6 | 0 | 0 |
| Qualification PostgreSQL | 25 | 25.5 % | 23 | 2 | 4 |
| Transferts sources/documentation | 36 | 36.7 % | 36 | 0 | 1 |
| Validation OpenSpec | 2 | 2.0 % | 2 | 0 | 0 |
| Archivage OpenSpec | 1 | 1.0 % | 1 | 0 | 0 |

Commandes en erreur native, regroupées sans les présenter comme exécutées :

| Libellé, au plus 100 caractères | Nombre | Part des Bash | État |
|---|---:|---:|---|
| cd /home/devops/datas/pixs && .venv/bin/python -m py_compile src/pixs/auth/runtime_verifier.py test… | 1 | 1.0 % | Refus de permission native |
| /home/devops/datas/pixs/.venv/bin/python -B -c 'import base64,zlib,hashlib,json,os;from pathlib imp… | 1 | 1.0 % | Refus de permission native |

Les 9 codes non nuls d'exécutions approuvées restent des résultats de commande, dont les échecs de recette corrigés ; ils ne sont ni masqués ni assimilés à un refus d'autorisation. Les recettes finales réussies sont indiquées dans VALIDATION.md.

## 5. Accès web

Dans l'historique natif de la session : aucun outil web d'accès/recherche ; 0 approbation, 0 refus, 0 erreur web natifs. Pourcentages de décision web : N/A, dénominateur zéro. Les téléchargements de dépendances D11 effectués par commandes sont comptabilisés comme Bash ; leur inventaire technique est dans le banc/checkpoint, pas transformé en appels d'un outil web.

L'orchestrateur a consulté les deux sources officielles ci-dessous avant cette clôture ; elles sont hors du compteur OpenCode. Le nombre complet de ses requêtes, leurs durées et les URL de téléchargements non présentes dans cette télémétrie sont N/A, historique propriétaire non disponible. Aucun refus d'accès web de l'orchestrateur n'est prouvé.

| URL connue, au plus 100 caractères | Statut |
|---|---|
| https://docs.syncthing.net/users/ignoring.html | Consultée, source de la remédiation autorisée |
| https://argon2-cffi.readthedocs.io/en/stable/api.html | Consultée, source de qualification D11 |

Une URL de fixture auth.example.test ou c03-vault-qualification.invalid n'est pas une visite réelle et n'est pas comptée comme telle. Aucun accès externe n'est déduit d'une chaîne trouvée dans un test.

## 6. Synthèse globale

| Durée de la session de codage reconstruite | Valeur |
|---|---|
| Début effectif, création native | 2026-10-20T17:41:12.886Z |
| Fin — après archivage, relevé final des quotas | 2026-10-21T04:37:04.511Z |
| Durée globale, pauses et attentes incluses | 10 h 55 min 51 s |

Ces bornes couvrent la nouvelle session mesurable et le contexte CAB433. Durée globale de l'ancien historique parent devenu404 : N/A, borne native complète non récupérable ; aucune durée manquante n'est reconstruite. La maintenance CAB et les attentes sont incluses dans la durée calendaire mesurée, pas additionnées aux temps d'autres agents.

| Relevé Codex sur sept jours, mcp__codex_app__get_usage_limits | Utilisation | Fenêtre/réinitialisation |
|---|---:|---|
| Avant reconstruction — 2026-10-20T17:40:35.546Z | 31 % | 10080min ; 1793082828 |
| Après archive — 2026-10-21T04:37:04.511Z | 83 % | 10080min ; 1793082828 |
| Différence attribuable/vérifiable | N/A | Identité de compte initiale non capturée ; compte partagé et autres RUN actifs. Aucune consommation propre au RUN déduite. |

| Domaine d'appels natifs, sans double compte | Nombre | Part globale | Approbations explicites observables | Refus natifs | Erreurs observées |
|---|---:|---:|---|---|---|
| Fichiers : outils natifs write/edit | 67 | 11.2 % | 67 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Commandes : Bash | 98 | 16.4 % | 96 / 98.0 % | 2 / 2.0 % | 9 / 9.2 % |
| Web : outils natifs | 0 | 0.0 % | 0 / N/A | 0 / N/A | 0 / N/A |
| Autres outils, dont MCP/lectures | 431 | 72.3 % | N/A — lectures/diagnostics sans décision individuelle | N/A | 10 / 2.3 % |
| Global | 596 | 100,0 % | 165 décisions CAB distinctes | 2 refus de permission natifs | 12 erreurs d'outil ; 9 codes Bash non nuls distincts |

Les axes approbation, refus natif et issue d'exécution ne s'additionnent pas : une commande approuvée peut échouer. La table globale partitionne seulement les appels d'outils ; la table des tentatives de fichiers recoupe certains Bash et n'est pas ajoutée à cette partition. Taux de fin native completed global : 98.0 % ; taux d'erreur d'outil : 2.0 %. Taux de refus CAB : 0.0 %.

Tests finaux réussis et archive effective prouvés. L'archive a émis un avertissement non bloquant sur les titres français de proposition et a laissé3.4 ouverte jusqu'au présent rapport ; la tâche est ensuite clôturée sous mandat distinct après vérification effective. Git : aucun commit/push dans ce RUN. Aucun service OpenCode/CAB partagé ni autre RUN n'est arrêté. Pas d'activation P0 globale ; trousseau mémoire constaté. Les valeurs privées PG restent dans les seuls processus de test, sorties masquées ; aucun secret réel n'est ajouté aux sources, arguments ou rapport. Publication et gates sont prouvés séparément dans le checkpoint et ne sont jamais déduits du seul rapport.
