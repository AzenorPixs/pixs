# STATISTIQUES — add-initial-audit-event-representation

Archive : openspec/changes/archive/2026-10-04-add-initial-audit-event-representation. Sessions : ses_efe62c6d3ffexoBmnIDMta2p7P, ses_ef7efb678ffeUcbQiDPZhYTCHm, ses_ef7eb7d79ffeuBiziOyVOpqd18. Historique API complet borné à 2026-10-04T17:02:48.085816+00:00–2026-10-04T18:24:14.002560+00:00 UTC. Rapport, son mandat et ses vérifications exclus des compteurs de production. Parent CISMP ouvert.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A — version exacte absente | opencode-go | xhigh | 3.282 s | 99.240 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version et identifiant exact non télémétrés | OpenAI | N/A — non télémétré | N/A — aucune sonde orchestrateur | N/A | N/A |

Moyennes du codeur : sondes valides uniquement, hors production. Le logiciel OpenCode 1.18.34 ne donne pas la version du modèle. Durées actives, dénominateur cumulé du temps de service et chevauchements inconnus ; aucune durée calendaire, attente CAB ou appel d’outil assimilé à une génération.

## 1. Statistiques générales et décisions

205 messages, 147 outils, durée calendaire 01 h 21 min 25 s avec pauses/attentes/tests/archive. Convention : succès d’un outil = exécution observée, pas preuve suffisante d’un consentement manuel ; décisions CAB corrélées séparément par requestId. Les compteurs de production portent sur l’historique API complet des trois sessions OpenCode ciblées. Les appels directs d’outils de l’orchestrateur ne disposent pas d’un historique agrégé exposé ici : totaux orchestrateur N/A, erreurs de récupération signalées séparément sans les confondre avec les tests. Refus explicite, erreur technique et expiration sont distincts.

Décisions finales CAB uniques

| Catégorie | Nombre | Part |
|---|---:|---:|
| APPROVED | 23 | 100.0 % |
| Total | 23 | 100 % |

Développement : compilation exit 0 ; 18 tests unitaires d’audit, 1 intégration fraîche et 238 régressions, 257/257 réussis (100 %). Contrôles stricts du change et du référentiel réussis avant code, après preuves, et du change après cochage. Toutes les cases du change cochées après preuves. Archivage exit 0, canonical audit inchangé. Les transitoires pending_count 1 ont été réconciliés sans répéter les effets observés. Les corrections éventuelles de brouillons ont précédé leur publication. Les résultats exécutés sont conservés dans les preuves du cycle ; les incidents éventuels de transport ne sont pas assimilés à des échecs de test ou à des refus de permission.

Incident de pilotage observé : le tour readonly de préparation de l’intégration a expiré côté client (540 s), puis a tenté une écriture sans mandat CAB. Permission per_10802746c001evIB6HTWRZBzuo explicitement refusée, outil natif write en erreur de refus, fichier absent, 52 baselines et deux sources exactes. Seul le tour a été interrompu. Nouvelle session persistante et nouveau contrat CAB strict, prévol unique /usr/bin/true exit0 et READY0. Une seconde tentative Bash readonly (rg/head) a également été refusée avant effet; une nouvelle session et un prévol inédit ont été établis. Les tours readonly désactivent désormais explicitement les outils mutateurs via API native. Aucun effet publié ni test prouvé rejoué. Les refus sont comptabilisés séparément ; l’expiration cliente n’est pas un échec de test.

| Mesure de production | Valeur |
|---|---:|
| Tokens input | 1008 |
| Tokens output | 121979 |
| Tokens reasoning | 0 |
| Tokens total | 26441365 |
| Tokens cache_read | 25278499 |
| Tokens cache_write | 1039879 |
| Coût SDK déclaré | 0.66991311 USD |
| Compactions OpenCode observées | 1 |
| Autres compactages automatiques orchestrateur | N/A — compteur absent |

Sondes séparées : même prompt déterministe de 40 lignes, configuration qwen3.8-flash/opencode-go/xhigh, sans outil, sessions dédiées jetables supprimées. Chaque relève conserve les horodatages reçus directement par SSE, la durée premier–dernier, le TTMT et les tokens réels.

