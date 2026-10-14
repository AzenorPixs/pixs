# Statistiques — add-initial-identity-assurance-vocabulary-v1

RUN : cismp-pixs-01a1387f5b20. Sessions natives : ses_ec6d5f766ffe35M3GmI99EjFwc, ses_ec6979152ffeRQs2qumn027ivs. Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-initial-identity-assurance-vocabulary-v1.

Collecte de tout l’historique natif de ces deux sessions jusqu’au relevé final après archive. Le présent rapport, son écriture et les contrôles de clôture ultérieurs sont hors de cet intervalle. Les sources documentaires fournies en message ne sont pas comptées comme des lectures par outil. Les sondes jetables sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte non fournie | OpenCode Go | high | 4.919 s | 272.087 | 00 h 06 min 32 s observables ; part N/A |
| muse-spark-1.3-contributor | N/A — version exacte non fournie | OpenCode Go | N/A — compactions | N/A — non sondé | N/A — non sondé | 00 h 00 min 22 s observables ; part N/A |

OpenCode 1.19.0 est la version de l’agent, pas celle du modèle. Le temps ci-dessus additionne l’union des intervalles natifs des parties texte/raisonnement ; sa couverture peut être partielle. Aucun temps d’outil ou d’attente de permission n’y est ajouté. Le temps de l’orchestrateur manque : dénominateur cumulé complet et part N/A. Les compactions natives utilisent le même modèle/fournisseur ; leur niveau de raisonnement n’est pas attesté dans les métadonnées, donc N/A pour ces messages.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact N/A | N/A | OpenAI | N/A | N/A — aucune sonde orchestrateur | N/A | N/A — télémétrie de génération absente |

## 1. Statistiques générales et décisions

Durée globale : 02 h 00 min 43 s (pauses, capacité fournisseur, reprises et attentes incluses). Résultats : 98 tests réussis (100 % des 98 tests de qualification/régression exécutés avec le bon chemin source), deux compilations réussies (100 %), quatre artefacts OpenSpec et deux fichiers de tests, production et façades inchangées, archive réussie. L’échec initial de chargement du test (1 erreur d’import) reste conservé ; il ne fait pas partie des 98 tests réussis.

| Mesure | Nombre et part |
| --- | --- |
| Messages | 245 (100.0 %) |
| Appels d’outils natifs | 118 (100.0 %) |
| Outils achevés | 109 (92.4 %) |
| Refus explicites | 1 (0.8 %) |
| Erreurs techniques d’outil | 8 (6.8 %) |
| Compactions natives | 2 (0.2 %) |

Convention : un appel natif terminé en succès est « achevé », sans prouver une approbation manuelle ; les décisions CAB sont distinguées ci-dessous. Un refus est une décision REJECTED explicite. Une expiration/annulation technique sans rejet compte en erreur d’outil lorsqu’elle interrompt l’appel. Un Bash achevé peut avoir un code non nul : ce résultat de validation est présenté séparément, sans le transformer en succès du contrôle.

| Décision CAB unique | Nombre et part |
| --- | --- |
| APPROVED | 24 (92.3 %) |
| CANCELLED | 1 (3.8 %) |
| REJECTED | 1 (3.8 %) |
| Total | 26 (100.0 %) |

Une ancienne création approuvée n’a pas été exécutée (outil indisponible) : permission non consommée invalidée par récupération native de session. Une demande suivante non enregistrée au contrôleur a été annulée, sans Bash ni fichier ; un mandat de validation divergent read/write a été refusé avant exécution. Le prévol neuf, les mandats ultérieurs et leurs permissions once ont été réconciliés. Aucun refus n’est présenté comme une exécution.

| Compteur natif | Valeur | Part des tokens total |
| --- | --- | --- |
| input | 1247947 | 12.9 % |
| output | 47597 | 0.5 % |
| reasoning | 29298 | 0.3 % |
| cache_read | 8377269 | 86.3 % |
| cache_write | 0 | 0.0 % |
| total | 9702111 | 100.0 % |

Coût natif cumulé : 0.156928238 pour 152 messages disposant du champ cost ; unité monétaire non attestée, conversion N/A. Tokens/cache/coût agrégés depuis les champs natifs, sans attribution exclusive au compte.

| Configuration observée | Messages et part |
| --- | --- |
| muse-spark-1.3-contributor / opencode-go / N/A | 2 (1.3 %) |
| muse-spark-1.3-contributor / opencode-go / high | 150 (98.7 %) |

Sondes de performance du codage (même prompt fixe, modèle/fournisseur/high ; zéro outil) :

