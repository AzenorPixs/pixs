# Statistiques — lecteur privé Bulk B04

Change : add-bulk-private-object-read-invocation-v1. RUN : cismp-pixs-6d45ca1d322c4c05. Archive : openspec/changes/archive/2026-10-14-add-bulk-private-object-read-invocation-v1.
Collecte : 2026-10-14 14:59:20 +0200 à 2026-10-14 17:40:17 +0200, préparation de sélection incluse. Sept sessions de ce RUN filtrées sur ces bornes ; B01 et les autres RUN sont exclus.
Ce rapport, sa publication et la clôture ultérieure sont hors borne. Les sondes jetables sont isolées des chiffres de production. Aucun contenu de message, raisonnement ou longue sortie d’outil n’est recopié.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version LLM N/A | OpenCode Go | high | 2,511 s | 262,295 | N/A — durée active complète non exposée |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; version LLM N/A | OpenCode Go | N/A — compactage natif | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex — modèle exact non exposé | N/A | OpenAI / Codex | N/A | N/A — aucune sonde orchestrateur | N/A | N/A |

Le niveau du compactage n’est pas publié par summarize. La version LLM n’est pas déduite de « 1.3 ». Les durées natives des réponses incluent des attentes d’outils : elles ne sont pas assimilées à de la génération. Seules les fenêtres SSE des sondes sont mesurées ; le dénominateur du temps de service total est N/A.

## 1. Statistiques générales et décisions

| Mesure | Nombre / valeur | Part et périmètre |
|---|---|---|
| Durée calendaire | 02 h 40 min 56 s | Pauses et attentes comprises |
| Sessions | 7 | 100 % du périmètre déclaré |
| Messages | 643 | 100 % |
| Utilisateur / mandats | 245 | 38,1 % |
| Assistant | 398 | 61,9 % |
| Parties | 2207 | 100 % des parties |
| Outils | 406 | 100 % des appels |
| exécuté | 400 | 98,5 % |
| erreur | 5 | 1,2 % |
| refusé | 1 | 0,2 % |

« Exécuté » signifie outil terminé. Lectures et appels MCP réussis ne représentent pas des approbations manuelles supplémentaires. Éditions et commandes terminées sont corrélées à leurs mandats CAB. Un Bash terminé avec code non nul reste autorisé et exécuté ; son échec est distinct.

| Décisions CAB finales corrélées | Nombre | Part |
|---|---|---|
| APPROVED | 48 | 94,1 % |
| N/A — erreur avant décision native | 2 | 3,9 % |
| REJECTED | 1 | 2,0 % |
| Total | 51 | 100 % |

51 request_validation : 48 APPROVED, un REJECTED confirmé par get_approval après timeout, deux erreurs de schéma avant décision. La seconde édition native refusée n’avait pas de nouveau mandat et ne double pas les refus CAB.

| Tokens — champs natifs de production | Nombre | Part des composantes |
|---|---|---|
| Entrée hors cache | 6682307 | 12,2 % |
| Sortie | 153625 | 0,3 % |
| Raisonnement | 69444 | 0,1 % |
| Cache lu | 48036614 | 87,4 % |
| Cache écrit | 0 | 0,0 % |
| Total des composantes mesurées | 54941990 | 100 % |

Sous-composantes disponibles pour 398/398 réponses (100,0 %). Le champ total natif manque pour 3 réponses ; sa somme disponible (54941990) coïncide avec les composantes. Aucun quota n’est converti en tokens.

| Configuration native | Réponses | Part | Tokens natifs connus | Coût natif |
|---|---|---|---|---|
| opencode-go / muse-spark-1.3-contributor / high | 397 | 99,7 % | 54918734 | 0.806413928 |
| opencode-go / muse-spark-1.3-contributor / N/A | 1 | 0,3 % | 23256 | 0.0025038 |

Somme du champ OpenCode cost : 0.808917728. Devise et dépense facturée N/A, non exposées par cette télémétrie. Sondes exclues.

