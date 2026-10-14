# Design — Vocabulaire des variantes d'opération en masse

## Choix structurel

- `enum.Enum` de la bibliothèque standard Python, deux membres `IMPORT` et `EXPORT`, valeur identique au nom.
- Représentation structurelle seule : aucune donnée, entité, persistance, API ni comportement d'exécution.
- Placement dans le module existant `src/pixs/kernel/bulk_operations.py` (décision technique CGPT, non normative) ; pas de nouveau module, pas de dépendance nouvelle, pas de `.openspec.yaml`.
- `__all__ = ["BulkCommitMode", "BulkOperationVariant"]` ; aucune façade modifiée.

## Zéro effet

Le module ne choisit aucune variante et n'exécute aucun import, export, staging, transaction, découpage, traitement de conflit, persistance ou sélection de provider. Il ne crée aucune session et n'accorde aucun accès.

## Validations

`python3 -m py_compile` du module, import neuf isolé, inspection AST de la surface Enum dans l’ordre canonique et de `__all__`, `openspec validate` du change en strict puis du canon `bulk-operations` `--type spec --strict`, suites existantes pureté du noyau, façades et vocabulaires. Aucun test ajouté pour le comportement standard de Enum.
