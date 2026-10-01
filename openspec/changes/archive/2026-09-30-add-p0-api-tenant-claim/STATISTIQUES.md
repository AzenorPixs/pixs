# Statistiques — add-p0-api-tenant-claim

Session maîtresse `ses_f0cd50463ffezWnvxK0kEMln8q`. Compteurs cumulatifs communs au lot de deux changes : ne pas additionner ce rapport au précédent. Historique intégral OpenCode borné avant ce rapport : 2026-09-30T16:34:35.555Z à 2026-09-30T20:21:00.753Z. Change courant : début 2026-09-30T18:48:39.867Z ; dernière tâche de codage 2026-09-30T20:12:16.916Z.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte absente | opencode-go | HIGH vérifié | N/A — zéro sonde valide | N/A — zéro sonde valide | N/A — génération active non isolée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (GPT-6 déclaré) | N/A — version télémétrique absente | OpenAI | HIGH demandé ; mesure absente | N/A | N/A | N/A |

Durée de service et chevauchements N/A : aucun dénominateur mesuré. La durée calendaire inclut outils et permissions.

## 1. Statistiques générales et décisions

Un appel terminé sans erreur est réussi et autorisé techniquement ; cela ne démontre pas une approbation manuelle. Les réponses MCP négatives peuvent être des transports réussis. Les décisions CAB sont distinctes des résultats natifs ; un exit 1 est une erreur technique.

| Mesure | Nombre | Part |
|---|---|---|
| Messages | 467 | 100 % |
| Outils | 341 | 100 % |
| Réussis | 331 | 97.1 % |
| Refus natifs | 0 | 0.0 % |
| Erreurs techniques | 10 | 2.9 % |

| Décision CAB par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 58 | 95.1 % |
| REJECTED | 1 | 1.6 % |
| NEEDS_CLARIFICATION | 2 | 3.3 % |
| Total | 61 | 100 % |

57 opérations exécutées, toutes corrélées à 57 approbations uniques (100 %). Une approbation supplémentaire a été réconciliée puis abandonnée sans exécution après timeout. Aucun mandat réutilisé. Le refus de fichier et les deux commandes NEEDS_CLARIFICATION n’ont pas été exécutés.

| Tokens de production natifs | Nombre | Part |
|---|---|---|
| input | 1803967 | 2.6 % |
| output | 88623 | 0.1 % |
| reasoning | 23103 | 0.0 % |
| cache_read | 68151077 | 97.3 % |
| cache_write | 0 | 0.0 % |
| Total | 70066770 | 100 % |

Coût API natif : 0.339044054 (100 % du coût disponible, unité API). Coût Codex N/A. Compactions Codex : nombre et durée N/A ; aucun événement de compaction identifié dans cet historique OpenCode.

Change courant : 10/10 tâches prouvées (100 %), 10 tests unitaires dédiés et 3 intégrations dédiées réussis ; suites globales 557 tests unitaires et 158 intégrations réussis. Les tests dédiés sont inclus dans les suites globales, sans addition. AST Python 3.11, huit fichiers UTF-8/LF et validations strictes OpenSpec réussis. Les deux anciens tests globaux en erreur ont été suivis de validations réussies après reprise. Une normalisation Unicode d’écriture a été détectée puis corrigée avant test. Les normes et les 14 références hors cible sont inchangées.

| Sonde du lot | Envoi UTC | Fin UTC | Sortie / raisonnement | État |
|---|---|---|---|---|
| Premier change : début | N/A — borne absente | N/A — borne absente | 2374 / 1406 | Invalide 193/200 |
| Premier change : début retry | N/A — borne absente | N/A — borne absente | 2358 / 554 | Invalide 193/200 |
| Premier change : +30 min | 2026-09-30T17:19:45.808759+00:00 | 2026-09-30T17:20:08.048434+00:00 | 2354 / 543 | Invalide 193/200 |
| Premier change : fin avant suspension | 2026-09-30T17:38:02.054Z | 2026-09-30T17:38:25.340Z | 2365 / 704 | Invalide 193/200 |
| Premier change : fin après archive | 2026-09-30T18:28:39.200Z | 2026-09-30T18:31:00.511Z | 2344 / 426 | Invalide 193/200 |
| Change courant : début add-p0-api-tenant-claim | 2026-09-30T18:50:00.472Z | 2026-09-30T18:50:24.086Z | 2368 / 926 | Invalide 193/200 |
| Change courant : +60 min tardive add-p0-api-tenant-claim | 2026-09-30T19:50:49.909Z | 2026-09-30T19:51:05.318Z | 2339 / 188 | Invalide 193/200 |
| Change courant : fin après archive add-p0-api-tenant-claim | 2026-09-30T20:14:41.976Z | 2026-09-30T20:14:59.630Z | 2356 / 617 | Invalide 193/200 |

