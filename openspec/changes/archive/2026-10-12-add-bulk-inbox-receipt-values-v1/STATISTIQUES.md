# STATISTIQUES — add-bulk-inbox-receipt-values-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-inbox-receipt-values-v1`. Session : `ses_ed005058affe3j6N5p51XwQrUO`. RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historique natif de la session jusqu’au relevé final après archivage ; sondes jetables et rédaction du rapport exclues. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 2.469 s | 250.715 | N/A |
| muse-spark-1.3-contributor, agent compaction | OpenCode 1.19.0 ; modèle N/A | opencode-go | N/A — non exposé par API summarize | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des sondes valides sur texte visible. Temps de service actif et dénominateur cumulé tous agents : N/A ; ne pas assimiler pauses, outils ou durée calendaire à de la génération. Chevauchements d’activité possibles.

## 1. Statistiques générales et décisions

181 messages ; 103 outils : 102 succès (99.0 %), 0 refus (0.0 %), 1 erreur (1.0 %). 14 décisions CAB uniques approved (100 %) et autant de permissions natives once corrélées ; aucun refus.

244 tests réussis sans ignoré, 3 fichiers compilés, strict change code0 sans issue. Global strict code1 limité aux 3 WARNING historiques exacts de longueur, non présenté comme validation globale verte. Archive unique --skip-specs, canon préservé.

Convention : succès d’un outil ne prouve pas une approbation manuelle ; lectures peuvent être autorisées automatiquement. Les opérations mutantes/commandes ont une décision CGPT explicite unique. Refus = permission rejetée ; erreur = échec technique sans refus.

Erreur native observée : read — File not found: /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-command-idempotency-values-v1/specs/events/spec.md. Ce chemin events était inexistant dans une archive interactions ; le delta B11 a été produit depuis le canon events réellement lu, recopié à l’identique et validé. Aucune écriture liée à la lecture erronée.

Compactages natifs dans cet intervalle : 1, cycle cismp-compact-31202191c12d à 14:21:21–14:21:36 Europe/Paris, résumé natif terminé et événement session.compacted corrélés. Corps API sans paramètre variant et métadonnée variant absente pour cet agent : aucune valeur high inventée ; le modèle/fournisseur restent imposés. API de compactage Codex non exposée, pas de réussite conjointe inventée.

Sondes valides : 2/2 (100.0 %), 0 échec. Initiale et finale réellement mesurées ; fin à 14:27:51 avant la première échéance périodique à 14:29:58, donc aucune relève intermédiaire due ni manquée.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début | 2026-10-12T13:59:50.168875+02:00 | 2.441 | 178.272 | 902 |
| fin | 2026-10-12T14:27:46.133845+02:00 | 2.496 | 323.159 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT min/max 2.441/2.496 s ; débit min/max 178.272/323.159. Surcharge hors production : 1792 tokens sortie, coût natif 0.002658200.

Quatre défauts des brouillons de tests ont été corrigés avant écriture/exécution : fixture de clé hostile, fuseau zéro singleton, portabilité frozen/slots et harness contournant les gardes avec probe hors racine. Ces brouillons n’ont produit aucun appel natif ni effet, et ne sont pas comptés comme refus ou erreurs d’outil. Le harness Outbox éprouvé a été repris et les 244 tests réels ont ensuite réussi.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 41 | 22.7 % |
| assistant | 140 | 77.3 % |
| Total | 181 | 100 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 180 | 25.3 % |
| step-start | 140 | 19.7 % |
| reasoning | 148 | 20.8 % |
| tool | 103 | 14.5 % |
| step-finish | 140 | 19.7 % |
| compaction | 1 | 0.1 % |
| Total | 712 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 23 | 22.3 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 7 | 6.8 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 7 | 6.8 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 33 | 32.0 % | 32 (97.0 %) | 0 (0.0 %) | 1 (3.0 %) |
| glob | 5 | 4.9 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 14 | 13.6 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 7.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 6 | 5.8 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 103 | 100 % | 102 (99.0 %) | 0 (0.0 %) | 1 (1.0 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 100 | 71.4 % |
| stop | 40 | 28.6 % |
| Total | 140 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 1072718 | 8.7 % |
| output | 39444 | 0.3 % |
| reasoning | 14024 | 0.1 % |
| cache_read | 11226466 | 90.9 % |
| cache_write | 0 | 0.0 % |
| Total | 12352652 | 100 % |

Coût natif cumulé 0.140418332 ; unité/devise non exposée par l’API, aucune conversion.

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-inbox-receipt-values-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-inbox-receipt-values-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-inbox-receipt-values-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-inbox-receipt-values-v1/specs/events/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_inbox_receipt_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_inbox_receipt_values.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_inbox_receipt_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

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
| Début | 2026-10-12T13:59:00.266487+02:00 |
| Fin — après archivage | 2026-10-12T14:27:52.728926+02:00 |
| Durée globale, pauses/attentes incluses | 00 h 28 min 52 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T13:59:00.307254+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T14:27:52.729018+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : codex/window10080/usedPercent/resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 89 | 86.4 % | 88 (98.9 %) | 0 (0.0 %) | 1 (1.1 %) |
| commandes | 6 | 5.8 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 7.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 103 | 100 % | 102 (99.0 %) | 0 (0.0 %) | 1 (1.0 %) |

Totaux par type/domaine vérifiés : 103 appels, 102 succès, 0 refus, 1 erreur. Pourcentages à une décimale, écarts d’arrondi possibles.

Résultat : 244 tests, 3 fichiers compilés, strict change0 ; global1 qualifié par 3 WARNING historiques. Validation et capture immuable pures des huit valeurs InboxReceiptV1 ; aucune persistance, déduplication, transaction, comparaison de versions ou fingerprint métier, horloge, catalogue, unicité ni preuve de consommation/commit. Aucun test PostgreSQL réel nécessaire à ce périmètre ; pas de frontend/navigateur concerné. Git non inspecté, aucun commit/push, aucun déploiement. Secrets confinés aux processus autorisés et authnative, aucune valeur dans modèle/rapport/sources. Le parent CISMP reprend la sélection après preuve de ce rapport, pas de TERMINÉ global.
