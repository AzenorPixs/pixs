# Statistiques — EventPublicationState v1

RUN cismp2-pixs-656eb3d126af4862 ; change add-initial-event-publication-state-v1 ; contexte CAB 279 ; projet /home/devops/datas/pixs.
Archive vérifiée : openspec/changes/archive/2026-10-18-add-initial-event-publication-state-v1. Un seul change puis arrêt ciblé.
Collecte arrêtée le 2026-10-18T02:12:14+02:00, après archivage et sonde finale, avant rédaction. Le présent rapport, sa permission et sa rédaction sont exclus des comptes.
Comptage exhaustif des appels propres à Codex : N/A, historique natif de l’orchestrateur non exposé ; les décisions CAB sont suivies séparément. Pourcentages arrondis à une décimale : les sommes des arrondis peuvent différer de 0,1 point.

Historique HTTP natif complet des deux sessions du RUN retenu pour les tableaux ; agrégat CAB du contexte 279 conservé séparément. Aucun événement CISMP1/CISMP3 attribué à CISMP2.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go / opencode-go | high | 1.897 s | 427.484 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex — identifiant natif du modèle non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Moyennes de codage : deux sondes valides ; aucune sonde de l’orchestrateur. Temps de service actif et dénominateur cumulé non mesurables : ni durée calendaire, ni busy, ni attente d’outil ne les remplacent. Chevauchements de service non déduits.

## 1. Statistiques générales et décisions

Durée de la session native : 00 h 25 min 24 s, pauses et attentes incluses. La préparation PLLM antérieure est exclue de cette durée ; sa première borne observée est 2026-10-18T01:27:53+02:00.
Sessions : ses_eb3bd2cf3ffeRccBotZ83As60M puis ses_eb3b9440effeCcFUZFXa0kWwY1, même job job-179b51defe7743a8. Modèle/fournisseur/raisonnement inchangés.
Un statut completed est compté « approuvé et exécuté » pour le transport observé ; il ne prouve pas une approbation manuelle. Les écritures et commandes ont séparément leurs décisions CAB et permissions once. Refus de permission et erreur technique restent distincts. Les deux contrôles stricts exit 1 sont des résultats de validation non passants, malgré un appel Bash achevé.

| Résultat des appels natifs | Nombre | Part |
|---|---:|---:|
| Approuvés et exécutés / completed | 101 | 92.7 % |
| Refus de permission explicites | 0 | 0,0 % |
| Erreurs techniques / error | 8 | 7.3 % |
| Total des tentatives | 109 | 100 % |

| Décisions CAB — contexte 279 | Nombre | Part |
|---|---:|---:|
| approved | 19 | 100 % |
| rejected | 0 | 0,0 % |
| needs_clarification | 0 | 0,0 % |
| Total | 19 | 100 % |
| Permissions once corrélées | 19 | 100 % des approved |

Une demande py_compile périmée a été annulée avant effet, sans décision admise ni permission : cache passé de révision 84 à 167 pendant une compilation concurrente. Nouvelle identité sur base fraîche ensuite réussie ; aucune commande rejouée. Le premier prévol automatique incomplet avait échoué avant enregistrement (-32602). Timeouts MCP réconciliés avec le même approval_id. Aucune purge ni récupération commune exécutée.

| Compteurs de tokens natifs de production | Valeur | Part de leur somme |
|---|---:|---:|
| Entrée non cachée | 565867 | 4.1 % |
| Lecture du cache | 13031867 | 95.5 % |
| Écriture du cache | 0 | 0.0 % |
| Sortie | 34898 | 0.3 % |
| Raisonnement | 15904 | 0.1 % |
| Total des compteurs | 13648536 | 100 % |

Coût natif OpenCode : 0.092811 $ (télémétrie, pas une facture fournisseur), hors sondes et benchmark PLLM. Compteurs cumulés par appel, dont relectures du cache ; ce ne sont ni des données uniques ni le quota Codex. Compactions natives observées : 0 ; aucune réussite de compactage conjoint revendiquée.

| Sonde | Statut | TTMT | Tokens/s | Tokens sortie | Durée calendaire |
|---|---|---:|---:|---:|---:|
| début | failed | N/A | N/A | 665 | 4.378 s |
| début-reprise-unique | success | 2.054 s | 388.695 | 665 | 3.893 s |
| fin | success | 1.739 s | 466.274 | 657 | 3.187 s |

