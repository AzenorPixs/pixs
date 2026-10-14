# Design — Adaptateur PostgreSQL initial pour source de fanions versionnée

## Contexte et décision

La source canonique `FeatureFlagSourceSnapshot`, ses validateurs et son codec existent déjà. Ils ne prouvent pas encore la provenance persistante de la version demandée.

La décision retenue est un premier adaptateur PostgreSQL strictement en lecture :

- l’app Django implicite `pixs.backend` est utilisée ;
- elle est déjà prouvée en processus frais avec `name = pixs.backend`, `label = backend`, registre prêt et zéro connexion ;
- deux nouveaux champs ORM suffisent : `TextField` comme clé primaire de configuration et `JSONField` pour le document canonique ;
- la migration initiale est un `CreateModel` Django standard, automatiquement réversible ;
- aucun `DeleteModel` personnalisé n’est ajouté ;
- le chargeur importe et active le modèle seulement après validation de la version demandée ;
- les `6` nouveaux fichiers et le `README` en append seul constituent tout le périmètre de livraison ;
- les `38` baselines sont préservées, seule la modification `README` étant autorisée ;
- les `154` tests de régression antérieurs restent inchangés et doivent continuer à réussir.

Ce change implémente partiellement `R4` : une source PostgreSQL versionnée en lecture. Il ne prétend ni prouver l’administration des affectations, ni l’audit, ni la corrélation des changements, ni la convergence des trois rôles, ni la garde des artefacts embarqués, ni l’accès multi-tenant sécurisé.

## Architecture retenue

```text
configuration_version
        ↓
FeatureFlagSourceSnapshotRecord.configuration_version = TextField(primary_key=True)
FeatureFlagSourceSnapshotRecord.snapshot              = JSONField()
        ↓
feature_flag_postgres_source.load_feature_flag_source_snapshot(...)
        ↓
feature_flag_snapshot_codec.decode_feature_flag_source_snapshot(...)
        ↓
FeatureFlagSourceSnapshot canonique
        ↓
evaluate_feature_flag_source_snapshot(...) (seulement dans les tests)
```

Aucune route, API HTTP, CLI, admin, cache, réglage Django réel ou activation runtime n’est ajouté.

## Modèle

Fichier :

```text
src/pixs/backend/models.py
```

Classe :

```python
FeatureFlagSourceSnapshotRecord
```

Champs exactement prévus :

```python
configuration_version = models.TextField(primary_key=True)
snapshot = models.JSONField()
```

Décisions :

- pas de champ `id`, `created_at`, `updated_at`, statut, actif, version d’artefact, tenant, scope ou audit ;
- pas de modèle abstrait ni héritage ;
- pas de `Index`, contrainte PostgreSQL, expression SQL, `db_comment`, option de schéma ou `SQL` personnalisés ;
- pas d’indice ni astuce PostgreSQL spécifique dans le modèle ou le code applicatif ;
- l’app est découverte implicitement par le nom `pixs.backend` ;
- le label effectif attendu est `backend` ;
- `apps.py` reste inchangé.

## Migration

Fichiers :

```text
src/pixs/backend/migrations/__init__.py
src/pixs/backend/migrations/0001_feature_flag_source_snapshot.py
```

La migration déclare `initial = True` et contient exactement le `CreateModel` du modèle. Django génère automatiquement l’opération inverse ; le fichier doit rester réversible sans `RunSQL`, `DeleteModel` ou dépendance PostgreSQL inventée.

La découverte de la migration est testée seulement après publication du fichier. La découverte préalable de l’app sans connexion ne doit pas être présentée comme une preuve de migration.

## Chargeur

Fichier :

```text
src/pixs/backend/feature_flag_postgres_source.py
```

API publique :

```python
class FeatureFlagSourceLoadError(ValueError):
    ...

def load_feature_flag_source_snapshot(
    expected_configuration_version: str,
) -> FeatureFlagSourceSnapshot:
    ...
```

Le chargeur retourne un snapshot canonique, jamais une évaluation. La composition réelle est vérifiée séparément par les tests à partir du snapshot chargé.

## Garde d’import paresseux

Le module du chargeur doit être importable :

- sans `settings.configure` ;
- sans `django.setup` ;
- sans accès à un modèle Django ;
- sans connexion PostgreSQL ;
- sans lecture d’environnement ;
- sans I/O ;
- sans horloge ;
- sans cache.

La version attendue est validée avant tout chargement paresseux du modèle. La règle est :

```python
type(expected_configuration_version) is str
and expected_configuration_version != ""
```

Le validateur existant utilise le type exact str et bool(value). Une chaîne contenant uniquement des espaces reste donc une version opaque non vide. Aucun strip, normalisation Unicode, repli, alias ou transformation de valeur n’est introduit. Un booléen, un objet, une chaîne vide et une chaîne non `str` sont refusés sans accès ORM.

Le modèle est résolu seulement après cette validation, via l’app label `backend`.

## Lecture exacte

Une version valide doit produire exactement une sélection par clé primaire :

