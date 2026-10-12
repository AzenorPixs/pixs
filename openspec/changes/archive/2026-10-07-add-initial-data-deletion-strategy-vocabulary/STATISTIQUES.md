# STATISTIQUES — add-initial-data-deletion-strategy-vocabulary

Session OpenCode : ses_eed633581ffeOeSPxYZNclbGnr. RUN parent : cismp-pixs-20261006-soir-R1. Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-deletion-strategy-vocabulary.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Qwen3.8 Flash (qwen3.8-flash) | N/A — version du modèle non fournie ; OpenCode 1.18.34 | OpenCode Go | xhigh observé dans les messages | N/A — aucune sonde valide | N/A — aucune sonde valide | N/A — génération non isolable des outils/attentes |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (GPT-6 déclaré) | N/A — version précise non exposée | OpenAI | N/A — télémétrie native non exposée | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — source de durée active absente |

Temps de service et pourcentage : N/A pour tous les agents ; aucun dénominateur fiable, durée calendaire et outils non assimilés à la génération. Les quotas Codex natifs sont indisponibles.

## 1. Statistiques générales et décisions

Source : historique natif complet de la session, filtré du début du mandat de sélection au dernier rapport d’archive, avec bornes ci-dessous. Sondes jetables séparées ; prévol initial, RSMP, benchmark PLLM et rédaction/publication du présent rapport exclus de la production. Les résultats de CGPT sont limités aux décisions CAB réellement relues ; autres outils/messages orchestrateur N/A, historique natif indisponible.

Convention : « approuvé/exécuté » désigne un outil natif terminé (permission implicite de lecture ou CAB explicite selon le type), sans prouver une approbation manuelle pour les lectures. Un outil Bash terminé et un code CLI 1 qualifié ne constituent pas une validation CLI réussie. Refus = rejet explicite de permission ; erreur = autre échec/interruption.

| Mesure | Effectif | Part ou taux |
|---|---|---|
| Messages | 145 | 100 % |
| Outils | 87 | 100 % |
| Outils terminés | 84 | 96.6 % |
| Refus natifs | 0 | 0.0 % |
| Erreurs techniques | 3 | 3.4 % |
| Décisions CAB APPROVED | 27 | 96.4 % |
| Décisions CAB REJECTED | 1 | 3.6 % |
| Tests réussis | 17 | 100 % (17/17) |
| Compilations réussies | 3 | 100 % (3/3) |
| Tâches prouvées/cochées | 6 | 100 % (6/6) |
| Compactions natives dans intervalle | 0 | N/A — aucun cycle prévu atteint |

| Tokens natifs de production | Valeur | Part |
|---|---|---|
| input | 672 | 0.0 % |
| output | 36858 | 0.1 % |
| reasoning | 0 | 0.0 % |
| cache_read | 32798251 | 99.6 % |
| cache_write | 93417 | 0.3 % |
| Total (somme catégories) | 32929198 | 100 % |

Coût natif OpenCode : 0.560879476 USD. Cache inclus dans le total déclaré des catégories, sans estimation de coût ou de tokens orchestrateur. L’intervalle inclut les prévols de récupération et la programmation opérationnelle de fermeture à 7h30 Paris. Les délais MCP et pollings corrélés sont tracés sans resoumission ni rejeu d’effet. Une commande de temporisateur altérée a été REJECTED avant exécution ; une expression différente, approuvée sous RID neuf, a lancé le seul timer. La fermeture future n’est pas comptée comme déjà effectuée.

| Relève | Tentative | Lignes | Outils | État |
|---|---|---|---|---|
| début-deletion-strategy-vocabulary | 1 | 1 | 0 | invalide — sortie fixe non conforme |
| début-deletion-strategy-vocabulary | 2 | 1 | 0 | invalide — sortie fixe non conforme |
| +30min-slot-2026-10-07T04:09:38.251462+00:00 | 1 | 50 | 0 | invalide — sortie fixe non conforme |
| +30min-slot-2026-10-07T04:09:38.251462+00:00 | 2 | 9 | 0 | invalide — sortie fixe non conforme |
| fin-deletion-strategy-vocabulary | 1 | 1 | 0 | invalide — sortie fixe non conforme |
| fin-deletion-strategy-vocabulary | 2 | N/A | N/A | échec — TimeoutError, télémétrie indisponible |

