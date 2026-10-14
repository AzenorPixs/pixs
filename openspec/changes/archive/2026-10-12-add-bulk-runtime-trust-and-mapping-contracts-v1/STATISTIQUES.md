# Statistiques de session — add-bulk-runtime-trust-and-mapping-contracts-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A version exacte non exposée | opencode-go | xhigh | 1.6 s | 89.124 | N/A durées actives non exposées |
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
| Change | add-bulk-runtime-trust-and-mapping-contracts-v1 |
| Archive réelle | openspec/changes/archive/2026-10-12-add-bulk-runtime-trust-and-mapping-contracts-v1 |
| Sessions | ses_ed35771b7ffeYdJStu4exhJLAI, ses_ed321b2adffehKtnZSQOPE31lg, ses_ed311519dffeeLTcmExyepmH4u |
| Messages | 210 |
| Parties natives | 569 |
| Appels outils | 110 |
| Coût natif observé (champ cost) | 0.996213854 |
| Couverture coût messages assistant | 149 / 149 (100.0 %) |
| Tentatives de compactage natives | 1 |
| Compactages natifs réussis | 1 |
| Compactages natifs en erreur | 0 |

Le coût natif observé est le champ cost de la télémétrie, pas une facture. Devise non exposée par ces messages, aucune conversion déduite. Les champs présents à zéro dans un message interrompu ne prouvent pas une consommation fournisseur nulle ; seules les valeurs natives disponibles sont additionnées. Cinq fichiers Python compilés, 54 nouveaux tests réussis (30 contrats, 23 ports synthétiques, un processus frais sous gardes positives), 204 régressions sur 31 modules regroupées en une invocation réussie. Strict du change zéro issue; global exit1 observé et qualifié par exactement trois WARNING historiques, zéro nouvelle issue. Aucun PG rejoué car ORM/migrations inchangés, preuves et sources du lot de persistance conservées par empreinte. Couverture des sept contrats et des seules frontières/composition serveur autorité/mapping; aucun provider de production, admission, worker, parsing effectif, idempotence/outbox ou mutation propriétaire. Deux permissions natives refusées avant effet (write sans CAB puis compilation sans CAB), récupérations du même change avec sources conservées; pilotage en deux phases ensuite éprouvé, outils d'exécution masqués jusqu'au receipt MCP APPROVED unique, sans double décision ni réécriture acquise. OpenCode jamais fermé ni redémarré. Trois délais MCP -32001 (request_validation182, poll_approval182, request_validation196) ont été réconciliés par les receipts corrélés des mêmes approval_id; aucune seconde décision ni seconde exécution.

| Décision CAB terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 29 | 100.0 % |
| TOTAL | 29 | 100.0 % |

