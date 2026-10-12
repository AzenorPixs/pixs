# Proposition — Vocabulaire des variantes d'opération en masse

## Why

La spécification validée `bulk-operations`, exigence « Contrat BulkOperation suivi par operation_id », nomme explicitement les variantes IMPORT et EXPORT. Leur représentation manque dans le code : `src/pixs/kernel/bulk_operations.py` ne fournit que `BulkCommitMode`.

## What Changes

Ajouter au module interne `src/pixs/kernel/bulk_operations.py` l'Enum `BulkOperationVariant` à deux membres, `IMPORT` et `EXPORT`, noms et valeurs conformes à la spécification, et l'ajouter à `__all__` en conservant `BulkCommitMode`. Le delta OpenSpec reproduit exactement l'exigence canon et son scénario, sans ajout normatif.

## Périmètre et validation

Cette unité représente uniquement le vocabulaire. Elle ne réalise ni états, formats, rattachement `operation_id`, travaux persistants, tenant, scope, import, staging, transaction, découpage, traitement de conflit, export, persistance ou choix de provider. Elle ne modifie aucune façade ni dépendance. Vérifier le canon et le change avec OpenSpec, la compilation, un import neuf isolé, l'inspection AST de la surface Enum, puis les suites existantes de pureté du noyau, façades et vocabulaires. Aucun fichier de test du comportement standard de Enum. Archivage et rapport statistique restent des mandats distincts.
