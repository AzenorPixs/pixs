# STATISTICS.md — PA02 add-pa-bootstrap-and-authority-binding

change ouvert — dépendances manquantes — archivage en attente

[Bilan de dépendances](./BLOCKERS.md)

Cumul de TOUTES les sessions et contextes CAB identifiés pour PA02 depuis le début observé, sans filtre de reprise. 5 sessions dédupliquées : ses_e886389f6ffe87Pl7ANpdw320l, ses_e886174a7ffecXneyk2X9wy7i4, ses_e8849feb2ffeEvVmwQDe9UqCLC, ses_e8844a6a8ffeOn5bpp6Si0Exc0, ses_e87924dd3ffeDgY0V6ZN1aJvDC. Contextes 1223 ABANDONED et 1368 RESERVED du même RUN cismp2-pixs-797dcac8c8814e27. Préparation plus ancienne sans activité attribuable = N/A. Registre BATCH_CODES inchangé. Map actuelle TOUJOURS BLOQUÉ 1/10. Création du présent fichier après le gel, exclue des compteurs pour éviter toute auto-référence. Contrôles et clôture postérieurs consignés dans le checkpoint sans résultat anticipé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 3.227712 | 291.5214 | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | medium | 2.9935 | 201.2123 | N/A |

Temps actif et pourcentage de service = N/A pour tous, sans estimation. Répartition des messages par configuration, distincte du temps de service : high 361 messages avec usage, medium 44 messages avec usage, total assistant avec usage 405. Coût natif sans unité monétaire inventée, sans addition cache/input dont le recouvrement est inconnu : high input 5950394, output 279483, reasoning 184223, cacheRead 57255166, cacheWrite 0, nativeCost 0.8022909319999999 ; medium input 2626349, output 20039, reasoning 7720, cacheRead 15097158, cacheWrite 0, nativeCost 0. Sondes mesurées : high 7, medium 2 dont finale réussie après CABU ; relève de 30 minutes d'échéance 2026-10-30T05:10:49.451Z, constatée manquée le 2026-10-30T05:11:44.629Z pendant la maintenance CAB partagée, non reconstruite ; collecte exhaustive des sondes prévues non prouvée = N/A. Compactions visibles : 4 enregistrements. Sorties observées des sondes : high 12069 tokens + medium 2642 tokens = 14711 tokens, 9 sondes dédupliquées distinctes des 5 sessions de production ; coût et durée exhaustifs de cette surcharge N/A car traces historiques incomplètes, sans mélange aux compteurs de production. Plages observées, sans somme entre configurations : high TTMT 1.3559226989746094–4.536646366119385 s, TPS 177.2867416874125–741.9635720823213 ; medium TTMT 2.963–3.024 s, TPS 182.9893337027289–219.43521594684387.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex orchestrateur | N/A | N/A | N/A | N/A | N/A | N/A |

Modèle et raisonnement exacts non exposés, métriques N/A, temps de service N/A.

## 1. Statistiques générales et décisions

Messages natifs 654 : user 220 (33.6%), assistant 405 (61.9%), system 11 (1.7%), compaction 4 (0.6%), model-switched 1 (0.2%), idle 13 (2.0%), total 100.0%. Appels outils natifs 339. Fins : tool-calls 261, stop 138, error 1, non renseigné 5, total 405.

Décisions CAB 70 : approved 69 (98.6%), rejected 1 (1.4%), needs_clarification 0 (0.0%), pending 0 (0.0%), total 100.0%. Once 65, distinct des appels natifs. TechnicalErrors 0. Une source COMPLÉTÉE ne prouve ni test ni permission manuelle. Refus CAB formel unique : /usr/bin/true, distinct des 16 erreurs natives.

Contexte 1223 : reserved 23764411 ms, busy 6390976 ms, idle 17263782 ms, nativeUnknown 109653 ms. Contexte 1368 : reserved 4223247 ms, busy 886318 ms, idle 3250201 ms, nativeUnknown 86728 ms. Coordination technique CAB, pas qualification produit.

## 2. Types de messages et d'outils

