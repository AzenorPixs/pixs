# Statistiques — BulkOperationFormat v1

Change : add-initial-bulk-operation-format-v1. RUN parent : cismp-pixs-758862ec875d4708.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Qwen3.8 Flash | N/A — version LLM non exposée | OpenCode Go | xhigh | N/A — six sondes invalides | N/A — six sondes invalides | N/A |

OpenCode 1.18.35. Sessions retenues : ses_ed8eb8adbffeNyHXg3lTAqRMx4, ses_ed8d7b766ffezgyrmNuuORg41q, ses_ed8d43969ffeFqgbu4SSopPljn, ses_ed8cfd185ffekOuGTnGfvivj81. Fournisseur, modèle, variante et racine confirmés dans les métadonnées natives.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| GPT-6 / Codex | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A | N/A | N/A |

Aucune sonde orchestrateur. Temps de service cumulé non isolable des outils et attentes : valeurs et pourcentages N/A. Durée calendaire et temps de service sont distincts.

## 1. Statistiques générales et décisions

Intervalle : 2026-10-10T20:30:14.564000+02:00 → 2026-10-10T21:05:07.649060+02:00. Durée calendaire : 00 h 34 min 53 s, attentes et récupérations incluses. Historique complet de quatre sessions, 136 messages, une page native par session. RSMP canonique préalable, compactage de sa session, préconditions et benchmarks PLLM, sessions temporaires de réception et sondes exclus de ces compteurs de production ; sondes comptées séparément. Contrôles HTTP/SSE et services CAB de l’orchestrateur hors historique natif de codage. Publication du présent rapport et sélection suivante après borne finale, hors compteurs.

| Résultat vérifié | Nombre | Part |
|---|---|---|
| Tests réussis | 83 / 83 | 100 % |
| Compilations séparées | 3 / 3 | 100 % |
| Validations strictes pré/post code | 2 / 2 | 100 % |
| Tâches prouvées et cochées | 7 / 7 | 100 % |
| Archive réussie | 1 / 1 | 100 % |

Tests : neuf unitaires et une intégration en processus frais sous gardes à contrôles positifs, puis 73 régressions. Archive : 2026-10-10-add-initial-bulk-operation-format-v1, specsUpdated=false ; quatre artefacts déplacés octet pour octet, change actif absent, delta verbatim du canon, 302 références et les cadrages PA/PZT conservés. Les validations RSMP préalables ciblée/globale ont retourné exit1 avec exactement trois WARNING historiques de longueur et zéro ERROR : elles ne sont pas présentées comme des validations strictes réussies.

| Décisions CAB uniques par requestId | Nombre | Part |
|---|---|---|
| approved | 18 | 85.7 % |
| rejected | 3 | 14.3 % |
| Total | 21 | 100 % |

18 décisions APPROVED correspondent à 18 effets natifs : dix commandes et huit écritures. Trois décisions REJECTED n’ont produit aucun effet : une demande d’archive omettait --yes --json ; un prévol de récupération omettait timeout_seconds ; le prévol suivant omettait timeout_seconds et utilisait true au lieu de /usr/bin/true. Sessions fautives interrompues et réconciliées ; récupération en deux phases puis deux renouvellements techniques CAB selon l’exception de prévol divergent. Checkpoint métier, sources et historiques natifs préservés, aucune fermeture ni relance du processus OpenCode. Le prévol exact final et la readiness zéro pending sont prouvés ; un pending_count transitoire a été relu sans rejouer /usr/bin/true. Aucun mandat consommé rejoué, aucune permission hors mandat consommée.

| Compteur natif de tokens | Nombre | Part |
|---|---|---|
| cache lecture | 6505487 | 93.0 % |
| cache écriture | 431759 | 6.2 % |
| entrée | 606 | 0.0 % |
| raisonnement exposé | 0 | 0.0 % |
| sortie | 53945 | 0.8 % |
| Total | 6991797 | 100 % |

Coût natif de production cumulé : 0.215884642 (unité monétaire non exposée, aucune conversion). Le compteur de raisonnement expose zéro malgré 104 parties reasoning : ventilation distincte indisponible. Usages des trois réponses interrompues potentiellement incomplets. Tokens, coût et historique exhaustif de l’orchestrateur N/A. Aucun compactage natif dans cet intervalle.

