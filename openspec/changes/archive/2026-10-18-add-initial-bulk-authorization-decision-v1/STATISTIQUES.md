# Statistiques — CISMP6 — add-initial-bulk-authorization-decision-v1

RUN `cismp6-pixs-4e81b7a045ac4e02`, contexte CAB 340, session OpenCode `ses_eaf92f729ffekNQRsCUyCZVGQt`, projet `/home/devops/datas/pixs`. Rapport par archive, fondé sur l’historique HTTP natif de cette seule session, le JSON et le brouillon `/runs/cismp6-pixs-4e81b7a045ac4e02/statistics`, les preuves du checkpoint et les deux sondes dédiées.

Fenêtre de codage : 18/10/2026 21:09:55 Europe/Paris à 18/10/2026 21:39:55 Europe/Paris. Instantané des messages/outils arrêté à 18/10/2026 21:39:31 Europe/Paris, avant la sonde finale. Le rapport, sa propre écriture et les contrôles de clôture sont hors de cette fenêtre de production ; leurs preuves restent dans le checkpoint. Les sondes sont comptées séparément.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte du modèle absente | OpenCode Go (`opencode-go`) | high | 0,845 s (1 sonde valide) | 399,745 (global, 1 sonde valide) | N/A — durée active complète non mesurée |

Agent natif OpenCode 1.19.3, modèle et variante vérifiés dans les métadonnées. La version du modèle n’est pas déduite de son nom. Les métriques de sondes ne sont pas des mesures de toute la production.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex (famille GPT-6) | N/A — identité exacte non exposée | OpenAI | N/A — télémétrie absente | N/A — non sondé | N/A — non sondé | N/A — durée active non mesurée |

Aucun orchestrateur sondé. Dénominateur du temps de service cumulé : N/A, faute de durées actives complètes des deux agents ; la durée calendaire, les outils, pauses et permissions ne sont pas assimilés à la génération du modèle.

## 1. Statistiques générales et décisions

Convention : « approuvé et exécuté » désigne un appel natif terminé, autorisé par le mandat ou les règles de lecture ; cela ne prouve pas une approbation humaine manuelle. Un appel MCP terminé peut porter une décision métier REJECTED. Un refus est une permission native explicitement rejetée ; un timeout, une interruption ou une erreur MCP est une erreur technique. Un outil Bash terminé avec code 1 reste distinct d’un refus et d’une réussite fonctionnelle.

| Résultat natif | Nombre | Part |
| --- | --- | --- |
| Approuvé et exécuté | 72 | 92,3 % |
| Refus de permission | 2 | 2,6 % |
| Erreur technique | 4 | 5,1 % |
| En cours | 0 | 0,0 % |
| Total | 78 | 100 % |

| Décision CAB (depuis réservation) | Nombre | Part |
| --- | --- | --- |
| approved | 20 | 95,2 % |
| rejected | 1 | 4,8 % |
| needs_clarification | 0 | 0,0 % |
| pending | 0 | 0,0 % |
| Total | 21 | 100 % |

Permissions `once` prouvées : 18, soit 18/18 effets natifs terminés soumis à permission (100 %). Deux autres permissions ont été refusées avant effet. Les 20 décisions approved ne constituent pas 20 exécutions.

Incidents conservés : une demande anticipée et une validation sur révision périmée annulées nativement sans effet ; un mandat de tests périmé refusé avant Bash ; une édition tasks.md et une archive refusées avant once sur accès STALE ; un objet MCP d’archive incomplet rejeté -32602 avant enregistrement. Aucune écriture hors périmètre ni réutilisation de permission observée. Les quatre erreurs techniques natives comprennent les interruptions/timeouts MCP ; elles ne prouvent pas quatre refus.

| Télémétrie de production native | Valeur |
| --- | --- |
| Tokens d’entrée (hors cache) | 274377 |
| Tokens de réponse | 36008 |
| Tokens de raisonnement | 10488 |
| Tokens de cache lus | 11150469 |
| Tokens de cache écrits | 0 |
| Coût déclaré par OpenCode | 0.059037838 $ |
| Compactions | N/A — aucune preuve native de compaction collectée |

Les tokens et le coût sont les sommes des métadonnées disponibles ; le coût déclaré ne constitue pas une facture. Les dépenses et tokens de l’orchestrateur sont N/A.

