# Statistiques — add-initial-bulk-job-handler-vocabulary-v1

RUN `cismp1-pixs-4e7ef6b5707c41ca`, contexte CAB 319, session OpenCode `ses_eafc899a0ffe24tQEtajuHwJxu`. Racine : /home/devops/datas/pixs. Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-job-handler-vocabulary-v1.

Périmètre figé avant rédaction du présent rapport : session de production seule, complétée par deux sondes dédiées. Les actes de rédaction de ce rapport et de clôture sont exclus des totaux de cet intervalle ; ils ont leurs mandats distincts. Sources : historique natif HTTP OpenCode, agrégats CAB filtrés, checkpoint non secret et relevés natifs Codex du tour.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version modèle non exposée ; agent OpenCode 1.19.3 | OpenCode Go (opencode-go) | high | 2.170 s | 547.677 | N/A — temps de génération non isolé |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| gpt-6.1-sol | N/A — version exacte non exposée | OpenAI / Codex | high | N/A — non sondé | N/A — non sondé | N/A — télémétrie de service non exposée |

Les identités proviennent des métadonnées natives réellement observées. Le modèle de codage reste identique aux sondes ; aucune version n’est déduite de son nom. Le temps de service cumulé et son dénominateur sont N/A : busy, durée calendaire et durée des outils ne sont pas du temps de génération. Aucun gain causal ni consommation exclusive ne sont calculés.

## 1. Statistiques générales et décisions

Durée calendaire : **00 h 17 min 47 s**, pauses, attentes, prévols, validations et archive inclus. Livraison structurelle : BulkJobHandler à quatre valeurs exactes et BULK_JOB_HANDLER_VERSION = 1.0.0 ; aucun worker ou runtime n’est qualifié par ce change.

| Décision CAB | Nombre | Part |
| --- | --- | --- |
| Approuvée | 17 | 100.0 % |
| Refusée | 0 | 0.0 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 17 | 100.0 % |

17 permissions natives once, dont le prévol exact /usr/bin/true (exit 0). Les 78 outils natifs sont terminés (100.0 %), sans erreur d’outil ni refus natif (0.0 % chacun). Convention : « approuvé et exécuté » signifie outil achevé, sous autorisation implicite de lecture ou décision CAB explicite ; un succès natif ne prouve jamais à lui seul une approbation manuelle ni un test réussi. Les 17 décisions explicites couvrent 8 écritures et 9 commandes.

Parmi les 9 commandes achevées : 7 exits 0 (77.8 %), 2 exits 1 (22.2 %), tous deux dus aux quatre warnings historiques de longueur du strict global ; zéro ERROR. Ce sont des résultats de validation non nuls, distincts des erreurs techniques d’outil. Les incidents d’orchestration HTTP 400 (identifiant local réconcilié) et 409 (acquisition de publication rectifiée en lecture) sont hors compteurs natifs, sans effet métier ni rejeu d’une once.

| Résultat du développement | Résultat observé |
| --- | --- |
| Compilation Python | 3 fichiers compilés, exit 0 |
| Tests ciblés et régressions | 23/23 réussis (100.0 %), 0 échec, 0 skip |
| OpenSpec ciblé strict | exit 0 ; skip_specs:true accepté sans delta artificiel |
| OpenSpec global standard avant archive | 185/185, exit 0 |
| Strict global avant archive | 183/185 ; exit 1, 4 WARNING longueur et 0 ERROR |
| Strict global après archive | 182/184 ; exit 1, mêmes 4 WARNING et 0 ERROR |
| Archive | Une seule exécution, exit 0, tâches complètes et déplacement vérifiés |
| Publication CAB | publish-160ff40902364881a3e099400d8ce491, référence 40 |
| Style/types | N/A — aucun contrôle dédié configuré dans pyproject.toml |
| PostgreSQL / navigateur / build frontend | N/A — vocabulaire pur sans effet DB ni interface |

Avertissements préexistants : bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4]. Les canons concernés n’ont pas été modifiés. Aucun strict global réussi n’est revendiqué.

| Compteur de production natif | Valeur |
| --- | --- |
| Messages | 124 |
| Outils | 78 |
| Entrée | 341272 |
| Sortie | 28504 |
| Raisonnement | 5621 |
| Cache lu | 12253746 |
| Cache écrit | 0 |
| Coût télémétrique cumulé | 0.065459692 — unité monétaire non exposée |
| Compactions observées | 0 |

