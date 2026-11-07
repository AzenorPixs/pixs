# Statistiques — add-initial-bulk-job-phase-vocabulary-v1

RUN cismp1-pixs-e286f24200f04ceb ; contexte CAB 302 ; projet /home/devops/datas/pixs.

Bornes de collecte instrumentée : 2026-10-18T16:18:16+02:00 à 2026-10-18T16:35:48+02:00, après archive et sonde finale, avant rédaction du présent rapport. Les lectures préparatoires antérieures au checkpoint ne sont pas chronométrées : durée totale incluant cette préparation = N/A. Le tableau de durée couvre exactement cet intervalle suivi.

Sources : historique natif complet des sessions de sélection ses_eb09e8d9cffebEST1CiRXnxwLJ et de change ses_eb09c2cefffeOZtT08PE24ZR8a ; GET /runs/cismp1-pixs-e286f24200f04ceb/statistics JSON et brouillon Markdown consultés ; relevés natifs Codex avant/après ; sondes dédiées. Les agrégats CAB ne couvrent que la session réservée, les tableaux natifs ci-dessous couvrent aussi la sélection. Les sondes restent une surcharge distincte. Les actions de rédaction, vérification et clôture postérieures aux bornes sont exclues des totaux figés.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go / opencode-go | high | 2.386 s | 549.674 — sortie seule | N/A — temps de génération non isolé |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | N/A — identifiant exact non exposé | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — non mesurable |

Les durées natives de réponse peuvent inclure transport et transitions ; elles ne sont pas assimilées au temps de service du modèle. Aucun dénominateur de service cumulé fiable : parts N/A, chevauchements non quantifiés.

## 1. Statistiques générales et décisions

| Mesure | Valeur |
| --- | --- |
| Durée calendaire instrumentée, pauses et attentes incluses | 00 h 17 min 32 s |
| Messages natifs de production/sélection | 136 |
| Appels outils natifs | 152 |
| Terminés avec succès natif | 149 (98.0 %) |
| Refus de permission | 0 (0.0 %) |
| Erreurs techniques | 3 (2.0 %) |
| En cours à la borne finale | 0 (0.0 %) |
| Compactions | 0 observée ; seuil 1 h 30 non atteint |
| Tokens total déclaré OpenCode | 16176620 |
| Tokens entrée hors cache | 579929 |
| Tokens sortie | 35915 |
| Tokens raisonnement | 17677 |
| Cache lu | 15543099 |
| Cache écrit | 0 |
| Coût déclaré OpenCode | 0.09979750 USD ; ne prouve pas la facture fournisseur |

Convention : un outil completed compte comme approuvé et exécuté, automatiquement ou manuellement ; il ne prouve pas une approbation CAB manuelle. Une commande autorisée à code 1 reste exécutée : son résultat fonctionnel est détaillé séparément. Refus = refus de permission explicite uniquement.

| Décision CAB du change | Nombre | Part |
| --- | --- | --- |
| approved | 16 | 100.0 % |
| rejected | 0 | 0.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 16 | 100 % |

Permissions natives once : 16. Une demande à révision inconnue a été annulée sans écriture ni décision, puis remplacée par des identifiants neufs ; elle reste distincte des refus. Erreurs techniques natives : délai MCP sur cette demande, un read de fichier absent et un glob invalide. Tentatives HTTP CAB observées séparément : {"resource-revision-stale": 4, "decision-run-divergent": 1} ; ne pas les additionner aux appels natifs.

Résultat du développement : trois nouveaux fichiers Python, trois compilations code 0, 32/32 tests OK dont trois nouveaux, validation ciblée stricte code 0. Global standard 186/186 code 0 ; global strict avant archive 184/186 code 1 et après archive 183/185 code 1 : les quatre WARNING historiques de longueur dans bulk-operations (6/10/13) et identity-assurance (4), zéro ERROR. Aucun canon corrigé hors périmètre.

| Sonde dédiée | TTMT | Débit sortie | Tokens sortie | Statut |
| --- | --- | --- | --- | --- |
| début | 3.003 s | 565.147 tokens/s | 347 | réussie |
| fin | 1.769 s | 534.202 tokens/s | 328 | réussie |

Protocole identique : nombres 1 à 160, un par ligne, aucun outil ni accès fichier/réseau par la sonde, même Muse high. Horodatages natifs début/fin de partie texte : mesure de premier événement de sortie, pas de capture monotone SSE du premier delta. Deux relèves prévues, deux réussies (100 %), zéro échouée/manquée (0 %), intervalle inférieur à 30 min. TTMT min/max 1.769/3.003 s ; débit min/max 534.202/565.147 tokens/s. Surcharge sondes : 26158 tokens déclarés, 675 tokens sortie, 6.008 s de durée native de réponse ; coût séparé N/A, non réparti.

PLLM réel courant, distinct des sondes : mode 1, Muse high, quotas utilisés 5 h 1 %, semaine 66 %, mois 98 % ; TTFT 3.9386 s, débit global raisonnement et réponse 1764.205 tokens/s, palier 1024, état Valide. Mesures fournisseur temporelles ; elles ne sont pas des performances du travail métier.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 28 | 20.6 % |
| assistant | 108 | 79.4 % |
| Total | 136 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 97 | 16.9 % |
| step-start | 108 | 18.8 % |
| reasoning | 110 | 19.1 % |
| tool | 152 | 26.4 % |
| step-finish | 108 | 18.8 % |
| Total | 575 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 84 | 77.8 % |
| stop | 24 | 22.2 % |
| Total | 108 | 100 % |

