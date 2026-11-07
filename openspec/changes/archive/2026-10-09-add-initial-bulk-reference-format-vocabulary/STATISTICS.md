# Statistiques — add-initial-bulk-reference-format-vocabulary

RUN cismp-pixs-069bf76fca7c4fa0. Sessions : ses_ee1a28732ffedx0eHVwrsBwH10. Intervalle arrêté avant rédaction ; publication du présent rapport exclue des totaux. Périmètre propre à ce change, filtré depuis sa sélection. Les travaux du change précédent et les préconditions communes du RUN ne sont pas répartis artificiellement.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A | OpenCode Go | xhigh | 3.7 s | 109.3 | N/A |

Version exacte du modèle et durées actives de génération non exposées. Version OpenCode observée : 1.18.35. Moyennes sur les seules sondes valides.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 (contexte système) | N/A | OpenAI | N/A, non exposé | N/A | N/A | N/A |

Temps de service et dénominateur indisponibles : pauses, outils et chevauchements calendaires ne sont pas assimilés à la génération.

## 1. Statistiques générales et décisions

Durée calendaire 01 h 05 min 44 s, préconditions, pauses et attentes incluses. Résultat : Enum BulkReferenceFormat CSV/NDJSON, BulkCommitMode et BulkOperationVariant préservés, compilation et import codes 0, 20 tests OK, change strict code 0, archive code 0 sans mise à jour du canon. Canon global : exit natif 1, 21 warnings de longueur, zéro ERROR ; résultat qualifié par le critère développeur excluant la longueur, jamais présenté comme réussite native globale.

| Statut des mandats | Nombre | Part |
|---|---:|---:|
| EXECUTED | 15 | 100.0 % |
| Total | 15 | 100 % |

Convention : un outil terminé compte comme exécuté, sans présumer une approbation manuelle ; éditions et commandes autorisées sont corrélées aux décisions CAB et permissions once. Les propositions refusées sont distinctes des erreurs techniques MCP. Aucun compactage dans cet intervalle. L’API native de compactage Codex est absente.

| Tokens de production natifs | Nombre | Part |
|---|---:|---:|
| input | 552 | 0.0 % |
| output | 27348 | 0.4 % |
| reasoning | 0 | 0.0 % |
| cache_read | 7002860 | 90.1 % |
| cache_write | 738363 | 9.5 % |
| Total | 7769123 | 100 % |

Coût natif cumulé déclaré : 0.272655, unité/devise non explicitée dans la télémétrie ; aucune conversion. Sondes exclues.

| Sonde | Résultat | TTMT | Tokens/s | Tokens sortie |
|---|---|---:|---:|---:|
| début | Sortie fixe non conforme | 1.5 | 44.3 | 430 |
| périodique | OK | 5.0 | 113.9 | 1132 |
| fin | OK | 2.4 | 104.6 | 1133 |

Sondes : 3 tentatives, 2 valides (66.7 %), 1 non conformes (33.3 %). Début, périodique et fin identifiés ci-dessus. La sonde +30 min a été tardive (créneau prévu 04:50:52+02:00, envoi 05:19:38+02:00) ; le créneau +60 min n’a pas eu de sonde distincte avant la fin de codage à 05:23:23+02:00. Ces écarts de collecte ne sont pas masqués et les mesures ne sont pas reconstruites. Moyennes valides : TTMT 3.7 s, débit 109.3 ; sorties non conformes exclues. Surcharge connue : 2695 tokens de sortie, coût 0.005679 (unité non exposée).

Minimum/maximum des sondes valides : TTMT 2.4/5.0 s ; débit 104.6/113.9 tokens/s.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 47 | 33.8 % |
| assistant | 92 | 66.2 % |
| Total | 139 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 109 | 25.3 % |
| step-start | 92 | 21.4 % |
| reasoning | 92 | 21.4 % |
| step-finish | 92 | 21.4 % |
| tool | 45 | 10.5 % |
| Total | 430 | 100 % |

| Terminaison native | Nombre | Part |
|---|---:|---:|
| stop | 47 | 51.1 % |
| tool-calls | 45 | 48.9 % |
| Total | 92 | 100 % |

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| cgpt-validation_request_validation | 15 | 33.3 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 15 | 33.3 % | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 4 | 8.9 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 9 | 20.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 2 | 4.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 45 | 100 % | 45 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-reference-format-vocabulary/proposal.md | 1 | 16.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-reference-format-vocabulary/design.md | 1 | 16.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-reference-format-vocabulary/tasks.md | 2 | 33.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-reference-format-vocabulary/specs/bulk-operations/spec.md | 1 | 16.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operations.py | 1 | 16.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 6 | 100 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Chiffres de tentatives, chemins absolus intégraux. Quatre artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-09-add-initial-bulk-reference-format-vocabulary. Canon et façade inchangés ; aucun test supplémentaire de comportement standard de Enum. STATISTIQUES.md est une publication distincte après cet intervalle.

## 4. Commandes

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| OpenSpec validation | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Import | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests | 4 | 44.4 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archive | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande native refusée | Nombre | Part des appels Bash | Statut |
|---|---:|---:|---|

Aucune commande refusée dans cet intervalle. Commandes exactes conservées dans l’historique et le checkpoint ; archivage exécuté une seule fois.

## 5. Accès web

Aucun webfetch/websearch dans la production : 0 accès, pourcentages N/A (dénominateur zéro), aucune URL visitée/refusée à publier. Communications fournisseur HTTPS et API locales autorisées pour pilotage et sondes.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-09T04:19:19.201728+02:00 |
| Fin — après archivage, avant rédaction | 2026-10-09T05:25:03.652771+02:00 |
| Durée globale (pauses et attentes incluses) | 01 h 05 min 44 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début | N/A | N/A | N/A |
| Après — après archivage | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : aucune valeur substituée ou consommation reconstruite. Quotas partagés par compte, aucune attribution exclusive de variation.

| Catégorie | Total | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| MCP CAB | 30 | 66.7 % | 30 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 6 | 13.3 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 9 | 20.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 45 | 100 % | 45 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

20 tests réussis, compilation et import codes 0, archive prouvée. Aucune demande divergente à effet de bord observée sur ce change ; libellé descriptif d’archivage tronqué, commande exacte préservée et explicitement approuvée. Aucun commit/push ni inspection Git. PostgreSQL non nécessaire à cette unité. Secrets fournisseur limités au processus sécurisé et authentification native privée, jamais dans prompts, sorties ou sources ; aucune lecture de fichier sensible par le codage observée. Arrêt du cycle parent explicitement demandé après publication de ce rapport ; aucun prochain change ne sera sélectionné. Le projet global n’est pas déclaré intégralement implémenté.

Les pourcentages sont arrondis indépendamment à une décimale : leur somme peut valoir 99,9 % ou 100,1 %. Les nombres entiers et la ligne totale sont la référence.
