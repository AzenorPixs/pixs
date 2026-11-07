# STATISTIQUES — add-initial-event-registration-declaration-v1

RUN cismp-pixs-01a13baffc02 ; contexte CAB 139 ; référence publiée figée 19. Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-event-registration-declaration-v1. Rapport du même change, incluant ses deux sessions maîtresses ; aucune répartition des travaux des autres RUN.

Bornes figées avant rédaction : création native 2026-10-15T07:01:47.985000+00:00 ; fin après archive et sonde finale, au relevé quota 2026-10-15 16:44:32 UTC. La collecte native complète ci-dessous couvre ces bornes. L’export CAB est partiel et cumulatif (2026-10-15T08:05:20.872000+00:00 → 2026-10-15T16:46:46.788000+00:00), capturé à 2026-10-15T16:46:46.789790+00:00 : ses compteurs et latences sont présentés séparément, jamais additionnés aux comptes natifs. La rédaction/écriture de ce rapport est hors intervalle.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | OpenCode Go | high | 2.856 s | 111.918 | N/A |
| muse-spark-1.3-contributor — compaction | OpenCode 1.19.0 ; modèle N/A | OpenCode Go | N/A — variant non exposé | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — identifiant exact non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Les versions de modèle ne sont pas déduites de « 1.3 ». Les moyennes du codage sont celles des sept sondes valides, pas du benchmark PLLM. Temps de service et dénominateur cumulé : N/A, faute de durées isolées de génération ; les attentes, outils, pauses et états busy ne sont pas du temps de service. Les métriques orchestrateur ne sont pas sondées. Les chevauchements entre agents ne sont pas ventilés.

## 1. Statistiques générales et décisions

Résultat fonctionnel : 28 tests Pixs réussis (12 unitaires neufs, 1 intégration gardée, 15 régressions), 0 échec, 0 ignoré ; trois compilations natives séparées exit 0 ; neuf tâches prouvées/cochées. Stricts ciblés change et events avant code, après tests et après cochage : 1/1, issues vides, exit 0. Global standard avant archive : 81/81, exit 0. Strict global avant : 79/81, exit 1 ; après : 78/80, exit 1. Ces deux sorties strictes ne sont pas des réussites strictes : exactement quatre WARNING historiques de longueur, zéro ERROR, identiques à la baseline.

| Bilan natif complet | Nombre | Part |
| --- | --- | --- |
| Messages | 477 | 100.0 % |
| Appels d’outils | 232 | 100.0 % |

Décisions de l’export CAB partiel — dénominateur 34 décisions, distinct des appels d’outils :

| Décision CAB | Nombre | Part |
| --- | --- | --- |
| approved | 32 | 94.1 % |
| rejected | 2 | 5.9 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 34 | 100.0 % |

Permissions once observées par CAB : 31, soit 96.9 % des décisions approved. Une approbation n’est pas une preuve d’exécution : l’ancien accord de cochage sans outil Write a été invalidé par prepare. Aucune permission ancienne n’a été rejouée. Les deux refus CAB locaux techniques ont précédé toute compilation ; la compilation unitaire correcte est ensuite passée une seule fois sous un mandat neuf.

| Tokens natifs déclarés OpenCode | Nombre | Part du total |
| --- | --- | --- |
| input | 7083862 | 27.4 % |
| output | 84172 | 0.3 % |
| reasoning | 30034 | 0.1 % |
| cache_read | 18611775 | 72.1 % |
| cache_write | 0 | 0.0 % |
| Total déclaré | 25809843 | 100.0 % |

Coût numérique cumulé exposé par OpenCode : 0.76845095 ; unité monétaire non fournie par cette télémétrie, facture fournisseur N/A. Aucune conversion du quota en tokens ou en argent. Compactions natives observées : 5 ; compaction propriétaire Codex : N/A, API non exposée. Les appels terminés avec erreur technique restent visibles dans les tableaux ; le succès technique d’un Bash ne signifie pas exit CLI 0.

Activité apparente CAB, couverture partielle ; dénominateur 31259268 ms, sans assimilation au travail productif :

