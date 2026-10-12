# Proposition — Vocabulaire des modes d’import en masse

## Pourquoi

La spécification validée `bulk-operations`, exigence « Import via staging privé et commandes propriétaires », nomme quatre modes explicites : VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK et BEST_EFFORT. Leur représentation manque dans le code.

## Changement

Ajouter le module interne `src/pixs/kernel/bulk_operations.py` avec `BulkCommitMode(Enum)`, quatre membres dont les noms et valeurs correspondent aux modes spécifiés, et le seul export `BulkCommitMode`. Le delta OpenSpec reproduit exactement l’exigence et son scénario, sans ajout normatif.

## Périmètre et validation

Cette unité représente uniquement le vocabulaire. Elle ne réalise ni import, staging, transaction, chunking, traitement de conflit, export, persistance ou choix de provider. Elle ne livre pas l’exigence d’import complète et ne modifie aucune façade ou dépendance.

Vérifier le canon et le change avec OpenSpec, la compilation, un import isolé et la surface Enum, puis les suites existantes de pureté du noyau, façades et vocabulaires. Aucun fichier de test supplémentaire du comportement standard de Enum. Archivage et rapport statistique restent des mandats distincts.
