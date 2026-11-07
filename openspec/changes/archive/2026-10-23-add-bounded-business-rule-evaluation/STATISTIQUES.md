# Statistiques — O06, évaluation bornée des règles métier

Rapport du seul RUN `cismp5-pixs-14f4c2f30c7c47f5`, contexte 635. Archive `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation`.

Collecte arrêtée au relevé final après archivage et publication technique : `2026-10-22 22:49:59 UTC`. La rédaction de ce rapport et la clôture ultérieure sont exclues des compteurs figés. Historique natif HTTP complet de la session `ses_e9ada0666ffe6B16CbOsuYBrmW` et agrégats CAB filtrés ; aucune source de secrets ni réactivation de session n'est nécessaire.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | Agent OpenCode 1.19.3 ; modèle N/A | OpenCode Go (opencode-go) | high ; compactages non exposés | 2.899 s | 371.268 | N/A — génération seule non mesurée |


Moyennes des quatre relèves périodiques valides. Version propre du modèle non exposée : elle n'est pas déduite de son nom. Les deux compactages n'exposent pas leur niveau de raisonnement. Le temps busy comprend outils et attentes ; il ne mesure pas le temps de service du modèle.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex / CGPT — modèle exact non exposé | N/A | OpenAI (outil natif Codex) | N/A | N/A — non sondé | N/A — non sondé | N/A — télémétrie absente |


Aucune sonde de l'orchestrateur. Le dénominateur du temps de service cumulé est inconnu ; aucun pourcentage de service n'est inventé.

## 1. Statistiques générales et décisions

La fenêtre de codage OpenCode commence au `2026-10-22T19:45:50.135334+00:00`. La durée globale inclut aussi la sélection initiale, les pauses, les attentes, les tests et l'archive ; voir section 6. Une réussite d'outil ne prouve pas une approbation manuelle ni une validation métier. Les décisions CAB, les erreurs de transport MCP et les échecs de tests restent distincts.

| Décision CAB | Nombre | Part |
|---|---|---|
| approved | 59 | 93,7 % |
| rejected | 4 | 6,3 % |
| needs_clarification | 0 | 0,0 % |
| pending | 0 | 0,0 % |
| Total | 63 | 100,0 % |


Permissions once : 59, pour 33 écritures et 26 commandes réellement terminées. Une requête MCP a échoué avant enregistrement CAB ; elle est conservée comme erreur technique, pas comme refus de permission.

| Tokens natifs de la session | Nombre | Part du total |
|---|---|---|
| input | 4037955 | 5,7 % |
| output | 192432 | 0,3 % |
| reasoning | 71500 | 0,1 % |
| cache_read | 66882041 | 94,0 % |
| cache_write | 0 | 0,0 % |
| Total | 71183928 | 100,0 % |


Coût estimé natif : 0.590345982000. Devise et unité de facturation non exposées par le schéma API : N/A ; aucune conversion en euros. Les sondes et le benchmark préalable sont séparés de la session de production.

### Sondes de l'agent de codage

| Position | Horodatage UTC réel ou échéance manquée | Mesure | TTMT s | Tokens/s | Sortie tokens | Coût natif |
|---|---|---|---|---|---|---|
| début | 2026-10-22T19:47:16.063171+00:00 | Invalide — filtre SSE | N/A | N/A | 2424 | 0.001935526 |
| +30 min tentative 1 | 2026-10-22T20:17:43.112648+00:00 | Invalide — filtre SSE | N/A | N/A | 2409 | 0.001899326 |
| +30 min tentative 2 | 2026-10-22T20:19:47.075157+00:00 | Valide | 0.970561 | 741.165382 | 2409 | 0.0019154 |
| +60 min tentative 1 | 2026-10-22T20:50:14.110768+00:00 | Valide | 4.397392 | 220.691751 | 2426 | 0.001974726 |
| +90 min tentative 1 | 2026-10-22T21:18:19.215887+00:00 | Valide | 2.370524 | 275.297348 | 2409 | 0.000561174 |
| +120 min tentative 1 | 2026-10-22T21:46:43.745181+00:00 | Valide | 3.856832 | 247.917466 | 2409 | 0.0019416 |
| +150 min | 2026-10-22T22:17:16.063171+00:00 | Manquée | N/A | N/A | N/A | N/A |
| finale apres tache5 | 2026-10-22T22:19:16.023055+00:00 | Valide | 4.212524 | 257.372051 | 2422 | 0.001953 |


Sept créneaux prévus, six exécutés (85,7 %) et un manqué (14,3 %) ; sept tentatives réelles avec une reprise immédiate de la relève +30. Mesures valides : 5/7 (71,4 %) ; deux invalides (28,6 %). Les mesures invalides sont exclues des moyennes. La relève +150 n'a pas été recréée rétroactivement ; la finale est distincte. Les retards réels restent horodatés ; +120 a été anticipée de 32,318 s.