| État observé | Millisecondes | Part |
| --- | --- | --- |
| busyMs | 4638388 | 14.8 % |
| idleMs | 26260736 | 84.0 % |
| nativeUnknownMs | 360144 | 1.2 % |
| Total réservé | 31259268 | 100.0 % |

Latence requestToDecision : n=34 (100 % de son échantillon), moyenne 50.825 s, médiane 25.179 s, p95 214.684 s ; dernières 2048 observations au maximum. Les trois populations se recouvrent et ne s’additionnent pas.

Latence decisionToOnce : n=31 (100 % de son échantillon), moyenne 7.363 s, médiane 4.702 s, p95 23.670 s ; dernières 2048 observations au maximum. Les trois populations se recouvrent et ne s’additionnent pas.

Latence nativeTool : n=165 (100 % de son échantillon), moyenne 15.977 s, médiane 0.337 s, p95 60.008 s ; dernières 2048 observations au maximum. Les trois populations se recouvrent et ne s’additionnent pas.

| Tentatives HTTP en échec, pas refus de permission | Nombre | Part |
| --- | --- | --- |
| native-validation-not-correlated | 8 | 47.1 % |
| run-mandate-already-active | 7 | 41.2 % |
| decision-run-divergent | 1 | 5.9 % |
| run-not-quiescent | 1 | 5.9 % |
| Total | 17 | 100.0 % |

Incidents conservés : délai/unknown approval avant compilation, demande prématurée rejetée sans effet, accord Write non consommé puis invalidé, prévol non admis annulé, diagnostics pré-prepare entraînant complete refusé, reprise humaine auditée après correctif CAB, et annonce de publication prématurée corrigée. Le 409 de release provenait d’un hold technique C2 ; aucune publication n’avait alors eu lieu. Après fermeture des holds et nouvelle vérification, l’API a réellement publié la référence 19 puis closing REPORT. Aucun de ces incidents n’est présenté comme un test fonctionnel réussi.

PLLM imposée mode 1, Muse/high : évaluation fraîche 2026-10-15T17:58:05+02:00, Valide ; TTFT 23.7583 s, débit global raisonnement+réponse 1629.485 tokens/s, palier 4096. Ce benchmark est distinct du débit textuel des sondes et n’est pas mélangé à leurs moyennes.

### Sondes de télémétrie hors production

| Relèves | Nombre | Part |
| --- | --- | --- |
| Réussies valides | 7 | 35.0 % |
| Échouées | 0 | 0.0 % |
| Manquées | 13 | 65.0 % |
| Total prévu, finale comprise | 20 | 100.0 % |

| Position / session jetable | Horodatage UTC | Tokens sortie | TTMT s | Tokens/s | Statut |
| --- | --- | --- | --- | --- | --- |
| début / ses_ec19bfbcbffeqkHxfy9NqT1rnW | 2026-10-15T07:08:24.504521+00:00 | 1139 | 3.399016 | 114.730363 | Valide : 100 lignes, zéro outil, high/stop |
| +30 min / ses_ec1801474ffeF8aYT0B2bCGxrD | 2026-10-15T07:38:53.200042+00:00 | 1149 | 2.633392 | 89.077202 | Valide : 100 lignes, zéro outil, high/stop |
| +150 min — relève différée après fenêtres / ses_ec1076ab1ffeDGl8EuZksgBRKe | 2026-10-15T09:50:40.979126+00:00 | 1152 | 3.197647 | 83.883904 | Valide : 100 lignes, zéro outil, high/stop |
| +180 min — implémentation / ses_ec0f166fbffe13aitKZzijiB70 | 2026-10-15T10:14:43.721092+00:00 | 1159 | 2.465593 | 106.986592 | Valide : 100 lignes, zéro outil, high/stop |
| +360 min — reprise après fenêtres / ses_ec04401efffeLFDrAMaGrq4HPR | 2026-10-15T13:24:07.318961+00:00 | 1119 | 2.529929 | 154.799374 | Valide : 100 lignes, zéro outil, high/stop |
| +540 min — relève courante retardée / ses_ebfaa50b9ffekUdMIePcInVbLY | 2026-10-15T16:11:59.692107+00:00 | 1144 | 2.768821 | 62.415452 | Valide : 100 lignes, zéro outil, high/stop |
| fin / ses_ebf930f3dffemkDcj51GC77MyA | 2026-10-15T16:37:23.782662+00:00 | 1126 | 2.998014 | 171.532525 | Valide : 100 lignes, zéro outil, high/stop |

