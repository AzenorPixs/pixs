# Statistiques — add-initial-bulk-command-execution-outcome-v1

RUN `cismp4-pixs-7e2b943059504e46`, job `cismp4-job-34b6a30fbdd6`, session OpenCode `ses_eafa6c075ffeWYoC9KAijaPMbN`. Racine : /home/devops/datas/pixs. Archive : openspec/changes/archive/2026-10-18-add-initial-bulk-command-execution-outcome-v1.

Périmètre figé avant rédaction du présent rapport : session de production seule, complétée par deux sondes dédiées. Les actes de rédaction de ce rapport et de clôture sont exclus des totaux de cet intervalle ; ils ont leurs mandats distincts. Sources : historique natif OpenCode, agrégats CAB filtrés, checkpoint non secret et relevés natifs du tour.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte non exposée ; agent OpenCode 1.19.3 | OpenCode Go (opencode-go) | high | 0.903 s (n=1, sonde finale seule) | 537.3 (n=1, sonde finale seule) | N/A — périodes natives incluent outils et attentes, busy ne prouve pas la génération |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle précis non exposé | N/A — non exposée | OpenAI | N/A — non exposé | N/A — non exposé | N/A — non exposé | N/A — télémétrie de service non exposée |

Les identités proviennent des métadonnées natives réellement observées. Le modèle de codage reste identique aux sondes ; aucune version n’est déduite de son nom. Le temps de service cumulé et son dénominateur sont N/A : busy, durée calendaire et durée des outils ne sont pas du temps de génération. Aucun gain causal ni consommation exclusive ne sont calculés.

Sondes TTMT/débit : même prompt déterministe « entiers de 1 à 200 séparés par un espace, sans outil ni fichier ni réseau ». Prévues 2 (100.0 %), réussies/mesurables 1 (50.0 %), échouées pour la mesure 1 (50.0 %, initiale sans SSE capturé, TTMT non inféré), manquées 0 (0.0 %) ; aucune relève périodique échue, car fin avant 30 min. Finale : TTMT 0.903 s, 408 tokens sortie, 105 raisonnement, 50 deltas SSE, 1.771 s écoulées dont 0.759 s génération, 537.317 tokens/s. Surcharge native des 2 sondes, séparée des totaux : 24944 tokens SDK, 843 réponse, 722 raisonnement, coût API 0.002639826 (devise non exposée).

Benchmark PLLM distinct, avant métier : mode1, opencode-go muse-spark-1.3-contributor high, endpoint responses ; palier 1024 en RuntimeError sans détail, palier 2048 valide (1175 completion, 970 raisonnement, 4.9948 s, TTFT 4.5044 s, 2421.776 tokens/s) ; quotas rolling 0 %, weekly 67 %, monthly 98 % ; coût N/A. Une tentative préparatoire interrompue non prouvée reste distincte et n’est pas comptée comme preuve.

## 1. Statistiques générales et décisions

| Début | Fin | Durée globale (pauses et attentes incluses) |
| --- | --- | --- |
| 18/10/2026 20:47:29 Europe/Paris | 18/10/2026 21:12:17 Europe/Paris | 00 h 24 min 47 s |

Bornes natives CAB post-borne, distinctes du temps de service : 18:51:01 UTC – 19:14:00 UTC. Réservé 1379.205 s, busy 811.395 s, idle 564.191 s, inconnu natif 3.619 s. Attente ressource 79.354 s, détention partagée 666.654 s, exclusive 0.000 s, effet émis 4.963 s. Les durées recouvrantes ne s’additionnent pas ; busy n’est pas du temps de service.

Livraison : Enum passif BulkCommandExecutionOutcome APPLIED, REPLAYED, REJECTED dans src/pixs/backend, sans mixin str ni modification des validateurs et consommateurs str ; trois fichiers Python nouveaux ; archivage réussi prouvé.

| Décision CAB | Nombre | Part |
| --- | --- | --- |
| Approuvée | 22 | 91.7 % |
| Refusée | 2 | 8.3 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total décisions | 24 | 100.0 % |

