# Statistiques de session — add-initial-bulk-operation-record-persistence-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A version exacte non exposée | opencode-go | xhigh | 1.568 s | 85.114 | N/A durées actives non exposées |

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
| Change | add-initial-bulk-operation-record-persistence-v1 |
| Archive réelle | openspec/changes/archive/2026-10-11-add-initial-bulk-operation-record-persistence-v1 |
| Sessions | ses_ed54d3053ffe3L1vqtTRX5yymL |
| Messages | 175 |
| Parties natives | 443 |
| Appels outils | 64 |
| Coût natif observé USD | 0.281981392 |
| Couverture coût messages assistant | 119 / 119 (100.0 %) |
| Compactions natives | 0 |

Le coût natif observé est une télémétrie, pas une facture. 5 compilations, 2 tests ciblés +128 régressions =130 tests réussis ; 2 scénarios PostgreSQL réels réussis, aller-retour0003 et régression0002, schémas possédés supprimés et connexions fermées, tables existantes/publiques préservées. Serveur mesuré16.14 conforme au DEVOPS courant. Strict du change avant/après exit0 sans issue ; global strict exit1, exactement trois WARNING historiques, zéro nouvelle issue. 327 empreintes préservées ; cinq fichiers Python conformes, models.py limité à un import unique, attendu CGPT qualifié après relecture sans réécriture.

| Décision CAB terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 25 | 100.0 % |
| TOTAL | 25 | 100.0 % |

| approval_id | requestId | Décision |
| --- | --- | --- |
| approval-rec-651b6621a9b5-0025 | cismp-rec-651b6621a9b5-0025 | APPROVED |
| approval-rec-651b6621a9b5-0026 | cismp-rec-651b6621a9b5-0026 | APPROVED |
| approval-rec-651b6621a9b5-0027 | cismp-rec-651b6621a9b5-0027 | APPROVED |
| approval-rec-651b6621a9b5-0028 | cismp-rec-651b6621a9b5-0028 | APPROVED |
| approval-rec-651b6621a9b5-0029 | cismp-rec-651b6621a9b5-0029 | APPROVED |
| approval-rec-651b6621a9b5-0030 | cismp-rec-651b6621a9b5-0030 | APPROVED |
| approval-rec-651b6621a9b5-0031 | cismp-rec-651b6621a9b5-0031 | APPROVED |
| approval-rec-651b6621a9b5-0032 | cismp-rec-651b6621a9b5-0032 | APPROVED |
| approval-rec-651b6621a9b5-0033 | cismp-rec-651b6621a9b5-0033 | APPROVED |
| approval-rec-651b6621a9b5-0034 | cismp-rec-651b6621a9b5-0034 | APPROVED |
| approval-rec-651b6621a9b5-0035 | cismp-rec-651b6621a9b5-0035 | APPROVED |
| approval-rec-651b6621a9b5-0036 | cismp-rec-651b6621a9b5-0036 | APPROVED |
| approval-rec-651b6621a9b5-0037 | cismp-rec-651b6621a9b5-0037 | APPROVED |
| approval-rec-651b6621a9b5-0038 | cismp-rec-651b6621a9b5-0038 | APPROVED |
| approval-rec-651b6621a9b5-0039 | cismp-rec-651b6621a9b5-0039 | APPROVED |
| approval-rec-651b6621a9b5-0040 | cismp-rec-651b6621a9b5-0040 | APPROVED |
| approval-rec-651b6621a9b5-0041 | cismp-rec-651b6621a9b5-0041 | APPROVED |
| approval-rec-651b6621a9b5-0042 | cismp-rec-651b6621a9b5-0042 | APPROVED |
| approval-rec-651b6621a9b5-0043 | cismp-rec-651b6621a9b5-0043 | APPROVED |
| approval-rec-651b6621a9b5-0044 | cismp-rec-651b6621a9b5-0044 | APPROVED |
| approval-rec-651b6621a9b5-0045 | cismp-rec-651b6621a9b5-0045 | APPROVED |
| approval-rec-651b6621a9b5-0046 | cismp-rec-651b6621a9b5-0046 | APPROVED |
| approval-rec-651b6621a9b5-0047 | cismp-rec-651b6621a9b5-0047 | APPROVED |
| approval-rec-651b6621a9b5-0048 | cismp-rec-651b6621a9b5-0048 | APPROVED |
| approval-rec-651b6621a9b5-0049 | cismp-rec-651b6621a9b5-0049 | APPROVED |