Sondes : prompt déterministe constant de 185 caractères (« lignes 001 à 100 : alpha beta gamma delta epsilon zeta eta theta »), mêmes modèle/fournisseur/high. Moyennes arithmétiques : TTMT 2.856059s ; débit 111.917916tokens/s ; min/max TTMT 2.465593/3.399016s ; débit 62.415452/171.532525. Surcharge séparée : 7988tokens de sortie et 100.278s écoulées, coût facturé N/A. Les tokens ne sont pas ajoutés à la production. La finale a été faite après archive et avant la levée effective d’exclusion, sans outil ni effet fichier ; elle n’a pas été rejouée.

| Échéance manquée | Mesures | Cause |
| --- | --- | --- |
| 2026-10-15T08:08:21.935124+00:00 | N/A | Pause maintenance/reprise technique ; aucune sonde rétroactive |
| 2026-10-15T08:38:21.935124+00:00 | N/A | Pause maintenance/reprise technique ; aucune sonde rétroactive |
| 2026-10-15T09:08:21.935124+00:00 | N/A | FIFO et exclusions C2/C1 ; aucune mesure rétroactive |
| 2026-10-15T10:38:21.935124+00:00 | N/A | Relève non collectée pendant pilotage/récupération opérationnelle ; mesure absente |
| 2026-10-15T11:08:21.935124+00:00 | N/A | Relève non collectée pendant pilotage/récupération opérationnelle ; mesure absente |
| 2026-10-15T11:38:21.935124+00:00 | N/A | HUMAN_REQUIREDglobal/attentedécisionhumaine |
| 2026-10-15T12:08:21.935124+00:00 | N/A | GelHUMAN_REQUIRED/maintenancecoordonnée/attenteRSMP C2 ; aucunerelèverétroactive |
| 2026-10-15T12:38:21.935124+00:00 | N/A | GelHUMAN_REQUIRED/maintenancecoordonnée/attenteRSMP C2 ; aucunerelèverétroactive |
| 2026-10-15T13:38:21.935124+00:00 | N/A | RécupérationopérationnellepuisattenteaccordhumainCAB, aucunsondagependantgel ni relèverétroactive |
| 2026-10-15T14:08:21.935124+00:00 | N/A | Attente accord humain ciblé CAB ; sondesLLM suspendues, aucunrelevé rétroactif |
| 2026-10-15T14:38:21.935124+00:00 | N/A | Attente décision explicite CAB horsracine, sondesLLM suspendues ; aucune reconstruction rétroactive |
| 2026-10-15T15:08:21.935124+00:00 | N/A | Attente validation CAB horsracine, sondesLLM suspendues, aucune reconstruction rétroactive |
| 2026-10-15T15:38:21.935124+00:00 | N/A | Gel humain puis maintenance/récupération CAB, pas de sonde rétroactive |

Prompt exact constant des sondes (185 caractères) : « Sonde de télémétrie. Sans outil ni commentaire, écris exactement les lignes de 001 à 100, chacune sous la forme NNN : alpha beta gamma delta epsilon zeta eta theta. Aucune autre sortie. »

## 2. Types de messages et d’outils

API native complète des deux sessions, chacun des232identifiants de tool part est unique. Les tool states et les décisions CAB ont des dénominateurs différents. Un request_validation terminé peut retourner REJECTED : le succès du transport et la décision sur l’opération sont deux faits distincts. Les appels Read/MCP terminés peuvent être autorisés automatiquement par les règles de session ; seuls les effets mutables ont leur mandat CAB unitaire/once. Aucun refus explicite de permission n’a été identifié dans ces tool states ; leur historique SSE complet hors couverture reste N/A.