Once 19. MCP request_validation completed 24 n’implique pas 24 approbations : 22 approved, 2 rejected ; 3 approved ont ensuite été refusées au natif avant effet, d’où 19 once. Historique maître complet : 104 outils, 101 terminés (97.1 %), 3 refus natifs (2.9 %), 0 erreur technique (0.0 %). Les 3 erreurs Bash brutes sont des refus explicites avant effet et non des pannes. Les 2 contrôles stricts en exit 1 sont des échecs de validation pour avertissements historiques, pas des erreurs de transport ; aucun strict success n’est revendiqué. Les chiffres sont figés avant rédaction du rapport ; son écriture, le gate et la clôture en sont exclus. Natifs bruts 104 outils / 140 messages contre agrégat CAB 103 outils / 136 messages depuis réservation : l’écart vient de l’initialisation avant réservation, sans addition des deux périmètres.

| Résultat du développement | Résultat observé |
| --- | --- |
| Compilation Python | 3 fichiers compilés, exit 0 |
| Tests ciblés et régressions | 36/36 réussis (100.0 %), 0 échec, 0 skip |
| OpenSpec ciblé strict | exit 0 ; skip_specs:true accepté sans delta |
| OpenSpec ciblé strict après cochage | exit 0 |
| OpenSpec global standard avant archive | 187 passed, 0 failed, exit 0 |
| Strict global avant archive | 185 passed, 2 failed, exit 1, 4 WARNING longueur et 0 ERROR |
| Archive | 1 exécution exit 0, 3 refus natifs avant effet, déplacement vérifié |
| Strict global après archive | 182 passed, 2 failed, exit 1, mêmes 4 WARNING et 0 ERROR |
| Publication CAB | publish-c4-044b4785d0f44783, référence 43, version 343, révisions 747/689/716/716/716/655/742 |
| Style/types | N/A — aucun contrôle dédié configuré |
| PostgreSQL / navigateur / build frontend | N/A — vocabulaire pur sans effet DB ni interface |

Avertissements préexistants : bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4], textes >500 caractères. Canons non modifiés.

| Mesure du quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 18/10/2026 20:47:29 Europe/Paris | 19 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage de la spécification | 18/10/2026 21:12:17 Europe/Paris | 28 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | +9 points de pourcentage | — |

Source : get_usage_limits, limitId codex, fenêtre 10080 min, même compte. Compte partagé par plusieurs RUN, aucune attribution exclusive à ce RUN.


| Télémétrie de production du codeur | Tokens | Part du total SDK |
| --- | ---: | ---: |
| Entrée non cachée | 434611 | 2.4 % |
| Réponse | 37467 | 0.2 % |
| Raisonnement | 13570 | 0.1 % |
| Cache lu | 17806011 | 97.3 % |
| Cache écrit | 0 | 0.0 % |
| Total SDK | 18291659 | 100.0 % |

Coût API OpenCode cumulé : 0.089280522 ; devise non exposée, aucune conversion ni assimilation à un montant en euros. Ces compteurs agrègent les 107 réponses de la session maîtresse ; les tokens de cache représentent des lectures cumulées, pas un volume unique de contexte. Coût et tokens de l’orchestrateur : N/A, non exposés. Compactions natives observées dans cet historique : 0 ; aucune échéance de 90 minutes atteinte.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 33 | 23.6 % |
| assistant | 107 | 76.4 % |
| Total natif complet | 140 | 100.0 % |

Agrégat CAB depuis réservation : 31 user + 105 assistant = 136. L’écart de 4 messages vient de l’initialisation avant réservation.

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 94 | 18.0 % |
| step-start | 107 | 20.5 % |
| reasoning | 110 | 21.1 % |
| tool | 104 | 19.9 % |
| step-finish | 107 | 20.5 % |
| Total | 522 | 100.0 % |

| Terminaison des réponses | Nombre | Part |
| --- | --- | --- |
| tool-calls | 79 | 73.8 % |
| stop | 28 | 26.2 % |
| Total | 107 | 100.0 % |

