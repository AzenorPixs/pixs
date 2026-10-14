# Design — Représentation déclarative des contrats d'événement

## Contexte et décision

La requirement canonique events « Événements immuables versionnés » impose qu'un
événement porte type, version, producteur, schéma et périmètre d'ordre déclaré,
et que les contrats de domaine internes et d'intégration publics restent
distincts. Ce change introduit seulement une représentation structurelle pure et
fermée dans le Kernel, sur le patron `AuditEvent` déjà prouvé.

Aucun wire format, aucune publication, aucune persistance, aucun registre de
schémas, aucune enveloppe d'instance, aucun runtime de diffusion, aucune garantie
d'ordre effectif ne sont définis ici.

Faits observés autorisant ce design : `src/pixs` ne contient aucun module
event*.py ni `DomainEvent`/`EventContract` ; `pixs.kernel.diagnostics` expose
`VALIDATE` et `Diagnostic` publics ; `pixs.kernel.manifest.semver` expose le
parseur public `parse_version` ; `pixs.kernel.contracts` (modèle et façade) est
déjà publié et reste inchangé.

## Frontière explicite : norme directe, choix techniques, risques

Norme directe (exigée par le texte canonique) :
- porter type, version, producteur, schéma et périmètre d'ordre déclaré ;
- garder domaine interne et intégration publique comme contrats distincts ;
- version de contrat indépendante des versions de composants (TECH9) ;
- ne rien retirer ni modifier aux contrats existants (TECH8).

Choix techniques (réversibles, non normatifs) :
- cinq champs, deux validateurs et quatre exports publics ;
- opacité str sans grammaire pour les quatre références hors version ;
- réutilisation des seuls parseurs publics et du helper interne de diagnostic ;
- deux dataclasses symétriques plutôt qu'un type à catégorie inventée ;
- cross-refus par type exact avant lecture d'attribut.

Risques assumés et bornés :
- un flux réel d'exposition extérieure ne peut être prouvé qu'au runtime : seule
  la distinction structurelle des deux contrats est testée; le Scenario du flux
  extérieur reste non prouvé ;
- l'absence de grammaire pour les références laissent au caller trusted la
  charge de la cohérence des valeurs ;
- une évolution incompatible du champ version ou du périmètre d'ordre imposerait
  une version majeure séparée (TECH9), non engagée ici.

## Architecture

```text
caller trusted ou fixture synthétique
          ↓
DomainEventContract / IntegrationEventContract immuables, construction structurelle
          ↓
validate_domain_event_contract(event: object) -> list[Diagnostic]
validate_integration_event_contract(event: object) -> list[Diagnostic]
          ↓
liste fraîche, triée et dédupliquée, sans écho de valeur
```

Aucune sortie écrite, transmise, journalisée ni persistée. Aucun contrat validé
par appel réseau, base, fichier, horloge ou environnement.

## Fichiers autorisés

- `src/pixs/kernel/event_contract.py`
- `tests/unit/test_event_contract.py`
- `tests/integration/test_event_contract_integration.py`

Les trois chemins sont nouveaux. Les cinquante-huit fichiers de baseline exacts
restent byte à byte inchangés : cinquante-deux du cycle audit précédent (norme
canonique audit comprise), trois sources du cycle audit (`audit_event.py`,
`test_audit_event.py`, `test_audit_event_integration.py`), la norme canonique
`events`, `contracts/models.py` et `contracts/__init__.py`.

## API publique

Quatre exports exactement :

```python
__all__ = [
    "DomainEventContract",
    "IntegrationEventContract",
    "validate_domain_event_contract",
    "validate_integration_event_contract",
]
```

Deux dataclasses `frozen=True`, structurelles, sans `__post_init__`, sans défaut,
sans méthode applicative, sans conversion implicite et sans héritage entre elles :

```python
@dataclass(frozen=True)
class DomainEventContract:
    event_type: str
    contract_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str

@dataclass(frozen=True)
class IntegrationEventContract:
    event_type: str
    contract_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str
```

Ordre des cinq champs identique et figé : `event_type`, `contract_version`,
`producer_reference`, `schema_reference`, `order_scope_reference`.

## Validateurs

Un validateur par type, seul point fermé :

- vérifier `type(event) is DomainEventContract` (respectivement
  `IntegrationEventContract`) avant toute lecture d'attribut et avant tout
  callback ;
