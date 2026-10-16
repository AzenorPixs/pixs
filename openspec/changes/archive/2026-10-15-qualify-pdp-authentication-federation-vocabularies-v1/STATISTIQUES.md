# STATISTIQUES — qualify-pdp-authentication-federation-vocabularies-v1

RUN : cismp-pixs-01a13baffc02 ; session maîtresse : ses_ec4411b3affeiiTH1oT56Ixtd8 ; job : cismp3-qualify-ac0e49223db1.
Archive réelle : /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-qualify-pdp-authentication-federation-vocabularies-v1. Exclusion CISMP3 sur référence 12 ; réservation v115. Rapport préparé après archivage unique et fermeture de collecte, avant sa propre écriture et avant publication/gate/release.
Source : historique natif OpenCode complet de cette maîtresse, neuf sessions jetables de sondes, décisions CAB relues par requestId, checkpoint non secret et métadonnées du tour Codex. Les historiques et quotas des autres RUN ne sont pas attribués à ce change.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go (opencode-go) | high | 3.017 s | 230.407 | N/A — durée de génération isolée non exposée |
| muse-spark-1.3-contributor (utilitaire de compactage) | N/A — version exacte non exposée | OpenCode Go (opencode-go) | N/A — variant natif absent | N/A | N/A | N/A — durée active isolée non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| N/A — agent Codex identifié, modèle exact non exposé | N/A | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — durée de génération isolée non exposée |

Le runtime OpenCode observé est 1.19.0 ; ce numéro ne constitue pas la version du modèle. Le temps de service cumulé et son dénominateur sont N/A : les durées calendaires, attentes CAB, outils et réponses complètes ne permettent pas d’isoler la génération. Les activités de codage et de pilotage peuvent se chevaucher.

## 1. Statistiques générales et décisions

| Population | Effectif | Part |
|---|---|---|
| Messages maîtresse | 521 | 100 % |
| Appels d’outils maîtresse | 116 | 100 % |
| Décisions CAB uniques | 24 | 100 % |
| Approbations CAB | 23 | 95.8 % |
| Refus CAB avant effet | 1 | 4.2 % |
| Sondes prévues et finale | 19 | 100 % |
| Sondes valides | 9 | 47.4 % |
| Sondes manquées | 10 | 52.6 % |
| Sondes échouées | 0 | 0.0 % |

Convention : un outil terminé avec succès est classé « réussi/autorisé techniquement », sans en déduire une approbation humaine. Les décisions CAB sont comptées séparément. Un code Bash non nul figure dans la colonne erreur/code non nul ; deux de ces codes proviennent du strict global avec avertissements, sans erreur normative nouvelle. Un refus CAB sans Bash n’est pas inventé comme un refus de permission native.

| Résultat natif des outils | Nombre | Part |
|---|---|---|
| Réussis | 107 | 92.2 % |
| Refus explicites d’outil | 0 | 0.0 % |
| Erreurs ou codes non nuls | 9 | 7.8 % |
| TOTAL | 116 | 100 % |

Les neuf erreurs/codes non nuls se répartissent en deux lectures, trois request_validation, un poll_approval et trois Bash. Les trois Bash non nuls sont le premier lancement des régressions (import du helper) et les deux contrôles stricts globaux. Le refus unique de compilation a été consommé REJECTED par son approval_id, sans exécution, puis un prévol neuf /usr/bin/true et READY pending0 ont prouvé la reprise.

| Compteur de tokens natif — maîtresse | Valeur |
|---|---|
| input | 1938429 |
| output | 51056 |
| reasoning | 22218 |
| cache_read | 21738987 |
| cache_write | 0 |
Coût natif OpenCode : 0.251975674 (unité non exposée par ces métadonnées). Tokens/coût de l’orchestrateur : N/A — export non exposé. Les compteurs natifs sont conservés séparément ; aucun total de tokens uniques ni prix en euros n’est reconstruit.

| Résultat du développement | Preuve |
|---|---|
| Compilation Python | Deux fichiers compilés séparément, sorties natives 0 |
| Tests dédiés | 7 tests réussis, sortie native 0, cismp3-d99dcc50d6414d |
| Régressions | 96 tests réussis, sortie native 0, cismp3-385248fa305745 ; 24 empreintes des entrées inchangées après intégration |
| Production | 7 fichiers authz inchangés ; aucune modification de production |
| Strict ciblé | 1/1, issues vides, sortie 0, cismp3-5b65726a9f4c49 |
| Global standard | 79/79, sortie 0, cismp3-56a7aa62d3894e |
| Strict global avant archive | 77/79, sortie 1, quatre WARNING historiques et zéro ERROR |
| Strict global après archive | 76/78, sortie 1, mêmes quatre WARNING et zéro ERROR, cismp3-d1ea247c985243 |
| Archive | Sortie 0, specsUpdated=false, --skip-specs justifié par delta canonique identique |

