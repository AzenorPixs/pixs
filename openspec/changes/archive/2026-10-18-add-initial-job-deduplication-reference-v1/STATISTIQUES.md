# STATISTIQUES — add-initial-job-deduplication-reference-v1

RUN : `cismp2-pixs-9b4f48c87f99466e` ; contexte CAB : `300` ; session de codage : `ses_eb0aed052ffedkgcJ4a11PIs84`. Archive : `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-job-deduplication-reference-v1`.

Bornes de production du change : 2026-10-18T16:01:23+02:00 → 2026-10-18T16:16:49+02:00. Le RUN parent a commencé à 2026-10-18T15:50:19+02:00 ; son inventaire initial et l'attente de validation humaine restent dans sa durée globale. Les compteurs ci-dessous portent sur la session du change, pas sur les RUN voisins. Les opérations de rédaction, édition et contrôle du présent rapport sont hors intervalle ; leurs preuves restent dans le checkpoint.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go / opencode-go | high | 2,494 s — 1 mesure finale valide | N/A — flux natif bufferisé | N/A — durée de génération isolée absente |


### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex — session principale | N/A — identifiant modèle exact non exposé | OpenAI | N/A — télémétrie absente | N/A — non sondé | N/A — non sondé | N/A — télémétrie absente |


Les 94 messages assistant observés emploient Muse / opencode-go / high. La version du modèle n'est pas déduite de son nom. Dénominateur du temps de service : N/A, aucune durée active de génération isolée pour les deux catégories ; ni la durée calendaire ni busy ni le temps des outils ne sont assimilés à ce temps. Les compteurs propres à Codex, tokens/coût compris, sont N/A faute de télémétrie complète exposée.

## 1. Statistiques générales et décisions

Convention : approuvé et exécuté désigne un outil natif terminé sans erreur, autorisé automatiquement ou explicitement ; cela ne prouve pas une approbation manuelle. Les 26 opérations nécessitant une permission native disposent séparément d'une décision CGPT corrélée et d'une permission once. Un appel Bash terminé avec exit 1 reste distingué d'une erreur technique de l'outil.

| Mesure | Valeur | Part / taux |
|---|---|---|
| Appels d’outils | 76 | 100 % |
| Approuvés et exécutés | 74 | 97.4 % |
| Refus de permission observés | 0 | 0.0 % |
| Erreurs techniques MCP | 2 | 2.6 % |
| Mandats CAB approuvés | 26 | 100 % des 26 décisions |
| Mandats CAB rejetés / clarification / en attente | 0 / 0 / 0 | 0,0 % chacun |
| Permissions once corrélées | 26 | 100 % des 26 opérations à permission |
| Change livré et archivé | 1 | 100 % du périmètre demandé |
| Tâches prouvées et cochées | 8 | 100 % |
| Tests réussis | 40 | 100 % ; 0 échec, 0 ignoré |
| Nouveaux tests du profil | 14 | 35,0 % des 40 tests |
| Compilations réussies | 3 | 100 % |


Tokens cumulés de production (répétitions/cache inclus, non uniques) : total=10582420, input=336149, output=32263, reasoning=3021, cache_read=10210987, cache_write=0. Coût natif déclaré : 0.061093674 sur 94/94 réponses ; la devise n'est pas exposée dans ces messages. Coût de l'orchestrateur : N/A. Compactions natives observées : 0 (0,0 % des 94 réponses) ; aucune échéance de 90 minutes atteinte.

Deux erreurs techniques conservées : timeout de request_validation et interruption de son poll_approval lors du mandat de création à révision périmée. Aucun APPROVED, once ou effet natif pour cette demande ; get_approval puis cancel_approval puis get_approval prouvent CANCELLED. Prévol neuf et création neuve ensuite réussis. L'erreur HTTP decision-run-divergent a été réconciliée sans décision appliquée avant sa nouvelle transmission ; les tentatives HTTP et les refus de permission ne sont pas confondus.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part |
|---|---|---|
| assistant | 94 | 74.0 % |
| user | 33 | 26.0 % |
| Total | 127 | 100 % |


| Type de partie | Nombre | Part |
|---|---|---|
| reasoning | 94 | 19.5 % |
| step-finish | 93 | 19.3 % |
| step-start | 94 | 19.5 % |
| text | 125 | 25.9 % |
| tool | 76 | 15.8 % |
| Total | 482 | 100 % |


| Terminaison assistant | Nombre | Part |
|---|---|---|
| interrompue/non exposée | 1 | 1.1 % |
| stop | 29 | 30.9 % |
| tool-calls | 64 | 68.1 % |
| Total | 94 | 100 % |


