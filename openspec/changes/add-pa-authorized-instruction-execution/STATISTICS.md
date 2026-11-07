# STATISTICS — add-pa-authorized-instruction-execution

Statut exact : change ouvert — dépendances manquantes — archivage en attente.
Référence bilan : [BLOCKERS](./BLOCKERS.md).
Checkpoint : /home/devops/datas/pixs/output/cismp/cismp4-pixs-01a175620d7b/state.json.
Fin de collecte : 2026-10-30T05:50:42.093Z. Fin du change et archivage : EN ATTENTE.
Périmètre : DEPUIS DÉBUT DU CHANGE : origine documentaire 2026-10-17, préparation GSCM1 du 2026-10-22 source output/gscm/GSCM1-20261022T152916Z/state.json, sessions métier ses_e87d23865ffeFkRjcCoO2MBd7e + ses_e87d0b034ffeyZLRL5NsZPb5DJ + ses_e8734b85bffec3uzdnITauY6s7 sur générations 1255 + 1369, pause du 2026-10-29, reprise du 2026-10-30. Déduplication : message.info.id et callID natifs uniques, requestId pour demandes, chaque session métier une seule fois. C14/CISMP4 autre change exclu. Rapport arrêté à la coupure, contrôles effectifs dans checkpoint.

Origine du 17/10 déclarée sans heure ni journal d'activité attribuable ; GSCM22 prouve 1 édition tasks partagée sans coût, tokens ou durée ventilables PA04. Les 350 messages, 172 outils et 208 usages sont les cumuls des traces observées des 3 sessions natives depuis le 26/10 jusqu'à la coupure, non une exhaustivité depuis le 17 ; les mesures initiales absentes restent N/A et ne valent pas zéro. TTMT, version et service absents des codeurs et de l'orchestrateur restent N/A motivés.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---:|---:|---:|---:|
| opencode-go/muse-spark-1.3-contributor | N/A | opencode-go | high | N/A | N/A | N/A |
| opencode-go/muse-spark-1.3-contributor | N/A | opencode-go | medium | 1576.0 ms | 237.7 tokens/s | N/A |
| N/A (GSCM non identifiable, encodage non ventilé) | N/A (faute version d'API) | N/A | N/A | N/A | N/A | N/A (sans mesure de génération ; durée d'outils/calendaire non assimilée) |

Sondes medium seules : 2052, 1031, 1645 ms et 210.8, 276.4, 225.9 tokens/s. Moyennes arithmétiques hors production, non durées de service.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---:|---:|---:|---:|
| Codex | N/A | OpenAI | N/A | N/A | N/A | N/A |

Orchestration sans télémétrie fournie. Coût natif observé non converti en euros.

## 1. Statistiques générales et décisions

Durée calendaire inclut pauses et attentes.

| Modèle | Messages usage (part) | Input | Output | Reasoning | CacheRead | CacheWrite | Coût natif |
|---|---:|---:|---:|---:|---:|---:|---:|
| high | 154 (74.0 %) | 3704723 | 121496 | 58236 | 57683668 | 0 | 0.521786036 |
| medium | 54 (26.0 %) | 4432203 | 21678 | 4531 | 27013138 | 0 | 0 |
| Total | 208 (100 %) | 8136926 | 143174 | 62767 | 84696806 | 0 | 0.521786036 |

Zéros natifs conservés, unité du coût non précisée sans conversion en euros. Reasoning non additionné aux outputs sans garantie. Sondes 3 valides : début 2026-10-30T04:39:30.631Z, post-maintenance 2026-10-30T05:41:38.390Z, fin 2026-10-30T05:48:51.336Z, même prompt SHA 9d5b8fae… 2568 octets, 1947 tokens de surcharge hors prod ; échéance +30 2026-10-30T05:09:30.631Z non réalisée, non rétrocréée. TTMT moyen 1576 ms, débit moyen 237.7. Version N/A non déduite.

| Messages cumulés 350 (100 %) | Nombre | Part |
|---|---:|---:|
| user | 119 | 34.0 % |
| assistant | 208 | 59.4 % |
| system | 6 | 1.7 % |
| model-switched | 1 | 0.3 % |
| idle | 16 | 4.6 % |
| Total | 350 | 100 % |

Incrément reprise seule : 92 messages (100 %). Unités locales 26/10 non rejouées.

