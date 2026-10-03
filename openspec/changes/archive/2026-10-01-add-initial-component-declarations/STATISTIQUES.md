# STATISTIQUES — add-initial-component-declarations

Change archivé seul, session ses_f0931f77cffegEUAT8Y42JkUJB. Archive : openspec/changes/archive/2026-10-01-add-initial-component-declarations. Le RUN parent reste en SÉLECTION, sans achèvement global Django/P0.

Historique HTTP complet de cette session, filtré du 2026-10-01T10:25:08.807221+00:00 au 2026-10-01T11:25:32.732845+00:00. Les travaux antérieurs du shell et la rédaction de ce rapport sont exclus. Root ne dispose pas d'un historique chiffrable de ses propres outils : N/A, aucune assimilation aux 31 messages user transmis.

Convention : un outil natif completed sans erreur est classé approuvé et exécuté ; cela ne prouve pas une approbation manuelle. Bash exit nonzero est une erreur de validation, jamais un refus CAB. Les 26 mandats CAB unicitaires distincts sont APPROVED ; un a été décidé par le rappel CGPT dans le périmètre prévalidé, sans doublon local, puis réconcilié par CABtest réel. Les lectures natives permises ne demandent pas de mandat mutateur.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version métadonnée absente | opencode-go | high | 3181.133 ms | 153.227 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex — GPT-6 selon plateforme | N/A | OpenAI | HIGH demandé ; niveau effectif non exposé | N/A | N/A | N/A |

Le temps de service effectif et son dénominateur interagents ne sont pas exposés. Les 341574 ms de segments assistant sans outil sont un intervalle de messages, pas une mesure de génération pure ; non utilisés comme temps de service. Chevauchements N/A.

## 1. Statistiques générales et décisions

Durée calendaire : 01 h 00 min 23.926 s, pauses/tests/permissions/archivage inclus. 176 messages, 114 appels natifs, 26 mandats CAB approuvés (100 %), aucun refus CAB. 113 appels réussis (99,1 %), 1 erreur technique (0,9 %). Zéro compaction observée dans cet intervalle (compactions root N/A). Coût modèle brut métadonné 0.165075342, unité/devise N/A.

Tokens métadonnés (total compté avec cache)

| Valeur | Nombre | Part |
|---|---|---|
| input | 927025 | 2.8 % |
| output | 29957 | 0.1 % |
| reasoning | 7408 | 0.0 % |
| cache_read | 32449921 | 97.1 % |
| cache_write | 0 | 0.0 % |
| Total | 33414311 | 100 % |

Résultats : syntaxe 2 fichiers, ciblés 8, unit 578, integration 161 OK ; strict avant code et deux validations finales OK. Première UNIT 578 tests / 18 échecs d'import pixs en sous-processus, env -i sans PYTHONPATH ; retest sans modification des tests avec PYTHONPATH explicite : 578 OK. Les six lignes README omises ont été restaurées sous mandat distinct et comparées à la lecture native antérieure. Neuf tâches cochées seulement sur preuves.

Sondes dédiées Muse HIGH, prompt identique, sans outil, 40 lignes fixes et 449 tokens de sortie chacune ; trois sessions supprimées après collecte.

| Position | Envoi UTC | TTMT ms | Flux ms | Tokens sortie | Tokens/s | Valide |
|---|---|---|---|---|---|---|
| début prochain cycle après shell | 2026-10-01T10:24:41.079538+00:00 | 2838.066 | 2075.853 | 449 | 216.297 | True |
| +30 min composants | 2026-10-01T10:55:17.240933+00:00 | 3932.151 | 4952.219 | 449 | 90.666 | True |
| fin et relève +60 min composants | 2026-10-01T11:25:08.349565+00:00 | 2773.183 | 2940.085 | 449 | 152.717 | True |

Trois relèves prévues/réussies (100 %), 0 échouée/manquée. La dernière sert à la fois de finale et de relève +60, sans double comptage. +30 relevée 36,161 s après échéance, +60/finale 27,270 s après échéance ; horodatages réels, aucune antidatation. TTMT moyenne 3181.133 ms, min 2773.183, max 3932.151. Débit moyen 153.227 tokens/s, min 90.666, max 216.297.

Prompt constant : Affiche exactement 40 lignes numérotées de 01 à 40. Chaque ligne: NN abcdefghijklmnopqrstuvwxyz 0123456789. Aucun autre texte.

Surcharge séparée des sondes : 26993 tokens métadonnés, 1347 sortie, coût brut 0.0028774 (unité/devise N/A), 19.512 s envoi/dernier token cumulé. Non incluse dans les chiffres de production.

## 2. Types de messages et d'outils

Rôles de messages

| Valeur | Nombre | Part |
|---|---|---|
| user | 31 | 17.6 % |
| assistant | 145 | 82.4 % |
| Total | 176 | 100 % |

Types de parties

