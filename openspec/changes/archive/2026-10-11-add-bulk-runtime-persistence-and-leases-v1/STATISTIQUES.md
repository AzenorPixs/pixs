# Statistiques de session — add-bulk-runtime-persistence-and-leases-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A version exacte non exposée | opencode-go | xhigh | 1.866 s | 89.543 | N/A durées actives non exposées |
| qwen3.8-flash (compactage natif) | N/A version exacte non exposée | opencode-go | N/A variant non exposé par summarize | N/A aucune sonde de compactage | N/A aucune sonde de compactage | N/A durées actives non exposées |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex GPT-6 | N/A version exacte non exposée | OpenAI | N/A non exposé | N/A aucune sonde | N/A aucune sonde | N/A durées actives non exposées |

Temps de service cumulé et chevauchements : N/A, télémétrie active absente pour ces agents. Les outils internes et le raisonnement de l’orchestrateur Codex ne sont pas exposés par cette source OpenCode. Les durées de message, de permission, d’outil et la durée calendaire ne sont pas utilisées comme durée de génération.

## 1. Statistiques générales et décisions

Historique natif OpenCode complet des sessions listées, dédupliqué par identifiants message/partie. Prévols et reprises inclus ; sondes dédiées et publication du présent rapport exclues. Un outil completed est un appel abouti autorisé dans son contexte, sans preuve d’approbation manuelle pour les lectures automatiques. Un message interrompu après un outil completed ne transforme pas cet outil en erreur. Un refus CAB retourné par MCP completed reste une décision séparée ; un délai MCP est une erreur technique.

| Mesure | Valeur |
| --- | --- |
| RUN | cismp-pixs-758862ec875d4708 |
| Change | add-bulk-runtime-persistence-and-leases-v1 |
| Archive réelle | openspec/changes/archive/2026-10-11-add-bulk-runtime-persistence-and-leases-v1 |
| Sessions | ses_ed3c2b2b2ffec9UqjCa5Q5x1n4, ses_ed378b8b4ffe3wIsaDVenJFlu8 |
| Messages | 318 |
| Parties natives | 786 |
| Appels outils | 161 |
| Coût natif observé (champ cost) | 1.623642644 |
| Couverture coût messages assistant | 231 / 231 (100.0 %) |
| Tentatives de compactage natives | 2 |
| Compactages natifs réussis | 1 |
| Compactages natifs en erreur | 1 |

Le coût natif observé est le champ cost de la télémétrie, pas une facture. Devise non exposée par ces messages, aucune conversion déduite. Les champs présents à zéro dans un message interrompu ne prouvent pas une consommation fournisseur nulle ; seules les valeurs natives disponibles sont additionnées. Six fichiers Python compilés, repository recompilé après revue finale, deux nouveaux tests offline en processus frais et202 régressions en 29 modules réussis. Un scénario PostgreSQL 16.14 réel isolé :18 indicateurs métier/techniques vrais, cleanup et connexions fermés, tables existantes et publiques préservées. Strict du change zéro issue ; strict global exit1 qualifié par exactement trois WARNING historiques, zéro nouvelle issue. Couverture persistance SQL/CAS/checkpoints/transitions/baux interne seulement, sans admission/worker/idempotence/outbox ni provider propriétaire de production. HTTP 400 avant outil dans une ancienne session et compaction en échec réconciliés par récupération CAB du même change sans redémarrer OpenCode, sources conservées; proposition de test divergente rejetée avant exécution puis reprise au premier test non prouvé.

| Décision CAB terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 62 | 98.4 % |
| REJECTED | 1 | 1.6 % |
| TOTAL | 63 | 100.0 % |

