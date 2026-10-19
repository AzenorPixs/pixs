# Statistiques — CISMP7 — CapabilityCriticality

RUN : `cismp7-pixs-bd898b1b379b4070` ; contexte CAB : 341 ; session de codage : `ses_eaf9343caffena34nb0js5e8G6`. Un seul change : `add-initial-capability-criticality-vocabulary-v1`. Modèle imposé : PLLM mode 1, muse-spark-1.3-contributor, high.

Sources : historique natif intégral de cette session, agrégats JSON et brouillon Markdown CAB filtrés par RUN/contexte, preuves des opérations et sondes dédiées. Photographie fixée avant rédaction du présent rapport : son écriture et les opérations ultérieures de gate/clôture sont exclues des compteurs. Aucun contenu secret ni historique d’un autre RUN utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go | high | 2.288 s | 411.441 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex (GPT-6) | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A | N/A | N/A |

OpenCode observé : 1.19.3. Le nom du modèle ne constitue pas une version télémétrique. Temps de service et dénominateur cumulé des agents indisponibles : aucune assimilation des attentes, appels d’outils ou durées de messages à du temps de génération. Aucun débit d’orchestrateur estimé.

## 1. Statistiques générales et décisions

Intervalle de collecte : 18/10/2026 21:09:57 CEST à 18/10/2026 21:28:24 CEST ; durée 00 h 18 min 26 s, pauses et attentes incluses. Les lectures préparatoires antérieures à la borne conservée ne sont pas chronométrées.

| Résultat natif | Nombre | Part |
|---|---:|---:|
| Terminés | 81 | 98.8 % |
| Erreurs techniques | 1 | 1.2 % |
| Refus de permission | 0 | 0.0 % |
| En cours | 0 | 0.0 % |
| Total | 82 | 100.0 % |

Convention : « terminé » indique une invocation effectivement achevée, automatiquement autorisée ou couverte par une décision CAB ; ce statut ne prouve ni approbation humaine ni validation fonctionnelle. Les deux validations strictes globales sont des commandes terminées avec code 1, distinguées des refus de permission et des erreurs de transport. L’erreur native est l’appel MCP interrompu, réconcilié puis annulé sans effet.

| Décisions CAB | Nombre | Part |
|---|---:|---:|
| Approuvées | 18 | 100.0 % |
| Refusées | 0 | 0.0 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 18 | 100.0 % |

17 permissions natives once sur 18 décisions approuvées (94,4 %) ; une demande approuvée puis en attente de ressource a été annulée avant permission/exécution. Les 8 écritures et 9 commandes exécutées ont leurs permissions unitaires. Une réservation ou une publication ne vaut jamais approbation.

| Mesure native de production | Valeur |
|---|---:|
| Tokens entrée hors cache | 482 542 |
| Tokens sortie | 29 596 |
| Tokens raisonnement | 7 361 |
| Tokens cache lus | 14 612 749 |
| Tokens cache écrits | 0 |
| Coût déclaré OpenCode | 0.084871098 |
Unité du coût non exposée dans la réponse native ; ce chiffre n’est pas une facture fournisseur. Les catégories de tokens sont reproduites séparément sans supposer une partition additive. Compactions : aucune lancée ; première échéance à 1 h 30 non atteinte.

| Sonde dédiée | TTMT | Débit sortie | Tokens sortie | Tokens raisonnement |
|---|---:|---:|---:|---:|
| début | 2.274 s | 356.168 tokens/s | 920 | 1509 |
| fin | 2.301 s | 466.714 tokens/s | 908 | 342 |
| Moyenne des deux sondes | 2.288 s | 411.441 tokens/s | N/A | N/A |

Sondes prévues/réussies : 2/2 (100,0 %) ; échouées/manquées : 0/2 (0,0 %). Échéance +30 min non atteinte. Même prompt de 0001 à 0300, même fournisseur/modèle/high, sessions dédiées archivées sans outil. TTMT : premier delta SSE de sortie mesurable, pouvant inclure le raisonnement ; débit : tokens de sortie natifs / intervalle premier–dernier delta SSE. Min/max TTMT : 2.274/2.301 s ; min/max débit : 356.168/466.714.

Surcharge de télémétrie distincte : 1828 tokens de sortie et 1851 de raisonnement ; durée calendaire cumulée des sondes 9.243 s ; coût natif déclaré 0.003188326. Le benchmark PLLM reste séparé : quotas frais avant génération, succès au palier 2048, TTFT visible 5,6909 s et débit global raisonnement/réponse 2484,956 tokens/s ; ce débit n’est pas directement comparable aux sondes de sortie.

## 2. Types de messages et d’outils

