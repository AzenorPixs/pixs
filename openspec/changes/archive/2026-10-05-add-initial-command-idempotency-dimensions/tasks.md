# Tâches — Collecte structurelle des dimensions d'idempotence

Périmètre : trois nouveaux chemins fixes, collecte structurelle des quatre dimensions
§18 seulement, Core direct sans nouveau paquet ni façade modifiée. Hors scope confirmé :
clé durable ou de lookup, format wire, hash, empreinte de payload, sérialisation,
concaténation, normalisation, déduplication effective PLATFORM/TENANT, restitution de
rejou identique, conflit divergent, rétention, fenêtre de rejeu, persistance,
transaction, cache, autorisation, exécution. Le second segment de la requirement
`interactions` et son Scenario « Rejou divergent » restent NON PROUVÉS. Aucun nombre ni
longueur cible de tests.

## 1. Publication du module direct Core

- [x] 1.1 Publier exactement `src/pixs/core/idempotency_dimensions.py` comme module direct de `pixs.core`, sans aucun autre fichier source ajouté ou modifié, sans nouveau sous-paquet et sans aucune modification de `src/pixs/core/__init__.py` ni d'aucune façade existante ; atteinte par chemin direct du module.
- [x] 1.2 Écrire une docstring de module indiquant que la collecte est structurelle des dimensions déjà portées, que les valeurs sont trusted ou synthétiques, que pour les valeurs collectées `tenant_id=None` est uniquement la valeur légale existante d'un contexte PLATFORM valide, qu'aucune clé durable, aucun format wire, aucune politique ou mécanisme de déduplication ou de lookup ne sont établis, et que le second segment de la requirement et son Scenario de rejou effectif restent NON PROUVÉS.
- [x] 1.3 Ne déclarer que deux exports publics : `CommandIdempotencyDimensions` et `collect_command_idempotency_dimensions`.
- [x] 1.4 Définir `CommandIdempotencyDimensions` en dataclass `frozen=True, slots=True`, structurelle, sans défaut, sans `__post_init__`, sans méthode applicative, sans conversion implicite, avec quatre champs obligatoires dans l'ordre de §18 : `tenant_id: str | None`, `subject_id: str`, `command_type: str`, `idempotency_key: str`.
- [x] 1.5 N'importer que `dataclasses.dataclass`, `validate_command_metadata` de `pixs.core.command_metadata`, `Diagnostic` de `pixs.kernel.diagnostics` et `__future__.annotations` ; ne pas importer `CommandMetadata` ni `ScopeContext` s'ils ne sont pas utilisés ; aucune aide privée d'un autre module.
- [x] 1.6 Vérifier que le constructeur accepte structurellement toute valeur, y compris `None` partout et des objets hostiles, et que le collecteur reste le seul point fermé.

## 2. Sémantique du collecteur

- [x] 2.1 Vérifier que `collect_command_idempotency_dimensions`, de signature `(command: object) -> tuple[CommandIdempotencyDimensions | None, list[Diagnostic]]`, appelle le `validate_command_metadata` public existant exactement une fois avant toute lecture locale d'attribut, sans recontrôler le type ni dupliquer aucune règle de `command_metadata` ou de `pixs.core.scope`.
- [x] 2.2 Sur liste non vide, vérifier le renvoi de `(None, cette même liste publique)` sans copie, tri, renommage, conversion ni aucune lecture d'attribut de la commande.
- [x] 2.3 Sur liste vide, vérifier la construction d'une nouvelle instance portant les quatre valeurs lues telles quelles — `tenant_id` du `scope_context`, `subject_id`, `command_type`, `idempotency_key` — et le renvoi de cette instance avec cette même liste vide exacte produite par l'appel public.
- [x] 2.4 Vérifier que `tenant_id=None` est conservé comme seule valeur légale existante d'un contexte PLATFORM valide, sans sentinelle, substitution, namespace, ni admission d'une clé d'exécution sans tenant, et que le `scope_context` n'est jamais restitué dans les dimensions.
- [x] 2.5 Vérifier qu'aucun message, élément ou diagnostic propre au module n'est fabriqué et qu'aucun état n'est partagé entre appels.
- [x] 2.6 Vérifier la propagation à l'identique de toute exception inattendue levée par le validateur public — `ValueError` hors conversion déjà publique, `RuntimeError`, `KeyboardInterrupt`, `SystemExit` et tout `BaseException` — sans capture, transformation ni tuple formé.

