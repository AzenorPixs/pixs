# STATISTIQUES — C06, Core HTTP protégé

Projet : Pixs l'Application Universelle (pixs). Archive : 2026-10-22-add-protected-core-http-commands-and-queries.

RUN : cismp5-pixs-1f3e128ad89f45a9 ; job : cismp5-c06-34960d24111a4362 ; contexte CAB : 529.

### Agents de codage

| Agent / rôle | Fournisseur et modèle | Raisonnement / version | Périmètre |
| --- | --- | --- | --- |
| OpenCode maître, session initiale puis récupération | opencode-go / muse-spark-1.3-contributor | high vérifié par configuration et sondes ; version exacte N/A non exposée | Deux sessions natives ; OpenCode 1.19.3, CAB 1.7.1 |
| Sessions auxiliaires de sondes | opencode-go / muse-spark-1.3-contributor | high observé ; version N/A | Sans outil, sans code métier, archivées individuellement |
Sessions maîtresses : ses_ea3350e14ffeCHibtjeEso66gG, ses_e9f5bce2fffeUS0Sa7bfjn9kV8. Aucune nouvelle session ne remplace rétroactivement les preuves de l'ancienne.

### Agents orchestrateurs

Codex, chat 01a15b3d-fa4d-7d23-a242-8cd9f80983da. Modèle exact et niveau internes : N/A, non exposés par une source native fiable de collecte. Ses tokens, coûts et appels d'outils complets : N/A ; les totaux OpenCode ne sont pas des totaux Codex. Les décisions CGPT sont conservées séparément dans le checkpoint.

## 1. Statistiques générales et décisions

Période C06 : 2026-10-21T04:49:26+00:00 → 2026-10-22T01:41:07.045000+00:00, durée calendaire 20 h 51 min 41 s. Elle inclut pause humaine, attente C03/CAB, reprise, corrections, tests et archivage. Ce n'est pas un temps de codage productif. Le RUN a une phase préliminaire antérieure à C06, dont le quota initial est conservé séparément.

| Mesure | Nombre | Part / source |
| --- | --- | --- |
| Demandes suivies dans le checkpoint | 134 | 100 % |
| Décisions approved | 128 | 95.52 % |
| Décisions rejected | 4 | 2.99 % |
| Annulations sans décision | 2 | 1.49 % |
| Messages OpenCode maîtres | 1255 | Deux historiques natifs, après début C06 |
| Appels d'outils OpenCode | 627 | 100 % des parties tool collectées |
| Erreurs techniques d'outils | 27 | 4.31 % |
| Fichiers Python compilés | 33 | 33/33 |
| Unitaires finaux | 166 | 166/166, 100 % |
| Cas PostgreSQL finaux | 192 | 192/192, 100 %, neuf recettes |
Les refus d'autorisation, erreurs techniques MCP, divergences de contenu et échecs de tests sont distincts. Une décision approuvée n'est ni un résultat de test ni une preuve de conformité du contenu écrit. Les permissions natives once et leurs fins sont corrélées par appel.

| Compteur de tokens natif OpenCode | Valeur |
| --- | --- |
| total | 226 809 206 |
| input | 10 481 253 |
| output | 527 027 |
| reasoning | 124 775 |
| cache_read | 215 676 151 |
| cache_write | 0 |
Ces compteurs incluent les lectures de cache selon le schéma natif ; ils ne représentent pas des tokens uniques. Coût natif cumulé déclaré : 1.609838002 ; devise/facturation effective N/A, non attestées par le champ collecté. Aucun calcul en euros ni conversion du quota n'est effectué.

Sondes : 12 observations, 10 valides et 2 invalidées conservées mais exclues des moyennes. Les écarts de planning et la pause sont conservés ; aucune relève manquée n'est recréée.

