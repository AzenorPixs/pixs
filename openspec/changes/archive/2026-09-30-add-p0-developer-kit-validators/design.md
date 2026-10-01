# Design — add-p0-developer-kit-validators

## 1. Façade et signatures

- `validate_manifest_text(text: str) -> ValidationReport` : pure, sans accès FS. `text` non-`str` → `TypeError` documentée (mésusage de programmation, pas un refus de validation).
- `validate_manifest_file(path: str | Path) -> ValidationReport` : lit exactement le fichier désigné, seulement sur demande explicite de l'appelant. `path` de mauvais type → `TypeError`. Aucun parcours de répertoire, aucune résolution, aucun import, aucune activation/provisionnement/publication.
- Les deux fonctions retournent le même type immuable et ne lèvent jamais d'exception pour un refus de validation.

## 2. Ports publiés uniquement

- Depuis la racine publiée `pixs.kernel.manifest` : `parse_manifest_text`, `load_manifest_file`, `ComponentManifest`, `ManifestValidationError`, `SUPPORTED_SCHEMA_VERSIONS`.
- Depuis la racine publiée `pixs.kernel.diagnostics` : `Diagnostic`, `VALIDATE`.
- Jamais d'import direct de `guards`, `models`, `semver`, `parser._check_schema_version` ni d'autre module privé. La validation sémantique est déléguée au noyau seul, sans duplication (ni SemVer locale, ni tables autorisées recopiées).

## 3. Retour immuable et invariants

- `ValidationReport` : dataclass frozen à slots `(ok: bool, manifest: ComponentManifest | None, diagnostics: tuple[Diagnostic, ...])`, constructible publiquement donc gardée par `__post_init__` :
  - types publics vérifiés (`ok` est `bool`, `manifest` est `ComponentManifest | None`, `diagnostics` est `tuple` de `Diagnostic`) ;
  - invariant ssi : `ok ⇔ (manifest is not None ∧ diagnostics == ())`, `¬ok ⇔ (manifest is None ∧ diagnostics ≠ ())`, sinon `ValueError`.
- `Diagnostic` immuable déjà publié réutilisé tel quel, construit directement `Diagnostic(step=VALIDATE, element=…, constraint=…, message=constraint)` avec `message = constraint` obligatoire ; jamais `from_legacy(texte_brut)`.

## 4. Délégation et point de rendu

- Texte : appel de `parse_manifest_text(text)` ; fichier : appel de `load_manifest_file(path)` sur le chemin exact fourni. `ComponentManifest` retourné tel que produit par le parser quand zéro diagnostic ; sinon refus fermé sanitisé (`manifest=None`, diagnostics non vide).
- `SUPPORTED_SCHEMA_VERSIONS` n'est consultée qu'à titre documentaire ; aucun pré-contrôle dupliquant `_check_schema_version`.

## 5. Sanitisation fermée

- Chaque diagnostic brut `« a : b »` est scindé une fois ; sans séparateur, vide, ou avec caractères de contrôle → repli.
- Élément : vocabulaire fermé issu des champs/sections publiés (`manifest`, `schema_version`, `id`, `type`, `version`, `name`, `dependencies`, `optional_dependencies`, `provides`, `implements` et leurs sous-chemins indexés à chiffres uniquement, indice généré par le parseur accepté sans plafond arbitraire). Toute clé inconnue/hostile (nom de secret, chemin privé, clé TOML exotique) → élément `manifest`. Jamais de chemin/clé brut recopié.
- Règle : vocabulaire fermé de règles sans valeur (`champ obligatoire manquant`, `champ non déclaré interdit`, `une chaîne est attendue`, …, `SemVer 2.0.0 complète attendue`, `expression exécutable refusée (…)`, `secret embarqué refusé (…)`, `TOML invalide : décodage impossible`, `fichier de manifest illisible`, `document texte invalide`, `entrée invalide`). Règle inconnue → `entrée invalide`.
- `schema_version` : la parenthèse `({version!r})` du parser est systématiquement supprimée → `schema_version : version de schéma non supportée` (cohérence « version concernée » par champ nommé, jamais par valeur).
- Repli fermé : `manifest : entrée invalide`.
- Erreurs de lecture/Unicode (`OSError`, `UnicodeError`) → `manifest : fichier de manifest illisible` sans détail (ni codec, ni position, ni octets). Syntaxe TOML → `manifest : TOML invalide : décodage impossible` sans ligne/colonne.

## 6. Fichiers d'implémentation et limites

- `src/pixs/developer_kit/__init__.py` : façade + `ValidationReport`, docstring du parcours local, limites explicites (pas de Kit complet, pas de conformité production).
- `src/pixs/developer_kit/validators.py` : implémentation + vocabulaires fermés, stdlib seule (`tomllib` via le parser noyau).
- `src/pixs/developer_kit/README.md` : parcours local (écrire `component.toml` → `validate_manifest_text/file` → lire diagnostics `champ : règle`), sans secret/réseau/production.
- `tests/unit/test_developer_kit_validators.py` : enveloppe (ok/manifest/diagnostics, immuabilité, `__post_init__` incohérent → `ValueError`), sanitisation et adversariaux (valeurs/noms malveillants vérifiés par prédicats d'absence, fixtures jamais affichées dans le rapport).
- `tests/integration/test_developer_kit_example.py` : `src/pixs/example/component.toml` validé via le kit, composition mémoire seule.
- Limites bornées : pas de CLI/API production, pas de scaffolding avec effets, pas de registre/publication, pas de nouvelle dépendance, pas de persistance, pas de modification noyau/specs/cadrages.

## 7. Vérifications

- Ciblés : `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p test_developer_kit_validators.py -v` avec `PYTHONPATH=src`, puis intégration exemple ; 100 % exigé.
- Régressions globales unit + intégration (`-B`, chemins absolus DEVOPS), AST Python, UTF-8/LF du périmètre, `openspec validate --all --strict` avec delta exact.