Les compteurs tokens et cache sont publiés séparément, sans addition pouvant les compter deux fois. Les contextes répétés ne représentent pas du contenu unique. Les sondes sont exclues de ces totaux. Les compteurs propres à l’orchestrateur ne sont pas exposés et restent N/A.

Sondes TTMT/débit : même prompt « Sans outil, sans fichier et sans réseau. Réponds seulement avec les entiers de 1 à 160, séparés par un espace, sans commentaire. ». Prévue : début + fin, 2 relèves ; réussies 2/2 (100.0 %), échouées 0/2, manquées 0/2. Aucune échéance +30 min dans cet intervalle inférieur à trente minutes.

| Position | Horodatage | TTMT | Tokens sortie | Fenêtre premier–dernier texte | Débit | Résultat |
| --- | --- | --- | --- | --- | --- | --- |
| début | 18/10/2026 20:11:52 Europe/Paris | 2.224 s | 328 | 0.612 s | 535.948 tokens/s | Réussi |
| fin | 18/10/2026 20:28:18 Europe/Paris | 2.116 s | 339 | 0.606 s | 559.406 tokens/s | Réussi |

Moyennes arithmétiques : TTMT 2.170 s (min 2.116, max 2.224) ; débit 547.677 tokens/s (min 535.948, max 559.406). TTMT utilise le début du texte natif, mesuré depuis l’envoi ; débit = tokens de sortie fournis / fenêtre entre début et fin du texte. Ces fenêtres courtes peuvent accentuer les effets de mise en tampon ; aucune assimilation au débit global du benchmark PLLM. Surcharge des sondes : 5.597 s de requêtes, 667 tokens de sortie, 783 de raisonnement, coût natif 0.003058452 (unité non exposée).

Benchmark PLLM distinct, avant métier : mode 1, Muse high, quotas utilisés 5 % / 67 % / 98 % ; palier 1024 incomplet puis succès 2048, TTFT 5.2226 s, débit global rapporté 2225.803 tokens/s. Ces valeurs ne remplacent pas les sondes.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 40 | 32.3 % |
| assistant | 84 | 67.7 % |
| Total | 124 | 100.0 % |

Le contrôleur a observé 39 user ; l’historique complet en contient 40, notamment le cadrage noReply. Le rapport retient l’historique natif complet.

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 117 | 26.1 % |
| step-start | 84 | 18.8 % |
| reasoning | 85 | 19.0 % |
| tool | 78 | 17.4 % |
| step-finish | 84 | 18.8 % |
| Total | 448 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
| --- | --- | --- |
| tool-calls | 46 | 54.8 % |
| stop | 38 | 45.2 % |
| Total | 84 | 100.0 % |

