# Design — Représentation minimale d’un événement d’audit

## Contexte et décision

La norme canonique `audit` exige qu’un événement puisse représenter un contenu minimal. Ce change introduit seulement une représentation structurelle, pure et fermée dans le Kernel.

Il ne définit aucun wire format, aucune persistance, aucune politique de rétention, aucune minimisation, aucun panneau d’administration, aucune application aux événements de fanions et aucune obligation runtime de corrélation ou causalité.

Les références d’acteur, de tenant, de ressource, d’action, de résultat et de motif restent des valeurs opaques fournies par un caller trusted ou des valeurs synthétiques de test. La validation prouve la syntaxe structurelle, jamais la légitimité métier, la classification de sensibilité ou le masquage de données.

## Architecture

```text
caller trusted ou fixture synthétique
              ↓
AuditEvent immuable, construction structurelle
              ↓
validate_audit_event(event: object) -> list[Diagnostic]
              ↓
liste fraîche, triée et dédupliquée, sans écho de valeur
```

Aucune sortie n’est écrite, transmise, journalisée ou persistée. Aucun event n’est validé par un appel réseau, base, fichier, horloge ou environnement.

## Fichiers autorisés

```text
src/pixs/kernel/audit_event.py
tests/unit/test_audit_event.py
tests/integration/test_audit_event_integration.py
```

Les trois chemins sont nouveaux. Les quarante-neuf fichiers de baseline initiaux et les trois tests de dépendances complémentaires restent byte à byte inchangés, notamment :

- les contrats et validateurs `feature-flags` ;
- le codec et la source PostgreSQL ;
- les modèles, migrations et tests PostgreSQL déjà archivés ;
- les tests des parseurs SemVer et des diagnostics typés ;
- les README, réglages, routes, API et composants existants.

## API publique

```python
__all__ = [
    "AuditEvent",
    "validate_audit_event",
]
```

```python
@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    occurred_at: str
    actor_reference: str
    tenant_reference: str | None
    action: str
    resource_type: str
    resource_id: str
    result: str
    reason_or_error: str | None
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]
    component_id: str
    component_version: str
```

```python
def validate_audit_event(event: object) -> list[Diagnostic]:
    ...
```

Décisions :

- aucun autre export public ;
- aucun constructeur de validation, builder ou exception publique ;
- `AuditEvent` est purement structurel : les annotations ne valident pas et `__post_init__` est absent ;
- un objet structurellement invalide peut donc être construit ;
- `validate_audit_event` est le seul point fermé.

## Validation structurelle

Ordre retenu :

1. vérifier `type(event) is AuditEvent` ;
2. refuser une sous-classe ou un autre objet avant toute lecture d’attribut ;
3. inspecter les treize champs déclarés ;
4. agréger au plus un diagnostic par champ ;
5. trier et dédupliquer selon `(element, constraint, message)` ;
6. retourner une liste fraîche.

Pour un objet de type incorrect, un seul diagnostic est produite et les champs ne sont jamais lus. Les diagnostics portent l’étape `VALIDATE`, l’élément `audit_event.<champ>` et une contrainte constante.

## Chaînes opaques

Pour un champ obligatoire :

```python
type(value) is str and bool(value)
```

Pour un champ facultatif :

```python
value is None or (type(value) is str and bool(value))
```

Conséquences pour les champs obligatoires opaques (les champs facultatifs admettent `None`) :

- `False`, `True`, `0`, `None`, une liste, un tuple et tout objet hôte sont refusés par type exact ;
- une chaîne d’un ou plusieurs espaces est valide si le champ est opaque ;
- aucun `strip()`, `lstrip()`, repli Unicode, alias, normalisation ni transformation ;
- aucun vocabulaire n’est imposé pour `action`, `result`, `reason_or_error` ou une référence ;
- aucune longueur, quota, troncature ni politique de minimisation arbitraire.

Le booléen exact est refusé comme non-chaîne. Aucun `bool()` ou autre callback n’est invoqué avant la vérification du type exact.

## Champs minimaux