Les quatre WARNING portent sur bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4], pour une longueur >500 caractères. Aucun strict-success global n’est déclaré. La longueur n’étant pas un critère de qualité du cadrage CISMP, aucune norme n’a été reformulée. Le premier échec d’import et le rapport OpenCode ayant annoncé à tort exit0 pour le strict avant archive restent tracés ; la métadonnée native exit1 prévaut.

Quatre compactages OpenCode ont une preuve native summary/finish stop et une reprise build high/READY : trois cycles communs et un cycle local horaire. Leur partie Codex pilotée reste N/A — API propriétaire non exposée. Le tour Codex exporté contient un événement contextCompaction automatique, distinct d’un cycle piloté. Les compactages différés pendant l’exclusion concurrente sont consignés sans dates de réussite inventées.

### Sondes et surcharge de télémétrie

Prompt constant : 185 caractères, sans outil ni source ; contenu déterministe de 100 lignes, toutes les sondes réalisées auditées conformes. Moyennes arithmétiques sur 9 sondes valides seulement : TTMT 3.017 s (min 2.208, max 4.422), débit 230.407 tokens/s (min 126.444, max 376.413).
| Position | Envoi UTC ou échéance manquée | État | Tokens sortie | TTMT (s) | Tokens/s |
|---|---|---|---|---|---|
| début | 2026-10-14T18:44:16.567801+00:00 | valide | 1109 | 2.208 | 320.141 |
| +30 min | 2026-10-14T19:15:42.321924+00:00 | valide | 1119 | 3.067 | 376.413 |
| +60 min | 2026-10-14T19:44:38.356558+00:00 | valide | 1146 | 3.122 | 138.138 |
| +90 min | 2026-10-14T20:14:36.954176+00:00 | valide | 1152 | 2.564 | 212.214 |
| +120 min | 2026-10-14T20:44:37.634214+00:00 | valide | 1136 | 2.838 | 233.014 |
| +150 min | 2026-10-14T21:14:34.660531+00:00 | valide | 1157 | 3.018 | 299.851 |
| +180 min | 2026-10-14T21:44:38.629789+00:00 | valide | 1134 | 2.818 | 202.158 |
| +210 min | 2026-10-14T22:14:22.265009+00:00 | manquée | N/A | N/A | N/A |
| +240 min | 2026-10-14T22:44:22.265009+00:00 | manquée | N/A | N/A | N/A |
| +270 min | 2026-10-14T23:14:22.265009+00:00 | manquée | N/A | N/A | N/A |
| périodique différée | 2026-10-14T23:44:22.265009+00:00 | manquée | N/A | N/A | N/A |
| périodique différée | 2026-10-15T00:14:22.265009+00:00 | manquée | N/A | N/A | N/A |
| périodique différée | 2026-10-15T00:44:22.265009+00:00 | manquée | N/A | N/A | N/A |
| périodique différée | 2026-10-15T01:14:22.265009+00:00 | manquée | N/A | N/A | N/A |
| périodique différée | 2026-10-15T01:44:22.265009+00:00 | manquée | N/A | N/A | N/A |
| périodique différée | 2026-10-15T02:14:22.265009+00:00 | manquée | N/A | N/A | N/A |
| +480 min | 2026-10-15T02:44:22.265009+00:00 | manquée | N/A | N/A | N/A |
| +510 min | 2026-10-15T03:15:19.433965+00:00 | valide | 1151 | 4.422 | 165.288 |
| fin | 2026-10-15T03:19:16.798865+00:00 | valide | 1165 | 3.092 | 126.444 |

| Surcharge des neuf sondes — hors production | Valeur |
|---|---|
| Tokens entrée | 113029 |
| Tokens sortie | 10269 |
| Tokens raisonnement | 6327 |
| Coût natif | 0.014623004 |
| Durées réponses complètes cumulées (inclut latence) | 78.603 s |

Les sondes manquées ne sont jamais reconstruites. La relève +210 min a été manquée dans le pilotage avant constat de la barrière ; les autres attentes/barrières et la discontinuité 23:28–02:23 UTC sont distinguées dans le checkpoint. La relève +510 min a un retard observé de 57,169 s. Deux gaps antérieurs de client de surveillance (environ 119 s puis 165,766 s) sont signalés ; aucune cadence parfaite n’est revendiquée. Le client passif ultérieur a continué ses heartbeats durant la discontinuité d’observation de l’orchestrateur. Les compteurs HTTP/SSE exhaustifs sont N/A — les historiques partiels et clients encore ouverts ne permettent pas un total clos à cette borne.