### Sondes isolées

Collecte activée à 2026-10-10T20:31:51.721634+02:00, après préconditions et avant travail métier. Fin de l’activité de codage : 2026-10-10T21:03:45.134280+02:00. Échéance périodique +30 min déclenchée ; +60 min non atteinte, aucune relève manquée ni reconstruite. Prompt constant : « Écris uniquement les entiers de 0001 à 0064 inclus, un par ligne sur quatre chiffres. Aucun commentaire, aucun outil. ». Sessions isolées sans outil, aucune lecture/écriture projet ou visite web ; contexte non injecté dans les sessions métier.

| Tentative | Lancement (fuseau inclus) | Tokens de sortie | TTMT | Tokens/s | État |
|---|---|---|---|---|---|
| début BulkOperationFormat | 2026-10-10T20:31:51.739681+02:00 | 1529 | N/A | N/A | Invalide — sortie hors consigne, exclue |
| début BulkOperationFormat reprise unique | 2026-10-10T20:32:45.944665+02:00 | 372 | N/A | N/A | Invalide — sortie hors consigne, exclue |
| +30 min BulkOperationFormat | 2026-10-10T21:01:52.298231+02:00 | 132 | N/A | N/A | Invalide — sortie hors consigne, exclue |
| +30 min BulkOperationFormat reprise unique | 2026-10-10T21:01:58.299437+02:00 | 220 | N/A | N/A | Invalide — sortie hors consigne, exclue |
| fin BulkOperationFormat | 2026-10-10T21:03:45.134301+02:00 | 573 | N/A | N/A | Invalide — sortie hors consigne, exclue |
| fin BulkOperationFormat reprise unique | 2026-10-10T21:04:09.290350+02:00 | 327 | N/A | N/A | Invalide — sortie hors consigne, exclue |

Positions prévues et déclenchées : 3/3 (début, +30 min, fin). Positions couvertes par mesure valide : 0/3 (0 %). Tentatives : 6, valides 0/6 (0 %), invalides 6/6 (100 %). Chaque position a reçu sa seule reprise immédiate autorisée, également invalide ; aucune troisième tentative. Moyennes, minima et maxima N/A : aucune mesure valide. Les réponses hors consigne sont conservées au checkpoint, avec instants monotones et métadonnées ; aucun diagnostic de cause fournisseur n’est déduit.

Surcharge séparée : 3153 tokens de sortie et coût natif 0.002555478. Formules prévues : TTMT = premier delta texte − envoi client monotone ; débit = compteur natif de sortie / intervalle premier-dernier delta. Raisonnement non ventilé, benchmarks PLLM exclus des moyennes.

## 2. Types de messages et d’outils

Convention : « approuvé et exécuté » = appel terminé avec succès, autorisé automatiquement ou sous CAB ; cela ne prouve pas une approbation manuelle. get_approval rapportant REJECTED reste une lecture réussie. Les refus CAB avant effet sont comptés séparément ; un outil interrompu ou en erreur reste une erreur technique, sans être reclassé en refus natif. Cinq erreurs techniques : quatre request_validation (trois interruptions après refus, un délai MCP) et un poll_approval expiré. Le délai ordinaire a été réconcilié sur le même approval_id.

| Rôle des messages | Nombre | Part |
|---|---|---|
| assistant | 104 | 76.5 % |
| user | 32 | 23.5 % |
| Total | 136 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| reasoning | 104 | 22.8 % |
| step-finish | 101 | 22.1 % |
| step-start | 104 | 22.8 % |
| text | 67 | 14.7 % |
| tool | 81 | 17.7 % |
| Total | 457 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| erreur/interruption | 3 | 2.9 % |
| stop | 29 | 27.9 % |
| tool-calls | 72 | 69.2 % |
| Total | 104 | 100 % |

