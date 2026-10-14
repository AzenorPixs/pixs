## 1. Validateur et delta

- [x] 1.1 Implementer `validate_bulk_outbox_publication_values` et `capture_bulk_outbox_publication_values` avec mapping 12 cles exact, deux phases types avant comportement, `str` runtime, `attempt_count >= 0`, `sequence_index/revision >= 1`, SemVer complete, UTC `timezone.utc` identite, seuls couplages `lease_owner/lease_expires_at`, `RETRYING/next_attempt_at`, `PUBLISHED/published_at`, dataclass privee `frozen/slots` owned, sans defaut, catalogue, horloge, comparaison, politique, FK, unicite, allocation, publication, retry, CAS, SQL ni preuve serveur.
- [x] 1.2 Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopie verbatim, sans annexe ni regle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et reussir les unitaires 12 cles, hostiles sans hooks, ints, SemVer, UTC identite, couplages fermes seuls, fraicheur des listes, sans echo.
- [x] 2.2 Prouver l isolation dans un processus frais sous gardes existantes reutilisees sans fichiers/reseau/processus/base/Core concret.
- [x] 2.3 Compiler les 3 Python, reussir les regressions existantes et preserver exports, sources et preuves precedentes par empreinte.
- [x] 2.4 Verifier strict du change, UTF-8/LF, coherence et absence d ecriture hors perimetre.

## Procedure apres preuves

Cocher seulement apres leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, verifier ses six sections et totaux puis revenir a SELECTION sans fin globale.