Surcharge des sept sondes générées : 16908 tokens de sortie, coût natif 0.012180752000. Durée totale de service des sondes : N/A — non collectée uniformément. Moyenne des cinq sondes valides, finale incluse : 3.161567 s et 348.488800 tokens/s. Benchmark PLLM initial et deux requêtes supplémentaires dues à l'adaptateur : surcharge distincte, coût complet N/A ; aucune confusion avec ces moyennes.

Compactages OpenCode natifs achevés : 2 (100 % des demandes suivies). API de compactage Codex non exposée ; aucun compactage conjoint revendiqué.

### Résultats du développement

| Contrôle | Résultat vérifié |
|---|---|
| Unitaires | 95 réussis : profil 51 + moteur 34 + manifest 10 |
| Recette PostgreSQL | 13/13 critères sur la base publiée ; dernière preuve call_01a165cdc9c57003b0edd46bdb5a34af |
| Expression exécutable | 6 refus avant activation, 0 activation ; call_01a165a718d374fca52ddef37d5815bf |
| OpenSpec strict | Canon et change valides, issues vides ; call_01a165aaba9577cd986712f1dcba0c19, call_01a165ad5f4e713e90277c26ac61e6b5 |
| Fidélité | 17 artefacts UTF-8/LF sans BOM ; 4 exigences et 5 scénarios, blocs canon/delta/copie identiques |
| Archive | Native exit 0 call_01a165b56af574a1aabacefc20a30c01 ; 6 fichiers déplacés identiques, canon préservé |
| Runtime observé | Python 3.14.9 ; Django 6.1.2 ; PostgreSQL 16.14 ; AST relu avec grammaire Python 3.12 |


La recette PG a été revalidée après des révisions communes, puis sous la même protection conservée jusqu'à publication. Chaque exécution suivie a nettoyé son seul schéma possédé et fermé ses connexions, y compris la première recette échouée. Deux sorties de commandes non nulles ont été corrigées : incompatibilité initiale skip_specs et premier lecteur AUDIT non raccordé. Aucune matrice d'exécution multi-version Python n'est revendiquée.

Avertissement d'archive non bloquant : OpenSpec attend les titres Why/What Changes dans la proposition en français. L'archive a néanmoins terminé avec exit 0 ; les deux validations strictes étaient valides. Deux copies du fichier de tests de profil ont différé seulement par des lignes vides : AST identique, frontière RECONCILED examinée, contenu final testé ; aucune identité octet fictive revendiquée.

## 2. Types de messages et d'outils

| Rôle HTTP natif | Nombre | Part |
|---|---|---|
| user | 237 | 46,7 % |
| assistant | 271 | 53,3 % |
| Total | 508 | 100,0 % |


Le contrôleur SSE observe 507 messages, contre 508 dans l'historique HTTP complet. Écart conservé : 1 message(s), sans recomposition de l'historique SSE.

| Type de partie | Nombre | Part |
|---|---|---|
| text | 499 | 30,9 % |
| step-start | 271 | 16,8 % |
| reasoning | 335 | 20,7 % |
| tool | 237 | 14,7 % |
| step-finish | 271 | 16,8 % |
| compaction | 2 | 0,1 % |
| Total | 1615 | 100,0 % |


| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 172 | 63,5 % |
| stop | 99 | 36,5 % |
| Total | 271 | 100,0 % |


| Outil | Total | Part | Terminé | Erreur | En cours |
|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 16 | 6,8 % | 16 | 0 | 0 |
| cgpt-validation_request_validation | 64 | 27,0 % | 45 | 19 | 0 |
| cgpt-validation_poll_approval | 18 | 7,6 % | 15 | 3 | 0 |
| cgpt-validation_get_approval | 4 | 1,7 % | 4 | 0 | 0 |
| bash | 26 | 11,0 % | 26 | 0 | 0 |
| read | 54 | 22,8 % | 54 | 0 | 0 |
| write | 33 | 13,9 % | 33 | 0 | 0 |
| cgpt-validation_broker_health | 10 | 4,2 % | 10 | 0 | 0 |
| cgpt-validation_list_pending | 10 | 4,2 % | 10 | 0 | 0 |
| cgpt-validation_broker_remediation_registry | 2 | 0,8 % | 2 | 0 | 0 |
| Total | 237 | 100,0 % | 215 | 22 | 0 |


Un bash terminé peut avoir exit 1 : 2 cas sur 26 (7,7 %). Les délais MCP réconciliés ne sont pas transformés en refus CAB. Le contenu des raisonnements et des sorties sensibles n'est pas recopié.