| Champ | Représentation |
|---|---|
| `event_id` | référence opaque de l’événement |
| `occurred_at` | horodatage UTC borné |
| `actor_reference` | référence opaque de l’acteur |
| `tenant_reference` | référence opaque ou `None` |
| `action` | libellé opaque sans vocabulaire canonique |
| `resource_type` | type de ressource opaque |
| `resource_id` | identité de ressource opaque |
| `result` | résultat opaque sans vocabulaire canonique |
| `reason_or_error` | motif ou code éventuel opaque, ou `None` |
| `correlation_ids` | tuple de références de corrélation |
| `causation_ids` | tuple de références de causalité |
| `component_id` | identifiant de composant validé par la grammaire publique |
| `component_version` | version SemVer validée par le parseur public |

## Horodatage UTC

Aucun validateur public de timestamp n’existant dans le Kernel, le module implémente une grammaire locale strictement identique à la convention canonique déjà employée :

```text
YYYY-MM-DDTHH:MM:SS[.fraction 1 à 6](Z | +00:00)
```

Contrôles :

- type exact `str` ;
- positions et séparateurs ASCII vérifiés ;
- chiffres ASCII aux positions numériques ;
- heure `00–23`, minute `00–59`, seconde `00–59` ;
- fraction optionnelle de un à six chiffres ;
- `Z` ou `+00:00` comme seul fuseau ;
- calendrier réel analysé par `datetime.fromisoformat` ;
- `utcoffset` vérifié UTC.

Aucune horloge n’est consultée. Seule une `ValueError` attendue de `datetime.fromisoformat` est convertie en diagnostic fixe. Toute autre exception est propagée.

## Composant et version

`component_id` est validé par la fonction publique :

```python
parse_requirement(value)
```

avec les conditions structurelles :

```python
requirement.constraints == ()
requirement.target_id == value
```

Cette règle reproduit la logique de validation d’un identifiant nu sans importer une fonction privée du module `manifest.models`.

`component_version` est validé par la fonction publique :

```python
parse_version(value)
```

Seules les `ValueError` attendues des parseurs publics sont converties en diagnostics fixes. Une erreur inattendue, une interruption ou un échec de programmation est propagé.

## Tuples de corrélation et de causalité

`correlation_ids` et `causation_ids` doivent être exactement des `tuple`. Chaque élément présent doit être une chaîne exacte non vide.

Décisions :

- un tuple vide est syntaxiquement permis ;
- cela ne constitue pas une preuve de la présence ou de l’absence d’une obligation runtime de corrélation ;
- aucun élément n’est trié, dédupliqué, normalisé ou tronqué ;
- aucun format `UUID`, `traceparent`, `operation_id`, tenant ou acteur n’est inventé ;
- une invalidité produit au plus un diagnostic pour le tuple, jamais un diagnostic indexé par élément.

## Diagnostics

Un helper interne unique fabrique chaque refus :

```python
Diagnostic(
    step=VALIDATE,
    element=f"audit_event.{field}",
    constraint=constraint,
    message=constraint,
)
```

Contraintes :

- messages statiques finis, nommant le champ et la règle ;
- aucune valeur d’entrée, identifiant, motif, SQL, environnement, secret ou cause technique ;
- tri stable par `(element, constraint, message)` ;
- déduplication de cette clé ;
- liste retournée neuve et indépendante à chaque appel ;
- les `Diagnostic` existants restent des chaînes compatibles avec les conventions du Kernel.

## Module et dépendances

`src/pixs/kernel/audit_event.py` peut importer :

- `dataclasses.dataclass` ;
- `datetime.datetime` et `datetime.timezone` ;
- la bibliothèque standard `re` si nécessaire pour la seule grammaire UTC, sans doublonner les parseurs composants ;
- `pixs.kernel.diagnostics.VALIDATE` et `Diagnostic` ;
- `pixs.kernel.manifest.semver.parse_requirement` et `parse_version`.

Le module ne doit pas :

- ouvrir ou lire de fichier ;
- consulter l’environnement ;
- importer Django ;
- importer PostgreSQL, psycopg ou un modèle ;
- utiliser une horloge, un socket ou un sous-processus ;
- utiliser une fonction privée d’un autre module ;
- produire une route, API, CLI, admin, cache ou politique d’audit ;
- exposer un wire format.