| approval_id | requestId | Décision |
| --- | --- | --- |
| approval-bex-d4c5208f6df3-0170 | cismp-bex-d4c5208f6df3-0170 | APPROVED |
| approval-bex-d4c5208f6df3-0171 | cismp-bex-d4c5208f6df3-0171 | APPROVED |
| approval-bex-d4c5208f6df3-0172 | cismp-bex-d4c5208f6df3-0172 | APPROVED |
| approval-bex-d4c5208f6df3-0173 | cismp-bex-d4c5208f6df3-0173 | APPROVED |
| approval-bex-d4c5208f6df3-0174 | cismp-bex-d4c5208f6df3-0174 | APPROVED |
| approval-bex-d4c5208f6df3-0175 | cismp-bex-d4c5208f6df3-0175 | APPROVED |
| approval-bex-d4c5208f6df3-0176 | cismp-bex-d4c5208f6df3-0176 | APPROVED |
| approval-bex-d4c5208f6df3-0177 | cismp-bex-d4c5208f6df3-0177 | APPROVED |
| approval-bex-d4c5208f6df3-0178 | cismp-bex-d4c5208f6df3-0178 | APPROVED |
| approval-bex-d4c5208f6df3-0179 | cismp-bex-d4c5208f6df3-0179 | APPROVED |
| approval-bex-d4c5208f6df3-0180 | cismp-bex-d4c5208f6df3-0180 | APPROVED |
| approval-bex-d4c5208f6df3-0181 | cismp-bex-d4c5208f6df3-0181 | APPROVED |
| approval-bex-d4c5208f6df3-0182 | cismp-bex-d4c5208f6df3-0182 | APPROVED |
| approval-bex-d4c5208f6df3-0183 | cismp-bex-d4c5208f6df3-0183 | APPROVED |
| approval-bex-d4c5208f6df3-0185 | cismp-bex-d4c5208f6df3-0185 | APPROVED |
| approval-bex-d4c5208f6df3-0186 | cismp-bex-d4c5208f6df3-0186 | APPROVED |
| approval-bex-d4c5208f6df3-0187 | cismp-bex-d4c5208f6df3-0187 | APPROVED |
| approval-bex-d4c5208f6df3-0189 | cismp-bex-d4c5208f6df3-0189 | APPROVED |
| approval-bex-d4c5208f6df3-0190 | cismp-bex-d4c5208f6df3-0190 | APPROVED |
| approval-bex-d4c5208f6df3-0191 | cismp-bex-d4c5208f6df3-0191 | APPROVED |
| approval-bex-d4c5208f6df3-0192 | cismp-bex-d4c5208f6df3-0192 | APPROVED |
| approval-bex-d4c5208f6df3-0193 | cismp-bex-d4c5208f6df3-0193 | APPROVED |
| approval-bex-d4c5208f6df3-0194 | cismp-bex-d4c5208f6df3-0194 | APPROVED |
| approval-bex-d4c5208f6df3-0195 | cismp-bex-d4c5208f6df3-0195 | APPROVED |
| approval-bex-d4c5208f6df3-0196 | cismp-bex-d4c5208f6df3-0196 | APPROVED |
| approval-bex-d4c5208f6df3-0197 | cismp-bex-d4c5208f6df3-0197 | APPROVED |
| approval-bex-d4c5208f6df3-0198 | cismp-bex-d4c5208f6df3-0198 | APPROVED |
| approval-bex-d4c5208f6df3-0199 | cismp-bex-d4c5208f6df3-0199 | APPROVED |
| approval-bex-d4c5208f6df3-0200 | cismp-bex-d4c5208f6df3-0200 | APPROVED |

| Mesure tokens native | Somme | Messages couverts | Couverture assistant |
| --- | --- | --- | --- |
| input | 720 | 149 | 100.0 % |
| output | 145897 | 149 | 100.0 % |
| reasoning | 0 | 149 | 100.0 % |
| total | 8886112 | 120 | 80.5 % |
| cache_read | 4458504 | 149 | 100.0 % |
| cache_write | 4280991 | 149 | 100.0 % |

Tokens entrée, sortie, raisonnement, cache et total sont des champs natifs séparés avec recouvrements possibles ; ils ne sont pas additionnés ni convertis en quota.

### Sondes de performance

Même prompt déterministe, modèle/fournisseur/xhigh, sans outil ni fichier ni réseau métier, dans des sessions dédiées jetables. Début avant la première tâche métier, cadence 30 minutes, fin après archivage avant rapport. TTMT = premier delta SSE du champ text observé − envoi ; débit = tokens sortie natifs / intervalle premier–dernier delta. Moyennes arithmétiques des seules sondes valides.

