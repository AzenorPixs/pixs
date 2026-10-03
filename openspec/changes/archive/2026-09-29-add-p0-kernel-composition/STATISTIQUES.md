# Statistiques — add-p0-kernel-composition

RUN `cismp-pixs-20260928-1548`. Archive effective : `openspec/changes/archive/2026-09-29-add-p0-kernel-composition`. Arrêt demandé après ce seul change.

Extraction native : 2026-09-29T08:59:12.039231+00:00 (UTC). Les trois historiques sont complets jusqu’à cette borne, sans pagination résiduelle ni outil en attente.

Sources : historique natif OpenCode complet des trois sessions ci-dessous, agrégé par identifiant sans copier les messages ni les parties de raisonnement. Le relevé couvre la production jusqu’au rapport d’archivage ; la rédaction de ce fichier et la clôture CAB ultérieure sont hors compteur. Les huit sessions de sonde sont comptées séparément. Les anciennes sessions antérieures au RUN du 28 septembre ne sont pas agrégées.

| Session OpenCode | Messages | Part des messages |
| --- | --- | --- |
| ses_f1431bd60ffeGZj7lfdkhLprB6 | 464 | 99,1 % |
| ses_f174befe7ffeNK2URyJT9P3e5h | 2 | 0,4 % |
| ses_f174b061effejo3dledpG9FWsJ | 2 | 0,4 % |

L’API Codex `read_thread` a été paginée jusqu’à `hasMore=false`, mais ses items restent tronqués : les totaux exhaustifs de messages, outils et tokens de l’orchestrateur sont **N/A**. Les totaux ci-dessous sont donc ceux d’OpenCode, pas ceux de tous les agents réunis. État orchestrateur : `/home/devops/datas/pixs/output/cismp-state.json`.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3.8-flash | N/A | opencode-go | low | N/A | N/A | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | low | N/A | N/A | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | N/A | N/A | N/A | N/A |

Les modèles et niveaux proviennent des métadonnées natives ; la version exacte n’est pas déduite du nom. Une réponse Muse ne renseigne pas sa variante. La configuration finale est Muse / opencode-go / low, PLLM mode 2. Les sondes Qwen n’étaient pas activées. Aucune sonde Muse valide : moyennes, minimum et maximum N/A. Les durées de génération actives ne sont pas fournies ; le dénominateur du temps de service est N/A. Aucune durée d’attente, de permission ou d’outil n’est assimilée à de la génération.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex (famille GPT-6 déclarée par la session) | N/A | OpenAI | N/A | N/A | N/A | N/A |

Aucune sonde de l’orchestrateur. Des activités et sondes ont pu se chevaucher ; aucun temps de service n’est extrapolé.

## 1. Statistiques générales et décisions

Durée observable du RUN : **17 h 11 min 55 s**, pauses nocturnes, attentes et tests inclus. Borne initiale : première session native du RUN ; les éventuelles préconditions Codex antérieures à cette borne ne sont pas mesurables ici.

| Périmètre | Tentatives (% tableau) | Approuvé/exécuté (% ligne) | Refusé (% ligne) | Erreur (% ligne) |
| --- | --- | --- | --- | --- |
| Tous les outils OpenCode | 356 (100,0 %) | 348 (97,8 %) | 2 (0,6 %) | 6 (1,7 %) |
| TOTAL | 356 (100,0 %) | 348 (97,8 %) | 2 (0,6 %) | 6 (1,7 %) |

Convention : « approuvé/exécuté » désigne un appel terminé avec succès, autorisé automatiquement ou manuellement ; un succès ne prouve pas une approbation manuelle. « Refusé » exige un refus de permission natif explicite. « Erreur » regroupe les interruptions/erreurs d’outil et les validations en échec, détaillées ci-dessous. Les arrondis à une décimale peuvent ne pas sommer exactement à 100 %.

| Décisions CAB uniques observées | Nombre | Part |
| --- | --- | --- |
| APPROVED | 78 | 100,0 % |
| Total | 78 | 100 % |