| Position | Horodatage | Résultat | TTMT | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-14T08:51:15.265697+02:00 | réussie | 3.194 s | 352.778 | 370 |
| +30 min | N/A | manquée | N/A | N/A | N/A |
| +60 min | N/A | manquée | N/A | N/A | N/A |
| +90 min | 2026-10-14T10:22:09.729122+02:00 | réussie | 5.117 s | 145.571 | 388 |
| fin | 2026-10-14T10:42:55.323022+02:00 | réussie | 6.447 s | 317.911 | 391 |

Prompt fixe : « Écris uniquement 30 lignes identiques, chacune exactement : alpha beta gamma delta epsilon zeta eta theta iota kappa. Aucune explication, aucun outil. »

| Relèves | Nombre et part |
| --- | --- |
| Prévues | 5 (100.0 %) |
| Réussies | 3 (60.0 %) |
| Échouées | 0 (0.0 %) |
| Manquées | 2 (40.0 %) |

TTMT moyen/min/max : 4.919/3.194/6.447 s. Débit moyen/min/max : 272.087/145.571/352.778 tokens/s. Les relèves +30 et +60 min ont été manquées pendant les interruptions/reprises ; aucune mesure rétroactive. Surcharge des sondes valides : 1149 tokens sortie, 00 h 00 min 20 s ; tokens complets 28924, coût N/A (non relevé). Sondes exclues des compteurs de production.

Cycles de compactage : 2, OpenCode achevé pour chacun ; API native de compactage Codex non exposée, cycles conjoints incomplets, non bloquants. Retards et identifiants conservés au checkpoint.

## 2. Types de messages et d’outils

| Rôle | Nombre et part |
| --- | --- |
| assistant | 152 (62.0 %) |
| user | 93 (38.0 %) |
| Total | 245 (100.0 %) |

| Type de partie | Nombre et part |
| --- | --- |
| compaction | 2 (0.2 %) |
| reasoning | 173 (20.8 %) |
| step-finish | 151 (18.1 %) |
| step-start | 151 (18.1 %) |
| text | 237 (28.5 %) |
| tool | 118 (14.2 %) |
| Total | 832 (100.0 %) |

| Terminaison assistant | Nombre et part |
| --- | --- |
| N/A | 1 (0.7 %) |
| stop | 63 (41.4 %) |
| tool-calls | 88 (57.9 %) |
| Total | 152 (100.0 %) |