| Outil | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| bash | 10 (12.3 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 8 (9.9 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 9 (11.1 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (2.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (1.2 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| cgpt-validation_request_validation | 21 (25.9 %) | 17 (81.0 %) | 0 (0.0 %) | 4 (19.0 %) |
| read | 21 (25.9 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (9.9 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 81 (100 %) | 76 (93.8 %) | 0 (0.0 %) | 5 (6.2 %) |

## 3. Fichiers modifiés

Huit écritures natives réussies sur sept fichiers uniques ; la seconde écriture de tasks.md coche les tâches après preuves. Quatre artefacts créés puis déplacés par archivage ; chemins finaux ci-dessous. STATISTIQUES.md sera publié sous mandat distinct après la borne, hors compteurs.

| Chemin absolu complet | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-operation-format-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-operation-format-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-operation-format-v1/specs/bulk-operations/spec.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-operation-format-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_operation_format.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_operation_format_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_operation_format.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 8 (100 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Aucun mandat d’édition refusé avant écriture (0/8). UTF-8/LF et contenus exacts examinés sans données sensibles. Périmètre vérifié sur les opérations natives, 302 références et les trois répertoires Python concernés ; aucune inspection Git, aucune prétention d’audit complet du dépôt.

## 4. Commandes

Dix commandes natives approuvées et exécutées, toutes exit0. Compilations : bytecode régénérable. Tests : processus frais et répertoires temporaires autorisés sous Pixs, nettoyés par gestionnaires de contexte ; aucune modification source autorisée.

| Famille de commandes | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| Archivage OpenSpec | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol CAB | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unitaires/intégration | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Trois demandes de commande refusées avant exécution sur treize mandats de commande (23,1 %) : archive 1, prévols 2. Les deux prévols exécutés /usr/bin/true sont distincts, chacun exécuté une seule fois sous son mandat. Commandes exactes, décisions et événements permission once conservés au checkpoint et dans les historiques natifs. Les opérations de contrôle et deux purges techniques CAB de l’orchestrateur sont hors compteurs métier ; elles ne modifient aucune source.

## 5. Accès web

| Résultat des outils web | Nombre | Taux |
|---|---|---|
| Approuvés et exécutés | 0 | N/A — aucun appel |
| Refusés | 0 | N/A — aucun appel |
| Erreurs | 0 | N/A — aucun appel |
| Total | 0 | N/A — dénominateur nul |

Aucun webfetch/websearch ; aucune URL approuvée, refusée ou visitée à lister. Transports locaux OpenCode/CAB et requêtes fournisseur LLM distincts des outils web ; aucune visite déduite d’un texte source.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — première session native | 2026-10-10T20:30:14.564000+02:00 |
| Fin — après archive et sonde finale | 2026-10-10T21:05:07.649060+02:00 |
| Durée globale, pauses incluses | 00 h 34 min 53 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de collecte | 2026-10-10T20:31:51.721634+02:00 | N/A | N/A |
| Après — archive et sonde finale | 2026-10-10T21:05:07.649060+02:00 | N/A | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

Outil natif get_usage_limits absent aux deux bornes : aucun ancien quota substitué. Quotas partagés par compte, attribution exclusive non démontrable ; aucune conversion en tokens ou coût.

| Domaine des appels d’outils | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| autres outils | 63 (77.8 %) | 58 (92.1 %) | 0 (0.0 %) | 5 (7.9 %) |
| commandes | 10 (12.3 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 (9.9 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total général | 81 (100 %) | 76 (93.8 %) | 0 (0.0 %) | 5 (6.2 %) |

Totaux croisés : 136 messages ; 81 outils = 76 réussis (93,8 %) + 0 refus natifs (0 %) + 5 erreurs techniques (6,2 %). Décisions CAB : 21 = 18 APPROVED (85,7 %) + 3 REJECTED (14,3 %). 18 effets natifs autorisés = 8 écritures sur 7 fichiers + 10 commandes. Sommes par type, domaine, fichier, commande et décision vérifiées contre les historiques complets.

Livraison : BulkOperationFormat mémoire immuable à deux champs explicites, référence opaque et formats canoniques CSV/NDJSON, refus exact des objets étrangers/dérivés/forgés et validation pure statique sans écho. 83 tests, trois compilations, deux validations strictes, sept tâches cochées et archive sans modification du canon. Aucun parsing, adaptateur, persistance ou runtime bulk ajouté. PostgreSQL et navigateurs sans objet pour ce profil ; aucune commande Git, aucun commit/push. RUN parent poursuit sa sélection, achèvement global de Pixs non démontré.

Limites : six sondes invalides, version LLM, métriques/quotas orchestrateur et temps de service N/A. Délais MCP et trois refus de transcription récupérés sur preuves, sans effet hors périmètre observé. Collecte sans reconstruction rétroactive.
