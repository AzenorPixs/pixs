# Design — add-initial-frontend-entry-path-validation-v1

## Contrats
- Source canonique unique : `openspec/specs/frontend/spec.md`, Requirements `Syntaxe lexicale préparatoire FrontendEntryPath v1` et `Limites du contrôle lexical FrontendEntryPath v1` avec leurs scénarios.
- Python `>=3.12` conservé, stdlib seule, aucun import I/O (`pathlib`/`os` interdits dans le module).
- API `validate_frontend_entry_path_v1(value: object) -> str` = choix d'implémentation, pas nouvelle norme.

## Fichiers
- `src/pixs/kernel/frontend_entry_paths.py` :
  - docstring lexicale seule, sans machine, enregistrement, composition, chargement, activation, manifest, routage, permission ou persistance ;
  - `def validate_frontend_entry_path_v1(value: object) -> str:` :
    - `TypeError` générique sans écho si `not isinstance(value, str)` (aucune coercition) ;
    - `ValueError` générique sans écho si chaîne vide, non encodable `value.encode("utf-8")` strict (surrogates isolés), absolue (`startswith("/")`), segments vides (`split("/")` avec vide), segment `.` ou `..` seuls (segments `.hidden` valides), caractère interdit `\`, `:`, `?`, `#`, `%`, ou U+0000–U+001F / U+007F ;
    - unicode UTF-8 et espaces littéraux conservés, aucune limite arbitraire longueur/ASCII/extension ;
    - `MUST NOT` normaliser, strip, décoder, accéder FS, resolver, stat ;
    - retourne `value` inchangée si valide ;
  - `__all__ = ["validate_frontend_entry_path_v1"]` ;
  - aucune autre fonction/classe/constante/registre/façade.
- `src/pixs/kernel/__init__.py` : inchangé.
- `tests/unit/test_frontend_entry_path.py` : table normative vrais `frontend/routes/contacts`, unicode `données/été`, espaces `a b/c d`, `.hidden/route` conservés sans transformation de valeur ; faux vide, absolu `/a`, segments vides `a//b` `/` `a/`, `.`, `..`, `a/./b`, `a/../b`, antislash, `:`, `?`, `#`, `%`, C0 0..31, DEL 127, surrogates `"\ud800"` non encodables, non-str `None/123/b"a"/["a"]` sans coercition ; messages génériques sans écho ; `__all__` seul.
- `tests/integration/test_frontend_entry_path_integration.py` : même forme que `test_frontend_contribution_type_integration.py` avec gardes writes/network/process/environ/db, contrôles positifs, `MARKER="FRONTEND_ENTRY_PATH_SAFE_INTEGRATION_OK"`, `FIXED_ENV={"LANG":"C.UTF-8","PATH":"/usr/bin:/bin"}`, `TIMEOUT_SECONDS=10` ; preload nécessaire puis import `pixs.kernel.frontend_entry_paths` sans effet observable ; contrôles positifs FS (`open(probe,"w")`, `os.path.exists`, `resolve/stat/access` bloqués) après import avant appel valideur pour prouver aucune lecture/écriture/resolve/stat/access ; puis cas valides/invalides fonction pure sous gardes et nettoyage prouvé ; sans réclamer zéro lecture des modules du chargeur Python.

## Exclusions
- Le module MUST NOT accéder au système de fichiers, résoudre un lien, enregistrer, composer, charger ou activer.
- Il MUST NOT définir un champ de manifest ni prouver existence, confinement ou confiance.