| Rôle de message | Nombre | Part |
|---|---:|---:|
| user | 45 | 32.4 % |
| assistant | 94 | 67.6 % |
| Total | 139 | 100,0 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| text | 127 | 25.9 % |
| step-start | 94 | 19.1 % |
| reasoning | 95 | 19.3 % |
| tool | 82 | 16.7 % |
| step-finish | 93 | 18.9 % |
| Total | 491 | 100,0 % |

| Fin de réponse assistant | Nombre | Part |
|---|---:|---:|
| tool-calls | 53 | 56.4 % |
| stop | 40 | 42.6 % |
| inconnu | 1 | 1.1 % |
| Total | 94 | 100,0 % |

| Type d’outil | Total | Part | Terminés et taux | Refus et taux | Erreurs et taux |
|---|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 4 | 4.9 % | 4 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 19 | 23.2 % | 18 (94.7 %) | 0 (0,0 %) | 1 (5.3 %) |
| bash | 9 | 11.0 % | 9 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| read | 28 | 34.1 % | 28 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| glob | 7 | 8.5 % | 7 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| grep | 3 | 3.7 % | 3 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 | 1.2 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 | 1.2 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| write | 8 | 9.8 % | 8 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 | 1.2 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 1.2 % | 1 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| Total | 82 | 100,0 % | 81 (98.8 %) | 0 (0,0 %) | 1 (1.2 %) |

L’agrégat CAB depuis réservation compte 81 outils, contre 82 dans l’historique intégral : le premier broker_readiness précède le contexte 341. De même, CAB observe 44 messages user et 92 assistant, contre 45 et 94 dans l’historique intégral. Ces périmètres ne sont pas additionnés. Les décisions/once proviennent du registre CAB ; les statuts d’outils ne sont pas des décisions.

## 3. Fichiers modifiés

Tentatives d’écriture natives avant rapport : 8, toutes approuvées et terminées, aucun refus ni erreur d’outil. Six fichiers distincts. Une écriture achevée ne garantit pas l’identité du contenu : le littéral divergent du test a été détecté puis corrigé avant les tests.

| Chemin absolu intégral | Écritures | Part | Approuvées/terminées | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-criticality-vocabulary-v1/.openspec.yaml | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-criticality-vocabulary-v1/proposal.md | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-criticality-vocabulary-v1/design.md | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-capability-criticality-vocabulary-v1/tasks.md | 2 | 25.0 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/capability_criticality.py | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_capability_criticality.py | 2 | 25.0 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 8 | 100,0 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Les quatre artefacts OpenSpec ont été déplacés par l’archivage natif vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-capability-criticality-vocabulary-v1/ ; les deux fichiers Python restent à leur emplacement. Le présent rapport est une écriture supplémentaire après la photographie, sous mandat distinct. Les bytecodes régénérables issus des deux compilations sont des artefacts de test, non des sources analysées. Les empreintes des cadrages, canons component-model/capabilities, façade Kernel, manifest/models.py, capabilities.py et lifecycle/availability.py sont inchangées.

## 4. Commandes

| Famille | Occurrences | Part | Exécutées | Refus | Erreurs d’outil |
|---|---:|---:|---:|---:|---:|
| Prévol inoffensif | 1 | 11.1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Compilation Python | 2 | 22.2 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Tests unittest | 1 | 11.1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Validation OpenSpec | 4 | 44.4 % | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Archivage OpenSpec | 1 | 11.1 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 9 | 100,0 % | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

| Commande exécutée, libellé limité à 100 caractères | Nombre | Part |
|---|---:|---:|
| `/usr/bin/true` | 1 | 11.1 % |
| `/home/devops/.local/npm/bin/openspec validate add-initial-capability-criticality-vocabulary-v1 --st…` | 1 | 11.1 % |
| `/home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/capability_criticality.py` | 1 | 11.1 % |
| `/home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_capability_criticality.py` | 1 | 11.1 % |
| `/usr/bin/env PYTHONPATH=src:tests/unit PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/…` | 1 | 11.1 % |
| `/home/devops/.local/npm/bin/openspec validate --all` | 1 | 11.1 % |
| `/home/devops/.local/npm/bin/openspec validate --all --strict` | 2 | 22.2 % |
| `/home/devops/.local/npm/bin/openspec archive add-initial-capability-criticality-vocabulary-v1 --ski…` | 1 | 11.1 % |
| Total | 9 | 100,0 % |

