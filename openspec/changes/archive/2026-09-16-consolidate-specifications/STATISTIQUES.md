# STATISTIQUES — 2026-09-16-consolidate-specifications (création lors revalidation)

Création lors revalidation RCAMP1, aucune statistique historique existante. Données d'implémentation historique : N/A motivé (change déjà archivé, audit sans correction).

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 2,02 s | 471,81 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (modèle exact N/A) | N/A | OpenAI (Codex) | N/A | N/A | N/A | N/A |

Modèle codeur exact natif `opencode-go` / `muse-spark-1.3-contributor` / `high`, version exacte modèle N/A. Orchestrateur nommé Codex, modèle exact N/A, pas sondé. Temps de service N/A : `busyMs` inclut outils et attentes, pas génération. Tokens/cache/coûts/compactions de production : N/A explicite, non collectés dans l'agrégat, distincts des 997 tokens sondes.

## 1. Statistiques générales et décisions

| Indicateur | Valeur |
|---|---|
| `run_id` | `rcamp1-pixs-53186d5cc52a4216` |
| Début | `2026-10-26T17:42:53.084460+00:00` |
| Fin d'activité comptée | `2026-10-26T18:08:04.829363+00:00` |
| Durée globale | 1511,74 s (25,20 min, <30 min : créneau périodique 30 min non requis) |
| Réservé / busy / idle (bruts) | 1467091 ms / 731691 ms / 707907 ms ; `nativeUnknownMs` 27493 ms |
| Quota fenêtre 10080 min (`codex`, `resetsAt` 1793599315) | 87 % → 95 % = +8 pts PARTAGÉS, sans attribution exclusive |
| Approbations | 6 APPROVED (100 %), 0 REJECTED, 0 clarification, 0 PENDING, 5 `once` (5/6=83,3 %), 1 NO_EFFECT, 0 erreurs techniques |
| Mandat édition | 1 APPROVED `NO_EFFECT` (outil non exposé), accès libéré, décision invalidée ; nouveau mandat `write` REVALIDATION réussi (1) ; 2 mandats édition approuvés dans fenêtre, 1 write effectif et 1 NO_EFFECT ; correction après capture hors compte |
| Refus CAB / erreurs outil natif | 0 / 0 |

Sondes valides même prompt (220 car.) : 2 prévues, 2 réussies, 0 manquées. TTMT min 1,5973 / max 2,4358 / moy 2,0165 s, débit min 157,394 / max 786,227 / moy 471,8105 tok/s, 997 tokens surcharge (489+508) distincte des travaux. Rédaction statistiques/publication/gates exclue des compteurs ; ne pas prétendre comptes finaux de toutes phases. Données arrêtées avant rédaction.

## 2. Types de messages et d'outils

| Type | Nombre | Part |
|---|---|---:|
| Messages user | 27 | 37,0 % |
| Messages assistant | 46 | 63,0 % |
| Total messages | 73 | 100 % |

| Outil | Completed | Part (55) |
|---|---:|---:|
| `cab-mcp` | 27 | 49,1 % |
| `read` | 21 | 38,2 % |
| `bash` | 4 | 7,3 % |
| `glob` | 2 | 3,6 % |
| `write` | 1 | 1,8 % |
| Total outils | 55 | 100 % |

| Domaine | Nombre | Part (55) |
|---|---:|---:|
| Édition | 1 | 1,8 % |
| Commandes | 4 | 7,3 % |
| Autres | 50 | 90,9 % |
| Web | 0 | 0,0 % |
| Total | 55 | 100 % |

Appels `completed` distincts des `exit` commandes. 0 erreur outil, 0 refus CAB. Échecs commandes conservés (§4).

## 3. Fichiers modifiés

| Fichier absolu | Effet fenêtre |
|---|---|
| `/home/devops/datas/pixs/output/rcamp/rcamp1-pixs-53186d5cc52a4216/REVALIDATION.md` | 2 mandats approuvés 100 %, 1 écriture réussie 50 %, 1 NO_EFFECT 50 %, 0 refus ; NO_EFFECT distinct d'erreur outil |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-09-16-consolidate-specifications/STATISTIQUES.md` | fichier courant hors fenêtre |

