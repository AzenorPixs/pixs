# Statistiques de session — add-bulk-runtime-value-validation-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A version exacte non exposée | opencode-go | xhigh | 1.704 s | 99.851 | N/A durées actives non exposées |
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
| Change | add-bulk-runtime-value-validation-v1 |
| Archive réelle | openspec/changes/archive/2026-10-11-add-bulk-runtime-value-validation-v1 |
| Sessions | ses_ed45f5d41ffeYVkLfcnkbC8TZg, ses_ed4536be7ffeD6F132plbnGy4X, ses_ed3f477a8ffeKcjicU6l1Lep1l, ses_ed3cef49dffeliWi8qx7sCOKra |
| Messages | 476 |
| Parties natives | 1222 |
| Appels outils | 232 |
| Coût natif observé (champ cost) | 1.626655598 |
| Couverture coût messages assistant | 339 / 339 (100.0 %) |
| Compactions natives | 1 |

Le coût natif observé est le champ cost de la télémétrie, pas une facture. Devise non exposée par ces messages, aucune conversion déduite. Les champs présents à zéro dans un message interrompu ne prouvent pas une consommation fournisseur nulle ; seules les valeurs natives disponibles sont additionnées. Trois compilations et202 tests unittest réussis (72 ciblés dont processus frais sous gardes,130 régressions),2 scénarios PG réels isolés avec cleanup/connexions fermées. Strict du change sans issue ; global exit1 qualifié par exactement3 WARNING historiques et zéro nouvelle issue. Couverture mémoire B02/B09 uniquement ; runtime complet reste à poursuivre.

| Décision CAB terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 70 | 88.6 % |
| REJECTED | 9 | 11.4 % |
| TOTAL | 79 | 100.0 % |

