# Statistiques — C04 autorisation runtime et Super Admin

RUN : cismp3-pixs-f2197224acbc47c0. Change : integrate-runtime-authorization-and-super-admin. Session OpenCode : ses_ea58912eeffeqSU1dq1rUdGWyZ. Contexte CAB repris : 443 ; contexte antérieur 439 clos BLOQUÉ puis libéré ABANDONED après incident sans écriture. Reprise autorisée par « Tu Peux reprendre le change ».

Intervalle : création effective de la session native jusqu’au relevé final de quota, après l’archive et la sonde finale. Le rapport, sa propre écriture et le gate ultérieur sont hors de cet intervalle ; leur preuve figure dans le checkpoint du RUN. Les pairs CISMP1/2/4/5 sont exclus des volumes de cette session. Les 21 scénarios communs sont rapportés comme preuve distincte de CISMP1.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte distincte non exposée | opencode-go | high | 2.4146 s — 10 sondes | 340.9632 — 10 sondes | N/A — temps actif du modèle non isolé |
| muse-spark-1.3-contributor — compactage | N/A — non exposée | opencode-go | N/A — absent sur 3 réponses | N/A — non sondé séparément | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex — session 01a15a73-7f64-7960-b5b1-665d26006676 | N/A — télémétrie exacte non exposée | OpenAI | N/A — non exposé | N/A — aucune sonde orchestrateur | N/A | N/A — durée active non exposée |

Les métriques de performance proviennent exclusivement des sondes jetables sans outil, avec le même modèle et high. La version n’est pas déduite de « 1.3 ». Le dénominateur des temps de service de tous les agents est indisponible : aucune part n’est inventée. Busy, attente, outils et durée calendaire ne sont pas du temps de génération.

## 1. Statistiques générales et décisions

Durée calendaire : 08 h 01 min 48 s, pauses, incident CAB, attente, tests et archivage inclus. Début : 2026-10-20T19:58:25+02:00 ; fin : 2026-10-21T04:00:14+02:00.

Sources : API native complète de la session (623 messages, bornée au relevé final), checkpoint et empreintes des mandats ; export /runs/<RUN>/statistics du contexte 443. Les compteurs CAB commencent à la reprise 2026-10-20T23:34:53+02:00 et ne remplacent pas l’historique natif antérieur. Les consultations HTTP de collecte postérieures à la borne ne sont pas ajoutées aux messages natifs.

| Décision CAB — contexte 443 | Nombre | Part |
|---|---|---|
| approved | 69 | 92.0 % |
| rejected | 6 | 8.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 75 | 100.0 % |

Permissions natives once : 69/69 approbations (100.0 %). Les six refus CAB ont précédé les effets concernés ; ils ne sont pas six éditions de fichier refusées. Les délais MCP ne valent pas refus : les demandes existantes ont été interrogées, sans rejouer une permission consommée.

Convention : « terminé » désigne un appel natif completed, sans conclure automatiquement à une approbation manuelle ni au succès d’un test. Les 48 écritures natives et les commandes exécutées disposent de mandats et de preuves once ; les lectures autorisées automatiquement restent des outils terminés. Refus : erreur native explicite de permission. Erreur technique : timeout, interruption, entrée MCP invalide ou lecture absente. Un Bash completed avec exit 1 reste un échec de test distinct.

| Validation finale | Résultat | Couverture |
|---|---|---|
| Unitaires | 192/192 (100.0 %) | 16 modules ; dernière exécution prt_15c1f237e001U4gfistvx75LNk |
| PG propres C04 | 113/113 (100.0 %) | 8 familles : 10+27+18+14+14+10+12+8 ; scénarios distincts |
| Régression Core C02 | 200/200 (100.0 %) | 20+46+14+62+58 ; migrations : 12 garanties distinctes |
| Banc commun Auth/Core/Audit | 21/21 (100.0 %) | CISMP1 prt_15c219d16001TUYoqUW4d5vuXs recoupé ; fixtures de configuration explicites |
| Syntaxe | 25/25 (100.0 %) | Python ; UTF-8/LF : 28/28 lors du contrôle final avant les dernières éditions documentaires |
| Empreintes propres avant publication | 29/29 (100.0 %) | 25 Python et 4 documents rédigés ; tous relus, UTF-8/LF |
| OpenSpec strict | 191/191 (100.0 %) avant archive | 113 changes + 78 spécifications ; C04 strict relancé juste avant archive |