| Outil | Total | Part globale | Approuvé/exécuté | Refus | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 4 | 2.6 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 74 | 48.7 % | 73 (98.6 %) | 0 (0.0 %) | 1 (1.4 %) |
| glob | 12 | 7.9 % | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |
| grep | 25 | 16.4 % | 25 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 17 | 11.2 % | 16 (94.1 %) | 0 (0.0 %) | 1 (5.9 %) |
| bash | 8 | 5.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 3 | 2.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 5.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 | 0.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 152 | 100 % | 149 (98.0 %) | 0 (0.0 %) | 3 (2.0 %) |

## 3. Fichiers modifiés

| Chemin absolu au moment de l’écriture | Tentatives | Part | Approuvées/exécutées | Refusées | En erreur |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-phase-vocabulary-v1/.openspec.yaml | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-phase-vocabulary-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-phase-vocabulary-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-phase-vocabulary-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_job_phase.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_job_phase.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_job_phase_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Ce sont les tentatives natives, huit écritures sur sept fichiers uniques ; la demande annulée n’a déclenché aucune tentative d’écriture. Les quatre artefacts ont été déplacés par l’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-job-phase-vocabulary-v1/. Aucun fichier préexistant modifié hors tâches propres au change ; onze empreintes de cadrages/canons/sources préservées. La création du présent /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-job-phase-vocabulary-v1/STATISTIQUES.md relève d’un mandat distinct postérieur aux totaux ci-dessus.

## 4. Commandes

| Commande exacte tronquée à 100 caractères | Occurrences | Part | Exécutées | Refus | Erreur outil |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_job_phase.py tests/u... | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m... | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-job-phase-vocabulary-v1 --strict | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-job-phase-vocabulary-v1 --yes | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Famille | Nombre | Part |
| --- | --- | --- |
| Prévol inoffensif | 1 | 12.5 % |
| Compilation | 1 | 12.5 % |
| Tests ciblés/régressions | 1 | 12.5 % |
| Validation OpenSpec | 4 | 50.0 % |
| Archivage OpenSpec | 1 | 12.5 % |
| Total | 8 | 100 % |

Codes de sortie : six à 0 (75.0 %), deux à 1 (25.0 %), ces derniers sont les contrôles globaux stricts aux warnings historiques documentés. Commandes refusées : aucune, 0 occurrence ; part N/A sur ensemble refusé vide. Aucun commit, push ni inspection Git.

## 5. Accès web

| Accès par outil web de l’agent de codage | Nombre | Part |
| --- | --- | --- |
| Approuvés/exécutés | 0 | N/A — dénominateur nul |
| Refusés | 0 | N/A — dénominateur nul |
| Erreurs | 0 | N/A — dénominateur nul |
| Total | 0 | N/A — aucun appel |

Aucune URL visitée par un outil web natif, aucune URL refusée. Les appels fournisseur autorisés du prévol PLLM sont distincts : https://opencode.ai/zen/go/v1/usage (quota), https://opencode.ai/zen/go/v1/responses (benchmark, une requête). Les requêtes de génération OpenCode au fournisseur et les API d’administration locales ne sont pas comptées comme visites web ; leur total réseau exhaustif est N/A. Aucun accès de la sonde à un outil réseau.

## 6. Synthèse globale

| Durée de la session de codage instrumentée | Valeur |
| --- | --- |
| Début | 2026-10-18T16:18:16+02:00 |
| Fin — après archivage | 2026-10-18T16:35:48+02:00 |
| Durée globale instrumentée (pauses et attentes incluses) | 00 h 17 min 32 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-18T16:18:16+02:00 | 11 % | 2026-10-25T01:23:28+02:00 |
| Après — après archivage de la spécification | 2026-10-18T16:35:48+02:00 | 13 % | 2026-10-25T01:23:28+02:00 |
| Différence après − avant | — | 2 points de pourcentage | — |

Source réelle : mcp__codex_app__get_usage_limits, rateLimitsByLimitId.codex, fenêtre 10080 minutes ; même compte et même réinitialisation vérifiés. Les quotas sont partagés : cette variation peut inclure des tâches simultanées et ne constitue pas une attribution exclusive au RUN.

| Domaine | Total | Part globale | Approuvé/exécuté | Refus | Erreur |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 8 | 5.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 8 | 5.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 136 | 89.5 % | 133 (97.8 %) | 0 (0.0 %) | 3 (2.2 %) |
| Global | 152 | 100 % | 149 (98.0 %) | 0 (0.0 %) | 3 (2.0 %) |

CAB 1.3.0 resource-scoped-v1, contexte 302 : attente de ressource 0.000 s ; détention partagée 158.251 s ; effets natifs suivis 3.760 s ; réconciliations ciblées 0. Ces durées peuvent se recouvrir et ne prouvent pas un temps de codage productif. Aucun gel global de ce RUN.

Archive unique confirmée, publication CAB publish-c25b1e9c26bc4c84, référence 37. Les 32 tests et compilations ont réussi ; le strict global conserve son code 1 et ses quatre avertissements préexistants. Le présent rapport doit encore être relu (six sections, UTF-8/LF, totaux), puis gate individuel, désarmement et libération seront vérifiés avant l’arrêt ciblé. Aucun prochain change autorisé dans ce RUN ; cycle_global_complete=false. Git non inspecté ni modifié, provenance Git N/A. Aucun secret lu par le modèle ou inclus dans les sources ; l’accès PLLM s’est limité au processus sécurisé autorisé. PostgreSQL réel et frontend non applicables au vocabulaire passif.
