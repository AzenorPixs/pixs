# Tâches — Représentation déclarative des contrats d'événement

Périmètre : trois nouveaux chemins fixes, norme directe events 1, déclaration
partielle uniquement. Hors scope confirmé : TECH8 (enregistrement,
`ContractDescriptor`, contrat public complet), TECH17 (instance, payload,
enveloppe complète), Scenario d'exposition extérieure réelle, requirements
events 2 et 3, tout runtime. Aucune quantité ni longueur cible de tests.

## 1. Publication du module pur

- [x] 1.1 Publier exactement `src/pixs/kernel/event_contract.py` comme module pur du Kernel, sans aucune autre source applicative ajoutée ou modifiée.
- [x] 1.2 Écrire une docstring de module indiquant que les valeurs sont fournies par un caller trusted ou des fixtures synthétiques, que la validation est seulement structurelle et déclarative partielle, qu'elle ne remplace ni l'enregistrement ni `ContractDescriptor` ni les garanties d'un contrat public (TECH8), et qu'elle ne définit aucune instance, payload, enveloppe complète (TECH17), persistance, publication, audience, schéma effectif, ordre effectif, outbox, transaction, idempotence, publisher ou runtime.
- [x] 1.3 Ne déclarer que quatre exports publics : `DomainEventContract`, `IntegrationEventContract`, `validate_domain_event_contract`, `validate_integration_event_contract`.
- [x] 1.4 Définir les deux dataclasses `frozen=True`, structurelles, sans `__post_init__`, sans défaut, sans méthode applicative, sans conversion implicite et sans héritage entre elles.
- [x] 1.5 Déclarer dans les deux types les cinq champs dans l'ordre figé `event_type`, `contract_version`, `producer_reference`, `schema_reference`, `order_scope_reference`, sans champ, défaut, alias ou constructeur supplémentaire.
- [x] 1.6 N'importer que `dataclasses.dataclass`, `pixs.kernel.diagnostics.VALIDATE` et `Diagnostic`, `pixs.kernel.manifest.semver.parse_version`, et `__future__.annotations` si utilisé ; aucun import de `parse_requirement` ; aucune fonction privée d'un autre module ; les aides internes du module restent privées et non exportées.
- [x] 1.7 Vérifier que la construction accepte structurellement des valeurs invalides et que les deux validateurs restent les seuls points fermés.

## 2. Validateurs fermés par type exact

- [x] 2.1 Vérifier que chaque validateur, de signature `(event: object) -> list[Diagnostic]`, retourne une liste fraîche de `Diagnostic`, neuve et indépendante à chaque appel.
- [x] 2.2 Exiger `type(event) is DomainEventContract` respectivement `type(event) is IntegrationEventContract` avant toute lecture d'attribut et avant tout callback.
- [x] 2.3 Refuser par cross-refus l'instance exacte du type partenaire, tout objet d'un autre type et toute sous-classe, par un unique diagnostic d'élément `event_contract.event`, sans inspection d'aucun champ.
- [x] 2.4 Agréger au maximum un refus par champ parmi les cinq, sans diagnostic indexé par position ou par occurrence.
- [x] 2.5 Trier et dédupliquer les diagnostics par `(element, constraint, message)` de façon stable, puis retourner la liste.
- [x] 2.6 Vérifier que chaque message est une contrainte statique nommant le champ et la règle, sans valeur, identifiant, environnement, cause technique ni secret reproduits.

## 3. Références opaques

- [x] 3.1 Valider `event_type`, `producer_reference`, `schema_reference` et `order_scope_reference` par `type(value) is str and bool(value)`, sans `strip()` ni normalisation.
- [x] 3.2 Vérifier qu'une chaîne composée uniquement d'espaces est acceptée comme référence opaque valide.
- [x] 3.3 Refuser `None`, chaîne vide, `True`, `False`, `0`, entier, objet, liste, tuple, `str` de sous-classe hostile et tout type non exact avant tout appel à `bool()`, `str()`, `len()` ou callback de l'objet fourni.
- [x] 3.4 Vérifier l'absence de grammaire, de préfixe imposé, de registre de noms, de vocabulaire canonique, de longueur maximale, de troncature et de transformation des références.
- [x] 3.5 Vérifier que la validation ne prouve ni légitimité, ni existence, ni résolution, ni classification de sensibilité des références trusted ou synthétiques.

## 4. Version de contrat