| Type d’outil | Total (part) | Achevé | Refus natif | Erreur technique |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 6 (5.8 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 (1.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (1.9 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 24 (23.1 %) | 24 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 14 (13.5 %) | 11 (78.6 %) | 3 (21.4 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 (1.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| todowrite | 4 (3.8 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 29 (27.9 %) | 29 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 10 (9.6 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 5 (4.8 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (7.7 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 104 (100.0 %) | 101 (97.1 %) | 3 (2.9 %) | 0 (0.0 %) |

Les appels CAB, read, glob, grep et todowrite sont des consultations ou transports ; ils ne constituent pas des décisions supplémentaires. Agrégat CAB : cab-mcp 33 completed, bash 11 completed et 3 error (refus avant effet), other 4, read 29, glob 10, grep 5, write 8, soit 103 outils depuis réservation ; le 104e est l’initialisation avant réservation.

## 3. Fichiers modifiés

Il s’agit de tentatives d’écriture, pas d’un décompte de lignes. 8 écritures réussies sur 7 chemins uniques, dont tasks.md écrit 2 fois après preuves.

| Chemin absolu de l’écriture | Nombre (part) | Approuvé et exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-command-execution-outcome-v1/.openspec.yaml | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-command-execution-outcome-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-command-execution-outcome-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-command-execution-outcome-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_command_execution_outcome.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_command_execution_outcome.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_command_execution_outcome_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 (100.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Les quatre artefacts OpenSpec ont été archivés depuis openspec/changes/add-initial-bulk-command-execution-outcome-v1 vers openspec/changes/archive/2026-10-18-add-initial-bulk-command-execution-outcome-v1, contenu exact vérifié avant et après déplacement. Le présent rapport ajoute un huitième chemin distinct après la borne de collecte. Les pyc régénérables et les sondes temporaires ne sont pas des sources nouvelles. Aucune façade, configuration, migration, source existante ou canon n’a été modifiée. Git non inspecté et non modifié.

## 4. Commandes

14 appels Bash natifs, 11 exécutés et 3 refusés avant effet. Deux refus CAB avant invocation sont présentés séparément. « Exécuté » décrit l’effet natif ; les deux contrôles stricts globaux restent en exit 1.

| Famille | Appels et part | Exécutés et taux | Refusés et taux | Erreurs techniques et taux |
| --- | ---: | ---: | ---: | ---: |
| Prévol | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilations Python | 3 (21.4 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec ciblé strict | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec global standard | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec global strict | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archivage | 4 (28.6 %) | 1 (25.0 %) | 3 (75.0 %) | 0 (0.0 %) |
| Total | 14 (100.0 %) | 11 (78.6 %) | 3 (21.4 %) | 0 (0.0 %) |

| Commande (100 caractères maximum) | Appels et part | Exécutés et taux | Refusés et taux |
| --- | ---: | ---: | ---: |
| /usr/bin/true | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-command-execution-outcome… | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_command_execution_out… | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_command_execution_outc… | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_command_executi… | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_… | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-command-execution-outcome-v1 --yes --… | 4 (28.6 %) | 1 (25.0 %) | 3 (75.0 %) |
| Total | 14 (100.0 %) | 11 (78.6 %) | 3 (21.4 %) |

Refus natifs regroupés :

| Commande refusée (≤100 caractères) | Occurrences et part des refus natifs | Cause et effet |
| --- | ---: | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-command-execution-outcome-v1 --yes --… | 3 (100.0 %) | STALE/FIFO avant once ; aucune exécution |
| Total | 3 (100.0 %) | Aucun effet |

Refus CAB avant invocation, sans appel Bash :

| Commande (≤100 caractères) | Occurrences et part de ces refus CAB | Motif |
| --- | ---: | --- |
| /home/devops/.local/npm/bin/openspec validate --all | 1 (50.0 %) | Révision devenue périmée |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-command-execution-outcome-v1 --yes --… | 1 (50.0 %) | Manifeste transmis divergent |
| Total | 2 (100.0 %) | Aucun effet |

Les cinq refus représentent des essais distincts. Aucun refus de permission n’est une erreur technique. Commandes exactes, identifiants et preuves figurent dans le checkpoint et l’historique natif. Aucune commande Git.

## 5. Accès web

| Outils web natifs | Total | Approuvés | Refusés | Erreurs | Part |
| --- | --- | --- | --- | --- | --- |
| Visites et requêtes projet | 0 | 0 | 0 | 0 | N/A (dénominateur nul) |

Outils web de production : 0 URL visitée, 0 requête. Les accès HTTP loopback locaux OpenCode et CAB, ainsi que les API du fournisseur pour sondes et benchmark (usage et responses sur le domaine du fournisseur), sont distincts du web du projet et ne sont pas comptés comme navigation web du codeur, d’autant que les outils web natifs sont absents. Aucune requête seule n’est transformée en preuve de visite.

API externes du prévol PLLM, autorisées par le prompt et distinctes des outils web de production :

| URL (moins de 100 caractères) | Statut observé | Décompte exhaustif |
| --- | --- | --- |
| https://opencode.ai/zen/go/v1/usage | Approuvé et consulté pour les quotas | N/A — une tentative préparatoire interrompue empêche un total exhaustif |
| https://opencode.ai/zen/go/v1/responses | Approuvé et utilisé pour le benchmark en flux | Un succès prouvé au palier 2048 ; essai 1024 non concluant distinct |

Aucune URL de navigation refusée. Les API locales et les appels serveur du fournisseur ne sont pas inventés dans les 104 outils de production.

## 6. Synthèse globale

| Mesure du quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 18/10/2026 20:47:29 Europe/Paris | 19 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage de la spécification | 18/10/2026 21:12:17 Europe/Paris | 28 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | +9 points de pourcentage | — |

Source : get_usage_limits, limitId codex, fenêtre 10080 min, même compte. Compte partagé par plusieurs RUN, aucune attribution exclusive à ce RUN.


| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 18/10/2026 20:47:29 Europe/Paris |
| Fin — après archivage, avant rapport | 18/10/2026 21:12:17 Europe/Paris |
| Durée globale (pauses et attentes incluses) | 00 h 24 min 47 s |

| Domaine | Total et part globale | Approuvé/exécuté au sens natif | Refusé | Erreur native |
| --- | --- | --- | --- | --- |
| Fichiers | 8 (7.7 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 14 (13.5 %) | 11 (78.6 %) | 3 (21.4 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 82 (78.8 %) | 82 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total global | 104 (100.0 %) | 101 (97.1 %) | 3 (2.9 %) | 0 (0.0 %) |

Coordination CAB de ce contexte : attente 79.354 s, détention partagée 666.654 s, exclusive 0.000 s, effet émis 4.963 s, 1 révision périmée HTTP sans effet métier, 0 gel global. Idle 564.191 s et busy 811.395 s sont des observations de session, sans preuve de productivité du modèle.

Tests 36/36 et compilation réussis ; archive unique vérifiée ; publication CAB reçue (transaction publish-c4-044b4785d0f44783). Le strict global conserve exit 1 pour quatre avertissements historiques, sans ERROR. Archivage réussi, statistiques du fichier courant préparées avant gate, Git non inspecté et non modifié. Aucun secret transmis au modèle, affiché ou écrit dans les sources ; seuls les processus sécurisés de vérification PLLM ont accédé aux valeurs d’authentification nécessaires. Cadrages cohérents dans le périmètre : pure fondation sans preuve P0 ni profil runtime ; README porte un relevé daté du 17 octobre et n’a pas été actualisé hors périmètre. Livraison finale en attente du gate au gel du présent rapport ; aucun gate futur n’est revendiqué.

Après le gel des compteurs de production, le seul rapport a nécessité une correction de forme puis une récupération CAB contrôlée vers la session ses_eaf874348ffep7LIQJf2cUN23i. Le prévol /usr/bin/true exact a été prouvé sous once, exit 0 puis READY, avant cette correction finale. Les effets sont limités à ce rapport, sans réarchivage. Les actes de rédaction, correction, récupération et clôture restent exclus des compteurs de production figés ci-dessus.