| Outil | Appels / part | Achevés / taux | Refus / taux | Erreurs / taux |
| --- | --- | --- | --- | --- |
| bash | 16 (13.6 %) | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 10 (8.5 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 16 (13.6 %) | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 4 (3.4 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 9 (7.6 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| cgpt-validation_poll_approval | 5 (4.2 %) | 1 (20.0 %) | 0 (0.0 %) | 4 (80.0 %) |
| cgpt-validation_request_validation | 26 (22.0 %) | 23 (88.5 %) | 1 (3.8 %) | 2 (7.7 %) |
| grep | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 23 (19.5 %) | 22 (95.7 %) | 0 (0.0 %) | 1 (4.3 %) |
| write | 7 (5.9 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 118 (100.0 %) | 109 (92.4 %) | 1 (0.8 %) | 8 (6.8 %) |

## 3. Fichiers modifiés

| Chemin absolu après archive | Écritures approuvées / part | Refusées | En erreur |
| --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-initial-identity-assurance-vocabulary-v1/design.md | 1 (14.3 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-initial-identity-assurance-vocabulary-v1/proposal.md | 1 (14.3 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-initial-identity-assurance-vocabulary-v1/specs/identity-assurance/spec.md | 1 (14.3 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-initial-identity-assurance-vocabulary-v1/tasks.md | 2 (28.6 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_identity_assurance_integration.py | 1 (14.3 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_identity_assurance.py | 1 (14.3 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 7 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |

Ces nombres sont des tentatives d’écriture par outils write/edit : 7 écritures sur 6 fichiers distincts, tasks.md écrit deux fois (création, puis mise à jour sur preuves). La commande OpenSpec a aussi créé la métadonnée .openspec.yaml, puis déplacé les quatre artefacts et cette métadonnée dans l’archive ; ces effets CLI ne sont pas des appels write supplémentaires. Aucun canon ni code de production modifié. Le présent STATISTIQUES.md est créé ensuite sous mandat distinct et exclu de sa propre collecte.

## 4. Commandes

| Famille exécutée | Nombre et part |
| --- | --- |
| Archivage OpenSpec | 1 (6.2 %) |
| Création OpenSpec | 1 (6.2 %) |
| Prévol inoffensif | 3 (18.8 %) |
| Syntaxe Python | 2 (12.5 %) |
| Tests Python | 4 (25.0 %) |
| Validation OpenSpec | 5 (31.2 %) |
| Total | 16 (100.0 %) |

| Commande exécutée (100 caractères maximum) | Occurrences et part |
| --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-identity-assurance-vocabulary-v1 --yes --s… | 1 (6.2 %) |
| /home/devops/.local/npm/bin/openspec new change add-initial-identity-assurance-vocabulary-v1 | 1 (6.2 %) |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 (6.2 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 (12.5 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-identity-assurance-vocabulary-v1 --strict… | 2 (12.5 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_identity_assurance -v | 1 (6.2 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_identity_assurance_i… | 1 (6.2 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_identity_assurance.py | 1 (6.2 %) |
| /usr/bin/true | 3 (18.8 %) |
| PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.integration.test_iden… | 1 (6.2 %) |
| PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_identity_as… | 1 (6.2 %) |
| PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_identity_mo… | 1 (6.2 %) |

| Code natif de commande | Nombre et part |
| --- | --- |
| 0 | 13 (81.2 %) |
| 1 | 3 (18.8 %) |
| Total | 16 (100.0 %) |

Commandes refusées avant exécution (déclarations CAB, séparées des appels Bash) :

| Commande refusée (100 caractères maximum) | Nombre et part des refus |
| --- | --- |
| /home/devops/.local/npm/bin/openspec validate add-initial-identity-assurance-vocabulary-v1 --strict… | 1 (100.0 %) |

Le premier lancement unittest a échoué sur ModuleNotFoundError pixs, corrigé par PYTHONPATH=src limité au processus après prévol neuf, sans installation ni modification source. Les deux contrôles globaux stricts retournent 1 pour les quatre warnings de longueur connus seulement ; standard avant archive 80/80, strict avant 78/80 et après 77/79, zéro ERROR et aucune nouvelle issue. Le change ciblé strict réussit 1/1 (code 0). Aucun regroupement shell, aucun Git.

## 5. Accès web

| Résultat | Nombre | Taux |
| --- | --- | --- |
| Accès approuvés | 0 | N/A |
| Accès refusés | 0 | N/A |
| Erreurs | 0 | N/A |
| Total | 0 | N/A — aucune requête web |

Aucune URL web visitée, refusée ou recherchée dans ces sessions. Les échanges localhost avec CAB/OpenCode et les appels au fournisseur de codage autorisé sont distincts d’une navigation web. Aucun secret fourni au modèle.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début natif du change | 14/10/2026 08:46:58 CEST |
| Fin — après archivage | 14/10/2026 10:47:41 CEST |
| Durée globale (pauses et attentes incluses) | 02 h 00 min 43 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de collecte | 14/10/2026 08:51:15 CEST | 15 % | 20/10/2026 06:59:31 CEST |
| Après — après archivage de la spécification | 14/10/2026 10:47:41 CEST | 17 % | 20/10/2026 06:59:31 CEST |
| Différence après − avant | — | 2 points | — |

Quota codex, fenêtre 10080 minutes ; lectures natives réelles. Comparaison même compte/fenêtre : vérifiée. La variation est partagée avec les autres tâches du compte et n’est pas attribuée exclusivement à CISMP3. Le relevé initial suit le démarrage natif/prévol et précède le premier travail de qualification ; sa borne est affichée, sans reconstruction rétroactive.

| Domaine natif | Appels / part globale | Achevés / taux | Refus / taux | Erreurs / taux |
| --- | --- | --- | --- | --- |
| Fichiers | 7 (5.9 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 16 (13.6 %) | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 95 (80.5 %) | 86 (90.5 %) | 1 (1.1 %) | 8 (8.4 %) |
| Total global | 118 (100.0 %) | 109 (92.4 %) | 1 (0.8 %) | 8 (6.8 %) |

Totaux croisés vérifiés : rôles = messages ; types = parties ; terminaisons = messages assistant ; outils = domaines ; écritures = fichiers ; commandes = familles et codes natifs. Les refus CAB préexécution sont recensés séparément, sans inventer de commande exécutée.

État vérifié : 98 tests et 2 compilations réussis ; archive réelle avec --skip-specs, contenus UTF-8/LF exacts, canon et production inchangés ; avertissements stricts connus explicitement qualifiés, aucun ERROR. Git non inspecté et non modifié. Aucun accès web, base réelle, réseau applicatif ni secret transmis. Publication commune et gate de clôture restent à confirmer après écriture/contrôle de ce rapport ; arrêt demandé après ce seul change, pas de prochaine sélection.
