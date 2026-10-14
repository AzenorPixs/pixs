# Design — add-initial-command-idempotency-dimensions

## Contexte et décision

Collecte STRUCTURELLE des quatre dimensions d'idempotence de TECHNICAL §18 et PROJECT
§28 (`tenant_id`, `subject_id`, `command_type`, `idempotency_key`) telles qu'elles
existent déjà dans une `CommandMetadata` validée par son validateur public. Décision
CGPT retenue : module direct Core sans nouveau sous-paquet ni façade modifiée ; le
`tenant_id` `None` d'un `ScopeContext` PLATFORM valide est conservé uniquement comme
donnée légale existante — ce n'est ni une clé de lookup, ni une admission d'exécution
sans tenant, ni une politique de déduplication. Le second segment de la requirement
`interactions` et son Scenario « Rejou divergent » restent NON PROUVÉS, ni implémentés
ni simulés.

## Frontière explicite

- Norme directe : le delta `specs/interactions/spec.md` est la copie byte exact de la
  seule requirement canonique « Idempotence et traçabilité des commandes », Scenario
  inclus ; aucune norme nouvelle, modifiée ou supprimée ; delta canonique effectif
  attendu +0/~0/-0.
- Aucune règle de `command_metadata` ni de `pixs.core.scope` n'est dupliquée,
  recontrôlée ou réinterprétée : la seule décision de lecture locale est la vacuité de
  la liste retournée par le validateur public. Aucun nouveau diagnostic n'est fabriqué
  par ce module.
- Aucun hash, empreinte de payload, sérialisation, concaténation en chaîne unique,
  normalisation, format wire, indexabilité affirmée, stockage, cache, fenêtre de
  rétention, transaction, déduplication, autorisation ou exécution.

## Fichiers autorisés

- `src/pixs/core/idempotency_dimensions.py` — module direct de `pixs.core` ; aucun
  sous-paquet nouveau ; `src/pixs/core/__init__.py` et toutes les façades existantes
  non modifiés ; atteinte par chemin direct du module.
- `tests/unit/test_command_idempotency_dimensions.py`
- `tests/integration/test_command_idempotency_dimensions_integration.py`
Aucun autre fichier source, test ou configuration n'est créé ou modifié.

## API publique

Deux exports seulement :

- `CommandIdempotencyDimensions` — `@dataclass(frozen=True, slots=True)`,
  structurelle, sans défaut, sans `__post_init__`, sans méthode applicative, sans
  conversion implicite ; quatre champs obligatoires dans l'ordre de §18 :
  `tenant_id: str | None`, `subject_id: str`, `command_type: str`,
  `idempotency_key: str`. Le constructeur accepte structurellement toute valeur, y
  compris `None` partout ou des objets hostiles : la collecte reste le seul point
  fermé.
- `collect_command_idempotency_dimensions(command: object) ->
  tuple[CommandIdempotencyDimensions | None, list[Diagnostic]]`.

## Collecteur — implémentation proposée

Comportement contractuel, en texte :

1. Appeler `validate_command_metadata(command)` — le validateur public exact, appelé
   une seule fois, avant toute lecture locale d'attribut ; aucune exception de ce call
   n'est capturée : `ValueError` hors `ScopeStructureError` déjà convertie par le
   public, `RuntimeError`, `KeyboardInterrupt`, `SystemExit` et tout `BaseException`
   inattendu sont propagés à l'identique par la pile d'appels.
2. Si la liste retournée est non vide : renvoyer `(None, cette même liste)`, sans
   copie, tri, renommage, conversion, ni aucune lecture d'attribut de `command`. La
   liste fraîche et les diagnostics statiques du public traversent inchangés.
3. Si la liste est vide : le type exact `CommandMetadata`, la forme des quatre champs
   et la structure du `ScopeContext` sont déjà garantis par les validateurs publics ;
   construire une nouvelle instance par mots-clés avec les valeurs lues telles
   quelles : `tenant_id=command.scope_context.tenant_id`,
   `subject_id=command.subject_id`, `command_type=command.command_type`,
   `idempotency_key=command.idempotency_key` ; renvoyer `(dimensions, cette même
   liste vide)`, soit la liste fraîche exacte produite par l'appel public.