## 3. Tests unitaires sûrs

- [x] 3.1 Publier exactement `tests/unit/test_command_idempotency_dimensions.py` comme première source de tests du module.
- [x] 3.2 Couvrir les deux exports exacts, les quatre champs dans l'ordre de §18, `frozen=True`, `slots`, l'absence de défauts, de `__post_init__` et de méthodes, et la constructibilité avec valeurs invalides.
- [x] 3.3 Couvrir par espion de l'alias public du module : un appel unique sur chaque chemin, identité d'objet de la liste publique sur refus comme sur succès, et fraîcheur et indépendance des listes et tuples entre appels successifs.
- [x] 3.4 Couvrir le refus d'un objet quelconque et d'une sous-classe de `CommandMetadata` par un objet dont toute lecture d'attribut lève, après sonde positive réelle remise à zéro, prouvant zéro lecture locale des champs et reprise de l'unique diagnostic public `command_metadata.command`.
- [x] 3.5 Couvrir les succès TENANT avec opacités distinctes y compris chaînes d'espaces et PLATFORM avec `tenant_id is None` conservé : quatre valeurs identiques, aucune mutation de la commande d'origine, tuples d'origine intacts.
- [x] 3.6 Couvrir la commande multi-refus : liste publique intégrale traversée inchangée en contenu, ordre, identité et longueur, dimensions `None`.
- [x] 3.7 Couvrir la propagation à l'identique, sur même objet, des erreurs inattendues injectées par espion, y compris `BaseException` personnalisé.

## 4. Intégration sûre en processus frais

- [x] 4.1 Publier exactement `tests/integration/test_command_idempotency_dimensions_integration.py`, sans créer aucun autre fichier d'intégration.
- [x] 4.2 Lancer un interpréteur neuf `-B` avec environnement réduit déclaré (`PATH`, `LANG`, `PYTHONPATH=src`, `PYTHONDONTWRITEBYTECODE`), sans PG réel, sans URL, sans Git, sans secret ; charger avant les gardes seulement les modules de bibliothèque standard nécessaires aux sondes et imports, dont `uuid` si requis, aucun import de `pixs.core` ne précédant les gardes fonctions/environnement/horloge/imports base.
- [x] 4.3 Armer les gardes de fonctions, d'environnement, d'horloge et d'imports base avant l'import applicatif sous gardes ; armer les gardes fichiers seulement après les imports bootstrap et applicatifs nécessaires et avant construction/collecte, sans exiger une absence absolue de toute activité physique d'import.
- [x] 4.4 Limiter les routes déclarées et propres à l'ensemble fini du design, les listes font foi, exactement : fichiers `builtins.open`, `io.open`, `os.open`, `os.read`, `os.write`, `os.listdir`, `os.remove`, `os.fdopen`, `os.stat`, `os.scandir`, `os.unlink`, `os.rename` ; environnement routes déclarées de `os.environ` (`__getitem__`, `get`, `__iter__`, `__len__`, `__contains__`, `__setitem__`, `__delitem__`, `keys`, `values`, `items`, `copy`, `setdefault`, `pop`, `update`) et `os.getenv` ; horloge `datetime.datetime.now/today/utcnow` (3), `datetime.date.today` (1), `time.time/monotonic/perf_counter/localtime/gmtime/sleep` (6) ; sockets `socket.socket.connect`, `socket.create_connection` ; processus `subprocess.Popen`, `subprocess.run`, `os.system`, `os.popen`, `os.execv`, `os.spawnl` ; imports `django`, `psycopg`, `psycopg2`, `psycopg_pool`, `psycopg_binary` et sous-modules. `os.openat` n'est pas une route déclarée.
- [x] 4.5 Éprouver chaque route déclarée (compteur un) puis la remettre à zéro avant la phase couverte ; contrôler les compteurs nuls après chaque phase sans masquer un accès applicatif par une remise à zéro.
- [x] 4.6 N'utiliser les mocks que pour les sondes des gardes ; exercer le `validate_command_metadata` public réel dans l'enfant et éprouver les scènes : collecte réussie TENANT avec les quatre dimensions exactes, collecte réussie PLATFORM avec `None` conservé, refus d'un type étranger avec liste publique reprise, aucune mutation ; aucun nouveau test calendaire.
- [x] 4.7 Limiter la sortie du sous-processus au marqueur fixe `COMMAND_IDEMPOTENCY_DIMENSIONS_SAFE_INTEGRATION_OK`, sans reproduction de valeur, diagnostic brut, environnement ou secret.
- [x] 4.8 Propager ou diagnostiquer explicitement toute erreur inattendue du sous-processus, sans capture générale ni masque de l'échec initial.

