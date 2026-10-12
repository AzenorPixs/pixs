## Context
Le RSMP groupé valide neuf valeurs stockées et leur future persistance. Ce premier change ne porte que leur validation en mémoire ; les exigences ORM et DB restent à implémenter ensuite.

## Goals / Non-Goals
Valider exactement neuf clés explicites, str exactes et trois None explicitement permis. Références opaques non vides, égalité admise, enum values canoniques, parse_version réutilisé.
Aucun ORM, I/O, résolution, autorisation, défaut, conversion, applicabilité de mode, mutation du dict ou contrat BulkOperation complet.

## Decisions
Module pur Kernel selon les conventions Bulk existantes. Type dict exact avant items, clés str exactes avant hash/comparaison, snapshot mémoire et contrôle des types de toutes les valeurs avant validation sémantique. Diagnostic VALIDATE statiques triés/dédupliqués, liste fraîche sans écho.

## Validation
Trois compilations, quatorze tests unitaires plus un processus frais sous gardes positives d'effets, 111 régressions Bulk/fondations. Strict du change avant/après code, UTF-8/LF, références et ensembles de fichiers préservés.

## Risks / Trade-offs
Le profil de stockage reçoit des str canoniques, contrairement aux profils Kernel à membres Enum ; aucune conversion implicite. Une validation réussie ne prouve ni stockage ni autorité.

## Rollback
Les trois nouveaux fichiers peuvent être retirés sur autorisation distincte ; aucun schéma ou donnée modifié.
