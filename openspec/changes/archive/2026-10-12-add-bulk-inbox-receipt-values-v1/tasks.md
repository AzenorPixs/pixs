## 1. Validateur et delta

- [x] 1.1 Implémenter `validate_bulk_inbox_receipt_values` et `capture_bulk_inbox_receipt_values` avec mapping huit clés exact, tous types et UTC avant helpers et valeurs, six `str` exactes, `causation_id` en `str | None`, `consumed_at` en `timezone.utc` identité, `str` runtime, SemVer complète, sha hex 64 minuscule, état `CONSUMED` seul, dataclass privée `frozen/slots` owned, `__all__` deux fonctions, listes fraîches `VALIDATE` triées sans écho, sans défaut, commit, preuve, déduplication, stockage, transaction, horloge, calcul, comparaison, catalogue, provenance, auth, FK, unicité ni cohérence entre champs.
- [x] 1.2 Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopié verbatim, sans annexe ni règle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et réussir les unitaires huit clés, vrais hostiles sans hooks, SemVer, sha, UTC identité, état seul, fraîcheur des listes, sans écho.
- [x] 2.2 Prouver l isolation en processus frais sous gardes existantes réutilisées sans fichiers, réseau, processus, base ou Core concret.
- [x] 2.3 Compiler les 3 Python, réussir les régressions pures existantes y compris Outbox et préserver exports, sources et preuves précédentes par empreinte.
- [x] 2.4 Vérifier strict du change, UTF-8 et LF, cohérence et absence d écriture hors périmètre.

## Procedure apres preuves

Cocher seulement après leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, vérifier ses six sections et totaux puis revenir à SELECTION sans fin globale.