| Valeur | Nombre | Part |
|---|---|---|
| text | 62 | 10.7 % |
| step-start | 145 | 24.9 % |
| reasoning | 116 | 19.9 % |
| tool | 114 | 19.6 % |
| step-finish | 145 | 24.9 % |
| Total | 582 | 100 % |

Terminaisons assistant

| Valeur | Nombre | Part |
|---|---|---|
| tool-calls | 114 | 78.6 % |
| stop | 31 | 21.4 % |
| Total | 145 | 100 % |

| Catégorie | Appels | Part | Approuvés exécutés | Taux | Refusés | Taux refus | Erreurs | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| read | 51 | 44.7 % | 51 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 3 | 2.6 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 0.9 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 7 | 6.1 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 26 | 22.8 % | 26 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| bash | 13 | 11.4 % | 12 | 92.3 % | 0 | 0.0 % | 1 | 7.7 % |
| write | 13 | 11.4 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 114 | 100 % | 113 | 99.1 % | 0 | 0.0 % | 1 | 0.9 % |

## 3. Fichiers modifiés

Tentatives natives d'écriture seulement ; les créations et déplacements de la CLI OpenSpec sont des commandes comptées séparément.

| Catégorie | Appels | Part | Approuvés exécutés | Taux | Refusés | Taux refus | Erreurs | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-component-declarations/proposal.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-component-declarations/design.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-component-declarations/tasks.md | 3 | 23.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-component-declarations/specs/initial-application-bootstrap/spec.md | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/component.toml | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/core/component.toml | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/composition_initial.py | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_initial_component_declarations.py | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 2 | 15.4 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 13 | 100 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Neuf chemins distincts (100 % des chemins natifs modifiés), treize tentatives réussies (100 %). Le change et ses cinq artefacts ont été déplacés vers l'archive réelle, hashes identiques. Canon et 31 références préservés, README antérieur préservé hors section nouvelle. STATISTIQUES.md créé après borne, exclu des treize écritures de production.

## 4. Commandes

| Catégorie | Appels | Part | Approuvés exécutés | Taux | Refusés | Taux refus | Erreurs | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| CAB test true | 3 | 23.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec creation | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 3 | 23.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python syntax in memory | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python unittest | 3 | 23.1 % | 2 | 66.7 % | 0 | 0.0 % | 1 | 33.3 % |
| Python integration | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec archive | 1 | 7.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 13 | 100 % | 12 | 92.3 % | 0 | 0.0 % | 1 | 7.7 % |

Aucune commande refusée (0 / 13, 0 %). Une UNIT en erreur, puis retest réussi ; les commandes complètes sont conservées dans l'état de preuves, hors reproduction des longues commandes. Libellés de familles ci-dessus inférieurs à 100 caractères. Aucune installation, commande Git, Docker, opération PostgreSQL réelle ou navigateur dans ce change.

## 5. Accès web

| Statut | Nombre | Part / taux |
|---|---|---|
| Approuvés exécutés | 0 | N/A |
| Refusés | 0 | N/A |
| Erreurs | 0 | N/A |
| Total | 0 | N/A — dénominateur nul |

Aucun outil web ni URL visitée dans l'historique de production de ce change. Pilotage API local OpenCode/CAB distinct : http://127.0.0.1:4096 et http://127.0.0.1:8788 ; ce ne sont pas des visites web de l'agent. Les sondes fournisseur font partie de la télémétrie séparée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-01T10:25:08.807221+00:00 |
| Fin — après archivage | 2026-10-01T11:25:32.732845+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 00 min 23.926 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-01T10:25:08.807248+00:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-01T11:25:32.732812+00:00 | N/A | N/A |
| Différence après − avant | — | N/A | N/A |

Outil natif mcp__codex_app__get_usage_limits absent : pas de pourcentage ni reset observé. Le constat initial a été fait après sonde initiale, pas de faux relevé rétrospectif. Quota codex fenêtre 10080 minutes non accessible. Les quotas sont partagés par le compte ; aucune consommation ne peut être attribuée à ce seul change.

| Catégorie | Appels | Part | Approuvés exécutés | Taux | Refusés | Taux refus | Erreurs | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| other | 88 | 77.2 % | 88 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| commands | 13 | 11.4 % | 12 | 92.3 % | 0 | 0.0 % | 1 | 7.7 % |
| files | 13 | 11.4 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Total | 114 | 100 % | 113 | 99.1 % | 0 | 0.0 % | 1 | 0.9 % |

Total 114 appels natifs, 113 succès, 0 refus, 1 erreur de test réconciliée. Les 26 transports CAB sont inclus dans autres outils, sans double comptage des décisions. Tests finaux et archivage réussis, statistiques séparées. Aucune inspection Git, commit ou push. Aucune valeur secrète ni configuration réelle lue, aucune connexion DB réelle, aucun accès externe métier ; constat limité aux opérations observées. La composition Django exécutable, l'activation P0 et la readiness globale restent non prouvées et ne sont pas déclarées achevées.
