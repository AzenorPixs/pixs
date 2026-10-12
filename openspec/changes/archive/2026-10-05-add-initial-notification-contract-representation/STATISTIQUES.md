# STATISTIQUES — add-initial-notification-contract-representation

RUN : cismp-pixs-20261005-2654fe47 ; archive : openspec/changes/archive/2026-10-05-add-initial-notification-contract-representation.
Intervalle OpenCode : 2026-10-05T18:51:41.927000+00:00 → 2026-10-05T20:09:13.292809+00:00 (UTC). Les trois sessions de reprise sont agrégées ; les sondes et la rédaction de ce rapport sont exclues des compteurs de production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Qwen3.8 Flash | N/A | opencode-go | xhigh | 1.9058 s | 93.9392 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (GPT-6) | N/A | OpenAI | N/A | N/A | N/A | N/A |

Versions exactes et temps de génération actifs absents de la télémétrie. Aucun pourcentage de service ne peut être calculé : dénominateur incomplet. Les métriques du codeur sont les moyennes arithmétiques des seules sondes dédiées valides ; aucune sonde de l'orchestrateur.

## 1. Statistiques générales et décisions

| Mesure | Nombre | Part / résultat |
|---|---|---|
| Messages OpenCode | 163 | 100 % |
| Appels d'outils | 107 | 100 % |
| Approuvés et exécutés / lectures autorisées | 99 | 92.5 % |
| Refus explicites d'outil | 0 | 0.0 % |
| Erreurs techniques | 8 | 7.5 % |
| Décisions CAB uniques APPROVED | 26 | 96.3 % |
| Décisions CAB uniques REJECTED | 1 | 3.7 % |
| Total décisions CAB | 27 | 100 % |
| Tests exécutés réussis | 91 | 100 % ; 16 unitaires + 1 intégration + 74 régressions |
| Compilations nouvelles réussies | 3 | 100 % |
| Stricts pré/post réussis | 6 | 100 % |
| Archivages réussis | 1 | 100 % |

Convention : un outil terminé avec succès est autorisé automatiquement ou explicitement ; cela ne prouve pas une permission native manuelle. Un timeout MCP est une erreur technique, même lorsque son opération a ensuite réussi par polling corrélé. Un SyntaxError du lanceur a précédé tout test ; aucun test n'a alors démarré. Le mandat modifié run-unit-02 a été refusé avant exécution.

Incident de pilotage : le champ API tools a temporairement remplacé ASK par allow. Les écritures avaient chacune une décision MCP explicite et ont été relues ; leur consommation native n'est pas prouvée. Le champ a été retiré, les anciennes sessions gelées, une nouvelle session ASK créée et le garde vérifié. Les tests, stricts finaux, cochage et archive ont des événements natifs ASK puis once corrélés. Aucun effet source hors périmètre observé.

| Compteur natif de production | Valeur |
|---|---|
| input | 762 |
| output | 59819 |
| reasoning | 0 |
| cache_read | 11039246 |
| cache_write | 773924 |

Coût monétaire et compactions natives : N/A (pas de mesure exploitable). Les compteurs de tokens/caches sont ceux d'OpenCode ; aucune conversion depuis les quotas.

| Sonde | Envoi UTC | TTMT (s) | Tokens sortie | Débit (tokens/s) | État |
|---|---|---|---|---|---|
| début | 2026-10-05T18:47:02.277344+00:00 | 1.8942 | 522 | 80.0022 | success |
| +30 min | 2026-10-05T19:17:54.309149+00:00 | 1.8473 | 771 | 101.6295 | success |
| +60 min | 2026-10-05T19:47:57.553961+00:00 | 2.5471 | 861 | 99.6678 | success |
| fin | 2026-10-05T20:09:05.997894+00:00 | 1.3346 | 563 | 94.4572 | success |

Sondes prévues/réussies : 4/4 ; échouées/manquées : 0/0. Relèves +30/+60 min exécutées avec retards observés de 52.032 s et 55.277 s, sans reconstruction rétroactive. TTMT min/max : 1.3346/2.5471 s ; débit min/max : 80.0022/101.6295. Surcharge séparée : 51229 tokens natifs dont 2717 tokens de sortie ; coût N/A. Prompt constant de 128 lignes fixes, quatre sessions dédiées supprimées, aucun outil invoqué. Les deux premières sondes conservent délais monotones, les suivantes aussi les horodatages des deltas SSE.

## 2. Types de messages et d'outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 35 | 21.5 % |
| assistant | 128 | 78.5 % |
| Total | 163 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 92 | 15.8 % |
| step-start | 128 | 22.0 % |
| reasoning | 128 | 22.0 % |
| tool | 107 | 18.4 % |
| step-finish | 127 | 21.8 % |
| Total | 582 | 100 % |

| Outil | Total | Part | Succès | Refus | Erreurs | Taux succès | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| read | 31 | 29.0 % | 30 | 0 | 1 | 96.8 % | 0.0 % | 3.2 % |
| cgpt-validation_request_validation | 27 | 25.2 % | 21 | 0 | 6 | 77.8 % | 0.0 % | 22.2 % |
| write | 8 | 7.5 % | 8 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| bash | 16 | 15.0 % | 15 | 0 | 1 | 93.8 % | 0.0 % | 6.2 % |
| grep | 2 | 1.9 % | 2 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_get_approval | 6 | 5.6 % | 6 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| edit | 2 | 1.9 % | 2 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_broker_readiness | 8 | 7.5 % | 8 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| glob | 2 | 1.9 % | 2 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_list_pending | 2 | 1.9 % | 2 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_poll_approval | 3 | 2.8 % | 3 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| Total | 107 | 100 % | 99 | 0 | 8 | 92.5 % | 0.0 % | 7.5 % |

