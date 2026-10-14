# STATISTIQUES — add-bulk-cancellation-request-primitive-v1

Archive : openspec/changes/archive/2026-10-12-add-bulk-cancellation-request-primitive-v1. Session : ses_ecef89a1affe4yKhB2u5OIK7RD. RUN parent : cismp-pixs-8a57078ff4d44bde.

Périmètre : historique natif complet de la session jusqu’au relevé final après archivage ; sondes jetables et production du présent rapport exclues. Les chemins d’artefacts ci-dessous sont leurs chemins après archivage. Télémétrie interne Codex non exposée : N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high | 3.052 s | 234.458 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version de modèle non exposée, aucune déduction depuis son nom. Moyennes arithmétiques des trois sondes valides sur texte visible. Temps actif de génération et dénominateur cumulé tous agents : N/A ; pauses, outils et attentes ne sont pas comptés comme génération. Chevauchements possibles.

## 1. Statistiques générales et décisions

191 messages ; 127 outils : 126 succès (99.2 %), 0 refus (0.0 %), 1 erreur (0.8 %). 19 décisions CAB uniques approved (100.0 %) et 19 permissions natives once corrélées (100.0 %), aucun refus (0.0 %).

Convention : succès d’outil = état natif completed ; ce compteur ne prouve ni une approbation manuelle de lecture ni une validation fonctionnelle verte. Le global strict retourne 1, qualifié ci-dessous, tout en étant une invocation native terminée. Refus = permission explicitement rejetée ; erreur = incident technique sans refus. Toutes écritures et commandes ont leur décision CGPT unitaire explicite.

Résultats : quatre tests unittest réussis sans ignoré, dont deux gardes d’import inerte ; deux suites PostgreSQL réelles réussies sur serveur 160014, quinze contrôles synthétiques validés pour cancellation et dix-huit pour la régression runtime. Types hostiles : vingt et une entrées invalides sous sept gardes réellement déclenchées puis remises à zéro. Trois fichiers compilés. Strict change : 1/1, zéro issue, exit 0 avant et après code. Global strict : exit 1, 77/78 ; seul bulk-operations échoue sur les trois WARNING historiques exacts requirements[6], [10], [13] de longueur, zéro nouvelle erreur. La longueur est exclue des critères de qualité ; aucune réussite globale stricte annoncée.

Incident natif : cgpt-validation_request_validation, MCP -32001 Request timed out, callID call_01a13122fead74a4b7fdd72131ecb6f3. Récupération par poll_approval du même approval_id approval-3e04a3952be143279ae5b9dbcf4ae541 ; une seule décision, permission et exécution de la régression PG. Aucun rejeu ni effet inconnu.

Les défauts des brouillons PG ont été corrigés avant écriture/exécution : nom de schéma non conforme, faux succès de cleanup/quoting par fallback, comparaison insuffisante de checkpoint et bail, contexte protected_unit non entré, fixture EXPORT recevant un input_sha256 IMPORT. CGPT a corrigé les brouillons depuis les helpers réellement lus ; OpenCode les a écrits sous mandats unitaires, égalité des octets vérifiée puis tests réels réussis. Ces refus éditoriaux ne sont pas des refus natifs. Aucun changement de norme, modèle, migration, dépendance ou cadrage.

Compactages natifs OpenCode : 0 (0.0 % des parties). API de compactage et télémétrie de l’orchestrateur non exposées ; aucune réussite conjointe annoncée. Aucune échéance 1 h 30 atteinte dans l’intervalle de cette session de codage.

Relèves prévues sur l’intervalle : initiale, +30 min, finale, soit 3 ; réussies 3/3 (100.0 %), échecs 0/3 (0.0 %), manquées 0/3 (0.0 %). La périodique a été réellement envoyée avec 124.173 s de retard, pas reconstruite rétroactivement. Prochaine échéance +60 min après la fin de l’intervalle.

| Position | Envoi réel | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- |
| début | 2026-10-12T18:52:53.121251+02:00 | 2.325 | 240.770 | 890 |
| +30 min | 2026-10-12T19:24:57.294324+02:00 | 2.956 | 235.402 | 907 |
| fin | 2026-10-12T19:35:22.222381+02:00 | 3.875 | 227.202 | 904 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT = premier delta texte moins envoi ; débit = tokens output natifs / durée premier–dernier delta texte, hors raisonnement. TTMT min/max 2.325/3.875 s ; débit min/max 227.202/240.770. Surcharge des sondes : 2701 tokens sortie, 970 raisonnement, 35877 entrée ; coût natif 0.0043219, hors production.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 60 | 31.4 % |
| assistant | 131 | 68.6 % |
| Total | 191 | 100.0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 143 | 21.4 % |
| step-start | 131 | 19.6 % |
| reasoning | 136 | 20.4 % |
| tool | 127 | 19.0 % |
| step-finish | 131 | 19.6 % |
| Total | 668 | 100.0 % |

