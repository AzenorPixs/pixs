# STATISTIQUES — C01 : provider systemd et audit d’amorçage

Change : `add-pbo-runtime-secret-provider`. RUN : `cismp3-pixs-ab58d92936e94d41`. Contexte CAB : `324`. Session de production : `ses_eafa73500ffeLMpuUnHlZObNId`. Archive : `/home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider`. Publication technique : référence **47**, transaction `publish-5bc02705e72a4922aab75e692695ef63`.

Collecte native figée à **19/10/2026 06:18:58 Europe/Paris**, après archive, dernière correction et sonde finale. La rédaction du présent rapport, ses validations, la supervision ultérieure et le gate sont hors de ces comptes. Les sondes sont séparées de la production. Le rapport est assemblé par fragments vérifiés dans son seul fichier, sans fichier auxiliaire. Le temps calendaire inclut pauses et attentes.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | Modèle N/A ; OpenCode 1.19.3 | OpenCode Go (opencode-go) | high | 1,913 s (19 sondes) | 504,883 tokens/s (19 sondes) | N/A — génération non isolée |
| Même modèle, résumés natifs | Modèle N/A ; OpenCode 1.19.3 | OpenCode Go | N/A — API de compactage sans variant | N/A — non sondés séparément | N/A — usage incomplet | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex (famille GPT-6) | N/A — version exacte non exportée | OpenAI | N/A — non exporté | N/A — aucune sonde orchestrateur | N/A — télémétrie non consolidée | N/A — dénominateur total inconnu |

Les versions exactes des modèles ne sont pas déduites de leurs noms. Les 952 réponses de production high et les trois résumés natifs proviennent du même codeur, sans autre modèle de codage observé. Le temps busy CAB et les durées de messages incluant outils/attentes ne sont pas du temps de génération ; aucun pourcentage de service global fiable n’est disponible.

## 1. Statistiques générales et décisions

Sources : historique HTTP persistant OpenCode de la session identifiée, état natif des outils et fins de commandes, agrégats CAB filtrés au contexte 324, sondes dédiées et relevés natifs de quota. Les sorties brutes et corps de messages ne sont pas recopiés. L’historique complet de l’orchestrateur n’est pas exportable dans la limite de taille de read_thread : ses compteurs exhaustifs restent N/A.

Convention A/R/E : A = appel réussi, autorisé automatiquement ou explicitement ; R = refus natif explicite ; E = erreur technique/interruption ou commande dont le code de sortie est non nul. Une consultation MCP réussie ou une demande d’approbation terminée ne prouve pas une exécution métier, ni une validation humaine. Les annulations de demandes non admises restent distinctes des refus.

| Catégorie | Total (% tableau) | Réussis A (% ligne) | Refusés R (% ligne) | Erreurs E (% ligne) |
| --- | --- | --- | --- | --- |
| Tous les outils natifs du codeur | 657 (100,0 %) | 625 (95,1 %) | 1 (0,2 %) | 31 (4,7 %) |
| TOTAL | 657 (100 %) | 625 (95,1 %) | 1 (0,2 %) | 31 (4,7 %) |

| Mesure de développement | Résultat |
| --- | --- |
| Tests unitaires globaux | 1 945 réussis, exit 0 ; 16,630 s |
| Correctifs natifs et récupération | 26 tests ciblés réussis, exit 0 |
| Harnais fonctionnel réel | 12 événements stricts et reçus vérifiés ; v1/v2, rotation, révocation et unités absentes |
| Canons synchronisés | 5 capacités ; 28 exigences ajoutées, 1 modifiée ; autres blocs préservés |
| OpenSpec C01 ciblé strict | exit 0 |
| OpenSpec global standard avant archive | 184 passés, 0 échec ; exit 0 |
| Strict global avant archive | 182 passés, 2 échecs sur 184 ; 4 warnings de longueur hors C01, 0 ERROR ; exit 1 |
| Strict global après archive | 181 passés, 2 échecs sur 183 ; mêmes 4 warnings hors C01, 0 ERROR ; exit 1 |
| Archive unique | c3-cmd-8bf41e4e-effect, once natif et exit 0 ; --skip-specs car synchronisation déjà prouvée |
| Format de proposition | Avertissement non bloquant à l’archive ; deux en-têtes standard corrigés ensuite sous mandat, sans réarchive |