- cross-refus : `DomainEventContract` exact refusé par le validateur
  d'intégration, `IntegrationEventContract` exact refusé par le validateur de
  domaine, tout autre objet (y compris sous-classes) pareillement ; un seul
  diagnostic d'élément `event_contract.event` sans inspection d'aucun champ ;
- agréger au plus un refus par champ parmi les cinq ;
- tri stable et déduplication par `(element, constraint, message)` ;
- retourner une liste fraîche indépendante à chaque appel.

## Références opaques

Pour `event_type`, `producer_reference`, `schema_reference`,
`order_scope_reference` :

- `type(value) is str and bool(value)` — garde de type avant tout appel à
  `bool()`, `str()`, `len()` ou callback de l'objet fourni ;
- chaîne d'un ou plusieurs espaces valide ;
- aucune grammaire, aucun préfixe imposé, aucun registre de noms, aucun
  vocabulaire canonique, aucune longueur ni troncature ;
- aucune normalisation, aucun `strip()`, aucun repli Unicode, aucun alias ;
- valeurs fournies par un caller trusted ou des fixtures synthétiques : la
  validation prouve la forme, jamais la légitimité, l'existence, la résolution
  ni la sensibilité de la référence.

## Version de contrat

- garde d'abord : `type(value) is str and bool(value)` ;
- validation ensuite par le seul parseur public `parse_version` de
  `pixs.kernel.manifest.semver` ; aucune grammaire SemVer parallèle ni privée ;
- seules les `ValueError` attendues du parseur deviennent un diagnostic statique
  sans écho ; toute autre exception (dont `RuntimeError`, `KeyboardInterrupt`,
  `SystemExit`) est propagée sans capture générale ;
- version indépendante de toute version de composant : le contrat ne porte aucun
  champ version de composant.

## Diagnostics

Chaque refus est fabriqué par un helper interne privé unique :

- `step = VALIDATE` ;
- `element = f"event_contract.{champ}"` (ou `event_contract.event` pour le refus
  de type exact) ;
- `constraint = message` : contraintes statiques nommant le champ et la règle,
  préfixe suffisant pour rendre le champ compréhensible, sans reproduction
  d'aucune valeur, identifiant, environnement, cause technique ou secret ;
- au plus un diagnostic par champ ; tri/dédup stable ; liste fraîche.

## Imports et docstring

Imports autorisés : `__future__.annotations` si utilisé, `dataclasses.dataclass`,
`pixs.kernel.diagnostics.VALIDATE` et `Diagnostic`,
`pixs.kernel.manifest.semver.parse_version`. Aucun import de `parse_requirement`
(inutile ici). Aucune fonction privée d'un autre module. Les aides internes du
module restent privées et non exportées.

Docstring de module : les valeurs sont fournies par un caller trusted ou des
fixtures synthétiques ; la validation est seulement structurelle ; la
représentation est déclarative partielle ; elle ne remplace ni l'enregistrement,
ni `ContractDescriptor`, ni les garanties documentées d'un contrat public (TECH8) ;
elle ne définit aucune instance, payload ni enveloppe complète (TECH17), aucune
persistance, publication, audience effective, schéma effectif, ordre effectif,
outbox, transaction, idempotence, publisher ou runtime.

## Tests unitaires

Couverte par comportements réellement prouvés, sans cible numérique :

- quatre exports exacts ; cinq champs dans l'ordre figé, absence de défauts,
  `frozen=True`, absence de `__post_init__`, construction structurelle de
  valeurs invalides sans exception, immuabilité à l'assignation ;
- cross-refus avec preuve réelle de non-inspection : instance exacte de chaque classe, avec
  `__getattribute__` instrumenté temporairement sur cette classe; lecture
  effective du champ probée puis compteur remis à zéro avant le validateur
  partenaire, vérification compteur nul. Sous-classes hostiles testées séparément ; un seul
  diagnostic `event_contract.event`, step `VALIDATE` ;
- sous-classes hostiles refusées avant égalité, hash, longueur ou callback ;
- primitives hostiles par champ (`None`, vide, booléens, int, liste, tuple,
  objet, sous-classe `str` comptant bool/len/str) refusées sans callback ; seules
  les versions non exactes ou vides évitent le parseur. La version valide est
  vérifiée indépendamment des autres champs ;