- [x] 4.1 Vérifier d'abord `type(contract_version) is str and bool(contract_version)` avant tout appel au parseur.
- [x] 4.2 Valider ensuite la version par le seul parseur public `parse_version` de `pixs.kernel.manifest.semver`, sans grammaire SemVer parallèle ni privée.
- [x] 4.3 Convertir uniquement les `ValueError` attendues du parseur en diagnostics fixes sans écho de la valeur.
- [x] 4.4 Propager toute exception inattendue du parseur ou de la validation, y compris `RuntimeError`, `KeyboardInterrupt` et `SystemExit`, sans capture générale ni transformation en refus normalisé.
- [x] 4.5 Vérifier que le contrat ne porte aucun champ version de composant et qu'aucune dépendance de version entre contrat et composant n'est introduite.

## 5. Diagnostics

- [x] 5.1 Vérifier que chaque refus porte `step=VALIDATE`, `element="event_contract.<champ>"` ou `event_contract.event`, et `constraint == message` statiques.
- [x] 5.2 Vérifier qu'un helper interne unique et privé fabrique les diagnostics et qu'aucune aide privée n'est exportée.
- [x] 5.3 Vérifier le tri stable, la déduplication et l'absence d'état partagé entre appels.
- [x] 5.4 Vérifier qu'aucune valeur d'entrée, SENTINEL, identifiant ou motif n'apparaît dans un élément, une contrainte ou un message.

## 6. Tests unitaires sûrs

- [x] 6.1 Publier exactement `tests/unit/test_event_contract.py` comme première source de tests du module.
- [x] 6.2 Couvrir les quatre exports exacts, les cinq champs dans l'ordre figé, l'absence de défauts, `frozen=True`, l'absence de `__post_init__`, la constructibilité des valeurs invalides et le refus d'assignation.
- [x] 6.3 Couvrir le cross-refus sur les instances exactes des deux classes avec compteur d'attribut réel : `__getattribute__` instrumenté temporairement sur la classe exacte, lecture effective du champ probée, compteur remis à zéro avant le validateur partenaire, vérification compteur nul après refus par l'unique diagnostic `event_contract.event` ; les sous-classes hostiles sont testées séparément.
- [x] 6.4 Couvrir les primitives hostiles champ par champ (`None`, vide, booléens, entier, liste, tuple, objet, sous-classe `str` comptant bool/len/str) refusées sans callback, et les chaînes d'espaces acceptées pour les références opaques ; une version non exacte ou vide ne doit jamais être transmise au parseur, tandis que la version valide est vérifiée indépendamment des autres champs.
- [x] 6.5 Couvrir `contract_version` : formes SemVer valides acceptées, invalides refusées par diagnostic fixe, spy du parseur public appelé sur la chaîne exacte sans transformation, `ValueError` attendue menant au diagnostic, `RuntimeError` et `BaseException` propagés à l'identique.
- [x] 6.6 Couvrir le lot de cinq champs invalides : cinq diagnostics uniques triés `event_contract.<champ>`, messages statiques, absence d'écho SENTINEL, listes fraîches et indépendantes, mutation de la première sans effet sur la suivante ni sur un nouvel appel.
- [x] 6.7 Couvrir le refus d'un objet quelconque, des deux sous-classes croisées et de tout non-instance avant tout callback.

## 7. Intégration sûre en processus frais

