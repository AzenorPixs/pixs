# STATISTIQUES — add-p0-developer-kit-validators

Session persistante : `ses_f1120eca1ffenF5n37NcrleooA`. RUN : `cismp-pixs-20260929-2033`. Racine : `/home/devops/datas/pixs`. Intervalle fermé : 2026-09-29T23:32:57.357340+00:00 à 2026-09-30T00:08:18.057289+00:00 (UTC), après archivage et sonde finale, avant rédaction. Historique natif complet filtré sur messages créés ou terminés dans ces bornes. Les travaux précédents, la rédaction de ce rapport et la réconciliation recovery03 après la borne sont exclus des agrégats. Les compteurs décrivent OpenCode ; ceux de Codex ne sont pas exposés.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | opencode-go | MEDIUM vérifié | 9.006 s | 222.055 | N/A — durée active complète non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version exacte non exposée | OpenAI | MEDIUM demandé ; télémétrie N/A | N/A | N/A | N/A |

Le temps calendaire, les attentes et les outils ne sont pas du temps de génération. Aucun dénominateur fiable de service cumulé n'est exposé : durées actives, parts et chevauchements restent N/A. La version exacte n'est pas déduite de l'identifiant modèle.

## 1. Statistiques générales et décisions

La durée calendaire est 35.345 minutes (2120.700 secondes), pauses et attentes incluses.

| Mesure | Effectif | Part ou taux |
|---|---:|---:|
| Messages | 138 | 100 % |
| Appels d'outils natifs | 87 | 100 % |
| Outils réussis | 84 | 96.6 % |
| Outils refusés | 1 | 1.1 % |
| Outils en erreur | 2 | 2.3 % |
| Mandats CAB | 28 | 100 % |
| Mandats APPROVED | 27 | 96.4 % |
| Mandats REJECTED | 1 | 3.6 % |
| Opérations d'écriture approuvées et exécutées | 15 | 55.6 % des mandats approuvés |
| Commandes approuvées et exécutées | 12 | 44.4 % des mandats approuvés |
| Compactions | 0 | 0,0 % des messages |

Convention : un outil terminé sans erreur ni code non nul est « réussi ». Cela ne prouve pas une approbation manuelle pour les lectures natives. Une réponse CAB REJECTED compte comme refus, sans exécution de sa cible. Une commande approuvée avec code 1 compte comme erreur technique/test, jamais comme refus. Les 27 mandats approuvés correspondent à 15 écritures et 12 commandes ; ces 12 commandes comprennent un test échoué et 11 réussites.

Erreurs conservées : lecture pré-création de `proposal.md` introuvable (`msg_0ef84e5d7001DfHq0PL0082lA7`), sans effet sur fichier ensuite créé, relu, validé et archivé ; test TOML 18/19, code 1 (`msg_0ef915432001Jd0Uamc2H1ZAe9`), corrigé dans validators03 puis 19/19 avec tests inchangés. Refus : AST01, commande soumise avec échappements différents du mandat ; aucun Bash lancé. Recovery01 et recovery02 rétablissent le test CAB avec `/usr/bin/true`, exit 0 et READY sans attente. La lecture manquante a été explicitement réconciliée par recovery03 après les bornes, exit 0 et READY pending0 à 00:09:50Z (`msg_0efa563c5001314mDGvN3R0e1T`) ; cette récupération et la publication statistique sont exclues des totaux.

| Compteur de tokens | Tokens | Part du total |
|---|---:|---:|
| input | 467739 | 3.3 % |
| output | 37376 | 0.3 % |
| reasoning | 14144 | 0.1 % |
| cache_read | 13554092 | 96.3 % |
| cache_write | 0 | 0.0 % |
| Total (somme des compteurs natifs) | 14073351 | 100 % |

Coût natif déclaré cumulé : 0.084186084 sur 110 réponses assistant (100.0 %). Devise, tarif de facturation et équivalence monétaire : N/A ; aucune conversion inventée. Les sondes jetables sont exclues de ces compteurs de production.

Résultats du périmètre : 19/19 tests unitaires ciblés (100 %), 7/7 intégration ciblée (100 %), régressions globales 380/380 unitaires et 125/125 intégration (100 %). Quatre AST Python valides, dix fichiers UTF-8/LF, deux requirements delta identiques aux canoniques, imports noyau via racines publiques ; OpenSpec global strict 77/77 valides (100 %), 0 invalide, 14 INFO non bloquantes préexistantes. Dix tâches cochées sur preuves, zéro restante. Validateurs locaux uniquement : le DeveloperKit complet, P0 global, runtime et audit durable ne sont pas prouvés.

## 2. Types de messages et d'outils

| Rôle | Messages | Part |
|---|---:|---:|
| user | 28 | 20.3 % |
| assistant | 110 | 79.7 % |
| Total | 138 | 100 % |

| Type de partie | Parties | Part |
|---|---:|---:|
| text | 56 | 10.6 % |
| step-start | 110 | 20.9 % |
| reasoning | 164 | 31.1 % |
| tool | 87 | 16.5 % |
| step-finish | 110 | 20.9 % |
| Total | 527 | 100 % |