| approval_id | requestId | Décision |
| --- | --- | --- |
| approval-bex-d4c5208f6df3-0024 | cismp-bex-d4c5208f6df3-0024 | APPROVED |
| approval-bex-d4c5208f6df3-0025 | cismp-bex-d4c5208f6df3-0025 | REJECTED |
| approval-bex-d4c5208f6df3-0026 | cismp-bex-d4c5208f6df3-0026 | APPROVED |
| approval-bex-d4c5208f6df3-0027 | cismp-bex-d4c5208f6df3-0027 | APPROVED |
| approval-bex-d4c5208f6df3-0028 | cismp-bex-d4c5208f6df3-0028 | APPROVED |
| approval-bex-d4c5208f6df3-0029 | cismp-bex-d4c5208f6df3-0029 | APPROVED |
| approval-bex-d4c5208f6df3-0030 | cismp-bex-d4c5208f6df3-0030 | APPROVED |
| approval-bex-d4c5208f6df3-0031 | cismp-bex-d4c5208f6df3-0031 | APPROVED |
| approval-bex-d4c5208f6df3-0032 | cismp-bex-d4c5208f6df3-0032 | APPROVED |
| approval-bex-d4c5208f6df3-0033 | cismp-bex-d4c5208f6df3-0033 | APPROVED |
| approval-bex-d4c5208f6df3-0034 | cismp-bex-d4c5208f6df3-0034 | APPROVED |
| approval-bex-d4c5208f6df3-0035 | cismp-bex-d4c5208f6df3-0035 | APPROVED |
| approval-bex-d4c5208f6df3-0036 | cismp-bex-d4c5208f6df3-0036 | REJECTED |
| approval-bex-d4c5208f6df3-0037 | cismp-bex-d4c5208f6df3-0037 | APPROVED |
| approval-bex-d4c5208f6df3-0038 | cismp-bex-d4c5208f6df3-0038 | APPROVED |
| approval-bex-d4c5208f6df3-0039 | cismp-bex-d4c5208f6df3-0039 | APPROVED |
| approval-bex-d4c5208f6df3-0040 | cismp-bex-d4c5208f6df3-0040 | REJECTED |
| approval-bex-d4c5208f6df3-0041 | cismp-bex-d4c5208f6df3-0041 | APPROVED |
| approval-bex-d4c5208f6df3-0042 | cismp-bex-d4c5208f6df3-0042 | APPROVED |
| approval-bex-d4c5208f6df3-0043 | cismp-bex-d4c5208f6df3-0043 | APPROVED |
| approval-bex-d4c5208f6df3-0044 | cismp-bex-d4c5208f6df3-0044 | APPROVED |
| approval-bex-d4c5208f6df3-0045 | cismp-bex-d4c5208f6df3-0045 | APPROVED |
| approval-bex-d4c5208f6df3-0046 | cismp-bex-d4c5208f6df3-0046 | APPROVED |
| approval-bex-d4c5208f6df3-0047 | cismp-bex-d4c5208f6df3-0047 | REJECTED |
| approval-bex-d4c5208f6df3-0048 | cismp-bex-d4c5208f6df3-0048 | APPROVED |
| approval-bex-d4c5208f6df3-0049 | cismp-bex-d4c5208f6df3-0049 | REJECTED |
| approval-bex-d4c5208f6df3-0050 | cismp-bex-d4c5208f6df3-0050 | APPROVED |
| approval-bex-d4c5208f6df3-0051 | cismp-bex-d4c5208f6df3-0051 | APPROVED |
| approval-bex-d4c5208f6df3-0052 | cismp-bex-d4c5208f6df3-0052 | APPROVED |
| approval-bex-d4c5208f6df3-0053 | cismp-bex-d4c5208f6df3-0053 | APPROVED |
| approval-bex-d4c5208f6df3-0054 | cismp-bex-d4c5208f6df3-0054 | APPROVED |
| approval-bex-d4c5208f6df3-0055 | cismp-bex-d4c5208f6df3-0055 | APPROVED |
| approval-bex-d4c5208f6df3-0056 | cismp-bex-d4c5208f6df3-0056 | APPROVED |
| approval-bex-d4c5208f6df3-0057 | cismp-bex-d4c5208f6df3-0057 | APPROVED |
| approval-bex-d4c5208f6df3-0058 | cismp-bex-d4c5208f6df3-0058 | APPROVED |
| approval-bex-d4c5208f6df3-0059 | cismp-bex-d4c5208f6df3-0059 | APPROVED |
| approval-bex-d4c5208f6df3-0060 | cismp-bex-d4c5208f6df3-0060 | APPROVED |
| approval-bex-d4c5208f6df3-0061 | cismp-bex-d4c5208f6df3-0061 | APPROVED |
| approval-bex-d4c5208f6df3-0062 | cismp-bex-d4c5208f6df3-0062 | REJECTED |
| approval-bex-d4c5208f6df3-0063 | cismp-bex-d4c5208f6df3-0063 | REJECTED |
| approval-bex-d4c5208f6df3-0064 | cismp-bex-d4c5208f6df3-0064 | APPROVED |
| approval-bex-d4c5208f6df3-0065 | cismp-bex-d4c5208f6df3-0065 | APPROVED |
| approval-bex-d4c5208f6df3-0066 | cismp-bex-d4c5208f6df3-0066 | APPROVED |
| approval-bex-d4c5208f6df3-0067 | cismp-bex-d4c5208f6df3-0067 | APPROVED |
| approval-bex-d4c5208f6df3-0068 | cismp-bex-d4c5208f6df3-0068 | APPROVED |
| approval-bex-d4c5208f6df3-0069 | cismp-bex-d4c5208f6df3-0069 | APPROVED |
| approval-bex-d4c5208f6df3-0070 | cismp-bex-d4c5208f6df3-0070 | APPROVED |
| approval-bex-d4c5208f6df3-0071 | cismp-bex-d4c5208f6df3-0071 | REJECTED |
| approval-bex-d4c5208f6df3-0072 | cismp-bex-d4c5208f6df3-0072 | APPROVED |
| approval-bex-d4c5208f6df3-0073 | cismp-bex-d4c5208f6df3-0073 | REJECTED |
| approval-bex-d4c5208f6df3-0074 | cismp-bex-d4c5208f6df3-0074 | APPROVED |
| approval-bex-d4c5208f6df3-0075 | cismp-bex-d4c5208f6df3-0075 | APPROVED |
| approval-bex-d4c5208f6df3-0076 | cismp-bex-d4c5208f6df3-0076 | APPROVED |
| approval-bex-d4c5208f6df3-0077 | cismp-bex-d4c5208f6df3-0077 | APPROVED |
| approval-bex-d4c5208f6df3-0078 | cismp-bex-d4c5208f6df3-0078 | APPROVED |
| approval-bex-d4c5208f6df3-0079 | cismp-bex-d4c5208f6df3-0079 | APPROVED |
| approval-bex-d4c5208f6df3-0080 | cismp-bex-d4c5208f6df3-0080 | APPROVED |
| approval-bex-d4c5208f6df3-0081 | cismp-bex-d4c5208f6df3-0081 | APPROVED |
| approval-bex-d4c5208f6df3-0082 | cismp-bex-d4c5208f6df3-0082 | APPROVED |
| approval-bex-d4c5208f6df3-0083 | cismp-bex-d4c5208f6df3-0083 | APPROVED |
| approval-bex-d4c5208f6df3-0084 | cismp-bex-d4c5208f6df3-0084 | APPROVED |
| approval-bex-d4c5208f6df3-0085 | cismp-bex-d4c5208f6df3-0085 | APPROVED |
| approval-bex-d4c5208f6df3-0086 | cismp-bex-d4c5208f6df3-0086 | APPROVED |
| approval-bex-d4c5208f6df3-0087 | cismp-bex-d4c5208f6df3-0087 | APPROVED |
| approval-bex-d4c5208f6df3-0088 | cismp-bex-d4c5208f6df3-0088 | APPROVED |
| approval-bex-d4c5208f6df3-0089 | cismp-bex-d4c5208f6df3-0089 | APPROVED |
| approval-bex-d4c5208f6df3-0090 | cismp-bex-d4c5208f6df3-0090 | APPROVED |
| approval-bex-d4c5208f6df3-0091 | cismp-bex-d4c5208f6df3-0091 | APPROVED |
| approval-bex-d4c5208f6df3-0092 | cismp-bex-d4c5208f6df3-0092 | APPROVED |
| approval-bex-d4c5208f6df3-0093 | cismp-bex-d4c5208f6df3-0093 | APPROVED |
| approval-bex-d4c5208f6df3-0094 | cismp-bex-d4c5208f6df3-0094 | APPROVED |
| approval-bex-d4c5208f6df3-0095 | cismp-bex-d4c5208f6df3-0095 | APPROVED |
| approval-bex-d4c5208f6df3-0096 | cismp-bex-d4c5208f6df3-0096 | APPROVED |
| approval-bex-d4c5208f6df3-0097 | cismp-bex-d4c5208f6df3-0097 | APPROVED |
| approval-bex-d4c5208f6df3-0098 | cismp-bex-d4c5208f6df3-0098 | APPROVED |
| approval-bex-d4c5208f6df3-0100 | cismp-bex-d4c5208f6df3-0100 | APPROVED |
| approval-bex-d4c5208f6df3-0101 | cismp-bex-d4c5208f6df3-0101 | APPROVED |
| approval-bex-d4c5208f6df3-0102 | cismp-bex-d4c5208f6df3-0102 | APPROVED |
| approval-bex-d4c5208f6df3-0103 | cismp-bex-d4c5208f6df3-0103 | APPROVED |