| Position | UTC | Validité | Tokens sortie | TTMT s | Débit tokens/s |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-21T04:53:49.110748+00:00 | valide | 728 | 2.493744 | 245.585 |
| relève +30 min | 2026-10-21T05:24:08.446903+00:00 | valide | 712 | 2.509370 | 184.430 |
| relève +60 min | 2026-10-21T05:54:36.855456+00:00 | valide | 713 | 2.011627 | 840.363 |
| reprise +30min | 2026-10-21T21:36:35.775633+00:00 | invalide | 712 | N/A | N/A |
| reprise +60min | 2026-10-21T22:11:15.648178+00:00 | invalide | 726 | N/A | N/A |
| reprise +60min | 2026-10-21T22:13:24.261400+00:00 | valide | 712 | 2.221384 | 217.395 |
| reprise +90min | 2026-10-21T22:52:37.475947+00:00 | valide | 727 | 4.209989 | 320.342 |
| reprise +120min | 2026-10-21T23:27:00.044922+00:00 | valide | 712 | 1.361225 | 668.861 |
| reprise +150min | 2026-10-21T23:57:36.639998+00:00 | valide | 712 | 2.484253 | 257.466 |
| reprise +180min | 2026-10-22T00:29:11.401454+00:00 | valide | 712 | 2.557135 | 240.121 |
| reprise +210min | 2026-10-22T01:10:13.560076+00:00 | valide | 731 | 2.074715 | 880.396 |
| finale après archivage C06 | 2026-10-22T01:40:13.508930+00:00 | valide | 713 | 1.425116 | 791.750 |
Moyennes arithmétiques par méthode :

| Méthode comparable | n | TTMT moyen s | Débit moyen tokens/s |
| --- | --- | --- | --- |
| Début avant pause, méthode originale conservée | 3 | 2.338247 | 423.459 |
| Reprise/finale, attribution assistant/message exact vérifiée | 7 | 2.333403 | 482.333 |
Deux mesures reprise +30 et première +60 sont invalides : événements texte non filtrés par rôle/message assistant. Les métriques temporelles sont N/A, leurs métadonnées restent conservées. Les erreurs de fermeture SSE des premières sondes sont tracées. Le débit utilise les tokens de sortie sur la fenêtre de deltas texte ; il n'est pas interchangeable avec le benchmark PLLM incluant raisonnement.

Compactions coordonnées :

| Cycle | Début UTC | OpenCode | Codex natif | Conjoint |
| --- | --- | --- | --- | --- |
| cismp5-compaction-28e254e594fe449a8795b752301c425b | 2026-10-21T06:20:57.717677+00:00 | N/A | N/A | False |
| cismp5-compaction-a8e38eca2a3a48e0b51f8e6fb9be2690 | 2026-10-21T22:36:46.171774+00:00 | COMPLETED | NOT_EXECUTED | False |
| cismp5-compaction-49d76f2646a54faf9451523f5f2ebaf7 | 2026-10-22T00:08:36.661767+00:00 | COMPLETED | NOT_EXECUTED | False |
| cismp5-compaction-5ccdb222d496425e9941b67087138cf9 | 2026-10-22T01:42:38.139742+00:00 | COMPLETED | NOT_EXECUTED | False |
L'API thread/compact/start du chat orchestrateur n'est pas exposée. Aucun lancement n'est présenté comme une fin sans message summary natif. Le dernier cycle technique de préparation du rapport intervient après le bornage de la période de codage ; il ne modifie aucune source ni quota historique.

## 2. Types de messages et d'outils

| Rôle | Effectif | Part |
| --- | --- | --- |
| assistant | 754 | 60.08 % |
| user | 501 | 39.92 % |

| Type de partie | Effectif | Part |
| --- | --- | --- |
| compaction | 3 | 0.08 % |
| reasoning | 747 | 19.21 % |
| step-finish | 752 | 19.34 % |
| step-start | 754 | 19.39 % |
| text | 1006 | 25.87 % |
| tool | 627 | 16.12 % |

| Terminaison assistant | Effectif | Part |
| --- | --- | --- |
| en_cours | 2 | 0.27 % |
| stop | 202 | 26.79 % |
| tool-calls | 550 | 72.94 % |

