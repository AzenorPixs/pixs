# STATISTIQUES — add-initial-feature-flag-cohort-rules

Archive : openspec/changes/archive/2026-10-04-add-initial-feature-flag-cohort-rules. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-04T08:48:04.999339+00:00–2026-10-04T10:00:09.460223+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.851 s | 96.178 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

172 messages, 118 outils, durée calendaire 01 h 12 min 04 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 21 | 95.5 % |
| REJECTED | 1 | 4.5 % |
| Total | 22 | 100 % |

Développement : compilation exit 0 ; 14 tests unitaires de la composition étendue, 1 intégration fraîche et 91 régressions, 106/106 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

| Mesure de production | Valeur | Part des tokens SDK |
|---|---:|---:|
| Tokens input | 852 | 0.0 % |
| Tokens output | 88837 | 0.5 % |
| Tokens reasoning | 0 | 0.0 % |
| Tokens total | 16507601 | 100.0 % |
| Tokens cache_read | 15337049 | 92.9 % |
| Tokens cache_write | 1080863 | 6.5 % |
| Coût SDK déclaré | 0.50344657 USD | N/A — coût |
| Compactions OpenCode observées | 1 | N/A — hors tokens |
| Compactions orchestrateur | N/A — compteur absent | N/A — hors tokens |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale règles de cohorte | 2026-10-04T08:48:05.171299+00:00 | 2026-10-04T08:48:08.649425+00:00 | 2026-10-04T08:48:13.550978+00:00 | 3.478 s | 4.902 s | 554 | 113.025/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T09:18:07.534498+00:00 | 2026-10-04T09:18:12.006192+00:00 | 2026-10-04T09:18:16.395762+00:00 | 4.472 s | 4.390 s | 500 | 113.906/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T09:48:09.227678+00:00 | 2026-10-04T09:48:12.506554+00:00 | 2026-10-04T09:48:19.450229+00:00 | 3.279 s | 6.944 s | 522 | 75.176/s | valide |
| finale après archive règles de cohorte | 2026-10-04T09:59:58.269193+00:00 | 2026-10-04T10:00:02.443088+00:00 | 2026-10-04T10:00:09.295015+00:00 | 4.174 s | 6.852 s | 566 | 82.604/s | valide |

Collecte : 4 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 3.279/4.472 s ; débit min/max 75.176/113.906/s. Surcharge : 2142 tokens de sortie, 53582 tokens total SDK, 0.01129354 USD, 38.489 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 144 | 83.7 % |
| user | 28 | 16.3 % |
| Total | 172 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.2 % |
| reasoning | 144 | 23.9 % |
| step-finish | 142 | 23.6 % |
| step-start | 144 | 23.9 % |
| text | 53 | 8.8 % |
| tool | 118 | 19.6 % |
| Total | 602 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 30 | 17.4 % |
| stop | 26 | 15.1 % |
| tool-calls | 116 | 67.4 % |
| Total | 172 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 55 (46.6 %) | 54 (98.2 %) | 0 (0.0 %) | 1 (1.8 %) |
| read | 8 (6.8 %) | 6 (75.0 %) | 0 (0.0 %) | 2 (25.0 %) |
| grep | 2 (1.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 2 (1.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 13 (11.0 %) | 12 (92.3 %) | 0 (0.0 %) | 1 (7.7 %) |
| cgpt-validation_request_validation | 22 (18.6 %) | 21 (95.5 %) | 0 (0.0 %) | 1 (4.5 %) |
| write | 8 (6.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (1.7 %) | 0 (0.0 %) | 0 (0.0 %) | 2 (100.0 %) |
| cgpt-validation_get_approval | 2 (1.7 %) | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| cgpt-validation_broker_health | 2 (1.7 %) | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| cgpt-validation_poll_approval | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 118 (100 %) | 109 (92.4 %) | 0 (0.0 %) | 9 (7.6 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-rules/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-rules/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-rules/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-rules/specs/feature-flags/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-rules/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flag_cohorts.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_cohorts.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_cohorts_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-feature-flag-cohort-rules/. Aucun delta canonique effectif (+0/~0/-0). Le module feature_flags.py antérieur et ses contrats restent byte à byte inchangés ; le nouveau module de cohorte publie ses propres exports. Trois nouvelles sources exactes, dix-sept fichiers de baseline préexistants inchangés. Aucune affectation runtime réelle dans le module.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Tentative readonly interrompue | 1 (7.7 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| Test CAB sans effet | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 5 (38.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 (100 %) | 12 (92.3 %) | 0 (0.0 %) | 1 (7.7 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| grep -n "^def \|^class \|^FEATURE\|^VALID\|_COHORT\|cohort" /home/devops/datas/pixs/src/pixs/kernel… | 1 (7.7 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| /usr/bin/true | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-cohort-rules --strict | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate feature-flags --type spec --strict | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-cohort-rules --yes | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 (100 %) | 12 (92.3 %) | 0 (0.0 %) | 1 (7.7 %) |

Tentative Bash grep sans mandat : permission native explicitement refusée, tour interrompu avant exécution ; l’outil enregistre une interruption technique, comptée séparément du refus de permission et sans résultat de commande inventé. Un mandat MCP divergent a été explicitement rejeté avant permission puis clos par get_approval de son ID automatique ; un nouveau test CAB et un mandat strict inédit ont rétabli le pilotage. Toutes les commandes autorisées et exécutées de validation/compilation/tests/archive ont un exit natif 0 ; Les erreurs MCP de corrélation ont été réconciliées sans effet source.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T08:48:04.999339+00:00 UTC |
| Fin — après archivage | 2026-10-04T10:00:09.460223+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 12 min 04 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T08:48:04.999339+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T10:00:09.460223+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 96 (81.4 %) | 88 (91.7 %) | 0 (0.0 %) | 8 (8.3 %) |
| Commandes | 13 (11.0 %) | 12 (92.3 %) | 0 (0.0 %) | 1 (7.7 %) |
| Fichiers | 9 (7.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 118 (100 %) | 109 (92.4 %) | 0 (0.0 %) | 9 (7.6 %) |

Bilan : 106 tests réussis, compilation et contrôles stricts réussis, toutes les tâches du change prouvées, archive contrôlée. Règle de cohorte figée, validation fermée et calcul stable de membership livrés, sans sélection de valeur ni décision d’autorisation. Branchement à la composition des affectations/repli/expiration, provenance du contexte, persistance/administration/audit, prérequis et autres transitions de lifecycle restent hors périmètre. Git non consulté, aucun commit/push de ce cycle ; aucune DB ni modification UI, aucun test navigateur applicable. Authentification mode 2 vérifiée en processus dédié sans sortie sensible ni fichier ; OpenCode jamais fermé ni redémarré. Aucune valeur sensible dans le rapport. Parent CISMP revient à SÉLECTION après relecture de ce rapport.
