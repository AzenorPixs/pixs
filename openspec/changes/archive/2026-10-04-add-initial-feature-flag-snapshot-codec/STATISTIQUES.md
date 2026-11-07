# STATISTIQUES — add-initial-feature-flag-snapshot-codec

Archive : openspec/changes/archive/2026-10-04-add-initial-feature-flag-snapshot-codec. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P. Historique API complet borné à 2026-10-04T13:11:40.905281+00:00–2026-10-04T14:38:17.121720+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 4.162 s | 89.838 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

227 messages, 164 outils, durée calendaire 01 h 26 min 36 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet de la session OpenCode ciblée. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 24 | 100.0 % |
| Total | 24 | 100 % |

Développement : compilation exit 0 ; 17 tests unitaires du codec, 1 intégration fraîche et 136 régressions, 154/154 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical feature-flags inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 1152 |
| Tokens output | 116143 |
| Tokens reasoning | 0 |
| Tokens total | 27573931 |
| Tokens cache_read | 27004185 |
| Tokens cache_write | 452451 |
| Coût SDK déclaré | 0.57731717 USD |
| Compactions OpenCode observées | 1 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| initiale codec snapshot | 2026-10-04T13:12:33.898857+00:00 | 2026-10-04T13:12:38.467300+00:00 | 2026-10-04T13:12:45.723757+00:00 | 4.568 s | 7.256 s | 547 | 75.381/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T13:42:36.018535+00:00 | 2026-10-04T13:42:39.377245+00:00 | 2026-10-04T13:42:46.917160+00:00 | 3.359 s | 7.540 s | 544 | 72.149/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T14:12:37.199906+00:00 | 2026-10-04T14:12:43.057635+00:00 | 2026-10-04T14:12:49.208308+00:00 | 5.858 s | 6.151 s | 667 | 108.443/s | valide |
| finale après archive codec | 2026-10-04T14:38:08.918956+00:00 | 2026-10-04T14:38:11.781289+00:00 | 2026-10-04T14:38:17.043605+00:00 | 2.862 s | 5.262 s | 544 | 103.376/s | valide |

Collecte : 4 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.862/5.858 s ; débit min/max 72.149/108.443/s. Surcharge : 2302 tokens de sortie, 53742 tokens total SDK, 0.01136874 USD, 42.857 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 192 | 84.6 % |
| user | 35 | 15.4 % |
| Total | 227 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.1 % |
| reasoning | 192 | 23.7 % |
| step-finish | 192 | 23.7 % |
| step-start | 192 | 23.7 % |
| text | 69 | 8.5 % |
| tool | 164 | 20.2 % |
| Total | 810 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 35 | 15.4 % |
| stop | 35 | 15.4 % |
| tool-calls | 157 | 69.2 % |
| Total | 227 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| read | 27 (16.5 %) | 26 (96.3 %) | 0 (0.0 %) | 1 (3.7 %) |
| cgpt-validation_broker_readiness | 60 (36.6 %) | 60 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 24 (14.6 %) | 24 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 14 (8.5 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 24 (14.6 %) | 24 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 3 (1.8 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 10 (6.1 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 2 (1.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 164 (100 %) | 163 (99.4 %) | 0 (0.0 %) | 1 (0.6 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-snapshot-codec/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-snapshot-codec/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-snapshot-codec/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-snapshot-codec/tasks.md | 3 (30.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-feature-flag-snapshot-codec/specs/feature-flags/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/feature_flag_snapshot_codec.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_feature_flag_snapshot_codec.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_feature_flag_snapshot_codec_integration.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-feature-flag-snapshot-codec/. Aucun delta canonique effectif (+0/~0/-0). Les modules antérieurs restent byte à byte inchangés. Trois nouvelles sources exactes, vingt-sept fichiers de baseline inchangés. Le codec adapte un snapshot injecté ; aucune affectation runtime réelle embarquée.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Test CAB sans effet | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 6 (42.9 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (21.4 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 (100 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /usr/bin/true | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-feature-flag-snapshot-codec --strict | 4 (28.6 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate feature-flags --type spec --strict | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (21.4 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 2 (14.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-feature-flag-snapshot-codec --yes | 1 (7.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 (100 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T13:11:40.905281+00:00 UTC |
| Fin — après archivage | 2026-10-04T14:38:17.121720+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 26 min 36 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T13:11:40.905281+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T14:38:17.121720+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 140 (85.4 %) | 139 (99.3 %) | 0 (0.0 %) | 1 (0.7 %) |
| Commandes | 14 (8.5 %) | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 10 (6.1 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 164 (100 %) | 163 (99.4 %) | 0 (0.0 %) | 1 (0.6 %) |

Bilan : 154 tests réussis, compilation et contrôles stricts réussis, toutes les tâches du change prouvées, archive contrôlée. Codec backend pur livré : encodage et décodage du document exact, validation réelle intégrale, scalaires et causes R3 préservés. Persistance, provenance serveur, administration/audit, cache et convergence des rôles restent hors périmètre. Git non consulté, aucun commit/push, accès DB ou modification UI. PLLM mode1 qwen3.8-flash xhigh conservée, processus OpenCode non arrêté ni redémarré. Deux brouillons JSON limités à une accolade ont été repris en Markdown avant publication. Lecture native protégée du prompt refusée puis intégralité transmise par CGPT et reçue. Le brouillon unitaire long a été reçu complet à la frontière d’un appel d’abandon de tour après600s, sans effet natif ; prévol CAB frais réussi. Une circularité de tâche entre preuves pré-archive et rapport post-archive a été corrigée et validée avant cochage. Les erreurs observées restent dans les comptes. Parent CISMP revient à SÉLECTION après vérification du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|
| paired-59205292e1f246978b4dc794fc7780d3 | 2026-10-04T13:16:49.620239+00:00 | msg_1070f5d12001iajYfg5ZDDk49E / 2026-10-04T13:18:20.275273+00:00 | 01a1070f-5c9a-7892-a733-e62981f900b1 / 2026-10-04T13:21:42.003510+00:00 | RESTORED |

Compteur conjoint documenté : 1. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