Éditions correctives après capture hors fenêtre. Checkpoints/preuves orchestrateur écrits hors compte outils OpenCode ; comptage orchestrateur exhaustif N/A. Archive 5 originaux identiques et 78 specs+7 cadrages (90 inchangés) + 1 DEVOPS divergent en concurrence. Secrets non lus. Git non autorisé et non utilisé.

## 4. Commandes

4 Bash natifs `completed`, tous `exit` conservés.

| # | Commande (100 car. max) | Exit |
|---|---|---:|
| 1 | `/usr/bin/true` | 0 |
| 2 | `/home/devops/.local/npm/bin/openspec validate consolidate-specifications --strict` | 1 |
| 3 | `/home/devops/.local/npm/bin/openspec validate --all --strict` | 1 |
| 4 | `/home/devops/python/current/bin/python3 -I -B - <<'PY' [...]` | 1 |

| Famille | Nombre | Part (4) |
|---|---:|---:|
| Prévol | 1 | 25,0 % |
| OpenSpec | 2 | 50,0 % |
| Inspection Python | 1 | 25,0 % |
| Total | 4 | 100 % |

4 exécutées approuvées 100 %, exit 0 = 1/4 = 25,0 %, exit 1 = 3/4 = 75,0 %, 0 commande refusée. Détails exacts en preuves : `test-target.json` (Unknown item archive), `test-global.json` (184 passed/1 failed sur 185), `test-static.json` (heredoc complet, 78/859/1064, 8 faux positifs). Cible archive non reconnue, global 184 passed/1 failed sur 185, filtre 8 faux positifs confirmés manuellement.

## 5. Accès web

| Canal | Nombre | Taux |
|---|---:|---:|
| Web session métier native | 0 | N/A |
| Total | 0 | N/A (dénominateur 0, pas 100 % pour zéro) |

Aucun webtool observé en session métier. API locales / sélection fournisseur distinctes, pas visites web. Aucune URL inventée.

## 6. Synthèse globale

| Période | Début | Fin | Archivage | Durée globale |
|---|---|---|---|---|
| Fenêtre comptée | 2026-10-26T17:42:53.084460+00:00 | 2026-10-26T18:08:04.829363+00:00 | sans objet | 00h25min12s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant | 2026-10-26T17:42:53.084460+00:00 | 87 % | 2026-11-02T07:01:55+01:00 |
| Après | 2026-10-26T18:08:04.829363+00:00 | 95 % | 2026-11-02T07:01:55+01:00 |
| Différence | — | +8 points | — |

- Outils : 1 édition + 4 commandes + 50 autres = 55, web 0, sans réadditionner preuves partagées.
- Tâches : 4 CONFORME 50,0 %, 1 ÉCART 12,5 %, 3 NON VÉRIFIABLE 37,5 %, 0 NON APPLICABLE ; 78 specs, 859 exigences, 1064 scénarios.
- Archivage : sans objet (déjà archivé). Intégrité 90 inchangées + 1 DEVOPS divergent, 5 archive identiques.
- Rapport revalidation : [REVALIDATION.md](../../../../output/rcamp/rcamp1-pixs-53186d5cc52a4216/REVALIDATION.md).
- État technique final : consulter `state.json`.

### Suivi direct autorisé — SUIVI_DIRECT_2026-10-26 — 2026-10-26T20:32:32.288247+01:00

Les six sections et tous les chiffres ci-dessus restent ceux de la fenêtre RCAMP initiale. Cet addendum décrit le suivi ultérieur autorisé par le développeur, notamment Git en lecture seule et le passage explicite en mode direct après refus CAB `change-already-delivered`. Aucun nouveau RUN, job ou gate CAB n'est revendiqué.

