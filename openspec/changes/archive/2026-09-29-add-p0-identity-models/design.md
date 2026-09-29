# Design — add-p0-identity-models

## Modèles et représentation

`src/pixs/core/identity/models.py` utilise uniquement dataclasses, enum et uuid de la bibliothèque standard.

- `IdentityType(Enum)` : HUMAN, SERVICE, DEVICE, FEDERATED ; valeurs textuelles identiques aux noms.
- `IdentityState(Enum)` : ACTIVE, SUSPENDED, REVOKED, EXPIRED ; valeurs textuelles identiques aux noms.
- `User(user_id: UUID)`, `DigitalIdentity(identity_id: UUID, identity_type: IdentityType, state: IdentityState)`, `IdentityLink(user_id: UUID, identity_id: UUID)` : dataclasses frozen, slots, repr=False ; aucune valeur implicite. Chaque construction appelle son validateur.
- Les UUID doivent être des objets `uuid.UUID` exacts, version 7 et variant `RFC_4122`. Aucun cast, génération, parsing ou normalisation implicite. Une future frontière de transport assurera son propre parsing.
- Le type SERVICE représente le compte de service ; aucune classe distincte ni état ACTIVE conférant un droit. Tous les états restent des valeurs structurelles, sans transition inventée.

## Contrats de validation

`validate_user(value)`, `validate_identity(value)` et `validate_link(value)` valident les types exacts et tous les champs, retournent True ou lèvent `IdentityError`. Les instances incomplètes ou altérées sont refusées avec la même erreur stable. Aucun appel à str, repr ou conversion d'une entrée invalide ; validation des types avant égalité ou hachage. Les validateurs n'accèdent pas à un provider, fichier, réseau ou stockage.

`validate_links(users, identities, links)` exige trois tuples exacts. Il revalide leurs membres avant de construire les ensembles d'identifiants. Les IDs sont uniques dans users, dans identities et entre les deux ensembles : un UUID partagé par un utilisateur et une identité est refusé, conformément à l’unicité globale de TECHNICAL §13. Chaque liaison référence des entités présentes ; un utilisateur ou une identité ne peut apparaître dans plusieurs liaisons. Une liaison répétée est donc également rejetée. Les entités sans lien et trois tuples vides sont valides. La fonction retourne True sans modifier, conserver ou exposer les entrées.

`IdentityError(ValueError)` expose le code stable `IDENTITY_INVALID` et un message constant sans valeur brute. Les classes d'entrées frauduleuses et leurs méthodes spéciales ne sont pas invoquées pour formater l'erreur. Les identifiants valides sont comparés uniquement après validation.

## Façades

`pixs.core.identity` exporte les trois modèles, les deux enums, IdentityError et les quatre validateurs via `__all__`. `pixs.core` ajoute identity à son import et à `__all__`, en conservant scope. Aucun changement de l'API authz existante.

## Tests et limites

- `tests/unit/test_identity_models.py` : UUIDv7 de fixtures, autres versions et variants, chaînes/entiers/bool/None/sous-classes, enums stricts, toutes combinaisons valides de type/état, immutabilité, instances incomplètes/altérées, erreurs sans valeur brute.
- `tests/unit/test_identity_links.py` : entités indépendantes, SERVICE sans User, références absentes, doublons d'entités et de liens, cardinalités dans chaque sens, collections et membres invalides, absence de mutation, même UUID dans les deux espaces.
- `tests/integration/test_identity_facade.py` : usage exclusivement public du profil, exports, absence de droit implicite et comportement de refus stable.

Les validations couvrent les suites unitaires et d'intégration complètes, AST des fichiers Python concernés, UTF-8/LF des seuls fichiers du change et OpenSpec strict. Aucune garantie de transaction, concurrence, authentification ou audit durable n'est prétendue.
