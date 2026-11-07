# STATISTIQUES — add-initial-audit-projection-invocation-v1

Projet Pixs ; RUN `cismp3-pixs-01a145c7189d` ; contexte CAB 256 ; session `ses_eb9ff2416ffePlK66zPcvUK3zB`. Archive `openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1`. Publication de référence 29 prouvée par reçu `publication-c3-invocation-a84067eda36d`.

Collecte native du contexte jusqu’au gel du 2026-10-16T22:17:54.299913+02:00 ; export contrôleur observé 2026-10-16T20:17:54.306Z. Le rapport lui-même et sa génération sont hors intervalle. La RSMP antérieure (référence 27) est hors de ce contexte ; elle n’est pas recomptée. Aucune source confidentielle ou journal exclu n’a été lu pour produire ce rapport.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A | OpenCode Go | high | 2,8 s | 242,7 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| N/A — Codex, identité native non exposée | N/A | OpenAI | N/A | N/A | N/A | N/A |

OpenCode 1.19.3 et CAB 1.2.1 sont observés. La révision exacte du modèle n’est pas exposée. Le temps de service et son dénominateur cumulé ne sont pas disponibles séparément des outils et attentes : aucune durée calendaire ou état busy n’est assimilé à de la génération productive. Aucune sonde de l’orchestrateur n’est réalisée.

## 1. Statistiques générales et décisions

Convention : « réussi » désigne un appel terminé avec succès, autorisé automatiquement ou par mandat ; cela ne prouve pas une approbation manuelle. Les décisions CAB sont comptées séparément. Les outils virtuels invalid sont des erreurs techniques même si leur enveloppe est completed ; un Bash avec exit 1 est compté comme échec CLI. Les refus de permission sont distincts des erreurs, délais et interruptions.

| Mesure | Valeur | Part/taux |
| --- | --- | --- |
| Mandats approuvés | 20 | 100,0 % |
| Mandats rejetés | 0 | 0,0 % |
| Clarifications CAB | 0 | 0,0 % |
| Permissions once consommées | 20 | 100,0 % |
| Demandes en attente | 0 | N/A |
| Total des décisions | 20 | 100,0 % |

| Résultat des outils | Nombre | Part du total |
| --- | --- | --- |
| réussi | 137 | 89,5 % |
| refus | 0 | 0,0 % |
| erreur | 16 | 10,5 % |
| inconnu | 0 | 0,0 % |
| Total | 153 | 100,0 % |

| Tokens natifs cumulés | Nombre | Part du total API |
| --- | --- | --- |
| input | 1988716 | 5,8 % |
| output | 52869 | 0,2 % |
| reasoning | 14682 | 0,0 % |
| cache_read | 32253208 | 94,0 % |
| cache_write | 0 | 0,0 % |
| total API | 34309475 | 100,0 % |

Les tokens sont les compteurs cumulés des réponses API, avec réinjection et cache ; ils ne représentent pas un contexte unique. Coût calculé natif OpenCode : 0.276888216 ; devise et facture réelles non exposées, aucune conversion monétaire inventée.

| État natif observé | Durée | Part de ces trois états |
| --- | --- | --- |
| busy | 00 h 34 min 11 s | 33,9 % |
| idle | 01 h 06 min 38 s | 66,1 % |
| inconnu natif | 00 h 00 min 00 s | 0,0 % |
| Total observé | 01 h 40 min 50 s | 100,0 % |

Ces états sont des observations contrôleur, pas du temps de service LLM. Exclusion propre C3 : 00 h 16 min 53 s ; file d’intégration : 00 h 24 min 07 s ; référence périmée : 00 h 05 min 50 s. Les chevauchements éventuels entre métriques empêchent de les additionner comme durée calendaire.

| Latence contrôleur | Échantillons | Moyenne ms | Médiane ms | p95 ms |
| --- | --- | --- | --- | --- |
| requestToDecision | 20 | 58473,1 | 31723,0 | 147020,0 |
| decisionToOnce | 20 | 24713,9 | 5465,0 | 117008,0 |
| nativeTool | 153 | 6872,4 | 346,0 | 60004,0 |

Quantiles sur les dernières 2 048 observations au maximum ; ici échantillons exposés par le contrôleur. Les délais de décision incluent l’attente de pilotage.

