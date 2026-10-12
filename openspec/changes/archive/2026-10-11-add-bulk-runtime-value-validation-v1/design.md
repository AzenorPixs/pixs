## Context
Le canon RSMP-BULK-EXECUTION-V1 approuvé ferme les choix normatifs B01-B14. Ce change implémente une fondation nécessaire aux extensions de persistance et aux services suivants, sans introduire un nouveau profil normatif.

## Goals / Non-Goals
Trois fonctions internes dans src/pixs/backend/bulk_execution_values.py : validate_bulk_execution_values(candidate), validate_bulk_progress_values(candidate), validate_bulk_policy_values(candidate). Résultat : liste fraîche de Diagnostic VALIDATE statiques, triés et dédupliqués, sans écho de valeurs.
Execution : neuf valeurs Record existantes et 27 valeurs BulkExecutionExtensionV1, toutes explicites. Progress : six valeurs et inégalités canoniques. Policy : 22 entiers strictement positifs et deux listes de délais explicites, avec contraintes canoniques.
Aucun ORM, I/O, parsing de fichier, stockage, autorisation, résolution de politique, changement d'état, CAS, bail ou worker. Ces exigences restent ouvertes pour les changes suivants.

## Decisions
Contrôler dict exact avant items, clés str exactes avant hash/comparaison, types exacts des valeurs et des structures imbriquées avant validation sémantique. Réutiliser le validateur Record et parse_version après cette garde. Ne modifier ni les candidats ni leurs références opaques.
Les textes runtime sont UTF-8 strict non vides sans NUL, sans normalisation. Les dates sont datetime exact avec timezone.utc, sans consultation d'un tzinfo étranger. Bool n'est jamais un int.
Le validateur Progress traite les contraintes intrinsèques ; les compteurs liés à IMPORT, EXPORT et VALIDATE_ONLY sont contrôlés par le validateur Execution.
Les deltas recopient les exigences canoniques B02 et B09 sans les modifier. L'archivage utilisera --skip-specs après preuve ; leurs annexes normatives restent dans les specs canoniques.

## Validation
Compiler les trois fichiers, exécuter les tests unitaires et une intégration en processus frais sous gardes positives de fichiers, environnement, réseau, sous-processus, base et Core. Vérifier les 130 régressions Bulk/fondations et les deux scénarios PostgreSQL existants dans leur environnement isolé autorisé. Valider strict du change avant/après, strict canon/global qualifié par les trois avertissements historiques et zéro nouvelle issue.
Vérifier UTF-8/LF, préservation des fichiers existants, archive unique et rapport STATISTIQUES.md distinct à six sections et totaux vérifiés.

## Risks / Trade-offs
Une validation positive ne prouve pas autorité, intégrité des objets, transaction, capacité de production ou exécution. Les signatures et ce découpage interne relèvent de la limite d'implémentation approuvée. Aucune nouvelle contrainte de taille de stockage ou de mode EXPORT ne doit être déduite.

## Rollback
Aucun schéma ni donnée modifié. Tout retrait des nouveaux fichiers nécessiterait l'autorisation applicable.