- chaînes d'espaces acceptées comme références opaques valides ;
- `contract_version` : formes SemVer valides acceptées, invalides refusées par
  diagnostic fixe ; spy du parseur public appelé sur la chaîne fournie sans
  transformation ; side effect `ValueError` attendu menant à un diagnostic fixe ;
  side effects `RuntimeError` et `BaseException` propagés à l'identique ;
- liste refus de cinq champs invalides : cinq diagnostics uniques triés
  `event_contract.<champ>`, messages statiques, aucun écho SENTINEL, listes
  fraîches et indépendantes, mutation de la première sans effet sur la suivante ;
- refus d'un objet quelconque, d'une instance du type partenaire et des deux
  sous-classes croisées avant tout callback.

## Intégration sûre en processus frais

Le test lance un interpréteur neuf (`-B`, environnement réduit `PATH`, `LANG`,
`PYTHONPATH=src`) dont les sondes de fonctions, environnement, horloge et imports base sont armées
avant l'import applicatif. Les sondes fichiers sont armées après les imports
normaux nécessaires et avant la construction/validation. Chaque route déclarée
est éprouvée avec compteur un puis remise à zéro avant la phase couverte; les
compteurs sont contrôlés nuls après chaque phase sans masquer un accès applicatif :

- fichiers : `builtins.open`, `io.open`, `os.open/read/write/listdir/remove/
  fdopen/stat/scandir/unlink/rename` ;
- environnement : routes déclarées de `os.environ` (getitem, get, iter, len, contains,
  keys, values, items, copy, setdefault, pop, update, setitem, delitem) et
  `os.getenv` ;
- horloge : `datetime.datetime.now/today/utcnow`, `datetime.date.today`,
  `time.time/monotonic/perf_counter/localtime/gmtime/sleep` ; la classe dérivée
  conserve les autres méthodes standard; aucune validation calendaire nouvelle
  n'est revendiquée ;
- sockets : `socket.socket.connect`, `socket.create_connection` ;
- subprocess : `subprocess.Popen/run`, `os.system/popen/execv/spawnl` ;
- imports base : sonde `meta_path` refusant `django`, `psycopg`, `psycopg2`,
  `psycopg_pool`, `psycopg_binary` et leurs sous-modules.

Les lectures normales du mécanisme d'import et son amorçage restent autorisées ;
aucune absence absolue de toute activité physique d'import n'est exigée. Après
import des deux contrats, les deux validateurs éprouvent un ou plusieurs contrats
représentatifs : valides, cross-refus, version SemVer valide et refusée,
opacités d'espaces. La sortie est limitée au marqueur fixe
`EVENT_CONTRACT_SAFE_INTEGRATION_OK` ; aucun effet de bord, aucune valeur, aucun
secret, aucune URL, aucun PG réel, aucun Git.

## Validations et cycle

- trois compilations natives sous mandats distincts, exit réel observé ;
- tests unitaires et d'intégration ciblés, exit et output réels complets ;
- préservation des deux cent cinquante-sept régressions sûres existantes (deux
  cent trente-huit commande de régression, dix-huit unitaires audit, un
  intégration audit), sans PG réel supplémentaire ;
- vérification que les cinquante-huit fichiers de baseline exacts restent
  inchangés, et les trois nouveaux en UTF-8/LF sans secret ;
- validation OpenSpec stricte du change et canonique concernée avant le code,
  après les preuves, puis après cochage ; tâches cochées seulement après preuve
  observable ; archivage et `STATISTIQUES.md` sous mandats distincts ;
- aucune nouvelle dépendance, aucun export de paquet, aucun README, aucune
  route, aucune configuration, aucune opération Git non autorisés.

## Limites

- aucune catégorie ajoutée à l'énumeration des contrats, aucun usage d'un champ
  privé de `contracts` ;
- aucun wire format JSON, TOML, HTTP ou binaire ; aucun schéma de payload ;
- aucune enveloppe complète d'instance ni événement horodaté : ce contrat est
  déclaratif, l'instant d'un fait relève d'autres exigences (audit notamment) ;
- aucune preuve de l'exposition réelle vers l'extérieur, d'audience, de
  résolution de schéma, d'ordre effectif, de livraison, de transaction, de
  publication, d'idempotence ni de runtime ;
- les requirements events 2 et 3 ainsi que l'audit persistant, l'append-only, la
  minimisation, le panneau admin et les R4 fanions/runtime restent non prouvés ;
  ce change ne prétend à aucune complétude de capacité.
