# Design — add-initial-command-metadata-representation

## Contexte et décision

Représentation déclarative PARTIELLE du premier segment de la requirement canonique
`interactions` « Idempotence et traçabilité des commandes » : porter identifiant,
corrélation, causalité, contexte de périmètre et clé d'idempotence. Le second segment
(rejou identique→restitution, divergent→conflit) et le Scenario « Rejou divergent »
restent NON PROUVÉS, ni implémentés ni simulés. Décision CGPT retenue : option O2 —
réutilisation du `ScopeContext` public déjà prouvé de `pixs.core.scope`, sans nouvelle
norme, sans nouveau paquet et sans aucune modification de façade.

## Frontière explicite

- Norme directe : le delta `specs/interactions/spec.md` est la copie byte exact de la seule
  requirement canonique citée, Scenario inclus ; delta effectif attendu +0/~0/-0.
- Aucun contrat public complet ni instance de commande, payload ou exécution ;
  transaction, persistance, autorisation, restitution, conflit effectif, déduplication,
  rétention, empreinte/hash/sérialisation, callback ou foncteur injecté restent hors périmètre.
- Aucune des règles existantes de `ScopeContext` n'est dupliquée ni réinterprétée : les
  contraintes tenant/PLATFORM viennent uniquement du `validate_structure` public appelé sur
  le contexte exact. `validate_context`/topologie/ownership/propagation ne sont pas utilisés.
- Pas de construction de la clé composée de TECHNICAL §18, pas de validation UUID du profil
  identité, aucune normalisation/grammaire/longueur/classification des références.

## Fichiers autorisés

- `src/pixs/core/command_metadata.py` — module direct de `pixs.core` ; aucun sous-paquet
  nouveau ; `src/pixs/core/__init__.py` et toutes les façades existantes non modifiés ;
  atteinte par chemin direct du module.
- `tests/unit/test_command_metadata.py`
- `tests/integration/test_command_metadata_integration.py`
Aucun autre fichier source, test ou configuration n'est créé ou modifié.

## API publique

Deux exports seulement :

- `CommandMetadata` — `@dataclass(frozen=True, slots=True)`, structurelle, sans défaut,
  sans `__post_init__`, sans méthode applicative, sans conversion implicite ; sept champs
  obligatoires dans l'ordre figé : `command_id`, `correlation_ids`, `causation_ids`,
  `scope_context`, `command_type`, `subject_id`, `idempotency_key`.
- `validate_command_metadata(command: object) -> list[Diagnostic]`.

Sémantique déclarative des champs :

- `command_id`, `command_type`, `subject_id`, `idempotency_key` : `type(value) is str and
  value != ""`. Les chaînes composées d'espaces sont des références opaques valides
  (trusted ou synthétiques). Aucune grammaire, préfixe, registre, longueur ni transformation.
- `correlation_ids`, `causation_ids` : `tuple` de type exact dont chaque élément est un `str`
  de type exact non vide ; ordre et doublons conservés, jamais altérés ; le `tuple` vide est
  permis pour cette seule représentation, sans affirmer de cardinalité d'exécution. Les
  conteneurs non exacts sont refusés avant toute itération ou callback ; les éléments
  du tuple exact sont inspectés par type avant tout callback de leurs valeurs. Aucun
  `len()`, `str()` ou `bool()` n’est appelé sur une valeur de type refusé.
- `scope_context` : instance de type exact du public `ScopeContext` (sous-classe refusée),
  contrôlée par `type` avant tout appel et toute lecture d'attribut.

## Validateur

- `type(command) is CommandMetadata` avant toute lecture d'attribut et tout callback ; sinon,
  un unique diagnostic d'élément `command_metadata.command`, sans inspection d'aucun champ.
- Chaque champ est vérifié indépendamment : au plus un refus par champ parmi les sept, sans
  diagnostic indexé par position ou occurrence.
- `scope_context` : après contrôle de type exact, appel du `validate_structure` public de
  `pixs.core.scope` sur le contexte exact, indépendamment des autres champs invalides.
  Seule `ScopeStructureError` attendue est convertie en diagnostic fixe du champ
  `scope_context` ; toute autre exception — `ValueError` qui n'est pas `ScopeStructureError`,
  `RuntimeError`, `KeyboardInterrupt`, `SystemExit` et tout `BaseException` inattendu — est
  propagée à l'identique, sans capture générale.