4. Aucune vérification locale de type, de vacuité de chaîne ou de règle de
   `pixs.core.scope` ; aucun message, élément ou diagnostic propre au module ; aucune
   lecture d'aide privée d'un autre module ; aucun état partagé entre appels.

## Imports et docstring

- Imports publics minimums : `dataclasses.dataclass`,
  `validate_command_metadata` de `pixs.core.command_metadata`, `Diagnostic` de
  `pixs.kernel.diagnostics`, et `__future__.annotations`. Les classes
  `CommandMetadata` et `ScopeContext` ne sont pas importées (non utilisées).
- Docstring de module : collecte structurelle des dimensions déjà portées ; valeurs
  trusted ou synthétiques ; pour les valeurs collectées, `tenant_id=None` est
  uniquement la valeur légale existante d'un contexte PLATFORM valide ; aucune clé durable, aucun format wire, aucune politique ou
  mécanisme de déduplication, aucun mécanisme de lookup ; le second segment de la requirement et
  son Scenario de rejou effectif restent NON PROUVÉS.

## Tests unitaires

Définis par comportements, sans nombre ni longueur imposés :

- Structure : `__all__` exactement les deux exports ; quatre champs obligatoires dans
  l'ordre §18 ; `frozen=True` (assignation refusée), `slots` (pas de `__dict__`),
  absence de défauts, de `__post_init__` et de méthodes ; constructibilité avec
  valeurs invalides (`None` partout, objets hostiles).
- Espion de l'alias public `validate_command_metadata` du module (wrapper déléguant au
  réel) : appelé exactement une fois sur chaque chemin ; sur refus la liste retournée
  par `collect` est identique en identité d'objet (`is`) à celle fabriquée par
  l'appel espionné ; sur succès la liste traversée est la même `[]` fraîche que
  celle du validateur ; deux appels successifs produisent listes et tuples distincts.
- Refus sans lecture locale : objet étranger quelconque et sous-classe de
  `CommandMetadata` (sonde positive réelle de lecture d'attribut, remise à zéro, puis
  collecte) — la collecte ne déclenche aucune lecture des champs ; un objet dont toute
  lecture d'attribut lève prouve le zéro lecture ; le refus porté est la liste publique
  de l'unique diagnostic `command_metadata.command`.
- Succès : commande TENANT valide avec opacités distinctes y compris chaînes
  d'espaces — les quatre valeurs sont conservées à l'identique (`is`/`==`), `None`
  absent ; commande PLATFORM valide — `tenant_id is None` conservé, aucune sentinelle
  ni substitution ; `scope_context` jamais restitué dans les dimensions ; la commande
  d'origine n'est pas mutée (relevé `dataclasses.asdict` avant/après) et ses tuples
  restent les mêmes objets.
- Malformée et multi-refus : commande à plusieurs refus publics — la liste intégrale
  traverse inchangée en contenu, ordre, identité et longueur ; dimensions `None`.
- Propagation : espion soulevant `ValueError` hors `ScopeStructureError`,
  `RuntimeError`, `KeyboardInterrupt`, `SystemExit` et un `BaseException` personnalisé
  — exception propagée à l'identique (même objet), aucun tuple formé, aucune capture.
- Absence d'état partagé : résultats stables entre appels pour une même entrée, sans
  mutation de l'entrée ni des listes restituées.

## Intégration sûre en processus frais

- Cadre fini déjà prouvé (cycles audit/event/CommandMetadata) réutilisé ; le
  validateur applicatif public n'est jamais mocké dans l'enfant ; les mocks sont
  limités aux sondes des gardes.
- Bootstrap standard borné avant les gardes : uniquement les modules de bibliothèque
  nécessaires aux sondes et imports, dont `uuid` si requis par le chargement de
  `pixs.core` ; aucun import de `pixs.core` ne précède les gardes
  fonctions/environnement/horloge/imports base.