PLLM mode 1, modèle imposé et raisonnement high : benchmark réel valide au palier 2 048, TTFT 2,5605 s, débit global de l’évaluateur 4 322,606 tokens/s. Le palier 1 024 est resté non concluant (RuntimeError conservée) ; nouveau contrôle de quota avant 2 048. Quotas fournisseur utilisés au contrôle : rolling 3 %, semaine 69 %, mois 99 %. Le benchmark est séparé des sondes et de la production.

| Sonde dédiée | Envoi UTC | Résultat | TTMT | Tokens/s globaux |
| --- | --- | --- | --- | --- |
| Début | 2026-10-18T19:10:25.779Z | Réponse modèle vérifiée, mesure incomplète | N/A | N/A |
| Fin | 2026-10-18T19:39:31.658Z | Valide, aucun outil | 0,845 s | 399,745 |

Deux relèves prévues : une mesure complète (50,0 %), une incomplète (50,0 %), zéro manquée (0,0 %). La sonde initiale n’a pas capturé son premier événement SSE ; elle est exclue des moyennes sans masquer sa réponse. La sonde finale utilise les horodatages natifs des parties générées et les tokens réels : premier événement à 2026-10-18T19:39:32.503Z, dernier à 2026-10-18T19:39:34.857Z, 941 tokens de réponse et raisonnement. Le débit ne doit pas être comparé comme une mesure identique au débit de réponse seule. La relève +30 min aurait été due le 2026-10-18T19:40:25.779Z, après la fin du codage et la sonde finale : elle est sans objet. Surcharge des deux sondes : 1476 tokens de sortie et raisonnement, 0.002571126 $ déclarés ; exclue de la production. Minimum et maximum des métriques valides égaux à la moyenne (un seul échantillon).

Résultats livrés : trois fichiers Python compilés, 75/75 tests ciblés et régressions réussis (100 %), validations ciblées strictes code 0, standard global avant archive 187/187 code 0. Strict global avant archive : 184/186, code 1 ; après archive : 182/184, code 1. Les quatre warnings de longueur préexistants concernent bulk-operations exigences 6/10/13 et identity-assurance exigence 4 ; zéro ERROR. Les effectifs globaux évoluent avec les archives concurrentes.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 34 | 27,6 % |
| assistant | 89 | 72,4 % |
| Total | 123 | 100 % |