Ces familles ne sont pas additionnées aux réexécutions intermédiaires. Un essai PG exit 1 a révélé une obligation AUDIT absente d’une politique produite ; correction puis recette verte. Aucun test frontend : aucun changement frontend. Python 3.14.8, Django 6.1.2, PostgreSQL 16.14 observés.

| Tokens natifs de production — réponse API | Nombre | Part du total |
|---|---|---|
| input | 4 459 235 | 4.1 % |
| output | 347 470 | 0.3 % |
| reasoning | 75 859 | 0.1 % |
| cache.read | 105 078 378 | 95.6 % |
| cache.write | 0 | 0.0 % |
| Total | 109 960 942 | 100.0 % |

Coût natif agrégé : 0.740746056, unité monétaire de la télémétrie OpenCode ; aucune conversion. Les tokens d’entrée cumulés comptent les contextes relus ; ils ne représentent pas un corpus unique. Les sondes ne sont pas incluses. Métadonnées : 401 réponses high et 3 réponses de compactage sans variant exposé.

### Sondes de performance et surcharge

| Position | Horodatage Paris | TTMT (s) | Tokens sortie | Débit tokens/s | Retard documenté (s) |
|---|---|---|---|---|---|
| reprise | 2026-10-20T23:37:00.905979+02:00 | 2.4739 | 283 | 593.0130 | N/A — échéance précise non conservée |
| +30min après reprise | 2026-10-21T00:08:20.760654+02:00 | 1.7730 | 265 | 864.3038 | N/A — échéance précise non conservée |
| +60min après reprise, relevé courant retardé | 2026-10-21T00:43:33.667397+02:00 | 2.0780 | 264 | 235.5975 | 310.8 |
| reprise +90 min | 2026-10-21T01:08:28.169393+02:00 | 2.6138 | 300 | 163.6319 | N/A — échéance précise non conservée |
| reprise +120 min | 2026-10-21T01:40:10.585050+02:00 | 2.3725 | 282 | 191.8059 | 97.8 |
| reprise +150 min (retard de suivi pendant revue technique) | 2026-10-21T02:24:24.581740+02:00 | 2.8922 | 278 | 118.2957 | 951.8 |
| reprise +180 min | 2026-10-21T02:40:57.077159+02:00 | 1.7531 | 265 | 977.7128 | 144.3 |
| reprise +210 min | 2026-10-21T03:09:14.130074+02:00 | 3.2773 | 276 | 76.9445 | 41.4 |
| reprise +240 min | 2026-10-21T03:39:37.779295+02:00 | 2.4587 | 278 | 129.4526 | 65.0 |
| fin après archivage | 2026-10-21T03:59:50.405996+02:00 | 2.4533 | 295 | 58.8737 | N/A — échéance précise non conservée |

Sonde initiale avant codage : session ses_ea589eb94ffe1QEEoi8657G39Q, 287 tokens, réponse réussie en 3.0187 s ; premier/dernier delta SSE non conservés, TTMT et débit N/A. Total : 11 sondes prévues et 11 réponses réussies (100.0 %), dont une initiale, une de reprise, huit périodiques et une finale ; 10/11 mesures TTMT/débit exploitables (90.9 %). Échecs : 0/11 (0.0 %). Six relèves périodiques ont un retard documenté ; les créneaux exacts manqués ne sont pas reconstitués rétroactivement. Le retard de 951.8 s correspond à la revue technique. Aucune sonde pendant la pause CAB.

