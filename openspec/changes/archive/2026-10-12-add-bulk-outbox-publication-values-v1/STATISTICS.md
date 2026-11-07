# STATISTIQUES — add-bulk-outbox-publication-values-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-outbox-publication-values-v1`. Session : `ses_ed01d77ffffeaYJGEGMlBqhaaH`. RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historique natif de la session jusqu’au relevé final après archivage ; sondes jetables et rédaction du rapport exclues. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 4.755 s | 333.696 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des sondes valides sur texte visible. Temps de service actif et dénominateur cumulé tous agents : N/A ; ne pas assimiler pauses, outils ou durée calendaire à de la génération. Chevauchements d’activité possibles.

## 1. Statistiques générales et décisions

150 messages ; 102 outils : 101 succès (99.0 %), 0 refus (0.0 %), 1 erreur (1.0 %). 16 décisions CAB uniques approved (100 %) et autant de permissions natives once corrélées ; aucun refus.

226 tests réussis sans ignoré, 3 fichiers compilés, strict change code0 sans issue. Global strict code1 limité aux 3 WARNING historiques exacts de longueur, non présenté comme validation globale verte. Archive unique --skip-specs, canon préservé.

Convention : succès d’un outil ne prouve pas une approbation manuelle ; lectures peuvent être autorisées automatiquement. Les opérations mutantes/commandes ont une décision CGPT explicite unique. Refus = permission rejetée ; erreur = échec technique sans refus.

Erreur native observée : read — File not found: /home/devops/datas/pixs/src/pixs/kernel/diagnostics.py

Did you mean one of these?
/home/devops/datas/pixs/src/pixs/kernel/diagnostics. Le chemin diagnostics.py inexistant a été corrigé par lecture du package diagnostics et de son __init__.py ; aucune écriture ni effet inconnu.

Compactages natifs dans cet intervalle : 0. API de compactage Codex non exposée, pas de réussite conjointe inventée.

Sondes valides : 2/2 (100.0 %), 0 échec. Initiale et finale réellement mesurées ; fin à 13:54:25 avant la première échéance périodique de 30 min à 14:03:50, donc aucune relève intermédiaire due ni manquée.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début | 2026-10-12T13:33:43.433922+02:00 | 4.489 | 331.95 | 910 |
| fin | 2026-10-12T13:54:17.542228+02:00 | 5.021 | 335.442 | 902 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT min/max 4.489/5.021 s ; débit min/max 331.950/335.442. Surcharge hors production : 1812 tokens sortie, coût natif 0.002796726.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 39 | 26.0 % |
| assistant | 111 | 74.0 % |
| Total | 150 | 100 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 122 | 22.4 % |
| step-start | 111 | 20.4 % |
| reasoning | 99 | 18.2 % |
| tool | 102 | 18.7 % |
| step-finish | 111 | 20.4 % |
| Total | 545 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 20 | 19.6 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 3 | 2.9 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 4 | 3.9 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 16 | 15.7 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 8 | 7.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 33 | 32.4 % | 32 (97.0 %) | 0 (0.0 %) | 1 (3.0 %) |
| glob | 9 | 8.8 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 1.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 7.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 102 | 100 % | 101 (99.0 %) | 0 (0.0 %) | 1 (1.0 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 72 | 64.9 % |
| stop | 39 | 35.1 % |
| Total | 111 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 568761 | 3.6 % |
| output | 40112 | 0.3 % |
| reasoning | 11864 | 0.1 % |
| cache_read | 15071487 | 96.0 % |
| cache_write | 0 | 0.0 % |
| Total | 15692224 | 100 % |

Coût natif cumulé 0.097414274 ; unité/devise non exposée par l’API, aucune conversion.

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-outbox-publication-values-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-outbox-publication-values-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-outbox-publication-values-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-outbox-publication-values-v1/specs/events/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_outbox_publication_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_outbox_publication_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_outbox_publication_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Compteurs = tentatives write/edit, pas lignes de code. tasks.md écrit puis coché après preuves. Artefacts déplacés par archivage, chemins actuels ci-dessus. Rapport publié après les bornes sous mandat distinct, sans auto-comptage. Aucun ancien code/export/canon/cadrage modifié par cet agent de codage. En parallèle, l’entretien explicitement demandé de huit prompts CISMP par un agent distinct reste hors de cet historique OpenCode et de ses compteurs.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Prévol true | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 4 | 50.0 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucune commande refusée : 0 (0.0 %). Commandes complètes et requestId conservés dans historique natif/checkpoint ; libellés ci-dessus inférieurs à 100 caractères.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Inférence LLM, quotas fournisseurs et API locales autorisés hors de ce domaine. Aucun service métier externe ni déploiement.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-12T13:32:18.190329+02:00 |
| Fin — après archivage | 2026-10-12T13:54:26.333615+02:00 |
| Durée globale, pauses/attentes incluses | 00 h 22 min 08 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T13:33:43.433922+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T13:54:26.333678+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : codex/window10080/usedPercent/resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 86 | 84.3 % | 85 (98.8 %) | 0 (0.0 %) | 1 (1.2 %) |
| commandes | 8 | 7.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 7.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 102 | 100 % | 101 (99.0 %) | 0 (0.0 %) | 1 (1.0 %) |

Totaux par type/domaine vérifiés : 102 appels, 101 succès, 0 refus, 1 erreur. Pourcentages à une décimale, écarts d’arrondi possibles.

Résultat : 226 tests, 3 fichiers compilés, strict change0 ; global1 qualifié par 3 WARNING historiques. Validation et capture immuable pures des douze valeurs OutboxPublicationV1, avec seuls couplages fermés du bail et des horodatages requis ; aucune FK, unicité, allocation de séquence, persistance, transaction, publication, politique serveur, bail actif, horloge ou CAS. Aucun test PostgreSQL réel nécessaire à ce périmètre ; pas de frontend/navigateur concerné. Git non inspecté, aucun commit/push, aucun déploiement. Secrets confinés aux processus autorisés et authnative, aucune valeur dans modèle/rapport/sources. Le parent CISMP reprend la sélection après preuve de ce rapport, pas de TERMINÉ global.