Relèves réelles de l’agent de codage, prompt identique de 4 815 caractères, sessions dédiées supprimées après contrôle, zéro outil :

| Position | Horodatage réel | TTMT s | Débit réponse tokens/s | Tokens sortie | État |
| --- | --- | --- | --- | --- | --- |
| début change | 2026-10-16T20:39:05.273121+02:00 | 2,5 | 283,6 | 1129 | réussie |
| complémentaire actuelle après échéance +30min manquée | 2026-10-16T21:10:51.462856+02:00 | 3,5 | 163,7 | 1175 | réussie |
| périodique anticipée à frontière avant intégration | 2026-10-16T21:40:47.850847+02:00 | 2,8 | 247,0 | 1149 | réussie |
| fin après archivage | 2026-10-16T22:05:11.732182+02:00 | 2,3 | 276,4 | 1150 | réussie |

Mesures valides : 4 ; échecs 0 ; créneaux manqués 1 ; créneaux anticipés 1. Le créneau manqué est signalé sans reconstruction ; sa sonde complémentaire possède son propre horodatage. Moyennes arithmétiques des seules mesures valides ; TTMT min/max 2,3/3,5 s, débit min/max 163,7/283,6. Cette télémétrie est une surcharge séparée de la production.

Incidents réconciliés : outil write initialement indisponible, appels invalid sans effet ; GET de santé loopback superflu ; question supplémentaire interrompue puis rejetée administrativement ; délais MCP suivis par polling sur les mêmes identifiants. Le mandat de cochage est resté en attente de ma décision, puis a repris sans nouveau requestId. Aucune écriture n’a été dupliquée, aucune permission hors mandat n’a été consommée, aucun effet inconnu ne subsiste. Une tentative HTTP de décision déjà enregistrée a été refusée sans créer une seconde décision.

| Échecs HTTP de coordination | Occurrences | Part |
| --- | --- | --- |
| decision-run-divergent | 1 | 4,0 % |
| native-validation-not-correlated | 22 | 88,0 % |
| native-observation-changed | 1 | 4,0 % |
| native-session-not-quiescent | 1 | 4,0 % |
| Total | 25 | 100,0 % |

Ces tentatives HTTP ne sont pas des refus distincts de permission native.

## 2. Types de messages et d’outils

| Rôle natif OpenCode | Messages | Part |
| --- | --- | --- |
| user | 90 | 36,7 % |
| assistant | 155 | 63,3 % |
| Total | 245 | 100,0 % |

Les user comprennent mandats CGPT, heartbeats sans réponse et relances superviseur. Les messages du chat Codex et les sessions des pairs ne sont pas recomptés ; leur historique complet n’est pas exposé ici.

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 172 | 22,1 % |
| step-start | 155 | 19,9 % |
| reasoning | 144 | 18,5 % |
| tool | 153 | 19,7 % |
| step-finish | 153 | 19,7 % |
| Total | 777 | 100,0 % |

| Fin de réponse assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 122 | 78,7 % |
| stop | 31 | 20,0 % |
| interrompu/non exposé | 2 | 1,3 % |
| Total | 155 | 100,0 % |

| Outil | Total | Part | Réussis | Taux réussi | Refus | Taux refus | Erreurs | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 11 | 7,2 % | 9 | 81,8 % | 0 | 0,0 % | 2 | 18,2 % |
| cgpt-validation_broker_health | 1 | 0,7 % | 1 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| cgpt-validation_broker_readiness | 31 | 20,3 % | 31 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| cgpt-validation_get_approval | 8 | 5,2 % | 8 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| cgpt-validation_list_pending | 1 | 0,7 % | 1 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| cgpt-validation_poll_approval | 10 | 6,5 % | 5 | 50,0 % | 0 | 0,0 % | 5 | 50,0 % |
| cgpt-validation_request_validation | 20 | 13,1 % | 15 | 75,0 % | 0 | 0,0 % | 5 | 25,0 % |
| edit | 1 | 0,7 % | 1 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| glob | 10 | 6,5 % | 10 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| grep | 2 | 1,3 % | 2 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| invalid | 3 | 2,0 % | 0 | 0,0 % | 0 | 0,0 % | 3 | 100,0 % |
| question | 1 | 0,7 % | 0 | 0,0 % | 0 | 0,0 % | 1 | 100,0 % |
| read | 39 | 25,5 % | 39 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| todowrite | 6 | 3,9 % | 6 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| webfetch | 1 | 0,7 % | 1 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| write | 8 | 5,2 % | 8 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| Total | 153 | 100,0 % | 137 | 89,5 % | 0 | 0,0 % | 16 | 10,5 % |

