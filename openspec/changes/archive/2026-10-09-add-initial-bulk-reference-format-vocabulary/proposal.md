# Proposition — Vocabulaire des formats de référence en masse

## Why

La spécification validée bulk-operations nomme CSV et NDJSON comme formats de référence ; leur représentation manque dans le module interne.

## What Changes

Ajouter BulkReferenceFormat(Enum) au module bulk_operations.py avec les seuls membres CSV et NDJSON, nom égal à la valeur. Conserver BulkCommitMode et BulkOperationVariant et ajouter le seul nouvel export interne. Le delta reproduit l’exigence canonique sans modification normative.

## Périmètre et validation

Vocabulaire de références uniquement, aucun parsing, IO, sélection, format global ou rejet des adapters. Les adapters XLSX, Parquet ou fournisseur restent extensibles selon le contrat existant. Aucun provider, persistance, état ou façade modifié. Compiler, importer en processus neuf, inspecter AST/exports et réussir les suites existantes. Archivage et rapport statistique restent séparés.
