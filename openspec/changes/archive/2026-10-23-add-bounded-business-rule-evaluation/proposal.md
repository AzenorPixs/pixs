# O06 — Évaluation bornée des règles métier (profil v1)

## Pourquoi

Le canon business-rules décrit des décisions déclaratives, versionnées et testables, distinctes de l'autorisation et des gardes de workflow. La RSMP validée le 22 octobre 2026 a fixé le profil v1 borné, sans code arbitraire, sans effet direct et sans activation P0. Sa réalisation séquentielle et sa qualification bornée sont tracées dans requirements.md.

## Modifications proposées

Précisions MODIFIED des quatre exigences par les oracles existants de leurs cinq scénarios, définissant le profil fermé v1 : document JSON versionné, grammaire bornée, résultat structuré et effets par propriétaire. Extension miroir du canon. Traçabilité actualisée dans requirements.md sans preuve fabriquée. Retaille de tasks.md en unités successives et auto-testables.

La préparation documentaire ne produisait ni code ni test applicatif. La réalisation ensuite autorisée du seul O06 conserve les exclusions : activation P0, bibliothèque supplémentaire, infrastructure, Git et archivage avant preuves.

## Capacités

### Profil de la capacité existante business-rules

Aucune nouvelle capacité. Profil d'évaluation bornée v1 : format JSON fermé versionné, opérateurs all, any, not, eq, ne, lt, lte, gt, gte, in, exists, types null, boolean, integer, string, array, plafonds 65536 octets, profondeur 8, noeuds 256, résultat corrélé et motifs minimisés, évaluation pure, effets par Command propriétaire, activation indépendante.

### Capacités modifiées

Aucune des quatre exigences actuelles n'est modifiée. Leurs cinq scénarios reçoivent les modalités v1 adoptées par validation explicite du développeur le 22 octobre 2026 (RSMP O06, six documents, puis implémentation après validation documentaire). Aucun nouveau titre d'exigence ou scénario n'est ajouté. Aucune qualification runtime n'est déduite.

## Périmètre documentaire de la RSMP validée

Fichiers : proposal.md, design.md, requirements.md, tasks.md, specs/business-rules/spec.md du change, specs/business-rules/spec.md du canon.

Les exclusions de cette étape documentaire portaient sur le code et les tests applicatifs, en plus des exclusions durables : activation P0, bibliothèque supplémentaire, Git, infrastructure, autres changes et archivage avant preuves. Le développeur a ensuite autorisé explicitement le septième fichier .openspec.yaml pour le seul passage de skip_specs de true à false. Le schéma, la date et le commentaire sont préservés ; cette métadonnée rend le delta présent compatible avec la validation OpenSpec.

## Dépendances

- integrate-runtime-authorization-and-super-admin (autorisation distincte conservée).
- add-durable-minimized-audit (audit minimisé et corrélation conservés).
- add-protected-core-http-commands-and-queries (surface Command conservée).

Une dépendance décrit un contrat attendu, non une disponibilité acquise.

## Réalisation du profil v1

Composant strictement facultatif au-dessus du Kernel, déclaré par manifest et sélection explicite. Contrats publics versionnés seuls exposés. Écritures seules via le propriétaire. Django et PostgreSQL conservés comme autorités, avec tenant et scope, audit et gouvernance. Le moteur utilise la bibliothèque standard Python ; le raccordement utilise les dépendances Core, Django et PostgreSQL existantes, sans provider externe ni installation nouvelle.

## Critères de sortie du profil v1

Reproductibilité à entrée et version identiques. Refus avant activation pour document inconnu, ambigu, incomplet ou hors bornes. Aucune élévation de droit par la règle.

## Décision et suites

La reprise et ses modalités v1 sont adoptées par la validation explicite du développeur du 22 octobre 2026. Le delta et le canon définissent la grammaire, les schémas, les bornes, les types et les refus ; aucun de ces choix n'est laissé à une invention pendant le code. Après validation OpenSpec des six documents et de cette métadonnée, le parent CISMP5 poursuit les tâches de réalisation et leurs tests séparés dans le seul O06, puis l'archive, le rapport et la clôture ciblée. Cette préparation ne prouve aucun test runtime.

## Qualification de réalisation — 23 octobre 2026

Les tâches 1 à 4 sont validées et cochées sur preuves natives : 95 unitaires, 13 critères PostgreSQL et six refus explicites du scénario exécutable avant activation. requirements.md relie les cinq scénarios aux commandes, appels natifs et artefacts ; design.md décrit les frontières effectives et les limites de qualification. Le raccordement n'ajoute aucune Command ni route HTTP Core et ne modifie pas les fichiers Core/backend.

La tâche 5 consolide ces preuves et les contrôles finaux avant l'archive autorisée, le rapport STATISTIQUES.md et la clôture du seul RUN O06. Aucun second change n'est inclus. C09/C10 synthétiques, absence d'activation P0 et absence de modification d'interface restent explicites.