| Position | Envoi UTC | Premier événement UTC | Dernier événement UTC | TTMT | Premier–dernier | Sortie | Débit | Validité |
|---|---|---|---|---:|---:|---:|---:|---|
| début — représentation audit | 2026-10-04T17:02:48.244966+00:00 | 2026-10-04T17:02:51.299309+00:00 | 2026-10-04T17:02:55.995450+00:00 | 3.054 s | 4.696 s | 521 | 110.942/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T17:32:50.576187+00:00 | 2026-10-04T17:32:53.438479+00:00 | 2026-10-04T17:32:58.952193+00:00 | 2.862 s | 5.514 s | 524 | 95.036/s | valide |
| périodique — déclenchement horloge 30 minutes | 2026-10-04T18:02:50.731460+00:00 | 2026-10-04T18:02:55.290234+00:00 | 2026-10-04T18:03:01.391808+00:00 | 4.559 s | 6.102 s | 647 | 106.038/s | valide |
| fin — après archivage AuditEvent | 2026-10-04T18:24:04.519299+00:00 | 2026-10-04T18:24:07.172078+00:00 | 2026-10-04T18:24:13.917602+00:00 | 2.653 s | 6.746 s | 573 | 84.945/s | valide |

Collecte : 4 tentatives comptabilisées (reprise unique incluse, pas un créneau supplémentaire), 4 réussies (100.0 %), 0 échouées (0.0 %), 0 manquées (0.0 %). Déclenchement périodique par horloge toutes les 30 minutes ; aucune attente du créneau ne bloque le travail. TTMT min/max 2.653/4.559 s ; débit min/max 84.945/110.942/s. Surcharge : 2265 tokens de sortie, 53705 tokens total SDK, 0.01135135 USD, 36.185 s d’intervalle envoi–dernier événement mesurable (pas durée active) ; durée des tentatives sans dernier événement mesurable N/A.

## 2. Types de messages et d’outils

Rôles

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 169 | 82.4 % |
| user | 36 | 17.6 % |
| Total | 205 | 100 % |

Parties des messages

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.1 % |
| reasoning | 168 | 22.5 % |
| step-finish | 168 | 22.5 % |
| step-start | 168 | 22.5 % |
| text | 96 | 12.8 % |
| tool | 147 | 19.7 % |
| Total | 748 | 100 % |

Terminaisons, messages user sous N/A

| Catégorie | Nombre | Part |
|---|---:|---:|
| N/A | 37 | 18.0 % |
| stop | 34 | 16.6 % |
| tool-calls | 134 | 65.4 % |
| Total | 205 | 100 % |

