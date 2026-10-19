# Design — add-bulk-validation-report-values-v1

## Réutilisation imposée
- `validate_bulk_policy_values` pour `PolicyV1` valide avec `max_diagnostics`, sans défaut ni max inventé.
- `_catalog_state` pour `declared_codes` et `declared_fields` en tuple exact ou frozenset d'opaque text, sans autorité ni provenance inventée.
- `_policy_bound`, `_row_diagnostic_refusals`, `_RowDiagnosticSnapshot` pour diagnostics.
- `_progress_structure` puis invariants intrinsèques et `validate_bulk_progress_values` pour `ProgressV1`.

## Ordre de contrôle
Header : types exacts, Progress structure six champs de taille fixe et diagnostics de type tuple exact. Valider PolicyV1 via _policy_bound pour la borne ; si len(diagnostics)>max, refuser immédiatement sans parcourir ni copier les éléments. Sinon contrôler les types des trois champs de tous les rows et copier leurs mappings exacts, puis valeurs header/progress/catalogues/rows. Les contextes ont leurs gardes propres existantes. Jamais de comportement étranger ni écho. Les copies owned des mappings exacts remplacent toute recopie générique récursive. `report_version`, `operation_id`, `mapping_version` str requises. `mode` str canon quatre valeurs ou `None` mémoire. `source_version` str ou `None`. `complete` bool exact.

## Capture
Dataclass privée frozen/slots six scalaires pour progress. Tuple de `_RowDiagnosticSnapshot` existants frozen trois scalaires après validation. Header huit champs owned. Aucun alias vers dict/list appelant.

## Limites
Pas de couplage mode/variante réelle. Pas de refus de `complete=True` à `len==max`. Pas de stockage, horloge, port, ORM ou JSON arbitraire. Tests hostiles imbriqués, harness frais inchangé avec gardes Inbox/Export seuls CAS adaptés et probes dans Root uniquement.

## Fichiers et vérifications

Trois nouveaux Python seulement : src/pixs/backend/bulk_validation_report_values.py, tests/unit/test_bulk_validation_report_values.py, tests/integration/test_bulk_validation_report_integration.py. Aucun ancien code, export, canon ou dépendance modifié. Compiler les trois, tester frontières imbriquées/borne/politique/catalogues/ownership et processus frais sous gardes éprouvées inchangées, puis régressions pures applicables. Strict du change, UTF-8/LF et empreintes à vérifier.

## Contraintes mémoire mode et progression

Le schéma ValidationReportV1 donne les quatre modes non nuls pour IMPORT et None pour le rapport d'erreur EXPORT ; ProgressV1 exige exported_rows nul en IMPORT, applied_rows nul en EXPORT et en VALIDATE_ONLY. Appliquer ces contraintes fermées : mode non nul implique exported_rows == 0 ; mode None implique applied_rows == 0 ; mode VALIDATE_ONLY implique aussi applied_rows == 0. Elles vérifient la cohérence du candidat, sans prouver la variante réelle de l'exécution, l'autorisation, la complétude ni les compteurs réels. Aucune relation supplémentaire avec total_rows, le nombre de diagnostics ou len == max n'est ajoutée.