| Décisions CAB à la coupure | Nombre | Part |
|---|---:|---:|
| approved | 31 | 100.0 % |
| rejected | 0 | 0.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| once native | 29 | 93.5 % des approved |
| Total décisions | 31 | 100 % |

Vues CAB et natives recouvrantes, non additionnées. Tâches : 1 [x], 2-10 [ ]. Avancement 10 % documentaire seul. Tests 32 historiques (13+19) + 2 syntaxes 26/10 non rejoués. Strict ciblé historique exit 0, contrôle courant après rapport à faire. Git aucun, archivage aucun, livraison aucune.

## 2. Types de messages et d'outils

| Parties 732 (100 %) | Nombre | Part |
|---|---:|---:|
| text | 299 | 40.8 % |
| reasoning | 261 | 35.7 % |
| tool | 172 | 23.5 % |
| Total | 732 | 100 % |

Parts distinctes des messages. Finishes assistant 208 : tool-calls 122 (58.7 %), stop 84 (40.4 %), error 1 (0.5 %), unknown 1 (0.5 %).


| Type outil natif (part des 172) | Complétés | Refus natif | Erreur technique | Total ligne |
|---|---:|---:|---:|---:|
| read | 52 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 52 (30.2 %) |
| cgpt-validation_broker_readiness | 37 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 37 (21.5 %) |
| cgpt-validation_broker_health | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (0.6 %) |
| cgpt-validation_broker_remediation_registry | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (0.6 %) |
| cgpt-validation_broker_auto_remediation_policy | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (0.6 %) |
| cgpt-validation_list_pending | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2 (1.2 %) |
| bash | 26 (96.3 %) | 0 (0.0 %) | 1 (3.7 %) | 27 (15.7 %) |
| cgpt-validation_request_validation | 28 (87.5 %) | 0 (0.0 %) | 4 (12.5 %) | 32 (18.6 %) |
| cgpt-validation_poll_approval | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) | 3 (1.7 %) |
| cab_codemode_discovery | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 2 (1.2 %) |
| execute | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (0.6 %) |
| glob | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 4 (2.3 %) |
| grep | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) | 5 (2.9 %) |
| edit | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) | 4 (2.3 %) |
| Total | 165 (95.9 %) | 1 (0.6 %) | 6 (3.5 %) | 172 (100 %) |

Détail 6 techniques : request_validation 3 timeouts + 1 retry -32602, poll_approval 1 timeout, bash 1 aborted. Incrément reprise 75 = 74 completed + 1 refus.

Détail erreurs techniques 6 : request_validation 4 (3 timeouts + 1 retry -32602), poll_approval 1 timeout, bash 1 aborted. Refus explicite 1 : edit Map declined. Incrément reprise : 75 outils (100 %) = 74 completed (98.7 %) + 1 refus (1.3 %) + 0 technique.

## 3. Fichiers modifiés

Tentatives par ligne, dénominateur = nombre de demandes RESSOURCE de la ligne, toujours positif. Zéro numérateur donne 0.0 %, N/A seulement si dénominateur 0 (aucun ici).

| Fichier absolu | Demandes approved / rejected / unknown | Effets completed / refus / tech / SANS OUTIL |
|---|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/design.md | 1 (50.0 %) / 0 (0.0 %) / 1 (50.0 %) | 2 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/tasks.md | 5 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 5 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/.openspec.yaml | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/proposal.md | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/specs | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/contracts.md | 2 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 2 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/specs/pixs-agent/spec.md | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/agent/pa04_service_catalog.py | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_pa04_service_catalog.py | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/agent/__pycache__ | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/__pycache__ | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-pa-authorized-instruction-execution/BLOCKERS.md | 2 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 2 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) / 0 (0.0 %) |
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | 3 (100.0 %) / 0 (0.0 %) / 0 (0.0 %) | 1 (33.3 %) / 1 (33.3 %) / 0 (0.0 %) / 1 (33.3 %) |
| Total 22 demandes | 21 (95.5 %) / 0 (0.0 %) / 1 (4.5 %) | 20 (90.9 %) / 1 (4.5 %) / 0 (0.0 %) / 1 (4.5 %) |

Dirs ressources recouvrantes : specs, src/pixs/agent/__pycache__, tests/unit/__pycache__ ; elles ne comptent pas des fichiers physiques. Tasks : 5 effets natifs PLUS 1 écriture GSCM22 hors natifs, sans double compte. Design unknown = trace MCP individuelle unknown motivée (req-fa189fe98ce2414c902179fab6c218d8 decision null), mandats et effet historiques conservés. Map : 3 approved vers 1 effet réussi + 1 refus natif + 1 STALE sans outil.

