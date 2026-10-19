# Statistiques — add-bulk-outbox-initial-persistence-v1

RUN cismp-pixs-8a57078ff4d44bde ; job cismp-outbox-initial-2896f4f8ee19 ; racine /home/devops/datas/pixs.

Sessions du même change : ses_ecbe259daffeSkiyNXkoVQdjGS, ses_ecbc48a39ffepaSW8ujibmwYol, ses_ecb0dd2f1ffeIXpjLDNDJ0Z3j1.

Historique de production : 2026-10-13T09:15:20.741000+02:00 à 2026-10-13T14:52:20.621953+02:00. Relevé final de quota : 2026-10-13T14:57:03+02:00, après archive, avant rédaction. Sources : checkpoint non secret, historique OpenCode, décisions CAB corrélées et événements SSE conservés. Le rapport décrit un archivage réussi et une clôture bloquée à la rédaction ; aucune fermeture d’OpenCode n’est encore prouvée.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | Modèle N/A, non fournie ; OpenCode 1.19.0 | OpenCode Go / opencode-go | high | 2.3520 s | 244.546 | N/A — durée active non mesurée |
| muse-spark-1.3-contributor, compactions | Modèle N/A ; OpenCode 1.19.0 | OpenCode Go / opencode-go | high configuré ; variant absent sur 2 messages | N/A — sans sonde propre | N/A — sans sonde propre | N/A — durée active non mesurée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / famille GPT-6 déclarée | N/A — version précise non exposée | OpenAI | N/A — télémétrie absente | N/A — non sondé | N/A — non sondé | N/A — durée active non mesurée |

Moyennes sur 8 sondes de codage dédiées. Temps de service et dénominateur cumulé indisponibles ; attentes, pauses, outils et chevauchements non assimilés à la génération.

## 1. Statistiques générales et décisions

| Indicateur | Valeur | Part / convention |
| --- | --- | --- |
| Messages | 664 | 100 % |
| Outils natifs | 169 | 100 % |
| Completed | 159 | 94.1 % |
| Erreurs techniques | 10 | 5.9 % |
| Refus natifs | 0 | 0.0 % |
| Inachevés | 0 | 0.0 % |
| Décisions CAB approved | 35 | 97.2 % |
| Décisions CAB rejected | 1 | 2.8 % |
| Décisions totales | 36 | 100 % |
| Effets mandatés constatés | 34 | 11 écritures + 23 commandes |
| Réponses SSE permission.replied conservées | 27 | once ; total exhaustif N/A |
| Compactions OpenCode | 2 | Réussies OpenCode ; API Root absente |

Completed désigne le statut technique de l’outil, pas une approbation manuelle ni un résultat fonctionnel réussi. Les effets sont corrélés aux mandats ; une approbation inutilisée a été invalidée lors de la récupération. Le refus CAB concerne une demande sans exécution. Les compactions à 10:34 et 12:06 ont préservé les sources ; réussite conjointe Root/OpenCode non revendiquée.

| Compteur natif de tokens | Valeur |
| --- | --- |
| input | 4554987 |
| output | 120146 |
| reasoning | 103393 |
| total | 36908428 |
| cache_read | 32129902 |
| cache_write | 0 |

Coût API déclaré : 0.564466304, unité non exposée, 381 échantillons. Compteurs restitués sans recomposer leur total ni déduire une facture. Métriques de production propres à Root : N/A, API absente.

Sondes dédiées sans outil, fichier ni réseau demandé ; prompt constant : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. »