TTMT min/moy/max : 1.7531/2.4146/3.2773 s. Débit min/moy/max : 58.8737/340.9632/977.7128 tokens/s, moyenne arithmétique des 10 sondes valides. Ces débits reposent sur les événements SSE parfois groupés ; ils ne constituent pas un débit de production. Surcharge : 3073 tokens de sortie ; coût connu 0.011458292 sur 9/11 sondes (81.8 %), coût total N/A (initiale et reprise non conservés). Durée totale de génération des 11 sondes N/A (mesures incomplètes), sans addition au temps de production.

Trois compactages OpenCode prouvés : msg_15b7a7d4e001ShOqQo6NlRnzcn, msg_15ba87998001ITGuIQKaZ0rvZ4 et msg_15c157493001Ri1gRF5xu5ly9L. API de compactage Codex non exposée ; aucun succès conjoint déclaré.

## 2. Types de messages et d’outils

| Rôles | Nombre | Part |
|---|---|---|
| user | 219 | 35.2 % |
| assistant | 404 | 64.8 % |
| Total | 623 | 100.0 % |

| Types de parties | Nombre | Part |
|---|---|---|
| text | 564 | 25.4 % |
| step-start | 404 | 18.2 % |
| reasoning | 468 | 21.1 % |
| tool | 379 | 17.1 % |
| step-finish | 402 | 18.1 % |
| compaction | 3 | 0.1 % |
| Total | 2220 | 100.0 % |

| Terminaisons assistant | Nombre | Part |
|---|---|---|
| tool-calls | 264 | 65.3 % |
| stop | 138 | 34.2 % |
| absent | 2 | 0.5 % |
| Total | 404 | 100.0 % |

