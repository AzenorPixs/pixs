## 1. Validateur et delta

- [x] 1.1 Implémenter `validate_bulk_event_envelope_values` avec mapping 13 clés exact, types exacts puis valeurs, opaques sans NUL, `kind`, SemVer, UTC aware, garde `None` par `non_tenant_authorized`, payload via `validate_json_value` sans défaut, sans capture/snapshot/port/ORM/horloge.
- [x] 1.2 Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopié verbatim, sans annexe ni règle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et réussir les unitaires JSON bornés, hostiles, UTC, garde `None`, fraîcheur des listes, sans écho.
- [x] 2.2 Prouver l'isolation dans un processus frais sous gardes positives sans fichiers/réseau/processus/base/Core concret.
- [x] 2.3 Compiler les 3 Python, réussir les régressions existantes et préserver exports, sources et preuves précédentes par empreinte.
- [x] 2.4 Vérifier strict du change, UTF-8/LF, cohérence et absence d'écriture hors périmètre.

## Procédure après preuves

Cocher seulement après leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, vérifier ses six sections et totaux puis revenir à SÉLECTION sans fin globale.