| Mesure tokens native | Somme | Messages couverts | Couverture assistant |
| --- | --- | --- | --- |
| input | 564 | 119 | 100.0 % |
| output | 44288 | 119 | 100.0 % |
| reasoning | 0 | 119 | 100.0 % |
| total | 8782642 | 94 | 79.0 % |
| cache_read | 8078677 | 119 | 100.0 % |
| cache_write | 659113 | 119 | 100.0 % |

Tokens entrée, sortie, raisonnement, cache et total sont des champs natifs séparés avec recouvrements possibles ; ils ne sont pas additionnés ni convertis en quota.

### Sondes de performance

Même prompt déterministe, modèle/fournisseur/xhigh, sans outil ni fichier ni réseau métier, dans des sessions dédiées jetables. Début avant la première tâche métier, cadence 30 minutes, fin après archivage avant rapport. TTMT = premier delta SSE généré − envoi ; débit = tokens sortie natifs / intervalle premier–dernier delta. Moyennes arithmétiques des seules sondes valides.

| Position | Horodatage | État | TTMT s | Débit tokens/s | Durée SSE s | Tokens sortie | Coût USD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-11T13:26:57.898910+02:00 | success | 1.5790808200836182 | 80.62955818043359 | 15.630999565124512 | 1133 | 0.00244321 |
| fin | 2026-10-11T13:48:25.359074+02:00 | success | 1.557469129562378 | 89.59852583947169 | 14.135801076889038 | 1127 | 0.00244039 |

| Mesure | Valeur |
| --- | --- |
| Prévues / réussies / échouées ou non mesurables / manquées | 2 / 2 / 0 / 0 |
| Taux de réussite | 100.0 % |
| TTMT min / max s | 1.557 / 1.579 |
| Débit min / max tokens/s | 80.63 / 89.599 |
| Surcharge tokens | 2260 |
| Surcharge coût USD | 0.0048836 |
| Surcharge durée SSE s | 29.767 |

Runtime OpenCode conservé 1.18.35 ; broker natif observé 0.87.1 ; plugin/contrôleur 0.87.2. Pas de redémarrage ni purge.

## 2. Types de messages et d’outils

| Rôle message | Nombre | Part |
| --- | --- | --- |
| user | 56 | 32.0 % |
| assistant | 119 | 68.0 % |
| TOTAL | 175 | 100.0 % |