```python
record = FeatureFlagSourceSnapshotRecord.objects.get(
    pk=expected_configuration_version
)
```

Conditions après lecture :

1. `type(record.configuration_version) is str` ;
2. `record.configuration_version == expected_configuration_version` ;
3. `record.snapshot` est transmis au codec existant ;
4. le codec décode et valide l’ensemble du lot ;
5. le snapshot restitué doit être de type exact `FeatureFlagSourceSnapshot` ;
6. `snapshot.configuration_version == expected_configuration_version` ;
7. le snapshot canonique est retourné.

Aucun filtre partiel, aucune récupération de plusieurs lignes, aucune jointure, aucun `select_related`, aucune écriture, aucun DML et aucun DDL ne sont possibles dans le chemin applicatif de chargement.

## Normalisation des erreurs

Le message public est fixe :

```text
Source de fanions indisponible
```

Les seules anomalies attendues normalisées sont :

- absence de ligne via le `DoesNotExist` exact du modèle ;
- `django.db.utils.DatabaseError` ;
- `FeatureFlagSnapshotCodecError`.

Toute autre exception est propagée, notamment :

- erreurs de configuration Django ;
- erreurs d’environnement ;
- erreurs de registre d’applications ;
- `TypeError` ou `ValueError` inattendus non portés par le codec ;
- interruptions, `KeyboardInterrupt` et `SystemExit` ;
- erreurs de programmation non prévues.

La transformation d’une erreur attendue vers `FeatureFlagSourceLoadError` ne doit révéler :

- la version demandée ;
- le contenu du snapshot ;
- le nom de la table ou du schéma ;
- un message SQL ou PostgreSQL ;
- un credential ;
- la cause d’origine ;
- un traceback technique.

Aucune journalisation n’est ajoutée.

## Tests unitaires sûrs

Fichier :

```text
tests/unit/test_feature_flag_postgres_source.py
```

Ils couvrent au minimum :

- import du module de chargeur sans réglage, setup, modèle, connexion ou I/O ;
- signature et API publique exactes ;
- refus avant ORM pour :
  `None`,
  booléen,
  objet,
  chaîne vide ;
- conservation exacte d’une version opaque, sans normalisation ;
- préservation de la valeur `False` du snapshot après round-trip ;
- lecture par clé primaire exacte via un gestionnaire instrumenté ;
- vérification du type et de l’égalité de la clé primaire renvoyée ;
- validation du lien entre version demandée et version interne ;
- décodage complet du lot par le codec ;
- refus d’un lot incohérent avec son `configuration_version` ;
- refus du document corrompu ;
- refus de l’absence ;
- refus d’un `DatabaseError` attendu ;
- propagation d’une erreur inattendue ;
- absence de `save`, `delete`, `create`, `update`, transaction ou DDL dans le chargeur ;
- absence de cache, horloge, environnement et effet secondaire.

## Tests d’intégration sûrs en processus frais

Fichier définitif validé :

```text
tests/integration/test_feature_flag_postgres_source_integration.py
```

Le subprocess utilise une configuration Django synthétique et des gardes réellement éprouvées contre :

- `psycopg.connect` ;
- `psycopg.Connection.connect` ;
- `DatabaseWrapper.get_new_connection` ;
- sockets et connexions réseau ;
- accès fichiers et environnement sensibles ;
- setup ou réglage inattendu lors de l’import du chargeur.

Il vérifie :

- `INSTALLED_APPS` avec seulement `pixs.backend` ;
- `name == pixs.backend` ;
- `label == backend` ;
- registre prêt ;
- deux champs ORM exacts ;
- absence de champ ID implicite ;
- découverte de `0001_feature_flag_source_snapshot.py` après publication ;
- absence de connexion et zéro appel à `get_new_connection` ;
- comportement du chargeur avec le modèle et gestionnaire instrumentés ;
- composition réelle avec `evaluate_feature_flag_source_snapshot` :
  - sélection C2 déterministe ;
  - membre et non-membre de cohorte ;
  - repli R3 `DENY` ou `DEFAULT` ;
  - expiration de définition ;
  - version canonique incompatible refusée.

Les gardes doivent prouver leur activation avant le travail et leur appel nul après, sans masquer les échecs.

## Commande PostgreSQL réelle dédiée

Elle ne fait pas partie de la suite par défaut et nécessite un mandat distinct. Durée maximale visée : `120 s` ou moins.

### Approvisionnement strictement borné

- Le processus réel autorisé est seul autorisé à charger `project.env`.
- Les credentials et valeurs de connexion restent en mémoire.
- Aucune commande `CREATE DATABASE`, `DROP DATABASE`, `CREATE ROLE`, `DROP ROLE` ou `GRANT` n’est exécutée.
- Le schéma de test est unique à chaque exécution.
- Aucun objet dans `public` n’est utilisé ou modifié.
- La base autorisée est uniquement la base de test déjà disponible.

### Isolation de schéma

Le nom de schéma est construit de façon contrôlée et appliqué exclusivement par des identifiants :

