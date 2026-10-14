# STATISTIQUES — add-initial-feature-flag-fallback

Archive : openspec/changes/archive/2026-10-04-add-initial-feature-flag-fallback. Session : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-04T02:02:26.854311+00:00–2026-10-04T02:39:59.632668+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 4.367 s | 85.089 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

131 messages, 85 outils, durée calendaire 00 h 37 min 32 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 20 | 100.0 % |
| Total | 20 | 100 % |

Développement : compilation exit 0 ; 9 nouveaux tests unitaires, 1 intégration fraîche et 61 régressions, 71/71 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Huit cases cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Corrections de brouillons avant publication : documentation BOOLEAN/VARIANT, compteur piège global, constructeur du DTO piégé. Aucun test exécuté en échec.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 648 |
| Tokens output | 56312 |
| Tokens reasoning | 0 |
| Tokens total | 51463255 |
| Tokens cache_read | 51304660 |
| Tokens cache_write | 101635 |
| Coût SDK déclaré | 0.86776540 USD |
| Compactions OpenCode observées | 0 |
| Compactions orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| début — repli pur avant artefacts | 2026-10-04T02:02:27.025135+00:00 | 2026-10-04T02:02:34.540569+00:00 | 2026-10-04T02:02:40.026126+00:00 | 7.515 s | 5.486 s | 571 | 104.092/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T02:32:29.388541+00:00 | 2026-10-04T02:32:32.362819+00:00 | 2026-10-04T02:32:38.917610+00:00 | 2.974 s | 6.555 s | 548 | 83.603/s | valide |
| fin — après archive vérifiée, avant statistiques | 2026-10-04T02:39:49.164073+00:00 | 2026-10-04T02:39:51.773998+00:00 | 2026-10-04T02:39:59.365680+00:00 | 2.610 s | 7.592 s | 513 | 67.574/s | valide |

Collecte : 3 relèves comptabilisées, 3 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.610/7.515 s ; débit min/max 67.574/104.092/s. Surcharge : 1632 tokens de sortie, 40212 tokens total SDK, 0.00848214 USD, 32.732 s d’intervalle envoi–dernier événement (pas durée active).

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 108 | 82.4 % |
| user | 23 | 17.6 % |
| Total | 131 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| reasoning | 108 | 23.7 % |
| step-finish | 108 | 23.7 % |
| step-start | 108 | 23.7 % |
| text | 46 | 10.1 % |
| tool | 85 | 18.7 % |
| Total | 455 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 23 | 17.6 % |
| stop | 23 | 17.6 % |
| tool-calls | 85 | 64.9 % |
| Total | 131 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 40 (47.1 %) | 40 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 20 (23.5 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 (8.2 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 10 (11.8 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 4 (4.7 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 3 (3.5 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 85 (100 %) | 85 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-fallback/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-fallback/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-fallback/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-fallback/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-fallback/specs/feature-flags/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/feature_flags.py | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_fallback.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_fallback_integration.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-feature-flag-fallback/. Aucun delta canonique effectif (+0/~0/-0). Anciennes classes et fonctions R1/C1a byte à byte conservées ; exports anciens dans le même ordre. Trois sources exactes, douze autres fichiers de baseline inchangés. Aucune affectation runtime réelle dans le module.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 5 (50.0 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-fallback --strict | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate feature-flags --type spec --strict | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/feature_flags.py tests/unit/t… | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-fallback --yes | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : aucune. Toutes les commandes de ce cycle ont terminé avec un exit natif 0 ; aucun test ni contrôle strict n’a été rejoué après un échec.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T02:02:26.854311+00:00 UTC |
| Fin — après archivage | 2026-10-04T02:39:59.632668+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 00 h 37 min 32 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T02:02:26.854311+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T02:39:59.632668+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 65 (76.5 %) | 65 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 10 (11.8 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 10 (11.8 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 85 (100 %) | 85 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Bilan : 71 tests réussis, compilation et contrôles stricts réussis, huit tâches prouvées, archive contrôlée. Primitive de repli livrée ; détection d’échec, classification/provenance serveur, réévaluation applicative de bout en bout, cohorte/prérequis et source persistante/admin/audit restent hors périmètre. Git non consulté, aucun commit/push de ce cycle ; aucune DB ni modification UI, aucun test navigateur applicable. Authentification mode 2 vérifiée en processus dédié sans sortie sensible ni fichier ; OpenCode jamais fermé ni redémarré. Aucune valeur sensible dans le rapport. Parent CISMP revient à SÉLECTION après relecture de ce rapport.
