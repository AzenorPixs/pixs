# STATISTIQUES — add-bulk-validation-report-persistence-v1

Archive : openspec/changes/archive/2026-10-13-add-bulk-validation-report-persistence-v1. RUN parent : cismp-pixs-8a57078ff4d44bde.

Périmètre : historique natif complet de la session du change, jusqu’après archivage et sonde finale. Sélection préalable, sessions de sonde jetables et production du présent rapport exclues. Télémétrie interne de l’orchestrateur : N/A, non exposée. Ce rapport ne clôture pas le RUN parent.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high | 2.211 s | 299.978 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; version modèle N/A | opencode-go | high configuré ; variant natif absent | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A | N/A | N/A |

Moyennes arithmétiques des quatre sondes build/high valides. Aucune sonde orchestrateur. Versions de modèle et durées actives de génération non exposées : N/A. Temps de service cumulé tous agents et pourcentages : N/A ; durée calendaire, outils, pauses et attentes ne sont pas du temps de génération.

## 1. Statistiques générales et décisions

Durée calendaire, pauses et attentes incluses : 01 h 13 min 21 s. 265 messages ; 168 appels natifs : 167 terminés (99.4 %), 0 refus (0.0 %), 1 erreurs (0.6 %).

Convention : terminé = état natif completed, sans implication de validation fonctionnelle verte. Refus = permission/règle refusée ; erreur = incident technique. Global strict exit1 est une invocation terminée, mais reste un échec strict. Décisions CAB, outils et permissions natives sont comptés séparément.

| Décision CAB unique | Nombre | Part |
| --- | --- | --- |
| approved | 28 | 100.0 % |
| Total | 28 | 100.0 % |

| Réponse permission native SSE | Nombre | Part |
| --- | --- | --- |
| once | 28 | 100.0 % |
| Total | 28 | 100.0 % |

28 décisions approved ; 28 opérations natives sous once corrélées ; aucune décision rejetée et aucune approbation inutilisée. Une session du même job, aucune récupération technique. Pas de répétition d’un effet ni de permission consommée.

Validation exécutée : 144 tests unittest sans saut (1 unité persistance, 1 inertie harness PG, 125 régressions, 17 contrat pur) ; six suites PostgreSQL réelles réussies sur serveur 160014 : ValidationReport, InboxReceipt, EventEnvelope, CommandIdempotency, runtime et AdmissionIdentity. Six sources Python compilées ; aucun test navigateur requis. Pas de test d’exécution Python 3.12 revendiqué à partir d’une analyse grammaticale.

ValidationReport réel : huit clés restituées, tuple de mappings diagnostics dans l’ordre, Progress à six clés, None/modes/Unicode/complete faux, captures et exports owned figés, entiers au-delà int64 dans TEXT, limites stdlib encodage et décodage réellement refusées sans changement global. Plusieurs rapports pour une même opération ont des id techniques distincts. Co-commit et co-rollback du rapport et de l’effet propriétaire ; observateur indépendant avant/après commit ; identifiant inflight sans attestation de résultat. Hydraté et autre alias hors atomic refusés. Bornes/catalogues/malformed/duplicate JSON/NaN revalidés ; CHECK temporaire 23514 propagé, transaction propriétaire invalidée même si erreur capturée. Migration0009 forward/reverse seule ; onze tables précédentes, public, nettoyage du schéma owned et fermeture des connexions vérifiés.

Strict ciblé précode et final : 1/1 sans issue exit0. Global strict : 77/78, exit1, seules les trois WARNING historiques exactes bulk-operations requirements[6], [10], [13], aucune nouvelle issue. Aucune réussite globale stricte annoncée. Archivage unique --skip-specs exit0, sans resynchronisation du canon.

Un délai client MCP lors de l’archivage a été récupéré par poll_approval du même approval_id, sans seconde décision ni opération ; preuve native finale unique.
Révisions CGPT des brouillons avant écriture : artefacts corrigés vers les huit noms canoniques, Progress6/tuple de mappings et tâches non circulaires ; plafonds int64 non spécifiés retirés des données TEXT ; contexte policy/catalogues copié et revalidé, get validant le contexte avant requête même si id absent, captures figées et validation avant connexion. Tests unitaires corrigés (compte arbitraire, True valide, mode cohérent pour grand entier, vrai deferred, contexte capturé, bornes avant poison). Harness PG corrigé : DDL sql.Literal, atomic manquant, preuves réelles de capacité encode/decode, rapport co-commit/co-rollback et observateur indépendant, TransactionManagementError pendant transaction invalide. OpenCode a effectué les écritures sous mandats ; ces corrections éditoriales ne sont pas des refus natifs. Aucun échec fonctionnel des commandes du change après écriture dans les preuves collectées, hormis global strict historiquement qualifié.

