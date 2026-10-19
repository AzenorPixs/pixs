# Statistiques — add-initial-architecture-decision-state-v1



RUN : cismp1-pixs-38567544a2534554 ; contexte CAB : 269 ; session native : ses_eb5d4c166fferj0r79sq1iuaYY.

Archive : openspec/changes/archive/2026-10-17-add-initial-architecture-decision-state-v1. Publication technique : publish-9bda851eb9874b58, référence 31.

Intervalle de production : événements du contexte à partir de sa réservation (2026-10-17T14:02:46.206Z) jusqu’à 2026-10-17T16:15:07.855427+02:00. La durée globale commence à la création native de la session. La rédaction de ce rapport, son mandat distinct et les opérations de fermeture ultérieures sont hors intervalle.

Sources : GET /runs/cismp1-pixs-38567544a2534554/statistics (JSON et brouillon Markdown), historique natif intégral filtré du même contexte, mandats et preuves conservés dans /home/devops/datas/pixs/output/cismp/cismp1-pixs-38567544a2534554/state.json. Les agrégats natifs et CAB sont recoupés ; aucune donnée importée ni répartition arbitraire entre RUN.

Un appel terminé avec succès ne prouve pas une approbation manuelle. « Approuvé et exécuté » couvre l’autorisation initiale des lectures et communications, et les décisions explicites CAB des effets. Un refus exige une décision de refus enregistrée ; une erreur technique reste distincte d’un résultat de validation non nul.



### Agents de codage



| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version distincte non exposée | OpenCode Go (opencode-go) | high | 1.914 s | 563.002 (réponse) | N/A — génération non isolée des outils/attentes |


OpenCode observé : 1.19.3. Les 69 messages assistant de production portent exactement le modèle, le fournisseur et le variant high. Les moyennes ci-dessus sont arithmétiques, issues des deux sondes de l’agent de codage, sans outils, fichiers ni réseau demandé au modèle, dans des sessions dédiées jetables. Le transport fournisseur nécessaire à la génération reste distinct d’un accès réseau par l’agent.



### Agents orchestrateurs



| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| N/A — agent Codex | N/A — identité/version exacte non exposée | OpenAI | N/A — non exposé | N/A — aucune sonde orchestrateur | N/A — aucune sonde orchestrateur | N/A — télémétrie de génération non exposée |


Le dénominateur du temps de service cumulé est indisponible : aucun pourcentage ni chevauchement productif n’est estimé. Busy, durée des outils, permissions et durée calendaire ne sont pas assimilés au service du modèle.



## 1. Statistiques générales et décisions



| Mesure | Valeur |
| --- | --- |
| Durée calendaire globale, pauses et attentes incluses | 00 h 13 min 17 s |
| Messages natifs de production | 108 (100.0 %) |
| Appels d’outils natifs | 79 (100.0 %) |
| Décisions CAB explicites approved | 17 (100.0 %) |
| Décisions rejected / clarification / pending | 0 / 0 / 0 (0.0 % chacune) |
| Effets natifs corrélés avec once | 17 / 17 (100.0 %) |
| Outils OC en erreur technique / refusés | 0 / 0 (0.0 %) |
| Échecs fonctionnels de test | 0 / 19 (0.0 %) |
| Contrôles stricts globaux avec code 1 | 2 / 9 commandes (22.2 %) : quatre avertissements de longueur, aucune ERROR |
| Incidents HTTP dans le contrôleur du RUN | 1 decision-run-divergent ; avant admission, sans décision ni effet |
| Erreurs et appels propres à Codex | N/A — audit exhaustif des outils orchestrateur non exposé |
| Compactions OpenCode observées | 0 ; compactions Codex N/A |


Deux permissions natives de communication MCP ont été répondues once par l’orchestrateur pendant le prévol, avant cadrage des noms exacts MCP. Elles ne sont pas confondues avec les 17 permissions d’effets CAB ci-dessus. Une réponse HTTP 400 à un champ de réponse incorrect n’a produit aucun effet ; le champ natif reply a ensuite été utilisé. Un GET décision 404 désignait l’absence de décision, pas un refus.



| Télémétrie de production OpenCode | Valeur | Part du total de tokens |
| --- | --- | --- |
| Entrée hors cache | 390074 | 4.0 % |
| Cache lu | 9212789 | 95.6 % |
| Cache écrit | 0 | 0.0 % |
| Sortie | 23244 | 0.2 % |
| Raisonnement | 9996 | 0.1 % |
| Total | 9636103 | 100.0 % |


Coût rapporté par la télémétrie native : 0.064080978 USD. Ce coût couvre seulement les messages de production identifiés, hors benchmarks, sondes et orchestrateur. La somme entrée + cache lu + cache écrit + sortie + raisonnement égale le total ; les tokens ne sont pas des fragments SSE.



| Sonde | Début | Durée | TTMT | Tokens sortie / raisonnement | Tokens/s réponse | État |
| --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-17T16:05:49.368004+02:00 | 2.908 s | 1.557 s | 776 / 206 | 583.135 | réussie |
| fin | 2026-10-17T16:14:21.156683+02:00 | 3.815 s | 2.272 s | 776 / 373 | 542.869 | réussie |


