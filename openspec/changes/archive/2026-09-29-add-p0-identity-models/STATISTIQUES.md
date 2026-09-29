# Statistiques — add-p0-identity-models

Session OpenCode `ses_f130e4e87ffeaY8YzgPakaCCOl`, Pixs `/home/devops/datas/pixs`, RUN `cismp-pixs-20260929-1134`.
Intervalle de production : 2026-09-29 18:43:16.041387 UTC à 2026-09-29 19:15:24.008088 UTC. Archive vérifiée : `openspec/changes/archive/2026-09-29-add-p0-identity-models`.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | opencode-go | low | 1,788 s | 416,898 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex, agent orchestrateur | N/A — identifiant exact du modèle absent de la télémétrie collectée | OpenAI | N/A | N/A — non sondé | N/A — non sondé | N/A |

Le modèle, fournisseur et variant `low` sont observés sur les 91 messages assistant de production (100 %). La version exacte ne se déduit pas du nom du modèle. Le temps de génération isolé et celui de l'orchestrateur ne sont pas disponibles : le dénominateur du temps de service cumulé est N/A. Les attentes CAB, outils et durée calendaire ne sont pas assimilés à de la génération. Les sondes dédiées sont exclues de la production ; la sonde périodique a pu chevaucher le mandat de mise à jour des tâches.

## 1. Statistiques générales et décisions

La production mesurée comprend la sélection, les artefacts, le code, les tests, les corrections, la récupération et l'archivage de ce seul change. La RSMP identité précédente, les autres changes du RUN et la rédaction de ce rapport sont hors intervalle. Les métriques d'outils proviennent de la session OpenCode ; les appels propres à l'orchestrateur ne disposent pas d'un compteur exhaustif exploitable et valent N/A.

| Mesure | Valeur |
| --- | --- |
| Durée calendaire, pauses et attentes incluses | 00 h 32 min 07 s (1 927,967 s) |
| Messages | 122 (100,0 %) |
| Appels d'outils | 65 (100,0 %) |
| Réussites techniques | 64 (98,5 %) |
| Erreurs techniques | 1 (1,5 %) |
| Refus de permission native observés | 0 (0,0 %) |
| Mandats CAB distincts | 29 (100,0 %) |
| Décisions CAB APPROVED | 28 (96,6 %) |
| Décisions CAB REJECTED | 1 (3,4 %) |
| Tâches OpenSpec prouvées | 7 (100,0 %) |
| Tests finaux réussis | 404 (100,0 %) |
| Nouveaux tests du change | 27 (6,7 %) |
| Coût natif de production, compteur API | 0.072500794 USD |
| Compactions observées pendant cet intervalle | 0 (0,0 % des 122 messages) |

Un appel terminé est compté comme « approuvé et exécuté » / réussite technique ; cela ne prouve pas une approbation manuelle pour une lecture ou un appel MCP. Un appel CAB retournant REJECTED a réussi techniquement à transporter un refus. Les 28 mandats approuvés correspondent aux 16 éditions et 12 commandes exécutées, dont une commande échouée. Aucun refus natif n'est déduit de cet échec. Le refus CAB est compté séparément et n'a déclenché aucun Bash.

| Compteur de tokens natif, agrégé sans contenu | Nombre et part |
| --- | --- |
| entrée_hors_cache | 225173 (1,0 %) |
| cache_lu | 21839147 (98,8 %) |
| cache_écrit | 0 (0,0 %) |
| sortie | 28892 (0,1 %) |
| raisonnement_compteur_seul | 2634 (0,0 %) |
| Total natif | 22095846 (100,0 %) |

La somme entrée hors cache + cache lu + cache écrit + sortie + raisonnement égale le total natif. Aucun contenu de raisonnement n'est reproduit. Le coût est celui rapporté par l'API, non une estimation tarifaire ni une mesure du quota Codex.

Sondes dédiées, sans outils ni accès projet, même prompt fixe de 64 lignes :
`Sans outil, fichier ni réseau. Réponds uniquement avec exactement 64 lignes identiques, chacune contenant : alpha beta gamma delta epsilon zeta eta theta. Aucun commentaire, aucune numérotation.`

| Position | Envoi UTC | Message preuve | Tokens sortie | TTMT s | Débit tokens/s | Résultat |
| --- | --- | --- | --- | --- | --- | --- |
| début | 2026-09-29 18:43:16.077915 UTC | `msg_0ee7a6e2c001yWuw3SEP2hnqla` | 586 | 1,574 | 397,649 | Réussie |
| +30 min | 2026-09-29 19:13:38.236406 UTC | `msg_0ee963c02001pqlWO3ADHkjOYX` | 585 | 2,143 | 421,130 | Réussie |
| fin | 2026-09-29 19:15:07.991079 UTC | `msg_0ee979aa2001QvOzfNiciFCOV7` | 585 | 1,646 | 431,915 | Réussie |