| Type d’outil | Total | Part globale | Approuvé et exécuté | Refusé | Erreur technique |
|---|---|---|---|---|---|
| bash | 16 | 21.1 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 4 | 5.3 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 | 1.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 | 2.6 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 1.3 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| cgpt-validation_request_validation | 27 | 35.5 % | 26 (96.3 %) | 0 (0.0 %) | 1 (3.7 %) |
| edit | 2 | 2.6 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 3 | 3.9 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 12 | 15.8 % | 12 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 10.5 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 76 | 100 % | 74 (97.4 %) | 0 (0.0 %) | 2 (2.6 %) |


## 3. Fichiers modifiés

Il s'agit de tentatives d'édition natives, pas de lignes de code. Les chemins ci-dessous sont les cibles originales observées avant archivage.

| Chemin absolu complet | Total et part | Écritures approuvées | Refusées | En erreur |
|---|---|---|---|---|
| /home/devops/datas/pixs/TECHNICAL.md | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-deduplication-reference-v1/design.md | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-deduplication-reference-v1/proposal.md | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-deduplication-reference-v1/specs/jobs/spec.md | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-job-deduplication-reference-v1/tasks.md | 2 (20.0 %) | 2 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/jobs/spec.md | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/job_deduplication_reference.py | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_job_deduplication_reference_integration.py | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_job_deduplication_reference.py | 1 (10.0 %) | 1 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 10 (100 %) | 10 (100 %) | 0 (0,0 %) | 0 (0,0 %) |


Neuf chemins édités directement ; le fichier `/home/devops/datas/pixs/openspec/changes/add-initial-job-deduplication-reference-v1/.openspec.yaml` a été créé par la commande OpenSpec distincte, et non par une édition native supplémentaire. Le dossier complet à cinq artefacts a été déplacé par l'archivage autorisé vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-job-deduplication-reference-v1` ; toutes ses empreintes sont préservées. Les seules sources nouvelles sont le module Python et ses deux tests. Les deux modifications existantes sont les insertions RSMP jobs et TECHNICAL §23. Caches de compilation régénérables et répertoires temporaires de tests restent des artefacts techniques ; les temporaires sont nettoyés par les tests.

## 4. Commandes

| Famille | Occurrences | Part |
|---|---|---|
| Compilation Python | 3 | 18.8 % |
| OpenSpec | 10 | 62.5 % |
| Prévol /usr/bin/true | 2 | 12.5 % |
| Tests unittest | 1 | 6.2 % |
| Total | 16 | 100 % |


| Commande exacte ou libellé tronqué à 100 caractères | Occurrences | Part |
|---|---|---|
| /home/devops/.local/npm/bin/openspec archive add-initial-job-deduplication-reference-v1 --skip-sp... | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec new change add-initial-job-deduplication-reference-v1 | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 6.2 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 4 | 25.0 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-job-deduplication-reference-v1 --type c... | 2 | 12.5 % |
| /home/devops/.local/npm/bin/openspec validate jobs --type spec --strict --json | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/job_deduplication_referen... | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_job_deduplication_... | 1 | 6.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_job_deduplication_referen... | 1 | 6.2 % |
| /usr/bin/env PYTHONPATH=src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python... | 1 | 6.2 % |
| /usr/bin/true | 2 | 12.5 % |
| Total | 16 | 100 % |


Commandes refusées par permission native : aucune, 0/16 (0,0 %). Une demande de création périmée a été annulée sans exécution : elle ne compte pas comme commande exécutée ni comme refus de permission. Quatre exécutions strictes globales retournent exit 1 (25,0 % des 16 commandes) pour les mêmes quatre warnings de longueur ; les douze autres commandes retournent exit 0 (75,0 %). Aucun ERROR OpenSpec nouveau.

## 5. Accès web

| Accès web natifs de la session du change | Nombre | Part / taux |
|---|---|---|
| Approuvés et visités | 0 | N/A — dénominateur nul |
| Refusés | 0 | N/A — dénominateur nul |
| Erreurs | 0 | N/A — dénominateur nul |
| Total | 0 | N/A — dénominateur nul |


Aucun outil web natif ni navigateur utilisé ; aucune URL refusée observée. Hors de ces compteurs, la vérification PLLM autorisée par le développeur a appelé les endpoints fournisseur ci-dessous avant la production. Ce sont des accès API, pas des visites navigateur ; leur comptage HTTP exhaustif et leurs taux sont N/A dans la télémétrie native. Les échanges de génération OpenCode vers son fournisseur ne sont pas reclassés artificiellement en outils web.

