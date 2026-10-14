# STATISTIQUES — add-bulk-event-envelope-validation-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-event-envelope-validation-v1`. Sessions : `ses_ed05082e6ffeGv2fYhKUIl8vPC`, `ses_ed049c549ffe3zKAsvOpmdIOV1`. RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historique natif de la session jusqu’au relevé final après archivage ; sondes jetables et rédaction du rapport exclues. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 5.661 s | 293.761 | N/A |

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor — compactage | OpenCode 1.19.0 ; modèle N/A | opencode-go | N/A non exposé | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des sondes valides sur texte visible. Temps de service actif et dénominateur cumulé tous agents : N/A ; ne pas assimiler pauses, outils ou durée calendaire à de la génération. Chevauchements d’activité possibles.

MessageAbortedError natif : 1 lors de l’interruption contrôlée, hors décompte des erreurs d’outils. Les erreurs -32602 de schéma MCP ne sont pas des refus de permission malgré le mot REJECTED dans la liste des valeurs permises.

## 1. Statistiques générales et décisions

235 messages ; 150 outils : 147 succès (98.0 %), 0 refus (0.0 %), 3 erreur (2.0 %). 21 décisions CAB uniques approved (100 %) et autant de permissions natives once corrélées ; aucun rejet de décision CAB. Une permission native todowrite hors mandat a été explicitement refusée avant effet.

200 tests réussis sans ignoré, 3 compilations, strict change code0 sans issue. Global strict code1 limité aux 3 WARNING historiques exacts de longueur, non présenté comme validation globale verte. Archive unique --skip-specs, canon préservé.

Convention : succès d’un outil ne prouve pas une approbation manuelle ; lectures peuvent être autorisées automatiquement. Les opérations mutantes/commandes ont une décision CGPT explicite unique. Refus = permission rejetée ; erreur = échec technique sans refus.

Erreur native observée : cgpt-validation_list_pending — MCP error -32602: status inconnu, attendu parmi PENDING,APPROVED,REJECTED,NEEDS_CLARIFICATION,CANCELLED,EXPIRED ; todowrite — Tool execution aborted ; read — File not found: /home/devops/datas/pixs/openspec/changes/add-bulk-event-envelope-validation-v1/proposal.md. Erreur MCP de paramètre -32602 corrigée sans effet ; todowrite interrompu/refusé avant exécution, todo vide et sources inchangées ; lecture proposal absent suivie de création. Récupération contrôlée prepare/complete vers nouvelle session, prévol réservé distinct, strictCommands conservé. Aucun effet inconnu.

Compactages natifs dans cet intervalle : 1. API de compactage Codex non exposée, pas de réussite conjointe inventée.

Sondes valides : 3/3 (100.0 %), 0 échec. Initiale, périodique et finale réellement mesurées ; relève périodique retardée de 46.9 secondes, datée à son heure réelle, aucune reconstruction rétroactive.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début validation EventEnvelopeV1 | 2026-10-12T12:39:22.422631+02:00 | 11.252 | 266.85 | 952 |
| périodique — heure réelle | 2026-10-12T13:10:24.385847+02:00 | 3.888 | 281.557 | 919 |
| fin après archive validation EventEnvelopeV1 | 2026-10-12T13:22:27.542207+02:00 | 1.844 | 332.877 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT min/max 1.844/11.252 s ; débit min/max 266.850/332.877. Surcharge hors production : 2761 tokens sortie, coût natif 0.004363700.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 63 | 26.8 % |
| assistant | 172 | 73.2 % |
| Total | 235 | 100 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 185 | 21.6 % |
| step-start | 172 | 20.1 % |
| reasoning | 177 | 20.7 % |
| tool | 150 | 17.5 % |
| step-finish | 171 | 20.0 % |
| compaction | 1 | 0.1 % |
| Total | 856 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 33 | 22.0 % | 33 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 8 | 5.3 % | 7 (87.5 %) | 0 (0.0 %) | 1 (12.5 %) |
| cgpt-validation_request_validation | 21 | 14.0 % | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 13 | 8.7 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 1 | 0.7 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| read | 44 | 29.3 % | 43 (97.7 %) | 0 (0.0 %) | 1 (2.3 %) |
| glob | 9 | 6.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 6 | 4.0 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 7 | 4.7 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 5.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 150 | 100 % | 147 (98.0 %) | 0 (0.0 %) | 3 (2.0 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 113 | 65.7 % |
| stop | 58 | 33.7 % |
| N/A | 1 | 0.6 % |
| Total | 172 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 1553766 | 6.6 % |
| output | 50365 | 0.2 % |
| reasoning | 17768 | 0.1 % |
| cache_read | 21857726 | 93.1 % |
| cache_write | 0 | 0.0 % |
| Total | 23479625 | 100 % |

Coût natif cumulé 0.212718652 ; unité/devise non exposée par l’API, aucune conversion.

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-event-envelope-validation-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-event-envelope-validation-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-event-envelope-validation-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-event-envelope-validation-v1/specs/events/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_event_envelope_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_event_envelope_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_event_envelope_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Compteurs = tentatives write/edit, pas lignes de code. tasks.md écrit puis coché après preuves. Artefacts déplacés par archivage, chemins actuels ci-dessus. Métadonnée /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-event-envelope-validation-v1/.openspec.yaml générée par CLI, hors compteur write. Rapport publié après les bornes sous mandat distinct, sans auto-comptage. Aucun ancien code/export/canon/cadrage modifié.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Prévol true | 2 | 15.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 5 | 38.5 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 23.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 3 | 23.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 | 100 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucune commande refusée : 0 (0.0 %). Commandes complètes et requestId conservés dans historique natif/checkpoint ; libellés ci-dessus inférieurs à 100 caractères.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Inférence LLM, quotas fournisseurs et API locales autorisés hors de ce domaine. Aucun service métier externe ni déploiement.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-12T12:36:32.409000+02:00 |
| Fin — après archivage | 2026-10-12T13:22:33.183321+02:00 |
| Durée globale, pauses/attentes incluses | 00 h 46 min 00 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T12:39:22.422631+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T13:22:33.183373+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : codex/window10080/usedPercent/resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 129 | 86.0 % | 126 (97.7 %) | 0 (0.0 %) | 3 (2.3 %) |
| commandes | 13 | 8.7 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 5.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 150 | 100 % | 147 (98.0 %) | 0 (0.0 %) | 3 (2.0 %) |

Totaux par type/domaine vérifiés : 150 appels, 147 succès, 0 refus, 3 erreur. Pourcentages à une décimale, écarts d’arrondi possibles.

Résultat : 200 tests, 3 compilations, strict change0 ; global1 qualifié par 3 WARNING historiques. Validation structurelle 13 valeurs et payload JSON borné uniquement ; aucun snapshot, enveloppe créée, schéma propriétaire, catalogue, preuve de minimisation/absence de secret, persistance, publication, horloge ou autorité. Aucun test PostgreSQL réel nécessaire à ce périmètre ; pas de frontend/navigateur concerné. Git non inspecté, aucun commit/push, aucun déploiement. Secrets confinés aux processus autorisés et authnative, aucune valeur dans modèle/rapport/sources. Le parent CISMP reprend la sélection après preuve de ce rapport, pas de TERMINÉ global.
