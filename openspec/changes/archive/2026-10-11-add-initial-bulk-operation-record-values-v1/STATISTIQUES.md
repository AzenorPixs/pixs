# Statistiques de session — add-initial-bulk-operation-record-values-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A version exacte non exposée | opencode-go | xhigh | 1.709 s | 92.945 | N/A durées actives non exposées |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex GPT-6 | N/A version exacte non exposée | OpenAI | N/A non exposé | N/A aucune sonde | N/A aucune sonde | N/A durées actives non exposées |

Temps de service cumulé et chevauchements : N/A, télémétrie active absente pour ces agents. Les durées de message, de permission, d’outil et la durée calendaire ne sont pas utilisées comme durée de génération.

## 1. Statistiques générales et décisions

Historique natif complet des sessions listées, dédupliqué par identifiants message/partie. Prévols et reprises inclus ; sondes dédiées et publication du présent rapport exclues. Un outil completed est un appel abouti autorisé dans son contexte, sans preuve d’approbation manuelle pour les lectures automatiques. Un message interrompu après un outil completed ne transforme pas cet outil en erreur. Un refus CAB retourné par MCP completed reste une décision séparée ; un délai MCP est une erreur technique.

| Mesure | Valeur |
| --- | --- |
| RUN | cismp-pixs-758862ec875d4708 |
| Change | add-initial-bulk-operation-record-values-v1 |
| Archive réelle | openspec/changes/archive/2026-10-11-add-initial-bulk-operation-record-values-v1 |
| Sessions | ses_ed575284bffe4Apmqq2103Zgnd |
| Messages | 141 |
| Parties natives | 380 |
| Appels outils | 54 |
| Coût natif observé USD | 0.270754976 |
| Couverture coût messages assistant | 97 / 97 (100.0 %) |
| Compactions natives | 0 |

Le coût natif observé est une télémétrie, pas une facture. 3 compilations, 15 tests ciblés et 111 régressions réussis ; strict avant/après code exit 0 sans issue ; 319 empreintes préservées. Global strict qualifié séparément par trois WARNING historiques, jamais présenté comme réussi.

| Décision CAB terminale distincte | Nombre | Part |
| --- | --- | --- |
| REJECTED | 2 | 10.5 % |
| APPROVED | 17 | 89.5 % |
| TOTAL | 19 | 100.0 % |

| approval_id | requestId | Décision |
| --- | --- | --- |
| approval-rec-651b6621a9b5-0004 | cismp-rec-651b6621a9b5-0004 | REJECTED |
| approval-rec-651b6621a9b5-0005 | cismp-rec-651b6621a9b5-0005 | APPROVED |
| approval-rec-651b6621a9b5-0006 | cismp-rec-651b6621a9b5-0006 | APPROVED |
| approval-rec-651b6621a9b5-0007 | cismp-rec-651b6621a9b5-0007 | APPROVED |
| approval-rec-651b6621a9b5-0008 | cismp-rec-651b6621a9b5-0008 | APPROVED |
| approval-rec-651b6621a9b5-0009 | cismp-rec-651b6621a9b5-0009 | APPROVED |
| approval-rec-651b6621a9b5-0010 | cismp-rec-651b6621a9b5-0010 | APPROVED |
| approval-rec-651b6621a9b5-0011 | cismp-rec-651b6621a9b5-0011 | APPROVED |
| approval-rec-651b6621a9b5-0012 | cismp-rec-651b6621a9b5-0012 | APPROVED |
| approval-rec-651b6621a9b5-0013 | cismp-rec-651b6621a9b5-0013 | APPROVED |
| approval-rec-651b6621a9b5-0014 | cismp-rec-651b6621a9b5-0014 | APPROVED |
| approval-rec-651b6621a9b5-0015 | cismp-rec-651b6621a9b5-0015 | APPROVED |
| approval-rec-651b6621a9b5-0016 | cismp-rec-651b6621a9b5-0016 | APPROVED |
| approval-rec-651b6621a9b5-0017 | cismp-rec-651b6621a9b5-0017 | APPROVED |
| approval-rec-651b6621a9b5-0018 | cismp-rec-651b6621a9b5-0018 | REJECTED |
| approval-rec-651b6621a9b5-0019 | cismp-rec-651b6621a9b5-0019 | APPROVED |
| approval-rec-651b6621a9b5-0020 | cismp-rec-651b6621a9b5-0020 | APPROVED |
| approval-rec-651b6621a9b5-0021 | cismp-rec-651b6621a9b5-0021 | APPROVED |
| approval-rec-651b6621a9b5-0022 | cismp-rec-651b6621a9b5-0022 | APPROVED |

| Mesure tokens native | Somme | Messages couverts | Couverture assistant |
| --- | --- | --- | --- |
| input | 480 | 97 | 100.0 % |
| output | 42972 | 97 | 100.0 % |
| reasoning | 0 | 97 | 100.0 % |
| total | 6481252 | 80 | 82.5 % |
| cache_read | 5636271 | 97 | 100.0 % |
| cache_write | 801529 | 97 | 100.0 % |

Tokens entrée, sortie, raisonnement, cache et total sont des champs natifs séparés avec recouvrements possibles ; ils ne sont pas additionnés ni convertis en quota.

### Sondes de performance

Même prompt déterministe, modèle/fournisseur/xhigh, sans outil ni fichier ni réseau métier, dans des sessions dédiées jetables. Début avant la première tâche métier, cadence 30 minutes, fin après archivage avant rapport. TTMT = premier delta SSE généré − envoi ; débit = tokens sortie natifs / intervalle premier–dernier delta. Moyennes arithmétiques des seules sondes valides.

