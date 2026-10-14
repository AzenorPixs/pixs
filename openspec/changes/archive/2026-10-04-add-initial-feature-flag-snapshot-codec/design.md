# Design — codec backend pur du snapshot source

## API

Le module `src/pixs/backend/feature_flag_snapshot_codec.py` expose trois noms :

- `FeatureFlagSnapshotCodecError(ValueError)` ;
- `encode_feature_flag_source_snapshot(snapshot)` retournant un `dict` ;
- `decode_feature_flag_source_snapshot(document)` retournant un `FeatureFlagSourceSnapshot`.

L’exception utilise un message constant, sans écho de l’entrée, du champ, de l’identifiant, de la version ou du diagnostic refusé. Elle signale uniformément une entrée, une forme ou une liaison invalide.

## Document technique

La racine est un `dict` exactement composé des quatre clés :

- `configuration_version` : texte opaque littéral ;
- `definitions` : `list` exacte de définitions ;
- `assignments` : `list` exacte d’affectations ;
- `cohort_rules` : `list` exacte de règles.

Chaque définition est un `dict` exact portant les douze champs de la dataclass : `flag_id`, `flag_version`, `owner_component`, `purpose`, `value_schema`, `default_value`, `targeting_dimensions`, `cohort_key`, `prerequisites`, `fallback_policy`, `expires_at` et `audit_policy`. `targeting_dimensions` et `prerequisites` sont des `list` exactes de chaînes exactes ; `cohort_key` est la seule valeur pouvant être `None`.

Chaque affectation est un `dict` exact portant les huit champs : `flag_id`, `selector`, `selector_value`, `value`, `valid_from`, `valid_until`, `configuration_version` et `updated_by`. Chaque règle est un `dict` exact portant `cohort_key`, `subject_dimension`, `threshold_basis_points` et `configuration_version`.

Les chaînes, booléens et entiers restent littéraux. `bool` n’est jamais assimilé à `int`. Le codec n’ajoute aucune grammaire ni normalisation : les validateurs canoniques continuent de vérifier les horodatages, politiques, identifiants et références. Les versions opaques sont conservées et leurs liaisons exactes sont vérifiées par le validateur du lot ; aucun ordre entre versions n’est introduit.

## Fermeture des entrées

Pour chaque dictionnaire, les clés attendues sont vérifiées comme chaînes exactes avant tout `set`, hachage, égalité ou tri. Les types de conteneurs et de scalaires sont vérifiés avant tout accès susceptible d’exécuter un hook. Les listes doivent être exactement `list`, jamais sous-classe ou tuple.

### Encodage

`encode_feature_flag_source_snapshot` commence par exiger le type exact du snapshot, puis appelle réellement `validate_feature_flag_source_snapshot` sur le lot complet. Si le lot retourne un diagnostic, aucune extraction de champ n’est effectuée et l’opération est refusée.

Après validation, le codec lit les modèles connus et construit récursivement des dictionnaires et des listes neufs. Les tuples canoniques deviennent des listes au bord du document. Aucune conversion générique telle que `dataclasses.asdict` ou `copy.deepcopy` n’est utilisée. Les conteneurs retournés ne partagent aucune collection mutable avec le snapshot source.

### Décodage

`decode_feature_flag_source_snapshot` vérifie d’abord la forme complète : racine exacte, clés exactes, enregistrements exacts, types, listes et éléments. Les formes hostiles sont rejetées avant hachage d’une clé inconnue ou itération d’un objet inconnu.

Après la forme, le codec construit exactement une dataclass par enregistrement, les collections en tuples canoniques, puis le snapshot à quatre champs. Il appelle ensuite réellement le même validateur de lot complet et refuse tout diagnostic avant retour.

## Continuité normative

Le codec ne décide pas qu’une valeur affectée est compatible avec `value_schema`. Un lot structurellement accepté, mais produisant `INVALID` lors de l’évaluation R3, reste préservé. Il ne détecte pas une origine PostgreSQL ou JSONB, ne présume aucune unicité supplémentaire avant le stockage réel, ne normalise aucun alias et n’expose aucun contenu refusé.

Les 27 baselines et les 136 tests existants restent inchangés. Le développement cible Python 3.12 minimum, vérifié dans l’environnement Python 3.14.8.

## Tests

La suite unitaire comportera environ 12 à 16 méthodes causales : aller-retours complets, `False` distinct de `0`, chaînes Unicode et opaques conservées, versions et références littérales, conteneurs frais, absence de mutation, clés absentes ou supplémentaires, toutes formes hostiles sans callback, mauvais types exacts, liaisons de lot invalides, erreurs sans écho, et préservation d’un cas structurellement valide dont l’évaluation R3 demeure `INVALID` pour l’évaluateur.

L’intégration créera un processus frais avec les gardes éprouvées avant import : filesystem, réseau, sous-processus, horloge et PostgreSQL comptés nuls après usage. Elle fera réellement appel aux validateurs et à la composition existante, sans aucune E/S externe.
