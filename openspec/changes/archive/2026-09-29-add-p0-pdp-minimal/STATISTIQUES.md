# Statistiques — add-p0-pdp-minimal

RUN `cismp-pixs-20260929-1134`, session `ses_f130e4e87ffeaY8YzgPakaCCOl`, racine `/home/devops/datas/pixs`. Archive : `2026-09-29-add-p0-pdp-minimal`.

Collecte du **2026-09-29T15:47:23.051923+00:00** au **2026-09-29T17:42:25.276812+00:00**, après archivage et sonde finale, avant rédaction de ce rapport. L'historique complet de la session est filtré sur cet intervalle : les travaux ScopeContext et RSMP antérieurs sont exclus. Les six sessions de sonde sont séparées de la production. Ce rapport, son mandat et sa vérification sont postérieurs à l'intervalle et exclus des totaux.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor (OpenCode build) | N/A — version exacte non exposée | OpenCode Go / opencode-go | low | 2.907 s | 340.173 | N/A — génération active non isolée |
| muse-spark-1.3-contributor (compaction native auxiliaire) | N/A | OpenCode Go / opencode-go | N/A — variant absent des métadonnées | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex / GPT-6 déclaré par la session | N/A — identifiant exact non exposé | OpenAI | N/A | N/A — aucune sonde orchestrateur | N/A | N/A |

Le temps calendaire des réponses OpenCode inclut génération, outils et attente CAB : il ne constitue pas un temps de service. Aucun dénominateur de service cumulé fiable n'est disponible, donc aucun pourcentage n'est estimé. Une sonde jetable a pu chevaucher une attente de compaction ; ses durées ne sont pas additionnées à la durée globale. La version n'est jamais déduite du nom du modèle. OpenCode observé : 1.18.33 ; CAB : 0.85.2.

## 1. Statistiques générales et décisions

Convention : « approuvé et exécuté » désigne un appel terminé avec succès, autorisé automatiquement ou manuellement. Une lecture native réussie ne prouve pas une approbation manuelle. Un refus exige une trace explicite de refus de permission ; aucun n'est observé. Les erreurs regroupent les échecs techniques et les commandes à sortie non nulle, distingués ci-dessous. Le refus fonctionnel DENY testé n'est pas un refus CAB.

| Mesure | Effectif | Part ou taux |
|---|---|---|
| Messages | 263 | 100 % |
| Appels d'outils | 168 | 100 % |
| Appels réussis | 162 | 96.4 % |
| Refus de permission | 0 | 0.0 % |
| Appels en erreur | 6 | 3.6 % |
| Mandats CAB uniques | 48 | 100 % |
| Mandats finalement APPROVED | 48 | 100 % des mandats |
| Opérations mutantes/commandes exécutées | 48 | 100 % des mandats : 35 écritures + 13 commandes |
| Réponses assistant interrompues | 2 | 1.0 % des réponses assistant |
| Compactions natives | 1 | 0.5 % des réponses assistant |
| Tâches achevées | 13 | 100 % des 13 tâches |
| Tests finaux | 377 | 100 % réussis : 281 unitaires + 96 intégration |
| Tests PDP dans les suites finales | 63 | 16.7 % : 53 unitaires + 10 intégration |
| Validation OpenSpec strict | 77 | 100 % ; 0 échec |
| AST Python | 9 | 100 % des 9 fichiers Python ciblés |
| UTF-8 / LF | 13 | 100 % des 13 fichiers ciblés |

Deux commandes policy ont terminé avec exit 1 (17 tests : 2 échecs/1 erreur ; puis 18 tests : 1 échec). Elles ont été corrigées et remplacées par les validations finales réussies. Les quatre autres erreurs d'outils sont trois délais MCP et une lecture de façade absente avant sa création. Les délais MCP ont été corrélés aux décisions APPROVED, sans rejouer d'opération consommée. Deux réponses assistant ont été interrompues ; ces interruptions ne s'ajoutent pas aux six erreurs d'outils.