Trois relèves prévues (début/+30 min/fin), zéro réussie, trois échouées ; cinq tentatives non conformes et une expirée, zéro relève manquée. Le créneau +30 min a été mesuré pendant le travail ; le suivant +60 min survient après la fin du codage, aucune relève n’a été recréée rétroactivement. TTMT/débit des tentatives invalides exclus des moyennes. Prompt constant de 200 lignes « alpha beta gamma delta epsilon zeta eta theta iota kappa », même configuration Qwen/OpenCode Go/xhigh demandée, zéro outil observé sur les cinq tentatives avec télémétrie ; outils de la tentative expirée N/A. Sessions supprimées après chaque tentative.

Surcharge de sondes partielle, sur cinq tentatives observées : 55499 tokens natifs (cache inclus), 0.007791974 USD, 37.226 s de durées natives cumulées (pas un temps de génération prouvé). Total complet N/A : la sixième tentative a expiré côté client sans télémétrie finale ; ses tokens, coût et durée native restent inconnus. Aucun zéro ni estimation substitués.

## 2. Types de messages et d’outils

| Rôle | Effectif | Part |
|---|---|---|
| assistant | 112 | 77.2 % |
| user | 33 | 22.8 % |
| Total | 145 | 100 % |

| Type de partie | Effectif | Part |
|---|---|---|
| reasoning | 112 | 22.7 % |
| step-finish | 112 | 22.7 % |
| step-start | 112 | 22.7 % |
| text | 70 | 14.2 % |
| tool | 87 | 17.6 % |
| Total | 493 | 100 % |

| Terminaison assistant | Effectif | Part |
|---|---|---|
| stop | 33 | 29.5 % |
| tool-calls | 79 | 70.5 % |
| Total | 112 | 100 % |

| Type | Total | Part | Terminés | Refus | Erreurs |
|---|---|---|---|---|---|
| bash | 18 | 20.7 % | 18 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 9 | 10.3 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 7 | 8.0 % | 7 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 1.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 28 | 32.2 % | 25 (89.3 %) | 0 (0.0 %) | 3 (10.7 %) |
| glob | 1 | 1.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 3 | 3.4 % | 3 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 11 | 12.6 % | 11 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 9 | 10.3 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 87 | 100 % | 84 (96.6 %) | 0 (0.0 %) | 3 (3.4 %) |

## 3. Fichiers modifiés

| Chemin absolu écrit | Tentatives | Part | Approuvées/exécutées | Refus | Erreurs |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-data-deletion-strategy-vocabulary/.openspec.yaml | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-deletion-strategy-vocabulary/design.md | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-deletion-strategy-vocabulary/proposal.md | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-deletion-strategy-vocabulary/specs/data-lifecycle/spec.md | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-deletion-strategy-vocabulary/tasks.md | 2 | 22.2 % | 2 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_deletion_strategies.py | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_deletion_strategies_integration.py | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_deletion_strategies.py | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

Tentatives d’écriture : neuf sur huit fichiers distincts (tasks.md écrit ouvert puis coché). Les cinq artefacts OpenSpec ont été déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-deletion-strategy-vocabulary. Les trois sources restent à leurs chemins. Aucun cadrage ou spec canonique modifié dans cet intervalle ; RSMP antérieure exclue. Contrôle après archive : cinq hashes d’artefacts, trois de sources et 140 références inchangés.

## 4. Commandes

