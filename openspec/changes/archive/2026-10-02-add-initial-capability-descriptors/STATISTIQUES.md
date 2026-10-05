# STATISTIQUES — add-initial-capability-descriptors

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T15:44:44.038109+00:00 ; fin après archivage et sonde finale 2026-10-02T18:04:04.571934+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

Collecte active après arbitrage conceptuel, avant blueprints intégraux et toute écriture OpenSpec/source; échange sur fenêtre GPT hors périmètre de production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| glm-5.3-flash | N/A — version modèle non exposée | opencode-go | N/A | N/A | N/A | 62.392 s mesurables ; part N/A |
| glm-5.3-flash | N/A — version modèle non exposée | opencode-go | high | 6.657 s | 66.853 | 1844.538 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | N/A — version modèle non exposée | OpenAI | high | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 142 | 100 % |
| Appels outils | 81 | 100 % |
| Approuvé et exécuté | 80 | 98.8 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 1 | 1.2 % |
| Durée calendaire avec pauses | 02 h 19 min 20 s | 100 % de l’intervalle |

| Réponses en erreur ou interrompues | Nombre | Part assistants |
|---|---|---|
| Champ error natif non vide | 0 | 0.0 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 15686656 | 81.2 % |
| cache_write | 0 | 0.0 % |
| input | 3501798 | 18.1 % |
| output | 68637 | 0.4 % |
| reasoning | 57002 | 0.3 % |
| total | 19314093 | 100 % du total API |

Coût agrégé API : 1.058688880 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 2 (part 0.5 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 21 | 100.0 % |
| TOTAL | 21 | 100 % |

Résultats finaux : 109 tests ont réussi sur Python 3.14.8 : 27 nouveaux tests unitaires, 1 nouvelle intégration, 39 tests unitaires de régression et 42 intégrations de régression. Le vérificateur a confirmé la syntaxe AST 3.11 du parent et du script enfant, UTF-8/LF, les quatre sources approuvées, les cinq artefacts, les 123 empreintes préservées, les algorithmes fournisseurs/conformité inchangés et une seule résolution. Neuf tâches ont été cochées après les preuves. Les validations OpenSpec strictes avant code, après code et après cochage ont réussi. Le seul archivage (requestId cismp-pixs-20261001-20da13be348a) a réussi ; les spécifications étaient déjà synchronisées et restent inchangées. La publication et la vérification de ce rapport sont distinctes et hors des bornes de production ; le cycle parent demeure OPEN.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 104 | 73.2 % |
| user | 38 | 26.8 % |
| TOTAL | 142 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| compaction | 2 | 0.5 % |
| reasoning | 27 | 6.5 % |
| step-finish | 103 | 24.9 % |
| step-start | 104 | 25.1 % |
| text | 97 | 23.4 % |
| tool | 81 | 19.6 % |
| TOTAL | 414 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| absent | 1 | 1.0 % |
| stop | 36 | 34.6 % |
| tool-calls | 67 | 64.4 % |
| TOTAL | 104 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 11 | 13.6 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 6 | 7.4 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 3 | 3.7 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 21 | 25.9 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 4 | 4.9 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 1.2 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 25 | 30.9 % | 24 | 96.0 % | 0 | 0.0 % | 1 | 4.0 % |
| write | 10 | 12.3 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 81 | 100 % | 80 | 98.8 % | 0 | 0.0 % | 1 | 1.2 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f0342c3e0ffeGjabJTz3rTDfnI | 142 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-descriptors/.openspec.yaml | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-descriptors/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-descriptors/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-descriptors/specs/capabilities/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-descriptors/tasks.md | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/capabilities.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/composition.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_capability_descriptors_integration.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_capability_descriptors.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 10 | 100 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-capability-descriptors. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 36.4 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 2 | 18.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/true | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /home/devops/.local/npm/bin/openspec validate add-initial-capability-descriptors --strict | 3 | 27.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] true | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src:/home/de… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [7] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src:/home/de… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [8] /home/devops/python/current/bin/python3 -B -c 'import json,hashlib from pathlib import Path s=j… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [9] /home/devops/.local/npm/bin/openspec archive add-initial-capability-descriptors --yes | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 11 | 100 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucune URL visitée par l’agent de codage dans cet intervalle, aucun outil web exécuté. Les recherches techniques de l’orchestrateur et l’évaluation fournisseur PLLM restent hors de la télémétrie de production OpenCode ; elles sont déclarées séparément et ne sont pas attribuées au codeur. Volumes d’outils orchestrateur non exposés dans cette télémétrie : N/A.