#### Agent et limites de collecte

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex — modèle exact non exposé, suivi direct | N/A | OpenAI | N/A | N/A | N/A | N/A |

Aucun OpenCode ni aucune sonde de pilotage n'est démarré pour ce suivi direct. Messages, appels d'outils exhaustifs, sondes, tokens, cache, coût et temps de génération : N/A, collecte exhaustive non activée. Les compteurs et métriques de l'ancien agent OpenCode ne sont pas réutilisés pour Codex. Les commandes Git et contrôles préparatoires ne sont pas reconstitués artificiellement dans un total.

#### Résultats actuels des tâches

| Verdict | Nombre | Part des 8 tâches |
|---|---:|---:|
| CONFORME | 8 | 100 % |
| ÉCART | 0 | 0 % |
| NON VÉRIFIABLE | 0 | 0 % |
| NON APPLICABLE | 0 | 0 % |
| Total | 8 | 100 % |

1.1 : 74 spécifications, 287 exigences, 290 scénarios prouvés dans la révision Git d'archivage ; quatre ajouts ultérieurs identifiés. 3.3 : canon identique avant/après et aucun code produit ou manifeste de dépendances modifié dans le commit. 3.2 : contrôles stricts ciblé et global réussis après la réorganisation des sept exigences longues. 3.1 : validation actuelle réussie sur une copie isolée identique ; la trace de l'exécution originale n'a pas été retrouvée et n'est pas inventée. Les quatre autres verdicts conformes du premier audit sont conservés sur des sources inchangées.

#### Validations observées

| Famille | Nombre | Part des 5 validations | Exit 0 | Exit 1 |
|---|---:|---:|---:|---:|
| Cible active avant/après | 2 | 40 % | 1 (50 %) | 1 (50 %) |
| Global avant/après | 2 | 40 % | 1 (50 %) | 1 (50 %) |
| Reproduction isolée de l'archive | 1 | 20 % | 1 (100 %) | 0 (0 %) |
| Total | 5 | 100 % | 3 (60 %) | 2 (40 %) |

Les trois validations après correction ou préparation réussissent : 3/3, soit 100 %. Le global passe de 185 réussites et 1 échec à **186 réussites et 0 échec**. Les sept avertissements de longueur disparaissent dans la validation ciblée. L'information globale de doublon `reference-composition` est conservée hors cible ; elle n'entraîne pas d'échec global et aucune correction de ces autres changes n'est effectuée. Aucune commande de ce suivi n'a fait l'objet d'un refus de permission ; les approbations et permissions CAB sont sans objet en mode direct.

Arguments, dates, durées et sorties : `validate-active-target.json`, `validate-global-before.json`, `validate-active-target-after.json`, `validate-global-after.json` et `validate-isolated-archive.json`, dans `output/rcamp/rcamp1-pixs-53186d5cc52a4216/followup-direct/`. Les preuves partagées ne sont comptées qu'une fois. Aucun test produit, PostgreSQL ou navigateur n'est requis pour cette correction documentaire.

#### Fichiers et intégrité

| Fichier absolu modifié | Nature |
|---|---|
| `/home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/specs/pixs-agent/spec.md` | Sept paragraphes réorganisés ; 8 exigences et 18 scénarios existants conservés, 7 scénarios de détails ajoutés, toutes les clauses conservées. |
| `/home/devops/datas/pixs/output/rcamp/rcamp1-pixs-53186d5cc52a4216/REVALIDATION.md` | Addendum daté ; bilan initial conservé. |
| `/home/devops/datas/pixs/openspec/changes/archive/2026-09-16-consolidate-specifications/STATISTIQUES.md` | Amendement du seul rapport existant ; données anciennes conservées. |

