# STATISTIQUES — add-bulk-runtime-private-object-staging-v1

RUN cismp-pixs-758862ec875d4708 ; session native ses_ed28c2be1ffe0qztRlBt3vYHkl. Historique natif complet paginé arrêté avant rédaction : 216 messages.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| qwen3.8-flash | N/A modèle ; OpenCode 1.18.35 observé | opencode-go mode 2 | xhigh | 2.104 s | 81.868 | N/A |
| muse-spark-1.3-contributor | N/A modèle ; OpenCode 1.19.0 observé | opencode-go mode 1 | high | 3.519 s | 227.763 | N/A |

Version exacte du modèle et temps actif de génération hors outils/attentes non exposés : N/A ; aucun dénominateur de temps de service inventé.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex/CGPT, orchestrateur principal identifiable | N/A télémétrie du thread non exposée | N/A | N/A | N/A | N/A | N/A |

Aucune sonde de l’orchestrateur.

## 1. Statistiques générales et décisions

Durée calendaire : 03 h 33 min 33 s, incluant pauses, attentes, outils et interruption du fournisseur (pilotage arrêté à 02:58 puis repris à 05:27, heure de Paris). Aucun temps actif n’en est déduit.

216 messages ; 588 parties ; 91 appels d’outils. Décisions MCP request_validation : {'APPROVED': 26}. Une réussite de lecture ne prouve pas une approbation manuelle. completed = succès technique ; un exit1 de global strict qualifié reste un exit1, pas un succès CLI. Refus = règle native explicite ; erreur = défaut technique ou schéma. Appel malformé avant permission distinct d’une écriture effective.

| Modèle / raisonnement | Réponses | Entrée | Sortie | Raisonnement | Cache lu | Cache écrit | Coût natif USD |
|---|---:|---:|---:|---:|---:|---:|---:|
| qwen3.8-flash / xhigh | 103 (70.1 %) | 480 (0.2 %) | 71949 (86.8 %) | 0 (0.0 %) | 3029154 (51.5 %) | 4552079 (97.4 %) | 0.99277029 (94.2 %) |
| qwen3.8-flash / N/A | 1 (0.7 %) | 6 (0.0 %) | 4164 (5.0 %) | 0 (0.0 %) | 0 (0.0 %) | 123369 (2.6 %) | 0.02663178 (2.5 %) |
| muse-spark-1.3-contributor / high | 43 (29.3 %) | 263599 (99.8 %) | 6798 (8.2 %) | 5619 (100.0 %) | 2852407 (48.5 %) | 0 (0.0 %) | 0.03454811 (3.3 %) |
| Total | 147 (100 %) | 264085 (100 %) | 82911 (100 %) | 5619 (100 %) | 5881561 (100 %) | 4675448 (100 %) | 1.05395019 (100 %) |

Compteurs tokens/cache conservés séparément selon télémétrie. Erreurs de réponses assistant (hors appels outils) : {'MessageAbortedError': 21}. Compactage : 1 partie(s) native(s) observée(s). Aucun temps de service reconstitué à partir des durées de message.

Sondes : Qwen2 prévues et réussies (début,+30min) ; Muse2 prévues et réussies (reprise début,fin). Aucun relevé reconstruit pendant l’arrêt du pilotage. Sonde finale Qwen non effectuée lors du blocage précédent : N/A. Protocoles différents, moyennes séparées. Version modèle N/A.

| Sonde | État | TTMT | Tokens/s |
|---|---|---:|---:|
| Qwen début | success | 2.238680601119995 | 82.73302591584316 |
| Qwen +30 min | success | 1.9685084819793701 | 81.00376573124612 |
| Muse reprise-début | SUCCESS | 4.953820775961503 | 197.15033344424265 |
| Muse reprise-fin-après-archive | SUCCESS | 2.0843495239969343 | 258.37635966358636 |

Surcharge sondes : 4756 tokens de sortie, 0.00797053 USD natifs, exclus des tableaux de production. Durées incluses dans le calendrier, sans attribution au temps actif du développement.

## 2. Types de messages et d’outils

| Catégorie | Nombre | Part |
|---|---:|---:|
| assistant | 147 | 68.1 % |
| user | 69 | 31.9 % |
| Total | 216 | 100 % |