Terminaisons natives des 128 réponses : tool-calls=93 (72.7 %), stop=34 (26.6 %), interrompu/non renseigné=1 (0.8 %). Compactions natives : aucune réussite coordonnée prouvée. Les reprises serveur et de session sont conservées dans le checkpoint. Les décisions sont regroupées séparément ci-dessus, sans confondre REJECTED CAB et résultat d'une lecture get_approval réussie.

## 3. Fichiers modifiés

| Chemin absolu (avant archive) | Tentatives | Part | Succès | Refus | Erreurs | Taux succès |
|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/.openspec.yaml | 1 | 10.0 % | 1 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/proposal.md | 1 | 10.0 % | 1 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/design.md | 1 | 10.0 % | 1 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/tasks.md | 2 | 20.0 % | 2 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-contract-representation/specs/notifications/spec.md | 1 | 10.0 % | 1 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/notification_contract.py | 1 | 10.0 % | 1 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/tests/unit/test_notification_contract.py | 1 | 10.0 % | 1 | 0 | 0 | 100.0 % |
| /home/devops/datas/pixs/tests/integration/test_notification_contract_integration.py | 2 | 20.0 % | 2 | 0 | 0 | 100.0 % |
| Total | 10 | 100 % | 10 | 0 | 0 | 100 % |

Il s'agit de tentatives d'édition. Les cinq artefacts OpenSpec ont été déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-05-add-initial-notification-contract-representation ; trois fichiers Python nouveaux restent à leur emplacement. Un cochage et une correction du marqueur concernent respectivement tasks.md et le test d'intégration. Les 96 références sont inchangées ; les huit fichiers autorisés ont leurs empreintes vérifiées, UTF-8/LF. STATISTIQUES.md et le checkpoint sont hors intervalle de production de ce tableau.

## 4. Commandes

| Famille | Total | Part | Succès | Refus | Erreurs | Taux succès |
|---|---|---|---|---|---|---|
| OpenSpec | 7 | 43.8 % | 7 | 0 | 0 | 100.0 % |
| Compilation Python | 3 | 18.8 % | 3 | 0 | 0 | 100.0 % |
| Tests Python | 4 | 25.0 % | 3 | 0 | 1 | 75.0 % |
| Prévol CAB | 2 | 12.5 % | 2 | 0 | 0 | 100.0 % |
| Total | 16 | 100 % | 15 | 0 | 1 | 93.8 % |

| Commande refusée avant exécution (≤100 caractères) | Nombre | Part des refus |
|---|---|---|
| /home/devops/python/current/bin/python3 -I -B -c '(__import__("sys").path.insert(0, "."), __impor... | 1 | 100.0 % |

La commande refusée avait une expression de tuple ajoutée. Aucun Git inspecté/exécuté. La commande de lanceur avec LF transformés en échappements a échoué avant la découverte des tests ; elle n'est pas comptée comme refus ni comme test échoué.

## 5. Accès web

| Domaine | Total | Approuvés | Refusés | Erreurs | Taux |
|---|---|---|---|---|---|
| Outils web du codeur | 0 | 0 | 0 | 0 | N/A — dénominateur zéro |

Aucune URL de navigation visitée ou refusée par un outil web. Hors agrégat de navigation : inférences/sondes via https://opencode.ai/zen/go/v1/messages et contrôles de quotas autorisés via https://opencode.ai/zen/go/v1/usage. Ces processus utilisent les secrets hors modèle et sorties ; leur comptage/coût global n'est pas reconstitué.

## 6. Synthèse globale

| Durée de session de codage | Valeur |
|---|---|
| Début | 2026-10-05T18:51:41.927000+00:00 |
| Fin — après archivage et sonde finale | 2026-10-05T20:09:13.292809+00:00 |
| Durée globale (pauses/attentes incluses) | 01 h 17 min 31 s |

| Quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

L'outil natif mcp__codex_app__get_usage_limits n'est pas exposé : aucun relevé remplacé par une ancienne valeur ou un quota OpenCode Go. Les quotas Codex seraient partagés par le compte, sans attribution exclusive ni conversion en tokens/coût.

| Domaine | Total | Part globale | Succès | Refus | Erreurs | Taux succès | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Fichiers | 10 | 9.3 % | 10 | 0 | 0 | 100 % | 0 % | 0 % |
| Commandes | 16 | 15.0 % | 15 | 0 | 1 | 93.8 % | 0 % | 6.2 % |
| Web | 0 | 0.0 % | 0 | 0 | 0 | N/A | N/A | N/A |
| Autres outils | 81 | 75.7 % | 74 | 0 | 7 | 91.4 % | 0 % | 8.6 % |
| Global | 107 | 100 % | 99 | 0 | 8 | 92.5 % | 0 % | 7.5 % |

Bilan : 91 exécutions de tests réussies, trois compilations et six stricts réussis, archive unique vérifiée avec +0/~0/-0/→0 canonique. La représentation reste interne et partielle ; envoi, persistance et préférences effectives ne sont pas livrés. PostgreSQL et frontend sans objet pour cette unité. Git non inspecté, aucun commit/push. Aucune donnée sensible lue par le codeur observée ; aucune valeur de secret publiée. Les statistiques d'outils de l'orchestrateur sont N/A, hors agrégat OpenCode. La publication a été différée par l'ancienne règle de compactage puis reprise après correction du protocole CAB 0.86.6. Cette rédaction et les prévols de reprise sont hors intervalle de production ; aucune mesure finale n'est refaite rétroactivement. Le RUN parent poursuit son cycle ; cette archive n'est pas l'achèvement de toutes les exigences Pixs.