- Approuvé et appelé : https://opencode.ai/zen/go/v1/usage
- Approuvé et appelé : https://opencode.ai/zen/go/v1/models
- Approuvé et appelé : https://opencode.ai/zen/go/v1/responses

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début du RUN | 2026-10-18T15:50:19+02:00 |
| Fin — après archivage et sonde finale | 2026-10-18T16:16:49+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 26 min 29 s |
| Début de la session du change | 2026-10-18T16:01:23+02:00 |
| Durée propre au change, attentes incluses | 00 h 15 min 25 s |


| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-18T15:50:19+02:00 (consignation du relevé natif) | 9 % | 2026-10-25T01:23:28+02:00 |
| Après — après archivage de la spécification | 2026-10-18T16:16:49+02:00 | 11 % | 2026-10-25T01:23:28+02:00 |
| Différence après − avant | — | 2 points de pourcentage | — |


Les deux relevés proviennent de l'outil natif get_usage_limits, quota codex, fenêtre 10080 minutes et même réinitialisation. L'horodatage initial est celui de sa consignation dans le checkpoint. Les quotas sont partagés par le compte : cette variation peut inclure d'autres tâches et ne lui est pas attribuée exclusivement. Le relevé intermédiaire avant la reprise du change indiquait 10 % utilisés ; la différence depuis cette reprise vaut 1 point.

| Domaine natif | Nombre | Part globale | Approuvé et exécuté | Refusé | Erreur technique |
|---|---|---|---|---|---|
| Fichiers | 10 | 13.2 % | 10 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commandes | 16 | 21.1 % | 16 (100 %) | 0 (0,0 %) | 0 (0,0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 50 | 65.8 % | 48 (96,0 %) | 0 (0,0 %) | 2 (4,0 %) |
| Total | 76 | 100 % | 74 (97.4 %) | 0 (0,0 %) | 2 (2.6 %) |


Sondes du modèle de codage : 2 prévues, 2 réponses réussies (100 %), 0 échouée, 0 manquée ; aucune échéance +30 minutes n'est survenue avant la fin. Même prompt fixe de 128 entiers, modèle/fournisseur/high, zéro outil dans deux sessions dédiées supprimées après contrôle. Mesure initiale TTMT non concluante : le premier événement enregistré n'était pas qualifié comme sortie générée ; elle est exclue. Sonde finale : TTMT 2,494 s au premier événement assistant non vide, 1/2 mesure valide (50 %). Débits sondés : 0/2 valides (0 %), N/A car flux natifs bufferisés. Le benchmark PLLM frais (TTFT 7,2706 s, palier 2048) reste distinct de ces moyennes.

Surcharge des sondes, exclue des tokens/coûts de production : 1737 tokens de sortie et raisonnement, 17812 tokens d'entrée ; durée calendaire cumulée des deux sondes 8.515 s, qui n'est pas un temps de service. Coût des sondes : N/A, non conservé. Version exacte : N/A.

Sources : brouillon Markdown et export JSON /runs/cismp2-pixs-9b4f48c87f99466e/statistics?contextId=300, historique natif de la session, relevés natifs de quota et checkpoint. Les agrégats CAB consultés après la borne contiennent aussi la supervision ultérieure : les messages, parties, outils, tokens et coûts sont donc recalculés depuis les messages terminés avant la borne ; une réponse interrompue reste explicitement conservée. Les observations postérieures ne sont pas ajoutées au bilan de production. Les compteurs de coordination ne prouvent pas un gain causal : attente de ressources 0 s, détention partagée 240,326 s, gel global 0 s, sans addition de durées recouvrantes.

Résultat : 40/40 tests et 3/3 compilations ; strict jobs et change sans issue ; standard global 186/186 avant archive ; strict global avant/après archive limité aux quatre warnings historiques identiques et zéro ERROR. Huit tâches cochées sur preuves. Archivage réussi, cinq empreintes conservées, publication CAB `publish-424a9376c6e34584`, référence 36. Rapport à vérifier avant gate et livraison ; le gate n'est pas déduit du brouillon.

Aucun commit, push ou inspection Git effectué ; provenance Git non revendiquée. Aucun provider, migration, runtime, interface ou déploiement ajouté. PostgreSQL et navigateur : sans objet dans ce profil pur. Les seuls accès externes observés concernent la PLLM autorisée. Aucune valeur secrète exposée à l'agent, affichée ou transmise au modèle ; l'usage PLLM est resté dans le processus sécurisé dédié ; seuls des marqueurs synthétiques sont employés dans les tests. La conformité de périmètre est fondée sur les appels natifs, les contenus exacts et les empreintes, pas sur un diff Git.
