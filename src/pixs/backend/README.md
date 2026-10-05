# Backend Pixs — fondation préparatoire P0

Fondation partielle déclarée Django 6.1.1, psycopg[binary] 3.3.6,
asgiref 3.12.1 et sqlparse 0.6.0, avec Python >=3.12 dans `pyproject.toml`.
L'extra `binary` impose psycopg-binary 3.3.6. Ces cinq versions sont installées et
qualifiées sur Python 3.14.8 : 736 tests UNIT et 185 tests INTEGRATION réussis,
sans échec ni test ignoré, et `pip check` conforme. L'interpréteur est inchangé.
Le projet devra suivre la dernière stable officielle supportée de Django et la
règle n° 2 pour toutes ses dépendances, psycopg compris : dernières versions
compatibles avec Django, le Python actuel et le graphe complet. Toute évolution
incompatible avec le Python actuel reste soumise à la décision exclusive du
développeur. Les versions de ce relevé ne constituent pas des verrous permanents.
La politique et le relevé horodaté sont décrits dans
[TECHNICAL.md § 41.1](../../../TECHNICAL.md#411-politique-de-version-django).
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

Les versions exactes qualifiées sont maintenant déclarées dans `pyproject.toml`.
Toute installation ou évolution devra suivre la politique Django stable courante,
la règle n° 2 et le support du Python actuel pour toutes les dépendances, psycopg
compris. Les tests ci-dessous décrivent le harnais synthétique en environnement
dédié ; la qualification du relevé courant utilise l'interpréteur déclaré dans
`DEVOPS.md`. Chaque commande conserve son mandat CAB distinct.

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

## Déclarations de composants initiales

`src/pixs/backend/composition_initial.py` expose quatre constantes publiques : `COMPOSITION_VERSION`, `MANIFEST_PATHS`, `OFFICIAL_IDS`, `REQUIRED_IDS`.
Les trois manifests sont `src/pixs/kernel/component.toml` (KERNEL 0.1.0), `src/pixs/core/component.toml` (MODULE 0.1.0, dépendance `pixs.kernel ==0.1.0`) et `src/pixs/example/component.toml` (1.0.0 préservé).
`official_ids` et `required_ids` sont portés en données via l'API publique `discover`/`validate`/`resolve`/`compose`.
`validate`/`resolve` réussis ne prouvent aucune activation. `compose` sans attestations refuse : pas de P0, de compatibilité globale, de readiness, de démarrage Django, de PostgreSQL, de worker ni de scheduler.
Tests ciblés `tests/unit/test_initial_component_declarations.py` en unittest sans base ni secret ni réseau ; commande reproductible `Python -B` avec `sys.path` vers `src` et découverte `tests/unit` motif `test_initial_component_declarations.py`, sans preuve avant exécution.
Pas de nouveau package, export ou configuration.

## Limites P0

Pas de fournisseur de secret, persistance, migration, modèle, API,
serveur, worker, scheduler, frontend ou déploiement. Pas de SQLite, Git,
environnement réel ou PostgreSQL réel.

Ceci n'est pas un artefact de readiness de production. Les contrôles synthétiques valident cette fondation préparatoire ; ils ne prouvent ni disponibilité de service ni persistance réelle.

## Entrée `manage.py` — jalon partiel

`manage.py` délègue à `django.core.management.execute_from_command_line`. `main(argv=None)` accepte un argv explicite ou utilise `sys.argv`, sans réglage par défaut, composition ni attestation.

Seul `django.core.exceptions.ImproperlyConfigured` est capturé : le message fixe `Configuration Django requise; aucun réglage par défaut.` est écrit sur stderr, avec sortie 2 et sans traceback ni exception brute. Les tests CLI isolés vérifient `--help` et `--version` (sortie 0), ainsi que `check` sans configuration (sortie 2). Aucun serveur ni migration n'est exécuté par ces tests.

`DJANGO_SETTINGS_MODULE` reste la configuration runtime standard future, sans valeur distribuée ni chargement pour ces tests. `--help` ne prouve ni activation, ni P0, ni PostgreSQL, ni readiness, ni projet complet.

## Vue liveness bornée

Module direct `src/pixs/backend/liveness_view.py` : GET/HEAD renvoient 200 vide ; les autres méthodes, 405 vide avec `Allow: GET, HEAD`.
Toutes ces réponses utilisent `text/plain; charset=utf-8` et `Cache-Control: no-store`.
Les URL doivent être déclarées explicitement ; le module ne distribue aucune route publique.
Cette vue prouve seulement le traitement de la requête, sans readiness, startup, P0 ni disponibilité globale.
Elle ne consulte aucune base, aucun secret et ne réalise aucune mutation.

## Littéraux statiques de la garde

`_require_path` admet les points internes seuls (`index.html`, `assets/index-HASH.js`) ; refus point initial/final, `..`, segments dot, traversal, wildcard. Aucune route publique distribuée.

## Adaptateur shell borné

`build_shell_views(dist_root)` précharge `index.html` + `assets` js/css (1MiB/fichier, 64 fichiers, 8MiB total), sans symlink/caché/traversal. GET corps exact, HEAD sans corps, 405 + Allow, MIME exact, no-store. Aucune URL publique distribuée.

## Document OpenAPI borné

`build_openapi_view(plan, document)` sert un document 3.1.0 borné (64KiB, info.version == version contrat, chemins sous préfixe majeur, application/json seul, schéma inline minimal). GET corps exact, HEAD sans corps, 405 + Allow, JSON + no-store. TEST seul, ni P0 ni production.

## Composition TEST locale conjointe

La fabrique `build_local_test_urlpatterns(dist_root, plan, document, capacity, ...)` réunit des routes TEST littérales explicites : `health/live`, racine du shell, assets préchargés, document `api/v<majeure>/openapi.json` et capacité fournie par l’appelant. Le chemin de cette capacité doit figurer dans le document OpenAPI et sous le préfixe majeur du plan. Les déclarations privées fournies sont refusées par la garde (403), les routes inconnues donnent 404 ; `unknown_ui_route` permet uniquement un littéral UI explicite en TEST. Les noms des déclarations de l’appelant sont conservés ; collisions de noms et chemins sont refusées.

Dépendances déjà présentes : Python compatible 3.11, Django et psycopg, dist TanStack construit séparément. La fabrique lit ce dist de façon bornée, sans configurer Django ni ouvrir de serveur ou de connexion PG. L’appelant configure son application WSGI TEST fraîche ; les fixtures fournissent uniquement l’ENGINE PostgreSQL, avec apps et middleware vides, sans secret ni donnée métier. Le plan, le document et la réponse de capacité synthétique sont cohérents et explicites dans les tests.

Le contexte `local_test_server(application, host=..., port=...)` accepte seulement `127.0.0.1` et un entier exact entre 0 et 65535. Le port 0 est éphémère pour le test du cycle ; le harnais navigateur utilise 5173. Il démarre le thread WSGI, puis demande l’arrêt, joint le thread et ferme la socket en sortie normale ou après une exception du corps. L’arrêt synchrone attend la fin du handler courant : l’appelant doit fournir des handlers TEST finis, et les processus de test ont des délais explicites. Une application arbitraire qui ne retourne jamais ne peut pas être annulée par ce helper.

Kernel/Core, P0, readiness, worker, scheduler et connexion PG ne sont pas pris en charge par cette composition TEST ; cela ne décrit pas leur présence sur la machine. Ce profil n’est pas un déploiement de production. Le Client teste sans socket ni PG ; le cycle WSGI et le navigateur font des requêtes réelles en boucle locale, avec gardes PG actives et nettoyage observé. Le script Chromium existant reste inchangé, avec profil éphémère et protections conservées.

Commande du harnais avec les exécutables déclarés dans `DEVOPS.md` : `/usr/bin/env -i PATH=/usr/bin:/bin:/home/devops/node/current/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/home/devops/datas/pixs/frontend/.cache /home/devops/datas/pixs/.venv/bin/python -B /home/devops/datas/pixs/tests/integration/check_local_composition_browser.py`. Node utilise `/home/devops/node/current/bin/node` et Chromium `/usr/lib/chromium/chromium`. Aucun build ou changement frontend n’est nécessaire pour ce harnais.

## Adaptateur Django explicite — enregistrement seul

`src/pixs/backend/apps.py` expose les classes `PixsKernelConfig`, `PixsCoreConfig` et `PixsExampleConfig`. Leurs noms d’application sont respectivement `pixs.kernel`, `pixs.core` et `pixs.example`, leurs labels stables `pixs_kernel`, `pixs_core` et `pixs_example`. Les trois classes ont `default = False` : le caller TEST les sélectionne explicitement dans `INSTALLED_APPS` par `pixs.backend.apps.PixsKernelConfig`, `pixs.backend.apps.PixsCoreConfig` et `pixs.backend.apps.PixsExampleConfig`. L’adaptateur n’appelle aucun setup, réglage, pipeline, connexion ou activation à l’import et hérite du `ready` sans hook.

La configuration TEST fraîche des preuves utilise uniquement ces trois applications, aucun middleware et l’ENGINE PostgreSQL, sans valeur de connexion ni secret. Le registre Django rempli en TEST (`apps.ready`) ne prouve pas la readiness globale du projet ni une composition P0. Le module `pixs.example` correspond au composant technique `example.hello` du manifest ; cet identifiant reste inchangé. Les manifests, le pipeline pur, les réglages préparatoires, les contrôles et `manage.py` sont préservés ; `manage.py check` conserve son diagnostic préparatoire et sa sortie 2 sans configuration valide. Aucun modèle, service, provider, serveur, secret ou choix `default_auto_field` n’est ajouté.


## Preuve initiale partielle

`src/pixs/backend/composition_proof.py` expose `build_initial_proof(manifest_texts)` pour la composition initiale seule. Le caller fournit un tuple exact de trois textes de manifests déclaratifs, chacun non vide et limité à 64 KiB UTF-8 ; les identifiants et types initiaux requis sont validés. Le helper appelle réellement `discover`, `validate` et `resolve` publics et retourne une chaîne JSON canonique interne versionnée `0.1.0`, avec graphe, ordre et déclarations minimales validées. Deux appels et les permutations des mêmes manifests produisent les mêmes octets.

La preuve est partielle : `activated` et `globally_compatible` restent faux. La portée effectivement évaluée couvre seulement composants, capacités et contrats ; conformité, profils et les autres dimensions non évaluées sont explicitement listés. Aucun texte brut, message de diagnostic, nom opaque, fallback, secret, hash de manifest, attestation ou warning inventé n’est émis. Aucun fichier, réglage, connexion ou serveur n’est ouvert par ce helper ; un refus est générique. Ceci ne prouve ni P0 ni readiness globale.


## Journal local corrélé

`src/pixs/backend/correlated_log.py` expose parse 00 partiel et émission unique vers sink caller trusted. Le caller fournit traceparent déjà valide, correlation_id existant et composant initial connu ; le helper retourne None après une seule écriture observée. Le sink appartient au caller : aucune flush ni close ni lecture, aucune livraison externe. Une écriture partielle ou en échec peut déjà avoir un effet et n est jamais relancée. Référence primaire W3C https://www.w3.org/TR/trace-context/ pour le seul format 00 pris en charge. Ceci ne prouve ni métriques ni traces globales ni propagation runtime.


## Sonde connectivité PG bornée

Module `src/pixs/backend/pg_connectivity.py` : une seule sonde ASYNC `SELECT 1`, sur une connexion explicitement détenue puis fermée. IP littérale unique avec `host` et `hostaddr` identiques, `connect_timeout` entier exact `>= 2` choisi par le caller. La borne de requête est une attente locale coopérative `asyncio.wait` choisie par le caller : ce n'est ni une garantie de délai physique ni une borne libpq ; en cas de dépassement local observé, la connexion est fermée avant l'annulation de la tâche de requête. Refus générique fixe `pg connectivity invalid` sans valeur de connexion, traceback libpq ni secret ; aucun état global, aucune DDL, aucune option persistante, aucun chemin de secrets inventé.

`tests/unit/test_pg_connectivity.py` exécute des doubles coopératifs et négatifs sans PG réel ni réseau. `tests/integration/test_pg_connectivity_integration.py` exécute un double sûr sans réseau et, uniquement dans une commande dédiée sous mandat, une vraie connexion `SELECT 1` dont la fermeture effective (`conn.closed`, `cur.closed`) y est observée par les tests ; cette fermeture observée dans les tests reste distincte du résultat booléen retourné par le helper.

Le sous-jalon prouve seulement une connexion `SELECT 1` réelle locale. Il ne prouve ni disponibilité globale, ni P0, ni persistance métier, ni readiness. Les valeurs conn 2 s, requête 2 s, statement 1500 ms et timeout global processus 12 s sont des constantes de test uniquement.

## Classificateur de snapshots santé pur

Module `src/pixs/backend/health_classifier.py` : `classify_health(*, alive, startup_complete, pg_available, required=(), optional=())` classifie un snapshot fourni par le caller en quatre types de contrôles séparés. La vivacité est `alive` seule, indépendante de PG ; le démarrage est `startup_complete` du snapshot ; la disponibilité exige vivacité, démarrage, PG et toutes les dépendances obligatoires ; `degraded` signale indépendamment les seules dépendances explicitement optionnelles en échec, sans masquer une disponibilité fausse. PG est un opérande obligatoire de la disponibilité : `required_count` = `1 + len(required)` et `required_ok_count` = `int(pg_available) + sum(required)` incluent PG ; `optional_count` et `optional_ok_count` couvrent les autres optionnels seulement.

Sortie : dict neuf champs fixes par appel — `liveness`, `startup`, `availability`, `degraded`, `pg_available`, `required_count`, `required_ok_count`, `optional_count`, `optional_ok_count` — nouveau et indépendant à chaque appel ; les comptes constituent le diagnostic, sans chaîne `DEGRADED` publique.

Gardes : types exacts `bool` et `tuple` vérifiés avant toute longueur ou itération ; longueurs des deux tuples vérifiées avant inspection des éléments ; limite interne constante privée de 256 booléens par tuple, sans configuration ni norme publique. Tout refus est `ValueError("Invalid health snapshot") from None`, sans valeur brute ni nom de champ ; `from None` masque la chaîne de contexte, sans supprimer la pile Python.

Aucun IO, aucun import Django, aucune fonction ou callback de sonde, aucun retest PG, aucun paramètre d'environnement ou de configuration, aucune route, aucun état global. Aucun contrat public ni exigence normative ajoutée.

Exemple exécutable :

```python
from pixs.backend.health_classifier import classify_health

snapshot = classify_health(
    alive=True,
    startup_complete=True,
    pg_available=True,
    required=(True,),
    optional=(True, False),
)
print(snapshot)
```

Tests : `tests/unit/test_health_classifier.py` (objets doubles, matrice combinatoire 32 cas, hostiles, bornes 256/257 des deux tuples, espion de type, dict neuf indépendant, sans réseau ni PG réel) et `tests/integration/test_health_classifier_integration.py` (subprocess frais via `sys.executable`, gardes installées avant l'import du helper, sans PG ni réseau réels).

Commandes reproductibles, exécutable Python déclaré dans `DEVOPS.md` :

```text
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops/python/current/bin/python3 -B -m unittest discover -s /home/devops/datas/pixs/tests/unit -p test_health_classifier.py -v
```

```text
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops/python/current/bin/python3 -B -m unittest discover -s /home/devops/datas/pixs/tests/integration -p test_health_classifier_integration.py -v
```

Ce sous-jalon prouve seulement la classification pure d'un snapshot mémoire. Il ne prouve ni disponibilité globale, ni P0, ni readiness, ni persistance ; il n'exécute aucune sonde, ne lit aucune donnée ni variable d'environnement et ne consulte aucun secret.


## Source PostgreSQL versionnée des fanions — preuve partielle R4

La limite P0 « aucune persistance démontrée » conserve son sens historique. Ce sous-jalon ajoute seulement une première preuve partielle R4 : une table de snapshots canoniques et une API de lecture. Il ne déclare ni P0, ni production, ni readiness globale.

`src/pixs/backend/models.py` définit `FeatureFlagSourceSnapshotRecord` avec exactement deux champs : `configuration_version` comme `TextField` clé primaire et `snapshot` comme `JSONField`. La table Django standard est `backend_featureflagsourcesnapshotrecord`. L’app `pixs.backend` est enregistrée implicitement sous le label `backend` ; les trois configurations d’app antérieures restent inchangées. Aucun administrateur, audit, corrélation, convergence `web`/`worker`/`scheduler`, garde de build, route ou API HTTP n’est ajouté.

`src/pixs/backend/migrations/0001_feature_flag_source_snapshot.py` est une migration initiale standard, sans dépendance, constituée d’un seul `CreateModel` réversible. Elle ne transporte aucune infrastructure de gestion de schéma : l’application des migrations avant et arrière est seulement exercée par tests explicites.

`src/pixs/backend/feature_flag_postgres_source.py` expose `load_feature_flag_source_snapshot(expected_configuration_version)`. Son import reste pur : aucun réglage, aucun `django.setup()` et aucun modèle ne sont chargés. L’appelant doit configurer Django explicitement avant l’appel.

L’API accepte seulement une valeur de type exact `str` non vide, y compris une chaîne composée uniquement d’espaces, transmise sans normalisation ni `strip()`. Elle lit exactement la ligne désignée par la clé primaire attendue, vérifie la version interne, puis décode le document avec le codec canonique. Aucun contrôle de tenant, cache, runtime ou corrélation n’est réalisé : le caller et son serveur restent responsables de la connexion, de la configuration, de l’isolation et du cycle de vie.

En échec attendu — absence, erreur de base ou refus du codec — l’API lève `FeatureFlagSourceLoadError` avec le message fixe `Source de fanions indisponible` et sans chaîne d’origine. Les erreurs inattendues sont propagées ; l’appelant de confiance doit donc contrôler ses diagnostics. Le chargeur ne journalise rien et son refus normalisé n’expose aucune valeur, requête ou cause technique.

Les preuves locales observées couvrent l’absence de modèle au moment de l’import, les refus et lectures simulées, la réussite d’un aller-retour réel en schéma isolé, la migration avant/arrière, l’unique `SELECT` public attendu, le nettoyage et la fermeture des connexions. Cette preuve reste partielle : elle valide la source versionnée en lecture, pas l’administration, l’activation des rôles ni la disponibilité d’un service.