| Terminaison assistant | Réponses | Part |
|---|---:|---:|
| tool-calls | 82 | 74.5 % |
| stop | 28 | 25.5 % |
| Total | 110 | 100 % |

| Outil | Appels (part) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 5 (5.7 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 28 (32.2 %) | 27 (96.4 %) | 1 (3.6 %) | 0 (0.0 %) |
| bash | 12 (13.8 %) | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |
| read | 21 (24.1 %) | 20 (95.2 %) | 0 (0.0 %) | 1 (4.8 %) |
| write | 13 (14.9 %) | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 2 (2.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 3 (3.4 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 2 (2.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 1 (1.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 87 (100.0 %) | 84 (96.6 %) | 1 (1.1 %) | 2 (2.3 %) |

### Sondes de performance hors production

Prompt constant, sans outil/fichier/réseau : « Sans outil, fichier ni réseau. Réponds uniquement avec exactement 64 lignes identiques, chacune contenant : alpha beta gamma delta epsilon zeta eta theta. Aucun commentaire, aucune numérotation. » Même modèle, fournisseur et MEDIUM dans trois sessions dédiées jetables supprimées après mesure. Version exacte N/A (non exposée). TTMT mesuré jusqu'au premier delta SSE textuel non vide ; débit fondé sur les tokens de sortie natifs divisés par la durée premier–dernier delta, pas sur le nombre de fragments.

| Position | Envoi UTC | Message de preuve | Tokens sortie | TTMT (s) | Durée sortie (s) | Tokens/s | État |
|---|---|---|---:|---:|---:|---:|---|
| début | 2026-09-29T23:32:57.367903+00:00 | `msg_0ef83a5a1001Y7tRpAHafF9edz` | 585 | 2.658693 | 1.326789 | 440.914114 | Réussie, 0 outil |
| +30 minutes | 2026-09-30T00:03:04.816242+00:00 | `msg_0ef9f39fb001isGveBnufu3dmY` | 585 | 17.508920 | 3.011522 | 194.253908 | Réussie, 0 outil |
| fin | 2026-09-30T00:06:43.764379+00:00 | `msg_0efa29140001D04I6uk4vx0qVt` | 603 | 6.849399 | 19.453941 | 30.996290 | Réussie, 0 outil |

Sondes prévues 3 (début, +30 min, fin), réussies 3 (100 %), échouées 0 (0,0 %), manquées 0 (0,0 %). La relève +30 min est envoyée environ 7,4 secondes après la cadence initiale, délai conservé et non recréé rétroactivement. TTMT moyen 9.005670 s, min 2.658693, max 17.508920. Débit moyen arithmétique 222.054771 tokens/s, min 30.996290, max 440.914114.

Surcharge distincte : 1773 tokens de sortie, 50.809264 s cumulées envoi–dernier delta. Tokens d'entrée, cache, raisonnement et coût des sondes N/A (non conservés dans le relevé). Cette durée n'est pas le temps de service de l'agent. Codex orchestrateur n'a pas été sondé.

## 3. Fichiers modifiés

Les nombres sont des tentatives natives d'écriture/edit, pas des lignes changées. Neuf chemins distincts, quinze écritures approuvées et réussies. La création générateur de `.openspec.yaml` et le déplacement par archive relèvent des commandes, pas d'un outil d'écriture séparé.

| Chemin absolu avant archivage | Écritures (part) | Réussies (taux) | Refusées (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| `/home/devops/datas/pixs/openspec/changes/add-p0-developer-kit-validators/proposal.md` | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/openspec/changes/add-p0-developer-kit-validators/design.md` | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/openspec/changes/add-p0-developer-kit-validators/tasks.md` | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/openspec/changes/add-p0-developer-kit-validators/specs/developer-experience/spec.md` | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/src/pixs/developer_kit/validators.py` | 3 (20.0 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/src/pixs/developer_kit/__init__.py` | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/src/pixs/developer_kit/README.md` | 1 (6.7 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/tests/unit/test_developer_kit_validators.py` | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| `/home/devops/datas/pixs/tests/integration/test_developer_kit_example.py` | 2 (13.3 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 15 (100 %) | 15 (100 %) | 0 (0,0 %) | 0 (0,0 %) |

Les artefacts du change et `.openspec.yaml` ont été déplacés par l'archivage autorisé vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-developer-kit-validators/`. Les cinq fichiers code/tests/documentation restent en place. Les 49 fichiers ciblés des fondations, exemple et cadrages contrôlés par SHA-256 sont inchangés ; aucune inspection Git. `output/cismp-state.json` relève de l'orchestrateur et n'entre pas dans les outils natifs de codage. Le présent STATISTIQUES.md, post-bornes, est exclu.

## 4. Commandes

Douze appels Bash effectifs ; le mandat AST01 refusé n'est pas un appel Bash. Pourcentages sur les douze exécutions, résultats sur chaque famille.

| Famille | Exécutions (part) | Réussies (taux) | Refusées (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| OpenSpec | 5 (41.7 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 5 (41.7 %) | 4 (80.0 %) | 0 (0.0 %) | 1 (20.0 %) |
| CAB true | 2 (16.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 (100.0 %) | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |

| Libellé de commande (100 caractères maximum) | Occurrences (part) | Résultats observés |
|---|---:|---|
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec new change add-p0-developer-…` | 1 (8.3 %) | exit 0 |
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate add-p0-developer-ki…` | 1 (8.3 %) | exit 0 |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test…` | 2 (16.7 %) | exit 1, exit 0 |
| `/usr/bin/true` | 2 (16.7 %) | exit 0, exit 0 |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test…` | 1 (8.3 %) | exit 0 |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test…` | 1 (8.3 %) | exit 0 |
| `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s test…` | 1 (8.3 %) | exit 0 |
| `/home/devops/python/current/bin/python3 -B -c 'import ast,pathlib,re,json files=["openspec/changes/…` | 1 (8.3 %) | exit 0 |
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate --all --strict` | 1 (8.3 %) | exit 0 |
| `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec archive add-p0-developer-kit…` | 1 (8.3 %) | exit 0 |

### Commandes refusées regroupées

| Mandat refusé | Libellé (100 caractères maximum) | Occurrences |
|---|---|---:|
| `cismp-pixs-20260929-kit-ast01` | `/home/devops/python/current/bin/python3 -B -c 'import ast,pathlib,re,json files=["openspec/changes/…` | 1 (100 % des refus de commande) |

Cette commande a été soumise mais jamais exécutée, échappements non strictement identiques au mandat original. Commandes ciblées par CAB : 13 (100 %), dont 12 approuvées/exécutées (92.3 %) et 1 refusée (7.7 %). Ne pas additionner ces intentions aux douze appels Bash.

Preuves : unittest02 `msg_0ef9412f00011nmCF2aqixx2gH` (19 OK), intégration ciblée `msg_0ef970b85001kY7TVud8wiahOu` (7 OK), global unit `msg_0ef97b562001M1kz401KCXrHy6` (380 OK), global intégration `msg_0ef987601001hG4tOyIEkl86JK` (125 OK), AST02 `msg_0ef9bf05e0017B8tQqQSSW4Hig` (4/10/delta exact), OpenSpec strict `msg_0ef9cd139001pgi8vQJyTL61px` (77/0), archivage report `msg_0efa1f4f7001Jk43vMIyPoowGY` (exit 0), tasks report `msg_0efa0be8f001sxukkSbQ1ReuZY` (10 cochées).

## 5. Accès web

| Accès web natifs | Total (part) | Approuvés/réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Aucun outil web observé | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucune URL externe visitée, aucun accès web refusé ni requête de recherche native dans ces bornes. Les échanges locaux de pilotage HTTP/SSE OpenCode et CAB ne sont pas assimilés à des visites web de l'agent ; leur volume Codex n'est pas exposé (N/A). Ils ne changent pas les zéros du tableau.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-29T23:32:57.357340+00:00 (UTC) |
| Fin — après archivage et sonde finale | 2026-09-30T00:08:18.057289+00:00 (UTC) |
| Durée globale (pauses et attentes incluses) | 00 h 35 min 20,700 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-09-29T23:32:57.357340+00:00 (UTC) | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-09-30T00:08:18.057289+00:00 (UTC) | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — relevés indisponibles | — |

Inventaire des outils natifs vérifié avant les travaux et après archivage : `mcp__codex_app__get_usage_limits` absent. Aucun ancien quota, secret ou compteur de fournisseur substitué. Les quotas Codex sont partagés par le compte et peuvent inclure d'autres tâches ; aucune variation n'est attribuée exclusivement à ce change.

| Domaine | Appels (part globale) | Réussis (taux) | Refusés (taux) | Erreurs (taux) |
|---|---:|---:|---:|---:|
| Écritures fichiers | 15 (17.2 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes Bash | 12 (13.8 %) | 11 (91.7 %) | 0 (0.0 %) | 1 (8.3 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils (lectures et CAB compris) | 60 (69.0 %) | 58 (96.7 %) | 1 (1.7 %) | 1 (1.7 %) |
| Total | 87 (100.0 %) | 84 (96.6 %) | 1 (1.1 %) | 2 (2.3 %) |

Totaux croisés : quinze écritures + douze commandes + zéro web + soixante autres outils = 87 ; 84 réussites + un refus + deux erreurs = 87. Neuf chemins écrits ; 28 mandats CAB, 27 APPROVED et un REJECTED. Les 110 réponses assistant et 28 messages utilisateur font 138 messages, 527 parties.

État : cinq fichiers d'implémentation/tests/documentation, dix tâches prouvées, 505 tests globaux réussis (100 %), OpenSpec 77/0, archivage unique autorisé et vérifié à `2026-09-30-add-p0-developer-kit-validators`, aucun change actif observé après archivage. Git non inspecté ni modifié ; aucun outil web, secret réel ni source exclue observé dans ce périmètre. La publication statistique reste une opération post-bornes séparée. Les validateurs locaux ne prouvent ni le Kit complet, ni P0 global, ni runtime/persistance/audit durable. Le cycle CISMP doit reprendre la sélection, sans état TERMINÉ déduit de cette archive.
