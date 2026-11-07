# STATISTIQUES — add-initial-data-retention-state-vocabulary

Session OpenCode : ses_eed633581ffeOeSPxYZNclbGnr. RUN parent : cismp-pixs-20261006-soir-R1. Archive : /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-retention-state-vocabulary.

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

Source : historique natif complet de la session, filtré du début du mandat de sélection au dernier rapport d’archive, avec bornes ci-dessous. Sondes jetables séparées ; prévol, RSMP, benchmark PLLM et rédaction/publication du présent rapport exclus de la production. Les résultats de CGPT sont limités aux décisions CAB réellement relues ; autres outils/messages orchestrateur N/A, historique natif indisponible.

Convention : « approuvé/exécuté » désigne un outil natif terminé (permission implicite de lecture ou CAB explicite selon le type), sans prouver une approbation manuelle pour les lectures. Un outil Bash terminé et un code CLI 1 qualifié ne constituent pas une validation CLI réussie. Refus = rejet explicite de permission ; erreur = autre échec/interruption.

| Mesure | Effectif | Part ou taux |
|---|---|---|
| Messages | 113 | 100 % |
| Outils | 70 | 100 % |
| Outils terminés | 70 | 100 % |
| Refus natifs | 0 | 0.0 % |
| Erreurs techniques | 0 | 0.0 % |
| Décisions CAB APPROVED | 23 | 100 % |
| Décisions CAB REJECTED | 0 | 0.0 % |
| Tests réussis | 17 | 100 % (17/17) |
| Compilations réussies | 3 | 100 % (3/3) |
| Tâches prouvées/cochées | 6 | 100 % (6/6) |
| Compactions natives dans intervalle | 0 | N/A — aucun cycle prévu atteint |

| Tokens natifs de production | Valeur | Part |
|---|---|---|
| input | 528 | 0.0 % |
| output | 31482 | 0.2 % |
| reasoning | 0 | 0.0 % |
| cache_read | 13667240 | 99.1 % |
| cache_write | 87175 | 0.6 % |
| Total (somme catégories) | 13786425 | 100 % |

Coût natif OpenCode : 0.250986580 USD. Cache inclus dans le total déclaré des catégories, sans estimation de coût ou de tokens orchestrateur. Le NFDOC a reçu une correction de cadrage (nouvelle exigence refusée avant écriture) ; ce refus fonctionnel n’est pas un refus CAB ni une erreur native.

| Relève | Tentative | Lignes | Outils | État |
|---|---|---|---|---|
| début-retention-vocabulary | 1 | 1 | 0 | invalide — sortie fixe non conforme |
| début-retention-vocabulary | 2 | 43 | 0 | invalide — sortie fixe non conforme |
| fin-retention-vocabulary | 1 | 45 | 0 | invalide — sortie fixe non conforme |
| fin-retention-vocabulary | 2 | 57 | 0 | invalide — sortie fixe non conforme |

Deux relèves prévues (début/fin), zéro réussie, deux échouées ; quatre tentatives invalides, zéro relève manquée. Aucun créneau +30 min atteint avant la fin du codage ; le travail n’a pas attendu ce créneau. TTMT/débit des tentatives invalides exclus des moyennes. Prompt constant de 200 lignes « alpha beta gamma delta epsilon zeta eta theta iota kappa », même configuration Qwen/OpenCode Go/xhigh, zéro outil, sessions supprimées après chaque tentative.

Surcharge de sondes séparée : 52902 tokens natifs (cache inclus), 0.009446644 USD, 165.938 s de durées natives cumulées (pas un temps de génération prouvé).

## 2. Types de messages et d’outils

| Rôle | Effectif | Part |
|---|---|---|
| assistant | 88 | 77.9 % |
| user | 25 | 22.1 % |
| Total | 113 | 100 % |

| Type de partie | Effectif | Part |
|---|---|---|
| reasoning | 88 | 22.9 % |
| step-finish | 88 | 22.9 % |
| step-start | 88 | 22.9 % |
| text | 50 | 13.0 % |
| tool | 70 | 18.2 % |
| Total | 384 | 100 % |

| Terminaison assistant | Effectif | Part |
|---|---|---|
| stop | 25 | 28.4 % |
| tool-calls | 63 | 71.6 % |
| Total | 88 | 100 % |

| Type | Total | Part | Terminés | Refus | Erreurs |
|---|---|---|---|---|---|
| bash | 14 | 20.0 % | 14 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 1 | 1.4 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 23 | 32.9 % | 23 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 2 | 2.9 % | 2 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 5 | 7.1 % | 5 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 16 | 22.9 % | 16 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 9 | 12.9 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 70 | 100 % | 70 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers modifiés