| Partie native | Nombre | Part |
| --- | --- | --- |
| text | 97 | 21.9 % |
| step-start | 94 | 21.2 % |
| reasoning | 94 | 21.2 % |
| tool | 64 | 14.4 % |
| step-finish | 94 | 21.2 % |
| TOTAL | 443 | 100.0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 64 | 53.8 % |
| stop | 30 | 25.2 % |
| absent | 25 | 21.0 % |
| TOTAL | 119 | 100.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 15 | 23.4 % | 15 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 3 | 4.7 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 26 | 40.6 % | 25 | 96.2 % | 0 | 0.0 % | 1 | 3.8 % | 0 | 0.0 % |
| edit | 1 | 1.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 10 | 15.6 % | 2 | 20.0 % | 0 | 0.0 % | 8 | 80.0 % | 0 | 0.0 % |
| write | 9 | 14.1 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 64 | 100.0 % | 55 | 85.9 % | 0 | 0.0 % | 9 | 14.1 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-persistence-v1/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-persistence-v1/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-persistence-v1/specs/bulk-operations/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-record-persistence-v1/tasks.md | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_operation_record.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0003_bulk_operation_record.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_record_postgres_integration.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_record.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 10 | 100.0 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Chemins absolus intégraux ; nombres = tentatives natives d’écriture/édition, pas un diff Git. Les quatre artefacts du change ont été déplacés par archivage unique vers openspec/changes/archive/2026-10-11-add-initial-bulk-operation-record-persistence-v1. Le présent rapport est publié ensuite sous un mandat distinct, hors périmètre temporel de collecte. Octets approuvés, UTF-8/LF et références préservées contrôlés.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 3 | 20.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PostgreSQL réel | 2 | 13.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| compilation Python | 5 | 33.3 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| prévol CAB | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 3 | 20.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 15 | 100.0 % | 15 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_operation_record.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/migrations/0003_bulk_opera… | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/models.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_operation_recor… | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_operation_record.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-initial-bulk-o… | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-initial-bulk-… | 2 | 13.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_bulk_ope… | 2 | 13.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_semver_c… | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/test_bulk_opera… | 2 | 13.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 15 | 100.0 % | 15 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Libellés limités à 100 caractères ; commandes intégrales et workdir vérifié conservés au checkpoint et dans les preuves natives.

### Commandes proposées et refusées (non exécutées)

Aucune commande CAB refusée.

## 5. Accès web

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web ni URL effectivement visitée dans les preuves natives de ce change. Les communications locales CAB/OpenCode et les connexions PG de tests ne sont pas des consultations web.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T11:22:04.211000+00:00 |
| Fin — après archivage | 2026-10-11T11:48:41.561836+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 26 min 37 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant travaux | 2026-10-11T13:26:57.898890+02:00 | N/A — get_usage_limits non exposé | N/A |
| Après archivage | 2026-10-11T13:48:41.584905+02:00 | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | N/A |

Fenêtre attendue codex 10080 minutes ; compte/fenêtre/réinitialisation non observables. Quotas partagés par compte : une variation peut inclure des tâches simultanées ; aucune attribution exclusive ni reconstruction en tokens/euros. Aucun quota fournisseur Qwen ne remplace ce relevé Codex.

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB | 29 | 45.3 % | 28 | 96.6 % | 0 | 0.0 % | 1 | 3.4 % | 0 | 0.0 % |
| commande | 15 | 23.4 % | 15 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| fichier | 20 | 31.2 % | 12 | 60.0 % | 0 | 0.0 % | 8 | 40.0 % | 0 | 0.0 % |
| TOTAL | 64 | 100.0 % | 55 | 85.9 % | 0 | 0.0 % | 9 | 14.1 % | 0 | 0.0 % |

| Contrôle croisé | Nombre | Part du total global |
| --- | --- | --- |
| Somme types outils | 64 | 100.0 % |
| Somme domaines | 64 | 100.0 % |
| Somme résultats | 64 | 100.0 % |
| Total outils | 64 | 100.0 % |

5 compilations, 2 tests ciblés +128 régressions =130 tests réussis ; 2 scénarios PostgreSQL réels réussis, aller-retour0003 et régression0002, schémas possédés supprimés et connexions fermées, tables existantes/publiques préservées. Serveur mesuré16.14 conforme au DEVOPS courant. Strict du change avant/après exit0 sans issue ; global strict exit1, exactement trois WARNING historiques, zéro nouvelle issue. 327 empreintes préservées ; cinq fichiers Python conformes, models.py limité à un import unique, attendu CGPT qualifié après relecture sans réécriture. Archivage unique prouvé. Git non inspecté, aucun commit/push. Accès externes limités aux communications LLM/pilotage autorisées et aux tests PG prévus le cas échéant ; aucun secret lu par l’agent, transmis au modèle ou publié. Ce jalon ne constitue pas la fin globale du RUN.
