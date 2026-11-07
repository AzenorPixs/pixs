# STATISTIQUES — add-initial-notification-deduplication-reference-v1

RUN cismp2-pixs-d96f4399cb554df5, contexte 252, session ses_eba0e91c2ffeCBJ2Rxk318AOcJ.

Intervalle natif : 2026-10-16T18:20:12.733000+00:00 → 2026-10-16T19:18:33.978457+00:00. Publication de ce rapport et clôture hors intervalle. La RSMP préalable (contexte 245, référence 26) est hors des agrégats de ce change.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version modèle non exposée | OpenCode Go | high | 7.560 s | 223.7 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A | OpenAI | N/A | N/A — non sondé | N/A | N/A |

Runtime observé : OpenCode 1.19.3, CAB 1.2.1. Busy inclut attentes/outils et ne prouve pas un temps de génération ; temps de service et dénominateur N/A. Sondes de codage séparées de la production, aucune sonde orchestrateur.

## 1. Statistiques générales et décisions

Début observé : 2026-10-16T18:20:12.783Z. Dernière observation : 2026-10-16T19:18:33.947Z. État RESERVED, phase REPORT.

| Décision CAB | Nombre | Part |
|---|---:|---:|
| approved | 22 | 100.0 % |
| rejected | 0 | 0.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 22 | 100.0 % |

Permissions once : 22. Erreurs techniques de validation : 0 (peuvent recouvrir une attente). Une approbation ne prouve pas une exécution.

| Latence observée | Nombre | Médiane | p95 | Échantillon |
|---|---:|---:|---:|---:|
| requestToDecision | 22 | 1.484 s | 5.370 s | 22 |
| decisionToOnce | 22 | 5.474 s | 30.142 s | 22 |
| nativeTool | 100 | 0.424 s | 5.240 s | 100 |

Quantiles sur les dernières 2048 observations au maximum. Temps réservé : 3501.164 s ; busy : 960.233 s ; idle : 2489.259 s ; natif inconnu : 51.672 s.

| Compteur natif cumulé | Valeur |
| --- | --- |
| Entrée | 2161133 |
| Sortie | 35621 |
| Raisonnement | 6734 |
| Cache lu | 21442409 |
| Cache écrit | 0 |

Coût natif cumulé : 0.267469118 (unité non exposée). Compteurs tokens/cache/raisonnement distincts, sans addition ni pourcentage commun ambigu. Quota Codex N/A, aucune consommation exclusive déduite.

Refus HTTP d’admission : {"decision-run-divergent": 1, "native-validation-not-correlated": 1}. Aucun n’est assimilé à un refus de permission. Un timeout MCP -32001 a été réconcilié via get/poll sur le même approval_id, puis approved, avec une seule exécution des régressions.

## 2. Types de messages et d'outils

| Rôle natif | Nombre | Part |
| --- | --- | --- |
| assistant | 121 | 62.4 % |
| user | 73 | 37.6 % |
| Total | 194 | 100.0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 124 | 21.0 % |
| step-finish | 121 | 20.5 % |
| step-start | 121 | 20.5 % |
| text | 124 | 21.0 % |
| tool | 100 | 16.9 % |
| Total | 590 | 100.0 % |

| Fin de réponse assistant | Nombre | Part |
| --- | --- | --- |
| stop | 32 | 26.4 % |
| tool-calls | 89 | 73.6 % |
| Total | 121 | 100.0 % |

| Famille | Total | Part | Achevés | Refusés | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| bash | 14 | 14.0 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cab-mcp | 63 | 63.0 % | 62 (98.4 %) | 0 (0.0 %) | 1 (1.6 %) |
| edit | 1 | 1.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 5 | 5.0 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 10 | 10.0 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 7 | 7.0 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 100 | 100.0 % | 99 (99.0 %) | 0 (0.0 %) | 1 (1.0 %) |

Convention : achevé décrit un appel natif terminé, autorisé automatiquement (lecture/MCP) ou via décision CAB (Bash/édition). Cela ne prouve pas à lui seul une approbation manuelle ni un code CLI nul. Les codes sont détaillés séparément ; une erreur MCP n’est pas un test échoué. L’historique natif inclut le cadrage initial, éventuellement antérieur de quelques millisecondes au contexte CAB.

## 3. Fichiers modifiés

| Chemin absolu avant archive | Tentatives | Part | Achevées | Refusées | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-deduplication-reference-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-deduplication-reference-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-deduplication-reference-v1/specs/notifications/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-notification-deduplication-reference-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/notification_deduplication.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_notification_deduplication_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_notification_deduplication.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Ces nombres sont des tentatives d’écriture native. Métadonnée générée par la commande OpenSpec, sans édition native distincte : /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-notification-deduplication-reference-v1/.openspec.yaml. Les quatre artefacts Markdown et cette métadonnée ont été déplacés dans cette archive. Les trois fichiers Python restent à leurs chemins ; les caches de compilation sont des effets régénérables déclarés, jamais lus comme sources. Canon et fichiers notifications existants préservés.

## 4. Commandes

| Famille | Nombre | Part |
| --- | --- | --- |
| Compilation Python | 3 | 21.4 % |
| OpenSpec | 8 | 57.1 % |
| Prévol | 1 | 7.1 % |
| Tests unittest | 2 | 14.3 % |
| Total | 14 | 100.0 % |

