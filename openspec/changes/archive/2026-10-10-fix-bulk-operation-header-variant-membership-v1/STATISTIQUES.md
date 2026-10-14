# Statistiques — correction appartenance Header

Change : fix-bulk-operation-header-variant-membership-v1. RUN parent : cismp-pixs-758862ec875d4708.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A — version LLM non exposée | OpenCode Go | xhigh | 1.407 s | 81.751 | N/A |

OpenCode 1.18.35. Sessions retenues : ses_ed9f4aaaeffeMWxaHArUs3MkhZ, ses_ed9cb10f8ffexesUzGo7FHmOBN.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 / Codex | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A | N/A | N/A |

Aucune sonde de l’orchestrateur. Le temps de génération et son dénominateur cumulé ne sont pas isolables des outils et attentes : temps de service et pourcentages N/A. La durée calendaire n’est pas assimilée à du temps de génération.

## 1. Statistiques générales et décisions

Intervalle : 2026-10-10T15:40:39.377000+02:00 → 2026-10-10T16:52:00.869512+02:00. Durée calendaire : 01 h 11 min 21 s, préconditions, pauses et attentes incluses. Historique complet des deux sessions ayant porté les écritures et validations. Sessions techniques antérieures, benchmarks PLLM et travail distinct Tools Codex exclus des compteurs ; sondes séparées de la production.

| Résultat du correctif | Nombre | Part |
|---|---:|---:|
| Tests réussis | 65 / 65 | 100 % |
| Compilations séparées réussies | 2 / 2 | 100 % |
| Validations OpenSpec strictes avant/après code | 2 / 2 | 100 % |
| Tâches prouvées et cochées | 7 / 7 | 100 % |
| Archive réussie | 1 / 1 | 100 % |

Archive : 2026-10-10-fix-bulk-operation-header-variant-membership-v1, specsUpdated=false. Delta identique au canon ; six fichiers métier/artéfacts attendus et 106 références préexistantes préservées.

| Décisions CAB uniques par requestId | Nombre | Part |
|---|---:|---:|
| APPROVED | 18 | 90,0 % |
| REJECTED | 2 | 10,0 % |
| Total | 20 | 100 % |

18 décisions APPROVED correspondent à 18 effets natifs observés : 11 commandes et 7 écritures. Deux refus CAB avant effet ; aucune permission native hors mandat consommée. Le délai MCP du cochage a été résolu sur le même approval_id sans nouvelle demande.

Incidents : summary prescrit altéré et refusé ; files omis, consultation inconnue et autorejeu interdit, puis interruption/refus et récupération en deux phases réussie ; délai MCP PENDING au cochage puis polling corrélé. Les trois erreurs techniques d’outils ne sont pas des échecs de tests ou de validations exécutées.

| Compteurs de tokens natifs OpenCode | Nombre | Part |
|---|---:|---:|
| cache lecture | 5154943 | 78,0 % |
| cache écriture | 1401839 | 21,2 % |
| entrée | 570 | 0,0 % |
| raisonnement exposé | 0 | 0,0 % |
| sortie | 49869 | 0,8 % |
| Total | 6607221 | 100 % |

Coût natif OpenCode cumulé : 0.386370818 (unité monétaire non exposée ; aucune conversion). Les compteurs des messages interrompus peuvent être incomplets. Tokens, coût et outils de l’orchestrateur : N/A, historique natif exhaustif non accessible. Aucun compactage natif observé dans cet intervalle.

### Sondes isolées

Collecte activée à 2026-10-10T16:09:23.459536+02:00, après les préconditions et avant le premier travail métier. Période technique antérieure non sondée. Prompt constant : « Écris uniquement les entiers de 0001 à 0064 inclus, un par ligne sur quatre chiffres. Aucun commentaire, aucun outil. ». Aucun outil appelé, aucune injection dans la session métier.

| Relève | Envoi (fuseau inclus) | Tokens de sortie | TTMT | Tokens/s | État |
|---|---|---:|---:|---:|---|
| début Header membres | 2026-10-10T16:09:23.491549+02:00 | 353 | 1.422 s | 82.175 | Valide |
| +30 min Header membres | 2026-10-10T16:39:29.737204+02:00 | 362 | 1.404 s | 80.136 | Valide |
| fin Header membres | 2026-10-10T16:50:15.996992+02:00 | 364 | 1.394 s | 82.941 | Valide |

Prévues : 3 ; réussies : 3 (100 %) ; échouées : 0 (0 %) ; manquées : 0 (0 %). Moyennes arithmétiques : TTMT 1.407 s, débit 81.751 tokens/s.
TTMT min/max : 1.394/1.422 s ; débit min/max : 80.136/82.941. Surcharge séparée : 1079 tokens de sortie et coût natif 0.006296830.
TTMT au premier delta de texte ; débit = tokens de sortie fournis par OpenCode / durée entre premier et dernier delta. Raisonnement non ventilé séparément. Instants monotones, dates natives et usages conservés dans le checkpoint. Benchmarks PLLM de protocole différent exclus des moyennes.

## 2. Types de messages et d’outils

Convention : « approuvés et exécutés » = appel terminé avec succès, autorisé automatiquement ou par CAB ; cela ne prouve pas une approbation manuelle. request_validation terminé REJECTED = refus. Une lecture get/poll réussie reste une lecture réussie même si elle rapporte un refus. État error/interrompu ou commande non zéro = erreur technique. Décisions métier comptées séparément par requestId.

| Rôle des messages | Nombre | Part |
|---|---:|---:|
| assistant | 96 | 72,7 % |
| user | 36 | 27,3 % |
| Total | 132 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 96 | 21,1 % |
| step-finish | 95 | 20,9 % |
| step-start | 96 | 21,1 % |
| text | 81 | 17,8 % |
| tool | 86 | 18,9 % |
| Total | 454 | 100 % |

