# Proposition — Vocabulaire des stratégies de conflit en masse v1

## Why

La spécification validée bulk-operations contient l'exigence « Vocabulaire structurel
BulkConflictStrategy v1 » qui nomme exactement quatre stratégies de conflit ; leur
représentation manque dans le module interne.

## What Changes

Ajouter BulkConflictStrategy(Enum) au module bulk_operations.py avec les seuls quatre
membres de stratégies, nom égal à la valeur, dans l'ordre du canon. Préserver octet pour
octet BulkCommitMode, BulkOperationVariant, BulkReferenceFormat, BulkOperationState, le
docstring et la façade ; ajouter le seul nouvel export interne. Le delta reproduit
exactement l'exigence canonique sans modification normative.

## Périmètre et validation

Vocabulaire préparatoire de stratégies de conflit uniquement : aucun choix ni défaut de
stratégie, aucune résolution de conflit, permission, import, idempotence ou persistance.
Le rejet par défaut existant et les autorisations module/contrat restent intacts. Aucun
provider, façade ou configuration modifié, aucun fichier de test ajouté ou modifié.
Compiler, importer en processus neuf, inspecter AST/exports et réussir les suites
existantes. Archivage et rapport statistique restent séparés.