| Outil | Total | Part | COMPLETED | Erreur | Taux COMPLETED | Taux erreur |
|---|---|---|---|---|---|---|
| read | 78 | 23.0 % | 78 | 0 | 100.0 % | 0.0 % |
| glob | 13 | 3.8 % | 13 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_broker_health | 1 | 0.3 % | 1 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_broker_readiness | 64 | 18.9 % | 64 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_list_pending | 2 | 0.6 % | 2 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_broker_remediation_registry | 1 | 0.3 % | 1 | 0 | 100.0 % | 0.0 % |
| bash | 67 | 19.8 % | 62 | 5 | 92.5 % | 7.5 % |
| cgpt-validation_request_validation | 72 | 21.2 % | 64 | 8 | 88.9 % | 11.1 % |
| cgpt-validation_get_approval | 16 | 4.7 % | 16 | 0 | 100.0 % | 0.0 % |
| grep | 10 | 2.9 % | 10 | 0 | 100.0 % | 0.0 % |
| write | 1 | 0.3 % | 0 | 1 | 0.0 % | 100.0 % |
| cgpt-validation_poll_approval | 7 | 2.1 % | 6 | 1 | 85.7 % | 14.3 % |
| cgpt-validation_cancel_approval | 1 | 0.3 % | 1 | 0 | 100.0 % | 0.0 % |
| cab_codemode_discovery | 2 | 0.6 % | 2 | 0 | 100.0 % | 0.0 % |
| edit | 4 | 1.2 % | 3 | 1 | 75.0 % | 25.0 % |
| Total | 339 | 100.0 % | 323 | 16 | 95.3 % | 4.7 % |

Arrondis à 1 décimale, total 100.0%, écarts possibles d'arrondi. Tools en attente finale 0.

## 3. Fichiers modifiés

Historique 13 fichiers, 31 opérations attribuables dédupliquées requestId : 28 COMPLETED (90.3%), 3 sans effet (9.7%), total 100.0%.

| Fichier absolu | Total | Part | COMPLETED | Sans effet |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/contracts.md | 7 | 22.6 % | 5 | 2 |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/identity-bindings.md | 3 | 9.7 % | 3 | 0 |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/authority-policy.md | 3 | 9.7 % | 3 | 0 |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/design.md | 3 | 9.7 % | 3 | 0 |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/tasks.md | 5 | 16.1 % | 5 | 0 |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/requirements.md | 1 | 3.2 % | 1 | 0 |
| /home/devops/datas/pixs/src/pixs/pa_native/provisioning_contracts.py | 1 | 3.2 % | 1 | 0 |
| /home/devops/datas/pixs/tests/unit/test_pa_provisioning_contracts.py | 2 | 6.5 % | 1 | 1 |
| /home/devops/datas/pixs/src/pixs/pa_native/provisioning_bindings.py | 1 | 3.2 % | 1 | 0 |
| /home/devops/datas/pixs/tests/unit/test_pa_provisioning_bindings.py | 1 | 3.2 % | 1 | 0 |
| /home/devops/datas/pixs/src/pixs/pa_native/provisioning_store.py | 2 | 6.5 % | 2 | 0 |
| /home/devops/datas/pixs/tests/unit/test_pa_provisioning_store.py | 1 | 3.2 % | 1 | 0 |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/BLOCKERS.md | 1 | 3.2 % | 1 | 0 |
| Total | 31 | 100.0 % | 28 | 3 |

Incrément de reprise, tableau séparé, 4 opérations distinctes des 31 opérations historiques, sans ajouter STATISTICS au comptage gelé :

| Fichier absolu | État | requestId | Résultat | Part |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/BLOCKERS.md | VERIFIED | pa02-doc-dc23fc1b2c4d4f8892212adb7e763d86 | COMPLETED | 25.0% |
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | DEFERRED_NO_EFFECT | pa02-doc-26a12196fc4c457b9e9fe0c45eba66a2 | sans effet, sans once | 25.0% |
| /home/devops/datas/pixs/openspec/changes/add-pa-bootstrap-and-authority-binding/tasks.md | VERIFIED | pa02-doc-7348b1eda70749db99987f2c9c3fb159 | COMPLETED | 25.0% |
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | VERIFIED | pa02-doc-78e5bff2e46448e08243bdb0dddfc26f | COMPLETED | 25.0% |
| Total | 4 | 100.0% | 3 COMPLETED, 1 sans effet | 100.0% |