Premier change : quatre relèves effectives prévues et un retry distinct, cinq tentatives invalides. Change courant : quatre relèves prévues (début, +30, +60, fin), trois tentatives invalides (75.0 %), une manquée (25.0 %) à 19:18:39.867Z. La relève +60 prévue à 19:48:39.867Z a été tardive, à 19:50:49.909Z. Le palier +90 est après la fin du codage et sans objet. Aucune reconstitution rétroactive.

Huit tentatives exécutées (100 %), zéro valide (0.0 %), huit invalides (100 %) : moyennes/min/max TTMT et débit N/A. Sessions dédiées jetables, même configuration Go/Muse HIGH, sans outils ; prompt constant demandant 200 lignes de dix mots identiques. Toutes ont produit 193 lignes. Les premiers chronométrages non filtrés par rôle sont exclus. Surcharge séparée : 18 858 tokens de sortie et 5 364 de raisonnement (100 % des compteurs connus de sondes), coût partiel connu 0.008454408 ; coût total et durée totale N/A, bornes/coûts incomplets. Les durées observées individuelles sont conservées au checkpoint. Ces compteurs ne sont pas mélangés à la production.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 92 | 19.7 % |
| assistant | 375 | 80.3 % |
| Total | 467 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 181 | 10.3 % |
| step-start | 374 | 21.4 % |
| reasoning | 480 | 27.4 % |
| tool | 341 | 19.5 % |
| step-finish | 373 | 21.3 % |
| Total | 1749 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 284 | 75.7 % |
| stop | 89 | 23.7 % |
| incomplete | 2 | 0.5 % |
| Total | 375 | 100 % |

