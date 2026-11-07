# STATISTICS.md — RUN cismp5-pixs-efa486919d4b4b90 — complete-shared-ui-i18n-and-accessibility

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A, runtime OpenCode 2.2.5 observé séparément | opencode-go | medium | N/A — sondes périodiques non activées | N/A — sondes périodiques non activées | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| GPT-6 | N/A | OpenAI | N/A | N/A | N/A | N/A |

## 1 Généralités, décisions et périmètre

RUN : `cismp5-pixs-efa486919d4b4b90`. Change : `complete-shared-ui-i18n-and-accessibility`. Sessions natives du RUN : `ses_e692f9b46ffe5xDkKBmIix0ejr` (agent plan), `ses_e6921ddbaffe5QGCFPuX8X9Cfx` (build), `ses_e5cd7ea40ffeYvliTqpTEmC2I3` (build, session courante) ; provider/model/variant de la session courante observés comme opencode-go/muse-spark-1.3-contributor/medium. Archive réellement effectuée : `2026-11-05-complete-shared-ui-i18n-and-accessibility` ; opération CAB `c12-archive-final-op-20261105-71`, COMPLETED exit 0.
Décisions du contrôleur CAB pour ce contexte, distinctes des appels natifs et des effets : 120 décisions distinctes, 116 approved (96,7%), 4 rejected (3,3%), 0 needs_clarification, 0 pending ; 101 once. Ces décisions ne se répartissent pas de façon sûre par fichier/commande : N/A pour les ventilations par cible. Expirations/annulations non agrégées séparément : N/A, pas zéro.
Les états natifs `completed` signifient que l’appel natif s’est terminé, pas que l’opération métier ou le test a réussi. Approbations CAB, appels natifs et effets métier restent séparés dans ce rapport.

## 2 Messages, parties, terminaisons, outils et état technique

Historique natif complet des 3 sessions, agrégé localement sans contenu. Les messages `user` peuvent venir de l’orchestrateur.
Messages : 2986 au total, user 764 (25,6%), assistant 1496 (50,1%), idle 702 (23,5%), system 19 (0,6%), synthetic 2 (0,1%), compaction 3 (0,1%).
Parties : 4728 au total, text 1970 (41,7%), reasoning 1803 (38,1%), tool 955 (20,2%).
Terminaisons : 2986 au total, N/A 1490 (49,9%), tool-calls 750 (25,1%), stop 720 (24,1%), error 26 (0,9%).
Appels d’outils : 955 au total, terminés 904 (94,7%), erreur 51 (5,3%), en cours 0. Outils sans appel web observé.

| Outil | Total | Part du total | Terminé natif | Terminé (%) | Erreur native | Erreur (%) | En cours |
|---|---:|---:|---:|---:|---:|---:|---:|
| execute | 87 | 9,1% | 85 | 97,7% | 2 | 2,3% | 0 |
| read | 252 | 26,4% | 251 | 99,6% | 1 | 0,4% | 0 |
| glob | 19 | 2,0% | 19 | 100% | 0 | 0% | 0 |
| cgpt-validation_request_validation | 227 | 23,8% | 206 | 90,7% | 21 | 9,3% | 0 |
| cgpt-validation_broker_readiness | 40 | 4,2% | 40 | 100% | 0 | 0% | 0 |
| cab_codemode_discovery | 19 | 2,0% | 19 | 100% | 0 | 0% | 0 |
| bash | 120 | 12,6% | 112 | 93,3% | 8 | 6,7% | 0 |
| grep | 43 | 4,5% | 43 | 100% | 0 | 0% | 0 |
| cgpt-validation_poll_approval | 52 | 5,4% | 51 | 98,1% | 1 | 1,9% | 0 |
| cgpt-validation_get_approval | 19 | 2,0% | 18 | 94,7% | 1 | 5,3% | 0 |
| edit | 68 | 7,1% | 53 | 77,9% | 15 | 22,1% | 0 |
| write | 5 | 0,5% | 3 | 60% | 2 | 40% | 0 |
| cgpt-validation_lookup_validation | 4 | 0,4% | 4 | 100% | 0 | 0% | 0 |

## 3 Fichiers par chemin absolu, tentatives et statuts natifs

Appels edit/write : 73 au total ; statut natif completed 56 / error 17 ; 56+17=73. Chaque pourcentage est sur 73. La décision d’approbation CAB par fichier n’est pas disponible. Pas de déplacement d’archive supplémentaire ; chemins reflétant les appels natifs d’avant l’archivage.

