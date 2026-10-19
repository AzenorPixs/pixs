## 1. Validateur et delta

- [x] 1.1 Implémenter `validate_bulk_export_manifest_values` et `capture_bulk_export_manifest_values` avec mapping dix-sept clés exact, tous types et UTC avant helpers et valeurs, douze `str` exactes, `scope_context_reference` en `str | None`, deux `int` exacts `>=0` sans max, `expires_at` en `timezone.utc` identité, `complete` `bool` mémoire, `str` runtime, `manifest_version` EXACT `1.0.0`, SemVer complète, `format`/`consistency_kind` seuls, sha hex 64 minuscule, dataclass privée `frozen/slots` owned, `__all__` deux fonctions, listes fraîches `VALIDATE` triées sans écho, sans défaut, manifeste servi, finalisation, horloge, gouvernance, autorité, consistance résolue, hash calculé, stockage/export/URL/transaction ni cohérence entre champs.
- [x] 1.2 Fournir le delta `specs/bulk-operations/spec.md` `MODIFIED` B12 recopié verbatim, sans annexe ni règle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et réussir les unitaires dix-sept clés, vrais hostiles sans hooks, SemVer, sha, UTC identité, formats/consistances seuls, fraîcheur des listes, sans écho.
- [x] 2.2 Prouver l isolation en processus frais sous gardes existantes réutilisées sans fichiers, réseau, processus, base ou Core concret.
- [x] 2.3 Compiler les 3 Python, réussir les régressions pures existantes y compris les profils purs Bulk existants et préserver exports, sources et preuves précédentes par empreinte.
- [x] 2.4 Vérifier strict du change, UTF-8 et LF, cohérence et absence d écriture hors périmètre.

## Procedure apres preuves

Cocher seulement après leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, vérifier ses six sections et totaux puis revenir à SELECTION sans fin globale.