## 3. Fichiers modifiés

| Chemin absolu complet | Écritures réussies | Part des éditions | Refus | Taux refus | Erreurs | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1/design.md | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1/proposal.md | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1/specs/audit/spec.md | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1/specs/authorization-engine/spec.md | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1/tasks.md | 2 | 22,2 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/src/pixs/core/authz/audit_projection_invocation.py | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/tests/integration/test_audit_projection_invocation_integration.py | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/tests/unit/test_audit_projection_invocation.py | 1 | 11,1 % | 0 | 0,0 % | 0 | 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1/.openspec.yaml | 0 | 0,0 % | 0 | N/A | 0 | N/A |
| Total des éditions | 9 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |

Il s’agit de tentatives d’édition natives : neuf éditions pour huit cibles, tasks.md ayant une création puis un cochage. La métadonnée .openspec.yaml est créée par la commande OpenSpec, pas par un outil d’édition. Neuf fichiers versionnables distincts sont concernés : trois nouvelles sources et six artefacts du change. L’archive déplace les six artefacts sans nouvelle édition des canons. Les caches py_compile régénérables sont des effets déclarés de compilation, pas des sources analysées. Le présent STATISTIQUES.md sera publié sous mandat distinct hors intervalle, et n’est pas compté comme écriture déjà réussie dans son propre rapport.

## 4. Commandes

| Famille | Total | Part | Réussies | Taux réussi | Refus | Taux refus | Erreurs | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Prévol | 1 | 9,1 % | 1 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| OpenSpec | 6 | 54,5 % | 4 | 66,7 % | 0 | 0,0 % | 2 | 33,3 % |
| Python | 4 | 36,4 % | 4 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| Total | 11 | 100,0 % | 9 | 81,8 % | 0 | 0,0 % | 2 | 18,2 % |

| Commande (100 caractères maximum) | Occurrences | Part | Réussies | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 1 | 9,1 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec new change add-initial-audit-projection-invocation-v1 | 1 | 9,1 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-audit-projection-invocation-v1 --strict | 1 | 9,1 % | 1 | 0 | 0 |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX= /home/devops/datas/pixs/.venv/bin/python3 -m py_comp… | 1 | 9,1 % | 1 | 0 | 0 |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests/unit:tests/integration /home/devops/datas/pixs/.venv… | 1 | 9,1 % | 1 | 0 | 0 |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests/unit:tests/integration /home/devops/datas/pixs/.venv… | 1 | 9,1 % | 1 | 0 | 0 |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests/unit:tests/integration /home/devops/datas/pixs/.venv… | 1 | 9,1 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 9,1 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 18,2 % | 0 | 0 | 2 |
| /home/devops/.local/npm/bin/openspec archive add-initial-audit-projection-invocation-v1 --yes --ski… | 1 | 9,1 % | 1 | 0 | 0 |
| Total | 11 | 100,0 % | 9 | 0 | 2 |

Commandes refusées : aucune (0 ; 0,0 %). Les deux exits 1 correspondent exclusivement aux validations globales strictes avant/après archive avec les quatre WARNING préexistants ; ils ne sont pas présentés comme succès CLI.

## 5. Accès web

| Résultat webfetch/websearch | Nombre | Part |
| --- | --- | --- |
| réussi | 1 | 100,0 % |
| refus | 0 | 0,0 % |
| erreur | 0 | 0,0 % |
| Total | 1 | 100,0 % |

| URL observée (100 caractères maximum) | Résultat | Autorisation |
| --- | --- | --- |
| http://127.0.0.1:4096/global/health | réussi | Automatique OpenCode ; diagnostic loopback superflu déclaré |

