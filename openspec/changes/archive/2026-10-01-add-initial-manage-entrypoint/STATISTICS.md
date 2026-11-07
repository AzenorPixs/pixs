# STATISTIQUES — add-initial-manage-entrypoint

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-01-add-initial-manage-entrypoint.

Sessions : ses_f0931f77cffegEUAT8Y42JkUJB, ses_f073e3494ffe75gnnICTtEguYs. Intervalle global : 2026-10-01T11:32:36.574883+00:00 → 2026-10-01T19:09:25.263134+00:00. Pauses entre créneaux incluses; rédaction du rapport exclue.

Couverture quantifiée : histoire API de la reprise actuelle uniquement. Ancienne session inaccessible HTTP404 : ses_f0931f77cffegEUAT8Y42JkUJB. Ses messages, outils non conservés, tokens, coûts, compactions et durées sont N/A; les références historiques du checkpoint ne reconstituent pas une télémétrie complète. Les totaux 100 % portent exclusivement sur les données accessibles. La durée calendaire globale conserve les bornes vérifiables du checkpoint. Les six écritures et trois validations antérieures y restent référencées séparément, non ajoutées aux totaux API.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A | opencode-go | high | 3.181 s | 237.35 | 221.536 s (100.0 %) |

Version exacte non exposée : N/A. Moyennes des deux sondes comparables de la reprise (prompt fixe de 40 lignes). Le temps de service somme les plages horodatées texte et raisonnement, hors outils et permissions; les périodes sans marqueur peuvent être omises. Dénominateur : seules durées mesurables des agents, 221.536 s. Temps orchestrateur absent : ces pourcentages ne répartissent pas tout le temps de service; chevauchements non établis.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | N/A | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — télémétrie absente |

## 1. Statistiques générales et décisions

Un outil terminé sans erreur est compté comme succès, y compris lectures/MCP autorisés par règle; cela ne prouve pas une approbation manuelle. Les opérations natives exigent une décision CAB corrélée. Refus explicites de permission, erreurs et interruptions restent distincts. Les deux ECART_OC prospectifs du minuteur n’ont soumis aucun CAB et n’ont exécuté aucun outil natif : notes de protocole séparées, sans les transformer en permissions refusées. Sources bornées au change; aucun contenu exclu ni secret exploité.

| Mesure | Valeur |
| --- | --- |
| Messages production | 66 (100 %) |
| Outils production | 49 (100 %) |
| Succès | 49 (100.0 %) |
| Refus explicites | 0 (0.0 %) |
| Erreurs techniques | 0 (0.0 %) |
| Décisions APPROVED distinctes observées via MCP | 10 (100 % des opérations natives observées) |
| Tokens télémétrie production | {'total': 3780176, 'input': 524309, 'output': 15545, 'reasoning': 14704, 'cache_read': 3225618, 'cache_write': 0} |
| Coût télémétrie production | 0.064931936 — unité API, facturation réelle non déduite |
| Compactions observées | 0 (0.0 % des réponses assistant) |
| Résultat | 3 CLI initiaux, 581 unit, 161 integration OK; AST et strict OK; 8 tâches cochées; archive réussie |

| Champ tokens API | Nombre | Part du total API |
| --- | --- | --- |
| input | 524309 | 13.9 % |
| output | 15545 | 0.4 % |
| reasoning | 14704 | 0.4 % |
| cache_read | 3225618 | 85.3 % |
| cache_write | 0 | 0.0 % |
| total | 3780176 | 100 % |

| Sonde | Envoyée le | Valide | TTMT | Débit tokens/s | Sortie tokens |
| --- | --- | --- | --- | --- | --- |
| début de la reprise avant première édition | 2026-10-01T18:44:16.149188+00:00 | True | 4.120 s | 159.04 | 489 |
| fin manage après archivage | 2026-10-01T19:09:21.359651+00:00 | True | 2.242 s | 315.66 | 489 |