Le checkpoint et les JSON de preuve sont conservés sous `output/`, hors compte exhaustif d'outils. La copie isolée de cinq fichiers est un artefact de preuve, pas un nouvel archivage. Sur les 575 fichiers d'entrée comparés après les contrôles, seul le delta autorisé diffère avant amendement des rapports. Les cinq originaux de l'archive et les 78 spécifications canoniques sont inchangés. Aucun code, test produit, tâche historique ou infrastructure n'est modifié ; aucun commit, push ou changement de référence Git n'est réalisé.

#### Durées, quota et accès

| Durée de la phase d'exécution directe mesurée | Valeur |
|---|---|
| Début consigné avant les commandes de validation | 2026-10-26T19:22:36.036020+00:00 |
| Fin des contrôles, archivage sans objet | 2026-10-26T19:26:59.319493+00:00 |
| Durée calendaire, analyses et préparation incluses | 00 h 04 min 23 s |

La préparation Git et l'attente du choix de mode sont antérieures à cette fenêtre ; la rédaction des addenda et la clôture documentaire sont postérieures. Aucun temps de génération n'est déduit de cette durée.

| Mesure du quota Codex sur 7 jours — suivi direct | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant le suivi | N/A — relevé initial absent | N/A | N/A |
| Après les contrôles, avant rédaction de cet addendum | 2026-10-26T19:30:02.524465+00:00 | 100 % | 2026-11-02T07:01:55+01:00 |
| Différence propre au suivi | — | N/A — relevé initial absent | — |

Le quota est partagé par le compte. Aucun écart avec les anciens relevés 87 % et 95 % n'est attribué à ce suivi. Accès web de recherche : 0 dans les actions exécutées ; aucun fournisseur externe de codage n'est sollicité par ce suivi direct. Les lectures HTTP du contrôle CAB ne sont pas des visites web. Données historiques de performance ou de coût : N/A pour cette nouvelle phase.

Référence : [bilan détaillé actualisé](../../../../output/rcamp/rcamp1-pixs-53186d5cc52a4216/REVALIDATION.md). Archivage : sans objet, archive conservée en place. La clôture et les empreintes effectives se trouvent dans le suivi direct de `state.json`.

#### Contrôle supplémentaire de clôture hors fenêtre initiale du suivi

Après la fenêtre mesurée des cinq validations, deux modifications concurrentes ont été observées dans `reconstruct-initial-specification-baseline-traceability/design.md` et `tasks.md`. Ces fichiers sont préservés. Le contrôle global strict a donc été rejoué le `2026-10-26T19:34:16.871326+00:00` : **186 réussites, 0 échec, exit 0**. Cette commande supplémentaire est séparée des cinq lignes de la première fenêtre.

Bilan de toutes les validations de ce suivi, contrôle final compris : **6 commandes**, dont **4 exit 0 (66,7 %)** et **2 exit 1 avant correction (33,3 %)**. Les **4 contrôles postérieurs à la correction ou à la préparation isolée réussissent, soit 100 %**. Les résultats initiaux de la fenêtre RCAMP restent distincts. Sur les 575 fichiers d'entrée : trois modifications prévues par ce suivi, deux changements documentaires concurrents et 570 fichiers inchangés ; les cinq originaux de l'archive et les 78 canons restent identiques. Preuve complémentaire : `followup-direct/validate-global-final.json` dans le dossier de sortie de ce suivi.

#### Dernière vérification de publication sur des entrées stables

Une modification concurrente de la proposition du même autre change a justifié un dernier contrôle global, achevé à `2026-10-26T19:37:39.461370+00:00` : **186 réussites, 0 échec, exit 0**, avec entrées inchangées pendant la commande. Le bilan final de ce suivi est de **7 validations : 5 exit 0 (71.4 %) et 2 exit 1 initiaux (28.6 %)**. Les cinq premiers contrôles et les fenêtres ultérieures restent distingués dans leurs preuves. Les sources comparées comportent trois fichiers modifiés par ce suivi, 3 documents concurrents préservés et 569 fichiers inchangés. Le bilan des tâches reste **8 CONFORME sur 8**. Preuve : `followup-direct/validate-global-publication.json` dans le dossier du suivi.
