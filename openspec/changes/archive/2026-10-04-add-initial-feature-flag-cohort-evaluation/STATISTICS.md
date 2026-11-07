# STATISTIQUES — add-initial-feature-flag-cohort-evaluation

Archive : openspec/changes/archive/2026-10-04-add-initial-feature-flag-cohort-evaluation. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-04T10:12:17.035301+00:00–2026-10-04T10:56:44.824310+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.316 s | 99.755 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

121 messages, 79 outils, durée calendaire 00 h 44 min 27 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 19 | 100.0 % |
| Total | 19 | 100 % |

Développement : compilation exit 0 ; 12 tests unitaires de la composition étendue, 1 intégration fraîche et 106 régressions, 119/119 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

| Mesure de production | Valeur | Part des tokens SDK |
|---|---:|---:|
| Tokens input | 600 | 0.0 % |
| Tokens output | 55396 | 0.2 % |
| Tokens reasoning | 0 | 0.0 % |
| Tokens total | 26019956 | 100.0 % |
| Tokens cache_read | 25635405 | 98.5 % |
| Tokens cache_write | 328555 | 1.3 % |
| Coût SDK déclaré | 0.50200360 USD | N/A — coût |
| Compactions OpenCode observées | 0 | N/A — hors tokens |
| Compactions orchestrateur | N/A — compteur absent | N/A — hors tokens |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale intégration cohorte | 2026-10-04T10:12:17.205737+00:00 | 2026-10-04T10:12:20.733423+00:00 | 2026-10-04T10:12:26.799280+00:00 | 3.528 s | 6.066 s | 523 | 86.220/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T10:42:18.250002+00:00 | 2026-10-04T10:42:21.136647+00:00 | 2026-10-04T10:42:26.767758+00:00 | 2.887 s | 5.631 s | 523 | 92.877/s | valide |
| finale après archive composition cohorte | 2026-10-04T10:56:36.120939+00:00 | 2026-10-04T10:56:39.655752+00:00 | 2026-10-04T10:56:44.648786+00:00 | 3.535 s | 4.993 s | 600 | 120.167/s | valide |

Collecte : 3 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 3 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.887/3.535 s ; débit min/max 86.220/120.167/s. Surcharge : 1646 tokens de sortie, 40226 tokens total SDK, 0.00848872 USD, 26.639 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 100 | 82.6 % |
| user | 21 | 17.4 % |
| Total | 121 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 100 | 23.8 % |
| step-finish | 100 | 23.8 % |
| step-start | 100 | 23.8 % |
| text | 42 | 10.0 % |
| tool | 79 | 18.8 % |
| Total | 421 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 21 | 17.4 % |
| stop | 21 | 17.4 % |
| tool-calls | 79 | 65.3 % |
| Total | 121 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 39 (49.4 %) | 39 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 19 (24.1 %) | 19 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (10.1 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 10 (12.7 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 2 (2.5 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (1.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 79 (100 %) | 79 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-evaluation/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-evaluation/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-evaluation/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-evaluation/specs/feature-flags/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-cohort-evaluation/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flag_cohorts.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_cohort_evaluation.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_cohort_evaluation_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-feature-flag-cohort-evaluation/. Aucun delta canonique effectif (+0/~0/-0). Le module feature_flags.py antérieur reste byte à byte inchangé ; les anciens corps/classes du module de cohorte et ses quatre exports sont conservés, avec une API et un export ajoutés. Une source étendue et deux nouvelles sources exactes, dix-neuf autres fichiers de baseline inchangés. Aucune affectation runtime réelle dans le module.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 5 (50.0 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-cohort-evaluation --strict | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate feature-flags --type spec --strict | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-cohort-evaluation --yes | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T10:12:17.035301+00:00 UTC |
| Fin — après archivage | 2026-10-04T10:56:44.824310+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 00 h 44 min 27 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T10:12:17.035301+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T10:56:44.824310+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 60 (75.9 %) | 60 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 9 (11.4 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 10 (12.7 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 79 (100 %) | 79 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Bilan : 119 tests réussis, compilation et contrôles stricts réussis, toutes les tâches du change prouvées, archive contrôlée. Composition réelle cohorte/candidats/repli/expiration livrée dans un profil borné : membre conserve la valeur, non-membre non expiré applique ABSENT/R3, définition expirée impose STALE et son diagnostic, jamais une autorisation positive. Provenance et cohérence globale du snapshot, persistance/administration/audit, résolution de prérequis, autre lifecycle et réévaluation applicative de bout en bout restent hors périmètre. Git non consulté, aucun commit/push de ce cycle ; aucune DB ni modification UI, aucun test navigateur applicable. Authentification mode 2 vérifiée en processus dédié sans sortie sensible ni fichier ; OpenCode jamais fermé ni redémarré. Aucune valeur sensible dans le rapport. Parent CISMP revient à SÉLECTION après relecture de ce rapport.
