# Statistiques — add-initial-inbox-receipt-state-v1

RUN cismp1-pixs-ac814b7269a74c1b ; contexte CAB 294 ; session de codage ses_eb0c57d4bffe2OAJ0nd4ZqI43S.

Périmètre : un change complet, archivage, statistiques puis arrêt ciblé. Intervalle mesuré clos avant rédaction du présent rapport : 2026-10-18T13:33:51.235392+00:00 à 2026-10-18T13:51:34.308648+00:00 (UTC). Les observations CAB commencent à la réservation, 13:36:37 UTC. Les outils et tokens ci-dessous concernent uniquement cette session métier, avant la borne finale. La sélection, les sondes, le prévol PLLM et la rédaction du rapport sont comptés séparément ou exclus explicitement.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go / opencode-go | high | 2.548 s | 395.296 | N/A — durée de génération non isolable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex, famille GPT-6 | N/A — identité exacte non exposée | OpenAI | N/A — télémétrie absente | N/A — aucune sonde orchestrateur | N/A — télémétrie absente | N/A — dénominateur non mesurable |

Les temps busy, outils et attentes ne sont pas des durées de génération. Aucun pourcentage de service n’est estimé ; les chevauchements ne sont pas additionnés. OpenCode 1.19.3 et CAB 1.3.0 sont des versions d’agents/services, pas une version exacte du modèle.

## 1. Statistiques générales et décisions

Livraison : Enum backend passif InboxReceiptState au seul membre CONSUMED, trois fichiers Python nouveaux et quatre artefacts OpenSpec nouveaux ; aucun fichier préexistant du périmètre contrôlé modifié. 26/26 tests réussis (100,0 %), dont 5 nouveaux et 21 régressions ; trois compilations réussies (100,0 %). OpenSpec ciblé strict code 0, global standard 186/186 code 0 ; strict global avant archive 184/186 code 1 et après archive 183/185 code 1, uniquement quatre WARNING historiques de longueur dans bulk-operations[6,10,13] et identity-assurance[4], zéro ERROR.

Archive effective : openspec/changes/archive/2026-10-18-add-initial-inbox-receipt-state-v1 ; commande native code 0. Publication CAB publish-7cade50497fb44ce, référence 35. Gate et arrêt sont encore à effectuer après vérification du rapport ; le cycle global du projet n’est pas déclaré achevé.

| Décision CAB | Nombre | Part |
|---|---|---|
| Approuvée | 17 | 100,0 % |
| Refusée | 0 | 0,0 % |
| Clarification | 0 | 0,0 % |
| En attente | 0 | 0,0 % |
| Total | 17 | 100,0 % |

17 décisions explicitement rendues par Codex, 17 permissions natives once observées et 17 opérations exécutées : 8 écritures et 9 commandes. Aucune décision n’a été réutilisée. Un outil terminé ne prouve pas à lui seul une approbation manuelle ni la réussite d’une validation. Trois commandes strictes ont un code 1 pour avertissements connus ; elles restent distinctes du refus de permission et de l’unique erreur native de lecture.

| Mesure métier native | Valeur |
|---|---|
| Messages | 114 |
| Outils | 73 |
| Outils completed | 72 (98.6 %) |
| Erreurs natives | 1 (1.4 %) |
| Compactions | 0 observée ; échéance de 90 min non atteinte |
| Entrée tokens (champ natif input) | 370402 |
| Sortie tokens (champ natif output) | 27672 |
| Raisonnement tokens | 9130 |
| Cache lu / écrit | 10669911 / 0 |
| Tokens total fournis par OpenCode | 11077115 |
| Coût natif cumulé, USD | 0.065740422 |

Les compteurs de tokens sont les champs natifs agrégés ; ils ne sont pas additionnés arbitrairement pour reconstruire un autre total. Leur coût concerne la session métier avant rédaction du rapport.

| Sonde dédiée high | Session | TTMT | Débit sortie | Tokens sortie | Résultat |
|---|---|---|---|---|---|
| début | ses_eb0c6e050ffev7tiLAsMZBTFTz | 3.361 s | 320.810 tokens/s | 329 | Réussie |
| fin | ses_eb0b87527ffeW3eUqq13O26ZaW | 1.736 s | 469.782 tokens/s | 308 | Réussie |

