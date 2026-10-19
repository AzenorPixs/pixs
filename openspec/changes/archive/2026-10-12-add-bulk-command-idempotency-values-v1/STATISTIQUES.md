# STATISTIQUES — add-bulk-command-idempotency-values-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1`. Session : `ses_ed0798c72ffel52EXPM4afG4S5`. RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historique natif de la session jusqu’au relevé final après archivage ; sondes jetables et rédaction du rapport exclues. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 2.723 s | 273.426 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des sondes valides sur texte visible. Temps de service actif et dénominateur cumulé tous agents : N/A ; ne pas assimiler pauses, outils ou durée calendaire à de la génération. Chevauchements d’activité possibles.

## 1. Statistiques générales et décisions

191 messages ; 114 outils : 113 succès (99.1 %), 0 refus (0.0 %), 1 erreur (0.9 %). 20 décisions CAB uniques approved (100 %) et autant de permissions natives once corrélées ; aucun refus.

178 tests réussis sans ignoré, 3 compilations, strict change code0 sans issue. Global strict code1 limité aux 3 WARNING historiques exacts de longueur, non présenté comme validation globale verte. Archive unique --skip-specs, canon préservé.

Convention : succès d’un outil ne prouve pas une approbation manuelle ; lectures peuvent être autorisées automatiquement. Les opérations mutantes/commandes ont une décision CGPT explicite unique. Refus = permission rejetée ; erreur = échec technique sans refus.

Erreur native observée : read — File not found: /home/devops/datas/pixs/openspec/changes/add-bulk-command-idempotency-values-v1/proposal.md. La lecture de proposal absent a été suivie de sa création autorisée ; aucun effet inconnu.

Compactages natifs dans cet intervalle : 0. API de compactage Codex non exposée, pas de réussite conjointe inventée.

Sondes valides : 2/2 (100.0 %), 0 échec. Initiale et finale réellement mesurées ; échéance périodique de 30 min non relevée séparément avant la finale proche de cette échéance, signalée sans reconstruction rétroactive.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début CommandIdempotencyV1 | 2026-10-12T11:55:07.452732+02:00 | 2.937 | 266.613 | 906 |
| fin après archive CommandIdempotencyV1 | 2026-10-12T12:25:41.531685+02:00 | 2.508 | 280.239 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT min/max 2.508/2.937 s ; débit min/max 266.613/280.239. Surcharge hors production : 1796 tokens sortie, coût natif 0.002855200.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 50 | 26.2 % |
| assistant | 141 | 73.8 % |
| Total | 191 | 100 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 151 | 22.5 % |
| step-start | 141 | 21.0 % |
| reasoning | 124 | 18.5 % |
| tool | 114 | 17.0 % |
| step-finish | 141 | 21.0 % |
| Total | 671 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 27 | 23.7 % | 27 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 20 | 17.5 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 12 | 10.5 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 4 | 3.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 31 | 27.2 % | 30 (96.8 %) | 0 (0.0 %) | 1 (3.2 %) |
| glob | 8 | 7.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 3 | 2.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 7.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 114 | 100 % | 113 (99.1 %) | 0 (0.0 %) | 1 (0.9 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 94 | 66.7 % |
| stop | 47 | 33.3 % |
| Total | 141 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 1047992 | 4.7 % |
| output | 43159 | 0.2 % |
| reasoning | 10232 | 0.0 % |
| cache_read | 21424648 | 95.1 % |
| cache_write | 0 | 0.0 % |
| Total | 22526031 | 100 % |

Coût natif cumulé 0.158326696 ; unité/devise non exposée par l’API, aucune conversion.

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1/specs/interactions/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_command_idempotency_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_command_idempotency_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_command_idempotency_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Compteurs = tentatives write/edit, pas lignes de code. tasks.md écrit puis coché après preuves. Artefacts déplacés par archivage, chemins actuels ci-dessus. Métadonnée /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1/.openspec.yaml générée par CLI, hors compteur write. Rapport publié après les bornes sous mandat distinct, sans auto-comptage. Aucun ancien code/export/canon/cadrage modifié.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Prévol true | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 5 | 41.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 25.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 3 | 25.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 | 100 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucune commande refusée : 0 (0.0 %). Commandes complètes et requestId conservés dans historique natif/checkpoint ; libellés ci-dessus inférieurs à 100 caractères.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Inférence LLM, quotas fournisseurs et API locales autorisés hors de ce domaine. Aucun service métier externe ni déploiement.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-12T11:51:42.990000+02:00 |
| Fin — après archivage | 2026-10-12T12:25:48.224135+02:00 |
| Durée globale, pauses/attentes incluses | 00 h 34 min 05 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T11:55:07.452732+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T12:25:48.224172+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : codex/window10080/usedPercent/resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 94 | 82.5 % | 93 (98.9 %) | 0 (0.0 %) | 1 (1.1 %) |
| commandes | 12 | 10.5 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 7.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 114 | 100 % | 113 (99.1 %) | 0 (0.0 %) | 1 (0.9 %) |

Totaux par type/domaine vérifiés : 114 appels, 113 succès, 0 refus, 1 erreur. Pourcentages à une décimale, écarts d’arrondi possibles.

Résultat : 178 tests, 3 compilations, strict change0 ; global1 qualifié par 3 WARNING historiques. Pure mémoire12valeurs seulement ; ni persistance/transaction/ownerbytes/provenance/catalogue/horloge/purge/retry/CAS. Aucun test PostgreSQL réel nécessaire à ce périmètre ; pas de frontend/navigateur concerné. Git non inspecté, aucun commit/push, aucun déploiement. Secrets confinés aux processus autorisés et authnative, aucune valeur dans modèle/rapport/sources. Le parent CISMP reprend la sélection après preuve de ce rapport, pas de TERMINÉ global.
