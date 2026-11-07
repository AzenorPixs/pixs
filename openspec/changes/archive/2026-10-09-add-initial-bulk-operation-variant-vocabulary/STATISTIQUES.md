# Statistiques — add-initial-bulk-operation-variant-vocabulary

RUN cismp-pixs-069bf76fca7c4fa0. Sessions : ses_ee1e76f10ffeEWzn80kxuTrUVS, ses_ee1a28732ffedx0eHVwrsBwH10. Intervalle arrêté avant rédaction ; publication du présent rapport exclue des totaux. Les quatre artefacts préparés au RUN précédent ne sont pas répartis artificiellement.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go | xhigh | 1.6 s | 87.4 | N/A |
| Qwen3.8 Flash, compactage | N/A | OpenCode Go | N/A, non exposé | N/A | N/A | N/A |

Version exacte du modèle et durées actives de génération non exposées. Version OpenCode observée : 1.18.35. Moyennes sur les seules sondes valides.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 (contexte système) | N/A | OpenAI | N/A, non exposé | N/A | N/A | N/A |

Temps de service et dénominateur indisponibles : pauses, outils et chevauchements calendaires ne sont pas assimilés à la génération.

## 1. Statistiques générales et décisions

Pourcentages arrondis individuellement à une décimale : leur somme affichée peut différer de 100 % de 0,1 point. Les totaux 100 % sont calculés sur les effectifs absolus ; aucun effectif n’est ajusté pour masquer un arrondi.

Durée calendaire 01 h 30 min 19 s, préconditions, pauses et attentes incluses. Résultat : Enum BulkOperationVariant IMPORT/EXPORT, compilation et import codes 0, 20 tests OK, change strict code 0, archive code 0 sans mise à jour du canon. Canon global : exit natif 1, 21 warnings de longueur, zéro ERROR ; résultat qualifié par le critère développeur excluant la longueur, jamais présenté comme réussite native globale.

| Statut des mandats | Nombre | Part |
|---|---:|---:|
| EXECUTED | 13 | 81.2 % |
| REJECTED | 2 | 12.5 % |
| NOT_SUBMITTED | 1 | 6.2 % |
| Total | 16 | 100 % |

Convention : un outil terminé compte comme exécuté, sans présumer une approbation manuelle ; éditions et commandes autorisées sont corrélées aux décisions CAB et permissions once. Les propositions refusées sont distinctes des erreurs techniques MCP. Un compactage OpenCode natif réussi ; compactage conjoint incomplet, API Codex absente.

| Tokens de production natifs | Nombre | Part |
|---|---:|---:|
| input | 660 | 0.0 % |
| output | 37894 | 0.9 % |
| reasoning | 0 | 0.0 % |
| cache_read | 3842075 | 88.5 % |
| cache_write | 459602 | 10.6 % |
| Total | 4340231 | 100 % |

Coût natif cumulé déclaré : 0.171303, unité/devise non explicitée dans la télémétrie ; aucune conversion. Sondes exclues.

| Sonde | Résultat | TTMT | Tokens/s | Tokens sortie |
|---|---|---:|---:|---:|
| début | TimeoutError: réponse native HTTP non obtenue en 180 s; session jetable supprimée | N/A | N/A | N/A |
| début_retry | Sortie fixe non conforme | 6.6 | 74.7 | 603 |
| périodique | Sortie fixe non conforme | 8.1 | 59.4 | 5888 |
| fin | OK | 1.6 | 87.4 | 2578 |

Trois relèves prévues (début, +30 min, fin), avec une retentative initiale conservée : 4 tentatives, 1 valide, 3 échouées, aucune relève manquée observée. Moyennes/minimum/maximum valides : TTMT 1.6 s, débit 87.4 ; une seule sonde valide, minimum et maximum identiques. Mesures invalides exclues sans les masquer ; premier horodatage et tokens absents N/A. Surcharge connue : 9069 tokens de sortie, coût 0.008675, première tentative non mesurable.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 48 | 30.4 % |
| assistant | 110 | 69.6 % |
| Total | 158 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 96 | 19.6 % |
| step-start | 110 | 22.4 % |
| reasoning | 110 | 22.4 % |
| tool | 64 | 13.0 % |
| step-finish | 110 | 22.4 % |
| compaction | 1 | 0.2 % |
| Total | 491 | 100 % |

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 6 | 9.4 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 16 | 25.0 % | 13 (81.2 %) | 0 (0.0 %) | 3 (18.8 %) |
| cgpt-validation_poll_approval | 13 | 20.3 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 12 | 18.8 % | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |
| read | 13 | 20.3 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 2 | 3.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 | 3.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 64 | 100 % | 60 (93.8 %) | 1 (1.6 %) | 3 (4.7 %) |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operations.py | 1 | 50.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-operation-variant-vocabulary/tasks.md | 1 | 50.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 2 | 100 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Chiffres de tentatives, chemins absolus intégraux. Quatre artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-09-add-initial-bulk-operation-variant-vocabulary. Canon et façade inchangés ; aucun test supplémentaire de comportement standard de Enum. STATISTIQUES.md est une publication distincte après cet intervalle.

## 4. Commandes

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| Prévol | 2 | 16.7 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Import | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests | 4 | 33.3 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validation | 2 | 16.7 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archive | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Autre | 1 | 8.3 % | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| Total | 12 | 100 % | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |

| Commande native refusée | Nombre | Part des appels Bash | Statut |
|---|---:|---:|---|
| ls openspec/changes/archive/2026-10-09-add-initial-bulk-operation-variant-vocabulary | 1 | 8.3 % | Refus avant exécution |

Deux propositions divergentes rejetées avant Bash : recompilation au lieu de l’import ; kernel_facades substitué à public_api_facades. Commandes exactes conservées dans historique et checkpoint. Aucune validation réussie ni archive rejouée.

## 5. Accès web

Aucun webfetch/websearch dans la production : 0 accès, pourcentages N/A (dénominateur zéro), aucune URL visitée/refusée à publier. Communications fournisseur HTTPS et API locales autorisées pour pilotage et sondes.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-09T02:30:46.458162+02:00 |
| Fin — après archivage, avant rédaction | 2026-10-09T04:01:06.336227+02:00 |
| Durée globale (pauses et attentes incluses) | 01 h 30 min 19 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début | N/A | N/A | N/A |
| Après — après archivage | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : aucune valeur substituée ou consommation reconstruite. Quotas partagés par compte, aucune attribution exclusive de variation.

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| MCP CAB | 37 | 57.8 % | 34 (91.9 %) | 0 (0.0 %) | 3 (8.1 %) |
| Commandes | 12 | 18.8 % | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |
| Lecture/recherche | 13 | 20.3 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 2 | 3.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 64 | 100 % | 60 (93.8 %) | 1 (1.6 %) | 3 (4.7 %) |

20 tests réussis, compilation et import codes 0, archive prouvée. Demandes divergentes et ls supplémentaire refusés sans effet ; archive conservée pendant récupération contrôlée. Aucun commit/push ni inspection Git. PostgreSQL non nécessaire à cette unité. Secrets fournisseur limités au processus sécurisé et authentification native privée, jamais dans prompts, sorties ou sources ; aucune lecture de fichier sensible par le codage observée. Le cycle parent reste en cours.