Les deux refus natifs sont distincts des décisions CAB : une seconde édition hors mandat consommé et une commande Python sans mandat. Ils n’ont pas été exécutés. Les six erreurs comprennent deux délais de request_validation, un délai de poll_approval, une lecture de chemin absent, une écriture avortée et un échec de validation unitaire (199 tests, deux erreurs), corrigé puis rejoué avec succès. Les incidents restent visibles ; aucune réussite n’est substituée rétroactivement à un échec.

| Tokens de production (compteurs natifs) | Nombre | Part |
| --- | --- | --- |
| entrée | 929961 | 1,9 % |
| sortie | 186155 | 0,4 % |
| raisonnement | 62549 | 0,1 % |
| cache lu | 48627291 | 97,5 % |
| cache écrit | 53025 | 0,1 % |
| Total | 49858981 | 100 % |

Total natif `tokens.total` : 49858981, égal à la somme des cinq catégories. Valeur native `cost` cumulée : 0.252752788 ; unité monétaire et facturation effective non vérifiées, aucune conversion en euros. Marqueurs de compaction natifs : 1 (télémétrie de parties, distincte des compactions Codex indisponibles).

| Validation finale | Réussis / total | Taux | Preuve native |
| --- | --- | --- | --- |
| Unitaires | 199 / 199 | 100 % | msg_0ec4cc7e1001UgVIudKpXmqtOW |
| Intégration | 77 / 77 | 100 % | msg_0ec5accf5001aUhesQWqcCVH3V |
| Total tests | 276 / 276 | 100 % | Deux suites finales, exit 0 |
| OpenSpec strict | 77 / 77 | 100 % | msg_0ec6145d5001mSJ1RbbbUVdzFe |
| Tâches | 24 / 24 | 100 % | Archive relue, zéro tâche ouverte |
| Encodage / syntaxe | 33 / 33 | 100 % | msg_0ec5d5aa3001LpEzRuKtA1bUvg |
| Compilation | 1 / 1 | 100 % | msg_0ec5cb209001m2HsHLgcRyJj3F |

Sondes : collecte tardive. Initiale et relèves antérieures : **N/A — sondes périodiques non activées** ; leur nombre exact n’est pas reconstruit. Après activation : quatre relèves (tardive, deux périodiques, finale), huit tentatives avec une seule reprise par relève ; 0/4 relèves réussies (0,0 %), 4/4 échouées (100 %), aucune relève prévue après activation manquée (0/4, 0,0 %). Les huit tentatives sont invalides car la sortie n’atteint pas les 200 lignes demandées. Aucune utilisation d’outil par les sondes.

