# Statistiques de session — add-bulk-runtime-streaming-import-parsers-v1

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A version exacte non exposée | opencode-go | xhigh | 1.68 s | 95.517 | N/A durées actives non exposées |
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
| Change | add-bulk-runtime-streaming-import-parsers-v1 |
| Archive réelle | openspec/changes/archive/2026-10-12-add-bulk-runtime-streaming-import-parsers-v1 |
| Sessions | ses_ed2ee9f13ffer2R8XRMWoCZBT3 |
| Messages | 227 |
| Parties natives | 611 |
| Appels outils | 103 |
| Coût natif observé (champ cost) | 1.459981838 |
| Couverture coût messages assistant | 156 / 156 (100.0 %) |
| Tentatives de compactage natives | 2 |
| Compactages natifs réussis | 2 |
| Compactages natifs en erreur | 0 |

Le coût natif observé est le champ cost de la télémétrie, pas une facture. Devise non exposée par ces messages, aucune conversion déduite. Les champs présents à zéro dans un message interrompu ne prouvent pas une consommation fournisseur nulle ; seules les valeurs natives disponibles sont additionnées. Trois fichiers Python compilés, 34 nouveaux tests réussis (33 unitaires de parsing et un processus frais sous gardes positives), 258 régressions sur 34 modules réussies en une invocation. Strict du change zéro issue; global exit1 observé et qualifié par exactement trois WARNING historiques, zéro nouvelle issue. Parsing IMPORT incrémental CSV/NDJSON, mapping exact, EOF, bornes et diagnostics minimisés seulement: aucune validation métier ou mutation propriétaire, admission/worker, idempotence/outbox, provider production ou HTTP. Aucun PG rejoué car ORM/migrations inchangés; sources et preuves de persistance précédentes conservées par empreinte. Première implémentation partielle non validée, complétée dans le même fichier par socle/CSV/NDJSON puis revue et tests; aucune tâche cochée avant preuves. Proposition CAB211 sans approval_id rejetée sous AID réellement généré puis observée REJECTED, aucune permission/écriture, même session conservée et prévol frais réussi. Variations de lignes vides qualifiées par AST identique; procédure tasks et assertions du harnais omises restaurées sous mandats distincts, sans rejouer une écriture acquise. Deux phases CAB outillées préservées, aucun OpenCode fermé ni redémarré. Deux délais MCP -32001 sur request_validation216 et220 ont été réconciliés sur les mêmes approval_id, sans nouvelle demande/decision ni seconde exécution. Deux compactages OpenCode achevés et corrélés, Codex API native N/A, aucuncompactage conjointfabriqué.

| Décision CAB terminale distincte | Nombre | Part |
| --- | --- | --- |
| APPROVED | 27 | 96.4 % |
| REJECTED | 1 | 3.6 % |
| TOTAL | 28 | 100.0 % |