## 4. Commandes

Familles par EXÉCUTABLE, 67 commandes : curl 1 erreur, true 9 COMPLETED + 1 erreur, openspec 13 COMPLETED, python3 40 COMPLETED + 3 erreurs ; soit 62 COMPLETED et 5 erreurs au sens shell natif avec sorties, total 67. Seul refus CAB formel : /usr/bin/true.

| Exécutable | Total | Part | COMPLETED | Erreur | Taux COMPLETED | Taux erreur |
|---|---|---|---|---|---|---|
| curl | 1 | 1.5 % | 0 | 1 | 0.0 % | 100.0 % |
| true | 10 | 14.9 % | 9 | 1 | 90.0 % | 10.0 % |
| openspec | 13 | 19.4 % | 13 | 0 | 100.0 % | 0.0 % |
| python3 | 43 | 64.2 % | 40 | 3 | 93.0 % | 7.0 % |
| Total | 67 | 100.0 % | 62 | 5 | 92.5 % | 7.5 % |

## 5. Accès web

| Périmètre | Accès observés | Dénominateur | Part |
|---|---|---|---|
| Sessions PA02 | 0 | 0 | N/A |

0 observé dans les sessions, pas une absence globale prouvée. URLs N/A, dénominateur 0. Global orchestrateur non collecté.

## 6. Synthèse globale

| Durée | Valeur |
|---|---|
| Première trace native | 2026-10-26T09:48:46.241Z |
| Borne de collecte | 2026-10-30T05:47:58.958Z |
| Durée calendaire provisoire pauses incluses | 91 h 59 min 12 s |
| Fin du change | EN ATTENTE |
| Fin de reprise | NON ANTICIPÉE, au gel EN COURS |

| Quotas, source mcp__codex_app__get_usage_limits | Valeur |
|---|---|
| Historique 31% au 2026-10-25T12:10:40.232249+00:00, reset 1793516785 | 31% |
| Initial reprise au 2026-10-30T04:35:15.695Z, reset 1793774753 | 62% |
| Final reprise au 2026-10-30T05:47:35.554Z, reset 1793774753 | 73% |
| Variation reprise, même compte et même fenêtre | +11 POINTS, compte partagé |
| Cumul depuis le début | N/A, fenêtres différentes |

| Domaine, 339 appels | Total | COMPLETED | Erreur | Part | Taux COMPLETED | Taux erreur |
|---|---|---|---|---|---|---|
| Éditions natives directes | 5 | 3 | 2 | 1.5 % | 60.0 % | 40.0 % |
| Commandes shell | 67 | 62 | 5 | 19.8 % | 92.5 % | 7.5 % |
| Web | 0 | 0 | 0 | 0.0 % | N/A | N/A |
| Autres outils | 267 | 258 | 9 | 78.8 % | 96.6 % | 3.4 % |
| Total | 339 | 323 | 16 | 100.0 % | 95.3 % | 4.7 % |

Éditions de fichiers via commandes shell non ajoutées aux éditions directes. Rôles 654 et fins : user 220, assistant 405, system 11, compaction 4, model-switched 1, idle 13 ; fins tool-calls 261, stop 138, error 1, non renseigné 5, total assistant 405. Web 0 observé.

Résultats produit : 102 historiques 44+28+30 en 3 suites, 1/10 tâches, 6 sources inchangées, aucun nouveau test produit. R01-R68, admission, origine, authenticité, autorisation, fencing, UTC, PZT non qualifiés. Archive en attente, Git non applicable sans archive, aucune inspection Git. Secrets sans valeurs exposées, clé API locale sécurisée jamais dans le rapport. Preuves et clôture postérieures au gel : checkpoint ABSOLU /home/devops/datas/pixs/output/cismp/cismp2-pixs-797dcac8c8814e27/state.json, sous réserve de leurs contrôles effectifs, sans validation anticipée ; sources : API historique OpenCode 5 sessions dédupliquées et agrégats CAB contextes 1223/1368 séparés, historique déjà clos le 26/10 à 16:25:14.973090Z.