| Sondes prévues | Réussies | Échouées | Manquées |
| --- | --- | --- | --- |
| 3 (100,0 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

TTMT min–max : 1,574–2,143 s. Débit min–max : 397,649–431,915 tokens/s. Moyennes arithmétiques sur trois sondes valides. La relève +30 min a été envoyée environ 22 s après l'échéance calculée depuis l'envoi initial ; aucun relevé n'est reconstitué rétroactivement.

Surcharge exclue des totaux de production : 1 756 tokens de sortie (100 % des tokens de sortie des sondes), 9,805 s cumulées entre envoi et fin native ; tokens d'entrée et coût des sondes N/A, non conservés par le collecteur. Les sessions jetables ont été supprimées après mesure.

Incidents conservés : correction des annotations et de tests insuffisants ; correction du design/code/test pour l'unicité globale exigée par TECHNICAL §13 ; mandat `identity-ast01` refusé pour échappement divergent, non exécuté ; commande `identity-alltests01` exécutée avec exit 1 (import existant `test_pdp_decision` introuvable depuis la découverte globale). Réconciliation puis test CAB `identity-recovery01` réussi, READY pending0, et suites séparées finales réussies. La vérification CAB de reprise a eu lieu après l'échec de découverte ; elle n'avait pas été rejouée immédiatement après le refus AST, écart de cadence de récupération signalé. Les sources n'ont pas été modifiées pour contourner l'import existant.

## 2. Types de messages et d'outils

| Rôle | Nombre et part |
| --- | --- |
| user | 31 (25,4 %) |
| assistant | 91 (74,6 %) |
| Total | 122 (100,0 %) |

| Type de partie, métadonnées seulement | Nombre et part |
| --- | --- |
| text | 61 (14,8 %) |
| step-start | 91 (22,1 %) |
| reasoning | 103 (25,1 %) |
| tool | 65 (15,8 %) |
| step-finish | 91 (22,1 %) |
| Total | 411 (100,0 %) |

| Terminaison assistant | Nombre et part |
| --- | --- |
| tool-calls | 61 (67,0 %) |
| stop | 30 (33,0 %) |
| Total | 91 (100,0 %) |

| Outil | Nombre (% outils) | Approuvé/exécuté techniquement | Refus natif | Erreur |
| --- | --- | --- | --- | --- |
| read | 5 (7,7 %) | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_request_validation | 29 (44,6 %) | 29 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| write | 15 (23,1 %) | 15 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| bash | 12 (18,5 %) | 11 (91,7 %) | 0 (0,0 %) | 1 (8,3 %) |
| edit | 1 (1,5 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 2 (3,1 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 1 (1,5 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 65 (100,0 %) | 64 (98,5 %) | 0 (0,0 %) | 1 (1,5 %) |

Aucune erreur de message ni interruption/compaction observée dans cet intervalle. L'unique erreur technique est le Bash de découverte globale, preuve `msg_0ee8fee31001bZo0nzOOTc9Dz6`, exit 1. Les autres 64 appels ont terminé avec succès technique.

## 3. Fichiers modifiés

Les nombres comptent les opérations d'édition, pas les lignes modifiées. Les quatre artefacts OpenSpec sont présentés à leur emplacement actuel après archivage ; leurs écritures ont eu lieu dans le répertoire actif du change, avant le déplacement autorisé.

| Chemin absolu complet | Écritures (% éditions) | Approuvées/exécutées | Refusées | En erreur |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-identity-models/proposal.md | 1 (6,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-identity-models/design.md | 2 (12,5 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-identity-models/tasks.md | 2 (12,5 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-identity-models/.openspec.yaml | 1 (6,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/models.py | 3 (18,8 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/__init__.py | 1 (6,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/__init__.py | 1 (6,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_identity_models.py | 2 (12,5 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_identity_links.py | 2 (12,5 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_identity_facade.py | 1 (6,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total : 10 fichiers | 16 (100,0 %) | 16 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Seize éditions approuvées sur dix fichiers ; le déplacement des quatre artefacts par OpenSpec est une commande d'archivage, pas quatre nouvelles éditions. `STATISTIQUES.md` est produit sous un mandat distinct après cet intervalle et ne s'inclut pas dans son propre décompte. Contrôle de périmètre par historique des outils et réconciliation des contenus autorisés ; aucun recours à Git.

## 4. Commandes

Libellés descriptifs limités à 100 caractères ; les commandes exactes restent dans la session et les mandats corrélés. Exécutables absolus DEVOPS, Python avec `-B`, télémétrie OpenSpec désactivée.

| Famille / libellé | Occurrences (% commandes exécutées) | Réussites | Refus natif | Erreurs |
| --- | --- | --- | --- | --- |
| OpenSpec validate --all --strict | 3 (25,0 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B unittest discover -s tests/unit -v | 2 (16,7 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B unittest discover -s tests/integration -v | 2 (16,7 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B unittest discover -s tests/unit -v | 2 (16,7 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B unittest discover -s tests -v | 1 (8,3 %) | 0 (0,0 %) | 0 (0,0 %) | 1 (100,0 %) |
| /usr/bin/true | 1 (8,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| OpenSpec archive add-p0-identity-models --yes --skip-specs --json | 1 (8,3 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 12 (100,0 %) | 11 (91,7 %) | 0 (0,0 %) | 1 (8,3 %) |

| Demande de commande refusée CAB, non exécutée | Occurrences (% refus CAB) | Résultat |
| --- | --- | --- |
| Contrôle AST/UTF-8/LF avec échappement divergent — identity-ast01 | 1 (100,0 %) | REJECTED ; aucun Bash |

Ce refus de mandat est déjà inclus dans les 29 décisions CAB ; il n'est pas ajouté aux 12 Bash. La découverte globale a exécuté 390 cas, dont 389 réussis (99,7 %) et un échec de chargement (0,3 %) ; elle n'est pas considérée comme la suite finale. Les suites finales séparées ont prouvé 304 unités + 100 intégrations, tous réussis.

## 5. Accès web

| Domaine | Appels et part des 65 outils | Approuvés | Refusés | Erreurs |
| --- | --- | --- | --- | --- |
| Web | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web ni URL consultée/refusée dans la session de codage. Dénominateur des taux web nul : N/A. Le transport local HTTP/SSE d'OpenCode et CAB sert au pilotage et n'est pas une consultation web externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-09-29 18:43:16.041387 UTC |
| Fin — après archivage et sonde finale | 2026-09-29 19:15:24.008088 UTC |
| Durée globale (pauses et attentes incluses) | 00 h 32 min 07 s (1 927,967 s) |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-09-29 18:43:16.041411 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-29 19:15:24.008088 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

L'outil natif `mcp__codex_app__get_usage_limits` n'était exposé à aucune des deux bornes : aucune lecture de quota `codex` fenêtre 10080 minutes n'a pu être effectuée. Les horodatages indiquent le constat d'indisponibilité, pas une mesure réussie. La comparaison et la réinitialisation sont N/A. Les quotas sont partagés par le compte ; même disponibles, leur variation pourrait inclure d'autres tâches simultanées. Aucune conversion en tokens ou en euros.

| Domaine | Total (% des outils) | Approuvés/exécutés techniquement | Refus natif | Erreurs |
| --- | --- | --- | --- | --- |
| autres | 37 (56,9 %) | 37 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| fichiers | 16 (24,6 %) | 16 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| commandes | 12 (18,5 %) | 11 (91,7 %) | 0 (0,0 %) | 1 (8,3 %) |
| web | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Global | 65 (100,0 %) | 64 (98,5 %) | 0 (0,0 %) | 1 (1,5 %) |

Totaux croisés : 16 éditions + 12 commandes + 37 autres outils + 0 web = 65 appels ; 64 réussites techniques et 1 erreur. Les 37 autres appels comprennent 5 lectures et 32 appels MCP. Les décisions CAB sont distinctes : 28 APPROVED + 1 REJECTED = 29 (100 %).

Preuves finales : unités `msg_0ee92a4380012vGUugsVHriiwR` (304/304), intégrations `msg_0ee9380840019OYIr0dmscleJx` (100/100), AST/UTF-8/LF `msg_0ee9468c0001oEIiVT34cQG6BU` (6 AST et 10 fichiers), OpenSpec `msg_0ee952457001OYXA2wPjEasmjF` (77/77), archivage `msg_0ee97019c001ec3iwGu2es7Q0U` exit 0, `specsUpdated=false`, rapport `msg_0ee971489001QVwDfzEcc1wg2T`. Archive réelle et absence du répertoire actif vérifiées. Les sept tâches sont cochées sur preuves.

Ce change fournit les modèles et validateurs structurels d'identité ; il ne fournit pas l'authentification, la persistance Django/PostgreSQL ni l'audit durable. Aucune nouvelle dépendance, opération Git ou consultation de secret n'est observée dans le périmètre des outils audités. Aucun accès web externe observé. La fin de ce change rend le contrôle à SÉLECTION du RUN CISMP ; elle ne déclare pas le projet complet.
