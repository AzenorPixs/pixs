# Statistiques — BulkScopeLink v1

Change : add-initial-bulk-scope-link-v1. RUN parent : cismp-pixs-758862ec875d4708.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Qwen3.8 Flash | N/A — version LLM non exposée | OpenCode Go | xhigh | 2.143 s | 78.905 | N/A |

OpenCode 1.18.35. Sessions retenues : ses_ed9932e2fffew6qJa1VK6gKYt4, ses_ed98f7649ffenn3uvw0pRhHlo5. Configuration réelle vérifiée dans les métadonnées natives.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 / Codex | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A | N/A | N/A |

Aucune sonde de l'orchestrateur. Temps de génération et dénominateur cumulé non isolables des outils et attentes : temps de service et pourcentages N/A. La durée calendaire ne mesure pas le service du modèle.

## 1. Statistiques générales et décisions

Intervalle : 2026-10-10T17:27:08.240000+02:00 → 2026-10-10T17:56:41.890280+02:00. Durée calendaire : 00 h 29 min 33 s, préconditions, attentes et récupération incluses. Historique complet de deux sessions (102 messages), une page native par session. La RSMP canonique préalable, les sessions temporaires de prévol, benchmarks PLLM et sondes sont exclus des compteurs de production; sondes comptabilisées séparément. Publication du présent rapport et sélection suivante après la borne finale, hors compteurs.

| Résultat vérifié | Nombre | Part |
|---|---|---|
| Tests réussis | 73 / 73 | 100 % |
| Compilations séparées | 3 / 3 | 100 % |
| Validations strictes du change avant/après code | 2 / 2 | 100 % |
| Tâches prouvées et cochées | 7 / 7 | 100 % |
| Archive réussie | 1 / 1 | 100 % |

Tests : 8 ciblés (7 unitaires, 1 processus frais sous gardes à contrôles positifs) et 65 régressions existantes. Archive : 2026-10-10-add-initial-bulk-scope-link-v1, specsUpdated=false, quatre artefacts déplacés à l'identique. Delta verbatim du canon; 296 empreintes de référence préservées. La RSMP préalable a conservé exactement trois WARNING historiques de longueur, zéro ERROR, avec exit 1 ciblé/global explicitement qualifié; ce résultat n'est pas présenté comme une validation stricte réussie.

| Décisions CAB uniques par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 19 | 95.0 % |
| REJECTED | 1 | 5.0 % |
| Total | 20 | 100 % |

19 décisions APPROVED correspondent à 19 effets natifs : 10 commandes et 9 écritures. Un refus avant écriture (timeout_seconds prescrit absent), interruption, get_approval du même identifiant puis récupération en deux phases avec prévol exact réussi; aucun mandat consommé rejoué. Une readiness transitoire pending_count=1 a été réconciliée par un nouvel appel réel, sans réexécuter /usr/bin/true. Aucune permission native hors cible ou commande corrélée n’a été consommée.

Une parenthèse parasite a été copiée dans WORKER lors de la création du test d'intégration. Revue directe et rapport OC ont identifié cet écart dans la cible autorisée, avant test. Une édition CAB distincte l'a corrigé; contenu ensuite vérifié octet pour octet et 73 tests passés. Ce défaut de contenu n'est pas un échec de permission ou de test exécuté.

| Compteur natif de tokens | Nombre | Part |
|---|---|---|
| cache lecture | 4639116 | 87.3 % |
| cache écriture | 633139 | 11.9 % |
| entrée | 444 | 0.0 % |
| raisonnement exposé | 0 | 0.0 % |
| sortie | 42441 | 0.8 % |
| Total | 5315140 | 100 % |

Coût natif de production cumulé : 0.220867526 (unité monétaire non exposée, aucune conversion). Le compteur de raisonnement expose 0 alors que des parties reasoning existent : ventilation distincte non disponible. Compteurs des réponses interrompues potentiellement incomplets. Tokens, coût et historique exhaustif d'outils de l'orchestrateur : N/A. Aucun compactage natif dans cet intervalle.

### Sondes isolées