## 2. Types de messages et d’outils

| Rôle natif | Nombre | Part |
|---|---|---|
| user | 233 | 44.7 % |
| assistant | 288 | 55.3 % |
| TOTAL | 521 | 100 % |

| Type de partie native | Nombre | Part |
|---|---|---|
| text | 483 | 32.9 % |
| step-start | 288 | 19.6 % |
| reasoning | 292 | 19.9 % |
| tool | 116 | 7.9 % |
| step-finish | 287 | 19.5 % |
| compaction | 4 | 0.3 % |
| TOTAL | 1470 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 83 | 28.8 % |
| stop | 204 | 70.8 % |
| None | 1 | 0.3 % |
| TOTAL | 288 | 100 % |
La terminaison absente correspond à l’interruption réconciliée, pas à un achèvement. Les 233 messages user comprennent les cadrages/mandats et relances de contrôle ; ils ne représentent pas 233 demandes humaines distinctes.

| Outil natif | Total | Part | Réussis | Refus explicites | Erreurs/codes non nuls |
|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 12 | 10.3 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 44 | 37.9 % | 42 (95.5 %) | 0 (0.0 %) | 2 (4.5 %) |
| glob | 8 | 6.9 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 25 | 21.6 % | 22 (88.0 %) | 0 (0.0 %) | 3 (12.0 %) |
| cgpt-validation_poll_approval | 2 | 1.7 % | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| bash | 14 | 12.1 % | 11 (78.6 %) | 0 (0.0 %) | 3 (21.4 %) |
| write | 8 | 6.9 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| TOTAL | 116 | 100.0 % | 107 (92.2 %) | 0 (0.0 %) | 9 (7.8 %) |

### Métadonnées de l’orchestrateur

| Type d’élément du tour Codex | Nombre | Part |
|---|---|---|
| userMessage | 4 | 0.3 % |
| agentMessage | 137 | 8.8 % |
| commandExecution | 391 | 25.1 % |
| reasoning | 753 | 48.4 % |
| mcpToolCall | 137 | 8.8 % |
| functionCallOutput | 40 | 2.6 % |
| sleep | 94 | 6.0 % |
| contextCompaction | 1 | 0.1 % |
| TOTAL | 1557 | 100 % |
Les types reasoning sont comptés par métadonnée uniquement : aucun contenu de raisonnement n’a été analysé ni recopié. Les sorties d’outil ne sont pas recomptées comme des appels. Borne : exec-1c009310-1f00-4bbd-ab60-1bf95200439d (dernier quota final).
| Appel app de l’orchestrateur | Nombre | Part |
|---|---|---|
| list_threads / completed | 1 | 0.7 % |
| send_message_to_thread / completed | 32 | 23.4 % |
| get_usage_limits / completed | 3 | 2.2 % |
| wait_threads / completed | 99 | 72.3 % |
| read_thread / completed | 1 | 0.7 % |
| open_in_codex / completed | 1 | 0.7 % |
| TOTAL | 137 | 100 % |

## 3. Fichiers modifiés

Ces nombres sont des tentatives natives write/edit, pas un diff Git ni un nombre de lignes modifiées. Tous les chemins sont absolus. Les chemins actifs OpenSpec ci-dessous ont ensuite été déplacés dans l’archive réelle par la commande autorisée.
| Cible au moment de l’écriture | Tentatives | Part | Réussies | Refusées | Erreurs |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/qualify-pdp-authentication-federation-vocabularies-v1/proposal.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/qualify-pdp-authentication-federation-vocabularies-v1/design.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/qualify-pdp-authentication-federation-vocabularies-v1/tasks.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/qualify-pdp-authentication-federation-vocabularies-v1/specs/authorization-engine/spec.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_authentication_federation_vocab.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_authentication_federation_vocab_integration.py | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| TOTAL | 9 | 100.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Autres effets autorisés, hors tentatives write/edit : .openspec.yaml a été créé par openspec new change ; les cinq artefacts ont été déplacés par l’archivage unique. Deux cfiles régénérables ont été écrits par compilation, sans lecture de leur contenu : /home/devops/datas/pixs/tests/unit/__pycache__/cismp3-authentication-federation.pyc et /home/devops/datas/pixs/tests/integration/__pycache__/cismp3-authentication-federation.pyc.
Le présent rapport /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-qualify-pdp-authentication-federation-vocabularies-v1/STATISTIQUES.md sera écrit sous un mandat distinct après cette borne ; sa propre écriture n’est pas incluse dans les compteurs de production. Les sources de production et façades restent inchangées par empreintes. Les modifications concurrentes des autres RUN ne sont pas attribuées ici.