| Position / session | Envoi UTC | Premier texte SSE UTC | Dernier texte SSE UTC | Tokens sortie | Lignes / 200 | TTMT brut s | Débit brut tok/s | Statut |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reprise tardive — initiale et relèves antérieures manquées / ses_f13da6692ffeuzXpT00iBwdTrd | 2026-09-29T07:51:22.244210+00:00 | 2026-09-29T07:51:27.505605+00:00 | 2026-09-29T07:51:41.707937+00:00 | 2335 | 193 | 5.261 | 164.410 | Invalide, exclue |
| reprise tardive — seconde et dernière tentative / ses_f13d9e1baffeT7djE5iWW1Ghp5 | 2026-09-29T07:51:56.264805+00:00 | 2026-09-29T07:51:59.544314+00:00 | 2026-09-29T07:52:09.903280+00:00 | 2301 | 191 | 3.280 | 222.126 | Invalide, exclue |
| +30 min après activation tardive / ses_f13be032effeasM1NVrDILUPZQ | 2026-09-29T08:22:22.709563+00:00 | 2026-09-29T08:22:27.383557+00:00 | 2026-09-29T08:22:38.865726+00:00 | 2340 | 193 | 4.674 | 203.794 | Invalide, exclue |
| +30 min après activation tardive — unique nouvelle tentative / ses_f13bd2b49ffecbGxnHOFwYQX3Y | 2026-09-29T08:23:17.958868+00:00 | 2026-09-29T08:23:20.876927+00:00 | 2026-09-29T08:23:32.417933+00:00 | 2325 | 193 | 2.918 | 201.456 | Invalide, exclue |
| +60 min après activation tardive / ses_f13a13f3cffe7KPWQ3XGBL5JCj | 2026-09-29T08:53:47.866849+00:00 | 2026-09-29T08:53:50.708170+00:00 | 2026-09-29T08:53:59.145424+00:00 | 2325 | 193 | 2.841 | 275.564 | Invalide, exclue |
| +60 min après activation tardive — unique nouvelle tentative / ses_f13a0b9f0ffex8QN1MyBkJQGHe | 2026-09-29T08:54:21.988068+00:00 | 2026-09-29T08:54:23.816161+00:00 | 2026-09-29T08:54:34.357041+00:00 | 2325 | 193 | 1.828 | 220.570 | Invalide, exclue |
| fin — après archivage effectif / ses_f139c79e5ffeY1s06317oyyaXv | 2026-09-29T08:59:00.528733+00:00 | 2026-09-29T08:59:06.909452+00:00 | 2026-09-29T08:59:21.675015+00:00 | 2370 | 193 | 6.381 | 160.509 | Invalide, exclue |
| fin — unique nouvelle tentative après archivage / ses_f139bc36dffe147MFIUGNzy0uW | 2026-09-29T08:59:47.233877+00:00 | 2026-09-29T08:59:48.902015+00:00 | 2026-09-29T08:59:58.966992+00:00 | 2325 | 193 | 1.668 | 230.999 | Invalide, exclue |
| 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_manifest_models.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| N/A — écriture avortée avant paramètres | 1 (1,8 %) | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) |
| /home/devops/datas/pixs/tests/unit/test_manifest_schema1.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/registry/requirements.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/registry/registries.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_registries.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_required_versions.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/conformity.py | 2 (3,6 %) | 2 (100,0 %) | 0 (
Surcharge de télémétrie séparée : 8 tentatives (100 %), 87548 tokens natifs dont 18646 de sortie, durée cumulée des requêtes 121.482 s (pas un temps de génération), coût natif 0.009771420. Prompt constant, conservé dans l’état du RUN :

> Sonde de télémétrie purement textuelle. N'utilise aucun outil, ne lis et ne modifie aucun fichier, aucun accès réseau. Sans introduction, conclusion ni raisonnement explicatif, écris exactement 200 lignes. Chaque ligne contient : alpha beta gamma delta epsilon zeta eta theta iota kappa. Répète cette ligne identique 200 fois.

## 2. Types de messages et d’outils

| Rôle du message | Nombre | Part |
| --- | --- | --- |
| user | 80 | 17,1 % |
| assistant | 388 | 82,9 % |
| Total | 468 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 175 | 9,1 % |
| step-start | 386 | 20,0 % |
| reasoning | 626 | 32,5 % |
| tool | 356 | 18,5 % |
| step-finish | 385 | 20,0 % |
| compaction | 1 | 0,1 % |
| Total | 1929 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 308 | 79,4 % |
| stop | 77 | 19,8 % |
| absent | 3 | 0,8 % |
| Total | 388 | 100 % |

| Configuration native (modèle | fournisseur | variante) | Nombre | Part |
| --- | --- | --- |
| qwen3.8-flash\|opencode-go\|low | 8 | 2,1 % |
| muse-spark-1.3-contributor\|opencode-go\|low | 379 | 97,7 % |
| muse-spark-1.3-contributor\|opencode-go\|N/A | 1 | 0,3 % |
| Total | 388 | 100 % |

| Outil | Tentatives (% tableau) | Approuvé/exécuté (% ligne) | Refusé (% ligne) | Erreur (% ligne) |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 25 (7,0 %) | 25 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 78 (21,9 %) | 76 (97,4 %) | 0 (0,0 %) | 2 (2,6 %) |
| bash | 24 (6,7 %) | 22 (91,7 %) | 1 (4,2 %) | 1 (4,2 %) |
| cgpt-validation_get_approval | 9 (2,5 %) | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 3 (0,8 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 107 (30,1 %) | 106 (99,1 %) | 0 (0,0 %) | 1 (0,9 %) |
| glob | 11 (3,1 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| grep | 40 (11,2 %) | 40 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 38 (10,7 %) | 37 (97,4 %) | 0 (0,0 %) | 1 (2,6 %) |
| edit | 18 (5,1 %) | 17 (94,4 %) | 1 (5,6 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 3 (0,8 %) | 2 (66,7 %) | 0 (0,0 %) | 1 (33,3 %) |
| TOTAL | 356 (100,0 %) | 348 (97,8 %) | 2 (0,6 %) | 6 (1,7 %) |

## 3. Fichiers modifiés

Nombre de **tentatives** d’écriture natives, pas nombre de lignes ni nombre de modifications fonctionnelles. 32 chemins identifiés ; une écriture avortée avant paramètres n’a pas de chemin enregistré. Le chemin indisponible n’est pas compté comme fichier créé.

| Chemin absolu au moment de l’opération | Tentatives (% tableau) | Approuvé/exécuté (% ligne) | Refusé (% ligne) | Erreur (% ligne) |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/tests/integration/test_ambiguity_and_cycles.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/component-model/spec.md | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/dependencies/spec.md | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/capabilities/spec.md | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/specs/compatibility/spec.md | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-kernel-composition/design.md | 4 (7,1 %) | 3 (75,0 %) | 1 (25,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-kernel-composition/tasks.md | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/TECHNICAL.md | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/manifest/semver.py | 3 (5,4 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_semver_constraints.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/manifest/models.py | 3 (5,4 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_manifest_models.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| N/A — écriture avortée avant paramètres | 1 (1,8 %) | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) |
| /home/devops/datas/pixs/tests/unit/test_manifest_schema1.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/registry/requirements.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/registry/registries.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_registries.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_required_versions.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/conformity.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_conformity_attestations.py | 3 (5,4 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/composition.py | 4 (7,1 %) | 4 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/manifest/__init__.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/conformity_fixtures.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_capability_resolution.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_diagnostics_typed.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_manifest_guards.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_no_secret_motifs.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_composition_pipeline.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_required_components.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_lifecycle_hooks.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_public_api_facades.py | 1 (1,8 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_versioned_composition.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_composition_conformity.py | 2 (3,6 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| TOTAL | 56 (100,0 %) | 54 (96,4 %) | 1 (1,8 %) | 1 (1,8 %) |

L’archivage OpenSpec est compté dans les commandes, pas comme quatre éditions : `.openspec.yaml`, `proposal.md`, `design.md` et `tasks.md` ont été déplacés de `/home/devops/datas/pixs/openspec/changes/add-p0-kernel-composition/` vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-kernel-composition/`. Aucun change suivant lancé. Les écritures de l’état orchestrateur sont hors compteurs OpenCode ; leur nombre exhaustif est N/A. Le présent rapport et le bytecode régénérable de compileall sont également hors compteur d’éditions source.

## 4. Commandes

| Famille | Tentatives (% tableau) | Approuvé/exécuté (% ligne) | Refusé (% ligne) | Erreur (% ligne) |
| --- | --- | --- | --- | --- |
| Prévol CAB | 8 (33,3 %) | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Tests unittest | 8 (33,3 %) | 7 (87,5 %) | 0 (0,0 %) | 1 (12,5 %) |
| OpenSpec | 5 (20,8 %) | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Contrôles Python | 2 (8,3 %) | 1 (50,0 %) | 1 (50,0 %) | 0 (0,0 %) |
| Compilation Python | 1 (4,2 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| TOTAL | 24 (100,0 %) | 22 (91,7 %) | 1 (4,2 %) | 1 (4,2 %) |

Toutes les commandes refusées, regroupées (libellé limité à 100 caractères ; commande exacte conservée dans l’historique natif) :

| Commande refusée | Occurrences | Part des refus | Part des tentatives Bash |
| --- | --- | --- | --- |
| python3 -c "import ast; t=ast.parse(open('/home/devops/datas/pixs/tests/unit/test_manifest_schema1.… | 1 | 100,0 % | 4,2 % |

Total refus : 1 (100 % des refus de commande ; 4,2 % des 24 tentatives Bash). Cette commande n’a pas été exécutée. L’échec unitaire exit 1 constitue une validation exécutée en échec, pas un refus d’autorisation.

## 5. Accès web

OpenCode : 0 accès web, 0 approuvé, 0 refusé, 0 erreur ; taux et parts N/A (dénominateur nul). Les appels locaux HTTP de pilotage ne sont pas assimilés à des consultations web.

| Agent / URL | Statut observé | Nombre | Part du sous-ensemble vérifiable |
| --- | --- | --- | --- |
| Codex — https://semver.org/spec/v2.0.0.html | Consultation approuvée et effectuée, référence normative | 1 | 100 % |

Ce relevé web Codex est une preuve ponctuelle conservée pendant la session ; les totaux exhaustifs Codex restent N/A. Aucun accès refusé à une URL n’est documenté dans ce sous-ensemble. Les URL affichées sont limitées à 100 caractères.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début observable | 2026-09-28T15:48:29.848Z (UTC ; première session native du RUN) |
| Fin — après archivage et sondes | 2026-09-29T09:00:25+00:00 (UTC ; vérification d’accès au quota, sans mesure disponible) |
| Durée globale (pauses et attentes incluses) | 17 h 11 min 55 s |

Les horodatages UTC correspondent à UTC+02:00 à Paris aux dates concernées. La rédaction du rapport et la fermeture CAB suivent cette borne et ne sont pas incluses dans la durée de production.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — relevé initial absent | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-29T09:00:25+00:00 (vérification d’accès échouée) | N/A — get_usage_limits non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota demandé : `codex`, fenêtre `10080` minutes. Aucun quota Spark ni quota restant substitué. Les quotas sont partagés par le compte : même une différence mesurée pourrait inclure d’autres tâches ; aucune consommation n’est attribuée exclusivement à ce RUN.

| Domaine OpenCode | Tentatives (% tableau) | Approuvé/exécuté (% ligne) | Refusé (% ligne) | Erreur (% ligne) |
| --- | --- | --- | --- | --- |
| Éditions de fichiers | 56 (15,7 %) | 54 (96,4 %) | 1 (1,8 %) | 1 (1,8 %) |
| Commandes | 24 (6,7 %) | 22 (91,7 %) | 1 (4,2 %) | 1 (4,2 %) |
| Web OpenCode | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 276 (77,5 %) | 272 (98,6 %) | 0 (0,0 %) | 4 (1,4 %) |
| TOTAL | 356 (100,0 %) | 348 (97,8 %) | 2 (0,6 %) | 6 (1,7 %) |

Totaux croisés vérifiés : somme par outil = somme par domaine = 356 appels ; 348 réussis, 2 refusés, 6 erreurs. Les sous-totaux fichiers (56 tentatives) et commandes (24 tentatives) concordent avec leurs tableaux. Historique de production : 468 messages. Sondes : huit sessions séparées, exclues de ces totaux. Orchestrateur : totaux N/A, aucune extrapolation.

Preuves de clôture du change : 276 tests réussis, compilation exit 0, contrôle UTF-8/LF/AST réussi, OpenSpec strict 77/77, archive effective exit 0 (`msg_0ec62c069001caP28pRSLTwtwV`) et 24/24 tâches. Les INFO OpenSpec sur la longueur de certaines exigences sont non bloquants ; le change déclare `skip_specs: true` et n’a pas de delta à synchroniser. Aucun script Bash créé : bash -n/shellcheck sans objet.

Correspondance utile : schéma/versionnement → test_manifest_models, test_manifest_schema1 ; contraintes → test_semver_constraints, test_required_versions, test_versioned_composition ; conformité → test_conformity_attestations, test_composition_conformity ; registres/configuration → test_registries, test_config_resolution ; déterminisme/cycles → test_composition_topology, test_composition_pipeline, test_ambiguity_and_cycles ; façades/hooks/pureté → test_public_api_facades, test_lifecycle_hooks, test_kernel_purity ; non-divulgation → test_manifest_guards, test_no_secret_motifs. Le noyau vérifie structure et couverture des preuves fournies ; l’appelant de confiance les authentifie. Les attestations des tests restent des doubles synthétiques.

Git n’a pas été inspecté ; aucun commit ni push effectué dans ce RUN. Le contrôle de non-divulgation porte sur les artefacts synthétiques autorisés, sans ouverture des sources exclues ni de secrets réels. Les accès réseau du modèle et du pilotage ne sont pas une publication du projet. Le périmètre P0 reste limité aux dimensions connues, sans validation globale de compatibilité. La fermeture du RUN et l’arrêt CAB sont consignés après ce rapport dans l’état orchestrateur ; ce fichier ne les prétend pas déjà effectués.