| Type d’outil | Total et part | Approuvé et exécuté (taux) | Refusé (taux) | Erreur technique (taux) |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 3 (3,8 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 24 (30,8 %) | 21 (87,5 %) | 0 (0,0 %) | 3 (12,5 %) |
| bash | 10 (12,8 %) | 9 (90,0 %) | 1 (10,0 %) | 0 (0,0 %) |
| todowrite | 3 (3,8 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 15 (19,2 %) | 15 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| glob | 6 (7,7 %) | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 4 (5,1 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 1 (1,3 %) | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) |
| cgpt-validation_cancel_approval | 2 (2,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 10 (12,8 %) | 9 (90,0 %) | 1 (10,0 %) | 0 (0,0 %) |
| Total | 78 (100 %) | 72 (92,3 %) | 2 (2,6 %) | 4 (5,1 %) |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 116 | 25,2 % |
| step-start | 89 | 19,3 % |
| reasoning | 91 | 19,7 % |
| tool | 78 | 16,9 % |
| step-finish | 87 | 18,9 % |
| Total | 461 | 100 % |

Les résultats de terminaison sont complétés depuis l’historique natif ci-dessus, sans confondre un résultat CAB REJECTED dans un appel MCP réussi et un outil natif refusé. La collecte CAB depuis réservation comptait 77 outils et 121 messages à sa borne, contre 78 outils et 123 messages pour la session HTTP complète : initialisation antérieure à la réservation et bornes de collecte différentes, sans fusion arbitraire des compteurs.

## 3. Fichiers modifiés

Il s’agit de tentatives d’écriture natives, incluant les refus et les chemins historiques avant déplacement. Sept fichiers logiques ont été créés ; quatre artefacts OpenSpec ont ensuite été déplacés dans l’archive par la commande dédiée.

| Chemin absolu de la tentative | Total et part | Approuvées (taux) | Refusées (taux) | En erreur (taux) |
| --- | --- | --- | --- | --- |
| `/home/devops/datas/pixs/openspec/changes/add-initial-bulk-authorization-decision-v1/.openspec.yaml` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/openspec/changes/add-initial-bulk-authorization-decision-v1/proposal.md` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/openspec/changes/add-initial-bulk-authorization-decision-v1/design.md` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/openspec/changes/add-initial-bulk-authorization-decision-v1/tasks.md` | 3 (30,0 %) | 2 (66,7 %) | 1 (33,3 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/src/pixs/backend/bulk_authorization_decision.py` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/tests/unit/test_bulk_authorization_decision.py` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/tests/integration/test_bulk_authorization_decision_integration.py` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-authorization-decision-v1/proposal.md` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 10 (100 %) | 9 (90,0 %) | 1 (10,0 %) | 0 (0,0 %) |

Les chemins OpenSpec initiaux ci-dessus correspondent désormais au dossier `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-authorization-decision-v1`. La seconde écriture de la proposition corrige uniquement les en-têtes structurels attendus par OpenSpec ; l’avertissement observé à l’archivage a été corrigé sans réarchivage. La prose française reste inchangée. Le cache de compilation régénérable est isolé dans `/home/devops/datas/pixs/.cache/cismp6` ; son nombre de fichiers n’est pas inventorié (source générée exclue).

Le présent rapport `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-authorization-decision-v1/STATISTIQUES.md` est édité après la borne de collecte sous mandat distinct, puis vérifié ; son écriture n’est pas ajoutée rétroactivement aux dix tentatives ci-dessus. Les cadrages, le canon bulk-operations, la façade backend et les consommateurs concernés ont conservé leurs empreintes. Aucun autre RUN n’a été modifié.

## 4. Commandes

| Famille | Tentatives | Part |
| --- | --- | --- |
| Prévol sans effet | 1 | 10,0 % |
| Compilation Python | 1 | 10,0 % |
| Tests unittest | 1 | 10,0 % |
| OpenSpec validations | 5 | 50,0 % |
| OpenSpec archivage | 2 | 20,0 % |
| Total | 10 | 100 % |

Les libellés suivants sont limités à 100 caractères, troncature comprise. Les chaînes exactes complètes et les identifiants natifs restent dans le checkpoint.

| Commande | Total et part | Exécutées (taux) | Refusées (taux) | Erreurs (taux) | Codes natifs des exécutions |
| --- | --- | --- | --- | --- | --- |
| `/usr/bin/true` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 : 1 ; 1 : 0 |
| `/home/devops/.local/npm/bin/openspec validate add-initial-bulk-authorization-decision-v1 --strict` | 2 (20,0 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 : 2 ; 1 : 0 |
| `PYTHONPYCACHEPREFIX=/home/devops/datas/pixs/.cache/cismp6 /home/devops/datas/pixs/.venv/bin/python3…` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 : 1 ; 1 : 0 |
| `PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_author…` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 : 1 ; 1 : 0 |
| `/home/devops/.local/npm/bin/openspec validate --all` | 1 (10,0 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 : 1 ; 1 : 0 |
| `/home/devops/.local/npm/bin/openspec validate --all --strict` | 2 (20,0 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 : 0 ; 1 : 2 |
| `/home/devops/.local/npm/bin/openspec archive add-initial-bulk-authorization-decision-v1 --yes --ski…` | 2 (20,0 %) | 1 (50,0 %) | 1 (50,0 %) | 0 (0,0 %) | 0 : 1 ; 1 : 0 |
| Total | 10 (100 %) | 9 (90,0 %) | 1 (10,0 %) | 0 (0,0 %) | 7 codes 0 ; 2 codes 1 |

Commandes refusées regroupées : `/home/devops/.local/npm/bin/openspec archive add-initial-bulk-authorization-decision-v1 --yes --ski…` : une permission native refusée avant once (10,0 % des dix tentatives Bash), aucune archive lors de ce refus. La tentative suivante a archivé une seule fois avec code 0. Le mandat CAB de tests refusé sur base périmée n’a jamais atteint Bash : une décision rejected, soit 4,8 % des 21 décisions CAB. Les demandes annulées ou -32602 ne constituent pas des commandes exécutées.

## 5. Accès web

Aucun outil natif de navigation, webfetch ou websearch dans la session de codage : 0 appel, 0 visite, 0 refus, 0 erreur ; taux N/A, dénominateur nul. Aucune URL refusée ni visite n’est déduite d’une demande sans exécution.

Le prévol fournisseur hors production a vérifié les quotas et une génération HTTPS. URL distinctes effectivement utilisées et autorisées :

| URL (100 caractères maximum) | Statut | Source |
| --- | --- | --- |
| https://opencode.ai/zen/go/v1/usage | Approuvé, réponse quota observée | Évaluateur PLLM mode 1 |
| https://opencode.ai/zen/go/v1/responses | Approuvé, réponse modèle observée | Benchmark imposé Muse high |

Deux URL distinctes vérifiées (100 % approuvées), zéro URL refusée (0,0 %). Nombre détaillé de requêtes réseau N/A : le compteur exhaustif des tentatives n’a pas été exporté, notamment pour le premier palier non concluant. Les API locales OpenCode/CAB sont du pilotage loopback et ne sont pas des visites web externes. Aucun secret n’est reproduit.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début effectif de la collecte persistante | 18/10/2026 21:09:55 Europe/Paris |
| Fin après archivage et sonde finale | 18/10/2026 21:39:55 Europe/Paris |
| Durée globale (pauses et attentes incluses) | 00 h 30 min 00 s (1799.949 s) |

La préparation initiale des protocoles précède cette fenêtre de codage ; la rédaction du rapport et la clôture la suivent. Les durées d’agents concurrents ne sont pas additionnées.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | Horodatage exact non fourni ; consigné 18/10/2026 21:09:55 Europe/Paris | 26 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage de la spécification | 18/10/2026 21:39:55 Europe/Paris | 36 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | 10 points de pourcentage | — |

Source : deux appels natifs mcp__codex_app__get_usage_limits, quota codex, fenêtre 10 080 minutes, même compte et même resetsAt=1792884208 vérifiés. Les valeurs absentes ne valent pas zéro. Le compteur est partagé par le compte : ces 10 points peuvent inclure les autres tâches simultanées et ne sont pas attribués exclusivement à CISMP6. La date de consignation initiale ne prétend pas être un horodatage exact renvoyé par l’API.

| Domaine natif | Nombre et part globale | Approuvé et exécuté (taux) | Refusé (taux) | Erreur technique (taux) |
| --- | --- | --- | --- | --- |
| Fichiers | 10 (12,8 %) | 9 (90,0 %) | 1 (10,0 %) | 0 (0,0 %) |
| Commandes | 10 (12,8 %) | 9 (90,0 %) | 1 (10,0 %) | 0 (0,0 %) |
| Web natif | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 58 (74,4 %) | 54 (93,1 %) | 0 (0,0 %) | 4 (6,9 %) |
| Total global | 78 (100 %) | 72 (92,3 %) | 2 (2,6 %) | 4 (5,1 %) |

Totaux croisés : 10 + 10 + 0 + 58 = 78 ; 72 + 2 + 4 = 78. Le détail par outil et par domaine est identique. Les pourcentages sont arrondis à une décimale, les écarts d’arrondi ne changent pas les effectifs.

Coordination CAB depuis réservation : attente de ressource 303,587 s ; détention partagée 609,870 s ; activité exclusive 0 s ; effets émis 4,665 s. Ces durées peuvent se recouvrir, ne mesurent pas un gain causal et ne sont pas additionnées au temps calendaire. Aucun gel exceptionnel global n’a été demandé par CISMP6.

Publication technique prouvée : reçu `cismp6-publish-19c93a41-4c46-4100-86f5-873df0166abb`, référence 45, version 360. Archivage unique prouvé, tâches complètes, correction des en-têtes vérifiée, tests et compilations réussis. Strict global : échec natif conservé avec seuls avertissements historiques, sans ERROR. Rapport obligatoire avant gate ; le gate, le désarmement, la libération et l’arrêt ciblé sont contrôlés après cette rédaction dans le checkpoint `/home/devops/datas/pixs/output/cismp/cismp6-pixs-4e81b7a045ac4e02/state.json`. Le cycle global Pixs reste incomplet. Aucune inspection ou opération Git, aucune persistance de secret dans les sources ou le rapport ; authentification seulement dans le processus sécurisé du prévol. OpenCode et les services partagés restent disponibles aux autres RUN.