| approval_id | requestId | Décision |
| --- | --- | --- |
| approval-bex-d4c5208f6df3-0105 | cismp-bex-d4c5208f6df3-0105 | APPROVED |
| approval-bex-d4c5208f6df3-0106 | cismp-bex-d4c5208f6df3-0106 | APPROVED |
| approval-bex-d4c5208f6df3-0107 | cismp-bex-d4c5208f6df3-0107 | APPROVED |
| approval-bex-d4c5208f6df3-0108 | cismp-bex-d4c5208f6df3-0108 | APPROVED |
| approval-bex-d4c5208f6df3-0109 | cismp-bex-d4c5208f6df3-0109 | APPROVED |
| approval-bex-d4c5208f6df3-0110 | cismp-bex-d4c5208f6df3-0110 | APPROVED |
| approval-bex-d4c5208f6df3-0111 | cismp-bex-d4c5208f6df3-0111 | APPROVED |
| approval-bex-d4c5208f6df3-0112 | cismp-bex-d4c5208f6df3-0112 | APPROVED |
| approval-bex-d4c5208f6df3-0113 | cismp-bex-d4c5208f6df3-0113 | APPROVED |
| approval-bex-d4c5208f6df3-0114 | cismp-bex-d4c5208f6df3-0114 | APPROVED |
| approval-bex-d4c5208f6df3-0115 | cismp-bex-d4c5208f6df3-0115 | APPROVED |
| approval-bex-d4c5208f6df3-0116 | cismp-bex-d4c5208f6df3-0116 | APPROVED |
| approval-bex-d4c5208f6df3-0117 | cismp-bex-d4c5208f6df3-0117 | APPROVED |
| approval-bex-d4c5208f6df3-0118 | cismp-bex-d4c5208f6df3-0118 | APPROVED |
| approval-bex-d4c5208f6df3-0119 | cismp-bex-d4c5208f6df3-0119 | APPROVED |
| approval-bex-d4c5208f6df3-0120 | cismp-bex-d4c5208f6df3-0120 | APPROVED |
| approval-bex-d4c5208f6df3-0121 | cismp-bex-d4c5208f6df3-0121 | APPROVED |
| approval-bex-d4c5208f6df3-0122 | cismp-bex-d4c5208f6df3-0122 | APPROVED |
| approval-bex-d4c5208f6df3-0123 | cismp-bex-d4c5208f6df3-0123 | APPROVED |
| approval-bex-d4c5208f6df3-0124 | cismp-bex-d4c5208f6df3-0124 | APPROVED |
| approval-bex-d4c5208f6df3-0125 | cismp-bex-d4c5208f6df3-0125 | APPROVED |
| approval-bex-d4c5208f6df3-0126 | cismp-bex-d4c5208f6df3-0126 | APPROVED |
| approval-bex-d4c5208f6df3-0127 | cismp-bex-d4c5208f6df3-0127 | APPROVED |
| approval-bex-d4c5208f6df3-0128 | cismp-bex-d4c5208f6df3-0128 | APPROVED |
| approval-bex-d4c5208f6df3-0129 | cismp-bex-d4c5208f6df3-0129 | APPROVED |
| approval-bex-d4c5208f6df3-0130 | cismp-bex-d4c5208f6df3-0130 | APPROVED |
| approval-bex-d4c5208f6df3-0131 | cismp-bex-d4c5208f6df3-0131 | APPROVED |
| approval-bex-d4c5208f6df3-0133 | cismp-bex-d4c5208f6df3-0133 | APPROVED |
| approval-bex-d4c5208f6df3-0134 | cismp-bex-d4c5208f6df3-0134 | APPROVED |
| approval-bex-d4c5208f6df3-0135 | cismp-bex-d4c5208f6df3-0135 | APPROVED |
| approval-bex-d4c5208f6df3-0136 | cismp-bex-d4c5208f6df3-0136 | APPROVED |
| approval-bex-d4c5208f6df3-0137 | cismp-bex-d4c5208f6df3-0137 | APPROVED |
| approval-bex-d4c5208f6df3-0138 | cismp-bex-d4c5208f6df3-0138 | APPROVED |
| approval-bex-d4c5208f6df3-0139 | cismp-bex-d4c5208f6df3-0139 | APPROVED |
| approval-bex-d4c5208f6df3-0140 | cismp-bex-d4c5208f6df3-0140 | APPROVED |
| approval-bex-d4c5208f6df3-0141 | cismp-bex-d4c5208f6df3-0141 | APPROVED |
| approval-bex-d4c5208f6df3-0142 | cismp-bex-d4c5208f6df3-0142 | REJECTED |
| approval-bex-d4c5208f6df3-0143 | cismp-bex-d4c5208f6df3-0143 | APPROVED |
| approval-bex-d4c5208f6df3-0144 | cismp-bex-d4c5208f6df3-0144 | APPROVED |
| approval-bex-d4c5208f6df3-0145 | cismp-bex-d4c5208f6df3-0145 | APPROVED |
| approval-bex-d4c5208f6df3-0146 | cismp-bex-d4c5208f6df3-0146 | APPROVED |
| approval-bex-d4c5208f6df3-0147 | cismp-bex-d4c5208f6df3-0147 | APPROVED |
| approval-bex-d4c5208f6df3-0148 | cismp-bex-d4c5208f6df3-0148 | APPROVED |
| approval-bex-d4c5208f6df3-0149 | cismp-bex-d4c5208f6df3-0149 | APPROVED |
| approval-bex-d4c5208f6df3-0150 | cismp-bex-d4c5208f6df3-0150 | APPROVED |
| approval-bex-d4c5208f6df3-0151 | cismp-bex-d4c5208f6df3-0151 | APPROVED |
| approval-bex-d4c5208f6df3-0152 | cismp-bex-d4c5208f6df3-0152 | APPROVED |
| approval-bex-d4c5208f6df3-0153 | cismp-bex-d4c5208f6df3-0153 | APPROVED |
| approval-bex-d4c5208f6df3-0154 | cismp-bex-d4c5208f6df3-0154 | APPROVED |
| approval-bex-d4c5208f6df3-0155 | cismp-bex-d4c5208f6df3-0155 | APPROVED |
| approval-bex-d4c5208f6df3-0156 | cismp-bex-d4c5208f6df3-0156 | APPROVED |
| approval-bex-d4c5208f6df3-0157 | cismp-bex-d4c5208f6df3-0157 | APPROVED |
| approval-bex-d4c5208f6df3-0158 | cismp-bex-d4c5208f6df3-0158 | APPROVED |
| approval-bex-d4c5208f6df3-0159 | cismp-bex-d4c5208f6df3-0159 | APPROVED |
| approval-bex-d4c5208f6df3-0160 | cismp-bex-d4c5208f6df3-0160 | APPROVED |
| approval-bex-d4c5208f6df3-0161 | cismp-bex-d4c5208f6df3-0161 | APPROVED |
| approval-bex-d4c5208f6df3-0162 | cismp-bex-d4c5208f6df3-0162 | APPROVED |
| approval-bex-d4c5208f6df3-0163 | cismp-bex-d4c5208f6df3-0163 | APPROVED |
| approval-bex-d4c5208f6df3-0164 | cismp-bex-d4c5208f6df3-0164 | APPROVED |
| approval-bex-d4c5208f6df3-0165 | cismp-bex-d4c5208f6df3-0165 | APPROVED |
| approval-bex-d4c5208f6df3-0166 | cismp-bex-d4c5208f6df3-0166 | APPROVED |
| approval-bex-d4c5208f6df3-0167 | cismp-bex-d4c5208f6df3-0167 | APPROVED |
| approval-bex-d4c5208f6df3-0168 | cismp-bex-d4c5208f6df3-0168 | APPROVED |

