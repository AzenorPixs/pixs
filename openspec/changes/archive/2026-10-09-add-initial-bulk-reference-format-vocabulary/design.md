# Conception — Formats de référence en masse

BulkReferenceFormat utilise enum.Enum de la bibliothèque standard : CSV puis NDJSON, noms et valeurs identiques. Il désigne les références déjà nommées par le canon ; il ne définit pas le domaine de tous les formats acceptables et ne valide aucun flux ni adapter.

Le module conserve intégralement les deux vocabulaires existants. __all__ ajoute uniquement BulkReferenceFormat. Aucune façade, dépendance ou configuration nouvelle.

Validation : strict du change avant code, compilation, import en processus neuf, AST et surface exacts, mêmes suites de pureté/façades/vocabulaires ; contrôles UTF-8/LF et empreintes. Aucun test supplémentaire du fonctionnement standard de Enum.