Protocole constant : Réponds uniquement par les entiers décimaux de 0001 à 0256 inclus, un entier sur chaque ligne, exactement quatre chiffres. Aucun commentaire, aucun outil. Taille : 154 caractères. Prévu : début et fin ; réussies 2/2 (100.0 %), échouées 0, manquées 0. La session dure moins de 30 minutes : aucune relève périodique +30 min n’était échue. Les deux sessions de sonde ont été supprimées après collecte.

TTMT min/max : 1.557/2.272 s ; débit min/max : 542.869/583.135 tokens/s. Surcharge des sondes : 6.723 s, 24174 tokens entrée, 226 cache lu, 1552 sortie et 579 raisonnement ; coût N/A, non conservé pour les sondes.

PLLM mode 1, modèle et high imposés : quotas actuels vérifiés avant chaque tentative ; dernier relevé avant benchmark : 5h 0 %, semaine 63 %, mois 96 % utilisés, tous admissibles. Palier 1024 non concluant (flux incomplet), puis 2048 réussi ; TTFT réponse 6.9065 s. La formule de débit global du testeur inclut le compteur de raisonnement alors que le flux n’exposait pas son premier token : ne pas comparer ce chiffre aux sondes de réponse. La borne inférieure conservatrice (1658 − 1) / 7.2508 = 228.527 tokens/s sur la durée totale de requête, latence incluse, dépasse aussi le seuil 15 et évite de dater le raisonnement caché. Ce benchmark ne remplace aucune preuve du produit. Les essais, quotas, budgets et cause sont conservés dans le checkpoint. Coût du benchmark et tokens manquants de la tentative non concluante : N/A, non reconstruits.



## 2. Types de messages et d’outils



| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 69 | 63.9 % |
| user | 39 | 36.1 % |
| Total | 108 | 100.0 % |


| Type de partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 72 | 19.3 % |
| step-finish | 69 | 18.4 % |
| step-start | 69 | 18.4 % |
| text | 85 | 22.7 % |
| tool | 79 | 21.1 % |
| Total | 374 | 100.0 % |


| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| stop | 21 | 30.4 % |
| tool-calls | 48 | 69.6 % |
| Total | 69 | 100.0 % |


| Outil natif | Total | Part | Approuvé/exécuté | Refusé | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| bash | 9 | 11.4 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 | 1.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 3 | 3.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 17 | 21.5 % | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 8 | 10.1 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 8 | 10.1 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 25 | 31.6 % | 25 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 10.1 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 79 | 100.0 % | 79 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |


Les 17 request_validation correspondent à 8 écritures et 9 commandes. Les autres appels MCP sont readiness (3) et broker_health (1), sans décision métier. Les lectures/recherches sont autorisées par leur mandat de lecture seule, sans approbation manuelle inventée.



## 3. Fichiers modifiés



Les nombres ci-dessous sont des tentatives d’écriture natives : 8 réussies, 7 fichiers distincts. Les quatre documents du dossier change ont ensuite été déplacés par l’unique commande d’archivage ; ce déplacement n’est pas compté comme quatre écritures supplémentaires. Le rapport lui-même est hors intervalle.



| Chemin absolu complet à l’écriture | Écritures approuvées/exécutées | Part des écritures | Refusées | Erreur technique |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-architecture-decision-state-v1/.openspec.yaml | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-architecture-decision-state-v1/design.md | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-architecture-decision-state-v1/proposal.md | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-architecture-decision-state-v1/tasks.md | 2 (100.0 %) | 25.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/architecture_decision_state.py | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_architecture_decision_state_integration.py | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_architecture_decision_state.py | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100.0 % | 0 (0.0 %) | 0 (0.0 %) |


Destination des documents : /home/devops/datas/pixs/openspec/changes/archive/2026-10-17-add-initial-architecture-decision-state-v1/. Le module et les deux tests restent dans leurs chemins sources. Les caches de compilation sont des artefacts régénérables couverts par le manifeste, pas des sources lues. Empreintes contrôlées inchangées : AGENTS, PROJECT, TECHNICAL, BUILD, DEVOPS, README, ORCHESTRATED_CODING, openspec/config.yaml, canons architecture-decisions/bulk-operations/identity-assurance, façade kernel et test d’intégration de référence. La provenance Git n’a pas été inspectée.



## 4. Commandes



| Famille | Nombre | Part | Approuvé/exécuté | Refusé | Erreur outil |
| --- | --- | --- | --- | --- | --- |
| Prévol /usr/bin/true | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Unittest : 19 tests | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Validation OpenSpec | 5 | 55.6 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Archivage OpenSpec | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |


| Commande exécutée, libellé au plus 100 caractères | Occurrences | Part |
| --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-architecture-decision-state-v1 --yes --ski… | 1 | 11.1 % |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 11.1 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 22.2 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-architecture-decision-state-v1 --strict | 2 | 22.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/architecture_decision_state… | 1 | 11.1 % |
| /usr/bin/true | 1 | 11.1 % |
| PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest tests.unit… | 1 | 11.1 % |
| Total | 9 | 100.0 % |


Commandes refusées : aucune (0). Sept commandes ont un exit 0 ; les deux stricts globaux ont un exit 1 pour les quatre warnings de longueur hors périmètre. Aucun échec de test ou de syntaxe. Les commandes complètes sont dans les mandats natifs et le checkpoint, sans secret.



## 5. Accès web



Aucun outil web de l’agent de codage : 0 appel, pourcentages N/A (dénominateur nul). Les 5 requêtes HTTPS suivantes proviennent du processus sécurisé de prévol PLLM de l’orchestrateur, autorisé par l’invocation CISMP : modèle publié (1), quotas (2), génération (2). Elles sont distinctes des 79 outils natifs de production et des requêtes fournisseur internes OpenCode, dont les URL effectives ne sont pas collectées.



| URL effectivement appelée, au plus 100 caractères | Nombre | Part | Autorisé/appelé | Refusé | Erreur HTTP observée |
| --- | --- | --- | --- | --- | --- |
| https://opencode.ai/zen/go/v1/models | 1 | 20.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| https://opencode.ai/zen/go/v1/usage | 2 | 40.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| https://opencode.ai/zen/go/v1/responses | 2 | 40.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 5 | 100.0 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |


La première génération n’a pas fourni de mesure concluante : cela ne transforme pas son accès HTTP en refus. URL refusées : aucune observée. Les accès locaux HTTP de contrôle et le nombre exact d’appels fournisseur induits par OpenCode sont N/A pour l’inventaire exhaustif ; aucun zéro global inventé. Aucun en-tête, secret ou identifiant de session fournisseur n’est publié.



## 6. Synthèse globale



| Durée de la session de codage | Valeur |
| --- | --- |
| Début — création native | 2026-10-17T16:01:50.489000+02:00 |
| Fin — après archivage et sonde finale, avant rédaction | 2026-10-17T16:15:07.855427+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 13 min 17 s |


| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil get_usage_limits non exposé | N/A | N/A |
| Après — après archivage de la spécification | N/A — outil get_usage_limits non exposé | N/A | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | — |


Le quota Codex (identité codex, fenêtre 10080 minutes) n’a pas pu être lu. Aucun quota Spark ou OpenCode Go n’est substitué. Les quotas de compte sont partagés ; même disponible, leur variation pourrait inclure d’autres tâches simultanées et ne serait pas imputée exclusivement à ce RUN.



| Domaine observé | Nombre | Part globale | Approuvé/exécuté | Refusé | Erreur technique observée |
| --- | --- | --- | --- | --- | --- |
| Fichiers — tentatives natives | 8 | 9.5 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes natives | 9 | 10.7 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web technique PLLM hors outils natifs | 5 | 6.0 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Autres outils natifs | 62 | 73.8 % | 62 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total du périmètre compté | 84 | 100.0 % | 84 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |


Contrôle croisé : 8 + 9 + 62 = 79 outils natifs ; + 5 appels HTTPS techniques = 84 actions du périmètre compté. Les 17 décisions CAB ne sont pas ajoutées comme de nouveaux effets. Ce total n’est pas un inventaire exhaustif des outils Codex : les lacunes restent N/A, et l’incident HTTP du contrôleur reste distinct. Les arrondis de parts peuvent ne pas sommer exactement à 100.0 %.



| Résultat de développement | État prouvé |
| --- | --- |
| Syntaxe | Trois fichiers py_compile, exit 0 |
| Tests | 19/19 réussis (100.0 %), 0 échec, 0 skip |
| OpenSpec ciblé | Deux validations strictes du change, exit 0 ; canon architecture-decisions valide |
| OpenSpec global standard avant archive | 186/186 éléments valides, exit 0 |
| OpenSpec strict avant / après archive | 184/186 puis 183/185 ; exit 1, 4 warnings de longueur dans deux canons non modifiés, 0 ERROR |
| Archivage | Une archive unique réussie, exit 0 ; tâches complètes ; --skip-specs, canon inchangé |
| Publication technique | Reçu publish-9bda851eb9874b58, référence 31, phase REPORT |
| Périmètre fonctionnel | Vocabulaire seul ; ne prouve pas modèle, transitions, lien de remplacement ou historique complets |
| Git | Aucune inspection, aucun commit/push ; provenance N/A |
| Accès externes et secrets | Seuls prévol fournisseur autorisé et générations OpenCode nécessaires ; secrets confinés au processus, aucun secret inclus dans les sources ou ce rapport |
| Clôture | Rapport à vérifier ; gate, désarmement/libération et fermeture OpenCode effectués ensuite, aucune réussite anticipée |


La session s’arrête après ce seul change selon la demande explicite. Le cycle global Pixs reste incomplet ; aucun prochain change n’est sélectionné.