## 3. Fichiers modifiés

Tentatives d'écriture natives approuvées, pas lignes de code. Les chemins ci-dessous désignent les emplacements actuels après déplacement. Le présent rapport est exclu du relevé figé.

| Chemin absolu complet | Approuvées et terminées | Part | Refusées | Erreur outil |
|---|---|---|---|---|
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation/.openspec.yaml` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation/design.md` | 3 | 9,1 % | 0 | 0 |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation/proposal.md` | 3 | 9,1 % | 0 | 0 |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation/requirements.md` | 2 | 6,1 % | 0 | 0 |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation/specs/business-rules/spec.md` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation/tasks.md` | 7 | 21,2 % | 0 | 0 |
| `/home/devops/datas/pixs/openspec/specs/business-rules/spec.md` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/src/pixs/business_rules/__init__.py` | 2 | 6,1 % | 0 | 0 |
| `/home/devops/datas/pixs/src/pixs/business_rules/core_binding.py` | 2 | 6,1 % | 0 | 0 |
| `/home/devops/datas/pixs/src/pixs/business_rules/evaluator.py` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/src/pixs/business_rules/json_contract.py` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/src/pixs/business_rules/manifest.py` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/src/pixs/business_rules/profile.py` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/tests/integration/test_business_rules_pg.py` | 3 | 9,1 % | 0 | 0 |
| `/home/devops/datas/pixs/tests/unit/test_business_rules_evaluator.py` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/tests/unit/test_business_rules_manifest.py` | 1 | 3,0 % | 0 | 0 |
| `/home/devops/datas/pixs/tests/unit/test_business_rules_profile.py` | 2 | 6,1 % | 0 | 0 |
| Total | 33 | 100,0 % | 0 | 0 |


17 fichiers de contenu concernés avant ce rapport : six modules Python, quatre tests et sept documents OpenSpec. Six fichiers du change ont été déplacés vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-23-add-bounded-business-rule-evaluation` par une unique commande d'archive. Les deux écarts de format résolus sur le test de profil ne sont pas des erreurs de l'outil write. Le cache régénérable propre au RUN a été supprimé ; aucun autre cache n'a été supprimé.

## 4. Commandes

| Famille exécutée | Nombre | Part |
|---|---|---|
| Prévol neutre | 4 | 15,4 % |
| OpenSpec — validation | 5 | 19,2 % |
| Python — compilation | 7 | 26,9 % |
| Unitaires | 3 | 11,5 % |
| Python — PostgreSQL | 4 | 15,4 % |
| Lecture ou contrôle ciblé | 2 | 7,7 % |
| OpenSpec — archive | 1 | 3,8 % |
| Total | 26 | 100,0 % |


| Commande, libellé limité à 100 caractères | Occurrences | Part | Exit 0 | Exit non nul |
|---|---|---|---|---|
| `/usr/bin/true` | 4 | 15,4 % | 4 | 0 |
| `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bounded-busin…` | 3 | 11,5 % | 2 | 1 |
| `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate business-rules --…` | 2 | 7,7 % | 2 | 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_business_ru…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_business_ru…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_business_ru…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/tes…` | 4 | 15,4 % | 3 | 1 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/tests/runtime/o06-pycache /home/devops/datas/pixs/.venv…` | 1 | 3,8 % | 1 | 0 |
| `PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import copy,json from pixs.business…` | 1 | 3,8 % | 1 | 0 |
| `/home/devops/datas/pixs/.venv/bin/python3 -B -c 'from pathlib import Path import shutil,platform,js…` | 1 | 3,8 % | 1 | 0 |
| `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bounded-busine…` | 1 | 3,8 % | 1 | 0 |
| Total | 26 | 100,0 % | 24 | 2 |


### Commandes refusées explicitement

| Commande refusée, 100 caractères maximum | Occurrences | Part des refus |
|---|---|---|
| `/usr/bin/true` | 1 | 25,0 % |
| `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_business_ru…` | 1 | 25,0 % |
| `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bounded-busin…` | 1 | 25,0 % |
| `/home/devops/datas/pixs/.venv/bin/python3 -B -c 'from pathlib import Path import hashlib,json expec…` | 1 | 25,0 % |
| Total | 4 | 100,0 % |


Les refus portent sur corrélation/access_id, ressource dupliquée, empreinte copiée incorrectement ou transformation des guillemets. Aucun effet n'a été autorisé par ces demandes. Une autre requête `/usr/bin/true` a échoué avant enregistrement : erreur MCP -32602, comptée séparément (1 occurrence). Les nouveaux mandats possèdent des identifiants neufs ; aucune once consommée n'a été rejouée.

## 5. Accès web

