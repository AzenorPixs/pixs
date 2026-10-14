# Tâches — Représentation déclarative des métadonnées de commande

Périmètre : trois nouveaux chemins fixes, métadonnées structurelles partielles seulement,
Core direct sans nouveau paquet ni façade modifiée. Hors scope confirmé : comparaison de
payload, empreinte/hash/sérialisation, callback/foncteur, restitution de résultat, conflit
effectif de rejou, déduplication, rétention, persistance, transaction, autorisation,
exécution, clé composée TECHNICAL §18 effective. Le second segment de la requirement
`interactions` et son Scenario restent NON PROUVÉS. Aucun nombre ni longueur cible de tests.

## 1. Publication du module direct Core

- [x] 1.1 Publier exactement `src/pixs/core/command_metadata.py` comme module direct de `pixs.core`, sans aucun autre fichier source ajouté ou modifié, sans nouveau sous-paquet et sans aucune modification de `src/pixs/core/__init__.py` ni d'aucune façade existante ; atteinte par chemin direct du module.
- [x] 1.2 Écrire une docstring de module indiquant que les métadonnées sont structurelles partielles, fournies par un caller trusted ou des fixtures synthétiques, que ne sont prouvés ni légitimité d'un sujet ou tenant, ni topologie, ni authentification, autorisation ou permission, que la clé composée §18 n'est pas construite et aucune déduplication PLATFORM/TENANT affirmée, et que le second segment de la requirement et son Scenario restent NON PROUVÉS.
- [x] 1.3 Ne déclarer que deux exports publics : `CommandMetadata` et `validate_command_metadata`.
- [x] 1.4 Définir `CommandMetadata` en dataclass `frozen=True, slots=True`, structurelle, sans défaut, sans `__post_init__`, sans méthode applicative, sans conversion implicite, avec les sept champs obligatoires dans l'ordre figé `command_id`, `correlation_ids`, `causation_ids`, `scope_context`, `command_type`, `subject_id`, `idempotency_key`.
- [x] 1.5 N'importer que `dataclasses.dataclass`, `pixs.kernel.diagnostics.VALIDATE` et `Diagnostic`, `pixs.core.scope.ScopeContext`, `ScopeStructureError` et `validate_structure`, et `__future__.annotations` si utilisé ; aucun parser SemVer, aucun import d'`AuditEvent`, aucune fonction privée d'un autre module ; les aides internes restent privées et non exportées.
- [x] 1.6 Vérifier que la construction accepte structurellement des valeurs invalides et que `validate_command_metadata` reste le seul point fermé.

## 2. Gardes par type exact

- [x] 2.1 Vérifier que `validate_command_metadata`, de signature `(command: object) -> list[Diagnostic]`, retourne une liste fraîche de `Diagnostic`, neuve et indépendante à chaque appel.
- [x] 2.2 Exiger `type(command) is CommandMetadata` avant toute lecture d'attribut et tout callback ; refuser sinon tout autre objet et toute sous-classe par un unique diagnostic d'élément `command_metadata.command`, sans inspection d'aucun champ et sans imposer d'ordre privé de lecture.
- [x] 2.3 Valider `command_id`, `command_type`, `subject_id` et `idempotency_key` par `type(value) is str and value != ""` ; accepter les chaînes composées d'espaces comme références opaques valides, sans normalisation, grammaire, longueur imposée, classification ni validation UUID.
- [x] 2.4 Valider `correlation_ids` et `causation_ids` par `type(value) is tuple` avant toute itération ou callback, puis chaque élément par `type(item) is str and item != ""` avant tout callback de valeur ; conserver ordre et doublons sans altération ; admettre le `tuple` vide pour cette seule représentation sans affirmer de cardinalité d'exécution ; n'appeler aucun `len()`, `str()` ni `bool()` sur une valeur de type refusé.

## 3. Réutilisation du ScopeContext public

- [x] 3.1 Exiger `type(scope_context) is ScopeContext` (sous-classe refusée) avant tout appel et toute lecture d'attribut.
- [x] 3.2 Appeler le `validate_structure` public de `pixs.core.scope` sur le contexte exact indépendamment des autres champs invalides, afin qu'un refus de contexte soit agrégé avec les autres.
- [x] 3.3 Convertir uniquement `ScopeStructureError` attendue en diagnostic fixe du champ `scope_context`, sans reproduction de la valeur ni du message brut de l'erreur.
- [x] 3.4 Propager à l'identique toute exception inattendue — `ValueError` qui n'est pas `ScopeStructureError`, `RuntimeError`, `KeyboardInterrupt`, `SystemExit` et tout `BaseException` — sans capture générale ni transformation en refus normalisé.
- [x] 3.5 Vérifier qu'aucune règle tenant/PLATFORM existante n'est dupliquée ou réinterprétée et que `validate_context`, la topologie, l'ownership et la propagation ne sont pas utilisés.
- [x] 3.6 Vérifier que ni la clé composée `tenant_id`/`subject_id`/`command_type`/`idempotency_key` de TECHNICAL §18 ni aucune déduplication PLATFORM/TENANT ne sont construites ou affirmées.

