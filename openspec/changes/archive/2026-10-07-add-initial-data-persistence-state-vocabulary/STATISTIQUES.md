# Statistiques de session — add-initial-data-persistence-state-vocabulary

RUN : `cismp-pixs-20261007-061019` ; session persistante : `ses_eea8a1e72ffeOAiwkcLCyeMI1e` ; archive : `openspec/changes/archive/2026-10-07-add-initial-data-persistence-state-vocabulary`. Intervalle : du message `msg_1157aaa630013Y04iFOB4V4M0y` au dernier rapport d'archive `msg_115c1a48900110b9iwm6MMhD6E`, fin de collecte horodatée ci-dessous. Préparation, code, corrections, validations, récupération et archive inclus ; rédaction/écriture du présent rapport et changes précédents exclus.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Qwen3.8 Flash / qwen3.8-flash | N/A — version exacte non publiée | opencode-go | xhigh | 2,4007 s | 77,42 | N/A — génération isolée non mesurable ; durées natives mêlent outils/attentes. OpenCode 1.18.34 est la version de l'outil. |


### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root (famille GPT-6 déclarée par plateforme) | N/A | OpenAI | N/A | N/A | N/A | N/A — télémétrie modèle du thread indisponible |


Temps de service cumulé et ses parts : N/A, dénominateur non mesurable. Activité de pilotage et sondes peuvent chevaucher le codage ; la durée calendaire ne mesure pas la génération.

## 1. Statistiques générales et décisions

Durée calendaire : 1 h 18 min 44,810 s (pauses, attentes, tests, récupération et archivage inclus). Début 2026-10-07T08:28:42.979Z ; fin après archive/sonde finale 2026-10-07T09:47:27.789Z. Historique natif complet : 202 messages ; 188 dans les bornes retenues.

| Mesure | Effectif | Part |
|---|---|---|
| Messages | 188 | 100 % |
| user | 43 | 22,9 % |
| assistant | 145 | 77,1 % |
| Décisions CAB explicites uniques | 31 | 100 % |
| APPROVED | 27 | 87,1 % |
| REJECTED | 4 | 12,9 % |
| Clarification | 0 | 0,0 % |
| Appels outils natifs | 142 | 100 % |
| completed | 132 | 93,0 % |
| error/interrompus | 10 | 7,0 % |


Tokens natifs de production : input 896, output 74180, reasoning 0, cache_read 12824592, cache_write 283889 ; coût 0,296970272 (devise N/A, non publiée). Une compaction native, message `msg_115b797e2001sxaJSFBUlcXbds`, finish stop, Qwen/opencode-go ; ses 4 085 tokens output et coût 0,022885650 sont inclus. Compactage natif orchestrateur : API absente, aucune réussite conjointe déclarée.

Développement : 19 exécutions de tests réussies (100 %) : 1 unitaire (5,3 %), 1 intégration (5,3 %), 17 régressions (89,5 %). Trois compilations exit 0 (100 %) ; quatre stricts pré/post exit 0 (100 %) ; deux globaux exit 1 natifs, qualifiés par identité des 19 WARNING/0 ERROR et des résumés 76 specs/77 items. Cinq tâches cochées sur preuves ; delta canonique identique ; 145 empreintes sans dérive ; trois fichiers Python exacts UTF-8/LF. Les commandes refusées ne sont pas des tests exécutés.

### Sondes de l'agent de codage

| Position / essai | Valide | Tokens | TTMT (s) | Tokens/s | Coût |
|---|---|---|---|---|---|
| début #1 | non | 593 | N/A — SSE rôle invalide | N/A — exclu | 0,003045410 |
| fin émise prématurément par arrêt du collecteur défectueux #1 | non | 575 | N/A — SSE rôle invalide | N/A — exclu | 0,000492414 |
| début #2 | oui | 520 | 2,8492 | 89,42 | 0,000466564 |
| +30 min #1 | oui | 600 | 2,1392 | 61,99 | 0,003048700 |
| +60 min #1 | oui | 531 | 2,1324 | 81,99 | 0,003016270 |
| fin #1 | oui | 523 | 2,4819 | 76,27 | 0,003012510 |