Commandes refusées : aucune (0/9, 0,0 %). La commande de validation initialement approuvée puis annulée en attente de ressource n’a pas été exécutée et n’est pas ajoutée aux 9 occurrences. Résultats : deux compilations code 0 ; 97 tests/97 réussis (100,0 %) ; ciblé strict code 0 ; global standard 187/187 code 0 ; strict avant archive 185/187 et après archive 184/186, code 1, quatre avertissements de longueur préexistants (bulk-operations exigences 6/10/13 ; identity-assurance exigence 4), zéro ERROR. Aucune réussite stricte globale revendiquée.

## 5. Accès web

| Domaine agent de codage | Total | Approuvés | Refusés | Erreurs |
|---|---:|---:|---:|---:|
| Outils webfetch/websearch | 0 | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil de navigation ni URL visitée par l’agent de codage ; parts et taux N/A car dénominateur nul. Les transports techniques autorisés de l’orchestrateur sont distincts : HTTPS fournisseur pour PLLM et HTTP loopback OpenCode/CAB. Points d’accès effectivement utilisés : https://opencode.ai/zen/go/v1/usage ; https://opencode.ai/zen/go/v1/models ; https://opencode.ai/zen/go/v1/responses ; http://127.0.0.1:4096 ; http://127.0.0.1:8788 ; http://127.0.0.1:8789 . Aucune URL refusée connue. Nombre exhaustif des requêtes de transport : N/A, non instrumenté ; ne pas les compter comme visites web de l’agent.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — borne de collecte conservée | 18/10/2026 21:09:57 CEST |
| Fin — après archivage et sonde finale | 18/10/2026 21:28:24 CEST |
| Durée globale, pauses et attentes incluses | 00 h 18 min 26 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé consigné | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de collecte | 18/10/2026 21:09:57 CEST | 26 % | 25/10/2026 01:23:28 CEST |
| Après — après archivage et sonde finale | 18/10/2026 21:28:24 CEST | 33 % | 25/10/2026 01:23:28 CEST |
| Différence après − avant | — | +7 points de pourcentage | — |

Source : deux lectures natives get_usage_limits, quota codex, fenêtre 10080 min, même compte et même resetsAt=1792884208. Les horodatages sont ceux de consignation des lectures dans le checkpoint. Quota partagé avec les autres chats : la variation 26 % → 33 % couvre l’intervalle et ne peut pas être attribuée exclusivement à CISMP7. La rédaction ultérieure du rapport est exclue.

| Domaine natif | Total | Part globale | Terminés et taux | Refus et taux | Erreurs et taux |
|---|---:|---:|---:|---:|---:|
| Écritures de fichiers | 8 | 9.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 9 | 11.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 65 | 79.3 % | 64 (98.5 %) | 0 (0.0 %) | 1 (1.5 %) |
| Total | 82 | 100,0 % | 81 (98,8 %) | 0 (0,0 %) | 1 (1,2 %) |

Les 65 autres outils regroupent 27 MCP et 38 lectures/recherches. Total recoupé : 8 + 9 + 0 + 65 = 82. Les décisions CAB (18) et once (17) sont des mesures de contrôle distinctes, sans ajout au total des outils.

Coordination CAB observée : attente de ressources 43,240 s ; détention partagée 479,229 s ; effet natif émis en suivi 4,012 s ; aucun gel global. Ces durées peuvent se recouvrir et ne mesurent pas du codage productif. Échecs HTTP filtrés : resource-revision-stale 3, native-validation-not-correlated 1, publication-written-resources-required 1 ; ce sont des incidents techniques d’admission/publication, pas des refus de permission. La première demande non admise a été annulée via MCP sans effet ; le premier accès de validation trop large a été annulé avant exécution ; le littéral divergent du test a été corrigé sous mandat neuf ; la publication a été reprise après ajout de la ressource logique de tests dans la protection de ses preuves, sans rejouer l’archive.

Livraison : CapabilityCriticality(Enum) pur, deux valeurs REQUIRED/OPTIONAL ; deux compilations et 97 tests réussis ; archivage natif code 0 et identité des six fichiers vérifiée ; validation ciblée stricte et globale standard conformes, limite stricte globale explicitée ci-dessus. Publication CAB durable : cismp7-publish-eead616961e14ee8beda2e8cd3f2e06f, référence 44. À cette photographie, le rapport reste à écrire/vérifier puis le gate, le désarmement et la libération ciblée restent à prouver. Aucun nouveau change ne doit suivre.

PostgreSQL, frontend et migrations : sans objet pour ce vocabulaire pur. Git : non inspecté, aucun commit/push mandaté. Secrets : usage PLLM limité au processus sécurisé ; aucune valeur affichée, transmise au modèle ou ajoutée aux sources dans les opérations examinées. OpenCode, broker et services communs sont conservés pour les RUN voisins. Cycle global Pixs incomplet : cycle_global_complete=false.