## 4. Diagnostics

- [x] 4.1 Vérifier que chaque refus porte `step=VALIDATE`, élément `command_metadata.<champ>` ou `command_metadata.command`, et `constraint == message` statiques nommant le champ et la règle, sans valeur, identifiant, environnement, cause technique ni secret reproduits.
- [x] 4.2 Vérifier qu'un helper interne unique et privé fabrique les diagnostics et qu'aucune aide privée n'est exportée.
- [x] 4.3 Vérifier qu'au plus un refus est agrégé par champ parmi les sept, sans diagnostic indexé par position ou par occurrence.
- [x] 4.4 Vérifier le tri stable, la déduplication par `(element, constraint, message)` et l'absence d'état partagé entre appels.
- [x] 4.5 Vérifier que les listes retournées sont fraîches et indépendantes, la mutation de l'une sans effet sur les suivantes ni sur un nouvel appel.

## 5. Tests unitaires sûrs

- [x] 5.1 Publier exactement `tests/unit/test_command_metadata.py` comme première source de tests du module.
- [x] 5.2 Couvrir les deux exports exacts, les sept champs dans l'ordre figé, l'absence de défauts, `frozen=True`, `slots`, l'absence de `__post_init__` et de méthodes applicatives, la constructibilité des valeurs invalides et le refus d'assignation.
- [x] 5.3 Couvrir le refus d'un objet quelconque et de la sous-classe de `CommandMetadata` avant toute lecture d'attribut ou callback, par l'unique diagnostic `command_metadata.command`, sans imposer d'ordre privé de lecture.
- [x] 5.4 Couvrir les primitives hostiles champ par champ (`None`, vide, booléens, entier, liste, objet, sous-classes `str` comptant bool/len/str, conteneurs de tuples hostiles, tuples de non-`str`) refusées sans callback après sondes positives réelles remises à zéro avant validation ; chaînes d'espaces acceptées ; tuples vides acceptés, ordre et doublons conservés.
- [x] 5.5 Couvrir le `ScopeContext` public réel : TENANT avec identifiants d'espaces opaques et PLATFORM sans identifiants selon les règles EXISTANTES de `pixs.core.scope`, sous-classe refusée par type exact, sans réécrire aucune de ces règles.
- [x] 5.6 Couvrir le contexte exact malformé fabriqué uniquement par `object.__new__` puis `object.__setattr__`, sans mutation d'objet réel : conversion seule de `ScopeStructureError` en diagnostic fixe du champ, sans écho.
- [x] 5.7 Couvrir par espionnement du `validate_structure` public : appel seulement sur contexte de type exact, exécution indépendante des autres champs invalides, propagation à l'identique de `ValueError` hors `ScopeStructureError`, `RuntimeError`, `KeyboardInterrupt`, `SystemExit` et `BaseException` inattendus.
- [x] 5.8 Couvrir le lot de sept champs invalides : sept diagnostics uniques triés par `(element, constraint, message)`, messages statiques, absence d'écho SENTINEL, listes fraîches et indépendantes.

## 6. Intégration sûre en processus frais