| Position | État | TTMT s | Débit tokens/s | Durée SSE s | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- | --- | --- |
| début | success | 1.832671880722046 | 87.60012239010135 | 14.949091911315918 | 1149 | 0.00245073 |
| fin | success | 1.5852165222167969 | 98.29078523813668 | 13.071542501449585 | 1129 | 0.00244133 |

| Mesure | Valeur |
| --- | --- |
| Prévues / réussies / échouées ou non mesurables / manquées | 2 / 2 / 0 / 0 |
| Taux de réussite | 100.0 % |
| TTMT min / max s | 1.585 / 1.833 |
| Débit min / max tokens/s | 87.6 / 98.291 |
| Surcharge tokens | 2278 |
| Surcharge coût USD | 0.00489206 |
| Surcharge durée SSE s | 28.021 |

Runtime OpenCode conservé 1.18.35 ; broker natif observé 0.87.1 ; plugin/contrôleur 0.87.2. Pas de redémarrage ni purge.

## 2. Types de messages et d’outils

| Rôle message | Nombre | Part |
| --- | --- | --- |
| user | 44 | 31.2 % |
| assistant | 97 | 68.8 % |
| TOTAL | 141 | 100.0 % |

| Partie native | Nombre | Part |
| --- | --- | --- |
| text | 86 | 22.6 % |
| step-start | 80 | 21.1 % |
| reasoning | 80 | 21.1 % |
| tool | 54 | 14.2 % |
| step-finish | 80 | 21.1 % |
| TOTAL | 380 | 100.0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 54 | 55.7 % |
| stop | 26 | 26.8 % |
| absent | 17 | 17.5 % |
| TOTAL | 97 | 100.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 9 | 16.7 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 4 | 7.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 3 | 5.6 % | 1 | 33.3 % | 0 | 0.0 % | 2 | 66.7 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 3 | 5.6 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 19 | 35.2 % | 17 | 89.5 % | 0 | 0.0 % | 2 | 10.5 % | 0 | 0.0 % |
| read | 8 | 14.8 % | 1 | 12.5 % | 0 | 0.0 % | 7 | 87.5 % | 0 | 0.0 % |
| write | 8 | 14.8 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 54 | 100.0 % | 43 | 79.6 % | 0 | 0.0 % | 11 | 20.4 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-values-v1/design.md | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-values-v1/proposal.md | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-values-v1/specs/bulk-operations/spec.md | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-values-v1/tasks.md | 2 | 25.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_record_values.py | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_record_values_integration.py | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_record_values.py | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100.0 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Chemins absolus intégraux ; nombres = tentatives natives d’écriture/édition, pas un diff Git. Les quatre artefacts du change ont été déplacés par archivage unique vers openspec/changes/archive/2026-10-11-add-initial-bulk-operation-record-values-v1. Le présent rapport est publié ensuite sous un mandat distinct, hors périmètre temporel de collecte. Octets approuvés, UTF-8/LF et références préservées contrôlés.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| compilation Python | 3 | 33.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| prévol CAB | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_operation_record_value… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_operation_recor… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_operation_record_value… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-initial-bulk-o… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-initial-bulk-… | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_bulk_ope… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_semver_c… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Libellés limités à 100 caractères ; commandes intégrales et workdir vérifié conservés au checkpoint et dans les preuves natives.

### Commandes proposées et refusées (non exécutées)

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 1 | 50.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_semver_c… | 1 | 50.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 2 | 100.0 % | 0 | 0.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

## 5. Accès web

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web ni URL effectivement visitée dans les preuves natives de ce change. Les communications locales CAB/OpenCode et les connexions PG de tests ne sont pas des consultations web.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T10:38:24.788000+00:00 |
| Fin — après archivage | 2026-10-11T11:17:15.796181+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 38 min 51 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant travaux | 2026-10-11T12:57:41.076775+02:00 | N/A — get_usage_limits non exposé | N/A |
| Après archivage | 2026-10-11T13:17:15.821030+02:00 | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | N/A |

Fenêtre attendue codex 10080 minutes ; compte/fenêtre/réinitialisation non observables. Quotas partagés par compte : une variation peut inclure des tâches simultanées ; aucune attribution exclusive ni reconstruction en tokens/euros. Aucun quota fournisseur Qwen ne remplace ce relevé Codex.

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB | 29 | 53.7 % | 25 | 86.2 % | 0 | 0.0 % | 4 | 13.8 % | 0 | 0.0 % |
| commande | 9 | 16.7 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| fichier | 16 | 29.6 % | 9 | 56.2 % | 0 | 0.0 % | 7 | 43.8 % | 0 | 0.0 % |
| TOTAL | 54 | 100.0 % | 43 | 79.6 % | 0 | 0.0 % | 11 | 20.4 % | 0 | 0.0 % |

| Contrôle croisé | Nombre | Part du total global |
| --- | --- | --- |
| Somme types outils | 54 | 100.0 % |
| Somme domaines | 54 | 100.0 % |
| Somme résultats | 54 | 100.0 % |
| Total outils | 54 | 100.0 % |

3 compilations, 15 tests ciblés et 111 régressions réussis ; strict avant/après code exit 0 sans issue ; 319 empreintes préservées. Global strict qualifié séparément par trois WARNING historiques, jamais présenté comme réussi. Archivage unique prouvé. Git non inspecté, aucun commit/push. Accès externes limités aux communications LLM/pilotage autorisées et aux tests PG prévus le cas échéant ; aucun secret lu par l’agent, transmis au modèle ou publié. Ce jalon ne constitue pas la fin globale du RUN.