| Outil | Terminés | Erreurs techniques | En cours | Total | Part globale |
| --- | --- | --- | --- | --- | --- |
| bash | 52 | 0 | 0 | 52 | 8.29 % |
| cgpt-validation_broker_health | 23 | 0 | 0 | 23 | 3.67 % |
| cgpt-validation_broker_readiness | 34 | 0 | 0 | 34 | 5.42 % |
| cgpt-validation_cancel_approval | 2 | 1 | 0 | 3 | 0.48 % |
| cgpt-validation_get_approval | 16 | 0 | 0 | 16 | 2.55 % |
| cgpt-validation_list_pending | 23 | 0 | 0 | 23 | 3.67 % |
| cgpt-validation_poll_approval | 10 | 8 | 0 | 18 | 2.87 % |
| cgpt-validation_request_validation | 120 | 17 | 0 | 137 | 21.85 % |
| edit | 17 | 0 | 0 | 17 | 2.71 % |
| glob | 13 | 0 | 0 | 13 | 2.07 % |
| grep | 30 | 0 | 0 | 30 | 4.78 % |
| read | 200 | 1 | 0 | 201 | 32.06 % |
| write | 60 | 0 | 0 | 60 | 9.57 % |
| Type d’action pilotée | Demandes | Approved | Taux app. | Rejected | Taux refus | Annulées |
| --- | --- | --- | --- | --- | --- | --- |
| fichiers | 78 | 77 | 98.72 % | 0 | 0.00 % | 1 |
| commandes | 56 | 51 | 91.07 % | 4 | 7.14 % | 1 |

Les outils MCP request/get/poll ne sont pas des effets métier. Un timeout de consultation ne vaut pas rejet ; les premières soumissions invalides sont conservées comme erreurs techniques. Les décisions sont comptées par demande suivie, pas par répétition de poll.

## 3. Fichiers modifiés

Il s'agit de tentatives de fichier, pas du nombre de fichiers distincts ou de lignes de code. Une écriture approuvée dont le SHA diffère est connue et corrigée sous mandat neuf ; sa permission n'est pas rejouée. L'archive déplace le dossier C06 et le rebasage de liens ne modifie pas le sens. La dernière édition du présent rapport n'est pas incluse dans le bornage.

| Chemin absolu complet | Approuvées | Taux app. | Refusées | Taux refus | Annulées | Erreurs natives | Taux err. | Total demandes | Part |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-protected-core-http-commands-and-queries/design.md | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/openspec/changes/add-protected-core-http-commands-and-queries/requirements.md | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/openspec/changes/add-protected-core-http-commands-and-queries/tasks.md | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-22-add-protected-core-http-commands-and-queries/design.md | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-22-add-protected-core-http-commands-and-queries/requirements.md | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/auth/api_request_source.py | 3 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 3 | 3.85 % |
| /home/devops/datas/pixs/src/pixs/auth/identifiers.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/auth/invocation.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/auth/runtime_verifier.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/auth/services.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_activity.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_catalog.py | 1 | 50.00 % | 0 | 0.00 % | 1 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_composition.py | 3 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 3 | 3.85 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_errors_catalog.py | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_openapi.py | 3 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 3 | 3.85 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_openapi_compare.py | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_pagination.py | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/src/pixs/backend/api_core_views.py | 4 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 4 | 5.13 % |
| /home/devops/datas/pixs/src/pixs/backend/openapi_document_view.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/api_core_idempotency_record.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/api_core_idempotency_repository.py | 3 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 3 | 3.85 % |
| /home/devops/datas/pixs/src/pixs/core/api_core_idempotency_values.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/api_core_serializer_v1.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/dto.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/migrations/0003_core_idempotence.py | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/src/pixs/core/models.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/query_source.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/services_queries.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/src/pixs/core/services_runtime_declarations.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/tests/integration/test_api_core_auth_postgres.py | 6 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 6 | 7.69 % |
| /home/devops/datas/pixs/tests/integration/test_api_core_idempotence_postgres.py | 5 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 5 | 6.41 % |
| /home/devops/datas/pixs/tests/integration/test_api_core_platform_postgres.py | 7 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 7 | 8.97 % |
| /home/devops/datas/pixs/tests/integration/test_api_core_tenant_postgres.py | 4 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 4 | 5.13 % |
| /home/devops/datas/pixs/tests/unit/test_api_core_errors.py | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/tests/unit/test_api_core_idempotency_values.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |
| /home/devops/datas/pixs/tests/unit/test_api_core_openapi.py | 3 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 3 | 3.85 % |
| /home/devops/datas/pixs/tests/unit/test_api_core_pagination.py | 2 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 2 | 2.56 % |
| /home/devops/datas/pixs/tests/unit/test_api_core_serializer.py | 1 | 100.00 % | 0 | 0.00 % | 0 | 0 | 0.00 % | 1 | 1.28 % |