| Position | Envoi | Premier texte SSE | Dernier texte SSE | Tokens sortie | TTMT s | Tokens/s | Retard s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T09:17:44.494358+02:00 | 2026-10-13T09:17:46.796189+02:00 | 2026-10-13T09:17:58.396224+02:00 | 904 | 2.3018 | 77.931 | N/A |
| +30 min | 2026-10-13T09:51:51.076187+02:00 | 2026-10-13T09:51:53.272497+02:00 | 2026-10-13T09:51:55.934459+02:00 | 890 | 2.1963 | 334.34 | 246.582 |
| +60 min | 2026-10-13T10:34:00.819900+02:00 | 2026-10-13T10:34:02.966866+02:00 | 2026-10-13T10:34:11.476904+02:00 | 890 | 2.1469 | 104.582 | 976.326 |
| +90 min | 2026-10-13T10:48:22.185264+02:00 | 2026-10-13T10:48:24.083430+02:00 | 2026-10-13T10:48:26.185191+02:00 | 890 | 1.8981 | 423.454 | 37.691 |
| +120 min | 2026-10-13T11:20:45.061030+02:00 | 2026-10-13T11:20:47.073389+02:00 | 2026-10-13T11:20:49.852920+02:00 | 890 | 2.0123 | 320.198 | 180.567 |
| +150 min | 2026-10-13T12:06:18.538269+02:00 | 2026-10-13T12:06:20.486291+02:00 | 2026-10-13T12:06:23.814593+02:00 | 890 | 1.948 | 267.404 | 1114.044 |
| +180 min | 2026-10-13T12:18:29.995903+02:00 | 2026-10-13T12:18:32.691170+02:00 | 2026-10-13T12:18:36.181817+02:00 | 890 | 2.6952 | 254.967 | 45.502 |
| fin | 2026-10-13T12:50:06.435683+02:00 | 2026-10-13T12:50:10.053414+02:00 | 2026-10-13T12:50:15.310084+02:00 | 912 | 3.6177 | 173.494 | N/A |

8 relèves valides sur 8 réalisées, 0 échouée. TTMT min/max : 1.8981/3.6177 s ; débit min/max : 77.931/423.454 tokens/s. Valeurs réelles de sortie 904 au début, 912 à la fin, 890 pour les six autres, sans normalisation.

Jusqu’au relevé final à 14:57:03, 11 échéances périodiques étaient prévues : 6 réalisées en retard, 5 manquées (+210, +240, +270, +300, +330 min). Avec début et fin : 13 relèves prévues, 8 réalisées (61,5 %), 5 manquées (38,5 %). La sonde finale de 12:50 précède la récupération tardive. Aucune relève rétroactive inventée.

| Surcharge des sondes, hors production | Valeur |
| --- | --- |
| Tokens sortie | 7156 |
| Tokens totaux API | 104813 |
| Durée cumulée calendaire, pas génération | 61.569 s |
| Coût API, unité non exposée | 0.0113954 |

## 2. Types de messages et d’outils

Rôles

| Type | Effectif | Part |
| --- | --- | --- |
| user | 283 | 42.6 % |
| assistant | 381 | 57.4 % |
| Total | 664 | 100 % |

Types de parties

| Type | Effectif | Part |
| --- | --- | --- |
| text | 651 | 31.9 % |
| step-start | 381 | 18.7 % |
| reasoning | 454 | 22.3 % |
| tool | 169 | 8.3 % |
| step-finish | 381 | 18.7 % |
| compaction | 2 | 0.1 % |
| Total | 2038 | 100 % |

Terminaisons assistant

| Type | Effectif | Part |
| --- | --- | --- |
| tool-calls | 139 | 36.5 % |
| stop | 242 | 63.5 % |
| Total | 381 | 100 % |

Variants assistant

| Type | Effectif | Part |
| --- | --- | --- |
| high | 379 | 99.5 % |
| None | 2 | 0.5 % |
| Total | 381 | 100 % |

| Outil | Total | Part globale | Completed, taux ligne | Refus, taux ligne | Erreur, taux ligne |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 37 | 21.9 % | 37 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 2 | 1.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 26 | 15.4 % | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 36 | 21.3 % | 34 (94.4 %) | 0 (0.0 %) | 2 (5.6 %) |
| bash | 23 | 13.6 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 | 1.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 20 | 11.8 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 19 | 11.2 % | 11 (57.9 %) | 0 (0.0 %) | 8 (42.1 %) |
| cgpt-validation_poll_approval | 3 | 1.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| question | 1 | 0.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 169 | 100 % | 159 (94,1 %) | 0 (0,0 %) | 10 (5,9 %) |