| Position | Horodatage | État | TTMT s | Débit tokens/s | Durée SSE s | Tokens sortie | Coût natif |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-11T22:31:31.515466+02:00 | success | 1.457449197769165 | 91.74204167799594 | 17.011931896209717 | 1427 | 0.00258259 |
| +30 min | 2026-10-11T23:01:31.860301+02:00 | success | 1.985525369644165 | 105.4127343367489 | 15.522789239883423 | 1427 | 0.00258259 |
| +60 min | 2026-10-11T23:31:32.503016+02:00 | success | 1.2732048034667969 | 77.64341762401618 | 35.4679901599884 | 2655 | 0.00315975 |
| +90 min | 2026-10-12T00:01:33.394518+02:00 | success | 1.69154953956604 | 83.03280891152443 | 18.805266618728638 | 1421 | 0.00257977 |
| fin | 2026-10-12T00:03:10.366451+02:00 | success | 1.5926055908203125 | 87.78889592814951 | 17.972809314727783 | 1438 | 0.00082964 |

| Mesure | Valeur |
| --- | --- |
| Prévues / réussies / échouées ou non mesurables / manquées | 5 / 5 / 0 / 0 |
| Taux de réussite | 100.0 % |
| TTMT min / max s | 1.273 / 1.986 |
| Débit min / max tokens/s | 77.643 / 105.413 |
| Surcharge tokens | 8368 |
| Surcharge coût natif | 0.01173434 |
| Surcharge durée SSE s | 104.781 |

Runtime OpenCode conservé 1.18.35 ; broker natif et plugin/contrôleur observés 0.87.2. 0 redémarrage(s) CAB avec purge technique autorisée dans cet intervalle après refus sans effet ; sources et historiques natifs préservés. OpenCode jamais fermé ou redémarré.

## 2. Types de messages et d’outils

| Rôle message | Nombre | Part |
| --- | --- | --- |
| user | 61 | 29.0 % |
| assistant | 149 | 71.0 % |
| TOTAL | 210 | 100.0 % |

| Partie native | Nombre | Part |
| --- | --- | --- |
| text | 98 | 17.2 % |
| step-start | 120 | 21.1 % |
| reasoning | 120 | 21.1 % |
| tool | 110 | 19.3 % |
| step-finish | 120 | 21.1 % |
| compaction | 1 | 0.2 % |
| TOTAL | 569 | 100.0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 91 | 61.1 % |
| stop | 29 | 19.5 % |
| absent | 29 | 19.5 % |
| TOTAL | 149 | 100.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 18 | 16.4 % | 17 | 94.4 % | 1 | 5.6 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 10 | 9.1 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 4 | 3.6 % | 3 | 75.0 % | 0 | 0.0 % | 1 | 25.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 29 | 26.4 % | 27 | 93.1 % | 0 | 0.0 % | 2 | 6.9 % | 0 | 0.0 % |
| glob | 3 | 2.7 % | 0 | 0.0 % | 0 | 0.0 % | 3 | 100.0 % | 0 | 0.0 % |
| read | 33 | 30.0 % | 25 | 75.8 % | 7 | 21.2 % | 1 | 3.0 % | 0 | 0.0 % |
| write | 13 | 11.8 % | 12 | 92.3 % | 1 | 7.7 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 110 | 100.0 % | 94 | 85.5 % | 9 | 8.2 % | 7 | 6.4 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-trust-and-mapping-contracts-v1/design.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-trust-and-mapping-contracts-v1/proposal.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-trust-and-mapping-contracts-v1/specs/bulk-operations/spec.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-trust-and-mapping-contracts-v1/tasks.md | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_runtime_contracts.py | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_trusted_ports.py | 3 | 23.1 % | 2 | 66.7 % | 1 | 33.3 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_runtime_trust_integration.py | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_runtime_contracts.py | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_trusted_ports.py | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 13 | 100.0 % | 12 | 92.3 % | 1 | 7.7 % | 0 | 0.0 % | 0 | 0.0 % |