| Outil incident | Résultat | callID | Diagnostic |
| --- | --- | --- | --- |
| cgpt-validation_request_validation | error | call_01a1332fe68076ab9086e21f69b82c94 | MCP error -32001: Request timed out |

Compactions natives résumées dans historique : 1. API native orchestrateur indisponible : aucune compaction conjointe revendiquée. Configuration Muse/high vérifiée ; variant natif du résumé absent : N/A. Sources contrôlées par SHA après compaction, aucun redémarrage ni fermeture OpenCode.

| Compaction | Échéance | Début réel | Retard (s) | Résultat |
| --- | --- | --- | --- | --- |
| cismp-compact-1176b8499dc1 | 2026-10-13T03:49:35.290288+02:00 | 2026-10-13T03:53:08.028497+02:00 | 212.738 | OC_COMPLETED_ROOT_API_UNAVAILABLE |

Sondes : initiale, +30 min, +60 min, finale ; quatre exigibles et quatre réussies, zéro échouée/manquée. Retards réels conservés ; aucune reconstitution rétroactive. +90 min postérieure à la fin de collecte.

| Position | Envoi réel | Retard (s) | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T03:46:13.413193+02:00 | None | 2.3917 | 299.515 | 902 |
| +30 min | 2026-10-13T04:16:43.485624+02:00 | 30.072 | 1.9033 | 333.148 | 890 |
| +60 min | 2026-10-13T04:47:21.057476+02:00 | 67.644 | 2.6371 | 287.291 | 915 |
| finale | 2026-10-13T04:58:12.945328+02:00 | None | 1.9135 | 279.956 | 890 |

Prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». TTMT = envoi au premier delta texte ; débit = output natif / durée premier–dernier delta texte, hors raisonnement. Horodatages conservés ; sessions jetables supprimées. Aucun outil/fichier/accès métier réseau.
TTMT min/max 1.903/2.637 s ; débit min/max 279.956/333.148. Surcharge séparée : entrée 47836, sortie 3597, raisonnement 975, coût natif 0.005698000.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 104 | 39.2 % |
| assistant | 161 | 60.8 % |
| Total | 265 | 100.0 % |

| Partie | Nombre | Part |
| --- | --- | --- |
| text | 255 | 27.7 % |
| step-start | 160 | 17.4 % |
| reasoning | 177 | 19.2 % |
| tool | 168 | 18.2 % |
| step-finish | 160 | 17.4 % |
| compaction | 1 | 0.1 % |
| Total | 921 | 100.0 % |

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_health | 26 | 15.5 % | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 27 | 16.1 % | 27 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 0.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 26 | 15.5 % | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_auto_remediation_policy | 1 | 0.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 28 | 16.7 % | 27 (96.4 %) | 0 (0.0 %) | 1 (3.6 %) |
| write | 11 | 6.5 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 17 | 10.1 % | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 30 | 17.9 % | 30 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 0.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 168 | 100.0 % | 167 (99.4 %) | 0 (0.0 %) | 1 (0.6 %) |

| Terminaison | Nombre | Part |
| --- | --- | --- |
| tool-calls | 97 | 60.2 % |
| stop | 63 | 39.1 % |
| None | 1 | 0.6 % |
| Total | 161 | 100.0 % |

| Composante tokens native | Nombre | Part des composantes |
| --- | --- | --- |
| input | 3633011 | 11.1 % |
| output | 80202 | 0.2 % |
| reasoning | 22095 | 0.1 % |
| cache_read | 29080976 | 88.6 % |
| cache_write | 0 | 0.0 % |
| Total | 32816284 | 100.0 % |

Coût natif cumulé : 0.441922452 ; devise/unité non exposée, aucune conversion. Cache séparé ; somme des composantes sans équivalence de facturation inventée. Pourcentages arrondis à une décimale.

| Configuration native provider/model/variant | Messages assistant | Part |
| --- | --- | --- |
| opencode-go / muse-spark-1.3-contributor / high | 160 | 99.4 % |
| opencode-go / muse-spark-1.3-contributor / None | 1 | 0.6 % |
| Total | 161 | 100.0 % |

## 3. Fichiers modifiés