Les warnings globaux concernent bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4]. Le strict global n’est pas présenté comme réussi. Le mode null du harnais prouve le transport fonctionnel avec fixtures publiques, pas la confidentialité ou l’authenticité du chiffrement en production ; aucune conformité P0/C05/C08 n’en découle.

| Champ natif de consommation, production seule | Valeur exposée |
| --- | --- |
| total | 337 144 406 |
| input | 7 075 348 |
| output | 467 728 |
| reasoning | 179 533 |
| cache_read | 329 421 797 |
| cache_write | 0 |
| Coût natif OpenCode, compteur déclaré | 1.495830594 |
| Facturation réelle / conversion monétaire | N/A — non fournie par ce compteur |
| Usage des 3 compactages natifs | N/A — total absent ; champs à zéro non traités comme mesure réelle |

Les compteurs input, output, reasoning et cache sont présentés selon leurs champs natifs. Le total disponible est partiel : trois résumés n’exposent pas de total. Le coût est le compteur déclaré par OpenCode, sans prétendre à une facture ni à un débit du compte. PLLM mode 1 a été maintenue sur instruction explicite, y compris la dérogation mensuelle à 100 % sur fonds propres ; aucune opération d’achat, recharge ou reset n’est effectuée par ce RUN.

| Décisions CAB du contexte, instantané 19/10/2026 06:22:35 Europe/Paris | Nombre | Part |
| --- | --- | --- |
| approved | 139 | 99,3 % |
| rejected | 1 | 0,7 % |
| needs_clarification | 0 | 0,0 % |
| pending | 0 | 0,0 % |
| TOTAL | 140 | 100 % |
| Permissions once (autre dénominateur) | 136 | N/A — suivi distinct |

Cet instantané CAB est postérieur à la borne de collecte et n’est pas substitué aux comptes natifs bornés. Les demandes d’archive non admises (manifeste divergent puis révision non déclarée) ont été annulées avant décision/effet ; elles ne sont pas des archives exécutées. Les erreurs MCP d’avant admission ne sont pas nécessairement dans le compteur de décisions du contrôleur.

| Coordination CAB cumulée, non additive | Durée / compte |
| --- | --- |
| availableFrom (borne native) | 18/10/2026 20:49:24 Europe/Paris |
| resourceWaitMs | 50,528 s |
| sharedHeldMs | 5 686,805 s |
| exclusiveActiveMs | 0 s |
| issuedEffectMs | 113,327 s |
| promotionWaitMs | 0 s |
| reconciliationMs | 0 s |
| reconciliationCount | 0 |

Ces compteurs ont leur propre borne availableFrom et peuvent se recouvrir ; ils ne donnent ni temps productif ni taux de service des modèles. Aucune exclusion globale n’a été utilisée pour publier C01.

Trois résumés natifs OpenCode sont prouvés : 18/10/2026 22:17:36 Europe/Paris (`msg_150a9771c0015TmYC6cP4DKyKI`) ; 18/10/2026 23:59:03 Europe/Paris (`msg_151062c32001k8GvGZIadlYV5g`) ; 19/10/2026 05:18:21 Europe/Paris (`msg_1522a9234001F4XmmEsxJ2xx4k`). Le compactage natif de l’orchestrateur est N/A (API absente). Des échéances ont été différées pendant les attentes humaines ; aucun succès rétroactif n’est fabriqué.

### Sondes du codeur et surcharge de télémétrie

Prompt constant : « Écris exactement les nombres de 0001 à 0120, un nombre par ligne, sans introduction, sans outil et sans autre texte. ». Chaque relève a une session dédiée, le même modèle/provider/high, aucun outil et un format de 120 lignes vérifié. TTMT comparable = réception native du message utilisateur → premier événement texte ; le premier envoi client est absent et les sent_at périodiques précèdent la préparation de session, donc les moyennes utilisent uniquement la borne native homogène. Débit = tokens output natifs / durée premier–dernier texte ; il ne comprend pas les tokens de raisonnement. Ce sont les horodatages OpenCode, pas une horloge de chaque token fournisseur.