Les premières réécritures du moteur étaient incomplètes et sont restées non validées. Revue, patches exacts vérifiés par SHA-256 et tests ont précédé le cochage. Une tentative de nouvelle session, sans travail projet, a été supprimée après refus de rebinding du job CAB immuable. La session principale a été conservée. Une compaction native réussie a ensuite réduit son contexte ; les erreurs du résumé compacté ont été explicitement corrigées avant reprise.

Tokens de production, métadonnées OpenCode cumulées par réponse (cache compté à chaque requête, pas un volume de texte unique) :

| Catégorie | Nombre | Part |
|---|---|---|
| entrée | 1480999 | 3.0 % |
| sortie | 93850 | 0.2 % |
| raisonnement | 4074 | 0.0 % |
| cache lu | 47835976 | 96.8 % |
| cache écrit | 0 | 0.0 % |
| Total | 49414899 | 100 % |

Le champ `tokens.total` cumulé vaut 49414899, égal à la somme des postes ci-dessus. Coût rapporté par OpenCode : **0.263356652**, unité monétaire non exposée dans ces métadonnées ; aucune conversion ni facturation réelle déduite.

Sondes du modèle build, prompt constant de 64 lignes, sans outil/fichier/réseau demandé à l'agent :

| Position réelle | Envoi UTC | Tokens sortie | TTMT s | Débit tokens/s | État |
|---|---|---|---|---|---|
| début | 2026-09-29T15:47:23.280507+00:00 | 585 | 2.618 | 344.103 | réussie |
| supplémentaire actuelle après échéance +30 min manquée | 2026-09-29T16:20:08.509375+00:00 | 585 | 4.124 | 305.326 | réussie |
| périodique à +30 min, exécutée avec retard observé après reprise du contexte | 2026-09-29T16:53:16.715600+00:00 | 585 | 2.272 | 363.808 | réussie |
| supplémentaire diagnostic latence pendant compaction, sans outils | 2026-09-29T17:09:05.995270+00:00 | 585 | 2.074 | 268.156 | réussie |
| périodique après +30 min depuis sonde diagnostic, horodatage réel | 2026-09-29T17:39:22.615037+00:00 | 585 | 3.744 | 297.650 | réussie |
| fin après archivage, avant statistiques | 2026-09-29T17:42:08.607169+00:00 | 586 | 2.611 | 461.999 | réussie |

| Bilan des sondes | Nombre | Part |
|---|---|---|
| Relèves effectivement tentées | 6 | 100 % des tentatives |
| Réussies | 6 | 100 % des tentatives |
| Échouées | 0 | 0,0 % des tentatives |
| Échéance manquée explicitement enregistrée | 1 | N/A — distincte des tentatives |
| Échéances prévues pour 1 h 55 d'activité | 5 | début + 3 périodiques + fin |

La cadence stricte de trente minutes n'a pas été tenue : l'échéance initiale du 29/09 à 16:17:27 UTC est enregistrée manquée ; une mesure supplémentaire réelle a été faite à 16:20. La suivante à 16:53 est retardée. La sonde de diagnostic à 17:09 est supplémentaire ; la mesure suivante est à 17:39. Ces mesures ne reconstruisent pas les échéances nominales initiales +60/+90 minutes. La table conserve leurs dates réelles ; elle ne revendique pas cinq relèves ponctuelles conformes.

Moyenne arithmétique TTMT : 2.907 s, min 2.074, max 4.124. Débit moyen : 340.173 tokens/s, min 268.156, max 461.999. Toutes les six sondes sont valides pour ces moyennes. Surcharge séparée : **3511 tokens de sortie**, **10.639 s de flux de sortie** ; coût des sondes et tokens d'entrée N/A, non conservés dans le relevé. Les instants monotoniques et identifiants de preuve restent dans `output/cismp-state.json`, clé `statistiques_pdp`.

## 2. Types de messages et d'outils

| Catégorie | Nombre | Part |
|---|---|---|
| user | 53 | 20.2 % |
| assistant | 210 | 79.8 % |
| Total | 263 | 100 % |

