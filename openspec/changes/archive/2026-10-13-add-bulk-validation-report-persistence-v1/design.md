# Design — add-bulk-validation-report-persistence-v1

## Données et limites du socle

Huit clés canoniques exactement : report_version, operation_id, mode, progress, diagnostics, complete, source_version, mapping_version ; tous attributs explicitement fournis.
report_version vaut 1.0.0 déclaré ; operation_id est opaque, sans FK ni unicité ajoutée.
mode appartient à VALIDATE_ONLY/ATOMIC/ATOMIC_PER_CHUNK/BEST_EFFORT ou None explicite pour EXPORT.
progress est un mapping ProgressV1 à six clés exactes : total_rows, validated_rows, invalid_rows, applied_rows, execution_rejected_rows, exported_rows.
diagnostics est un TUPLE exact de mappings RowDiagnosticV1 ; CHAQUE mapping a les trois clés exactes code, field_reference, line_index, pas un tuple à trois positions ni un message brut.
complete bool, source_version str opaque ou None et mapping_version SemVer sont des valeurs structurales ; leur présence ne prouve ni compteurs réels ni complétude/exécution/autorité.
Le producteur serveur assume ces préconditions ; stockage ne produit/tronque/horodate/hache aucun rapport.

## Physique et API

PK locale id BigAutoField technique hors huit, aucun Unique/PK sur operation_id.
Neuf colonnes physiques : id, six scalaires et deux TEXT privés progress/diagnostics.
Append-only snapshots indépendants, pas de cardinalité fonctionnelle, versionnement/latest/update/CAS ou format de référence public inventés.
Repository séparé : insert des huit données -> identifiant local technique ; get par identifiant technique exact positif et capacité PostgreSQL -> capture figée owned ou None.
Aucun champ technique dans les huit exports. Les données retournées ne sont ni une autorisation READ_RESULT ni attestation de résultat.

## Capture, politique et codec

Réutiliser validate/capture_bulk_validation_report_values, PolicyV1, ProgressV1 et RowDiagnosticV1 existants sans les modifier.
policy, declared_codes et declared_fields sont requis explicitement par fabrique et lecture, fournis par appelant serveur de confiance ; aucune nouvelle autorité, catalogue, trust bool, variable/default.
Capturer un contexte privé immuable de valeurs déjà validées pour save/full_clean/exports d’une instance fabriquée ; une instance hydratée nécessite un contexte explicite.
La borne max_diagnostics est vérifiée AVANT inspection des éléments d’un tuple surdimensionné, même si ces éléments sont hostiles.
Capture typed OWNED/FROZEN des huit valeurs et sous-objets avant sérialisation.
Codec JSON stdlib de stockage interne : progress mapping -> TEXT, tuple diagnostics -> liste privée de mappings -> TEXT ; reconstruire tuple exact dans le même ordre, sans modifier noms, types, None ni valeurs.
Pas JSONB présumé, canonical/wire public ni hash. Refus statique de capacité ValueError/RecursionError avant write sans modifier globals int ; tests int640 dans enfant isolé seulement.
Chargement de données DB TEXT : dupkeys, NaN/constantes spéciales, malformed refusés ; revalider les huit valeurs, borne et catalogues avant capture/export, sans coercition de valeurs étrangères.

## Modèle et transaction

from_values valide/capture avant construction sans I/O, pas de défaut logique ni sauvegarde.
as_values utilise les attributs courants présents dans __dict__, aucun chargement différé ; exports owned uniquement.
full_clean contrôle huit valeurs même avec exclude, sans requête de validation SQL.
save surchargé insert-only, force_insert True, force_update False, update_fields None, instance adding, alias str exact explicite et transaction propriétaire active sur cet alias après validation avant ORM.
Autres erreurs DB propagées avec rollback/cause, aucune exception ou diagnostic ne reproduit de valeur.
Une instance hydratée ne peut pas être mise à jour ; QuerySet/SQL brut hors primitive et aucune immutabilité DB globale prétendue.

## Sources, preuves et exclusions

Six sources : record, repository, migration0009_bulk_validation_report dépendant de0008_bulk_inbox_receipt, import minimal models.py, unité offline, harness PG isolé.
Une table créée, reverse0009 seule laisse les onze tables préexistantes intactes.
Unit : véritables gardes d’import/I/O, types hostiles/clé armée, borne avant poison, catalogues/policy, copie/gel, codec tuples/ordre/None, capacité réelle en enfant int640, metadata/migration sans DB.
PG : neuf colonnes, multiples rapports même operation_id sans latest, get identifiant technique sans format public, co-commit/co-rollback et erreurs/capacité, codec fidèle/progress/diagnostics, malformations DB refusées, nettoyage owned/connexions/public et onze tables stables ; régressions pertinentes.
Complétude réelle/arrêt des traitements/READ_RESULT/gouvernance/production rapport propriétaire sont préconditions ou hors de ce socle, jamais attestés.
Pas de nouveaux ports, callback métier, auth bool, catalogue, hash, clock, wire/endpoint, receiver/provider, Outbox/Manifest/PA/PZT, frontend, Git, secrets, infrastructure ou norme ; B13 global reste incomplet.