| Rôle natif | Nombre | Part |
| --- | --- | --- |
| user | 166 | 34.8 % |
| assistant | 311 | 65.2 % |
| Total | 477 | 100.0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 470 | 28.6 % |
| step-start | 311 | 18.9 % |
| reasoning | 316 | 19.2 % |
| tool | 232 | 14.1 % |
| step-finish | 311 | 18.9 % |
| compaction | 5 | 0.3 % |
| Total | 1645 | 100.0 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 194 | 62.4 % |
| stop | 117 | 37.6 % |
| Total | 311 | 100.0 % |

| Outil | Total / part | Completed | Erreur tool | Taux erreur |
| --- | --- | --- | --- | --- |
| read | 52 / 22.4 % | 46 | 6 | 11.5 % |
| cgpt-validation_broker_readiness | 62 / 26.7 % | 62 | 0 | 0.0 % |
| cgpt-validation_request_validation | 36 / 15.5 % | 28 | 8 | 22.2 % |
| bash | 24 / 10.3 % | 24 | 0 | 0.0 % |
| cgpt-validation_broker_health | 13 / 5.6 % | 13 | 0 | 0.0 % |
| write | 8 / 3.4 % | 8 | 0 | 0.0 % |
| cgpt-validation_poll_approval | 16 / 6.9 % | 10 | 6 | 37.5 % |
| cgpt-validation_get_approval | 3 / 1.3 % | 2 | 1 | 33.3 % |
| todowrite | 4 / 1.7 % | 4 | 0 | 0.0 % |
| cgpt-validation_list_pending | 10 / 4.3 % | 9 | 1 | 10.0 % |
| question | 1 / 0.4 % | 1 | 0 | 0.0 % |
| cgpt-validation_broker_evaluate_remediation | 1 / 0.4 % | 1 | 0 | 0.0 % |
| cgpt-validation_broker_execute_controlled_remediation | 1 / 0.4 % | 1 | 0 | 0.0 % |
| cgpt-validation_cancel_approval | 1 / 0.4 % | 1 | 0 | 0.0 % |
| Total | 232 / 100.0 % | 210 | 22 | 9.5 % |

## 3. Fichiers modifiés

Tentatives natives Write : huit écritures approuvées/exécutées, sept chemins distincts, zéro refus/erreur Write. Les chemins sont ceux des appels ; les quatre documents sont désormais sous l’archive indiquée en tête. Le schéma .openspec.yaml a été créé par CLI, hors compteur Write. Les cinq fichiers OpenSpec ont été déplacés une seule fois, sans changement de SHA ; canon Events et huit bases restent identiques.

| Chemin absolu lors des écritures | Écritures / part | Approuvées / taux | Refus / taux | Erreur / taux |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-registration-declaration-v1/proposal.md | 1 / 12.5 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-registration-declaration-v1/design.md | 1 / 12.5 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-registration-declaration-v1/tasks.md | 2 / 25.0 % | 2 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-registration-declaration-v1/specs/events/spec.md | 1 / 12.5 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/event_registration.py | 1 / 12.5 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_event_registration.py | 1 / 12.5 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_event_registration_integration.py | 1 / 12.5 % | 1 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| Total | 8 / 100.0 % | 8 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |

| Fichier réellement archivé | SHA256 |
| --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-event-registration-declaration-v1/.openspec.yaml | c5936a7e8ac90455175dd905c9e8fb9d33cf82476be795f24133b51ef95c3d96 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-event-registration-declaration-v1/proposal.md | 2a90fcd1f725de7ccdc903028e014935512c5d4cc8257e1144be6676eaea5c78 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-event-registration-declaration-v1/design.md | 9dc7e8a37f4f451b554d8d04538d5462726cb99726365a855249caa2d7fd783d |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-event-registration-declaration-v1/tasks.md | 67efd93c616e3b163d7289e39ead49b1024478cf6aba1ac46844ed3f3bc8d8d9 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-15-add-initial-event-registration-declaration-v1/specs/events/spec.md | dfb10597bcd6ce6f21e02f8c239cdb3aed9a83a169d170f58fff7cc82993594f |