| Catégorie | Nombre | Part |
|---|---|---|
| text | 102 | 10.2 % |
| step-start | 208 | 20.7 % |
| reasoning | 317 | 31.6 % |
| tool | 168 | 16.7 % |
| step-finish | 208 | 20.7 % |
| compaction | 1 | 0.1 % |
| Total | 1004 | 100 % |

Les parties `reasoning` sont comptées par type uniquement ; leur contenu n'est pas reproduit.

Terminaisons des réponses assistant :

| Catégorie | Nombre | Part |
|---|---|---|
| tool-calls | 158 | 75.2 % |
| stop | 50 | 23.8 % |
| absente | 2 | 1.0 % |
| Total | 210 | 100 % |

Configurations observées : build low 209 réponses (99.5 %) ; compaction auxiliaire au raisonnement non exposé 1 réponse (0.5 %).

| Outil | Total (part) | Approuvé et exécuté (taux) | Refusé (taux) | Erreur (taux) |
|---|---|---|---|---|
| cgpt-validation_request_validation | 48 (28.6 %) | 46 (95.8 %) | 0 (0.0 %) | 2 (4.2 %) |
| write | 26 (15.5 %) | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 57 (33.9 %) | 56 (98.2 %) | 0 (0.0 %) | 1 (1.8 %) |
| bash | 13 (7.7 %) | 11 (84.6 %) | 0 (0.0 %) | 2 (15.4 %) |
| cgpt-validation_get_approval | 5 (3.0 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 9 (5.4 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 7 (4.2 %) | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (0.6 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| grep | 2 (1.2 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 168 (100 %) | 162 (96.4 %) | 0 (0.0 %) | 6 (3.6 %) |

## 3. Fichiers modifiés

Les nombres représentent des tentatives d'écriture natives réussies, pas des fichiers distincts : **35 écritures sur 13 fichiers**. Les chemins sont ceux au moment des opérations. Aucun refus ou échec d'écriture observé.

| Chemin absolu | Total (part) | Approuvé et exécuté (taux) | Refusé (taux) | Erreur (taux) |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-pdp-minimal/proposal.md | 1 (2.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-pdp-minimal/design.md | 3 (8.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-pdp-minimal/tasks.md | 2 (5.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-pdp-minimal/.openspec.yaml | 1 (2.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/policy.py | 3 (8.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/ports.py | 2 (5.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/snapshot.py | 4 (11.4 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_pdp_policy.py | 5 (14.3 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/decision.py | 6 (17.1 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/__init__.py | 1 (2.9 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_pdp_decision.py | 3 (8.6 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_pdp_time.py | 2 (5.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_pdp_audit.py | 2 (5.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 35 (100 %) | 35 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

L'archivage a déplacé les quatre artefacts de `/home/devops/datas/pixs/openspec/changes/add-p0-pdp-minimal/` vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-pdp-minimal/`. Ce déplacement est compté comme une commande, sans quatre écritures artificiellement ajoutées. Les spécifications normatives n'ont pas été synchronisées (`specsUpdated=false`). Ce rapport est une écriture ultérieure distincte.

## 4. Commandes

| Famille | Total (part) | Approuvé et exécuté (taux) | Refusé (taux) | Erreur (taux) |
|---|---|---|---|---|
| Tests | 7 (53.8 %) | 5 (71.4 %) | 0 (0.0 %) | 2 (28.6 %) |
| OpenSpec validation/archivage | 3 (23.1 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol CAB | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| AST/encodage | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 (100 %) | 11 (84.6 %) | 0 (0.0 %) | 2 (15.4 %) |
| Commande — libellé ≤100 caractères | Total (part) | Approuvé et exécuté (taux) | Refusé (taux) | Erreur (taux) |
|---|---|---|---|---|
| openspec validate --all --strict (exécutable DEVOPS, télémétrie 0) | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| python3 -B -m unittest discover -s tests/unit -p test_pdp_policy.py -v | 3 (23.1 %) | 1 (33.3 %) | 0 (0.0 %) | 2 (66.7 %) |
| /usr/bin/true | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| python3 -B -m unittest discover -s tests/unit -p 'test_pdp_*.py' -v | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| python3 -B -m unittest discover -s tests/unit -v | 2 (15.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| python3 -B -m unittest discover -s tests/integration -v | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| python3 -B -c : AST mémoire et SHA-256, UTF-8/LF des 13 chemins explicites | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| openspec archive add-p0-pdp-minimal --yes --skip-specs --json | 1 (7.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 (100 %) | 11 (84.6 %) | 0 (0.0 %) | 2 (15.4 %) |
Les libellés sont abrégés ; les commandes exactes sont conservées dans les entrées CAB et les appels Bash. **Commandes refusées : 0 (0,0 %)**. Les deux sorties exit 1 sont des validations en échec, jamais des refus de permission. Toutes les commandes ont utilisé les exécutables déclarés dans DEVOPS. Aucun Git, Docker, installation de dépendance ou commande de production observé.

## 5. Accès web

| Statut | Nombre | Taux |
|---|---|---|
| Approuvé/visité | 0 | N/A |
| Refusé | 0 | N/A |
| Erreur | 0 | N/A |
| Total | 0 | N/A — dénominateur nul |

Aucun outil web, URL visitée ou URL refusée dans l'historique de codage de cet intervalle. Les transports locaux OpenCode/CAB et les requêtes de génération vers le fournisseur ne sont pas des consultations web de l'agent. Aucun accès web n'est inventé à partir d'un lien cité.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-29T15:47:23.051923+00:00 |
| Fin — après archivage | 2026-09-29T17:42:25.276812+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 55 min 02 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-09-29T15:47:23.051963+00:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-29T17:42:25.276812+00:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Cause avant/après : outil natif `mcp__codex_app__get_usage_limits` non exposé, vérifié à chaque borne. Aucun quota Spark, ancien relevé, secret ou fichier de profil n'a été substitué. Les quotas sont partagés par le compte : une différence mesurable pourrait inclure d'autres tâches simultanées ; aucune attribution exclusive ni conversion en tokens n'est faite.

| Domaine | Total (part) | Approuvé et exécuté (taux) | Refusé (taux) | Erreur (taux) |
|---|---|---|---|---|
| Fichiers | 35 (20.8 %) | 35 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 13 (7.7 %) | 11 (84.6 %) | 0 (0.0 %) | 2 (15.4 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres | 120 (71.4 %) | 116 (96.7 %) | 0 (0.0 %) | 4 (3.3 %) |
| Total | 168 (100 %) | 162 (96.4 %) | 0 (0.0 %) | 6 (3.6 %) |

Contrôles croisés : 35 + 13 + 0 + 120 = 168 outils ; 162 succès + 0 refus + 6 erreurs = 168. 53 messages utilisateur + 210 assistant = 263. 48 mandats uniques APPROVED couvrent 35 écritures et 13 commandes. Les taux de la ligne Web valent N/A car son total est nul ; sa part globale est 0,0 %.

État de développement : 13/13 tâches prouvées, 281 tests unitaires et 96 d'intégration réussis, 77 validations OpenSpec strict réussies, AST/UTF-8/LF validés. Preuves finales : `msg_0ee3beaea001czNs46J3NmnpgH`, `msg_0ee39d289001fgqoFmAmAH7nKQ`, `msg_0ee3d83ca001at9xHC5T7g96Vx`, `msg_0ee3ec6bd001vLtuQPf5kC37BE`.

Archivage effectivement observé, exit 0 : `msg_0ee41eccb001FdcidFUKV7F0Mu`. L'ancien répertoire actif est absent, l'archive existe et ses tâches correspondent au contenu validé. Le PDP est un socle mémoire ; les tests ne prouvent aucun backend réel, PEP, filtrage source ou audit durable. Aucun Git inspecté, commit/push, nouveau secret lu ou opération de production observé. Le parent CISMP poursuit la sélection après vérification de ce rapport ; ce change archivé ne termine pas le projet.