| Relève | Réception native (Paris) | TTMT natif (s) | Tokens output | Débit (tokens/s) | État |
| --- | --- | --- | --- | --- | --- |
| début | 18/10/2026 20:47:34 Europe/Paris | 1,654 | 368 | 523,471 | Valide sans outil |
| +60 min | 18/10/2026 21:47:34 Europe/Paris | 1,171 | 368 | 404,84 | Valide sans outil |
| +90 min | 18/10/2026 22:17:34 Europe/Paris | 2,589 | 396 | 555,4 | Valide sans outil |
| +120 min | 18/10/2026 22:47:34 Europe/Paris | 1,54 | 368 | 508,287 | Valide sans outil |
| +150 min | 18/10/2026 23:17:34 Europe/Paris | 2,903 | 389 | 358,856 | Valide sans outil |
| +180 min | 18/10/2026 23:47:34 Europe/Paris | 1,39 | 368 | 960,836 | Valide sans outil |
| +210 min | 19/10/2026 00:17:34 Europe/Paris | 1,175 | 368 | 500 | Valide sans outil |
| +240 min | 19/10/2026 00:47:34 Europe/Paris | 1,753 | 368 | 650,177 | Valide sans outil |
| +270 min | 19/10/2026 01:17:34 Europe/Paris | 2,26 | 368 | 450,98 | Valide sans outil |
| +300 min | 19/10/2026 01:47:34 Europe/Paris | 1,741 | 368 | 400 | Valide sans outil |
| +330 min | 19/10/2026 02:17:34 Europe/Paris | 1,593 | 368 | 625,85 | Valide sans outil |
| +360 min | 19/10/2026 02:47:34 Europe/Paris | 2,027 | 368 | 400,435 | Valide sans outil |
| +390 min | 19/10/2026 03:17:34 Europe/Paris | 1,912 | 368 | 504,801 | Valide sans outil |
| +420 min | 19/10/2026 03:47:34 Europe/Paris | 1,692 | 368 | 631,218 | Valide sans outil |
| +450 min | 19/10/2026 04:17:34 Europe/Paris | 3,095 | 390 | 478,528 | Valide sans outil |
| +480 min | 19/10/2026 04:47:34 Europe/Paris | 2,39 | 368 | 361,493 | Valide sans outil |
| +510 min | 19/10/2026 05:17:34 Europe/Paris | 1,64 | 368 | 471,191 | Valide sans outil |
| +540 min | 19/10/2026 05:47:34 Europe/Paris | 1,937 | 388 | 478,422 | Valide sans outil |
| fin | 19/10/2026 06:17:11 Europe/Paris | 1,883 | 368 | 327,986 | Valide sans outil |
| +30 min | 18/10/2026 21:17:34 Europe/Paris | N/A | N/A | N/A | Manquée : non reconstruite |

| Bilan des sondes | Nombre | Part prévue |
| --- | --- | --- |
| Prévues | 20 | 100 % |
| Valides | 19 | 95,0 % |
| Échouées / invalides | 0 | 0,0 % |
| Manquées | 1 | 5,0 % |

Moyennes arithmétiques : TTMT 1,913 s, débit 504,883 tokens/s. Min–max : 1,171–3,095 s et 327,986–960,836 tokens/s. Surcharge séparée : 7 083 tokens output, 233 494 tokens totaux natifs et coût déclaré 0.022032544. La cadence a aussi produit des sondes pendant la pause humaine ; ces sessions ne sont pas du codage productif. La collecte périodique est close après la sonde finale.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 440 | 31,5 % |
| assistant | 955 | 68,5 % |
| TOTAL | 1 395 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 1 228 | 25,4 % |
| step-start | 955 | 19,7 % |
| reasoning | 1 042 | 21,5 % |
| tool | 657 | 13,6 % |
| step-finish | 953 | 19,7 % |
| compaction | 3 | 0,1 % |
| TOTAL | 4 838 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 562 | 58,8 % |
| stop | 391 | 40,9 % |
| erreur sans finish | 2 | 0,2 % |
| TOTAL | 955 | 100 % |