- [x] 7.1 Publier exactement `tests/integration/test_event_contract_integration.py`, sans créer `tests/integration/test_event_contract.py`.
- [x] 7.2 Lancer un interpréteur neuf `-B` avec environnement réduit déclaré (`PATH`, `LANG`, `PYTHONPATH=src`, `PYTHONDONTWRITEBYTECODE`), sans PG réel, sans URL, sans Git, sans secret.
- [x] 7.3 Armer avant l'import applicatif les sondes de fonctions, d'environnement, d'horloge et d'imports base ; armer les sondes fichiers seulement après les imports bootstrap normaux nécessaires et avant la construction/validation, sans exiger une absence absolue de toute activité physique d'import.
- [x] 7.4 Limiter les routes déclarées et propres aux ensembles finis suivants : fichiers `builtins.open`, `io.open`, `os.open`, `os.read`, `os.write`, `os.listdir`, `os.remove`, `os.fdopen`, `os.stat`, `os.scandir`, `os.unlink`, `os.rename` ; environnement routes déclarées de `os.environ` (`__getitem__`, `get`, `__iter__`, `__len__`, `__contains__`, `__setitem__`, `__delitem__`, `keys`, `values`, `items`, `copy`, `setdefault`, `pop`, `update`) et `os.getenv` ; horloge `datetime.datetime.now/today/utcnow`, `datetime.date.today`, `time.time/monotonic/perf_counter/localtime/gmtime/sleep` ; sockets `socket.socket.connect`, `socket.create_connection` ; processus `subprocess.Popen`, `subprocess.run`, `os.system`, `os.popen`, `os.execv`, `os.spawnl` ; imports `django`, `psycopg`, `psycopg2`, `psycopg_pool`, `psycopg_binary` et sous-modules. `os.openat` n'est pas une route déclarée.
- [x] 7.5 Éprouver chaque route déclarée (compteur un) puis la remettre à zéro avant la phase couverte ; contrôler les compteurs nuls après chaque phase sans masquer un accès applicatif par une remise à zéro.
- [x] 7.6 Conserver dans la classe d'horloge dérivée les méthodes standard non interdites, y compris le vrai `fromisoformat` calendaire ; n'affirmer aucune validation calendaire nouvelle dans ce scope.
- [x] 7.7 Importer les deux contrats dans le processus frais et éprouver les deux validateurs sur des contrats représentatifs : valides, cross-refus des instances exactes, version SemVer valide et refusée, opacités d'espaces.
- [x] 7.8 Limiter la sortie du sous-processus au marqueur fixe `EVENT_CONTRACT_SAFE_INTEGRATION_OK`, sans reproduction de valeur, diagnostic brut, environnement ou secret.
- [x] 7.9 Propager ou diagnostiquer explicitement toute erreur inattendue du sous-processus, sans capture générale ni masque de l'échec initial.

## 8. Compilations natives et exécution des tests

- [x] 8.1 Compiler nativement `src/pixs/kernel/event_contract.py` sous mandat distinct et vérifier son exit réel.
- [x] 8.2 Compiler nativement `tests/unit/test_event_contract.py` sous mandat distinct et vérifier son exit réel.
- [x] 8.3 Compiler nativement `tests/integration/test_event_contract_integration.py` sous mandat distinct et vérifier son exit réel.
- [x] 8.4 Exécuter les tests unitaires ciblés et vérifier leur exit réel et leur output complet.
- [x] 8.5 Exécuter le test d'intégration ciblé et vérifier son exit réel et son output complet.
- [x] 8.6 Exécuter la suite de deux cent cinquante-sept régressions sûres existantes, sans PG réel supplémentaire, pour préserver fanions, backend, source PostgreSQL, audit et dépendances déjà acquis.
- [x] 8.7 Vérifier que les ajouts de tests sont déterminés par les comportements réellement prouvés, sans nombre ni longueur imposé arbitrairement.

## 9. Périmètre, encodage et conformité OpenSpec

- [x] 9.1 Vérifier que le périmètre exact comprend les trois nouveaux chemins et aucun autre fichier source, test ou configuration modifié.
- [x] 9.2 Vérifier que les cinquante-huit fichiers de baseline exacts restent inchangés byte à byte : cinquante-deux du cycle audit précédent (norme canonique audit comprise), les trois sources du cycle audit, la norme canonique `events`, `contracts/models.py` et `contracts/__init__.py`.
- [x] 9.3 Vérifier l'encodage UTF-8 et les fins de ligne LF des trois nouveaux fichiers, sans CRLF ni secret.
- [x] 9.4 Vérifier que le delta normatif est la copie byte exact de la seule requirement canonique events « Événements immuables versionnés », y compris son Scenario « Contrat d'intégration séparé », sans norme nouvelle, modifiée ou supprimée.
- [x] 9.5 Vérifier l'absence de nouvelle dépendance, de package exporté, de README modifié, d'opération Git, de wire format, de persistance, de route, d'API runtime, de panneau admin, de PG réel supplémentaire et de politique d'audit.
- [x] 9.6 Exécuter la validation OpenSpec stricte du change avant la publication du code et après les tests.
- [x] 9.7 Exécuter la validation OpenSpec stricte canonique concernée avant la publication du code et après les tests.
- [x] 9.8 Vérifier qu'aucune tâche n'est cochée avant preuve observable de son exécution réussie.

Note de séquence : après tous les cochages, exécuter la validation stricte post-cochage ; obtenir ensuite une autorisation d'archivage unitaire distincte, exécuter l'archive, puis produire et vérifier séparément `STATISTIQUES.md` avec ses six sections, UTF-8/LF, totaux croisés et mesures `N/A` motivées. L'archivage et le rapport statistique ne constituent pas des tâches pré-cochage du souscycle.
