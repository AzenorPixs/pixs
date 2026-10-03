# Developer Kit — validation locale de manifests (P0, local seul)

## Parcours local reproductible

1. Écrire un `component.toml` conforme au schéma publié (`component-model`).
2. Le valider via `pixs.developer_kit`, sans secret, sans réseau, sans activation ni publication.
3. Lire le `ValidationReport` immuable : soit le manifest validé, soit des diagnostics `champ : règle`.

## API (depuis `pixs.developer_kit`)

```python
from pixs.developer_kit import (
    ValidationReport,
    validate_manifest_file,
    validate_manifest_text,
)

report = validate_manifest_text(texte_toml)  # texte fourni, aucun accès FS
report = validate_manifest_file("chemin/exact/component.toml")  # str|Path
# fichier exact seulement sur demande explicite de l'appelant, sans traversée
```

Le manifest d'exemple existant `src/pixs/example/component.toml` sert de
référence de parcours ; il est lu tel quel, jamais réécrit.

## Lecture du rapport

- Succès : `report.ok is True`, `report.manifest` est le `ComponentManifest`
  public validé, `report.diagnostics == ()`.
- Échec : `report.ok is False`, `report.manifest is None`, chaque diagnostic
  nomme un champ du vocabulaire fermé et une règle fermée, sans reproduire
  valeur, clé brute, chemin privé ni version fournie ; repli fermé
  `manifest : entrée invalide`.
- Mésusage : `TypeError` si `text` n'est pas `str` ou si `path` n'est ni
  `str` ni `Path` (erreur de programmation, pas un refus de validation).
- Chemin NUL, fichier illisible, indécodable ou erreur Unicode : refus fermé
  `manifest : fichier de manifest illisible`, sans chemin, sans détail et
  sans traceback.

## Tests ciblés (répertoire projet, chemins DEVOPS)

```bash
/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p test_developer_kit_validators.py -v
/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration -p test_developer_kit_example.py -v
```

## Limites

Validateurs locaux de manifests uniquement : ni Kit complet, ni preuve de
conformité production, ni P0 global. Aucune exigence nouvelle.