## 5. Compilations natives et exécution des tests

- [x] 5.1 Compiler nativement `src/pixs/core/idempotency_dimensions.py` sous mandat distinct et vérifier son exit réel.
- [x] 5.2 Compiler nativement `tests/unit/test_command_idempotency_dimensions.py` sous mandat distinct et vérifier son exit réel.
- [x] 5.3 Compiler nativement `tests/integration/test_command_idempotency_dimensions_integration.py` sous mandat distinct et vérifier son exit réel.
- [x] 5.4 Exécuter les tests unitaires ciblés et vérifier leur exit réel et leur output complet.
- [x] 5.5 Exécuter le test d'intégration ciblé et vérifier son exit réel et son output complet.
- [x] 5.6 Exécuter en mandat distinct la suite de régressions du design : lot identifié de trois cent vingt-cinq tests antérieurs (suite de trois cent un du design `CommandMetadata` et vingt-quatre tests `CommandMetadata`), sans PG réel supplémentaire ; le nombre réel de tests est relevé après exécution du nouveau lot, sans cible imposée.
- [x] 5.7 Vérifier que les ajouts de tests sont déterminés par les comportements réellement prouvés, sans nombre ni longueur imposé arbitrairement.

## 6. Périmètre, encodage et conformité OpenSpec

- [x] 6.1 Vérifier que le périmètre exact comprend les trois nouveaux chemins et aucun autre fichier source, test ou configuration modifié, aucun sous-paquet ni aucune façade ajoutés ou modifiés.
- [x] 6.2 Vérifier que les soixante-dix-neuf fichiers de baseline exacts restent inchangés byte à byte, y compris le Kernel, `pixs.core` et ses paquets `scope`/`identity`, les cycles antérieurs audit, fanions, backend, event-contract archivé et les trois sources du cycle `CommandMetadata`.
- [x] 6.3 Vérifier l'encodage UTF-8 et les fins de ligne LF des trois nouveaux fichiers, sans CRLF ni secret, avec une AST compatible des versions Python 3.12 supportées.
- [x] 6.4 Vérifier que le delta normatif est la copie byte exact de la seule requirement canonique `interactions` « Idempotence et traçabilité des commandes », y compris son Scenario « Rejou divergent », sans norme nouvelle, modifiée ou supprimée.
- [x] 6.5 Vérifier l'absence de nouvelle dépendance, de package exporté, de README modifié, d'opération Git, de wire format, de persistance, de route, d'API d’exécution métier, de panneau admin, de PG réel supplémentaire et de politique d'audit.
- [x] 6.6 Vérifier le rejet de toute attribution de rejou effectif, de déduplication ou d'exécution dans les docstrings, diagnostics et documentation du change.
- [x] 6.7 Exécuter la validation OpenSpec stricte du change et la validation stricte canonique `--specs` avant la publication du code.
- [x] 6.8 Exécuter la validation OpenSpec stricte du change et la validation stricte `--all` du référentiel après les tests.
- [x] 6.9 Vérifier qu'aucune tâche n'est cochée avant preuve observable de son exécution réussie.

Note de séquence : après tous les cochages, exécuter en mandat distinct la validation stricte du change post-cochage ; obtenir ensuite une autorisation d'archivage unitaire distincte, exécuter l'archive, puis produire et vérifier séparément `STATISTIQUES.md` avec ses six sections, UTF-8/LF, totaux croisés et mesures `N/A` motivées. L'archivage et le rapport statistique ne constituent pas des tâches pré-cochage du souscycle.