## 4. Commandes

Quatorze appels Bash ont réellement eu lieu. Une quinzième tentative de commande CAB (compilation) a été refusée avant Bash ; les demandes CAB et les exécutions restent distinguées.
| Famille de commandes exécutées | Total | Part | Réussies | Refus outil | Codes non nuls |
|---|---|---|---|---|---|
| OpenSpec | 7 | 50.0 % | 5 (71.4 %) | 0 (0.0 %) | 2 (28.6 %) |
| Tests unittest | 3 | 21.4 % | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| Prévol inoffensif | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| TOTAL | 14 | 100 % | 11 (78,6 %) | 0 (0,0 %) | 3 (21,4 %) |

| Commande exécutée (100 caractères maximum) | Exécutions | Part | Réussies | Refus outil | Codes non nuls |
|---|---|---|---|---|---|
| /home/devops/.local/npm/bin/openspec new change qualify-pdp-authentication-federation-vocabularies-… | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate qualify-pdp-authentication-federation-vocabularies-v1… | 2 | 15.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_pdp_policy … | 1 | 7.7 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| /usr/bin/true | 2 | 15.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit.test_… | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c "__import__('py_compile').compile('tests/unit/test_… | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c "__import__('py_compile').compile('tests/integratio… | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 | 15.4 % | 0 (0.0 %) | 0 (0.0 %) | 2 (100.0 %) |
| /home/devops/.local/npm/bin/openspec archive qualify-pdp-authentication-federation-vocabularies-v1 … | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| TOTAL | 13 | 100.0 % | 10 (76.9 %) | 0 (0.0 %) | 3 (23.1 %) |

### Commandes refusées — non exécutées

| Commande refusée (100 caractères maximum) | Nombre | Part des refus | Part des 15 tentatives CAB de commande |
|---|---|---|---|
| /home/devops/datas/pixs/.venv/bin/python3 -B -c "__import__('py_compile').compile('tests/unit/test_… | 1 | 100 % | 6.7 % |
Refus de reprise après omission resources dans le premier appel MCP ; absence de Bash/write/edit et permission non consommée prouvées. REJECTED a été consommé par get_approval sur le même approval_id, puis prévol inédit /usr/bin/true sortie0 et READY pending0 ; nouvelle compilation ensuite réussie.

| Commandes de pilotage Codex, métadonnées | Nombre | Part |
|---|---|---|
| completed / 0 | 382 | 97.7 % |
| failed / 1 | 7 | 1.8 % |
| failed / 2 | 2 | 0.5 % |
| TOTAL | 391 | 100 % |
Ces 391 commandes incluent l’observation HTTP, les lectures, benchmarks PLLM et agrégations, avec 382 sorties0 et neuf sorties non nulles. Les neuf sorties non nulles du pilotage ne sont pas présentées comme neuf tests échoués. La classification fine refus automatique/erreur d’environnement/non-correspondance de recherche est N/A à partir de ces seuls codes. Aucun état Git n’a été inspecté.

## 5. Accès web

| Outils web natifs de cette maîtresse | Nombre | Part | Approbations | Refus | Erreurs |
|---|---|---|---|---|---|
| Aucun webfetch/websearch/browser | 0 | N/A | 0 | 0 | 0 |
| TOTAL | 0 | N/A | 0 | 0 | 0 |
Aucune page web ni URL refusée n’est observée dans les outils natifs de la maîtresse. Les API LLM et locales sont des communications techniques, distinctes de visites de pages.

| URL technique autorisée (100 caractères maximum) | Statut réellement observé | Comptage |
|---|---|---|
| https://opencode.ai/zen/go/v1/responses | Benchmark PLLM autorisé ; requêtes envoyées | 4 tentatives de performance dans les deux évaluations conservées |
| https://opencode.ai/zen/go/v1/usage | Lecture de quotas autorisée par processus sécurisé | Nombre global N/A ; dernière évaluation : deux lectures avant ses paliers |
Les quatre tentatives de benchmark comprennent deux budgets incomplets et deux réussites ; elles ne sont pas fusionnées avec les sondes statistiques. La dernière évaluation Muse high est Valide : TTFT 22,7431 s, débit natif de benchmark 1509,836 tokens/s, palier 4096 ; quotas utilisés rolling 0 %, hebdomadaire 37 %, mensuel 83 %. Ce débit mesure le flux reasoning_and_response selon le skill, tandis que le débit des sondes utilise leurs tokens.output natifs ; aucune moyenne commune n’est calculée.
Les requêtes d’inférence internes OpenCode Go et les appels locaux http://127.0.0.1:4096, :8788, :8789 ne disposent pas d’un journal HTTP exhaustif clos à cette borne : N/A pour leur volume. Les communications Muse nécessaires au travail Pixs sont explicitement autorisées. Les valeurs secrètes restent dans le seul processus sécurisé, jamais dans le modèle, le checkpoint ou ce rapport.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — première entrée native de la maîtresse | 2026-10-14T18:48:48.590000+00:00 |
| Fin — après archivage, sonde finale et relevé quota | 2026-10-15T03:20:05+00:00 |
| Durée globale (pauses et attentes incluses) | 08 h 31 min 16 s |
RUN parent commencé le 2026-10-14T18:32:34+00:00 ; réservation du change le 2026-10-14T18:53:56.319876+00:00. La durée du RUN parent jusqu’à la borne est 08 h 47 min 31 s. Les sondes initiales et données de contrôle communes antérieures au change sont identifiées comme telles, sans répartition arbitraire. Les temps d’attente dominent la durée calendaire ; celle-ci n’est pas un temps de génération.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — préparation du change | N/A heure exacte ; consignation 2026-10-14T18:53:56.319866+00:00 | 24 % | 2026-10-20T04:59:31+00:00 |
| Après — après archivage de la spécification | Entre 2026-10-15 03:20:04 UTC et 2026-10-15 03:20:05 UTC | 32 % | 2026-10-20T04:59:31+00:00 |
| Différence après − avant | — | 8 points de pourcentage | — |
Même compte et même fenêtre codex, 10080 min, réinitialisation vérifiés par l’outil natif. Le relevé initial reste conservé ; son heure exacte non exposée n’est pas inventée. Le quota est partagé avec les autres chats : ces huit points représentent la variation du compte pendant l’intervalle et ne sont pas attribués exclusivement à ce change. La rédaction du présent rapport est postérieure à la borne finale.

### Totaux natifs du change

| Domaine natif | Total | Part | Réussis | Refus explicites | Erreurs/codes non nuls |
|---|---|---|---|---|---|
| Fichiers write/edit | 9 | 7.8 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes Bash | 14 | 12.1 % | 11 (78.6 %) | 0 (0.0 %) | 3 (21.4 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 93 | 80.2 % | 87 (93.5 %) | 0 (0.0 %) | 6 (6.5 %) |
| TOTAL | 116 | 100.0 % | 107 (92.2 %) | 0 (0.0 %) | 9 (7.8 %) |
À part : 24 décisions CAB =23 approbations (95,8 %) +1 refus avant Bash (4,2 %). Les 15 tentatives CAB de commande comprennent 14 exécutions +1 refus ; ne pas ajouter ce refus comme un Bash fictif.

### Pilotage et codage, populations observables combinées

| Domaine | Total | Part | Réussis | Refus explicites | Erreurs/codes non nuls | Résultat non exposé |
|---|---|---|---|---|---|---|
| Fichiers | 9 | 1.2 % | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commandes | 405 | 54.9 % | 393 (97.0 %) | 0 (0.0 %) | 12 (3.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils/attentes | 324 | 43.9 % | 224 (69.1 %) | 0 (0.0 %) | 6 (1.9 %) | 94 (29.0 %) |
| TOTAL | 738 | 100 % | 626 (84.8 %) | 0 (0.0 %) | 18 (2.4 %) | 94 (12.7 %) |
Le total combiné de 738 est constitué de 116 outils natifs + 391 commandes Codex + 137 appels app + 94 attentes ; les sorties, messages et parties reasoning ne sont pas des outils supplémentaires. Les 94 attentes ont un résultat de disposition non exposé, jamais assimilé à zéro erreur ou à une approbation manuelle. Les appels HTTP internes aux commandes ne sont pas recomptés. Les colonnes de résultats totalisent bien chaque ligne ; les arrondis à une décimale peuvent produire un écart de 0,1 point.

À cette borne : sept tests dédiés et 96 régressions réussis en deux lots, deux compilations réussies, archive unique réussie, delta et production inchangés. Le strict global reste non réussi avec quatre avertissements historiques, sans ERROR nouveau. Aucun commit/push ni inspection Git n’a été effectué. Les seules transmissions externes nécessaires concernent OpenCode Go/Muse et le processus PLLM autorisés, sans secret transmis au modèle. Le rapport, sa vérification puis publication/gate/disarm/release sont des opérations postérieures à cette borne ; le RUN parent continuera en SÉLECTION.