| Chemin absolu écrit | Tentatives | Part | Approuvées/exécutées | Refus | Erreurs |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-data-retention-state-vocabulary/.openspec.yaml | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-retention-state-vocabulary/design.md | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-retention-state-vocabulary/proposal.md | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-retention-state-vocabulary/specs/data-lifecycle/spec.md | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-data-retention-state-vocabulary/tasks.md | 2 | 22.2 % | 2 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_retention_states.py | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_retention_states_integration.py | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_retention_states.py | 1 | 11.1 % | 1 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 | 100 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

Tentatives d’écriture : neuf sur huit fichiers distincts (tasks.md écrit ouvert puis coché). Les cinq artefacts OpenSpec ont été déplacés par la commande d’archive vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-retention-state-vocabulary. Les trois sources restent à leurs chemins. Aucun cadrage ou spec canonique modifié dans cet intervalle ; RSMP antérieure exclue. Contrôle après archive : cinq hashes d’artefacts, trois de sources et 136 références inchangés.

## 4. Commandes

| Famille | Exécutions | Part |
|---|---|---|
| OpenSpec archive | 1 | 7.1 % |
| OpenSpec validate | 9 | 64.3 % |
| Python compilation | 3 | 21.4 % |
| Python tests | 1 | 7.1 % |
| Total | 14 | 100 % |

| Commande (100 caractères max.) | Occurrences | Part |
|---|---|---|
| /home/devops/.local/npm/bin/openspec archive add-initial-data-retention-state-vocabulary --yes --js… | 1 | 7.1 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json --report findings | 2 | 14.3 % |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json --report findings | 2 | 14.3 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-data-retention-state-vocabulary --strict | 3 | 21.4 % |
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --type spec --strict | 2 | 14.3 % |
| /home/devops/python/current/bin/python3 -B -c '__import__("sys").path.insert(0,"src") or __import__… | 1 | 7.1 % |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_retention_states.py | 1 | 7.1 % |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_retention_states_… | 1 | 7.1 % |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_retention_states.py | 1 | 7.1 % |
| Total | 14 | 100 % |

Commandes refusées : aucune (0). Codes natifs : quatre diagnostics globaux exit 1 qualifiés exactement 19 WARNING préexistants/0 ERROR (76 capacités, 77 items avec change), jamais convertis en succès CLI ; toutes les autres commandes exit 0. Archive : specsUpdated=false, +0/~0/-0/→0.

## 5. Accès web

| Type | Total | Part | Terminés | Refus | Erreurs |
|---|---|---|---|---|---|
| Web | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web demandé ou visité par l’agent : zéro URL approuvée, refusée ou en erreur. Les appels HTTP locaux de pilotage, décisions CAB et probes sont séparés des outils web ; quotas/benchmark externes de préconditions hors intervalle.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — sélection native | 2026-10-06T23:41:38.700000+00:00 |
| Fin — après archive et sondes finales | 2026-10-07T00:08:25.563656+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 26 min 46 s |

Intervalle de production natif : 2026-10-06T23:41:38.700000+00:00 à 2026-10-07T00:05:53.472838+00:00 ; collecte totale se termine après sondes finales, avant rédaction du rapport.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage de la spécification | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil mcp__codex_app__get_usage_limits non exposé : aucun relevé ni différence reconstitués, aucune substitution Spark/profil/PLLM. Les quotas sont partagés par le compte ; aucune consommation exclusive n’est attribuée à ce change.

| Domaine | Total | Part globale | Terminés | Refus | Erreurs |
|---|---|---|---|---|---|
| Fichiers | 9 | 12.9 % | 9 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 14 | 20.0 % | 14 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 47 | 67.1 % | 47 (100 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total global | 70 | 100 % | 70 (100 %) | 0 (0.0 %) | 0 (0.0 %) |

Résultat : vocabulaire partiel de rétention livré, 17/17 tests et 3/3 compilations réussis, six tâches prouvées ; stricts ciblés avant/après/final exit 0 ; quatre diagnostics globaux qualifiés sans finding nouveau ; archive native exit 0 et hashes conservés. La purge, la suppression, les transitions et la restauration ne sont pas implémentées par cette unité. Git non inspecté ni modifié ; aucune opération DB/PG, aucun secret lu ou transmis dans ce cycle ; aucun accès web de l’agent. La publication de ce rapport est un mandat séparé, exclu des comptes ci-dessus.