| Chemin absolu après archive | Tentatives | Part | Terminées | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-validation-report-persistence-v1/proposal.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-validation-report-persistence-v1/design.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-validation-report-persistence-v1/tasks.md | 2 | 18.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-validation-report-persistence-v1/specs/bulk-operations/spec.md | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_validation_report_record.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_validation_report_repository.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0009_bulk_validation_report.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_validation_report_persistence.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_validation_report_persistence_integration.py | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 | 100.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

11 tentatives natives sur dix chemins : six sources Python (cinq nouvelles, import models.py minimal) et quatre artefacts OpenSpec déplacés par archive ; tasks écrit puis coché sur preuves. Présent rapport hors bornes, sous mandat distinct. Checkpoint cismp-state de l’orchestrateur hors télémétrie OpenCode. Cadrages, canon, purs et sources précédentes du périmètre contrôlé conservés ; Git non inspecté.

## 4. Commandes

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 4 | 23.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 | 17.6 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 4 | 23.5 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PostgreSQL réel | 6 | 35.3 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 17 | 100.0 % | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : zéro. Libellés tronqués à 100 caractères ; commandes exactes/requestId dans historique natif/checkpoint.

| Commande, libellé | Exécutions | Part |
| --- | --- | --- |
| /home/devops/.local/npm/bin/openspec validate add-bulk-validation-report-persistence-v1 --strict --… | 2 | 11.8 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_validation_report_rec… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_validation_report_pers… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -m unittest discover -s tests/unit -p test_bulk_val… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_validation_report_rec… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import json sys.path.insert(0, "/hom… | 1 | 5.9 % |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys import unittest sys.path.insert(0, "… | 1 | 5.9 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 5.9 % |
| /home/devops/.local/npm/bin/openspec archive add-bulk-validation-report-persistence-v1 --yes --skip… | 1 | 5.9 % |
| Total | 17 | 100.0 % |

Seul global strict exit1 ; autres commandes exit0. Contrôles ciblés avant/après code distincts et autorisés ; aucun test ignoré ou interrompu compté vert.

## 5. Accès web

Aucun webfetch/websearch : zéro succès, refus ou erreur ; taux N/A (dénominateur nul). Aucune URL visitée/refusée. Inférence/quotas autorisés, API locales et PostgreSQL de test hors de ce domaine ; aucun déploiement ni effet métier externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif | 2026-10-13T03:45:39.113000+02:00 |
| Fin après archive et sonde finale | 2026-10-13T04:59:00.231638+02:00 |
| Durée globale avec pauses/attentes | 01 h 13 min 21 s |

| Mesure quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant | 2026-10-13T03:45:39.121777+02:00 | N/A | N/A |
| Après | 2026-10-13T04:59:00.231638+02:00 | N/A | N/A |
| Différence après moins avant | — | N/A | — |

Outil natif get_usage_limits absent aux contrôles live ; codex/window10080/usedPercent/resetsAt : N/A. Aucun quota Go substitué. Quotas partagés par compte ; aucune attribution exclusive ni conversion en tokens/euros.

| Catégorie | Total | Part | Terminés | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| others | 140 | 83.3 % | 139 (99.3 %) | 0 (0.0 %) | 1 (0.7 %) |
| files | 11 | 6.5 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| commands | 17 | 10.1 % | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 168 | 100.0 % | 167 (99.4 %) | 0 (0.0 %) | 1 (0.6 %) |

Totaux croisés : 168 = 167 terminés + 0 refus + 1 erreurs ; 11 tentatives fichier + 17 commandes + 140 autres ; 28 décisions approved, 28 opérations natives et 28 once corrélées. Historique complet : ses_ecd1031d6ffe374CtBNpRIihZ4 (265 messages).

Livraison : primitive ValidationReportV1 à huit clés, id technique hors huit, stockage append-only sans unicité operation/latest/CAS/FK, capture structurale figée sous policy/catalogues explicites. Mode/complete/compteurs/versions ne prouvent pas la production métier ni READ_RESULT. Migration0009 réversible, 144 tests et six suites PG, six sources compilées, archive unique et rapport distinct. Aucun producteur de rapport, Outbox, Manifest, autorité, endpoint, nouvelle norme/dépendance/cadrage ; B13 global non complet. Frontend/navigateur sans objet. Git non inspecté, aucun commit/push. Secrets confinés aux processus autorisés et auth native ; aucune valeur dans modèle/sources/rapport. RUN parent continue.