| Mesure tokens native | Somme | Messages couverts | Couverture assistant |
| --- | --- | --- | --- |
| input | 1548 | 339 | 100.0 % |
| output | 153449 | 339 | 100.0 % |
| reasoning | 0 | 339 | 100.0 % |
| total | 22149500 | 258 | 76.1 % |
| cache_read | 15459773 | 339 | 100.0 % |
| cache_write | 6534730 | 339 | 100.0 % |

Tokens entrée, sortie, raisonnement, cache et total sont des champs natifs séparés avec recouvrements possibles ; ils ne sont pas additionnés ni convertis en quota.

### Sondes de performance

Même prompt déterministe, modèle/fournisseur/xhigh, sans outil ni fichier ni réseau métier, dans des sessions dédiées jetables. Début avant la première tâche métier, cadence 30 minutes, fin après archivage avant rapport. TTMT = premier delta SSE du champ text observé − envoi ; débit = tokens sortie natifs / intervalle premier–dernier delta. Moyennes arithmétiques des seules sondes valides.

| Position | Horodatage | État | TTMT s | Débit tokens/s | Durée SSE s | Tokens sortie | Coût natif |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-11T17:44:42.615447+02:00 | success | 1.3208422660827637 | 110.28425120164948 | 14.232930660247803 | 1424 | 0.00082306 |
| +30 min | 2026-10-11T18:14:43.053224+02:00 | success | 1.6033506393432617 | 82.97695113358795 | 19.692711353302002 | 1501 | 0.00261737 |
| +60 min | 2026-10-11T18:44:43.480535+02:00 | success | 1.7370250225067139 | 133.60295382087426 | 12.425411462783813 | 1428 | 0.00258306 |
| +90 min | 2026-10-11T19:14:43.977529+02:00 | success | 1.7341816425323486 | 122.28188294543547 | 13.706519365310669 | 1464 | 0.00259998 |
| +120 min | 2026-10-11T19:50:54.860112+02:00 | success | 1.706279993057251 | 83.36260728629927 | 18.800275087356567 | 1425 | 0.00258165 |
| +150 min | 2026-10-11T20:14:43.377891+02:00 | success | 1.885240077972412 | 78.61292151969137 | 22.97592043876648 | 1658 | 0.00269116 |
| fin | 2026-10-11T20:24:07.379781+02:00 | success | 1.9431984424591064 | 87.83889802687621 | 18.211617469787598 | 1429 | 0.00083369 |