| Accès web natif observé | Nombre | Part du relevé natif | Taux approbation/refus/erreur |
|---|---|---|---|
| Appels | 0 | 0,0 % | N/A — dénominateur nul |
| URL approuvées et visitées | 0 | 0,0 % | N/A |
| URL refusées | 0 | 0,0 % | N/A |
| Erreurs | 0 | 0,0 % | N/A |


Aucun outil web ni URL visitée ou refusée dans l'historique de codage capturé. Les communications avec le fournisseur LLM, les sondes, les API CAB/OpenCode et PostgreSQL sont des échanges de service distincts, pas des visites web déduites.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début effectif | 2026-10-22T19:30:55.454718+00:00 |
| Fin — après archivage et publication, avant rapport | 2026-10-22T22:49:59+00:00 |
| Durée globale, pauses et attentes incluses | 03 h 19 min 04 s |
| Précision | 11943.545282 secondes ; affichage arrondi à la seconde |


En Europe/Paris : 2026-10-22T21:30:55.454718+02:00 → 2026-10-23T00:49:59+02:00. Aucune durée d'agents simultanés n'est additionnée.

| Quota Codex sur 7 jours | Horodatage du relevé | Utilisé | Réinitialisation |
|---|---|---|---|
| Avant | 2026-10-22T19:30:55.454718+00:00 | 7 % | 1793293778 / 2026-10-29T17:09:38+00:00 |
| Après archive et publication | 2026-10-22 22:49:59 UTC | 61 % | 1793293778 / 2026-10-29T17:09:38+00:00 |
| Différence, même compte et même fenêtre | — | 54 points de pourcentage | Fenêtre 10080 min |


Source : outil natif get_usage_limits, rateLimitsByLimitId.codex. Identité de compte et réinitialisation vérifiées égales depuis les réponses originales. Le quota est partagé : cette variation peut inclure les autres tâches simultanées et n'est pas attribuée exclusivement à O06. Le relevé intermédiaire antérieur à la révalidation post-archive n'est pas présenté comme final.

### Totaux croisés des intentions et consultations de codage

Cette vue remplace chaque demande request_validation et son effet par une intention unique ; les consultations read et MCP de contrôle restent des appels distincts. Elle ne s'ajoute pas au total natif de la section 2. Réussite signifie effet ou consultation terminés selon cette convention ; les approbations CAB de commandes peuvent néanmoins avoir un exit non nul.

| Domaine | Total | Part globale | Réussites | Taux | Refus | Taux | Erreurs | Taux |
|---|---|---|---|---|---|---|---|---|
| Fichiers | 33 | 18,5 % | 33 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| Commandes | 31 | 17,4 % | 24 | 77,4 % | 4 | 12,9 % | 3 | 9,7 % |
| Web observé | 0 | 0,0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres consultations et contrôles | 114 | 64,0 % | 111 | 97,4 % | 0 | 0,0 % | 3 | 2,6 % |
| Global observé | 178 | 100,0 % | 168 | 94,4 % | 4 | 2,2 % | 6 | 3,4 % |


Le pilotage Codex complet n'est pas exposé par ces API : compteurs et temps de service de l'orchestrateur N/A. La télémétrie ne fabrique donc pas un total toutes sources confondues.

| Observation CAB du seul contexte | Valeur |
|---|---|
| Date du relevé agrégé | 2026-10-22T22:50:21.416Z |
| Busy natif, outils/attentes inclus | 4637.693 s |
| Attente ressource connue | 0.0 s |
| Détention partagée | 4548.407 s |
| Activité exclusive | 0.0 s |
| Réconciliation ciblée /locks/reconcile | 0 |
| Gels exceptionnels observés | 0.0 s |


Ces durées peuvent se recouvrir et ne s'additionnent pas. La sélection porte sur ce seul RUN ; aucun gain causal de parallélisme ni état global des autres RUN n'est déduit.

Publication technique CAB durable : référence 61, transaction `o06-publish-df01e0059fcf482a9f5fcf5f81972b4d`. Le contexte est limité au seul rapport en phase REPORT. Le gate, le désarmement et la libération sont ultérieurs à ce relevé ; le checkpoint conserve leurs preuves sans réécrire les statistiques.

État vérifié : 95 unitaires réussis, 13 critères PG courants réussis, six refus avant activation, deux stricts OpenSpec valides, archive unique vérifiée et cache propre supprimé. Aucun fichier Core/backend n'a été écrit par ce RUN. C09/C10 restent synthétiques dans la recette ; aucune activation P0, aucun changement d'interface ni qualification globale du produit. Les contrôles navigateur sont non applicables. Git : aucune commande, aucun commit ni push de ce RUN. Aucun secret n'est introduit dans les fichiers revus ; les valeurs PG restent dans le processus de test masqué et les clés fournisseur hors du modèle.