Collecte activée à 2026-10-10T17:28:26.337337+02:00, après préconditions et avant toute écriture; sonde initiale lancée avec l'inventaire, reprise achevée avant le premier artefact. Fin de l'activité de codage : 2026-10-10T17:55:31.075281+02:00. L'échéance +30 min (2026-10-10T17:58:26.337337+02:00) n'était pas atteinte : aucune relève périodique due ou manquée. Prompt constant : « Écris uniquement les entiers de 0001 à 0064 inclus, un par ligne sur quatre chiffres. Aucun commentaire, aucun outil. ». Aucun outil, aucune lecture/écriture ou visite web dans ces sondes; aucune injection de leur contexte dans les sessions métier.

| Tentative | Lancement (fuseau inclus) | Tokens de sortie | TTMT | Tokens/s | État |
|---|---|---|---|---|---|
| début BulkScopeLink | 2026-10-10T17:28:26.337348+02:00 | 470 | N/A | N/A | Invalide — sortie hors consigne |
| début BulkScopeLink reprise unique | 2026-10-10T17:28:59.828384+02:00 | 359 | 2.213 s | 70.699 | Valide |
| fin BulkScopeLink | 2026-10-10T17:55:31.092160+02:00 | 346 | 2.073 s | 87.112 | Valide |

Positions prévues : 2 (début, fin); positions couvertes : 2/2 (100 %), aucune non couverte ou manquée. Tentatives : 3; valides 2/3 (66,7 %), invalides 1/3 (33,3 %). La première réponse était hors consigne, sans outil; une seule reprise immédiate autorisée, réussie. Tentative invalide conservée et exclue des moyennes.

Moyennes arithmétiques valides : TTMT 2.143 s, débit 78.905 tokens/s. TTMT min/max 2.073/2.213 s; débit min/max 70.699/87.112.
Surcharge séparée de toutes les tentatives : 1175 tokens de sortie, coût natif 0.003119014. TTMT = premier delta de texte moins envoi client monotone; débit = compteur natif de tokens de sortie / intervalle premier-dernier delta. Dates de lancement, instants monotones, métadonnées et usages conservés au checkpoint. Raisonnement non ventilé; benchmark PLLM exclu des moyennes.

## 2. Types de messages et d'outils

Convention : approuvé et exécuté = outil terminé avec succès, autorisé automatiquement ou par CAB; ce succès ne prouve pas une approbation manuelle. request_validation terminé REJECTED = refus. get_approval réussi reste une lecture réussie même s'il rapporte REJECTED. Erreur/interruption ou commande non zéro = erreur technique; décisions CAB comptées séparément. Les deux erreurs sont la lecture d'un chemin inexistant et le request_validation interrompu du mandat refusé.

| Rôle des messages | Nombre | Part |
|---|---|---|
| assistant | 75 | 73.5 % |
| user | 27 | 26.5 % |
| Total | 102 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| reasoning | 75 | 22.2 % |
| step-finish | 74 | 21.9 % |
| step-start | 75 | 22.2 % |
| text | 55 | 16.3 % |
| tool | 59 | 17.5 % |
| Total | 338 | 100 % |

| Terminaison des réponses assistant | Nombre | Part |
|---|---|---|
| erreur/interruption | 1 | 1.3 % |
| stop | 26 | 34.7 % |
| tool-calls | 48 | 64.0 % |
| Total | 75 | 100 % |