| approval_id | requestId | Décision |
| --- | --- | --- |
| approval-bex-d4c5208f6df3-0202 | cismp-bex-d4c5208f6df3-0202 | APPROVED |
| approval-bex-d4c5208f6df3-0203 | cismp-bex-d4c5208f6df3-0203 | APPROVED |
| approval-bex-d4c5208f6df3-0204 | cismp-bex-d4c5208f6df3-0204 | APPROVED |
| approval-bex-d4c5208f6df3-0205 | cismp-bex-d4c5208f6df3-0205 | APPROVED |
| approval-bex-d4c5208f6df3-0206 | cismp-bex-d4c5208f6df3-0206 | APPROVED |
| approval-bex-d4c5208f6df3-0207 | cismp-bex-d4c5208f6df3-0207 | APPROVED |
| approval-bex-d4c5208f6df3-0208 | cismp-bex-d4c5208f6df3-0208 | APPROVED |
| approval-bex-d4c5208f6df3-0209 | cismp-bex-d4c5208f6df3-0209 | APPROVED |
| approval-bex-d4c5208f6df3-0210 | cismp-bex-d4c5208f6df3-0210 | APPROVED |
| apr-f16d943e43624767 | cismp-bex-d4c5208f6df3-0211 | REJECTED |
| approval-bex-d4c5208f6df3-0212 | cismp-bex-d4c5208f6df3-0212 | APPROVED |
| approval-bex-d4c5208f6df3-0213 | cismp-bex-d4c5208f6df3-0213 | APPROVED |
| approval-bex-d4c5208f6df3-0214 | cismp-bex-d4c5208f6df3-0214 | APPROVED |
| approval-bex-d4c5208f6df3-0215 | cismp-bex-d4c5208f6df3-0215 | APPROVED |
| approval-bex-d4c5208f6df3-0216 | cismp-bex-d4c5208f6df3-0216 | APPROVED |
| approval-bex-d4c5208f6df3-0217 | cismp-bex-d4c5208f6df3-0217 | APPROVED |
| approval-bex-d4c5208f6df3-0218 | cismp-bex-d4c5208f6df3-0218 | APPROVED |
| approval-bex-d4c5208f6df3-0219 | cismp-bex-d4c5208f6df3-0219 | APPROVED |
| approval-bex-d4c5208f6df3-0220 | cismp-bex-d4c5208f6df3-0220 | APPROVED |
| approval-bex-d4c5208f6df3-0221 | cismp-bex-d4c5208f6df3-0221 | APPROVED |
| approval-bex-d4c5208f6df3-0222 | cismp-bex-d4c5208f6df3-0222 | APPROVED |
| approval-bex-d4c5208f6df3-0223 | cismp-bex-d4c5208f6df3-0223 | APPROVED |
| approval-bex-d4c5208f6df3-0224 | cismp-bex-d4c5208f6df3-0224 | APPROVED |
| approval-bex-d4c5208f6df3-0225 | cismp-bex-d4c5208f6df3-0225 | APPROVED |
| approval-bex-d4c5208f6df3-0226 | cismp-bex-d4c5208f6df3-0226 | APPROVED |
| approval-bex-d4c5208f6df3-0227 | cismp-bex-d4c5208f6df3-0227 | APPROVED |
| approval-bex-d4c5208f6df3-0228 | cismp-bex-d4c5208f6df3-0228 | APPROVED |
| approval-bex-d4c5208f6df3-0229 | cismp-bex-d4c5208f6df3-0229 | APPROVED |

| Mesure tokens native | Somme | Messages couverts | Couverture assistant |
| --- | --- | --- | --- |
| input | 768 | 156 | 100.0 % |
| output | 216229 | 156 | 100.0 % |
| reasoning | 0 | 156 | 100.0 % |
| total | 11910884 | 128 | 82.1 % |
| cache_read | 5329013 | 156 | 100.0 % |
| cache_write | 6364874 | 156 | 100.0 % |

Tokens entrée, sortie, raisonnement, cache et total sont des champs natifs séparés avec recouvrements possibles ; ils ne sont pas additionnés ni convertis en quota.

### Sondes de performance

Même prompt déterministe, modèle/fournisseur/xhigh, sans outil ni fichier ni réseau métier, dans des sessions dédiées jetables. Début avant la première tâche métier, cadence 30 minutes, fin après archivage avant rapport. TTMT = premier delta SSE du champ text observé − envoi ; débit = tokens sortie natifs / intervalle premier–dernier delta. Moyennes arithmétiques des seules sondes valides.

| Position | Horodatage | État | TTMT s | Débit tokens/s | Durée SSE s | Tokens sortie | Coût natif |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-12T00:25:56.082694+02:00 | success | 1.4795265197753906 | 90.51439935519774 | 17.24497389793396 | 1427 | 0.00258259 |
| +30 min | 2026-10-12T00:55:56.846607+02:00 | success | 1.9161803722381592 | 82.59124127421205 | 19.109286785125732 | 1420 | 0.0025793 |
| +60 min | 2026-10-12T01:25:57.446790+02:00 | success | 1.7078235149383545 | 110.96413407520429 | 14.504751205444336 | 1420 | 0.0025793 |
| +90 min | 2026-10-12T01:55:58.381634+02:00 | success | 1.2084317207336426 | 103.07948612348856 | 14.984208583831787 | 1420 | 0.0025793 |
| fin | 2026-10-12T02:00:28.813481+02:00 | success | 2.0879409313201904 | 90.43459408390909 | 17.867300748825073 | 1427 | 0.00082447 |

