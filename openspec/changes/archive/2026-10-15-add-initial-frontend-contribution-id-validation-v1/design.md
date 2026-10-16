# Design — add-initial-frontend-contribution-id-validation-v1
## Contrats
- Source unique : `openspec/specs/frontend/spec.md`, 2 requirements Id v1 + scénarios.
- Python `>=3.12`, stdlib seule, aucun import I/O dans module.
- API `validate_frontend_contribution_id_v1(value: object)->str` = choix implémentation, pas norme.
## Fichiers
- `frontend_contribution_ids.py` : docstring lexicale seule ; `TypeError` générique si non-str ; sinon `ValueError` générique si `len(segments)<2`, segment vide, ou char hors `[A-Za-z0-9_-]` (ASCII seul, donc espace/non-ASCII refusés, `.` seul séparateur) ; conservation valeur textuelle à l'identique si valide ; `__all__` seul ; rien d'autre.
- `__init__.py` : inchangé. Helpers `types/paths`, shared, frontendJS, docs : inchangés.
- `tests/unit/test_frontend_contribution_id.py` : valides `acme.crm.contacts`, `ACME.crm-2.contacts_1` égaux sans transformation ; invalides `""`, 1 segment, `.a`, `a.`, `a..b`, espace, non-ASCII, char interdit, non-str sans coercition ; messages génériques sans écho ; `__all__` seul.
- `tests/integration/..._integration.py` : même forme `entry_path` : `MARKER=FRONTEND_CONTRIBUTION_ID_SAFE_INTEGRATION_OK`, `FIXED_ENV LANG=C.UTF-8 PATH=/usr/bin:/bin`, `TIMEOUT 10`, gardes writes/network/process/environ/db + FS/reads, contrôles positifs, import sans effet, cas valides/invalides fonction pure, `TemporaryDirectory(dir=REPO_ROOT)` nettoyé, `stderr==""`.
## Exclusions
- MUST NOT FS/resolve/enregistrer/composer/router/charger/activer ; MUST NOT prouver propriété/provenance/confiance/unicité/droit `pixs.*` ; MUST NOT manifest.