| Famille | Exécutions | Part |
|---|---|---|
| Fermeture programmée OpenCode | 1 | 5.6 % |
| OpenSpec archive | 1 | 5.6 % |
| OpenSpec validate | 9 | 50.0 % |
| Prévol CAB | 3 | 16.7 % |
| Python compilation | 3 | 16.7 % |
| Python tests | 1 | 5.6 % |
| Total | 18 | 100 % |

| Commande (100 caractères max.) | Occurrences | Part |
|---|---|---|
| /home/devops/.local/npm/bin/openspec archive add-initial-data-deletion-strategy-vocabulary --yes --… | 1 | 5.6 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json --report findings | 2 | 11.1 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json --report findings | 2 | 11.1 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-data-deletion-strategy-vocabulary --strict | 3 | 16.7 % |
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --type spec --strict | 2 | 11.1 % |
| /home/devops/python/current/bin/python3 -B -c '(lambda p: (lambda u,e,t: (lambda w: (lambda x: prin… | 1 | 5.6 % |
| /home/devops/python/current/bin/python3 -B -c '__import__("sys").path.insert(0,"src") or __import__… | 1 | 5.6 % |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_deletion_strategies.py | 1 | 5.6 % |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_deletion_strategi… | 1 | 5.6 % |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_deletion_strategies.py | 1 | 5.6 % |
| /usr/bin/true | 3 | 16.7 % |
| Total | 18 | 100 % |

Commande de temporisateur REJECTED avant exécution (une décision, aucun Bash exécuté) : /home/devops/python/current/bin/python3 -B -c 'exec("import os,json,subprocess,sys\nfrom pathlib im…. Codes natifs : quatre diagnostics globaux exit 1 qualifiés exactement 19 WARNING préexistants/0 ERROR (76 capacités, 77 items avec change), jamais convertis en succès CLI ; toutes les autres commandes exit 0. Archive : specsUpdated=false, +0/~0/-0/→0.

## 5. Accès web

| Type | Total | Part | Terminés | Refus | Erreurs |
|---|---|---|---|---|---|
| Web | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web demandé ou visité par l’agent : zéro URL approuvée, refusée ou en erreur. Les appels HTTP locaux de pilotage, décisions CAB et probes sont séparés des outils web ; quotas/benchmark externes de préconditions hors intervalle.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — sélection native | 2026-10-07T03:39:09.917000+00:00 |
| Fin — après archive et sondes finales | 2026-10-07T04:43:42.272167+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 04 min 32 s |

Intervalle de production natif : 2026-10-07T03:39:09.917000+00:00 à 2026-10-07T04:37:55.306090+00:00 ; collecte totale se termine après sondes finales, avant rédaction du rapport.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage de la spécification | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil mcp__codex_app__get_usage_limits non exposé : aucun relevé ni différence reconstitués, aucune substitution Spark/profil/PLLM. Les quotas sont partagés par le compte ; aucune consommation exclusive n’est attribuée à ce change.

| Domaine | Total | Part globale | Terminés | Refus | Erreurs |
|---|---|---|---|---|---|
| Fichiers | 9 | 10.3 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 18 | 20.7 % | 18 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 60 | 69.0 % | 57 (95.0 %) | 0 (0.0 %) | 3 (5.0 %) |
| Total global | 87 | 100 % | 84 (96.6 %) | 0 (0.0 %) | 3 (3.4 %) |

Résultat : vocabulaire déclaratif des stratégies de suppression livré, 17/17 tests et 3/3 compilations réussis, six tâches prouvées ; stricts ciblés avant/après/final exit 0 ; quatre diagnostics globaux qualifiés sans finding nouveau ; archive native exit 0 et hashes conservés. La purge, la suppression, les transitions et la restauration ne sont pas implémentées par cette unité. Git non inspecté ni modifié ; aucune opération DB/PG, aucun secret lu ou transmis dans ce cycle ; aucun accès web de l’agent. La publication de ce rapport est un mandat séparé, exclu des comptes ci-dessus.