| Mesure | Valeur |
| --- | --- |
| Prévues / réussies / échouées ou non mesurables / manquées | 5 / 5 / 0 / 0 |
| Taux de réussite | 100.0 % |
| TTMT min / max s | 1.208 / 2.088 |
| Débit min / max tokens/s | 82.591 / 110.964 |
| Surcharge tokens | 7114 |
| Surcharge coût natif | 0.01114496 |
| Surcharge durée SSE s | 83.711 |

Runtime OpenCode conservé 1.18.35 ; broker natif et plugin/contrôleur observés 0.87.2. 0 redémarrage(s) CAB avec purge technique autorisée dans cet intervalle après refus sans effet ; sources et historiques natifs préservés. OpenCode jamais fermé ou redémarré.

## 2. Types de messages et d’outils

| Rôle message | Nombre | Part |
| --- | --- | --- |
| user | 71 | 31.3 % |
| assistant | 156 | 68.7 % |
| TOTAL | 227 | 100.0 % |

| Partie native | Nombre | Part |
| --- | --- | --- |
| text | 120 | 19.6 % |
| step-start | 129 | 21.1 % |
| reasoning | 129 | 21.1 % |
| tool | 103 | 16.9 % |
| step-finish | 128 | 20.9 % |
| compaction | 2 | 0.3 % |
| TOTAL | 611 | 100.0 % |

| Fin assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 86 | 55.1 % |
| stop | 42 | 26.9 % |
| absent | 28 | 17.9 % |
| TOTAL | 156 | 100.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 13 | 12.6 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 9 | 8.7 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 3 | 2.9 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 29 | 28.2 % | 26 | 89.7 % | 0 | 0.0 % | 3 | 10.3 % | 0 | 0.0 % |
| edit | 4 | 3.9 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 35 | 34.0 % | 28 | 80.0 % | 3 | 8.6 % | 4 | 11.4 % | 0 | 0.0 % |
| write | 10 | 9.7 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 103 | 100.0 % | 93 | 90.3 % | 3 | 2.9 % | 7 | 6.8 % | 0 | 0.0 % |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-streaming-import-parsers-v1/design.md | 1 | 7.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-streaming-import-parsers-v1/proposal.md | 1 | 7.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-streaming-import-parsers-v1/specs/bulk-operations/spec.md | 1 | 7.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-streaming-import-parsers-v1/tasks.md | 3 | 21.4 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_streaming_import.py | 5 | 35.7 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_streaming_import_integration.py | 2 | 14.3 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_streaming_import.py | 1 | 7.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 14 | 100.0 % | 14 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Chemins absolus intégraux ; nombres = tentatives natives d’écriture/édition, pas un diff Git. Les 4 artefacts du change ont été déplacés par archivage unique vers openspec/changes/archive/2026-10-12-add-bulk-runtime-streaming-import-parsers-v1. Le présent rapport est publié ensuite sous un mandat distinct, hors périmètre temporel de collecte. Octets approuvés, UTF-8/LF et références préservées contrôlés.

## 4. Commandes

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archivage | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 4 | 30.8 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| compilation Python | 3 | 23.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| prévol CAB | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| unittest | 3 | 23.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 13 | 100.0 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_streaming_import.py | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_streaming_impor… | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_streaming_import.py | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-s… | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_stream… | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 13 | 100.0 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |

Libellés limités à 100 caractères ; commandes intégrales et workdir vérifié conservés au checkpoint et dans les preuves natives.

### Commandes proposées et refusées (non exécutées)

Aucune commande CAB refusée.

## 5. Accès web

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web ni URL effectivement visitée dans les preuves natives de ce change. Les communications locales CAB/OpenCode et les connexions PG de tests ne sont pas des consultations web.