| Nouveau code ou test Pixs | SHA256 |
| --- | --- |
| /home/devops/datas/pixs/src/pixs/kernel/event_registration.py | d05bb737abc011cbe5b00dbf4a5385330d418e0f626d39f99bf55950f75eb8b9 |
| /home/devops/datas/pixs/tests/unit/test_event_registration.py | 9bf6c3e5f46503641e6366bf893d7bc58930247831586a8629b04934dee9e432 |
| /home/devops/datas/pixs/tests/integration/test_event_registration_integration.py | 84174e51c7c9a1675eb68af02ad0983c9cf5759e3c06ff77d4a406bc9915cfa3 |

Le présent rapport est une neuvième pièce documentaire, écrite sous mandat distinct hors des232 appels figés. Sa vérification UTF-8/LF, six sections et totaux par CGPT reste obligatoire avant gate et livraison ; aucun archivage supplémentaire n’est nécessaire.

### Maintenance CAB distincte explicitement autorisée

Cette maintenance hors Pixs a été réalisée par Codex pendant l’intervalle : six fichiers sources/documentaires/tests CAB et quatre copies runtime/cache,10 chemins distincts. Compteurs d’écritures/outils de l’orchestrateur : N/A faute d’export structuré ; ces chemins ne sont pas ajoutés aux huit Write OpenCode.81 tests CAB pertinents réussis, 0 ignoré, strict controller-transport 1/1, issues vides, exit 0 ; ils ne sont pas additionnés aux28 tests Pixs. Les deux scripts ont été sauvegardés puis propagés, seuls contrôleur/superviseur redémarrés. Le premier passage combiné avait rencontré deux collisions de sockets entre fixtures et une erreur temporelle de la nouvelle fixture historique ; exécution séquentielle et correction de cette fixture ont rétabli le succès. Deux avertissements introduits dans le brouillon CAB ont été supprimés par clauses atomiques ; strict ciblé final sans issue. Ces essais de maintenance ne sont pas ajoutés aux résultats Pixs. OpenCode/broker jamais arrêtés. Accord humain01a14030-91eb-7bf3-8280-9cec7c051c8b ; reprise même job auditée sans nouvelle permission ou prévol rejoué.

| Chemin CAB autorisé | Type | SHA256 final | Tentatives d’écriture |
| --- | --- | --- | --- |
| /home/devops/datas/cab/plugins/cab-approval-bridge/scripts/cgpt-approval-bridge-job-context.mjs | source/test/document | b896363ee58fdf04ba869d7d552d6c97e2d9cf3d6783954e0a738aa988b125d1 | N/A |
| /home/devops/datas/cab/tests/controller-session-recovery.test.mjs | source/test/document | 1074bb8bec747615859ac77c961957291cb9f12e6c9577f6d071fd6c431dab7c | N/A |
| /home/devops/datas/cab/openspec/specs/controller-transport/spec.md | source/test/document | 9b40c48ec93cabaa06c6942422d0f74846320a968065ea9e323a0ef8aba630de | N/A |
| /home/devops/datas/cab/TECHNICAL.md | source/test/document | c54a7217bdf2a0fc3347f6bc4c87495006de22aced6eb51a70f095fab551c600 | N/A |
| /home/devops/datas/cab/plugins/cab-approval-bridge/scripts/cgpt-approval-bridge-controller.mjs | source/test/document | 97e4c4276c843adc11003973744cbcaaa686ef493b5b1aa1fd6ba9d6d8e58d91 | N/A |
| /home/devops/datas/cab/tests/concurrent-controller.test.mjs | source/test/document | 95050698cc303616da98ed0a4a82bc6ac9a2df5364d23d07a2dbd3d23bd2a04d | N/A |
| /home/ade/.local/share/cab-approval-bridge/cgpt-approval-bridge-controller.mjs | copie runtime/cache | 97e4c4276c843adc11003973744cbcaaa686ef493b5b1aa1fd6ba9d6d8e58d91 | N/A |
| /home/ade/.local/share/cab-approval-bridge/cgpt-approval-bridge-job-context.mjs | copie runtime/cache | b896363ee58fdf04ba869d7d552d6c97e2d9cf3d6783954e0a738aa988b125d1 | N/A |
| /home/ade/.codex/plugins/cache/cab_codex_plugins/cab-approval-bridge/1.1.0+codex.20261015044105/scripts/cgpt-approval-bridge-controller.mjs | copie runtime/cache | 97e4c4276c843adc11003973744cbcaaa686ef493b5b1aa1fd6ba9d6d8e58d91 | N/A |
| /home/ade/.codex/plugins/cache/cab_codex_plugins/cab-approval-bridge/1.1.0+codex.20261015044105/scripts/cgpt-approval-bridge-job-context.mjs | copie runtime/cache | b896363ee58fdf04ba869d7d552d6c97e2d9cf3d6783954e0a738aa988b125d1 | N/A |

