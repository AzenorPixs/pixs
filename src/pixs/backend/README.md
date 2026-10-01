# Backend Pixs — fondation préparatoire P0

Fondation partielle Django 5.2.17 et psycopg 3.3.5, compatible Python >= 3.11.
Aucun service opérationnel, aucune persistance démontrée.

## API

Quatre noms publics via `pixs.backend` :

- `SettingsTemplate`
- `build_settings_template`
- `check_template`
- `inspect_roles`

Les références de secret réutilisent la classe publique du Kernel
`pixs.kernel.config.resolution.SecretReference`. Elles restent opaques,
distinctes et non résolues.

## Construction en mémoire

```python
from pixs.backend import build_settings_template
from pixs.kernel.config.resolution import SecretReference

config = {"PIXS_PROFILE": "web"}
gabarit = build_settings_template(
    profile=config["PIXS_PROFILE"],
    database={
        "name": "db-synthetique",
        "user": "u-synthetique",
        "host": "example.invalid",
        "port": 5432,
    },
    allowed_hosts=["localhost"],
    secret_key_ref=SecretReference(
        owner_id="pixs.backend",
        entry_id="django_secret_key",
        source="vault://exemple/opaque-cle",
    ),
    database_password_ref=SecretReference(
        owner_id="pixs.backend",
        entry_id="db_password",
        source="vault://exemple/opaque-mdp",
    ),
)
```

Règles :

- `profile` transmis explicitement depuis `config["PIXS_PROFILE"]`,
  sans environnement ni valeur par défaut.
- `database` contient exactement `name`, `user`, `host`, `port`.
- `allowed_hosts` est explicite, sans wildcard ni espaces.
- Références distinctes obligatoires, non résolues.
- Objet figé, `ready` toujours faux.
- `non_secret_settings` est insuffisant sans `SECRET_KEY` ni `PASSWORD`.
- Les trois rôles `web`, `worker` et `scheduler` restent indisponibles.

Exemple sans Django, sans réseau et sans vrai secret ni credential.

## Parcours synthétique

Depuis la racine du projet :

```text
/home/devops/python/current/bin/python3 -m venv .venv-backend-foundation
```

Chaque commande fait l'objet d'un mandat CAB distinct.

```text
./.venv-backend-foundation/bin/python -m pip --isolated install --index-url https://pypi.org/simple --no-cache-dir --disable-pip-version-check Django==5.2.17 psycopg==3.3.5
```

Tests ciblés backend :

```text
./.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.insert(0, 'src'); suite = unittest.defaultTestLoader.discover('tests', pattern='test_backend_*.py'); result = unittest.TextTestRunner(verbosity=2).run(suite); sys.exit(not result.wasSuccessful())"
```

Régressions unitaires (UNIT) :

```text
./.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.insert(0, 'src'); suite = unittest.defaultTestLoader.discover('tests/unit'); result = unittest.TextTestRunner(verbosity=1).run(suite); sys.exit(not result.wasSuccessful())"
```

Régressions d'intégration (INTEGRATION) :

```text
./.venv-backend-foundation/bin/python -B -c "import sys, unittest; sys.path.insert(0, 'src'); suite = unittest.defaultTestLoader.discover('tests/integration'); result = unittest.TextTestRunner(verbosity=1).run(suite); sys.exit(not result.wasSuccessful())"
```

Chaque suite suit sa propre racine de découverte, à exécuter une par une. La convention de tests/unit/test_pdp_time.py importe test_pdp_decision par nom de module, d'où la découverte séparée sans modification des tests. Ces commandes sont des instructions reproductibles, pas des preuves
déjà effectuées ; le détail des résultats est porté par les rapports de session.

## Vérifications

Quatre sous-processus neufs : un import pur sans Django et un par rôle
Django `web`, `worker`, `scheduler`.

La conversion du gabarit vers des réglages Django avec valeurs
synthétiques existe seulement dans le harnais de tests. Les gardes sur
le wrapper PostgreSQL concret, `psycopg` et les sockets vérifient zéro
connexion, avec `run_checks(databases=[])`. La configuration globale du
parent reste préservée.

## Limites P0

Pas de fournisseur de secret, persistance, migration, modèle, API,
serveur, worker, scheduler, frontend ou déploiement. Pas de SQLite, Git,
environnement réel ou PostgreSQL réel.

Ceci n'est pas un artefact de readiness de production. Les contrôles synthétiques valident cette fondation préparatoire ; ils ne prouvent ni disponibilité de service ni persistance réelle.