Relèves prévues : 2 ; réussies : 2 (100 %) ; manquées : 0 (0 %). Tentatives : 3, dont 2 valides (66,7 %) et 1 invalidée (33,3 %). Le premier filtre SSE incluait le texte utilisateur : invalidation conservée et unique reprise immédiate, exclue des moyennes. Le créneau +30 minutes après la sonde initiale valide n’a pas été atteint avant la sonde finale.
Surcharge des sondes séparée : 1987 tokens de sortie, 1492 de raisonnement, 11.457 s calendaires. Coût total N/A : non conservé pour les deux premières tentatives ; seule la fin expose 0.0014928 $.
TTMT min/max : 1.739/2.054 s ; débit min/max : 388.695/466.274 tokens/s. Prompt constant, sessions jetables sans outil ; premier/dernier événement SSE de texte assistant et tokens natifs.
PLLM mode 1 imposée : muse-spark-1.3-contributor sur high, benchmark validé le 2026-10-18T01:44:58+02:00, palier 2048 tokens, TTFT 4.9082 s. Quotas fournisseur utilisés au contrôle initial réussi : 5 h 0 %, semaine 64 %, mois 97 % ; distincts du quota Codex.

Validation produit : trois compilations séparées exit 0 ; 54 tests réussis (100 %, 0 échec) en 0,982 s. OpenSpec ciblé strict avant/après : exit 0 ; globale standard avant archive : 187/187 (100 %), exit 0. Stricte avant : 185/187, exit 1 ; après archive : 184/186, exit 1. Quatre WARNING de longueur préexistants : bulk-operations requirements[6]/[10]/[13] et identity-assurance requirements[4], zéro ERROR. Aucun succès strict global annoncé.

## 2. Types de messages et d’outils

| Rôle natif | Nombre | Part |
|---|---:|---:|
| user | 52 | 32.3 % |
| assistant | 109 | 67.7 % |
| Total | 161 | 100 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 137 | 23.6 % |
| step-start | 109 | 18.8 % |
| reasoning | 117 | 20.2 % |
| tool | 109 | 18.8 % |
| step-finish | 108 | 18.6 % |
| Total | 580 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---:|---:|
| tool-calls | 79 | 72.5 % |
| stop | 29 | 26.6 % |
| absent | 1 | 0.9 % |
| Total | 109 | 100 % |

| Outil | Total | Part globale | Achevés | Taux achevés | Refus | Erreurs | Taux erreur |
|---|---:|---:|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 9 | 8.3 % | 8 | 88.9 % | 0 | 1 | 11.1 % |
| cgpt-validation_broker_health | 3 | 2.8 % | 3 | 100.0 % | 0 | 0 | 0.0 % |
| cgpt-validation_list_pending | 3 | 2.8 % | 3 | 100.0 % | 0 | 0 | 0.0 % |
| cgpt-validation_request_validation | 21 | 19.3 % | 18 | 85.7 % | 0 | 3 | 14.3 % |
| cgpt-validation_poll_approval | 3 | 2.8 % | 1 | 33.3 % | 0 | 2 | 66.7 % |
| cgpt-validation_get_approval | 2 | 1.8 % | 2 | 100.0 % | 0 | 0 | 0.0 % |
| bash | 11 | 10.1 % | 11 | 100.0 % | 0 | 0 | 0.0 % |
| read | 31 | 28.4 % | 30 | 96.8 % | 0 | 1 | 3.2 % |
| grep | 7 | 6.4 % | 6 | 85.7 % | 0 | 1 | 14.3 % |
| todowrite | 2 | 1.8 % | 2 | 100.0 % | 0 | 0 | 0.0 % |
| glob | 8 | 7.3 % | 8 | 100.0 % | 0 | 0 | 0.0 % |
| write | 8 | 7.3 % | 8 | 100.0 % | 0 | 0 | 0.0 % |
| cgpt-validation_cancel_approval | 1 | 0.9 % | 1 | 100.0 % | 0 | 0 | 0.0 % |
| Total | 109 | 100 % | 101 | 92.7 % | 0 | 8 | 7.3 % |

## 3. Fichiers modifiés

Nombres de tentatives d’écriture, pas de lignes de code ni de fichiers uniques. Le déplacement des quatre artefacts OpenSpec relève de la commande d’archive. Les trois caches pyc explicitement couverts sont régénérables, pas des écritures source. Le présent rapport est créé après la borne de collecte.

| Chemin absolu complet | Écritures exécutées | Part des écritures | Refus | Erreurs | Taux réussite |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-event-publication-state-v1/.openspec.yaml | 1 | 12.5 % | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-publication-state-v1/proposal.md | 1 | 12.5 % | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-publication-state-v1/design.md | 1 | 12.5 % | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-event-publication-state-v1/tasks.md | 2 | 25.0 % | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/src/pixs/backend/event_publication_state.py | 1 | 12.5 % | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/tests/unit/test_event_publication_state.py | 1 | 12.5 % | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/tests/integration/test_event_publication_state_integration.py | 1 | 12.5 % | 0 | 0 | 100.0 % |
| Total : 7 fichiers uniques | 8 | 100 % | 0 | 0 | 100 % |

Quatre fichiers déplacés une seule fois de openspec/changes/add-initial-event-publication-state-v1/ vers openspec/changes/archive/2026-10-18-add-initial-event-publication-state-v1/, SHA-256 conservés. Seize empreintes de fichiers existants inchangées. Aucune façade ni canon modifié. Git non inspecté : provenance historique du répertoire partagé non établie.