| Catégorie | Nombre | Part |
|---|---:|---:|
| compaction | 1 | 0.2 % |
| reasoning | 126 | 21.4 % |
| step-finish | 123 | 20.9 % |
| step-start | 124 | 21.1 % |
| text | 123 | 20.9 % |
| tool | 91 | 15.5 % |
| Total | 588 | 100 % |

Terminaisons assistant :

| Catégorie | Nombre | Part |
|---|---:|---:|
| non fourni | 24 | 16.3 % |
| stop | 44 | 29.9 % |
| tool-calls | 79 | 53.7 % |
| Total | 147 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| bash | 14 | 15.4 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 16 | 17.6 % | 16 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 26 | 28.6 % | 26 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 4 | 4.4 % | 3 (75.0 %) | 0 (0.0 %) | 1 (25.0 %) |
| read | 23 | 25.3 % | 18 (78.3 %) | 4 (17.4 %) | 1 (4.3 %) |
| write | 8 | 8.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 91 | 100 % | 85 (93.4 %) | 4 (4.4 %) | 2 (2.2 %) |

## 3. Fichiers modifiés

Tentatives d’écriture par cible absolue, pas un nombre de fichiers distincts. Cible absente d’un appel malformé non reconstruite.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-private-object-staging-v1/design.md | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-private-object-staging-v1/proposal.md | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-private-object-staging-v1/specs/object-storage/spec.md | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-bulk-runtime-private-object-staging-v1/tasks.md | 3 | 25.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_object_staging.py | 2 | 16.7 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_object_staging_integration.py | 2 | 16.7 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_object_staging.py | 1 | 8.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| N/A — cible absente, schéma refusé | 1 | 8.3 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| Total | 12 | 100 % | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |

Archivage unique : quatre artefacts déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-private-object-staging-v1 ; specsUpdated=false. Trois sources Python ajoutées ; 358 références contrôlées ; seul DEVOPS.md rafraîchi extérieurement est signalé sans correction. Le présent rapport est publié après cet intervalle sous mandat distinct et exclu de ses compteurs.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| Compilation Python | 3 | 21.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 5 | 35.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol inoffensif | 3 | 21.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests Python | 3 | 21.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 | 100 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Libellés limités à100 caractères (troncature explicite) :

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_object_staging.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_object_staging_… | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_object_staging.py | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/true | 3 | 21.4 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-p… | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 14.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_object… | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 1 | 7.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 14 | 100 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : aucune. Les quatre refus natifs portent sur des lectures. Trois compilations,29unitaires,1intégration fraîche et292régressions prouvés. Strict change sans issue ; global exit1 qualifié uniquement par les trois tuples WARNING identiques à la référence avant code.

## 5. Accès web

Aucun webfetch/websearch dans la session de production :0 accès,0 approuvé,0 refusé,0 erreur ; pourcentages N/A (dénominateur nul). Aucune URL visitée ou refusée à lister. Authentification, quotas et benchmark PLLM du processus dédié sont hors production ; aucun secret transmis au modèle.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-12T02:12:08.097528+02:00 |
| Fin — après archivage | 2026-10-12T05:45:41.866104+02:00 |
| Durée globale (pauses et attentes incluses) | 03 h 33 min 33 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-12T02:13:40.277178+02:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-12T05:45:41.866104+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé, aucun quota externe substitué. Quotas partagés par le compte : aucune variation attribuée exclusivement au change.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|
| autres | 65 | 71.4 % | 60 (92.3 %) | 4 (6.2 %) | 1 (1.5 %) |
| commandes | 14 | 15.4 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 12 | 13.2 % | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 91 | 100 % | 85 (93.4 %) | 4 (4.4 %) | 2 (2.2 %) |

322 tests et3compilations prouvés, archive unique vérifiée ; aucune activation de provider réel ou runtime complet. Profils et migrations antérieurs préservés ; pas de PG réel rejoué pour ces primitives mémoire. Git non consulté ni modifié. Aucun secret lu par le modèle, aucun déploiement ni effet externe de production. Défaut edit sans filePath refusé par schéma avant permission ; une seule édition réelle des tâches avec permission once et relecture octet pour octet. Les réponses interrompues sont comptées séparément des refus. Le RUN parent revient à SÉLECTION et reste incomplet.
