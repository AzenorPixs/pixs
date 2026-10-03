# Statistiques — add-p0-runtime-profile-declarations

Session maîtresse `ses_f0cd50463ffezWnvxK0kEMln8q`. Historique intégral consulté ; compteurs de la seule phase de ce change, filtrés sur les horodatages natifs depuis 2026-09-30T20:49:40.850Z jusqu’au relevé final après archive 2026-09-30T21:20:09.811Z. Aucun partage reconstruit des anciens changes. Ce rapport et son mandat sont hors borne. L’orchestration commence à l’armement du job ; dernière tâche de code 2026-09-30T21:16:00.505Z.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte non publiée | opencode-go | HIGH — 105 messages vérifiés | N/A — aucune sonde valide | N/A — aucune sonde valide | N/A — génération active non isolée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (GPT-6 déclaré) | N/A — version télémétrique absente | OpenAI | HIGH demandé ; mesure absente | N/A | N/A | N/A |

Temps de service et chevauchements N/A : aucun dénominateur mesuré. Durée calendaire, outils et attentes ne sont pas assimilés au temps de génération.

## 1. Statistiques générales et décisions

Appel natif réussi et autorisé techniquement ne signifie pas nécessairement approbation manuelle. Décisions CAB et refus natifs sont distincts ; un échec de test serait une erreur technique.

| Mesure | Nombre | Part |
|---|---|---|
| Messages | 129 | 100 % |
| Appels outils | 81 | 100 % |
| Réussis | 81 | 100 % |
| Refus natifs | 0 | 0.0 % |
| Erreurs natives | 0 | 0.0 % |

| Décision CAB finale unique | Nombre | Part |
|---|---|---|
| APPROVED | 20 | 100 % |
| REJECTED | 0 | 0.0 % |
| NEEDS_CLARIFICATION | 0 | 0.0 % |
| Total | 20 | 100 % |

20 opérations exécutées, corrélées à 20 approbations uniques (100 %), aucun mandat réutilisé. Les publications HTTP de décision ont rencontré trois réponses vides documentées côté orchestrateur ; GET404 a confirmé l’absence de décision avant nouvelle tentative de transport. Chaque décision a été conservée une seule fois. Deux prévols true frais réussis après réconciliation. Aucun timeout natif non résolu ni opération doublée. Ces incidents du pilotage sont hors dénominateur des 81 outils natifs.

| Tokens de production natifs | Nombre | Part |
|---|---|---|
| input | 108188 | 0.3 % |
| output | 19309 | 0.1 % |
| reasoning | 643 | 0.0 % |
| cache_read | 36490329 | 99.7 % |
| cache_write | 0 | 0.0 % |
| Total | 36618469 | 100 % |

Coût API natif : 0.087789858 (100 % du coût disponible, unité API). Coût orchestrateur N/A. Compactions OpenCode : aucun événement observé ; nombre/durée des compactions Codex N/A.

Résultat : 10/10 tâches prouvées (100 %), 13 tests unitaires dédiés, 3 intégrations dédiées, 570 tests unitaires globaux et 161 intégrations globales réussis. Les dédiés sont inclus dans les suites globales, sans addition comme cas uniques. Exemple docstring réellement exécuté, import pur sans Django/psycopg, readiness/rôles backend inchangés, AST Python3.11 trois fichiers, UTF8/LF huit fichiers et trois validations strictes réussis. Neuf références inchangées et norme runtime byte-identique après archive.

| Sonde | Envoi UTC | Premier événement assistant UTC | Dernier événement UTC | Fin UTC | Sortie / raisonnement | État |
|---|---|---|---|---|---|---|
| début add-p0-runtime-profile-declarations | 2026-09-30T20:49:40.865Z | 2026-09-30T20:49:56.057Z | 2026-09-30T20:50:08.487Z | 2026-09-30T20:50:08.498Z | 2341 / 405 | Invalide 193/200 |
| fin après archive add-p0-runtime-profile-declarations | 2026-09-30T21:18:44.575Z | 2026-09-30T21:18:47.435Z | 2026-09-30T21:18:58.311Z | 2026-09-30T21:18:58.305Z | 2358 / 711 | Invalide 193/200 |

Deux relèves prévues et exécutées (100 %), zéro valide (0.0 %), deux invalides (100 %), zéro manquée (0.0 %). +30 prévu à 2026-09-30T21:19:40.850Z après fin du code : sans objet, aucune reconstitution. Sessions dédiées Go/Muse HIGH, même prompt de 200 lignes de dix mots constants, sans outils ni fichiers ; 193 lignes à chaque tentative. Moyennes/minimum/maximum TTMT et débit N/A. Les timings bruts sont conservés mais exclus des moyennes.