Sa docstring doit expliquer que les valeurs sont trusted ou synthétiques et que la validation est seulement structurelle.

## Tests unitaires

`tests/unit/test_audit_event.py` couvre les comportements réellement nécessaires, sans objectif numérique arbitraire.

Au minimum :

- `__all__` exactement `AuditEvent` et `validate_audit_event` ;
- treize champs exacts, ordre et absence de défauts ;
- modèle `frozen=True`, sans `__post_init__` ;
- construction structurelle des valeurs invalides sans exception immédiate ;
- refus par type exact avant toute lecture hostile ;
- sous-classe de `AuditEvent` refusée sans inspection de ses champs ;
- chaînes d’espaces valides comme références opaques ;
- refus de `False`, `True`, `None`, `0`, objet, liste et chaîne vide ;
- `None` admis pour `tenant_reference` et `reason_or_error` ;
- grammaire UTC valide et horodatages calendaires invalides ;
- bornes des positions, fraction et secondes ;
- `component_id` nu accepté, contraintes comparatives et cible divergente refusées ;
- `component_version` SemVer accepté et refusé ;
- tuples de corrélation et causalité vides admis ;
- éléments de tuple non exacts ou vides refusés sans écho ni index ;
- absence de tri, déduplication ou transformation des identifiants fournis ;
- tri et déduplication stables des diagnostics ;
- liste fraîche, indépendante et sans état partagé ;
- propagation des exceptions inattendues, y compris `KeyboardInterrupt` et `SystemExit` si déclenchées par un double explicitement autorisé ;
- absence de lecture d’un secret, d’un chemin, d’un environnement ou d’un flux.

## Intégration sûre

`tests/integration/test_audit_event_integration.py` exécute un processus Python neuf avec gardes réellement armées avant l’import, au minimum contre :

- fichiers et environnement ;
- horloge système ;
- sockets et connexions réseau ;
- subprocess ;
- base ou psycopg si des imports transitifs étaient tentés.

Les lectures normales du mécanisme d’import et son amorçage restent autorisés ; les gardes interdisent les E/S applicatives sensibles du module. Chaque route gardée est réellement appelée pour éprouver son armement, puis son compteur est remis à zéro. Une classe datetime dérivée patchable conserve le vrai `fromisoformat` calendaire et permet de garder `now`, `today` et `utcnow` sans modifier la classe immutable de la bibliothèque standard. Le subprocess valide un ou plusieurs events représentatifs. À la fin :

- les compteurs de garde restent nuls ;
- aucun effet de bord n’est observé ;
- la sortie est limitée à un marqueur fixe ;
- aucun PG réel, aucune URL, aucun Git, aucune configuration ni aucun secret n’est consulté.

Les gardes ne masquent pas les échecs : un appel interdit produit une erreur explicite sans reproduction de valeur.

## Validations et cycle

- trois compilations natives distinctes pour les trois nouveaux fichiers ;
- tests unitaires et intégration ciblés ;
- 192 tests sûrs de la baseline fanions/backend/PG, sans PG réel supplémentaire ;
- tests concernés des parseurs et diagnostics :
  - `tests/unit/test_semver_constraints.py` ;
  - `tests/unit/test_manifest_models.py` ;
  - `tests/unit/test_diagnostics_typed.py` ;
- strict OpenSpec avant publication du code ;
- strict après publication du code ;
- strict après cochage ;
- archivage sous mandat distinct ;
- rapport `STATISTIQUES.md` sous mandat séparé après archivage.

## Limites

- aucune action, résultat, motif ou code d’erreur normalisé ;
- aucun wire format JSON, TOML, HTTP ou binaire ;
- aucune validation d’acteur, tenant, ressource ou permission ;
- aucune preuve de redaction, minimisation ou classification de sensibilité ;
- aucune obligation d’un event à posséder une référence de corrélation ou de causalité ;
- aucune relation avec une mutation administrative réelle ;
- aucune persistance append-only, rétention, intégrité, purge ou consultation ;
- aucune complétion de `feature-flags` R4, administration, audit durable ou convergence des rôles.