- Diagnostics fabriqués par un helper interne unique privé : `step=VALIDATE`, éléments
  `command_metadata.<champ>` (ou `command_metadata.command`), `constraint == message`
  statiques nommant le champ et la règle, sans valeur, identifiant, environnement, cause
  technique ni secret reproduits.
- Tri stable et déduplication par `(element, constraint, message)` ; liste fraîche et
  indépendante à chaque appel, aucune état partagé.

## Imports et docstring

- Imports publics uniquement : `dataclasses.dataclass`,
  `pixs.kernel.diagnostics` (`VALIDATE`, `Diagnostic`),
  `pixs.core.scope` (`ScopeContext`, `ScopeStructureError`, `validate_structure`),
  `__future__.annotations` si utilisé. Aucun parser SemVer, aucun import d'`AuditEvent`,
  aucune fonction privée d'un autre module ; helpers internes privés non exportés.
- Le module est au-dessus du Kernel : aucun import de `pixs.core` n'entre dans le Kernel.
- Docstring de module : déclaration des métadonnées structurelles partielles seulement ;
  valeurs fournies par caller trusted ou fixtures synthétiques ; ne prouve ni légitimité
  d'un sujet ou tenant, ni topologie, ni authentification, autorisation ou permission ; ne
  construit pas la clé composée §18 et n'affirme aucune déduplication PLATFORM/TENANT ; ne
  compare aucun payload, n'injecte aucun callback, ne restitue ni ne conflictualise aucun
  rejou, ne persiste, ne transige, n'exécute rien ; le second segment de la requirement et
  son Scenario restent NON PROUVÉS.

## Tests unitaires

Dérivés des comportements, sans nombre ni longueur imposés :

- Structure : sept champs obligatoires dans l'ordre figé, absence de défauts, `frozen=True`,
  absence de `__post_init__` et de méthodes applicatives, slots ; refus d'assignation ;
  constructibilité structurelle avec valeurs invalides (la validation reste le seul point fermé).
- Hostiles champ par champ avec sondes positives (`__getattribute__`/dunder instrumentés
  temporairement sur les classes exactes, compteurs remis à zéro avant validation) : `None`,
  vide, `True`/`False`, entier, liste, objet, sous-classes hostiles de `str` comptant
  `bool`/`len`/`str`, tuples de non-`str`, sous-classes de `tuple` ; aucun callback déclenché
  des valeurs hostiles sur refus ; l’appel attendu au validateur public du contexte exact
  reste permis pour agréger les diagnostics. Chaînes d’espaces acceptées comme références opaques.