Sondes reprise : 2 prévues, 2 réussies (100 %), 0 échec (0 %), 0 manquée (0 %); activité de reprise inférieure à 30 min. Min/max TTMT : 2.242/4.120 s; débit : 159.04/315.66. Sonde historique de 11 h 32 conservée dans checkpoint, exclue des moyennes car prompt comparatif non exposé. Surcharge séparée des sondes actuelles : 22029 tokens totaux, 978 sortie, 0.002306452 coût télémétrie. Aucun ajout à production.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 16 | 24.2 % |
| assistant | 50 | 75.8 % |
| Total | 66 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 32 | 11.7 % |
| step-start | 50 | 18.3 % |
| reasoning | 92 | 33.7 % |
| tool | 49 | 17.9 % |
| step-finish | 50 | 18.3 % |
| Total | 273 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 34 | 68.0 % |
| stop | 16 | 32.0 % |
| Total | 50 | 100 % |

| Catégorie | Total | Part | Succès / approuvé et exécuté | Refus | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 4 | 8.2 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 10 | 20.4 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 8 | 16.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 21 | 42.9 % | 21 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 1 | 2.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total global | 49 | 100 % | 49 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

Tentatives d’écriture natives, pas fichiers uniques; reprise API accessible uniquement; préparation/code antérieurs non quantifiables ici. Le déplacement OpenSpec est une commande distincte. Parts du tableau fichiers : dénominateur 2.

| Catégorie | Total | Part | Succès / approuvé et exécuté | Refus | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 50.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-manage-entrypoint/tasks.md | 1 | 50.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total écritures | 2 | 100 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-01-add-initial-manage-entrypoint. Empreintes des quatre artefacts Markdown conservées, norme inchangée. Dans la reprise, manage.py/tests préservés, README ajouté puis cases tasks cochées. État non versionné output/cismp-state.json mis à jour par orchestrateur hors des appels de l’agent, exclu du tableau.

## 4. Commandes

| Commande (max100 caractères) | Occurrences | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python venv -B -c : AST manage.py/test et versions Django/psycopg | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python venv -B : unittest discover -s tests/unit -p test_initial_manage_entrypoint.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec : validate add-initial-manage-entrypoint --strict | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python venv -B : unittest discover -s tests/unit | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python venv -B : unittest discover -s tests/integration | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec : archive add-initial-manage-entrypoint --yes --skip-specs --json | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 | 100 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Catégorie | Total | Part | Succès / approuvé et exécuté | Refus | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| Prévol true / autres | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 4 | 50.0 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 3 | 37.5 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Commandes refusées : aucune permission native refusée observée. Les deux minuteurs non soumis ne sont pas des commandes exécutées/refusées par permission.

## 5. Accès web

| Statut | Nombre | Part |
| --- | --- | --- |
| Approuvé et visité | 0 | N/A — total 0 |
| Refusé | 0 | N/A — total0 |
| Erreur | 0 | N/A — total0 |

Aucun accès web de production observé. Prévol HTTPS PLLM orchestrateur hors de cette télémétrie; ne devient pas accès web de l’agent.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-01T11:32:36.574883+00:00 |
| Fin — après archivage et sonde finale | 2026-10-01T19:09:25.263134+00:00 |
| Durée globale (pauses et attentes incluses) | 07 h 36 min 48 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil natif absent | N/A | N/A |
| Après — après archivage | N/A — outil natif absent | N/A | N/A |
| Différence après − avant | — | N/A — relevés absents | — |

Quota partagé par le compte : aucune variation attribuée exclusivement à ce change ni convertie en tokens/euros. Aucun quota Spark, profil ancien ou secret ne remplace l’outil natif absent.

| Catégorie | Total | Part | Succès / approuvé et exécuté | Refus | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| Autres outils (lectures, MCP) | 39 | 79.6 % | 39 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 8 | 16.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Fichiers (écritures) | 2 | 4.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total global | 49 | 100 % | 49 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Totaux croisés : 49 = 49 par outil = 49 par domaine. Tests/strict réussis; archive prouvée, rapport validé séparément ensuite. Git non inspecté/modifié; aucun PostgreSQL réel, secret ou effet externe fonctionnel utilisé dans le jalon. Cycle global CISMP OPEN : prochaine sélection requise. Fermeture OpenCode à 07 h 30 à traiter; minuteurs non soumis, sans effet.