| Type | Appels | Part | Terminés | Refusés | Erreur technique |
|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 26 | 6.9 % | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 79 | 20.8 % | 61 (77.2 %) | 0 (0.0 %) | 18 (22.8 %) |
| bash | 23 | 6.1 % | 22 (95.7 %) | 1 (4.3 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 22 | 5.8 % | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 129 | 34.0 % | 128 (99.2 %) | 0 (0.0 %) | 1 (0.8 %) |
| glob | 5 | 1.3 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 18 | 4.7 % | 18 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 12 | 3.2 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 48 | 12.7 % | 48 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 4 | 1.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 10 | 2.6 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 2 | 0.5 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 379 | 100.0 % | 359 (94.7 %) | 1 (0.3 %) | 19 (5.0 %) |

Les 18 erreurs request_validation comprennent 15 timeouts, deux entrées MCP -32602 avant enregistrement et une interruption. Une lecture a visé un rapport alors encore absent. Le seul refus natif Bash est la commande de contrôle non mandatée ci-dessous, sans exécution. Les états CAB et les erreurs natives décrivent des couches distinctes et ne s’additionnent pas.

| Refus HTTP de coordination observé — contexte 443 | Nombre | Part |
|---|---|---|
| resource-revision-stale | 1 | 0.3 % |
| native-validation-not-correlated | 40 | 10.6 % |
| run-accesses-unresolved | 1 | 0.3 % |
| native-session-not-quiescent | 3 | 0.8 % |
| reconciliation-resources-required | 1 | 0.3 % |
| reservation-version-stale | 330 | 87.5 % |
| reservation-invalid | 1 | 0.3 % |
| Total | 377 | 100.0 % |

Ces refus de coordination incluent des rappels du superviseur sur des révisions de réservation périmées ; ils ne représentent pas autant de commandes métier ni d’effets exécutés. Leur attribution détaillée N/A dans cet agrégat. Readiness finale observée READY ; aucun effet inconnu conservé par C04 avant publication.

## 3. Fichiers modifiés

Il s’agit de tentatives natives write/edit, pas de lignes modifiées ni de fichiers Git. 48 écritures terminées, 29 chemins distincts ; 0 refus et 0 erreur d’écriture. La présente écriture STATISTIQUES.md, postérieure à la borne, est exclue.

| Chemin absolu au moment de l’écriture | Tentatives | Part | Terminées sous once | Refusées | Erreur |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/integrate-runtime-authorization-and-super-admin/design.md | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/bootstrap_operator.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bootstrap_operator.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/ports.py | 3 | 6.2 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_bootstrap_facts.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_bootstrap.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_transactions.py | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_common.py | 3 | 6.2 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_core_bootstrap_r01.py | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/decision.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_runtime_authorization_admission.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_authorization_guard.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_authorization_guard.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_store.py | 3 | 6.2 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_decider.py | 5 | 10.4 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_authorization.py | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_filter.py | 3 | 6.2 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_authorization_filter.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_declarations.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_authorization_declarations.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_bootstrap.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_authorization_bootstrap.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_facts.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_auth_finalizer.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_trusted_facts.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_auth_freshness.py | 1 | 2.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/integrate-runtime-authorization-and-super-admin/VALIDATION.md | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/integrate-runtime-authorization-and-super-admin/proposal.md | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/integrate-runtime-authorization-and-super-admin/tasks.md | 2 | 4.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 48 | 100.0 % | 48 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Déplacement autorisé par OpenSpec : /home/devops/datas/pixs/openspec/changes/integrate-runtime-authorization-and-super-admin vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-21-integrate-runtime-authorization-and-super-admin. requirements.md, delta et métadonnées préexistants ont été déplacés sans rédaction par cette session. Le canon authorization/spec.md est inchangé : SHA-256 c09e4dac79ecbe6bdb16550d8a4d1566307127818cdeaf9dfbe9224f50858310. Cache régénérable de tests sous tests/runtime/c04-cache ; schémas PG temporaires nettoyés et connexions closes selon les recettes. Aucun changement de migration, configuration, branche ou infrastructure par C04.

## 4. Commandes

| Famille | Nombre | Part |
|---|---|---|
| Prévol | 2 | 8.7 % |
| Python : syntaxe, tests unitaires et PostgreSQL | 17 | 73.9 % |
| Contrôle non mandaté refusé | 1 | 4.3 % |
| Revue OpenSpec et pré-archivage | 2 | 8.7 % |
| Archivage OpenSpec | 1 | 4.3 % |
| Total | 23 | 100.0 % |

Bash : 23 tentatives ; 22 terminées (95.7 %), dont 21 exit 0 et une exit 1 ; une refusée avant effet (4.3 %). La réussite finale de chaque famille est prouvée indépendamment des essais intermédiaires. Les scripts multilignes sont représentés ci-dessous par leur préfixe, limité à 100 caractères ; la commande intégrale exacte reste dans le mandat natif et le checkpoint.

| Libellé de commande, 100 caractères maximum | État natif | Exit | Occurrences | Part |
|---|---|---|---|---|
| /usr/bin/true | completed | 0 | 2 | 8.7 % |
| PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/c04-cache /home/devops/datas/pixs/.venv... | completed | 0 | 3 | 13.0 % |
| PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/c04-cache PYTHONPATH=src:tests/unit /ho... | completed | 0 | 5 | 21.7 % |
| python3 -c "import hashlib,pathlib; p=pathlib.Path('/home/devops/datas/pixs/src/pixs/core/service... | refused | None | 1 | 4.3 % |
| PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/c04-cache PYTHONPATH=src:tests/unit:tes... | completed | 0 | 8 | 34.8 % |
| PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/c04-cache PYTHONPATH=src:tests/unit:tes... | completed | 1 | 1 | 4.3 % |
| PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/python3 - <<'C04_OPENSPEC_REVIEW' imp... | completed | 0 | 1 | 4.3 % |
| PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/python3 - <<'C04_PREARCHIVE' import h... | completed | 0 | 1 | 4.3 % |
| PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/python3 - <<'C04_ARCHIVE' import hash... | completed | 0 | 1 | 4.3 % |

### Toutes les commandes refusées

| Libellé refusé, 100 caractères maximum | Occurrences | Part des tentatives Bash |
|---|---|---|
| python3 -c "import hashlib,pathlib; p=pathlib.Path('/home/devops/datas/pixs/src/pixs/core/service... | 1 | 4.3 % |

Ce contrôle python3 -c hors mandat a été refusé avant exécution. Aucun commit, push, changement de branche, déploiement ou commande d’arrêt global exécuté par cette session.

## 5. Accès web

| Statut des outils web natifs | Nombre | Taux |
|---|---|---|
| Approuvés / terminés | 0 | N/A — aucun appel |
| Refusés | 0 | N/A — aucun appel |
| Erreur technique | 0 | N/A — aucun appel |
| Total | 0 | N/A — dénominateur nul |

Aucun outil web dans les 379 appels natifs, aucune URL externe approuvée ou refusée à lister. L’orchestrateur n’a effectué aucune recherche web dans ce RUN. Les échanges HTTP locaux OpenCode/CAB et la lecture du quota sont du pilotage, pas des visites web. Les sondes ont leurs outils désactivés et n’ont aucun accès projet ou réseau.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-20T19:58:25+02:00 |
| Fin — après archivage | 2026-10-21T04:00:14+02:00 |
| Durée globale (pauses et attentes incluses) | 08 h 01 min 48 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-20T19:57:00.021414+02:00 | 34 % | 2026-10-27T07:33:48+01:00 |
| Après — après archivage de la spécification | 2026-10-21T04:00:14+02:00 | 75 % | 2026-10-27T07:33:48+01:00 |
| Différence après − avant | — | 41 points de pourcentage | — |

Même compte, quota codex, fenêtre 10080 minutes et même réinitialisation vérifiés. Le quota est partagé : sa variation inclut potentiellement les autres chats simultanés ; elle n’est pas attribuée exclusivement à C04 et n’est convertie ni en tokens ni en euros. Le relevé initial précède la création de la session et les sondes. La rédaction ultérieure de ce rapport est hors intervalle du relevé final.

| Type | Appels | Part | Terminés | Refusés | Erreur technique |
|---|---|---|---|---|---|
| Fichiers (write/edit) | 48 | 12.7 % | 48 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes (bash) | 23 | 6.1 % | 22 (95.7 %) | 1 (4.3 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 308 | 81.3 % | 289 (93.8 %) | 0 (0.0 %) | 19 (6.2 %) |
| Total | 379 | 100.0 % | 359 (94.7 %) | 1 (0.3 %) | 19 (5.0 %) |

Publication CAB acquittée : c3-publication-4025015ac89f4d399af4dbec4405a029, référence 52, génération 508. Archive native prt_15c2f33da001V6HCnxiA24mala, exit 0, source absente/destination présente, aucune modification de spécification canonique (specsUpdated false). Aucun skip-specs ni no-validate.

Coordination du contexte repris : attente de ressource 0.0 s ; détention partagée 9140.782 s ; activité exclusive 0.0 s ; une réconciliation ciblée 0.033 s. Ces durées peuvent se recouvrir ; aucun gain de parallélisme causal n’en est déduit. L’interruption historique du contrôleur est une inconnue globale, pas une durée de panne attribuable à C04.

Tests et archivage C04 sont prouvés. Le banc commun utilise des fixtures explicites de trust/assurance/catalogue/plans ; il ne démontre ni la livraison complète C03/C08/C10, ni le P0 hôte, ni le cycle global Pixs. La phase REPORT ne couvre plus que ce fichier. Le gate terminal, le désarmement et la libération ciblée seront constatés après vérification du rapport, dans le checkpoint ; aucun gate futur n’est déclaré acquis ici. Git sans effet, services OpenCode/CAB partagés préservés, aucun change suivant. Aucun secret ajouté ou affiché dans les preuves de cette session ; les paramètres PG ont été traités uniquement par le helper local existant sans sortie de valeur.