Aucune URL web refusée. Ce compteur porte sur les outils web ; le transport MCP/SSE et les appels nécessaires au fournisseur LLM ne sont pas assimilés à webfetch. Les quotas OpenCode Go sont lus par processus sécurisé ; les valeurs de secrets ne sont jamais transmises au modèle ou conservées dans ce rapport. Les compteurs HTTP complets du fournisseur et du chat Codex sont N/A, non exposés.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début natif du contexte | 2026-10-16T20:37:03.861000+02:00 |
| Fin — après archive, sondes et gel de collecte | 2026-10-16T22:17:54.299913+02:00 |
| Durée globale (pauses et attentes incluses) | 01 h 40 min 50 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage de la spécification | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits absent de cette connexion : aucun relevé Codex n’est reconstruit, aucun quota Spark ou Go ne le remplace. Les quotas de comptes sont partagés : aucune variation n’est attribuée exclusivement à cette session.

| Relevé réel Mode 1 partagé | Horodatage | 5 h utilisé | Semaine utilisé | Mois utilisé |
| --- | --- | --- | --- | --- |
| début change | 2026-10-16T20:39:05+02:00 | 4 % | 61 % | 95 % |
| complémentaire actuelle après échéance +30min manquée | 2026-10-16T21:10:51+02:00 | 7 % | 62 % | 96 % |
| périodique anticipée à frontière avant intégration | 2026-10-16T21:40:47+02:00 | 9 % | 62 % | 96 % |
| fin après archivage | 2026-10-16T22:05:11+02:00 | 10 % | 63 % | 96 % |

Réinitialisations du dernier relevé : 5 h 2026-10-16T20:32:04.000Z ; semaine 2026-10-19T00:00:00.000Z ; mois 2026-10-19T19:07:16.000Z. Ces relevés ne mesurent pas une consommation exclusive C3.

| Domaine des outils | Total | Part globale | Réussis | Taux réussi | Refus | Taux refus | Erreurs | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAB MCP | 71 | 46,4 % | 61 | 85,9 % | 0 | 0,0 % | 10 | 14,1 % |
| Commandes | 11 | 7,2 % | 9 | 81,8 % | 0 | 0,0 % | 2 | 18,2 % |
| Autres outils | 10 | 6,5 % | 6 | 60,0 % | 0 | 0,0 % | 4 | 40,0 % |
| Lectures/recherches | 51 | 33,3 % | 51 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| Éditions | 9 | 5,9 % | 9 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| Web | 1 | 0,7 % | 1 | 100,0 % | 0 | 0,0 % | 0 | 0,0 % |
| Total global | 153 | 100,0 % | 137 | 89,5 % | 0 | 0,0 % | 16 | 10,5 % |

| Preuve exécutée | Résultat |
| --- | --- |
| Tests dédiés et processus frais | 13 réussis, 0 échec, 0 skip |
| Régressions audit/authz | 124 réussis, 0 échec, 0 skip |
| Requalification combinée sous exclusion | 137 réussis, 0 échec, 0 skip |
| Total des exécutions de tests | 274 ; la campagne combinée requalifie les cas déjà exécutés |
| Syntaxe | 3 fichiers compilés par une invocation, exit 0 ; grammaire Python 3.12 analysée, exécution dans venv du projet |
| OpenSpec ciblé du change | exit 0 |
| OpenSpec global standard avant archive | 80/80, exit 0 |
| OpenSpec global strict après archive | 77 passés, 2 échoués, exit 1 ; 4 WARNING antérieurs et 0 ERROR |
| Tâches | 9/9 cochées après preuves |
| Archive | openspec/changes/archive/2026-10-16-add-initial-audit-projection-invocation-v1 ; exit 0 ; six artefacts vérifiés |
| Publication CAB | référence 29, exclusion libérée, reçu atomique REPORT |
| Git | Non inspecté ; aucun commit/push effectué |
| Backend réel, navigateur, nouvelle dépendance | Sans objet pour ce profil borné ; non exécutés/non ajoutés |

Avertissements stricts exacts : bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4], chacun « Requirement text is very long (>500 characters) ». Ils préexistaient à ce change ; aucun nouveau warning n’est introduit. Le retour True du port n’est ni une preuve de persistance, ni une conformité P0, ni une autorisation d’accès.

La session C3 doit être arrêtée à la borne explicitement demandée après vérification de ce rapport, sans nouvelle sélection. Le gate final et la clôture ne sont pas annoncés comme déjà exécutés par ce document avant sa publication. Les services des autres RUN restent préservés.