| Session source | Messages | Part | Titre natif |
|---|---|---|---|
| ses_ec5852abcffelYVGCpFtJDGLZJ | 77 | 12,0 % | CISMP1 - sélection après admission B01 |
| ses_ec5682d24ffer7HQAnCPnuQr2y | 30 | 4,7 % | CISMP1 - lecture privée d’objet B04 |
| ses_ec55e97ebffePGsHJC0bJZFLs5 | 215 | 33,4 % | CISMP1 - récupération du lecteur privé B04 |
| ses_ec52e26baffebX6n4m54E32It0 | 29 | 4,5 % | CISMP1 - récupération du lecteur privé B04 |
| ses_ec524fc2effeqKToMCBgKMyWL0 | 47 | 7,3 % | CISMP1 - récupération du lecteur privé B04 |
| ses_ec51dbaecffe4X4tbC2EoT1xpS | 111 | 17,3 % | CISMP1 - récupération du lecteur privé B04 |
| ses_ec50a3cfcffeIg5TrH8fL7bvE1 | 134 | 20,8 % | CISMP1 - récupération du lecteur privé B04 |
| Total | 643 | 100 % | Sept historiques |

Source d’audit : /home/devops/datas/pixs/output/cismp/cismp-pixs-6d45ca1d322c4c05/state.json. Le champ b04_statistics_data conserve identifiants, premières/dernières réponses, bornes et SHA-256 des historiques filtrés.

**Sondes du seul agent de codage**

| Horodatage Paris | Position | Résultat | TTMT s | Tokens/s | Fenêtre SSE s | Tokens sortie | Coût natif |
|---|---|---|---|---|---|---|---|
| 2026-10-14 14:59:54 +0200 | début-reprise | SUCCÈS | 2,167 | 296,213 | 4,085 | 1210 | 0.0015668 |
| 2026-10-14 15:37:07 +0200 | sonde supplémentaire après relève manquée | ÉCHEC | N/A | N/A | 2,016 | N/A | N/A |
| 2026-10-14 15:40:33 +0200 | nouvel essai unique de la sonde supplémentaire échouée | SUCCÈS | 3,029 | 249,517 | 4,926 | 1229 | 0.0016028 |
| 2026-10-14 15:59:57 +0200 | relève périodique | SUCCÈS | 2,836 | 187,962 | 6,437 | 1210 | 0.0015796 |
| 2026-10-14 16:29:56 +0200 | relève périodique | SUCCÈS | 2,380 | 490,595 | 2,466 | 1210 | 0.001582126 |
| 2026-10-14 17:01:17 +0200 | sonde supplémentaire après relève manquée | SUCCÈS | 2,033 | 179,108 | 6,756 | 1210 | 0.001566 |
| 2026-10-14 17:29:57 +0200 | relève périodique | SUCCÈS | 2,871 | 136,657 | 8,854 | 1210 | 0.0015788 |
| 2026-10-14 17:39:42 +0200 | fin après archivage | SUCCÈS | 2,261 | 296,014 | 4,088 | 1210 | 0.001567126 |

- Relève manquée : 2026-10-14 15:29:54 +0200. Aucune mesure rétroactive ; tentative supplémentaire distinguée.
- Relève manquée : 2026-10-14 16:59:54 +0200. Aucune mesure rétroactive ; tentative supplémentaire distinguée.

| Cadence | Nombre | Part / dénominateur |
|---|---|---|
| Créneaux prévus : initiale, cinq périodiques, finale | 7 | 100 % des créneaux |
| Créneaux effectivement mesurés | 5 | 71,4 % |
| Créneaux manqués | 2 | 28,6 % |
| Tentatives supplémentaires dont unique nouvel essai | 3 | Hors créneaux |
| Sondes réussies, supplémentaires incluses | 7 | 70,0 % |
| Sondes échouées | 1 | 10,0 % |
| Relèves manquées | 2 | 20,0 % |
| Total observations et manques | 10 | 100 % |