## 4. Commandes

27 commandes exactes : 26 completed (25 exit0 + 1 exit1) + 1 aborted. Exit1 = outil completed mais contrôle échoué.

| Famille | Total | Completed | Exit0 | Exit1 | Aborted | Part des 27 |
|---|---:|---:|---:|---:|---:|---:|
| python écriture unitaire | 15 | 15 (100.0 %) | 15 | 0 | 0 | 55.6 % |
| true | 4 | 4 (100.0 %) | 4 | 0 | 0 | 14.8 % |
| OpenSpec ciblé | 4 | 4 (100.0 %) | 3 | 1 | 0 | 14.8 % |
| py_compile | 2 | 2 (100.0 %) | 2 | 0 | 0 | 7.4 % |
| unittest | 1 | 1 (100.0 %) | 1 | 0 | 0 | 3.7 % |
| curl interrompu | 1 | 0 (0.0 %) | 0 | 0 | 1 | 3.7 % |
| Total | 27 | 26 (96.3 %) | 25 | 1 | 1 | 100 % |

Libellés limités à 100 caractères. Commandes refusées : aucune (0 dans traces). 1 commande aborted technique sans preuve de visite. Contrôles globaux/produit non exécutés ; 32 tests historiques structure locale seulement. Aucune famille ajoutée.

## 5. Accès web

Aucun web externe natif observé. URLs des documents non prises comme visitées.

| Accès web | Nombre | Part |
|---|---:|---:|
| Approuvés visités | 0 | N/A |
| Refusés | 0 | N/A |
| Erreurs | 0 | N/A |
| Total | 0 | N/A |

Curl loopback aborted = mention interne, non web externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | N/A (origine 2026-10-17 heure inconnue, durée globale N/A) |
| Fin — fin de collecte avant rédaction | 2026-10-30T05:50:42.093Z |
| Reprise depuis resumeStart | 2026-10-30T04:36:39.240Z, écoulé 4442853 ms soit 01 h 14 min 02 s |
| Intervalle disponible natif | 2026-10-26T12:27:11.899Z → 2026-10-30T05:50:42.093Z soit 89 h 23 min 30.194 s (pas durée entière du change) |

Rapport arrêté à la coupure.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Historique 26/10 autre fenêtre | 2026-10-26T12:33:27.656643+00:00 | 41 % | 2026-11-02T06:01:55.000Z |
| Reprise seule avant | N/A (heure initiale non consignée) | 62 % | 2026-11-04T06:45:53.000Z |
| Après — fin de collecte avant rédaction | 2026-10-30T05:49:53.521Z | 73 % | 2026-11-04T06:45:53.000Z |
| Différence reprise (73−62) | — | 11 points partagés non exclusifs | même compte/fenêtre |
| Différence cumulée 41→73 | — | N/A (fenêtres/resets différents) | — |

Quotas partagés, variation possiblement multitâche.

| Domaine mutuellement exclusif (total 172, 100 %) | Total (part globale) | Completed (taux ligne) | Refusé (taux ligne) | Technique (taux ligne) |
|---|---:|---:|---:|---:|
| Fichiers (read/glob/grep/edit) | 65 (37.8 %) | 64 (98.5 %) | 1 (1.5 %) | 0 (0.0 %) |
| Commandes | 27 (15.7 %) | 26 (96.3 %) | 0 (0.0 %) | 1 (3.7 %) |
| Web externe | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| CAB MCP | 77 (44.8 %) | 72 (93.5 %) | 0 (0.0 %) | 5 (6.5 %) |
| Autres (discovery/execute) | 3 (1.7 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 172 (100 %) | 165 (95.9 %) | 1 (0.6 %) | 6 (3.5 %) |

HTTP failures : gen1255 total 9 (evidence-references-required 1, run-not-quiescent 2, run-pause 1, native-validation-not-correlated 3, decision-run-divergent 2) ; gen1369 total 3 (run-not-quiescent 1, validation-request-invalid 1, run-transition-in-flight 1) ; aucun REFUS déduit. Coût natif 0.521786036 non converti. État : tests non rejoués, archivage aucun, Git aucun, livraison aucune, secrets aucun.