| Position / essai | Envoi UTC | Premier / dernier SSE texte UTC | Session / message |
|---|---|---|---|
| début #1 | 2026-10-07T08:29:43.796580+00:00 | 2026-10-07T08:29:43.860420+00:00 / 2026-10-07T08:29:55.030103+00:00 | ses_eea846817fferO00Bmmy8RLlM6 / msg_1157b9853001hZANvjevjoUeIy |
| fin émise prématurément par arrêt du collecteur défectueux #1 | 2026-10-07T08:31:31.688436+00:00 | 2026-10-07T08:31:31.744495+00:00 / 2026-10-07T08:31:40.481142+00:00 | ses_eea82c2a3ffeHpfqM56tIFakx0 / msg_1157d3db8001yEiik8rpcwG2I7 |
| début #2 | 2026-10-07T08:32:10.225776+00:00 | 2026-10-07T08:32:13.075024+00:00 / 2026-10-07T08:32:18.890395+00:00 | ses_eea822c18ffeG464tkwoY1Nij4 / msg_1157dd44300186A3t65aVnIwlg |
| +30 min #1 | 2026-10-07T08:59:43.849166+00:00 | 2026-10-07T08:59:45.988338+00:00 / 2026-10-07T08:59:55.666569+00:00 | ses_eea68f0b5ffebPv2CXFcSvcy8r / msg_115970fb7001SWe0i43Tagy7FJ |
| +60 min #1 | 2026-10-07T09:29:43.812606+00:00 | 2026-10-07T09:29:45.945038+00:00 / 2026-10-07T09:29:52.421207+00:00 | ses_eea4d7996ffexffpJWzbLA5KKa / msg_115b286fc001z40O0qkxJA1KuD |
| fin #1 | 2026-10-07T09:46:38.644133+00:00 | 2026-10-07T09:46:41.126077+00:00 / 2026-10-07T09:46:47.983364+00:00 | ses_eea3dfd5bffeGAN7uH2ZRwzi4w / msg_115c20300001XRlLS7r3mqGLZC |


Cadence conservée depuis 08:29:43.750381Z, sondes sans outil/fichier/réseau généré, même prompt déterministe de 40 lignes et configuration Qwen/opencode-go/xhigh. Quatre positions prévues (début, +30, +60, fin), quatre réussies (100 %), zéro échouée/manquée (0 %). Six tentatives : quatre valides (66,7 %), deux invalides (33,3 %). La première collecte prenait l'écho utilisateur comme premier SSE ; ses deux mesures sont exclues, dont une fin incidente prématurée lors de l'arrêt du collecteur. Une reprise du début après correction du filtre de rôle a réussi avant le premier code ; aucune relève reconstituée rétroactivement.

Moyennes sur quatre sondes valides : TTMT 2,4007 s (min 2,1324, max 2,8492), débit 77,42 tokens/s (min 61,99, max 89,42). Surcharge hors production : 3342 tokens, coût 0,013081868, 58,504 s cumulées ; invalides 1168 tokens, coût 0,003537824.

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 95 | 14,2 % |
| step-start | 145 | 21,6 % |
| reasoning | 145 | 21,6 % |
| tool | 142 | 21,2 % |
| step-finish | 142 | 21,2 % |
| compaction | 1 | 0,1 % |
| Total | 670 | 100 % |


| Fin de réponse assistant | Nombre | Part |
|---|---|---|
| tool-calls | 104 | 71,7 % |
| stop | 38 | 26,2 % |
| interrupted | 3 | 2,1 % |
| Total | 145 | 100 % |


| Outil | Total (part des 142) | Completed (taux ligne) | Error/interrompu (taux ligne) |
|---|---|---|---|
| read | 37 (26,1 %) | 36 (97,3 %) | 1 (2,7 %) |
| glob | 8 (5,6 %) | 8 (100,0 %) | 0 (0,0 %) |
| grep | 5 (3,5 %) | 5 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 31 (21,8 %) | 24 (77,4 %) | 7 (22,6 %) |
| bash | 16 (11,3 %) | 16 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 11 (7,7 %) | 11 (100,0 %) | 0 (0,0 %) |
| write | 7 (4,9 %) | 7 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 10 (7,0 %) | 8 (80,0 %) | 2 (20,0 %) |
| edit | 4 (2,8 %) | 4 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 7 (4,9 %) | 7 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 6 (4,2 %) | 6 (100,0 %) | 0 (0,0 %) |
| Total | 142 (100 %) | 132 (93,0 %) | 10 (7,0 %) |


Convention : completed décrit l'appel, ne prouve ni une approbation manuelle ni la conformité de son résultat. Les 27 effets natifs (11 éditions, 16 Bash) ont chacun leur APPROVED unique ; 4 décisions REJECTED sont sans effet. Parmi les 10 statuts error, quatre demandes rejetées sont classées en refus, six en erreur technique (lecture absente, délais MCP/polling interrompu). L'édition 55 completed divergeait du texte gelé : un écart de conformité, corrigé par 56. Les deux globaux exit 1 sont qualifiés séparément, jamais présentés comme exit 0.