| Mesure | Valeur |
| --- | --- |
| Prévues / réussies / échouées ou non mesurables / manquées | 7 / 7 / 0 / 0 |
| Taux de réussite | 100.0 % |
| TTMT min / max s | 1.321 / 1.943 |
| Débit min / max tokens/s | 78.613 / 133.603 |
| Surcharge tokens | 10329 |
| Surcharge coût natif | 0.01472997 |
| Surcharge durée SSE s | 120.045 |

Runtime OpenCode conservé 1.18.35 ; broker natif et plugin/contrôleur observés 0.87.2. 1 redémarrage(s) CAB avec purge technique autorisée dans cet intervalle après refus sans effet ; sources et historiques natifs préservés. OpenCode jamais fermé ou redémarré.

## 2. Types de messages et d’outils

| Rôle message | Nombre | Part |
| --- | --- | --- |
| user | 137 | 28.8 % |
| assistant | 339 | 71.2 % |
| TOTAL | 476 | 100.0 % |

| Partie native | Nombre | Part |
| --- | --- | --- |
| text | 193 | 15.8 % |
| step-start | 269 | 22.0 % |
| reasoning | 269 | 22.0 % |
| tool | 232 | 19.0 % |
| step-finish | 258 | 21.1 % |
| compaction | 1 | 0.1 % |
| TOTAL | 1222 | 100.0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 204 | 60.2 % |
| absent | 81 | 23.9 % |
| stop | 54 | 15.9 % |
| TOTAL | 339 | 100.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 52 | 22.4 % | 51 | 98.1 % | 1 | 1.9 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_health | 1 | 0.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 37 | 15.9 % | 35 | 94.6 % | 0 | 0.0 % | 2 | 5.4 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 13 | 5.6 % | 12 | 92.3 % | 0 | 0.0 % | 1 | 7.7 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 0.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 4 | 1.7 % | 3 | 75.0 % | 0 | 0.0 % | 1 | 25.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 79 | 34.1 % | 66 | 83.5 % | 0 | 0.0 % | 13 | 16.5 % | 0 | 0.0 % |
| edit | 10 | 4.3 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 26 | 11.2 % | 22 | 84.6 % | 0 | 0.0 % | 4 | 15.4 % | 0 | 0.0 % |
| write | 9 | 3.9 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 232 | 100.0 % | 210 | 90.5 % | 1 | 0.4 % | 21 | 9.1 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-value-validation-v1/design.md | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-value-validation-v1/proposal.md | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-value-validation-v1/specs/bulk-operations/spec.md | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-value-validation-v1/specs/jobs/spec.md | 1 | 5.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-value-validation-v1/tasks.md | 2 | 10.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_execution_values.py | 4 | 21.1 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_execution_values_integration.py | 2 | 10.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_execution_values.py | 7 | 36.8 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 19 | 100.0 % | 19 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Chemins absolus intégraux ; nombres = tentatives natives d’écriture/édition, pas un diff Git. Les cinq artefacts du change ont été déplacés par archivage unique vers openspec/changes/archive/2026-10-11-add-bulk-runtime-value-validation-v1. Le présent rapport est publié ensuite sous un mandat distinct, hors périmètre temporel de collecte. Octets approuvés, UTF-8/LF et références préservées contrôlés.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 5 | 9.6 % | 4 | 80.0 % | 1 | 20.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PostgreSQL réel | 2 | 3.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| autre | 3 | 5.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| compilation Python | 3 | 5.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| prévol CAB | 10 | 19.2 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 28 | 53.8 % | 28 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 52 | 100.0 % | 51 | 98.1 % | 1 | 1.9 % | 0 | 0.0 % | 0 | 0.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -c 'from pathlib import Path import hashlib p=Path('"'"'o… | 3 | 5.8 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_execution_values.py | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_execution_value… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_execution_values.py | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 10 | 19.2 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-v… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 3 | 5.8 % | 2 | 66.7 % | 1 | 33.3 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 3.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 10 | 19.2 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_job_… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_kern… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_publ… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_execut… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_job_li… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 7 | 13.5 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_scope_… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_tenant… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_job_record | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_job_state | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_notificatio… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_semver_cons… | 1 | 1.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/test_bulk_opera… | 2 | 3.8 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 52 | 100.0 % | 51 | 98.1 % | 1 | 1.9 % | 0 | 0.0 % | 0 | 0.0 % |