```python
psycopg.sql.Identifier(schema_name)
```

Séquence :

1. vérifier que le nom de schéma ne collide pas avec un objet préexistant ;
2. en cas de collision, refuser immédiatement avec un diagnostic fixe ;
3. ne tenter ni appropriation, ni nettoyage d’un objet préexistant ;
4. créer le schéma éphémère ;
5. placer strictement `search_path` sur ce seul schéma ;
6. n’ajouter aucune référence `public` comme solution de repli ;
7. exécuter migrations et ORM uniquement dans ce périmètre.

### Migration cible backend

- Le chargeur/plan de migration est borné à l’app `backend`.
- Les tables auxiliaires Django nécessaires dans le schéma éphémère restent locales à ce schéma.
- Aucune table préexistante de l’installation n’est ciblée.
- La preuve inclut l’application de la migration puis sa réversibilité en `migrate backend zero` dans le même schéma isolé.

### Round-trip fonctionnel

Données exclusivement synthétiques :

1. construire une définition, une affectation et une règle de cohorte valides ;
2. encoder le snapshot canonique ;
3. insérer la version exacte dans le schéma éphémère ;
4. relire via `load_feature_flag_source_snapshot` ;
5. comparer structurellement le snapshot restitué à l’original ;
6. vérifier la préservation de types et valeurs, notamment `False`, entiers et textes opaques ;
7. modifier ou corromper contrôlé dans le schéma pour vérifier le refus ;
8. tenter une version absente, une corruption de document et une divergence PK/version interne ;
9. confirmer les refus génériques ;
10. charger une version valide avec une seule catégorie `SELECT` et zéro écriture.

### Métriques et journalisation

- Les requêtes peuvent être capturées en mémoire privée.
- Seules les catégories `SELECT`, `INSERT`, `UPDATE`, `DELETE` et DDL sont exposées comme compteurs.
- Aucun texte SQL, nom de table, nom de schéma, credential, valeur de version, payload ou diagnostic interne ne doit apparaître.
- stdout/stderr/logs utilisés pendant la phase de credentials et ORM sont redirigés vers des tampons privés ou supprimés.
- La sortie finale est fermée et limitée à une indication de succès ou d’échec et à des compteurs autorisés.

### Nettoyage et erreurs

- Toute connexion ouverte est fermée.
- Le schéma éphémère créé est supprimé en `CASCADE`, seulement si sa création lui est attribuée.
- Le nettoyage est tenté en cas de succès ou d’échec fonctionnel.
- Un échec de cleanup est signalé par un diagnostic fixe et ne masque jamais l’échec original.
- Un échec de création de schéma, de collision, de migration, d’ORM ou de nettoyage doit rendre la commande en échec explicite.

## Rollback de production

La migration Django est automatiquement réversible. Une restauration en production consisterait en une exécution explicite et ciblée, par exemple `migrate backend zero`, mais elle doit rester :

- hors de ce change ;
- précédée d’un mandat distinct ;
- limitée à l’app backend ;
- accompagnée d’une vérification de dépendances et de perte de données ;
- traitée comme une opération destructive autorisée ;
- jamais déclenchée par une simple validation de tests.

Aucune opération de production n’est exécutée ici.

## Documentation

`src/pixs/backend/README.md` est modifié uniquement par append. Le texte documente :

- l’app backend implicite ;
- la table et la migration ;
- la lecture d’un snapshot canonique versionné ;
- la précondition que la provenance du contexte serveur canonique reste une responsabilité de l’appelant ;
- l’absence d’API route, runtime activation, admin, audit, corrélation, cache, convergence des rôles et garde de build.

## Limites conservées

Première livraison partielle de `R4` :

- administration non prouvée ;
- audit non prouvé ;
- corrélation non prouvée ;
- convergence `web`/`worker`/`scheduler` non prouvée ;
- runtime activation non prouvée ;
- garde contre affectations embarquées non prouvée ;
- contrôle d’accès tenant/scope non prouvé ;
- cache et invalidation non fournis ;
- version active non sélectionnée.

## Conditions de preuve et séquence de clôture

Le nombre de tâches est déterminé par la couverture réellement nécessaire, sans quota fixe. Avant archivage, code, tests, cohérence et tâches cochées doivent être prouvés. L’autorisation et le mandat d’archive viennent ensuite ; la production et la vérification du rapport statistique viennent après archive, avant TERMINÉ. Les jalons successifs sont :

- code et tests applicables réellement réussis ;
- suite complète préservée ;
- tests PostgreSQL réels dédiés réussis dans un schéma éphémère nettoyé ;
- cohérence entre proposal, design, specs et tâches ;
- stricts change et canonique réussis ;
- tâches cochées seulement après preuves ;
- archivage autorisé séparément après contrôle CGPT ;
- `STATISTIQUES.md` post-archivage produit sous mandat distinct ;
- aucune tâche ou statistique ne déclare `TERMINÉ` avant ses preuves propres ;
- aucune circularité entre archivage, tâches et rapport statistique.
