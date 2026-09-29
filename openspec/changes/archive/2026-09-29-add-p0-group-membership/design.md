# Design — add-p0-group-membership

## Modèles et réutilisation

`Group(group_id: uuid.UUID, context: ScopeContext)` et `Membership(user_id: uuid.UUID, group_id: uuid.UUID)` sont des dataclasses frozen, slots, repr=False, sans valeur par défaut. Leur construction appelle leur validateur.

Group exige un contexte explicite. TENANT désigne un groupe de tenant ; PLATFORM représente explicitement un groupe de plateforme sans tenant/scope. L'absence de contexte est refusée : aucun tenant ni accès par défaut n'est inventé. La validation de structure réutilise la façade scope ; elle ne prouve pas que le tenant ou scope existe dans une topologie. Le service applicatif futur devra vérifier cette topologie, les appartenances et l'autorisation avant usage.

Membership est ici une relation de paire utilisateur-groupe ; elle n'est pas présentée comme une entité persistée. Elle ne possède pas d'identifiant supplémentaire, de CRUD ou de transition. Les identifiants référencent User et Group. Plusieurs utilisateurs peuvent appartenir au même groupe et un utilisateur à plusieurs groupes ; les entités sans liaison restent valides.

Le helper UUID interne `identity.models._check_uuid` est réutilisé dans ce même package, sans copie ni refactoring. Le validateur User existant est réutilisé. Les consommateurs restent sur la façade publique. La validation UUID exige objet exact, version7, variant RFC_4122 et int interne valide, avant hachage.

## Contrats et erreurs

- `validate_group(value)` vérifie type Group exact, UUIDv7 et ScopeContext exact structurellement valide.
- `validate_membership(value)` vérifie type Membership exact et les deux UUIDv7.
- `validate_memberships(users, groups, memberships)` exige trois tuples exacts, revalide chaque membre avant égalité/hachage, refuse doublons d'IDs dans chaque ensemble et collision User/Group entre ensembles (TECHNICAL §13), puis refuse références absentes et paires répétées. Trois tuples vides sont valides. Aucun état n'est conservé et aucune entrée n'est modifiée.
- Tous retournent True ou lèvent `GroupError(ValueError)`, code stable `GROUP_INVALID`, message constant sans valeurs brutes. Les erreurs IdentityError, ScopeStructureError ou de champs incomplets sont converties en GroupError sans contexte d'exception exposé. Aucun str/repr/eq/hash d'une entrée invalide n'est appelé.
- Des relations vers des groupes de contextes différents peuvent être structurellement valides ; elles n'autorisent aucun accès, partage, héritage ou usage intertenant. Un groupe PLATFORM n'est jamais converti en TENANT.

La portée de ces contrôles est l'ensemble fourni. Ils ne prouvent pas l'unicité de toute une base, une appartenance authentifiée ni une transaction concurrente.

## Façade et fichiers

La façade `src/pixs/core/identity/__init__.py` conserve les dix exports existants et ajoute uniquement Group, Membership, GroupError, validate_group, validate_membership et validate_memberships. `core/__init__.py`, identity/models.py et scope restent inchangés.

`tests/integration/test_identity_facade.py` adapte seulement l'ensemble attendu des exports ; ses assertions fonctionnelles existantes sont conservées.

Un seul fichier unitaire `tests/unit/test_group_membership.py` couvre les modèles, enums de contexte, UUID, données incomplètes/altérées/hostiles, n:m, références, doublons, collision d'IDs et non-mutation par capture de valeurs primitives. `tests/integration/test_group_facade.py` exerce la façade avec User/Group/Membership et les contextes tenant/plateforme sans prétendre prouver une autorisation.

## Validation et limites

Les suites existantes se lancent séparément depuis tests/unit et tests/integration ; la découverte globale tests/ est incompatible avec un import existant du PDP et n'est pas utilisée. Contrôles AST des cinq fichiers Python concernés, UTF-8/LF des neuf fichiers du change et OpenSpec strict. Les tâches sont cochées sur preuves, l'archivage et STATISTIQUES.md restent deux mandats distincts.

Cette tranche n'implémente ni groupes imbriqués, cycle/profondeur, résolution d'annuaire, audit durable, invalidation de politique ni backend réel ; elle ne revendique pas l'achèvement général de core ou du P0.