Résultats par outil

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 58 (39.5 %) | 58 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 17 (11.6 %) | 17 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 7 (4.8 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 23 (15.6 %) | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 9 (6.1 %) | 8 (88.9 %) | 1 (11.1 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 16 (10.9 %) | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 15 (10.2 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |
| grep | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (0.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 147 (100 %) | 145 (98.6 %) | 2 (1.4 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives natives, pas nombre de fichiers uniques. Rapport présent exclu de l’intervalle ; compilation peut produire du bytecode régénérable exclu des écritures source.

Écritures observées, chemins intégraux

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-event-representation/proposal.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-event-representation/design.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-event-representation/tasks.md | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-event-representation/.openspec.yaml | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-event-representation/specs/audit/spec.md | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/audit_event.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_audit_event.py | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_audit_event_integration.py | 2 (20.0 %) | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| Total | 10 (100 %) | 9 (90.0 %) | 1 (10.0 %) | 0 (0.0 %) |

8 chemins uniques. Cinq artefacts déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-04-add-initial-audit-event-representation/. Aucun delta canonique effectif (+0/~0/-0). Les modules antérieurs restent byte à byte inchangés. Trois nouvelles sources/tests exactes, cinquante-deux fichiers de baseline inchangés. AuditEvent représente des métadonnées injectées ; aucune persistance ou mutation runtime.

## 4. Commandes

Familles

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec validate | 5 (33.3 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Test CAB sans effet | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tentative readonly refusée | 1 (6.7 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |

Libellés limités à 100 caractères ; préfixes tronqués identiques regroupés, commandes exactes dans les mandats

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec validate add-initial-audit-event-representation --strict | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --strict | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/python… | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src PYTH… | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| rg -n -i "python|pytest|unittest|test" /home/devops/datas/pixs/TECHNICAL.md /home/devops/datas/pixs… | 1 (6.7 %) | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-audit-event-representation --strict --no-… | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict --no-interactive | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-audit-event-representation --yes | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |

Commandes refusées et erreurs : voir les lignes réellement observées ci-dessus ; aucune tentative non présente dans cet intervalle n’est attribuée à ce cycle. Les opérations autorisées de compilation/tests/stricts/archivage ont leurs exits natifs contrôlés.

## 5. Accès web

Aucun webfetch/websearch de production : 0 approuvé, 0 refusé, 0 erreur ; taux N/A (dénominateur zéro), aucune URL visitée. API locales CAB/OpenCode et transport fournisseur LLM ne sont pas des visites web du codeur ; coûts réseau détaillés N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-04T17:02:48.085816+00:00 UTC |
| Fin — après archivage | 2026-10-04T18:24:14.002560+00:00 UTC |
| Durée globale (pauses et attentes incluses) | 01 h 21 min 25 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-04T17:02:48.086932+00:00 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-04T18:24:14.002560+00:00 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits absent : quota codex/window10080, compte et reset invérifiables ; aucun remplacement par quotas OpenCode. Les quotas Codex sont partagés, aucune variation attribuable à cette seule session.

Totaux croisés des domaines

| Élément | Total (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Autres outils | 122 (83.0 %) | 122 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers | 10 (6.8 %) | 9 (90.0 %) | 1 (10.0 %) | 0 (0.0 %) |
| Commandes | 15 (10.2 %) | 14 (93.3 %) | 1 (6.7 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 147 (100 %) | 145 (98.6 %) | 2 (1.4 %) | 0 (0.0 %) |

Bilan : 257 tests sûrs réussis, trois compilations natives exit0 et stricts réussis, toutes tâches du change prouvées, archive contrôlée. Représentation pure AuditEvent figée13champs, constructeur structurel non validant, validation explicite avec diagnostics freshlist triés/dédupliqués sans valeurs, types exacts avant callbacks, UTC calendaire injecté, parseurs composants publics réutilisés. Références opaques trusted ou synthétiques ; validation structurelle ne prouve ni classification de secret ni minimisation, permission, corrélation runtime, wireformat, persistance append-only, rétention ou intégrité. Source PostgreSQL et suites fanions/backend antérieures restent inchangées ; aucun PG réel supplémentaire. Git non consulté, aucun commit/push, config, dépendance ou UI modifié. PLLM mode1 qwen3.8-flash xhigh conservée, processus OpenCode jamais fermé ni redémarré. Corrections ciblées de brouillons avant publication : liste fraîche suivant conventions, chemin intégration fixe, imports normaux permis et gardes sensibles probées/reset avant comportement sans masquer appels, datetime dérivée pour horloges avec calendrier réel, grammaire UTC locale sans dupliquer parseurs SemVer, citation canonique exacte et extraction complète des blocs Markdown imbriqués. Les incidents de pilotage sont distingués des résultats natifs des tests. Parent CISMP revient à SÉLECTION après preuve du rapport.

### Compactage natif conjoint observé

Cycle commun 5400 secondes orchestré par CGPT. Seul l’achèvement natif des deux sessions compte.

| Cycle | Déclenchement UTC | Preuve codage | Preuve orchestrateur | Restauration |
|---|---|---|---|---|
| paired-b845f3e2a2f54430ae5f5c814a3f0871 | 2026-10-04T17:49:58.418722+00:00 | msg_10809708f001QVUmoJJ3v8A2nc / 2026-10-04T17:52:51.728279+00:00 | 01a10809-6f81-70e0-8b64-6f86761d8e7a / 2026-10-04T17:55:07.610915+00:00 | RESTORED |

Compteur conjoint documenté : 1. Autres compactages Codex automatiques N/A. Compacteur OC opencode-go/qwen3.8-flash, variante API non exposée, agent configuré xhigh. La preuve orchestrateur vise son fil réel.