379 variants high ; deux absents sur les compactions configurées high. Modèle unique imposé ; aucun remplacement à la fermeture.

## 3. Fichiers modifiés

19 tentatives d’écriture : 11 completed (57,9 %), 8 erreurs de schéma avant effet (42,1 %), 0 refus natif (0,0 %). Dix chemins effectivement écrits, six sources et quatre artefacts ; tasks.md écrit deux fois. Les 20 lectures completed sont séparées des modifications.

| Chemin absolu de la tentative | Tentatives | Part | Écritures mandatées completed | Refus | Erreur |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/src/pixs/backend/bulk_outbox_publication_record.py | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_outbox_publication_repository.py | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0011_bulk_outbox_publication.py | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_outbox_initial_persistence.py | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_outbox_initial_persistence_integration.py | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-outbox-initial-persistence-v1/proposal.md | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-outbox-initial-persistence-v1/design.md | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-outbox-initial-persistence-v1/tasks.md | 2 | 10.5 % | 2 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-outbox-initial-persistence-v1/specs/events/spec.md | 1 | 5.3 % | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| N/A — argument chemin absent | 8 | 42.1 % | 0 (0,0 %) | 0 (0,0 %) | 8 (100 %) |
| Total | 19 | 100 % | 11 (57,9 %) | 0 (0,0 %) | 8 (42,1 %) |

Les quatre artefacts ont été déplacés une fois par OpenSpec vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-outbox-initial-persistence-v1, sans synchronisation des spécifications canoniques (--skip-specs). models.py reçoit seulement l’import Publication ; les cinq autres sources sont nouvelles.

| Chemin source final | SHA-256 |
| --- | --- |
| /home/devops/datas/pixs/src/pixs/backend/bulk_outbox_publication_record.py | c9b70d202f12d8dbf21927bdd205ee62969f9fa86cba7f5e7474cd5b5b9ebee4 |
| /home/devops/datas/pixs/src/pixs/backend/bulk_outbox_publication_repository.py | 0fd62bbde4844b680c169c71fe259f7352a474fa35133bb08110601536403832 |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0011_bulk_outbox_publication.py | 047e9160b5bd8f1086236d2f53a93939b1ee207753b7366b67f6a486f36d9c4f |
| /home/devops/datas/pixs/src/pixs/backend/models.py | c97e48236da185bb4738f32fd0f1a8f75ed491528f28c787ea647468f57125ec |
| /home/devops/datas/pixs/tests/unit/test_bulk_outbox_initial_persistence.py | cc3888707bcb156ae9dc7803ab959e0c93b659be8816ae3fb8f21f64e5224b92 |
| /home/devops/datas/pixs/tests/integration/test_bulk_outbox_initial_persistence_integration.py | 22a7cccda71d9f01882d6444fc5622acd72e9fe15069895a51732980f15f45ee |

Lectures : 20 completed (100 %), 0 refus, 0 erreur ; chemins détaillés conservés dans statistics.metrics.files du checkpoint, sans les qualifier de modifications. Les erreurs write sans chemin ne sont attribuées à aucun fichier supposé.

## 4. Commandes

23 appels Bash completed (100 %), zéro refus natif et erreur d’outil. Les codes fonctionnels restent distincts : validation globale strict exit 1, qualifiée ci-dessous. Commandes intégrales dans le checkpoint, libellés ici limités à 100 caractères.

Familles

| Type | Effectif | Part |
| --- | --- | --- |
| Prévol CAB | 4 | 17.4 % |
| Validation OpenSpec | 4 | 17.4 % |
| Compilation Python | 3 | 13.0 % |
| Tests et contrôles Python | 11 | 47.8 % |
| Archivage OpenSpec | 1 | 4.3 % |
| Total | 23 | 100 % |

