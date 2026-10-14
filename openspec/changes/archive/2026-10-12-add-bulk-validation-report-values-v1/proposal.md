# Proposal — add-bulk-validation-report-values-v1

## Why
Le canon `bulk-operations` B13 exige des diagnostics bornés sans écho de valeurs, une progression persistée et un rapport explicite de complétude. Aucune valeur mémoire `ValidationReportV1` n'existe encore pour porter `mode`, compteurs, codes et versions sans prouver exécution, arrêt, consommation ou transaction.

## What Changes
Ajout purement mémoire de `ValidationReportV1` à huit clés exactes, avec deux fonctions pures :
- `validate_bulk_validation_report_values(candidate: object,*,policy: object,declared_codes: object,declared_fields: object)->list[Diagnostic]`
- `capture_bulk_validation_report_values` mêmes params `->tuple[_ValidationReportBound|None,list[Diagnostic]]`
Contexte `policy` et catalogues `declared_codes` / `declared_fields` obligatoires, fermés par helpers existants. Aucun ancien code modifié. Trois fichiers Python nouveaux uniquement.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : implémentation partielle des valeurs ValidationReportV1 déjà définies par B13 ; delta verbatim, canon inchangé.

- Header huit champs owned, `report_version` exacte `1.0.0`, `mapping_version` SemVer complète, textes runtime stricts.
- `progress` dict six clés exactes avec invariants intrinsèques via helper existant, `total_rows=None` admis.
- `diagnostics` tuple exact borné `<= policy.max_diagnostics`, chaque row trois clés exactes `RowDiagnosticV1` avec membership codes/champs et `line_index int>=1|None` via helpers existants.
- Capture privée frozen/slots imbriquée, sans alias dict/list appelant, `__all__` deux fonctions, diagnostics statiques `VALIDATE` triés dédupliqués sans écho, `None` avec refus jamais d'exception attendue.

## Impact
Aucun rapport servi créé. Aucune preuve de complétude, arrêt, consommation, transaction, variante réelle, `applied`/`exported`, stockage, horloge, port, ORM ou JSON arbitraire. `None` mémoire n'autorise aucun `EXPORT`. `complete` bool n'atteste pas que la limite atteinte est connue. Seul `len>max` est refusé, jamais `len==max` par inférence.