| Outil | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 18 | 14.2 % | 18 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 41 | 32.3 % | 41 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 7 | 5.5 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 5 | 3.9 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 17 | 13.4 % | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 19 | 15.0 % | 18 (94.7 %) | 0 (0.0 %) | 1 (5.3 %) |
| write | 7 | 5.5 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 11 | 8.7 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 127 | 100.0 % | 126 (99.2 %) | 0 (0.0 %) | 1 (0.8 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 91 | 69.5 % |
| stop | 40 | 30.5 % |
| Total | 131 | 100.0 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| input | 1305138 | 6.1 % |
| output | 49808 | 0.2 % |
| reasoning | 13044 | 0.1 % |
| cache_read | 19882541 | 93.6 % |
| cache_write | 0 | 0.0 % |
| Total | 21250531 | 100.0 % |

Coût natif cumulé 0.182849282 ; unité/devise non exposée par l’API, aucune conversion. Pourcentages à une décimale, écarts d’arrondi possibles.

## 3. Fichiers modifiés

| Chemin absolu après archivage | Tentatives | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-cancellation-request-primitive-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-cancellation-request-primitive-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-cancellation-request-primitive-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-cancellation-request-primitive-v1/specs/bulk-operations/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_runtime_repository.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_cancellation_request.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_cancellation_request_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Compteurs = tentatives write/edit, pas lignes de code : sept fichiers distincts, tasks.md écrit puis coché après preuves. Quatre artefacts déplacés par l’archive. Présent rapport publié après les bornes sous mandat distinct, sans auto-comptage. Les autres octets du repository et tous cadrages/canons sont préservés.

## 4. Commandes

| Famille | Exécutions | Part | Terminées | Refus | Erreurs transport |
| --- | --- | --- | --- | --- | --- |
| OpenSpec : strict ciblé x2, global strict, archive | 4 | 36.4 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest : unitaires et gardes | 4 | 36.4 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PostgreSQL réel : cancellation et régression runtime | 2 | 18.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 | 100.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Dix commandes complètes distinctes, onze exécutions : le strict ciblé est contrôlé avant et après code. Le global strict exit 1 est un échec de validation qualifié, pas une réussite verte ; les autres commandes retournent 0. Commandes refusées : aucune, 0 (0.0 %). Libellés ci-dessus limités à 100 caractères, commandes complètes et requestId conservés dans historique natif/checkpoint.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée ou refusée à lister. Inférence/quotas fournisseurs et API locales autorisées hors de ce domaine. Aucun service métier externe ni déploiement.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif de session | 2026-10-12T18:52:10.853000+02:00 |
| Fin — après archivage et sonde finale | 2026-10-12T19:38:51.599212+02:00 |
| Durée globale, pauses et attentes incluses | 00 h 46 min 40 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de collecte avant premier travail | 2026-10-12T18:52:53.121251+02:00 | N/A | N/A |
| Après — après archivage | 2026-10-12T19:38:51.599212+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux contrôles : codex/window10080/usedPercent/resetsAt indisponibles ; aucun ancien relevé ou source externe substitué. Quotas partagés par compte, aucune attribution exclusive ou conversion en tokens/euros.

| Domaine | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 108 | 85.0 % | 107 (99.1 %) | 0 (0.0 %) | 1 (0.9 %) |
| commandes | 11 | 8.7 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 8 | 6.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 127 | 100.0 % | 126 (99.2 %) | 0 (0.0 %) | 1 (0.8 %) |

Totaux croisés vérifiés : 127 appels, 126 terminés, 0 refus, 1 erreur MCP récupérée ; 19 décisions et 19 once ; 8 écritures + 11 commandes + 108 autres.

Résultat livré : primitive interne de pose cooperative cancellation_requested avec CAS et révision, aucune autorité CANCEL fabriquée, aucun état/chunk/progrès/checkpoint/bail/échéance réécrit. Quatre unittest et deux suites PostgreSQL réelles réussis, trois compilations, strict ciblé vert ; global strict qualifié ci-dessus. Archive unique --skip-specs et canon préservé. Aucun modèle, migration, dépendance ou cadrage modifié. Aucune preuve d’action CANCEL autoritative de bout en bout ni de runtime Bulk global terminé. Pas de frontend concerné, tests navigateur sans objet. Git non inspecté, aucun commit/push ni déploiement. Secrets confinés aux processus autorisés et auth native ; aucune valeur dans modèle, sources ou rapport. Le RUN parent revient à SÉLECTION après vérification de ce rapport, sans clôture globale.