- Contexte public réutilisé : `ScopeContext` TENANT avec ids d'espaces opaques et `PLATFORM`
  sans ids acceptés selon les règles EXISTANTES ; sous-classe de `ScopeContext` refusée par
  type exact ; contexte exact malformé construit par `object.__new__` puis `object.__setattr__`
  (aucune mutation d'objet réel) → `ScopeStructureError` convertie en diagnostic fixe du champ,
  sans écho.
- Propagation : spy du `validate_structure` public soulevant `ValueError` non
  `ScopeStructureError`, puis `RuntimeError`/`BaseException` → propagés à l'identique.
- Indépendance : le spy `validate_structure` n'est appelé que sur un contexte de type exact,
  y compris quand d'autres champs sont invalides ; le type étranger produit l'unique
  diagnostic `command_metadata.command` sans aucun appel.
- Agrégation : lot des sept champs invalides → sept diagnostics uniques triés, éléments
  `command_metadata.<champ>`, messages statiques, aucun écho SENTINEL ; listes fraîches,
  mutation de la première sans effet sur la suivante ni sur un nouvel appel.

## Intégration sûre en processus frais

- Cadre fini déjà prouvé (cycles audit/event) réutilisé, adapté aux imports publics de
  `pixs.core` et `pixs.kernel`.
- Bootstrap standard borné avant l’import applicatif : charger seulement les modules
  de bibliothèque standard nécessaires aux sondes et imports, dont `uuid` si requis.
  Aucun import de `pixs.core` ne précède les gardes fonctions/environnement/horloge/imports
  base ; aucune fonction génératrice d’UUID n’est appelée, aucune source stdlib n’est lue
  par les agents. Les imports applicatifs restent dans la phase gardée prévue ci-dessous.
- Gardes fonctions/environnement/horloge/imports DB armées avant les imports applicatifs ;
  gardes fichiers armées après les imports bootstrap/applicatifs nécessaires et avant
  construction/validation, sans prétendre à une absence absolue d'activité physique d'import.
- Routes finies identiques au lot déjà acquis : fichiers `builtins.open`, `io.open`,
  `os.open`, `os.read`, `os.write`, `os.listdir`, `os.remove`, `os.fdopen`, `os.stat`,
  `os.scandir`, `os.unlink`, `os.rename` (aucune autre ; `os.openat` n'est pas une route) ;
  environnement routes déclarées de `os.environ` (`__getitem__`, `get`, `__iter__`, `__len__`,
  `__contains__`, `__setitem__`, `__delitem__`, `keys`, `values`, `items`, `copy`,
  `setdefault`, `pop`, `update`) et `os.getenv` ; horloge `datetime.datetime.now/today/utcnow`,
  `datetime.date.today`, `time.time/monotonic/perf_counter/localtime/gmtime/sleep` ; sockets
  `socket.socket.connect`, `socket.create_connection` ; processus `subprocess.Popen`,
  `subprocess.run`, `os.system`, `os.popen`, `os.execv`, `os.spawnl` ; imports `django`,
  `psycopg`, `psycopg2`, `psycopg_pool`, `psycopg_binary` et sous-modules.
- Chaque route réellement probée (compteur un) puis remise à zéro avant la phase couverte ;
  compteurs nuls contrôlés après chaque phase ; aucune remise à zéro ne masque un accès
  applicatif.
- Scènes enfant : construction et validation d'exemples valides (TENANT et PLATFORM),
  cross-refus type étranger, contexte malformé `object.__new__` converti ; aucun nouveau test
  calendaire ; sortie de l'enfant limitée au marqueur fixe
  `COMMAND_METADATA_SAFE_INTEGRATION_OK`, sans reproduction de valeur, diagnostic brut,
  environnement ou secret ; erreur inattendue de l'enfant propagée ou diagnostiquée
  explicitement, jamais masquée. Aucun PG réel, aucun réseau, aucune horloge, aucun Git.

## Régressions

- Suite préservée : lot antérieur de deux cent cinquante-sept régressions sûres, tests
  unitaires et d'intégration event-contract, plus les tests existants des dépendances touchées
  par la façade réutilisée : `tests/unit/test_scope_context_structure.py`,
  `tests/integration/test_public_api_facades.py`, `tests/integration/test_kernel_purity.py`.
- Le nombre réel de tests est déterminé après exécution, jamais imposé d'avance.

## Validations et séquence

- Compilations natives `py_compile` séparées des trois fichiers, sous mandats distincts, exits réels.
- Avant le code : validation stricte OpenSpec du change, puis des specs canoniques (`--specs`).
- Unitaires ciblés et intégration fraîche sous mandats distincts.
- Après les tests : validation stricte du change puis du référentiel (`--all`).
- Après cochage de toutes les tâches prouvées : validation stricte du change post-cochage.
- Archivage sous mandat distinct, puis `STATISTIQUES.md` sous mandat de fichier distinct.
- Aucune tâche cochée avant preuve observable ; aucun artefact publié hors mandat.

## Limites

- Ne prouve : ni légitimité de `subject_id`/tenant, ni topologie, ni authentification,
  autorisation ou permission, ni idempotence d'exécution, ni restitution/conflit de rejou,
  ni déduplication, rétention, persistance, transaction ou exécution.
- Représentation déclarative seulement ; le tuple vide permis ici n'affirme aucune
  cardinalité runtime ; les secondes garanties de la requirement restent ouvertes à un
  futur travail runtime, non entrepris dans ce change.
