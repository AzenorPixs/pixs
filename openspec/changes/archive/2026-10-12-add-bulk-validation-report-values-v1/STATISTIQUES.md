# STATISTIQUES — add-bulk-validation-report-values-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-validation-report-values-v1`. Session : `ses_ecfb0b00fffemV6Whsuy9tsHJr`. RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historique natif de la session jusqu’au relevé final après archivage ; sondes jetables et rédaction du rapport exclues. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 3.306 s | 289.315 | N/A |
| muse-spark-1.3-contributor, agent compaction | OpenCode 1.19.0 ; modèle N/A | opencode-go | N/A — variant non exposé par summarize | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des sondes valides sur texte visible. Temps de service actif et dénominateur cumulé tous agents : N/A ; ne pas assimiler pauses, outils ou durée calendaire à de la génération. Chevauchements d’activité possibles.

## 1. Statistiques générales et décisions

193 messages ; 115 outils : 113 succès (98.3 %), 0 refus (0.0 %), 2 erreurs (1.7 %). 15 décisions CAB uniques approved (100 %) et autant de permissions natives once corrélées ; aucun refus.

284 tests réussis sans ignoré, 3 fichiers compilés, strict change code0 sans issue. Global strict code1 limité aux 3 WARNING historiques exacts de longueur, non présenté comme validation globale verte. Archive unique --skip-specs, canon préservé.

Convention : succès d’un outil ne prouve pas une approbation manuelle ; lectures peuvent être autorisées automatiquement. Les opérations mutantes/commandes ont une décision CGPT explicite unique. Refus = permission rejetée ; erreur = échec technique sans refus.

Erreur native observée : read — File not found: /home/devops/datas/pixs/openspec/changes/add-bulk-validation-report-values-v1 ; cgpt-validation_request_validation — MCP error -32602: parametre 'commands' : liste non vide obligatoire. La lecture du dossier absent a précédé sa création autorisée. La requête MCP avait commands en chaîne vide au lieu de tableau vide : rejet de schéma avant soumission/approbation/effet, puis demande neuve correcte. Un mandat tasks apparu tard a été repris avec sa même approbation et une seule écriture, sans rejouer. Son titre hérité CommandIdempotency était trompeur ; change_id et chemin ValidationReport étaient exacts et ont été contrôlés. Aucune permission non corrélée ni effet inconnu.

Compactage natif OpenCode : 1, cycle cismp-compact-dbef6dd2cafe, 15:54:52–15:55:06 Europe/Paris, résumé terminé et SSE session.compacted corrélés, artefacts inchangés puis réellement relus. Même modèle/fournisseur imposés ; variant absent des métadonnées du compactor, sans valeur inventée. API Codex non exposée : moitié Codex non exécutée, aucune réussite conjointe déclarée.

Sondes valides : 3/3 (100.0 %), 0 échec. Initiale, relève périodique et finale réellement mesurées. Relève prévue à 16:02:09, envoyée à 16:03:17, retard réel de 67,3 s enregistré. Aucune relève reconstruite. La suivante à 16:32:09 est postérieure à la fin de l’intervalle.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début | 2026-10-12T15:32:01.598890+02:00 | 3.986 | 272.134 | 909 |
| périodique — heure réelle | 2026-10-12T16:03:17.169516+02:00 | 2.694 | 313.656 | 902 |
| fin | 2026-10-12T16:21:40.570320+02:00 | 3.236 | 282.155 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT min/max 2.694/3.986 s ; débit min/max 272.134/313.656. Surcharge hors production : 2701 tokens sortie, coût natif 0.004027226.

