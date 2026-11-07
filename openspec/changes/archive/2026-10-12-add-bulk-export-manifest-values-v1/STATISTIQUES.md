# STATISTIQUES — add-bulk-export-manifest-values-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-export-manifest-values-v1`. Sessions : `ses_ecfe118e9ffeGG2fOd8hNeQTrc` (préparation interrompue sans effet) puis `ses_ecfd57213ffeQeDoTO3M1HmP67` (récupération et production). RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historiques natifs des deux sessions corrélées jusqu’au relevé final après archivage ; sondes jetables et rédaction du rapport exclues. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 3.242 s | 342.226 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des sondes valides sur texte visible. Temps de service actif et dénominateur cumulé tous agents : N/A ; ne pas assimiler pauses, outils ou durée calendaire à de la génération. Chevauchements d’activité possibles.

## 1. Statistiques générales et décisions

203 messages ; 104 outils : 104 succès (100.0 %), 0 refus (0.0 %), 0 erreur (0.0 %). 15 décisions CAB uniques approved (100 %) et autant de permissions natives once corrélées ; aucun refus.

266 tests réussis sans ignoré, 3 fichiers compilés, strict change code0 sans issue. Global strict code1 limité aux 3 WARNING historiques exacts de longueur, non présenté comme validation globale verte. Archive unique --skip-specs, canon préservé.

Convention : succès d’un outil ne prouve pas une approbation manuelle ; lectures peuvent être autorisées automatiquement. Les opérations mutantes/commandes ont une décision CGPT explicite unique. Refus = permission rejetée ; erreur = échec technique sans refus.

Erreur native d’outil observée : aucune. Les brouillons initiaux ont été rejetés avant toute écriture : absence de relecture, delta B12 réécrit, contrats de retour divergents et formulation de probe hors racine. Le registre API déclarait read, mais aucun appel read n’était observé dans l’ancienne session et l’agent déclarait l’outil absent. Cause interne non établie. La récupération contrôlée recover-be00a6bb5e074fd5ae71ddc2e9a14ccd, sans purge/redémarrage ni changement de modèle, a révoqué l’ancienne session, conservé job/change/critères et prouvé un prévol unique /usr/bin/true exit0 avec once/READY0. Les lectures réelles ont ensuite repris dans la candidate, sans overrides tools. Les artefacts conformes ont été relus et approuvés avant écriture. Ces difficultés de préparation ne sont ni des refus natifs ni des erreurs d’outil.

Compactages natifs dans cet intervalle : 0. API de compactage Codex non exposée, pas de réussite conjointe inventée.

Sondes valides : 3/3 (100.0 %), 0 échec. Initiale, relève périodique de +30 min et finale réellement mesurées. Relève prévue 15:09:06, envoyée 15:09:24 : retard réel 17,6 s conservé ; aucune relève manquée ni reconstruite. La suivante à 15:39:06 est postérieure à la fin de l’intervalle.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début | 2026-10-12T14:39:00.535387+02:00 | 3.011 | 367.583 | 911 |
| périodique — heure réelle | 2026-10-12T15:09:24.328783+02:00 | 3.838 | 336.515 | 913 |
| fin | 2026-10-12T15:18:47.830474+02:00 | 2.878 | 322.581 | 902 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT min/max 2.878/3.838 s ; débit min/max 322.581/367.583. Surcharge hors production : 2726 tokens sortie, coût natif 0.003017256.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 52 | 25.6 % |
| assistant | 151 | 74.4 % |
| Total | 203 | 100 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 166 | 22.7 % |
| step-start | 151 | 20.7 % |
| reasoning | 159 | 21.8 % |
| tool | 104 | 14.2 % |
| step-finish | 151 | 20.7 % |
| Total | 731 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 31 | 29.8 % | 31 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 7 | 6.7 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 10 | 9.6 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 1.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 15 | 14.4 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 7 | 6.7 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 24 | 23.1 % | 24 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 1.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 7.7 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 104 | 100 % | 104 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 104 | 68.9 % |
| stop | 47 | 31.1 % |
| Total | 151 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 568438 | 4.0 % |
| output | 43274 | 0.3 % |
| reasoning | 18614 | 0.1 % |
| cache_read | 13498911 | 95.5 % |
| cache_write | 0 | 0.0 % |
| Total | 14129237 | 100 % |

Coût natif cumulé 0.096219222 ; unité/devise non exposée par l’API, aucune conversion.

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-export-manifest-values-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-export-manifest-values-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-export-manifest-values-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-export-manifest-values-v1/specs/bulk-operations/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_export_manifest_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_export_manifest_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_export_manifest_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Compteurs = tentatives write/edit, pas lignes de code. tasks.md écrit puis coché après preuves. Artefacts déplacés par archivage, chemins actuels ci-dessus. Rapport publié après les bornes sous mandat distinct, sans auto-comptage. Aucun ancien code/export/canon/cadrage modifié.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Prévol true | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 4 | 57.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 1 | 14.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 7 | 100 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucune commande refusée : 0 (0.0 %). Commandes complètes et requestId conservés dans historique natif/checkpoint ; libellés ci-dessus inférieurs à 100 caractères.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Inférence LLM, quotas fournisseurs et API locales autorisés hors de ce domaine. Aucun service métier externe ni déploiement.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-12T14:38:15.705546+02:00 |
| Fin — après archivage | 2026-10-12T15:18:54.520511+02:00 |
| Durée globale, pauses/attentes incluses | 00 h 40 min 38 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T14:38:15.744945+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T15:18:54.520616+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : codex/window10080/usedPercent/resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 89 | 85.6 % | 89 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commandes | 7 | 6.7 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 7.7 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 104 | 100 % | 104 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Totaux par type/domaine vérifiés : 104 appels, 104 succès, 0 refus, 0 erreur. Pourcentages à une décimale, écarts d’arrondi possibles.

Résultat : 266 tests, 3 fichiers compilés, strict change0 ; global1 qualifié par 3 WARNING historiques. Validation et capture immuable pures des dix-sept scalaires ExportManifestV1 ; aucune finalisation, objet privé, octet/hash recalculé, gouvernance, autorité, consistance résolue, horloge, stockage, export, URL ni transaction attestée. Aucun test PostgreSQL réel nécessaire à ce périmètre ; pas de frontend/navigateur concerné. Git non inspecté, aucun commit/push, aucun déploiement. Secrets confinés aux processus autorisés et authnative, aucune valeur dans modèle/rapport/sources. Le parent CISMP reprend la sélection après preuve de ce rapport, pas de TERMINÉ global.