| Chemin absolu | Appels | Part de 73 | Completed natif | Error natif |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | 13 | 17,8% | 11 | 2 |
| /home/devops/datas/pixs/frontend/package.json | 2 | 2,7% | 1 | 1 |
| /home/devops/datas/pixs/frontend/scripts/pixs-composition-plugin-v1.mjs | 1 | 1,4% | 1 | 0 |
| /home/devops/datas/pixs/frontend/scripts/validate_pixs_css_tokens.mjs | 3 | 4,1% | 2 | 1 |
| /home/devops/datas/pixs/frontend/src/theme.css | 3 | 4,1% | 1 | 2 |
| /home/devops/datas/pixs/frontend/tests/browser-check.mjs | 8 | 11,0% | 8 | 0 |
| /home/devops/datas/pixs/frontend/tests/css-tokens.test.mjs | 1 | 1,4% | 1 | 0 |
| /home/devops/datas/pixs/openspec/changes/complete-shared-ui-i18n-and-accessibility/BLOCKERS.md | 4 | 5,5% | 3 | 1 |
| /home/devops/datas/pixs/openspec/changes/complete-shared-ui-i18n-and-accessibility/design.md | 2 | 2,7% | 1 | 1 |
| /home/devops/datas/pixs/openspec/changes/complete-shared-ui-i18n-and-accessibility/STATISTICS.md | 1 | 1,4% | 0 | 1 |
| /home/devops/datas/pixs/openspec/changes/complete-shared-ui-i18n-and-accessibility/tasks.md | 19 | 26,0% | 13 | 6 |
| /home/devops/datas/pixs/src/pixs/backend/api/__init__.py | 2 | 2,7% | 1 | 1 |
| /home/devops/datas/pixs/src/pixs/backend/api/errors.py | 2 | 2,7% | 1 | 1 |
| /home/devops/datas/pixs/src/pixs/backend/api/README.md | 5 | 6,8% | 5 | 0 |
| /home/devops/datas/pixs/src/pixs/backend/api/responses.py | 1 | 1,4% | 1 | 0 |
| /home/devops/datas/pixs/tests/integration/test_api_error_projection_integration.py | 3 | 4,1% | 3 | 0 |
| /home/devops/datas/pixs/tests/integration/test_api_error_response_integration.py | 1 | 1,4% | 1 | 0 |
| /home/devops/datas/pixs/tests/unit/test_api_error_projection.py | 2 | 2,7% | 2 | 0 |

## 4 Commandes, comptages sûrs et limites d’attribution

Commandes bash direct : 120 au total, completed 112, error 8. Execute wrapper : 87 au total, completed 85, error 2. Aucune chaîne de commande révélée. Statut refusé par commande/famille non attribuable à partir des agrégats présents : N/A ; ne requalifie pas les erreurs natives en refus CAB. Les 101 once CAB et les 120 décisions restent comptés en section 1, sans double comptage avec les 955 appels d’outils.

## 5 Accès web et URLs

Aucun appel à un outil web observé dans l’historique natif agrégé ; 0 URL visitée ; aucune URL créée ou devinée dans ce rapport.

## 6 Synthèse globale, durée, quota, archive et tests

Regroupement sans double comptage : 2986 messages, 4728 parties, 955 appels d’outils dont 904 terminés et 51 en erreur, 120 décisions CAB distinctes dont 116 approved et 4 rejected, 101 once, 73 tentatives edit/write dont 56 completed et 17 error, commandes bash 120 et execute 87 selon section 4, web 0.

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-11-01T11:13:22.106Z |
| Fin — après archivage | 2026-11-05T03:09:38.192Z |
| Durée globale (pauses et attentes incluses) | 87 h 56 min 16,086 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A — relevé initial absent | N/A — relevé initial absent | N/A — relevé initial absent |
| Après — après archivage de la spécification | 2026-11-05T03:09:37.570Z | 91% | 2026-11-07T10:36:34Z |
| Différence après − avant | N/A — relevé initial absent | N/A — relevé initial absent | N/A — relevé initial absent |

Quota partagé par le compte ; différence non attribuable exclusivement au RUN. Archive : `2026-11-05-complete-shared-ui-i18n-and-accessibility`, opération `c12-archive-final-op-20261105-71` COMPLETED exit 0. Tests établis dans les preuves d’archive : compilation Python 8 fichiers exit 0 ; unitaires API erreurs 18/18 ; intégration API erreurs 7/7 ; core erreurs 7/7 ; Node 162/162 ; catalog Chromium 145 et Firefox 145 passés ; build exit 0, 111 modules, avertissements MODULE_LEVEL_DIRECTIVE non bloquants ; browser-check critique exit0 avec clavier/focus, AX, reflow320 320/320, zoomCSS2x proxy sans zoom natif, contrastes clair/sombre, reduced motion, 0 erreur console/HTTP, cleanup vérifié ; preuve .32 Chromium 156, Orca48.1, AT-SPI2, Ctrl+Plus x5, DPR2, reflow sans overflow, AX45, tab vers Skip to content, limites sans certification WCAG totale ni annonce Orca stable ; validation OpenSpec strict .68 exit0, change valid, zéro delta. Tests ne signifient ni certification ni livraison. Git non autorisé/non exécuté ; aucun commit, push, déploiement ou publication.