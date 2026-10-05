# STATISTIQUES — add-initial-feature-flag-definition-expiry

Archive : openspec/changes/archive/2026-10-04-add-initial-feature-flag-definition-expiry. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P, ses_efa763808ffe4HQXIb678vnpxT. Historique API complet borné à 2026-10-04T05:39:47.789812+00:00–2026-10-04T06:48:00.458255+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.142 s | 113.510 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

169 messages, 118 outils, durée calendaire 01 h 08 min 12 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet des deux sessions OpenCode. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 20 | 95.2 % |
| REJECTED | 1 | 4.8 % |
| Total | 21 | 100 % |

Développement : compilation exit 0 ; 19 tests unitaires de la composition étendue, 1 intégration fraîche et 71 régressions, 91/91 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats et incidents sont conservés dans les preuves : omission de session_id, polling inconnu et délais MCP, un mandat CAB explicitement rejeté sans permission ni effet source, reprise de la session originale immuable après clôture du pending puis nouveau test CAB réussi. Une session complémentaire n’a servi qu’au diagnostic broker. Corrections des scripts d’orchestration en mémoire, aucun fichier du broker/contrôleur modifié.

| Mesure de production | Valeur | Part des tokens SDK |
|---|---:|---:|
| Tokens input | 846 | 0.0 % |
| Tokens output | 91470 | 0.1 % |
| Tokens reasoning | 0 | 0.0 % |
| Tokens total | 110940220 | 100.0 % |
| Tokens cache_read | 109850728 | 99.0 % |
| Tokens cache_write | 997176 | 0.9 % |
| Coût SDK déclaré | 2.00016465 USD | N/A — coût, pas un effectif |
| Compactions OpenCode observées | 0 | N/A — compteur hors tokens |
| Compactions orchestrateur | N/A — compteur absent | N/A — compteur hors tokens |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale expiry | 2026-10-04T05:39:47.989206+00:00 | 2026-10-04T05:39:50.343532+00:00 | 2026-10-04T05:39:54.333531+00:00 | 2.354 s | 3.990 s | 498 | 124.812/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T06:09:49.285587+00:00 | 2026-10-04T06:09:52.211505+00:00 | 2026-10-04T06:09:56.162268+00:00 | 2.926 s | 3.951 s | 552 | 139.720/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T06:39:51.533698+00:00 | 2026-10-04T06:39:55.539417+00:00 | 2026-10-04T06:40:02.187162+00:00 | 4.006 s | 6.648 s | 540 | 81.231/s | valide |
| finale après archivage expiry | 2026-10-04T06:47:51.481053+00:00 | 2026-10-04T06:47:54.763295+00:00 | 2026-10-04T06:48:00.396912+00:00 | 3.282 s | 5.634 s | 610 | 108.278/s | valide |

Collecte : 4 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.354/4.006 s ; débit min/max 81.231/139.720/s. Surcharge : 2200 tokens de sortie, 53640 tokens total SDK, 0.01132080 USD, 32.790 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 143 | 84.6 % |
| user | 26 | 15.4 % |
| Total | 169 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 142 | 23.9 % |
| step-finish | 141 | 23.7 % |
| step-start | 142 | 23.9 % |
| text | 52 | 8.7 % |
| tool | 118 | 19.8 % |
| Total | 595 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 28 | 16.6 % |
| stop | 24 | 14.2 % |
| tool-calls | 117 | 69.2 % |
| Total | 169 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 48 (40.7 %) | 47 (97.9 %) | 0 (0.0 %) | 1 (2.1 %) |
| glob | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 21 (17.8 %) | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 2 (1.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 22 (18.6 %) | 20 (90.9 %) | 0 (0.0 %) | 2 (9.1 %) |
| write | 8 (6.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 11 (9.3 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 (1.7 %) | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| cgpt-validation_list_pending | 1 (0.8 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| cgpt-validation_broker_health | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (0.8 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 118 (100 %) | 113 (95.8 %) | 0 (0.0 %) | 5 (4.2 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definition-expiry/.openspec.yaml | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definition-expiry/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definition-expiry/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definition-expiry/specs/feature-flags/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-definition-expiry/tasks.md | 2 (22.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flags.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_evaluation_bounded.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_evaluation_bounded_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-feature-flag-definition-expiry/. Aucun delta canonique effectif (+0/~0/-0). Anciens contrats et corps des autres primitives byte à byte préservés ; composition étendue et trois docstrings locales actualisées ; exports antérieurs conservés dans le même ordre. Trois sources exactes, quatorze autres fichiers de baseline inchangés. Aucune affectation runtime réelle dans le module.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 5 (45.5 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test CAB sans effet | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (27.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 (100 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-definition-expiry --strict | 3 (27.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate feature-flags --type spec --strict | 2 (18.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (27.3 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-definition-expiry --yes | 1 (9.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 11 (100 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : aucune. Toutes les commandes de ce cycle ont terminé avec un exit natif 0 ; Les erreurs MCP de corrélation ont été réconciliées sans effet source.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A. Le processus d’authentification/contrôle des quotas de l’orchestrateur a interrogé `https://opencode.ai/zen/go/v1/usage` à 06:44:45 UTC sous autorisation explicite : accès réellement réalisé, sans sortie de secret ni fichier. Ce contrôle n’est pas un webfetch de production OpenCode et n’est pas inclus dans les 118 outils ; les totaux globaux des appels directs de l’orchestrateur restent N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T05:39:47.789812+00:00 UTC |
| Fin — après archivage | 2026-10-04T06:48:00.458255+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 08 min 12 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T05:39:47.789812+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T06:48:00.458255+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 98 (83.1 %) | 93 (94.9 %) | 0 (0.0 %) | 5 (5.1 %) |
| Fichiers | 9 (7.6 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 11 (9.3 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 118 (100 %) | 113 (95.8 %) | 0 (0.0 %) | 5 (4.2 %) |

Bilan : 91 tests réussis, compilation et contrôles stricts réussis, toutes les tâches du change prouvées, archive contrôlée. Expiration inclusive de définition appliquée à la composition bornée et gate temporelle des nouvelles affectations livrées, sur instant UTC injecté et sans horloge interne. Provenance serveur, branchement administratif et réévaluation applicative de bout en bout, cohorte/prérequis, autres transitions de lifecycle et source persistante/admin/audit restent hors périmètre. Git non consulté, aucun commit/push de ce cycle ; aucune DB ni modification UI, aucun test navigateur applicable. Authentification mode 2 vérifiée en processus dédié sans sortie sensible ni fichier ; OpenCode jamais fermé ni redémarré. Aucune valeur sensible dans le rapport. Parent CISMP revient à SÉLECTION après relecture de ce rapport.