## 4. Commandes

| Famille | Appels | Part |
| --- | --- | --- |
| Prévol inoffensif | 5 | 20.8 % |
| Versions | 2 | 8.3 % |
| Création OpenSpec | 1 | 4.2 % |
| Validation OpenSpec | 9 | 37.5 % |
| Compilations Python | 3 | 12.5 % |
| Tests Python | 3 | 12.5 % |
| Archivage OpenSpec | 1 | 4.2 % |
| Total | 24 | 100.0 % |

| Commande,100 caractères maximum | Occurrences / part | Exit0 | Exit1 |
| --- | --- | --- | --- |
| /usr/bin/true | 5 / 20.8 % | 5 | 0 |
| /home/devops/.local/npm/bin/openspec --version | 1 / 4.2 % | 1 | 0 |
| /home/devops/.local/npm/bin/openspec new change add-initial-event-registration-declaration-v1 | 1 / 4.2 % | 1 | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-event-registration-declaration-v1 --stric… | 3 / 12.5 % | 3 | 0 |
| /home/devops/.local/npm/bin/openspec validate events --type spec --strict --json | 3 / 12.5 % | 3 | 0 |
| /home/devops/python/current/bin/python3 --version | 1 / 4.2 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -B -m py_compile src/pixs/kernel/event_registration.py | 1 / 4.2 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -B -m py_compile tests/unit/test_event_registration.py | 1 / 4.2 % | 1 | 0 |
| /usr/bin/env PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 /home/devops/python/c… | 1 / 4.2 % | 1 | 0 |
| /home/devops/python/current/bin/python3 -B -m py_compile tests/integration/test_event_registration_… | 1 / 4.2 % | 1 | 0 |
| /usr/bin/env PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 /home/devops/python/c… | 1 / 4.2 % | 1 | 0 |
| /usr/bin/env PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 /home/devops/python/c… | 1 / 4.2 % | 1 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 / 4.2 % | 1 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 / 8.3 % | 0 | 2 |
| /home/devops/.local/npm/bin/openspec archive add-initial-event-registration-declaration-v1 --yes --… | 1 / 4.2 % | 1 | 0 |
| Total | 24 / 100.0 % | 22 / 91.7 % | 2 / 8.3 % |

Les deux exit1 sont exclusivement les stricts globaux avec les quatre WARNING historiques ; aucun ERROR ni nouvelle divergence. Tous les Bash ont été autorisés et terminés ; cela ne transforme pas ces deux validations strictes en succès.

Demandes CAB refusées avant exécution, regroupées ; elles ne sont pas comptées comme Bash exécutés :

| Commande refusée,100 caractères maximum | Occurrences | Part | Effet natif |
| --- | --- | --- | --- |
| /home/devops/python/current/bin/python3 -B -m py_compile tests/unit/test_event_registration.py | 2 | 100.0 % | aucun |
| Total | 2 | 100.0 % | 0 Bash |

| Demande interrompue ou refusée | Statut | Effet source |
| --- | --- | --- |
| cismp3-49b028c97f7d45 | REJECTED_LOCAL_TECHNICAL_ERROR | aucun |
| cismp3-156dec9f2fa14b | REJECTED_PRECONDITION_NOT_MET | aucun |
| cismp3-691557becbe740 | CLOS_SANS_EFFET_OUTIL_INDISPONIBLE | aucun |
| cismp3-8c22ebc9b3564a | CLOS_SANS_EFFET_MCP_TIMEOUT_AVANT_ADMISSION | aucun |

## 5. Accès web

| Outils de visite/recherche web dans les sessions | Total | Approuvés | Refusés | Erreurs | Part |
| --- | --- | --- | --- | --- | --- |
| webfetch/websearch | 0 | 0 | 0 | 0 | N/A — dénominateur nul |
| Total | 0 | 0 | 0 | 0 | N/A |