37 fichiers de réalisation ont été examinés avant archive (33 Python, quatre documents modifiés). Les appels natifs write/edit sont 77 (60 write, 17 edit) ; ce total ne compte pas les déplacements effectués par la commande d'archive.

## 4. Commandes

Résultats d’exécution natifs, distincts des décisions CAB :

| Résultat Bash | Nombre | Part des 52 appels |
| --- | --- | --- |
| Terminés avec exit zéro | 44 | 84.62 % |
| Échecs d’exécution/tests intermédiaires | 8 | 15.38 % |
| Erreurs techniques Bash | 0 | 0.00 % |
Les huit échecs sont conservés ; les suites finales sont toutes passées. Un outil terminé ne signifie donc pas que son test intermédiaire a réussi.

| Famille | Approuvées | Refusées | Annulées | Total | Part |
| --- | --- | --- | --- | --- | --- |
| Compilation | 10 | 0 | 0 | 10 | 17.86 % |
| OpenSpec | 5 | 0 | 0 | 5 | 8.93 % |
| PostgreSQL | 21 | 3 | 0 | 24 | 42.86 % |
| Prévol / autres | 4 | 0 | 0 | 4 | 7.14 % |
| Unitaires | 11 | 1 | 1 | 13 | 23.21 % |
Les libellés suivants sont bornés à 100 caractères ; les commandes exactes et appels natifs restent dans le checkpoint. Les échecs d'exécution de recettes intermédiaires n'ont pas été relancés sous une once consommée.

| Commande, libellé ≤100 caractères | Occurrences demandes | Part | Refusées |
| --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive --help | 1 | 1.79 % | 0 |
| /home/devops/.local/npm/bin/openspec archive add-protected-core-http-commands-and-queries --yes --s… | 1 | 1.79 % | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 3.57 % | 0 |
| /home/devops/.local/npm/bin/openspec validate add-protected-core-http-commands-and-queries --strict | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -c 'from django.conf impor… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s te… | 2 | 3.57 % | 0 |
| /usr/bin/env PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s te… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/output/cismp/cismp5-pixs-1f… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 4 | 7.14 % | 2 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 4 | 7.14 % | 1 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m test_… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m test_… | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m test_… | 4 | 7.14 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m test_… | 5 | 8.93 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 2 | 3.57 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 2 | 3.57 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 1 | 1.79 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 3 | 5.36 % | 1 |
| /usr/bin/true | 3 | 5.36 % | 0 |

Commandes refusées regroupées :

| Libellé ≤100 caractères | Occurrences refusées | Part des demandes commandes |
| --- | --- | --- |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 2 | 3.57 % |
| /usr/bin/env PYTHONPATH=src:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -c 'impo… | 1 | 1.79 % |
| /usr/bin/env PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v … | 1 | 1.79 % |
Les quatre refus portent sur des divergences de recopie/manifeste avant effet, pas sur un accord implicite. Les annulations sont séparées. L'absence de Git est vérifiée dans les commandes pilotées.

## 5. Accès web

OpenCode : zéro appel webfetch/websearch collecté ; approbations 0, refus 0, erreurs 0, pourcentages N/A (dénominateur nul).

Orchestrateur : documentation primaire consultée pour Django Signer, hors outils web OpenCode. Sources effectivement consultées :

| Statut | URL affichée ≤100 caractères |
| --- | --- |
| consultée | https://docs.djangoproject.com/en/6.1/topics/signing/ |
| consultée, préalable | https://docs.djangoproject.com/en/6.0/topics/signing/ |
Les nombres complets de requêtes et décisions web de l'orchestrateur sont N/A : aucune source native de collecte exhaustive de son historique n'est exposée. Aucune URL refusée n'est inventée ; les deux liens listés ne constituent pas un total de requêtes. Aucun accès web applicatif n'est nécessaire aux recettes.