## 4. Commandes

| Famille | Exécutées | Part | Refus | Erreur d’appel | Exit 0 | Exit 1 |
|---|---:|---:|---:|---:|---:|---:|
| Prévol inoffensif | 1 | 9,1 % | 0 | 0 | 1 | 0 |
| Compilation Python | 3 | 27,3 % | 0 | 0 | 3 | 0 |
| Tests Python | 1 | 9,1 % | 0 | 0 | 1 | 0 |
| Validations OpenSpec | 5 | 45,5 % | 0 | 0 | 3 | 2 |
| Archivage OpenSpec | 1 | 9,1 % | 0 | 0 | 1 | 0 |
| Total | 11 | 100 % | 0 | 0 | 9 | 2 |

| Commande — libellé limité à 100 caractères | Occurrences | Part | Codes natifs |
|---|---:|---:|---|
| /usr/bin/true | 1 | 9.1 % | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-event-publication-state-v1 --strict | 2 | 18.2 % | 0,0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/event_publication_state.py | 1 | 9.1 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_event_publication_state.py | 1 | 9.1 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_event_publication_st… | 1 | 9.1 % | 0 |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unitte… | 1 | 9.1 % | 0 |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 9.1 % | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 18.2 % | 1,1 |
| /home/devops/.local/npm/bin/openspec archive add-initial-event-publication-state-v1 --yes | 1 | 9.1 % | 0 |
| Total | 11 | 100 % | 9 sorties 0, 2 sorties 1 |

Commandes refusées par permission : aucune. Une demande de compilation périmée annulée avant effet, non comptée parmi les onze exécutées ni comme refus. Les deux sorties 1 correspondent aux warnings stricts historiques ; aucun test Python échoué.

## 5. Accès web

| Appels d’outils web du codeur | Nombre | Part |
|---|---:|---:|
| Approuvés/exécutés | 0 | N/A — dénominateur nul |
| Refusés | 0 | N/A — dénominateur nul |
| Erreurs | 0 | N/A — dénominateur nul |
| Total | 0 | N/A — aucun appel |

Aucune URL visitée ou refusée par un outil web. Les API locales CAB/OpenCode et les appels techniques du modèle ne sont pas des consultations de pages. Le contrôle PLLM antérieur a interrogé les endpoints autorisés OpenCode Go ; aucune valeur de clé ni en-tête d’authentification conservé dans le rapport.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — première session native | 2026-10-18T01:46:50+02:00 |
| Fin — après archivage et sonde finale | 2026-10-18T02:12:14+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 25 min 24 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage de la spécification | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

L’outil natif mcp__codex_app__get_usage_limits n’est pas exposé : aucun relevé réel disponible. Le quota OpenCode Go ne remplace pas celui de Codex. Quotas de compte partagés ; aucune attribution exclusive au RUN ni conversion en tokens/coût.

| Domaine | Tentatives | Part globale | Exécutées | Refus | Erreurs | Taux réussite | Taux refus | Taux erreur |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fichiers | 8 | 7.3 % | 8 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| Commandes | 11 | 10.1 % | 11 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| Web | 0 | 0.0 % | 0 | 0 | 0 | N/A | N/A | N/A |
| Autres outils | 90 | 82.6 % | 82 | 0 | 8 | 91.1 % | 0.0 % | 8.9 % |
| Global | 109 | 100 % | 101 | 0 | 8 | 92.7 % | 0,0 % | 7.3 % |

Contrôleur, contexte 279 : 19 décisions approved et 19 once ; messages {'user': 49, 'assistant': 99}. Ses agrégats d’événements ne couvrent pas exactement l’historique HTTP complet ({'user': 52, 'assistant': 109}, 109 outils). Écart conservé sans reconstitution ; tableaux issus des parties natives dédupliquées par identifiant. Export JSON et brouillon Markdown filtrés référencés dans le checkpoint.
Coordination de ce RUN : attente ressources 0.000 s ; protections partagées 415.966 s ; effets émis suivis 6.167 s. Durées recouvrantes possibles, pas du codage productif. Échecs HTTP {'native-validation-not-correlated': 3, 'reservation-version-stale': 1, 'resource-revision-stale': 4}, distincts des refus de permission. Aucun gel global exécuté.

Archive native réussie une seule fois ; publication CAB publish-05a37c81e1c84ccc en référence 33. Dernière écriture demandée : le présent rapport. Sa vérification, le gate, le désarmement et la libération se prouvent après rédaction, hors borne de collecte.
Tests réussis ; strict global limité aux quatre warnings historiques. Aucun Git, installation, migration, provider concret, publication externe ou effet métier. Secrets utilisés uniquement par le processus sécurisé PLLM, sans valeur exposée dans les sources ou prompts. Arrêt après ce seul change ; achèvement global de Pixs non revendiqué.