| Documentation primaire consultée par orchestrateur | URL |
| --- | --- |
| Lecture technique | https://docs.python.org/3.12/library/csv.html |
| Lecture technique | https://docs.python.org/3.12/library/json.html |

Consultations web de l’orchestrateur déclarées : 2 appels et 2 URL distinctes. Hors compteurs OpenCode ci-dessus ; aucune donnée secrète transmise, aucun téléchargement exécuté.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T22:24:36.330000+00:00 |
| Fin — après archivage | 2026-10-12T00:00:47.109137+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 36 min 10 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant travaux | 2026-10-12T00:25:56.082684+02:00 | N/A — get_usage_limits non exposé | N/A |
| Après archivage | 2026-10-12T02:00:47.186847+02:00 | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | N/A |

Fenêtre attendue codex 10080 minutes ; compte/fenêtre/réinitialisation non observables. Quotas partagés par compte : une variation peut inclure des tâches simultanées ; aucune attribution exclusive ni reconstruction en tokens/euros. Aucun quota fournisseur Qwen ne remplace ce relevé Codex.

| Catégorie | Total | Part | Aboutis | Taux aboutis | Refusés | Taux refusés | Erreurs | Taux erreurs | Non terminés | Taux non terminés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB | 41 | 39.8 % | 38 | 92.7 % | 0 | 0.0 % | 3 | 7.3 % | 0 | 0.0 % |
| commande | 13 | 12.6 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 | 0.0 % |
| fichier | 49 | 47.6 % | 42 | 85.7 % | 3 | 6.1 % | 4 | 8.2 % | 0 | 0.0 % |
| TOTAL | 103 | 100.0 % | 93 | 90.3 % | 3 | 2.9 % | 7 | 6.8 % | 0 | 0.0 % |

| Contrôle croisé | Nombre | Part du total global |
| --- | --- | --- |
| Somme types outils | 103 | 100.0 % |
| Somme domaines | 103 | 100.0 % |
| Somme résultats | 103 | 100.0 % |
| Total outils | 103 | 100.0 % |

Trois fichiers Python compilés, 34 nouveaux tests réussis (33 unitaires de parsing et un processus frais sous gardes positives), 258 régressions sur 34 modules réussies en une invocation. Strict du change zéro issue; global exit1 observé et qualifié par exactement trois WARNING historiques, zéro nouvelle issue. Parsing IMPORT incrémental CSV/NDJSON, mapping exact, EOF, bornes et diagnostics minimisés seulement: aucune validation métier ou mutation propriétaire, admission/worker, idempotence/outbox, provider production ou HTTP. Aucun PG rejoué car ORM/migrations inchangés; sources et preuves de persistance précédentes conservées par empreinte. Première implémentation partielle non validée, complétée dans le même fichier par socle/CSV/NDJSON puis revue et tests; aucune tâche cochée avant preuves. Proposition CAB211 sans approval_id rejetée sous AID réellement généré puis observée REJECTED, aucune permission/écriture, même session conservée et prévol frais réussi. Variations de lignes vides qualifiées par AST identique; procédure tasks et assertions du harnais omises restaurées sous mandats distincts, sans rejouer une écriture acquise. Deux phases CAB outillées préservées, aucun OpenCode fermé ni redémarré. Deux délais MCP -32001 sur request_validation216 et220 ont été réconciliés sur les mêmes approval_id, sans nouvelle demande/decision ni seconde exécution. Deux compactages OpenCode achevés et corrélés, Codex API native N/A, aucuncompactage conjointfabriqué. Archivage unique prouvé. Git non inspecté, aucun commit/push. Accès externes limités aux communications LLM/pilotage autorisées, aux tests PG prévus et aux lectures de documentation primaire déclarées le cas échéant ; secrets utilisés seulement dans les processus sécurisés autorisés de quotas et de tests PostgreSQL, aucune valeur transmise au modèle ou publiée. Ce jalon ne constitue pas la fin globale du RUN.