| Commande | Occurrences | Part | Completed | Refus | Erreur |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 4 | 17.4 % | 4 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate add-bulk-outbox-initial-persistence-v1 --strict --json | 3 | 13.0 % | 3 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_outbox_publication_re… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_outbox_initial_persist… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m unittest discover -s tests/unit -p test_bulk_outbox_in… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_outbox_initial_… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m unittest discover -s tests/integration -p test_bulk_ou… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -X int_max_str_digits=640 - <<'CISMP_PG_NATIVE' ↵ i… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import unittest ↵ sys.path.insert(… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -I -B -c 'import sys ↵ import json ↵ sys.path.insert(0, "… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec archive add-bulk-outbox-initial-persistence-v1 --yes --skip-sp… | 1 | 4.3 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 23 | 100 % | 23 (100 %) | 0 (0,0 %) | 0 (0,0 %) |

Commande refusée par décision CAB : true, demande hors mandat « integration pg-D dump », jamais exécutée ; 0 occurrence native. Distincte des quatre prévols /usr/bin/true mandatés et exécutés.

## 5. Accès web

| Périmètre | Appels | Approuvés | Refusés | Erreurs |
| --- | --- | --- | --- | --- |
| Codage natif | 0 | 0 ; taux N/A | 0 ; taux N/A | 0 ; taux N/A |
| Orchestrateur | N/A — agrégat non exposé | N/A | N/A | N/A |

Vérification documentaire enregistrée par Root pour Django models.E023 : https://docs.djangoproject.com/en/dev/ref/checks/ ; source officielle utilisée, aucune URL refusée enregistrée. Aucun test frontend/navigateur applicable à cette persistance backend. API locales de pilotage distinctes des accès web métier.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-13T09:15:20.741000+02:00 |
| Fin de collecte après archivage, avant rédaction | 2026-10-13T14:57:03+02:00 |
| Durée globale, pauses et attentes incluses | 05 h 41 min 42 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-13T09:11:26.421000+02:00 | 1 % | 2026-10-20T06:59:31+02:00 |
| Après — après archivage de la spécification | 2026-10-13 12:57:02 UTC à 2026-10-13 12:57:03 UTC | 5 % | 2026-10-20T06:59:31+02:00 |
| Différence après − avant | — | 4 points de pourcentage | — |

Même compte vérifié par empreinte, quota codex, fenêtre 10080 minutes, même réinitialisation. Quota partagé : variation potentiellement due à d’autres tâches, non attribuée exclusivement au change. Ancien relevé après archive sans horodatage exact conservé remplacé dans cette synthèse par un relevé natif réel. La durée décrit la collecte et non une fermeture déjà réalisée.

| Domaine | Appels | Part globale | Completed, taux ligne | Refus, taux ligne | Erreur, taux ligne |
| --- | --- | --- | --- | --- | --- |
| files | 39 | 23.1 % | 31 (79.5 %) | 0 (0.0 %) | 8 (20.5 %) |
| commands | 23 | 13.6 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| other | 107 | 63.3 % | 105 (98.1 %) | 0 (0.0 %) | 2 (1.9 %) |
| Global | 169 | 100 % | 159 (94,1 %) | 0 (0,0 %) | 10 (5,9 %) |

Fichiers : 20 lectures, 11 écritures completed, 8 erreurs. Autres : 105 completed, 2 erreurs MCP. Les 36 décisions CAB ne sont pas additionnées aux outils. Les 27 permission.replied once sont une borne conservée : troncature SSE à 10:34, total exhaustif N/A, aucune reconstruction depuis les effets.

Validation : 194 tests de régression réussis ; deux exécutions isolées supplémentaires réussies, soit 196 exécutions avec répétitions, sans prétendre 196 tests uniques. Huit suites PostgreSQL réelles réussies, connexions fermées, nettoyage et tables publiques préservées. Six sources compilées dans trois commandes. Syntaxe AST 3.12 contrôlée ; runtime Python 3.14.8 réellement exécuté, aucun runtime 3.12 testé. Suite Outbox réelle : 33 indicateurs vrais, concurrence de même scope observée via pg_blocking_pids, scope indépendant non bloqué, rollback, contraintes, FK et migration aller/retour vérifiés.

OpenSpec ciblé : 1/1, zéro problème, exit 0. Global : 77/78, exit 1 ; seuls trois WARNING historiques de longueur sur bulk-operations requirements[6], [10], [13], aucun nouveau problème. Message : Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. Six tâches cochées après preuves ; archive unique réussie le 2026-10-13 à 12:45:03+02:00.

Livraison : persistance initiale OutboxPublicationV1, 12 champs logiques, 13 colonnes Publication et compteur privé à deux colonnes ; allocation par scope et transaction propriétaire, verrouillage et rollback/concurrence vérifiés. Aucun publisher, CAS, horloge ou autorité de politique serveur ; chantier global B11 partiel.

Incidents : huit write à arguments vides échoués avant effet, récupération et invalidation de l’autorisation inutilisée. Deux délais MCP réconciliés avec le même approval_id, sans décision nouvelle ni double exécution. Brouillons comportant contraintes/defaults indus corrigés avant écriture. Variante de représentation de docstring AST équivalente tracée, puis contrôle CAB avant nouvelles écritures. Revues excessivement longues de l’orchestrateur et cadence de sondes manquée : délais non imputés au fournisseur ou au quota.

DEVOPS.md : rafraîchissement extérieur de la seule date de ligne 6, aucune écriture Root. Écart Root : recherche puis lecture de 30 lignes dans Django sous .venv, source exclue ; arrêt de son utilisation, vérification indépendante dans la documentation officielle, aucune modification.

Blocage CAB : demande cismp-f736bc2ea4c74be2a61c67828b1890f0 pour true rejetée explicitement, sans exécution. Récupération du même job, candidate unique ses_ecb0dd2f1ffeIXpjLDNDJ0Z3j1. Prévol réservé cismp-preflight-307661be553245df9adead346c43bb48 approuvé, permission unique consommée par /usr/bin/true exit 0, puis READY sans attente. Complete refusé HTTP 409 preflight-poll-divergent. Seul polling étranger observé antérieur à prepare : son inclusion dans le contrôle est une hypothèse de cause. Prévol approuvé et consommé : aucun retry, purge d’historique, autre candidate ou nouvel archivage. Reprise gelée ; contrôle 14:57 sans demande active ni permission non résolue. Décision humaine indispensable pour ce rapport ou une correction CAB séparément autorisée.

Git : aucune inspection, commit, push ou modification de branche. Secrets : aucune valeur transférée au modèle ou enregistrée ici ; seul le processus de test a chargé les paramètres privés selon CISMP. Contrôle exhaustif du dépôt pour secrets non réalisé. Sources canoniques et autres sources du périmètre contrôlé préservées.

Le développeur demande après ce rapport la fin de session et la fermeture d’OpenCode, sans prochain change. À la préparation, rapport non écrit et OpenCode ouvert ; aucune clôture normale ni fin globale du projet déclarée. Preuve de fermeture réelle à conserver séparément dans le checkpoint.

Complément de publication — 2026-10-13T16:35:52.321886+02:00 : à la demande du développeur « Peux tu finaliser ce qui aurait dû être fait sur la session CISMP1 », l’orchestrateur publie directement ce seul rapport préparé, sous mandat de clôture distinct developer-finalization-2d7343a9c785480f8790d723c42506a5. Le circuit CAB reste gelé et cette publication ne constitue pas une approbation CAB. Aucun prévol consommé, aucune écriture source et aucun archivage ne sont rejoués. Les agrégats ci-dessus conservent leurs bornes de collecte ; cette reprise de clôture en est exclue. Contrôle natif renouvelé : 664 messages, 169 outils, 159 completed et 10 erreurs, totaux concordants ; six empreintes source, quatre empreintes d’archive et 124 références préservées. Le quota partagé observé pendant cette finalisation est 6 % utilisés sur la même fenêtre hebdomadaire, relevé distinct du bilan de production. La clôture du job est demandée en BLOQUÉ avec incident preflight-poll-divergent conservé ; la validation effective du gate, le désarmement, l’arrêt des services et la fermeture d’OpenCode seront prouvés séparément dans output/cismp-state.json. Le change livré et la fin globale du projet restent distincts.