Sondes : 2 prévues, 2 réussies (100,0 %), 0 échouée, 0 manquée. Intervalle de codage inférieur à 30 minutes : aucune relève périodique due. Prompt constant : entiers 001 à 150 séparés par une espace, sans outil ni accès fichier/réseau demandé au modèle. Débit = tokens de sortie natifs / durée entre premier et dernier delta textuel SSE ; TTMT depuis l’envoi. Version exacte N/A. TTMT min/max 1.736/3.361 s ; débit min/max 320.810/469.782. Surcharge : 637 tokens de sortie, 723 de raisonnement, durée calendaire native cumulée 6,782 s et coût 0,002525126 USD ; exclus de la production.

PLLM mode 1 imposée Muse high : deux tentatives réelles, 1 024 tokens inconclusif puis 2 048 réussi, TTFT 9,9846 s, débit global mesuré 3 010,369 tokens/s. La borne conservatrice incluant toute la durée de requête vaut 132,693 tokens/s. Ces mesures du benchmark ne remplacent pas les moyennes des sondes. Quotas utilisés au prévol : 5 h 0 %, semaine 65 %, mois 97 %.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 43 | 37.7 % |
| assistant | 71 | 62.3 % |
| Total | 114 | 100,0 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 102 | 26.0 % |
| step-start | 71 | 18.1 % |
| reasoning | 75 | 19.1 % |
| tool | 73 | 18.6 % |
| step-finish | 71 | 18.1 % |
| Total | 392 | 100,0 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 50 | 70.4 % |
| stop | 21 | 29.6 % |
| Total | 71 | 100,0 % |

| Famille | Total et part | Completed et taux | Erreur et taux | Refus |
|---|---|---|---|---|
| cab-mcp | 19 (26.0 %) | 19 (100.0 %) | 0 (0.0 %) | 0 (0,0 %) |
| bash | 9 (12.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0,0 %) |
| read | 30 (41.1 %) | 29 (96.7 %) | 1 (3.3 %) | 0 (0,0 %) |
| glob | 4 (5.5 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0,0 %) |
| grep | 3 (4.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0,0 %) |
| write | 8 (11.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0,0 %) |
| Total | 73 (100,0 %) | 72 (98.6 %) | 1 (1.4 %) | 0 (0,0 %) |

Erreur native : lecture d’un chemin diagnostics.py inexistant ; le package diagnostics a ensuite été identifié. Aucun effet d’écriture. Incident HTTP d’orchestration distinct : une progression avec mandat null refusée, puis release refusé run-not-quiescent ; correction en chaîne vide, sans rejeu de /usr/bin/true ni perte de once. Le compteur CAB expose un refus HTTP run-not-quiescent ; les erreurs HTTP ne sont pas des refus de permission.

## 3. Fichiers modifiés

| Chemin absolu final | Tentatives et part | Approuvées/exécutées | Refusées | Erreur |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-inbox-receipt-state-v1/.openspec.yaml | 1 (12.5 %) | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-inbox-receipt-state-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-inbox-receipt-state-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-inbox-receipt-state-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/backend/inbox_receipt_state.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_inbox_receipt_state.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_inbox_receipt_state_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total : 7 fichiers | 8 (100,0 %) | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Les quatre artefacts ont été créés sous openspec/changes/add-initial-inbox-receipt-state-v1 puis déplacés par une unique commande OpenSpec d’archivage. tasks.md compte deux écritures, les coches n’étant ajoutées qu’après preuves. Les tentatives du présent STATISTIQUES.md sont hors intervalle, sous mandat distinct à venir. Les écritures régénérables py_compile et les répertoires temporaires de tests sont des effets de commandes, pas des fichiers source supplémentaires. Le contenu et les empreintes des références préexistantes ont été contrôlés sans Git.

## 4. Commandes

| Commande observée, libellé borné à 100 caractères | Nombre et part | Codes de sortie | Refus |
|---|---|---|---|
| /usr/bin/true | 1 (11.1 %) | [0] | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/inbox_receipt_state.py tes… | 1 (11.1 %) | [0] | 0 (0,0 %) |
| PYTHONPATH=src:tests:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m u… | 1 (11.1 %) | [0] | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-inbox-receipt-state-v1 --strict | 1 (11.1 %) | [0] | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate --all | 1 (11.1 %) | [0] | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 (22.2 %) | [1, 1] | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate bulk-operations --type spec --strict | 1 (11.1 %) | [1] | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-inbox-receipt-state-v1 --yes | 1 (11.1 %) | [0] | 0 (0,0 %) |
| Total | 9 (100,0 %) | 6 codes 0 ; 3 codes 1 | 0 (0,0 %) |