Chemins absolus intégraux ; nombres = tentatives natives d’écriture/édition, pas un diff Git. Les 4 artefacts du change ont été déplacés par archivage unique vers openspec/changes/archive/2026-10-12-add-bulk-runtime-trust-and-mapping-contracts-v1. Le présent rapport est publié ensuite sous un mandat distinct, hors périmètre temporel de collecte. Octets approuvés, UTF-8/LF et références préservées contrôlés.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 4 | 22.2 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| compilation Python | 6 | 33.3 % | 5 | 83.3 % | 1 | 16.7 % | 0 | 0.0 % | 0 | 0.0 % |
| prévol CAB | 3 | 16.7 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 4 | 22.2 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 18 | 100.0 % | 17 | 94.4 % | 1 | 5.6 % | 0 | 0.0 % | 0 | 0.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_runtime_contracts.py | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_trusted_ports.py | 2 | 11.1 % | 1 | 50.0 % | 1 | 50.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_runtime_trust_i… | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_runtime_contracts.py | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_trusted_ports.py | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 3 | 16.7 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-t… | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 2 | 11.1 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 11.1 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_runtim… | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_truste… | 1 | 5.6 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 18 | 100.0 % | 17 | 94.4 % | 1 | 5.6 % | 0 | 0.0 % | 0 | 0.0 % |

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
| Début | 2026-10-11T20:30:06.613000+00:00 |
| Fin — après archivage | 2026-10-11T22:03:31.584925+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 33 min 24 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant travaux | 2026-10-11T22:31:31.515455+02:00 | N/A — get_usage_limits non exposé | N/A |
| Après archivage | 2026-10-12T00:03:31.631513+02:00 | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | N/A |

Fenêtre attendue codex 10080 minutes ; compte/fenêtre/réinitialisation non observables. Quotas partagés par compte : une variation peut inclure des tâches simultanées ; aucune attribution exclusive ni reconstruction en tokens/euros. Aucun quota fournisseur Qwen ne remplace ce relevé Codex.

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB | 43 | 39.1 % | 40 | 93.0 % | 0 | 0.0 % | 3 | 7.0 % | 0 | 0.0 % |
| commande | 18 | 16.4 % | 17 | 94.4 % | 1 | 5.6 % | 0 | 0.0 % | 0 | 0.0 % |
| fichier | 49 | 44.5 % | 37 | 75.5 % | 8 | 16.3 % | 4 | 8.2 % | 0 | 0.0 % |
| TOTAL | 110 | 100.0 % | 94 | 85.5 % | 9 | 8.2 % | 7 | 6.4 % | 0 | 0.0 % |

| Contrôle croisé | Nombre | Part du total global |
| --- | --- | --- |
| Somme types outils | 110 | 100.0 % |
| Somme domaines | 110 | 100.0 % |
| Somme résultats | 110 | 100.0 % |
| Total outils | 110 | 100.0 % |

Cinq fichiers Python compilés, 54 nouveaux tests réussis (30 contrats, 23 ports synthétiques, un processus frais sous gardes positives), 204 régressions sur 31 modules regroupées en une invocation réussie. Strict du change zéro issue; global exit1 observé et qualifié par exactement trois WARNING historiques, zéro nouvelle issue. Aucun PG rejoué car ORM/migrations inchangés, preuves et sources du lot de persistance conservées par empreinte. Couverture des sept contrats et des seules frontières/composition serveur autorité/mapping; aucun provider de production, admission, worker, parsing effectif, idempotence/outbox ou mutation propriétaire. Deux permissions natives refusées avant effet (write sans CAB puis compilation sans CAB), récupérations du même change avec sources conservées; pilotage en deux phases ensuite éprouvé, outils d'exécution masqués jusqu'au receipt MCP APPROVED unique, sans double décision ni réécriture acquise. OpenCode jamais fermé ni redémarré. Trois délais MCP -32001 (request_validation182, poll_approval182, request_validation196) ont été réconciliés par les receipts corrélés des mêmes approval_id; aucune seconde décision ni seconde exécution. Archivage unique prouvé. Git non vérifié, aucun commit/push. Accès externes limités aux communications LLM/pilotage autorisées et aux tests PG autorisés ; secrets utilisés seulement dans les processus sécurisés autorisés de quotas et de tests PostgreSQL, aucune valeur transmise au modèle ou publiée. Ce jalon ne constitue pas la fin globale du RUN.