| Type d’outil | Total (part) | Achevé | Refus natif | Erreur technique |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 4 (5.1 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 17 (21.8 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 9 (11.5 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 26 (33.3 %) | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 7 (9.0 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 3 (3.8 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 2 (2.6 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (2.6 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (10.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 78 (100.0 %) | 78 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Les appels CAB/read/grep/glob sont des consultations ou transports ; ils ne constituent pas des décisions supplémentaires.

## 3. Fichiers modifiés

Il s’agit de tentatives d’écriture, pas d’un décompte de lignes. 8 écritures approuvées et exécutées sur 7 fichiers distincts, dont tasks.md deux fois après preuves.

| Chemin absolu de l’écriture | Nombre (part) | Approuvé et exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-handler-vocabulary-v1/.openspec.yaml | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-handler-vocabulary-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-handler-vocabulary-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-handler-vocabulary-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_job_handler.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_job_handler.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_job_handler_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 (100.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Les quatre artefacts OpenSpec ont été déplacés une fois depuis /home/devops/datas/pixs/openspec/changes/add-initial-bulk-job-handler-vocabulary-v1 vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-job-handler-vocabulary-v1. Leurs contenus ont été comparés avant/après archive. Le présent rapport ajoute un huitième fichier distinct après la borne de collecte. Les pyc régénérables de compilation et les répertoires temporaires des tests ne sont pas des sources nouvelles ; les répertoires temporaires de tests ont été nettoyés par leurs gestionnaires de contexte. Aucune façade, configuration, migration, source existante ou canon n’a été modifié dans les empreintes contrôlées.

## 4. Commandes

9 commandes approuvées et exécutées, 0 refus, 0 erreur native ; 7 exits 0 et 2 exits 1 distingués ci-dessus. Familles : prévol 1/9 (11.1 %), OpenSpec 5/9 (55.6 %), compilation 1/9 (11.1 %), unittest 2/9 (22.2 %), total 9/9 (100.0 %).

| Commande (100 caractères maximum) | Occurrences (part) | Approbation | Exit observé |
| --- | --- | --- | --- |
| /usr/bin/true | 1 (11.1 %) | 1 (100.0 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-job-handler-vocabulary-v1 --strict | 1 (11.1 %) | 1 (100.0 %) | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/bulk_job_handler.py tests/u… | 1 (11.1 %) | 1 (100.0 %) | 0 |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.ven… | 1 (11.1 %) | 1 (100.0 %) | 0 |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.ven… | 1 (11.1 %) | 1 (100.0 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate --all | 1 (11.1 %) | 1 (100.0 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 (22.2 %) | 2 (100.0 %) | 1, 1 |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-job-handler-vocabulary-v1 --yes | 1 (11.1 %) | 1 (100.0 %) | 0 |

Commandes refusées regroupées : aucune (0/9 ; 0.0 %). Les libellés longs sont tronqués volontairement ; les commandes exactes et leurs requestId figurent au checkpoint et dans l’historique natif. Aucune commande Git ni inspection Git n’a été exécutée.

## 5. Accès web

Outils web de la session de production : 0 ; approuvés 0, refusés 0, erreurs 0, taux N/A (dénominateur nul). Aucune URL n’a été visitée par un outil web ; aucune requête seule n’est transformée en preuve de visite.

Les communications techniques autorisées de prévol sont séparées des outils web de production : https://opencode.ai/zen/go/v1/usage (quotas), https://opencode.ai/zen/go/v1/models (disponibilité) et https://opencode.ai/zen/go/v1/responses (benchmark, modèle et sondes). Statut : autorisées par CISMP/PLLM ; aucun de ces accès n’est classé comme navigation web du codeur. Les API locales OpenCode/CAB transportent la session. Aucun secret, en-tête d’authentification ou contenu de secret n’est conservé ici.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 18/10/2026 20:11:01 Europe/Paris |
| Fin — après archivage | 18/10/2026 20:28:48 Europe/Paris |
| Durée globale (pauses et attentes incluses) | 00 h 17 min 47 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé consigné | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 18/10/2026 20:11:01 Europe/Paris | 18 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage de la spécification | 18/10/2026 20:28:48 Europe/Paris | 19 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | 1 point de pourcentage | — |

Source : mcp__codex_app__get_usage_limits, limitId=codex, windowDurationMins=10080, même compte et même resetsAt. Quotas partagés par le compte : cette variation peut inclure d’autres chats simultanés et ne constitue pas une consommation exclusive de CISMP1. La rédaction ultérieure du rapport est exclue de l’intervalle.

| Domaine | Total et part globale | Approuvé/exécuté au sens natif | Refusé | Erreur native |
| --- | --- | --- | --- | --- |
| Fichiers | 8 (10.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 9 (11.5 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 61 (78.2 %) | 61 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total global | 78 (100.0 %) | 78 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Coordination CAB de ce contexte : attente de ressource 0.000 s ; détention partagée 442.204 s ; activité exclusive 0.000 s ; promotion et réconciliation ciblée 0 ; aucun gel exceptionnel global. Le service signale une lacune historique de redémarrage commune ; elle n’est pas imputée à ce RUN. Les durées recouvrantes ne s’additionnent pas. Busy 494.235 s et idle 436.791 s sont des observations de session, sans preuve de productivité du modèle.

Tests 23/23 et compilation réussis ; archive unique vérifiée ; publication CAB référence 40 prouvée. Le strict global conserve exit 1 pour quatre warnings historiques, sans ERROR. Git non exécuté. Accès fournisseur nécessaires autorisés, valeurs de secrets restées dans le processus sécurisé ; aucune valeur exposée dans les preuves examinées. Le rapport doit être vérifié avant gate, désarmement, libération et arrêt ciblé CISMP1. Aucun prochain change ; cycle global Pixs toujours incomplet.