| Surcharge de télémétrie hors production | Valeur | Part des compteurs de sondes |
|---|---|---|
| Sortie | 4699 | 100 % |
| Raisonnement | 1116 | 100 % |
| Coût API | 0.003337052 | 100 % |
| Durée calendaire des sondes (non service) | 41.363 s | 100 % |


## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 24 | 18.6 % |
| assistant | 105 | 81.4 % |
| Total | 129 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 48 | 10.3 % |
| step-start | 105 | 22.6 % |
| reasoning | 125 | 26.9 % |
| step-finish | 105 | 22.6 % |
| tool | 81 | 17.5 % |
| Total | 464 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| stop | 24 | 22.9 % |
| tool-calls | 81 | 77.1 % |
| Total | 105 | 100 % |

| Outil | Nombre / part | Réussis / taux | Refus / taux | Erreurs / taux |
|---|---|---|---|---|
| cgpt-validation_request_validation | 20 (24.7 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 12 (14.8 %) | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 20 (24.7 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 20 (24.7 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (9.9 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 81 (100 %) | 81 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |


## 3. Fichiers modifiés

Huit tentatives natives toutes exécutées et réussies (100 %). Aucun refus ni erreur d’écriture (0.0 %). Métadonnées générées par CLI comptées parmi commandes, pas comme write.

| Chemin absolu complet avant archive | Tentatives / part | Approuvées exécutées / taux | Refusées / taux | Erreurs / taux |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-runtime-profile-declarations/proposal.md | 1 (12.5 %) | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-runtime-profile-declarations/design.md | 1 (12.5 %) | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-runtime-profile-declarations/tasks.md | 2 (25.0 %) | 2 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-runtime-profile-declarations/specs/runtime/spec.md | 1 (12.5 %) | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/runtime_profiles.py | 1 (12.5 %) | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_runtime_profiles.py | 1 (12.5 %) | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_runtime_profiles_integration.py | 1 (12.5 %) | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 (100 %) | 8 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

Dossier du change déplacé par la commande archive vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-runtime-profile-declarations`. Neuf références hors cible inchangées, aucune façade modifiée. Écritures orchestrateur de `/home/devops/datas/pixs/output/cismp-state.json` hors historique natif : nombre N/A.

## 4. Commandes

| Famille | Exécutées / part | Réussies / taux | Refusées / taux | Erreurs / taux |
|---|---|---|---|---|
| Création OpenSpec | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol true | 2 (16.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 3 (25.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 4 (33.3 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Contrôles Python | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive/aide | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 (100 %) | 12 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

Toutes les 12 commandes mandatées sont exécutées (100 %). Commandes refusées : aucune (0/12, 0.0 %). Aucune commande non exécutée ni reprise d’un requestId. Les deux prévols true ont chacun leur propre approbation, opération unique. Aucun libellé de commande long reproduit.

## 5. Accès web

Zéro outil webfetch/websearch (0/81, 0.0 %), zéro URL visitée ou refusée par l’agent de codage ; taux par résultat N/A (dénominateur zéro). Aucun téléchargement ni accès externe métier entrepris pour ce change. Les appels au fournisseur LLM pour génération et les transports CAB locaux sont distincts des outils de navigation. Aucun accès web de l’orchestrateur pendant cette phase, hors transport normal du fournisseur de modèles ; diagnostic CAB par lecture locale de source publique sans modification.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-30T20:49:40.850Z |
| Fin — après archivage | 2026-09-30T21:20:09.811Z |
| Durée globale (pauses et attentes incluses) | 00 h 30 min 29 s |

Durée propre à ce change, arrondie à la seconde, distincte de la génération active.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-09-30T20:49:40.850Z | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-30T21:20:09.811Z | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent au début et à la fin : quota codex/fenêtre10080, compte et resets non vérifiables. Aucune valeur remplacée par Go ou reconstituée. Quota partagé par le compte ; exclusivité de consommation non vérifiée, aucune conversion en tokens/euros.

| Domaine natif | Nombre / part | Réussis / taux | Refus / taux | Erreurs / taux |
|---|---|---|---|---|
| Fichiers | 8 (9.9 %) | 8 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 12 (14.8 %) | 12 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 61 (75.3 %) | 61 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 81 (100 %) | 81 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

8 + 12 + 0 + 61 = 81 ; 81 réussis + 0 refus natifs + 0 erreurs = 81. Les décisions CAB ont un dénominateur de 20.

État : archive prouvée, tests finaux570/161 verts, norme préservée ; descriptions uniquement, aucune readiness opérationnelle revendiquée. Git : aucune opération d’agent constatée, inspection exclue, état Git N/A. Aucun PostgreSQL réel, environnement réel, secret lu/résolu ni nouveau fournisseur/dépendance. Les incidents d’authentification des phases antérieures ne sont pas effacés par ce rapport ; ils restent au checkpoint et au rapport précédent. Après preuve de ce fichier, le RUN revient à SÉLECTION ; le P0 complet reste non prouvé.