- [x] 6.1 Publier exactement `tests/integration/test_command_metadata_integration.py`, sans créer aucun autre fichier d'intégration.
- [x] 6.2 Lancer un interpréteur neuf `-B` avec environnement réduit déclaré (`PATH`, `LANG`, `PYTHONPATH=src`, `PYTHONDONTWRITEBYTECODE`), sans PG réel, sans URL, sans Git, sans secret ; charger avant les gardes seulement les modules de bibliothèque standard nécessaires aux sondes et imports, dont `uuid` si requis, aucun import de `pixs.core` ne précédant les gardes fonctions/environnement/horloge/imports base.
- [x] 6.3 Armer les gardes de fonctions, d'environnement, d'horloge et d'imports base avant l'import applicatif sous gardes ; armer les gardes fichiers seulement après les imports bootstrap et applicatifs nécessaires et avant la construction/validation, sans exiger une absence absolue de toute activité physique d'import.
- [x] 6.4 Limiter les routes déclarées et propres à l'ensemble fini du design, les listes font foi, exactement : fichiers `builtins.open`, `io.open`, `os.open`, `os.read`, `os.write`, `os.listdir`, `os.remove`, `os.fdopen`, `os.stat`, `os.scandir`, `os.unlink`, `os.rename` ; environnement routes déclarées de `os.environ` (`__getitem__`, `get`, `__iter__`, `__len__`, `__contains__`, `__setitem__`, `__delitem__`, `keys`, `values`, `items`, `copy`, `setdefault`, `pop`, `update`) et `os.getenv` ; horloge `datetime.datetime.now/today/utcnow` (3), `datetime.date.today` (1), `time.time/monotonic/perf_counter/localtime/gmtime/sleep` (6) ; sockets `socket.socket.connect`, `socket.create_connection` ; processus `subprocess.Popen`, `subprocess.run`, `os.system`, `os.popen`, `os.execv`, `os.spawnl` ; imports `django`, `psycopg`, `psycopg2`, `psycopg_pool`, `psycopg_binary` et sous-modules. `os.openat` n'est pas une route déclarée.
- [x] 6.5 Éprouver chaque route déclarée (compteur un) puis la remettre à zéro avant la phase couverte ; contrôler les compteurs nuls après chaque phase sans masquer un accès applicatif par une remise à zéro.
- [x] 6.6 Importer `CommandMetadata` et `validate_command_metadata` dans le processus frais sous les gardes et éprouver des exemples représentatifs : contexte TENANT et contexte PLATFORM valides, cross-refus d'un type étranger, contexte exact malformé converti en diagnostic ; aucun nouveau test calendaire.
- [x] 6.7 Limiter la sortie du sous-processus au marqueur fixe `COMMAND_METADATA_SAFE_INTEGRATION_OK`, sans reproduction de valeur, diagnostic brut, environnement ou secret.
- [x] 6.8 Propager ou diagnostiquer explicitement toute erreur inattendue du sous-processus, sans capture générale ni masque de l'échec initial.

## 7. Compilations natives et exécution des tests

- [x] 7.1 Compiler nativement `src/pixs/core/command_metadata.py` sous mandat distinct et vérifier son exit réel.
- [x] 7.2 Compiler nativement `tests/unit/test_command_metadata.py` sous mandat distinct et vérifier son exit réel.
- [x] 7.3 Compiler nativement `tests/integration/test_command_metadata_integration.py` sous mandat distinct et vérifier son exit réel.
- [x] 7.4 Exécuter les tests unitaires ciblés et vérifier leur exit réel et leur output complet.
- [x] 7.5 Exécuter le test d'intégration ciblé et vérifier son exit réel et son output complet.
- [x] 7.6 Exécuter en mandat distinct la suite de régressions du design : lot antérieur de deux cent cinquante-sept régressions sûres, tests unitaires et d'intégration event-contract, `tests.unit.test_scope_context_structure`, `tests.integration.test_public_api_facades` et `tests.integration.test_kernel_purity`, sans PG réel supplémentaire ; le nombre réel de tests est relevé après exécution, sans cible imposée.
- [x] 7.7 Vérifier que les ajouts de tests sont déterminés par les comportements réellement prouvés, sans nombre ni longueur imposé arbitrairement.

## 8. Périmètre, encodage et conformité OpenSpec

- [x] 8.1 Vérifier que le périmètre exact comprend les trois nouveaux chemins et aucun autre fichier source, test ou configuration modifié, aucun sous-paquet ni aucune façade ajoutés ou modifiés.
- [x] 8.2 Vérifier que les soixante-seize fichiers de baseline exacts restent inchangés byte à byte, y compris le Kernel, `pixs.core` et ses paquets `scope`/`identity`, et les cycles antérieurs audit, fanions, backend et event-contract archivé.
- [x] 8.3 Vérifier l'encodage UTF-8 et les fins de ligne LF des trois nouveaux fichiers, sans CRLF ni secret, avec une AST compatible des versions Python 3.12 supportées.
- [x] 8.4 Vérifier que le delta normatif est la copie byte exact de la seule requirement canonique `interactions` « Idempotence et traçabilité des commandes », y compris son Scenario « Rejou divergent », sans norme nouvelle, modifiée ou supprimée.
- [x] 8.5 Vérifier l'absence de nouvelle dépendance, de package exporté, de README modifié, d'opération Git, de wire format, de persistance, de route, d'API runtime, de panneau admin, de PG réel supplémentaire et de politique d'audit.
- [x] 8.6 Exécuter la validation OpenSpec stricte du change et la validation stricte canonique `--specs` avant la publication du code.
- [x] 8.7 Exécuter la validation OpenSpec stricte du change et la validation stricte `--all` du référentiel après les tests.
- [x] 8.8 Vérifier qu'aucune tâche n'est cochée avant preuve observable de son exécution réussie.

Note de séquence : après tous les cochages, exécuter en mandat distinct la validation stricte du change post-cochage ; obtenir ensuite une autorisation d'archivage unitaire distincte, exécuter l'archive, puis produire et vérifier séparément `STATISTIQUES.md` avec ses six sections, UTF-8/LF, totaux croisés et mesures `N/A` motivées. L'archivage et le rapport statistique ne constituent pas des tâches pré-cochage du souscycle.