Lectures web de l’orchestrateur dans ce scope : 1 appel(s) (100 % des appels enregistrés de ce sous-périmètre) ; statut approuvé et lu. URL : https://docs.python.org/3/reference/expressions.html#membership-test-operations. Hors comptages natifs OpenCode ; autres volumes orchestrateur N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T15:44:44.038109+00:00 |
| Fin — après archivage | 2026-10-02T18:04:04.571934+00:00 |
| Durée globale (pauses et attentes incluses) | 02 h 19 min 20 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T15:44:44.038109+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T18:04:04.571920+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 60 | 74.1 % | 59 | 98.3 % | 0 | 0.0 % | 1 | 1.7 % |
| Commandes | 11 | 13.6 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 10 | 12.3 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 81 | 100 % | 80 | 98.8 % | 0 | 0.0 % | 1 | 1.2 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| initiale | 2026-10-02T15:44:44.085906+00:00 | 2026-10-02T15:45:02.777537+00:00 | 2026-10-02T15:45:38.209500+00:00 | 18.691629 | 13.518867 | 479 | réussie |
| périodique — créneau 2026-10-02T16:45:38.677407+00:00 | 2026-10-02T16:56:45.136185+00:00 | 2026-10-02T16:56:46.583792+00:00 | 2026-10-02T16:56:49.935987+00:00 | 1.447603 | 142.294727 | 477 | réussie |
| périodique — créneau 2026-10-02T17:15:38.677407+00:00 | 2026-10-02T17:30:05.348352+00:00 | 2026-10-02T17:30:07.199250+00:00 | 2026-10-02T17:30:21.661593+00:00 | 1.850896 | 33.120499 | 479 | réussie |
| périodique — créneau 2026-10-02T17:45:38.677407+00:00 | 2026-10-02T17:46:03.653044+00:00 | 2026-10-02T17:46:04.855038+00:00 | 2026-10-02T17:46:08.647268+00:00 | 1.201992 | 125.783374 | 477 | réussie |
| finale — après archivage avant rapport | 2026-10-02T18:03:24.484250+00:00 | 2026-10-02T18:03:34.574794+00:00 | 2026-10-02T18:03:59.078662+00:00 | 10.090542 | 19.547933 | 479 | réussie |

Relèves prévues : 6 (100 %) ; réussies 5 (83.3 %), échouées 0 (0.0 %), manquées 1 (16.7 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 1.201992/6.656533/18.691629 s ; débit min/moy/max : 13.518867/66.853080/142.294727 tok/s.

| Relève manquée UTC | Cause |
|---|---|
| 2026-10-02T16:15:38.677407+00:00 | Créneau manqué pendant génération initiale interrompue par arrêt OpenCode, puis reprise manuelle et pause Codex demandée ; non recréé rétroactivement |

| Relève prévue UTC | Envoi réel UTC | Retard secondes |
|---|---|---|
| 2026-10-02T16:45:38.677407+00:00 | 2026-10-02T16:56:45.136185+00:00 | 666.459 |
| 2026-10-02T17:15:38.677407+00:00 | 2026-10-02T17:30:05.348352+00:00 | 866.671 |
| 2026-10-02T17:45:38.677407+00:00 | 2026-10-02T17:46:03.653044+00:00 | 24.976 |

Surcharge sondes : 46082 tokens total API, 2391 tokens sortie, coût API 0.007863250, durées stream mesurées 81.542608 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Propositions source corrigées avant toute écriture : fixtures de conformité, validation des entrées, syntaxe du script enfant et filtre des types exacts avec régression de métaclasse. OpenCode s’est arrêté pendant une proposition et le développeur l’a relancé manuellement. La pause et le redémarrage Codex pour le contexte figurent dans le checkpoint. 2 compactions natives ont conservé la même session ; aucun mandat exécuté n’a été rejoué. Un tour de readiness vide a été suivi d’un appel réel READY. Les listes vides optionnelles du SDK ont été corrélées sur le résultat MCP normalisé avant décision. Les HTTP 400 sans décision stockée ont été repris après GET 404, puis une décision unique. Aucun effet hors périmètre ni opération refusée exécutée. Une lecture native du chemin inexistant src/pixs/kernel/diagnostics.py est conservée comme erreur technique ; le paquet diagnostics/ a ensuite été lu, sans effet. Une relève manquée n’a pas été recréée ; les relèves différées portent leurs heures réelles.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-capability-descriptors, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucune variable PostgreSQL chargée ni connexion applicative dans ce scope ; aucune installation ni modification Git. Sources sensibles exclues des lectures natives de ce scope. Descripteurs seulement ; aucune couverture opérationnelle AVAILABLE, aucun P0/readiness/global ; Python pur. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.

Publication hors des bornes de production : une première tentative a été interrompue avant exécution après une demande Bash non corrélée au mandat d’édition. La permission pour « ls openspec/changes/archive/2026-10-02-add-initial-capability-descriptors/ 2>&1 » a été explicitement refusée ; aucun fichier STAT n’existait et les sources/spécifications restaient intactes. La session fautive a été figée, une nouvelle session ses_f022b133fffe9xGy4geWvAaJN6 a confirmé READY ; le test CAB inédit cismp-pixs-20261001-5a6121a815b0 a exécuté true une fois avec exit 0 et décision corrélée. Un premier contrôle avait encore pending_count 1 ; un nouvel appel réel a confirmé READY et pending_count 0 avant la reprise. Seule la publication reste à reprendre, sans réarchivage. Cet incident et sa récupération sont hors des tableaux bornés à 18:04:04 UTC.
