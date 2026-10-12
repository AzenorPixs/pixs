# Proposition — Vocabulaire des états d'opération en masse v1

## Why

La spécification validée bulk-operations contient l'exigence « Vocabulaire structurel
BulkOperationState v1 » qui nomme exactement dix états ; leur représentation manque
dans le module interne.

## What Changes

Ajouter BulkOperationState(Enum) au module bulk_operations.py avec les seuls dix
membres d'états, nom égal à la valeur. Préserver octet pour octet BulkCommitMode,
BulkOperationVariant et BulkReferenceFormat, et ajouter le seul nouvel export interne.
Le delta reproduit exactement l'exigence canonique sans modification normative.

## Périmètre et validation

Vocabulaire préparatoire d'états uniquement : aucun runtime, transition, ordre,
terminalité, alias, défaut, rattachement à JobState ni effet d'import, d'export ou de
persistance. Aucun provider, façade ou configuration modifié, aucun fichier de test
ajouté ou modifié. Compiler, importer en processus neuf, inspecter AST/exports et
réussir les suites existantes. Archivage et rapport statistique restent séparés.