## 3. Fichiers modifiés

Douze tentatives d'édition au sens autorisation : onze éditions réellement exécutées sous APPROVED (91,7 %), une demande d'édition refusée sans écriture (8,3 %). Conformité au texte gelé : dix succès, un écart initial 55 corrigé. Les chemins OpenSpec ci-dessous désignent leur destination finale après archivage.

| Chemin absolu | Tentatives (part des 12) | Approuvées conformes | Refusées sans effet | Écart de conformité |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-persistence-state-vocabulary/proposal.md | 1 (8,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-persistence-state-vocabulary/design.md | 2 (16,7 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-persistence-state-vocabulary/tasks.md | 3 (25,0 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-persistence-state-vocabulary/specs/data-lifecycle/spec.md | 1 (8,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_persistence.py | 2 (16,7 %) | 1 (50,0 %) | 0 (0,0 %) | 1 (50,0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_persistence_vocabulary.py | 2 (16,7 %) | 1 (50,0 %) | 1 (50,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_persistence_vocabulary_integration.py | 1 (8,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 12 (100 %) | 10 (83,3 %) | 1 (8,3 %) | 1 (8,3 %) |


Hors éditions : .openspec.yaml créé par la commande native new change ; cinq artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-persistence-state-vocabulary par l'archive autorisée, empreintes identiques. État orchestrateur /home/devops/datas/pixs/output/cismp-state.json mis à jour hors des outils OpenCode ; compteurs natifs orchestrateur N/A. Source canonique, façades et références antérieures inchangées.

## 4. Commandes

Dix-neuf demandes de commande : seize exécutées sous APPROVED (84,2 %), trois refusées sans Bash (15,8 %). Parmi les seize natives : quatorze exit 0 (87,5 %), deux exit 1 qualifiés (12,5 %), aucune erreur d'exécution ; aucune commande rejouée sous une décision consommée.

| Famille native | Nombre | Part des 16 | exit 0 | exit 1 qualifié |
|---|---|---|---|---|
| openspec new change | 1 | 6,3 % | 1 (100,0 %) | 0 (0,0 %) |
| stricts ciblés pré/post | 4 | 25,0 % | 4 (100,0 %) | 0 (0,0 %) |
| py_compile | 3 | 18,8 % | 3 (100,0 %) | 0 (0,0 %) |
| tests unit/intégration/régression | 3 | 18,8 % | 3 (100,0 %) | 0 (0,0 %) |
| tests CAB /usr/bin/true | 2 | 12,5 % | 2 (100,0 %) | 0 (0,0 %) |
| globaux OpenSpec | 2 | 12,5 % | 0 (0,0 %) | 2 (100,0 %) |
| archive | 1 | 6,3 % | 1 (100,0 %) | 0 (0,0 %) |
| Total | 16 | 100 % | 14 (87,5 %) | 2 (12,5 %) |


| Commande native (libellé ≤100 caractères) | Occurrences (part des 16) | Codes natifs |
|---|---|---|
| /home/devops/.local/npm/bin/openspec new change add-initial-data-persistence-state-vocabulary | 1 (6,3 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-data-persistence-state-vocabulary --strict | 2 (12,5 %) | 0, 0 |
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --type spec --strict | 2 (12,5 %) | 0, 0 |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_persistence.py | 1 (6,3 %) | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_persistence_vocabulary.py | 1 (6,3 %) | 0 |
| /usr/bin/true | 2 (12,5 %) | 0, 0 |
| PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p tes… | 1 (6,3 %) | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_persistence_vocab… | 1 (6,3 %) | 0 |
| PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration… | 1 (6,3 %) | 0 |
| PYTHONPATH=src:tests/unit:tests/integration /home/devops/python/current/bin/python3 -B -m unittest … | 1 (6,3 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json --report findings | 1 (6,3 %) | 1 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json --report findings | 1 (6,3 %) | 1 |
| /home/devops/.local/npm/bin/openspec archive add-initial-data-persistence-state-vocabulary --yes --… | 1 (6,3 %) | 0 |


Commandes refusées — demandes seulement, jamais exécutées :

| requestId | Commande demandée (≤100 caractères) | Part des 3 refus |
|---|---|---|
| cismp-pixs-20261007-061019-persistence-unit-run-60 | /home/devops/python/current/bin/python3 -B -c 'import sys sys.path[:0]=["src","tests"] import unitt… | 1 (33,3 %) |
| cismp-pixs-20261007-061019-persistence-regression-68 | PYTHONPATH=src:tests /home/devops/python/current/bin/python3 -B -m unittest -v tests.unit.test_data… | 1 (33,3 %) |
| cismp-pixs-20261007-061019-persistence-regression-69 | PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p tes… | 1 (33,3 %) |


60 reformulait la commande avec exit=False ; 68 reformulait une commande dont le chemin fourni par Codex était incomplet ; 69 était anticipée sans mandat. Refus, abort et réconciliation ont empêché les effets. Régression corrigée 71 : 17 OK. Test CAB 70 : /usr/bin/true exit 0 unique et readiness final READY/0. Le refus d'édition supplémentaire 58 concernait un requestId différent du mandat, corrigé avant écriture.

## 5. Accès web

Agent de codage : aucun outil web ni URL visitée (0/142, 0,0 %) ; zéro approbation, refus, erreur web, taux internes N/A (dénominateur nul). Orchestrateur : aucun outil web pendant cet intervalle ; réseau interne de génération N/A. Les échanges HTTP locaux de pilotage/CAB/SSE et les sondes fournisseur sont distingués des visites web. Aucune URL refusée présentée comme visitée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-07T08:28:42.979Z (UTC) |
| Fin — après archivage et sonde finale | 2026-10-07T09:47:27.789Z (UTC) |
| Durée globale (pauses et attentes incluses) | 1 h 18 min 44,810 s |


| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-07T08:28:42.776Z (tentative, UTC) | N/A — outil absent | N/A |
| Après — après archivage de la spécification | 2026-10-07T09:47:27.789Z (tentative, UTC) | N/A — outil absent | N/A |
| Différence après − avant | — | N/A | — |


L'outil natif mcp__codex_app__get_usage_limits était absent avant et reste absent à la vérification après archive/sonde finale. Compte et fenêtre de 10 080 minutes invérifiables ; aucune valeur reconstruite. Quotas partagés par compte, exclusivité de consommation non vérifiable.

| Domaine | Appels (part globale) | Succès conformes | Refusés | Erreurs techniques/conformité | Qualifiés |
|---|---|---|---|---|---|
| Éditions natives | 11 (7,7 %) | 10 (90,9 %) | 0 (0,0 %) | 1 (9,1 %) | 0 (0,0 %) |
| Commandes natives | 16 (11,3 %) | 14 (87,5 %) | 0 (0,0 %) | 0 (0,0 %) | 2 (12,5 %) |
| Web | 0 (0,0 %) | N/A | N/A | N/A | N/A |
| Autres outils (lecture/CAB) | 115 (81,0 %) | 105 (91,3 %) | 4 (3,5 %) | 6 (5,2 %) | 0 (0,0 %) |
| Total | 142 (100 %) | 129 (90,8 %) | 4 (2,8 %) | 7 (4,9 %) | 2 (1,4 %) |


Totaux croisés : 11 + 16 + 115 = 142 ; 129 + 4 + 7 + 2 = 142 ; 27 APPROVED + 4 REJECTED = 31 décisions. Les refus d'édition/commande sont comptés une fois au niveau des demandes CAB dans ce tableau des outils, sans les ajouter comme effets natifs.

Incidents conservés : écart de texte 55 corrigé par 56 ; critères design/tasks corrigés pour comparer les imports après la façade existante ; rapport 64 annonçant à tort un edit inexistant écarté, première vraie exécution vérifiée ensuite ; refus 58/60/68/69 sans effet ; délais récupérés sans resoumission de demande enregistrée ; compaction native de récupération ; compteur readiness pending temporairement périmé réconcilié à zéro. Le comparateur root a été corrigé pour comparer la valeur JSON et non l'identité d'objet, sans rejouer une validation.

Résultat : 19 tests OK, 3 compilations et 4 stricts exit 0, globaux exit 1 qualifiés exacts (19 WARNING/0 ERROR, 76/77 items), 145 références intactes, cinq tâches prouvées, archive exit 0 avec validation conservée et --skip-specs. PostgreSQL et navigateur : non nécessaires, non exécutés. Git : non inspecté, aucun commit/push/branche. Secrets : aucun accès pendant cet intervalle de travail observé. Livraison partielle : vocabulaire de persistance déclaratif ; aucune transition, suppression, purge ou tombstone exécuté. Retour au parent SÉLECTION après vérification du présent rapport ; aucune déclaration de cycle global TERMINÉ.