Libellés limités à 100 caractères ; commandes intégrales et workdir vérifié conservés au checkpoint et dans les preuves natives.

### Commandes proposées et refusées (non exécutées)

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -c "p.write_bytes(b+bytes([10])) if __import__('hashlib')… | 1 | 11.1 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -c 'from pathlib import Path import hashlib p=Path('"'"'t… | 1 | 11.1 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -c 'from pathlib import Path import hashlib,json,zlib,bas… | 1 | 11.1 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec | 1 | 11.1 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 1 | 11.1 % | 0 | 0.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 4 | 44.4 % | 0 | 0.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 9 | 100.0 % | 0 | 0.0 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

## 5. Accès web

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web ni URL effectivement visitée dans les preuves natives de ce change. Les communications locales CAB/OpenCode et les connexions PG de tests ne sont pas des consultations web.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T15:41:50.293000+00:00 |
| Fin — après archivage | 2026-10-11T18:24:27.536952+00:00 |
| Durée globale (pauses et attentes incluses) | 02 h 42 min 37 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant travaux | 2026-10-11T17:44:42.615433+02:00 | N/A — get_usage_limits non exposé | N/A |
| Après archivage | 2026-10-11T20:24:27.617779+02:00 | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | N/A |

Fenêtre attendue codex 10080 minutes ; compte/fenêtre/réinitialisation non observables. Quotas partagés par compte : une variation peut inclure des tâches simultanées ; aucune attribution exclusive ni reconstruction en tokens/euros. Aucun quota fournisseur Qwen ne remplace ce relevé Codex.

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB | 135 | 58.2 % | 118 | 87.4 % | 0 | 0.0 % | 17 | 12.6 % | 0 | 0.0 % |
| commande | 52 | 22.4 % | 51 | 98.1 % | 1 | 1.9 % | 0 | 0.0 % | 0 | 0.0 % |
| fichier | 45 | 19.4 % | 41 | 91.1 % | 0 | 0.0 % | 4 | 8.9 % | 0 | 0.0 % |
| TOTAL | 232 | 100.0 % | 210 | 90.5 % | 1 | 0.4 % | 21 | 9.1 % | 0 | 0.0 % |

| Contrôle croisé | Nombre | Part du total global |
| --- | --- | --- |
| Somme types outils | 232 | 100.0 % |
| Somme domaines | 232 | 100.0 % |
| Somme résultats | 232 | 100.0 % |
| Total outils | 232 | 100.0 % |

Trois compilations et202 tests unittest réussis (72 ciblés dont processus frais sous gardes,130 régressions),2 scénarios PG réels isolés avec cleanup/connexions fermées. Strict du change sans issue ; global exit1 qualifié par exactement3 WARNING historiques et zéro nouvelle issue. Couverture mémoire B02/B09 uniquement ; runtime complet reste à poursuivre. Archivage unique prouvé. Git non inspecté, aucun commit/push. Accès externes limités aux communications LLM/pilotage autorisées et aux tests PG prévus le cas échéant ; secrets utilisés seulement dans les processus sécurisés autorisés de quotas et de tests PostgreSQL, aucune valeur transmise au modèle ou publiée. Ce jalon ne constitue pas la fin globale du RUN.