| Mesure tokens native | Somme | Messages couverts | Couverture assistant |
| --- | --- | --- | --- |
| input | 990 | 231 | 100.0 % |
| output | 200208 | 231 | 100.0 % |
| reasoning | 0 | 231 | 100.0 % |
| total | 14924796 | 165 | 71.4 % |
| cache_read | 7691974 | 231 | 100.0 % |
| cache_write | 7031624 | 231 | 100.0 % |

Tokens entrée, sortie, raisonnement, cache et total sont des champs natifs séparés avec recouvrements possibles ; ils ne sont pas additionnés ni convertis en quota.

### Sondes de performance

Même prompt déterministe, modèle/fournisseur/xhigh, sans outil ni fichier ni réseau métier, dans des sessions dédiées jetables. Début avant la première tâche métier, cadence 30 minutes, fin après archivage avant rapport. TTMT = premier delta SSE du champ text observé − envoi ; débit = tokens sortie natifs / intervalle premier–dernier delta. Moyennes arithmétiques des seules sondes valides.

| Position | Horodatage | État | TTMT s | Débit tokens/s | Durée SSE s | Tokens sortie | Coût natif |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-11T20:34:45.516300+02:00 | success | 1.4121067523956299 | 97.42658362120754 | 16.059033155441284 | 1427 | 0.00258259 |
| +30 min | 2026-10-11T21:04:45.965853+02:00 | success | 1.6857616901397705 | 73.5904024819783 | 28.197371006011963 | 1951 | 0.00282887 |
| +60 min | 2026-10-11T21:34:46.404517+02:00 | success | 2.680565118789673 | 88.70701556507208 | 18.81232190132141 | 1431 | 0.00258447 |
| +90 min | 2026-10-11T22:04:46.967134+02:00 | success | 1.659916877746582 | 102.36241804597557 | 15.68850302696228 | 1436 | 0.00258682 |
| fin | 2026-10-11T22:17:46.636311+02:00 | success | 1.889718770980835 | 85.6270774776241 | 18.473258018493652 | 1420 | 0.0025793 |