| Famille | Nombre | Part |
|---|---|---|
| Python : compilation/tests | 2 | 22.2 % |
| OpenSpec : validations/archive | 6 | 66.7 % |
| Système : prévol inoffensif | 1 | 11.1 % |
| Total | 9 | 100,0 % |

Commandes refusées : aucune (0 ; taux 0,0 % sur 9 demandes de commande). Succès code 0 : 6/9 (66,7 %) ; sorties non nulles : 3/9 (33,3 %), validations strictes liées aux avertissements explicités en section 1. Les commandes complètes et sorties sont conservées dans les outils natifs de la session et dans le checkpoint non secret.

## 5. Accès web

Outils webfetch/websearch : 0 appel ; approbations 0, refus 0, erreurs 0 ; taux N/A (dénominateur nul). Aucune URL visitée par un outil web métier.

| Prévol fournisseur hors outils métier | URL autorisée et effectivement appelée | Requêtes | Résultat |
|---|---|---|---|
| Quotas | https://opencode.ai/zen/go/v1/usage | 2 | Réponses valides avant chaque tentative |
| Catalogue modèle | https://opencode.ai/zen/go/v1/models | 1 | Muse demandé présent |
| Benchmark | https://opencode.ai/zen/go/v1/responses | 2 | 1 inconclusif, 1 réussi |
| Total | — | 5 | Aucun refus de permission |

Ces accès de service sont ceux du prévol PLLM sécurisé explicitement autorisé, distincts des outils web et des échanges modèles OpenCode. Les secrets sont restés dans le processus sécurisé ; aucune valeur n’est incluse dans les prompts, les sorties ou ce rapport. Les adresses loopback OpenCode/CAB sont des interfaces locales, pas des visites web externes.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début, consignation du RUN | 2026-10-18T13:33:51.235392+00:00 |
| Fin — après archivage, sonde finale et relevé de quota | 2026-10-18T13:51:34.308648+00:00 |
| Durée globale, pauses et attentes incluses | 00 h 17 min 43 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé consigné | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-18T13:33:51.235392+00:00 | 8 % | 2026-10-24T23:23:28+00:00 |
| Après — après archivage | 2026-10-18T13:51:34.308648+00:00 | 9 % | 2026-10-24T23:23:28+00:00 |
| Différence après − avant | — | +1 point de pourcentage | — |

Outil natif mcp__codex_app__get_usage_limits : entrée codex, fenêtre 10 080 min, même compte et même resetsAt. Quota partagé : la variation peut inclure d’autres tâches simultanées ; aucune attribution exclusive au RUN. La rédaction ultérieure du rapport est exclue de l’intervalle.

| Domaine | Nombre et part | Completed et taux | Refus et taux | Erreur native et taux |
|---|---|---|---|---|
| Fichiers : éditions | 8 (11.0 %) | 8 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| Commandes | 9 (12.3 %) | 9 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| Web natif | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils : CAB/lecture/recherche | 56 (76.7 %) | 55 (98.2 %) | 0 (0,0 %) | 1 (1.8 %) |
| Total | 73 (100,0 %) | 72 (98.6 %) | 0 (0,0 %) | 1 (1.4 %) |

Coordination CAB attribuée au contexte 294 : attente de ressource 0.000 s ; détention partagée 477.083 s ; effet natif sous suivi 5.392 s ; 0 réconciliation ciblée et 0 gel global. Ces durées peuvent se recouvrir ; busy ne prouve aucun gain de productivité. Les lacunes historiques globales du service ne sont pas imputées à ce change.

Après la borne de collecte, le superviseur a envoyé une relance : readiness/health et lecture de la seule archive ont reconfirmé l’attente du rapport, sans écriture métier ni nouveau change. Ces événements et la création du présent rapport sont hors statistiques de production.

Résultat vérifié : 26 tests OK, compilation 0, archive unique et publication référence 35. Strict global non réussi, limité aux quatre avertissements historiques documentés. Base de données et navigateur N/A pour ce vocabulaire passif. Git ni inspecté ni modifié, aucun commit/push. Aucun secret exposé ou persisté dans les sources. Les services partagés et le RUN CISMP3 en pause sont préservés. Gate, désarmement et libération seront demandés après contrôle des six sections, de l’encodage et des totaux ; cette étape n’affirme pas la fin globale du projet.