Aucune URL de page visitée ou refusée n’apparaît dans cet historique natif. Les API locales de pilotage ne sont pas des visites web. Accès fournisseur distincts, autorisés pour la PLLM : https://opencode.ai/zen/go/v1/usage et https://opencode.ai/zen/go/v1/responses ; aucune clé, aucun en-tête secret ni identifiant de session fournisseur conservé ici. Nombre exhaustif des requêtes d’infrastructure : N/A, compteur fournisseur non exposé. Ces endpoints ne sont pas présentés comme pages consultées par l’agent.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début natif | 2026-10-15T07:01:47.985000+00:00 |
| Fin — après archivage et sonde finale | 2026-10-15 16:44:32 UTC |
| Durée globale, pauses et attentes incluses | 09 h 42 min 44 s |

La collecte préparée a démarré à 2026-10-15T07:05:09.923636+00:00 ; la création native ci-dessus établit le début effectif. La durée calendaire n’est ni une somme des temps d’agents ni un temps de génération.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-15 07:04:25 UTC → 2026-10-15 07:04:26 UTC | 1 % | 2026-10-22T06:12:56+00:00 |
| Après — après archivage de la spécification | 2026-10-15 16:44:31 UTC → 2026-10-15 16:44:32 UTC | 14 % | 2026-10-22T06:12:56+00:00 |
| Différence après − avant | — | 13 points de pourcentage | — |

Source : outil natif mcp__codex_app__get_usage_limits, quota codex, fenêtre de 10080 minutes. Même compte vérifié sans en publier l’identifiant, même resetsAt ; aucune réinitialisation traversée. Le quota est partagé : la variation13 points couvre tout le compte, y compris les autres tâches, et n’est pas attribuée exclusivement à ce RUN. Aucune conversion en tokens ou en argent.

| Domaine | Nombre / partglobale | Terminés autorisés / taux | Refuspermission / taux | Erreurs techniques / taux |
| --- | --- | --- | --- | --- |
| fichiers | 8 / 3.4 % | 8 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| commandes | 24 / 10.3 % | 24 / 100.0 % | 0 / 0.0 % | 0 / 0.0 % |
| web | 0 / 0.0 % | 0 / N/A | 0 / N/A | 0 / N/A |
| autres | 200 / 86.2 % | 178 / 89.0 % | 0 / 0.0 % | 22 / 11.0 % |
| Total global | 232 / 100.0 % | 210 / 90.5 % | 0 / 0.0 % | 22 / 9.5 % |

Arrondis à une décimale : les parts arrondies peuvent ne pas sommer exactement100 %, les nombres absolus et totaux sont contrôlés. « Terminés autorisés » inclut les Read/MCP permis automatiquement ; ce n’est pas le nombre de décisions manuelles. Les résultats CLI0/1 sont détaillés séparément. Refus de permission :0 dans ces états d’outil, couverture SSE historique exhaustive N/A. Les2 refus CAB du collecteur sont des demandes de compilation non exécutées, distinctes de ces états natifs.

Coordination CAB observée : file 1361351ms, exclusion 908183ms, référence à réconcilier 520218ms ; champs susceptibles de se recouvrir, non additionnés. Interruption contrôleur inconnue cumulée : 26598ms. Persistance export : READY. Aucun gain causal ou temps productif déduit.

Bilan à la borne :28 tests Pixs/3 compilations/9 tâches prouvés ; archive unique native0 et cinq artefacts exacts ; publication réellement confirmée, référence 19, phaseREPORT sur ce seul fichier. Strictglobal reste exit1 pour4 WARNING historiques, zéro ERROR. Git non inspecté, aucun commit/push effectué par ce RUN. Pas de PostgreSQL pour ce profil passif. Secret PLLM utilisé seulement dans le processus sécurisé, jamais transmis au modèle/rapport/sources ; aucun fichier sensible lu. Le gate individuel et la libération seront vérifiés après ce rapport ; le cycle parent CISMP devra ensuite reprendre la sélection, sans assimiler cette archive à une fin globale.