Moyennes arithmétiques sur 7 sondes valides : TTMT 2,511 s (min. 2,033, max. 3,029) ; débit 262,295 tokens/s (min. 136,657, max. 490,595). La sonde échouée est exclue ; sa fenêtre SSE est partielle.

| Surcharge de télémétrie séparée | Valeur | Couverture |
|---|---|---|
| Tokens sortie connus | 8489 | 7/8 tentatives ; échec N/A |
| Tokens natifs totaux connus | 100498 | Somme des compteurs fournis, sans production |
| Coût natif connu | 0.011043252 | Total complet N/A : une tentative sans coût final |
| Fenêtres de génération SSE valides | 37,612 s | Pas le service complet de production |
| Sonde échouée | Tokens/coût finaux N/A | Nouvel essai unique ; immédiateté non attestée |

Prompt constant : « Écris exactement 80 lignes, sans autre texte. Chaque ligne suit ce modèle : Ligne 001 : mesure déterministe du débit de génération. Numérote les lignes de 001 à 080. Aucun outil. » Les sessions jetables sont exclues des messages de production. Deux retards et un échec restent visibles.

| Compactage dans la fenêtre | OpenCode | Codex | Retard s |
|---|---|---|---|
| compact-ce388cfc5114498787a33e6106d25475 | ACHEVÉ_NATIF | API_NATIVE_NON_EXPOSÉE | 390,015 |

OpenCode achevé nativement ; cycle conjoint partiel faute d’API Codex exposée. Retard lié à la récupération et à la conservation du préfixe natif jusqu’à complete.

Résultats : quatre compilations réussies ; premiers bilans 86 tests/18 erreurs puis 87 tests/une assertion erronée ; ensuite 87 puis 91 tests réussis. Régressions locale et combinée : 545/545 chacune. Cumul 1441 exécutions de tests avec recoupements, pas un nombre de cas uniques.
Incidents conservés : prévol anticipé invalide, timeout MCP réconcilié, manifeste vide, règle Bash ask à rétablir, seconde édition refusée, glob zsh non protégé avant Python, deux relèves manquées et première preuve d’intégration refusée en revue. Effets autorisés préservés par reprise ; aucun effet hors périmètre établi.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 245 | 38,1 % |
| assistant | 398 | 61,9 % |
| Total | 643 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 568 | 25,7 % |
| step-start | 397 | 18,0 % |
| reasoning | 439 | 19,9 % |
| tool | 406 | 18,4 % |
| step-finish | 396 | 17,9 % |
| compaction | 1 | 0,0 % |
| Total | 2207 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 260 | 65,3 % |
| stop | 135 | 33,9 % |
| unknown | 1 | 0,3 % |
| N/A / interrompu | 2 | 0,5 % |
| Total | 398 | 100 % |