| Outil | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| bash | 10 (16.9 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 5 (8.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 3 (5.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 20 (33.9 %) | 19 (95.0 %) | 0 (0.0 %) | 1 (5.0 %) |
| edit | 2 (3.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 12 (20.3 %) | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |
| write | 7 (11.9 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 59 (100 %) | 57 (96.6 %) | 0 (0.0 %) | 2 (3.4 %) |

## 3. Fichiers modifiés

Neuf écritures natives réussies sur sept fichiers uniques. Deux éditions supplémentaires : correction ciblée de l'intégration et cochage des tâches. Les quatre artefacts ont été créés dans le change actif puis déplacés par archivage; chemins finaux ci-dessous. Le rapport lui-même est publié après la borne finale, hors compteurs.

| Chemin absolu complet | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-scope-link-v1/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-scope-link-v1/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-scope-link-v1/specs/bulk-operations/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-10-add-initial-bulk-scope-link-v1/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_scope_link.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_scope_link_integration.py | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_scope_link.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Refus avant écriture native : 1 / 10 mandats d'édition (10,0 %), sur proposal.md. Aucune écriture native pour ce refus. UTF-8/LF et contenus attendus vérifiés; absence de secret et de modification hors périmètre contrôlée sur les opérations observées et les 296 références.

## 4. Commandes

Dix commandes natives approuvées et exécutées, toutes exit 0. Compilations : bytecode régénérable. Tests : processus frais et répertoires temporaires de test dans Pixs, nettoyés par leurs gestionnaires de contexte; aucune écriture source autorisée par les mandats de tests.

| Famille de commandes | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| Archivage OpenSpec | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol CAB | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unitaires/intégration | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées avant exécution : aucune (0 / 10, 0 %). Deux prévols /usr/bin/true distincts, chacun une seule exécution sous son propre mandat. Commandes exactes, décisions et permissions once corrélées conservées dans les historiques natifs et le checkpoint.

## 5. Accès web

| Résultat des outils web | Nombre | Taux |
|---|---|---|
| Approuvés et exécutés | 0 | N/A — aucun appel |
| Refusés | 0 | N/A — aucun appel |
| Erreurs | 0 | N/A — aucun appel |
| Total | 0 | N/A — dénominateur nul |

Aucun webfetch/websearch, aucune URL approuvée/refusée/visitée à lister. Transports locaux OpenCode/CAB et requêtes du fournisseur LLM distincts des outils web; aucune visite déduite d'une URL mentionnée dans une source.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — première session native retenue | 2026-10-10T17:27:08.240000+02:00 |
| Fin — après archivage et sonde finale | 2026-10-10T17:56:41.890280+02:00 |
| Durée globale, pauses et attentes incluses | 00 h 29 min 33 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — constat au début de collecte | 2026-10-10T17:28:26.337337+02:00 | N/A | N/A |
| Après — après archivage et sonde finale | 2026-10-10T17:56:41.890280+02:00 | N/A | N/A |
| Différence après − avant | — | N/A — relevés comparables absents | — |

Outil natif get_usage_limits non exposé aux deux bornes : aucun quota inventé ou ancien substitué. Les quotas sont partagés par compte; une différence disponible ne serait attribuable exclusivement à cette session qu'avec preuve d'exclusivité. Aucune conversion en tokens ou coût.

| Domaine des appels d'outils | Total (part) | Approuvés et exécutés (taux) | Refusés (taux) | Erreurs (taux) |
|---|---|---|---|---|
| autres outils | 40 (67.8 %) | 38 (95.0 %) | 0 (0.0 %) | 2 (5.0 %) |
| commandes | 10 (16.9 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 9 (15.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total général | 59 (100 %) | 57 (96.6 %) | 0 (0.0 %) | 2 (3.4 %) |

Totaux croisés : 102 messages; 59 outils = 57 réussis (96,6 %) + 0 refus natifs (0 %) + 2 erreurs techniques (3,4 %). Décisions CAB distinctes : 20 = 19 APPROVED (95,0 %) + 1 REJECTED (5,0 %). 19 effets natifs autorisés : 9 écritures sur 7 fichiers + 10 commandes. Sommes par type et domaine vérifiées.

Livraison : BulkScopeLink mémoire immuable à deux références explicites opaques, égalité admise, validation pure et statique; 73 tests, trois compilations, deux validations strictes, sept tâches cochées, archive sans modification du canon. Aucun import concret core, résolution, autorisation, persistance ou runtime bulk ajouté. PostgreSQL et navigateurs sans objet pour ce profil; aucune commande Git, aucun commit/push. RUN parent CISMP ouvert pour la sélection suivante; achèvement global de Pixs non démontré.

Limites : version exacte du LLM, métriques/quotas de l'orchestrateur et temps de service N/A; compteurs interrompus incomplets possibles, sondes invalides exclues sans être masquées. Collecte après préconditions, sans reconstruction rétroactive. Défaut de copie corrigé et refus de protocole récupéré sur preuves, sans effet hors périmètre observé.