| Mesure | Valeur |
| --- | --- |
| Prévues / réussies / échouées ou non mesurables / manquées | 5 / 5 / 0 / 0 |
| Taux de réussite | 100.0 % |
| TTMT min / max s | 1.412 / 2.681 |
| Débit min / max tokens/s | 73.59 / 102.362 |
| Surcharge tokens | 7665 |
| Surcharge coût natif | 0.01316205 |
| Surcharge durée SSE s | 97.23 |

Runtime OpenCode conservé 1.18.35 ; broker natif et plugin/contrôleur observés 0.87.2. 0 redémarrage(s) CAB avec purge technique autorisée dans cet intervalle après refus sans effet ; sources et historiques natifs préservés. OpenCode jamais fermé ou redémarré.

## 2. Types de messages et d’outils

| Rôle message | Nombre | Part |
| --- | --- | --- |
| user | 87 | 27.4 % |
| assistant | 231 | 72.6 % |
| TOTAL | 318 | 100.0 % |

| Partie native | Nombre | Part |
| --- | --- | --- |
| text | 126 | 16.0 % |
| step-start | 166 | 21.1 % |
| reasoning | 166 | 21.1 % |
| tool | 161 | 20.5 % |
| step-finish | 165 | 21.0 % |
| compaction | 2 | 0.3 % |
| TOTAL | 786 | 100.0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 145 | 62.8 % |
| stop | 20 | 8.7 % |
| absent | 66 | 28.6 % |
| TOTAL | 231 | 100.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 47 | 29.2 % | 47 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 9 | 5.6 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 1 | 0.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 1 | 0.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 63 | 39.1 % | 61 | 96.8 % | 0 | 0.0 % | 2 | 3.2 % | 0 | 0.0 % |
| edit | 1 | 0.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 25 | 15.5 % | 22 | 88.0 % | 0 | 0.0 % | 3 | 12.0 % | 0 | 0.0 % |
| write | 14 | 8.7 % | 14 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 161 | 100.0 % | 156 | 96.9 % | 0 | 0.0 % | 5 | 3.1 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-persistence-and-leases-v1/design.md | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-persistence-and-leases-v1/proposal.md | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-persistence-and-leases-v1/specs/bulk-operations/spec.md | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-persistence-and-leases-v1/specs/jobs/spec.md | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-persistence-and-leases-v1/tasks.md | 2 | 13.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_runtime_records.py | 2 | 13.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_runtime_repository.py | 3 | 20.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0004_bulk_runtime_persistence.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_runtime_persistence_postgres_integration.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_runtime_records.py | 1 | 6.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 15 | 100.0 % | 15 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Chemins absolus intégraux ; nombres = tentatives natives d’écriture/édition, pas un diff Git. Les cinq artefacts du change ont été déplacés par archivage unique vers openspec/changes/archive/2026-10-11-add-bulk-runtime-persistence-and-leases-v1. Le présent rapport est publié ensuite sous un mandat distinct, hors périmètre temporel de collecte. Octets approuvés, UTF-8/LF et références préservées contrôlés.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 4 | 8.5 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PostgreSQL réel | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| compilation Python | 7 | 14.9 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| prévol CAB | 3 | 6.4 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 31 | 66.0 % | 31 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 47 | 100.0 % | 47 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_runtime_records.py | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_runtime_repository.py | 2 | 4.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/migrations/0004_bulk_runti… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/models.py | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_runtime_persist… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_runtime_records.py | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 3 | 6.4 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-p… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 2 | 4.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 4.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 12 | 25.5 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_job_… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_kern… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_publ… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_execut… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_job_li… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 7 | 14.9 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_runtim… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_scope_… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_tenant… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_job_record | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_job_state | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_notificatio… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_semver_cons… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/test_bulk_runti… | 1 | 2.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 47 | 100.0 % | 47 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Libellés limités à 100 caractères ; commandes intégrales et workdir vérifié conservés au checkpoint et dans les preuves natives.