| Commande (100 caractères maximum) | Occurrences | Part | Codes natifs |
| --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-notification-deduplication-reference-v1 --… | 1 | 7.1 % | 0 |
| /home/devops/.local/npm/bin/openspec new change add-initial-notification-deduplication-reference-v1 | 1 | 7.1 % | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 7.1 % | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json | 2 | 14.3 % | 1, 1 |
| /home/devops/.local/npm/bin/openspec validate add-initial-notification-deduplication-reference-v1 -… | 2 | 14.3 % | 0, 0 |
| /home/devops/.local/npm/bin/openspec validate notifications --type spec --strict | 1 | 7.1 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/notification_deduplication.… | 1 | 7.1 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_notification_dedupli… | 1 | 7.1 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_notification_deduplication.… | 1 | 7.1 % | 0 |
| /usr/bin/true | 1 | 7.1 % | 0 |
| Tests ciblés : PYTHONPATH=src:tests/unit:tests/integration ; python3 -B -m unittest (tronqué) | 1 | 7.1 % | 0 |
| Régressions : PYTHONPATH=src:tests/unit:tests/integration ; python3 -B -m unittest (tronqué) | 1 | 7.1 % | 0 |

Commandes refusées : aucune permission native refusée observée. Deux validations strictes globales achevées retournent 1 pour les warnings historiques ; ce ne sont pas des réussites CLI. Les refus HTTP d’admission ne sont pas des commandes refusées. Commandes complètes et corrélations conservées dans le checkpoint du RUN.

## 5. Accès web

| Statut natif web | Nombre | Part |
| --- | --- | --- |
| Achevés | 0 | N/A |
| Refusés | 0 | N/A |
| Erreurs | 0 | N/A |
| Total | 0 | N/A |

Aucun outil web ni URL visitée/refusée observé dans cette session. Transport du fournisseur LLM distinct de la navigation. Les contrôles positifs des gardes réseau ne constituent pas des connexions métier réelles.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début natif | 2026-10-16T18:20:12.733000+00:00 |
| Fin après archivage, avant rédaction | 2026-10-16T19:18:33.978457+00:00 |
| Durée globale, pauses et attentes incluses | 00 h 58 min 21 s |

| Mesure du quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-16T18:20:12.792217+00:00 | N/A | N/A |
| Après — archivage et sonde finale | 2026-10-16T19:18:33.978457+00:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux relevés ; aucune différence reconstituée. Compte partagé, sans attribution exclusive à ce RUN.

### Sondes de codage

| Position | Horodatage | TTMT(s) | Tokens/s | Tokens sortie | État |
| --- | --- | --- | --- | --- | --- |
| début change implémentation avant première tâche | 2026-10-16T18:20:54.524154+00:00 | 2.823 | 218.0 | 602 | valide |
| +30 min change implémentation | 2026-10-16T18:50:24.920283+00:00 | 18.088 | 169.9 | 584 | valide |
| fin après archivage publié, avant rédaction des statistiques | 2026-10-16T19:11:58.665092+00:00 | 1.768 | 283.2 | 584 | valide |

Trois sondes prévues/réussies, 0 échouée / 0 manquée durant le codage terminé avant le créneau +60 min. Moyennes arithmétiques TTMT 7.560 s, débit 223.7 tokens/s ; min/max TTMT 1.768/18.088 s et débit 169.9/283.2 tokens/s. Prompt constant, sessions jetables sans outil/fichier/réseau, configuration Muse/high identique. Surcharge : 1770 tokens sortie des sondes, exclus des compteurs de production. Durée complète et coût des sondes N/A, non collectés ; leurs TTMT et débits observés sont détaillés ci-dessus.

| Domaine | Total | Part globale | Achevés | Refusés | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 8 | 8.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 14 | 14.0 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 78 | 78.0 % | 77 (98.7 %) | 0 (0.0 %) | 1 (1.3 %) |
| Global | 100 | 100.0 % | 99 (99.0 %) | 0 (0.0 %) | 1 (1.0 %) |

### Résultats et limites

| Contrôle | Résultat réellement observé |
| --- | --- |
| Compilations Python | 3 commandes, exit0 |
| Tests ciblés | 13 unitaires + 1 intégration fraîche = 14 passants |
| Régressions notifications | 65 passants ; total 79, aucun échec |
| Strict change et notifications | Change strict exit0 avant et après code ; notifications strict exit0 après code (RSMP préalable validée) |
| Global standard combiné | 81/81, exit0 |
| Global strict avant archive | 79/81, exit1, 4 WARNING historiques, 0 ERROR |
| Global strict après archive | 78/80, exit1, mêmes 4 WARNING, 0 ERROR |
| Archive | /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-notification-deduplication-reference-v1 |
| Publication | Référence 28, reçu atomique au checkpoint |
| Canon/existants | SHAs préservés, --skip-specs |
| Git | Non inspecté ; aucun commit/push |
| Secrets | Aucun secret transmis au modèle ou ajouté aux sources ; authentification fournisseur utilisée seulement par processus sécurisé |
| Clôture | Après vérification du seul STATISTIQUES.md, sans sélection suivante ; preuve au checkpoint |

Warnings : bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4], tous WARNING au message exact : Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior. La longueur reste hors critère de qualité ; aucune correction silencieuse ni réussite stricte CLI inventée.

CAB : exclusion 351.927 s ; file 797.303 s ; référence périmée 2.194 s ; natif inconnu 51.672 s. Conditions pouvant se recouvrir, non additionnables. Aucun gain causal ni temps productif déduit de busy.