- Gardes fonctions, environnement, horloge et imports DB armées avant l'import
  applicatif ; gardes fichiers armées après les imports bootstrap et applicatifs
  nécessaires et avant construction/collecte, sans prétendre à une absence absolue
  d'activité physique d'import.
- Routes exactes, identiques à la liste finie déjà acquise et faisant foi : fichiers
  `builtins.open`, `io.open`, `os.open`, `os.read`, `os.write`, `os.listdir`,
  `os.remove`, `os.fdopen`, `os.stat`, `os.scandir`, `os.unlink`, `os.rename` ;
  environnement routes déclarées de `os.environ` (`__getitem__`, `get`, `__iter__`,
  `__len__`, `__contains__`, `__setitem__`, `__delitem__`, `keys`, `values`, `items`,
  `copy`, `setdefault`, `pop`, `update`) et `os.getenv` ; horloge
  `datetime.datetime.now/today/utcnow`, `datetime.date.today`,
  `time.time/monotonic/perf_counter/localtime/gmtime/sleep` ; sockets
  `socket.socket.connect`, `socket.create_connection` ; processus `subprocess.Popen`,
  `subprocess.run`, `os.system`, `os.popen`, `os.execv`, `os.spawnl` ; imports
  `django`, `psycopg`, `psycopg2`, `psycopg_pool`, `psycopg_binary` et sous-modules.
  `os.openat` n'est pas une route déclarée.
- Chaque route réellement probée (compteur un) puis remise à zéro avant la phase
  couverte ; compteurs nuls contrôlés après chaque phase sans masquer un accès
  applicatif.
- Scènes enfant : construction d'exemples valides TENANT et PLATFORM, collecte réussie
  avec les quatre dimensions exactes et `None` conservé sur PLATFORM, refus d'un type
  étranger avec liste publique reprise, aucune mutation ; aucun nouveau test
  calendaire ; sortie limitée au marqueur fixe
  `COMMAND_IDEMPOTENCY_DIMENSIONS_SAFE_INTEGRATION_OK`, sans reproduction de valeur,
  diagnostic brut, environnement ou secret ; erreur inattendue propagée ou
  diagnostiquée explicitement, jamais masquée. Aucun PG réel, réseau, horloge ou Git.

## Régressions

- Suite préservée : le lot identifié de trois cent vingt-cinq tests antérieurs — la
  suite de trois cent un du design `CommandMetadata` et les vingt-quatre tests
  `CommandMetadata` (unitaires et intégration) —, sans rejouer les artefacts archivés.
- Le nombre réel de tests est déterminé après exécution du nouveau lot, jamais imposé
  d'avance.

## Validations et séquence

- Avant le code : validation stricte OpenSpec du change, puis des specs canoniques
  (`--specs`).
- Compilations natives `py_compile` séparées des trois fichiers, sous mandats
  distincts, exits réels.
- Unitaires ciblés puis intégration fraîche sous mandats distincts.
- Après les tests : validation stricte du change puis du référentiel (`--all`).
- Après cochage de toutes les tâches prouvées : validation stricte du change
  post-cochage en mandat distinct.
- Archivage sous mandat distinct, puis `STATISTIQUES.md` sous mandat de fichier
  distinct (six sections, sondes de modèle périodiques de trente minutes
  indépendantes, cycle conjoint de 1 h 30, totaux croisés, UTF-8/LF, mesures `N/A`
  motivées).
- Aucune tâche cochée avant preuve observable ; aucun artefact publié hors mandat.

## Limites

- Ce jalon ne prouve aucune déduplication effective PLATFORM/TENANT, aucun rejou identique
  restitué, aucun conflit divergent, aucune autorisation, légitimité de sujet ou
  tenant, persistance, transaction, rétention, fenêtre de rejeu ou exécution.
- Collecte déclarative seulement ; la présence de `None` n'admet aucun mécanisme
  d'exécution sans tenant ; le Scenario de rejou effectif et le second segment de la
  requirement restent ouverts à un futur change runtime, non entrepris ici.