### Commandes proposées et refusées (non exécutées)

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 100.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 1 | 100.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

## 5. Accès web

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web ni URL effectivement visitée dans les preuves natives de ce change. Les communications locales CAB/OpenCode et les connexions PG de tests ne sont pas des consultations web.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T18:32:57.596000+00:00 |
| Fin — après archivage | 2026-10-11T20:18:07.797991+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 45 min 10 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant travaux | 2026-10-11T20:34:45.516290+02:00 | N/A — get_usage_limits non exposé | N/A |
| Après archivage | 2026-10-11T22:18:07.835005+02:00 | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | N/A |

Fenêtre attendue codex 10080 minutes ; compte/fenêtre/réinitialisation non observables. Quotas partagés par compte : une variation peut inclure des tâches simultanées ; aucune attribution exclusive ni reconstruction en tokens/euros. Aucun quota fournisseur Qwen ne remplace ce relevé Codex.

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB | 74 | 46.0 % | 72 | 97.3 % | 0 | 0.0 % | 2 | 2.7 % | 0 | 0.0 % |
| commande | 47 | 29.2 % | 47 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| fichier | 40 | 24.8 % | 37 | 92.5 % | 0 | 0.0 % | 3 | 7.5 % | 0 | 0.0 % |
| TOTAL | 161 | 100.0 % | 156 | 96.9 % | 0 | 0.0 % | 5 | 3.1 % | 0 | 0.0 % |

| Contrôle croisé | Nombre | Part du total global |
| --- | --- | --- |
| Somme types outils | 161 | 100.0 % |
| Somme domaines | 161 | 100.0 % |
| Somme résultats | 161 | 100.0 % |
| Total outils | 161 | 100.0 % |

Six fichiers Python compilés, repository recompilé après revue finale, deux nouveaux tests offline en processus frais et202 régressions en 29 modules réussis. Un scénario PostgreSQL 16.14 réel isolé :18 indicateurs métier/techniques vrais, cleanup et connexions fermés, tables existantes et publiques préservées. Strict du change zéro issue ; strict global exit1 qualifié par exactement trois WARNING historiques, zéro nouvelle issue. Couverture persistance SQL/CAS/checkpoints/transitions/baux interne seulement, sans admission/worker/idempotence/outbox ni provider propriétaire de production. HTTP 400 avant outil dans une ancienne session et compaction en échec réconciliés par récupération CAB du même change sans redémarrer OpenCode, sources conservées; proposition de test divergente rejetée avant exécution puis reprise au premier test non prouvé. Archivage unique prouvé. Git non inspecté, aucun commit/push. Accès externes limités aux communications LLM/pilotage autorisées et aux tests PG prévus le cas échéant ; secrets utilisés seulement dans les processus sécurisés autorisés de quotas et de tests PostgreSQL, aucune valeur transmise au modèle ou publiée. Ce jalon ne constitue pas la fin globale du RUN.