| Outil | Nombre / part | Réussis / taux | Refus / taux | Erreurs / taux |
|---|---|---|---|---|
| cgpt-validation_broker_readiness | 81 (23.8 %) | 81 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 61 (17.9 %) | 60 (98.4 %) | 0 (0.0 %) | 1 (1.6 %) |
| cgpt-validation_get_approval | 11 (3.2 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 36 (10.6 %) | 34 (94.4 %) | 0 (0.0 %) | 2 (5.6 %) |
| read | 72 (21.1 %) | 68 (94.4 %) | 0 (0.0 %) | 4 (5.6 %) |
| glob | 4 (1.2 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 5 (1.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 9 (2.6 %) | 6 (66.7 %) | 0 (0.0 %) | 3 (33.3 %) |
| write | 21 (6.2 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 39 (11.4 %) | 39 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 2 (0.6 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 341 (100 %) | 331 (97.1 %) | 0 (0.0 %) | 10 (2.9 %) |

## 3. Fichiers modifiés

Tentatives : 22 (21 écritures exécutées et un mandat de fichier refusé). Ce rapport est exclu de sa propre borne ; le précédent rapport est inclus. Les commandes génératrices et déplacements sont séparés.

| Chemin absolu complet | Tentatives / part | Approuvées exécutées / taux | Refusées / taux | Erreurs / taux |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/proposal.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/design.md | 2 (9.1 %) | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/tasks.md | 2 (9.1 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/specs/core/spec.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/tenant_membership.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/__init__.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/README.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_tenant_membership.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_tenant_membership_integration.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_identity_facade.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-tenant-membership/STATISTIQUES.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-tenant-claim/proposal.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-tenant-claim/design.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-tenant-claim/tasks.md | 2 (9.1 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-api-tenant-claim/specs/api/spec.md | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/api/tenant_claim.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_tenant_claim.py | 2 (9.1 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_tenant_claim_integration.py | 1 (4.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 22 (100 %) | 21 (95.5 %) | 1 (4.5 %) | 0 (0.0 %) |

Deux déplacements par commande d’archive vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-tenant-membership` et `/home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-api-tenant-claim`. `.openspec.yaml` du second change est généré par `openspec new`, sans édition manuelle. Normes core/api inchangées après archive. Écritures du checkpoint orchestrateur : nombre N/A hors télémétrie OpenCode. Artefacts `.venv/` confinés au projet, exclus de lecture/indexation.

## 4. Commandes

| Famille | Exécutées / part | Réussies / taux | Refusées / taux | Erreurs / taux |
|---|---|---|---|---|
| Prévol true | 9 (25.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 7 (19.4 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 11 (30.6 %) | 9 (81.8 %) | 0 (0.0 %) | 2 (18.2 %) |
| Contrôles Python | 3 (8.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Création venv | 1 (2.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Installation déclarée | 1 (2.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive/aide | 3 (8.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Création OpenSpec | 1 (2.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 36 (100 %) | 34 (94.4 %) | 0 (0.0 %) | 2 (5.6 %) |

39 mandats de commande : 36 exécutés (92.3 %), deux NEEDS_CLARIFICATION sans exécution (5.1 %), une approbation abandonnée sans exécution (2.6 %). Commandes explicitement refusées : aucune (0/39, 0.0 %). Deux exécutions en erreur (2/36, 5.6 %) et 34 réussies (94.4 %).

| Commande non exécutée (libellé limité à 100 caractères) | Statut | Occurrences / part des 39 mandats |
|---|---|---|
| /home/devops/python/current/bin/pip3 --python /home/devops/datas/pixs/.venv/bin/python install Djan… | Clarification | 1 (2.6 %) |
| /usr/bin/true | Clarification | 1 (2.6 %) |

| Commande approuvée non exécutée | Statut | Occurrences / part des 39 mandats |
|---|---|---|
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -c '… | APPROVED — abandonnée | 1 (2.6 %) |

L’approbation abandonnée est conservée dans `syntax_wait_incident`, sans Bash ; reprise après prévol frais et nouveau mandat.

## 5. Accès web

Agent de codage : zéro webfetch/websearch (0/341, 0.0 %), zéro URL visitée ou refusée ; taux par résultat N/A, dénominateur nul. Installation pip autorisée : téléchargements observés, URL complètes des distributions N/A.

Accès orchestrateur connus hors compte natif OpenCode : nombre global et pourcentages N/A, collecte exhaustive absente. URL réellement consultées avec succès :

- `https://opencode.ai/zen/go/v1/usage` — accès autorisé réussi
- `https://raw.githubusercontent.com/anomalyco/opencode/v1.18.33/packages/opencode/src/auth/index.ts` — accès autorisé réussi
- `https://raw.githubusercontent.com/anomalyco/opencode/v1.18.33/packages/opencode/src/server/routes/i…` — accès autorisé réussi
- `https://developers.openai.com/api/docs/guides/compaction` — accès autorisé réussi

Accès technique échoué : `https://developers.openai.com/api/docs/guides/compaction.md` — format non accepté, page non consultée ; aucune preuve de refus d’autorisation. Aucun secret dans ces URL.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-30T16:34:35.555Z |
| Fin — après archivage | 2026-09-30T20:21:00.753Z |
| Durée globale (pauses et attentes incluses) | 03 h 46 min 25 s |

Bornes cumulatives du lot partagé. Change courant : début 18:48:39.867Z, fin après archive et collecte 20:21:00.753Z, durée 01 h 32 min 20 s. Ces durées ne mesurent pas le service du modèle.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-09-30T16:46:25.578Z | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-30T20:21:00.753Z | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif `mcp__codex_app__get_usage_limits` non exposé : compte, fenêtre codex 10080 et réinitialisation non vérifiables. Le relevé initial propre au second change est également conservé comme N/A au checkpoint. Quotas partagés par le compte : aucune consommation exclusive ni conversion en tokens ou euros déduite.

| Domaine des appels natifs | Nombre / part | Réussis / taux | Refus / taux | Erreurs / taux |
|---|---|---|---|---|
| Fichiers | 21 (6.2 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 36 (10.6 %) | 34 (94.4 %) | 0 (0.0 %) | 2 (5.6 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 284 (83.3 %) | 276 (97.2 %) | 0 (0.0 %) | 8 (2.8 %) |
| Total | 341 (100 %) | 331 (97.1 %) | 0 (0.0 %) | 10 (2.9 %) |

Les 61 décisions CAB et 22 tentatives de fichier ont leurs propres dénominateurs ; le refus CAB n’ajoute aucun appel write. 21 + 36 + 0 + 284 = 341 ; 331 réussis + 0 refus natifs + 10 erreurs = 341.

État : deux archives prouvées, normes préservées, tests globaux finaux 557/158 réussis. Git : aucune opération d’agent constatée, inspection Git exclue ; état du dépôt N/A. PostgreSQL et fichiers de secrets : aucune opération ni lecture par l’agent. Incident d’authentification antérieur : le PUT a persisté une entrée contrairement à la contrainte sans fichier ; l’entrée Go a ensuite été retirée par API avec autorisation, fournisseur conservé et cache mémoire validé. Aucune valeur secrète affichée au modèle ; absence totale de persistance initiale non revendiquée. Aucune nouvelle écriture d’authentification depuis correction. Après vérification de ce rapport, le RUN retourne à SÉLECTION, sans déclaration de complétude globale.