## 6. Synthèse globale

| Borne de la session C06 | Horodatage / durée |
| --- | --- |
| Début effectif du job C06 | 2026-10-21T04:49:26+00:00 |
| Fin après archive et sonde finale, avant rédaction | 2026-10-22T01:41:07.045000+00:00 |
| Durée globale calendaire, pauses et attentes incluses | 20 h 51 min 41 s |

| Quota codex, fenêtre10080 min | Lecture native | Utilisé | Réinitialisation Unix |
| --- | --- | --- | --- |
| Avant C06 | 2026-10-21T04:49:26Z | 84 % | 1793082828 |
| Après archive et sonde finale | 2026-10-22T01:41:07.045Z | 100 % | 1793082828 |
| Variation pendant la session | même compte et même fenêtre | 16 points | Aucune réinitialisation |
Les quotas sont partagés : la variation de 16 points n'est pas attribuée exclusivement à C06. Le relevé de démarrage du RUN antérieur à C06 (41 %) est conservé séparément ; il ne remplace pas le relevé avant C06 (84 %). Aucun reset ni achat n'est exécuté. Le relevé final ne couvre pas la rédaction ultérieure du rapport.

| Demandes pilotées | Total | Part | Approved | Taux approved | Rejected | Taux rejected | Annulées |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fichiers | 78 | 58.21 % | 77 | 98.72 % | 0 | 0.00 % | 1 |
| commandes | 56 | 41.79 % | 51 | 91.07 % | 4 | 7.14 % | 1 |
| autres | 0 | 0.00 % | 0 | N/A | 0 | N/A | 0 |
| Global | 134 | 100 % | 128 | 95.52 % | 4 | 2.99 % | 2 |

Agrégat des appels natifs, distinct des demandes CAB :

| Domaine natif | Appels | Part globale |
| --- | --- | --- |
| Fichiers | 77 | 12.28 % |
| Commandes | 52 | 8.29 % |
| Web | 0 | 0.00 % |
| Autres outils | 498 | 79.43 % |
| Global | 627 | 100 % |
| Domaine natif | Appels | Erreurs techniques | Taux erreurs |
| --- | --- | --- | --- |
| Fichiers | 77 | 0 | 0.00 % |
| Commandes | 52 | 0 | 0.00 % |
| Web | 0 | 0 | N/A — zéro appel |
| Autres outils | 498 | 27 | 5.42 % |
| Global | 627 | 27 | 4.31 % |

Le domaine autres contient notamment les demandes/consultations CAB ; ne pas additionner ses appels aux demandes pilotées comme s'il s'agissait d'effets métier supplémentaires. Taux d'erreur technique natif global : 4.31 %. Répartition native terminale par outil en section2 ; les totaux ne sont pas des mesures de codage productif.

Livraison vérifiée : 192/192 cas PG finaux, 166/166 unitaires, 33/33 py_compile ; strict OpenSpec avant et après archive, zéro lien local cassé et UTF-8/LF. Archive unique prouvée par call_01a1613f4710754a924c30ac3a848a13, sans mise à jour du canon. Publication CAB prouvée par c06-publish-8738a487f82e4576b2ad3cfbe99b69f8, référence 55.

Ce rapport est produit après publication sous la seule ressource STATISTIQUES.md. Son intégrité et le gate/désarmement/libération sont contrôlés ensuite ; ils ne sont pas déclarés déjà accomplis à l'instant de rédaction. Git et déploiement non exécutés ; aucun frontend ni P0 complet revendiqué. Données Auth brutes non projetées par les bilans masqués ; les données PG sont traitées uniquement dans les processus locaux protégés. OpenCode, broker, contrôleur, superviseur et moniteur partagés restent ouverts.

Sources : historiques natifs des deux sessions maîtresses filtrés à partir du début C06 ; checkpoint, décisions explicites, reçus, empreintes et sondes du RUN. Les agrégats CAB globaux mêlant d'autres contextes ne servent pas à attribuer leurs durées à C06. Les observations manquantes restent N/A ; aucune activité absente n'est reconstruite.