| Terminaison des réponses | Nombre | Part |
|---|---:|---:|
| erreur/interruption | 1 | 1,0 % |
| stop | 35 | 36,5 % |
| tool-calls | 60 | 62,5 % |
| Total | 96 | 100 % |

| Outil | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| bash | 11 (12,8 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 9 (10,5 %) | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 5 (5,8 %) | 4 (80,0 %) | 0 (0,0 %) | 1 (20,0 %) |
| cgpt-validation_poll_approval | 3 (3,5 %) | 2 (66,7 %) | 0 (0,0 %) | 1 (33,3 %) |
| cgpt-validation_request_validation | 21 (24,4 %) | 19 (90,5 %) | 1 (4,8 %) | 1 (4,8 %) |
| edit | 3 (3,5 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| glob | 1 (1,2 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 1 (1,2 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 28 (32,6 %) | 28 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 4 (4,7 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total général | 86 (100 %) | 82 (95,3 %) | 1 (1,2 %) | 3 (3,5 %) |

## 3. Fichiers modifiés

Sept tentatives natives d’écriture, toutes approuvées et exécutées, sur six fichiers uniques. Chemins finaux ci-dessous : les quatre artefacts ont été écrits dans le change actif puis déplacés par l’archivage.

| Chemin absolu complet | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-fix-bulk-operation-header-variant-membership-v1/design.md | 1 (14,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-fix-bulk-operation-header-variant-membership-v1/proposal.md | 1 (14,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-fix-bulk-operation-header-variant-membership-v1/specs/bulk-operations/spec.md | 1 (14,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-fix-bulk-operation-header-variant-membership-v1/tasks.md | 2 (28,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_header.py | 1 (14,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_header.py | 1 (14,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total général | 7 (100 %) | 7 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Refus avant écriture native : 1 / 8 mandats d’édition (12,5 %), sur la proposition. Il ne constitue pas une édition native exécutée. Le présent rapport est publié après la borne finale et exclu des compteurs.

## 4. Commandes

Onze commandes natives, toutes approuvées et exécutées avec exit 0. Compilations et tests peuvent produire du bytecode régénérable.

| Famille de commandes | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Archivage OpenSpec | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Compilation Python | 2 (18,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Prévol CAB | 3 (27,3 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Reproduction Python bornée | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Tests unitaires/intégration | 2 (18,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Validation OpenSpec | 2 (18,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total général | 11 (100 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Toutes les commandes refusées avant exécution :

| Commande (100 caractères maximum) | Occurrences | Part des refus commande |
|---|---:|---:|
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate fix-bulk-operatio… | 1 | 100,0 % |

1 / 12 mandats de commande refusés (8,3 %) ; zéro exécution pour ce refus. Soumission malformée et autorejeu tracés dans les erreurs MCP. Commandes exactes et corrélation conservées dans le checkpoint et les historiques natifs.

## 5. Accès web

| Résultat des outils web | Nombre | Taux |
|---|---:|---:|
| Approuvés et exécutés | 0 | N/A — aucun appel |
| Refusés | 0 | N/A — aucun appel |
| Erreurs | 0 | N/A — aucun appel |
| Total | 0 | N/A — dénominateur nul |

Aucun webfetch/websearch : aucune URL approuvée, refusée ou visitée à lister. Transports locaux OpenCode/CAB et requêtes du fournisseur LLM distincts des outils web ; aucune visite déduite d’un lien présent dans une source.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — première session native retenue | 2026-10-10T15:40:39.377000+02:00 |
| Fin — après archivage et sonde finale | 2026-10-10T16:52:00.869512+02:00 |
| Durée globale (pauses et attentes incluses) | 01 h 11 min 21 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A — relevé initial absent | N/A | N/A |
| Après — après archivage | 2026-10-10T16:52:00.869498+02:00 (constat d’indisponibilité) | N/A | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

Outil natif get_usage_limits non exposé : aucun quota inventé ou repris d’une ancienne session. Les quotas sont partagés par compte ; une différence disponible ne serait pas attribuable exclusivement à ce travail sans preuve d’exclusivité.

| Domaine des appels d’outils | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| autres outils | 68 (79,1 %) | 64 (94,1 %) | 1 (1,5 %) | 3 (4,4 %) |
| commandes | 11 (12,8 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| fichiers | 7 (8,1 %) | 7 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| web | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total général | 86 (100 %) | 82 (95,3 %) | 1 (1,2 %) | 3 (3,5 %) |

Bilan distinct : 20 mandats uniques, 18 APPROVED (90,0 %) et 2 REJECTED (10,0 %). 18 effets natifs autorisés (100,0 %) : 7 écritures sur 6 fichiers et 11 commandes. 86 appels d’outils : 82 réussis, 1 refus et 3 erreurs techniques selon la section 2. Sommes par type et domaine croisées.

Livraison : garde canonique et cas forgé vérifiés par 65 tests, deux compilations et deux validations strictes ; sept tâches cochées ; archive sans synchronisation du canon. Aucun appel Git, commit ou push. PostgreSQL et navigateurs sans objet pour ce correctif structurel. Aucun secret transmis, affiché ou ajouté aux sources par les opérations observées. RUN parent CISMP ouvert pour la sélection suivante ; achèvement global de Pixs non démontré.

Limites : métriques de l’orchestrateur et version exacte du LLM N/A ; aucun temps de service estimé. Deux erreurs de collecte après la borne finale (limite de ligne du canal de contrôle, puis curseur de pagination) corrigées, pages ensuite lues avec le curseur natif. Aucune source ni archive modifiée par ces erreurs ; elles sont hors compteurs OpenCode.