Les brouillons ajoutant des normes B13, des champs/progressions/modes erronés, un faux Diagnostic, une limite de 500 inventée, des signatures incorrectes, des captures générales ou un appel à l’horloge ont été rejetés avant écriture/exécution. Codex orchestrateur a reconstruit les contenus correctifs depuis les helpers réellement lus ; OpenCode les a écrits sous mandats unitaires explicites, avec égalité des octets, puis les 284 tests réels ont réussi. Les brouillons ne sont pas des refus natifs et leurs défauts ne sont pas ajoutés aux compteurs d’outils.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 62 | 32.1 % |
| assistant | 131 | 67.9 % |
| Total | 193 | 100 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 192 | 26.7 % |
| step-start | 131 | 18.2 % |
| reasoning | 149 | 20.7 % |
| tool | 115 | 16.0 % |
| step-finish | 131 | 18.2 % |
| compaction | 1 | 0.1 % |
| Total | 719 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 38 | 33.0 % | 38 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 3 | 2.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 21 | 18.3 % | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 16 | 13.9 % | 15 (93.8 %) | 0 (0.0 %) | 1 (6.2 %) |
| glob | 4 | 3.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 16 | 13.9 % | 15 (93.8 %) | 0 (0.0 %) | 1 (6.2 %) |
| write | 9 | 7.8 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 6 | 5.2 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 115 | 100 % | 113 (98.3 %) | 0 (0.0 %) | 2 (1.7 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 76 | 58.0 % |
| stop | 55 | 42.0 % |
| Total | 131 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 922735 | 8.5 % |
| output | 39205 | 0.4 % |
| reasoning | 23093 | 0.2 % |
| cache_read | 9815002 | 90.9 % |
| cache_write | 0 | 0.0 % |
| Total | 10800035 | 100 % |

Coût natif cumulé 0.124363104 ; unité/devise non exposée par l’API, aucune conversion.

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-validation-report-values-v1/proposal.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-validation-report-values-v1/design.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-validation-report-values-v1/tasks.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-validation-report-values-v1/specs/bulk-operations/spec.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_validation_report_values.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_validation_report_values.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_validation_report_integration.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Compteurs = tentatives write/edit, pas lignes de code. tasks.md écrit puis coché après preuves. Artefacts déplacés par archivage, chemins actuels ci-dessus. Rapport publié après les bornes sous mandat distinct, sans auto-comptage. Aucun ancien code/export/canon/cadrage modifié.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 4 | 66.7 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 1 | 16.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 1 | 16.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 6 | 100 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucune commande refusée : 0 (0.0 %). Commandes complètes et requestId conservés dans historique natif/checkpoint ; libellés ci-dessus inférieurs à 100 caractères.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Inférence LLM, quotas fournisseurs et API locales autorisés hors de ce domaine. Aucun service métier externe ni déploiement.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-12T15:31:09.155804+02:00 |
| Fin — après archivage | 2026-10-12T16:21:47.976059+02:00 |
| Durée globale, pauses/attentes incluses | 00 h 50 min 38 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T15:31:09.204259+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T16:21:47.976096+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : codex/window10080/usedPercent/resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 100 | 87.0 % | 98 (98.0 %) | 0 (0.0 %) | 2 (2.0 %) |
| commandes | 6 | 5.2 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 9 | 7.8 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 115 | 100 % | 113 (98.3 %) | 0 (0.0 %) | 2 (1.7 %) |

Totaux par type/domaine vérifiés : 115 appels, 113 succès, 0 refus, 2 erreurs. Pourcentages à une décimale, écarts d’arrondi possibles.

Résultat : 284 tests, 3 fichiers compilés, strict change0 ; global1 qualifié par 3 WARNING historiques. Validation et capture des huit valeurs ValidationReportV1, diagnostics bornés par PolicyV1 et catalogues explicites, Progress/RowDiagnostic immuables sans alias et contraintes mémoire mode/progression canoniques. Aucune preuve de compteurs réels, de complétude, d’autorisation, d’arrêt ou de transaction. Aucun test PostgreSQL réel nécessaire à ce périmètre ; pas de frontend/navigateur concerné. Git non inspecté, aucun commit/push, aucun déploiement. Secrets confinés aux processus autorisés et authnative, aucune valeur dans modèle/rapport/sources. Instruction finale du développeur : après cette archive et ce rapport conformes, clôturer immédiatement la session et OpenCode sans nouveau change ; le projet global n’est pas déclaré entièrement implémenté.