| Outil | Total | Part globale | Terminé / taux | Refusé / taux | Erreur / taux | Attente / taux |
|---|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 88 | 21,7 % | 88 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_health | 39 | 9,6 % | 39 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 39 | 9,6 % | 39 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 96 | 23,6 % | 95 (99,0 %) | 0 (0,0 %) | 1 (1,0 %) | 0 (0,0 %) |
| glob | 10 | 2,5 % | 10 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 32 | 7,9 % | 32 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 51 | 12,6 % | 48 (94,1 %) | 0 (0,0 %) | 3 (5,9 %) | 0 (0,0 %) |
| bash | 23 | 5,7 % | 23 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 1 | 0,2 % | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 1 | 0,2 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 18 | 4,4 % | 18 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| edit | 8 | 2,0 % | 7 (87,5 %) | 1 (12,5 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 406 | 100,0 % | 400 (98,5 %) | 1 (0,2 %) | 5 (1,2 %) | 0 (0,0 %) |

Erreurs techniques : trois request_validation, une consultation poll_approval et une lecture. Refus natif : une seconde édition non couverte par once. Les lectures/MCP terminés ne sont pas des autorisations manuelles.

## 3. Fichiers modifiés

| Chemin absolu lors de la tentative | Tentatives | Part | Autorisées/exécutées | Refusées | Erreurs |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-bulk-private-object-read-invocation-v1/proposal.md | 1 | 3,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-private-object-read-invocation-v1/design.md | 2 | 7,7 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-private-object-read-invocation-v1/specs/object-storage/spec.md | 1 | 3,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-private-object-read-invocation-v1/tasks.md | 3 | 11,5 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_trusted_ports.py | 1 | 3,8 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_private_object_reader.py | 9 | 34,6 % | 8 (88,9 %) | 1 (11,1 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_private_object_reader.py | 6 | 23,1 % | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_private_object_reader_integration.py | 3 | 11,5 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 26 | 100 % | 25 (96,2 %) | 1 (3,8 %) | 0 (0,0 %) |

Tentatives d’édition, pas lignes ni fichiers uniques : huit chemins. Mutations de commandes OpenSpec inventoriées séparément, sans doubler les outils.

Déplacement vérifié : /home/devops/datas/pixs/openspec/changes/add-bulk-private-object-read-invocation-v1 vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-bulk-private-object-read-invocation-v1. Quatre Markdown et .openspec.yaml présents dans l’archive ; dossier actif absent.
Mutation canonique CLI : /home/devops/datas/pixs/openspec/specs/object-storage/spec.md, une exigence modifiée et trois scénarios ajoutés. Annexe normative inchangée, SHA-256 c066b51c4ecbb18f4d9998d98654df5715e3978c6171863bd7c76c9cebf365ce.
Rapport /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-bulk-private-object-read-invocation-v1/STATISTIQUES.md sous mandat séparé après borne : écriture/clôture exclues. Neuf empreintes locales au checkpoint ; aucun comptage Git.

## 4. Commandes

| Famille | Nombre | Part | Autorisées/exécutées | Refusées | Erreurs |
|---|---|---|---|---|---|
| Validation OpenSpec | 8 | 34,8 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Prévol inoffensif | 5 | 21,7 % | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Création OpenSpec | 1 | 4,3 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Tests unittest | 7 | 30,4 % | 7 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Compilation Python | 1 | 4,3 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Archivage OpenSpec | 1 | 4,3 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 23 | 100 % | 23 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

| Commande — libellé ≤100 caractères avec empreinte si tronqué | Occurrences | Part | Résultat outil |
|---|---|---|---|
| /home/devops/.local/npm/bin/openspec validate object-storage --type spec --strict --jso…#46fa0d5dc9 | 1 | 4,3 % | exécuté: 1 |
| /usr/bin/true | 5 | 21,7 % | exécuté: 5 |
| /home/devops/.local/npm/bin/openspec new change add-bulk-private-object-read-invocation…#5cdf627365 | 1 | 4,3 % | exécuté: 1 |
| /home/devops/.local/npm/bin/openspec validate add-bulk-private-object-read-invocation-v…#d1439175ae | 3 | 13,0 % | exécuté: 3 |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/devops/datas/pixs/src:/home/dev…#4868ab67bb | 3 | 13,0 % | exécuté: 3 |
| /home/devops/datas/pixs/.venv/bin/python3 -X pycache_prefix=/home/devops/datas/pixs/src…#d4b1318ae9 | 1 | 4,3 % | exécuté: 1 |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/devops/datas/pixs/src:/home/dev…#869fe435f5 | 1 | 4,3 % | exécuté: 1 |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/devops/datas/pixs/src:/home/dev…#5d9bd519f1 | 1 | 4,3 % | exécuté: 1 |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/devops/datas/pixs/src:/home/dev…#9b20d9239b | 2 | 8,7 % | exécuté: 2 |
| /home/devops/.local/npm/bin/openspec validate --all --json | 2 | 8,7 % | exécuté: 2 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 | 8,7 % | exécuté: 2 |
| /home/devops/.local/npm/bin/openspec archive add-bulk-private-object-read-invocation-v1 --yes | 1 | 4,3 % | exécuté: 1 |

| Codes de sortie | Nombre | Part |
|---|---|---|
| 0 | 18 | 78,3 % |
| 1 | 5 | 21,7 % |
| Total | 23 | 100 % |

23 commandes autorisées/exécutées : 18 codes 0 et 5 codes 1. Codes 1 : deux bilans unittest initiaux, un glob zsh refusé avant Python et deux contrôles stricts globaux avec avertissements préexistants. Aucune commande native refusée (0 ; taux du sous-ensemble vide N/A). Les erreurs MCP n’ont pas produit de commande. Texte intégral et empreintes au checkpoint.

## 5. Accès web

| Accès web natifs de l’agent de codage | Nombre | Part des outils | Taux |
|---|---|---|---|
| Approuvés/exécutés | 0 | 0,0 % | N/A — aucun accès |
| Refusés | 0 | 0,0 % | N/A |
| Erreurs | 0 | 0,0 % | N/A |
| Total | 0 | 0,0 % | N/A — dénominateur nul |

Aucune URL de contenu web approuvée, refusée ou visitée dans ces historiques. Services LLM, transports locaux CAB/OpenCode et tests PostgreSQL autorisés sont distincts. Décompte exhaustif des accès de l’orchestrateur non exposé : N/A, pas zéro.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-14 14:59:20 +0200 |
| Fin — après archivage et sonde finale | 2026-10-14 17:40:17 +0200 |
| Durée globale (pauses et attentes incluses) | 02 h 40 min 56 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-14 14:59:18 +0200 | 19 % | 2026-10-20 06:59:31 +0200 |
| Après — après archivage de la spécification | 2026-10-14 17:40:17 +0200 | 22 % | 2026-10-20 06:59:31 +0200 |
| Différence après − avant | — | 3 points de pourcentage | — |

Même compte (empreinte fnv1a64:acac69dd79e8d1ad), quota codex, fenêtre 10080 minutes et réinitialisation. Quota partagé : 3 points peuvent inclure d’autres chats, sans attribution exclusive à CISMP1. Rédaction ultérieure du rapport exclue.

| Domaine | Total | Part globale | Exécuté / taux | Refusé / taux | Erreur / taux | Attente / taux |
|---|---|---|---|---|---|---|
| Éditions | 26 | 6,4 % | 25 (96,2 %) | 1 (3,8 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commandes | 23 | 5,7 % | 23 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Web | 0 | 0,0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils — lectures et MCP | 357 | 87,9 % | 352 (98,6 %) | 0 (0,0 %) | 5 (1,4 %) | 0 (0,0 %) |
| Total global | 406 | 100,0 % | 400 (98,5 %) | 1 (0,2 %) | 5 (1,2 %) | 0 (0,0 %) |

Développement final : 545/545 tests Bulk sous exclusion, 91 tests ciblés/intégration fraîche et quatre compilations réussies. Le nouveau lecteur mémoire ne nécessite pas PostgreSQL ; les tests PG de régression restent distincts d’une qualification de production.
Archive réussie une seule fois. Après archive : standard OpenSpec 78/78 ; strict global 76/78, exactement quatre WARNING de longueur préexistants, zéro ERROR, aucune nouvelle anomalie. Le strict global n’est pas déclaré réussi ; annexe B04 préservée.
Git non inspecté ni modifié ; aucun commit/push revendiqué. Aucun fournisseur de production, worker complet, route, migration ou dépendance ajouté. Aucun secret reproduit dans ce rapport ; valeurs PostgreSQL réservées au processus de test, secret fournisseur au stockage/processus autorisé.
Arrêt demandé après ce change. Ce rapport décrit la fenêtre terminée après archive ; gate, désarmement et arrêt ultérieurs sont vérifiés dans le checkpoint avant restitution finale. Aucun nouveau change ne sera sélectionné.