| Catégorie | Total (% tableau) | Réussis A (% ligne) | Refusés R (% ligne) | Erreurs E (% ligne) |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 101 (15,4 %) | 101 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 89 (13,5 %) | 89 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_propose_approval | 1 (0,2 %) | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) |
| cgpt-validation_request_validation | 147 (22,4 %) | 131 (89,1 %) | 0 (0,0 %) | 16 (10,9 %) |
| bash | 90 (13,7 %) | 80 (88,9 %) | 1 (1,1 %) | 9 (10,0 %) |
| cgpt-validation_get_approval | 16 (2,4 %) | 16 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| todowrite | 2 (0,3 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 91 (13,9 %) | 91 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| glob | 10 (1,5 %) | 10 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 36 (5,5 %) | 36 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 46 (7,0 %) | 45 (97,8 %) | 0 (0,0 %) | 1 (2,2 %) |
| cgpt-validation_poll_approval | 10 (1,5 %) | 7 (70,0 %) | 0 (0,0 %) | 3 (30,0 %) |
| cgpt-validation_cancel_approval | 5 (0,8 %) | 4 (80,0 %) | 0 (0,0 %) | 1 (20,0 %) |
| grep | 9 (1,4 %) | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| edit | 2 (0,3 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_remediation_registry | 1 (0,2 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_auto_remediation_policy | 1 (0,2 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| TOTAL | 657 (100 %) | 625 (95,1 %) | 1 (0,2 %) | 31 (4,7 %) |

## 3. Fichiers modifiés

Tentatives d’écriture identifiées par les outils write/edit et les commandes de copie relue (payload lié à un chemin et SHA). Les lectures ne sont pas des modifications. Le remappage du dossier actif vers l’archive regroupe les tentatives sur le même fichier logique ; le déplacement CLI reste une commande distincte. Les écritures implicites des tests/cache/fixtures ne sont pas intégralement instrumentées par fichier et ne sont pas présentées comme absentes.

| Catégorie | Total (% tableau) | Réussis A (% ligne) | Refusés R (% ligne) | Erreurs E (% ligne) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/.openspec.yaml | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/design.md | 4 (5,3 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/PREUVES-C01.json | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md | 5 (6,6 %) | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/requirements.md | 5 (6,6 %) | 4 (80,0 %) | 0 (0,0 %) | 1 (20,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/specs/audit/spec.md | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/specs/authorization/spec.md | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/specs/initial-administration/spec.md | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/specs/reference-composition/spec.md | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/specs/secrets-providers/spec.md | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-19-add-pbo-runtime-secret-provider/tasks.md | 3 (3,9 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/audit/spec.md | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/authorization/spec.md | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/initial-administration/spec.md | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/reference-composition/spec.md | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/secrets-providers/spec.md | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bootstrap_audit.py | 4 (5,3 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bootstrap_policy.py | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/runtime_resolve.py | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/systemd_secret_provider/__init__.py | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/systemd_secret_provider/component.toml | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/systemd_secret_provider/lifecycle.py | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/systemd_secret_provider/native.py | 5 (6,6 %) | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/systemd_secret_provider/provider.py | 4 (5,3 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_c01_systemd_harness.py | 3 (3,9 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bootstrap_audit.py | 3 (3,9 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bootstrap_policy.py | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_c01_harness_controls.py | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_runtime_resolve.py | 1 (1,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_systemd_lifecycle.py | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_systemd_native.py | 5 (6,6 %) | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_systemd_provider.py | 4 (5,3 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| TOTAL | 76 (100 %) | 75 (98,7 %) | 0 (0,0 %) | 1 (1,3 %) |

Nombre de chemins logiques après remappage : 33. Les contenus source/canons et preuves ont été vérifiés par SHA et UTF-8/LF. Le présent STATISTIQUES.md est créé après la borne, sous son mandat distinct, puis vérifié avant gate ; son écriture n’est pas comptée rétroactivement dans ce tableau.

## 4. Commandes

| Catégorie | Total (% tableau) | Réussis A (% ligne) | Refusés R (% ligne) | Erreurs E (% ligne) |
| --- | --- | --- | --- | --- |
| Prévol sans effet | 11 (12,2 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| OpenSpec — validation ciblée | 5 (5,6 %) | 4 (80,0 %) | 0 (0,0 %) | 1 (20,0 %) |
| Python — syntaxe | 13 (14,4 %) | 13 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python — tests par découverte | 8 (8,9 %) | 6 (75,0 %) | 0 (0,0 %) | 2 (25,0 %) |
| Diagnostic et vérification systemd | 11 (12,2 %) | 9 (81,8 %) | 1 (9,1 %) | 1 (9,1 %) |
| Autres commandes | 1 (1,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python — tests ciblés | 6 (6,7 %) | 5 (83,3 %) | 0 (0,0 %) | 1 (16,7 %) |
| Python — copie de contenu relu | 28 (31,1 %) | 28 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Harnais / barrière de privilège | 3 (3,3 %) | 1 (33,3 %) | 0 (0,0 %) | 2 (66,7 %) |
| OpenSpec — standard global | 1 (1,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| OpenSpec — strict global | 2 (2,2 %) | 0 (0,0 %) | 0 (0,0 %) | 2 (100,0 %) |
| OpenSpec — archivage | 1 (1,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| TOTAL | 90 (100 %) | 80 (88,9 %) | 1 (1,1 %) | 9 (10,0 %) |

### Commandes refusées

| Libellé (100 caractères maximum) | Occurrences | Part des refus |
| --- | --- | --- |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import json,os,runpy; h=runpy.run_path("/home/devo… | 1 | 100,0 % |

Un refus natif explicite de commande reformattée est distingué des erreurs techniques. Les exits non nuls de tests, validations strictes ou sudo sont des E, pas des refus de permission. La première commande sudo -n a échoué avant lancement ; l’exécution root manuelle ultérieure n’a pas de fin d’outil OpenCode et n’est pas inventée dans ces comptes. Le succès métier est établi par les reçus et leur vérification indépendante.

## 5. Accès web

| Catégorie | Total (% tableau) | Réussis A (% ligne) | Refusés R (% ligne) | Erreurs E (% ligne) |
| --- | --- | --- | --- | --- |
| Outils web du codeur | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| TOTAL | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web natif du codeur n’est observé. L’orchestrateur a consulté des sources primaires ; ses totaux exhaustifs et pourcentages A/R/E sont N/A faute d’un export complet des appels. Aucun refus web n’est identifié dans le relevé disponible, ce qui ne prouve pas un taux global nul. Les URL ci-dessous sont des références consultées/utilisées (liste non exhaustive), distinctes des requêtes de recherche sans URL ouverte. Les libellés URL sont limités à 100 caractères.

| URL / statut de la référence disponible | Statut |
| --- | --- |
| [https://systemd.io/CREDENTIALS/](https://systemd.io/CREDENTIALS/) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/systemd/systemd.service.5.en.html](https://manpages.debian.org/trixie/systemd/systemd.service.5.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/systemd/systemd-creds.1.en.html](https://manpages.debian.org/trixie/systemd/systemd-creds.1.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/systemd/systemd-run.1.en.html](https://manpages.debian.org/trixie/systemd/systemd-run.1.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/systemd/busctl.1.en.html](https://manpages.debian.org/trixie/systemd/busctl.1.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/manpages-dev/fsync.2.en.html](https://manpages.debian.org/trixie/manpages-dev/fsync.2.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/manpages-dev/flock.2.en.html](https://manpages.debian.org/trixie/manpages-dev/flock.2.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://www.freedesktop.org/software/systemd/man/latest/sd_pid_get_unit.html](https://www.freedesktop.org/software/systemd/man/latest/sd_pid_get_unit.html) | Consultée/utilisée par l’orchestrateur |
| [https://raw.githubusercontent.com/systemd/systemd/v257/src/core/exec-credential.c](https://raw.githubusercontent.com/systemd/systemd/v257/src/core/exec-credential.c) | Consultée/utilisée par l’orchestrateur |
| [https://raw.githubusercontent.com/systemd/systemd/v257/src/core/dbus-execute.c](https://raw.githubusercontent.com/systemd/systemd/v257/src/core/dbus-execute.c) | Consultée/utilisée par l’orchestrateur |
| [https://manpages.debian.org/trixie/libsystemd-dev/sd_bus_call_method.3.en.html](https://manpages.debian.org/trixie/libsystemd-dev/sd_bus_call_method.3.en.html) | Consultée/utilisée par l’orchestrateur |
| [https://cdn.kernel.org/doc/html/latest/userspace-api/no_new_privs.html](https://cdn.kernel.org/doc/html/latest/userspace-api/no_new_privs.html) | Consultée/utilisée par l’orchestrateur |
| [https://www.freedesktop.org/software/systemd/man/257/org.freedesktop.systemd1.html](https://www.freedesktop.org/software/systemd/man/257/org.freedesktop.systemd1.html) | Consultée/utilisée par l’orchestrateur |
| [https://www.freedesktop.org/software/systemd/man/257/systemctl.html](https://www.freedesktop.org/software/systemd/man/257/systemctl.html) | Consultée/utilisée par l’orchestrateur |

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 18/10/2026 20:46:56 Europe/Paris |
| Fin — après archivage | 19/10/2026 06:18:58 Europe/Paris |
| Durée globale (pauses et attentes incluses) | 09 h 32 min 01 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 18/10/2026 20:46:56 Europe/Paris | 19 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage de la spécification | 19/10/2026 06:18:58 Europe/Paris | 49 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | N/A | — |

Le quota est partagé par le compte et peut inclure d’autres tâches. Les deux relevés natifs sont codex, fenêtre 10 080 minutes et même resetsAt ; l’identifiant de compte initial n’a pas été conservé et la tentative de lecture historique dépasse la taille exportable. La comparaison du compte n’est donc pas certifiée : différence N/A, sans attribution exclusive à CISMP3. Le premier relevé est conservé, non recréé.

| Catégorie | Total (% tableau) | Réussis A (% ligne) | Refusés R (% ligne) | Erreurs E (% ligne) |
| --- | --- | --- | --- | --- |
| Autres outils | 519 (79,0 %) | 498 (96,0 %) | 0 (0,0 %) | 21 (4,0 %) |
| Commandes Bash | 90 (13,7 %) | 80 (88,9 %) | 1 (1,1 %) | 9 (10,0 %) |
| Fichiers — outils natifs | 48 (7,3 %) | 47 (97,9 %) | 0 (0,0 %) | 1 (2,1 %) |
| TOTAL | 657 (100 %) | 625 (95,1 %) | 1 (0,2 %) | 31 (4,7 %) |

Les domaines du tableau global sont exclusifs par type d’outil. Les vues fichiers et commandes se recouvrent pour les copies Bash ; elles ne sont pas additionnées deux fois au total global. Les outils orchestrateur et interventions manuelles ne sont pas intégrés à ce dénominateur natif incomplet pour l’ensemble du travail.

État observé à la rédaction : C01 implémenté, 1 945 tests passants, transport fonctionnel qualifié avec données publiques, archive effective et publication technique référence 47. Les quatre warnings de longueur hors C01 du strict global restent signalés (exit 1), sans ERROR. Aucun état Git, commit, push ou branche n’a été inspecté/modifié par ce RUN. Aucune valeur de secret réel n’est livrée ; clé hôte non créée par le harnais, aucun accès base/session métier et aucune disponibilité P0 revendiquée. Les fichiers incertains et journaux de test sont conservés.

Ce rapport est contrôlé après écriture (six sections, UTF-8/LF, SHA et totaux), puis le gate, le désarmement et la libération du seul RUN sont exécutés. Leur preuve terminale est conservée dans `/home/devops/datas/pixs/output/cismp/cismp3-pixs-ab58d92936e94d41/state.json`. Le cycle CISMP global reste incomplet (`cycle_global_complete=false`) ; aucun change suivant n’est sélectionné et les services partagés restent disponibles.
